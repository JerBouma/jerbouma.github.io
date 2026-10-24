"""Charts and outputs of the Yield Curve page (interest-rates/yield-curve.md)."""

import numpy as np

from common import NUMBERS, bar, default_run, quantiles, write
from financescenarios.factors.term_structure.term_structure_model import nelson_siegel_yield

TITLES = {
    "yield-curve-median": "Median Treasury Curve Today, after One Year and after Five Years",
    "yield-curve-five-years": "Treasury Curve after Five Years",
}
TENORS = [0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30]
charts = {}

scenarios, calibration, result = default_run()
decay = scenarios.config.yield_curve.decay
print("decay", decay)
for factor in ("rate_level", "rate_slope", "rate_curvature"):
    params = calibration.calibrated_params[factor]
    print(factor, params)
print(result.describe().filter(result.describe()["category"] == "yield_curve"))

curves = {
    tenor: nelson_siegel_yield(
        result.paths["rate_level"], result.paths["rate_slope"], result.paths["rate_curvature"], tenor=tenor, decay=decay
    )
    for tenor in TENORS
}
steps = {"Today": 0, "After one year": 12, "After five years": result.paths["rate_level"].shape[1] - 1}
medians = {name: [float(np.median(curves[t][:, step])) for t in TENORS] for name, step in steps.items()}
x = [f"{t:g}" for t in TENORS]
charts["yield-curve-median"] = bar(x, medians, kind="line", xname="Maturity (years)")

last = steps["After five years"]
bands = [quantiles(curves[t][:, last:last + 1], inner=True) for t in TENORS]
charts["yield-curve-five-years"] = {
    "type": "fan", "x": x, "xname": "Maturity (years)", "format": "percent",
    "series": [{"name": "After five years", **{k: [b[k][0] for b in bands] for k in bands[0]}}],
}

for name, values in medians.items():
    NUMBERS[name] = dict(zip(x, [round(v, 4) for v in values]))
inverted = (curves[10] < curves[0.25]).mean(axis=0)
NUMBERS["share 10y below 3m"] = {"1y": float(inverted[12]), "5y": float(inverted[-1])}
ten_year = np.quantile(curves[10][:, -1], [0.05, 0.5, 0.95])
NUMBERS["10y five years"] = {k: round(float(v), 4) for k, v in zip(["q05", "q50", "q95"], ten_year)}
print(NUMBERS)

write("yield-curve", charts, TITLES)
