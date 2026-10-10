---
title: "DividendGrowth"
seo_title: "DividendGrowth Reference – Finance Scenarios"
excerpt: "Dividend growth, one per ticker."
description: "Dividend growth, one per ticker."
author_profile: false
permalink: /projects/financescenarios/docs/reference/dividend-growth
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Dividend growth, one per ticker. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.factors.dividend_growth.dividend_growth_controller import DividendGrowth
```

```python
DividendGrowth(toolkit: Toolkit)
```

The Dividend Growth module simulates how fast a company's or fund's dividends grow,
as a dividend index: the dividends paid over the past year, tracked through time.
Dividends tend to keep up with inflation, with a delay, and move after a surprise
in the dividend yield, and those links are the behaviour this module captures.

In plain terms: in the Wilkie (1986) framework (`factor-sets/wilkie.yaml`), add a
ticker such as JNJ and its dividend index becomes a variable in the simulated
scenarios, driven by the simulated inflation rate and by the shocks of the paired
dividend yield. Divided by that dividend yield, it gives the simulated share price
(`equities[].method="wilkie_derived"`), so this is the dividend leg of Wilkie's
equity model. It is opt-in: `dividend_growth` is an empty list by default, and
each entry is calibrated independently and named by its own `name`.

Wilkie's model is a *cascade*: inflation is simulated first, and dividend yield,
dividend growth and long-term interest rates each follow from it in one direction,
with nothing feeding back into inflation. Every other framework in this project
links inflation to the rest only through the estimated correlation matrix; Wilkie
argues these variables are genuine functions of inflation's own path, and offering
his framework lets a user compare the two approaches on the same engine. This
module is Wilkie-only: there is no other dividend growth process here, so every
entry needs a paired `inflation[]` entry and a paired `dividend_yield[]` entry.

The model is the share dividend index process of Wilkie
([1986](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf)),
in his own "Reduced Basis" parameterisation (Table 5, `DB=0`):

```text
dln D(t) = DMU + DW * dlnQ(t) + DX * DM(t-1) + DY * YE(t-1) + DSD * DZ(t)
DM(t) = DD * dlnQ(t) + (1 - DD) * DM(t-1)
```

where `dln D(t)` is the period's growth in the log dividend index and `dlnQ(t)`
the force of inflation (the inflation rate in log terms), read directly from the
paired inflation entry, which reports it as an annual rate whatever the period.
Each coefficient has a plain reading:

- `DMU` (`long_run_drift`): long-term real dividend growth, net of inflation.
  Wilkie sets it to 0.0 in both his published bases but leaves it free, so it is
  fitted here.
- `DW` (`inflation_sensitivity`): how much of this period's inflation passes
  straight into dividends.
- `DM(t)` with weight `DD` (`carried_forward_weight`): a slowly updating average of
  past inflation (an exponentially weighted moving average), so dividends keep
  catching up with inflation for a while after it moves. `DD` is a fixed setting
  (0.2, Wilkie's own value), not fitted, because it enters non-linearly through
  its own recursion. `DX` (`carried_forward_sensitivity`) is the effect of last
  period's `DM`.
- `DY` (`yield_residual_sensitivity`): the effect of the paired dividend yield's
  own surprise (its realised shock) one period earlier, `YE(t-1)`. Wilkie's account
  of the cause runs the other way, share prices anticipate a dividend change and
  the yield moves first, but "it is convenient in the model to reflect the temporal
  sequence", so last period's already-realised yield surprise drives this period's
  dividend growth. The shock is rebuilt exactly from the yield path (actual change
  minus expected drift, see
  `dividend_yield_model.reconstruct_dividend_yield_residuals`), since the engine
  passes simulated levels, not raw shocks, between factors.
- `DSD * DZ(t)` (`volatility`): the index's own random shock.

Wilkie's full model also carries a moving-average term on its own previous shock
(`DB * DE(t-1)`). It is left out because fitting it needs a Kalman filter or an
iterative fit used nowhere else in this project, which fits everything by ordinary
least squares; this is not a local shortcut, since Wilkie's own Reduced Basis
already sets `DB=0` as a published alternative.

The data are derived, since the Finance Toolkit has no dividend index series: the
`Dividends` column of `Toolkit.get_historical_data(period="daily")` is summed over
the trailing `window` trading days, the same numerator `DividendYield` divides by
the price. An entry has no `period` of its own: it always runs at its paired
inflation entry's period, because current inflation drives every regression row
and must be a genuinely same-period observation. The paired dividend yield must
resolve to that same period, or calibration raises. The paired dividend yield must
also use the plain log-space fit: one with `volatility_model: garch` or
`condition_on_business_cycle: true` is rejected when the configuration is loaded,
because its shocks cannot be rebuilt.

During simulation the carried-forward inflation `DM` and the previous yield shock
are carried from step to step by a stateful stepper; before the first simulated
step no previous yield shock exists, so it is taken as zero for that step only.

Scope: Wilkie's cascade does not model unemployment, real estate, credit, FX, a
leading indicator or commodities, and only the 1986 original is implemented, not
later extensions such as the 1995 short-rate extension. Wilkie fitted his model to
1919-1982 UK data; the shipped preset applies the same equations to US data.

Configuration (`dividend_growth[i]` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `name` | `dividend_growth` | The factor's name in the simulated output; unique across all factor lists. |
| `ticker` | `SPY` | Any dividend-paying ticker the `Toolkit` includes. |
| `currency` | `USD` | The ticker's listing currency; descriptive metadata used by reporting only. |
| `window` | `252` | Trading days of trailing dividends summed for one dividend index value. |
| `inflation_name` | `inflation` | Which `inflation[i].name` drives `dlnQ(t)`; also sets the period. |
| `dividend_yield_name` | `dividend_yield` | Which `dividend_yield[i].name` supplies `YE(t-1)`. |
| `carried_forward_weight` | `0.2` | `DD`, strictly between 0 and 1; Wilkie's published value. |
| `beliefs.long_run_drift` | `null` | Override the fitted `DMU`. |
| `beliefs.inflation_sensitivity` | `null` | Override the fitted `DW`. |
| `beliefs.carried_forward_sensitivity` | `null` | Override the fitted `DX`. |
| `beliefs.yield_residual_sensitivity` | `null` | Override the fitted `DY`. |
| `beliefs.volatility` | `null` | Override the fitted `DSD`; must be above 0. |

A belief left `null` keeps the calibrated value. `carried_forward_weight` has no
belief, since it is a fixed setting rather than a fitted value; change it on the
entry itself.

**References:**

- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>
- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. The modular successor framework that positions itself against Wilkie's cascade. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>

## calibrate

```python
calibrate(
    name: str,
    inflation: pl.Series,
    yield_residual: np.ndarray,
    ticker: str = 'SPY',
    window: int = 252,
    period: str = 'daily',
    carried_forward_weight: float = 0.2,
) -> DividendGrowthParams
```

Calibrate one ticker's Wilkie (1986) dividend growth process from its history:
derive the trailing dividend index from daily dividends, and fit how its growth
responds to current inflation (`inflation_sensitivity`), to the carried-forward
average of past inflation (`carried_forward_sensitivity`) and to the paired
dividend yield's previous surprise (`yield_residual_sensitivity`), plus its own
drift (`long_run_drift`) and random swings (`volatility`).

In plain terms: this learns from the past how a ticker's dividends grew with
inflation and after yield surprises, so the simulated dividend index (and the
share price derived from it) behaves the way the real one has. The inflation
input is an annual rate while the dividend growth is per period, so at a monthly
period an `inflation_sensitivity` of 1/12 (about 0.083) passes inflation one for
one into that month's dividend growth; a value near 0 means dividends do not
react within the period.

Given the fixed weight `carried_forward_weight` (`DD`), the carried-forward
inflation `DM(t)` is a fixed function of the inflation series, so all the other
coefficients come from one ordinary least squares regression of the log dividend
growth on a constant, current inflation, last period's `DM` and last period's
yield shock. The dividend index, the inflation series and the yield shocks are
fetched separately, so before fitting all three are cut to their common most
recent stretch (matching by length rather than by date). `initial_value` is the
last dividend index level (dividends per share over the trailing window) and
`initial_carried_forward_inflation` the last `DM`, the simulation's starting
points.

Also known as: Wilkie share dividend index model, Wilkie dividend model.

**Args:**

- <u>name (str):</u> this entry's name, used to key params()/changes() and as the factor name in the simulation.
- <u>inflation (pl.Series):</u> the paired inflation entry's raw historical rate series (see inflation_controller.Inflation.series); Wilkie's dlnQ(t), used directly, not its change, because this project's inflation factor already simulates the rate itself.
- <u>yield_residual (np.ndarray):</u> the paired dividend yield entry's own reconstructed shocks (see dividend_yield_model. reconstruct_dividend_yield_residuals), one shorter than the dividend index series after alignment.
- <u>ticker (str):</u> the ticker to derive a dividend index for; any dividend-paying ticker the shared Toolkit instance includes.
- <u>window (int):</u> trading days of trailing dividends to sum for one dividend index observation (matches dividend_yield's own window convention).
- <u>period (str):</u> sampling frequency for calibration ("daily", "weekly", "monthly", "quarterly", "yearly"); must match the period of `inflation` and of the dividend yield behind `yield_residual`. The dividends are always fetched daily and averaged to `period`.
- <u>carried_forward_weight (float):</u> DD, the fixed EWMA smoothing weight on current inflation (see DividendGrowthParams.carried_forward_weight).

**Returns:**

<u>DividendGrowthParams:</u> the calibrated process parameters.

**Raises:**

- <u>ValueError:</u> if period is not recognized, window is not positive, or the derived series fails fit_dividend_growth_process's own validation (too few observations, a non-positive dividend index, or carried_forward_weight outside (0, 1)).
- <u>KeyError:</u> if `ticker` is not in the Toolkit's historical data, which includes the Toolkit's benchmark ticker (SPY by default), relabelled "Benchmark" by the Finance Toolkit; build the Toolkit with `benchmark_ticker=None`.
- <u>pl.exceptions.ColumnNotFoundError:</u> if `ticker` has no `Dividends` data.

**Notes:**

- The alignment is by length, not by date, so the inflation series, the yield
  shocks and the dividends must already share a period and an end date; the
  configuration-driven path (`Scenarios.calibrate`) enforces the shared period.
- The first regression row has no earlier yield shock, so it is taken as zero.
- On a Financial Modeling Prep Free-plan key the dividend history holds only the
  five most recent payments, too few for a trailing-year sum; no key at all
  (the Yahoo Finance path) works better.
- Wilkie's own fit used 1919-1982 UK data; the shipped preset
  (`settings/wilkie.yaml`) caps the history to 1995-2019, a window chosen for
  Wilkie's Consols rate rather than for this module.
- `changes(name)` returns the period-to-period change in the *log* dividend
  index, the series the correlation matrix is estimated from.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.dividend_growth.dividend_growth_controller import DividendGrowth
from financescenarios.factors.dividend_yield.dividend_yield_controller import DividendYield
from financescenarios.factors.dividend_yield.dividend_yield_model import reconstruct_dividend_yield_residuals
from financescenarios.factors.inflation.inflation_controller import Inflation

toolkit = Toolkit(
    ["JNJ"],
    start_date="1995-01-01",
    end_date="2019-12-31",
    benchmark_ticker=None,
)

# The Wilkie cascade: inflation first, then the inflation-conditioned dividend yield.
inflation = Inflation(toolkit)
inflation.calibrate("inflation", country="United States", period="monthly", method="wilkie_ar1")
inflation_series = inflation.series("inflation")

dividend_yield = DividendYield(toolkit)
yield_params = dividend_yield.calibrate(
    "dividend_yield", ticker="JNJ", period="monthly", inflation_covariate=inflation_series
)

# Rebuild the yield's own shocks on the same stretch the yield was fitted on.
yield_level = dividend_yield.series("dividend_yield")
length = min(yield_level.len(), inflation_series.len())
yield_residual = reconstruct_dividend_yield_residuals(
    yield_level.tail(length),
    yield_params,
    dividend_yield.time_step("dividend_yield"),
    inflation=inflation_series.tail(length),
)

dividend_growth = DividendGrowth(toolkit)
dividend_growth.calibrate(
    "dividend_growth", inflation=inflation_series, yield_residual=yield_residual, ticker="JNJ", period="monthly"
)
```

Which returns (calibrated on 2026-10-04):

| Parameter | Value |
|:----------|------:|
| long_run_drift (DMU) | 0.0085 |
| inflation_sensitivity (DW) | 0.0205 |
| carried_forward_weight (DD) | 0.2000 |
| carried_forward_sensitivity (DX) | -0.0176 |
| yield_residual_sensitivity (DY) | -0.1927 |
| volatility (DSD) | 0.0274 |
| initial_value | 3.7500 |
| initial_carried_forward_inflation | 0.0092 |

The coefficients are per period (here per month): JNJ's dividend index grew about
0.85% a month (roughly 10% a year) over 1996-2019 on its own drift. `DW` applies to
an annual inflation rate, so 0.0205 x 12 = 0.25: about a quarter of inflation
passes into the same month's dividend growth. The negative `DY` means a
surprise drop in the yield (the price rising ahead of a dividend increase) is
followed by faster dividend growth the next month, Wilkie's anticipation story.
The index starts at $3.75, JNJ's dividends per share over 2019. The paired
inflation-conditioned yield fit on the same data gave a speed of 0.1032, a
normal level of exp(-3.6397) = 2.63% and an `inflation_sensitivity` of 0.1290.

**References:**

- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. Sections 3.7-3.9, the share dividend index model and its Reduced Basis. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>

## names

```python
dividendgrowth.names  # property -> list[str]
```

The names of every dividend growth entry calibrated so far, in calibration order.

## params

```python
params(name: str) -> DividendGrowthParams
```

The calibrated process parameters for one dividend growth entry.

**Args:**

- <u>name (str):</u> the entry's name, as passed to calibrate().

**Raises:**

- <u>RuntimeError:</u> if calibrate(name, ...) hasn't been called yet.

## changes

```python
changes(name: str) -> pl.DataFrame
```

Dated period log-dividend-index changes for one dividend growth entry,
from the same data calibrate() already fetched, reused for cross-factor
correlation estimation (Dependence) instead of triggering a second
Finance Toolkit fetch.

**Args:**

- <u>name (str):</u> the entry's name, as passed to calibrate().

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` (pl.Date) and `value` (f64); see helpers.dated_changes().

**Raises:**

- <u>RuntimeError:</u> if calibrate(name, ...) hasn't been called yet.
