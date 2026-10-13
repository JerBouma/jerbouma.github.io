---
title: "Configuration Classes"
seo_title: "Configuration Classes Reference – Finance Scenarios"
excerpt: "The typed settings behind each factor block, the engine and the data download, plus beliefs, belief paths and shocks."
description: "The typed settings behind each factor block, the engine and the data download, plus beliefs, belief paths and shocks."
author_profile: false
permalink: /projects/financescenarios/docs/reference/configuration-classes
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

The typed settings behind each factor block, the engine and the data download, plus beliefs, belief paths and shocks.

```python
from financescenarios import EngineConfig, ToolkitConfig, InterestRateConfig, InflationConfig, UnemploymentConfig, EquityConfig, FXConfig, CreditConfig, CommodityConfig, DividendYieldConfig, DividendGrowthConfig, RealEstateConfig, YieldCurveConfig, OUBeliefs, EquityBeliefs, BeliefPath, Shock
```

## EngineConfig

How a run is simulated: how many scenarios, how many steps of what length, and how the random shocks are drawn.

More scenarios make percentiles and averages more precise (the error of an average shrinks with the square root of
the count), at a cost in time and memory. The shocks are what makes the scenarios differ, and their shape sets the
tails: Gaussian by default, or Student-t (`shock_distribution: student_t`) for fat tails in which large moves are
more frequent and tend to hit several markets at once. Antithetic sampling pairs every scenario with its mirror
image, which measures averages more precisely for the same number of scenarios without changing the model.

The correlations that tie the factors together are estimated from their historical changes, each pair on the
history the two share, and pulled slightly toward their average (`correlation_shrinkage`), since a correlation
estimated from a few years of data is noisy and the noise is worst in the extremes.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class EngineConfig(_StrictModel):
    n_simulations: int = Field(gt=0, le=100000, default=1000, description='The number of scenarios to simulate.')
    n_steps: int = Field(gt=0, le=10000, default=52, description='The number of time steps in each scenario.')
    frequency: str = Field(default='weekly', description=f'The length of one step, one of {list(FREQUENCY_TO_TIME_STEP)}.')
    seed: int | None = Field(default=None, description='Fix it to get the same scenarios on every run.')
    antithetic: bool = Field(default=False, description='Pair every scenario with its mirror image (the opposite shocks), which measures averages more precisely for the same number of scenarios. n_simulations must be even.')
    shock_distribution: Literal['gaussian', 'student_t'] = Field(default='gaussian', description="'gaussian' (the default) or 'student_t', whose fat tails make extreme moves more frequent and more likely to hit several factors at once. Each factor's volatility means the same either way; only the shape of the tails changes.")
    degrees_of_freedom: float = Field(default=5.0, gt=2, description="Student-t degrees of freedom, only used when shock_distribution='student_t'. Lower means fatter tails and stronger tail dependence; must be > 2 for finite variance.")
    correlation_method: Literal['pairwise', 'complete_case'] = Field(default='pairwise', description="How the correlations are estimated. 'pairwise' (the default) uses each pair's own shared history, so one factor with a short history only affects its own pairs; a pair that overlaps too little is set to 0 and listed in correlation_fallback_pairs. 'complete_case' cuts every factor to the one window they all share, which gives a consistent matrix but lets a single short history shrink every estimate.")
    correlation_shrinkage: float | Literal['auto'] = Field(default=0.1, description="How much the sample correlation matrix is shrunk before use. A number in [0, 1] blends it that far toward its own average correlation (0.1, the default). 'auto' instead shrinks toward no correlation by the data-driven intensity of Schafer and Strimmer (2005), larger when correlations rest on few observations; on the broad factor set it lowered the out-of-sample correlation error by 2-8%.")
    shared_equity_regimes: bool = Field(default=False, description="Draw every regime-switching equity's regime changes from one shared stream of random numbers instead of one stream each, so markets tend to enter and leave their crisis regimes together, as they do. Each entry keeps its own fitted transition probabilities, so the paths still differ where those differ. Without it, independent regime paths dilute the simulated correlation between equities: on the core factor set the mean gap to the calibrated correlations fell from 0.094 to 0.044.")
```

</details>

## EngineConfig.time_step

Time increment per step, in years, derived from `frequency`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
engineconfig.time_step  # property -> float
```

</details>

## ToolkitConfig

Settings for the embedded Finance Toolkit `Toolkit` instance: Finance Scenarios'
sole calibration data source. `Scenarios.from_config_file()`/`from_config()` build
this `Toolkit` automatically; a caller never constructs one directly.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class ToolkitConfig(_StrictModel):
    start_date: date | None = Field(default=None, description='Start of the historical data window pulled for calibration.')
    end_date: date | None = Field(default=None, description="End of the historical data window pulled for calibration (default: today). Useful to cap a calibration window before a specific event, e.g. an interest_rates[] entry with method='wilkie_consols' assumes the inflation-adjusted real yield stays positive throughout the fit window, an assumption that broke down during the 2020-2022 COVID/ZIRP era; capping end_date before that period keeps the model usable as a legacy calibration.")
    extra_tickers: list[str] = Field(default_factory=list, description='Tickers to include beyond interest_rates[i].ticker/equities[i].ticker, e.g. for a factor with no dedicated config field yet.')
    benchmark_ticker: str | None = Field(default=None, description="FinanceToolkit's benchmark ticker. Left as None by default since FinanceToolkit silently drops a ticker from the list when it matches the benchmark.")
    progress_bar: bool = False
```

</details>

## InterestRateConfig

One interest rate in the run: a country's short or long rate, fitted to its history and simulated as its own
correlated factor. `ScenariosConfig.interest_rates` holds one or more of these, at least one.

By default the rate is mean-reverting (Hull-White): pulled toward a long-run level at its historical speed, with
shocks of its historical size, and free to go negative, as euro, yen and Swiss franc rates did. The data comes
from a Treasury-yield ticker (`source: ticker`, US), the OECD's short and long rates (`source: oecd`, worldwide) or
the Global Macro Database (`source: gmdb`, more countries, yearly only); `history_source` can fit the speed and
level on more than a century of data instead.

The model can be changed with `method`:

- `hull_white` (default): mean-reverting, can go negative.
- `cir`: shocks shrink as the rate nears zero, so it stays positive.
- `wilkie_consols`: Wilkie's (1986) long yield, expected inflation plus a real yield. It assumes real yields stay
  positive, which the near-zero rates of 2020-2022 broke, so cap the data window before that era.
- `hibbert_two_factor`: the short rate reverts to a long rate that itself moves (Hibbert et al., 2001), so the
  whole level of rates can drift for years.
- `knw` and `knw_sv`: the rate and a paired inflation entry are fitted jointly, as in De Nederlandsche Bank's
  scenario set; `knw_sv` adds a stochastic volatility the two share, which an equity can join.

Other options shape the economics further. `volatility_model: garch` lets calm and turbulent periods alternate.
`condition_on_business_cycle` tilts the rate with the leading indicator. `long_run_anchor` pulls the rate toward
EIOPA's forward rates (the Solvency II reference) or the median of DNB's scenario set instead of its own fitted
level. `zero_lower_bound` floors it at 0%. `beliefs` overrides the fit with your own view (see `OUBeliefs`). Only
`hull_white` and `cir` take `condition_on_business_cycle`, a `history_source` or a `long_run_anchor`, only
`hull_white` takes `volatility_model: garch`, and beliefs apply to constant-volatility, real-world `hull_white` and
`cir` entries. `knw` and `knw_sv` pair one rate with one inflation entry: both set the same method and name each
other, at the same `period`.

For a market-consistent valuation, `measure: risk_neutral` with `risk_neutral_forward_curve: true` makes the rate
reproduce today's Treasury forward curve rather than history; `Scenarios.simulate(measure="risk_neutral")` sets
this up for you.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class InterestRateConfig(_StrictModel):
    name: str = 'interest_rate'
    source: Literal['ticker', 'oecd', 'gmdb'] = Field(default='ticker', description="'ticker' (a Yahoo Finance Treasury-yield ticker, US only), 'oecd' (the OECD short- or long-term rate of country, monthly, quarterly or yearly) or 'gmdb' (the Global Macro Database, which covers countries outside the OECD, yearly only).")
    currency: str = Field(default='USD', description="The currency this rate belongs to, a three-letter ISO code such as 'EUR'. Used to convert results into the reporting currency and to pick long_run_anchor's curve.")
    measure: Literal['real_world', 'risk_neutral'] = Field(default='real_world', description="'real_world' (fitted on history, the default) or 'risk_neutral' (matched to today's market: a flat path at today's rate, or today's forward curve with risk_neutral_forward_curve). A risk_neutral entry takes no beliefs.")
    method: Literal['hull_white', 'cir', 'wilkie_consols', 'hibbert_two_factor', 'knw', 'knw_sv'] = 'hull_white'
    ticker: str = Field(default='^IRX', description="With source='ticker': the Treasury-yield ticker, e.g. ^IRX (13-week), ^FVX (5-year), ^TNX (10-year) or ^TYX (30-year).")
    country: str = Field(default='United States', description="With source 'oecd' or 'gmdb' (or a history_source): the country.")
    term: Literal['short', 'long'] = Field(default='short', description="With source 'oecd' or 'gmdb': the short-term or the long-term rate.")
    period: str = Field(default='daily', description='The frequency of the history the rate is fitted on: any for a ticker, monthly, quarterly or yearly for oecd, yearly for gmdb. Left unset, it is daily for a ticker, monthly for oecd and yearly for gmdb.')
    volatility_model: Literal['constant', 'garch'] = Field(default='constant', description="'constant' (the default) or 'garch' (GARCH(1,1) time-varying volatility, Bollerslev 1986); 'garch' needs method='hull_white'.")
    condition_on_business_cycle: bool = Field(default=False, description="Add an additive drift term on the leading indicator's step-to-step change (business-cycle conditioning). Requires leading_indicator.enabled=true; incompatible with volatility_model='garch'.")
    risk_neutral_forward_curve: bool = Field(default=False, description="With measure='risk_neutral' and method='hull_white': simulate a Hull-White rate whose drift reproduces today's forward curve (from the four Treasury tenors), with speed and volatility fitted on history, instead of a flat path at today's rate.")
    inflation_name: str = Field(default='inflation', description="With method 'wilkie_consols', 'knw' or 'knw_sv': the name of the inflation entry this rate is paired with. A wilkie_consols rate is fitted at that entry's period.")
    inflation_weight: float = Field(default=1.0, description="With method='wilkie_consols': Wilkie's CW, the weight on inflation; fixed, not fitted.")
    inflation_decay: float = Field(default=0.05, gt=0, lt=1, description="With method='wilkie_consols': Wilkie's CD, how fast past inflation fades; fixed, not fitted.")
    target_source: Literal['long_term_rate', 'ewma'] = Field(default='long_term_rate', description="With method='hibbert_two_factor': what the rate reverts toward. 'long_term_rate' (the default) fetches the same country's long rate (target_term or target_ticker) and simulates it as a second factor, '<name>_target'; 'ewma' uses a moving average of this rate's own path (target_smoothing) instead.")
    target_term: Literal['short', 'long'] = Field(default='long', description="With target_source='long_term_rate' and source 'oecd' or 'gmdb': the target's term, which must differ from term (the same term would be the same series).")
    target_ticker: str = Field(default='^TNX', description="With target_source='long_term_rate' and source='ticker': the target's ticker, which must differ from ticker.")
    target_smoothing: float = Field(default=0.05, gt=0, lt=1, description="With target_source='ewma': the weight of each new observation in the moving average; smaller is a slower target. Fixed, not fitted.")
    history_source: Literal['millennium', 'jst', 'oecd'] | None = Field(default=None, description="Fit the dynamics (speed, volatility, long-run level) on decades or centuries of history instead of the recent window, at the maturity term names; today's level and the correlation series still come from source. 'oecd': the OECD's short- or long-term rate of country, yearly from 1950; 'millennium': the Bank of England's Bank Rate from 1694 or long government bond (consols) yields (country 'United Kingdom'); 'jst': the Jordà-Schularick-Taylor bill return of country from 1870, short only (needs accept_licence). Real-world hull_white or cir with constant volatility only.")
    history_start_year: int | None = Field(default=None, description='With history_source: leave out years before this one, e.g. 1900.')
    accept_licence: bool = Field(default=False, description="Confirms non-commercial use, which history_source 'jst' requires (CC BY-NC-SA 4.0).")
    zero_lower_bound: bool = Field(default=False, description='Keep this rate at or above 0%, as some scenario generators do. The model still evolves underneath as a shadow rate that may go negative (Black 1995); the rate every path, discount factor and linked factor sees is max(shadow, 0), so a rate that touched zero climbs back from where the shadow went rather than from 0. Off by default: negative rates did happen (euro, yen, Swiss franc). Real-world entries only.')
    history_volatility: Literal['history', 'recent'] = Field(default='history', description="With history_source: 'history' (default) takes the volatility from the long history along with the speed and level; 'recent' keeps the volatility fitted on the recent window, so a calm or volatile recent era sets how much the rate swings while the long history sets how fast it reverts.")
    long_run_anchor: Literal['eiopa', 'dnb'] | None = Field(default=None, description="Pull the rate toward an official curve's forward rates instead of one fitted long-run level: 'eiopa' uses EIOPA's risk-free curve for this entry's currency (USD, EUR or GBP), the 1-year forward rate for term short and the 10-year forward for term long, starting at every scenario date, ending at EIOPA's ultimate forward rate (Solvency II's reference). 'dnb' (EUR only) follows the median of De Nederlandsche Bank's real-world scenario set instead, its 1-year or 10-year nominal rate, the reference for Dutch pension funds. Speed and volatility stay fitted. An explicit beliefs.long_run_mean takes precedence. hull_white or cir, real_world, constant volatility only.")
    beliefs: OUBeliefs = Field(default_factory=OUBeliefs)
```

</details>

## InflationConfig

One country's consumer price inflation, fitted to its history and simulated as its own correlated factor.
`ScenariosConfig.inflation` holds one or more of these, at least one.

By default inflation is mean-reverting (an Ornstein-Uhlenbeck process, as in Ahlgrim, D'Arcy & Gorvett, 2005):
pulled back toward a long-run rate at its historical speed, so a spike fades over a few years rather than becoming
the new normal, and deflation is possible but rare. The data is the OECD's consumer price index (`source: oecd`,
monthly to yearly) or the Global Macro Database (`source: gmdb`, more countries, yearly only).

The model can be changed with `method`:

- `ou` (default): mean-reverting toward one long-run rate.
- `wilkie_ar1`: Wilkie's (1986) original inflation model, a simple autoregression.
- `hibbert_two_factor`: inflation reverts to an "expected inflation" level that itself moves (Hibbert et al.,
  2001), so inflation regimes can persist for years.
- `knw` and `knw_sv`: fitted jointly with a paired interest rate, as in De Nederlandsche Bank's scenario set.

`volatility_model: garch` lets calm and turbulent periods alternate, `condition_on_business_cycle` tilts inflation
with the leading indicator, `condition_on_interest_rate` lets it respond to changes in a paired rate, and `beliefs`
overrides the fit with your own view, such as a central bank's 2% target (see `OUBeliefs`). These options apply
to `ou` only, and GARCH entries keep their fitted parameters.

Under `measure: risk_neutral`, a `knw_sv` entry takes the pair's market-consistent fit, and an `ou` entry follows
the market's breakeven inflation curve (nominal minus inflation-linked bond yields) of the United States, the
United Kingdom, Germany or the euro area instead of history, read with no API key (leave `source` and `period` at
their defaults).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class InflationConfig(_StrictModel):
    name: str = 'inflation'
    country: str = Field(default='United States', description='The country whose consumer price inflation to fit.')
    source: Literal['oecd', 'gmdb'] = Field(default='oecd', description="'oecd' (the OECD consumer price index, monthly, quarterly or yearly) or 'gmdb' (the Global Macro Database, which covers countries outside the OECD, yearly only).")
    currency: str = Field(default='USD', description='The currency of this inflation series, a three-letter ISO code; used when converting results.')
    measure: Literal['real_world', 'risk_neutral'] = Field(default='real_world', description="'real_world' (fitted on history, the default) or 'risk_neutral', with method 'knw_sv' (the market-consistent fit of the pair) or 'ou' (today's breakeven inflation curve of the United States, the United Kingdom, Germany or the euro area). A risk_neutral entry takes no beliefs.")
    period: str = Field(default='monthly', description='The frequency of the history inflation is fitted on: monthly, quarterly or yearly.')
    method: Literal['ou', 'wilkie_ar1', 'hibbert_two_factor', 'knw', 'knw_sv'] = Field(default='ou', description="'ou' (mean-reverting, the default), 'wilkie_ar1' (Wilkie 1986's AR(1)), 'hibbert_two_factor' (reverts to a moving target, see target_source), 'knw' (jointly fitted with interest_rate_name's rate) or 'knw_sv' (knw with stochastic volatility). Only 'ou' takes GARCH, conditioning or beliefs.")
    target_source: Literal['coarser_period', 'ewma'] = Field(default='coarser_period', description="With method='hibbert_two_factor': what inflation reverts toward. 'coarser_period' (the default) fetches the same country's inflation at target_period and simulates it as a second factor, '<name>_target'; 'ewma' uses a moving average of this entry's own path (target_smoothing) instead.")
    target_period: Literal['quarterly', 'yearly'] = Field(default='yearly', description="With target_source='coarser_period': the target's frequency, coarser than period (monthly allows quarterly or yearly, quarterly only yearly). Growth over a longer window is larger, so the fitted reversion speed has no direct years-to-close-the-gap reading.")
    target_smoothing: float = Field(default=0.05, gt=0, lt=1, description="With target_source='ewma': the weight of each new observation in the moving average; smaller is a slower target. Fixed, not fitted.")
    tips_breakeven_decay: float = Field(default=0.7308, gt=0, description="With measure='risk_neutral' and method='ou': the Nelson-Siegel decay (lambda) of the breakeven curve fit, the same default as yield_curve.")
    volatility_model: Literal['constant', 'garch'] = Field(default='constant', description="'constant' (the default) or 'garch' (GARCH(1,1) time-varying volatility, Bollerslev 1986).")
    condition_on_business_cycle: bool = Field(default=False, description="Add an additive drift term on the leading indicator's step-to-step change (business-cycle conditioning). Requires leading_indicator.enabled=true; incompatible with volatility_model='garch'.")
    condition_on_interest_rate: bool = Field(default=False, description="Add a drift term on the step-to-step change of interest_rate_name's rate: the link between nominal rates and inflation of macro-finance term-structure models (Dai and Singleton 2000). Not with volatility_model='garch' or condition_on_business_cycle, since the fit takes one covariate.")
    interest_rate_name: str = Field(default='interest_rate', description="With condition_on_interest_rate or method 'knw' or 'knw_sv': the name of the interest_rates entry this inflation is paired with.")
    history_source: Literal['millennium', 'shiller'] | None = Field(default=None, description="Fit the dynamics (speed, volatility, long-run level) on centuries of history instead of the recent window; today's level and the correlation series still come from source. 'millennium': UK consumer price inflation from 1209 (country 'United Kingdom'); 'shiller': US December-to-December inflation from 1872 (country 'United States'). Real-world ou with constant volatility only.")
    history_start_year: int | None = Field(default=None, description='With history_source: leave out years before this one, e.g. 1900.')
    beliefs: OUBeliefs = Field(default_factory=OUBeliefs)
```

</details>

## UnemploymentConfig

Unemployment factor settings: one entry per country. `ScenariosConfig.unemployment` holds at least one; each entry
becomes its own correlated factor, keyed by `name`, mean-reverting with a Phillips-curve term on the inflation entry
named by `inflation_name`. It has no `period` of its own: it is fitted at that inflation entry's period, which must
be yearly for `source: gmdb`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class UnemploymentConfig(_StrictModel):
    name: str = 'unemployment'
    country: str = 'United States'
    source: Literal['oecd', 'gmdb'] = Field(default='oecd', description="'oecd' (FinanceToolkit's OECD unemployment rate, worldwide within the OECD roster) or 'gmdb' (its Global Macro Database; covers countries outside the OECD roster; requires the paired inflation[i].period to be 'yearly', since this entry has no period of its own).")
    inflation_name: str = Field(default='inflation', description="Which configured inflation[i].name drives this entry's Phillips-curve term.")
    condition_on_business_cycle: bool = Field(default=False, description="Add a second drift term, on the leading indicator's step-to-step change, next to the inflation term. Requires leading_indicator.enabled=true, with leading_indicator.period equal to the paired inflation entry's period.")
    beliefs: UnemploymentBeliefs = Field(default_factory=UnemploymentBeliefs)
```

</details>

## EquityConfig

One equity market in the run: a broad index, a sector, a region or a style, each from one ticker and simulated as
its own correlated factor. `ScenariosConfig.equities` holds one or more of these, at least one.

By default the returns switch between regimes (Hardy, 2001): a calm one with steady gains and a turbulent one with
losses and high volatility, each fitted to the ticker's history along with how often the market moves between
them. This gives what a single bell curve misses: crashes cluster, volatility stays high once it rises, and the
distribution of returns has a fat left tail. `shared_equity_regimes` in the engine settings makes markets enter
and leave their turbulent regime together.

Other methods tie equities to the rest of the economy: `wilkie_derived` builds the price from a dividend index and
a dividend yield (Wilkie, 1986), `hibbert_regime_switching` fits the regimes to returns in excess of a short rate,
so equities earn a premium over cash, and `knw_sv` shares stochastic volatility with rates and inflation. Under
`measure: risk_neutral` the market earns the risk-free rate less its dividend yield, with a volatility from
option prices. `asset_class` stands in a listed fund for an asset class without a public index, such as private
equity or infrastructure. `beliefs` overrides the fit with your own view (see `EquityBeliefs`).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class EquityConfig(_StrictModel):
    name: str = 'equity'
    ticker: str = 'SPY'
    asset_class: str | None = Field(default=None, description="An asset class without a public return index, e.g. 'Private Equity', 'Infrastructure', 'Hedge Funds' or 'Private Credit' (a key of ASSET_CLASS_PROXIES): sets ticker to the listed fund the Finance Toolkit's economics.get_asset_class_proxies uses for it. Listed prices are marked to market daily, so they swing more and move more with equities than the appraisal-based returns private funds report, and they are net of the fund's fees.")
    currency: str = Field(default='USD', description='The currency the ticker is listed in, which is not always the market it tracks (VGK and EWJ are USD-listed); used when converting results.')
    measure: Literal['real_world', 'risk_neutral'] = Field(default='real_world', description="'real_world' (fitted on history, the default) or 'risk_neutral' (geometric Brownian motion growing at the risk-free rate minus the dividend yield, with the volatility from volatility_source). A risk_neutral entry takes no beliefs.")
    volatility_source: Literal['implied', 'svi', 'realized', 'heston'] = Field(default='implied', description="Only used when measure='risk_neutral': where the flat GBM volatility comes from. 'implied' (default) reads the at-the-money strike from one raw per-strike Black-Scholes inversion at FinanceToolkit's nearest expiration. 'svi' reads the ATM value off FinanceToolkit's SVI-fitted, calendar-arbitrage-checked volatility surface (options.get_volatility_surface) at the longest fitted expiration: smoothed across the whole smile instead of passing one quote's noise straight through, and a longer expiry is the better match for a GBM simulated over years. 'realized' skips options data entirely and uses the annualized standard deviation of historical log-returns (the right choice for tickers without a liquid options market, e.g. most sector/regional/style ETFs). 'heston' fits the Heston (1993) stochastic-volatility model to the SVI surface at six expirations from one to twelve months, so the simulated paths carry the market's smile and volatility term structure instead of one flat volatility. 'implied', 'svi' and 'heston' fall back to realized volatility (flat GBM) with a logged warning when options data is unavailable.")
    n_regimes: int = Field(gt=1, default=2)
    period: str = 'monthly'
    method: Literal['regime_switching', 'wilkie_derived', 'hibbert_regime_switching', 'knw_sv'] = Field(default='regime_switching', description="'regime_switching' (a Markov regime-switching fit, the default), 'wilkie_derived' (Wilkie 1986: the price is dividend_growth_name's dividend index over dividend_yield_name's yield, with no fit of its own), 'hibbert_regime_switching' (Hibbert et al. 2001: regimes fitted to returns in excess of nominal_rate_name's rate) or 'knw_sv' (DNB's KNW model: returns earn nominal_rate_name's rate plus a fitted premium, with the rate's stochastic volatility). All but 'regime_switching' are real-world only.")
    dividend_growth_name: str | None = Field(default=None, description="Required when method='wilkie_derived'. Which configured dividend_growth[i].name this entry's price numerator reads.")
    dividend_yield_name: str | None = Field(default=None, description="Required when method='wilkie_derived'. Which configured dividend_yield[i].name this entry's price denominator reads.")
    nominal_rate_name: str | None = Field(default=None, description="Required with method 'hibbert_regime_switching' or 'knw_sv': the name of the interest_rates entry whose rate the returns are measured over, at the same period. For 'knw_sv' that entry must use method='knw_sv' too.")
    condition_on_business_cycle: bool = Field(default=False, description="Let the odds of switching regime depend on the leading indicator (Filardo 1994), instead of a drift term as for other factors. Requires leading_indicator.enabled=true, method='regime_switching' and leading_indicator.period equal to engine.frequency.")
    history_source: Literal['shiller', 'jst'] | None = Field(default=None, description="Fit the regimes on long history instead of the ticker's: 'shiller' is the US S&P Composite total return, monthly from 1871; 'jst' the yearly equity total return of history_country from 1870 (needs accept_licence). Today's price and the correlation series still come from ticker. Real-world regime_switching without condition_on_business_cycle only.")
    history_country: str = Field(default='United States', description="The JST country for history_source 'jst'.")
    history_start_year: int | None = Field(default=None, description='With history_source: leave out years before this one, e.g. 1950.')
    accept_licence: bool = Field(default=False, description="Confirms non-commercial use, which history_source 'jst' requires (CC BY-NC-SA 4.0).")
    beliefs: EquityBeliefs = Field(default_factory=EquityBeliefs)
```

</details>

## FXConfig

Exchange rate settings: opt-in, one entry per currency (an empty `fx` list simulates none). Each entry is a
geometric Brownian motion on one currency's exchange rate against the US dollar, from the OECD (`source: oecd`,
monthly at the finest) or the Global Macro Database (`source: gmdb`, yearly only), correlated with the rest of the
model. `drift_mode` picks where the trend comes from.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class FXConfig(_StrictModel):
    name: str = 'fx'
    country: str = Field(default='EA20', description="The country (or currency area) whose currency is paired against the US dollar. The OECD exchange-rate series is keyed by currency area, not member state: 'EA20' is the euro area, and an individual member ('Germany', 'France', ...) has no series of its own there, unlike interest_rates/inflation/unemployment, which do take a member state's name.")
    currency: str | None = Field(default=None, description="The ISO code of the currency this pair quotes against the dollar, e.g. 'EUR'. Read by financescenarios.reporting to convert into that currency. When unset it is taken from an interest_rates/inflation entry with the same country, or 'EUR' for the OECD's euro-area codes ('EA20', 'EA19', 'Euro Area').")
    source: Literal['oecd', 'gmdb'] = Field(default='oecd', description="'oecd' (FinanceToolkit's OECD exchange rate, period='monthly'/'quarterly'/'yearly') or 'gmdb' (its Global Macro Database; covers countries outside the OECD roster, period='yearly' only).")
    period: str = 'monthly'
    measure: Literal['real_world', 'risk_neutral'] = Field(default='real_world', description="'real_world' (fitted on history, the default) or 'risk_neutral' (covered interest rate parity: a fixed drift of the foreign minus the US short rate, from this run's interest_rates entries for both countries, with the historical volatility). A risk_neutral entry takes no beliefs.")
    drift_mode: Literal['historical', 'irp', 'random_walk'] = Field(default='historical', description="'historical' (the drift fitted on history, the default), 'irp' (uncovered interest rate parity: each step's drift is the difference between the simulated domestic_rate_name and foreign_rate_name rates) or 'random_walk', which keeps the historical volatility but drops the trend, so the median rate stays at today's level instead of extrapolating the sample's appreciation (Meese and Rogoff 1983, https://doi.org/10.1016/0022-1996(83)90017-X).")
    domestic_rate_name: str | None = Field(default=None, description="Required with drift_mode='irp': the name of the interest_rates entry for the US dollar leg.")
    foreign_rate_name: str | None = Field(default=None, description="With drift_mode='irp': the name of the interest_rates entry for the foreign leg; by default '<country>_short_rate', e.g. 'japan_short_rate' for country 'Japan'.")
    beliefs: FXBeliefs = Field(default_factory=FXBeliefs)
```

</details>

## CreditConfig

Credit factor settings: opt-in, one entry per credit spread (an empty `credit` list simulates none). Each entry is
a mean-reverting process on one spread series, correlated with the rest of the model; `dimension` picks the series.
Belief overrides only apply when `volatility_model` is "constant".

| dimension | Series | Coverage |
|:----------|:-------|:---------|
| `maturity`, `rating` | ICE BofA option-adjusted spread by maturity or rating bucket | United States, daily |
| `moodys` | Moody's Aaa or Baa yield over the 10-year Treasury, or Baa minus Aaa | United States, from 1953 |
| `corporate` | Corporate bond spread over government bonds, per `country` | Germany, Australia, monthly |
| `borrowing_cost` | ECB cost of new bank loans to companies, a rate level | Euro area or a member, monthly |

There is no euro or UK spread by rating: those indices are licensed data.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class CreditConfig(_StrictModel):
    name: str = 'credit'
    currency: str = Field(default='USD', description="The spread's currency: USD for the US sources, defaulting to EUR for 'corporate' Germany and 'borrowing_cost', AUD for 'corporate' Australia. Read by financescenarios.reporting.")
    dimension: Literal['maturity', 'rating', 'moodys', 'corporate', 'borrowing_cost'] = Field(default='maturity', description="Which spread to fit: the ICE BofA option-adjusted spread by 'maturity' (uses maturity_bucket, one of credit_controller.MATURITY_BUCKETS) or by 'rating' (uses rating_bucket, one of credit_controller.RATING_BUCKETS), both with three years of history on FRED; or 'moodys': Moody's Aaa or Baa yield over the 10-year Treasury, or Baa minus Aaa (rating_bucket one of credit_controller.MOODYS_BUCKETS), monthly from 1953; 'corporate': a country's corporate bond spread over its government bonds (country 'Germany', rating_bucket 'All ratings', from 1957; or 'Australia', rating_bucket e.g. 'BBB 10Y', from 2005); or 'borrowing_cost': the ECB's composite cost of new bank loans to companies (country 'Euro Area' or a member, from 2003), a rate level rather than a spread. The last two are monthly.")
    country: str | None = Field(default=None, description="Used when dimension is 'corporate' (default 'Germany') or 'borrowing_cost' (default 'Euro Area'); must stay unset otherwise.")
    maturity_bucket: str = Field(default='7-10 Years', description="One of credit_controller.MATURITY_BUCKETS. Used when dimension='maturity'.")
    rating_bucket: str = Field(default='BBB', description="One of credit_controller.RATING_BUCKETS for dimension='rating', of credit_controller.MOODYS_BUCKETS ('Aaa', 'Baa', 'Baa - Aaa') for dimension='moodys', or of credit_controller.CORPORATE_BUCKETS[country] for dimension='corporate' (default 'All ratings').")
    period: str = 'daily'
    volatility_model: Literal['constant', 'garch'] = Field(default='constant', description="'constant' (the default) or 'garch' (GARCH(1,1) time-varying volatility, Bollerslev 1986).")
    condition_on_business_cycle: bool = Field(default=False, description="Add an additive drift term on the leading indicator's step-to-step change (business-cycle conditioning). Requires leading_indicator.enabled=true; incompatible with volatility_model='garch'.")
    beliefs: CreditBeliefs = Field(default_factory=CreditBeliefs)
```

</details>

## CommodityConfig

Commodity factor settings: opt-in, one entry per futures ticker (an empty `commodities` list simulates none).
`method: single_factor` (the default) is Schwartz's (1997) mean-reverting log price; `method: schwartz_smith` is
Schwartz and Smith's (2000) two-factor model, a short-term deviation and a long-term equilibrium simulated as the
extra factors `<name>_chi` and `<name>_xi`. Each is correlated with the rest of the model.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class CommodityConfig(_StrictModel):
    name: str = 'commodity'
    ticker: str = Field(default='CL=F', description="Any commodity/futures ticker the Toolkit instance includes, e.g. CL=F (WTI crude), GC=F (gold), NG=F (natural gas), HG=F (copper). method='schwartz_smith' needs a ticker with a futures curve in the Finance Toolkit: crude oil, natural gas, gold, silver, copper, corn, wheat or soybeans.")
    currency: str = Field(default='USD', description='The currency the price is quoted in, USD by convention; used when converting results.')
    period: str = 'daily'
    method: Literal['single_factor', 'schwartz_smith'] = Field(default='single_factor', description="'single_factor' (default): Schwartz (1997) mean-reverting log-price process. 'schwartz_smith': Schwartz & Smith (2000) two-factor process (short-term deviation + long-term equilibrium), simulated as f'{name}_chi'/f'{name}_xi'.")
    measure: Literal['real_world', 'risk_neutral'] = Field(default='real_world', description="'real_world' (P-measure, the default) or 'risk_neutral' (Q-measure, calibrated against the ticker's real observed forward curve). Only 'schwartz_smith' has a defined risk-neutral version.")
    contracts: int = Field(default=12, gt=0, description="With method='schwartz_smith': how many monthly futures contracts to fetch for the fit.")
    long_term_window_years: float = Field(default=3.0, gt=0, description="With method='schwartz_smith': the trailing window, in years, whose average stands in for the long-term equilibrium price.")
    volatility_model: Literal['constant', 'garch'] = Field(default='constant', description="method='single_factor' only: 'constant' (Schwartz's own log-price OU fit) or 'garch' (GARCH(1,1) time-varying volatility, Bollerslev 1986). Incompatible with method='schwartz_smith'.")
    condition_on_business_cycle: bool = Field(default=False, description="method='single_factor' only: add an additive drift term on the leading indicator's step-to-step change (business-cycle conditioning). Requires leading_indicator.enabled=true; incompatible with volatility_model='garch' and with method='schwartz_smith'.")
    beliefs: CommodityBeliefs = Field(default_factory=CommodityBeliefs)
```

</details>

## DividendYieldConfig

Dividend yield factor settings: opt-in, one entry per ticker (an empty `dividend_yield` list simulates none). Each
entry is an Ahlgrim, D'Arcy and Gorvett (2005) mean-reverting process on the log of the ticker's trailing dividend
yield, correlated with the rest of the model. `condition_on_inflation` adds Wilkie's (1986) inflation term, fitted
at the period of the `inflation_name` entry.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class DividendYieldConfig(_StrictModel):
    name: str = 'dividend_yield'
    ticker: str = Field(default='SPY', description='Any dividend-paying ticker the Toolkit instance includes.')
    currency: str = Field(default='USD', description="The ticker's listing currency. A yield is a ratio and is never converted; this only labels it.")
    window: int = Field(default=252, gt=0, description='Trading days of trailing dividends summed for one yield observation.')
    period: str = 'daily'
    condition_on_inflation: bool = Field(default=False, description="Add Wilkie's (1986) inflation-sensitivity term to the fit. Requires inflation_name to match a configured inflation[i].name; forces this entry's calibration period to that entry's period. Incompatible with a belief override.")
    inflation_name: str = Field(default='inflation', description="Used when condition_on_inflation=true. Which configured inflation[i].name this entry's inflation-sensitivity term reads its step-to-step change from.")
    volatility_model: Literal['constant', 'garch'] = Field(default='constant', description="'constant' (Ahlgrim/D'Arcy/Gorvett's own log-yield OU fit) or 'garch' (GARCH(1,1) time-varying volatility, Bollerslev 1986). Incompatible with condition_on_inflation=true.")
    condition_on_business_cycle: bool = Field(default=False, description="Add an additive drift term on the leading indicator's step-to-step change (business-cycle conditioning). Requires leading_indicator.enabled=true; incompatible with volatility_model='garch' and with condition_on_inflation=true.")
    beliefs: DividendYieldBeliefs = Field(default_factory=DividendYieldBeliefs)
```

</details>

## DividendGrowthConfig

Dividend growth factor settings: opt-in, one entry per ticker, following Wilkie (1986). Each entry is driven by an
inflation entry (`inflation_name`) and a dividend yield entry (`dividend_yield_name`). It has no `period` of its
own: it is fitted at the inflation entry's period, which the dividend yield entry must share.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class DividendGrowthConfig(_StrictModel):
    name: str = 'dividend_growth'
    ticker: str = Field(default='SPY', description='Any dividend-paying ticker the Toolkit instance includes.')
    currency: str = Field(default='USD', description="The ticker's listing currency; used when converting results.")
    window: int = Field(default=252, gt=0, description='Trading days of trailing dividends summed for one dividend index observation.')
    inflation_name: str = Field(default='inflation', description="Which configured inflation[i].name this entry's dlnQ(t) term reads. Also forces this entry's calibration period to that inflation entry's period.")
    dividend_yield_name: str = Field(default='dividend_yield', description="Which configured dividend_yield[i].name this entry's YE(t-1) term reads its own shock from. Must resolve to the same period as inflation_name's entry.")
    carried_forward_weight: float = Field(default=0.2, gt=0, lt=1, description="DD, the fixed EWMA weight on current inflation in the carried-forward inflation influence: Wilkie's own published value.")
    beliefs: DividendGrowthBeliefs = Field(default_factory=DividendGrowthBeliefs)
```

</details>

## RealEstateConfig

Real estate factor settings: opt-in. A mean-reverting process on property price growth (Ahlgrim, D'Arcy and Gorvett
2005, eq. 3.18), correlated with the rest of the model. Belief overrides only apply when `volatility_model` is
"constant".

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class RealEstateConfig(_StrictModel):
    enabled: bool = False
    country: str = 'United States'
    currency: str = 'USD'
    period: str = 'quarterly'
    source: Literal['house_price', 'commercial'] = Field(default='house_price', description="'house_price' (default): OECD residential house-price growth via get_house_prices(). 'commercial': FRED's (IMF-sourced) US commercial real estate price index growth via get_commercial_real_estate_prices() instead; United States only (that call takes no country argument) and quarterly-only (no annual series), so requires country='United States' and period='quarterly'; also requires a FRED API key. Neither option is a substitute for Ahlgrim/D'Arcy/Gorvett's (2005) original calibration, which used NCREIF's appraisal-smoothed commercial-property index: no open NCREIF equivalent exists; 'commercial' is transaction-based index data, not appraisal-based (see https://www.jeroenbouma.com/projects/financescenarios/docs/coverage).")
    volatility_model: Literal['constant', 'garch'] = Field(default='constant', description="'constant' (the default) or 'garch' (GARCH(1,1) time-varying volatility, Bollerslev 1986).")
    condition_on_business_cycle: bool = Field(default=False, description="Add an additive drift term on the leading indicator's step-to-step change (business-cycle conditioning). Requires leading_indicator.enabled=true; incompatible with volatility_model='garch'.")
    beliefs: OUBeliefs = Field(default_factory=OUBeliefs)
```

</details>

## YieldCurveConfig

Nelson-Siegel dynamic yield curve settings: opt-in, alongside the single-tenor
interest_rate factor. When enabled, adds three correlated factors (rate_level,
rate_slope, rate_curvature) to the simulation, calibrated from historical
multi-tenor treasury yields (see `source`).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class YieldCurveConfig(_StrictModel):
    enabled: bool = False
    period: str = 'daily'
    decay: float = Field(default=0.7308, gt=0, description='Nelson-Siegel decay parameter (lambda), annualized.')
    source: Literal['yahoo', 'treasury', 'government'] = Field(default='yahoo', description="'yahoo' (default) calibrates against the four Yahoo Finance Treasury-yield tickers (3-month, 5-, 10- and 30-year). 'treasury' calibrates against the official daily 12-tenor Treasury par curve (1 Month through 30 Year) via FinanceToolkit's fixedincome.get_treasury_rates(): a much denser cross-section for the same three-factor Nelson-Siegel fit, especially at the short end the Yahoo set barely covers. Requires an FMP API key and period='daily' (the Treasury publishes daily); falls back to 'yahoo' with a logged warning when the fetch fails. Tenor columns the Treasury only started publishing partway through the window (e.g. '2 Month', 2018) are dropped rather than truncating every other tenor's history. 'government' calibrates against the official government bond yield curve of `country` via FinanceToolkit's fixedincome.get_government_bond_yield_curve() (no API key): the US Treasury, the ECB's euro area curve, the Bundesbank, the Bank of England, Japan's Ministry of Finance, the Bank of Canada, the Riksbank or Norges Bank; period daily, weekly or monthly. It never falls back to the US curve, since that would silently simulate the wrong country.")
    country: str = Field(default='United States', description=f"With source='government': the country whose curve to fit, one of {list(GOVERNMENT_CURVE_COUNTRIES)}.")
    beliefs: YieldCurveBeliefs = Field(default_factory=YieldCurveBeliefs)
```

</details>

## OUBeliefs

Your views on a mean-reverting factor (an interest rate, inflation, ...), laid over its historical fit. A field
left unset keeps the fitted value.

History is a guide, not a forecast: a fit on the last twenty years may put the long-run short rate at 1.5% when your
house view is 3%. `long_run_mean` sets the level the factor is pulled toward, either one number for the whole
horizon or a `BeliefPath` that moves over time ("9% next year, 2.5% by year eight"). `mean_reversion_speed` sets
how quickly shocks fade and `volatility` how large they are. `shocks` add one-off jumps at chosen years, from which
the factor then reverts on its own. A `BeliefPath` applies to constant-volatility factors without business-cycle
conditioning.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class OUBeliefs(_StrictModel):
    mean_reversion_speed: float | None = Field(default=None, gt=0)
    long_run_mean: float | BeliefPath | None = None
    volatility: float | None = Field(default=None, gt=0)
    shocks: list[Shock] = Field(default_factory=list, description='One-off jumps applied at specific simulated years.')
```

</details>

## EquityBeliefs

Your views on an equity market, laid over its regime-switching fit. A field left unset keeps the fitted value.

`regime_means` and `regime_volatilities` set each regime's yearly log-return and volatility, one value per regime
from the weakest to the strongest, so you can lower the calm regime's return (a lower equity premium) or deepen the
turbulent one. `shocks`
add one-off falls or jumps at chosen years, such as a regulator's stress path.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class EquityBeliefs(_StrictModel):
    regime_means: list[float] | None = None
    regime_volatilities: list[float] | None = None
    shocks: list[Shock] = Field(default_factory=list, description="One-off jumps in the price: each multiplies the price at its year by exp(magnitude), a log-return (-0.3 is about a 26% fall), after which the regimes continue from the shocked price. Additive only; stress_test_regime fills these from a regulator's stock-market path.")
```

</details>

## BeliefPath

A view on where a mean-reverting factor is heading over time, rather than one long-run level for the whole
horizon: "inflation at 9% in a year, 5% in three, 2.5% by year eight".

Each anchor sets the level the factor is pulled toward at that horizon; between anchors the target moves in a
straight line, and before the first it holds at the first. The factor still has its own volatility and reversion
speed, so scenarios scatter around the path and lag behind a fast-moving target rather than tracking it exactly.
Where a plain number says "the long-run level is X", a `BeliefPath` says "X now, Y in 5 years, Z in 10".

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
class BeliefPath(BaseModel):
    anchors: dict[float, float] = Field(description='horizon in years from t=0 -> target long_run_mean value.')
    converge_over_years: float | None = Field(default=None, gt=0, description='Years, past the last anchor, over which the target converges linearly to long_run_mean before holding flat there. None (default) holds flat at the last anchor forever.')
```

**Attributes:**

- <u>anchors (dict[float, float]):</u> years from the start -> the long-run level targeted then; at least one.
- <u>converge_over_years (float &#124; None):</u> after the last anchor, move the target back to the factor's own long-run level over this many years. Defaults to None, which holds the last anchor's level.

</details>

## BeliefPath.terminal_value

The level targeted at the furthest anchor, the path's single-number summary.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
beliefpath.terminal_value  # property -> float
```

</details>

## Shock

A one-off jump in a factor's level at a given year, such as "+2% on the short rate in year 3".

Unlike a `BeliefPath`, which moves where the factor is heading, a shock moves where it is: the factor jumps once,
then its own dynamics take over, so a mean-reverting factor drifts back from the shocked level at its fitted speed.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
class Shock(BaseModel):
    year: float = Field(ge=0, description='Simulated year the shock lands on.')
    magnitude: float = Field(allow_inf_nan=False, description='Shock size: added (additive) or set (absolute).')
    mode: Literal['additive', 'absolute'] = Field(default='additive', description="'additive' adds magnitude to the step's value; 'absolute' replaces it.")
```

**Attributes:**

- <u>year (float):</u> the year the shock lands, at the nearest simulated date.
- <u>magnitude (float):</u> the size of the jump, or the level to jump to with mode "absolute".
- <u>mode (str):</u> "additive" (default) adds `magnitude` to the simulated value; "absolute" sets the value to it.

</details>
