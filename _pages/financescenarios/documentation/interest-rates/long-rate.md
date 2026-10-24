---
title: Long Rate
seo_title: "Long Rate | Finance Scenarios"
seo_title_suffix: false
excerpt: "How Finance Scenarios builds the 10-year rate: the short rate expected over the bond's life plus a term premium that reverts, moves with the short rate's gap and answers its change, fitted on OECD rates since 1950."
description: "The long rate of Finance Scenarios: the expectations hypothesis and Vasicek's weight, a bias-corrected speed, the term premium regression, the simulation and the slope of the curve in a run."
author_profile: false
permalink: /projects/financescenarios/docs/interest-rates/long-rate
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/interest-rates
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-interest-rates"
---

Two rates that each revert on their own, linked only by correlated shocks, let the gap between them wander: a simulated curve can invert at random and stay inverted for decades. The default model instead builds each currency's 10-year rate on its [short rate](/projects/financescenarios/docs/interest-rates): the short rate expected over the bond's life plus a term premium. The curve then inverts when the short rate jumps and steepens again as it falls back, as it has done historically.

<div class="fs-facts">
  <div><span>Series</span><b>The 10-year rate of each currency</b></div>
  <div><span>Fitted on</span><b>OECD 10-year and 3-month rates, yearly 1950-2025</b></div>
  <div><span>Default model</span><b>Expected short-rate path plus a term premium</b></div>
</div>

## The Expected Path

Under the expectations hypothesis, a long yield is the short rate expected over the bond's life, plus a term premium for holding the longer bond ([Campbell and Shiller, 1991, section 2, eq. 1](https://doi.org/10.2307/2298008){:target="_blank"}). If the short rate's gap to its long-run level $$\theta$$ fades at speed $$a$$, the average expected short rate over $$n$$ years is a weighted mix of today's rate and that level, with the same weight as in the yield of [Vasicek (1977, section 5, eq. 25)](https://doi.org/10.1016/0304-405x(77)90016-2){:target="_blank"}:

$$
\text{EP}_t = D\,r_t + (1 - D)\,\theta, \qquad D = \frac{1 - e^{-a n}}{a n}, \qquad n = 10
$$

$$D$$ is the share of a short-rate move a 10-year yield carries. In the fit, $$\theta$$ is the rule's steady state ($$r^* + \pi^*$$). In a run on the [market's path](/projects/financescenarios/docs/interest-rates/expected-path), $$\text{EP}_t$$ averages that path over the bond's life and adds the share of today's gap to it that is still expected: $$\text{EP}_t = \bar m_t + D\,(r_t - m_t)$$.

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">Two different speeds</p>

The speed $$a$$ in $$D$$ is the short rate's own persistence, not the rule's 0.65. The rule's speed is how fast the rate closes its gap to a target that inflation and unemployment keep moving; how long a gap in the short rate itself lasts, which is what bond markets price, depends on how persistent those drivers are.
</div>

The speed is fitted as a mean-reverting (Hull-White) process on each country's OECD 3-month rate, yearly from 1950 to 2025. A least-squares speed is biased upward in a sample of any realistic length: by $$B_1/T$$ a year for $$T$$ years of data, with $$B_1 = \tfrac{5}{2} + e^{a\Delta t} + \tfrac{1}{2}e^{2a\Delta t}$$, about 4.2 to 4.5 on yearly data ([Tang and Chen, 2009, Theorem 3.1.1](https://doi.org/10.1016/j.jeconom.2008.11.001){:target="_blank"}). That bias is taken off (the correction is set out on [Commodities](/projects/financescenarios/docs/markets/commodities#correcting-the-speed-for-a-short-sample)), so the plain fits of 0.114 a year for the US, 0.192 for Germany and 0.099 for the UK become 0.057, 0.133 and 0.043. A 10-year yield then carries 0.76, 0.55 and 0.81 of a short-rate move, against 0.60, 0.44 and 0.63 at the plain speeds. The rule's 0.65 would give 0.15.

An outside check: the New York Fed's expected average short rate over ten years, the risk-neutral yield of [Adrian, Crump and Moench (2013, section 2.4)](https://doi.org/10.1016/j.jfineco.2013.04.009){:target="_blank"} (series ACMRNY10, [Federal Reserve Bank of New York, Treasury Term Premia](https://www.newyorkfed.org/research/data_indicators/term-premia-tabs){:target="_blank"}), moves 0.59 for every point the 3-month bill moves, monthly from June 1961 to September 2026. The plain US weight of 0.60 is close to it; the corrected 0.76 is higher, so in the model a short-rate move lasts longer in the 10-year yield than in the New York Fed's estimate, and the same-step response below takes part of it back. The chart sets the weight against the short rate's speed, with each country's fitted speed before and after the correction:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/expected-path-weight" alt="The weight of today's short rate in the 10-year expected path against the short rate's speed, with each country's fitted speed before and after the bias correction and the New York Fed's estimate" %}

## The Term Premium

What is left of the long rate after the expected path is the term premium, $$\text{TP}_t = L_t - \text{EP}_t$$. It reverts toward a long-run level, moves with the short rate's gap to its own level, and responds to the short rate's change in the same step:

$$
\text{TP}_{t+1} = c + \phi\,\text{TP}_t + \psi\,(r_t - \theta) + \gamma\,(r_{t+1} - r_t) + e_{t+1}
$$

One least-squares regression on each country's OECD 10-year and 3-month rates, yearly from 1950 to 2025, gives every parameter: the speed $$\kappa = -\ln\phi$$ a year (the data are yearly), the long-run premium $$\tau = c/(1-\phi)$$ (the premium when the short rate sits at its level), the sensitivity to the short rate's gap $$\beta = \psi/(1-\phi)$$, the same-step response $$\gamma$$ and the volatility $$\sigma$$ of the residual, scaled to a yearly Ornstein-Uhlenbeck volatility. This yearly premium is the one the 10-year rate simulates; the month-end premia of the [expected path](/projects/financescenarios/docs/interest-rates/expected-path) are what is taken out of today's curve.

| Parameter | United States | Germany (euro) | United Kingdom | Kind |
|:--|--:|--:|--:|:--|
| Expected-path speed $$a$$, per year | 0.057 | 0.133 | 0.043 | Fitted, OECD 3-month rate 1950-2025, less Tang and Chen's bias |
| Weight $$D$$ (10 years) | 0.76 | 0.55 | 0.81 | Derived from $$a$$ |
| Long-run premium $$\tau$$ | 1.34% | 0.94% | 1.03% | Fitted |
| Sensitivity to the short rate's gap $$\beta$$ | 0.25 | 0.48 | 0.09 | Fitted |
| Same-step response $$\gamma$$ | -0.27 | -0.19 | -0.43 | Fitted |
| Premium's speed $$\kappa$$, per year | 0.36 | 0.22 | 0.18 | Fitted |
| Premium's volatility $$\sigma$$ | 0.60% | 0.63% | 0.80% | Fitted |
| Years in the fit | 76 | 76 | 76 | |

Historically, the premium was largest from the mid-1970s to the early 1990s, when holding a long bond meant carrying inflation risk, and near or below zero around 2020; Germany's was also large in the 1950s and 1960s. Each premium averages more than its $$\tau$$ (1.52%, 2.09% and 1.26%) because the short rate averaged above the rule's steady state over these years, and $$\beta$$ adds to the premium when it does. The chart splits each country's 10-year yield into the expected path and the premium:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/long-rate-decomposition" alt="OECD 10-year and 3-month rates since 1950 with the expected-path component and the term premium for the US, Germany and the UK" %}

The US premium can be set against the New York Fed's ACM term premium (after Adrian, Crump and Moench), which comes from a five-factor no-arbitrage model of the whole Treasury curve rather than from two rates. Over 1962-2025 the two correlate 0.92 in yearly averages. Ours averages 1.66% against ACM's 1.45%; the fitted long-run premium $$\tau$$ is 1.34%. The same-step response is larger than ACM's: their premium falls 0.12 for every point the 3-month bill rises (yearly-average changes, 1962-2025), against a $$\gamma$$ of -0.27 here. That offsets most of the larger weight $$D$$: a short-rate jump still lifts the 10-year by $$D + \gamma = 0.49$$ at once. The chart sets the two US premia side by side:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/term-premium-acm" alt="The fitted US 10-year term premium against the New York Fed's ACM term premium, yearly 1962-2025" %}

## In the Simulation

Each month the premium moves toward its target $$\tau + \beta\,(r_t - \theta)$$ at speed $$\kappa$$, takes $$\gamma$$ of the short rate's change and a shock of its own; the long rate is the expected path plus the premium:

$$
\text{TP}_{t+\Delta t} = \text{TP}^*_t + (\text{TP}_t - \text{TP}^*_t)\,e^{-\kappa\Delta t} + \gamma\,(r_{t+\Delta t} - r_t) + \sigma\sqrt{\tfrac{1 - e^{-2\kappa\Delta t}}{2\kappa}}\;z_t, \qquad L_{t+\Delta t} = \text{EP}_{t+\Delta t} + \text{TP}_{t+\Delta t}
$$

A 1-point jump in the short rate therefore lifts the 10-year at once by $$D + \gamma$$, and then by more or less as the premium follows the short rate's gap and the gap fades at the rule's speed. With every shock set to zero, the US 10-year rises:

<div class="ca-nums fs-nums">
  <span><b>0.49 pp</b>in the first month</span>
  <span><b>0.38 pp</b>after a year</span>
  <span><b>0.21 pp</b>after three years</span>
</div>

The same response for the US, Germany and the UK:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/shock-response" alt="The response of the 10-year yield to a 1-point jump in the short rate for the US, Germany and the UK" %}

## Data Choices

Which data the long rate is fitted on, and why:

| Choice | Kind | Why |
|:--|:--|:--|
| The term premium and the expected-path speed are fitted on the OECD's yearly rates since 1950 | Judgement | Seventy-six years hold the high-inflation decades, the low-rate 2010s and the 2022 rise; a window since 2000 holds one rate cycle |

## Examples

The examples on this page use the run from the [overview](/projects/financescenarios/docs#simulating-scenarios): the default settings and factor set, calibrated on 19 October 2026, with 2,000 scenarios and seed 42.

### The Long Rates

The default factor set has a 10-year government rate for the US, the euro area (Germany's) and the UK. To simulate them and read them off after five years:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
result = scenarios.simulate(n_simulations=2000, seed=42)

result.describe()
```

Which gives, for the three long rates:

| factor | initial | terminal_mean | terminal_q05 | terminal_q95 |
|:-------|--------:|--------------:|-------------:|-------------:|
| united_states_long_rate | 0.0511 | 0.0579 | 0.0180 | 0.1072 |
| eurozone_long_rate | 0.0347 | 0.0416 | 0.0123 | 0.0786 |
| united_kingdom_long_rate | 0.0524 | 0.0481 | 0.0176 | 0.0821 |

The long rates move less than the short rates, as each is the short rate expected over ten years plus a premium: nine US scenarios in ten end between 1.80% and 10.72%, against 0% and 10.99% for the short rate. When plotted, the long rates:

{% include ft-chart.html id="interest-rates-long" src="/assets/data/financescenarios-guides/interest-rates.json" label="Median and 5-95% band of the 10-year rate of the US, the euro area and the UK over five years" %}

### What the Long Rate Reads

The 10-year rate's own parameters hold its term premium and how much of a short-rate move it carries. To read them for the US:

```python
calibration = scenarios.calibrate()

calibration.calibrated_params["united_states_long_rate"]

calibration.calibration_notes["united_states_long_rate"]
```

Which gives a long-run term premium of 1.34% for the US (0.94% for the euro area and 1.03% for the UK), and a weight of 0.76 on today's short rate in the expected path (0.55 and 0.81), from how fast each country's short rate has reverted since 1950.

### The Slope of the Curve

The paths of a run are plain arrays, one row per scenario and one column per date, so anything built from two variables is one line away. The slope of the curve is the 10-year rate minus the short rate, and a negative slope is an inverted curve. To compute it and the share of scenarios in which the curve is inverted at each date:

```python
countries = {"US": "united_states", "Euro area": "eurozone", "UK": "united_kingdom"}

spread = {
    name: result.paths[f"{country}_long_rate"] - result.paths[f"{country}_short_rate"]
    for name, country in countries.items()
}
inverted = {name: (paths < 0).mean(axis=0) for name, paths in spread.items()}
```

Every curve starts upward sloping, by 1.03 percentage points in the US, 0.83 in the euro area and 1.25 in the UK, and the median US slope is still 1.26 points after five years. When plotted, the slopes:

{% include ft-chart.html id="interest-rates-spread" src="/assets/data/financescenarios-guides/interest-rates.json" label="Median and 5-95% band of the 10-year rate minus the short rate of the US, the euro area and the UK over five years" %}

The share of inverted curves follows the market's expected path. The Bank of England's curve prices UK short rates rising to 4.95% within a year, so after one year 58% of the UK scenarios have an inverted curve, against 37% in the euro area and 10% in the US; after five years it is 31%, 31% and 15%. When plotted, the share of inverted curves:

{% include ft-chart.html id="interest-rates-inversion" src="/assets/data/financescenarios-guides/interest-rates.json" label="Share of the 2,000 scenarios in which the 10-year rate is below the short rate, for the US, the euro area and the UK" %}

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">5</span></summary>

- Adrian, T., Crump, R.K., Moench, E. (2013). "Pricing the Term Structure with Linear Regressions." Journal of Financial Economics, 110(1), 110-138. [doi.org](https://doi.org/10.1016/j.jfineco.2013.04.009){:target="_blank"}
- Campbell, J.Y., Shiller, R.J. (1991). "Yield Spreads and Interest Rate Movements: A Bird's Eye View." The Review of Economic Studies, 58(3), 495-514. [doi.org](https://doi.org/10.2307/2298008){:target="_blank"}
- Federal Reserve Bank of New York (2026). Treasury Term Premia (ACMTP10, ACMRNY10). [newyorkfed.org](https://www.newyorkfed.org/research/data_indicators/term-premia-tabs){:target="_blank"}
- Tang, C.Y., Chen, S.X. (2009). "Parameter Estimation and Bias Correction for Diffusion Processes." Journal of Econometrics, 149(1), 65-81. [doi.org](https://doi.org/10.1016/j.jeconom.2008.11.001){:target="_blank"}
- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. [doi.org](https://doi.org/10.1016/0304-405x(77)90016-2){:target="_blank"}

</details>

{% include ft-charts-script.html %}
