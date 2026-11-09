"""Charts for the Fixed Income guide (/projects/financetoolkit/docs/fixedincome#getting-started)."""

import os

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
    fixedincome = FixedIncome(start_date="2012-01-01", api_key=os.environ.get("FINANCIAL_MODELING_PREP_KEY", ""))
    charts = {}

    LAST["statistics"] = fixedincome.collect_bond_statistics(date="2026-11-05")

    # Every Treasury security on one day: nominal and real yields by years to maturity
    treasuries = fixedincome.get_treasury_securities(date="2026-11-05")
    LAST["treasuries"] = treasuries
    bonds = treasuries[treasuries["Security Type"] != "FRN"].copy()
    years = (pd.to_datetime(bonds["Maturity"]) - pd.Timestamp("2026-11-05")).dt.days / 365.25
    bonds["Years"] = years.clip(lower=0).astype(int) + 1
    bonds["Kind"] = bonds["Security Type"].where(bonds["Security Type"] == "TIPS", "Nominal")
    curve = bonds.groupby(["Years", "Kind"])["Yield to Maturity"].mean().unstack()
    LAST["treasury_curve"] = curve
    print("Treasury securities:", len(treasuries), treasuries["Security Type"].value_counts().to_dict())
    print(curve.loc[[1, 2, 5, 10, 20, 30]].round(4).to_string())
    curve_chart = line([str(y) for y in curve.index],
                       {"Bills, notes and bonds": curve["Nominal"], "TIPS (real yield)": curve["TIPS"]},
                       fmt="percent", xname="Years to maturity")
    curve_chart["series"][1]["color"] = ORANGE
    charts["fixed-income-treasuries"] = curve_chart

    # Corporate bonds from the bond ETF holdings: Apple's yields and G-spreads by maturity
    apple = fixedincome.get_bond_universe(issuer="APPLE INC").sort_values("Maturity")
    LAST["apple"] = apple
    print("Apple bonds:", len(apple), apple["Maturity"].min(), apple["Maturity"].max())
    maturities = [str(m)[:10] for m in apple["Maturity"]]
    ytm = line(maturities, {"Yield to maturity": apple["Yield to Maturity"]}, fmt="percent", xname="Maturity")
    spread = line(maturities, {"G-spread": apple["G-Spread"]}, fmt="percent", kind="bar", xname="Maturity")
    spread["series"][0]["color"] = ORANGE
    charts["fixed-income-corporate"] = {
        "type": "tabs",
        "tabs": [{"label": "Yield to maturity", **ytm}, {"label": "G-spread", **spread}],
    }

    # Euribor
    euribor = fixedincome.get_euribor_rates()
    LAST["euribor"] = euribor
    charts["fixed-income-euribor"] = zero(frame_chart(
        euribor,
        fmt="percent",
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
        "tabs": [
            {"label": "Curve then and now", **curve_chart},
            {"label": "Over time", **frame_chart(weekly_ytw, fmt="percent")},
        ],
    }

    return charts
