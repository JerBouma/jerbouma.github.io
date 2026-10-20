"""Charts for /projects/financetoolkit/docs#getting-started (the overview guide)."""

from financetoolkit import Discovery, Toolkit

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

    # Explore the Modules, Discovery: the semiconductor screen, primary listings only
    discovery = Discovery(api_key=API_KEY)
    semis = discovery.get_stock_screener(
        industry="Semiconductors", country="US", market_cap_higher=100_000_000_000, is_etf=False
    )
    caps = semis.loc[~semis.index.str.contains(r"\.", regex=True)]
    caps = caps.loc[caps["Exchange"].str.contains("NASDAQ|New York", regex=True)]
    caps = caps["Market Cap (USD)"].sort_values(ascending=False)
    # how many of the next chipmakers together are still worth less than Nvidia
    behind = int((caps.iloc[1:].cumsum() < caps.iloc[0]).sum())
    charts["getting-started-semiconductors"] = {
        "type": "bar",
        "title": f"Nvidia is worth more than the next {behind} US chipmakers combined",
        "x": list(caps.index),
        "series": [{"name": "Market cap", "data": [round(float(v)) for v in caps]}],
        "format": "usd",
        "highlight": 0,
    }

    # Explore the Modules, Models: the Extended DuPont analysis over the last five years
    dupont = companies.models.get_extended_dupont_analysis()
    parts = [("Interest Burden Ratio", "Interest burden", "percent"),
             ("Tax Burden Ratio", "Tax burden", "percent"),
             ("Operating Profit Margin", "Operating margin", "percent"),
             ("Asset Turnover", "Asset turnover", "multiple"),
             ("Equity Multiplier", "Equity multiplier", "multiple")]
    tabs = []
    for ticker in TICKERS:
        frame = dupont.loc[ticker].dropna(axis=1, how="any").iloc[:, -5:]
        tabs.append({
            "label": NAMES[ticker],
            "years": [label(c) for c in frame.columns],
            "components": [{"name": short, "format": fmt, "data": values(frame.loc[row])} for row, short, fmt in parts],
            "result": {"name": "Return on equity", "format": "percent", "data": values(frame.loc["Return on Equity"])},
        })
    charts["getting-started-dupont"] = {
        "type": "dupont",
        "title": "Apple's equity multiplier of 5.5x turns a 32% operating margin into a 171% return on equity",
        "tabs": tabs,
    }
    return charts
