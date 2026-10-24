---
title: Short Rate
seo_title: "Short Rate | Finance Scenarios"
seo_title_suffix: false
excerpt: "How Finance Scenarios sets the short rate: the Federal Reserve's inertial balanced-approach rule on each scenario's inflation and unemployment, reached gradually, with each central bank's floor, and every number behind it sourced or fitted."
description: "The policy-rule short rate of Finance Scenarios: the Taylor and balanced-approach rules, gradual adjustment, the floor and the shadow rate, the sourced and fitted numbers, and a run with an inflation shock."
author_profile: false
permalink: /projects/financescenarios/docs/interest-rates
classes: wide-sidebar
layout: single
redirect_from:
    - /projects/financescenarios/docs/reference/interest-rates
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-interest-rates"
---

Interest rates discount liabilities, drive bond returns and set the risk-free rate every equity earns on top of. A short rate that reverts to one fixed level ignores why rates move: central banks raise them when inflation runs above target and cut them when unemployment rises. In the default model each currency's 3-month rate therefore follows a monetary-policy rule on the scenario's own inflation and unemployment, so a scenario with an inflation surge also has rising rates, and a recession has falling ones. The rule starts from the path the bond market expects, which has a page of its own: [Expected Path](/projects/financescenarios/docs/interest-rates/expected-path).

<div class="fs-facts">
  <div><span>Series</span><b>The 3-month rate of each currency</b></div>
  <div><span>Reads</span><b>The scenario's inflation and unemployment</b></div>
  <div><span>Default model</span><b>The Fed's inertial rule, from the market's path, with a floor</b></div>
</div>

## The Policy Rule

[Taylor (1993, p. 202, eq. 1)](https://doi.org/10.1016/0167-2231(93)90009-L){:target="_blank"} showed that a simple rule tracked the federal funds rate from 1987 to 1992: the neutral real rate plus inflation, plus half of inflation's gap to target, plus half of the output gap. The balanced-approach rule the Federal Reserve also reports gives the output gap twice that weight, 1 instead of 0.5 ([Board of Governors of the Federal Reserve System, 2018, table "Examples of Policy Rules"](https://www.federalreserve.gov/monetarypolicy/policy-rules-and-how-policymakers-use-them.htm){:target="_blank"}). The [Monetary Policy Report (2026, Box 4, Table A)](https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-part2.htm){:target="_blank"} writes both rules with the unemployment gap in place of the output gap, through Okun's law, which links the two gaps (note 3 of the box): a weight of 1 for Taylor's rule and 2 for the balanced approach. Each scenario follows the balanced-approach rule. As a function of the scenario's inflation and unemployment:

$$
R^*_t = R^*(\pi_t, u_t) = r^* + \pi_t + 0.5\,(\pi_t - \pi^*) - 2.0\,(u_t - u^*)
$$

Here $$\pi_t$$ is the scenario's inflation over the past year, $$\pi^*$$ the 2% target, $$u_t$$ the scenario's unemployment rate, $$u^*$$ the longer-run unemployment rate and $$r^*$$ the neutral real rate. With inflation 3 points above target, the rule asks for 4.5 points more; with unemployment 1 point above its longer-run rate, for 2 points less.

## Gradual Adjustment

Central banks move in steps, not to the rule's rate at once. The Federal Reserve's inertial rule keeps 85% of last quarter's rate and moves 15% of the way to the balanced-approach rule, $$i_t = 0.85\,i_{t-1} + 0.15\,R^*_t$$ for the policy rate $$i_t$$ (the same table of the [Board of Governors, 2018](https://www.federalreserve.gov/monetarypolicy/policy-rules-and-how-policymakers-use-them.htm){:target="_blank"}). The default uses that published rule unchanged. Written as a continuous process, the rate closes its gap to the rule at speed $$\kappa = -\ln(0.85)/0.25 = 0.65$$ a year, so a gap halves in about 1.1 years:

$$
s_{t+\Delta t} = R^*_t + (s_t - R^*_t)\,e^{-\kappa \Delta t} + \sigma \sqrt{\frac{1 - e^{-2\kappa\Delta t}}{2\kappa}}\;\varepsilon_t
$$

Here $$s_t$$ is the scenario's short rate before the floor of the next section, $$\kappa$$ the speed, $$\varepsilon_t$$ the rate's own random shock, correlated with the shocks of every other factor, and $$\sigma$$ its size. The rule reads inflation and unemployment as they stand at the start of each step, as a central bank sets its rate on the latest data. This is the step of a rule that starts from its own path. The default starts from the market's expected path instead, which replaces $$R^*_t$$ with a target built on that path and adds the path's own move to each step (see [Expected Path](/projects/financescenarios/docs/interest-rates/expected-path#the-rule-acts-on-the-surprises)).

## The Floor and the Shadow Rate

A policy rate has a floor, the effective lower bound (ELB): a central bank cannot cut much below it. The model keeps an unconstrained shadow rate $$s_t$$ that follows the rule, and the observed rate is $$r_t = \max(s_t, \text{ELB})$$, the shadow-rate idea of [Black (1995, section I, p. 1372)](https://doi.org/10.1111/j.1540-6261.1995.tb05182.x){:target="_blank"}. In a deep recession the shadow rate falls well below the floor, so the observed rate stays at the floor until the shadow rate climbs back above it, as the federal funds rate did from 2008 to 2015.

Run on each currency's own history since 2000 with the calibrated numbers, the rule reached gradually stayed 1.4, 2.2 and 2.4 points from the US, German and UK rate on average (root mean square), against 2.9, 3.0 and 3.7 for the prescription itself. The largest misses are the euro area and the United Kingdom before 2008, when the rule called for lower rates than the ECB and the Bank of England set; the United Kingdom from 2017 to 2019, when it called for 3% to 4% while Bank Rate stayed below 1%; and 2021 to 2023, when the rule called for far higher rates than any of the three central banks set. The chart shows the rule's prescription (gray line), that prescription reached gradually at 0.65 a year (orange) and the 3-month rate (blue):

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/taylor-rule" alt="The balanced-approach rule's prescription, the rule reached at the inertial speed and the 3-month rate for the US, the euro area and the UK since 2000" %}

## How Each Number Is Set

Each number in the rule, where it comes from and why it has this value:

| Number | Value | Kind | Why this value |
|:--|:--|:--|:--|
| Inflation-gap weight | 0.5 | Sourced | [Taylor (1993, p. 202, eq. 1)](https://doi.org/10.1016/0167-2231(93)90009-L){:target="_blank"}; [Federal Reserve (2026, Box 4, Table A)](https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-part2.htm){:target="_blank"} |
| Unemployment-gap weight | 2.0 | Sourced | The balanced-approach rule inside the Federal Reserve's inertial rule, [Board of Governors (2018)](https://www.federalreserve.gov/monetarypolicy/policy-rules-and-how-policymakers-use-them.htm){:target="_blank"}, written with the unemployment gap through Okun's law, [Federal Reserve (2026, Box 4, Table A and note 3)](https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-part2.htm){:target="_blank"}. Taylor's 1.0 is an option. |
| Adjustment speed | 0.65 a year | Sourced | The inertial rule's 0.85 of last quarter's rate, [Board of Governors (2018)](https://www.federalreserve.gov/monetarypolicy/policy-rules-and-how-policymakers-use-them.htm){:target="_blank"}. A speed fitted on the US bill rate is unstable: from 1987 to 2012 the slope even turns negative. |
| Inflation target | 2% (USD, EUR, GBP) | Sourced | [FOMC (2026, Statement on Longer-Run Goals, paragraph 4)](https://www.federalreserve.gov/monetarypolicy/files/fomc_longerrungoals.pdf){:target="_blank"}; [ECB (2021, strategy statement, paragraph 5)](https://www.ecb.europa.eu/home/search/review/html/ecb.strategyreview_monpol_strategy_statement.en.html){:target="_blank"}; [HM Treasury (2025, remit letter, paragraph 4)](https://www.gov.uk/government/publications/monetary-policy-remit-budget-2025/letter-from-chancellor-of-the-exchequer-to-govenor-of-the-bank-of-england){:target="_blank"}. The Federal Reserve's 2% refers to PCE prices, which have tended to run a little below the CPI the model reads. |
| Neutral real rate, USD | 1.2% | Sourced | The FOMC's longer-run federal funds rate of 3.2% less its 2% longer-run inflation, [Summary of Economic Projections (16 September 2026, Table 1)](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm){:target="_blank"} |
| Neutral real rate, EUR | 0.09% | Sourced | The Holston-Laubach-Williams estimate for the euro area in 2026Q2, [Federal Reserve Bank of New York (2026, HLW estimates)](https://www.newyorkfed.org/research/policy/rstar){:target="_blank"} |
| Neutral real rate, GBP | 1.0% | Judgement | The midpoint of the Bank of England's range: 2-3% nominal in 2018 plus 25-75 basis points since, less 2% inflation, [Bank of England (2025, Monetary Policy Report February 2025, Box A)](https://www.bankofengland.co.uk/monetary-policy-report/2025/february-2025){:target="_blank"}. The Bank publishes a range, not a point. |
| Longer-run unemployment $$u^*$$ | US 4.2%, euro 7.16%, UK 4.21% | Sourced | The FOMC's median, [Summary of Economic Projections (16 September 2026, Table 1)](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm){:target="_blank"}; the European Commission's NAWRU (non-accelerating wage rate of unemployment) for 2027 for France (the euro area's rule reads French unemployment) and the UK, [AMECO ZNAWRU, Spring 2026 forecast](https://ec.europa.eu/economy_finance/ameco/wq/series?fullVariable=1.0.0.0.ZNAWRU&countries=FRA,GBR,DEU&years=2027&lastYear=0&yearOrder=ASC){:target="_blank"} |
| Floor, USD | 0% | Sourced | The federal funds target range of 0 to 0.25%, 16 December 2008 to 2015 and 16 March 2020 to 2022, [Federal Reserve (open market operations)](https://www.federalreserve.gov/monetarypolicy/openmarket.htm){:target="_blank"} |
| Floor, EUR | -0.50% | Sourced | The ECB's deposit facility rate from 18 September 2019 to 27 July 2022, its lowest, [ECB (key interest rates)](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/html/index.en.html){:target="_blank"} |
| Floor, GBP | 0.10% | Sourced | Bank Rate from 19 March 2020 to 16 December 2021, its lowest, [Bank of England (Bank Rate history)](https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp){:target="_blank"} |
| At the floor | Within 25 basis points | Judgement | Months that start within 25 basis points of the floor (or of zero, if the floor is below it) while the rule prescribed less are left out of the volatility fit: the rate could not follow the rule there. The Federal Reserve's range was 0-0.25%, and a euro rate held at 0% in 2012-2014 was at the floor of the time. |
| Volatility | USD 0.89%, EUR 0.81%, GBP 0.82% a year | Fitted | The standard deviation of each month's change less the part the rule explains, scaled to a yearly Ornstein-Uhlenbeck volatility, on each 3-month rate since 2000. 99 US, 96 euro and 7 UK months held at the floor are left out (shaded in the chart above). |

The neutral real rates come from three kinds of source. For the dollar, the FOMC's own longer-run projection: the median has risen from 2.5% in 2019-2023 to 3.2% today. For the euro, the one-sided estimate of the Holston-Laubach-Williams model, which fell from about 2% before 2008 to near zero. For the pound, no official point estimate exists, so the midpoint of the Bank of England's range is a judgement. The chart shows all three over time:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/neutral-rates" alt="The FOMC's longer-run federal funds rate and the neutral real rate it implies since 2012; the euro-area Holston-Laubach-Williams estimate and the UK's 1.0% since 2000" %}

Each floor is the lowest policy rate its central bank has set, and the 3-month rates the model reads sat at or near those floors for years:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/lower-bounds" alt="The US, German and UK 3-month rates since 2000 with each central bank's lowest policy rate" %}

The rule measures labor-market slack from the official longer-run unemployment rate, as the published rules do. Only where no official rate exists does it fall back to the calm level of unemployment, the level recessions push it up from (see [Unemployment](/projects/financescenarios/docs/economy/unemployment#euro-area-unemployment)). On the [market's expected path](/projects/financescenarios/docs/interest-rates/expected-path#the-rule-acts-on-the-surprises), that level cancels out of the rule's target anyway.

With inflation at target and unemployment at $$u^*$$, the rule settles at $$r^* + \pi^*$$, or at the floor if that is higher:

<div class="ca-nums fs-nums">
  <span><b>3.2%</b>dollar</span>
  <span><b>2.09%</b>euro</span>
  <span><b>3.0%</b>pound</span>
</div>

These are the values a run reads today. A calibration as of a past date, which is what every [backtest](/projects/financescenarios/docs/validation/out-of-sample) is, reads each of them as published by that date. The neutral real rate comes from the New York Fed's real-time estimates ([Federal Reserve Bank of New York, r-star](https://www.newyorkfed.org/research/policy/rstar){:target="_blank"}): for the dollar until the FOMC first projected the longer-run federal funds rate in January 2012, and for the pound until the Bank of England published its range in 2018. The longer-run unemployment rate and the NAWRU come from the projections and AMECO releases of the time, and the target and the floor are those then in force. A rule fitted at the end of 2007 reads a US neutral real rate of 2.14%, the Laubach-Williams estimate published on 20 December 2007, where a run today reads 1.2%. [Dated Values](/projects/financescenarios/docs/validation/dated-values) shows each of these histories with its sources.

## Data Choices

Which data the short rate is fitted on, and why:

| Choice | Kind | Why |
|:--|:--|:--|
| The US short rate is the 13-week Treasury bill (^IRX), monthly | Judgement | A market rate the policy rate drives, available daily and without an API key; [Ahlgrim, D'Arcy and Gorvett (2005, section 3)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"} likewise use the three-month Treasury rate for the short rate |
| The euro area's rates are Germany's (OECD, monthly) | Judgement | The euro area's largest economy and its benchmark Bund |
| The euro area's rule reads German inflation (quarterly) and French unemployment | Judgement | German unemployment fell structurally after the mid-2000s labor reforms; see [Unemployment](/projects/financescenarios/docs/economy/unemployment#euro-area-unemployment) |
| The rule's volatility and every starting value come from data since 2000 | Judgement | The default settings' calibration window: two full bear markets (2000-2002, 2008-2009) and the sector ETFs' history |

## Examples

The examples on this page use the run from the [overview](/projects/financescenarios/docs#simulating-scenarios): the default settings and factor set, calibrated on 19 October 2026, with 2,000 scenarios and seed 42.

### The Short Rates

The default factor set has a short rate, the 3-month rate, for the US, the euro area (Germany's) and the UK. To simulate them and read them off after five years:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
result = scenarios.simulate(n_simulations=2000, seed=42)

result.describe()
```

Which gives, for the three short rates:

| factor | initial | terminal_mean | terminal_q05 | terminal_q95 |
|:-------|--------:|--------------:|-------------:|-------------:|
| united_states_short_rate | 0.0408 | 0.0459 | 0.0000 | 0.1099 |
| eurozone_short_rate | 0.0264 | 0.0359 | -0.0050 | 0.0901 |
| united_kingdom_short_rate | 0.0399 | 0.0395 | 0.0010 | 0.0839 |

The 5th percentile of each short rate sits on its floor after five years: 0% for the US, -0.5% for the euro area and 0.1% for the UK, the lowest policy rate each central bank has set. The 95th percentiles reach 11.0%, 9.0% and 8.4%, the scenarios in which inflation took off. When plotted, the short rates:

{% include ft-chart.html id="interest-rates-short" src="/assets/data/financescenarios-guides/interest-rates.json" label="Median and 5-95% band of the short rate of the US, the euro area and the UK over five years" %}

### What the Policy Rule Reads

The calibration that `calibrate` returns holds every fitted and sourced number, per variable. The short rate's parameters hold the rule: its weights on the inflation and unemployment gaps, the neutral real rate, the inflation target, the longer-run unemployment rate and the floor, and the calibration notes say where each comes from. To read them for the US:

```python
calibration = scenarios.calibrate()

calibration.calibrated_params["united_states_short_rate"]

calibration.calibration_notes["united_states_short_rate"]
```

Which shows the balanced-approach rule the Federal Reserve reports in its [Monetary Policy Report (2026, Box 4, Table A)](https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-part2.htm){:target="_blank"}, with weights of 0.5 on the inflation gap and 2.0 on the unemployment gap, and the numbers it reads per economy:

| | US | Euro area | UK |
|:--|--:|--:|--:|
| Neutral real rate | 1.20% | 0.09% | 1.00% |
| Inflation target | 2.00% | 2.00% | 2.00% |
| Longer-run unemployment | 4.20% | 7.16% | 4.21% |
| Floor | 0.00% | -0.50% | 0.10% |
| Rule's steady state | 3.20% | 2.09% | 3.00% |

### An Inflation Shock

Because the short rate follows a rule on inflation, a scenario in which inflation jumps also gets the rate rises that answer it. `shock_regime` builds a one-variable what-if: here US inflation heads to 8% within a year and back onto its usual path by year five, while every scenario keeps its own randomness. To run it on the same calibration and compare the medians after five years:

```python
from financescenarios import compare_runs, shock_regime

regime = shock_regime("inflation", 0.08, calibration=calibration)
shocked = scenarios.simulate(regime=regime, calibration=calibration, n_simulations=2000, seed=42)

compare_runs(
    {"baseline": result, "inflation_at_8": shocked},
    statistic="terminal_median",
    factors=["united_states_inflation", "united_states_short_rate", "united_states_long_rate"],
)
```

Which returns:

| factor | baseline | inflation_at_8 |
|:-------|---------:|---------------:|
| united_states_inflation | 0.0181 | 0.0181 |
| united_states_short_rate | 0.0439 | 0.0612 |
| united_states_long_rate | 0.0562 | 0.0793 |

The median inflation is 7.64% after one year against 2.71% in the baseline and 4.66% after three, and is back on the baseline's 1.81% after five. The rule answers with a lag: the median short rate is 6.24% after one year against 4.33% in the baseline, 8.71% after three, and still 6.12% after five, when inflation has long come back. When plotted, the short rate and inflation in both runs:

{% include ft-chart.html id="interest-rates-shock" src="/assets/data/financescenarios-guides/interest-rates.json" label="Median and 5-95% band of the US short rate and US inflation in the baseline and with inflation at 8% within a year" %}

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">15</span></summary>

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. [casact.org](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}
- Bank of England (2025). Monetary Policy Report, February 2025, Box A. [bankofengland.co.uk](https://www.bankofengland.co.uk/monetary-policy-report/2025/february-2025){:target="_blank"}
- Bank of England. Bank Rate history and data. [bankofengland.co.uk](https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp){:target="_blank"}
- Black, F. (1995). "Interest Rates as Options." The Journal of Finance, 50(5), 1371-1376. [doi.org](https://doi.org/10.1111/j.1540-6261.1995.tb05182.x){:target="_blank"}
- Board of Governors of the Federal Reserve System (2018). Policy Rules and How Policymakers Use Them. [federalreserve.gov](https://www.federalreserve.gov/monetarypolicy/policy-rules-and-how-policymakers-use-them.htm){:target="_blank"}
- Board of Governors of the Federal Reserve System (2026). Monetary Policy Report, July 2026, Part 2, Box 4. [federalreserve.gov](https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-part2.htm){:target="_blank"}
- Board of Governors of the Federal Reserve System. Open Market Operations: federal funds target ranges. [federalreserve.gov](https://www.federalreserve.gov/monetarypolicy/openmarket.htm){:target="_blank"}
- European Central Bank (2021). The ECB's monetary policy strategy statement, 8 July 2021. [ecb.europa.eu](https://www.ecb.europa.eu/home/search/review/html/ecb.strategyreview_monpol_strategy_statement.en.html){:target="_blank"}
- European Central Bank. Official interest rates: key ECB interest rates. [ecb.europa.eu](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/html/index.en.html){:target="_blank"}
- European Commission (2026). AMECO, Spring 2026 forecast: ZNAWRU. [ec.europa.eu](https://ec.europa.eu/economy_finance/ameco/wq/series?fullVariable=1.0.0.0.ZNAWRU&countries=FRA,GBR,DEU&years=2027&lastYear=0&yearOrder=ASC){:target="_blank"}
- Federal Open Market Committee (2026). Statement on Longer-Run Goals and Monetary Policy Strategy. [federalreserve.gov](https://www.federalreserve.gov/monetarypolicy/files/fomc_longerrungoals.pdf){:target="_blank"}
- Federal Open Market Committee (2026). Summary of Economic Projections, 16 September 2026, Table 1. [federalreserve.gov](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm){:target="_blank"}
- Federal Reserve Bank of New York (2026). Measuring the natural rate of interest: Holston-Laubach-Williams and Laubach-Williams estimates, current and real-time. [newyorkfed.org](https://www.newyorkfed.org/research/policy/rstar){:target="_blank"}
- HM Treasury (2025). Monetary policy remit: Budget 2025, letter from the Chancellor of the Exchequer to the Governor of the Bank of England, 26 November 2025. [gov.uk](https://www.gov.uk/government/publications/monetary-policy-remit-budget-2025/letter-from-chancellor-of-the-exchequer-to-govenor-of-the-bank-of-england){:target="_blank"}
- Taylor, J.B. (1993). "Discretion versus Policy Rules in Practice." Carnegie-Rochester Conference Series on Public Policy, 39, 195-214. [doi.org](https://doi.org/10.1016/0167-2231(93)90009-L){:target="_blank"}

</details>

{% include ft-charts-script.html %}
