"""Builds the data behind the interactive charts on /projects/financetoolkit.

Runs the same Finance Toolkit calls as the examples on that page and writes
the results to assets/data/financetoolkit-charts.json, which the page draws
with ECharts. Rerun it to refresh the charts:

    pip install "financetoolkit[econometrics]"
    python _scripts/financetoolkit_charts.py

It needs a Financial Modeling Prep key in FINANCIAL_MODELING_PREP_KEY: the
screener, the option chains and the fund holdings come from there. With
--tables it also prints the frames behind the tables on the page.
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
from financetoolkit import Discovery, Econometrics, Portfolio, Toolkit

warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)

START = "2017-12-31"
END = "2025-12-31"
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
# eight year ends: the palette's seven colours and one more
YEAR_COLOURS = ["#38bdf8", "#818cf8", "#f97316", "#34d399", "#f472b6", "#fbbf24", "#a78bfa", "#e2e8f0"]

# the frames behind the charts, printed as the page's tables with --tables
TABLES = {}


def discovery_chart() -> dict:
    """The stock screener: US semiconductor companies above $100 billion."""
    discovery = Discovery(api_key=API_KEY)
    semiconductors = discovery.get_stock_screener(
        industry="Semiconductors", country="US", exchange="NASDAQ", market_cap_higher=100_000_000_000, is_etf=False
    )
    TABLES["discovery"] = semiconductors[["Name", "Market Cap", "Beta", "Price", "Dividend"]].head()
    caps = semiconductors["Market Cap"].sort_values(ascending=False)
    return line(caps.index, {"Market cap": caps}, fmt="usd", kind="bar", title="Market Capitalization")


def main() -> None:
    if not API_KEY:
        sys.exit("Set FINANCIAL_MODELING_PREP_KEY first")
    charts = {"discovery": discovery_chart()}

    companies = Toolkit(TICKERS, api_key=API_KEY, start_date=START, end_date=END)

    # Following the Market: cumulative returns and the 14-week RSI, each in its own tab
    historical = companies.get_historical_data(period="weekly")
    rsi = companies.technicals.get_relative_strength_index(period="weekly", window=14)
    TABLES["historical"] = rsi.groupby(rsi.index.start_time.year).max()
    cumulative = historical["Cumulative Return"]
    order = [*TICKERS, "Benchmark"]
    rsi_tab = line(rsi.index, {NAMES[t]: rsi[t] for t in order}, fmt="num")
    rsi_tab["series"].append({"name": "Overbought (70)", "data": [70] * len(rsi_tab["x"]), "reference": True})
    charts["historical"] = {
        "type": "tabs",
        "title": "Cumulative Returns and Relative Strength Index",
        "tabs": [
            {"label": "Cumulative return", **line(cumulative.index, {NAMES[t]: cumulative[t] for t in order}, fmt="multiple")},
            {"label": "RSI (14 weeks)", **rsi_tab},
        ],
    }

    # Zooming in on Competitors: Nvidia's profitability and its Extended DuPont Analysis
    profitability = companies.ratios.collect_profitability_ratios()
    TABLES["ratios"] = profitability.loc["NVDA"].head()
    kpis = profitability.loc["NVDA"].loc[
        ["Gross Margin", "Operating Margin", "Net Profit Margin", "EBITDA Margin", "Free Cash Flow Margin",
         "Return on Equity"]
    ].dropna(axis=1, how="any")
    charts["ratios"] = {
        "type": "kpis",
        "title": "Profitability Ratios for Nvidia",
        "period": False,
        "x": list(kpis.index),
        "series": [{"name": label(year), "data": values(kpis[year])} for year in kpis.columns],
        "format": "percent",
    }

    dupont = companies.models.get_extended_dupont_analysis()
    TABLES["models"] = dupont.loc["NVDA"]
    parts = [("Interest Burden Ratio", "Interest burden", "percent"),
             ("Tax Burden Ratio", "Tax burden", "percent"),
             ("Operating Profit Margin", "Operating margin", "percent"),
             ("Asset Turnover", "Asset turnover", "multiple"),
             ("Equity Multiplier", "Equity multiplier", "multiple")]
    frame = dupont.loc["NVDA"].dropna(axis=1, how="any")
    charts["models"] = {
        "type": "dupont",
        "title": "Extended DuPont Analysis for Nvidia",
        "tabs": [{
            "label": NAMES["NVDA"],
            "years": [label(c) for c in frame.columns],
            "components": [{"name": short, "format": fmt, "data": values(frame.loc[row])} for row, short, fmt in parts],
            "result": {"name": "Return on equity", "format": "percent", "data": values(frame.loc["Return on Equity"])},
        }],
    }

    # Weighing Risk and Return
    sharpe = companies.performance.get_sharpe_ratio(period="yearly", annualize=True)
    drawdown = companies.risk.get_maximum_drawdown(period="yearly", within_period=True)
    TABLES["risk"] = sharpe
    charts["risk"] = {
        "type": "tabs",
        "title": "Sharpe Ratio and Maximum Drawdown",
        "tabs": [
            {"label": "Sharpe ratio", **line(sharpe.index, {NAMES[t]: sharpe[t] for t in order if t in sharpe}, fmt="ratio", kind="bar")},
            {"label": "Maximum drawdown", **line(drawdown.index, {NAMES[t]: drawdown[t] for t in order}, fmt="percent", kind="bar")},
        ],
    }

    # What the Option Market Expects: live chains, so the Toolkit runs up to today
    companies_today = Toolkit(TICKERS, api_key=API_KEY)
    premium = companies_today.options.get_volatility_risk_premium(days=30)
    TABLES["options"] = premium
    charts["options"] = line(
        [NAMES[t] for t in premium.index],
        {"Implied volatility": premium["Implied Volatility"], "Realized volatility": premium["Realized Volatility"]},
        fmt="percent", kind="bar", title="Implied and Realized Volatility (30 Days)",
    )

    # The Economic Environment: the Treasury par yield curve at each year end
    treasury_rates = companies.fixedincome.get_treasury_rates()
    curves = treasury_rates.groupby(treasury_rates.index.year).last()
    TABLES["economics"] = curves
    charts["economics"] = {
        **line(curves.columns, {str(year): curves.loc[year] for year in curves.index}, fmt="percent"),
        "title": "U.S. Treasury Yield Curve at Each Year End",
    }
    for series, colour in zip(charts["economics"]["series"], YEAR_COLOURS):
        series["color"] = colour

    # Economic Relations: monthly returns on the change in the real yield and inflation expectations
    real_yield = companies.economics.get_real_yield_curve("United States", period="monthly")
    inflation_expectations = companies.economics.get_breakeven_inflation_expectations("United States", period="monthly")
    monthly_returns = companies.get_historical_data(period="monthly")["Return"][TICKERS]
    monthly_returns["Real Yield"] = real_yield[("United States", "10Y")].diff()
    monthly_returns["Inflation Expectations"] = inflation_expectations[("United States", "10Y")].diff()
    econometrics = Econometrics(data=monthly_returns, changes=None)
    regressions = pd.concat({
        ticker: econometrics.get_ols(dependent_ticker=ticker, independent_tickers=["Real Yield", "Inflation Expectations"])
        for ticker in TICKERS
    })
    TABLES["econometrics"] = regressions.loc["NVDA"]
    rows = regressions.drop(index="Intercept", level=1)
    # the 95% interval from the coefficient and its standard error
    charts["econometrics"] = {
        "type": "coef",
        "title": "Coefficients with 95% Confidence Intervals",
        "x": [f"{NAMES[t]} · {name}" for t, name in rows.index],
        "coef": values(rows["Coefficient"]),
        "low": values(rows["Coefficient"] - 1.96 * rows["Std. Error"]),
        "high": values(rows["Coefficient"] + 1.96 * rows["Std. Error"]),
        "p": values(rows["P-Value"]),
    }

    # Comparing the Sector's ETFs: holdings are those of today
    funds = Toolkit(["SOXX", "XSD", "PSI", "SMH", "SMHC", "KCHP"], api_key=API_KEY, start_date=START, end_date=END)
    country_weightings = funds.etf.get_country_weightings()
    overlap = funds.etf.get_overlap()
    TABLES["etf"] = overlap.round(2)
    TABLES["etf-countries"] = country_weightings
    TABLES["etf-concentration"] = funds.etf.get_concentration()
    charts["etf-countries"] = country_chart(country_weightings)
    charts["etf-overlap"] = {
        "type": "heatmap",
        "title": "Overlap Between the Funds",
        "x": list(overlap.columns),
        "y": list(overlap.index),
        "values": [values(overlap.loc[fund].clip(upper=1), 2) for fund in overlap.index],
        "min": 0,
        "max": 1,
        "scale": "sequential",
        "digits": 2,
    }

    # Building a Diversified Portfolio
    assets = Toolkit(["SMH", "XLV", "XLE", "TLT", "GLD"], api_key=API_KEY, start_date="2021-01-01", end_date=END)
    efficient_frontier = assets.portfolio.get_efficient_frontier(points=25, maximum_weight=0.4)
    maximum_sharpe = assets.portfolio.get_maximum_sharpe_weights(maximum_weight=0.4)
    risk_parity = assets.portfolio.get_risk_parity_weights()
    TABLES["optimization"] = risk_parity
    TABLES["frontier"] = efficient_frontier
    TABLES["maximum-sharpe"] = maximum_sharpe
    charts["optimization-frontier"] = frontier_chart(efficient_frontier, maximum_sharpe, risk_parity)
    weights = pd.DataFrame({
        "Maximum Sharpe ratio": maximum_sharpe["Weight"].drop("Portfolio"),
        "Risk parity": risk_parity["Weight"].drop("Portfolio"),
    })
    charts["optimization-weights"] = line(
        weights.index, {c: weights[c] for c in weights.columns}, fmt="percent", kind="bar", title="Portfolio Weights",
    )

    # Following the Portfolio: the risk parity weights, rebalanced every year, up to today
    portfolio = Portfolio(weights=risk_parity, start_date="2021-01-01", rebalancing="yearly", api_key=API_KEY)
    overview = portfolio.get_portfolio_overview()
    TABLES["portfolio"] = overview[["Weight", "Return", "Benchmark Return", "Volatility", "Alpha", "Beta"]]
    charts["portfolio"] = line(
        overview.index, {"Return": overview["Return"], "Benchmark return": overview["Benchmark Return"]},
        fmt="percent", kind="bar", title="Return of Each Position and the Benchmark",
    )

    payload = {"generated": date.today().isoformat(), "charts": charts}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, separators=(",", ":")))
    print(f"Wrote {len(charts)} charts to {OUTPUT} ({OUTPUT.stat().st_size // 1024} KB)")

    if "--tables" in sys.argv:
        for name, frame in TABLES.items():
            print(f"\n## {name}\n")
            print(frame.round(4).to_markdown() if hasattr(frame, "to_markdown") else frame)


def country_chart(country_weightings: pd.DataFrame) -> dict:
    """The country weights of each fund, stacked to 100%: the largest countries, the rest together."""
    weights = country_weightings
    # one column per fund, one row per country, whichever way the frame comes
    if not set(weights.columns) & {"SOXX", "SMH"}:
        weights = weights.T
    # funds name some countries differently
    weights = weights.fillna(0).rename(index={"Korea (the Republic of)": "South Korea"}).groupby(level=0).sum()
    # the funds' own "Other" goes into the rest
    largest = weights.drop(index="Other", errors="ignore").max(axis=1).sort_values(ascending=False)
    top = list(largest.index[:5])
    shown = weights.loc[top]
    other = (1 - shown.sum()).clip(lower=0)
    series = {country: shown.loc[country] for country in top}
    if other.max() > 0.005:
        series["Other"] = other
    return line(weights.columns, series, fmt="percent", kind="bar", stack=True, title="Country Weights")


def frontier_chart(frontier: pd.DataFrame, maximum_sharpe: pd.DataFrame, risk_parity: pd.DataFrame) -> dict:
    """The efficient frontier as a curve, with both portfolios and each asset on its own as points."""
    points = [
        {"name": asset, "x": round(float(row["Volatility"]), 4), "y": round(float(row["Expected Return"]), 4)}
        for asset, row in risk_parity.drop("Portfolio").iterrows()
    ]
    points.append({"name": "Maximum Sharpe ratio", "x": round(float(maximum_sharpe.loc["Portfolio", "Volatility"]), 4),
                   "y": round(float(maximum_sharpe.loc["Portfolio", "Expected Return"]), 4)})
    points.append({"name": "Risk parity", "x": round(float(risk_parity.loc["Portfolio", "Volatility"]), 4),
                   "y": round(float(risk_parity.loc["Portfolio", "Expected Return"]), 4)})
    return {
        "type": "scatter",
        "title": "Efficient Frontier",
        "xname": "Volatility",
        "yname": "Expected return",
        "xformat": "percent",
        "yformat": "percent",
        "points": points,
        "highlight": [len(points) - 2, len(points) - 1],
        "curve": [[round(float(v), 4), round(float(r), 4)] for v, r in zip(frontier["Volatility"], frontier["Expected Return"])],
    }


if __name__ == "__main__":
    main()
