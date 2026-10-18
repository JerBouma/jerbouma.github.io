---
title: Interest Rates and Yield Curves
seo_title: "Interest Rates Documentation | Finance Scenarios"
seo_title_suffix: false
excerpt: "How the default model sets interest rates: a Taylor-rule short rate with each central bank's floor, a long rate built from the expected short-rate path plus a fitted term premium, and how every number behind them is derived from data."
description: "The Taylor-rule short rate and expected-path long rate of Finance Scenarios: the theory, the sourced and fitted numbers, the charts that derive them, and the other rate models."
author_profile: false
permalink: /projects/financescenarios/docs/interest-rates
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Interest rates discount liabilities, drive bond returns and set the risk-free rate every equity earns on top of. In the default model each currency has two rates that move together the way central banks and bond markets make them move: a short rate that follows a monetary-policy rule on the simulated inflation and unemployment, and a 10-year rate built on that short rate as its expected path plus a term premium.

This page explains the theory behind both, then derives every number they use: what it is, whether it comes from a published source, from a fit on data or from a judgement, and the chart that shows it. The other rate models (Hull-White, CIR, Wilkie, Hibbert, Nelson-Siegel curves, HJM) are summarised at the end. Argument lists are in the reference pages for [InterestRates](/projects/financescenarios/docs/reference/interest-rates) and the [configuration classes](/projects/financescenarios/docs/reference/configuration-classes).

The numbers below come from one calibration of the default settings and factor set, made on 17 October 2026, the same one the README and the example notebooks use.

<div class="ca-nav">
  <a href="#the-short-rate-follows-a-taylor-rule"><i class="fas fa-landmark" aria-hidden="true"></i>Short rate</a>
  <a href="#the-long-rate-is-the-expected-short-rate-path-plus-a-term-premium"><i class="fas fa-chart-line" aria-hidden="true"></i>Long rate</a>
  <a href="#data-choices"><i class="fas fa-database" aria-hidden="true"></i>Data choices</a>
  <a href="#run-it"><i class="fas fa-terminal" aria-hidden="true"></i>Run it</a>
  <a href="#other-rate-models"><i class="fas fa-layer-group" aria-hidden="true"></i>Other rate models</a>
</div>

## The Short Rate Follows a Taylor Rule

A short rate that reverts to one fixed level ignores why rates move: central banks raise them when inflation runs above target and cut them when unemployment rises. A rule makes that link explicit, so a scenario with an inflation surge also has rising rates, and a recession has falling ones.

<div class="fs-facts">
  <div><span>Series</span><b>The 3-month rate of each currency</b></div>
  <div><span>Reads</span><b>The scenario's inflation and unemployment</b></div>
  <div><span>Default model</span><b>Taylor rule, reached gradually, with a floor</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/reference/interest-rates">InterestRates</a></div>
</div>

### The Rule

[Taylor (1993, p. 202, eq. 1)](https://doi.org/10.1016/0167-2231(93)90009-L){:target="_blank"} showed that a simple rule tracked the federal funds rate from 1987 to 1992: the neutral real rate plus inflation, plus half of inflation's gap to target, plus half of the output gap. The Federal Reserve's [Monetary Policy Report (2026, Box 4, Table A)](https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-part2.htm){:target="_blank"} writes the same rule with the unemployment gap in place of the output gap, with a weight of 1 through Okun's law (note 3 of the box). That is the rule each scenario follows:

$$
R^*_t = r^* + \pi_t + 0.5\,(\pi_t - \pi^*) - 1.0\,(u_t - u^*)
$$

Here $$\pi_t$$ is the scenario's inflation over the past year, $$\pi^*$$ the 2% target, $$u_t$$ its unemployment rate, $$u^*$$ the unemployment rate the rule treats as neutral and $$r^*$$ the neutral real rate. With inflation 3 points above target, the rule asks for 4.5 points more.

### Gradual Adjustment

Central banks move in steps, not to the rule's rate at once. The Federal Reserve's inertial rule keeps 85% of last quarter's rate and moves 15% of the way to the rule ([Board of Governors of the Federal Reserve System, 2018, table "Examples of Policy Rules"](https://www.federalreserve.gov/monetarypolicy/policy-rules-and-how-policymakers-use-them.htm){:target="_blank"}). Written as a continuous process, the rate closes its gap to the rule at speed $$\kappa = -\ln(0.85)/0.25 = 0.65$$ a year, so a gap halves in about 1.1 years:

$$
s_{t+\Delta t} = R^*_t + (s_t - R^*_t)\,e^{-\kappa \Delta t} + \sigma \sqrt{\frac{1 - e^{-2\kappa\Delta t}}{2\kappa}}\;\varepsilon_t
$$

The shock $$\varepsilon_t$$ is the rate's own surprise, correlated with every other factor, and $$\sigma$$ its size.

### The Floor and the Shadow Rate

A central bank cannot cut much below its lowest rate. The model keeps an unconstrained shadow rate $$s_t$$ that follows the rule, and the observed rate is $$r_t = \max(s_t, \text{ELB})$$, the shadow-rate idea of [Black (1995, section I, p. 1372)](https://doi.org/10.1111/j.1540-6261.1995.tb05182.x){:target="_blank"}. In a deep recession the shadow rate falls well below the floor, so the rate stays there until the rule climbs back above it, as the federal funds rate did from 2008 to 2015.

The chart below runs the rule on each currency's own history since 2000, with the calibrated numbers: the grey line is the rule's prescription, the orange line that prescription reached gradually at 0.65 a year, the blue line the 3-month rate. The reached rule stayed 2.7, 2.1 and 3.4 points from the US, German and UK rate on average (root mean square), against 3.8, 2.9 and 4.3 for the prescription itself. The largest misses are the euro area before 2008, when German inflation and French unemployment called for a lower rate than the ECB set; the United Kingdom after 2008, when the rule called for 3% to 6% while Bank Rate sat at 0.5% or below; and 2021-2023, when the rule called for far higher rates than any of the three central banks set. None of the UK months counts as held at the floor: the UK 3-month rate stayed between 0.5% and 1.2% from 2009 to 2016, above the 0.10% floor plus 25 basis points.

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/taylor-rule" alt="The Taylor rule's prescription, the rule reached gradually and the 3-month rate for the US, the euro area and the UK since 2000" %}

### How Each Number Is Set

Each number in the rule, where it comes from and why it has this value:

| Number | Value | Kind | Why this value |
|:--|:--|:--|:--|
| Inflation-gap weight | 0.5 | Sourced | [Taylor (1993, p. 202, eq. 1)](https://doi.org/10.1016/0167-2231(93)90009-L){:target="_blank"}; [Federal Reserve (2026, Box 4, Table A)](https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-part2.htm){:target="_blank"} |
| Unemployment-gap weight | 1.0 | Sourced | The Taylor rule written with the unemployment gap through Okun's law, [Federal Reserve (2026, Box 4, Table A and note 3)](https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-part2.htm){:target="_blank"}. The balanced-approach rule's 2.0 is an option. |
| Adjustment speed | 0.65 a year | Sourced | The inertial rule's 0.85 of last quarter's rate, [Board of Governors (2018)](https://www.federalreserve.gov/monetarypolicy/policy-rules-and-how-policymakers-use-them.htm){:target="_blank"}. A speed fitted on the US bill rate is unstable: from 1987 to 2012 the slope even turns negative. |
| Inflation target | 2% (USD, EUR, GBP) | Sourced | [FOMC (2026, Statement on Longer-Run Goals, paragraph 4)](https://www.federalreserve.gov/monetarypolicy/files/fomc_longerrungoals.pdf){:target="_blank"}; [ECB (2021, strategy statement, paragraph 5)](https://www.ecb.europa.eu/home/search/review/html/ecb.strategyreview_monpol_strategy_statement.en.html){:target="_blank"}; [HM Treasury (2025, remit letter, paragraph 4)](https://www.gov.uk/government/publications/monetary-policy-remit-budget-2025/letter-from-chancellor-of-the-exchequer-to-govenor-of-the-bank-of-england){:target="_blank"}. The Federal Reserve's 2% refers to PCE prices, which have tended to run a little below the CPI the model reads. |
| Neutral real rate, USD | 1.2% | Sourced | The FOMC's longer-run federal funds rate of 3.2% less its 2% longer-run inflation, [Summary of Economic Projections (16 September 2026, Table 1)](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm){:target="_blank"} |
| Neutral real rate, EUR | 0.09% | Sourced | The Holston-Laubach-Williams estimate for the euro area in 2026Q2, [Federal Reserve Bank of New York (2026, HLW estimates)](https://www.newyorkfed.org/research/policy/rstar){:target="_blank"} |
| Neutral real rate, GBP | 1.0% | Judgement | The midpoint of the Bank of England's range: 2-3% nominal in 2018 plus 25-75 basis points since, less 2% inflation, [Bank of England (2025, Monetary Policy Report February 2025, Box A)](https://www.bankofengland.co.uk/monetary-policy-report/2025/february-2025){:target="_blank"}. The Bank publishes a range, not a point. |
| Floor, USD | 0% | Sourced | The federal funds target range of 0 to 0.25%, 16 December 2008 to 2015 and 16 March 2020 to 2022, [Federal Reserve (open market operations)](https://www.federalreserve.gov/monetarypolicy/openmarket.htm){:target="_blank"} |
| Floor, EUR | -0.50% | Sourced | The ECB's deposit facility rate from 18 September 2019 to 27 July 2022, its lowest, [ECB (key interest rates)](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/html/index.en.html){:target="_blank"} |
| Floor, GBP | 0.10% | Sourced | Bank Rate from 19 March 2020 to 16 December 2021, its lowest, [Bank of England (Bank Rate history)](https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp){:target="_blank"} |
| At the floor | Within 25 basis points | Judgement | Months that start within 25 basis points of the floor (or of zero, if the floor is below it) while the rule prescribed less are left out of the volatility fit: the rate could not follow the rule there. The Federal Reserve's range was 0-0.25%, and a euro rate held at 0% in 2012-2014 was at the floor of the time. |
| Volatility | USD 0.80%, EUR 9.3%, GBP 8.6% a year | Fitted | The standard deviation of each month's change less the part the rule explains, scaled to a yearly Ornstein-Uhlenbeck volatility, on each 3-month rate since 2000. 33 US, 82 euro and 0 UK months held at the floor are left out (shaded in the chart above). |

The neutral real rates come from different kinds of source, and the chart shows both. For the dollar, the FOMC's own longer-run projection: the median has risen from 2.5% in 2019-2023 to 3.2% today. For the euro, the one-sided estimate of the Holston-Laubach-Williams model, which fell from about 2% before 2008 to near zero. For the pound, no official point estimate exists, so the midpoint of the Bank of England's range is a judgement.

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/neutral-rates" alt="The FOMC's longer-run federal funds rate and the neutral real rate it implies since 2012; the euro-area Holston-Laubach-Williams estimate and the UK's 1.0% since 2000" %}

Each floor is the lowest policy rate its central bank has set, and the 3-month rates the model reads sat at or near those floors for years:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/lower-bounds" alt="The US, German and UK 3-month rates since 2000 with each central bank's lowest policy rate" %}

### Which Unemployment Gap the Rule Reads

The rule's $$u^*$$ can be measured three ways, and which one a central bank effectively uses is a judgement:

<div class="ca-cards ca-cards--3">
  <div><i class="ca-icon fas fa-landmark" aria-hidden="true"></i><p class="ca-card-title">Longer-run level</p><p>The official estimate of where unemployment settles: the FOMC's 4.2% for the United States (<a href="https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm" target="_blank">Summary of Economic Projections, 16 September 2026, Table 1</a>) and the European Commission's NAWRU for 2027 elsewhere. That is the textbook gap. But unemployment in the model rises sharply in recessions and settles at that level only in a long expansion, so its average sits above it, and a rule against the longer-run level would hold rates below their steady state on average.</p></div>
  <div><i class="ca-icon fas fa-calculator" aria-hidden="true"></i><p class="ca-card-title">The model's own average</p><p>The gap then averages zero, the way Taylor (1993, p. 202) measured slack against trend real GDP, a path the economy was above in the late 1980s and below in the 1990-91 recession.</p></div>
  <div><i class="ca-icon fas fa-history" aria-hidden="true"></i><p class="ca-card-title">The average less history's gap (the default)</p><p>History says unemployment has averaged a little above its official natural rate. The default sets the neutral unemployment rate to the model's average unemployment less that historical gap, so the simulated gap averages what history's did.</p></div>
</div>

The US gap is the Bureau of Labor Statistics' unemployment rate ([LNS14000000](https://data.bls.gov/timeseries/LNS14000000){:target="_blank"}) less the Congressional Budget Office's noncyclical rate of unemployment ([CBO, Budget and Economic Data](https://www.cbo.gov/data/budget-economic-data){:target="_blank"}), quarter by quarter from 1949Q1 to 2026Q3: it averaged +0.29 points.

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/us-unemployment-gap" alt="US unemployment and the CBO's noncyclical rate since 1949, and the gap between them with its average" %}

For the euro area and the United Kingdom the same gap comes from the European Commission's AMECO database: the unemployment rate (ZUTN) less the NAWRU (ZNAWRU), yearly over every year both exist ([European Commission, AMECO, Spring 2026 forecast](https://ec.europa.eu/economy_finance/ameco/wq/series?fullVariable=1.0.0.0.ZNAWRU&countries=FRA,GBR,DEU&years=2027&lastYear=0&yearOrder=ASC){:target="_blank"}). The euro area's rule reads French unemployment (see [the economy page](/projects/financescenarios/docs/economy#euro-area-unemployment)), so its gap is France's.

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/nawru-gaps" alt="Unemployment and the NAWRU for France, the United Kingdom and Germany, with the average gap" %}

The numbers behind the neutral unemployment rate of each currency:

| Number | Value | Kind | Source |
|:--|:--|:--|:--|
| Longer-run unemployment, US | 4.2% | Sourced | FOMC median, [Summary of Economic Projections (16 September 2026, Table 1)](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm){:target="_blank"} |
| NAWRU 2027: France, UK, Germany | 7.16%, 4.21%, 3.48% | Sourced | [AMECO ZNAWRU, Spring 2026 forecast (3 June 2026)](https://ec.europa.eu/economy_finance/ameco/wq/series?fullVariable=1.0.0.0.ZNAWRU&countries=FRA,GBR,DEU&years=2027&lastYear=0&yearOrder=ASC){:target="_blank"} |
| Historical gap, US | +0.29 points | Derived from data | BLS unemployment less CBO noncyclical rate, quarterly 1949Q1-2026Q3 |
| Historical gap: France, UK, Germany | +0.51, +0.10, +0.04 points | Derived from data | AMECO ZUTN less ZNAWRU, yearly 1965-2025, 1971-2025 and 1991-2025, the years both series cover |
| Which gap | Average less history's gap | Judgement | The simulated gap averages what history's did; the other two are options |
| Resulting $$u^*$$ | US 5.72%, euro 6.65%, UK 6.98% | Derived | Each paired unemployment rate's long-run average (6.01%, 7.16%, 7.08%) less its historical gap |

With inflation at target and unemployment at $$u^*$$, the rule settles at $$r^* + \pi^*$$:

<div class="ca-nums fs-nums">
  <span><b>3.2%</b>dollar</span>
  <span><b>2.09%</b>euro</span>
  <span><b>3.0%</b>pound</span>
</div>

## The Long Rate Is the Expected Short-Rate Path plus a Term Premium

Two rates that each revert on their own, linked only by correlated shocks, let the gap between them wander: a simulated curve can invert at random and stay inverted for decades. Building the long rate on the short rate ties the curve together. The curve then inverts when the short rate jumps and steepens again as it falls back, as it has done historically.

<div class="fs-facts">
  <div><span>Series</span><b>The 10-year rate of each currency</b></div>
  <div><span>Fitted on</span><b>OECD 10-year and 3-month rates, yearly 1950-2025</b></div>
  <div><span>Default model</span><b>Expected short-rate path plus a term premium</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/reference/interest-rates">InterestRates</a></div>
</div>

### The Expected Path

Under the expectations hypothesis, a long yield is the short rate expected over the bond's life, plus a term premium for holding the longer bond ([Campbell and Shiller, 1991, section 2, eq. 1](https://doi.org/10.2307/2298008){:target="_blank"}). If the short rate's gap to its long-run level $$\theta$$ fades at speed $$a$$, the average expected short rate over $$m$$ years is a weighted mix of today's rate and that level, the same weight as in the yield of [Vasicek (1977, section 5, eq. 25)](https://doi.org/10.1016/0304-405x(77)90016-2){:target="_blank"}:

$$
\text{EP}_t = D\,r_t + (1 - D)\,\theta, \qquad D = \frac{1 - e^{-a m}}{a m}
$$

$$D$$ is the share of a short-rate move a 10-year yield carries. In the default, $$\theta$$ is the rule's steady state ($$r^* + \pi^*$$).

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">Two different speeds</p>

The speed $$a$$ in $$D$$ is the short rate's own persistence, not the rule's 0.65. The rule's speed is how fast the rate closes its gap to a target that inflation and unemployment keep moving; how long a gap in the short rate itself lasts, which is what bond markets price, depends on how persistent those drivers are.
</div>

Fitted as a mean-reverting (Hull-White) process on each country's OECD 3-month rate, yearly from 1950 to 2025, the speed is 0.114 a year for the US, 0.192 for Germany and 0.099 for the UK, so a 10-year yield carries 0.60, 0.44 and 0.63 of a short-rate move. The rule's 0.65 would give 0.15.

An outside check: the New York Fed's expected average short rate over ten years, the risk-neutral yield of [Adrian, Crump and Moench (2013, section 2.4)](https://doi.org/10.1016/j.jfineco.2013.04.009){:target="_blank"} (series ACMRNY10, [Federal Reserve Bank of New York, Treasury Term Premia](https://www.newyorkfed.org/research/data_indicators/term-premia-tabs){:target="_blank"}), moves 0.59 for every point the 3-month bill moves, monthly from June 1961 to September 2026. The US weight of 0.60 is close to it.

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/expected-path-weight" alt="The weight of today's short rate in the 10-year expected path against the short rate's speed, with each country's fitted speed and the New York Fed's estimate" %}

### The Term Premium

What is left of the long rate after the expected path is the term premium, $$\text{TP}_t = L_t - \text{EP}_t$$. It reverts toward a long-run level, moves with the short rate's gap to its own level, and responds to the short rate's change in the same step:

$$
\text{TP}_{t+1} = c + \phi\,\text{TP}_t + \psi\,(r_t - \theta) + \gamma\,(r_{t+1} - r_t) + e_{t+1}
$$

One least-squares regression on each country's OECD 10-year and 3-month rates, yearly from 1950 to 2025, gives every parameter: the speed $$\kappa = -\ln\phi$$, the long-run premium $$\tau = c/(1-\phi)$$ (the premium when the short rate sits at its level), the sensitivity $$\beta = \psi/(1-\phi)$$, the same-step response $$\gamma$$ and the volatility $$\sigma$$ of the residual, scaled to a yearly Ornstein-Uhlenbeck volatility.

| Parameter | United States | Germany (euro) | United Kingdom | Kind |
|:--|--:|--:|--:|:--|
| Expected-path speed $$a$$, per year | 0.114 | 0.192 | 0.099 | Fitted, OECD 3-month rate 1950-2025 |
| Weight $$D$$ (10 years) | 0.60 | 0.44 | 0.63 | Derived from $$a$$ |
| Long-run premium $$\tau$$ | 1.34% | 0.94% | 1.03% | Fitted |
| Sensitivity to the short rate's gap $$\beta$$ | 0.42 | 0.59 | 0.27 | Fitted |
| Same-step response $$\gamma$$ | -0.11 | -0.08 | -0.25 | Fitted |
| Premium's speed $$\kappa$$, per year | 0.36 | 0.22 | 0.18 | Fitted |
| Premium's volatility $$\sigma$$ | 0.60% | 0.63% | 0.80% | Fitted |
| Years in the fit | 76 | 76 | 76 | |

The chart splits each country's 10-year yield into the expected path and the premium. The premium was largest from the mid-1970s to the early 1990s, when holding a long bond meant carrying inflation risk, and near or below zero around 2020; Germany's was also large in the 1950s and 1960s. Each premium averages more than its $$\tau$$ because the short rate averaged above the rule's steady state over these years, and $$\beta$$ adds to the premium when it does.

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/long-rate-decomposition" alt="OECD 10-year and 3-month rates since 1950 with the expected-path component and the term premium for the US, Germany and the UK" %}

The US premium can be set against the New York Fed's, which comes from a five-factor no-arbitrage model of the whole Treasury curve rather than from two rates. Over 1962-2025 the two correlate 0.96 in yearly averages. Ours averages 1.87% against ACM's 1.45%; the fitted long-run premium $$\tau$$ is 1.34%. The same-step response matches too: ACM's premium falls 0.12 for every point the 3-month bill rises, in yearly-average changes from 1962 to 2025, against our $$\gamma$$ of -0.11 for the US.

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/term-premium-acm" alt="The fitted US 10-year term premium against the New York Fed's ACM term premium, yearly 1962-2025" %}

### In the Simulation

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

Which data each rate is fitted on, and why:

| Choice | Kind | Why |
|:--|:--|:--|
| The US short rate is the 13-week Treasury bill (^IRX), monthly | Judgement | A market rate the policy rate drives, daily and keyless; [Ahlgrim, D'Arcy and Gorvett (2005, section 3)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"} likewise use the three-month Treasury rate for the short rate |
| The euro area's rates are Germany's (OECD, monthly) | Judgement | The euro area's largest economy and its benchmark Bund |
| The euro area's rule reads German inflation (quarterly) and French unemployment | Judgement | German unemployment fell structurally after the mid-2000s labour reforms; see [the economy page](/projects/financescenarios/docs/economy#euro-area-unemployment) |
| The term premium and the expected-path speed are fitted on the OECD's yearly rates since 1950 | Judgement | Seventy-six years hold the high-inflation decades, the low-rate 2010s and the 2022 rise; a window since 2000 holds one rate cycle |
| The rule's volatility and every starting value come from data since 2000 | Judgement | The settings' calibration window: two full bear markets (2000-02, 2008-09) and the sector ETFs' history |

## Run It

The default profiles calibrate and simulate everything above; the fitted parameters and the calibration notes show each number.

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(api_key="FINANCIAL_MODELING_PREP_KEY")  # the default settings and factor set
calibration = scenarios.calibrate()

calibration.calibrated_params["united_states_short_rate"]  # the rule: weights, neutral rate, target, floor, speed, volatility
calibration.calibrated_params["united_states_long_rate"]  # the expected-path speed and the term premium
calibration.calibration_notes["united_states_long_rate"]  # where the expected-path speed comes from

result = scenarios.simulate(calibration=calibration, n_simulations=2000, seed=42)
scenarios.check_relationships(result)  # does the 10-year move with the short rate the way it has in history?
```

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">Your own views</p>

A belief replaces a number for your own view. A belief on the neutral real rate moves where the rule settles, a path of long-run levels prescribes the short rate for a while (as a supervisory stress scenario prescribes the policy rate), and a belief on the term premium sets the long-run premium; see the [regimes page](/projects/financescenarios/docs/regimes) and the [configuration reference](/projects/financescenarios/docs/reference/configuration-classes).
</div>

## Other Rate Models

The default is one choice among several; each of these is an option on an interest rate in the factor set or a factor of its own.

**Hull-White (Vasicek).** The rate reverts to one long-run level $$\theta$$ at speed $$a$$ with constant volatility, $$dr_t = a(\theta - r_t)\,dt + \sigma\,dW_t$$ ([Vasicek, 1977](https://doi.org/10.1016/0304-405x(77)90016-2){:target="_blank"}; [Hull and White, 1990](https://doi.org/10.1093/rfs/3.4.573){:target="_blank"}). It is the general-purpose model, supports GARCH volatility ([Bollerslev, 1986, section 3, eq. 8, p. 311](https://doi.org/10.1016/0304-4076(86)90063-1){:target="_blank"}), beliefs, a zero floor, a long history (OECD rates since 1950, UK rates since 1694) and a long-run anchor on EIOPA's forward curve ([Solvency II Directive, Article 77a](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02009L0138-20250117#art_77a){:target="_blank"}). It is also the risk-neutral short rate: with a time-dependent $$\theta$$ that reproduces today's Treasury or EIOPA curve ([Brigo and Mercurio, 2006, section 3.3](https://doi.org/10.1007/978-3-540-34604-3){:target="_blank"}), the curve a Solvency II best estimate discounts with ([Article 77(2)](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02009L0138-20250117#art_77){:target="_blank"}).

**Cox-Ingersoll-Ross.** Shocks scale with the square root of the rate, so rates stay positive when the Feller condition holds and calm down near zero ([Cox, Ingersoll and Ross, 1985, section 3, eq. 17, p. 391](https://doi.org/10.2307/1911242){:target="_blank"}).

**Wilkie consols.** The long yield as expected inflation plus a positive real part, from [Wilkie's (1986, section 3.15)](https://doi.org/10.1017/S0071368600009009){:target="_blank"} actuarial model; it needs long yields above average inflation throughout the fit.

**Hibbert two-factor.** The short rate reverts to a slower-moving rate rather than a fixed level ([Hibbert, Mowbray and Turnbull, 2001, section 5.1.1, p. 15](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf#page=15){:target="_blank"}).

**KNW.** The nominal rate and inflation as one coupled system, with optional shared stochastic volatility; see [KNW models](/projects/financescenarios/docs/knw).

**Nelson-Siegel curves.** A whole government curve as level, slope and curvature factors ([Nelson and Siegel, 1987](https://doi.org/10.1086/296409){:target="_blank"}; [Diebold and Li, 2006, section 3.2](https://doi.org/10.1016/j.jeconom.2005.03.005){:target="_blank"}), each simulated as its own mean-reverting factor, with a corporate spread curve on top; see [TermStructure](/projects/financescenarios/docs/reference/term-structure) and [CreditTermStructure](/projects/financescenarios/docs/reference/credit-term-structure).

**HJM.** An arbitrage-free forward curve whose drift follows from its volatility ([Heath, Jarrow and Morton, 1992, section 4, Proposition 3, p. 86](https://doi.org/10.2307/2951677){:target="_blank"}), with two Hull-White factors (G2++) fitted to how historical forwards moved together; see [Hjm](/projects/financescenarios/docs/reference/hjm).

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">15</span></summary>

- Adrian, T., Crump, R.K., Moench, E. (2013). "Pricing the Term Structure with Linear Regressions." Journal of Financial Economics, 110(1), 110-138. [doi.org](https://doi.org/10.1016/j.jfineco.2013.04.009){:target="_blank"}
- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. [casact.org](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}
- Bank of England (2025). Monetary Policy Report, February 2025, Box A. [bankofengland.co.uk](https://www.bankofengland.co.uk/monetary-policy-report/2025/february-2025){:target="_blank"}
- Black, F. (1995). "Interest Rates as Options." The Journal of Finance, 50(5), 1371-1376. [doi.org](https://doi.org/10.1111/j.1540-6261.1995.tb05182.x){:target="_blank"}
- Board of Governors of the Federal Reserve System (2018). Policy Rules and How Policymakers Use Them. [federalreserve.gov](https://www.federalreserve.gov/monetarypolicy/policy-rules-and-how-policymakers-use-them.htm){:target="_blank"}
- Board of Governors of the Federal Reserve System (2026). Monetary Policy Report, July 2026, Part 2, Box 4. [federalreserve.gov](https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-part2.htm){:target="_blank"}
- Campbell, J.Y., Shiller, R.J. (1991). "Yield Spreads and Interest Rate Movements: A Bird's Eye View." The Review of Economic Studies, 58(3), 495-514. [doi.org](https://doi.org/10.2307/2298008){:target="_blank"}
- Congressional Budget Office (2026). Budget and Economic Data: noncyclical rate of unemployment. [cbo.gov](https://www.cbo.gov/data/budget-economic-data){:target="_blank"}; series NROU on [FRED](https://fred.stlouisfed.org/series/NROU){:target="_blank"}
- European Commission (2026). AMECO, Spring 2026 forecast: ZUTN and ZNAWRU. [ec.europa.eu](https://ec.europa.eu/economy_finance/ameco/wq/series?fullVariable=1.0.0.0.ZUTN&countries=FRA,GBR,DEU&years=2025&lastYear=0&yearOrder=ASC){:target="_blank"}
- Federal Open Market Committee (2026). Summary of Economic Projections, 16 September 2026, Table 1. [federalreserve.gov](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm){:target="_blank"}
- Federal Reserve Bank of New York (2026). Holston-Laubach-Williams estimates of the natural rate of interest. [newyorkfed.org](https://www.newyorkfed.org/research/policy/rstar){:target="_blank"}
- Federal Reserve Bank of New York (2026). Treasury Term Premia (ACMTP10, ACMRNY10). [newyorkfed.org](https://www.newyorkfed.org/research/data_indicators/term-premia-tabs){:target="_blank"}
- Taylor, J.B. (1993). "Discretion versus Policy Rules in Practice." Carnegie-Rochester Conference Series on Public Policy, 39, 195-214. [doi.org](https://doi.org/10.1016/0167-2231(93)90009-L){:target="_blank"}
- U.S. Bureau of Labor Statistics. Unemployment rate, LNS14000000. [bls.gov](https://data.bls.gov/timeseries/LNS14000000){:target="_blank"}
- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. [doi.org](https://doi.org/10.1016/0304-405x(77)90016-2){:target="_blank"}

</details>
