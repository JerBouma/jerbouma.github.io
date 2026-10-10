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

The Reporting module expresses simulated prices in one reporting currency: it takes a
factor that was simulated in its own currency, such as a Japanese equity in yen, and
converts every simulated path into, say, US dollars using the simulated exchange rate
of that same path.

In plain terms: an investor who reports in dollars wants to see what a Japanese or
European holding is worth in dollars in each scenario, including the currency gain or
loss, not just its local price. `Reporting` gives that converted view after the
simulation has run. It is entirely optional and read-only: it never calibrates or
simulates anything, never changes the `ScenarioSet` or the config, and leaves the
correlation structure alone. Every single-currency run (the default: everything in
`USD`, `fx: []`) behaves exactly as without it. `Portfolio` uses it to put every
holding in the reporting currency before weighting.

The module is built around the split between level factors and rate factors
(`reporting_model.LEVEL_FACTOR_TYPES`/`RATE_FACTOR_TYPES`):

- Level (price) factors: `equities`, `commodities`, and `real_estate` once compounded
  into an index. These simulate an amount of money and are the only ones converted.
- Rate and ratio factors: `interest_rates`, `inflation`, `credit`, `unemployment`,
  `yield_curve`, `dividend_yield` and `leading_indicator`. A German short rate of 3% is
  not "converted to dollars"; it stays 3%. A dividend yield is a ratio (only the
  ticker's price would need converting), and the leading indicator is an index not
  quoted in any currency (its `currency` field is descriptive metadata, kept for schema
  consistency). Asking to convert one of these raises a `ValueError` rather than
  silently multiplying a rate by an exchange rate.

`real_estate` simulates a growth *rate*, so it is first compounded into a price index
with `ScenarioSet.cumulative_index()`, the same rate-to-level step the engine already
provides, and that index is converted.

The conversion follows the Finance Toolkit's OECD exchange-rate convention
(`economics.get_exchange_rates`): national currency units *per US dollar*. Going from a
native currency to USD divides by that currency's simulated FX path; going from USD to
another reporting currency multiplies by that currency's path. When neither side is USD
(euro equity reported in pounds), the conversion goes through USD in two legs, because
every `fx` factor in this project is quoted against the US dollar and there are no
direct cross pairs. Because the FX path is simulated jointly with the price, the
converted result carries the currency risk and its correlation with the asset.

Which `fx` entry supplies which currency: `FXConfig` has a `country`, not a
`currency`, so a country is mapped to its currency by reading the (`country`,
`currency`) pairs of the configured `interest_rates` and `inflation` entries, the only
place a run already states both. This is deliberately not a separate country/currency
table, so it can never drift from what the user set up. An `fx` entry whose `country`
has no matching `interest_rates`/`inflation` entry cannot be used and is treated as not
configured, rather than guessed at.

Whether a factor *can* be converted depends on which `fx` entries were actually
calibrated in this run (the calibration result, not the config, is the source of
truth for opt-in factors), so this is checked in `convert()`, not when the config is
loaded.

Why a separate package rather than a `ScenarioSet` method: the engine is
asset-class-agnostic, and currency is a domain concept that would make `ScenarioSet`
depend on `ScenariosConfig` (which factor is in which currency). One package per
concern, each with its own `_model.py`/`_controller.py`, is this project's pattern.

What it does not do: this is mechanically correct unit conversion; whether the result
is free of arbitrage depends on how the `fx` factor was configured. With the default
`fx[i].drift_mode: historical`, the exchange rate is a free-floating geometric Brownian
motion, independent of the simulated interest rates, so moving cash into a foreign
currency and back is not guaranteed to be a fair bet on average: the gap that interest
rate parity is meant to close. `drift_mode: irp` closes it under the real-world measure
by setting the FX drift to the simulated short-rate differential every step (the same
mechanism commercial multi-currency generators from Ortec Finance, Moody's/Barrie &
Hibbert and Conning use), and `measure: risk_neutral` does the equivalent under the
risk-neutral measure through covered interest rate parity
([Gorvett, 2001](https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf)).
This module is the "convert after simulation" half of that design whichever drift mode
feeds it, and does not check which one was used.

Configuration (`reporting` in a settings profile, beside `engine` and `toolkit`):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `reporting.reporting_currency` | `USD` | The currency `convert()` expresses a level factor in. |

It is a run setting, not a factor-set setting, and changing it has no effect on
`Scenarios.calibrate()`/`simulate()` or on the correlation matrix. Each level factor's
own `currency` field (`equities[i].currency`, `commodities[i].currency`,
`real_estate.currency`) says which currency it is natively simulated in.

**References:**

- Gorvett, R.W. (2001). "Foreign Exchange Rate Risk: Institutional Issues and Stochastic Modeling." CAS Discussion Paper Program. <https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf>

## convert

```python
convert(factor_name: str) -> pl.DataFrame
```

Convert one level factor's simulated paths into this run's reporting currency
(`config.reporting.reporting_currency`), path by path, using the `fx` paths of the
same simulations.

In plain terms: ask for a factor by name and get back its simulated prices as they
would read in your reporting currency. A yen-priced equity of 430 when the dollar
buys 158.79 yen reads as 430 / 158.79 = 2.71 dollars, and in every later year each
simulated path is divided by that same path's simulated exchange rate, so currency
swings are part of the outcome.

When the factor's native currency already is the reporting currency, the native
paths come back untouched and no `fx` entry is needed. Otherwise one leg (native to
USD, or USD to reporting) or two legs through USD are applied; see
`reporting_model.convert_to_reporting_currency`. `real_estate` is compounded into an
index first (`ScenarioSet.cumulative_index()`), since its own path is a growth rate.

Also known as: currency translation, re-denomination, FX conversion.

**Args:**

- <u>factor_name (str):</u> a factor name from a currency-tagged, level-type factor list (`equities`/`commodities`/`real_estate`); must be present in `config` and, apart from `real_estate`, in `scenario_set.paths`.

**Returns:**

<u>pl.DataFrame:</u> a `scenario` column plus one column per simulation date (ISO strings), one row per simulated path: the same layout as `ScenarioSet.to_dataframe()`, but holding price levels denominated in the reporting currency. When the factor's native currency already equals the reporting currency, this is a true identity/no-op over the native path (no `fx` lookup at all).

**Raises:**

- <u>ValueError:</u> if `factor_name` isn't a configured, currency-tagged factor, or names a rate/ratio/non-monetary-index factor type reporting-currency conversion doesn't apply to (see `reporting_model.assert_convertible_factor_type`).
- <u>KeyError:</u> if `factor_name` is configured but not actually present in `scenario_set.paths` (e.g. simulated with a different factor set, or a hand-built `ScenarioSet` holding only a Schwartz-Smith commodity's `_chi`/`_xi` components).
- <u>RuntimeError:</u> if the native and reporting currencies differ and one or both FX legs needed to bridge them weren't configured/calibrated in this run.

**Notes:**

- A missing leg is reported by country name where the run names one, for example:
  `converting 'eu_equity' (EUR) to reporting currency 'GBP' needs a configured fx
  entry for Germany, found: ['GBP']`.
- The `fx` entry's country must also appear in an `interest_rates` or `inflation`
  entry with its `currency`; that is how the exchange rate is tied to a currency code.
- This converts units only; see the class docstring for when the FX paths are
  consistent with interest rate parity.

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

Which returns (calibrated on 2026-10-04), summarized as the 5th, 50th and 95th
percentile across the 1,000 paths next to the native yen price and the simulated
yen per dollar:

| date | jp_equity (JPY), median | usd_jpy, median | jp_equity (USD), 5% | median | 95% |
|:-----|------------------------:|----------------:|--------------------:|-------:|----:|
| 2026-10-01 | 430.2 | 158.79 | 2.71 | 2.71 | 2.71 |
| 2027-10-01 | 483.0 | 162.17 | 2.02 | 2.98 | 3.70 |
| 2028-09-30 | 532.4 | 165.26 | 1.93 | 3.17 | 4.58 |
| 2029-10-01 | 564.0 | 167.75 | 1.92 | 3.38 | 5.33 |
| 2030-10-01 | 602.2 | 171.54 | 1.77 | 3.54 | 6.28 |
| 2031-10-01 | 661.8 | 174.18 | 1.79 | 3.78 | 7.12 |

The TOPIX ETF starts at 430.2 yen, which at 158.79 yen per dollar is 2.71 dollars.
Its median yen price grows about 54% over five years, but the median simulated yen
also weakens to 174 per dollar, so the median dollar value grows less, to 3.78
dollars. `reporting.convert("interest_rate")` raises a `ValueError` instead,
because a rate has no currency to convert.

**References:**

- Gorvett, R.W. (2001). "Foreign Exchange Rate Risk: Institutional Issues and Stochastic Modeling." CAS Discussion Paper Program. <https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf>
