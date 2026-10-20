"""Charts for /projects/financetoolkit/docs#getting-started (the overview guide)."""

from financetoolkit import Toolkit

from .common import API_KEY, frame_chart, line

TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN"]
NAMES = {"AAPL": "Apple", "MSFT": "Microsoft", "GOOGL": "Alphabet", "AMZN": "Amazon", "Benchmark": "S&P 500"}


def renamed(frame):
    """Company names instead of tickers as series names."""
    return frame.rename(columns=NAMES)


def build() -> dict:
    companies = Toolkit(TICKERS, api_key=API_KEY, start_date="2005-01-01")
    charts = {}

    # Historical data: quarterly cumulative returns, the S&P 500 (SPY) included
    cumulative = companies.get_historical_data(period="quarterly")["Cumulative Return"]
    charts["getting-started-cumulative"] = frame_chart(
        renamed(cumulative[TICKERS + ["Benchmark"]]), fmt="multiple",
        title="Cumulative return, quarterly (1 = start)",
    )

    # Financial statements: total shareholder equity and revenue growth
    balance_sheet = companies.get_balance_sheet_statement()
    equity = balance_sheet.xs("Total Shareholder Equity", level=1).T / 1e9
    charts["getting-started-equity"] = frame_chart(
        renamed(equity[TICKERS]), fmt="billions", kind="bar",
        title="Total shareholder equity (USD billions)",
    )

    income_statement_growth = companies.get_income_statement(growth=True)
    revenue_growth = income_statement_growth.loc[:, "Revenue", :].T
    charts["getting-started-revenue-growth"] = frame_chart(
        renamed(revenue_growth[TICKERS]), fmt="percent", title="Revenue growth, year over year",
    )

    # trailing, standardize and rolling
    trailing = companies.ratios.get_net_profit_margin(trailing=4).T.dropna()
    standardized = companies.ratios.get_return_on_equity(standardize=True).T.dropna()
    rolling = companies.performance.get_beta(period="monthly", rolling=12)
    charts["getting-started-parameters"] = {
        "type": "tabs",
        "title": "Three parameters that work across the modules",
        "tabs": [
            {"label": "Trailing net profit margin",
             **frame_chart(renamed(trailing[TICKERS]), fmt="percent")},
            {"label": "Return on equity (Z-Score)",
             **frame_chart(renamed(standardized[TICKERS]), fmt="ratio")},
            {"label": "Rolling 12-month beta",
             **frame_chart(renamed(rolling[TICKERS].dropna(how="all")), fmt="ratio")},
        ],
    }
    return charts
