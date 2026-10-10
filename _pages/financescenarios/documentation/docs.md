---
title: Documentation
seo_title: Finance Scenarios Documentation
excerpt: "The documentation of Finance Scenarios, an open-source economic scenario generator that simulates thousands of possible scenarios for interest rates, inflation, stock markets, currencies and other economic variables, linked to each other the way they have been historically."
description: "Documentation for Finance Scenarios, an open-source Python economic scenario generator: configuration, simulation engine, units, regimes, plotting and validation."
author_profile: false
permalink: /projects/financescenarios/docs
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Finance Scenarios is an economic scenario generator (ESG): it simulates thousands of possible scenarios for interest rates, inflation, stock markets, currencies and other economic variables, linked to each other the way they have been historically.

Instead of one forecast you get a range of plausible scenarios, so you can see the typical outcome, the bad years and the extreme cases. That is what risk analysis, actuarial reserving, pension and retirement planning, and stress testing need.

Installing the package and a first run are covered on the [Finance Scenarios page](/projects/financescenarios#installation), and the [example notebooks](/projects/financescenarios#notebooks) show each part with real output.

## Where the documentation lives

The documentation is split the same way as the [Finance Toolkit](https://github.com/JerBouma/FinanceToolkit)'s:

- **Each component documents itself.** What a factor or module models, which papers it follows, its options, its data source and limits, its configuration keys, and a worked example with real output are all in the class and method docstrings, readable with `help(...)` in Python and rendered as the reference pages on the website.
- **These pages cover the infrastructure:** how a run is put together, how to configure it, the units everything is reported in, and how the output is checked.

| Component | Class (`help(...)`) | Default | Shape |
|:----------|:--------------------|:--------|:------|
| Interest rates | `InterestRates` (`factors/interest_rates`) | On | One per country or region |
| Inflation | `Inflation` (`factors/inflation`) | On | One per country or region |
| Equities | `Equities` (`factors/equities`) | On | One per index, sector, region or style |
| Unemployment | `Unemployment` (`factors/unemployment`) | On | One per country or region, paired with an inflation entry |
| Yield curve | `TermStructure` (`factors/term_structure`) | On in `default.yaml` and `broad.yaml` | Nelson-Siegel level, slope and curvature |
| Forward curve (HJM) | `Hjm` (`factors/hjm`) | Opt-in | Two-factor Gaussian forward curve |
| Real estate | `RealEstate` (`factors/real_estate`) | Opt-in | House-price growth |
| Credit spreads | `Credit` (`factors/credit`) | Opt-in | One per US maturity or rating bucket (ICE BofA), Moody's Aaa/Baa from 1953, German or Australian corporate spreads, or the ECB's euro-area cost of borrowing |
| Rating migration | `CreditMigration` (`factors/credit_migration`) | Opt-in | A credit cycle driving rating moves and defaults; `rating_migration` for a portfolio |
| Credit curve | `CreditTermStructure` (`factors/credit_term_structure`) | Opt-in | Nelson-Siegel curve from the Treasury HQM spread curve (or a bond panel) |
| Leading indicator | `LeadingIndicator` (`factors/leading_indicator`) | Opt-in | OECD composite leading indicator |
| FX | `FX` (`factors/fx`) | Opt-in | One per currency against the US dollar |
| Commodities | `Commodities` (`factors/commodities`) | Opt-in | One per commodity future |
| Dividend yield and growth | `DividendYield`, `DividendGrowth` (`factors/dividend_*`) | Opt-in | One per ticker |
| Mortality | `Mortality` (`factors/mortality`) | Opt-in | Cairns-Blake-Dowd two-factor model; Eurostat life tables or a supplied table |
| KNW model family | `Knw`, `KnwSv`, `KnwSvQ` (`models/`) | Per entry (`method:`) | Interest rate and inflation fitted jointly |
| Correlations | `Dependence` (`dependence/`) | Always | The correlation matrix that links every factor |
| Portfolios | `Portfolio` (`portfolio/`) | On demand | Allocations, cashflows, risk metrics, backtests |
| Currency reporting | `Reporting` (`reporting/`) | On demand | Converts prices into one reporting currency |
| Solvency II | `Solvency` (`solvency/`) | On demand | `Solvency(real_world, risk_neutral).report(cashflows, assets)` in one table; also the martingale test, EIOPA risk-free curves, best estimate, standard-formula interest rate and equity risk, one-year SCR and scenario files on their own |
| Climate scenarios | `climate` section, `climate_controller` | Opt-in | NGFS pathways laid over a run, plus the carbon price |
| Official stress tests | `stress_test_regime` (`stress_tests/`) | On demand | Federal Reserve and ESRB scenarios as regimes |
| Calibration releases | `publish_calibration`, `load_release` (`release/`) | On demand | Versioned calibrations with a validation report; published yearly as GitHub releases |
| Long history | `history_source` on equities, rates and inflation (`long_history/`) | Per entry | Dynamics fitted on Shiller (1871), the Bank of England's millennium data (1209/1694) or JST (1870) |

The four default factors are not simulated in isolation. Following [Wilkie (1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf) and [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf), inflation feeds interest rates and unemployment, and both feed equity returns; every other factor is linked through the estimated correlation matrix (`Dependence`).

## How a run is put together

| Page | What it covers |
|:-----|:---------------|
| [architecture](/projects/financescenarios/docs/architecture) | The module layout (`_model`, `_controller`, `_view`) and the data flow from configuration to results. |
| [configuration](/projects/financescenarios/docs/configuration) | Settings and factor-set profiles, every top-level field, multi-instance factors, beliefs and shocks, the published frameworks (Wilkie, Ahlgrim, Hibbert, KNW), real-world and risk-neutral measures, and API keys. |
| [simulation-engine](/projects/financescenarios/docs/simulation-engine) | How the correlated shocks are drawn, how each factor steps forward, and the `ScenarioSet` result and its methods. |
| [units](/projects/financescenarios/docs/units) | The one unit everything is reported in: rates as annualized decimals, prices as annualized returns since start. |
| [regimes](/projects/financescenarios/docs/regimes) | Named stress narratives: belief overrides, post-simulation filters, or both. |
| [plotting](/projects/financescenarios/docs/plotting) | The `.plot()` on every result and the chart functions behind it. |
| [validation-and-testing](/projects/financescenarios/docs/validation) | How the output is checked: analytical tests, external benchmarks (NAIC GOES, a bond panel, option-implied densities) and the test suite. |
| [coverage](/projects/financescenarios/docs/coverage) | What this project can and can't do, and why: every factor, every calibration method, every measure and every known gap, in one place. |

## Data, measures and currency

Finance Scenarios fetches no data itself: all history comes from a [Finance Toolkit](https://github.com/JerBouma/FinanceToolkit) `Toolkit`, which `build_toolkit()` constructs from the configuration, reading the optional FinancialModelingPrep and FRED keys from the environment or a local `.env` (see the Secrets section of [configuration](/projects/financescenarios/docs/configuration)). Most factors calibrate on free OECD and Yahoo Finance data without any key.

Every factor calibrates under the **real-world** measure by default, a fit to how it has actually behaved. Equities, interest rates, FX, inflation, the KNW pair and two-factor commodities can each opt into a **risk-neutral** calibration that reproduces today's market prices instead; [configuration](/projects/financescenarios/docs/configuration)'s Real-world and risk-neutral measures section lists which, and why the others cannot. [Merton (1973)](https://doi.org/10.2307/3003143) gives the classic no-arbitrage argument and [the SOA (2022)](https://www.soa.org/resources/research-reports/2022/understanding-the-connection/) a practical treatment of when each measure is the right tool.

Each factor is simulated in its own currency. `FX`'s `drift_mode: "irp"` ties an exchange rate's drift to two simulated interest rates and `drift_mode: "random_walk"` drops the historical trend so the median rate stays at today's level, and `Reporting` converts prices into one reporting currency after the simulation, without touching calibration or correlations.

## Quick example

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(settings="default", factor_set="us_only")   # settings/default.yaml + factor-sets/us_only.yaml
result = scenarios.simulate()

result.describe()                                   # every factor in one unit, see units
result.plot("us_broad")                             # a quick chart, see plotting
help(type(scenarios.equities))                      # the Equities documentation itself

scenarios.validate(result)                          # pass/warn/fail checks on the run, see validation-and-testing
path = scenarios.save(result, "results/")           # the run, its config and calibration, in its own folder
history = scenarios.history(portfolio="balanced_60_40")       # what actually happened, for a backtest
```

`scenarios.save()` returns the run's folder, which `read_run(path)` reads back; `scenarios.history()` returns the realized history as a one-path run, so `Portfolio` and every chart work on it the same way (see the [README](/projects/financescenarios#backtesting-against-history)'s backtesting section). `from_profiles()` also takes `regime="oil_crisis"` for a named stress narrative (see [regimes](/projects/financescenarios/docs/regimes)); when a named profile directory does not exist locally, the copy bundled with the package is used, so this works from a plain install. `Scenarios.calibrate(config)` with `CalibrationResult.save()` and `.load()` replays a calibration without any data access, see [simulation-engine](/projects/financescenarios/docs/simulation-engine).
