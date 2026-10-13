---
title: Units
seo_title: Units Documentation – Finance Scenarios
excerpt: "Rates are annualized decimals and prices read as their annualized return since the start. Why, and how to convert to cumulative, simple and log returns."
description: "Why Finance Scenarios reports annualized decimals and annualized returns since start, and how to convert to cumulative, simple and log returns."
author_profile: false
permalink: /projects/financescenarios/docs/units
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Every number is on one scale: an **annualized decimal**. A short rate of `0.035` is 3.5% a year, inflation of `0.026` is 2.6% a year, an equity return of `0.095` is 9.5% a year. A fitted parameter, a belief you set, a regime target and a simulated value can be compared directly, whatever the data frequency or the step of the run.

## How Each Series Is Fitted

Each series is fitted in the form economists and actuaries normally use for it:

| Series | Fitted as | Why |
|:-------|:----------|:----|
| Interest rates, credit spreads, unemployment, dividend yield | The level, as a decimal | They mean-revert as levels ([Vasicek, 1977](<https://doi.org/10.1016/0304-405X(77)90016-2>)) |
| Inflation, house prices | Year-over-year change of the index | The headline figure statistics offices publish, free of seasonality |
| Equities, commodities, FX | Log returns of the price | Prices are not stationary, their returns are, and log returns add up over time |
| Dividends (Wilkie) | Log change of the dividend index | [Wilkie's (1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf) own specification |
| Leading indicator | Index points around 100 | It is built as a stationary cycle around 100 |
| Mortality | Logit of death rates | [Cairns, Blake and Dowd's (2006)](https://doi.org/10.1111/j.1539-6975.2006.00195.x) specification |

Year-over-year inflation is smooth: consecutive monthly readings share eleven of their twelve months. A monthly fit on it shows slower mean reversion and smaller monthly shocks than a fit on month-on-month changes. This is the convention economic scenario generators commonly calibrate inflation on, and it means a belief about inflation is stated as a year-over-year rate.

## How Results Read

A rate reads as itself. A price (an equity, commodity, exchange rate or portfolio value) reads by default as its **annualized return since the start**, the constant yearly return that takes today's value to the value at time $$t$$ (in years):

$$
R_t = \left(\frac{S_t}{S_0}\right)^{1/t} - 1
$$

An equity path from 769 to 1,209 over five years reads as 9.5% a year. This is the CAGR, the way returns are quoted in investment reports, and it puts a one-year and a thirty-year outcome on the same scale. Its spread narrows with the horizon, since good and bad years average out, while the spread of the cumulative return keeps widening. Over the first months it is extremely wide, since a few weeks' move is scaled up to a year.

Every table and chart can show another reading instead:

| Reading | A price | Inflation | A rate |
|:--------|:--------|:----------|:-------|
| Default | annualized return since start | the rate | the rate |
| `level` | the price | a price index, 100 at start | the rate |
| `change` | % change over one step | % change of the index over one step | change over one step |
| `yoy` | % change over one year | % change of the index over one year | change over one year |
| `cumulative` | % change since start | % change of the index since start | change since start |
| `annualized` | yearly return since start | average yearly growth since start | not available |

A change of a rate is a **difference** in its own units: `0.005` is half a percentage point (50 basis points), not a percentage of a percentage.

```python
result.describe()                                         # each factor's default reading
result.describe(metric="cumulative")                      # change since start
result.plot("united_states_inflation", metric="level")    # inflation as a price index from 100
result.to_dataframe("us_broad", levels=True)              # the simulated prices themselves
```

## Converting

With $$R$$ the annualized return over $$t$$ years, $$C$$ the cumulative return and $$r$$ the log return per year:

$$
1 + C = (1 + R)^t, \qquad r = \ln(1 + R), \qquad R = e^{r} - 1
$$

So 9.5% a year for five years is a cumulative 57%, and a log return of 9.1% a year. Log returns add up over time and are what the models work in; simple returns are what a portfolio earns and reports. The gap grows with volatility: an asset with a 0% median log return still has a positive mean simple return, so the expected return sits above the median scenario.

A simulated inflation rate compounds into its price index the same way, as $$100\,e^{\int \pi_s\,ds}$$. Because a year-over-year rate stands in for the instantaneous rate, the rebuilt index trails actual prices by about half a year, and at 3% it compounds about 0.05 percentage points a year above simple growth. Both are small next to the spread of the scenarios.

## References

- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. <https://doi.org/10.1016/0304-405X(77)90016-2>
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>
- Cairns, A.J.G., Blake, D., Dowd, K. (2006). "A Two-Factor Model for Stochastic Mortality with Parameter Uncertainty: Theory and Calibration." Journal of Risk and Insurance, 73(4), 687-718. <https://doi.org/10.1111/j.1539-6975.2006.00195.x>
