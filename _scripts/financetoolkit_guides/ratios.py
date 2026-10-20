"""Charts for /projects/financetoolkit/docs/ratios#getting-started."""

from financetoolkit import Toolkit

from .common import API_KEY, frame_chart

TICKERS = ["AAPL", "AMZN", "META", "WMT"]
NAMES = {"AAPL": "Apple", "AMZN": "Amazon", "META": "Meta", "WMT": "Walmart"}


def by_year(frame, since=None):
    """Tickers as rows, years as columns -> years as rows, company names as columns."""
    frame = frame.loc[TICKERS].T.rename(columns=NAMES)
    if since:
        frame = frame[[int(str(p)[:4]) >= since for p in frame.index]]
    return frame


def build() -> dict:
    companies = Toolkit(TICKERS, api_key=API_KEY, start_date="2005-01-01")
    charts = {}

    # Amazon's and Meta's pre-tax income was close to zero in their early years, which makes
    # the effective tax rate swing far outside 0-100%; the chart starts in 2015 for that reason
    tax = companies.ratios.get_effective_tax_rate()
    charts["ratios-effective-tax-rate"] = frame_chart(
        by_year(tax, since=2015), fmt="percent", title="Effective tax rate",
    )

    # Price-to-book growth from 2013, the first full year after Meta's listing
    price_to_book_growth = companies.ratios.get_price_to_book_ratio(growth=True)
    charts["ratios-price-to-book-growth"] = frame_chart(
        by_year(price_to_book_growth, since=2013), fmt="percent", kind="bar",
        title="Growth of the price-to-book ratio",
    )

    current_ratio_growth = companies.ratios.get_current_ratio(growth=True, lag=[1, 2, 3])
    charts["ratios-current-ratio-lags"] = {
        "type": "tabs",
        "title": "Growth of the current ratio over one, two and three years",
        "tabs": [
            {"label": NAMES[ticker],
             **frame_chart(current_ratio_growth.loc[ticker].T.dropna(how="all"), fmt="percent")}
            for ticker in TICKERS
        ],
    }

    eps = companies.ratios.get_earnings_per_share(trailing=4).T.dropna()
    eps_growth = companies.ratios.get_earnings_per_share(trailing=4, growth=True).T.dropna()
    charts["ratios-trailing-eps"] = {
        "type": "tabs",
        "title": "Earnings per share, summed over four years",
        "tabs": [
            {"label": "Trailing EPS", **frame_chart(eps[TICKERS].rename(columns=NAMES), fmt="price")},
            {"label": "Growth", **frame_chart(eps_growth[TICKERS].rename(columns=NAMES), fmt="percent")},
        ],
    }

    shareholder_yield = companies.ratios.get_shareholder_yield()
    debt_to_capital = companies.ratios.get_debt_to_capital_ratio()
    charts["ratios-shareholder-yield"] = {
        "type": "tabs",
        "title": "Cash returned to shareholders and capital structure",
        "tabs": [
            {"label": "Shareholder yield", **frame_chart(by_year(shareholder_yield, since=2013), fmt="percent")},
            {"label": "Debt-to-capital", **frame_chart(by_year(debt_to_capital, since=2013), fmt="percent")},
        ],
    }
    return charts
