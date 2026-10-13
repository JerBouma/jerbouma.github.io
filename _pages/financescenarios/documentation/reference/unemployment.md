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

The Unemployment module simulates the unemployment rate: the share of people who want work but cannot find it.
Unemployment drifts back toward a normal level over time, and it also moves with inflation: as inflation rises, the
labor market tends to tighten and unemployment tends to fall. This module captures both.

Every run has at least one unemployment rate; add one per country or region. Each becomes a variable in the
simulated scenarios, correlated with the other factors, and is paired with one simulated inflation rate, so a
scenario in which inflation jumps also tends to be one in which unemployment falls, the way the two have moved
together historically.

The model is a mean-reverting (Ornstein-Uhlenbeck) process with an added Phillips-curve term, the link between
inflation and unemployment first documented by
[Phillips (1958)](https://doi.org/10.1111/j.1468-0335.1958.tb00003.x). It is equation 3.19 of
[Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf):

```text
du = kappa_u * (mu_u - u) * dt + alpha_u * d(inflation) + sigma_u * dW
```

`kappa_u` is how fast unemployment is pulled back to its normal level `mu_u`, `alpha_u` its sensitivity to the
change in inflation over the same step (expected to be negative), and `sigma_u` the size of its own random swings
`dW`. In the simulation, the change in inflation is the paired inflation entry's own simulated move.
`condition_on_business_cycle` adds the leading indicator's change as a second driver next to inflation, with its own
sensitivity.

The data are the Finance Toolkit's unemployment rate and year-over-year Consumer Price Index for the entry's
`country`, with no ticker or API key needed. `source: oecd` covers OECD members; `source: gmdb` (the Global Macro
Database) adds countries such as Brazil and India, yearly only. An entry has no `period` of its own: it uses the
paired inflation entry's, so the two series share one frequency.

Configuration (`unemployment[i]` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `name` | `unemployment` | The factor's name; unique across all factors. |
| `country` | `United States` | The country for both the unemployment and the inflation data. |
| `source` | `oecd` | `oecd` or `gmdb`; `gmdb` needs the paired inflation entry to be `yearly`. |
| `inflation_name` | `inflation` | The `inflation[i].name` that drives the Phillips-curve term. |
| `condition_on_business_cycle` | `false` | Adds the leading indicator; needs `leading_indicator.enabled: true`. |
| `beliefs.mean_reversion_speed` | `null` | Your own speed in place of the fit; greater than 0. |
| `beliefs.long_run_mean` | `null` | Your own long-run unemployment rate. |
| `beliefs.inflation_sensitivity` | `null` | Your own Phillips-curve sensitivity; any sign. |
| `beliefs.volatility` | `null` | Your own volatility; greater than 0. |

A belief left `null` keeps the fitted value; a regime file addresses one entry as `"unemployment.<name>"`. This
models the unemployment rate itself, not wages or employment by sector, and the Phillips curve is a statistical link
fitted to history, not a model of how central banks or wage setters respond.

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

Calibrate one country's unemployment process from its history: how fast unemployment returns to its normal
level (`mean_reversion_speed`), what that level is (`long_run_mean`), how strongly it moves with the change in
inflation (`inflation_sensitivity`) and how much it swings on its own (`volatility`).

This learns how unemployment has behaved, so simulated scenarios rise, fall and move against inflation the way
the real rate has. In the US example below, a speed of 0.55 a year halves a jump in about 1.3 years, and a
sensitivity of -0.34 means a one-point rise in inflation lowers unemployment by about a third of a point.

The fit regresses each period's change in unemployment on its previous level and the same period's change in
inflation, matched by date, following
[Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf).
Use an early Toolkit `start_date`, as the default window is short.

**Args:**

- <u>name (str):</u> the entry's name, e.g. "united_states".
- <u>country (str):</u> the country for both data series, default "United States".
- <u>period (str):</u> data frequency: "yearly" (default), "quarterly" or "monthly"; only "yearly" for "gmdb". A configured run uses the paired inflation entry's period.
- <u>source (str):</u> "oecd" (default) or "gmdb" (the Global Macro Database, for countries outside the OECD).
- <u>business_cycle_covariate (pl.Series &#124; None):</u> the leading indicator's level, a second driver next to inflation, default None.
- <u>business_cycle_covariate_dates (pl.Series &#124; None):</u> its dates; required with it.

**Returns:**

<u>UnemploymentParams:</u> `mean_reversion_speed`, `long_run_mean`, `inflation_sensitivity`, `volatility`, `initial_value` (the last observed rate) and, with the leading indicator, `business_cycle_sensitivity`.

**Raises:**

- <u>ValueError:</u> if `period` or `source` is not recognized, only one covariate argument is given, no data come back (the OECD sends none after too many requests; retry a minute later), or the history is too short or shows no pull toward a normal level.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.unemployment.unemployment_controller import Unemployment

toolkit = Toolkit(["AAPL"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2000-01-01")
unemployment = Unemployment(toolkit)

unemployment.calibrate("united_states", country="United States", period="quarterly")
```

Which returns (calibrated on 2026-10-05):

| name | mean_reversion_speed | long_run_mean | inflation_sensitivity | volatility | initial_value |
|:-----|---------------------:|--------------:|----------------------:|-----------:|--------------:|
| united_states | 0.5534 | 0.0567 | -0.3432 | 0.0211 | 0.0427 |

US unemployment starts at 4.27% and is pulled toward 5.67%.

## names

```python
unemployment.names  # property -> list[str]
```

The names of every unemployment entry calibrated so far, in calibration order.

## params

```python
params(name: str) -> UnemploymentParams
```

The calibrated parameters for one unemployment entry.

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

## step_function

```python
unemployment.step_function  # property
```

The function that moves unemployment one step: the exact mean-reverting step plus the Phillips-curve term,
shared by every entry.

## changes

```python
changes(name: str) -> pl.DataFrame
```

Dated period-over-period changes in one entry's unemployment rate, from the data `calibrate` already fetched; used
to estimate the correlations between factors.

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

### fit_unemployment_process

```python
fit_unemployment_process(
    unemployment: pl.Series,
    inflation: pl.Series,
    time_step: float,
    business_cycle: pl.Series | None = None,
) -> UnemploymentParams
```

Fit the unemployment process to historical unemployment and inflation series by OLS regression of the change in
unemployment on its own level and the same-period change in inflation, the discretized form of Ahlgrim, D'Arcy
and Gorvett's (2005) Phillips-curve-augmented Ornstein-Uhlenbeck process (their eq. 3.19-3.21).

The formula is as follows:

$$
u(t) - u(t-1) = c + b \cdot u(t-1) + \alpha_{u} \cdot (\pi(t) - \pi(t-1)) + \gamma_{u} \cdot (\operatorname{CLI}(t) - \operatorname{CLI}(t-1)) + e(t)
$$

$$
\kappa_{u} = - \ln(1 + b) / \text{dt},\;\; \mu_{u} = - c / b
$$

Without `business_cycle` the gamma_u term is dropped and the fit is `calibration_model.
fit_ou_process_with_covariate`. With it, the leading indicator's change is a second covariate alongside
inflation (never a replacement), fit through `calibration_model._fit_ou_drift`'s `extra_columns`.

**Args:**

- <u>unemployment (pl.Series):</u> historical unemployment-rate observations, evenly spaced in time.
- <u>inflation (pl.Series):</u> historical inflation-rate observations, the same length and time index as `unemployment`.
- <u>time_step (float):</u> time increment between observations, in years.
- <u>business_cycle (pl.Series &#124; None):</u> the leading indicator's raw historical level series, the same length and time index as `unemployment`/ `inflation` (already date-aligned by the caller; see `unemployment_controller.Unemployment.calibrate`). None (the default) fits the single-covariate (inflation only) process.

**Returns:**

<u>UnemploymentParams:</u> the calibrated mean-reversion speed, long-run mean, inflation sensitivity, volatility, and the series' last value as the simulation starting point, plus `business_cycle_sensitivity` when `business_cycle` was given.

**Raises:**

- <u>ValueError:</u> if the series have different lengths, too few observations remain after jointly dropping nulls, or the fitted mean-reversion speed is non-positive.

**References:**

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Phillips, A.W. (1958). "The Relation Between Unemployment and the Rate of Change of Money Wage Rates in the United Kingdom, 1861-1957." Economica, 25(100), 283-299. <https://doi.org/10.1111/j.1468-0335.1958.tb00003.x>

### step_unemployment

```python
step_unemployment(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: UnemploymentParams,
    inflation_change: np.ndarray | float,
    business_cycle_change: np.ndarray | float | None = None,
) -> np.ndarray
```

Advance the unemployment process by one time step with the exact OU transition plus the per-step covariate terms.
Without `params.business_cycle_sensitivity` this is `calibration_model.step_ou_process_with_covariate`.

The formula is as follows:

$$
u(t + \text{dt}) = \mu_{u} + (u(t) - \mu_{u}) \cdot \exp(- \kappa_{u} \cdot \text{dt}) + \alpha_{u} \cdot d\pi + \gamma_{u} \cdot \text{dCLI} + s \cdot z
$$

$$
s = \sigma_{u} \cdot \sqrt{(1 - \exp(- 2 \cdot \kappa_{u} \cdot \text{dt})) / (2 \cdot \kappa_{u})}
$$

Where dpi and dCLI are the simulated inflation and leading-indicator changes over the same step and z is a
standard normal draw. The result is clipped to [0, 1].

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> the unemployment rate at the current time step.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw for this step.
- <u>time_step (float):</u> the time increment, in years.
- <u>params (UnemploymentParams):</u> calibrated mean-reversion speed, long-run mean, inflation sensitivity, volatility, and (optionally) business-cycle sensitivity.
- <u>inflation_change (np.ndarray &#124; float):</u> the change in the inflation rate over this same step (the already-simulated inflation factor's move this step), the Phillips-curve input.
- <u>business_cycle_change (np.ndarray &#124; float &#124; None):</u> the change in the leading indicator's level over this same step (the already-simulated leading_indicator factor's move this step). Required when `params.business_cycle_sensitivity` is set, unused otherwise.

**Returns:**

<u>np.ndarray:</u> the unemployment rate at the next time step, kept within [0, 1]: a rate is a share of the labour force, and the Gaussian step alone can cross zero in a few paths (about 0.3% of monthly paths in a default run) or, under an extreme inflation belief, pass 100%.

**Raises:**

- <u>ValueError:</u> if `params.business_cycle_sensitivity` is set but `business_cycle_change` is not supplied.

**References:**

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Phillips, A.W. (1958). "The Relation Between Unemployment and the Rate of Change of Money Wage Rates in the United Kingdom, 1861-1957." Economica, 25(100), 283-299. <https://doi.org/10.1111/j.1468-0335.1958.tb00003.x>
