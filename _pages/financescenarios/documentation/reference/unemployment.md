---
title: "Unemployment"
seo_title: "Unemployment Reference – Finance Scenarios"
excerpt: "Unemployment rates, each paired with an inflation entry."
description: "Unemployment rates, each paired with an inflation entry."
author_profile: false
permalink: /projects/financescenarios/docs/reference/unemployment
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Unemployment rates, each paired with an inflation entry. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.factors.unemployment.unemployment_controller import Unemployment
```

```python
Unemployment(toolkit: Toolkit)
```

The Unemployment module simulates the unemployment rate: the share of people who
want work but cannot find it. Unemployment drifts back toward a normal level over
time, and it also moves with inflation, since the two are historically linked: as
inflation rises the labor market tends to tighten and unemployment tends to fall.
This module captures both.

In plain terms: every run carries one or more unemployment rates, one per country or
region (the United States, the Eurozone, ...), and each becomes a variable in the
simulated scenarios, linked to interest rates, equities and the rest through the
correlation matrix. Each unemployment rate is paired with one simulated inflation
rate, so a scenario in which inflation jumps also tends to be one in which
unemployment falls, the way the two have moved together historically.

The model is a mean-reverting (Ornstein-Uhlenbeck) process with an added
Phillips-curve term, the relation between inflation and unemployment first
documented by [Phillips (1958)](https://doi.org/10.1111/j.1468-0335.1958.tb00003.x):

```text
du = kappa_u * (mu_u - u) * dt + alpha_u * d(inflation) + sigma_u * dW
```

Here `kappa_u` is the mean-reversion speed (how quickly unemployment is pulled back
toward its normal level), `mu_u` the long-run unemployment rate, `alpha_u` the
Phillips-curve sensitivity to the *change* in inflation over the same step (expected
to be negative: rising inflation goes with falling unemployment) and `sigma_u` the
volatility of unemployment's own random shock `dW`. This is equation 3.19 of
[Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf),
"Modeling Financial Scenarios: A Framework for the Actuarial Profession", the same
base framework the interest rate, inflation and equity modules follow; unemployment
is one of that framework's six variables, and the first of its remaining ones
(alongside dividend yield and real estate) added to Finance Scenarios.

Each simulated step uses the exact discrete-time Ornstein-Uhlenbeck transition for
the mean-reverting part (exact rather than an approximation, so a large time step
stays accurate), with the Phillips-curve term added on top, since that term is
already a per-step quantity:

```text
next_value = mu_u + (current_value - mu_u) * exp(-kappa_u * dt) + alpha_u * inflation_change
             + sigma_u * sqrt((1 - exp(-2 * kappa_u * dt)) / (2 * kappa_u)) * shock
```

`inflation_change` is the paired inflation factor's *already simulated* move over that
same step, not a separately drawn number. Each unemployment entry depends on exactly
its own paired inflation entry (the `dependencies` that `Scenarios.calibrate()` builds),
so the simulation engine's ordering of factors always advances that inflation entry
first within a step, and the unemployment step reads its just-written value.

One option changes the process. `condition_on_business_cycle` adds a *second*
covariate (an extra explanatory series in the fit), the leading indicator's
step-to-step change, alongside the inflation term rather than instead of it:

```text
du = kappa_u * (mu_u - u) * dt + alpha_u * d(inflation) + gamma_u * d(CLI) + sigma_u * dW
```

This differs from every other factor's `condition_on_business_cycle`, where the leading
indicator becomes the factor's *only* covariate (see `LeadingIndicator`). Unemployment
already has a covariate, so the fit estimates two at once, and
`UnemploymentParams.business_cycle_sensitivity` (`gamma_u`) is `None` unless this is
enabled. It requires `leading_indicator.enabled: true` and `leading_indicator.period`
equal to the paired inflation entry's period, so all three series share one frequency
(checked when the configuration loads); calibration then joins unemployment, inflation
and the leading indicator on date before fitting.

The data come from the Finance Toolkit's Economics module, no ticker required:
`economics.get_unemployment_rate` for the unemployment rate and
`economics.get_consumer_price_index(growth=True)`, year over year, for the inflation input of the
Phillips-curve fit, both for this entry's own `country` and `source`. With
`source: oecd` (the default) both come from the OECD, which covers OECD members;
`source: gmdb` routes both through the Global Macro Database instead, covering
countries outside the OECD roster (Brazil, India, China, ...), but GMDB is annual
only. Neither source needs an API key.

Multiple regions: `unemployment` in a factor set is a list, with at least one entry
required. Each entry is calibrated independently, linked to the others through the
correlation matrix and named by its own `name`. `inflation_name` names which
`inflation[i].name` entry this one reads its Phillips-curve change from during the
simulation; the configuration raises an error at load time if it does not match a
configured inflation entry. The fit itself pulls this entry's own `country` inflation,
independently of which entry it is paired with for the simulation. An unemployment
entry has no `period` of its own: calibration uses the paired inflation entry's period
(`monthly`, `quarterly` or `yearly`), so the two series share one frequency, and joins
them on date rather than truncating them to equal length. For that reason
`source: gmdb` requires the paired inflation entry's `period` to be `yearly`, which the
configuration checks up front rather than silently truncating.

This models the unemployment rate itself, not employment by sector, wages or labor
force participation. The Phillips curve here is a statistical link fitted to history,
not a structural model of how central banks or wage setting respond.

Configuration (`unemployment[i]` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `name` | `unemployment` | The factor's name in the simulated output; unique across all factor lists. |
| `country` | `United States` | Used for both the unemployment and the inflation fetch of the fit. |
| `source` | `oecd` | `oecd` or `gmdb`; `gmdb` requires the paired inflation entry to be `yearly`. |
| `inflation_name` | `inflation` | Which `inflation[i].name` drives the Phillips-curve term in the simulation. |
| `condition_on_business_cycle` | `false` | Adds the leading indicator as a second covariate (see above). |
| `beliefs.mean_reversion_speed` | `null` | Override the fitted speed; must be greater than 0. |
| `beliefs.long_run_mean` | `null` | Override the fitted long-run unemployment rate. |
| `beliefs.inflation_sensitivity` | `null` | Override the fitted Phillips-curve coefficient; any sign is allowed. |
| `beliefs.volatility` | `null` | Override the fitted volatility; must be greater than 0. |

A belief left as `null` keeps the statistically calibrated value; any other value
replaces that one parameter with your own view, per entry (`apply_unemployment_beliefs`
in `config_model.py`). In a regime file, address one entry's beliefs with a dotted
`"unemployment.<name>"` key.

Every entry across `interest_rates`, `inflation`, `equities`, `unemployment`, `fx` and
`credit` shares one flat name space, which is why the shipped `factors.yaml` names these
`<region>_unemployment`. That file writes the list in a friendlier `defaults` +
`countries` shape, where `inflation_name` defaults to the same country's own inflation
factor (`name: Eurozone` pairs with `eurozone_inflation`) unless overridden.

**References:**

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Phillips, A.W. (1958). "The Relation Between Unemployment and the Rate of Change of Money Wage Rates in the United Kingdom, 1861-1957." Economica, 25(100), 283-299. <https://doi.org/10.1111/j.1468-0335.1958.tb00003.x>
- Uhlenbeck, G.E., Ornstein, L.S. (1930). "On the Theory of the Brownian Motion." Physical Review, 36(5), 823-841. <https://doi.org/10.1103/PhysRev.36.823>

## calibrate

```python
calibrate(
    name: str,
    country: str = 'United States',
    period: str = 'yearly',
    source: str = 'oecd',
    business_cycle_covariate: pl.Series | None = None,
    business_cycle_covariate_dates: pl.Series | None = None,
) -> UnemploymentParams
```

Calibrate one country or region's unemployment process from its history: fetch
the unemployment rate and inflation for `country`, and fit how fast unemployment
returns to its normal level (`mean_reversion_speed`), what that normal level is
(`long_run_mean`), how strongly it moves with the change in inflation
(`inflation_sensitivity`) and how much it swings on its own (`volatility`).

In plain terms: this learns from the past how unemployment behaves, so the
simulated scenarios rise and fall the way the real rate has, and move against
inflation the way the two have moved together. The half-life of a shock is
ln 2 / `mean_reversion_speed`: a speed of 0.62 a year means a jump in
unemployment has faded by half after about 1.1 years.

The fit is an ordinary least squares regression of each period's change in
unemployment on the previous level and the same period's change in inflation,
the regression of `fit_ou_process` with one added explanatory series. Its
coefficients convert back into the mean-reversion speed, long-run mean and
Phillips-curve sensitivity, and the spread of what is left unexplained gives the
volatility. Every field is a decimal and annualized: `long_run_mean` of 0.0566 is a
5.66% unemployment rate, `initial_value` is the last observed rate (the start of
every simulated path), and `inflation_sensitivity` is the change in unemployment
per unit change in annualized inflation over one step (a 1 point rise in inflation
with a sensitivity of -0.037 lowers unemployment by about 0.04 points). With a
business-cycle covariate, `business_cycle_sensitivity` is the change in
unemployment per one-point change in the leading indicator over one step.

Also known as: Phillips-curve calibration, unemployment mean-reversion fit.

**Args:**

- <u>name (str):</u> this entry's name, used to key params()/changes() and as the factor name in the simulation (e.g. "united_states", "eurozone").
- <u>country (str):</u> the country to pull unemployment and inflation data for.
- <u>period (str):</u> sampling frequency of the underlying data ("monthly", "quarterly" or "yearly" for source="oecd"; "yearly" only for source="gmdb"), determines dt; also the period inflation is fetched at, so the Phillips-curve pairing below is always genuinely date-aligned regardless of which one is chosen. Defaults to "yearly" when called directly; a configured run passes the paired inflation entry's period.
- <u>source (str):</u> "oecd" (the default: Finance Toolkit's OECD unemployment rate and Consumer Price Index) or "gmdb" (its Global Macro Database for both series; covers countries outside the OECD roster, period="yearly" only).
- <u>business_cycle_covariate (pl.Series &#124; None):</u> the leading indicator's raw historical level series (e.g. LeadingIndicator.series). When supplied, adds a second Phillips-curve-style covariate term alongside inflation's; see unemployment_model.fit_unemployment_process's own docstring for why this is a genuine two-covariate extension, not the shared single-covariate `condition_on_business_cycle` mechanism every other factor uses.
- <u>business_cycle_covariate_dates (pl.Series &#124; None):</u> the dates paired with `business_cycle_covariate` (e.g. LeadingIndicator.dates). Required whenever `business_cycle_covariate` is supplied: this entry's own unemployment/inflation fetch and the leading indicator are independent, so the three series are inner-joined on date before fitting, the same way credit/real_estate's own `business_cycle_covariate` is paired against their own fetch.

**Returns:**

<u>UnemploymentParams:</u> the calibrated process parameters.

**Raises:**

- <u>ValueError:</u> if period or source is not recognized, period isn't "yearly" for source="gmdb", or exactly one of business_cycle_covariate/business_cycle_covariate_dates is given; also, from the fit, if the joined series have fewer than 5 observations (6 with a business-cycle covariate) or the fitted mean-reversion speed is not positive.

**Notes:**

- In a full run the `period` is not chosen per unemployment entry: it is the paired
  `inflation_name` entry's period (or `leading_indicator.period` when conditioned on
  the business cycle), so the Phillips-curve pair shares one frequency.
- Unemployment and inflation are joined on date, not truncated to the same length,
  so the pairs are contemporaneous; rows with a missing value in either are dropped.
- Inflation is the year-over-year growth of the Consumer Price Index, the same
  series as the paired inflation factor it reads in the simulation.
- The data start at the `Toolkit`'s `start_date`; the Finance Toolkit's default
  window is short, so pass an early `start_date` for a meaningful fit.
- A near-zero mean-reversion speed makes `long_run_mean` unreliable. Germany at a
  quarterly period from 2000 gave a speed of 0.014 and a long-run mean of -5.2%,
  because its unemployment fell steadily for fifteen years; set
  `beliefs.long_run_mean` and `beliefs.mean_reversion_speed` in such a case.
- The fitted Phillips-curve sign is not forced: Brazil (GMDB, yearly) came out
  positive. Override it with `beliefs.inflation_sensitivity` if needed.
- The OECD API rate-limits bursts of requests (HTTP 429); the Finance Toolkit then
  returns no data and this raises a `ValueError` naming the empty series. Waiting a
  minute and retrying resolves it.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.unemployment.unemployment_controller import Unemployment

toolkit = Toolkit(["AAPL"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2000-01-01")
unemployment = Unemployment(toolkit)

unemployment.calibrate("united_states", country="United States", period="quarterly")
unemployment.calibrate("brazil", country="Brazil", period="yearly", source="gmdb")
```

Which returns (calibrated on 2026-10-05):

| name | mean_reversion_speed | long_run_mean | inflation_sensitivity | volatility | initial_value |
|:-----|---------------------:|--------------:|----------------------:|-----------:|--------------:|
| united_states | 0.5534 | 0.0567 | -0.3432 | 0.0211 | 0.0427 |
| brazil | 0.1939 | 0.0906 | 0.0366 | 0.0143 | 0.0734 |

US unemployment starts at 4.27% and is pulled toward 5.67% with a half-life of
about 1.3 years, and moves against inflation as the Phillips curve expects. Brazil's
starts at 7.34% and is pulled toward 9.06% far more slowly (a half-life of about 3.6
years, fitted on 26 yearly observations), and its inflation sensitivity came out
slightly positive.

**References:**

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Phillips, A.W. (1958). "The Relation Between Unemployment and the Rate of Change of Money Wage Rates in the United Kingdom, 1861-1957." Economica, 25(100), 283-299. <https://doi.org/10.1111/j.1468-0335.1958.tb00003.x>

## names

```python
unemployment.names  # property -> list[str]
```

The names of every unemployment entry calibrated so far, in calibration order.

## params

```python
params(name: str) -> UnemploymentParams
```

The calibrated process parameters for one unemployment entry.

**Args:**

- <u>name (str):</u> the entry's name, as passed to calibrate().

**Raises:**

- <u>RuntimeError:</u> if calibrate(name, ...) hasn't been called yet.

## step_function

```python
unemployment.step_function  # property
```

The step function for the unemployment process (exact OU transition plus the Phillips-curve term; stateless,
shared across every entry).

## changes

```python
changes(name: str) -> pl.DataFrame
```

Dated period-over-period changes in one entry's unemployment rate, from the
same data calibrate() already fetched, reused for cross-factor correlation
estimation (Dependence) instead of triggering a second Finance Toolkit fetch
at a different period.

**Args:**

- <u>name (str):</u> the entry's name, as passed to calibrate().

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` (pl.Date) and `value` (f64); see helpers.dated_changes().

**Raises:**

- <u>RuntimeError:</u> if calibrate(name, ...) hasn't been called yet.
