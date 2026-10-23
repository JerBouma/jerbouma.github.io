## How It Works

This page explains the theory of both, then derives every number they use: what it is, whether it comes from a published source, a fit on data or a judgement, and the chart that shows it. The other inflation models, the leading indicator and mortality follow. The numbers come from one calibration of the default settings and factor set, made on 19 October 2026.

### Inflation: Calm and High-Inflation Regimes

Inflation sets the real value of every nominal cash flow. A single mean-reverting process fitted on a calm window cannot produce a 1970s or a 2021: fitted on US data from 2000 to 2019, its 90% band for 2021 ended near 4%, and inflation came in at 7.0%. History instead shows long calm stretches near target, interrupted by spells in which inflation runs far higher and swings more.

<div class="fs-facts">
  <div><span>Series</span><b>CPI inflation over the past year</b></div>
  <div><span>Data</span><b>OECD CPI since 1956 (the UK since 1993)</b></div>
  <div><span>Default model</span><b>Calm and high-inflation regimes</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/economy">Inflation</a></div>
</div>

#### The Model

Each regime $$s$$ is the yearly AR(1) of [Wilkie (1986, section 3.4)](https://doi.org/10.1017/S0071368600009009){:target="_blank"} with its own level $$\mu_s$$ and shock size $$\sigma_s$$, and a Markov chain decides each year whether to stay or switch ([Hamilton, 1989, section 2, eq. 2.2, p. 360](https://doi.org/10.2307/1912559){:target="_blank"}; [Harris, 1999, section 2, p. 49](https://doi.org/10.2143/AST.29.1.504606){:target="_blank"}):

$$
I_t = \mu_{s_t} + \phi\,(I_{t-1} - \mu_{s_t}) + \sigma_{s_t}\,\varepsilon_t, \qquad P(s_t = j \mid s_{t-1} = i) = p_{ij}
$$

Here $$I_t$$ is CPI inflation over the past year, $$\phi$$ the share of a gap to the regime's level left after a year, and $$p_{ij}$$ the chance of moving from regime $$i$$ to $$j$$ in a year. Both regimes share $$\phi$$: on US, UK and German inflation since 1956 that fits better by the Bayesian information criterion than a persistence per regime.

The parameters maximise the likelihood from Hamilton's filter (section 4.2, pp. 367-368), started from the long-run shares of the two regimes. Inflation is a year-over-year rate, so neighbouring monthly readings share eleven of their twelve months; the fit therefore pairs each reading with the one a year earlier, twelve interleaved yearly series (every January, every February, ...) run through the filter together. Regime-switching likelihoods have several local maxima ([Harris, 1999, section 1, p. 48](https://doi.org/10.2143/AST.29.1.504606){:target="_blank"}), so the fit starts from three points and keeps the best. In the simulation each regime becomes the monthly Ornstein-Uhlenbeck process with the same yearly behaviour, and the switching chances are rescaled to the month through the matrix's generator ([Israel, Rosenthal and Wei, 2001, section 2, p. 247](https://doi.org/10.1111/1467-9965.00114){:target="_blank"}).

The chart shows the fit on each country's OECD inflation, the US and Germany since 1956 and the UK since 1993 (below). The shaded months are those the filter puts in the high regime: the 1970s and early 1980s in the US and Germany, 1991-93 in Germany, and 2021-2023 everywhere.

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/economy/inflation-regimes" alt="US and German CPI inflation since 1956 and UK CPI inflation since 1993, with the months in the high-inflation regime shaded and the two regime levels as fitted and anchored" %}

The fitted parameters per country:

| Fitted on OECD CPI | United States | Germany (euro) | United Kingdom |
|:--|--:|--:|--:|
| Data | Monthly since 1956, 849 readings | Quarterly since 1956, 283 readings | Monthly since 1993, 404 readings |
| Calm level $$\mu_0$$, as fitted | 2.55% | 1.73% | 2.00% |
| High level $$\mu_1$$, as fitted | 7.92% | 6.35% | 6.44% |
| Persistence $$\phi$$ (a year) | 0.52 | 0.40 | 0.36 |
| Shock size, calm / high | 1.09% / 2.96% | 0.89% / 1.11% | 0.73% / 2.53% |
| Chance of staying a year, calm / high | 0.93 / 0.72 | 0.92 / 0.67 | 0.94 / 0.55 |
| Average spell, calm / high (years) | 13.9 / 3.5 | 12.5 / 3.0 | 17.9 / 2.2 |
| Long-run share of the high regime | 20% | 19% | 11% |
| Long-run mean, as fitted | 3.64% | 2.62% | 2.49% |
| Long-run median, as fitted | 3.12% | 2.26% | 2.20% |

In the US and the UK the high regime's shocks are 2.7 and 3.5 times the calm regime's, in line with [Harris (1999, section 4, Table 2, p. 57)](https://doi.org/10.2143/AST.29.1.504606){:target="_blank"}, who finds a turbulent regime about three times as volatile in Australian data; Germany's high-inflation spells were steadier, 1.2 times.

#### The UK Is Fitted on Its Inflation-Targeting Era

Inflation's level and persistence depend on the monetary regime: [Benati (2008, section 2.1.1)](https://doi.org/10.1162/qjec.2008.123.3.1005){:target="_blank"} finds inflation persistence high under regimes without a clear nominal anchor and close to zero under inflation targeting, for the UK among others. UK inflation targeting began on 8 October 1992, so the default fits the UK from 1993, its first full year.

The long record does not fit the UK of today. Fitted since 1956, its high regime sits at 11.7% and takes a quarter of the time: a long-run mean of 2% would then need a calm level of &minus;0.28%, normal times with falling prices that the record never shows. Fitted from 1993, the calm level is 2.00% and the high regime, 6.4%, is the 2022-23 surge. On backtests from 2000 to 2022 that read only what was known at each year end, the 1993 fit has the best skill: a CRPS skill of +0.37 against +0.22 for the long record on the 18 origins no choice was made on, and +0.38 against +0.25 on the 14 origins never used for any choice.

That has a cost, stated here because it is real:

<div class="ca-nums fs-nums">
  <span><b>0.63</b>90% coverage on those backtests: the bands are narrow</span>
  <span><b>5.9%</b>highest year-end level in a 30-year scenario, at the median</span>
  <span><b>24.9%</b>highest year-end level in UK history (1975)</span>
</div>

The 1970s are not in the fit, so a default run does not produce them on its own. The bundled stagflation_1970s, energy_war_2022 and inflation_shock_2022 regimes simulate those spells (see the [regimes page](/projects/financescenarios/docs/regimes)). The US and Germany keep their long records: their means meet the anchors with calm levels well above zero.

#### Anchoring the Mean to Expectations

As fitted, the long-run mean sits where history's average decades put it: 3.64% for the US and 2.62% for Germany, above what anyone expects today. The default moves both regime levels by the same amount so that the long-run mean equals today's long-run expectation for the country. The gap between the regimes, their shock sizes, the persistence and the switching chances stay as fitted, so a move into the high regime lifts inflation by as much as it did in history, and the chance and shape of a high-inflation spell are history's.

The mean is matched because that is what the sources measure. The Philadelphia Fed's 10-year forecast is an annual-average rate of inflation over the next ten years ([Survey of Professional Forecasters, 2026Q3, p. 4](https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/survey-of-professional-forecasters/2026/spfq326.pdf){:target="_blank"}), an expected average, and the models this one builds on read their long-run level the same way: [Wilkie's (1986, section 3.4)](https://doi.org/10.1017/S0071368600009009){:target="_blank"} QMU is the mean of his inflation AR(1), and [Ahlgrim, D'Arcy and Gorvett's (2005, section 3)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"} $$\mu_q$$ is the level expected inflation reverts to. With a shared persistence, the long-run mean is the regimes' levels weighted by their long-run shares, $$\pi_0\mu_0 + \pi_1\mu_1$$, so moving both levels by the same amount moves the mean by that amount, in closed form.

Rare high-inflation spells skew the distribution, so its median sits below its mean. The median is kept as a diagnostic only. It is computed rather than simulated: the inflation axis is cut into bins an eighth of a month's shock wide, the chain the simulation steps is written as a transition matrix between (bin, regime) states, and its stationary vector is solved directly. On the US fit its median is within two basis points of 100,000 simulated 60-year paths.

The levels move no lower than a calm level of zero: normal times with falling prices are not in the OECD record of the US, the UK and Germany since 1956. Where a record's high regime is too high or too frequent for the expectation, the calm level stops at zero, the mean stays above the expectation, and the calibration warns.

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

After anchoring, the calm and high levels are 1.21% and 6.59% for the US, 1.10% and 5.73% for Germany, and 1.51% and 5.95% for the UK. The long-run means meet their anchors, and the spikes keep the medians below them, as they did in history:

<div class="ca-nums fs-nums">
  <span><b>1.78%</b>US long-run median (mean 2.30%)</span>
  <span><b>1.63%</b>German long-run median (mean 2.00%)</span>
  <span><b>1.71%</b>UK long-run median (mean 2.00%)</span>
</div>

A 30-year run of 2,000 scenarios reproduces them: over years 10 to 30, US inflation averages 2.32% with a median of 1.80%. The lower calm level has one visible cost: the lowest year-end US inflation in a 30-year scenario is &minus;1.1% at the median, against 0.1% at the end of 2008, the lowest year end since 1956.

The anchor sets where inflation settles in the long run only. Every scenario starts from today's inflation and in a regime drawn from today's probabilities, which the filter reads off the recent data again with the anchored levels: US inflation starts at 3.74% with a 13% chance of being in the high regime. The share of scenarios in the high regime moves toward its long-run value by $$p_{00} + p_{11} - 1$$ a year (0.65 for the US), so a run that starts calm reaches the long-run mix within a few years.

#### Price Indices Compound with ln(1 + π)

Inflation is a year-over-year rate, the growth of the price index over a year. The index a scenario builds from it compounds by the log change of that rate, as [Ahlgrim, D'Arcy and Gorvett (2005, section 3, eq. 3.7)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"} model the price index:

$$
P_{t+\Delta t} = P_t \exp\!\big(\ln(1 + \pi_t)\,\Delta t\big)
$$

so inflation held at 4% gives an index of $$1.04^T$$. Compounding the rate itself, $$\exp(\sum \pi_t\,\Delta t)$$, would overstate a 30-year index by about 1% at 3% inflation. House prices, the price gap behind purchasing power parity and gold's real drift compound the same way (see the [simulation engine](/projects/financescenarios/docs/simulation-engine#price-indices)).

#### How Each Number Is Set

Every number in the inflation model, and where it comes from:

| Number | Value | Kind | Why |
|:--|:--|:--|:--|
| Regimes | 2 | Judgement | Calm and high inflation; US inflation since 1956 holds one long high-inflation episode, too few to separate a third regime |
| Shared persistence | One $$\phi$$ for both regimes | Judgement | Fits better by the Bayesian information criterion on US, UK and German inflation since 1956 (in-house fits); it also makes the long-run mean a closed form |
| History | OECD CPI since 1956; the UK since 1993 | Judgement, sourced for the UK | The longest official series for all three countries at monthly or quarterly frequency; the UK's inflation-targeting era from 1993 ([Benati, 2008](https://doi.org/10.1162/qjec.2008.123.3.1005){:target="_blank"}) |
| Minimum history | 10 years; a warning below 40 | Judgement | Under 40 years the high regime rests on one or two episodes; the UK's 33 years carry that warning |
| Regime levels, shocks, persistence, switching | Table above | Fitted | Maximum likelihood, Hamilton's filter |
| Levels after anchoring | Calm 1.21%, 1.10%, 1.51%; high 6.59%, 5.73%, 5.95% | Derived | Both levels moved by the same amount so the long-run mean equals the anchor, the calm level no lower than zero |
| Anchors | 2.3%, 2.0%, 2% | Sourced | Table above |
| Starting point | Today's inflation and the filter's regime probabilities | Data | OECD inflation since 2000, read through the anchored regimes |

### Unemployment: Expansions and Recessions

Unemployment drives wage-linked benefits, disability claims and credit losses. It does not move like one bell curve of shocks around a trend: it rises fast in recessions and falls slowly in expansions, an asymmetry [Neftçi (1984)](https://doi.org/10.1086/261226){:target="_blank"} and [Sichel (1993)](https://doi.org/10.1111/j.1465-7295.1993.tb00879.x){:target="_blank"} document for the US rate. One normal shock fitted to the average month gives a 2008-09, five points in two years, almost no chance: fitted from 2000 to 2007, the 90% band reached only 6.1% by 2009, when the US rate hit 9.9%.

<div class="fs-facts">
  <div><span>Series</span><b>Unemployment rate per country</b></div>
  <div><span>Data</span><b>OECD, monthly (US from 1956, UK from 1971)</b></div>
  <div><span>Default model</span><b>Expansion and recession regimes</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/economy">Unemployment</a></div>
</div>

#### The Model (United States and United Kingdom)

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

#### Recessions Are Likelier after a Stock-Market Fall (United States)

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

#### Settling at the Official Longer-Run Rate

Where does unemployment settle? The [plucking model of Dupraz, Nakamura and Steinsson (2019, sections 1 and 2.2)](https://doi.org/10.3386/w26351){:target="_blank"} reads the business cycle as rises of unemployment above a floor: recessions pluck it up from a resting point of low unemployment, and it does not swing symmetrically around a natural rate. The FOMC reads its longer-run projections the same way, as the values reached in the absence of further shocks ([Summary of Economic Projections, 16 September 2026, note to Table 1](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm){:target="_blank"}). In this model that is the calm level, where unemployment settles in a long expansion. The default therefore moves each fitted process so its calm level equals the official estimate, and keeps the fitted distance from the calm level to the average: the recessions still push the average above it.

The anchored averages, 6.01% for the US and 7.08% for the UK, sit above history's 5.81% since 1956 and 6.61% since 1971: the official longer-run rates are above the calm levels the fits found (3.78% and 3.67%), and the distance from calm level to average is kept as fitted, 1.8 points for the US and 2.9 for the UK. For the UK that distance is large because its recessions last 17.2 months on average and unemployment falls back slowly, at 0.13 a year.

The other reading takes the official rate as unemployment's average over the cycle, the zero-mean gap the European Commission builds its NAWRU on ([Havik et al., 2014, section 2.4.2](https://ec.europa.eu/economy_finance/publications/economic_paper/2014/pdf/ecp535_en.pdf){:target="_blank"}). It is available as an option (`natural_rate_anchor: average`), but it puts the calm level the whole push below the official rate: 2.4% for the US and 1.3% for the UK on the default fits. US unemployment has not been below 3.4% since the OECD record starts in 1956; it touched 3.4% in 1968-69 and in April 2023. The chart compares both readings, with France for the euro area:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/economy/unemployment-anchor" alt="US, UK and French unemployment with the calm level at the official natural rate, the average over the cycle, and the calm level the average reading would give" %}

Which years the regimes are fitted on matters as well. The Great Moderation from 1984 ([McConnell and Perez-Quiros, 2000](https://doi.org/10.1257/aer.90.5.1464){:target="_blank"}; [Stock and Watson, 2002, section 3](https://doi.org/10.1086/ma.17.3585284){:target="_blank"}) had milder US recessions, so a fit from 1984 has a smaller push. The US choices, scored on 30-year runs (2,000 scenarios, months in years 10 to 30) and on backtests from 2000 to 2022 that read only what was known at each year end (the 18 origins no choice was made on, scored before the backtests waited for each month's first release):

| US regimes fitted on | Official 4.2% is the | Calm level | Average | Months below 3.4% | 90% coverage | CRPS skill |
|:--|:--|--:|--:|--:|--:|--:|
| 1956 on (the default) | Calm level | 4.2% | 6.0% | 2.5% | 0.70 | +0.37 |
| 1984 on | Calm level | 4.2% | 5.7% | 4.3% | 0.62 | +0.37 |
| 1984 on | Average | 2.7% | 4.2% | 26% | 0.70 | +0.43 |

The average reading scores best on the backtests, which mostly start from low unemployment, but a quarter of its months sit below anything the US has seen since 1956, and that is not a scenario set to defend. The shorter sample keeps the calm reading's skill but narrows the bands. The default keeps the whole record with the calm reading; both alternatives stay available (`natural_rate_anchor`, `history_start_year`).

#### Euro-Area Unemployment {#euro-area-unemployment}

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

#### How Each Number Is Set

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
| Equity link, slope on the shortfall | -7.57 on the log-odds per unit of log-return shortfall | none | Fitted | Shiller's index is the only keyless monthly equity history long enough |
| Equity window lag | 3 months | | Judgement | The lag that fits US data 1969-2025 best: R² of 0.43 at three months, 0.42 at none and 0.35 at six, in the yearly regression of unemployment's change on the past year's equity return |
| Prior scale on the slope | 1.25 | | Sourced | [Gelman et al. (2008, sections 2.1-2.2)](https://doi.org/10.1214/08-AOAS191){:target="_blank"} |
| Calm level, fitted | 3.78% | 3.67% | Fitted | |
| Calm level, anchored | 4.2% | 4.21% | Sourced | The official natural rate as the level reached without further shocks ([Dupraz, Nakamura and Steinsson, 2019](https://doi.org/10.3386/w26351){:target="_blank"}): FOMC longer-run median ([SEP, 16 September 2026, Table 1](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm){:target="_blank"}); the European Commission's NAWRU for 2027 ([AMECO ZNAWRU, Spring 2026](https://ec.europa.eu/economy_finance/ameco/wq/series?fullVariable=1.0.0.0.ZNAWRU&countries=FRA,GBR,DEU&years=2027&lastYear=0&yearOrder=ASC){:target="_blank"}) |
| Long-run average, anchored | 6.01% | 7.08% | Derived | The anchor plus the fitted distance from calm level to average |

### Other Inflation Models

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

**Links.** Inflation can respond to the same step's move in a paired short rate or in the leading indicator; for rates and inflation that drive each other, fitted jointly, use the [KNW model](/projects/financescenarios/docs/interest-rates#knw).

<div class="fs-ref"><a href="/projects/financescenarios/docs/economy"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Inflation</a></div>

<div class="fs-ref"><a href="/projects/financescenarios/docs/economy"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Unemployment</a></div>

### The Leading Indicator and the Business Cycle

The leading indicator gives the model an explicit business cycle, so other factors move with booms and slowdowns, not only through average correlations. It is the OECD Composite Leading Indicator for about 22 countries and country groups, designed to turn ahead of the economy and published detrended around 100, simulated as a mean-reverting process.

<div class="fs-facts">
  <div><span>Series</span><b>OECD Composite Leading Indicator</b></div>
  <div><span>Coverage</span><b>About 22 countries and groups</b></div>
  <div><span>Model</span><b>Mean reversion</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/economy">Leading indicator</a></div>
</div>

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
leading_indicator:
  enabled: true
  country: United States
```

For interest rates, inflation, real estate growth, credit spreads, commodity prices and dividend yields, the step-to-step change in the indicator can enter the drift, $$dX_t = a(\theta - X_t)\,dt + \beta\,dL_t + \sigma\,dW_t$$, with $$\beta$$ fitted from history, so a simulated downturn widens spreads and lowers rates on the same path.

Unemployment without regimes can also react to a stock-market fall or a flat yield curve (its cycle links). Those links are fitted in one regression together with the pull back to the average and the Phillips term, not in two steps on the residuals of a first fit: a second-step regression on residuals gives the right slope only when the link is uncorrelated with the first step's regressors, which the Frisch-Waugh-Lovell theorem makes precise ([Frisch and Waugh, 1933](https://doi.org/10.2307/1907330){:target="_blank"}; [Lovell, 1963](https://doi.org/10.1080/01621459.1963.10480682){:target="_blank"}). Unemployment can add it next to inflation, and equity regimes can switch with its level through the time-varying transition probabilities of [Filardo (1994)](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}.

<div class="fs-callout" markdown="1">
The default factor set leaves these links off: its rates, unemployment and equities are tied together through the Taylor rule, the equity link and inflation instead.
</div>

<div class="fs-ref"><a href="/projects/financescenarios/docs/economy"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Leading indicator</a></div>

### Mortality and Longevity

Longevity risk is the risk that people live longer than a pension fund or annuity provider expected. Mortality has fallen for decades, but not at a steady pace; that uncertain trend is what this factor captures. It is opt-in.

<div class="fs-facts">
  <div><span>Series</span><b>One-year death probabilities by age</b></div>
  <div><span>Data</span><b>Eurostat, or your own life table</b></div>
  <div><span>Model</span><b>Cairns-Blake-Dowd, two factors</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/economy">Mortality</a></div>
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

<div class="fs-ref"><a href="/projects/financescenarios/docs/economy"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Mortality</a></div>

### References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">24</span></summary>

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. [casact.org](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}
- Benati, L. (2008). "Investigating Inflation Persistence Across Monetary Regimes." Quarterly Journal of Economics, 123(3), 1005-1060. [doi.org](https://doi.org/10.1162/qjec.2008.123.3.1005){:target="_blank"}
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." Journal of Econometrics, 31(3), 307-327. [doi.org](https://doi.org/10.1016/0304-4076(86)90063-1){:target="_blank"}
- Cairns, A.J.G., Blake, D., Dowd, K. (2006). "A Two-Factor Model for Stochastic Mortality with Parameter Uncertainty: Theory and Calibration." Journal of Risk and Insurance, 73(4), 687-718. [doi.org](https://doi.org/10.1111/j.1539-6975.2006.00195.x){:target="_blank"}
- Diebold, F.X., Lee, J.-H., Weinbach, G.C. (1994). "Regime Switching with Time-Varying Transition Probabilities." In Hargreaves, C. (ed.), Nonstationary Time Series Analysis and Cointegration, 283-302. [doi.org](https://doi.org/10.1093/oso/9780198773917.003.0010){:target="_blank"}
- Dupraz, S., Nakamura, E., Steinsson, J. (2019). "A Plucking Model of Business Cycles." NBER Working Paper 26351. [doi.org](https://doi.org/10.3386/w26351){:target="_blank"}
- Estrella, A., Mishkin, F.S. (1998). "Predicting U.S. Recessions: Financial Variables as Leading Indicators." Review of Economics and Statistics, 80(1), 45-61. [doi.org](https://doi.org/10.1162/003465398557320){:target="_blank"}
- European Central Bank (2026). Survey of Professional Forecasters, third quarter of 2026, press release of 24 July 2026. [ecb.europa.eu](https://www.ecb.europa.eu/press/pr/date/2026/html/ecb.pr260724~a099353951.en.html){:target="_blank"}
- Federal Reserve Bank of Philadelphia (2026). Survey of Professional Forecasters, third quarter 2026. [philadelphiafed.org](https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/survey-of-professional-forecasters/2026/spfq326.pdf){:target="_blank"}
- Filardo, A.J. (1994). "Business-Cycle Phases and Their Transitional Dynamics." Journal of Business & Economic Statistics, 12(3), 299-308. [doi.org](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}
- Frisch, R., Waugh, F.V. (1933). "Partial Time Regressions as Compared with Individual Trends." Econometrica, 1(4), 387-401. [doi.org](https://doi.org/10.2307/1907330){:target="_blank"}
- Gelman, A., Jakulin, A., Pittau, M.G., Su, Y.-S. (2008). "A Weakly Informative Default Prior Distribution for Logistic and Other Regression Models." The Annals of Applied Statistics, 2(4), 1360-1383. [doi.org](https://doi.org/10.1214/08-AOAS191){:target="_blank"}
- Hamilton, J.D. (1989). "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle." Econometrica, 57(2), 357-384. [doi.org](https://doi.org/10.2307/1912559){:target="_blank"}
- Harris, G.R. (1999). "Markov Chain Monte Carlo Estimation of Regime Switching Vector Autoregressions." ASTIN Bulletin, 29(1), 47-79. [doi.org](https://doi.org/10.2143/AST.29.1.504606){:target="_blank"}
- Havik, K., Mc Morrow, K., Orlandi, F., Planas, C., Raciborski, R., Röger, W., Rossi, A., Thum-Thysen, A., Vandermeulen, V. (2014). "The Production Function Methodology for Calculating Potential Growth Rates & Output Gaps." European Economy, Economic Papers 535. [ec.europa.eu](https://ec.europa.eu/economy_finance/publications/economic_paper/2014/pdf/ecp535_en.pdf){:target="_blank"}
- Israel, R.B., Rosenthal, J.S., Wei, J.Z. (2001). "Finding Generators for Markov Chains via Empirical Transition Matrices, with Applications to Credit Ratings." Mathematical Finance, 11(2), 245-265. [doi.org](https://doi.org/10.1111/1467-9965.00114){:target="_blank"}
- Lenza, M., Primiceri, G.E. (2022). "How to Estimate a Vector Autoregression after March 2020." Journal of Applied Econometrics, 37(4), 688-699. [doi.org](https://doi.org/10.1002/jae.2895){:target="_blank"}
- Lovell, M.C. (1963). "Seasonal Adjustment of Economic Time Series and Multiple Regression Analysis." Journal of the American Statistical Association, 58(304), 993-1010. [doi.org](https://doi.org/10.1080/01621459.1963.10480682){:target="_blank"}
- McConnell, M.M., Perez-Quiros, G. (2000). "Output Fluctuations in the United States: What Has Changed Since the Early 1980's?" American Economic Review, 90(5), 1464-1476. [doi.org](https://doi.org/10.1257/aer.90.5.1464){:target="_blank"}
- Neftçi, S.N. (1984). "Are Economic Time Series Asymmetric over the Business Cycle?" Journal of Political Economy, 92(2), 307-328. [doi.org](https://doi.org/10.1086/261226){:target="_blank"}
- Phillips, A.W. (1958). "The Relation Between Unemployment and the Rate of Change of Money Wage Rates in the United Kingdom, 1861-1957." Economica, 25(100), 283-299. [doi.org](https://doi.org/10.1111/j.1468-0335.1958.tb00003.x){:target="_blank"}
- Sichel, D.E. (1993). "Business Cycle Asymmetry: A Deeper Look." Economic Inquiry, 31(2), 224-236. [doi.org](https://doi.org/10.1111/j.1465-7295.1993.tb00879.x){:target="_blank"}
- Stock, J.H., Watson, M.W. (2002). "Has the Business Cycle Changed and Why?" NBER Macroeconomics Annual, 17, 159-218. [doi.org](https://doi.org/10.1086/ma.17.3585284){:target="_blank"}
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. [doi.org](https://doi.org/10.1017/S0071368600009009){:target="_blank"}

</details>
