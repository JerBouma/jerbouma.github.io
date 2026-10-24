"""Charts and outputs of the Short Rate, Expected Path and Long Rate pages (interest-rates/short-rate.md,
expected-path.md and long-rate.md)."""

import numpy as np

from common import NUMBERS, bar, default_run, fan, labels, runs_fan, tabs, write
from financescenarios import compare_runs, shock_regime

TITLES = {
    "interest-rates-short": "Short Rates of the US, the Euro Area and the UK",
    "interest-rates-long": "10-Year Rates of the US, the Euro Area and the UK",
    "interest-rates-market-path": "The Market's Expected Short-Rate Path",
    "interest-rates-spread": "10-Year Rate minus Short Rate",
    "interest-rates-inversion": "Share of Scenarios with an Inverted Curve",
    "interest-rates-shock": "US Short Rate and Inflation with Inflation at 8% within a Year",
}
COUNTRIES = {"US": "united_states", "Euro area": "eurozone", "UK": "united_kingdom"}
charts = {}

scenarios, calibration, result = default_run()
print(result.describe().filter(result.describe()["category"] == "interest_rates"))

charts["interest-rates-short"] = fan(result, {k: f"{v}_short_rate" for k, v in COUNTRIES.items()})
charts["interest-rates-long"] = fan(result, {k: f"{v}_long_rate" for k, v in COUNTRIES.items()})

for country in COUNTRIES.values():
    short = calibration.calibrated_params[f"{country}_short_rate"]
    long = calibration.calibrated_params[f"{country}_long_rate"]
    print(country, "rule", short.rule, "neutral", short.neutral_real_rate, "target", short.inflation_target,
          "weights", short.inflation_gap_weight, short.unemployment_gap_weight, "u*", short.longer_run_unemployment,
          "floor", short.effective_lower_bound, "speed", round(short.mean_reversion_speed, 4),
          "vol", round(short.volatility, 4), "weights_source", short.weights_source)
    print(country, "long", "term_premium", round(long.term_premium, 4), "speed", round(long.mean_reversion_speed, 4),
          "short_sens", round(long.short_rate_sensitivity, 4), "vol", round(long.volatility, 4),
          "path speed", round(long.short_rate_speed, 4))
    print(calibration.calibration_notes[f"{country}_short_rate"])
    print(calibration.calibration_notes[f"{country}_long_rate"])

# interest-rates-market-path: calibration.calibrated_params[f"{country}_short_rate"].market_path
paths = {k: calibration.calibrated_params[f"{v}_short_rate"].market_path for k, v in COUNTRIES.items()}
times = paths["US"].times
assert all(p.times == times for p in paths.values())
charts["interest-rates-market-path"] = bar([f"{t:g}" for t in times], {k: p.rates for k, p in paths.items()},
                                           kind="line", xname="Years ahead")

spread = {k: result.paths[f"{v}_long_rate"] - result.paths[f"{v}_short_rate"] for k, v in COUNTRIES.items()}
charts["interest-rates-spread"] = fan(result, spread)
inverted = {k: (s < 0).mean(axis=0) for k, s in spread.items()}
charts["interest-rates-inversion"] = bar(labels(result.dates), inverted, kind="line")
for k, s in spread.items():
    NUMBERS[f"spread {k}"] = {"start": float(s[0, 0]), "median 5y": float(np.median(s[:, -1])),
                              "inverted share 1y": float(inverted[k][12]), "inverted share 5y": float(inverted[k][-1])}

regime = shock_regime("inflation", 0.08, calibration=calibration)
shocked = scenarios.simulate(regime=regime, calibration=calibration, n_simulations=2000, seed=42)
print(compare_runs({"baseline": result, "inflation_at_8": shocked}, statistic="terminal_median",
                   factors=["united_states_inflation", "united_states_short_rate", "united_states_long_rate",
                            "united_states_unemployment"]))
for run_name, run in {"baseline": result, "shocked": shocked}.items():
    print(run_name, run.horizon_summary([1, 2, 3, 5], factors=["united_states_inflation", "united_states_short_rate",
                                                                "united_states_long_rate"]).select(
        "factor", "horizon", "q0.05", "q0.5", "q0.95"))
charts["interest-rates-shock"] = tabs({
    "Short rate": runs_fan({"Baseline": result, "Inflation at 8%": shocked}, "united_states_short_rate"),
    "Inflation": runs_fan({"Baseline": result, "Inflation at 8%": shocked}, "united_states_inflation"),
})

write("interest-rates", charts, TITLES)
