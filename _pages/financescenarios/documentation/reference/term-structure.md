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

The Term Structure module simulates the whole government yield curve, the yield at
every maturity from three months to thirty years, rather than a single interest rate.
It describes each day's curve with three numbers (its level, slope and curvature) and
lets those three numbers move through time, so the simulated curve can shift, steepen,
flatten and bend the way the real one does.

In plain terms: the interest rate factor (`InterestRates`) gives you one point on the
curve, such as the 13-week Treasury bill. Switch on `yield_curve` and every simulated
future also carries a full curve, so you can read off a simulated 2-year, 10-year or
30-year yield, see how often the curve inverts (short rates above long rates) and
value bonds of any maturity. It is opt-in in the configuration model
(`yield_curve.enabled` defaults to `false`); the shipped `factor-sets/default.yaml` and `broad.yaml`
switches it on.

The model is the dynamic Nelson-Siegel model of
[Diebold and Li (2006)](https://doi.org/10.1016/j.jeconom.2005.03.005), built on the
curve shape of [Nelson and Siegel (1987)](https://doi.org/10.1086/296409). At any date
the yield at maturity `tenor` is approximated as

`yield(tenor) = level + slope * slope_loading(tenor) + curvature * curvature_loading(tenor)`

where the three components are:

- **Level**: a parallel shift that moves every maturity equally (its loading is 1).
- **Slope**: a steepening or flattening, loading more on short maturities than on
  long ones (`slope_loading = (1 - exp(-decay*tenor)) / (decay*tenor)`).
- **Curvature**: a hump or trough, loading most on medium maturities
  (`curvature_loading = slope_loading - exp(-decay*tenor)`).

The loadings are fixed functions of maturity and of one decay parameter (`decay`,
lambda, annualized), not calibrated themselves (`nelson_siegel_loadings`); Diebold and
Li fix the decay rather than estimate it, and so does this module (default `0.7308`).
Reading these three as level, slope and curvature also matches the principal
components [Litterman and Scheinkman (1991)](https://doi.org/10.3905/jfi.1991.692347)
found in bond returns, though neither result derives the other.

Instead of one stochastic process (the short rate) the module simulates three,
`rate_level`, `rate_slope` and `rate_curvature`, each its own mean-reverting
Ornstein-Uhlenbeck process fitted with the same `fit_ou_process` machinery as the
interest rate and inflation factors and stepped with the exact discrete-time
transition of [Vasicek (1977)](https://doi.org/10.1016/0304-405x(77)90016-2)
(`step_curve_factor`), just applied to a curve factor instead of a single-maturity
rate. The three factors have no cascade dependency on inflation or any other factor in
the simulation's dependency graph: only the correlation matrix (`Dependence`, applied
through a Cholesky decomposition) links them to each other and to the rest, which is
how Diebold and Li specify their own three-factor system.

To get the simulated yield at any maturity after a run, apply `nelson_siegel_yield`
directly to the simulated path arrays; it broadcasts over `(n_simulations, n_steps + 1)`
arrays the same way it does over single numbers:

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

`curve_inversion_frequency` and `negative_spread_frequency` turn the same paths into
the share of simulated cells where the curve is inverted or a yield is negative.

Three data sources are available through `source`, all obtained through the Finance
Toolkit:

- `yahoo` (default): the four standard Yahoo Finance treasury-yield tickers
  (`YIELD_CURVE_TENORS`: `^IRX` 13-week, `^FVX` 5-year, `^TNX` 10-year and `^TYX`
  30-year) from one `Toolkit.get_historical_data()` call. No API key is needed, and
  `build_toolkit()` adds the four tickers to the Toolkit it builds when the factor is
  enabled.
- `treasury`: the official daily 12-tenor Treasury par curve (1 Month through 30 Year,
  `TREASURY_RATES_TENORS`) via `fixedincome.get_treasury_rates()`: the same
  three-factor fit against three times the maturities, with real short-end coverage
  (1M, 2M, 3M, 6M, 1Y, 2Y, 3Y) the Yahoo set barely has. It requires a Financial
  Modeling Prep API key and `period: daily`, and falls back to the Yahoo tickers with
  a logged warning on any fetch failure.
- `government`: the official government bond yield curve of one `country` via
  `fixedincome.get_government_bond_yield_curve()` (no API key): the US Treasury par
  curve, the European Central Bank's euro area curve, the
  Bundesbank's German curve, the Bank of England's gilt yields, Japan's Ministry of
  Finance curve, and the Bank of Canada, Riksbank and Norges Bank curves
  (`GOVERNMENT_CURVE_COUNTRIES`), daily, weekly or monthly. This is what makes a
  non-US yield curve possible. It never falls back to the US curve: simulating a German
  curve from US data would be worse than failing.

Since the Yahoo source uses only four maturities (not the dozens a production
term-structure model would use), its cross-sectional fit is a coarse approximation of
the true curve shape: adequate for the broad level, slope and curvature dynamics, not
a precision pricing tool. Two country caveats for `government`: the Bank of England
publishes only the 5, 10 and 20 year maturities, so the UK fit is exactly determined
by three points and its short end is an extrapolation; and Japanese yields have risen
steadily from near zero since 2000, so over that window the level shows no mean
reversion at a monthly step and the fit stops with a clear error rather than
simulating a process that does not describe the data.

What it does not do: the three factors are statistical, fitted to history under the
real-world measure, with no guarantee that the simulated curves are free of arbitrage
between maturities (for an arbitrage-free curve, see `Hjm`); and nothing stops the
simulated curve from inverting or going negative, which is why the two frequency
diagnostics above exist.

Configuration (`yield_curve` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `enabled` | `false` | Adds `rate_level`/`rate_slope`/`rate_curvature` and the four tenor tickers when `true`. |
| `source` | `yahoo` | `yahoo` (four Yahoo tickers), `treasury` (12-tenor par curve, FMP key) or `government`. |
| `country` | `United States` | The country of a `government` curve; rejected with the other two sources. |
| `period` | `daily` | The time step. `daily` with `treasury`; `daily`, `weekly` or `monthly` with `government`. |
| `decay` | `0.7308` | The Nelson-Siegel decay (lambda), annualized; fixed, not calibrated (Diebold-Li). |
| `beliefs.level` | all `null` | An `OUBeliefs` block for the level factor (see below). |
| `beliefs.slope` | all `null` | An `OUBeliefs` block for the slope factor. |
| `beliefs.curvature` | all `null` | An `OUBeliefs` block for the curvature factor. |

Each belief block overrides a calibrated `mean_reversion_speed`, `long_run_mean` or
`volatility` the same way the interest rate factor's beliefs do (and accepts the same
`shocks` list); a `null` keeps the fitted value. `Scenarios.simulate()` calibrates and
simulates the yield curve automatically whenever `yield_curve.enabled` is `true`;
nothing else about the call changes.

**References:**

- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. <https://doi.org/10.1016/j.jeconom.2005.03.005>
- Nelson, C.R., Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." The Journal of Business, 60(4), 473-489. <https://doi.org/10.1086/296409>
- Litterman, R., Scheinkman, J. (1991). "Common Factors Affecting Bond Returns." The Journal of Fixed Income, 1(1), 54-61. <https://doi.org/10.3905/jfi.1991.692347>
- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. <https://doi.org/10.1016/0304-405x(77>)90016-2

## calibrate

```python
calibrate(
    period: str = 'daily',
    decay: float = 0.7308,
    source: str = 'yahoo',
    country: str = 'United States',
) -> YieldCurveParams
```

Calibrate the Nelson-Siegel yield curve from history: fetch the treasury yields at
every available maturity, decompose each date's curve into its level, slope and
curvature, and fit each of those three series as its own mean-reverting process
(how fast it returns to normal, `mean_reversion_speed`; what that normal value is,
`long_run_mean`; how much it swings, `volatility`; and where it starts today,
`initial_value`).

In plain terms: this learns from the past how the shape of the yield curve moves,
so the simulated curves shift and twist the way real ones have. The level is
roughly the long-term yield, the slope roughly the short yield minus the long yield
(negative for a normal, upward-sloping curve) and the curvature the size of the
hump in the middle. A level speed of 0.60 a year, for example, means a parallel
shift of the curve has faded by half after about 14 months (ln 2 / 0.60 years).

At every date the yields are regressed on the fixed Nelson-Siegel loadings for the
available maturities (an ordinary least squares fit, solved for every date at once
since the loadings never change, see `fit_nelson_siegel_factors`), which produces a
level, slope and curvature time series. Each series is then calibrated
independently with `fit_ou_process`, exactly as the interest rate factor calibrates
the short rate. All values are decimal fractions (`0.05` is 5%), and the time step
follows `period` (1/252 of a year for daily data).

Also known as: dynamic Nelson-Siegel, Diebold-Li yield curve calibration.

**Args:**

- <u>period (str):</u> sampling frequency of the underlying data ("daily", "weekly", "monthly", "quarterly", "yearly"), determines the time_step used to fit each factor.
- <u>decay (float):</u> the Nelson-Siegel decay parameter (lambda), annualized; fixed rather than calibrated, per Diebold & Li (2006).
- <u>source (str):</u> "yahoo" (default) fits the four standard Yahoo treasury tickers (term_structure_model.YIELD_CURVE_TENORS); "treasury" fits the official daily 12-tenor Treasury par curve via Finance Toolkit's `fixedincome.get_treasury_rates()` (FMP key required; daily only, so requires period="daily"), a much denser cross-section for the same three-factor fit. Falls back to "yahoo" with a logged warning when the treasury fetch fails or comes back empty. A tenor column with more than _TREASURY_TENOR_MAX_NULL_FRACTION nulls is dropped whole rather than truncating every other tenor's history. "government" fits the official government curve of `country` via Finance Toolkit's `fixedincome.get_government_bond_yield_curve()` (no key; daily, weekly or monthly), with no fallback.
- <u>country (str):</u> the country of a "government" curve, one of term_structure_model.GOVERNMENT_CURVE_COUNTRIES. Ignored by the other sources.

**Returns:**

<u>YieldCurveParams:</u> the calibrated level, slope and curvature processes.

**Raises:**

- <u>ValueError:</u> if period or source is not recognized, source="treasury" is combined with a non-daily period, or source="government" fails: an older Finance Toolkit, a country without a curve, nothing returned, fewer than three usable maturities, or no mean reversion in the fitted factors.

**Notes:**

- The four Yahoo tickers are quoted in percentage points (4.1 meaning 4.10%) and
  divided by 100; the Treasury par curve already arrives as decimals.
- Both sources quote bond-equivalent (semiannual) yields, which are used as they are,
  with no conversion to continuous compounding.
- A date on which any maturity is missing is dropped from the fit, with a logged
  warning saying how many dates were lost. That is why a Treasury maturity first
  published partway through the window (`2 Month` began in 2018) is dropped whole
  once more than 5% of its values are missing, rather than truncating every other
  maturity's history.
- With exactly three maturities the fit is exactly determined (a zero residual by
  construction) and a warning says so; it then gives no signal of a bad print.
- `source="treasury"` changes only this factor's cross-section; the other models
  that fit their own Nelson-Siegel anchor curve (`Hjm`, the interest rate factor's
  `risk_neutral_forward_curve` mode, `knw_sv_q`) still use the four Yahoo tickers.
- `source="government"` reads maturity labels such as "1.5M" or "10Y" as years
  (`parse_tenor_label`) and drops maturities missing on more than 5% of the dates.
- `calibrate` also stores the dated period-over-period changes of each factor
  (`changes`), which `Dependence` uses to estimate the correlations.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.term_structure.term_structure_controller import TermStructure

toolkit = Toolkit(["^IRX", "^FVX", "^TNX", "^TYX"], api_key="FINANCIAL_MODELING_PREP_KEY")
term_structure = TermStructure(toolkit)

term_structure.calibrate(period="daily")
term_structure.calibrate(period="daily", source="treasury")
```

Which returns (calibrated on 2026-10-04, daily data from 2021-10-06 to 2026-10-02):

| source | factor | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-------|:-------|---------------------:|--------------:|-----------:|--------------:|
| yahoo | level | 0.5977 | 0.0533 | 0.0089 | 0.0572 |
| yahoo | slope | 5.6466 | -0.0030 | 0.0423 | -0.0181 |
| yahoo | curvature | 4.9853 | -0.0169 | 0.0593 | -0.0090 |
| treasury | level | 0.6540 | 0.0517 | 0.0095 | 0.0566 |
| treasury | slope | 0.4768 | 0.0012 | 0.0109 | -0.0161 |
| treasury | curvature | 1.7026 | -0.0084 | 0.0360 | -0.0032 |

Both sources agree on the level: about 5.7% today, pulled toward about 5.2-5.3% with
a half-life of just over a year. Feeding today's Yahoo factors into
`nelson_siegel_yield` gives a 3-month yield of 3.99%, 2-year 4.50%, 10-year 5.35%
and 30-year 5.59%, an upward-sloping curve. The slope and curvature differ much
more between the sources: with only four maturities their daily estimates are
noisy and snap back within weeks (a slope half-life of ln 2 / 5.65, about 1.5
months), while the denser Treasury curve gives a smoother slope with a half-life of
about 1.5 years.

With `source="government"`, the same model fits other
countries' official curves, here monthly from January 2000:

```python
toolkit = Toolkit(["SPY"], start_date="2000-01-01")

for country in ["United States", "Germany", "Euro Area", "United Kingdom"]:
    TermStructure(toolkit).calibrate(period="monthly", source="government", country=country)
```

Which returns (calibrated on 2026-10-05, the level factor's long-run mean and speed and
all three factors today):

| country | level long_run_mean | level speed | level today | slope today | curvature today |
|:--------|--------------------:|------------:|------------:|------------:|----------------:|
| United States | 0.0392 | 0.3046 | 0.0568 | -0.0154 | -0.0047 |
| Germany | 0.0272 | 0.1142 | 0.0404 | -0.0054 | -0.0290 |
| Euro Area | 0.0327 | 0.1610 | 0.0460 | -0.0192 | -0.0132 |
| United Kingdom | 0.0467 | 0.0986 | 0.0614 | 0.0528 | -0.1095 |

Over 26 years every curve's level sits above its long-run average today and is pulled
back toward it slowly (a German half-life of about six years, ln 2 / 0.1142). The
UK's extreme slope and curvature come from fitting only its 5, 10 and 20 year yields;
Japan, whose yields rose steadily from near zero, stops with a no-mean-reversion
error over this window.

**References:**

- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. <https://doi.org/10.1016/j.jeconom.2005.03.005>
- Nelson, C.R., Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." The Journal of Business, 60(4), 473-489. <https://doi.org/10.1086/296409>

## params

```python
termstructure.params  # property -> YieldCurveParams
```

The last-calibrated yield curve parameters.

**Raises:**

- <u>RuntimeError:</u> if calibrate() hasn't been called yet.

## step_function

```python
termstructure.step_function  # property
```

The exact-transition OU step function (see step_curve_factor's own
docstring, not Euler-Maruyama) shared by all three curve factors.

## changes

```python
termstructure.changes  # property -> dict[str, pl.DataFrame]
```

Dated period-over-period changes in each curve factor ("rate_level",
"rate_slope", "rate_curvature"), from the same data calibrate() already
fetched; reused for cross-factor correlation estimation (Dependence)
instead of triggering a second Finance Toolkit fetch.

**Returns:**

<u>dict[str, pl.DataFrame]:</u> one entry per curve factor, each two columns, `date` (pl.Date) and `value` (f64); see helpers.dated_changes().

**Raises:**

- <u>RuntimeError:</u> if calibrate() hasn't been called yet.
