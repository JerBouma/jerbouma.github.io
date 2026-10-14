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

The project requires Python 3.11 or higher. To install Finance Scenarios it simply requires the following:

```bash
pip install financescenarios -U
```

To be able to get the most out of it, you need an API key from FinancialModelingPrep. It is used for the price histories behind every ticker-priced factor: stock markets such as the S&P 500 (`SPY`), Europe (`VGK`) and Japan (`EWJ`), Treasury yields such as the 10-year (`^TNX`), commodities such as gold (`GC=F`) and Brent oil (`BZ=F`), and the dividends of those funds. Note that the Free plan is limited to 250 requests each day, 5 years of data and only companies listed on US exchanges.

[Obtain an API Key from FinancialModelingPrep](/fmp){: .btn .btn--warning .btn--large .align-center target="_blank"}

Through the link you are able to subscribe for the free plan and also premium plans at a **15% discount**. This is an affiliate link and thus supports the project at the same time.

Optionally, add a free [FRED key](https://fred.stlouisfed.org/docs/api/api_key.html) from the Federal Reserve Bank of St. Louis. It is used for US corporate bond spreads (the ICE BofA option-adjusted spreads behind `credit`) and US commercial property prices (`real_estate` with `source: commercial`). The [configuration documentation](/projects/financescenarios/docs/configuration#secrets) lists exactly which key each factor uses. The `default` factor set reads EIOPA's risk-free curves, which need Finance Toolkit 2.2.2 or newer (`pip install -U financetoolkit`).


## Functionality

Every table below is real output, cut to a few rows, and every chart is interactive, from one run calibrated on {{ site.data.financescenarios_run.date }}. Live data moves, so another day gives slightly different numbers. The full [documentation](/projects/financescenarios/docs) explains each model and its assumptions.

Every run combines two ready-made *profiles*: a **settings** profile, which says how the run goes (how many scenarios, how far ahead, how much history to learn from), and a **factor set**, which says what gets simulated (which interest rates, stock markets, currencies and so on). Optionally a **regime** adds a stress story, and a **portfolio** is an investment mix to read the scenarios through. `list_presets()` lists them all with what each is for; `kind=` narrows it to one kind:

```python
from financescenarios import list_presets

list_presets(kind="settings")  # or "factor-sets", "regimes", "portfolios"; leave it out for all 39
```

Open a kind below to see its options and the call it goes in.

<details class="ft-details" markdown="1">
<summary><i class="fas fa-sliders-h"></i> <b>Settings profiles</b> <span class="ft-details__meta">4</span></summary>

Passed as `Scenarios.from_profiles(settings="...")`.

| id           | description                                                                                                                                    |
|:-------------|:-----------------------------------------------------------------------------------------------------------------------------------------------|
| default      | 2,000 scenarios, one step a month, five years ahead, fitted on history since 2000.                                                               |
| goes         | Default, but fitted on history since 2019 only; pair it with the goes factor set to match the NAIC's scenario generator.                       |
| long_horizon | Default with 500 scenarios instead of 2,000, so multi-decade runs stay fast; pick the length with simulate(years=30).                            |
| wilkie       | Default, fitted on 1995 to 2007 only, as the wilkie set needs.                                                                                 |

</details>

<details class="ft-details" markdown="1">
<summary><i class="fas fa-layer-group"></i> <b>Factor sets</b> <span class="ft-details__meta">9</span></summary>

Passed as `Scenarios.from_profiles(factor_set="...")`.

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

<details class="ft-details" markdown="1">
<summary><i class="fas fa-bolt"></i> <b>Stress regimes</b> <span class="ft-details__meta">12</span></summary>

Passed as `Scenarios.from_profiles(regime="...")`, see [Applying Stress Regimes](#applying-stress-regimes).

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

<details class="ft-details" markdown="1">
<summary><i class="fas fa-chart-pie"></i> <b>Portfolios</b> <span class="ft-details__meta">14</span></summary>

Passed as `Portfolio.from_preset(result, preset="...")`, see [Building a Portfolio](#building-a-portfolio).

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
| united_states_inflation    |  0.0340 |        0.0283 |      -0.0005 |       0.0570 |
| united_states_short_rate   |  0.0406 |        0.0442 |       0.0050 |       0.0859 |
| united_states_unemployment |  0.0410 |        0.0558 |       0.0216 |       0.0903 |
| us_broad                   |         |        0.0983 |      -0.0466 |       0.2321 |
| europe                     |         |        0.0766 |      -0.0919 |       0.2202 |
| gold                       |         |        0.0594 |      -0.0636 |       0.1970 |

{% include ft-chart.html id="simulation" src="/assets/data/financescenarios-charts.json" label="Simulated short rate, inflation and US equities" %}

The fan charts show the median and the bands holding half and nine in ten of the scenarios. The US short rate starts at 4.06% and averages 4.42% after five years, but 1 in 20 scenarios end below 0.50% and 1 in 20 above 8.59%. In money, 100 in US equities becomes 161 in the median scenario, below 79 in the worst 1 in 20 and above 284 in the best. **Find [the Notebook](/projects/financescenarios/getting-started) and [the simulation documentation](/projects/financescenarios/docs/simulation-engine).**

### Reading the Tails

The mean hides the asymmetry that matters for risk. The distribution of the five-year equity return shows it directly.

```python
result.summary_statistics("us_broad")
result.plot("us_broad", kind="distribution")
```

{% include ft-chart.html id="distribution" src="/assets/data/financescenarios-charts.json" label="Distribution of the five-year US equity return" %}

The median scenario returns 10.04% a year, above the 9.83% mean, because the left tail reaches further than the right: the worst 1 in 20 lose more than 4.66% a year, 14.7 points below the median, while the best 1 in 20 gain more than 23.21%, 13.2 points above it. These equity returns are fitted on history; for planning work, a long-run [belief](/projects/financescenarios/docs/configuration#beliefs) about the equity return is advisable. **Find [the documentation](/projects/financescenarios/docs/units).**

### Building a Portfolio

An asset mix inherits the correlations of its holdings, so diversification shows up in the scenarios rather than being assumed. Here a 60/40 of US stocks and Treasuries, rebalanced once a year. Shipped mixes range from all-weather and permanent portfolios to a target-date glidepath and an endowment model.

```python
from financescenarios import Portfolio

portfolio = Portfolio.from_preset(result, preset="balanced_60_40")
values = portfolio.compute(initial_value=100_000, rebalance_every=12)
values.plot(levels=True)
```

{% include ft-chart.html id="portfolio" src="/assets/data/financescenarios-charts.json" label="Simulated value of a 60/40 portfolio" %}

The 60/40 earns 8.34% a year on average, less than the stocks' 9.83% but with a narrower range. The median scenario turns 100,000 into 149,916 and the best 1 in 20 into more than 210,755, while the worst 1 in 20 end below 99,843: five years without a gain. Drawdowns, Value at Risk, saving and withdrawal plans, glidepaths and fees build on the same values. **Find [the Notebook](/projects/financescenarios/portfolio-notebook).**

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
| united_states_short_rate |   0.0442 |     0.0648 |
| us_broad                 |   0.0983 |     0.0160 |
| europe                   |   0.0766 |     0.0181 |

{% include ft-chart.html id="regimes" src="/assets/data/financescenarios-charts.json" label="US inflation in the baseline and under three stress regimes" %}

In the oil crisis, US inflation ends at 5.12% instead of 2.83% and stocks return 1.60% a year instead of 9.83%. The regimes differ in timing as much as in level: the oil shock follows the baseline until its shock hits in January 2028 and then fades, while the oil crisis and climate collapse lift inflation from the first month. **Find [the Notebook](/projects/financescenarios/regimes-notebook) and [the regime documentation](/projects/financescenarios/docs/regimes).**

### Backtesting Against History

The same portfolio can run against what prices actually did, with its exposure measured against the [Fama-French factors](https://doi.org/10.1016/j.jfineco.2014.10.010) from [Ken French's data library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html).

```python
portfolio = Portfolio.backtest(scenarios, "balanced_60_40")
portfolio.factor_exposure()
portfolio.compute(initial_value=100_000, rebalance_every=12).plot(levels=True)
```

| portfolio      | Mkt-RF |     SMB |     HML |    RMW |     CMA |  alpha | r_squared | from       | to         |
|:---------------|-------:|--------:|--------:|-------:|--------:|-------:|----------:|:-----------|:-----------|
| 60/40 Balanced | 0.5398 | -0.0715 | -0.0416 | 0.1200 | -0.0172 | 0.0008 |    0.8653 | 2000-01-01 | 2026-10-01 |

{% include ft-chart.html id="backtest" src="/assets/data/financescenarios-charts.json" label="Historical value of a 60/40 portfolio since 2000" %}

A market loading of 0.54 with an R² of 0.87: the five factors explain most of the 60/40's monthly moves, and its equity half drives them. 100,000 invested in 2000 grew to 628,229 by October 2026, with the deepest fall, 28% from the peak, in February 2009. **Find [the Notebook](/projects/financescenarios/portfolio-analysis-notebook).**

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
| best estimate       | 43,434                    | what the payments are worth today                          |
| own funds           | 15,657                    | assets minus what is owed, today                           |
| SCR (1 in 200 year) | 12,484                    | the capital that survives a 1-in-200 bad year              |
| solvency ratio      | 1.25                      | own funds / SCR; above 1 means enough capital              |

{% include ft-chart.html id="solvency" src="/assets/data/financescenarios-charts.json" label="Distribution of own funds after one year" %}

The SCR of 12,484 is the distance from today's own funds to the 1-in-200 outcome at the left of the chart, where own funds fall to around 3,200. A ratio of 1.25 means the 60,000 covers both the payments and the required capital. **Find [the documentation](/projects/financescenarios/docs).**

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
