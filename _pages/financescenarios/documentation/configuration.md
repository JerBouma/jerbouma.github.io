---
title: Configuration
seo_title: "Configuration Documentation | Finance Scenarios"
seo_title_suffix: false
excerpt: "The modeling choices behind a run: horizon and step, number of scenarios, calibration window, real-world or risk-neutral measure, expert beliefs and published frameworks."
description: "The modeling choices behind a Finance Scenarios run: horizon, scenario count, calibration window, measure, expert beliefs and published frameworks."
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

<div class="ca-nav">
  <a href="#settings-profiles-and-factor-sets"><i class="fas fa-folder-open" aria-hidden="true"></i>Profiles</a>
  <a href="#horizon-and-step"><i class="fas fa-calendar-days" aria-hidden="true"></i>Horizon and step</a>
  <a href="#number-of-scenarios"><i class="fas fa-calculator" aria-hidden="true"></i>Number of scenarios</a>
  <a href="#calibration-window"><i class="fas fa-history" aria-hidden="true"></i>Calibration window</a>
  <a href="#real-world-and-risk-neutral-measures"><i class="fas fa-scale-balanced" aria-hidden="true"></i>Measures</a>
  <a href="#beliefs"><i class="fas fa-lightbulb" aria-hidden="true"></i>Beliefs</a>
  <a href="#published-frameworks"><i class="fas fa-book" aria-hidden="true"></i>Published frameworks</a>
  <a href="#secrets"><i class="fas fa-key" aria-hidden="true"></i>API keys</a>
</div>

## Settings Profiles and Factor Sets {#settings-profiles-and-factor-sets}

A run combines two profiles:

<div class="ca-cards">
  <div><i class="ca-icon fas fa-sliders-h" aria-hidden="true"></i><p class="ca-card-title">Settings profile: how the run executes</p><p>Start date, horizon, step, number of scenarios and calibration window.</p></div>
  <div><i class="ca-icon fas fa-cubes" aria-hidden="true"></i><p class="ca-card-title">Factor set: what is simulated</p><p>Rates, inflation, markets, which countries, and any views that override the fit.</p></div>
</div>

Keeping them apart lets you rerun the same economy at another horizon, or another economy with the same mechanics. The shipped settings profiles:

| Settings profile | What it is for |
|:-----------------|:---------------|
| `default` | 2,000 scenarios, monthly steps, five years ahead, fitted on history since 2000 |
| `long_horizon` | 500 scenarios, so runs of several decades stay fast; the length is chosen per run |
| `wilkie` | Fitted on 1995 to 2007 only, as Wilkie's long-yield equation needs (inflation's own dynamics come from US history since 1919) |
| `goes` | Fitted on history since 2019, to match the NAIC's generator with the `goes` factor set |

And the shipped factor sets:

| Factor set | What it simulates |
|:-----------|:------------------|
| `default` | `core`, with rates anchored to EIOPA's forward rates and fitted on rates since 1950; the recommended start |
| `core` | The US, the euro area and the UK: rates, inflation, unemployment, global equities, gold, oil and the major currencies |
| `us_only` | US rates, inflation, unemployment and equities, plus the shared factors (currencies, commodities); quick to run |
| `broad` | Everything the package can simulate, across many countries; the widest and slowest to fit |
| `private_markets` | `us_only` plus listed stand-ins for private equity, infrastructure, hedge funds and private credit |
| `goes` | `us_only` with the short rate's long-run level set to the NAIC generator's (about 3.73%) |
| `ahlgrim`, `wilkie`, `hibbert` | A published model as its paper wrote it; see [published frameworks](#published-frameworks) |

A run picks one of each:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(settings="default", factor_set="default")
result = scenarios.simulate()
```

## Horizon and Step {#horizon-and-step}

The horizon follows the question: one year for a Solvency II view, since the solvency capital requirement is the 99.5% Value-at-Risk of basic own funds over one year ([Solvency II Directive, Article 101(3)](https://eur-lex.europa.eu/eli/dir/2009/138/oj){:target="_blank"}); 15 to 60 years for an ALM study or a pension fund's continuity analysis. The step should match what the liabilities and the investment policy react to: monthly for rebalancing and hedging decisions, yearly for long projections where intra-year noise adds nothing.

Over long horizons the long-run parameters (where rates and inflation revert to, and how fast) dominate, and today's starting point fades.

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">Small biases compound</p>

A 0.5 percentage point difference in the long-run equity return is about 15% of terminal wealth after 30 years.
</div>

## Number of Scenarios {#number-of-scenarios}

Monte Carlo error falls with the square root of the number of scenarios, and a tail percentile converges far more slowly than the mean: with 2,000 scenarios a 1-in-200 outcome rests on about ten of them. If the figure you report moves more than you could act on when you rerun with another seed, add scenarios or use antithetic variates; the [simulation engine](/projects/financescenarios/docs/simulation-engine#monte-carlo-error) covers both.

A profile of your own can start from a shipped one and state only what differs:

<ol class="ca-steps">
  <li markdown="span">Copy the shipped profiles into your own folder: a profile extends a file in its own folder.</li>
  <li markdown="span">Write your profile next to them, naming the file it extends and only the settings that change.</li>
  <li markdown="span">Load it by name from that folder.</li>
</ol>

For an ALM study:

```yaml
# my-project/settings/my_alm.yaml (a settings profile)
name: ALM study
extends: default.yaml   # the copy scaffold_project("my-project") wrote next to this file

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

Loaded from its folder:

```python
scenarios = Scenarios.from_profiles(
    settings="my_alm", settings_dir="my-project/settings", factor_set="default"
)
```

## Calibration Window {#calibration-window}

Today's data tells the model where things are; the history tells it how they move. The window decides which economic regimes the fitted parameters have seen. A window from 2000 has seen a decade of near-zero rates and low inflation. Rates drift so slowly against its length that the speed of mean reversion is barely pinned down, and the long-run level, estimated together with it, swings with small changes in the data. Where US rates settle in each window:

| Window | US short rate | US 10-year | The curve |
|:-------|:--------------|:-----------|:----------|
| Since 2000 | 5.3% | 3.2% | Inverted forever |
| OECD rates since 1950 | 4.5% | 6.0% | Every curve slopes upward again |

The 2000 window's result is a weakly identified estimate, not a forecast.

Short windows also understate tail events that did not happen in them. For runs of decades, the speed of mean reversion and the volatility should come from a history that includes the inflation of the 1970s and a few full rate cycles.

### Long History {#long-history}

A factor can be fitted on a long history while the run still starts from today's values; the default factor set fits its rates on the OECD's data since 1950. Older sources exist:

| Source | Series | From |
|:-------|:-------|:-----|
| [Shiller](https://shillerdata.com/) | US equity returns and inflation | The 1870s |
| [Jordà-Schularick-Taylor](https://doi.org/10.1093/qje/qjz012) | A panel of returns and bill rates by country (non-commercial licence) | 1870 |
| [Bank of England](https://www.bankofengland.co.uk/statistics/research-datasets) | UK series | 1694 for rates, 1209 for prices |

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">Older is not always better</p>

Medieval harvests and the 1923 hyperinflation are rarely what you want. A start year cuts the history short, and the volatility can come from the recent window while the long history sets the mean reversion.
</div>

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
interest_rates:
  defaults:                  # every country's rates
    history_source: oecd
    history_start_year: 1950
    history_volatility: recent   # swings from the recent window, reversion from the long one
```

## Real-World and Risk-Neutral {#real-world-and-risk-neutral-measures}

Each measure answers its own question:

<div class="ca-cards">
  <div><i class="ca-icon fas fa-globe" aria-hidden="true"></i><p class="ca-card-title">Real-world: what could happen?</p><p>Follows how markets have behaved, risk premia included. For ALM, solvency projections and strategic asset allocation.</p></div>
  <div><i class="ca-icon fas fa-scale-balanced" aria-hidden="true"></i><p class="ca-card-title">Risk-neutral: what is this worth today?</p><p>Grows every asset at the risk-free rate on average, so it reproduces today's market prices. For guarantees, options and other embedded features.</p></div>
</div>

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">A classic error</p>

Mixing them up: a risk-neutral run has no equity risk premium, so it says nothing about expected returns, and a real-world run does not price an option correctly. [Merton (1973)](https://doi.org/10.2307/3003143) gives the classic no-arbitrage argument and [the SOA (2022)](https://www.soa.org/resources/research-reports/2022/understanding-the-connection/) a practical treatment of when each measure fits.
</div>

Every factor is real-world by default; a single factor or a whole run can switch to risk-neutral. The risk-neutral version of each factor:

| Factor | Risk-neutral version |
|:-------|:---------------------|
| Equities | Grows at the risk-free rate minus the dividend yield; volatility from option prices or a Heston model fitted to the volatility smile |
| Interest rates | A Hull-White rate that reproduces EIOPA's risk-free curve for the dollar, euro and pound (the Treasury curve otherwise), with its volatility fitted to how much yields across maturities have moved; the default when the whole run is risk-neutral. Switched on one factor alone, a flat path at today's rate, or the Treasury curve with `risk_neutral_forward_curve` (`risk_neutral_curve: eiopa` for EIOPA's) |
| FX | The interest-rate gap between the two currencies |
| Inflation | Random around the breakeven inflation curve (US, UK, Germany or the euro area) with its historical volatility, so the expected price index matches the curve; part of a whole risk-neutral run. `risk_neutral_volatility: none` follows the curve exactly |
| KNW with stochastic volatility | A market price of risk fitted to the yield curve |
| Commodities (two-factor) | Fitted to the futures curve |
| Unemployment, real estate, leading indicator, mortality, credit | Not available: there is no traded price to match |

```python
result = scenarios.simulate(measure="risk_neutral")   # or measure: risk_neutral on one factor
```

<div class="fs-callout" markdown="1">
A flat rate at today's level is deterministic discounting: it has no rate volatility and ignores the shape of the curve, so it does not value options or guarantees on rates. Use the forward-curve version for those.
</div>

The [Solvency II](/projects/financescenarios/docs/solvency) guide shows how the two measures work together in a nested valuation.

## Beliefs: Expert Judgement over the Fit {#beliefs}

A fitted parameter is an estimate from one stretch of history; a long-run view is a judgement. A belief replaces one fitted parameter with your own value and keeps the rest of the fit. The typical case is the long-run level of rates or inflation: you set where it heads, the data still sets how fast and how volatile. Values are annualized decimals (0.035 is 3.5%, see [units](/projects/financescenarios/docs/units)).

The target can also be a path (inflation at 6% in year 5, back to 2% by year 10), and a factor can take a one-off shock at a given year, after which it moves on normally from the new level. That is how a stress narrative enters a real-world run; [regimes](/projects/financescenarios/docs/regimes) package such stories.

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
inflation:
  defaults:                 # every country's inflation; a regime can target one
    beliefs:
      long_run_mean:
        anchors:            # year: target, interpolated in between
          5.0: 0.06
          10.0: 0.02
      shocks:
        - year: 2.0
          magnitude: 0.03   # +3 percentage points in year 2
```

<div class="fs-callout fs-callout--limits" markdown="1">
<p class="fs-callout__title">Limits</p>

- Beliefs don't apply to risk-neutral factors, which exist to match the market.
- A level path applies only to constant-volatility factors that do not follow the business cycle.
</div>

### Anchoring Long-Run Rate Levels {#anchoring-long-run-rate-levels}

Instead of your own view, a rate's long-run level can follow an official path.

Anchored to EIOPA, it follows the forward rates of EIOPA's risk-free curve for its currency (USD, EUR or GBP), which converge to the [ultimate forward rate](https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en) Solvency II insurers discount with only beyond the last liquid point (30 years for the dollar, 20 for the euro and 50 for sterling, as set in [EIOPA's RFR technical documentation, EIOPA-BoS-25-599, section 9.2.2 and Tables 7-8](https://www.eiopa.europa.eu/document/download/f7fca58f-4d24-4441-ac60-de562bf26d77_en?filename=EIOPA-BoS-25-599%20-%20RFR%20Technical%20Documentation.pdf#page=44){:target="_blank"}; from 30 January 2027 the amended rules extrapolate from a first smoothing point instead). Over a few decades the anchor therefore still follows market forwards, not the UFR.

Anchored to DNB (euro only), it follows the median of [De Nederlandsche Bank's](https://www.dnb.nl/voor-de-sector/open-boek-toezicht/sectoren/pensioenfondsen/) pension scenario set. Speed and volatility stay fitted, and an explicit belief still wins. The default factor set uses EIOPA; the US 10-year median after 30 years:

<div class="ca-nums fs-nums">
  <span><b>4.8%</b>default factor set, anchored to EIOPA</span>
  <span><b>4.5%</b>the NAIC's generator</span>
</div>

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
interest_rates:
  defaults:
    long_run_anchor: eiopa   # or dnb, for euro rates
```

### Keeping Rates at or Above Zero {#keeping-rates-at-or-above-zero}

Gaussian rate models let rates go well below zero. No floor is the default, since negative rates did happen; a zero lower bound turns the model into a shadow rate floored at 0%, so rates linger at zero as policy rates did. [Interest rates](/projects/financescenarios/docs/interest-rates#keeping-rates-at-or-above-zero) explains the model. Real-world rates only.

### Volatility That Clusters and the Business Cycle {#business-cycle-conditioning}

By default volatility is constant. Two alternatives, which don't combine on one factor:

<div class="ca-cards">
  <div><i class="ca-icon fas fa-pulse" aria-hidden="true"></i><p class="ca-card-title">GARCH volatility</p><p>Volatility clusters, so calm periods stay calm and turbulent ones stay turbulent (<a href="https://doi.org/10.1016/0304-4076(86)90063-1">Bollerslev, 1986</a>).</p></div>
  <div><i class="ca-icon fas fa-gauge" aria-hidden="true"></i><p class="ca-card-title">The business cycle</p><p>A factor's drift follows the leading indicator, so inflation or rates move with the business cycle (<a href="/projects/financescenarios/docs/economy#conditioning-on-the-cycle">conditioning on the cycle</a>).</p></div>
</div>

Switching on the cycle, or GARCH instead:

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
leading_indicator:
  enabled: true

inflation:
  defaults:
    condition_on_business_cycle: true   # or volatility_model: garch
```

## Published Frameworks {#published-frameworks}

Economic scenario generators differ mostly in how they link the variables. Each framework ships as a factor set, so you can run a paper's model and compare frameworks on the same engine and data:

| Factor set | Framework | How the variables are linked |
|:-----------|:----------|:-----------------------------|
| `ahlgrim` | [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf) | Each variable is its own process; inflation feeds rates and unemployment, and a correlation matrix ties everything together. |
| `wilkie` | [Wilkie (1986)](https://doi.org/10.1017/S0071368600009009) | A cascade: inflation first, then dividend yields, long bond yields, dividend growth and share prices, each driven by it. |
| `hibbert` | [Hibbert, Mowbray and Turnbull (2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf) | Rates and inflation revert to a slowly moving target; equities switch between two regimes. |
| any set with the KNW method | [Koijen, Nijman and Werker (2010)](https://doi.org/10.1093/rfs/hhp058) | Rates and inflation drive each other, optionally with shared stochastic volatility; see the [KNW guide](/projects/financescenarios/docs/knw). |

Wilkie is a discrete-time model. KNW is continuous-time in the paper, but the package fits its discrete-time version, a VAR(1) of the short rate and expected inflation, as DNB's [Commissie Parameters (2022)](https://open.overheid.nl/repository/ronl-f2685a42fd0bf01d5821446bcda34e719fdf7ef1/1/pdf/bijlage-2-technische-appendix.pdf){:target="_blank"} does. For both, the step must match the frequency they were fitted at.

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">The window is a modeling choice</p>

Wilkie's long bond model, a real yield plus an allowance for expected inflation ([Wilkie, 1986, section 3.12](https://doi.org/10.1017/S0071368600009009){:target="_blank"}), needs the long yield to stay above average inflation, which US yields did not from 2008 to 2017, so its settings profile fits on 1995 to 2007: the calibration window is a modeling choice, not a technicality.
</div>

Running Wilkie's model with its own settings:

```python
scenarios = Scenarios.from_profiles(settings="wilkie", factor_set="wilkie")
```

## API Keys {#secrets}

Profiles never hold API keys. Most factors need none:

| Factors | Data | Key |
|:--------|:-----|:----|
| Inflation, unemployment, FX, real estate, OECD rates | OECD | None |
| Mortality | Eurostat | None |
| Equities, commodities, the yield curve | Financial Modeling Prep when a key is given, Yahoo Finance otherwise | Optional |
| Credit spreads, commercial real estate | FRED | A FRED key |

Pass the keys when creating the scenarios, or set `FINANCIAL_MODELING_PREP_API_KEY` and `FRED_API_KEY` in the environment.

```python
scenarios = Scenarios.from_profiles(
    settings="default",
    factor_set="default",
    api_key="FINANCIAL_MODELING_PREP_KEY",
    fred_api_key="FRED_KEY",
)
```
