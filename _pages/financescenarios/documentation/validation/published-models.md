---
title: Published Models
seo_title: "Published Models | Finance Scenarios"
seo_title_suffix: false
excerpt: "The published models in Finance Scenarios: Ahlgrim, D'Arcy and Gorvett, Hibbert, Mowbray and Turnbull, and Wilkie, run with their papers' own parameters, checked against their papers' tables and scored against what happened since."
description: "Published models in Finance Scenarios: the ahlgrim, hibbert and wilkie factor sets, how they reproduce their papers' tables within Monte Carlo error, and how their forecasts held up against the history since they were written."
author_profile: false
permalink: /projects/financescenarios/docs/validation/published-models
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/validation
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-validation"
---

A published scenario generator can be checked twice: against the tables its own paper reports, and against what happened in the years since it was written. Three published models ship as factor sets, and this page does both for each.

## The Published Sets {#published-frameworks}

Economic scenario generators differ mostly in how they link the variables. Each of the three sets reproduces its paper's model and has a settings profile of the same name for the paper's own start date, number of scenarios and horizon:

| Factor set | Framework | How the variables are linked |
|:-----------|:----------|:-----------------------------|
| `ahlgrim` | [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"} | Each variable is its own process; inflation feeds the nominal rate (the real rate plus inflation) and unemployment, and the paper's correlations tie the shocks together. |
| `hibbert` | [Hibbert, Mowbray and Turnbull (2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"} | Rates and inflation revert to a slowly moving target; equities earn a premium over cash and switch between two regimes. Calibration A. |
| `wilkie` | [Wilkie (1986)](https://doi.org/10.1017/S0071368600009009){:target="_blank"} | A cascade: inflation first, then dividend yields, dividend growth, the Consols yield and share prices, each driven by it, on four independent white-noise series. |

Each set states every parameter of its paper as a belief, with its section or table, and never refits it. The correlations are the paper's own, with any pair it does not list set to zero (`unlisted: zero`). So are the starting values: Ahlgrim's workbook base case of June 2004, Hibbert's calibration A start of March 2001 and Wilkie's neutral start. With `published_model` the calibration is built from these alone, so the sets read no data, need no API key and run the same offline. To run one as the paper ran it:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(settings="wilkie", factor_set="wilkie")
result = scenarios.simulate()   # 1,000 scenarios of 100 years in yearly steps, as in the paper
```

`compare_published` holds a set to the tables its paper reports for its own model, and `held_up` scores it against the history since; both are covered below. The equations of the rate models they use are on [Other Rate Models](/projects/financescenarios/docs/interest-rates/other-models) and Wilkie's dividends on [Dividends](/projects/financescenarios/docs/markets/dividends).

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">Reproduction, not projection</p>

These sets answer "what does the paper's model say?", from the paper's own starting point. To use a method on today's data, write a factor set with the same options (`method: wilkie_consols`, `hibbert_two_factor`, `real_rate` and so on), leave out `published_model` and keep only the beliefs you want fixed; the rest is fitted. Each set's description says so.
</div>

Two published models of rates and inflation together have pages of their own: DNB's [CP2022](/projects/financescenarios/docs/interest-rates/cp2022), which the `dnb` factor set runs with DNB's quarterly parameters, and the [KNW models](/projects/financescenarios/docs/interest-rates/knw) after Koijen, Nijman and Werker (2010), fitted on history.

## Reproducing the Papers {#published-parameter-mode}

Because the sets use their papers' own parameters, correlations and starting values and read no data, they can be checked: run as the paper ran, from its start date and over its horizon, each should reproduce the tables its paper reports for its own model. `compare_published` runs the check:

```python
from financescenarios.validation.published_frameworks.published_frameworks_controller import compare_published

compare_published("wilkie")
```

Which returns every reported mean, standard deviation, percentile and correlation next to the simulated one (the first 3 of 91 rows; GQ is Wilkie's average yearly price inflation over the horizon):

| source | variable | statistic | horizon | published | simulated | tolerance | within |
|:-------|:---------|:----------|--------:|----------:|----------:|----------:|:-------|
| Table 3 | GQ | mean | 1.0 | 0.0537 | 0.0538 | 0.0076 | true |
| Table 3 | GQ | mean | 5.0 | 0.0537 | 0.0531 | 0.0055 | true |
| Table 3 | GQ | mean | 10.0 | 0.0514 | 0.0526 | 0.0043 | true |

A difference counts as Monte Carlo error when it is within four standard errors of the gap between the paper's estimate and the run's, plus half the paper's last printed digit. The standard error comes from batch means (the spread of the statistic across equal groups of scenarios), scaled to the paper's number of scenarios. Four standard errors keeps the chance of a false alarm across a table of a few dozen checks near 1%. With 10,000 scenarios:

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
- **Hibbert:** calibration A only. Calibration B adds risk premia that exist to price bonds, which the package does not do, so B, with its floors and yield-curve reflection, is left out, as are the bond rows of Exhibit 7.2A.
- **Wilkie:** the set runs his yearly step. On a monthly step four cells at one and five years fall outside Monte Carlo error (the Consols-inflation correlation at one year is -0.22 against -0.42), because a monthly run's inflation is a year-on-year rate read every month.
- **Data:** Wilkie's UK series (1919-1982), the NCREIF commercial property index and Hibbert's UK calibration data are not available here, so the parameters are used as published and nothing is refitted. Hibbert's and Wilkie's models have no unemployment, so their sets simulate none.
</div>

## How They Held Up {#published-models-held-up}

Because each published set starts from its paper's own date, each is a forecast made years ago that can be checked against what happened since. `held_up` runs a set from its paper's start and places every year since in its fan:

- Ahlgrim, D'Arcy and Gorvett from June 2004, on US data;
- Hibbert, Mowbray and Turnbull from end-March 2001, on UK data;
- Wilkie from his neutral start, dated 1986, on UK data.

All of the history is the OECD's and needs no key: the short and long rates, year-on-year CPI inflation, unemployment, share prices and US house prices. To score the Wilkie set:

```python
from financescenarios.validation.published_frameworks.published_frameworks_controller import held_up

rows, scores = held_up("wilkie")  # the fan and the realized value per year, and the scores per factor
```

Run for all three sets, the scores per factor:

| Model | Factor | Years | Inside 50% band | Inside 90% band | Mean PIT | CRPS skill vs no change |
|:--|:--|--:|--:|--:|--:|--:|
| Ahlgrim (US, 2004) | Short rate | 22 | 36% | 100% | 0.24 | -0.67 |
| | Inflation | 22 | 59% | 100% | 0.36 | -0.02 |
| | Unemployment | 22 | 14% | 45% | 0.37 | +0.19 |
| | Share prices (growth since start) | 22 | 23% | 100% | 0.26 | -1.19 |
| | Real estate (vs house prices) | 22 | 36% | 82% | 0.27 | +0.29 |
| Hibbert (UK, 2001) | Short rate | 24 | 33% | 100% | 0.24 | +0.40 |
| | Inflation | 25 | 72% | 96% | 0.46 | +0.41 |
| | Share prices (growth since start) | 25 | 44% | 96% | 0.23 | -1.62 |
| Wilkie (UK, 1986) | Inflation | 40 | 93% | 100% | 0.37 | +0.33 |
| | Long yield (vs the 10-year gilt) | 40 | 13% | 28% | 0.19 | +0.48 |
| | Share prices (growth since start) | 40 | 70% | 100% | 0.64 | +0.66 |

A calibrated fan holds about half the years in its 50% band and nine in ten in its 90% band, with a mean PIT (the share of scenarios below the outcome) near 0.5. A skill above zero means the fan's CRPS beat a forecast that the value stays where it started (zero growth for share prices). When plotted, Ahlgrim's model against what happened in the US, one factor per tab:

{% include ft-chart.html id="validation-held-up-ahlgrim" src="/assets/data/financescenarios-guides/validation-held-up.json" label="5th percentile, median and 95th percentile of Ahlgrim, D'Arcy and Gorvett's model from June 2004 and what happened in the US, year by year" %}

**Rates.** None of the three models allowed for a decade of rates near zero. Ahlgrim's median US short rate rises toward 7.6% (a 2.8% real rate plus 4.8% inflation). Hibbert's UK median holds at 5% for 30 years. The realized rates sat near zero from 2009 to 2021, in the lower tail of both fans, though still inside their 90% bands; that gives mean PITs of 0.24. Wilkie's long yield fared worst. His model reverts the real yield to 3.5% on top of about 5% expected inflation, so its median stays near 8.5%. The 10-year gilt fell from about 10% in 1986 to below his 5th percentile in 27 of the 40 years, from 1999 on, and was 4.4% in 2026 against a median of 8.7%. Wilkie's CRPS still beats "no change" only because no change means staying at 1986's 10%. When plotted, Wilkie's model against what happened in the UK:

{% include ft-chart.html id="validation-held-up-wilkie" src="/assets/data/financescenarios-guides/validation-held-up.json" label="5th percentile, median and 95th percentile of Wilkie's model from his neutral start, dated 1986, and what happened in the UK, year by year" %}

**Inflation.** The fans held inflation well. Wilkie's 5% mean with wide bands kept 93% of UK years inside its 50% band; that is too many, which means the bands were wider than needed. Hibbert's 2.5% target matched the Bank of England's era (72% inside the 50% band); only 2023's 10% spike went above the 95th percentile. Ahlgrim's 4.8% mean sits above the 2.5% the US averaged, so realized years fell below the median (mean PIT 0.36).

**Unemployment.** Ahlgrim's band was far too narrow: about 4.3% to 8.0% at every horizon. That band comes from the workbook's monthly unemployment step, which Table 1 shows. US unemployment went above the 95th percentile in 2009 to 2012 and in 2020, and below the 5th in 2018, 2019 and every year from 2022 to 2026. Only 45% of years fell inside the 90% band.

**Share prices.** The fans are wide, so the 90% bands held almost every year. The medians are another matter. Ahlgrim's and Hibbert's equity premia, taken from long histories, put their medians well above what the OECD's US and UK share price indices did; the UK index was up 79% in 25 years against Hibbert's median of 194%. Their CRPS skill is negative. Wilkie's median for UK share prices sits close to the realized growth (626% against 634% by 2026). When plotted, Hibbert's model against what happened in the UK:

{% include ft-chart.html id="validation-held-up-hibbert" src="/assets/data/financescenarios-guides/validation-held-up.json" label="5th percentile, median and 95th percentile of Hibbert, Mowbray and Turnbull's model from March 2001 and what happened in the UK, year by year" %}

**Real estate.** Ahlgrim models NCREIF's commercial property returns; the nearest history that needs no key is US house prices. The 2008 to 2011 fall went below the 5th percentile in all four years.

These numbers score a single path of history year by year. The years overlap in what they test, so the shares describe what happened rather than test calibration. The comparisons also use OECD stand-ins for the papers' own series: a 3-month rate for a 1-month one, a 10-year gilt for Consols, share price indices for total-return indices, and house prices for NCREIF. Wilkie's run starts from his neutral values (5% inflation, an 8.5% long yield), not from 1986's actual market.

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">3</span></summary>

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. [casact.org](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}
- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert Limited. [ressources-actuarielles.net](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"}
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. [doi.org](https://doi.org/10.1017/S0071368600009009){:target="_blank"}

</details>

{% include ft-charts-script.html %}
