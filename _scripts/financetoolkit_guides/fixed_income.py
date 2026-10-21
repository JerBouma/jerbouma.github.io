"""Charts for the Fixed Income guide (/projects/financetoolkit/docs/fixedincome#getting-started)."""

import pandas as pd
from financetoolkit import FixedIncome

from .common import frame_chart, label, line

# the frames behind the charts, kept for checking the numbers in the text
LAST = {}

BLUE, INDIGO, ORANGE, GREEN, PINK = "#38bdf8", "#818cf8", "#f97316", "#34d399", "#f472b6"


def resample(df: pd.DataFrame, freq: str = "W") -> pd.DataFrame:
    """A daily series as its last observation per week or month, enough for a chart of years."""
    frame = df.copy()
    if isinstance(frame.index, pd.PeriodIndex):
        frame.index = frame.index.to_timestamp()
    frame.index = pd.to_datetime(frame.index)
    frame = frame.dropna(how="all")
    if freq == "W":
        # the last observation of each week, under its own date
        return frame.groupby(pd.Grouper(freq="W")).tail(1)
    frame = frame.resample(freq).last().dropna(how="all")
    frame.index = frame.index.to_period("M")
    return frame


def zero(chart: dict) -> dict:
    """Adds a dashed line at 0% to a chart."""
    chart["series"].append({"name": "0%", "data": [0] * len(chart["x"]), "reference": True})
    return chart


def build() -> dict:
    fixedincome = FixedIncome(start_date="2012-01-01")
    charts = {}

    LAST["statistics"] = fixedincome.collect_bond_statistics(
        par_value=1000, coupon_rate=0.05, years_to_maturity=5, yield_to_maturity=0.08, frequency=2
    )

    # Duration over the grid of coupon rates and maturities
    duration = fixedincome.get_duration()
    LAST["duration"] = duration
    coupons = [rate for rate in [0.01, 0.03, 0.05, 0.07, 0.09] if rate in duration.index]
    last = duration.columns[-1]
    charts["fixed-income-duration"] = line(
        [str(i + 1) for i in range(len(duration.columns))],
        {f"{rate:.0%} coupon": duration.loc[rate] for rate in coupons},
        fmt="ratio",
        title=f"Lower coupons mean more rate risk: {duration.loc[0.01, last]:.1f} against "
              f"{duration.loc[0.09, last]:.1f} years at a ten-year maturity",
        xname="Years to maturity",
        smooth=True,
    )

    # Swaptions: the two models side by side, and each across maturities
    prices = {}
    for model, extra in [("black", {}), ("bachelier", {"volatility_type": "lognormal"})]:
        prices[model] = fixedincome.get_derivative_price(
            model=model, forward_rate=0.0325, volatility=0.20, risk_free_rate=0.02, notional=10_000_000, **extra
        )
        LAST[model] = prices[model]
    strikes = [f"{rate:.2%}" for rate in prices["black"].index]
    columns = list(prices["black"].columns)
    five = columns[4]
    atm = [{"x": "3.25%", "label": "At the money"}]
    # up to just past the money, where the two models differ; above it they are almost identical
    low = [i for i, rate in enumerate(prices["black"].index) if rate <= 0.0426]
    head = line([strikes[i] for i in low],
                {"Black": prices["black"][five].iloc[low], "Bachelier": prices["bachelier"][five].iloc[low]},
                fmt="amount", kind="bar", xname="Strike rate (5 years to maturity)")
    head["series"][1]["color"] = ORANGE
    tabs = [{"label": "Black against Bachelier", **head}]
    for model, name in [("black", "Black"), ("bachelier", "Bachelier")]:
        pick = {f"{i} year{'s' if i > 1 else ''}": columns[i - 1] for i in (1, 3, 5, 10) if i <= len(columns)}
        tabs.append({"label": f"{name} by maturity",
                     **line(strikes, {k: prices[model][c] for k, c in pick.items()}, fmt="amount", xname="Strike rate", markers=atm)})
    charts["fixed-income-swaption"] = {
        "type": "tabs",
        "title": "Black and Bachelier agree at the money and part ways deep out of it",
        "tabs": tabs,
    }

    # Euribor
    euribor = fixedincome.get_euribor_rates()
    LAST["euribor"] = euribor
    charts["fixed-income-euribor"] = zero(frame_chart(
        euribor,
        fmt="percent",
        title="Euribor spent seven years below zero, then reached 4% in little over a year",
        bands=[{"from": "2022-07", "to": "2023-09", "label": "ECB hikes"}],
    ))

    # Central banks: both policy rates together, then each in detail
    ecb = resample(fixedincome.get_european_central_bank_rates(), "ME")
    fed = resample(fixedincome.get_federal_reserve_rates(), "ME")
    LAST["ecb"], LAST["fed"] = ecb, fed
    both = pd.DataFrame({"Fed funds rate (effective)": fed["Rate"], "ECB deposit rate": ecb["Deposit"]}).dropna(how="all")
    LAST["both"] = both
    together = frame_chart(both, fmt="percent")
    together["series"][1]["color"] = ORANGE
    fed_detail = frame_chart(
        fed[["Rate", "Target Rate From", "Target Rate To"]].rename(
            columns={"Rate": "Effective rate", "Target Rate From": "Target, lower", "Target Rate To": "Target, upper"}),
        fmt="percent", cloud=["Target, lower", "Target, upper"])
    for s in fed_detail["series"][1:]:
        s.update({"dashed": True, "color": INDIGO})
    charts["fixed-income-central-banks"] = {
        "type": "tabs",
        "title": "The ECB went from -0.5% to 4%, the Fed from near zero to 5.33%",
        "tabs": [
            {"label": "Fed and ECB", **zero(together)},
            {"label": "European Central Bank", **zero(frame_chart(ecb, fmt="percent"))},
            {"label": "Federal Reserve", **fed_detail},
        ],
    }

    # Government bond yields: five markets over time, and the latest across countries
    government = fixedincome.get_government_bond_yield(short_term=False)
    LAST["government"] = government
    countries = ["United States", "Japan", "Germany", "China", "United Kingdom"]
    latest = government.dropna(how="all").iloc[-1].dropna().rename({"EA20": "Euro area"}).sort_values(ascending=False)
    LAST["latest"] = latest
    charts["fixed-income-government"] = {
        "type": "tabs",
        "title": "Germany and Japan yielded below zero in 2020, the United States and the United Kingdom close to 5% now",
        "tabs": [
            {"label": "Five markets", **zero(frame_chart(government[countries], fmt="percent",
                                                         bands=[{"from": "2020Q1", "to": "2021Q4", "label": "Covid"}]))},
            {"label": f"All countries, {label(government.dropna(how='all').index[-1])}",
             **line(list(latest.index), {"10-year yield": latest.values}, fmt="percent", kind="bar",
                    highlight=list(latest.index).index("United States"))},
        ],
    }

    # ICE BofA option-adjusted spreads, split into investment grade and high yield
    spread = resample(fixedincome.get_ice_bofa_option_adjusted_spread(maturity=False), "W")
    LAST["spread"] = spread
    weeks = [label(d) for d in spread.index]
    tariffs = [{"from": next(w for w in weeks if w >= "2025-04-01"), "to": next(w for w in weeks if w >= "2025-05-01"),
                "label": "Tariff shock"}] if weeks[0] < "2025-04-01" < weeks[-1] else []
    grades = [c for c in ["AAA", "AA", "A", "BBB"] if c in spread.columns]
    junk = [c for c in ["BB", "B", "CCC"] if c in spread.columns]
    charts["fixed-income-oas"] = {
        "type": "tabs",
        "title": f"CCC spreads widened to {spread['CCC'].iloc[-1]:,.0f} basis points while the rest stayed tight",
        "tabs": [
            {"label": "High yield", **frame_chart(spread[junk], fmt="number", bands=tariffs)},
            {"label": "Investment grade", **frame_chart(spread[grades], fmt="number", bands=tariffs)},
        ],
    }

    # ICE BofA yield to worst: the curve then and now, and over time
    ytw = fixedincome.get_ice_bofa_yield_to_worst(maturity=True)
    weekly_ytw = resample(ytw, "W")
    LAST["ytw"] = weekly_ytw
    first, now = weekly_ytw.index[0], weekly_ytw.index[-1]
    curve = pd.DataFrame({label(first): weekly_ytw.loc[first], label(now): weekly_ytw.loc[now]})
    LAST["curve"] = curve
    curve_chart = line(list(curve.index), {c: curve[c] for c in curve.columns}, fmt="percent", kind="bar")
    curve_chart["series"][0]["color"] = INDIGO
    curve_chart["series"][1]["color"] = BLUE
    charts["fixed-income-ytw"] = {
        "type": "tabs",
        "title": "Short corporate yields fell, long ones did not: the curve steepened (yield to worst)",
        "tabs": [
            {"label": "Curve then and now", **curve_chart},
            {"label": "Over time", **frame_chart(weekly_ytw, fmt="percent")},
        ],
    }

    return charts
