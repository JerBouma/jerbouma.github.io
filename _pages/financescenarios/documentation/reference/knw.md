---
title: "Knw"
seo_title: "Knw Reference – Finance Scenarios"
excerpt: "The KNW model: interest rate and inflation fitted jointly."
description: "The KNW model: interest rate and inflation fitted jointly."
author_profile: false
permalink: /projects/financescenarios/docs/reference/knw
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

The KNW model: interest rate and inflation fitted jointly.

```python
from financescenarios.models.knw.knw_controller import Knw
```

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
[Koijen, Nijman & Werker (2010)](https://doi.org/10.1093/rfs/hhp058) and is specified in full in the
[CP2022 Technical Appendix (2022)](
https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix). This class keeps its
rate and inflation recursion (eq. 52) at constant volatility, which leaves a bivariate VAR(1): each variable is
regressed on the previous value of both ([Lutkepohl, 2005](https://doi.org/10.1007/978-3-540-27752-1)).

```text
r(t)  = c_r  + phi_rr*r(t-1)   + phi_r_pi*pi(t-1) + sigma_r*z_r(t)
pi(t) = c_pi + phi_pi_r*r(t-1) + phi_pipi*pi(t-1) + sigma_pi*z_pi(t)
```

`KnwSv` adds DNB's stochastic volatility back, and `KnwSvQ` builds a risk-neutral version on top of that.

The data come from the Finance Toolkit without an API key: the rate from a Treasury-yield ticker or an OECD
country's short or long rate, inflation from OECD consumer price index growth. OECD data are not daily or
weekly, so a pair runs monthly, quarterly or yearly.

Configuration (both entries of a pair in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `interest_rates[i].method` | `hull_white` | Set to `knw` to make this entry the pair's rate leg. |
| `interest_rates[i].inflation_name` | `inflation` | The `name` of the paired `inflation[j]` entry. |
| `interest_rates[i].source` | `ticker` | `ticker` (set `ticker`, default `^IRX`) or `oecd` (set `country`, `term`). |
| `interest_rates[i].period` | `daily` | Shared by both legs and equal to `engine.frequency`. |
| `inflation[j].method` | `ou` | Set to `knw` to make this entry the pair's inflation leg. |
| `inflation[j].interest_rate_name` | `interest_rate` | The `name` of the paired `interest_rates[i]` entry. |
| `inflation[j].country` | `United States` | The country whose OECD consumer price index is used. |

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

## calibrate_pair

Calibrate one interest rate and inflation pair: fetch both histories and fit how each one pulls on the other.

For each leg you get how much of its own last value carries over (`own_persistence`), how much of the other
leg's last value spills into it (`cross_coupling`), a constant (`intercept`) and the size of its random
surprise per period (`volatility`). An `own_persistence` of 0.9 a quarter means half of a deviation is left
after ln(0.5) / ln(0.9) = 6.6 quarters, ignoring cross effects. Rates and inflation are decimals (0.04 = 4%).

Each leg is one least squares regression on the previous rate and inflation, the bivariate VAR(1) of
[Lutkepohl (2005)](https://doi.org/10.1007/978-3-540-27752-1). Only dates both series cover are used, and the
fitted system must settle down over time (be stationary).

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.models.knw.knw_controller import Knw

toolkit = Toolkit(["^IRX"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1990-01-01")
knw = Knw(toolkit)

knw.calibrate_pair("interest_rate", "inflation", period="quarterly")
```

Which returns (calibrated on 2026-10-05):

| leg | intercept | own_persistence | cross_coupling | volatility |
|:----|----------:|----------------:|---------------:|-----------:|
| interest_rate | -0.0009 | 0.9397 | 0.0918 | 0.0044 |
| inflation | 0.0036 | 0.8910 | -0.0246 | 0.0073 |

One percentage point more inflation adds 0.092 points to next quarter's rate, and the pair settles at a 2.60%
rate and 2.74% inflation in the long run.

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

**Returns:**

<u>tuple[KnwParams, KnwParams]:</u> (interest_rate_params, inflation_params), with the fields above plus `initial_value`, the last observation.

**Raises:**

- <u>ValueError:</u> if fewer than 5 dates overlap, or the fitted coupling is not stationary.

</details>

## names

The names of every knw leg calibrated so far (both legs of every pair), in calibration order.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
knw.names  # property -> list[str]
```

</details>

## params

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

## series

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

## dates

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

## changes

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

## step_function

The function that moves any knw leg forward by one period, given its parameters and the other leg's
current value.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Knw.step_function()
```

</details>

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

### fit_knw_pair

Fit how a nominal short rate r and inflation pi pull on each other: each is regressed by least squares on last
period's rate and last period's inflation, a bivariate VAR(1).

The cross terms carry the economics: a positive coefficient of the rate on lagged inflation is the central bank
leaning against inflation, and the inflation leg's coefficient on the lagged rate shows how tighter policy
feeds back into prices. Because both equations share the same regressors, fitting them one at a time is
already as efficient as a joint estimate.

The formula is as follows:

$$
x_{t} = c_{x} + \phi_{x} \cdot x_{t-1} + \phi_{y} \cdot y_{t-1} + u_{t}
$$

$$
\sigma_{x} = \sqrt{\operatorname{sum}(u_{t} ^{2}) / (T - 3)}
$$

Where (x, y) is (r, pi) for the rate leg and (pi, r) for the inflation leg, and T the number of transitions. The
fit is accepted only when the 2x2 coefficient matrix Phi has spectral radius below 1, the condition for the joint
system to be stationary: only then does a shock fade and the pair settle at long-run levels, rather than drift
off. Only dates both histories cover are used.

**References:**

- Koijen, R.S.J., Nijman, T.E., Werker, B.J.M. (2010). "When Can Life Cycle Investors Benefit from Time-Varying Bond Risk Premia?" The Review of Financial Studies, 23(2), 741-780. The model CP2022 extends. <https://doi.org/10.1093/rfs/hhp058> (open working paper: <https://doi.org/10.2139/ssrn.795925>)
- Commissie Parameters (2022). "Technical Appendix: Specification of the CP2022 Model." Eq. 52, the discrete-time recursion fit here at zero stochastic volatility. <https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix>
- Dai, Q., Singleton, K.J. (2000). "Specification Analysis of Affine Term Structure Models." Journal of Finance, 55(5), 1943-1978. Why a matrix (not scalar) mean reversion is standard here. <https://doi.org/10.1111/0022-1082.00278>
- Lutkepohl, H. (2005). "New Introduction to Multiple Time Series Analysis." Springer. The reduced-form VAR(1) OLS estimator and its stability condition. <https://doi.org/10.1007/978-3-540-27752-1>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_knw_pair(
    interest_rate: pl.Series,
    interest_rate_dates: pl.Series,
    inflation: pl.Series,
    inflation_dates: pl.Series,
) -> tuple[KnwParams, KnwParams]
```

**Args:**

- <u>interest_rate (pl.Series):</u> the historical nominal short rate, as decimals.
- <u>interest_rate_dates (pl.Series):</u> the dates of those observations.
- <u>inflation (pl.Series):</u> the historical inflation rate, as decimals, at the same frequency as the rate.
- <u>inflation_dates (pl.Series):</u> the dates of those observations.

**Returns:**

<u>tuple[KnwParams, KnwParams]:</u> (interest_rate_params, inflation_params).

**Raises:**

- <u>ValueError:</u> if fewer than 5 dates overlap, or Phi's spectral radius is 1 or more (the pair does not settle at this frequency).

</details>

### step_knw_process

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
