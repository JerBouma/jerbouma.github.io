---
title: Markets and Credit
seo_title: Markets and Credit Documentation – Finance Scenarios
excerpt: "How Finance Scenarios simulates equities, exchange rates, commodities, real estate, dividends, credit spreads and rating migration: the models, the data behind them, when to use each and where they stop."
description: "How Finance Scenarios models equities, FX, commodities, real estate, dividends, credit spreads and rating migration, with data sources and limits."
author_profile: false
permalink: /projects/financescenarios/docs/markets
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

This page covers the factors that describe markets: equity indices, exchange rates, commodities, real estate, dividends, credit spreads and rating migration. Each one is fitted to its own history, becomes one or more named variables in the scenarios, and moves together with everything else through the shared correlation matrix (see [simulation engine](/projects/financescenarios/docs/simulation-engine)). Interest rates, inflation and unemployment have their own pages: [interest rates](/projects/financescenarios/docs/interest-rates) and [economy](/projects/financescenarios/docs/economy).

For each factor you will find what it does, when to use it, what it assumes and where its data comes from. Every factor is set in a factor set (see [configuration](/projects/financescenarios/docs/configuration)), and most accept beliefs: overrides of a fitted parameter that replace history with your own view. Every method and parameter is in the [API reference](/projects/financescenarios/docs/reference).

## Equities

Use this factor for anything that holds shares: a broad index, a sector, a region, a style, or a listed proxy for private markets.

### Regime Switching (the Default)

Markets alternate between calm stretches with steady gains and turbulent stretches with losses and large swings. The default regime-switching lognormal model of [Hardy (2001)](https://doi.org/10.1080/10920277.2001.10595984){:target="_blank"} fits two regimes (or more, with `n_regimes`) from the ticker's price history: each regime has its own annual mean return and volatility, plus the chance of staying in it or switching to another each period.

The regimes are estimated with the Baum-Welch algorithm ([Baum et al., 1970](https://doi.org/10.1214/aoms/1177697196){:target="_blank"}), and the simulation starts in the regime most likely at the last observation. SPY calibrated from 2005 on 2026-10-04 gave:

| Regime | Annual mean | Annual volatility | Average stay |
|:-------|------------:|------------------:|-------------:|
| Turbulent | -0.1% | 20.2% | about 8 months |
| Calm | 18.5% | 7.9% | about 10 months |

Each step the price moves by `next = current * exp(mean * dt + volatility * sqrt(dt) * shock)`, using the active regime's mean and volatility. Transition probabilities are rescaled to the simulation step ([Israel, Rosenthal and Wei, 2001](https://doi.org/10.1111/1467-9965.00114){:target="_blank"}), so a monthly fit simulated weekly keeps the right time in each regime. You can list as many equities as you like, each with its own regime path:

```yaml
equities:
  - name: us_broad
    ticker: SPY
    n_regimes: 2
    period: monthly
  - name: europe
    ticker: VGK
  - name: emerging_markets
    ticker: EEM
```

With the engine setting `shared_equity_regimes: true` (on in the shipped settings), every market draws its switches from one shared stream, so markets tend to enter and leave crises together while keeping their own fitted probabilities.

Any ticker the Finance Toolkit holds works. A fit needs at least `n_regimes * 5` price observations and warns below `n_regimes * 20`, or when a regime is visited less than 2% of the time; fewer regimes or a longer window helps. The `currency` field is the listing currency only: VGK and EWJ are US-dollar ETFs that track markets outside the US.

For private equity, infrastructure, hedge funds or private credit, set `asset_class` instead of a ticker, and the entry uses a listed fund as a proxy. Listed prices swing more, and move more with equities, than the appraisal-based returns private funds report.

Beliefs override the fitted `regime_means` or `regime_volatilities`, one value per regime, and `shocks` add one-off jumps to the price (a log-return, so `-0.3` is about a 26% fall). What the model leaves out: within a regime, returns are normal in log terms, so there are no extra-heavy tails inside a regime, and there is no volatility smile or skew in the real-world process.

### Linking Regimes to the Business Cycle

With `condition_on_business_cycle: true`, the chance of switching regime depends on the leading indicator's level, following [Filardo (1994)](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}. For SPY, the chance of leaving the calm regime in a month rose from 5.8% at an indicator of 105 to 8.9% at 95, so a weakening economy shortens calm stretches from about 17 to 11 months. This needs `leading_indicator.enabled: true` and the default `regime_switching` method. The fit is the common two-step version of [Diebold, Lee and Weinbach (1994)](https://doi.org/10.1093/oso/9780198773917.003.0010){:target="_blank"}.

### Long Histories: Shiller and JST

For runs of 50 to 100 years, a window starting in 2005 misses the 1930s, the wars and the 1970s. With `history_source`, the regimes are fitted on a much longer total-return history instead, while today's price and the series used for correlations still come from the ticker.

| `history_source` | Data | Frequency | From |
|:-----------------|:-----|:----------|-----:|
| `shiller` | [Shiller's](https://shillerdata.com/){:target="_blank"} S&P Composite total return, US | Monthly | 1871 |
| `jst` | Equity total return of one of 18 countries, [Jordà-Schularick-Taylor](https://doi.org/10.1093/qje/qjz012){:target="_blank"} | Yearly | 1870 |

```yaml
equities:
  - name: uk_equity
    ticker: EWU
    history_source: jst
    history_country: United Kingdom
    history_start_year: 1950
    accept_licence: true
```

The JST database is licensed for non-commercial use only (CC BY-NC-SA 4.0), so it needs `accept_licence: true`. Where a country has gaps in war years, only the latest unbroken stretch is used. Long history works with real-world `regime_switching` entries without business-cycle conditioning.

### Hibbert: Returns Above Cash

`method: hibbert_regime_switching` fits the same two regimes, but on returns in excess of a short rate, as in [Hibbert, Mowbray and Turnbull (2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"}. When simulating, the equity reads the simulated short rate and adds it back, so equity returns rise and fall with rates. Against the 13-week Treasury bill, SPY's calm regime earned 16.5% a year above cash and its turbulent regime 1.5% below it.

```yaml
equities:
  - name: equity
    ticker: SPY
    method: hibbert_regime_switching
    nominal_rate_name: short_rate
```

The rate and the price must share a `period`. This is the equity leg of the shipped `hibbert` factor set; the paper's fixed cross-factor correlations are not copied.

### Wilkie: Price From Dividends

`method: wilkie_derived` has no fit of its own: the price is the simulated dividend index divided by the simulated dividend yield, the last link of [Wilkie's (1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf){:target="_blank"} cascade. See [Dividend Yield and Dividend Growth](#dividend-yield-and-dividend-growth) below. It needs `dividend_growth_name` and `dividend_yield_name`, ignores `ticker`, `n_regimes` and `period`, and takes no beliefs.

### KNW: Shared Stochastic Volatility

`method: knw_sv` ties the equity's drift to a nominal short rate plus a constant risk premium, and scales its variance by the same volatility factor that the paired rate and inflation share. It belongs to the KNW family of models used for Dutch pension scenarios; see [KNW models](/projects/financescenarios/docs/knw).

### Risk-Neutral Equities

Use `measure: risk_neutral` when you value options or guarantees and need prices consistent with today's market, not a forecast. Under this measure the expected return is the risk-free rate minus the dividend yield, whatever history says. The process is a geometric Brownian motion (GBM), a lognormal random walk with one constant volatility, in the spirit of [Black and Scholes (1973)](https://doi.org/10.1086/260062){:target="_blank"} and [Merton (1973)](https://doi.org/10.2307/3003143){:target="_blank"}:

`d(log S) = (r - q - 0.5 * sigma^2) dt + sigma dW`

`r` is the current level of the first `interest_rates` entry, and `q` the last yield of the `dividend_yield` entry with the same ticker; without one, the equity's calibration fails rather than assume a zero yield. Where the volatility comes from is set by `volatility_source`:

| `volatility_source` | Where sigma comes from | Good for |
|:--------------------|:-----------------------|:---------|
| `implied` (default) | At-the-money implied volatility of one expiration, at least a week out | Liquid index options |
| `svi` | At-the-money point of the Finance Toolkit's fitted volatility surface ([Gatheral and Jacquier, 2014](https://doi.org/10.1080/14697688.2013.819986){:target="_blank"}), longest expiry | Smoothing out single-quote noise |
| `realized` | Standard deviation of historical returns | ETFs without a liquid options market |
| `heston` | The [Heston (1993)](https://doi.org/10.1093/rfs/6.2.327){:target="_blank"} stochastic-volatility model, fitted to the surface at six expirations from one to twelve months | Keeping the smile and term structure |

When options data is missing, `implied`, `svi` and `heston` fall back to `realized` with a warning. For SPY on 2026-10-04, with a 3.99% bill rate and a 1.15% dividend yield, the drift was 2.84% and the four sources agreed within about three points (13.5% to 16.2%).

```yaml
equities:
  - name: us_broad
    ticker: SPY
    measure: risk_neutral
    volatility_source: svi
dividend_yield:
  - name: spy_yield
    ticker: SPY
```

Beliefs are rejected on a risk-neutral entry, since a market-consistent fit must match market prices exactly. `hibbert_regime_switching`, `wilkie_derived` and `knw_sv` have no risk-neutral version. Reference: [Equities API](/projects/financescenarios/docs/reference/equities).

## FX

Use this factor when a portfolio holds foreign assets, or when you want results in another reporting currency.

An exchange rate has no natural long-run level to return to over decades, so unlike rates or spreads it does not mean-revert. Each pair is a geometric Brownian motion against the US dollar, the standard treatment surveyed by [Gorvett (2001)](https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf){:target="_blank"}. Rates are quoted as foreign currency per dollar. The fit is closed-form: volatility is the standard deviation of log changes, drift their mean, and the simulation uses the exact solution, so the rate stays positive.

The trend is set by `drift_mode`:

| `drift_mode` | Drift | When to use it |
|:-------------|:------|:---------------|
| `historical` (default) | The sample's own average change | Short horizons, or when you trust the window's trend |
| `random_walk` | None: the median stays at today's rate | Long horizons; [Meese and Rogoff (1983)](https://doi.org/10.1016/0022-1996(83)90017-X){:target="_blank"} found a random walk forecasts at least as well as structural models |
| `irp` | Each step, the gap between the two simulated short rates | When currency moves should follow rate differentials (uncovered interest parity) |

The shipped `default` factor set uses `random_walk`. With `irp`, the higher-rate currency depreciates by roughly the rate gap, so a higher US rate pushes the euros-per-dollar quote down. It needs `domestic_rate_name`; `foreign_rate_name` defaults to the country's slug plus `_short_rate`.

```yaml
fx:
  - name: eur
    country: EA20
    period: monthly
    drift_mode: irp
    domestic_rate_name: united_states_short_rate
    foreign_rate_name: eurozone_short_rate
```

Data comes from the OECD through the Finance Toolkit, no API key needed, for the major economies. It is keyed by currency area, so the euro is `EA20`, not `Germany`. For countries outside the OECD set, `source: gmdb` uses the Global Macro Database, yearly only.

`measure: risk_neutral` sets a fixed drift of foreign minus US short rate once at calibration (covered interest parity), read from the run's own interest-rate entries for both countries. Volatility stays historical, since there is no FX options source. Reference: [FX API](/projects/financescenarios/docs/reference/fx).

## Commodities

Use this factor for oil, gas, metals or grains, either as holdings or as an inflation and cost driver.

Unlike a stock index, a commodity price is pulled back toward a level set by the economics of production and storage. Storage costs and the convenience yield (the benefit of holding the physical good) do the pulling, the core result of [Schwartz (1997)](https://doi.org/10.1111/j.1540-6261.1997.tb02721.x){:target="_blank"}. Two methods are available:

| `method` | What it models | Measures |
|:---------|:---------------|:---------|
| `single_factor` (default) | The log price reverts to one long-run level | Real-world |
| `schwartz_smith` | A short-term deviation that fades, on top of a long-term level that drifts ([Schwartz and Smith, 2000](https://doi.org/10.1287/mnsc.46.7.893.12034){:target="_blank"}) | Real-world and risk-neutral |

```yaml
commodities:
  - name: gold
    ticker: GC=F
    period: daily
  - name: oil
    ticker: CL=F
    method: schwartz_smith
```

**Single factor.** The log price mean-reverts, which keeps the price positive. On 2026-10-04 crude oil started at 91.11 USD and was pulled toward 67.06 USD, with a shock halving in about six months. `exp(long_run_mean)` is the long-run median price, so a `long_run_mean` belief is a log price: for a 70 USD median, use `log(70)`. Optional `volatility_model: garch` ([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1){:target="_blank"}) and `condition_on_business_cycle` (not together) fit the raw price rather than the log, so they lose the guarantee of a positive price.

**Two factor.** A spike that should fade quickly sits in the short-term part; a lasting shift sits in the long-term part. A run holds both parts (`oil_chi` and `oil_xi`) plus the rebuilt price `oil`, which a portfolio can hold. The volatilities come from the listed futures curve where one exists (crude oil, natural gas, gold, silver, copper, corn, wheat and soybeans), with a spot-only fallback and a warning otherwise.

`measure: risk_neutral` requires `schwartz_smith`. It keeps the same volatilities and fits only the two drift terms to today's futures prices, so it needs a curve and raises without one. On 2026-10-04 the steeply backwardated crude curve implied the long-term level falling about 17.7% a year, against 2.5% in the real-world fit.

A trending price over a short window can fail the fit with a "no mean reversion" error: gold sampled monthly from 2016 does. The shipped `core` and `default` sets fit gold on daily prices since 2000, where it does revert, but so slowly that `diagnose()` flags it as slow to settle. Separately, a daily `CL=F` history that includes WTI's negative settlement of 2020-04-20 fails the positivity check. Schwartz's convenience-yield and stochastic-rate variants are not implemented, and beliefs apply only to the constant-volatility single-factor model.

Prices come from Yahoo Finance by default, no key needed. Reference: [Commodities API](/projects/financescenarios/docs/reference/commodities).

## Real Estate

Use this factor for property exposure or for projections of house-price growth, for example in mortgage or housing scenarios.

The model follows eq. 3.18 of [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}: the growth rate of prices mean-reverts to a long-run rate. Real estate is linked to the rest of the model only through correlations; the authors tested inflation as a direct driver, found it insignificant, and so did not include it.

Two sources measure different things:

| `source` | Measures | Coverage | Key |
|:---------|:---------|:---------|:----|
| `house_price` (default) | Year-over-year residential house-price growth (OECD) | Many countries, quarterly or yearly | None |
| `commercial` | Year-over-year growth of FRED's Commercial Real Estate Price Index ([`COMREPUSQ159N`](https://fred.stlouisfed.org/series/COMREPUSQ159N){:target="_blank"}, from the IMF): office, retail, industrial, apartments | United States, quarterly only | FRED |

```yaml
real_estate:
  enabled: true
  country: United States
  period: quarterly
  source: house_price
```

On 2026-10-06, US house prices were 2.1% above a year earlier and pulled toward 3.4% a year, with a boom or slump fading by half in about 5.7 years. Commercial property grew faster (6.6%) but toward a lower 2.5%, reverted within about a year and was almost four times as volatile, as a transaction-based series would be.

Neither source matches the paper. The authors used NCREIF's appraisal-based index, which smooths prices and has no open equivalent; see [coverage](/projects/financescenarios/docs/coverage). GARCH volatility and business-cycle conditioning are available, the latter with a quarterly or yearly leading indicator. Reference: [Real estate API](/projects/financescenarios/docs/reference/real-estate).

## Dividend Yield and Dividend Growth

Use these factors when dividend income matters on its own, for example in pension or income projections, or to run Wilkie's model.

### Dividend Yield

The equity factor simulates total return only. A `dividend_yield` entry simulates the yield itself, following eq. 3.17 of [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}: the log of the yield mean-reverts. The yield is computed from the Finance Toolkit's daily data as the dividends paid over the last `window` trading days (252, about a year) divided by the closing price.

```yaml
dividend_yield:
  - name: spy_yield
    ticker: SPY
    period: monthly
```

Dividend yields move slowly. On 2026-10-04 SPY yielded 0.99% and was pulled toward 1.39% with a half-life of about 4.7 years. The source paper found the speed "not significantly different from zero" on 1871-2003 data, close to a random walk, so a window with no mean reversion raises an error. A longer history or a coarser period usually helps.

The fit is on the log yield, so a belief about the normal level is a log too: a 2% target is `log(0.02)`, about -3.9. On the Financial Modeling Prep Free plan the dividend history holds only five payments, too short for a year's window, so no key at all (Yahoo Finance) works better. `condition_on_inflation: true` adds Wilkie's inflation term, linking the yield to a named inflation entry.

### Dividend Growth (Wilkie)

[Wilkie's (1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf){:target="_blank"} model is a cascade. Inflation is simulated first, and dividend yield, dividend growth and long-term rates follow from it in one direction, with nothing feeding back. The shipped `wilkie` factor set wires it as:

1. inflation (`method: wilkie_ar1`),
2. dividend yield (`condition_on_inflation: true`),
3. dividend growth,
4. the share price (`equities[].method: wilkie_derived`), equal to the dividend index divided by the yield.

Dividend growth is Wilkie's "Reduced Basis" equation, in plain terms:

`dividend growth = real drift + part of this period's inflation + part of past inflation + last period's yield surprise + noise`

| Config name | Wilkie | Meaning |
|:------------|:-------|:--------|
| `long_run_drift` | DMU | Dividend growth net of inflation |
| `inflation_sensitivity` | DW | How much of this period's inflation passes straight into dividends |
| `carried_forward_sensitivity` | DX | Effect of a slow moving average of past inflation, so dividends keep catching up |
| `yield_residual_sensitivity` | DY | Effect of last period's unexpected move in the dividend yield |
| `volatility` | DSD | The index's own random shock |
| `carried_forward_weight` | DD | Weight of the moving average; fixed at Wilkie's 0.2, not fitted |

The yield term reflects Wilkie's view that prices anticipate dividend changes, so the yield moves first. Everything except `carried_forward_weight` is fitted by one least squares regression; Wilkie's moving-average term on the index's own shock is left out, as his Reduced Basis allows.

```yaml
dividend_growth:
  - name: dividend_growth
    ticker: JNJ
    inflation_name: inflation
    dividend_yield_name: dividend_yield
    carried_forward_weight: 0.2
```

Every entry needs a paired inflation entry and a paired dividend yield entry. It runs at the inflation entry's period, and the paired yield must use the plain fit, not GARCH or business-cycle conditioning, because its shocks have to be rebuilt from its path. Wilkie fitted 1919-1982 UK data; the shipped preset applies the same equations to JNJ and US data, with the `wilkie` settings capping history at 2019 for the cascade's long-rate leg. References: [Dividend yield API](/projects/financescenarios/docs/reference/dividend-yield), [Dividend growth API](/projects/financescenarios/docs/reference/dividend-growth).

## Credit Spreads

Use this factor when a portfolio holds corporate bonds or when you need the extra yield companies pay over government debt.

Each `credit` entry is one spread bucket, simulated as a mean-reverting process on the log spread so it never turns negative. A spread that has touched zero in its history has no log, and is fitted on its level instead; its parameters and beliefs are then plain decimals.

| `dimension` | What | Coverage | Key |
|:------------|:-----|:---------|:----|
| `maturity` | ICE BofA US corporate option-adjusted spread by maturity (`1-3 Years` up to `15+ Years`) | Last three years only | FRED |
| `rating` | ICE BofA spread by rating, `AAA` to `CCC` | Last three years only | FRED |
| `moodys` | Moody's seasoned `Aaa` and `Baa` yields over the 10-year Treasury, or `Baa - Aaa` | From 1953 | FRED |
| `corporate` | Germany, all ratings ([Bundesbank](https://www.bundesbank.de/en/statistics/money-and-capital-markets){:target="_blank"}, from 1957); Australia, A and BBB at 3 to 10 years ([RBA table F3](https://www.rba.gov.au/statistics/tables/){:target="_blank"}, from 2005) | Monthly | None |
| `borrowing_cost` | ECB composite cost of new bank loans to companies ([ECB MIR](https://data.ecb.europa.eu/data/datasets/MIR){:target="_blank"}), a rate rather than a spread | Euro area or a member, from 2003 | None |

The ICE BofA indices are the most detailed, but FRED limits every ICE BofA series to a trailing three-year window. That is too short to estimate a reliable correlation against slower yearly factors, which is why the shipped factor sets leave credit off. For long horizons, the Moody's or corporate series give decades of history.

```yaml
credit:
  - name: bbb_spread
    dimension: rating
    rating_bucket: BBB
    period: monthly
  - name: baa_aaa
    dimension: moodys
    rating_bucket: Baa - Aaa
    period: monthly
```

Spreads revert quickly. On 2026-10-04 the 7-10 year investment-grade spread started at 1.05% and was pulled toward 1.01% with a half-life of about three months. As with dividend yields, a belief about the normal level of a log-fitted spread is a log: a 2% target is `log(0.02)`.

GARCH volatility and business-cycle conditioning are available (not together) and fit the raw spread level. There is no euro or UK spread by rating, since those indices are licensed data. For a full spread curve rather than buckets, see the [credit term structure API](/projects/financescenarios/docs/reference/credit-term-structure). Reference: [Credit API](/projects/financescenarios/docs/reference/credit).

## Credit Migration and Default

Use this factor when you need downgrades, defaults and credit losses on a bond portfolio by rating, not only spread moves.

The model treats each borrower's credit quality as a random draw. Part of it, set by the asset correlation, is a shared credit cycle; the rest is the borrower's own luck. A through-the-cycle transition matrix sets each rating's cut-offs for upgrades, downgrades and default. A bad year shifts every row at once, toward downgrade and default. This is the one-factor approach described by [Kim (1999)](https://www.msci.com/www/research-report/a-way-to-condition-transition/018440984){:target="_blank"}, in the Markov rating framework of [Jarrow, Lando and Turnbull (1997)](https://doi.org/10.1093/rfs/10.2.481){:target="_blank"}.

The data is ESMA's [CEREP](https://registers.esma.europa.eu/cerep-publication){:target="_blank"} repository of rating agency statistics, no key needed. The cycle is fitted year by year from default rates across ratings, then simulated as a mean-reverting process around zero, the through-the-cycle average. The run gains one yearly variable, `credit_cycle`, high in good years.

```yaml
credit_migration:
  enabled: true
  agency: S&P
  rating_type: corporate
  matrix_years: 10
```

```python
from financescenarios import rating_migration

# result: a ScenarioSet from a run with credit_migration enabled
migration = rating_migration(result, {"A": 40, "BBB": 50, "BB": 10}, recovery_rate=0.4)
migration.summary()
```

`rating_migration` rolls the rating mix forward one year at a time and returns the share in each rating and in default, and the loss after recovery, in every scenario.

The matrix pools the last `matrix_years` of transition counts, with each rating's average yearly default rate as its default column. A rating that never defaulted in the sample gets Basel's 0.03% floor ([CRR Article 160(1)](https://eur-lex.europa.eu/eli/reg/2013/575/oj){:target="_blank"}). CEREP publishes a year's statistics during the next year, so the latest complete year can lag by one or two years.

On S&P corporate ratings from 2000 to 2025, the worst years came out as 2009, 2001, 2020 and 2002, the asset correlation was about 0.10, and a shock to the cycle halved in about eight months.

What it does not do: spreads are not derived from the ratings (use [credit spreads](#credit-spreads) for that), recovery is a fixed input, and the cycle is one index for all sectors and regions. Reference: [Credit migration API](/projects/financescenarios/docs/reference/credit-migration).
