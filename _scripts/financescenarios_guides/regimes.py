"""Charts and outputs of the Regimes Getting Started (regimes.md). Regimes with targets draw extra scenarios: run it
under the heavy-job lock."""

import resource

from common import NUMBERS, default_run, runs_fan, tabs, write
from financescenarios import compare_runs, list_presets, load_regime, search_regimes

TITLES = {
    "regimes-soft-landing": "US Inflation in the Baseline and under Soft Landing",
    "regimes-financial-crisis": "US Stocks, Unemployment and Short Rate under Financial Crisis",
    "regimes-inflation": "US Inflation under Oil Shock, Oil Crisis and Climate Collapse",
    "regimes-fed": "US Unemployment, Stocks and Rates under the Fed's Severely Adverse Scenario",
}
charts = {}

presets = list_presets(kind="regimes")
print(presets.height, presets.columns)
print(search_regimes("high inflation").head(5))

scenarios, calibration, result = default_run()
print(load_regime("oil_crisis"))

soft_landing = scenarios.simulate(regime="soft_landing", n_simulations=2000, seed=42, calibration=calibration)
print(compare_runs({"baseline": result, "soft_landing": soft_landing},
                   factors=["united_states_inflation", "united_states_short_rate", "us_broad"]))
charts["regimes-soft-landing"] = runs_fan({"Baseline": result, "Soft Landing": soft_landing},
                                          "united_states_inflation")

financial_crisis = scenarios.simulate(regime="financial_crisis", n_simulations=2000, seed=42, calibration=calibration)
print(compare_runs({"baseline": result, "financial_crisis": financial_crisis},
                   factors=["us_broad", "united_states_unemployment", "united_states_short_rate",
                            "united_states_inflation"]))
print("rss MB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
crisis_runs = {"Baseline": result, "Financial Crisis": financial_crisis}
charts["regimes-financial-crisis"] = tabs({
    "US stocks": runs_fan(crisis_runs, "us_broad"),
    "Unemployment": runs_fan(crisis_runs, "united_states_unemployment"),
    "Short rate": runs_fan(crisis_runs, "united_states_short_rate"),
})

runs = {"baseline": result}
for regime in ("oil_shock", "oil_crisis", "climate_collapse"):
    runs[regime] = scenarios.simulate(regime=regime, n_simulations=2000, seed=42, calibration=calibration)
print(compare_runs(runs, factors=["united_states_inflation", "united_states_short_rate", "us_broad",
                                  "united_states_unemployment"]))
print(runs["oil_crisis"].horizon_summary([1, 3, 5], factors=["united_states_inflation", "united_states_short_rate"]))
print(runs["oil_shock"].horizon_summary([1, 2, 3, 5], factors=["united_states_inflation"]))
print("rss MB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
charts["regimes-inflation"] = runs_fan(
    {"Baseline": runs["baseline"], "Oil Shock": runs["oil_shock"], "Oil Crisis": runs["oil_crisis"],
     "Climate Collapse": runs["climate_collapse"]}, "united_states_inflation")

fed = scenarios.simulate(regime="fed_severely_adverse_2026", n_simulations=2000, seed=42, calibration=calibration)
print(compare_runs({"baseline": result, "fed_severely_adverse_2026": fed}, statistic="terminal_median",
                   factors=["united_states_unemployment", "us_broad", "united_states_short_rate",
                            "united_states_long_rate", "real_estate"]))
for name, run in {"baseline": result, "fed": fed}.items():
    print(name, run.horizon_summary([0.5, 1, 2, 3], factors=["united_states_unemployment", "us_broad",
                                                            "united_states_short_rate", "united_states_long_rate"]
                                    ).select("factor", "horizon", "q0.05", "q0.5", "q0.95"))
fed_runs = {"Baseline": result, "Fed Severely Adverse 2026": fed}
charts["regimes-fed"] = tabs({
    "Unemployment": runs_fan(fed_runs, "united_states_unemployment"),
    "US stocks": runs_fan(fed_runs, "us_broad"),
    "Short rate": runs_fan(fed_runs, "united_states_short_rate"),
    "10-year rate": runs_fan(fed_runs, "united_states_long_rate"),
})
print("rss MB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
NUMBERS["done"] = True
write("regimes", charts, TITLES)
