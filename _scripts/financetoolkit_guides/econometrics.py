"""Charts for the Econometrics guide (/projects/financetoolkit/docs/econometrics#getting-started)."""

from financetoolkit import Toolkit

from .common import API_KEY, frame_chart, line, values

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
        "title": "Five of ten stocks explain Apple's weekly returns, and the consumer staples name PG is one of them",
        "x": list(rows.index),
        "coef": [round(float(c), 4) for c in rows["Coefficient"]],
        "low": [round(float(c - 1.96 * se), 4) for c, se in zip(rows["Coefficient"], rows["Std. Error"])],
        "high": [round(float(c + 1.96 * se), 4) for c, se in zip(rows["Coefficient"], rows["Std. Error"])],
        "p": [round(float(p), 4) for p in rows["P-Value"]],
    }

    weekly = companies.get_historical_data(period="weekly")
    weekly_returns = weekly["Return"]
    correlations = weekly_returns.drop(columns="Benchmark").corr()
    LAST.update(weekly=weekly, correlations=correlations)
    order = list(correlations.columns)
    charts["econometrics-correlations"] = {
        "type": "heatmap",
        "title": "Apple's regressors move with each other too, which is what makes the regression hard to read",
        "x": order,
        "y": order,
        "values": [values(correlations.loc[t, order], 2) for t in order],
    }

    LAST["jarque_bera"] = companies.econometrics.get_jarque_bera_test(period="quarterly", within_period=False)
    granger = companies.econometrics.get_granger_causality(period="weekly")
    LAST["granger"] = granger
    into_apple = granger.loc["AAPL", "P-Value"].astype(float).sort_values()
    LAST["into_apple"] = into_apple
    spec = line(list(into_apple.index), {"P-value": into_apple.values}, fmt="ratio", kind="bar")
    spec["series"].append({"name": "5% significance", "data": [0.05] * len(spec["x"]), "reference": True})
    charts["econometrics-granger"] = {**spec, "title": "Of the ten stocks, only Amazon's past returns help predict Apple's"}

    prices = weekly["Adj Close"][["AAPL", "TSM"]]
    LAST["prices"] = prices
    spec = frame_chart(prices, fmt="price", format2="price")
    spec["series"][1]["axis"] = 1
    charts["econometrics-prices"] = {**spec, "title": "Apple and TSMC rose together until the turn of 2022, then TSMC fell much further"}

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
        "type": "bar",
        "title": "On top of the common SWKS effect, Nvidia earned 0.75% a week of its own",
        "x": list(effects.index),
        "series": [{"name": "Entity effect", "data": [round(float(v), 4) for v in effects]}],
        "format": "percent",
    }

    return charts
