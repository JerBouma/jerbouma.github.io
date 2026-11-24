"""Builds the charts on the Finance Toolkit method pages.

Each method page shows its docstring example and the table it returns. Where a
chart says more than that table (a daily indicator whose table holds its last
five days), _data/financetoolkit_docs_charts.yml says what to plot. This script
runs the page's example over its whole period and writes one file per chart to
assets/data/financetoolkit-docs-charts/<module>/<function>.json, which the page
draws next to the table (Chart and Table tabs).

    FINANCIAL_MODELING_PREP_KEY=... python _scripts/financetoolkit_docs_charts.py [module.function ...]

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
API_KEY = os.environ.get("FINANCIAL_MODELING_PREP_KEY", "")


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
        expr = re.sub(r"\.tail\(\d*\)\s*$", "", last.strip())
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


def chart(module: str, function: str, spec: dict) -> dict:
    result, scope = run(example_code(module, function), spec.get("expr"))
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
    return out


def main(only: list[str]) -> None:
    specs = yaml.safe_load(SPECS.read_text())
    failed = []
    for key, spec in specs.items():
        if only and key not in only:
            continue
        module, function = key.split(".")
        try:
            data = chart(module, function, spec)
        except Exception as error:  # keep the previous file when a call fails
            failed.append(f"{key}: {type(error).__name__}: {error}")
            continue
        path = OUTPUT / module / f"{function}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"charts": {function: data}}, separators=(",", ":")))
        print(f"{key}: {len(data['x'])} points, {len(data['series'])} series")
    for line in failed:
        print("FAILED", line, file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
