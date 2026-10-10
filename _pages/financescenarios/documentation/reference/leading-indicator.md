---
title: "LeadingIndicator"
seo_title: "LeadingIndicator Reference – Finance Scenarios"
excerpt: "The OECD composite leading indicator."
description: "The OECD composite leading indicator."
author_profile: false
permalink: /projects/financescenarios/docs/reference/leading-indicator
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

The OECD composite leading indicator. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.factors.leading_indicator.leading_indicator_controller import LeadingIndicator
```

```python
LeadingIndicator(toolkit: Toolkit)
```

The Leading Indicator module simulates the OECD Composite Leading Indicator (CLI), an
index built to signal turning points in the business cycle, the alternation of
economic expansions and slowdowns, a few months before they show up in output.

In plain terms: switch it on (`leading_indicator.enabled: true`) and the simulated
scenarios gain one more variable that tracks where the economy is in its cycle,
correlated with every other factor. On its own it is just that, one more
correlation-linked factor like real estate or credit; it does not steer any other
factor. Its second role is as the business-cycle signal other factors can opt into
with `condition_on_business_cycle: true`, so that, for example, credit spreads tend to
widen as the indicator turns down.

The model is the mean-reverting Ornstein-Uhlenbeck process the interest rate module
uses for its short rate ([Vasicek, 1977](https://doi.org/10.1016/0304-405x(77)90016-2)):

```text
d(CLI) = a * (theta - CLI) * dt + sigma * dW
```

where `a` is the mean-reversion speed, `theta` the long-run level and `sigma` the
volatility. Mean reversion is close to true by construction here rather than an
empirical claim: the OECD publishes the CLI already detrended (long-run growth
removed), amplitude-adjusted and normalized to oscillate around a long-run average of
100, unlike a price index or an exchange rate, which trend rather than revert. There
is no `leading_indicator_model.py`: the generic `fit_ou_process` and `step_ou_process`
in `calibration_model` do the work. One option changes the process:
`volatility_model: garch` replaces the fixed volatility with a GARCH(1,1) process, in
which the size of the swings varies over time so calm and turbulent periods each
persist ([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1)); it reuses
the interest rate module's `fit_garch_process` and `GARCHStepper`.

Business-cycle conditioning: `condition_on_business_cycle: true` on an
`interest_rates[i]`, `inflation[i]`, `real_estate`, `credit[i]`, `commodities[i]` or
`dividend_yield[i]` entry adds a drift term on the leading indicator's step-to-step
change, the same shape as unemployment's Phillips-curve term on inflation, shared
through `OUCovariateParams`, `fit_ou_process_with_covariate` and
`step_ou_process_with_covariate` in `calibration_model` rather than duplicated per factor:

```text
d(x) = a * (theta - x) * dt + beta * d(CLI) + sigma * dW
```

The rules for a conditioned entry:
- It requires `leading_indicator.enabled: true`.
- It is calibrated at `leading_indicator.period` instead of its own `period`, because
  the regression needs both series at the same frequency to align them by date (the
  same reason unemployment uses its paired inflation entry's period).
- `leading_indicator.period` must be one that factor supports: `interest_rates` and
  `credit` accept daily to yearly (ticker-sourced rates only; `source: oecd` rate
  entries accept only quarterly or yearly), `inflation` accepts monthly, quarterly or
  yearly, and `real_estate` only quarterly or yearly, so the default
  `leading_indicator.period: monthly` cannot condition `real_estate`.
- It cannot be combined with `volatility_model: garch` on the same factor, which avoids
  a three-way mean-reversion, GARCH and covariate hybrid.
- Belief overrides do not apply to it: `OUCovariateParams` does not map onto
  `OUBeliefs`, so the fit is used as calibrated.

Two factors are conditioned differently. Equity's regime-switching model has no drift
term to add one to, so `equities[i].condition_on_business_cycle` instead makes its
regime transition probabilities a function of the indicator's level, the
time-varying transition probabilities of
[Filardo (1994)](https://doi.org/10.1080/07350015.1994.10524545) (see `Equities`). And
unemployment, which already has an inflation covariate, adds the indicator as a
genuine *second* covariate next to it (see `Unemployment`).

The data come from the Finance Toolkit's `economics.get_composite_leading_indicator`:
the OECD-harmonized, amplitude-adjusted monthly index, no API key needed. Coverage is
about 22 countries and country groups, narrower than most OECD series, and a coarser
`period` averages the monthly data rather than skipping months.

It models the index level only, not recession dates or the probability of a recession.

Configuration (`leading_indicator` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `enabled` | `false` | Adds a `leading_indicator` factor to the simulation when `true`. |
| `country` | `United States` | The country whose indicator is fetched. |
| `currency` | `USD` | The currency the factor is reported under in the reporting registry. |
| `period` | `monthly` | `monthly`, `quarterly` or `yearly`: the calibration time step. |
| `volatility_model` | `constant` | `constant` or `garch`. |
| `beliefs.mean_reversion_speed` | `null` | Override the fitted speed; must be greater than 0. |
| `beliefs.long_run_mean` | `null` | Override the fitted long-run level. |
| `beliefs.volatility` | `null` | Override the fitted volatility; must be greater than 0. |

A belief left as `null` keeps the calibrated value. Beliefs apply only with
`volatility_model: constant`, through `apply_ou_beliefs` in `config_model.py`.

**References:**

- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. <https://doi.org/10.1016/0304-405x(77>)90016-2
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." Journal of Econometrics, 31(3), 307-327. <https://doi.org/10.1016/0304-4076(86>)90063-1
- Filardo, A.J. (1994). "Business-Cycle Phases and Their Transitional Dynamics." Journal of Business & Economic Statistics, 12(3), 299-308. <https://doi.org/10.1080/07350015.1994.10524545>

## calibrate

```python
calibrate(
    country: str = 'United States',
    period: str = 'monthly',
    volatility_model: str = 'constant',
) -> OUParams | GARCHParams
```

Calibrate the leading indicator process from its history: fetch the OECD
Composite Leading Indicator for `country`, and fit how fast it returns to its
normal level (`mean_reversion_speed`), what that normal level is
(`long_run_mean`) and how much it swings (`volatility`).

In plain terms: this learns how the business-cycle signal has moved, so the
simulated scenarios pass through expansions and slowdowns at a realistic pace. The
half-life of a swing is ln 2 / `mean_reversion_speed`: a speed of 0.50 a year means
a dip below 100 has recovered half of the way after about 1.4 years.

All fields are in index points, not decimals: `long_run_mean` near 100 is the
level the OECD normalizes the indicator to, `initial_value` is the latest reading
(the start of every simulated path, above 100 meaning above-trend activity ahead)
and `volatility` is the annualized standard deviation of its shocks in points.
The calibrated level series and its dates stay available as `series` and `dates`,
for the factors that condition on the business cycle.

Also known as: business-cycle indicator calibration, CLI mean-reversion fit.

**Args:**

- <u>country (str):</u> the country to pull the indicator for.
- <u>period (str):</u> sampling frequency for calibration ("monthly", "quarterly", "yearly"). The underlying data itself is always fetched monthly; anything coarser is resampled (pandas mean-resample) before fitting, so dt stays consistent with the actual observation spacing.
- <u>volatility_model (str):</u> "constant" (fixed-volatility OU, the default) or "garch" (GARCH(1,1) time-varying volatility, Bollerslev 1986).

**Returns:**

<u>OUParams &#124; GARCHParams:</u> the calibrated process parameters; GARCHParams only when volatility_model="garch".

**Raises:**

- <u>ValueError:</u> if period or volatility_model is not recognized.

**Notes:**

- The source is always monthly; a `period` of "quarterly" or "yearly" averages it to
  that frequency before fitting, so the time step and the data spacing agree.
- The data start at the `Toolkit`'s `start_date`; the Finance Toolkit's default
  window is short (five years gave 59 monthly readings), so pass an early
  `start_date` for a meaningful fit.
- The OECD API rate-limits bursts of requests (HTTP 429); the Finance Toolkit then
  returns no data and this raises a `ValueError`. Waiting a minute and retrying
  resolves it.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.leading_indicator.leading_indicator_controller import LeadingIndicator

toolkit = Toolkit(["AAPL"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2000-01-01")
leading_indicator = LeadingIndicator(toolkit)

leading_indicator.calibrate(country="United States", period="monthly")
leading_indicator.calibrate(country="United States", period="quarterly")
```

Which returns (calibrated on 2026-10-04):

| period | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-------|---------------------:|--------------:|-----------:|--------------:|
| monthly | 0.5033 | 99.7353 | 1.3512 | 100.9563 |
| quarterly | 0.7928 | 99.7440 | 1.6913 | 100.9243 |

The US indicator stands at about 100.9, slightly above trend, and is pulled toward
99.7 with a half-life of about 1.4 years on monthly data (320 readings from January
2000 to August 2026); averaging to quarters smooths out short reversals and gives a
somewhat faster fitted speed. A second `calibrate` call replaces the first, since
there is one leading indicator per run.

**References:**

- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. <https://doi.org/10.1016/0304-405x(77>)90016-2
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." Journal of Econometrics, 31(3), 307-327. <https://doi.org/10.1016/0304-4076(86>)90063-1

## params

```python
leadingindicator.params  # property -> OUParams | GARCHParams
```

The last-calibrated process parameters.

**Raises:**

- <u>RuntimeError:</u> if calibrate() hasn't been called yet.

## step_function

```python
leadingindicator.step_function  # property
```

The step function for the leading indicator process (`step_ou_process`, shared with interest rates).

## series

```python
leadingindicator.series  # property -> pl.Series
```

The raw historical Composite Leading Indicator level series calibrate()
fetched, used as the business-cycle covariate by other factors'
condition_on_business_cycle option (see calibration_controller.py), which
needs the raw level series (to compute its own step-to-step change), not
just the pre-differenced `.changes`.

**Raises:**

- <u>RuntimeError:</u> if calibrate() hasn't been called yet.

## dates

```python
leadingindicator.dates  # property -> pl.Series
```

The dates paired with `series`, same length and order. Lets a
business-cycle-conditioned factor inner-join `series` against its own
historical dates before fitting (see calibration_controller.py's
`_covariate_dates_for`), rather than pairing the two series
positionally by observation count, which silently mismatches
whenever either series has gaps or a different history length.

**Raises:**

- <u>RuntimeError:</u> if calibrate() hasn't been called yet.

## changes

```python
leadingindicator.changes  # property -> pl.DataFrame
```

Dated period-over-period changes in the leading indicator, from the same
data calibrate() already fetched, reused for cross-factor correlation
estimation (Dependence) instead of triggering a second Finance Toolkit fetch.

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` (pl.Date) and `value` (f64); see helpers.dated_changes().

**Raises:**

- <u>RuntimeError:</u> if calibrate() hasn't been called yet.
