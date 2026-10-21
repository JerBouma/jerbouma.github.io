"""Charts for the Options guide: the same calls as the code on that page."""

import numpy as np
import pandas as pd
from financetoolkit import Toolkit
from financetoolkit.options import greeks_model

from .common import API_KEY, label, line, values

TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN"]
NAMES = {"AAPL": "Apple", "MSFT": "Microsoft", "GOOGL": "Alphabet", "AMZN": "Amazon"}
# a listed expiration far enough out to stay available for a while
EXPIRATION = "2027-12-17"
# the expirations shown from the default grid of 1 to 29 days: a day, two weeks, four weeks
PICKS = (0, 13, -1)


def days_out(frame: pd.DataFrame, column) -> int:
    """Calendar days from the stock price date to an expiration column."""
    return (pd.Period(column, "D") - pd.Period(frame.columns[0], "D")).n + 1


def days_label(frame: pd.DataFrame, column) -> str:
    n = days_out(frame, column)
    return f"{n} day" if n == 1 else f"{n} days"


def by_strike(frame: pd.DataFrame, picks=PICKS, fmt: str = "ratio", **extra) -> dict:
    """Value against the strike price, one series per selected expiration date."""
    columns = list(frame.columns)
    chosen = sorted({columns[i] for i in picks}, key=columns.index)
    return line([f"{k:g}" for k in frame.index],
                {days_label(frame, c): frame[c] for c in chosen},
                fmt=fmt, xname="Strike price", **extra)


def lattice(paths: pd.DataFrame) -> dict:
    """The recombining tree of simulated prices: one line per number of down moves."""
    columns = list(paths.columns)
    nodes = [sorted(set(paths[c].round(4)), reverse=True) for c in columns]
    # from green (all up moves) through indigo to pink (all down moves)
    stops = [(0x34, 0xd3, 0x99), (0x81, 0x8c, 0xf8), (0xf4, 0x72, 0xb6)]
    series = []
    for downs in range(len(columns)):
        f = downs / (len(columns) - 1) * 2
        a, b = stops[int(min(f, 1.999))], stops[int(min(f, 1.999)) + 1]
        t = f - int(min(f, 1.999))
        color = "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))
        series.append({"name": f"{downs} down",
                       "data": [round(nodes[i][downs], 2) if downs < len(nodes[i]) else None for i in range(len(columns))],
                       "color": color})
    return {"type": "line", "x": [label(c) for c in columns], "series": series, "format": "price"}


def build() -> dict:
    companies = Toolkit(TICKERS, api_key=API_KEY, start_date="2005-01-01")
    charts = {}
    price = companies.get_historical_data()["Adj Close"].iloc[-1]

    # Black-Scholes: Apple's call value and its time value by strike
    black_scholes = companies.options.get_black_scholes_model()
    apple_bs = black_scholes.loc["AAPL"]
    strikes = apple_bs.index
    atm = min(strikes, key=lambda k: abs(k - price["AAPL"]))
    time_value = apple_bs.sub(np.maximum(price["AAPL"] - strikes.values, 0), axis=0)
    marker = [{"x": f"{atm:g}", "label": f"Stock ${price['AAPL']:.2f}"}]
    value_chart = by_strike(apple_bs, fmt="price", markers=marker)
    time_chart = by_strike(time_value, fmt="price", markers=marker)
    time_chart["series"][-1]["area"] = True
    charts["options-black-scholes"] = {
        "type": "tabs",
        "tabs": [{"label": "Time value", **time_chart}, {"label": "Call value", **value_chart}],
    }
    print("Apple price", price["AAPL"], "ATM strike", atm)
    print("BS AAPL:\n", apple_bs.loc[atm - 20:atm + 20, [apple_bs.columns[i] for i in PICKS]].round(2).to_string())
    print("Time value AAPL:\n", time_value.loc[atm - 20:atm + 20, [apple_bs.columns[i] for i in PICKS]].round(2).to_string())

    binomial = companies.options.get_binomial_model(american_option=True)
    binomial_strikes = binomial.loc["AAPL"].index.get_level_values(0).unique()
    binomial_atm = min(binomial_strikes, key=lambda k: abs(k - price["AAPL"]))
    print("Binomial ATM", binomial_atm, "\n", binomial.loc[("AAPL", binomial_atm)].iloc[:5, :5].round(2).to_string())

    # option chains and implied volatility: the skew of all four by moneyness,
    # and where Apple's open interest sits
    chains = companies.options.get_option_chains(expiration_date=EXPIRATION)
    implied_volatility = companies.options.get_implied_volatility(expiration_date=EXPIRATION)
    apple_chain = chains.loc["AAPL"]
    near = apple_chain[(apple_chain.index > price["AAPL"] * 0.94) & (apple_chain.index < price["AAPL"] * 1.07)]
    print(near[["Last Price", "Bid", "Ask", "Volume", "Open Interest", "Implied Volatility", "In The Money"]].to_string())
    buckets = np.round(np.arange(0.6, 1.501, 0.05), 2)
    skew = {}
    for ticker in TICKERS:
        iv = implied_volatility.loc[ticker].dropna()
        iv = iv[iv > 0]
        moneyness = (np.round(iv.index.values / price[ticker] / 0.05) * 0.05).round(2)
        skew[NAMES[ticker]] = iv.groupby(moneyness).median().reindex(buckets)
    skew_chart = line([f"{b:.0%}" for b in buckets], skew, fmt="percent", xname="Strike as % of the stock price",
                      markers=[{"x": "100%", "label": "At the money"}])
    window = apple_chain[(apple_chain.index >= 250) & (apple_chain.index <= 450)]
    oi_x = [f"{k:g}" for k in window.index]
    oi_chart = line(oi_x, {"Open interest": window["Open Interest"]}, kind="bar", fmt="amount", xname="Strike price")
    oi_chart["highlight"] = int(np.argmin(np.abs(window.index.values - price["AAPL"])))
    charts["options-implied-volatility"] = {
        "type": "tabs",
        "tabs": [
            {"label": "Volatility skew", **skew_chart},
            {"label": "Apple's open interest", **oi_chart},
        ],
    }
    print("Skew:\n", pd.DataFrame(skew).round(3).to_string())
    print("OI top:\n", window["Open Interest"].sort_values().tail(6).to_string())

    # the binomial tree of stock prices, and where its 1,024 paths end
    simulations = companies.options.get_stock_price_simulation(timesteps=10)
    apple_paths = simulations.loc["AAPL"]
    ends = apple_paths.iloc[:, -1].round(2).value_counts().sort_index()
    end_chart = line([f"${v:,.0f}" for v in ends.index], {"Paths ending here": ends}, kind="bar", fmt="amount",
                     xname="Price after ten steps")
    end_chart["highlight"] = int(np.argmin(np.abs(ends.index.values - price["AAPL"])))
    charts["options-simulation"] = {
        "type": "tabs",
        "tabs": [
            {"label": "The tree", **lattice(apple_paths)},
            {"label": "Where the paths end", **end_chart},
        ],
    }
    print("Ends:\n", ends.to_string())

    # Delta: a grid of strikes and expirations for Apple
    delta = companies.options.get_delta()
    apple_delta = delta.loc["AAPL"]
    grid_strikes = [k for k in apple_delta.index if abs(k - atm) <= 40 and (k - atm) % 10 == 0]
    grid_days = [apple_delta.columns[i] for i in (0, 6, 13, 20, 28)]
    charts["options-delta"] = {
        "type": "heatmap",
        "x": [days_label(apple_delta, c) for c in grid_days],
        "y": [f"${k:g} strike" for k in grid_strikes],
        "values": [[round(float(apple_delta.loc[k, c]), 2) for c in grid_days] for k in grid_strikes],
    }
    print("Delta grid:\n", apple_delta.loc[grid_strikes, grid_days].round(2).to_string())

    dual_gamma = companies.options.get_dual_gamma(
        start_date="2020-01-02",
        strike_price_range=0.2,
        expiration_time_range=180,
        show_input_info=True,
    )
    dg_tabs = []
    for ticker in ["MSFT", "AMZN", "AAPL", "GOOGL"]:
        spec = by_strike(dual_gamma.loc[ticker], picks=(29, 89, -1), fmt="num", smooth=True)
        spec["series"][0]["area"] = True
        dg_tabs.append({"label": NAMES[ticker], **spec})
    charts["options-dual-gamma"] = {
        "type": "tabs",
        "tabs": dg_tabs,
    }
    msft_dg = dual_gamma.loc["MSFT"]
    print("MSFT price 2020-01-02:", companies.get_historical_data()["Adj Close"].loc["2020-01-02"].round(2).to_dict())
    print("Dual gamma MSFT peak:", {c: (msft_dg[c].idxmax(), round(msft_dg[c].max(), 4)) for c in [msft_dg.columns[i] for i in (29, 89, -1)]})

    greeks = companies.options.collect_all_greeks()
    last_greek = greeks.columns.get_level_values(0)[-1]
    apple = greeks.loc["AAPL"][last_greek]
    around = [k for k in apple.index if abs(k - atm) <= 20 and (k - atm) % 20 == 0]
    print("Greeks", last_greek, "\n", apple.loc[around].T.round(4).to_string())

    # Delta and Gamma against the stock price, from the model functions directly
    STRIKE_PRICE, RISK_FREE_RATE, TIME_TO_EXPIRATION, VOLATILITY, DIVIDEND_YIELD = 100, 0.05, 180 / 365, 0.2, 0.01
    inputs = dict(strike_price=STRIKE_PRICE, risk_free_rate=RISK_FREE_RATE, time_to_expiration=TIME_TO_EXPIRATION,
                  volatility=VOLATILITY, dividend_yield=DIVIDEND_YIELD)
    prices = list(range(50, 152, 2))
    call = pd.Series({s: greeks_model.get_delta(stock_price=s, **inputs) for s in prices})
    put = pd.Series({s: greeks_model.get_delta(stock_price=s, put_option=True, **inputs) for s in prices})
    gamma = pd.Series({s: greeks_model.get_gamma(stock_price=s, **inputs) for s in prices})
    dg_chart = line([f"{s}" for s in prices], {"Call Delta": call, "Put Delta": put, "Gamma (right axis)": gamma},
                    fmt="ratio", xname="Stock price", smooth=True, format2="num")
    dg_chart["series"][2].update({"axis": 1, "area": True, "color": "#f97316"})
    charts["options-delta-gamma"] = dg_chart
    print("gamma peak at", gamma.idxmax(), gamma.max(), "call delta at 100", call[100], "put", put[100],
          "call delta 80/120", call[80], call[120])
    return charts
