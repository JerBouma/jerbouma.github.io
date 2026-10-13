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

Unemployment rates, each paired with an inflation entry.

```python
from financescenarios.factors.unemployment.unemployment_controller import Unemployment
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

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Unemployment(toolkit: Toolkit)
```

</details>

## calibrate

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(
    name: str,
    country: str = 'United States',
    period: str = 'yearly',
    source: str = 'oecd',
    business_cycle_covariate: pl.Series | None = None,
    business_cycle_covariate_dates: pl.Series | None = None,
    inflation: pl.Series | None = None,
    inflation_dates: pl.Series | None = None,
) -> UnemploymentParams
```

**Args:**

- <u>name (str):</u> the entry's name, e.g. "united_states".
- <u>country (str):</u> the country for both data series, default "United States".
- <u>period (str):</u> data frequency: "yearly" (default), "quarterly" or "monthly"; only "yearly" for "gmdb". A configured run uses the paired inflation entry's period.
- <u>source (str):</u> "oecd" (default) or "gmdb" (the Global Macro Database, for countries outside the OECD).
- <u>business_cycle_covariate (pl.Series &#124; None):</u> the leading indicator's level, a second driver next to inflation, default None.
- <u>business_cycle_covariate_dates (pl.Series &#124; None):</u> its dates; required with it.
- <u>inflation (pl.Series &#124; None):</u> an already-fetched year-over-year inflation rate for `country` at `period` (as decimals, e.g. `Inflation.series(name)`), to skip fetching it again; default None fetches it.
- <u>inflation_dates (pl.Series &#124; None):</u> its dates; required with it.

**Returns:**

<u>UnemploymentParams:</u> `mean_reversion_speed`, `long_run_mean`, `inflation_sensitivity`, `volatility`, `initial_value` (the last observed rate) and, with the leading indicator, `business_cycle_sensitivity`.

**Raises:**

- <u>ValueError:</u> if `period` or `source` is not recognized, a series is given without its dates, no data come back (the OECD sends none after too many requests; retry a minute later), or the history is too short or shows no pull toward a normal level.

</details>

## names

The names of every unemployment entry calibrated so far, in calibration order.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
unemployment.names  # property -> list[str]
```

</details>

## params

The calibrated parameters for one unemployment entry.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
params(name: str) -> UnemploymentParams
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

</details>

## step_function

The one-step unemployment update: the exact mean-reverting step plus the Phillips-curve term.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
unemployment.step_function  # property
```

</details>

## changes

Dated period-over-period changes in one entry's unemployment rate: the history its correlations with the other
factors are estimated from.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
changes(name: str) -> pl.DataFrame
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

</details>

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

### fit_unemployment_process

Estimate how unemployment returns to its normal level and how it moves with inflation, from a country's history.

The model is the Phillips-curve-augmented mean-reverting process of Ahlgrim, D'Arcy and Gorvett (2005), eq.
3.19-3.21. It assumes unemployment is pulled toward a natural rate (frictional and structural unemployment that
persists through the cycle) and that a rise in inflation comes with a tighter labour market, as Phillips (1958)
found for UK wages. The fit is one regression of each period's change in unemployment on its previous level and the
same period's change in inflation: the level term gives the speed and the natural rate, the inflation term the
Phillips-curve sensitivity alpha_u, expected to be negative. With a business-cycle series, the leading indicator's
change enters as a second driver next to inflation, never in its place.

The formula is as follows:

$$
u(t) - u(t-1) = c + b \cdot u(t-1) + \alpha_{u} \cdot (\pi(t) - \pi(t-1)) + \gamma_{u} \cdot (\operatorname{CLI}(t) - \operatorname{CLI}(t-1)) + e(t)
$$

$$
\kappa_{u} = - \ln(1 + b) / \text{dt},\;\; \mu_{u} = - c / b
$$

Without a business-cycle series the gamma_u term is dropped. The Phillips curve is a statistical link fitted to
history; it has flattened in many countries since the 1990s, so expect a small sensitivity on recent data.

**References:**

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Phillips, A.W. (1958). "The Relation Between Unemployment and the Rate of Change of Money Wage Rates in the United Kingdom, 1861-1957." Economica, 25(100), 283-299. <https://doi.org/10.1111/j.1468-0335.1958.tb00003.x>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_unemployment_process(
    unemployment: pl.Series,
    inflation: pl.Series,
    time_step: float,
    business_cycle: pl.Series | None = None,
) -> UnemploymentParams
```

**Args:**

- <u>unemployment (pl.Series):</u> the historical unemployment rate, evenly spaced.
- <u>inflation (pl.Series):</u> the historical inflation rate on the same dates.
- <u>time_step (float):</u> the time between observations, in years.
- <u>business_cycle (pl.Series &#124; None):</u> the leading indicator's level on the same dates, a second driver next to inflation; None (the default) uses inflation only.

**Returns:**

<u>UnemploymentParams:</u> the reversion speed, natural rate, inflation sensitivity, volatility and the latest rate as the starting point, plus `business_cycle_sensitivity` with a business-cycle series.

**Raises:**

- <u>ValueError:</u> if the series differ in length, too few dates have both values, or unemployment shows no pull toward a normal level.

</details>

### step_unemployment

Move the unemployment rate one step forward: pulled toward its natural rate and pushed by the simulated change in
inflation (and, if configured, in the leading indicator).

Because the inflation term uses the same scenario's simulated inflation move, unemployment and inflation stay
linked path by path: an inflation surge tends to come with falling unemployment, and a disinflation with rising
unemployment, on top of whatever correlation their own shocks have. The mean-reverting part uses the exact
transition, so a gap to the natural rate halves in ln(2) / kappa_u years whatever the step size.

The formula is as follows:

$$
u(t + \text{dt}) = \mu_{u} + (u(t) - \mu_{u}) \cdot \exp(- \kappa_{u} \cdot \text{dt}) + \alpha_{u} \cdot d\pi + \gamma_{u} \cdot \text{dCLI} + s \cdot z
$$

$$
s = \sigma_{u} \cdot \sqrt{(1 - \exp(- 2 \cdot \kappa_{u} \cdot \text{dt})) / (2 \cdot \kappa_{u})}
$$

Where dpi and dCLI are the simulated inflation and leading-indicator changes over the same step and z is a
standard normal draw. The result is clipped to [0, 1], since a rate is a share of the labour force: the normal
shock alone could push a few paths (about 0.3% of monthly paths in a default run) below zero.

**References:**

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Phillips, A.W. (1958). "The Relation Between Unemployment and the Rate of Change of Money Wage Rates in the United Kingdom, 1861-1957." Economica, 25(100), 283-299. <https://doi.org/10.1111/j.1468-0335.1958.tb00003.x>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's unemployment rate.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw.
- <u>time_step (float):</u> the step length, in years.
- <u>params (UnemploymentParams):</u> the reversion speed, natural rate, inflation sensitivity, volatility and, if fitted, the business-cycle sensitivity.
- <u>inflation_change (np.ndarray &#124; float):</u> the simulated change in inflation over the same step.
- <u>business_cycle_change (np.ndarray &#124; float &#124; None):</u> the simulated change in the leading indicator over the same step; required when a business-cycle sensitivity was fitted.

**Returns:**

<u>np.ndarray:</u> the unemployment rate one step later, between 0 and 1.

**Raises:**

- <u>ValueError:</u> if a business-cycle sensitivity was fitted but no leading-indicator change is given.

</details>
