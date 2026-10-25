---
title: Unemployment
seo_title: "Unemployment | Finance Scenarios"
seo_title_suffix: false
excerpt: "How Finance Scenarios simulates unemployment: expansions and recessions after Hamilton, a recession likelier after a stock-market fall, and a calm level anchored to the official longer-run rate."
description: "Unemployment in Finance Scenarios: Hamilton's regime-switching regression with a Phillips-curve term, time-varying recession chances on the stock market, the plucking-model anchor, the euro area's mean reversion and a run."
author_profile: false
permalink: /projects/financescenarios/docs/economy/unemployment
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/economy
redirect_from:
    - /projects/financescenarios/docs/reference/unemployment
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-economy"
---

Unemployment drives wage-linked benefits, disability claims and credit losses. It does not move like one bell curve of shocks around a trend: it rises fast in recessions and falls slowly in expansions, an asymmetry [Neftçi (1984)](https://doi.org/10.1086/261226){:target="_blank"} and [Sichel (1993)](https://doi.org/10.1111/j.1465-7295.1993.tb00879.x){:target="_blank"} document for the US rate. A model with one normal shock, fitted to the average month, gives a rise like 2008-09's (five points in two years) almost no chance: fitted from 2000 to 2007, its 90% band reached only 6.1% by 2009, when the US rate hit 9.9%. In the default model US and UK unemployment therefore switch between expansion and recession regimes, a US recession is likelier after a stock-market fall, and each country's calm level is anchored to the official longer-run rate.

<div class="fs-facts">
  <div><span>Series</span><b>Unemployment rate per country</b></div>
  <div><span>Data</span><b>OECD, monthly (US from 1956, UK from 1971)</b></div>
  <div><span>Default model</span><b>Expansion and recession regimes</b></div>
</div>

## The Model (United States and United Kingdom)

Following [Hamilton (1989, section 2, eq. 2.1-2.2)](https://doi.org/10.2307/1912559){:target="_blank"}, who presents his model as an extension of Neftçi's states of rising and falling unemployment (p. 359), each month's change in unemployment is a regression whose intercept and noise depend on an unobserved regime, expansion or recession:

$$
\Delta u_t = c_{s_t} + b\,u_{t-1} + \alpha\,\Delta\pi_t + \sigma_{s_t}\,\varepsilon_t
$$

Here $$s_t$$ is the regime and $$\pi_t$$ inflation. The regression keeps the pull back to a calm level ($$b < 0$$) and the Phillips-curve term $$\alpha\,\Delta\pi_t$$ of [Ahlgrim, D'Arcy and Gorvett (2005, eq. 3.21)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}, which ties unemployment to changes in inflation. The speed of the pull is $$\kappa = -12\ln(1+b)$$ a year and the calm level $$\mu_{\text{calm}} = c_{\text{expansion}}/(-b)$$. In a recession the intercept is higher, so unemployment is pushed up by $$D_r = (c_{\text{recession}} - c_{\text{expansion}})\,\kappa/(-b)$$ a year, about twelve times the monthly gap, on top of its pull back. The long-run average therefore lies above the calm level by the recessions' average push:

$$
\mu = \mu_{\text{calm}} + \frac{D_r\,w_r}{\kappa}
$$

with $$w_r$$ the long-run share of months in recession. The chance of staying in a recession is fixed; the chance of one starting is fixed for the UK and moves with the stock market for the US (below). Maximum likelihood through Hamilton's filter (section 4.2, pp. 367-369) gives every parameter and each month's chance of a recession. The optimizer (L-BFGS-B) starts from three splits of the months into regimes (by the largest residuals, by their size and by short recessions), plus two more with the equity link, and keeps the best.

The NBER's recession dates are not an input, yet the regimes line up with them: on US data the fit puts 12% of months in recession, in spells of 7.6 months on average, against 12% of months in NBER recessions since 1955. The chart shows US unemployment with the NBER recessions and the fit's filtered chance of the recession regime:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/economy/unemployment-regimes-us" alt="US unemployment since 1956 with NBER recessions, and the fit's filtered chance of the recession regime" %}

The UK fit on the OECD's record since 1971 finds longer, slower recessions: 18% of months, in spells of 17.3 months. A single mean-reverting fit on that record, with history's volatility, reaches zero in a fifth of 30-year paths; the sharp rises and slow falls of the regimes keep it off the floor. The chart shades the months the fit puts in the recession regime:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/economy/unemployment-regimes-uk" alt="UK unemployment since 1971 with the months in the recession regime shaded, the fitted calm level and the average" %}

## Recessions Are Likelier after a Stock-Market Fall (United States)

The chance of a US recession starting moves with the stock market's return over the past year. These are the time-varying transition probabilities of [Filardo (1994)](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}, in the logistic form of [Diebold, Lee and Weinbach (1994, section 2)](https://doi.org/10.1093/oso/9780198773917.003.0010){:target="_blank"}, fitted jointly with the regimes by maximum likelihood (with a prior on the slope, below):

$$
P(s_t = \text{recession} \mid s_{t-1} = \text{expansion}) = \frac{1}{1 + e^{-(a + g_R \min(R_t, 0))}}, \qquad R_t = \ln S_{t-3} - \ln S_{t-15} - m_R
$$

$$R_t$$ is the trailing-year log return of Shiller's S&P Composite total-return index ([Shiller, U.S. stock market data](https://shillerdata.com/){:target="_blank"}), ending three months earlier, less its normal level $$m_R$$: its average over the fit, and in a run the linked equity market's own expected return. Only a shortfall counts: returns above normal do not lower the chance. Falling stock prices are one of the financial signs [Estrella and Mishkin (1998)](https://doi.org/10.1162/003465398557320){:target="_blank"} find most useful ahead of a recession. The chance that a recession starts in a given month:

<div class="ca-nums fs-nums">
  <span><b>1.1%</b>with returns at their normal level</span>
  <span><b>5.6%</b>after a year 20% below normal</span>
</div>

In a run, each scenario's own US equity market drives its own chance of a recession.

Every US recession since 1969 followed a bear market or an inverted curve, so a slope fitted by maximum likelihood alone would run off to infinity (separation: the signal predicts the outcome perfectly in the sample). The slope therefore carries the default prior of [Gelman, Jakulin, Pittau and Su (2008, sections 2.1-2.2)](https://doi.org/10.1214/08-AOAS191){:target="_blank"}, a Cauchy distribution with scale 2.5 on an input with a standard deviation of 0.5, which is a scale of 1.25 on the unit-variance signal the fit uses; the fit is the mode of the resulting posterior.

## Settling at the Official Longer-Run Rate

Where does unemployment settle? The [plucking model of Dupraz, Nakamura and Steinsson (2019, sections 1 and 2.2)](https://doi.org/10.3386/w26351){:target="_blank"} reads the business cycle as rises of unemployment above a floor: recessions pluck it up from a resting point of low unemployment, and it does not swing symmetrically around a natural rate. The FOMC reads its longer-run projections the same way, as the values reached in the absence of further shocks ([Summary of Economic Projections, 16 September 2026, note to Table 1](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm){:target="_blank"}). In this model that is the calm level, where unemployment settles in a long expansion. The default therefore shifts every unemployment process that a policy-rule short rate reads (all three in the default factor set) so that its calm level equals the official estimate, and keeps the fitted distance from the calm level to the average: recessions still push the average above it.

The anchored averages, 6.01% for the US and 7.11% for the UK, sit above history's 5.81% since 1956 and 6.61% since 1971: the official longer-run rates are above the calm levels the fits found (3.78% and 3.61%), and the distance from calm level to average is kept as fitted, 1.8 points for the US and 2.9 for the UK. For the UK that distance is large because its recessions last 17.3 months on average and unemployment falls back slowly, at a speed of 0.13 a year.

The alternative reading takes the official rate as unemployment's average over the cycle, the zero-mean gap the European Commission builds its NAWRU (non-accelerating wage rate of unemployment) on ([Havik et al., 2014, section 2.4.2](https://ec.europa.eu/economy_finance/publications/economic_paper/2014/pdf/ecp535_en.pdf){:target="_blank"}). It is available as an option (`natural_rate_anchor: average`), but it puts the calm level the whole push below the official rate: 2.4% for the US and 1.3% for the UK on the default fits. US unemployment has not been below 3.4% since the OECD record starts in 1956; it touched 3.4% in 1968-69 and in April 2023. The chart compares both readings, with France for the euro area:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/economy/unemployment-anchor" alt="US, UK and French unemployment with the calm level at the official natural rate, the average over the cycle, and the calm level the average reading would give" %}

Which years the regimes are fitted on matters as well. The Great Moderation from 1984 ([McConnell and Perez-Quiros, 2000](https://doi.org/10.1257/aer.90.5.1464){:target="_blank"}; [Stock and Watson, 2002, section 3](https://doi.org/10.1086/ma.17.3585284){:target="_blank"}) had milder US recessions, so a fit from 1984 has a smaller push. The table scores the US choices on 30-year runs (2,000 scenarios, months in years 10 to 30) and on backtests from 2000 to 2022 that read only what was known at each year end. The backtests use the 18 year-end start dates (origins) no choice was made on, scored without waiting for each month's first release; the CRPS skill is how much the scenarios improve on a forecast of no change:

| US regimes fitted on | Official 4.2% is the | Calm level | Average | Months below 3.4% | 90% coverage | CRPS skill |
|:--|:--|--:|--:|--:|--:|--:|
| 1956 on (the default) | Calm level | 4.2% | 6.0% | 2.5% | 0.70 | +0.37 |
| 1984 on | Calm level | 4.2% | 5.7% | 4.3% | 0.62 | +0.37 |
| 1984 on | Average | 2.7% | 4.2% | 26% | 0.70 | +0.43 |

The average reading scores best on the backtests, which mostly start from low unemployment, but a quarter of its months sit below anything the US has seen since 1956, and that is not a scenario set to defend. The shorter sample keeps the calm reading's skill but narrows the bands. The default keeps the whole record with the calm reading; both alternatives remain available (`natural_rate_anchor`, `history_start_year`).

## Euro-Area Unemployment {#euro-area-unemployment}

The euro area's unemployment is fitted on France's. German unemployment fell structurally after the mid-2000s labor reforms, so a fit on 2000-2026 gives a half-life of about 53 years; France's reverts in a few years, closer to the euro area's own cycle. The model is the mean-reverting one of [Ahlgrim, D'Arcy and Gorvett (2005, eq. 3.19)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"} with a Phillips-curve term ([Phillips, 1958](https://doi.org/10.1111/j.1468-0335.1958.tb00003.x){:target="_blank"}), fitted quarterly since 2000:

$$
du_t = \kappa\,(\mu - u_t)\,dt + \alpha\,d\pi_t + \sigma\,dW_t
$$

Without regimes the calm level is the mean, so the anchor sets it to France's NAWRU. The fitted speed is 0.17 a year:

<div class="ca-nums fs-nums">
  <span><b>7.16%</b>calm level, France's NAWRU for 2027</span>
  <span><b>4.1 years</b>half-life of a gap</span>
  <span><b>&minus;0.12</b>Phillips sensitivity</span>
  <span><b>0.57%</b>volatility</span>
</div>

## How Each Number Is Set

Every number in the US and UK unemployment models, and where it comes from:

| Number | United States | United Kingdom | Kind | Why |
|:--|--:|--:|:--|:--|
| History | OECD, monthly from 1956-02 | OECD, monthly from 1971-03 | Data | The longest official monthly records; a fit from 1984 narrows the bands at the same skill (table above) |
| Months left out | March-December 2020 | March-December 2020 | Judgement | The lockdown and reopening stay out of the likelihood, while the filter carries the regime probabilities through them, as [Lenza and Primiceri (2022, sections 1 and 4)](https://doi.org/10.1002/jae.2895){:target="_blank"} find acceptable for estimating parameters. Kept in, April 2020's ten-point jump turns the recession regime into a 2% outlier regime of three-month spells |
| Minimum history | 240 months | 240 months | Judgement | Fewer hold too few recessions to time two regimes on |
| Speed $$\kappa$$, per year | 0.24 | 0.13 | Fitted | |
| Recession push $$D_r$$, per year | 3.44 points | 2.14 points | Fitted | |
| Volatility, expansion / recession | 0.52% / 0.74% | 0.29% / 0.27% | Fitted | |
| Chance a recession lasts another month | 0.869 | 0.942 | Fitted | |
| Share of months in recession | 12% | 18% | Fitted | |
| Phillips sensitivity $$\alpha$$ | -0.031 | -0.013 | Fitted | |
| Equity link, slope on the shortfall | -7.57 on the log-odds per unit of log-return shortfall | none | Fitted | Shiller's index is the only monthly equity history long enough that needs no API key |
| Equity window lag | 3 months | | Judgement | The lag that fits US data 1969-2025 best: R² of 0.43 at three months, 0.42 at none and 0.35 at six, in the yearly regression of unemployment's change on the past year's equity return |
| Prior scale on the slope | 1.25 | | Sourced | [Gelman et al. (2008, sections 2.1-2.2)](https://doi.org/10.1214/08-AOAS191){:target="_blank"} |
| Calm level, fitted | 3.78% | 3.61% | Fitted | |
| Calm level, anchored | 4.2% | 4.21% | Sourced | The official natural rate as the level reached without further shocks ([Dupraz, Nakamura and Steinsson, 2019](https://doi.org/10.3386/w26351){:target="_blank"}): FOMC longer-run median ([SEP, 16 September 2026, Table 1](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm){:target="_blank"}); the European Commission's NAWRU for 2027 ([AMECO ZNAWRU, Spring 2026](https://ec.europa.eu/economy_finance/ameco/wq/series?fullVariable=1.0.0.0.ZNAWRU&countries=FRA,GBR,DEU&years=2027&lastYear=0&yearOrder=ASC){:target="_blank"}) |
| Long-run average, anchored | 6.01% | 7.11% | Derived | The anchor plus the fitted distance from calm level to average |

## Examples

The examples on this page use the run from the [overview](/projects/financescenarios/docs#simulating-scenarios): the default settings and factor set, calibrated on 25 October 2026, with 2,000 scenarios and seed 42.

### Unemployment in Three Economies {#unemployment-rate}

To simulate the three economies and read unemployment off after one, three and five years:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
result = scenarios.simulate(n_simulations=2000, seed=42)

result.horizon_summary(
    [1, 3, 5], factors=["united_states_unemployment", "eurozone_unemployment", "united_kingdom_unemployment"]
)
```

Which gives:

| factor | horizon | q0.05 | q0.5 | q0.95 |
|:-------|--------:|------:|-----:|------:|
| united_states_unemployment | 1 | 0.0351 | 0.0429 | 0.0567 |
| united_states_unemployment | 3 | 0.0330 | 0.0472 | 0.0812 |
| united_states_unemployment | 5 | 0.0338 | 0.0514 | 0.0895 |
| eurozone_unemployment | 1 | 0.0704 | 0.0796 | 0.0884 |
| eurozone_unemployment | 3 | 0.0647 | 0.0776 | 0.0902 |
| eurozone_unemployment | 5 | 0.0614 | 0.0759 | 0.0909 |
| united_kingdom_unemployment | 1 | 0.0423 | 0.0471 | 0.0579 |
| united_kingdom_unemployment | 3 | 0.0399 | 0.0484 | 0.0810 |
| united_kingdom_unemployment | 5 | 0.0390 | 0.0506 | 0.0951 |

US unemployment starts at 4.2% and its median drifts up to 5.14% over five years, while the 95th percentile reaches 8.95%: recessions push unemployment up fast and it comes down slowly. The euro area, fitted on France without regimes, stays in a narrow band around 7.6%. When plotted:

{% include ft-chart.html id="economy-unemployment" src="/assets/data/financescenarios-guides/economy.json" label="Median and 5-95% band of unemployment in the US, the euro area and the UK over five years" %}

The US regimes put 12% of months in recession, and a recession month is followed by another with a chance of 87%, so a rise, once started, tends to continue. To count the scenarios in which unemployment has risen by a point or more from today's level:

```python
countries = {"US": "united_states", "Euro area": "eurozone", "UK": "united_kingdom"}

rise = {
    name: (result.paths[f"{country}_unemployment"] - result.paths[f"{country}_unemployment"][:, :1] >= 0.01).mean(axis=0)
    for name, country in countries.items()
}
```

That share grows from 10% after one year to 35% after three and 48% after five in the US, against 6%, 24% and 36% in the UK and at most 6% in the euro area. When plotted:

{% include ft-chart.html id="economy-unemployment-rise" src="/assets/data/financescenarios-guides/economy.json" label="Share of the 2,000 scenarios in which unemployment is at least one percentage point above today's level, for the US, the euro area and the UK" %}

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">17</span></summary>

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. [casact.org](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}
- Diebold, F.X., Lee, J.-H., Weinbach, G.C. (1994). "Regime Switching with Time-Varying Transition Probabilities." In Hargreaves, C. (ed.), Nonstationary Time Series Analysis and Cointegration, 283-302. [doi.org](https://doi.org/10.1093/oso/9780198773917.003.0010){:target="_blank"}
- Dupraz, S., Nakamura, E., Steinsson, J. (2019). "A Plucking Model of Business Cycles." NBER Working Paper 26351. [doi.org](https://doi.org/10.3386/w26351){:target="_blank"}
- Estrella, A., Mishkin, F.S. (1998). "Predicting U.S. Recessions: Financial Variables as Leading Indicators." Review of Economics and Statistics, 80(1), 45-61. [doi.org](https://doi.org/10.1162/003465398557320){:target="_blank"}
- European Commission (2026). AMECO, Spring 2026 forecast: ZNAWRU. [ec.europa.eu](https://ec.europa.eu/economy_finance/ameco/wq/series?fullVariable=1.0.0.0.ZNAWRU&countries=FRA,GBR,DEU&years=2027&lastYear=0&yearOrder=ASC){:target="_blank"}
- Federal Open Market Committee (2026). Summary of Economic Projections, 16 September 2026, Table 1. [federalreserve.gov](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm){:target="_blank"}
- Filardo, A.J. (1994). "Business-Cycle Phases and Their Transitional Dynamics." Journal of Business & Economic Statistics, 12(3), 299-308. [doi.org](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}
- Gelman, A., Jakulin, A., Pittau, M.G., Su, Y.-S. (2008). "A Weakly Informative Default Prior Distribution for Logistic and Other Regression Models." The Annals of Applied Statistics, 2(4), 1360-1383. [doi.org](https://doi.org/10.1214/08-AOAS191){:target="_blank"}
- Hamilton, J.D. (1989). "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle." Econometrica, 57(2), 357-384. [doi.org](https://doi.org/10.2307/1912559){:target="_blank"}
- Havik, K., Mc Morrow, K., Orlandi, F., Planas, C., Raciborski, R., Röger, W., Rossi, A., Thum-Thysen, A., Vandermeulen, V. (2014). "The Production Function Methodology for Calculating Potential Growth Rates & Output Gaps." European Economy, Economic Papers 535. [ec.europa.eu](https://ec.europa.eu/economy_finance/publications/economic_paper/2014/pdf/ecp535_en.pdf){:target="_blank"}
- Lenza, M., Primiceri, G.E. (2022). "How to Estimate a Vector Autoregression after March 2020." Journal of Applied Econometrics, 37(4), 688-699. [doi.org](https://doi.org/10.1002/jae.2895){:target="_blank"}
- McConnell, M.M., Perez-Quiros, G. (2000). "Output Fluctuations in the United States: What Has Changed Since the Early 1980's?" American Economic Review, 90(5), 1464-1476. [doi.org](https://doi.org/10.1257/aer.90.5.1464){:target="_blank"}
- Neftçi, S.N. (1984). "Are Economic Time Series Asymmetric over the Business Cycle?" Journal of Political Economy, 92(2), 307-328. [doi.org](https://doi.org/10.1086/261226){:target="_blank"}
- Phillips, A.W. (1958). "The Relation Between Unemployment and the Rate of Change of Money Wage Rates in the United Kingdom, 1861-1957." Economica, 25(100), 283-299. [doi.org](https://doi.org/10.1111/j.1468-0335.1958.tb00003.x){:target="_blank"}
- Shiller, R.J. (2015). "Irrational Exuberance", 3rd edition, Princeton University Press, and its data as updated by the author: monthly US stock prices, dividends, earnings and consumer prices since 1871. [shillerdata.com](https://shillerdata.com/){:target="_blank"}
- Sichel, D.E. (1993). "Business Cycle Asymmetry: A Deeper Look." Economic Inquiry, 31(2), 224-236. [doi.org](https://doi.org/10.1111/j.1465-7295.1993.tb00879.x){:target="_blank"}
- Stock, J.H., Watson, M.W. (2002). "Has the Business Cycle Changed and Why?" NBER Macroeconomics Annual, 17, 159-218. [doi.org](https://doi.org/10.1086/ma.17.3585284){:target="_blank"}

</details>

{% include ft-charts-script.html %}
