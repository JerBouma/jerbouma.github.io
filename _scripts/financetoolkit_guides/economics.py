"""Charts for the Economics guide (/projects/financetoolkit/docs/economics#getting-started)."""

import pandas as pd
from financetoolkit import Economics
from financetoolkit.economics import oecd_model

from .common import frame_chart, label, line

# the frames behind the charts, kept for checking the numbers in the text
LAST = {}

BLUE, INDIGO, ORANGE, GREEN = "#38bdf8", "#818cf8", "#f97316", "#34d399"


def flat(x, value) -> list:
    """A constant reference line, e.g. the long-term average of 100."""
    return [value] * len(x)


def inversions(both: pd.DataFrame, depth: float = 0.005) -> list:
    """Shaded runs of quarters in which the 3-month rate was above the 10-year yield, by 0.5 points at some point."""
    gap = (both["3-month rate"] - both["10-year yield"]).tolist()
    bands, start = [], None
    for i, value in enumerate(gap + [0]):
        flag = value == value and value > 0  # not NaN and inverted
        if flag and start is None:
            start = i
        elif not flag and start is not None:
            if max(gap[start:i]) >= depth:
                bands.append({"from": label(both.index[start]), "to": label(both.index[i - 1]), "label": "Inverted"})
            start = None
    return bands


def build() -> dict:
    economics = Economics(start_date="2015-01-01")
    charts = {}

    # Real GDP, rebased to 2015 = 100
    gdp = economics.get_gross_domestic_product(inflation_adjusted=True)
    gdp_index = gdp.loc[:, ["United States", "China", "Germany", "Japan"]]
    gdp_index = gdp_index / gdp_index.iloc[0] * 100
    LAST["gdp"] = gdp_index
    charts["economics-gdp"] = frame_chart(
        gdp_index,
        fmt="number",
        markers=[{"x": "2020", "label": "Covid"}],
    )

    # Inflation, with Turkey on its own axis
    inflation = economics.get_inflation_rate()
    selection = inflation.loc[:, ["United States", "United Kingdom", "Brazil", "Turkey"]]
    LAST["inflation"] = selection
    shock = [{"from": "2021", "to": "2023", "label": "Inflation shock"}]
    charts["economics-inflation"] = {
        "type": "tabs",
        "tabs": [
            {"label": "All four", **frame_chart(selection, fmt="percent", bands=shock)},
            {"label": "Without Turkey", **frame_chart(selection.drop(columns="Turkey"), fmt="percent", bands=shock)},
        ],
    }

    # Smoothing: the annual rate against its three-year rolling average
    smoothed = economics.get_inflation_rate(rolling=3).loc[:, ["United States", "United Kingdom", "Brazil", "Turkey"]]
    LAST["inflation_rolling"] = smoothed
    chart = line(
        smoothed.index,
        {"US annual": selection["United States"], "US 3-year average": smoothed["United States"],
         "UK annual": selection["United Kingdom"], "UK 3-year average": smoothed["United Kingdom"]},
        fmt="percent",
    )
    for s, color, dashed in zip(chart["series"], [BLUE, BLUE, INDIGO, INDIGO], [True, False, True, False]):
        s.update({"color": color, "dashed": dashed})
    charts["economics-inflation-rolling"] = chart

    # Consumer confidence, with the long-term average of 100
    cci = economics.get_consumer_confidence_index()
    selection = cci.loc[:, ["United States", "China", "Spain", "Germany"]]
    LAST["cci"] = selection
    chart = frame_chart(
        selection,
        fmt="number",
        bands=[{"from": "2020-03", "to": "2020-12", "label": "Covid"},
               {"from": "2022-02", "to": "2022-12", "label": "Inflation shock"}],
    )
    chart["series"].append({"name": "Long-term average", "data": flat(chart["x"], 100), "reference": True})
    charts["economics-cci"] = chart

    # Interest rates: the 10-year yield against the 3-month rate per country
    countries = ["United States", "United Kingdom", "Germany", "Canada", "Japan"]
    long_term = economics.get_long_term_interest_rate(period="quarterly").loc[:, countries]
    short_term = economics.get_short_term_interest_rate(period="quarterly").loc[:, countries]
    LAST["long_term"], LAST["short_term"] = long_term, short_term
    tabs = []
    for country in countries:
        both = pd.DataFrame({"10-year yield": long_term[country], "3-month rate": short_term[country]})
        bands = inversions(both)
        tab = frame_chart(both, fmt="percent", bands=bands)
        tab["series"][1]["area"] = True
        tab["series"][1]["color"] = ORANGE
        tab["label"] = country
        tabs.append(tab)
    charts["economics-rates"] = {
        "type": "tabs",
        "tabs": tabs,
    }

    # House prices: the ranking and the path of five markets
    house_prices = economics.get_house_prices()
    LAST["house_prices"] = house_prices
    major_markets = ["United States", "Canada", "Mexico", "Brazil", "United Kingdom", "Ireland", "Netherlands",
                     "Spain", "Portugal", "Germany", "France", "Italy", "Sweden", "Japan", "South Korea", "China",
                     "India", "Australia"]
    ranking = house_prices.iloc[-1][major_markets].sort_values(ascending=False)
    LAST["ranking"] = ranking
    picked = ["Australia", "United States", "United Kingdom", "Spain", "Brazil"]
    charts["economics-house-prices"] = {
        "type": "tabs",
        "tabs": [
            {"label": "Ranking", **line(list(ranking.index), {"House price index": ranking.values}, fmt="number", kind="bar",
                                        highlight=list(ranking.index).index("United States"))},
            {"label": "Five markets over time", **frame_chart(house_prices[picked], fmt="number",
                                                              markers=[{"x": "2020", "label": "Covid"}])},
        ],
    }

    # Unemployment straight from the OECD model, since 1990
    unemployment = oecd_model.get_unemployment_rate(period="quarterly")
    selection = unemployment.loc["1990":, ["United States", "Germany", "Japan", "Spain", "Canada"]]
    LAST["unemployment"] = selection
    charts["economics-unemployment"] = frame_chart(
        selection,
        fmt="percent",
        bands=[{"from": "2008Q3", "to": "2009Q4", "label": "Financial crisis"},
               {"from": "2011Q3", "to": "2013Q4", "label": "Euro crisis"},
               {"from": "2020Q1", "to": "2020Q4", "label": "Covid"}],
    )

    return charts
