## Reference

The reference is generated from the docstrings in the package, so it says what `help(...)` says in Python: what each class and function does, a worked example with real output where the docstring has one, and the arguments and return value folded underneath.

The factor and model classes are reached through a `Scenarios` object, after `scenarios = Scenarios.from_profiles(...)`:

```python
scenarios.inflation          # Inflation
scenarios.unemployment       # Unemployment
scenarios.mortality          # Mortality
scenarios.leading_indicator  # LeadingIndicator
```

### Inflation

The Inflation module simulates consumer price inflation for one or more countries: the driver of indexed
liabilities, real returns and purchasing power.

The model assumes inflation is pulled back toward a long-run level after a shock, as it was after the 2022 surge
once central banks responded, and that the pull is steady rather than abrupt. That gives scenarios a realistic
spread: a spike decays over a few years instead of persisting forever, while the long-run level anchors 30-year
projections. Inflation can turn negative, so deflation scenarios are possible. Because inflation sits at the root
of the economy in actuarial models such as [Wilkie (1986)][wilkie-1986] and
[Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf),
it can drive interest rates, dividends and property; `ScenarioSet.cumulative_index` turns a path into a price
index.

The default model is the Ornstein-Uhlenbeck process of
[Uhlenbeck and Ornstein (1930)](https://doi.org/10.1103/PhysRev.36.823), `dpi = a(theta - pi)dt + sigma*dW`: `a`
is how fast a gap to the long-run level `theta` closes and `sigma` the size of the random swings. `method` picks
the process:

| Method | What it is |
|:-------|:-----------|
| `ou` (default) | The model above; inflation can go negative. |
| `wilkie_ar1` | Each period keeps a fixed share of the last gap to the mean: [Wilkie (1986)][wilkie-1986]. |
| `hibbert_two_factor` | Toward moving expected inflation: [Hibbert, Mowbray and Turnbull (2001)][hibbert-2001]. |
| `regime_switching` | A calm and a high, volatile regime: [Hamilton (1989)](https://doi.org/10.2307/1912559). |
| `knw` | Linked both ways with a paired interest rate; fitted by `Knw`. |
| `knw_sv` | `knw` with a shared, randomly changing volatility; fitted by `KnwSv`. |

[wilkie-1986]: https://doi.org/10.1017/S0071368600009009
[hibbert-2001]: https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf

For `ou`, `volatility_model: garch` lets calm and turbulent periods alternate, which fattens the tails, as in
[Bollerslev (1986)](https://doi.org/10.1016/0304-4076(86)90063-1); `condition_on_business_cycle` and
`condition_on_interest_rate` tie inflation to the leading indicator or a paired interest rate; and
`measure: risk_neutral` moves inflation around the breakeven inflation the bond market prices today, with its
historical volatility (see `calibrate_risk_neutral`).

The data are the Finance Toolkit's Consumer Price Index, year over year, with no API key needed: 0.034 means
prices are 3.4% higher than a year ago. `source: oecd` covers the roughly 38 OECD members; `source: gmdb`
(the Global Macro Database) adds countries such as Brazil and India, yearly only. Only headline inflation is
modeled.

The `inflation[i]` keys of a factor set and their defaults are listed on the reference page
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/reference/configuration-classes).

Beliefs are annual decimals (`long_run_mean: 0.09` is 9% a
year) and apply to the constant-volatility `ou` fit, every belief, and to `regime_switching`, whose mean follows
a `long_run_mean` (one level or a path) and which takes `shocks`; not with `risk_neutral`. A regime file addresses
one entry as `"inflation.<name>"`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Inflation(toolkit: Toolkit)
```

</details>

#### Inflation.calibrate

Calibrate one country's inflation process from its history: how fast inflation returns to its normal level
(`mean_reversion_speed`), what that level is (`long_run_mean`) and how much it swings (`volatility`).

The parameters come from the country's own Consumer Price Index history, so simulated inflation spikes and
settles the way it has in that economy: a high-inflation country such as Brazil gets a higher anchor and
wider swings than the United States. The `ou` fit regresses each value on the value a year earlier, which
measures how strongly inflation has been pulled back after deviations ([Uhlenbeck and Ornstein,
1930](https://doi.org/10.1103/PhysRev.36.823)): two neighbouring monthly year-over-year rates share 11 months of
price changes, so a month-to-month fit would read that overlap as slow mean reversion. `wilkie_ar1` gives a
`persistence`, the share of last period's gap to the mean carried into this one, from the same year-apart
regression, so the two methods agree on the same history. Values are annual decimals and every path starts from
`initial_value`, the latest observed rate. The long-run level is only as good as the history behind it, so use
an early `start_date`: five years cover too few inflation cycles.

`hibbert_two_factor` assumes inflation is pulled toward an expected-inflation level that itself drifts, which
keeps regime shifts such as the 1970s or the 2010s low-inflation decade inside the scenario set.
`regime_switching` lets inflation move between a calm regime and a high, volatile one, each with its own level
and shock size (`fit_regime_switching_inflation`); fit it on a long history through `regime_history`.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.inflation.inflation_controller import Inflation

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2000-01-01")
inflation = Inflation(toolkit)

inflation.calibrate("united_states_inflation", country="United States")
inflation.calibrate("brazil_inflation", country="Brazil", source="gmdb", period="yearly")
```

Which returns (calibrated on 2026-10-19):

| name | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-----|---------------------:|--------------:|-----------:|--------------:|
| united_states_inflation | 1.1806 | 0.0257 | 0.0269 | 0.0374 |
| brazil_inflation | 1.0904 | 0.0615 | 0.0387 | 0.0502 |

US inflation starts at 3.74% and is pulled toward 2.57%, halving a gap in about seven months: since 2000, a
value regressed on the value a year earlier keeps only 26% of its gap. The month-to-month fit (`ou_fit="step"`)
gives a speed of 0.2586, a gap halving in 2.7 years, because it reads the overlap of monthly rates as
persistence; the yearly series, which has no overlap, gives 0.887.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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
    ou_fit: str = 'year_apart',
    regime_history: pl.Series | None = None,
    regime_history_time_step: float | None = None,
    regime_history_start_year: int | None = None,
) -> OUParams | GARCHParams | OUCovariateParams | AR1Params | MovingTargetOUParams | InflationRegimeParams
```

**Args:**

- <u>name (str):</u> the entry's name.
- <u>country (str):</u> the country, default "United States".
- <u>period (str):</u> "monthly" (default), "quarterly" or "yearly"; only "yearly" for "gmdb".
- <u>source (str):</u> "oecd" (default) or "gmdb" (the Global Macro Database).
- <u>method (str):</u> "ou" (default), "wilkie_ar1", "hibbert_two_factor" or "regime_switching".
- <u>volatility_model (str):</u> "constant" (default) or "garch".
- <u>business_cycle_covariate (pl.Series &#124; None):</u> the leading indicator or paired interest rate inflation moves with, default None.
- <u>business_cycle_covariate_dates (pl.Series &#124; None):</u> the dates of that series; required with it.
- <u>target_source (str):</u> the "hibbert_two_factor" target: "coarser_period" (default, the same inflation at `target_period`) or "ewma" (a smoothed average of its own history).
- <u>target_period (str):</u> "quarterly" or "yearly" (default) for "coarser_period", coarser than `period`.
- <u>target_smoothing (float):</u> the "ewma" weight on each new observation, between 0 and 1, default 0.05, a judgement (a memory of about 20 observations; the paper's target is unobserved).
- <u>ou_fit (str):</u> how the "ou" fits (constant volatility, "garch" or a covariate) and the "hibbert_two_factor" legs read persistence: "year_apart" (default) regresses each value on the value a year earlier, "step" on the previous observation, which reads the overlap of monthly year-over-year rates as slow mean reversion (the fit before October 2026). Yearly data give the same result either way.
- <u>regime_history (pl.Series &#124; None):</u> with "regime_switching", a longer year-over-year history to fit the regimes on, such as the OECD's since 1956; the run still starts from this country's latest rate and the regime the filter reads off its recent data. Default None, the fetched history itself.
- <u>regime_history_time_step (float &#124; None):</u> the spacing of `regime_history` in years, required with it.
- <u>regime_history_start_year (int &#124; None):</u> the year `regime_history` was chosen to start in, if one was; a short history is then by design and is not warned about. Default None.

**Returns:**

<u>OUParams &#124; GARCHParams &#124; OUCovariateParams &#124; AR1Params &#124; MovingTargetOUParams:</u> the fitted parameters, including `initial_value`.

**Raises:**

- <u>ValueError:</u> if an option is unknown or two options clash, no data come back, or the history is too short or shows no pull toward a normal level.

</details>

#### Inflation.calibrate_risk_neutral

Calibrate risk-neutral inflation: random around the breakeven curve the bond market prices today, so the
expected price index matches market prices and caps and floors on indexation get a time value.

The gap between a nominal government bond yield and an inflation-protected one of the same maturity, the
"breakeven", is the inflation the bond market prices in. It is a curve, not one number, because expected
inflation differs by horizon. Inflation that followed it exactly in every scenario would value a plain
inflation-linked cashflow correctly but give a capped or floored one (limited price indexation, a 0%-5%
pension increase) no time value, since a cap above the curve would never be hit. So by default inflation
moves randomly around the curve with the speed and volatility of the country's own consumer price history,
corrected so the expected price index still grows as the curve says (see `BreakevenInflationParams`). The
volatility is historical because the Finance Toolkit has no prices of inflation caps and floors to imply one
from; treat the time value as indicative. This is what `measure: risk_neutral` selects with `method: ou`.

The curve is a [Nelson and Siegel (1987)](https://doi.org/10.1086/296409) fit (a long-run level, a slope and a
hump) on the latest date every maturity is quoted. The data come from the US Treasury, the Bank of England and,
for Germany, the Bundesbank's federal securities yields (inflation-linked minus nominal), with no API key needed.
The shortest breakeven is three (UK) or five years out (US, Germany); before it the curve holds the fitted
breakeven at that maturity flat, the constant-forward rule EIOPA uses before its first quoted maturity (EIOPA
(2026, Annex D.8.2-D.8.3), where a constant forward makes every forward and
every spot rate before the first maturity t1 equal to the spot rate r_t1 at t1), rather than extrapolate the
Nelson-Siegel forward to today.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.inflation.inflation_controller import Inflation

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2005-01-01")
inflation = Inflation(toolkit)

inflation.calibrate_risk_neutral("us_breakeven")
```

Which returns (calibrated on 2026-10-14):

| name | level | slope | curvature | initial_value | mean_reversion_speed | volatility |
|:-----|------:|------:|----------:|--------------:|---------------------:|-----------:|
| us_breakeven | 0.0237 | -0.0001 | -0.0015 | 0.0237 | 1.1456 | 0.0289 |

The breakeven curve is close to flat at 2.37%. Inflation scatters around it with a long-run spread of
0.0289 / sqrt(2 x 1.1456) = 1.91%, in line with the 1.87% spread of US inflation since 2005.

**References:**

- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. <https://doi.org/10.1016/j.jeconom.2005.03.005>
- Jarrow, R., Yildirim, Y. (2003). "Pricing Treasury Inflation Protected Securities and Related Derivatives using an HJM Model." Journal of Financial and Quantitative Analysis, 38(2), 337-358. <https://doi.org/10.2307/4126754>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_risk_neutral(
    name: str,
    decay: float = 0.7308,
    country: str = 'United States',
    volatility: str = 'history',
    source: str = 'oecd',
    period: str = 'monthly',
) -> DeterministicPathParams | BreakevenInflationParams
```

**Args:**

- <u>name (str):</u> the entry's name, also its factor name in the simulation.
- <u>decay (float):</u> the Nelson-Siegel decay, which sets where the hump sits, default 0.7308; fixed rather than fitted, from Diebold and Li (2006, section 3.2), whose λ of 0.0609 a month puts the medium-term factor's peak loading at 30 months; 0.0609 a month × 12 = 0.7308 a year.
- <u>country (str):</u> "United States" (default, 5 to 30 years), "United Kingdom" (3 to 40 years, against the Retail Prices Index), or "Germany" or "Euro Area" (German bonds paying euro area inflation).
- <u>volatility (str):</u> "history" (default) for random inflation around the curve, or "none" to follow the curve exactly in every scenario.
- <u>source (str):</u> "oecd" (default) or "gmdb", the consumer price history the volatility is fitted on.
- <u>period (str):</u> the frequency of that history, default "monthly".

**Returns:**

<u>BreakevenInflationParams &#124; DeterministicPathParams:</u> the curve's `level`, `slope`, `curvature` and `decay`, `initial_value` (today's rate) and, with volatility "history", `mean_reversion_speed` and `volatility`.

**Raises:**

- <u>ValueError:</u> if `country`, `decay`, `volatility`, `source` or `period` is not valid, or no date has every maturity quoted (for the United States, an `end_date` before February 2010).

</details>

#### Inflation.names

The names of every inflation entry calibrated so far, in calibration order.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
inflation.names  # property -> list[str]
```

</details>

#### Inflation.params

The calibrated parameters for one inflation entry.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
params(
    name: str,
) -> OUParams | GARCHParams | OUCovariateParams | AR1Params | MovingTargetOUParams | DeterministicPathParams | InflationRegimeParams
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

</details>

#### Inflation.step_function

The one-period inflation update for a method: Wilkie's AR(1) for "wilkie_ar1" and the exact
Ornstein-Uhlenbeck step otherwise.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
Inflation.step_function(method: str)
```

**Args:**

- <u>method (str):</u> "ou" or "wilkie_ar1".

</details>

#### Inflation.series

The historical inflation rate for one entry. Factors that respond to the level of inflation, such as the
dividend yield's `condition_on_inflation`, are fitted against it.

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

#### Inflation.dates

The dates that go with `series(name)`, in the same order, so another factor can match its own data to this
inflation rate by date rather than by position.

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

#### Inflation.changes

Dated period-over-period changes in one entry's inflation rate: the history its correlations with the other
factors are estimated from.

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

### Unemployment

The Unemployment module simulates the unemployment rate: the share of people who want work but cannot find it.
Unemployment drifts back toward a normal level over time, and it also moves with inflation: as inflation rises, the
labor market tends to tighten and unemployment tends to fall. This module captures both.

Every run has at least one unemployment rate; add one per country or region. Each becomes a variable in the
simulated scenarios, correlated with the other factors, and is paired with one simulated inflation rate, so a
scenario in which inflation jumps also tends to be one in which unemployment falls, the way the two have moved
together historically.

The model is a mean-reverting (Ornstein-Uhlenbeck) process with an added Phillips-curve term, the link between
inflation and unemployment first documented by
[Phillips (1958)](https://doi.org/10.1111/j.1468-0335.1958.tb00003.x). It is
[Ahlgrim, D'Arcy and Gorvett (2005, eq. 3.19)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf):

```text
du = kappa_u * (mu_u - u) * dt + alpha_u * d(inflation) + sigma_u * dW
```

`kappa_u` is how fast unemployment is pulled back to its normal level `mu_u`, `alpha_u` its sensitivity to the
change in inflation over the same step (expected to be negative), and `sigma_u` the size of its own random swings
`dW`. In the simulation, the change in inflation is the paired inflation entry's own simulated move.
`condition_on_business_cycle` adds the leading indicator's change as a second driver next to inflation, with its own
sensitivity. `condition_on_equity` and `condition_on_term_spread` make each scenario's unemployment rise after its
own bear market or flattening yield curve (`calibrate_cycle_links`), and `history_source: oecd` fits the dynamics
on December-to-December changes since 1955 rather than on a window April 2020 dominates (`calibrate_history`).
`regime_switching` splits the process into expansions and recessions, so a scenario can live through a 2008-09
(`calibrate_regimes`).

The data are the Finance Toolkit's unemployment rate and year-over-year Consumer Price Index for the entry's
`country`, with no ticker or API key needed. `source: oecd` covers OECD members; `source: gmdb` (the Global Macro
Database) adds countries such as Brazil and India, yearly only. An entry has no `period` of its own: it uses the
paired inflation entry's, so the two series share one frequency.

The `unemployment[i]` keys of a factor set and their defaults are listed on the reference page
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/reference/configuration-classes).

A belief left `null` keeps the fitted value; a regime file addresses one entry as `"unemployment.<name>"`. This
models the unemployment rate itself, not wages or employment by sector, and the Phillips curve is a statistical link
fitted to history, not a model of how central banks or wage setters respond.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Unemployment(toolkit: Toolkit)
```

</details>

#### Unemployment.calibrate

Calibrate one country's unemployment process from its history: how fast unemployment returns to its normal
level (`mean_reversion_speed`), what that level is (`long_run_mean`), how strongly it moves with the change in
inflation (`inflation_sensitivity`) and how much it swings on its own (`volatility`).

This learns how unemployment has behaved, so simulated scenarios rise, fall and move against inflation the way
the real rate has. In the US example below, a speed of 0.55 a year halves a jump in about 1.3 years, and a
sensitivity of -0.34 means a one-point rise in inflation lowers unemployment by about a third of a point.

The fit regresses each period's change in unemployment on its previous level and the same period's change in
inflation, matched by date, following
[Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf).
Use an early Toolkit `start_date`, as the default window is short.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.unemployment.unemployment_controller import Unemployment

toolkit = Toolkit(["AAPL"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2000-01-01")
unemployment = Unemployment(toolkit)

unemployment.calibrate("united_states", country="United States", period="quarterly")
```

Which returns (calibrated on 2026-10-05):

| name | mean_reversion_speed | long_run_mean | inflation_sensitivity | volatility | initial_value |
|:-----|---------------------:|--------------:|----------------------:|-----------:|--------------:|
| united_states | 0.5534 | 0.0567 | -0.3432 | 0.0211 | 0.0427 |

US unemployment starts at 4.27% and is pulled toward 5.67%.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(
    name: str,
    country: str = 'United States',
    period: str = 'yearly',
    source: str = 'oecd',
    business_cycle_covariate: pl.Series | None = None,
    business_cycle_covariate_dates: pl.Series | None = None,
    inflation: pl.Series | None = None,
    inflation_dates: pl.Series | None = None,
) -> UnemploymentParams
```

**Args:**

- <u>name (str):</u> the entry's name, e.g. "united_states".
- <u>country (str):</u> the country for both data series, default "United States".
- <u>period (str):</u> data frequency: "yearly" (default), "quarterly" or "monthly"; only "yearly" for "gmdb". A configured run uses the paired inflation entry's period.
- <u>source (str):</u> "oecd" (default) or "gmdb" (the Global Macro Database, for countries outside the OECD).
- <u>business_cycle_covariate (pl.Series &#124; None):</u> the leading indicator's level, a second driver next to inflation, default None.
- <u>business_cycle_covariate_dates (pl.Series &#124; None):</u> its dates; required with it.
- <u>inflation (pl.Series &#124; None):</u> an already-fetched year-over-year inflation rate for `country` at `period` (as decimals, e.g. `Inflation.series(name)`), to skip fetching it again; default None fetches it.
- <u>inflation_dates (pl.Series &#124; None):</u> its dates; required with it.

**Returns:**

<u>UnemploymentParams:</u> `mean_reversion_speed`, `long_run_mean`, `inflation_sensitivity`, `volatility`, `initial_value` (the last observed rate) and, with the leading indicator, `business_cycle_sensitivity`.

**Raises:**

- <u>ValueError:</u> if `period` or `source` is not recognized, a series is given without its dates, no data come back (the OECD sends none after too many requests; retry a minute later), or the history is too short or shows no pull toward a normal level. In that last case the series and today's rate are still kept (`latest_rates`), so `calibrate_history` or `calibrate_regimes` can fit the dynamics on long history.

</details>

#### Unemployment.calibrate_history

Refit an entry's dynamics on decades of December-to-December history, so one extraordinary month cannot set
how every scenario's unemployment moves; today's rate stays the starting point.

A fit on the window since 2000 takes its volatility and speed from April 2020, when US unemployment rose ten
points in a month: the volatility comes out four times what the rest of the window shows and scenarios spend
one month in seven below 3.4%, the lowest US rate since 1955. Fitted on the OECD's monthly unemployment and CPI
inflation for `country` since 1955, one observation per December as in `fit_unemployment_history` (the annual
regressions of
[Ahlgrim, D'Arcy and Gorvett (2005, section 3)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf)),
2020 is one year in seventy. The speed, natural rate, Phillips-curve sensitivity and volatility are replaced;
the starting rate is the latest from `calibrate`.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.unemployment.unemployment_controller import Unemployment

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2000-01-01")
unemployment = Unemployment(toolkit)

unemployment.calibrate("united_states", country="United States", period="monthly")
unemployment.calibrate_history("united_states")
```

Which returns (calibrated on 2026-10-17, US data 1957-2025):

| mean_reversion_speed | long_run_mean | inflation_sensitivity | volatility | initial_value |
|---------------------:|--------------:|----------------------:|-----------:|--------------:|
| 0.3060 | 0.0581 | -0.2030 | 0.0112 | 0.042 |

Against the window since 2000 (speed 0.62, volatility 2.2%), a gap to the natural rate of 5.8% halves in 2.3
years and the volatility is half as large.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_history(
    name: str,
    country: str = 'United States',
    economics: Economics | None = None,
    start_year: int | None = None,
) -> UnemploymentParams
```

**Args:**

- <u>name (str):</u> the entry, already calibrated with `calibrate`, whose own window need not show a pull toward a normal level.
- <u>country (str):</u> the country of the OECD history. Defaults to "United States".
- <u>economics (Economics &#124; None):</u> a Finance Toolkit `Economics` reaching back to 1955; built on first use.
- <u>start_year (int &#124; None):</u> fit on the December-to-December changes of this year on. Defaults to None, all.

**Returns:**

<u>UnemploymentParams:</u> the long-history speed, natural rate, inflation sensitivity and volatility, with `fit_time_step` 1.0 and today's starting rate.

**Raises:**

- <u>RuntimeError:</u> if `calibrate` has not read `name`'s data.
- <u>ValueError:</u> if the history is missing or too short, or shows no pull toward a normal level.

</details>

#### Unemployment.calibrate_cycle_links

Fit how far unemployment rises after the equity market falls or the yield curve flattens, on decades of
history, and build both links into an entry already calibrated with `calibrate`.

Unemployment does not move on its own: it climbs in the year after a bear market or an inverted yield curve,
as the recessions of 1974, 1982, 2001 and 2009 show, and comes back down slowly. On its own the fitted process
only knows inflation, so a scenario's stock market crash would leave its unemployment untouched. With these
links, each scenario's unemployment answers to its own simulated equity market (`equity`: a past-year return
short of normal, read three months on) and to the gap between its own long and short rate against its average
of the five years before (`term_spread`, read six months on).

The sensitivities come from December-to-December changes, so no month enters two observations: the OECD's
monthly unemployment, inflation and short and long rates for `country` (from 1955, keyless) and Shiller's
S&P Composite total return for the equity link, regressed as in `fit_cycle_links`, which cites Okun (1962),
[Estrella and Hardouvelis (1991)](https://doi.org/10.1111/j.1540-6261.1991.tb02674.x),
[Estrella and Mishkin (1998)](https://doi.org/10.1162/003465398557320),
[Neftçi (1984)](https://doi.org/10.1086/261226) and [Sichel (1993)](https://doi.org/10.1111/j.1465-7295.1993.tb00879.x).
The links, the pull back to normal and the Phillips-curve term come from that one regression, which replaces
the entry's own speed, long-run mean, inflation sensitivity and volatility; today's rate stays the start, and
unemployment settles below its long-run mean while markets are calm (`calm_level`, `with_cycle_links`).

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.unemployment.unemployment_controller import Unemployment

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2000-01-01")
unemployment = Unemployment(toolkit)

unemployment.calibrate("united_states", country="United States", period="monthly")
unemployment.calibrate_cycle_links("united_states")
unemployment.cycle_link_fit("united_states")
```

Which returns (calibrated on 2026-10-19, US data 1969-2025):

| equity_sensitivity | equity_upside_sensitivity | term_spread_sensitivity | explained_share |
|-------------------:|--------------------------:|------------------------:|----------------:|
| -0.0670 | -0.0216 | -0.2826 | 0.4925 |

A past-year log return 10 points short of its normal 10.6% lifts unemployment by 0.67 points over the next
year, while returns above normal leave it alone (-0.022, standard error 0.022), and a curve one point flatter
than its five-year average for a year lifts it by 0.28 points; together they explain 49% of what the level and
inflation leave unexplained. In history recoveries come with rallies and steeper curves, so the joint regression
gives the links much of unemployment's fall after a recession: its own pull is slow (0.086 a year) and the calm
level it implies low (1.0%, against a 6.1% average).

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_cycle_links(
    name: str,
    country: str = 'United States',
    equity: bool = True,
    term_spread: bool = True,
    economics: Economics | None = None,
    start_year: int | None = None,
) -> UnemploymentParams
```

**Args:**

- <u>name (str):</u> the entry, already calibrated with `calibrate`.
- <u>country (str):</u> the country of the long history; the equity link needs "United States". Defaults to it.
- <u>equity (bool):</u> link unemployment to the equity market. Defaults to True.
- <u>term_spread (bool):</u> link it to the long minus the short rate. Defaults to True.
- <u>economics (Economics &#124; None):</u> a Finance Toolkit `Economics` reaching back to 1955; built on first use.
- <u>start_year (int &#124; None):</u> fit on the December-to-December changes of this year on. Defaults to None, all.

**Returns:**

<u>UnemploymentParams:</u> the entry's parameters with `equity_sensitivity`, `term_spread_sensitivity`, `cycle_lag`, their normal levels and the volatility net of the links.

**Raises:**

- <u>RuntimeError:</u> if `name` has not been calibrated.
- <u>ValueError:</u> if neither link is asked for, the equity link is asked for outside the United States, or the history is missing or too short.

</details>

#### Unemployment.calibrate_regimes

Fit unemployment's expansions and recessions on decades of monthly history and build them into an entry
already calibrated with `calibrate`, so scenarios hold recessions as deep and as long as history's.

One mean-reverting process with one normal shock moves unemployment by about the same amount every year: from
the end of 2007 its 90% band reached only 6.1% by 2009, when the US rate hit 9.9%. Unemployment does not move
that way: it falls slowly through long expansions and jumps in recessions. Here the monthly change is a
regression whose intercept and noise switch between an expansion and a recession regime as a Markov chain,
[Hamilton's (1989)](https://doi.org/10.2307/1912559) model, fitted by maximum likelihood through his filter on
the OECD's monthly unemployment and CPI inflation for `country` (from 1955, keyless), with the pandemic months
of 2020 left out (`fit_unemployment_regimes`). The pull back to a calm level and the Phillips-curve term stay in
the regression. With `equity` and/or `term_spread`, the chance of a recession starting moves with the cycle
links' signals ([Filardo (1994)](https://doi.org/10.1080/07350015.1994.10524545)), and their history before the
start is kept, so a run that starts after the curve inverted carries that warning. Every scenario starts in
recession with the chance the filter gives the last month of history; today's rate stays the starting point.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.unemployment.unemployment_controller import Unemployment

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2000-01-01")
unemployment = Unemployment(toolkit)

unemployment.calibrate("united_states", country="United States", period="monthly")
unemployment.calibrate_regimes("united_states")
unemployment.regime_fit("united_states")
```

Which returns (calibrated on 2026-10-17, US data 1956-2026):

| recession_share | mean_recession_months | mean_expansion_months | long_run_mean | calm_level |
|----------------:|----------------------:|----------------------:|--------------:|-----------:|
| 0.134 | 9.8 | 63.4 | 0.0555 | 0.0378 |

Recessions take 13% of months and last ten months on average, pushing unemployment up 3.2 points a year;
expansions pull it back toward a calm level of 3.8% at a speed of 0.24 a year, so it averages 5.6%. A policy
rule's natural rate then sets either level (`UnemploymentConfig.natural_rate_anchor`), and the other keeps
its fitted distance.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_regimes(
    name: str,
    country: str = 'United States',
    equity: bool = False,
    term_spread: bool = False,
    economics: Economics | None = None,
    start_year: int | None = None,
) -> UnemploymentParams
```

**Args:**

- <u>name (str):</u> the entry, already calibrated with `calibrate`, whose own window need not show a pull toward a normal level.
- <u>country (str):</u> the country of the OECD history; the equity link needs "United States". Defaults to it.
- <u>equity (bool):</u> let a shortfall in the equity market's past-year return raise the chance of a recession. Defaults to False.
- <u>term_spread (bool):</u> let a flatter curve than over the five years before raise it. Defaults to False.
- <u>economics (Economics &#124; None):</u> a Finance Toolkit `Economics` reaching back to 1955; built on first use.
- <u>start_year (int &#124; None):</u> fit on the months from January of this year on, such as 1984 for the US Great Moderation; the signals still read the months before. Defaults to None, every month.

**Returns:**

<u>UnemploymentParams:</u> the entry with `regimes` set and the regime fit's speed, long-run average, inflation sensitivity and average volatility.

**Raises:**

- <u>RuntimeError:</u> if `calibrate` has not read `name`'s data.
- <u>ValueError:</u> if the equity link is asked for outside the United States, or the history is missing, too short or shows no pull toward a calm level.

</details>

#### Unemployment.regime_fit

The expansion and recession regimes fitted for one entry by `calibrate_regimes`: the process, the switching
chances, the share and length of recessions, the likelihoods and each month's filtered chance of a recession.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
regime_fit(name: str) -> UnemploymentRegimeFit
```

**Args:**

- <u>name (str):</u> the entry's name.

**Raises:**

- <u>RuntimeError:</u> if no regimes were fitted for that entry.

</details>

#### Unemployment.cycle_link_fit

The cycle links fitted for one entry by `calibrate_cycle_links`: the sensitivities with their standard errors,
the normal levels, the share of unemployment's yearly moves they explain and the years used.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
cycle_link_fit(name: str) -> CycleLinkFit
```

**Args:**

- <u>name (str):</u> the entry's name.

**Raises:**

- <u>RuntimeError:</u> if no cycle links were fitted for that entry.

</details>

#### Unemployment.names

The names of every unemployment entry calibrated so far, in calibration order.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
unemployment.names  # property -> list[str]
```

</details>

#### Unemployment.latest_rates

The last unemployment rate `calibrate` read for each entry, where its scenarios start: kept even when the
entry's own window shows no pull toward a normal level (a window ending in a surge, such as 2009's), so
`calibrate_history` or `calibrate_regimes` can still fit its dynamics on long history.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
unemployment.latest_rates  # property -> dict[str, float]
```

</details>

#### Unemployment.params

The calibrated parameters for one unemployment entry.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
params(name: str) -> UnemploymentParams
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

</details>

#### Unemployment.step_function

The one-step unemployment update: the exact mean-reverting step plus the Phillips-curve term.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
unemployment.step_function  # property
```

</details>

#### Unemployment.changes

Dated period-over-period changes in one entry's unemployment rate: the history its correlations with the other
factors are estimated from.

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

#### Unemployment.series

The historical unemployment rate one entry was fitted on, as decimals; a policy-rule interest rate reads it
to fit how fast the rate has followed its rule.

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

#### Unemployment.dates

The observation dates that go with `series(name)`.

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

### Mortality

The Mortality module simulates how death rates at older ages change over the coming years: the longevity risk a
pension fund or annuity provider carries when people live longer than expected. Mortality has fallen steadily for
decades, but not at a fixed pace, and that uncertain trend is what this module captures.

Give it a table of historical death rates by age and year, and every scenario gets a path for the overall
mortality level and for how steeply mortality rises with age, correlated with rates, equities and the rest. From
those two paths the death rate at any age in any simulated year can be read back, which is what a pension or
annuity liability needs. It is opt-in (`mortality.enabled`) and off in the shipped factor sets.

The model is the two-factor model of [Cairns, Blake and Dowd (2006)](https://doi.org/10.1111/j.1539-6975.2006.00195.x):

`logit(q(x, t)) = kappa1(t) + kappa2(t) * (x - mean_age)`

where `q(x, t)` is the one-year probability of death at age `x` in year `t`, the logit is `log(q / (1 - q))` and
`mean_age` the average fitted age. `kappa1` is the level, moving mortality at every age alike; `kappa2` is the age
slope. Both are simulated as a random walk with drift (`mortality_level`, `mortality_slope`), with no pull back to
a normal level: mortality improvement is a trend over decades, and its uncertainty grows with the horizon,so the
range of death rates in year 30 is far wider than in year 5. That is the longevity risk a long-dated
liability carries. The logit form keeps every death probability between 0 and 1, and the straight line in age
describes mortality well from about 60 upward, the ages that drive pension and annuity values.
`cbd_mortality_rate(kappa1, kappa2, age, mean_age)` turns the paths back into a death rate, with `mean_age` from
the calibrated parameters.

The data come one of two ways (`source`):

- `supplied` (default): you pass a historical table, for example from the
  [Human Mortality Database](https://www.mortality.org/), a Society of Actuaries table or a national statistics
  agency, for any country. Without one, calibration raises a `ValueError` rather than skipping the factor.
- `eurostat`: a European country's life table is fetched through the Finance Toolkit (yearly from 1960 for most
  countries, no API key), for ages 60 to 84 by default.

```python
result = scenarios.simulate(
    config,
    mortality_rates=mortality_rates,  # pl.DataFrame: one row per year, one column per age
    mortality_ages=[60.0, 65.0, 70.0, 75.0, 80.0, 85.0],
)
```

The `mortality` keys of a factor set and their defaults are listed on the reference page
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/reference/configuration-classes).

**References:**

- Cairns, A.J.G., Blake, D., Dowd, K. (2006). "A Two-Factor Model for Stochastic Mortality with Parameter Uncertainty: Theory and Calibration." Journal of Risk and Insurance, 73(4), 687-718. <https://doi.org/10.1111/j.1539-6975.2006.00195.x>
- Eurostat. "Life table by age and sex" (dataset demo_mlifetable). <https://ec.europa.eu/eurostat/databrowser/view/demo_mlifetable/default/table>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Mortality(toolkit: Toolkit | None = None)
```

</details>

#### Mortality.fetch_life_table

One European country's historical one-year death probabilities by single year of age, from Eurostat's life
tables: a row per calendar year (oldest first), a column per age, ready for `calibrate`.

This gives how likely a person of each age was to die within the year, for every year Eurostat has recorded
(from 1960 for most countries), so the mortality trend is learned from official national statistics rather than
from a table you provide.

**References:**

- Eurostat. "Life table" (demo_mlifetable). <https://ec.europa.eu/eurostat/databrowser/view/demo_mlifetable/default/table>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fetch_life_table(
    country: str,
    sex: str = 'total',
    min_age: int = 60,
    max_age: int = 84,
) -> tuple[pl.DataFrame, list[float], list[int]]
```

**Args:**

- <u>country (str):</u> a European Economic Area country as Eurostat names it, e.g. "Germany".
- <u>sex (str):</u> "total", "male" or "female". Defaults to "total".
- <u>min_age (int):</u> the youngest age to fit. Defaults to 60: Cairns, Blake and Dowd (2006) fit mortality rates above age 60.
- <u>max_age (int):</u> the oldest age, at most 94. Defaults to 84: Eurostat extended its life tables and life expectancy by single age from an open 85+ group to an open 95+ group only from reference year 2014 ([metadata](https://ec.europa.eu/eurostat/cache/metadata/en/demo_mor_esms.htm)), so a higher age keeps only recent years.

**Returns:**

<u>tuple[pl.DataFrame, list[float], list[int]]:</u> the death probabilities, the ages of its columns, and the calendar year of each row. Years with a missing age are dropped.

**Raises:**

- <u>ValueError:</u> if no Toolkit was given, the age range is invalid, or Eurostat has no table for the country.

</details>

#### Mortality.calibrate

Calibrate the Cairns-Blake-Dowd mortality model: split every year's death rates into a level (`kappa1`) and an
age slope (`kappa2`), then fit each as a random walk with a yearly trend (`drift`) and swing size (`volatility`).

This measures how fast death rates have been falling and how uncertain that pace is; the scenarios carry that
trend forward, so an annuity's value reflects both the expected improvement and the risk that it runs faster. A
`kappa1` drift of -0.015 means death rates fall by roughly 1.5% a year at every age; `1 / (1 + exp(-kappa1))` is
the one-year death probability at the mean age and `exp(kappa2)` its growth per extra year of age.

Each year's logit mortality is regressed on age, as in
[Cairns, Blake and Dowd (2006)](https://doi.org/10.1111/j.1539-6975.2006.00195.x).

**As an example:**

```python
import pandas as pd
import polars as pl

from financescenarios.factors.mortality.mortality_controller import Mortality

ages = [60, 64, 68, 72, 76, 80, 84]
url = (
    "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/demo_mlifetable/"
    "A.PROBDEATH.T." + "+".join(f"Y{age}" for age in ages) + ".NL?format=SDMX-CSV"
)
table = pd.read_csv(url).pivot(index="TIME_PERIOD", columns="age", values="OBS_VALUE").dropna()
table = table[[f"Y{age}" for age in ages]]  # Dutch one-year death probabilities, 1985-2024

mortality = Mortality()
mortality.calibrate(
    pl.from_pandas(table.reset_index(drop=True)),
    ages=[float(age) for age in ages],
    mortality_years=table.index.to_list(),
)
```

Which returns (calibrated on 2026-10-04, `mean_age` 72.0):

| factor | drift | volatility | initial_value |
|:-------|------:|-----------:|--------------:|
| kappa1 | -0.0153 | 0.0272 | -3.9380 |
| kappa2 | 0.0003 | 0.0019 | 0.1105 |

A 72-year-old in 2024 had a 1.9% chance of dying within the year.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(
    mortality_rates: pl.DataFrame,
    ages: list[float],
    period: str = 'yearly',
    mortality_years: list[int] | None = None,
) -> CBDParams
```

**Args:**

- <u>mortality_rates (pl.DataFrame):</u> one row per year (oldest first), one column per age, of one-year death probabilities (the Human Mortality Database's `qx`, not `Mx`).
- <u>ages (list[float]):</u> the age of each column, strictly increasing.
- <u>period (str):</u> the data frequency; only "yearly" is supported. Defaults to "yearly".
- <u>mortality_years (list[int] &#124; None):</u> the calendar year of each row, to date the changes. Defaults to None: the last row is taken as last year, with a warning.

**Returns:**

<u>CBDParams:</u> the fitted `kappa1` and `kappa2` processes, `mean_age`, `min_age` and `max_age`.

**Raises:**

- <u>ValueError:</u> if `period` is unknown, `ages` has fewer than 2 entries or does not match the columns, a rate is outside 0 to 1, or `mortality_years` has the wrong length.

</details>

#### Mortality.params

The calibrated mortality model: the `kappa1` and `kappa2` trends and the fitted age range.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
mortality.params  # property -> CBDParams
```

**Raises:**

- <u>RuntimeError:</u> if the model has not been calibrated yet.

</details>

#### Mortality.step_function

The one-step move of `kappa1` and `kappa2`: a random walk with drift, so improvement continues at the fitted
pace with no pull back to a past level.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
mortality.step_function  # property
```

</details>

#### Mortality.changes

The historical yearly changes of `mortality_level` and `mortality_slope`, the input for their correlation with
the other factors.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
mortality.changes  # property -> dict[str, pl.DataFrame]
```

**Returns:**

<u>dict[str, pl.DataFrame]:</u> one table per factor, with a `date` and a `value` column.

**Raises:**

- <u>RuntimeError:</u> if the model has not been calibrated yet.

</details>

### LeadingIndicator

The Leading Indicator module simulates the OECD Composite Leading Indicator (CLI), an index built to signal turning
points in the business cycle, the alternation of economic expansions and slowdowns, a few months before they show up
in output.

Switch it on (`leading_indicator.enabled: true`) and the simulated scenarios gain one more variable that tracks where
the economy is in its cycle, correlated with every other factor. On its own it does not steer any other factor. Its
second role is as the business-cycle signal other factors can opt into with `condition_on_business_cycle: true`, so
that, for example, credit spreads tend to widen as the indicator turns down.

The model is the mean-reverting Ornstein-Uhlenbeck process the interest rate module uses for its short rate, as in
[Vasicek (1977)](https://doi.org/10.1016/0304-405x(77)90016-2):

```text
d(CLI) = a * (theta - CLI) * dt + sigma * dW
```

where `a` is the mean-reversion speed, `theta` the long-run level and `sigma` the volatility. Mean reversion holds
almost by construction: the OECD publishes the CLI with its long-run trend removed, scaled to swing around 100 as its
long-term trend: the CLI averages de-trended, smoothed component series, and the amplitude-adjusted CLI rescales that
average to the amplitude of the de-trended reference series, as described in [OECD (2012, pp. 3 and
9)](https://www.oecd.org/content/dam/oecd/en/data/methods/OECD-System-of-Composite-Leading-Indicators.pdf), "OECD
System of Composite Leading Indicators". `volatility_model: garch` lets the size of the swings vary over time, so calm
and turbulent periods each persist, as in [Bollerslev (1986)](https://doi.org/10.1016/0304-4076(86)90063-1).

A conditioned `interest_rates[i]`, `inflation[i]`, `real_estate`, `credit[i]`, `commodities[i]` or `dividend_yield[i]`
entry gains a pull from the indicator's change:

```text
d(x) = a * (theta - x) * dt + beta * d(CLI) + sigma * dW
```

The beta term is a judgement with no published source: it is built like the inflation term of the
Ahlgrim, D'Arcy and Gorvett (2005) unemployment equation, a covariate's same-period change added to the drift.
It is then calibrated at `leading_indicator.period`, which that factor must support (`real_estate` needs quarterly or
yearly), it cannot use `volatility_model: garch`, and its belief overrides do not apply. Equities instead let their
regime-switching probabilities depend on the indicator, as in
[Filardo (1994)](https://doi.org/10.1080/07350015.1994.10524545), and unemployment adds it as a second driver next to
inflation.

The data are the OECD's monthly Composite Leading Indicator for about 22 countries and country groups, no API key
needed. It models the index level only, not recession dates or the
probability of a recession.

The `leading_indicator` keys of a factor set and their defaults are listed on the reference page
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/reference/configuration-classes).

**References:**

- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. <https://doi.org/10.1016/0304-405x(77>)90016-2
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." Journal of Econometrics, 31(3), 307-327. <https://doi.org/10.1016/0304-4076(86>)90063-1
- Filardo, A.J. (1994). "Business-Cycle Phases and Their Transitional Dynamics." Journal of Business & Economic Statistics, 12(3), 299-308. <https://doi.org/10.1080/07350015.1994.10524545>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
LeadingIndicator(toolkit: Toolkit)
```

</details>

#### LeadingIndicator.calibrate

Calibrate the leading indicator from its history: fetch the OECD Composite Leading Indicator for `country`, then
fit how fast it returns to its normal level (`mean_reversion_speed`), what that level is (`long_run_mean`) and how
much it swings (`volatility`).

This learns how the business-cycle signal has moved, so the simulated scenarios pass through expansions and
slowdowns at a realistic pace. The half-life of a swing is ln 2 / `mean_reversion_speed`: a speed of 0.50 a year
means a dip below 100 has recovered half of the way after about 1.4 years. All values are in index points:
`long_run_mean` is near 100, the level the OECD scales the index to, and `initial_value` is the latest reading,
where every simulated path starts (above 100 means above-trend activity ahead).

The history starts at the Toolkit's `start_date`; the Finance Toolkit's default window is short, so pass an early
`start_date` for a meaningful fit. A second call replaces the first, since a run has one leading indicator.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.leading_indicator.leading_indicator_controller import LeadingIndicator

toolkit = Toolkit(["AAPL"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2000-01-01")
leading_indicator = LeadingIndicator(toolkit)

leading_indicator.calibrate(country="United States", period="monthly")
leading_indicator.calibrate(country="United States", period="quarterly")
```

Which returns (calibrated on 2026-10-19):

| period | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-------|---------------------:|--------------:|-----------:|--------------:|
| monthly | 0.3481 | 99.7380 | 1.3410 | 100.9993 |
| quarterly | 0.6254 | 99.7405 | 1.6596 | 100.9383 |

The US indicator stands at about 101.0, slightly above trend, and is pulled toward 99.7 with a half-life of about
2.0 years on monthly data, once the finite-sample bias of the speed is taken off (`fit_ou_process`).

**References:**

- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. <https://doi.org/10.1016/0304-405x(77>)90016-2

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(
    country: str = 'United States',
    period: str = 'monthly',
    volatility_model: str = 'constant',
) -> OUParams | GARCHParams
```

**Args:**

- <u>country (str):</u> the country to fetch the indicator for. Defaults to "United States".
- <u>period (str):</u> "monthly", "quarterly" or "yearly"; a coarser period averages the monthly data. Defaults to "monthly".
- <u>volatility_model (str):</u> "constant" or "garch". Defaults to "constant".

**Returns:**

<u>OUParams &#124; GARCHParams:</u> the fitted process, including `initial_value`; GARCHParams with "garch".

**Raises:**

- <u>ValueError:</u> if `period` or `volatility_model` is not recognized, or the OECD returns no data, for example when it rate-limits a burst of requests (wait a minute and retry).

</details>

#### LeadingIndicator.params

The calibrated indicator process: reversion speed, long-run level, volatility and today's reading.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
leadingindicator.params  # property -> OUParams | GARCHParams
```

**Raises:**

- <u>RuntimeError:</u> if `calibrate()` has not been called yet.

</details>

#### LeadingIndicator.step_function

The one-step update of the indicator: the same exact Ornstein-Uhlenbeck step as the short rate.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
leadingindicator.step_function  # property
```

</details>

#### LeadingIndicator.series

The historical indicator levels `calibrate()` fetched. Factors with `condition_on_business_cycle` use them to fit
how they respond to the indicator's change.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
leadingindicator.series  # property -> pl.Series
```

**Raises:**

- <u>RuntimeError:</u> if `calibrate()` has not been called yet.

</details>

#### LeadingIndicator.dates

The dates of `series`, in the same order, so a conditioned factor can match the indicator to its own history by
date.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
leadingindicator.dates  # property -> pl.Series
```

**Raises:**

- <u>RuntimeError:</u> if `calibrate()` has not been called yet.

</details>

#### LeadingIndicator.changes

Dated period-over-period changes of the indicator: the history its correlations with the other factors are
estimated from.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
leadingindicator.changes  # property -> pl.DataFrame
```

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if `calibrate()` has not been called yet.

</details>

### How It Is Calculated

The model functions behind this page, each with the formula it implements.

#### fit_wilkie_ar1

Fit Wilkie's (1986) inflation AR(1) on year-apart observations, and scale it to the simulation step.

Wilkie's persistence QA is a yearly coefficient: the share of this year's gap to the long-run mean that is left next
year. Year-over-year inflation sampled monthly overlaps: two neighbouring months share 11 of their 12 months of
price changes, so a month-to-month regression measures that overlap rather than how inflation itself fades, and
reads 0.9 to 0.99 a month even when a shock is gone within a year. Here each value is regressed on the value one
year earlier instead, which measures exactly what QA means. Wilkie's own values on UK data (yearly from 1919 to 1982,
section 2.11) are QMU = 0.05, QA = 0.6 and QSD = 0.05 (section 3.4); a fit on a short, calm
history can land far from them, as US inflation from 1995 to 2007 does (QA near 0, QSD 0.8%), so check the fitted
values against that benchmark. US inflation since 1919 (Shiller's yearly series, `history_source: shiller`) gives
QMU 2.6%, QA 0.54 and QSD 3.4%, which is what the shipped Wilkie preset uses.

The yearly AR(1) is then stepped at the run's frequency with a persistence per step chosen so that the long-run
uncertainty of the price level stays Wilkie's: an average of simulated inflation over many years varies as much as
it does in the yearly model, so indexed cash flows far out carry the right spread. For persistent inflation (QA of
0.6 or more) this per-step value is within 0.001 of QA^(1/k), so sampled once a year the simulated inflation is
Wilkie's AR(1) again. When a year keeps little of the year before, it stays near 0.85 a month, so neighbouring
months still move together as overlapping year-over-year rates do, where a plain k-th root would make every month
an independent draw and understate the price level's spread. The shock is scaled so the spread of inflation
itself, QSD / sqrt(1 - QA^2), stays the same.

The formula is as follows:

$$
I_{t} = \text{QMU} + \text{QA} \cdot (I_{t-1} - \text{QMU}) + \text{QSD} \cdot e_{t}
$$

$$
(1 + \phi) / (1 - \phi) = k \cdot (1 + \text{QA}) / (1 - \text{QA})
$$

$$
\sigma = \text{QSD} \cdot \sqrt{(1 - \phi ^{2}) / (1 - \text{QA} ^{2})}
$$

Where t counts years, so I_t-1 is year-over-year inflation one year (k observations) before I_t, k is the number
of observations per year (12 monthly, 4 quarterly, 1 yearly), QMU the long-run mean, QA and QSD the yearly
persistence and shock size fitted by least squares on all year-apart pairs, and phi and sigma the persistence and
shock size per step the simulation uses. The second line equates the long-run variance of the two processes'
averages. With yearly data, phi = QA and this is Wilkie's own fit.

**References:**

- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. Sections 3.3-3.4. <https://doi.org/10.1017/S0071368600009009>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_wilkie_ar1(inflation_rate: pl.Series, steps_per_year: int = 1) -> AR1Params
```

**Args:**

- <u>inflation_rate (pl.Series):</u> the year-over-year inflation history, evenly spaced, as decimals.
- <u>steps_per_year (int):</u> observations per year, which is also the simulation's steps per year. Defaults to 1.

**Returns:**

<u>AR1Params:</u> the long-run mean, the persistence and shock size per step, and the latest inflation rate.

**Raises:**

- <u>ValueError:</u> if the history is too short, or the yearly persistence is not between -1 and 1, so inflation would not settle at a long-run level.

</details>

#### wilkie_ar1_per_step

Turn a yearly inflation AR(1) (Wilkie's QMU, QA, QSD) into the per-step AR(1) a monthly or quarterly run steps
with, keeping the long-run spread of inflation and of the price level; see `fit_wilkie_ar1` for the reasoning.

The formula is as follows:

$$
(1 + \phi) / (1 - \phi) = k \cdot (1 + \text{QA}) / (1 - \text{QA})
$$

$$
\sigma = \text{QSD} \cdot \sqrt{(1 - \phi ^{2}) / (1 - \text{QA} ^{2})}
$$

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
wilkie_ar1_per_step(yearly: AR1Params, steps_per_year: int) -> AR1Params
```

**Args:**

- <u>yearly (AR1Params):</u> the yearly fit, persistence QA and shock size QSD per year.
- <u>steps_per_year (int):</u> k, the simulation's steps per year; 1 returns `yearly` unchanged.

**Returns:**

<u>AR1Params:</u> the same long-run mean and starting value, with the persistence and shock size per step.

</details>

#### fit_inflation_ou

Fit the Ornstein-Uhlenbeck inflation process on year-apart observations, so the overlap of monthly
year-over-year rates does not pass for slow mean reversion.

Two neighbouring monthly year-over-year rates share 11 of their 12 months of price changes, so a month-to-month
fit reads that overlap as persistence. On US inflation since 1960 it gives a speed of 0.13 a year, which keeps 88%
of a gap after a year, where the data keep 73% (a value regressed on the value a year earlier); since 2000 it keeps
66% where the data keep 26%. Too slow a pull leaves a spike in place for years and overstates long-run price-level
uncertainty. This fit is `fit_wilkie_ar1` written as an OU process: an OU stepped at the data's frequency makes the
same moves as Wilkie's per-step AR(1), so the two methods agree on the same history. With yearly data it is the
plain exact OU fit (`fit_ou_process`). Ahlgrim, D'Arcy and Gorvett (2005, section 3) do the same for their OU
inflation, choosing its parameters from annual regressions because monthly data are noisy: they find a speed of
0.37 on 1913-2001 and 0.47 on 1946-2001 and choose 0.4; this fit gives 0.32 on US inflation since 1960.

The formula is as follows:

$$
a = - k \cdot \ln(\phi)
$$

$$
\sigma = \text{sigma\_step} \cdot \sqrt{2 \cdot a / (1 - \phi ^{2})}
$$

Where phi and sigma_step are the per-step persistence and shock size of `fit_wilkie_ar1` and k the observations
per year, so the stationary spread sigma / sqrt(2a) equals that of the data.

**References:**

- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. Sections 3.3-3.4. <https://doi.org/10.1017/S0071368600009009>
- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. Section 3. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_inflation_ou(inflation_rate: pl.Series, steps_per_year: int = 1) -> OUParams
```

**Args:**

- <u>inflation_rate (pl.Series):</u> the year-over-year inflation history, evenly spaced, as decimals.
- <u>steps_per_year (int):</u> observations per year (12 monthly, 4 quarterly, 1 yearly). Defaults to 1.

**Returns:**

<u>OUParams:</u> the yearly mean-reversion speed, long-run mean, yearly volatility and the latest inflation rate.

**Raises:**

- <u>ValueError:</u> if the history is too short, or inflation shows no pull toward a long-run level (with yearly data, a year-apart persistence of zero or below, which an OU process cannot hold).

</details>

#### step_ar1

Move inflation one period forward under Wilkie's (1986) model, the classic UK actuarial inflation model.

Wilkie models the force of inflation (the log change in the price index) as an AR(1): each period keeps a fixed
share of last period's gap to the long-run mean and adds a normal shock. A persistence near one means shocks fade
slowly, so scenarios can show long stretches of high or low inflation; the stationary spread of inflation is
QSD / sqrt(1 - QA^2), wider than one period's shock.

The formula is as follows:

$$
I_{t} = \text{QMU} + \text{QA} \cdot (I_{t-1} - \text{QMU}) + \text{QSD} \cdot z_{t}
$$

Where I_t is the inflation rate, QMU is `long_run_mean`, QA is `persistence` and QSD is `volatility`, all per
simulation step. Wilkie's persistence is yearly; at a monthly or quarterly step the fit (`fit_wilkie_ar1`) turns
it into a per-step value with the same long-run spread of inflation and of the price level. The
simulation frequency must equal the entry's `period`.

**References:**

- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. Sections 3.3-3.4. <https://doi.org/10.1017/S0071368600009009>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_ar1(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: AR1Params,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> this period's inflation rate.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw.
- <u>time_step (float):</u> not used; the period is fixed by the calibration.
- <u>params (AR1Params):</u> calibrated long-run mean, persistence, and volatility.

**Returns:**

<u>np.ndarray:</u> inflation one period later.

</details>

#### step_ou

Move inflation one step forward under the Ornstein-Uhlenbeck process d(pi_t) = a * (theta - pi_t) * dt + sigma *
dW_t, the default inflation model.

Inflation is pulled toward its long-run level theta at speed a: a gap halves in ln(2) / a years, and the
long-run spread of inflation around theta is sigma / sqrt(2a). This matches how inflation behaves under a
central bank with a target, where shocks fade over a few years, and is the inflation generator of Ahlgrim and
D'Arcy (2012). The step uses the exact transition (as for the Vasicek short rate), so the result is the same
whether you simulate monthly or yearly.

The formula is as follows:

$$
\pi(t + \text{dt}) = \theta + (\pi(t) - \theta) \cdot \exp(- a \cdot \text{dt}) + \sigma \cdot \sqrt{(1 - \exp(- 2 \cdot a \cdot \text{dt})) / (2 \cdot a)} \cdot z
$$

Where a is `mean_reversion_speed`, theta `long_run_mean`, sigma `volatility` and z a standard normal draw.
Nothing stops inflation from going negative, so deflation scenarios occur with the probability the history
implies.

**References:**

- Ahlgrim, K.C., D'Arcy, S.P. (2012). "A User's Guide to the Inflation Generator." Casualty Actuarial Society, Canadian Institute of Actuaries, Society of Actuaries. <https://www.soa.org/globalassets/assets/files/research/projects/research-2012-02-effect-deflation-user-guide.pdf>
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://doi.org/10.1017/S0071368600009009>
- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. Section 5, eqs. (25)-(26), p. 185: the exact transition used here. <https://doi.org/10.1016/0304-405X(77>)90016-2

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_ou(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: OUParams,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's inflation rate.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw.
- <u>time_step (float):</u> the step length, in years.
- <u>params (OUParams):</u> calibrated mean-reversion speed, long-run mean, and volatility.

**Returns:**

<u>np.ndarray:</u> inflation one step later.

</details>

#### breakeven_forward

Today's breakeven inflation forward at each horizon: the Nelson-Siegel forward from the shortest quoted maturity
on, and the fitted breakeven at that maturity held flat before it.

Breakevens are quoted from three (UK) or five years (US, Germany) out, so a Nelson-Siegel forward read at shorter
horizons is an extrapolation the data do not support: on 2026-10-14 it started the German curve at 5.72% against
a 2.28% five-year quote, and the UK one at 7.76% against a 4.03% three-year quote. Below the shortest maturity the
forward is held at the fitted yield there, the constant-forward rule EIOPA applies before its first quoted
maturity (EIOPA (2026, Annex D.8.2), where a constant forward sets f_j-1,j = f_j = f_1 = r_t1
for j = 1, 2, ..., t1, and EIOPA (2026, Annex D.8.3), which gives the spot rates z_j = r_t1 for the same j).
The accumulated forward to the shortest maturity is unchanged, so every breakeven yield from that maturity on is
still the Nelson-Siegel one and inflation-linked cashflows from there are priced as before.

The formula is as follows:

$$
f_{BE}(t) = y_{NS}(T_{1}) \text{for}\; t < T_{1}
$$

$$
f_{BE}(t) = L + S \cdot \exp(- \lambda \cdot t) + C \cdot \lambda \cdot t \cdot \exp(- \lambda \cdot t) \text{for}\; t \geq T_{1}
$$

Where T1 is `params.shortest_maturity` and y_NS the Nelson-Siegel yield; with T1 = 0 this is the plain forward.

**References:**

- EIOPA (2026). "RFR Technical Documentation", EIOPA-BoS-26/198, Annex D.8. <https://www.eiopa.europa.eu/eiopa-publishes-rfr-technical-documentation-become-applicable-30-january-2027-2026-05-26_en>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
breakeven_forward(
    elapsed_time: float | np.ndarray,
    params: DeterministicPathParams,
) -> float | np.ndarray
```

**Args:**

- <u>elapsed_time (float &#124; np.ndarray):</u> years since the valuation date.
- <u>params (DeterministicPathParams):</u> today's breakeven curve and its shortest quoted maturity.

**Returns:**

<u>float &#124; np.ndarray:</u> the breakeven forward, one value per time given.

</details>

#### breakeven_inflation_centre

The path risk-neutral inflation is centred on: the breakeven forward minus the convexity correction that keeps
the expected price index on the breakeven curve.

The formula is as follows:

$$
\alpha_{I}(t) = f_{BE}(0,\; t) - \sigma ^{2} / (2 \cdot a ^{2}) \cdot (1 - \exp(- a \cdot t)) ^{2}
$$

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
breakeven_inflation_centre(
    elapsed_time: float | np.ndarray,
    params: BreakevenInflationParams,
) -> float | np.ndarray
```

**Args:**

- <u>elapsed_time (float &#124; np.ndarray):</u> years since the valuation date.
- <u>params (BreakevenInflationParams):</u> today's breakeven curve and the historical speed and volatility.

**Returns:**

<u>float &#124; np.ndarray:</u> alpha_I(t), one value per time given.

</details>

#### step_breakeven_inflation

Move risk-neutral inflation one step: the force of inflation's gap to the breakeven-implied path decays at the
fitted speed and takes a normal shock, the exact Ornstein-Uhlenbeck transition.

The formula is as follows:

$$
x(t + \text{dt}) = \alpha_{I}(t + \text{dt}) + (x(t) - \alpha_{I}(t)) \cdot \exp(- a \cdot \text{dt}) + s \cdot z,\;\; x = \ln(1 + \pi)
$$

$$
s = \sigma \cdot \sqrt{(1 - \exp(- 2 \cdot a \cdot \text{dt})) / (2 \cdot a)}
$$

$$
\pi(t + \text{dt}) = \exp(x(t + \text{dt})) - 1
$$

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_breakeven_inflation(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    elapsed_time: float,
    params: BreakevenInflationParams,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> this step's inflation in each scenario.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw.
- <u>time_step (float):</u> the step length, in years.
- <u>elapsed_time (float):</u> years since the valuation date at the start of this step.
- <u>params (BreakevenInflationParams):</u> today's breakeven curve and the historical speed and volatility.

**Returns:**

<u>np.ndarray:</u> inflation one step later, as a year-over-year rate.

</details>

#### fit_regime_switching_inflation

Fit two inflation regimes, calm and high, on observations a year apart: each regime's long-run level and yearly
shock size, one shared persistence, and the yearly chances of switching between them.

A single mean-reverting process fitted on calm decades cannot produce a 1970s or a 2021-22: from a 2019 start its
90% band for 2021 ended near 4%, against the 7.0% that came. Inflation has spent long stretches in two different
states, a calm one near its target with small shocks and a high one with large shocks, and moves between them
rarely. Hamilton (1989, section 2, eq. 2.2, p. 360) models such a hidden state as a Markov chain and gives the
filter that infers it and the likelihood (section 4.2, pp. 367-368, started from the long-run regime shares as on
p. 368). Harris (1999, section 2, p. 49) gives each regime its own mean, persistence and shock size, and in
quarterly Australian data finds a turbulent regime in which the change in inflation is about three times as
volatile (section 4, Table 2, p. 57). Here the persistence is shared and each regime is Wilkie's yearly AR(1).

Year-over-year rates sampled monthly overlap, so the history is read as 12 interleaved yearly series (every
January, every February, ...), each value paired with the one a year earlier, as `fit_inflation_ou` does. The 12
series are not independent, so their summed log-likelihood is a composite likelihood (Lindsay (1988)): maximizing
it gives consistent estimates, but it is not a full likelihood, so the information criteria and likelihood-ratio
tests that assume one do not apply to it. It is divided by 12 (one yearly series' worth) and maximized (Powell's
method) from three fixed starting points; a month missing inside the history is predicted through, not fitted.

The formula is as follows:

$$
I_{t} = \mu_{s} + \text{QA} \cdot (I_{t-1} - \mu_{s}) + \text{QSD}_{s} \cdot e_{t},\;\; \text{s the regime in year t}
$$

$$
P(s_{t} = j | s_{t-1} = i) = p_{ij}
$$

**References:**

- Hamilton, J.D. (1989). "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle." Econometrica, 57(2), 357-384. <https://doi.org/10.2307/1912559>
- Harris, G.R. (1999). "Markov Chain Monte Carlo Estimation of Regime Switching Vector Autoregressions." ASTIN Bulletin, 29(1), 47-79. <https://doi.org/10.2143/AST.29.1.504606>
- Lindsay, B.G. (1988). "Composite Likelihood Methods." Contemporary Mathematics, 80, 221-239. <https://doi.org/10.1090/conm/080/999014>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_regime_switching_inflation(
    inflation_rate: pl.Series,
    steps_per_year: int = 1,
    short_history_chosen: bool = False,
) -> InflationRegimeParams
```

**Args:**

- <u>inflation_rate (pl.Series):</u> the year-over-year inflation history, evenly spaced, as decimals; use a long one.
- <u>steps_per_year (int):</u> observations per year (12 monthly, 4 quarterly, 1 yearly). Defaults to 1.
- <u>short_history_chosen (bool):</u> the history starts where the configuration chose (`history_start_year`), so a short one is noted at INFO rather than warned about. Defaults to False.

**Returns:**

<u>InflationRegimeParams:</u> the two regimes, calm first, today's regime probabilities and the latest rate.

**Raises:**

- <u>ValueError:</u> if the history has fewer than 10 years, or inflation shows no pull toward its regime's level.

</details>

{% raw %}
#### shift_regime_mean

Move both regimes' levels by the same amount so the long-run mean of inflation is `long_run_mean`, keeping the gap
between the regimes, their shocks, the persistence and the chances of switching: what a belief `long_run_mean` of
one level does on a regime-switching entry, the same move a `BeliefPath` makes step by step
(`regime_level_shifts`).

The long-run mean is each regime's level weighted by its long-run share of time, and the two regimes share one
speed, so moving both levels by the same amount moves every scenario's inflation by that amount once today's start
has worn off: the whole long-run distribution, spikes included, moves with it. Any level can be met this way, 12%
as well as mild deflation.

The formula is as follows:

$$
\text{mu\_k'} = \mu_{k} + (m - m_{0}),\;\; \text{for both regimes k}
$$

$$
m_{0} = s_{\text{calm}} \cdot \text{mu\_calm} + s_{\text{high}} \cdot \text{mu\_high},\;\; s_{\text{high}} = (1 - p_{00}) / (2 - p_{00} - p_{11})
$$

Where m is `long_run_mean` and m_0 the regimes' long-run mean before the move.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
shift_regime_mean(params: InflationRegimeParams, long_run_mean: float) -> InflationRegimeParams
```

**Args:**

- <u>params (InflationRegimeParams):</u> the regimes, anchored or as fitted.
- <u>long_run_mean (float):</u> the long-run mean inflation to meet, a yearly decimal.

**Returns:**

<u>InflationRegimeParams:</u> the regimes with both levels moved, anchored to `long_run_mean`.

</details>
{% endraw %}

#### fit_unemployment_process

Estimate how unemployment returns to its normal level and how it moves with inflation, from a country's history.

The model is the Phillips-curve-augmented mean-reverting process of Ahlgrim, D'Arcy and Gorvett (2005, eq.
3.19-3.21). It assumes unemployment is pulled toward a natural rate (frictional and structural unemployment that
persists through the cycle) and that a rise in inflation comes with a tighter labour market, as Phillips (1958)
found for UK wages. The fit is one regression of each period's change in unemployment on its previous level and the
same period's change in inflation: the level term gives the speed and the natural rate, the inflation term the
Phillips-curve sensitivity alpha_u, expected to be negative. This is the paper's own regression, eq. 3.21, with the
same-period change in inflation, as the paper keeps it simple and uses no distributed lags (section 3,
Unemployment). On US monthly data from 1948 to 2001 they find a speed of 0.13, a natural rate of
6.1%, alpha_u of -0.72 and a volatility of 0.76% (eq. 3.22). With a business-cycle series, the leading indicator's
change enters as a second driver next to inflation, never in its place; that second term is this package's
extension, built the same way as the paper's inflation term.

The formula is as follows:

$$
u(t) - u(t-1) = c + b \cdot u(t-1) + \alpha_{u} \cdot (\pi(t) - \pi(t-1)) + \gamma_{u} \cdot (\operatorname{CLI}(t) - \operatorname{CLI}(t-1)) + e(t)
$$

$$
\kappa_{u} = - \ln(1 + b) / \text{dt},\;\; \mu_{u} = - c / b
$$

Without a business-cycle series the gamma_u term is dropped. The Phillips curve is a statistical link fitted to
history; it has flattened in many countries since the 1990s, so expect a small sensitivity on recent data.

**References:**

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Phillips, A.W. (1958). "The Relation Between Unemployment and the Rate of Change of Money Wage Rates in the United Kingdom, 1861-1957." Economica, 25(100), 283-299. <https://doi.org/10.1111/j.1468-0335.1958.tb00003.x>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_unemployment_process(
    unemployment: pl.Series,
    inflation: pl.Series,
    time_step: float,
    business_cycle: pl.Series | None = None,
) -> UnemploymentParams
```

**Args:**

- <u>unemployment (pl.Series):</u> the historical unemployment rate, evenly spaced.
- <u>inflation (pl.Series):</u> the historical inflation rate on the same dates.
- <u>time_step (float):</u> the time between observations, in years.
- <u>business_cycle (pl.Series &#124; None):</u> the leading indicator's level on the same dates, a second driver next to inflation; None (the default) uses inflation only.

**Returns:**

<u>UnemploymentParams:</u> the reversion speed, natural rate, inflation sensitivity, volatility and the latest rate as the starting point, plus `business_cycle_sensitivity` with a business-cycle series.

**Raises:**

- <u>ValueError:</u> if the series differ in length, too few dates have both values, or unemployment shows no pull toward a normal level.

</details>

#### step_unemployment

Move the unemployment rate one step forward: pulled toward its natural rate and pushed by the simulated change in
inflation (and, if configured, in the leading indicator, and by the equity market and the yield curve half a year
earlier).

Because the inflation term uses the same scenario's simulated inflation move, unemployment and inflation stay
linked path by path: an inflation surge tends to come with falling unemployment, and a disinflation with rising
unemployment, on top of whatever correlation their own shocks have. The cycle links work the same way: a scenario
whose equity market falls, or whose yield curve inverts, sees its unemployment rise over the following year. The
mean-reverting part uses the exact transition, so a gap to the natural rate halves in ln(2) / kappa_u years
whatever the step size.

The formula is as follows:

$$
u(t + \text{dt}) = \mu_{u} + (u(t) - \mu_{u}) \cdot \exp(- \kappa_{u} \cdot \text{dt}) + \alpha_{u} \cdot d\pi + \gamma_{u} \cdot \text{dCLI} + w \cdot c \cdot \text{dt} + s \cdot z
$$

$$
c = \beta_{R} \cdot \min(g_{R},\; 0) + \beta_{S} \cdot g_{S}
$$

$$
s = \sigma_{u} \cdot \sqrt{(1 - \exp(- 2 \cdot \kappa_{u} \cdot \text{dt})) / (2 \cdot \kappa_{u})}
$$

Where dpi and dCLI are the simulated inflation and leading-indicator changes over the same step, g_R the equity
market's log return over the year ending `equity_lag` earlier less its normal return, g_S the long minus short rate
`term_spread_lag` earlier less its average over the `spread_baseline` years ending a year before that, w =
`yearly_sensitivity_weight(kappa_u, dt)` and z a standard normal draw. The result is clipped to [0, 1], since a
rate is a share of the labour force: the normal shock alone could push a few paths (about 0.3% of monthly paths in
a default run) below zero.

With regimes, each scenario's regime over the step (`RecessionChain`) sets the volatility, and a recession adds the
push D_r * (1 - exp(-kappa_u * dt)) / kappa_u; the cycle links then act through the chance of a recession, not here.

**References:**

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Phillips, A.W. (1958). "The Relation Between Unemployment and the Rate of Change of Money Wage Rates in the United Kingdom, 1861-1957." Economica, 25(100), 283-299. <https://doi.org/10.1111/j.1468-0335.1958.tb00003.x>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_unemployment(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: UnemploymentParams,
    inflation_change: np.ndarray | float,
    business_cycle_change: np.ndarray | float | None = None,
    equity_return_gap: np.ndarray | float | None = None,
    term_spread_gap: np.ndarray | float | None = None,
    regime: np.ndarray | None = None,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's unemployment rate.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw.
- <u>time_step (float):</u> the step length, in years.
- <u>params (UnemploymentParams):</u> the reversion speed, natural rate, inflation sensitivity, volatility and, if fitted, the business-cycle and cycle-link sensitivities.
- <u>inflation_change (np.ndarray &#124; float):</u> the simulated change in inflation over the same step.
- <u>business_cycle_change (np.ndarray &#124; float &#124; None):</u> the simulated change in the leading indicator over the same step; required when a business-cycle sensitivity was fitted.
- <u>equity_return_gap (np.ndarray &#124; float &#124; None):</u> g_R; required when an equity sensitivity was fitted.
- <u>term_spread_gap (np.ndarray &#124; float &#124; None):</u> g_S; required when a term-spread sensitivity was fitted.
- <u>regime (np.ndarray &#124; None):</u> each scenario's regime over the step, 0 for expansion and 1 for recession; required with regimes.

**Returns:**

<u>np.ndarray:</u> the unemployment rate one step later, between 0 and 1.

**Raises:**

- <u>ValueError:</u> if a sensitivity was fitted but its driver is not given, or the process has regimes and no regime is given.

</details>

#### calm_level

The level unemployment settles at in a long calm stretch: its long-run average less the average push of the
recessions (with regimes) or of the bear markets (with the equity link), so the average over the cycle stays the
long-run mean. Without either it is the long-run mean.

The formula is as follows:

$$
\text{with regimes:}\;\; \text{mu\_calm} = \mu_{u} - D_{r} \cdot \pi_{r} / \kappa_{u}
$$

$$
\text{with the equity link:}\;\; \text{mu\_calm} = \mu_{u} - \beta_{R} \cdot s_{R} / (1 - \exp(- \kappa_{u}))
$$

Where pi_r is the long-run share of months in recession and s_R the average shortfall of the equity's
trailing-year return. The first is the exact long-run mean of a mean-reverting process whose drift switches with
the regime; in the second, 1 - exp(-kappa_u) is the share of a gap closed in a year, so a push of beta_R * s_R a
year holds unemployment that far above its calm level.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calm_level(params: UnemploymentParams) -> float
```

**Args:**

- <u>params (UnemploymentParams):</u> the process.

**Returns:**

<u>float:</u> the calm level.

</details>

#### yearly_cycle_observations

Turn monthly history into one row per December: the year's change in unemployment and the cycle signals behind it,
the inputs of `fit_unemployment_history` and `fit_cycle_links`.

The change runs December to December, so no month enters two observations, as the package's other yearly fits do
for overlapping year-over-year rates. Each signal is the yearly sum of what the simulation's step reads month by
month, so a fitted sensitivity carries over to any step. The equity signal averages, over the year's months, the
shortfall of the market's log return over the 12 months ending `equity_lag_months` before each month below its
average over the history; returns above it count as zero. The spread signal is the average long minus short rate
over the 12 months ending `spread_lag_months` before December, less its average over the `baseline_months` before
them, so a curve that has been flat or steep for years is no signal by itself; in history the two readings carry
the same information, as the US curve never stayed inverted for long.

The formula is as follows:

$$
\operatorname{du}(t) = u(\text{Dec}\; t) - u(\text{Dec}\; t-1),\;\; \operatorname{dpi}(t) = \pi(\text{Dec}\; t) - \pi(\text{Dec}\; t-1)
$$

$$
D(t) = \text{mean over the months}\; m \;\text{of year}\; t \;\text{of min} (\text{ln}\; S (m - l_{R}) - \text{ln}\; S (m - l_{R} - 12) - m_{R},\; 0)
$$

$$
U(t) = \text{the same with max} (...,\; 0),\;\; \text{the upside the fit tests and leaves out}
$$

$$
G(t) = \text{mean of}\; L - i \;\text{over the}\; 12 \;\text{months ending Dec}\; t - l_{S},\;\; \text{less its mean over the b months before them}
$$

Where l_R and l_S are the lags, b `baseline_months`, S the equity total-return index, m_R its average 12-month log
return over the months with unemployment data, L and i the long and short rate.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
yearly_cycle_observations(
    monthly: pl.DataFrame,
    equity_lag_months: int = EQUITY_LAG_MONTHS,
    spread_lag_months: int = SPREAD_LAG_MONTHS,
    baseline_months: int = SPREAD_BASELINE_MONTHS,
) -> pl.DataFrame
```

**Args:**

- <u>monthly (pl.DataFrame):</u> one row per calendar month, contiguous and in order, with `date`, `unemployment` and `inflation`, plus `equity` (a total-return index level) and/or `short_rate` and `long_rate`, as decimals.
- <u>equity_lag_months (int):</u> l_R. Defaults to `EQUITY_LAG_MONTHS`.
- <u>spread_lag_months (int):</u> l_S. Defaults to `SPREAD_LAG_MONTHS`.
- <u>baseline_months (int):</u> b. Defaults to `SPREAD_BASELINE_MONTHS`.

**Returns:**

<u>pl.DataFrame:</u> `year`, `change`, `level`, `inflation_change`, plus `equity_shortfall`, `equity_upside` and `equity_normal_return` and/or `term_spread_gap`; rows with a missing value are kept as nulls.

**Raises:**

- <u>ValueError:</u> if the months are not contiguous or a lag or the baseline is out of range.

</details>

#### fit_unemployment_history

Estimate how unemployment returns to its normal level and moves with inflation from decades of December-to-December
changes, so one extraordinary month cannot set the dynamics of every scenario.

A fit on the recent window reads its speed and volatility from whatever that window holds. Since 2000 that is
dominated by April 2020, when US unemployment jumped ten points in a month: that single residual sets the monthly
fit's volatility at 2.2% a year (0.55% without March to December 2020) and its speed at 0.62 (0.03 without them),
so scenarios spend one month in seven below 3.4%, the lowest US rate since 1955. This fit runs the same regression as
`fit_unemployment_process` on yearly changes since the 1950s instead, the annual regressions Ahlgrim, D'Arcy and
Gorvett (2005, section 3) chose because monthly data are noisy: no month enters two observations, and 2020 is one
year in seventy (+3.1 points December to December). On US data from 1957 to 2025 it gives a speed of 0.31, a
natural rate of 5.8%, a Phillips-curve sensitivity of -0.20 and a volatility of 1.1% a year; leaving 2020 out moves
the speed to 0.26 and the volatility by 4%.

The formula is as follows:

$$
u(t) - u(t-1) = c + b \cdot u(t-1) + \alpha_{u} \cdot (\pi(t) - \pi(t-1)) + e(t),\;\; \text{one row per December}
$$

$$
\kappa_{u} = - \ln(1 + b),\;\; \mu_{u} = - c / b,\;\; \sigma_{u} = \operatorname{std}(e) / \sqrt{(1 - \exp(- 2 \cdot \kappa_{u})) / (2 \cdot \kappa_{u})}
$$

**References:**

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. Section 3. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_unemployment_history(observations: pl.DataFrame) -> UnemploymentParams
```

**Args:**

- <u>observations (pl.DataFrame):</u> `yearly_cycle_observations`' output; only `change`, `level` and `inflation_change` are used.

**Returns:**

<u>UnemploymentParams:</u> the speed, natural rate, inflation sensitivity and volatility, with `fit_time_step` 1.0 and the last December's rate as `initial_value` (replace it with today's to start a run from now).

**Raises:**

- <u>ValueError:</u> if fewer than `MINIMUM_CYCLE_YEARS` years have every value or unemployment shows no pull toward a normal level.

</details>

#### fit_cycle_links

Estimate how far unemployment rises after the equity market falls short or the yield curve flattens, from decades
of yearly history.

Unemployment and output move together over the business cycle: Okun (1962, p. 99) finds that each percentage
point of unemployment above 4% came with about 3% less output in the postwar US. Markets see the cycle coming:
a steeper yield curve predicts faster growth over the next six to seven quarters (Estrella and Hardouvelis (1991,
section II.C, p. 559)), and the spread and stock prices are the most useful financial predictors of a recession, the
curve especially two to six quarters ahead and stock prices up to four (Estrella and Mishkin (1998, p. 50)).
Recessions are also short and sharp next to long, gradual expansions: unemployment rises faster than it falls (Neftçi
(1984); Sichel (1993)). This fit measures the links on unemployment itself, as one regression of each year's change on
its level, inflation's change and the signals of `yearly_cycle_observations`, the regression of
`fit_unemployment_history` with the links added. By the Frisch-Waugh-Lovell theorem (Frisch and Waugh (1933); Lovell
(1963)) each link's coefficient is then what the signal explains once the level and inflation are partialled out of
both unemployment's change and the signal; regressing only the residual of a regression without the links on the raw
signals would leave the part of the signals the level explains in and bias the links. Only a shortfall of equity
returns enters, since on US data returns above normal do not speed unemployment's fall (`equity_upside_sensitivity`,
near zero), so it rises sharply after a bear market and comes back down at its own pace.

The formula is as follows:

$$
\operatorname{du}(t) = c + b \cdot u(t-1) + a \cdot \operatorname{dpi}(t) + \beta_{R} \cdot D(t) + \beta_{S} \cdot G(t) + v(t)
$$

$$
\kappa_{u} = - \ln(1 + b),\;\; \text{mu\_calm} = c / - b,\;\; \mu_{u} = \text{mu\_calm} + \beta_{R} \cdot \operatorname{mean}(D) / - b
$$

$$
\sigma_{u} = \operatorname{std}(v) / \sqrt{(1 - \exp(- 2 \cdot \kappa_{u})) / (2 \cdot \kappa_{u})}
$$

The share the links explain is 1 - var(v) / var(e) over the same years, e the residual without the links.

**References:**

- Okun, A.M. (1962). "Potential GNP: Its Measurement and Significance." Proceedings of the Business and Economic Statistics Section, American Statistical Association, 98-104. Cowles Foundation Paper 190. <https://cowles.yale.edu/node/142137>
- Estrella, A., Hardouvelis, G.A. (1991). "The Term Structure as a Predictor of Real Economic Activity." Journal of Finance, 46(2), 555-576. <https://doi.org/10.1111/j.1540-6261.1991.tb02674.x>
- Estrella, A., Mishkin, F.S. (1998). "Predicting U.S. Recessions: Financial Variables as Leading Indicators." Review of Economics and Statistics, 80(1), 45-61. <https://doi.org/10.1162/003465398557320>
- Neftçi, S.N. (1984). "Are Economic Time Series Asymmetric over the Business Cycle?" Journal of Political Economy, 92(2), 307-328. <https://doi.org/10.1086/261226>
- Sichel, D.E. (1993). "Business Cycle Asymmetry: A Deeper Look." Economic Inquiry, 31(2), 224-236. <https://doi.org/10.1111/j.1465-7295.1993.tb00879.x>
- Frisch, R., Waugh, F.V. (1933). "Partial Time Regressions as Compared with Individual Trends." Econometrica, 1(4), 387-401. <https://doi.org/10.2307/1907330>
- Lovell, M.C. (1963). "Seasonal Adjustment of Economic Time Series and Multiple Regression Analysis." Journal of the American Statistical Association, 58(304), 993-1010. <https://doi.org/10.1080/01621459.1963.10480682>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_cycle_links(
    observations: pl.DataFrame,
    equity_lag: float = EQUITY_LAG_MONTHS / _MONTHS_PER_YEAR,
    term_spread_lag: float = SPREAD_LAG_MONTHS / _MONTHS_PER_YEAR,
    spread_baseline: float = SPREAD_BASELINE_MONTHS / _MONTHS_PER_YEAR,
) -> CycleLinkFit
```

**Args:**

- <u>observations (pl.DataFrame):</u> `yearly_cycle_observations`' output, with `equity_shortfall` and/or `term_spread_gap`.
- <u>equity_lag (float):</u> the equity signal's lag, in years. Defaults to a quarter.
- <u>term_spread_lag (float):</u> the spread signal's lag, in years. Defaults to half a year.
- <u>spread_baseline (float):</u> the years the spread gap was measured against. Defaults to five.

**Returns:**

<u>CycleLinkFit:</u> the process, the sensitivities, their standard errors and normal levels, and the variance they explain.

**Raises:**

- <u>ValueError:</u> if neither signal is present, fewer than `MINIMUM_CYCLE_YEARS` years have every value, or unemployment shows no pull toward a normal level.

</details>

#### monthly_regime_observations

Turn monthly history into one row per month: unemployment's change over the month, its level before, inflation's
change and the two cycle signals exactly as a scenario's monthly step reads them, the inputs of
`fit_unemployment_regimes`.

The equity signal is the market's log return over the 12 months ending `equity_lag_months` before the month's end,
less its average over the months with unemployment data; the slope signal is the long minus short rate
`spread_lag_months` before the month's end, less its average over the `baseline_months` ending a year before that.
These are the reads of `CycleLinkReader`, so a sensitivity fitted here acts in a run as it did in history, and both
are known before the month starts.

The formula is as follows:

$$
\operatorname{du}(t) = u(t) - u(t-1),\;\; \operatorname{dpi}(t) = \pi(t) - \pi(t-1)
$$

$$
R(t) = \text{ln}\; S (t - l_{R}) - \text{ln}\; S (t - l_{R} - 12) - m_{R}
$$

$$
G(t) = \operatorname{Sp}(t - l_{S}) - \text{mean of Sp over the}\; b \;\text{months ending}\; t - l_{S} - 12
$$

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
monthly_regime_observations(
    monthly: pl.DataFrame,
    equity_lag_months: int = EQUITY_LAG_MONTHS,
    spread_lag_months: int = SPREAD_LAG_MONTHS,
    baseline_months: int = SPREAD_BASELINE_MONTHS,
) -> pl.DataFrame
```

**Args:**

- <u>monthly (pl.DataFrame):</u> one row per calendar month, contiguous and in order, with `date`, `unemployment` and `inflation`, plus `equity` (a total-return index level) and/or `short_rate` and `long_rate`, as decimals.
- <u>equity_lag_months (int):</u> l_R. Defaults to `EQUITY_LAG_MONTHS`.
- <u>spread_lag_months (int):</u> l_S. Defaults to `SPREAD_LAG_MONTHS`.
- <u>baseline_months (int):</u> b. Defaults to `SPREAD_BASELINE_MONTHS`.

**Returns:**

<u>pl.DataFrame:</u> `date`, `unemployment`, `change`, `level`, `inflation_change`, plus `equity_return_gap` and `equity_normal_return` and/or `term_spread_gap`; missing values are nulls.

**Raises:**

- <u>ValueError:</u> if the months are not contiguous or a lag or the baseline is out of range.

</details>

{% raw %}
#### fit_unemployment_regimes

Find the expansions and recessions in a country's monthly unemployment history: the slow decline of a long expansion
and the sharp rise of a recession, each with its own pace and noise, and how likely and how long each is.

Unemployment does not move like one bell curve of shocks around a trend. It rises fast in recessions and falls
slowly in expansions, an asymmetry Neftçi (1984) and Sichel (1993) document for the US rate and regime and threshold
models of it build on (Montgomery, Zarnowitz, Tsay and Tiao (1998)). One normal shock fitted to the average month
gives a recession like 2008-09, five points in two years, almost no chance. This fit follows Hamilton (1989), who
presents his model as an extension of Neftçi's states of rising and falling unemployment (p. 359): unemployment's
monthly change is a regression whose intercept and noise depend on an unobserved regime, expansion or recession,
that switches as a Markov chain (section 2, eq. 2.1-2.2). His filter, started from the long-run shares of the two
regimes, gives the likelihood and each month's chance of a recession (section 4.2, pp. 367-369); the parameters
maximise the likelihood from several starting splits (by the residual's sign, its size and the recessions'
persistence), keeping the best. The pull back to a calm level and the Phillips-curve term of Ahlgrim, D'Arcy and
Gorvett (2005, eq. 3.21) stay in the regression. The NBER's dates are no input: on US data since 1956 the fit puts
13% of months in recession, in spells of ten months on average, against 12% and 10.3 months for the NBER's
recessions since 1955.

With `equity` and/or `term_spread`, the chance of a recession starting moves with the cycle links' signals
(`monthly_regime_observations`), the time-varying transition probabilities of Filardo (1994), fitted jointly by
maximum likelihood; an inverted curve and falling stock prices are the financial signs Estrella and Mishkin (1998)
find most useful ahead of a recession. The chance of a recession ending stays fixed. Every US recession since 1969
followed one of the two signals, so their slopes would run off to infinity (separation); each slope therefore
carries the default prior of Gelman, Jakulin, Pittau and Su (2008, sections 2.1-2.2), a Cauchy with scale 2.5 for an
input scaled to a standard deviation of 0.5, and the fit is that posterior's mode. The months in `excluded_months`
(by default the 2020 pandemic, `PANDEMIC_MONTHS`) do not enter the likelihood and the filter carries the regime
probabilities through them, as Lenza and Primiceri (2022, sections 1 and 4) find acceptable for estimating
parameters; a lockdown jump like April 2020's is then outside what the regimes produce.

The formula is as follows:

$$
\operatorname{du}(t) = c_{k} + b \cdot u(t-1) + \alpha_{u} \cdot \operatorname{dpi}(t) + s_{k} \cdot e(t),\;\; \text{k the regime in month t}
$$

$$
P(k(t) = \text{recession} | k(t-1) = \text{expansion}) = 1 / (1 + \exp(- (a + g_{R} \cdot \min(R(t),\; 0) + g_{S} \cdot G(t))))
$$

$$
\kappa_{u} = - 12 \cdot \ln(1 + b),\;\; \text{mu\_calm} = c_{\text{expansion}} / - b,\;\; D_{r} = (c_{\text{recession}} - c_{\text{expansion}}) \cdot \kappa_{u} / - b
$$

$$
\mu_{u} = \text{mu\_calm} + D_{r} \cdot \pi_{r} / \kappa_{u},\;\; \text{the long-run average},\;\; \text{with pi\_r the long-run share in recession}
$$

$$
\sigma_{k} = s_{k} / \sqrt{(1 - \exp(- 2 \cdot \kappa_{u} / 12)) / (2 \cdot \kappa_{u})}
$$

**References:**

- Hamilton, J.D. (1989). "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle." Econometrica, 57(2), 357-384. <https://doi.org/10.2307/1912559>
- Filardo, A.J. (1994). "Business-Cycle Phases and Their Transitional Dynamics." Journal of Business & Economic Statistics, 12(3), 299-308. <https://doi.org/10.1080/07350015.1994.10524545>
- Montgomery, A.L., Zarnowitz, V., Tsay, R.S., Tiao, G.C. (1998). "Forecasting the U.S. Unemployment Rate." Journal of the American Statistical Association, 93(442), 478-493. <https://doi.org/10.1080/01621459.1998.10473696>
- Neftçi, S.N. (1984). "Are Economic Time Series Asymmetric over the Business Cycle?" Journal of Political Economy, 92(2), 307-328. <https://doi.org/10.1086/261226>
- Sichel, D.E. (1993). "Business Cycle Asymmetry: A Deeper Look." Economic Inquiry, 31(2), 224-236. <https://doi.org/10.1111/j.1465-7295.1993.tb00879.x>
- Estrella, A., Mishkin, F.S. (1998). "Predicting U.S. Recessions: Financial Variables as Leading Indicators." Review of Economics and Statistics, 80(1), 45-61. <https://doi.org/10.1162/003465398557320>
- Gelman, A., Jakulin, A., Pittau, M.G., Su, Y.-S. (2008). "A Weakly Informative Default Prior Distribution for Logistic and Other Regression Models." Annals of Applied Statistics, 2(4), 1360-1383. <https://doi.org/10.1214/08-AOAS191>
- Lenza, M., Primiceri, G.E. (2022). "How to Estimate a Vector Autoregression after March 2020." Journal of Applied Econometrics, 37(4), 688-699. <https://doi.org/10.1002/jae.2895>
- NBER, US Business Cycle Expansions and Contractions. <https://www.nber.org/research/data/us-business-cycle-expansions-and-contractions>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_unemployment_regimes(
    monthly: pl.DataFrame,
    equity: bool = False,
    term_spread: bool = False,
    excluded_months: tuple[date, date] | None = PANDEMIC_MONTHS,
    first_month: date | None = None,
) -> UnemploymentRegimeFit
```

**Args:**

- <u>monthly (pl.DataFrame):</u> monthly history as `monthly_regime_observations` takes it.
- <u>equity (bool):</u> let a shortfall in the equity market's trailing-year return raise the chance of a recession. Defaults to False.
- <u>term_spread (bool):</u> let a flatter curve than over the five years before raise it. Defaults to False.
- <u>excluded_months (tuple[date, date] &#124; None):</u> the first and last month left out of the likelihood; None keeps every month. Defaults to `PANDEMIC_MONTHS`.
- <u>first_month (date &#124; None):</u> fit on the months from this one on, such as an era of one monetary regime; the signals still read the months before it. None (the default) takes every month.

**Returns:**

<u>UnemploymentRegimeFit:</u> the process, the regimes, the start and the likelihoods.

**Raises:**

- <u>ValueError:</u> if a link's columns are missing, fewer than `MINIMUM_REGIME_MONTHS` months have every value, or unemployment shows no pull toward a calm level.

</details>
{% endraw %}

#### recession_switch_probabilities

The chance of a recession starting and of one lasting, over one scenario step, given the cycle links' reads.

The fitted chances are per month. For another step they come from the monthly chain held for that many months (the
two-regime closed form of `rescale_transition_matrix`), so expansions and recessions last as long in calendar time
at any step; within a longer step the links' reads are taken as held.

The formula is as follows:

$$
q = 1 / (1 + \exp(- (a + g_{R} \cdot \min(R,\; 0) + g_{S} \cdot G))),\;\; p = p_{rr}
$$

$$
\text{over} \;\; n = \text{dt} / \text{month}\; \text{months:} \pi = q / (q + 1 - p),\;\; \lambda = \max(p - q,\; 0)
$$

$$
q_{n} = \pi \cdot (1 - \lambda ^{n}),\;\; p_{n} = \pi + (1 - \pi) \cdot \lambda ^{n}
$$

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
recession_switch_probabilities(
    regimes: UnemploymentRegimes,
    time_step: float,
    equity_return_gap: np.ndarray | float | None = None,
    term_spread_gap: np.ndarray | float | None = None,
) -> tuple[np.ndarray, np.ndarray]
```

**Args:**

- <u>regimes (UnemploymentRegimes):</u> the fitted regimes.
- <u>time_step (float):</u> the step in years.
- <u>equity_return_gap (np.ndarray &#124; float &#124; None):</u> R, the equity's trailing-year log return against normal; required with the equity link.
- <u>term_spread_gap (np.ndarray &#124; float &#124; None):</u> G, the slope against its recent average; required with the slope link.

**Returns:**

<u>tuple[np.ndarray, np.ndarray]:</u> per scenario, the chance of a recession starting during the step from an expansion and of a recession still running at its end.

**Raises:**

- <u>ValueError:</u> if a link was fitted but its read is not given.

</details>

#### cbd_mortality_rate

The one-year probability of death at a given age in a simulated year, read back from the two Cairns-Blake-Dowd
factors: the level `kappa1` and the age slope `kappa2`.

The model assumes that, at pension ages, the log-odds of dying rise in a straight line with age, so two numbers
per year describe the whole table: how high mortality is at the mean age and how fast it climbs with every extra
year of age. Feeding in simulated factor paths gives a death probability per scenario and year, the input for an
annuity or pension liability, and an improving `kappa1` lowers mortality at every age at once. Working on the
logit keeps every probability between 0 and 1, however far a scenario runs, as in
[Cairns, Blake and Dowd (2006)](https://doi.org/10.1111/j.1539-6975.2006.00195.x).

The formula is as follows:

$$
\text{logit}\; q (x,\; t) = \operatorname{kappa1}(t) + \operatorname{kappa2}(t) \cdot (x - \text{xbar})
$$

$$
q(x,\; t) = 1 / (1 + \exp(- (\operatorname{kappa1}(t) + \operatorname{kappa2}(t) \cdot (x - \text{xbar}))))
$$

Where xbar is the mean age of the fit.

**References:**

- Cairns, A.J.G., Blake, D., Dowd, K. (2006). "A Two-Factor Model for Stochastic Mortality with Parameter Uncertainty: Theory and Calibration." Journal of Risk and Insurance, 73(4), 687-718. <https://doi.org/10.1111/j.1539-6975.2006.00195.x>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
cbd_mortality_rate(
    kappa1: float | np.ndarray,
    kappa2: float | np.ndarray,
    age: float,
    mean_age: float,
    min_age: float | None = None,
    max_age: float | None = None,
) -> float | np.ndarray
```

**Args:**

- <u>kappa1 (float &#124; np.ndarray):</u> the simulated mortality level.
- <u>kappa2 (float &#124; np.ndarray):</u> the simulated age slope.
- <u>age (float):</u> the age to read the death probability for.
- <u>mean_age (float):</u> the mean age of the fitted ages, `mean_age` in the calibrated parameters.
- <u>min_age (float &#124; None):</u> the youngest fitted age; with `max_age`, warns when `age` lies outside the fitted range, where the straight-line logit is not validated. Defaults to None.
- <u>max_age (float &#124; None):</u> the oldest fitted age, paired with `min_age`. Defaults to None.

**Returns:**

<u>float &#124; np.ndarray:</u> the one-year death probability at `age`, per scenario and year when paths are passed.

</details>

#### fit_cbd_factors

Split each year's mortality table into the two Cairns-Blake-Dowd factors: the level `kappa1` and the age slope
`kappa2`, by regressing that year's log-odds of death on age.

This turns a table with dozens of ages per year into two time series, whose trend and volatility are what the
longevity scenarios project: a falling `kappa1` is mortality improvement at every age, a changing `kappa2` means
older ages improve faster or slower than younger ones. A straight line in age fits mortality well from about 60
upward, the range that matters for pensions and annuities, see
[Cairns, Blake and Dowd (2006)](https://doi.org/10.1111/j.1539-6975.2006.00195.x), fitted the paper's way:
for each year, a least-squares regression of the ungraduated log-odds of death log(q/p) on age, as in Cairns, Blake
and Dowd (2006, footnote 8).

The formula is as follows:

$$
\ln(q(x_{j},\; t) / (1 - q(x_{j},\; t))) = \operatorname{kappa1}(t) + \operatorname{kappa2}(t) \cdot (x_{j} - \text{xbar}) + e_{t},\;\; \text{j}
$$

Where q(x_j, t) is the one-year probability of death at age x_j in year t and xbar the mean age.

**References:**

- Cairns, A.J.G., Blake, D., Dowd, K. (2006). "A Two-Factor Model for Stochastic Mortality with Parameter Uncertainty: Theory and Calibration." Journal of Risk and Insurance, 73(4), 687-718. <https://doi.org/10.1111/j.1539-6975.2006.00195.x>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_cbd_factors(mortality_rates: pl.DataFrame, ages: list[float]) -> tuple[pl.DataFrame, float]
```

**Args:**

- <u>mortality_rates (pl.DataFrame):</u> one row per calendar year, one column per age, of one-year death probabilities q(x, t), not central death rates m(x, t) (q = 1 - e^(-m)).
- <u>ages (list[float]):</u> the age of each column, strictly increasing.

**Returns:**

<u>tuple[pl.DataFrame, float]:</u> `kappa1` and `kappa2` per year, and the mean age the ages are centred on.

**Raises:**

- <u>ValueError:</u> if fewer than 2 ages are given, `ages` is not strictly increasing or does not match the columns, or a rate is not strictly between 0 and 1.

</details>
