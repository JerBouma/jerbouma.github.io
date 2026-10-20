"""Charts for the Portfolio guide (/projects/financetoolkit/docs/portfolio#getting-started)."""

import pandas as pd
from financetoolkit import Portfolio

from .common import API_KEY, frame_chart, line

# the frames behind the charts and tables, kept for checking the numbers in the text
LAST = {}


def _bars(series, fmt):
    """A bar chart of one value per position, largest first."""
    series = series.dropna().sort_values(ascending=False)
    return line(series.index, {series.name or "Value": series}, fmt=fmt, kind="bar")


def build() -> dict:
    # the example portfolio that ships with the Finance Toolkit (example=True never writes
    # the template files into the working directory)
    portfolio = Portfolio(example=True, api_key=API_KEY, benchmark_ticker="^GSPC")
    charts = {}

    overview = portfolio.get_portfolio_overview(include_portfolio=True)
    LAST["overview"] = overview
    charts["portfolio-overview"] = {
        "type": "tabs",
        "title": "Each position in the example portfolio",
        "tabs": [
            {"label": "Return", **_bars(overview["Return"].rename("Return"), "percent")},
            {"label": "Alpha", **_bars(overview["Alpha"].rename("Alpha"), "percent")},
            {"label": "Weight", **_bars(overview["Weight"].drop("Portfolio").rename("Weight"), "percent")},
        ],
    }

    positions = portfolio.get_positions_overview()
    LAST["positions"] = positions
    totals = pd.DataFrame(
        {
            "Invested Amount": positions["Invested Amount"].sum(axis=1),
            "Current Value": positions["Current Value"].sum(axis=1),
        }
    )
    totals.index = totals.index.to_timestamp()
    totals = totals.resample("W").last()
    LAST["totals"] = totals
    charts["portfolio-value"] = frame_chart(
        totals, fmt="amount", title="Invested amount and value of the portfolio"
    )

    transactions = portfolio.get_transactions_overview(pnl_method="FIFO")
    LAST["transactions"] = transactions

    performance = portfolio.get_portfolio_performance(period="yearly")
    LAST["performance"] = performance
    yearly = performance.groupby(level="Date")[["Invested Amount", "Current Value"]].sum()
    LAST["yearly"] = yearly
    charts["portfolio-yearly"] = frame_chart(yearly, fmt="amount", kind="bar", title="Invested amount and value at the end of each year")
    LAST["transactions_performance"] = portfolio.get_transactions_performance(period="quarterly")

    toolkit = portfolio.toolkit

    net_profit_margin = toolkit.ratios.get_net_profit_margin()
    LAST["net_profit_margin"] = net_profit_margin
    charts["portfolio-net-profit-margin"] = line(
        net_profit_margin.columns, {"Portfolio": net_profit_margin.loc["Portfolio"]}, fmt="percent", kind="bar",
        title="Net profit margin of the portfolio",
    )

    beta = toolkit.performance.get_beta(period="yearly")
    beta["Benchmark"] = 1
    value_at_risk = toolkit.risk.get_value_at_risk(period="yearly", within_period=True)
    LAST.update(beta=beta, value_at_risk=value_at_risk)
    charts["portfolio-beta-var"] = {
        "type": "tabs",
        "title": "The portfolio against the benchmark",
        "tabs": [
            {"label": "Beta", **frame_chart(beta[["Benchmark", "Portfolio"]], fmt="ratio")},
            {"label": "Value at Risk", **frame_chart(value_at_risk[["Benchmark", "Portfolio"]], fmt="percent", kind="bar")},
        ],
    }

    rsi = toolkit.technicals.get_relative_strength_index()
    LAST["rsi"] = rsi
    last_year = rsi[["Portfolio", "ASML", "FIX", "MPWR"]].iloc[-252:]
    spec = frame_chart(last_year, fmt="number", title="Relative Strength Index, last 12 months")
    for level in (70, 30):
        spec["series"].append({"name": str(level), "data": [level] * len(spec["x"]), "reference": True})
    charts["portfolio-rsi"] = spec

    return charts
