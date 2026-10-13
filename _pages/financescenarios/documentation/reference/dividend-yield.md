---
title: "DividendYield"
seo_title: "DividendYield Reference – Finance Scenarios"
excerpt: "Dividend yields, one per ticker."
description: "Dividend yields, one per ticker."
author_profile: false
permalink: /projects/financescenarios/docs/reference/dividend-yield
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Dividend yields, one per ticker. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.factors.dividend_yield.dividend_yield_controller import DividendYield
```

```python
DividendYield(toolkit: Toolkit)
```

The Dividend Yield module simulates the dividend yield of a stock or fund: the dividends it paid over the past year
divided by its current price.

A yield rises when prices fall or payouts grow, and over long stretches it tends to drift back toward a typical level.
Each entry in `dividend_yield` (empty by default), such as SPY, becomes a simulated variable linked to the other
factors through the correlation matrix. That matters for pension and income planning, where dividend income is its own
cash-flow input.

The model comes from Ahlgrim, D'Arcy and Gorvett
([2005](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf)) (eq. 3.17): the log yield is
pulled back toward a normal level,

```text
d(log y) = kappa * (mu - log y) * dt + sigma * dW
```

where `kappa` is the speed of the pull, `exp(mu)` the normal yield and `sigma` the size of the swings. Working in logs
keeps the yield positive. The authors found the pull close to zero over 1871-2003, so a history without mean reversion
raises an error.

Three options change the model; only one can be used at a time:

- `condition_on_inflation` adds the inflation term of Wilkie (1986): the yield also moves with a named inflation
  entry. It is the dividend yield step of the Wilkie model (`factor-sets/wilkie.yaml`) that `DividendGrowth` builds
  on.
- `volatility_model="garch"` lets the size of the swings vary over time, so calm and volatile spells each persist
  ([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1)).
- `condition_on_business_cycle` makes the yield move with the leading indicator (requires
  `leading_indicator.enabled: true`).

Data: the Finance Toolkit has no dividend yield series, so it is derived from daily prices: the `Dividends` paid over
the trailing `window` trading days divided by the raw `Close` (not `Adj Close`, which already includes dividends). A
ticker that pays no dividends raises an error. Use Yahoo Finance (no API key): the Financial Modeling Prep Free plan
returns only the last five payments, too few for a trailing-year yield.

Configuration (`dividend_yield[i]` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `name` | `dividend_yield` | Name in the output. |
| `ticker` | `SPY` | A dividend-paying ticker. |
| `currency` | `USD` | Reporting label. |
| `window` | `252` | Trading days of dividends summed for one yield (about a year). |
| `period` | `daily` | `daily`, `weekly`, `monthly`, `quarterly` or `yearly`. |
| `condition_on_inflation` | `false` | Add Wilkie's inflation term. |
| `inflation_name` | `inflation` | The `inflation[i].name` that term reads. |
| `volatility_model` | `constant` | Or `garch`. |
| `condition_on_business_cycle` | `false` | Follow the leading indicator. |
| `beliefs.<field>` | `null` | Override `mean_reversion_speed`, `long_run_mean` or `volatility`. |

A belief's `long_run_mean` is a log yield: a 2% target is `log(0.02)`, about -3.9.

**References:**

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92, eq. 3.17. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>

## calibrate

```python
calibrate(
    name: str,
    ticker: str = 'SPY',
    window: int = 252,
    period: str = 'daily',
    inflation_covariate: pl.Series | None = None,
    volatility_model: str = 'constant',
    business_cycle_covariate: pl.Series | None = None,
    business_cycle_covariate_dates: pl.Series | None = None,
) -> DividendYieldParams | GARCHParams | OUCovariateParams
```

Calibrate one ticker's dividend yield: how fast its logarithm returns to a normal level (`mean_reversion_speed`),
that level (`long_run_mean`) and how much it swings (`volatility`).

A speed of 0.15 a year halves a gap from the normal level in about 4.6 years (ln 2 / 0.15). `exp(long_run_mean)`
is the normal yield and `initial_value` is today's yield (0.0099 is 0.99%).

Each day's yield is the `Dividends` of the last `window` trading days divided by that day's `Close`, averaged per
`period`; the log yield is then fitted by ordinary least squares, following Ahlgrim, D'Arcy and Gorvett
([2005](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf)). Without mean reversion
it raises; a longer history or a coarser `period` usually helps.

**Args:**

- <u>name (str):</u> the entry's name.
- <u>ticker (str):</u> any dividend-paying ticker in the Toolkit. Defaults to "SPY".
- <u>window (int):</u> trading days of dividends summed for one yield, about a year. Defaults to 252.
- <u>period (str):</u> the fit's time step, "daily" to "yearly". Defaults to "daily".
- <u>inflation_covariate (pl.Series &#124; None):</u> a paired inflation entry's history at the same period, adding the inflation term of Wilkie ([1986](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf)). Defaults to None.
- <u>volatility_model (str):</u> "constant", or "garch" for swings whose size varies. Defaults to "constant".
- <u>business_cycle_covariate (pl.Series &#124; None):</u> a leading indicator's history (`LeadingIndicator.series`) for the yield to follow. Defaults to None.
- <u>business_cycle_covariate_dates (pl.Series &#124; None):</u> the dates of `business_cycle_covariate`, required with it. Defaults to None.

**Returns:**

<u>DividendYieldParams &#124; GARCHParams &#124; OUCovariateParams:</u> `mean_reversion_speed`, `long_run_mean`, `volatility` and `initial_value` (plus `inflation_sensitivity` with an inflation covariate).

**Raises:**

- <u>ValueError:</u> if an option is not recognised or combined with another, `window` is not positive, the ticker has no price or dividend data, or the yield is not positive or does not mean-revert.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.dividend_yield.dividend_yield_controller import DividendYield

toolkit = Toolkit(["SPY", "JNJ"], start_date="1995-01-01", benchmark_ticker=None)
dividend_yield = DividendYield(toolkit)

dividend_yield.calibrate("spy_yield", ticker="SPY", period="monthly")
dividend_yield.calibrate("jnj_yield", ticker="JNJ", period="monthly")
```

Which returns (calibrated on 2026-10-04):

| name | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-----|---------------------:|--------------:|-----------:|--------------:|
| spy_yield | 0.1481 | -4.2784 | 0.1525 | 0.0099 |
| jnj_yield | 0.1281 | -3.7328 | 0.1638 | 0.0205 |

SPY yields 0.99% today and is pulled toward exp(-4.2784) = 1.39%.

## names

```python
dividendyield.names  # property -> list[str]
```

The names of every dividend yield entry calibrated so far, in calibration order.

## params

```python
params(name: str) -> DividendYieldParams | GARCHParams | OUCovariateParams
```

The calibrated parameters of one dividend yield entry.

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if `name` has not been calibrated yet.

## step_function

```python
dividendyield.step_function  # property
```

The function that moves a dividend yield one time step forward in the simulation, shared by every entry.

## series

```python
series(name: str) -> pl.Series
```

The historical trailing dividend yield one entry was calibrated on, as a decimal rather than its log.
`DividendGrowth` uses it to rebuild this yield's past surprises.

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if `name` has not been calibrated yet.

## time_step

```python
time_step(name: str) -> float
```

The time step, in years, between the observations one entry was calibrated on (1/12 for monthly). Used with
`series` to rebuild the yield's past surprises.

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if `name` has not been calibrated yet.

## changes

```python
changes(name: str) -> pl.DataFrame
```

The dated period-to-period changes in one entry's log yield, from the data `calibrate` already fetched. The
correlation matrix is estimated from these.

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if `name` has not been calibrated yet.

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

### step_dividend_yield_process

```python
step_dividend_yield_process(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: DividendYieldParams,
    inflation_change: np.ndarray | float = 0.0,
) -> np.ndarray
```

Advance the trailing dividend yield by one time step with the exact OU transition of the log yield (see
`log_yield_drift`), exponentiated back to a yield. `current_value` and the result are actual (decimal) yields;
the log transform is internal, matching `step_commodity_process`.

The formula is as follows:

$$
\text{ln}\; y (t + \text{dt}) = \text{ln}\; y (t) + (\mu - \text{ln}\; y (t)) \cdot (1 - \exp(- \kappa \cdot \text{dt})) + w \cdot d(\text{inflation}) + s \cdot z
$$

$$
s = \sigma \cdot \sqrt{(1 - \exp(- 2 \cdot \kappa \cdot \text{dt})) / (2 \cdot \kappa)}
$$

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> the trailing yield at the current time step (> 0).
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw for this step.
- <u>time_step (float):</u> the time increment, in years.
- <u>params (DividendYieldParams):</u> calibrated mean-reversion speed, long-run log-yield level, log-yield volatility, and (if conditioned) inflation_sensitivity.
- <u>inflation_change (float):</u> the change in the already-simulated inflation factor over this same step. Unused (and harmless to pass as 0.0) when `params.inflation_sensitivity` is None.

**Returns:**

<u>np.ndarray:</u> the trailing yield at the next time step. Always strictly positive.

**References:**

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92, eq. 3.17. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
