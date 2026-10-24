"""Builds the Finance Toolkit MCP example on every function page of the Finance Toolkit docs.

Each function's spec in _data/financetoolkit_mcp/<module>.yml holds a question, the arguments of the MCP call that
answers it and how to chart the answer:

    get_return_on_equity:
      question: How has Apple's return on equity compared with Microsoft's and Alphabet's?
      tool: profitability
      arguments: {tickers: AAPL,MSFT,GOOGL, start_date: "2021-01-01", end_date: "2025-12-31"}
      chart: {format: percent}

This script runs every call against the Finance Toolkit MCP server in-process, the same code the hosted server runs,
and writes the answer as chart data to assets/data/financetoolkit-mcp/<module>/<function>.json. The function page
(_plugins/docs_metric_pages.rb) shows the question, the call and the chart.

    pip install "financetoolkit[mcp]"
    FINANCIAL_MODELING_PREP_KEY=... python _scripts/financetoolkit_mcp_examples.py [module ...] [--only get_a,get_b]

Chart options, all optional:
    type     bar or line; bar when there are 12 or fewer points on the x-axis, line otherwise
    format   percent, ratio, decimal (small values), multiple, amount, billions, usd, price or number (default ratio)
    x        the column that becomes the x-axis; by default the date column, else the period columns
    series   the column whose values name the series, for data with one row per date and ticker
    values   the value columns to draw (default: every numeric column)
    keep     {column: value or [values]}: only the rows that match
    drop     series to leave out; the benchmark is left out unless keep_benchmark is true
    rename   {old series name: new name}
    xdigits  decimals of numeric x labels, such as a strike grid
    transpose  true to swap the x-axis and the series (one statistic for several tickers: the tickers on the x-axis)
    last     only the last n points on the x-axis
    title    the chart title (default: the function's name in the sidebar)
    stack    true to stack the series

    type heatmap: x is the column of row labels, values the matrix columns; min, max, scale (sequential) and digits
    type coef:    x is the column of names, coef the estimates, error their standard errors (or low and high), p the
                  p-values
    type table:   for an answer that is text rather than numbers: values are the columns, rows how many rows to show,
                  cell_chars how much of a long text to keep (default 400 characters)
"""

import argparse
import asyncio
import fcntl
import json
import logging
import math
import os
import re
import sys
import time
import warnings
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parent.parent
SPECS = ROOT / "_data" / "financetoolkit_mcp"
OUTPUT = ROOT / "assets" / "data" / "financetoolkit-mcp"
REPORT = Path(os.environ.get("FT_MCP_REPORT", "/tmp/financetoolkit-mcp-examples"))
LOCK = Path(os.environ.get("FT_MCP_LOCK", "/tmp/financetoolkit-mcp-examples.lock"))
DATE_COLUMNS = ("Date", "date", "Period", "period", "Expiration", "expiration")
PERIOD = re.compile(r"^(\d{4}(-\d{2}(-\d{2})?)?|\d{4}Q[1-4]|\d{4}-Q[1-4]|\d{4}M\d{1,2}|\d{4}-W\d{2})$")

warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)


def is_period(name) -> bool:
    return bool(PERIOD.match(str(name)))


def number(value):
    """A value as a float rounded for the chart, or None for a gap."""
    if value is None or isinstance(value, bool):
        return None
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(value) or math.isinf(value):
        return None
    return round(value, 6 if abs(value) < 1 else 4) + 0.0  # + 0.0 turns -0.0 into 0.0


def records_of(text: str) -> pd.DataFrame:
    """The MCP answer (JSON records, or an object holding them) as a DataFrame."""
    data = json.loads(text)
    if isinstance(data, dict):
        # {"data": [...], "_notes": [...]}: the records, without the notes
        lists = [v for k, v in data.items() if isinstance(v, list) and not k.startswith("_") and v and isinstance(v[0], dict)]
        data = lists[0] if len(lists) == 1 else [{k: v for k, v in data.items() if not k.startswith("_")}]
    return pd.DataFrame(data)


def special_chart(frame: pd.DataFrame, options: dict, title: str) -> dict:
    """A heatmap (a matrix such as correlations), a coefficient plot (estimates with their intervals and p-values) or
    a table (an answer that is text rather than numbers)."""
    kind = options["type"]
    label = options.get("x") or next(c for c in frame.columns if not pd.api.types.is_numeric_dtype(frame[c]))
    if options.get("last_rows"):
        frame = frame.tail(int(options["last_rows"]))
    if options.get("rows"):
        frame = frame.head(int(options["rows"]))
    if kind == "heatmap":
        columns = options.get("values") or [c for c in frame.columns if c != label]
        chart = {"type": "heatmap", "x": [str(c) for c in columns], "y": frame[label].astype(str).tolist(),
                 "values": [[number(v) for v in row] for row in frame[columns].itertuples(index=False)]}
        for key in ("min", "max", "scale", "reverse", "digits"):
            if key in options:
                chart[key] = options[key]
    elif kind == "coef":
        coef = frame[options.get("coef", "Coefficient")].map(number)
        if options.get("low") and options.get("high"):
            low, high = frame[options["low"]].map(number), frame[options["high"]].map(number)
        else:
            error = frame[options.get("error", "Standard Error")].map(number)
            low, high = coef - 1.96 * error, coef + 1.96 * error
        chart = {"type": "coef", "x": frame[label].astype(str).tolist(), "coef": coef.round(6).tolist(),
                 "low": low.round(6).tolist(), "high": high.round(6).tolist(),
                 "p": frame[options.get("p", "P-Value")].map(number).tolist()}
    elif kind == "table":
        columns = options.get("values") or list(frame.columns)
        limit = int(options.get("cell_chars", 400))

        def cell(value):
            if isinstance(value, float):
                value = number(value)
                # a flag or a count reads as 1 or 250, not 1.0 or 250.0
                return int(value) if value is not None and value.is_integer() and abs(value) < 1e15 else value
            if value is None or (not isinstance(value, (list, dict)) and pd.isna(value)) or value in ("None", "nan", "NaN"):
                return ""
            # long text (a transcript) is cut, so the page shows how the answer starts
            return value if not isinstance(value, str) or len(value) <= limit else value[:limit].rsplit(" ", 1)[0] + " ..."

        rows = [[cell(v) for v in row] for row in frame[columns].itertuples(index=False)]
        rows = [row for row in rows if row[0] != ""]  # a row without its name says nothing
        rows = [row for i, row in enumerate(rows) if row not in rows[:i]]  # nor does the same row twice
        names = options.get("rename") or {}
        return {"type": "table", "columns": [str(names.get(c, c)) for c in columns], "rows": rows,
                "title": options.get("title") or title}
    else:
        raise ValueError(f"unknown chart type {kind}")
    names = options.get("rename") or {}
    for key in ("x", "y"):
        if key in chart:
            chart[key] = [names.get(v, v) for v in chart[key]]
    chart.update({"format": options.get("format", "ratio"), "title": options.get("title") or title, "period": False})
    return chart


def chart_of(frame: pd.DataFrame, options: dict, title: str) -> dict:
    """Turns an MCP answer into the x-axis and series of a bar or line chart."""
    frame = frame.copy()
    if options.get("type") in ("heatmap", "coef", "table"):
        for column, wanted in (options.get("keep") or {}).items():
            wanted = wanted if isinstance(wanted, list) else [wanted]
            frame = frame[frame[column].astype(str).isin([str(w) for w in wanted])]
        return special_chart(frame, options, title)
    for column, wanted in (options.get("keep") or {}).items():
        wanted = wanted if isinstance(wanted, list) else [wanted]
        frame = frame[frame[column].astype(str).isin([str(w) for w in wanted])]
    drop = set(options.get("drop") or [])
    if not options.get("keep_benchmark"):
        drop |= {"Benchmark", "benchmark"}
    # the benchmark and other dropped rows (a ticker column holding "Benchmark")
    texts = [c for c in frame.columns if not pd.api.types.is_numeric_dtype(frame[c])]
    if texts:
        frame = frame[~frame[texts].astype(str).isin(drop).any(axis=1)]
    if frame.empty:
        raise ValueError("no rows left after keep")

    x_column = options.get("x") or next((c for c in DATE_COLUMNS if c in frame.columns), None)
    by = options.get("series")
    if not by and x_column and frame[x_column].duplicated().any():
        # one row per date and ticker (or country, metric): those become the series
        by = next((c for c in frame.columns if c != x_column and not pd.api.types.is_numeric_dtype(frame[c])
                   and c not in DATE_COLUMNS and frame[c].nunique() > 1), None)
    numeric = [c for c in frame.columns
               if c not in (x_column, by) and c not in DATE_COLUMNS and pd.to_numeric(frame[c], errors="coerce").notna().any()]
    labels = [c for c in frame.columns if c not in numeric]
    periods = [c for c in numeric if is_period(c)]
    series = {}
    if not x_column and periods:
        # one row per ticker (and metric): the periods on the x-axis
        periods = options.get("values") or periods
        x = [str(p) for p in periods]
        ids = [c for c in labels if frame[c].nunique() > 1] or labels[:1]
        for _, row in frame.iterrows():
            key = " ".join(str(row[c]) for c in ids) if ids else title
            series[key] = [number(row[p]) for p in periods]
    else:
        # one row per date, ticker, country or instrument: that column on the x-axis
        x_column = x_column or (labels[0] if labels else None)
        values = options.get("values") or numeric
        if by:
            x = list(dict.fromkeys(frame[x_column].astype(str)))
            for name, part in frame.groupby(by, sort=False):
                part = part.drop_duplicates(x_column).set_index(part[x_column].astype(str).drop_duplicates())
                for value in values:
                    key = str(name) if len(values) == 1 else f"{name} {value}"
                    series[key] = [number(part[value].get(d)) for d in x]
        else:
            x = frame[x_column].astype(str).tolist() if x_column else [str(i) for i in frame.index]
            for value in values:
                series[str(value)] = [number(v) for v in frame[value]]

    series = {k: v for k, v in series.items() if k not in drop and not any(k.startswith(f"{d} ") for d in drop)}
    if options.get("transpose"):
        # one x category with a series per ticker reads better as the tickers on the x-axis
        series, x = {xi: [series[k][i] for k in series] for i, xi in enumerate(x)}, list(series)
    if options.get("rename"):
        series = {options["rename"].get(k, k): v for k, v in series.items()}
        x = [options["rename"].get(v, v) for v in x]
    # leave out the points where every series is empty, then keep the last n
    keep = [i for i in range(len(x)) if any(v[i] is not None for v in series.values())]
    if options.get("last"):
        keep = keep[-int(options["last"]):]
    if not keep or not series:
        raise ValueError("nothing to chart")
    x = [x[i] for i in keep]
    if options.get("xdigits") is not None:
        # numeric x labels (a strike grid) rounded for the axis
        x = [f"{float(v):.{int(options['xdigits'])}f}" if re.match(r"^-?[\d.]+$", str(v)) else v for v in x]
    series = {k: [v[i] for i in keep] for k, v in series.items()}
    chart = {
        "type": options.get("type") or ("bar" if len(x) <= 12 else "line"),
        "x": x,
        "series": [{"name": k, "data": v} for k, v in series.items()],
        "format": options.get("format", "ratio"),
        "title": options.get("title") or title,
        "period": False,
    }
    for key in ("stack", "xname", "format2"):
        if key in options:
            chart[key] = options[key]
    return chart


NAVIGATION = {"toolkit": ("financetoolkit-docs", ""), "discovery": ("financetoolkit-docs-discovery", "/discovery"),
              "ratios": ("financetoolkit-docs-ratios", "/ratios"), "models": ("financetoolkit-docs-models", "/models"),
              "options": ("financetoolkit-docs-options", "/options"),
              "technicals": ("financetoolkit-docs-technicals", "/technicals"),
              "fixedincome": ("financetoolkit-docs-fixedincome", "/fixedincome"),
              "risk": ("financetoolkit-docs-risk", "/risk"), "performance": ("financetoolkit-docs-performance", "/performance"),
              "econometrics": ("financetoolkit-docs-econometrics", "/econometrics"),
              "economics": ("financetoolkit-docs-economics", "/economics"),
              "portfolio": ("financetoolkit-docs-portfolio", "/portfolio")}


def titles(module: str) -> dict:
    """Function name to its name in the docs sidebar, the page title."""
    key, path = NAVIGATION[module]
    prefix = f"/projects/financetoolkit/docs{path}#"
    found = {}

    def walk(items):
        for item in items or []:
            url = str(item.get("url", ""))
            if url.startswith(prefix):
                found.setdefault(url.split("#", 1)[1].lower(), str(item.get("title", "")).strip())
            walk(item.get("children"))

    walk(yaml.safe_load((ROOT / "_data" / "navigation.yml").read_text()).get(key))
    return found


async def call(mcp, tool: str, arguments: dict) -> str:
    result = await mcp.call_tool(tool, arguments)
    blocks = result[0] if isinstance(result, tuple) else result.content
    return "".join(getattr(b, "text", "") for b in blocks)


async def build(modules: list[str], only: set[str]) -> int:
    from financetoolkit.mcp_server.mcp_controller import mcp

    failures = 0
    REPORT.mkdir(parents=True, exist_ok=True)
    for module in modules:
        specs = yaml.safe_load((SPECS / f"{module}.yml").read_text()) or {}
        names = titles(module)
        report = {}
        for function, spec in specs.items():
            if only and function not in only:
                continue
            arguments = {"indicator": function, **(spec.get("arguments") or {})}
            started = time.time()
            try:
                text = await call(mcp, spec["tool"], arguments)
                (REPORT / f"{module}.{function}.txt").write_text(text)
                chart = chart_of(records_of(text), spec.get("chart") or {}, names.get(function.lower(), function))
                target = OUTPUT / module / f"{function}.json"
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(json.dumps({"charts": {function: chart}}, separators=(",", ":")))
                report[function] = {"ok": True, "points": len(chart.get("x") or chart.get("rows") or []),
                                    "series": [s["name"] for s in chart.get("series", [])],
                                    "seconds": round(time.time() - started, 1)}
            except Exception as error:  # noqa: BLE001 - every failure is reported, the rest still runs
                failures += 1
                report[function] = {"ok": False, "error": f"{type(error).__name__}: {error}"[:600]}
            status = "ok" if report[function]["ok"] else "FAILED " + report[function]["error"][:200]
            print(f"{module}.{function}: {status}", flush=True)
        previous = REPORT / f"{module}.json"
        merged = json.loads(previous.read_text()) if previous.exists() and only else {}
        merged.update(report)
        previous.write_text(json.dumps(merged, indent=1))
    return failures


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("modules", nargs="*", help="modules to build (default: all)")
    parser.add_argument("--only", default="", help="comma-separated functions to build")
    args = parser.parse_args()
    modules = args.modules or sorted(p.stem for p in SPECS.glob("*.yml"))
    only = {f.strip() for f in args.only.split(",") if f.strip()}
    os.environ.setdefault("FINANCIAL_MODELING_PREP_KEY", os.environ.get("FINANCIAL_MODELING_PREP_API_KEY", ""))
    # one run at a time, so parallel runs don't compete for the API limit and memory
    with LOCK.open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        failures = asyncio.run(build(modules, only))
    print(f"{failures} failed")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
