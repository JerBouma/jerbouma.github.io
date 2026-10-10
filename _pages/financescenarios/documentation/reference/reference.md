---
title: "Reference"
seo_title: "Reference – Finance Scenarios"
excerpt: "Reference for the Finance Scenarios Python package, generated from its docstrings: every public class, method and function."
description: "Reference for the Finance Scenarios Python package, generated from its docstrings: every public class, method and function."
author_profile: false
permalink: /projects/financescenarios/docs/reference
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

The reference pages are generated from the docstrings in the Finance Scenarios package, so they say exactly what `help(...)` says in Python. Each page covers one class or area: its constructor, then every public method and property with its signature, arguments, return value, errors and, where the docstring has one, a worked example with real output.

How a run is put together, the configuration keys and the units every result is reported in are on the [documentation](/projects/financescenarios/docs) pages.

## Core

| Page | What it covers |
|:-----|:---------------|
| [Scenarios](/projects/financescenarios/docs/reference/scenarios) | Calibrate every configured factor and simulate correlated scenarios; also the saved calibration and the Toolkit builder. |
| [ScenarioSet](/projects/financescenarios/docs/reference/scenario-set) | The result of a run: describe, filter, plot, diagnose and compare simulated scenarios. |
| [Portfolio](/projects/financescenarios/docs/reference/portfolio) | Read a finished run through an investment portfolio: allocations, cashflows, glidepaths, risk metrics and factor exposure. |
| [Solvency](/projects/financescenarios/docs/reference/solvency) | Solvency II on a real-world and a risk-neutral run: the martingale test, best estimate, SCR and EIOPA curves. |
| [Configuration and Presets](/projects/financescenarios/docs/reference/configuration) | Load settings, factor sets and presets, list every named preset and scaffold a project. |
| [Regimes and Stress Tests](/projects/financescenarios/docs/reference/regimes) | Named stress narratives and the official Federal Reserve and ESRB stress scenarios as regimes. |
| [Run Files and Releases](/projects/financescenarios/docs/reference/runs-and-releases) | Write and read saved runs, and publish, load and simulate versioned calibration releases. |
| [History and Metrics](/projects/financescenarios/docs/reference/history-and-metrics) | Fetch the realized history behind a run, turn it into a backtest and compute factor and price metrics. |
| [Charts](/projects/financescenarios/docs/reference/charts) | The chart functions behind every `.plot()`: fan charts, paths, terminal distributions, runs and portfolios. |
| [Dependence](/projects/financescenarios/docs/reference/dependence) | The correlation matrix that links every factor: estimation, shrinkage and repair. |
| [Reporting](/projects/financescenarios/docs/reference/reporting) | Convert simulated prices into one reporting currency after the simulation. |

## Factors

| Page | What it covers |
|:-----|:---------------|
| [InterestRates](/projects/financescenarios/docs/reference/interest-rates) | Short and long interest rates, one per country or region. |
| [Inflation](/projects/financescenarios/docs/reference/inflation) | Consumer price inflation, one per country or region. |
| [Equities](/projects/financescenarios/docs/reference/equities) | Equity indices, sectors, regions and styles with regime switching. |
| [Unemployment](/projects/financescenarios/docs/reference/unemployment) | Unemployment rates, each paired with an inflation entry. |
| [TermStructure](/projects/financescenarios/docs/reference/term-structure) | The yield curve as Nelson-Siegel level, slope and curvature. |
| [Hjm](/projects/financescenarios/docs/reference/hjm) | A two-factor Gaussian HJM forward curve. |
| [RealEstate](/projects/financescenarios/docs/reference/real-estate) | House-price and commercial property growth. |
| [Credit](/projects/financescenarios/docs/reference/credit) | Credit spreads by maturity, rating bucket or country. |
| [CreditMigration](/projects/financescenarios/docs/reference/credit-migration) | A credit cycle driving rating migrations and defaults. |
| [CreditTermStructure](/projects/financescenarios/docs/reference/credit-term-structure) | A Nelson-Siegel credit spread curve. |
| [LeadingIndicator](/projects/financescenarios/docs/reference/leading-indicator) | The OECD composite leading indicator. |
| [FX](/projects/financescenarios/docs/reference/fx) | Exchange rates, one per currency against the US dollar. |
| [Commodities](/projects/financescenarios/docs/reference/commodities) | Commodity futures, one per commodity. |
| [DividendYield](/projects/financescenarios/docs/reference/dividend-yield) | Dividend yields, one per ticker. |
| [DividendGrowth](/projects/financescenarios/docs/reference/dividend-growth) | Dividend growth, one per ticker. |
| [Mortality](/projects/financescenarios/docs/reference/mortality) | Mortality improvement with the Cairns-Blake-Dowd model. |

## Joint models

| Page | What it covers |
|:-----|:---------------|
| [Knw](/projects/financescenarios/docs/reference/knw) | The KNW model: interest rate and inflation fitted jointly. |
| [KnwSv](/projects/financescenarios/docs/reference/knw-sv) | The KNW model with stochastic volatility. |
| [KnwSvQ](/projects/financescenarios/docs/reference/knw-sv-q) | The risk-neutral (Q-measure) side of the KNW models. |
