"""Charts for the Economics guide (/projects/financetoolkit/docs/getting-started/economics)."""

from financetoolkit import Economics
from financetoolkit.economics import oecd_model

from .common import frame_chart

# the frames behind the charts, kept for checking the numbers in the text
LAST = {}


def build() -> dict:
    economics = Economics(start_date="2015-01-01")
    charts = {}

    gdp = economics.get_gross_domestic_product(inflation_adjusted=True)
    gdp_index = gdp.loc[:, ["United States", "China", "Germany", "Japan"]]
    gdp_index = gdp_index / gdp_index.iloc[0] * 100
    LAST["gdp"] = gdp_index
    charts["economics-gdp"] = frame_chart(gdp_index, fmt="number", title="Real GDP, 2015 = 100")

    inflation = economics.get_inflation_rate()
    LAST["inflation"] = inflation.loc[:, ["United States", "United Kingdom", "Brazil", "Turkey"]]
    charts["economics-inflation"] = frame_chart(LAST["inflation"], fmt="percent", title="Inflation rate")

    smoothed = economics.get_inflation_rate(rolling=3).loc[:, ["United States", "United Kingdom", "Brazil", "Turkey"]]
    LAST["inflation_rolling"] = smoothed
    charts["economics-inflation-rolling"] = frame_chart(smoothed, fmt="percent", title="Inflation rate, 3-year rolling average")

    cci = economics.get_consumer_confidence_index()
    LAST["cci"] = cci.loc[:, ["United States", "South Africa", "China", "Spain", "Germany"]]
    charts["economics-cci"] = frame_chart(LAST["cci"], fmt="number", title="Consumer Confidence Index (long-term average = 100)")

    countries = ["United States", "United Kingdom", "Japan", "Germany", "France", "Canada"]
    long_term = economics.get_long_term_interest_rate(period="quarterly").loc[:, countries]
    short_term = economics.get_short_term_interest_rate(period="quarterly").loc[:, countries]
    LAST["long_term"], LAST["short_term"] = long_term, short_term
    charts["economics-rates"] = {
        "type": "tabs",
        "title": "Interest rates by country",
        "tabs": [
            {"label": "Long term (10-year)", **frame_chart(long_term, fmt="percent")},
            {"label": "Short term (3-month)", **frame_chart(short_term, fmt="percent")},
        ],
    }

    house_prices = economics.get_house_prices()
    LAST["house_prices"] = house_prices
    charts["economics-house-prices"] = frame_chart(
        house_prices[["Australia", "United States", "United Kingdom", "Spain", "Brazil"]],
        fmt="number",
        title="House price index (2015 = 100)",
    )

    unemployment = oecd_model.get_unemployment_rate(period="quarterly")
    selection = unemployment.loc["1990":, ["United States", "Germany", "Japan", "Spain", "Canada"]]
    LAST["unemployment"] = selection
    charts["economics-unemployment"] = frame_chart(selection, fmt="percent", title="Unemployment rate, quarterly")

    return charts
