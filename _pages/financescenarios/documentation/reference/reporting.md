---
title: "Reporting"
seo_title: "Reporting Reference | Finance Scenarios"
seo_title_suffix: false
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

Convert simulated prices into one reporting currency after the simulation.

```python
from financescenarios.reporting.reporting_controller import Reporting
```

Show simulated prices in one reporting currency: take a factor simulated in its own currency, such as a Japanese
equity in yen, and convert every scenario into, say, US dollars with that scenario's own simulated exchange rate.

An investor who reports in dollars wants to see what a Japanese or European holding is worth in dollars in each
scenario, including the currency gain or loss, not just its local price. Because the exchange rate is simulated
together with the price, the converted result carries the currency risk and its correlation with the asset: in
a scenario where the yen weakens as Japanese equities rally, the dollar investor keeps less of the rally. An
unhedged foreign holding is therefore usually riskier in the reporting currency than in its own, unless the
currency tends to move against the asset. `Portfolio` uses it to put every holding in the reporting currency
before weighting; the run itself is left unchanged.

Only price-like factors are converted: `equities`, `commodities` and `real_estate`, whose growth rate is first
compounded into a price index. Rates and ratios (`interest_rates`, `inflation`, `credit`, `unemployment`,
`yield_curve`, `dividend_yield`, `leading_indicator`) have no currency to convert: a German short rate of 3% stays
3%, so asking to convert one raises a `ValueError`.

Exchange rates follow the OECD convention: units of the national currency per US dollar. Going from a currency to
dollars divides by its simulated rate, going from dollars to a currency multiplies by it, and two non-dollar
currencies are bridged through the dollar in two steps, since every `fx` factor is quoted against the dollar. Each
`fx` entry names its currency in `currency`; when that is unset, it is read from an `interest_rates` or `inflation`
entry for the same `country`, or is `EUR` for the OECD's euro area codes.

With the default `fx[i].drift_mode: random_walk` (or `historical`) the exchange rate moves independently of the
simulated interest rates; `drift_mode: irp` or `measure: risk_neutral` ties its expected move to the rate gap
between the two currencies through interest rate parity, as a market-consistent valuation needs
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

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Reporting(scenario_set: ScenarioSet, config: ScenariosConfig)
```

</details>

## convert

Convert one price-like factor's simulated paths into the run's reporting currency, using each path's own
simulated exchange rate.

Ask for a factor by name and get its simulated prices in your reporting currency. A yen-priced equity of 430
when the dollar buys 158.79 yen reads as 430 / 158.79 = 2.71 dollars, and every later value is divided by that
path's exchange rate, so currency swings are part of the outcome. A factor already in the reporting currency
comes back unchanged; `real_estate` is first compounded from a growth rate into a price index.

With P_N the price in its own currency and X_N and X_R the simulated units of the native and the reporting
currency per US dollar (1 for the dollar itself), each path converts at its own exchange rates.

The formula is as follows:
- P_R = P_N * X_R / X_N

**As an example:**

```python
from datetime import date

from financescenarios import (
    EngineConfig,
    EquityConfig,
    FXConfig,
    InflationConfig,
    InterestRateConfig,
    Scenarios,
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

Which returns (calibrated on 2026-10-14), as percentiles across the 1,000 paths next to the median yen price
and yen per dollar:

| date | jp_equity (JPY), median | usd_jpy, median | jp_equity (USD), 5% | median | 95% |
|:-----|------------------------:|----------------:|--------------------:|-------:|----:|
| 2026-10-01 | 431.3 | 157.00 | 2.75 | 2.75 | 2.75 |
| 2027-10-01 | 483.5 | 157.14 | 2.13 | 3.10 | 3.80 |
| 2031-10-01 | 666.5 | 156.49 | 2.01 | 4.19 | 7.71 |

The yen price grows 55% in five years and the median exchange rate stays near 157 yen per dollar, so the
median dollar value grows about as much, but the 5% to 95% range in dollars is wide: the dollar investor
carries the currency risk on top of the equity risk.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
convert(factor_name: str) -> pl.DataFrame
```

**Args:**

- <u>factor_name (str):</u> the name of an `equities`, `commodities` or `real_estate` factor in this run.

**Returns:**

<u>pl.DataFrame:</u> a `scenario` column plus one column per date, one row per path, as `ScenarioSet.to_dataframe()`.

**Raises:**

- <u>ValueError:</u> if `factor_name` is not a configured factor with a currency, or is a rate or ratio factor.
- <u>KeyError:</u> if the factor is configured but missing from this `ScenarioSet`.
- <u>RuntimeError:</u> if this run lacks the `fx` entry the conversion needs; the message names its country.

</details>

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

### convert_to_reporting_currency

Convert a price simulated in its own currency into the reporting currency, scenario by scenario, with each
scenario's own simulated exchange rate. The converted price carries the currency gain or loss, and its correlation
with the asset, that an investor reporting in another currency actually experiences.

Exchange rates are quoted as units of the national currency per US dollar (the OECD convention). Going from a
currency to dollars divides by its rate, going from dollars to a currency multiplies by it, and two non-dollar
currencies are bridged through the dollar in two steps. A price already in the reporting currency comes back
unchanged.

The formula is as follows:

$$
P_{rep}(t) = P_{nat}(t) / X_{nat}(t) \cdot X_{rep}(t)
$$

Where P_nat is the price in its own currency, X_nat and X_rep the units of the native and the reporting currency
per US dollar, and X_USD = 1, so a USD price skips the division and a USD reporting currency the multiplication.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
convert_to_reporting_currency(
    native_paths: np.ndarray,
    fx_rate_paths: dict[str, np.ndarray],
    native_currency: str,
    reporting_currency: str,
) -> np.ndarray
```

**Args:**

- <u>native_paths (np.ndarray):</u> the simulated price per scenario and date, in its own currency.
- <u>fx_rate_paths (dict[str, np.ndarray]):</u> currency code to its simulated exchange rate (units per US dollar) per scenario and date; only the currencies the conversion needs.
- <u>native_currency (str):</u> the currency the price is in.
- <u>reporting_currency (str):</u> the currency to convert into.

**Returns:**

<u>np.ndarray:</u> the price per scenario and date, in the reporting currency.

**Raises:**

- <u>KeyError:</u> if an exchange rate the conversion needs is missing.

</details>
