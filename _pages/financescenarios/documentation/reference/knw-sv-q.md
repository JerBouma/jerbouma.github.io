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

The KnwSvQ module turns a calibrated `KnwSv` pair into a risk-neutral (Q-measure) model: it learns the market
price of risk that makes the model reproduce the observed Treasury yield curve, and then prices zero-coupon bonds
in closed form, simulates the pair under Q, or builds a stochastic deflator for a real-world run.

A real-world (P-measure) simulation answers "where might rates go?", while pricing needs the risk-neutral view
"what is a future cash flow worth today?". The bridge between the two is the market price of risk, the extra
return investors demand for bearing each source of risk. This module fits that price so the model's yields match
the 13-week, 5-, 10- and 30-year Treasury yields, then gives you model yields at any maturity
(`zero_coupon_yield`), the Q-measure parameters to simulate with (`q_params`) and a deflator to price claims off
a real-world run (`deflator`).

De Nederlandsche Bank (DNB) derives the Q-measure of its scenario sets from option, swaption and inflation-cap
prices ([CP2022 Technical Appendix](
https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix), sections 5-6), data
this project does not have. This module fits the market price of risk to the yield curve instead: a different,
not merely simplified, alternative. The price of risk is completely affine
([Duffie & Kan, 1996](https://doi.org/10.1111/j.1467-9965.1996.tb00123.x)), with five parameters that change only
the drift: under Q, `v`'s mean-reversion speed is its real-world speed plus `risk_premium_v`, and each leg's
`intercept` and `variance_coupling` drop by its constant and variance premium. Everything else stays the same, so
the Q parameters simulate exactly like the P ones. Bond prices come from a discrete-time affine recursion: the
price `n` periods out is `exp(A[n] + Bv[n]*v + Br[n]*r + Bpi[n]*pi)`.

The stochastic deflator follows [Cheng & Planchet (2018)](https://hal.science/hal-01730072): a per-path weight
`D(T)` such that the average of `D(T)*payoff(T)` over a real-world run prices the claim. It is accurate only when
`risk_premium_v` is small relative to `v`'s mean-reversion speed (`calibrate_mpr` warns past 5%), and it is for
programmatic use: the engine does not store `v`'s path, so you simulate and record it yourself.

Limits: the closed-form prices assume uncorrelated rate and inflation shocks (the Monte Carlo engine does not),
the inflation premiums are weakly identified from a nominal-only curve, and there is no Q-measure equity leg.

Configuration: set `measure: risk_neutral` on both entries of a `method: knw_sv` pair; everything else is as for
`KnwSv`, including `period` equal to `engine.frequency`. The four Treasury tickers (`^IRX`, `^FVX`, `^TNX`,
`^TYX`) are added to the run automatically.

| Key | Default | Meaning |
|:----|:--------|:--------|
| `interest_rates[i].measure` | `real_world` | `risk_neutral` fits the market price of risk and simulates under Q. |
| `inflation[j].measure` | `real_world` | Must equal the paired rate entry's `measure`. |

**References:**

- Duffie, D., Kan, R. (1996). "A Yield-Factor Model of Interest Rates." Mathematical Finance, 6(4), 379-406. <https://doi.org/10.1111/j.1467-9965.1996.tb00123.x>
- Cheng, P.-K., Planchet, F. (2018). "Stochastic Deflator for an Economic Scenario Generator with Five Factors." HAL preprint hal-01730072. <https://hal.science/hal-01730072>
- Commissie Parameters (2022). "Technical Appendix: Specification of the CP2022 Model." <https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix>

## calibrate_mpr

```python
calibrate_mpr(
    knw_sv: KnwSv,
    interest_rate_name: str,
    inflation_name: str,
    period: str,
) -> CompletelyAffineMprParams
```

Fit the market price of risk of a calibrated knw_sv pair to the observed Treasury yield curve, and store the
matching risk-neutral (Q-measure) parameters for `q_params`, `zero_coupon_yield` and `deflator`.

This finds the five risk premiums that make the model's yields line up with the 13-week, 5-, 10- and 30-year
Treasury yields on every historical date. Under Q, the turbulence factor `v` mean reverts at its real-world
speed plus `risk_premium_v`, and each leg's expected next value drops by its `..._constant` premium plus its
`..._variance` premium times `v`.

The fit minimizes the squared gap between model and observed yields over all four tenors, with the completely
affine form of [Duffie & Kan (1996)](https://doi.org/10.1111/j.1467-9965.1996.tb00123.x). The inflation
premiums are only weakly pinned down by a nominal-only curve. When `|risk_premium_v|` exceeds 5% of `v`'s
real-world speed, a warning says `deflator` is materially biased at long maturities.

**Args:**

- <u>knw_sv (KnwSv):</u> a `KnwSv` instance with this pair already calibrated.
- <u>interest_rate_name (str):</u> the pair's rate leg name, as passed to `knw_sv.calibrate_triple`.
- <u>inflation_name (str):</u> the pair's inflation leg name, as passed to `knw_sv.calibrate_triple`.
- <u>period (str):</u> the frequency `knw_sv.calibrate_triple` used: "monthly" or "quarterly" ("yearly" raises, as the 13-week tenor is not a whole number of years).

**Returns:**

<u>CompletelyAffineMprParams:</u> the five `risk_premium_*` fields.

**Raises:**

- <u>ValueError:</u> if `period` is not supported, a tenor is not a whole number of periods, or fewer than 10 dates overlap.
- <u>RuntimeError:</u> if `knw_sv.calibrate_triple` has not been run for this pair.

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

Under Q, `v` reverts at 0.399 - 0.153 = 0.246 a year toward 1.6 times its historical normal level: the curve
prices in more turbulence than history shows, and the deflator warning fires.

## mpr

```python
mpr(interest_rate_name: str) -> CompletelyAffineMprParams
```

The calibrated market price of risk of one pair.

**Args:**

- <u>interest_rate_name (str):</u> the pair's rate leg name, as passed to `calibrate_mpr`.

**Raises:**

- <u>RuntimeError:</u> if calibrate_mpr(...) naming this pair hasn't been called yet.

## q_params

```python
q_params(interest_rate_name: str) -> tuple[OUParams, KnwSvLegParams, KnwSvLegParams]
```

The risk-neutral (Q-measure) parameters of one pair's `v`, rate and inflation, computed with its market price
of risk. They have the same shapes as the real-world ones from `KnwSv.calibrate_triple` and replace them when
a config sets `measure: risk_neutral`.

**Args:**

- <u>interest_rate_name (str):</u> the pair's rate leg name, as passed to `calibrate_mpr`.

**Returns:**

<u>tuple[OUParams, KnwSvLegParams, KnwSvLegParams]:</u> (v_q, interest_rate_q, inflation_q).

**Raises:**

- <u>RuntimeError:</u> if calibrate_mpr(...) naming this pair hasn't been called yet.

## zero_coupon_yield

```python
zero_coupon_yield(interest_rate_name: str, tenor: float) -> float
```

The model's zero-coupon yield at `tenor` years, read off the fitted risk-neutral model at the pair's current
state (the last observed rate, inflation and `v`).

This gives today's yield curve at any maturity that is a whole number of periods, including maturities the
Treasury panel does not quote. A value of 0.04 at `tenor=10` means a 10-year zero-coupon bond is priced at
exp(-0.04 * 10) = 0.67 per unit of face value. The one-period yield equals today's short rate.

The price comes from the discrete-time affine recursion `exp(A[n] + Bv[n]*v + Br[n]*r + Bpi[n]*pi)` with
`n = tenor / period length` ([Duffie & Kan, 1996](https://doi.org/10.1111/j.1467-9965.1996.tb00123.x)), and the
yield, continuously compounded, is `-log(price) / tenor`. It assumes uncorrelated rate and inflation shocks,
which the Monte Carlo engine does not.

**Args:**

- <u>interest_rate_name (str):</u> the pair's rate leg name, as passed to `calibrate_mpr`.
- <u>tenor (float):</u> the maturity in years, a whole number of periods (0.25, 0.5, ... for a quarterly pair).

**Returns:**

<u>float:</u> the model zero-coupon yield at `tenor`, as a decimal.

**Raises:**

- <u>RuntimeError:</u> if `calibrate_mpr` has not been run for this pair. ValueError: if `tenor` is not a whole number of periods.
- <u>As an example, continuing from `calibrate_mpr`:</u> 
- ```python
- <u>for tenor in [0.25, 1, 2, 5, 10, 20, 30]:</u> print(tenor, knw_sv_q.zero_coupon_yield("interest_rate", tenor))
- ```
- <u>Which returns (calibrated on 2026-10-04):</u> 
- | tenor (years) | 0.25 | 1 | 2 | 5 | 10 | 20 | 30 |
- <u>&#124;:</u> --------------|-----:|--:|--:|--:|---:|---:|---:|
- | yield | 0.0375 | 0.0381 | 0.0404 | 0.0453 | 0.0487 | 0.0496 | 0.0492 |
- The curve starts at today's 3.75% short rate, rises to 4.5% at five years and flattens just under 5% beyond
- ten, below the latest observed Treasury yields, since the premiums are fit across the whole history.

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

Build a stochastic deflator ([Cheng & Planchet, 2018](https://hal.science/hal-01730072)) from a real-world
simulated knw_sv run and this pair's fitted market price of risk.

Multiply a simulated cash flow at time `T` by `D(T)` on the same path and average across paths, and you get
its market value today, without a separate risk-neutral simulation. `D(T)` combines discounting at the
simulated short rate with a per-path weight that makes paths the market fears more count for more.

Each step recovers the rate's and inflation's realized shock `z` from the path and weights it by
`exp(-theta*z - 0.5*theta^2)`, where `theta` is the gap between the real-world and risk-neutral expected value
divided by the volatility. `v`'s own shock is not reweighted, so the deflator is accurate only when
`risk_premium_v` is small relative to `v`'s mean-reversion speed, or at short maturities; `calibrate_mpr` warns
past 5% of that speed. It is for programmatic use: the engine does not store `v` in `ScenarioSet.paths`, so you
simulate and record `v` yourself.

**Args:**

- <u>interest_rate_name (str):</u> the pair's rate leg name, as passed to `calibrate_mpr`.
- <u>v_path (np.ndarray):</u> the simulated `v`, shape (n_simulations, n_steps + 1).
- <u>interest_rate_path (np.ndarray):</u> the simulated rate, same shape (e.g. `ScenarioSet.paths[name]`).
- <u>inflation_path (np.ndarray):</u> the simulated inflation, same shape.
- <u>interest_rate_params (KnwSvLegParams):</u> the real-world rate parameters the paths were simulated with.
- <u>inflation_params (KnwSvLegParams):</u> the real-world inflation parameters, likewise.

**Returns:**

<u>np.ndarray:</u> `D(t)`, shape (n_simulations, n_steps + 1), equal to 1 at the start of every path.

**Raises:**

- <u>RuntimeError:</u> if `calibrate_mpr` has not been run for this pair. ValueError: if a leg's volatility is exactly zero at some step.
- As an example, continuing from `calibrate_mpr`, with `v_path`, `rate_path` and `inflation_path` simulated by
- <u>hand over 20 quarters and 20,000 paths:</u> 
- ```python
- rate, inflation = knw_sv.params("interest_rate"), knw_sv.params("inflation")
- deflator = knw_sv_q.deflator("interest_rate", v_path, rate_path, inflation_path, rate, inflation)
- ```
- <u>Which returns (calibrated on 2026-10-04):</u> 
- | T (years) | mean of D(T) | closed-form Q bond price |
- <u>&#124;----------:</u> |-------------:|-------------------------:|
- | 1 | 0.2818 | 0.9626 |
- | 5 | 0.0001 | 0.7972 |
- Here `|risk_premium_v|` is 66% of `v`'s speed, so the average collapses toward zero instead of matching the
- <u>bond price:</u> the regime `calibrate_mpr` warns about.
