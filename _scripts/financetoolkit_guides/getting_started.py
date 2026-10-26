"""Charts for /projects/financetoolkit/docs#getting-started (the overview guide)."""

import pandas as pd
from financetoolkit import Toolkit

from .common import API_KEY, frame_chart, label, line, values

TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN"]
NAMES = {"AAPL": "Apple", "MSFT": "Microsoft", "GOOGL": "Alphabet", "AMZN": "Amazon", "Benchmark": "S&P 500"}

def renamed(frame):
    """Company names instead of tickers as series names."""
    return frame.rename(columns=NAMES)


def since(frame, first, last=2025):
    """The fiscal years from first to last (fiscal 2026 is Microsoft's alone)."""
    return frame[[c for c in frame.columns if first <= int(str(c)[:4]) <= last]]


def combine(charts: dict) -> None:
    """The charts of one example become the tabs of one chart: the three parameters, and earnings and ESG."""
    trailing = charts.pop("getting-started-trailing")
    standardized = charts.pop("getting-started-standardized")
    beta = charts.pop("getting-started-beta")
    charts["getting-started-parameters"] = {"type": "panels", "title": "Trailing, Standardized and Rolling Metrics", "panels": [
        {**trailing, "label": "Trailing net profit margin", "period": False},
        {**standardized, "label": "Operating margin Z-Score"},
        {**beta, "label": "Rolling 12-month beta"},
    ]}
    surprise = charts.pop("getting-started-surprise")
    esg = charts.pop("getting-started-esg")
    charts["getting-started-earnings"] = {"type": "panels", "title": "Revenue Surprise and ESG Scores", "panels": [
        {**surprise, "label": "Revenue surprise"},
        {**esg, "label": "ESG score"},
    ]}


def build() -> dict:
    companies = Toolkit(TICKERS, api_key=API_KEY, start_date="2005-01-01")
    charts = {}

    # Historical data: quarterly cumulative returns, the S&P 500 (SPY) included
    cumulative = renamed(companies.get_historical_data(period="quarterly")["Cumulative Return"])
    cumulative = cumulative[[NAMES[t] for t in TICKERS] + ["S&P 500"]]
    growth = frame_chart(cumulative, fmt="multiple")
    for s in growth["series"]:
        if s["name"] == "S&P 500":
            s["dashed"] = True
    final = cumulative.ffill().iloc[-1].sort_values(ascending=False)
    ranking = line(list(final.index), {"Cumulative return": final}, fmt="multiple", kind="bar",
                   highlight=list(final.index).index("S&P 500"))
    charts["getting-started-cumulative"] = {
        "type": "tabs",
        "tabs": [
            {"label": "Growth since 2005", **growth},
            {"label": "Where each ended", **ranking},
        ],
    }

    # Financial statements: total shareholder equity
    balance_sheet = companies.get_balance_sheet_statement()
    equity = renamed((balance_sheet.xs("Total Shareholder Equity", level=1).T / 1e9)[TICKERS])
    equity = equity[[int(str(p)[:4]) <= 2025 for p in equity.index]]  # fiscal 2026 is Microsoft's alone
    charts["getting-started-equity"] = frame_chart(equity, fmt="billions")

    # Revenue growth; Alphabet's 57-93% of 2005-2007 would flatten everything else, so it starts in 2008
    income_statement_growth = companies.get_income_statement(growth=True)
    revenue_growth = renamed(income_statement_growth.loc[:, "Revenue", :].T[TICKERS])
    revenue_growth = revenue_growth[[2008 <= int(str(p)[:4]) <= 2025 for p in revenue_growth.index]]
    charts["getting-started-revenue-growth"] = {
        "type": "tabs",
        "tabs": [
            {"label": name, **frame_chart(revenue_growth[[name]], fmt="percent", kind="bar")}
            for name in revenue_growth.columns
        ],
    }

    # trailing: the net profit margin over four years, one card per company
    trailing = since(companies.ratios.get_net_profit_margin(trailing=4), 2015).loc[TICKERS].rename(index=NAMES)
    charts["getting-started-trailing"] = {
        "type": "kpis",
        "x": list(trailing.index),
        "series": [{"name": str(year), "data": values(trailing[year])} for year in trailing.columns],
        "format": "percent",
    }

    # standardize: the operating margin as a Z-Score, company by year
    standardized = companies.ratios.get_operating_margin(standardize=True)
    standardized = since(standardized, 2015).loc[TICKERS].rename(index=NAMES)
    charts["getting-started-standardized"] = {
        "type": "heatmap",
        "x": [str(c) for c in standardized.columns],
        "y": list(standardized.index),
        "values": [values(standardized.loc[name], 2) for name in standardized.index],
    }

    # rolling: the 12-month beta of Apple and Alphabet, with the market's beta of 1
    rolling = companies.performance.get_beta(period="monthly", rolling=12)
    rolling = rolling[[str(p) >= "2015-01" for p in rolling.index]]
    beta = frame_chart(renamed(rolling[["AAPL", "GOOGL"]]), fmt="ratio", smooth=True)
    beta["series"].append({"name": "Market (beta 1)", "data": [1] * len(beta["x"]), "reference": True})
    charts["getting-started-beta"] = beta

    # Earnings calendar: revenue against the analyst consensus, per reported quarter
    calendar = companies.get_earnings_calendar()
    surprise = {}
    for ticker in TICKERS:
        frame = calendar.loc[ticker].dropna(subset=["Revenue", "Estimated Revenue"])
        # a report in the first weeks of a quarter covers the quarter before it
        quarters = [pd.Period(d, "Q") - 1 for d in frame.index]
        surprise[NAMES[ticker]] = pd.Series((frame["Revenue"] / frame["Estimated Revenue"] - 1).values, index=quarters)
    surprise = pd.DataFrame(surprise).sort_index().dropna().iloc[-8:]
    charts["getting-started-surprise"] = frame_chart(surprise, fmt="percent", kind="bar")

    # ESG scores: the combined score per company and year
    esg = companies.get_esg_scores()["ESG Score"][TICKERS]
    esg = esg[[2015 <= int(str(p)[:4]) for p in esg.index]].rename(columns=NAMES)
    charts["getting-started-esg"] = {
        "type": "heatmap", "x": [label(p) for p in esg.index], "y": list(esg.columns),
        "values": [values(esg[name], 1) for name in esg.columns],
        "min": 50, "max": 70, "digits": 1, "scale": "sequential",
    }

    # Revenue segmentation: Apple's revenue by product (complete from 2019) and by region
    products = companies.get_revenue_product_segmentation().loc["AAPL"]
    products = products.loc[:, [2019 <= int(str(c)[:4]) <= 2025 for c in products.columns]]
    products = products.loc[(products > 0).any(axis=1)].T / 1e9
    products = products[products.iloc[-1].sort_values(ascending=False).index]
    products = products.rename(columns={"Iphone": "iPhone", "Ipad": "iPad", "Service": "Services",
                                           "Wearables, Home And Accessories": "Wearables and Home"})
    regions = companies.get_revenue_geographic_segmentation().loc["AAPL"]
    regions = regions.loc[:, [2015 <= int(str(c)[:4]) <= 2025 for c in regions.columns]]
    regions = regions.loc[(regions > 0).any(axis=1)].T / 1e9
    regions = regions[regions.iloc[-1].sort_values(ascending=False).index]
    combine(charts)
    charts["getting-started-segments"] = {
        "type": "tabs",
        "tabs": [
            {"label": "By product", **frame_chart(products, fmt="billions", kind="bar", stack=True)},
            {"label": "By region", **frame_chart(regions, fmt="billions", kind="bar", stack=True)},
        ],
    }
    return charts
