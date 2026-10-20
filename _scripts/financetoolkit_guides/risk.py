"""Charts for the Risk guide (/projects/financetoolkit/docs/risk#getting-started)."""

import numpy as np
import pandas as pd
from financetoolkit import Toolkit

from .common import API_KEY, frame_chart, heatmap, label, line

TICKERS = ["MSFT", "AAPL", "AMZN", "META"]
NAMES = {"Benchmark": "S&P 500"}

# shaded periods: the Covid crash and the 2022 inflation shock
MONTH_BANDS = [
    {"from": "2020-02", "to": "2020-06", "label": "Covid"},
    {"from": "2022-01", "to": "2022-12", "label": "2022 sell-off"},
]
QUARTER_BANDS = [
    {"from": "2020Q1", "to": "2020Q2", "label": "Covid"},
    {"from": "2022Q1", "to": "2022Q4", "label": "2022 sell-off"},
]

# the frames behind the charts, kept for checking the numbers in the text
LAST = {}


def _named(frame):
    return frame.rename(columns=NAMES)


def _weekly(frame):
    """A daily series as weekly closing values, for the long-run charts."""
    frame = frame.copy()
    frame.index = frame.index.to_timestamp() if hasattr(frame.index, "to_timestamp") else frame.index
    return frame.resample("W").last()


def _histogram(returns, width=0.01):
    """Weekly returns counted in bins of one percentage point."""
    returns = returns.dropna()
    edges = np.arange(np.floor(returns.min() / width) * width, returns.max() + width, width)
    counts, edges = np.histogram(returns, bins=edges)
    return [round(float(e + width / 2), 4) for e in edges[:-1]], [int(c) for c in counts]


def build() -> dict:
    companies = Toolkit(TICKERS, api_key=API_KEY, start_date="2013-01-01")
    charts = {}

    # one value per ticker over the whole sample, from monthly returns
    var_sample = companies.risk.get_value_at_risk(period="monthly")
    cvar_sample = companies.risk.get_conditional_value_at_risk(period="monthly")
    LAST.update(var_sample=var_sample, cvar_sample=cvar_sample)
    charts["risk-var-sample"] = line(
        [NAMES.get(t, t) for t in var_sample.index],
        {"VaR (95%)": var_sample.values, "CVaR (95%)": cvar_sample.values},
        fmt="percent", kind="bar",
        title="Meta's worst months cost 17.9% on average, more than twice the S&P 500's 8.3%",
    )

    # one value per quarter, from the daily returns within that quarter
    var = companies.risk.get_value_at_risk(period="quarterly", within_period=True)
    cvar = companies.risk.get_conditional_value_at_risk(period="quarterly", within_period=True)
    rolling_var = companies.risk.get_value_at_risk(period="monthly", rolling=12)
    LAST.update(var=var, cvar=cvar, rolling_var=rolling_var)
    tabs = []
    for ticker in TICKERS:
        spec = line(
            var.index,
            {f"{ticker} VaR": var[ticker], f"{ticker} CVaR": cvar[ticker], "S&P 500 VaR": var["Benchmark"]},
            fmt="percent", bands=QUARTER_BANDS,
        )
        spec["series"][0]["area"] = "down"
        spec["series"][2]["dashed"] = True
        tabs.append({"label": ticker, **spec})
    tabs.append({"label": "Rolling 12-month VaR", **frame_chart(_named(rolling_var[["META", "AMZN", "Benchmark"]]), fmt="percent", bands=MONTH_BANDS)})
    charts["risk-var"] = {
        "type": "tabs",
        "title": "Daily tail risk peaked in the Covid crash of early 2020 and again in the 2022 sell-off",
        "tabs": tabs,
    }

    ulcer = companies.risk.get_ulcer_index(period="yearly", growth=True)
    LAST["ulcer"] = ulcer
    charts["risk-ulcer"] = heatmap(
        frame_chart(_named(ulcer)), fmt="percent", low=-1, high=1,
        title="Stress comes in waves: the Ulcer Index jumped in 2018, 2020 and 2022 and fell back the year after",
    )
    charts["risk-ulcer"]["reverse"] = True  # more stress in pink

    cdar = companies.risk.get_conditional_drawdown_at_risk(period="quarterly", within_period=True)
    tail = companies.risk.get_tail_ratio(period="yearly", within_period=True)
    LAST.update(cdar=cdar, tail=tail)
    spec = frame_chart(_named(cdar[["META", "MSFT", "Benchmark"]]), fmt="percent", bands=QUARTER_BANDS)
    spec["series"][0]["area"] = "down"
    spec["series"][2]["color"] = "#94a3b8"
    charts["risk-cdar"] = {**spec, "title": "Meta's CDaR hit -44.5% in early 2022; the S&P 500's worst was -31% in the Covid crash"}
    # centred on 1, balanced tails: pink where the left tail is the heavier one
    charts["risk-tail"] = heatmap(frame_chart(_named(tail)), fmt="ratio", low=0.5, high=1.5,
                                  title="Every Tail Ratio fell below 1 in 2022 and rose above it in 2023")

    duration = companies.risk.get_maximum_drawdown_duration(period="yearly", within_period=True)
    recovery = companies.risk.get_maximum_drawdown_recovery_time(period="yearly", within_period=True)
    LAST.update(duration=duration, recovery=recovery)
    charts["risk-drawdown-duration"] = {
        "type": "tabs",
        "title": "In 2022 the worst decline lasted 195 to 248 trading days, with no recovery before year-end",
        "tabs": [
            {"label": "Duration", **frame_chart(_named(duration), fmt="amount", kind="bar")},
            {"label": "Recovery time", **frame_chart(_named(recovery), fmt="amount", kind="bar")},
        ],
    }

    ewma = companies.risk.get_ewma_volatility()
    hurst = companies.risk.get_hurst_exponent()
    LAST.update(ewma=ewma, hurst=hurst)
    weekly_ewma = _weekly(ewma)
    tabs = []
    for ticker in TICKERS:
        spec = line(weekly_ewma.index, {ticker: weekly_ewma[ticker], "S&P 500": weekly_ewma["Benchmark"]}, fmt="percent")
        spec["series"][0]["area"] = True
        spec["series"][1]["color"] = "#94a3b8"
        tabs.append({"label": ticker, **spec})
    charts["risk-ewma"] = {
        "type": "tabs",
        "title": "EWMA volatility jumps with each shock and decays within months",
        "tabs": tabs,
    }

    returns = companies.get_historical_data(period="weekly")["Return"]
    drawdown = companies.risk.get_maximum_drawdown(period="quarterly", within_period=True)
    LAST.update(returns=returns, drawdown=drawdown)
    meta = returns["META"].dropna()
    bins, counts = _histogram(meta)
    worst = meta.idxmin()
    LAST.update(meta_var=float(meta.quantile(0.05)), meta_worst=(label(worst), float(meta.min())),
                benchmark_var=float(returns["Benchmark"].dropna().quantile(0.05)))
    charts["risk-returns"] = {
        "type": "hist",
        "title": "Three in four of Meta's weeks stay within ±5%, but the left tail reaches -23.7%",
        "bins": bins,
        "counts": counts,
        "width": 0.01,
        "format": "percent",
        "xname": "Weekly return of Meta",
        "markers": [
            {"label": "Worst week", "value": round(float(meta.min()), 4)},
            {"label": "5% quantile", "value": round(float(meta.quantile(0.05)), 4)},
            {"label": "S&P 500 5% quantile", "value": round(float(returns["Benchmark"].dropna().quantile(0.05)), 4)},
        ],
    }
    # the compounded annual return over the whole sample, from the weekly returns
    annual_return = (1 + returns.dropna()).prod() ** (52 / len(returns.dropna())) - 1
    worst_quarter = drawdown.min()
    LAST.update(annual_return=annual_return, worst_quarter=worst_quarter)
    charts["risk-max-drawdown"] = {
        "type": "scatter",
        "title": "Microsoft matched Meta's 26% a year with a worst quarter of -28% instead of -45%",
        "xname": "Worst quarterly drawdown",
        "yname": "Annual return",
        "xformat": "percent",
        "yformat": "percent",
        "points": [
            {"name": NAMES.get(t, t), "x": round(float(worst_quarter[t]), 4), "y": round(float(annual_return[t]), 4)}
            for t in worst_quarter.index
        ],
        "highlight": [list(worst_quarter.index).index("Benchmark")],
    }

    return charts
