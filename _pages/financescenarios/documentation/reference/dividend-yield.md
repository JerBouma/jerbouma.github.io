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

Dividend yields, one per ticker.

```python
from financescenarios.factors.dividend_yield.dividend_yield_controller import DividendYield
```

Simulate the dividend yield of a stock or fund: the dividends it paid over the past year divided by its current
price.

A yield rises when prices fall or payouts grow, and over long stretches it drifts back toward a typical level: a
market priced cheaply against its dividends tends to re-rate, a dear one to cheapen. Simulating the yield gives
dividend income its own path, which matters for pension and income planning, and, in the Wilkie model, it is half
of what sets the equity price. Each entry, such as SPY, is linked to the other factors through the correlation
matrix.

The model comes from Ahlgrim, D'Arcy and Gorvett
([2005](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf)) (eq. 3.17): the log yield is
pulled back toward a normal level,

```text
d(log y) = kappa * (mu - log y) * dt + sigma * dW
```

where `kappa` is the speed of the pull, `exp(mu)` the normal yield and `sigma` the size of the swings. Working in logs
keeps the yield positive and makes its swings proportional to its level, so a 1% yield moves less in absolute terms
than a 5% one. The pull is slow: the authors find a mean reversion speed not significantly different from
zero, so yields can stay far from normal for years. A history with no pull at all raises an error.

Three options change the model; only one can be used at a time:

- `condition_on_inflation` adds the inflation term of Wilkie (1986): the yield also moves with a named inflation
  entry, so higher inflation pushes yields up and prices down. It is the dividend yield of the Wilkie model (the
  `wilkie` factor set) that `DividendGrowth` builds on.
- `volatility_model="garch"` lets the size of the swings vary over time, so calm and volatile spells each persist
  ([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1)).
- `condition_on_business_cycle` makes the yield move with the leading indicator (requires
  `leading_indicator.enabled: true`).

Data: the dividends paid over the trailing `window` trading days divided by the unadjusted closing price, from the
Finance Toolkit. A ticker that pays no dividends raises an error. Use Yahoo Finance (no API key): the Financial
Modeling Prep Free plan returns only the last five payments, too few for a trailing-year yield.

The `dividend_yield[i]` keys of a factor set and their defaults are listed on the reference page
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/reference/configuration-classes).

A belief's `long_run_mean` is a log yield: a 2% target is `log(0.02)`, about -3.9.

**References:**

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92, eq. 3.17. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
DividendYield(toolkit: Toolkit)
```

</details>

## calibrate

Calibrate one ticker's dividend yield: how fast its logarithm returns to a normal level (`mean_reversion_speed`),
that level (`long_run_mean`) and how much it swings (`volatility`).

A speed of 0.15 a year halves a gap from the normal level in about 4.6 years (ln 2 / 0.15), so scenarios that
start from an unusually low yield, as today's US market does, drift back up only slowly: yield, and with it
dividend income per unit invested, stays low for years. `exp(long_run_mean)` is the normal yield and
`initial_value` today's yield (0.0099 is 0.99%).

Each day's yield is the dividends of the last `window` trading days divided by that day's price, averaged per
`period`; the log yield is then fitted by ordinary least squares, following Ahlgrim, D'Arcy and Gorvett
([2005](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf)). Without mean reversion
it raises; a longer history or a coarser `period` usually helps.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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

</details>

## names

The names of every dividend yield entry calibrated so far, in calibration order.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
dividendyield.names  # property -> list[str]
```

</details>

## params

The calibrated parameters of one dividend yield entry.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
params(name: str) -> DividendYieldParams | GARCHParams | OUCovariateParams
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if `name` has not been calibrated yet.

</details>

## step_function

The step that moves a dividend yield forward: its log is pulled toward the normal level and shocked.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
dividendyield.step_function  # property
```

</details>

## series

The historical trailing dividend yield one entry was calibrated on, as a decimal. `DividendGrowth` uses it to
rebuild this yield's past surprises.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
series(name: str) -> pl.Series
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if `name` has not been calibrated yet.

</details>

## time_step

The time step, in years, between the observations one entry was calibrated on (1/12 for monthly). Used with
`series` to rebuild the yield's past surprises.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
time_step(name: str) -> float
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if `name` has not been calibrated yet.

</details>

## changes

The historical changes in one entry's log yield, by date, from which its correlations with the other factors
are estimated.

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

- <u>RuntimeError:</u> if `name` has not been calibrated yet.

</details>

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

### fit_dividend_yield_process

Fit Ahlgrim/D'Arcy/Gorvett's (2005) mean-reverting log-dividend-yield process (eq. 3.17) to a historical
trailing-yield series: the discretized-OU OLS regression of `calibration_model.fit_ou_process`, run on the *log*
yield, as `fit_commodity_process` does for a spot price. Passing `inflation` adds Wilkie's (1986) inflation term
as an extra regression column. The slope maps to the exact OU transition, so a simulation at a coarser step than
the data stays stable.

The formula is as follows:

$$
\text{ln}\; y (t) - \text{ln}\; y (t-1) = c + b \cdot \text{ln}\; y (t-1) + w \cdot (\pi(t) - \pi(t-1)) + e(t)
$$

$$
\kappa = - \ln(1 + b) / \text{dt}
$$

$$
\mu = - c / b
$$

$$
\sigma = \operatorname{std}(e) / \sqrt{(1 - \exp(- 2 \cdot \kappa \cdot \text{dt})) / (2 \cdot \kappa)}
$$

Where pi is the inflation rate (the w term only when `inflation` is given) and std(e) the residual standard
deviation, with one degree of freedom per fitted coefficient.

**References:**

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92, eq. 3.17. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. Share dividend yield equation. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>
- Schwartz, E.S. (1997). "The Stochastic Behavior of Commodity Prices: Implications for Valuation and Hedging." Journal of Finance, 52(3), 923-973. The same log-space OLS fit. <https://doi.org/10.1111/j.1540-6261.1997.tb02721.x>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_dividend_yield_process(
    yields: pl.Series,
    time_step: float,
    inflation: pl.Series | None = None,
) -> DividendYieldParams
```

**Args:**

- <u>yields (pl.Series):</u> historical trailing dividend-yield observations, evenly spaced in time, all > 0.
- <u>time_step (float):</u> time increment between observations, in years.
- <u>inflation (pl.Series &#124; None):</u> historical inflation-rate observations, the same length and time index as `yields`. When supplied, adds Wilkie's inflation-sensitivity term to the fit.

**Returns:**

<u>DividendYieldParams:</u> the calibrated mean-reversion speed, long-run log-yield level, log-yield volatility, and the series' last (actual, not log) value as the simulation starting point. `inflation_sensitivity` is set only when `inflation` was supplied.

**Raises:**

- <u>ValueError:</u> if fewer than `MINIMUM_OBSERVATIONS_OU` observations are supplied, any observation is not strictly positive, `inflation` is supplied with a different length than `yields`, or the fitted mean-reversion speed is non-positive (the series shows no mean reversion at this time step; Ahlgrim/D'Arcy/Gorvett's own finding that dividend yield sits close to a random walk means this is a real possibility, not just an edge case).

</details>

### reconstruct_dividend_yield_residuals

Recover this process's own realised shock at every historical step: the actual log-yield change minus the
drift `step_dividend_yield_process` applies. Runs store levels, not shocks, so a consumer that needs the
dividend yield's own shock (Wilkie's (1986) YE(t-1) in the dividend index model) rebuilds it this way.

The formula is as follows:

$$
\operatorname{YE}(t) = \text{ln}\; y (t) - \text{ln}\; y (t-1) - (\mu - \text{ln}\; y (t-1)) \cdot (1 - \exp(- \kappa \cdot \text{dt})) - w \cdot (\pi(t) - \pi(t-1))
$$

Where the w term applies only when `params` were conditioned on inflation.

**References:**

- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. The YE(t) yield residual in the dividend equation. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
reconstruct_dividend_yield_residuals(
    yields: pl.Series,
    params: DividendYieldParams,
    time_step: float,
    inflation: pl.Series | None = None,
) -> np.ndarray
```

**Args:**

- <u>yields (pl.Series):</u> the same historical trailing-yield series `params` was fit from (or a like-for-like series at the same period/dt).
- <u>params (DividendYieldParams):</u> this process's calibrated parameters.
- <u>time_step (float):</u> the time increment between observations, in years; must match what `params` was fit with.
- <u>inflation (pl.Series &#124; None):</u> the same inflation series `params` was conditioned on, if `params.inflation_sensitivity is not None`. Must be the same length as `yields`.

**Returns:**

<u>np.ndarray:</u> one residual per step-to-step transition, length `yields.len() - 1`; index i is the shock realised moving from observation i to observation i+1.

**Raises:**

- <u>ValueError:</u> if `inflation` is required (params.inflation_sensitivity is not None) but not supplied, or supplied with a different length than `yields`.

</details>

### step_dividend_yield_process

Move a dividend yield one step forward: its logarithm is pulled toward the normal level and shocked, as in
Ahlgrim, D'Arcy and Gorvett (2005).

Modeling the log keeps the yield positive and makes its swings proportional to its level, so the simulated
yield is lognormal around its normal value: it can spike after a market fall but never turns negative. The
pull is slow, so a low starting yield stays low for years in most scenarios. The step is exact, so the
result does not depend on the step size. With the Wilkie inflation term, a rise in inflation over the step
lifts the yield by `w` times that rise, the channel through which inflation lowers equity prices in the
Wilkie model.

The formula is as follows:

$$
\text{ln}\; y (t + \text{dt}) = \text{ln}\; y (t) + (\mu - \text{ln}\; y (t)) \cdot (1 - \exp(- \kappa \cdot \text{dt})) + w \cdot d(\text{inflation}) + s \cdot z
$$

$$
s = \sigma \cdot \sqrt{(1 - \exp(- 2 \cdot \kappa \cdot \text{dt})) / (2 \cdot \kappa)}
$$

Where kappa is `mean_reversion_speed`, mu `long_run_mean` (a log yield), sigma `volatility`, w
`inflation_sensitivity` and z the yield's correlated standard normal shock.

**References:**

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92, eq. 3.17. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_dividend_yield_process(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: DividendYieldParams,
    inflation_change: np.ndarray | float = 0.0,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's dividend yield in each scenario, as a decimal.
- <u>shock (np.ndarray &#124; float):</u> the yield's correlated standard normal shock for this step.
- <u>time_step (float):</u> the step length, in years.
- <u>params (DividendYieldParams):</u> the calibrated reversion speed, normal log yield, volatility and, with the Wilkie term, the inflation sensitivity.
- <u>inflation_change (np.ndarray &#124; float):</u> the change in simulated inflation over the step; only used with the Wilkie term.

**Returns:**

<u>np.ndarray:</u> the dividend yield at the end of the step, always positive.

</details>
