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

The HJM module simulates the whole forward-rate curve with a two-factor Gaussian
Heath-Jarrow-Morton model: the first multi-factor curve model in this project that
rules out riskless arbitrage between maturities by construction. A forward rate is the interest
rate agreed today for borrowing over a short period that starts at some future date;
the forward curve lists those rates for every scenario start date, and it carries the
same information as the yield curve.

In plain terms: every other rate factor here (the interest rate factor's single-tenor
`hull_white`/`cir` methods, the `knw` VAR(1) pair, the `yield_curve` Nelson-Siegel
factors in `TermStructure`) learns its drift, the direction the rate tends to move,
from how rates mean-reverted in the past. This one does not. Once you choose how
volatile the forward curve is at each maturity, the no-arbitrage condition of
[Heath, Jarrow and Morton (1992)](https://doi.org/10.2307/2951677) fixes the drift
analytically, so it is never fitted. Use it when simulated bond prices across
maturities need to be consistent with each other, for example to value liabilities
against today's curve; use `yield_curve` when you want curves that behave like
history.

Why this framework exists: an economic scenario generator's curve factors should
ideally exclude riskless arbitrage between simulated maturities by construction, not
by accident. The `yield_curve` factors are a cross-sectional statistical fit, three
independent mean-reverting processes whose combination happens to look like a curve,
with no guarantee that the resulting dynamics are consistent with an arbitrage-free
bond market. HJM builds the curve the other way around: fix how the forward curve's
volatility depends on time to maturity, and the no-arbitrage condition derives the
drift.

The model fixes that volatility to two independent, exponentially dampened factors,
`sigma_i(t, x) = sigma_i * exp(-kappa_i * x)`, where `x` is time to maturity (the
Musiela parametrization, which indexes the curve by time to maturity rather than by
calendar maturity date), `sigma_i` is the factor's volatility and `kappa_i` its
volatility decay. Under this choice the model reduces to the closed-form, Markovian
(memoryless) two-factor Hull-White or G2++ representation
([Hull and White, 1994](https://doi.org/10.3905/jod.1994.407908);
[Brigo and Mercurio, 2006](https://doi.org/10.1007/978-3-540-34604-3), chapters 3-4),
and each factor's state collapses to a plain zero-mean Ornstein-Uhlenbeck process:

`dx_i = -kappa_i * x_i * dt + sigma_i * dW_i^Q`, with `x_i(0) = 0`

(`dW_i^Q` is a Brownian increment, continuous random noise, under the risk-neutral
measure Q). Each state is stepped with its exact discrete-time transition
(`step_hjm_factor`, the same closed-form Vasicek transition `step_curve_factor` and
`step_ou_process` use), with a long-run mean derived from an optional market price of
risk (zero by default) rather than fitted. `kappa_i` is not an independently fitted
mean-reversion speed the way it is for every other mean-reverting factor here: it is
a consequence of the chosen exponential volatility shape, forced by the no-arbitrage
condition, and that is the conceptual point of building HJM at all.

The forward rate at time to maturity `x`, `t` years after the model was anchored, is
rebuilt as (`hjm_forward_rate`):

`f(t, x) = f_anchor(t + x) + exp(-kappa_1*x)*x_1(t) + exp(-kappa_2*x)*x_2(t) + Phi(t, x)`

- `f_anchor` is today's observed forward curve, taken from the last fitted
  [Nelson-Siegel (1987)](https://doi.org/10.1086/296409) cross-section and evaluated
  in its forward-rate form (`nelson_siegel_forward`) rather than bootstrapped, since it
  is smooth and can be extrapolated at any maturity, including beyond the four
  observed treasury maturities. Evaluating it at the calendar maturity `t + x`, not
  just `x`, makes the curve roll down today's curve as time passes: the arbitrage-free
  property.
- `Phi(t, x)` is a deterministic convexity term that the no-arbitrage condition itself
  supplies (`hjm_convexity`). It is not fitted, not a free parameter, and required for
  the reconstruction to be arbitrage-free. Its cross term reads `factor_correlation`,
  so it is only correct when the two factors' simulated shocks are drawn with that
  same correlation; they are here, because `Dependence` estimates the correlation from
  the model's own fitted `changes`.

At `t = 0` both states are zero and `Phi(0, x) = 0`, so the model reproduces today's
anchor curve exactly at every maturity. To read a simulated curve after a run:

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

`hjm_zero_yield` rebuilds a zero-coupon yield the same way (the closed-form average of
`hjm_forward_rate` over `[t, t + x]`), for discount factors or curve-shape checks such
as inversion (`term_structure_model.curve_inversion_frequency`) that want a yield
rather than an instantaneous forward.

The data are the same four Yahoo Finance treasury-yield tickers as `yield_curve`'s
default source (`term_structure_model.YIELD_CURVE_TENORS`: `^IRX`, `^FVX`, `^TNX`,
`^TYX`), from one `Toolkit.get_historical_data()` call; no API key is needed. HJM fits
its own Nelson-Siegel anchor curve with its own `decay`, independent of a separately
enabled `yield_curve` block. How the volatilities, decays and correlation are
estimated is described under `calibrate`.

What it does not do, and the simplifications it makes:

- **Risk-neutral by construction, zero term premium by default.** The HJM drift
  condition is a risk-neutral (Q-measure) result. With `market_price_of_risk = 0` for
  both factors, `E^Q[f(t, x)] = f_anchor(t + x) + Phi(t, x)`: future rates equal
  today's forwards plus convexity, with no term premium (the extra yield investors
  demand for holding long bonds). Every other rate factor here is real-world
  (P-measure) and fitted to history, so mixing this factor into a real-world scenario
  set is a genuine measure inconsistency to be aware of. No data source in this
  project identifies the market price of risk (the same gap `knw_sv_q` has for its
  risk-neutral leg), so it is a settable belief, not fitted.
- **Four observed maturities, not a dense curve.** True HJM estimates a continuous
  volatility function from a dense curve; here a two-factor exponential structure is
  imposed up front and fitted to a covariance derived from four maturities.
- **Forwards are Nelson-Siegel-derived, not bootstrapped.** The anchor curve and the
  whole historical forward panel inherit Nelson-Siegel's three-factor shape, so the
  calibration can never see a forward-curve movement outside that family.
- **Forward-rate volatility can only decrease with maturity.** A positive `kappa_i`
  makes each factor's volatility contribution decay monotonically, while real
  forward-volatility curves are typically humped. The standard fix
  ([Cheyette, 1992](https://doi.org/10.3905/jfi.1992.408036);
  [Ritchken and Sankarasubramanian, 1995](https://doi.org/10.1111/j.1467-9965.1995.tb00101.x)),
  a loading of the form `(a + b*x)*exp(-kappa*x)`, stays Markovian but needs an extra
  coupled state per factor and a messier drift condition; it is a documented extension
  point, not attempted.
- **Two factors cannot generate curvature.** Reachable forward-curve moves span only
  `exp(-kappa_1*x)` and `exp(-kappa_2*x)`, so a random hump in the forward curve is
  impossible; only the anchor's own Nelson-Siegel curvature produces one, and only
  deterministically as it rolls down.
- **Time-homogeneous volatility.** `sigma_i(t, x)` depends on time to maturity only,
  never on calendar time: the model fits today's curve exactly but not today's
  volatility term structure. A full Hull-White calibration would make volatility
  piecewise constant in calendar time against cap and swaption implied volatilities,
  and no such market data exists in this project.
- **Only the state transition is exact.** `step_hjm_factor` has no discretization
  error, but a discount factor or bank account built on top of it by integrating the
  simulated short rate over the step grid should use trapezoidal accumulation, not a
  left-endpoint sum; this was confirmed to matter at this project's default
  simulation frequencies.
- **Compounding convention.** The reconstructions return continuously compounded
  forwards and zero yields, while the Yahoo tickers are bond-equivalent (semiannual)
  quotes; like `yield_curve` and the interest rate factor, the quotes are divided by
  100 with no further compounding conversion.
- **Flat beliefs only.** `hjm.beliefs` substitutes parameters; unlike `OUBeliefs`
  there is no time-varying target path and no `shocks` list in this first version.

Configuration (`hjm` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `enabled` | `false` | Adds `hjm_factor_1`/`hjm_factor_2` and the four tenor tickers when `true`. |
| `period` | `daily` | Calibration frequency; sets the time step. |
| `decay` | `0.7308` | Nelson-Siegel decay (lambda) for HJM's own anchor fit; independent of `yield_curve`. |
| `kappa_bounds` | `(0.01, 6.0)` | Search bounds for both factors' `volatility_decay` (see below). |
| `beliefs.factor_1.volatility` | `null` | Override `sigma_1`; must be greater than 0. |
| `beliefs.factor_1.volatility_decay` | `null` | Override `kappa_1`; must be greater than 0. |
| `beliefs.factor_1.market_price_of_risk` | `null` | Set `lambda_1`; non-zero adds a real-world drift. |
| `beliefs.factor_2.*` | all `null` | The same three overrides for factor 2. |
| `beliefs.factor_correlation` | `null` | Override the fitted `rho`, between -1 and 1 (see below). |

The `kappa_bounds` floor of 0.01 (a half-life of about 70 years) is an economic choice,
not a numerical one; `calibrate` explains what a near-zero `kappa_1` does to the
convexity term at long horizons. If `factor_correlation` is overridden, remember that
`hjm_convexity`'s cross term uses the override, so it should match the correlation the
simulated shocks are actually drawn with, or the curve is no longer arbitrage-free.
`Scenarios.simulate()` calibrates and simulates HJM automatically whenever
`hjm.enabled` is `true`; nothing else about the call changes.

**References:**

- Heath, D., Jarrow, R., Morton, A. (1992). "Bond Pricing and the Term Structure of Interest Rates: A New Methodology for Contingent Claims Valuation." Econometrica, 60(1), 77-105. <https://doi.org/10.2307/2951677>
- Hull, J., White, A. (1994). "Numerical Procedures for Implementing Term Structure Models II: Two-Factor Models." The Journal of Derivatives, 2(2), 37-48. <https://doi.org/10.3905/jod.1994.407908>
- Brigo, D., Mercurio, F. (2006). "Interest Rate Models: Theory and Practice" (2nd ed.), chapters 3-4 (G1++ and G2++), the closed-form two-factor reduction the reconstruction and convexity formulas were verified against. Springer Finance. <https://doi.org/10.1007/978-3-540-34604-3>
- Cheyette, O. (1992). "Term Structure Dynamics and Mortgage Valuation." The Journal of Fixed Income, 1(4), 28-41. <https://doi.org/10.3905/jfi.1992.408036>
- Ritchken, P., Sankarasubramanian, L. (1995). "Volatility Structures of Forward Rates and the Dynamics of the Term Structure." Mathematical Finance, 5(1), 55-72. <https://doi.org/10.1111/j.1467-9965.1995.tb00101.x>
- Litterman, R., Scheinkman, J. (1991). "Common Factors Affecting Bond Returns." The Journal of Fixed Income, 1(1), 54-61, the principal-component justification for the calibration approach. <https://doi.org/10.3905/jfi.1991.692347>
- Nelson, C.R., Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." The Journal of Business, 60(4), 473-489, the source of the anchor curve. <https://doi.org/10.1086/296409>

## calibrate

```python
calibrate(
    period: str = 'daily',
    decay: float = 0.7308,
    kappa_bounds: tuple[float, float] = (0.01, 6.0),
) -> HjmParams
```

Calibrate the two-factor Gaussian HJM model from historical treasury yields across
the four standard maturities: estimate each factor's volatility (`volatility`,
sigma_i), how fast that volatility fades with maturity (`volatility_decay`,
kappa_i) and the correlation between the two factors (`factor_correlation`, rho),
and record today's curve as the anchor the simulation rolls forward from.

In plain terms: this measures how much, and how differently, the short and long
ends of the forward curve have moved day to day, and summarizes that as two
sources of movement: a slow-fading one that shifts the whole curve (factor 1) and a
fast-fading one that mostly moves the short end (factor 2). A decay `kappa` means a
factor's effect on the forward rate halves every ln 2 / kappa years of maturity; a
`kappa_1` of 0.027, for example, barely fades over 30 years (a half-length of about
25 years), while a `kappa_2` of 1.86 has halved by a maturity of four to five months.
Because the drift is derived rather than fitted, there is no mean-reversion speed
or long-run mean to estimate, unlike every other mean-reverting factor here.

The estimation (`fit_hjm_factors`) runs in four steps:

1. Fit the same Nelson-Siegel curve as `yield_curve` (`fit_nelson_siegel_factors`)
   to the four maturities at every historical date.
2. Evaluate that curve's forward-rate form on a dense 12-point maturity grid
   (`HJM_CALIBRATION_TENORS`, 3 months to 30 years), not just the four raw
   maturities: with the shared decay default the raw four make the 5-, 10- and
   30-year forwards about 99% collinear, too little shape information to separate
   two exponential decay rates. Since the historical forward curve is itself
   Nelson-Siegel-derived (at most three dimensions by construction), the denser
   grid re-weights the shape-matching objective; it does not add new information.
3. Take the historical covariance of the period-over-period changes in that forward
   curve across the grid, annualized by the time step.
4. Fit the two-factor exponential model whose implied covariance best matches it.
   For any candidate `(kappa_1, kappa_2)`, `(sigma_1, sigma_2, rho)` have closed-form
   estimates: project each historical change onto the two loading vectors
   `exp(-kappa_i * x)` by least squares, then read `sigma_i` off the projected
   shocks' standard deviation and `rho` off their correlation. The search is
   therefore only two-dimensional: an 80 by 80 grid scan plus a local least
   squares polish, with factor 1 the slower-decaying one by convention.

Two goodness-of-fit numbers come back. `covariance_fit_error`, the relative
Frobenius norm (a matrix version of the root of summed squared differences) between
the model's implied covariance and the historical one, is the honest one; a value
above 0.35 logs a warning. `variance_share` is a raw principal-component diagnostic
(each factor's share of the historical covariance's total variance) and is high
almost by construction here, so it is no evidence that two factors are adequate.

Also known as: G2++ calibration, two-factor Hull-White calibration, forward-rate
volatility fit.

**Args:**

- <u>period (str):</u> sampling frequency of the underlying data ("daily", "weekly", "monthly", "quarterly", "yearly"), determines the time_step used to fit each factor.
- <u>decay (float):</u> the Nelson-Siegel decay parameter (lambda), annualized, for both the historical cross-sectional fit and the anchor curve.
- <u>kappa_bounds (tuple[float, float]):</u> (min, max) search bounds for both factors' volatility_decay. The default floor (0.01, a ~70-year half-life) is an economic choice, not a numerical one; see Notes.

**Returns:**

<u>HjmParams:</u> the calibrated 2-factor model.

**Raises:**

- <u>ValueError:</u> if period is not recognized, or fewer than 30 forward-curve changes remain after the Nelson-Siegel fit (`fit_hjm_factors`).

**Notes:**

- The Yahoo tickers are quoted in percentage points and divided by 100.
- The faster-decaying factor (`factor_2`) is weakly identified: with the shortest
  observed maturity at three months, fast decays look almost alike. Recovery tests
  on synthetic data get `kappa_2` only to the right order of magnitude, while the
  covariance itself (and therefore the simulated curve dynamics) fits closely
  regardless. Do not read a fitted `kappa_2` as an economically meaningful rate.
- `kappa_1` often fits at or near its search floor (0.027 against 0.01 in the example
  below): a near Ho-Lee level mode (a parallel shift that hardly mean-reverts) is
  what the data tend to say. An arbitrage-free Gaussian model with high long-rate
  volatility and weak mean reversion must then carry a large convexity drift at long horizons, so a 50-year
  projection at the floor is not credible. A warning is logged when either decay
  sits at a bound; raising the floor in `kappa_bounds` (for example to a
  Hull-White-conventional 0.03-0.10) is a defensible prior if long-horizon
  convexity looks too large for a use case.
- The cross-convexity term must match the engine's correlation matrix. It does by
  construction, since the returned `changes` are the model's own projected shocks
  and feed `Dependence`'s correlation estimate; a `factor_correlation` belief
  breaks that unless it matches what the shocks are actually drawn with.
- `changes` holds, per factor, the dated changes of the cumulative projected shock,
  shaped like `TermStructure.changes` so `Dependence` treats both alike.
- Belief overrides are applied after this call, by `config_model.apply_hjm_beliefs`.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.hjm.hjm_controller import Hjm
from financescenarios.factors.hjm.hjm_model import hjm_forward_rate, hjm_zero_yield

toolkit = Toolkit(["^IRX", "^FVX", "^TNX", "^TYX"], api_key="FINANCIAL_MODELING_PREP_KEY")
hjm = Hjm(toolkit)

params = hjm.calibrate(period="daily")

for tenor in (0.25, 2.0, 10.0, 30.0):
    print(
        tenor,
        hjm_zero_yield(0.0, 0.0, tenor, 0.0, params),
        hjm_forward_rate(0.0, 0.0, tenor, 0.0, params),
        hjm_forward_rate(0.0, 0.0, tenor, 10.0, params),
    )
```

Which returns (calibrated on 2026-10-04, daily data from 2021-10-06 to 2026-10-02):

| factor | volatility | volatility_decay | variance_share |
|:-------|-----------:|-----------------:|---------------:|
| factor_1 | 0.0132 | 0.0272 | 0.4856 |
| factor_2 | 0.0518 | 1.8637 | 0.4210 |

with `factor_correlation` -0.5346 and `covariance_fit_error` 0.2604, and the
reconstructed curve:

| tenor | zero yield today | forward today | expected forward in 10 years | of which convexity |
|------:|-----------------:|--------------:|-----------------------------:|-------------------:|
| 0.25 | 0.0399 | 0.0407 | 0.0627 | 0.0056 |
| 2 | 0.0450 | 0.0499 | 0.0643 | 0.0072 |
| 10 | 0.0535 | 0.0571 | 0.0699 | 0.0128 |
| 30 | 0.0559 | 0.0572 | 0.0716 | 0.0144 |

Factor 1 is the slow, level-like movement (1.32% a year, fading little across
maturities) and factor 2 the fast, short-end movement (5.18% a year at the very
short end, halved by four to five months of maturity); the two tend to move in
opposite directions (a correlation of -0.53). The model's covariance misses the
historical one by 26%, inside the 35% warning level. Today's zero yields match the
Nelson-Siegel curve of `TermStructure` (3.99% at 3 months to 5.59% at 30 years). Ten
years out, with both states at their expected value of zero, the expected forward
rate is today's forward for that later date plus a convexity term of 0.56 to 1.44
percentage points, growing with maturity: the price of keeping the curve
arbitrage-free with a slow-fading level factor.

**References:**

- Heath, D., Jarrow, R., Morton, A. (1992). "Bond Pricing and the Term Structure of Interest Rates: A New Methodology for Contingent Claims Valuation." Econometrica, 60(1), 77-105. <https://doi.org/10.2307/2951677>
- Brigo, D., Mercurio, F. (2006). "Interest Rate Models: Theory and Practice" (2nd ed.), chapters 3-4. Springer Finance. <https://doi.org/10.1007/978-3-540-34604-3>
- Litterman, R., Scheinkman, J. (1991). "Common Factors Affecting Bond Returns." The Journal of Fixed Income, 1(1), 54-61. <https://doi.org/10.3905/jfi.1991.692347>

## params

```python
hjm.params  # property -> HjmParams
```

The last-calibrated HJM parameters.

**Raises:**

- <u>RuntimeError:</u> if calibrate() hasn't been called yet.

## step_function

```python
hjm.step_function  # property
```

The exact-transition state step function (see hjm_model.step_hjm_factor's
own docstring) shared by both factors, differing only in which factor's
HjmFactorParams the caller supplies.

## changes

```python
hjm.changes  # property -> dict[str, pl.DataFrame]
```

Dated period-over-period changes in each HJM factor's cumulative projected
shock ("hjm_factor_1", "hjm_factor_2"), from the same data calibrate()
already fetched; reused for cross-factor correlation estimation
(Dependence) instead of triggering a second Finance Toolkit fetch.

**Returns:**

<u>dict[str, pl.DataFrame]:</u> one entry per factor, each two columns, `date` (pl.Date) and `value` (f64); see helpers.dated_changes().

**Raises:**

- <u>RuntimeError:</u> if calibrate() hasn't been called yet.
