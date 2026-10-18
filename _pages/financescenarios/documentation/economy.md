---
title: Inflation, Labor and Longevity
seo_title: "Inflation, Labor and Longevity | Finance Scenarios"
seo_title_suffix: false
excerpt: "How the default model sets inflation and unemployment: calm and high-inflation regimes anchored to sourced expectations, expansion and recession regimes for unemployment anchored to official longer-run rates, and how every number is derived from data."
description: "Regime-switching inflation and unemployment in Finance Scenarios: the theory, the sourced and fitted numbers, the charts that derive them, and the business-cycle and longevity models."
author_profile: false
permalink: /projects/financescenarios/docs/economy
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Many liabilities follow the economy rather than markets: pensions are indexed to prices, claims move with the labor market, and annuities run for as long as people live. In the default model inflation and unemployment both switch between regimes: calm and high-inflation spells for inflation, expansions and recessions for unemployment. Both feed the [Taylor-rule short rate](/projects/financescenarios/docs/interest-rates), so a scenario's rates follow its own economy.

This page explains the theory of both, then derives every number they use: what it is, whether it comes from a published source, a fit on data or a judgement, and the chart that shows it. The other inflation models, the leading indicator and mortality follow. The numbers come from one calibration of the default settings and factor set, made on 17 October 2026.

<div class="ca-nav">
  <a href="#inflation-calm-and-high-inflation-regimes"><i class="fas fa-percentage" aria-hidden="true"></i>Inflation</a>
  <a href="#unemployment-expansions-and-recessions"><i class="fas fa-briefcase" aria-hidden="true"></i>Unemployment</a>
  <a href="#run-it"><i class="fas fa-terminal" aria-hidden="true"></i>Run it</a>
  <a href="#other-inflation-models"><i class="fas fa-layer-group" aria-hidden="true"></i>Other inflation models</a>
  <a href="#the-leading-indicator-and-the-business-cycle"><i class="fas fa-gauge" aria-hidden="true"></i>Business cycle</a>
  <a href="#mortality-and-longevity"><i class="fas fa-heart" aria-hidden="true"></i>Mortality and longevity</a>
</div>

## Inflation: Calm and High-Inflation Regimes

Inflation sets the real value of every nominal cash flow. A single mean-reverting process fitted on a calm window cannot produce a 1970s or a 2021: fitted on US data from 2000 to 2019, its 90% band for 2021 ended near 4%, and inflation came in at 7.0%. History instead shows long calm stretches near target, interrupted by spells in which inflation runs far higher and swings more.

<div class="fs-facts">
  <div><span>Series</span><b>CPI inflation over the past year</b></div>
  <div><span>Data</span><b>OECD CPI since 1956</b></div>
  <div><span>Default model</span><b>Calm and high-inflation regimes</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/reference/inflation">Inflation</a></div>
</div>

### The Model

Each regime $$s$$ is the yearly AR(1) of [Wilkie (1986, section 3.4)](https://doi.org/10.1017/S0071368600009009){:target="_blank"} with its own level $$\mu_s$$ and shock size $$\sigma_s$$, and a Markov chain decides each year whether to stay or switch ([Hamilton, 1989, section 2, eq. 2.2, p. 360](https://doi.org/10.2307/1912559){:target="_blank"}; [Harris, 1999, section 2, p. 49](https://doi.org/10.2143/AST.29.1.504606){:target="_blank"}):

$$
I_t = \mu_{s_t} + \phi\,(I_{t-1} - \mu_{s_t}) + \sigma_{s_t}\,\varepsilon_t, \qquad P(s_t = j \mid s_{t-1} = i) = p_{ij}
$$

Here $$I_t$$ is CPI inflation over the past year, $$\phi$$ the share of a gap to the regime's level left after a year, and $$p_{ij}$$ the chance of moving from regime $$i$$ to $$j$$ in a year. Both regimes share $$\phi$$: on US, UK and German inflation since 1956 that fits better by the Bayesian information criterion than a persistence per regime.

The parameters maximise the likelihood from Hamilton's filter (section 4.2, pp. 367-368), started from the long-run shares of the two regimes. Inflation is a year-over-year rate, so neighbouring monthly readings share eleven of their twelve months; the fit therefore pairs each reading with the one a year earlier, twelve interleaved yearly series (every January, every February, ...) run through the filter together. Regime-switching likelihoods have several local maxima ([Harris, 1999, section 1, p. 48](https://doi.org/10.2143/AST.29.1.504606){:target="_blank"}), so the fit starts from three points and keeps the best. In the simulation each regime becomes the monthly Ornstein-Uhlenbeck process with the same yearly behaviour, and the switching chances are rescaled to the month through the matrix's generator ([Israel, Rosenthal and Wei, 2001, section 2, p. 247](https://doi.org/10.1111/1467-9965.00114){:target="_blank"}).

The chart shows the fit on each country's OECD inflation since 1956. The shaded months are those the filter puts in the high regime: the 1970s and early 1980s everywhere, 1990-91 in Germany and the UK, and 2021-2023.

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/economy/inflation-regimes" alt="US, German and UK CPI inflation since 1956 with the months in the high-inflation regime shaded and the two regime levels" %}

The fitted parameters per country:

| Fitted on OECD CPI since 1956 | United States | Germany (euro) | United Kingdom |
|:--|--:|--:|--:|
| Data | Monthly, 849 readings | Quarterly, 283 readings | Monthly, 848 readings |
| Calm level $$\mu_0$$, as fitted | 2.55% | 1.73% | 2.57% |
| High level $$\mu_1$$ | 7.92% | 6.35% | 11.73% |
| Persistence $$\phi$$ (a year) | 0.52 | 0.40 | 0.53 |
| Shock size, calm / high | 1.09% / 2.96% | 0.89% / 1.11% | 1.25% / 4.52% |
| Chance of staying a year, calm / high | 0.93 / 0.72 | 0.92 / 0.67 | 0.93 / 0.79 |
| Average spell, calm / high (years) | 13.9 / 3.5 | 12.5 / 3.0 | 14.5 / 4.8 |
| Long-run share of the high regime | 20% | 19% | 25% |
| Long-run median, as fitted | 3.12% | 2.26% | 3.52% |

In the US and the UK the high regime's shocks are 2.7 and 3.6 times the calm regime's, in line with [Harris (1999, section 4, Table 2, p. 57)](https://doi.org/10.2143/AST.29.1.504606){:target="_blank"}, who finds a turbulent regime about three times as volatile in Australian data; Germany's high-inflation spells were steadier, 1.2 times.

### Anchoring the Median to Expectations

As fitted, the long-run median sits where history's average decades put it: 3.12% for the US and 3.52% for the UK, above what anyone expects today. The default moves the calm regime's level, and nothing else, so that the long-run median equals today's long-run expectation for the country. The high regime's level and shock sizes, the persistence and the switching chances stay as fitted, so the chance and the shape of a 1970s-style spell are history's.

The median rather than the mean is matched because a survey reports point forecasts, a typical outcome, while rare high-inflation spells skew the distribution: its mean sits above its median by the spikes. The long-run distribution is computed rather than simulated: the inflation axis is cut into bins an eighth of a month's shock wide, the chain the simulation steps is written as a transition matrix between (bin, regime) states, and its stationary vector is solved directly. On the US fit its median is within two basis points of 100,000 simulated 60-year paths.

The chart shows the long-run distribution as fitted and after anchoring, with the medians:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/economy/inflation-stationary" alt="The long-run distribution of inflation as fitted and after anchoring, with the medians, for the US, Germany and the UK" %}

Each anchor is a published long-run expectation or target:

| Anchor | Value | Kind | Source |
|:--|:--|:--|:--|
| United States | 2.3% | Sourced | Headline CPI inflation over 2026-2035, the median of 25 forecasters in the [Survey of Professional Forecasters, Federal Reserve Bank of Philadelphia (2026Q3, p. 4; p. 18, Table Eight)](https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/survey-of-professional-forecasters/2026/spfq326.pdf){:target="_blank"}; their mean is 2.43% |
| Euro area (Germany) | 2.0% | Sourced | Longer-term (2031) HICP expectation, [ECB Survey of Professional Forecasters (2026Q3, press release of 24 July 2026)](https://www.ecb.europa.eu/press/pr/date/2026/html/ecb.pr260724~a099353951.en.html){:target="_blank"}; the euro-area survey stands in for Germany, whose CPI has no survey of its own |
| United Kingdom | 2% | Sourced | The Bank of England's CPI target, [HM Treasury (2025, remit letter, paragraph 4)](https://www.gov.uk/government/publications/monetary-policy-remit-budget-2025/letter-from-chancellor-of-the-exchequer-to-govenor-of-the-bank-of-england){:target="_blank"}; the UK has no comparable long-horizon survey |

The chart shows the long-run inflation expectations of professional forecasters in the US and the euro area since 1991 and 1999:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/economy/inflation-expectations" alt="Long-run inflation expectations of professional forecasters in the US and the euro area since 1991 and 1999" %}

After anchoring, the calm levels are 1.66%, 1.46% and 0.92% and the medians meet their anchors. The spikes keep the long-run mean above the median, as they did in history:

<div class="ca-nums fs-nums">
  <span><b>2.93%</b>US long-run mean</span>
  <span><b>2.40%</b>German long-run mean</span>
  <span><b>3.61%</b>UK long-run mean</span>
</div>

The share of scenarios in the high regime moves toward its long-run value by $$p_{00} + p_{11} - 1$$ a year (0.65 for the US), so a run that starts calm reaches the long-run mix within a few years.

### How Each Number Is Set

Every number in the inflation model, and where it comes from:

| Number | Value | Kind | Why |
|:--|:--|:--|:--|
| Regimes | 2 | Judgement | Calm and high inflation; US inflation since 1956 holds one long high-inflation episode, too few to separate a third regime |
| Shared persistence | One $$\phi$$ for both regimes | Judgement | Fits better by the Bayesian information criterion on US, UK and German inflation since 1956 (in-house fits) |
| History | OECD CPI since 1956 | Judgement | The longest official series for all three countries at monthly or quarterly frequency |
| Minimum history | 10 years; a warning below 40 | Judgement | Under 40 years the high regime rests on one or two episodes |
| Regime levels, shocks, persistence, switching | Table above | Fitted | Maximum likelihood, Hamilton's filter |
| Calm level after anchoring | 1.66%, 1.46%, 0.92% | Derived | Solved so the long-run median equals the anchor |
| Anchors | 2.3%, 2.0%, 2% | Sourced | Table above |
| Starting point | Today's inflation and the filter's regime probabilities | Data | OECD inflation since 2000, read through the long-history regimes |

## Unemployment: Expansions and Recessions

Unemployment drives wage-linked benefits, disability claims and credit losses. It does not move like one bell curve of shocks around a trend: it rises fast in recessions and falls slowly in expansions, an asymmetry [Neftçi (1984)](https://doi.org/10.1086/261226){:target="_blank"} and [Sichel (1993)](https://doi.org/10.1111/j.1465-7295.1993.tb00879.x){:target="_blank"} document for the US rate. One normal shock fitted to the average month gives a 2008-09, five points in two years, almost no chance: fitted from 2000 to 2007, the 90% band reached only 6.1% by 2009, when the US rate hit 9.9%.

<div class="fs-facts">
  <div><span>Series</span><b>Unemployment rate per country</b></div>
  <div><span>Data</span><b>OECD, monthly (US from 1956, UK from 1971)</b></div>
  <div><span>Default model</span><b>Expansion and recession regimes</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/reference/unemployment">Unemployment</a></div>
</div>

### The Model (United States and United Kingdom)

Following [Hamilton (1989, section 2, eq. 2.1-2.2)](https://doi.org/10.2307/1912559){:target="_blank"}, who presents his model as an extension of Neftçi's states of rising and falling unemployment (p. 359), each month's change in unemployment is a regression whose intercept and noise depend on an unobserved regime, expansion or recession:

$$
\Delta u_t = c_{s_t} + b\,u_{t-1} + \alpha\,\Delta\pi_t + s_{s_t}\,\varepsilon_t
$$

The pull back to a calm level ($$b < 0$$) and the Phillips-curve term $$\alpha\,\Delta\pi_t$$ of [Ahlgrim, D'Arcy and Gorvett (2005, eq. 3.21)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"} stay in the regression. In a recession the intercept is higher, so unemployment is pushed up by $$D_r$$ a year on top of its pull back. The speed is $$\kappa = -12\ln(1+b)$$ a year, the calm level $$\mu_{\text{calm}} = c_{\text{expansion}}/(-b)$$, and the long-run average lies above the calm level by the recessions' average push:

$$
\mu = \mu_{\text{calm}} + \frac{D_r\,\pi_r}{\kappa}
$$

with $$\pi_r$$ the long-run share of months in recession. The chance of staying in a recession is fixed; the chance of one starting is fixed for the UK and moves with the stock market for the US (below). Maximum likelihood through Hamilton's filter (section 4.2, pp. 367-369) gives every parameter and each month's chance of a recession, from three starting splits of the months (by the sign of the residual, its size, and short recessions), keeping the best.

The NBER's recession dates are no input, yet the regimes line up with them: on US data the fit puts 12% of months in recession, in spells of 7.6 months on average, against 12% of months in NBER recessions since 1955. The chart shows US unemployment with the NBER recessions and the fit's filtered chance of the recession regime:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/economy/unemployment-regimes-us" alt="US unemployment since 1956 with NBER recessions, and the fit's filtered chance of the recession regime" %}

The UK fit on the OECD's record since 1971 finds longer, slower recessions: 18% of months, in spells of 17.2 months. A single mean-reverting fit on that record, with history's volatility, reaches zero in a fifth of 30-year paths; the sharp rises and slow falls of the regimes keep it off the floor. The chart shades the months the fit puts in the recession regime:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/economy/unemployment-regimes-uk" alt="UK unemployment since 1971 with the months in the recession regime shaded, the fitted calm level and the average" %}

### Recessions Are Likelier after a Stock-Market Fall (United States)

The chance of a US recession starting moves with the stock market's return over the past year, the time-varying transition probabilities of [Filardo (1994)](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}, in the logistic form of [Diebold, Lee and Weinbach (1994, section 2)](https://doi.org/10.1093/oso/9780198773917.003.0010){:target="_blank"}, fitted jointly with the regimes by maximum likelihood:

$$
P(\text{recession next month} \mid \text{expansion}) = \frac{1}{1 + e^{-(a + g_R \min(R_t, 0))}}, \qquad R_t = \ln S_{t-3} - \ln S_{t-15} - m_R
$$

$$R_t$$ is the trailing-year log return of Shiller's S&P Composite total-return index ([Shiller, U.S. stock market data](https://shillerdata.com/){:target="_blank"}), ending three months earlier, less its average $$m_R$$; only a shortfall counts. Falling stock prices are one of the financial signs [Estrella and Mishkin (1998)](https://doi.org/10.1162/003465398557320){:target="_blank"} find most useful ahead of a recession. The chance that a recession starts in a given month:

<div class="ca-nums fs-nums">
  <span><b>1.1%</b>with returns at their normal level</span>
  <span><b>5.6%</b>after a year 20% below normal</span>
</div>

In a run, each scenario's own US equity market drives its own chance of a recession.

Every US recession since 1969 followed a bear market or an inverted curve, so a slope fitted by maximum likelihood alone would run off to infinity (separation). The slope therefore carries the default prior of [Gelman, Jakulin, Pittau and Su (2008, sections 2.1-2.2)](https://doi.org/10.1214/08-AOAS191){:target="_blank"}, a Cauchy with scale 2.5 on an input with a standard deviation of 0.5, which is a scale of 1.25 on the unit-variance signal the fit uses; the fit is that posterior's mode.

### Settling at the Official Longer-Run Rate

The FOMC defines its longer-run projections as the values reached in the absence of further shocks ([Summary of Economic Projections, 16 September 2026, note to Table 1](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm){:target="_blank"}). In this model that is the calm level, where unemployment settles in a long expansion. The default therefore moves each fitted process so its calm level equals the official estimate, and keeps the fitted distance from the calm level to the average: the recessions still push the average above it.

The anchored averages, 6.01% for the US and 7.08% for the UK, sit above history's 5.81% since 1956 and 6.61% since 1971: the official longer-run rates are above the calm levels the fits found (3.78% and 3.67%), and the distance from calm level to average is kept as fitted. For the UK that distance is large, 2.9 points, because its recessions last 17.2 months on average and unemployment falls back slowly, at 0.13 a year. The chart compares the fitted and anchored calm levels and the anchored averages, with France for the euro area:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/economy/unemployment-anchor" alt="US, UK and French unemployment with the fitted and anchored calm levels and the anchored averages" %}

### Euro-Area Unemployment {#euro-area-unemployment}

The euro area's unemployment is France's. German unemployment fell structurally after the mid-2000s labour reforms, so a fit on 2000-2026 gives a half-life of about 53 years; France's reverts in a few years, closer to the euro area's own cycle. It is the mean-reverting model of [Ahlgrim, D'Arcy and Gorvett (2005, eq. 3.19)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"} with a Phillips-curve term ([Phillips, 1958](https://doi.org/10.1111/j.1468-0335.1958.tb00003.x){:target="_blank"}), fitted quarterly since 2000:

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

### How Each Number Is Set

Every number in the US and UK unemployment models, and where it comes from:

| Number | United States | United Kingdom | Kind | Why |
|:--|--:|--:|:--|:--|
| History | OECD, monthly from 1956-02 | OECD, monthly from 1971-03 | Data | The longest official monthly records |
| Months left out | March-December 2020 | March-December 2020 | Judgement | The lockdown and reopening stay out of the likelihood, while the filter carries the regime probabilities through them, as [Lenza and Primiceri (2022, sections 1 and 4)](https://doi.org/10.1002/jae.2895){:target="_blank"} find acceptable for estimating parameters. Kept in, April 2020's ten-point jump turns the recession regime into a 2% outlier regime of three-month spells |
| Minimum history | 240 months | 240 months | Judgement | Fewer hold too few recessions to time two regimes on |
| Speed $$\kappa$$, per year | 0.24 | 0.13 | Fitted | |
| Recession push $$D_r$$, per year | 3.44 points | 2.14 points | Fitted | |
| Volatility, expansion / recession | 0.52% / 0.74% | 0.29% / 0.27% | Fitted | |
| Chance a recession lasts another month | 0.869 | 0.942 | Fitted | |
| Share of months in recession | 12% | 18% | Fitted | |
| Phillips sensitivity $$\alpha$$ | -0.031 | -0.013 | Fitted | |
| Equity link, slope on the shortfall | -7.57 on the log-odds per unit of log-return shortfall | none | Fitted | Shiller's index is the only keyless monthly equity history long enough |
| Equity window lag | 3 months | | Judgement | The lag that fits US data 1969-2025 best: R² of 0.43 at three months, 0.42 at none and 0.35 at six, in the yearly regression of unemployment's change on the past year's equity return |
| Prior scale on the slope | 1.25 | | Sourced | [Gelman et al. (2008, sections 2.1-2.2)](https://doi.org/10.1214/08-AOAS191){:target="_blank"} |
| Calm level, fitted | 3.78% | 3.67% | Fitted | |
| Calm level, anchored | 4.2% | 4.21% | Sourced | FOMC longer-run median ([SEP, 16 September 2026, Table 1](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm){:target="_blank"}); the European Commission's NAWRU for 2027 ([AMECO ZNAWRU, Spring 2026](https://ec.europa.eu/economy_finance/ameco/wq/series?fullVariable=1.0.0.0.ZNAWRU&countries=FRA,GBR,DEU&years=2027&lastYear=0&yearOrder=ASC){:target="_blank"}) |
| Long-run average, anchored | 6.01% | 7.08% | Derived | The anchor plus the fitted distance from calm level to average |

## Run It

The default settings calibrate and simulate both models, and the run can be checked against history's extremes:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(api_key="FINANCIAL_MODELING_PREP_KEY")  # the default settings and factor set
calibration = scenarios.calibrate()

calibration.calibrated_params["united_states_inflation"]  # regime levels, shocks, persistence, switching, the anchor
calibration.calibrated_params["united_states_unemployment"]  # speed, average, and the expansion and recession regimes

result = scenarios.simulate(calibration=calibration, n_simulations=2000, seed=42)
scenarios.check_realism(result)  # how often the scenarios reach history's extremes, such as inflation above 5%
```

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">Your own long-run view</p>

A long-run belief on a regime-switching inflation entry moves both regime levels so the median meets the belief; a path moves it over time. See the [regimes page](/projects/financescenarios/docs/regimes).
</div>

## Other Inflation Models

**Mean reversion to one level.** Inflation as an Ornstein-Uhlenbeck process ([Uhlenbeck and Ornstein, 1930, section 5, pp. 827-828](https://doi.org/10.1103/PhysRev.36.823){:target="_blank"}), $$d\pi_t = a(\theta - \pi_t)\,dt + \sigma\,dW_t$$, fitted on readings a year apart as [Ahlgrim, D'Arcy and Gorvett (2005, section 3, p. 15)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf#page=15){:target="_blank"} do, with optional GARCH volatility ([Bollerslev, 1986, section 3, eq. 8, p. 311](https://doi.org/10.1016/0304-4076(86)90063-1){:target="_blank"}) or a long history (UK inflation from 1210, US from 1872).

**Wilkie's AR(1).** The discrete yearly model of [Wilkie (1986, section 3.4)](https://doi.org/10.1017/S0071368600009009){:target="_blank"}, the top of his cascade of dividend yield, dividend growth and consols.

**Hibbert's two-factor model.** Inflation reverts to a slower-moving expected-inflation level ([Hibbert, Mowbray and Turnbull, 2001, section 5.1.2, p. 19](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf#page=19){:target="_blank"}).

**Market-implied inflation (risk-neutral).** To value inflation-linked cash flows at market prices, inflation moves around today's breakeven curve, a Nelson-Siegel fit ([Nelson and Siegel, 1987](https://doi.org/10.1086/296409){:target="_blank"}; [Diebold and Li, 2006](https://doi.org/10.1016/j.jeconom.2005.03.005){:target="_blank"}) to the nominal less the inflation-linked yields:

$$
\pi_t = f_{BE}(t) - \frac{\sigma^2}{2a^2}\left(1 - e^{-at}\right)^2 + y_t, \qquad dy_t = -a\,y_t\,dt + \sigma\,dW_t, \quad y_0 = 0
$$

The convexity term keeps the expected price index on the breakeven curve, so a plain inflation-linked cash flow is valued at the market's breakeven while a cap or floor on indexation gets a time value from the country's historical speed and volatility. Before the first quoted maturity the curve holds the fitted breakeven there flat, EIOPA's constant-forward rule before the first quoted maturity of its risk-free curve ([RFR Technical Documentation, EIOPA-BoS-26/198, Annex D.8](https://www.eiopa.europa.eu/eiopa-publishes-rfr-technical-documentation-become-applicable-30-january-2027-2026-05-26_en){:target="_blank"}). The breakevens come from:

| Market | Source | Maturities | Index |
|:--|:--|:--|:--|
| United States | US Treasury, nominal minus TIPS | 5 to 30 years | US CPI |
| United Kingdom | Bank of England implied inflation curve | 3 to 40 years | RPI |
| Germany / euro area | Bundesbank, nominal minus inflation-linked | 5 to 15 years | Euro area HICP ex tobacco |

**Links.** Inflation can respond to the same step's move in a paired short rate or in the leading indicator; for rates and inflation that drive each other, fitted jointly, use the [KNW model](/projects/financescenarios/docs/knw).

<div class="fs-ref"><a href="/projects/financescenarios/docs/reference/inflation"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Inflation</a></div>

<div class="fs-ref"><a href="/projects/financescenarios/docs/reference/unemployment"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Unemployment</a></div>

## The Leading Indicator and the Business Cycle

The leading indicator gives the model an explicit business cycle, so other factors move with booms and slowdowns, not only through average correlations. It is the OECD Composite Leading Indicator for about 22 countries and country groups, designed to turn ahead of the economy and published detrended around 100, simulated as a mean-reverting process.

<div class="fs-facts">
  <div><span>Series</span><b>OECD Composite Leading Indicator</b></div>
  <div><span>Coverage</span><b>About 22 countries and groups</b></div>
  <div><span>Model</span><b>Mean reversion</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/reference/leading-indicator">Leading indicator</a></div>
</div>

To add the US leading indicator to a factor set:

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
leading_indicator:
  enabled: true
  country: United States
```

For interest rates, inflation, real estate growth, credit spreads, commodity prices and dividend yields, the step-to-step change in the indicator can enter the drift, $$dX_t = a(\theta - X_t)\,dt + \beta\,dL_t + \sigma\,dW_t$$, with $$\beta$$ fitted from history, so a simulated downturn widens spreads and lowers rates on the same path. Unemployment can add it next to inflation, and equity regimes can switch with its level through the time-varying transition probabilities of [Filardo (1994)](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}.

<div class="fs-callout" markdown="1">
The default factor set leaves these links off: its rates, unemployment and equities are tied together through the Taylor rule, the equity link and inflation instead.
</div>

<div class="fs-ref"><a href="/projects/financescenarios/docs/reference/leading-indicator"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Leading indicator</a></div>

## Mortality and Longevity

Longevity risk is the risk that people live longer than a pension fund or annuity provider expected. Mortality has fallen for decades, but not at a steady pace; that uncertain trend is what this factor captures. It is opt-in.

<div class="fs-facts">
  <div><span>Series</span><b>One-year death probabilities by age</b></div>
  <div><span>Data</span><b>Eurostat, or your own life table</b></div>
  <div><span>Model</span><b>Cairns-Blake-Dowd, two factors</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/reference/mortality">Mortality</a></div>
</div>

Finance Scenarios uses the two-factor model of [Cairns, Blake and Dowd (2006)](https://doi.org/10.1111/j.1539-6975.2006.00195.x){:target="_blank"}:

$$
\operatorname{logit} q(x,t) = \kappa_1(t) + \kappa_2(t)\,(x - \bar{x})
$$

Here $$q(x,t)$$ is the one-year probability of death at age $$x$$ in year $$t$$ and $$\bar{x}$$ the mean of the fitted ages. $$\kappa_1$$ is the level and $$\kappa_2$$ the age slope. Mortality improvement is a sustained trend, so each is a random walk with drift, as in [Cairns, Blake and Dowd (2006, p. 692, eq. 2)](https://www.pensions-institute.org/wp-content/uploads/2019/workingpapers/wp0611.pdf#page=7){:target="_blank"}:

$$
\kappa_i(t+1) = \kappa_i(t) + \mu_i + \sigma_i\,z_i(t)
$$

A fit on 40 years (1985 to 2024) of German population death probabilities, at every fourth age from 60 to 84, gave a level drift of -0.014: death rates fall roughly 1.4% a year at every age.

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
mortality:
  enabled: true
  source: eurostat
  country: Germany
  min_age: 60
  max_age: 84
```

Life tables come from Eurostat (from 1960 for most countries of the European Economic Area) or from your own table of one-year death probabilities ($$q_x$$, not central death rates), for example from the [Human Mortality Database](https://www.mortality.org/){:target="_blank"}.

<div class="fs-callout fs-callout--limits" markdown="1">
<p class="fs-callout__title">Limits</p>

- No cohort effects and no Lee-Carter alternative.
- The straight-line shape holds only near the fitted ages.
</div>

<div class="fs-ref"><a href="/projects/financescenarios/docs/reference/mortality"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Mortality</a></div>

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">17</span></summary>

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. [casact.org](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." Journal of Econometrics, 31(3), 307-327. [doi.org](https://doi.org/10.1016/0304-4076(86)90063-1){:target="_blank"}
- Cairns, A.J.G., Blake, D., Dowd, K. (2006). "A Two-Factor Model for Stochastic Mortality with Parameter Uncertainty: Theory and Calibration." Journal of Risk and Insurance, 73(4), 687-718. [doi.org](https://doi.org/10.1111/j.1539-6975.2006.00195.x){:target="_blank"}
- Diebold, F.X., Lee, J.-H., Weinbach, G.C. (1994). "Regime Switching with Time-Varying Transition Probabilities." In Hargreaves, C. (ed.), Nonstationary Time Series Analysis and Cointegration, 283-302. [doi.org](https://doi.org/10.1093/oso/9780198773917.003.0010){:target="_blank"}
- Estrella, A., Mishkin, F.S. (1998). "Predicting U.S. Recessions: Financial Variables as Leading Indicators." Review of Economics and Statistics, 80(1), 45-61. [doi.org](https://doi.org/10.1162/003465398557320){:target="_blank"}
- European Central Bank (2026). Survey of Professional Forecasters, third quarter of 2026, press release of 24 July 2026. [ecb.europa.eu](https://www.ecb.europa.eu/press/pr/date/2026/html/ecb.pr260724~a099353951.en.html){:target="_blank"}
- Federal Reserve Bank of Philadelphia (2026). Survey of Professional Forecasters, third quarter 2026. [philadelphiafed.org](https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/survey-of-professional-forecasters/2026/spfq326.pdf){:target="_blank"}
- Filardo, A.J. (1994). "Business-Cycle Phases and Their Transitional Dynamics." Journal of Business & Economic Statistics, 12(3), 299-308. [doi.org](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}
- Gelman, A., Jakulin, A., Pittau, M.G., Su, Y.-S. (2008). "A Weakly Informative Default Prior Distribution for Logistic and Other Regression Models." The Annals of Applied Statistics, 2(4), 1360-1383. [doi.org](https://doi.org/10.1214/08-AOAS191){:target="_blank"}
- Hamilton, J.D. (1989). "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle." Econometrica, 57(2), 357-384. [doi.org](https://doi.org/10.2307/1912559){:target="_blank"}
- Harris, G.R. (1999). "Markov Chain Monte Carlo Estimation of Regime Switching Vector Autoregressions." ASTIN Bulletin, 29(1), 47-79. [doi.org](https://doi.org/10.2143/AST.29.1.504606){:target="_blank"}
- Israel, R.B., Rosenthal, J.S., Wei, J.Z. (2001). "Finding Generators for Markov Chains via Empirical Transition Matrices, with Applications to Credit Ratings." Mathematical Finance, 11(2), 245-265. [doi.org](https://doi.org/10.1111/1467-9965.00114){:target="_blank"}
- Lenza, M., Primiceri, G.E. (2022). "How to Estimate a Vector Autoregression after March 2020." Journal of Applied Econometrics, 37(4), 688-699. [doi.org](https://doi.org/10.1002/jae.2895){:target="_blank"}
- Neftçi, S.N. (1984). "Are Economic Time Series Asymmetric over the Business Cycle?" Journal of Political Economy, 92(2), 307-328. [doi.org](https://doi.org/10.1086/261226){:target="_blank"}
- Phillips, A.W. (1958). "The Relation Between Unemployment and the Rate of Change of Money Wage Rates in the United Kingdom, 1861-1957." Economica, 25(100), 283-299. [doi.org](https://doi.org/10.1111/j.1468-0335.1958.tb00003.x){:target="_blank"}
- Sichel, D.E. (1993). "Business Cycle Asymmetry: A Deeper Look." Economic Inquiry, 31(2), 224-236. [doi.org](https://doi.org/10.1111/j.1465-7295.1993.tb00879.x){:target="_blank"}
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. [doi.org](https://doi.org/10.1017/S0071368600009009){:target="_blank"}

</details>
