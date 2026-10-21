"""Charts for the Performance guide (/projects/financetoolkit/docs/performance#getting-started)."""

import pandas as pd
from financetoolkit import Toolkit
from financetoolkit.performance import performance_model

from .common import API_KEY, frame_chart, line, values

TICKERS = ["ASML", "MSFT", "AAPL", "WMT"]
FACTORS = ["Mkt-RF", "SMB", "HML", "RMW", "CMA"]
FACTOR_NAMES = {"Mkt-RF": "Market (Mkt-RF)", "SMB": "Size (SMB)", "HML": "Value (HML)",
                "RMW": "Profitability (RMW)", "CMA": "Investment (CMA)"}

# shaded periods: the financial crisis, the Covid crash and the 2022 sell-off
QUARTER_BANDS = [
    {"from": "2008Q3", "to": "2009Q1", "label": "Financial crisis"},
    {"from": "2020Q1", "to": "2020Q2", "label": "Covid"},
    {"from": "2022Q1", "to": "2022Q4", "label": "2022"},
]
MONTH_BANDS = [
    {"from": "2008-09", "to": "2009-03", "label": "Financial crisis"},
    {"from": "2020-02", "to": "2020-06", "label": "Covid"},
    {"from": "2022-01", "to": "2022-12", "label": "2022"},
]

# the frames behind the charts, kept for checking the numbers in the text
LAST = {}


def build() -> dict:
    companies = Toolkit(TICKERS, api_key=API_KEY, start_date="2005-01-01")
    charts = {}

    alpha = companies.performance.get_jensens_alpha(period="quarterly")
    capm = companies.performance.get_capital_asset_pricing_model(period="yearly")
    yearly_returns = companies.get_historical_data(period="yearly")["Return"]
    LAST.update(alpha=alpha, capm=capm, yearly_returns=yearly_returns)

    # the quarterly alphas added up, so the outperformance builds up over time
    cumulative_alpha = alpha.cumsum()
    LAST["cumulative_alpha"] = cumulative_alpha
    spec = frame_chart(cumulative_alpha, fmt="percent", bands=QUARTER_BANDS)
    spec["series"][2]["area"] = True
    charts["performance-alpha"] = {
        **spec,
        "title": "Apple's quarterly alphas add up to 430 percentage points since 2005, more than twice ASML's",
    }

    tabs = []
    for ticker in TICKERS:
        both = pd.DataFrame({"Actual return": yearly_returns[ticker], "CAPM expected return": capm[ticker]}).dropna()
        spec = frame_chart(both, fmt="percent", kind="bar")
        spec["series"][1]["color"] = "#94a3b8"
        tabs.append({"label": ticker, **spec})
    charts["performance-capm"] = {
        "type": "tabs",
        "title": "Actual return against the CAPM expected return: the gap each year is the alpha",
        "tabs": tabs,
    }

    sharpe = companies.performance.get_sharpe_ratio(period="monthly", rolling=12)
    LAST["sharpe"] = sharpe
    tabs = []
    for label_, pair in (("ASML and Walmart", ["ASML", "WMT"]), ("Apple and Microsoft", ["AAPL", "MSFT"])):
        spec = frame_chart(sharpe[pair], fmt="ratio", bands=MONTH_BANDS)
        spec["series"][1]["color"] = "#f97316"
        spec["series"].append({"name": "Zero", "data": [0] * len(spec["x"]), "reference": True})
        tabs.append({"label": label_, **spec})
    charts["performance-sharpe"] = {
        "type": "tabs",
        "title": "Walmart's Sharpe Ratio peaked at 0.65 in September 2008, as ASML's fell to -0.52",
        "tabs": tabs,
    }

    sortino = companies.performance.get_sortino_ratio(period="yearly")
    treynor = companies.performance.get_treynor_ratio(period="yearly")
    beta = companies.performance.get_beta(period="yearly")
    LAST.update(sortino=sortino, treynor=treynor, beta=beta)
    walmart = line(treynor.index, {"Walmart Treynor Ratio": treynor["WMT"], "Walmart Beta": beta["WMT"].reindex(treynor.index)},
                   fmt="ratio", format2="ratio")
    walmart["series"][1]["axis"] = 1
    walmart["series"][1]["dashed"] = True
    charts["performance-sortino-treynor"] = {
        "type": "tabs",
        "title": "Sortino and Treynor tell the same story, until Beta gets close to zero",
        "tabs": [
            {"label": "Sortino Ratio", **frame_chart(sortino, fmt="ratio", kind="bar")},
            {"label": "Treynor Ratio", **frame_chart(treynor[["ASML", "MSFT", "AAPL"]], fmt="ratio", kind="bar")},
            {"label": "Walmart's Treynor and Beta", **walmart},
        ],
    }

    fama_and_french = companies.performance.get_fama_and_french_model(period="yearly", method="simple")
    LAST["fama_and_french"] = fama_and_french
    r_squared = {ticker: fama_and_french[ticker].xs("R Squared", level=1, axis=1)[FACTORS] for ticker in TICKERS}
    LAST["r_squared"] = r_squared
    market = pd.DataFrame({ticker: r_squared[ticker]["Mkt-RF"] for ticker in TICKERS})
    average = pd.DataFrame({ticker: r_squared[ticker].mean() for ticker in TICKERS})
    LAST.update(market_r_squared=market, average_r_squared=average)
    charts["performance-fama-french"] = {
        "type": "tabs",
        "title": "The market factor explains far more of the daily returns than size, value, profitability or investment",
        "tabs": [
            {"label": "Average per factor", **line(list(average.index),
                                                   {t: average[t] for t in TICKERS}, fmt="percent", kind="bar")},
            {"label": "Market factor per year", **frame_chart(market, fmt="percent")},
        ],
    }

    correlations = companies.performance.get_factor_asset_correlations(period="quarterly")
    LAST["correlations"] = correlations
    mean_correlations = pd.DataFrame({ticker: correlations[ticker][FACTORS].mean() for ticker in TICKERS}).T
    LAST["mean_correlations"] = mean_correlations
    charts["performance-factor-correlations"] = {
        "type": "heatmap",
        "title": "ASML, Microsoft and Apple correlate negatively with value and investment, the signature of growth stocks",
        "x": [FACTOR_NAMES[f] for f in FACTORS],
        "y": TICKERS,
        "values": [values(mean_correlations.loc[t, FACTORS], 2) for t in TICKERS],
    }

    LAST["dataset"] = performance_model.obtain_fama_and_french_dataset()

    return charts
