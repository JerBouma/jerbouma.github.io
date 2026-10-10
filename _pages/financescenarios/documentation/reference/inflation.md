---
title: "Inflation"
seo_title: "Inflation Reference – Finance Scenarios"
excerpt: "Consumer price inflation, one per country or region."
description: "Consumer price inflation, one per country or region."
author_profile: false
permalink: /projects/financescenarios/docs/reference/inflation
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Consumer price inflation, one per country or region. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.factors.inflation.inflation_controller import Inflation
```

```python
Inflation(toolkit: Toolkit)
```

The Inflation module simulates the inflation rate: how fast consumer prices rise each
year, for one or more countries. Inflation drifts back toward a normal level after a
shock (the 2022 surge had largely faded by 2024), it can briefly turn negative
(deflation), and this module captures that behavior.

In plain terms: add an inflation entry per country, such as the United States or
Brazil, and each becomes a variable in the simulated scenarios, linked to interest
rates, equities and the rest through the correlation matrix. You use it to see how
the purchasing power of a portfolio, a pension promise or a salary might evolve, and
`ScenarioSet.cumulative_index("...")` turns a simulated inflation path back into a
price-level index. At least one entry is required; each is calibrated independently
and named by its own `name`.

The model. Inflation sits first in the factor cascade (the order in which factors are
simulated, see the architecture documentation), following the framework of Wilkie
[(1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf)
and Ahlgrim, D'Arcy and Gorvett
[(2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf),
where inflation drives the rest of the model rather than the other way around. The
default `method: "ou"` is a mean-reverting Ornstein-Uhlenbeck process, the same kind
of process used for the short interest rate:
`dpi = a(theta - pi)dt + sigma*dW`, where `pi` is the inflation rate, `a` the
mean-reversion speed (how fast a gap to normal closes), `theta` the long-run mean
(the normal level) and `sigma` the volatility (the size of the random swings `dW`).
It is calibrated with the same `fit_ou_process` the interest rate uses, since
inflation is structurally the same process as the short rate, and is stepped with
the exact discrete-time transition (see `inflation_model.step_ou`). The simulated
rate is unconstrained and can go negative, matching history: deflation is a real,
if less common, condition.

Other methods, each a published framework's own inflation piece. They are picked
automatically when that framework's factor-set/settings pair is selected (see
the configuration documentation's Frameworks section) but can be chosen directly too:

- `wilkie_ar1`: Wilkie's (1986) original force-of-inflation process, a directly
  fitted discrete AR(1) (each period's value is a fixed fraction of last period's
  gap to the mean, plus noise) with no continuous-time reinterpretation; see
  `inflation_model.step_ar1`. It is the first link of Wilkie's cascade, in which
  the dividend yield (`dividend_yield[i].condition_on_inflation`), dividend growth
  and the Consols (long-term) yield (`interest_rates[i].method: wilkie_consols`)
  are each a direct function of inflation's own path, not merely correlated with it.
- `hibbert_two_factor`: Hibbert, Mowbray and Turnbull's
  [(2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf)
  structure, in which actual inflation reverts not to a fixed level but to a second,
  slower "expected inflation" factor's current level (a moving target):
  `d(fast) = mean_reversion_speed * (target(t) - fast(t)) * dt + volatility * dW`.
  The paper extracts the slow factor with a Kalman filter (a latent-state
  estimator) this project does not have, so `target_source` picks an observable
  approximation: `coarser_period` (the default, the same country's CPI growth
  refetched at the coarser `target_period` and simulated as its own correlated
  factor `f"{name}_target"`) or `ewma` (an exponentially weighted moving average of
  this entry's own path, smoothed by `target_smoothing`).
- `knw` and `knw_sv`: a bivariate VAR(1) (a two-variable autoregression) fitted
  jointly with a paired `interest_rates[]` entry, with genuine two-way coupling of
  the two levels, and its stochastic-volatility extension. These are calibrated by
  `financescenarios/models/knw` and `knw_sv` (see `Knw`,
  `KnwSv`), not by this class.

Options that change the `ou` process:

- `volatility_model: "garch"` replaces the fixed volatility with a GARCH(1,1)
  process ([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1)), so
  calm and turbulent inflation spells each persist; the same
  `calibration_model.fit_garch_process`/`GARCHStepper` the interest rate uses
  (documented in full in `InterestRates`).
- `condition_on_business_cycle: true` adds a drift term on the leading indicator's
  step-to-step change (see `LeadingIndicator`). It requires
  `leading_indicator.enabled: true` and forces calibration onto
  `leading_indicator.period`; since inflation accepts monthly, quarterly and yearly,
  that period (default monthly) is always compatible.
- `condition_on_interest_rate: true` adds the same kind of drift term, but on a
  paired `interest_rates[]` entry's step-to-step change (named by
  `interest_rate_name`), and calibrates at that entry's period. It is a one-way,
  correlated-shocks-style coupling (`calibration_model.OUCovariateParams`), unlike
  `method: "knw"`'s two-way coupling of the levels (compared in
  `Knw`).
- `measure: "risk_neutral"` with `method: "ou"` replaces the historical fit with a
  market-implied snapshot: a Nelson-Siegel forward curve fitted to the US
  TIPS-breakeven term structure (see `calibrate_risk_neutral`). With
  `method: "knw_sv"` it selects `KnwSvQ`'s completely-affine Q-measure parameters
  instead (see `KnwSvQ`). No other method has a risk-neutral
  counterpart.

Rules between these: `wilkie_ar1`, `hibbert_two_factor`, `knw` and `knw_sv` are each
incompatible with `volatility_model: "garch"`, `condition_on_business_cycle` and any
belief override (none of those frameworks have such concepts, and their parameters
have no OU-style `mean_reversion_speed`/`long_run_mean` to override);
`condition_on_interest_rate` is incompatible with `garch`,
`condition_on_business_cycle` and `knw`.

Data source. Inflation is not ticker-based: each entry comes from the Finance
Toolkit's `economics.get_consumer_price_index(countries=country,
oecd_source=(source == "oecd"), period=period, growth=True, lag=...)`, so the `Toolkit`
does not need to hold any particular ticker. Inflation is always year-over-year: the
lag is 12 months, 4 quarters or 1 year (`helpers.YEAR_OVER_YEAR_LAG`), so each value
compares the CPI with its level a year earlier, the headline rate statistics offices
publish and identical to the Finance Toolkit's `get_inflation_rate`. A US reading of
0.034 means prices are 3.4% higher than a year ago, the same annual decimal scale as
the short rate. Because consecutive monthly readings share 11 of their 12 months, the
series is smooth: a monthly fit shows slower mean reversion and smaller monthly
shocks than a fit on month-on-month changes would, which is the convention most
economic scenario generators calibrate inflation on. `source: "oecd"` (the default)
covers the roughly 38 OECD members at monthly, quarterly or yearly frequency. `source: "gmdb"` routes the same call
through the Global Macro Database, which covers countries outside the OECD (Brazil,
India, China) but is annual only, so such an entry needs `period: "yearly"`; config
validation rejects monthly or quarterly up front rather than silently truncating.
Everything else (method, volatility model, conditioning, beliefs) works the same for
both sources. Neither source needs an API key, and neither does the risk-neutral
breakeven curve.

Multiple countries. `config.inflation` is a list, one correlated factor per entry.
Every entry across `interest_rates`/`inflation`/`equities`/`unemployment`/`fx`/
`credit` shares one flat name space, so the shipped `factors.yaml` names these
`<region>_inflation` (e.g. `united_states_inflation`) to avoid collisions; it is
authored there in a friendlier `defaults` + `countries` shape (`name: Eurozone`
resolves to `eurozone_inflation`, see the configuration documentation's Multi-instance
factors). `unemployment[i].inflation_name` references an inflation entry's `name`
to pair the two for the Phillips-curve term (see `Unemployment`).

What it does not do: it models headline CPI inflation only (no core or sector price
indices); the Hibbert method approximates the paper's Kalman-filtered expected
inflation with observable data and does not replicate its fixed cross-factor
correlations or closed-form bond prices (correlations come from the same estimated
matrix as every other factor); and the risk-neutral breakeven curve exists for the
United States, the United Kingdom (RPI) and the euro area (German linkers) only.

Configuration (`inflation[i]` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `name` | `inflation` | The factor's name in the output; unique across every multi-instance list. |
| `country` | `United States` | For `get_consumer_price_index`; risk-neutral `ou`: a `BREAKEVEN_COUNTRIES` key. |
| `source` | `oecd` | `oecd` or `gmdb` (`period: yearly` only). |
| `currency` | `USD` | The series' currency; descriptive metadata only, read by `financescenarios.reporting`. |
| `method` | `ou` | `ou`, `wilkie_ar1`, `hibbert_two_factor`, `knw` or `knw_sv`. |
| `measure` | `real_world` | `real_world` or `risk_neutral` (with `method: ou` or `knw_sv` only). |
| `tips_breakeven_decay` | `0.7308` | Nelson-Siegel decay for the risk-neutral breakeven curve. |
| `period` | `monthly` | `monthly`, `quarterly` or `yearly` (`yearly` only for `gmdb`). |
| `volatility_model` | `constant` | `constant` or `garch`. |
| `condition_on_business_cycle` | `false` | Requires `leading_indicator.enabled: true`. |
| `condition_on_interest_rate` | `false` | Requires `interest_rate_name` to match an `interest_rates[i].name`. |
| `interest_rate_name` | `interest_rate` | Used by `condition_on_interest_rate` and `method: knw`/`knw_sv`. |
| `target_source` | `coarser_period` | `hibbert_two_factor` only: `coarser_period` or `ewma`. |
| `target_period` | `yearly` | `coarser_period` only: `quarterly` or `yearly`, strictly coarser than `period`. |
| `target_smoothing` | `0.05` | `ewma` only: weight on each new observation, in (0, 1). |
| `beliefs.mean_reversion_speed` | `null` | Override the fitted speed; must be greater than 0. |
| `beliefs.long_run_mean` | `null` | Override the fitted normal level, as an annual decimal. |
| `beliefs.volatility` | `null` | Override the fitted volatility; must be greater than 0. |

`method` is checked when calibration runs, not when the config file is loaded. A
belief left `null` keeps the calibrated value; beliefs apply only to the constant-
volatility `ou` fit, are stated on the annual scale (`long_run_mean: 0.09` for 9% a
year), and in a regime YAML (see the regimes documentation) one entry's beliefs are
addressed with a dotted `"inflation.<name>"` key. A non-empty `beliefs` block with
`measure: risk_neutral` (either method) is rejected at config validation, because a
risk-neutral fit must match the market input exactly. A risk-neutral `ou` entry also
rejects any non-default `country`, `source`, `period`, `volatility_model`,
`condition_on_business_cycle` or `condition_on_interest_rate` at load time, since
`calibrate_risk_neutral` ignores them.

**References:**

- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>
- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the CAS, 92. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert Limited. <https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf>
- Uhlenbeck, G.E., Ornstein, L.S. (1930). "On the Theory of the Brownian Motion." Physical Review, 36(5), 823-841. <https://doi.org/10.1103/PhysRev.36.823>
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." Journal of Econometrics, 31(3), 307-327. <https://doi.org/10.1016/0304-4076(86>)90063-1
- Nelson, C.R., Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." Journal of Business, 60(4), 473-489. <https://doi.org/10.1086/296409>
- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. <https://doi.org/10.1016/j.jeconom.2005.03.005>

## calibrate

```python
calibrate(
    name: str,
    country: str = 'United States',
    period: str = 'monthly',
    source: str = 'oecd',
    method: str = 'ou',
    volatility_model: str = 'constant',
    business_cycle_covariate: pl.Series | None = None,
    business_cycle_covariate_dates: pl.Series | None = None,
    target_source: str = 'coarser_period',
    target_period: str = 'yearly',
    target_smoothing: float = 0.05,
) -> OUParams | GARCHParams | OUCovariateParams | AR1Params | MovingTargetOUParams
```

Calibrate one country's inflation process from its history: fetch the year-over-year
Consumer Price Index growth and fit how fast inflation returns to its normal
level (`mean_reversion_speed`), what that normal level is (`long_run_mean`) and how
much it swings (`volatility`), or the matching parameters of the chosen `method`.

In plain terms: this learns from the past how a country's inflation behaves, so the
simulated scenarios spike and settle the way the real rate has. A mean-reversion speed
of 8 a year, for example, means a shock to inflation has faded by half after about
a month (ln 2 / 8 years), which is how quickly the noisy month-to-month readings fall
back to trend; `long_run_mean` is the rate it settles around and `initial_value` is
the latest observed rate, where every simulated path starts.

All values are annual decimals (0.025 is 2.5% a year): each period's CPI growth `g`
is converted with `ln(1 + g) / dt`, where `dt` is the period length in years (1/12,
1/4 or 1). What comes back depends on the options:

- `OUParams` (the default `ou` fit): `mean_reversion_speed`, `long_run_mean`,
  `volatility`, `initial_value`.
- `GARCHParams` (`volatility_model="garch"`): the same speed and mean, plus
  `omega`, `alpha` and `beta`, the GARCH(1,1) variance recursion
  (`variance = omega + alpha * last shock^2 + beta * last variance`), and
  `initial_variance`.
- `OUCovariateParams` (a covariate supplied): the OU fit plus the sensitivity to the
  covariate's step-to-step change.
- `AR1Params` (`method="wilkie_ar1"`): `long_run_mean`, `persistence` (the AR
  coefficient itself, the share of last period's gap carried into this one, with
  no conversion through `dt`) and `volatility` (the per-period shock size).
- `MovingTargetOUParams` (`method="hibbert_two_factor"`): `mean_reversion_speed`
  toward the moving target, `volatility`, `initial_value` and, for `ewma`,
  `initial_target_value`. It deliberately has no `long_run_mean`: the level the
  rate reverts to is whatever the target factor's path says at each step.

Also known as: inflation calibration, CPI mean-reversion fit, Vasicek-type
inflation model, Wilkie inflation model, Hibbert two-factor inflation.

**Args:**

- <u>name (str):</u> this entry's name, used to key params()/changes()/series() and as the factor name in the simulation (e.g. "united_states_inflation").
- <u>country (str):</u> the country to pull CPI data for, as the Finance Toolkit names it (e.g. "United States", "Brazil").
- <u>period (str):</u> sampling frequency of the data ("monthly", "quarterly" or "yearly" for source="oecd"; "yearly" only for source="gmdb"); sets dt.
- <u>source (str):</u> "oecd" (the default: the OECD Consumer Price Index) or "gmdb" (the Global Macro Database, which covers countries outside the OECD, period="yearly" only).
- <u>method (str):</u> "ou" (the default: a continuous-time Ornstein-Uhlenbeck process, Ahlgrim/D'Arcy/Gorvett 2005's treatment), "wilkie_ar1" (Wilkie's 1986 original: a directly fitted discrete AR(1) on the inflation rate itself; see `calibration_model.AR1Params`), or "hibbert_two_factor" (Hibbert/Barrie & Hibbert 2001's fast inflation reverting to a moving "expected inflation" target; see target_source and `calibration_model.MovingTargetOUParams`). "wilkie_ar1" and "hibbert_two_factor" are incompatible with volatility_model="garch" and business_cycle_covariate. "knw"/"knw_sv" are not accepted here; they are fitted jointly with an interest rate in `financescenarios/models/`.
- <u>volatility_model (str):</u> "constant" (the default) or "garch" (GARCH(1,1) time-varying volatility, Bollerslev 1986).
- <u>business_cycle_covariate (pl.Series &#124; None):</u> a raw historical level series to condition on, usually the leading indicator (LeadingIndicator.series) or, for `condition_on_interest_rate`, the paired interest rate's own series. When supplied, adds a drift term on the covariate's step-to-step change; incompatible with volatility_model="garch".
- <u>business_cycle_covariate_dates (pl.Series &#124; None):</u> the dates paired with `business_cycle_covariate`, same length and order. Required whenever `business_cycle_covariate` is supplied: this entry's inflation series and the covariate are fetched independently and forced onto the same *period* but not guaranteed the same *start date*, so the two are inner-joined on date before fitting, the same way unemployment_controller.py aligns unemployment against inflation.
- <u>target_source (str):</u> used when method="hibbert_two_factor". "coarser_period" (the default) refetches this same country's CPI growth at target_period as the slow/target leg, fitted as a plain OU and simulated as its own correlated f"{name}_target" factor. "ewma" instead derives the target as a deterministic exponentially weighted moving average of this entry's own history (target_smoothing): no second fetch, no second factor.
- <u>target_period (str):</u> used when method="hibbert_two_factor" and target_source="coarser_period"; "quarterly" or "yearly", strictly coarser than `period` (enforced at config-validation time, see config_model.InflationConfig; this method does not re-check it).
- <u>target_smoothing (float):</u> used when method="hibbert_two_factor" and target_source="ewma"; the EWMA weight on each new observation, in (0, 1): `y(t) = smoothing * x(t) + (1 - smoothing) * y(t-1)`, so smaller values make a slower-moving target. A fixed setting, not fitted.

**Returns:**

<u>OUParams &#124; GARCHParams &#124; OUCovariateParams &#124; AR1Params &#124; MovingTargetOUParams:</u> the calibrated process parameters: GARCHParams when volatility_model="garch", OUCovariateParams when business_cycle_covariate is supplied, AR1Params when method="wilkie_ar1", MovingTargetOUParams when method="hibbert_two_factor", OUParams otherwise.

**Raises:**

- <u>ValueError:</u> if source, period, method or volatility_model is not recognized, period isn't "yearly" for source="gmdb", business_cycle_covariate is combined with volatility_model="garch", business_cycle_covariate is supplied without business_cycle_covariate_dates (or vice versa), method="wilkie_ar1"/"hibbert_two_factor" is combined with volatility_model="garch" or business_cycle_covariate, the Finance Toolkit returns no CPI data for the country/period/source, or the history is too short or shows no mean reversion to fit (the fit functions raise).

**Notes:**

- The default Toolkit history is only about five years; pass a `start_date` (the
  shipped `settings/default.yaml` uses 2000-01-01) for a stable fit. With the short
  default, `hibbert_two_factor`'s yearly target leg has too few points to fit.
- `source="gmdb"` is annual only, and the Global Macro Database extends its series
  with IMF projections, so its most recent year may be a forecast, not an outturn.
- For `hibbert_two_factor` with `coarser_period`, the two legs are matched with an
  as-of join (each month paired with the latest yearly value already known). The
  fit and the fast leg's `initial_value` therefore stop at the last month that has
  a published target value; when the OECD's latest yearly figure is still missing,
  that can be more than a year before today's print.
- The `coarser_period` variant is a documented simplification. Both legs are
  year-over-year rates, so they share one scale, but the yearly target is a
  calendar-year change paired with the latest month's twelve-month change, and the
  monthly leg moves only gradually; the fitted speed and volatility are well
  defined yet not a clean "years to close the gap" reading.
- `coarser_period` registers a second entry, f"{name}_target", in params(),
  changes() and series(); the fast leg reads its simulated level each step, a real
  dependency registered in `Scenarios._build_dependency_graph()`. `ewma` registers
  nothing extra and is simulated by a stateful `MovingTargetEWMAStepper` that
  tracks the running average of the simulated path itself.
- The moving-target fit uses a first-order Euler discretization: a moving target
  has no closed-form exact transition the way a fixed-target OU does.
- `wilkie_ar1` (like `knw`) is a discrete recursion with no time step to rescale,
  so `engine.frequency` must equal the entry's `period` or `ScenariosConfig`
  rejects it. Wilkie's preset pairs it with `settings/wilkie.yaml`, which caps the
  history at 1995-2019 for the sake of its Consols-yield leg.
- Belief overrides are applied after this call (by the calibration controller),
  only to the constant-volatility `ou` fit; GARCH parameters are used as fitted.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.inflation.inflation_controller import Inflation

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2000-01-01")
inflation = Inflation(toolkit)

inflation.calibrate("united_states_inflation", country="United States")
inflation.calibrate("brazil_inflation", country="Brazil", source="gmdb", period="yearly")
inflation.calibrate("us_wilkie", method="wilkie_ar1")
inflation.calibrate("us_hibbert", method="hibbert_two_factor", target_source="ewma")
```

Which returns (calibrated on 2026-10-05):

| name | method | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-----|:-------|---------------------:|--------------:|-----------:|--------------:|
| united_states_inflation | ou | 0.4150 | 0.0266 | 0.0158 | 0.0340 |
| brazil_inflation | ou | 0.9484 | 0.0592 | 0.0371 | 0.0313 |
| us_wilkie | wilkie_ar1 | persistence 0.9660 | 0.0266 | 0.0045 | 0.0340 |
| us_hibbert | hibbert_two_factor | 0.0187 | moving target (0.0335 today) | 0.0156 | 0.0340 |

US inflation starts at 3.40% (August 2026 prices against August 2025's) and is
pulled toward 2.66%, close to its 2000-2026 average, halving a gap in about 1.7
years; Wilkie's AR(1) says the same thing per step (97% of each month's gap carries
into the next). Brazil's yearly series starts at 3.13%, settles around 5.92% and
halves a gap in about nine months. The Hibbert fit pulls US inflation toward its
own smoothed recent average, 3.35% today, rather than toward a fixed number; with
year-over-year data that average tracks inflation so closely that the remaining
gap closes only slowly, so nearly all of the movement sits in the target.

**References:**

- Uhlenbeck, G.E., Ornstein, L.S. (1930). "On the Theory of the Brownian Motion." Physical Review, 36(5), 823-841. <https://doi.org/10.1103/PhysRev.36.823>
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." Journal of Econometrics, 31(3), 307-327. <https://doi.org/10.1016/0304-4076(86>)90063-1
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>
- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the CAS, 92. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert Limited. <https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf>

## calibrate_risk_neutral

```python
calibrate_risk_neutral(
    name: str,
    decay: float = 0.7308,
    country: str = 'United States',
) -> DeterministicPathParams
```

Calibrate one risk-neutral (Q-measure) inflation path: fit a Nelson-Siegel
forward-rate curve to today's breakeven inflation term structure (in the United States the 5, 7, 10, 20
and 30-year TIPS breakevens) and use that curve as the inflation path, taken as given
rather than projected forward with a historically fitted random process.

In plain terms: the gap between a nominal Treasury yield and the yield on an
inflation-protected Treasury (TIPS) of the same maturity is the inflation rate the
bond market is pricing in, the "breakeven". Where the real-world `calibrate` asks
how inflation has behaved, this asks what inflation the market prices today, which
is what you need to value inflation-linked cash flows consistently with market
prices (no arbitrage, meaning no riskless profit from mispricing). The answer is a
curve, not one number, because expected inflation differs by horizon, and every
simulated path follows that same curve.

Each breakeven is an average annualized rate over `[0, tenor]`, mathematically the
same shape as a Treasury yield, so the fit reuses
`term_structure_model.fit_nelson_siegel_factors`, the cross-sectional fit
(level, slope and curvature at one date) that `yield_curve`,
`credit_term_structure` and `hjm` use, at the last date on which every tenor is
observed. Level is the long-horizon rate the curve flattens to, slope the gap
between the short and long end (negative means the near term is lower), and
curvature a hump in the middle. At simulation time the path is rebuilt as the
instantaneous forward rate `nelson_siegel_forward(level, slope, curvature, t,
decay)` across the time grid (`scenarios_controller._make_deterministic_path_step`
looks up each step's value): no mean reversion, no diffusion, no beliefs or shocks.
This is the same "match an observable market input exactly, invent no dynamics the
market does not discipline" scope as the interest rate's
`InterestRates.calibrate_risk_neutral`, shaped as a term structure instead of one
flat level, which is why it has its own `DeterministicPathParams` type.

Also known as: market-implied inflation curve, breakeven inflation forward curve,
Q-measure inflation.

**Args:**

- <u>name (str):</u> this entry's name, used to key params()/changes()/series() and as the factor name in the simulation.
- <u>decay (float):</u> the Nelson-Siegel decay parameter (lambda), annualized; it sets where along the maturities the curvature hump sits. Fixed rather than calibrated, per Diebold & Li (2006); the same default as `TermStructure.calibrate`/`CreditTermStructure.calibrate`/`hjm_model`, exposed in a factor set as `tips_breakeven_decay`.
- <u>country (str):</u> whose breakeven curve to fit, one of `BREAKEVEN_COUNTRIES`: - "United States" (default): nominal minus TIPS yields, 5 to 30 years, from 2003. - "United Kingdom": the Bank of England's implied inflation spot curve, 3 to 40 years, measured against the Retail Prices Index (RPI), which index-linked gilts pay and which has run above CPI inflation; fitted at 3, 5, 7, 10, 15, 20, 25, 30 and 40 years. - "Germany" or "Euro Area": German federal nominal minus inflation-linked yields at 5, 7, 10 and 15 years, from 2014. The linkers pay euro area inflation (HICP excluding tobacco), so this is the euro area's market-implied inflation.

**Returns:**

<u>DeterministicPathParams:</u> `level`/`slope`/`curvature`/`decay` of the fitted curve, plus `initial_value`, the instantaneous forward rate at t=0, all as annual decimals. changes() and series() for this entry hold the history of the fitted level factor.

**Raises:**

- <u>ValueError:</u> if no date in the fetch window has every breakeven tenor observed (e.g. `end_date` before February 2010, when the 30-year TIPS series starts), rather than silently fitting fewer tenors.

**Notes:**

- The data come from the Finance Toolkit's
  `economics.get_breakeven_inflation_expectations()` (nominal Treasury yield minus
  real TIPS yield), read from the US Treasury without a key, or from FRED when the
  Toolkit has a `fred_api_key`.
- The United States, the United Kingdom and the euro area (through Germany) are covered; the curves
  come from the Finance Toolkit's `economics.get_breakeven_inflation_expectations(countries=...)`, from
  the US Treasury (or FRED with a key), the Bank of England and the Bundesbank, none needing a key.
  A config entry must keep the
  default `source`, `period`, `volatility_model`, `condition_on_business_cycle`
  and `condition_on_interest_rate`; any other value raises at load time rather
  than being silently dropped. Belief overrides are rejected for the same reason.
- There is no US or German breakeven shorter than five years, nor a UK one shorter than three,
  so the first years of the path are a Nelson-Siegel extrapolation (a warning is logged when today's value
  lands more than a point from the shortest quoted breakeven; on 2026-10-07 it was 1.1% against a 5-year
  2.4% for the US, 7.9% against a 3-year 4.0% for the UK and 5.6% against a 5-year 2.2% for Germany, while
  one year out the paths were 2.2%, 4.1% and 2.5%): smoother
  and more defensible than a flat clamp, but a model artifact, not a market print.
- Dates missing any tenor are dropped before the latest is taken, so a partial
  intraday FRED row (seen live with 3 of 5 tenors empty) is skipped in favor of the
  last fully quoted date.
- A breakeven can go negative (nominal yield below real yield), and nothing floors
  it: a negative inflation path is possible and left as the market prices it.
- In a configuration, `measure: "risk_neutral"` with `method: "knw_sv"` does not
  come here; it selects `KnwSvQ`'s parameters instead (see
  `KnwSvQ`).
- With a Toolkit `start_date` far back (2000-01-01 tested), the breakeven fetch
  failed inside the Finance Toolkit on 2026-10-04; the default window works.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.inflation.inflation_controller import Inflation

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", fred_api_key="FRED_KEY")
inflation = Inflation(toolkit)

inflation.calibrate_risk_neutral("us_breakeven")
```

Which returns (calibrated on 2026-10-04):

| name | level | slope | curvature | decay | initial_value |
|:-----|------:|------:|----------:|------:|--------------:|
| us_breakeven | 0.0238 | -0.0057 | 0.0053 | 0.7308 | 0.0181 |

The curve starts at 1.81% a year today (extrapolated, since the shortest breakeven
is five years), rises to about 2.29% one year out and 2.42% at five years, and
settles at 2.38% for the long run: the inflation the market prices in, followed by
every simulated path.

**References:**

- Nelson, C.R., Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." Journal of Business, 60(4), 473-489. <https://doi.org/10.1086/296409>
- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. <https://doi.org/10.1016/j.jeconom.2005.03.005>

## names

```python
inflation.names  # property -> list[str]
```

The names of every inflation entry calibrated so far, in calibration order.

## params

```python
params(
    name: str,
) -> OUParams | GARCHParams | OUCovariateParams | AR1Params | MovingTargetOUParams | DeterministicPathParams
```

The calibrated process parameters for one inflation entry.

**Args:**

- <u>name (str):</u> the entry's name, as passed to calibrate().

**Raises:**

- <u>RuntimeError:</u> if calibrate(name, ...) hasn't been called yet.

## step_function

```python
Inflation.step_function(method: str)
```

The step function matching the given method: `inflation_model.step_ar1` for
"wilkie_ar1", `inflation_model.step_ou` (the exact OU transition) otherwise. A
plain function of `method`, not tied to any calibrated entry's instance
state: callers derive `method` from `InflationConfig.method` (the same
config-is-source-of-truth convention `InterestRates.step_function` already
uses), so this stays correct even when simulating from a `CalibrationResult`
loaded without ever calling calibrate() on this instance. GARCH, covariate,
moving-target and risk-neutral entries are dispatched to their own step
functions by `scenarios_controller`, whatever this returns.

**Args:**

- <u>method (str):</u> "ou" or "wilkie_ar1".

## series

```python
series(name: str) -> pl.Series
```

The raw historical inflation-rate series for one entry, from the same data
calibrate() already fetched; used by other factors' `condition_on_inflation`-
style covariate wiring (e.g. dividend_yield), which needs the raw level
series (it computes its own step-to-step change internally), unlike
changes() which already returns pre-differenced values.

**Args:**

- <u>name (str):</u> the entry's name, as passed to calibrate().

**Raises:**

- <u>RuntimeError:</u> if calibrate(name, ...) hasn't been called yet.

## changes

```python
changes(name: str) -> pl.DataFrame
```

Dated period-over-period changes in one entry's inflation rate, from the
same data calibrate() already fetched; reused for cross-factor correlation
estimation (Dependence) instead of triggering a second Finance Toolkit fetch
at a different period.

**Args:**

- <u>name (str):</u> the entry's name, as passed to calibrate().

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` (pl.Date) and `value` (f64); see helpers.dated_changes().

**Raises:**

- <u>RuntimeError:</u> if calibrate(name, ...) hasn't been called yet.
