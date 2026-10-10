---
title: Configuration
seo_title: Configuration Documentation – FinanceScenarios
excerpt: "A simulation run is driven by two named profiles, run settings and a factor set. This page covers every field, multi-instance factors, beliefs and shocks, the published frameworks, long history, real-world and risk-neutral measures, and API keys."
description: "How to configure a FinanceScenarios run: settings and factor-set profiles, every field, beliefs and shocks, published frameworks, measures and API keys."
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

A simulation run is driven by **two named profiles**, each a directory of one-YAML-file-per-preset (optionally `extends:`-ing another, same pattern as `regimes/`; see [regimes](/projects/financescenarios/docs/regimes)), at the repository root by default:

- `settings/<id>.yaml` holds run settings only: `start_date`, the Monte Carlo `engine`, and the `toolkit`'s data-fetch settings. Nothing here names a ticker/index/country or sets a belief.
- `factor-sets/<id>.yaml` holds every factor definition: which factors are configured, their calibration settings, and any belief overrides. Anything that picks an index/ETF/ticker/country, or overrides a calibrated parameter, lives here instead.

Each directory ships a `default.yaml` profile (the run-everything-as-shipped baseline) plus example profiles proving the pattern, such as `settings/long_horizon.yaml`, `factor-sets/us_only.yaml` (interest rates/inflation/unemployment/equities narrowed to the United States) `factor-sets/core.yaml` (the United States, the euro area and the United Kingdom with monthly or quarterly data only: a curated set that passes every release check) and `factor-sets/private_markets.yaml` (us_only plus listed proxies for private equity, infrastructure, hedge funds and private credit, set with an equity entry's `asset_class` key; pair it with the `endowment_model` portfolio). Add your own alongside them; a profile only needs to state what's different from `extends:`, if anything.

`load_profiles()` in `config_controller.py` resolves a named settings profile and a named factor-set profile (each independently, including its own `extends` chain) and merges them into one `ScenariosConfig` object, validated via [Pydantic](https://docs.pydantic.dev) (types, required fields, constraints like "greater than 0", all checked at load time with a clear error on mismatch):

```python
from financescenarios import load_profiles

config = load_profiles("settings", "default", "factor-sets", "default")
```

Swap either id independently to compare runs while holding the other side byte-identical; e.g. `load_profiles("settings", "default", "factor-sets", "us_only")` keeps every run setting the same and only narrows the factor set.

`load_config(config_path, factors_path=None)` still works for anyone calling it directly with explicit file paths (e.g. a config assembled outside `settings/`/`factor-sets/` entirely); `factors_path` defaults to a `factors.yaml` sibling of `config_path`, and if that file doesn't exist, every factor section just falls back to `ScenariosConfig`'s own single-region defaults, the same as any other omitted section.

`Scenarios.from_profiles(settings, factor_set, regime=None)` does all of this in one call: it loads the named pair (and, optionally, a named regime from `regimes/`), builds the FinanceToolkit `Toolkit` instance to calibrate against, and keeps the resolved config on the instance, so `simulate()` needs no arguments. `Scenarios.from_config(config)` is the same for a config you already hold, and `Scenarios.from_config_file(config_path, factors_path=None)` the same for two explicit file paths. There is no separate `Toolkit` to construct in any of them: `build_toolkit()` in `scenarios_controller.py` builds it straight from `config.toolkit` and the tickers named in `interest_rates`/`equities` (`config.tickers`).

A directory argument that doesn't exist falls back to the copy of those profiles bundled inside the package (`profiles_controller.resolve_directory()`), which is what makes `Scenarios.from_profiles()` work from a plain `pip install` with nothing scaffolded yet. A local directory of the same name always wins, so `scaffold_project()` copies stay authoritative once you have them.

## Top-level fields

| Key | Profile | Type | Required | Notes |
|---|---|---|---|---|
| `start_date` | `settings/<id>.yaml` | date | Yes | The simulation's starting date. Loading the config fails if this is missing. |
| `engine` | `settings/<id>.yaml` | section | No | Monte Carlo engine settings, see [simulation-engine](/projects/financescenarios/docs/simulation-engine). Defaults apply if omitted. |
| `toolkit` | `settings/<id>.yaml` | section | No | Settings for the embedded FinanceToolkit `Toolkit` instance, see below. |
| `reporting` | `settings/<id>.yaml` | section | No | Reporting-currency conversion settings, see `Reporting`. A run setting (has no effect on calibration/simulation), not a per-factor one; lives beside `engine`/`toolkit`. |
| `interest_rates` | `factor-sets/<id>.yaml` | `defaults`+`countries` | No | One or more interest-rate "cloud" factor settings (one per country/region), see `InterestRates` and Multi-instance factors below. Must have at least one entry. |
| `inflation` | `factor-sets/<id>.yaml` | `defaults`+`countries` | No | One or more inflation "cloud" factor settings (one per country), see `Inflation` and Multi-instance factors below. Must have at least one entry. |
| `equities` | `factor-sets/<id>.yaml` | list of sections | No | One or more equity "cloud" factor settings (broad index, sector, region, style, ...), see `Equities` and Multi-instance factors below. Must have at least one entry; defaults to a single `SPY`-tracking entry named `"equity"`. |
| `unemployment` | `factor-sets/<id>.yaml` | `defaults`+`countries` | No | One or more unemployment "cloud" factor settings (one per region), each paired with a named inflation entry, see `Unemployment` and Multi-instance factors below. Must have at least one entry. |
| `yield_curve` | `factor-sets/<id>.yaml` | section | No | Opt-in Nelson-Siegel yield curve settings, see `TermStructure`. Off in the schema (`enabled: false`), but `factor-sets/default.yaml` turns it on. |
| `credit_term_structure` | `factor-sets/<id>.yaml` | section | No | Opt-in Nelson-Siegel credit-spread term structure settings, reusing the yield curve's own machinery against the US Treasury's HQM corporate spread curve (`source: hqm`, the default, monthly from 1984) or a bond-level spread panel (`source: bond_panel`, a 1.8 GB download), alongside `credit`'s discrete maturity/rating buckets, not a replacement for them. Disabled by default. |
| `credit_migration` | `factor-sets/<id>.yaml` | section | No | Opt-in rating migration and default: a credit cycle calibrated on a rating agency's transition counts and default rates from ESMA's CEREP (`agency`, `rating_type`, `region`, `matrix_years`), see `CreditMigration`. Disabled by default. |
| `climate` | `factor-sets/<id>.yaml` | section | No | Opt-in NGFS climate scenario overlay (`scenario`, `model`, `risk`, `equity_country`, `country_map`, `carbon_price`, `carbon_price_region`): each rate, inflation, unemployment and equity factor shifted by the scenario's deviation from its baseline after simulating, see `climate_controller.apply_climate_scenario`. Disabled by default. |
| `real_estate` | `factor-sets/<id>.yaml` | section | No | Opt-in real estate factor settings, see `RealEstate`. Disabled by default. |
| `credit` | `factor-sets/<id>.yaml` | list of sections | No | Opt-in list of credit spread bucket factor settings, see `Credit` and Multi-instance factors below. Empty (`[]`) by default. |
| `leading_indicator` | `factor-sets/<id>.yaml` | section | No | Opt-in leading indicator factor settings, see `LeadingIndicator`. Disabled by default. |
| `fx` | `factor-sets/<id>.yaml` | list of sections | No | Opt-in list of currency-pair factor settings, see `FX` and Multi-instance factors below. Empty (`[]`) by default. |
| `commodities` | `factor-sets/<id>.yaml` | list of sections | No | Opt-in list of commodity/futures-ticker factor settings, see `Commodities`. Empty (`[]`) by default. |
| `dividend_yield` | `factor-sets/<id>.yaml` | list of sections | No | Opt-in list of dividend-yield ticker factor settings, see `DividendYield`. Empty (`[]`) by default. |
| `dividend_growth` | `factor-sets/<id>.yaml` | list of sections | No | Opt-in list of dividend growth factor settings, a Wilkie (1986) Reduced Basis process on one ticker's dividend index; see [configuration](/projects/financescenarios/docs/configuration)'s Published frameworks section. Each entry requires a paired `inflation[]` entry and a paired `dividend_yield[]` entry. Empty (`[]`) by default. |
| `mortality` | `factor-sets/<id>.yaml` | section | No | Opt-in mortality/longevity factor settings, see `Mortality`. Disabled by default. With `source: supplied` (the default) it needs `mortality_rates`/`mortality_ages` passed to `calibrate()`/`simulate()`; `source: eurostat` fetches a European Economic Area country's life table instead. |

## Multi-instance factors (interest_rates / inflation / unemployment / equities / fx / credit)

Unlike `yield_curve`/`real_estate`/`leading_indicator`/`mortality` (one settings block, one process), `interest_rates`, `inflation`, `unemployment`, `equities`, `fx` and `credit` each become **several** independently calibrated, correlation-linked factors in the simulation, one per configured entry. This is what lets the model represent, e.g., equities as many correlated "clouds" (a broad index, several sector ETFs, several regional ETFs, several style ETFs, ...) rather than a single SPY-driven process, or interest rates as several countries' short-rate clouds rather than one US-only process.

`equities`, `fx` and `credit` are authored as a plain **list**, one block per entry, each fully self-contained:

```yaml
equities:
  - name: us_broad
    ticker: SPY
  - name: tech
    ticker: XLK
  - name: europe
    ticker: VGK

fx:
  - name: eur
    country: Germany
  - name: jpy
    country: Japan

credit:
  - name: ig_7_10y
    dimension: maturity
    maturity_bucket: "7-10 Years"
  - name: high_yield_bb
    dimension: rating
    rating_bucket: BB
```

`interest_rates`, `inflation` and `unemployment` are authored differently, in a **`defaults` + `countries`** shape, since these three usually share the same settings across every country and only differ in a couple of fields (source, term, period):

```yaml
interest_rates:
  defaults:
    source: ticker
    method: hull_white
    ticker: "^IRX"
    period: daily
  countries:
    - name: United States               # inherits every default field
    - name: Eurozone
      source: oecd
      country: Germany
      period: quarterly
    - name: United Kingdom              # country defaults to "United Kingdom"
      source: oecd
      period: quarterly

inflation:
  defaults:
    period: yearly
  countries:
    - name: United States
    - name: Eurozone
      country: Germany
    - name: United Kingdom

unemployment:
  countries:
    - name: United States
    - name: Eurozone
      country: Germany
    - name: United Kingdom
```

Each `countries[]` entry only states what's *different* from `defaults` for that country; every other field is inherited. `name` (e.g. `"Eurozone"`, `"United Kingdom"`) is a display label, not the internal factor name: `ScenariosConfig` resolves it into `<slug(name)>_<inflation|unemployment>` or, for interest rates, `<slug(name)>_<short|long>_rate` (`"Eurozone"` -> `"eurozone_short_rate"`/`"eurozone_inflation"`/`"eurozone_unemployment"`) so it stays unique in the flat cross-factor namespace shared with `equities`/`fx`/`credit` (see below) without you having to type the suffix yourself. `country` (the FinanceToolkit country parameter) defaults to the entry's own `name` when not separately given; only needed when they differ, e.g. `"Eurozone"` has no FinanceToolkit country of that name, so a proxy (`Germany`) must be given explicitly. `unemployment[].countries[].inflation_name` similarly defaults to that same country's own resolved inflation factor name (`"Eurozone"` -> `"eurozone_inflation"`); override it only to pair with a *different* country's inflation entry. This expansion (`_resolve_countries()` in `config_model.py`) happens once at config-load time; every consumer downstream (calibration, simulation, regime overrides) still sees the same flat, fully-resolved `list[InterestRateConfig]`/`list[InflationConfig]`/`list[UnemploymentConfig]` as before, so a config built programmatically (e.g. in a test) can still pass a plain flat list directly for these three fields too, skipping `defaults`/`countries` entirely.

- `interest_rates`/`inflation`/`equities`/`unemployment` are never empty: all four are always-on MVP factors. `fx`/`credit` stay opt-in: an empty list (the default) means neither is simulated, same as the old `enabled: false`.
- Resolved names must be unique within each list, **and globally unique across all six lists combined**: every entry becomes a plain factor name in one flat namespace (`calibrated_params`, `ScenarioSet.paths`, ...), so e.g. an `interest_rates` entry and an `equities` entry can't both resolve to `"japan"`. `ScenariosConfig` raises at load time if this happens; the shipped `factors.yaml` avoids it by construction (`interest_rates`/`inflation`/`unemployment`'s auto-suffixing already disambiguates from `equities`' bare region names like `"japan"`/`"europe"`).
- `unemployment[i].inflation_name` must match a configured `inflation[i].name` (its *resolved* name); it's how an unemployment entry's Phillips-curve term picks which inflation entry to read during simulation (see `Unemployment`).
- `interest_rates`/`equities`/`fx` accept any ticker/country worldwide, not just US ones; see `InterestRates`/`Equities`/`FX` for the shipped default taxonomy (a ticker or OECD-country rate source; US sectors, major world regions, style tilts; major-economy currency pairs).
- `credit` covers the US by default (ICE BofA spreads by `maturity` or `rating`, and Moody's with `dimension: moodys`). Outside the US, `dimension: corporate` reads a country's corporate bond spread over its government bonds: Germany's all-ratings average from the [Bundesbank](https://www.bundesbank.de/en/statistics/money-and-capital-markets) (from 1957), or Australia's A and BBB spreads at 3, 5, 7 and 10 years from the [Reserve Bank of Australia](https://www.rba.gov.au/statistics/tables/) (table F3, from 2005). `dimension: borrowing_cost` reads the [ECB's](https://data.ecb.europa.eu/data/datasets/MIR) composite cost of new bank loans to companies for the euro area or a member (from 2003). That is a rate level rather than a spread, and the broadest free measure of what euro area companies pay to borrow, since most of them borrow from banks. Both are monthly and default `period: monthly`, `country` (Germany, Euro Area) and `currency` (EUR, or AUD for Australia). Set `toolkit.start_date` back to use their long history. See `Credit`.
- Regime YAML (`regimes/<id>.yaml`) addresses one list entry's beliefs with a dotted `"<container>.<name>"` key, using the *resolved* name (e.g. `"equities.tech"`, `"inflation.eurozone_inflation"`); post-simulation `targets:` use the same resolved name (e.g. `"tech"`, `"eurozone_inflation"`), since that's the factor's actual name in the simulated output. See [regimes](/projects/financescenarios/docs/regimes).

## Toolkit section

FinanceToolkit accepts any ticker Financial Modeling Prep or Yahoo Finance carries. A factor-set profile is where most of those tickers live (never hardcoded in the model code), a settings profile's `toolkit.extra_tickers` covers anything without its own dedicated field yet. The tickers a run pulls are every ticker-sourced `interest_rates[i].ticker` and every `equities[i].ticker` (both in `factors.yaml`), the four yield-curve tenor tickers if `yield_curve.enabled`, plus anything listed under `toolkit.extra_tickers`, deduplicated (`ScenariosConfig.tickers`). OECD-sourced interest-rate entries (`source: oecd`) need no ticker, and without a `period` of their own they read monthly (GMDB entries yearly), the finest each source publishes. Every factor's `period` is checked when the configuration loads against what its data source publishes, so a typo or an unavailable frequency (daily CPI, monthly house prices) fails immediately with the allowed values rather than mid-calibration.

| Key | Default | Notes |
|---|---|---|
| `toolkit.start_date` | `null` | Start of the historical data window pulled for calibration. `null` uses FinanceToolkit's own default (5 years back). |
| `toolkit.extra_tickers` | `[]` | Additional tickers beyond `interest_rates[i].ticker`/`equities[i].ticker`, for a factor with no dedicated ticker field yet. |
| `toolkit.benchmark_ticker` | `null` | FinanceToolkit's benchmark ticker. Left `null` by default: FinanceToolkit silently drops a ticker from the list when it matches the benchmark (e.g. the default broad `equities` entry's ticker, `SPY`). |
| `toolkit.progress_bar` | `false` | FinanceToolkit's download progress bar. |

## Belief overrides

Every factor section has a `beliefs` block. A belief lets the user substitute their own view for one specific calibrated parameter, without discarding the rest of the statistical calibration. For example, a user who trusts the calibrated mean-reversion speed and volatility for the interest rate, but has a specific view on where rates are heading long-term, can set just `long_run_mean`:

```yaml
interest_rates:
  - name: interest_rate
    beliefs:
      mean_reversion_speed: null
      long_run_mean: 0.035
      volatility: null
```

Leaving a belief field as `null`, or omitting it entirely, keeps the statistically calibrated value for that parameter. This substitution happens after calibration, in `apply_ou_beliefs` (interest rate, inflation, real estate, credit, leading indicator; every plain OU factor shares this one function), `apply_equity_beliefs` (equity), `apply_unemployment_beliefs` (unemployment), `apply_yield_curve_beliefs` (yield curve, one `OUBeliefs` block per level/slope/curvature factor), `apply_fx_beliefs` (fx, its own shape since it's drift/volatility rather than mean-reversion) and `apply_mortality_beliefs` (mortality, one `RandomWalkBeliefs` block per kappa1/kappa2 factor; the same drift/volatility shape as fx, since neither is mean-reverting), all in `config_model.py`.

Belief overrides don't apply when a factor's `volatility_model` is `"garch"` (see below): `GARCHParams`' omega/alpha/beta shape doesn't map onto the constant-volatility `OUBeliefs` fields, so a GARCH-calibrated factor is used as calibrated, unmodified, in v1.

## Belief paths (a term structure of beliefs)

`long_run_mean` on any `OUBeliefs`-shaped factor (each `interest_rates[i]`, each `inflation[i]`, `real_estate`, each `credit[i]`, `leading_indicator`, each of `yield_curve.beliefs.level`/`slope`/`curvature`) or `UnemploymentBeliefs` accepts either a constant number (the substitution described above) or a `BeliefPath`: a set of target values at several future horizons, interpolated between them rather than fixed for the whole run. For example, believing rates rise toward 6% within 5 years before easing back to 2% by year 10:

```yaml
interest_rates:
  - name: interest_rate
    beliefs:
      long_run_mean:
        anchors:
          5.0: 0.06
          10.0: 0.02
```

`resolve_belief_path()` (`calibration_model.py`) resolves the sparse `anchors` (horizon in years from `start_date` -> target value) onto every point of the simulated time grid by linear interpolation, holding flat before the first anchor: the mean-reversion target the OU process pulls toward moves over the simulated horizon instead of staying fixed. `mean_reversion_speed` still governs how fast the process actually catches up to that moving target at any given point; a belief path states the target, not how quickly it's reached.

**After the last anchor**, the default is the same flat hold as before the first: the target stays pinned at the last anchor's value forever. Set `converge_over_years` to change that: the target instead keeps moving past the last anchor, converging linearly to the factor's own *statistically calibrated* `long_run_mean` over that many years, then holding flat there:

```yaml
inflation:
  - name: inflation
    beliefs:
      long_run_mean:
        anchors:
          5.0: 0.02
          10.0: 0.025
        converge_over_years: 5.0 # by year 15 (10 + 5), the target has moved on to the
        # calibrated long_run_mean and holds there, not pinned at 0.025 forever
```

`converge_over_years` is implemented as one implicit extra anchor, placed `converge_over_years` years past the last explicit anchor with the calibrated `long_run_mean` as its value; the same `np.interp` linear interpolation handles it, no separate code path. This converges to the factor's *raw calibrated* `long_run_mean`, not to whatever `ScenarioSet.calibration_metadata[factor].long_run_mean` reports (see the terminal-value caveat below); those are deliberately different numbers.

Two things to watch:

- **Units are one convention: an annualized decimal rate for every rate-type factor (`0.06` means 6% a year), a price level for equities/fx/commodities.** Sources that don't arrive that way are converted at the fetch. See [units](/projects/financescenarios/docs/units) for the full statement, including which conversion each source needs and how belief anchors follow from it. Check `scenarios.calibrate().describe()` for the exact level a belief anchor is displacing.
- **Only for constant-volatility, non-covariate-conditioned factors**, same restriction as GARCH above: a belief path is ignored (falls back to the plain belief/calibrated behavior) when combined with `volatility_model: "garch"` or `condition_on_business_cycle: true`, to avoid a three-way hybrid step function. `ScenarioSet.calibration_metadata[factor].long_run_mean` reflects the belief path's *terminal* (furthest-explicit-anchor) value as a single-number summary (e.g. for `diagnose()`'s theoretical stationary-distribution check), even though the actual simulated target moved further than that when `converge_over_years` is set. The `raw_long_run_means` field on a saved/loaded `CalibrationResult` carries the true calibrated value `converge_over_years` actually converges to, separately from this summary.

`fx`/`mortality` (geometric Brownian motion / random-walk-with-drift families) have no `long_run_mean`: there's no mean-reversion target for a belief path to move, so they're not supported.

## Shocks (one-off jumps)

`shocks` on any `OUBeliefs`-shaped factor or `UnemploymentBeliefs` is a list of one-off perturbations to the *simulated value*, independent of `long_run_mean`/belief paths: each shock jumps the process's level once, at a specific year, after which its own calibrated dynamics (mean-reversion, volatility, and any active belief-path target) continue unmodified from the shocked level. Not a deterministic path, a one-time jump in initial conditions mid-run.

```yaml
inflation:
  - name: inflation
    beliefs:
      shocks:
        - year: 2.0        # +3pp jump at year 2, then normal dynamics resume
          magnitude: 0.03
          mode: additive
```

Each shock has `year`, `magnitude`, and `mode`: `year` (>= 0) is snapped to the nearest simulated time-grid step; `magnitude` is added to (`mode: "additive"`, the default) or replaces (`mode: "absolute"`) the process's own step output at that point. Two shocks on the same factor that round to the same step raise a `ValueError`; making it unambiguous which one should apply is left to the user, not resolved by "last one wins". Shocks apply regardless of `volatility_model`/`condition_on_business_cycle`, since they act on the final numeric value, not the drift mechanism that produced it, unlike belief paths, which are constant-volatility/non-conditioned only.

Equities take `shocks` too (`EquityBeliefs.shocks`), as one-off log-returns: a shock of `magnitude` multiplies the price at its year by `exp(magnitude)`, so `-0.4` takes the price about 33% lower and the price then grows on from there. Equity shocks must use `mode: "additive"`, since replacing a price outright has no meaning across currencies or indices. This is how `stress_test_regime` moves stocks.

## Time-varying volatility (GARCH)

Each `interest_rates[i]`, `inflation[i]`, `real_estate`, `credit[i]`, `leading_indicator`, `commodities[i]` (`method: "single_factor"` only) and `dividend_yield[i]` entry accepts `volatility_model: "constant"` (the default, a fixed-volatility OU process stepped via its exact discrete-time transition, see [simulation-engine](/projects/financescenarios/docs/simulation-engine)) or `volatility_model: "garch"` (a GARCH(1,1) conditional-variance process, Bollerslev 1986, replacing the fixed volatility with one that clusters over time: calm periods stay calm, volatile periods stay volatile). `volatility_model: "garch"` on an interest-rate entry additionally requires `method: "hull_white"` on that same entry: CIR's own square-root diffusion scaling is a different, incompatible volatility specification.

```yaml
interest_rates:
  - name: interest_rate
    method: hull_white
    volatility_model: garch
```

Internally, a GARCH-calibrated factor's calibrated parameters are `GARCHParams` (`calibration_model.py`) instead of `OUParams`, and its simulation step is a stateful `GARCHStepper` instead of the plain step function; see [simulation-engine](/projects/financescenarios/docs/simulation-engine).

## Business-cycle conditioning

Each `interest_rates[i]`, `inflation[i]`, `real_estate`, `credit[i]`, `commodities[i]` (`method: "single_factor"` only) and `dividend_yield[i]` entry accepts `condition_on_business_cycle: true`, an additive drift term on the leading indicator's step-to-step change, the same shape `Unemployment`'s Phillips-curve term already uses for inflation, generalized via `calibration_model.OUCovariateParams`. Requires `leading_indicator.enabled: true`; enabling it on an entry forces that entry's calibration onto `leading_indicator.period` rather than its own configured `period` (the covariate regression needs both series date-aligned at the same frequency), and is incompatible with `volatility_model: "garch"` on the same entry. `dividend_yield[i]` also treats it as mutually exclusive with `condition_on_inflation: true` (a different, log-space covariate mechanism; see `DividendYield`). See `LeadingIndicator` for the full treatment, including which `leading_indicator.period` values each factor's own sampling frequency actually supports.

```yaml
leading_indicator:
  enabled: true
  period: yearly

inflation:
  - name: inflation
    condition_on_business_cycle: true
```

Belief overrides don't apply to a conditioned factor either (`OUCovariateParams`' shape doesn't map onto `OUBeliefs`): used as calibrated, unmodified, same as GARCH-calibrated factors above.

## Published frameworks

A framework is a complete, published recipe for how the variables relate to each other. Each one ships as a ready-made factor set, so you can run a paper's own model specification instead of assembling one, and compare frameworks on the same engine.

Every component documents its own models in its class docstring (for example `InterestRates`, `Inflation`, `Equities`); a framework is just a curated combination of each component's `method` choice:

| Factor set | Framework | How the variables are linked |
|:-----------|:----------|:-----------------------------|
| `ahlgrim.yaml` (and the default) | [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf) | Each variable is its own process; inflation feeds rates and unemployment, and everything is tied together through the estimated correlation matrix. |
| `wilkie.yaml` + `settings/wilkie.yaml` | [Wilkie (1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf) | A one-way cascade: inflation is simulated first and dividend yields, long bond yields, dividend growth and share prices are each a direct function of it. |
| `hibbert.yaml` | [Hibbert, Mowbray and Turnbull (2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf) | Fast-moving rates and inflation mean-revert to a second, slowly moving target rather than to a fixed level; equities switch between two market regimes. |
| any set using `method: knw` / `knw_sv` | [Koijen, Nijman and Werker (2010)](https://doi.org/10.1093/rfs/hhp058) | Interest rate and inflation drive each other in both directions (a VAR), optionally with shared stochastic volatility; the basis of De Nederlandsche Bank's scenario sets. |

Wilkie's cascade, in the order it is simulated:

```
inflation (wilkie_ar1)
    |-- dividend yield (condition_on_inflation: true)
    |-- consols yield  (wilkie_consols)
         |
dividend growth (reads dividend yield's own lagged residual)
    |
share price = dividend growth index / dividend yield  (wilkie_derived)
```

These are real functional dependencies, registered in `Scenarios._build_dependency_graph()`, not correlations.

A few rules apply across frameworks:

- **Discrete recursions need a matching frequency.** `wilkie_ar1`, `wilkie_consols`, `knw` and `knw_sv` are fitted and stepped as discrete-time recursions with no time step to rescale, so `engine.frequency` must equal those entries' `period`; `ScenariosConfig` rejects a mismatch.
- **Wilkie needs a capped history.** Its consols model assumes the inflation-adjusted long yield stays positive, which the 2020-2022 era broke; `settings/wilkie.yaml` caps `toolkit.end_date` so the fit uses 1995-2019. `hibbert.yaml` needs no such pairing.
- **Scope.** Wilkie's set populates rates, inflation, equities, dividend yield and dividend growth, plus the one unemployment entry every run requires. Hibbert's prescribed fixed cross-factor correlations are not replicated (every framework estimates correlations from data), and neither is its closed-form bond pricing. Hibbert's methods are real-world only.

## Long history

Today tells the model where things are; history tells it how they move. A calibration window of 25 years misses the inflation of the 1970s, the deflation of the 1930s and the wars, so for a run of 50 to 100 years it understates how far rates, inflation and markets can travel. `history_source` learns *how they move* from 75 to 800 years of data instead, while the run still *starts* from today's values.

Set on an entry, `history_source` fits that entry's dynamics on long history: an interest rate's or inflation's speed of mean reversion, volatility and long-run level, or an equity market's calm and crisis regimes. Today's starting value and the series behind the correlation matrix still come from the entry's usual `source`/`ticker`, so every factor's correlation is estimated over the same recent window (`long_history_controller.LongHistory`).

| Factor | `history_source` | Data | From |
|:-------|:-----------------|:-----|-----:|
| `equities` (`regime_switching`) | `shiller` | [Shiller's](https://shillerdata.com/) S&P Composite total return, monthly, US | 1871 |
| `equities` (`regime_switching`) | `jst` | Yearly equity total return of `history_country`, [Jordà-Schularick-Taylor](https://doi.org/10.1093/qje/qjz012) | 1870 |
| `interest_rates` (`hull_white`, `cir`) | `oecd` | The OECD's short-term (`term: short`) or long-term (`term: long`) rate of `country`, yearly, the same series `source: oecd` uses recently | 1950 |
| `interest_rates` (`hull_white`, `cir`) | `millennium` | Bank Rate (`term: short`) or long government bond (consols) yields (`term: long`), yearly, `country: United Kingdom` ([Bank of England](https://www.bankofengland.co.uk/statistics/research-datasets)) | 1694 |
| `interest_rates` (`hull_white`, `cir`) | `jst` | Yearly return on short-term government bills of `country` (`term: short` only) | 1870 |
| `inflation` (`ou`) | `millennium` | UK consumer price inflation, yearly | 1209 |
| `inflation` (`ou`) | `shiller` | US December-to-December inflation from Shiller's price index | 1872 |

- `history_volatility: recent` (interest rates) keeps the volatility fitted on the recent window and takes only the speed of mean reversion and the long-run level from the long history: recent data pin down how much a rate swings well, decades are needed to see how fast it reverts.
- `history_start_year` leaves out earlier years. Usually you want one: from 1209 UK inflation swings 21% a year with medieval harvests, and from 1870 German equities include the 1923 hyperinflation.
- The JST database is licensed [CC BY-NC-SA 4.0](https://www.macrohistory.net/database/) for non-commercial use, so `history_source: jst` needs `accept_licence: true` on the entry.
- Only the latest unbroken stretch of a JST series is used, since chaining across missing war years would count them as zero returns.
- It applies to real-world entries with constant volatility and no business-cycle conditioning. Other combinations raise when the configuration loads.

The window matters most for interest rates, whose recent decades alone barely pin down a long-run level: on 2000-2026 data the US short rate settles at 5.3% while the 10-year settles at 3.2%, an inverted curve in the long run, and from 2010 the fitted short-rate level is 45%. Fitted on the OECD's yearly rates since 1950 (`history_source: oecd`) every curve slopes upward (US 4.5% short and 6.0% long, Germany 4.1% and 4.5%, the UK 6.2% and 7.0%), at higher levels than either regulator's scenarios use (the NAIC's US 10-year median about 4.5%, DNB's euro 10-year about 1.8% at 30 years); from 1970 Germany's curve inverts again.

Live on 2026-10-07, the `us_only` set's short rate fitted on JST bills from 1950 reverts with a 7-year half-life and 1.6% volatility, against 18 years and 0.7% on the recent window. US inflation from Shiller since 1950 settles at 3.4% instead of 2.7%. US equities' crisis regime averages -14% a year instead of +0.6%.

## Keeping rates at or above zero

The default rate models let rates go below zero, as euro, Swiss franc and yen rates did in the 2010s. Some scenario generators cut rates off at 0% instead. `zero_lower_bound: true` on an interest-rate entry does that, the shadow-rate way.

The model keeps evolving underneath as a shadow rate that may go negative, and the rate every path, discount factor and linked factor sees is the larger of the shadow and 0% ([Black, 1995](https://doi.org/10.1111/j.1540-6261.1995.tb05182.x)). A rate that sat at zero therefore climbs back from wherever the shadow went, the way policy rates lingered at zero for years, rather than bouncing off 0% the moment the pressure eases. It is off by default and for real-world entries only, since a floor breaks a risk-neutral rate's exact fit to today's curve. Today's rate is floored too when it is negative; CIR rates are positive anyway.

## Anchoring long-run rate levels

A rate model pulls each simulated rate toward a long-run level. Fitted on recent decades that level is barely identified (the US short rate settles at 5.3% while the 10-year settles at 3.2%, an inverted curve for decades), so official scenario sets fix it instead: EIOPA's risk-free curves, which every Solvency II insurer discounts with, end at the [ultimate forward rate](https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en).

`long_run_anchor: eiopa` on an interest-rate entry replaces its single fitted long-run level by a path: the forward rate of its maturity (1 year for `term: short`, 10 years for `term: long`) starting at each scenario year, read off EIOPA's latest curve for the entry's `currency` (USD, EUR or GBP). The path starts near today's curve and ends at the ultimate forward rate; speed and volatility stay fitted. `long_run_anchor: dnb` (euro entries only) follows the median path of [De Nederlandsche Bank's](https://www.dnb.nl/voor-de-sector/open-boek-toezicht/sectoren/pensioenfondsen/) real-world scenario set instead (its 1-year or 10-year nominal rate), the reference Dutch pension funds must use; it is a Dutch-market choice, so EIOPA stays the general one. DNB's workbook is parsed in a separate short-lived process (about a minute, near 900 MB there, nothing kept in the calling process). Calibration stores the path (`CalibrationResult.long_run_anchors`), so a saved calibration replays without fetching it again, and an explicit `beliefs.long_run_mean` still wins. Live on 2026-10-07 the `core` rates anchored this way slope upward through 10 years (US 4.1%/5.2% short/long in year 1), the US 10-year median of 5.2% falling to 4.1% by year 30 against the NAIC generator's 5.3% to 4.5%, while the euro 10-year median of 3.4% at 30 years sits above DNB's 1.8%: the two official sources disagree on the euro's long run.

## Real-world and risk-neutral measures

The same economy can be simulated for two jobs. A *real-world* run follows how markets have actually behaved and answers "what could happen?". A *risk-neutral* run is adjusted so that every investment grows on average at the risk-free rate, which makes it reproduce today's market prices and answers "what is this worth today?".

Every factor calibrates real-world by default. Each entry that supports it opts in separately with `measure: "risk_neutral"`; there is no single switch, because several factors have no meaningful risk-neutral version in this project.

| Factor | Risk-neutral version | Documented in |
|:-------|:---------------------|:--------------|
| Equities | Drift = risk-free rate minus dividend yield; volatility from option prices (`implied`, `svi`) or history (`realized`), or (`volatility_source: heston`) a stochastic volatility fitted to the whole option surface | `Equities.calibrate_risk_neutral`, `calibrate_heston` |
| Interest rates | Today's observed rate held flat, or (`risk_neutral_forward_curve: true`) a Hull-White rate whose expected path reproduces today's forward curve | `InterestRates.calibrate_risk_neutral`, `calibrate_risk_neutral_forward` |
| FX | Drift set by covered interest-rate parity, the gap between the two countries' interest rates | `FX.calibrate_risk_neutral` |
| Inflation (`method: ou`; United States, United Kingdom, Germany or Euro Area) | A forward curve fitted to breakeven inflation: US TIPS, UK index-linked gilts (RPI) or German inflation-linked federal bonds (euro area HICP) | `Inflation.calibrate_risk_neutral` |
| Inflation and rates (`method: knw_sv`) | A completely-affine market price of risk fitted to the yield curve | `KnwSvQ` |
| Commodities (`method: schwartz_smith`) | The two-factor model's risk-neutral leg, fitted to the futures curve | `Commodities` |
| Unemployment, real estate, leading indicator, mortality, credit | Not supported: no tradeable market price to match | |

This is a first version, not a full market-consistent engine: volatility is a single number rather than a smile- or skew-consistent surface, except for an equity with `volatility_source: heston`. That entry fits the Heston ([1993](https://doi.org/10.1093/rfs/6.2.327)) model to the volatility smile at six expirations from one to twelve months, so its paths price options across strikes and maturities close to the market (on SPY, within half a volatility point). Interest-rate volatility still comes from history: the one published rates-volatility index, ICE's MOVE, is a single number, which cannot pin down both the speed and the size of the Hull-White model's swings. **Belief overrides cannot be combined with `measure: "risk_neutral"`**: a risk-neutral calibration exists to match a market input exactly, and replacing that input with a belief would undo it, so a non-empty `beliefs` block on such an entry raises at configuration time (`config_model._validate_no_beliefs_when_risk_neutral`). Risk-neutral runs are what the Solvency II functions in `financescenarios.solvency` value liabilities with.

## Example files

`settings/default.yaml`, run settings only:

```yaml
name: Default
description: "2,000 scenarios, one step a month, five years ahead, fitted on history since 2000."

start_date: 2026-01-01

engine:
  n_simulations: 2000
  n_steps: 60
  frequency: monthly # daily | weekly | monthly | quarterly | semi-yearly | yearly
  seed: 42
  antithetic: false # variance reduction via paired +/- shocks; n_simulations must be even if true
  correlation_shrinkage: auto # data-driven (Schafer-Strimmer); a number in [0, 1] for a fixed blend
  shared_equity_regimes: true # equities switch calm/crisis regimes on one shared random stream
  # shock_distribution: student_t  # optional, gaussian by default; degrees_of_freedom: 5.0 sets its tails

toolkit:
  start_date: 2000-01-01 # history window pulled for calibration
  extra_tickers: [] # tickers beyond interest_rate.ticker/equity.ticker, e.g. for a future factor
  benchmark_ticker: null # avoids FinanceToolkit silently dropping a ticker that matches the benchmark
  progress_bar: false
```

`factor-sets/default.yaml` is the curated set behind every run that names no factor set: `core.yaml` (the United States, the euro area and the United Kingdom with monthly or quarterly data, global equities, gold, oil, the major currencies) with each interest rate's long-run level anchored to EIOPA's forward rates and its speed and volatility fitted on the OECD's rates since 1950 (see Anchoring long-run rate levels). Benchmarked over 30 years on 2026-10-07, its US 10-year median ends at 4.8% against 4.5% in the NAIC's generator (built by Conning), with a similar 5-95% range, and it passes every release check. `factor-sets/broad.yaml` is this project's expansive showcase: every opt-in factor category turned on, broadest built-in breadth, not tied to any one paper (see Published frameworks above for the frameworks and methods it's built on). `factor-sets/ahlgrim.yaml` (Ahlgrim/D'Arcy/Gorvett 2005, this project's original framework, selectable by that name directly) is scoped instead to the paper's own six factors, single country/instrument each, close to the illustration below, not a byte-for-byte copy:

```yaml
name: Ahlgrim-style illustration (see factor-sets/ahlgrim.yaml for the real file)
description: Ahlgrim/D'Arcy/Gorvett (2005)-style factor definitions.

interest_rates: # at least one entry required; each becomes its own correlated interest-rate "cloud"
  - name: interest_rate
    source: ticker # ticker (Yahoo, US-only in practice) | oecd (country-parameterized, worldwide)
    method: hull_white # hull_white | cir
    ticker: "^IRX" # ^IRX 13-week | ^FVX 5-year | ^TNX 10-year | ^TYX 30-year
    period: daily
    beliefs:
      mean_reversion_speed: null
      long_run_mean: null
      volatility: null
  # - name: eurozone_short_rate
  #   source: oecd
  #   country: Germany
  #   term: short
  #   period: quarterly

inflation: # at least one entry required; each becomes its own correlated inflation "cloud"
  - name: inflation
    country: United States
    period: yearly
    beliefs:
      mean_reversion_speed: null
      long_run_mean: null
      volatility: null
  # - name: eurozone_inflation
  #   country: Germany

equities: # at least one entry required; each becomes its own correlated equity "cloud"
  - name: equity
    ticker: SPY
    n_regimes: 2
    period: monthly
    beliefs:
      regime_means: null
      regime_volatilities: null
  # - name: tech # add more entries for sector/region/style clouds
  #   ticker: XLK

unemployment: # at least one entry required; each becomes its own correlated unemployment "cloud"
  - name: unemployment
    country: United States
    inflation_name: inflation # which inflation[i].name entry drives this entry's Phillips-curve term;
    # sampled at that entry's period, the two series must align
    beliefs:
      mean_reversion_speed: null
      long_run_mean: null
      inflation_sensitivity: null
      volatility: null
  # - name: eurozone_unemployment
  #   country: Germany
  #   inflation_name: eurozone_inflation

yield_curve:
  enabled: false
  period: daily
  decay: 0.7308
  beliefs:
    level:
      mean_reversion_speed: null
      long_run_mean: null
      volatility: null
    slope:
      mean_reversion_speed: null
      long_run_mean: null
      volatility: null
    curvature:
      mean_reversion_speed: null
      long_run_mean: null
      volatility: null

real_estate:
  enabled: false
  country: United States
  period: yearly
  beliefs:
    mean_reversion_speed: null
    long_run_mean: null
    volatility: null

credit: [] # opt-in list, empty = none simulated. Example entry (see Multi-instance factors above):
  # - name: credit
  #   dimension: maturity # maturity | rating | moodys | corporate | borrowing_cost
  #   country: null # corporate: Germany | Australia; borrowing_cost: Euro Area or a member
  #   maturity_bucket: "7-10 Years"
  #   rating_bucket: BBB
  #   period: daily
  #   beliefs:
  #     mean_reversion_speed: null
  #     long_run_mean: null
  #     volatility: null

leading_indicator:
  enabled: false
  country: United States
  period: monthly
  beliefs:
    mean_reversion_speed: null
    long_run_mean: null
    volatility: null

fx: [] # opt-in list, empty = none simulated. Example entry (any worldwide country):
  # - name: eur
  #   country: Germany
  #   period: monthly
  #   beliefs:
  #     drift: null
  #     volatility: null

mortality:
  enabled: false # requires mortality_rates/mortality_ages passed to calibrate()/simulate() directly
  period: yearly
  beliefs:
    kappa1:
      drift: null
      volatility: null
    kappa2:
      drift: null
      volatility: null
```

## Secrets

Neither a settings profile nor a factor-set profile ever holds API keys. Pass them when you create the scenarios, as the Finance Toolkit's `Toolkit` takes them: `Scenarios.from_profiles(..., api_key="...", fred_api_key="...")` (`from_config()` and `build_toolkit()` take the same two). A key left out is read from the `FINANCIAL_MODELING_PREP_API_KEY`/`FRED_API_KEY` environment variables, loading a `.env` file (excluded from version control) automatically if one is present in the folder Python runs from or a folder above it. `scaffold_project()` (see the [README](/projects/financescenarios#starting-your-own-project)) writes a `.env` template carrying this same breakdown.

Both keys are optional to start: most factors calibrate against free OECD or Yahoo Finance data and need neither:

| Factor(s) | Key needed | Why |
|---|---|---|
| `inflation` (default `method="ou"`/`"wilkie_ar1"`), `unemployment`, `fx`, `leading_indicator`, `real_estate` (default `source="growth"`), `interest_rates` with `source: oecd` | none | OECD-sourced, no key required by FinanceToolkit at all. |
| `equities`, `dividend_yield`, `dividend_growth`, `yield_curve`, `hjm`, `commodities`, `knw_sv_q`, `interest_rates` with a ticker source | FMP, optional | Ticker price history: FMP gives the full universe (non-US exchanges, cleaner dividend data); without a key FinanceToolkit falls back to Yahoo Finance automatically (US exchanges only). |
| `credit` | FRED, required | ICE BofA option-adjusted spreads are FRED-published; there's no keyless alternative. |
| `real_estate` with `source: commercial` | FRED, required | US commercial real-estate prices come from FRED (IMF-sourced), unlike the default OECD-sourced `source: growth`. |
| `inflation` with `method: hibbert_two_factor` and `target_source: breakeven` | FRED, required | Pulls FRED's daily TIPS-breakeven series for that target-fit path only; the default target sources don't need it. |
| `mortality` | neither | Eurostat life tables through the Finance Toolkit (`source: eurostat`, no key), or rates supplied via `calibrate(mortality_rates=...)`; see `Mortality`. |
