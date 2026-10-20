"""Charts for the Options guide: the same calls as the code on that page."""

import pandas as pd
from financetoolkit import Toolkit
from financetoolkit.options import greeks_model

from .common import API_KEY, label, line, values

TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN"]
NAMES = {"AAPL": "Apple", "MSFT": "Microsoft", "GOOGL": "Alphabet", "AMZN": "Amazon"}
# a listed expiration far enough out to stay available for a while
EXPIRATION = "2027-12-17"


def by_strike(frame: pd.DataFrame, picks=(0, 14, -1), prefix: str = "Expires") -> dict:
    """Value against the strike price, one series per selected expiration date."""
    columns = list(frame.columns)
    chosen = sorted({columns[i] for i in picks}, key=columns.index)
    return line(frame.index, {f"{prefix} {label(c)}": frame[c] for c in chosen}, fmt="ratio", xname="Strike price")


def ticker_tabs(frame: pd.DataFrame, title: str, fmt: str = "ratio", **kwargs) -> dict:
    tabs = []
    for ticker in TICKERS:
        spec = by_strike(frame.loc[ticker], **kwargs)
        spec["format"] = fmt
        tabs.append({"label": NAMES[ticker], **spec})
    return {"type": "tabs", "title": title, "tabs": tabs}


def lattice(paths: pd.DataFrame) -> dict:
    """The recombining tree of simulated prices: one line per number of down moves."""
    columns = list(paths.columns)
    nodes = [sorted(set(paths[c].round(4)), reverse=True) for c in columns]
    series = {}
    for downs in range(len(columns)):
        series[f"{downs} down"] = [nodes[t][downs] if downs < len(nodes[t]) else None for t in range(len(columns))]
    x = [label(c) for c in columns]
    return {
        "x": x,
        "series": [{"name": name, "data": data} for name, data in series.items()],
        "format": "price",
        "type": "line",
        "title": "",
    }


def build() -> dict:
    companies = Toolkit(TICKERS, api_key=API_KEY, start_date="2005-01-01")
    charts = {}

    black_scholes = companies.options.get_black_scholes_model()
    charts["options-black-scholes"] = ticker_tabs(black_scholes, "Black-Scholes value of a call option by strike price", fmt="price")

    binomial = companies.options.get_binomial_model(american_option=True)
    price = companies.get_historical_data()["Adj Close"].iloc[-1]
    strikes = binomial.loc["AAPL"].index.get_level_values(0).unique()
    atm = min(strikes, key=lambda k: abs(k - price["AAPL"]))
    tree = binomial.loc[("AAPL", atm)].iloc[:5, :5]
    print("Apple price", price["AAPL"], "ATM strike", atm)
    print(tree.round(2).to_string())

    chains = companies.options.get_option_chains(expiration_date=EXPIRATION)
    implied_volatility = companies.options.get_implied_volatility(expiration_date=EXPIRATION)
    apple_chain = chains.loc["AAPL"]
    near = apple_chain[(apple_chain.index > price["AAPL"] * 0.85) & (apple_chain.index < price["AAPL"] * 1.15)]
    print(near[["Last Price", "Bid", "Ask", "Volume", "Open Interest", "Implied Volatility", "In The Money"]].to_string())
    iv_tabs = []
    for ticker in TICKERS:
        iv = implied_volatility.loc[ticker].dropna()
        iv = iv[(iv.index >= price[ticker] * 0.6) & (iv.index <= price[ticker] * 1.5) & (iv > 0)]
        iv_tabs.append({"label": NAMES[ticker], **line([f"{k:g}" for k in iv.index], {"Implied volatility": iv},
                                                       fmt="percent", xname="Strike price")})
    charts["options-implied-volatility"] = {
        "type": "tabs",
        "title": f"Implied volatility by strike price, expiring {EXPIRATION}",
        "tabs": iv_tabs,
    }

    simulations = companies.options.get_stock_price_simulation(timesteps=10)
    charts["options-simulation"] = {
        "type": "tabs",
        "title": "Simulated stock prices of the binomial tree",
        "tabs": [{"label": NAMES[t], **lattice(simulations.loc[t])} for t in TICKERS],
    }

    delta = companies.options.get_delta()
    charts["options-delta"] = ticker_tabs(delta, "Delta of a call option by strike price")

    dual_gamma = companies.options.get_dual_gamma(
        start_date="2020-01-02",
        strike_price_range=0.2,
        expiration_time_range=180,
        show_input_info=True,
    )
    charts["options-dual-gamma"] = ticker_tabs(dual_gamma, "Dual Gamma by strike price, from 2 January 2020", picks=(29, 89, -1))

    greeks = companies.options.collect_all_greeks()
    last = greeks.columns.get_level_values(0)[-1]
    apple = greeks.loc["AAPL"][last]
    around = [k for k in apple.index if abs(k - atm) <= 20 and (k - atm) % 20 == 0]
    print("Greeks", last, "\n", apple.loc[around].T.round(4).to_string())

    # Delta and Gamma against the stock price, from the model functions directly
    STRIKE_PRICE, RISK_FREE_RATE, TIME_TO_EXPIRATION, VOLATILITY, DIVIDEND_YIELD = 100, 0.05, 180 / 365, 0.2, 0.01
    inputs = dict(strike_price=STRIKE_PRICE, risk_free_rate=RISK_FREE_RATE, time_to_expiration=TIME_TO_EXPIRATION,
                  volatility=VOLATILITY, dividend_yield=DIVIDEND_YIELD)
    prices = list(range(50, 150, 1))
    call = pd.Series({s: greeks_model.get_delta(stock_price=s, **inputs) for s in prices})
    put = pd.Series({s: greeks_model.get_delta(stock_price=s, put_option=True, **inputs) for s in prices})
    gamma = pd.Series({s: greeks_model.get_gamma(stock_price=s, **inputs) for s in prices})
    x = [f"{s}" for s in prices]
    charts["options-delta-gamma"] = {
        "type": "tabs",
        "title": "Delta and Gamma of a $100 strike option against the stock price",
        "tabs": [
            {"label": "Delta", **line(x, {"$100 Call Delta": call, "$100 Put Delta": put}, fmt="ratio", xname="Stock price")},
            {"label": "Gamma", **line(x, {"$100 Gamma": gamma}, fmt="ratio", xname="Stock price")},
        ],
    }
    print("gamma peak at", gamma.idxmax(), gamma.max(), "call delta at 100", call[100], "put", put[100])
    return charts
