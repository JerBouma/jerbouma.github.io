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

The goal is not to compete with a vendor model but to make the published methods accessible and reproducible in the open. Every calibration method is written out in plain Python and linked to the paper it came from, from [Wilkie (1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf) and [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf) to [Hibbert, Mowbray and Turnbull (2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf), [Cairns, Blake and Dowd (2006)](https://www.macs.hw.ac.uk/~andrewc/papers/jri2006e.pdf) and [Koijen, Nijman and Werker (2010)](https://doi.org/10.1093/rfs/hhp058), with a documentation page per factor and per model. The assumptions, parameters, beliefs and correlations all live in files you can edit, so you can change one and run it again to see what it does. The results still depend on the assumptions you chose, on the data available, and on your own judgement.

<img src="/assets/images/projects/financescenarios/banner.png" alt="Finance Scenarios" width="100%"/>

## Installation

The project requires Python 3.11 or higher. To install Finance Scenarios it simply requires the following:

```bash
pip install financescenarios -U
```

To be able to get the most out of it, you need an API key from FinancialModelingPrep. It is used for the price histories behind every ticker-priced factor: stock markets such as the S&P 500 (`SPY`), Europe (`VGK`) and Japan (`EWJ`), Treasury yields such as the 10-year (`^TNX`), commodities such as gold (`GC=F`) and Brent oil (`BZ=F`), and the dividends of those funds. Note that the Free plan is limited to 250 requests each day, 5 years of data and only companies listed on US exchanges.

[Obtain an API Key from FinancialModelingPrep](/fmp){: .btn .btn--warning .btn--large .align-center target="_blank"}

Through the link you are able to subscribe for the free plan and also premium plans at a **15% discount**. This is an affiliate link and thus supports the project at the same time.

Optionally, add a free [FRED key](https://fred.stlouisfed.org/docs/api/api_key.html) from the Federal Reserve Bank of St. Louis. It is used for US corporate bond spreads (the ICE BofA option-adjusted spreads behind `credit`), US commercial property prices (`real_estate` with `source: commercial`) and the market's expected inflation from breakevens (`inflation` with `target_source: breakeven`). The [configuration documentation](/projects/financescenarios/docs/configuration#secrets) lists exactly which key each factor uses. The `default` factor set reads EIOPA's risk-free curves, which need Finance Toolkit 2.2.2 or newer (`pip install -U financetoolkit`).


## Functionality

This section is an introduction to Finance Scenarios, run on the default settings and the default factor set (the US, the euro area and the UK) with 2,000 scenarios. Every table is the actual output of the snippet above it, cut down to a few rows, and every chart is interactive and drawn from the same kind of run, calibrated on 2026-10-08 (the stress regime, backtest and Solvency II charts on 2026-10-10); live data moves, so another day gives slightly different numbers. Every class also documents itself (try `help(Portfolio)`).

There is also full [documentation](/projects/financescenarios/docs) and, further down the page, the Notebooks section with many examples.

Every run combines two ready-made *profiles*: a **settings** profile, which says how the run goes (how many scenarios, how far ahead, how much history to learn from), and a **factor set**, which says what gets simulated (which interest rates, stock markets, currencies and so on). Optionally a **regime** adds a stress story, and a **portfolio** is an investment mix to read the scenarios through. `list_presets()` shows every one of them with what it is for and the call it goes in; `kind=` narrows it to one kind:

```python
from financescenarios import list_presets

list_presets(kind="settings")  # or "factor-sets", "regimes", "portfolios"; leave it out for all 39
```

Each kind's output is below; open one to see its options.

<details markdown="1">
<summary><b>Settings profiles (4)</b>, passed as <code>Scenarios.from_profiles(settings="...")</code></summary>

| id           | description                                                                                                                                    |
|:-------------|:-----------------------------------------------------------------------------------------------------------------------------------------------|
| default      | 2,000 scenarios, one step a month, five years ahead, fitted on history since 2000.                                                               |
| goes         | Default, but fitted on history since 2019 only; pair it with the goes factor set to match the NAIC's scenario generator.                       |
| long_horizon | Default with 500 scenarios instead of 2,000, so multi-decade runs stay fast; pick the length with simulate(years=30).                            |
| wilkie       | Default, fitted on 1995 to 2019 only, as the wilkie set needs.                                                                                 |

</details>

<details markdown="1">
<summary><b>Factor sets (9)</b>, passed as <code>Scenarios.from_profiles(factor_set="...")</code></summary>

| id              | description                                                                                                                                           |
|:----------------|:------------------------------------------------------------------------------------------------------------------------------------------------------|
| ahlgrim         | The six factors of Ahlgrim, D'Arcy and Gorvett (2005): short rate, inflation, equities, unemployment, real estate and dividend yield.                 |
| broad           | Everything this project can simulate, across many countries: the widest set, and the slowest to fit.                                                  |
| core            | The US, the euro area and the UK, with global equities, gold, oil and the major currencies; a curated set that passes every release check.            |
| default         | Core, with interest rates anchored to EIOPA's official forward rates and their swings fitted on rates since 1950; the recommended starting point.     |
| goes            | US Only, with the short rate's long-run level set to the NAIC scenario generator's own (about 3.67%); pair it with the goes settings.                 |
| hibbert         | The two-factor model of Hibbert, Mowbray and Turnbull (2001): short rate and inflation that chase moving targets, regime-switching equities.          |
| private_markets | US Only plus listed stand-ins for private equity, infrastructure, hedge funds and private credit.                                                     |
| us_only         | The United States only: its rates, inflation, unemployment and stock market, plus currencies, commodities and the other shared factors; quick to run. |
| wilkie          | The original Wilkie (1986) actuarial model: inflation, dividends, a consols rate and share prices; pair it with the wilkie settings.                  |

</details>

<details markdown="1">
<summary><b>Stress regimes (12)</b>, passed as <code>Scenarios.from_profiles(regime="...")</code>, see <a href="#applying-stress-regimes">Applying Stress Regimes</a></summary>

| id                    | description                                                                                                                                           |
|:----------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------|
| climate_collapse      | Rough stand-in for a climate shock: keeps the scenarios with the highest US inflation and the weakest US stocks.                                        |
| commodity_supercycle  | A long oil boom: keeps the scenarios where crude oil earns a top-quarter return.                                                                        |
| credit_crunch         | Bank stocks collapse and the market follows: a harsher bear market for financials, then their worst scenarios. Needs the financials equity (broad set). |
| currency_crisis       | The Brazilian real devalues sharply against the dollar, about 22% a year, then keeps its worst scenarios. Needs the us_only or broad set.               |
| financial_crisis      | Stocks fall, unemployment rises and rates are cut, all at once: keeps the scenarios where that happens together.                                        |
| oil_crisis            | Pulls inflation towards 9% in year one and back to 2.5% by year 8, then keeps the scenarios with high rates and weak stocks.                              |
| oil_shock             | A one-off three-point jump in US inflation in year 2, after which everything behaves normally again.                                                  |
| rate_cut_cycle        | Inflation eases to 2% by year 5 and 2.5% by year 10, then drifts back to its usual level.                                                             |
| real_estate_crash     | House-price growth falls to -8% within a year and recovers over four, then keeps the worst housing scenarios.                                           |
| soft_landing          | Inflation eases smoothly to 2% by year 5 and stays there; no scenarios are filtered out.                                                                |
| tech_selloff          | Tech stocks fall while the wider market holds up; keeps the worst tech scenarios. Needs the broad set.                                                  |
| yield_curve_inversion | Short rates rise two points above long ones within six months, then the curve slowly rights itself.                                                   |

</details>

<details markdown="1">
<summary><b>Portfolios (14)</b>, passed as <code>Portfolio.from_preset(result, preset="...")</code>, see <a href="#building-a-portfolio">Building a Portfolio</a></summary>

| id                    | description                                                                                                                                   |
|:----------------------|:----------------------------------------------------------------------------------------------------------------------------------------------|
| all_weather           | Ray Dalio's mix for every economic climate: 30% US stocks, 55% long US Treasuries and 15% gold.                                               |
| balanced_60_40        | The textbook mix: 60% US stocks and 40% US Treasury bonds.                                                                                    |
| barbell               | Nassim Taleb's barbell: 80% Treasury bills, 20% small-cap and growth stocks, nothing in between. Needs the broad set.                         |
| bogleheads_three_fund | The Bogleheads' three funds: 40% US stocks, 20% international stocks and 40% US Treasury bonds. Needs the default, core or broad set.         |
| buffett_90_10         | Warren Buffett's advice for his estate: 90% in an S&P 500 fund and 10% in Treasury bills.                                                     |
| conservative_income   | Mostly US, euro-area and UK government bonds, with 10% in US stocks for growth. Needs the default, core or broad set.                         |
| endowment_model       | A university-endowment mix with 40% in listed stand-ins for private markets. Needs the private_markets set.                                   |
| global_60_40          | The 60/40 spread across countries: US, European and emerging-market stocks; US, euro-area and UK bonds. Needs the default, core or broad set. |
| global_equity_growth  | All stocks, spread across the US, Europe, Japan, emerging markets and China, tilted to growth. Needs the broad set.                           |
| golden_butterfly      | Equal fifths of stocks, small-cap and value stocks, long bonds, Treasury bills and gold. Needs the broad set.                                 |
| permanent_portfolio   | Harry Browne's four quarters: US stocks, long US Treasuries, Treasury bills and gold.                                                         |
| small_cap_value_tilt  | 80% in small-cap and value stocks, the Fama-French premia, with 20% US Treasury bonds. Needs the broad set.                                   |
| target_date_glidepath | A target-date fund: 90% stocks today, gliding to 30% stocks over 30 years as the target date nears.                                           |
| us_equity_sectors     | All stocks, split evenly across nine US sectors. Needs the broad set.                                                                         |

</details>

The examples below use the default settings and the default factor set.

### Simulating Scenarios

Fit every variable to its history and draw 2,000 scenarios at once. The API keys go in here, as with the Finance Toolkit; leave them out to read them from the `FINANCIAL_MODELING_PREP_API_KEY` and `FRED_API_KEY` environment variables or a `.env` file.

```python
from financescenarios import Scenarios

# The default settings and the default factor set: the US, the euro area and the UK
scenarios = Scenarios.from_profiles(
    settings="default",
    factor_set="default",
    api_key="FINANCIAL_MODELING_PREP_KEY",  # replace with your actual API key
    fred_api_key="FRED_KEY",  # optional, replace with your actual FRED key or leave it out
)
result = scenarios.simulate(n_simulations=2000)

# Where every variable starts and where it ends up after five years
result.describe()
```

For example, 6 of the 27 variables are shown below. Rates are yearly rates and anything with a price a yearly return, written as decimals (`0.0441` is 4.41%); `terminal_q05` and `terminal_q95` are what 1 in 20 scenarios end below and above.

| factor                     | category       | initial | terminal_mean | terminal_q05 | terminal_q95 |
|:---------------------------|:---------------|--------:|--------------:|-------------:|-------------:|
| united_states_inflation    | inflation      |  0.0340 |        0.0283 |      -0.0005 |       0.0570 |
| united_states_short_rate   | interest_rates |  0.0404 |        0.0441 |       0.0049 |       0.0858 |
| united_states_unemployment | unemployment   |  0.0410 |        0.0558 |       0.0216 |       0.0903 |
| us_broad                   | equities       |         |        0.0983 |      -0.0465 |       0.2321 |
| europe                     | equities       |         |        0.0768 |      -0.0918 |       0.2204 |
| gold                       | commodities    |         |        0.0586 |      -0.0643 |       0.1959 |

And below the short rate, inflation and US equities are plotted with `result.plot(["united_states_short_rate", "united_states_inflation", "us_broad"])`. **Find the Notebook [here](/projects/financescenarios/getting-started) and the simulation documentation [here](/projects/financescenarios/docs/simulation-engine).**

{% include ft-chart.html id="simulation" src="/assets/data/financescenarios-charts.json" label="Simulated short rate, inflation and US equity return" %}

### Reading the Distribution

Follow any variable date by date as percentile bands, or read it off at chosen horizons with `result.horizon_summary([1, 3, 5])`.

```python
result.summary_statistics("united_states_short_rate")
```

For example, the last three months of the US short rate are shown below.

| date       |   mean |    std |  q0.05 |  q0.25 |   q0.5 |  q0.75 |  q0.95 |
|:-----------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| 2030-11-01 | 0.0441 | 0.0244 | 0.0047 | 0.0276 | 0.0445 | 0.0600 | 0.0856 |
| 2030-12-02 | 0.0440 | 0.0245 | 0.0042 | 0.0275 | 0.0437 | 0.0606 | 0.0854 |
| 2031-01-01 | 0.0441 | 0.0245 | 0.0049 | 0.0275 | 0.0442 | 0.0602 | 0.0858 |

And below the spread of the five-year US equity return is plotted with `result.plot("us_broad", kind="distribution")`. **Find the documentation [here](/projects/financescenarios/docs/units).**

{% include ft-chart.html id="distribution" src="/assets/data/financescenarios-charts.json" label="Distribution of the five-year US equity return" %}

### Building a Portfolio

Put an investment mix through the same scenarios with `Portfolio`, here the 60/40 (60% US stocks, 40% US government bonds) from the 14 ready-made mixes, rebalanced once a year.

```python
from financescenarios import Portfolio

# 60% broad US equities, 40% US government bonds, rebalanced once a year
portfolio = Portfolio.from_preset(result, preset="balanced_60_40")
values = portfolio.compute(initial_value=100_000, rebalance_every=12)

values.describe()
```

This returns the portfolio's yearly return over the five years, and that of each holding:

| factor                        | category  | initial | terminal_mean | terminal_q05 | terminal_q95 |
|:------------------------------|:----------|--------:|--------------:|-------------:|-------------:|
| portfolio                     | portfolio |         |        0.0837 |      -0.0000 |       0.1611 |
| us_broad_value                | holding   |         |        0.0837 |      -0.0000 |       0.1611 |
| united_states_long_rate_value | holding   |         |        0.0837 |      -0.0000 |       0.1611 |

The 60/40 earns 8.37% a year on average, so 100,000 grows to 152,553. `portfolio.risk_metrics()` adds the drawdowns and Value at Risk, and the same module covers saving and withdrawal plans, glidepaths and fees. And below the value is plotted in money with `values.plot(levels=True)`. **Find the Notebook [here](/projects/financescenarios/portfolio-notebook).**

{% include ft-chart.html id="portfolio" src="/assets/data/financescenarios-charts.json" label="Simulated value of a 60/40 portfolio" %}

### Applying Stress Regimes

Run the same variables through one of 12 named stress stories, such as an oil crisis. A regime changes an assumption before simulating, keeps only the scenarios that fit the story, or both.

```python
from financescenarios import compare_runs

oil_crisis = Scenarios.from_profiles(regime="oil_crisis", api_key="FINANCIAL_MODELING_PREP_KEY")
shocked = oil_crisis.simulate(keep=2000)

compare_runs({"baseline": result, "oil_crisis": shocked})
```

`Oil Crisis` pulls US inflation towards 9% and keeps the scenarios with high interest rates and weak stocks; `keep=2000` draws enough scenarios that 2,000 fit the story. For example, four of the variables are shown below.

| factor                   | baseline | oil_crisis |
|:-------------------------|---------:|-----------:|
| united_states_inflation  |   0.0283 |     0.0516 |
| united_states_short_rate |   0.0441 |     0.0647 |
| us_broad                 |   0.0983 |     0.0178 |
| europe                   |   0.0768 |     0.0201 |

And below US inflation is plotted for the baseline and the Oil Shock, Oil Crisis and Climate Collapse regimes with `plot_runs(runs, "united_states_inflation")`, 2,000 scenarios each. **Find the Notebook [here](/projects/financescenarios/regimes-notebook) and the regime documentation [here](/projects/financescenarios/docs/regimes).**

{% include ft-chart.html id="regimes" src="/assets/data/financescenarios-charts.json" label="US inflation in the baseline and under three stress regimes" %}

### Backtesting Against History

Run the same portfolio against what prices actually did, and measure what it is exposed to with the [Fama-French factors](https://doi.org/10.1016/j.jfineco.2014.10.010) from [Ken French's data library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html).

```python
# What the 60/40's holdings actually did, month by month, as one "scenario"
history = scenarios.history(portfolio="balanced_60_40")
portfolio = Portfolio.from_preset(history, preset="balanced_60_40")

portfolio.factor_exposure()
```

Which gives the mix's loading on each factor and how much they explain:

| portfolio      | Mkt-RF |     SMB |     HML |    RMW |     CMA |  alpha | r_squared | observations | from       | to         |
|:---------------|-------:|--------:|--------:|-------:|--------:|-------:|----------:|-------------:|:-----------|:-----------|
| 60/40 Balanced | 0.5399 | -0.0714 | -0.0420 | 0.1201 | -0.0168 | 0.0008 |    0.8654 |          319 | 2000-01-01 | 2026-10-01 |

And below is what the 60/40 actually did since 2000, plotted with `portfolio.compute(initial_value=100_000, rebalance_every=12).plot(levels=True)`: 100,000 grew to 628,180 by October 2026. **Find the Notebook [here](/projects/financescenarios/portfolio-analysis-notebook).**

{% include ft-chart.html id="backtest" src="/assets/data/financescenarios-charts.json" label="Historical value of a 60/40 portfolio since 2000" %}

### Valuing Liabilities and Capital Under Solvency II

Value what an insurer owes from a run priced like today's market (risk-neutral) and its one-year 99.5% capital requirement (the SCR) from the real-world run, as [Solvency II](https://eur-lex.europa.eu/eli/dir/2009/138/oj) asks.

```python
from financescenarios import Solvency

# The same factors priced the way markets price them today, for valuing what is owed
risk_neutral = scenarios.simulate(n_simulations=2000, measure="risk_neutral")
solvency = Solvency(real_world=result, risk_neutral=risk_neutral)

# Pay out 10,000 a year for five years, backed by 60,000 invested in the 60/40
assets = Portfolio.from_preset(result, preset="balanced_60_40").compute(initial_value=60_000, rebalance_every=12)
solvency.report(cashflows=[10_000] * 5, assets=assets)
```

Which gives every number in one table:

| item                | value                     | meaning                                                    |
|:--------------------|:--------------------------|:-----------------------------------------------------------|
| market consistent   | passed (largest gap 1.0%) | discounted back, us_broad stays within 2% of today's price |
| best estimate       | 43,444                    | what the payments are worth today                          |
| own funds           | 15,635                    | assets minus what is owed, today                           |
| SCR (1 in 200 year) | 12,453                    | the capital that survives a 1-in-200 bad year              |
| solvency ratio      | 1.26                      | own funds / SCR; above 1 means enough capital              |

And below is where own funds could be after one year, plotted with `solvency.plot(cashflows=[10_000] * 5, assets=assets)`. **Find the documentation [here](/projects/financescenarios/docs).**

{% include ft-chart.html id="solvency" src="/assets/data/financescenarios-charts.json" label="Distribution of own funds after one year" %}

### Validating the Output

Check a run against what its own models promise. Most variables can also be simulated with other published models through one `method:` setting, such as [Hull-White](https://doi.org/10.1093/rfs/3.4.573), [CIR](https://doi.org/10.2307/1911242) and [regime-switching](https://doi.org/10.1080/10920277.2001.10595984) equities, and the published `wilkie`, `ahlgrim`, `hibbert` and `goes` specifications ship as whole factor sets.

```python
scenarios.validate(result)
```

For example, three of the checks are shown below.

| check                                  | status | detail                                                                                                                                   |
|:---------------------------------------|:-------|:-----------------------------------------------------------------------------------------------------------------------------------------|
| Every factor calibrated                | pass   | every factor calibrated                                                                                                                  |
| Simulation reproduces the correlations | pass   | largest gap 0.067 (us_broad/europe); pairs with a linked factor, not graded: largest gap 0.219 (eurozone_inflation/eurozone_unemployment) |
| Every path is finite                   | pass   | 27 factors, all finite                                                                                                                   |

**Find every model and its status [here](/projects/financescenarios/docs/coverage) and the validation documentation [here](/projects/financescenarios/docs/validation).**

### Starting Your Own Project

Everything above runs on the ready-made profiles as they ship. To change an assumption, add a market of your own or keep your results, copy the profiles into a folder of your own:

```python
from financescenarios import read_run, scaffold_project

scaffold_project("my-project")              # editable settings, factor sets, regimes, portfolios and a .env
path = scenarios.save(result, "results/")   # the run, its settings and its calibration, in its own folder
result = read_run(path)
```

Run Python from inside `my-project` and every run reads its YAML files instead of the bundled ones, and the keys pasted into `my-project/.env`, so `api_key` can be left out. `read_run` reads a saved run back without downloading or simulating anything again. **Find the configuration documentation [here](/projects/financescenarios/docs/configuration).**

## Notebooks

Each of the Jupyter Notebooks below covers a different part of Finance Scenarios. Click any card to open the notebook.

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

</div>

## Questions & Answers

This section includes frequently asked questions. If yours is not answered here, feel free to reach out to me via the contact details below.

> **Do I need an economic scenario generator?**

When the answer you need is a range rather than one number. A forecast gives the expected outcome; an ESG shows the bad 5% of cases too. That comes up in Solvency II capital and technical provisions, pension funding projections, asset-liability matching, portfolio tail risk, stress testing and whether retirement withdrawals last.

> **How does this relate to the Finance Toolkit?**

The [Finance Toolkit](https://github.com/JerBouma/FinanceToolkit) looks backwards: it retrieves and calculates from historical data. Finance Scenarios looks forwards: it fits models to that history to simulate where things could go next, with the Finance Toolkit as its data layer.

> **How do I know whether the method I need is supported?**

The [coverage overview](/projects/financescenarios/docs/coverage) lists every factor, model, measure, portfolio analytic and Solvency II read as available, partial or unavailable. A run also logs a notice when your configuration hits one of the documented gaps; `set_log_level("INFO")` prints it.

> **Are my results reproducible between runs?**

The random draws are, through the seed in the settings. The calibration follows live data, so store it with `CalibrationResult.save()` and replay it later with `.load()` to pin both.

> **How long does a run take?**

Calibration takes the time: a couple of minutes for the default factor set on a cold cache and seconds once the Finance Toolkit has cached the data. Simulating is fast; pass a small `n_simulations` while you experiment.

> **Can I add my own factor, model, regime or portfolio?**

A regime or a portfolio is a YAML file, so copy a shipped one and edit it. A new model or factor follows the [architecture](/projects/financescenarios/docs/architecture): a `_model.py` for the calculation and a `_controller.py` that fetches the data.

## Contact

If you have any questions about Finance Scenarios or would like to share with me what you have been working on, feel free to reach out to me via the [contact page](/contact).

{% include ft-charts-script.html %}
