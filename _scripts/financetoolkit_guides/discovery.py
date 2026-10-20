"""Charts for /projects/financetoolkit/docs/discovery#getting-started."""

from financetoolkit import Discovery, Toolkit

from .common import API_KEY, frame_chart

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


def bars(series, title: str, name: str, fmt: str) -> dict:
    """Vertical bars, largest first."""
    series = series.dropna().sort_values(ascending=False)
    return {
        "type": "bar",
        "title": title,
        "x": [str(i) for i in series.index],
        "series": [{"name": name, "data": [round(float(v), 4) for v in series]}],
        "format": fmt,
    }


def build() -> dict:
    discovery = Discovery(api_key=API_KEY)
    charts = {}

    screener = discovery.get_stock_screener(**SCREEN)
    caps = screener["Market Cap (USD)"] if "Market Cap (USD)" in screener else screener["Market Cap"]
    charts["discovery-screener"] = bars(
        caps, "Stocks that pass the screen, by market cap (USD)", "Market cap", "usd"
    )

    sectors = discovery.get_sector_performance(date="2024-02-01")
    charts["discovery-sector-performance"] = bars(
        sectors["Average Change"] / 100, "Average change per sector on 2024-02-01", "Average change", "percent"
    )

    sector_pe = discovery.get_sector_pe(sector="Technology")
    charts["discovery-sector-pe"] = frame_chart(
        sector_pe[["PE Ratio"]].rename(columns={"PE Ratio": "Technology"}), fmt="ratio",
        title="P/E ratio of the Technology sector",
    )

    # the screened tickers straight into the Toolkit
    tickers = screener.index.tolist()
    companies = Toolkit(tickers=tickers, api_key=API_KEY)
    cumulative = companies.get_historical_data()["Cumulative Return"]
    total = cumulative.drop(columns="Benchmark", errors="ignore").ffill().iloc[-1] - 1
    chart = bars(total, "Cumulative return of the screened stocks since " + str(cumulative.index[0])[:10],
                 "Cumulative return", "percent")
    # the S&P 500 as a reference bar, in its own colour
    benchmark = float(cumulative["Benchmark"].ffill().iloc[-1] - 1)
    names = chart["x"] + ["S&P 500"]
    data = chart["series"][0]["data"] + [round(benchmark, 4)]
    order = sorted(range(len(names)), key=lambda i: data[i], reverse=True)
    chart["x"] = [names[i] for i in order]
    chart["series"][0]["data"] = [data[i] for i in order]
    chart["highlight"] = chart["x"].index("S&P 500")
    charts["discovery-screener-returns"] = chart
    return charts
