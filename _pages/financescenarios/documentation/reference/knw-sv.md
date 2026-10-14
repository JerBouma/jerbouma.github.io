---
title: "KnwSv"
seo_title: "KnwSv Reference – Finance Scenarios"
excerpt: "The KNW model with stochastic volatility."
description: "The KNW model with stochastic volatility."
author_profile: false
permalink: /projects/financescenarios/docs/reference/knw-sv
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

The KNW model with stochastic volatility.

```python
from financescenarios.models.knw_sv.knw_sv_controller import KnwSv
```

The KnwSv module simulates the interest rate and inflation as a two-way coupled pair, like `Knw`, plus a shared,
hidden "market nervousness" factor `v` that makes both swing harder in turbulent periods and calmer in quiet ones.

Real markets alternate between spells of calm and stress, and in stress rates and inflation move sharply at the
same time. The CP2022 model of De Nederlandsche Bank (DNB), the Dutch central bank, captures this with one random
variance factor scaling the volatility of everything. The result is volatility clustering and fatter tails than
`Knw`: a turbulent spell lasts a while before it fades, which matters for multi-year solvency projections.

The model is the stochastic-volatility form of [Koijen, Nijman & Werker (2010)](https://doi.org/10.1093/rfs/hhp058)
that the [CP2022 Technical Appendix (2022)](
https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix) specifies (eq. 2-5).
`v` follows a CIR process ([Cox, Ingersoll & Ross, 1985](https://doi.org/10.2307/1911242)), the mean-reverting,
never-negative variance process of [Heston (1993)](https://doi.org/10.1093/rfs/6.2.327), and both legs read its
previous level in their drift and variance:

```text
r(t)  = c_r  + gamma_r*v(t-1)  + phi_rr*r(t-1)   + phi_r_pi*pi(t-1)
        + sqrt(base_r  + sens_r*v(t-1))*z_r(t)
pi(t) = c_pi + gamma_pi*v(t-1) + phi_pi_r*r(t-1) + phi_pipi*pi(t-1)
        + sqrt(base_pi + sens_pi*v(t-1))*z_pi(t)
```

With `variance_coupling` (gamma) and `variance_sensitivity` (sens) at zero this is exactly `Knw`. `v` is simulated
with [Andersen's (2008)](https://doi.org/10.21314/jcf.2008.189) QE scheme, which never goes negative; the rate
and inflation can. DNB treats `v` as an input observed without measurement error (Technical Appendix,
section 4) and backs the rate and expected inflation out of a nominal and
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

## calibrate_triple

Calibrate one `v`, interest rate and inflation triple: fetch both histories, estimate the hidden turbulence
factor `v`, and fit how each leg depends on `v`, itself and the other leg.

`v_params` give the turbulence's normal level (`long_run_mean`), how fast a spike fades (`mean_reversion_speed`,
a half-life of ln 2 / speed years) and how jumpy it is (`volatility`). A leg's `variance_sensitivity` says how
much its per-period variance grows with `v`, and `variance_coupling` how much `v` shifts its expected next
value; the rest reads as in `Knw.calibrate_pair`.

The surprises of a constant-volatility fit, averaged over the past year and lagged one, stand in for `v`; a CIR
process ([Cox, Ingersoll & Ross, 1985](https://doi.org/10.2307/1911242)) is fit to that, and both legs are
refit with `v` as an extra input. If no leg's variance rises with `v`, a warning suggests `method: knw`: the
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

## calibrate_equity_leg

Calibrate an equity index that shares an already calibrated knw_sv pair's turbulence factor `v`.

The index earns the simulated short rate plus a constant risk premium, and its swings grow when `v` is high.
Equity and rate turbulence therefore rise and fall together, rather than being linked only through a fixed
correlation.
`risk_premium` is the extra log return per period over the short rate (0.02 a quarter is roughly 8% a year),
`base_variance` the per-period variance when `v` is zero, and `variance_sensitivity` how much variance each
unit of `v` adds. Without a link to `v`, `variance_sensitivity` is 0 and a warning says so.

This is the equity row of DNB's [CP2022 Technical Appendix](
https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix) (eq. 4-5), a
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

## names

The names of everything calibrated so far, in calibration order: both legs of every pair, each pair's
`v` (see `variance_factor_name`) and any equity leg.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
knwsv.names  # property -> list[str]
```

</details>

## params

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

## series

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

## dates

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

## changes

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

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

### compute_v_proxy

Estimate the hidden turbulence factor v from history: how large the rate and inflation surprises have been
lately.

v is not a market price. DNB's CP2022 calibration takes it as given: v_t and the yields of one nominal and one
real bond are treated as observed without measurement error (Technical Appendix, section 4). Without that series,
here it is the average squared surprise of a constant-volatility rate and inflation fit over the past year. When
both legs have recently surprised by a lot, v is high; in quiet spells it is low. The rate and inflation legs, the
equity leg and the risk-neutral market price of risk are all fitted against this one estimate, so they agree on
when markets were turbulent.

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

### fit_knw_sv_triple

Fit the rate and inflation pair together with the turbulence factor v that scales both their volatilities.

v follows a CIR process ([Cox, Ingersoll & Ross, 1985](https://doi.org/10.2307/1911242)): it is pulled back to a
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
### step_knw_sv_v

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
### step_knw_sv_leg

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

### fit_knw_sv_equity_leg

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
### step_knw_sv_equity

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
