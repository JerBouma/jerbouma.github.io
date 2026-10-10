---
title: Units
seo_title: Units Documentation – Finance Scenarios
excerpt: "Every series is calibrated in the form economists and actuaries normally use for it, and every result can be shown as a rate, a level, a change or an annualized return."
description: "The units Finance Scenarios calibrates and reports in: the calibration input of each series, the native simulated values and every metric= reading."
author_profile: false
permalink: /projects/financescenarios/docs/units
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Every series is calibrated in the form economists and actuaries normally use for it: an interest rate as a rate, inflation as the change in prices over the past year, a stock as its price. Every result can then be shown in whichever form you need: the rate, the level (a price or a price index), the change over one step or over one year, the change since today, or the yearly average since today.

There are three layers, and this page is the single statement of each; [configuration](/projects/financescenarios/docs/configuration), [regimes](/projects/financescenarios/docs/regimes) and each class's docstring point here rather than restating it:

1. **Calibration inputs:** which transformation each fetched series gets before a model is fitted to it.
2. **Native simulation values:** what `result.paths[factor]` holds.
3. **Reported readings:** what every table and chart shows, chosen with `metric=`.

## 1. Calibration inputs: best practice per series

Each series is fitted in the form that suits its economics, decided by what the series is and never by the data source it happened to come from:

| Series | Fitted as | Why | Where |
|:-------|:----------|:----|:------|
| Interest rates, yields, OECD short/long rates | Level, decimal (`3.71` percentage points becomes `0.0371`) | Rates are already annual and mean-revert as levels ([Vasicek, 1977](<https://doi.org/10.1016/0304-405X(77)90016-2>)) | `interest_rates_controller` |
| Credit spreads, unemployment, dividend yield | Level, decimal | The same: a spread or a ratio that mean-reverts as a level | each factor's controller |
| Inflation (CPI) | **Year over year**: `growth=True, lag=12` monthly, `lag=4` quarterly, `lag=1` yearly | The headline figure statistics offices publish; removes seasonality; identical to the Finance Toolkit's `get_inflation_rate` | `helpers.year_over_year_growth` |
| House prices (OECD) and commercial property (FRED) | **Year over year**: `lag=4` quarterly, `lag=1` yearly; FRED publishes it only that way | One scale for both sources; removes the seasonal pattern not every country adjusts for | `helpers.year_over_year_growth` |
| Equities, commodities, FX | **Log returns** of the price at the sampling period (daily, weekly, monthly) | Prices are not stationary but their returns are, and returns compound | each factor's controller |
| Dividends (Wilkie) | Log change of the trailing dividend index | [Wilkie's (1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf) own specification | `DividendGrowth` |
| Leading indicator (OECD CLI) | Level, index points around 100 | It is built to be a stationary cycle around 100 | `LeadingIndicator` |
| Yield curve, credit curve | Nelson-Siegel level, slope, curvature from yield levels | The factors of the curve, fitted per date | `TermStructure`, `CreditTermStructure` |
| HJM forward curve | Changes in forward rates | The HJM volatility functions describe changes | `Hjm` |
| Mortality | Logit of death rates | [Cairns, Blake and Dowd's (2006)](https://doi.org/10.1111/j.1539-6975.2006.00195.x) specification | `Mortality` |

[Year over year](https://en.wikipedia.org/wiki/Year_over_year) means a value is compared with the same period a year earlier. Consecutive monthly year-over-year readings share eleven of their twelve months, so the series is smooth: a monthly fit shows slower mean reversion and smaller monthly shocks than a fit on month-on-month changes, which is the convention economic scenario generators commonly calibrate inflation on. A [log return](https://en.wikipedia.org/wiki/Rate_of_return#Logarithmic_or_continuously_compounded_return) is `ln(S_t / S_{t-1})`, the continuously compounded change in a price.

Every calibrated parameter of a rate-type factor is therefore an annualized decimal (`long_run_mean` of `0.026` is 2.6% a year), so a belief override, a regime anchor and a calibrated parameter are all on one scale:

```python
scenarios.calibrate().describe()   # long_run_mean/volatility, comparable down the column
```

`helpers.annualize_period_growth` (`ln(1 + g) / dt`) remains for any other one-period growth series: its log form is exactly what `exp(rate * dt)` inverts.

## 2. Native simulation values

Each factor is simulated natively, and `ScenarioSet.factor_kind(factor)` says which of four kinds it is:

| Kind | Categories | Native value |
|:-----|:-----------|:-------------|
| `price` | `equities`, `commodities`, `fx`, `dividend_growth`, `portfolio` and `<sleeve>_value` | A price or index level in the instrument's own currency |
| `growth` | `inflation`, `real_estate` | The yearly growth rate of a price index, an annualized decimal |
| `rate` | `interest_rates`, the yield-curve and credit-curve components, `credit`, `unemployment`, `dividend_yield`, `mortality` and anything uncategorized | A rate, spread or model factor as a level |
| `index` | `leading_indicator` | Index points around 100 |

`result.paths[factor]` (and `result[factor]`) holds these, and so does everything that needs a real price: portfolio construction, currency reporting, the Solvency II functions, `write_run()` and the scenario-file export. Every reporting method takes `levels=True` to show the native value.

A price's parameters are annualized like everything else (an equity's `regime_means`/`regime_volatilities` are annualized log-return figures). A two-factor (`method: "schwartz_smith"`) commodity simulates `<name>_chi`/`<name>_xi` in log space, and `Scenarios.simulate()` attaches the reconstructed price under the entry's own name.

A growth rate compounds into its index as `100 * exp(cumsum(rate * dt))` (`cumulative_index`). Because the rate is a year-over-year change used as the instantaneous rate, the rebuilt index follows prices with a lag of about half a year, and at 3% it compounds about 0.05 percentage points a year above simple growth: both are small next to the scenario spread.

## 3. Reported readings: `metric=`

`describe()`, `summary_statistics()`, `horizon_summary()`, `to_dataframe()`, `to_long()`, `compare_runs()` and every `.plot()` take `metric=`, read through `ScenarioSet.metric_paths(factor, metric=...)`:

| `metric` | price | growth rate | rate | index |
|:---------|:------|:------------|:-----|:------|
| `None` (default) | `annualized` | `rate` | `rate` | `level` |
| `"rate"` | not available | the simulated rate | the simulated rate | not available |
| `"level"` | the price | the compounded index, 100 at start | the rate | the index |
| `"change"` | % change over one step | % change of the index over one step | change over one step | % change over one step |
| `"yoy"` | % change over one year | % change of the index over one year | change over one year | % change over one year |
| `"cumulative"` | % change since start | % change of the index since start | change since start | % change since start |
| `"annualized"` | yearly return since start | average yearly growth since start | not available | yearly change since start |

- A change of a rate is a **difference** in its own units (`0.005` is half a percentage point), the convention for rates and spreads, not a percentage of a percentage.
- The annualized return since start is `(S_t / S_0) ** (1 / t) - 1`, the constant yearly return that turns today's value into the value at `t`. It has no value at `t0` (null in tables), reads `-1.0` for a path that reaches zero, and its spread narrows with the horizon. For a portfolio it is the figure `Portfolio.risk_metrics()` reports as `cagr_percentiles`.
- A change over `n` steps has no value for the first `n` points. `"yoy"` needs a time step that divides a year (monthly, quarterly, yearly, weekly, daily).
- On a multi-factor report a metric with no reading for some factor (`"rate"` of a price, `"annualized"` of a rate) keeps that factor's default, and `describe()`'s `metric` column names the reading of every row.
- Charts format rates, changes and returns as percentages, and prices and index levels with thousands separators.

```python
result.describe()                                          # each factor's default reading
result.describe(metric="yoy")                              # every factor's change over the past year
result.describe(levels=True)                               # the native values
result.plot("united_states_inflation", metric="level")     # inflation as a price index from 100
result.to_dataframe("us_broad", metric="change")           # equity returns per step
result.factor_kind("gold")                                 # "price"
```

## Writing beliefs and regimes against this

A belief override replaces a calibrated parameter, so it is stated in that parameter's own units: for every rate factor an annualized decimal, and for inflation a year-over-year rate:

```yaml
beliefs:
  inflation.united_states_inflation:
    long_run_mean:
      anchors:
        1.0: 0.09 # 9% a year within a year
        3.0: 0.05
```

`shocks` are in the same units (`magnitude: 0.03` is three percentage points of inflation). Regime filters rank a rate by its average over the window and a price by its return across the window. Check the level a belief is displacing with `scenarios.calibrate().describe()` before choosing anchors.

## References

- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. <https://doi.org/10.1016/0304-405X(77)90016-2>
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>
- Cairns, A.J.G., Blake, D., Dowd, K. (2006). "A Two-Factor Model for Stochastic Mortality with Parameter Uncertainty: Theory and Calibration." Journal of Risk and Insurance, 73(4), 687-718. <https://doi.org/10.1111/j.1539-6975.2006.00195.x>
