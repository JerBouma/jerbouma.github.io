"""Builds the charts on the Finance Toolkit method pages.

Each method page shows its docstring example and the table it returns. Where a
chart says more than that table (a daily indicator whose table holds its last
five days), _data/financetoolkit_docs_charts.yml says what to plot. This script
runs the page's example over its whole period and writes one file per chart to
assets/data/financetoolkit-docs-charts/<module>/<function>.json, which the page
draws next to the table (Chart and Table tabs).

    FINANCIAL_MODELING_PREP_KEY=... python _scripts/financetoolkit_docs_charts.py [module.function ...]
    FINANCIAL_MODELING_PREP_KEY=... python _scripts/financetoolkit_docs_charts.py --outputs [module.function ...]

The second form writes only the full result of every other example that its
docstring shortens (.tail(), .head() or a slice of rows at the end).

The chart keys in the YAML:

    expr      the expression whose result is plotted; defaults to the example's
              last line without its .tail()
    ticker    for results with a ticker level in the columns: that ticker's columns
    columns   the columns to plot, in this order ({old: new} renames one)
    price     add the Close of this ticker (overlays such as bands and averages)
    last      the number of rows to plot, counted from the end (default all)
    kind      line (default), bar or area
    levels    reference lines, such as [30, 70] or [0]
    cloud     two series names to shade between (bands, channels)
    colors    {series: "#rrggbb"} for series whose colour carries meaning
    dots      series drawn as dots, not lines (the Parabolic SAR)
    split     {column, by, names: {value: name}}: one series per state of `by`
    format    the number format (see assets/js/ft-charts.js)
    title     the chart title; subtitle: a line under it on how to read it

A technical indicator is drawn the way it usually is (chart: ta): the price of
`price` as candlesticks with `overlays` on it ([{column, color, dashed, dots}],
`fill` shading between two of them), and `lower`: the indicator in its own panel
({series: [{column, bar, signed, color}], levels, min, max, format}). `derive`
adds columns from the result ({name: "f['A'] - f['B']"}) and `zoom` sets how
many days show at first. The full result is also written to
_financetoolkit_docs_outputs/<module>/<function>.json for the page's table.
"""

import json
import logging
import os
import re
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)

ROOT = Path(__file__).resolve().parent.parent
SPECS = ROOT / "_data" / "financetoolkit_docs_charts.yml"
DOCS = ROOT / "_pages" / "financetoolkit" / "documentation"
OUTPUT = ROOT / "assets" / "data" / "financetoolkit-docs-charts"
TABLES = ROOT / "_financetoolkit_docs_outputs"
API_KEY = os.environ.get("FINANCIAL_MODELING_PREP_KEY", "")
# how a docstring shortens its example's result: the last rows, the first rows or a
# slice of rows at the end of the call (the same pattern is in _plugins/docs_metric_pages.rb)
ROW_CUT = re.compile(r"\.(?:tail|head)\(\d*\)\s*$|\.iloc\[(?:\[[^\]]*\]|[^\],\[]*)\]\s*$")
MAX_ROWS = 2000


def example_code(module: str, function: str) -> str:
    """The Python example of a function's section on its module's docs page."""
    page = (DOCS / f"{module}.md").read_text()
    section = re.search(rf"^## {re.escape(function)}\n(.*?)(?=^## |\Z)", page, re.S | re.M)
    if not section:
        raise KeyError(f"{module}.{function} is not on the docs page")
    code = re.search(r"```python\n(.*?)```", section.group(1), re.S)
    if not code:
        raise KeyError(f"{module}.{function} has no example")
    return code.group(1)


def run(code: str, expr: str | None):
    """Run the example and return what it plots: expr, or its last statement without .tail()."""
    code = code.replace('"FINANCIAL_MODELING_PREP_KEY"', "__API_KEY__").replace("'FINANCIAL_MODELING_PREP_KEY'", "__API_KEY__")
    lines = code.rstrip().split("\n")
    # the last statement can span lines: everything from its first unindented line
    start = max(i for i, line in enumerate(lines) if line and not line[0].isspace() and not line.startswith(")"))
    body, last = "\n".join(lines[:start]), "\n".join(lines[start:])
    scope = {"__API_KEY__": API_KEY}
    exec(body, scope)
    if expr is None:
        expr = ROW_CUT.sub("", last.strip())
        if re.match(r"^\w+\s*=", expr):  # an assignment: plot the variable it sets
            exec(expr, scope)
            expr = expr.split("=", 1)[0].strip()
    return eval(expr, scope), scope


def label(value) -> str:
    if isinstance(value, pd.Period):
        return value.end_time.strftime("%Y-%m-%d") if value.freqstr.startswith("W") else str(value)
    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d %H:%M") if value.hour or value.minute else value.strftime("%Y-%m-%d")
    return str(value)


def numbers(series: pd.Series) -> list:
    return [None if pd.isna(v) or np.isinf(v) else float(f"{float(v):.6g}") for v in series]


def table(result) -> dict:
    """The example's full result as rows for the docs page's table (at most MAX_ROWS)."""
    frame = result.to_frame() if isinstance(result, pd.Series) else result
    total = len(frame)
    frame = frame.iloc[:MAX_ROWS]
    columns = [" / ".join(map(str, c)) if isinstance(c, tuple) else str(c) for c in frame.columns]
    rows = [[label(i)] + [None if pd.isna(v) else (float(f"{float(v):.6g}") if isinstance(v, (int, float, np.number)) else str(v)) for v in row]
            for i, row in zip(frame.index, frame.itertuples(index=False))]
    return {"index": frame.index.name or "", "columns": columns, "rows": rows, "total": total}


def ta_chart(spec: dict, result, scope) -> dict:
    """Price candles with overlays, and an indicator panel below (the usual way to draw technicals)."""
    frame = result.to_frame() if isinstance(result, pd.Series) else result
    if spec.get("ticker") and isinstance(frame.columns, pd.MultiIndex):
        frame = frame.xs(spec["ticker"], level=1, axis="columns")
    frame = frame.rename(columns=spec.get("rename", {})).copy()
    # columns drawn from the result, such as the MACD histogram or the Supertrend per trend
    for name, expression in spec.get("derive", {}).items():
        frame[name] = eval(expression, {"f": frame, "pd": pd, "np": np})
    ohlc = None
    if spec.get("price"):
        ticker = spec["price"]
        history = scope["toolkit"].get_historical_data(period=spec.get("price_period", "daily"))
        pick = lambda column: history[column][ticker] if isinstance(history[column], pd.DataFrame) else history[column]
        ohlc = pd.DataFrame({c: pick(c) for c in ["Open", "Close", "Low", "High"]}).reindex(frame.index)
        # days the instrument did not trade (another market's holiday) would break every line;
        # days after its last price stay, for indicators projected forward (the Ichimoku cloud)
        traded = ohlc.notna().all(axis=1)
        keep = traded | (frame.index > traded[traded].index.max())
        frame, ohlc = frame[keep], ohlc[keep]
    start = frame.notna().any(axis=1).idxmax()
    frame = frame[start:]
    # a missing value inside a line breaks it; fill short interior gaps
    frame = frame.apply(lambda c: c.interpolate(limit=5, limit_area="inside") if pd.api.types.is_numeric_dtype(c) and c.notna().sum() > 1 else c)
    out = {"type": "ta", "title": spec["title"], "x": [label(v) for v in frame.index], "format": spec.get("format", "ratio")}
    if ohlc is not None:
        ohlc = ohlc[start:]
        out["priceName"] = spec.get("price_name", spec["price"])
        out["ohlc"] = [None if r.isna().any() else [float(f"{v:.6g}") for v in r] for _, r in ohlc.iterrows()]

    def series(items):
        return [dict({"name": i.get("name", i["column"]), "data": numbers(frame[i["column"]])},
                     **{k: v for k, v in i.items() if k not in ("column", "name")}) for i in items]

    out["overlays"] = series(spec.get("overlays", []))
    if spec.get("lower"):
        low = spec["lower"]
        out["lower"] = {k: v for k, v in low.items() if k != "series"}
        out["lower"]["series"] = series(low["series"])
    for key in ("fill", "fill_colors", "subtitle", "zoom"):
        if key in spec:
            out[key] = spec[key]
    return out


def chart(module: str, function: str, spec: dict) -> dict:
    result, scope = run(example_code(module, function), spec.get("expr"))
    if spec.get("chart") == "ta":
        return ta_chart(spec, result, scope), table(result)
    frame = result.to_frame() if isinstance(result, pd.Series) else result
    if spec.get("ticker") and isinstance(frame.columns, pd.MultiIndex):
        frame = frame.xs(spec["ticker"], level=1, axis="columns")
    if spec.get("price"):
        prices = scope["toolkit"].get_historical_data()["Close"]
        if isinstance(prices, pd.DataFrame):  # one column per ticker unless there is only one
            prices = prices[spec["price"]]
        # on the indicator's own dates, so no line breaks on a day only the price has
        frame = pd.concat([prices.rename("Close").reindex(frame.index), frame.drop(columns="Close", errors="ignore")], axis=1)
    split = spec.get("split")
    if split:  # one line per state, such as the Supertrend in an uptrend and in a downtrend
        state = frame[split["by"]]
        for value, name in split["names"].items():
            frame[name] = frame[split["column"]].where(state == value)
    columns = spec.get("columns")
    if columns:
        renames = {}
        for column in columns:
            if isinstance(column, dict):
                renames.update(column)
        frame = frame[[next(iter(c)) if isinstance(c, dict) else c for c in columns]].rename(columns=renames)
    frame = frame.dropna(how="all")
    if spec.get("last"):
        frame = frame.iloc[-spec["last"]:]
    # a day one market was closed (another's holiday in the index) would break a line
    if spec.get("kind") != "bar":
        frame = frame.apply(lambda column: column.interpolate(limit=5, limit_area="inside") if column.notna().sum() > 1 else column)
    x = [label(v) for v in frame.index]
    series = [{"name": str(name), "data": numbers(frame[name])} for name in frame.columns]
    for se in series:
        if se["name"] in spec.get("dots", []):
            se["dots"] = True
        if se["name"] in spec.get("colors", {}):
            se["color"] = spec["colors"][se["name"]]
    if spec.get("kind") == "area":
        for se in series:
            se["area"] = True
    for level in spec.get("levels", []):
        series.append({"name": str(level), "data": [level] * len(x), "reference": True})
    out = {
        "type": "bar" if spec.get("kind") == "bar" else "line",
        "title": spec["title"],
        "x": x,
        "series": series,
        "format": spec.get("format", "ratio"),
    }
    if "Close" in frame.columns and len(frame.columns) > 1:
        out["overlay"] = True  # the price drawn as the main line, the indicator around it
    for key in ("subtitle", "cloud", "log", "stack"):
        if key in spec:
            out[key] = spec[key]
    return out, table(result)


def shortened_examples() -> list[tuple[str, str]]:
    """Every (module, function) whose docstring example ends by shortening its result."""
    found = []
    for page in sorted(DOCS.glob("*.md")):
        for section in re.split(r"(?m)^## ", page.read_text())[1:]:
            code = re.search(r"```python\n(.*?)```", section, re.S)
            if code and ROW_CUT.search(code.group(1).rstrip()):
                found.append((page.stem, section.split("\n", 1)[0].strip()))
    return found


def outputs(only: list[str], specs: dict) -> None:
    """The full result of the shortened examples without a chart of their own."""
    failed = []
    for module, function in shortened_examples():
        key = f"{module}.{function}"
        if key in specs or (only and key not in only):
            continue
        try:
            result, _ = run(example_code(module, function), None)
            rows = table(result)
        except Exception as error:
            failed.append(f"{key}: {type(error).__name__}: {str(error)[:200]}")
            continue
        path = TABLES / module / f"{function}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(rows, separators=(",", ":")))
        print(f"{key}: {rows['total']} rows")
    for line in failed:
        print("FAILED", line, file=sys.stderr)


def main(only: list[str]) -> None:
    specs = yaml.safe_load(SPECS.read_text())
    failed = []
    for key, spec in specs.items():
        if only and key not in only:
            continue
        module, function = key.split(".")
        try:
            data, rows = chart(module, function, spec)
        except Exception as error:  # keep the previous file when a call fails
            failed.append(f"{key}: {type(error).__name__}: {error}")
            continue
        path = OUTPUT / module / f"{function}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"charts": {function: data}}, separators=(",", ":")))
        # the full result, which the docs page shows as its table (the docstring shows its end)
        full = TABLES / module / f"{function}.json"
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(json.dumps(rows, separators=(",", ":")))
        print(f"{key}: {len(data['x'])} points")
    for line in failed:
        print("FAILED", line, file=sys.stderr)


if __name__ == "__main__":
    if sys.argv[1:2] == ["--outputs"]:
        outputs(sys.argv[2:], yaml.safe_load(SPECS.read_text()))
    else:
        main(sys.argv[1:])
