---
title: Against History
seo_title: "Against History | Finance Scenarios"
seo_title_suffix: false
excerpt: "How Finance Scenarios checks a run against its own model and against history: long-run moments, the run's own checks, the macro relationships, history's extremes and guardrails on the fitted parameters."
description: "Validating Finance Scenarios against history: what the simulation must reproduce, the checks on every run, macro relationships with Newey-West errors, the extremes of the longest records, parameter guardrails and what is not validated."
author_profile: false
permalink: /projects/financescenarios/docs/validation
classes: wide-sidebar
layout: single
redirect_from:
    - /projects/financescenarios/model-validation-notebook
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-validation"
---

A scenario set is only useful if you can defend it to a model validator, an auditor or a regulator. Defending it takes four kinds of evidence:

<div class="ca-cards">
  <div><i class="ca-icon fas fa-square-root-variable" aria-hidden="true"></i><p class="ca-card-title">The model</p><p>The simulation does what the model's mathematics says (<a href="#the-simulation-reproduces-the-model">below</a>) and, for a valuation run, reproduces market prices (<a href="/projects/financescenarios/docs/solvency#the-martingale-test">the martingale test</a>).</p></div>
  <div><i class="ca-icon fas fa-earth-americas" aria-hidden="true"></i><p class="ca-card-title">The economy</p><p>The factors move together the way the economy does (<a href="#macro-relationships">relationships</a>), stay within how far history has gone (<a href="#historys-extremes">extremes</a>) and come from plausible fitted parameters (<a href="#parameter-guardrails">guardrails</a>).</p></div>
  <div><i class="ca-icon fas fa-history" aria-hidden="true"></i><p class="ca-card-title">Out of sample</p><p>A model fitted in the past, on only what was known then, would have held what actually happened (<a href="/projects/financescenarios/docs/validation/out-of-sample">Out of Sample</a>, with the <a href="/projects/financescenarios/docs/validation/dated-values">dated values</a> such a fit reads).</p></div>
  <div><i class="ca-icon fas fa-scale-balanced" aria-hidden="true"></i><p class="ca-card-title">Outside references</p><p>The scenarios land near the generators regulators prescribe (<a href="/projects/financescenarios/docs/validation/benchmarks">Benchmarks</a>), and the published models reproduce their papers and are scored against what happened since (<a href="/projects/financescenarios/docs/validation/published-models">Published Models</a>).</p></div>
</div>

This page covers the first two: the checks against the model itself and against history.

## The Simulation Reproduces the Model {#the-simulation-reproduces-the-model}

The strongest evidence compares simulated output with a result derived independently of the code.

**Long-run moments.** Most rate-type factors are mean-reverting (Ornstein-Uhlenbeck), which has a known long-run distribution:

$$
dx_t = a(\theta - x_t)\,dt + \sigma\,dW_t \quad\Rightarrow\quad \mathbb{E}[x_\infty] = \theta,\qquad \operatorname{Var}[x_\infty] = \frac{\sigma^2}{2a}
$$

Here $$a$$ is the mean-reversion speed, $$\theta$$ the long-run level and $$\sigma$$ the volatility. For a CIR (Cox-Ingersoll-Ross) rate the long-run variance is $$\sigma^2\theta/(2a)$$ instead. `diagnose` compares each mean-reverting factor's simulated mean and standard deviation at the horizon with these values: the mean must land within 20% of $$\theta$$ or within three Monte Carlo standard errors, whichever is wider, and the standard deviation within 20% of its long-run value. A gap is not always a fault: over a horizon shorter than about three time constants ($$1/a$$) the factor has not settled yet, and a factor whose long-run level follows a belief path is steered elsewhere on purpose. A gap that remains points to the discretization or the calibration.

**Boundary behavior.** Hull-White rates are Gaussian and can go negative, as the model intends. CIR rates can dip very slightly below zero: they are simulated with the full-truncation scheme, the least biased of the schemes compared by [Lord, Koekkoek and van Dijk (2010)](https://doi.org/10.1080/14697680802392496){:target="_blank"} (see [Simulation Engine](/projects/financescenarios/docs/simulation-engine#time-stepping)).

**Correlations.** The correlated shocks reproduce their target: 50,000 draws with a target of 0.6 land within 0.02. Across a full run, one of the checks below compares the simulated factor moves with the calibrated matrix; pairs where the model links one factor's drift to the other's legitimately differ, so they are reported but not graded. This is the correlation test EIOPA lists for a generator: simulated against historical correlations ([Guidelines on valuation of technical provisions, EIOPA-BoS-14/166, Guideline 58, paragraph 1.105](https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en){:target="_blank"}).

**Market prices.** A risk-neutral run must reproduce today's prices: the martingale test of [Market Consistency](/projects/financescenarios/docs/solvency#the-martingale-test) checks it, with Holm's adjustment for testing many dates at once. Passing shows the drift is risk neutral; it does not show that option prices are reproduced, since outside an equity with Heston (stochastic) volatility the volatility is a single number, with no smile across strikes.

## Checks on Every Run {#checking-a-run-against-history}

The same checks run on every published calibration and on any run of your own. Each passes, warns or fails, with the numbers and what they mean. They are screens for errors in the fit or the implementation, not acceptance criteria for the model.

The bands are wide on purpose: a mean-reverting, regime-switching or GARCH factor simulated at a different step from its history legitimately moves a little differently, and a correlation gap above 0.25 points to a wiring problem rather than noise. A factor fitted on a longer history than the recent window is reported but not graded on volatility. Year-over-year rates (inflation, house-price growth) are compared on their changes over a year, in history and simulation alike: neighboring monthly readings share 11 of their 12 months, so their month-to-month changes understate how much they really move. The checks:

| Check | Warns or fails when | What a failure implies |
|:------|:--------------------|:-----------------------|
| Every factor calibrated | A configured factor's fit failed and it was left out (warn). | The run is missing a risk driver; read the reason before using it. |
| Parameters in a plausible range | A rate's long-run level is outside -5% to 25%, or a half-life outside about a week to 50 years (warn). | The fit is suspect, often from a short or unusual history, not necessarily wrong. |
| Valid correlation matrix | Not symmetric, no unit diagonal or a negative eigenvalue (fail); a repair to the nearest valid matrix that moves it by more than 1.0 (warn). | The joint distribution is not well defined, or the estimates did not hold together. |
| Simulation reproduces the correlations | A pair the model does not link directly misses its calibrated correlation by over 0.1 (warn) or 0.25 (fail). | Diversification between those factors is misstated. |
| Simulated volatility matches history | A factor's simulated yearly volatility is outside 0.67-1.5 times its history's (warn) or 0.33-3 times (fail). | Tails are too narrow or too wide for that factor. |
| Reproducible under a seed | Two runs with the same seed differ (fail; published calibrations only). | Results cannot be replayed for audit. |
| Every path is finite | Any path holds NaN or infinity (fail). | A numerical breakdown; the run should not be used. |

<div class="fs-callout" markdown="1">
A "warn" is worth a look, not a reason to discard the run.
</div>

The run itself also warns when a correlation was set to 0 because two factors shared fewer than 5 observations, when two factors correlate above 0.98 (usually the same driver configured twice), and when a filter leaves too few scenarios for percentiles to mean much ([Dependence](/projects/financescenarios/docs/dependence#how-the-correlations-are-estimated) explains how the correlations are estimated).

`validate` runs these checks, and `diagnose` the long-run moments above. On the five-year run of the [overview](/projects/financescenarios/docs#checking-the-run), `validate` gives four passes and two warnings: the euro-area and UK inflation correlation comes out 0.103 away from the one it was given, and the euro-area short rate moves 1.72 times as much as in its history.

## Macro Relationships

A run can match every factor's own volatility and correlations and still get the economy wrong: rates that ignore inflation, a Phillips curve with the wrong sign, a curve that inverts at random. These links are what a stress narrative or a liability valuation leans on, so each one is measured the same way on decades of history and on every scenario, and the two are compared.

Everything is read at year ends, where the slow links show and month-to-month noise does not. History comes from the OECD's monthly series since the 1950s and Shiller's US data since 1871 for stocks and consumer prices. Each relationship is a slope or a correlation:

| Relationship | Measured as | Source of the expected sign |
|:--|:--|:--|
| Policy rate reacts to inflation and to unemployment | The short rate's yearly change on the changes in inflation and unemployment | [Taylor (1993, p. 202, eq. 1)](https://doi.org/10.1016/0167-2231(93)90009-L){:target="_blank"}; [Federal Reserve (2026, Monetary Policy Report, Box 4, Table A)](https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-part2.htm){:target="_blank"} |
| Rates near neutral at target, higher above it | The average short rate in years with inflation 2 points above target, less that in years within half a point of it | The same rule |
| Phillips curve | Inflation's yearly change on unemployment's | [Phillips (1958, p. 285, Figure 1)](https://doi.org/10.1111/j.1468-0335.1958.tb00003.x){:target="_blank"} |
| Bear markets come with rising unemployment | The correlation of the year's equity return with unemployment's change around it | The sign only: equity returns are low in the years unemployment rises |
| Long rate moves with the short rate | The 10-year's yearly change on the short rate's | [Campbell and Shiller (1991, section 2, eq. 1)](https://doi.org/10.2307/2298008){:target="_blank"} |
| Inverted curve precedes higher unemployment | Unemployment's change over the next two years on the 10-year less the short rate | [Estrella and Hardouvelis (1991, section II.D)](https://doi.org/10.1111/j.1540-6261.1991.tb02674.x){:target="_blank"}; [Estrella and Mishkin (1998, Table 2, p. 49)](https://doi.org/10.1162/003465398557320){:target="_blank"} |
| Real equity returns fall with high inflation | The real return in years with inflation above 5%, less that in years below 3% | [Fama and Schwert (1977, Table 5, p. 128)](https://doi.org/10.1016/0304-405X(77)90014-9){:target="_blank"} |
| Higher rates slow house prices | The next year's change in house-price growth on the 10-year's change | [Iacoviello (2005, section I, Figure 1, p. 741)](https://doi.org/10.1257/0002828054201477){:target="_blank"} |
| Oil prices pass into inflation | Inflation's change on the oil price's | [Hooker (2002)](https://doi.org/10.1353/mcb.2002.0041){:target="_blank"} |
| Rate differential and the currency | The exchange rate's log change over the next year on the year-end rate gap | [Fama (1984, Table 2, p. 326)](https://doi.org/10.1016/0304-3932(84)90046-1){:target="_blank"} |
| Credit spreads and unemployment | The spread's yearly change on unemployment's | [Gilchrist and Zakrajšek (2012, section II.A, Table 2, p. 1699)](https://doi.org/10.1257/aer.102.4.1692){:target="_blank"}; only with a credit factor |

The grade compares the median $$m$$ of the scenarios' estimates with history's estimate $$h$$ and its standard error (se). If history cannot tell the sign ($$\vert h\vert < 2\,\text{se}$$), the row passes when the scenarios land within two standard errors of it and warns otherwise. If it can, the row fails when the scenarios have the opposite sign or none ($$m\,h \le 0$$), passes when they are between half and twice history's size, and warns when they are weaker or stronger than that. The factor of two is a judgment: it accepts a link that is there but weaker or stronger, and flags one that is missing or reversed.

### History's Standard Error

Everything in that grade hangs on the standard error, and for yearly macro series the textbook one is too small. Interest rates, inflation and unemployment persist from one year to the next, and a two-year change in unemployment shares a year with its neighbor, so the regression's errors are autocorrelated. Ordinary least squares then finds links in noise: with 150 years of two unrelated series, each as persistent as an AR(1) with coefficient 0.9, it finds a correlation beyond two standard errors in half the samples. The standard errors are therefore [Newey and West's (1987)](https://doi.org/10.2307/1913610){:target="_blank"}, which weight the autocovariances of the errors with Bartlett weights (declining linearly with the lag) up to $$\lfloor 4(T/100)^{2/9} \rfloor$$ lags, the starting bandwidth of [Newey and West (1994)](https://doi.org/10.2307/2297912){:target="_blank"}: three lags for 28 to 99 years. The lags are counted on the calendar, so a year missing from a history still counts as a year apart.

How often a check finds a link where there is none, at two standard errors, in simulated histories of 150 years:

| Check | Textbook errors | Newey-West errors |
|:--|--:|--:|
| Inverted-curve slope (an AR(1) spread with coefficient 0.8 against a random-walk unemployment) | 0.133 | 0.085 |
| The correlation of two independent AR(1) levels with coefficient 0.9 | 0.512 | 0.287 |
| Rates near neutral at target (a difference in means) | 0.332 | 0.198 |

That is much closer to the 5% a test at two standard errors should give, but above it: Newey-West errors are still too small for levels as persistent as these over a few decades, so a pass on a persistent level is weaker evidence than its standard error suggests.

### Example

The checks against history need many year-end observations per scenario, so the examples on this page run the calibration of the [overview](/projects/financescenarios/docs#simulating-scenarios), made on 19 October 2026, 30 years ahead with 1,000 scenarios and seed 42. `check_relationships` measures every relationship in the table above on history and on each scenario, and grades the scenarios' median as described. To simulate the run and check it:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
result = scenarios.simulate(n_simulations=1000, years=30, seed=42)

relationships = scenarios.check_relationships(result)
```

Which returns 26 rows, one per relationship and economy:

| Relationship | Region | Status | History | Standard error | Simulated median |
|:--|:--|:--|--:|--:|--:|
| Policy rate reacts to inflation | United States | warn | 0.45 | 0.13 | 0.21 |
| Policy rate reacts to unemployment | United States | pass | -0.58 | 0.17 | -0.38 |
| Rates near neutral at target, higher above it | United States | pass | 0.06 | 0.01 | 0.03 |
| Phillips curve | United States | pass | -0.59 | 0.22 | -0.32 |
| Bear markets come with rising unemployment | United States | warn | -0.41 | 0.11 | -0.12 |
| Long rate moves with the short rate | United States | pass | 0.33 | 0.06 | 0.58 |
| Inverted curve precedes higher unemployment | United States | warn | -0.67 | 0.07 | -0.26 |
| Real equity returns fall with high inflation | United States | pass | -0.15 | 0.04 | -0.08 |
| Higher rates slow house prices | United States | pass | -0.96 | 0.39 | -0.90 |
| Oil prices pass into inflation | United States | warn | 0.04 | 0.01 | 0.01 |
| Policy rate reacts to inflation | Euro area | warn | 0.04 | 0.08 | 0.24 |
| Policy rate reacts to unemployment | Euro area | pass | -0.96 | 0.25 | -0.57 |
| Rates near neutral at target, higher above it | Euro area | pass | 0.04 | 0.01 | 0.03 |
| Phillips curve | Euro area | pass | -0.89 | 0.43 | -0.97 |
| Long rate moves with the short rate | Euro area | pass | 0.27 | 0.05 | 0.44 |
| Inverted curve precedes higher unemployment | Euro area | pass | -0.19 | 0.12 | -0.12 |
| Oil prices pass into inflation | Euro area | pass | 0.03 | 0.02 | 0.00 |
| Rate differential and the currency | Euro area | pass | -0.72 | 0.84 | 0.21 |
| Policy rate reacts to inflation | United Kingdom | pass | 0.23 | 0.14 | 0.17 |
| Policy rate reacts to unemployment | United Kingdom | pass | -0.93 | 0.31 | -0.61 |
| Rates near neutral at target, higher above it | United Kingdom | pass | 0.05 | 0.03 | 0.02 |
| Phillips curve | United Kingdom | pass | -0.49 | 0.34 | -0.09 |
| Long rate moves with the short rate | United Kingdom | pass | 0.30 | 0.09 | 0.38 |
| Inverted curve precedes higher unemployment | United Kingdom | warn | -0.45 | 0.14 | -0.11 |
| Oil prices pass into inflation | United Kingdom | pass | 0.02 | 0.02 | 0.00 |
| Rate differential and the currency | United Kingdom | pass | -0.53 | 0.90 | 0.17 |

Twenty pass and six warn; none fails. The policy rate answers unemployment in all three economies, at -0.38, -0.57 and -0.61 against history's -0.58, -0.96 and -0.93, because the default rule is the Federal Reserve's inertial balanced-approach rule, with twice the weight on the unemployment gap (see [Short Rate](/projects/financescenarios/docs/interest-rates)). The Phillips curve passes in all three, the long rate follows the short rate, higher rates slow house prices (-0.90 against -0.96), and real equity returns fall with high inflation (-0.08 against -0.15).

Five of the warnings are links that are there but less than half as strong as in history: the US policy rate's answer to inflation (0.21 against 0.45), bear markets coming with rising unemployment (-0.12 against -0.41), an inverted curve foreshadowing higher unemployment in the US (-0.26 against -0.67) and the UK (-0.11 against -0.45), and oil passing into US inflation (0.01 against 0.04). The sixth is the euro area's policy rate, which answers inflation at 0.24 where history cannot tell the sign (0.04 with a standard error of 0.08). The two currency rows pass with the opposite sign to history only because history's own slope is too uncertain to tell. When plotted, the ten US relationships:

{% include ft-chart.html id="validation-relationships" src="/assets/data/financescenarios-guides/validation.json" label="Ten US macro relationships measured on history and as the median across 1,000 scenarios over thirty years" %}

## History's Extremes

A fit on a few decades says little about a factor's extremes. Nothing in it stops a rate from wandering below anything a central bank has set, or keeps a calm window from ruling out a 1970s. So every factor is read at year ends against its longest record (OECD series from the 1950s for rates, inflation and unemployment; Shiller's US home prices since 1890; each equity market's long index; the World Bank's Pink Sheet since 1971 for gold and oil; exchange rates in real terms), with the same statistics on both:

- the lowest and highest level, and the largest one-year rise and fall;
- the worst drawdown from the previous ten years' high, and the longest stretch below the running high, up to ten years;
- the longest stretches at the zero lower bound, in a curve inversion and with inflation above 5%;
- states no economy can be in: unemployment at or below zero, a price at or below zero, house prices down 100% and a negative spread, each a hard fail; and deflation below -10% for two years, which warns whenever it happens and fails only when it happens more often than a 1-in-200-year event would.

Two grades are combined, and the worse one counts:

- **Frequency.** History is cut into every window of the run's length. At the most extreme level history reached in at least two separate episodes, the share of scenarios that reach it is set against the share of windows that did, within a [Wilson (1927, p. 209)](https://doi.org/10.1080/01621459.1927.10502953){:target="_blank"} interval (a confidence interval for a share) sized for the handful of independent windows behind it: pass inside the 90% interval, warn inside the 99% one, fail outside it. Reaching it too rarely flags a "tail too thin", too often a "tail too fat".
- **Envelope.** Beyond history's worst, where it gives no frequency, the scenarios may go at most as often as a 1-in-200-year event would over the run, $$1 - (1 - 1/200)^T$$, which is 14% for 30 years: the 99.5% one-year level of [Solvency II (Directive 2009/138/EC, Article 101(3))](https://eur-lex.europa.eu/eli/dir/2009/138/oj){:target="_blank"}. History's extreme is widened by half a standard deviation of its yearly moves (or one year, for a stretch) before a warning, and by one and a half (three years) before a failure; these margins are judgments.

### Example

`check_realism` runs these statistics and grades on the same run; with `summary=True` it returns one row per factor. To run it:

```python
scenarios.check_realism(result, summary=True)
```

Which flags every factor somewhere. Of the 23 factors, and of the 120 statistics behind them:

<div class="ca-nums fs-nums">
  <span><b>5</b>factors warn</span>
  <span><b>18</b>factors fail</span>
  <span><b>66 / 26 / 28</b>statistics pass, warn, fail</span>
</div>

Most flags are tails that are too thin: over 30 years the scenarios reach history's record years less often than history's own windows did, for the rates and unemployment of all three economies, US house prices, US, Japanese and emerging-market stocks, and crude oil's largest one-year rise. The highest level of inflation is too thin in all three economies; for the UK that is the accepted cost of fitting its inflation from 1993, after the start of inflation targeting, which leaves the 1970s to the stress regimes (see [Inflation](/projects/financescenarios/docs/economy#the-uk-is-fitted-on-its-inflation-targeting-era)). The lowest level of US inflation goes the other way ("tail too fat"): anchoring the regimes on the long-run mean lowers the calm level. No factor reaches a state no economy can be in.

## Parameter Guardrails

The last screen looks at the fitted parameters themselves, against what any economy has shown:

| Guardrail | Pass | Warn | Fail |
|:--|:--|:--|:--|
| Half-life $$\ln 2 / a$$ of a mean-reverting factor | 0.1 to 50 years | Outside | Below 0.02 or above 200 years |
| A fit at its bound | | Within 1% of a bound, a regime at the volatility floor or below a 2% share, a regime's chance of staying at 0 or 1, a GARCH persistence $$\alpha + \beta$$ of 0.98 or more, an AR(1) persistence of 0.999 or more | |
| Long-run level | Inside the range history spans | Outside it | Beyond it by more than its width; a rate outside -5% to 25% |
| Volatility against the history behind the fit | 2/3 to 1.5 times | 1/3 to 3 times | Outside |
| Equity regimes against the same model on Ken French's month-end US market since 1926 | The crisis regime's share and each regime's expected spell within 2 times | Within 4 times | Outside |

The bands are judgments: no published standard sets them.

### The Yardstick for Equity Regimes

The last guardrail needs a long record to compare a fund's regimes with, and the record has to be measured the same way the funds are. Every equity is fitted on month-end prices. Shiller's monthly US series, the longest there is, is not: each month's price is the average of that month's daily closes. [Working (1960)](https://doi.org/10.2307/1907574){:target="_blank"} shows what averaging does to a random walk: the changes between averages keep about two thirds of the variance, and neighboring changes correlate by about a quarter, because two neighboring averages share the movements around the month's turn. A regime model fitted on such a series sees smoother, more persistent returns and longer regimes. So the yardstick is the same two-regime model fitted on Ken French's month-end US market (the CRSP value-weighted market, Mkt-RF plus RF) since July 1926. The chart shows the autocorrelation of monthly returns in both records:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/validation/regime-yardstick" alt="The autocorrelation of monthly US stock market returns at lags of 1 to 12 months, Ken French's month-end returns against Shiller's monthly averages, with Working's 0.25" %}

The lag-one autocorrelation is +0.271 in Shiller's averages, close to Working's 0.25, against +0.085 at month-ends. The fitted regimes change with it:

| Two-regime fit on | Crisis share | Crisis stay | Calm stay | Crisis mean, volatility | Calm mean, volatility |
|:--|--:|--:|--:|--:|--:|
| Shiller, monthly averages since 1871 | 0.143 | 0.48 years | 2.87 years | -20.8%, 26.5% | 13.9%, 9.8% |
| Ken French, month-ends since 1926 | 0.165 | 0.67 years | 3.39 years | -22.1%, 33.8% | 16.1%, 12.5% |

### Example

`check_parameters` runs these guardrails on the same run. To list the ones that flag:

```python
scenarios.check_parameters(result, flagged_only=True)
```

Which returns six warnings and no failures; the other 76 guardrails pass. UK inflation, fitted on its inflation-targeting era from 1993, swings 0.51 times as much as in its longer history; euro-area unemployment settles at 7.16%, just below the 7.20% to 10.90% of the French history it was fitted on; the euro-area short rate swings 1.67 times its calibration history and the UK long rate 0.64 times; and Japan's stock market, the furthest from the long US record, is in its crisis regime 44.9% of the time against 16.5%, with calm spells of 1.16 years against 3.39.

## Published Calibrations {#published-calibrations}

A published calibration is fixed under a version tag, passes the checks on every run before release, and records its data window, package versions and a hash of its configuration. A run can then state exactly which calibration it used, and anyone can reproduce its scenarios offline. A release whose configuration no longer matches its hash is refused rather than silently mixing two sets of assumptions. Reference calibrations are meant to be published once a year, the minimum frequency EIOPA sets for these tests ([Guidelines on valuation of technical provisions, Guideline 58, paragraph 1.106](https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en){:target="_blank"}).

## What Is Not Validated {#what-is-not-validated}

<div class="fs-callout fs-callout--limits" markdown="1">
- **Dependence is one linear correlation matrix**, constant over the horizon. A Student-t shock distribution adds joint tail risk through one shared t-copula (see [Dependence](/projects/financescenarios/docs/dependence#fat-tails-and-tail-dependence)), but tail dependence that differs by pair or is asymmetric is not captured.
- **Risk-neutral calibration is limited in scope.** Interest rates, inflation, equities, FX and commodities can be calibrated risk neutral, but without a full arbitrage-free volatility surface: rate and inflation volatilities come from history, not from swaption or inflation-option prices, so the time value of guarantees is indicative; see [Configuration](/projects/financescenarios/docs/configuration#real-world-and-risk-neutral-measures).
- **Judgment calls are not checked for economic sense.** The number of equity regimes and every belief override are the user's choice; only their shape is checked, not whether they are reasonable.
- **Out of sample rests on few independent outcomes.** Twenty-three yearly origins four years ahead leave as few as five non-overlapping outcomes per group at the four-year horizon, so the tests flag only clear misses. The published values a fit reads are dated, and each series waits for its first release. Some reads are not real time, though: the data are read as revised today, the US term premium is the New York Fed's ACM estimate as re-estimated today on the full sample, natural rates of unemployment before 2011 are 2011 vintages, and before each dated table's first real-time release a later estimate for that quarter or year stands in.
- **A regime that reaches a crisis was written after it.** The COVID and 2022 regimes replay those episodes' published paths; the financial-crisis regime, which sets no levels, does not reach the depth of 2008.
- **The relationship and realism bands are judgments.** Half to twice history's slope, and the margins around history's extremes, are not published standards; a warning is a reason to look, not a verdict. Newey-West errors still understate the uncertainty of very persistent levels.
- **No scenario reduction or moment matching.** Every simulated path is returned as drawn; none are selected or reweighted to match target moments with fewer scenarios.
</div>

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">18</span></summary>

- Board of Governors of the Federal Reserve System (2026). Monetary Policy Report, July 2026, Part 2, Box 4. [federalreserve.gov](https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-part2.htm){:target="_blank"}
- Campbell, J.Y., Shiller, R.J. (1991). "Yield Spreads and Interest Rate Movements: A Bird's Eye View." The Review of Economic Studies, 58(3), 495-514. [doi.org](https://doi.org/10.2307/2298008){:target="_blank"}
- EIOPA (2014). Guidelines on Valuation of Technical Provisions (EIOPA-BoS-14/166). [eiopa.europa.eu](https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en){:target="_blank"}
- Estrella, A., Hardouvelis, G.A. (1991). "The Term Structure as a Predictor of Real Economic Activity." Journal of Finance, 46(2), 555-576. [doi.org](https://doi.org/10.1111/j.1540-6261.1991.tb02674.x){:target="_blank"}
- Estrella, A., Mishkin, F.S. (1998). "Predicting U.S. Recessions: Financial Variables as Leading Indicators." Review of Economics and Statistics, 80(1), 45-61. [doi.org](https://doi.org/10.1162/003465398557320){:target="_blank"}
- European Parliament and Council (2009). "Directive 2009/138/EC (Solvency II)", Articles 76-77 (technical provisions, best estimate) and 101 (SCR at 99.5% over one year). [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/dir/2009/138/oj){:target="_blank"}
- Fama, E.F. (1984). "Forward and Spot Exchange Rates." Journal of Monetary Economics, 14(3), 319-338. [doi.org](https://doi.org/10.1016/0304-3932(84)90046-1){:target="_blank"}
- Fama, E.F., Schwert, G.W. (1977). "Asset Returns and Inflation." Journal of Financial Economics, 5(2), 115-146. [doi.org](https://doi.org/10.1016/0304-405X(77)90014-9){:target="_blank"}
- Gilchrist, S., Zakrajšek, E. (2012). "Credit Spreads and Business Cycle Fluctuations." American Economic Review, 102(4), 1692-1720. [doi.org](https://doi.org/10.1257/aer.102.4.1692){:target="_blank"}
- Hooker, M.A. (2002). "Are Oil Shocks Inflationary? Asymmetric and Nonlinear Specifications versus Changes in Regime." Journal of Money, Credit and Banking, 34(2), 540-561. [doi.org](https://doi.org/10.1353/mcb.2002.0041){:target="_blank"}
- Iacoviello, M. (2005). "House Prices, Borrowing Constraints, and Monetary Policy in the Business Cycle." American Economic Review, 95(3), 739-764. [doi.org](https://doi.org/10.1257/0002828054201477){:target="_blank"}
- Lord, R., Koekkoek, R., van Dijk, D. (2010). "A Comparison of Biased Simulation Schemes for Stochastic Volatility Models." Quantitative Finance, 10(2), 177-194. [doi.org](https://doi.org/10.1080/14697680802392496){:target="_blank"}
- Newey, W.K., West, K.D. (1987). "A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix." Econometrica, 55(3), 703-708. [doi.org](https://doi.org/10.2307/1913610){:target="_blank"}; eq. (5) of the working-paper version, [nber.org](https://www.nber.org/papers/t0055){:target="_blank"}
- Newey, W.K., West, K.D. (1994). "Automatic Lag Selection in Covariance Matrix Estimation." The Review of Economic Studies, 61(4), 631-653. [doi.org](https://doi.org/10.2307/2297912){:target="_blank"}
- Phillips, A.W. (1958). "The Relation Between Unemployment and the Rate of Change of Money Wage Rates in the United Kingdom, 1861-1957." Economica, 25(100), 283-299. [doi.org](https://doi.org/10.1111/j.1468-0335.1958.tb00003.x){:target="_blank"}
- Taylor, J.B. (1993). "Discretion versus Policy Rules in Practice." Carnegie-Rochester Conference Series on Public Policy, 39, 195-214. [doi.org](https://doi.org/10.1016/0167-2231(93)90009-L){:target="_blank"}
- Wilson, E.B. (1927). "Probable Inference, the Law of Succession, and Statistical Inference." Journal of the American Statistical Association, 22(158), 209-212. [doi.org](https://doi.org/10.1080/01621459.1927.10502953){:target="_blank"}
- Working, H. (1960). "Note on the Correlation of First Differences of Averages in a Random Chain." Econometrica, 28(4), 916-918. [doi.org](https://doi.org/10.2307/1907574){:target="_blank"}

</details>

{% include ft-charts-script.html %}
