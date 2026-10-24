---
title: Units
seo_title: "Units | Finance Scenarios"
seo_title_suffix: false
excerpt: "How every number in Finance Scenarios reads: one scale of annualized decimals, each series fitted in its natural form, and the readings and conversions between annualized, cumulative and log returns."
description: "Units in Finance Scenarios: annualized decimals, how each series is fitted, how results read as rates and annualized returns since the start, the other readings, and conversions between them."
author_profile: false
permalink: /projects/financescenarios/docs/units
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/architecture
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-architecture"
---

Every number is on one scale: an **annualized decimal**.

<div class="ca-nums fs-nums">
  <span><b>0.035</b>a short rate of 3.5% a year</span>
  <span><b>0.026</b>inflation of 2.6% a year</span>
  <span><b>0.095</b>an equity return of 9.5% a year</span>
</div>

A fitted parameter, a belief you set, a regime target and a simulated value can be compared directly, whatever the data frequency or the step of the run. This page sets out how each series is fitted, how results read and how to convert between annualized, cumulative and log returns.

## How Each Series Is Fitted {#how-each-series-is-fitted}

Each series is fitted in the form economists and actuaries normally use for it:

| Series | Fitted as | Why |
|:-------|:----------|:----|
| Interest rates, unemployment | The level, as a decimal | They mean-revert as levels ([Vasicek, 1977](https://doi.org/10.1016/0304-405x(77)90016-2){:target="_blank"}) |
| Credit spreads, dividend yields | The log of the level | Their swings scale with their level, and they stay positive |
| Inflation, house prices | Year-over-year change of the index, each reading regressed on the one a year earlier | The headline figure statistics offices publish, free of seasonality; neighboring monthly or quarterly readings overlap, so they would overstate persistence |
| Equities, commodities, FX | Log returns of the price | Prices are not stationary, their returns are, and log returns add up over time |
| Dividends (Wilkie) | Log change of the dividend index | [Wilkie's (1986)](https://doi.org/10.1017/S0071368600009009){:target="_blank"} own specification |
| Leading indicator | Index points around 100 | It is built as a stationary cycle around 100 |
| Mortality | Logit of death rates | [Cairns, Blake and Dowd's (2006, eq. 1, p. 691)](https://www.pensions-institute.org/wp-content/uploads/2019/workingpapers/wp0611.pdf#page=6){:target="_blank"} specification |

A belief about inflation is stated the same way, as a year-over-year rate; [Inflation](/projects/financescenarios/docs/economy#the-model) explains what that basis implies for the fit.

## How Results Read {#how-results-read}

A rate reads as itself. A price (an equity, commodity, exchange rate or portfolio value) reads by default as its **annualized return since the start**, the constant yearly return that takes today's value to the value at time $$t$$ (in years):

$$
R_t = \left(\frac{S_t}{S_0}\right)^{1/t} - 1
$$

An equity path from 763 to 1,209 over five years reads as 9.6% a year. This is the CAGR (compound annual growth rate), the way investment reports quote returns, and it puts a one-year and a thirty-year outcome on the same scale. Its spread narrows with the horizon as good and bad years average out, while the spread of the cumulative return keeps widening. Over the first months it is extremely wide, since a few weeks' move is scaled up to a year.

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

## Converting {#converting}

With $$R$$ the annualized return over $$t$$ years, $$C$$ the cumulative return and $$r$$ the log return per year:

$$
1 + C = (1 + R)^t, \qquad r = \ln(1 + R), \qquad R = e^{r} - 1
$$

So 9.6% a year for five years is a cumulative 58%, or a log return of 9.2% a year. Log returns add up over time and are what the models work in; simple returns are what a portfolio earns and reports. The gap grows with volatility: an asset with a 0% median log return still has a positive mean simple return, so the expected outcome sits above the median scenario.

A simulated inflation rate $$\pi_t$$, a year-over-year rate, compounds into a price index as $$I_t = 100\exp\big(\sum_{s<t}\ln(1 + \pi_s)\,\Delta t\big)$$, so a constant 3% gives exactly $$100 \times 1.03^t$$ ([Simulation Engine](/projects/financescenarios/docs/simulation-engine#price-indices)). A year-over-year rate measures inflation over the past twelve months, so an index built from it runs about half a year behind actual prices, a lag that is small next to the spread of the scenarios.

## Example

The example uses the run from the [overview](/projects/financescenarios/docs#simulating-scenarios): the default settings and factor set, calibrated on 19 October 2026, with 2,000 scenarios and seed 42. `describe` reads every factor in its default reading, and `metric` picks another for all of them. To read US stocks, gold, US inflation and the US short rate three ways:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
result = scenarios.simulate(n_simulations=2000, seed=42)

result.describe()                    # each factor's default reading
result.describe(metric="cumulative")  # the change since the start
result.describe(metric="level")       # the price, an inflation index from 100, the rate
```

Which gives, for the mean after five years:

| factor | default | cumulative | level |
|:-------|--------:|-----------:|------:|
| us_broad | 0.0849 (annualized) | 0.5844 | 1,209.31 (from 763.25) |
| gold | 0.0308 (annualized) | 0.2405 | 5,188.71 (from 4,182.60) |
| united_states_inflation | 0.0234 (rate) | 0.1426 | 114.26 (from 100) |
| united_states_short_rate | 0.0459 (rate) | 0.0051 | 0.0459 |

The cumulative and level readings agree (763.25 times 1.5844 is 1,209.31), while the annualized mean of 8.49% sits below the 9.6% a year that takes 763.25 to the mean price: compounding is convex, so the average of the yearly rates is below the rate of the average outcome. A rate's cumulative reading is its change since the start, 0.51 percentage points for the short rate, not a percentage of it.

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">3</span></summary>

- Cairns, A.J.G., Blake, D., Dowd, K. (2006). "A Two-Factor Model for Stochastic Mortality with Parameter Uncertainty: Theory and Calibration." Pensions Institute Discussion Paper PI-0611. [pensions-institute.org](https://www.pensions-institute.org/wp-content/uploads/2019/workingpapers/wp0611.pdf){:target="_blank"}
- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. [doi.org](https://doi.org/10.1016/0304-405x(77)90016-2){:target="_blank"}
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. [doi.org](https://doi.org/10.1017/S0071368600009009){:target="_blank"}

</details>
