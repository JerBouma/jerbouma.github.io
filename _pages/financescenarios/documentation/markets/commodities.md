---
title: Commodities
seo_title: "Commodities | Finance Scenarios"
seo_title_suffix: false
excerpt: "How Finance Scenarios simulates gold and oil: gold as a random walk in real terms, Brent pulled toward a level in the one-factor model of Schwartz, and a mean-reversion speed corrected for a short sample."
description: "Commodities in Finance Scenarios: gold's real random walk, Schwartz's mean-reverting log price for Brent, Tang and Chen's bias correction of the speed, the Schwartz-Smith two-factor option and a run."
author_profile: false
permalink: /projects/financescenarios/docs/markets/commodities
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/markets
redirect_from:
    - /projects/financescenarios/docs/reference/commodities
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-markets"
---

Commodities hedge inflation and drive it: oil prices pass into consumer prices, and gold is held for what it keeps when money does not. In the default model gold is a random walk in real terms, with no level its price returns to, and Brent crude is pulled toward a level set by the cost of production, with its speed of mean reversion corrected for the short sample it is fitted on. The two-factor model of Schwartz and Smith is the alternative.

<div class="fs-facts">
  <div><span>Gold</span><b>A random walk in real terms</b></div>
  <div><span>Brent</span><b>One-factor mean reversion in logs</b></div>
  <div><span>Alternative</span><b>Schwartz-Smith two factor</b></div>
</div>

## Gold: A Random Walk in Real Terms

Gold has no level its real price returns to. About 2,500 tonnes are mined a year, some 1.5% of the 171,300 tonnes above ground, so supply barely responds to price ([Erb and Harvey, 2013, pp. 28-29](https://doi.org/10.2469/faj.v69.n4.1){:target="_blank"}). The "golden constant", a long-run real return near zero, rests on centuries of data (p. 11), while the real price swings as much as the nominal one (p. 12), and a mean reversion fitted on a short sample rests on one episode (p. 15). A mean-reverting fit on gold futures since 2000 settles at about $24,000 an ounce with a 21-year half-life: no credible level.

The default therefore makes gold a random walk in real terms: it keeps pace with the simulated US price index, which grows by $$\ln(1 + \pi_t)$$ a year, and its log price has no other drift (a drift of $$\sigma^2/2$$ in $$dS/S$$), so its median real price stays flat:

$$
S_{t+\Delta t} = S_t \exp\!\left(\ln(1 + \pi_t)\,\Delta t + \sigma\sqrt{\Delta t}\,z_t\right)
$$

The volatility, 17.9% a year, comes from the daily gold futures price (GC=F) since 2000. The chart shows gold's price in today's US dollars an ounce since 1971:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/markets/gold-real" alt="Gold's price in today's US dollars an ounce since 1971" %}

## Brent: Pulled toward a Level

An oil price is pulled toward a level set by the cost of production: high prices bring new supply, low prices cut it. The log price follows the one-factor model of [Schwartz (1997)](https://doi.org/10.1111/j.1540-6261.1997.tb02721.x){:target="_blank"}, which keeps the price positive:

$$
dX_t = a(\theta - X_t)\,dt + \sigma\,dW_t, \qquad X_t = \ln S_t
$$

Fitted on daily Brent futures (BZ=F) since July 2007, the long-run median $$e^{\theta}$$ is $78 a barrel, a shock halves in 1.6 years, and the volatility is 38.3% a year. The model uses Brent rather than WTI because the WTI front-month future closed at -$37.63 on 20 April 2020, a price the log model cannot take. The chart shows Brent since 1990 with the fitted long-run median:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/markets/brent" alt="Brent crude since 1990 with the fitted long-run median" %}

## Correcting the Speed for a Short Sample

The speed comes from regressing each day's change in the log price on the previous day's level. That estimate is biased upward in any sample of realistic length: a series that wanders for a few years looks like it is being pulled back faster than it is. [Tang and Chen (2009, Theorem 3.1.1)](https://doi.org/10.1016/j.jeconom.2008.11.001){:target="_blank"} give the bias of the maximum-likelihood speed of an Ornstein-Uhlenbeck process whose level is estimated too, over $$T$$ years of steps $$\Delta t$$ apart:

$$
E(\hat a) - a \approx \frac{B_1}{T}, \qquad B_1 = \frac{5}{2} + e^{a\Delta t} + \frac{1}{2}e^{2a\Delta t}
$$

As the step shrinks $$B_1$$ tends to 4, so the bias is about $$4/T$$ a year whatever the frequency: twenty years of daily data add about 0.2 to the speed. The fit subtracts $$B_1/T$$, evaluated at the estimate, from the speed, and re-estimates the volatility at the corrected speed so that one step's spread stays the one the data show. Brent's 19 years of daily prices give a plain speed of 0.65 and a corrected one of 0.45: the half-life of a shock rises from 1.1 to 1.6 years.

The correction applies to every plain mean-reverting fit, among them the US Treasury curve's level, slope and curvature (from 0.35, 0.24 and 0.73 to 0.20, 0.09 and 0.58 a year). It does not apply to regressions with extra terms, to the fits read a year apart (house prices on [Real Estate](/projects/financescenarios/docs/markets/real-estate)) or to the Euler fits behind GARCH volatility, which the theorem does not cover. When the correction would remove all mean reversion, as it can on five years of data, the plain speed is kept with a warning: the sample cannot tell the series from a random walk.

The chart applies the plain and corrected estimators to simulated paths with a true speed of 0.46, about Brent's corrected 0.45, and shows the default's daily fits before and after the correction:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/markets/ou-speed-bias" alt="The average plain and corrected mean-reversion speed of simulated paths against the years of data, and the default's Brent and Treasury curve speeds before and after the correction" %}

At 20 years the plain estimate averages 0.68 against a true 0.46, and the corrected one 0.48. At five years the correction would leave no pull in many samples, which keep the plain speed, so the average stays above the truth.

## How Each Number Is Set

Every number in the commodity models, and where it comes from:

| Number | Value | Kind | Why |
|:--|:--|:--|:--|
| Gold model | Random walk in real terms | Sourced | [Erb and Harvey (2013, pp. 11-15, 28-29)](https://doi.org/10.2469/faj.v69.n4.1){:target="_blank"} |
| Gold volatility | 17.9% | Fitted | Daily GC=F since 2000 |
| Brent level, speed, volatility | $78, 0.45 a year, 38.3% | Fitted | Daily BZ=F since July 2007, [Schwartz (1997)](https://doi.org/10.1111/j.1540-6261.1997.tb02721.x){:target="_blank"}, speed corrected for the sample's length ([Tang and Chen, 2009](https://doi.org/10.1016/j.jeconom.2008.11.001){:target="_blank"}) |

## The Two-Factor Alternative

In the two-factor model of [Schwartz and Smith (2000)](https://doi.org/10.1287/mnsc.46.7.893.12034){:target="_blank"} the log price is a short-term deviation $$\chi$$ that fades plus a long-term level $$\xi$$ that drifts:

$$
\ln S_t = \chi_t + \xi_t, \qquad d\chi_t = -\kappa\,\chi_t\,dt + \sigma_\chi\,dW^\chi_t, \qquad d\xi_t = \mu_\xi\,dt + \sigma_\xi\,dW^\xi_t, \qquad dW^\chi_t\,dW^\xi_t = \rho\,dt
$$

Fitted on history, $$\xi$$ is the trailing three-year mean of the log price and $$\chi$$ the rest; $$\kappa$$ comes from a regression of $$\chi$$'s change on its level. Where a futures curve exists (WTI crude, natural gas, gold, silver, copper, corn, wheat and soybeans), the volatilities and $$\rho$$ are then refitted to the futures' realized volatilities, which fall with maturity as the short-term factor fades (section 3.1, from eq. 9):

$$
\sigma^2(F_T) = e^{-2\kappa T}\sigma_\chi^2 + \sigma_\xi^2 + 2e^{-\kappa T}\rho\,\sigma_\chi\sigma_\xi
$$

In a risk-neutral run the drifts are fitted to today's futures prices instead, through $$\ln F(0, T) = e^{-\kappa T}\chi_0 + \xi_0 - (1 - e^{-\kappa T})\lambda_\chi/\kappa + \mu^Q T + \tfrac{1}{2}V(T)$$, with $$\lambda_\chi$$ the short-term factor's risk premium, $$\mu^Q$$ the long-term level's risk-neutral drift and $$V(T)$$ the variance of $$\ln S_T$$. The run steps $$\chi$$ exactly and $$\xi$$ as a random walk, correlated through the run's correlation matrix. Brent has no futures curve here, so its two-factor fit rests on the spot price alone and has no risk-neutral version.

## Example

The example uses the run from the [overview](/projects/financescenarios/docs#simulating-scenarios): the default settings and factor set, calibrated on 25 October 2026, with 2,000 scenarios and seed 42. To simulate it and read the fitted parameters of gold and oil:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
calibration = scenarios.calibrate()
result = scenarios.simulate(calibration=calibration, n_simulations=2000, seed=42)

calibration.calibrated_params["gold"]

calibration.calibrated_params["crude_oil"]
```

Which gives gold a drift of 1.6% a year and a volatility of 17.9%, starting from $4,007.90 an ounce, and oil a long-run level of $77.50 a barrel (a log level of 4.350), a speed of 0.45 a year and a volatility of 38.3%, starting from $116.72. After five years the median gold price is $4,578.19, with a 90% range of $2,363.91 to $8,869.17, and the median oil price is $80.39, between $42.68 and $161.88. When plotted:

{% include ft-chart.html id="markets-commodities" src="/assets/data/financescenarios-guides/markets.json" label="Median, 25-75% and 5-95% band of the gold price in dollars an ounce and the crude oil price in dollars a barrel over five years" %}

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">4</span></summary>

- Erb, C.B., Harvey, C.R. (2013). "The Golden Dilemma." Financial Analysts Journal, 69(4), 10-42. [doi.org](https://doi.org/10.2469/faj.v69.n4.1){:target="_blank"}
- Schwartz, E., Smith, J.E. (2000). "Short-Term Variations and Long-Term Dynamics in Commodity Prices." Management Science, 46(7), 893-911. [doi.org](https://doi.org/10.1287/mnsc.46.7.893.12034){:target="_blank"}
- Schwartz, E.S. (1997). "The Stochastic Behavior of Commodity Prices: Implications for Valuation and Hedging." The Journal of Finance, 52(3), 923-973. [doi.org](https://doi.org/10.1111/j.1540-6261.1997.tb02721.x){:target="_blank"}
- Tang, C.Y., Chen, S.X. (2009). "Parameter Estimation and Bias Correction for Diffusion Processes." Journal of Econometrics, 149(1), 65-81. [doi.org](https://doi.org/10.1016/j.jeconom.2008.11.001){:target="_blank"}

</details>

{% include ft-charts-script.html %}
