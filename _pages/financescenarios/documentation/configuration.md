---
title: Configuration
seo_title: Configuration Documentation – Finance Scenarios
excerpt: "The modelling choices behind a run: horizon and step, number of scenarios, calibration window, real-world or risk-neutral measure, expert beliefs and published frameworks."
description: "The modelling choices behind a Finance Scenarios run: horizon, scenario count, calibration window, measure, expert beliefs and published frameworks."
author_profile: false
permalink: /projects/financescenarios/docs/configuration
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

A scenario set is only as good as the choices behind it: how far ahead and in what steps, how many scenarios, which history the models learn from, which probability measure, and where expert judgement overrides the data. This page covers those choices. Every field is listed in the [reference](/projects/financescenarios/docs/reference/configuration-classes).

A run is described by two YAML profiles. A **settings** profile says how the run executes (start date, horizon, step, number of scenarios, calibration window). A **factor set** says what is simulated (rates, inflation, markets, which countries and tickers) and any views that override the fit. Keeping them apart lets you rerun the same economy at another horizon, or another economy with the same mechanics.

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(settings="default", factor_set="default")
result = scenarios.simulate()
```

The shipped factor sets range from `us_only` to `core` (the United States, the euro area and the United Kingdom) and `broad` (every factor). `default` builds on `core` with rates anchored to EIOPA and fitted on a long history, both explained below. A profile can start from another with `extends:` and state only what differs.

## Horizon and Step

The horizon follows the question. A one-year Solvency II view needs one year, an ALM study or a pension fund's continuity analysis 15 to 60 years. The step should be fine enough to capture what the liabilities and the investment policy react to: monthly for rebalancing and hedging decisions, yearly for long-horizon projections where intra-year noise adds nothing.

Two things change with the horizon. Over long horizons the long-run parameters (where rates and inflation revert to, how fast) dominate the result, and today's starting point fades. And small biases compound: a 0.5 percentage point difference in the long-run equity return is about 15% of terminal wealth after 30 years.

## Number of Scenarios

Monte Carlo error falls with the square root of the number of scenarios: four times as many scenarios halves the noise. The mean of a distribution converges fast; a tail percentile converges slowly, because only a few scenarios sit out there. With 2,000 scenarios a 1-in-200 outcome rests on about ten of them.

A practical test: rerun with another seed and see how much the figure you care about moves. If the 5th percentile of the funding ratio shifts more than you could act on, add scenarios or switch on antithetic variates (each shock paired with its mirror image). The [simulation engine](/projects/financescenarios/docs/simulation-engine) covers both, plus fat-tailed shocks.

```yaml
# settings/my_alm.yaml
name: ALM study
extends: default.yaml

start_date: 2026-01-01

engine:
  n_simulations: 5000
  n_steps: 30
  frequency: yearly
  antithetic: true      # paired +/- shocks, less Monte Carlo noise
  seed: 42              # same inputs, same scenarios

toolkit:
  start_date: 1990-01-01   # the calibration window
```

## Calibration Window

Today's data tells the model where things are; the history tells it how they move. The window decides which economic regimes the fitted parameters have seen. A window of 2000 to today has seen near-zero rates and low inflation, and little else. Fitted on it, the US short rate settles at 5.3% and the 10-year at 3.2%: an inverted curve forever. Fitted on the OECD's rates since 1950, every curve slopes upward again, with US rates at 4.5% short and 6.0% long.

Short windows also understate tail events that did not happen in them. For runs of decades, the speed of mean reversion and the volatility should come from a history that includes the inflation of the 1970s and a few full rate cycles.

### Long History {#long-history}

A factor can be fitted on a long history while the run still starts from today's values; the default factor set fits its rates on the OECD's data since 1950. Sources go back further: [Shiller's](https://shillerdata.com/) US equity returns and inflation from the 1870s, the [Jordà-Schularick-Taylor](https://doi.org/10.1093/qje/qjz012) panel of returns and bill rates by country from 1870 (non-commercial licence), and the [Bank of England's](https://www.bankofengland.co.uk/statistics/research-datasets) UK series from 1694 for rates and 1209 for prices. Older is not always better: medieval harvests and the 1923 hyperinflation are rarely what you want, so a start year cuts the history short, and the volatility can come from the recent window while the long history sets the mean reversion.

```yaml
interest_rates:
  - name: us_short_rate
    history_source: oecd
    history_start_year: 1950
```

## Real-world and Risk-neutral {#real-world-and-risk-neutral-measures}

A **real-world** run follows how markets have behaved, risk premia included, and answers "what could happen?": ALM, solvency projections, strategic asset allocation. A **risk-neutral** run grows every asset at the risk-free rate on average, so it reproduces today's market prices and answers "what is this worth today?": valuing guarantees, options and other embedded features. Mixing them up is a classic error: a risk-neutral run has no equity risk premium, so it says nothing about expected returns; a real-world run does not price an option correctly.

Every factor is real-world by default. An entry switches with `measure: risk_neutral`, a whole run with `simulate(measure="risk_neutral")`.

| Factor | Risk-neutral version |
|:-------|:---------------------|
| Equities | Grows at the risk-free rate minus the dividend yield; volatility from option prices or a Heston model fitted to the volatility smile |
| Interest rates | Today's rate, or a Hull-White rate that follows today's forward curve |
| FX | The interest-rate gap between the two currencies |
| Inflation | A forward curve from breakeven inflation (US, UK, Germany or the euro area) |
| KNW with stochastic volatility | A market price of risk fitted to the yield curve |
| Commodities (two-factor) | Fitted to the futures curve |
| Unemployment, real estate, leading indicator, mortality, credit | Not available: there is no traded price to match |

The [Solvency II](/projects/financescenarios/docs/solvency) guide shows how the two measures work together in a nested valuation.

## Beliefs: Expert Judgement over the Fit

A fitted parameter is an estimate from one stretch of history; a long-run view is a judgement. A belief replaces one fitted parameter with your own value and keeps the rest of the fit. The typical case is the long-run level of rates or inflation: you set where it heads, the data still sets how fast and how volatile. All values are annualized decimals (`0.035` is 3.5%, see [units](/projects/financescenarios/docs/units)).

The target can also be a path (inflation at 6% in year 5, back to 2% by year 10), and a factor can take a one-off shock at a given year, after which it moves on normally from the new level. That is how a stress narrative enters a real-world run; [regimes](/projects/financescenarios/docs/regimes) package such stories.

```yaml
inflation:
  - name: inflation
    beliefs:
      long_run_mean:
        anchors:            # year: target, interpolated in between
          5.0: 0.06
          10.0: 0.02
      shocks:
        - year: 2.0
          magnitude: 0.03   # +3 percentage points in year 2
```

Beliefs don't combine with risk-neutral entries, which exist to match the market, and level beliefs apply only to constant-volatility factors that do not follow the business cycle.

### Anchoring Long-run Rate Levels {#anchoring-long-run-rate-levels}

Instead of your own view, a rate's long-run level can follow an official path. With `eiopa` it follows the forward rates of EIOPA's risk-free curve for its currency (USD, EUR or GBP), ending at the [ultimate forward rate](https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en) Solvency II insurers discount with. With `dnb` (euro only) it follows the median of [De Nederlandsche Bank's](https://www.dnb.nl/voor-de-sector/open-boek-toezicht/sectoren/pensioenfondsen/) pension scenario set. Speed and volatility stay fitted, and an explicit belief still wins. The default factor set uses EIOPA: over 30 years its US 10-year median ends at 4.8%, against 4.5% in the NAIC's generator.

### Keeping Rates at or Above Zero {#keeping-rates-at-or-above-zero}

Gaussian rate models let rates go well below zero. Negative rates did happen (euro, yen, Swiss franc), so this is off by default, but for many uses a floor is the more plausible assumption. With a zero lower bound, the model moves on below zero unseen and the observed rate is the larger of that shadow rate and 0% ([Black, 1995](https://doi.org/10.1111/j.1540-6261.1995.tb05182.x)). Rates then linger at zero for a while, as policy rates did, instead of bouncing straight back. Real-world entries only.

### Volatility That Clusters and the Business Cycle {#business-cycle-conditioning}

By default volatility is constant. With GARCH it clusters, so calm periods stay calm and turbulent ones stay turbulent ([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1)). Alternatively a factor's drift can follow the leading indicator, so inflation or rates move with the business cycle.

```yaml
leading_indicator:
  enabled: true

inflation:
  - name: inflation
    condition_on_business_cycle: true
```

## Published Frameworks {#published-frameworks}

Economic scenario generators differ mostly in how they link the variables. Each framework ships as a ready-made factor set, so you can run a paper's model and compare frameworks on the same engine and data:

| Factor set | Framework | How the variables are linked |
|:-----------|:----------|:-----------------------------|
| `ahlgrim` | [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf) | Each variable is its own process; inflation feeds rates and unemployment, and a correlation matrix ties everything together. |
| `wilkie` | [Wilkie (1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf) | A cascade: inflation first, then dividend yields, long bond yields, dividend growth and share prices, each driven by it. |
| `hibbert` | [Hibbert, Mowbray and Turnbull (2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf) | Rates and inflation revert to a slowly moving target; equities switch between two regimes. |
| any set with the KNW method | [Koijen, Nijman and Werker (2010)](https://doi.org/10.1093/rfs/hhp058) | Rates and inflation drive each other, optionally with shared stochastic volatility; see the [KNW guide](/projects/financescenarios/docs/knw). |

Wilkie and KNW are discrete-time models, so the step must match the frequency they were fitted at. Wilkie's set comes with its own settings profile fitted on 1995 to 2007: its long bond model needs the long yield to stay above average inflation, which US yields did not from 2008 to 2017. A neat illustration of why the calibration window is a modelling choice, not a technicality.

```python
scenarios = Scenarios.from_profiles(settings="wilkie", factor_set="wilkie")
```

## API Keys {#secrets}

Profiles never hold API keys. Most factors need none: inflation, unemployment, FX, real estate and OECD rates come from the OECD, mortality from Eurostat. Equities, commodities and the yield curve use Financial Modeling Prep when a key is given (Yahoo Finance otherwise, US exchanges only); credit spreads and commercial real estate need a FRED key. Pass them when creating the scenarios or set them in the environment (`FINANCIAL_MODELING_PREP_API_KEY`, `FRED_API_KEY`):

```python
scenarios = Scenarios.from_profiles(
    settings="default",
    factor_set="default",
    api_key="FINANCIAL_MODELING_PREP_KEY",
    fred_api_key="FRED_KEY",
)
```
