"""Builds the charts and full tables on the Finance Toolkit method pages.

Every method page shows its docstring example, then what it returns as a Chart and
a Table tab. _data/financetoolkit_docs_charts/<module>.yml defines per method how
that result is usually plotted; this script runs the page's example in full (a
docstring may shorten it with .tail(), .head() or a slice of rows) and writes

    assets/data/financetoolkit-docs-charts/<module>/<function>.json   the chart
    _financetoolkit_docs_outputs/<module>/<function>.json             the full table

    FINANCIAL_MODELING_PREP_KEY=... python _scripts/financetoolkit_docs_charts.py [module | module.function ...]
    FINANCIAL_MODELING_PREP_KEY=... python _scripts/financetoolkit_docs_charts.py --outputs [module.function ...]

The second form writes only the full table of the shortened examples that have no
spec. FT_DOCS_CHART_SPECS points the script at another folder of specs (for tests).

A spec, keyed by function name:

    chart     line (default), bar, area, hbar, scatter, heatmap, coef, tabs, ta or none
    title     what is plotted, without a conclusion or a period ("Gross Margin")
    subtitle  optional: the unit, how it is built or how to read it; never the numbers
    reason    for chart: none, why the result has no chart (text, one value, a list)
    expr      the expression to chart and tabulate, when not the example's last statement
    chart_expr  an expression for the chart only (the table stays the example's result),
              such as the same call with more decimals

Shaping the result into x (index) and series (columns), in this order:

    ticker    keep one value of a MultiIndex level (level: 1 by default; columns, else rows)
    transpose turn rows into series (a ticker per row, years as columns: transpose: true)
    latest    keep only the last row (applied before transpose): the latest reading per ticker
    x         a column to use as the x axis (set_index)
    rows      keep and order rows; {old: new} renames one
    drop      rows to leave out, such as [Total]
    derive    new columns, {name: "f['A'] - f['B']"} (f is the frame)
    columns   keep and order columns; {old: new} renames one
    first / last   keep the first or last n rows; sort: asc or desc by the first column

Drawing:

    format    percent (fractions), ratio (2 decimals), decimal, number (1 decimal), amount,
              compact (1.2B), multiple (12.3x), usd, price; format2 for axis2
    axis2     series on a second value axis; area: series drawn as areas; dots: as dots
    colors    {series: "#rrggbb"}; levels: reference lines [0] or [30, 70]
    zones     shaded value ranges: [{from, to, label, tone: bad|mid|good}] (open ends allowed)
    stack     stack the series (bar or area); log: a log value axis; xname / yname: axis titles
    hbar      one column as horizontal bars per row (rankings, weights), sort: desc
    scatter   xcol and ycol: a point per row, labelled with the row name; xname, yname
    heatmap   the frame as a matrix (rows down, columns across); min, max, scale: sequential
    coef      coef (column), se or low and high, p: a dot per row with its 95% interval
    tabs      [{label, ...spec}]: several views of one result, each shaped on its own

A technical indicator is drawn the way charting packages draw it (chart: ta): the
price of `price` as candlesticks with `overlays` on it ([{column, name, color,
dashed, dots, step}], `fill` shading between two of them, `fill_colors` for a
two-coloured cloud), and `lower`: the indicator in its own panel ({series:
[{column, name, bar, signed, color}], levels, min, max, format}). `price_period`
sets the candles' period and `zoom` how many of them show at first. Without
`price`, the overlays are drawn on their own (a market's breadth).
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
SPECS = Path(os.environ.get("FT_DOCS_CHART_SPECS", ROOT / "_data" / "financetoolkit_docs_charts"))
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
    start = max(i for i, line in enumerate(lines) if line and not line[0].isspace() and not line.startswith((")", "]", "}")))
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


def flat(value) -> str:
    """A label for an index or column value, tuples joined (('AAPL', '2025') -> AAPL · 2025)."""
    if isinstance(value, tuple):
        return " · ".join(label(v) for v in value)
    return label(value)


def select(frame: pd.DataFrame, items: list, axis: str) -> pd.DataFrame:
    """Keep and order rows or columns; an item {old: new} also renames it."""
    keys, renames = [], {}
    for item in items:
        if isinstance(item, dict):
            (old, new), = item.items()
            keys.append(old)
            renames[old] = new
        else:
            keys.append(item)
    if axis == "rows":
        # a row of a MultiIndex can also be named as it prints: "('AAPL', '2025')" or "AAPL · 2025"
        printed = {}
        for value in frame.index:
            if isinstance(value, tuple):
                printed[str(value)] = value
                printed[flat(value)] = value
        keys = [printed.get(k, k) if isinstance(k, str) else k for k in keys]
        renames = {printed.get(k, k) if isinstance(k, str) else k: v for k, v in renames.items()}
        frame = frame.loc[keys]
        frame.index = [renames.get(i, i) for i in frame.index]
        return frame
    return frame[keys].rename(columns=renames)


def shaped(spec: dict, result) -> pd.DataFrame:
    """The result reshaped to what the chart draws: x in the index, one column per series."""
    frame = result.to_frame() if isinstance(result, pd.Series) else result.copy()
    if spec.get("ticker") is not None:
        level = spec.get("level", 1)
        if isinstance(frame.columns, pd.MultiIndex):
            frame = frame.xs(spec["ticker"], level=level, axis="columns")
        else:
            frame = frame.xs(spec["ticker"], level=level, axis="index")
    if spec.get("latest"):  # only the last row, before transpose: the latest reading per ticker
        frame = frame.iloc[[-1]]
    if spec.get("transpose"):
        frame = frame.T
    if spec.get("x"):
        frame = frame.set_index(spec["x"])
    if spec.get("rows"):
        frame = select(frame, spec["rows"], "rows")
    if spec.get("drop"):  # rows left out, such as a Total
        frame = frame.drop(index=spec["drop"], errors="ignore")
    for name, expression in spec.get("derive", {}).items():
        frame[name] = eval(expression, {"f": frame, "pd": pd, "np": np})
    if spec.get("columns"):
        frame = select(frame, spec["columns"], "columns")
    frame.columns = [flat(c) for c in frame.columns]
    frame.index = [flat(i) for i in frame.index]
    frame = frame.apply(pd.to_numeric, errors="coerce") if spec.get("chart") not in ("scatter",) else frame
    frame = frame.dropna(how="all")
    if spec.get("sort"):  # before first/last, so first: 10 with sort: desc keeps the ten largest
        frame = frame.sort_values(frame.columns[0], ascending=spec["sort"] == "asc")
    if spec.get("first"):
        frame = frame.iloc[: spec["first"]]
    if spec.get("last"):
        frame = frame.iloc[-spec["last"]:]
    return frame


def plot(spec: dict, result, scope) -> dict:
    """A chart other than a technical one (see the module docstring for the keys)."""
    kind = spec.get("chart", "line")
    out = {"title": spec["title"]}
    if kind == "tabs":  # several views of one result, such as the ratios of a collect_ method
        out["type"] = "tabs"
        out["tabs"] = [dict(plot(dict(tab, title=tab.get("label", spec["title"])), result, scope), label=tab["label"])
                       for tab in spec["tabs"]]
        return out
    frame = shaped(spec, result)
    if kind == "hbar":
        out.update(type="hbar", x=list(frame.index), series=[{"name": frame.columns[0], "data": numbers(frame.iloc[:, 0])}])
    elif kind == "scatter":
        xs, ys = spec["xcol"], spec["ycol"]
        out.update(type="scatter", xname=spec.get("xname", xs), yname=spec.get("yname", ys),
                   points=[{"name": str(i), "x": float(r[xs]), "y": float(r[ys])} for i, r in frame.iterrows()
                           if pd.notna(r[xs]) and pd.notna(r[ys])])
        for point in out["points"]:  # positions: {name: left|top|bottom|topleft|bottomleft} for crowded labels
            if point["name"] in spec.get("positions", {}):
                point["pos"] = spec["positions"][point["name"]]
    elif kind == "heatmap":
        out.update(type="heatmap", x=list(frame.columns), y=list(frame.index),
                   values=[numbers(frame.loc[i]) for i in frame.index])
    elif kind == "coef":
        coef = frame[spec.get("coef", "Coefficient")]
        if spec.get("se"):
            low, high = coef - 1.96 * frame[spec["se"]], coef + 1.96 * frame[spec["se"]]
        else:
            low, high = frame[spec["low"]], frame[spec["high"]]
        pvalues = frame[spec["p"]] if spec.get("p") else pd.Series(0.0, index=frame.index)
        out.update(type="coef", x=list(frame.index), coef=numbers(coef), low=numbers(low), high=numbers(high), p=numbers(pvalues))
    else:  # line, bar or area over the index
        if kind != "bar":  # a day one market was closed would break a line
            frame = frame.apply(lambda c: c.interpolate(limit=5, limit_area="inside") if c.notna().sum() > 1 else c)
        series = [{"name": name, "data": numbers(frame[name])} for name in frame.columns]
        for se in series:
            if kind == "area" or se["name"] in spec.get("area", []):
                se["area"] = True
            if se["name"] in spec.get("dots", []):
                se["dots"] = True
            if se["name"] in spec.get("axis2", []):
                se["axis"] = 1
            if se["name"] in spec.get("colors", {}):
                se["color"] = spec["colors"][se["name"]]
        for level in spec.get("levels", []):
            series.append({"name": str(level), "data": [level] * len(frame), "reference": True})
        out.update(type="bar" if kind == "bar" else "line", x=list(frame.index), series=series)
    out["format"] = spec.get("format", "ratio")
    for key in ("subtitle", "format2", "xformat", "yformat", "labels", "zones", "stack", "log", "xname", "yname", "cloud", "min", "max",
                "scale", "reverse", "highlight", "cards", "legend", "digits"):
        if key in spec:
            out[key] = spec[key]
    return out


def chart(module: str, function: str, spec: dict):
    """The chart and the full table of one method; the chart is None for chart: none."""
    result, scope = run(example_code(module, function), spec.get("expr"))
    rows = table(result)
    if spec.get("chart") == "none":
        return None, rows
    # chart_expr: the chart from another call (such as more decimals), the table from the example
    if spec.get("chart_expr"):
        result = eval(spec["chart_expr"], scope)
    if spec.get("chart") == "ta":
        return ta_chart(spec, result, scope), rows
    return plot(spec, result, scope), rows


def load_specs() -> dict:
    """Every method's chart, from _data/financetoolkit_docs_charts/<module>.yml (keys are function names)."""
    specs = {}
    for path in sorted(SPECS.glob("*.yml")):
        try:
            loaded = yaml.safe_load(path.read_text()) or {}
        except yaml.YAMLError as error:  # one broken file should not stop the other modules
            print(f"SKIPPED {path.name}: {str(error).splitlines()[0]}", file=sys.stderr)
            continue
        for function, spec in loaded.items():
            specs[f"{path.stem}.{function}"] = spec
    return specs


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
    specs = load_specs()
    failed = []
    for key, spec in specs.items():
        module, function = key.split(".")
        if only and key not in only and module not in only:
            continue
        try:
            data, rows = chart(module, function, spec)
        except Exception as error:  # keep the previous file when a call fails
            failed.append(f"{key}: {type(error).__name__}: {error}")
            continue
        path = OUTPUT / module / f"{function}.json"
        if data is None:
            path.unlink(missing_ok=True)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps({"charts": {function: data}}, separators=(",", ":")))
        # the full result, which the docs page shows as its table (the docstring may show a part)
        full = TABLES / module / f"{function}.json"
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(json.dumps(rows, separators=(",", ":")))
        print(f"{key}: {data['type'] if data else 'table only'}, {rows['total']} rows", flush=True)
    for line in failed:
        print("FAILED", line, file=sys.stderr)


if __name__ == "__main__":
    if sys.argv[1:2] == ["--outputs"]:
        outputs(sys.argv[2:], load_specs())
    else:
        main(sys.argv[1:])
