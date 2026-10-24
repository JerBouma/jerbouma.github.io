---
title: Out of Sample
seo_title: "Out of Sample | Finance Scenarios"
seo_title_suffix: false
excerpt: "How Finance Scenarios tests a model fitted in the past on only what was known then: PIT, coverage and the fair CRPS, tests that hold their size across overlapping origins, the crises of 2008, 2020 and 2022, and twenty-three origins."
description: "Out-of-sample backtests of Finance Scenarios: what a past fit may know, the PIT, coverage and CRPS scores, exact binomial coverage tests on non-overlapping origins, backtests from 2007, 2019 and 2021, and the crises against the regimes."
author_profile: false
permalink: /projects/financescenarios/docs/validation/out-of-sample
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/validation
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-validation"
---

The [checks against history](/projects/financescenarios/docs/validation) compare a run with the history it was fitted on. The harder test goes back to a past date, fits the model on only what was known then, simulates from that day and sets the scenarios against what actually happened. This page covers what such a fit may know, how its forecasts are scored and tested, the backtests from the ends of 2007, 2019 and 2021, twenty-three origins scored together, and the crises against the bundled regimes.

## What the Fit May Know

Every series the fit reads ends on that date, and a month counts only once it was published: consumer prices a month after the month ends, unemployment one month after in the US and two months after in the euro area and the UK, as the release calendars of the [Bureau of Labor Statistics](https://www.bls.gov/bls/histreleasedates.pdf){:target="_blank"}, the [Office for National Statistics](https://www.ons.gov.uk/releasecalendar){:target="_blank"} and [Eurostat](https://ec.europa.eu/eurostat/news/release-calendar){:target="_blank"} have it. A fit as of the end of 2007 sees US unemployment up to November. The published values it reads besides the data, such as the neutral real rate of the policy rule, the natural rate of unemployment and long-run inflation expectations, are the ones known that day (see [Dated Values](/projects/financescenarios/docs/validation/dated-values)).

Three reads stay today's, and every run's notes say so: OECD and FRED series are read as revised today, not as first published; the US term premium of the long rate is the New York Fed's ACM estimate as re-estimated today on the whole sample; and the natural rates of unemployment before 2011 come from the 2011 vintages of the Congressional Budget Office and the European Commission, which estimated those earlier years with later data. Beliefs, which are today's views, are reported too.

## Scoring a Forecast

Each factor is scored at every whole year ahead, with $$X$$ and $$X'$$ two independent scenarios and $$y$$ what happened:

- **PIT** (probability integral transform): where the realized value fell among the scenarios, the share below it. For a correct forecast it is uniform between 0 and 1, so its mean is 0.5 and its standard deviation $$1/\sqrt{12} = 0.289$$ ([Diebold, Gunther and Tay, 1998, section 3, pp. 867-868](https://doi.org/10.2307/2527342){:target="_blank"}).
- **Coverage**: how often the 50% and 90% bands held the outcome.
- **CRPS**: the continuous ranked probability score, $$E\vert X - y\vert - \tfrac{1}{2}E\vert X - X'\vert$$ ([Gneiting and Raftery, 2007, section 4.2, eq. 21, p. 367](https://doi.org/10.1198/016214506000001437){:target="_blank"}), which rewards a cloud that is both centered and tight; its skill against a forecast of no change shows whether the scenarios beat standing still. With $$n$$ scenarios (1,000 here), the second term averages over the $$n(n-1)$$ distinct pairs rather than all $$n^2$$: the fair CRPS of [Ferro (2014)](https://doi.org/10.1002/qj.2270){:target="_blank"}, whose expectation does not depend on how many scenarios are drawn.
- **Tails**: how often the scenarios go beyond history's worst and best year. If the run's $$T$$ years and history's $$N$$ come from one distribution, any of the $$N + T$$ years is equally likely to be the most extreme, so a $$T$$-year run goes past history's record with probability $$T/(N+T)$$.

## Tests That Hold Their Size

Coverage and PIT are tested across origins, and that is where overlap matters. With yearly origins and four-year horizons, neighboring forecasts share three years of outcomes: a miss in 2008 is a miss for the forecasts made at the end of 2004, 2005, 2006 and 2007 at once. A test that treats every row as an independent draw then flags a correct model far more often than its 5% (the test's size). So the rows of each horizon $$h$$ are split into groups of origins at least $$h$$ years apart, whose outcomes do not overlap; with yearly origins these are the $$h$$ interleaved subsequences of [Diebold, Gunther and Tay (1998, p. 880)](https://doi.org/10.2307/2527342){:target="_blank"}. Within a group a correct band holds each outcome independently with its nominal probability, so coverage is tested with the exact binomial test of unconditional coverage ([Christoffersen, 1998, section 3.1](https://doi.org/10.2307/2527341){:target="_blank"}; [Kupiec's (1995)](https://doi.org/10.3905/jod.1995.407942){:target="_blank"} is the likelihood-ratio version), exact because a group holds few rows. Uniformity of the PITs is tested with a Kolmogorov-Smirnov test on the same groups. Both are Bonferroni-corrected for the number of tests: the PIT test over the horizons and the groups, the coverage test over the two bands as well.

How often each test flags a forecast that is right, a random walk forecast by its own distribution, over 2,000 repetitions:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/validation/test-size" alt="The share of correct forecasts flagged by the band and PIT tests, with every row treated as independent against origins grouped h years apart, for three designs" %}

For the design of the twenty-three origins below:

| 23 yearly origins, four years ahead | Every row as independent | Non-overlapping groups |
|:--|--:|--:|
| Bands flagged | 0.502 | 0.004 |
| PIT flagged | 0.203 | 0.022 |

The cost is power, the chance of catching a model that is wrong. With a handful of independent outcomes per group, only a clear miss is flagged; a band that is a little too narrow passes. The verdicts below are therefore a floor: "too narrow" means clearly too narrow.

## From the End of 2007

The examples on this page use the calibration settings of the [overview](/projects/financescenarios/docs#simulating-scenarios), refitted as of each past date with 1,000 scenarios and seed 42. `out_of_sample` cuts every series at a date, fits the model on what was known then and simulates from that day; its table sets each year end against what happened. To run it from the end of 2007 for six variables:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)

factors = [
    "us_broad",
    "united_states_unemployment",
    "united_states_short_rate",
    "united_states_long_rate",
    "united_states_inflation",
    "united_kingdom_inflation",
]
crisis = scenarios.out_of_sample(as_of="2007-12-31", years=5, n_simulations=1000, seed=42, factors=factors)

crisis.table.select("factor", "date", "realized", "p5", "p50", "p95", "pit")
crisis.scores.select("factor", "coverage_50", "coverage_90", "pit_mean", "crps_skill")
```

The financial crisis falls largely outside the scenarios, because of its speed. US unemployment reached 7.3% at the end of 2008 and 9.9% at the end of 2009, while one scenario in twenty went above 6.36% and 7.45%; it was back inside the 90% band only in 2011, at 8.5%. The short rate was cut to 0.11% within the year against a 5th percentile of 1.05%, and US stocks were down 36.8% by the end of 2008 against a 5th percentile of -12.0%. In the scores, the 90% band held four of the five years for both rates and US inflation, three for stocks and two for unemployment and UK inflation; on CRPS the scenarios beat a no-change forecast for every variable except stocks. When plotted, one variable per tab:

{% include ft-chart.html id="validation-crisis" src="/assets/data/financescenarios-guides/validation.json" label="5th percentile, median and 95th percentile of six US and UK variables at each year end from 2008 to 2012, fitted on what was known at the end of 2007, against what happened" %}

What the fit knew is in the run's notes, each value with its source, and [Dated Values](/projects/financescenarios/docs/validation/dated-values) shows how each one is read as of a past date.

## From the End of 2019

The same test from the end of 2019 covers the pandemic and the inflation that followed. To run it:

```python
pandemic = scenarios.out_of_sample(as_of="2019-12-31", years=5, n_simulations=1000, seed=42, factors=factors)

pandemic.scores.select("factor", "coverage_50", "coverage_90", "pit_mean", "crps_skill")
```

Here the scenarios hold more. US stocks stay inside the 90% band in all five years, through the 2020 crash and the rally after it. The jump in US unemployment to 6.7% at the end of 2020 is above the 95th percentile of 5.34%, and the cut to zero lies below the band at first (0.07% against a 5th percentile of 0.38%); from 2021 both are inside. The inflation that followed does not fit: US inflation of 7.04% at the end of 2021 is above the 95th percentile of 4.07%, and UK inflation, fitted on its calm years since 1993, is above its narrow band from 2021 to 2024, at 9.24% in 2022 against 3.30%. When plotted, one variable per tab:

{% include ft-chart.html id="validation-pandemic" src="/assets/data/financescenarios-guides/validation.json" label="5th percentile, median and 95th percentile of six US and UK variables at each year end from 2020 to 2024, fitted on what was known at the end of 2019, against what happened" %}

## From the End of 2021

A fit as of the end of 2021 already has 2021's inflation in its data, and the four years since can be scored. The chart shows the fans against what happened:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/validation/out-of-sample-2021" alt="Out-of-sample fan charts from the end of 2021 for US stocks, US unemployment, the US short and long rate and US and UK inflation, with the realized path to the latest month published" %}

This time US inflation is inside the band in all four years: at the end of 2022 it was 6.45% against a median of 6.60%, and it came down faster than the median after that, landing in the lower half of the cloud (PITs of 0.20 to 0.29). US stocks stay inside (down 18.2% at the end of 2022 against a 5th percentile of -27.3%), and so does unemployment, though it stayed in the lower half of its band, so a no-change forecast beats the scenarios on CRPS (skill -0.74). The rate rises of 2022 go just past the band: the short rate at 4.26% at the end of 2022 against a 95th percentile of 4.06%, the 10-year rate at 3.88% against 3.82%, both inside from 2023. UK inflation of 9.24% at the end of 2022 is far above its 95th percentile of 5.16% and back inside from 2023.

## Twenty-Three Origins

A single crisis is an anecdote. Every year end from 2000 to 2022 serves as an origin, each fitted on what was known then and run four years ahead (1,000 scenarios, seed 42), so each year from 2001 to 2025 is scored up to four times. The UK factors start in 2003: fitted from 1993, UK inflation needs ten years of history, and the UK rates, unemployment and the pound depend on it.

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

Every factor beats a no-change forecast on CRPS except UK unemployment, which ties it. Inflation and the US rates hold their bands best: US inflation and the US short rate keep 90% and 93% of their years inside the 90% band. Where the model falls short, the bands are too narrow, and clearly so for unemployment in all three economies (58% to 63%), the euro-area short rate (66%), US house prices (63%) and the leading indicator (79%). UK inflation's band holds only 67%, the cost of its 1993 sample, though the test, with its few independent outcomes, does not call it. The rates lean low: PIT means of 0.37 to 0.43 for five of the six rates say they ended below the scenarios' middle more often than above it, as they did through the long years near zero.

The model's choices were tested on the five origins four years apart (2003, 2007, 2011, 2015 and 2019). The other eighteen are a holdout, though four of them informed a later choice, so fourteen were never used for any choice. The scores barely move between these groups, a sign that the choices were not overfitted to the origins used to make them:

| Origins | All 27 factors, 90% coverage | All 27 factors, CRPS skill | Six rates, 90% coverage | Six rates, CRPS skill |
|:--|--:|--:|--:|--:|
| The five used for choices | 0.81 | 0.31 | 0.78 | 0.29 |
| The eighteen others | 0.83 | 0.29 | 0.82 | 0.27 |
| The fourteen never used | 0.83 | 0.29 | 0.81 | 0.27 |

### Example

`out_of_sample_many` runs the same test from several origins and scores every variable across them; with origins four years apart and four-year runs, the forecasts do not overlap and every year from 2004 to 2023 is scored once. To run it for all 27 variables:

```python
evaluation = scenarios.out_of_sample_many(
    origins=["2003-12-31", "2007-12-31", "2011-12-31", "2015-12-31", "2019-12-31"],
    years=4,
    n_simulations=1000,
    seed=42,
)
evaluation.scores.select("factor", "origins", "coverage_50", "coverage_90", "pit_mean", "crps_skill")
```

A 90% band should hold 90% of the years. US and euro-area inflation hold 85% and UK inflation 60%; the US short and long rates hold 90% and the UK short rate 85%, while the euro-area rates hold 50% and 70% and ended below the middle of the scenarios in most years, with PIT means of 0.33 and 0.39. Unemployment's bands are too narrow in the US and the euro area (50%), as are US house prices' (50%); US stocks hold 85%. On CRPS every variable beats a no-change forecast except UK unemployment. Small caps, gold, European and emerging-market stocks and oil have shorter histories and enter from later origins. When plotted:

{% include ft-chart.html id="validation-coverage" src="/assets/data/financescenarios-guides/validation.json" label="Share of the years from 2004 to 2023 inside the 90% band per variable, five origins four years apart, against the 90% it should hold" %}

## Crises against the Bundled Regimes {#crises-against-the-bundled-regimes}

The baseline is a model of ordinary times, fitted on a few decades, and the fans above show the crises it does not reach in their first year. That is what the [regimes](/projects/financescenarios/docs/regimes) are for. Each chart below starts from the same past origin and the same calibration as the fan, and runs it twice: without a regime, and with the bundled regime written for that crisis. The test is whether the regime library covers the event, not whether the model foresaw it: the COVID and 2022 regimes are written from those very episodes' published paths, so reaching them shows only that they are calibrated to what happened, and, timed from the origin, they run a month or two early. The financial-crisis regime is the fairer test, since it sets no levels and only keeps the scenarios where stocks fall, unemployment rises and rates are cut together.

**2008: the financial-crisis regime does not reach it.** It moves the cloud the right way, but not far enough. US stocks fell 48.2% to their low of February 2009; by then 1 in 20 scenarios had fallen 16.4% without the regime and 26.1% with it, and the regime's lowest 5th percentile over the five years is -37.4%. US unemployment peaked at 10.0% in October 2009; by then 1 in 20 scenarios had reached 7.5% without the regime and 9.4% with it, so the peak lies just outside, and the regime's 95th percentile reaches 10.9% only later. The short rate's fall to zero is inside both, and with the regime it is the median path. The chart shows all three from the end of 2007, without and with the regime:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/validation/crisis-2008" alt="From the end of 2007, US stocks, US unemployment and the US short rate without a regime and with the Financial Crisis regime, against what happened" %}

**2020: the COVID regime reaches it.** Without a regime, 1 in 20 scenarios took US unemployment above 4.3% by April 2020; it reached 14.8%. With the regime the scenarios reach 14.8% two months early, in February, because the regime counts its months from the origin while the pandemic began in March, and they fall back as unemployment did. US stocks were down 19.5% at the end of March 2020, beyond the baseline's 5th percentile of -7.1% and inside the regime's -37.5%. The cut to zero is the regime's median path. The chart shows all three from the end of 2019, without and with the regime:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/validation/crisis-2020" alt="From the end of 2019, US unemployment, US stocks and the US short rate without a regime and with the COVID Crash and Rebound 2020 regime, against what happened" %}

**2022: both inflation regimes reach it, each from its own start.** German inflation, which the euro-area inflation of the default set follows, peaked at 8.6% at the end of 2022; from the end of 2021, 1 in 20 scenarios had reached 6.3% without a regime and 9.9% with the energy-war regime. US inflation peaked at 9.1% in June 2022; by then, 1 in 20 scenarios had reached 4.1% without the 2022 inflation regime and 9.7% with it. That regime replays the surge from January 2021, so its panel starts at the end of 2020. The UK has no regime of its own for 2022: its 9.2% at the end of 2022, far above the fan from the end of 2021, is left to a user's own regime or to the broader inflation regimes. The chart shows both inflation panels, without and with their regimes:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/validation/crisis-2022" alt="German inflation from the end of 2021 with and without the Energy War Shock 2022 regime, and US inflation from the end of 2020 with and without the 2022 Inflation and Rate Hikes regime, against what happened" %}

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">8</span></summary>

- Christoffersen, P.F. (1998). "Evaluating Interval Forecasts." International Economic Review, 39(4), 841-862. [doi.org](https://doi.org/10.2307/2527341){:target="_blank"}
- Diebold, F.X., Gunther, T.A., Tay, A.S. (1998). "Evaluating Density Forecasts with Applications to Financial Risk Management." International Economic Review, 39(4), 863-883. [doi.org](https://doi.org/10.2307/2527342){:target="_blank"}
- Eurostat. Release calendar. [ec.europa.eu](https://ec.europa.eu/eurostat/news/release-calendar){:target="_blank"}
- Ferro, C.A.T. (2014). "Fair Scores for Ensemble Forecasts." Quarterly Journal of the Royal Meteorological Society, 140(683), 1917-1923. [doi.org](https://doi.org/10.1002/qj.2270){:target="_blank"}
- Gneiting, T., Raftery, A.E. (2007). "Strictly Proper Scoring Rules, Prediction, and Estimation." Journal of the American Statistical Association, 102(477), 359-378. [doi.org](https://doi.org/10.1198/016214506000001437){:target="_blank"}
- Kupiec, P.H. (1995). "Techniques for Verifying the Accuracy of Risk Measurement Models." The Journal of Derivatives, 3(2), 73-84. [doi.org](https://doi.org/10.3905/jod.1995.407942){:target="_blank"}
- Office for National Statistics. Release calendar. [ons.gov.uk](https://www.ons.gov.uk/releasecalendar){:target="_blank"}
- U.S. Bureau of Labor Statistics. Historical release dates. [bls.gov](https://www.bls.gov/bls/histreleasedates.pdf){:target="_blank"}

</details>

{% include ft-charts-script.html %}
