"""Charts for /projects/financetoolkit/docs/ratios#getting-started."""

from financetoolkit import Toolkit

from .common import API_KEY, frame_chart, heatmap, values

TICKERS = ["AAPL", "AMZN", "META", "WMT"]
NAMES = {"AAPL": "Apple", "AMZN": "Amazon", "META": "Meta", "WMT": "Walmart"}
LAGS = {"Lag 1": "1 year", "Lag 2": "2 years", "Lag 3": "3 years"}
LAST = 2025  # the latest fiscal year all four have reported


def years(frame, since, until=LAST):
    """The fiscal years from since to until, as columns."""
    return frame[[c for c in frame.columns if since <= int(str(c)[:4]) <= until]]


def by_year(frame, since):
    """Tickers as rows, years as columns -> years as rows, company names as columns."""
    return years(frame.loc[TICKERS], since).T.rename(columns=NAMES)


def build() -> dict:
    companies = Toolkit(TICKERS, api_key=API_KEY, start_date="2005-01-01")
    charts = {}

    # collect_all_ratios: the gross margin of each company, one card each
    all_ratios = companies.ratios.collect_all_ratios()
    gross_margin = years(all_ratios.xs("Gross Margin", level=1).loc[TICKERS], 2015).rename(index=NAMES)
    charts["ratios-gross-margin"] = {
        "type": "kpis",
        "x": list(gross_margin.index),
        "series": [{"name": str(year), "data": values(gross_margin[year])} for year in gross_margin.columns],
        "format": "percent",
    }

    # Amazon's and Meta's pre-tax income was close to zero in their early years, which makes
    # the effective tax rate swing far outside 0-100%; the chart starts in 2015 for that reason.
    # The US federal corporate rate (35%, 21% from 2018) as a reference
    tax = by_year(companies.ratios.get_effective_tax_rate(), 2015)
    federal = [0.35 if int(str(y)[:4]) < 2018 else 0.21 for y in tax.index]
    tabs = []
    for name in tax.columns:
        tab = frame_chart(tax[[name]], fmt="percent", markers=[{"x": "2018", "label": "US tax reform"}])
        tab["series"].append({"name": "US federal rate", "reference": True, "data": federal})
        tabs.append({"label": name, **tab})
    charts["ratios-effective-tax-rate"] = {
        "type": "tabs",
        "tabs": tabs,
    }

    # Price-to-book growth over the last ten years
    price_to_book_growth = by_year(companies.ratios.get_price_to_book_ratio(growth=True), 2016)
    # company by year, with the colour scale capped at a doubling either way
    charts["ratios-price-to-book-growth"] = heatmap(
        frame_chart(price_to_book_growth), fmt="percent", low=-1, high=1,
    )

    # the growth of the current ratio over one, two and three years, one company per tab
    current_ratio_growth = companies.ratios.get_current_ratio(growth=True, lag=[1, 2, 3])
    charts["ratios-current-ratio-lags"] = {
        "type": "tabs",
        "tabs": [
            {"label": NAMES[ticker],
             **frame_chart(years(current_ratio_growth.loc[ticker], 2015).T.rename(columns=LAGS),
                 fmt="percent", kind="bar")}
            for ticker in TICKERS
        ],
    }

    # trailing EPS; the growth from 2019, as Amazon's 401% of 2016 would flatten the rest
    eps = by_year(companies.ratios.get_earnings_per_share(trailing=4), 2010)
    eps_growth = by_year(companies.ratios.get_earnings_per_share(trailing=4, growth=True), 2019)
    charts["ratios-trailing-eps"] = {
        "type": "tabs",
        "tabs": [
            {"label": "Trailing EPS", **frame_chart(eps, fmt="price")},
            {"label": "Growth", **frame_chart(eps_growth, fmt="percent", kind="bar")},
        ],
    }

    # shareholder yield and debt-to-capital: Apple against Walmart, head to head
    shareholder_yield = years(companies.ratios.get_shareholder_yield(), 2013)
    debt_to_capital = years(companies.ratios.get_debt_to_capital_ratio(), 2013)
    pair = ["AAPL", "WMT"]
    charts["ratios-shareholder-yield"] = {
        "type": "compare",
        "x": [str(c) for c in shareholder_yield.columns],
        "names": {NAMES[t]: NAMES[t] for t in pair},
        "format": "percent",
        "metrics": [
            {"name": name, "series": [{"name": NAMES[t], "data": values(frame.loc[t])} for t in pair]}
            for name, frame in [("Shareholder yield", shareholder_yield), ("Debt-to-capital", debt_to_capital)]
        ],
    }
    return charts
