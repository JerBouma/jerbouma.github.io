---
title: "Solvency"
seo_title: "Solvency Reference – Finance Scenarios"
excerpt: "Solvency II on a real-world and a risk-neutral run: the martingale test, best estimate, SCR and EIOPA curves."
description: "Solvency II on a real-world and a risk-neutral run: the martingale test, best estimate, SCR and EIOPA curves."
author_profile: false
permalink: /projects/financescenarios/docs/reference/solvency
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Solvency II on a real-world and a risk-neutral run: the martingale test, best estimate, SCR and EIOPA curves. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios import Solvency, best_estimate, solvency_capital_requirement, interest_rate_scr, equity_scr, martingale_test, market_consistency_check, eiopa_risk_free_curve, eiopa_symmetric_adjustment, zero_coupon_curve, curve_discount_factors, write_scenario_files
```

## Solvency

```python
Solvency(
    real_world: ScenarioSet,
    risk_neutral: ScenarioSet,
    short_rate: str | None = None,
    asset: str | None = None,
)
```

Run an insurer's two Solvency II jobs on one pair of runs and read the answers in one table.

An insurer uses scenarios for two different jobs, and Solvency II names both. The first is valuing what it owes: the
best estimate (Article 77) is the average present value of the future payments under scenarios priced like today's
market, a risk-neutral run. The second is the capital requirement: the Solvency Capital Requirement or SCR (Article
101) is the loss of own funds (assets minus what is owed) over one year that is exceeded only once in 200 years,
measured on a real-world run. Before valuing anything, `Solvency` also checks that the risk-neutral run really
reproduces today's prices. Together they answer how much is owed, valued at today's market prices, and whether
there is enough capital to keep paying it after a very bad year.

| Method | What it gives |
|:-------|:--------------|
| `report(cashflows, assets)` | Market consistency, best estimate, own funds, SCR and solvency ratio in one table. |
| `plot(cashflows, assets)` | Where own funds could be after one year, with the 1-in-200 outcome marked. |
| `write_files(directory)` | Both runs as scenario files for a liability or ALM system. |

**As an example:**

```python
from financescenarios import Portfolio, Scenarios, Solvency

scenarios = Scenarios.from_profiles(settings="default", factor_set="default")
result = scenarios.simulate(n_simulations=2000)

# The same factors priced the way markets price them today, for valuing what is owed
risk_neutral = scenarios.simulate(n_simulations=2000, measure="risk_neutral")
solvency = Solvency(real_world=result, risk_neutral=risk_neutral)

# Pay out 10,000 a year for five years, backed by 60,000 invested in the 60/40
assets = Portfolio.from_preset(result, preset="balanced_60_40").compute(initial_value=60_000, rebalance_every=12)
solvency.report(cashflows=[10_000] * 5, assets=assets)
```

Which returns:

| item                | value                     | meaning                                                    |
|:--------------------|:--------------------------|:-----------------------------------------------------------|
| market consistent   | passed (largest gap 1.0%) | discounted back, us_broad stays within 2% of today's price |
| best estimate       | 43,444                    | what the payments are worth today                          |
| own funds           | 15,635                    | assets minus what is owed, today                           |
| SCR (1 in 200 year) | 12,453                    | the capital that survives a 1-in-200 bad year              |
| solvency ratio      | 1.26                      | own funds / SCR; above 1 means enough capital              |

**References:**

- European Parliament and Council (2009). "Directive 2009/138/EC (Solvency II)", Articles 77 and 101. <https://eur-lex.europa.eu/eli/dir/2009/138/oj>

## report

```python
report(
    cashflows: Sequence[float] | np.ndarray,
    assets: ScenarioSet | str | np.ndarray,
    horizon_years: float = 1.0,
    price_tolerance: float = 0.02,
) -> pl.DataFrame
```

Every Solvency II read in one table: whether the run is market consistent, what the payments are worth, own
funds, the SCR and the solvency ratio.

The best estimate is valued on the risk-neutral run. Own funds and the SCR come from the real-world run, where
own funds are the assets minus what is still owed. A solvency ratio above 1 means there is enough capital to
survive a 1-in-200 bad year. The market-consistency row appears only when the risk-neutral run has an equity to
price; it judges the size of the largest gap from today's price rather than a pass or fail per date, which a few
dates fail by chance once there are thousands of scenarios.

**Args:**

- <u>cashflows (Sequence[float] &#124; np.ndarray):</u> what is paid: one amount per year (`[10_000] * 5`, paid at each year end), or one amount per date of the run, t0 included.
- <u>assets (ScenarioSet &#124; str &#124; np.ndarray):</u> what backs it on the real-world run: a `Portfolio.compute()` result, a factor name, or a value array shaped (n_simulations, n_steps + 1).
- <u>horizon_years (float):</u> the capital requirement's horizon; 1.0 (one year, as Solvency II asks) by default.
- <u>price_tolerance (float):</u> how far the discounted price may drift from today's, as a fraction, before the run counts as not market consistent; 0.02 (2%) by default.

**Returns:**

<u>pl.DataFrame:</u> 'item', 'value' (formatted to read) and 'meaning', one row per read.

**Raises:**

- <u>ValueError:</u> if `assets` does not have the real-world run's shape, or the yearly payments run past its end.
- <u>As an example, with `solvency` and `assets` from the class example:</u> 
- ```python
- solvency.report(cashflows=[10_000] * 5, assets=assets)
- ```
- <u>Which returns a solvency ratio of 1.26:</u> own funds of 15,635 against an SCR of 12,453.

## plot

```python
plot(
    cashflows: Sequence[float] | np.ndarray,
    assets: ScenarioSet | str | np.ndarray,
    horizon_years: float = 1.0,
    confidence: float = 0.995,
    ax: Axes | None = None,
) -> Figure
```

Chart where own funds could be after `horizon_years` across every real-world scenario, discounted to today.

Today's own funds and the 1-in-200 outcome are marked: the gap between them is the SCR that `report()` gives.

**Args:**

- <u>cashflows (Sequence[float] &#124; np.ndarray):</u> what is paid, as for `report()`.
- <u>assets (ScenarioSet &#124; str &#124; np.ndarray):</u> what backs it, as for `report()`.
- <u>horizon_years (float):</u> the capital requirement's horizon; 1.0 (one year, as Solvency II asks) by default.
- <u>confidence (float):</u> the level the SCR is read at; 0.995 (99.5%, as Solvency II asks) by default.
- <u>ax (Axes &#124; None):</u> an existing matplotlib Axes to draw into; a new figure by default.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the chart.

**As an example:**

```python
solvency.plot(cashflows=[10_000] * 5, assets=assets)
```

## write_files

```python
write_files(
    directory: str | Path,
    step_stride: int = 1,
    file_format: Literal['csv', 'xlsx'] = 'csv',
)
```

Write both runs as the scenario files liability and ALM systems load, under `real_world/` and `risk_neutral/`.

Each run gets one file per variable, one row per trial and one column per date; see `write_scenario_files`.

**Args:**

- <u>directory (str &#124; Path):</u> the folder to write into.
- <u>step_stride (int):</u> keep every n-th date, e.g. 12 for yearly columns from a monthly run; 1 by default.
- <u>file_format (str):</u> "csv" (default) or "xlsx".

**Returns:**

<u>dict[str, list[Path]]:</u> the files written, per run.

## best_estimate

```python
best_estimate(
    scenario_set: ScenarioSet,
    cashflows: np.ndarray | Sequence[float],
    short_rate: str | None,
    percentiles: Sequence[float] = _DEFAULT_PERCENTILES,
    discount_curve: pl.DataFrame | None = None,
) -> BestEstimateResult
```

Compute the best estimate of a stream of future payments: their average present value across scenarios, the value
Solvency II asks an insurer to hold for what it owes (Article 77).

Per scenario the present value is the sum of D(t) * cashflow(t), with D the discount factor along that scenario's
own interest rates; on a risk-neutral run the average is the market-consistent value. The standard error says how
precise that average is. Payments can be fixed or differ per scenario, such as inflation-linked benefits. To
discount with EIOPA's risk-free curve instead, as Solvency II prescribes (Article 77(2)), pass `discount_curve`.

**Args:**

- <u>scenario_set (ScenarioSet):</u> a simulated run; risk-neutral for a market-consistent best estimate.
- <u>cashflows (np.ndarray &#124; Sequence[float]):</u> the amount paid at each date, t0 included, positive for a payment out: one schedule, or one per scenario shaped (n_simulations, n_steps + 1).
- <u>short_rate (str &#124; None):</u> the rate factor to discount with; None when `discount_curve` is given.
- <u>percentiles (Sequence[float]):</u> the percentiles to report, each between 0 and 1; 0.005, 0.05, 0.25, 0.5, 0.75, 0.95 and 0.995 by default.
- <u>discount_curve (pl.DataFrame &#124; None):</u> a published curve ("maturity", "rate") to discount with instead, e.g. from `eiopa_risk_free_curve`; None by default.

**Returns:**

<u>BestEstimateResult:</u> `best_estimate`, `standard_error`, `std` (the spread across scenarios) and `percentiles`.

**Raises:**

- <u>ValueError:</u> if `cashflows` does not match the run's dates or holds a non-finite amount.

**As an example:**

```python
import numpy as np

from financescenarios import best_estimate

# `result`: the risk-neutral run set up in full in the Solvency II guide,
# https://www.jeroenbouma.com/projects/financescenarios/docs/solvency#martingale-test-example
annuity = np.zeros(len(result.time_grid))
annuity[12::12] = 10_000.0  # 10,000 a year at each year end
level = best_estimate(result, annuity, short_rate="united_states_short_rate")

index = result.cumulative_index("united_states_inflation", initial_index=1.0).drop("scenario").to_numpy()
indexed = best_estimate(result, annuity * index, short_rate="united_states_short_rate")
```

Which returns (calibrated on 2026-10-04):

| annuity | best_estimate | standard_error | p0.5 | p99.5 |
|:--------|--------------:|---------------:|-----:|------:|
| level | 80,811.82 | 0.00 | 80,811.82 | 80,811.82 |
| inflation-indexed | 93,142.15 | 4.05 | 83,990.68 | 103,236.21 |

**References:**

- European Parliament and Council (2009). "Directive 2009/138/EC (Solvency II)", Articles 76-77. <https://eur-lex.europa.eu/eli/dir/2009/138/oj>
- EIOPA (2015, updated 2023). "Guidelines on valuation of technical provisions." <https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en>

## solvency_capital_requirement

```python
solvency_capital_requirement(
    scenario_set: ScenarioSet,
    own_funds: str | np.ndarray,
    horizon_years: float = 1.0,
    confidence: float = _SOLVENCY_II_CONFIDENCE,
    short_rate: str | None = None,
) -> SolvencyCapitalResult
```

Compute the Solvency II capital requirement (SCR) the way an internal model does: the loss of own funds over one
year that is exceeded only once in 200 years (Article 101).

Own funds are assets minus what is owed, the insurer's buffer. The `solvency_ratio`, own funds divided by the SCR,
is the headline number insurers publish: above 1 the buffer covers the 1-in-200 loss.

Per scenario the loss is OF(0) - D(h) * OF(h), with D the discount factor back to today (1 without `short_rate`);
the SCR is its 99.5% quantile, floored at 0. Check another seed too: with 2,000 scenarios only 10 lie beyond it.

**Args:**

- <u>scenario_set (ScenarioSet):</u> a real-world run spanning at least `horizon_years`.
- <u>own_funds (str &#124; np.ndarray):</u> a factor name, or own funds per scenario and date, shaped (n_simulations, n_steps + 1), e.g. asset values minus liability values.
- <u>horizon_years (float):</u> the risk horizon; 1.0 by default.
- <u>confidence (float):</u> the quantile level, between 0 and 1; 0.995 by default.
- <u>short_rate (str &#124; None):</u> the rate factor to discount own funds back to today with; None by default.

**Returns:**

<u>SolvencyCapitalResult:</u> `scr`, `own_funds` (today), `solvency_ratio`, `expected_shortfall` (the average loss beyond the SCR) and `probability_of_ruin` (the share of scenarios where own funds turn negative).

**Raises:**

- <u>ValueError:</u> if `confidence` is not between 0 and 1, the horizon is not positive or past the run's end, or `own_funds` does not match the run's shape.

**As an example:**

```python
from financescenarios import solvency_capital_requirement

# `result`: a one-year monthly real-world run of SPY and US rates. 1,000,000 in SPY against a liability of 800,000
# that grows at the short rate.
equity = result["us_broad"]
assets = 1_000_000.0 * equity / equity[:, [0]]
liabilities = 800_000.0 / result.discount_factor_paths("united_states_short_rate")
scr = solvency_capital_requirement(
    result, assets - liabilities, horizon_years=1.0, short_rate="united_states_short_rate"
)
```

Which returns (calibrated on 2026-10-04), with own funds of 200,000, at two seeds:

| seed | scr | solvency_ratio | probability_of_ruin |
|-----:|----:|---------------:|--------------------:|
| 42 | 254,117.61 | 0.7870 | 0.0220 |
| 1 | 284,116.51 | 0.7039 | 0.0220 |

**References:**

- European Parliament and Council (2009). "Directive 2009/138/EC (Solvency II)", Article 101. <https://eur-lex.europa.eu/eli/dir/2009/138/oj>

## interest_rate_scr

```python
interest_rate_scr(
    scenario_set: ScenarioSet,
    cashflows: np.ndarray | Sequence[float],
    base_curve: pl.DataFrame,
    up_curve: pl.DataFrame,
    down_curve: pl.DataFrame,
) -> InterestRateScrResult
```

Compute the interest rate capital of a liability under the Solvency II standard formula: how much more it is worth
when rates move by the regulator's prescribed shocks.

The liability is valued on EIOPA's basic risk-free curve and on its two shocked curves, up and down. Lower rates
make future payments dearer today, so for most liabilities the downward shock binds. The answer is the capital the
standard formula sets aside for this one risk, before it is combined with the others. Only the liability is
revalued: for the full interest rate module, revalue the assets on the same curves too.

The formula is SCR = max(BE_up - BE, BE_down - BE, 0), with BE the best estimate on each curve (Delegated
Regulation 2015/35, Articles 165-167). Positive cashflows are payments out, as in `best_estimate`.

**Args:**

- <u>scenario_set (ScenarioSet):</u> the run whose dates (and, for cashflows that differ per scenario, whose scenarios) the cashflows follow.
- <u>cashflows (np.ndarray &#124; Sequence[float]):</u> the amount paid at each date, as in `best_estimate`.
- <u>base_curve (pl.DataFrame):</u> the basic risk-free curve, e.g. `eiopa_risk_free_curve(toolkit, curve="spot_no_va")`.
- <u>up_curve (pl.DataFrame):</u> the curve after the upward shock (`curve="shock_up"`).
- <u>down_curve (pl.DataFrame):</u> the curve after the downward shock (`curve="shock_down"`).

**Returns:**

<u>InterestRateScrResult:</u> `best_estimate`, `best_estimate_up`, `best_estimate_down`, `scr` and `binding_shock` ("up", "down", or None when neither costs anything).

**Raises:**

- <u>ValueError:</u> if a curve or the cashflows are malformed (see `best_estimate`).

**As an example:**

```python
from financescenarios import eiopa_risk_free_curve, interest_rate_scr

# `result` and `annuity` as in the `best_estimate` example, `toolkit` as in the `eiopa_risk_free_curve` one.
base, up, down = (eiopa_risk_free_curve(toolkit, curve=name) for name in ("spot_no_va", "shock_up", "shock_down"))
interest_rate_scr(result, annuity, base, up, down)
```

**References:**

- European Commission (2015). "Commission Delegated Regulation (EU) 2015/35", Articles 165-167 (interest rate risk sub-module). <https://eur-lex.europa.eu/eli/reg_del/2015/35/oj>
- EIOPA. "Risk-free interest rate term structures." <https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en>

## equity_scr

```python
equity_scr(
    type_1_value: float,
    type_2_value: float = 0.0,
    symmetric_adjustment: float = 0.0,
) -> EquityScrResult
```

Compute the equity risk capital of the Solvency II standard formula: the loss on an insurer's shares after the
regulator's prescribed stock market fall.

Type 1 equities (listed in the European Economic Area or the OECD) fall by 39% and type 2 equities (all others:
unlisted shares, private equity, hedge funds, commodities) by 49%, each plus EIOPA's symmetric adjustment. That
adjustment, the "equity dampener", raises the shock by up to 10 points after a rally and lowers it by up to 10
points after a fall, so insurers are not forced to sell into a falling market; EIOPA publishes it every month (see
`eiopa_symmetric_adjustment`).

The two losses combine with a 0.75 correlation, SCR = sqrt(L1 ** 2 + 2 * 0.75 * L1 * L2 + L2 ** 2), so the total
is less than their sum (Delegated Regulation 2015/35, Articles 168-169). Strategic participations, long-term equity
investments and the transitional measure are not covered.

**Args:**

- <u>type_1_value (float):</u> the market value of type 1 equity holdings.
- <u>type_2_value (float):</u> the market value of type 2 equity holdings; 0.0 by default.
- <u>symmetric_adjustment (float):</u> EIOPA's symmetric adjustment as a decimal (0.0771 for 7.71 points), between -0.10 and 0.10; 0.0 by default.

**Returns:**

<u>EquityScrResult:</u> `type_1_charge` and `type_2_charge` (the shocks), `type_1_scr` and `type_2_scr` (the losses) and `scr`, the combined equity risk capital.

**Raises:**

- <u>ValueError:</u> if a value is negative or not finite, or the adjustment lies outside -0.10 to 0.10.

**As an example:**

```python
from financescenarios import equity_scr

equity_scr(type_1_value=1_000_000, type_2_value=250_000, symmetric_adjustment=0.0771)
```

Which returns a type 1 charge of 46.71% and a type 2 charge of 56.71%, losses of 467,100 and 141,775, and an
equity risk capital of 581,048: less than the sum of the two (608,875), since the two types do not fall
perfectly together.

**References:**

- European Commission (2015). "Commission Delegated Regulation (EU) 2015/35", Articles 168-172 (equity risk sub-module and symmetric adjustment). <https://eur-lex.europa.eu/eli/reg_del/2015/35/oj>
- EIOPA. "Symmetric adjustment of the equity capital charge." <https://www.eiopa.europa.eu/tools-and-data/symmetric-adjustment-equity-capital-charge_en>

## martingale_test

```python
martingale_test(
    scenario_set: ScenarioSet,
    asset: str,
    short_rate: str,
    dividend_yield: float = 0.0,
    confidence: float = 0.95,
) -> MartingaleTestResult
```

Check that a risk-neutral run is market consistent: discounted back, a traded asset must be worth today's price on
average at every future date.

In market-consistent scenarios no asset beats the risk-free cash account on average: discounted with each
scenario's own short rate, dividends added back, the asset's average value at any date must equal today's price, up
to Monte Carlo noise. EIOPA's guidelines expect a scenario generator used for valuation to pass this test.

The test is E[D(t) * S(t) * exp(q * t)] = S(0) at every date t, with D the discount factor and q the dividend yield
(Varnell, 2011); a date passes when S(0) lies inside a normal band around the average.

**Args:**

- <u>scenario_set (ScenarioSet):</u> a risk-neutral run.
- <u>asset (str):</u> the price factor to test, such as an equity.
- <u>short_rate (str):</u> the rate factor to discount with.
- <u>dividend_yield (float):</u> the asset's dividend yield q, added back; 0.0 by default.
- <u>confidence (float):</u> the width of each date's band, between 0 and 1; 0.95 by default.

**Returns:**

<u>MartingaleTestResult:</u> `passed`, `pass_rate`, `max_abs_deviation` (largest gap from today's price) and a per-date `table` with 'ratio' (average over today's price) and 'within_band'.

**Raises:**

- <u>KeyError:</u> if either factor is not in the run.
- <u>ValueError:</u> if `confidence` is not between 0 and 1, or `asset` is not a price that starts above 0.

**As an example:**

```python
from financescenarios import martingale_test

# `result`: a risk-neutral ten-year monthly run of SPY ("us_broad") and US rates; `calibration`: its fit.
dividend_yield = calibration.calibrated_params["spy_yield"].initial_value
test = martingale_test(result, "us_broad", "united_states_short_rate", dividend_yield=dividend_yield)
test.table.filter(test.table["time"].is_in([1.0, 5.0, 10.0]))
```

Which returns (calibrated on 2026-10-04), with `passed` False, `pass_rate` 0.825 and `max_abs_deviation` 0.0091:

| date | time | ratio | within_band |
|:-----|-----:|------:|:------------|
| 2027-10-01 | 1 | 0.9990 | false |
| 2031-10-01 | 5 | 0.9994 | true |
| 2036-09-30 | 10 | 0.9922 | true |

A few dates fall outside their band; at other seeds, or 99% confidence, it passes.

**References:**

- EIOPA (2015, updated 2023). "Guidelines on valuation of technical provisions." <https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en>
- Varnell, E.M. (2011). "Economic Scenario Generators and Solvency II." British Actuarial Journal, 16(1), 121-159. <https://doi.org/10.1017/S1357321711000079>

## market_consistency_check

```python
market_consistency_check(
    scenario_set: ScenarioSet,
    short_rate: str,
    discount_curve: pl.DataFrame,
) -> pl.DataFrame
```

Compare the bond curve a risk-neutral run implies with a published risk-free curve, at every whole year of the run.

This asks whether the simulated interest rates price bonds the way the official curve says they should, the
rates-side test EIOPA's guidelines ask of a Solvency II scenario generator. A difference inside about two standard
errors at every maturity means yes. A steady gap means the run was calibrated to a different curve (Treasury yields
rather than EIOPA's, say) or the short rate is not risk neutral.

**Args:**

- <u>scenario_set (ScenarioSet):</u> a risk-neutral run.
- <u>short_rate (str):</u> its short-rate factor.
- <u>discount_curve (pl.DataFrame):</u> the curve to compare with, "maturity" and "rate" columns, annually compounded like EIOPA's.

**Returns:**

<u>pl.DataFrame:</u> "maturity", "model_rate" (annually compounded, from the simulated bond price), "curve_rate", "difference" (model minus curve) and "standard_error" (of the model rate).

**Raises:**

- <u>KeyError:</u> if `short_rate` is not in the run.
- <u>ValueError:</u> if the curve is malformed or the run is shorter than a year.

**As an example:**

```python
from financescenarios import eiopa_risk_free_curve, market_consistency_check

# `result`: the risk-neutral run set up in full in the Solvency II guide,
# https://www.jeroenbouma.com/projects/financescenarios/docs/solvency#martingale-test-example
curve = eiopa_risk_free_curve(toolkit, country="United States")
market_consistency_check(result, "united_states_short_rate", curve)
```

**References:**

- EIOPA (2015, updated 2023). "Guidelines on valuation of technical provisions." <https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en>

## eiopa_risk_free_curve

```python
eiopa_risk_free_curve(
    toolkit: Toolkit,
    country: str = 'Euro Area',
    curve: str = 'spot_no_va',
    as_of: date | str | None = None,
) -> pl.DataFrame
```

Fetch one EIOPA risk-free interest rate curve, the curve European insurers must discount what they owe with under
Solvency II.

It gives the official interest rate for every maturity from 1 to 150 years (Directive 2009/138/EC, Article 77(2)).
Past the last maturity where bonds trade freely (20 years for the euro), the curve bends toward a fixed long-term
rate the regulator sets, the ultimate forward rate. The table plugs straight into
`best_estimate(..., discount_curve=...)`, `interest_rate_scr` and `market_consistency_check`.

The data come through the Finance Toolkit (`fixedincome.get_eiopa_risk_free_rate`) with no API key: one release a
month from January 2023, for the euro, every European Economic Area currency, the Swiss franc, the pound, the
Australian, Canadian and US dollar, the yen and a few others. Rates are annually compounded decimals.

Also known as: EIOPA RFR, Solvency II discount curve, risk-free rate term structure, UFR curve.

**Args:**

- <u>toolkit (Toolkit):</u> the Finance Toolkit `Toolkit`; its start and end dates bound the releases read.
- <u>country (str):</u> the currency area as EIOPA names it, e.g. "United Kingdom"; "Euro Area" by default.
- <u>curve (str):</u> "spot_no_va" (the basic curve, default), "spot_with_va" (with the volatility adjustment), "shock_up" or "shock_down" (after the standard formula's interest rate shocks).
- <u>as_of (date &#124; str &#124; None):</u> the month of the release, e.g. "2026-09"; the latest available by default.

**Returns:**

<u>pl.DataFrame:</u> "maturity" (years) and "rate" (decimal), one row per published maturity.

**Raises:**

- <u>ValueError:</u> if `curve` is unknown, nothing comes back for `country`, or `as_of` has no release.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios import eiopa_risk_free_curve

toolkit = Toolkit(["AAPL"], start_date="2023-01-01")
curve = eiopa_risk_free_curve(toolkit, country="Euro Area", as_of="2026-09")
curve.filter(curve["maturity"].is_in([1.0, 10.0, 20.0, 60.0, 150.0]))
```

Which returns:

| maturity | rate |
|---------:|-----:|
| 1 | 0.0327 |
| 10 | 0.0358 |
| 20 | 0.0360 |
| 60 | 0.0342 |
| 150 | 0.0335 |

**References:**

- EIOPA. "Risk-free interest rate term structures." <https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en>
- European Parliament and Council (2009). "Directive 2009/138/EC (Solvency II)", Article 77. <https://eur-lex.europa.eu/eli/dir/2009/138/oj>

## eiopa_symmetric_adjustment

```python
eiopa_symmetric_adjustment(toolkit: Toolkit, as_of: date | str | None = None) -> float
```

Fetch EIOPA's symmetric adjustment of the Solvency II equity capital charge, the "equity dampener", for one month.

It is the number of percentage points EIOPA adds to the 39% and 49% equity shocks of the standard formula after a
rally, or takes off after a fall, between -10 and +10, based on where equity prices stand against their three-year
average. It keeps insurers from being forced to sell into a falling market. Pass it to
`equity_scr(..., symmetric_adjustment=...)`.

The data come through the Finance Toolkit (`fixedincome.get_eiopa_symmetric_adjustment`), daily from 1991, with no
API key; this reads the month-end value insurers apply at that reporting date.

**Args:**

- <u>toolkit (Toolkit):</u> the Finance Toolkit `Toolkit`; its start and end dates bound the history read.
- <u>as_of (date &#124; str &#124; None):</u> the month, e.g. "2026-09"; the latest available by default.

**Returns:**

<u>float:</u> the symmetric adjustment as a decimal (0.0771 for 7.71 points).

**Raises:**

- <u>ValueError:</u> if nothing comes back or `as_of` has no value.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios import eiopa_symmetric_adjustment

toolkit = Toolkit(["AAPL"], start_date="2023-01-01")
eiopa_symmetric_adjustment(toolkit, as_of="2026-09")
```

Which returns 0.0771: the equity shocks that month are 46.71% and 56.71% instead of 39% and 49%.

**References:**

- EIOPA. "Symmetric adjustment of the equity capital charge." <https://www.eiopa.europa.eu/tools-and-data/symmetric-adjustment-equity-capital-charge_en>

## zero_coupon_curve

```python
zero_coupon_curve(scenario_set: ScenarioSet, short_rate: str) -> pl.DataFrame
```

Compute the bond curve a simulated short rate implies: what a bond paying 1 at each future date is worth today, and
the yield that price implies.

A price of 0.82 at five years, for example, means 1 paid in five years is worth 0.82 today, a yield of
-ln(0.82) / 5 = 4.0% a year. On a risk-neutral run this is the curve the scenarios price bonds off, so setting it
beside the curve the run was calibrated to checks the rates side of market consistency: a gap wider than a few
standard errors means the run is off. `market_consistency_check` does this against a published curve such as
EIOPA's.

The price is the average discount factor across scenarios, P(0, t) = E[D(t)], and the spot rate is
-ln P(0, t) / t, continuously compounded.

**Args:**

- <u>scenario_set (ScenarioSet):</u> a simulated run.
- <u>short_rate (str):</u> the rate factor to discount with.

**Returns:**

<u>pl.DataFrame:</u> "date", "maturity" (years), "price", "standard_error" and "spot_rate" (empty at maturity 0).

**Raises:**

- <u>KeyError:</u> if `short_rate` is not in the run.
- <u>ValueError:</u> if `short_rate` is a price rather than a rate.

**As an example:**

```python
from financescenarios import zero_coupon_curve

# `result`: the risk-neutral run set up in full in the Solvency II guide,
# https://www.jeroenbouma.com/projects/financescenarios/docs/solvency#martingale-test-example
curve = zero_coupon_curve(result, "united_states_short_rate")
curve.filter(curve["maturity"].is_in([1.0, 2.0, 5.0, 10.0]))
```

Which returns (calibrated on 2026-10-04):

| date | maturity | price | standard_error | spot_rate |
|:-----|---------:|------:|---------------:|----------:|
| 2027-10-01 | 1 | 0.9609 | 0.0000 | 0.03993 |
| 2028-09-30 | 2 | 0.9232 | 0.0000 | 0.03993 |
| 2031-10-01 | 5 | 0.8190 | 0.0000 | 0.03993 |
| 2036-09-30 | 10 | 0.6708 | 0.0000 | 0.03993 |

By default the risk-neutral short rate stays at today's 13-week Treasury yield, 3.993%, so every maturity prices
off exactly that rate with no Monte Carlo error.

**References:**

- Varnell, E.M. (2011). "Economic Scenario Generators and Solvency II." British Actuarial Journal, 16(1), 121-159. <https://doi.org/10.1017/S1357321711000079>
- Wüthrich, M.V., Merz, M. (2013). "Financial Modeling, Actuarial Valuation and Solvency in Insurance." Springer. <https://doi.org/10.1007/978-3-642-31392-9>

## curve_discount_factors

```python
curve_discount_factors(discount_curve: pl.DataFrame, times: np.ndarray) -> np.ndarray
```

Compute discount factors from a published interest-rate curve: the value today of 1 paid at each time `t`.

This reads the value off a curve such as EIOPA's risk-free curve (see `eiopa_risk_free_curve`) rather than off the
simulated rates. A 3% rate at ten years, for example, values 1 paid then at 1.03 ** -10 = 0.744.

The formula is (1 + r(t)) ** -t, annually compounded like EIOPA's curves, with r read linearly between the curve's
maturities and held flat before the first and after the last.

**Args:**

- <u>discount_curve (pl.DataFrame):</u> a "maturity" column (years, increasing) and a "rate" column (decimals).
- <u>times (np.ndarray):</u> the times in years to discount from, e.g. a run's `time_grid`.

**Returns:**

<u>np.ndarray:</u> one discount factor per time, 1 at t = 0.

**Raises:**

- <u>ValueError:</u> if the curve lacks the two columns, is empty, unsorted or holds non-finite values.

## write_scenario_files

```python
write_scenario_files(
    scenario_set: ScenarioSet,
    directory: str | Path,
    factors: Sequence[str] | None = None,
    file_format: Literal['csv', 'xlsx'] = 'csv',
    step_stride: int = 1,
) -> list[Path]
```

Write a run as the scenario files actuarial and asset-liability (ALM) systems load: one table per variable, with
one row per trial and one column per projection time.

This hands the simulated scenarios to the system that projects an insurer's liabilities, without any reshaping.
Trials are numbered from 1, as scenario vendors ship them, and columns are labelled by time in years ("0", "1", ...,
"10") rather than by date, so a file reads the same whatever the run's start date. An `index` table gives each
variable's label, category and unit: an annualized decimal rate (0.04 is 4% a year), or a price or index level.
Either kind of run works: risk neutral for market-consistent valuation, real world for projections.

**Args:**

- <u>scenario_set (ScenarioSet):</u> the run to export.
- <u>directory (str &#124; Path):</u> the folder to write into, created if missing.
- <u>factors (Sequence[str] &#124; None):</u> the variables to write; every factor by default.
- <u>file_format ("csv" &#124; "xlsx"):</u> "csv" (default) writes `<variable>.csv` files plus `index.csv`; "xlsx" writes one `scenarios.xlsx` workbook with an `index` sheet and one sheet per variable. Prefer CSV for large runs.
- <u>step_stride (int):</u> keep every n-th time point, e.g. 12 on a monthly run for yearly columns; time 0 is always kept. 1 (every point) by default.

**Returns:**

<u>list[Path]:</u> every file written, the index first.

**Raises:**

- <u>KeyError:</u> if a requested factor is not in the run.
- <u>ValueError:</u> if `step_stride` is below 1, `file_format` is unknown, or two variable names share their first 31 characters (Excel's limit for a sheet name).

**As an example:**

```python
from financescenarios import write_scenario_files

# `result`: the risk-neutral run set up in full in the Solvency II guide,
# https://www.jeroenbouma.com/projects/financescenarios/docs/solvency#martingale-test-example
write_scenario_files(result, "esg_output", step_stride=12)  # annual CSVs
```

Which writes (calibrated on 2026-10-04) `index.csv`, reading:

| variable | label | category | unit |
|:---------|:------|:---------|:-----|
| united_states_short_rate | Short Rate — United States | interest_rates | annualized decimal rate |
| us_broad | US Broad — Equity | equities | price level |

and one CSV per variable, such as `united_states_short_rate.csv`, with 2,000 rows (trials) and columns "trial"
and "0" to "10" (years).
