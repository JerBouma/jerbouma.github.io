"""Charts and outputs of the Solvency pages (solvency/market-consistency.md and capital.md).

The page's risk-neutral run is scenarios.simulate(n_simulations=2000, seed=42, measure="risk_neutral"); it is
reproduced here from the README's saved risk-neutral calibration of 2026-10-19, as the README does."""

import numpy as np

from common import CALIBRATION_RISK_NEUTRAL, NUMBERS, bar, default_run, hist, labels, runs_fan, tabs, write
from financescenarios import (
    CalibrationResult, Portfolio, Scenarios, Solvency, equity_scr, martingale_test,
)
from financescenarios.config.config_model import risk_neutral_config

TITLES = {
    "solvency-risk-neutral": "US Short Rate and Stocks, Real-World and Risk-Neutral",
    "solvency-martingale": "Discounted US Stock Price against Today's Price",
    "solvency-own-funds": "Own Funds after One Year, Discounted to Today",
}
charts = {}

scenarios, calibration, result = default_run()
market = Scenarios.from_config(risk_neutral_config(scenarios.config))
risk_neutral = market.simulate(n_simulations=2000, seed=42, calibration=CalibrationResult.load(CALIBRATION_RISK_NEUTRAL))
print(risk_neutral.factor_names)
print(risk_neutral.describe())

runs = {"Real-world": result, "Risk-neutral": risk_neutral}
charts["solvency-risk-neutral"] = tabs({
    "Short rate": runs_fan(runs, "united_states_short_rate"),
    "US stocks": runs_fan(runs, "us_broad", fmt="price", levels=True),
})
for name, run in runs.items():
    print(name, run.horizon_summary([1, 5], factors=["united_states_short_rate", "us_broad"]).select(
        "factor", "horizon", "mean", "q0.05", "q0.5", "q0.95"))

solvency = Solvency(real_world=result, risk_neutral=risk_neutral)
print("short rate", solvency.short_rate, "asset", solvency.asset, "dividend yield", solvency._dividend_yield())
test = martingale_test(risk_neutral, asset="us_broad", short_rate="united_states_short_rate",
                       dividend_yield=0.0099)  # the yield the risk-neutral fit used, 0.99%
print(test.passed, test.pass_rate, test.max_abs_deviation)
# solvency-martingale: test.table, the discounted mean price and its 95% band, each as a ratio to today's price
start = test.table["deflated_mean"][0]
charts["solvency-martingale"] = bar(
    labels(test.table["date"]),
    {"Discounted mean price": test.table["ratio"], "Lower 95% bound": test.table["lower"] / start,
     "Upper 95% bound": test.table["upper"] / start},
    fmt="ratio", kind="line",
)
for s_ in charts["solvency-martingale"]["series"][1:]:
    s_["dashed"] = True

assets = Portfolio.from_preset(result, preset="balanced_60_40").compute(initial_value=60_000, rebalance_every=12)
report = solvency.report(cashflows=[10_000] * 5, assets=assets)
print(report)
for row in report.iter_rows():
    print(row)

# solvency-own-funds: the data of solvency.plot(cashflows=[10_000] * 5, assets=assets)
own_funds = solvency._own_funds([10_000] * 5, assets)
step = result.step_at(1.0)
discounted = result.discount_factor_paths(solvency.short_rate)[:, step] * own_funds[:, step]
today = float(own_funds[:, 0].mean())
charts["solvency-own-funds"] = hist(
    discounted, width=1_000, xname="Own funds after one year, discounted to today", fmt="amount",
    markers={"Today": today, "1 in 200": np.quantile(discounted, 0.005)},
)
NUMBERS["own funds"] = {"today": today, "q005": float(np.quantile(discounted, 0.005)),
                        "median": float(np.median(discounted))}

print(equity_scr(type_1_value=1_000_000, type_2_value=250_000, symmetric_adjustment=0.0771))

write("solvency", charts, TITLES)
