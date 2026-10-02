"""Builds the data behind the interactive charts on /projects/financetoolkit.

Runs the same Finance Toolkit calls as the examples on that page and writes
the results to assets/data/financetoolkit-charts.json, which the page draws
with ECharts. Rerun it to refresh the charts:

    pip install financetoolkit
    python _scripts/financetoolkit_charts.py

Without a Financial Modeling Prep key the Toolkit falls back to Yahoo Finance,
which covers the last five years of financial statements; set
FINANCIAL_MODELING_PREP_KEY for a longer history. The ICE BofA yields are read
straight from FRED's public CSV download, which needs no key.
"""

import io
import json
import logging
import os
import time
import urllib.request
import warnings
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
from financetoolkit import Economics, Portfolio, Toolkit

warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)

START = "2017-12-31"
OUTPUT = Path(__file__).resolve().parent.parent / "assets" / "data" / "financetoolkit-charts.json"
API_KEY = os.environ.get("FINANCIAL_MODELING_PREP_KEY", "")


def label(value) -> str:
    """Dates, periods and numbers as short axis labels."""
    if isinstance(value, pd.Period):
        # weekly periods print as a date range; the week's last day reads better
        if value.freqstr.startswith("W"):
            return value.end_time.strftime("%Y-%m-%d")
        return str(value)
    if isinstance(value, (pd.Timestamp, date)):
        return pd.Timestamp(value).strftime("%Y-%m-%d")
    return str(value)


def values(series: pd.Series, digits: int = 4) -> list:
    """A series as a JSON list, with gaps as null."""
    return [None if pd.isna(v) or np.isinf(v) else round(float(v), digits) for v in series]


def line(x, series: dict, fmt: str = "num", kind: str = "line", **extra) -> dict:
    """A chart; periods where every series is empty are left out."""
    x = [label(v) for v in x]
    data = {name: values(s) for name, s in series.items()}
    keep = [i for i in range(len(x)) if any(d[i] is not None for d in data.values())]
    return {
        "type": kind,
        "x": [x[i] for i in keep],
        "series": [{"name": name, "data": [d[i] for i in keep]} for name, d in data.items()],
        "format": fmt,
        **extra,
    }


def main() -> None:
    companies = Toolkit(["AAPL", "MSFT"], api_key=API_KEY, start_date=START, benchmark_ticker="SPY")
    charts = {}

    # Statements first: the models module relies on them being loaded
    # EBITDA: Apple against Alphabet, whose fiscal years line up with Apple's
    # closely enough that both have the same latest reported year (Microsoft's
    # year ends in June, so it reports a year Apple has not finished yet)
    peers = Toolkit(["AAPL", "GOOGL"], api_key=API_KEY, start_date=START)
    ebitda = peers.get_income_statement().xs("EBITDA", level=1)
    charts["statements"] = line(
        ebitda.columns,
        {"Apple": ebitda.loc["AAPL"] / 1e9, "Alphabet": ebitda.loc["GOOGL"] / 1e9},
        fmt="billions",
        kind="bar",
        title="EBITDA (USD billions)",
    )
    companies.get_income_statement()  # the models module relies on the statements

    historical = companies.get_historical_data(period="weekly")
    cumulative = historical["Cumulative Return"]
    charts["historical"] = line(
        cumulative.index,
        {"Apple": cumulative["AAPL"], "Microsoft": cumulative["MSFT"], "S&P 500": cumulative["Benchmark"]},
        fmt="multiple",
        title="Cumulative return (1 = start)",
    )

    ratios = companies.ratios.collect_profitability_ratios().loc["MSFT"]
    picked = ["Gross Margin", "Operating Margin", "Net Profit Margin", "Return on Equity", "Return on Assets"]
    charts["ratios"] = line(
        ratios.columns,
        {name: ratios.loc[name] for name in picked if name in ratios.index},
        fmt="percent",
        title="Profitability ratios for Microsoft",
    )

    dupont = companies.models.get_extended_dupont_analysis()
    charts["models"] = {
        "type": "tabs",
        "title": "Extended DuPont Analysis",
        "tabs": [
            {"label": ticker, **line(dupont.loc[ticker].columns, {row: dupont.loc[ticker].loc[row] for row in dupont.loc[ticker].index}, fmt="ratio")}
            for ticker in ["AAPL", "MSFT"]
        ],
    }

    # Greeks for Apple: one line per expiration, against the strike price
    greek_tabs = []
    for name, getter in [("Delta", companies.options.get_delta), ("Gamma", companies.options.get_gamma),
                         ("Theta", companies.options.get_theta), ("Vega", companies.options.get_vega)]:
        frame = getter(expiration_time_range=180).loc["AAPL"]
        columns = list(frame.columns)
        pick = sorted({columns[min(len(columns) - 1, i)] for i in (29, 89, 179)})
        greek_tabs.append({"label": name, **line(frame.index, {f"Expires {label(c)}": frame[c] for c in pick}, fmt="num", xname="Strike price")})
    charts["greeks"] = {"type": "tabs", "title": "Option Greeks for Apple", "tabs": greek_tabs}

    factors = companies.performance.get_factor_asset_correlations(period="quarterly")
    charts["performance"] = {
        "type": "tabs",
        "title": "Correlation with the Fama-French factors",
        "tabs": [
            {"label": ticker, **line(factors.index, {f: factors[ticker][f] for f in factors[ticker].columns}, fmt="num")}
            for ticker in ["AAPL", "MSFT"]
        ],
    }

    var = companies.risk.get_value_at_risk(period="weekly", within_period=True)
    charts["risk"] = line(
        var.index,
        {"Apple": var["AAPL"], "Microsoft": var["MSFT"], "S&P 500": var["Benchmark"]},
        fmt="percent",
        title="Weekly Value at Risk (95%)",
    )

    ichimoku = companies.technicals.get_ichimoku_cloud()
    daily = companies.get_historical_data()["Close"]
    since = ichimoku.index[-260]
    tech_tabs = []
    for ticker, name in [("AAPL", "Apple"), ("MSFT", "Microsoft")]:
        cloud = ichimoku.xs(ticker, axis=1, level=1).loc[since:]
        close = daily[ticker].reindex(cloud.index)
        tech_tabs.append({"label": name, **line(cloud.index, {"Close": close, **{c: cloud[c] for c in cloud.columns}}, fmt="price", cloud=["Leading Span A", "Leading Span B"])})
    charts["technicals"] = {"type": "tabs", "title": "Ichimoku Cloud, last 12 months", "tabs": tech_tabs}

    # ICE BofA effective yields per credit rating, straight from FRED
    ratings = {"AAA": "BAMLC0A1CAAAEY", "AA": "BAMLC0A2CAAEY", "A": "BAMLC0A3CAEY", "BBB": "BAMLC0A4CBBBEY",
               "BB": "BAMLH0A1HYBBEY", "B": "BAMLH0A2HYBEY", "CCC": "BAMLH0A3HYCEY"}
    yields = {}
    for rating, series_id in ratings.items():
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}&cosd={START}"
        with urllib.request.urlopen(url, timeout=60) as response:
            frame = pd.read_csv(io.StringIO(response.read().decode()), index_col=0, parse_dates=True)
        yields[rating] = pd.to_numeric(frame.iloc[:, 0], errors="coerce") / 100
    yields = pd.DataFrame(yields).resample("W").last()
    charts["fixedincome"] = line(yields.index, {r: yields[r] for r in yields.columns}, fmt="percent",
                                 title="ICE BofA effective yield by credit rating")

    # the macro dataset is downloaded from GitHub, which now and then answers 503
    for attempt in range(5):
        try:
            unemployment = Economics(start_date="2010-01-01").get_unemployment_rate()
            break
        except Exception:
            if attempt == 4:
                raise
            time.sleep(20)
    countries = ["Colombia", "United States", "Sweden", "Japan", "Germany"]
    charts["economics"] = line(unemployment.index, {c: unemployment[c] for c in countries if c in unemployment}, fmt="percent",
                               title="Unemployment rate")

    # the latest weight and return of every position in the example portfolio
    portfolio = Portfolio(example=True, api_key=API_KEY)
    overview = portfolio.get_positions_overview()
    last = overview.iloc[-1]
    weights = last["Current Weight"].sort_values(ascending=False)
    returns = (last["Cumulative Return"] - 1).reindex(weights.index)
    charts["portfolio"] = {
        "type": "tabs",
        "title": f"Example portfolio on {label(overview.index[-1])}",
        "tabs": [
            {"label": "Weights", **line(weights.index, {"Current weight": weights}, fmt="percent", kind="bar")},
            {"label": "Returns", **line(returns.index, {"Cumulative return": returns}, fmt="percent", kind="bar")},
        ],
    }

    payload = {"generated": date.today().isoformat(), "charts": charts}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, separators=(",", ":")))
    print(f"Wrote {len(charts)} charts to {OUTPUT} ({OUTPUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
