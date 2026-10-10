---
title: "Commodities"
seo_title: "Commodities Reference – Finance Scenarios"
excerpt: "Commodity futures, one per commodity."
description: "Commodity futures, one per commodity."
author_profile: false
permalink: /projects/financescenarios/docs/reference/commodities
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Commodity futures, one per commodity. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.factors.commodities.commodities_controller import Commodities
```

```python
Commodities(toolkit: Toolkit)
```

The Commodities module simulates commodity prices, such as crude oil, natural gas,
gold or copper, as prices that swing widely but are pulled back toward a normal level
over time, rather than drifting off without limit the way a stock index can.

In plain terms: add one or more commodities to a run and each becomes a simulated
price path, linked to interest rates, equities, FX and the rest through the
correlation matrix, and usable as a portfolio sleeve like any other priced series. It
is opt-in: `commodities` is an empty list by default, and each entry is calibrated
independently and named by its own `name`. It has no cascade dependency on any other
factor; the link is through correlation only, the same shape as `fx` and `credit`.

Why the price is pulled back, when equities and exchange rates are not: every other
price-level factor in this project is a random walk (equities are a regime-switching
lognormal, FX a geometric Brownian motion), since there is no economically meaningful
long-run level for a stock index or a currency over a multi-decade horizon. A
commodity is different. Storage costs and the convenience yield (the benefit of
holding the physical good rather than a claim on it, such as keeping a refinery
running) pull the spot price back toward a level set by the economics of extraction,
production and storage. That is the founding result of
[Schwartz (1997)](https://doi.org/10.1111/j.1540-6261.1997.tb02721.x) and the standard
justification for mean reversion in commodity price models specifically.

The default model (`method="single_factor"`) is Schwartz's single-factor process: the
*logarithm* of the spot price follows an Ornstein-Uhlenbeck (mean-reverting) process,

```text
d(log S) = kappa * (mu - log S) dt + sigma * dW
```

where `kappa` is the speed of mean reversion, `mu` the long-run log-price level and
`sigma` the log-price volatility. Working in logs keeps the simulated price strictly
positive, the same reason FX exponentiates a log-return. `exp(mu)` is the stationary
*median* price the calibration window implies, not the mean (see `calibrate`).

Schwartz (1997) is a family of three models, genuinely distinct from each other. Model
1 is the single-factor process above. Model 2, equivalent to
[Gibson and Schwartz (1990)](https://doi.org/10.1111/j.1540-6261.1990.tb05114.x), adds
a second, mean-reverting convenience-yield factor correlated with the spot price, and
Model 3 adds a stochastic (Vasicek) interest rate as a third factor. Models 2 and 3 are
not implemented. [Schwartz and Smith (2000)](https://doi.org/10.1287/mnsc.46.7.893.12034)
is a separate, later re-parameterization of the same two-factor economics (not a
further extension of Models 2 and 3): a mean-reverting short-term deviation plus a
random-walk long-run equilibrium price, in place of spot price plus convenience yield.
`method="schwartz_smith"` implements that one directly, under both measures.

Options that change the model:

- `method="schwartz_smith"`: the two-factor model, `ln(S_t) = chi_t + xi_t`, where
  `chi` is a short-term deviation that mean-reverts to exactly 0 and `xi` a long-term
  equilibrium log-price that follows a random walk with drift. It separates a
  *transient* shock (a supply disruption, a demand spike) from a *permanent* shift in
  the commodity's own long-run economics. `chi` and `xi` are simulated as two named,
  correlation-linked factors, `f"{name}_chi"` and `f"{name}_xi"` (e.g. `oil_chi` and
  `oil_xi`); `Scenarios.simulate()` then attaches the reconstructed price
  (`exp(chi + xi)`, `commodities_model.reconstruct_schwartz_smith_price`) under the
  entry's own name, so `paths["oil"]` exists too and works as a portfolio sleeve or a
  reporting-currency conversion. The two components keep category
  `commodities_state` (not `commodities`) in `ScenarioSet.factor_categories`: they are
  log-space state variables, not a priced series, so a portfolio sleeve cannot name
  them. See `calibrate_schwartz_smith`.
- `measure="risk_neutral"` (risk-neutral, or Q, measure: the drift that prices today's
  futures without arbitrage, rather than the drift history shows): requires
  `method="schwartz_smith"` and calibrates the drift terms against today's forward
  curve; see `calibrate_schwartz_smith_risk_neutral`. Single-factor Schwartz (1997)
  has no defined risk-neutral leg in this project.
- `volatility_model="garch"` (`method="single_factor"` only): replaces the fixed
  volatility with a GARCH(1,1) process, so calm and turbulent periods each persist
  ([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1)).
- `condition_on_business_cycle` (`method="single_factor"` only): adds a pull from the
  leading indicator's step-to-step change, so prices tend to move with the economy.

Data: the spot price is any commodity or futures ticker the shared `Toolkit` holds,
read from the "Adj Close" column of `Toolkit.get_historical_data()` (the same call
equities use, Yahoo Finance by default, no key needed). Common examples are `CL=F`
(WTI crude oil, the default), `GC=F` (gold), `NG=F` (natural gas) and `HG=F` (copper).
The Schwartz-Smith method additionally reads today's listed futures through
`Toolkit.economics.get_commodity_forward_curve`, which only exists for the tickers in
`_COMMODITY_NAMES`: Crude Oil, Natural Gas, Gold, Silver, Copper, Corn, Wheat and
Soybeans. Commodity futures are quoted in US dollars worldwide, so `currency` is
descriptive metadata for reporting only.

What it does not do: no Kalman-filter estimation of Schwartz-Smith (there is no
historical futures panel to filter against, only today's curve; see
`calibrate_schwartz_smith`), no convenience-yield or stochastic-rate models (Schwartz
Models 2 and 3), and no risk-neutral single-factor model.

Configuration (`commodities[i]` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `name` | `commodity` | The factor's name in the output; unique across every multi-instance list. |
| `ticker` | `CL=F` | Any commodity or futures ticker the `Toolkit` holds. |
| `currency` | `USD` | Descriptive metadata only, consumed by `financescenarios.reporting`. |
| `period` | `daily` | `daily`, `weekly`, `monthly`, `quarterly` or `yearly`: the fit's time step. |
| `method` | `single_factor` | `single_factor` (Schwartz 1997) or `schwartz_smith` (Schwartz-Smith 2000). |
| `measure` | `real_world` | `real_world` or `risk_neutral`; `risk_neutral` requires `schwartz_smith`. |
| `contracts` | `12` | `schwartz_smith` only: monthly forward contracts to try to fetch. |
| `long_term_window_years` | `3.0` | `schwartz_smith` only: trailing window (years) that proxies `xi`. |
| `volatility_model` | `constant` | `single_factor` only: `constant` or `garch`. |
| `condition_on_business_cycle` | `false` | `single_factor` only; requires `leading_indicator.enabled: true`. |
| `beliefs.mean_reversion_speed` | `null` | `single_factor` only: override the fitted speed; must be > 0. |
| `beliefs.long_run_mean` | `null` | `single_factor` only: override the long-run level, in log-price units. |
| `beliefs.volatility` | `null` | `single_factor` only: override the fitted volatility; must be > 0. |

For `method="schwartz_smith"` the names `f"{name}_chi"` and `f"{name}_xi"` must also be
free of collisions with every other factor. `contracts` and `long_term_window_years`
are ignored for `single_factor`; `volatility_model` and `condition_on_business_cycle`
are rejected together with `schwartz_smith`.

Beliefs: a field left `null` keeps the calibrated value; the substitution happens per
entry in `config_model.apply_commodity_beliefs`, and only when `volatility_model` is
`constant` (a GARCH fit has no field to override). In a regime YAML, address one
entry's beliefs with a dotted `"commodities.<name>"` key. `beliefs.long_run_mean` is
a *log* price: check the calibrated `long_run_mean`
(`Scenarios.calibrate(config).calibrated_params`) first, then convert a target price
with `log(price)`. That sets the stationary *median* price; the mean is
`exp(long_run_mean + volatility^2 / (4 * mean_reversion_speed))`, strictly higher
because a lognormal price is skewed to the right, so for a target mean price use
`log(price) - volatility^2 / (4 * mean_reversion_speed)`. Beliefs are rejected
entirely for `method="schwartz_smith"` entries: their shape does not fit a two-factor
chi/xi model.

**References:**

- Schwartz, E.S. (1997). "The Stochastic Behavior of Commodity Prices: Implications for Valuation and Hedging." Journal of Finance, 52(3), 923-973. <https://doi.org/10.1111/j.1540-6261.1997.tb02721.x>
- Gibson, R., Schwartz, E.S. (1990). "Stochastic Convenience Yield and the Pricing of Oil Contingent Claims." Journal of Finance, 45(3), 959-976. <https://doi.org/10.1111/j.1540-6261.1990.tb05114.x>
- Schwartz, E., Smith, J.E. (2000). "Short-Term Variations and Long-Term Dynamics in Commodity Prices." Management Science, 46(7), 893-911. <https://doi.org/10.1287/mnsc.46.7.893.12034>
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." Journal of Econometrics, 31(3), 307-327. <https://doi.org/10.1016/0304-4076(86>)90063-1

## calibrate

```python
calibrate(
    name: str,
    ticker: str = 'CL=F',
    period: str = 'daily',
    volatility_model: str = 'constant',
    business_cycle_covariate: pl.Series | None = None,
    business_cycle_covariate_dates: pl.Series | None = None,
) -> CommodityParams | GARCHParams | OUCovariateParams
```

Calibrate one commodity's single-factor Schwartz (1997) process from its price
history: fetch the ticker's spot price and fit how fast the log price returns to
its normal level (`mean_reversion_speed`), what that level is (`long_run_mean`) and
how much it swings (`volatility`).

In plain terms: this learns from the past how a commodity price behaves, so the
simulated futures spike and slump the way the real price has and then settle back.
The half-life of a shock is ln 2 / `mean_reversion_speed` years: a speed of 1.37 a
year means half of a price spike has faded after about six months.

The fit is on the logarithm of the price, so `long_run_mean` is a log price:
`exp(long_run_mean)` is the price the process is pulled toward (its stationary
median), and `initial_value` is today's actual price, not its log, matching every
other price-level factor (equities, FX) whose `ScenarioSet.paths` hold real levels.
The stationary mean price is `exp(mu + sigma^2 / (4 * kappa))`, a little above the
median because a lognormal price is skewed to the right.

How the fit works: the exact discrete-time version of the process is a linear
regression of each period's change in log price on the previous log price, solved by
ordinary least squares (`commodities_model.fit_commodity_process`, the same exact
transition `calibration_model.fit_ou_process` uses on a level, with slope
`e^(-kappa * dt) - 1` rather than Euler's first-order `-kappa * dt`). The slope and
intercept convert back into the speed and the long-run level, and the residual
standard deviation gives the volatility. Simulation then uses the same exact
transition (`commodities_model.step_commodity_process`),

```text
next = exp(mu + (log(current) - mu) * e^(-kappa*dt)
           + sigma * sqrt((1 - e^(-2*kappa*dt)) / (2*kappa)) * shock)
```

which has zero discretization error and is stable for any `kappa * dt`.

Also known as: Schwartz one-factor model, mean-reverting log-price (exponential
Ornstein-Uhlenbeck) commodity model.

**Args:**

- <u>name (str):</u> this commodity's name, used to key params()/changes() and as the factor name in the simulation (e.g. "crude_oil", "gold").
- <u>ticker (str):</u> the ticker to calibrate against, any ticker the shared Toolkit instance includes, e.g. "CL=F" (WTI crude), "GC=F" (gold), "NG=F" (natural gas), "HG=F" (copper).
- <u>period (str):</u> sampling frequency of the underlying data ("daily", "weekly", "monthly", "quarterly", "yearly"), determines the time step used to fit.
- <u>volatility_model (str):</u> "constant" (the default, Schwartz's own log-price OU fit via fit_commodity_process) or "garch" (GARCH(1,1) time-varying volatility, Bollerslev 1986). The GARCH path fits the raw (not log) price level via the generic fit_garch_process, the same "constant-vol path is log-space, GARCH/ covariate paths are raw-level" limitation the credit module has (fit_garch_process has no log-space variant yet).
- <u>business_cycle_covariate (pl.Series &#124; None):</u> a business-cycle indicator's raw historical level series (e.g. LeadingIndicator.series). When supplied, adds an additive drift term on the covariate's step-to-step change (business-cycle conditioning); incompatible with volatility_model="garch". Also fits the raw price level (fit_ou_process_with_covariate), not the log price.
- <u>business_cycle_covariate_dates (pl.Series &#124; None):</u> the dates paired with `business_cycle_covariate` (e.g. LeadingIndicator.dates), same length and order. Required whenever `business_cycle_covariate` is supplied: the price series and the leading indicator are fetched independently and forced onto the same *period* but not guaranteed the same *start date*, so this commodity's own dates and the covariate's are inner-joined on date before fitting.

**Returns:**

<u>CommodityParams &#124; GARCHParams &#124; OUCovariateParams:</u> the calibrated process parameters: GARCHParams when volatility_model="garch", OUCovariateParams when business_cycle_covariate is supplied.

**Raises:**

- <u>ValueError:</u> if period or volatility_model is not recognized, business_cycle_covariate is combined with volatility_model="garch", business_cycle_covariate is supplied without business_cycle_covariate_dates (or vice versa), or the underlying price series fails its fitter's own validation (fewer than 4 observations, a price that is not strictly positive, or a fitted mean-reversion speed that is not positive, meaning the series is trending or explosive at this frequency rather than mean-reverting).

**Notes:**

- A trending price fails the fit rather than returning a meaningless speed: gold
  (`GC=F`) sampled monthly from 2016 raised the "no mean reversion" error when the
  example below was run, while crude oil and natural gas calibrated fine.
- WTI crude settled at -37.63 USD on 2020-04-20, so a *daily* `CL=F` history that
  includes that day fails the "strictly positive" check; a monthly average or a
  later start date avoids it.
- The GARCH and business-cycle paths fit the raw price level, not the log price, so
  they lose the positivity guarantee, and belief overrides do not apply to a GARCH
  fit. With `condition_on_business_cycle`, the calibration runs on
  `leading_indicator.period`.
- `changes(name)` holds the dated log-price changes, reused for the correlation
  matrix without a second fetch.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.commodities.commodities_controller import Commodities

toolkit = Toolkit(["CL=F", "NG=F"], start_date="2016-01-01")
commodities = Commodities(toolkit)

commodities.calibrate("crude_oil", ticker="CL=F", period="monthly")
commodities.calibrate("natural_gas", ticker="NG=F", period="monthly")
```

Which returns (calibrated on 2026-10-04):

| name | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-----|---------------------:|--------------:|-----------:|--------------:|
| crude_oil | 1.3659 | 4.2056 | 0.4692 | 91.1100 |
| natural_gas | 1.6133 | 1.1284 | 0.5993 | 3.0350 |

Crude oil starts at 91.11 USD a barrel and is pulled toward exp(4.2056) = 67.06 USD,
with a shock halving in about six months (ln 2 / 1.3659 = 0.51 years); natural gas
starts at 3.04 USD and is pulled toward exp(1.1284) = 3.09 USD, a little faster
and with larger swings.

**References:**

- Schwartz, E.S. (1997). "The Stochastic Behavior of Commodity Prices: Implications for Valuation and Hedging." Journal of Finance, 52(3), 923-973. <https://doi.org/10.1111/j.1540-6261.1997.tb02721.x>
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." Journal of Econometrics, 31(3), 307-327. <https://doi.org/10.1016/0304-4076(86>)90063-1

## calibrate_schwartz_smith

```python
calibrate_schwartz_smith(
    name: str,
    ticker: str = 'CL=F',
    period: str = 'daily',
    contracts: int = 12,
    long_term_window_years: float = 3.0,
) -> SchwartzSmithParams
```

Calibrate one commodity's real-world Schwartz & Smith (2000) two-factor process:
split the log price into a short-term deviation `chi` that fades back to zero and a
long-term equilibrium log price `xi` that wanders as a random walk with drift, and
fit both.

In plain terms: this separates the part of today's price that is a temporary
dislocation (a refinery outage, a cold snap) from the part that reflects a lasting
change in what the commodity costs to produce. The temporary part halves in
ln 2 / `chi.mean_reversion_speed` years; the long-term part never reverts, it only
drifts at `xi.drift` a year. Today's price is `exp(chi.initial_value +
xi.initial_value)`.

The two parts are stored as two derived factors, `f"{name}_chi"` and
`f"{name}_xi"`, so the existing `names`/`params`/`changes` accessors keep working
unmodified. `chi` is an `OUParams` with `long_run_mean` fixed at exactly 0 (it is a
deviation *from* `xi`, so it has no level of its own) and `xi` a `RandomWalkParams`;
both reuse the engine's existing step functions.

How the fit is assembled, from two independent sources:

- `kappa` (chi's mean-reversion speed) and today's chi/xi split come from
  `commodities_model.fit_schwartz_smith_process`, a documented simplification of
  the paper's Kalman-filter maximum-likelihood estimate. The paper filters a
  historical *panel* of futures prices across maturities; Finance Toolkit offers
  only today's forward curve, so here `xi` is proxied as a
  `long_term_window_years` trailing moving average of the log price and `chi` is
  the residual. Only `kappa` and the split are reliable from this: a rolling mean
  understates `xi`'s true volatility by roughly an order of magnitude (verified on
  synthetic data), so its own volatility and correlation are a last resort.
- `sigma_chi`, `sigma_xi` and their correlation `rho` instead come from
  `commodities_model.fit_schwartz_smith_diffusion_from_forward_curve`, fitted to the
  ticker's real listed forward curve (`Economics.get_commodity_forward_curve`):
  each listed contract's recent realized volatility is regressed on the model's
  closed-form futures-volatility formula, with `kappa` held at the spot fit. That
  is a better-identified source than the spot series.

The forward-curve fit is skipped, with a logged warning, in favor of the spot-only
estimate when the ticker has no forward-curve mapping (`_COMMODITY_NAMES`), fewer
than 3 contracts have enough trading history (20 closes in their last 120), or the
fit comes back degenerate (`rho` pinned at its +-1 clipping boundary, or `sigma_xi`
under 5% of `sigma_chi`; `commodities_model.is_degenerate_diffusion_fit`).

Also known as: short-term/long-term two-factor commodity model, Schwartz-Smith
model.

**Args:**

- <u>name (str):</u> this commodity's name; `f"{name}_chi"`/`f"{name}_xi"` key `params()`/`changes()` and become the two simulated factor names (see `scenarios_controller.py`'s Schwartz-Smith wiring).
- <u>ticker (str):</u> the spot ticker to calibrate against, e.g. "CL=F" (WTI crude), "GC=F" (gold). Must be a key of `_COMMODITY_NAMES` for the forward-curve diffusion fit to run at all; otherwise this falls back to the spot-only diffusion estimate.
- <u>period (str):</u> sampling frequency of the underlying spot data.
- <u>contracts (int):</u> number of sequential monthly forward contracts to attempt to fetch for the diffusion fit (forwarded to `get_commodity_forward_curve`). Not every calendar month has a listed contract, so fewer maturities than this may end up used.
- <u>long_term_window_years (float):</u> the trailing window, in years, whose moving average of the log price proxies `xi`; forwarded to `fit_schwartz_smith_process`.

**Returns:**

<u>SchwartzSmithParams:</u> the calibrated real-world chi/xi processes.

**Raises:**

- <u>ValueError:</u> if period is not recognized, or the underlying price series fails `fit_schwartz_smith_process`'s own validation (too short for the long-term window, a price that is not strictly positive, or no short-term mean reversion in chi).

**Notes:**

- At simulation time, the correlation between `chi` and `xi` comes from the
  correlation matrix estimated over `changes(f"{name}_chi")` and
  `changes(f"{name}_xi")`, not from the forward-curve `rho`, so the simulated
  futures-volatility term structure need not match the forward-curve fit exactly.
- `xi.drift` always comes from the spot decomposition: under the real-world measure
  the forward curve offers no substitute for it.
- The forward-curve fetch can include an expired front-month contract that Yahoo
  no longer quotes (the run below logged a 404 for `CLV26.NYM`); it is skipped.
- Not combinable with `volatility_model="garch"`, `condition_on_business_cycle` or
  belief overrides.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.commodities.commodities_controller import Commodities

toolkit = Toolkit(["CL=F"], start_date="2021-01-01")
commodities = Commodities(toolkit)

commodities.calibrate_schwartz_smith("oil", ticker="CL=F", period="daily")
```

Which returns (calibrated on 2026-10-04):

| factor | mean_reversion_speed | long_run_mean | drift | volatility | initial_value |
|:-------|---------------------:|--------------:|------:|-----------:|--------------:|
| oil_chi | 2.7274 | 0.0000 | | 0.4177 | 0.2145 |
| oil_xi | | | -0.0251 | 0.0058 | 4.2975 |

Today's 91.11 USD crude price splits into a long-term level of exp(4.2975) = 73.5
USD and a short-term premium of exp(0.2145) = 1.24 (24% above it), which halves in
about three months (ln 2 / 2.7274 = 0.25 years). On this run the forward-curve fit
came back degenerate (`rho` = 1), so the logged fallback applied and the very small
`xi` volatility is the spot-only estimate this method warns understates it.

**References:**

- Schwartz, E., Smith, J.E. (2000). "Short-Term Variations and Long-Term Dynamics in Commodity Prices." Management Science, 46(7), 893-911. <https://doi.org/10.1287/mnsc.46.7.893.12034>

## calibrate_schwartz_smith_risk_neutral

```python
calibrate_schwartz_smith_risk_neutral(
    name: str,
    ticker: str = 'CL=F',
    period: str = 'daily',
    contracts: int = 12,
    long_term_window_years: float = 3.0,
) -> SchwartzSmithParams
```

Calibrate one commodity's risk-neutral (Q-measure) Schwartz & Smith (2000)
two-factor process against today's observed forward curve
(`Economics.get_commodity_forward_curve`): the drift terms are chosen so that the
model reproduces the futures prices the market quotes today.

In plain terms: instead of asking how the price has behaved, this asks what path
the futures market is pricing in. If the curve slopes down (backwardation, futures
below spot), the risk-neutral drift of `xi` comes out negative; if it slopes up
(contango), positive. Use it for pricing and hedging, where the simulated
prices must agree with tradeable futures, not for a forecast.

The diffusion parameters (`kappa`, `sigma_chi`, `sigma_xi`, `rho`) do not change
under a change of measure, so they are estimated exactly as in
`calibrate_schwartz_smith`. Only the two drift terms are fitted here, against the
paper's futures-pricing formula (eq. 9, see
`commodities_model.fit_schwartz_smith_risk_neutral`), which is linear in them: the
short-term risk premium `lambda_chi`, which moves `chi`'s long-run level under Q to
`-lambda_chi / kappa`, and `xi`'s risk-adjusted growth rate `mu*_xi`. With about
12 listed contracts for 2 unknowns, ordinary least squares is comfortably
over-identified.

Unlike `calibrate_schwartz_smith`, a forward curve is not optional here: there is no
market-implied drift to calibrate without one, so this raises rather than falling
back to a spot-only estimate.

Also known as: Schwartz-Smith Q-measure calibration, futures-curve calibration.

**Args:**

- <u>name (str):</u> this commodity's name; see `calibrate_schwartz_smith`.
- <u>ticker (str):</u> the spot ticker to calibrate against. Must be a key of `_COMMODITY_NAMES`; required, no fallback (see above).
- <u>period (str):</u> sampling frequency of the underlying spot data, used for the real-world diffusion fit's spot leg.
- <u>contracts (int):</u> forwarded to `get_commodity_forward_curve`.
- <u>long_term_window_years (float):</u> forwarded to `fit_schwartz_smith_process`.

**Returns:**

<u>SchwartzSmithParams:</u> the calibrated risk-neutral chi/xi processes: `chi` with `long_run_mean = -lambda_chi / kappa`, `xi` with `drift = mu*_xi`, the same speed and volatilities as the real-world fit.

**Raises:**

- <u>ValueError:</u> if period is not recognized, `ticker` has no known commodity mapping, the spot price series fails `fit_schwartz_smith_process`'s own validation, or the forward curve doesn't have at least 2 usable maturities (with today's price) to fit the risk-neutral drift terms.

**Notes:**

- The diffusion estimate goes through the same forward-curve fit and fallback as
  `calibrate_schwartz_smith`, so a degenerate forward-curve volatility fit still
  falls back (with a warning) to the spot-only volatilities; only the drift fit
  strictly needs the curve.
- Configured through `commodities[i].measure: risk_neutral` with
  `method: schwartz_smith`; belief overrides are rejected for it.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.commodities.commodities_controller import Commodities

toolkit = Toolkit(["CL=F"], start_date="2021-01-01")
commodities = Commodities(toolkit)

commodities.calibrate_schwartz_smith_risk_neutral("oil_q", ticker="CL=F", period="daily")
```

Which returns (calibrated on 2026-10-04):

| factor | mean_reversion_speed | long_run_mean | drift | volatility | initial_value |
|:-------|---------------------:|--------------:|------:|-----------:|--------------:|
| oil_q_chi | 2.7274 | 0.1965 | | 0.4177 | 0.2145 |
| oil_q_xi | | | -0.1775 | 0.0058 | 4.2975 |

Speed, volatilities and today's state match the real-world fit; only the drifts
moved. The crude curve that day was steeply backwardated (91.11 USD for November
2026 down to 77.90 USD for September 2027), so the market prices the long-term
level falling about 17.7% a year (against 2.5% in the real-world fit), while the
short-term premium settles at 0.1965 rather than 0 under this measure.

**References:**

- Schwartz, E., Smith, J.E. (2000). "Short-Term Variations and Long-Term Dynamics in Commodity Prices." Management Science, 46(7), 893-911. <https://doi.org/10.1287/mnsc.46.7.893.12034>

## names

```python
commodities.names  # property -> list[str]
```

The names of every commodity calibrated so far, in calibration order.

## params

```python
params(name: str) -> CommodityParams | OUParams | RandomWalkParams | GARCHParams | OUCovariateParams
```

The calibrated process parameters for one commodity.

**Args:**

- <u>name (str):</u> the commodity's name, as passed to calibrate().

**Raises:**

- <u>RuntimeError:</u> if calibrate(name, ...) hasn't been called yet.

## step_function

```python
commodities.step_function  # property
```

The Schwartz (1997) log-price step function (stateless, shared across every commodity).

## changes

```python
changes(name: str) -> pl.DataFrame
```

Dated period log-price changes for one commodity, from the same data
calibrate() already fetched, reused for cross-factor correlation
estimation (Dependence) instead of triggering a second Finance Toolkit fetch.

**Args:**

- <u>name (str):</u> the commodity's name, as passed to calibrate().

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` (pl.Date) and `value` (f64); see helpers.dated_changes().

**Raises:**

- <u>RuntimeError:</u> if calibrate(name, ...) hasn't been called yet.
