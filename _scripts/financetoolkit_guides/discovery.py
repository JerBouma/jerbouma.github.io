"""Charts for /projects/financetoolkit/docs/discovery#getting-started."""

import pandas as pd

from financetoolkit import Discovery, Toolkit

from .common import API_KEY, label, values

SCREEN = dict(
    market_cap_higher=1000000,
    market_cap_lower=200000000000,
    price_higher=100,
    price_lower=200,
    beta_higher=1,
    beta_lower=1.5,
    volume_higher=100000,
    volume_lower=2000000,
    dividend_higher=1,
    dividend_lower=2,
    is_etf=False,
)

# the snapshot of every sector's P/E; a recent trading day
PE_DATE = "2026-10-16"

# names that would cover a neighbour in the return-against-beta scatter
LABELS = {"RRX": "top", "AGCO": "bottom", "ODFL": "top", "A": "bottom", "TFII": "top", "AWI": "bottom", "EXPD": "bottom"}


def build() -> dict:
    discovery = Discovery(api_key=API_KEY)
    charts = {}

    # the screen, counted per sector
    screener = discovery.get_stock_screener(**SCREEN)
    sectors = screener["Sector"].value_counts()
    charts["discovery-screener"] = {
        "type": "bar",
        "title": f"{sectors.iloc[0]} of the {len(screener)} stocks that pass the screen are {sectors.index[0].lower()}",
        "x": list(sectors.index),
        "series": [{"name": "Stocks", "data": [int(v) for v in sectors]}],
        "format": "amount",
        "highlight": 0,
    }

    # one day's sector moves: risers and fallers in their own colour
    performance = (discovery.get_sector_performance(date="2024-02-01")["Average Change"] / 100).sort_values(ascending=False)
    charts["discovery-sector-performance"] = {
        "type": "bar",
        "stack": True,
        "title": f"On 1 February 2024 {performance.index[0].lower()} rose {performance.iloc[0]:.1%} "
                 f"while {performance.index[-1].lower()} fell {-performance.iloc[-1]:.1%}",
        "x": list(performance.index),
        "series": [
            {"name": "Rose", "color": "#34d399", "data": [round(float(v), 4) if v >= 0 else None for v in performance]},
            {"name": "Fell", "color": "#f472b6", "data": [round(float(v), 4) if v < 0 else None for v in performance]},
        ],
        "format": "percent",
    }

    # Technology's P/E since 2019 as a monthly average, against its average over the period;
    # and every sector's P/E on one day
    history = discovery.get_sector_pe(sector="Technology", start_date="2019-01-01")["PE Ratio"]
    history.index = pd.to_datetime(history.index)
    monthly = history.resample("ME").mean().dropna()
    x = [d.strftime("%Y-%m") for d in monthly.index]
    snapshot = discovery.get_sector_pe(date=PE_DATE)["PE Ratio"].sort_values(ascending=False)
    charts["discovery-sector-pe"] = {
        "type": "tabs",
        "title": "Technology's P/E fell from 60 to below 30 in 2022 and is back in the high 40s",
        "tabs": [
            {"label": "Technology since 2019", "type": "line", "x": x, "format": "ratio",
             "bands": [{"from": "2020-02", "to": "2020-04", "label": "Covid"},
                       {"from": "2022-01", "to": "2022-12", "label": "Inflation shock"}],
             "series": [
                 {"name": "Technology P/E", "data": values(monthly, 2), "area": True},
                 {"name": f"Average {history.mean():.0f}", "data": [round(float(history.mean()), 2)] * len(x), "reference": True},
             ]},
            {"label": "Every sector on " + PE_DATE, "type": "bar", "x": list(snapshot.index), "format": "ratio",
             "highlight": list(snapshot.index).index("Technology"),
             "series": [{"name": "P/E ratio", "data": values(snapshot, 2)}]},
        ],
    }

    # the screened tickers straight into the Toolkit: five-year return against beta
    tickers = screener.index.tolist()
    companies = Toolkit(tickers=tickers, api_key=API_KEY)
    cumulative = companies.get_historical_data()["Cumulative Return"]
    total = (cumulative.ffill().iloc[-1] - 1).dropna()
    benchmark = float(total.pop("Benchmark"))
    points = [{"name": t, "x": round(float(screener.loc[t, "Beta"]), 2), "y": round(float(r), 4)}
              for t, r in total.items() if t in screener.index]
    for p in points:
        if p["name"] in LABELS:
            p["pos"] = LABELS[p["name"]]
    charts["discovery-screener-returns"] = {
        "type": "scatter",
        "title": f"Betas of 1.0 to 1.5, five-year returns from {total.min():.0%} to +{total.max():.0%}",
        "points": points,
        "xname": "Beta",
        "yname": "Return since " + label(cumulative.index[0]),
        "xformat": "ratio",
        "yformat": "percent",
        # the stocks that beat the S&P 500 in orange
        "highlight": [i for i, p in enumerate(points) if p["y"] > benchmark],
        "lines": [{"axis": "y", "value": round(benchmark, 4), "label": f"S&P 500 +{benchmark:.0%}"},
                  {"axis": "y", "value": 0, "label": ""}],
    }
    return charts
