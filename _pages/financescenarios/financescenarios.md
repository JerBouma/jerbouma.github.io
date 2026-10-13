---
permalink: /projects/financescenarios
software:
  name: "Finance Scenarios"
  repository: "https://github.com/JerBouma/FinanceScenarios"
  download: "https://pypi.org/project/financescenarios/"
title: Finance Scenarios
excerpt: An open-source economic scenario generator in Python. Correlated scenarios for rates, inflation, equities, currencies and more, fitted to live data, with portfolio outcomes and Solvency II capital on top.
description: "Open-source Python economic scenario generator: correlated rates, inflation and equity scenarios fitted to live data, portfolio outcomes and Solvency II."
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

The question about the future is rarely "what will happen?". It is "what could happen, and how bad does it get?". How much capital does a 1-in-200-year shock eat? Will a pension fund's assets keep up with its liabilities for thirty years? A single forecast cannot answer either, because the answer lives in the spread of outcomes. The tools that do answer it, economic scenario generators, have mostly been vendor products: you receive scenario files and a calibration report while the method stays with the vendor.

**Finance Scenarios makes those methods open.** It gives you:

- **Correlated scenarios fitted to live data.** Thousands of paths for interest rates, inflation, equities, unemployment, currencies, commodities and more, linked to each other the way they have moved historically, calibrated on data pulled through the [Finance Toolkit 🛠️](https://github.com/JerBouma/FinanceToolkit).
- **Published models, written out.** Each calibration method follows its paper, from [Wilkie (1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf) and [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf) to [Hibbert, Mowbray and Turnbull (2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf), [Cairns, Blake and Dowd (2006)](https://www.macs.hw.ac.uk/~andrewc/papers/jri2006e.pdf) and [Koijen, Nijman and Werker (2010)](https://doi.org/10.1093/rfs/hhp058), with a documentation page per factor and model.
- **Portfolio and balance-sheet outcomes.** Put an asset mix or a stream of liabilities through the scenarios and read the median, the bad year in twenty and the 1-in-200 event, including a Solvency II best estimate and SCR.

Assumptions, parameters, correlations and stress stories live in editable files, so you can change one and see what it does. The results still depend on the assumptions you chose, the data available and your own judgement.

<img src="/assets/images/projects/financescenarios/banner.webp" alt="Finance Scenarios" width="100%"/>

## Installation

Finance Scenarios requires Python 3.11 or higher.

```bash
pip install financescenarios -U
```

Market prices (equity indices, Treasury yields, gold, oil, fund dividends) come from FinancialModelingPrep, so you need an API key. The free plan allows 250 requests a day, 5 years of data and US-listed securities only.

[Obtain an API Key from FinancialModelingPrep](/fmp){: .btn .btn--warning .btn--large .align-center target="_blank"}

The link gives a **15% discount** on premium plans; it is an affiliate link and supports the project.

A free [FRED key](https://fred.stlouisfed.org/docs/api/api_key.html) is optional and adds US corporate bond spreads and commercial property prices. The default factor set anchors rates to EIOPA's risk-free curves, which needs Finance Toolkit 2.2.2 or newer. The [configuration documentation](/projects/financescenarios/docs/configuration#secrets) lists which key each factor uses.

## Functionality

Every table below is real output, cut to a few rows, and every chart is interactive, from runs calibrated on 2026-10-08 (stress, backtest and Solvency II on 2026-10-10). Live data moves, so another day gives slightly different numbers. The full [documentation](/projects/financescenarios/docs) explains each model and its assumptions.

A run combines a **settings** profile (how many scenarios, how far ahead, how much history to fit on) with a **factor set** (what gets simulated). The `default` set covers the US, the euro area and the UK, with rates anchored to EIOPA's forward curve. Other sets reproduce published models (`wilkie`, `ahlgrim`, `hibbert`, the NAIC-style `goes`), cover a single country (`us_only`), add listed stand-ins for private markets, or simulate everything (`broad`). The [coverage overview](/projects/financescenarios/docs/coverage) lists every factor and model.

### Simulating Correlated Scenarios {#simulating-scenarios}

Each variable is fitted to its own history, and the shocks are drawn jointly so the scenarios keep the historical correlations: a bad year for equities tends to come with rising unemployment and falling short rates.

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

Rates are annual rates and priced assets annualized returns, as decimals; `terminal_q05` and `terminal_q95` are the 1-in-20 outcomes at five years.

| factor                     | initial | terminal_mean | terminal_q05 | terminal_q95 |
|:---------------------------|--------:|--------------:|-------------:|-------------:|
| united_states_inflation    |  0.0340 |        0.0283 |      -0.0005 |       0.0570 |
| united_states_short_rate   |  0.0404 |        0.0441 |       0.0049 |       0.0858 |
| united_states_unemployment |  0.0410 |        0.0558 |       0.0216 |       0.0903 |
| us_broad                   |         |        0.0983 |      -0.0465 |       0.2321 |
| europe                     |         |        0.0768 |      -0.0918 |       0.2204 |
| gold                       |         |        0.0586 |      -0.0643 |       0.1959 |

{% include ft-chart.html id="simulation" src="/assets/data/financescenarios-charts.json" label="Simulated short rate, inflation and US equities" %}

The fan charts show the median and the bands holding half and nine in ten of the scenarios. The US short rate starts at 4.04% and averages 4.41% after five years, but 1 in 20 scenarios end below 0.49% and 1 in 20 above 8.58%. In money, 100 in US equities becomes 161 in the median scenario, below 79 in the worst 1 in 20 and above 284 in the best. **Find [the Notebook](/projects/financescenarios/getting-started) and [the simulation documentation](/projects/financescenarios/docs/simulation-engine).**

### Reading the Tails

The mean hides the asymmetry that matters for risk. The distribution of the five-year equity return shows it directly.

```python
result.summary_statistics("us_broad")
result.plot("us_broad", kind="distribution")
```

{% include ft-chart.html id="distribution" src="/assets/data/financescenarios-charts.json" label="Distribution of the five-year US equity return" %}

The median scenario returns 10.04% a year, above the 9.83% mean, because the left tail reaches further than the right: the worst 1 in 20 lose more than 4.65% a year, 14.7 points below the median, while the best 1 in 20 gain more than 23.21%, 13.2 points above it. **Find [the documentation](/projects/financescenarios/docs/units).**

### Building a Portfolio

An asset mix inherits the correlations of its holdings, so diversification shows up in the scenarios rather than being assumed. Here a 60/40 of US stocks and Treasuries, rebalanced once a year. Shipped mixes range from all-weather and permanent portfolios to a target-date glidepath and an endowment model.

```python
from financescenarios import Portfolio

portfolio = Portfolio.from_preset(result, preset="balanced_60_40")
values = portfolio.compute(initial_value=100_000, rebalance_every=12)
values.plot(levels=True)
```

{% include ft-chart.html id="portfolio" src="/assets/data/financescenarios-charts.json" label="Simulated value of a 60/40 portfolio" %}

The 60/40 earns 8.37% a year on average, between the stocks' 9.83% and the Treasuries' 5.46%. The median scenario turns 100,000 into 150,106 and the best 1 in 20 into more than 211,015, while the worst 1 in 20 end at 99,989: five years without a gain. Drawdowns, Value at Risk, saving and withdrawal plans, glidepaths and fees build on the same values. **Find [the Notebook](/projects/financescenarios/portfolio-notebook).**

### Applying Stress Regimes

A stress regime tells a story: it shifts an assumption before simulating (inflation pulled towards 9%), keeps only the scenarios consistent with the story (high rates and weak stocks), or both. Because the kept scenarios still come from the fitted model, the other variables move with the stress in a way the history supports. Twelve regimes ship, from an oil crisis and a credit crunch to a soft landing and a yield-curve inversion.

```python
from financescenarios import compare_runs

shocked = scenarios.simulate(regime="oil_crisis", n_simulations=2000)
compare_runs({"baseline": result, "oil_crisis": shocked})
```

| factor                   | baseline | oil_crisis |
|:-------------------------|---------:|-----------:|
| united_states_inflation  |   0.0283 |     0.0512 |
| united_states_short_rate |   0.0441 |     0.0649 |
| us_broad                 |   0.0983 |     0.0161 |
| europe                   |   0.0768 |     0.0180 |

{% include ft-chart.html id="regimes" src="/assets/data/financescenarios-charts.json" label="US inflation in the baseline and under three stress regimes" %}

In the oil crisis, US inflation ends at 5.12% instead of 2.83% and stocks return 1.61% a year instead of 9.83%. The regimes differ in timing as much as in level: the oil shock follows the baseline until its shock hits in January 2028 and then fades, while the oil crisis and climate collapse lift inflation from the first month. **Find [the Notebook](/projects/financescenarios/regimes-notebook) and [the regime documentation](/projects/financescenarios/docs/regimes).**

### Backtesting Against History

The same portfolio can run against what prices actually did, with its exposure measured against the [Fama-French factors](https://doi.org/10.1016/j.jfineco.2014.10.010) from [Ken French's data library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html).

```python
portfolio = Portfolio.backtest(scenarios, "balanced_60_40")
portfolio.factor_exposure()
portfolio.compute(initial_value=100_000, rebalance_every=12).plot(levels=True)
```

| portfolio      | Mkt-RF |     SMB |     HML |    RMW |     CMA |  alpha | r_squared | from       | to         |
|:---------------|-------:|--------:|--------:|-------:|--------:|-------:|----------:|:-----------|:-----------|
| 60/40 Balanced | 0.5399 | -0.0714 | -0.0420 | 0.1201 | -0.0168 | 0.0008 |    0.8654 | 2000-01-01 | 2026-10-01 |

{% include ft-chart.html id="backtest" src="/assets/data/financescenarios-charts.json" label="Historical value of a 60/40 portfolio since 2000" %}

A market loading of 0.54 with an R² of 0.87: the five factors explain most of the 60/40's monthly moves, and its equity half drives them. 100,000 invested in 2000 grew to 626,189 by October 2026, with the deepest fall, 28% from the peak, in February 2009. **Find [the Notebook](/projects/financescenarios/portfolio-analysis-notebook).**

### Valuing Liabilities and Capital Under Solvency II

[Solvency II](https://eur-lex.europa.eu/eli/dir/2009/138/oj) needs two views of the same economy. Liabilities are valued market-consistently, from a risk-neutral run in which discounted asset prices are martingales. Capital is the one-year 99.5% loss of own funds, read from the real-world run. Below, 10,000 a year for five years is backed by 60,000 in the 60/40.

```python
from financescenarios import Solvency

risk_neutral = scenarios.simulate(n_simulations=2000, measure="risk_neutral")
solvency = Solvency(real_world=result, risk_neutral=risk_neutral)

assets = Portfolio.from_preset(result, preset="balanced_60_40").compute(initial_value=60_000, rebalance_every=12)
solvency.report(cashflows=[10_000] * 5, assets=assets)
```

| item                | value                     | meaning                                                    |
|:--------------------|:--------------------------|:-----------------------------------------------------------|
| market consistent   | passed (largest gap 1.0%) | discounted back, us_broad stays within 2% of today's price |
| best estimate       | 43,444                    | what the payments are worth today                          |
| own funds           | 15,635                    | assets minus what is owed, today                           |
| SCR (1 in 200 year) | 12,453                    | the capital that survives a 1-in-200 bad year              |
| solvency ratio      | 1.26                      | own funds / SCR; above 1 means enough capital              |

{% include ft-chart.html id="solvency" src="/assets/data/financescenarios-charts.json" label="Distribution of own funds after one year" %}

The SCR of 12,453 is the distance from today's own funds to the 1-in-200 outcome at the left of the chart, where own funds fall to around 3,000. A ratio of 1.26 means the 60,000 covers both the payments and the required capital. **Find [the documentation](/projects/financescenarios/docs).**

### Validating the Output

A scenario set is only useful if it does what its models promise. Each run can be checked for calibration, finite paths and whether the simulated correlations match the fitted ones. Most variables can also be simulated with alternative published models, such as [Hull-White](https://doi.org/10.1093/rfs/3.4.573), [CIR](https://doi.org/10.2307/1911242) and [regime-switching](https://doi.org/10.1080/10920277.2001.10595984) equities, so model risk can be compared directly.

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

> **Do I need an economic scenario generator?**

When the answer you need is a range rather than one number: Solvency II capital and technical provisions, pension funding projections, asset-liability matching, portfolio tail risk, stress testing, or whether retirement withdrawals last.

> **How does this relate to the Finance Toolkit?**

The [Finance Toolkit](https://github.com/JerBouma/FinanceToolkit) looks backwards: it retrieves and calculates from historical data. Finance Scenarios looks forwards: it fits models to that history and simulates where things could go next.

> **How do I know whether the method I need is supported?**

The [coverage overview](/projects/financescenarios/docs/coverage) lists every factor, model, measure, portfolio analytic and Solvency II output as available, partial or unavailable.

> **Are my results reproducible?**

The random draws are fixed by a seed in the settings. The calibration follows live data, so save it and load it later to pin both.

> **How long does a run take?**

Calibration takes a couple of minutes for the default factor set on a cold cache and seconds once the data is cached. Simulating is fast.

> **Can I add my own regime, portfolio or model?**

A regime or a portfolio is a YAML file: copy a shipped one and edit it. A new model or factor plugs into the same calibration and correlation steps as the shipped ones; the [reference](/projects/financescenarios/docs/reference) shows what each one provides.

## Contact

If you have any questions about Finance Scenarios or would like to share what you have been working on, reach out via the [contact page](/contact).

{% include ft-charts-script.html %}
