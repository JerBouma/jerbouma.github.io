"""Builds the data behind the interactive charts on /projects/financetoolkit.

Runs the same Finance Toolkit calls as the examples on that page and writes
the results to assets/data/financetoolkit-charts.json, which the page draws
with ECharts. Rerun it to refresh the charts:

    pip install financetoolkit
    python _scripts/financetoolkit_charts.py

Without a Financial Modeling Prep key the Toolkit falls back to Yahoo Finance,
which covers the last five years of financial statements; set
FINANCIAL_MODELING_PREP_KEY for a longer history. With --tables it also prints
the frames behind the tables on the page.
"""

import json
import logging
import os
import sys
import warnings
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
from financetoolkit import Discovery, Portfolio, Toolkit

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


TICKERS = ["NVDA", "AMD", "INTC"]
NAMES = {"NVDA": "Nvidia", "AMD": "AMD", "INTC": "Intel", "Benchmark": "S&P 500"}

# the frames behind the charts, printed as the page's tables with --tables
TABLES = {}


def discovery_chart(api_key: str) -> dict:
    """The stock screener: US semiconductor companies above $100 billion."""
    discovery = Discovery(api_key=api_key)
    screen = discovery.get_stock_screener(
        industry="Semiconductors", country="US", exchange="NASDAQ", market_cap_higher=100_000_000_000, is_etf=False
    )
    TABLES["discovery"] = screen
    caps = screen["Market Cap"].sort_values(ascending=False)
    return line(caps.index, {"Market cap": caps}, fmt="usd", kind="bar", title="Market Capitalization")


def main() -> None:
    charts = {}
    if API_KEY:
        charts["discovery"] = discovery_chart(API_KEY)
    else:
        print("No FMP key, keeping the previous Discovery chart")
        charts["discovery"] = json.loads(OUTPUT.read_text())["charts"]["discovery"]

    companies = Toolkit(TICKERS, api_key=API_KEY, start_date=START)

    historical = companies.get_historical_data(period="weekly")
    TABLES["historical"] = historical.xs("NVDA", axis=1, level=1)
    cumulative = historical["Cumulative Return"]
    charts["historical"] = line(
        cumulative.index, {NAMES[t]: cumulative[t] for t in [*TICKERS, "Benchmark"]},
        fmt="multiple", title="Cumulative Returns",
    )

    income = companies.get_income_statement()
    TABLES["statements"] = income.loc["NVDA"]
    revenue = income.xs("Revenue", level=1)
    charts["statements"] = line(
        revenue.columns, {NAMES[t]: revenue.loc[t] / 1e9 for t in TICKERS},
        fmt="billions", kind="bar", title="Revenue (USD billions)",
    )

    profitability = companies.ratios.collect_profitability_ratios()
    TABLES["ratios"] = profitability.loc["NVDA"]
    kpis = profitability.loc["NVDA"].loc[
        ["Gross Margin", "Operating Margin", "Net Profit Margin", "Return on Equity", "Return on Assets",
         "Return on Invested Capital"]
    ].dropna(axis=1, how="any")
    charts["ratios"] = {
        "type": "kpis",
        "title": "Profitability Ratios for Nvidia",
        "period": False,
        "x": list(kpis.index),
        "series": [{"name": label(year), "data": values(kpis[year])} for year in kpis.columns],
        "format": "percent",
    }

    # Extended DuPont: five components that multiply into Return on Equity
    dupont = companies.models.get_extended_dupont_analysis()
    TABLES["models"] = dupont.loc["NVDA"]
    parts = [("Interest Burden Ratio", "Interest burden", "percent"),
             ("Tax Burden Ratio", "Tax burden", "percent"),
             ("Operating Profit Margin", "Operating margin", "percent"),
             ("Asset Turnover", "Asset turnover", "multiple"),
             ("Equity Multiplier", "Equity multiplier", "multiple")]
    tabs = []
    for ticker in TICKERS:
        frame = dupont.loc[ticker].dropna(axis=1, how="any")
        tabs.append({
            "label": NAMES[ticker],
            "years": [label(c) for c in frame.columns],
            "components": [{"name": short, "format": fmt, "data": values(frame.loc[row])} for row, short, fmt in parts],
            "result": {"name": "Return on equity", "format": "percent", "data": values(frame.loc["Return on Equity"])},
        })
    charts["models"] = {"type": "dupont", "title": "Extended DuPont Analysis", "tabs": tabs}

    sharpe = companies.performance.get_sharpe_ratio(period="yearly", annualize=True)
    drawdown = companies.risk.get_maximum_drawdown(period="yearly", within_period=True)
    TABLES["risk"] = drawdown
    TABLES["performance"] = sharpe
    order = [*TICKERS, "Benchmark"]
    charts["risk"] = {
        "type": "tabs",
        "title": "Sharpe Ratio and Maximum Drawdown",
        "tabs": [
            {"label": "Sharpe ratio", **line(sharpe.index, {NAMES[t]: sharpe[t] for t in order if t in sharpe}, fmt="ratio", kind="bar")},
            {"label": "Maximum drawdown", **line(drawdown.index, {NAMES[t]: drawdown[t] for t in order}, fmt="percent", kind="bar")},
        ],
    }

    # the latest weight and return of every position in the example portfolio
    portfolio = Portfolio(example=True, api_key=API_KEY)
    overview = portfolio.get_positions_overview()
    TABLES["portfolio"] = overview
    last = overview.iloc[-1]
    weights = last["Current Weight"].sort_values(ascending=False)
    returns = (last["Cumulative Return"] - 1).reindex(weights.index)
    charts["portfolio"] = {
        "type": "tabs",
        "title": "Example Portfolio",
        "tabs": [
            {"label": "Weights", **line(weights.index, {"Current weight": weights}, fmt="percent", kind="bar")},
            {"label": "Returns", **line(returns.index, {"Cumulative return": returns}, fmt="percent", kind="bar")},
        ],
    }

    payload = {"generated": date.today().isoformat(), "charts": charts}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, separators=(",", ":")))
    print(f"Wrote {len(charts)} charts to {OUTPUT} ({OUTPUT.stat().st_size // 1024} KB)")

    if "--tables" in sys.argv:
        for name, frame in TABLES.items():
            print(f"\n## {name}\n")
            print(frame.round(4).to_markdown() if hasattr(frame, "to_markdown") else frame)


if __name__ == "__main__":
    main()
