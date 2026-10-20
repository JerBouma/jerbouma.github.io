"""Charts for the Risk guide (/projects/financetoolkit/docs/getting-started/risk)."""

from financetoolkit import Toolkit

from .common import API_KEY, frame_chart

TICKERS = ["MSFT", "AAPL", "AMZN", "META"]

# the frames behind the charts, kept for checking the numbers in the text
LAST = {}


def _weekly(frame):
    """A daily series as weekly closing values, for the long-run charts."""
    frame = frame.copy()
    frame.index = frame.index.to_timestamp() if hasattr(frame.index, "to_timestamp") else frame.index
    return frame.resample("W").last()


def build() -> dict:
    companies = Toolkit(TICKERS, api_key=API_KEY, start_date="2013-01-01")
    charts = {}

    # one value per ticker over the whole sample, from monthly returns
    LAST["var_sample"] = companies.risk.get_value_at_risk(period="monthly")
    LAST["cvar_sample"] = companies.risk.get_conditional_value_at_risk(period="monthly")

    # one value per month, from the daily returns within that month
    var = companies.risk.get_value_at_risk(period="monthly", within_period=True)
    cvar = companies.risk.get_conditional_value_at_risk(period="monthly", within_period=True)
    rolling_var = companies.risk.get_value_at_risk(period="monthly", rolling=12)
    LAST.update(var=var, cvar=cvar, rolling_var=rolling_var)
    charts["risk-var"] = {
        "type": "tabs",
        "title": "Monthly Value at Risk and Conditional Value at Risk (95%)",
        "tabs": [
            {"label": "VaR", **frame_chart(var, fmt="percent")},
            {"label": "CVaR", **frame_chart(cvar, fmt="percent")},
            {"label": "Rolling 12-month VaR", **frame_chart(rolling_var, fmt="percent")},
        ],
    }

    ulcer = companies.risk.get_ulcer_index(period="yearly", growth=True)
    LAST["ulcer"] = ulcer
    charts["risk-ulcer"] = frame_chart(ulcer, fmt="percent", kind="bar", title="Year-on-year change in the Ulcer Index")

    cdar = companies.risk.get_conditional_drawdown_at_risk(period="quarterly", within_period=True)
    tail = companies.risk.get_tail_ratio(period="yearly", within_period=True)
    LAST.update(cdar=cdar, tail=tail)
    charts["risk-cdar-tail"] = {
        "type": "tabs",
        "title": "Conditional Drawdown at Risk and Tail Ratio",
        "tabs": [
            {"label": "CDaR (quarterly)", **frame_chart(cdar, fmt="percent")},
            {"label": "Tail Ratio (yearly)", **frame_chart(tail, fmt="ratio", kind="bar")},
        ],
    }

    duration = companies.risk.get_maximum_drawdown_duration(period="yearly", within_period=True)
    recovery = companies.risk.get_maximum_drawdown_recovery_time(period="yearly", within_period=True)
    LAST.update(duration=duration, recovery=recovery)
    charts["risk-drawdown-duration"] = {
        "type": "tabs",
        "title": "Length of the worst drawdown in each year, in trading days",
        "tabs": [
            {"label": "Duration", **frame_chart(duration, fmt="number", kind="bar")},
            {"label": "Recovery time", **frame_chart(recovery, fmt="number", kind="bar")},
        ],
    }

    ewma = companies.risk.get_ewma_volatility()
    LAST["ewma"] = ewma
    LAST["hurst"] = companies.risk.get_hurst_exponent()
    charts["risk-ewma"] = frame_chart(_weekly(ewma), fmt="percent", title="EWMA volatility (daily, end of each week)")

    returns = companies.get_historical_data(period="weekly")["Return"]
    drawdown = companies.risk.get_maximum_drawdown(period="quarterly", within_period=True)
    LAST.update(returns=returns, drawdown=drawdown)
    charts["risk-returns"] = frame_chart(returns, fmt="percent", title="Weekly returns")
    charts["risk-max-drawdown"] = frame_chart(drawdown, fmt="percent", title="Maximum drawdown in each quarter")

    return charts
