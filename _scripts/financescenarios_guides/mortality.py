"""Chart and outputs of the Mortality page (economy/mortality.md).

The default factor set leaves mortality off, so this example calibrates a small yearly configuration of its own with
German mortality from Eurostat switched on. It downloads its history (OECD, Eurostat and the S&P 500 through the
Finance Toolkit), so its numbers are those of the day it runs.
"""

from datetime import date

import numpy as np

from common import NUMBERS, fan, labels, tabs, write
from financescenarios import Scenarios, ScenariosConfig
from financescenarios.factors.mortality.mortality_model import cbd_mortality_rate

TITLES = {"mortality-death-probability": "One-Year Death Probability in Germany at 65 and 80"}

config = ScenariosConfig.model_validate({
    "start_date": date(2026, 1, 1),
    "engine": {"n_simulations": 2000, "n_steps": 30, "frequency": "yearly", "seed": 42},
    "toolkit": {"start_date": date(1985, 1, 1)},
    "interest_rates": [{"name": "us_short_rate", "country": "United States", "currency": "USD", "source": "oecd",
                        "period": "yearly"}],
    "inflation": [{"name": "inflation", "country": "United States", "currency": "USD", "period": "yearly"}],
    "equities": [{"name": "us_stocks", "ticker": "^GSPC", "currency": "USD", "period": "yearly"}],
    "mortality": {"enabled": True, "source": "eurostat", "country": "Germany"},
})
scenarios = Scenarios.from_config(config)
calibration = scenarios.calibrate(config)
for factor in ("mortality_level", "mortality_slope"):
    print(factor, calibration.calibrated_params[factor])
result = scenarios.simulate(config, calibration=calibration)
print(result.describe())
corr = result.simulated_correlation()
print(corr)

mean_age = (config.mortality.min_age + config.mortality.max_age) / 2
death = {}
for age in (65, 80):
    q = cbd_mortality_rate(result.paths["mortality_level"], result.paths["mortality_slope"], age, mean_age)
    death[age] = q
    NUMBERS[f"q{age}"] = {"today": float(q[0, 0]), **{
        f"{year}y": [round(float(v), 5) for v in np.quantile(q[:, year], [0.05, 0.5, 0.95])] for year in (10, 30)}}
print(NUMBERS)


def band(q):
    quantile = np.nanquantile(q, [0.05, 0.25, 0.5, 0.75, 0.95], axis=0)
    keys = ("q05", "q25", "q5", "q75", "q95")
    return {key: [round(float(v), 6) for v in row] for key, row in zip(keys, quantile)}


charts = {"mortality-death-probability": tabs({
    f"Age {age}": {"type": "fan", "x": labels(result.dates), "format": "percent",
                   "series": [{"name": f"Age {age}", **band(q)}]}
    for age, q in death.items()
})}
write("mortality", charts, TITLES)
