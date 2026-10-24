"""Charts and outputs of the Configuration and Beliefs pages (configuration/configuration.md and beliefs.md)."""

import sys

import numpy as np

from common import NUMBERS, bar, default_run, fan, runs_fan, write
from financescenarios import BeliefPath, OUBeliefs, Shock, compare_runs, load_profiles

TITLES = {
    "configuration-factor-sets": "Variables per Category in the Default and Broad Factor Sets",
    "configuration-thirty-years": "US Short Rate, Long Rate and Inflation over Thirty Years",
    "configuration-seeds": "Mean Five-Year Return of US Stocks per Seed",
    "configuration-belief": "US Inflation with and without a Belief Path",
}
charts = {}

# configuration-factor-sets: load_profiles(...).describe() for both factor sets
config = load_profiles(settings_id="default", factor_set_id="default")
print(config.start_date, config.engine.n_simulations, config.engine.n_steps, config.engine.frequency, config.toolkit.start_date)
default_sets = config.describe()
print(default_sets)
broad = load_profiles(settings_id="default", factor_set_id="broad")
broad_sets = broad.describe()
print(broad_sets)
categories = sorted(set(broad_sets["category"]) | set(default_sets["category"]))
count = lambda frame: [dict(zip(frame["category"], frame["n_factors"])).get(c, 0) for c in categories]
charts["configuration-factor-sets"] = bar(
    [c.replace("_", " ").capitalize() for c in categories],
    {"Default": count(default_sets), "Broad": count(broad_sets)}, fmt="amount",
)
NUMBERS["factors"] = {"default": int(default_sets["n_factors"].sum()), "broad": int(broad_sets["n_factors"].sum())}

scenarios, calibration, result = default_run()

# configuration-thirty-years: scenarios.simulate(calibration=calibration, years=30, n_simulations=1000, seed=42)
long_run = scenarios.simulate(calibration=calibration, years=30, n_simulations=1000, seed=42)
print(long_run.horizon_summary([5, 10, 30], factors=["united_states_short_rate", "united_states_long_rate",
                                                      "united_states_inflation"]))
charts["configuration-thirty-years"] = fan(long_run, {
    "US short rate": "united_states_short_rate",
    "US 10-year rate": "united_states_long_rate",
    "US inflation": "united_states_inflation",
})

# configuration-seeds: the five-year mean of us_broad for seeds 1 to 5 at 500 and 2,000 scenarios
means = {500: [], 2000: []}
for n in means:
    for seed in range(1, 6):
        run = scenarios.simulate(calibration=calibration, n_simulations=n, seed=seed)
        stats = run.summary_statistics("us_broad").tail(1)
        means[n].append(stats["mean"][0])
        NUMBERS[f"seed {seed} n {n}"] = {"mean": stats["mean"][0], "se": stats["se"][0]}
charts["configuration-seeds"] = bar(
    [f"Seed {s}" for s in range(1, 6)], {"500 scenarios": means[500], "2,000 scenarios": means[2000]},
)

# configuration-belief: a long-run path and a shock on US inflation, on the same calibration
beliefs = OUBeliefs(
    long_run_mean=BeliefPath(anchors={2.0: 0.04, 5.0: 0.02}),
    shocks=[Shock(year=1.0, magnitude=0.02)],
)
us_inflation = config.inflation[0].model_copy(update={"beliefs": beliefs})
believed = config.model_copy(update={"inflation": [us_inflation, *config.inflation[1:]]})
with_belief = scenarios.simulate(believed, calibration=calibration, n_simulations=2000, seed=42)
print(compare_runs({"fitted": result, "belief": with_belief}, statistic="terminal_median",
                   factors=["united_states_inflation", "united_states_short_rate", "us_broad"]))
print(with_belief.horizon_summary([1, 2, 3, 5], factors=["united_states_inflation"]))
print(result.horizon_summary([1, 2, 3, 5], factors=["united_states_inflation"]))
charts["configuration-belief"] = runs_fan({"Fitted": result, "Belief path": with_belief}, "united_states_inflation")

if "--live" in sys.argv:  # a configuration in code: calibrates live on the day it runs
    from datetime import date

    from financescenarios import Scenarios, ScenariosConfig
    from financescenarios.config.config_model import (
        EngineConfig, EquityConfig, InflationConfig, InterestRateConfig, ToolkitConfig,
    )

    small_config = ScenariosConfig(
        start_date=date(2026, 1, 1),
        toolkit=ToolkitConfig(start_date=date(1990, 1, 1)),
        interest_rates=[InterestRateConfig(name="us_short_rate", country="United States", currency="USD")],
        inflation=[InflationConfig(name="inflation", country="United States", currency="USD")],
        equities=[EquityConfig(name="us_broad", ticker="SPY", currency="USD")],
        engine=EngineConfig(n_simulations=500, n_steps=120, frequency="monthly", seed=42),
    )
    small_result = Scenarios.from_config(small_config).simulate()
    print(small_result.describe())

write("configuration", charts, TITLES)
