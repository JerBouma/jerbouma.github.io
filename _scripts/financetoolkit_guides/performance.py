"""Charts for the Performance guide (/projects/financetoolkit/docs/getting-started/performance)."""

from financetoolkit import Toolkit
from financetoolkit.performance import performance_model

from .common import API_KEY, frame_chart

TICKERS = ["ASML", "MSFT", "AAPL", "WMT"]
FACTORS = ["Mkt-RF", "SMB", "HML", "RMW", "CMA"]

# the frames behind the charts, kept for checking the numbers in the text
LAST = {}


def build() -> dict:
    companies = Toolkit(TICKERS, api_key=API_KEY, start_date="2005-01-01")
    charts = {}

    alpha = companies.performance.get_jensens_alpha(period="quarterly")
    capm = companies.performance.get_capital_asset_pricing_model(period="yearly")
    LAST.update(alpha=alpha, capm=capm)
    charts["performance-alpha"] = frame_chart(alpha, fmt="percent", title="Jensen's Alpha per quarter")
    charts["performance-capm"] = frame_chart(capm, fmt="percent", kind="bar", title="Expected return per year according to CAPM")

    sharpe = companies.performance.get_sharpe_ratio(period="monthly", rolling=12)
    LAST["sharpe"] = sharpe
    charts["performance-sharpe"] = frame_chart(sharpe, fmt="ratio", title="12-month rolling Sharpe Ratio")

    sortino = companies.performance.get_sortino_ratio(period="yearly")
    treynor = companies.performance.get_treynor_ratio(period="yearly")
    LAST.update(sortino=sortino, treynor=treynor)
    charts["performance-sortino-treynor"] = {
        "type": "tabs",
        "title": "Sortino and Treynor Ratio per year",
        "tabs": [
            {"label": "Sortino Ratio", **frame_chart(sortino, fmt="ratio", kind="bar")},
            {"label": "Treynor Ratio", **frame_chart(treynor, fmt="ratio", kind="bar")},
        ],
    }

    fama_and_french = companies.performance.get_fama_and_french_model(period="yearly", method="simple")
    LAST["fama_and_french"] = fama_and_french
    charts["performance-fama-french"] = {
        "type": "tabs",
        "title": "R-squared of each Fama-French factor per year",
        "tabs": [
            {"label": ticker, **frame_chart(fama_and_french[ticker].xs("R Squared", level=1, axis=1)[FACTORS], fmt="ratio")}
            for ticker in TICKERS
        ],
    }

    correlations = companies.performance.get_factor_asset_correlations(period="quarterly")
    LAST["correlations"] = correlations
    charts["performance-factor-correlations"] = {
        "type": "tabs",
        "title": "Quarterly correlation with the Fama-French factors",
        "tabs": [{"label": ticker, **frame_chart(correlations[ticker][FACTORS], fmt="ratio")} for ticker in TICKERS],
    }

    LAST["dataset"] = performance_model.obtain_fama_and_french_dataset()

    return charts
