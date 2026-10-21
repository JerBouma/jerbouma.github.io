"""Charts for the Portfolio guide (/projects/financetoolkit/docs/portfolio#getting-started)."""

import pandas as pd
from financetoolkit import Portfolio

from .common import API_KEY, frame_chart, line

# the frames behind the charts and tables, kept for checking the numbers in the text
LAST = {}


# shaded periods: the financial crisis, the Covid crash and the 2022 sell-off
MONTH_BANDS = [
    {"from": "2008-09", "to": "2009-03", "label": "Financial crisis"},
    {"from": "2020-02", "to": "2020-04", "label": "Covid"},
    {"from": "2022-01", "to": "2022-12", "label": "2022"},
]


def build() -> dict:
    # the example portfolio that ships with the Finance Toolkit (example=True never writes
    # the template files into the working directory)
    portfolio = Portfolio(example=True, api_key=API_KEY, benchmark_ticker="^GSPC")
    charts = {}

    overview = portfolio.get_portfolio_overview(include_portfolio=True)
    LAST["overview"] = overview
    profit = overview["Return Value"].drop("Portfolio").sort_values(ascending=False)
    LAST["profit"] = profit
    charts["portfolio-overview"] = {
        "type": "bar",
        "x": list(profit.index),
        "series": [{"name": "Return Value", "data": [round(float(v), 0) for v in profit]}],
        "format": "amount",
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
    # the value at the end of each month
    totals = totals.resample("ME").last()
    totals.index = totals.index.to_period("M")
    LAST["totals"] = totals
    spec = frame_chart(totals[["Current Value", "Invested Amount"]], fmt="amount", bands=MONTH_BANDS)
    spec["series"][0]["area"] = True
    spec["series"][1]["dashed"] = True
    spec["series"][1]["color"] = "#94a3b8"
    charts["portfolio-value"] = spec

    transactions = portfolio.get_transactions_overview(pnl_method="FIFO")
    LAST["transactions"] = transactions

    performance = portfolio.get_portfolio_performance(period="yearly")
    LAST["performance"] = performance
    yearly_value = performance["Current Value"].unstack("Identifier")
    invested = performance.groupby(level="Date")["Invested Amount"].sum()
    largest = list(yearly_value.iloc[-1].sort_values(ascending=False).index[:4])
    stacked = yearly_value[largest].copy()
    stacked["Other positions"] = yearly_value.drop(columns=largest).sum(axis=1)
    LAST.update(yearly_value=yearly_value, invested=invested, stacked=stacked)
    spec = frame_chart(stacked, fmt="amount", kind="bar", stack=True)
    spec["series"].append({"name": "Invested Amount", "data": [round(float(v), 0) for v in invested.reindex(stacked.index)], "reference": True})
    charts["portfolio-yearly"] = spec
    LAST["transactions_performance"] = portfolio.get_transactions_performance(period="quarterly")

    toolkit = portfolio.toolkit

    net_profit_margin = toolkit.ratios.get_net_profit_margin()
    LAST["net_profit_margin"] = net_profit_margin
    margin = net_profit_margin.loc["Portfolio"]
    charts["portfolio-net-profit-margin"] = line(
        margin.index, {"Portfolio": margin}, fmt="percent", kind="bar", highlight=len(margin.dropna()) - 1,
    )

    beta = toolkit.performance.get_beta(period="yearly")
    beta["Benchmark"] = 1
    value_at_risk = toolkit.risk.get_value_at_risk(period="yearly", within_period=True)
    LAST.update(beta=beta, value_at_risk=value_at_risk)
    beta_spec = line(beta.index, {"Portfolio": beta["Portfolio"], "Benchmark": beta["Benchmark"]}, fmt="ratio")
    beta_spec["series"][0]["area"] = True
    beta_spec["series"][1]["reference"] = True
    var_spec = frame_chart(value_at_risk[["Portfolio", "Benchmark"]], fmt="percent", kind="bar")
    var_spec["series"][1]["color"] = "#94a3b8"
    charts["portfolio-beta-var"] = {
        "type": "tabs",
        "tabs": [{"label": "Beta", **beta_spec}, {"label": "Value at Risk", **var_spec}],
    }

    rsi = toolkit.technicals.get_relative_strength_index()
    LAST["rsi"] = rsi
    last_year = rsi[["Portfolio", "ASML", "FIX", "MPWR"]].iloc[-252:]
    LAST["last_year"] = last_year
    tabs = []
    for i, name in enumerate(last_year.columns):
        spec = line(last_year.index, {name: last_year[name]}, fmt="number")
        spec["series"][0]["color"] = ["#38bdf8", "#818cf8", "#f97316", "#34d399"][i]
        for level, text in ((70, "Overbought (70)"), (30, "Oversold (30)")):
            spec["series"].append({"name": text, "data": [level] * len(spec["x"]), "reference": True})
        tabs.append({"label": name, **spec})
    charts["portfolio-rsi"] = {
        "type": "tabs",
        "tabs": tabs,
    }

    return charts
