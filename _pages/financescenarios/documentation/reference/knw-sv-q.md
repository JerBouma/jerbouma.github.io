---
title: "KnwSvQ"
seo_title: "KnwSvQ Reference – Finance Scenarios"
excerpt: "The risk-neutral (Q-measure) side of the KNW models."
description: "The risk-neutral (Q-measure) side of the KNW models."
author_profile: false
permalink: /projects/financescenarios/docs/reference/knw-sv-q
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

The risk-neutral (Q-measure) side of the KNW models. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.models.knw_sv_q.knw_sv_q_controller import KnwSvQ
```

```python
KnwSvQ(toolkit: Toolkit)
```

The KnwSvQ module turns a calibrated `KnwSv` pair into a risk-neutral (Q-measure)
model: it learns the market price of risk that makes the model reproduce the observed
Treasury yield curve, and with that it can price zero-coupon bonds in closed form,
simulate the pair under Q, or build a stochastic deflator for a real-world run.

In plain terms: a real-world (P-measure) simulation answers "where might rates go?",
while pricing needs the risk-neutral view "what is a future cash flow worth today?".
The bridge between the two is the market price of risk, the extra return investors
demand for bearing each source of risk. This module fits that price so the model's
yields match the 13-week, 5-, 10- and 30-year Treasury yields seen in the market, then
gives you model yields at any maturity (`zero_coupon_yield`), the Q-measure parameters
to simulate with (`q_params`, used when a config entry sets `measure: risk_neutral`),
and a deflator to price claims off a real-world run (`deflator`).

Why not DNB's own method: DNB derives its Q-measure with an essentially-affine market
price of risk (`M = K + Sigma*lambda1`), calibrated by maximum likelihood against
option, swaption and inflation-cap prices (CP2022 Technical Appendix, sections 5-6).
This project has none of that data (only single-point equity at-the-money implied
volatility in `equities_controller` and commodity forward curves in
`commodities_model`, neither useful for rate or inflation derivatives). Standard
affine term-structure practice offers an alternative that needs no derivatives: fit the
market price of risk to the observed yield curve itself, the same four-tenor Treasury
panel (`^IRX`, `^FVX`, `^TNX`, `^TYX`, `term_structure_model.YIELD_CURVE_TENORS`) the
Nelson-Siegel `TermStructure` fit ([Diebold & Li, 2006](https://doi.org/10.1016/j.jeconom.2005.03.005))
pulls. A Q-measure that reproduces the historical yield curve at every maturity is a
real, useful (if less rich) alternative to a derivatives-calibrated one.

The market price of risk is completely affine ([Duffie & Kan, 1996](
https://doi.org/10.1111/j.1467-9965.1996.tb00123.x)), with five free parameters
(`knw_sv_q_model.CompletelyAffineMprParams`) that change only the drift:

```text
kappa_v^Q  = kappa_v^P + risk_premium_v
theta_v^Q  = kappa_v^P * theta_v^P / kappa_v^Q   (keeps the drift's constant term)
c_r^Q      = c_r^P      - risk_premium_interest_rate_constant
gamma_r^Q  = gamma_r^P  - risk_premium_interest_rate_variance
c_pi^Q     = c_pi^P     - risk_premium_inflation_constant
gamma_pi^Q = gamma_pi^P - risk_premium_inflation_variance
```

Every other field (`own_persistence`, `cross_coupling`, `base_variance`,
`variance_sensitivity`, `volatility`, `initial_value`) is the same under both measures,
since a change of drift does not touch a diffusion coefficient or today's observed
level. The Q parameters therefore have the exact `OUParams`/`KnwSvLegParams` shapes of
the P ones, and `step_knw_sv_v`, `step_knw_sv_leg` and `KnwSvVarianceStepper` simulate
them unchanged. It is deliberately not the richer essentially-affine form of
[Duffee (2002)](https://doi.org/10.1111/1540-6261.00426) that DNB uses: the price of risk
on the rate and inflation loads on a constant and `v` only, never on their own lagged
level. `v` is the only state variable the model's variance depends on, so a loading on
the rate's or inflation's own level would shift the Q drift with no volatility channel
to justify it, and a short quarterly OECD panel (40-80 dates) cannot reliably identify a
general 12-parameter essentially-affine form (a 3x3 loading matrix plus a 3-vector) in
the first place. Each of the five parameters stays tied to a real variance channel.

Bond prices come from a discrete-time affine recursion
(`knw_sv_q_model.zero_coupon_bond_recursion`), not a continuous-time Riccati
differential equation. The rate and inflation coefficients are a directly fit discrete
recursion with no time step to rescale, so a continuous-time equation would mean
inventing a reinterpretation the fit never produced. The discrete form needs none:
`v`'s CIR factor has an exact discrete transition (the non-central chi-square that
Andersen's QE scheme samples), and the rate and inflation transitions are Gaussian
given `v`, exactly what `step_knw_sv_leg` implements. The price `n` periods out is
`exp(A[n] + Bv[n]*v + Br[n]*r + Bpi[n]*pi)`, built by a plain backward loop; `Bv`'s
update is a discrete Riccati difference equation, nonlinear because `v`'s diffusion
scales with `v` itself, while `Br`/`Bpi` stay linear. `v`'s conditional log
moment-generating function (`knw_sv_q_model._cir_log_mgf`) is closed form, from CIR's
exact transition ([Cox, Ingersoll & Ross, 1985](https://doi.org/10.2307/1911242)), and is
cross-checked against a Monte Carlo average of `step_knw_sv_v` in
`tests/models/knw_sv_q/test_knw_sv_q_model.py`. The recursion computes the same
model's expectation in closed form instead of sampling it.

The stochastic deflator (`deflator`) follows [Cheng & Planchet (2018)](
https://hal.science/hal-01730072): `D(t) = delta(t) * dQ/dP`, a pricing kernel built
from a Radon-Nikodym derivative (the density that reweights real-world paths into
risk-neutral ones), not just the bank-account discount factor
`ScenarioSet.discount_factors` already gives. Its defining property,
`E^P[D(T)] = ` the Q-measure zero-coupon price at `T`, lets a real-world-only run price
a claim as `E^P[D(T)*payoff(T)]` without a separate risk-neutral run, the paper's own
motivation.

The data are the same as `KnwSv`'s plus the four Treasury yield tickers, pulled from
Yahoo Finance through the Toolkit's `get_historical_data` (no API key needed; a
config with `measure: risk_neutral` adds the tickers to `ScenariosConfig.tickers`
automatically, the same four `yield_curve.enabled` pulls). In a run,
`calibrate_all()` fits the P-measure triple first (`KnwSv.calibrate_triple`), then
calls `calibrate_mpr` and swaps in `q_params`, so the step-function dispatch in
`scenarios_controller` simulates either measure unchanged.

What it does not do:
- Not DNB's own Q-measure: the derivatives-calibrated essentially-affine fit stays
  unbuilt for lack of market data. This is a genuine, different (not merely
  simplified) alternative: real closed-form Q-measure machinery, calibrated against
  different data.
- Completely affine, not essentially affine (see above).
- The closed-form recursion assumes the rate's and inflation's own shocks are
  uncorrelated. The P-measure Monte Carlo engine still applies the full correlation
  matrix (`Dependence`); only this deterministic pricing formula assumes it away. A
  nonzero correlation would add one constant cross term, a documented extension point
  not attempted since `KnwSv` does not expose the fitted correlation here.
- No Q-measure equity leg: a `knw_sv` equity entry naming a `measure: risk_neutral`
  rate is rejected, since its drift (DNB eq. 4/5) is a P-measure-only fit, blocked on
  the same options data as DNB's own Q-measure.
- The deflator does not reweight `v`'s own shock (see `deflator`), which biases it
  materially once `risk_premium_v` is far from zero at long maturities.
- The inflation-specific risk premium is weakly identified from a nominal-only curve
  (see `calibrate_mpr`); a real (TIPS) curve or inflation swaps would fix this, and
  neither is in this project's data sources.

Configuration: set `measure: risk_neutral` on both the `interest_rates[i]` entry and
its paired `inflation[j]` entry of a `method: knw_sv` pair (`ScenariosConfig` rejects a
mismatch, since the market price of risk is fit for the whole `(v, r, pi)` triple at
once and the pair simulates under one measure together). Everything else is
configured as for `KnwSv`, including `period` equal to `engine.frequency`.

| Key | Default | Meaning |
|:----|:--------|:--------|
| `interest_rates[i].measure` | `real_world` | `risk_neutral` fits the market price of risk and simulates under Q. |
| `inflation[j].measure` | `real_world` | Must equal the paired rate entry's `measure`. |

**References:**

- Duffie, D., Kan, R. (1996). "A Yield-Factor Model of Interest Rates." Mathematical Finance, 6(4), 379-406. <https://doi.org/10.1111/j.1467-9965.1996.tb00123.x>
- Duffee, G.R. (2002). "Term Premia and Interest Rate Forecasts in Affine Models." Journal of Finance, 57(1), 405-443. <https://doi.org/10.1111/1540-6261.00426>
- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). "A Theory of the Term Structure of Interest Rates." Econometrica, 53(2), 385-407. <https://doi.org/10.2307/1911242>
- Diebold, F.X., Li, C. (2006). "Forecasting the term structure of government bond yields." Journal of Econometrics, 130(2), 337-364. <https://doi.org/10.1016/j.jeconom.2005.03.005>
- Cheng, P.-K., Planchet, F. (2018). "Stochastic Deflator for an Economic Scenario Generator with Five Factors." HAL preprint hal-01730072. <https://hal.science/hal-01730072>
- Commissie Parameters (2022). "Technical Appendix: Specification of the CP2022 Model." Sections 5-6 describe DNB's derivatives-calibrated market price of risk, which this module deliberately does not implement. <https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix>
- Andersen, L. (2008). "Simple and Efficient Simulation of the Heston Stochastic Volatility Model." Journal of Computational Finance, 11(3), 1-42. <https://doi.org/10.21314/jcf.2008.189>

## calibrate_mpr

```python
calibrate_mpr(
    knw_sv: KnwSv,
    interest_rate_name: str,
    inflation_name: str,
    period: str,
) -> CompletelyAffineMprParams
```

Fit the completely-affine market price of risk for an already real-world
(P-measure) calibrated knw_sv pair against the observed Treasury yield curve, and
store the matching risk-neutral (Q-measure) parameters for `q_params`,
`zero_coupon_yield` and `deflator`.

In plain terms: this finds the five risk premiums that make the model's bond
yields line up with the 13-week, 5-, 10- and 30-year Treasury yields on every
historical date. `risk_premium_v` changes how fast the turbulence factor `v` mean
reverts under Q (its Q speed is the P speed plus this premium); the two
`..._constant` premiums shift each leg's Q drift by a fixed amount per period, and
the two `..._variance` premiums shift it in proportion to `v`. A positive
`risk_premium_interest_rate_constant` lowers the Q drift of the short rate.

The fit is nonlinear least squares (`scipy.optimize.least_squares`, starting at
zero): across every date both the state history and the yield panel cover, it
minimizes the squared gap between the model yield (`zero_coupon_yield`, given that
date's actual `v`, rate and inflation) and the observed yield, summed over all
four tenors. `v` is latent, so its "observed" state is the same realized-variance
proxy the P-measure CIR fit used (`knw_sv_model.compute_v_proxy`, rebuilt from
`knw_sv.series`/`knw_sv.dates`). Treasury yields are quoted in percent and divided
by 100. `risk_premium_v` is bounded so `v`'s Q speed stays positive.

Also known as: market price of risk calibration, term-premium fit, P-to-Q change
of measure.

**Args:**

- <u>knw_sv (KnwSv):</u> an already-calibrated knw_sv controller instance.
- <u>interest_rate_name (str):</u> the pair's interest-rate leg's name, as passed to `knw_sv.calibrate_triple`.
- <u>inflation_name (str):</u> the pair's inflation leg's name, as passed to `knw_sv.calibrate_triple`.
- <u>period (str):</u> the sampling frequency `knw_sv.calibrate_triple` used ("monthly", "quarterly", or "yearly"); determines this fit's time_step.

**Returns:**

<u>CompletelyAffineMprParams:</u> the calibrated market price of risk.

**Raises:**

- <u>ValueError:</u> if `period` is not recognized, or propagated from `knw_sv_q_model.calibrate_completely_affine_mpr` (too few overlapping observations, or a tenor that isn't a whole number of periods).
- <u>RuntimeError:</u> propagated from `knw_sv.params`/`knw_sv.series`/`knw_sv.dates` if `calibrate_triple` for this pair hasn't been called yet.

**Notes:**

- What matters is that the Q model reprices the observed panel closely, not that
  each of the five parameters is recovered precisely on a short sample.
  `risk_premium_inflation_variance` in particular is weakly identified from a
  nominal-only curve: inflation reaches bond prices only through the rate leg's
  `cross_coupling`, a much weaker path than the rate's direct role as the discount
  rate. A real (TIPS) curve or inflation swaps would close this gap, as DNB's
  derivatives-calibrated approach does; neither is in this project's data.
- When `|risk_premium_v|` exceeds 5% of `v`'s P speed, a warning says `deflator()`
  is in its materially biased regime at long maturities (see `deflator`).
- Every tenor must be a whole number of periods: the 13-week tenor is 0.25 years, so
  monthly and quarterly pairs work and a yearly pair raises. At least 10 dates must
  overlap.
- A non-converging optimizer logs a warning and returns its last point.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.models.knw_sv.knw_sv_controller import KnwSv
from financescenarios.models.knw_sv_q.knw_sv_q_controller import KnwSvQ

toolkit = Toolkit(
    ["^IRX", "^FVX", "^TNX", "^TYX"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1990-01-01"
)
knw_sv = KnwSv(toolkit)
knw_sv.calibrate_triple("interest_rate", "inflation", period="quarterly")

knw_sv_q = KnwSvQ(toolkit)
knw_sv_q.calibrate_mpr(knw_sv, "interest_rate", "inflation", period="quarterly")
```

Which returns (calibrated on 2026-10-05):

| risk_premium_v | rate_constant | rate_variance | inflation_constant | inflation_variance |
|---------------:|--------------:|--------------:|-------------------:|-------------------:|
| -0.1532 | 0.0001 | -8.5226 | -0.0027 | 9.4999 |

The columns are the five `risk_premium_*` fields. Under Q, `v` reverts at
0.399 - 0.153 = 0.246 a year toward 0.000102, 1.6 times its historical normal
level, so the yield curve prices in more turbulence than history shows. The
inflation variance premium of 9.5 is the weakly identified one, and since
`|risk_premium_v|` is 38% of `v`'s speed the deflator warning fires.

**References:**

- Duffie, D., Kan, R. (1996). "A Yield-Factor Model of Interest Rates." Mathematical Finance, 6(4), 379-406. <https://doi.org/10.1111/j.1467-9965.1996.tb00123.x>
- Duffee, G.R. (2002). "Term Premia and Interest Rate Forecasts in Affine Models." Journal of Finance, 57(1), 405-443. <https://doi.org/10.1111/1540-6261.00426>
- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). "A Theory of the Term Structure of Interest Rates." Econometrica, 53(2), 385-407. <https://doi.org/10.2307/1911242>

## mpr

```python
mpr(interest_rate_name: str) -> CompletelyAffineMprParams
```

The calibrated market price of risk for one pair.

**Args:**

- <u>interest_rate_name (str):</u> the pair's interest-rate leg's name, as passed to calibrate_mpr().

**Raises:**

- <u>RuntimeError:</u> if calibrate_mpr(...) naming this pair hasn't been called yet.

## q_params

```python
q_params(interest_rate_name: str) -> tuple[OUParams, KnwSvLegParams, KnwSvLegParams]
```

The Q-measure (v, interest_rate, inflation) params `apply_completely_affine_mpr`
computed alongside the fitted market price of risk: drop-in replacements for
the P-measure triple `calibrate_triple` produced (same `OUParams`/`KnwSvLegParams`
shapes, see `apply_completely_affine_mpr`'s own docstring), for a config entry
that wants this pair simulated under `measure="risk_neutral"` instead of priced
off of separately via `zero_coupon_yield`.

**Args:**

- <u>interest_rate_name (str):</u> the pair's interest-rate leg's name, as passed to calibrate_mpr().

**Returns:**

<u>tuple[OUParams, KnwSvLegParams, KnwSvLegParams]:</u> (v_q, interest_rate_q, inflation_q).

**Raises:**

- <u>RuntimeError:</u> if calibrate_mpr(...) naming this pair hasn't been called yet.

## zero_coupon_yield

```python
zero_coupon_yield(interest_rate_name: str, tenor: float) -> float
```

The model-implied continuously compounded zero-coupon yield at `tenor` years,
evaluated at the pair's current state (each leg's `initial_value`, the last
observed level, the convention every calibrated-params type here uses).

In plain terms: this reads today's yield curve off the fitted risk-neutral model,
at any maturity that is a whole number of periods, including maturities the
Treasury panel does not quote. A value of 0.04 at `tenor=10` means a 10-year
zero-coupon bond is priced at exp(-0.04 * 10) = 0.67 per unit of face value.

The price comes from the discrete-time affine recursion
`exp(A[n] + Bv[n]*v + Br[n]*r + Bpi[n]*pi)` with `n = tenor / period length`
(`knw_sv_q_model.zero_coupon_bond_recursion`), and the yield is
`-log(price) / tenor`.

Also known as: model zero curve, affine spot yield.

**Args:**

- <u>interest_rate_name (str):</u> the pair's interest-rate leg's name, as passed to calibrate_mpr().
- <u>tenor (float):</u> the maturity, in years, to price.

**Returns:**

<u>float:</u> the model-implied zero-coupon yield at `tenor`.

**Raises:**

- <u>RuntimeError:</u> if calibrate_mpr(...) naming this pair hasn't been called yet.
- <u>ValueError:</u> if `tenor` is not a whole number of periods at this pair's time_step.

**Notes:**

- The one-period yield equals today's short rate, since the first step of the
  recursion discounts at `r` itself.
- The recursion assumes uncorrelated rate and inflation shocks (see the class
  docstring); the Monte Carlo engine does not.

As an example, continuing from `calibrate_mpr`:

```python
for tenor in [0.25, 1, 2, 5, 10, 20, 30]:
    print(tenor, knw_sv_q.zero_coupon_yield("interest_rate", tenor))
```

Which returns (calibrated on 2026-10-04):

| tenor (years) | 0.25 | 1 | 2 | 5 | 10 | 20 | 30 |
|:--------------|-----:|--:|--:|--:|---:|---:|---:|
| yield | 0.0375 | 0.0381 | 0.0404 | 0.0453 | 0.0487 | 0.0496 | 0.0492 |

The model curve starts at today's 3.75% short rate, rises to 4.5% at five years and
flattens just under 5% beyond ten. That is below the latest observed Treasury yields
(13-week 3.99%, 5-year 5.06%, 10-year 5.28%, 30-year 5.63%), since the premiums are
fit across the whole history and the state is the last OECD quarter.

**References:**

- Duffie, D., Kan, R. (1996). "A Yield-Factor Model of Interest Rates." Mathematical Finance, 6(4), 379-406. <https://doi.org/10.1111/j.1467-9965.1996.tb00123.x>
- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). "A Theory of the Term Structure of Interest Rates." Econometrica, 53(2), 385-407. <https://doi.org/10.2307/1911242>

## deflator

```python
deflator(
    interest_rate_name: str,
    v_path: np.ndarray,
    interest_rate_path: np.ndarray,
    inflation_path: np.ndarray,
    interest_rate_params: KnwSvLegParams,
    inflation_params: KnwSvLegParams,
) -> np.ndarray
```

A stochastic deflator ([Cheng & Planchet, 2018](https://hal.science/hal-01730072))
built from an already real-world (P-measure) simulated knw_sv run and this pair's
fitted market price of risk.

In plain terms: multiply a simulated cash flow at time `T` by `D(T)` on the same
path and average across paths, and you get its market value today
(`E^P[D(T)*payoff(T)]`), without running a separate risk-neutral simulation.
`D(T)` combines ordinary discounting at the simulated short rate with a
per-path weight that makes paths the market fears more count for more.

Per step, for the rate leg (inflation is the same with its own parameters): the
P conditional mean is `mu_P = intercept + variance_coupling*v(t) +
own_persistence*r(t) + cross_coupling*pi(t)`, and the market price of risk shifts
it under Q to `mu_Q = mu_P - risk_premium_interest_rate_constant -
risk_premium_interest_rate_variance*v(t)`, with the same `sigma` under both. The
realized standardized shock `z = (r(t+1) - mu_P) / sigma` is recovered from the
simulated path itself (no re-simulation, only inverting the known step formula),
and the step's Girsanov density ratio is `dQ/dP = exp(-theta*z - 0.5*theta^2)` with
`theta = (mu_P - mu_Q) / sigma`. `E^P[dQ/dP] = 1` exactly, the defining property of
a Radon-Nikodym derivative, verified in `tests/models/knw_sv_q/test_knw_sv_q_model.py`.
Full derivation in `knw_sv_q_model.compute_stochastic_deflator`.

Also known as: state-price deflator, pricing kernel, stochastic discount factor.

**Args:**

- <u>interest_rate_name (str):</u> the pair's interest-rate leg's name, as passed to calibrate_mpr().
- <u>v_path (np.ndarray):</u> shape (n_simulations, n_steps+1), the shared latent variance factor's P-measure simulated path. NOTE: the engine deliberately never writes v into `ScenarioSet.paths` (it lives inside the pair's KnwSvVarianceStepper, see engine_controller), so a caller must simulate/record v itself; this method is programmatic-use-only until v is persisted on the run (see the coverage overview's knw_sv_q deflator row).
- <u>interest_rate_path (np.ndarray):</u> shape (n_simulations, n_steps+1), the interest-rate leg's P-measure simulated path (e.g. `ScenarioSet.paths[interest_rate_name]`).
- <u>inflation_path (np.ndarray):</u> shape (n_simulations, n_steps+1), the inflation leg's P-measure simulated path.
- <u>interest_rate_params (KnwSvLegParams):</u> the interest-rate leg's calibrated P-measure parameters, the same ones the simulated path above used (e.g. from the run's own `calibration_metadata`).
- <u>inflation_params (KnwSvLegParams):</u> the inflation leg's calibrated P-measure parameters.

**Returns:**

<u>np.ndarray:</u> shape (n_simulations, n_steps+1), D(0)=1 for every path.

**Raises:**

- <u>RuntimeError:</u> if calibrate_mpr(...) naming this pair hasn't been called yet.
- <u>ValueError:</u> propagated from `compute_stochastic_deflator` when a leg's conditional volatility is exactly zero at some step.

**Notes:**

- `v`'s own CIR shock is deliberately not reweighted: doing so needs the ratio of
  the non-central chi-square transition densities under the P and Q fits of `v`,
  much more involved than the Gaussian case. `v` still drives the rate and
  inflation mean and variance on every step exactly as simulated, but the
  deflator treats the price of `v`'s own risk as zero.
- The accuracy therefore depends on `risk_premium_v`. At `risk_premium_v = 0`
  (`v` has the same dynamics under P and Q) a 40,000-60,000-path average of `D(T)`
  matches the closed-form price within about 0.1-2%, even at realistic
  `variance_coupling`/`variance_sensitivity` and a 10-year maturity. With a
  realistic nonzero premium (about 0.14, some 15% of `v`'s speed, on the
  realistically scaled fit in `tests/models/knw_sv/json/test_knw_sv_model/test_fit_knw_sv_triple.json`),
  `E^P[D(T)]` undershoots the closed-form price by about 1% at 2 years, 8% at
  5 years and 20% at 10 years. Rely on it only when `risk_premium_v` is small
  relative to `v`'s mean-reversion speed, or for short maturities;
  `calibrate_mpr` warns when the premium exceeds 5% of that speed.
- The engine never writes `v` into `ScenarioSet.paths` (it lives inside the pair's
  `KnwSvVarianceStepper`), so for now this is for programmatic use only: the caller
  simulates and records `v` itself, as in the example below.

As an example, continuing from `calibrate_mpr` with a hand-simulated real-world
run:

```python
import numpy as np

from financescenarios.models.knw_sv.knw_sv_controller import variance_factor_name
from financescenarios.models.knw_sv.knw_sv_model import step_knw_sv_leg, step_knw_sv_v

v = knw_sv.params(variance_factor_name("interest_rate"))
rate, inflation = knw_sv.params("interest_rate"), knw_sv.params("inflation")
rng, n_simulations, n_steps, time_step = np.random.default_rng(42), 20_000, 20, 0.25

v_path = np.full((n_simulations, n_steps + 1), v.initial_value)
rate_path = np.full((n_simulations, n_steps + 1), rate.initial_value)
inflation_path = np.full((n_simulations, n_steps + 1), inflation.initial_value)
for t in range(n_steps):
    v_path[:, t + 1] = step_knw_sv_v(
        v_path[:, t], rng.standard_normal(n_simulations), rng.random(n_simulations), time_step, v
    )
    rate_path[:, t + 1] = step_knw_sv_leg(
        rate_path[:, t], rng.standard_normal(n_simulations), time_step, rate, inflation_path[:, t], v_path[:, t]
    )
    inflation_path[:, t + 1] = step_knw_sv_leg(
        inflation_path[:, t], rng.standard_normal(n_simulations), time_step, inflation, rate_path[:, t],
        v_path[:, t],
    )

deflator = knw_sv_q.deflator("interest_rate", v_path, rate_path, inflation_path, rate, inflation)
```

Which returns (calibrated on 2026-10-04):

| T (years) | mean of D(T) | closed-form Q bond price | mean bank-account discount |
|----------:|-------------:|-------------------------:|---------------------------:|
| 1 | 0.2818 | 0.9626 | 0.9607 |
| 2 | 0.0202 | 0.9224 | 0.9235 |
| 5 | 0.0001 | 0.7972 | 0.8302 |

On this live fit the deflator is not usable: `|risk_premium_v|` is 66% of `v`'s
speed and the inflation variance premium is 31, so each step's reweighting is so
extreme that the 20,000-path average collapses toward zero instead of matching the
closed-form price (`exp(-zero_coupon_yield * T)`). This is the regime
`calibrate_mpr` warns about; plain discounting at the simulated rate stays close.

**References:**

- Cheng, P.-K., Planchet, F. (2018). "Stochastic Deflator for an Economic Scenario Generator with Five Factors." HAL preprint hal-01730072. <https://hal.science/hal-01730072>
- Duffie, D., Kan, R. (1996). "A Yield-Factor Model of Interest Rates." Mathematical Finance, 6(4), 379-406. <https://doi.org/10.1111/j.1467-9965.1996.tb00123.x>
