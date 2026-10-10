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

Dividend yields, one per ticker. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.factors.dividend_yield.dividend_yield_controller import DividendYield
```

```python
DividendYield(toolkit: Toolkit)
```

The Dividend Yield module simulates the dividend yield of a stock or fund: the
dividends it paid over the past year divided by its current price. A yield rises
when prices fall or payouts grow, and over long stretches it tends to drift back
toward a typical level, which is the behaviour this module captures.

In plain terms: add one or more tickers, such as SPY or JNJ, and each one's
trailing dividend yield becomes a variable in the simulated scenarios, linked to
interest rates, inflation, equities and the rest through the correlation matrix.
This matters for pension and income planning, where dividend income is a separate
input to cash-flow and funding-ratio projections, not just a slice of total
return (the equity module simulates total return only). It is opt-in:
`dividend_yield` is an empty list by default, and each entry is calibrated
independently and named by its own `name`.

The model comes from Ahlgrim, D'Arcy and Gorvett
([2005](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf)),
the actuarial framework that lists dividend yield next to equity return, real
estate, interest rates and inflation as one of the variables its scenarios produce
(eq. 3.17, "Equity Dividend Yields"). The *logarithm* of the yield follows a
mean-reverting (Ornstein-Uhlenbeck) process:

```text
d(log y) = kappa * (mu - log y) * dt + sigma * dW
```

where `kappa` is how fast the log yield returns to normal (the mean-reversion
speed), `mu` is that normal level in logs (`exp(mu)` is the equilibrium yield the
calibration window implies), `sigma` is the size of its random swings, and `dW` a
random shock. Working in logs keeps the simulated yield strictly positive. The
mechanics are the same as the [Schwartz (1997)](https://doi.org/10.1111/j.1540-6261.1997.tb02721.x)
commodity model in `Commodities` (a mean-reverting process on a log level); the
two keep separate model files because they rest on different literature, the
same reason interest rates and commodities do. One caveat comes from the source
paper itself: Ahlgrim, D'Arcy and Gorvett found the mean-reversion speed of
dividend yield "not significantly different from zero" on their 1871-2003 data,
close to a random walk. A calibration window that shows no mean reversion
therefore raises a `ValueError`, a possibility the literature anticipates rather
than a rare edge case.

Three options change the model, each mutually exclusive with the others:

- `condition_on_inflation` adds Wilkie's (1986) inflation term (`YW * dlnQ(t)`):
  the yield also moves with the change in a named inflation entry, the dividend
  yield leg of the Wilkie framework (see "The Wilkie cascade" below).
- `volatility_model="garch"` lets the size of the swings vary over time
  ([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1)), so calm and
  volatile spells each persist. Unlike the default, this fits the raw yield level
  rather than its log (the generic GARCH fit has no log-space variant, the same
  limitation as `Credit`), and belief overrides do not apply.
- `condition_on_business_cycle` adds a pull from the leading indicator's
  step-to-step change, so the yield tends to move with the economy. It requires
  `leading_indicator.enabled: true`, forces this entry onto
  `leading_indicator.period`, and also fits the raw yield level.

The Wilkie cascade: in the Wilkie (1986) framework (`factor-sets/wilkie.yaml`),
inflation is simulated first and the other variables follow from it in one
direction, nothing feeding back into inflation. A `condition_on_inflation` entry
is the dividend yield step of that cascade; `DividendGrowth` then reads this
entry's own realised shocks, and `equities[].method="wilkie_derived"` sets the
share price to the dividend index divided by this yield. Because
`DividendGrowth` must rebuild those shocks from the plain log-space fit, a
`dividend_growth[]` entry paired (via `dividend_yield_name`) with a GARCH or
business-cycle-conditioned entry is rejected when the configuration is loaded.

The data are derived, since the Finance Toolkit has no dedicated dividend yield
series: `Toolkit.get_historical_data(period="daily")` already carries every
ticker's raw `Close` price and its `Dividends` (the cash actually paid, not
adjusted). The yield is the sum of dividends over the trailing `window` trading
days divided by `Close`. Raw `Close` is used rather than `Adj Close`, because the
adjusted price already folds reinvested dividends in, and pairing it with
`Dividends` again would count them twice. A ticker that pays no dividends has no
sensible zero-yield fallback, so it raises. Prices come from Financial Modeling
Prep when an API key is set, otherwise from Yahoo Finance; on the Financial
Modeling Prep Free plan the dividend history is capped at the five most recent
payments, too short for a trailing-year window, so a free key does worse here
than no key at all.

This module models the yield level, not dividend growth on its own (see
`DividendGrowth`, Wilkie-only) or the timing of individual payments.

Configuration (`dividend_yield[i]` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `name` | `dividend_yield` | The factor's name in the simulated output; unique across all factor lists. |
| `ticker` | `SPY` | Any dividend-paying ticker the `Toolkit` includes. |
| `currency` | `USD` | The ticker's listing currency; descriptive metadata used by reporting only. |
| `window` | `252` | Trading days of trailing dividends summed for one yield (252 is about a year). |
| `period` | `daily` | Calibration frequency; the source is daily and the yield is averaged to coarser ones. |
| `condition_on_inflation` | `false` | Add Wilkie's inflation term; forces this entry onto that inflation's period. |
| `inflation_name` | `inflation` | Which `inflation[i].name` the inflation term reads. |
| `volatility_model` | `constant` | `constant` or `garch`. |
| `condition_on_business_cycle` | `false` | Requires `leading_indicator.enabled: true`. |
| `beliefs.mean_reversion_speed` | `null` | Override the fitted speed; must be above 0. |
| `beliefs.long_run_mean` | `null` | Override the fitted normal level, in log-yield units (see below). |
| `beliefs.volatility` | `null` | Override the fitted volatility; must be above 0. |

A belief left `null` keeps the calibrated value. Beliefs apply only with
`volatility_model: constant`, and are rejected together with
`condition_on_inflation: true` (there is no override for the inflation term).
Because the fit is on the log yield, a belief about the normal level is a log
too: a 2% target yield is `log(0.02)`, about `-3.9`, not `0.02`; check the
calibrated `long_run_mean` (`Scenarios.calibrate(config).calibrated_params`)
first. In a regime file, address one entry's beliefs with a dotted
`"dividend_yield.<name>"` key.

**References:**

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92, eq. 3.17 ("Equity Dividend Yields"). <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>
- Schwartz, E.S. (1997). "The Stochastic Behavior of Commodity Prices: Implications for Valuation and Hedging." Journal of Finance, 52(3), 923-973. <https://doi.org/10.1111/j.1540-6261.1997.tb02721.x>
- Uhlenbeck, G.E., Ornstein, L.S. (1930). "On the Theory of the Brownian Motion." Physical Review, 36(5), 823-841. <https://doi.org/10.1103/PhysRev.36.823>
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." Journal of Econometrics, 31(3), 307-327. <https://doi.org/10.1016/0304-4076(86>)90063-1

## calibrate

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

Calibrate one ticker's dividend yield from its history: derive the trailing
dividend yield from daily prices and dividends, and fit how fast its logarithm
returns to its normal level (`mean_reversion_speed`), what that normal level is
(`long_run_mean`) and how much it swings (`volatility`).

In plain terms: this learns from the past how a ticker's dividend yield behaves,
so the simulated scenarios drift and swing the way the real yield has. The speed
reads as a half-life: a speed of 0.15 a year means a gap from the normal level
has halved after about 4.6 years (ln 2 / 0.15), so a dividend yield is a slow,
persistent variable.

The calculation runs in three steps. The daily history is always fetched, whatever
`period` is, because the trailing sum needs day-level data. The `Dividends` paid
over the last `window` trading days are summed and divided by that day's `Close`,
giving one yield per day; for a `period` coarser than daily these are averaged per
period. The default fit then regresses each period's change in the log yield on
the previous log yield by ordinary least squares, the discretized form of the
Ornstein-Uhlenbeck equation. Because of that log fit, `long_run_mean` is a log
yield: `exp(long_run_mean)` is the yield the process is pulled toward, while
`initial_value` is today's yield as a decimal (0.0099 is 0.99%).

Also known as: trailing twelve-month dividend yield calibration, log-yield
mean-reversion fit.

**Args:**

- <u>name (str):</u> this entry's name, used to key params()/changes() and as the factor name in the simulation (e.g. "spy_yield", "dow_yield").
- <u>ticker (str):</u> the ticker to derive a trailing yield for; any ticker the shared Toolkit instance includes, typically a dividend-paying broad index or ETF (e.g. "SPY").
- <u>window (int):</u> trading days of trailing dividends to sum for one yield observation (252, about one year, is the default: a trailing twelve-month yield, the standard convention).
- <u>period (str):</u> sampling frequency for calibration ("daily", "weekly", "monthly", "quarterly", "yearly"); the underlying price/dividend data is always fetched daily (the trailing window needs day-level granularity to sum), but the derived yield series is itself resampled (pandas mean-resample) to `period` before fitting, so dt stays consistent with the actual observation spacing.
- <u>inflation_covariate (pl.Series &#124; None):</u> a paired inflation entry's raw historical rate series at the same period. When supplied, adds Wilkie's (1986) inflation-sensitivity term to the fit (see `dividend_yield_model.fit_dividend_yield_process`); if the two histories differ in length, both are cut to their common most recent stretch. Incompatible with volatility_model="garch" and business_cycle_covariate.
- <u>volatility_model (str):</u> "constant" (the default, Ahlgrim/D'Arcy/ Gorvett's own log-yield OU fit via fit_dividend_yield_process) or "garch" (GARCH(1,1) time-varying volatility, Bollerslev 1986); the GARCH path fits the raw (not log) yield level via the generic fit_garch_process, the same "constant-vol path is log-space, GARCH/covariate paths are raw-level" limitation `Credit` has.
- <u>business_cycle_covariate (pl.Series &#124; None):</u> a business-cycle indicator's raw historical level series (e.g. LeadingIndicator.series). When supplied, adds an additive drift term on the covariate's step-to-step change (business-cycle conditioning); incompatible with volatility_model="garch" and inflation_covariate. Also fits the raw yield level (fit_ou_process_with_covariate), not the log yield.
- <u>business_cycle_covariate_dates (pl.Series &#124; None):</u> the dates paired with `business_cycle_covariate` (e.g. LeadingIndicator.dates), same length and order. Required whenever `business_cycle_covariate` is supplied; the yield series and the leading indicator are fetched independently and forced onto the same *period* but not guaranteed the same *start date*, so this entry's own dates and the covariate's are inner-joined on date before fitting.

**Returns:**

<u>DividendYieldParams &#124; GARCHParams &#124; OUCovariateParams:</u> the calibrated process parameters: DividendYieldParams for the default log-space fit (with `inflation_sensitivity` set when inflation_covariate is supplied), GARCHParams when volatility_model="garch", OUCovariateParams when business_cycle_covariate is supplied.

**Raises:**

- <u>ValueError:</u> if period or volatility_model is not recognized, window is not positive, business_cycle_covariate is combined with volatility_model="garch" or inflation_covariate, volatility_model="garch" is combined with inflation_covariate, business_cycle_covariate is supplied without business_cycle_covariate_dates (or vice versa), or the derived yield series fails its fitter's own validation (too few observations, a non-positive yield, or no fitted mean reversion).
- <u>KeyError:</u> if `ticker` is not in the Toolkit's historical data, which includes the Toolkit's benchmark ticker (SPY by default): the Finance Toolkit relabels the benchmark's columns "Benchmark", so build the Toolkit with `benchmark_ticker=None`.
- <u>pl.exceptions.ColumnNotFoundError:</u> if `ticker` has no `Dividends` data (e.g. a non-dividend-paying ticker); this factor requires a dividend-paying ticker, there is no sensible zero-yield fallback.

**Notes:**

- `Close` is the raw price, not `Adj Close`: the adjusted price already includes
  reinvested dividends, so dividing `Dividends` by it would count them twice.
- The first `window` trading days produce no yield (the trailing sum is not yet
  full), so the usable history starts about a year after the Toolkit's
  `start_date`.
- Ahlgrim, D'Arcy and Gorvett found dividend yield close to a random walk, so a
  window that shows no mean reversion raises rather than returning a fit; a
  longer history or a coarser `period` usually helps.
- On a Financial Modeling Prep Free-plan key the dividend history holds only the
  five most recent payments, too few for a trailing-year sum; no key at all
  (the Yahoo Finance path) works better.
- `changes(name)` returns the period-to-period change in the *log* yield, the
  series the correlation matrix is estimated from.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.dividend_yield.dividend_yield_controller import DividendYield

# No API key: the Yahoo Finance path keeps the full dividend history (see Notes).
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

SPY yields 0.99% today and is pulled toward exp(-4.2784) = 1.39%, with a
half-life of about 4.7 years; JNJ yields 2.05% and is pulled toward
exp(-3.7328) = 2.39%, even more slowly (a half-life of about 5.4 years). Both
speeds are low, in line with the near-random-walk finding of the source paper.

**References:**

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92, eq. 3.17. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." Journal of Econometrics, 31(3), 307-327. <https://doi.org/10.1016/0304-4076(86>)90063-1

## names

```python
dividendyield.names  # property -> list[str]
```

The names of every dividend yield entry calibrated so far, in calibration order.

## params

```python
params(name: str) -> DividendYieldParams | GARCHParams | OUCovariateParams
```

The calibrated process parameters for one dividend yield entry.

**Args:**

- <u>name (str):</u> the entry's name, as passed to calibrate().

**Raises:**

- <u>RuntimeError:</u> if calibrate(name, ...) hasn't been called yet.

## step_function

```python
dividendyield.step_function  # property
```

The Ahlgrim/D'Arcy/Gorvett log-yield step function (stateless, shared across every entry).

## series

```python
series(name: str) -> pl.Series
```

The raw historical trailing-yield series (actual, not log) for one entry,
the same series calibrate() fit against; used by dividend_growth's
`dividend_yield_model.reconstruct_dividend_yield_residuals`, which needs
the raw level series to recover this process's own realised shocks (see
that function's docstring for why).

**Args:**

- <u>name (str):</u> the entry's name, as passed to calibrate().

**Raises:**

- <u>RuntimeError:</u> if calibrate(name, ...) hasn't been called yet.

## time_step

```python
time_step(name: str) -> float
```

The time increment (in years) between observations one entry was actually
calibrated at; used alongside series() by dividend_growth's residual
reconstruction (see dividend_yield_model.reconstruct_dividend_yield_residuals),
which needs the exact dt this entry's `params` were fit with.

**Args:**

- <u>name (str):</u> the entry's name, as passed to calibrate().

**Raises:**

- <u>RuntimeError:</u> if calibrate(name, ...) hasn't been called yet.

## changes

```python
changes(name: str) -> pl.DataFrame
```

Dated period log-yield changes for one dividend yield entry, from the same
data calibrate() already fetched, reused for cross-factor correlation
estimation (Dependence) instead of triggering a second Finance Toolkit fetch.

**Args:**

- <u>name (str):</u> the entry's name, as passed to calibrate().

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` (pl.Date) and `value` (f64); see helpers.dated_changes().

**Raises:**

- <u>RuntimeError:</u> if calibrate(name, ...) hasn't been called yet.
