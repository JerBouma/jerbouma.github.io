"""Thirty-year numbers and charts of the Portfolio and Risk Metrics pages (portfolio/portfolio.md, portfolio/risk.md).

The same calibration as every other page, simulated 30 years ahead: a mix of 60% US stocks and 40% cash (the US short
rate) shows what rebalancing, cashflows, a glidepath and fees do over a working life.
"""

import numpy as np

from common import CALIBRATION, NUMBERS, bar, write
from financescenarios import CalibrationResult, GlidepathCheckpoint, Portfolio, Scenarios

TITLES = {
    "portfolio-rebalancing": "Growth per Year over Thirty Years by Percentile",
    "portfolio-plan": "Share of Scenarios with Money Left",
}
charts = {}

calibration = CalibrationResult.load(CALIBRATION)
scenarios = Scenarios.from_profiles(settings="default", factor_set="default")
result = scenarios.simulate(calibration=calibration, years=30, n_simulations=2000, seed=42)

portfolio = Portfolio(result)
weights = {"us_broad": 0.6, "united_states_short_rate": 0.4}

buy_and_hold = portfolio.compute(weights, initial_value=100.0)
bh_risk = portfolio.risk_metrics(buy_and_hold)
yearly = portfolio.compute(weights, initial_value=100.0, rebalance_every=12)
yearly_fee = portfolio.compute(weights, initial_value=100.0, rebalance_every=12, fee_rate=0.002)
fee_risk = portfolio.risk_metrics(yearly_fee)
for name, run in {"buy and hold": buy_and_hold, "yearly": yearly, "yearly with fee": yearly_fee}.items():
    end = run.paths["portfolio"][:, -1]
    NUMBERS[name] = {q: round(float(np.quantile(end, q)), 1) for q in (0.05, 0.5, 0.95)}
    share = run.paths["us_broad_value"][:, -1] / end
    NUMBERS[name]["median equity share at 30y"] = round(float(np.median(share)), 3)
NUMBERS["risk buy and hold"] = {"drawdown": bh_risk.max_drawdown_percentiles, "vol": bh_risk.annualized_volatility,
                                "cagr": bh_risk.cagr_percentiles}
NUMBERS["risk yearly with fee"] = {"drawdown": fee_risk.max_drawdown_percentiles,
                                   "vol": fee_risk.annualized_volatility, "cagr": fee_risk.cagr_percentiles}
# the end values span 200 to 4,000, so the chart compares them as growth per year, percentile by percentile
levels = {"5th": 0.05, "10th": 0.1, "25th": 0.25, "Median": 0.5, "75th": 0.75, "90th": 0.9, "95th": 0.95}
growth = {name: [(np.quantile(run.paths["portfolio"][:, -1], q) / 100.0) ** (1 / 30) - 1 for q in levels.values()]
          for name, run in {"Rebalanced yearly": yearly, "Buy and hold": buy_and_hold}.items()}
NUMBERS["growth per year"] = {name: [round(float(v), 4) for v in values] for name, values in growth.items()}
charts["portfolio-rebalancing"] = bar(list(levels), growth, xname="Percentile")

rules = [
    portfolio.cashflow_rule(10_000, every_years=1, end_year=14),
    portfolio.cashflow_rule(-40_000, every_years=1, start_year=15),
]
fixed = portfolio.compute(weights, initial_value=100_000.0, rebalance_every=12, cashflow_rules=rules)
fixed_success = portfolio.withdrawal_success(fixed)
indexed = portfolio.compute(weights, initial_value=100_000.0, rebalance_every=12, cashflow_rules=rules,
                            inflation_factor="united_states_inflation")
indexed_success = portfolio.withdrawal_success(indexed)
NUMBERS["plan fixed"] = {"success": fixed_success.success_rate, "depletion": fixed_success.median_depletion_year,
                         "median end": fixed_success.terminal_value_percentiles}
NUMBERS["plan indexed"] = {"success": indexed_success.success_rate, "depletion": indexed_success.median_depletion_year,
                           "median end": indexed_success.terminal_value_percentiles}
steps = [result.step_at(float(year)) for year in range(31)]
left = {name: (run.paths["portfolio"][:, steps] > 0).mean(axis=0)
        for name, run in {"Fixed withdrawals": fixed, "Indexed to inflation": indexed}.items()}
NUMBERS["money left"] = {name: [round(float(v), 3) for v in values] for name, values in left.items()}
charts["portfolio-plan"] = bar(list(range(31)), left, kind="line", xname="Years ahead")

saver = [portfolio.cashflow_rule(10_000, every_years=1)]
saving = portfolio.compute(weights, initial_value=100_000.0, rebalance_every=12, cashflow_rules=saver)
summary = portfolio.summary(saving, inflation_factor="united_states_inflation", real_value_year=20)
step20 = 20 * 12
NUMBERS["saver at 20y"] = {"nominal median": float(np.median(saving.paths["portfolio"][:, step20])),
                           "real": summary.real_value.percentiles if summary.real_value else None}

glide = portfolio.compute_glidepath(
    [
        GlidepathCheckpoint(year=0, weights={"us_broad": 0.9, "united_states_short_rate": 0.1}),
        GlidepathCheckpoint(year=30, weights={"us_broad": 0.3, "united_states_short_rate": 0.7}),
    ],
    initial_value=100.0,
    rebalance_every=12,
)
glide_end = glide.paths["portfolio"][:, -1]
NUMBERS["glidepath"] = {q: round(float(np.quantile(glide_end, q)), 1) for q in (0.05, 0.5, 0.95)}

for key, value in NUMBERS.items():
    print(key, value)
write("portfolio-theory", charts, TITLES)
