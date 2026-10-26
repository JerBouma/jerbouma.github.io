"""Charts for the ETF guide (/projects/financetoolkit/docs/etf#getting-started)."""

from financetoolkit import Toolkit

from .common import API_KEY, frame_chart, line, values

FUNDS = ["VOO", "RSP", "QQQ", "SCHD"]
INDEX_FUNDS = ["VOO", "IVV"]

# the frames behind the charts, kept for checking the numbers in the text
LAST = {}


def build() -> dict:
    # holdings, weightings and profiles are those of today, so this Toolkit runs up to today
    funds = Toolkit(FUNDS, api_key=API_KEY)
    charts = {}

    profile = funds.etf.get_profile()
    holdings = funds.etf.get_holdings(limit=5)
    LAST.update(profile=profile, holdings=holdings)

    # sector weightings as 100% stacked bars, one bar per fund, the largest sectors first
    sectors = funds.etf.get_sector_weightings()
    sectors = sectors.drop(index="Cash & Others", errors="ignore")
    sectors = sectors.loc[sectors.max(axis=1).sort_values(ascending=False).index]
    LAST["sectors"] = sectors
    charts["etf-sectors"] = line(
        FUNDS, {sector: sectors.loc[sector, FUNDS] for sector in sectors.index},
        fmt="percent", kind="bar", stack=True,
    )

    # concentration and overlap, one tab each, as bars so every tab has the height of the heatmap
    concentration = funds.etf.get_concentration()
    overlap = funds.etf.get_overlap()
    LAST.update(concentration=concentration, overlap=overlap)
    top_10 = line(FUNDS, {"Top 10 weight": concentration.loc["Top 10 Weight", FUNDS].astype(float)},
                  fmt="percent", kind="bar")
    effective = line(FUNDS, {"Effective number of holdings": concentration.loc["Effective Number of Holdings", FUNDS].astype(float)},
                     fmt="number", kind="bar")
    # the overlap of a fund with itself says nothing
    cells = [[None if a == b else round(float(overlap.loc[a, b]), 2) for b in FUNDS] for a in FUNDS]
    charts["etf-concentration"] = {"type": "panels", "panels": [
        {**top_10, "label": "Top 10 weight", "height": 380, "cards": False},
        {**effective, "label": "Effective number of holdings", "height": 380, "cards": False},
        {"type": "heatmap", "label": "Overlap", "x": FUNDS, "y": FUNDS, "values": cells,
         "min": 0, "max": 1, "scale": "sequential", "digits": 2, "height": 380},
    ]}

    # the valuation of the largest 50 holdings of each fund
    valuation = funds.etf.get_look_through_valuation(holdings=50)
    LAST["valuation"] = valuation
    charts["etf-valuation"] = {"type": "panels", "panels": [
        {**line(FUNDS, {"Price-to-earnings": valuation.loc["Price-to-Earnings", FUNDS]}, fmt="ratio", kind="bar"),
         "label": "Price-to-earnings"},
        {**line(FUNDS, {"Dividend yield": valuation.loc["Dividend Yield", FUNDS]}, fmt="percent", kind="bar"),
         "label": "Dividend yield"},
        {**line(FUNDS, {"Coverage": valuation.loc["Coverage", FUNDS]}, fmt="percent", kind="bar"),
         "label": "Coverage"},
    ]}

    # two S&P 500 funds against the largest one, SPY, from 2021 to 2025
    index_funds = Toolkit(INDEX_FUNDS, api_key=API_KEY, start_date="2021-01-01", end_date="2025-12-31",
                          benchmark_ticker="SPY")
    tracking = index_funds.etf.get_tracking()
    yearly = index_funds.etf.get_tracking(yearly=True)
    LAST.update(tracking=tracking, yearly=yearly)
    charts["etf-tracking"] = frame_chart(yearly[INDEX_FUNDS], fmt="percent", kind="bar")

    liquidity = funds.etf.get_liquidity()
    LAST["liquidity"] = liquidity
    charts["etf-liquidity"] = line(
        FUNDS, {"Average dollar volume": liquidity.loc["Average Dollar Volume", FUNDS] / 1e9},
        fmt="billions", kind="bar",
    )
    return charts
