---
title: Documentation
seo_title: "Documentation | Finance Scenarios"
seo_title_suffix: false
excerpt: "Finance Scenarios is an open-source economic scenario generator: thousands of joint scenarios for interest rates, inflation, equities, currencies, credit and more, linked the way they have been historically."
description: "Finance Scenarios documentation: a first run from choosing a profile to reading the distribution, what each model simulates, how the factors are linked, and real-world against risk-neutral runs."
author_profile: false
permalink: /projects/financescenarios/docs
classes: wide-sidebar
layout: single
redirect_from:
    - /projects/financescenarios/getting-started
    - /projects/financescenarios/docs/reference
    - /projects/financescenarios/docs/reference/scenarios
    - /projects/financescenarios/docs/reference/scenario-set
    - /projects/financescenarios/docs/reference/charts
    - /projects/financescenarios/docs/plotting
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Finance Scenarios is an economic scenario generator (ESG). It simulates thousands of joint scenarios for interest rates, inflation, equities, currencies, credit and other economic variables, each fitted to its own history and linked to the others the way they have moved together. A scenario set replaces a single forecast with a distribution, which is what asset-liability studies, strategic asset allocation, pension planning, reserving and Solvency II valuation need: the median path, but also the bad years and the tail.

This page runs a first set of scenarios from start to finish: choosing a run, simulating it, reading the result, checking it and keeping it. It ends with what is modeled, how the factors are linked and the two measures a run can be simulated under. Every other page explains one model or one part of a run, with its mathematics, the source of every number it uses and an example of it in a run.

To install Finance Scenarios:

```bash
pip install financescenarios -U
```

## Data and API Keys

All history comes through the [Finance Toolkit](https://github.com/JerBouma/FinanceToolkit){:target="_blank"}, and most factors calibrate on free OECD, central-bank, Ken French and Yahoo Finance data without any API key. Stock markets, government bond yields, commodities and dividends come from Financial Modeling Prep when you have a key. Its free plan allows 250 requests a day, five years of data and US-listed securities only, which is enough to try it out; longer histories and markets outside the US need a paid plan. You can get a key [through this link](/fmp){:target="_blank"}, which also gives 15% off the paid plans and supports the project. A free [FRED key](https://fred.stlouisfed.org/docs/api/api_key.html){:target="_blank"} is optional and adds US corporate bond spreads and commercial property prices.

## Choosing a Run

Every run combines two ready-made profiles: a **settings** profile, which says how the run executes (how many scenarios, how far ahead, how much history to learn from), and a **factor set**, which says what gets simulated. A **regime** can add a stress story and a **portfolio** reads the scenarios through an investment mix; both have their own page. To list the settings profiles:

```python
from financescenarios import list_presets

list_presets(kind="settings")  # or "factor-sets", "regimes", "portfolios"
```

Which returns each profile with what it is for:

| id | description |
|:---|:------------|
| ahlgrim | The run of Ahlgrim, D'Arcy and Gorvett (2005): from June 200… |
| default | 2,000 scenarios, one step a month, five years ahead, fitted … |
| dnb | Monthly steps over 100 years, DNB's horizon, with 2,000 scen… |
| goes | Default, but fitted on history since 2019 only; pair it with… |
| hibbert | The run of Hibbert, Mowbray and Turnbull (2001): from March … |
| long_horizon | Default with 500 scenarios instead of 2,000, so multi-decade… |
| wilkie | The run of Wilkie (1986): 1,000 simulations of 100 years in … |

The factor sets range from `default` (the US, the euro area and the UK, each factor fitted to its long history and linked the way the economy is) to `broad` (more countries, US sectors and styles, more commodities and currencies), with `goes` and `dnb` as the generators the NAIC and De Nederlandsche Bank prescribe, and `ahlgrim`, `hibbert` and `wilkie` as published models reproduced from their papers, each with a settings profile of the same name. The [Configuration](/projects/financescenarios/docs/configuration) page describes each.

## Simulating Scenarios

Everything starts with a `Scenarios` instance. The API keys go in here, as with the Finance Toolkit; leave them out to read them from your environment or a `.env` file. `simulate` collects the history, fits every factor, estimates how the factors move together and draws the scenarios. To simulate 2,000 scenarios of the default factor set:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(
    settings="default",
    factor_set="default",
    api_key="FINANCIAL_MODELING_PREP_KEY",
    fred_api_key="FRED_KEY",  # optional
)
result = scenarios.simulate(n_simulations=2000, seed=42)

result.describe()
```

Which returns where each of the 27 variables starts and where it ends up after five years, of which six are shown below. Rates read as yearly rates and anything with a price as its annualized return from today, written as decimals (0.0459 is 4.59%):

| factor | category | metric | initial | terminal_mean | terminal_q05 | terminal_q95 |
|:-------|:---------|:-------|--------:|--------------:|-------------:|-------------:|
| united_states_inflation | inflation | rate | 0.0374 | 0.0234 | -0.0064 | 0.0770 |
| united_states_short_rate | interest_rates | rate | 0.0408 | 0.0459 | 0.0000 | 0.1099 |
| united_states_unemployment | unemployment | rate | 0.0420 | 0.0553 | 0.0337 | 0.0894 |
| us_broad | equities | annualized |  | 0.0849 | -0.0569 | 0.2082 |
| europe | equities | annualized |  | 0.0933 | -0.0753 | 0.2487 |
| gold | commodities | annualized |  | 0.0308 | -0.0999 | 0.1716 |

US inflation starts at 3.74% and averages 2.34% after five years, the US short rate starts at 4.08% and averages 4.59%, and US stocks return 8.49% a year on average, with one scenario in twenty below -5.69% a year. When plotted, the median of three of them, with US stocks as what 100 invested today is worth, and the bands that hold the middle half and nine in ten of the scenarios, one variable per tab:

{% include ft-chart.html id="scenarios-overview" src="/assets/data/financescenarios-guides/getting-started.json" label="Median, 25-75% and 5-95% bands of the US short rate, US inflation and what 100 in US stocks is worth over five years" %}

## Reading the Distribution

`summary_statistics` gives one variable's mean, standard deviation, Monte Carlo standard error (how precisely the run pins down the mean) and percentiles at every date, and `horizon_summary` reads the same off at chosen horizons. To get both:

```python
result.summary_statistics("united_states_short_rate")

result.horizon_summary([1, 3, 5], factors=["us_broad", "united_states_inflation"])
```

The first returns a row per month; its last three rows show that the short rate's mean is known to within 0.08 percentage points (the `se` column) after five years:

| date | mean | std | se | q0.05 | q0.25 | q0.5 | q0.75 | q0.95 |
|:-----|-----:|----:|---:|------:|------:|-----:|------:|------:|
| 2030-11-01 | 0.0459 | 0.0341 | 0.0008 | 0.0000 | 0.0204 | 0.0437 | 0.0650 | 0.1095 |
| 2030-12-02 | 0.0458 | 0.0343 | 0.0008 | 0.0000 | 0.0198 | 0.0435 | 0.0651 | 0.1089 |
| 2031-01-01 | 0.0459 | 0.0345 | 0.0008 | 0.0000 | 0.0196 | 0.0439 | 0.0659 | 0.1099 |

The second returns a row per variable and horizon:

| factor | horizon | mean | std | q0.05 | q0.25 | q0.5 | q0.75 | q0.95 |
|:-------|--------:|-----:|----:|------:|------:|-----:|------:|------:|
| us_broad | 1 | 0.0917 | 0.1570 | -0.1785 | -0.0053 | 0.0968 | 0.1973 | 0.3361 |
| us_broad | 3 | 0.0859 | 0.0985 | -0.0795 | 0.0241 | 0.0914 | 0.1555 | 0.2387 |
| us_broad | 5 | 0.0849 | 0.0806 | -0.0569 | 0.0337 | 0.0873 | 0.1393 | 0.2082 |
| united_states_inflation | 1 | 0.0294 | 0.0170 | 0.0076 | 0.0193 | 0.0271 | 0.0364 | 0.0622 |
| united_states_inflation | 3 | 0.0245 | 0.0234 | -0.0037 | 0.0102 | 0.0200 | 0.0322 | 0.0740 |
| united_states_inflation | 5 | 0.0234 | 0.0254 | -0.0064 | 0.0077 | 0.0181 | 0.0312 | 0.0770 |

The range of a return read as a yearly average narrows with the horizon: the 90% range of US stocks runs from -17.85% to 33.61% over one year and from -5.69% to 20.82% a year over five. Inflation's range widens instead, from between 0.76% and 6.22% after one year to between -0.64% and 7.70% after five, as it moves away from today's reading. When plotted, the stock market rows:

{% include ft-chart.html id="scenarios-horizons" src="/assets/data/financescenarios-guides/getting-started.json" label="5th percentile, median and 95th percentile of the annualized US stock market return after one, three and five years" %}

Across all 2,000 scenarios the five-year return of US stocks has a median of 8.73% a year, and 14% of the scenarios end with a loss. When plotted, the number of scenarios per percentage point of yearly return:

{% include ft-chart.html id="scenarios-equity-distribution" src="/assets/data/financescenarios-guides/getting-started.json" label="Distribution of the five-year annualized US stock market return across 2,000 scenarios, with the 5th percentile, median and 95th percentile" %}

## Individual Scenarios

A percentile band is not a path: no single scenario follows the median. `to_dataframe` returns every scenario of a variable, one row per scenario and one column per date, ready for your own valuation or ALM model. To get the US short rate's paths:

```python
paths = result.to_dataframe("united_states_short_rate")

paths.select(paths.columns[:6]).head()
```

Which returns the first five scenarios over the first four months:

| scenario | 2026-01-01 | 2026-01-31 | 2026-03-03 | 2026-04-02 | 2026-05-03 |
|---------:|-----------:|-----------:|-----------:|-----------:|-----------:|
| 0 | 0.0408 | 0.0431 | 0.0490 | 0.0526 | 0.0491 |
| 1 | 0.0408 | 0.0441 | 0.0426 | 0.0429 | 0.0424 |
| 2 | 0.0408 | 0.0416 | 0.0446 | 0.0450 | 0.0473 |
| 3 | 0.0408 | 0.0422 | 0.0435 | 0.0435 | 0.0436 |
| 4 | 0.0408 | 0.0450 | 0.0433 | 0.0412 | 0.0437 |

When plotted, the same five scenarios over all five years:

{% include ft-chart.html id="scenarios-paths" src="/assets/data/financescenarios-guides/getting-started.json" label="The US short rate in the first five of 2,000 scenarios over five years" %}

## Checking the Run

Before relying on a run it is worth knowing how far to trust it. `validate` runs six checks on the calibration and the simulation, and `diagnose` sets each mean-reverting variable's simulated mean and spread against the ones its own model implies in the long run. To run both:

```python
scenarios.validate(result)

result.diagnose()
```

Which returns, for the checks:

| check | status | detail |
|:------|:-------|:-------|
| Every factor calibrated | pass | every factor calibrated |
| Parameters in a plausible range | pass | every long-run level and half-life in range |
| Valid correlation matrix | pass | 27 factors, smallest eigenvalue 1.14e-01, symmetric True, unit diagonal True; shrinkage 0.15; repair 0.00 |
| Simulation reproduces the correlations | warn | largest gap 0.103 (eurozone_inflation/united_kingdom_inflation); rate_level and rate_slope read off the short and long rate, not graded |
| Simulated volatility matches history | warn | 16 factors compared, median ratio 0.99; outside 0.67-1.50x: eurozone_short_rate 1.72x |
| Every path is finite | pass | 27 factors, all finite |

Four checks pass and two warn: the euro-area and UK inflation correlation comes out 0.103 away from the one it was given, and the euro-area short rate moves 1.72 times as much as in its history. `diagnose` returns a row for each of the seven variables whose model implies a long-run mean and spread; the yield curve's level and slope have none, as they are read off the short and the long rate. Two of them, US and UK unemployment, are flagged because they settle slowly, with half-lives (the time to close half the gap to the long-run level) of 2.9 and 5.1 years against a five-year run, so a gap is expected.

The [Validation](/projects/financescenarios/docs/validation) page goes much further: whether the factors move together the way the economy does, whether they stay within what history has seen, and whether a model fitted in the past would have held what happened next.

## Keeping a Run

Calibrating downloads and fits everything, which takes about two minutes; the simulation itself takes under a second. `calibrate` returns the fitted calibration, which can be saved and passed back to `simulate`, and the same seed then gives back exactly the same scenarios. `save` stores a whole run, its settings and its calibration in a folder of its own, and `read_run` reads it back without calibrating or simulating anything. To do both:

```python
from financescenarios import CalibrationResult, read_run

calibration = scenarios.calibrate()
calibration.save("calibration.json")

calibration = CalibrationResult.load("calibration.json")
result = scenarios.simulate(calibration=calibration, n_simulations=2000, seed=42)

path = scenarios.save(result, "results/")
result = read_run(path)
```

The examples throughout this documentation run on the calibration of 19 October 2026, saved this way, and reading the saved run back gives the same 2,000 scenarios of 27 variables, value for value.

## What Is Modeled

Each variable follows a model suited to how it behaves, and each model has a page of its own:

| Area | What is simulated | Default model | Page |
|:--|:--|:--|:--|
| Short rate | The 3-month rate per currency | The Federal Reserve's inertial balanced-approach rule on each scenario's inflation and unemployment, with each central bank's floor | [Short Rate](/projects/financescenarios/docs/interest-rates) |
| | Where the short rate starts from | Forward rates less the term premium, read off each government curve | [Expected Path](/projects/financescenarios/docs/interest-rates/expected-path) |
| Long rate | The 10-year rate per currency | The expected short-rate path plus a mean-reverting term premium | [Long Rate](/projects/financescenarios/docs/interest-rates/long-rate) |
| Yield curve | Level, slope and curvature of the curve, or the whole forward curve | Dynamic Nelson-Siegel through the simulated short and long rate; a two-factor Gaussian HJM | [Yield Curve](/projects/financescenarios/docs/interest-rates/yield-curve) |
| Rates and inflation together | Nominal and real rates, inflation, optionally an equity | KNW, fitted on history; DNB's CP2022, with DNB's own parameters | [KNW Models](/projects/financescenarios/docs/interest-rates/knw), [CP2022](/projects/financescenarios/docs/interest-rates/cp2022) |
| Other rate models | One rate per entry | Hull-White, Cox-Ingersoll-Ross, Wilkie's consols, Hibbert's two-factor model | [Other Rate Models](/projects/financescenarios/docs/interest-rates/other-models) |
| Inflation | Year-over-year consumer price inflation per country | Calm and high-inflation regimes, anchored to long-run expectations | [Inflation](/projects/financescenarios/docs/economy) |
| Unemployment | The unemployment rate per country | Expansions and recessions, with a recession likelier after a stock-market fall | [Unemployment](/projects/financescenarios/docs/economy/unemployment) |
| Business cycle | The OECD composite leading indicator | Mean reversion, optionally moving other factors' drift | [Business Cycle](/projects/financescenarios/docs/economy/business-cycle) |
| Longevity | One-year death probabilities by age | Cairns-Blake-Dowd | [Mortality](/projects/financescenarios/docs/economy/mortality) |
| Equities | Indices, regions, sectors and styles | Calm and turbulent regimes that switch with inflation, earning a premium over the short rate | [Equities](/projects/financescenarios/docs/markets) |
| Currencies | Each currency against the US dollar | Purchasing power parity for the euro and the pound, a random walk for the yen | [Currencies](/projects/financescenarios/docs/markets/currencies) |
| Commodities | Gold, oil and other futures | Gold a random walk in real terms, Brent mean-reverting in logs | [Commodities](/projects/financescenarios/docs/markets/commodities) |
| Real estate | House-price growth | Mean reversion, slowed by the long rate a year earlier | [Real Estate](/projects/financescenarios/docs/markets/real-estate) |
| Dividends | Dividend yield and dividend growth | A mean-reverting log yield; Wilkie's dividend growth | [Dividends](/projects/financescenarios/docs/markets/dividends) |
| Credit | Spreads, the spread curve, rating migration and default | Mean-reverting log spreads; a one-factor credit cycle | [Credit](/projects/financescenarios/docs/markets/credit) |

Interest rates, inflation, equities and unemployment are always simulated; the rest is switched on per factor set (see [Configuration](/projects/financescenarios/docs/configuration)). Each factor is simulated in its own currency and can be converted into one reporting currency afterwards. What comes after the simulation has its own pages too: stress stories in [Regimes](/projects/financescenarios/docs/regimes) and [Stress Tests](/projects/financescenarios/docs/regimes/stress-tests), investment mixes in [Portfolio](/projects/financescenarios/docs/portfolio), Solvency II in [Market Consistency](/projects/financescenarios/docs/solvency) and [Best Estimate and SCR](/projects/financescenarios/docs/solvency/capital), and the tests against history in [Validation](/projects/financescenarios/docs/validation). [Coverage](/projects/financescenarios/docs/coverage) lists every model, measure and known gap.

## How the Factors Are Linked

When equities fall, spreads, rates and currencies should move the way they did in past sell-offs. Where theory says one variable drives another (inflation and unemployment setting the policy rate, a stock-market fall making a recession likelier), the driver's simulated path feeds the next factor; everything else is tied together by one correlation matrix of the historical shocks. Each arrow in the diagram is a direct link in the model's equations:

<div class="fs-diagram">
<div class="fs-links">
  <div class="fs-links__row">
    <div class="fs-node is-accent"><b>Inflation</b><small>top of the cascade</small></div>
    <div class="fs-links__to">
      <div class="fs-link"><em>policy rule</em><div class="fs-node"><b>Short rates</b></div></div>
      <div class="fs-link"><em>Phillips curve</em><div class="fs-node"><b>Unemployment</b></div></div>
      <div class="fs-link"><em>turbulence odds</em><div class="fs-node"><b>Equities</b></div></div>
      <div class="fs-link"><em>purchasing power parity</em><div class="fs-node"><b>Euro and pound</b></div></div>
      <div class="fs-link"><em>real terms</em><div class="fs-node"><b>Gold</b></div></div>
    </div>
  </div>
  <div class="fs-links__row">
    <div class="fs-node"><b>Unemployment</b></div>
    <div class="fs-links__to">
      <div class="fs-link"><em>policy rule</em><div class="fs-node"><b>Short rates</b></div></div>
    </div>
  </div>
  <div class="fs-links__row">
    <div class="fs-node"><b>Short rates</b></div>
    <div class="fs-links__to">
      <div class="fs-link"><em>expected path</em><div class="fs-node"><b>Long rates</b><small>plus a term premium</small></div></div>
      <div class="fs-link"><em>short end</em><div class="fs-node"><b>Yield curve</b></div></div>
      <div class="fs-link"><em>rate plus premium</em><div class="fs-node"><b>Equities</b></div></div>
    </div>
  </div>
  <div class="fs-links__row">
    <div class="fs-node"><b>Equities</b></div>
    <div class="fs-links__to">
      <div class="fs-link"><em>recession odds</em><div class="fs-node"><b>US unemployment</b></div></div>
    </div>
  </div>
  <div class="fs-links__row">
    <div class="fs-node"><b>Long rates</b></div>
    <div class="fs-links__to">
      <div class="fs-link"><em>long end</em><div class="fs-node"><b>Yield curve</b></div></div>
      <div class="fs-link"><em>a year later</em><div class="fs-node"><b>House prices</b></div></div>
    </div>
  </div>
  <div class="fs-links__row">
    <div class="fs-node"><b>Leading indicator</b><small>business cycle, opt-in</small></div>
    <div class="fs-links__to">
      <div class="fs-link is-dashed"><em>drift</em><div class="fs-node"><b>Inflation, rates, spreads</b></div></div>
      <div class="fs-link is-dashed"><em>crisis odds</em><div class="fs-node"><b>Equities</b></div></div>
    </div>
  </div>
</div>
<p class="fs-diagram__note">Dashed: only with business-cycle conditioning. Wilkie's and the KNW models' links from inflation, and interest-rate parity for exchange rates, are further options.</p>
</div>

Factors with no theoretical driver, such as oil, mortality and the yield curve's curvature, are linked only through the correlation matrix; the curve's level and slope are read off the simulated short and long rate. [How a Run Is Built](/projects/financescenarios/docs/architecture#dependence) explains both mechanisms, and [Dependence](/projects/financescenarios/docs/dependence) how the correlations are estimated.

## Real-World and Risk-Neutral Runs

Every run is simulated under one of two probability measures, each answering its own question:

<div class="ca-cards">
  <div><i class="ca-icon fas fa-globe" aria-hidden="true"></i><p class="ca-card-title">Real-world: what could happen?</p><p>Keeps each factor's historical drift and risk premia. For ALM studies, asset allocation and capital.</p></div>
  <div><i class="ca-icon fas fa-scale-balanced" aria-hidden="true"></i><p class="ca-card-title">Risk-neutral: what is this worth?</p><p>Grows every asset at the risk-free rate, so it reproduces today's prices. For guarantees and the Solvency II best estimate.</p></div>
</div>

[Configuration](/projects/financescenarios/docs/configuration#real-world-and-risk-neutral-measures) explains the difference and which factors have a risk-neutral form. Both come from the same configuration:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(settings="default", factor_set="default")

real_world = scenarios.simulate()                         # ALM, allocation, risk
risk_neutral = scenarios.simulate(measure="risk_neutral")  # valuation, best estimate
real_world.describe()                                     # every factor at a glance
```

{% include ft-charts-script.html %}
