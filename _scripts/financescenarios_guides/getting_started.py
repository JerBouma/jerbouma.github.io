"""Charts and outputs of the documentation overview (docs.md)."""

import tempfile

import numpy as np

from common import NUMBERS, bar, default_run, fan, hist, labels, tabs, write
from financescenarios import list_presets, read_run

TITLES = {
    "scenarios-overview": "US Short Rate, Inflation and Stock Market Return",
    "scenarios-equity-distribution": "Five-Year Annualized Return of US Stocks",
    "scenarios-paths": "US Short Rate in Five Scenarios",
    "scenarios-horizons": "Percentiles of the US Stock Market Return after One, Three and Five Years",
}

print(list_presets(kind="settings").select("id", "description"))
print(list_presets(kind="factor-sets").select("id", "description"))

scenarios, calibration, result = default_run()
print(result.describe())

charts = {}
# scenarios-overview: result.plot(["united_states_short_rate", "united_states_inflation", "us_broad"])
charts["scenarios-overview"] = tabs({
    "Short rate": fan(result, {"US short rate": "united_states_short_rate"}, inner=True),
    "Inflation": fan(result, {"US inflation": "united_states_inflation"}, inner=True),
    "US stocks": fan(result, {"US stocks, annualized return": "us_broad"}, inner=True),
})

summary = result.summary_statistics("united_states_short_rate")
print(summary.tail(3))
horizons = result.horizon_summary([1, 3, 5], factors=["us_broad", "united_states_inflation"])
print(horizons)

# scenarios-horizons: the us_broad rows of horizon_summary([1, 3, 5])
stocks = horizons.filter(horizons["factor"] == "us_broad")
charts["scenarios-horizons"] = bar(
    [f"{int(h)} year" + ("s" if h > 1 else "") for h in stocks["horizon"]],
    {"5th percentile": stocks["q0.05"], "Median": stocks["q0.5"], "95th percentile": stocks["q0.95"]},
)

# scenarios-equity-distribution: result.plot("us_broad", kind="distribution")
five_year = result.metric_paths("us_broad")[:, -1]
charts["scenarios-equity-distribution"] = hist(
    five_year, width=0.01, xname="Five-year annualized return of US stocks",
    markers={"5th percentile": np.quantile(five_year, 0.05), "Median": np.median(five_year),
             "95th percentile": np.quantile(five_year, 0.95)},
)
NUMBERS["us_broad five-year"] = {"q05": np.quantile(five_year, 0.05), "median": np.median(five_year),
                                 "q95": np.quantile(five_year, 0.95), "share below 0": float((five_year < 0).mean())}

paths = result.to_dataframe("united_states_short_rate")
print(paths.select(paths.columns[:6]).head())
# scenarios-paths: the first five rows of result.to_dataframe("united_states_short_rate")
charts["scenarios-paths"] = bar(
    labels(result.dates),
    {f"Scenario {i}": paths.row(i)[1:] for i in range(5)}, kind="line",
)

print(scenarios.validate(result))
print(result.diagnose())

with tempfile.TemporaryDirectory() as folder:
    path = scenarios.save(result, folder)
    reloaded = read_run(path)
    same = all(np.array_equal(reloaded.paths[name], result.paths[name]) for name in result.factor_names)
    print(path.name, reloaded.n_simulations, len(reloaded.factor_names), same)

write("getting-started", charts, TITLES)
