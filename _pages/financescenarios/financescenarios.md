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

Every table below is real output, cut to a few rows, and every chart is interactive, from one run calibrated on {{ site.data.financescenarios_run.date }}. Live data moves, so another day gives slightly different numbers. The full [documentation](/projects/financescenarios/docs) explains each model and its assumptions.

Every run combines two ready-made *profiles*: a **settings** profile, which says how the run goes (how many scenarios, how far ahead, how much history to learn from), and a **factor set**, which says what gets simulated (which interest rates, stock markets, currencies and so on). Optionally a **regime** adds a stress story, and a **portfolio** is an investment mix to read the scenarios through. Each kind comes with ready-made options:

```python
from financescenarios import list_presets

list_presets(kind="settings")  # or "factor-sets", "regimes", "portfolios"; leave it out for all 39
```

Open a kind below to see what each option is for.

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

### Simulating Correlated Scenarios {#simulating-scenarios}

Each variable is fitted to its own history, and the shocks are drawn jointly so the scenarios keep the co-movements seen in that history. That matters because risks rarely arrive alone: in a typical recession, equities fall, unemployment rises and central banks cut short rates.

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(
    settings="default",
    factor_set="default",
    api_key="FINANCIAL_MODELING_PREP_KEY",
    fred_api_key="FRED_KEY",  # optional
)
result = scenarios.simulate(n_simulations=2000)

result.describe()
result.plot(["united_states_short_rate", "united_states_inflation"])
```

Rates are annual rates and priced assets annualized returns, as decimals; `terminal_q05` and `terminal_q95` are the levels that 1 in 20 scenarios end below and above after five years.

| factor                     | initial | terminal_mean | terminal_q05 | terminal_q95 |
|:---------------------------|--------:|--------------:|-------------:|-------------:|
| united_states_inflation    |  0.0340 |        0.0262 |      -0.0033 |       0.0549 |
| united_states_short_rate   |  0.0406 |        0.0442 |       0.0050 |       0.0859 |
| united_states_unemployment |  0.0410 |        0.0557 |       0.0210 |       0.0904 |
| us_broad                   |         |        0.0983 |      -0.0465 |       0.2318 |
| europe                     |         |        0.0766 |      -0.0925 |       0.2197 |
| gold                       |         |        0.0596 |      -0.0614 |       0.1936 |

The table gives the end point; the fan charts show how the range opens up month by month, with the median and the bands holding half and nine in ten of the scenarios.

{% include ft-chart.html id="simulation" src="/assets/data/financescenarios-charts.json" label="Simulated short rate, inflation and US equities" %}

The US short rate starts at 4.06% and averages 4.42% after five years, but 1 in 20 scenarios end below 0.50% and 1 in 20 above 8.59%. In money, 100 in US equities becomes 161 in the median scenario, below 79 in the worst 1 in 20 and above 284 in the best. **Find [the Notebook](/projects/financescenarios/getting-started) and [the simulation documentation](/projects/financescenarios/docs/simulation-engine).**

### Reading the Tails

The mean hides the asymmetry that matters for risk. The distribution of the five-year equity return shows it directly.

```python
result.summary_statistics("us_broad")
result.plot("us_broad", kind="distribution")
```

{% include ft-chart.html id="distribution" src="/assets/data/financescenarios-charts.json" label="Distribution of the five-year US equity return" %}

The median scenario returns 10.04% a year, above the 9.83% mean, because the left tail reaches further than the right: the worst 1 in 20 lose more than 4.65% a year, 14.7 points below the median, while the best 1 in 20 gain more than 23.18%, 13.1 points above it. These equity returns are fitted on history; for planning work, a long-run [belief](/projects/financescenarios/docs/configuration#beliefs) about the equity return is advisable. **Find [the documentation](/projects/financescenarios/docs/units).**

### Building a Portfolio

An asset mix inherits the correlations of its holdings, so diversification shows up in the scenarios rather than being assumed. Here a 60/40 of US stocks and Treasuries, rebalanced once a year. Shipped mixes range from all-weather and permanent portfolios to a target-date glidepath and an endowment model.

```python
from financescenarios import Portfolio

portfolio = Portfolio.from_preset(result, preset="balanced_60_40")
values = portfolio.compute(initial_value=100_000, rebalance_every=12)
values.plot(levels=True)
```

{% include ft-chart.html id="portfolio" src="/assets/data/financescenarios-charts.json" label="Simulated value of a 60/40 portfolio" %}

The 60/40 earns 8.34% a year on average, less than the stocks' 9.83% but with a narrower range. The median scenario turns 100,000 into 150,012 and the best 1 in 20 into more than 210,721, while the worst 1 in 20 end below 99,780: five years without a gain. Drawdowns, Value at Risk, saving and withdrawal plans, glidepaths and fees build on the same values. **Find [the Notebook](/projects/financescenarios/portfolio-notebook).**

### Applying Stress Regimes

A stress regime tells a story: it shifts an assumption before simulating (inflation pulled towards 12%), keeps only the scenarios consistent with the story (high rates and weak stocks), or both. Because the kept scenarios still come from the fitted model, the other variables move with the stress in a way the history supports. Twelve regimes ship, from an oil crisis and a credit crunch to a soft landing and a yield-curve inversion.

```python
from financescenarios import compare_runs

shocked = scenarios.simulate(regime="oil_crisis", n_simulations=2000)
compare_runs({"baseline": result, "oil_crisis": shocked})
```

| factor                   | baseline | oil_crisis |
|:-------------------------|---------:|-----------:|
| united_states_inflation  |   0.0262 |     0.0492 |
| united_states_short_rate |   0.0442 |     0.0648 |
| us_broad                 |   0.0983 |     0.0161 |
| europe                   |   0.0766 |     0.0178 |

The stories differ in timing as much as in size. Below, US inflation under three regimes against the baseline, each with its median and spread.

{% include ft-chart.html id="regimes" src="/assets/data/financescenarios-charts.json" label="US inflation in the baseline and under three stress regimes" %}

In the oil crisis, US inflation ends at 4.92% instead of 2.62% and stocks return 1.61% a year instead of 9.83%. The oil shock follows the baseline until its shock hits in January 2028 and then fades, while the oil crisis and climate collapse lift inflation from the first month. **Find [the Notebook](/projects/financescenarios/regimes-notebook) and [the regime documentation](/projects/financescenarios/docs/regimes).**

### Backtesting Against History

Any number of mixes can run against what prices actually did, on one shared calendar, with their exposure measured against the [Fama-French factors](https://doi.org/10.1016/j.jfineco.2014.10.010) from [Ken French's data library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html).

```python
portfolio = Portfolio.backtest(scenarios, ["balanced_60_40", "all_weather", "permanent_portfolio"])
portfolio.factor_exposure()
portfolio.compute(initial_value=100_000, rebalance_every=12).plot(levels=True)
```

| portfolio           | Mkt-RF |     SMB |     HML |    RMW |     CMA |  alpha | r_squared | from       | to         |
|:--------------------|-------:|--------:|--------:|-------:|--------:|-------:|----------:|:-----------|:-----------|
| 60/40 Balanced      | 0.5369 | -0.0687 | -0.0447 | 0.1215 | -0.0116 | 0.0007 |    0.8615 | 2000-08-01 | 2026-10-01 |
| All Weather         | 0.2039 | -0.0620 | -0.1435 | 0.2162 |  0.0335 | 0.0029 |    0.1318 | 2000-08-01 | 2026-10-01 |
| Permanent Portfolio | 0.2173 | -0.0615 | -0.1418 | 0.2017 |  0.0473 | 0.0033 |    0.1240 | 2000-08-01 | 2026-10-01 |

The loadings say how each mix is built; the chart shows where that took 100,000 invested in August 2000.

{% include ft-chart.html id="backtest" src="/assets/data/financescenarios-charts.json" label="Historical value of the 60/40, All Weather and Permanent Portfolio mixes since 2000" %}

The three mixes ended within 3% of each other: 100,000 invested in August 2000 grew to 550,762 in the 60/40, 541,823 in All Weather and 556,105 in the Permanent Portfolio by October 2026. They got there very differently. The 60/40 carries more than twice the stock-market loading of the other two (0.54 against about 0.21), and the five factors explain 86% of its monthly moves but only 13% of the others', whose bonds and gold the equity factors don't capture. Its deepest fall was 28% from the peak, in February 2009; the other two fell furthest in September 2022, by 21% and 15%, when stocks and bonds dropped together. **Find [the Notebook](/projects/financescenarios/portfolio-analysis-notebook).**

### Valuing Liabilities and Capital Under Solvency II

[Solvency II](https://eur-lex.europa.eu/eli/dir/2009/138/oj) needs two views of the same economy. Liabilities are valued market-consistently, from a risk-neutral run: under that measure every asset is expected to earn the risk-free rate, so its discounted total-return price is a martingale and the scenarios reproduce today's prices. Capital is the one-year 99.5% loss of own funds, read from the real-world run. Below, 10,000 a year for five years is backed by 60,000 in the 60/40.

```python
from financescenarios import Solvency

risk_neutral = scenarios.simulate(n_simulations=2000, measure="risk_neutral")
solvency = Solvency(real_world=result, risk_neutral=risk_neutral)

assets = Portfolio.from_preset(result, preset="balanced_60_40").compute(initial_value=60_000, rebalance_every=12)
solvency.report(cashflows=[10_000] * 5, assets=assets)
```

| item                | value                     | meaning                                                    |
|:--------------------|:--------------------------|:-----------------------------------------------------------|
| market consistent   | passed (largest gap 0.7%) | discounted back, us_broad stays within 2% of today's price |
| best estimate       | 43,514                    | what the payments are worth today                          |
| own funds           | 15,657                    | assets minus what is owed, today                           |
| SCR (1 in 200 year) | 12,482                    | the capital that survives a 1-in-200 bad year              |
| solvency ratio      | 1.25                      | own funds / SCR; above 1 means enough capital              |

Behind the SCR is the distribution of own funds one year ahead, discounted to today, across the 2,000 scenarios.

{% include ft-chart.html id="solvency" src="/assets/data/financescenarios-charts.json" label="Distribution of own funds after one year" %}

The SCR of 12,482 is the distance from today's own funds to the 1-in-200 outcome at the left of the chart, where own funds fall to around 3,200. A ratio of 1.25 means the 60,000 covers both the payments and the required capital. **Find [the documentation](/projects/financescenarios/docs).**

### Validating the Output

A scenario set is only useful if it does what its models promise. Each run can be checked for plausible fitted parameters, a valid correlation matrix, simulated correlations and volatilities in line with the calibration and history, and finite paths. Most variables can also be simulated with alternative published models, such as [Hull-White](https://doi.org/10.1093/rfs/3.4.573), [CIR](https://doi.org/10.2307/1911242) and [regime-switching](https://doi.org/10.1080/10920277.2001.10595984) equities, so model risk can be compared directly.

```python
scenarios.validate(result)
```

**Find [every model and its status](/projects/financescenarios/docs/coverage) and [the validation documentation](/projects/financescenarios/docs/validation).**

### Starting Your Own Project

To change an assumption, add a market or keep your results, copy the profiles into a folder of your own; runs from there read your files instead of the bundled ones.

```python
from financescenarios import read_run, scaffold_project

scaffold_project("my-project")              # editable settings, factor sets, regimes and portfolios
path = scenarios.save(result, "results/")   # the run with its settings and calibration
result = read_run(path)                     # read it back without fitting again
```

**Find [the configuration documentation](/projects/financescenarios/docs/configuration).**

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

  Each model is documented with the paper it follows and the choices made where the implementation departs from it, so you can judge whether it fits your purpose before you run it. The guides explain the financial logic behind each factor, and the regulatory choices quote the source text they come from.

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

## Contact

If you have any questions about Finance Scenarios or would like to share what you have been working on, reach out via the [contact page](/contact).

{% include ft-charts-script.html %}
