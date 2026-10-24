"""Chart and outputs of the KNW Models page (interest-rates/knw.md).

The default factor set holds no KNW pair, so this example calibrates the page's own quarterly configuration: the US
short rate and inflation as a KNW pair with stochastic volatility, and the S&P 500 as its equity leg. It downloads its
history (OECD and the S&P 500 through the Finance Toolkit), so its numbers are those of the day it runs.
"""

from datetime import date

from common import fan, tabs, write
from financescenarios import Scenarios, ScenariosConfig

TITLES = {"knw-run": "US Short Rate, Inflation and Stocks in a KNW Run"}

config = ScenariosConfig.model_validate({
    "start_date": date(2026, 10, 1),
    "engine": {"frequency": "quarterly", "n_simulations": 2000, "n_steps": 120, "seed": 42},
    "toolkit": {"start_date": date(1990, 1, 1)},
    "interest_rates": [{"name": "interest_rate", "source": "oecd", "country": "United States", "term": "short",
                        "period": "quarterly", "method": "knw_sv", "inflation_name": "inflation"}],
    "inflation": [{"name": "inflation", "country": "United States", "period": "quarterly", "method": "knw_sv",
                   "interest_rate_name": "interest_rate"}],
    "equities": [{"name": "equity", "ticker": "^GSPC", "period": "quarterly", "method": "knw_sv",
                  "nominal_rate_name": "interest_rate"}],
})
scenarios = Scenarios.from_config(config)
calibration = scenarios.calibrate(config)
for name in ("interest_rate", "inflation", "equity"):
    print(name, calibration.calibrated_params[name])
result = scenarios.simulate(config, calibration=calibration)
print(result.horizon_summary([1, 10, 30], factors=["interest_rate", "inflation", "equity"]).select(
    "factor", "horizon", "mean", "q0.05", "q0.5", "q0.95"))

charts = {"knw-run": tabs({
    "Short rate": fan(result, {"Short rate": "interest_rate"}, inner=True),
    "Inflation": fan(result, {"Inflation": "inflation"}, inner=True),
    "Stocks": fan(result, {"Stocks": "equity"}, inner=True),
})}
write("knw", charts, TITLES)
