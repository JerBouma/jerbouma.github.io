---
permalink: /projects/financescenarios
software:
  name: "Finance Scenarios"
  repository: "https://github.com/JerBouma/FinanceScenarios"
  download: "https://pypi.org/project/financescenarios/"
title: Finance Scenarios
excerpt: An open-source economic scenario generator in Python. It simulates thousands of possible scenarios for interest rates, inflation, equities, currencies and more, calibrated on live data from the Finance Toolkit, with portfolio analysis and Solvency II on top.
description: "Finance Scenarios is an open-source Python economic scenario generator: simulate correlated rates, inflation, equities and more, then put portfolios and liabilities through them."
classes: wide-sidebar ft-overview
author_profile: false
sidebar:
  nav: "financescenarios"
image: assets/images/projects/financescenarios/banner.png
sitemap: false
noindex: true
search: false
---

<div class="page-header-action notebook-viewer-actions"><a href="https://github.com/JerBouma/FinanceScenarios" target="_blank" rel="noopener"><i class="fab fa-github"></i> View on GitHub</a></div>

Whether you are saving for retirement or running the balance sheet of an insurer, the question about the future is rarely "what will happen?". It is "what could happen, and how bad does it get?". Will my savings last thirty years of withdrawals? How much capital does a 1-in-200-year market shock eat? A single forecast cannot answer either, because the answer lives in the spread of outcomes, not in the middle of it. The tools that do answer it, economic scenario generators, have mostly been vendor products from Moody's, Conning, Ortec Finance and Barrie & Hibbert: you receive a set of scenario files and a calibration report while the method itself stays with the vendor.

**Finance Scenarios tries to solve that.** It simulates thousands of possible scenarios for interest rates, inflation, equities, unemployment and more, all linked to each other the way they have been historically, and calibrated on live data pulled through the [Finance Toolkit 🛠️](https://github.com/JerBouma/FinanceToolkit). Put your portfolio or your liabilities through those scenarios and you see the full range: the typical outcome, the bad year in twenty, and the 1-in-200 event a regulator asks about.

The goal is not to compete with a vendor model but to make the published methods accessible and reproducible in the open. Every calibration method is written out in plain Python and linked to the paper it came from, from [Wilkie (1986)](https://doi.org/10.1017/S0071368600009009) and [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf) to [Hibbert, Mowbray and Turnbull (2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf), [Cairns, Blake and Dowd (2006)](https://www.macs.hw.ac.uk/~andrewc/papers/jri2006e.pdf) and [Koijen, Nijman and Werker (2010)](https://doi.org/10.1093/rfs/hhp058), with a documentation page per factor and per model. The assumptions, parameters, beliefs and correlations all live in files you can edit, so you can change one and run it again to see what it does. The results still depend on the assumptions you chose, on the data available, and on your own judgement.

<img src="/assets/images/projects/financescenarios/banner.webp" alt="Finance Scenarios" width="100%"/>

## Installation

Finance Scenarios requires Python 3.11 or higher and installs with a single command:

```bash
pip install financescenarios -U
```

The scenarios are fitted to market history, so to get the most out of it you need an API key from FinancialModelingPrep. It supplies the price histories the model learns from: stock markets, government bond yields, commodities and dividends. The Free plan allows 250 requests a day, five years of data and US-listed securities only, which is enough to try it out; longer histories and markets outside the US need a premium plan.

[Obtain an API Key from FinancialModelingPrep](/fmp){: .btn .btn--warning .btn--large .align-center target="_blank"}

The link gives access to the free plan and to premium plans at a **15% discount**. It is an affiliate link, so it supports the project at the same time.

A free [FRED key](https://fred.stlouisfed.org/docs/api/api_key.html) from the Federal Reserve Bank of St. Louis is optional and adds US corporate bond spreads and commercial property prices. The [configuration documentation](/projects/financescenarios/docs/configuration#secrets) shows which data each part of the model relies on.

## Functionality

This section is an introduction to Finance Scenarios, run on the default settings and the default factor set (the US, the euro area and the UK) with 2,000 scenarios. Every table is the actual output of the snippet above it, cut down to a few rows, and every chart is interactive and drawn from that same run, calibrated on {{ site.data.financescenarios_run.date }}; live data moves, so another day gives slightly different numbers. Every class also documents itself through Python's built-in help, and the [documentation](/projects/financescenarios/docs) explains each model and its assumptions.

Every run combines two ready-made *profiles*: a **settings** profile, which says how the run goes (how many scenarios, how far ahead, how much history to learn from), and a **factor set**, which says what gets simulated (which interest rates, stock markets, currencies and so on). Optionally a **regime** adds a stress story, and a **portfolio** is an investment mix to read the scenarios through. Every one of them can be listed with what it is for, all at once or one kind at a time:

```python
from financescenarios import list_presets

list_presets(kind="settings")  # or "factor-sets", "regimes", "portfolios"; leave it out for all 39
```

Each kind's output is below; open one to see its options.

<details class="ft-details" markdown="1">
<summary><i class="fas fa-sliders-h"></i> <b>Settings profiles</b> <span class="ft-details__meta">4</span></summary>

| id           | description                                                                                                              |
|:-------------|:-------------------------------------------------------------------------------------------------------------------------|
| default      | 2,000 scenarios, one step a month, five years ahead, fitted on history since 2000.                                       |
| goes         | Default, but fitted on history since 2019 only; pair it with the goes factor set to match the NAIC's scenario generator. |
| long_horizon | Default with 500 scenarios instead of 2,000, so multi-decade runs stay fast; pick the length with simulate(years=30).    |
| wilkie       | Default, fitted on 1995 to 2007 only, as the wilkie set needs.                                                           |

</details>

<details class="ft-details" markdown="1">
<summary><i class="fas fa-layer-group"></i> <b>Factor sets</b> <span class="ft-details__meta">9</span></summary>

| id              | description                                                                                                                                           |
|:----------------|:------------------------------------------------------------------------------------------------------------------------------------------------------|
| ahlgrim         | The six factors of Ahlgrim, D'Arcy and Gorvett (2005): short rate, inflation, equities, unemployment, real estate and dividend yield.                 |
| broad           | Everything this project can simulate, across many countries: the widest set, and the slowest to fit.                                                  |
| core            | The US, the euro area and the UK, with global equities, gold, oil and the major currencies; a curated set that passes every release check.            |
| default         | Core, with interest rates anchored to EIOPA's official forward rates and their swings fitted on rates since 1950; the recommended starting point.     |
| goes            | US Only, with the short rate's long-run level set to the NAIC scenario generator's own (about 3.73%); pair it with the goes settings.                 |
| hibbert         | The two-factor model of Hibbert, Mowbray and Turnbull (2001): short rate and inflation that chase moving targets, regime-switching equities.          |
| private_markets | US Only plus listed stand-ins for private equity, infrastructure, hedge funds and private credit.                                                     |
| us_only         | The United States only: its rates, inflation, unemployment and stock market, plus currencies, commodities and the other shared factors; quick to run. |
| wilkie          | The original Wilkie (1986) actuarial model: inflation, dividends, a consols rate and share prices; pair it with the wilkie settings.                  |

</details>

<details class="ft-details" markdown="1">
<summary><i class="fas fa-bolt"></i> <b>Stress regimes</b> <span class="ft-details__meta">12</span></summary>

| id                    | description                                                                                                                                             |
|:----------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------|
| climate_collapse      | Rough stand-in for a climate shock: keeps the scenarios with the highest US inflation and the weakest US stocks.                                        |
| commodity_supercycle  | A long oil boom: keeps the scenarios where crude oil earns a top-quarter return.                                                                        |
| credit_crunch         | Bank stocks collapse and the market follows: a harsher bear market for financials, then their worst scenarios. Needs the financials equity (broad set). |
| currency_crisis       | The Brazilian real devalues sharply against the dollar, about 22% a year, then keeps its worst scenarios. Needs the us_only or broad set.               |
| financial_crisis      | Stocks fall, unemployment rises and rates are cut, all at once: keeps the scenarios where that happens together.                                        |
| oil_crisis            | Pulls inflation towards 12% in year one and back to 2.5% by year 8, then keeps the scenarios with high rates and weak stocks.                           |
| oil_shock             | A one-off three-point jump in US inflation in year 2, after which everything behaves normally again.                                                    |
| rate_cut_cycle        | Inflation eases to 2% by year 5 and 2.5% by year 10, then drifts back to its usual level.                                                               |
| real_estate_crash     | House-price growth falls to -8% within a year and recovers over four, then keeps the worst housing scenarios.                                           |
| soft_landing          | Inflation eases smoothly to 2% by year 5 and stays there; no scenarios are filtered out.                                                                |
| tech_selloff          | Tech stocks fall while the wider market holds up; keeps the worst tech scenarios. Needs the broad set.                                                  |
| yield_curve_inversion | Short rates rise two points above long ones within six months, then the curve slowly rights itself.                                                     |

</details>

<details class="ft-details" markdown="1">
<summary><i class="fas fa-chart-pie"></i> <b>Portfolios</b> <span class="ft-details__meta">14</span></summary>

| id                    | description                                                                                                                                   |
|:----------------------|:----------------------------------------------------------------------------------------------------------------------------------------------|
| all_weather           | Ray Dalio's mix: 30% US stocks, 55% Treasuries for his 40% long and 15% intermediate bonds, 15% gold for his 7.5% gold and 7.5% commodities.  |
| balanced_60_40        | The textbook mix: 60% US stocks and 40% US Treasury bonds.                                                                                    |
| barbell               | Nassim Taleb's barbell: 85% Treasury bills, 15% small-cap and growth stocks, nothing in between. Needs the broad set.                         |
| bogleheads_three_fund | The Bogleheads' three funds: 40% US stocks, 20% international stocks and 40% US Treasury bonds. Needs the default, core or broad set.         |
| buffett_90_10         | Warren Buffett's advice for his estate: 90% in an S&P 500 fund and 10% in Treasury bills.                                                     |
| conservative_income   | Mostly US, euro-area and UK government bonds, with 10% in US stocks for growth. Needs the default, core or broad set.                         |
| endowment_model       | A university-endowment mix with 40% in listed stand-ins for private markets. Needs the private_markets set.                                   |
| global_60_40          | The 60/40 spread across countries: US, European and emerging-market stocks; US, euro-area and UK bonds. Needs the default, core or broad set. |
| global_equity_growth  | All stocks, spread across the US, Europe, Japan, emerging markets and China, tilted to growth. Needs the broad set.                           |
| golden_butterfly      | Equal fifths of stocks, small-cap and value stocks, long bonds, Treasury bills and gold. Needs the broad set.                                 |
| permanent_portfolio   | Harry Browne's four quarters: US stocks, long US Treasuries, Treasury bills and gold.                                                         |
| small_cap_value_tilt  | 80% in small-cap and value stocks, the Fama-French premia, with 20% US Treasury bonds. Needs the broad set.                                   |
| target_date_glidepath | A target-date fund on Vanguard's glide path: 90% stocks until 25 years out, 50% at the target date and 30% seven years after.                 |
| us_equity_sectors     | All stocks, split evenly across nine US sectors. Needs the broad set.                                                                         |

</details>

The examples below use the default settings and the default factor set.

### Simulating Scenarios {#simulating-scenarios}

Fit every variable to its history and draw 2,000 scenarios at once. The API keys go in here, as with the Finance Toolkit; leave them out to read them from your environment or a .env file.

```python
from financescenarios import Scenarios

# The default settings and the default factor set: the US, the euro area and the UK
scenarios = Scenarios.from_profiles(
    settings="default",
    factor_set="default",
    api_key="FINANCIAL_MODELING_PREP_KEY",  # replace with your actual API key
    fred_api_key="FRED_KEY",  # optional, replace with your actual FRED key or leave it out
)
result = scenarios.simulate(n_simulations=2000, seed=42)

# Where every variable starts and where it ends up after five years
result.describe()
```

For example, 6 of the 27 variables are shown below. Rates are yearly rates and anything with a price a yearly return, written as decimals (0.0442 is 4.42%).

| factor                     | category       | initial | terminal_mean | terminal_q05 | terminal_q95 |
|:---------------------------|:---------------|--------:|--------------:|-------------:|-------------:|
| united_states_inflation    | inflation      |  0.0340 |        0.0262 |      -0.0033 |       0.0549 |
| united_states_short_rate   | interest_rates |  0.0406 |        0.0442 |       0.0049 |       0.0859 |
| united_states_unemployment | unemployment   |  0.0410 |        0.0557 |       0.0210 |       0.0904 |
| us_broad                   | equities       |         |        0.0983 |      -0.0465 |       0.2318 |
| europe                     | equities       |         |        0.0765 |      -0.0927 |       0.2197 |
| gold                       | commodities    |         |        0.0594 |      -0.0614 |       0.1926 |

The chart below follows the US short rate, US inflation and US equities through all 2,000 scenarios. **Find [the Notebook](/projects/financescenarios/getting-started) and [the simulation documentation](/projects/financescenarios/docs/simulation-engine).**

```python
result.plot(["united_states_short_rate", "united_states_inflation", "us_broad"])
```

Which draws the median of each variable with the bands that hold half and nine in ten of the scenarios:

{% include ft-chart.html id="simulation" src="/assets/data/financescenarios-charts.json" label="Simulated short rate, inflation and US equities" %}

### Reading the Distribution

Follow any variable date by date as percentile bands, or read it off at chosen horizons.

```python
result.summary_statistics("united_states_short_rate")
```

For example, the last three months of the US short rate are shown below.

| date       |   mean |    std |  q0.05 |  q0.25 |   q0.5 |  q0.75 |  q0.95 |
|:-----------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| 2030-11-01 | 0.0442 | 0.0244 | 0.0048 | 0.0277 | 0.0447 | 0.0600 | 0.0857 |
| 2030-12-02 | 0.0441 | 0.0245 | 0.0043 | 0.0276 | 0.0439 | 0.0607 | 0.0856 |
| 2031-01-01 | 0.0442 | 0.0245 | 0.0049 | 0.0276 | 0.0442 | 0.0604 | 0.0859 |

The chart below shows how widely the five-year US equity return spreads across the scenarios. **Find [the documentation](/projects/financescenarios/docs/units).**

```python
result.plot("us_broad", kind="distribution")
```

Which shows where the five-year return lands across all 2,000 scenarios:

{% include ft-chart.html id="distribution" src="/assets/data/financescenarios-charts.json" label="Distribution of the five-year US equity return" %}

### Building a Portfolio

Put an investment mix through the same scenarios, here the 60/40 (60% US stocks, 40% US government bonds) from the 14 ready-made mixes, rebalanced once a year.

```python
from financescenarios import Portfolio

# 60% broad US equities, 40% US government bonds, rebalanced once a year
portfolio = Portfolio.from_preset(result, preset="balanced_60_40")
values = portfolio.compute(initial_value=100_000, rebalance_every=12)

values.describe()
```

This returns the portfolio's yearly return over the five years, and what each holding earned on its own:

| factor                        | category  | initial | terminal_mean | terminal_q05 | terminal_q95 |
|:------------------------------|:----------|--------:|--------------:|-------------:|-------------:|
| portfolio                     | portfolio |         |        0.0835 |      -0.0004 |       0.1609 |
| us_broad_value                | holding   |         |        0.0983 |      -0.0465 |       0.2318 |
| united_states_long_rate_value | holding   |         |        0.0539 |       0.0328 |       0.0748 |

The 60/40 earns 8.35% a year on average, between the stocks' 9.83% and the Treasury fund's 5.39%, so 100,000 grows to 152,361. The same portfolio also reports its drawdowns and Value at Risk, and covers saving and withdrawal plans, glidepaths and fees. The chart below shows the portfolio's value in money across the scenarios. **Find [the Notebook](/projects/financescenarios/portfolio-notebook).**

```python
values.plot(levels=True)
```

Which shows the portfolio's value in money, with the same bands:

{% include ft-chart.html id="portfolio" src="/assets/data/financescenarios-charts.json" label="Simulated value of a 60/40 portfolio" %}

### Applying Stress Regimes

Run the same variables through one of 12 named stress stories, such as an oil crisis. A regime changes an assumption before simulating, keeps only the scenarios that fit the story, or both.

```python
from financescenarios import compare_runs

shocked = scenarios.simulate(regime="oil_crisis", n_simulations=2000, seed=42)

compare_runs({"baseline": result, "oil_crisis": shocked})
```

Oil Crisis pulls US inflation towards 12% and keeps the scenarios with high interest rates and weak stocks; it draws as many scenarios as it takes for 2,000 to fit the story. For example, four of the variables are shown below.

| factor                   | baseline | oil_crisis |
|:-------------------------|---------:|-----------:|
| united_states_inflation  |   0.0262 |     0.0492 |
| united_states_short_rate |   0.0442 |     0.0649 |
| us_broad                 |   0.0983 |     0.0158 |
| europe                   |   0.0765 |     0.0177 |

The chart below sets US inflation in the baseline next to the Oil Shock, Oil Crisis and Climate Collapse regimes, 2,000 scenarios each. **Find [the Notebook](/projects/financescenarios/regimes-notebook) and [the regime documentation](/projects/financescenarios/docs/regimes).**

```python
from financescenarios import plot_runs

runs = {"baseline": result}
for regime in ("oil_shock", "oil_crisis", "climate_collapse"):
    runs[regime] = scenarios.simulate(regime=regime, n_simulations=2000, seed=42)

plot_runs(runs, "united_states_inflation")
```

Which puts the four runs side by side:

{% include ft-chart.html id="regimes" src="/assets/data/financescenarios-charts.json" label="US inflation in the baseline and under three stress regimes" %}

### Backtesting Against History

Run ready-made mixes against what prices actually did, on one shared calendar, and measure what each is exposed to with the [Fama-French factors](https://doi.org/10.1016/j.jfineco.2014.10.010) from [Ken French's data library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html).

```python
# What each mix's holdings actually did, month by month, as one "scenario" per mix
portfolio = Portfolio.backtest(scenarios, ["balanced_60_40", "all_weather", "permanent_portfolio"])

portfolio.factor_exposure()
```

Which gives each mix's loading on each factor and how much they explain:

| portfolio           | Mkt-RF |     SMB |     HML |    RMW |     CMA |  alpha | r_squared | observations | from       | to         |
|:--------------------|-------:|--------:|--------:|-------:|--------:|-------:|----------:|-------------:|:-----------|:-----------|
| 60/40 Balanced      | 0.5369 | -0.0687 | -0.0450 | 0.1216 | -0.0113 | 0.0007 |    0.8615 |          312 | 2000-08-01 | 2026-10-01 |
| All Weather         | 0.2043 | -0.0621 | -0.1445 | 0.2166 |  0.0344 | 0.0029 |    0.1324 |          312 | 2000-08-01 | 2026-10-01 |
| Permanent Portfolio | 0.2175 | -0.0615 | -0.1424 | 0.2019 |  0.0478 | 0.0033 |    0.1244 |          312 | 2000-08-01 | 2026-10-01 |

The chart below shows what each mix actually did since August 2000, rebalanced once a year: 100,000 grew to 550,744 in the 60/40, 541,653 in All Weather and 555,908 in the Permanent Portfolio by October 2026, with the 60/40 carrying more than twice the stock market risk of the other two. **Find [the Notebook](/projects/financescenarios/portfolio-analysis-notebook).**

```python
portfolio.compute(initial_value=100_000, rebalance_every=12).plot(levels=True)
```

Which follows each mix month by month:

{% include ft-chart.html id="backtest" src="/assets/data/financescenarios-charts.json" label="Historical value of the 60/40, All Weather and Permanent Portfolio mixes since 2000" %}

### Valuing Liabilities and Capital Under Solvency II

Value what an insurer owes from a run priced like today's market (risk-neutral) and its one-year 99.5% capital requirement (the SCR) from the real-world run, as [Solvency II](https://eur-lex.europa.eu/eli/dir/2009/138/oj) asks.

```python
from financescenarios import Solvency

# The same factors priced the way markets price them today, for valuing what is owed
risk_neutral = scenarios.simulate(n_simulations=2000, seed=42, measure="risk_neutral")
solvency = Solvency(real_world=result, risk_neutral=risk_neutral)

# Pay out 10,000 a year for five years, backed by 60,000 invested in the 60/40
assets = Portfolio.from_preset(result, preset="balanced_60_40").compute(initial_value=60_000, rebalance_every=12)
solvency.report(cashflows=[10_000] * 5, assets=assets)
```

Which gives every number in one table:

| item                | value                     | meaning                                                    |
|:--------------------|:--------------------------|:-----------------------------------------------------------|
| market consistent   | passed (largest gap 0.1%) | discounted back, us_broad stays within 2% of today's price |
| best estimate       | 43,514                    | what the payments are worth today                          |
| own funds           | 15,661                    | assets minus what is owed, today                           |
| SCR (1 in 200 year) | 12,487                    | the capital that survives a 1-in-200 bad year              |
| solvency ratio      | 1.25                      | own funds / SCR; above 1 means enough capital              |

The chart below shows where own funds could be after one year, with today's level and the 1-in-200 outcome marked. **Find [the documentation](/projects/financescenarios/docs).**

```python
solvency.plot(cashflows=[10_000] * 5, assets=assets)
```

Which marks today's own funds and the 1-in-200 outcome:

{% include ft-chart.html id="solvency" src="/assets/data/financescenarios-charts.json" label="Distribution of own funds after one year" %}

### Validating the Output

Check a run against what its own models promise. Most variables can also be simulated with other published models through a single setting, such as [Hull-White](https://doi.org/10.1093/rfs/3.4.573), [CIR](https://doi.org/10.2307/1911242) and [regime-switching](https://doi.org/10.1080/10920277.2001.10595984) equities, and the published Wilkie, Ahlgrim, Hibbert and GOES specifications ship as whole factor sets.

```python
scenarios.validate(result)
```

For example, three of the checks are shown below.

| check                                  | status | detail                                                                                                                                   |
|:---------------------------------------|:-------|:-----------------------------------------------------------------------------------------------------------------------------------------|
| Every factor calibrated                | pass   | every factor calibrated                                                                                                                  |
| Simulation reproduces the correlations | pass   | largest gap 0.068 (us_broad/europe); pairs with a linked factor, not graded: largest gap 0.312 (eurozone_inflation/eurozone_unemployment) |
| Every path is finite                   | pass   | 27 factors, all finite                                                                                                                   |

**Find [every model and its status](/projects/financescenarios/docs/coverage) and [the validation documentation](/projects/financescenarios/docs/validation).**

### Starting Your Own Project

Everything above runs on the ready-made profiles as they ship. To change an assumption, add a market of your own or keep your results, copy the profiles into a folder of your own:

```python
from financescenarios import read_run, scaffold_project

scaffold_project("my-project")              # editable settings, factor sets, regimes, portfolios and a .env
path = scenarios.save(result, "results/")   # the run, its settings and its calibration, in its own folder
result = read_run(path)
```

Run Python from inside `my-project` and every run reads its YAML files instead of the bundled ones, and the keys pasted into its .env file, so the API key can be left out. A saved run reads back without downloading or simulating anything again. **Find [the configuration documentation](/projects/financescenarios/docs/configuration).**

## Notebooks

Each notebook covers a different part of Finance Scenarios. Click a card to open it.

<div class="bento-grid">

  <a href="/projects/financescenarios/getting-started" class="bento-card">
    <div class="bento-content">
      <i class="fas fa-rocket bento-icon"></i>
      <h2>Getting Started</h2>
      <p>If you are new to Finance Scenarios, start here: pick the profiles, simulate, read the overview and the spread of every variable, and chart it.</p>
    </div>
  </a>

  <a href="/projects/financescenarios/regimes-notebook" class="bento-card">
    <div class="bento-content">
      <i class="fas fa-bolt bento-icon"></i>
      <h2>Regimes</h2>
      <p>Run the scenarios through named stress stories such as an oil crisis, a financial crisis or a tech selloff, and compare them with the baseline.</p>
    </div>
  </a>

  <a href="/projects/financescenarios/portfolio-notebook" class="bento-card">
    <div class="bento-content">
      <i class="fas fa-briefcase bento-icon"></i>
      <h2>Portfolio</h2>
      <p>Put an investment mix through every scenario: its value, rebalancing, risk, saving and withdrawal plans, glidepaths and fees.</p>
    </div>
  </a>

  <a href="/projects/financescenarios/portfolio-analysis-notebook" class="bento-card">
    <div class="bento-content">
      <i class="fas fa-history bento-icon"></i>
      <h2>Portfolio Analysis</h2>
      <p>Backtest a mix against what prices actually did, measure its exposure to the Fama-French factors and compare two portfolios head to head.</p>
    </div>
  </a>

  <a href="/projects/financescenarios/model-validation-notebook" class="bento-card">
    <div class="bento-content">
      <i class="fas fa-vial bento-icon"></i>
      <h2>Model Validation</h2>
      <p>Check the default model against history: do the factors move together the way the economy does, and would a past calibration have held what happened next?</p>
    </div>
  </a>

</div>

## Questions & Answers

<details class="ft-details" markdown="1">
  <summary><h3>Do I need an economic scenario generator?</h3></summary>

  When the answer you need is a range rather than one number. A single forecast tells you where rates or markets are expected to go; it says nothing about how bad things could get, how often, or what moves together when they do. Those are exactly the questions behind Solvency II capital and technical provisions, pension funding projections, asset-liability matching, portfolio tail risk, stress testing and whether retirement withdrawals last thirty years.

  A scenario generator answers them by simulating thousands of internally consistent paths for the whole economy: when inflation rises, rates and unemployment respond in the same scenario, and equities share their crisis spells. You then put your assets or liabilities through every path and read the full distribution: the median, the bad year in twenty, the 1-in-200 event.

  You don't need one when one number is enough: a point forecast for a budget, or a single prescribed shock such as the Solvency II standard formula, which applies fixed stresses rather than a simulation.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>How does this relate to the Finance Toolkit?</h3></summary>

  They are two halves of the same workflow. The [Finance Toolkit](https://github.com/JerBouma/FinanceToolkit) looks backwards: it retrieves and calculates from historical data, from financial statements and ratios to yield curves, inflation and unemployment. Finance Scenarios looks forwards: it fits models to that history and simulates where things could go next.

  Finance Scenarios gets its history through the Finance Toolkit: market prices, government bond yields, OECD and central-bank series, EIOPA's risk-free curves and credit spreads. That means the scenarios start from the same data you would analyse in the Toolkit, and a backtest of a portfolio uses the same prices as its simulation.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>How do I know whether the method I need is supported?</h3></summary>

  The [coverage overview](/projects/financescenarios/docs/coverage) lists every factor, model, measure, portfolio analytic and Solvency II output as available, partial or unavailable. Where something is partial, it says what is missing: the risk-neutral rate volatility, for example, is fitted to historical yield moves rather than implied from swaption prices.

  Each model is documented with the paper it follows and the choices made where the implementation departs from it, so you can judge whether it fits your purpose before you run it. The guides explain the financial logic behind each factor, and every regulatory choice cites the article, section or table it comes from.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>Are my results reproducible?</h3></summary>

  Yes, once you pin down both of the things a run depends on. The random draws are fixed by a seed in the settings, so the same calibration with the same seed gives exactly the same scenarios.

  The calibration itself follows live data: every day adds observations, and statistical agencies revise past figures, so fitting again tomorrow gives slightly different parameters. To reproduce a result months later, for an audit trail or a regulatory submission, save the calibration together with the run. A saved calibration can be simulated again with more scenarios or another seed without downloading or fitting anything, and a saved run keeps its settings alongside the results.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>How long does a run take?</h3></summary>

  Most of the time goes into the first calibration: downloading the history for every factor and fitting each model. For the default factor set that takes a couple of minutes on a cold cache, and seconds once the data is cached.

  Simulating is fast by comparison and grows with the number of scenarios and the length of the horizon. For long projections the long-horizon settings use 500 scenarios instead of 2,000 to keep runs quick. A risk-neutral run for valuation calibrates its own market-consistent setup, so it adds a second fit.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>Can I add my own regime, portfolio or model?</h3></summary>

  Yes. Regimes, portfolios and profiles are plain YAML files, so the easiest start is to copy a shipped one into your own project folder and edit it. A regime can shift an assumption before simulating (inflation pulled toward a level by a given year), keep only the scenarios that fit its story (high rates and weak stocks), or both. A portfolio sets the weights of its holdings, the duration of its bond funds and how often it rebalances. A profile of your own can extend a shipped one and state only what differs.

  Your own views on long-run levels, such as a central bank's inflation target or an equity risk premium, go in as beliefs that override the fitted values. A new model or factor plugs into the same calibration and correlation steps as the shipped ones, so it is linked to everything else automatically; the [reference](/projects/financescenarios/docs/reference) shows what each one provides.

</details>

## Contributing

First of all, thank you for taking the time to contribute (or at least read the section about contributing)! 🚀

The most useful contributions are the gaps marked unavailable or partial in the [coverage overview](/projects/financescenarios/docs/coverage), for which the [`resources`](https://github.com/JerBouma/FinanceScenarios/tree/main/resources) catalog usually already names the paper, and validation against a published scenario set this project does not check yet. If a calibration here disagrees with your own implementation or with a vendor's, please open an issue. Read the [architecture](/projects/financescenarios/docs/architecture) before opening a pull request, and run the tests:

```bash
uv sync --all-extras --group dev
uv run pytest tests
```

## Contact

If you have any questions about Finance Scenarios or would like to share what you have been working on, reach out via the [contact page](/contact).

{% include ft-charts-script.html %}
