## Reference

The reference is generated from the docstrings in the package, so it says what `help(...)` says in Python: what each class and function does, a worked example with real output where the docstring has one, and the arguments and return value folded underneath.

The factor and model classes are reached through a `Scenarios` object, after `scenarios = Scenarios.from_profiles(...)`:

```python
scenarios.interest_rates  # InterestRates
scenarios.term_structure  # TermStructure
scenarios.hjm             # Hjm
scenarios.knw             # Knw
scenarios.knw_sv          # KnwSv
```

`KnwSvQ` imports as follows:

```python
from financescenarios.models.knw_sv_q.knw_sv_q_controller import KnwSvQ
```

### InterestRates

The Interest Rates module simulates the short rate: the yield on very short lending, such as a 13-week Treasury
bill, which sets the risk-free return and the discount rate in every scenario. Each entry is one country or
region, correlated with the other factors, which read it where they need a risk-free rate. For a whole yield
curve, add the `yield_curve` or `hjm` factor.

The core assumption is mean reversion: central banks raise rates when the economy runs hot and cut them when it
slows, so a short rate is pulled back toward a long-run level. That keeps 30-year projections realistic while
still allowing rate cycles. The default model is the Ornstein-Uhlenbeck process of [Vasicek (1977)](https://doi.org/10.1016/0304-405x(77)90016-2),
`dr = a(theta - r)dt + sigma*dW`: `theta` is the long-run level, `a` the speed of the pull (a gap halves in
ln 2 / `a` years) and `sigma` the size of the random swings `dW`. Shocks are normal, so the rate can go
negative, as euro and yen rates did after 2014, and swing sizes do not depend on the level. `method` picks the
process:

| Method | What it is |
|:-------|:-----------|
| `hull_white` (default) | The model above; the rate can go negative: [Hull and White (1990)][hull-white-1990]. |
| `cir` | Swings shrink with the level, so rates stay at zero or above: [Cox, Ingersoll and Ross (1985)][cir-1985]. |
| `wilkie_consols` | A long yield = expected inflation + a real yield, as in [Wilkie (1986)][wilkie-1986]. |
| `hibbert_two_factor` | Toward a moving long rate: [Hibbert, Mowbray and Turnbull (2001)][hibbert-2001]. |
| `knw` | Linked both ways with a paired inflation entry; fitted by `Knw`. |
| `knw_sv` | `knw` with a shared, randomly changing volatility; fitted by `KnwSv`. |

[hull-white-1990]: https://doi.org/10.1093/rfs/3.4.573
[cir-1985]: https://doi.org/10.2307/1911242
[wilkie-1986]: https://doi.org/10.1017/S0071368600009009
[hibbert-2001]: https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf

Inflation feeds yields in `wilkie_consols`, `knw` and `knw_sv`: a yield carries expected inflation plus a real
return. With `policy_rule`, a `hull_white` short rate follows a monetary-policy rule instead of one long-run level:
it is pulled toward the rate [Taylor (1993, p. 202, eq. 1)](https://doi.org/10.1016/0167-2231(93)90009-L) or the
Federal Reserve's balanced-approach rule prescribes for each scenario's simulated inflation and unemployment, so
scenarios with an inflation spike are also scenarios with high rates, and a recession brings rates down (see
`calibrate_policy_rule`). With `expectations_hypothesis`, a long rate is built on its short rate in each scenario:
the short rate expected over its maturity plus a mean-reverting term premium, as in
[Campbell and Shiller (1991, section 2, eq. 1)](https://doi.org/10.2307/2298008), so the curve inverts when the
short rate jumps and steepens again as it falls back, rather than the two rates drifting apart for decades (see
`calibrate_expectations`).

Real rate volatility comes in bursts (2008, 2022), so `volatility_model: garch` lets the size of the swings change
over time, as in [Bollerslev (1986)](https://doi.org/10.1016/0304-4076(86)90063-1), with `hull_white` only, giving
calm and turbulent stretches and fatter tails. `condition_on_business_cycle` tilts the rate with the leading
indicator. `measure: risk_neutral` follows today's market instead of history, for valuing cash flows at market
prices: a flat path at today's rate or, with `risk_neutral_forward_curve`, a random Hull-White rate whose average
discount factor reproduces today's Treasury curve or, with `risk_neutral_curve: eiopa`, EIOPA's risk-free curve,
the Solvency II default of `Scenarios.simulate(measure="risk_neutral")`.

The data come through the Finance Toolkit, with no API key needed: a Yahoo Finance Treasury yield such as `^IRX`
(`source: ticker`, US only in practice), an OECD member's short- or long-term rate (`oecd`, monthly or slower) or
the Global Macro Database, which adds countries such as Brazil and India (`gmdb`, yearly only). The OECD's rate of
a country can stop months before the calibration date (the United Kingdom's ended in February 2026), so a euro or
pound OECD short rate printed last more than a month before then starts from that print carried forward with the
change in the three-month point between SONIA or the euro short-term rate and the month-end government curve
(`fresh_short_rate_start`); the fit stays on the rates as printed.

The `interest_rates[i]` keys of a factor set and their defaults are listed on the reference page
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/reference/configuration-classes).

Beliefs apply to `hull_white` and `cir` with constant
volatility, not with `risk_neutral`; a regime file addresses one entry as `"interest_rates.<name>"`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
InterestRates(toolkit: Toolkit)
```

</details>

#### InterestRates.calibrate

Calibrate one country or region's short rate from its history: how fast it returns to its normal level
(`mean_reversion_speed`), what that level is (`long_run_mean`) and how much it swings (`volatility`).

These are the real-world parameters: how the rate has actually behaved, so simulated rate cycles are as deep
and as long as history suggests. The speed sets how persistent a shock is: 0.73 a year halves a gap to the
long-run level in about eleven months (ln 2 / 0.73 years), while a slow speed lets low or high rates linger for
years. The long-run level is where rates settle over a long horizon, the number that matters most for
long-dated liabilities, so check it against your own view and override it with `beliefs` where needed. The
default fit regresses each period's change in the rate on its level, as in
[Vasicek (1977)](https://doi.org/10.1016/0304-405x(77)90016-2); the class lists the other methods. The fit
reflects the window you give it: a window dominated by zero rates gives a low long-run level.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.interest_rates.interest_rates_controller import InterestRates

toolkit = Toolkit(["SPY", "^IRX", "^TNX"], api_key="FINANCIAL_MODELING_PREP_KEY")
rates = InterestRates(toolkit)

rates.calibrate("united_states", ticker="^IRX", period="monthly")
rates.calibrate("germany", source="oecd", country="Germany", period="monthly")
```

Which returns (calibrated on 2026-10-19):

| name | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-----|---------------------:|--------------:|-----------:|--------------:|
| united_states | 0.7324 | 0.0491 | 0.0071 | 0.0407 |
| germany | 0.4639 | 0.0364 | 0.0056 | 0.0264 |

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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

**Args:**

- <u>name (str):</u> the entry's name (e.g. "united_states").
- <u>source (str):</u> "ticker" (default), "oecd" or "gmdb".
- <u>method (str):</u> "hull_white" (default), "cir", "wilkie_consols" or "hibbert_two_factor".
- <u>ticker (str):</u> the yield ticker for "ticker", default "^IRX", the 13-week bill; must be in the Toolkit. Ahlgrim, D'Arcy and Gorvett (2005, section 3) likewise proxy the instantaneous short rate with the three-month Constant Maturity Treasury (CMT).
- <u>country (str):</u> the country for "oecd" or "gmdb", default "United States".
- <u>term (str):</u> "short" (default) or "long", for "oecd" or "gmdb".
- <u>period (str):</u> data frequency, default "daily"; "monthly" or slower for "oecd", "yearly" for "gmdb".
- <u>volatility_model (str):</u> "constant" (default) or "garch" ("hull_white" only).
- <u>business_cycle_covariate (pl.Series &#124; None):</u> the leading indicator's level to move with, default None.
- <u>business_cycle_covariate_dates (pl.Series &#124; None):</u> its dates; required with it.
- <u>inflation (pl.Series &#124; None):</u> the paired inflation history, for "wilkie_consols" only (required there).
- <u>inflation_weight (float):</u> how much of expected inflation passes into the long yield (Wilkie's CW), default 1.0, one for one (CW = 1.0 in Wilkie (1986, section 3.15)).
- <u>inflation_decay (float):</u> how fast expected inflation adapts to new inflation (Wilkie's CD), default 0.05 a year, a memory of about 20 years (section 3.15, Reduced Standard Basis, CD = 0.05).
- <u>target_source (str):</u> the "hibbert_two_factor" target: "long_term_rate" (default) or "ewma" (a smoothed average of the rate itself).
- <u>target_term (str):</u> the target's term for "oecd" or "gmdb", default "long"; not equal to `term`.
- <u>target_ticker (str):</u> the target's ticker for "ticker", default "^TNX", the 10-year yield, which Ahlgrim, D'Arcy and Gorvett (2005, section 3) use as their long-rate proxy; not equal to `ticker`.
- <u>target_smoothing (float):</u> the "ewma" weight on each new observation, between 0 and 1, default 0.05, a judgement (an average with a memory of about 20 observations; the paper's target is unobserved).

**Returns:**

<u>OUParams &#124; GARCHParams &#124; OUCovariateParams &#124; WilkieConsolsParams &#124; MovingTargetOUParams:</u> the fitted parameters, including `initial_value`.

**Raises:**

- <u>ValueError:</u> if an option is unknown or two options clash (such as "garch" with "cir"), no data come back, or the history is too short or shows no pull toward a normal level.

</details>

#### InterestRates.calibrate_policy_rule

Calibrate a short rate that follows a monetary-policy rule: how much it moved around the rate the rule
prescribed for actual inflation and unemployment (`volatility`), at the speed the Federal Reserve's inertial
rule closes the gap to it, or a speed fitted on the same history (`mean_reversion_speed`).

A plain mean-reverting rate is pulled toward one long-run level whatever the economy does, so an inflation
spike leaves rates where they were. Under a rule the level itself moves with each scenario's inflation and
unemployment: the neutral real rate plus inflation, plus half the gap of inflation to target, minus one
(Taylor (1993)) or two (the Federal Reserve's balanced-approach rule) times the gap of unemployment to its
longer-run level. Those weights come from
[Taylor (1993, p. 202, eq. 1)](https://doi.org/10.1016/0167-2231(93)90009-L), written with the unemployment
gap through Okun's law as in the Federal Reserve's
[Monetary Policy Report (2026, Box 4, Table A)](https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-part2.htm).
The rate closes part of its gap to the rule each period: by default 0.15 a quarter, the Federal Reserve's
[inertial rule](https://www.federalreserve.gov/monetarypolicy/policy-rules-and-how-policymakers-use-them.htm)
(table "Examples of Policy Rules"), 0.65 a year. `speed="fitted"` fits it on history instead, which reads every
lasting gap between the published rule and the rate as slow adjustment and falls back to the inertial speed,
with a warning, when the rate shows none (see `fit_policy_rule_process`). The volatility is fitted on the
rate's own dates, as the simulation steps it, each reading the inflation and unemployment of its period (a
quarterly figure holds through its quarter), leaving out the months the rate was held at its floor while the
rule prescribed less. `weights="fitted"` replaces the published weights by the rule this rate followed on the
same dates, the partial-adjustment rule of
[Clarida, Galí and Gertler (2000, section II, eqs. (1)-(4))](https://doi.org/10.1162/003355300554692),
fitted jointly with the speed, so it needs `speed="fitted"`; when history does not pin the rule down (a
response that is not significant or has the wrong sign, or no adjustment at all), the published weights stay,
with a warning, and `rule_fit` keeps the estimates (see `fit_policy_rule_weights`). `tracking_error` says how
far the rule's rate was from the observed rate on average, and `smoothed_tracking_error` the same for the rule
reached gradually at that speed. The rule reads inflation as the paired series measures it (consumer prices
here), while the Federal Reserve's 2% target refers to the price index for personal consumption expenditures,
which has tended to run a little lower.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.inflation.inflation_controller import Inflation
from financescenarios.factors.interest_rates.interest_rates_controller import InterestRates
from financescenarios.factors.unemployment.unemployment_controller import Unemployment

toolkit = Toolkit(["^IRX"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2000-01-01")
inflation, unemployment = Inflation(toolkit), Unemployment(toolkit)
inflation.calibrate("united_states", period="monthly")
unemployment.calibrate("united_states", period="monthly")

InterestRates(toolkit).calibrate_policy_rule(
    "united_states",
    inflation=inflation.series("united_states"),
    inflation_dates=inflation.dates("united_states"),
    unemployment=unemployment.series("united_states"),
    unemployment_dates=unemployment.dates("united_states"),
)
```

Which returns (calibrated on 2026-10-17):

| Field | Value |
|:------|------:|
| mean_reversion_speed | 0.6501 |
| volatility | 0.0084 |
| initial_value | 0.0407 |
| speed_source | inertial |
| tracking_error | 0.0288 |
| smoothed_tracking_error | 0.0161 |
| n_held_at_bound | 72 |

At the inertial rule's pace a gap to the Taylor rule halves in 1.1 years, and the rule reached that way stayed
1.6 points from the 13-week bill rate on average since 2000; the 72 months the bill rate sat at zero while the
rule called for less are left out of the volatility. With `speed="fitted"` the same history gives 0.2153, a
half-life of 3.2 years.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_policy_rule(
    name: str,
    inflation: pl.Series,
    inflation_dates: pl.Series,
    unemployment: pl.Series,
    unemployment_dates: pl.Series,
    source: str = 'ticker',
    ticker: str = '^IRX',
    country: str = 'United States',
    period: str = 'monthly',
    economy_period: str = 'monthly',
    rule: str = 'taylor',
    neutral_real_rate: float = 0.012,
    inflation_target: float = 0.02,
    longer_run_unemployment: float = 0.042,
    effective_lower_bound: float = 0.0,
    speed: str = 'inertial',
    weights: str = 'published',
) -> PolicyRuleParams
```

**Args:**

- <u>name (str):</u> the entry's name, also its factor name in the simulation.
- <u>inflation (pl.Series):</u> the paired inflation history, year over year, as decimals.
- <u>inflation_dates (pl.Series):</u> its dates.
- <u>unemployment (pl.Series):</u> the paired unemployment rate history, as decimals.
- <u>unemployment_dates (pl.Series):</u> its dates.
- <u>source (str):</u> "ticker" (default), "oecd" or "gmdb", as in `calibrate`.
- <u>ticker (str):</u> the yield ticker for "ticker", default "^IRX", the 13-week bill.
- <u>country (str):</u> the country for "oecd" or "gmdb", default "United States".
- <u>period (str):</u> the rate's data frequency, default "monthly".
- <u>economy_period (str):</u> the frequency of the inflation and unemployment series, default "monthly".
- <u>rule (str):</u> "taylor" (default) or "balanced".
- <u>neutral_real_rate (float):</u> the neutral real rate, default 0.012, the FOMC's September 2026 longer-run federal funds rate of 3.2% less its 2% longer-run inflation.
- <u>inflation_target (float):</u> the inflation target, default 0.02.
- <u>longer_run_unemployment (float):</u> the unemployment rate at which the rule is neutral, default 0.042, the FOMC's longer-run median of September 2026.
- <u>effective_lower_bound (float):</u> the floor under the rate, default 0.
- <u>speed (str):</u> "inertial" (default), the inertial rule's 0.65 a year, or "fitted" on this history.
- <u>weights (str):</u> "published" (default), the rule's published weights, or "fitted" on this history, with `speed="fitted"`.

**Returns:**

<u>PolicyRuleParams:</u> the speed and fitted volatility with the rule's settings, today's rate and the two tracking errors.

**Raises:**

- <u>ValueError:</u> if `rule`, `speed`, `weights` or a period is unknown, fitted weights come with the inertial speed, no data come back or too few dates overlap.

</details>

#### InterestRates.calibrate_expectations

Calibrate a long rate that follows the expectations hypothesis: the short rate expected over its maturity in
each scenario, plus a term premium whose speed, long-run level, link to the short rate and volatility are
fitted on history (see `fit_term_premium_process`).

Two separately mean-reverting rates, linked only by correlated shocks, let the gap between them wander: a
curve that inverts can stay inverted for decades, which history never showed. Here the long rate is built on
the short rate of the same scenario, as in [Campbell and Shiller (1991, section 2, eq. 1)](https://doi.org/10.2307/2298008):
the part of a short-rate move expected to last over the bond's life passes into the long rate at once, and the
term premium closes most of the rest within a few years. So the curve inverts when the short rate jumps above
where it is expected to settle and steepens again as it falls back. The expected path reverts at
`short_rate_speed` to the short rate's long-run level, so the long rate follows the same anchor or policy rule.
The maturity follows the instrument: 5, 10 or 30 years for `^FVX`, `^TNX` or `^TYX`, 10 for an OECD or GMDB
long rate.

A policy rule's speed says how fast the rate closes its gap to a target that inflation and unemployment keep
moving (0.65 a year for the Federal Reserve's inertial rule), not how long a gap in the short rate lasts,
which is what a bond prices. `short_rate_speed_from="history"` therefore reverts the expected path at the short
rate's own speed, a Hull-White fit on the data the premium is fitted on: 0.114 a year for the US on the OECD's
yearly rates from 1950 to 2025, so a 10-year yield carries 0.60 of a short-rate move rather than 0.15, about
the New York Fed's 0.59 (see `expectations_weight`). The level stays the short rate's own.
`short_rate_change=True` also fits gamma, the premium's move with the short rate's change in the same step,
which history and the New York Fed's estimates show negative (see `fit_term_premium_process`); a short-rate
jump then moves the long rate by D + gamma at once.

The premium is fitted on `history` when given (the long and short rate of a longer record, such as the
OECD's yearly rates since 1950), otherwise on the two rates' own data at `period`. Today's long rate is the
starting point, and the premium's own moves over the recent data set its correlation with the other factors.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.interest_rates.interest_rates_controller import InterestRates

toolkit = Toolkit(["^IRX", "^TNX"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1990-01-01")
rates = InterestRates(toolkit)
short = rates.calibrate("united_states_short_rate", ticker="^IRX", period="monthly")

rates.calibrate_expectations(
    "united_states_long_rate",
    short_rate_name="united_states_short_rate",
    short_rate_speed=short.mean_reversion_speed,
    short_rate_level=short.long_run_mean,
)
```

Which returns (calibrated on 2026-10-19):

| Field | Value |
|:------|------:|
| mean_reversion_speed | 0.3678 |
| term_premium | 0.0166 |
| short_rate_sensitivity | -0.1082 |
| volatility | 0.0097 |
| initial_value | 0.0511 |

Since 1990 the 13-week bill has reverted at only 0.010 a year once the finite-sample bias is taken off its
speed, so the 10-year yield carries 0.95 of every lasting move in it through expectations; the term premium has
averaged 1.66 points, closing half of any gap to that level in 1.9 years.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_expectations(
    name: str,
    short_rate_name: str,
    short_rate_speed: float,
    short_rate_level: float,
    source: str = 'ticker',
    ticker: str = '^TNX',
    country: str = 'United States',
    period: str = 'monthly',
    history: tuple[np.ndarray, np.ndarray, float] | None = None,
    history_volatility: str = 'history',
    short_rate_speed_from: str = 'short_rate',
    short_rate_change: bool = False,
) -> TermPremiumParams
```

**Args:**

- <u>name (str):</u> the entry's name, also its factor name in the simulation.
- <u>short_rate_name (str):</u> the calibrated short-rate entry whose expected path the long rate averages.
- <u>short_rate_speed (float):</u> that short rate's speed of mean reversion, a year.
- <u>short_rate_level (float):</u> that short rate's fitted long-run level, against which history is read.
- <u>source (str):</u> "ticker" (default), "oecd" or "gmdb", as in `calibrate`.
- <u>ticker (str):</u> the long yield's ticker for "ticker", default "^TNX", the 10-year Treasury yield.
- <u>country (str):</u> the country for "oecd" or "gmdb", default "United States".
- <u>period (str):</u> the data frequency, the short rate's own, default "monthly".
- <u>history (tuple[np.ndarray, np.ndarray, float] &#124; None):</u> a longer record to fit on, as (long rate, short rate, time step in years) on shared dates; None (default) fits on the recent data.
- <u>history_volatility (str):</u> with `history`, "history" (default) takes the premium's volatility from it, "recent" from the recent data.
- <u>short_rate_speed_from (str):</u> "short_rate" (default) reverts the expected path at `short_rate_speed`; "history" at the short rate's own speed on the data the premium is fitted on, or at `short_rate_speed`, with a warning, when that data shows no mean reversion.
- <u>short_rate_change (bool):</u> also fit gamma, the premium's move with the short rate's change in the same step; False (the default) leaves it at 0.

**Returns:**

<u>TermPremiumParams:</u> the term premium's fitted dynamics, the short rate's expected-path settings and today's long rate.

**Raises:**

- <u>ValueError:</u> if the short rate has not been calibrated, a period or `short_rate_speed_from` is unknown, no data come back, too few dates overlap, or the premium does not revert.

</details>

#### InterestRates.calibrate_risk_neutral

Calibrate one country or region's risk-neutral short rate: a flat path at today's observed rate.

A real-world calibration asks how the rate has behaved and projects that forward. A risk-neutral one asks what
today's market says, so that nothing priced off the rate offers a riskless profit (no arbitrage). The simplest
answer that respects this is to take today's rate as given and hold it, rather than fit a speed and volatility
that no market price confirms. Every scenario then discounts at the same rate, so all spread in a valuation
comes from the other factors: a risk-neutral equity entry grows at this rate, and a risk-neutral exchange rate
drifts by the gap between two countries' rates (covered interest rate parity). This is what
`measure: risk_neutral` selects. A flat rate ignores the shape of today's curve and gives interest-rate
guarantees no time value, so it does not suit a Solvency II best estimate; use `calibrate_risk_neutral_forward`
(the default of `Scenarios.simulate(measure="risk_neutral")`) when the curve, or interest-rate risk itself,
matters for the valuation.

The rate's history still sets its correlation with the other factors.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.interest_rates.interest_rates_controller import InterestRates

toolkit = Toolkit(["SPY", "^IRX"], api_key="FINANCIAL_MODELING_PREP_KEY")
rates = InterestRates(toolkit)

rates.calibrate_risk_neutral("united_states", ticker="^IRX")
```

Which returns (calibrated on 2026-10-14):

| Field | Value |
|:------|------:|
| level | 0.0406 |
| initial_value | 0.0406 |

Every simulated path holds the 13-week Treasury bill rate at today's 4.06%.

**References:**

- Hull, J., White, A. (1990). "Pricing Interest-Rate-Derivative Securities." The Review of Financial Studies, 3(4), 573-592. <https://doi.org/10.1093/rfs/3.4.573>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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

**Args:**

- <u>name (str):</u> the entry's name, also its factor name in the simulation.
- <u>source (str):</u> "ticker" (default), "oecd" or "gmdb", as in `calibrate`.
- <u>ticker (str):</u> the yield ticker for source="ticker", default "^IRX".
- <u>country (str):</u> the country for source="oecd" or "gmdb", default "United States".
- <u>term (str):</u> the "short" (default) or "long" rate, for source="oecd" or "gmdb".
- <u>period (str):</u> data frequency, default "daily"; the same choices as in `calibrate`.

**Returns:**

<u>DeterministicParams:</u> `level` and `initial_value`, both today's observed rate.

**Raises:**

- <u>ValueError:</u> if `source` or `period` is not recognized, or no data come back.

</details>

#### InterestRates.calibrate_risk_neutral_forward

Calibrate one country or region's risk-neutral short rate that follows today's yield curve: a random,
mean-reverting rate whose average discount factor reproduces today's zero-coupon bond prices.

The rate still moves randomly, but it reverts toward the path today's curve implies rather than toward one
historical average, so the average discount factor across scenarios matches today's bond prices at every
maturity. That is what a market-consistent valuation of interest-rate-sensitive liabilities needs: the curve is
matched exactly, and the spread around it gives guarantees and options their time value, which a flat path
at today's rate cannot. Pass EIOPA's risk-free curve as `discount_curve` (see `eiopa_risk_free_curve`) for a
Solvency II best estimate; `Scenarios.simulate(measure="risk_neutral")` does this for the euro, the pound
and the US dollar. Without one, the curve is a [Nelson and Siegel (1987)](https://doi.org/10.1086/296409) fit to
the latest 13-week, 5, 10 and 30-year Treasury yields (`^IRX`, `^FVX`, `^TNX`, `^TYX`), which the Toolkit
must include.

The model is that of [Hull and White (1990)](https://doi.org/10.1093/rfs/3.4.573) in the form of
[Brigo and Mercurio (2006, section 3.3)](https://doi.org/10.1007/978-3-540-34604-3): `r(t) = x(t) + alpha(t)`, a
mean-reverting random part plus a fixed shift that matches the forward curve at every maturity. Rates are
normally distributed, so they can go negative. The speed and volatility are not implied from swaption prices,
since the Finance Toolkit has no swaption volatilities. The speed is the short rate's own historical speed of
mean reversion. By default the volatility is then fitted so the model moves yields at every maturity as much
as they have moved historically (`fit_hull_white_to_yield_volatilities`): the 13-week, 5, 10 and 30-year
Treasury yields for a ticker source, or the country's short and long rate for "oecd" and "gmdb". That ties the
spread of long rates, which drives the time value of long guarantees, to how much long yields have actually
moved, rather than to the 13-week bill alone, whose moves are damped by the policy rate. The result is
historical, not the market's price of options, so treat the cost of guarantees as indicative. EIOPA's
Guideline 57 (paragraph 1.101) asks that an ESG used for market-consistent valuation be calibrated to data
from deep, liquid and transparent financial markets, which a historical volatility is not; for a
reported best estimate, replace `volatility` with one implied from swaption prices.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.interest_rates.interest_rates_controller import InterestRates

toolkit = Toolkit(
    ["SPY", "^IRX", "^FVX", "^TNX", "^TYX"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2005-01-01"
)
rates = InterestRates(toolkit)

rates.calibrate_risk_neutral_forward("united_states", ticker="^IRX", period="monthly")
```

Which returns (calibrated on 2026-10-14):

| Field | Value |
|:------|------:|
| mean_reversion_speed | 0.0358 |
| volatility | 0.0090 |
| anchor_level | 0.0564 |
| anchor_slope | -0.0165 |
| initial_value | 0.0399 |

Since 2005 the 13-week, 5, 10 and 30-year yields moved 69, 87, 85 and 79 basis points a year; a 90 basis point
short-rate volatility at that speed moves them 89, 82, 75 and 55. Today's curve starts at 3.99% and rises
toward 5.64%, steering the simulated rate upward.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_risk_neutral_forward(
    name: str,
    source: str = 'ticker',
    ticker: str = '^IRX',
    country: str = 'United States',
    term: str = 'short',
    period: str = 'daily',
    decay: float = 0.7308,
    discount_curve: pl.DataFrame | None = None,
    curve_name: str = 'supplied',
    volatility_fit: str = 'yield_curve',
) -> HullWhiteForwardParams
```

**Args:**

- <u>name (str):</u> the entry's name, also its factor name in the simulation.
- <u>source (str):</u> "ticker" (default), "oecd" or "gmdb", for the speed and volatility fit, as in `calibrate`.
- <u>ticker (str):</u> the yield ticker for "ticker", default "^IRX".
- <u>country (str):</u> the country for "oecd" or "gmdb", default "United States".
- <u>term (str):</u> "short" (default) or "long", for "oecd" or "gmdb".
- <u>period (str):</u> data frequency for both fits, default "daily".
- <u>decay (float):</u> the Nelson-Siegel decay of the Treasury curve, which sets where its hump sits, default 0.7308, from Diebold and Li (2006, section 3.2), whose λ of 0.0609 a month puts the medium-term factor's peak loading at 30 months; 0.0609 a month × 12 = 0.7308 a year.
- <u>discount_curve (pl.DataFrame &#124; None):</u> a published curve to reproduce, "maturity" (years) and "rate" (annually compounded), such as EIOPA's; None (default) fits the Treasury curve.
- <u>curve_name (str):</u> the name recorded for `discount_curve`, e.g. "eiopa".
- <u>volatility_fit (str):</u> "yield_curve" (default) fits the volatility to the historical volatility of yields across maturities; "short_rate" takes it from the short rate's own history.

**Returns:**

<u>HullWhiteForwardParams:</u> `mean_reversion_speed`, `volatility`, today's curve and `initial_value`, today's short rate.

**Raises:**

- <u>ValueError:</u> if `source`, `period`, `decay` or `discount_curve` is not valid, no data come back, or the rate shows no pull toward a normal level.

</details>

#### InterestRates.market_path

The short rate the market expected on the start date, year by year for ten years, with the term premium
taken out: the path a policy-rule rate with `expected_path: market` follows (`market_expected_short_rates`).

For the dollar the curve is the New York Fed's fit of the Treasury zero-coupon curve (`acm_term_structure`), so
the term premium comes out of the yields it was estimated on; without it the US Treasury's daily par curve
(bootstrapped to zero rates, `zero_rates_from_par`) is read with no premium taken out, and a warning. For the
euro it is the Deutsche Bundesbank's zero-coupon curve of listed Federal securities and for the pound the Bank of
England's nominal spot curve of gilts, keyless through the Finance Toolkit on the last day the toolkit has. The
Bundesbank compounds its zero rates once a year (Schich (1997, section II.1, note 3, and eq. 6)), the Bank of
England continuously, the convention the path is computed in. No official premium estimate is published for
the euro or the pound, so with `money_market` each gets its own: the regressions of Adrian, Crump and Moench
(2013) run on its own month-end curve over its OECD 3-month rate (`own_term_premium`), as Malik and Meldrum
(2016) run them on the gilt curve. Without it, or when that fit fails, the Treasury premium of the same date
and maturity stands in: Wright (2011) finds term premia falling together across ten countries, and
Jotikasthira, Le and Lundblad (2015) find the co-movement of US, UK and German yields running mostly through
term premia. Without any premium a curve's forward rates, which carry it, would be read as expected short
rates, and a long rate built on them would carry the premium twice. With `bill_days` the path past today is
quoted as that bill's bank discount rate (`bank_discount_rate`), the basis of a bill-rate ticker such as
`^IRX`, so it starts on the basis of today's rate: continuously compounded, the 13-week bill's path would
start 7 basis points above it at 4%.

**References:**

- Adrian, T., Crump, R.K., Moench, E. (2013). "Pricing the Term Structure with Linear Regressions." Journal of Financial Economics, 110(1), 110-138. Section 2.4. <https://doi.org/10.1016/j.jfineco.2013.04.009>
- Wright, J.H. (2011). "Term Premia and Inflation Uncertainty: Empirical Evidence from an International Panel Dataset." American Economic Review, 101(4), 1514-1534. <https://doi.org/10.1257/aer.101.4.1514>
- Jotikasthira, C., Le, A., Lundblad, C. (2015). "Why Do Term Structures in Different Currencies Co-move?" Journal of Financial Economics, 115(1), 58-83. <https://doi.org/10.1016/j.jfineco.2014.09.004>
- Malik, S., Meldrum, A. (2016). "Evaluating the Robustness of UK Term Structure Decompositions Using Linear Regression Methods." Journal of Banking & Finance, 67, 85-102. <https://doi.org/10.1016/j.jbankfin.2016.02.006>
- Bank of England. "Yield curves", yield curve methodology: continuously compounded spot rates. <https://www.bankofengland.co.uk/statistics/yield-curves>
- Schich, S.T. (1997). "Estimating the German Term Structure." Deutsche Bundesbank Discussion Paper 4/97. Section II.1, note 3, and eq. (6). <https://www.bundesbank.de/resource/blob/622394/ab816caf466eeea7dd2fef26d0fbfc30/mL/1997-10-01-dkp-04-data.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
market_path(
    name: str,
    currency: str,
    short_rate: float,
    convergence_speed: float,
    as_of: date | None = None,
    cache_dir: Path | None = None,
    bill_days: int | None = None,
    money_market: tuple[np.ndarray, np.ndarray] | None = None,
) -> MarketPath
```

**Args:**

- <u>name (str):</u> the rate entry's name, for messages.
- <u>currency (str):</u> "USD", "EUR" or "GBP".
- <u>short_rate (float):</u> today's short rate, where the path starts.
- <u>convergence_speed (float):</u> how fast the path converges to the steady state after ten years, the short rate's own speed of mean reversion.
- <u>as_of (date &#124; None):</u> the date the path should describe; a curve more than a month older is refused. Defaults to None, the latest curve.
- <u>cache_dir (Path &#124; None):</u> where the ACM term premia are kept. Defaults to None, the validation cache.
- <u>bill_days (int &#124; None):</u> with a bill-rate short rate, the bill's days to maturity, to quote the path as its bank discount rate; None (the default) keeps the curve's continuously compounded rates.
- <u>money_market (tuple[np.ndarray, np.ndarray] &#124; None):</u> for the euro or the pound, the months (numpy datetime64[M]) and values of the OECD 3-month rate its own term premium is estimated over (`own_term_premium`); None (the default) takes the Treasury premium out instead.

**Returns:**

<u>MarketPath:</u> the expected path, its date and sources.

**Raises:**

- <u>ValueError:</u> if the currency has no curve, none comes back, or it is stale.

</details>

#### InterestRates.own_term_premium

The euro's or the pound's own term premium on a curve's date, from the regressions of Adrian, Crump and
Moench (2013) run on that currency's month-end government curve, as Malik and Meldrum (2016) run them on the
gilt curve, instead of the Treasury premium.

The model is fitted on every month-end up to the curve's date (`monthly_government_curve`): the Bundesbank's
curve from September 1972, the Bank of England's from January 1970, each from the month the OECD's 3-month
rate of that country starts (Germany 1960, the United Kingdom 1986). That rate is the one the excess returns
are measured over and the one the curve's short end is filled from below its first published maturity
(`yields_on_month_grid`), as Malik and Meldrum (2016, note 2) fill the gilt curve from Bank Rate. It is the
rate a euro or pound short rate simulates, so the expected path the premium leaves is that rate's own: the
gap between interbank and government rates goes into the premium, as the New York Fed's premia, which this
code reproduces with the 3-month bill as the short rate, carry the gap between bills and the Treasury curve.
The premium is read on the curve's own date, the factors taken from that day's zero rates (the short end
filled from today's short rate), as the New York Fed reads its daily premia off a monthly model.

**References:**

- Adrian, T., Crump, R.K., Moench, E. (2013). "Pricing the Term Structure with Linear Regressions." Journal of Financial Economics, 110(1), 110-138. Section 3.1. <https://doi.org/10.1016/j.jfineco.2013.04.009>
- Malik, S., Meldrum, A. (2016). "Evaluating the Robustness of UK Term Structure Decompositions Using Linear Regression Methods." Journal of Banking & Finance, 67, 85-102. Section 3 and note 2. <https://doi.org/10.1016/j.jbankfin.2016.02.006>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
InterestRates.own_term_premium(
    currency: str,
    curve_date: date,
    tenors: np.ndarray,
    zero_rates: np.ndarray,
    short_rate: float,
    money_market: tuple[np.ndarray, np.ndarray],
    cache_dir: Path | None = None,
) -> tuple[np.ndarray, np.ndarray, str]
```

**Args:**

- <u>currency (str):</u> "EUR" or "GBP".
- <u>curve_date (date):</u> the date of the curve the market path reads.
- <u>tenors (np.ndarray):</u> that curve's maturities in years.
- <u>zero_rates (np.ndarray):</u> its continuously compounded zero rates, decimals.
- <u>short_rate (float):</u> today's short rate, the 3-month point of today's curve.
- <u>money_market (tuple[np.ndarray, np.ndarray]):</u> the months (numpy datetime64[M]) and values of the OECD 3-month rate, simple annual decimals.
- <u>cache_dir (Path &#124; None):</u> where the month-end curves are kept. Defaults to None, the validation cache.

**Returns:**

<u>tuple[np.ndarray, np.ndarray, str]:</u> the maturities 1 to 10 years, the term premium at each and where it comes from.

**Raises:**

- <u>ValueError:</u> if the curve or the rate cannot be read or the sample is too short.

</details>

#### InterestRates.names

The names of every interest-rate entry calibrated so far, in calibration order.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
interestrates.names  # property -> list[str]
```

</details>

#### InterestRates.params

The calibrated parameters for one interest-rate entry.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
params(
    name: str,
) -> OUParams | GARCHParams | OUCovariateParams | DeterministicParams | HullWhiteForwardParams | WilkieConsolsParams | MovingTargetOUParams | PolicyRuleParams | TermPremiumParams
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

</details>

#### InterestRates.step_function

The one-step rule that moves the rate forward for a given method: `step_hull_white` for "hull_white" and
`step_cir` for "cir", both described below.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
InterestRates.step_function(method: str)
```

**Args:**

- <u>method (str):</u> "hull_white" or "cir".

</details>

#### InterestRates.changes

The historical period-over-period changes in one entry's rate, which set its correlation with the other
factors.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
changes(name: str) -> pl.DataFrame
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

</details>

#### InterestRates.series

The historical rate level for one entry. Other factors use it where they need the level itself rather than its
changes, such as equities' `hibbert_regime_switching` method, which fits returns in excess of this rate.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
series(name: str) -> pl.Series
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

</details>

#### InterestRates.dates

The observation dates that go with `series(name)`, so other data can be lined up with this rate by date.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
dates(name: str) -> pl.Series
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

</details>

### TermStructure

The Term Structure module simulates the whole government yield curve, the yield at every maturity from three
months to thirty years, rather than a single interest rate. It describes each day's curve with three numbers (its
level, slope and curvature) and lets those numbers move through time, so the simulated curve can shift, steepen,
flatten and bend the way the real one does.

The interest rate factor (`InterestRates`) gives you one point on the curve, such as the 13-week Treasury bill.
Switch on `yield_curve` and every simulated future also carries a full curve, so you can read off a simulated
2-year, 10-year or 30-year yield, see how often the curve inverts (short rates above long rates) and value bonds of
any maturity. It is off unless `yield_curve.enabled` is `true`; the shipped `default` and `broad` factor sets
switch it on.

The model is the dynamic Nelson-Siegel model of
[Diebold and Li (2006)](https://doi.org/10.1016/j.jeconom.2005.03.005), built on the curve shape of
[Nelson and Siegel (1987)](https://doi.org/10.1086/296409):

`yield(tenor) = level + slope * slope_loading(tenor) + curvature * curvature_loading(tenor)`

Three factors are enough because almost all of a government curve's day-to-day movement is a parallel shift, a
change in steepness or a change in the hump, and summarising it this way keeps every maturity consistent with
every other: no scenario has a 9-year yield that jumps while the 10-year stands still. The level moves every
maturity equally, the slope weighs most on short maturities and the curvature most on medium ones; how much
depends only on a fixed `decay` (lambda), set rather than fitted, as Diebold and Li do.

Each factor (`rate_level`, `rate_slope`, `rate_curvature`) mean-reverts toward its historical average at its own
fitted speed. In practice the level is slow and the slope and curvature fast, so the scenarios show long rate
cycles with shorter bouts of steepening, flattening or inversion around them, and the curve drifts back toward
its usual upward slope. Shocks are normal, so yields can go negative and the curve can invert, as both have.
The factors link to the short rate, inflation and the rest only through the correlation matrix. Because it is
fitted to history, nothing guarantees the curve is free of arbitrage between maturities; use it for real-world
projections, and `Hjm` when bond prices must be arbitrage-free.

To read a simulated yield at any maturity after a run, pass the three paths to `nelson_siegel_yield`:

```python
from financescenarios.factors.term_structure.term_structure_model import nelson_siegel_yield

ten_year_paths = nelson_siegel_yield(
    result.paths["rate_level"],
    result.paths["rate_slope"],
    result.paths["rate_curvature"],
    tenor=10.0,
    decay=config.yield_curve.decay,
)
```

The `yield_curve` keys of a factor set and their defaults are listed on the reference page
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/reference/configuration-classes).

**References:**

- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. <https://doi.org/10.1016/j.jeconom.2005.03.005>
- Nelson, C.R., Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." The Journal of Business, 60(4), 473-489. <https://doi.org/10.1086/296409>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
TermStructure(toolkit: Toolkit)
```

</details>

#### TermStructure.calibrate

Calibrate the yield curve from history: split each date's curve into its level, slope and curvature, then fit
each of the three as its own mean-reverting process.

This learns how the shape of the yield curve has moved, so the simulated curves shift and twist the way real ones
have. The level is roughly the long-term yield, the slope the short minus the long yield and the curvature
the hump in the middle. Each gets a speed (`mean_reversion_speed`), a normal value (`long_run_mean`), a swing
size (`volatility`) and today's value (`initial_value`), in decimals. A level speed of 0.60 means a parallel
shift has halved after about 14 months (ln 2 / 0.60 years), while a slope speed of 5.6 halves a deviation in
the slope in about six weeks, so simulated inversions are short-lived. The long-run level is where long yields
settle in the scenarios, so it reflects the window: a window full of zero-rate years gives a low one.

Each date's yields are regressed on the fixed loadings of
[Nelson and Siegel (1987)](https://doi.org/10.1086/296409), and each resulting series is fitted as in
[Diebold and Li (2006)](https://doi.org/10.1016/j.jeconom.2005.03.005), the dynamic Nelson-Siegel model.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.term_structure.term_structure_controller import TermStructure

toolkit = Toolkit(["^IRX", "^FVX", "^TNX", "^TYX"], api_key="FINANCIAL_MODELING_PREP_KEY")
term_structure = TermStructure(toolkit)

term_structure.calibrate(period="daily")
```

Which returns (calibrated on 2026-10-19, daily data from 2021-10-20 to 2026-10-16):

| factor | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-------|---------------------:|--------------:|-----------:|--------------:|
| level | 0.7024 | 0.0514 | 0.0088 | 0.0552 |
| slope | 0.5969 | -0.0004 | 0.0116 | -0.0149 |
| curvature | 1.1138 | -0.0165 | 0.0363 | -0.0104 |

Five years are too short to correct the level's and slope's speeds for their finite-sample bias, so those two
keep the plain estimate, with a warning; the curvature's is corrected.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(
    period: str = 'daily',
    decay: float = 0.7308,
    source: str = 'yahoo',
    country: str = 'United States',
) -> YieldCurveParams
```

**Args:**

- <u>period (str):</u> data frequency and time step: "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>decay (float):</u> the Nelson-Siegel decay (lambda), annualized; fixed, not fitted. Defaults to 0.7308, from Diebold and Li (2006, section 3.2), where λ=0.0609 maximizes the loading on the medium-term factor at exactly 30 months; 0.0609 a month × 12 = 0.7308 a year.
- <u>source (str):</u> "yahoo" (four Yahoo treasury tickers), "treasury" (the 12-maturity Treasury par curve; FMP key, daily only, falls back to "yahoo") or "government" (one country's official curve). Defaults to "yahoo".
- <u>country (str):</u> the "government" curve's country, such as "Germany", "Euro Area" or "Japan". Defaults to "United States".

**Returns:**

<u>YieldCurveParams:</u> the fitted `level`, `slope` and `curvature` processes and the `decay`.

**Raises:**

- <u>ValueError:</u> if `period`, `source` or `country` is not recognized, `decay` is not positive, "treasury" gets a non-daily period, or a "government" curve has under three maturities or no mean reversion.

</details>

#### TermStructure.params

The calibrated yield curve: the level, slope and curvature processes and the decay.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
termstructure.params  # property -> YieldCurveParams
```

**Raises:**

- <u>RuntimeError:</u> if the curve has not been calibrated yet.

</details>

#### TermStructure.step_function

The one-step move of each curve factor, `step_curve_factor` below.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
termstructure.step_function  # property
```

</details>

#### TermStructure.changes

The historical period-over-period changes of `rate_level`, `rate_slope` and `rate_curvature`, which set their
correlation with each other and with the other factors.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
termstructure.changes  # property -> dict[str, pl.DataFrame]
```

**Returns:**

<u>dict[str, pl.DataFrame]:</u> one table per factor, with a `date` and a `value` column.

**Raises:**

- <u>RuntimeError:</u> if the curve has not been calibrated yet.

</details>

{% raw %}
### Hjm

The HJM module simulates the whole forward-rate curve with a two-factor Gaussian Heath-Jarrow-Morton model, which
rules out riskless arbitrage between maturities by construction. A forward rate is the interest rate agreed today
for borrowing over a short period that starts at some future date; the forward curve lists those rates for every
start date and carries the same information as the yield curve.

Every other rate factor here, including the `yield_curve` factors of `TermStructure`, learns its drift (the
direction rates tend to move) from how rates mean-reverted in the past. This one does not. Once you choose how
volatile the forward curve is at each maturity, the no-arbitrage condition of
[Heath, Jarrow and Morton (1992)](https://doi.org/10.2307/2951677) fixes the drift, so it is never fitted. Use it
when simulated bond prices across maturities must be consistent with each other, for example to value liabilities
against today's curve; use `yield_curve` when you want curves that behave like history.

Each factor's volatility fades with time to maturity `x`, which makes the model the two-factor Hull-White or G2++
model of [Hull and White (1994)](https://doi.org/10.3905/jod.1994.407908) and
[Brigo and Mercurio (2006)](https://doi.org/10.1007/978-3-540-34604-3). Its two states, `hjm_factor_1` and
`hjm_factor_2`, start at zero and rebuild the forward rate.

The formula is as follows:

$$
\sigma_{i}(x) = \sigma_{i} \cdot \exp(- \kappa_{i} \cdot x)
$$

$$
f(t,\; x) = f_{\text{anchor}}(t + x) + \exp(- \kappa_{1} \cdot x) \cdot x_{1}(t) + \exp(- \kappa_{2} \cdot x) \cdot x_{2}(t) + \Phi(t,\; x)
$$

Where `f_anchor` is today's forward curve from a [Nelson and Siegel (1987)](https://doi.org/10.1086/296409) fit and
`Phi` a convexity term the no-arbitrage condition supplies. Both states and `Phi` start at zero, so the model
starts exactly on today's curve. It is risk-neutral: with the default zero market price of risk there is no term
premium (the extra yield investors demand for long bonds), unlike the real-world rate factors it may run next to.
The factors are Gaussian, so forward rates can go negative, and the slow first factor (see `calibrate`) settles
only over decades, so the spread of long rates keeps widening for a long time: suited to valuation, less so to a
long real-world projection.

To read a simulated 10-year forward rate after a run (`hjm_zero_yield` takes the same inputs and gives a
zero-coupon yield):

```python
import numpy as np

from financescenarios.factors.hjm.hjm_model import hjm_forward_rate

ten_year_paths = hjm_forward_rate(
    result.paths["hjm_factor_1"],
    result.paths["hjm_factor_2"],
    tenor=10.0,
    elapsed_time=np.arange(result.paths["hjm_factor_1"].shape[1]) * config.engine.time_step,
    params=scenarios.hjm.params,
)
```

The `hjm` keys of a factor set and their defaults are listed on the reference page
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/reference/configuration-classes).

**References:**

- Heath, D., Jarrow, R., Morton, A. (1992). "Bond Pricing and the Term Structure of Interest Rates: A New Methodology for Contingent Claims Valuation." Econometrica, 60(1), 77-105. <https://doi.org/10.2307/2951677>
- Hull, J., White, A. (1994). "Numerical Procedures for Implementing Term Structure Models II: Two-Factor Models." The Journal of Derivatives, 2(2), 37-48. <https://doi.org/10.3905/jod.1994.407908>
- Brigo, D., Mercurio, F. (2006). "Interest Rate Models: Theory and Practice" (2nd ed.), chapters 3-4. Springer Finance. <https://doi.org/10.1007/978-3-540-34604-3>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Hjm(toolkit: Toolkit)
```

</details>
{% endraw %}

#### Hjm.calibrate

Calibrate the two-factor HJM model from historical treasury yields: each factor's `volatility`, how fast it
fades with maturity (`volatility_decay`) and their `factor_correlation`, plus today's curve as the anchor the
simulation starts from.

This measures how much, and how differently, the short and long ends of the forward curve have moved, as two
sources of movement: a slow-fading one that shifts the whole curve (factor 1) and a fast-fading one that mostly
moves the short end (factor 2). A factor's effect halves every ln 2 / `volatility_decay` years of maturity.
There is no mean-reversion speed or long-run mean to fit: the no-arbitrage condition sets the drift.

The method fits a [Nelson and Siegel (1987)](https://doi.org/10.1086/296409) curve to the four maturities at every
date, takes the covariance of the changes in its forward rates and picks the two-factor model whose covariance
matches it best, as in [Brigo and Mercurio (2006)](https://doi.org/10.1007/978-3-540-34604-3).
`covariance_fit_error` says how far apart the two are; above 0.35 a warning is logged.

Two factors are the minimum that lets short and long rates move imperfectly together: with one, every maturity
moves in lockstep and a curve can never steepen in one scenario and flatten in another. This is the G2++, or
two-factor Hull-White, calibration to historical forward-rate volatility.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.hjm.hjm_controller import Hjm

toolkit = Toolkit(["^IRX", "^FVX", "^TNX", "^TYX"], api_key="FINANCIAL_MODELING_PREP_KEY")
hjm = Hjm(toolkit)

params = hjm.calibrate(period="daily")
```

Which returns (calibrated on 2026-10-04, daily data from 2021-10-06 to 2026-10-02):

| factor | volatility | volatility_decay | variance_share |
|:-------|-----------:|-----------------:|---------------:|
| factor_1 | 0.0132 | 0.0272 | 0.4856 |
| factor_2 | 0.0518 | 1.8637 | 0.4210 |

with `factor_correlation` -0.5346 and `covariance_fit_error` 0.2604: factor 1 barely fades over 30 years,
factor 2 halves within five months, and the two tend to move in opposite directions.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(
    period: str = 'daily',
    decay: float = 0.7308,
    kappa_bounds: tuple[float, float] = (0.01, 6.0),
) -> HjmParams
```

**Args:**

- <u>period (str):</u> data frequency and time step: "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>decay (float):</u> the Nelson-Siegel decay (lambda), annualized, for the historical and anchor curves. Defaults to 0.7308, from Diebold and Li (2006, section 3.2), whose λ of 0.0609 a month puts the medium-term factor's peak loading at 30 months; 0.0609 a month × 12 = 0.7308 a year.
- <u>kappa_bounds (tuple[float, float]):</u> the lowest and highest `volatility_decay` searched for both factors. Defaults to (0.01, 6.0), a judgement; a floor of 0.03 to 0.10 tempers long-horizon convexity.

**Returns:**

<u>HjmParams:</u> the two factors (`factor_1`, `factor_2`), `factor_correlation`, the `anchor` curve and `covariance_fit_error`.

**Raises:**

- <u>ValueError:</u> if `period`, `decay` or `kappa_bounds` is invalid, or fewer than 30 curve changes remain to fit.

</details>

#### Hjm.params

The calibrated HJM model: the two factors, their correlation and today's anchor curve.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
hjm.params  # property -> HjmParams
```

**Raises:**

- <u>RuntimeError:</u> if the model has not been calibrated yet.

</details>

#### Hjm.step_function

The one-step move of each HJM factor, `step_hjm_factor` below.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
hjm.step_function  # property
```

</details>

#### Hjm.changes

The historical period-over-period changes of `hjm_factor_1` and `hjm_factor_2`, which set their correlation
with the other factors.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
hjm.changes  # property -> dict[str, pl.DataFrame]
```

**Returns:**

<u>dict[str, pl.DataFrame]:</u> one table per factor, with a `date` and a `value` column.

**Raises:**

- <u>RuntimeError:</u> if the model has not been calibrated yet.

</details>

### Knw

The Knw module simulates a short interest rate and inflation as one coupled pair, in which each one's next value
depends on the current level of both. It is the constant-volatility core of the scenario model De Nederlandsche
Bank (DNB), the Dutch central bank, uses for the scenario sets Dutch pension funds and insurers are regulated
against.

The coupling runs both ways. When inflation is high, the central bank tends to raise rates, so today's
inflation feeds next period's rate; and the level of rates feeds back into next period's inflation. Treating
the two as merely correlated would miss this: a scenario with an inflation surge would not, on average, see
rates follow. Both legs are pulled toward the long-run levels the fitted system implies, at a speed set by
the persistence coefficients, and since the shocks are normal, both can go negative. Use it when nominal
liabilities and inflation-linked cash flows must stay consistent with each other, without the extra machinery
of stochastic volatility.

DNB's CP2022 model extends the term-structure model of
[Koijen, Nijman and Werker (2010)](https://doi.org/10.1093/rfs/hhp058) and is specified in full in the
Technical Appendix of [Commissie Parameters (2022)](
https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix). This class keeps its
rate and inflation recursion (eq. 52) at constant volatility, which leaves a bivariate VAR(1): each variable is
regressed on the previous value of both, as in [Lutkepohl (2005)](https://doi.org/10.1007/978-3-540-27752-1).

```text
r(t)  = c_r  + phi_rr*r(t-1)   + phi_r_pi*pi(t-1) + sigma_r*z_r(t)
pi(t) = c_pi + phi_pi_r*r(t-1) + phi_pipi*pi(t-1) + sigma_pi*z_pi(t)
```

`KnwSv` adds DNB's stochastic volatility back, and `KnwSvQ` builds a risk-neutral version on top of that.

The data come from the Finance Toolkit without an API key: the rate from a Treasury-yield ticker or an OECD
country's short or long rate, inflation from OECD consumer price index growth. OECD data are not daily or
weekly, so a pair runs monthly, quarterly or yearly.

In KNW the inflation factor is expected inflation, not the measured rate: the price index follows dPi_t / Pi_t =
pi_t dt + sigma_Pi' dZ_t with pi_t the instantaneous expected inflation in Koijen, Nijman and Werker (2010), so
measured inflation is expected inflation plus noise. KNW filter it from yields and CPI with a Kalman filter
and CP2022 backs it out of a real bond yield; here year-over-year CPI growth stands in for it, a
judgement that keeps the model on keyless data. Averaging twelve months of price changes damps much of that noise;
what is left ends up in the fitted inflation volatility.

A pair is an `interest_rates[i]` and an `inflation[j]` entry; their keys and defaults are listed on the reference page
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/reference/configuration-classes).

Both entries set `method: knw` and name each other, and both use one `period` equal to `engine.frequency`. The
config is rejected otherwise: the fitted coefficients hold per period, so another frequency would compound them
too fast or too slow. Belief overrides, `volatility_model: garch`, `condition_on_business_cycle` and
`condition_on_interest_rate` are not supported on a knw pair.

**References:**

- Koijen, R.S.J., Nijman, T.E., Werker, B.J.M. (2010). "When Can Life Cycle Investors Benefit from Time-Varying Bond Risk Premia?" The Review of Financial Studies, 23(2), 741-780. <https://doi.org/10.1093/rfs/hhp058>
- Commissie Parameters (2022). "Technical Appendix: Specification of the CP2022 Model." <https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix>
- Lutkepohl, H. (2005). "New Introduction to Multiple Time Series Analysis." Springer. <https://doi.org/10.1007/978-3-540-27752-1>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Knw(toolkit: Toolkit)
```

</details>

#### Knw.calibrate_pair

Calibrate one interest rate and inflation pair: fetch both histories and fit how each one pulls on the other.

For each leg you get how much of its own last value carries over (`own_persistence`), how much of the other
leg's last value spills into it (`cross_coupling`), a constant (`intercept`) and the size of its random
surprise per period (`volatility`). An `own_persistence` of 0.9 a quarter means half of a deviation is left
after ln(0.5) / ln(0.9) = 6.6 quarters, ignoring cross effects. Rates and inflation are decimals (0.04 = 4%).

Each leg is one least squares regression of its deviation from its historical average on the previous rate's
and inflation's deviations, a bivariate VAR(1) as in
[Lutkepohl (2005)](https://doi.org/10.1007/978-3-540-27752-1), fitted on mean-adjusted data, so the pair
settles at the history's averages. Only dates both series cover are used, and the fitted system must settle
down over time (be stationary).

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.models.knw.knw_controller import Knw

toolkit = Toolkit(["^IRX"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1990-01-01")
knw = Knw(toolkit)

knw.calibrate_pair("interest_rate", "inflation", period="quarterly")
```

Which returns (calibrated on 2026-10-14):

| leg | intercept | own_persistence | cross_coupling | volatility |
|:----|----------:|----------------:|---------------:|-----------:|
| interest_rate | -0.0005 | 0.9432 | 0.0803 | 0.0043 |
| inflation | 0.0037 | 0.8890 | -0.0206 | 0.0073 |

One percentage point more inflation adds 0.080 points to next quarter's rate, and the pair settles at the
history's averages: a 3.04% rate and 2.72% inflation, a long-run real short rate of 0.3%. That sits below the
1.0% of the Federal Reserve's longer-run projection (a 3.0% federal funds rate against 2.0% PCE inflation in
Federal Reserve (2025, Table 1), the Summary of Economic Projections of September 2025:
https://www.federalreserve.gov/monetarypolicy/files/fomcprojtabl20250917.pdf) and the 1.7% that Koijen, Nijman
and Werker (2010) estimate on 1959-2005 data (5.89% nominal rate, 4.20% expected inflation), because this
history includes the zero-rate years 2009-2015 and 2020-2021. With 36 years of quarterly data and a rate that
keeps 94% of a gap each quarter, the long-run levels carry a sampling error of about 0.6 percentage points.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_pair(
    interest_rate_name: str,
    inflation_name: str,
    period: str,
    interest_rate_source: str = 'oecd',
    interest_rate_ticker: str = '^IRX',
    interest_rate_country: str = 'United States',
    interest_rate_term: str = 'short',
    inflation_country: str = 'United States',
    mean_estimate: Literal['sample', 'regression'] = 'sample',
) -> tuple[KnwParams, KnwParams]
```

**Args:**

- <u>interest_rate_name (str):</u> the rate leg's name, its key in `params()` and the simulation.
- <u>inflation_name (str):</u> the inflation leg's name.
- <u>period (str):</u> the shared sampling frequency, also the simulation's: "monthly", "quarterly" or "yearly".
- <u>interest_rate_source (str):</u> "oecd" (OECD rate) or "ticker" (Yahoo Finance Treasury yield). Defaults to "oecd".
- <u>interest_rate_ticker (str):</u> the Treasury-yield ticker when the source is "ticker". Defaults to "^IRX".
- <u>interest_rate_country (str):</u> the country when the source is "oecd". Defaults to "United States".
- <u>interest_rate_term (str):</u> "short" or "long" OECD rate when the source is "oecd". Defaults to "short".
- <u>inflation_country (str):</u> the country whose OECD consumer price index is used. Defaults to "United States".
- <u>mean_estimate (str):</u> "sample" (default) puts the long-run levels at the history's averages; "regression" at the free intercepts of the two regressions.

**Returns:**

<u>tuple[KnwParams, KnwParams]:</u> (interest_rate_params, inflation_params), with the fields above plus `initial_value`, the last observation.

**Raises:**

- <u>ValueError:</u> if fewer than 5 dates overlap, or the fitted coupling is not stationary.

</details>

#### Knw.names

The names of every knw leg calibrated so far (both legs of every pair), in calibration order.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
knw.names  # property -> list[str]
```

</details>

#### Knw.params

The calibrated parameters of one knw leg.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
params(name: str) -> KnwParams
```

**Args:**

- <u>name (str):</u> the leg's name, as passed to calibrate_pair().

**Raises:**

- <u>RuntimeError:</u> if calibrate_pair(...) naming this leg hasn't been called yet.

</details>

#### Knw.series

The historical series one knw leg was calibrated on.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
series(name: str) -> pl.Series
```

**Args:**

- <u>name (str):</u> the leg's name, as passed to calibrate_pair().

**Raises:**

- <u>RuntimeError:</u> if calibrate_pair(...) naming this leg hasn't been called yet.

</details>

#### Knw.dates

The dates paired with series(name), same length and order.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
dates(name: str) -> pl.Series
```

**Args:**

- <u>name (str):</u> the leg's name, as passed to calibrate_pair().

**Raises:**

- <u>RuntimeError:</u> if calibrate_pair(...) naming this leg hasn't been called yet.

</details>

#### Knw.changes

The dated period-over-period changes of one knw leg, used to estimate its correlation with other factors
without fetching the data again.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
changes(name: str) -> pl.DataFrame
```

**Args:**

- <u>name (str):</u> the leg's name, as passed to calibrate_pair().

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if calibrate_pair(...) naming this leg hasn't been called yet.

</details>

#### Knw.step_function

The function that moves any knw leg forward by one period, given its parameters and the other leg's
current value.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Knw.step_function()
```

</details>

### KnwSv

The KnwSv module simulates the interest rate and inflation as a two-way coupled pair, like `Knw`, plus a shared,
hidden "market nervousness" factor `v` that makes both swing harder in turbulent periods and calmer in quiet ones.

Real markets alternate between spells of calm and stress, and in stress rates and inflation move sharply at the
same time. The CP2022 model of De Nederlandsche Bank (DNB), the Dutch central bank, captures this with one random
variance factor scaling the volatility of everything. The result is volatility clustering and fatter tails than
`Knw`: a turbulent spell lasts a while before it fades, which matters for multi-year solvency projections.

The model is the stochastic-volatility form of [Koijen, Nijman and Werker (2010)](https://doi.org/10.1093/rfs/hhp058)
that [Commissie Parameters (2022, eq. 2-5)](
https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix) specifies.
`v` follows the CIR process of [Cox, Ingersoll and Ross (1985)](https://doi.org/10.2307/1911242), the mean-reverting,
never-negative variance process of [Heston (1993)](https://doi.org/10.1093/rfs/6.2.327), and both legs read its
previous level in their drift and variance:

```text
r(t)  = c_r  + gamma_r*v(t-1)  + phi_rr*r(t-1)   + phi_r_pi*pi(t-1)
        + sqrt(base_r  + sens_r*v(t-1))*z_r(t)
pi(t) = c_pi + gamma_pi*v(t-1) + phi_pi_r*r(t-1) + phi_pipi*pi(t-1)
        + sqrt(base_pi + sens_pi*v(t-1))*z_pi(t)
```

With `variance_coupling` (gamma) and `variance_sensitivity` (sens) at zero this is exactly `Knw`. `v` is simulated
with the QE scheme of [Andersen (2008)](https://doi.org/10.21314/jcf.2008.189), which never goes negative; the rate
and inflation can. DNB treats `v` as an input observed without measurement error (Commissie Parameters
(2022, section 4)) and backs the rate and expected inflation out of a nominal and
a real yield; here `v` is estimated from history instead, as a rolling average of the pair's squared surprises.
An optional equity leg (`calibrate_equity_leg`) reads the same `v`, so stock and rate turbulence rise together.

`v` follows the first row of the appendix's eq. 2, dv = K_vv * (E_v - v) * dt + omega * sqrt(v) * dW, a
Heston-type stochastic variance process equal to the square of the stochastic volatility.
DNB's eq. 3 also lets the rate and inflation load on `v`'s own shock (sigma_vr, sigma_vpi); here `v`'s shock is
independent of theirs, a simplification that leaves out any leverage-type link between turbulence and rates.

A pair is an `interest_rates[i]` and an `inflation[j]` entry, plus an optional `equities[k]` leg; their keys and
defaults are listed on the reference page
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/reference/configuration-classes).

Data sources and pairing rules are as for `Knw`, and a `knw_sv` entry's partner must also be `knw_sv`. Every
entry sharing a `v`, the equity leg included, must use one `period` equal to `engine.frequency`, which the config
enforces: a mismatch compounds the fit too fast or too slow. `measure: risk_neutral` on both entries simulates
under `KnwSvQ`'s Q-measure; an equity leg cannot name such a rate.

**References:**

- Koijen, R.S.J., Nijman, T.E., Werker, B.J.M. (2010). "When Can Life Cycle Investors Benefit from Time-Varying Bond Risk Premia?" The Review of Financial Studies, 23(2), 741-780. <https://doi.org/10.1093/rfs/hhp058>
- Commissie Parameters (2022). "Technical Appendix: Specification of the CP2022 Model." <https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
KnwSv(toolkit: Toolkit)
```

</details>

#### KnwSv.calibrate_triple

Calibrate one `v`, interest rate and inflation triple: fetch both histories, estimate the hidden turbulence
factor `v`, and fit how each leg depends on `v`, itself and the other leg.

`v_params` give the turbulence's normal level (`long_run_mean`), how fast a spike fades (`mean_reversion_speed`,
a half-life of ln 2 / speed years) and how jumpy it is (`volatility`). A leg's `variance_sensitivity` says how
much its per-period variance grows with `v`, and `variance_coupling` how much `v` shifts its expected next
value; the rest reads as in `Knw.calibrate_pair`.

The surprises of a constant-volatility fit, averaged over the past year and lagged one, stand in for `v`; a CIR
process, as in [Cox, Ingersoll and Ross (1985)](https://doi.org/10.2307/1911242), is fit to that, and both legs
are refit with `v` as an extra input. If no leg's variance rises with `v`, a warning suggests `method: knw`: the
history then shows no volatility clustering worth modelling. Read `v`'s parameters with
`params(variance_factor_name(interest_rate_name))`.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.models.knw_sv.knw_sv_controller import KnwSv

toolkit = Toolkit(["^IRX"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1990-01-01")
knw_sv = KnwSv(toolkit)

knw_sv.calibrate_triple("interest_rate", "inflation", period="quarterly")
```

Which returns (calibrated on 2026-10-05):

| | mean_reversion_speed | long_run_mean | initial_value |
|:--|---------------------:|--------------:|--------------:|
| v | 0.3988 | 0.0000627 | 0.0000094 |

| leg | variance_coupling | base_variance | variance_sensitivity |
|:----|------------------:|--------------:|---------------------:|
| interest_rate | -5.5025 | 0.0000152 | 0.0322 |
| inflation | -0.2861 | 0.0000099 | 0.5858 |

`v` halves in about 1.7 years and sits below its normal level, so the pair is calmer than usual.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_triple(
    interest_rate_name: str,
    inflation_name: str,
    period: str,
    interest_rate_source: str = 'oecd',
    interest_rate_ticker: str = '^IRX',
    interest_rate_country: str = 'United States',
    interest_rate_term: str = 'short',
    inflation_country: str = 'United States',
    variance_window: int | None = None,
) -> tuple[OUParams, KnwSvLegParams, KnwSvLegParams]
```

**Args:**

- <u>interest_rate_name (str):</u> the rate leg's name, its key in `params()` and the simulation.
- <u>inflation_name (str):</u> the inflation leg's name.
- <u>period (str):</u> the shared sampling frequency, also the simulation's: "monthly", "quarterly" or "yearly".
- <u>interest_rate_source (str):</u> "oecd" or "ticker", as in `Knw.calibrate_pair`. Defaults to "oecd".
- <u>interest_rate_ticker (str):</u> the ticker for the "ticker" source. Defaults to "^IRX".
- <u>interest_rate_country (str):</u> the country for the "oecd" source. Defaults to "United States".
- <u>interest_rate_term (str):</u> "short" or "long" OECD rate. Defaults to "short".
- <u>inflation_country (str):</u> the country of the OECD consumer price index. Defaults to "United States".
- <u>variance_window (int &#124; None):</u> the observations averaged into each `v` estimate. Defaults to None, one year at `period` (4 quarters or 12 months), the window of Engle's (1982) four-quarter ARCH model.

**Returns:**

<u>tuple[OUParams, KnwSvLegParams, KnwSvLegParams]:</u> (v_params, interest_rate_params, inflation_params).

**Raises:**

- <u>ValueError:</u> if fewer than one year plus 7 dates overlap, or the fitted coupling is not stationary.

</details>

#### KnwSv.calibrate_equity_leg

Calibrate an equity index that shares an already calibrated knw_sv pair's turbulence factor `v`.

The index earns the simulated short rate plus a constant risk premium, and its swings grow when `v` is high.
Equity and rate turbulence therefore rise and fall together, rather than being linked only through a fixed
correlation.
`risk_premium` is the extra log return per period over the short rate (0.02 a quarter is roughly 8% a year),
`base_variance` the per-period variance when `v` is zero, and `variance_sensitivity` how much variance each
unit of `v` adds. Without a link to `v`, `variance_sensitivity` is 0 and a warning says so.

This is the equity row of DNB's model in [Commissie Parameters (2022, eq. 4-5)](
https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix), a
[Heston (1993)](https://doi.org/10.1093/rfs/6.2.327) style index on a random short rate:
`d ln(S) = (r + risk_premium - 0.5*var)dt + sqrt(var)dW`, with `var = base_variance + variance_sensitivity*v`.
It is fit on price history only, where DNB also uses option prices, and runs under the real-world measure only.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.equities.equities_controller import fetch_equity_prices
from financescenarios.models.knw_sv.knw_sv_controller import KnwSv

toolkit = Toolkit(["^GSPC"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1990-01-01")
knw_sv = KnwSv(toolkit)
knw_sv.calibrate_triple("interest_rate", "inflation", period="quarterly")

dates, prices = fetch_equity_prices(toolkit, "^GSPC", "quarterly")
knw_sv.calibrate_equity_leg("equity", "interest_rate", "inflation", prices, dates, period="quarterly")
```

Which returns (calibrated on 2026-10-05):

| name | risk_premium | base_variance | variance_sensitivity | initial_value |
|:-----|-------------:|--------------:|---------------------:|--------------:|
| equity | 0.0159 | 0.0042 | 26.0769 | 7773.95 |

The S&P 500 earned 1.59% a quarter above the short rate, with a volatility of about 13% a year at `v = 0` and
15.3% at `v`'s long-run level.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_equity_leg(
    equity_name: str,
    interest_rate_name: str,
    inflation_name: str,
    equity_prices: pl.Series,
    equity_dates: pl.Series,
    period: str,
) -> KnwSvEquityParams
```

**Args:**

- <u>equity_name (str):</u> the equity leg's name, its key in `params()` and the simulation.
- <u>interest_rate_name (str):</u> the rate leg's name of the already calibrated pair to share `v` with.
- <u>inflation_name (str):</u> the same pair's inflation leg's name.
- <u>equity_prices (pl.Series):</u> historical index levels (not returns).
- <u>equity_dates (pl.Series):</u> the dates of `equity_prices`, same length.
- <u>period (str):</u> the pair's sampling frequency as passed to `calibrate_triple`: "monthly", "quarterly" or "yearly".

**Returns:**

<u>KnwSvEquityParams:</u> `risk_premium`, `base_variance`, `variance_sensitivity` and `initial_value` (the last price).

**Raises:**

- <u>ValueError:</u> if `period` is not supported, the prices and dates differ in length, or fewer than 6 dates overlap with the pair.
- <u>RuntimeError:</u> if `calibrate_triple` has not been run for this pair.

</details>

#### KnwSv.names

The names of everything calibrated so far, in calibration order: both legs of every pair, each pair's
`v` (see `variance_factor_name`) and any equity leg.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
knwsv.names  # property -> list[str]
```

</details>

#### KnwSv.params

The calibrated parameters of one knw_sv leg or `v`: an `OUParams` for `v`, a `KnwSvLegParams` for an
interest rate or inflation leg, a `KnwSvEquityParams` for an equity leg.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
params(name: str) -> OUParams | KnwSvLegParams | KnwSvEquityParams
```

**Args:**

- <u>name (str):</u> the leg's name, or `variance_factor_name(interest_rate_name)` for a pair's `v`.

**Raises:**

- <u>RuntimeError:</u> if nothing has been calibrated under this name yet.

</details>

#### KnwSv.series

The historical series one knw_sv leg was calibrated on (`v` has no series of its own).

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
series(name: str) -> pl.Series
```

**Args:**

- <u>name (str):</u> the leg's name, as passed to calibrate_triple().

**Raises:**

- <u>RuntimeError:</u> if calibrate_triple(...) naming this leg hasn't been called yet.

</details>

#### KnwSv.dates

The dates paired with series(name), same length and order.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
dates(name: str) -> pl.Series
```

**Args:**

- <u>name (str):</u> the leg's name, as passed to calibrate_triple().

**Raises:**

- <u>RuntimeError:</u> if calibrate_triple(...) naming this leg hasn't been called yet.

</details>

#### KnwSv.changes

The dated period-over-period changes of one knw_sv leg, used to estimate its correlation with other factors
without fetching the data again.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
changes(name: str) -> pl.DataFrame
```

**Args:**

- <u>name (str):</u> the leg's name, as passed to calibrate_triple().

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if calibrate_triple(...) naming this leg hasn't been called yet.

</details>

### KnwSvQ

The KnwSvQ module turns a calibrated `KnwSv` pair into a risk-neutral (Q-measure) model: it learns the market
price of risk that makes the model reproduce the observed Treasury yield curve, and then prices zero-coupon bonds
in closed form, simulates the pair under Q, or builds a stochastic deflator for a real-world run.

A real-world (P-measure) simulation answers "where might rates go?", while pricing needs the risk-neutral view
"what is a future cash flow worth today?". The bridge between the two is the market price of risk, the extra
return investors demand for bearing each source of risk. This module fits that price so the model's yields match
the 13-week, 5-, 10- and 30-year Treasury yields, then gives you model yields at any maturity
(`zero_coupon_yield`), the Q-measure parameters to simulate with (`q_params`) and a deflator to price claims off
a real-world run (`deflator`).

De Nederlandsche Bank (DNB) fits its Q-measure to nominal yields at 1, 5, 10, 20 and 30 years and real yields at 1, 5,
15, 20 and 30 ([Commissie Parameters (2022, section 4)](
https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix)), and constrains it with
option, swaption and inflation-cap implied volatilities (section 5, eq. 25), data this project does not have. This
module keeps the yield-curve part on the four US Treasury points Yahoo Finance quotes (13 weeks, 5, 10 and 30 years):
no real yields and no implied volatilities. The price of risk is completely affine as in [Duffie and Kan
(1996)](https://doi.org/10.1111/j.1467-9965.1996.tb00123.x), with five parameters that change only the drift: under Q,
`v`'s mean-reversion speed is its real-world speed plus `risk_premium_v`, and each leg's `intercept` and
`variance_coupling` drop by its constant and variance premium. Everything else stays the same, so the Q parameters
simulate exactly like the P ones. Bond prices come from a discrete-time affine recursion: the price `n` periods out is
`exp(A[n] + Bv[n]*v + Br[n]*r + Bpi[n]*pi)`.

The stochastic deflator follows [Cheng and Planchet
(2019)](https://www.journaleska.com/index.php/bmi/article/view/9378): a per-path weight `D(T)` such that the average
of `D(T)*payoff(T)` over a real-world run prices the claim. It is accurate only when `risk_premium_v` is small
relative to `v`'s mean-reversion speed (`calibrate_mpr` warns past 5%), and it needs the path of `v`, which a scenario
set does not include, so you simulate and record it yourself.

The closed-form prices, the market price of risk fit and the deflator all use the correlation of the rate and
inflation shocks, estimated from the same period changes the scenarios' correlation matrix is built from, so model
prices and discounting along simulated paths agree. Limits: the inflation premiums are weakly identified from a
nominal-only curve, and there is no Q-measure equity leg.

Configuration: set `measure: risk_neutral` on both entries of a `method: knw_sv` pair; everything else is as for
`KnwSv`, including `period` equal to `engine.frequency`. The four Treasury tickers (`^IRX`, `^FVX`, `^TNX`,
`^TYX`) are added to the run automatically.

The keys and their defaults are listed on the reference page
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/reference/configuration-classes).

**References:**

- Duffie, D., Kan, R. (1996). "A Yield-Factor Model of Interest Rates." Mathematical Finance, 6(4), 379-406. <https://doi.org/10.1111/j.1467-9965.1996.tb00123.x>
- Cheng, P.-K., Planchet, F. (2019). "Stochastic Deflator for an Economic Scenario Generator with Five Factors." Bankers, Markets & Investors, 157. <https://www.journaleska.com/index.php/bmi/article/view/9378>
- Commissie Parameters (2022). "Technical Appendix: Specification of the CP2022 Model." <https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
KnwSvQ(toolkit: Toolkit)
```

</details>

#### KnwSvQ.calibrate_mpr

Fit the market price of risk of a calibrated knw_sv pair to the observed Treasury yield curve, and store the
matching risk-neutral (Q-measure) parameters for `q_params`, `zero_coupon_yield` and `deflator`.

This finds the five risk premiums that make the model's yields line up with the 13-week, 5-, 10- and 30-year
Treasury yields on every historical date. Under Q, the turbulence factor `v` mean reverts at its real-world
speed plus `risk_premium_v`, and each leg's expected next value drops by its `..._constant` premium plus its
`..._variance` premium times `v`.

The fit minimizes the squared gap between model and observed yields over all four tenors, with the completely
affine form of [Duffie and Kan (1996)](https://doi.org/10.1111/j.1467-9965.1996.tb00123.x). The model yields
include the convexity from the correlation between rate and inflation shocks, the one the scenarios simulate
with. Every date and tenor weighs the same, and the observed yields, those of coupon-paying Treasuries, stand
in for zero-coupon yields: both are judgements, the second close when coupons sit near the yield. The
inflation premiums are only weakly pinned down by a nominal-only curve. When `|risk_premium_v|`
exceeds 5% of `v`'s real-world speed, a warning says `deflator` is materially biased at long maturities.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.models.knw_sv.knw_sv_controller import KnwSv
from financescenarios.models.knw_sv_q.knw_sv_q_controller import KnwSvQ

toolkit = Toolkit(
    ["^IRX", "^FVX", "^TNX", "^TYX"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1990-01-01"
)
knw_sv = KnwSv(toolkit)
knw_sv.calibrate_triple("interest_rate", "inflation", period="quarterly")

knw_sv_q = KnwSvQ(toolkit)
knw_sv_q.calibrate_mpr(knw_sv, "interest_rate", "inflation", period="quarterly")
```

Which returns (calibrated on 2026-10-14):

| risk_premium_v | rate_constant | rate_variance | inflation_constant | inflation_variance |
|---------------:|--------------:|--------------:|-------------------:|-------------------:|
| -0.1536 | 0.0001 | -8.4981 | -0.0027 | 9.3876 |

Under Q, `v` reverts at 0.399 - 0.154 = 0.245 a year toward 1.6 times its historical normal level: the curve
prices in more turbulence than history shows, and the deflator warning fires.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_mpr(
    knw_sv: KnwSv,
    interest_rate_name: str,
    inflation_name: str,
    period: str,
    shock_correlation: float | None = None,
) -> CompletelyAffineMprParams
```

**Args:**

- <u>knw_sv (KnwSv):</u> a `KnwSv` instance with this pair already calibrated.
- <u>interest_rate_name (str):</u> the pair's rate leg name, as passed to `knw_sv.calibrate_triple`.
- <u>inflation_name (str):</u> the pair's inflation leg name, as passed to `knw_sv.calibrate_triple`.
- <u>period (str):</u> the frequency `knw_sv.calibrate_triple` used: "monthly" or "quarterly" ("yearly" raises, as the 13-week tenor is not a whole number of years).
- <u>shock_correlation (float &#124; None):</u> the correlation of the rate and inflation shocks. Defaults to None, the correlation of the two legs' historical period changes, the input of the scenarios' correlation matrix.

**Returns:**

<u>CompletelyAffineMprParams:</u> the five `risk_premium_*` fields.

**Raises:**

- <u>ValueError:</u> if `period` is not supported, a tenor is not a whole number of periods, fewer than 10 dates overlap, or the correlation is not strictly between -1 and 1.
- <u>RuntimeError:</u> if `knw_sv.calibrate_triple` has not been run for this pair.

</details>

#### KnwSvQ.shock_correlation

The correlation of one pair's rate and inflation shocks that its bond prices and deflator use.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
shock_correlation(interest_rate_name: str) -> float
```

**Args:**

- <u>interest_rate_name (str):</u> the pair's rate leg name, as passed to `calibrate_mpr`.

**Raises:**

- <u>RuntimeError:</u> if calibrate_mpr(...) naming this pair hasn't been called yet.

</details>

#### KnwSvQ.mpr

The calibrated market price of risk of one pair.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
mpr(interest_rate_name: str) -> CompletelyAffineMprParams
```

**Args:**

- <u>interest_rate_name (str):</u> the pair's rate leg name, as passed to `calibrate_mpr`.

**Raises:**

- <u>RuntimeError:</u> if calibrate_mpr(...) naming this pair hasn't been called yet.

</details>

#### KnwSvQ.q_params

The risk-neutral (Q-measure) parameters of one pair's `v`, rate and inflation, computed with its market price
of risk. They have the same shapes as the real-world ones from `KnwSv.calibrate_triple` and replace them when
a config sets `measure: risk_neutral`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
q_params(interest_rate_name: str) -> tuple[OUParams, KnwSvLegParams, KnwSvLegParams]
```

**Args:**

- <u>interest_rate_name (str):</u> the pair's rate leg name, as passed to `calibrate_mpr`.

**Returns:**

<u>tuple[OUParams, KnwSvLegParams, KnwSvLegParams]:</u> (v_q, interest_rate_q, inflation_q).

**Raises:**

- <u>RuntimeError:</u> if calibrate_mpr(...) naming this pair hasn't been called yet.

</details>

#### KnwSvQ.zero_coupon_yield

The model's zero-coupon yield at `tenor` years, read off the fitted risk-neutral model at the pair's current
state (the last observed rate, inflation and `v`).

This gives today's yield curve at any maturity that is a whole number of periods, including maturities the
Treasury panel does not quote. A value of 0.04 at `tenor=10` means a 10-year zero-coupon bond is priced at
exp(-0.04 * 10) = 0.67 per unit of face value. The one-period yield equals today's short rate.

The price comes from the discrete-time affine recursion `exp(A[n] + Bv[n]*v + Br[n]*r + Bpi[n]*pi)` with `n =
tenor / period length`, after [Duffie and Kan (1996)](https://doi.org/10.1111/j.1467-9965.1996.tb00123.x), and the
yield, continuously compounded, is `-log(price) / tenor`. The convexity includes the correlation of rate and
inflation shocks, so the price matches the average discount factor along paths simulated under Q.

**As an example:**

Continuing from `calibrate_mpr`.

```python
for tenor in [0.25, 1, 2, 5, 10, 20, 30]:
    print(tenor, knw_sv_q.zero_coupon_yield("interest_rate", tenor))
```

Which returns (calibrated on 2026-10-14):

| tenor (years) | 0.25 | 1 | 2 | 5 | 10 | 20 | 30 |
|:--------------|-----:|--:|--:|--:|---:|---:|---:|
| yield | 0.0375 | 0.0387 | 0.0405 | 0.0447 | 0.0478 | 0.0484 | 0.0483 |

The curve starts at the 3.75% short rate of the last quarter, rises to 4.5% at five years and flattens near
4.8% beyond ten, below the latest observed Treasury yields, since the premiums are fit across the whole
history.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
zero_coupon_yield(interest_rate_name: str, tenor: float) -> float
```

**Args:**

- <u>interest_rate_name (str):</u> the pair's rate leg name, as passed to `calibrate_mpr`.
- <u>tenor (float):</u> the maturity in years, a whole number of periods (0.25, 0.5, ... for a quarterly pair).

**Returns:**

<u>float:</u> the model zero-coupon yield at `tenor`, as a decimal.

**Raises:**

- <u>RuntimeError:</u> if `calibrate_mpr` has not been run for this pair.
- <u>ValueError:</u> if `tenor` is not a whole number of periods.

</details>

#### KnwSvQ.deflator

Build a stochastic deflator, after
[Cheng and Planchet (2019)](https://www.journaleska.com/index.php/bmi/article/view/9378), from a real-world
simulated knw_sv run and this pair's fitted market price of risk.

Multiply a simulated cash flow at time `T` by `D(T)` on the same path and average across paths, and you get
its market value today, without a separate risk-neutral simulation. `D(T)` combines discounting at the
simulated short rate with a per-path weight that makes paths the market fears more count for more.

Each step recovers the rate's and inflation's realized shock `z` from the path and weights it by
`exp(-theta*z - 0.5*theta^2)`, where `theta` is the gap between the real-world and risk-neutral expected value
divided by the volatility, with the correlation of the two shocks taken into account. `v`'s own shock is not
reweighted, so the deflator is accurate only when `risk_premium_v` is small relative to `v`'s mean-reversion
speed, or at short maturities; `calibrate_mpr` warns past 5% of that speed. A scenario set does not include
`v`, so you simulate and record it yourself.

**As an example:**

Continuing from `calibrate_mpr`, with `v_path`, `rate_path` and `inflation_path` simulated by hand over 20
quarters and 20,000 paths (seed 42, the rate and inflation shocks correlated at `shock_correlation`, 0.14).

```python
rate, inflation = knw_sv.params("interest_rate"), knw_sv.params("inflation")
deflator = knw_sv_q.deflator("interest_rate", v_path, rate_path, inflation_path, rate, inflation)
```

Which returns (calibrated on 2026-10-14):

| T (years) | mean of D(T) | closed-form Q bond price |
|----------:|-------------:|-------------------------:|
| 1 | 0.9827 | 0.9620 |
| 5 | 0.7606 | 0.7996 |

Here `|risk_premium_v|` is 38.5% of `v`'s speed, so the average misses the bond price, by 2% at one year and 5%
at five: the regime `calibrate_mpr` warns about.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
deflator(
    interest_rate_name: str,
    v_path: np.ndarray,
    interest_rate_path: np.ndarray,
    inflation_path: np.ndarray,
    interest_rate_params: KnwSvLegParams,
    inflation_params: KnwSvLegParams,
) -> np.ndarray
```

**Args:**

- <u>interest_rate_name (str):</u> the pair's rate leg name, as passed to `calibrate_mpr`.
- <u>v_path (np.ndarray):</u> the simulated `v`, one row per scenario and one column per date, the start included.
- <u>interest_rate_path (np.ndarray):</u> the simulated short rate on the same scenarios and dates.
- <u>inflation_path (np.ndarray):</u> the simulated inflation on the same scenarios and dates.
- <u>interest_rate_params (KnwSvLegParams):</u> the real-world rate parameters the paths were simulated with.
- <u>inflation_params (KnwSvLegParams):</u> the real-world inflation parameters, likewise.

**Returns:**

<u>np.ndarray:</u> `D(t)` per scenario and date, equal to 1 at the start of every path.

**Raises:**

- <u>RuntimeError:</u> if `calibrate_mpr` has not been run for this pair.
- <u>ValueError:</u> if a leg's volatility is exactly zero at some step.

</details>

### How It Is Calculated

The model functions behind this page, each with the formula it implements.

{% raw %}
#### fit_cir_process

Fit the Cox-Ingersoll-Ross (CIR) short-rate model to a rate history: the same pull toward a long-run level as
Hull-White, but with swings that scale with the square root of the rate itself.

That scaling is the point of CIR: when rates are high they move a lot, and as they approach zero the moves
shrink, so simulated rates stay near or above zero. It suits a view that deeply negative rates are not a
plausible scenario for the liabilities in question; the price is a weaker fit in a zero-rate era, when CIR sees
almost no volatility. The speed and long-run level are fitted as in Hull-White, and the volatility from the
period-by-period surprises divided by the square root of the rate.

The formula is as follows:

$$
\text{dr} = a \cdot (\theta - r) \cdot \text{dt} + \sigma \cdot \sqrt{r} \cdot \text{dW}
$$

$$
\sigma = \operatorname{std}(e_{t} / \sqrt{r_{t-1}}) / \sqrt{\text{dt}},\;\; \text{over} \;\; r_{t-1} \geq \text{minimum\_level}
$$

$$
2 \cdot a \cdot \theta \geq \sigma ^{2} (\text{Feller condition})
$$

Where e_t is the unexpected part of each change, given the pull toward theta. Negative observations (the US
bill rate printed some in 2015 and 2020) are set to zero, since CIR has no room for them. Days with almost zero
rates are left out of the volatility estimate, because dividing by a near-zero sqrt(r) would inflate it many
times over. When the Feller condition fails, the fit still holds but simulated rates touch zero more often than
the theoretical model would.

**References:**

- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). "A Theory of the Term Structure of Interest Rates." Econometrica, 53(2), 385-407. <https://doi.org/10.2307/1911242>
- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. <https://doi.org/10.1016/0304-405x(77>)90016-2
- Chan, K.C., Karolyi, G.A., Longstaff, F.A., Sanders, A.B. (1992). "An Empirical Comparison of Alternative Models of the Short-Term Interest Rate." Journal of Finance, 47(3), 1209-1227. Section II, eqs. (2)-(3), the discrete-time fit used for sigma, r_t+1 - r_t = alpha + beta r_t + e_t+1 with E[e^2_t+1] = sigma^2 r_t^(2 gamma), and gamma = 1/2 for CIR. <https://doi.org/10.1111/j.1540-6261.1992.tb04011.x>
- Ahlgrim, K.C. "Hull-White Term Structure Model." CAS Exam 8 Online Course, Module 4. <https://www.casact.org/sites/default/files/old/oncourses_module4_ahlgrim.pdf>
- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2008). "A Comparison of Actuarial Financial Scenario Generators." Casualty Actuarial Society. <https://www.casact.org/sites/default/files/document/darcy_1.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_cir_process(
    short_rate: pl.Series,
    time_step: float,
    minimum_level: float = _MINIMUM_LEVEL_FOR_CIR_VOLATILITY,
) -> OUParams
```

**Args:**

- <u>short_rate (pl.Series):</u> the short-rate history as decimals, evenly spaced.
- <u>time_step (float):</u> the time between observations, in years (1/12 for monthly).
- <u>minimum_level (float):</u> rates below this are left out of the volatility estimate, default 10bp; a series on another scale, such as a variance, needs a cutoff on its own scale.

**Returns:**

<u>OUParams:</u> the mean-reversion speed, long-run level, volatility and today's rate.

**Raises:**

- <u>ValueError:</u> if too few observations remain above `minimum_level`.

</details>
{% endraw %}

#### step_hull_white

Move a Hull-White short rate forward one step: part of the gap to the long-run level closes, and a normally
distributed shock is added.

Each step the rate keeps a share exp(-a * dt) of its gap to theta, so after a shock the rate drifts back at a
steady pace, while the shock's size grows with the step but levels off for long steps, because mean reversion
caps how far the rate can wander. The long-run spread of rates around theta is sigma / sqrt(2 * a): a fast pull
keeps rates in a narrow band. The step is the exact one for this model, so a yearly simulation gives the same
distribution as a daily one.

The formula is as follows:

$$
r(t + \text{dt}) = \theta + (r(t) - \theta) \cdot \exp(- a \cdot \text{dt}) + \sigma \cdot \sqrt{(1 - \exp(- 2 \cdot a \cdot \text{dt})) / (2 \cdot a)} \cdot z
$$

Where a is the mean-reversion speed, theta the long-run level, sigma the volatility and z a standard normal draw.
Nothing stops the rate from going below zero, which is how Hull-White allows for negative rates.

**References:**

- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. Section 5, p. 185: dr = α(γ−r)dt+ρdz, eq. (24), with the exact transition E_t r(s) = γ+(r(t)−γ)e^{−α(s−t)}, eq. (25), and Var_t r(s) = ρ²/(2α)(1−e^{−2α(s−t)}), eq. (26). <https://doi.org/10.1016/0304-405x(77>)90016-2
- Hull, J., White, A. (1990). "Pricing Interest-Rate-Derivative Securities." The Review of Financial Studies, 3(4), 573-592. Section 2, eq. (3): their extension of Vasicek's model is eq. (2) with β = 0; with constant a and σ it is the Hull-White model. <https://doi.org/10.1093/rfs/3.4.573>
- Ahlgrim, K.C. "Hull-White Term Structure Model." CAS Exam 8 Online Course, Module 4. <https://www.casact.org/sites/default/files/old/oncourses_module4_ahlgrim.pdf>
- Society of Actuaries & Casualty Actuarial Society (2002). "Report on Modeling of Economic Series Coordinated with Interest Rate Scenarios." <https://www.soa.org/globalassets/assets/files/sections/modeling-of-economic-scenarios.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_hull_white(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: OUParams,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's short rate in each scenario.
- <u>shock (np.ndarray &#124; float):</u> the random draw for this step, standard normal.
- <u>time_step (float):</u> the step length, in years.
- <u>params (OUParams):</u> the calibrated speed, long-run level and volatility.

**Returns:**

<u>np.ndarray:</u> the short rate one step later; it may be negative.

</details>

{% raw %}
#### step_cir

Move a CIR short rate forward one step: the same pull toward the long-run level as Hull-White, with a shock
that shrinks as the rate approaches zero.

Because the shock scales with sqrt(r), a rate of 1% moves about a third as much as one of 9%, so low-rate
scenarios are calm and high-rate scenarios volatile, as in the 1970s and 1980s. The step is the full-truncation
scheme of Lord, Koekkoek and van Dijk (2010), the most accurate of their simple schemes.

The formula is as follows:

$$
r(t + \text{dt}) = r(t) + a \cdot (\theta - r +) \cdot \text{dt} + \sigma \cdot \sqrt{r + \cdot \text{dt}} \cdot z
$$

$$
r + = \max(r(t),\; 0)
$$

Only the pull and the shock size use r+; the rate itself is not floored, so it is not stuck at zero once it gets
there. As an approximation to the exact CIR distribution, a path can dip slightly below zero with coarse steps;
monthly or finer steps keep this rare.

**References:**

- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). "A Theory of the Term Structure of Interest Rates." Econometrica, 53(2), 385-407. <https://doi.org/10.2307/1911242>
- Lord, R., Koekkoek, R., van Dijk, D. (2010). "A Comparison of Biased Simulation Schemes for Stochastic Volatility Models." Quantitative Finance, 10(2), 177-194. Section 5: full truncation beats every other biased scheme they test on bias and root-mean-squared error. <https://doi.org/10.1080/14697680802392496>
- Andersen, L. (2008). "Simple and Efficient Simulation of the Heston Stochastic Volatility Model." Journal of Computational Finance, 11(3), 1-42. Its Quadratic-Exponential scheme is a lower-bias alternative for a CIR process, not implemented here. <https://doi.org/10.21314/JCF.2008.189>
- Ahlgrim, K.C. "Hull-White Term Structure Model." CAS Exam 8 Online Course, Module 4. <https://www.casact.org/sites/default/files/old/oncourses_module4_ahlgrim.pdf>
- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2008). "A Comparison of Actuarial Financial Scenario Generators." Casualty Actuarial Society. <https://www.casact.org/sites/default/files/document/darcy_1.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_cir(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: OUParams,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's short rate in each scenario (may be slightly negative).
- <u>shock (np.ndarray &#124; float):</u> the random draw for this step, standard normal.
- <u>time_step (float):</u> the step length, in years.
- <u>params (OUParams):</u> the calibrated speed, long-run level and volatility.

**Returns:**

<u>np.ndarray:</u> the short rate one step later; it can dip slightly below zero.

</details>
{% endraw %}

#### hull_white_yield_volatility

How much a Hull-White model moves the zero-coupon yield of a given maturity, per year: the short rate's volatility
damped by mean reversion, since a shock to the short rate is expected to fade before a long bond matures.

The formula is as follows:

$$
\operatorname{vol}(T) = \sigma \cdot (1 - \exp(- a \cdot T)) / (a \cdot T)
$$

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
hull_white_yield_volatility(
    maturity: float | np.ndarray,
    mean_reversion_speed: float,
    volatility: float,
)
```

**Args:**

- <u>maturity (float &#124; np.ndarray):</u> the yield's maturity in years.
- <u>mean_reversion_speed (float):</u> a.
- <u>volatility (float):</u> sigma, the short rate's yearly volatility.

**Returns:**

<u>float &#124; np.ndarray:</u> the yearly volatility of the T-year yield, in the same units as sigma.

</details>

#### curve_forward_rates

The continuously compounded forward rates a published spot curve implies between its maturities, the
constant-forward interpolation EIOPA itself uses (EIOPA (2026, section 3.7.1), which
holds the forward rate constant between known DLT points).

The formula is as follows:

$$
z(T) = \ln(1 + s(T))
$$

$$
f(T_{i}) = (T_{i} \cdot z(T_{i}) - \text{T\_i-1} \cdot z(\text{T\_i-1})) / (T_{i} - \text{T\_i-1}),\;\; \text{with}\; T_{0} = 0
$$

Where s(T) is the annually compounded spot rate at maturity T and f(T_i) the forward rate between T_i-1 and T_i.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
curve_forward_rates(maturities: np.ndarray, spot_rates: np.ndarray) -> np.ndarray
```

**Args:**

- <u>maturities (np.ndarray):</u> the curve's maturities in years, positive and ascending.
- <u>spot_rates (np.ndarray):</u> annually compounded spot rates, one per maturity.

**Returns:**

<u>np.ndarray:</u> one continuously compounded forward rate per maturity.

**Raises:**

- <u>ValueError:</u> if the inputs are empty, unequal in length or the maturities are not positive and ascending.

</details>

#### hull_white_alpha

The path a risk-neutral Hull-White short rate is centred on, chosen so the scenarios reprice today's yield curve
exactly.

The short rate is split into a random, mean-reverting part x(t) that starts at zero and a fixed path alpha(t), as
in Brigo and Mercurio (2006, section 3.3). alpha(t) is today's instantaneous forward rate f^M(0, t), read off the
Nelson-Siegel fit to today's Treasury curve or off a supplied curve such as EIOPA's, plus a small convexity term.
That term is needed because discounting is convex in rates: random rates raise the average discount factor, so
the centre is lifted slightly to keep zero-coupon bond prices where the market has them. The adjustment grows
with volatility and maturity and is small for typical parameters (a few basis points).

The formula is as follows:

$$
r(t) = x(t) + \alpha(t),\;\; \text{with dx} = - a \cdot x \cdot \text{dt} + \sigma \cdot \text{dW and}\; x (0) = 0
$$

$$
\alpha(t) = f ^{M} (0,\; t) + \sigma ^{2} / (2 \cdot a ^{2}) \cdot (1 - \exp(- a \cdot t)) ^{2}
$$

$$
\theta(t) = \text{df} ^{M} (0,\; t) / \text{dt} + a \cdot f ^{M} (0,\; t) + \sigma ^{2} / (2 \cdot a) \cdot (1 - \exp(- 2 \cdot a \cdot t))
$$

The last line is the same model in Hull and White's (1990) form, dr = (theta(t) - a * r) * dt + sigma * dW.

**References:**

- Brigo, D., Mercurio, F. (2006). "Interest Rate Models: Theory and Practice" (2nd ed.), section 3.3. Springer Finance. <https://doi.org/10.1007/978-3-540-34604-3>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
hull_white_alpha(
    elapsed_time: float | np.ndarray,
    params: HullWhiteForwardParams,
) -> float | np.ndarray
```

**Args:**

- <u>elapsed_time (float &#124; np.ndarray):</u> years since the valuation date.
- <u>params (HullWhiteForwardParams):</u> the calibrated speed, volatility and today's curve.

**Returns:**

<u>float &#124; np.ndarray:</u> alpha(t), one value per time given.

</details>

#### step_hull_white_forward

Move a risk-neutral Hull-White short rate forward one step, reverting toward today's forward curve rather than to
a fixed long-run level.

The rate's distance from the curve-implied path alpha(t) (see `hull_white_alpha`) decays at the calibrated speed
and receives a normal shock, exactly as in `step_hull_white`. Because the centre moves along today's curve, an
upward-sloping curve lifts the simulated rates over time and an inverted one lowers them, and the average
discount factor across scenarios matches today's bond prices. Rates can go negative.

The formula is as follows:

$$
r(t + \text{dt}) = \alpha(t + \text{dt}) + (r(t) - \alpha(t)) \cdot \exp(- a \cdot \text{dt}) + \sigma \cdot \sqrt{(1 - \exp(- 2 \cdot a \cdot \text{dt})) / (2 \cdot a)} \cdot z
$$

**References:**

- Brigo, D., Mercurio, F. (2006). "Interest Rate Models: Theory and Practice" (2nd ed.), section 3.3. Springer Finance. <https://doi.org/10.1007/978-3-540-34604-3>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_hull_white_forward(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    elapsed_time: float,
    params: HullWhiteForwardParams,
) -> np.ndarray
```

**Args:**

- <u>current_value (float &#124; np.ndarray):</u> today's short rate in each scenario.
- <u>shock (float &#124; np.ndarray):</u> the random draw for this step, standard normal.
- <u>time_step (float):</u> the step length, in years.
- <u>elapsed_time (float):</u> years since the valuation date at the start of this step.
- <u>params (HullWhiteForwardParams):</u> the calibrated speed, volatility and today's Nelson-Siegel curve.

**Returns:**

<u>float &#124; np.ndarray:</u> the short rate one step later.

</details>

#### inflation_expectation

Wilkie's (1986) expected inflation: an exponentially weighted average of past inflation (eq. 3.12-3.13), the
inflation the bond market is assumed to build into long yields.

Investors are taken to form expectations adaptively, giving recent inflation more weight but remembering the
past: with Wilkie's CD of 0.05 a year, a burst of inflation raises expected inflation, and with it long yields,
only gradually, and the effect fades over roughly 20 years. That slow adjustment is why a Wilkie long yield
lags an inflation shock rather than jumping with it.

The formula is as follows:

$$
\operatorname{CM}(t) = \text{CD} \cdot I(t) + (1 - \text{CD}) \cdot \operatorname{CM}(t-1)
$$

Where I(t) is the force of inflation and CD the `decay`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
inflation_expectation(inflation: np.ndarray, decay: float, start: float | None = None) -> np.ndarray
```

**Args:**

- <u>inflation (np.ndarray):</u> inflation per period, oldest first.
- <u>decay (float):</u> CD, the weight of the latest observation, between 0 and 1.
- <u>start (float &#124; None):</u> expected inflation before the first observation, default None (the first observation).

**Returns:**

<u>np.ndarray:</u> expected inflation CM(t) for every period.

</details>

{% raw %}
#### fit_wilkie_consols_process

Fit Wilkie's (1986) long-term (Consols) yield model, in which a long yield is expected inflation plus a real
yield, to a history of long yields and inflation.

This is how inflation feeds yields in the classic actuarial model: the nominal long yield C(t) is CW times
expected inflation CM(t), a slow moving average of past inflation, plus a real yield CN(t). The real part is
lognormal and mean-reverting, so it stays positive and its swings are proportional to its level. In the
scenarios, a sustained rise in inflation lifts long yields gradually and permanently, while a brief spike barely
moves them. The fit backs CN(t) out of the data and fits its persistence CA1, long-run level CMU and volatility
CSD; CW and CD stay at Wilkie's published values (his Reduced Basis).

The formula is as follows:

$$
\operatorname{CM}(t) = \text{CD\_dt} \cdot \operatorname{dlnQ}(t) + (1 - \text{CD\_dt}) \cdot \operatorname{CM}(t-1),\;\; \text{started at CM} (0) = \operatorname{dlnQ}(0)
$$

$$
\text{CD\_dt} = 1 - (1 - \text{CD}) ^{\text{dt}}
$$

$$
\operatorname{CN}(t) = C(t) - \text{CW} \cdot \operatorname{CM}(t)
$$

$$
\text{ln CN} (t) = \text{ln CMU} + \text{CA1} \cdot (\text{ln CN} (t-1) - \text{ln CMU}) + \text{CSD} \cdot \operatorname{CZ}(t)
$$

CD_dt makes 1/dt steps decay as much as one year at Wilkie's yearly CD (his model steps a year, since an actuary is
usually content to project in annual steps, section 1.3). Starting CM at the first observation is a judgement:
Wilkie's neutral value for CM is QMU (section 4.5), which is not known before inflation is fitted.

**References:**

- Wilkie, A.D. (1986). "A stochastic investment model for actuarial use." Transactions of the Faculty of Actuaries, 39, 341-403. Section 3.12-3.15, the Consols yield model and its Reduced Basis parameterisation. <https://doi.org/10.1017/S0071368600009009>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_wilkie_consols_process(
    consols_yield: pl.Series,
    inflation: pl.Series,
    inflation_weight: float = 1.0,
    inflation_decay: float = 0.05,
    time_step: float = 1.0,
) -> WilkieConsolsParams
```

**Args:**

- <u>consols_yield (pl.Series):</u> the long-term government yield history as decimals (0.04 is 4%), evenly spaced.
- <u>inflation (pl.Series):</u> the inflation history over the same dates (Wilkie's dlnQ(t)).
- <u>inflation_weight (float):</u> CW, how much of expected inflation passes into the yield, default 1.0 (Wilkie, section 3.15, CW = 1.0).
- <u>inflation_decay (float):</u> CD, the yearly weight of new inflation in expected inflation, default 0.05 (Wilkie, section 3.15, Reduced Standard Basis, CD = 0.05; his full basis has 0.045).
- <u>time_step (float):</u> the time between observations in years, default 1.0; 1/12 for monthly data keeps Wilkie's roughly 20-year memory.

**Returns:**

<u>WilkieConsolsParams:</u> CW, CD, the real yield's CMU, CA1 and CSD, and today's long yield.

**Raises:**

- <u>ValueError:</u> if the two histories differ in length, or the long yield falls to or below expected inflation anywhere in the window (a negative real yield, which the model cannot hold; on US data, end the window before 2008).

</details>
{% endraw %}

#### forward_rate_path

The forward rates a spot curve implies: the rate it locks in today for borrowing over `tenor` years starting at
each future date.

This turns an official curve such as EIOPA's into a path for the long-run level a simulated rate is pulled toward
(`long_run_anchor`), so scenarios settle where the curve says rates will be, ending at its ultimate forward rate,
rather than at a historical average. Between published maturities the forward rate is held flat (log-linear
discount factors), and beyond the last maturity it stays at the last forward rate.

The formula is as follows:

$$
\text{ln}\; P (T) = - T \cdot \ln(1 + s(T))
$$

$$
F(t,\; m) = \exp((\text{ln}\; P (t) - \text{ln}\; P (t + m)) / m) - 1
$$

Where s(T) is the spot rate at maturity T, P(T) the discount factor and m the `tenor`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
forward_rate_path(
    maturities: np.ndarray,
    spot_rates: np.ndarray,
    tenor: float,
    years: np.ndarray,
) -> np.ndarray
```

**Args:**

- <u>maturities (np.ndarray):</u> the curve's maturities in years, ascending, all positive.
- <u>spot_rates (np.ndarray):</u> annually compounded spot rates, one per maturity.
- <u>tenor (float):</u> the forward rate's own length in years, e.g. 1 for a short rate, 10 for a long rate.
- <u>years (np.ndarray):</u> the start dates in years from today.

**Returns:**

<u>np.ndarray:</u> the annually compounded forward rates, one per start date.

**Raises:**

- <u>ValueError:</u> if the inputs are empty, unequal in length, not ascending or `tenor` is not positive.

</details>

#### fit_policy_rule_weights

Fit a monetary-policy rule on a short rate's own history: how far the rate has moved with inflation and with
unemployment, and how gradually, so the rule describes what this central bank did rather than the weights the
Federal Reserve publishes.

Clarida, Galí and Gertler (2000, section II, eqs. (1)-(4)) estimate the rule as a target rate that moves with
inflation and slack, which the actual rate closes only part of each period. For the Federal Reserve they found an
inflation response of 0.83 before 1979 and 2.15 under Volcker and Greenspan, keeping 0.79 of last quarter's rate
(Table II); for the Bundesbank (1979-1993) 1.31 and for the Bank of England (1979-1990) 0.98, keeping 0.91 and 0.92
of last month's rate (Clarida, Galí and Gertler (1998, Tables 1 and 4)). Here the rule reads inflation over the
past year and the unemployment rate at the start of each period, as the simulation's rule does, so it is ordinary
least squares on those lagged data rather than their GMM on expected inflation. The standard errors allow for a
year of autocorrelated errors, as theirs did, with the Bartlett weights of Newey and West (1987).

Steps that start with the rate within 25 basis points of its floor (or of zero, if higher) are left out: the rate
could not follow a rule that called for less. The standard errors then pair only steps that are the given number
of months apart, so the sample falls into contiguous blocks rather than joining the months either side of a
spell at the floor. The fit is sound when rho lies between 0 and 1 and both responses
are at least 1.96 standard errors from zero, up for inflation and down for unemployment. A response to inflation
below 1 is kept: real rates then fall as inflation rises, against the Taylor principle, as they did under the
Federal Reserve's rule before 1979. A sample with little variation in inflation can leave the response
unidentified (Clarida, Galí and Gertler (2000, section II.C)), which the flag catches.

The formula is as follows:

$$
r(t + 1) = k + \rho \cdot r(t) + b_{1} \cdot (\pi(t) - \text{pi\_target}) + b_{2} \cdot (u(t) - u_{LR}) + e(t + 1)
$$

$$
c = k / (1 - \rho),\;\; \beta = b_{1} / (1 - \rho),\;\; \gamma = b_{2} / (1 - \rho)
$$

**As an example:**

```python
import numpy as np

from financescenarios.factors.interest_rates.interest_rates_model import fit_policy_rule_weights

rng = np.random.default_rng(7)
inflation, unemployment, rate = np.full(480, 0.025), np.full(480, 0.055), np.full(480, 0.035)
for month in range(1, 480):
    inflation[month] = 0.025 + 0.97 * (inflation[month - 1] - 0.025) + rng.normal(0, 0.003)
    unemployment[month] = 0.055 + 0.98 * (unemployment[month - 1] - 0.055) + rng.normal(0, 0.002)
    target = 0.032 + 1.8 * (inflation[month - 1] - 0.02) - 1.5 * (unemployment[month - 1] - 0.055)
    rate[month] = 0.95 * rate[month - 1] + 0.05 * target + rng.normal(0, 0.001)

fit_policy_rule_weights(rate, inflation, unemployment, 1 / 12, 0.02, 0.055)
```

Which returns:

| Field | Estimate | Standard error |
|:------|---------:|---------------:|
| steady_state_rate | 0.0282 | 0.0014 |
| inflation_response | 1.9428 | 0.0962 |
| unemployment_response | -1.7475 | 0.1635 |
| smoothing | 0.9525 | 0.0037 |

Forty years of a rate generated by a rule with weights 1.8 and -1.5, keeping 0.95 of last month's rate, give
back both weights within 0.25 and the smoothing within 0.003, so the fit is sound.

**References:**

- Clarida, R., Galí, J., Gertler, M. (2000). "Monetary Policy Rules and Macroeconomic Stability: Evidence and Some Theory." The Quarterly Journal of Economics, 115(1), 147-180. Section II, eqs. (1)-(4), Table II. <https://doi.org/10.1162/003355300554692>
- Clarida, R., Galí, J., Gertler, M. (1998). "Monetary Policy Rules in Practice: Some International Evidence." European Economic Review, 42(6), 1033-1067. <https://doi.org/10.1016/S0014-2921(98>)00016-6; Tables 1 and 4 of the working-paper version, <https://www.nber.org/papers/w6254>
- Newey, W.K., West, K.D. (1987). "A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix." Econometrica, 55(3), 703-708. <https://doi.org/10.2307/1913610>; eq. (5) of the working-paper version, <https://www.nber.org/papers/t0055>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_policy_rule_weights(
    rate: np.ndarray,
    inflation: np.ndarray,
    unemployment: np.ndarray,
    time_step: float,
    inflation_target: float,
    longer_run_unemployment: float,
    effective_lower_bound: float = 0.0,
) -> PolicyRuleFit
```

**Args:**

- <u>rate (np.ndarray):</u> the observed short rate, as decimals, evenly spaced.
- <u>inflation (np.ndarray):</u> inflation over the past year on the same dates.
- <u>unemployment (np.ndarray):</u> the unemployment rate on the same dates.
- <u>time_step (float):</u> the time between observations, in years.
- <u>inflation_target (float):</u> the target the inflation gap is measured from.
- <u>longer_run_unemployment (float):</u> the level the unemployment gap is measured from.
- <u>effective_lower_bound (float):</u> the floor under the rate, default 0.

**Returns:**

<u>PolicyRuleFit:</u> the estimates, their standard errors, the implied neutral real rate and whether the fit is sound.

**Raises:**

- <u>ValueError:</u> if the series differ in length.

</details>

#### policy_rule_rate

The short rate a monetary-policy rule prescribes for a given inflation and unemployment rate: the neutral real
rate plus inflation, raised for inflation above target and lowered for unemployment above its longer-run level.

Taylor (1993, p. 202, eq. 1) showed that a rule of this shape tracked the federal funds rate from 1987 to 1992, and
the Federal Reserve reports it and the balanced-approach rule in every Monetary Policy Report, both with a weight
of 0.5 on the inflation gap and 1 or 2 on the unemployment gap (Board of Governors of the Federal Reserve System
(2026, Box 4, Table A)). Because the weight on inflation is above one in total, a rise in inflation lifts the
nominal rate by more than the rise itself, so the real rate goes up: inflation 3 points above target adds 4.5
points. With inflation on target and unemployment at its longer-run level the rule gives the neutral real rate
plus the target. In a deep recession the prescription goes below the effective lower bound; the simulated rate
stays at the bound while its shadow rate follows the prescription (see `step_policy_rule_rate`).

The formula is as follows:

$$
R \cdot = r_{LR} + \pi + a \cdot (\pi - \text{pi\_target}) - b \cdot (u - u_{LR})
$$

**References:**

- Taylor, J.B. (1993). "Discretion versus Policy Rules in Practice." Carnegie-Rochester Conference Series on Public Policy, 39, 195-214. p. 202, eq. (1). <https://doi.org/10.1016/0167-2231(93>)90009-L
- Board of Governors of the Federal Reserve System (2026). "Monetary Policy Report, July 2026." Box 4, Table A and note 3. <https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-part2.htm>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
policy_rule_rate(
    inflation: np.ndarray | float,
    unemployment: np.ndarray | float,
    params: PolicyRuleParams,
) -> np.ndarray
```

**Args:**

- <u>inflation (np.ndarray &#124; float):</u> inflation over the past year, as a decimal.
- <u>unemployment (np.ndarray &#124; float):</u> the unemployment rate, as a decimal.
- <u>params (PolicyRuleParams):</u> the rule's neutral rate, target, weights and longer-run unemployment.

**Returns:**

<u>np.ndarray:</u> the prescribed rate, as a decimal; it may be below `params.effective_lower_bound`.

</details>

#### fit_policy_rule_process

Fit how much a short rate has moved around a monetary-policy rule, and optionally how fast it has followed it and
how strongly it has responded to inflation and unemployment, from its history.

By default the rule's weights are the published ones; the neutral rate, target and longer-run unemployment are
always given. With `weights="fitted"` the weights and the speed come from the rate's own history instead, fitted
jointly (`fit_policy_rule_weights`, which needs `speed="fitted"`); when that fit is not sound the published
weights stay, with a warning, and the speed is fitted on them as below.

Central banks move in steps rather than at once, so the rate closes only part of its gap to the rule's rate each
period, the partial adjustment of Clarida, Galí and Gertler (2000). By default that speed is the Federal Reserve's
inertial rule, which keeps 0.85 of last quarter's rate and moves 0.15 of the way to the rule (Board of Governors of
the Federal Reserve System (2018, table "Examples of Policy Rules")): 0.65 a year, a gap halving in about a year.
With the published weights, fitting the speed instead regresses each period's change in the rate on its gap to the
rule's rate, with no intercept. That reads every lasting gap between the published rule and the rate as slow
adjustment: a neutral rate that drifts over the decades, or headline inflation swings a central bank looks through.
On the US bill rate from 1987 to 2012 the slope even turns negative: the Federal Reserve raised rates in 1988 and
1994 with the rule below them, and cut them through 2008 while headline inflation peaked. The speeds that do come
out on other windows, half-lives of 3 to 20 years, left the simulated rate's largest one-year rise at about a third
of history's. A fitted slope outside (0, 1) falls back to the inertial rule's speed, with a warning.

The volatility comes from what each step leaves unexplained at that speed. Steps that start with the rate held at
its floor while the rule prescribed less are left out (`held_at_lower_bound`), as the rate could not follow the
rule there; elsewhere the rate is read against the rule's own prescription, which a run's shadow rate follows
below the floor too (Black (1995)). Fitted weights leave out every step that starts at the floor, whatever the
rule prescribed (the weights are not known before the fit), and the volatility then leaves out the same steps.

The formula is as follows:

$$
r(t + 1) - r(t) = \beta \cdot (R \cdot (t) - r(t)) + e(t)
$$

$$
\beta = 1 - \exp(- \kappa \cdot \text{dt}),\;\; \kappa = - \ln(0.85) / 0.25 \;\text{for the inertial rule}
$$

$$
\sigma = \operatorname{std}(e) / \sqrt{(1 - \exp(- 2 \cdot \kappa \cdot \text{dt})) / (2 \cdot \kappa)}
$$

Where R*(t) is the rule's rate for the period's inflation and unemployment (see `policy_rule_rate`).

**References:**

- Board of Governors of the Federal Reserve System (2018). "Policy Rules and How Policymakers Use Them." Table "Examples of Policy Rules", inertial rule. <https://www.federalreserve.gov/monetarypolicy/policy-rules-and-how-policymakers-use-them.htm>
- Clarida, R., Galí, J., Gertler, M. (2000). "Monetary Policy Rules and Macroeconomic Stability: Evidence and Some Theory." The Quarterly Journal of Economics, 115(1), 147-180. <https://doi.org/10.1162/003355300554692>
- Black, F. (1995). "Interest Rates as Options." The Journal of Finance, 50(5), 1371-1376. <https://doi.org/10.1111/j.1540-6261.1995.tb05182.x>
- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. Section 5, eqs. (25)-(26). <https://doi.org/10.1016/0304-405x(77>)90016-2

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_policy_rule_process(
    rate: np.ndarray,
    inflation: np.ndarray,
    unemployment: np.ndarray,
    time_step: float,
    rule: Literal['taylor', 'balanced'],
    neutral_real_rate: float,
    inflation_target: float,
    longer_run_unemployment: float,
    effective_lower_bound: float = 0.0,
    speed: Literal['inertial', 'fitted'] = 'inertial',
    weights: Literal['published', 'fitted'] = 'published',
) -> PolicyRuleParams
```

**Args:**

- <u>rate (np.ndarray):</u> the observed short rate, as decimals, evenly spaced.
- <u>inflation (np.ndarray):</u> inflation over the past year on the same dates.
- <u>unemployment (np.ndarray):</u> the unemployment rate on the same dates.
- <u>time_step (float):</u> the time between observations, in years.
- <u>rule (str):</u> "taylor" or "balanced".
- <u>neutral_real_rate (float):</u> the neutral real rate.
- <u>inflation_target (float):</u> the inflation target.
- <u>longer_run_unemployment (float):</u> the unemployment rate at which the rule is neutral.
- <u>effective_lower_bound (float):</u> the floor under the rate, default 0.
- <u>speed (str):</u> "inertial" (default), the Federal Reserve's inertial rule's speed, or "fitted" on this history.
- <u>weights (str):</u> "published" (default), the rule's published weights, or "fitted" on this history, jointly with the speed.

**Returns:**

<u>PolicyRuleParams:</u> the speed and the fitted volatility with the rule's settings, the last rate as the starting point and how closely the rule tracked the rate.

**Raises:**

- <u>ValueError:</u> if the series differ in length, `speed` or `weights` is unknown, fitted weights come with the inertial speed or too few steps are left to fit on.

</details>

#### step_policy_rule_rate

Move a policy-rule short rate forward one step: it closes part of its gap to the rate the rule prescribes for
this scenario's inflation and unemployment at the start of the step, plus a normally distributed shock.

This is what ties rates to the economy inside each scenario. An inflation spike lifts the rule's rate, and the
simulated rate follows it up at the rule's speed, so high-inflation scenarios are also high-rate scenarios, as in
1973-1981 or 2022; a jump in unemployment pulls the rule's rate down. Inflation that settles at the target with
unemployment at its longer-run level leaves the rate at the neutral real rate plus the target. The rule reads
inflation and unemployment as they stand when the step begins, as a central bank sets its rate on the latest
data, and the mean-reverting part is the exact Vasicek (1977) transition, so a gap halves in ln 2 / kappa years
whatever the step size. In a run the rate stops at the effective lower bound, as the Federal Reserve notes the
funds rate cannot be cut materially below it (Board of Governors of the Federal Reserve System (2026, Box 4)):
this step moves the shadow rate underneath, as in Black (1995), which keeps following the rule below the floor,
so a deep recession holds the rate at the floor until the rule climbs back above it, as from 2008 to 2015.

A prescribed path replaces the rule for a while, as a supervisory scenario prescribes the policy rate (the
Federal Reserve's 2026 severely adverse scenario takes the 3-month Treasury rate from 3.7% to 0.1% within half a
year, Board of Governors of the Federal Reserve System (2026, p. 14)): the rate is then pulled toward
`prescribed_rate` instead of the rule's rate, at the same speed, and `prescribed_weight` below one blends the two
while the path hands the rate back to the rule.

With an `anchor` the expected path is the market's instead of the rule's (`market_expected_short_rates`): the
rate follows the path m(t) the forward curve implied on the start date, and the rule acts on the gap between
this scenario's inflation and unemployment and their expected paths, the calibrated model's median paths without
regimes, beliefs or shocks (`MacroBaseline`). The rule's weights, speed and floor are unchanged, but what the
market already priced in is not counted again: a scenario whose inflation and unemployment stay on their expected
paths, with no shocks of its own, follows m(t) exactly, and a regime that lifts inflation by a point in every
scenario lifts the rate's target by 1 + a points, as the rule's own path would. The median, not the average, is
the expected path here because inflation's rare high spells lift its average above where most scenarios are:
read against the average, the typical scenario would sit below the market path and, past the curve, below the
rule's steady state, by half again the spikes' pull on the average. This is the deterministic shift of Brigo and
Mercurio (2001; section 2, eq. 3, of the authors' extended report), r(t) = x(t) + phi(t), which lets a short-rate
model start from any expected path while its dynamics stay its own; phi(t) = m(t) - R*(pi_bar(t), u_bar(t)) is a
fixed function of time, the same in every run of the calibration whatever its size.

The formula is as follows:

$$
s(t + \text{dt}) = (1 - w(t)) \cdot (m(t + \text{dt}) - m(t)) + T(t) + (s(t) - T(t)) \cdot \exp(- \kappa \cdot \text{dt}) + \sigma \cdot s(\text{dt}) \cdot z
$$

$$
s(\text{dt}) = \sqrt{(1 - \exp(- 2 \cdot \kappa \cdot \text{dt})) / (2 \cdot \kappa)}
$$

$$
T(t) = A(t) + w(t) \cdot (P(t) - A(t))
$$

$$
A(t) = R \cdot (t) \text{without an}\; \text{anchor;} A (t) = m(t) + R \cdot (\pi(t),\; u(t)) - R \cdot (\pi_{bar}(t),\; u_{bar}(t)) \text{with one}
$$

Where s is the shadow rate, R*(t) is `policy_rule_rate` at this scenario's inflation and unemployment, P(t) the
prescribed rate and w(t) its weight (0 without a path), m(t) the anchored path (constant without one), pi_bar and
u_bar the expected inflation and unemployment, and z a standard normal draw.

**References:**

- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. Section 5, eqs. (25)-(26). <https://doi.org/10.1016/0304-405x(77>)90016-2
- Black, F. (1995). "Interest Rates as Options." The Journal of Finance, 50(5), 1371-1376. <https://doi.org/10.1111/j.1540-6261.1995.tb05182.x>
- Board of Governors of the Federal Reserve System (2026). "2026 Final Supervisory Stress Test Scenarios." p. 14. <https://www.federalreserve.gov/publications/files/2026-final-supervisory-stress-test-scenarios-20260204.pdf>
- Brigo, D., Mercurio, F. (2001). "A Deterministic-Shift Extension of Analytically-Tractable and Time-Homogeneous Short-Rate Models." Finance and Stochastics, 5(3), 369-387. <https://doi.org/10.1007/pl00013541>; extended report, section 2, eq. (3): <https://www.ma.imperial.ac.uk/~dbrigo/detshiftrep.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_policy_rule_rate(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: PolicyRuleParams,
    inflation: np.ndarray | float,
    unemployment: np.ndarray | float,
    prescribed_rate: float | None = None,
    prescribed_weight: float = 1.0,
    anchor: tuple[float, float, float, float] | None = None,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's shadow rate in each scenario.
- <u>shock (np.ndarray &#124; float):</u> the random draw for this step, standard normal.
- <u>time_step (float):</u> the step length, in years.
- <u>params (PolicyRuleParams):</u> the rule's settings and the speed and volatility.
- <u>inflation (np.ndarray &#124; float):</u> each scenario's inflation at the start of the step.
- <u>unemployment (np.ndarray &#124; float):</u> each scenario's unemployment rate at the start of the step.
- <u>prescribed_rate (float &#124; None):</u> the rate a belief path prescribes at the start of the step, P(t); None (the default) follows the rule.
- <u>prescribed_weight (float):</u> w(t), the weight of `prescribed_rate` against the rule's rate, 1 by default.
- <u>anchor (tuple[float, float, float, float] &#124; None):</u> (m(t), m(t + dt), pi_bar(t), u_bar(t)), the anchored path at the start and end of the step and the expected (median) inflation and unemployment at its start; None (the default) follows the rule's own path.

**Returns:**

<u>np.ndarray:</u> the shadow rate one step later; it may be below the lower bound.

</details>

#### fit_acm_term_structure

Fit the term premium of a government curve with the three-step regressions of Adrian, Crump and Moench (2013):
how much of each yield is the short rate investors expect over the bond's life, and how much is the premium they
demand for holding the bond instead.

A forward rate is the expected short rate plus a premium, so reading a market path off a curve needs the premium
of that curve. Adrian, Crump and Moench (2013, section 2) price the curve with a few of its principal components
X(t). Their three ordinary least-squares steps: a VAR of the components gives their dynamics and innovations;
each bond's excess return over the one-month rate is regressed on the innovations (its exposures beta) and on
the lagged components; a cross-section of those exposures gives the market prices of risk lambda0 and lambda1.
Two recursions then price every maturity, once with those prices of risk and once without: the yield and the
risk-neutral yield, the average short rate expected over the bond's life. Their difference is the term premium.
The curve's principal components are read from its 3- to 120-month yields and the excess returns of twelve
bonds of 6 to 120 months are priced, as in their section 3.1. Run on the Gürkaynak, Sack and Wright (2007)
Treasury curve with the 3-month bill as the short rate, month-ends from June 1961 to September 2026, this code
gives the New York Fed's ten-year premium (ACMTP10) within 4 basis points on average (largest gap 16); with the
curve's own one-month yield as the short rate, as the paper describes, it comes out 18 basis points lower, the
average gap between that yield and the bill. Malik and Meldrum (2016) run the same regressions on the gilt curve.

The formula is as follows:

$$
X(t + 1) = \mu + \Phi \cdot X(t) + v(t + 1),\;\; \Sigma = V V' / T
$$

$$
\operatorname{rx}(n - 1,\; t + 1) = a(n) + \beta(n) \text{'} \cdot v(t + 1) + c(n) \text{'} \cdot X(t) + e(t + 1),\;\; \sigma ^{2} = \operatorname{tr}(E E') / (N \cdot T)
$$

$$
\text{lambda0} = (B B') ^{-1} \cdot B \cdot (a + (B \cdot \operatorname{vec}(\Sigma) + \sigma ^{2}) / 2),\;\; \text{lambda1} = (B B') ^{-1} \cdot B \cdot C
$$

$$
A(n) = A(n - 1) + B(n - 1) \text{'} (\mu - \text{lambda0}) + (B(n - 1) \text{'} \Sigma B (n - 1) + \sigma ^{2}) / 2 - \text{delta0}
$$

$$
B(n) \text{'} = B(n - 1) \text{'} (\Phi - \text{lambda1}) - \text{delta1'},\;\; \text{with}\; r (t) = \text{delta0} + \text{delta1'} X (t) \text{and}\; y (n) = - (A(n) + B(n) \text{'} X) / n
$$

$$
\operatorname{TP}(n) = y(n) - y_{RN}(n),\;\; \text{where} \;\; y_{RN} \;\text{takes}\; \text{lambda0} = \text{lambda1} = 0
$$

Where rx(n - 1, t + 1) = ln P(n - 1, t + 1) - ln P(n, t) - r(t) is the log excess return of a bond of n months
held for one, and B* stacks vec(beta(n) beta(n)').

**As an example:**

```python
import numpy as np

from financescenarios.factors.interest_rates.interest_rates_model import acm_term_premia, fit_acm_term_structure

# Fifty years of a one-factor curve whose investors demand a known premium.
rng = np.random.default_rng(0)
factor = np.zeros(600)
for month in range(1, 600):
    factor[month] = 0.97 * factor[month - 1] + 0.0004 * rng.standard_normal()
constant, loading, neutral = np.zeros(121), np.zeros(121), np.zeros(121)
for n in range(1, 121):
    constant[n] = constant[n - 1] + 0.00002 * loading[n - 1] + 0.5 * (0.0004 * loading[n - 1]) ** 2 - 0.003
    neutral[n] = neutral[n - 1] + 0.5 * (0.0004 * loading[n - 1]) ** 2 - 0.003
    loading[n] = 0.97 * loading[n - 1] - 1
scale = 12 / np.arange(1, 121)
yields = -(constant[1:] + np.outer(factor, loading[1:])) * scale

model = fit_acm_term_structure(yields, yields[:, 0], n_factors=1)
acm_term_premia(model, yields[-1])[[11, 59, 119]]
```

Which returns:

| Maturity | Fitted premium | True premium |
|:---------|---------------:|-------------:|
| 1 year   | 0.0006 | 0.0012 |
| 5 years  | 0.0037 | 0.0043 |
| 10 years | 0.0063 | 0.0058 |

Fifty years of month-ends of a one-factor curve with a known price of risk give back its premium within 6 basis
points; the gap is what fifty years leave unknown about the factor's own dynamics.

**References:**

- Adrian, T., Crump, R.K., Moench, E. (2013). "Pricing the Term Structure with Linear Regressions." Journal of Financial Economics, 110(1), 110-138. Sections 2.3-2.4 and 3.1. <https://doi.org/10.1016/j.jfineco.2013.04.009>
- Malik, S., Meldrum, A. (2016). "Evaluating the Robustness of UK Term Structure Decompositions Using Linear Regression Methods." Journal of Banking & Finance, 67, 85-102. Sections 2-3. <https://doi.org/10.1016/j.jbankfin.2016.02.006>
- Gürkaynak, R.S., Sack, B., Wright, J.H. (2007). "The U.S. Treasury Yield Curve: 1961 to the Present." Journal of Monetary Economics, 54(8), 2291-2304. <https://doi.org/10.1016/j.jmoneco.2007.06.029>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_acm_term_structure(
    yields: np.ndarray,
    short_rate: np.ndarray,
    curve_months: np.ndarray | tuple[int, ...] = ACM_CURVE_MONTHS,
    return_months: tuple[int, ...] = ACM_RETURN_MATURITIES,
    n_factors: int = ACM_FACTORS,
    short_rate_name: str = 'one-month rate',
    sample: tuple[str, str] = ('', ''),
) -> AcmTermStructure
```

**Args:**

- <u>yields (np.ndarray):</u> continuously compounded zero rates, decimals, one row per month-end and one column per month of maturity from 1 to 120 (nan where not used).
- <u>short_rate (np.ndarray):</u> the one-month rate the excess returns are measured over, continuously compounded, decimals, one per month-end.
- <u>curve_months (np.ndarray &#124; tuple[int, ...]):</u> the maturities, in months, the principal components are read from. Defaults to `ACM_CURVE_MONTHS`.
- <u>return_months (tuple[int, ...]):</u> the maturities whose excess returns are priced. Defaults to `ACM_RETURN_MATURITIES`.
- <u>n_factors (int):</u> the principal components priced. Defaults to `ACM_FACTORS`.
- <u>short_rate_name (str):</u> what the short rate is, for the record.
- <u>sample (tuple[str, str]):</u> the first and last month of the sample, for the record.

**Returns:**

<u>AcmTermStructure:</u> the factor loadings and each maturity's term premium as a function of them.

**Raises:**

- <u>ValueError:</u> if the shapes disagree, yields the fit needs are missing, fewer than `ACM_MINIMUM_MONTHS` months are given, or the fitted yields miss the curve by more than `ACM_MAXIMUM_FIT_RMSE`.

</details>

#### zero_rates_from_par

The zero-coupon rates a par curve implies, every half year up to `horizon`: what a single payment at each date is
worth, the curve forward rates are read from.

The US Treasury publishes par yields, the coupon at which a bond of each maturity would trade at its face value,
on a bond-equivalent (semiannual) basis. Each half year's discount factor follows from the bond that matures then,
given the earlier ones: the bootstrap. Par yields between published maturities are interpolated linearly, as the
Treasury's own curve is read between its points, and held flat beyond the first and last.

The formula is as follows:

$$
1 = (c_{k} / 2) \cdot (D_{1} + ... + \text{D\_k-1}) + (1 + c_{k} / 2) \cdot D_{k},\;\; \text{for} \;\; \text{the bond maturing at}\; t_{k} = k / 2
$$

$$
z(t_{k}) = - \ln(D_{k}) / t_{k}
$$

Where c_k is the par yield at t_k, D_k the discount factor and z the continuously compounded zero rate.

**References:**

- U.S. Department of the Treasury. "Treasury Yield Curve Methodology." Par yields on a bond-equivalent basis. <https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics/treasury-yield-curve-methodology>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
zero_rates_from_par(
    maturities: np.ndarray,
    par_yields: np.ndarray,
    horizon: float = MARKET_PATH_HORIZON,
) -> tuple[np.ndarray, np.ndarray]
```

**Args:**

- <u>maturities (np.ndarray):</u> the par curve's maturities in years, positive and ascending.
- <u>par_yields (np.ndarray):</u> the par yields, decimals, semiannual bond-equivalent.
- <u>horizon (float):</u> the last maturity to bootstrap, in years. Defaults to `MARKET_PATH_HORIZON`.

**Returns:**

<u>tuple[np.ndarray, np.ndarray]:</u> the half-year maturities and their continuously compounded zero rates.

**Raises:**

- <u>ValueError:</u> if the inputs are empty, unequal in length, not ascending, or a discount factor is not positive.

</details>

#### market_expected_short_rates

The short rate the market expects in each year ahead: the forward rate the curve locks in for that year, less
the term premium investors demand for lending that far ahead.

A forward rate is what the curve lets you lock in today for borrowing in a future year, so it is the market's
expected short rate for that year plus a premium for bearing interest-rate risk until then. Adrian, Crump and
Moench (2013, section 2.4) split each yield into the average short rate expected over the bond's life (the
risk-neutral yield) and that term premium; taking the premium's forward part out of each year's forward rate
leaves the expected path. Without a premium the forward rates themselves are the path.

The zero rates are interpolated linearly to whole years, and so are the premia (zero at maturity zero). Each
year's rate is placed in the middle of that year, after today's short rate.

The formula is as follows:

$$
F(n) = n \cdot z(n) - (n - 1) \cdot z(n - 1),\;\; \text{the forward rate for year n},\;\; \text{with}\; z (0) \cdot 0 = 0
$$

$$
\text{TP}_{f}(n) = n \cdot \operatorname{TP}(n) - (n - 1) \cdot \operatorname{TP}(n - 1),\;\; \text{the premium's forward part}
$$

$$
m(n - 0.5) = F(n) - \text{TP}_{f}(n),\;\; \text{and}\; m (0) = r(0)
$$

Where z is the continuously compounded zero rate, TP the yield's term premium and r(0) today's short rate.

**References:**

- Adrian, T., Crump, R.K., Moench, E. (2013). "Pricing the Term Structure with Linear Regressions." Journal of Financial Economics, 110(1), 110-138. Section 2.4. <https://doi.org/10.1016/j.jfineco.2013.04.009>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
market_expected_short_rates(
    maturities: np.ndarray,
    zero_rates: np.ndarray,
    short_rate: float,
    premium_maturities: np.ndarray | None = None,
    term_premia: np.ndarray | None = None,
    horizon: float = MARKET_PATH_HORIZON,
) -> tuple[np.ndarray, np.ndarray]
```

**Args:**

- <u>maturities (np.ndarray):</u> the curve's maturities in years, positive and ascending.
- <u>zero_rates (np.ndarray):</u> continuously compounded zero rates at those maturities, decimals.
- <u>short_rate (float):</u> today's short rate, the path's first point.
- <u>premium_maturities (np.ndarray &#124; None):</u> the maturities of the term premium estimate, in years.
- <u>term_premia (np.ndarray &#124; None):</u> the term premium of the yield at each, decimals; None takes none out.
- <u>horizon (float):</u> the last year read off the curve. Defaults to `MARKET_PATH_HORIZON`.

**Returns:**

<u>tuple[np.ndarray, np.ndarray]:</u> the times (0, 0.5, 1.5, ...) and the expected short rate at each.

**Raises:**

- <u>ValueError:</u> if the curve does not reach a year ahead or the premia come without their maturities.

</details>

#### bank_discount_rate

A continuously compounded rate quoted the way a Treasury bill is: as its bank discount rate, the discount from
par over a 360-day year, so a path read off a zero-coupon curve is on the basis of the bill rate it anchors.

The 13-week bill rate a dollar short rate is fitted and starts on (`^IRX`) is quoted on this basis, which the US
Treasury defines as the rate "based on the par value, amount of the discount and a 360-day year", against the
coupon equivalent on the purchase price and a 365-day year (Daily Treasury Bill Rates, definitions). At 4% the
discount rate is about 7 basis points below the continuously compounded rate of the same bill, at 10% about 27.

The formula is as follows:

$$
P / F = \exp(- r \cdot t / 365)
$$

$$
d = (F - P) / F \cdot 360 / t = (360 / t) \cdot (1 - \exp(- r \cdot t / 365))
$$

Where r is the continuously compounded rate, t the bill's days to maturity, P its price and F its par value.

**References:**

- U.S. Department of the Treasury. "Daily Treasury Bill Rates", definitions of the bank discount rate and the coupon equivalent. <https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_bill_rates&field_tdr_date_value=202610>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
bank_discount_rate(rate: np.ndarray | float, days: int) -> np.ndarray
```

**Args:**

- <u>rate (np.ndarray &#124; float):</u> continuously compounded rates, decimals.
- <u>days (int):</u> the bill's days to maturity, 91 for the 13-week bill.

**Returns:**

<u>np.ndarray:</u> the same rates as bank discount rates, decimals.

</details>

#### market_path_levels

The market-anchored expected short rate at any time ahead: the market's path up to its horizon, then converging
to the policy rule's steady state, the neutral real rate plus the inflation target.

Past the maturities whose expectations can be read, the short rate is expected to close its gap to its long-run
level at its own speed of mean reversion, as in Vasicek (1977, section 5, eq. 25): the expected rate s years
ahead is the level plus the gap times exp(-a * s). The speed is the one the paired expectations long rate reads
the short rate with (`expectations_weight`), fitted on the short rate's own history, so the path and the long
rate built on it describe one expected path (Campbell and Shiller (1991)). Kozicki and Tinsley (2001) read long
rates against such a long-horizon endpoint that shifts as beliefs about it do, rather than a fixed historical
mean; here the endpoint is the steady state as known on the curve's date.

The formula is as follows:

$$
m(t) = \text{the path interpolated linearly},\;\; \text{for t up to its last point},\;\; \text{then held to the horizon H}
$$

$$
m(H + s) = m_{ss} + (m(H) - m_{ss}) \cdot \exp(- a \cdot s)
$$

Where m_ss is `steady_state` and a the short rate's own speed of mean reversion (`MarketPath.convergence_speed`).

**References:**

- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. Section 5, eq. (25). <https://doi.org/10.1016/0304-405x(77>)90016-2
- Campbell, J.Y., Shiller, R.J. (1991). "Yield Spreads and Interest Rate Movements: A Bird's Eye View." The Review of Economic Studies, 58(3), 495-514. Section 2, eq. (1). <https://doi.org/10.2307/2298008>
- Kozicki, S., Tinsley, P.A. (2001). "Shifting Endpoints in the Term Structure of Interest Rates." Journal of Monetary Economics, 47(3), 613-652. <https://doi.org/10.1016/s0304-3932(01>)00054-x

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
market_path_levels(times: np.ndarray, path: MarketPath, steady_state: float) -> np.ndarray
```

**Args:**

- <u>times (np.ndarray):</u> years ahead to read the path at.
- <u>path (MarketPath):</u> the market's path.
- <u>steady_state (float):</u> where the path converges beyond its horizon.

**Returns:**

<u>np.ndarray:</u> the expected short rate at each time.

</details>

#### expectations_weight

How much of a short rate's gap to its long-run level is still expected, on average, over a bond's life: the
weight a long yield under the expectations hypothesis puts on today's short rate.

A short rate that reverts fast is expected to close most of its gap within a few years, so a 10-year yield moves
little with it; one that reverts slowly carries its gap through most of the bond's life, so the yield follows it
closely. Fitted as a Hull-White rate on the OECD's yearly rates from 1950 to 2025, the US short rate reverts at
0.114 a year, so a 10-year yield carries 0.60 of every move in it; the German short rate reverts at 0.192 (0.44)
and the British at 0.099 (0.63). The US weight is about the loading of the New York Fed's expected average short
rate over ten years on the 3-month bill: 0.59 in a regression of its ACMRNY10 series on ^IRX, monthly from June
1961 to September 2026, the risk-neutral yield of Adrian, Crump and Moench (2013, section 2.4). A policy rule's
speed is something else: the inertial rule's 0.65 a year is how fast the rate closes its gap to a target that
inflation and unemployment keep moving, and as a speed here it would give 0.15. A long rate on a policy-rule short
rate therefore takes the short rate's own speed on the history its term premium is fitted on (see
`InterestRates.calibrate_expectations`).

The formula is as follows:

$$
D = (1 - \exp(- a \cdot m)) / (a \cdot m)
$$

Where a is the short rate's speed of mean reversion and m the maturity in years.

**References:**

- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. Section 5, eq. (25), the expected future short rate. <https://doi.org/10.1016/0304-405x(77>)90016-2
- Adrian, T., Crump, R.K., Moench, E. (2013). "Pricing the Term Structure with Linear Regressions." Journal of Financial Economics, 110(1), 110-138. Section 2.4, the risk-neutral yields. <https://doi.org/10.1016/j.jfineco.2013.04.009>
- Federal Reserve Bank of New York. "Treasury Term Premia" (ACMTermPremium.xls: these statistics from its ACM Monthly sheet; a market path reads its ACM Daily sheet, `acm_term_structure`). <https://www.newyorkfed.org/research/data_indicators/term-premia-tabs>
- Federal Reserve. "Policy Rules and How Policymakers Use Them" (2018), the inertial rule. <https://www.federalreserve.gov/monetarypolicy/policy-rules-and-how-policymakers-use-them.htm>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
expectations_weight(short_rate_speed: float, maturity: float) -> float
```

**Args:**

- <u>short_rate_speed (float):</u> the short rate's speed of mean reversion, a year.
- <u>maturity (float):</u> the long rate's maturity in years.

**Returns:**

<u>float:</u> the weight D, between 0 and 1.

</details>

#### average_expected_level

The part of the expected average short rate that comes from where the short rate is heading: its long-run level
path averaged over a bond's life, each date weighted by how far the short rate is expected to have reverted.

With a constant long-run level this is just that level. With a moving one, such as EIOPA's forward rates, a
10-year yield looks ahead along the path, so a level that rises over the next decade lifts it today.

The formula is as follows:

$$
\theta_{bar}(t) = \text{integral of}\; w (v) \cdot \theta(t + v) \text{dv} / \text{integral of}\; w (v) \text{dv},\;\; \text{over v from 0 to m}
$$

$$
w(v) = 1 - \exp(- a \cdot (m - v))
$$

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
average_expected_level(
    levels: np.ndarray,
    time_step: float,
    short_rate_speed: float,
    maturity: float,
) -> np.ndarray
```

**Args:**

- <u>levels (np.ndarray):</u> the long-run level path on an even grid, reaching `maturity` years past the last date.
- <u>time_step (float):</u> the grid's spacing in years.
- <u>short_rate_speed (float):</u> the short rate's speed of mean reversion, a year.
- <u>maturity (float):</u> the long rate's maturity in years.

**Returns:**

<u>np.ndarray:</u> one weighted average per date, `maturity / time_step` fewer than `levels`.

**Raises:**

- <u>ValueError:</u> if `levels` does not reach `maturity` years past its first date.

</details>

#### anchored_level_average

The level a long rate's expected path averages when its short rate follows an anchored expected path: chosen so
that `expected_average_short_rate` gives the anchored path's own average over the bond's life plus the share of
today's gap to it still expected, D * (r(t) - m(t)).

A market-anchored short rate is expected to follow the market's path m, so a 10-year yield reads that path's
average over the next ten years, here the trapezoid rule on the grid; a scenario's short rate away from the path
is expected to close the gap at the short rate's own speed, which is what D measures (`expectations_weight`).

The formula is as follows:

$$
m_{bar}(t) = (1 / M) \cdot \text{integral of}\; m (t + v) \text{dv},\;\; \text{over v from 0 to M}
$$

$$
\theta_{bar}(t) = (m_{bar}(t) - D \cdot m(t)) / (1 - D)
$$

$$
\text{so that}\; D \cdot r(t) + (1 - D) \cdot \theta_{bar}(t) = m_{bar}(t) + D \cdot (r(t) - m(t))
$$

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
anchored_level_average(
    levels: np.ndarray,
    time_step: float,
    short_rate_speed: float,
    maturity: float,
) -> np.ndarray
```

**Args:**

- <u>levels (np.ndarray):</u> the anchored path m on an even grid, reaching `maturity` years past the last date.
- <u>time_step (float):</u> the grid's spacing in years.
- <u>short_rate_speed (float):</u> the short rate's speed of mean reversion, a year.
- <u>maturity (float):</u> the long rate's maturity in years.

**Returns:**

<u>np.ndarray:</u> one level per date, `maturity / time_step` fewer than `levels`.

**Raises:**

- <u>ValueError:</u> if `levels` does not reach `maturity` years past its first date, or the speed leaves no room for the path (D of one).

</details>

#### expected_average_short_rate

The short rate expected on average over a bond's life, given today's short rate and where it is heading: the
expectations-hypothesis part of a long yield (Campbell and Shiller (1991, section 2, eq. 1)).

The formula is as follows:

$$
\operatorname{EH}(t) = D \cdot r(t) + (1 - D) \cdot \theta_{bar}(t)
$$

Where D is `expectations_weight` and theta_bar the `average_expected_level`.

**References:**

- Campbell, J.Y., Shiller, R.J. (1991). "Yield Spreads and Interest Rate Movements: A Bird's Eye View." The Review of Economic Studies, 58(3), 495-514. Section 2, eq. (1). <https://doi.org/10.2307/2298008>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
expected_average_short_rate(
    short_rate: np.ndarray | float,
    level_average: np.ndarray | float,
    short_rate_speed: float,
    maturity: float,
) -> np.ndarray
```

**Args:**

- <u>short_rate (np.ndarray &#124; float):</u> today's short rate in each scenario.
- <u>level_average (np.ndarray &#124; float):</u> the long-run level averaged over the bond's life.
- <u>short_rate_speed (float):</u> the short rate's speed of mean reversion, a year.
- <u>maturity (float):</u> the long rate's maturity in years.

**Returns:**

<u>np.ndarray:</u> the expected average short rate.

</details>

#### fit_term_premium_process

Fit the term premium of a long rate that follows the expectations hypothesis: what is left of the long rate after
the short rate expected over its maturity, how fast that premium reverts, and how it moves with the short rate.

Campbell and Shiller (1991, section 2, eq. 1) write a long yield as the average of the short rates expected over
its life plus a term premium. The expected path here reverts at `short_rate_speed` to the short rate's fitted
long-run level, so the premium is the long rate less `expected_average_short_rate` along that path. History
shows that premium reverting within a few years, and higher when short rates are high: on the OECD's yearly
rates since 1950 the long rate has followed a lasting gap in the short rate about one for one, more than a short
rate reverting to a fixed level would justify, and the New York Fed's ACM 10-year term premium moves the same way
(a correlation of 0.52 between its ACMTP10 series and the 3-month bill, monthly from June 1961 to September 2026).
The premium therefore reverts toward a target that moves with the short rate's gap to its long-run level, which
keeps the spread between the two rates mean-reverting, as it is in the data.
The regression is read through the exact mean-reverting transition, so the speed is a yearly figure whatever the
sampling period.

In the same year, though, the premium moves the other way: the ACM premium falls 0.12 for every point the 3-month
bill rises, in yearly-average changes from 1962 to 2025 (ACMTP10 on ^IRX), while its risk-neutral yield, the
expected path of Adrian, Crump and Moench (2013, section 2.4), takes 0.52. A premium that only follows the gap
rises with the short rate instead, so the long rate overreacts to every move. `short_rate_change` adds the short
rate's change over the step as a regressor, gamma: on the OECD's yearly rates from 1950 to 2025, with the expected
path at each short rate's own speed and the policy rule's steady state, it is -0.107 for the US (t-statistic
-2.4), -0.082 for Germany (-2.0) and -0.255 for the UK (-4.9), the US figure close to ACM's.

The formula is as follows:

$$
\operatorname{TP}(t) = L(t) - (D \cdot r(t) + (1 - D) \cdot \theta)
$$

$$
\operatorname{TP}(t + 1) = c + \phi \cdot \operatorname{TP}(t) + \psi \cdot (r(t) - \theta) + \gamma \cdot (r(t + 1) - r(t)) + e(t)
$$

$$
\kappa = - \ln(\phi) / \text{dt},\;\; \tau = c / (1 - \phi),\;\; \beta = \psi / (1 - \phi)
$$

Where theta is the short rate's long-run level, D the `expectations_weight` and gamma 0 without
`short_rate_change`.

**References:**

- Campbell, J.Y., Shiller, R.J. (1991). "Yield Spreads and Interest Rate Movements: A Bird's Eye View." The Review of Economic Studies, 58(3), 495-514. Section 2, eq. (1). <https://doi.org/10.2307/2298008>
- Adrian, T., Crump, R.K., Moench, E. (2013). "Pricing the Term Structure with Linear Regressions." Journal of Financial Economics, 110(1), 110-138. Section 2.4, the risk-neutral yields and the term premium. <https://doi.org/10.1016/j.jfineco.2013.04.009>
- Federal Reserve Bank of New York. "Treasury Term Premia" (ACMTermPremium.xls: these statistics from its ACM Monthly sheet; a market path reads its ACM Daily sheet, `acm_term_structure`). <https://www.newyorkfed.org/research/data_indicators/term-premia-tabs>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_term_premium_process(
    long_rate: np.ndarray,
    short_rate: np.ndarray,
    time_step: float,
    short_rate_speed: float,
    short_rate_level: float,
    maturity: float,
    short_rate_change: bool = False,
) -> TermPremiumParams
```

**Args:**

- <u>long_rate (np.ndarray):</u> the long rate's history as decimals, evenly spaced.
- <u>short_rate (np.ndarray):</u> the short rate on the same dates.
- <u>time_step (float):</u> the time between observations, in years.
- <u>short_rate_speed (float):</u> the short rate's speed of mean reversion, a year.
- <u>short_rate_level (float):</u> the short rate's fitted long-run level.
- <u>maturity (float):</u> the long rate's maturity in years.
- <u>short_rate_change (bool):</u> also fit gamma, the premium's move with the short rate's change in the same step; False (the default) leaves it at 0.

**Returns:**

<u>TermPremiumParams:</u> the premium's speed, long-run level, short-rate sensitivities and volatility, and the last long rate as the starting point.

**Raises:**

- <u>ValueError:</u> if the series differ in length, are too short, or the premium does not revert.

</details>

#### step_expectations_long_rate

Move a long rate that follows the expectations hypothesis forward one step: it is the short rate expected over its
maturity in this scenario, plus a term premium that reverts toward its target with a normally distributed shock.

This is what ties the long end of the curve to the short end inside each scenario. A rise in the short rate lifts
the long rate at once by the share of it expected to last over the bond's life, plus gamma (a fitted premium
falls a little in the same step), and over the next few years by more as the premium follows the short rate's
gap; a fall does the reverse. The spread between the two rates
therefore reverts within a few years, so the curve inverts when the short rate jumps and steepens again as the
jump fades, as it has done historically, rather than staying inverted for decades. Today's premium is read off
the current long and short rate, so a one-off shock to the long rate moves the premium with it.

A prescribed path replaces the expected short rate and the premium for a while, as a supervisory scenario
prescribes the 10-year yield: the long rate is then pulled toward `prescribed_rate` at the premium's speed, with
the premium's volatility, and `prescribed_weight` below one blends that step with the usual one while the path
hands the long rate back to its short rate.

The formula is as follows:

$$
\operatorname{TP}(t) = L(t) - (D \cdot r(t) + (1 - D) \cdot \theta_{bar}(t))
$$

$$
\operatorname{TP}(t + \text{dt}) = \text{TP} \cdot (t) + (\operatorname{TP}(t) - \text{TP} \cdot (t)) \cdot \exp(- \kappa \cdot \text{dt}) + \gamma \cdot (r(t + \text{dt}) - r(t)) + \sigma \cdot s(\text{dt}) \cdot z
$$

$$
s(\text{dt}) = \sqrt{(1 - \exp(- 2 \cdot \kappa \cdot \text{dt})) / (2 \cdot \kappa)}
$$

$$
L(t + \text{dt}) = D \cdot r(t + \text{dt}) + (1 - D) \cdot \theta_{bar}(t + \text{dt}) + \operatorname{TP}(t + \text{dt})
$$

$$
\text{with a path:}\;\; L(t + \text{dt}) = w(t) \cdot (P(t) + (L(t) - P(t)) \cdot \exp(- \kappa \cdot \text{dt}) + \sigma \cdot s(\text{dt}) \cdot z) + (1 - w(t)) \cdot L'
$$

Where TP*(t) = tau + beta * (r(t) - theta(t)) is the premium's target, z a standard normal draw, P(t) the
prescribed rate, w(t) its weight and L' the long rate of the step without a path.

**References:**

- Campbell, J.Y., Shiller, R.J. (1991). "Yield Spreads and Interest Rate Movements: A Bird's Eye View." The Review of Economic Studies, 58(3), 495-514. Section 2, eq. (1). <https://doi.org/10.2307/2298008>
- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. Section 5, eqs. (25)-(26). <https://doi.org/10.1016/0304-405x(77>)90016-2

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_expectations_long_rate(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: TermPremiumParams,
    short_rate: np.ndarray | float,
    next_short_rate: np.ndarray | float,
    level: float,
    level_average: float,
    next_level_average: float,
    prescribed_rate: float | None = None,
    prescribed_weight: float = 1.0,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's long rate in each scenario.
- <u>shock (np.ndarray &#124; float):</u> the random draw for this step, standard normal.
- <u>time_step (float):</u> the step length, in years.
- <u>params (TermPremiumParams):</u> the fitted term premium and the short rate's expected-path settings.
- <u>short_rate (np.ndarray &#124; float):</u> each scenario's short rate at the start of the step.
- <u>next_short_rate (np.ndarray &#124; float):</u> each scenario's short rate at the end of the step.
- <u>level (float):</u> the short rate's long-run level at the start of the step.
- <u>level_average (float):</u> that level averaged over the maturity, at the start of the step.
- <u>next_level_average (float):</u> the same at the end of the step.
- <u>prescribed_rate (float &#124; None):</u> the long rate a belief path prescribes at the start of the step, P(t); None (the default) follows the short rate and the premium.
- <u>prescribed_weight (float):</u> w(t), the weight of the step toward `prescribed_rate`, 1 by default.

**Returns:**

<u>np.ndarray:</u> the long rate one step later; it may be negative.

</details>

#### nelson_siegel_loadings

How strongly the slope and the curvature move the yield at one maturity, in the Nelson-Siegel curve.

These loadings are what give the three factors their meaning. The level's loading is 1 at every maturity, so it
shifts the whole curve in parallel. The slope's loading B(tau) starts at 1 for the shortest maturity and fades
toward 0 for long ones, so a rise in the slope lifts short yields more than long ones. The curvature's loading is
0 at both ends and peaks at medium maturities (about 2.5 years with the default decay of 0.7308), so it bends
the middle of the curve. A higher decay moves that peak to shorter maturities.

The formula is as follows:

$$
y(\tau) = L + S \cdot B(\tau) + C \cdot (B(\tau) - \exp(- \lambda \cdot \tau))
$$

$$
B(\tau) = (1 - \exp(- \lambda \cdot \tau)) / (\lambda \cdot \tau)
$$

Where L, S and C are the level, slope and curvature factors and lambda is `decay`; this returns the S and C
loadings, B(tau) and B(tau) - exp(-lambda * tau).

**References:**

- Nelson, C.R., Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." The Journal of Business, 60(4), 473-489. <https://doi.org/10.1086/296409> The static functional form and loadings this function implements.
- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. <https://doi.org/10.1016/j.jeconom.2005.03.005>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
nelson_siegel_loadings(tenor: float, decay: float) -> tuple[float, float]
```

**Args:**

- <u>tenor (float):</u> the maturity, in years (above 0).
- <u>decay (float):</u> the Nelson-Siegel decay (lambda), per year.

**Returns:**

<u>tuple[float, float]:</u> the slope loading and the curvature loading at this maturity.

**Raises:**

- <u>ValueError:</u> if `tenor` is not above 0.

</details>

#### nelson_siegel_yield

The yield at one maturity from the curve's level, slope and curvature. Pass one date's factors to read one yield,
or the simulated `rate_level`, `rate_slope` and `rate_curvature` paths to get that maturity's yield in every
scenario and period.

The formula is as follows:

$$
y(\tau) = L + S \cdot B(\tau) + C \cdot (B(\tau) - \exp(- \lambda \cdot \tau))
$$

$$
B(\tau) = (1 - \exp(- \lambda \cdot \tau)) / (\lambda \cdot \tau)
$$

Where L, S and C are the level, slope and curvature and lambda is `decay` (see `nelson_siegel_loadings`).

**References:**

- Nelson, C.R., Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." The Journal of Business, 60(4), 473-489. <https://doi.org/10.1086/296409>
- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. <https://doi.org/10.1016/j.jeconom.2005.03.005>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
nelson_siegel_yield(
    level: float | np.ndarray,
    slope: float | np.ndarray,
    curvature: float | np.ndarray,
    tenor: float,
    decay: float,
) -> float | np.ndarray
```

**Args:**

- <u>level (float &#124; np.ndarray):</u> the level factor, or its simulated paths.
- <u>slope (float &#124; np.ndarray):</u> the slope factor, or its simulated paths.
- <u>curvature (float &#124; np.ndarray):</u> the curvature factor, or its simulated paths.
- <u>tenor (float):</u> the maturity, in years.
- <u>decay (float):</u> the Nelson-Siegel decay (lambda) the curve was calibrated with.

**Returns:**

<u>float &#124; np.ndarray:</u> the yield at `tenor`, for each value or path given.

</details>

#### nelson_siegel_forward

The instantaneous forward rate at a maturity from the curve's level, slope and curvature: the rate the curve
implies today for borrowing over a very short period starting `tenor` years from now.

Nelson and Siegel (1987) define their curve through this forward rate, r(m) = β0 + β1 exp(−m/τ) + β2[(m/τ) *
exp(−m/τ)], with 1/τ the decay; the yield at a maturity is its
average out to that maturity. It starts at L + S, today's short rate, and tends to L, the long-run rate, with the
curvature adding a hump in between. Because it is smooth and settles at a finite level, it extrapolates sensibly
beyond the longest observed bond, unlike a piecewise bootstrap, which is why the arbitrage-free `Hjm` curve and
the risk-neutral Hull-White short rate use it as today's forward curve.

The formula is as follows:

$$
f(\tau) = L + S \cdot \exp(- \lambda \cdot \tau) + C \cdot \lambda \cdot \tau \cdot \exp(- \lambda \cdot \tau)
$$

**References:**

- Nelson, C.R., Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." The Journal of Business, 60(4), 473-489. <https://doi.org/10.1086/296409>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
nelson_siegel_forward(
    level: float | np.ndarray,
    slope: float | np.ndarray,
    curvature: float | np.ndarray,
    tenor: float | np.ndarray,
    decay: float,
) -> float | np.ndarray
```

**Args:**

- <u>level (float &#124; np.ndarray):</u> the level factor.
- <u>slope (float &#124; np.ndarray):</u> the slope factor.
- <u>curvature (float &#124; np.ndarray):</u> the curvature factor.
- <u>tenor (float &#124; np.ndarray):</u> one or more maturities, in years (0 or more; 0 gives the short rate).
- <u>decay (float):</u> the Nelson-Siegel decay (lambda), per year.

**Returns:**

<u>float &#124; np.ndarray:</u> the instantaneous forward rate at each maturity.

**Raises:**

- <u>ValueError:</u> if any `tenor` is negative.

</details>

#### nelson_siegel_forward_integral

The Nelson-Siegel forward rate accumulated from today to a maturity: the yield times the maturity, so that
exp(-F(tau)) is the price of a zero-coupon bond paying 1 at tau.

It is the building block for discount factors and for the yield between two future dates, which is how the `Hjm`
curve turns today's forward curve into bond prices at every point of a scenario. It is 0 at maturity 0.

The formula is as follows:

$$
F(\tau) = L \cdot \tau + S \cdot D(\tau) + C \cdot (D(\tau) - \tau \cdot \exp(- \lambda \cdot \tau))
$$

$$
D(\tau) = (1 - \exp(- \lambda \cdot \tau)) / \lambda
$$

**References:**

- Nelson, C.R., Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." The Journal of Business, 60(4), 473-489. <https://doi.org/10.1086/296409>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
nelson_siegel_forward_integral(
    level: float | np.ndarray,
    slope: float | np.ndarray,
    curvature: float | np.ndarray,
    tenor: float | np.ndarray,
    decay: float,
) -> float | np.ndarray
```

**Args:**

- <u>level (float &#124; np.ndarray):</u> the level factor.
- <u>slope (float &#124; np.ndarray):</u> the slope factor.
- <u>curvature (float &#124; np.ndarray):</u> the curvature factor.
- <u>tenor (float &#124; np.ndarray):</u> one or more maturities, in years (0 or more).
- <u>decay (float):</u> the Nelson-Siegel decay (lambda), per year.

**Returns:**

<u>float &#124; np.ndarray:</u> the accumulated forward rate from today to each maturity.

**Raises:**

- <u>ValueError:</u> if any `tenor` is negative.

</details>

#### curve_inversion_frequency

The share of all simulated scenario-periods in which the curve is inverted: the short-maturity yield above the
long-maturity one.

Inversions happen in practice (ahead of most US recessions) and the curve model allows them, so this checks that
they appear about as often as history suggests. The NAIC's draft GOES acceptance criteria (October 2023, T3b) ask
only that the frequency of each yield curve shape in the early years be reasonable given the starting curve, with
no number
(https://content.naic.org/sites/default/files/call_materials/GOES%20Acceptance%20Criteria%20100523.pdf). Far more
inversions point to a slope that is too volatile; almost none, to one that reverts too fast.

The formula is as follows:

$$
\text{share} = \text{mean over cells of}\; 1 \left[y(\text{short\_tenor}) > y(\text{long\_tenor})\right]
$$

Where y is `nelson_siegel_yield` in each scenario and period.

**References:**

- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. <https://doi.org/10.1016/j.jeconom.2005.03.005>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
curve_inversion_frequency(
    level: np.ndarray,
    slope: np.ndarray,
    curvature: np.ndarray,
    short_tenor: float,
    long_tenor: float,
    decay: float,
) -> float
```

**Args:**

- <u>level (np.ndarray):</u> the simulated `rate_level` paths.
- <u>slope (np.ndarray):</u> the simulated `rate_slope` paths.
- <u>curvature (np.ndarray):</u> the simulated `rate_curvature` paths.
- <u>short_tenor (float):</u> the shorter maturity, in years, such as 2.
- <u>long_tenor (float):</u> the longer maturity, in years, such as 10.
- <u>decay (float):</u> the Nelson-Siegel decay (lambda) the curve was calibrated with.

**Returns:**

<u>float:</u> the share of scenario-periods with the short yield above the long yield, between 0 and 1.

**Raises:**

- <u>ValueError:</u> if `short_tenor` isn't strictly less than `long_tenor`.

</details>

#### negative_spread_frequency

The share of all simulated scenario-periods in which the curve is below zero at one maturity.

The curve factors are normally distributed with no floor, so negative values can occur. For a government curve a
negative yield is real if uncommon; for a credit spread curve (`CreditTermStructure`), where the short end is
roughly level plus slope, it is not economically meaningful, and a high share signals that the short-end spread
is too volatile for the use at hand.

The formula is as follows:

$$
\text{share} = \text{mean over cells of}\; 1 \left[y(\text{tenor}) < 0\right]
$$

Where y is `nelson_siegel_yield` in each scenario and period.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
negative_spread_frequency(
    level: np.ndarray,
    slope: np.ndarray,
    curvature: np.ndarray,
    tenor: float,
    decay: float,
) -> float
```

**Args:**

- <u>level (np.ndarray):</u> the simulated level paths.
- <u>slope (np.ndarray):</u> the simulated slope paths.
- <u>curvature (np.ndarray):</u> the simulated curvature paths.
- <u>tenor (float):</u> the maturity to check, in years.
- <u>decay (float):</u> the Nelson-Siegel decay (lambda) the curve was calibrated with.

**Returns:**

<u>float:</u> the share of scenario-periods below zero at `tenor`, between 0 and 1.

</details>

#### fit_nelson_siegel_factors

Summarise each date's yield curve by its Nelson-Siegel level, slope and curvature, giving three time series that
capture how the curve has moved.

On each date the observed yields across maturities are regressed on the fixed Nelson-Siegel loadings, as
Diebold and Li (2006) do: the level is close to the long yield, the slope to the short minus the long yield and
the curvature to the hump in the middle. These series are what the mean-reverting curve factors are fitted to,
and their changes set the curve's correlation with the other factors. With only three maturities the curve
passes through every observed yield exactly, so a bad print on one date goes straight into the factors; more
maturities give a smoother summary.

The formula is as follows:

$$
y_{t}(\tau_{j}) = L_{t} + S_{t} \cdot \operatorname{slope\_loading}(\tau_{j}) + C_{t} \cdot \operatorname{curvature\_loading}(\tau_{j}) + e_{t},\;\; \text{j}
$$

Solved by least squares across the tenors tau_j for each date t, as in Diebold and Li (2006, section 3), which
gives a time series of level, slope and curvature estimates.

**References:**

- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. <https://doi.org/10.1016/j.jeconom.2005.03.005>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_nelson_siegel_factors(
    yields_by_tenor: dict[float, pl.Series],
    decay: float,
    dates: pl.Series,
) -> pl.DataFrame
```

**Args:**

- <u>yields_by_tenor (dict[float, pl.Series]):</u> the yield history at each maturity (in years), over the same dates.
- <u>decay (float):</u> the Nelson-Siegel decay (lambda), per year.
- <u>dates (pl.Series):</u> the observation dates.

**Returns:**

<u>pl.DataFrame:</u> the `date`, `level`, `slope` and `curvature` on every date all maturities were quoted.

**Raises:**

- <u>ValueError:</u> if fewer than 3 maturities are given, the histories differ in length, or the fit fails.

</details>

#### step_curve_factor

Move one yield curve factor (level, slope or curvature) forward one step: part of its gap to the long-run value
closes, and a normally distributed shock is added.

This is the same mean reversion as the Hull-White short rate, applied to the curve's shape: a steep or inverted
curve drifts back toward its usual slope, and the level back toward its usual height, each at its own speed.
The shocks to the three factors are correlated with each other and with the rest of the model, so a scenario can
combine, for instance, falling rates with a steepening curve, as in an easing cycle. The step is the exact one,
so the frequency of the simulation does not change the distribution.

The formula is as follows:

$$
\beta(t + \text{dt}) = \theta + (\beta(t) - \theta) \cdot \exp(- a \cdot \text{dt}) + \sigma \cdot \sqrt{(1 - \exp(- 2 \cdot a \cdot \text{dt})) / (2 \cdot a)} \cdot z
$$

This is the univariate AR(1) per factor that Diebold and Li (2006, section 3) model and forecast the factors
with, here with coefficient exp(-a * dt).

**References:**

- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. <https://doi.org/10.1016/j.jeconom.2005.03.005>
- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. <https://doi.org/10.1016/0304-405x(77>)90016-2 Source of the exact transition used here.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_curve_factor(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: OUParams,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> the factor's current value in each scenario.
- <u>shock (np.ndarray &#124; float):</u> the random draw for this step, standard normal.
- <u>time_step (float):</u> the step length, in years.
- <u>params (OUParams):</u> the factor's calibrated speed, long-run value and volatility.

**Returns:**

<u>np.ndarray:</u> the factor's value one step later.

</details>

#### hjm_convexity

The convexity drift Phi(t, x) that no-arbitrage adds to a forward rate: how far the forward rate at maturity `x`
has risen by time `t` purely because rates are random.

Bond prices are convex in rates, so randomness on its own makes bonds worth more on average; without a
correction, a model would let an investor lock in a riskless profit across maturities. Heath, Jarrow and Morton
(1992) showed that the correction is fully determined by the volatilities, so nothing here is fitted. It is
zero today, grows with the horizon and the volatility, and is largest for long maturities and slow-fading
factors. It assumes the two factors' shocks have the calibrated correlation, which the simulation ensures.

The formula is as follows:

$$
\mu(t,\; T) = \sum_{i},\;\; j \rho_{ij} \cdot \sigma_{i}(T - t) \cdot \text{integral}_{t} ^{T} \sigma_{j}(u - t) \text{du}
$$

$$
\sigma_{i}(x) = \sigma_{i} \cdot \exp(- \kappa_{i} \cdot x)
$$

$$
\Phi(t,\; x) = \sum_{i},\;\; j \rho_{ij} \cdot \sigma_{i} \cdot \sigma_{j} / \kappa_{j} \cdot (K(\kappa_{i}) - K(\kappa_{i} + \kappa_{j}))
$$

$$
K(k) = \exp(- k \cdot x) \cdot (1 - \exp(- k \cdot t)) / k
$$

The first line is the Heath, Jarrow and Morton (1992) drift condition for correlated factors, their forward rate drift
restriction with the market price of risk set to 0; Phi(t, x) is that drift integrated from 0 to t at a fixed
time-to-maturity x = T - t.

**References:**

- Brigo, D., Mercurio, F. (2006). "Interest Rate Models: Theory and Practice" (2nd ed.), chapter 4: the G2++ phi(t) correction this term generalizes to an arbitrary tenor, not just t itself. Springer Finance. <https://doi.org/10.1007/978-3-540-34604-3>
- Heath, D., Jarrow, R., Morton, A. (1992). "Bond Pricing and the Term Structure of Interest Rates: A New Methodology for Contingent Claims Valuation." Econometrica, 60(1), 77-105. <https://doi.org/10.2307/2951677>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
hjm_convexity(
    elapsed_time: float | np.ndarray,
    tenor: float | np.ndarray,
    params: HjmParams,
) -> float | np.ndarray
```

**Args:**

- <u>elapsed_time (float &#124; np.ndarray):</u> t, years since the valuation date.
- <u>tenor (float &#124; np.ndarray):</u> x, the time to maturity in years (0 or more); an array broadcasts against `elapsed_time`.
- <u>params (HjmParams):</u> the calibrated two-factor model.

**Returns:**

<u>float &#124; np.ndarray:</u> Phi(t, x), one value per time and maturity given.

</details>

{% raw %}
#### hjm_forward_rate

The simulated forward rate at a given time to maturity, at a future date in a scenario.

It is built from three parts. First, today's forward curve read at the same calendar date, so with no shocks
the curve simply rolls down as time passes, which is what an arbitrage-free model requires. Second, the two
factors' shocks, each fading with maturity at its own rate: the slow factor moves the whole curve, the fast one
mostly the short end. Third, the convexity drift `hjm_convexity`. Today, with both factors at zero, it gives back
today's curve exactly.

The formula is as follows:

$$
f(t,\; t + x) = f_{\text{anchor}}(t + x) + \exp(- \kappa_{1} \cdot x) \cdot x_{1}(t) + \exp(- \kappa_{2} \cdot x) \cdot x_{2}(t) + \Phi(t,\; x)
$$

Where f_anchor is today's Nelson-Siegel forward curve and Phi(t, x) is `hjm_convexity`.

**References:**

- Heath, D., Jarrow, R., Morton, A. (1992). "Bond Pricing and the Term Structure of Interest Rates: A New Methodology for Contingent Claims Valuation." Econometrica, 60(1), 77-105. <https://doi.org/10.2307/2951677>
- Brigo, D., Mercurio, F. (2006). "Interest Rate Models: Theory and Practice" (2nd ed.), chapters 3-4. Springer Finance. <https://doi.org/10.1007/978-3-540-34604-3>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
hjm_forward_rate(
    state_1: float | np.ndarray,
    state_2: float | np.ndarray,
    tenor: float | np.ndarray,
    elapsed_time: float | np.ndarray,
    params: HjmParams,
) -> float | np.ndarray
```

**Args:**

- <u>state_1 (float &#124; np.ndarray):</u> x_1(t), the simulated `hjm_factor_1` value or paths.
- <u>state_2 (float &#124; np.ndarray):</u> x_2(t), the simulated `hjm_factor_2` value or paths.
- <u>tenor (float &#124; np.ndarray):</u> x, the time to maturity in years (0 gives the short rate); an array of maturities gives the whole curve at once.
- <u>elapsed_time (float &#124; np.ndarray):</u> t, years since the valuation date.
- <u>params (HjmParams):</u> the calibrated two-factor model.

**Returns:**

<u>float &#124; np.ndarray:</u> the forward rate, for each scenario, date and maturity given.

</details>
{% endraw %}

{% raw %}
#### hjm_zero_yield

The simulated zero-coupon yield to a given maturity, at a future date in a scenario: the continuously
compounded yield of a bond paying 1 at `tenor` years from then, the number to discount cash flows with or to
read the curve's slope from.

It is the average of `hjm_forward_rate` over the bond's life, in closed form. Each factor moves the yield by
B_i(m) times its value: close to one for short bonds and smaller for long ones, the more so for the fast-fading
second factor, so a shock to it moves short yields far more than long ones. Bond prices exp(-m * y) built from
these yields are consistent with each other at every maturity, which is what makes the curve arbitrage-free.

The formula is as follows:

$$
y(t,\; m) = (F_{\text{anchor}}(t + m) - F_{\text{anchor}}(t)) / m + \sum_{i} B_{i} (m) \cdot x_{i}(t) + (1 / m) \cdot \text{integral}_{0} ^{m} \Phi(t,\; u) \text{du}
$$

$$
B_{i}(m) = (1 - \exp(- \kappa_{i} \cdot m)) / (\kappa_{i} \cdot m)
$$

Where m is `tenor` and F_anchor is the integral of today's forward curve (`nelson_siegel_forward_integral`).

**References:**

- Brigo, D., Mercurio, F. (2006). "Interest Rate Models: Theory and Practice" (2nd ed.), chapters 3-4. Springer Finance. <https://doi.org/10.1007/978-3-540-34604-3>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
hjm_zero_yield(
    state_1: float | np.ndarray,
    state_2: float | np.ndarray,
    tenor: float,
    elapsed_time: float | np.ndarray,
    params: HjmParams,
) -> float | np.ndarray
```

**Args:**

- <u>state_1 (float &#124; np.ndarray):</u> x_1(t), the simulated `hjm_factor_1` value or paths.
- <u>state_2 (float &#124; np.ndarray):</u> x_2(t), the simulated `hjm_factor_2` value or paths.
- <u>tenor (float):</u> the bond's maturity, in years (above 0).
- <u>elapsed_time (float &#124; np.ndarray):</u> t, years since the valuation date.
- <u>params (HjmParams):</u> the calibrated two-factor model.

**Returns:**

<u>float &#124; np.ndarray:</u> the zero-coupon yield, for each scenario and date given.

**Raises:**

- <u>ValueError:</u> if `tenor` is not above 0.

</details>
{% endraw %}

#### step_hjm_factor

Move one HJM factor forward one step: it decays toward its centre at the rate its volatility fades with
maturity, and receives a normally distributed shock.

The pull is not a separate assumption: in this model the speed at which a factor's effect fades along the curve is the
same speed at which it mean-reverts over time, as in Vasicek (1977). Under the risk-neutral measure the centre is
zero, so the factors carry no term premium. A non-zero market price of risk moves the centre, adding the extra return
investors demand for holding long bonds, for a real-world view. The step is the exact one, so the simulation frequency
does not change the distribution.

The formula is as follows:

$$
x(t + \text{dt}) = m + (x(t) - m) \cdot \exp(- \kappa \cdot \text{dt}) + \sigma \cdot \sqrt{(1 - \exp(- 2 \cdot \kappa \cdot \text{dt})) / (2 \cdot \kappa)} \cdot z
$$

$$
m = \sigma \cdot \lambda / \kappa
$$

Where lambda is the market price of risk (0 under the risk-neutral measure, so m = 0) and z a standard normal draw.

**References:**

- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. <https://doi.org/10.1016/0304-405x(77>)90016-2

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_hjm_factor(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: HjmFactorParams,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> the factor's current value in each scenario.
- <u>shock (np.ndarray &#124; float):</u> the random draw for this step, standard normal.
- <u>time_step (float):</u> the step length, in years.
- <u>params (HjmFactorParams):</u> the factor's volatility, volatility decay and market price of risk.

**Returns:**

<u>np.ndarray:</u> the factor's value one step later.

</details>

#### fit_hjm_factors

Calibrate a 2-factor Gaussian HJM model from historical yields at several maturities.

No-arbitrage fixes the drift, so only each factor's volatility and decay and their correlation are fit. A
Nelson-Siegel curve is fit at every date, turned into forward rates on a dense tenor grid, and the two-factor
model whose covariance best matches the covariance of the forward-curve changes is chosen (a grid search, then
a least-squares polish).

The formula is as follows:

$$
C(x,\; y) = \sum_{i} \sum_{j} \rho_{ij} \cdot \sigma_{i} \cdot \sigma_{j} \cdot \exp(- \kappa_{i} \cdot x - \kappa_{j} \cdot y)
$$

$$
e = \operatorname{norm}(C - \Sigma) / \operatorname{norm}(\Sigma)
$$

Sigma is the historical covariance of the forward-curve changes at tenors x and y, rho_11 = rho_22 = 1, norm is
the Frobenius norm, and the decays are chosen to minimize e.

The fitted forward curve has rank 3 at most, so `covariance_fit_error` is the honest goodness-of-fit number;
`variance_share` is close to 100% almost by construction.

**References:**

- Brigo, D., Mercurio, F. (2006). "Interest Rate Models: Theory and Practice" (2nd ed.), chapters 3-4. Springer Finance. <https://doi.org/10.1007/978-3-540-34604-3>
- Litterman, R., Scheinkman, J. (1991). "Common Factors Affecting Bond Returns." The Journal of Fixed Income, 1(1), 54-61. <https://doi.org/10.3905/jfi.1991.692347>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_hjm_factors(
    yields_by_tenor: dict[float, pl.Series],
    dates: pl.Series,
    time_step: float,
    decay: float = 0.7308,
    kappa_bounds: tuple[float, float] = (MINIMUM_KAPPA, MAXIMUM_KAPPA),
) -> tuple[HjmParams, pl.DataFrame]
```

**Args:**

- <u>yields_by_tenor (dict[float, pl.Series]):</u> maturity (years) -> historical yield series at that maturity; same shape term_structure_model. fit_nelson_siegel_factors expects (at least 3 tenors).
- <u>dates (pl.Series):</u> one date per observation, aligned to `yields_by_tenor`.
- <u>time_step (float):</u> the time increment between observations, in years.
- <u>decay (float):</u> the Nelson-Siegel decay parameter (lambda) for both the historical cross-sectional fit and the anchor curve.
- <u>kappa_bounds (tuple[float, float]):</u> (min, max) search bounds for both factors' volatility_decay. The default floor (0.01, a ~70-year half-life) is an economic choice, not a numerical one: a near-zero kappa_1 makes the convexity term grow at long horizons.

**Returns:**

<u>tuple[HjmParams, pl.DataFrame]:</u> the calibrated model, and a "date", "hjm_factor_1", "hjm_factor_2" DataFrame of the two factors' cumulative projected shocks.

**Raises:**

- <u>ValueError:</u> if fewer than MINIMUM_OBSERVATIONS_HJM forward-curve changes are available after the underlying Nelson-Siegel fit.

</details>

#### fit_knw_pair

Fit how a nominal short rate r and inflation pi pull on each other: each is regressed by least squares on last
period's rate and last period's inflation, a bivariate VAR(1).

The cross terms carry the economics: a positive coefficient of the rate on lagged inflation is the central bank
leaning against inflation, and the inflation leg's coefficient on the lagged rate shows how tighter policy
feeds back into prices. Because both equations share the same regressors, fitting them one at a time is
already as efficient as a joint estimate.

The formula is as follows:

$$
x_{t} - m_{x} = \phi_{x} \cdot (x_{t-1} - m_{x}) + \phi_{y} \cdot (y_{t-1} - m_{y}) + u_{t}
$$

$$
c_{x} = m_{x} - \phi_{x} \cdot m_{x} - \phi_{y} \cdot m_{y}
$$

$$
\sigma_{x} = \sqrt{\operatorname{sum}(u_{t} ^{2}) / (T - 3)}
$$

Where (x, y) is (r, pi) for the rate leg and (pi, r) for the inflation leg, m the sample average of each series and T
the number of transitions. The long-run levels the pair settles at are then the historical averages, a VAR fitted on
mean-adjusted data, the estimator of Lutkepohl (2005, section 3.3) on least squares with mean-adjusted data, see
Lutkepohl (2005, section 3.3.3) where the process mean is unknown. The alternative, an intercept fitted freely in each
regression, puts the long-run levels at (I - Phi)^-1 * c, which for a pair this persistent amplifies where the sample
happens to start and end: on US data since 1990 it puts the long-run rate 0.5 percentage points below the rate's own
average and the long-run real rate below zero. The fit is accepted only when the 2x2 coefficient matrix Phi has
spectral radius below 1, the condition for the joint system to be stationary: only then does a shock fade and the pair
settle at long-run levels, rather than drift off. Only dates both histories cover are used.

**References:**

- Koijen, R.S.J., Nijman, T.E., Werker, B.J.M. (2010). "When Can Life Cycle Investors Benefit from Time-Varying Bond Risk Premia?" The Review of Financial Studies, 23(2), 741-780. The model CP2022 extends. <https://doi.org/10.1093/rfs/hhp058>
- Commissie Parameters (2022). "Technical Appendix: Specification of the CP2022 Model." Eq. 52, the discrete-time recursion fit here at zero stochastic volatility. <https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix>
- Dai, Q., Singleton, K.J. (2000). "Specification Analysis of Affine Term Structure Models." Journal of Finance, 55(5), 1943-1978. Why a matrix (not scalar) mean reversion is standard here. <https://doi.org/10.1111/0022-1082.00278>
- Lutkepohl, H. (2005). "New Introduction to Multiple Time Series Analysis." Springer. The reduced-form VAR(1) OLS estimator (section 3.2), its mean-adjusted form (section 3.3) and its stability condition. <https://doi.org/10.1007/978-3-540-27752-1>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_knw_pair(
    interest_rate: pl.Series,
    interest_rate_dates: pl.Series,
    inflation: pl.Series,
    inflation_dates: pl.Series,
    mean_estimate: Literal['sample', 'regression'] = 'sample',
) -> tuple[KnwParams, KnwParams]
```

**Args:**

- <u>interest_rate (pl.Series):</u> the historical nominal short rate, as decimals.
- <u>interest_rate_dates (pl.Series):</u> the dates of those observations.
- <u>inflation (pl.Series):</u> the historical inflation rate, as decimals, at the same frequency as the rate.
- <u>inflation_dates (pl.Series):</u> the dates of those observations.
- <u>mean_estimate (str):</u> "sample" (default) sets the long-run levels to the historical averages; "regression" fits a free intercept per equation instead.

**Returns:**

<u>tuple[KnwParams, KnwParams]:</u> (interest_rate_params, inflation_params).

**Raises:**

- <u>ValueError:</u> if fewer than 5 dates overlap, or Phi's spectral radius is 1 or more (the pair does not settle at this frequency).

</details>

#### step_knw_process

Move one leg of the rate and inflation pair one period ahead: a share of its own last value, a share of the
other leg's last value, a constant and a normal shock.

Both legs react to where the other stood at the start of the period, not to where it moves during it, so a
rate move shows up in inflation one period later and vice versa. The shocks are normal, so either leg can go
negative. The shocks are correlated with those of every other factor through the run's correlation matrix.

The formula is as follows:

$$
x_{t} = c + \phi_{x} \cdot x_{t-1} + \phi_{y} \cdot y_{t-1} + \sigma \cdot z_{t}
$$

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_knw_process(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: KnwParams,
    other_current_value: np.ndarray | float,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> this leg's value last period, x_t-1.
- <u>shock (np.ndarray &#124; float):</u> the standard normal shock z_t.
- <u>time_step (float):</u> unused: the coefficients already hold per period of the data.
- <u>params (KnwParams):</u> the calibrated intercept, own and cross coefficients and volatility.
- <u>other_current_value (np.ndarray &#124; float):</u> the other leg's value last period, y_t-1.

**Returns:**

<u>np.ndarray:</u> this leg's value x_t.

</details>

#### compute_v_proxy

Estimate the hidden turbulence factor v from history: how large the rate and inflation surprises have been
lately.

v is not a market price. DNB's CP2022 calibration takes it as given: v_t and the yields of one nominal and one real
bond are treated as observed without measurement error (Commissie Parameters (2022, section 4)). Without that series,
here it is the average squared surprise of a constant-volatility rate and inflation fit over the past year. When both
legs have recently surprised by a lot, v is high; in quiet spells it is low. The rate and inflation legs, the equity
leg and the risk-neutral market price of risk are all fitted against this one estimate, so they agree on when markets
were turbulent.

The formula is as follows:

$$
e_{t} = u_{t} ^{2} + w_{t} ^{2}
$$

$$
V_{t} = (1 / W) \cdot \operatorname{sum}(e_{s} \;\text{for}\; s = t - W + 1 \;\text{to}\; t)
$$

Where u and w are the rate and inflation surprises of the constant-volatility fit and W the window, one year of
observations. Each date is paired with the window ending one period earlier, so a surprise never explains itself.

The window follows Engle's (1982, section 9, p. 1002) model of UK inflation variance: a test for fourth-order
linear ARCH gives a highly significant chi-squared statistic of 15.2 with 4 degrees of freedom, and the fitted
variance is h_t = a_0 + a_1(0.4 e_t-1^2 + 0.3 e_t-2^2 + 0.2 e_t-3^2 + 0.1 e_t-4^2) (eq. 38) on quarterly data:
the last four quarters, one year. The window keeps that year at the data's frequency, 12 months on monthly data and
one observation on yearly data. Equal weights and adding the two legs' surprises are judgements: they keep one
turbulence measure for both legs.

**References:**

- Engle, R.F. (1982). "Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation." Econometrica, 50(4), 987-1007. <https://doi.org/10.2307/1912773>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
compute_v_proxy(
    interest_rate: pl.Series,
    interest_rate_dates: pl.Series,
    inflation: pl.Series,
    inflation_dates: pl.Series,
    window: int | None = None,
) -> pl.DataFrame
```

**Args:**

- <u>interest_rate (pl.Series):</u> the historical nominal short rate, as decimals.
- <u>interest_rate_dates (pl.Series):</u> the dates of those observations.
- <u>inflation (pl.Series):</u> the historical inflation rate, as decimals, at the same frequency as the rate.
- <u>inflation_dates (pl.Series):</u> the dates of those observations.
- <u>window (int &#124; None):</u> the number of observations averaged; None (the default) uses one year at the data's spacing, 4 for quarterly data.

**Returns:**

<u>pl.DataFrame:</u> one row per date after the window: "date", last and current rate and inflation ("r_lag", "pi_lag", "r_next", "pi_next") and "v_proxy", the turbulence estimate V_t-1.

**Raises:**

- <u>ValueError:</u> if a series and its dates differ in length, the window is below 1, or too little overlapping history remains (the window plus 7 dates: 11 for quarterly data).

</details>

#### fit_knw_sv_triple

Fit the rate and inflation pair together with the turbulence factor v that scales both their volatilities.

v follows the CIR process of [Cox, Ingersoll and Ross (1985)](https://doi.org/10.2307/1911242): it is pulled back to a
normal level at speed kappa, never goes negative, and swings more the higher it is, so a turbulent spell is
followed by gradual calm. Each leg then keeps the two-way coupling of `Knw` and adds two links to v: v can
shift its expected next value (k_v) and widen its swings (g_1). A positive g_1 is what gives the scenarios
volatility clustering and fatter tails than a constant-volatility model.

The fit runs in three stages: v is estimated from recent surprises (`compute_v_proxy`) and a CIR process fitted to
it; each leg is regressed on last period's v, rate and inflation; and each leg's squared surprises are regressed
on last period's v.

The formula is as follows:

$$
\text{dv} = \kappa \cdot (\theta - v) \cdot \text{dt} + \omega \cdot \sqrt{v} \cdot \text{dW},\;\; \text{fit to V}
$$

$$
x_{t} = c + k_{v} \cdot V_{t-1} + \phi_{x} \cdot x_{t-1} + \phi_{y} \cdot y_{t-1} + u_{t}
$$

$$
u_{t} ^{2} = g_{0} + g_{1} \cdot V_{t-1} + e_{t}
$$

Where x and y are the two legs; g_0 and g_1 are floored at 0 since a small sample can fit them negative. The
rate and inflation block of the coefficient matrix must have spectral radius below 1, so the pair settles at
long-run levels; v mean-reverts by construction.

The rolling windows overlap, which biases v's CIR fit downward, but only noticeably for histories of
thousands of observations.

**References:**

- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). "A Theory of the Term Structure of Interest Rates." Econometrica, 53(2), 385-407. v's process family. <https://doi.org/10.2307/1911242>
- Commissie Parameters (2022). "Technical Appendix: Specification of the CP2022 Model." Eq. 2-3 (the K matrix's block-triangular structure the stationarity check relies on) and eq. 52 (the discrete-time recursion). <https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix>
- Koijen, R.S.J., Nijman, T.E., Werker, B.J.M. (2010). "When Can Life Cycle Investors Benefit from Time-Varying Bond Risk Premia?" The Review of Financial Studies, 23(2), 741-780. <https://doi.org/10.1093/rfs/hhp058>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_knw_sv_triple(
    interest_rate: pl.Series,
    interest_rate_dates: pl.Series,
    inflation: pl.Series,
    inflation_dates: pl.Series,
    time_step: float,
    variance_window: int | None = None,
) -> tuple[OUParams, KnwSvLegParams, KnwSvLegParams]
```

**Args:**

- <u>interest_rate (pl.Series):</u> the historical nominal short rate, as decimals.
- <u>interest_rate_dates (pl.Series):</u> the dates of those observations.
- <u>inflation (pl.Series):</u> the historical inflation rate, as decimals, at the same frequency as the rate.
- <u>inflation_dates (pl.Series):</u> the dates of those observations.
- <u>time_step (float):</u> the years between observations (0.25 for quarterly); v is a continuous-time process.
- <u>variance_window (int &#124; None):</u> the observations behind each v estimate; None (the default) uses one year.

**Returns:**

<u>tuple[OUParams, KnwSvLegParams, KnwSvLegParams]:</u> (v_params, interest_rate_params, inflation_params), with v a CIR process.

**Raises:**

- <u>ValueError:</u> if too little overlapping history remains (one year plus 7 dates), or the rate and inflation block has spectral radius 1 or more.

</details>

{% raw %}
#### step_knw_sv_v

Move the shared turbulence factor v one period ahead: pulled back toward its normal level, never below zero.

v follows a CIR process, the variance process of [Heston (1993)](https://doi.org/10.1093/rfs/6.2.327): a spike
in turbulence fades at speed kappa, and v swings more the higher it is. Simulating such a process naively can
push it below zero or bias its average; Andersen's (2008) Quadratic-Exponential scheme avoids both by matching
the mean and variance of the exact transition. Far from zero the next value is a scaled squared normal draw;
near zero it is either exactly zero or an exponential draw, which is how a calm market can stay very calm.

The formula is as follows:

$$
d = \exp(- \kappa \cdot \text{dt})
$$

$$
m = \theta + (v_{t} - \theta) \cdot d
$$

$$
s ^{2} = v_{t} \cdot \omega ^{2} \cdot d \cdot (1 - d) / \kappa + \theta \cdot \omega ^{2} \cdot (1 - d) ^{2} / (2 \cdot \kappa)
$$

$$
\psi = s ^{2} / m ^{2}
$$

$$
b ^{2} = 2 / \psi - 1 + \sqrt{2 / \psi} \cdot \sqrt{2 / \psi - 1}
$$

$$
v_{\text{next}} = m / (1 + b ^{2}) \cdot (b + z) ^{2},\;\; \text{if}\; \psi \leq 1.5
$$

$$
p = (\psi - 1) / (\psi + 1)
$$

$$
v_{\text{next}} = \max(\ln((1 - p) / (1 - u)),\; 0) \cdot m \cdot (\psi + 1) / 2,\;\; \text{if psi > 1.5}
$$

Where z is a standard normal draw and u a uniform draw, so u <= p lands on the point mass at 0.

**References:**

- Andersen, L. (2008). "Simple and Efficient Simulation of the Heston Stochastic Volatility Model." Journal of Computational Finance, 11(3), 1-42. Moments m and s^2: eq. 17-19. Quadratic branch: eq. 27-28. Exponential branch: eq. 29-30. Switching rule psi_c = 1.5: sec 3.2.3. <https://doi.org/10.21314/jcf.2008.189>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_knw_sv_v(
    v_current: np.ndarray | float,
    standard_normal_draw: np.ndarray | float,
    uniform_draw: np.ndarray | float,
    time_step: float,
    params: OUParams,
) -> np.ndarray
```

**Args:**

- <u>v_current (np.ndarray):</u> v_t in each scenario.
- <u>standard_normal_draw (np.ndarray):</u> the normal draws z, used far from zero.
- <u>uniform_draw (np.ndarray):</u> the uniform draws u, used near zero.
- <u>time_step (float):</u> dt, in years.
- <u>params (OUParams):</u> v's CIR parameters (mean_reversion_speed=kappa, long_run_mean=theta, volatility=omega).

**Returns:**

<u>np.ndarray:</u> v_next in each scenario, never negative.

</details>
{% endraw %}

{% raw %}
#### step_knw_sv_leg

Move the rate or inflation leg one period ahead: the `Knw` coupling of the two legs, plus a shift and a shock
size that both depend on the turbulence factor v.

When v is high, the leg's shock is larger, so rates and inflation swing harder together in turbulent spells
and settle in calm ones. The leg reacts to where the other leg and v stood at the start of the period. The
shocks are normal, so rates and inflation can go negative.

The formula is as follows:

$$
x_{t} = c + k_{v} \cdot v_{t-1} + \phi_{x} \cdot x_{t-1} + \phi_{y} \cdot y_{t-1} + \sqrt{g_{0} + g_{1} \cdot v_{t-1}} \cdot z_{t}
$$

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_knw_sv_leg(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: KnwSvLegParams,
    other_current_value: np.ndarray | float,
    v_current_value: np.ndarray | float,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> this leg's value last period, x_t-1.
- <u>shock (np.ndarray &#124; float):</u> the standard normal shock z_t.
- <u>time_step (float):</u> unused: the coefficients already hold per period of the data.
- <u>params (KnwSvLegParams):</u> the calibrated intercept, coupling coefficients and variance parameters.
- <u>other_current_value (np.ndarray &#124; float):</u> the other leg's value last period, y_t-1.
- <u>v_current_value (np.ndarray &#124; float):</u> the turbulence factor last period, v_t-1.

**Returns:**

<u>np.ndarray:</u> this leg's value x_t.

</details>
{% endraw %}

#### fit_knw_sv_equity_leg

Fit an equity index whose volatility rises and falls with the rate and inflation pair's turbulence factor v.

The risk premium is the average log return above the short rate, corrected for the volatility drag (half the
variance). The variance is then regressed on last period's v: a positive slope means equity swings grew when
rates and inflation were turbulent, so in the scenarios equity stress and rate stress arrive together. This is
the equity row of DNB's CP2022 model, fitted on price history only, where DNB also uses option prices.

The formula is as follows:

$$
x_{t} = \ln(S_{t} / S_{t-1}) - r_{t-1} \cdot \text{dt}
$$

$$
\mu = \operatorname{mean}(x) + 0.5 \cdot \operatorname{var}(x)
$$

$$
(x_{t} - \operatorname{mean}(x)) ^{2} = g_{0} + g_{1} \cdot V_{t-1} + e_{t}
$$

Where r is the short rate, V the turbulence estimate of `compute_v_proxy`, and g_0 and g_1 are floored at 0 so a
variance is never negative.

**References:**

- Commissie Parameters (2022). "Technical Appendix: Specification of the CP2022 Model." Eq. 4-5 (the equity row fit here) and eq. 25 (the derivatives constraint not applied). <https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_knw_sv_equity_leg(
    equity_prices: pl.Series,
    equity_dates: pl.Series,
    v_proxy: pl.DataFrame,
    time_step: float,
) -> KnwSvEquityParams
```

**Args:**

- <u>equity_prices (pl.Series):</u> the historical index levels (not returns).
- <u>equity_dates (pl.Series):</u> the dates of those levels.
- <u>v_proxy (pl.DataFrame):</u> the pair's turbulence estimate from `compute_v_proxy`, with the short rate it lines up with.
- <u>time_step (float):</u> dt, the years between observations, matching the pair's frequency.

**Returns:**

<u>KnwSvEquityParams:</u> the risk premium, base variance, sensitivity to v and the last price.

**Raises:**

- <u>ValueError:</u> if the prices and dates differ in length, or fewer than 6 dates overlap with the pair.

</details>

{% raw %}
#### step_knw_sv_equity

Move the equity index one period ahead: it earns last period's short rate plus the risk premium, minus the
volatility drag, plus a shock whose size is set by the turbulence factor v.

When v is high the index swings harder, in both directions, at the same time as rates and inflation do; when v
is low the market is calm. Prices stay positive, and the return over the short rate is the risk premium on
average.

The formula is as follows:

$$
h_{t-1} = \max(g_{0} + g_{1} \cdot v_{t-1},\; 0)
$$

$$
S_{t} = S_{t-1} \cdot \exp(r_{t-1} \cdot \text{dt} + \mu - 0.5 \cdot h_{t-1} + \sqrt{h_{t-1}} \cdot z_{t})
$$

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_knw_sv_equity(
    current_level: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: KnwSvEquityParams,
    rate_current_value: np.ndarray | float,
    v_current_value: np.ndarray | float,
) -> np.ndarray
```

**Args:**

- <u>current_level (np.ndarray &#124; float):</u> the index level S_t-1.
- <u>shock (np.ndarray &#124; float):</u> the standard normal shock z_t.
- <u>time_step (float):</u> dt, in years; the short rate is annual, the premium and variance per period.
- <u>params (KnwSvEquityParams):</u> the calibrated risk premium and variance parameters.
- <u>rate_current_value (np.ndarray &#124; float):</u> the pair's short rate last period, r_t-1.
- <u>v_current_value (np.ndarray &#124; float):</u> the turbulence factor last period, v_t-1.

**Returns:**

<u>np.ndarray:</u> the index level S_t.

</details>
{% endraw %}

#### apply_completely_affine_mpr

Turn the real-world (P) parameters of a rate, inflation and turbulence model into risk-neutral (Q) ones, given
the market price of risk.

The market price of risk is the extra expected return investors demand per unit of each risk. Moving to Q
removes it from the drift: rates and inflation are expected lower or higher by their premium, and the
turbulence factor `v` reverts at a different speed toward a different level. A negative `lambda_v` makes `v`
revert more slowly toward a higher level, so the market prices in more turbulence than history shows. The
volatilities stay the same, as Girsanov's theorem requires, and so do the coupling between the legs and today's
values, so Q scenarios are simulated exactly like P scenarios with these parameters.

The formula is as follows:

$$
\kappa ^{Q} = \kappa + \lambda_{v}
$$

$$
\theta ^{Q} = \kappa \cdot \theta / \kappa ^{Q}
$$

$$
c ^{Q} = c - \lambda_{0}
$$

$$
k_{v} ^{Q} = k_{v} - \lambda_{1}
$$

Where kappa and theta are `v`'s real-world speed and level, c and k_v a leg's intercept and coupling to `v`, and
lambda_v, lambda_0 and lambda_1 the market prices of risk of `v` and of the leg (constant and per unit of `v`).

**References:**

- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). "A Theory of the Term Structure of Interest Rates." Econometrica, 53(2), 385-407. The proportional risk premium applied to v. <https://doi.org/10.2307/1911242>
- Duffie, D., Kan, R. (1996). "A Yield-Factor Model of Interest Rates." Mathematical Finance, 6(4), 379-406. The completely-affine market price of risk applied to r and pi. <https://doi.org/10.1111/j.1467-9965.1996.tb00123.x>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
apply_completely_affine_mpr(
    v_params: OUParams,
    interest_rate_params: KnwSvLegParams,
    inflation_params: KnwSvLegParams,
    mpr: CompletelyAffineMprParams,
) -> tuple[OUParams, KnwSvLegParams, KnwSvLegParams]
```

**Args:**

- <u>v_params (OUParams):</u> `v`'s real-world CIR parameters.
- <u>interest_rate_params (KnwSvLegParams):</u> the rate leg's real-world parameters.
- <u>inflation_params (KnwSvLegParams):</u> the inflation leg's real-world parameters.
- <u>mpr (CompletelyAffineMprParams):</u> the market price of risk to apply.

**Returns:**

<u>tuple[OUParams, KnwSvLegParams, KnwSvLegParams]:</u> (v_params_q, interest_rate_params_q, inflation_params_q).

**Raises:**

- <u>ValueError:</u> if kappa^Q is zero or negative (`v` would no longer mean-revert under Q).

</details>

{% raw %}
#### compute_stochastic_deflator

Build a stochastic deflator for a real-world run: a per-scenario discount factor that prices cash flows at
market value, so one set of real-world scenarios serves both projection and valuation.

The deflator discounts at the simulated short rate and then reweights each scenario by how much the market
fears it: scenarios whose shocks investors demand a premium for get more weight. The weight is the Girsanov
density of the fitted market price of risk, as in
[Cheng and Planchet (2019)](https://www.journaleska.com/index.php/bmi/article/view/9378). The
average deflator at T then equals the model's risk-neutral zero-coupon bond price for T, and the average of
deflator times cash flow is the cash flow's market value.

The formula is as follows:

$$
\mu_{t-1} = c + k_{v} \cdot v_{t-1} + \phi_{x} \cdot x_{t-1} + \phi_{y} \cdot y_{t-1}
$$

$$
\sigma_{t-1} = \sqrt{g_{0} + g_{1} \cdot v_{t-1}}
$$

$$
z_{t} = (x_{t} - \mu_{t-1}) / \sigma_{t-1}
$$

$$
\lambda_{t-1} = (\lambda_{0} + \lambda_{1} \cdot v_{t-1}) / \sigma_{t-1}
$$

$$
\ln(D_{t}) = \ln(D_{t-1}) - r_{t-1} \cdot \text{dt} - \lambda_{t-1} ^{T} \cdot R ^{-1} \cdot z_{t} - 0.5 \cdot \lambda_{t-1} ^{T} \cdot R ^{-1} \cdot \lambda_{t-1}
$$

Where x is each leg, y the other one, z_t the pair of real-world shocks read back from the simulated path,
lambda_t-1 the pair of prices of risk and R the 2x2 correlation matrix of the rate and inflation shocks (rho
off the diagonal). The correlation matters: the scenarios draw correlated shocks, and a weight that treated them
as independent would no longer average to the bond price. `v`'s own shock is not reweighted, so the deflator is
accurate only when `v`'s risk premium is small relative to its mean-reversion speed; `v` still drives both legs'
drift and variance.

**References:**

- Cheng, P.-K., Planchet, F. (2019). "Stochastic Deflator for an Economic Scenario Generator with Five Factors." Bankers, Markets & Investors, 157. <https://www.journaleska.com/index.php/bmi/article/view/9378>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
compute_stochastic_deflator(
    v_path: np.ndarray,
    interest_rate_path: np.ndarray,
    inflation_path: np.ndarray,
    interest_rate_params: KnwSvLegParams,
    inflation_params: KnwSvLegParams,
    mpr: CompletelyAffineMprParams,
    time_step: float,
    shock_correlation: float = 0.0,
) -> np.ndarray
```

**Args:**

- <u>v_path (np.ndarray):</u> the simulated turbulence factor, one row per scenario and one column per date.
- <u>interest_rate_path (np.ndarray):</u> the simulated short rate on the same scenarios and dates.
- <u>inflation_path (np.ndarray):</u> the simulated inflation on the same scenarios and dates.
- <u>interest_rate_params (KnwSvLegParams):</u> the real-world rate parameters the scenarios were simulated with.
- <u>inflation_params (KnwSvLegParams):</u> the real-world inflation parameters.
- <u>mpr (CompletelyAffineMprParams):</u> the fitted market price of risk (see `calibrate_completely_affine_mpr`).
- <u>time_step (float):</u> dt, in years.
- <u>shock_correlation (float):</u> rho, the correlation of the rate and inflation shocks the scenarios were simulated with. Defaults to 0.0.

**Returns:**

<u>np.ndarray:</u> D_t per scenario and date, with D_0 = 1 in every scenario.

**Raises:**

- <u>ValueError:</u> if a leg's volatility is exactly 0 at some step, so its shock cannot be read back, or the correlation is not strictly between -1 and 1.

</details>
{% endraw %}

#### zero_coupon_bond_recursion

Price risk-neutral zero-coupon bonds at every maturity in closed form, as an exponential of a linear function of
today's turbulence, short rate and inflation.

Because the model is affine, as in [Duffie and Kan (1996)](https://doi.org/10.1111/j.1467-9965.1996.tb00123.x), the
price of a bond maturing n periods out is P(n) = exp(A(n) + Bv(n) * v + Br(n) * r + Bpi(n) * pi). The
coefficients follow from one period of discounting at the short rate and the risk-neutral expectation of next
period's bond price, so they build up maturity by maturity without simulation. Br says how much a bond's log
price falls when the short rate rises, the model's duration; Bpi carries inflation's feed into future rates;
Bv says how turbulence moves prices, through expected rates, convexity and the risk premium.

The formula is as follows:

$$
\operatorname{Q0}(n) = 0.5 \cdot (\operatorname{Br}(n) ^{2} \cdot g_{0r} + \operatorname{Bpi}(n) ^{2} \cdot g_{0 \pi}) + \rho \cdot \operatorname{Br}(n) \cdot \operatorname{Bpi}(n) \cdot h_{0}
$$

$$
\operatorname{Q1}(n) = 0.5 \cdot (\operatorname{Br}(n) ^{2} \cdot g_{1r} + \operatorname{Bpi}(n) ^{2} \cdot g_{1 \pi}) + \rho \cdot \operatorname{Br}(n) \cdot \operatorname{Bpi}(n) \cdot h_{1}
$$

$$
A(n + 1) = A(n) + C(\operatorname{Bv}(n)) + \operatorname{Br}(n) \cdot c_{r} + \operatorname{Bpi}(n) \cdot c_{\pi} + \operatorname{Q0}(n)
$$

$$
\operatorname{Bv}(n + 1) = L(\operatorname{Bv}(n)) + \operatorname{Br}(n) \cdot k_{vr} + \operatorname{Bpi}(n) \cdot k_{v \pi} + \operatorname{Q1}(n)
$$

$$
\operatorname{Br}(n + 1) = \operatorname{Br}(n) \cdot \phi_{rr} + \operatorname{Bpi}(n) \cdot \phi_{\pi r} - \text{dt}
$$

$$
\operatorname{Bpi}(n + 1) = \operatorname{Br}(n) \cdot \phi_{r \pi} + \operatorname{Bpi}(n) \cdot \phi_{\pi \pi}
$$

Where A(0) = Bv(0) = Br(0) = Bpi(0) = 0, L and C come from the closed-form expectation of the CIR process `v`
of [Cox, Ingersoll and Ross (1985)](https://doi.org/10.2307/1911242), the r and pi suffixes name the leg, phi_pir is
the inflation leg's coefficient on r and phi_rpi the rate leg's on pi. Q0 and Q1 are the convexity of the bond
price: half the variance of next period's log price, the rate-inflation covariance included.

rho is the correlation of the rate and inflation shocks, the same one the scenarios draw with, so model prices
and discounting along the simulated paths agree. Their covariance rho * sqrt(g_0r + g_1r * v) *
sqrt(g_0pi + g_1pi * v) is not linear in `v` unless both legs load on `v` in the same proportion, so it is
replaced by its tangent h_0 + h_1 * v at `v`'s risk-neutral long-run level: exact at constant volatility and for
proportional loadings, and off only to second order in `v`'s distance from that level otherwise. `v`'s own shock
is independent of both legs, as in the scenarios.

**References:**

- Duffie, D., Kan, R. (1996). "A Yield-Factor Model of Interest Rates." Mathematical Finance, 6(4), 379-406. <https://doi.org/10.1111/j.1467-9965.1996.tb00123.x>
- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). "A Theory of the Term Structure of Interest Rates." Econometrica, 53(2), 385-407. <https://doi.org/10.2307/1911242>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
zero_coupon_bond_recursion(
    v_params_q: OUParams,
    interest_rate_params_q: KnwSvLegParams,
    inflation_params_q: KnwSvLegParams,
    time_step: float,
    n_periods: int,
    shock_correlation: float = 0.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
```

**Args:**

- <u>v_params_q (OUParams):</u> `v`'s risk-neutral CIR parameters (see `apply_completely_affine_mpr`).
- <u>interest_rate_params_q (KnwSvLegParams):</u> the rate leg's risk-neutral parameters.
- <u>inflation_params_q (KnwSvLegParams):</u> the inflation leg's risk-neutral parameters.
- <u>time_step (float):</u> dt, years per period.
- <u>n_periods (int):</u> the longest maturity, in periods.
- <u>shock_correlation (float):</u> rho, the correlation of the rate and inflation shocks. Defaults to 0.0.

**Returns:**

<u>tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:</u> (A, Bv, Br, Bpi), one value per maturity from 0 to `n_periods` periods.

**Raises:**

- <u>ValueError:</u> if the correlation is not strictly between -1 and 1.

</details>

#### zero_coupon_yield

The continuously compounded zero-coupon yield n periods to maturity, given today's turbulence, short rate and
inflation, from the bond price coefficients of `zero_coupon_bond_recursion`.

Because the yield is linear in the state, a whole yield curve moves with the short rate, inflation and `v` in a
fixed pattern: a higher short rate lifts short yields most, as it mean-reverts before long bonds mature, and
inflation moves the curve through its feed into future rates.

The formula is as follows:

$$
y(n) = - (A(n) + \operatorname{Bv}(n) \cdot v + \operatorname{Br}(n) \cdot r + \operatorname{Bpi}(n) \cdot \pi) / (n \cdot \text{dt})
$$

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
zero_coupon_yield(
    v: float | np.ndarray,
    interest_rate: float | np.ndarray,
    inflation: float | np.ndarray,
    a: np.ndarray,
    bv: np.ndarray,
    br: np.ndarray,
    bpi: np.ndarray,
    n_periods: int,
    time_step: float,
) -> float | np.ndarray
```

**Args:**

- <u>v (float &#124; np.ndarray):</u> the turbulence factor, in one or many scenarios.
- <u>interest_rate (float &#124; np.ndarray):</u> the short rate.
- <u>inflation (float &#124; np.ndarray):</u> inflation.
- <u>a (np.ndarray):</u> the A coefficients by maturity.
- <u>bv (np.ndarray):</u> the Bv coefficients by maturity.
- <u>br (np.ndarray):</u> the Br coefficients by maturity.
- <u>bpi (np.ndarray):</u> the Bpi coefficients by maturity.
- <u>n_periods (int):</u> the maturity n, in periods, at least 1.
- <u>time_step (float):</u> dt, years per period.

**Returns:**

<u>float &#124; np.ndarray:</u> the yield, as a decimal, per scenario.

**Raises:**

- <u>ValueError:</u> if `n_periods` is not at least 1.

</details>

{% raw %}
#### calibrate_completely_affine_mpr

Fit the market price of risk so the model's yield curve matches the observed one across history.

A real-world rate model fitted on the short rate alone says nothing about term premiums: why a 10-year yield
sits above the expected path of short rates. The market price of risk fills that gap. Its five parameters are
chosen so that, on every historical date, the model's yields at the observed maturities are as close as
possible to the observed yields, given that date's rate, inflation and turbulence. The premiums are completely
affine, as in [Duffie and Kan (1996)](https://doi.org/10.1111/j.1467-9965.1996.tb00123.x): a constant plus a part
proportional to `v`, so investors can demand more compensation in turbulent markets. `v` is not observed, so
its history is the same estimate the real-world fit used (`compute_v_proxy`). With a nominal curve only, the
inflation premiums are weakly identified.

The formula is as follows:

$$
\text{loss} = \operatorname{sum}((y_{\text{model}} - y_{\text{observed}}) ^{2}),\;\; \text{over dates t and tenors n}
$$

Where the five lambdas minimize the loss and y_model is `zero_coupon_yield` under the risk-neutral parameters
from `apply_completely_affine_mpr`. lambda_v is bounded so `v` still mean-reverts under Q.

**References:**

- Duffie, D., Kan, R. (1996). "A Yield-Factor Model of Interest Rates." Mathematical Finance, 6(4), 379-406. <https://doi.org/10.1111/j.1467-9965.1996.tb00123.x>
- Diebold, F.X., Li, C. (2006). "Forecasting the term structure of government bond yields." Journal of Econometrics, 130(2), 337-364. The four-tenor Treasury panel calibrated against. <https://doi.org/10.1016/j.jeconom.2005.03.005>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_completely_affine_mpr(
    v_params: OUParams,
    interest_rate_params: KnwSvLegParams,
    inflation_params: KnwSvLegParams,
    time_step: float,
    state_dates: pl.Series,
    v_series: pl.Series,
    interest_rate_series: pl.Series,
    inflation_series: pl.Series,
    yield_dates: pl.Series,
    yields_by_tenor: dict[float, pl.Series],
    shock_correlation: float = 0.0,
) -> CompletelyAffineMprParams
```

**Args:**

- <u>v_params (OUParams):</u> `v`'s calibrated real-world CIR parameters.
- <u>interest_rate_params (KnwSvLegParams):</u> the rate leg's calibrated real-world parameters.
- <u>inflation_params (KnwSvLegParams):</u> the inflation leg's calibrated real-world parameters.
- <u>time_step (float):</u> the years per period; every maturity must be a whole number of periods.
- <u>state_dates (pl.Series):</u> the dates of the rate, inflation and `v` history.
- <u>v_series (pl.Series):</u> the estimated `v` on each of those dates.
- <u>interest_rate_series (pl.Series):</u> the short rate on each of those dates.
- <u>inflation_series (pl.Series):</u> inflation on each of those dates.
- <u>yield_dates (pl.Series):</u> the dates of the observed yield curve.
- <u>yields_by_tenor (dict[float, pl.Series]):</u> the observed yield history per maturity in years.
- <u>shock_correlation (float):</u> the correlation of the rate and inflation shocks, as in the scenarios. Defaults to 0.0.

**Returns:**

<u>CompletelyAffineMprParams:</u> the calibrated market price of risk.

**Raises:**

- <u>ValueError:</u> if a maturity is not a whole number of periods, or fewer than 10 dates are covered by both the state history and the yield curve.

</details>
{% endraw %}
