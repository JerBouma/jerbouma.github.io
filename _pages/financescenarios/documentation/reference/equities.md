---
title: "Equities"
seo_title: "Equities Reference – Finance Scenarios"
excerpt: "Equity indices, sectors, regions and styles with regime switching."
description: "Equity indices, sectors, regions and styles with regime switching."
author_profile: false
permalink: /projects/financescenarios/docs/reference/equities
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Equity indices, sectors, regions and styles with regime switching. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.factors.equities.equities_controller import Equities
```

```python
Equities(toolkit: Toolkit)
```

The Equities module simulates equity prices: a broad stock index, a sector, a region or
an investment style, each tracked through one ticker such as SPY or an ETF. Stock
markets alternate between calm stretches of steady gains and turbulent stretches of
losses and large swings, and that switching is the behavior this module captures.

In plain terms: every run has at least one equity (it is an always-on factor, like
interest rates), and you can add as many as you like, such as the S&P 500, technology
stocks, Europe and emerging markets. Each one is called a "cloud": it is calibrated
on its own and becomes its own variable in the simulated scenarios, linked to the other
equities, interest rates, inflation and the rest through the correlation matrix. One
instance of this class holds every cloud, each keyed by its own `name`; a run with a
single entry (the default: `SPY`, named `equity`) is the plain single-index model.

The model is the regime-switching lognormal model of
[Hardy (2001)](https://doi.org/10.1080/10920277.2001.10595984). Rather than drawing
every return from one distribution, it assumes the market is at any moment in one of
a small number of regimes, for example a calm regime with modest positive returns and
a turbulent regime with negative returns, each with its own mean and volatility of
log-returns (the logarithm of one period's price ratio, which keeps a simulated price
positive). Which regime is active switches over time as a Markov chain: a random
process where the chance of moving to another regime depends only on the current
regime, not on how long the market has been in it. `n_regimes` (default 2, Hardy's
original bull and bear model) sets how many regimes are fitted. Calibration estimates
the regimes with the Baum-Welch expectation-maximization algorithm (see `calibrate`).

When simulating, the regime sequence of each cloud is drawn separately from the
continuous return shock: `equities_model.simulate_regime_path` draws the whole
sequence of regimes for every simulation upfront, from its own random generator,
seeded independently of the correlated-shocks generator (offset from the main seed
by a large constant, `scenarios_controller._REGIME_SEED_OFFSET`, even when both come
from the same user-supplied seed). The discrete regime draws are therefore
statistically independent of the continuous shocks that drive interest rates,
inflation and the equity return itself, and every cloud gets its own regime path, so
technology and energy do not share one bull and bear sequence. Given the active
regime, `equities_model.step_regime_switching` advances the price by one lognormal
step, `next = current * exp(mean + volatility * shock)`, with the active regime's
annual mean scaled by the step length `dt` and its volatility by `sqrt(dt)`. The transition matrix is fit
at the data's frequency and rescaled to the simulation's own step through its
continuous-time generator ([Israel, Rosenthal and Wei, 2001](https://doi.org/10.1111/1467-9965.00114)),
so a monthly fit simulated weekly keeps the right time spent in each regime.

Four options change the model:

- `method` picks the process. `regime_switching` (the default) is Hardy's model on
  raw log-returns. `hibbert_regime_switching` fits the same model to the return in
  excess of a nominal short rate, as in Hibbert, Mowbray and Turnbull
  [(2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf)
  and adds the simulated rate back each step (see `calibrate_hibbert_regime_switching`).
  `wilkie_derived` has no fit of its own: the price is the dividend index divided by
  the dividend yield, as in Wilkie
  [(1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf)
  (see `calibrate_derived`). `knw_sv` is the equity leg of the Koijen, Nijman and
  Werker model, fitted together with its paired interest rate by
  `knw_sv_model.fit_knw_sv_equity_leg` (it reuses `fetch_equity_prices`, not a method
  of this class).
- `condition_on_business_cycle` (with `method: regime_switching` only) makes the
  chance of switching regime depend on the leading indicator, following
  [Filardo (1994)](https://doi.org/10.1080/07350015.1994.10524545), so a turbulent
  regime can become more likely when the economy signals a downturn (see `calibrate_tvtp`).
- `measure: risk_neutral` replaces the regime fit with a single-volatility geometric
  Brownian motion whose drift is the risk-free rate minus the dividend yield, the
  pricing measure of [Black and Scholes (1973)](https://doi.org/10.1086/260062) and
  [Merton (1973)](https://doi.org/10.2307/3003143) (see `calibrate_risk_neutral`).
- `beliefs` replaces the fitted regime means and volatilities with your own.

With the default method a cloud is only correlated with inflation and interest rates,
not driven by them: its regimes are fit purely from the ticker's own history.
`hibbert_regime_switching` and `wilkie_derived` are the two methods that add a real
functional dependency, where the equity step reads another factor's simulated path.

The data are each ticker's adjusted closing prices, obtained through the Finance
Toolkit's `get_historical_data`, from Yahoo Finance or, with a
`FINANCIAL_MODELING_PREP_API_KEY`, Financial Modeling Prep. Any ticker the shared
`Toolkit` holds works, worldwide; `ScenariosConfig.tickers` collects every configured
ticker automatically. The Finance Toolkit silently drops a ticker that equals its
benchmark ticker, which is why `Scenarios` builds its `Toolkit` with
`benchmark_ticker=None`; do the same when building one yourself. A fit needs at least
`n_regimes * 5` price observations and warns below `n_regimes * 20`. The shipped
`factor-sets/broad.yaml` holds 23 worldwide clouds: SPY, eleven US sectors (the
nine original SPDR Select Sector ETFs plus real estate XLRE and communications VOX),
eight regions or countries (Europe, Japan, emerging markets, China, India, Brazil,
Canada, Australia) and three styles (small-cap, value, growth). Newer sector or
single-country ETFs with short histories can be added in your own factor set, as long
as `toolkit.start_date` leaves enough observations.

This does not model heavy-tailed returns within a regime (each regime is normal in
log-returns; the heavy-tailed hidden Markov models of Alswaidan, Jin and Varner are
related literature, not implemented), a volatility smile or skew in the simulated
process, or any risk-neutral variant of `hibbert_regime_switching` or `wilkie_derived`.

Configuration (`equities[i]` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `name` | `equity` | The factor's name in the simulated output; unique across the list. |
| `ticker` | `SPY` | Any ticker the `Toolkit` holds: an index, sector, regional or style ETF. |
| `asset_class` | `null` | A private-market class (e.g. `Private Equity`); sets `ticker` to its listed proxy. |
| `currency` | `USD` | The listing currency; descriptive only, used by reporting. |
| `n_regimes` | `2` | Number of regimes; must be greater than 1. |
| `period` | `monthly` | Price sampling frequency passed to `get_historical_data`. |
| `method` | `regime_switching` | `regime_switching`, `hibbert_regime_switching`, `wilkie_derived` or `knw_sv`. |
| `nominal_rate_name` | `null` | The `interest_rates[i].name` to use; `hibbert_regime_switching`/`knw_sv`. |
| `dividend_growth_name` | `null` | The `dividend_growth[i].name` for the numerator; `wilkie_derived` only. |
| `dividend_yield_name` | `null` | The `dividend_yield[i].name` for the denominator; `wilkie_derived` only. |
| `condition_on_business_cycle` | `false` | Requires `leading_indicator.enabled: true`; `regime_switching` only. |
| `measure` | `real_world` | `real_world` or `risk_neutral`. |
| `volatility_source` | `implied` | `implied`, `svi`, `heston` or `realized`; only with `measure: risk_neutral`. |
| `beliefs.regime_means` | `null` | Override the fitted annual mean log-return per regime. |
| `beliefs.regime_volatilities` | `null` | Override the fitted annual volatility per regime. |

A belief that does not have exactly `n_regimes` entries raises a `ValueError`; a
belief left as `null` keeps the fitted value (applied per entry by
`config_model.apply_equity_beliefs`). In a regime YAML, address one entry's beliefs
with a dotted `"equities.<name>"` key. Beliefs are rejected at configuration time
together with `measure: risk_neutral` (a risk-neutral fit must match market prices
exactly, so a silently honored-looking override would reopen arbitrage) and with
`wilkie_derived` (which has no regimes to override). `wilkie_derived` ignores
`ticker`, `n_regimes` and `period`; `hibbert_regime_switching`, `wilkie_derived` and
`knw_sv` are all incompatible with `measure: risk_neutral`. `expiration_date` of
`calibrate_risk_neutral` is available from Python only, not as a factor-set key.

**References:**

- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. <https://doi.org/10.1080/10920277.2001.10595984>
- Baum, L.E., Petrie, T., Soules, G., Weiss, N. (1970). "A Maximization Technique Occurring in the Statistical Analysis of Probabilistic Functions of Markov Chains." The Annals of Mathematical Statistics, 41(1), 164-171. <https://doi.org/10.1214/aoms/1177697196>
- Israel, R.B., Rosenthal, J.S., Wei, J.Z. (2001). "Finding Generators for Markov Chains via Empirical Transition Matrices, with Applications to Credit Ratings." Mathematical Finance, 11(2), 245-265. <https://doi.org/10.1111/1467-9965.00114>
- Filardo, A.J. (1994). "Business-Cycle Phases and Their Transitional Dynamics." Journal of Business & Economic Statistics, 12(3), 299-308. <https://doi.org/10.1080/07350015.1994.10524545>
- Diebold, F.X., Lee, J.H., Weinbach, G.C. (1994). "Regime Switching with Time-Varying Transition Probabilities." In Hargreaves, C. (ed.), Nonstationary Time Series Analysis and Cointegration, Oxford University Press. <https://doi.org/10.1093/oso/9780198773917.003.0010>
- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert Limited. <https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf>
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>
- Black, F., Scholes, M. (1973). "The Pricing of Options and Corporate Liabilities." Journal of Political Economy, 81(3), 637-654. <https://doi.org/10.1086/260062>
- Merton, R.C. (1973). "Theory of Rational Option Pricing." Bell Journal of Economics and Management Science, 4(1), 141-183. <https://doi.org/10.2307/3003143>
- Alswaidan, A., Jin, C., Varner, J.D. "Continuous Hidden Markov Models for Equity Returns: Heavy-Tail Emission Families and Regime-Conditional Value-at-Risk." arXiv:2606.23492. <https://arxiv.org/abs/2606.23492>

## calibrate

```python
calibrate(name: str, ticker: str, n_regimes: int = 2, period: str = 'monthly') -> RegimeParams
```

Calibrate one equity cloud from its price history: fetch the ticker's adjusted
closing prices, and fit the mean and volatility of the log-return in each regime
(`regime_means`, `regime_volatilities`) and the chance of moving between regimes
each period (`transition_matrix`).

In plain terms: this learns from the past how a market alternates between calm and
turbulent stretches, so the simulated scenarios switch the same way. The diagonal of
the transition matrix is the chance of staying in a regime for one more period, so
the expected stay is 1 / (1 - that chance) periods: a 0.90 monthly chance of
staying calm means calm stretches last about ten months on average.

The fit is the Baum-Welch expectation-maximization (EM) algorithm for hidden
Markov models ([Baum et al., 1970](https://doi.org/10.1214/aoms/1177697196)): the
regime is never observed, only the returns are, so each iteration first estimates
for every historical return the probability that it came from each regime (the
E-step, with the forward-backward algorithm), then re-estimates the regime means,
volatilities and transition probabilities as the probability-weighted
maximum-likelihood values (the M-step). It stops once the log-likelihood (how
well the parameters explain the observed returns) improves by less than `1e-6`,
or after 200 iterations, and warns when it hits that limit unconverged. The fit
also derives the stationary distribution (the long-run share of time spent in
each regime, the eigenvector of the transition matrix for eigenvalue 1) and the
initial regime (the most likely regime at the last observation, where the
simulation starts). Regimes are ordered by mean, so regime 0 is always the one
with the lowest mean return.

`regime_means` and `regime_volatilities` are annualized (divided by the period
length in years and by its square root), so they do not depend on `period`;
`transition_matrix` stays per period of the data and is rescaled to the
simulation's step when simulating. `initial_value` is the last observed price.

Also known as: Markov-switching lognormal model, regime-switching lognormal (RSLN),
hidden Markov model of equity returns.

**Args:**

- <u>name (str):</u> this cloud's name, used to key params()/changes() and as the factor name in the simulation (e.g. "us_broad", "tech", "europe").
- <u>ticker (str):</u> the ticker to calibrate against, held by the Toolkit: a broad equity index like "SPY", or a sector, regional or style ETF.
- <u>n_regimes (int):</u> number of regimes to fit (2 = bull/bear, per Hardy 2001).
- <u>period (str):</u> sampling frequency of the underlying data ("daily", "weekly", "monthly", "quarterly", "yearly").

**Returns:**

<u>RegimeParams:</u> the calibrated regime parameters.

**Raises:**

- <u>ValueError:</u> if period is not recognized, the price history has fewer than `n_regimes * 5` observations, or the fit collapses a regime to almost no observations.

**Notes:**

- A fit with fewer than `n_regimes * 20` observations logs a warning: it clears the
  hard minimum but the regime parameters are likely unstable.
- A regime whose volatility lands at the numerical floor, or whose long-run share is
  below 2%, logs a warning: it is likely a spurious regime that will rarely be
  visited; fewer regimes or a longer window usually helps.
- Belief overrides are not applied here but by the calibration layer
  (`config_model.apply_equity_beliefs`), after this returns.
- The cloud's period-over-period log-returns are stored for `changes()`, which
  feeds the correlation estimate without a second data fetch.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.equities.equities_controller import Equities

toolkit = Toolkit(
    ["SPY", "EFA"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2005-01-01", benchmark_ticker=None
)
equities = Equities(toolkit)

equities.calibrate("us_broad", "SPY", period="monthly")
equities.calibrate("developed_ex_us", "EFA", period="monthly")
```

Which returns (calibrated on 2026-10-04):

| name | regime | regime_mean | regime_volatility | chance of staying | long-run share |
|:-----|-------:|------------:|------------------:|------------------:|---------------:|
| us_broad | 0 | -0.0009 | 0.2020 | 0.8715 | 0.4377 |
| us_broad | 1 | 0.1853 | 0.0793 | 0.9000 | 0.5623 |
| developed_ex_us | 0 | -0.1054 | 0.2567 | 0.8678 | 0.2893 |
| developed_ex_us | 1 | 0.1267 | 0.1096 | 0.9462 | 0.7107 |

Both start in regime 1, the calm one, at prices of 769.64 (SPY) and 103.96 (EFA).
For the S&P 500 the turbulent regime has a flat average return and 20% annual
volatility, the calm one an 18.5% return at 8% volatility, and each lasts about
8 and 10 months on average; developed markets outside the US spend more time calm
(about 19 months per stretch) but lose 10.5% a year in their turbulent regime.

**References:**

- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. <https://doi.org/10.1080/10920277.2001.10595984>
- Baum, L.E., Petrie, T., Soules, G., Weiss, N. (1970). "A Maximization Technique Occurring in the Statistical Analysis of Probabilistic Functions of Markov Chains." The Annals of Mathematical Statistics, 41(1), 164-171. <https://doi.org/10.1214/aoms/1177697196>
- Alswaidan, A., Jin, C., Varner, J.D. "Continuous Hidden Markov Models for Equity Returns: Heavy-Tail Emission Families and Regime-Conditional Value-at-Risk." arXiv:2606.23492. <https://arxiv.org/abs/2606.23492>. Only its shared Gaussian EM/forward-backward machinery is used here, not its heavy-tail emission families.

## calibrate_tvtp

```python
calibrate_tvtp(
    name: str,
    ticker: str,
    business_cycle_covariate: pl.Series,
    business_cycle_covariate_dates: pl.Series,
    n_regimes: int = 2,
    period: str = 'monthly',
) -> RegimeParams
```

Calibrate one equity cloud whose regime switching depends on the business cycle:
the same regime fit as `calibrate()`, plus a regression that makes the chance of
moving between regimes a function of the leading indicator's level. This is the
time-varying transition probability (TVTP) model of
[Filardo (1994)](https://doi.org/10.1080/07350015.1994.10524545).

In plain terms: with `calibrate()` the chance of a calm market turning turbulent is
the same every month; here it rises when the leading indicator (the OECD Composite
Leading Indicator, around 100 in a normal economy and lower ahead of a slowdown)
signals a downturn, so turbulent stretches cluster around weak economies the way
they have historically.

The estimation has two steps, not Filardo's joint maximum likelihood:

1. The same Baum-Welch EM fit as `calibrate()`, on the prices joined by date to
   the leading indicator.
2. Each return is assigned its most likely regime, and for each starting regime a
   multinomial logit (a regression that turns a linear score into probabilities
   that sum to one) is fit of "which regime came next" on the leading indicator's
   level at the start, with a small ridge penalty to keep it finite.

This fit-then-regress approach is the standard two-step simplification of the
applied TVTP literature ([Diebold, Lee and Weinbach, 1994](https://doi.org/10.1093/oso/9780198773917.003.0010));
Filardo's own estimation re-fits the transition probabilities inside every EM
iteration, a much heavier computation. The result is a `RegimeParams` whose
`tvtp` field holds `baseline_log_odds` and `covariate_sensitivity`, one row per
starting regime with column 0 fixed at zero as the reference regime: the chance
of moving from regime i to regime j is proportional to
`exp(baseline_log_odds[i][j] + covariate_sensitivity[i][j] * level)`.

Because each step's transition probabilities depend on the leading indicator's
simulated level at that step, the regime path cannot be drawn upfront the way
`calibrate()`'s is: it is resolved inside the engine's per-step loop by
`equities_model.RegimeTVTPStepper`, which reads `paths["leading_indicator"]`, a
real functional dependency added to this entry's dependency list the same way
every other business-cycle-conditioned factor gets it. This is a different
mechanism from every other `condition_on_business_cycle` flag in the project,
which adds a drift term to an Ornstein-Uhlenbeck process instead.

Also known as: Markov-switching model with time-varying transition probabilities,
TVTP regime switching, business-cycle-conditioned regime switching.

**Args:**

- <u>name (str):</u> this cloud's name, used to key params()/changes() and as the factor name in the simulation.
- <u>ticker (str):</u> the ticker to calibrate against (same meaning as calibrate()).
- <u>business_cycle_covariate (pl.Series):</u> the leading indicator's raw historical level series (e.g. LeadingIndicator.series).
- <u>business_cycle_covariate_dates (pl.Series):</u> the dates paired with `business_cycle_covariate` (e.g. LeadingIndicator.dates).
- <u>n_regimes (int):</u> number of regimes to fit (2 = bull/bear, per Hardy 2001).
- <u>period (str):</u> sampling frequency of the underlying price data.

**Returns:**

<u>RegimeParams:</u> the calibrated regime parameters, with `tvtp` set.

**Raises:**

- <u>ValueError:</u> if period is not recognized, or fit_regime_switching_tvtp's own validation fails (too few date-aligned observations, a collapsed regime, or a transition row too thin to fit).

**Notes:**

- `business_cycle_covariate` is not fetched here: the calibration layer passes in
  the leading indicator's already-fetched series (`LeadingIndicator.series` and
  `LeadingIndicator.dates`), the same "fetch once, pass the series in" convention
  every other `condition_on_business_cycle` factor uses.
- Prices and the indicator are inner-joined on date, not paired by position, since
  the two series are fetched independently and need not start on the same date.
- Every starting regime needs at least `2 * (n_regimes - 1) * 5` observed
  transitions for its own regression, or this raises.
- Requires `leading_indicator.enabled: true` and `method: regime_switching` in a
  factor set.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.equities.equities_controller import Equities
from financescenarios.factors.leading_indicator.leading_indicator_controller import LeadingIndicator

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2005-01-01", benchmark_ticker=None)
leading_indicator = LeadingIndicator(toolkit)
leading_indicator.calibrate(country="United States", period="monthly")

equities = Equities(toolkit)
params = equities.calibrate_tvtp(
    "us_broad", "SPY", leading_indicator.series, leading_indicator.dates, period="monthly"
)
```

Which returns (calibrated on 2026-10-04), the regime fit and its `params.tvtp` rows:

| regime | regime_mean | regime_volatility | baseline_log_odds | covariate_sensitivity |
|-------:|------------:|------------------:|:------------------|:----------------------|
| 0 | -0.0016 | 0.2020 | [0.0, -1.0835] | [0.0, -0.0106] |
| 1 | 0.1876 | 0.0798 | [0.0, -1.9354] | [0.0, 0.0449] |

Reading the calm regime (row 1): at a leading indicator of 105 it moves to the
turbulent regime with a 5.8% chance a month, at 100 with 7.2% and at 95 with 8.9%,
so a weakening economy shortens calm stretches from about 17 to 11 months. The
turbulent regime's own persistence barely moves (an 89% to 90% monthly chance of
staying), and the regime means and volatilities are close to `calibrate()`'s.

**References:**

- Filardo, A.J. (1994). "Business-Cycle Phases and Their Transitional Dynamics." Journal of Business & Economic Statistics, 12(3), 299-308. <https://doi.org/10.1080/07350015.1994.10524545>
- Diebold, F.X., Lee, J.H., Weinbach, G.C. (1994). "Regime Switching with Time-Varying Transition Probabilities." In Hargreaves, C. (ed.), Nonstationary Time Series Analysis and Cointegration, Oxford University Press. <https://doi.org/10.1093/oso/9780198773917.003.0010>
- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. <https://doi.org/10.1080/10920277.2001.10595984>

## calibrate_hibbert_regime_switching

```python
calibrate_hibbert_regime_switching(
    name: str,
    ticker: str,
    risk_free_rate: pl.Series,
    n_regimes: int = 2,
    period: str = 'monthly',
) -> RegimeParams
```

Calibrate one equity cloud the way Hibbert, Mowbray and Turnbull
[(2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf)
do (the Barrie & Hibbert model): the same regime-switching fit as `calibrate()`,
but on the log-return in excess of a paired nominal short rate rather than the raw
log-return, so the regimes describe the equity risk premium, not the total return.

In plain terms: the extra return stocks earn over cash, not the whole return,
switches between a calm and a turbulent regime. When simulating, the simulated
short rate of the paired interest rate is added back on top of the regime draw
each step, so a scenario with higher rates also has higher expected equity
returns, while the premium on top keeps its own regime dynamics.

The excess return of each period is the log-return minus the short rate times the
period length. The fit is otherwise identical to `calibrate()` (Baum-Welch EM, the
same tolerance, ordering and warnings), and the returned `regime_means` are
annualized excess returns. At simulation time
`scenarios_controller._make_hibbert_equity_step` reads the rate's simulated path
directly, a real functional dependency, so the rate is always simulated first.

This is the equity leg of the `factor-sets/hibbert.yaml` framework, which Hibbert's
paper positions against the inflation cascade of Wilkie (1986); its rate and
inflation legs live in `InterestRates` and `Inflation`.

Also known as: Barrie & Hibbert equity model, regime-switching excess return model,
regime-switching equity risk premium.

**Args:**

- <u>name (str):</u> this cloud's name, used to key params()/changes() and as the factor name in the simulation.
- <u>ticker (str):</u> the ticker to calibrate against (same meaning as calibrate()).
- <u>risk_free_rate (pl.Series):</u> the paired interest_rates[] entry's raw historical level series (annualized, decimal fraction). Trailing- truncated to match this ticker's own price history's length if longer; see fit_hibbert_regime_switching's own docstring.
- <u>n_regimes (int):</u> number of regimes to fit (2 = bull/bear, per Hardy 2001).
- <u>period (str):</u> sampling frequency of the underlying price data.

**Returns:**

<u>RegimeParams:</u> the calibrated regime parameters, in excess-return units.

**Raises:**

- <u>ValueError:</u> if period is not recognized, the price history has fewer than `n_regimes * 5` observations, or the fit collapses a regime.

**Notes:**

- `risk_free_rate` is not fetched here: the calibration layer passes in the paired
  `interest_rates[]` entry's already-fetched series (`InterestRates.series()`), named
  by `nominal_rate_name` in a factor set.
- Prices and rates are paired by trailing length (the most recent observations of
  each), not joined on date, so both must be sampled at the same `period`.
- Incompatible with `measure: risk_neutral`; no risk-neutral variant of the excess
  return treatment exists. Belief overrides still apply, in excess-return units.
- The paper's fixed cross-factor correlations (such as dividend yield against equity
  at -0.95) are not replicated: the correlation comes from the same estimated
  matrix every other factor uses.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.equities.equities_controller import Equities
from financescenarios.factors.interest_rates.interest_rates_controller import InterestRates

toolkit = Toolkit(
    ["SPY", "^IRX"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2005-01-01", benchmark_ticker=None
)
rates = InterestRates(toolkit)
rates.calibrate("us_short_rate", ticker="^IRX", period="monthly")

equities = Equities(toolkit)
equities.calibrate_hibbert_regime_switching(
    "us_premium", "SPY", rates.series("us_short_rate"), period="monthly"
)
```

Which returns (calibrated on 2026-10-04):

| regime | regime_mean | regime_volatility | chance of staying | long-run share |
|-------:|------------:|------------------:|------------------:|---------------:|
| 0 | -0.0149 | 0.2016 | 0.8735 | 0.4389 |
| 1 | 0.1651 | 0.0799 | 0.9010 | 0.5611 |

Against the 13-week Treasury bill, the S&P 500's calm regime earns 16.5% a year
above cash and its turbulent regime 1.5% below it; next to `calibrate()`'s total
returns (-0.1% and 18.5%) the regime means drop by roughly the average bill rate
since 2005, while volatilities and regime persistence are almost unchanged.

**References:**

- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert Limited. <https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf>
- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. <https://doi.org/10.1080/10920277.2001.10595984>

## calibrate_risk_neutral

```python
calibrate_risk_neutral(
    name: str,
    ticker: str,
    risk_free_rate: float,
    dividend_yield: float,
    volatility_source: str = 'implied',
    expiration_date: str | None = None,
    period: str = 'monthly',
) -> FXParams
```

Calibrate one equity cloud under the risk-neutral (Q) measure: a geometric Brownian
motion with one constant volatility and a drift fixed at the risk-free rate minus
the dividend yield, the pricing setup of Black and Scholes
[(1973)](https://doi.org/10.1086/260062) and Merton
[(1973)](https://doi.org/10.2307/3003143).

In plain terms: `calibrate()` answers "how has this market actually behaved, and how
is it likely to behave" (the real-world, or P, measure). This answers a different
question: "which drift and volatility are consistent with today's market prices",
so that an option or cash flow valued on the simulated paths does not allow a
riskless profit (an arbitrage). Use it for pricing and market-consistent
valuation, not for forecasting returns: under this measure the expected return is
simply the risk-free rate, whatever the regime history says.

The simulated process is `d(log S) = (r - q - 0.5 * sigma^2) dt + sigma dW`, with
`r` the risk-free rate, `q` the dividend yield and `sigma` the volatility. This
is mathematically the FX model, so the result is an `FXParams` simulated with
`fx_model.step_fx_process` (`equities_model.fit_risk_neutral_equity` is a thin
wrapper); `CalibrationResult.calibrated_params` therefore holds `FXParams`, not
`RegimeParams`, for a risk-neutral entry. The volatility comes from
`volatility_source`:

- `"implied"` (the default): the at-the-money implied volatility, the volatility
  that makes the Black-Scholes price match the market price of the option whose
  strike is nearest today's price, from the Finance Toolkit's
  `options.get_implied_volatility` for one expiration date.
- `"svi"`: the at-the-money value of the Finance Toolkit's SVI-fitted,
  calendar-arbitrage-checked volatility surface (`options.get_volatility_surface`,
  the raw SVI parametrization of
  [Gatheral and Jacquier, 2014](https://doi.org/10.1080/14697688.2013.819986), fit
  per expiration), at the longest fitted expiration. The fit smooths quote noise
  across the whole smile rather than passing one strike's quote through, and the
  longest expiration is the better match for a process simulated over years. The
  simulated process stays single-volatility; the surface only improves where that
  one number comes from.
- `"realized"`: the annualized standard deviation of historical log-returns, the
  same calculation `fx_model.fit_fx_process` performs, over the same price history
  the real-world fit uses. The right choice for tickers without a liquid options
  market, which includes most sector, regional and style ETFs.

`volatility_source: heston` in a factor set goes to `calibrate_heston` instead.

`"implied"` and `"svi"` fall back to the realized volatility (a flat GBM), with a logged
warning, when the options call fails or returns nothing for this ticker.

Also known as: Q-measure equity, market-consistent equity, Black-Scholes-Merton
geometric Brownian motion, cost-of-carry drift.

**Args:**

- <u>name (str):</u> this cloud's name, used to key params()/changes() and as the factor name in the simulation.
- <u>ticker (str):</u> the ticker to calibrate volatility/spot against (same ticker calibrate() would use for this cloud).
- <u>risk_free_rate (float):</u> today's risk-free rate (annualized, decimal fraction), forming this GBM's drift together with dividend_yield.
- <u>dividend_yield (float):</u> today's dividend yield (annualized, decimal fraction).
- <u>volatility_source (str):</u> "implied" (default) reads the at-the-money (nearest-to-spot-strike) options-implied volatility via `self._toolkit.options.get_implied_volatility()`, falling back to realized volatility with a logged warning if that call fails or comes back empty (illiquid ticker, no option chain). "svi" reads the ATM volatility off Finance Toolkit's SVI-fitted, calendar-arbitrage-checked surface instead (`options.get_volatility_surface()`), at the longest fitted expiration: smoothed across the whole smile rather than one raw per-strike Black-Scholes inversion, and the longest expiry is the best available match for a GBM simulated over multiple years; same realized-volatility fallback. "realized" skips the options call entirely and always uses the annualized standard deviation of historical log-returns, the same calculation `fit_fx_process` uses, reused here rather than duplicated, appropriate when no liquid options market exists for this ticker (most sector/ regional/style ETFs).
- <u>expiration_date (str &#124; None):</u> forwarded to `get_implied_volatility(expiration_date=...)` when volatility_source="implied". None (default) uses Finance Toolkit's own most-recent-expiration default. Ignored for "svi" (the surface always resolves its own expirations).
- <u>period (str):</u> sampling frequency of the underlying price data, used for the spot price / realized-volatility-fallback fetch. Same meaning as calibrate()'s `period`.

**Returns:**

<u>FXParams:</u> drift = risk_free_rate - dividend_yield, the resolved volatility, and today's spot price as initial_value.

**Raises:**

- <u>ValueError:</u> if volatility_source or period is not recognized.

**Notes:**

- `risk_free_rate` and `dividend_yield` are not fetched here, so "what counts as r
  and q today" is defined in one place. The calibration layer passes `r` as the
  current level of `interest_rates[0]` (its `DeterministicParams.level` when that
  entry is itself risk-neutral, otherwise the last observed rate); there is no
  per-currency rate mapping yet, so this is one project-wide risk-free rate. It
  passes `q` as the last observed yield of the `dividend_yield[]` entry with the
  same `ticker`, and raises a `ValueError` when no such entry is configured, since
  a silent zero yield would misprice the drift.
- The result is stored in the same registry as the real-world fits, keyed by
  `name`, so the correlation estimate and the dependency graph do not need to know
  which measure produced a cloud.
- The default `expiration_date` is the Finance Toolkit's nearest expiration, which
  can be a day away and have no quotes left; on 2026-10-04 it came back empty for
  SPY and `"implied"` fell back to the realized volatility. Pass a later
  `expiration_date` from Python (it is not a factor-set key) to avoid that.
- Belief overrides are rejected at configuration time for a risk-neutral entry.
- A full smile- or skew-consistent simulation and a market-implied risk-neutral
  density are out of scope: the simulated process has one volatility.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.equities.equities_controller import Equities

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2005-01-01", benchmark_ticker=None)
equities = Equities(toolkit)

runs = [("implied", "2026-12-18"), ("implied", "2027-06-17"), ("svi", None), ("realized", None)]
for source, expiration in runs:
    equities.calibrate_risk_neutral(
        f"spy_{source}_{expiration}", "SPY", risk_free_rate=0.0399, dividend_yield=0.0115,
        volatility_source=source, expiration_date=expiration,
    )
```

Which returns (calibrated on 2026-10-04):

| volatility_source | expiration_date | drift | volatility | initial_value |
|:------------------|:----------------|------:|-----------:|--------------:|
| implied | 2026-12-18 | 0.0284 | 0.1426 | 769.64 |
| implied | 2027-06-17 | 0.0284 | 0.1618 | 769.64 |
| svi | (longest fitted) | 0.0284 | 0.1349 | 769.64 |
| realized | | 0.0284 | 0.1486 | 769.64 |

With a 3.99% Treasury bill rate and a 1.15% dividend yield, SPY drifts at 2.84% a
year under the pricing measure. The options market prices 14.3% volatility for
December and 16.2% for June 2027, the smoothed surface 13.5%, and the history since
2005 shows 14.9%, so the four sources agree to within about three points here.

**References:**

- Black, F., Scholes, M. (1973). "The Pricing of Options and Corporate Liabilities." Journal of Political Economy, 81(3), 637-654. <https://doi.org/10.1086/260062>
- Merton, R.C. (1973). "Theory of Rational Option Pricing." Bell Journal of Economics and Management Science, 4(1), 141-183. <https://doi.org/10.2307/3003143>
- Gatheral, J., Jacquier, A. (2014). "Arbitrage-free SVI Volatility Surfaces." Quantitative Finance, 14(1), 59-71. <https://doi.org/10.1080/14697688.2013.819986>

## calibrate_derived

```python
calibrate_derived(
    name: str,
    dividend_growth_changes: pl.DataFrame,
    dividend_growth_initial_value: float,
    dividend_yield_changes: pl.DataFrame,
    dividend_yield_initial_value: float,
) -> EquityDerivedParams
```

Set up a share price derived from dividends, as in Wilkie
[(1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf):
the price is the dividend index divided by the dividend yield, both already
calibrated sibling factors. There is no data fetch and no statistical fit here;
the starting price is `P(0) = D(0) / Y(0)`.

In plain terms: a dividend yield is the yearly dividend divided by the price, so
the price is the dividend divided by the yield. Wilkie's model simulates
dividends and yields, and the share price follows from them by definition. When
dividends grow or yields fall, the price rises; there is no separate equity
shock, drift or mean reversion.

This is the last link of Wilkie's cascade, where inflation is simulated first and
drives the dividend yield and dividend growth, which in turn give the price:
`factor-sets/wilkie.yaml` wires it as inflation (`wilkie_ar1`) to dividend yield
(`condition_on_inflation: true`) and dividend growth (which reads the yield's
lagged shock) to this price. Each step,
`scenarios_controller._make_equity_derived_step` looks up the two siblings'
simulated values at the same step and divides them, the same "read two sibling
factors each step" capability FX's `drift_mode: irp` uses. Both siblings are real
functional dependencies in `Scenarios._build_dependency_graph()`, so they are
always simulated first. The result is an `EquityDerivedParams`, a minimal type that
only seeds the starting price.

This entry also needs its own `changes()` series for the correlation estimate:
since `log P = log D - log Y`, its log-return is exactly the date-joined
difference of the two siblings' log-changes, a pure combination of data already
fetched. It is an inner join on date rather than the trailing-length alignment
used elsewhere, since both series are already dated.

Also known as: Wilkie share price, dividend-discount derived price, price = dividend
index / dividend yield.

**Args:**

- <u>name (str):</u> this entry's name, used to key params()/changes() and as the factor name in the simulation.
- <u>dividend_growth_changes (pl.DataFrame):</u> the paired dividend_growth[] entry's own `.changes()` output (`date`/`value` columns).
- <u>dividend_growth_initial_value (float):</u> that entry's calibrated `.initial_value`, D(0).
- <u>dividend_yield_changes (pl.DataFrame):</u> the paired dividend_yield[] entry's own `.changes()` output (`date`/`value` columns).
- <u>dividend_yield_initial_value (float):</u> that entry's calibrated `.initial_value`, Y(0).

**Returns:**

<u>EquityDerivedParams:</u> initial_value = dividend_growth_initial_value / dividend_yield_initial_value.

**Notes:**

- In a factor set, `method: wilkie_derived` requires `dividend_growth_name` and
  `dividend_yield_name`, ignores `ticker`, `n_regimes` and `period`, and rejects
  `measure: risk_neutral` (a price ratio has no cost of carry to price under Q)
  and any belief override (there are no regimes to override).
- The shipped `factor-sets/wilkie.yaml` uses JNJ and must be paired with
  `settings/wilkie.yaml`, which ends the data in 2019 for the cascade's Consols
  interest-rate leg.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.dividend_growth.dividend_growth_controller import DividendGrowth
from financescenarios.factors.dividend_yield.dividend_yield_controller import DividendYield
from financescenarios.factors.dividend_yield.dividend_yield_model import reconstruct_dividend_yield_residuals
from financescenarios.factors.equities.equities_controller import Equities
from financescenarios.factors.inflation.inflation_controller import Inflation

toolkit = Toolkit(
    ["JNJ"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1995-01-01", end_date="2019-12-31",
    benchmark_ticker=None,
)
inflation = Inflation(toolkit)
inflation.calibrate("inflation", country="United States", period="monthly", method="wilkie_ar1")
dividend_yield = DividendYield(toolkit)
yield_params = dividend_yield.calibrate("dividend_yield", ticker="JNJ", period="monthly")
yield_residual = reconstruct_dividend_yield_residuals(
    dividend_yield.series("dividend_yield"), yield_params, dividend_yield.time_step("dividend_yield")
)
dividend_growth = DividendGrowth(toolkit)
growth_params = dividend_growth.calibrate(
    "dividend_growth", inflation.series("inflation"), yield_residual, ticker="JNJ", period="monthly"
)

equities = Equities(toolkit)
equities.calibrate_derived(
    "equity",
    dividend_growth_changes=dividend_growth.changes("dividend_growth"),
    dividend_growth_initial_value=growth_params.initial_value,
    dividend_yield_changes=dividend_yield.changes("dividend_yield"),
    dividend_yield_initial_value=yield_params.initial_value,
)
```

Which returns (calibrated on 2026-10-04):

| dividend index D(0) | dividend yield Y(0) | initial_value P(0) | months in changes() |
|--------------------:|--------------------:|-------------------:|--------------------:|
| 3.75 | 0.0263 | 142.47 | 288 |

Johnson & Johnson's trailing twelve-month dividend of $3.75 at a 2.63% yield gives
a starting price of $142.47 at the end of 2019, close to its actual closing price
of $145.87 (the yield is a monthly average, so the two differ slightly). Its
derived monthly log-returns from 1996 to 2019 average 0.66% with a 3.8% standard
deviation.

**References:**

- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>

## calibrate_heston

```python
calibrate_heston(
    name: str,
    ticker: str,
    risk_free_rate: float,
    dividend_yield: float,
    period: str = 'monthly',
) -> HestonParams | FXParams
```

Calibrate one equity cloud under the risk-neutral (Q) measure with the Heston
[(1993)](https://doi.org/10.1093/rfs/6.2.327) stochastic-volatility model, fitted to the Finance Toolkit's
SVI volatility surface at the listed expirations nearest 1, 2, 3, 6, 9 and 12 months, on strikes within 20%
of today's price (`heston_model.fit_heston`).

In plain terms: a flat volatility treats a 20% fall and a 20% rise as equally likely and every horizon as
equally uncertain. Option prices disagree: protection against a crash costs more than a bet on a rally (the
skew), and volatility for a year differs from volatility for a month (the term structure). Heston lets
the variance itself move, mean-revert and rise when prices fall, which reproduces both, so a guarantee or
option valued on these paths prices close to the market's own quote rather than a flat-volatility one.

The drift is still the risk-free rate minus the dividend yield, as in `calibrate_risk_neutral`, and the
simulated paths use the full-truncation scheme of
[Lord, Koekkoek and van Dijk (2010)](https://doi.org/10.1080/14697680802392496)
(`heston_model.HestonStepper`). When the options data or the fit is unavailable, this falls back to
`calibrate_risk_neutral(volatility_source="realized")`, a flat GBM, with a logged warning.

**Args:**

- <u>name (str):</u> this cloud's name.
- <u>ticker (str):</u> the ticker whose options to fit (it needs a liquid listed options market, e.g. SPY).
- <u>risk_free_rate (float):</u> today's risk-free rate, decimal.
- <u>dividend_yield (float):</u> today's dividend yield, decimal.
- <u>period (str):</u> sampling frequency of the price history behind `changes()` and the fallback.

**Returns:**

<u>HestonParams &#124; FXParams:</u> the Heston fit, or the flat-GBM fallback.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.equities.equities_controller import Equities

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", benchmark_ticker=None)
params = Equities(toolkit).calibrate_heston("spy", "SPY", risk_free_rate=0.0399, dividend_yield=0.0115)
```

Which returns (calibrated on 2026-10-07, 545 quotes at six expirations from November 2026 to September 2027):

| Field | Value |
|:------|------:|
| drift | 0.0284 |
| initial_variance | 0.0201 |
| mean_reversion_speed | 14.62 |
| long_run_variance | 0.0219 |
| volatility_of_variance | 1.18 |
| correlation | -0.51 |
| initial_value | 779.09 |
| fit_error | 0.0050 |

Today's volatility is 14.2% (the square root of 0.0201) and the long-run level 14.8%, the price's and the
variance's shocks are correlated by -0.51 (the skew), and the model misses the market's implied volatilities
by half a point on average. Options up to a year out mostly pin down the short end, so the fast mean
reversion (a shock halves in under three weeks) is typical of such fits; a 1-year at-the-money call simulated
on these paths prices at 55.75 against the formula's 55.36.

**References:**

- Heston, S.L. (1993). "A Closed-Form Solution for Options with Stochastic Volatility with Applications to Bond and Currency Options." Review of Financial Studies, 6(2), 327-343. <https://doi.org/10.1093/rfs/6.2.327>
- Lord, R., Koekkoek, R., van Dijk, D. (2010). "A comparison of biased simulation schemes for stochastic volatility models." Quantitative Finance, 10(2), 177-194. <https://doi.org/10.1080/14697680802392496>
- Gatheral, J., Jacquier, A. (2014). "Arbitrage-free SVI Volatility Surfaces." Quantitative Finance, 14(1), 59-71. <https://doi.org/10.1080/14697688.2013.819986>

## names

```python
equities.names  # property -> list[str]
```

The names of every equity cloud calibrated so far, in calibration order.

## params

```python
params(name: str) -> RegimeParams | FXParams | HestonParams | EquityDerivedParams
```

The calibrated parameters for one equity cloud: RegimeParams for a
real-world calibration, FXParams for a risk-neutral one, EquityDerivedParams
for a Wilkie-derived one.

**Args:**

- <u>name (str):</u> the cloud's name, as passed to calibrate()/calibrate_risk_neutral().

**Raises:**

- <u>RuntimeError:</u> if calibrate(name, ...) hasn't been called yet.

## step_function

```python
equities.step_function  # property
```

The regime-switching lognormal step function (stateless, shared across every cloud).

## changes

```python
changes(name: str) -> pl.DataFrame
```

Dated period log-returns for one equity cloud, from the same price data
calibrate() already fetched, reused for cross-factor correlation
estimation (Dependence) instead of triggering a second Finance Toolkit fetch.

**Args:**

- <u>name (str):</u> the cloud's name, as passed to calibrate().

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` (pl.Date) and `value` (f64); see helpers.dated_changes().

**Raises:**

- <u>RuntimeError:</u> if calibrate(name, ...) hasn't been called yet.
