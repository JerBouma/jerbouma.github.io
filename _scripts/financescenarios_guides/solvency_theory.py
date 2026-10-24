"""Numbers of the Solvency pages beyond the charts (solvency/market-consistency.md, solvency/capital.md): the martingale
test in detail, the bond prices the risk-neutral run implies against EIOPA's curve, a level and an inflation-indexed
annuity on the risk-neutral run, the own funds behind the report, and the SCR across seeds.

Reads EIOPA's curve through the Finance Toolkit (no API key)."""

import numpy as np

from common import CALIBRATION, CALIBRATION_RISK_NEUTRAL, default_run
from financescenarios import (
    CalibrationResult, Portfolio, Scenarios, Solvency, best_estimate, build_toolkit, eiopa_risk_free_curve,
    martingale_test,
)
from financescenarios.config.config_model import risk_neutral_config

scenarios, calibration, result = default_run()
market = Scenarios.from_config(risk_neutral_config(scenarios.config))
risk_neutral = market.simulate(
    n_simulations=2000, seed=42, calibration=CalibrationResult.load(CALIBRATION_RISK_NEUTRAL)
)

test = martingale_test(risk_neutral, asset="us_broad", short_rate="united_states_short_rate", dividend_yield=0.0099)
table = test.table
print("martingale", test.passed, "pass rate", test.pass_rate, "max dev", test.max_abs_deviation, "rows", len(table))
print(table.columns)
print(table.head(3))
print(table.tail(3))

deflator = risk_neutral.discount_factor_paths("united_states_short_rate")
years = [1, 2, 3, 4, 5]
prices = {y: float(deflator[:, risk_neutral.step_at(float(y))].mean()) for y in years}
se = {y: float(deflator[:, risk_neutral.step_at(float(y))].std(ddof=1) / np.sqrt(deflator.shape[0])) for y in years}
print("model bond prices", prices, "se", se)
toolkit = build_toolkit(scenarios.config)
curve = eiopa_risk_free_curve(toolkit, country="United States")
print("eiopa curve head", curve.head(12) if hasattr(curve, "head") else curve)

grid = risk_neutral.time_grid
annuity = np.zeros(len(grid))
for y in years:
    annuity[risk_neutral.step_at(float(y))] = 10_000.0
level = best_estimate(risk_neutral, annuity, short_rate="united_states_short_rate")
index = risk_neutral.cumulative_index("united_states_inflation", initial_index=1.0).drop("scenario").to_numpy()
indexed = best_estimate(risk_neutral, annuity * index, short_rate="united_states_short_rate")
print("level", level)
print("indexed", indexed)

assets = Portfolio.from_preset(result, preset="balanced_60_40").compute(initial_value=60_000, rebalance_every=12)
solvency = Solvency(real_world=result, risk_neutral=risk_neutral)
report = solvency.report(cashflows=[10_000] * 5, assets=assets)
print(report)
own_funds = solvency._own_funds([10_000] * 5, assets)
print("own funds today", float(own_funds[:, 0].mean()), "assets today", float(assets.paths["portfolio"][:, 0].mean()))

for seed in (1, 2, 3, 4):
    run = scenarios.simulate(n_simulations=2000, seed=seed, calibration=CalibrationResult.load(CALIBRATION))
    run_assets = Portfolio.from_preset(run, preset="balanced_60_40").compute(initial_value=60_000, rebalance_every=12)
    rep = Solvency(real_world=run, risk_neutral=risk_neutral).report(cashflows=[10_000] * 5, assets=run_assets)
    print("seed", seed, [r for r in rep.iter_rows()][3:5])
