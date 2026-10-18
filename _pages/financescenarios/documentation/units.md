---
title: Units
seo_title: "Units Documentation | Finance Scenarios"
seo_title_suffix: false
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

Every number is on one scale: an **annualized decimal**.

<div class="ca-nums fs-nums">
  <span><b>0.035</b>a short rate of 3.5% a year</span>
  <span><b>0.026</b>inflation of 2.6% a year</span>
  <span><b>0.095</b>an equity return of 9.5% a year</span>
</div>

A fitted parameter, a belief you set, a regime target and a simulated value can be compared directly, whatever the data frequency or the step of the run.

<div class="ca-nav">
  <a href="#how-each-series-is-fitted"><i class="fas fa-ruler" aria-hidden="true"></i>How each series is fitted</a>
  <a href="#how-results-read"><i class="fas fa-chart-line" aria-hidden="true"></i>How results read</a>
  <a href="#converting"><i class="fas fa-calculator" aria-hidden="true"></i>Converting</a>
</div>

## How Each Series Is Fitted {#how-each-series-is-fitted}

Each series is fitted in the form economists and actuaries normally use for it:

| Series | Fitted as | Why |
|:-------|:----------|:----|
| Interest rates, credit spreads, unemployment, dividend yield | The level, as a decimal | They mean-revert as levels ([Vasicek, 1977](<https://doi.org/10.1016/0304-405X(77)90016-2>)) |
| Inflation, house prices | Year-over-year change of the index, each reading regressed on the one a year earlier | The headline figure statistics offices publish, free of seasonality; neighbouring monthly or quarterly readings overlap, so they would overstate persistence |
| Equities, commodities, FX | Log returns of the price | Prices are not stationary, their returns are, and log returns add up over time |
| Dividends (Wilkie) | Log change of the dividend index | [Wilkie's (1986)](https://doi.org/10.1017/S0071368600009009) own specification |
| Leading indicator | Index points around 100 | It is built as a stationary cycle around 100 |
| Mortality | Logit of death rates | [Cairns, Blake and Dowd's (2006, eq. 1, p. 691)](https://www.pensions-institute.org/wp-content/uploads/2019/workingpapers/wp0611.pdf#page=6) specification |

A belief about inflation is stated the same way, as a year-over-year rate; [the inflation guide](/projects/financescenarios/docs/economy#inflation-calm-and-high-inflation-regimes) explains what that basis implies for the fit.

## How Results Read {#how-results-read}

A rate reads as itself. A price (an equity, commodity, exchange rate or portfolio value) reads by default as its **annualized return since the start**, the constant yearly return that takes today's value to the value at time $$t$$ (in years):

$$
R_t = \left(\frac{S_t}{S_0}\right)^{1/t} - 1
$$

An equity path from 769 to 1,209 over five years reads as 9.5% a year. This is the CAGR, as investment reports quote returns, and it puts a one-year and a thirty-year outcome on the same scale. Its spread narrows with the horizon as good and bad years average out, while the spread of the cumulative return keeps widening. Over the first months it is extremely wide, since a few weeks' move is scaled up to a year.

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">Not the expected return</p>

The mean of these annualized returns across scenarios is not the expected return: compounding is convex, so the expected value at the horizon is higher than today's value grown at that mean.
</div>

Every table and chart can show another reading instead:

| Reading | A price | Inflation | A rate |
|:--------|:--------|:----------|:-------|
| Default | annualized return since start | the rate | the rate |
| `level` | the price | a price index, 100 at start | the rate |
| `change` | % change over one step | % change of the index over one step | change over one step |
| `yoy` | % change over one year | % change of the index over one year | change over one year |
| `cumulative` | % change since start | % change of the index since start | change since start |
| `annualized` | yearly return since start | average yearly growth since start | not available |

<div class="fs-callout" markdown="1">
A change of a rate is a **difference** in its own units: 0.005 is half a percentage point (50 basis points), not a percentage of a percentage.
</div>

Choosing the reading in code:

```python
result.describe()                                         # each factor's default reading
result.describe(metric="cumulative")                      # change since start
result.plot("united_states_inflation", metric="level")    # inflation as a price index from 100
result.to_dataframe("us_broad", levels=True)              # the simulated prices themselves
```

## Converting {#converting}

With $$R$$ the annualized return over $$t$$ years, $$C$$ the cumulative return and $$r$$ the log return per year:

$$
1 + C = (1 + R)^t, \qquad r = \ln(1 + R), \qquad R = e^{r} - 1
$$

So 9.5% a year for five years is a cumulative 57%, or a log return of 9.1% a year. Log returns add up over time and are what the models work in; simple returns are what a portfolio earns and reports. The gap grows with volatility: an asset with a 0% median log return still has a positive mean simple return, so the expected outcome sits above the median scenario.

A simulated inflation rate $$\pi_s$$ compounds into a price index as $$100\,e^{\int_0^t \pi_s\,ds}$$. A year-over-year rate measures inflation over the past twelve months, so an index built from it runs about half a year behind actual prices, and at 3% it compounds about 0.05 percentage points a year above simple growth. Both are small next to the spread of the scenarios.

