---
title: "RealEstate"
seo_title: "RealEstate Reference – Finance Scenarios"
excerpt: "House-price and commercial property growth."
description: "House-price and commercial property growth."
author_profile: false
permalink: /projects/financescenarios/docs/reference/real-estate
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

House-price and commercial property growth.

```python
from financescenarios.factors.real_estate.real_estate_controller import RealEstate
```

The Real Estate module simulates the growth rate of property prices: how fast house prices (or commercial property
prices) rise or fall each year. Property booms and busts tend to fade back toward a normal growth rate over a few
years, and that is the behavior this module captures. Growth can turn negative, so price slumps such as 2008 are
in the scenario set, and because growth is persistent, a slump lasts several years rather than one bad quarter.

Enable it and every simulated scenario gets a property-price growth path, linked to interest rates, inflation,
equities and the rest through the correlation matrix, so a portfolio or liability that holds property can be put
through the same scenarios. It is opt-in (`real_estate.enabled`, `false` in a bare config), though the shipped
`default.yaml` and `broad.yaml` factor sets turn it on for the United States.

The model is a mean-reverting (Ornstein-Uhlenbeck) process on the growth rate:

```text
d(re) = a * (theta - re) * dt + sigma * dW
```

Growth is pulled toward a normal level `theta` at speed `a`, with random swings of size `sigma`. It is the real estate
process of the
[Ahlgrim, D'Arcy & Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf)
scenario generator (their eq. 3.18). The growth rate is modelled rather than the price index, because an index level
has no normal level to return to over decades, while its growth rate does. `volatility_model: garch` lets the size of
the swings vary over time ([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1)), and
`condition_on_business_cycle` adds a pull from the leading indicator, so property growth tends to slow as the economy
does; the two cannot be combined.

Two data sources (`source`), both through the Finance Toolkit and both as year-over-year growth (0.04 is 4% a year):

- `house_price` (default): the OECD residential house-price index for `country`, quarterly or yearly, no API
  key.
- `commercial`: FRED's US Commercial Real Estate Price Index (from the IMF), office, retail, industrial and
  apartment prices. United States and quarterly only, and it needs a FRED API key.

Neither is the appraisal-based NCREIF index the paper was calibrated on, which has no open equivalent.

Configuration (`real_estate` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `enabled` | `false` | Adds a `real_estate` factor to the simulation when `true`. |
| `source` | `house_price` | `house_price` (OECD residential) or `commercial` (FRED/IMF US commercial). |
| `country` | `United States` | The house-price country; must be `United States` for `commercial`. |
| `currency` | `USD` | The currency the prices are in, used when `Reporting` converts them. |
| `period` | `quarterly` | `quarterly` or `yearly`; must be `quarterly` for `commercial`. |
| `volatility_model` | `constant` | `constant` or `garch`. |
| `condition_on_business_cycle` | `false` | Needs `leading_indicator.enabled` with a quarterly or yearly period. |
| `beliefs` | none | Override the fitted speed, normal growth rate or volatility (constant volatility only). |

**References:**

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Uhlenbeck, G.E., Ornstein, L.S. (1930). "On the Theory of the Brownian Motion." Physical Review, 36(5), 823-841. <https://doi.org/10.1103/PhysRev.36.823>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
RealEstate(toolkit: Toolkit)
```

</details>

## calibrate

Calibrate the real estate growth process: fetch the house-price (or commercial property price) growth series, then
fit how fast growth returns to its normal rate (`mean_reversion_speed`), what that rate is (`long_run_mean`) and
how much it swings (`volatility`).

This learns how property price growth has behaved, so the simulated scenarios boom and cool the way the real
market has. A speed of 0.5 a year means a boom has faded by half after about 1.4 years (ln 2 / 0.5). All values
are annualized decimals: a `long_run_mean` of 0.04 is 4% growth a year, and `initial_value` is the latest growth
rate, where every simulated path starts. Give the Toolkit an early `start_date`: its default window is too short
for a stable fit.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.real_estate.real_estate_controller import RealEstate

toolkit = Toolkit(
    ["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", fred_api_key="FRED_KEY", start_date="2000-01-01"
)
real_estate = RealEstate(toolkit)

real_estate.calibrate(country="United States", period="quarterly")
real_estate.calibrate(source="commercial", period="quarterly")
```

Which returns (calibrated on 2026-10-06):

| source | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-------|---------------------:|--------------:|-----------:|--------------:|
| house_price | 0.1221 | 0.0343 | 0.0282 | 0.0214 |
| commercial | 0.6735 | 0.0245 | 0.1083 | 0.0658 |

US house prices are 2.1% higher than a year ago and are pulled toward 3.4% a year, a slump fading by half in about
5.7 years; commercial prices revert within about a year, with almost four times the volatility.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(
    country: str = 'United States',
    period: str = 'quarterly',
    volatility_model: str = 'constant',
    source: str = 'house_price',
    business_cycle_covariate: pl.Series | None = None,
    business_cycle_covariate_dates: pl.Series | None = None,
) -> OUParams | GARCHParams | OUCovariateParams
```

**Args:**

- <u>country (str):</u> the house-price country; "United States" for "commercial". Defaults to "United States".
- <u>period (str):</u> "quarterly" or "yearly"; "commercial" needs "quarterly". Defaults to "quarterly".
- <u>volatility_model (str):</u> "constant" or "garch". Defaults to "constant".
- <u>source (str):</u> "house_price" (OECD) or "commercial" (FRED, key needed). Defaults to "house_price".
- <u>business_cycle_covariate (pl.Series &#124; None):</u> leading indicator history to condition on. Defaults to None.
- <u>business_cycle_covariate_dates (pl.Series &#124; None):</u> its dates, needed with it. Defaults to None.

**Returns:**

<u>OUParams &#124; GARCHParams &#124; OUCovariateParams:</u> the fitted process; GARCHParams with "garch", OUCovariateParams with a covariate.

**Raises:**

- <u>ValueError:</u> if an option is not recognized or not allowed with "commercial", "garch" is combined with a covariate, or no data come back (an unsupported country, a missing FRED key or an OECD rate limit).

</details>

## params

The calibrated growth process: reversion speed, normal growth rate, volatility and today's growth rate.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
realestate.params  # property -> OUParams | GARCHParams | OUCovariateParams
```

**Raises:**

- <u>RuntimeError:</u> if `calibrate()` has not been called yet.

</details>

## step_function

The one-step update of the growth rate: an exact Ornstein-Uhlenbeck step.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
realestate.step_function  # property
```

</details>

## changes

Dated period-over-period changes of the growth rate: the history its correlations with the other factors are
estimated from.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
realestate.changes  # property -> pl.DataFrame
```

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if `calibrate()` has not been called yet.

</details>
