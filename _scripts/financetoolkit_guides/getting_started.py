"""Charts for /projects/financetoolkit/docs#getting-started (the overview guide)."""

from financetoolkit import Toolkit

from .common import API_KEY, frame_chart, label, line, values

TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN"]
NAMES = {"AAPL": "Apple", "MSFT": "Microsoft", "GOOGL": "Alphabet", "AMZN": "Amazon", "Benchmark": "S&P 500"}

# the market shocks that shaped these series, on a quarterly axis and on a yearly one
QUARTER_BANDS = [
    {"from": "2007Q4", "to": "2009Q1", "label": "Financial crisis"},
    {"from": "2020Q1", "to": "2020Q2", "label": "Covid"},
    {"from": "2022Q1", "to": "2022Q4", "label": "Inflation shock"},
]
YEAR_BANDS = [
    {"from": "2008", "to": "2009", "label": "Financial crisis"},
    {"from": "2020", "to": "2021", "label": "Covid"},
]


def renamed(frame):
    """Company names instead of tickers as series names."""
    return frame.rename(columns=NAMES)


def since(frame, first, last=2025):
    """The fiscal years from first to last (fiscal 2026 is Microsoft's alone)."""
    return frame[[c for c in frame.columns if first <= int(str(c)[:4]) <= last]]


def build() -> dict:
    companies = Toolkit(TICKERS, api_key=API_KEY, start_date="2005-01-01")
    charts = {}

    # Historical data: quarterly cumulative returns, the S&P 500 (SPY) included
    cumulative = renamed(companies.get_historical_data(period="quarterly")["Cumulative Return"])
    cumulative = cumulative[[NAMES[t] for t in TICKERS] + ["S&P 500"]]
    growth = frame_chart(cumulative, fmt="multiple", bands=QUARTER_BANDS)
    for s in growth["series"]:
        if s["name"] == "S&P 500":
            s["dashed"] = True
    final = cumulative.ffill().iloc[-1].sort_values(ascending=False)
    ranking = line(list(final.index), {"Cumulative return": final}, fmt="multiple", kind="bar",
                   highlight=list(final.index).index("S&P 500"))
    charts["getting-started-cumulative"] = {
        "type": "tabs",
        "title": f"$1 in Apple in 2005 is worth ${final['Apple']:.0f} now; in the S&P 500, ${final['S&P 500']:.0f}",
        "tabs": [
            {"label": "Growth since 2005", **growth},
            {"label": "Where each ended", **ranking},
        ],
    }

    # Financial statements: total shareholder equity, Apple's capital return programme marked
    balance_sheet = companies.get_balance_sheet_statement()
    equity = renamed((balance_sheet.xs("Total Shareholder Equity", level=1).T / 1e9)[TICKERS])
    equity = equity[[int(str(p)[:4]) <= 2025 for p in equity.index]]  # fiscal 2026 is Microsoft's alone
    charts["getting-started-equity"] = frame_chart(
        equity, fmt="billions",
        title="Apple's equity peaked in 2017 and has since fallen by half, while the others kept building",
        markers=[{"x": "2012", "label": "Apple starts buybacks"}, {"x": "2017", "label": "Apple's peak"}],
    )

    # Revenue growth; Alphabet's 57-93% of 2005-2007 would flatten everything else, so it starts in 2008
    income_statement_growth = companies.get_income_statement(growth=True)
    revenue_growth = renamed(income_statement_growth.loc[:, "Revenue", :].T[TICKERS])
    revenue_growth = revenue_growth[[2008 <= int(str(p)[:4]) <= 2025 for p in revenue_growth.index]]
    charts["getting-started-revenue-growth"] = {
        "type": "tabs",
        "title": "Alphabet's revenue grew 41% in 2021 and Amazon's 38% in 2020; since 2022 none has topped 18%",
        "tabs": [
            {"label": name, **frame_chart(revenue_growth[[name]], fmt="percent", kind="bar", bands=YEAR_BANDS)}
            for name in revenue_growth.columns
        ],
    }

    # trailing: the net profit margin over four years, one card per company
    trailing = since(companies.ratios.get_net_profit_margin(trailing=4), 2015).loc[TICKERS].rename(index=NAMES)
    charts["getting-started-trailing"] = {
        "type": "kpis",
        "title": "Trailing net margin: Microsoft keeps 36 cents per dollar of revenue, Amazon 7",
        "x": list(trailing.index),
        "series": [{"name": str(year), "data": values(trailing[year])} for year in trailing.columns],
        "format": "percent",
    }

    # standardize: the operating margin as a Z-Score, company by year
    standardized = companies.ratios.get_operating_margin(standardize=True)
    standardized = since(standardized, 2015).loc[TICKERS].rename(index=NAMES)
    charts["getting-started-standardized"] = {
        "type": "heatmap",
        "title": "Operating margin Z-Scores: all four above their own average, Amazon by 2.4",
        "x": [str(c) for c in standardized.columns],
        "y": list(standardized.index),
        "values": [values(standardized.loc[name], 2) for name in standardized.index],
    }

    # rolling: the 12-month beta of Apple and Alphabet, with the market's beta of 1
    rolling = companies.performance.get_beta(period="monthly", rolling=12)
    rolling = rolling[[str(p) >= "2015-01" for p in rolling.index]]
    beta = frame_chart(renamed(rolling[["AAPL", "GOOGL"]]), fmt="ratio", smooth=True,
                       title="Alphabet's rolling beta swung from -0.7 at the start of 2025 to 2.6 by mid-2026")
    beta["series"].append({"name": "Market (beta 1)", "data": [1] * len(beta["x"]), "reference": True})
    charts["getting-started-beta"] = beta

    # Analyst estimates: the EPS consensus, average with the low-high range, years with five analysts or more
    estimates = companies.get_analyst_estimates()
    years = sorted({int(str(c)[:4]) for c in estimates.columns if int(str(c)[:4]) >= 2026})
    fan = []
    for ticker in TICKERS:
        frame = estimates.loc[ticker]
        frame = frame.loc[:, [int(str(c)[:4]) in years for c in frame.columns]]
        covered = frame.loc["Number of Analysts"] >= 5
        pick = lambda row: values(frame.loc[row].where(covered), 2)
        fan.append({"name": NAMES[ticker], "q05": pick("Estimated EPS Low"), "q5": pick("Estimated EPS Average"),
                    "q95": pick("Estimated EPS High")})
    keep = [i for i in range(len(years)) if any(f["q5"][i] is not None for f in fan)]
    for f in fan:
        for key in ("q05", "q5", "q95"):
            f[key] = [f[key][i] for i in keep]
    charts["getting-started-estimates"] = {
        "type": "fan", "title": "Analysts expect Microsoft's earnings per share to reach $45 by 2031, from $17 in 2026",
        "x": [str(years[i]) for i in keep], "series": fan, "format": "price",
        "center": "average", "range": "low to high",
    }

    # ESG scores: the combined score per company and year
    esg = companies.get_esg_scores()["ESG Score"][TICKERS]
    esg = esg[[2015 <= int(str(p)[:4]) for p in esg.index]].rename(columns=NAMES)
    charts["getting-started-esg"] = {
        "type": "heatmap", "title": "Amazon has the lowest ESG score of the four every year; Apple's fell from 64.6 in 2023 to 54.9 in 2025",
        "x": [label(p) for p in esg.index], "y": list(esg.columns),
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
    share = products["Services"].iloc[-1] / products.iloc[-1].sum()
    charts["getting-started-segments"] = {
        "type": "tabs",
        "title": f"Services is now {share:.0%} of Apple's revenue, up from {products['Services'].iloc[0] / products.iloc[0].sum():.0%} in 2019",
        "tabs": [
            {"label": "By product", **frame_chart(products, fmt="billions", kind="bar", stack=True)},
            {"label": "By region", **frame_chart(regions, fmt="billions", kind="bar", stack=True)},
        ],
    }
    return charts
