---
title: "KnwSvQ"
seo_title: "KnwSvQ Reference | Finance Scenarios"
seo_title_suffix: false
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

The risk-neutral (Q-measure) side of the KNW models.

```python
from financescenarios.models.knw_sv_q.knw_sv_q_controller import KnwSvQ
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

De Nederlandsche Bank (DNB) fits its Q-measure to nominal yields at 1, 5, 10, 20 and 30 years and real yields
at 1, 5, 15, 20 and 30 ([CP2022 Technical Appendix](
https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix), section 4), and
constrains it with option, swaption and inflation-cap implied volatilities (section 5, eq. 25), data this project
does not have. This module keeps the yield-curve part on the four US Treasury points Yahoo Finance quotes (13
weeks, 5, 10 and 30 years): no real yields and no implied volatilities. The price of risk is completely affine
([Duffie & Kan, 1996](https://doi.org/10.1111/j.1467-9965.1996.tb00123.x)), with five parameters that change only
the drift: under Q, `v`'s mean-reversion speed is its real-world speed plus `risk_premium_v`, and each leg's
`intercept` and `variance_coupling` drop by its constant and variance premium. Everything else stays the same, so
the Q parameters simulate exactly like the P ones. Bond prices come from a discrete-time affine recursion: the
price `n` periods out is `exp(A[n] + Bv[n]*v + Br[n]*r + Bpi[n]*pi)`.

The stochastic deflator follows [Cheng & Planchet (2018)](https://hal.science/hal-01730072): a per-path weight
`D(T)` such that the average of `D(T)*payoff(T)` over a real-world run prices the claim. It is accurate only when
`risk_premium_v` is small relative to `v`'s mean-reversion speed (`calibrate_mpr` warns past 5%), and it needs
the path of `v`, which a scenario set does not include, so you simulate and record it yourself.

The closed-form prices, the market price of risk fit and the deflator all use the correlation of the rate and
inflation shocks, estimated from the same period changes the scenarios' correlation matrix is built from, so model
prices and discounting along simulated paths agree. Limits: the inflation premiums are weakly identified from a
nominal-only curve, and there is no Q-measure equity leg.

Configuration: set `measure: risk_neutral` on both entries of a `method: knw_sv` pair; everything else is as for
`KnwSv`, including `period` equal to `engine.frequency`. The four Treasury tickers (`^IRX`, `^FVX`, `^TNX`,
`^TYX`) are added to the run automatically.

The keys and their defaults are listed on the reference page
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/reference/configuration-classes).

**References:**

- Duffie, D., Kan, R. (1996). "A Yield-Factor Model of Interest Rates." Mathematical Finance, 6(4), 379-406. <https://doi.org/10.1111/j.1467-9965.1996.tb00123.x>
- Cheng, P.-K., Planchet, F. (2018). "Stochastic Deflator for an Economic Scenario Generator with Five Factors." HAL preprint hal-01730072. <https://hal.science/hal-01730072>
- Commissie Parameters (2022). "Technical Appendix: Specification of the CP2022 Model." <https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
KnwSvQ(toolkit: Toolkit)
```

</details>

## calibrate_mpr

Fit the market price of risk of a calibrated knw_sv pair to the observed Treasury yield curve, and store the
matching risk-neutral (Q-measure) parameters for `q_params`, `zero_coupon_yield` and `deflator`.

This finds the five risk premiums that make the model's yields line up with the 13-week, 5-, 10- and 30-year
Treasury yields on every historical date. Under Q, the turbulence factor `v` mean reverts at its real-world
speed plus `risk_premium_v`, and each leg's expected next value drops by its `..._constant` premium plus its
`..._variance` premium times `v`.

The fit minimizes the squared gap between model and observed yields over all four tenors, with the completely
affine form of [Duffie & Kan (1996)](https://doi.org/10.1111/j.1467-9965.1996.tb00123.x). The model yields
include the convexity from the correlation between rate and inflation shocks, the one the scenarios simulate
with. Every date and tenor weighs the same, and the observed yields, those of coupon-paying Treasuries, stand
in for zero-coupon yields: both are judgements, the second close when coupons sit near the yield. The
inflation premiums are only weakly pinned down by a nominal-only curve. When `|risk_premium_v|`
exceeds 5% of `v`'s real-world speed, a warning says `deflator` is materially biased at long maturities.

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

Which returns (calibrated on 2026-10-14):

| risk_premium_v | rate_constant | rate_variance | inflation_constant | inflation_variance |
|---------------:|--------------:|--------------:|-------------------:|-------------------:|
| -0.1536 | 0.0001 | -8.4981 | -0.0027 | 9.3876 |

Under Q, `v` reverts at 0.399 - 0.154 = 0.245 a year toward 1.6 times its historical normal level: the curve
prices in more turbulence than history shows, and the deflator warning fires.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_mpr(
    knw_sv: KnwSv,
    interest_rate_name: str,
    inflation_name: str,
    period: str,
    shock_correlation: float | None = None,
) -> CompletelyAffineMprParams
```

**Args:**

- <u>knw_sv (KnwSv):</u> a `KnwSv` instance with this pair already calibrated.
- <u>interest_rate_name (str):</u> the pair's rate leg name, as passed to `knw_sv.calibrate_triple`.
- <u>inflation_name (str):</u> the pair's inflation leg name, as passed to `knw_sv.calibrate_triple`.
- <u>period (str):</u> the frequency `knw_sv.calibrate_triple` used: "monthly" or "quarterly" ("yearly" raises, as the 13-week tenor is not a whole number of years).
- <u>shock_correlation (float &#124; None):</u> the correlation of the rate and inflation shocks. Defaults to None, the correlation of the two legs' historical period changes, the input of the scenarios' correlation matrix.

**Returns:**

<u>CompletelyAffineMprParams:</u> the five `risk_premium_*` fields.

**Raises:**

- <u>ValueError:</u> if `period` is not supported, a tenor is not a whole number of periods, fewer than 10 dates overlap, or the correlation is not strictly between -1 and 1.
- <u>RuntimeError:</u> if `knw_sv.calibrate_triple` has not been run for this pair.

</details>

## shock_correlation

The correlation of one pair's rate and inflation shocks that its bond prices and deflator use.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
shock_correlation(interest_rate_name: str) -> float
```

**Args:**

- <u>interest_rate_name (str):</u> the pair's rate leg name, as passed to `calibrate_mpr`.

**Raises:**

- <u>RuntimeError:</u> if calibrate_mpr(...) naming this pair hasn't been called yet.

</details>

## mpr

The calibrated market price of risk of one pair.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
mpr(interest_rate_name: str) -> CompletelyAffineMprParams
```

**Args:**

- <u>interest_rate_name (str):</u> the pair's rate leg name, as passed to `calibrate_mpr`.

**Raises:**

- <u>RuntimeError:</u> if calibrate_mpr(...) naming this pair hasn't been called yet.

</details>

## q_params

The risk-neutral (Q-measure) parameters of one pair's `v`, rate and inflation, computed with its market price
of risk. They have the same shapes as the real-world ones from `KnwSv.calibrate_triple` and replace them when
a config sets `measure: risk_neutral`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
q_params(interest_rate_name: str) -> tuple[OUParams, KnwSvLegParams, KnwSvLegParams]
```

**Args:**

- <u>interest_rate_name (str):</u> the pair's rate leg name, as passed to `calibrate_mpr`.

**Returns:**

<u>tuple[OUParams, KnwSvLegParams, KnwSvLegParams]:</u> (v_q, interest_rate_q, inflation_q).

**Raises:**

- <u>RuntimeError:</u> if calibrate_mpr(...) naming this pair hasn't been called yet.

</details>

## zero_coupon_yield

The model's zero-coupon yield at `tenor` years, read off the fitted risk-neutral model at the pair's current
state (the last observed rate, inflation and `v`).

This gives today's yield curve at any maturity that is a whole number of periods, including maturities the
Treasury panel does not quote. A value of 0.04 at `tenor=10` means a 10-year zero-coupon bond is priced at
exp(-0.04 * 10) = 0.67 per unit of face value. The one-period yield equals today's short rate.

The price comes from the discrete-time affine recursion `exp(A[n] + Bv[n]*v + Br[n]*r + Bpi[n]*pi)` with
`n = tenor / period length` ([Duffie & Kan, 1996](https://doi.org/10.1111/j.1467-9965.1996.tb00123.x)), and the
yield, continuously compounded, is `-log(price) / tenor`. The convexity includes the correlation of rate and
inflation shocks, so the price matches the average discount factor along paths simulated under Q.

**As an example:**

Continuing from `calibrate_mpr`.

```python
for tenor in [0.25, 1, 2, 5, 10, 20, 30]:
    print(tenor, knw_sv_q.zero_coupon_yield("interest_rate", tenor))
```

Which returns (calibrated on 2026-10-14):

| tenor (years) | 0.25 | 1 | 2 | 5 | 10 | 20 | 30 |
|:--------------|-----:|--:|--:|--:|---:|---:|---:|
| yield | 0.0375 | 0.0387 | 0.0405 | 0.0447 | 0.0478 | 0.0484 | 0.0483 |

The curve starts at the 3.75% short rate of the last quarter, rises to 4.5% at five years and flattens near
4.8% beyond ten, below the latest observed Treasury yields, since the premiums are fit across the whole
history.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
zero_coupon_yield(interest_rate_name: str, tenor: float) -> float
```

**Args:**

- <u>interest_rate_name (str):</u> the pair's rate leg name, as passed to `calibrate_mpr`.
- <u>tenor (float):</u> the maturity in years, a whole number of periods (0.25, 0.5, ... for a quarterly pair).

**Returns:**

<u>float:</u> the model zero-coupon yield at `tenor`, as a decimal.

**Raises:**

- <u>RuntimeError:</u> if `calibrate_mpr` has not been run for this pair.
- <u>ValueError:</u> if `tenor` is not a whole number of periods.

</details>

## deflator

Build a stochastic deflator ([Cheng & Planchet, 2018](https://hal.science/hal-01730072)) from a real-world
simulated knw_sv run and this pair's fitted market price of risk.

Multiply a simulated cash flow at time `T` by `D(T)` on the same path and average across paths, and you get
its market value today, without a separate risk-neutral simulation. `D(T)` combines discounting at the
simulated short rate with a per-path weight that makes paths the market fears more count for more.

Each step recovers the rate's and inflation's realized shock `z` from the path and weights it by
`exp(-theta*z - 0.5*theta^2)`, where `theta` is the gap between the real-world and risk-neutral expected value
divided by the volatility, with the correlation of the two shocks taken into account. `v`'s own shock is not
reweighted, so the deflator is accurate only when `risk_premium_v` is small relative to `v`'s mean-reversion
speed, or at short maturities; `calibrate_mpr` warns past 5% of that speed. A scenario set does not include
`v`, so you simulate and record it yourself.

**As an example:**

Continuing from `calibrate_mpr`, with `v_path`, `rate_path` and `inflation_path` simulated by hand over 20
quarters and 20,000 paths (seed 42, the rate and inflation shocks correlated at `shock_correlation`, 0.14).

```python
rate, inflation = knw_sv.params("interest_rate"), knw_sv.params("inflation")
deflator = knw_sv_q.deflator("interest_rate", v_path, rate_path, inflation_path, rate, inflation)
```

Which returns (calibrated on 2026-10-14):

| T (years) | mean of D(T) | closed-form Q bond price |
|----------:|-------------:|-------------------------:|
| 1 | 0.9827 | 0.9620 |
| 5 | 0.7606 | 0.7996 |

Here `|risk_premium_v|` is 38.5% of `v`'s speed, so the average misses the bond price, by 2% at one year and 5%
at five: the regime `calibrate_mpr` warns about.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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

**Args:**

- <u>interest_rate_name (str):</u> the pair's rate leg name, as passed to `calibrate_mpr`.
- <u>v_path (np.ndarray):</u> the simulated `v`, one row per scenario and one column per date, the start included.
- <u>interest_rate_path (np.ndarray):</u> the simulated short rate on the same scenarios and dates.
- <u>inflation_path (np.ndarray):</u> the simulated inflation on the same scenarios and dates.
- <u>interest_rate_params (KnwSvLegParams):</u> the real-world rate parameters the paths were simulated with.
- <u>inflation_params (KnwSvLegParams):</u> the real-world inflation parameters, likewise.

**Returns:**

<u>np.ndarray:</u> `D(t)` per scenario and date, equal to 1 at the start of every path.

**Raises:**

- <u>RuntimeError:</u> if `calibrate_mpr` has not been run for this pair.
- <u>ValueError:</u> if a leg's volatility is exactly zero at some step.

</details>

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

### apply_completely_affine_mpr

Turn the real-world (P) parameters of a rate, inflation and turbulence model into risk-neutral (Q) ones, given
the market price of risk.

The market price of risk is the extra expected return investors demand per unit of each risk. Moving to Q
removes it from the drift: rates and inflation are expected lower or higher by their premium, and the
turbulence factor `v` reverts at a different speed toward a different level. A negative `lambda_v` makes `v`
revert more slowly toward a higher level, so the market prices in more turbulence than history shows. The
volatilities stay the same, as Girsanov's theorem requires, and so do the coupling between the legs and today's
values, so Q scenarios are simulated exactly like P scenarios with these parameters.

The formula is as follows:

$$
\kappa ^{Q} = \kappa + \lambda_{v}
$$

$$
\theta ^{Q} = \kappa \cdot \theta / \kappa ^{Q}
$$

$$
c ^{Q} = c - \lambda_{0}
$$

$$
k_{v} ^{Q} = k_{v} - \lambda_{1}
$$

Where kappa and theta are `v`'s real-world speed and level, c and k_v a leg's intercept and coupling to `v`, and
lambda_v, lambda_0 and lambda_1 the market prices of risk of `v` and of the leg (constant and per unit of `v`).

**References:**

- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). "A Theory of the Term Structure of Interest Rates." Econometrica, 53(2), 385-407. The proportional risk premium applied to v. <https://doi.org/10.2307/1911242>
- Duffie, D., Kan, R. (1996). "A Yield-Factor Model of Interest Rates." Mathematical Finance, 6(4), 379-406. The completely-affine market price of risk applied to r and pi. <https://doi.org/10.1111/j.1467-9965.1996.tb00123.x>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
apply_completely_affine_mpr(
    v_params: OUParams,
    interest_rate_params: KnwSvLegParams,
    inflation_params: KnwSvLegParams,
    mpr: CompletelyAffineMprParams,
) -> tuple[OUParams, KnwSvLegParams, KnwSvLegParams]
```

**Args:**

- <u>v_params (OUParams):</u> `v`'s real-world CIR parameters.
- <u>interest_rate_params (KnwSvLegParams):</u> the rate leg's real-world parameters.
- <u>inflation_params (KnwSvLegParams):</u> the inflation leg's real-world parameters.
- <u>mpr (CompletelyAffineMprParams):</u> the market price of risk to apply.

**Returns:**

<u>tuple[OUParams, KnwSvLegParams, KnwSvLegParams]:</u> (v_params_q, interest_rate_params_q, inflation_params_q).

**Raises:**

- <u>ValueError:</u> if kappa^Q is zero or negative (`v` would no longer mean-revert under Q).

</details>

{% raw %}
### compute_stochastic_deflator

Build a stochastic deflator for a real-world run: a per-scenario discount factor that prices cash flows at
market value, so one set of real-world scenarios serves both projection and valuation.

The deflator discounts at the simulated short rate and then reweights each scenario by how much the market
fears it: scenarios whose shocks investors demand a premium for get more weight. The weight is the Girsanov
density of the fitted market price of risk ([Cheng & Planchet, 2018](https://hal.science/hal-01730072)). The
average deflator at T then equals the model's risk-neutral zero-coupon bond price for T, and the average of
deflator times cash flow is the cash flow's market value.

The formula is as follows:

$$
\mu_{t-1} = c + k_{v} \cdot v_{t-1} + \phi_{x} \cdot x_{t-1} + \phi_{y} \cdot y_{t-1}
$$

$$
\sigma_{t-1} = \sqrt{g_{0} + g_{1} \cdot v_{t-1}}
$$

$$
z_{t} = (x_{t} - \mu_{t-1}) / \sigma_{t-1}
$$

$$
\lambda_{t-1} = (\lambda_{0} + \lambda_{1} \cdot v_{t-1}) / \sigma_{t-1}
$$

$$
\ln(D_{t}) = \ln(D_{t-1}) - r_{t-1} \cdot \text{dt} - \lambda_{t-1} ^{T} \cdot R ^{-1} \cdot z_{t} - 0.5 \cdot \lambda_{t-1} ^{T} \cdot R ^{-1} \cdot \lambda_{t-1}
$$

Where x is each leg, y the other one, z_t the pair of real-world shocks read back from the simulated path,
lambda_t-1 the pair of prices of risk and R the 2x2 correlation matrix of the rate and inflation shocks (rho
off the diagonal). The correlation matters: the scenarios draw correlated shocks, and a weight that treated them
as independent would no longer average to the bond price. `v`'s own shock is not reweighted, so the deflator is
accurate only when `v`'s risk premium is small relative to its mean-reversion speed; `v` still drives both legs'
drift and variance.

**References:**

- Cheng, P.-K., Planchet, F. (2018). "Stochastic Deflator for an Economic Scenario Generator with Five Factors." HAL preprint hal-01730072. <https://hal.science/hal-01730072>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
compute_stochastic_deflator(
    v_path: np.ndarray,
    interest_rate_path: np.ndarray,
    inflation_path: np.ndarray,
    interest_rate_params: KnwSvLegParams,
    inflation_params: KnwSvLegParams,
    mpr: CompletelyAffineMprParams,
    time_step: float,
    shock_correlation: float = 0.0,
) -> np.ndarray
```

**Args:**

- <u>v_path (np.ndarray):</u> the simulated turbulence factor, one row per scenario and one column per date.
- <u>interest_rate_path (np.ndarray):</u> the simulated short rate on the same scenarios and dates.
- <u>inflation_path (np.ndarray):</u> the simulated inflation on the same scenarios and dates.
- <u>interest_rate_params (KnwSvLegParams):</u> the real-world rate parameters the scenarios were simulated with.
- <u>inflation_params (KnwSvLegParams):</u> the real-world inflation parameters.
- <u>mpr (CompletelyAffineMprParams):</u> the fitted market price of risk (see `calibrate_completely_affine_mpr`).
- <u>time_step (float):</u> dt, in years.
- <u>shock_correlation (float):</u> rho, the correlation of the rate and inflation shocks the scenarios were simulated with. Defaults to 0.0.

**Returns:**

<u>np.ndarray:</u> D_t per scenario and date, with D_0 = 1 in every scenario.

**Raises:**

- <u>ValueError:</u> if a leg's volatility is exactly 0 at some step, so its shock cannot be read back, or the correlation is not strictly between -1 and 1.

</details>
{% endraw %}

### zero_coupon_bond_recursion

Price risk-neutral zero-coupon bonds at every maturity in closed form, as an exponential of a linear function of
today's turbulence, short rate and inflation.

Because the model is affine ([Duffie & Kan, 1996](https://doi.org/10.1111/j.1467-9965.1996.tb00123.x)), the
price of a bond maturing n periods out is P(n) = exp(A(n) + Bv(n) * v + Br(n) * r + Bpi(n) * pi). The
coefficients follow from one period of discounting at the short rate and the risk-neutral expectation of next
period's bond price, so they build up maturity by maturity without simulation. Br says how much a bond's log
price falls when the short rate rises, the model's duration; Bpi carries inflation's feed into future rates;
Bv says how turbulence moves prices, through expected rates, convexity and the risk premium.

The formula is as follows:

$$
\operatorname{Q0}(n) = 0.5 \cdot (\operatorname{Br}(n) ^{2} \cdot g_{0r} + \operatorname{Bpi}(n) ^{2} \cdot g_{0 \pi}) + \rho \cdot \operatorname{Br}(n) \cdot \operatorname{Bpi}(n) \cdot h_{0}
$$

$$
\operatorname{Q1}(n) = 0.5 \cdot (\operatorname{Br}(n) ^{2} \cdot g_{1r} + \operatorname{Bpi}(n) ^{2} \cdot g_{1 \pi}) + \rho \cdot \operatorname{Br}(n) \cdot \operatorname{Bpi}(n) \cdot h_{1}
$$

$$
A(n + 1) = A(n) + C(\operatorname{Bv}(n)) + \operatorname{Br}(n) \cdot c_{r} + \operatorname{Bpi}(n) \cdot c_{\pi} + \operatorname{Q0}(n)
$$

$$
\operatorname{Bv}(n + 1) = L(\operatorname{Bv}(n)) + \operatorname{Br}(n) \cdot k_{vr} + \operatorname{Bpi}(n) \cdot k_{v \pi} + \operatorname{Q1}(n)
$$

$$
\operatorname{Br}(n + 1) = \operatorname{Br}(n) \cdot \phi_{rr} + \operatorname{Bpi}(n) \cdot \phi_{\pi r} - \text{dt}
$$

$$
\operatorname{Bpi}(n + 1) = \operatorname{Br}(n) \cdot \phi_{r \pi} + \operatorname{Bpi}(n) \cdot \phi_{\pi \pi}
$$

Where A(0) = Bv(0) = Br(0) = Bpi(0) = 0, L and C come from the closed-form expectation of the CIR process `v`
([Cox, Ingersoll & Ross, 1985](https://doi.org/10.2307/1911242)), the r and pi suffixes name the leg, phi_pir is
the inflation leg's coefficient on r and phi_rpi the rate leg's on pi. Q0 and Q1 are the convexity of the bond
price: half the variance of next period's log price, the rate-inflation covariance included.

rho is the correlation of the rate and inflation shocks, the same one the scenarios draw with, so model prices
and discounting along the simulated paths agree. Their covariance rho * sqrt(g_0r + g_1r * v) *
sqrt(g_0pi + g_1pi * v) is not linear in `v` unless both legs load on `v` in the same proportion, so it is
replaced by its tangent h_0 + h_1 * v at `v`'s risk-neutral long-run level: exact at constant volatility and for
proportional loadings, and off only to second order in `v`'s distance from that level otherwise. `v`'s own shock
is independent of both legs, as in the scenarios.

**References:**

- Duffie, D., Kan, R. (1996). "A Yield-Factor Model of Interest Rates." Mathematical Finance, 6(4), 379-406. <https://doi.org/10.1111/j.1467-9965.1996.tb00123.x>
- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). "A Theory of the Term Structure of Interest Rates." Econometrica, 53(2), 385-407. <https://doi.org/10.2307/1911242>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
zero_coupon_bond_recursion(
    v_params_q: OUParams,
    interest_rate_params_q: KnwSvLegParams,
    inflation_params_q: KnwSvLegParams,
    time_step: float,
    n_periods: int,
    shock_correlation: float = 0.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
```

**Args:**

- <u>v_params_q (OUParams):</u> `v`'s risk-neutral CIR parameters (see `apply_completely_affine_mpr`).
- <u>interest_rate_params_q (KnwSvLegParams):</u> the rate leg's risk-neutral parameters.
- <u>inflation_params_q (KnwSvLegParams):</u> the inflation leg's risk-neutral parameters.
- <u>time_step (float):</u> dt, years per period.
- <u>n_periods (int):</u> the longest maturity, in periods.
- <u>shock_correlation (float):</u> rho, the correlation of the rate and inflation shocks. Defaults to 0.0.

**Returns:**

<u>tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:</u> (A, Bv, Br, Bpi), one value per maturity from 0 to `n_periods` periods.

**Raises:**

- <u>ValueError:</u> if the correlation is not strictly between -1 and 1.

</details>

### zero_coupon_yield

The continuously compounded zero-coupon yield n periods to maturity, given today's turbulence, short rate and
inflation, from the bond price coefficients of `zero_coupon_bond_recursion`.

Because the yield is linear in the state, a whole yield curve moves with the short rate, inflation and `v` in a
fixed pattern: a higher short rate lifts short yields most, as it mean-reverts before long bonds mature, and
inflation moves the curve through its feed into future rates.

The formula is as follows:

$$
y(n) = - (A(n) + \operatorname{Bv}(n) \cdot v + \operatorname{Br}(n) \cdot r + \operatorname{Bpi}(n) \cdot \pi) / (n \cdot \text{dt})
$$

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
zero_coupon_yield(
    v: float | np.ndarray,
    interest_rate: float | np.ndarray,
    inflation: float | np.ndarray,
    a: np.ndarray,
    bv: np.ndarray,
    br: np.ndarray,
    bpi: np.ndarray,
    n_periods: int,
    time_step: float,
) -> float | np.ndarray
```

**Args:**

- <u>v (float &#124; np.ndarray):</u> the turbulence factor, in one or many scenarios.
- <u>interest_rate (float &#124; np.ndarray):</u> the short rate.
- <u>inflation (float &#124; np.ndarray):</u> inflation.
- <u>a (np.ndarray):</u> the A coefficients by maturity.
- <u>bv (np.ndarray):</u> the Bv coefficients by maturity.
- <u>br (np.ndarray):</u> the Br coefficients by maturity.
- <u>bpi (np.ndarray):</u> the Bpi coefficients by maturity.
- <u>n_periods (int):</u> the maturity n, in periods, at least 1.
- <u>time_step (float):</u> dt, years per period.

**Returns:**

<u>float &#124; np.ndarray:</u> the yield, as a decimal, per scenario.

**Raises:**

- <u>ValueError:</u> if `n_periods` is not at least 1.

</details>

{% raw %}
### calibrate_completely_affine_mpr

Fit the market price of risk so the model's yield curve matches the observed one across history.

A real-world rate model fitted on the short rate alone says nothing about term premiums: why a 10-year yield
sits above the expected path of short rates. The market price of risk fills that gap. Its five parameters are
chosen so that, on every historical date, the model's yields at the observed maturities are as close as
possible to the observed yields, given that date's rate, inflation and turbulence. The premiums are completely
affine ([Duffie & Kan, 1996](https://doi.org/10.1111/j.1467-9965.1996.tb00123.x)): a constant plus a part
proportional to `v`, so investors can demand more compensation in turbulent markets. `v` is not observed, so
its history is the same estimate the real-world fit used (`compute_v_proxy`). With a nominal curve only, the
inflation premiums are weakly identified.

The formula is as follows:

$$
\text{loss} = \operatorname{sum}((y_{\text{model}} - y_{\text{observed}}) ^{2}),\;\; \text{over dates t and tenors n}
$$

Where the five lambdas minimize the loss and y_model is `zero_coupon_yield` under the risk-neutral parameters
from `apply_completely_affine_mpr`. lambda_v is bounded so `v` still mean-reverts under Q.

**References:**

- Duffie, D., Kan, R. (1996). "A Yield-Factor Model of Interest Rates." Mathematical Finance, 6(4), 379-406. <https://doi.org/10.1111/j.1467-9965.1996.tb00123.x>
- Diebold, F.X., Li, C. (2006). "Forecasting the term structure of government bond yields." Journal of Econometrics, 130(2), 337-364. The four-tenor Treasury panel calibrated against. <https://doi.org/10.1016/j.jeconom.2005.03.005>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_completely_affine_mpr(
    v_params: OUParams,
    interest_rate_params: KnwSvLegParams,
    inflation_params: KnwSvLegParams,
    time_step: float,
    state_dates: pl.Series,
    v_series: pl.Series,
    interest_rate_series: pl.Series,
    inflation_series: pl.Series,
    yield_dates: pl.Series,
    yields_by_tenor: dict[float, pl.Series],
    shock_correlation: float = 0.0,
) -> CompletelyAffineMprParams
```

**Args:**

- <u>v_params (OUParams):</u> `v`'s calibrated real-world CIR parameters.
- <u>interest_rate_params (KnwSvLegParams):</u> the rate leg's calibrated real-world parameters.
- <u>inflation_params (KnwSvLegParams):</u> the inflation leg's calibrated real-world parameters.
- <u>time_step (float):</u> the years per period; every maturity must be a whole number of periods.
- <u>state_dates (pl.Series):</u> the dates of the rate, inflation and `v` history.
- <u>v_series (pl.Series):</u> the estimated `v` on each of those dates.
- <u>interest_rate_series (pl.Series):</u> the short rate on each of those dates.
- <u>inflation_series (pl.Series):</u> inflation on each of those dates.
- <u>yield_dates (pl.Series):</u> the dates of the observed yield curve.
- <u>yields_by_tenor (dict[float, pl.Series]):</u> the observed yield history per maturity in years.
- <u>shock_correlation (float):</u> the correlation of the rate and inflation shocks, as in the scenarios. Defaults to 0.0.

**Returns:**

<u>CompletelyAffineMprParams:</u> the calibrated market price of risk.

**Raises:**

- <u>ValueError:</u> if a maturity is not a whole number of periods, or fewer than 10 dates are covered by both the state history and the yield curve.

</details>
{% endraw %}
