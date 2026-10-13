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

The Dividend Growth module simulates how a company's or fund's dividends grow, as a dividend index: the dividends paid
over the past year, tracked through time.

It is part of the Wilkie model (`factor-sets/wilkie.yaml`), where inflation is simulated first and the other variables
follow from it. Dividends keep up with inflation, with a delay, and react to surprises in the dividend yield. Divided
by the paired dividend yield, the index gives the simulated share price (`equities[].method="wilkie_derived"`). It is
opt-in: `dividend_growth` is empty by default, and every entry needs a paired `inflation[]` and `dividend_yield[]`
entry.

The model is the share dividend index of Wilkie (1986), in his "Reduced Basis" form:

```text
dln D(t) = DMU + DW * dlnQ(t) + DX * DM(t-1) + DY * YE(t-1) + DSD * DZ(t)
DM(t) = DD * dlnQ(t) + (1 - DD) * DM(t-1)
```

where `dln D(t)` is the growth of the log dividend index and `dlnQ(t)` the inflation rate in log terms. Each
coefficient has a plain reading:

- `DMU` (`long_run_drift`): long-term real dividend growth, net of inflation.
- `DW` (`inflation_sensitivity`): how much of this period's inflation passes straight into dividends.
- `DM`, with weight `DD` (`carried_forward_weight`, fixed at Wilkie's 0.2): a slowly updating average of past
  inflation, so dividends keep catching up after inflation moves; `DX` (`carried_forward_sensitivity`) is its effect.
- `DY` (`yield_residual_sensitivity`): the effect of last period's surprise in the dividend yield, `YE(t-1)`.
- `DSD` (`volatility`): the size of the index's own random shock.

Data: the Finance Toolkit has no dividend index series, so the `Dividends` paid over the trailing `window` trading
days are summed, the numerator `DividendYield` divides by the price. An entry runs at its paired inflation entry's
period, and the paired dividend yield must use the plain fit (no `garch` or business-cycle option).

Configuration (`dividend_growth[i]` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `name` | `dividend_growth` | Name in the output. |
| `ticker` | `SPY` | A dividend-paying ticker. |
| `currency` | `USD` | Reporting label. |
| `window` | `252` | Trading days of dividends summed for one index value. |
| `inflation_name` | `inflation` | The `inflation[i].name` that drives `dlnQ(t)` and sets the period. |
| `dividend_yield_name` | `dividend_yield` | The `dividend_yield[i].name` that supplies `YE(t-1)`. |
| `carried_forward_weight` | `0.2` | `DD`, strictly between 0 and 1. |
| `beliefs.<field>` | `null` | Override a fitted value, such as `inflation_sensitivity` or `volatility`. |

**References:**

- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>
- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. The modular framework that positions itself against Wilkie's model. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>

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

Calibrate one ticker's Wilkie (1986) dividend growth model from its dividend history.

It fits how dividend growth responds to current inflation (`inflation_sensitivity`), to past inflation carried
forward (`carried_forward_sensitivity`) and to the dividend yield's last surprise (`yield_residual_sensitivity`),
plus its own drift (`long_run_drift`) and swings (`volatility`).

As in Wilkie
([1986](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf)),
with `carried_forward_weight` fixed, one ordinary least squares regression fits them all. The inputs are matched
by length, so they must share a period and end date.

**Args:**

- <u>name (str):</u> the entry's name.
- <u>inflation (pl.Series):</u> the paired inflation entry's history of annual rates (`Inflation.series`).
- <u>yield_residual (np.ndarray):</u> the paired dividend yield's past surprises, rebuilt as in the example.
- <u>ticker (str):</u> any dividend-paying ticker in the Toolkit. Defaults to "SPY".
- <u>window (int):</u> trading days of dividends summed for one index value. Defaults to 252.
- <u>period (str):</u> the fit's time step, "daily" to "yearly", matching both inputs. Defaults to "daily".
- <u>carried_forward_weight (float):</u> `DD`, the weight of current inflation in the carried-forward average, strictly between 0 and 1. Defaults to 0.2.

**Returns:**

<u>DividendGrowthParams:</u> the five fitted coefficients, plus `initial_value` (the last dividend index level) and `initial_carried_forward_inflation`.

**Raises:**

- <u>ValueError:</u> if an input is invalid, the ticker has no dividend data, or the history is too short.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.dividend_growth.dividend_growth_controller import DividendGrowth
from financescenarios.factors.dividend_yield.dividend_yield_controller import DividendYield
from financescenarios.factors.dividend_yield.dividend_yield_model import reconstruct_dividend_yield_residuals
from financescenarios.factors.inflation.inflation_controller import Inflation

toolkit = Toolkit(["JNJ"], start_date="1995-01-01", end_date="2019-12-31", benchmark_ticker=None)

inflation = Inflation(toolkit)
inflation.calibrate("inflation", country="United States", period="monthly", method="wilkie_ar1")
inflation_series = inflation.series("inflation")

dividend_yield = DividendYield(toolkit)
yield_params = dividend_yield.calibrate(
    "dividend_yield", ticker="JNJ", period="monthly", inflation_covariate=inflation_series
)

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
| carried_forward_sensitivity (DX) | -0.0176 |
| yield_residual_sensitivity (DY) | -0.1927 |
| volatility (DSD) | 0.0274 |
| initial_value | 3.7500 |

The coefficients are per month, while inflation is an annual rate: 0.0205 x 12 = 0.25, so about a quarter of
inflation passes into the same month's dividends.

## names

```python
dividendgrowth.names  # property -> list[str]
```

The names of every dividend growth entry calibrated so far, in calibration order.

## params

```python
params(name: str) -> DividendGrowthParams
```

The calibrated parameters of one dividend growth entry.

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if `name` has not been calibrated yet.

## changes

```python
changes(name: str) -> pl.DataFrame
```

The dated period-to-period changes in one entry's log dividend index, from the data `calibrate` already fetched.
The correlation matrix is estimated from these.

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if `name` has not been calibrated yet.
