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

A two-factor Gaussian HJM forward curve.

```python
from financescenarios.factors.hjm.hjm_controller import Hjm
```

{% raw %}
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

Each factor's volatility fades with time to maturity `x`, which makes the model the two-factor Hull-White or G2++
model ([Hull and White, 1994](https://doi.org/10.3905/jod.1994.407908);
[Brigo and Mercurio, 2006](https://doi.org/10.1007/978-3-540-34604-3)). Its two states, `hjm_factor_1` and
`hjm_factor_2`, start at zero and rebuild the forward rate.

The formula is as follows:

$$
\sigma_{i}(x) = \sigma_{i} \cdot \exp(- \kappa_{i} \cdot x)
$$

$$
f(t,\; x) = f_{\text{anchor}}(t + x) + \exp(- \kappa_{1} \cdot x) \cdot x_{1}(t) + \exp(- \kappa_{2} \cdot x) \cdot x_{2}(t) + \Phi(t,\; x)
$$

Where `f_anchor` is today's forward curve from a [Nelson-Siegel (1987)](https://doi.org/10.1086/296409) fit and
`Phi` a convexity term the no-arbitrage condition supplies. Both states and `Phi` start at zero, so the model
starts exactly on today's curve. It is risk-neutral: with the default zero market price of risk there is no term
premium (the extra yield investors demand for long bonds), unlike the real-world rate factors it may run next to.
The factors are Gaussian, so forward rates can go negative, and the slow first factor (see `calibrate`) settles
only over decades, so the spread of long rates keeps widening for a long time: suited to valuation, less so to a
long real-world projection.

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

The `hjm` keys of a factor set and their defaults are listed on the reference page
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/reference/configuration-classes).

**References:**

- Heath, D., Jarrow, R., Morton, A. (1992). "Bond Pricing and the Term Structure of Interest Rates: A New Methodology for Contingent Claims Valuation." Econometrica, 60(1), 77-105. <https://doi.org/10.2307/2951677>
- Hull, J., White, A. (1994). "Numerical Procedures for Implementing Term Structure Models II: Two-Factor Models." The Journal of Derivatives, 2(2), 37-48. <https://doi.org/10.3905/jod.1994.407908>
- Brigo, D., Mercurio, F. (2006). "Interest Rate Models: Theory and Practice" (2nd ed.), chapters 3-4. Springer Finance. <https://doi.org/10.1007/978-3-540-34604-3>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Hjm(toolkit: Toolkit)
```

</details>
{% endraw %}

## calibrate

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

Two factors are the minimum that lets short and long rates move imperfectly together: with one, every maturity
moves in lockstep and a curve can never steepen in one scenario and flatten in another. This is the G2++, or
two-factor Hull-White, calibration to historical forward-rate volatility.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(
    period: str = 'daily',
    decay: float = 0.7308,
    kappa_bounds: tuple[float, float] = (0.01, 6.0),
) -> HjmParams
```

**Args:**

- <u>period (str):</u> data frequency and time step: "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>decay (float):</u> the Nelson-Siegel decay (lambda), annualized, for the historical and anchor curves. Defaults to 0.7308, from Diebold and Li (2006, section 3 of NBER w10048): "The λ value that maximizes the loading on the medium-term factor at exactly 30 months is λ=0.0609"; 0.0609 a month × 12 = 0.7308 a year.
- <u>kappa_bounds (tuple[float, float]):</u> the lowest and highest `volatility_decay` searched for both factors. Defaults to (0.01, 6.0), a judgement; a floor of 0.03 to 0.10 tempers long-horizon convexity.

**Returns:**

<u>HjmParams:</u> the two factors (`factor_1`, `factor_2`), `factor_correlation`, the `anchor` curve and `covariance_fit_error`.

**Raises:**

- <u>ValueError:</u> if `period`, `decay` or `kappa_bounds` is invalid, or fewer than 30 curve changes remain to fit.

</details>

## params

The calibrated HJM model: the two factors, their correlation and today's anchor curve.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
hjm.params  # property -> HjmParams
```

**Raises:**

- <u>RuntimeError:</u> if the model has not been calibrated yet.

</details>

## step_function

The one-step move of each HJM factor, `step_hjm_factor` below.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
hjm.step_function  # property
```

</details>

## changes

The historical period-over-period changes of `hjm_factor_1` and `hjm_factor_2`, which set their correlation
with the other factors.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
hjm.changes  # property -> dict[str, pl.DataFrame]
```

**Returns:**

<u>dict[str, pl.DataFrame]:</u> one table per factor, with a `date` and a `value` column.

**Raises:**

- <u>RuntimeError:</u> if the model has not been calibrated yet.

</details>

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

### hjm_convexity

The convexity drift Phi(t, x) that no-arbitrage adds to a forward rate: how far the forward rate at maturity `x`
has risen by time `t` purely because rates are random.

Bond prices are convex in rates, so randomness on its own makes bonds worth more on average; without a
correction, a model would let an investor lock in a riskless profit across maturities. Heath, Jarrow and Morton
(1992) showed that the correction is fully determined by the volatilities, so nothing here is fitted. It is
zero today, grows with the horizon and the volatility, and is largest for long maturities and slow-fading
factors. It assumes the two factors' shocks have the calibrated correlation, which the simulation ensures.

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

The first line is the Heath, Jarrow and Morton (1992) drift condition for correlated factors, which they call "the
forward rate drift restriction" (working-paper version, Cornell ORIE Technical Report 900, 1989, Proposition 3,
eq. (19), with the market price of risk set to 0); Phi(t, x) is that drift integrated from 0 to t at a fixed
time-to-maturity x = T - t.

**References:**

- Brigo, D., Mercurio, F. (2006). "Interest Rate Models: Theory and Practice" (2nd ed.), chapter 4: the G2++ phi(t) correction this term generalizes to an arbitrary tenor, not just t itself. Springer Finance. <https://doi.org/10.1007/978-3-540-34604-3>
- Heath, D., Jarrow, R., Morton, A. (1992). "Bond Pricing and the Term Structure of Interest Rates: A New Methodology for Contingent Claims Valuation." Econometrica, 60(1), 77-105. <https://doi.org/10.2307/2951677>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
hjm_convexity(
    elapsed_time: float | np.ndarray,
    tenor: float | np.ndarray,
    params: HjmParams,
) -> float | np.ndarray
```

**Args:**

- <u>elapsed_time (float &#124; np.ndarray):</u> t, years since the valuation date.
- <u>tenor (float &#124; np.ndarray):</u> x, the time to maturity in years (0 or more); an array broadcasts against `elapsed_time`.
- <u>params (HjmParams):</u> the calibrated two-factor model.

**Returns:**

<u>float &#124; np.ndarray:</u> Phi(t, x), one value per time and maturity given.

</details>

{% raw %}
### hjm_forward_rate

The simulated forward rate at a given time to maturity, at a future date in a scenario.

It is built from three parts. First, today's forward curve read at the same calendar date, so with no shocks
the curve simply rolls down as time passes, which is what an arbitrage-free model requires. Second, the two
factors' shocks, each fading with maturity at its own rate: the slow factor moves the whole curve, the fast one
mostly the short end. Third, the convexity drift `hjm_convexity`. Today, with both factors at zero, it gives back
today's curve exactly.

The formula is as follows:

$$
f(t,\; t + x) = f_{\text{anchor}}(t + x) + \exp(- \kappa_{1} \cdot x) \cdot x_{1}(t) + \exp(- \kappa_{2} \cdot x) \cdot x_{2}(t) + \Phi(t,\; x)
$$

Where f_anchor is today's Nelson-Siegel forward curve and Phi(t, x) is `hjm_convexity`.

**References:**

- Heath, D., Jarrow, R., Morton, A. (1992). "Bond Pricing and the Term Structure of Interest Rates: A New Methodology for Contingent Claims Valuation." Econometrica, 60(1), 77-105. <https://doi.org/10.2307/2951677>
- Brigo, D., Mercurio, F. (2006). "Interest Rate Models: Theory and Practice" (2nd ed.), chapters 3-4. Springer Finance. <https://doi.org/10.1007/978-3-540-34604-3>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
hjm_forward_rate(
    state_1: float | np.ndarray,
    state_2: float | np.ndarray,
    tenor: float | np.ndarray,
    elapsed_time: float | np.ndarray,
    params: HjmParams,
) -> float | np.ndarray
```

**Args:**

- <u>state_1 (float &#124; np.ndarray):</u> x_1(t), the simulated `hjm_factor_1` value or paths.
- <u>state_2 (float &#124; np.ndarray):</u> x_2(t), the simulated `hjm_factor_2` value or paths.
- <u>tenor (float &#124; np.ndarray):</u> x, the time to maturity in years (0 gives the short rate); an array of maturities gives the whole curve at once.
- <u>elapsed_time (float &#124; np.ndarray):</u> t, years since the valuation date.
- <u>params (HjmParams):</u> the calibrated two-factor model.

**Returns:**

<u>float &#124; np.ndarray:</u> the forward rate, for each scenario, date and maturity given.

</details>
{% endraw %}

{% raw %}
### hjm_zero_yield

The simulated zero-coupon yield to a given maturity, at a future date in a scenario: the continuously
compounded yield of a bond paying 1 at `tenor` years from then, the number to discount cash flows with or to
read the curve's slope from.

It is the average of `hjm_forward_rate` over the bond's life, in closed form. Each factor moves the yield by
B_i(m) times its value: close to one for short bonds and smaller for long ones, the more so for the fast-fading
second factor, so a shock to it moves short yields far more than long ones. Bond prices exp(-m * y) built from
these yields are consistent with each other at every maturity, which is what makes the curve arbitrage-free.

The formula is as follows:

$$
y(t,\; m) = (F_{\text{anchor}}(t + m) - F_{\text{anchor}}(t)) / m + \sum_{i} B_{i} (m) \cdot x_{i}(t) + (1 / m) \cdot \text{integral}_{0} ^{m} \Phi(t,\; u) \text{du}
$$

$$
B_{i}(m) = (1 - \exp(- \kappa_{i} \cdot m)) / (\kappa_{i} \cdot m)
$$

Where m is `tenor` and F_anchor is the integral of today's forward curve (`nelson_siegel_forward_integral`).

**References:**

- Brigo, D., Mercurio, F. (2006). "Interest Rate Models: Theory and Practice" (2nd ed.), chapters 3-4. Springer Finance. <https://doi.org/10.1007/978-3-540-34604-3>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
hjm_zero_yield(
    state_1: float | np.ndarray,
    state_2: float | np.ndarray,
    tenor: float,
    elapsed_time: float | np.ndarray,
    params: HjmParams,
) -> float | np.ndarray
```

**Args:**

- <u>state_1 (float &#124; np.ndarray):</u> x_1(t), the simulated `hjm_factor_1` value or paths.
- <u>state_2 (float &#124; np.ndarray):</u> x_2(t), the simulated `hjm_factor_2` value or paths.
- <u>tenor (float):</u> the bond's maturity, in years (above 0).
- <u>elapsed_time (float &#124; np.ndarray):</u> t, years since the valuation date.
- <u>params (HjmParams):</u> the calibrated two-factor model.

**Returns:**

<u>float &#124; np.ndarray:</u> the zero-coupon yield, for each scenario and date given.

**Raises:**

- <u>ValueError:</u> if `tenor` is not above 0.

</details>
{% endraw %}

### step_hjm_factor

Move one HJM factor forward one step: it decays toward its centre at the rate its volatility fades with
maturity, and receives a normally distributed shock.

The pull is not a separate assumption: in this model the speed at which a factor's effect fades along the curve
is the same speed at which it mean-reverts over time (Vasicek, 1977). Under the risk-neutral measure the centre is
zero, so the factors carry no term premium. A non-zero market price of risk moves the centre, adding the extra
return investors demand for holding long bonds, for a real-world view. The step is the exact one, so the
simulation frequency does not change the distribution.

The formula is as follows:

$$
x(t + \text{dt}) = m + (x(t) - m) \cdot \exp(- \kappa \cdot \text{dt}) + \sigma \cdot \sqrt{(1 - \exp(- 2 \cdot \kappa \cdot \text{dt})) / (2 \cdot \kappa)} \cdot z
$$

$$
m = \sigma \cdot \lambda / \kappa
$$

Where lambda is the market price of risk (0 under the risk-neutral measure, so m = 0) and z a standard normal draw.

**References:**

- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. <https://doi.org/10.1016/0304-405x(77>)90016-2

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_hjm_factor(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: HjmFactorParams,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> the factor's current value in each scenario.
- <u>shock (np.ndarray &#124; float):</u> the random draw for this step, standard normal.
- <u>time_step (float):</u> the step length, in years.
- <u>params (HjmFactorParams):</u> the factor's volatility, volatility decay and market price of risk.

**Returns:**

<u>np.ndarray:</u> the factor's value one step later.

</details>

### fit_hjm_factors

Calibrate a 2-factor Gaussian HJM model from historical yields at several maturities.

No-arbitrage fixes the drift, so only each factor's volatility and decay and their correlation are fit. A
Nelson-Siegel curve is fit at every date, turned into forward rates on a dense tenor grid, and the two-factor
model whose covariance best matches the covariance of the forward-curve changes is chosen (a grid search, then
a least-squares polish).

The formula is as follows:

$$
C(x,\; y) = \sum_{i} \sum_{j} \rho_{ij} \cdot \sigma_{i} \cdot \sigma_{j} \cdot \exp(- \kappa_{i} \cdot x - \kappa_{j} \cdot y)
$$

$$
e = \operatorname{norm}(C - \Sigma) / \operatorname{norm}(\Sigma)
$$

Sigma is the historical covariance of the forward-curve changes at tenors x and y, rho_11 = rho_22 = 1, norm is
the Frobenius norm, and the decays are chosen to minimize e.

The fitted forward curve has rank 3 at most, so `covariance_fit_error` is the honest goodness-of-fit number;
`variance_share` is close to 100% almost by construction.

**References:**

- Brigo, D., Mercurio, F. (2006). "Interest Rate Models: Theory and Practice" (2nd ed.), chapters 3-4. Springer Finance. <https://doi.org/10.1007/978-3-540-34604-3>
- Litterman, R., Scheinkman, J. (1991). "Common Factors Affecting Bond Returns." The Journal of Fixed Income, 1(1), 54-61. <https://doi.org/10.3905/jfi.1991.692347>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_hjm_factors(
    yields_by_tenor: dict[float, pl.Series],
    dates: pl.Series,
    time_step: float,
    decay: float = 0.7308,
    kappa_bounds: tuple[float, float] = (MINIMUM_KAPPA, MAXIMUM_KAPPA),
) -> tuple[HjmParams, pl.DataFrame]
```

**Args:**

- <u>yields_by_tenor (dict[float, pl.Series]):</u> maturity (years) -> historical yield series at that maturity; same shape term_structure_model. fit_nelson_siegel_factors expects (at least 3 tenors).
- <u>dates (pl.Series):</u> one date per observation, aligned to `yields_by_tenor`.
- <u>time_step (float):</u> the time increment between observations, in years.
- <u>decay (float):</u> the Nelson-Siegel decay parameter (lambda) for both the historical cross-sectional fit and the anchor curve.
- <u>kappa_bounds (tuple[float, float]):</u> (min, max) search bounds for both factors' volatility_decay. The default floor (0.01, a ~70-year half-life) is an economic choice, not a numerical one: a near-zero kappa_1 makes the convexity term grow at long horizons.

**Returns:**

<u>tuple[HjmParams, pl.DataFrame]:</u> the calibrated model, and a "date", "hjm_factor_1", "hjm_factor_2" DataFrame of the two factors' cumulative projected shocks.

**Raises:**

- <u>ValueError:</u> if fewer than MINIMUM_OBSERVATIONS_HJM forward-curve changes are available after the underlying Nelson-Siegel fit.

</details>
