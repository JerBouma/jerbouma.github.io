---
title: "Reporting"
seo_title: "Reporting Reference – Finance Scenarios"
excerpt: "Convert simulated prices into one reporting currency after the simulation."
description: "Convert simulated prices into one reporting currency after the simulation."
author_profile: false
permalink: /projects/financescenarios/docs/reference/reporting
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Convert simulated prices into one reporting currency after the simulation. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.reporting.reporting_controller import Reporting
```

```python
Reporting(scenario_set: ScenarioSet, config: ScenariosConfig)
```

The Reporting module shows simulated prices in one reporting currency: it takes a factor simulated in its own
currency, such as a Japanese equity in yen, and converts every simulated path into, say, US dollars using the
simulated exchange rate of that same path.

An investor who reports in dollars wants to see what a Japanese or European holding is worth in dollars in each
scenario, including the currency gain or loss, not just its local price. Because the exchange rate is simulated
together with the price, the converted result carries the currency risk and its correlation with the asset.
`Reporting` is optional and read-only: it works on a finished simulation, never calibrates or simulates anything,
and never changes the `ScenarioSet` or the config. A run with everything in `USD` behaves exactly as without it.
`Portfolio` uses it to put every holding in the reporting currency before weighting.

Only price-like factors are converted: `equities`, `commodities` and `real_estate`, whose growth rate is first
compounded into a price index. Rates and ratios (`interest_rates`, `inflation`, `credit`, `unemployment`,
`yield_curve`, `dividend_yield`, `leading_indicator`) have no currency to convert: a German short rate of 3% stays
3%, so asking to convert one raises a `ValueError`.

Exchange rates follow the Finance Toolkit's OECD convention (`economics.get_exchange_rates`): units of the national
currency per US dollar. Going from a currency to dollars divides by its simulated rate, going from dollars to a
currency multiplies by it, and two non-dollar currencies are bridged through the dollar in two steps, since every
`fx` factor is quoted against the dollar. Each `fx` entry names its currency in `currency`; when that is unset, it
is read from an `interest_rates` or `inflation` entry for the same `country`, or is `EUR` for the OECD's euro area
codes.

This converts units only. With the default `fx[i].drift_mode: historical` the exchange rate moves independently of
the simulated interest rates; `drift_mode: irp` or `measure: risk_neutral` ties it to the rate gap between the two
currencies through interest rate parity
([Gorvett, 2001](https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf)).

Configuration (`reporting` in a settings profile, beside `engine` and `toolkit`):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `reporting.reporting_currency` | `USD` | The currency `convert()` expresses a level factor in. |

Each level factor's own `currency` field (`equities[i].currency`, `commodities[i].currency`, `real_estate.currency`)
says which currency it is simulated in. The reporting currency has no effect on calibration, simulation or the
correlation matrix.

**References:**

- Gorvett, R.W. (2001). "Foreign Exchange Rate Risk: Institutional Issues and Stochastic Modeling." CAS Discussion Paper Program. <https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf>

## convert

```python
convert(factor_name: str) -> pl.DataFrame
```

Convert one price-like factor's simulated paths into the run's reporting currency, using each path's own
simulated exchange rate.

Ask for a factor by name and get its simulated prices in your reporting currency. A yen-priced equity of 430
when the dollar buys 158.79 yen reads as 430 / 158.79 = 2.71 dollars, and every later value is divided by that
path's exchange rate, so currency swings are part of the outcome. A factor already in the reporting currency
comes back unchanged; `real_estate` is first compounded from a growth rate into a price index.

**Args:**

- <u>factor_name (str):</u> the name of an `equities`, `commodities` or `real_estate` factor in this run.

**Returns:**

<u>pl.DataFrame:</u> a `scenario` column plus one column per date, one row per path, as `ScenarioSet.to_dataframe()`.

**Raises:**

- <u>ValueError:</u> if `factor_name` is not a configured factor with a currency, or is a rate or ratio factor.
- <u>KeyError:</u> if the factor is configured but missing from this `ScenarioSet`.
- <u>RuntimeError:</u> if this run lacks the `fx` entry the conversion needs; the message names its country.

**As an example:**

```python
from datetime import date

from financescenarios import Scenarios
from financescenarios.config.config_model import (
    EngineConfig,
    EquityConfig,
    FXConfig,
    InflationConfig,
    InterestRateConfig,
    ScenariosConfig,
    ToolkitConfig,
)
from financescenarios.reporting.reporting_controller import Reporting

config = ScenariosConfig(
    start_date=date(2026, 10, 1),
    engine=EngineConfig(n_simulations=1000, n_steps=5, frequency="yearly", seed=42),
    toolkit=ToolkitConfig(start_date=date(2005, 1, 1)),
    interest_rates=[InterestRateConfig(name="interest_rate", country="United States", currency="USD")],
    inflation=[
        InflationConfig(name="inflation", country="United States", currency="USD"),
        InflationConfig(name="jp_inflation", country="Japan", currency="JPY"),
    ],
    equities=[
        EquityConfig(name="us_equity", ticker="SPY", currency="USD"),
        EquityConfig(name="jp_equity", ticker="1306.T", currency="JPY"),
    ],
    fx=[FXConfig(name="usd_jpy", country="Japan")],
)
result = Scenarios.from_config(config).simulate()

reporting = Reporting(result, config)
jp_equity_in_usd = reporting.convert("jp_equity")
```

Which returns (calibrated on 2026-10-04), as percentiles across the 1,000 paths next to the median yen price
and yen per dollar:

| date | jp_equity (JPY), median | usd_jpy, median | jp_equity (USD), 5% | median | 95% |
|:-----|------------------------:|----------------:|--------------------:|-------:|----:|
| 2026-10-01 | 430.2 | 158.79 | 2.71 | 2.71 | 2.71 |
| 2027-10-01 | 483.0 | 162.17 | 2.02 | 2.98 | 3.70 |
| 2031-10-01 | 661.8 | 174.18 | 1.79 | 3.78 | 7.12 |

The yen price grows 54% in five years, but the yen weakens to 174 per dollar, so the dollar value grows less.
