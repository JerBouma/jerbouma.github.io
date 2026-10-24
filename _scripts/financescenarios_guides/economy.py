"""Charts and outputs of the Inflation, Unemployment and Business Cycle pages (economy/)."""

import numpy as np

from common import NUMBERS, bar, default_run, fan, labels, write

TITLES = {
    "economy-inflation": "Inflation in the US, the Euro Area and the UK",
    "economy-high-inflation": "Share of Scenarios with Inflation above 5%",
    "economy-unemployment": "Unemployment in the US, the Euro Area and the UK",
    "economy-unemployment-rise": "Share of Scenarios with Unemployment a Point or More above Today's",
    "economy-leading-indicator": "OECD Composite Leading Indicator of the US",
}
COUNTRIES = {"US": "united_states", "Euro area": "eurozone", "UK": "united_kingdom"}
charts = {}

scenarios, calibration, result = default_run()
summary = result.describe()
print(summary.filter(summary["category"].is_in(["inflation", "unemployment", "leading_indicator"])))
print(result.horizon_summary([1, 3, 5], factors=[f"{c}_inflation" for c in COUNTRIES.values()]).select(
    "factor", "horizon", "q0.05", "q0.5", "q0.95"))

for country in COUNTRIES.values():
    p = calibration.calibrated_params[f"{country}_inflation"]
    stay = np.diag(np.asarray(p.transition_matrix))
    print(country, "inflation regimes", np.round(p.regime_means, 4), "vols", np.round(p.regime_volatilities, 4),
          "stay", np.round(stay, 4), "months per spell", np.round(1 / (1 - stay), 1), "persistence",
          round(p.persistence, 3), "anchored_to", p.anchored_to, p.anchored_statistic, "start prob",
          np.round(p.initial_probabilities, 3))

charts["economy-inflation"] = fan(result, {k: f"{v}_inflation" for k, v in COUNTRIES.items()})
above = {k: (result.paths[f"{v}_inflation"] > 0.05).mean(axis=0) for k, v in COUNTRIES.items()}
charts["economy-high-inflation"] = bar(labels(result.dates), above, kind="line")
NUMBERS["above 5%"] = {k: {"1y": float(a[12]), "3y": float(a[36]), "5y": float(a[-1])} for k, a in above.items()}

for country in COUNTRIES.values():
    p = calibration.calibrated_params[f"{country}_unemployment"]
    print(country, "unemployment", "speed", round(p.mean_reversion_speed, 4), "mean", round(p.long_run_mean, 4),
          "inflation_sens", round(p.inflation_sensitivity, 4), "vol", round(p.volatility, 4), "regimes",
          p.regimes and {k: v for k, v in p.regimes.model_dump().items() if "recent" not in k})
print(result.horizon_summary([1, 3, 5], factors=[f"{c}_unemployment" for c in COUNTRIES.values()]).select(
    "factor", "horizon", "q0.05", "q0.5", "q0.95"))
charts["economy-unemployment"] = fan(result, {k: f"{v}_unemployment" for k, v in COUNTRIES.items()})
rise = {k: (result.paths[f"{v}_unemployment"] - result.paths[f"{v}_unemployment"][:, :1] >= 0.01).mean(axis=0)
        for k, v in COUNTRIES.items()}
charts["economy-unemployment-rise"] = bar(labels(result.dates), rise, kind="line")
NUMBERS["unemployment +1pt"] = {k: {"1y": float(a[12]), "3y": float(a[36]), "5y": float(a[-1])} for k, a in rise.items()}

p = calibration.calibrated_params["leading_indicator"]
print("leading indicator", p)
charts["economy-leading-indicator"] = fan(result, {"US leading indicator": "leading_indicator"}, fmt="number",
                                          inner=True)

write("economy", charts, TITLES)
