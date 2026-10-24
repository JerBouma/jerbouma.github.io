"""Charts and outputs of the published-model examples on Other Rate Models and Dividends.

The ahlgrim, hibbert and wilkie factor sets run their papers' models with the papers' own parameters and read no
data, so these runs need no calibration and no API key.
"""

import numpy as np

from common import NUMBERS, fan, tabs, write
from financescenarios import Scenarios

TITLES = {
    "other-models-rates": "Two-Factor Short Rates and Wilkie's Consols Yield",
    "dividends-wilkie": "Dividend Yield and Dividend Growth in Wilkie's Model",
}
charts = {}
runs = {name: Scenarios.from_profiles(settings=name, factor_set=name).simulate(seed=42) for name in
        ("ahlgrim", "hibbert", "wilkie")}
for name, run in runs.items():
    print(name, run.paths[next(iter(run.paths))].shape)
    print(run.describe())
    print(run.horizon_summary([1, 10, 30], factors=list(run.paths)).select("factor", "horizon", "mean", "q0.05",
                                                                            "q0.5", "q0.95"))

ahlgrim, hibbert, wilkie = runs["ahlgrim"], runs["hibbert"], runs["wilkie"]
charts["other-models-rates"] = tabs({
    "Hibbert, Mowbray and Turnbull": fan(hibbert, {"Nominal short rate": "short_rate"}, inner=True),
    "Ahlgrim, D'Arcy and Gorvett": fan(ahlgrim, {"Nominal short rate": "interest_rate"}, inner=True),
    "Wilkie": fan(wilkie, {"Consols yield": "consols_rate"}, inner=True),
})
charts["dividends-wilkie"] = tabs({
    "Dividend yield": fan(wilkie, {"Dividend yield": "dividend_yield"}, inner=True),
    "Dividend growth": fan(wilkie, {"Dividend growth": "dividend_growth"}, inner=True),
})

for name, factor in {"ahlgrim": "interest_rate", "hibbert": "short_rate", "wilkie": "consols_rate"}.items():
    paths = runs[name].metric_paths(factor)
    NUMBERS[f"{name} {factor}"] = {
        "share below 0 at end": float((paths[:, -1] < 0).mean()),
        "min": float(paths.min()),
        "q05 end": float(np.quantile(paths[:, -1], 0.05)),
    }
print(NUMBERS)

write("published-models", charts, TITLES)
