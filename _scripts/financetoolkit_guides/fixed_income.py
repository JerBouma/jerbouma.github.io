"""Charts for the Fixed Income guide (/projects/financetoolkit/docs/fixedincome#getting-started)."""

import pandas as pd
from financetoolkit import FixedIncome

from .common import frame_chart, line

# the frames behind the charts, kept for checking the numbers in the text
LAST = {}


def weekly(df: pd.DataFrame) -> pd.DataFrame:
    """A daily series as its last observation per week, enough for a chart of a decade."""
    frame = df.copy()
    if isinstance(frame.index, pd.PeriodIndex):
        frame.index = frame.index.to_timestamp()
    frame.index = pd.to_datetime(frame.index)
    return frame.dropna(how="all").groupby(pd.Grouper(freq="W")).tail(1)


def maturity_labels(columns) -> list:
    return [str(i + 1) for i in range(len(columns))]


def build() -> dict:
    fixedincome = FixedIncome(start_date="2012-01-01")
    charts = {}

    LAST["statistics"] = fixedincome.collect_bond_statistics(
        par_value=1000, coupon_rate=0.05, years_to_maturity=5, yield_to_maturity=0.08, frequency=2
    )

    duration = fixedincome.get_duration()
    LAST["duration"] = duration
    charts["fixed-income-duration"] = line(
        maturity_labels(duration.columns),
        {f"{rate:.0%} coupon": duration.loc[rate] for rate in [0.01, 0.03, 0.05, 0.07, 0.09] if rate in duration.index},
        fmt="ratio",
        title="Modified duration by coupon rate (yield to maturity 8%)",
        xname="Years to maturity",
    )

    tabs = []
    # the same 20% lognormal volatility in both models; Bachelier converts it to a normal one
    for model, name, extra in [("black", "Black", {}), ("bachelier", "Bachelier", {"volatility_type": "lognormal"})]:
        prices = fixedincome.get_derivative_price(
            model=model,
            forward_rate=0.0325,
            volatility=0.20,
            risk_free_rate=0.02,
            notional=10_000_000,
            **extra,
        )
        LAST[model] = prices
        columns = list(prices.columns)
        pick = {f"{i} year{'s' if i > 1 else ''}": columns[i - 1] for i in (1, 3, 5, 10) if i <= len(columns)}
        tabs.append({
            "label": name,
            **line([f"{rate:.2%}" for rate in prices.index], {k: prices[c] for k, c in pick.items()},
                   fmt="usd", xname="Strike rate"),
        })
    charts["fixed-income-swaption"] = {"type": "tabs", "title": "Receiver swaption value on a notional of 10 million", "tabs": tabs}

    euribor = fixedincome.get_euribor_rates()
    charts["fixed-income-euribor"] = frame_chart(euribor, fmt="percent", title="Euribor rates by maturity")

    ecb = weekly(fixedincome.get_european_central_bank_rates())
    fed = weekly(fixedincome.get_federal_reserve_rates())
    fed_columns = [c for c in ["Rate", "Target Rate From", "Target Rate To"] if c in fed.columns]
    charts["fixed-income-central-banks"] = {
        "type": "tabs",
        "title": "Policy rates of the ECB and the Federal Reserve",
        "tabs": [
            {"label": "European Central Bank", **frame_chart(ecb, fmt="percent")},
            {"label": "Federal Reserve", **frame_chart(fed[fed_columns].rename(columns={"Rate": "Effective Federal Funds Rate"}), fmt="percent")},
        ],
    }

    government = fixedincome.get_government_bond_yield(short_term=False)
    countries = ["United States", "Japan", "Germany", "China", "United Kingdom"]
    charts["fixed-income-government"] = frame_chart(
        government[[c for c in countries if c in government.columns]], fmt="percent", title="10-year government bond yields"
    )

    spread = fixedincome.get_ice_bofa_option_adjusted_spread(maturity=False)
    charts["fixed-income-oas"] = frame_chart(spread, fmt="number", title="ICE BofA option-adjusted spread by rating (basis points)")

    ytw = fixedincome.get_ice_bofa_yield_to_worst(maturity=True)
    charts["fixed-income-ytw"] = frame_chart(ytw, fmt="percent", title="ICE BofA yield to worst by maturity")

    return charts
