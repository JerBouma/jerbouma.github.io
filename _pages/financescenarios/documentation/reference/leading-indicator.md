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

The Leading Indicator module simulates the OECD Composite Leading Indicator (CLI), an index built to signal turning
points in the business cycle, the alternation of economic expansions and slowdowns, a few months before they show up
in output.

Switch it on (`leading_indicator.enabled: true`) and the simulated scenarios gain one more variable that tracks where
the economy is in its cycle, correlated with every other factor. On its own it does not steer any other factor. Its
second role is as the business-cycle signal other factors can opt into with `condition_on_business_cycle: true`, so
that, for example, credit spreads tend to widen as the indicator turns down.

The model is the mean-reverting Ornstein-Uhlenbeck process the interest rate module uses for its short rate
([Vasicek, 1977](https://doi.org/10.1016/0304-405x(77)90016-2)):

```text
d(CLI) = a * (theta - CLI) * dt + sigma * dW
```

where `a` is the mean-reversion speed, `theta` the long-run level and `sigma` the volatility. Mean reversion holds
almost by construction: the OECD publishes the CLI with its long-run trend removed, scaled to swing around 100.
`volatility_model: garch` lets the size of the swings vary over time, so calm and turbulent periods each persist
([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1)).

A conditioned `interest_rates[i]`, `inflation[i]`, `real_estate`, `credit[i]`, `commodities[i]` or `dividend_yield[i]`
entry gains a pull from the indicator's change:

```text
d(x) = a * (theta - x) * dt + beta * d(CLI) + sigma * dW
```

It is then calibrated at `leading_indicator.period`, which that factor must support (`real_estate` needs quarterly or
yearly), it cannot use `volatility_model: garch`, and its belief overrides do not apply. Equities instead let their
regime-switching probabilities depend on the indicator
([Filardo, 1994](https://doi.org/10.1080/07350015.1994.10524545)), and unemployment adds it as a second driver next to
inflation.

The data come from the Finance Toolkit's `economics.get_composite_leading_indicator`: the OECD's monthly index for
about 22 countries and country groups, no API key needed. It models the index level only, not recession dates or the
probability of a recession.

Configuration (`leading_indicator` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `enabled` | `false` | Adds a `leading_indicator` factor to the simulation when `true`. |
| `country` | `United States` | The country whose indicator is fetched. |
| `currency` | `USD` | A label only: the index has no currency and is never converted. |
| `period` | `monthly` | `monthly`, `quarterly` or `yearly`: the calibration time step. |
| `volatility_model` | `constant` | `constant` or `garch`. |
| `beliefs` | none | Override the fitted speed, long-run level or volatility (constant volatility only). |

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

Calibrate the leading indicator from its history: fetch the OECD Composite Leading Indicator for `country`, then
fit how fast it returns to its normal level (`mean_reversion_speed`), what that level is (`long_run_mean`) and how
much it swings (`volatility`).

This learns how the business-cycle signal has moved, so the simulated scenarios pass through expansions and
slowdowns at a realistic pace. The half-life of a swing is ln 2 / `mean_reversion_speed`: a speed of 0.50 a year
means a dip below 100 has recovered half of the way after about 1.4 years. All values are in index points:
`long_run_mean` is near 100, the level the OECD scales the index to, and `initial_value` is the latest reading,
where every simulated path starts (above 100 means above-trend activity ahead).

The history starts at the Toolkit's `start_date`; the Finance Toolkit's default window is short, so pass an early
`start_date` for a meaningful fit. A second call replaces the first, since a run has one leading indicator.

**Args:**

- <u>country (str):</u> the country to fetch the indicator for. Defaults to "United States".
- <u>period (str):</u> "monthly", "quarterly" or "yearly"; a coarser period averages the monthly data. Defaults to "monthly".
- <u>volatility_model (str):</u> "constant" or "garch". Defaults to "constant".

**Returns:**

<u>OUParams &#124; GARCHParams:</u> the fitted process, including `initial_value`; GARCHParams with "garch".

**Raises:**

- <u>ValueError:</u> if `period` or `volatility_model` is not recognized, or the OECD returns no data, for example when it rate-limits a burst of requests (wait a minute and retry).

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

The US indicator stands at about 100.9, slightly above trend, and is pulled toward 99.7 with a half-life of about
1.4 years on monthly data.

**References:**

- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. <https://doi.org/10.1016/0304-405x(77>)90016-2

## params

```python
leadingindicator.params  # property -> OUParams | GARCHParams
```

The last-calibrated process parameters.

**Raises:**

- <u>RuntimeError:</u> if `calibrate()` has not been called yet.

## step_function

```python
leadingindicator.step_function  # property
```

The function that moves the indicator one time step (the same Ornstein-Uhlenbeck step interest rates use).

## series

```python
leadingindicator.series  # property -> pl.Series
```

The historical indicator levels `calibrate()` fetched. Factors with `condition_on_business_cycle` use them to fit
how they respond to the indicator's change.

**Raises:**

- <u>RuntimeError:</u> if `calibrate()` has not been called yet.

## dates

```python
leadingindicator.dates  # property -> pl.Series
```

The dates of `series`, in the same order, so a conditioned factor can match the indicator to its own history by
date.

**Raises:**

- <u>RuntimeError:</u> if `calibrate()` has not been called yet.

## changes

```python
leadingindicator.changes  # property -> pl.DataFrame
```

Dated period-over-period changes of the indicator, from the data `calibrate()` already fetched, used to estimate
its correlation with the other factors without fetching the data again.

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if `calibrate()` has not been called yet.
