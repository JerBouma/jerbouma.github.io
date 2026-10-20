"""Charts for the Econometrics guide (/projects/financetoolkit/docs/getting-started/econometrics)."""

from financetoolkit import Toolkit

from .common import API_KEY

TICKERS = ["AAPL", "TSM", "QCOM", "SWKS", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "XOM", "PG"]

# the frames behind the charts and tables, kept for checking the numbers in the text
LAST = {}


def build() -> dict:
    companies = Toolkit(TICKERS, api_key=API_KEY, start_date="2019-01-01", end_date="2023-01-01")
    charts = {}

    ols = companies.econometrics.get_ols(period="weekly")
    LAST["ols"] = ols
    rows = ols.drop(index="Intercept").sort_values("Coefficient", ascending=False)
    charts["econometrics-ols"] = {
        "type": "coef",
        "title": "Apple's weekly returns regressed on ten stocks: coefficients and 95% confidence intervals",
        "x": list(rows.index),
        "coef": [round(float(c), 4) for c in rows["Coefficient"]],
        "low": [round(float(c - 1.96 * se), 4) for c, se in zip(rows["Coefficient"], rows["Std. Error"])],
        "high": [round(float(c + 1.96 * se), 4) for c, se in zip(rows["Coefficient"], rows["Std. Error"])],
        "p": [round(float(p), 4) for p in rows["P-Value"]],
    }

    LAST["jarque_bera"] = companies.econometrics.get_jarque_bera_test(period="quarterly", within_period=False)
    LAST["granger"] = companies.econometrics.get_granger_causality(period="weekly")
    LAST["adf"] = companies.econometrics.get_augmented_dickey_fuller(period="quarterly")
    LAST["cointegration"] = companies.econometrics.get_engle_granger_cointegration(period="quarterly")

    fixed_effects = companies.econometrics.get_fixed_effects(
        independent_tickers="SWKS",
        dependent_tickers=["TSM", "QCOM", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "XOM", "PG"],
        period="weekly",
    )
    LAST["fixed_effects"] = fixed_effects
    effects = fixed_effects.loc[fixed_effects.index.str.startswith("Entity Effect: "), "Coefficient"]
    effects.index = effects.index.str.replace("Entity Effect: ", "")
    effects = effects.sort_values(ascending=False)
    charts["econometrics-entity-effects"] = {
        "type": "hbar",
        "title": "Entity effects: each stock's own average weekly return",
        "x": list(effects.index),
        "series": [{"name": "Entity effect", "data": [round(float(v), 4) for v in effects]}],
        "format": "percent",
    }

    return charts
