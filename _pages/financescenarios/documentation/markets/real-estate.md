---
title: Real Estate
seo_title: "Real Estate | Finance Scenarios"
seo_title_suffix: false
excerpt: "How Finance Scenarios simulates house prices: growth that reverts to a long-run rate and slows a year after the long rate rises, with calm and turbulent volatility regimes as an option."
description: "Real estate in Finance Scenarios: mean-reverting house-price growth after Ahlgrim, D'Arcy and Gorvett, the lagged long-rate link, Crawford and Fratantoni's volatility regimes with a bootstrap test, and a run."
author_profile: false
permalink: /projects/financescenarios/docs/markets/real-estate
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/markets
redirect_from:
    - /projects/financescenarios/docs/reference/real-estate
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-markets"
---

House-price growth, not the price level, reverts to a long-run rate, as in eq. 3.18 of [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf#page=21){:target="_blank"}: a price index has no level to return to over decades, and booms fade in growth while leaving a mark on the level. In the default model, growth also responds to the long rate a year earlier. Higher rates make mortgages dearer and cool the housing market with a delay: [Iacoviello (2005, section I, Figure 1, p. 741)](https://doi.org/10.1257/0002828054201477){:target="_blank"} finds that tighter money lowers real house prices in US data from 1974 to 2003. Calm and turbulent volatility regimes are an option.

<div class="fs-facts">
  <div><span>Series</span><b>US house-price growth over the past year</b></div>
  <div><span>Data</span><b>OECD house prices and the OECD US 10-year rate</b></div>
  <div><span>Model</span><b>Mean-reverting growth, linked to the long rate a year earlier</b></div>
</div>

## Growth Linked to the Long Rate

Each step moves growth toward its long-run rate, then adds the long rate's change a year earlier and a shock of its own:

$$
g_{t+\Delta t} = \theta + (g_t - \theta)\,e^{-a\Delta t} + w\,\beta\,\Delta L_{t-\ell} + \sigma\sqrt{\frac{1 - e^{-2a\Delta t}}{2a}}\;z_t
$$

Here $$g_t$$ is US house-price growth over the past year (the OECD's nominal house price index), $$\Delta L_{t-\ell}$$ the simulated US long rate's change over the step that ended $$\ell$$ = 1 year earlier, and $$w$$ the weight that spreads the yearly sensitivity $$\beta$$ over the steps. Before the run starts the rate counts as unchanged, so the first year gets no push from it. The sensitivity is fitted on the longest record, from 1971: each quarter's growth regressed on its own value a year earlier and the long rate's change over the year ending a year earlier,

$$
g_t = c + Q\,g_{t-4} + \beta\,(L_{t-4} - L_{t-8}) + e_t
$$

which gives $$\beta$$ = -0.86: a 1-point rise in the long rate slows house-price growth by about 0.86 points a year later. Scanning the lag from 0 to 8 quarters, four explains the most (a partial R² of 8%), with three quarters close behind. The chart plots house-price growth against the long rate's change a year earlier, and the sensitivity at every lag from 0 to 8 quarters:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/markets/house-prices-rates" alt="US house-price growth against the long rate's change a year earlier with the fitted line, and the sensitivity at every lag from 0 to 8 quarters" %}

The path is price growth only; rental income is added when real estate is held as an asset (see [Portfolio](/projects/financescenarios/docs/portfolio#what-a-portfolio-can-hold)). The price index compounds the simulated growth as $$\ln(1 + g_t)$$ a year, the log change of eq. 3.7 of Ahlgrim, D'Arcy and Gorvett, so a steady 4% gives $$1.04^T$$.

## How Each Number Is Set

Every number in the house-price model, and where it comes from:

| Number | Value | Kind | Why |
|:--|:--|:--|:--|
| Lag | 4 quarters | Judgement | The lag that explains the most on US data since 1971 (chart) |
| Sensitivity $$\beta$$ | -0.86 (standard error 0.20) | Fitted | OECD house prices and the OECD US 10-year rate, 1973Q1-2026Q2 |
| Minimum sample | 80 quarters | Judgement | Twenty years of data before the link is fitted |
| Speed, long-run growth, volatility | 0.37 a year, 4.3%, 4.8% | Fitted | OECD US house prices since 2000, read a year apart; the volatility net of what the link explains, keeping at least half of it |

## Calm and Turbulent House Prices

House prices do not swing with one steady volatility: long quiet stretches alternate with booms and busts. The `regime_switching` volatility option lets the size of the shocks switch between a calm and a turbulent regime. It is fitted on quarter-on-quarter growth, the data [Crawford and Fratantoni (2003)](https://doi.org/10.1111/1540-6229.00064){:target="_blank"} fit their regimes on: an autoregression whose shock size alone follows a two-regime Markov chain, estimated by maximum likelihood through [Hamilton's (1989)](https://doi.org/10.2307/1912559){:target="_blank"} filter:

$$
x_t = \ln(1 + q_t) = c + \phi\,x_{t-1} + s_{k_t}\,e_t, \qquad e_t \sim N(0, 1), \qquad P(k_{t+1} = j \mid k_t = i) = p_{ij}
$$

with $$q_t$$ the growth over the quarter and $$k_t$$ the regime.

The fit uses quarterly growth, not growth over the past year read every quarter: each year-over-year reading shares three quarters with the one before, so its residuals are strongly autocorrelated, and two regimes then beat one even on data with a single constant volatility. On simulated samples of US length with no regimes at all, year-over-year growth read every quarter gives the two regimes a log-likelihood gain of about 57; quarterly growth gives one close to zero.

The regimes' shock sizes are then scaled so their long-run average variance is the growth process's own, and the switching chances are converted to the scenario's step. The option needs the OECD's long house-price record (`history_source: oecd`), so the speed and volatility then come from 1971 onward rather than the table above. Fitted on the OECD's US index, 1970 to 2026 (224 quarters):

| | Calm | Turbulent |
|:--|--:|--:|
| Shock size a quarter | 0.24% | 1.02% |
| Volatility in the scenarios, a year | 1.2% | 5.0% |
| Chance of staying, a quarter | 0.960 | 0.970 |
| Average spell | 6.2 years | 8.4 years |
| Long-run share | 42% | 58% |

The two regimes raise the log-likelihood by 61.3 over one constant volatility. A parametric bootstrap checks whether that could be chance: histories simulated from the constant-volatility autoregression fitted to the same data, each fitted both ways, give gains of a few points at most, so none comes near 61.3. The turbulent regime holds the 1970s and early 1980s, the early 1990s, the bust from 2006 to 2014 and the swings since 2020; today the index is in it. The chart shades the quarters in the turbulent regime:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/markets/house-price-regimes" alt="US quarter-on-quarter house-price growth since 1970 with the quarters in the turbulent regime shaded" %}

The default keeps one constant volatility, read a year apart with the rate link above; the regimes are an option for a run whose house prices should alternate between quiet stretches and booms and busts.

## Example

The example uses the run from the [overview](/projects/financescenarios/docs#simulating-scenarios): the default settings and factor set, calibrated on 25 October 2026, with 2,000 scenarios and seed 42. To simulate it and read the fitted parameters of US house-price growth and its range after one, three and five years:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
calibration = scenarios.calibrate()
result = scenarios.simulate(calibration=calibration, n_simulations=2000, seed=42)

calibration.calibrated_params["real_estate"]

result.horizon_summary([1, 3, 5], factors=["real_estate"])
```

Which gives a long-run growth of 4.29% a year, a speed of 0.37 a year and a sensitivity of -0.86 to the long rate's change a year earlier. Growth starts at 2.14%; its median rises to 2.83% after one year and 3.90% after five, when one scenario in twenty is below -5.11%. When plotted:

{% include ft-chart.html id="markets-real-estate" src="/assets/data/financescenarios-guides/markets.json" label="Median, 25-75% and 5-95% band of US house-price growth over five years" %}

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">4</span></summary>

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. [casact.org](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}
- Crawford, G.W., Fratantoni, M.C. (2003). "Assessing the Forecasting Performance of Regime-Switching, ARIMA and GARCH Models of House Prices." Real Estate Economics, 31(2), 223-243. [doi.org](https://doi.org/10.1111/1540-6229.00064){:target="_blank"}
- Hamilton, J.D. (1989). "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle." Econometrica, 57(2), 357-384. [doi.org](https://doi.org/10.2307/1912559){:target="_blank"}
- Iacoviello, M. (2005). "House Prices, Borrowing Constraints, and Monetary Policy in the Business Cycle." American Economic Review, 95(3), 739-764. [doi.org](https://doi.org/10.1257/0002828054201477){:target="_blank"}

</details>

{% include ft-charts-script.html %}
