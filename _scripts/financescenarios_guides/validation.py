"""Charts and outputs of the Validation Getting Started (validation.md). Downloads history and refits the model as of
past dates: run it under the heavy-job lock."""

import time

import polars as pl

from common import NUMBERS, bar, default_run, labels, tabs, values, write

TITLES = {
    "validation-relationships": "US Macro Relationships in History and in the Scenarios",
    "validation-crisis": "Scenarios from the End of 2007 against What Happened",
    "validation-pandemic": "Scenarios from the End of 2019 against What Happened",
    "validation-coverage": "Share of Years inside the 90% Band, Five Origins from 2003 to 2019",
}
FACTORS = ["us_broad", "united_states_unemployment", "united_states_short_rate", "united_states_long_rate",
           "united_states_inflation", "united_kingdom_inflation"]
NAMES = {"us_broad": "US stocks", "united_states_unemployment": "US unemployment",
         "united_states_short_rate": "US short rate", "united_states_long_rate": "US 10-year rate",
         "united_states_inflation": "US inflation", "united_kingdom_inflation": "UK inflation"}
charts = {}
pl.Config.set_tbl_rows(40)
pl.Config.set_fmt_str_lengths(80)
t = time.time()

scenarios, calibration, _ = default_run()
result = scenarios.simulate(calibration=calibration, n_simulations=1000, years=30, seed=42)

relationships = scenarios.check_relationships(result)
print(relationships.select("relationship", "region", "status", "history", "simulated_median"))
print(relationships["status"].value_counts())
us = relationships.filter(pl.col("region") == "United States")
charts["validation-relationships"] = bar(
    list(us["relationship"]), {"History": us["history"], "Scenarios (median)": us["simulated_median"]},
    fmt="ratio",
)

realism = scenarios.check_realism(result, summary=True)
print(realism)
print(realism.columns)
parameters = scenarios.check_parameters(result, flagged_only=True)
print(parameters)
print("checks", round(time.time() - t))


def fan_against_history(run, factors):
    """One tab per factor: the 5th, 50th and 95th percentile at each year end and what happened."""
    out = {}
    for factor in factors:
        rows = run.table.filter(pl.col("factor") == factor).sort("date")
        spec = bar(labels(rows["date"]), {"5th percentile": rows["p5"], "Median": rows["p50"],
                                          "95th percentile": rows["p95"], "What happened": rows["realized"]},
                   kind="line", fmt="percent")
        spec["series"][0]["dashed"] = spec["series"][2]["dashed"] = True
        out[NAMES[factor]] = spec
    return tabs(out)


crisis = scenarios.out_of_sample(as_of="2007-12-31", years=5, n_simulations=1000, seed=42, factors=FACTORS)
print(crisis.table.select("factor", "date", "realized", "p5", "p50", "p95", "pit"))
print(crisis.scores.select("factor", "coverage_50", "coverage_90", "pit_mean", "crps_skill"))
for note in crisis.notes:
    if note.startswith("united_states_short_rate:"):
        print(note)
charts["validation-crisis"] = fan_against_history(crisis, FACTORS)
print("crisis", round(time.time() - t))

pandemic = scenarios.out_of_sample(as_of="2019-12-31", years=5, n_simulations=1000, seed=42, factors=FACTORS)
print(pandemic.table.select("factor", "date", "realized", "p5", "p50", "p95", "pit"))
print(pandemic.scores.select("factor", "coverage_50", "coverage_90", "pit_mean", "crps_skill"))
charts["validation-pandemic"] = fan_against_history(pandemic, FACTORS)
print("pandemic", round(time.time() - t))

evaluation = scenarios.out_of_sample_many(
    origins=["2003-12-31", "2007-12-31", "2011-12-31", "2015-12-31", "2019-12-31"],
    years=4,
    n_simulations=1000,
    seed=42,
)
print(evaluation.scores.columns)
print(evaluation.scores.select("factor", "origins", "coverage_50", "coverage_90", "pit_mean", "crps_skill"))
scores = evaluation.scores.sort("factor")
charts["validation-coverage"] = bar(
    list(scores["factor"]), {"Inside the 90% band": scores["coverage_90"],
                             "Expected": [0.9] * scores.height}, fmt="percent",
)
charts["validation-coverage"]["series"][1].update(reference=True)
NUMBERS["seconds"] = round(time.time() - t)
write("validation", charts, TITLES)
