---
title: Configuration
seo_title: Configuration Documentation – Finance Scenarios
excerpt: "A simulation run is driven by two named profiles, run settings and a factor set. This page covers every field, multi-instance factors, beliefs and shocks, the published frameworks, long history, real-world and risk-neutral measures, and API keys."
description: "How to configure a Finance Scenarios run: settings and factor-set profiles, every field, beliefs and shocks, published frameworks, measures and API keys."
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

A run is described by two named profiles, each a YAML file:

- `settings/<id>.yaml` holds the run settings: the start date, the Monte Carlo `engine` and the data download settings (`toolkit`).
- `factor-sets/<id>.yaml` holds the factors: which ones are simulated, which tickers and countries they use, and any beliefs that override the fitted values.

Keeping them apart lets you change one side while the other stays identical, for example the same run settings on a narrower factor set:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(settings="default", factor_set="us_only")
scenarios.simulate()
```

Each directory ships a `default.yaml` and a few examples: `settings/long_horizon.yaml`, `factor-sets/us_only.yaml` (the United States only), `factor-sets/core.yaml` (the United States, the euro area and the United Kingdom) and `factor-sets/private_markets.yaml` (listed proxies for private equity, infrastructure, hedge funds and private credit). A profile can start from another with `extends:` and only state what is different, the same way as [regimes](/projects/financescenarios/docs/regimes). When there is no local `settings/` or `factor-sets/` folder, the copies bundled with the package are used, so a plain `pip install` works.

Other ways in: `Scenarios.from_config(config)` for a configuration you already loaded with `load_profiles()`, and `Scenarios.from_config_file(path)` for explicit file paths. The configuration is checked when it loads, so a missing field or a wrong type fails straight away with a clear message.

## Top-level Fields

| Key | Profile | Default | What it is |
|---|---|---|---|
| `start_date` | settings | required | The date the simulation starts from. |
| `engine` | settings | defaults | Number of scenarios, steps, frequency and seed; see the [simulation engine](/projects/financescenarios/docs/simulation-engine). |
| `toolkit` | settings | defaults | The data window and download settings, see below. |
| `reporting` | settings | off | Convert results into one reporting currency. |
| `interest_rates` | factor set | United States | One or more short or long rates, one per country. |
| `inflation` | factor set | United States | One or more inflation rates, one per country. |
| `unemployment` | factor set | United States | One or more unemployment rates, each linked to an inflation entry. |
| `equities` | factor set | `SPY` | One or more equity markets: broad indices, sectors, regions or styles. |
| `fx` | factor set | none | Currency pairs. |
| `credit` | factor set | none | Credit spreads by maturity, rating or country. |
| `commodities` | factor set | none | Commodity prices or futures. |
| `dividend_yield`, `dividend_growth` | factor set | none | Dividend yields and growth, used by the Wilkie framework. |
| `yield_curve` | factor set | off | A Nelson-Siegel yield curve (level, slope and curvature). |
| `credit_term_structure` | factor set | off | A Nelson-Siegel curve of corporate credit spreads. |
| `hjm` | factor set | off | A two-factor HJM forward curve. |
| `credit_migration` | factor set | off | Rating migration and default, fitted on ESMA's CEREP data. |
| `real_estate` | factor set | off | House or commercial property prices. |
| `leading_indicator` | factor set | off | A business-cycle indicator other factors can follow. |
| `mortality` | factor set | off | Mortality improvement, from Eurostat life tables or your own. |
| `climate` | factor set | off | An NGFS climate scenario applied on top of the simulation. |
| `external_scenario_source` | factor set | off | Replace chosen factors with a published scenario set (NAIC's GOES or DNB's). |

How each area behaves is covered in its own guide: [interest rates](/projects/financescenarios/docs/interest-rates), [the KNW model](/projects/financescenarios/docs/knw), [the economy](/projects/financescenarios/docs/economy), [markets](/projects/financescenarios/docs/markets), [portfolios](/projects/financescenarios/docs/portfolio) and [Solvency II](/projects/financescenarios/docs/solvency).

## Several Countries or Markets per Factor

Interest rates, inflation, unemployment, equities, FX and credit can each hold several entries. Every entry becomes its own factor, fitted separately and linked to the others through the correlation matrix. That is how a run holds US, euro area and UK rates side by side, or a broad index next to sector and regional ETFs.

Equities, FX and credit are a plain list:

```yaml
equities:
  - name: us_broad
    ticker: SPY
  - name: europe
    ticker: VGK

fx:
  - name: eur
    country: Germany
```

Interest rates, inflation and unemployment usually share their settings across countries, so they take `defaults` plus a list of `countries` that only state what differs:

```yaml
interest_rates:
  defaults:
    source: oecd
    period: quarterly
  countries:
    - name: United States
    - name: Eurozone
      country: Germany        # the data country, when it differs from the name
```

The name becomes the factor's name in the results, with a suffix added for you: `Eurozone` becomes `eurozone_short_rate`, `eurozone_inflation` and `eurozone_unemployment`. Names must be unique across all factors. Each unemployment entry follows the inflation entry of the same country unless you set `inflation_name`.

## Data Settings

| Key | Default | What it does |
|---|---|---|
| `toolkit.start_date` | 5 years back | Start of the history used for fitting. |
| `toolkit.extra_tickers` | `[]` | Extra tickers to download. |
| `toolkit.benchmark_ticker` | `null` | Leave empty: a ticker equal to the benchmark would be dropped. |
| `toolkit.progress_bar` | `false` | Show download progress. |

Nothing is downloaded until a factor is fitted, and everything is served from the Finance Toolkit's local cache when it is already there. When the OECD's limit of 60 downloads an hour is reached, the latest cached copy is used. To see the data before simulating, `fetch_historical_data(config, build_toolkit(config))` returns the series each factor would be fitted on.

## Beliefs

A belief replaces one fitted parameter with your own view and keeps the rest of the fit. To set where rates head in the long run while keeping the fitted speed and volatility:

```yaml
interest_rates:
  - name: interest_rate
    beliefs:
      long_run_mean: 0.035
```

A field left out or set to `null` keeps the fitted value. All rates are annualized decimals (`0.035` is 3.5%); see [units](/projects/financescenarios/docs/units).

**A path instead of one number.** `long_run_mean` also takes target values at future years, interpolated in between. Rates heading to 6% in year 5 and back to 2% by year 10:

```yaml
long_run_mean:
  anchors:
    5.0: 0.06
    10.0: 0.02
  converge_over_years: 5.0   # optional: then move back to the fitted level over 5 years
```

The target moves; how fast the simulated rate follows it is still the fitted speed of mean reversion.

**One-off shocks.** `shocks` makes a factor jump once at a given year, after which it moves on normally from the new level:

```yaml
inflation:
  - name: inflation
    beliefs:
      shocks:
        - year: 2.0
          magnitude: 0.03    # +3 percentage points in year 2
```

`mode: absolute` sets the level instead of adding to it. For equities a shock is a log return: `-0.4` takes prices about 33% lower.

Beliefs and belief paths only apply to constant-volatility factors that are not conditioned on the business cycle, and not to risk-neutral entries (see below); shocks apply to all.

## Volatility That Clusters (GARCH)

By default a factor's volatility is constant. `volatility_model: garch` lets it cluster instead, so calm periods stay calm and volatile periods stay volatile ([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1)):

```yaml
interest_rates:
  - name: interest_rate
    method: hull_white       # GARCH needs Hull-White for rates
    volatility_model: garch
```

It is available for interest rates, inflation, real estate, credit, the leading indicator, single-factor commodities and dividend yields.

## Following the Business Cycle {#business-cycle-conditioning}

`condition_on_business_cycle: true` makes a factor's drift follow the leading indicator, the way unemployment follows inflation. It needs `leading_indicator.enabled: true`, and the factor is then fitted at the indicator's frequency:

```yaml
leading_indicator:
  enabled: true
  period: yearly

inflation:
  - name: inflation
    condition_on_business_cycle: true
```

## Published Frameworks

A framework is a published recipe for how the variables relate. Each ships as a ready-made factor set, so you can run a paper's model and compare frameworks on the same engine:

| Factor set | Framework | How the variables are linked |
|:-----------|:----------|:-----------------------------|
| `ahlgrim.yaml` (and the default) | [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf) | Each variable is its own process; inflation feeds rates and unemployment, and a correlation matrix ties everything together. |
| `wilkie.yaml` + `settings/wilkie.yaml` | [Wilkie (1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf) | A cascade: inflation first, then dividend yields, long bond yields, dividend growth and share prices, each a function of it. |
| `hibbert.yaml` | [Hibbert, Mowbray and Turnbull (2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf) | Rates and inflation revert to a slowly moving target; equities switch between two regimes. |
| any set with `method: knw` / `knw_sv` | [Koijen, Nijman and Werker (2010)](https://doi.org/10.1093/rfs/hhp058) | Rates and inflation drive each other, optionally with shared stochastic volatility; see the [KNW guide](/projects/financescenarios/docs/knw). |

Wilkie and KNW step in fixed time steps, so `engine.frequency` must match their `period`. `settings/wilkie.yaml` fits on 1995-2019, because Wilkie's long bond model assumes positive real yields.

## Long History

Today tells the model where things are; history tells it how they move. Twenty-five years of data miss the inflation of the 1970s and the crashes of the 1930s, which matters for runs of 50 years or more. `history_source` fits an entry's dynamics on a long history while the run still starts from today's values:

| Factor | `history_source` | Data | From |
|:-------|:-----------------|:-----|-----:|
| equities | `shiller` | [Shiller's](https://shillerdata.com/) US total return, monthly | 1871 |
| equities | `jst` | [Jordà-Schularick-Taylor](https://doi.org/10.1093/qje/qjz012) yearly equity returns of `history_country` | 1870 |
| interest rates | `oecd` | The OECD's short or long rate of `country`, yearly | 1950 |
| interest rates | `millennium` | [Bank of England](https://www.bankofengland.co.uk/statistics/research-datasets) Bank Rate or consol yields, UK | 1694 |
| interest rates | `jst` | Short-term bill returns of `country` | 1870 |
| inflation | `millennium` | UK consumer price inflation | 1209 |
| inflation | `shiller` | US inflation from Shiller's price index | 1872 |

```yaml
interest_rates:
  - name: us_short_rate
    history_source: oecd
    history_start_year: 1950
```

`history_start_year` drops earlier years (medieval harvests and the 1923 hyperinflation are rarely what you want), `history_volatility: recent` keeps the volatility of the recent window, and JST data needs `accept_licence: true` (CC BY-NC-SA, non-commercial).

The long window matters most for rates. Fitted on 2000-2026, the US short rate settles at 5.3% and the 10-year at 3.2%, an inverted curve forever. Fitted on the OECD's rates since 1950, every curve slopes upward again: US 4.5% short and 6.0% long.

## Rates at or Above Zero

`zero_lower_bound: true` keeps an interest rate at or above 0% the shadow-rate way ([Black, 1995](https://doi.org/10.1111/j.1540-6261.1995.tb05182.x)): the model moves on below zero unseen, and the rate you see is the larger of that shadow rate and 0%. Rates then linger at zero for a while, as policy rates did, instead of bouncing straight back. Real-world entries only.

## Anchoring Long-run Rate Levels

`long_run_anchor` replaces a rate's fitted long-run level with an official path:

- `eiopa`: the forward rates of EIOPA's risk-free curve for the entry's `currency` (USD, EUR or GBP), ending at the [ultimate forward rate](https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en) every Solvency II insurer discounts with.
- `dnb` (euro only): the median path of [De Nederlandsche Bank's](https://www.dnb.nl/voor-de-sector/open-boek-toezicht/sectoren/pensioenfondsen/) scenario set, the reference for Dutch pension funds.

Speed and volatility stay fitted, and an explicit `beliefs.long_run_mean` still wins. The default factor set uses `eiopa`: over 30 years its US 10-year median ends at 4.8%, against 4.5% in the NAIC's generator.

## Real-world and Risk-neutral {#real-world-and-risk-neutral-measures}

A real-world run follows how markets have behaved and answers "what could happen?". A risk-neutral run grows every investment at the risk-free rate on average, so it reproduces today's prices and answers "what is this worth today?". Every factor is real-world by default; an entry switches with `measure: risk_neutral`, or a whole run with `scenarios.simulate(measure="risk_neutral")`.

| Factor | Risk-neutral version |
|:-------|:---------------------|
| Equities | Grows at the risk-free rate minus the dividend yield; volatility from option prices or, with `volatility_source: heston`, a Heston model fitted to the volatility smile |
| Interest rates | Today's rate, or a Hull-White rate that follows today's forward curve |
| FX | The interest-rate gap between the two countries |
| Inflation | A forward curve from breakeven inflation (US, UK, Germany or the euro area) |
| KNW with stochastic volatility | A market price of risk fitted to the yield curve |
| Commodities (`schwartz_smith`) | Fitted to the futures curve |
| Unemployment, real estate, leading indicator, mortality, credit | Not available: there is no traded price to match |

Beliefs can't be combined with a risk-neutral entry, since it exists to match the market. The [Solvency II](/projects/financescenarios/docs/solvency) guide shows how real-world and risk-neutral runs work together.

## Example Files

`settings/default.yaml`:

```yaml
name: Default
description: "2,000 scenarios, one step a month, five years ahead, fitted on history since 2000."

start_date: 2026-01-01

engine:
  n_simulations: 2000
  n_steps: 60
  frequency: monthly
  seed: 42

toolkit:
  start_date: 2000-01-01
```

A small factor set, close to `factor-sets/ahlgrim.yaml`:

```yaml
name: Ahlgrim-style
description: One rate, inflation, equity market and unemployment rate for the United States.

interest_rates:
  - name: interest_rate
    source: ticker          # ticker | oecd
    method: hull_white      # hull_white | cir
    ticker: "^IRX"          # 13-week T-bill
    period: daily

inflation:
  - name: inflation
    country: United States
    period: yearly

equities:
  - name: equity
    ticker: SPY
    n_regimes: 2
    period: monthly

unemployment:
  - name: unemployment
    country: United States
    inflation_name: inflation

yield_curve:
  enabled: false

credit: []    # e.g. - {name: ig_7_10y, dimension: maturity, maturity_bucket: "7-10 Years"}
fx: []        # e.g. - {name: eur, country: Germany}
```

`factor-sets/default.yaml` builds on `core.yaml` (the United States, the euro area and the United Kingdom, global equities, gold, oil and the major currencies) with long-run rate levels anchored to EIOPA, and passes every release check. `factor-sets/broad.yaml` switches on every factor.

## API Keys {#secrets}

Profiles never hold API keys. Pass them when creating the scenarios, `Scenarios.from_profiles(..., api_key="...", fred_api_key="...")`, or set `FINANCIAL_MODELING_PREP_API_KEY` and `FRED_API_KEY` in the environment or a `.env` file. Most factors need neither:

| Factor | Key |
|---|---|
| Inflation, unemployment, FX, leading indicator, real estate, OECD interest rates | None (OECD data) |
| Equities, dividends, yield curve, HJM, commodities, ticker interest rates | FMP, optional (Yahoo Finance otherwise, US exchanges only) |
| Credit, commercial real estate | FRED, required |
| Mortality | None (Eurostat, or your own table) |
