"""Chart and outputs of the Credit page (markets/credit.md).

The default factor set leaves credit off, so this example calibrates a small yearly configuration of its own with
the S&P credit cycle switched on. It downloads its history (OECD, ESMA's CEREP rating statistics and the S&P 500
through the Finance Toolkit), so its numbers are those of the day it runs; CEREP answers slowly.
"""

from datetime import date

import numpy as np

from common import NUMBERS, bar, write
from financescenarios import Scenarios, ScenariosConfig, rating_migration

TITLES = {"credit-defaults": "Cumulative Default Loss of a Bond Portfolio by Year"}

config = ScenariosConfig.model_validate({
    "start_date": date(2026, 1, 1),
    "engine": {"n_simulations": 2000, "n_steps": 10, "frequency": "yearly", "seed": 42},
    "toolkit": {"start_date": date(2000, 1, 1)},
    "interest_rates": [{"name": "us_short_rate", "country": "United States", "currency": "USD", "source": "oecd",
                        "period": "yearly"}],
    "inflation": [{"name": "inflation", "country": "United States", "currency": "USD", "period": "yearly"}],
    "equities": [{"name": "us_stocks", "ticker": "^GSPC", "currency": "USD", "period": "yearly"}],
    "credit_migration": {"enabled": True, "agency": "S&P"},
})
scenarios = Scenarios.from_config(config)
calibration = scenarios.calibrate(config)
cycle = [v for k, v in calibration.calibrated_params.items() if "credit" in k]
for params in cycle:
    print({k: v for k, v in params.model_dump().items() if k != "transition_matrix"})
    print("ratings", params.ratings)
    print(np.round(np.asarray(params.transition_matrix), 4))
result = scenarios.simulate(config, calibration=calibration)

migration = rating_migration(result, {"A": 40, "BBB": 50, "BB": 10}, recovery_rate=0.4)
summary = migration.summary()
print(summary)
loss = np.asarray(migration.loss)[:, 1:] / 100  # per 100 invested, as a share; year 0 holds no loss
years = list(range(1, loss.shape[1] + 1))
print("loss shape", loss.shape)
q = {name: np.quantile(loss, level, axis=0) for name, level in
     {"Median": 0.5, "95th percentile": 0.95, "99.5th percentile": 0.995}.items()}
for name, values in q.items():
    NUMBERS[name] = [round(float(v), 4) for v in values]
NUMBERS["mean"] = [round(float(v), 4) for v in loss.mean(axis=0)]
print(NUMBERS)
charts = {"credit-defaults": bar([str(y) for y in years], q, fmt="percent", xname="Years ahead")}
write("credit", charts, TITLES)
