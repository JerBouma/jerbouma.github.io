---
title: "Knw"
seo_title: "Knw Reference – Finance Scenarios"
excerpt: "The KNW model: interest rate and inflation fitted jointly."
description: "The KNW model: interest rate and inflation fitted jointly."
author_profile: false
permalink: /projects/financescenarios/docs/reference/knw
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

The KNW model: interest rate and inflation fitted jointly. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.models.knw.knw_controller import Knw
```

```python
Knw(toolkit: Toolkit)
```

The Knw module simulates the interest rate and inflation as one coupled pair, in which
each one's next value depends on the current level of both. It is the constant-volatility
core of the scenario model De Nederlandsche Bank (DNB), the Dutch central bank, uses for
the scenario sets Dutch pension funds and insurers are regulated against.

In plain terms: elsewhere in this project the interest rate and inflation are either
simulated side by side and linked only through correlated shocks (the Ahlgrim and
Hibbert frameworks), or one drives the other in a single direction (Wilkie's cascade,
or `condition_on_interest_rate`). With `method="knw"` they talk to each other both
ways: high inflation today feeds into next period's interest rate, and today's
interest rate feeds into next period's inflation, at the same time. Use it when you
want DNB-style two-way coupling between rates and inflation without the extra
machinery of stochastic volatility. It is a generic method, selectable on any
`interest_rates[]`/`inflation[]` entry pair, not tied to a framework preset, and one
instance holds any number of independently calibrated pairs, one `calibrate_pair()`
call each.

The model comes from DNB's CP2022 model, an extension of the three-factor affine
term-structure model of [Koijen, Nijman & Werker (2010)](https://doi.org/10.1093/rfs/hhp058)
("affine" meaning yields are linear in a few state variables) with
[Heston (1993)](https://doi.org/10.1093/rfs/6.2.327) stochastic volatility on a latent
(never observed) variance factor `v`. The [CP2022 Technical Appendix (2022)](
https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix)
specifies the model in full, including a discrete-time state recursion (its eq. 52) that
couples the nominal short rate and expected inflation through a full 2x2 matrix, not a
diagonal one. `method="knw"` implements the constant-volatility simplification of that
recursion: `v` is dropped as a simulated factor and its constant contribution is folded
into the two fitted intercepts, which leaves a bivariate Gaussian VAR(1), a vector
autoregression of order one in which each variable is regressed on the previous value
of both ([Lutkepohl, 2005](https://doi.org/10.1007/978-3-540-27752-1)):

```text
r(t)  = c_r  + phi_rr*r(t-1)   + phi_r_pi*pi(t-1) + sigma_r*z_r(t)
pi(t) = c_pi + phi_pi_r*r(t-1) + phi_pipi*pi(t-1) + sigma_pi*z_pi(t)
```

This is not a from-scratch reinvention of DNB's model: it is the smallest genuinely new
piece of it the simulation engine can express without a stateful stochastic-volatility
stepper, a Riccati-equation solver or a market-price-of-risk fit. `KnwSv` adds the
stochastic volatility back and `KnwSvQ` adds a risk-neutral version on top of that.

How it differs from `condition_on_interest_rate` (available on any `method="ou"`
inflation entry, a one-way analogue of the rate/inflation coupling joint macro-finance
affine models study, [Dai & Singleton, 2000](https://doi.org/10.1111/0022-1082.00278)):

| | `condition_on_interest_rate` | `method="knw"` |
|:--|:--|:--|
| Direction | One way (inflation reads the rate) | Two ways (each reads the other) |
| What is read | The rate's step-to-step change | The other factor's level |
| Fit | Single-equation OLS, `fit_ou_process_with_covariate` | Two-equation joint OLS, `fit_knw_pair` |
| Stays as | `method="ou"` on the inflation entry | `method="knw"` on both entries |

The arrow between the two legs points both ways and carries no ordering constraint:
each leg's step reads only the other's start-of-step (lag-1) value, which is already
final before the step begins, so it does not matter which leg the engine steps first.
Every other cross-factor read in this project (`_make_covariate_step`,
`_make_moving_target_step` in `scenarios_controller`) reads the already-advanced value
of the same step and therefore needs a one-way order; see `_make_knw_step` there.

The data come from the Finance Toolkit without any API key: the rate leg through
`interest_rates_controller.fetch_short_rate` (a Yahoo Finance Treasury-yield ticker, or
the OECD short- or long-term rate of any covered country via `economics`), and the
inflation leg from OECD consumer price index growth
(`economics.get_consumer_price_index(oecd_source=True, growth=True)`), year over year. The
OECD series have no daily or weekly frequency, so a pair runs monthly, quarterly or
yearly, and the joint fit only uses the dates both series cover.

What it does not do, deliberately:
- No stochastic volatility: DNB's latent variance factor `v` (a CIR/Heston-type process
  that scales the volatility of the rate, inflation and the equity and CPI index
  processes, simulated with [Andersen's (2008)](https://doi.org/10.21314/jcf.2008.189)
  QE scheme) is folded into the intercepts here; `KnwSv` adds it back.
- No risk-neutral (Q-measure) variant: DNB derives one with an essentially-affine
  market price of risk (`M = K + Sigma*lambda1`); `KnwSvQ` builds a different,
  yield-curve-calibrated one on top of `KnwSv`, not on top of this class.
- No closed-form yield curve: DNB's affine framework gives `y(tau) = phi(tau) + Psi(tau)'X`
  for any maturity through Riccati equations; this project's `yield_curve` and
  `credit_term_structure` factors use an unrelated Nelson-Siegel fit instead.
- Equities and other factors are untouched: a knw pair works alongside the default
  regime-switching equity and OU dividend yield, and DNB's own equity and CPI index
  treatment is not replicated.

Configuration (both entries of a pair in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `interest_rates[i].method` | `hull_white` | Set to `knw` to make this entry the pair's rate leg. |
| `interest_rates[i].inflation_name` | `inflation` | The `name` of the paired `inflation[j]` entry. |
| `interest_rates[i].source` | `ticker` | Where the rate comes from: `ticker` or `oecd`. |
| `interest_rates[i].ticker` | `^IRX` | Treasury-yield ticker, used when `source: ticker`. |
| `interest_rates[i].country` | `United States` | OECD country, used when `source: oecd`. |
| `interest_rates[i].term` | `short` | OECD `short` or `long` rate, used when `source: oecd`. |
| `interest_rates[i].period` | `daily` | Shared by both legs and equal to `engine.frequency` (see below). |
| `inflation[j].method` | `ou` | Set to `knw` to make this entry the pair's inflation leg. |
| `inflation[j].interest_rate_name` | `interest_rate` | The `name` of the paired `interest_rates[i]` entry. |
| `inflation[j].country` | `United States` | The country whose OECD consumer price index is used. |
| `inflation[j].period` | `monthly` | Must equal the rate leg's `period`. |

Both entries set `method: knw` and name each other back; `config_model.ScenariosConfig`
checks that the pairing is mutual and complete and that both share one `period`, since
the joint fit needs both series on the same dates. That `period` must also equal
`engine.frequency`, and the config is rejected otherwise: the fitted coefficients are a
discrete recursion tied to the exact period they were fit at (`step_knw_process` has no
time step to rescale with), so simulating at another frequency silently compounds the
recursion too fast or too slow, which was confirmed against real DNB CP2022 data
through the `knw_sv` equity leg. Belief overrides are not supported, because a coupled
system's long-run mean depends on both legs' intercepts and the full matrix together
(the same restriction `wilkie_consols` and `hibbert_two_factor` apply), and
`volatility_model: garch`, `condition_on_business_cycle` (either entry) and
`condition_on_interest_rate` (the inflation entry) are rejected.

**References:**

- Koijen, R.S.J., Nijman, T.E., Werker, B.J.M. (2010). "When Can Life Cycle Investors Benefit from Time-Varying Bond Risk Premia?" The Review of Financial Studies, 23(2), 741-780. <https://doi.org/10.1093/rfs/hhp058>
- Commissie Parameters (2022). "Technical Appendix: Specification of the CP2022 Model." Published with De Nederlandsche Bank's scenario sets; eq. 52 is the recursion implemented here at zero stochastic volatility. <https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix>
- Dai, Q., Singleton, K.J. (2000). "Specification Analysis of Affine Term Structure Models." Journal of Finance, 55(5), 1943-1978. <https://doi.org/10.1111/0022-1082.00278>
- Lutkepohl, H. (2005). "New Introduction to Multiple Time Series Analysis." Springer. <https://doi.org/10.1007/978-3-540-27752-1>
- Heston, S.L. (1993). "A Closed-Form Solution for Options with Stochastic Volatility with Applications to Bond and Currency Options." The Review of Financial Studies, 6(2), 327-343. <https://doi.org/10.1093/rfs/6.2.327>
- Andersen, L. (2008). "Simple and Efficient Simulation of the Heston Stochastic Volatility Model." Journal of Computational Finance, 11(3), 1-42. <https://doi.org/10.21314/jcf.2008.189>

## calibrate_pair

```python
calibrate_pair(
    interest_rate_name: str,
    inflation_name: str,
    period: str,
    interest_rate_source: str = 'oecd',
    interest_rate_ticker: str = '^IRX',
    interest_rate_country: str = 'United States',
    interest_rate_term: str = 'short',
    inflation_country: str = 'United States',
) -> tuple[KnwParams, KnwParams]
```

Jointly calibrate one (interest_rate, inflation) knw pair: fetch both historical
series and fit the bivariate VAR(1) coupling between them
(`knw_model.fit_knw_pair`), returning one parameter set per leg.

In plain terms: this learns from history how the interest rate and inflation pull
on each other. For each leg you get how much of its own last value carries over
(`own_persistence`), how much of the other leg's last value spills into it
(`cross_coupling`), a constant (`intercept`) and the size of its random surprise
per period (`volatility`). An `own_persistence` of 0.9 at a quarterly period means
a deviation shrinks to 90% of itself each quarter, so about half of it is left
after ln(0.5) / ln(0.9) = 6.6 quarters, before cross effects.

Both equations share one design matrix `[1, r(t-1), pi(t-1)]` and are fit by two
ordinary-least-squares (OLS) regressions; because both use identical regressors,
per-equation OLS is already the efficient estimator, with no need for
seemingly-unrelated-regressions machinery. The fitted 2x2 matrix
`[[phi_rr, phi_r_pi], [phi_pi_r, phi_pipi]]` must have every eigenvalue strictly
inside the unit circle (spectral radius below 1), the two-variable version of
requiring a positive mean-reversion speed; otherwise the system would not settle
down and the fit raises. `volatility` is each equation's residual standard
deviation at the calibration period, taken at face value (no continuous-time
reinterpretation), like `calibration_model.AR1Params` for Wilkie's inflation.
There is no `long_run_mean` per leg: the pair's long-run levels are
`(I - Phi)^-1 c`, a joint property of both legs. Rates and inflation are decimals
(0.04 is 4%), inflation being the year-over-year growth of the consumer price
index.

Also known as: KNW-lite, constant-volatility KNW, bivariate VAR(1) rate/inflation fit.

**Args:**

- <u>interest_rate_name (str):</u> this pair's interest-rate leg's name, used to key params()/changes()/series()/dates() and as the factor name in the simulation.
- <u>inflation_name (str):</u> this pair's inflation leg's name, same role.
- <u>period (str):</u> shared sampling frequency ("monthly", "quarterly", or "yearly"; Finance Toolkit's OECD series support no daily/weekly frequency, unlike a ticker-sourced interest rate on its own).
- <u>interest_rate_source (str):</u> "ticker" (Yahoo Treasury-yield ticker) or "oecd" (Finance Toolkit's country-parameterized OECD short/long-term rate, the default; worldwide coverage, matching this pair's inflation leg which is always OECD-sourced).
- <u>interest_rate_ticker (str):</u> used when interest_rate_source="ticker".
- <u>interest_rate_country (str):</u> used when interest_rate_source="oecd".
- <u>interest_rate_term (str):</u> used when interest_rate_source="oecd"; "short" or "long".
- <u>inflation_country (str):</u> the country to pull OECD CPI growth for.

**Returns:**

<u>tuple[KnwParams, KnwParams]:</u> (interest_rate_params, inflation_params).

**Raises:**

- <u>ValueError:</u> propagated from knw_model.fit_knw_pair; too few overlapping observations after joining on date, or the fitted coupling matrix isn't stationary at this sampling frequency.

**Notes:**

- Both legs share one `period`: the joint regression needs both series on the same
  dates. That is enforced at config validation (`config_model.ScenariosConfig`),
  not re-checked here; a mismatch would still join on date, against an almost
  empty overlap.
- The two series are fetched independently and can start on different dates, so
  they are inner-joined on date, never paired by position; the fit uses only the
  overlap. Fewer than 5 overlapping observations raise, fewer than 10 log a warning.
- The simulation must run at this same `period` (`engine.frequency`), since the
  fitted recursion has no time step to rescale with.
- `changes()` of both legs feed the cross-factor correlation estimate
  (`Dependence`) without a second fetch.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.models.knw.knw_controller import Knw

toolkit = Toolkit(["^IRX"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1990-01-01")
knw = Knw(toolkit)

knw.calibrate_pair("interest_rate", "inflation", period="quarterly")
```

Which returns (calibrated on 2026-10-05):

| leg | intercept | own_persistence | cross_coupling | volatility | initial_value |
|:----|----------:|----------------:|---------------:|-----------:|--------------:|
| interest_rate | -0.0009 | 0.9397 | 0.0918 | 0.0044 | 0.0375 |
| inflation | 0.0036 | 0.8910 | -0.0246 | 0.0073 | 0.0386 |

Fit on 146 quarters (1990Q1 to 2026Q2) of the US OECD short rate and year-over-year
CPI growth. Both legs are persistent, inflation slightly less so, and the rate picks
up some of inflation: one percentage point more inflation adds 0.092 points to next
quarter's rate, while a higher rate nudges inflation down a little. The matrix's
largest eigenvalue is 0.916, so a joint shock halves in about 8 quarters
(ln 0.5 / ln 0.916), and the pair's long-run levels `(I - Phi)^-1 c` are a 2.60% rate
and 2.74% inflation.

**References:**

- Lutkepohl, H. (2005). "New Introduction to Multiple Time Series Analysis." Springer. <https://doi.org/10.1007/978-3-540-27752-1>
- Commissie Parameters (2022). "Technical Appendix: Specification of the CP2022 Model." Eq. 52. <https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix>
- Koijen, R.S.J., Nijman, T.E., Werker, B.J.M. (2010). "When Can Life Cycle Investors Benefit from Time-Varying Bond Risk Premia?" The Review of Financial Studies, 23(2), 741-780. <https://doi.org/10.1093/rfs/hhp058>

## names

```python
knw.names  # property -> list[str]
```

The names of every knw leg calibrated so far (both legs of every pair), in calibration order.

## params

```python
params(name: str) -> KnwParams
```

The calibrated VAR(1) parameters for one knw leg.

**Args:**

- <u>name (str):</u> the leg's name, as passed to calibrate_pair().

**Raises:**

- <u>RuntimeError:</u> if calibrate_pair(...) naming this leg hasn't been called yet.

## series

```python
series(name: str) -> pl.Series
```

The raw historical series for one knw leg, from the same data calibrate_pair() already fetched.

**Args:**

- <u>name (str):</u> the leg's name, as passed to calibrate_pair().

**Raises:**

- <u>RuntimeError:</u> if calibrate_pair(...) naming this leg hasn't been called yet.

## dates

```python
dates(name: str) -> pl.Series
```

The dates paired with series(name), same length and order.

**Args:**

- <u>name (str):</u> the leg's name, as passed to calibrate_pair().

**Raises:**

- <u>RuntimeError:</u> if calibrate_pair(...) naming this leg hasn't been called yet.

## changes

```python
changes(name: str) -> pl.DataFrame
```

Dated period-over-period changes in one knw leg, from the same data
calibrate_pair() already fetched; reused for cross-factor correlation
estimation (Dependence) instead of triggering a second Finance Toolkit fetch.

**Args:**

- <u>name (str):</u> the leg's name, as passed to calibrate_pair().

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` (pl.Date) and `value` (f64); see helpers.dated_changes().

**Raises:**

- <u>RuntimeError:</u> if calibrate_pair(...) naming this leg hasn't been called yet.

## step_function

```python
Knw.step_function()
```

The step function for any knw leg: a plain function, not tied to any
calibrated entry's instance state (see knw_model.step_knw_process).
