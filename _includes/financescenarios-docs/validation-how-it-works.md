## How It Works

Defending a scenario set takes four kinds of evidence:

<div class="ca-cards">
  <div><i class="ca-icon fas fa-square-root-variable" aria-hidden="true"></i><p class="ca-card-title">The model</p><p>The simulation does what the model's mathematics says (<a href="#the-simulation-reproduces-the-model">the simulation reproduces the model</a>) and, for a valuation run, reproduces market prices (<a href="#market-consistency-the-martingale-test">the martingale test</a>).</p></div>
  <div><i class="ca-icon fas fa-earth-americas" aria-hidden="true"></i><p class="ca-card-title">The economy</p><p>The scenarios behave like the economy they describe: they fit their history (<a href="#checking-a-run-against-history">checks against history</a>), the factors move together the way the economy does (<a href="#do-the-factors-move-together-the-way-the-economy-does">relationships</a>), stay within how far history has gone (<a href="#does-each-factor-stay-within-what-history-has-seen">realism</a>) and come from plausible fitted parameters (<a href="#are-the-fitted-parameters-ones-the-real-world-could-produce">guardrails</a>).</p></div>
  <div><i class="ca-icon fas fa-history" aria-hidden="true"></i><p class="ca-card-title">Out of sample</p><p>A model fitted in the past, on only what was known then, would have held what actually happened (<a href="#out-of-sample-would-a-past-calibration-have-held-what-happened">out of sample</a>), and a bundled regime reaches the crises the baseline misses (<a href="#crises-against-the-bundled-regimes">crises and regimes</a>).</p></div>
  <div><i class="ca-icon fas fa-scale-balanced" aria-hidden="true"></i><p class="ca-card-title">Outside references</p><p>The scenarios land near independent outside references (<a href="#external-benchmarks">external benchmarks</a>), meet the acceptance criteria of NAIC's generator (<a href="#goes-acceptance-criteria">GOES</a>), and the published models reproduce their papers (<a href="#published-parameter-mode">published models</a>) and are scored against what happened since (<a href="#published-models-held-up">how they held up</a>).</p></div>
</div>

This page covers each, the theory behind the measure, the numbers on the default model and what is not validated. Every number below comes from the calibration of 19 October 2026, the one the README uses.

### The Simulation Reproduces the Model {#the-simulation-reproduces-the-model}

The strongest evidence compares simulated output with a result derived independently of the code.

**Long-run moments.** Most rate-type factors are mean-reverting (Ornstein-Uhlenbeck), which has a known long-run distribution:

$$
dx_t = a(\theta - x_t)\,dt + \sigma\,dW_t \quad\Rightarrow\quad \mathbb{E}[x_\infty] = \theta,\qquad \operatorname{Var}[x_\infty] = \frac{\sigma^2}{2a}
$$

Here $$a$$ is the mean-reversion speed, $$\theta$$ the long-run level and $$\sigma$$ the volatility. For CIR the long-run variance is $$\sigma^2\theta/(2a)$$. Each mean-reverting factor's simulated mean and standard deviation at the horizon are compared with these values, allowing three standard errors of Monte Carlo noise. A gap is not always a fault: with a horizon shorter than about three time constants ($$1/a$$) the factor has not settled yet, and a factor on a belief path is deliberately steered elsewhere. A gap that remains points to the discretization or the calibration.

**Boundary behavior.** Hull-White rates are Gaussian and can go negative, as they should. CIR rates can dip very slightly below zero because of the full-truncation scheme, the least biased of those compared by [Lord, Koekkoek and van Dijk (2010)](https://doi.org/10.1080/14697680802392496){:target="_blank"}; see [time stepping](/projects/financescenarios/docs/simulation-engine#time-stepping).

**Correlations.** The correlated shocks reproduce their target: 50,000 draws with a target of 0.6 land within 0.02. Across a full run, the simulated factor moves are compared with the calibrated matrix (see the checks below); pairs where a model links one factor's drift to the other legitimately differ, so they are reported but not graded. This is the correlation test EIOPA lists for a generator: simulated against historical correlations ([Guidelines on valuation of technical provisions, EIOPA-BoS-14/166, Guideline 58, paragraph 1.105](https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en){:target="_blank"}).

### Market Consistency: The Martingale Test {#market-consistency-the-martingale-test}

A risk-neutral run used for valuation must reproduce today's prices: discounted along each scenario's own short rate, with dividends added back, a traded asset must on average be worth today's price at every future date. Passing shows the drift is risk neutral; it does not show that option prices are reproduced, since outside an equity with Heston volatility the volatility is a single number with no smile. With many dates tested at once, a correct run misses a few by chance, so the verdict adjusts for that ([Holm, 1979](https://www.jstor.org/stable/4615733){:target="_blank"}) rather than requiring every date to pass. The same holds for an exchange rate: a foreign deposit converted to dollars and discounted at the US rate is worth, on average, what it cost, because the rate drifts by the gap between the two currencies' rates ([Garman and Kohlhagen, 1983](https://doi.org/10.1016/S0261-5606(83)80001-1){:target="_blank"}). The formula, a worked example and the matching bond-price check against EIOPA's curve are on the [Solvency II page](/projects/financescenarios/docs/solvency#martingale-test-example).

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">Most dates failing?</p>

Most dates failing usually means a real-world run or a missing dividend yield.
</div>

### Checking a Run Against History {#checking-a-run-against-history}

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

```python
result = scenarios.simulate(n_simulations=2000)
scenarios.validate(result)   # one row per check: status, detail, meaning
```

<div class="fs-callout" markdown="1">
A "warn" is worth a look, not a reason to discard the run.
</div>

The run itself also warns when a correlation was set to 0 because two factors shared fewer than 5 observations, when two factors correlate above 0.98 (usually the same driver configured twice), and when a filter leaves too few scenarios for percentiles to mean much. See [How the Correlations Are Estimated](/projects/financescenarios/docs/simulation-engine#how-the-correlations-are-estimated).

#### How Far to Trust Each Correlation {#how-far-to-trust-each-correlation}

A correlation estimated on a few years of monthly data is noisy, and a run that takes it at face value builds diversification or concentration into the scenarios that the data never showed. So the calibrated matrix is pulled toward zero by an intensity that [Schäfer and Strimmer (2005)](https://doi.org/10.2202/1544-6115.1175){:target="_blank"} derive in closed form: the summed sampling variance of the correlations over their summed squares (section 2, eq. 10). Everything rests on that variance. The textbook formula, $$(1 - r^2)^2/(n - 1)$$, holds for normal data. Monthly returns and rate changes are not normal, and under fat tails a few large joint moves make a correlation much less certain than a normal sample of the same size. Schäfer and Strimmer's own estimate (their Appendix A) reads the variance from the data: standardize both series over the months they share, multiply them month by month, and the spread of those products is the correlation's variance.

The chart sets both against the true variance, from 4,000 samples of 120 months:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/validation/correlation-variance" alt="The normal-theory and Schafer-Strimmer Appendix A estimates of a correlation's sampling variance, divided by the true variance, for normal and Student-t(5) data at true correlations of 0, 0.3 and 0.6" %}

With Student-t tails of 5 degrees of freedom the normal-theory formula reads 0.46 times the true variance, about half, at every correlation; Appendix A reads 0.99 at a true correlation of zero. It errs on the high side as the correlation grows (1.30 times at 0.3, 3.33 times at 0.6), because it leaves out what standardizing takes away. The error is on the side of shrinking more, and most pairs in a scenario set have small correlations. On the default set the intensity is 0.155, against 0.067 with the normal-theory formula.

### Do the Factors Move Together the Way the Economy Does?

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

The grade compares the scenarios' median with history's estimate $$h$$ and its standard error. If history cannot tell the sign ($$\vert h\vert < 2\,\text{se}$$), the row passes when the scenarios land within two standard errors of it and warns otherwise. If it can, the row fails when the scenarios have the opposite sign, passes when they are between half and twice history's size, and warns in between. The factor of two is a judgement: it accepts a link that is there but weaker or stronger, and flags one that is missing or reversed.

#### History's Standard Error

Everything in that grade hangs on the standard error, and yearly macro series make the textbook one too small. Interest rates, inflation and unemployment persist from one year to the next, and a two-year change of unemployment shares a year with its neighbour, so the regression's errors are autocorrelated. Ordinary least squares then reads a link in noise: with 150 years of two unrelated series that each persist like an AR(1) with 0.9, it finds a correlation beyond two standard errors in half the samples. The standard errors are [Newey and West's (1987)](https://doi.org/10.2307/1913610){:target="_blank"} instead, which weight the autocovariances of the errors with Bartlett weights up to $$\lfloor 4(T/100)^{2/9} \rfloor$$ lags, the starting bandwidth of [Newey and West (1994)](https://doi.org/10.2307/2297912){:target="_blank"}: three lags for 28 to 99 years. The lags are counted on the calendar, so a year missing from a history still counts as a year apart.

How often a check finds a link where there is none, at two standard errors, in simulated histories of 150 years:

| Check | Textbook errors | Newey-West errors |
|:--|--:|--:|
| Inverted-curve slope (an AR(0.8) spread against a random-walk unemployment) | 0.133 | 0.085 |
| The correlation of two independent AR(0.9) levels | 0.512 | 0.287 |
| Rates at target (a difference in means) | 0.332 | 0.198 |

That is much closer to the 5% a test at two standard errors should give, but not there: Newey-West errors are still too small for levels as persistent as these over a few decades, so a pass on a persistent level is weaker evidence than its standard error suggests.

#### On the Default Model

On a 30-year run of 1,000 scenarios from the default calibration (seed 42), out of 26 relationships:

<div class="ca-nums fs-nums">
  <span><b>20</b>pass</span>
  <span><b>6</b>warn</span>
  <span><b>0</b>fail</span>
</div>

The policy rate now answers unemployment in all three economies, at -0.38, -0.57 and -0.61 against history's -0.58, -0.96 and -0.93, because the default rule is the Federal Reserve's inertial balanced-approach rule, with twice the weight on the unemployment gap (see the [interest-rates page](/projects/financescenarios/docs/interest-rates)). The Phillips curve passes in all three, the long rate follows the short rate, higher rates slow house prices (-0.90 against -0.96), and real equity returns fall with high inflation (-0.08 against -0.15). What warns is a link that is there but less than half as strong as in history: the US policy rate's answer to inflation (0.21 against 0.45), bear markets coming with rising unemployment (-0.12 against -0.41), an inverted curve foreshadowing higher unemployment in the US (-0.26 against -0.67) and the UK (-0.11 against -0.45), and oil passing into US inflation (0.01 against 0.04). The euro area's policy rate answers inflation at 0.24 where history cannot tell the sign (0.04 with a standard error of 0.08). The two currency rows pass with the opposite sign to history only because history's own slope is too uncertain to tell. Row by row:

| Relationship | Region | Status | History | Its standard error | Simulated median |
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

### Does Each Factor Stay within What History Has Seen?

A fit on a few decades says little about a factor's extremes. Nothing in it stops a rate from wandering below anything a central bank has set, or keeps a calm window from ruling out a 1970s. So every factor is read at year ends against its longest record (OECD series from the 1950s for rates, inflation and unemployment; Shiller's US home prices since 1890; each equity market's long index; the World Bank's Pink Sheet since 1971 for gold and oil; exchange rates in real terms), on the same statistics:

- the lowest and highest level, and the largest one-year rise and fall;
- the worst drawdown from the previous ten years' high, and the longest stretch below one;
- the longest stretches at the zero lower bound, in a curve inversion and with inflation above 5%;
- states no economy can be in: unemployment at or below zero, a price at or below zero, house prices down 100%, a negative spread (each a hard fail), and deflation below -10% for two years.

Two grades are combined, and the worse one counts:

- **Frequency.** History is cut into every window as long as the run. At the most extreme level history reached in at least two separate episodes, the share of scenarios that reach it is set against the share of windows that did, within a [Wilson (1927, p. 209)](https://doi.org/10.1080/01621459.1927.10502953){:target="_blank"} interval for the handful of independent windows behind it: pass inside the 90% interval, warn inside the 99% one, fail outside it. Too rarely is a tail too thin, too often one too fat.
- **Envelope.** Beyond history's worst, where it gives no frequency, the scenarios may go at most as often as a 1-in-200-year event would over the run, $$1 - (1 - 1/200)^T$$, which is 14% for 30 years: the 99.5% one-year level of [Solvency II (Directive 2009/138/EC, Article 101(3))](https://eur-lex.europa.eu/eli/dir/2009/138/oj){:target="_blank"}. History's extreme is widened by half a standard deviation of its yearly moves (or one year, for a stretch) before a warning, and by one and a half (three years) before a failure; these margins are judgements.

On the same run, no factor passes every test. Of the 23 factors, and of the 120 statistics behind them:

<div class="ca-nums fs-nums">
  <span><b>5</b>factors warn</span>
  <span><b>18</b>factors fail</span>
  <span><b>66 / 26 / 28</b>statistics pass, warn, fail</span>
</div>

Most flags are tails that are too thin: over 30 years the scenarios reach history's record years less often than history's own windows did, for the rates and unemployment of all three economies, US house prices, US, Japanese and emerging-market stocks, and crude oil's largest one-year rise. The highest level of inflation is too thin in all three economies; for the UK that is the accepted cost of fitting its inflation from 1993, after the start of inflation targeting, which leaves the 1970s to the stress regimes (see the [economy page](/projects/financescenarios/docs/economy)). The lowest level of US inflation goes the other way ("tail too fat"): anchoring the regimes on the long-run mean lowers the calm level. No factor reaches a state no economy can be in.

### Are the Fitted Parameters Ones the Real World Could Produce?

The last screen looks at the fitted parameters themselves, against what any economy has shown:

| Guardrail | Pass | Warn | Fail |
|:--|:--|:--|:--|
| Half-life $$\ln 2 / a$$ of a mean-reverting factor | 0.1 to 50 years | Outside | Below 0.02 or above 200 years |
| A fit at its bound | | Within 1% of a bound, a regime at the volatility floor or below a 2% share, a stay chance at 0 or 1 | |
| Long-run level | Inside the range history spans | Outside it | Beyond it by more than its width; a rate outside -5% to 25% |
| Volatility against the history behind the fit | 2/3 to 1.5 times | 1/3 to 3 times | Outside |
| Equity regimes against the same model on Ken French's month-end US market since 1926 | Turbulent share and spells within 2 times | Within 4 times | Outside |

The bands are judgements: no published standard sets them. On the same run, 76 guardrails pass, six warn and none fails. Euro-area unemployment settles at 7.16%, just below the 7.20% to 10.90% of the French history it was fitted on; the euro-area short rate swings 1.67 times its calibration history; UK inflation and the UK long rate swing 0.51 and 0.64 times their history; and Japan's equity regimes are furthest from the long US record, in the crisis regime 44.9% of the time against 16.5%, with calm spells of 1.16 years against 3.39.

#### The Yardstick for Equity Regimes

The last guardrail needs a long record to compare a fund's regimes with, and the record has to be measured the same way the funds are. Every equity is fitted on month-end prices. Shiller's monthly US series, the longest there is, is not: each month's price is the average of that month's daily closes. [Working (1960)](https://doi.org/10.2307/1907574){:target="_blank"} shows what averaging does to a random walk: the changes between averages keep about two thirds of the variance, and neighbouring changes correlate by about a quarter, because two neighbouring averages share the movements around the month's turn. A regime model fitted on such a series sees smoother, more persistent returns, and longer regimes. So the yardstick is the same two-regime model fitted on Ken French's month-end US market (the CRSP value-weighted market, Mkt-RF plus RF) since July 1926:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/validation/regime-yardstick" alt="The autocorrelation of monthly US stock market returns at lags of 1 to 12 months, Ken French's month-end returns against Shiller's monthly averages, with Working's 0.25" %}

The lag-one autocorrelation is +0.271 in Shiller's averages, close to Working's 0.25, against +0.085 at month-ends. The fitted regimes change with it:

| Two-regime fit on | Crisis share | Crisis stay | Calm stay | Crisis mean, volatility | Calm mean, volatility |
|:--|--:|--:|--:|--:|--:|
| Shiller, monthly averages since 1871 | 0.143 | 0.48 years | 2.87 years | -20.8%, 26.5% | 13.9%, 9.8% |
| Ken French, month-ends since 1926 | 0.165 | 0.67 years | 3.39 years | -22.1%, 33.8% | 16.1%, 12.5% |

### Out of Sample: Would a Past Calibration Have Held What Happened? {#out-of-sample-would-a-past-calibration-have-held-what-happened}

The checks above compare a run with the history it was fitted on. The harder test goes back to a past date, fits the model on only what was known then, simulates from that day and sets the scenarios against what actually happened.

**What the fit may know.** Every series the fit reads ends on that date, and a month counts only once it was published: consumer prices a month after the month ends, unemployment a month later in the US and two months later in the euro area and the UK, as the release calendars of the [Bureau of Labor Statistics](https://www.bls.gov/bls/histreleasedates.pdf){:target="_blank"}, the [Office for National Statistics](https://www.ons.gov.uk/releasecalendar){:target="_blank"} and [Eurostat](https://ec.europa.eu/eurostat/news/release-calendar){:target="_blank"} have it. A fit as of the end of 2007 sees US unemployment up to November. The published values it reads besides the data, such as the neutral real rate of the policy rule, the natural rate of unemployment and long-run inflation expectations, are the ones known that day (see [Dated Values](#dated-values) below). Three reads stay today's, and every run's notes say so: OECD and FRED series are read as revised today, not as first published; the US term premium of the long rate is the New York Fed's ACM estimate as re-estimated today on the whole sample; and the natural rates of unemployment before 2011 come from the 2011 vintages of the Congressional Budget Office and the European Commission, which estimated those earlier years with later data. Beliefs held today are reported.

Each factor is scored at every whole year ahead:

- **PIT**: where the realised value fell among the scenarios, the share below it. For a correct forecast it is uniform between 0 and 1, so its mean is 0.5 and its standard deviation $$1/\sqrt{12} = 0.289$$ ([Diebold, Gunther and Tay, 1998, section 3, pp. 867-868](https://doi.org/10.2307/2527342){:target="_blank"}).
- **Coverage**: how often the 50% and 90% bands held the outcome.
- **CRPS**: the continuous ranked probability score, $$E\vert X - y\vert - \tfrac{1}{2}E\vert X - X'\vert$$ ([Gneiting and Raftery, 2007, section 4.2, eq. 21, p. 367](https://doi.org/10.1198/016214506000001437){:target="_blank"}), which rewards a cloud that is both centred and tight; its skill against a forecast of no change shows whether the scenarios beat standing still. With 1,000 scenarios, the second term averages over the $$n(n-1)$$ distinct pairs rather than all $$n^2$$, the fair CRPS of [Ferro (2014)](https://doi.org/10.1002/qj.2270){:target="_blank"}, whose expectation does not depend on how many scenarios are drawn.
- **Tails**: how often the scenarios go beyond history's worst and best year. If the run's $$T$$ years and history's $$N$$ come from one distribution, any of the $$N + T$$ years is equally likely to be the most extreme, so a $$T$$-year run goes past history's record with probability $$T/(N+T)$$.

#### Tests That Hold Their Size

Coverage and PIT are tested across origins, and that is where overlap matters. With yearly origins and four-year horizons, neighbouring forecasts share three years of outcomes: a miss in 2008 is a miss for the forecasts from 2005, 2006 and 2007 at once. A test that treats every row as an independent draw then flags a correct model far more often than its 5%. So each horizon's rows are split into groups of origins at least that many years apart, whose outcomes do not overlap; with yearly origins these are the $$h$$ interleaved subsequences of [Diebold, Gunther and Tay (1998, p. 880)](https://doi.org/10.2307/2527342){:target="_blank"}. Within a group a correct band holds each outcome independently with its nominal probability, so the coverage test is the exact binomial test of unconditional coverage ([Christoffersen, 1998, section 3.1](https://doi.org/10.2307/2527341){:target="_blank"}; the likelihood-ratio version is [Kupiec's (1995)](https://doi.org/10.3905/jod.1995.407942){:target="_blank"}), exact because a group holds few rows. Uniformity of the PITs is a Kolmogorov-Smirnov test on the same groups. Both are bounded with Bonferroni over the horizons, the groups and the two bands.

How often each test flags a forecast that is right, a random walk forecast by its own distribution, over 2,000 repetitions:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/validation/test-size" alt="The share of correct forecasts flagged by the band and PIT tests, with every row treated as independent against origins grouped h years apart, for three designs" %}

| 23 yearly origins, four years ahead | Every row as independent | Non-overlapping groups |
|:--|--:|--:|
| Bands flagged | 0.502 | 0.004 |
| PIT flagged | 0.203 | 0.022 |

The cost is power. With a handful of independent outcomes per group, only a clear miss is flagged; a band that is a little too narrow passes. The verdicts below are therefore a floor: "too narrow" means clearly too narrow.

#### From the End of 2007

The model fitted on the 26 years before the end of 2007, 1,000 scenarios run five years ahead (seed 42):

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/validation/out-of-sample-2007" alt="Out-of-sample fan charts from the end of 2007 for US stocks, US unemployment, the US short and long rate and US and UK inflation, with the realised path" %}

The financial crisis falls outside the cloud in its first two years, because of its speed. US stocks were down 36.8% at the end of 2008 and 20.1% at the end of 2009, against 5th percentiles of -12.0% and -14.8%, and back inside from 2010. US unemployment reached 7.3% at the end of 2008, 9.9% at the end of 2009 and 9.3% at the end of 2010, while 1 in 20 scenarios went above 6.36%, 7.45% and 8.16%; only in 2011, at 8.5%, was it back inside the 90% band. The short rate was cut to 0.11% within 2008 against a 5th percentile of 1.05%; from 2009 on, the band's lower edge is the zero bound itself, so the years at zero are inside it, though in the band's tail (PITs of 0.08 to 0.21) and with a median between 2.7% and 3.0%. The 10-year rate fell to 2.24% against 2.78% in 2008 and was inside from 2009. US inflation dipped below the band at the end of 2008 (0.09% against 1.27%) and came back inside it. UK inflation went above its narrow band in three of the five years (3.08%, 3.15% and 3.60% at the ends of 2008, 2010 and 2011, against 95th percentiles near 3.0%): fitted from 1993, the UK's two inflation regimes sit close together. In the scores, the 90% band held four of the five years for both US rates and for US inflation, three for stocks, and two for unemployment and UK inflation; on CRPS the scenarios lose to a no-change forecast only for stocks.

The neutral rate the rule settles at was the one known then: 2.14%, the New York Fed's Laubach-Williams estimate published on 20 December 2007, where a run today reads 1.2%. Estimates of the neutral rate only came down over the following decade, and a backtest that read today's value would carry into 2007 a lesson learned afterwards.

#### From the End of 2019

Through the pandemic and the inflation that followed:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/validation/out-of-sample-2019" alt="Out-of-sample fan charts from the end of 2019 for US stocks, US unemployment, the US short and long rate and US and UK inflation, with the realised path" %}

US stocks stay inside the 90% band in all five years, through the 2020 crash and the rally after it. The jump in US unemployment to 6.7% at the end of 2020 is above the band's 5.34%, and the cut to zero lies below it: the short rate at 0.07% against a 5th percentile of 0.39%, the 10-year rate at 0.92% against 1.33%. From 2021 both rates are back inside. The inflation that followed is outside: US inflation of 7.04% at the end of 2021 and 6.45% at the end of 2022 is above the 95th percentiles of 4.07% and 4.48%, back inside from 2023, and UK inflation stays above its band for four years running, 4.84%, 9.24%, 4.15% and 3.52% at the ends of 2021 to 2024 against 95th percentiles of 3.21%, 3.30%, 3.43% and 3.40%. This fit read a US neutral real rate of 0.5%, the FOMC's December 2019 projection less its 2% goal. Unemployment's CRPS skill is -0.03: after the jump of 2020 it fell back, and standing still would have done as well.

#### From the End of 2021

Fitted with 2021's inflation already in the data, four years have happened so far:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/validation/out-of-sample-2021" alt="Out-of-sample fan charts from the end of 2021 for US stocks, US unemployment, the US short and long rate and US and UK inflation, with the realised path to the latest month published" %}

Here US inflation is inside the band in all four years: at the end of 2022 it was 6.45% against a median of 6.60%, and it came down faster than the median after that, landing in the lower half of the cloud (PITs of 0.20 to 0.29). US stocks stay inside (down 18.2% at the end of 2022 against a 5th percentile of -27.3%), and so does unemployment, which stayed in the lower half of its band, so on CRPS the scenarios lose to a no-change forecast (skill -0.74). The rate rises of 2022 go just past the band: the short rate at 4.26% at the end of 2022 against a 95th percentile of 4.06%, the 10-year rate at 3.88% against 3.82%, both inside from 2023. UK inflation of 9.24% at the end of 2022 is far above its 95th percentile of 5.16% and back inside from 2023.

#### Twenty-Three Origins

A crisis is an anecdote. Every year end from 2000 to 2022, each fitted on what was known then and run four years ahead (1,000 scenarios, seed 42), scores each year from 2001 to 2025 up to four times. The UK factors start in 2003: fitted from 1993, UK inflation needs ten years of history, and the UK rates, unemployment and the pound read it.

| Factor | Origins | Coverage 50% | Coverage 90% | Bands | PIT mean | CRPS skill |
|:--|--:|--:|--:|:--|--:|--:|
| US inflation | 23 | 0.54 | 0.90 | ok | 0.59 | 0.36 |
| Euro-area inflation | 23 | 0.57 | 0.85 | ok | 0.53 | 0.41 |
| UK inflation | 20 | 0.28 | 0.67 | ok | 0.59 | 0.37 |
| US short rate | 23 | 0.56 | 0.93 | ok | 0.43 | 0.37 |
| US long rate | 23 | 0.55 | 0.86 | ok | 0.37 | 0.22 |
| Euro-area short rate | 23 | 0.37 | 0.66 | too narrow | 0.40 | 0.36 |
| Euro-area long rate | 23 | 0.47 | 0.75 | ok | 0.38 | 0.17 |
| UK short rate | 20 | 0.65 | 0.85 | ok | 0.55 | 0.33 |
| UK long rate | 20 | 0.43 | 0.84 | ok | 0.38 | 0.21 |
| US unemployment | 23 | 0.21 | 0.63 | too narrow | 0.31 | 0.32 |
| Euro-area unemployment | 23 | 0.24 | 0.58 | too narrow | 0.42 | 0.25 |
| UK unemployment | 20 | 0.28 | 0.58 | too narrow | 0.29 | 0.00 |
| US stocks | 23 | 0.38 | 0.82 | ok | 0.58 | 0.44 |
| US small caps | 18 | 0.62 | 0.97 | ok | 0.52 | 0.42 |
| European stocks | 13 | 0.67 | 0.98 | ok | 0.47 | 0.36 |
| Japanese stocks | 22 | 0.64 | 0.94 | ok | 0.43 | 0.14 |
| Emerging-market stocks | 15 | 0.54 | 0.98 | ok | 0.41 | 0.14 |
| Euro | 23 | 0.51 | 0.95 | ok | 0.56 | 0.37 |
| Pound sterling | 20 | 0.53 | 0.89 | ok | 0.65 | 0.24 |
| Yen | 23 | 0.48 | 0.82 | ok | 0.53 | 0.29 |
| Gold | 18 | 0.41 | 0.86 | ok | 0.65 | 0.38 |
| Crude oil | 11 | 0.67 | 0.93 | ok | 0.46 | 0.33 |
| US house prices | 23 | 0.38 | 0.63 | too narrow | 0.56 | 0.24 |
| Yield-curve level | 23 | 0.58 | 0.90 | ok | 0.42 | 0.19 |
| Yield-curve slope | 23 | 0.43 | 0.91 | ok | 0.56 | 0.44 |
| Yield-curve curvature | 23 | 0.49 | 0.84 | ok | 0.38 | 0.29 |
| Leading indicator | 22 | 0.39 | 0.79 | too narrow | 0.51 | 0.30 |

Every factor beats a no-change forecast on CRPS except UK unemployment, which ties it. Inflation and the US rates hold their bands best: US inflation and the US short rate keep 90% and 93% of their years inside the 90% band. Where the model falls short, the bands are too narrow, and clearly so for unemployment in all three economies (0.58 to 0.63), the euro-area short rate (0.66), US house prices (0.63) and the leading indicator. UK inflation's band holds only 0.67, the cost of its 1993 sample, though the test, with its few independent outcomes, does not call it. The rates lean low: PIT means of 0.37 to 0.43 for five of the six rates say they ended below the scenarios' middle more often than above it, as the long years near zero did.

The model's choices were tested on the five origins four years apart (2003, 2007, 2011, 2015 and 2019) and two more; the other eighteen are a holdout, and fourteen of them were never used for any choice. The scores barely move between them, which is the sign that the choices did not fit the test set:

| Origins | All 27 factors, 90% coverage | All 27 factors, CRPS skill | Six rates, 90% coverage | Six rates, CRPS skill |
|:--|--:|--:|--:|--:|
| The five used for choices | 0.81 | 0.31 | 0.78 | 0.29 |
| The eighteen others | 0.83 | 0.29 | 0.82 | 0.27 |
| The fourteen never used | 0.83 | 0.29 | 0.81 | 0.27 |

### Crises against the Bundled Regimes {#crises-against-the-bundled-regimes}

The baseline is a model of ordinary times, fitted on a few decades, and the fans above show the crises it does not reach in their first year. That is what the [regimes](/projects/financescenarios/docs/regimes) are for. Each chart below starts from the same past origin and the same calibration as the fan, and runs it twice: without a regime, and with the bundled regime written for that crisis. The test is whether the library covers the event, not whether the model foresaw it: the COVID and 2022 regimes are written from those very episodes' published paths, so their reaching them shows they are calibrated to what happened, and timed from the origin they are a month or two early. The financial-crisis regime is the fairer test, since it sets no levels and only keeps the scenarios where stocks fall, unemployment rises and rates are cut together.

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/validation/crisis-2008" alt="From the end of 2007, US stocks, US unemployment and the US short rate without a regime and with the Financial Crisis regime, against what happened" %}

**2008: the financial-crisis regime does not reach it.** It moves the cloud the right way, but not far enough. US stocks fell 48.2% to their low of February 2009; by then 1 in 20 scenarios had fallen 16.4% without the regime and 26.1% with it, and the regime's lowest 5th percentile over the five years is -37.4%. US unemployment peaked at 10.0% in October 2009; by then 1 in 20 scenarios had reached 7.5% without the regime and 9.4% with it, so the peak lies just outside, and the regime's 95th percentile reaches 10.9% only later. The short rate's fall to zero is inside both, and with the regime it is the median path.

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/validation/crisis-2020" alt="From the end of 2019, US unemployment, US stocks and the US short rate without a regime and with the COVID Crash and Rebound 2020 regime, against what happened" %}

**2020: the COVID regime reaches it.** Without a regime, 1 in 20 scenarios took US unemployment above 4.3% by April 2020; it reached 14.8%. With the regime the scenarios reach 14.8% two months early, in February, because the regime counts its months from the origin while the pandemic began in March, and they fall back as unemployment did. US stocks were down 19.5% at the end of March 2020, beyond the baseline's 5th percentile of -7.1% and inside the regime's -37.5%. The cut to zero is the regime's median path.

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/validation/crisis-2022" alt="German inflation from the end of 2021 with and without the Energy War Shock 2022 regime, and US inflation from the end of 2020 with and without the 2022 Inflation and Rate Hikes regime, against what happened" %}

**2022: both inflation regimes reach it, each from its own start.** German inflation, which the euro-area inflation of the default set follows, peaked at 8.6% at the end of 2022; from the end of 2021, 1 in 20 scenarios had reached 6.3% without a regime and 9.9% with the energy-war regime. US inflation peaked at 9.1% in June 2022. The 2022 inflation regime replays the surge from January 2021, so this panel starts at the end of 2020: without it, 1 in 20 scenarios had reached 4.1% by then; with it, 9.7%. The UK has no regime of its own for 2022: its 9.2% at the end of 2022, far above the fan from the end of 2021, is left to a user's own regime or to the broader inflation regimes.

### Dated Values: What a Backtest Could Have Known {#dated-values}

A backtest is only honest if the model it fits could have been built on the day it starts from. Cutting every data series at that date is the obvious half. The other half is easy to miss: a calibration also reads values that are published rather than fitted, such as the neutral real rate of the policy rule, the natural rate of unemployment, long-run inflation expectations, the inflation target, the lowest policy rate and the long-run equity premium. Read as they stand today, they carry what happened afterwards into the past. A 2007 fit that reads today's neutral rate has already learned what the decade after 2007 taught.

So a calibration as of a past date reads each of these values as it had been published by that date, from its official history. Every release becomes a row from the day it was published, and a run as of a date reads the latest row on or before it. The run's notes list each value it read with its source and release. A run of today reads today's values.

| Value | Read today | How a past date reads it | Rows |
|:--|:--|:--|--:|
| Neutral real rate, US | 1.2% | From 25 January 2012: the FOMC's median longer-run federal funds rate less its 2% goal, from each [Summary of Economic Projections](https://fred.stlouisfed.org/series/FEDTARMDLR){:target="_blank"}. Before: the New York Fed's [real-time Laubach-Williams estimates](https://www.newyorkfed.org/research/policy/rstar){:target="_blank"}, the last quarter's one-sided estimate of each vintage from its publication date (8 July 2005 to 27 October 2011) | 263 |
| Neutral real rate, euro area | 0.09% | The New York Fed's real-time Holston-Laubach-Williams estimates, each vintage from its publication date (3 March 2016 to 26 August 2026) | 210 |
| Neutral real rate, UK | 1.0% | The Holston-Laubach-Williams real-time estimates from March 2016 to May 2018; then the midpoint of the Bank of England's range: 0.5% from 2 August 2018 ([Inflation Report August 2018, Box 6](https://www.bankofengland.co.uk/inflation-report/2018/august-2018){:target="_blank"}), 1.0% from 6 February 2025 ([Monetary Policy Report February 2025, Box A](https://www.bankofengland.co.uk/monetary-policy-report/2025/february-2025){:target="_blank"}) | 232 |
| Longer-run unemployment, US | 4.2% | The FOMC's median from 17 June 2015 and the midpoint of its central tendency from 18 February 2009 ([FRED UNRATEMDLR and UNRATECTMLR](https://fred.stlouisfed.org/series/UNRATEMDLR){:target="_blank"}); before 2009, the Congressional Budget Office's noncyclical rate in its [earliest ALFRED vintage](https://alfred.stlouisfed.org/series?seid=NROU){:target="_blank"} (2 February 2011) | 311 |
| NAWRU: France, UK, Germany | 7.16%, 4.21%, 3.48% | Each release in the European Commission's [AMECO archive](https://economy-finance.ec.europa.eu/economic-research-and-databases/economic-databases/ameco-database/ameco-archive_en){:target="_blank"}, Spring 2011 to Autumn 2025, the NAWRU for its last forecast year; Spring 2026 today | 220 |
| Long-run inflation expectations, US | 2.3% | The [Survey of Professional Forecasters'](https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/inflation-forecasts){:target="_blank"} median 10-year CPI inflation from each release date since 1991Q4; before, the Blue Chip Economic Indicators and the Livingston Survey from 1979Q4 | 166 |
| Long-run inflation expectations, euro area | 2.0% | The [ECB Survey of Professional Forecasters'](https://data.ecb.europa.eu/data/datasets/SPF){:target="_blank"} longer-term HICP expectation, each round since 1999Q1 | 105 |
| Inflation target and the UK's expectation | 2% | The target in force: the Federal Reserve's 2% from 25 January 2012 ([FOMC, Statement on Longer-Run Goals](https://www.federalreserve.gov/monetarypolicy/files/fomc_longerrungoals.pdf){:target="_blank"}) and [Taylor's (1993, p. 202)](https://doi.org/10.1016/0167-2231(93)90009-L){:target="_blank"} 2% before; the ECB's 2% (below 2% from 13 October 1998, below but close to 2% from 8 May 2003, a symmetric 2% from 8 July 2021); the UK's 2.5% RPIX until 10 December 2003, then 2% CPI ([Bank of England, Inflation Report February 2004](https://www.bankofengland.co.uk/inflation-report/2004/february-2004){:target="_blank"}) | 12 |
| Lowest policy rate | US 0%, euro -0.50%, UK 0.10% | Zero until a central bank set a lower rate: the ECB's [deposit facility rate](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/html/index.en.html){:target="_blank"} at each cut from 0% on 11 July 2012 to -0.50% on 18 September 2019, [Bank Rate](https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp){:target="_blank"} at 0.10% from 19 March 2020 | 11 |
| Long-run equity premium | 3.77% | [Jordà, Knoll, Kuvshinov, Schularick and Taylor (2019, Table II)](https://doi.org/10.1093/qje/qjz012){:target="_blank"} from 2019; before, the same statistic on the [JST Macrohistory Database](https://www.macrohistory.net/database/){:target="_blank"} up to each year, from 1900 to 2018 | 120 |

Before a table's first real-time release (mid-2005 for the US neutral rate, 2016 for the euro area's, 2009 for US unemployment, mid-2011 for the NAWRU), the first release's estimate for that quarter or year stands in. It was made later, but on data only up to that quarter, the closest to real time there is; the run's notes name the release each value comes from.

The neutral rate matters most. At 11 of the 15 pairs of origin and currency (the ends of 2003, 2007, 2011, 2015 and 2019, for three currencies), the backtests read a neutral rate above today's. At the end of 2007 the Laubach-Williams estimate published on 20 December read 2.14% for the US, against 1.2% today, and the first Holston-Laubach-Williams vintage puts the euro area's at 2.24%, against 0.09%. The FOMC's own projection of the longer-run funds rate stood at 4.3% in January 2012, 2.3% above its goal, and fell to 2.5% only in 2019. A rule given those numbers expects rates to return to normal, as the FOMC's projections did through the 2010s, while rates stayed near zero.

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/validation/dated-neutral-rates" alt="The neutral real rate as known on each day since 2000 for the US, the euro area and the UK, with the value each backtest origin reads and today's value" %}

Long-run inflation expectations moved far less once they had come down: US forecasters expected 6.9% a year over the next decade at the end of 1979, but since 1999 their expectation has stayed between 2.0% and 3.0% (2.3% today), and the euro area's between 1.6% and 2.2%.

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/validation/dated-inflation-expectations" alt="Long-run inflation expectations as published since 1979: the US 10-year CPI expectation, the ECB survey's longer-term expectation and the UK target" %}

The natural rate of unemployment was revised with what unemployment did: France's NAWRU read 8.8% at the end of 2007, 10.0% at the end of 2015 and 7.16% today; the UK's 6.0%, 5.8% and 4.21%.

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/validation/dated-unemployment" alt="The US longer-run unemployment rate and the French and UK NAWRU as known on each day since 2000" %}

The equity premium on the data up to each year ranges from 0.74% (up to 1932) to 4.10% (up to 1999); a backtest from the end of 2007 reads 3.96%, one from the end of 2019 the published 3.77%.

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/validation/dated-equity-premium" alt="The long-run equity premium computed on the JST data up to each year from 1900 to 2018, and the published 3.77%" %}

### External Benchmarks {#external-benchmarks}

The checks above compare the model with itself and its own data. The benchmarks below compare a calibrated factor with independent sources. Each reference embeds its own model choices, so a gap is not automatically an error, but a large or systematic one needs explaining. Four references are used:

| Benchmark | What is compared | Note |
|:----------|:-----------------|:-----|
| NAIC GOES | A US Treasury rate's simulated percentile bands, and a run against GOES's own acceptance criteria | Differences by percentile, and a pass or fail per criterion |
| DNB scenario set | A run's interest rate, inflation or equity, quantile by quantile at every whole year | A regulator-reviewed reference for a euro run |
| Corporate bond panel | Credit spread levels and their dispersion across individual bonds | Validates spread levels, not rating migration |
| Option-implied densities | A risk-neutral equity's terminal-price distribution | Tests the flat-volatility lognormal assumption |

- **NAIC GOES.** The Generator of Economic Scenarios, the prescribed generator of the NAIC Valuation Manual for US principle-based reserves (VM-20 for life, VM-21 for variable annuities), run by Conning for the NAIC. Prescribed is not mandatory: a company may use its own generator if the result meets the Valuation Manual's standard in section 2.G ([NAIC Valuation Manual, 2026 edition, VM-20 Appendix 1, Section E](https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf#page=132){:target="_blank"}).

  A US Treasury rate's simulated percentile bands are compared with the percentile grid of NAIC's 10,000-scenario set for the matching tenor; the result is a set of differences, not a pass or fail. `check_acceptance` adds the pass or fail: it holds the run to the criteria NAIC sets GOES itself ([below](#goes-acceptance-criteria)). A large gap usually means the long-run level or the volatility differs from what US regulators consider a reasonable real-world spread of rates.
- **DNB scenario set.** De Nederlandsche Bank publishes a scenario set every quarter: 20,000 scenarios over 100 years from the Commissie Parameters 2022 model, both real world (the P-set) and market consistent (the Q-set, calibrated to market prices including swaptions). A run's interest rate, inflation or equity is compared with it at every whole year, quantile by quantile: rates and inflation by level, equities by yearly return. It is a regulator-reviewed reference for a euro run and the only free swaption-consistent one. `Dnb.compare_moments` and `Dnb.compare_correlations` set a run's means, standard deviations, percentiles and correlations beside the set's, year by year; the `dnb` factor set, which runs DNB's own model ([CP2022](/projects/financescenarios/docs/interest-rates#cp2022-model)), lands within Monte Carlo error of it. The same sets, and NAIC's 16 deterministic stress scenarios for US rates (the set of the Valuation Manual's Stochastic Exclusion Ratio Test, SERT), can also replace factors in a run (see the [configuration reference](/projects/financescenarios/docs/configuration)).
- **Corporate bond panel.** Credit spreads are fitted to one aggregate index per maturity bucket. The Open Source Bond Asset Pricing panel (Dickerson, Robotti and Rossetti; built on TRACE trades from 2002 to 2025, tens of millions of bond-date rows) shows the spread distribution of the individual bonds underneath. The comparison shows whether the aggregate's fitted level and volatility represent the real dispersion or smooth over fatter tails and idiosyncratic widening. The public data has no credit ratings, so it validates spread levels, not rating migration.
- **Option-implied densities.** A risk-neutral equity's simulated terminal-price distribution is compared with the market's own risk-neutral density at the nearest listed expiration, extracted from option prices with the [Breeden-Litzenberger (1978)](https://doi.org/10.1086/296025) result. Both sides come from the same market, so this tests the flat-volatility lognormal assumption rather than providing an outside view. The headline number is the Wasserstein distance (how far apart the two terminal-price views are, on average, in price units); a Kolmogorov-Smirnov statistic flags a sharp local tail mismatch the average could hide. Expect a gap: the market's density is skewed and fat-tailed, the model's is not.

#### GOES Acceptance Criteria {#goes-acceptance-criteria}

NAIC holds GOES itself to a set of acceptance criteria, published with each release on its workbook's `Acceptance Criteria_Dashboard` sheet. A company that uses its own generator must meet the Valuation Manual's requirements ([VM-20, Appendix 1](https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf#page=132){:target="_blank"}), so holding a run to the bar GOES clears shows how close it comes. `NaicGoes.check_acceptance` reads the thresholds from the release, so they follow NAIC's revisions, and checks:

| Criterion | What it checks |
|:--|:--|
| T1 | The upper tail: the 99.5th percentile of the 1-year and 20-year yields, and the share of scenarios that ever cross the cap |
| T2 | Negative rates: the lowest 1-year and 20-year yields |
| T4 | Low for long: the share of scenarios whose 20-year yield averages below a floor for ten and thirty years |
| T5 | The spread of the 20-year yield's 20-year geometric averages |
| T6 | Mean reversion: the 1-year and 20-year medians in year 30 |
| E1 | The S&P 500's gross wealth factors, percentile by percentile |

The criteria are written on the 1-year and 20-year yields, which no index quotes; a run that does not simulate them has them read off its neighbouring tenors in a straight line (3-month and 5-year, 10-year and 30-year). E1 publishes targets but no tolerance, so each percentile passes within 10% of its target (`tolerance`), a judgement: GOES's own factors sit within 7.2% of the targets from the 1st to the 99th percentile.

```python
from financescenarios import Scenarios
from financescenarios.validation.naic_goes.naic_goes_controller import NaicGoes

scenarios = Scenarios.from_profiles(settings="goes", factor_set="goes")
result = scenarios.simulate(years=30, n_simulations=10_000)
NaicGoes(vintage="20260930").check_acceptance(result, scenarios.config, equity_name="us_broad")
```

The `goes` factor set is built on what NAIC and the American Academy of Actuaries publish. Its 3-month, 5-year, 10-year and 30-year yields are each a one-factor CIR: the speed is ln 2 / 15, the 15-year half-life behind T6; the long-run level is GOES's mean over years 20 to 30; and the volatility puts the exact year-30 median on GOES's. Its stocks are fitted on Shiller's S&P total return since 1946, shifted so the long-run return is E1's own median of 7.41% a year (GOES's 3.73% cash plus 3.68%), and earn their premium over that long-run level rather than over the simulated rate, as the GOES Subgroup decided when it removed the old generator's equity-rate link. Against the release of 30 September 2026, with 10,000 scenarios, GOES's own count:

| Check | GOES | `goes` set |
|:--|--:|--:|
| 3-month yield, 50th / 95th / 99th percentile in year 30 | 2.80 / 10.88 / 15.42% | 2.76 / 11.03 / 16.55% |
| 3-month yield, 50th / 95th / 99th percentile in year 10 | 3.21 / 10.61 / 14.13% | 3.29 / 9.56 / 13.21% |
| 10-year yield, 50th / 99th percentile in year 30 | 4.50 / 14.83% | 4.44 / 14.33% |
| T1: 1-year 99.5th percentile, highest (at most 18%) | 17.65% | 16.87%, pass |
| T1: 20-year 99.5th percentile, highest (at most 17%) | 16.41% | 15.84%, pass |
| T1: share ever above the cap, 1-year / 20-year (at most 0.5%) | 3.06 / 2.57% | 1.60 / 1.06%, fail |
| T2: lowest 1-year (at least -1%) | pass | -0.04%, pass |
| T2: lowest 20-year (at least 0%) | pass | 0.03%, pass |
| T4: low for long over 10 / 30 years (at least 7.5 / 3.75%) | 3.44 / 2.87%, fail | 0.00 / 0.59%, fail |
| T5: 99th percentile of the 20-year averages, 10 / 30 years | 10.01 / 10.61% | 8.88 / 10.38%, fail (bounds 9.00 / 10.54%) |
| T6: 1-year median in year 30 (1.31 to 3.35%) | 3.09% | 3.05%, pass |
| T6: 20-year median in year 30 (3.35 to 4.89%) | 4.83% | 4.66%, pass |
| E1: median gross wealth factor in year 30 (9.23) | 9.26 | 9.49 |
| E1: percentiles within 10% of their targets | 40 of 40 | 40 of 40 |

<div class="fs-callout fs-callout--limits" markdown="1">
<p class="fs-callout__title">Where the goes set still misses GOES</p>

- **T4, low for long.** GOES fails it too. A CIR 20-year rate almost never averages below 1.45% for ten years; GOES gets closer with its flooring mechanisms.
- **T1's share of scenarios ever above the cap.** It is 1.6% against a limit of 0.5%, though GOES's own share is 3.06% and the dashboard does not judge it.
- **T5's upper tail** is about 0.1 to 0.2 points short. The bounds are interpolated at the run's own starting 20-year yield, about 5.1%, not GOES's 5.68%.
- **The first ten years** are narrower than GOES's: the 3-month 99th percentile is 13.2% against 14.1% in year 10. One CIR factor per tenor cannot widen the early years without overshooting year 30, and NAIC publishes neither a two-factor specification nor its parameters.
- **Corporate bond funds** (C1) are not modelled.
</div>

### Published Models: Reproducing Their Papers {#published-parameter-mode}

The `ahlgrim`, `hibbert` and `wilkie` factor sets run their papers' models with the papers' own parameters, correlations and starting values, and read no data (see [published frameworks](/projects/financescenarios/docs/configuration#published-frameworks)). That makes them checkable: run as the paper ran, from its start date and over its horizon, each should reproduce the tables its paper reports for its own model. `compare_published` runs the check:

```python
from financescenarios.validation.published_frameworks.published_frameworks_controller import compare_published

compare_published("wilkie")
```

Which returns every reported mean, standard deviation, percentile and correlation next to the simulated one (the first 3 of 91 rows):

| source | variable | statistic | horizon | published | simulated | tolerance | within |
|:-------|:---------|:----------|--------:|----------:|----------:|----------:|:-------|
| Table 3 | GQ | mean | 1.0 | 0.0537 | 0.0538 | 0.0076 | true |
| Table 3 | GQ | mean | 5.0 | 0.0537 | 0.0531 | 0.0055 | true |
| Table 3 | GQ | mean | 10.0 | 0.0514 | 0.0526 | 0.0043 | true |

A difference counts as Monte Carlo error when it is within four standard errors of the gap between the paper's estimate and the run's (batch means, scaled to the paper's number of scenarios), plus half the paper's last printed digit. Four standard errors keeps the chance of a false alarm across a table of a few dozen checks near 1%. With 10,000 scenarios:

| Paper | Table | Checked | Within Monte Carlo error |
|:------|:------|--------:|-------------------------:|
| Ahlgrim, D'Arcy and Gorvett (2005) | Table 1 (year-1 and year-50 means, year-10 1st and 99th percentiles) and Table 2's inflation-rate correlation | 26 | 26 |
| Hibbert, Mowbray and Turnbull (2001) | Exhibit 7.2A (equities, cash, inflation) | 11 | 11 |
| Wilkie (1986) | Table 3, every cell, on his yearly step | 91 | 91 |

A few of those numbers, paper against run:

| | Paper | Run |
|:--|--:|--:|
| Ahlgrim: inflation against the nominal short rate, year 1 | 0.906 | 0.907 |
| Ahlgrim: nominal short rate, mean in year 50 | 7.8% | 7.8% |
| Ahlgrim: unemployment, 1st to 99th percentile in year 10 | 3.5% to 8.7% | 3.5% to 8.8% |
| Hibbert: equity log return over cash | 2.5% | 2.4% |
| Hibbert: cash, mean and standard deviation | 5.0% / 3.5% | 5.0% / 3.4% |
| Wilkie: one-year share return against inflation, correlation | -0.24 | -0.23 |
| Wilkie: real share return at 50 years | 4.45% | 4.39% |

<div class="fs-callout fs-callout--limits" markdown="1">
<p class="fs-callout__title">What still differs from the papers</p>

- **Ahlgrim:** small stocks, the 1-year and 10-year yields of the closed-form bond prices and the first-period 1-month yields are not simulated; the equity regimes are lognormal with the moments of the workbook's normal simple returns, and equities earn the floored nominal rate.
- **Hibbert:** calibration A only. Calibration B adds risk premia that exist to price bonds, which the package does not do, so its floors and reflection are left out, as are the bond rows of Exhibit 7.2A.
- **Wilkie:** the set runs his yearly step. On a monthly step four cells at one and five years fall outside Monte Carlo error (the Consols-inflation correlation at one year is -0.22 against -0.42), because a monthly run's inflation is a year-on-year rate read every month.
- **Data:** Wilkie's UK series (1919-1982), NCREIF and Hibbert's UK calibration data are not available here, so the parameters are used as published and nothing is refitted. Hibbert's and Wilkie's models have no unemployment, so their sets simulate none.
</div>

### How the Published Models Held Up {#published-models-held-up}

Because each reference set starts from its paper's own date, each is a forecast made years ago, which can now be checked against what happened. `held_up` runs a set from its paper's start and places every year since in its fan:

- Ahlgrim, D'Arcy and Gorvett from June 2004, on US data;
- Hibbert, Mowbray and Turnbull from end-March 2001, on UK data;
- Wilkie from his neutral start, dated 1986, on UK data.

All of the history is the OECD's and needs no key: the short and long rates, year-on-year CPI inflation, unemployment, share prices and US house prices.

```python
from financescenarios.validation.published_frameworks.published_frameworks_controller import held_up

rows, scores = held_up("wilkie")  # the fan and the realized value per year, and the scores per factor
```

| Model | Factor | Years | Inside 50% band | Inside 90% band | Mean PIT | CRPS skill vs no change |
|:--|:--|--:|--:|--:|--:|--:|
| Ahlgrim (US, 2004) | Short rate | 22 | 36% | 100% | 0.24 | -0.67 |
| | Inflation | 22 | 59% | 100% | 0.36 | -0.02 |
| | Unemployment | 22 | 14% | 45% | 0.37 | +0.19 |
| | Share prices (growth since start) | 22 | 23% | 100% | 0.26 | -1.20 |
| | Real estate (vs house prices) | 22 | 36% | 82% | 0.27 | +0.29 |
| Hibbert (UK, 2001) | Short rate | 24 | 33% | 100% | 0.24 | +0.40 |
| | Inflation | 25 | 72% | 96% | 0.47 | +0.41 |
| | Share prices (growth since start) | 25 | 44% | 96% | 0.23 | -1.62 |
| Wilkie (UK, 1986) | Inflation | 40 | 93% | 100% | 0.37 | +0.33 |
| | Long yield (vs the 10-year gilt) | 40 | 13% | 28% | 0.19 | +0.48 |
| | Share prices (growth since start) | 40 | 70% | 100% | 0.64 | +0.66 |

A calibrated fan holds about half the years in its 50% band and nine in ten in its 90% band, with a mean PIT near 0.5. A skill above zero means the fan's CRPS beat a forecast that the value stays where it started (zero growth for share prices).

{% include ft-chart.html id="validation-held-up-ahlgrim" src="/assets/data/financescenarios-guides/validation-held-up.json" label="5th percentile, median and 95th percentile of Ahlgrim, D'Arcy and Gorvett's model from June 2004 and what happened in the US, year by year" %}

**Rates.** None of the three models allowed for a decade of rates near zero. Ahlgrim's median US short rate rises toward 7.6% (a 2.8% real rate plus 4.8% inflation). Hibbert's UK median holds at 5% for 30 years. The realized rates sat near zero from 2009 to 2021, in the lower tail of both fans, though still inside their 90% bands; that gives mean PITs of 0.24. Wilkie's long yield fared worst. His model reverts the real yield to 3.5% on top of about 5% expected inflation, so its median stays near 8.5%. The 10-year gilt fell from about 10% in 1986 to below his 5th percentile in 27 of the 40 years from 1999 on, and was 4.4% in 2026 against a median of 8.7%. Wilkie's CRPS still beats "no change" only because no change means staying at 1986's 10%.

{% include ft-chart.html id="validation-held-up-wilkie" src="/assets/data/financescenarios-guides/validation-held-up.json" label="5th percentile, median and 95th percentile of Wilkie's model from his neutral start, dated 1986, and what happened in the UK, year by year" %}

**Inflation.** The fans held inflation well. Wilkie's 5% mean with wide bands kept 93% of UK years inside its 50% band; that is too many, which means the bands were wider than needed. Hibbert's 2.5% target matched the Bank of England's era (72% inside the 50% band); only 2023's 10% spike went above the 95th percentile. Ahlgrim's 4.8% mean sits above the 2.5% the US averaged, so realized years fell below the median (mean PIT 0.36).

**Unemployment.** Ahlgrim's band was far too narrow: about 4.3% to 8.0% at every horizon. That band comes from the workbook's monthly unemployment step, which Table 1 shows. US unemployment went above the 95th percentile in 2009 to 2012 and in 2020, and below the 5th in 2018, 2019 and every year from 2022 to 2026. Only 45% of years fell inside the 90% band.

**Share prices.** The fans are wide, so the 90% bands held almost every year. The medians differ. Ahlgrim's and Hibbert's equity premia, taken from long histories, put their medians well above what the OECD's US and UK share price indices did; the UK index was up 79% in 25 years against Hibbert's median of 194%. Their CRPS skill is negative. Wilkie's median for UK share prices sits close to the realized growth (626% against 634% by 2026).

{% include ft-chart.html id="validation-held-up-hibbert" src="/assets/data/financescenarios-guides/validation-held-up.json" label="5th percentile, median and 95th percentile of Hibbert, Mowbray and Turnbull's model from March 2001 and what happened in the UK, year by year" %}

**Real estate.** Ahlgrim models NCREIF's commercial property returns; the nearest keyless history is US house prices. The 2008 to 2011 fall went below the 5th percentile in all four years.

What these numbers are not: one path of history scored year by year. The years overlap in what they test, so the shares describe what happened rather than test calibration. The comparisons also use OECD stand-ins for the papers' own series: a 3-month rate for a 1-month one, a 10-year gilt for Consols, share price indices for total-return indices, and house prices for NCREIF. Wilkie's run starts from his neutral values (5% inflation, an 8.5% long yield), not from 1986's actual market.

### Published Calibrations {#published-calibrations}

A published calibration is fixed under a version tag, passes the checks above before release, and records its data window, package versions and a hash of its configuration. A run can then state exactly which calibration it used, and anyone can reproduce its scenarios offline. A release whose configuration no longer matches its hash is refused rather than silently mixing two sets of assumptions. Reference calibrations are meant to be published once a year, the minimum frequency EIOPA sets for these tests ([Guidelines on valuation of technical provisions, Guideline 58, paragraph 1.106](https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en){:target="_blank"}).

Downloading and simulating a release is covered in the runs and releases reference.

<div class="fs-ref"><a href="/projects/financescenarios/docs/run-files#reference"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Runs and releases</a></div>

### What Is Not Validated {#what-is-not-validated}

<div class="fs-callout fs-callout--limits" markdown="1">
- **Dependence is one linear correlation matrix**, constant over the horizon. A Student-t shock distribution adds joint tail risk through one shared t-copula (see [fat tails](/projects/financescenarios/docs/simulation-engine#fat-tails-and-tail-dependence)), but tail dependence that differs by pair or is asymmetric is not captured.
- **Risk-neutral calibration is limited in scope.** Interest rates, inflation, equities, FX and commodities can be calibrated risk neutral, but without a full arbitrage-free volatility surface: rate and inflation volatilities come from history, not from swaption or inflation-option prices, so the time value of guarantees is indicative; see the [measures section of the configuration page](/projects/financescenarios/docs/configuration#real-world-and-risk-neutral-measures).
- **Judgment calls are not checked for economic sense.** The number of equity regimes and every belief override are the user's choice; only their shape is checked, not whether they are reasonable.
- **Out of sample rests on few independent outcomes.** Twenty-three yearly origins four years ahead leave as few as six non-overlapping outcomes per group at the four-year horizon, so the tests flag only clear misses. The published values a fit reads are dated, and each series waits for its first release, but the data are read as revised today, the US term premium is today's full-sample ACM estimate, natural rates before 2011 are 2011 vintages, and before each dated table's first real-time release a later estimate for that quarter or year stands in.
- **A regime that reaches a crisis was written after it.** The COVID and 2022 regimes replay those episodes' published paths; the financial-crisis regime, which sets no levels, does not reach the depth of 2008.
- **The relationship and realism bands are judgements.** Half to twice history's slope, and the margins around history's extremes, are not published standards; a warning is a reason to look, not a verdict. Newey-West errors still understate the uncertainty of very persistent levels.
- **No scenario reduction or moment matching.** Every simulated path is returned as drawn; none are selected or reweighted to match target moments with fewer scenarios.
</div>
