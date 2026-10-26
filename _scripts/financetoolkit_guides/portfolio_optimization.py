"""Charts for the Portfolio Optimization guide (/projects/financetoolkit/docs/portfolio-optimization#getting-started)."""

import pandas as pd
from financetoolkit import Toolkit

from .common import API_KEY, line

TICKERS = ["VTI", "VEA", "VWO", "TLT", "GLD", "VNQ"]
METHODS = {
    "Minimum variance": "get_minimum_variance_weights",
    "Maximum Sharpe": "get_maximum_sharpe_weights",
    "Risk parity": "get_risk_parity_weights",
    "HRP": "get_hierarchical_risk_parity_weights",
    "Inverse volatility": "get_inverse_volatility_weights",
    "Minimum CVaR": "get_minimum_cvar_weights",
}
# a strategic allocation as the starting point of Black-Litterman: market capitalizations mean little for funds
STRATEGIC = {"VTI": 0.35, "VEA": 0.15, "VWO": 0.05, "TLT": 0.30, "GLD": 0.10, "VNQ": 0.05}
VIEWS = {"VWO": 0.10, "GLD-TLT": 0.03}
CONFIDENCES = {"VWO": 0.5, "GLD-TLT": 0.7}
MIXED = {"QQQ": 0.4, "XLV": 0.2, "AAPL": 0.15, "MSFT": 0.15, "JPM": 0.1}
STOCKS = {"AAPL": 0.2, "MSFT": 0.2, "NVDA": 0.15, "JNJ": 0.1, "LLY": 0.1, "JPM": 0.15, "XOM": 0.1}

# the frames behind the charts, kept for checking the numbers in the text
LAST = {}


def point(name: str, frame: pd.DataFrame, row: str = "Portfolio") -> dict:
    """A portfolio or asset as a point on the risk-return plane."""
    return {"name": name, "x": round(float(frame.loc[row, "Volatility"]), 4),
            "y": round(float(frame.loc[row, "Expected Return"]), 4)}


def build() -> dict:
    assets = Toolkit(TICKERS, api_key=API_KEY, start_date="2015-01-01", end_date="2025-12-31")
    charts = {}

    # six ways to weight the same assets: their weights and where their risk comes from
    portfolios = {name: getattr(assets.portfolio, method)() for name, method in METHODS.items()}
    LAST.update(portfolios)
    weights = pd.DataFrame({name: frame["Weight"].drop("Portfolio") for name, frame in portfolios.items()})
    risk = pd.DataFrame({name: frame["Risk Contribution"].drop("Portfolio") for name, frame in portfolios.items()})
    charts["portfolio-optimization-weights"] = {"type": "panels", "panels": [
        {"label": "Weights", **line(list(weights.columns), {t: weights.loc[t] for t in TICKERS},
                                    fmt="percent", kind="bar", stack=True)},
        {"label": "Risk contributions", **line(list(risk.columns), {t: risk.loc[t] for t in TICKERS},
                                               fmt="percent", kind="bar", stack=True)},
    ]}

    # the efficient frontier, with the portfolios above and the maximum Sharpe portfolio at most 30% per asset
    frontier = assets.portfolio.get_efficient_frontier(points=20)
    capped = assets.portfolio.get_maximum_sharpe_weights(maximum_weight=0.3)
    LAST.update(frontier=frontier, capped=capped)
    points = [point(t, portfolios["Risk parity"], t) for t in TICKERS]
    # the minimum variance and risk parity portfolios lie close together: their names above and below
    marked = [{**point("Minimum variance", portfolios["Minimum variance"]), "pos": "top"},
              point("Maximum Sharpe", portfolios["Maximum Sharpe"]),
              point("Maximum Sharpe, at most 30%", capped),
              {**point("Risk parity", portfolios["Risk parity"]), "pos": "bottom"}]
    charts["portfolio-optimization-frontier"] = {
        "type": "scatter", "xname": "Volatility", "yname": "Expected return",
        "xformat": "percent", "yformat": "percent", "height": 420,
        "points": points + marked,
        "highlight": list(range(len(points), len(points) + len(marked))),
        "curve": [[round(float(v), 4), round(float(r), 4)]
                  for v, r in zip(frontier["Volatility"], frontier["Expected Return"])],
    }

    # equal weights: each asset's share of the weight against its share of the risk
    contributions = assets.portfolio.get_risk_contributions()
    LAST["contributions"] = contributions
    shares = contributions.drop("Total")
    charts["portfolio-optimization-risk"] = line(
        list(shares.index), {"Weight": shares["Weight"], "Share of the risk": shares["Percentage Contribution"]},
        fmt="percent", kind="bar")

    # Black-Litterman: the strategic allocation, moved by two views
    black_litterman = assets.portfolio.get_black_litterman_weights(
        views=VIEWS, view_confidences=CONFIDENCES, market_weights=STRATEGIC)
    LAST["black_litterman"] = black_litterman
    charts["portfolio-optimization-black-litterman"] = {"type": "panels", "panels": [
        {"label": "Weights", **line(list(black_litterman.index), {
            "Strategic weight": black_litterman["Market Weight"],
            "Black-Litterman weight": black_litterman["Weight"]}, fmt="percent", kind="bar")},
        {"label": "Expected returns", **line(list(black_litterman.index), {
            "Implied return": black_litterman["Implied Return"],
            "Black-Litterman return": black_litterman["Black-Litterman Return"]}, fmt="percent", kind="bar")},
    ]}

    # the risk parity portfolio replayed through the crises its assets lived through
    risk_parity = portfolios["Risk parity"]["Weight"].drop("Portfolio").to_dict()
    stress = assets.portfolio.get_stress_test(weights=risk_parity).dropna(subset=["Portfolio Return"])
    LAST["stress"] = stress
    charts["portfolio-optimization-stress"] = line(
        list(stress.index), {"Risk parity portfolio": stress["Portfolio Return"],
                             "S&P 500": stress["Benchmark Return"]}, fmt="percent", kind="bar")

    # looking through two funds and three stocks to their sectors and holdings
    mixed = Toolkit(list(MIXED), api_key=API_KEY, start_date="2025-01-01", end_date="2025-12-31")
    sectors = mixed.portfolio.get_look_through_exposure(weights=MIXED)
    holdings = mixed.portfolio.get_look_through_exposure(weights=MIXED, by="holdings").head(10)
    LAST.update(sectors=sectors, holdings=holdings)
    sectors = sectors[(sectors["Exposure"] > 0) | (sectors["Benchmark Exposure"] > 0)]
    charts["portfolio-optimization-look-through"] = {"type": "panels", "panels": [
        {"label": "Sectors", **line(list(sectors.index), {
            "Portfolio": sectors["Exposure"], "S&P 500": sectors["Benchmark Exposure"]},
            fmt="percent", kind="bar")},
        {"label": "Largest holdings", **line(list(holdings.index), {"Exposure": holdings["Exposure"]},
                                             fmt="percent", kind="bar")},
    ]}

    # Brinson-Fachler attribution of a stock portfolio against the S&P 500, by sector
    stocks = Toolkit(list(STOCKS), api_key=API_KEY, start_date="2025-01-01", end_date="2025-12-31")
    brinson = stocks.portfolio.get_brinson_attribution(weights=STOCKS)
    LAST["brinson"] = brinson
    effects = brinson.drop("Total")
    charts["portfolio-optimization-brinson"] = line(
        list(effects.index), {"Allocation": effects["Allocation Effect"], "Selection": effects["Selection Effect"],
                              "Interaction": effects["Interaction Effect"]}, fmt="percent", kind="bar", stack=True)
    return charts
