"""Charts for the External Datasets guide (/projects/financetoolkit/docs/getting-started/external-datasets).

The statements and normalisation files are the ones in examples/external_datasets of the
Finance Toolkit repository, read here from the local mirror of that repository.
"""

from pathlib import Path

import pandas as pd
from financetoolkit import Toolkit
from financetoolkit.utilities import dataframe_model

from .common import API_KEY, frame_chart, label, line, values

FOLDER = Path("/sources/finance-toolkit/examples/external_datasets")
NAMES = {"TSLA": "Tesla", "GOOGL": "Alphabet", "Benchmark": "S&P 500"}

# the frames behind the charts, kept for checking the numbers in the text
LAST = {}


def statements() -> tuple:
    def read(name):
        return pd.read_csv(FOLDER / f"{name}.csv", index_col=0)

    balance = dataframe_model.combine_dataframes({"TSLA": read("TSLA_balance"), "GOOGL": read("GOOGL_balance")})
    income = dataframe_model.combine_dataframes({"TSLA": read("TSLA_income"), "GOOGL": read("GOOGL_income")})
    cash = dataframe_model.combine_dataframes({"TSLA": read("TSLA_cash"), "GOOGL": read("GOOGL_cash")})
    return balance, income, cash


def build() -> dict:
    balance, income, cash = statements()
    companies = Toolkit(
        tickers=["TSLA", "GOOGL"],
        balance=balance,
        income=income,
        cash=cash,
        format_location=str(FOLDER),
        reverse_dates=True,
    )
    charts = {}

    dupont = companies.models.get_extended_dupont_analysis()
    LAST["dupont"] = dupont
    parts = [("Interest Burden Ratio", "Interest burden", "percent"),
             ("Tax Burden Ratio", "Tax burden", "percent"),
             ("Operating Profit Margin", "Operating margin", "percent"),
             ("Asset Turnover", "Asset turnover", "multiple"),
             ("Equity Multiplier", "Equity multiplier", "multiple")]
    tabs = []
    for ticker in ["TSLA", "GOOGL"]:
        frame = dupont.loc[ticker].dropna(axis=1, how="any")
        tabs.append({
            "label": NAMES[ticker],
            "years": [label(c) for c in frame.columns],
            "components": [{"name": short, "format": fmt, "data": values(frame.loc[row])} for row, short, fmt in parts],
            "result": {"name": "Return on equity", "format": "percent", "data": values(frame.loc["Return on Equity"])},
        })
    charts["external-datasets-dupont"] = {"type": "dupont", "title": "Extended DuPont Analysis from Yahoo Finance statements", "tabs": tabs}

    efficiency = companies.ratios.collect_efficiency_ratios()
    LAST["efficiency"] = efficiency
    metrics = ["Cash Conversion Efficiency", "SGA-to-Revenue Ratio", "R&D Intensity Ratio", "Operating Ratio"]
    years = [c for c in efficiency.columns if all(pd.notna(efficiency.loc[(t, m), c]) for t in ["TSLA", "GOOGL"] for m in metrics)]
    charts["external-datasets-efficiency"] = {
        "type": "compare",
        "title": "Efficiency ratios of Tesla and Alphabet",
        "x": [label(y) for y in years],
        "format": "percent",
        "names": {"TSLA": "Tesla", "GOOGL": "Alphabet"},
        "metrics": [
            {"name": m, "series": [{"name": t, "data": values(efficiency.loc[(t, m), years])} for t in ["TSLA", "GOOGL"]]}
            for m in metrics
        ],
    }

    days = ["Days of Inventory Outstanding", "Days of Sales Outstanding", "Days of Accounts Payable Outstanding", "Cash Conversion Cycle"]
    latest = efficiency.columns[-1]
    charts["external-datasets-days"] = line(
        ["Inventory", "Receivables", "Payables", "Cash conversion cycle"],
        {NAMES[t]: [efficiency.loc[(t, d), latest] for d in days] for t in ["TSLA", "GOOGL"]},
        fmt="number",
        kind="bar",
        title=f"Working capital in days, {label(latest)}",
    )

    growth = companies.get_balance_sheet_statement(growth=True)
    LAST["growth"] = growth

    beta = companies.performance.get_beta(period="monthly")
    LAST["beta"] = beta
    charts["external-datasets-beta"] = frame_chart(beta.rename(columns=NAMES), fmt="ratio", title="Beta against the S&P 500, monthly")

    drawdown = companies.risk.get_maximum_drawdown(period="quarterly", within_period=True)
    LAST["drawdown"] = drawdown
    charts["external-datasets-drawdown"] = frame_chart(drawdown.rename(columns=NAMES), fmt="percent", kind="bar", title="Maximum drawdown within each quarter")

    historical = companies.get_historical_data()
    cumulative = historical["Cumulative Return"]
    LAST["cumulative"] = cumulative
    charts["external-datasets-returns"] = frame_chart(cumulative.rename(columns=NAMES), fmt="ratio", title="Cumulative return (1 = start)")

    if API_KEY:
        with_key = Toolkit(
            tickers=["TSLA", "GOOGL"],
            balance=balance,
            income=income,
            cash=cash,
            api_key=API_KEY,
            format_location=str(FOLDER),
            reverse_dates=True,
        )
        estimates = with_key.get_analyst_estimates()
        LAST["estimates"] = estimates
        charts["external-datasets-estimates"] = {
            "type": "tabs",
            "title": "Analyst estimates (average)",
            "tabs": [
                {"label": "Revenue", **line(estimates.columns, {NAMES[t]: estimates.loc[(t, "Estimated Revenue Average")] for t in ["TSLA", "GOOGL"]}, fmt="usd")},
                {"label": "EPS", **line(estimates.columns, {NAMES[t]: estimates.loc[(t, "Estimated EPS Average")] for t in ["TSLA", "GOOGL"]}, fmt="price")},
            ],
        }

    return charts
