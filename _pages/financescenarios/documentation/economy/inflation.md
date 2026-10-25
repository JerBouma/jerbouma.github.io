---
title: Inflation
seo_title: "Inflation | Finance Scenarios"
seo_title_suffix: false
excerpt: "How Finance Scenarios simulates inflation: calm and high-inflation regimes after Hamilton and Harris, each a Wilkie AR(1), with the long-run mean anchored to the expectations forecasters publish."
description: "Inflation in Finance Scenarios: the regime-switching AR(1) and Hamilton's filter, the UK's inflation-targeting sample, anchoring the mean to survey expectations, price indices, the market-implied model and a run."
author_profile: false
permalink: /projects/financescenarios/docs/economy
classes: wide-sidebar
layout: single
redirect_from:
    - /projects/financescenarios/docs/reference/inflation
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-economy"
---

Inflation sets the real value of every nominal cash flow. A single mean-reverting process fitted on a calm window cannot produce a 1970s or a 2021: fitted on US data from 2000 to 2019, its 90% band for 2021 ended near 4%, and inflation came in at 7.0%. History instead shows long calm stretches near target, interrupted by spells in which inflation runs far higher and swings more. In the default model inflation therefore switches between a calm and a high-inflation regime, with its long-run mean anchored to the long-run expectation or target published for each country.

<div class="fs-facts">
  <div><span>Series</span><b>CPI inflation over the past year</b></div>
  <div><span>Data</span><b>OECD CPI since 1956 (the UK since 1993)</b></div>
  <div><span>Default model</span><b>Calm and high-inflation regimes</b></div>
</div>

## The Model

Each regime $$s$$ is the yearly AR(1) of [Wilkie (1986, section 3.4)](https://doi.org/10.1017/S0071368600009009){:target="_blank"} with its own level $$\mu_s$$ and shock size $$\sigma_s$$, and a Markov chain decides each year whether to stay or switch ([Hamilton, 1989, section 2, eq. 2.2, p. 360](https://doi.org/10.2307/1912559){:target="_blank"}; [Harris, 1999, section 2, p. 49](https://doi.org/10.2143/AST.29.1.504606){:target="_blank"}):

$$
I_t = \mu_{s_t} + \phi\,(I_{t-1} - \mu_{s_t}) + \sigma_{s_t}\,\varepsilon_t, \qquad P(s_t = j \mid s_{t-1} = i) = p_{ij}
$$

Here $$I_t$$ is CPI inflation over the past year, $$\phi$$ the share of a gap to the regime's level left after a year, and $$p_{ij}$$ the chance of moving from regime $$i$$ to $$j$$ in a year. Both regimes share $$\phi$$, which keeps the long-run mean in closed form (below).

The parameters maximize the likelihood of Hamilton's filter (section 4.2, pp. 367-368), started from the long-run shares of the two regimes. Inflation is a year-over-year rate, so neighboring monthly readings share eleven of their twelve months; the fit therefore pairs each reading with the one a year earlier. For monthly data that gives twelve interleaved yearly series (every January, every February, ...) and for quarterly data four; each is run through the filter and their likelihoods are averaged, a composite likelihood. Regime-switching likelihoods have several local maxima ([Harris, 1999, section 1, p. 48](https://doi.org/10.2143/AST.29.1.504606){:target="_blank"}), so the fit starts from three points and keeps the best.

In the simulation each regime becomes a monthly mean-reverting (Ornstein-Uhlenbeck) process. Its persistence per step $$\phi_m$$ keeps the regime's long-run spread and the variance of its multi-year averages, $$(1 + \phi_m)/(1 - \phi_m) = k\,(1 + \phi)/(1 - \phi)$$ for $$k$$ steps a year, and the switching chances are rescaled to the month through the generator of the yearly transition matrix, its continuous-time equivalent ([Israel, Rosenthal and Wei, 2001, section 2, p. 247](https://doi.org/10.1111/1467-9965.00114){:target="_blank"}).

The filter puts the 1970s and early 1980s in the high regime in the US and Germany, 1991-1993 in Germany, and 2021-2023 everywhere. The chart shades those months on each country's OECD inflation, the US and Germany since 1956 and the UK since 1993 (next section):

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/economy/inflation-regimes" alt="US and German CPI inflation since 1956 and UK CPI inflation since 1993, with the months in the high-inflation regime shaded and the two regime levels as fitted and anchored" %}

The fitted parameters per country:

| Fitted on OECD CPI | United States | Germany (euro) | United Kingdom |
|:--|--:|--:|--:|
| Data | Monthly since 1956, 849 readings | Quarterly since 1956, 283 readings | Monthly since 1993, 405 readings |
| Calm level $$\mu_0$$, as fitted | 2.55% | 1.73% | 2.01% |
| High level $$\mu_1$$, as fitted | 7.92% | 6.35% | 6.57% |
| Persistence $$\phi$$ (a year) | 0.52 | 0.40 | 0.36 |
| Shock size, calm / high | 1.09% / 2.96% | 0.89% / 1.11% | 0.74% / 2.52% |
| Chance of staying a year, calm / high | 0.93 / 0.72 | 0.92 / 0.67 | 0.94 / 0.53 |
| Average spell, calm / high (years) | 13.9 / 3.5 | 12.5 / 3.0 | 18.1 / 2.1 |
| Long-run share of the high regime | 20% | 19% | 11% |
| Long-run mean, as fitted | 3.64% | 2.62% | 2.49% |
| Long-run median, as fitted | 3.12% | 2.26% | 2.21% |

In the US and the UK the high regime's shocks are 2.7 and 3.4 times the calm regime's, in line with [Harris (1999, section 4, Table 2, p. 57)](https://doi.org/10.2143/AST.29.1.504606){:target="_blank"}, who finds a turbulent regime about three times as volatile in Australian data; Germany's high-inflation spells were steadier, 1.2 times.

## The UK Is Fitted on Its Inflation-Targeting Era

Inflation's level and persistence depend on the monetary regime: [Benati (2008, section 2.1.1)](https://doi.org/10.1162/qjec.2008.123.3.1005){:target="_blank"} finds inflation persistence high under regimes without a clear nominal anchor and close to zero under inflation targeting, for the UK among others. UK inflation targeting began on 8 October 1992, so the default fits the UK from 1993, its first full year.

The long record does not fit the UK of today. Fitted since 1956, its high regime sits at 11.7% and takes a quarter of the time: a long-run mean of 2% would then need a calm level of &minus;0.28%, normal times with falling prices that the record never shows. Fitted from 1993, the calm level is 2.01% and the high regime, 6.6%, is the 2022-2023 surge. On backtests from 2000 to 2022 that read only what was known at each year end, the 1993 fit scores best. Its CRPS skill (how much its scenarios improve on a forecast of no change) is +0.37 against +0.22 for the long record on the 18 year-end start dates (origins) no choice was made on, and +0.38 against +0.25 on the 14 origins never used for any choice.

That choice has a cost:

<div class="ca-nums fs-nums">
  <span><b>0.63</b>share of outcomes inside the 90% band on those backtests: the bands are narrow</span>
  <span><b>6.2%</b>highest year-end level in a 30-year scenario, at the median</span>
  <span><b>24.9%</b>highest year-end level in UK history (1975)</span>
</div>

The 1970s are not in the UK fit, so a default run does not produce them on its own. The bundled `stagflation_1970s`, `energy_war_2022` and `inflation_shock_2022` regimes simulate those spells (see [Regimes](/projects/financescenarios/docs/regimes)). The US and Germany keep their long records: their means meet the anchors with calm levels well above zero.

## Anchoring the Mean to Expectations

As fitted, the long-run mean sits where the historical record puts it: 3.64% for the US and 2.62% for Germany, above what forecasters expect today. The default moves both regime levels by the same amount so that the long-run mean equals today's long-run expectation for the country. The gap between the regimes, their shock sizes, the persistence and the switching chances stay as fitted, so a move into the high regime lifts inflation by as much as it did in history, and the chance and shape of a high-inflation spell are history's.

The anchor matches the mean, not the median, because the mean is what the sources measure. The Philadelphia Fed's 10-year forecast is an annual-average rate of inflation over the next ten years ([Survey of Professional Forecasters, 2026Q3, p. 4](https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/survey-of-professional-forecasters/2026/spfq326.pdf){:target="_blank"}), an expected average. The models this one builds on read their long-run level the same way: [Wilkie's (1986, section 3.4)](https://doi.org/10.1017/S0071368600009009){:target="_blank"} QMU is the mean of his inflation AR(1), and [Ahlgrim, D'Arcy and Gorvett's (2005, section 3)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"} $$\mu_q$$ is the level expected inflation reverts to. With a shared persistence, the long-run mean is the regimes' levels weighted by their long-run shares, $$w_0\mu_0 + w_1\mu_1$$, so moving both levels by the same amount moves the mean by that amount, in closed form.

Rare high-inflation spells skew the distribution, so its median sits below its mean. The median is kept as a diagnostic only. It is computed rather than simulated: the inflation axis is cut into bins an eighth of a month's shock wide, the chain the simulation steps is written as a transition matrix between (bin, regime) states, and its long-run (stationary) distribution is solved directly. On the US fit this median lies within two basis points of the median of 100,000 simulated 60-year paths.

The shift stops at a calm level of zero: normal times with falling prices are not in the OECD record of the US, the UK and Germany since 1956. Where a record's high regime is too high or too frequent for the expectation, the calm level stops at zero, the mean stays above the expectation, and the calibration warns.

The chart shows the long-run distribution as fitted and after anchoring, with the means and the anchored medians:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/economy/inflation-stationary" alt="The long-run distribution of inflation as fitted and after anchoring, with the means and the anchored medians, for the US, Germany and the UK" %}

Each anchor is a published long-run expectation or target:

| Anchor | Value | Kind | Source |
|:--|:--|:--|:--|
| United States | 2.3% | Sourced | Headline CPI inflation over 2026-2035, an annual-average rate, the median of 25 forecasters in the [Survey of Professional Forecasters, Federal Reserve Bank of Philadelphia (2026Q3, p. 4; p. 18, Table Eight)](https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/survey-of-professional-forecasters/2026/spfq326.pdf){:target="_blank"}; their mean is 2.43% |
| Euro area (Germany) | 2.0% | Sourced | Longer-term (2031) HICP expectation, the average of the respondents' point forecasts, [ECB Survey of Professional Forecasters (2026Q3, press release of 24 July 2026)](https://www.ecb.europa.eu/press/pr/date/2026/html/ecb.pr260724~a099353951.en.html){:target="_blank"}; the euro-area survey stands in for Germany, whose CPI has no survey of its own |
| United Kingdom | 2% | Sourced | The Bank of England's CPI target, [HM Treasury (2025, remit letter, paragraph 4)](https://www.gov.uk/government/publications/monetary-policy-remit-budget-2025/letter-from-chancellor-of-the-exchequer-to-govenor-of-the-bank-of-england){:target="_blank"}; the UK has no comparable long-horizon survey |

The chart shows the long-run inflation expectations of professional forecasters in the US and the euro area since 1991 and 1999:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/economy/inflation-expectations" alt="Long-run inflation expectations of professional forecasters in the US and the euro area since 1991 and 1999" %}

After anchoring, the calm and high levels are 1.21% and 6.59% for the US, 1.10% and 5.73% for Germany, and 1.52% and 6.08% for the UK. The long-run means meet their anchors, and the spikes keep the medians below them, as they did in history:

<div class="ca-nums fs-nums">
  <span><b>1.78%</b>US long-run median (mean 2.30%)</span>
  <span><b>1.63%</b>German long-run median (mean 2.00%)</span>
  <span><b>1.72%</b>UK long-run median (mean 2.00%)</span>
</div>

A 30-year run of 2,000 scenarios reproduces them: over years 10 to 30, US inflation averages 2.32% with a median of 1.80%. The lower calm level has one visible cost: the lowest year-end US inflation in a 30-year scenario is &minus;1.1% at the median, against 0.1% at the end of 2008, the lowest year end since 1956.

The anchor only sets where inflation settles in the long run. Every scenario starts from today's inflation and in a regime drawn from today's probabilities, which the filter reads off the recent data again with the anchored levels: US inflation starts at 3.74% with a 13% chance of being in the high regime. The gap between the share of scenarios in the high regime and its long-run value shrinks to $$p_{00} + p_{11} - 1$$ of itself each year (0.65 for the US), so a run that starts calm reaches the long-run mix within a few years.

## Price Indices Compound with ln(1 + π)

Inflation is a year-over-year rate, the growth of the price index over a year. The index a scenario builds from it compounds by the log change that rate implies, $$\ln(1 + I_t)$$ a year, as [Ahlgrim, D'Arcy and Gorvett (2005, section 3, eq. 3.7)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"} model the price index:

$$
P_{t+\Delta t} = P_t \exp\!\big(\ln(1 + I_t)\,\Delta t\big)
$$

so inflation held at 4% gives an index of $$1.04^T$$. Compounding the rate itself, $$\exp(\sum I_t\,\Delta t)$$, would overstate a 30-year index by about 1.3% at 3% inflation. House prices, the price gap behind purchasing power parity and gold's real drift compound the same way (see [Simulation Engine](/projects/financescenarios/docs/simulation-engine#price-indices)).

## How Each Number Is Set

Every number in the inflation model, and where it comes from:

| Number | Value | Kind | Why |
|:--|:--|:--|:--|
| Regimes | 2 | Judgement | Calm and high inflation; US inflation since 1956 holds one long high-inflation episode, too few to separate a third regime |
| Shared persistence | One $$\phi$$ for both regimes | Judgement | It makes the long-run mean a closed form, so the anchor below moves it exactly |
| History | OECD CPI since 1956; the UK since 1993 | Judgement, sourced for the UK | The longest official series for all three countries at monthly or quarterly frequency; the UK's inflation-targeting era from 1993 ([Benati, 2008](https://doi.org/10.1162/qjec.2008.123.3.1005){:target="_blank"}) |
| Minimum history | 10 years; a notice below 40 | Judgement | Under 40 years the high regime rests on one or two episodes; the UK's 33 years are below it by choice (above) |
| Regime levels, shocks, persistence, switching | Table above | Fitted | Maximum likelihood, Hamilton's filter |
| Levels after anchoring | Calm 1.21%, 1.10%, 1.52%; high 6.59%, 5.73%, 6.08% | Derived | Both levels moved by the same amount so the long-run mean equals the anchor, the calm level no lower than zero |
| Anchors | 2.3%, 2.0%, 2% | Sourced | Table above |
| Starting point | Today's inflation and the filter's regime probabilities | Data | OECD inflation since 2000, read through the anchored regimes |

## Other Inflation Models

**Mean reversion to one level** (`method: ou`). Inflation as an Ornstein-Uhlenbeck process ([Uhlenbeck and Ornstein, 1930, section 5, pp. 827-828](https://doi.org/10.1103/PhysRev.36.823){:target="_blank"}),

$$
dI_t = a(\theta - I_t)\,dt + \sigma\,dW_t
$$

fitted on readings a year apart, $$I_t = c + \phi\,I_{t-k} + e_t$$ for $$k$$ readings a year, as [Ahlgrim, D'Arcy and Gorvett (2005, section 3, p. 15)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf#page=15){:target="_blank"} do, with the long-run level $$\theta = c/(1 - \phi)$$. GARCH volatility, which rises after large shocks ([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1){:target="_blank"}), and a long history (UK inflation from 1210, US from 1872) are options.

**Wilkie's AR(1)** (`method: wilkie_ar1`). The discrete yearly model of [Wilkie (1986, sections 3.3-3.4)](https://doi.org/10.1017/S0071368600009009){:target="_blank"}, the top of his cascade of dividend yield, dividend growth and consols:

$$
I_t = \mu + \phi\,(I_{t-1} - \mu) + \sigma\,z_t
$$

with his UK values $$\mu$$ = 5%, $$\phi$$ = 0.6 and $$\sigma$$ = 5% ([Dividends](/projects/financescenarios/docs/markets/dividends) and [Other Rate Models](/projects/financescenarios/docs/interest-rates/other-models#wilkies-consols-yield) cover the rest of the cascade).

**Hibbert's two-factor model** (`method: hibbert_two_factor`). Inflation reverts to an expected-inflation level $$m_t$$ that itself moves, $$dI_t = a(m_t - I_t)\,dt + \sigma\,dW_t$$ ([Hibbert, Mowbray and Turnbull, 2001, section 5.1.2, p. 19](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf#page=19){:target="_blank"}): by default a yearly mean-reverting factor of its own, or an exponentially weighted average of inflation's own path.

**Market-implied inflation (risk-neutral).** To value inflation-linked cash flows at market prices, inflation moves around today's breakeven curve, a Nelson-Siegel fit ([Nelson and Siegel, 1987](https://doi.org/10.1086/296409){:target="_blank"}; [Diebold and Li, 2006](https://doi.org/10.1016/j.jeconom.2005.03.005){:target="_blank"}) to the nominal less the inflation-linked yields, with $$f_{BE}$$ its forward breakeven rate, continuously compounded:

$$
\ln(1 + I_t) = f_{BE}(t) - \frac{\sigma^2}{2a^2}\left(1 - e^{-at}\right)^2 + y_t, \qquad dy_t = -a\,y_t\,dt + \sigma\,dW_t, \quad y_0 = 0
$$

The convexity term keeps the expected price index on the breakeven curve, so a plain inflation-linked cash flow is valued at the market's breakeven while a cap or floor on indexation gets a time value from the country's historical speed and volatility. Before the first quoted maturity the curve holds the fitted breakeven flat, as EIOPA's constant-forward rule does for its risk-free curve ([RFR Technical Documentation, EIOPA-BoS-26/198, Annex D.8](https://www.eiopa.europa.eu/eiopa-publishes-rfr-technical-documentation-become-applicable-30-january-2027-2026-05-26_en){:target="_blank"}). The breakevens come from:

| Market | Source | Maturities | Index |
|:--|:--|:--|:--|
| United States | US Treasury, nominal minus TIPS | 5 to 30 years | US CPI |
| United Kingdom | Bank of England implied inflation curve | 3 to 40 years | RPI |
| Germany / euro area | Bundesbank, nominal minus inflation-linked | 5 to 15 years | Euro area HICP ex tobacco |

**Links.** Inflation can respond to the same step's move in a paired short rate or in the leading indicator; for rates and inflation that drive each other, fitted jointly, use the [KNW models](/projects/financescenarios/docs/interest-rates/knw).

## Examples

The examples on this page use the run from the [overview](/projects/financescenarios/docs#simulating-scenarios): the default settings and factor set, calibrated on 25 October 2026, with 2,000 scenarios and seed 42.

### Inflation in Three Economies

The default factor set simulates year-over-year consumer price inflation for the US, the euro area (fitted on Germany's long record) and the UK. To simulate them and read them off after one, three and five years:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
result = scenarios.simulate(n_simulations=2000, seed=42)

result.horizon_summary(
    [1, 3, 5], factors=["united_states_inflation", "eurozone_inflation", "united_kingdom_inflation"]
)
```

Which gives, among other columns:

| factor | horizon | q0.05 | q0.5 | q0.95 |
|:-------|--------:|------:|-----:|------:|
| united_states_inflation | 1 | 0.0076 | 0.0271 | 0.0622 |
| united_states_inflation | 3 | -0.0037 | 0.0200 | 0.0740 |
| united_states_inflation | 5 | -0.0064 | 0.0181 | 0.0770 |
| eurozone_inflation | 1 | 0.0057 | 0.0210 | 0.0484 |
| eurozone_inflation | 3 | -0.0012 | 0.0166 | 0.0549 |
| eurozone_inflation | 5 | -0.0027 | 0.0157 | 0.0541 |
| united_kingdom_inflation | 1 | 0.0114 | 0.0270 | 0.0705 |
| united_kingdom_inflation | 3 | 0.0046 | 0.0202 | 0.0668 |
| united_kingdom_inflation | 5 | 0.0023 | 0.0174 | 0.0552 |

Inflation starts at 3.74% in the US, 2.97% in the euro area and 3.67% in the UK, and the median falls to between 1.57% and 1.81% after five years. The bands are lopsided: the US 95th percentile rises from 6.22% to 7.70% while the median falls, because a minority of scenarios enter a high-inflation spell. When plotted:

{% include ft-chart.html id="economy-inflation" src="/assets/data/financescenarios-guides/economy.json" label="Median and 5-95% band of inflation in the US, the euro area and the UK over five years" %}

### The Regimes Behind It

The fitted parameters show the two regimes. To read them for the US:

```python
calibration = scenarios.calibrate()

calibration.calibrated_params["united_states_inflation"]
```

Which shows a calm regime at 1.21% and a high-inflation regime at 6.59%, whose shocks are 2.7 times as large (1.09% against 2.96%), and a chance of 13% that the economy is in the high regime today. The two levels are set so that the long-run mean meets the long-run expectation of 2.3% for the US; the euro area and the UK are anchored to 2.0%.

The share of scenarios in a high-inflation spell is what the regimes add over a single mean-reverting model. To count, at every date, the scenarios with inflation above 5%:

```python
countries = {"US": "united_states", "Euro area": "eurozone", "UK": "united_kingdom"}

above_5 = {name: (result.paths[f"{country}_inflation"] > 0.05).mean(axis=0) for name, country in countries.items()}
```

After five years 12.1% of the US scenarios, 7.0% of the euro-area scenarios and 6.3% of the UK scenarios have inflation above 5%. When plotted:

{% include ft-chart.html id="economy-high-inflation" src="/assets/data/financescenarios-guides/economy.json" label="Share of the 2,000 scenarios with inflation above 5% in the US, the euro area and the UK" %}

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">15</span></summary>

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. [casact.org](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}
- Benati, L. (2008). "Investigating Inflation Persistence Across Monetary Regimes." Quarterly Journal of Economics, 123(3), 1005-1060. [doi.org](https://doi.org/10.1162/qjec.2008.123.3.1005){:target="_blank"}
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." Journal of Econometrics, 31(3), 307-327. [doi.org](https://doi.org/10.1016/0304-4076(86)90063-1){:target="_blank"}
- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. [doi.org](https://doi.org/10.1016/j.jeconom.2005.03.005){:target="_blank"}
- EIOPA (2026). Technical documentation of the methodology to derive EIOPA's risk-free interest rate term structures, applicable from 30 January 2027. [eiopa.europa.eu](https://www.eiopa.europa.eu/eiopa-publishes-rfr-technical-documentation-become-applicable-30-january-2027-2026-05-26_en){:target="_blank"}
- European Central Bank (2026). Survey of Professional Forecasters, third quarter of 2026, press release of 24 July 2026. [ecb.europa.eu](https://www.ecb.europa.eu/press/pr/date/2026/html/ecb.pr260724~a099353951.en.html){:target="_blank"}
- Federal Reserve Bank of Philadelphia (2026). Survey of Professional Forecasters, third quarter 2026. [philadelphiafed.org](https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/survey-of-professional-forecasters/2026/spfq326.pdf){:target="_blank"}
- Hamilton, J.D. (1989). "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle." Econometrica, 57(2), 357-384. [doi.org](https://doi.org/10.2307/1912559){:target="_blank"}
- Harris, G.R. (1999). "Markov Chain Monte Carlo Estimation of Regime Switching Vector Autoregressions." ASTIN Bulletin, 29(1), 47-79. [doi.org](https://doi.org/10.2143/AST.29.1.504606){:target="_blank"}
- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert Limited. [ressources-actuarielles.net](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"}
- HM Treasury (2025). Monetary policy remit: Budget 2025, letter from the Chancellor of the Exchequer to the Governor of the Bank of England, 26 November 2025. [gov.uk](https://www.gov.uk/government/publications/monetary-policy-remit-budget-2025/letter-from-chancellor-of-the-exchequer-to-govenor-of-the-bank-of-england){:target="_blank"}
- Israel, R.B., Rosenthal, J.S., Wei, J.Z. (2001). "Finding Generators for Markov Chains via Empirical Transition Matrices, with Applications to Credit Ratings." Mathematical Finance, 11(2), 245-265. [doi.org](https://doi.org/10.1111/1467-9965.00114){:target="_blank"}
- Nelson, C.R., Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." The Journal of Business, 60(4), 473-489. [doi.org](https://doi.org/10.1086/296409){:target="_blank"}
- Uhlenbeck, G.E., Ornstein, L.S. (1930). "On the Theory of the Brownian Motion." Physical Review, 36(5), 823-841. [doi.org](https://doi.org/10.1103/PhysRev.36.823){:target="_blank"}
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. [doi.org](https://doi.org/10.1017/S0071368600009009){:target="_blank"}

</details>

{% include ft-charts-script.html %}
