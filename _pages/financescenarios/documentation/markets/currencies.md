---
title: Currencies
seo_title: "Currencies | Finance Scenarios"
seo_title_suffix: false
excerpt: "How Finance Scenarios simulates exchange rates: the euro and the pound revert to purchasing power parity at a four-year half-life, the yen is a random walk, and a risk-neutral rate drifts at the interest-rate gap."
description: "Currencies in Finance Scenarios: purchasing power parity on the real exchange rate, the anchor's standard error, the random-walk yen, uncovered interest parity, Garman-Kohlhagen risk-neutral rates and a run."
author_profile: false
permalink: /projects/financescenarios/docs/markets/currencies
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/markets
redirect_from:
    - /projects/financescenarios/docs/reference/fx
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-markets"
---

Exchange rates turn foreign assets and liabilities into the reporting currency. Each currency is simulated against the US dollar, as the amount of it one dollar buys. Over a few years an exchange rate moves like a random walk, but over decades it is pulled back toward purchasing power parity: in the default model the euro and the pound revert to it at a four-year half-life, the yen is a random walk with no trend, and a risk-neutral exchange rate drifts at the gap between the two currencies' interest rates.

<div class="fs-facts">
  <div><span>Series</span><b>Each currency against the US dollar</b></div>
  <div><span>Data</span><b>BIS end-of-month rates, OECD consumer prices</b></div>
  <div><span>Default model</span><b>Purchasing power parity for the euro and the pound; a random walk for the yen</b></div>
</div>

## Purchasing Power Parity for the Euro and the Pound

Under purchasing power parity, a currency that buys much more abroad than it usually does loses that edge over time. The studies [Rogoff (1996, section 5.B, p. 656)](https://ideas.repec.org/a/aea/jeclit/v34y1996i2p647-668.html){:target="_blank"} surveys agree on a half-life of three to five years for real exchange rates, and cross-country panels find about four (section 5.C, p. 657). The default takes four years.

The real exchange rate is the nominal rate (foreign currency per US dollar) adjusted for the two price levels, $$q_t = \ln S_t - \ln(P^f_t / P^{us}_t)$$. It reverts to its average since 2000 at $$\kappa = \ln 2 / 4 = 0.173$$ a year, and the nominal rate also moves with the two simulated inflation rates:

$$
q_{t+\Delta t} = \bar q + (q_t - \bar q)\,e^{-\kappa\Delta t} + \sigma\sqrt{\frac{1 - e^{-2\kappa\Delta t}}{2\kappa}}\;z_t, \qquad S_{t+\Delta t} = S_t \exp\!\left(\left[\ln(1 + \pi^f_t) - \ln(1 + \pi^{us}_t)\right]\Delta t + q_{t+\Delta t} - q_t\right)
$$

Inflation is a rate over a year, so a price index grows by $$\ln(1 + \pi)$$ a year, the log change that [Ahlgrim, D'Arcy and Gorvett (2005, section 3, eq. 3.7)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"} model: the two price levels in $$q_t$$ move the way the simulated price indices do.

The volatility $$\sigma$$ is that of the nominal rate's monthly changes since 2000: the short-run volatility of real exchange rates is of the same order as that of nominal ones (Rogoff, 1996, section 1, p. 647). The rates are the Bank for International Settlements' end-of-month rates ([BIS](https://data.bis.org/topics/XRU){:target="_blank"}), not monthly averages, whose changes would keep only about two thirds of a random walk's variance ([Working, 1960](https://doi.org/10.2307/1907574){:target="_blank"}). The price indices are the OECD's consumer price indices of the United States, Germany (for the euro, as the euro area's inflation series) and the United Kingdom.

The chart shows the euro and pound real exchange rates since 2000 against their average, with the expected pull back at a four-year half-life:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/markets/fx-ppp" alt="The euro and pound real exchange rates since 2000 against their average, with the expected pull back at a four-year half-life" %}

Today, in real terms, the dollar buys more than its average since 2000:

<div class="ca-nums fs-nums">
  <span><b>11%</b>more euros</span>
  <span><b>10%</b>more pounds</span>
</div>

The median scenario has the dollar losing half of that edge in four years.

How sure is the anchor? For a process that reverts at speed $$\kappa$$, the average of $$T$$ years has a standard error of about $$\sigma / (\kappa\sqrt{T})$$: 0.104 for the euro and 0.096 for the pound over 27 years, as large as today's distance from the anchor. Today's level lies about one standard error from the historical average, so the data alone cannot tell the two apart. The anchor stays on the historical average, where the parity literature [Rogoff (1996)](https://ideas.repec.org/a/aea/jeclit/v34y1996i2p647-668.html){:target="_blank"} surveys measures it. Anchoring on today's level instead (the `today` option) turns the pull off and leaves a random walk around today's level; on year-end backtests from 2000 to 2022 doing so lowers the euro's four-year CRPS skill (how much its scenarios improve on a forecast of no change) from +0.39 to +0.30.

## No Trend for the Yen

The default factor set has no Japanese inflation series to measure the yen's real rate against, so the yen is a random walk with no trend. Its log drift is zero (a drift of $$\sigma^2/2$$ in $$dS/S$$), which keeps the median at today's rate. A random walk forecasts exchange rates at least as well as structural models ([Meese and Rogoff, 1983, section 4, Table 1, p. 13](https://doi.org/10.1016/0022-1996(83)90017-X){:target="_blank"}), and a fitted trend would carry a currency view forward for decades.

Other drifts are options: the sample's own trend, or uncovered interest-rate parity, $$d\ln S_t = (r^f_t - r^{us}_t - \tfrac{1}{2}\sigma^2)\,dt + \sigma\,dW_t$$, which [Fama (1984, Table 2, p. 326)](https://doi.org/10.1016/0304-3932(84)90046-1){:target="_blank"} finds history does not support. That drift gives an investor who counts in euros the same expected return in either currency; one who counts in dollars expects $$\sigma^2$$ a year more, since the expected rate and the expected value of its inverse cannot both grow at the rate gap ([Siegel, 1972](https://doi.org/10.2307/1880565){:target="_blank"}).

## How Each Number Is Set

Every number in the currency model, and where it comes from:

| Number | Value | Kind | Why |
|:--|:--|:--|:--|
| Half-life of the real rate | 4 years | Sourced | [Rogoff (1996, sections 5.B and 5.C, pp. 656-657)](https://ideas.repec.org/a/aea/jeclit/v34y1996i2p647-668.html){:target="_blank"} |
| Anchor $$\bar q$$ | The average real rate since 2000 | Judgement | The calibration window; the anchor less today's real rate is -0.105 (euro) and -0.096 (pound) in logs |
| Volatility | Euro 9.3%, pound 8.6%, yen 9.3% a year | Fitted | End-of-month rates since 2000 |
| Yen | Random walk | Sourced | [Meese and Rogoff (1983, section 4, Table 1, p. 13)](https://doi.org/10.1016/0022-1996(83)90017-X){:target="_blank"} |

## Risk-Neutral Exchange Rates

For valuation, an exchange rate must drift so that a foreign deposit, converted into dollars and discounted at the US rate, is worth what it costs: values are measured in dollars, as for every other price in a valuation run. In [Garman and Kohlhagen (1983)](https://doi.org/10.1016/S0261-5606(83)80001-1){:target="_blank"} the dollar price of a unit of foreign currency, $$Y = 1/S$$, drifts at $$r^{us} - r^f$$. The model quotes $$S$$, foreign currency per dollar, and by Itô's lemma $$S = 1/Y$$ then drifts at the gap the other way plus the variance:

$$
\frac{dS_t}{S_t} = \left(r^f_t - r^{us}_t + \sigma^2\right)dt + \sigma\,dW_t
$$

with both rates the simulated ones at the start of each step when both are simulated, and today's otherwise. Leaving out the $$\sigma^2$$, as a drift of $$r^f - r^{us}$$ does, is risk-neutral for an investor who counts in euros, not in dollars, and overstates the dollar value of foreign holdings by $$e^{\sigma^2 T}$$: about 9% at 10 years at the euro's 9.3% volatility. As a check, a 10-year euro deposit, converted to dollars and discounted at the simulated US rate, has a mean value of 1.

## Example

The example uses the run from the [overview](/projects/financescenarios/docs#simulating-scenarios): the default settings and factor set, calibrated on 25 October 2026, with 2,000 scenarios and seed 42. To simulate it and read the euro's fitted parameters:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
calibration = scenarios.calibrate()
result = scenarios.simulate(calibration=calibration, n_simulations=2000, seed=42)

calibration.calibrated_params["eur"]
```

Which gives a speed of 0.173 a year (ln 2 over four years), a volatility of 9.3% a year and a `long_run_deviation` of -0.105, the average real exchange rate since 2000 less today's in logs: in real terms the dollar buys about 11% more euros than usual. A dollar buys 0.8807 euros, 0.7526 pounds and 157.0 yen at the start. After five years the median scenario has it buying 0.8146 euros and 0.7133 pounds, as the dollar loses part of that edge, and still 156.8 yen. When plotted as exchange-rate levels, one currency per tab:

{% include ft-chart.html id="markets-fx" src="/assets/data/financescenarios-guides/markets.json" label="Median, 25-75% and 5-95% band of the number of euros, pounds and yen one US dollar buys over five years" %}

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">8</span></summary>

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. [casact.org](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}
- Bank for International Settlements. Exchange rates (XRU). [data.bis.org](https://data.bis.org/topics/XRU){:target="_blank"}
- Fama, E.F. (1984). "Forward and Spot Exchange Rates." Journal of Monetary Economics, 14(3), 319-338. [doi.org](https://doi.org/10.1016/0304-3932(84)90046-1){:target="_blank"}
- Garman, M.B., Kohlhagen, S.W. (1983). "Foreign Currency Option Values." Journal of International Money and Finance, 2(3), 231-237. [doi.org](https://doi.org/10.1016/S0261-5606(83)80001-1){:target="_blank"}
- Meese, R.A., Rogoff, K. (1983). "Empirical Exchange Rate Models of the Seventies: Do They Fit Out of Sample?" Journal of International Economics, 14(1-2), 3-24. [doi.org](https://doi.org/10.1016/0022-1996(83)90017-X){:target="_blank"}
- Rogoff, K. (1996). "The Purchasing Power Parity Puzzle." Journal of Economic Literature, 34(2), 647-668. [ideas.repec.org](https://ideas.repec.org/a/aea/jeclit/v34y1996i2p647-668.html){:target="_blank"}
- Siegel, J.J. (1972). "Risk, Interest Rates and the Forward Exchange." Quarterly Journal of Economics, 86(2), 303-309. [doi.org](https://doi.org/10.2307/1880565){:target="_blank"}
- Working, H. (1960). "Note on the Correlation of First Differences of Averages in a Random Chain." Econometrica, 28(4), 916-918. [doi.org](https://doi.org/10.2307/1907574){:target="_blank"}

</details>

{% include ft-charts-script.html %}
