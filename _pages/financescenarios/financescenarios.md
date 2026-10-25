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

The goal is not to compete with a vendor model but to make the published methods accessible and reproducible in the open. Every calibration method is written out in plain Python and linked to the paper it came from, from [Wilkie (1986)](https://doi.org/10.1017/S0071368600009009) and [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf) to [Hibbert, Mowbray and Turnbull (2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf), [Cairns, Blake and Dowd (2006)](https://doi.org/10.1111/j.1539-6975.2006.00195.x) and [Koijen, Nijman and Werker (2010)](https://doi.org/10.1093/rfs/hhp058), with a documentation page per factor and per model. The assumptions, parameters, beliefs and correlations all live in files you can edit, so you can change one and run it again to see what it does. The results still depend on the assumptions you chose, on the data available, and on your own judgement.

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

list_presets(kind="settings")  # or "factor-sets", "regimes", "portfolios"; leave it out for all 66
```

Each kind's output is below; open one to see its options.

<details class="ft-details" markdown="1">
<summary><i class="fas fa-sliders-h"></i> <b>Settings profiles</b> <span class="ft-details__meta">7</span></summary>

| id           | description                                                                                                                                         |
|:-------------|:----------------------------------------------------------------------------------------------------------------------------------------------------|
| ahlgrim      | The run of Ahlgrim, D'Arcy and Gorvett (2005): from June 2004, 5,000 scenarios, 50 years, one step a month; pair it with the ahlgrim factor set.    |
| default      | 2,000 scenarios, one step a month, five years ahead, fitted on history since 2000.                                                                  |
| dnb          | Monthly steps over 100 years, DNB's horizon, with 2,000 scenarios; pair it with the dnb factor set.                                                 |
| goes         | Default, but fitted on history since 2019 only; pair it with the goes factor set to match the NAIC's scenario generator.                            |
| hibbert      | The run of Hibbert, Mowbray and Turnbull (2001): from March 2001, 1,000 scenarios, 30 years, one step a month; pair it with the hibbert factor set. |
| long_horizon | Default with 500 scenarios instead of 2,000, so multi-decade runs stay fast; pick the length with simulate(years=30).                               |
| wilkie       | The run of Wilkie (1986): 1,000 simulations of 100 years in yearly steps, dated 1986; pair it with the wilkie factor set.                           |

</details>

<details class="ft-details" markdown="1">
<summary><i class="fas fa-layer-group"></i> <b>Factor sets</b> <span class="ft-details__meta">7</span></summary>

| id      | description                                                                                                                                                                                                                                                                                                                       |
|:--------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ahlgrim | Reproduces Ahlgrim, D'Arcy and Gorvett (2005) from its June 2004 start with the published parameters and no data; pair it with the ahlgrim settings. For current data, build your own set with the same options.                                                                                                                  |
| broad   | Default plus Japan, Canada, Australia and India, US sectors and styles, more countries' equities, silver, copper, natural gas, five more currencies and SPY's dividend yield.                                                                                                                                                     |
| default | The US, the euro area and the UK, with global equities, gold, oil and the major currencies, each factor fitted to its long history and linked the way the economy is: a policy-rule short rate on the market's expected path, inflation and unemployment regimes, equities on a long-run premium; the recommended starting point. |
| dnb     | De Nederlandsche Bank's real-world scenarios rebuilt with its CP2022 model and its quarterly parameters: euro nominal and real rates, euro and Dutch inflation and world equity.                                                                                                                                                  |
| goes    | The United States as the NAIC's scenario generator (GOES) describes it: four Treasury yields on CIR set to its published bands, stocks on post-war history earning its long-run cash rate plus a premium, inflation, unemployment, commodities, currencies and SPY's dividend yield; pair it with the goes settings.              |
| hibbert | Reproduces Hibbert, Mowbray and Turnbull (2001), calibration A from its March 2001 start, with the published parameters and no data; pair it with the hibbert settings. For current data, build your own set with the same options.                                                                                               |
| wilkie  | Reproduces Wilkie (1986) on its Reduced Standard Basis from his neutral start, with the published parameters and no data; pair it with the wilkie settings. For current data, build your own set with the same options.                                                                                                           |

</details>

<details class="ft-details" markdown="1">
<summary><i class="fas fa-bolt"></i> <b>Stress regimes</b> <span class="ft-details__meta">39</span></summary>

| id                        | description                                                                                                                                                                                                                                  |
|:--------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ai_tech_boom              | Keeps the scenarios where US stocks gain the most over two years, the top 9% where 2023-24's 53% rise sits.                                                                                                                                  |
| asian_crisis_1997         | Emerging-market stocks fall 56% over five quarters and the yen weakens 23% against the dollar, as in 1997-98. Needs the default or broad set.                                                                                                |
| black_monday_1987         | US stocks lose a third within a quarter and are back by month 23, as in the 1987 crash, other markets follow through their correlations, short rates ease by three quarters of a point and unemployment keeps falling.                       |
| boe_stress_2025           | The Bank of England's 2025 stress test: UK inflation to 10%, short rates to 8% in the UK and the US, ten-year yields to 6.4%, US stocks down 57% and unemployment peaking in year three. Needs the default or broad set.                     |
| bond_massacre_1994        | Short rates rise 2.8 points and long yields 2.6 points within a year, as in the 1994 bond market rout.                                                                                                                                       |
| commodity_supercycle      | Oil rises sevenfold over six and a half years, year after year, as Brent did from 2002 to its 2008 record, then falls back.                                                                                                                  |
| covid_crash_2020          | Stocks everywhere fall a fifth to two fifths in a month and recover by month six, unemployment jumps to 14.8%, rates go to zero for two years and oil collapses, as in 2020.                                                                 |
| credit_crunch             | Bank stocks collapse and the market follows: a harsher bear market for financials, then their worst scenarios. Needs the financials equity (broad set).                                                                                      |
| currency_crisis           | The Indian rupee devalues sharply against the dollar, about 17% a year for two and a third years, as in 2011-13. Needs the broad set.                                                                                                        |
| dot_com_bust              | US stocks lose half over two and a half years, Japanese stocks 56% and emerging markets 47%, short rates fall to 1.6% and unemployment rises to 6.3%, as in 2000-2003.                                                                       |
| early_1990s_recession     | Oil spikes, US stocks fall 20% within a quarter, unemployment rises to 7.8% over two years and short rates are cut to 2.9%.                                                                                                                  |
| energy_war_2022           | Oil jumps a quarter, euro-area inflation climbs to 9% and falls back, euro-area short rates rise to 4%, European stocks fall 17% and the euro 15%, as after February 2022. Needs the default or broad set.                                   |
| esrb_adverse_2025         | The ESRB's adverse scenario for the 2025 EU-wide bank stress test: stocks down by half, unemployment rising for three years in Europe and the UK, and to 10% by year two in the US. Needs the default or broad set.                          |
| euro_debt_crisis_2011     | European stocks fall 35%, the euro weakens 19%, Bund yields drop two points and euro-area unemployment climbs, as in 2011-12. Needs the default or broad set.                                                                                |
| fed_severely_adverse_2026 | The Federal Reserve's 2026 severely adverse stress test: unemployment to 10%, US stocks down almost 60%, house prices down 30%, short rates at 0.1%.                                                                                         |
| financial_crisis          | Stocks everywhere lose more than half in seventeen months, unemployment doubles to 10%, short rates go to zero for seven years and house prices fall 7% a year, as in 2007-09.                                                               |
| gold_rally                | Gold nearly triples over two and a quarter years, as in 2023-26.                                                                                                                                                                             |
| goldilocks_1990s          | Inflation near 2.4% and unemployment near 4% for the whole run, with the strongest fifth of US stock outcomes, as in the late 1990s.                                                                                                         |
| housing_boom              | US house prices grow about 11% a year for two years, then cool, as in 2004-06.                                                                                                                                                               |
| inflation_shock_2022      | Inflation climbs to 9% and falls back to 3% within a year, short rates rise to the 5.3% peak of 2023 and long yields to 4.8%, unemployment stays near 3.7%, US stocks rise 30% and then fall 25%, and the dollar strengthens, as in 2021-23. |
| japan_lost_decade         | Mild deflation, zero short rates, long yields near 1.4% and house prices falling 3% a year for fourteen years, and US stocks losing 63% over two and a half years, as in Japan after 1990.                                                   |
| ltcm_1998                 | US stocks fall 19% and recover within four months, Treasury yields drop about 1.4 points and the yen jumps 24%, as in 1998.                                                                                                                  |
| mild_recession            | Unemployment rises to 6.9% over 15 months, the policy rule cuts short rates as it climbs and US stocks fall 14% over a year: the mildest quarter of post-war recessions.                                                                     |
| oil_collapse_2014         | Oil falls about 72% over a year and a half and US inflation dips below zero before recovering, as in 2014-16.                                                                                                                                |
| oil_crisis                | US inflation climbs to 12% within a year and eases to 5.5% by year three, short rates rise to 9% and fall back, unemployment rises to 9% and stocks fall 43%, as after the 1973 oil embargo.                                                 |
| oil_shock                 | A one-off rise of about three points in US inflation over the half year to year 2, after which everything behaves normally again.                                                                                                            |
| persistent_inflation      | US inflation climbs towards 6.6% and stays high instead of returning to target, as over 1965-1982.                                                                                                                                           |
| rate_cut_cycle            | Short rates are cut 5 points over two and a half years, the median of the Fed's six easing cycles from 1984 to 2020, then follow the policy rule again.                                                                                      |
| real_estate_crash         | House-price growth falls to -8% within a year and recovers to zero over the four years after, as US house prices did after 2008.                                                                                                             |
| september_11              | US stocks drop 12% and recover within a month, short rates fall 1.5 points and oil 27%, as after 11 September 2001.                                                                                                                          |
| soft_landing              | No recession after the Fed's tightening: unemployment holds at today's level for three years and short rates are cut 0.7 points within a year, as after the soft landings of 1966, 1984 and 1995, then follow the policy rule again; inflation eases as in the baseline. |
| stagflation_1970s         | Inflation climbs towards 9% and unemployment towards 7.3% while US stocks fall 43% over two years, as in 1973-1982.                                                                                                                          |
| strong_dollar_2014        | The dollar strengthens fast: the euro falls 24%, the pound 15% and the yen 19% against it within a year, as in 2014-15.                                                                                                                      |
| taper_tantrum_2013        | Long US yields rise 1.3 points in four months while emerging-market stocks fall 18%, as in 2013. Needs the default or broad set.                                                                                                             |
| tech_selloff              | Tech stocks fall about a fifth in a year and stay down while the wider market holds up, as in 2022. Needs the broad set.                                                                                                                     |
| uk_gilt_crisis_2022       | UK long yields jump 1.8 points within two months and the pound falls 13% against the dollar before partly recovering, as in the 2022 gilt crisis. Needs the default or broad set.                                                            |
| volcker_shock             | Short rates rise about seven points from today's level, to near 11%, month by month as the 3-month bill did in 1979-81, while inflation rises and falls back, long yields rise about five points in two years, unemployment climbs to 10.8%, US stocks fall 27%, gold spikes and falls back and the dollar strengthens, as in 1979-1982. |
| weak_dollar_2002          | The dollar weakens for three years: the euro gains 58%, the pound 36% and the yen 31% against it, as in 2002-04.                                                                                                                             |
| yield_curve_inversion     | The yield curve inverts within six months, short yields about one and a half points above the ten-year, then slowly rights itself.                                                                                                           |

</details>

<details class="ft-details" markdown="1">
<summary><i class="fas fa-chart-pie"></i> <b>Portfolios</b> <span class="ft-details__meta">13</span></summary>

| id                    | description                                                                                                                                  |
|:----------------------|:---------------------------------------------------------------------------------------------------------------------------------------------|
| all_weather           | Ray Dalio's mix: 30% US stocks, 55% Treasuries for his 40% long and 15% intermediate bonds, 15% gold for his 7.5% gold and 7.5% commodities. |
| balanced_60_40        | The textbook mix: 60% US stocks and 40% US Treasury bonds.                                                                                   |
| barbell               | Nassim Taleb's barbell: 85% Treasury bills, 15% small-cap and growth stocks, nothing in between. Needs the broad set.                        |
| bogleheads_three_fund | The Bogleheads' three funds: 40% US stocks, 20% international stocks and 40% US Treasury bonds. Needs the default or broad set.              |
| buffett_90_10         | Warren Buffett's advice for his estate: 90% in an S&P 500 fund and 10% in Treasury bills.                                                    |
| conservative_income   | Mostly US, euro-area and UK government bonds, with 10% in US stocks for growth. Needs the default or broad set.                              |
| global_60_40          | The 60/40 spread across countries: US, European and emerging-market stocks; US, euro-area and UK bonds. Needs the default or broad set.      |
| global_equity_growth  | All stocks, spread across the US, Europe, Japan, emerging markets and China, tilted to growth. Needs the broad set.                          |
| golden_butterfly      | Equal fifths of stocks, small-cap and value stocks, long bonds, Treasury bills and gold. Needs the broad set.                                |
| permanent_portfolio   | Harry Browne's four quarters: US stocks, long US Treasuries, Treasury bills and gold.                                                        |
| small_cap_value_tilt  | 80% in small-cap and value stocks, the Fama-French premia, with 20% US Treasury bonds. Needs the broad set.                                  |
| target_date_glidepath | A target-date fund on Vanguard's glide path: 90% stocks until 25 years out, 50% at the target date and 30% seven years after.                |
| us_equity_sectors     | All stocks, split evenly across nine US sectors. Needs the broad set.                                                                        |

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

For example, 6 of the 27 variables are shown below. Rates are yearly rates and anything with a price a yearly return, written as decimals (0.0455 is 4.55%).

| factor                     | category       | initial | terminal_mean | terminal_q05 | terminal_q95 |
|:---------------------------|:---------------|--------:|--------------:|-------------:|-------------:|
| united_states_inflation    | inflation      |  0.0374 |        0.0234 |      -0.0064 |       0.0770 |
| united_states_short_rate   | interest_rates |  0.0403 |        0.0455 |       0.0000 |       0.1091 |
| united_states_unemployment | unemployment   |  0.0420 |        0.0554 |       0.0338 |       0.0895 |
| us_broad                   | equities       |         |        0.0844 |      -0.0572 |       0.2076 |
| europe                     | equities       |         |        0.0928 |      -0.0757 |       0.2482 |
| gold                       | commodities    |         |        0.0307 |      -0.1002 |       0.1722 |

The chart below follows the US short rate, US inflation and US equities through all 2,000 scenarios. **Find [the Scenarios documentation](/projects/financescenarios/docs) and [the simulation engine](/projects/financescenarios/docs/simulation-engine).**

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
| 2030-11-01 | 0.0455 | 0.0339 | 0.0000 | 0.0201 | 0.0433 | 0.0644 | 0.1090 |
| 2030-12-02 | 0.0455 | 0.0342 | 0.0000 | 0.0195 | 0.0433 | 0.0645 | 0.1082 |
| 2031-01-01 | 0.0455 | 0.0344 | 0.0000 | 0.0195 | 0.0436 | 0.0655 | 0.1091 |

The chart below shows how widely the five-year US equity return spreads across the scenarios. **Find [the Scenarios documentation](/projects/financescenarios/docs#reading-the-distribution) and [how results read](/projects/financescenarios/docs/units).**

```python
result.plot("us_broad", kind="distribution")
```

Which shows where the five-year return lands across all 2,000 scenarios:

{% include ft-chart.html id="distribution" src="/assets/data/financescenarios-charts.json" label="Distribution of the five-year US equity return" %}

### Building a Portfolio

Put an investment mix through the same scenarios, here the 60/40 (60% US stocks, 40% US government bonds) from the 13 ready-made mixes, rebalanced once a year.

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
| portfolio                     | portfolio |         |        0.0721 |      -0.0098 |       0.1461 |
| us_broad_value                | holding   |         |        0.0844 |      -0.0572 |       0.2076 |
| united_states_long_rate_value | holding   |         |        0.0470 |       0.0090 |       0.0784 |

The 60/40 earns 7.21% a year on average, between the stocks' 8.44% and the Treasury fund's 4.70%, so 100,000 grows to 144,358 on average. The same portfolio also reports its drawdowns and Value at Risk, and covers saving and withdrawal plans, glidepaths and fees. The chart below shows the portfolio's value in money across the scenarios. **Find [the Portfolio documentation](/projects/financescenarios/docs/portfolio).**

```python
values.plot(levels=True)
```

Which shows the portfolio's value in money, with the same bands:

{% include ft-chart.html id="portfolio" src="/assets/data/financescenarios-charts.json" label="Simulated value of a 60/40 portfolio" %}

### Applying Stress Regimes

Run the same variables through one of 39 named stress stories, such as an oil crisis. A regime changes an assumption before simulating, keeps only the scenarios that fit the story, or both.

```python
from financescenarios import compare_runs

shocked = scenarios.simulate(regime="oil_crisis", n_simulations=2000, seed=42)

compare_runs({"baseline": result, "oil_crisis": shocked})
```

Oil Crisis replays 1973-74 from today: the middle of US inflation climbs to 12% within a year and eases to 5.5% by year three, the short rate to the 3-month bill's 9% and back, unemployment to 9%, and US stocks fall 43% before recovering, with every scenario keeping its own distance from that path and the world's other stock markets following through their correlations. After five years the short rate averages 4.24% instead of 4.55% and US stocks earn 0.86% a year instead of 8.44%. For example, four of the variables are shown below.

| factor                   | baseline | oil_crisis |
|:-------------------------|---------:|-----------:|
| united_states_inflation  |   0.0234 |     0.0483 |
| united_states_short_rate |   0.0455 |     0.0424 |
| united_states_long_rate  |   0.0584 |     0.0623 |
| us_broad                 |   0.0844 |     0.0086 |

The chart below sets US inflation in the baseline next to the Oil Shock, Oil Crisis and 2022 Inflation and Rate Hikes regimes, 2,000 scenarios each. **Find [the Regimes documentation](/projects/financescenarios/docs/regimes).**

```python
from financescenarios import plot_runs

runs = {"baseline": result}
for regime in ("oil_shock", "oil_crisis", "inflation_shock_2022"):
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
| 60/40 Balanced      | 0.5369 | -0.0687 | -0.0447 | 0.1215 | -0.0116 | 0.0007 |    0.8615 |          312 | 2000-08-01 | 2026-10-01 |
| All Weather         | 0.2039 | -0.0620 | -0.1435 | 0.2162 |  0.0335 | 0.0029 |    0.1318 |          312 | 2000-08-01 | 2026-10-01 |
| Permanent Portfolio | 0.2173 | -0.0615 | -0.1418 | 0.2017 |  0.0473 | 0.0033 |    0.1240 |          312 | 2000-08-01 | 2026-10-01 |

The chart below shows what each mix actually did since August 2000, rebalanced once a year: 100,000 grew to 545,686 in the 60/40, 542,849 in All Weather and 551,770 in the Permanent Portfolio by October 2026, with the 60/40 carrying more than twice the stock market risk of the other two. **Find [the Portfolio documentation](/projects/financescenarios/docs/portfolio/backtests#backtesting-against-history).**

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
| market consistent   | passed (largest gap 1.2%) | discounted back, us_broad stays within 2% of today's price |
| best estimate       | 43,514                    | what the payments are worth today                          |
| own funds           | 15,624                    | assets minus what is owed, today                           |
| SCR (1 in 200 year) | 13,066                    | the capital that survives a 1-in-200 bad year              |
| solvency ratio      | 1.20                      | own funds / SCR; above 1 means enough capital              |

The chart below shows where own funds could be after one year, with today's level and the 1-in-200 outcome marked. **Find [the Solvency documentation](/projects/financescenarios/docs/solvency).**

```python
solvency.plot(cashflows=[10_000] * 5, assets=assets)
```

Which marks today's own funds and the 1-in-200 outcome:

{% include ft-chart.html id="solvency" src="/assets/data/financescenarios-charts.json" label="Distribution of own funds after one year" %}

### Validating the Output

Check a run against what its own models promise. Most variables can also be simulated with other published models through a single setting, such as [Hull-White](https://doi.org/10.1093/rfs/3.4.573), [CIR](https://doi.org/10.2307/1911242) and [regime-switching](https://doi.org/10.1080/10920277.2001.10595984) equities, and the published Wilkie, Ahlgrim, Hibbert and GOES specifications ship as whole factor sets, as does De Nederlandsche Bank's CP2022 model with the parameters DNB publishes every quarter. The first three reproduce their papers as published, from the papers' own start dates and with no data, matching the tables those papers report.

```python
scenarios.validate(result)
```

On this run five of the six checks pass and one warns, on the volatilities. For example, three of the checks are shown below.

| check                                  | status | detail                                                                                                                                                                                                                                                                                                                      |
|:---------------------------------------|:-------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Every factor calibrated                | pass   | every factor calibrated                                                                                                                                                                                                                                                                                                     |
| Simulation reproduces the correlations | pass   | largest gap 0.109 (eurozone_inflation/united_kingdom_inflation); 120,000 moves per factor, so gaps up to 0.01 more are sampling noise; pairs with a linked factor, not graded: largest gap 0.543 (united_states_short_rate/united_states_long_rate); rate_level and rate_slope read off the short and long rate, not graded |
| Every path is finite                   | pass   | 27 factors, all finite                                                                                                                                                                                                                                                                                                      |

Whether the variables also move together the way the economy does, measured the same way on decades of history and on every scenario, is a check of its own:

```python
scenarios.check_relationships(result)
```

On this five-year run 18 of the 26 relationships pass, 8 warn and none fails. For example, three of them are shown below.

| relationship                        | region        | status | history | simulated_median |
|:------------------------------------|:--------------|:-------|--------:|-----------------:|
| Policy rate reacts to inflation     | United States | warn   |  0.4522 |           0.1813 |
| Phillips curve                      | United States | pass   | -0.5923 |          -0.3976 |
| Long rate moves with the short rate | United States | pass   |  0.3303 |           0.5112 |

**Find [the Validation documentation](/projects/financescenarios/docs/validation) and [every model and its status](/projects/financescenarios/docs/coverage).**

### Starting Your Own Project

Everything above runs on the ready-made profiles as they ship. To change an assumption, add a market of your own or keep your results, copy the profiles into a folder of your own:

```python
from financescenarios import read_run, scaffold_project

scaffold_project("my-project")              # editable settings, factor sets, regimes, portfolios and a .env
path = scenarios.save(result, "results/")   # the run, its settings and its calibration, in its own folder
result = read_run(path)
```

Run Python from inside `my-project` and every run reads its YAML files instead of the bundled ones, and the keys pasted into its .env file, so the API key can be left out. A saved run reads back without downloading or simulating anything again. **Find [the Configuration documentation](/projects/financescenarios/docs/configuration).**

# MCP Server

The Finance Scenarios MCP Server lets any AI assistant that supports the [Model Context Protocol](https://modelcontextprotocol.io) (MCP) run the scenarios for you. Ask in plain English what could happen to stocks if inflation reached 8%, or how a single world equity fund could develop over ten years, and the assistant answers with the range of outcomes from this month's calibration, next to the historical episodes that tell the same story. No API key is needed. Find the tools, example questions and how to host the server yourself in the [MCP Server Documentation](/projects/financescenarios/mcp).

### Local installation

Add the following to your client's MCP config file (e.g. `claude_desktop_config.json` or `.cursor/mcp.json`; VS Code's `.vscode/mcp.json` uses `servers` instead of `mcpServers`):

```json
{
  "mcpServers": {
    "finance-scenarios": {
      "command": "uvx",
      "args": ["--from", "financescenarios[mcp]", "financescenarios-mcp"]
    }
  }
}
```

The very first question calibrates the data, which takes about a minute; after that the server answers from it and recalibrates once a month in the background. To have it ready beforehand, run `uvx --from "financescenarios[mcp]" financescenarios-mcp-warm`.

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

  Your own views on long-run levels, such as a central bank's inflation target or an equity risk premium, go in as beliefs that override the fitted values. A new model or factor plugs into the same calibration and correlation steps as the shipped ones, so it is linked to everything else automatically; the [documentation](/projects/financescenarios/docs) shows what each one provides.

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
