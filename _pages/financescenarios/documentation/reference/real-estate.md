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

House-price and commercial property growth. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.factors.real_estate.real_estate_controller import RealEstate
```

```python
RealEstate(toolkit: Toolkit)
```

The Real Estate module simulates the growth rate of property prices: how fast house prices
(or commercial property prices) rise or fall each year. Property booms and busts tend to fade
back toward a normal growth rate over a few years, and that is the behavior this module
captures.

In plain terms: enable it and every simulated scenario gets a property-price growth path,
linked to interest rates, inflation, equities and the rest through the correlation matrix,
so a portfolio or liability that holds property can be put through the same scenarios. It is
opt-in (`real_estate.enabled`, `false` in a bare config), though the shipped `default.yaml` and `broad.yaml`
factor set turns it on for the United States.

The model is a mean-reverting (Ornstein-Uhlenbeck) process on the growth rate,
`d(re) = a(theta - re)dt + sigma*dW`: growth is pulled toward a normal level `theta` at speed
`a`, with random swings of size `sigma`. It is the real estate process of the
[Ahlgrim, D'Arcy & Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf)
financial scenario generator (their eq. 3.18), the same framework the interest rate,
inflation, equity and unemployment modules follow. They also tested inflation as an extra
driver of real estate growth (the way unemployment uses a Phillips-curve term), found it not
statistically significant and dropped it, and so does this module. The growth rate is
modeled rather than the price index itself, because an index level (2015 = 100) has no
normal level to return to over decades, while its growth rate does; the FX module uses
geometric Brownian motion on the level for the same reason. There is no
`real_estate_model.py`: nothing here is real-estate-specific, so calibration goes straight
through `calibration_model.fit_ou_process` and simulation through `step_ou_process`, for
either source. The factor is correlation-linked only, with no cascade dependency on any
other factor.

Two options change the process. `volatility_model="garch"` replaces the fixed volatility
with GARCH(1,1), so calm and turbulent property markets each persist
([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1)), reusing the interest rate
module's `fit_garch_process`/`GARCHStepper`. `condition_on_business_cycle` adds a pull from
the leading indicator's step-to-step change, so property growth tends to slow as the economy
does; it needs `leading_indicator.enabled: true` with `period: quarterly` or `yearly`, since
real estate does not accept the leading indicator's default `monthly`. The two cannot be
combined, and belief overrides apply only to the constant-volatility fit.

Two data sources are available (`source`), both through the Finance Toolkit:

- `house_price` (default): the OECD residential house-price index for `country`, via
  `economics.get_house_prices(countries=..., quarterly=..., growth=True, lag=..., gmdb_source=False)`.
  The lag is 4 quarters or 1 year (`helpers.YEAR_OVER_YEAR_LAG`), so each value is the
  change in house prices over the past year, the headline figure, on the same scale as the
  commercial series and every other rate factor (0.04 is 4% a year). A year-over-year
  change also removes the seasonal pattern of house prices, which not every country's
  series is adjusted for. `gmdb_source=False` matters: the call otherwise defaults to the Global
  Macro Database, which is annual-only and silently ignores `quarterly` (the same trap the
  interest rate module's OECD path avoids). Quarterly is the finest frequency; no monthly
  series exists.
- `commercial`: FRED's quarterly Commercial Real Estate Price Index for the United States
  (series `COMREPUSQ159N`, itself from the IMF's Financial Soundness Indicators), via
  `economics.get_commercial_real_estate_prices()`. It tracks office, retail, industrial and
  apartment prices, a different asset class from homes. The call takes no country, so
  `country` must be "United States"; no annual series exists, so `period` must be
  "quarterly"; and it needs a FRED API key (`FRED_API_KEY`, which `build_toolkit()` picks up).
  FRED publishes it only as a year-over-year growth rate, so it is used as-is, neither
  differenced again nor annualized. Both `RealEstateConfig` and `calibrate()` enforce these.

Neither source is what Ahlgrim, D'Arcy and Gorvett calibrated against: NCREIF's
appraisal-based commercial property index, which is smoothed by appraisals (lower measured
volatility, higher autocorrelation) and has no open equivalent anywhere. The FRED series is
transaction-based and more volatile. See the coverage overview for this gap.

Configuration (`real_estate` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `enabled` | `false` | Adds a `real_estate` factor to the simulation when `true`. |
| `source` | `house_price` | `house_price` (OECD residential) or `commercial` (FRED/IMF US commercial). |
| `country` | `United States` | The house-price country; must be `United States` for `commercial`. |
| `currency` | `USD` | Currency label used when results are exported; does not affect calibration. |
| `period` | `quarterly` | `quarterly` or `yearly`; must be `quarterly` for `commercial`. |
| `volatility_model` | `constant` | `constant` or `garch`. |
| `condition_on_business_cycle` | `false` | Requires `leading_indicator.enabled` with a quarterly/yearly period. |
| `beliefs.mean_reversion_speed` | `null` | Override the fitted speed; must be above 0. |
| `beliefs.long_run_mean` | `null` | Override the fitted normal growth rate (annualized decimal). |
| `beliefs.volatility` | `null` | Override the fitted volatility; must be above 0. |

A belief left as `null` keeps the fitted value. Beliefs apply only when `volatility_model` is
`constant`, through `config_model.apply_ou_beliefs`, the same function the interest rate and
inflation modules use.

**References:**

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Uhlenbeck, G.E., Ornstein, L.S. (1930). "On the Theory of the Brownian Motion." Physical Review, 36(5), 823-841. <https://doi.org/10.1103/PhysRev.36.823>
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." Journal of Econometrics, 31(3), 307-327. <https://doi.org/10.1016/0304-4076(86>)90063-1

## calibrate

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

Calibrate the real estate growth process from its history: fetch the house-price (or
commercial property price) growth series, and fit how fast growth returns to its normal
rate (`mean_reversion_speed`), what that normal rate is (`long_run_mean`) and how much it
swings (`volatility`).

In plain terms: this learns from the past how property price growth behaves, so the
simulated scenarios boom and cool the way the real market has. A mean-reversion speed of
0.5 a year, for example, means a boom has faded by half after about 1.4 years
(ln 2 / 0.5 years).

All values are annualized decimals: a `long_run_mean` of 0.04 is 4% price growth a year,
and `initial_value` is the latest observed growth rate, the starting point of every
simulated scenario.

Also known as: house price growth calibration, Ahlgrim-D'Arcy-Gorvett real estate process.

**Args:**

- <u>country (str):</u> the country to pull house prices for. Only used when source="house_price"; source="commercial" is US-only and requires this to be "United States".
- <u>period (str):</u> sampling frequency of the underlying data ("quarterly" or "yearly"), which sets the time step. Quarterly is the finest available. source="commercial" is quarterly-only and requires "quarterly".
- <u>volatility_model (str):</u> "constant" (constant-volatility OU, the default) or "garch" (GARCH(1,1) time-varying volatility, Bollerslev 1986).
- <u>source (str):</u> "house_price" (default): OECD residential house-price growth via get_house_prices(). "commercial": FRED's (IMF-sourced) US commercial real estate price growth via get_commercial_real_estate_prices() instead (US and quarterly only, needs a FRED API key, still not NCREIF-equivalent).
- <u>business_cycle_covariate (pl.Series &#124; None):</u> a business-cycle indicator's raw historical level series (e.g. LeadingIndicator.series). When supplied, adds an additive drift term on the covariate's step-to-step change (business-cycle conditioning); incompatible with volatility_model="garch".
- <u>business_cycle_covariate_dates (pl.Series &#124; None):</u> the dates paired with `business_cycle_covariate` (e.g. LeadingIndicator.dates), same length and order. Required whenever `business_cycle_covariate` is supplied: house-price growth and the leading indicator are fetched independently and forced onto the same *period* but not guaranteed the same *start date*, so this factor's own dates and the covariate's are inner-joined on date before fitting, the same way unemployment_controller.py aligns unemployment against inflation.

**Returns:**

<u>OUParams &#124; GARCHParams &#124; OUCovariateParams:</u> the calibrated process parameters: GARCHParams when volatility_model="garch", OUCovariateParams when business_cycle_covariate is supplied.

**Raises:**

- <u>ValueError:</u> if period, volatility_model or source is not recognized, source="commercial" is combined with a country other than "United States" or a period other than "quarterly", business_cycle_covariate is combined with volatility_model="garch", business_cycle_covariate is supplied without business_cycle_covariate_dates (or vice versa), or the Finance Toolkit returned no data for the country (an unsupported country or a transient OECD rate limit).

**Notes:**

- The history starts at the Toolkit's `start_date`; a Toolkit built without one pulls
  only a few recent years, too few for a stable fit. Scenario runs use the settings
  profile's `toolkit.start_date` (2000-01-01 by default).
- Both sources are year-over-year growth: house prices are fetched with a one-year lag,
  and the commercial series is published that way. Because consecutive quarterly
  readings share three of their four quarters, the series is smooth, which the fitted
  mean reversion and volatility reflect.
- Without a FRED key, source="commercial" fails; inside a scenario run that failure is
  recorded in `calibration_failures` like any other per-factor fit failure.
- The OECD API allows about 60 downloads an hour; a rate-limited call returns no data and
  raises here.

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

US house prices are 2.1% higher than a year ago and are pulled toward 3.4% a year, with a
boom or slump fading by half in about 5.7 years (ln 2 / 0.122), the long housing cycle
of 2006-2012 (fitted on quarterly year-over-year data since 2000). Commercial property
prices grow faster today (6.6%) but toward a lower normal rate of 2.5% and revert within
about a year, with almost four times the volatility, as a transaction-based series
would show.

**References:**

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." Journal of Econometrics, 31(3), 307-327. <https://doi.org/10.1016/0304-4076(86>)90063-1

## params

```python
realestate.params  # property -> OUParams | GARCHParams | OUCovariateParams
```

The last-calibrated process parameters.

**Raises:**

- <u>RuntimeError:</u> if calibrate() hasn't been called yet.

## step_function

```python
realestate.step_function  # property
```

The exact-transition OU step function for the real estate process (`step_ou_process`).

## changes

```python
realestate.changes  # property -> pl.DataFrame
```

Dated period-over-period changes in the real estate return, from the same
data calibrate() already fetched, reused for cross-factor correlation
estimation (Dependence) instead of triggering a second Finance Toolkit fetch.

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` (pl.Date) and `value` (f64); see helpers.dated_changes().

**Raises:**

- <u>RuntimeError:</u> if calibrate() hasn't been called yet.
