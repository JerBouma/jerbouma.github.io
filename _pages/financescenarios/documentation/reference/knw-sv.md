---
title: "KnwSv"
seo_title: "KnwSv Reference – Finance Scenarios"
excerpt: "The KNW model with stochastic volatility."
description: "The KNW model with stochastic volatility."
author_profile: false
permalink: /projects/financescenarios/docs/reference/knw-sv
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

The KNW model with stochastic volatility. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.models.knw_sv.knw_sv_controller import KnwSv
```

```python
KnwSv(toolkit: Toolkit)
```

The KnwSv module simulates the interest rate and inflation as a two-way coupled pair,
like `Knw`, but adds a shared, hidden "market nervousness" factor `v` that makes both
of them swing harder in turbulent periods and calmer in quiet ones. Optionally an
equity index can read the same `v`, so stock market and rate turbulence rise together.

In plain terms: `Knw` gives the rate and inflation a fixed amount of randomness every
period. Real markets have spells of calm and spells of stress, and DNB's CP2022
scenario model captures that with a stochastic variance factor that scales the
volatility of everything. This module brings that factor back: you get the same
rate/inflation pair as `Knw`, but with volatility that clusters over time, and
optionally an equity leg on top that earns the simulated short rate plus a risk
premium, with its own volatility tied to the same `v`. One instance holds any number of
independently calibrated pairs, one `calibrate_triple()` call each.

The model is the stochastic-volatility extension of `Knw`'s VAR(1). `v` follows a CIR
process ([Cox, Ingersoll & Ross, 1985](https://doi.org/10.2307/1911242)), the
mean-reverting, never-negative process [Heston (1993)](https://doi.org/10.1093/rfs/6.2.327)
uses for variance, and both legs read its previous level in their drift and their
variance:

```text
v(t)  = v's own CIR process (Andersen QE), with no cross-coupling in its own row
r(t)  = c_r  + gamma_r*v(t-1)  + phi_rr*r(t-1)   + phi_r_pi*pi(t-1)
        + sqrt(base_r  + sens_r*v(t-1))*z_r(t)
pi(t) = c_pi + gamma_pi*v(t-1) + phi_pi_r*r(t-1) + phi_pipi*pi(t-1)
        + sqrt(base_pi + sens_pi*v(t-1))*z_pi(t)
```

- `v`'s row is a standard CIR process (mean-reversion speed, long-run mean and
  volatility-of-volatility, Feller-condition checked), fit with
  `interest_rates_model.fit_cir_process` unmodified and returned as an `OUParams` with
  `family="cir"`, the same type the CIR short-rate factor uses.
- `gamma_r`/`gamma_pi` (`variance_coupling`): how much of `v`'s level feeds each leg's
  next-period drift (`K_rv`/`K_piv` in DNB's state matrix). Not forced to zero, since
  DNB's `K` matrix has no such constraint: `v` drives the level, not only the noise.
- `phi_rr`/`phi_pipi` (`own_persistence`) and `phi_r_pi`/`phi_pi_r` (`cross_coupling`):
  the same two-way VAR(1) coupling as `Knw`.
- `base_r`/`base_pi` (`base_variance`) and `sens_r`/`sens_pi` (`variance_sensitivity`):
  each leg's variance is `base_variance + variance_sensitivity * v(t-1)`, matching
  `Sigma^rpi(Gamma0 + v_t*Gamma)^0.5` in DNB's Technical Appendix (eq. 2-3). With
  `variance_coupling = variance_sensitivity = 0` on both legs this is exactly `Knw`'s
  shape: `KnwSvLegParams` is a strict superset, not a parallel model.

Estimating `v`: DNB recovers `v` by inverting its closed-form yield curve against
market yields on every historical date, risk-neutral machinery this project does not
build. Instead a first constant-volatility fit (the same one `Knw` performs, run only
for its residuals) gives squared surprises, a rolling four-period average of those
serves as a realized-variance proxy for `v`, and a CIR process is fit to that proxy
(`knw_sv_model.compute_v_proxy` and `fit_knw_sv_triple`). The proxy is lagged: the row
for transition `t` carries the window ending at `t-1`, never `t`'s own residual, since
a window ending at `t` regresses each residual on itself and invents variance coupling
(under a no-coupling null that version reports a `variance_sensitivity` of about 0.64,
the lagged one about 0). This is structurally faithful to `v` being a mean-reverting
variance process and econometrically simpler than DNB's market-yield inversion.

Simulating `v`: `v` is stepped with [Andersen's (2008)](https://doi.org/10.21314/jcf.2008.189)
Quadratic-Exponential (QE) scheme (`knw_sv_model.step_knw_sv_v`), not the
full-truncation Euler scheme `interest_rates_model.step_cir` uses for the CIR short
rate. That stepper already names QE as the next step if its bias ever mattered, and
here it does: both legs' volatility is proportional to `v`, so any bias in `v` feeds
straight into theirs. QE is (near) bias-free and never negative by construction: it
matches the true conditional distribution (a scaled non-central chi-square) with a
squared Gaussian when `v` is high enough for that to be close to Gaussian, and with a
Bernoulli-plus-exponential mixture when `v` is near zero, where the true distribution
has a probability mass at the origin a Gaussian cannot represent.

How `v` is shared: `v` is deliberately not a first-class simulated factor. It has no
historical series of its own, and pushing it through the correlation matrix and
dependency graph every real factor goes through would be a category error. Instead
`knw_sv_model.KnwSvVarianceStepper` carries `v`'s state privately (the pattern
`calibration_model.GARCHStepper` uses for GARCH variance), shared by the pair's two
legs and the optional equity leg. The engine does not promise which leg it steps
first, and both must see the same `v(t-1)`, so the stepper uses a two-phase
read/advance protocol (see its docstring). The rate and inflation legs keep `Knw`'s
bidirectional, order-free relationship, both reading only lag-1 values:

```text
    v (internal, shared)
 /          |          \
v           v           v
```

   interest_rate (knw_sv) <--> inflation (knw_sv)     equity (knw_sv, optional)

The equity leg (`calibrate_equity_leg`) follows DNB's eq. 4/5 log-price row,
`d ln(S_t) = (r_t + eta_S)dt - 0.5*var*dt + sqrt(var)*dW_t` with
`var = Gamma0 + v_t*Gamma`: the drift is the paired short rate plus a constant risk
premium `eta_S`, and the variance is scaled by the same `v`. It reads `v` and the rate
one way; `v`'s own process never reads equity back, matching DNB's eq. 4, where the
equity and CPI index rows are driven by the state vector but do not drive it. It adds
no new latent state, only one more reader of the shared stepper.

The data are the same as `Knw`'s, with no API key needed: the rate leg from a Treasury
ticker or the OECD short or long rate (`interest_rates_controller.fetch_short_rate`),
the inflation leg from OECD consumer price index growth, year over year, and for the
equity leg any index price series (in a full run, `equities_controller.fetch_equity_prices`
on the equity entry's ticker). `v` has no config entry and no fetched series.

What it does not do, on top of everything `Knw` already leaves out:
- No DNB-faithful risk-neutral (Q-measure) variant: DNB's essentially-affine market
  price of risk (`M = K + Sigma*lambda1`) is calibrated jointly against option,
  swaption and inflation-cap prices (Technical Appendix, sections 5-6), and this project
  has no such data (only single-point equity at-the-money implied volatility and
  commodity forward curves exist anywhere in the codebase). `KnwSvQ` builds a genuine,
  closed-form Q-measure instead, fit to the observed yield curve and restricted to a
  completely-affine specification.
- `v` is a realized-variance proxy, not DNB's market-recovered series: a different
  (not merely simplified) estimate, since DNB's method needs the Q-measure machinery.
- The equity leg is a real-world, history-only fit: DNB constrains `eta_S` and the
  equity variance jointly against equity-derivative implied volatility (eq. 25,
  `e_eq(Theta)^2 <= (1.50%)^2`) alongside rate and inflation derivatives, market data
  this project has no source for, so this is a materially simpler, less constrained
  estimate. DNB's CPI index row (eq. 4's second output) stays out of scope, and
  `dividend_yield` keeps the default OU process.
- No leverage effect: `v`'s own shocks are drawn independently of the rate and
  inflation shocks (from the engine's shared random generator, not a correlated shock
  column), so a shock to `v` is not correlated with a shock to either leg beyond what
  `variance_coupling`/`variance_sensitivity` encode through `v`'s level. DNB's
  `Sigma^rpi` has off-diagonal `sigma_rv`/`sigma_piv` terms for exactly this; they are
  not fit here.

Configuration (both entries of a pair, plus an optional equity entry, in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `interest_rates[i].method` | `hull_white` | Set to `knw_sv` to make this entry the pair's rate leg. |
| `interest_rates[i].inflation_name` | `inflation` | The `name` of the paired `inflation[j]` entry. |
| `interest_rates[i].source`, `ticker`, `country`, `term` | `ticker`, ... | Rate data source, as for `Knw`. |
| `interest_rates[i].period` | `daily` | Shared by every entry using this `v`, equal to `engine.frequency`. |
| `interest_rates[i].measure` | `real_world` | `risk_neutral` simulates under `KnwSvQ`'s Q-measure. |
| `inflation[j].method` | `ou` | Set to `knw_sv` to make this entry the pair's inflation leg. |
| `inflation[j].interest_rate_name` | `interest_rate` | The `name` of the paired `interest_rates[i]` entry. |
| `inflation[j].country` | `United States` | The country whose OECD consumer price index is used. |
| `inflation[j].measure` | `real_world` | Must equal the rate leg's `measure`. |
| `equities[k].method` | (regime switching) | Set to `knw_sv` to add an equity leg reading the pair's `v`. |
| `equities[k].nominal_rate_name` | `null` | Required for `knw_sv`: the pair's rate entry `name`. |

The pairing rules are `Knw`'s (mutual naming, one shared `period`, no beliefs, no
GARCH or business-cycle conditioning), and a `knw_sv` entry's partner must also be
`knw_sv`, since the two methods fit different systems. Every entry sharing a `v` must
use the same `period`, equal to `engine.frequency`: `step_knw_sv_leg` and
`step_knw_sv_equity` apply their fit once per engine step, so a mismatch silently
compounds too fast or too slow (confirmed live: the equity leg overshot DNB CP2022's
median by 15-20 percentage points a year at a monthly engine frequency, and by 0.5-1.6
points once matched to quarterly). `ScenariosConfig` rejects a mismatch, and rejects an
equity leg that names a `measure: risk_neutral` rate.

**References:**

- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). "A Theory of the Term Structure of Interest Rates." Econometrica, 53(2), 385-407. <https://doi.org/10.2307/1911242>
- Heston, S.L. (1993). "A Closed-Form Solution for Options with Stochastic Volatility with Applications to Bond and Currency Options." The Review of Financial Studies, 6(2), 327-343. <https://doi.org/10.1093/rfs/6.2.327>
- Andersen, L. (2008). "Simple and Efficient Simulation of the Heston Stochastic Volatility Model." Journal of Computational Finance, 11(3), 1-42. <https://doi.org/10.21314/jcf.2008.189>
- Commissie Parameters (2022). "Technical Appendix: Specification of the CP2022 Model." Published with De Nederlandsche Bank's scenario sets; eq. 2-5 are the state and equity dynamics this real-world, proxy-estimated special case implements. <https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix>
- Koijen, R.S.J., Nijman, T.E., Werker, B.J.M. (2010). "When Can Life Cycle Investors Benefit from Time-Varying Bond Risk Premia?" The Review of Financial Studies, 23(2), 741-780. <https://doi.org/10.1093/rfs/hhp058>
- Lutkepohl, H. (2005). "New Introduction to Multiple Time Series Analysis." Springer. <https://doi.org/10.1007/978-3-540-27752-1>

## calibrate_triple

```python
calibrate_triple(
    interest_rate_name: str,
    inflation_name: str,
    period: str,
    interest_rate_source: str = 'oecd',
    interest_rate_ticker: str = '^IRX',
    interest_rate_country: str = 'United States',
    interest_rate_term: str = 'short',
    inflation_country: str = 'United States',
) -> tuple[OUParams, KnwSvLegParams, KnwSvLegParams]
```

Jointly calibrate one (v, interest_rate, inflation) knw_sv triple: fetch the rate
and inflation history, build the realized-variance proxy for the hidden variance
factor `v`, fit `v`'s CIR process to it and fit both legs' coupling on `v`, on
themselves and on each other (`knw_sv_model.fit_knw_sv_triple`).

In plain terms: this learns how turbulent the rate/inflation pair has been over
time and how that turbulence behaves. `v_params` describe the turbulence itself:
its normal level (`long_run_mean`), how fast a spike fades (`mean_reversion_speed`;
a speed of 1.4 a year means half of a spike is gone after ln 2 / 1.4 = 0.5 years)
and how jumpy it is (`volatility`). Each leg's `variance_sensitivity` says how much
its own surprises grow when `v` is high, and `variance_coupling` how much a high `v`
shifts its expected next value; the rest reads as in `Knw.calibrate_pair`.

The fit runs in stages: a constant-volatility pass identical to `Knw`'s, purely for
its residuals; a four-period trailing average of the summed squared residuals as
the proxy for `v`, lagged one period so a residual is never explained by itself; a
CIR fit to that proxy (`interest_rates_model.fit_cir_process`, unmodified, with the
lowest-level floor set to the proxy's 1st percentile rather than the 10 basis-point
floor tuned for rates); a second OLS pass with `v(t-1)` as a fourth regressor; and
a regression of each leg's squared residuals on `v(t-1)` for `base_variance` and
`variance_sensitivity`, clamped at zero. `v`'s parameters are stored under
`variance_factor_name(interest_rate_name)`, since `v` has no config entry of its own.
Each leg's `base_variance` and `variance_sensitivity` are per-period variances.

Also known as: KNW with stochastic volatility, CP2022-style (v, r, pi) fit.

**Args:**

- <u>interest_rate_name (str):</u> this pair's interest-rate leg's name, used to key params()/changes()/series()/dates() and as the factor name in the simulation.
- <u>inflation_name (str):</u> this pair's inflation leg's name, same role.
- <u>period (str):</u> shared sampling frequency ("monthly", "quarterly", or "yearly").
- <u>interest_rate_source (str):</u> "ticker" or "oecd" (the default).
- <u>interest_rate_ticker (str):</u> used when interest_rate_source="ticker".
- <u>interest_rate_country (str):</u> used when interest_rate_source="oecd".
- <u>interest_rate_term (str):</u> used when interest_rate_source="oecd"; "short" or "long".
- <u>inflation_country (str):</u> the country to pull OECD CPI growth for.

**Returns:**

<u>tuple[OUParams, KnwSvLegParams, KnwSvLegParams]:</u> (v_params, interest_rate_params, inflation_params).

**Raises:**

- <u>ValueError:</u> propagated from knw_sv_model.fit_knw_sv_triple: too few overlapping observations (at least 11 after joining on date), too few proxy points left after the rolling window, or a non-stationary [r, pi] coupling submatrix.

**Notes:**

- Both legs share one `period`, as in `Knw.calibrate_pair`, enforced at config
  validation (`config_model.ScenariosConfig`), not re-checked here; the simulation
  must also run at that `period`.
- The proxy for `v` comes from a first constant-volatility fit, not from market
  yields as in DNB's CP2022: a different estimate, not a simplified version of it.
- If neither leg shows any positive link between `v` and its variance, both
  `variance_sensitivity` values are 0 and a warning suggests `method="knw"`.
- Known limitation, only at very long histories: the rolling windows overlap
  (neighboring proxy values share three of their four squared residuals), which
  biases the CIR fit's speed, mean and volatility downward. On a synthetic triple
  with true `(kappa, theta, omega) = (0.8, 0.02, 0.12)` the fit drifts toward about
  `(0.65, 0.013, 0.10)` past ~2,000 quarterly observations (500 years), and the
  bias does not shrink with more data. At the 100-400 quarterly observations real
  OECD/FRED panels offer it is essentially unbiased (`kappa` of 0.78-0.83 against
  0.8 at n=100, 30-seed average, no failed fits). More Monte Carlo paths or a
  longer horizon do not change this, as `v`'s parameters are fixed at calibration.
- Two fixes were tried and rejected: a non-overlapping block-averaged proxy, and a
  skip-lag regression pairing `v_proxy[t]` with `v_proxy[t+window]`. Both removed
  the downward bias but replaced it with a larger upward one (`kappa` 1.3-2.5x too
  high) and 10-50% failed fits at realistic sample sizes. The root cause is that the
  proxy is a window average, not a point sample of the variance; a real fix needs
  a method-of-moments estimator built on the autocovariance of a window-averaged
  CIR process, disproportionate against a bias negligible at every scale used here.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.models.knw_sv.knw_sv_controller import KnwSv

toolkit = Toolkit(["^IRX"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1990-01-01")
knw_sv = KnwSv(toolkit)

v, interest_rate, inflation = knw_sv.calibrate_triple("interest_rate", "inflation", period="quarterly")
```

Which returns (calibrated on 2026-10-05):

| v | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:--|---------------------:|--------------:|-----------:|--------------:|
| `__knw_sv_variance_interest_rate` | 0.3988 | 0.0000627 | 0.0078 | 0.0000094 |

| leg | intercept | variance_coupling | own_persistence | cross_coupling | base_variance | variance_sensitivity |
|:----|----------:|------------------:|----------------:|---------------:|--------------:|---------------------:|
| interest_rate | -0.0007 | -5.5025 | 0.9420 | 0.0960 | 0.0000152 | 0.0322 |
| inflation | 0.0040 | -0.2861 | 0.8837 | -0.0338 | 0.0000099 | 0.5858 |

Both legs start from their last observation (`initial_value` 0.0375 and 0.0386), as
in `Knw`. Turbulence `v` fades by half in about ln 2 / 0.399 = 1.7 years and today
(0.0000094) sits well below its normal level (0.0000627), so the pair is calmer than
usual. Inflation's variance responds most to `v`: its standard deviation is 0.31% a
quarter at `v = 0` and 0.68% at `v`'s long-run level. The fit also warned that the
Feller condition fails (2 * 0.399 * 0.0000627 < 0.0078^2), so simulated `v` touches
zero more often than the stationary distribution suggests.

**References:**

- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). "A Theory of the Term Structure of Interest Rates." Econometrica, 53(2), 385-407. <https://doi.org/10.2307/1911242>
- Heston, S.L. (1993). "A Closed-Form Solution for Options with Stochastic Volatility with Applications to Bond and Currency Options." The Review of Financial Studies, 6(2), 327-343. <https://doi.org/10.1093/rfs/6.2.327>
- Commissie Parameters (2022). "Technical Appendix: Specification of the CP2022 Model." Eq. 2-3 and 52. <https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix>

## calibrate_equity_leg

```python
calibrate_equity_leg(
    equity_name: str,
    interest_rate_name: str,
    inflation_name: str,
    equity_prices: pl.Series,
    equity_dates: pl.Series,
    period: str,
) -> KnwSvEquityParams
```

Calibrate one equity leg that shares an already calibrated knw_sv pair's variance
factor `v`, following DNB's eq. 4/5 equity row (`knw_sv_model.fit_knw_sv_equity_leg`).

In plain terms: this fits an equity index that earns the simulated short rate plus
a constant risk premium, and whose swings grow when the pair's turbulence factor
`v` is high. `risk_premium` is the extra log return per period over the short
rate (0.02 at a quarterly period is roughly 8% a year), `base_variance` the
per-period variance when `v` is zero, and `variance_sensitivity` how much variance
each unit of `v` adds.

Two stages, the same shape as the second stage of `calibrate_triple`: first
`risk_premium` from the mean excess log return (log return minus `r(t-1)` times
the period length), corrected for the half-variance (Jensen) term; then a
regression of the squared residuals on `v(t-1)` for `base_variance` and
`variance_sensitivity`, clamped at zero. Only historical prices, rates and the
`v` proxy are used, no options data. The pair's `v` proxy is rebuilt from its
already fetched `series()`/`dates()` rather than cached, the same reuse
`KnwSvQ.calibrate_mpr` relies on, so the equity leg sees exactly the `r(t-1)` and
`v(t-1)` the pair was fit against.

Also known as: CP2022 equity row, Heston-style equity leg with a stochastic short rate.

**Args:**

- <u>equity_name (str):</u> this leg's name, used to key params() and as the factor name in the simulation.
- <u>interest_rate_name (str):</u> the already-calibrated knw_sv pair's interest_rate leg name to share v with.
- <u>inflation_name (str):</u> that same pair's inflation leg name; v_proxy is a function of the whole pair, not just the rate leg.
- <u>equity_prices (pl.Series):</u> historical equity index level observations (not log, not returns).
- <u>equity_dates (pl.Series):</u> dates paired with `equity_prices`, same length.
- <u>period (str):</u> the pair's own shared sampling frequency ("monthly", "quarterly", or "yearly"); must match what `calibrate_triple` was called with for this pair.

**Returns:**

<u>KnwSvEquityParams:</u> the calibrated equity leg.

**Raises:**

- <u>ValueError:</u> if `period` isn't one of "monthly"/"quarterly"/"yearly", or propagated from knw_sv_model.fit_knw_sv_equity_leg.
- <u>RuntimeError:</u> propagated from series()/dates() if calibrate_triple(...) naming `interest_rate_name`/`inflation_name` hasn't been called yet.

**Notes:**

- This is not DNB's own equity calibration: DNB constrains `eta_S` and the equity
  variance against equity-derivative implied volatility (Technical Appendix
  eq. 25), which this project has no data for; a history-only fit is materially
  simpler and less constrained.
- The equity leg reads `v` and the rate one way; `v` never reads equity back.
- The leg runs under the real-world measure only; a config pairing it with a
  `measure: risk_neutral` rate is rejected.
- If no positive link between `v` and the equity variance is found,
  `variance_sensitivity` is 0 and a warning says the coupling is inactive.
- Only dates the equity series and the pair's proxy share are used (at least 6).

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.equities.equities_controller import fetch_equity_prices
from financescenarios.models.knw_sv.knw_sv_controller import KnwSv

toolkit = Toolkit(["^GSPC"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1990-01-01")
knw_sv = KnwSv(toolkit)
knw_sv.calibrate_triple("interest_rate", "inflation", period="quarterly")

dates, prices = fetch_equity_prices(toolkit, "^GSPC", "quarterly")
knw_sv.calibrate_equity_leg("equity", "interest_rate", "inflation", prices, dates, period="quarterly")
```

Which returns (calibrated on 2026-10-05):

| name | risk_premium | base_variance | variance_sensitivity | initial_value |
|:-----|-------------:|--------------:|---------------------:|--------------:|
| equity | 0.0159 | 0.0042 | 26.0769 | 7773.95 |

Over the S&P 500's quarterly history since 1990 the index earned 1.59% a quarter
(about 6.4% a year) above the short rate. Its volatility is 6.5% a quarter (about
13% a year) at `v = 0` and 7.6% a quarter (about 15.3% a year) at `v`'s long-run
level, so equity turbulence rises with the pair's.

**References:**

- Commissie Parameters (2022). "Technical Appendix: Specification of the CP2022 Model." Eq. 4-5 and 25. <https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix>
- Heston, S.L. (1993). "A Closed-Form Solution for Options with Stochastic Volatility with Applications to Bond and Currency Options." The Review of Financial Studies, 6(2), 327-343. <https://doi.org/10.1093/rfs/6.2.327>

## names

```python
knwsv.names  # property -> list[str]
```

The names of every knw_sv leg calibrated so far (both legs of every pair,
plus each pair's internal variance-factor name), in calibration order.

## params

```python
params(name: str) -> OUParams | KnwSvLegParams
```

The calibrated parameters for one knw_sv leg or variance factor: an
`OUParams` for a variance-factor name (see variance_factor_name), a
`KnwSvLegParams` for an interest_rate/inflation leg name.

**Args:**

- <u>name (str):</u> the leg's name (as passed to calibrate_triple) or a variance factor's derived name (see variance_factor_name).

**Raises:**

- <u>RuntimeError:</u> if calibrate_triple(...) covering this name hasn't been called yet.

## series

```python
series(name: str) -> pl.Series
```

The raw historical series for one knw_sv leg (interest_rate/inflation
only; v has no fetched series of its own).

**Args:**

- <u>name (str):</u> the leg's name, as passed to calibrate_triple().

**Raises:**

- <u>RuntimeError:</u> if calibrate_triple(...) naming this leg hasn't been called yet.

## dates

```python
dates(name: str) -> pl.Series
```

The dates paired with series(name), same length and order.

**Args:**

- <u>name (str):</u> the leg's name, as passed to calibrate_triple().

**Raises:**

- <u>RuntimeError:</u> if calibrate_triple(...) naming this leg hasn't been called yet.

## changes

```python
changes(name: str) -> pl.DataFrame
```

Dated period-over-period changes in one knw_sv leg, reused for cross-factor
correlation estimation (Dependence) instead of triggering a second
Finance Toolkit fetch; see Knw.changes' own docstring, same reasoning.

**Args:**

- <u>name (str):</u> the leg's name, as passed to calibrate_triple().

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` (pl.Date) and `value` (f64).

**Raises:**

- <u>RuntimeError:</u> if calibrate_triple(...) naming this leg hasn't been called yet.
