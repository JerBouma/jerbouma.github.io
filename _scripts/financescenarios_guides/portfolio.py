"""Charts and outputs of the Portfolio Getting Started (portfolio.md). With --live the backtest downloads the history;
without it, it replays the README's saved history (docs/assets/readme/backtest_history), which gives the same values."""

import sys

import numpy as np

from common import NUMBERS, REPO, bar, default_run, fan, hist, labels, runs_fan, write
from financescenarios import GlidepathCheckpoint, Portfolio, list_presets, read_run

TITLES = {
    "portfolio-value": "Value of 100,000 in a 60/40 Portfolio",
    "portfolio-end-values": "Value of the 60/40 Portfolio after Five Years",
    "portfolio-drawdown": "Deepest Fall from a Peak of the 60/40 Portfolio within Five Years",
    "portfolio-withdrawals": "Portfolio Value with Withdrawals Fixed and Indexed to Inflation",
    "portfolio-glidepath": "Median Value per Holding along the Glidepath",
    "portfolio-backtest": "Value of 100,000 in Three Mixes since 2000",
    "portfolio-exposure": "Fama-French Factor Loadings of Three Mixes",
}
charts = {}

print(list_presets(kind="portfolios").select("id", "description"))
scenarios, calibration, result = default_run()

portfolio = Portfolio.from_preset(result, preset="balanced_60_40")
values = portfolio.compute(initial_value=100_000, rebalance_every=12)
print(values.describe())
print(values.describe(levels=True))
charts["portfolio-value"] = fan(values, {"60/40 portfolio": "portfolio"}, fmt="amount", levels=True, inner=True)

risk = portfolio.risk_metrics()
print(risk)
end = values.paths["portfolio"][:, -1]
NUMBERS["end value"] = {"mean": end.mean(), "median": np.median(end), "q05": np.quantile(end, 0.05),
                        "q95": np.quantile(end, 0.95), "below 100k": float((end < 100_000).mean())}

summary = portfolio.summary(goal_value=150_000)
print(summary.goal_probability)
charts["portfolio-end-values"] = hist(
    end, width=5_000, xname="Value after five years", fmt="amount",
    markers={"Goal": 150_000, "Median": np.median(end), "5th percentile": np.quantile(end, 0.05)},
)
drawdowns = risk.max_drawdown_percentiles
charts["portfolio-drawdown"] = bar(
    [f"{k}th percentile" if k != "50" else "Median" for k in drawdowns], {"Deepest fall": list(drawdowns.values())},
)

custom = portfolio.compute(
    {"us_broad": 0.5, "united_states_long_rate": 0.3, "gold": 0.2},
    initial_value=100_000,
    durations={"united_states_long_rate": 5.4},
    fee_rate=0.002,
    rebalance_band=0.05,
)
print(custom.describe())
print(portfolio.weight_drift_summary())

plan = [
    portfolio.cashflow_rule(5_000, every_years=1, start_year=0, end_year=1),
    portfolio.cashflow_rule(-30_000, every_years=1, start_year=2),
]
funded = portfolio.compute(initial_value=100_000, rebalance_every=12, cashflow_rules=plan)
success = portfolio.withdrawal_success()
print("lasts", success.success_rate, "median end", success.terminal_value_percentiles["50"], "depletion",
      success.median_depletion_year)
indexed = portfolio.compute(initial_value=100_000, rebalance_every=12, cashflow_rules=plan,
                            inflation_factor="united_states_inflation")
success_indexed = portfolio.withdrawal_success()
print("indexed lasts", success_indexed.success_rate, "median end", success_indexed.terminal_value_percentiles["50"],
      "depletion", success_indexed.median_depletion_year)
charts["portfolio-withdrawals"] = runs_fan({"Fixed withdrawals": funded, "Indexed to inflation": indexed},
                                           "portfolio", fmt="amount", levels=True)

checkpoints = [
    GlidepathCheckpoint(year=0, weights={"us_broad": 0.9, "united_states_long_rate": 0.1}),
    GlidepathCheckpoint(year=5, weights={"us_broad": 0.4, "united_states_long_rate": 0.6}),
]
glidepath = portfolio.compute_glidepath(
    checkpoints, initial_value=100_000, rebalance_every=1, durations={"united_states_long_rate": 5.4}
)
print(glidepath.describe(levels=True))
charts["portfolio-glidepath"] = bar(
    labels(glidepath.dates),
    {"US stocks": np.median(glidepath.paths["us_broad_value"], axis=0),
     "US Treasuries": np.median(glidepath.paths["united_states_long_rate_value"], axis=0)},
    fmt="amount", kind="line", stack=True,
)

mixes = ["balanced_60_40", "all_weather", "permanent_portfolio"]
if "--live" in sys.argv:
    backtest = Portfolio.backtest(scenarios, mixes)
else:  # the README's saved history of the same call
    backtest = Portfolio.from_preset(read_run(REPO / "docs/assets/readme/backtest_history"), preset=mixes)
history = backtest.compute(initial_value=100_000, rebalance_every=12)
print(history.factor_names, history.dates[0], history.dates[-1], len(history.dates))
series = {name: history.paths[name][0] for name in history.factor_names}  # one path per mix: the history
print({k: v[-1] for k, v in series.items()})
charts["portfolio-backtest"] = bar(labels(history.dates), series, fmt="amount", kind="line")
exposure = backtest.factor_exposure()
print(exposure)
loadings = ["Mkt-RF", "SMB", "HML", "RMW", "CMA"]
charts["portfolio-exposure"] = bar(loadings, {row["portfolio"]: [row[k] for k in loadings]
                                              for row in exposure.iter_rows(named=True)}, fmt="ratio")

stocks_only = backtest.compute({"us_broad": 1.0}, initial_value=100_000, rebalance_every=12)
print(backtest.factor_exposure(stocks_only).select("Mkt-RF", "r_squared"))
print(backtest.benchmark(history, stocks_only, benchmark_weights={"us_broad": 1.0}))
print({k: v for k, v in backtest.risk_metrics(history).items()} if isinstance(backtest.risk_metrics(history), dict)
      else backtest.risk_metrics(history))

write("portfolio", charts, TITLES)
