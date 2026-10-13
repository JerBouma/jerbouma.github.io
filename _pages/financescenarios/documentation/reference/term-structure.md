---
title: "TermStructure"
seo_title: "TermStructure Reference – Finance Scenarios"
excerpt: "The yield curve as Nelson-Siegel level, slope and curvature."
description: "The yield curve as Nelson-Siegel level, slope and curvature."
author_profile: false
permalink: /projects/financescenarios/docs/reference/term-structure
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

The yield curve as Nelson-Siegel level, slope and curvature. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.factors.term_structure.term_structure_controller import TermStructure
```

```python
TermStructure(toolkit: Toolkit)
```

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

The level moves every maturity equally, the slope weighs most on short maturities and the curvature most on medium
ones; how much depends only on a fixed `decay` (lambda), set rather than fitted, as Diebold and Li do. Each factor
(`rate_level`, `rate_slope`, `rate_curvature`) is simulated as its own mean-reverting (Ornstein-Uhlenbeck) process,
pulled back toward a normal level at a fitted speed, and linked to the rest only through the correlation matrix.
The factors are fitted to history, so nothing guarantees a curve free of arbitrage between maturities (see `Hjm`
for that) and nothing stops a curve from inverting or going negative.

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

Configuration (`yield_curve` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `enabled` | `false` | Adds `rate_level`, `rate_slope` and `rate_curvature` when `true`. |
| `source` | `yahoo` | `yahoo` (four Yahoo tickers), `treasury` (12-maturity par curve, FMP key) or `government`. |
| `country` | `United States` | The country of a `government` curve. |
| `period` | `daily` | The time step: `daily` with `treasury`; `daily`, `weekly` or `monthly` with `government`. |
| `decay` | `0.7308` | The Nelson-Siegel decay (lambda), annualized; fixed, not fitted. |
| `beliefs.level`, `.slope`, `.curvature` | `null` | Override a fitted speed, long-run mean or volatility. |

**References:**

- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. <https://doi.org/10.1016/j.jeconom.2005.03.005>
- Nelson, C.R., Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." The Journal of Business, 60(4), 473-489. <https://doi.org/10.1086/296409>

## calibrate

```python
calibrate(
    period: str = 'daily',
    decay: float = 0.7308,
    source: str = 'yahoo',
    country: str = 'United States',
) -> YieldCurveParams
```

Calibrate the yield curve from history: split each date's curve into its level, slope and curvature, then fit
each of the three as its own mean-reverting process.

This learns how the shape of the yield curve has moved, so the simulated curves shift and twist the way real ones
have. The level is roughly the long-term yield, the slope the short minus the long yield and the curvature
the hump in the middle. Each gets a speed (`mean_reversion_speed`), a normal value (`long_run_mean`), a swing
size (`volatility`) and today's value (`initial_value`), in decimals. A level speed of 0.60 means a parallel
shift has halved after about 14 months (ln 2 / 0.60 years).

Each date's yields are regressed on the fixed loadings of
[Nelson and Siegel (1987)](https://doi.org/10.1086/296409), and each resulting series is fitted as in
[Diebold and Li (2006)](https://doi.org/10.1016/j.jeconom.2005.03.005).

Also known as: dynamic Nelson-Siegel, Diebold-Li yield curve calibration.

**Args:**

- <u>period (str):</u> data frequency and time step: "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>decay (float):</u> the Nelson-Siegel decay (lambda), annualized; fixed, not fitted. Defaults to 0.7308.
- <u>source (str):</u> "yahoo" (four Yahoo treasury tickers), "treasury" (the 12-maturity Treasury par curve; FMP key, daily only, falls back to "yahoo") or "government" (one country's official curve). Defaults to "yahoo".
- <u>country (str):</u> the "government" curve's country, such as "Germany", "Euro Area" or "Japan". Defaults to "United States".

**Returns:**

<u>YieldCurveParams:</u> the fitted `level`, `slope` and `curvature` processes and the `decay`.

**Raises:**

- <u>ValueError:</u> if `period`, `source` or `country` is not recognized, `decay` is not positive, "treasury" gets a non-daily period, or a "government" curve has under three maturities or no mean reversion.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.term_structure.term_structure_controller import TermStructure

toolkit = Toolkit(["^IRX", "^FVX", "^TNX", "^TYX"], api_key="FINANCIAL_MODELING_PREP_KEY")
term_structure = TermStructure(toolkit)

term_structure.calibrate(period="daily")
```

Which returns (calibrated on 2026-10-04, daily data from 2021-10-06 to 2026-10-02):

| factor | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-------|---------------------:|--------------:|-----------:|--------------:|
| level | 0.5977 | 0.0533 | 0.0089 | 0.0572 |
| slope | 5.6466 | -0.0030 | 0.0423 | -0.0181 |
| curvature | 4.9853 | -0.0169 | 0.0593 | -0.0090 |

## params

```python
termstructure.params  # property -> YieldCurveParams
```

The parameters from the last `calibrate` call.

**Raises:**

- <u>RuntimeError:</u> if `calibrate` has not been called yet.

## step_function

```python
termstructure.step_function  # property
```

The step function that moves each curve factor forward one time step, using the exact mean-reverting transition.

## changes

```python
termstructure.changes  # property -> dict[str, pl.DataFrame]
```

The dated period-over-period changes of `rate_level`, `rate_slope` and `rate_curvature` from the last
`calibrate` call, from which the correlation matrix is estimated.

**Returns:**

<u>dict[str, pl.DataFrame]:</u> one table per factor, with a `date` and a `value` column.

**Raises:**

- <u>RuntimeError:</u> if `calibrate` has not been called yet.

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

### nelson_siegel_loadings

```python
nelson_siegel_loadings(tenor: float, decay: float) -> tuple[float, float]
```

Compute the slope and curvature factor loadings for one maturity, per the
Nelson-Siegel yield curve formula. The level factor's loading is always 1
(a parallel shift affects every maturity equally), so it isn't returned here.

The formula is as follows:

$$
y(\tau) = L + S \cdot B(\tau) + C \cdot (B(\tau) - \exp(- \lambda \cdot \tau))
$$

$$
B(\tau) = (1 - \exp(- \lambda \cdot \tau)) / (\lambda \cdot \tau)
$$

Where L, S and C are the level, slope and curvature factors and lambda is `decay`; this returns the S and C
loadings, B(tau) and B(tau) - exp(-lambda * tau).

**Args:**

- <u>tenor (float):</u> maturity, in years (must be > 0).
- <u>decay (float):</u> the Nelson-Siegel decay parameter (lambda), annualized.

**Returns:**

<u>tuple[float, float]:</u> (slope_loading, curvature_loading) for this maturity.

**Raises:**

- <u>ValueError:</u> if tenor is not strictly positive.

**References:**

- Nelson, C.R., Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." The Journal of Business, 60(4), 473-489. <https://doi.org/10.1086/296409> The static functional form and loadings this function implements.
- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. <https://doi.org/10.1016/j.jeconom.2005.03.005>

### nelson_siegel_forward

```python
nelson_siegel_forward(
    level: float | np.ndarray,
    slope: float | np.ndarray,
    curvature: float | np.ndarray,
    tenor: float | np.ndarray,
    decay: float,
) -> float | np.ndarray
```

Nelson & Siegel's (1987) own instantaneous forward-rate parametrization:
their yield curve is itself derived as the average of this forward curve, not
the other way around. Used by `hjm_model` as the deterministic curve a
2-factor Gaussian HJM anchors to, since it's smooth and defensible to
extrapolate at any maturity (including beyond the 4 observed treasury
tenors), unlike a piecewise bootstrap. Unlike `nelson_siegel_yield`, `tenor`
may be an array (HJM evaluates this at every point of a whole time grid at
once) and `tenor == 0` is valid (the short rate).

The formula is as follows:

$$
f(\tau) = L + S \cdot \exp(- \lambda \cdot \tau) + C \cdot \lambda \cdot \tau \cdot \exp(- \lambda \cdot \tau)
$$

**Args:**

- <u>level (float &#124; np.ndarray):</u> the level factor value(s).
- <u>slope (float &#124; np.ndarray):</u> the slope factor value(s).
- <u>curvature (float &#124; np.ndarray):</u> the curvature factor value(s).
- <u>tenor (float &#124; np.ndarray):</u> maturity/maturities, in years (must be >= 0).
- <u>decay (float):</u> the Nelson-Siegel decay parameter (lambda), annualized.

**Returns:**

<u>float &#124; np.ndarray:</u> the instantaneous forward rate at `tenor`, broadcast against whichever of the inputs is array-valued.

**Raises:**

- <u>ValueError:</u> if any `tenor` is negative.

**References:**

- Nelson, C.R., Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." The Journal of Business, 60(4), 473-489. <https://doi.org/10.1086/296409>

### nelson_siegel_forward_integral

```python
nelson_siegel_forward_integral(
    level: float | np.ndarray,
    slope: float | np.ndarray,
    curvature: float | np.ndarray,
    tenor: float | np.ndarray,
    decay: float,
) -> float | np.ndarray
```

Closed-form `integral_0^tenor nelson_siegel_forward(..., u, decay) du`:
equivalently `tenor * nelson_siegel_yield(..., tenor, decay)` for `tenor > 0`,
provided here directly (and valid at `tenor == 0`, where it's 0) since
`hjm_model.hjm_zero_yield` needs the *difference* of this integral at two
points, not a yield itself.

The formula is as follows:

$$
F(\tau) = L \cdot \tau + S \cdot D(\tau) + C \cdot (D(\tau) - \tau \cdot \exp(- \lambda \cdot \tau))
$$

$$
D(\tau) = (1 - \exp(- \lambda \cdot \tau)) / \lambda
$$

**Args:**

- <u>level (float &#124; np.ndarray):</u> the level factor value(s).
- <u>slope (float &#124; np.ndarray):</u> the slope factor value(s).
- <u>curvature (float &#124; np.ndarray):</u> the curvature factor value(s).
- <u>tenor (float &#124; np.ndarray):</u> maturity/maturities, in years (must be >= 0).
- <u>decay (float):</u> the Nelson-Siegel decay parameter (lambda), annualized.

**Returns:**

<u>float &#124; np.ndarray:</u> the accumulated forward rate from 0 to `tenor`.

**Raises:**

- <u>ValueError:</u> if any `tenor` is negative.

**References:**

- Nelson, C.R., Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." The Journal of Business, 60(4), 473-489. <https://doi.org/10.1086/296409>

### fit_nelson_siegel_factors

```python
fit_nelson_siegel_factors(
    yields_by_tenor: dict[float, pl.Series],
    decay: float,
    dates: pl.Series,
) -> pl.DataFrame
```

Cross-sectionally fit Nelson-Siegel level/slope/curvature factors at every date,
via OLS regression of that date's yields (across tenors) on the fixed
Nelson-Siegel loadings for those tenors. Since the loadings depend only on the
(fixed) tenor set and decay, not on the date, this is one linear system solved
for every date at once.

The formula is as follows:

$$
y_{t}(\tau_{j}) = L_{t} + S_{t} \cdot \operatorname{slope\_loading}(\tau_{j}) + C_{t} \cdot \operatorname{curvature\_loading}(\tau_{j}) + e_{t},\;\; \text{j}
$$

Solved by least squares across the tenors tau_j for each date t, as in Diebold and Li (2006).

**Args:**

- <u>yields_by_tenor (dict[float, pl.Series]):</u> maturity (years) -> historical yield series at that maturity, all the same length and time index.
- <u>decay (float):</u> the Nelson-Siegel decay parameter (lambda), annualized.
- <u>dates (pl.Series):</u> one date per observation, same length and order as every series in `yields_by_tenor`; carried through (and dropped jointly with a missing-tenor date, same as every yield column) so the returned level/slope/curvature series can be date-aligned against other factors for cross-factor correlation, instead of only being positionally ordered.

**Returns:**

<u>pl.DataFrame:</u> "date", "level", "slope" and "curvature" columns, one row per date with every tenor observed (dates with any tenor missing are dropped first; see below), in the same date order as the input series.

**Raises:**

- <u>ValueError:</u> if fewer than 3 tenors are supplied, the tenor series aren't all the same length, or the fit produces a non-finite factor despite the null-dropping below (should be unreachable, kept as a hard failure rather than letting a silent NaN reach `fit_ou_process`).

**References:**

- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. <https://doi.org/10.1016/j.jeconom.2005.03.005>

### step_curve_factor

```python
step_curve_factor(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: OUParams,
) -> np.ndarray
```

Advance one Nelson-Siegel factor (level, slope or curvature) by one time step
via its *exact* discrete-time transition (see
`calibration_model.step_ou_process`), the closed-form solution of
dx = a(theta - x)dt + sigma*dW rather than an Euler-Maruyama approximation of
it; the same Ornstein-Uhlenbeck dynamics used for the short rate and
inflation, applied here to a cross-sectional yield curve factor instead of a
single-tenor rate.

The formula is as follows:

$$
\beta(t + \text{dt}) = \theta + (\beta(t) - \theta) \cdot \exp(- a \cdot \text{dt}) + \sigma \cdot \sqrt{(1 - \exp(- 2 \cdot a \cdot \text{dt})) / (2 \cdot a)} \cdot z
$$

This is the AR(1) per factor that Diebold and Li (2006) forecast with, with coefficient exp(-a * dt).

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> the factor's value at the current time step.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw for this step.
- <u>time_step (float):</u> the time increment, in years.
- <u>params (OUParams):</u> calibrated mean-reversion speed, long-run mean, and volatility.

**Returns:**

<u>np.ndarray:</u> the factor's value at the next time step.

**References:**

- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. <https://doi.org/10.1016/j.jeconom.2005.03.005>
- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. <https://doi.org/10.1016/0304-405x(77>)90016-2 Source of the exact transition used here.
