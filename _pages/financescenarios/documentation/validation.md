---
title: Validation
seo_title: "Validation Documentation | Finance Scenarios"
seo_title_suffix: false
excerpt: "How to trust a run: whether the scenarios reproduce the model's own mathematics, move together the way the economy does, stay within what history has seen, would have held what happened when fitted in the past, and land near outside benchmarks."
description: "How to trust a Finance Scenarios run: long-run moments, macro relationships, realism against history, parameter guardrails, out-of-sample coverage, PIT and CRPS, external benchmarks and limits."
author_profile: false
permalink: /projects/financescenarios/docs/validation
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

A scenario set is only useful if you can defend it to a model validator, an auditor or a regulator. That takes four kinds of evidence:

<div class="ca-cards">
  <div><i class="ca-icon fas fa-square-root-variable" aria-hidden="true"></i><p class="ca-card-title">The model</p><p>The simulation does what the model's mathematics says (<a href="#the-simulation-reproduces-the-model">the simulation reproduces the model</a>) and, for a valuation run, reproduces market prices (<a href="#market-consistency-the-martingale-test">the martingale test</a>).</p></div>
  <div><i class="ca-icon fas fa-earth-americas" aria-hidden="true"></i><p class="ca-card-title">The economy</p><p>The scenarios behave like the economy they describe: they fit their history (<a href="#checking-a-run-against-history">checks against history</a>), the factors move together the way the economy does (<a href="#do-the-factors-move-together-the-way-the-economy-does">relationships</a>), stay within how far history has gone (<a href="#does-each-factor-stay-within-what-history-has-seen">realism</a>) and come from plausible fitted parameters (<a href="#are-the-fitted-parameters-ones-the-real-world-could-produce">guardrails</a>).</p></div>
  <div><i class="ca-icon fas fa-history" aria-hidden="true"></i><p class="ca-card-title">Out of sample</p><p>A model fitted in the past would have held what actually happened (<a href="#out-of-sample-would-a-past-calibration-have-held-what-happened">out of sample</a>).</p></div>
  <div><i class="ca-icon fas fa-scale-balanced" aria-hidden="true"></i><p class="ca-card-title">Outside references</p><p>The scenarios land near independent outside references (<a href="#external-benchmarks">external benchmarks</a>).</p></div>
</div>

This page covers each, the theory behind the measure, the numbers on the default model and what is not validated.

<div class="ca-nav">
  <a href="#the-simulation-reproduces-the-model"><i class="fas fa-square-root-variable" aria-hidden="true"></i>The model</a>
  <a href="#market-consistency-the-martingale-test"><i class="fas fa-coins" aria-hidden="true"></i>Martingale test</a>
  <a href="#checking-a-run-against-history"><i class="fas fa-list-check" aria-hidden="true"></i>Checks against history</a>
  <a href="#do-the-factors-move-together-the-way-the-economy-does"><i class="fas fa-project-diagram" aria-hidden="true"></i>Relationships</a>
  <a href="#does-each-factor-stay-within-what-history-has-seen"><i class="fas fa-ruler" aria-hidden="true"></i>Realism against history</a>
  <a href="#are-the-fitted-parameters-ones-the-real-world-could-produce"><i class="fas fa-sliders-h" aria-hidden="true"></i>Parameter guardrails</a>
  <a href="#out-of-sample-would-a-past-calibration-have-held-what-happened"><i class="fas fa-history" aria-hidden="true"></i>Out of sample</a>
  <a href="#run-it"><i class="fas fa-terminal" aria-hidden="true"></i>Run it</a>
  <a href="#external-benchmarks"><i class="fas fa-scale-balanced" aria-hidden="true"></i>External benchmarks</a>
  <a href="#published-calibrations"><i class="fas fa-tags" aria-hidden="true"></i>Published calibrations</a>
  <a href="#what-is-not-validated"><i class="fas fa-triangle-exclamation" aria-hidden="true"></i>What is not validated</a>
</div>

## The Simulation Reproduces the Model {#the-simulation-reproduces-the-model}

The strongest evidence compares simulated output with a result derived independently of the code.

**Long-run moments.** Most rate-type factors are mean-reverting (Ornstein-Uhlenbeck), which has a known long-run distribution:

$$
dx_t = a(\theta - x_t)\,dt + \sigma\,dW_t \quad\Rightarrow\quad \mathbb{E}[x_\infty] = \theta,\qquad \operatorname{Var}[x_\infty] = \frac{\sigma^2}{2a}
$$

Here $$a$$ is the mean-reversion speed, $$\theta$$ the long-run level and $$\sigma$$ the volatility. For CIR the long-run variance is $$\sigma^2\theta/(2a)$$. Each mean-reverting factor's simulated mean and standard deviation at the horizon are compared with these values, allowing three standard errors of Monte Carlo noise. A gap is not always a fault: with a horizon shorter than about three time constants ($$1/a$$) the factor has not settled yet, and a factor on a belief path is deliberately steered elsewhere. A gap that remains points to the discretization or the calibration.

**Boundary behavior.** Hull-White rates are Gaussian and can go negative, as they should. CIR rates can dip very slightly below zero because of the full-truncation scheme, the least biased of those compared by [Lord, Koekkoek and van Dijk (2010)](https://doi.org/10.1080/14697680802392496){:target="_blank"}; see [time stepping](/projects/financescenarios/docs/simulation-engine#time-stepping).

**Correlations.** The correlated shocks reproduce their target: 50,000 draws with a target of 0.6 land within 0.02. Across a full run, the simulated factor moves are compared with the calibrated matrix (see the checks below); pairs where a model links one factor's drift to the other legitimately differ, so they are reported but not graded. This is the correlation test EIOPA lists for a generator: simulated against historical correlations ([Guidelines on valuation of technical provisions, EIOPA-BoS-14/166, Guideline 58, paragraph 1.105](https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en){:target="_blank"}).

## Market Consistency: The Martingale Test {#market-consistency-the-martingale-test}

A risk-neutral run used for valuation must reproduce today's prices: discounted along each scenario's own short rate, with dividends added back, a traded asset must on average be worth today's price at every future date. Passing shows the drift is risk neutral; it does not show that option prices are reproduced, since outside an equity with Heston volatility the volatility is a single number with no smile. With many dates tested at once, a correct run misses a few by chance, so the verdict adjusts for that ([Holm, 1979](https://www.jstor.org/stable/4615733){:target="_blank"}) rather than requiring every date to pass. The formula, a worked example and the matching bond-price check against EIOPA's curve are on the [Solvency II page](/projects/financescenarios/docs/solvency#martingale-test-example).

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">Most dates failing?</p>

Most dates failing usually means a real-world run or a missing dividend yield.
</div>

## Checking a Run Against History {#checking-a-run-against-history}

The same checks run on every published calibration and on any run of your own. Each passes, warns or fails, with the numbers and what they mean. They are screens for errors in the fit or the implementation, not acceptance criteria for the model.

The bands are wide on purpose: mean-reverting, regime-switching and GARCH factors legitimately move a little differently at another step size than their history, and a correlation gap above 0.25 points to a wiring problem rather than noise. A factor fitted on a longer history than the recent window is reported but not graded on volatility. Year-over-year rates (inflation, house-price growth) are compared on their changes over a year, in history and simulation alike: neighboring monthly readings share 11 of their 12 months, so their month-to-month changes understate how much they really move. The checks:

| Check | Warns or fails when | What a failure implies |
|:------|:--------------------|:-----------------------|
| Every factor calibrated | A configured factor's fit failed and it was left out (warn). | The run is missing a risk driver; read the reason before using it. |
| Parameters in a plausible range | A rate's long-run level is outside -5% to 25%, or a half-life outside about a week to 50 years (warn). | The fit is suspect, often from a short or unusual history, not necessarily wrong. |
| Valid correlation matrix | Not symmetric, no unit diagonal or a negative eigenvalue (fail). | The joint distribution is not well defined. |
| Simulation reproduces the correlations | A pair the model does not link directly misses its calibrated correlation by over 0.1 (warn) or 0.25 (fail). | Diversification between those factors is misstated. |
| Simulated volatility matches history | A factor's simulated yearly volatility is outside 0.67-1.5 times its history's (warn) or 0.33-3 times (fail). | Tails are too narrow or too wide for that factor. |
| Reproducible under a seed | Two runs with the same seed differ (fail; published calibrations only). | Results cannot be replayed for audit. |
| Every path is finite | Any path holds NaN or infinity (fail). | A numerical breakdown; the run should not be used. |

All of these checks run in one call on a simulated run:

```python
result = scenarios.simulate(n_simulations=2000)
scenarios.validate(result)   # one row per check: status, detail, meaning
```

<div class="fs-callout" markdown="1">
A "warn" is worth a look, not a reason to discard the run.
</div>

The run itself also warns when a correlation was set to 0 because two factors shared fewer than 5 observations, when two factors correlate above 0.98 (usually the same driver configured twice), and when a filter leaves too few scenarios for percentiles to mean much. See [How the Correlations Are Estimated](/projects/financescenarios/docs/simulation-engine#how-the-correlations-are-estimated).

## Do the Factors Move Together the Way the Economy Does?

A run can match every factor's own volatility and correlations and still get the economy wrong: rates that ignore inflation, a Phillips curve with the wrong sign, a curve that inverts at random. These links are what a stress narrative or a liability valuation leans on, so each one is measured the same way on decades of history and on every scenario, and the two are compared.

Everything is read at year ends, where the slow links show and month-to-month noise does not. History comes from the OECD's monthly series since the 1950s, read at the end of each year, and Shiller's US data since 1871 for stocks and consumer prices. Each relationship is a slope or a correlation:

| Relationship | Measured as | Source of the expected sign |
|:--|:--|:--|
| Policy rate reacts to inflation and to unemployment | The short rate's yearly change on the changes in inflation and unemployment | [Taylor (1993, p. 202, eq. 1)](https://doi.org/10.1016/0167-2231(93)90009-L){:target="_blank"}; [Federal Reserve (2026, Monetary Policy Report, Box 4, Table A)](https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-part2.htm){:target="_blank"} |
| Rates sit higher when inflation is far above target | The average short rate in years with inflation 2 points above target less in years within half a point of it | The same rule |
| Phillips curve | Inflation's yearly change on unemployment's | [Phillips (1958, p. 285, Figure 1)](https://doi.org/10.1111/j.1468-0335.1958.tb00003.x){:target="_blank"} |
| Unemployment rises around bear markets | The correlation of the year's equity return with unemployment's change around it | The sign only: equity returns are low in the years unemployment rises |
| The long rate moves with the short rate | The 10-year's yearly change on the short rate's | [Campbell and Shiller (1991, section 2, eq. 1)](https://doi.org/10.2307/2298008){:target="_blank"} |
| An inverted curve comes before higher unemployment | Unemployment's change over the next two years on the 10-year less the short rate | [Estrella and Hardouvelis (1991, section II.D)](https://doi.org/10.1111/j.1540-6261.1991.tb02674.x){:target="_blank"}; [Estrella and Mishkin (1998, Table 2, p. 49)](https://doi.org/10.1162/003465398557320){:target="_blank"} |
| Stocks do worse when inflation is high | The real return in years with inflation above 5% less below 3% | [Fama and Schwert (1977, Table 5, p. 128)](https://doi.org/10.1016/0304-405X(77)90014-9){:target="_blank"} |
| Higher rates slow house prices | The change in house-price growth on the 10-year's change | [Iacoviello (2005, section I, Figure 1, p. 741)](https://doi.org/10.1257/0002828054201477){:target="_blank"} |
| Oil and inflation | Inflation's change on the oil price's | [Hooker (2002)](https://doi.org/10.1353/mcb.2002.0041){:target="_blank"} |
| Rate differentials and the currency | The exchange rate's change on the rate gap | [Fama (1984, Table 2, p. 326)](https://doi.org/10.1016/0304-3932(84)90046-1){:target="_blank"} |
| Credit spreads and unemployment | Unemployment's change on the spread | [Gilchrist and Zakrajšek (2012, section II.A, Table 2, p. 1699)](https://doi.org/10.1257/aer.102.4.1692){:target="_blank"}; only with a credit factor |

The grade compares the scenarios' median with history's estimate $$h$$ and its standard error. If history cannot tell the sign ($$|h| < 2\,\text{se}$$), the row passes when the scenarios land within two standard errors of it and warns otherwise. If it can, the row fails when the scenarios have the opposite sign, passes when they are between half and twice history's size, and warns in between. The factor of two is a judgement: it accepts a link that is there but weaker or stronger, and flags one that is missing or reversed.

On a 30-year run of 1,000 scenarios from the default calibration, out of 26 relationships:

<div class="ca-nums fs-nums">
  <span><b>15</b>pass</span>
  <span><b>11</b>warn</span>
  <span><b>0</b>fail</span>
</div>

The US policy rate answers inflation with a slope of 0.24 against history's 0.45, and the long rate following the short rate (0.59 against 0.33) and higher rates slowing house prices (-0.93 against -0.96) come out in history's direction. What warns is mostly a link that is there but weaker than in history: unemployment moves the policy rate less than half as strongly in all three economies (-0.22 against -0.58 in the US), the US Phillips curve is about half as steep (-0.29 against -0.59), bear markets come with rising unemployment at -0.15 against -0.41, and an inverted US curve foreshadows higher unemployment at -0.24 against -0.67. The two currency rows pass with the opposite sign to history only because history's own slope is too uncertain to tell. Row by row:

| Relationship | Region | Status | History | Simulated median |
|:--|:--|:--|--:|--:|
| Policy rate reacts to inflation | United States | pass | 0.45 | 0.24 |
| Policy rate reacts to unemployment | United States | warn | -0.58 | -0.22 |
| Rates near neutral at target, higher above it | United States | pass | 0.06 | 0.04 |
| Phillips curve | United States | warn | -0.59 | -0.29 |
| Bear markets come with rising unemployment | United States | warn | -0.41 | -0.15 |
| Long rate moves with the short rate | United States | pass | 0.33 | 0.59 |
| Inverted curve precedes higher unemployment | United States | warn | -0.67 | -0.24 |
| Real equity returns fall with high inflation | United States | warn | -0.15 | -0.07 |
| Higher rates slow house prices | United States | pass | -0.96 | -0.93 |
| Oil prices pass into inflation | United States | warn | 0.04 | 0.01 |
| Policy rate reacts to inflation | Euro area | warn | 0.04 | 0.27 |
| Policy rate reacts to unemployment | Euro area | warn | -0.96 | -0.33 |
| Rates near neutral at target, higher above it | Euro area | pass | 0.04 | 0.03 |
| Phillips curve | Euro area | pass | -0.89 | -1.00 |
| Long rate moves with the short rate | Euro area | pass | 0.27 | 0.45 |
| Inverted curve precedes higher unemployment | Euro area | pass | -0.19 | -0.13 |
| Oil prices pass into inflation | Euro area | warn | 0.03 | 0.00 |
| Rate differential and the currency | Euro area | pass | -0.72 | 0.35 |
| Policy rate reacts to inflation | United Kingdom | pass | 0.23 | 0.26 |
| Policy rate reacts to unemployment | United Kingdom | warn | -0.93 | -0.38 |
| Rates near neutral at target, higher above it | United Kingdom | pass | 0.05 | 0.06 |
| Phillips curve | United Kingdom | pass | -0.49 | -0.27 |
| Long rate moves with the short rate | United Kingdom | pass | 0.30 | 0.44 |
| Inverted curve precedes higher unemployment | United Kingdom | warn | -0.45 | -0.04 |
| Oil prices pass into inflation | United Kingdom | pass | 0.02 | 0.01 |
| Rate differential and the currency | United Kingdom | pass | -0.53 | 0.46 |

## Does Each Factor Stay within What History Has Seen?

A fit on a few decades says little about a factor's extremes. Nothing in it stops a rate from wandering below anything a central bank has set, or keeps a calm window from ruling out a 1970s. So every factor is read at year ends against its longest record (OECD series from the 1950s for rates, inflation and unemployment; Shiller's US home prices since 1890; each equity market's long index; the World Bank's Pink Sheet since 1971 for gold and oil; exchange rates in real terms), on the same statistics:

- the lowest and highest level, and the largest one-year rise and fall;
- the worst drawdown from the previous ten years' high, and the longest stretch below one;
- the longest stretches at the zero lower bound, in a curve inversion and with inflation above 5%;
- states no economy can be in: unemployment at or below zero, a price at or below zero, house prices down 100%, a negative spread (each a hard fail), and deflation below -10% for two years.

Two grades are combined, and the worse one counts:

- **Frequency.** History is cut into every window as long as the run. At the most extreme level history reached in at least two separate episodes, the share of scenarios that reach it is set against the share of windows that did, within a [Wilson (1927, p. 209)](https://doi.org/10.1080/01621459.1927.10502953){:target="_blank"} interval for the handful of independent windows behind it: pass inside the 90% interval, warn inside the 99% one, fail outside it. Too rarely is a tail too thin, too often one too fat.
- **Envelope.** Beyond history's worst, where it gives no frequency, the scenarios may go at most as often as a 1-in-200-year event would over the run, $$1 - (1 - 1/200)^T$$, which is 14% for 30 years: the 99.5% one-year level of [Solvency II (Directive 2009/138/EC, Article 101(3))](https://eur-lex.europa.eu/eli/dir/2009/138/oj){:target="_blank"}. History's extreme is widened by half a standard deviation of its yearly moves (or one year, for a stretch) before a warning, and by one and a half (three years) before a failure; these margins are judgements.

On the same run, no factor passes every test. Of the 23 factors:

<div class="ca-nums fs-nums">
  <span><b>8</b>warn</span>
  <span><b>15</b>fail</span>
</div>

Most flags are tails that are too thin: over 30 years the scenarios reach history's record years less often than history's own windows did, for the rates and unemployment of all three economies, house prices, Japanese stocks and crude oil's largest one-year rise. A few go the other way, such as low inflation in the US and the UK ("tail too fat"). No factor reaches a state no economy can be in.

## Are the Fitted Parameters Ones the Real World Could Produce?

The last screen looks at the fitted parameters themselves, against what any economy has shown:

| Guardrail | Pass | Warn | Fail |
|:--|:--|:--|:--|
| Half-life $$\ln 2 / a$$ of a mean-reverting factor | 0.1 to 50 years | Outside | Below 0.02 or above 200 years |
| A fit at its bound | | Within 1% of a bound, a regime at the volatility floor or below a 2% share, a stay chance at 0 or 1 | |
| Long-run level | Inside the range history spans | Outside it | Beyond it by more than its width; a rate outside -5% to 25% |
| Volatility against the history behind the fit | 2/3 to 1.5 times | 1/3 to 3 times | Outside |
| Equity regimes against the same model on Shiller's US record since 1871 | Turbulent share and spells within 2 times | Within 4 times | Outside |

The bands are judgements: no published standard sets them. On the same run, four guardrails warn and none fails. Euro-area unemployment settles at 7.16%, just below the 7.20% to 10.90% of the French history it was fitted on; the UK short rate swings 1.56 times its calibration history; and Japan's equity regimes are furthest from the long US record, in the crisis regime 44.8% of the time against 14.3%, with calm spells of 1.16 years against 2.87.

## Out of Sample: Would a Past Calibration Have Held What Happened?

The checks above compare a run with the history it was fitted on. The harder test goes back to a past date, fits the model on only the data known then, simulates from that day and sets the scenarios against what actually happened. Every series the fit reads ends on that date, and beliefs held today are reported; OECD and FRED series are still read as revised today.

Each factor is scored at every whole year ahead:

- **PIT**: where the realised value fell among the scenarios, the share below it. For a correct forecast it is uniform between 0 and 1, so its mean is 0.5 and its standard deviation $$1/\sqrt{12} = 0.289$$ ([Diebold, Gunther and Tay, 1998, section 3, pp. 867-868](https://doi.org/10.2307/2527342){:target="_blank"}). Across origins, a Kolmogorov-Smirnov test per horizon checks the uniformity, with a Bonferroni correction across horizons (p. 880).
- **Coverage**: how often the 50% and 90% bands held the outcome, with [Kupiec's (1995, section V, expression 8)](https://doi.org/10.3905/jod.1995.407942){:target="_blank"} likelihood-ratio test: bands that held too seldom are "too narrow", too often "too wide", at a 5% significance level.
- **CRPS**: the continuous ranked probability score, $$E|X - y| - \tfrac{1}{2}E|X - X'|$$ ([Gneiting and Raftery, 2007, section 4.2, eq. 21, p. 367](https://doi.org/10.1198/016214506000001437){:target="_blank"}), which rewards a cloud that is both centred and tight; its skill against a forecast of no change shows whether the scenarios beat standing still.

From the end of 2007, the model fitted on the 26 years before it, 1,000 scenarios run five years ahead:

<figure class="theme-image"><img src="/assets/images/projects/financescenarios/docs/validation/out-of-sample-2007-light.png" alt="Out-of-sample fan charts from the end of 2007 for US stocks, US unemployment, the US short and long rate and US and UK inflation, with the realised path" loading="lazy" style="display:block"></figure>

The financial crisis falls largely outside the cloud, because of its speed. US unemployment reached 7.3% at the end of 2008 and 9.9% at the end of 2009, while 1 in 20 scenarios went above 6.69% and 7.39%; only by 2012, at 7.9%, was it back inside the 90% band. The short rate was cut to 0.11% within the year against a 5th percentile of 2.86%, and stayed below the band until 2012. US stocks were down 36.8% by the end of 2008 against a 5th percentile of -15.1%, and the 10-year rate fell to 2.24% against 3.75%. US inflation dipped below the band at the end of 2008 (0.09%) and came back inside it; UK inflation stayed inside throughout. In the scores, the 90% band held one of the five years for the short rate and for unemployment, two for the long rate and three for stocks, and on CRPS the scenarios lose to a no-change forecast for stocks, both rates and UK inflation.

From the end of 2019, through the pandemic and the inflation that followed:

<figure class="theme-image"><img src="/assets/images/projects/financescenarios/docs/validation/out-of-sample-2019-light.png" alt="Out-of-sample fan charts from the end of 2019 with the realised path" loading="lazy" style="display:block"></figure>

Here the cloud holds more. US stocks stay inside the 90% band in all five years, through the 2020 crash and the rally after it. The jump in US unemployment to 6.7% at the end of 2020 is above the band's 5.34%, and the cut to zero again lies below it: the short rate at 0.07% and 0.03% at the end of 2020 and 2021 against 5th percentiles of 1.99% and 2.01%, the 10-year rate at 0.92% and 1.51% against 2.22% and 2.58%. The inflation that followed sits at the edge: US inflation of 7.04% at the end of 2021 and 6.45% at the end of 2022 is above the 95th percentiles of 4.68% and 4.91%, and UK inflation of 4.84% in 2021 lands just inside its 4.88% before 9.24% in 2022 goes past 6.44%. From 2022 on, both rates are back inside the band.

One crisis is an anecdote. Five origins four years apart (the ends of 2003, 2007, 2011, 2015 and 2019), each run four years ahead, score every year from 2004 to 2023 once:

| Factor | Coverage 50% | Coverage 90% | Bands | PIT mean | CRPS skill |
|:--|--:|--:|:--|--:|--:|
| US inflation | 0.45 | 0.85 | ok | 0.56 | 0.47 |
| Euro-area inflation | 0.50 | 0.85 | ok | 0.48 | 0.43 |
| UK inflation | 0.65 | 0.90 | ok | 0.64 | 0.41 |
| US short rate | 0.30 | 0.70 | too narrow | 0.29 | 0.19 |
| US long rate | 0.40 | 0.80 | ok | 0.27 | -0.35 |
| Euro-area short rate | 0.35 | 0.70 | too narrow | 0.59 | 0.43 |
| Euro-area long rate | 0.45 | 0.90 | ok | 0.34 | 0.37 |
| UK short rate | 0.30 | 0.75 | ok | 0.23 | 0.15 |
| UK long rate | 0.30 | 0.95 | ok | 0.22 | 0.02 |
| US unemployment | 0.35 | 0.75 | ok | 0.44 | 0.36 |
| Euro-area unemployment | 0.15 | 0.60 | too narrow | 0.66 | 0.34 |
| UK unemployment | 0.30 | 0.65 | too narrow | 0.42 | 0.31 |
| US stocks | 0.50 | 0.90 | ok | 0.56 | 0.53 |
| Japanese stocks | 0.70 | 0.85 | ok | 0.42 | 0.25 |
| Euro | 0.70 | 1.00 | too wide | 0.56 | 0.29 |
| Pound sterling | 0.35 | 0.90 | ok | 0.68 | 0.21 |
| Yen | 0.50 | 0.70 | too narrow | 0.52 | 0.29 |
| Yield-curve level | 0.45 | 0.95 | ok | 0.33 | 0.12 |
| Yield-curve slope | 0.40 | 0.75 | ok | 0.57 | 0.44 |
| Yield-curve curvature | 0.50 | 0.90 | ok | 0.40 | 0.24 |
| US house prices | 0.25 | 0.50 | too narrow | 0.61 | 0.08 |
| Leading indicator | 0.40 | 0.80 | ok | 0.57 | 0.23 |
| US small caps | 0.50 | 0.94 | ok | 0.52 | 0.38 |
| Gold | 0.50 | 1.00 | ok | 0.62 | 0.43 |
| European stocks | 0.67 | 1.00 | ok | 0.48 | 0.29 |
| Emerging-market stocks | 0.67 | 1.00 | ok | 0.53 | 0.16 |
| Crude oil | 0.62 | 1.00 | ok | 0.63 | 0.53 |

Inflation holds best: US, euro-area and UK inflation keep 85% to 90% of their years inside the 90% band, close to the 0.9 it should hold, and US stocks hold 0.90. Where it falls short, the bands are too narrow: the US and euro-area short rates (0.70), euro-area and UK unemployment (0.60 and 0.65), the yen (0.70) and US house prices (0.50). The US short and long rates also have low tails that are too thin, as the cuts to zero in 2008 and 2020 showed; with a PIT mean of 0.29 the US short rate ran below the scenarios' middle more often than above it, and on CRPS the US long rate loses to a no-change forecast. The euro's band is too wide (1.00).

## Run It

The numbers above come from the [Model Validation notebook](/projects/financescenarios/model-validation-notebook): the README's calibration of the default profiles, a 30-year run of 1,000 scenarios with seed 42 for the checks against history, and 1,000 scenarios from each past origin.

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(api_key="FINANCIAL_MODELING_PREP_KEY")  # the default settings and factor set
result = scenarios.simulate(n_simulations=1000, years=30, seed=42)

scenarios.check_relationships(result)  # the macro relationships, history against the scenarios
scenarios.check_realism(result, summary=True)  # one row per factor: what warns or fails against its longest record
scenarios.check_parameters(result, flagged_only=True)  # the parameter guardrails that flag

crisis = scenarios.out_of_sample(as_of="2007-12-31", years=5, n_simulations=1000, seed=42)
crisis.plot(["us_broad", "united_states_unemployment"])  # the fan from that date against what happened
scenarios.out_of_sample_many(
    origins=["2003-12-31", "2007-12-31", "2011-12-31", "2015-12-31", "2019-12-31"], years=4, n_simulations=1000, seed=42
).scores  # coverage, PIT and CRPS per factor across the origins
```

<div class="fs-ref"><a href="/projects/financescenarios/docs/reference/scenarios"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Scenarios</a></div>

## External Benchmarks {#external-benchmarks}

The checks above compare the model with itself and its own data. The benchmarks below compare a calibrated factor with independent sources. Each reference embeds its own model choices, so a gap is not automatically an error, but a large or systematic one needs explaining. Four references are used:

| Benchmark | What is compared | Note |
|:----------|:-----------------|:-----|
| NAIC GOES | A US Treasury rate's simulated percentile bands | A set of differences, not a pass or fail |
| DNB scenario set | A run's interest rate, inflation or equity, quantile by quantile at every whole year | A regulator-reviewed reference for a euro run |
| Corporate bond panel | Credit spread levels and their dispersion across individual bonds | Validates spread levels, not rating migration |
| Option-implied densities | A risk-neutral equity's terminal-price distribution | Tests the flat-volatility lognormal assumption |

- **NAIC GOES.** The Generator of Economic Scenarios, the prescribed generator of the NAIC Valuation Manual for US principle-based reserves (VM-20 for life, VM-21 for variable annuities), run by Conning for the NAIC. Prescribed is not mandatory: a company may use its own generator if the result meets the Valuation Manual's standard in section 2.G ([NAIC Valuation Manual, 2026 edition, VM-20 Appendix 1, Section E](https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf#page=132){:target="_blank"}).

  A US Treasury rate's simulated percentile bands are compared with the percentile grid of NAIC's 10,000-scenario set for the matching tenor; the result is a set of differences, not a pass or fail. A large gap usually means the long-run level or the volatility differs from what US regulators consider a reasonable real-world spread of rates.
- **DNB scenario set.** De Nederlandsche Bank publishes a scenario set every quarter: 20,000 scenarios over 100 years from the Commissie Parameters 2022 model, both real world (the P-set) and market consistent (the Q-set, calibrated to market prices including swaptions). A run's interest rate, inflation or equity is compared with it at every whole year, quantile by quantile: rates and inflation by level, equities by yearly return. It is a regulator-reviewed reference for a euro run and the only free swaption-consistent one. The same sets, and NAIC's 16 deterministic stress scenarios for US rates (the set of the Valuation Manual's Stochastic Exclusion Ratio Test, SERT), can also replace factors in a run (see the [configuration reference](/projects/financescenarios/docs/reference/configuration)).
- **Corporate bond panel.** Credit spreads are fitted to one aggregate index per maturity bucket. The Open Source Bond Asset Pricing panel (Dickerson, Robotti and Rossetti; built on TRACE trades from 2002 to 2025, tens of millions of bond-date rows) shows the spread distribution of the individual bonds underneath. The comparison shows whether the aggregate's fitted level and volatility represent the real dispersion or smooth over fatter tails and idiosyncratic widening. The public data has no credit ratings, so it validates spread levels, not rating migration.
- **Option-implied densities.** A risk-neutral equity's simulated terminal-price distribution is compared with the market's own risk-neutral density at the nearest listed expiration, extracted from option prices with the [Breeden-Litzenberger (1978)](https://doi.org/10.1086/296025) result. Both sides come from the same market, so this tests the flat-volatility lognormal assumption rather than providing an outside view. The headline number is the Wasserstein distance (how far apart the two terminal-price views are, on average, in price units); a Kolmogorov-Smirnov statistic flags a sharp local tail mismatch the average could hide. Expect a gap: the market's density is skewed and fat-tailed, the model's is not.

## Published Calibrations {#published-calibrations}

A published calibration is fixed under a version tag, passes the checks above before release, and records its data window, package versions and a hash of its configuration. A run can then state exactly which calibration it used, and anyone can reproduce its scenarios offline. A release whose configuration no longer matches its hash is refused rather than silently mixing two sets of assumptions. Reference calibrations are meant to be published once a year, the minimum frequency EIOPA sets for these tests ([Guidelines on valuation of technical provisions, Guideline 58, paragraph 1.106](https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en){:target="_blank"}).

Downloading and simulating a release is covered in the runs and releases reference.

<div class="fs-ref"><a href="/projects/financescenarios/docs/reference/runs-and-releases"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Runs and releases</a></div>

## What Is Not Validated {#what-is-not-validated}

<div class="fs-callout fs-callout--limits" markdown="1">
- **Dependence is one linear correlation matrix**, constant over the horizon. A Student-t shock distribution adds joint tail risk through one shared t-copula (see [fat tails](/projects/financescenarios/docs/simulation-engine#fat-tails-and-tail-dependence)), but tail dependence that differs by pair or is asymmetric is not captured.
- **Risk-neutral calibration is limited in scope.** Interest rates, inflation, equities, FX and commodities can be calibrated risk neutral, but without a full arbitrage-free volatility surface: rate and inflation volatilities come from history, not from swaption or inflation-option prices, so the time value of guarantees is indicative; see the [measures section of the configuration page](/projects/financescenarios/docs/configuration#real-world-and-risk-neutral-measures).
- **Judgment calls are not checked for economic sense.** The number of equity regimes and every belief override are the user's choice; only their shape is checked, not whether they are reasonable.
- **Out of sample is a handful of origins.** Five origins four years apart score twenty years once each; the years within one origin's run are not independent, so coverage and PIT rest on few independent observations, and OECD and FRED series are read as revised today, not as they were known at the time.
- **The relationship and realism bands are judgements.** Half to twice history's slope, and the margins around history's extremes, are not published standards; a warning is a reason to look, not a verdict.
- **No scenario reduction or moment matching.** Every simulated path is returned as drawn; none are selected or reweighted to match target moments with fewer scenarios.
</div>
