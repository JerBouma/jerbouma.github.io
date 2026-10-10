---
title: "InterestRates"
seo_title: "InterestRates Reference – Finance Scenarios"
excerpt: "Short and long interest rates, one per country or region."
description: "Short and long interest rates, one per country or region."
author_profile: false
permalink: /projects/financescenarios/docs/reference/interest-rates
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Short and long interest rates, one per country or region. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.factors.interest_rates.interest_rates_controller import InterestRates
```

```python
InterestRates(toolkit: Toolkit)
```

The Interest Rates module simulates the short rate: the interest rate for a very short
lending period, such as a 13-week Treasury bill. Actuarial and financial models use it
as the basic building block that the rest of a yield curve can be derived from. Rates
drift up and down with the economy but tend to be pulled back toward a normal level,
and that pull is what this module captures.

In plain terms: every run has at least one interest rate (it is an always-on factor,
like equities), and you can add one per country or region, such as the United States
and the Eurozone. Each becomes a variable in the simulated scenarios, linked to
inflation, equities, FX and the rest through the correlation matrix, and the other
factors read it where they need a risk-free rate. This is a single point on the
curve; for a whole simulated term structure across maturities, add the opt-in
`yield_curve` (`TermStructure`) or `hjm` (`Hjm`) factor alongside it.

The default model is a mean-reverting Ornstein-Uhlenbeck process: `dr = a(theta - r)dt
+ sigma*dW`, where `a` is the mean-reversion speed (how fast the rate returns to
normal), `theta` the long-run mean (that normal level), `sigma` the volatility (how
much it swings) and `dW` a Brownian increment, the standard mathematical
representation of continuous random noise. It descends from
[Vasicek (1977)](https://doi.org/10.1016/0304-405x(77)90016-2) and is known as the
[Hull-White (1990)](https://doi.org/10.1093/rfs/3.4.573) model. `method` picks one of
six short-rate processes:

| Method | Behavior |
|:-------|:----------|
| `hull_white` (default) | Gaussian (normally distributed) diffusion; the simulated rate can go negative. |
| `cir` | Cox-Ingersoll-Ross square-root diffusion, whose swings shrink as the rate nears zero. |
| `wilkie_consols` | Wilkie's (1986) consols (long-term) yield, driven by a paired `inflation` entry. |
| `hibbert_two_factor` | Hibbert (2001): a fast short rate pulled toward a second, moving long-rate target. |
| `knw` | A two-way coupled VAR(1) with a paired `inflation` entry (`Knw` controller). |
| `knw_sv` | `knw` plus a shared stochastic-volatility factor (`KnwSv` controller). |

The [Cox, Ingersoll and Ross (1985)](https://doi.org/10.2307/1911242) process scales
its noise with the square root of the rate, so the theoretical process cannot go
negative when the Feller condition (`2*a*theta >= sigma^2`) holds. The Wilkie (1986)
and Hibbert, Mowbray and Turnbull (2001) methods (linked under References) are each
one piece of a published framework, picked automatically by the shipped
`factor-sets/wilkie.yaml` and `factor-sets/hibbert.yaml` but selectable directly too;
`calibrate` documents both. `knw` and `knw_sv` are a generic affine coupling, not
tied to a framework, and are fit jointly with their inflation partner by the
`Knw`/`KnwSv` controllers rather than by this class.

Three options change the process further. `volatility_model="garch"` lets the size of
the swings vary over time, so calm and volatile periods each persist
([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1)); it works with
`hull_white` only. `condition_on_business_cycle` adds a pull from the leading
indicator, so rates tend to move with the business cycle. And `measure="risk_neutral"`
switches from the real-world measure (a statistical fit to history: how has the rate
behaved?) to the risk-neutral measure (what is consistent with today's market prices,
so that nothing priced off the rate admits arbitrage): either a flat path at today's
observed rate (`calibrate_risk_neutral`) or, with `risk_neutral_forward_curve`, a
stochastic Hull-White rate whose expected path reproduces today's whole forward curve
(`calibrate_risk_neutral_forward`).

Each entry picks one of three data sources, all obtained through the Finance Toolkit
and all normalized to a decimal fraction (`0.06` is 6%) before fitting:

- `source="ticker"` (default): a Yahoo Finance Treasury-yield ticker through
  `Toolkit.get_historical_data()`, the same path equities use: `^IRX` (13-week),
  `^FVX` (5-year), `^TNX` (10-year) or `^TYX` (30-year). These four are quoted in
  percentage points (3.8 meaning 3.80%) and divided by 100; any other ticker is
  assumed to be a decimal rate already. US-only in practice, since Yahoo has no
  sovereign-yield ticker for other countries. `build_toolkit()` adds every entry's
  `ticker` (and `target_ticker`) to the Toolkit it builds, so there is nothing extra
  to wire up.
- `source="oecd"`: the country-parameterized OECD short- or long-term rate
  (`economics.get_short_term_interest_rate` / `get_long_term_interest_rate`),
  genuinely worldwide but monthly, quarterly or yearly only (no daily or weekly OECD
  series). `term` picks short or long.
- `source="gmdb"`: the same two calls routed through the Finance Toolkit's Global
  Macro Database (`gmdb_source=True`), which covers countries outside the OECD's
  roster of about 38 members (Brazil, India, China) that `oecd` has no data for at
  all. The trade-off is frequency: the database is annual-only, so `period` must be
  `yearly`, and configuration validation rejects anything else up front rather than
  silently truncating.

No API key is needed for any of the three. `method`, `volatility_model`,
`condition_on_business_cycle` and `beliefs` apply identically whichever source an
entry uses.

What it does not do: it has no options or swaption data, so a risk-neutral
mean-reversion speed and volatility are never fit to market prices (the forward-curve
mode reuses the historical ones); it does not price bonds in closed form; and
`hibbert_two_factor` approximates the paper's latent (Kalman-filtered) slow factor
with observable data rather than filtering it.

Configuration (`interest_rates[i]` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `name` | `interest_rate` | The factor's name in the simulated output; unique across every factor list. |
| `source` | `ticker` | `ticker`, `oecd` or `gmdb` (see above). |
| `method` | `hull_white` | One of the six in the method table; an unknown value fails when the config loads. |
| `ticker` | `^IRX` | Used when `source: ticker`; any ticker included in the Toolkit. |
| `country` | `United States` | Used when `source: oecd` or `gmdb`; any country the data covers. |
| `term` | `short` | Used when `source: oecd` or `gmdb`: `short` or `long`. |
| `period` | `daily` | Calibration frequency; sets the time step (see the source limits above). |
| `volatility_model` | `constant` | `constant` or `garch`; `garch` requires `method: hull_white`. |
| `condition_on_business_cycle` | `false` | Requires `leading_indicator.enabled: true`; not with `garch`. |
| `measure` | `real_world` | `real_world` or `risk_neutral`; `risk_neutral` takes no `beliefs`. |
| `risk_neutral_forward_curve` | `false` | Forward-curve mode; needs `risk_neutral` and `hull_white`. |
| `currency` | `USD` | Descriptive label, used by reporting and by risk-neutral FX to find each leg. |
| `inflation_name` | `inflation` | The paired `inflation[j].name` for `wilkie_consols` and `knw`. |
| `inflation_weight` | `1.0` | `wilkie_consols` only: Wilkie's CW, fixed, not fit. |
| `inflation_decay` | `0.05` | `wilkie_consols` only: Wilkie's CD, fixed, not fit. |
| `target_source` | `long_term_rate` | `hibbert_two_factor` only: `long_term_rate` or `ewma`. |
| `target_term` | `long` | `hibbert_two_factor` with `oecd`: the target's term; must differ from `term`. |
| `target_ticker` | `^TNX` | `hibbert_two_factor` with `ticker`: the target ticker; must differ from `ticker`. |
| `target_smoothing` | `0.05` | `hibbert_two_factor` with `ewma`: weight on each new observation, in (0, 1). |
| `beliefs.mean_reversion_speed` | `null` | Override the fitted speed; must be greater than 0. |
| `beliefs.long_run_mean` | `null` | Override the fitted normal level; any sign (Hull-White rates can go negative). |
| `beliefs.volatility` | `null` | Override the fitted volatility; must be greater than 0. |

In a factor set the list is authored in a friendlier `defaults` + `countries` shape,
where each country states only what differs from a shared default and its label
(`Eurozone`) is suffixed by term into the factor name (`eurozone_short_rate`); the
shipped factor sets suffix every region entry by category (`united_states_short_rate`,
`united_states_inflation`) because all factor lists share one flat name space and a
duplicate name raises at load time.

A belief left as `null` keeps the fitted value; any other value replaces that one
parameter and leaves the rest of the fit untouched (`config_model.apply_ou_beliefs`).
Beliefs apply only with `volatility_model: constant` (a GARCH fit is used as
calibrated), not to `wilkie_consols`, `hibbert_two_factor`, `knw` or `knw_sv` (their
parameters have no OU speed or normal level to override), and raise when combined
with `measure: risk_neutral`, where they would silently undo the match to market
prices. In a regime file, address one entry's beliefs with an
`"interest_rates.<name>"` key.

**References:**

- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. <https://doi.org/10.1016/0304-405x(77>)90016-2
- Hull, J., White, A. (1990). "Pricing Interest-Rate-Derivative Securities." The Review of Financial Studies, 3(4), 573-592. <https://doi.org/10.1093/rfs/3.4.573>
- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). "A Theory of the Term Structure of Interest Rates." Econometrica, 53(2), 385-407. <https://doi.org/10.2307/1911242>
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." Journal of Econometrics, 31(3), 307-327. <https://doi.org/10.1016/0304-4076(86>)90063-1
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>
- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert Limited. <https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf>
- Brigo, D., Mercurio, F. (2006). "Interest Rate Models: Theory and Practice" (2nd ed.), Section 3.3. Springer Finance. <https://doi.org/10.1007/978-3-540-34604-3>
- Society of Actuaries & Casualty Actuarial Society (2002). "Report on Modeling of Economic Series Coordinated with Interest Rate Scenarios." <https://www.soa.org/globalassets/assets/files/sections/modeling-of-economic-scenarios.pdf>

## calibrate

```python
calibrate(
    name: str,
    source: str = 'ticker',
    method: str = 'hull_white',
    ticker: str = '^IRX',
    country: str = 'United States',
    term: str = 'short',
    period: str = 'daily',
    volatility_model: str = 'constant',
    business_cycle_covariate: pl.Series | None = None,
    business_cycle_covariate_dates: pl.Series | None = None,
    inflation: pl.Series | None = None,
    inflation_weight: float = 1.0,
    inflation_decay: float = 0.05,
    target_source: str = 'long_term_rate',
    target_term: str = 'long',
    target_ticker: str = '^TNX',
    target_smoothing: float = 0.05,
) -> OUParams | GARCHParams | OUCovariateParams | WilkieConsolsParams | MovingTargetOUParams
```

Calibrate one country or region's short-rate process from its history: fetch the
rate series from a Treasury-yield ticker, the OECD or the Global Macro Database,
and fit how fast it returns to its normal level (`mean_reversion_speed`), what that
normal level is (`long_run_mean`) and how much it swings (`volatility`).

In plain terms: this learns from the past how an interest rate behaves, so the
simulated scenarios rise and fall the way the real rate has. A mean-reversion speed
of 0.73 a year, for example, means a shock away from the normal level has faded by
half after about eleven months (ln 2 / 0.73 years). Call it once per country or
region; each call is stored under its own `name`.

The fit uses the process's exact discrete-time transition, `r(t+dt) = theta +
(r(t) - theta)*e^(-a*dt) + sigma*sqrt((1 - e^(-2*a*dt))/(2*a))*eps`, not a
first-order (Euler-Maruyama) approximation. Its mean is linear in today's rate, so
it is still an ordinary least squares regression of the change in the rate on its
level, converted back with `a = -ln(1 + slope)/dt` and `theta = intercept/(-slope)`;
the volatility is the residual standard deviation divided by the transition's own
conditional standard deviation. This is `calibration_model.fit_ou_process`, shared
with inflation, since both are the same process. All values are decimal fractions
(`0.04` is 4%) and the time step `dt` follows `period` (1/252 a year for daily data,
1/12 for monthly). The other methods:

- `cir` reuses the same drift estimate, then re-estimates volatility with the
  square-root diffusion `sigma*sqrt(r)` (see `fit_cir_process`), so its
  `volatility` is per unit of square-root rate, not a rate itself, and checks the
  Feller condition `2*a*theta >= sigma^2`.
- `volatility_model="garch"` (with `hull_white`) fits the same drift regression,
  then a Gaussian quasi-maximum-likelihood GARCH(1,1) to its residuals: the
  variance follows `h(t+1) = omega + alpha*eps(t)^2 + beta*h(t)`, stationary by
  construction (`alpha + beta < 1`), and is simulated by a stateful
  `GARCHStepper` that carries the variance from step to step.
- `business_cycle_covariate` adds a drift term on the leading indicator's
  step-to-step change; configured through `condition_on_business_cycle`, which also
  forces calibration onto `leading_indicator.period` so the two series align.
- `wilkie_consols` is Wilkie's (1986) Reduced Basis consols yield (his section
  3.15), the long-term-rate leg of his inflation cascade:
  `C(t) = CW*dlnQ(t) - CW*(1-CD)*dlnQ(t-1) + CN(t)` and
  `ln CN(t) = ln CMU + CA1*(ln CN(t-1) - ln CMU) + CSD*CZ(t)`. `C(t)` is the
  observed nominal yield, `dlnQ(t)` the paired inflation entry's force of
  inflation, and `CN(t)` a hidden real yield recovered by subtracting the
  inflation term and fit as a plain AR(1) (an autoregression on its own last
  value) on its logarithm; `CW` (`inflation_weight`) and `CD` (`inflation_decay`)
  are fixed at Wilkie's published values, not fit. See `fit_wilkie_consols_process`.
- `hibbert_two_factor` is Hibbert, Mowbray and Turnbull's (2001) two-factor
  structure: `d(fast) = a*(target(t) - fast(t))*dt + sigma*dW`, where the rate
  reverts not to a fixed level but to a second, slower factor's current level. The
  paper extracts that slow factor as a Kalman-filtered hidden state, which this
  project does not have, so `target_source` picks an observable approximation.
  `"long_term_rate"` (default) refetches the same country's long-term rate
  (`target_ticker` or `target_term`), fits it as its own plain OU factor and
  registers it as `f"{name}_target"`, a correlated factor the short rate reads
  each step. `"ewma"` uses an exponentially weighted moving average of the
  entry's own history, `y(t) = smoothing*x(t) + (1-smoothing)*y(t-1)`: no second
  fetch, factor or correlation, simulated by a stateful
  `MovingTargetEWMAStepper`. Fit by a first-order Euler regression, since a moving
  target has no closed-form exact transition, so the result has no `long_run_mean`.

Also known as: short-rate calibration, Vasicek / Hull-White / CIR fit,
Ornstein-Uhlenbeck mean-reversion fit.

**Args:**

- <u>name (str):</u> this entry's name, used to key params()/changes() and as the factor name in the simulation (e.g. "united_states", "eurozone").
- <u>source (str):</u> "ticker" (Yahoo Treasury-yield ticker, US-only in practice), "oecd" (country-parameterized OECD rate, worldwide), or "gmdb" (the Finance Toolkit's Global Macro Database; covers countries outside the OECD roster, period="yearly" only).
- <u>method (str):</u> "hull_white" (Gaussian, can go negative), "cir" (square-root diffusion), "wilkie_consols" (Wilkie's 1986 Reduced Basis consols yield; requires `inflation`, incompatible with volatility_model="garch"/business_cycle_covariate), or "hibbert_two_factor" (Hibbert, Mowbray and Turnbull's 2001 fast short rate reverting to a moving long-term-rate target, see target_source; incompatible with volatility_model="garch"/business_cycle_covariate). "knw"/"knw_sv" are calibrated by the Knw/KnwSv controllers, not here.
- <u>ticker (str):</u> used when source="ticker"; the ticker to calibrate against, e.g. one of the Yahoo Finance Treasury-yield tickers: "^IRX" (13-week), "^FVX" (5-year), "^TNX" (10-year), "^TYX" (30-year). The Toolkit passed to this controller must include it (e.g. Toolkit(["SPY", "^IRX"], ...)), the same requirement as the Equities controller.
- <u>country (str):</u> used when source="oecd" or "gmdb"; the country to pull the interest-rate series for.
- <u>term (str):</u> used when source="oecd" or "gmdb"; "short" or "long", which series to use.
- <u>period (str):</u> sampling frequency of the underlying data. source="ticker" accepts "daily"/"weekly"/"monthly"/"quarterly"/"yearly"; source="oecd" accepts "monthly"/"quarterly"/"yearly" (no daily/weekly OECD series); source="gmdb" accepts "yearly" only (no monthly/quarterly GMDB series). Determines the time step used to fit.
- <u>volatility_model (str):</u> "constant" (the default) or "garch" (GARCH(1,1) time-varying volatility, Bollerslev 1986). Only valid together with method="hull_white"; CIR's square-root diffusion is a different, incompatible volatility specification.
- <u>business_cycle_covariate (pl.Series &#124; None):</u> a business-cycle indicator's raw historical level series (e.g. LeadingIndicator.series). When supplied, adds an additive drift term on the covariate's step-to-step change (business-cycle conditioning); incompatible with volatility_model="garch".
- <u>business_cycle_covariate_dates (pl.Series &#124; None):</u> the dates paired with `business_cycle_covariate` (e.g. LeadingIndicator.dates), same length and order. Required whenever `business_cycle_covariate` is supplied: this entry's own rate series and the leading indicator are fetched independently and forced onto the same *period* but not guaranteed the same *start date*, so the two are inner-joined on date before fitting, the same way unemployment_controller.py aligns unemployment against inflation.
- <u>inflation (pl.Series &#124; None):</u> required when method="wilkie_consols"; the paired inflation entry's raw historical rate series (Wilkie's dlnQ(t)), at the same period as this entry's own series (the config forces this entry onto the paired entry's period). Unused (must be None) for every other method.
- <u>inflation_weight (float):</u> used only when method="wilkie_consols"; CW, fixed (not fit), Wilkie's own published value is the default.
- <u>inflation_decay (float):</u> used only when method="wilkie_consols"; CD, fixed (not fit), Wilkie's own Reduced Basis value is the default.
- <u>target_source (str):</u> used when method="hibbert_two_factor". "long_term_rate" (the default) refetches this same country's long-term rate (target_term when source="oecd", target_ticker when source="ticker") as a real, independently-simulated slow/target factor. "ewma" instead derives the target as a deterministic EWMA of this entry's own historical path (target_smoothing); no second fetch, no second factor.
- <u>target_term (str):</u> used when method="hibbert_two_factor", target_source="long_term_rate", and source="oecd"; must differ from `term` (enforced at config-validation time, see config_model.InterestRateConfig).
- <u>target_ticker (str):</u> used when method="hibbert_two_factor", target_source="long_term_rate", and source="ticker"; must differ from `ticker`.
- <u>target_smoothing (float):</u> used when method="hibbert_two_factor" and target_source="ewma"; the EWMA weight on each new observation, in (0, 1); smaller means a slower-moving target.

**Returns:**

<u>OUParams &#124; GARCHParams &#124; OUCovariateParams &#124; WilkieConsolsParams &#124; MovingTargetOUParams:</u> the calibrated process parameters: OUParams for "hull_white"/"cir" (its `family` says which), GARCHParams when volatility_model="garch", OUCovariateParams when business_cycle_covariate is supplied, WilkieConsolsParams when method="wilkie_consols", MovingTargetOUParams when method="hibbert_two_factor". Every type carries `initial_value`, the last observed rate, from which the simulation starts.

**Raises:**

- <u>ValueError:</u> if source, method, period (for the given source) or volatility_model is not recognized, volatility_model="garch" is combined with method="cir", business_cycle_covariate is combined with volatility_model="garch", method="wilkie_consols" is missing `inflation` or combined with volatility_model="garch"/ business_cycle_covariate, `inflation` is supplied for any other method, or method="hibbert_two_factor" is combined with volatility_model="garch"/business_cycle_covariate. The fits themselves raise when fewer than 4 observations are supplied, when the fitted mean-reversion speed is not positive (the series shows no mean reversion at this frequency), or, for "wilkie_consols", when the hidden real yield CN(t) is not strictly positive.

**Notes:**

- A median rate above 0.5 (50%) logs a warning: it almost always means a
  percentage-quoted series was not divided by 100.
- CIR floors negative observations at 0 with a warning (Treasury bills printed
  slightly negative yields in 2015 and 2020) and warns, without failing, when the
  Feller condition is violated, since simulated paths may then touch zero more
  often than the theoretical process would.
- Simulation: Hull-White steps with the exact transition above (no
  discretization error, stable for any step size, unconstrained in sign); CIR
  steps with full-truncation Euler (see `step_cir`), so a CIR path can still dip
  slightly below zero.
- `wilkie_consols` is a legacy model: its hidden real yield must stay positive
  throughout the fit window, true for Wilkie's own 1919-1982 UK data and most
  developed-market history since, but not during the 2020-2022 COVID and
  zero-interest-rate era, when real long-term yields went negative across most
  developed markets (verified against live UK and US OECD data). Cap
  `toolkit.end_date` before that era, as `settings/wilkie.yaml` does (1995-2019,
  live-verified clean against US OECD long-term rates). It is a discrete
  recursion with no time step, so `engine.frequency` must equal its `period`.
- `wilkie_consols` pairs the two series by window length, not by date: when the
  inflation history is longer or shorter, both are cut to their common tail.
- Wilkie's 1995 extension (short rate = consols times exp(-spread)) is not
  implemented, only the 1986 original.
- `hibbert_two_factor` needs no `toolkit.end_date` cap and no dedicated settings
  file, unlike `wilkie_consols`. It is real-world only: combining it with
  `measure="risk_neutral"` raises. Hibbert's fixed cross-factor correlations and
  closed-form bond prices are not replicated; correlations come from the same
  estimated correlation matrix as every other factor.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.interest_rates.interest_rates_controller import InterestRates

toolkit = Toolkit(["SPY", "^IRX", "^TNX"], api_key="FINANCIAL_MODELING_PREP_KEY")
rates = InterestRates(toolkit)

rates.calibrate("united_states", ticker="^IRX", period="monthly")
rates.calibrate("united_states_cir", method="cir", ticker="^IRX", period="monthly")
rates.calibrate("germany", source="oecd", country="Germany", period="monthly")
```

Which returns (calibrated on 2026-10-04):

| name | family | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-----|:-------|---------------------:|--------------:|-----------:|--------------:|
| united_states | vasicek | 0.7344 | 0.0488 | 0.0071 | 0.0399 |
| united_states_cir | cir | 0.7344 | 0.0488 | 0.0448 | 0.0399 |
| germany | vasicek | 0.4667 | 0.0359 | 0.0057 | 0.0251 |

The 13-week US Treasury bill rate starts at 3.99% and is pulled toward 4.88% with
a half-life of about eleven months, swinging by about 0.7 percentage points a
year. The CIR fit shares the drift; its 0.0448 is scaled by the square root of the
rate, about 0.9 points a year at 4%, and the Feller condition holds
(0.0717 >= 0.0020). Germany's OECD short rate starts at 2.51% and reverts more
slowly (half-life about 1.5 years) toward 3.59%.

With `method="hibbert_two_factor", target_ticker="^TNX"` on the same Toolkit, the
13-week rate (speed 0.9653, volatility 0.0071, start 3.99%) is pulled toward the
10-year yield, registered as `united_states_target` (speed 1.1438, long-run mean
4.52%, volatility 0.0099, start 5.28%), instead of toward a fixed level.

**References:**

- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. <https://doi.org/10.1016/0304-405x(77>)90016-2
- Hull, J., White, A. (1990). "Pricing Interest-Rate-Derivative Securities." The Review of Financial Studies, 3(4), 573-592. <https://doi.org/10.1093/rfs/3.4.573>
- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). "A Theory of the Term Structure of Interest Rates." Econometrica, 53(2), 385-407. <https://doi.org/10.2307/1911242>
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." Journal of Econometrics, 31(3), 307-327. <https://doi.org/10.1016/0304-4076(86>)90063-1
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>
- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert Limited. <https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf>
- Society of Actuaries & Casualty Actuarial Society (2002). "Report on Modeling of Economic Series Coordinated with Interest Rate Scenarios." <https://www.soa.org/globalassets/assets/files/sections/modeling-of-economic-scenarios.pdf>

## calibrate_risk_neutral

```python
calibrate_risk_neutral(
    name: str,
    source: str = 'ticker',
    ticker: str = '^IRX',
    country: str = 'United States',
    term: str = 'short',
    period: str = 'daily',
) -> DeterministicParams
```

Calibrate one country or region's risk-neutral (Q-measure) short rate as a flat
path at today's observed rate: no fitted stochastic process at all. This is what
`measure: risk_neutral` selects (with `risk_neutral_forward_curve: false`).

In plain terms: under the real-world measure the module asks how the rate has
behaved and projects that forward; under the risk-neutral measure it asks what
today's market says, so that anything priced off the rate cannot be arbitraged.
The minimal correct answer is to take today's observed rate as given and hold it,
rather than fitting a mean-reversion speed and volatility from history and calling
that risk-neutral, since no market price disciplines those.

It fetches the same series `calibrate` would (a Treasury-yield ticker through
`get_historical_data()`, or the OECD or Global Macro Database short- or long-term
rate), but only the last observation is used; no regression is fit, and
`mean_reversion_speed`/`volatility` do not exist for this entry. The result is a
dedicated `DeterministicParams` (`level` and `initial_value`, equal), not a
degenerate `OUParams` with a huge speed and zero volatility: `OUParams`' speed
means reversion toward a mean, which does not apply to something that does not
revert. Simulating a step (`calibration_model.step_deterministic`) returns the
current value unchanged; the shock and time step are accepted, so it plugs into
the same engine, but unused.

Also known as: risk-neutral short rate, Q-measure snapshot, deterministic rate.

**Args:**

- <u>name (str):</u> this entry's name, used to key params()/changes() and as the factor name in the simulation.
- <u>source (str):</u> "ticker" (Yahoo Treasury-yield ticker, US-only in practice), "oecd" (country-parameterized OECD rate, worldwide), or "gmdb" (the Finance Toolkit's Global Macro Database, period="yearly" only).
- <u>ticker (str):</u> used when source="ticker"; same meaning as calibrate().
- <u>country (str):</u> used when source="oecd" or "gmdb"; same meaning as calibrate().
- <u>term (str):</u> used when source="oecd" or "gmdb"; same meaning as calibrate().
- <u>period (str):</u> sampling frequency of the underlying data fetch. Same accepted values as calibrate() for the given source; only the fetch's last observation is used, so this mostly determines how far back the Finance Toolkit needs to look to have at least one point.

**Returns:**

<u>DeterministicParams:</u> level=initial_value=today's observed rate.

**Raises:**

- <u>ValueError:</u> if source or period (for the given source) is not recognized.

**Notes:**

- The full history is still stored, so `changes()` feeds the correlation
  estimate exactly as for a real-world entry.
- Beliefs raise at configuration time when combined with `measure: risk_neutral`,
  as do `volatility_model: garch` and `condition_on_business_cycle`, which this
  path would otherwise silently ignore; `method` must be `hull_white` (or
  `knw_sv`, whose risk-neutral leg is the `KnwSvQ` model).
- Other factors read this level: a risk-neutral equity entry uses
  `interest_rates[0]`'s level as its risk-free rate, and a risk-neutral FX entry
  uses the domestic and foreign entries' levels for its interest-rate-parity drift.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.interest_rates.interest_rates_controller import InterestRates

toolkit = Toolkit(["SPY", "^IRX"], api_key="FINANCIAL_MODELING_PREP_KEY")
rates = InterestRates(toolkit)

rates.calibrate_risk_neutral("united_states", ticker="^IRX")
```

Which returns (calibrated on 2026-10-04):

| Field | Value |
|:------|------:|
| level | 0.0399 |
| initial_value | 0.0399 |

Every simulated path holds the 13-week Treasury bill rate at today's 3.99%.

**References:**

- Hull, J., White, A. (1990). "Pricing Interest-Rate-Derivative Securities." The Review of Financial Studies, 3(4), 573-592. <https://doi.org/10.1093/rfs/3.4.573>

## calibrate_risk_neutral_forward

```python
calibrate_risk_neutral_forward(
    name: str,
    source: str = 'ticker',
    ticker: str = '^IRX',
    country: str = 'United States',
    term: str = 'short',
    period: str = 'daily',
    decay: float = 0.7308,
) -> HullWhiteForwardParams
```

Calibrate one country or region's forward-curve-consistent risk-neutral short
rate: a genuinely stochastic Hull-White rate whose expected path reproduces
today's whole observed forward curve, not just today's level. This is what
`risk_neutral_forward_curve: true` selects, in place of the flat snapshot of
`calibrate_risk_neutral`.

In plain terms: the rate still moves randomly and mean-reverts, but instead of
reverting to one historical average it is steered along the path that today's
Treasury curve implies. If the market prices rates to rise from 3.9% now to about
5.7% in the long run, the average simulated path does exactly that, so cash flows
discounted along these paths agree with today's bond prices.

The model is Brigo and Mercurio's (2006, Section 3.3) "x-process" form of the
extended Vasicek / Hull-White model: `r(t) = x(t) + alpha(t)`, where `x` is a
zero-drift Ornstein-Uhlenbeck process starting at 0 and `alpha(t) = f(0,t) +
sigma^2/(2*a^2)*(1 - e^(-a*t))^2` is a deterministic shift that forces the model
to match the market forward curve `f(0,t)` at every maturity (see
`interest_rates_model.hull_white_alpha`). Two independent fits combine:

1. `mean_reversion_speed` and `volatility` (`a`, `sigma`): the same historical
   Ornstein-Uhlenbeck fit (`calibration_model.fit_ou_process`) the real-world
   `hull_white` method performs on this entry's own short-rate series. They are
   not fit under the risk-neutral measure, because this project has no options or
   swaption prices to identify them from (the same gap the `KnwSvQ` model's
   Q-measure leg has); an explicitly documented simplification.
2. The forward-curve anchor: a Nelson-Siegel curve (level, slope and curvature
   factors with a fixed decay) fit across the four Treasury tenors in
   `term_structure_model.YIELD_CURVE_TENORS` (13-week, 5, 10 and 30 years), taking
   the most recent date's factors; the same anchor `Hjm.calibrate` uses.

The simulation (`interest_rates_model.step_hull_white_forward`) advances `x` by
its exact transition and adds `alpha` back, so it needs the elapsed time, not
just the step size.

Also known as: Hull-White fitted to the initial term structure, extended Vasicek,
arbitrage-free short-rate calibration.

**Args:**

- <u>name (str):</u> this entry's name, used to key params()/changes() and as the factor name in the simulation.
- <u>source (str):</u> "ticker", "oecd", or "gmdb"; same meaning as calibrate(), for the short-rate series the mean-reversion speed/volatility are fit against. The forward-curve anchor always uses the four Yahoo Treasury tenors regardless of this choice.
- <u>ticker (str):</u> used when source="ticker"; same meaning as calibrate().
- <u>country (str):</u> used when source="oecd" or "gmdb"; same meaning as calibrate().
- <u>term (str):</u> used when source="oecd" or "gmdb"; same meaning as calibrate().
- <u>period (str):</u> sampling frequency for both the short-rate fit and the forward-curve fetch. Same accepted values as calibrate() for the given source.
- <u>decay (float):</u> the Nelson-Siegel decay parameter (lambda), annualized; same default (0.7308) as hjm_controller.Hjm.calibrate().

**Returns:**

<u>HullWhiteForwardParams:</u> the historical `mean_reversion_speed` and `volatility`, today's Nelson-Siegel anchor (`anchor_level`, `anchor_slope`, `anchor_curvature`, `anchor_decay`) and `initial_value`, today's instantaneous short rate `alpha(0)`.

**Raises:**

- <u>ValueError:</u> if source or period (for the given source) is not recognized, or the short-rate series shows no mean reversion (fit_ou_process's own non-positive-mean-reversion-speed check).

**Notes:**

- The Toolkit must include every ticker in `YIELD_CURVE_TENORS` (and `ticker`
  itself when source="ticker"); `build_toolkit()` adds them whenever an entry sets
  `risk_neutral_forward_curve`.
- Only valid with `measure: risk_neutral` and `method: hull_white`; beliefs,
  `volatility_model` and `condition_on_business_cycle` are rejected at
  configuration time rather than silently ignored.
- At t = 0 the convexity term is zero, so `initial_value` equals the Nelson-Siegel
  instantaneous forward `level + slope`.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.interest_rates.interest_rates_controller import InterestRates

toolkit = Toolkit(["SPY", "^IRX", "^FVX", "^TNX", "^TYX"], api_key="FINANCIAL_MODELING_PREP_KEY")
rates = InterestRates(toolkit)

rates.calibrate_risk_neutral_forward("united_states", ticker="^IRX", period="monthly")
```

Which returns (calibrated on 2026-10-04):

| Field | Value |
|:------|------:|
| mean_reversion_speed | 0.7344 |
| volatility | 0.0071 |
| anchor_level | 0.0572 |
| anchor_slope | -0.0181 |
| anchor_curvature | -0.0090 |
| anchor_decay | 0.7308 |
| initial_value | 0.0391 |

Today's curve starts at 3.91% (5.72% - 1.81%) and rises toward 5.72% at long
maturities, so the simulated rate is steered upward along that path, with the same
speed and volatility as the real-world fit on the 13-week bill.

**References:**

- Hull, J., White, A. (1990). "Pricing Interest-Rate-Derivative Securities." The Review of Financial Studies, 3(4), 573-592. <https://doi.org/10.1093/rfs/3.4.573>
- Brigo, D., Mercurio, F. (2006). "Interest Rate Models: Theory and Practice" (2nd ed.), Section 3.3. Springer Finance. <https://doi.org/10.1007/978-3-540-34604-3>
- Nelson, C.R., Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." Journal of Business, 60(4), 473-489. <https://doi.org/10.1086/296409>

## names

```python
interestrates.names  # property -> list[str]
```

The names of every interest-rate entry calibrated so far, in calibration order.

## params

```python
params(
    name: str,
) -> OUParams | GARCHParams | OUCovariateParams | DeterministicParams | HullWhiteForwardParams | WilkieConsolsParams | MovingTargetOUParams
```

The calibrated process parameters for one interest-rate entry.

**Args:**

- <u>name (str):</u> the entry's name, as passed to calibrate().

**Raises:**

- <u>RuntimeError:</u> if calibrate(name, ...) hasn't been called yet.

## step_function

```python
InterestRates.step_function(method: str)
```

The step function matching the given method: the exact transition for
hull_white, full-truncation Euler for cir. A plain function of `method`, not tied to any calibrated entry's
instance state; callers derive `method` from `InterestRateConfig.method`
(the same config-is-source-of-truth convention `Scenarios.simulate()` already
uses for belief overrides), so this stays correct even when simulating from a
`CalibrationResult` loaded without ever calling calibrate() on this instance.

**Args:**

- <u>method (str):</u> "hull_white" or "cir".

## changes

```python
changes(name: str) -> pl.DataFrame
```

Dated period-over-period changes in one entry's short rate, from the same
data calibrate() already fetched; reused for cross-factor correlation
estimation (Dependence) instead of triggering a second Finance Toolkit fetch.

**Args:**

- <u>name (str):</u> the entry's name, as passed to calibrate().

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` (pl.Date) and `value` (f64); see helpers.dated_changes().

**Raises:**

- <u>RuntimeError:</u> if calibrate(name, ...) hasn't been called yet.

## series

```python
series(name: str) -> pl.Series
```

The raw historical short-rate level series for one entry, from the same
data calibrate() already fetched; used by other factors' own
rate-conditioned wiring (e.g. equities' method="hibbert_regime_switching",
fit against excess return over this series), which needs the raw level,
unlike changes() which already returns pre-differenced values.

**Args:**

- <u>name (str):</u> the entry's name, as passed to calibrate().

**Raises:**

- <u>RuntimeError:</u> if calibrate(name, ...) hasn't been called yet.

## dates

```python
dates(name: str) -> pl.Series
```

The dates paired with `series(name)`, same length and order; lets a
caller inner-join this entry's raw level series against another
factor's own dates before fitting (e.g. inflation's
condition_on_interest_rate), rather than pairing the two series
positionally, which would silently mismatch whenever either has gaps
or a different history length.

**Args:**

- <u>name (str):</u> the entry's name, as passed to calibrate().

**Raises:**

- <u>RuntimeError:</u> if calibrate(name, ...) hasn't been called yet.
