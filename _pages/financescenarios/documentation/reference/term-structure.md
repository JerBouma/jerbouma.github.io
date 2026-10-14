---
title: "TermStructure"
seo_title: "TermStructure Reference | Finance Scenarios"
seo_title_suffix: false
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

The yield curve as Nelson-Siegel level, slope and curvature.

```python
from financescenarios.factors.term_structure.term_structure_controller import TermStructure
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

## calibrate

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

Which returns (calibrated on 2026-10-04, daily data from 2021-10-06 to 2026-10-02):

| factor | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-------|---------------------:|--------------:|-----------:|--------------:|
| level | 0.5977 | 0.0533 | 0.0089 | 0.0572 |
| slope | 5.6466 | -0.0030 | 0.0423 | -0.0181 |
| curvature | 4.9853 | -0.0169 | 0.0593 | -0.0090 |

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
- <u>decay (float):</u> the Nelson-Siegel decay (lambda), annualized; fixed, not fitted. Defaults to 0.7308, from Diebold and Li (2006, section 3 of NBER w10048): "The λ value that maximizes the loading on the medium- term factor at exactly 30 months is λ=0.0609"; 0.0609 a month × 12 = 0.7308 a year.
- <u>source (str):</u> "yahoo" (four Yahoo treasury tickers), "treasury" (the 12-maturity Treasury par curve; FMP key, daily only, falls back to "yahoo") or "government" (one country's official curve). Defaults to "yahoo".
- <u>country (str):</u> the "government" curve's country, such as "Germany", "Euro Area" or "Japan". Defaults to "United States".

**Returns:**

<u>YieldCurveParams:</u> the fitted `level`, `slope` and `curvature` processes and the `decay`.

**Raises:**

- <u>ValueError:</u> if `period`, `source` or `country` is not recognized, `decay` is not positive, "treasury" gets a non-daily period, or a "government" curve has under three maturities or no mean reversion.

</details>

## params

The calibrated yield curve: the level, slope and curvature processes and the decay.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
termstructure.params  # property -> YieldCurveParams
```

**Raises:**

- <u>RuntimeError:</u> if the curve has not been calibrated yet.

</details>

## step_function

The one-step move of each curve factor, `step_curve_factor` below.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
termstructure.step_function  # property
```

</details>

## changes

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

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

### nelson_siegel_loadings

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

### nelson_siegel_yield

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

### nelson_siegel_forward

The instantaneous forward rate at a maturity from the curve's level, slope and curvature: the rate the curve
implies today for borrowing over a very short period starting `tenor` years from now.

Nelson and Siegel (1987) define their curve through this forward rate, "r(m) = β0 + β1 exp(−m/τ) + β2[(m/τ) *
exp(−m/τ)]" (eq. 2.1 of the working-paper version, NBER w1594, with 1/τ the decay); the yield at a maturity is its
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

### nelson_siegel_forward_integral

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

### curve_inversion_frequency

The share of all simulated scenario-periods in which the curve is inverted: the short-maturity yield above the
long-maturity one.

Inversions happen in practice (ahead of most US recessions) and the curve model allows them, so this checks that
they appear about as often as history suggests. The NAIC's draft GOES acceptance criteria (October 2023, T3b) ask
only that "The frequency of different yield curve shapes in early durations should be reasonable considering the
shape of the starting yield curve", with no number
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

### negative_spread_frequency

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

### fit_nelson_siegel_factors

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

Solved by least squares across the tenors tau_j for each date t, as in Diebold and Li (2006, section 3):
"Applying ordinary least squares to the yield data for each month gives us a time series of estimates".

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

### step_curve_factor

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

This is the AR(1) per factor that Diebold and Li (2006, section 3) forecast with, with coefficient exp(-a * dt):
"We model and forecast the Nelson-Siegel factors as univariate AR(1) processes".

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
