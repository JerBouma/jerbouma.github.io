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

The typed settings behind each factor block, the engine and the data download, plus beliefs, belief paths and shocks. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios import EngineConfig, ToolkitConfig, InterestRateConfig, InflationConfig, UnemploymentConfig, EquityConfig, FXConfig, CreditConfig, CommodityConfig, DividendYieldConfig, DividendGrowthConfig, RealEstateConfig, YieldCurveConfig, OUBeliefs, EquityBeliefs, BeliefPath, Shock
```

## EngineConfig

```python
class EngineConfig(_StrictModel):
    n_simulations: int = Field(gt=0, le=100000, default=1000)
    n_steps: int = Field(gt=0, le=10000, default=52)
    frequency: str = Field(default='weekly', description=f'Simulation step frequency, one of {list(FREQUENCY_TO_TIME_STEP)}.')
    seed: int | None = None
    antithetic: bool = Field(default=False, description='Use antithetic variates (paired +/- shocks) for Monte Carlo variance reduction. n_simulations must be even when enabled.')
    shock_distribution: Literal['gaussian', 'student_t'] = Field(default='gaussian', description="'gaussian' (linear/Gaussian-copula correlated shocks, the default) or 'student_t' (a multivariate Student-t/t-copula, adding fat tails and tail dependence across every factor at once; see engine.engine_model.generate_correlated_shocks). Every factor's calibrated volatility means the same thing either way; only the shape of the tail changes.")
    degrees_of_freedom: float = Field(default=5.0, gt=2, description="Student-t degrees of freedom, only used when shock_distribution='student_t'. Lower means fatter tails and stronger tail dependence; must be > 2 for finite variance.")
    correlation_method: Literal['pairwise', 'complete_case'] = Field(default='pairwise', description="How the cross-factor correlation matrix is estimated from each factor's own calibration history; see dependence_model.build_pairwise_correlation_matrix()'s own docstring for the full tradeoff writeup. 'pairwise' (the default): each pair's correlation is estimated from just that pair's own calendar overlap, so one short-history factor (a newly-added credit bucket, a thin-history commodity ticker) only costs the pairs it's actually in. Pairs with too little overlap (fewer than dependence_model._MINIMUM_RELIABLE_PAIR_OBSERVATIONS observations) default to 0.0 (assumed uncorrelated) rather than a near-mathematically-forced +-1.0; see ScenarioSet/CalibrationResult's own correlation_fallback_pairs for exactly which pairs that happened to. 'complete_case': every factor is intersected down to one shared calendar window first (the coarsest period among ALL configured factors), then correlated together (the original method). Every entry in that matrix comes from the same underlying data points, so it's PSD by construction (no fallback pairs, rarely needs Higham repair), but a single short-history or coarse-period factor shrinks the window every OTHER factor's mutual correlation is estimated from too, not just the pairs it's in; it can crash calibration outright for a large/heterogeneous factor set (see dependence_model.align_factor_series_by_date()).")
    correlation_shrinkage: float | Literal['auto'] = Field(default=0.1, description="How much the sample correlation matrix is shrunk before use. A number in [0, 1] blends it that far toward its own average correlation (0.1, the default). 'auto' instead shrinks toward no correlation by the data-driven intensity of Schafer and Strimmer (2005), larger when correlations rest on few observations; on the broad factor set it lowered the out-of-sample correlation error by 2-8%. See dependence_model.optimal_shrinkage_intensity().")
    shared_equity_regimes: bool = Field(default=False, description="Draw every regime-switching equity's regime changes from one shared stream of random numbers instead of one stream each, so markets tend to enter and leave their crisis regimes together, as they do. Each entry keeps its own fitted transition probabilities, so the paths still differ where those differ. Without it, independent regime paths dilute the simulated correlation between equities: on the core factor set the mean gap to the calibrated correlations fell from 0.094 to 0.044.")
```

Monte Carlo engine settings.

## EngineConfig.time_step

```python
engineconfig.time_step  # property -> float
```

Time increment per step, in years, derived from `frequency`.

## ToolkitConfig

```python
class ToolkitConfig(_StrictModel):
    start_date: date | None = Field(default=None, description='Start of the historical data window pulled for calibration.')
    end_date: date | None = Field(default=None, description="End of the historical data window pulled for calibration (default: today). Useful to cap a calibration window before a specific event, e.g. an interest_rates[] entry with method='wilkie_consols' assumes the inflation-adjusted real yield stays positive throughout the fit window, an assumption that broke down during the 2020-2022 COVID/ZIRP era; capping end_date before that period keeps the model usable as a legacy calibration.")
    extra_tickers: list[str] = Field(default_factory=list, description='Tickers to include beyond interest_rates[i].ticker/equities[i].ticker, e.g. for a factor with no dedicated config field yet.')
    benchmark_ticker: str | None = Field(default=None, description="FinanceToolkit's benchmark ticker. Left as None by default since FinanceToolkit silently drops a ticker from the list when it matches the benchmark.")
    progress_bar: bool = False
```

Settings for the embedded Finance Toolkit `Toolkit` instance: Finance Scenarios'
sole calibration data source. `Scenarios.from_config_file()`/`from_config()` build
this `Toolkit` automatically; a caller never constructs one directly.

## InterestRateConfig

```python
class InterestRateConfig(_StrictModel):
    name: str = 'interest_rate'
    source: Literal['ticker', 'oecd', 'gmdb'] = Field(default='ticker', description="'ticker' (Yahoo treasury-yield ticker, US-only in practice), 'oecd' (country-parameterized OECD short/long-term rate, worldwide, period='quarterly'/'yearly'), or 'gmdb' (FinanceToolkit's Global Macro Database; covers countries outside the OECD roster, period='yearly' only).")
    currency: str = Field(default='USD', description="Which currency's economy this short rate belongs to. Descriptive metadata only in v1 (not validated against ISO-4217), consumed by financescenarios.reporting for currency-conversion and by an fx[i].measure='risk_neutral' entry's interest-rate-parity drift to know which interest_rates[] entry is which currency's leg.")
    measure: Literal['real_world', 'risk_neutral'] = Field(default='real_world', description="'real_world' (P-measure, historical-regression calibration, the default) or 'risk_neutral' (Q-measure: a deterministic snapshot at today's observed rate level, not a fitted stochastic process; matches the current market rather than projecting historical dynamics forward). Belief overrides don't apply to risk_neutral entries.")
    method: Literal['hull_white', 'cir', 'wilkie_consols', 'hibbert_two_factor', 'knw', 'knw_sv'] = 'hull_white'
    ticker: str = Field(default='^IRX', description="Used when source='ticker'. Treasury-yield ticker to calibrate against: ^IRX (13-week), ^FVX (5-year), ^TNX (10-year), ^TYX (30-year), or any other ticker your Toolkit instance includes.")
    country: str = Field(default='United States', description="Used when source='oecd'. Any country FinanceToolkit's OECD data covers.")
    term: Literal['short', 'long'] = Field(default='short', description="Used when source='oecd'. Which OECD interest-rate series to use.")
    period: str = Field(default='daily', description="Sampling frequency. source='ticker' accepts daily/weekly/monthly/quarterly/yearly; source='oecd' monthly/quarterly/yearly (no daily OECD series); source='gmdb' only yearly (GMDB is annual-only). Left unset, it is daily for a ticker, monthly for oecd and yearly for gmdb.")
    volatility_model: Literal['constant', 'garch'] = Field(default='constant', description="'constant' (exact OU transition) or 'garch' (GARCH(1,1) time-varying volatility, Bollerslev 1986). 'garch' requires method='hull_white'.")
    condition_on_business_cycle: bool = Field(default=False, description="Add an additive drift term on the leading indicator's step-to-step change (business-cycle conditioning). Requires leading_indicator.enabled=true; incompatible with volatility_model='garch'.")
    risk_neutral_forward_curve: bool = Field(default=False, description="Used when measure='risk_neutral' and method='hull_white'. False (default, v1) uses a deterministic flat path at today's observed short-rate level (InterestRates.calibrate_risk_neutral()). True (Phase 2) instead uses a genuinely stochastic, forward-curve-consistent Hull-White short rate: mean_reversion_speed/volatility historically fit exactly as the real_world Hull-White process, but the drift target theta(t) is forced to reproduce today's whole observed forward curve (the four YIELD_CURVE_TENORS treasury tenors) rather than a fixed historical mean; see interest_rates_model.HullWhiteForwardParams and InterestRates.calibrate_risk_neutral_forward.")
    inflation_name: str = Field(default='inflation', description="Used when method='wilkie_consols'. Which configured inflation[i].name this entry's dlnQ(t) term reads; also forces this entry's calibration period to that inflation entry's period.")
    inflation_weight: float = Field(default=1.0, description="Used when method='wilkie_consols'. CW, fixed (not fit): Wilkie's own published value.")
    inflation_decay: float = Field(default=0.05, gt=0, lt=1, description="Used when method='wilkie_consols'. CD, fixed (not fit): Wilkie's own Reduced Basis value.")
    target_source: Literal['long_term_rate', 'ewma'] = Field(default='long_term_rate', description="Used when method='hibbert_two_factor'. 'long_term_rate' (the default) refetches this same country's long-term rate (target_term/target_ticker) as a real, independently-simulated slow/target factor. 'ewma' instead derives the target as a deterministic EWMA of this entry's own historical path (target_smoothing): no second fetch, no second factor, no correlation.")
    target_term: Literal['short', 'long'] = Field(default='long', description="Used when method='hibbert_two_factor', target_source='long_term_rate', and source='oecd'. Must differ from this entry's own term: a same-term target would be an identical series to the fast leg.")
    target_ticker: str = Field(default='^TNX', description="Used when method='hibbert_two_factor', target_source='long_term_rate', and source='ticker'. Must differ from this entry's own ticker: a same-ticker target would be an identical series to the fast leg.")
    target_smoothing: float = Field(default=0.05, gt=0, lt=1, description="Used when method='hibbert_two_factor' and target_source='ewma'. The EWMA weight on each new observation; smaller means a slower-moving target (more history retained). Not itself statistically fitted, a fixed hyperparameter like DividendGrowthConfig.carried_forward_weight.")
    history_source: Literal['millennium', 'jst', 'oecd'] | None = Field(default=None, description="Fit the dynamics (speed, volatility, long-run level) on decades or centuries of history instead of the recent window, at the maturity term names; today's level and the correlation series still come from source. 'oecd': the OECD's short- or long-term rate of country, yearly from 1950; 'millennium': the Bank of England's Bank Rate from 1694 or long government bond (consols) yields (country 'United Kingdom'); 'jst': the Jordà-Schularick-Taylor bill return of country from 1870, short only (needs accept_licence). method hull_white or cir, constant volatility only; see long_history_controller.LongHistory.")
    history_start_year: int | None = Field(default=None, description='With history_source: leave out years before this one, e.g. 1900.')
    accept_licence: bool = Field(default=False, description="Confirms non-commercial use, which history_source 'jst' requires (CC BY-NC-SA 4.0).")
    zero_lower_bound: bool = Field(default=False, description='Keep this rate at or above 0%, as some scenario generators do. The model still evolves underneath as a shadow rate that may go negative (Black 1995); the rate every path, discount factor and linked factor sees is max(shadow, 0), so a rate that touched zero climbs back from where the shadow went rather than from 0. Off by default: negative rates did happen (euro, yen, Swiss franc). Real-world entries only.')
    history_volatility: Literal['history', 'recent'] = Field(default='history', description="With history_source: 'history' (default) takes the volatility from the long history along with the speed and level; 'recent' keeps the volatility fitted on the recent window, so a calm or volatile recent era sets how much the rate swings while the long history sets how fast it reverts.")
    long_run_anchor: Literal['eiopa', 'dnb'] | None = Field(default=None, description="Pull the rate toward an official curve's forward rates instead of one fitted long-run level: 'eiopa' uses EIOPA's risk-free curve for this entry's currency (USD, EUR or GBP), the 1-year forward rate for term short and the 10-year forward for term long, starting at every scenario date, ending at EIOPA's ultimate forward rate (Solvency II's reference). 'dnb' (EUR only) follows the median of De Nederlandsche Bank's real-world scenario set instead, its 1-year or 10-year nominal rate, the reference for Dutch pension funds. Speed and volatility stay fitted. An explicit beliefs.long_run_mean takes precedence. hull_white or cir, real_world, constant volatility only.")
    beliefs: OUBeliefs = Field(default_factory=OUBeliefs)
```

Interest-rate factor settings: one entry per country/region "cloud" (a short
rate, a term picked via `term`). `ScenariosConfig.interest_rates` is a list of
these; each becomes its own correlated factor in the simulation, keyed by
`name`. At least one entry is required: interest rate, like equity, is an
always-on MVP factor, not opt-in.

`source: "ticker"` (default) calibrates against a Yahoo Finance treasury-yield
ticker via `get_historical_data()`, US-only in practice, since Yahoo has no
sovereign-yield ticker for other countries. `source: "oecd"` calibrates against
Finance Toolkit's country-parameterized OECD short/long-term interest rate series
(`economics.get_short_term_interest_rate`/`get_long_term_interest_rate`, the same
data source `inflation`/`unemployment`/`fx` already use); genuinely worldwide,
but only `period: "monthly"`/`"quarterly"`/`"yearly"` (no daily OECD series). `source: "gmdb"`
calibrates against the same two Finance Toolkit calls but backed by its Global
Macro Database instead (`gmdb_source=True`); it covers countries outside the
OECD's ~38-member roster, at the cost of `period: "yearly"` only (GMDB has no
monthly/quarterly series; enforced below, not silently truncated). All three
sources are normalized to a decimal fraction (`0.06` = 6%) before fitting, so
`interest_rate` stays internally consistent regardless of which entry uses
which source.

`volatility_model: "garch"` is only valid with `method: "hull_white"`: CIR's own
square-root diffusion scaling is a different volatility specification,
incompatible with also layering GARCH on top in v1. Belief overrides currently
only apply when `volatility_model` is `"constant"`; GARCH-calibrated parameters
are used as calibrated, unmodified. `condition_on_business_cycle: true` requires
`leading_indicator.enabled: true` and is incompatible with `volatility_model:
"garch"` in v1; also forces this factor's calibration to use
`leading_indicator.period` rather than its own `period`, so the two series align
(see `LeadingIndicator`).

`method: "wilkie_consols"` switches this entry to Wilkie's (1986) Reduced Basis
Consols-yield process (see `interest_rates_model.WilkieConsolsParams`), a
LEGACY model: it assumes the inflation-adjusted real long-term yield stays
positive throughout the fit window, an assumption the 2020-2022 COVID/ZIRP
era genuinely broke across most developed markets (verified against live
UK/US OECD data), not just Wilkie's own pre-1982 UK data. Cap
`ScenariosConfig.toolkit.end_date` before that era when using this method
against real data spanning it. Forces this entry's calibration period to its
paired `inflation_name` entry's period; requires `inflation_name` to match a
configured `inflation[i].name`; incompatible with `volatility_model="garch"`
or `condition_on_business_cycle` (Wilkie's cascade has no such concepts).

`method: "hibbert_two_factor"` switches this entry to Hibbert/Barrie & Hibbert
(2001)'s two-factor structure: the short rate mean-reverts not to a fixed
long-run level but to a second, slower factor's own currently simulated
level (see `calibration_model.MovingTargetOUParams`). The paper extracts that
slow factor via Kalman-filtered latent state, which this project has no
infrastructure for; `target_source` picks a documented, observable-data
approximation instead:

- `"long_term_rate"` (the default): the slow leg is the *same* country's
  long-term rate, refetched via `target_term` (source="oecd") or
  `target_ticker` (source="ticker"), a real, independently fetched second
  series, registered as its own correlated factor (`f"{name}_target"`,
  mirroring commodities' `method="schwartz_smith"` two-name registration),
  plain-OU-fit via the existing `fit_ou_process` unchanged. The fast leg
  reads that factor's already-simulated level each step, a real functional
  dependency (see `Scenarios._build_dependency_graph`).
- `"ewma"`: the slow leg is a deterministic EWMA of this entry's *own*
  historical path (`calibration_model.compute_ewma_target`), smoothed by
  `target_smoothing`. No second fetch, no second factor, no correlation, no
  dependency edge. Simulated by a stateful `calibration_model.
  MovingTargetEWMAStepper` instead.

Incompatible with `volatility_model="garch"`, `condition_on_business_cycle`,
and any belief override in v1 (same reasoning as `wilkie_consols`).

`method: "knw"` switches this entry to a bivariate discrete-time VAR(1)
coupling with a paired `inflation_name` entry (see `knw_model.KnwParams`):
the constant-volatility simplification of DNB's own CP2022/KNW scenario-set
methodology, jointly fit with that paired entry rather than in isolation.
Genuine two-way drift coupling: this entry's next-period level depends on
*both* its own and the paired inflation entry's current level, and vice versa
(unlike `condition_on_interest_rate`'s one-way, change-based sensitivity;
see `Knw` for a comparison). Requires a matching
`inflation[j]` entry with `method="knw"` naming this entry back via its own
`interest_rate_name`, and the same `period` as that entry (the joint OLS fit
needs both series date-alignable at one shared frequency); both enforced at
`ScenariosConfig` level, not re-checked here. Incompatible with
`volatility_model="garch"`, `condition_on_business_cycle`, and any belief
override (`KnwParams` has no `mean_reversion_speed`/`long_run_mean` in the OU
sense `OUBeliefs` overrides, the same reasoning `wilkie_consols`/
`hibbert_two_factor` disallow them).

`method: "knw_sv"` is the stochastic-volatility extension of `"knw"`: the same
mutual pairing and requirements above apply verbatim (the paired `inflation[j]`
entry must also set `method="knw_sv"`, not `"knw"`; the two methods pair with
themselves only, not each other), but the joint fit adds a latent CIR/Heston
variance factor `v` (see `knw_sv_model.fit_knw_sv_triple`) that drift-couples
into and scales the volatility of both legs, rather than folding its constant
contribution into their intercepts. See `KnwSv`.

## InflationConfig

```python
class InflationConfig(_StrictModel):
    name: str = 'inflation'
    country: str = 'United States'
    source: Literal['oecd', 'gmdb'] = Field(default='oecd', description="'oecd' (FinanceToolkit's OECD Consumer Price Index, period='monthly'/'quarterly'/'yearly') or 'gmdb' (its Global Macro Database; covers countries outside the OECD roster, period='yearly' only).")
    currency: str = Field(default='USD', description='Which currency this inflation series is denominated in. Descriptive metadata only in v1, consumed by financescenarios.reporting.')
    measure: Literal['real_world', 'risk_neutral'] = Field(default='real_world', description="'real_world' (P-measure, the default) or 'risk_neutral'. Valid paired with method='knw_sv' (selects KnwSvQ's completely-affine Q-measure params for this leg, see `KnwSvQ`) or method='ou' (a standalone Nelson-Siegel TIPS-breakeven forward-curve snapshot for the US, UK or euro area, keyless, see tips_breakeven_decay and https://www.jeroenbouma.com/projects/financescenarios/docs/configuration). No other method has a Q-measure counterpart.")
    period: str = 'monthly'
    method: Literal['ou', 'wilkie_ar1', 'hibbert_two_factor', 'knw', 'knw_sv'] = Field(default='ou', description="'ou' (continuous-time-discretized Ornstein-Uhlenbeck, the default), 'wilkie_ar1' (Wilkie 1986's original directly-fit discrete AR(1) force-of-inflation process), 'hibbert_two_factor' (Hibbert/Barrie & Hibbert 2001's fast-inflation-reverts-to-a-moving-'expected inflation'-target structure; see target_source), 'knw' (a bivariate VAR(1) coupling with a paired interest_rates[] entry; see interest_rate_name), or 'knw_sv' (knw's stochastic-volatility extension, see `KnwSv`). 'wilkie_ar1'/'hibbert_two_factor'/'knw'/'knw_sv' are incompatible with volatility_model='garch', condition_on_business_cycle, and any belief override.")
    target_source: Literal['coarser_period', 'ewma'] = Field(default='coarser_period', description="Used when method='hibbert_two_factor'. 'coarser_period' (the default) fetches this same country's CPI growth again at target_period (a coarser frequency than this entry's own period) as a real, independently-simulated slow/target factor. 'ewma' instead derives the target as a deterministic EWMA of this entry's own historical path (target_smoothing): no second fetch, no second factor, no correlation.")
    target_period: Literal['quarterly', 'yearly'] = Field(default='yearly', description='Used when method=\'hibbert_two_factor\' and target_source=\'coarser_period\'. Must be strictly coarser than this entry\'s own period (e.g. period=\'monthly\' allows target_period=\'quarterly\' or \'yearly\'; period=\'quarterly\' only allows \'yearly\'); a same-or-finer target wouldn\'t actually be the slower of the two factors. A documented simplification: FinanceToolkit\'s period-over-period CPI growth is a genuinely different-*scale* quantity at different periods (e.g. a ~0.2-0.3% monthly reading vs. a ~2-4% yearly reading isn\'t monthly inflation being an order of magnitude calmer, just a shorter compounding window). Unlike interest_rates\' long_term_rate variant (an already annualized level at any period), pairing raw growth rates at genuinely different frequencies here mixes units in the fit\'s gap term. The fitted reversion speed/volatility are still well-defined (verified against live US CPI data), just not on a directly "years to close the gap" reading the way a same-unit pair would be.')
    target_smoothing: float = Field(default=0.05, gt=0, lt=1, description="Used when method='hibbert_two_factor' and target_source='ewma'. The EWMA weight on each new observation; smaller means a slower-moving target (more history retained). Not itself statistically fitted, a fixed hyperparameter like DividendGrowthConfig.carried_forward_weight.")
    tips_breakeven_decay: float = Field(default=0.7308, gt=0, description="Used when measure='risk_neutral' and method='ou'. Nelson-Siegel decay parameter (lambda) for the TIPS-breakeven curve fit; same default as yield_curve/credit_term_structure/hjm.")
    volatility_model: Literal['constant', 'garch'] = Field(default='constant', description="'constant' (exact OU transition) or 'garch' (GARCH(1,1) time-varying volatility, Bollerslev 1986).")
    condition_on_business_cycle: bool = Field(default=False, description="Add an additive drift term on the leading indicator's step-to-step change (business-cycle conditioning). Requires leading_indicator.enabled=true; incompatible with volatility_model='garch'.")
    condition_on_interest_rate: bool = Field(default=False, description="Add an additive drift term on the paired interest_rates[] entry's step-to-step change: the structural nominal-rate/inflation coupling used by joint macro-finance affine term-structure models (Dai & Singleton, 2000), a simplified real-world analogue of DNB's own CP2022/KNW scenario-set methodology (see `Knw`). Requires interest_rate_name to match a configured interest_rates[i].name (which must already be calibrated, enforced by calibrate_all()'s ordering, not re-checked here); incompatible with volatility_model='garch' and condition_on_business_cycle (fit_ou_process_with_covariate only supports one covariate).")
    interest_rate_name: str = Field(default='interest_rate', description="Used when condition_on_interest_rate=true or method in ('knw', 'knw_sv'). Which configured interest_rates[i].name this entry's rate-sensitivity term reads its step-to-step change from (condition_on_interest_rate) or its coupled VAR(1)/knw_sv pair reads/is read by.")
    history_source: Literal['millennium', 'shiller'] | None = Field(default=None, description="Fit the dynamics (speed, volatility, long-run level) on centuries of history instead of the recent window; today's level and the correlation series still come from source. 'millennium': UK consumer price inflation from 1209 (country 'United Kingdom'); 'shiller': US December-to-December inflation from 1872 (country 'United States'). method ou, constant volatility only; see long_history_controller.LongHistory.")
    history_start_year: int | None = Field(default=None, description='With history_source: leave out years before this one, e.g. 1900.')
    beliefs: OUBeliefs = Field(default_factory=OUBeliefs)
```

Inflation factor settings: one entry per country. `ScenariosConfig.inflation`
is a list of these; each becomes its own correlated factor in the simulation,
keyed by `name`. At least one entry is required. Belief overrides currently only
apply when `volatility_model` is `"constant"`; GARCH-calibrated parameters are
used as calibrated, unmodified. `condition_on_business_cycle: true` requires
`leading_indicator.enabled: true` and forces this factor's calibration to use
`leading_indicator.period` rather than its own `period`.

`source: "oecd"` (default) calibrates against Finance Toolkit's OECD Consumer
Price Index series (`period` "monthly"/"quarterly"/"yearly"). `source: "gmdb"`
calibrates against its Global Macro Database instead; it covers countries outside
the OECD roster, at the cost of `period: "yearly"` only (enforced below).

`method: "wilkie_ar1"` switches this entry to Wilkie's (1986) original
force-of-inflation AR(1) (a directly-fit discrete AR(1), no continuous-time
reinterpretation; see `calibration_model.AR1Params`) instead of the default
continuous-time-discretized Ornstein-Uhlenbeck fit (Ahlgrim/D'Arcy/Gorvett
2005's treatment). Incompatible with `volatility_model="garch"` and
`condition_on_business_cycle` (Wilkie's cascade has no such concepts) and with
any belief override (Wilkie's AR(1) has no `long_run_mean`/`mean_reversion_speed`
in the OU sense `OUBeliefs` overrides).

`method: "hibbert_two_factor"` switches this entry to Hibbert/Barrie & Hibbert
(2001)'s two-factor structure: actual inflation mean-reverts not to a fixed
long-run level but to a second, slower "expected inflation" factor's own
currently simulated level (see `calibration_model.MovingTargetOUParams`). The
paper extracts that slow factor via Kalman-filtered latent state, which this
project has no infrastructure for; `target_source` picks a documented,
observable-data approximation instead:

- `"coarser_period"` (the default): the slow leg is the *same* country's CPI
  growth refetched at `target_period` (a coarser sampling frequency than this
  entry's own `period`, e.g. yearly vs. monthly), a real, independently
  fetched second series, registered as its own correlated factor
  (`f"{name}_target"`, mirroring commodities' `method="schwartz_smith"`
  two-name registration), plain-OU-fit via the existing `fit_ou_process`
  unchanged. The fast leg reads that factor's already-simulated level each
  step, a real functional dependency (see `Scenarios._build_dependency_graph`).
- `"ewma"`: the slow leg is a deterministic EWMA of this entry's *own*
  historical path (`calibration_model.compute_ewma_target`), smoothed by
  `target_smoothing`. No second fetch, no second factor, no correlation, no
  dependency edge. Simulated by a stateful `calibration_model.
  MovingTargetEWMAStepper` that tracks the running EWMA of this factor's own
  simulated path instead.

Incompatible with `volatility_model="garch"`, `condition_on_business_cycle`,
and any belief override in v1 (`MovingTargetOUParams` has no
`long_run_mean`/`mean_reversion_speed` in the OU sense `OUBeliefs` overrides,
the same reason `wilkie_ar1` disallows them).

`method: "knw"` switches this entry to a bivariate discrete-time VAR(1)
coupling with a paired `interest_rates[i]` entry (see `knw_model.KnwParams`):
the interest_rates side of the same pairing `InterestRateConfig`'s own
`method="knw"` docstring describes; both entries must set `method="knw"` and
name each other back (`interest_rate_name` here, `inflation_name` there).
Incompatible with `volatility_model="garch"`, `condition_on_business_cycle`,
`condition_on_interest_rate` (a different, one-way coupling mechanism; see
`Knw`), and any belief override.

`method: "knw_sv"` is the stochastic-volatility extension of `"knw"`; see
`InterestRateConfig`'s own `method="knw_sv"` docstring and
`KnwSv`. Same mutual-pairing/period/incompatibility rules as
`"knw"`, and pairs with itself only (a `"knw_sv"` entry's partner must also be
`"knw_sv"`, not `"knw"`). `measure="risk_neutral"` paired with `method="knw_sv"`
selects `KnwSvQ`'s completely-affine Q-measure params for this leg instead of
the P-measure fit (see `KnwSvQ`).

`measure="risk_neutral"` paired with `method="ou"` instead selects a
standalone Q-measure snapshot: a Nelson-Siegel instantaneous forward-rate
curve fit against the daily breakeven inflation curve (nominal minus inflation-linked bond yields) of the
United States, the United Kingdom or the euro area through Germany, read without a key from the US Treasury
(FRED when a FRED key is set), the Bank of England and the Bundesbank, ignoring `source`/`period`/`volatility_model`/
`condition_on_business_cycle`/`condition_on_interest_rate` entirely (see
`tips_breakeven_decay` and the configuration documentation's Real-world and risk-neutral measures and
Inflation sections).
No other `method` has a Q-measure counterpart.

## UnemploymentConfig

```python
class UnemploymentConfig(_StrictModel):
    name: str = 'unemployment'
    country: str = 'United States'
    source: Literal['oecd', 'gmdb'] = Field(default='oecd', description="'oecd' (FinanceToolkit's OECD unemployment rate, worldwide within the OECD roster) or 'gmdb' (its Global Macro Database; covers countries outside the OECD roster; requires the paired inflation[i].period to be 'yearly', since this entry has no period of its own).")
    inflation_name: str = Field(default='inflation', description="Which configured inflation[i].name drives this entry's Phillips-curve term.")
    condition_on_business_cycle: bool = Field(default=False, description="Add a *second* Phillips-curve-style covariate term on the leading indicator's step-to-step change, alongside the existing inflation term: a genuine two-covariate extension (unemployment_model.fit_unemployment_process's own business_cycle_sensitivity), not the shared single-covariate mechanism other condition_on_business_cycle factors use. Requires leading_indicator.enabled=true, and leading_indicator.period to equal this entry's paired inflation_name entry's own period (both covariates must be sampled at the same frequency to date-align in the regression).")
    beliefs: UnemploymentBeliefs = Field(default_factory=UnemploymentBeliefs)
```

Unemployment factor settings: one entry per region. `ScenariosConfig.unemployment`
is a list of these; each becomes its own correlated factor, keyed by `name`. At
least one entry is required. `inflation_name` names which `inflation[i].name`
entry this region's Phillips-curve term reads its step-to-step change from during
simulation (must match a configured inflation entry); calibration itself still
fetches this entry's own `country`-based inflation series independently, for the
Phillips-curve regression fit.

`source: "oecd"` (default) or `"gmdb"` (Finance Toolkit's Global Macro Database;
covers countries outside the OECD roster). Since this entry has no `period` of
its own (it's always forced to its paired inflation entry's, see
`inflation_name` above), `source="gmdb"` requires that paired inflation entry's
`period` to be `"yearly"`, enforced at `ScenariosConfig` level, not re-checked
here (mirrors how the mutual `method="knw"` pairing's own period-match check
lives there too).

## EquityConfig

```python
class EquityConfig(_StrictModel):
    name: str = 'equity'
    ticker: str = 'SPY'
    asset_class: str | None = Field(default=None, description="An asset class without a public return index, e.g. 'Private Equity', 'Infrastructure', 'Hedge Funds' or 'Private Credit' (a key of ASSET_CLASS_PROXIES): sets ticker to the listed fund the Finance Toolkit's economics.get_asset_class_proxies uses for it. Listed prices are marked to market daily, so they swing more and move more with equities than the appraisal-based returns private funds report, and they are net of the fund's fees.")
    currency: str = Field(default='USD', description="The ticker's listing/settlement currency (not necessarily its underlying regional exposure; e.g. VGK/EWJ/FXI are USD-listed ETFs despite tracking non-US markets). Descriptive metadata only in v1, consumed by financescenarios.reporting.")
    measure: Literal['real_world', 'risk_neutral'] = Field(default='real_world', description="'real_world' (P-measure regime-switching fit, the default) or 'risk_neutral' (Q-measure: geometric Brownian motion with drift = risk_free_rate - dividend_yield, volatility per volatility_source, options-implied where available with a realized-vol fallback). Belief overrides don't apply to risk_neutral entries. Incompatible with method='wilkie_derived'.")
    volatility_source: Literal['implied', 'svi', 'realized', 'heston'] = Field(default='implied', description="Only used when measure='risk_neutral': where the flat GBM volatility comes from. 'implied' (default) reads the at-the-money strike from one raw per-strike Black-Scholes inversion at FinanceToolkit's nearest expiration. 'svi' reads the ATM value off FinanceToolkit's SVI-fitted, calendar-arbitrage-checked volatility surface (options.get_volatility_surface) at the longest fitted expiration: smoothed across the whole smile instead of passing one quote's noise straight through, and a longer expiry is the better match for a GBM simulated over years. 'realized' skips options data entirely and uses the annualized standard deviation of historical log-returns (the right choice for tickers without a liquid options market, e.g. most sector/regional/style ETFs). 'heston' fits the Heston (1993) stochastic-volatility model to the SVI surface at six expirations from one to twelve months, so the simulated paths carry the market's smile and volatility term structure instead of one flat volatility. 'implied', 'svi' and 'heston' fall back to realized volatility (flat GBM) with a logged warning when options data is unavailable.")
    n_regimes: int = Field(gt=1, default=2)
    period: str = 'monthly'
    method: Literal['regime_switching', 'wilkie_derived', 'hibbert_regime_switching', 'knw_sv'] = Field(default='regime_switching', description="'regime_switching' (Baum-Welch 2-state fit, the default), 'wilkie_derived' (Wilkie 1986: price = dividend_growth index / dividend_yield, no own calibration; a same-step lookup-and-divide over two already-simulated sibling factors, see equities_model.EquityDerivedParams), 'hibbert_regime_switching' (Hibbert/Barrie & Hibbert 2001: the same Baum-Welch 2-state fit, but on log-returns in excess of a paired nominal short rate; see nominal_rate_name, equities_model.fit_hibbert_regime_switching), or 'knw_sv' (DNB CP2022 Technical Appendix eq. 4/5, P-measure/historical-fit-only simplification: log-return drift = the paired nominal_rate_name's own current level plus a constant risk premium, variance scaled by the same latent factor v that interest_rate/inflation already share, see knw_sv_model.fit_knw_sv_equity_leg; NOT DNB's own options-calibrated risk premium/variance, this project has no such market data). 'wilkie_derived' requires dividend_growth_name/dividend_yield_name, ignores ticker/n_regimes/period, and is incompatible with measure='risk_neutral' or a belief override. 'hibbert_regime_switching'/'knw_sv' both require nominal_rate_name and are incompatible with measure='risk_neutral' in v1; 'knw_sv' additionally requires that named interest_rates[] entry to itself use method='knw_sv' (there's no v to share otherwise).")
    dividend_growth_name: str | None = Field(default=None, description="Required when method='wilkie_derived'. Which configured dividend_growth[i].name this entry's price numerator reads.")
    dividend_yield_name: str | None = Field(default=None, description="Required when method='wilkie_derived'. Which configured dividend_yield[i].name this entry's price denominator reads.")
    nominal_rate_name: str | None = Field(default=None, description="Required when method='hibbert_regime_switching' or method='knw_sv'. Which configured interest_rates[i].name this entry reads its nominal short rate from: for 'hibbert_regime_switching', fit against log-returns in excess of that rate, with the already-simulated level added back on top of the regime draw at simulation time (a real functional dependency, see Scenarios._build_dependency_graph); for 'knw_sv', the same entry this leg shares its latent variance factor v with (that entry must itself use method='knw_sv').")
    condition_on_business_cycle: bool = Field(default=False, description="Make the regime-switching transition matrix itself a function of the leading indicator's level (Filardo 1994's time-varying-transition-probability extension), instead of one fixed, unconditional matrix, a structurally different mechanism from every other condition_on_business_cycle flag in this project (those add an additive drift term; this one changes the discrete regime-transition dynamics, see equities_model.RegimeTVTPParams and `LeadingIndicator`). Requires leading_indicator.enabled=true and method='regime_switching'; not supported for 'wilkie_derived'/'hibbert_regime_switching'/'knw_sv' in v1.")
    history_source: Literal['shiller', 'jst'] | None = Field(default=None, description="Fit the regimes on long history instead of the ticker's: 'shiller' is the US S&P Composite total return, monthly from 1871; 'jst' the yearly equity total return of history_country from 1870 (needs accept_licence). Today's price and the correlation series still come from ticker. method regime_switching, real_world, without condition_on_business_cycle; see long_history_controller.LongHistory.")
    history_country: str = Field(default='United States', description="The JST country for history_source 'jst'.")
    history_start_year: int | None = Field(default=None, description='With history_source: leave out years before this one, e.g. 1950.')
    accept_licence: bool = Field(default=False, description="Confirms non-commercial use, which history_source 'jst' requires (CC BY-NC-SA 4.0).")
    beliefs: EquityBeliefs = Field(default_factory=EquityBeliefs)
```

Equity factor settings. One entry is one regime-switching "cloud": a single
ticker (a broad index, a sector ETF, a regional ETF, a style/factor ETF, ...).
`ScenariosConfig.equities` is a list of these; each becomes its own correlated
factor in the simulation, keyed by `name`. At least one entry is required:
equity, unlike fx/credit, is an always-on MVP factor, not opt-in.

## FXConfig

```python
class FXConfig(_StrictModel):
    name: str = 'fx'
    country: str = Field(default='EA20', description="The country (or currency area) whose currency is paired against the US dollar. The OECD exchange-rate series is keyed by currency area, not member state: 'EA20' is the euro area, and an individual member ('Germany', 'France', ...) has no series of its own there, unlike interest_rates/inflation/unemployment, which do take a member state's name.")
    currency: str | None = Field(default=None, description="The ISO code of the currency this pair quotes against the dollar, e.g. 'EUR'. Read by financescenarios.reporting to convert into that currency. When unset it is taken from an interest_rates/inflation entry with the same country, or 'EUR' for the OECD's euro-area codes ('EA20', 'EA19', 'Euro Area').")
    source: Literal['oecd', 'gmdb'] = Field(default='oecd', description="'oecd' (FinanceToolkit's OECD exchange rate, period='monthly'/'quarterly'/'yearly') or 'gmdb' (its Global Macro Database; covers countries outside the OECD roster, period='yearly' only).")
    period: str = 'monthly'
    measure: Literal['real_world', 'risk_neutral'] = Field(default='real_world', description="'real_world' (P-measure GBM fit to historical log-returns, the default) or 'risk_neutral' (Q-measure: covered interest-rate parity; drift = foreign short rate minus US short rate, since the OECD quotes foreign currency per USD, both read from this run's own calibrated interest_rates entries for that country and the United States; volatility unchanged from the historical fit; see FX.calibrate_risk_neutral). Belief overrides don't apply to risk_neutral entries. This is a static per-calibration drift, not the dynamic per-step interest-rate-parity conditioning drift_mode='irp' provides under the real-world measure.")
    drift_mode: Literal['historical', 'irp', 'random_walk'] = Field(default='historical', description="'historical' (GBM drift fit to historical log-returns, the default) or 'irp' (dynamic per-step uncovered-interest-rate-parity conditioning: at each simulated step, drift is replaced by the instantaneous differential between domestic_rate_name's and foreign_rate_name's already-simulated short-rate paths that step, rather than a fixed calibrated value). Distinct from measure='risk_neutral' (a static drift computed once at calibration time); 'irp' is dynamic and real-world-measure-compatible, requiring domestic_rate_name (and, optionally, foreign_rate_name) to name configured interest_rates[] entries. 'random_walk' keeps the historical volatility but drops the trend, so the median rate stays at today's level instead of extrapolating the sample's appreciation (Meese and Rogoff 1983, https://doi.org/10.1016/0022-1996(83)90017-X).")
    domestic_rate_name: str | None = Field(default=None, description="Required when drift_mode='irp'. Which configured interest_rates[].name entry supplies the domestic (USD) leg of the rate differential. No natural default: unlike foreign_rate_name, there's no single canonical 'the USD one' among possibly several interest_rates entries.")
    foreign_rate_name: str | None = Field(default=None, description="Used when drift_mode='irp'. Which configured interest_rates[].name entry supplies the foreign leg of the rate differential. Defaults to this fx entry's own country, slugified + '_short_rate' (the same auto-pairing convention UnemploymentCountry.inflation_name uses elsewhere in this file) when not explicitly set.")
    beliefs: FXBeliefs = Field(default_factory=FXBeliefs)
```

FX factor settings: opt-in, one entry per currency pair. `ScenariosConfig.fx`
is a list of these; an empty list means no FX factors are simulated. Each
entry is a geometric Brownian motion process on the USD exchange rate against
one other country's currency (any country Finance Toolkit's OECD-backed
`economics.get_exchange_rates` covers, not US-only), correlation-linked to
the rest of the model.

`source: "oecd"` (default) calibrates against Finance Toolkit's OECD exchange-rate
series (`period` "monthly"/"quarterly"/"yearly"). `source: "gmdb"` calibrates
against its Global Macro Database instead; it covers countries outside the OECD
roster, at the cost of `period: "yearly"` only (enforced below).

## CreditConfig

```python
class CreditConfig(_StrictModel):
    name: str = 'credit'
    currency: str = Field(default='USD', description="The spread's currency: USD for the US sources, defaulting to EUR for 'corporate' Germany and 'borrowing_cost', AUD for 'corporate' Australia. Read by financescenarios.reporting.")
    dimension: Literal['maturity', 'rating', 'moodys', 'corporate', 'borrowing_cost'] = Field(default='maturity', description="Which spread to fit: the ICE BofA option-adjusted spread by 'maturity' (uses maturity_bucket, one of credit_controller.MATURITY_BUCKETS) or by 'rating' (uses rating_bucket, one of credit_controller.RATING_BUCKETS), both with three years of history on FRED; or 'moodys': Moody's Aaa or Baa yield over the 10-year Treasury, or Baa minus Aaa (rating_bucket one of credit_controller.MOODYS_BUCKETS), monthly from 1953; 'corporate': a country's corporate bond spread over its government bonds (country 'Germany', rating_bucket 'All ratings', from 1957; or 'Australia', rating_bucket e.g. 'BBB 10Y', from 2005); or 'borrowing_cost': the ECB's composite cost of new bank loans to companies (country 'Euro Area' or a member, from 2003), a rate level rather than a spread. The last two are monthly.")
    country: str | None = Field(default=None, description="Used when dimension is 'corporate' (default 'Germany') or 'borrowing_cost' (default 'Euro Area'); must stay unset otherwise.")
    maturity_bucket: str = Field(default='7-10 Years', description="One of credit_controller.MATURITY_BUCKETS. Used when dimension='maturity'.")
    rating_bucket: str = Field(default='BBB', description="One of credit_controller.RATING_BUCKETS for dimension='rating', of credit_controller.MOODYS_BUCKETS ('Aaa', 'Baa', 'Baa - Aaa') for dimension='moodys', or of credit_controller.CORPORATE_BUCKETS[country] for dimension='corporate' (default 'All ratings').")
    period: str = 'daily'
    volatility_model: Literal['constant', 'garch'] = Field(default='constant', description="'constant' (exact OU transition) or 'garch' (GARCH(1,1) time-varying volatility, Bollerslev 1986).")
    condition_on_business_cycle: bool = Field(default=False, description="Add an additive drift term on the leading indicator's step-to-step change (business-cycle conditioning). Requires leading_indicator.enabled=true; incompatible with volatility_model='garch'.")
    beliefs: CreditBeliefs = Field(default_factory=CreditBeliefs)
```

Credit spread factor settings: opt-in, one entry per spread bucket.
`ScenariosConfig.credit` is a list of these; an empty list means no credit
factors are simulated. Each entry is a mean-reverting process on one ICE BofA
option-adjusted spread bucket, correlation-linked to the rest of the model.
Belief overrides currently only apply when `volatility_model` is `"constant"`.

Data sources: the ICE BofA spreads (`"maturity"`, `"rating"`) and Moody's
(`"moodys"`) are US only. `"corporate"` adds Germany's and Australia's corporate
bond spreads over government bonds and `"borrowing_cost"` the ECB's cost of bank
loans to companies in the euro area or a member, both monthly, read per `country`.
There is no euro or UK spread by rating: those indices are licensed data.

## CommodityConfig

```python
class CommodityConfig(_StrictModel):
    name: str = 'commodity'
    ticker: str = Field(default='CL=F', description="Any commodity/futures ticker the Toolkit instance includes, e.g. CL=F (WTI crude), GC=F (gold), NG=F (natural gas), HG=F (copper). method='schwartz_smith' additionally needs this ticker to map to a FinanceToolkit-supported forward-curve commodity name (Crude Oil, Natural Gas, Gold, Silver, Copper, Corn, Wheat, Soybeans) for its risk-neutral leg, and for a well-identified real-world diffusion fit; see commodities_controller._COMMODITY_NAMES.")
    currency: str = Field(default='USD', description='Commodity scenarios are USD-quoted globally by convention. Descriptive metadata only in v1, consumed by financescenarios.reporting.')
    period: str = 'daily'
    method: Literal['single_factor', 'schwartz_smith'] = Field(default='single_factor', description="'single_factor' (default): Schwartz (1997) mean-reverting log-price process. 'schwartz_smith': Schwartz & Smith (2000) two-factor process (short-term deviation + long-term equilibrium), simulated as f'{name}_chi'/f'{name}_xi'.")
    measure: Literal['real_world', 'risk_neutral'] = Field(default='real_world', description="'real_world' (P-measure, the default) or 'risk_neutral' (Q-measure, calibrated against the ticker's real observed forward curve). Only 'schwartz_smith' has a defined risk-neutral leg; single-factor Schwartz (1997) has no market-implied drift to calibrate against in this project.")
    contracts: int = Field(default=12, gt=0, description="method='schwartz_smith' only: number of sequential monthly forward contracts to attempt to fetch for the diffusion fit / risk-neutral calibration (forwarded to get_commodity_forward_curve). Ignored for method='single_factor'.")
    long_term_window_years: float = Field(default=3.0, gt=0, description="method='schwartz_smith' only: trailing window (years) used to proxy the long-term equilibrium component; see fit_schwartz_smith_process's own docstring. Ignored for method='single_factor'.")
    volatility_model: Literal['constant', 'garch'] = Field(default='constant', description="method='single_factor' only: 'constant' (Schwartz's own log-price OU fit) or 'garch' (GARCH(1,1) time-varying volatility, Bollerslev 1986). Incompatible with method='schwartz_smith'.")
    condition_on_business_cycle: bool = Field(default=False, description="method='single_factor' only: add an additive drift term on the leading indicator's step-to-step change (business-cycle conditioning). Requires leading_indicator.enabled=true; incompatible with volatility_model='garch' and with method='schwartz_smith'.")
    beliefs: CommodityBeliefs = Field(default_factory=CommodityBeliefs)
```

Commodity factor settings: opt-in, one entry per commodity. `ScenariosConfig.commodities`
is a list of these; an empty list means no commodity factors are simulated.
`method="single_factor"` (the default) is a Schwartz (1997) single-factor
mean-reverting process on the log spot price of one commodity/futures ticker
(e.g. crude oil, gold, natural gas, copper), correlation-linked to the rest of
the model. `method="schwartz_smith"` is Schwartz & Smith's (2000) two-factor
model instead: a short-term deviation and a long-term equilibrium log-price,
simulated as two derived factors named `f"{name}_chi"`/`f"{name}_xi"` (see
`commodities_controller.Commodities.calibrate_schwartz_smith`), each still
correlation-linked to the rest of the model.

## DividendYieldConfig

```python
class DividendYieldConfig(_StrictModel):
    name: str = 'dividend_yield'
    ticker: str = Field(default='SPY', description='Any dividend-paying ticker the Toolkit instance includes.')
    currency: str = Field(default='USD', description="The underlying ticker's listing currency. Descriptive metadata only in v1, consumed by financescenarios.reporting. A yield is a ratio, not itself converted, but tagged the same as its ticker for consistency.")
    window: int = Field(default=252, gt=0, description='Trading days of trailing dividends summed for one yield observation.')
    period: str = 'daily'
    condition_on_inflation: bool = Field(default=False, description="Add Wilkie's (1986) inflation-sensitivity term to the fit. Requires inflation_name to match a configured inflation[i].name; forces this entry's calibration period to that entry's period. Incompatible with a belief override.")
    inflation_name: str = Field(default='inflation', description="Used when condition_on_inflation=true. Which configured inflation[i].name this entry's inflation-sensitivity term reads its step-to-step change from.")
    volatility_model: Literal['constant', 'garch'] = Field(default='constant', description="'constant' (Ahlgrim/D'Arcy/Gorvett's own log-yield OU fit) or 'garch' (GARCH(1,1) time-varying volatility, Bollerslev 1986). Incompatible with condition_on_inflation=true.")
    condition_on_business_cycle: bool = Field(default=False, description="Add an additive drift term on the leading indicator's step-to-step change (business-cycle conditioning). Requires leading_indicator.enabled=true; incompatible with volatility_model='garch' and with condition_on_inflation=true.")
    beliefs: DividendYieldBeliefs = Field(default_factory=DividendYieldBeliefs)
```

Dividend yield factor settings: opt-in, one entry per ticker.
`ScenariosConfig.dividend_yield` is a list of these; an empty list means no
dividend yield factors are simulated. Each entry is an Ahlgrim/D'Arcy/Gorvett
(2005) mean-reverting process on the log of a ticker's trailing dividend yield
(see dividend_yield_controller.py for how the yield itself is derived from
price/dividend data), correlation-linked to the rest of the model.

`condition_on_inflation: true` adds Wilkie's (1986) inflation-sensitivity term
to the fit: the same shape unemployment's Phillips-curve term already uses,
generalized here to dividend yield (see `dividend_yield_model.
fit_dividend_yield_process`). Requires `inflation_name` to match a configured
`inflation[i].name`, and forces this entry's calibration to use that entry's
`period` rather than its own, so the two series align (the same convention
`condition_on_business_cycle` already uses elsewhere). Incompatible with any
belief override in v1.

## DividendGrowthConfig

```python
class DividendGrowthConfig(_StrictModel):
    name: str = 'dividend_growth'
    ticker: str = Field(default='SPY', description='Any dividend-paying ticker the Toolkit instance includes.')
    currency: str = Field(default='USD', description="The underlying ticker's listing currency. Descriptive metadata only in v1, consumed by financescenarios.reporting.")
    window: int = Field(default=252, gt=0, description='Trading days of trailing dividends summed for one dividend index observation.')
    inflation_name: str = Field(default='inflation', description="Which configured inflation[i].name this entry's dlnQ(t) term reads. Also forces this entry's calibration period to that inflation entry's period.")
    dividend_yield_name: str = Field(default='dividend_yield', description="Which configured dividend_yield[i].name this entry's YE(t-1) term reads its own shock from. Must resolve to the same period as inflation_name's entry.")
    carried_forward_weight: float = Field(default=0.2, gt=0, lt=1, description="DD, the fixed EWMA weight on current inflation in the carried-forward inflation influence: Wilkie's own published value.")
    beliefs: DividendGrowthBeliefs = Field(default_factory=DividendGrowthBeliefs)
```

Dividend growth factor settings: opt-in, one entry per ticker. Wilkie
(1986)-specific: unlike dividend_yield (an optional add-on to Ahlgrim/D'Arcy/
Gorvett's default cascade), there is no non-Wilkie dividend growth process in
this project, so every entry always requires a paired `inflation[]` entry
(`inflation_name`) and a paired `dividend_yield[]` entry (`dividend_yield_name`);
see dividend_growth_model.py for the process itself.

Has no `period` field of its own: like `UnemploymentConfig`, it's always
forced to its paired inflation entry's `period` (`inflation_name`'s), since
dlnQ(t) is a direct (not covariate-differenced) driver here and every
regression row needs a genuinely same-period inflation observation, not
just a same *row count* one. The paired `dividend_yield[]` entry must
resolve to that same period too (enforced at calibration time); see
calibration_controller._calibrate_dividend_growth.

## RealEstateConfig

```python
class RealEstateConfig(_StrictModel):
    enabled: bool = False
    country: str = 'United States'
    currency: str = 'USD'
    period: str = 'quarterly'
    source: Literal['house_price', 'commercial'] = Field(default='house_price', description="'house_price' (default): OECD residential house-price growth via get_house_prices(). 'commercial': FRED's (IMF-sourced) US commercial real estate price index growth via get_commercial_real_estate_prices() instead; United States only (that call takes no country argument) and quarterly-only (no annual series), so requires country='United States' and period='quarterly'; also requires a FRED API key. Neither option is a substitute for Ahlgrim/D'Arcy/Gorvett's (2005) original calibration, which used NCREIF's appraisal-smoothed commercial-property index: no open NCREIF equivalent exists; 'commercial' is transaction-based index data, not appraisal-based (see https://www.jeroenbouma.com/projects/financescenarios/docs/coverage).")
    volatility_model: Literal['constant', 'garch'] = Field(default='constant', description="'constant' (exact OU transition) or 'garch' (GARCH(1,1) time-varying volatility, Bollerslev 1986).")
    condition_on_business_cycle: bool = Field(default=False, description="Add an additive drift term on the leading indicator's step-to-step change (business-cycle conditioning). Requires leading_indicator.enabled=true; incompatible with volatility_model='garch'.")
    beliefs: OUBeliefs = Field(default_factory=OUBeliefs)
```

Real estate factor settings: opt-in. A mean-reverting process on house-price
growth (Ahlgrim/D'Arcy/Gorvett 2005, eq. 3.18), correlation-linked to the rest of
the model rather than cascade-dependent (see real_estate_controller.py). Belief
overrides currently only apply when `volatility_model` is `"constant"`.

## YieldCurveConfig

```python
class YieldCurveConfig(_StrictModel):
    enabled: bool = False
    period: str = 'daily'
    decay: float = Field(default=0.7308, gt=0, description='Nelson-Siegel decay parameter (lambda), annualized.')
    source: Literal['yahoo', 'treasury', 'government'] = Field(default='yahoo', description="'yahoo' (default) calibrates against the four standard Yahoo treasury-yield tickers (term_structure_model.YIELD_CURVE_TENORS: 3M/5Y/10Y/30Y). 'treasury' calibrates against the official daily 12-tenor Treasury par curve (1 Month through 30 Year) via FinanceToolkit's fixedincome.get_treasury_rates(): a much denser cross-section for the same three-factor Nelson-Siegel fit, especially at the short end the Yahoo set barely covers. Requires an FMP API key and period='daily' (the Treasury publishes daily); falls back to 'yahoo' with a logged warning when the fetch fails. Tenor columns the Treasury only started publishing partway through the window (e.g. '2 Month', 2018) are dropped rather than truncating every other tenor's history. 'government' calibrates against the official government bond yield curve of `country` via FinanceToolkit's fixedincome.get_government_bond_yield_curve() (no API key): the US Treasury, the ECB's euro area curve, the Bundesbank, the Bank of England, Japan's Ministry of Finance, the Bank of Canada, the Riksbank or Norges Bank; period daily, weekly or monthly. It never falls back to the US curve, since that would silently simulate the wrong country.")
    country: str = Field(default='United States', description="The country whose government curve to fit when source='government', one of term_structure_model.GOVERNMENT_CURVE_COUNTRIES. Only used with source='government'.")
    beliefs: YieldCurveBeliefs = Field(default_factory=YieldCurveBeliefs)
```

Nelson-Siegel dynamic yield curve settings: opt-in, alongside the single-tenor
interest_rate factor. When enabled, adds three correlated factors (rate_level,
rate_slope, rate_curvature) to the simulation, calibrated from historical
multi-tenor treasury yields (see `source`).

## OUBeliefs

```python
class OUBeliefs(_StrictModel):
    mean_reversion_speed: float | None = Field(default=None, gt=0)
    long_run_mean: float | BeliefPath | None = None
    volatility: float | None = Field(default=None, gt=0)
    shocks: list[Shock] = Field(default_factory=list, description='One-off jumps applied at specific simulated years.')
```

Optional per-parameter overrides on top of a calibrated Ornstein-Uhlenbeck fit
(shared shape for both interest_rate and inflation, since both calibrate to the
same OUParams). Leave a field unset (null in YAML) to keep the statistically
calibrated value.

long_run_mean accepts either a constant float (the existing behavior: substitute
one target for the whole horizon) or a BeliefPath (a term structure of targets at
several horizons, e.g. 5/10/20/30-year points, interpolated between them; see
resolve_belief_path()). A BeliefPath only takes effect for constant-volatility,
non-business-cycle-conditioned factors, the same restriction this project
already applies to combining GARCH or covariate conditioning with belief overrides.

shocks are one-off perturbations to the simulated value at specific years (see
calibration_model.Shock), independent of long_run_mean/BeliefPath; applied
regardless of volatility_model/condition_on_business_cycle, since a shock only
touches the final numeric value, not the drift mechanism that produced it.

## EquityBeliefs

```python
class EquityBeliefs(_StrictModel):
    regime_means: list[float] | None = None
    regime_volatilities: list[float] | None = None
    shocks: list[Shock] = Field(default_factory=list, description="One-off jumps in the price: each multiplies the price at its year by exp(magnitude), a log-return (-0.3 is about a 26% fall), after which the regimes continue from the shocked price. Additive only; stress_test_regime fills these from a regulator's stock-market path.")
```

Optional per-parameter overrides on top of a calibrated regime-switching fit.
If provided, regime_means/regime_volatilities must have one entry per calibrated
regime (n_regimes). Leave unset (null in YAML) to keep the statistically
calibrated value.

## BeliefPath

```python
class BeliefPath(BaseModel):
    anchors: dict[float, float] = Field(description='horizon in years from t=0 -> target long_run_mean value.')
    converge_over_years: float | None = Field(default=None, gt=0, description='Years, past the last anchor, over which the target converges linearly to long_run_mean before holding flat there. None (default) holds flat at the last anchor forever.')
```

A time-varying belief override for an Ornstein-Uhlenbeck factor's long_run_mean:
instead of substituting one constant target for the whole horizon, states the
target level at several future horizons (e.g. {5: 0.03, 10: 0.04, 20: 0.025} for
5/10/20-year targets) and lets the mean-reversion target move between them over
the simulated horizon; see resolve_belief_path() for how it's turned into a
per-step target. Where a plain float belief says "I believe theta is X," a
BeliefPath says "I believe theta is X now, Y in 5 years, Z in 10."

**Attributes:**

- <u>anchors (dict[float, float]):</u> horizon in years from the simulation start (t=0) -> target long_run_mean value at that horizon. At least one anchor is required; horizons must be non-negative.
- <u>converge_over_years (float &#124; None):</u> if set, the target keeps moving past the last stated anchor, converging linearly to the factor's own (calibrated or belief-overridden) long_run_mean over this many years, then holding flat there. If None (default), the target instead holds flat at the last anchor's value forever (today's behavior, unchanged).

## BeliefPath.terminal_value

```python
beliefpath.terminal_value  # property -> float
```

The target value at the furthest stated horizon, used as the single-number
summary wherever a plain float long_run_mean is still needed (e.g. diagnose()'s
theoretical stationary-distribution check).

## Shock

```python
class Shock(BaseModel):
    year: float = Field(ge=0, description='Simulated year the shock lands on.')
    magnitude: float = Field(allow_inf_nan=False, description='Shock size: added (additive) or set (absolute).')
    mode: Literal['additive', 'absolute'] = Field(default='additive', description="'additive' adds magnitude to the step's value; 'absolute' replaces it.")
```

A one-off perturbation to a factor's simulated value at a specific year, distinct
from BeliefPath: it doesn't change the mean-reversion target, it jumps the
process's actual level once and lets its own calibrated stochastic dynamics
(mean-reversion + volatility, and any active BeliefPath target) continue
unmodified from the shocked level; e.g. "+2% to the rate at year 3" rather than
a deterministic path.

**Attributes:**

- <u>year (float):</u> the simulated year the shock lands on, snapped to the nearest time-grid step (see scenarios_controller._make_shock_step).
- <u>magnitude (float):</u> the shock's size. Added to (mode="additive") or replaces (mode="absolute") the process's value at that step.
- <u>mode (Literal["additive", "absolute"]):</u> "additive" (default) adds magnitude to whatever the process's own dynamics produced that step; "absolute" replaces it outright.
