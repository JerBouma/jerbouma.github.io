---
title: "Hjm"
seo_title: "Hjm Reference – Finance Scenarios"
excerpt: "A two-factor Gaussian HJM forward curve."
description: "A two-factor Gaussian HJM forward curve."
author_profile: false
permalink: /projects/financescenarios/docs/reference/hjm
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

A two-factor Gaussian HJM forward curve. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.factors.hjm.hjm_controller import Hjm
```

```python
Hjm(toolkit: Toolkit)
```

The HJM module simulates the whole forward-rate curve with a two-factor Gaussian Heath-Jarrow-Morton model, which
rules out riskless arbitrage between maturities by construction. A forward rate is the interest rate agreed today
for borrowing over a short period that starts at some future date; the forward curve lists those rates for every
start date and carries the same information as the yield curve.

Every other rate factor here, including the `yield_curve` factors of `TermStructure`, learns its drift (the
direction rates tend to move) from how rates mean-reverted in the past. This one does not. Once you choose how
volatile the forward curve is at each maturity, the no-arbitrage condition of
[Heath, Jarrow and Morton (1992)](https://doi.org/10.2307/2951677) fixes the drift, so it is never fitted. Use it
when simulated bond prices across maturities must be consistent with each other, for example to value liabilities
against today's curve; use `yield_curve` when you want curves that behave like history.

Each factor's volatility fades with time to maturity `x` as `sigma_i * exp(-kappa_i * x)`, which makes the model
the two-factor Hull-White or G2++ model ([Hull and White, 1994](https://doi.org/10.3905/jod.1994.407908);
[Brigo and Mercurio, 2006](https://doi.org/10.1007/978-3-540-34604-3)). Its two states, `hjm_factor_1` and
`hjm_factor_2`, start at zero and rebuild the forward rate as

`f(t, x) = f_anchor(t + x) + exp(-kappa_1*x)*x_1(t) + exp(-kappa_2*x)*x_2(t) + Phi(t, x)`

where `f_anchor` is today's forward curve from a [Nelson-Siegel (1987)](https://doi.org/10.1086/296409) fit and
`Phi` a convexity term the no-arbitrage condition supplies. Both states and `Phi` start at zero, so the model
starts exactly on today's curve. It is risk-neutral: with the default zero market price of risk there is no term
premium (the extra yield investors demand for long bonds), unlike the real-world rate factors it may run next to.

To read a simulated 10-year forward rate after a run (`hjm_zero_yield` takes the same inputs and gives a
zero-coupon yield):

```python
import numpy as np

from financescenarios.factors.hjm.hjm_model import hjm_forward_rate

ten_year_paths = hjm_forward_rate(
    result.paths["hjm_factor_1"],
    result.paths["hjm_factor_2"],
    tenor=10.0,
    elapsed_time=np.arange(result.paths["hjm_factor_1"].shape[1]) * config.engine.time_step,
    params=scenarios.hjm.params,
)
```

Configuration (`hjm` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `enabled` | `false` | Adds `hjm_factor_1` and `hjm_factor_2` when `true`. |
| `period` | `daily` | Calibration frequency; sets the time step. |
| `decay` | `0.7308` | Nelson-Siegel decay (lambda) for HJM's own anchor curve. |
| `kappa_bounds` | `(0.01, 6.0)` | Search range for both factors' volatility decay. |
| `beliefs.factor_1`, `.factor_2` | `null` | Override `volatility`, `volatility_decay` or `market_price_of_risk`. |
| `beliefs.factor_correlation` | `null` | Override the fitted correlation, between -1 and 1. |

**References:**

- Heath, D., Jarrow, R., Morton, A. (1992). "Bond Pricing and the Term Structure of Interest Rates: A New Methodology for Contingent Claims Valuation." Econometrica, 60(1), 77-105. <https://doi.org/10.2307/2951677>
- Hull, J., White, A. (1994). "Numerical Procedures for Implementing Term Structure Models II: Two-Factor Models." The Journal of Derivatives, 2(2), 37-48. <https://doi.org/10.3905/jod.1994.407908>
- Brigo, D., Mercurio, F. (2006). "Interest Rate Models: Theory and Practice" (2nd ed.), chapters 3-4. Springer Finance. <https://doi.org/10.1007/978-3-540-34604-3>

## calibrate

```python
calibrate(
    period: str = 'daily',
    decay: float = 0.7308,
    kappa_bounds: tuple[float, float] = (0.01, 6.0),
) -> HjmParams
```

Calibrate the two-factor HJM model from historical treasury yields: each factor's `volatility`, how fast it
fades with maturity (`volatility_decay`) and their `factor_correlation`, plus today's curve as the anchor the
simulation starts from.

This measures how much, and how differently, the short and long ends of the forward curve have moved, as two
sources of movement: a slow-fading one that shifts the whole curve (factor 1) and a fast-fading one that mostly
moves the short end (factor 2). A factor's effect halves every ln 2 / `volatility_decay` years of maturity.
There is no mean-reversion speed or long-run mean to fit: the no-arbitrage condition sets the drift.

The method fits a [Nelson-Siegel (1987)](https://doi.org/10.1086/296409) curve to the four maturities at every
date, takes the covariance of the changes in its forward rates and picks the two-factor model whose covariance
matches it best ([Brigo and Mercurio, 2006](https://doi.org/10.1007/978-3-540-34604-3)).
`covariance_fit_error` says how far apart the two are; above 0.35 a warning is logged.

Also known as: G2++ calibration, two-factor Hull-White calibration, forward-rate volatility fit.

**Args:**

- <u>period (str):</u> data frequency and time step: "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>decay (float):</u> the Nelson-Siegel decay (lambda), annualized, for the historical and anchor curves. Defaults to 0.7308.
- <u>kappa_bounds (tuple[float, float]):</u> the lowest and highest `volatility_decay` searched for both factors. Defaults to (0.01, 6.0); a floor of 0.03 to 0.10 tempers long-horizon convexity.

**Returns:**

<u>HjmParams:</u> the two factors (`factor_1`, `factor_2`), `factor_correlation`, the `anchor` curve and `covariance_fit_error`.

**Raises:**

- <u>ValueError:</u> if `period`, `decay` or `kappa_bounds` is invalid, or fewer than 30 curve changes remain to fit.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.hjm.hjm_controller import Hjm

toolkit = Toolkit(["^IRX", "^FVX", "^TNX", "^TYX"], api_key="FINANCIAL_MODELING_PREP_KEY")
hjm = Hjm(toolkit)

params = hjm.calibrate(period="daily")
```

Which returns (calibrated on 2026-10-04, daily data from 2021-10-06 to 2026-10-02):

| factor | volatility | volatility_decay | variance_share |
|:-------|-----------:|-----------------:|---------------:|
| factor_1 | 0.0132 | 0.0272 | 0.4856 |
| factor_2 | 0.0518 | 1.8637 | 0.4210 |

with `factor_correlation` -0.5346 and `covariance_fit_error` 0.2604: factor 1 barely fades over 30 years,
factor 2 halves within five months, and the two tend to move in opposite directions.

## params

```python
hjm.params  # property -> HjmParams
```

The parameters from the last `calibrate` call.

**Raises:**

- <u>RuntimeError:</u> if `calibrate` has not been called yet.

## step_function

```python
hjm.step_function  # property
```

The step function that moves each HJM state forward one time step, using its exact mean-reverting transition.

## changes

```python
hjm.changes  # property -> dict[str, pl.DataFrame]
```

The dated period-over-period changes of `hjm_factor_1` and `hjm_factor_2` from the last `calibrate` call, from
which the correlation matrix is estimated.

**Returns:**

<u>dict[str, pl.DataFrame]:</u> one table per factor, with a `date` and a `value` column.

**Raises:**

- <u>RuntimeError:</u> if `calibrate` has not been called yet.

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

### hjm_convexity

```python
hjm_convexity(
    elapsed_time: float | np.ndarray,
    tenor: float,
    params: HjmParams,
) -> float | np.ndarray
```

Phi(t, x): the deterministic drift the HJM no-arbitrage condition adds to the forward rate at tenor `x` by time
`t`, derived (not fit) from the two factors' volatility specification. It reads params.factor_correlation, so it
is only arbitrage-free if the simulated shocks of factor_1 and factor_2 are drawn with that same correlation.

The formula is as follows:

$$
\mu(t,\; T) = \sum_{i},\;\; j \rho_{ij} \cdot \sigma_{i}(T - t) \cdot \text{integral}_{t} ^{T} \sigma_{j}(u - t) \text{du}
$$

$$
\sigma_{i}(x) = \sigma_{i} \cdot \exp(- \kappa_{i} \cdot x)
$$

$$
\Phi(t,\; x) = \sum_{i},\;\; j \rho_{ij} \cdot \sigma_{i} \cdot \sigma_{j} / \kappa_{j} \cdot (K(\kappa_{i}) - K(\kappa_{i} + \kappa_{j}))
$$

$$
K(k) = \exp(- k \cdot x) \cdot (1 - \exp(- k \cdot t)) / k
$$

The first line is the Heath, Jarrow and Morton (1992) drift condition for correlated factors; Phi(t, x) is that
drift integrated from 0 to t at a fixed time-to-maturity x = T - t.

**Args:**

- <u>elapsed_time (float &#124; np.ndarray):</u> t, years since the curve was anchored (t=0). Broadcasts against a whole simulated time grid.
- <u>tenor (float):</u> x, time-to-maturity in years (>= 0).
- <u>params (HjmParams):</u> the calibrated 2-factor model.

**Returns:**

<u>float &#124; np.ndarray:</u> Phi(t, x), same shape as `elapsed_time`.

**References:**

- Brigo, D., Mercurio, F. (2006). "Interest Rate Models: Theory and Practice" (2nd ed.), chapter 4: the G2++ phi(t) correction this term generalizes to an arbitrary tenor, not just t itself. Springer Finance. <https://doi.org/10.1007/978-3-540-34604-3>
- Heath, D., Jarrow, R., Morton, A. (1992). "Bond Pricing and the Term Structure of Interest Rates: A New Methodology for Contingent Claims Valuation." Econometrica, 60(1), 77-105. <https://doi.org/10.2307/2951677>

### hjm_forward_rate

```python
hjm_forward_rate(
    state_1: float | np.ndarray,
    state_2: float | np.ndarray,
    tenor: float,
    elapsed_time: float | np.ndarray,
    params: HjmParams,
) -> float | np.ndarray
```

Reconstruct the instantaneous forward rate at time-to-maturity `tenor`, `t`
years after this model was anchored: today's observed curve, evaluated at the
resulting calendar maturity `t + tenor` (the arbitrage-free roll-down), plus
each state's own contribution, plus the deterministic no-arbitrage convexity
term. At t=0 with state_1=state_2=0 (their initial value), this reproduces the
anchor curve exactly; see hjm_convexity and HjmFactorParams.initial_value.

The formula is as follows:

$$
f(t,\; t + x) = \operatorname{f\_anchor}(t + x) + \exp(- \kappa_{1} \cdot x) \cdot x_{1}(t) + \exp(- \kappa_{2} \cdot x) \cdot x_{2}(t) + \Phi(t,\; x)
$$

Where f_anchor is today's Nelson-Siegel forward curve and Phi(t, x) is hjm_convexity.

**Args:**

- <u>state_1 (float &#124; np.ndarray):</u> x_1(t), factor_1's current simulated value.
- <u>state_2 (float &#124; np.ndarray):</u> x_2(t), factor_2's current simulated value.
- <u>tenor (float):</u> x, time-to-maturity in years (>= 0; 0 is the short rate).
- <u>elapsed_time (float &#124; np.ndarray):</u> t, years since t=0.
- <u>params (HjmParams):</u> the calibrated 2-factor model.

**Returns:**

<u>float &#124; np.ndarray:</u> the reconstructed forward rate, broadcast against whichever of state_1/state_2/elapsed_time is array-valued (e.g. full (n_simulations, n_steps + 1) simulated paths against a time grid).

**References:**

- Heath, D., Jarrow, R., Morton, A. (1992). "Bond Pricing and the Term Structure of Interest Rates: A New Methodology for Contingent Claims Valuation." Econometrica, 60(1), 77-105. <https://doi.org/10.2307/2951677>
- Brigo, D., Mercurio, F. (2006). "Interest Rate Models: Theory and Practice" (2nd ed.), chapters 3-4. Springer Finance. <https://doi.org/10.1007/978-3-540-34604-3>

### hjm_zero_yield

```python
hjm_zero_yield(
    state_1: float | np.ndarray,
    state_2: float | np.ndarray,
    tenor: float,
    elapsed_time: float | np.ndarray,
    params: HjmParams,
) -> float | np.ndarray
```

Reconstruct the continuously-compounded zero-coupon yield to `tenor`, `t` years
after this model was anchored: the closed-form average of hjm_forward_rate
over [t, t+tenor], for discount-factor and curve-shape (e.g. inversion)
consumers that want a yield rather than an instantaneous forward.

The formula is as follows:

$$
y(t,\; m) = (\operatorname{F\_anchor}(t + m) - \operatorname{F\_anchor}(t)) / m + \sum_{i} B_{i} (m) \cdot x_{i}(t) + (1 / m) \cdot \text{integral}_{0} ^{m} \Phi(t,\; u) \text{du}
$$

$$
B_{i}(m) = (1 - \exp(- \kappa_{i} \cdot m)) / (\kappa_{i} \cdot m)
$$

Where m is `tenor` and F_anchor is the integral of today's forward curve (nelson_siegel_forward_integral).

**Args:**

- <u>state_1 (float &#124; np.ndarray):</u> x_1(t), factor_1's current simulated value.
- <u>state_2 (float &#124; np.ndarray):</u> x_2(t), factor_2's current simulated value.
- <u>tenor (float):</u> the maturity, in years (must be > 0).
- <u>elapsed_time (float &#124; np.ndarray):</u> t, years since t=0.
- <u>params (HjmParams):</u> the calibrated 2-factor model.

**Returns:**

<u>float &#124; np.ndarray:</u> the reconstructed yield, broadcast against whichever of state_1/state_2/elapsed_time is array-valued.

**Raises:**

- <u>ValueError:</u> if tenor is not strictly positive.

**References:**

- Brigo, D., Mercurio, F. (2006). "Interest Rate Models: Theory and Practice" (2nd ed.), chapters 3-4. Springer Finance. <https://doi.org/10.1007/978-3-540-34604-3>

### step_hjm_factor

```python
step_hjm_factor(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: HjmFactorParams,
) -> np.ndarray
```

Advance one HJM state factor by one time step via its *exact* discrete-time
transition (a plain Vasicek/OU transition, see calibration_model.
step_ou_process, with a long-run mean derived from the market price of risk
rather than independently fit), not an Euler-Maruyama approximation.

The formula is as follows:

$$
x(t + \text{dt}) = m + (x(t) - m) \cdot \exp(- \kappa \cdot \text{dt}) + \sigma \cdot \sqrt{(1 - \exp(- 2 \cdot \kappa \cdot \text{dt})) / (2 \cdot \kappa)} \cdot z
$$

$$
m = \sigma \cdot \lambda / \kappa
$$

Where lambda is the market price of risk (0 under the risk-neutral measure, so m = 0) and z a standard normal draw.

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> the factor's value at the current time step.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw for this step.
- <u>time_step (float):</u> the time increment, in years.
- <u>params (HjmFactorParams):</u> this factor's calibrated volatility/decay/ market-price-of-risk.

**Returns:**

<u>np.ndarray:</u> the factor's value at the next time step.

**References:**

- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. <https://doi.org/10.1016/0304-405x(77>)90016-2
