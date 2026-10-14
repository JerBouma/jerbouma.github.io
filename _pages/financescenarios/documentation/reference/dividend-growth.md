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

Dividend growth, one per ticker.

```python
from financescenarios.factors.dividend_growth.dividend_growth_controller import DividendGrowth
```

Simulate how a company's or fund's dividends grow, as a dividend index: the dividends paid over the past year,
tracked through time.

It is part of the Wilkie model (the `wilkie` factor set), a cascade in which inflation drives the other variables.
Over the long run dividends are a real quantity: companies raise payouts with prices, but only partly at once and
the rest over the following years. Equities are therefore an inflation hedge in the long run but not in the short
run, and an inflation shock first lowers real dividends before they catch up. Divided by the paired dividend yield,
the index gives the simulated share price (`equities[].method="wilkie_derived"`). Every entry needs a paired
`inflation[]` and `dividend_yield[]` entry.

The model is the share dividend index of Wilkie (1986), section 3.7, in the form of his Reduced Standard Basis
(Table 1), the simpler version without the DB term that section 3.9 describes:

```text
dln D(t) = DMU + DW * DM(t) + DX * dlnQ(t) + DY * YE(t-1) + DSD * DZ(t)
DM(t) = DD * dlnQ(t) + (1 - DD) * DM(t-1)
```

where `dln D(t)` is the growth of the log dividend index and `dlnQ(t)` the inflation rate in log terms. Each
coefficient has a plain reading:

- `DMU` (`long_run_drift`): long-term real dividend growth, net of inflation.
- `DM`, with weight `DD` (`carried_forward_weight`, Wilkie's 0.2 a year): a slowly updating average of past
  inflation, so dividends keep catching up after inflation moves; `DW` (`lagged_inflation_weight`) is its effect.
- `DX` (`direct_inflation_weight`): how much of this period's inflation passes straight into dividends.
- `DY` (`yield_residual_sensitivity`): the effect of last period's surprise in the dividend yield, `YE(t-1)`.
- `DSD` (`volatility`): the size of the index's own random shock.

Wilkie's model has unit gain, DW + DX = 1 (section 3.7: a given percentage rise in the Retail Prices Index
ends up as the same percentage rise in the dividend index), and the fit imposes it; his bases use
DW = 0.8 and DX = 0.2 (section 3.9).

Data: the Finance Toolkit has no dividend index series, so the `Dividends` paid over the trailing `window` trading
days are summed, the numerator `DividendYield` divides by the price. An entry runs at its paired inflation entry's
period, and the paired dividend yield must use the plain fit (no `garch` or business-cycle option).

The `dividend_growth[i]` keys of a factor set and their defaults are listed on the reference page
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/reference/configuration-classes).

**References:**

- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>
- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. The modular framework that positions itself against Wilkie's model. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
DividendGrowth(toolkit: Toolkit)
```

</details>

## calibrate

Calibrate one ticker's Wilkie (1986) dividend growth model from its dividend history.

It fits how much of current inflation reaches dividends at once (`direct_inflation_weight`, Wilkie's DX), the
rest arriving through the carried-forward average (`lagged_inflation_weight`, DW = 1 - DX), plus the dividend
yield's last surprise (`yield_residual_sensitivity`), the real drift (`long_run_drift`) and the swings
(`volatility`). As in Wilkie
([1986](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf)),
DW + DX = 1, so inflation passes fully into dividends in the long run and equities keep their real value. A
negative `yield_residual_sensitivity` means a jump in the yield (a price fall) is followed by slower dividend
growth, as when a falling market anticipates dividend cuts. Wilkie's DD is a yearly weight and inflation a
yearly rate, so both are converted to the data's period. The inputs are matched by length, so they must share
a period and end date.

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

Which returns (calibrated on 2026-10-14):

| Parameter | Value |
|:----------|------:|
| long_run_drift (DMU) | 0.0020 |
| direct_inflation_weight (DX) | 1.6891 |
| lagged_inflation_weight (DW) | -0.6891 |
| yield_residual_sensitivity (DY) | -0.0923 |
| volatility (DSD) | 0.0355 |
| initial_value | 3.7500 |

Johnson & Johnson's dividends grew 0.2% a month above inflation. They took up inflation faster than Wilkie's
0.2 / 0.8 split: a rise lifts them at once and the slow average then gives part back, one for one in the end.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(
    name: str,
    inflation: pl.Series,
    yield_residual: np.ndarray,
    ticker: str = 'SPY',
    window: int = 252,
    period: str = 'daily',
    carried_forward_weight: float = 0.2,
    unit_gain: bool = True,
) -> DividendGrowthParams
```

**Args:**

- <u>name (str):</u> the entry's name.
- <u>inflation (pl.Series):</u> the paired inflation entry's history of annual rates (`Inflation.series`).
- <u>yield_residual (np.ndarray):</u> the paired dividend yield's past surprises, rebuilt as in the example.
- <u>ticker (str):</u> any dividend-paying ticker in the Toolkit. Defaults to "SPY".
- <u>window (int):</u> trading days of dividends summed for one index value. Defaults to 252.
- <u>period (str):</u> the fit's time step, "daily" to "yearly", matching both inputs. Defaults to "daily".
- <u>carried_forward_weight (float):</u> `DD`, the yearly weight of current inflation in the carried-forward average, strictly between 0 and 1. Defaults to 0.2, Wilkie's value (section 3.9).
- <u>unit_gain (bool):</u> impose Wilkie's DW + DX = 1. Defaults to True; False gives the earlier free fit.

**Returns:**

<u>DividendGrowthParams:</u> the five fitted coefficients, plus `initial_value` (the last dividend index level) and `initial_carried_forward_inflation`.

**Raises:**

- <u>ValueError:</u> if an input is invalid, the ticker has no dividend data, or the history is too short.

</details>

## names

The names of every dividend growth entry calibrated so far, in calibration order.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
dividendgrowth.names  # property -> list[str]
```

</details>

## params

The calibrated parameters of one dividend growth entry.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
params(name: str) -> DividendGrowthParams
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if `name` has not been calibrated yet.

</details>

## changes

The historical changes in one entry's log dividend index, by date, from which its correlations with the other
factors are estimated.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
changes(name: str) -> pl.DataFrame
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if `name` has not been calibrated yet.

</details>

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

{% raw %}
### fit_dividend_growth_process

Fit Wilkie's (1986) share dividend index to a dividend history, a paired inflation history and the paired
dividend yield's past shocks.

Wilkie ties dividends to inflation with unit gain. A given percentage rise in the Retail Prices Index ends up as
the same percentage rise in the dividend index (section 3.7). Part of the effect is immediate (DX) and part
arrives through a slowly
updating average of past inflation (DW); his bases use DW = 0.8 and DX = 0.2 (section 3.9). The fit imposes
DW + DX = 1, so equities hold their real value against inflation in the long run, and estimates DX, DMU and DY
by one ordinary least squares regression. DD is fixed, not fitted: Wilkie's DD is a yearly weight, the share of
the current inflation rate that enters the dividend model each year (section 3.8), so it is
converted to the data's step, as is the inflation rate, which is quoted per year.

The formula is as follows:

$$
d = 1 - (1 - \text{DD}) ^{\text{dt}}
$$

$$
\operatorname{DM}(t) = d \cdot I(t) + (1 - d) \cdot \operatorname{DM}(t-1),\;\; \operatorname{DM}(0) = I(0)
$$

$$
\text{ln}\; D (t) - \text{ln}\; D (t-1) - \operatorname{DM}(t) \cdot \text{dt} = \text{DMU} + \text{DX} \cdot (I(t) - \operatorname{DM}(t)) \cdot \text{dt} + \text{DY} \cdot \operatorname{YE}(t-1) + e(t)
$$

$$
\text{DW} = 1 - \text{DX}
$$

$$
\text{DSD} = \sqrt{\text{sum}\; e (t) ^{2} / (n - 3)}
$$

Where I(t) is the annual inflation rate, dt the step in years, n the number of regression rows and YE(t-1) zero
on the first row. With `unit_gain=False` the earlier free fit is used instead: DW and DX unrestricted, inflation
and DD taken per step as given.

**References:**

- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. Sections 3.7-3.9 and Table 1. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_dividend_growth_process(
    dividend_index: pl.Series,
    inflation: pl.Series,
    yield_residual: np.ndarray,
    carried_forward_weight: float = 0.2,
    time_step: float = 1.0,
    unit_gain: bool = True,
) -> DividendGrowthParams
```

**Args:**

- <u>dividend_index (pl.Series):</u> the dividend index history, evenly spaced, all above 0.
- <u>inflation (pl.Series):</u> the paired annual inflation rate, same length and dates as `dividend_index`.
- <u>yield_residual (np.ndarray):</u> the paired dividend yield's past shocks (see `reconstruct_dividend_yield_residuals`), one shorter than `dividend_index`.
- <u>carried_forward_weight (float):</u> DD, Wilkie's yearly weight of current inflation in DM(t); default 0.2, his value in both bases (Table 1).
- <u>time_step (float):</u> the time between observations, in years; default 1.0, Wilkie's yearly step.
- <u>unit_gain (bool):</u> impose Wilkie's DW + DX = 1 (default); False gives the free fit.

**Returns:**

<u>DividendGrowthParams:</u> the fitted parameters, with DW and DX in Wilkie's own terms.

**Raises:**

- <u>ValueError:</u> if the inputs differ in length, there are too few rows, a dividend index value is not above 0, or `carried_forward_weight` is not strictly between 0 and 1.

</details>
{% endraw %}
