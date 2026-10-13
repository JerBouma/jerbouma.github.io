---
title: Documentation
seo_title: Finance Scenarios Documentation
excerpt: "Finance Scenarios is an open-source economic scenario generator: thousands of joint scenarios for interest rates, inflation, equities, currencies, credit and more, linked the way they have been historically."
description: "Finance Scenarios documentation: what the economic scenario generator models, how factors are linked, real-world vs risk-neutral runs, and a map of the guides."
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

Finance Scenarios is an economic scenario generator (ESG). It simulates thousands of joint scenarios for interest rates, inflation, equities, currencies, credit and other economic variables, each fitted to its own history and linked to the others the way they have moved together.

An ESG replaces a single forecast with a distribution. That is what ALM studies, strategic asset allocation, pension and retirement planning, reserving and Solvency II valuation need: the median path, but also the bad years and the tail. Installation and a first run are on the [Finance Scenarios page](/projects/financescenarios#installation); the [example notebooks](/projects/financescenarios#notebooks) show every part with real output.

## What Is Modeled

Each factor follows a model suited to how it behaves: rates, inflation and spreads revert to a long-run level at their own historical speed, equities switch between calm and crisis regimes so bad months cluster, and currencies keep their historical volatility.

| Area | What is simulated | Model | Guide |
|:-----|:------------------|:------|:------|
| Short and long rates | One rate per country, short or long end | Hull-White (default, can go negative), CIR (rates kept near or above zero), Wilkie, Hibbert two-factor | [Interest rates](/projects/financescenarios/docs/interest-rates) |
| Yield curve | Level, slope and curvature of the whole curve | Dynamic Nelson-Siegel | [Interest rates](/projects/financescenarios/docs/interest-rates) |
| Forward curve | The full forward curve, arbitrage-free | Two-factor Gaussian HJM | [Interest rates](/projects/financescenarios/docs/interest-rates) |
| Rates and inflation jointly | Nominal and real rates, inflation, optionally equities | KNW, with stochastic volatility or priced like the market | [KNW](/projects/financescenarios/docs/knw) |
| Inflation | Year-over-year inflation per country | Mean-reverting (Ornstein-Uhlenbeck) or Wilkie AR(1) | [Economy](/projects/financescenarios/docs/economy) |
| Unemployment | Unemployment rate per country | Mean-reverting with a Phillips-curve link to inflation | [Economy](/projects/financescenarios/docs/economy) |
| Business cycle | OECD composite leading indicator | Mean-reverting | [Economy](/projects/financescenarios/docs/economy) |
| Longevity | Mortality improvement by age | Cairns-Blake-Dowd | [Economy](/projects/financescenarios/docs/economy) |
| Equities | Indices, sectors, regions, styles | Regime-switching lognormal | [Markets](/projects/financescenarios/docs/markets) |
| Currencies | Each currency against the dollar | Lognormal, optionally with an interest-rate-parity drift | [Markets](/projects/financescenarios/docs/markets) |
| Commodities | Gold, oil and other futures | Mean-reverting log price (Schwartz), or two-factor | [Markets](/projects/financescenarios/docs/markets) |
| Real estate | House-price growth | Mean-reverting | [Markets](/projects/financescenarios/docs/markets) |
| Dividends | Dividend yield and dividend growth | Mean-reverting log yield, Wilkie-style growth | [Markets](/projects/financescenarios/docs/markets) |
| Credit | Spreads by maturity or rating, the credit curve, rating migration and default | Mean-reverting spreads, Nelson-Siegel credit curve, a credit cycle driving migration | [Markets](/projects/financescenarios/docs/markets) |
| Stress and climate | Fed and ESRB stress tests, NGFS climate pathways, your own narratives | Overlays on a run | [Regimes](/projects/financescenarios/docs/regimes) |

Interest rates, inflation, equities and unemployment are always simulated; the rest is switched on per factor set. [Coverage](/projects/financescenarios/docs/coverage) lists every model, calibration choice and known gap, and the [reference](/projects/financescenarios/docs/reference) documents each model's parameters.

## How the Factors Are Linked

A sell-off should come with the spread, rate and currency moves history saw alongside one. Where theory says one variable drives another (inflation driving unemployment, a rate gap driving an exchange rate), the driver's simulated path feeds the next factor; everything else is tied together by one correlation matrix of the historical shocks. [How a run is built](/projects/financescenarios/docs/architecture#dependence) explains both.

## Real-World and Risk-Neutral Runs

A **real-world** run keeps each factor's historical drift and risk premia and answers "what could happen?" (ALM, allocation, capital). A **risk-neutral** run grows every asset at the risk-free rate so it reproduces today's prices, and answers "what is this worth?" (guarantees, the Solvency II best estimate). [Configuration](/projects/financescenarios/docs/configuration#real-world-and-risk-neutral-measures) explains the difference and which factors have a risk-neutral form.

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(settings="default", factor_set="us_only")

real_world = scenarios.simulate()                         # ALM, allocation, risk
risk_neutral = scenarios.simulate(measure="risk_neutral")  # valuation, best estimate
real_world.describe()                                     # every factor at a glance
```

All history comes from the [Finance Toolkit](https://github.com/JerBouma/FinanceToolkit); most factors calibrate on free OECD and Yahoo Finance data without any API key. Each factor is simulated in its own currency and can be converted into one reporting currency afterwards.

## Map of the Documentation

| Page | What it covers |
|:-----|:---------------|
| [How a run is built](/projects/financescenarios/docs/architecture) | How a scenario set is built: data, calibration, dependence, simulation, output. |
| [Simulation engine](/projects/financescenarios/docs/simulation-engine) | Correlated shocks, fat tails, time stepping, Monte Carlo error and working with a run. |
| [Configuration](/projects/financescenarios/docs/configuration) | Profiles, beliefs, published frameworks (Wilkie, Ahlgrim, Hibbert, KNW), long history and the two measures. |
| [Units](/projects/financescenarios/docs/units) | How every result reads: rates as annualized decimals, prices as annualized returns since the start. |
| [Interest rates](/projects/financescenarios/docs/interest-rates) | Short-rate models and when to pick each, the zero lower bound, the yield curve, credit curve and HJM. |
| [KNW](/projects/financescenarios/docs/knw) | The joint interest-rate and inflation models behind De Nederlandsche Bank's scenario set. |
| [Economy](/projects/financescenarios/docs/economy) | Inflation, unemployment, the business cycle and mortality. |
| [Markets](/projects/financescenarios/docs/markets) | Equities, currencies, commodities, real estate, dividends, credit spreads and rating migration. |
| [Regimes](/projects/financescenarios/docs/regimes) | Stress narratives, official stress tests and climate pathways. |
| [Portfolio](/projects/financescenarios/docs/portfolio) | From scenarios to an investment mix: rebalancing, cashflows, glidepaths, fees, risk metrics and backtests. |
| [Solvency](/projects/financescenarios/docs/solvency) | Best estimate, own funds and the SCR under Solvency II, and the market-consistency check. |
| [Validation](/projects/financescenarios/docs/validation) | How the output is checked against theory and external benchmarks. |
| [Coverage](/projects/financescenarios/docs/coverage) | What the project can and can't do, and why. |
| [Plotting](/projects/financescenarios/docs/plotting) | Fan charts, paths and distributions for every result. |
| [Reference](/projects/financescenarios/docs/reference) | Every class and function, with its parameters, papers and a worked example. |
