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

Solvency II on a real-world and a risk-neutral run: the martingale test, best estimate, SCR and EIOPA curves.

```python
from financescenarios import Solvency, best_estimate, solvency_capital_requirement, interest_rate_scr, equity_scr, symmetric_adjustment_cap, eiopa_extrapolation, martingale_test, market_consistency_check, eiopa_risk_free_curve, eiopa_symmetric_adjustment, zero_coupon_curve, curve_discount_factors, write_scenario_files
```

## Solvency

Run an insurer's two Solvency II jobs on one pair of runs and read the answers in one table.

An insurer uses scenarios for two different jobs, and Solvency II names both. The first is valuing what it owes: the
best estimate (Article 77) is the average present value of the future payments under scenarios priced like today's
market, a risk-neutral run, so the liabilities are worth what a market would charge to take them over. The second
is the capital requirement: the Solvency Capital Requirement or SCR (Article 101) is the loss of own funds (assets
minus what is owed) over one year that is exceeded only once in 200 years, the 99.5% Value-at-Risk, measured on a
real-world run because it asks what could actually happen next year.

The calibration is a policy choice: holding the SCR means the insurer still covers its obligations after all but
the worst 0.5% of years over the coming year (Article 101(3)). Own funds over the SCR is the solvency ratio: below 1
the supervisor intervenes. Before valuing anything, `Solvency` checks that the risk-neutral run
really reproduces today's prices, since a best estimate on a run that does not is not market consistent. The
risk-neutral run of `Scenarios.simulate(measure="risk_neutral")` discounts with a Hull-White short rate fitted to
EIOPA's risk-free curve and moves inflation around its breakeven curve, both with historical volatility, so
guarantees and capped indexation get a time value; the volatilities are not implied from swaption or inflation
option prices, so treat that time value as indicative.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Solvency(
    real_world: ScenarioSet,
    risk_neutral: ScenarioSet,
    short_rate: str | None = None,
    asset: str | None = None,
)
```

</details>

## report

Every Solvency II read in one table: whether the run is market consistent, what the payments are worth, own
funds, the SCR and the solvency ratio.

The best estimate is valued on the risk-neutral run. Own funds and the SCR come from the real-world run, where
own funds are the assets minus what is still owed. A solvency ratio above 1 means there is enough capital to
survive a 1-in-200 bad year; the gap above 1 is the room left to take more risk, pay dividends or absorb a
shock before the supervisor steps in. The market-consistency row appears only when the risk-neutral run has an
equity to price; it judges the size of the largest gap from today's price rather than a pass or fail per date,
which a few dates fail by chance once there are thousands of scenarios. A failed check means the best estimate
is not a market price and should not be reported as one.

The formula is as follows:

$$
\text{passed} = \max(\operatorname{abs}(\operatorname{ratio}(t) - 1)) \leq \text{price\_tolerance}
$$

$$
\text{solvency ratio} = \operatorname{OF}(0) / \text{SCR}
$$

Where ratio(t) is the average discounted price at date t over today's price (see `martingale_test`) and OF(0)
today's own funds.

**As an example:**

With `solvency` and `assets` from the class example.

```python
solvency.report(cashflows=[10_000] * 5, assets=assets)
```

Which returns a solvency ratio of 1.26: own funds of 15,635 against an SCR of 12,453.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
report(
    cashflows: Sequence[float] | np.ndarray,
    assets: ScenarioSet | str | np.ndarray,
    horizon_years: float = 1.0,
    price_tolerance: float = 0.02,
) -> pl.DataFrame
```

**Args:**

- <u>cashflows (Sequence[float] &#124; np.ndarray):</u> what is paid: one amount per year (`[10_000] * 5`, paid at each year end), or one amount per date of the run, t0 included.
- <u>assets (ScenarioSet &#124; str &#124; np.ndarray):</u> what backs it on the real-world run: a `Portfolio.compute()` result, a factor name, or a value array shaped (n_simulations, n_steps + 1).
- <u>horizon_years (float):</u> the capital requirement's horizon; 1.0 (one year, as Solvency II asks) by default.
- <u>price_tolerance (float):</u> how far the discounted price may drift from today's, as a fraction, before the run counts as not market consistent; 0.02 (2%) by default. Solvency II and EIOPA's Guideline 58 set no tolerance, so 2% is a judgement: about twice the largest gap a calibrated 2,000-scenario, ten-year run shows from Monte Carlo noise alone (1.0% in the example), yet small next to a mispriced drift.

**Returns:**

<u>pl.DataFrame:</u> 'item', 'value' (formatted to read) and 'meaning', one row per read.

**Raises:**

- <u>ValueError:</u> if `assets` does not have the real-world run's shape, or the yearly payments run past its end.

</details>

## plot

Chart where own funds could be after `horizon_years` across every real-world scenario, discounted to today.

Today's own funds and the 1-in-200 outcome are marked: the gap between them is the SCR that `report()` gives.
The shape matters as much as the line: a long left tail means the capital requirement hinges on a few extreme
scenarios, so it is sensitive to how fat-tailed the real-world calibration is.

**As an example:**

```python
solvency.plot(cashflows=[10_000] * 5, assets=assets)
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
plot(
    cashflows: Sequence[float] | np.ndarray,
    assets: ScenarioSet | str | np.ndarray,
    horizon_years: float = 1.0,
    confidence: float = 0.995,
    ax: Axes | None = None,
) -> Figure
```

**Args:**

- <u>cashflows (Sequence[float] &#124; np.ndarray):</u> what is paid, as for `report()`.
- <u>assets (ScenarioSet &#124; str &#124; np.ndarray):</u> what backs it, as for `report()`.
- <u>horizon_years (float):</u> the capital requirement's horizon; 1.0 (one year, as Solvency II asks) by default.
- <u>confidence (float):</u> the level the SCR is read at; 0.995 (99.5%, as Solvency II asks) by default.
- <u>ax (Axes &#124; None):</u> an existing matplotlib Axes to draw into; a new figure by default.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the chart.

</details>

## write_files

Write both runs as the scenario files liability and ALM systems load, under `real_world/` and `risk_neutral/`.

Each run gets one file per variable, one row per trial and one column per date; see `write_scenario_files`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
write_files(
    directory: str | Path,
    step_stride: int = 1,
    file_format: Literal['csv', 'xlsx'] = 'csv',
)
```

**Args:**

- <u>directory (str &#124; Path):</u> the folder to write into.
- <u>step_stride (int):</u> keep every n-th date, e.g. 12 for yearly columns from a monthly run; 1 by default.
- <u>file_format (str):</u> "csv" (default) or "xlsx".

**Returns:**

<u>dict[str, list[Path]]:</u> the files written, per run.

</details>

## best_estimate

Compute the best estimate of a stream of future payments: their average present value across scenarios, the value
Solvency II asks an insurer to hold for what it owes (Article 77).

On a risk-neutral run the average is the market-consistent value: what the obligation would cost to hand over to
another party at today's prices. The standard error says how precise that number is, and should be small next to
the materiality of the result; more scenarios shrink it. Payments can be fixed or differ per scenario, such as
inflation-linked or profit-sharing benefits; when they do, the gap between this average and the value on one
central scenario is the time value of the options and guarantees the insurer has written. To discount with
EIOPA's risk-free curve instead, as Solvency II prescribes (Article 77(2)), pass `discount_curve`.

The formula is as follows:

$$
\text{PV}_{i} = \text{CF}_{i}(t_{0}) \cdot D_{i}(t_{0}) + \text{CF}_{i}(t_{1}) \cdot D_{i}(t_{1}) + ... + \text{CF}_{i}(T) \cdot D_{i}(T)
$$

$$
\text{BE} = \operatorname{mean}(\text{PV}_{i})
$$

$$
\text{SE} = \operatorname{std}(\text{PV}_{i}) / \sqrt{n}
$$

Where D_i is scenario i's discount factor (see `martingale_test`), or (1 + r(t)) ** -t on a `discount_curve`, and
n the number of scenarios; when the scenarios come in antithetic pairs SE is taken over the n / 2 pair averages.

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

Which returns (calibrated on 2026-10-14):

| annuity | best_estimate | standard_error | p0.5 | p99.5 |
|:--------|--------------:|---------------:|-----:|------:|
| level | 80,532.45 | 0.00 | 80,532.45 | 80,532.45 |
| inflation-indexed | 93,976.96 | 6.15 | 83,336.15 | 106,135.94 |

Indexing the annuity to inflation makes it about 17% dearer, and unlike the level annuity its value is uncertain:
the 99.5th percentile is 13% above the best estimate.

**References:**

- European Parliament and Council (2009). "Directive 2009/138/EC (Solvency II)", Articles 76-77. <https://eur-lex.europa.eu/eli/dir/2009/138/oj>
- EIOPA (2015, updated 2023). "Guidelines on valuation of technical provisions." <https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en>
- Wüthrich, M.V., Merz, M. (2013). "State Price Deflators and Stochastic Discounting", chapter 2 of "Financial Modeling, Actuarial Valuation and Solvency in Insurance." Springer. <https://doi.org/10.1007/978-3-642-31392-9_2>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
best_estimate(
    scenario_set: ScenarioSet,
    cashflows: np.ndarray | Sequence[float],
    short_rate: str | None,
    percentiles: Sequence[float] = _DEFAULT_PERCENTILES,
    discount_curve: pl.DataFrame | None = None,
) -> BestEstimateResult
```

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

</details>

## solvency_capital_requirement

Compute the Solvency II capital requirement (SCR) the way an internal model does: the loss of own funds over one
year that is exceeded only once in 200 years (Article 101).

Own funds are assets minus what is owed, the insurer's buffer. The SCR is the 99.5% one-year Value-at-Risk of that
buffer: the capital that keeps the insurer able to pay policyholders over the coming year in all but the worst
0.5% of outcomes. The `solvency_ratio`, own funds divided by the SCR, is the headline number
insurers publish: above 1 the buffer covers the 1-in-200 loss, below 1 the supervisor requires a recovery plan.

The SCR says nothing about how bad the worst 0.5% are; the expected shortfall does, and a large gap between the
two points to a tail driven by a few extreme scenarios. The probability of ruin is the share of scenarios in
which the buffer is gone after one year.

The formula is as follows:

$$
L_{i} = \text{OF}_{i}(0) - D_{i}(h) \cdot \text{OF}_{i}(h)
$$

$$
\text{SCR} = \max(\text{VaR}_{0.995}(L),\; 0)
$$

$$
\text{ES} = \operatorname{mean}(L_{i} \;\text{given}\; L_{i} \geq \text{VaR}_{0.995}(L))
$$

Where OF is own funds, h the horizon, D_i the discount factor back to today (1 without `short_rate`) and VaR the
empirical quantile of the losses at `confidence`. Check another seed too: with 2,000 scenarios only 10 lie beyond it.

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

- European Parliament and Council (2009). "Directive 2009/138/EC (Solvency II)", Article 101(3). <https://eur-lex.europa.eu/eli/dir/2009/138/oj>
- Wüthrich, M.V., Merz, M. (2013). "Solvency", chapter 9 of "Financial Modeling, Actuarial Valuation and Solvency in Insurance." Springer. <https://doi.org/10.1007/978-3-642-31392-9_9>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
solvency_capital_requirement(
    scenario_set: ScenarioSet,
    own_funds: str | np.ndarray,
    horizon_years: float = 1.0,
    confidence: float = _SOLVENCY_II_CONFIDENCE,
    short_rate: str | None = None,
) -> SolvencyCapitalResult
```

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

</details>

## interest_rate_scr

Compute the interest rate capital of a liability under the Solvency II standard formula: how much more it is worth
when rates move by the regulator's prescribed shocks.

The liability is valued on EIOPA's basic risk-free curve and on its two shocked curves, up and down. Lower rates
make future payments dearer today, so for most liabilities the downward shock binds. The answer is the capital the
standard formula sets aside for this one risk, before it is combined with the others. Only the liability is
revalued: for the full interest rate module, revalue the assets on the same curves too, since what matters is the
mismatch. An insurer whose bonds match the duration of its liabilities loses little under either shock.

The formula is as follows:

$$
\text{SCR} = \max(\text{BE\_up} - \text{BE},\; \text{BE\_down} - \text{BE},\; 0)
$$

Where BE, BE_up and BE_down are the best estimates on the base, upward-shocked and downward-shocked curves
(Delegated Regulation 2015/35, Articles 165-167). Positive cashflows are payments out, as in `best_estimate`.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
interest_rate_scr(
    scenario_set: ScenarioSet,
    cashflows: np.ndarray | Sequence[float],
    base_curve: pl.DataFrame,
    up_curve: pl.DataFrame,
    down_curve: pl.DataFrame,
) -> InterestRateScrResult
```

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

</details>

{% raw %}
## equity_scr

Compute the equity risk capital of the Solvency II standard formula: the loss on an insurer's shares after the
regulator's prescribed stock market fall.

Type 1 equities (listed in the European Economic Area or the OECD) fall by 39% and type 2 equities (all others:
unlisted shares, private equity, hedge funds, commodities) by 49%, each plus EIOPA's symmetric adjustment. That
adjustment, the "equity dampener", raises the shock after a rally and lowers it after a fall, so insurers are not
forced to sell into a falling market; EIOPA publishes it every month (see `eiopa_symmetric_adjustment`). It is
capped at 10 points either way until 29 January 2027 and at 13 points from 30 January 2027 (Delegated Regulation
(EU) 2026/269, point (51): "The symmetric adjustment shall not be lower than – 13 % or higher than 13 %"), so pass
`valuation_date` to apply the cap in force on that date (see `symmetric_adjustment_cap`).

The two losses combine with a 0.75 correlation, so the total is less than their sum (Delegated Regulation 2015/35,
Articles 168-169). Strategic participations, long-term equity investments and the transitional measure are not
covered.

The formula is as follows:

$$
L_{1} = (0.39 + \text{SA}) \cdot V_{1}
$$

$$
L_{2} = (0.49 + \text{SA}) \cdot V_{2}
$$

$$
\text{SCR} = \sqrt{L_{1} ^{2} + 2 \cdot 0.75 \cdot L_{1} \cdot L_{2} + L_{2} ^{2}}
$$

Where V1 and V2 are the market values of type 1 and type 2 equities and SA the symmetric adjustment.

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
- European Commission (2025). "Commission Delegated Regulation (EU) 2026/269", Article 1, point (51) (the 13% cap from 30 January 2027). <http://data.europa.eu/eli/reg_del/2026/269/oj>
- EIOPA. "Symmetric adjustment of the equity capital charge." <https://www.eiopa.europa.eu/tools-and-data/symmetric-adjustment-equity-capital-charge_en>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
equity_scr(
    type_1_value: float,
    type_2_value: float = 0.0,
    symmetric_adjustment: float = 0.0,
    valuation_date: date | str | None = None,
) -> EquityScrResult
```

**Args:**

- <u>type_1_value (float):</u> the market value of type 1 equity holdings.
- <u>type_2_value (float):</u> the market value of type 2 equity holdings; 0.0 by default.
- <u>symmetric_adjustment (float):</u> EIOPA's symmetric adjustment as a decimal (0.0771 for 7.71 points), within the cap in force; 0.0 by default.
- <u>valuation_date (date &#124; str &#124; None):</u> the valuation date, which sets the cap: 0.10 before 30 January 2027, 0.13 from it; None by default, which keeps the 0.10 cap.

**Returns:**

<u>EquityScrResult:</u> `type_1_charge` and `type_2_charge` (the shocks), `type_1_scr` and `type_2_scr` (the losses) and `scr`, the combined equity risk capital.

**Raises:**

- <u>ValueError:</u> if a value is negative or not finite, or the adjustment lies outside the cap in force.

</details>
{% endraw %}

## symmetric_adjustment_cap

The largest symmetric adjustment, up or down, Solvency II allows on a valuation date: 10 percentage points
before 30 January 2027 and 13 from that date.

Directive 2009/138/EC, Article 106(3), originally said the adjustment "shall not result in an equity capital charge
being applied that is more than 10 percentage points lower or 10 percentage points higher than the standard equity
capital charge"; Directive (EU) 2025/2 replaced that with "more than 13 percentage points lower or higher", and
Delegated Regulation (EU) 2026/269, point (51), rewrites Article 172(4) of Delegated Regulation 2015/35 to "The
symmetric adjustment shall not be lower than – 13 % or higher than 13 %", applying "from 30 January 2027"
(Article 2).

**References:**

- European Commission (2015). "Commission Delegated Regulation (EU) 2015/35", Article 172(4). <https://eur-lex.europa.eu/eli/reg_del/2015/35/oj>
- European Commission (2025). "Commission Delegated Regulation (EU) 2026/269", Article 1, point (51), and Article 2. <http://data.europa.eu/eli/reg_del/2026/269/oj>
- European Parliament and Council (2024). "Directive (EU) 2025/2", amending Directive 2009/138/EC (Article 106(3)). <http://data.europa.eu/eli/dir/2025/2/oj>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
symmetric_adjustment_cap(valuation_date: date | str | None = None) -> float
```

**Args:**

- <u>valuation_date (date &#124; str &#124; None):</u> the valuation date, e.g. "2027-03-31"; None keeps the 10-point cap.

**Returns:**

<u>float:</u> 0.10 before 30 January 2027 (or with no date), 0.13 from it.

</details>

## eiopa_extrapolation

Extrapolate a risk-free curve beyond its First Smoothing Point the way EIOPA does from 30 January 2027, so the
effect of the amended Solvency II rules on a best estimate can be measured before EIOPA's own releases switch.

Until 29 January 2027 EIOPA extrapolates past the Last Liquid Point with the Smith-Wilson method. The amended
Directive (Article 77a, as changed by Directive (EU) 2025/2) and Delegated Regulation (EU) 2026/269 replace it:
the curve is interpolated with constant forwards up to the First Smoothing Point (FSP, 20 years for the euro),
and beyond it each forward rate starting at the FSP is a weighted average of the Last Liquid Forward Rate (LLFR,
the forward rate at the FSP) and the Ultimate Forward Rate (UFR), with the weight on the LLFR fading at the
convergence speed alpha. Market information past the FSP therefore keeps more weight than under Smith-Wilson,
so where the forward rate at the FSP sits below the UFR, long rates come out lower and the best estimate of
long-dated liabilities higher.

The formula is as follows:

$$
f(\text{FSP},\; \text{FSP} + h) = \text{UFR}_{c} + (\text{LLFR} - \text{UFR}_{c}) \cdot B(\alpha,\; h),\;\; \text{with}\; B (\alpha,\; h) = (1 - \exp(- \alpha \cdot h)) / (\alpha \cdot h)
$$

$$
z_{c}(\text{FSP} + h) = (\text{FSP} \cdot z_{c}(\text{FSP}) + h \cdot f(\text{FSP},\; \text{FSP} + h)) / (\text{FSP} + h)
$$

$$
z(\text{FSP} + h) = \exp(z_{c}(\text{FSP} + h)) - 1,\;\; \text{with UFR}_{c} = \ln(1 + \text{UFR}) \text{and}\; z_{c} (t) = \ln(1 + z(t))
$$

Where f(FSP, FSP + h) is the continuously compounded forward rate from the FSP for h years and z the annually
compounded zero rate (RFR Technical Documentation EIOPA-BoS-26-198, paragraphs 8.5.5-8.5.8). The LLFR is EIOPA's
swap-volume-weighted average of the one-year forward just before the FSP and the forwards from the FSP to longer
liquid maturities; those volumes come from EIOPA's annual liquidity assessment, so by default the LLFR is the
one-year forward just before the FSP, EIOPA's rule when no liquid maturity lies beyond the FSP. Pass EIOPA's
published LLFR when it differs. The defaults are EIOPA's: alpha "equals 40% for the Swedish Krona and 11% for all
other currencies" (paragraph 8.1.5; Table 4 phases it in from 20% in 2027 for undertakings that apply the
phasing-in), and the euro's FSP is 20 years with an LLFR weight of 100% on the forward just before it (Table 2).

**As an example:**

```python
from financescenarios import eiopa_extrapolation, eiopa_risk_free_curve

# `toolkit` as in the `eiopa_risk_free_curve` example.
published = eiopa_risk_free_curve(toolkit, country="Euro Area", as_of="2026-09")
amended = eiopa_extrapolation(published, ultimate_forward_rate=0.033)
```

**References:**

- EIOPA (2026). "RFR Technical Documentation" (EIOPA-BoS-26-198), applicable from 30 January 2027, section 8.5. <https://www.eiopa.europa.eu/eiopa-publishes-rfr-technical-documentation-become-applicable-30-january-2027-2026-05-26_en>
- European Commission (2025). "Commission Delegated Regulation (EU) 2026/269", amending Delegated Regulation (EU) 2015/35 (Articles 43a and 46). <http://data.europa.eu/eli/reg_del/2026/269/oj>
- European Parliament and Council (2024). "Directive (EU) 2025/2", amending Directive 2009/138/EC (Article 77a). <http://data.europa.eu/eli/dir/2025/2/oj>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
eiopa_extrapolation(
    base_curve: pl.DataFrame,
    ultimate_forward_rate: float,
    first_smoothing_point: int = 20,
    convergence: float = 0.11,
    last_liquid_forward_rate: float | None = None,
) -> pl.DataFrame
```

**Args:**

- <u>base_curve (pl.DataFrame):</u> the curve up to at least the FSP, "maturity" (years) and "rate" (annually compounded), e.g. `eiopa_risk_free_curve(toolkit, curve="spot_no_va")`.
- <u>ultimate_forward_rate (float):</u> the currency's UFR, annually compounded, e.g. 0.033 for 3.3%.
- <u>first_smoothing_point (int):</u> the FSP in whole years; 20 by default, the euro's.
- <u>convergence (float):</u> alpha, 0.11 by default (0.40 for the Swedish krona; higher under the phase-in).
- <u>last_liquid_forward_rate (float &#124; None):</u> the LLFR, continuously compounded; None takes the one-year forward just before the FSP.

**Returns:**

<u>pl.DataFrame:</u> "maturity" (1 to 150 years) and "rate" (annually compounded): the curve as given up to the FSP and extrapolated beyond it.

**Raises:**

- <u>ValueError:</u> if the curve lacks a maturity up to the FSP, or `convergence` is not positive.

</details>

{% raw %}
## martingale_test

Check that a risk-neutral run is market consistent: discounted back, a traded asset must be worth today's price on
average at every future date.

In market-consistent scenarios no asset beats the risk-free cash account on average: discounted with each
scenario's own short rate, dividends added back, the asset's average value at any date must equal today's price, up
to Monte Carlo noise. EIOPA's guidelines expect a scenario generator used for valuation to pass this test.

It tells you whether the run can be trusted to put a price on anything that depends on that asset. A run whose
discounted equity drifts above today's price creates value out of nothing, so the cost of guarantees and options
valued on it is understated (or overstated if it drifts below). Read `max_abs_deviation` first: a gap of a few
tenths of a percent is noise, a steady gap of several percent is a calibration error.

EIOPA's Guideline 58 (paragraph 1.105(b)) asks undertakings to "verify the Martingale test for the asset classes
... that have been used in the calibration process of the ESG" but prescribes no confidence level; the 95% default
is the conventional statistical one. Testing many dates at once needs care. With 120 monthly dates and a 95% band
at each, a perfect martingale still sees about six dates fall outside by chance, so "every date inside its band"
fails a true martingale about half the time. The verdict therefore uses Holm's (1979) step-down adjustment, which
"has a prescribed level of significance protection against error of the first kind for any combination of true
hypotheses" (Holm, 1979, abstract), so the chance of wrongly failing a true martingale stays at most 1 -
`confidence` however strongly the dates are related (neighbouring dates share the same scenarios, so a binomial
count of passing dates, which assumes independent dates, would be misleading). `pass_rate` is still reported
beside `expected_pass_rate`, the rate a true martingale shows on average, as a plain read of the per-date bands.

The formula is as follows:

$$
D(t) = \exp(- (r(t_{0}) + r(t_{1}) + ... + r(t - \text{dt})) \cdot \text{dt})
$$

$$
\operatorname{ratio}(t) = \operatorname{mean}(D(t) \cdot S(t) \cdot \exp(q \cdot t)) / S(0)
$$

$$
\operatorname{band}(t) = \operatorname{mean}(D(t) \cdot S(t) \cdot \exp(q \cdot t)) + / - z \cdot \operatorname{SE}(t)
$$

$$
p(t) = 2 \cdot (1 - N(| \operatorname{mean}(D(t) \cdot S(t) \cdot \exp(q \cdot t)) - S(0) | / \operatorname{SE}(t)))
$$

$$
p_{\text{holm}}(k) = \max(p_{\text{holm}}(k - 1),\; \min(1,\; (m - k + 1) \cdot p(k)))
$$

Where r is the simulated short rate, q the dividend yield, z the normal quantile at (1 + `confidence`) / 2, N the
standard normal distribution, p(k) the k-th smallest of the m dates' p-values, and SE the standard error over
scenarios (over pair averages when the scenarios come in antithetic pairs). A date's band holds when S(0) lies
inside it; the run passes when the smallest Holm-adjusted p-value is at least 1 - `confidence`. A martingale has
ratio(t) = 1 at every date (Varnell, 2011).

**As an example:**

```python
from financescenarios import martingale_test

# `result`: a risk-neutral ten-year monthly run of SPY ("us_broad") and US rates; `calibration`: its fit.
dividend_yield = calibration.calibrated_params["spy_yield"].initial_value
test = martingale_test(result, "us_broad", "united_states_short_rate", dividend_yield=dividend_yield)
test.table.filter(test.table["time"].is_in([1.0, 5.0, 10.0]))
```

Which returns (calibrated on 2026-10-14), with `pass_rate` 0.80 against an `expected_pass_rate` of 0.95 and
`max_abs_deviation` 0.0094:

| date | time | ratio | within_band |
|:-----|-----:|------:|:------------|
| 2027-10-01 | 1 | 0.9990 | false |
| 2031-10-01 | 5 | 0.9992 | true |
| 2036-09-30 | 10 | 0.9918 | false |

A few neighbouring dates fall just outside their band, which is chance on 120 related dates.

**References:**

- EIOPA (2015, updated 2023). "Guidelines on valuation of technical provisions", Guideline 58. <https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en>
- Varnell, E.M. (2011). "Economic Scenario Generators and Solvency II." British Actuarial Journal, 16(1), 121-159. <https://doi.org/10.1017/S1357321711000079>
- Holm, S. (1979). "A Simple Sequentially Rejective Multiple Test Procedure." Scandinavian Journal of Statistics, 6(2), 65-70. <https://www.jstor.org/stable/4615733>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
martingale_test(
    scenario_set: ScenarioSet,
    asset: str,
    short_rate: str,
    dividend_yield: float = 0.0,
    confidence: float = 0.95,
    criterion: Literal['holm', 'every_date'] = 'holm',
) -> MartingaleTestResult
```

**Args:**

- <u>scenario_set (ScenarioSet):</u> a risk-neutral run.
- <u>asset (str):</u> the price factor to test, such as an equity.
- <u>short_rate (str):</u> the rate factor to discount with.
- <u>dividend_yield (float):</u> the asset's dividend yield q, added back; 0.0 by default.
- <u>confidence (float):</u> the width of each date's band and the test's overall confidence; 0.95 by default.
- <u>criterion (str):</u> "holm" (default) for the multiple-testing verdict, or "every_date" to require every date's own band to hold.

**Returns:**

<u>MartingaleTestResult:</u> `passed`, `pass_rate` against `expected_pass_rate`, `family_p_value`, `max_abs_deviation` (largest gap from today's price) and a per-date `table`.

**Raises:**

- <u>KeyError:</u> if either factor is not in the run.
- <u>ValueError:</u> if `confidence` is not between 0 and 1, `criterion` is unknown, or `asset` is not a price that starts above 0.

</details>
{% endraw %}

## market_consistency_check

Compare the bond curve a risk-neutral run implies with a published risk-free curve, at every whole year of the run.

This asks whether the simulated interest rates price bonds the way the official curve says they should, the
rates-side test EIOPA's guidelines ask of a Solvency II scenario generator. A difference inside about two standard
errors at every maturity means yes. A steady gap means the run was calibrated to a different curve (Treasury yields
rather than EIOPA's, say) or the short rate is not risk neutral.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
market_consistency_check(
    scenario_set: ScenarioSet,
    short_rate: str,
    discount_curve: pl.DataFrame,
) -> pl.DataFrame
```

**Args:**

- <u>scenario_set (ScenarioSet):</u> a risk-neutral run.
- <u>short_rate (str):</u> its short-rate factor.
- <u>discount_curve (pl.DataFrame):</u> the curve to compare with, "maturity" and "rate" columns, annually compounded like EIOPA's.

**Returns:**

<u>pl.DataFrame:</u> "maturity", "model_rate" (annually compounded, from the simulated bond price), "curve_rate", "difference" (model minus curve) and "standard_error" (of the model rate).

**Raises:**

- <u>KeyError:</u> if `short_rate` is not in the run.
- <u>ValueError:</u> if the curve is malformed or the run is shorter than a year.

</details>

## eiopa_risk_free_curve

Fetch one EIOPA risk-free interest rate curve, the curve European insurers must discount what they owe with under
Solvency II.

It gives the official interest rate for every maturity from 1 to 150 years (Directive 2009/138/EC, Article 77(2)).
Past the last maturity where markets are deep and liquid, the Last Liquid Point (20 years for the euro, 30 for
the US dollar and 50 for the pound: RFR Technical Documentation EIOPA-BoS-25-599, Tables 7-8), the curve bends
toward a fixed long-term rate the regulator sets, the ultimate forward rate. For long-dated liabilities such as
annuities and pensions that extrapolated part carries most of the value, so the choice of curve (with or without
the volatility adjustment, which adds part of the spread insurers earn on their bonds to damp the effect of
spread swings) moves the best estimate and own funds directly. The table plugs straight into
`best_estimate(..., discount_curve=...)`, `interest_rate_scr` and `market_consistency_check`.

This reads the curve as EIOPA publishes it and does not refit it. Up to 29 January 2027 EIOPA extrapolates past
the Last Liquid Point with the Smith-Wilson method below. From 30 January 2027 the amended rules (Directive (EU)
2025/2 and Delegated Regulation (EU) 2026/269) switch to an extrapolation from the First Smoothing Point, in which
market forward rates past that point keep more weight; releases from that date carry the new method as published,
and `eiopa_extrapolation` applies it to an earlier curve to measure the change in a best estimate.

The formula is as follows:

$$
p(v) = \exp(- \omega \cdot v) \cdot (1 + H(v,\; u) \cdot b)
$$

$$
y(v) = - \ln(p(v)) / v
$$

Where p is the price of a zero-coupon bond maturing at v, omega the ultimate forward rate as a continuous
intensity, u the liquid maturities, H the Wilson kernel and b chosen so p matches the market at every u (RFR
Technical Documentation, sections 9.7-9.12).

The data come through the Finance Toolkit with no API key: one release a month from January 2023, for the euro,
every European Economic Area currency, the Swiss franc, the pound, the Australian, Canadian and US dollar, the yen
and a few others. Rates are annually compounded decimals.

Also known as: EIOPA RFR, Solvency II discount curve, risk-free rate term structure, UFR curve.

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
- EIOPA (2025). "RFR Technical Documentation" (EIOPA-BoS-25-599), section 9 (Smith-Wilson extrapolation). <https://www.eiopa.europa.eu/document/download/f7fca58f-4d24-4441-ac60-de562bf26d77_en>
- EIOPA (2026). "RFR Technical Documentation" (EIOPA-BoS-26-198), applicable from 30 January 2027. <https://www.eiopa.europa.eu/eiopa-publishes-rfr-technical-documentation-become-applicable-30-january-2027-2026-05-26_en>
- European Parliament and Council (2009). "Directive 2009/138/EC (Solvency II)", Article 77. <https://eur-lex.europa.eu/eli/dir/2009/138/oj>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
eiopa_risk_free_curve(
    toolkit: Toolkit,
    country: str = 'Euro Area',
    curve: str = 'spot_no_va',
    as_of: date | str | None = None,
) -> pl.DataFrame
```

**Args:**

- <u>toolkit (Toolkit):</u> the Finance Toolkit `Toolkit`; its start and end dates bound the releases read.
- <u>country (str):</u> the currency area as EIOPA names it, e.g. "United Kingdom"; "Euro Area" by default.
- <u>curve (str):</u> "spot_no_va" (the basic curve, default), "spot_with_va" (with the volatility adjustment), "shock_up" or "shock_down" (after the standard formula's interest rate shocks).
- <u>as_of (date &#124; str &#124; None):</u> the month of the release, e.g. "2026-09"; the latest available by default.

**Returns:**

<u>pl.DataFrame:</u> "maturity" (years) and "rate" (decimal), one row per published maturity.

**Raises:**

- <u>ValueError:</u> if `curve` is unknown, nothing comes back for `country`, or `as_of` has no release.

</details>

## eiopa_symmetric_adjustment

Fetch EIOPA's symmetric adjustment of the Solvency II equity capital charge, the "equity dampener", for one month.

It is the number of percentage points EIOPA adds to the 39% and 49% equity shocks of the standard formula after a
rally, or takes off after a fall, based on where equity prices stand against their three-year average: between -10
and +10 until 29 January 2027 (Delegated Regulation 2015/35, Article 172(4)) and between -13 and +13 from 30
January 2027 (Delegated Regulation (EU) 2026/269, point (51): "The symmetric adjustment shall not be lower than
– 13 % or higher than 13 %"). It is counter-cyclical: after a crash the charge falls, so insurers are not forced
to sell equities into a falling market to restore their ratio, and after a rally it rises. Pass it to
`equity_scr(..., symmetric_adjustment=..., valuation_date=...)`.

The formula is as follows:

$$
\text{SA} = \min(\max(1 / 2 \cdot ((\text{CI} - \text{AI}) / \text{AI} - 0.08),\; - \text{cap}),\; \text{cap})
$$

Where CI is the current level of EIOPA's equity index, AI "the weighted average of the daily levels of the equity
index over the last 36 months" (Delegated Regulation 2015/35, Article 172(2)) and cap 0.10, or 0.13 from 30
January 2027.

The data come through the Finance Toolkit, daily from 1991, with no API key; this reads the month-end value
insurers apply at that reporting date.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios import eiopa_symmetric_adjustment

toolkit = Toolkit(["AAPL"], start_date="2023-01-01")
eiopa_symmetric_adjustment(toolkit, as_of="2026-09")
```

Which returns 0.0771: the equity shocks that month are 46.71% and 56.71% instead of 39% and 49%.

**References:**

- European Commission (2015). "Commission Delegated Regulation (EU) 2015/35", Article 172 (symmetric adjustment). <https://eur-lex.europa.eu/eli/reg_del/2015/35/oj>
- European Commission (2025). "Commission Delegated Regulation (EU) 2026/269", Article 1, point (51). <http://data.europa.eu/eli/reg_del/2026/269/oj>
- EIOPA. "Symmetric adjustment of the equity capital charge." <https://www.eiopa.europa.eu/tools-and-data/symmetric-adjustment-equity-capital-charge_en>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
eiopa_symmetric_adjustment(toolkit: Toolkit, as_of: date | str | None = None) -> float
```

**Args:**

- <u>toolkit (Toolkit):</u> the Finance Toolkit `Toolkit`; its start and end dates bound the history read.
- <u>as_of (date &#124; str &#124; None):</u> the month, e.g. "2026-09"; the latest available by default.

**Returns:**

<u>float:</u> the symmetric adjustment as a decimal (0.0771 for 7.71 points).

**Raises:**

- <u>ValueError:</u> if nothing comes back or `as_of` has no value.

</details>

## zero_coupon_curve

Compute the bond curve a simulated short rate implies: what a bond paying 1 at each future date is worth today, and
the yield that price implies.

A price of 0.82 at five years, for example, means 1 paid in five years is worth 0.82 today, a yield of
-ln(0.82) / 5 = 4.0% a year. On a risk-neutral run this is the curve the scenarios price bonds off, so setting it
beside the curve the run was calibrated to checks the rates side of market consistency: a gap wider than a few
standard errors means the run is off. `market_consistency_check` does this against a published curve such as
EIOPA's.

The formula is as follows:

$$
P(0,\; t) = \operatorname{mean}(D(t))
$$

$$
R(0,\; t) = - \ln(P(0,\; t)) / t
$$

Where D(t) is each scenario's discount factor along its simulated short rate (see `martingale_test`), P the
zero-coupon bond price and R the continuously compounded spot rate (Wüthrich and Merz, 2013, chapter 2).

**As an example:**

```python
from financescenarios import zero_coupon_curve

# `result`: the risk-neutral run set up in full in the Solvency II guide,
# https://www.jeroenbouma.com/projects/financescenarios/docs/solvency#martingale-test-example
curve = zero_coupon_curve(result, "united_states_short_rate")
curve.filter(curve["maturity"].is_in([1.0, 2.0, 5.0, 10.0]))
```

Which returns (calibrated on 2026-10-14):

| date | maturity | price | standard_error | spot_rate |
|:-----|---------:|------:|---------------:|----------:|
| 2027-10-01 | 1 | 0.9602 | 0.0000 | 0.04060 |
| 2028-09-30 | 2 | 0.9220 | 0.0000 | 0.04060 |
| 2031-10-01 | 5 | 0.8163 | 0.0000 | 0.04060 |
| 2036-09-30 | 10 | 0.6663 | 0.0000 | 0.04060 |

By default the risk-neutral short rate stays at today's 13-week Treasury yield, 4.06%, so every maturity prices
off exactly that rate with no Monte Carlo error.

**References:**

- Varnell, E.M. (2011). "Economic Scenario Generators and Solvency II." British Actuarial Journal, 16(1), 121-159. <https://doi.org/10.1017/S1357321711000079>
- Wüthrich, M.V., Merz, M. (2013). "Financial Modeling, Actuarial Valuation and Solvency in Insurance." Springer. <https://doi.org/10.1007/978-3-642-31392-9>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
zero_coupon_curve(scenario_set: ScenarioSet, short_rate: str) -> pl.DataFrame
```

**Args:**

- <u>scenario_set (ScenarioSet):</u> a simulated run.
- <u>short_rate (str):</u> the rate factor to discount with.

**Returns:**

<u>pl.DataFrame:</u> "date", "maturity" (years), "price", "standard_error" and "spot_rate" (empty at maturity 0).

**Raises:**

- <u>KeyError:</u> if `short_rate` is not in the run.
- <u>ValueError:</u> if `short_rate` is a price rather than a rate.

</details>

## curve_discount_factors

Compute discount factors from a published interest-rate curve: the value today of 1 paid at each time `t`.

This reads the value off a curve such as EIOPA's risk-free curve (see `eiopa_risk_free_curve`) rather than off the
simulated rates. A 3% rate at ten years, for example, values 1 paid then at 1.03 ** -10 = 0.744.

The formula is as follows:

$$
\operatorname{DF}(t) = (1 + r(t)) ^{-t}
$$

Where r(t) is the curve's annually compounded rate, like EIOPA's, read linearly between the curve's maturities and
held flat before the first and after the last.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
curve_discount_factors(discount_curve: pl.DataFrame, times: np.ndarray) -> np.ndarray
```

**Args:**

- <u>discount_curve (pl.DataFrame):</u> a "maturity" column (years, increasing) and a "rate" column (decimals).
- <u>times (np.ndarray):</u> the times in years to discount from, e.g. a run's `time_grid`.

**Returns:**

<u>np.ndarray:</u> one discount factor per time, 1 at t = 0.

**Raises:**

- <u>ValueError:</u> if the curve lacks the two columns, is empty, unsorted or holds non-finite values.

</details>

## write_scenario_files

Write a run as the scenario files actuarial and asset-liability (ALM) systems load: one table per variable, with
one row per trial and one column per projection time.

This hands the simulated scenarios to the system that projects an insurer's liabilities, without any reshaping.
Trials are numbered from 1, as scenario vendors ship them, and columns are labelled by time in years ("0", "1", ...,
"10") rather than by date, so a file reads the same whatever the run's start date. An `index` table gives each
variable's label, category and unit: an annualized decimal rate (0.04 is 4% a year), or a price or index level.
Either kind of run works: risk neutral for market-consistent valuation, real world for projections.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
write_scenario_files(
    scenario_set: ScenarioSet,
    directory: str | Path,
    factors: Sequence[str] | None = None,
    file_format: Literal['csv', 'xlsx'] = 'csv',
    step_stride: int = 1,
) -> list[Path]
```

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

</details>

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

{% raw %}
### martingale_test

Check that a risk-neutral run is market consistent: discounted back, a traded asset must be worth today's price on
average at every future date.

In market-consistent scenarios no asset beats the risk-free cash account on average: discounted with each
scenario's own short rate, dividends added back, the asset's average value at any date must equal today's price, up
to Monte Carlo noise. EIOPA's guidelines expect a scenario generator used for valuation to pass this test.

It tells you whether the run can be trusted to put a price on anything that depends on that asset. A run whose
discounted equity drifts above today's price creates value out of nothing, so the cost of guarantees and options
valued on it is understated (or overstated if it drifts below). Read `max_abs_deviation` first: a gap of a few
tenths of a percent is noise, a steady gap of several percent is a calibration error.

EIOPA's Guideline 58 (paragraph 1.105(b)) asks undertakings to "verify the Martingale test for the asset classes
... that have been used in the calibration process of the ESG" but prescribes no confidence level; the 95% default
is the conventional statistical one. Testing many dates at once needs care. With 120 monthly dates and a 95% band
at each, a perfect martingale still sees about six dates fall outside by chance, so "every date inside its band"
fails a true martingale about half the time. The verdict therefore uses Holm's (1979) step-down adjustment, which
"has a prescribed level of significance protection against error of the first kind for any combination of true
hypotheses" (Holm, 1979, abstract), so the chance of wrongly failing a true martingale stays at most 1 -
`confidence` however strongly the dates are related (neighbouring dates share the same scenarios, so a binomial
count of passing dates, which assumes independent dates, would be misleading). `pass_rate` is still reported
beside `expected_pass_rate`, the rate a true martingale shows on average, as a plain read of the per-date bands.

The formula is as follows:

$$
D(t) = \exp(- (r(t_{0}) + r(t_{1}) + ... + r(t - \text{dt})) \cdot \text{dt})
$$

$$
\operatorname{ratio}(t) = \operatorname{mean}(D(t) \cdot S(t) \cdot \exp(q \cdot t)) / S(0)
$$

$$
\operatorname{band}(t) = \operatorname{mean}(D(t) \cdot S(t) \cdot \exp(q \cdot t)) + / - z \cdot \operatorname{SE}(t)
$$

$$
p(t) = 2 \cdot (1 - N(| \operatorname{mean}(D(t) \cdot S(t) \cdot \exp(q \cdot t)) - S(0) | / \operatorname{SE}(t)))
$$

$$
p_{\text{holm}}(k) = \max(p_{\text{holm}}(k - 1),\; \min(1,\; (m - k + 1) \cdot p(k)))
$$

Where r is the simulated short rate, q the dividend yield, z the normal quantile at (1 + `confidence`) / 2, N the
standard normal distribution, p(k) the k-th smallest of the m dates' p-values, and SE the standard error over
scenarios (over pair averages when the scenarios come in antithetic pairs). A date's band holds when S(0) lies
inside it; the run passes when the smallest Holm-adjusted p-value is at least 1 - `confidence`. A martingale has
ratio(t) = 1 at every date (Varnell, 2011).

**As an example:**

```python
from financescenarios import martingale_test

# `result`: a risk-neutral ten-year monthly run of SPY ("us_broad") and US rates; `calibration`: its fit.
dividend_yield = calibration.calibrated_params["spy_yield"].initial_value
test = martingale_test(result, "us_broad", "united_states_short_rate", dividend_yield=dividend_yield)
test.table.filter(test.table["time"].is_in([1.0, 5.0, 10.0]))
```

Which returns (calibrated on 2026-10-14), with `pass_rate` 0.80 against an `expected_pass_rate` of 0.95 and
`max_abs_deviation` 0.0094:

| date | time | ratio | within_band |
|:-----|-----:|------:|:------------|
| 2027-10-01 | 1 | 0.9990 | false |
| 2031-10-01 | 5 | 0.9992 | true |
| 2036-09-30 | 10 | 0.9918 | false |

A few neighbouring dates fall just outside their band, which is chance on 120 related dates.

**References:**

- EIOPA (2015, updated 2023). "Guidelines on valuation of technical provisions", Guideline 58. <https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en>
- Varnell, E.M. (2011). "Economic Scenario Generators and Solvency II." British Actuarial Journal, 16(1), 121-159. <https://doi.org/10.1017/S1357321711000079>
- Holm, S. (1979). "A Simple Sequentially Rejective Multiple Test Procedure." Scandinavian Journal of Statistics, 6(2), 65-70. <https://www.jstor.org/stable/4615733>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
martingale_test(
    scenario_set: ScenarioSet,
    asset: str,
    short_rate: str,
    dividend_yield: float = 0.0,
    confidence: float = 0.95,
    criterion: Literal['holm', 'every_date'] = 'holm',
) -> MartingaleTestResult
```

**Args:**

- <u>scenario_set (ScenarioSet):</u> a risk-neutral run.
- <u>asset (str):</u> the price factor to test, such as an equity.
- <u>short_rate (str):</u> the rate factor to discount with.
- <u>dividend_yield (float):</u> the asset's dividend yield q, added back; 0.0 by default.
- <u>confidence (float):</u> the width of each date's band and the test's overall confidence; 0.95 by default.
- <u>criterion (str):</u> "holm" (default) for the multiple-testing verdict, or "every_date" to require every date's own band to hold.

**Returns:**

<u>MartingaleTestResult:</u> `passed`, `pass_rate` against `expected_pass_rate`, `family_p_value`, `max_abs_deviation` (largest gap from today's price) and a per-date `table`.

**Raises:**

- <u>KeyError:</u> if either factor is not in the run.
- <u>ValueError:</u> if `confidence` is not between 0 and 1, `criterion` is unknown, or `asset` is not a price that starts above 0.

</details>
{% endraw %}

### zero_coupon_curve

Compute the bond curve a simulated short rate implies: what a bond paying 1 at each future date is worth today, and
the yield that price implies.

A price of 0.82 at five years, for example, means 1 paid in five years is worth 0.82 today, a yield of
-ln(0.82) / 5 = 4.0% a year. On a risk-neutral run this is the curve the scenarios price bonds off, so setting it
beside the curve the run was calibrated to checks the rates side of market consistency: a gap wider than a few
standard errors means the run is off. `market_consistency_check` does this against a published curve such as
EIOPA's.

The formula is as follows:

$$
P(0,\; t) = \operatorname{mean}(D(t))
$$

$$
R(0,\; t) = - \ln(P(0,\; t)) / t
$$

Where D(t) is each scenario's discount factor along its simulated short rate (see `martingale_test`), P the
zero-coupon bond price and R the continuously compounded spot rate (Wüthrich and Merz, 2013, chapter 2).

**As an example:**

```python
from financescenarios import zero_coupon_curve

# `result`: the risk-neutral run set up in full in the Solvency II guide,
# https://www.jeroenbouma.com/projects/financescenarios/docs/solvency#martingale-test-example
curve = zero_coupon_curve(result, "united_states_short_rate")
curve.filter(curve["maturity"].is_in([1.0, 2.0, 5.0, 10.0]))
```

Which returns (calibrated on 2026-10-14):

| date | maturity | price | standard_error | spot_rate |
|:-----|---------:|------:|---------------:|----------:|
| 2027-10-01 | 1 | 0.9602 | 0.0000 | 0.04060 |
| 2028-09-30 | 2 | 0.9220 | 0.0000 | 0.04060 |
| 2031-10-01 | 5 | 0.8163 | 0.0000 | 0.04060 |
| 2036-09-30 | 10 | 0.6663 | 0.0000 | 0.04060 |

By default the risk-neutral short rate stays at today's 13-week Treasury yield, 4.06%, so every maturity prices
off exactly that rate with no Monte Carlo error.

**References:**

- Varnell, E.M. (2011). "Economic Scenario Generators and Solvency II." British Actuarial Journal, 16(1), 121-159. <https://doi.org/10.1017/S1357321711000079>
- Wüthrich, M.V., Merz, M. (2013). "Financial Modeling, Actuarial Valuation and Solvency in Insurance." Springer. <https://doi.org/10.1007/978-3-642-31392-9>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
zero_coupon_curve(scenario_set: ScenarioSet, short_rate: str) -> pl.DataFrame
```

**Args:**

- <u>scenario_set (ScenarioSet):</u> a simulated run.
- <u>short_rate (str):</u> the rate factor to discount with.

**Returns:**

<u>pl.DataFrame:</u> "date", "maturity" (years), "price", "standard_error" and "spot_rate" (empty at maturity 0).

**Raises:**

- <u>KeyError:</u> if `short_rate` is not in the run.
- <u>ValueError:</u> if `short_rate` is a price rather than a rate.

</details>

### eiopa_extrapolation

Extrapolate a risk-free curve beyond its First Smoothing Point the way EIOPA does from 30 January 2027, so the
effect of the amended Solvency II rules on a best estimate can be measured before EIOPA's own releases switch.

Until 29 January 2027 EIOPA extrapolates past the Last Liquid Point with the Smith-Wilson method. The amended
Directive (Article 77a, as changed by Directive (EU) 2025/2) and Delegated Regulation (EU) 2026/269 replace it:
the curve is interpolated with constant forwards up to the First Smoothing Point (FSP, 20 years for the euro),
and beyond it each forward rate starting at the FSP is a weighted average of the Last Liquid Forward Rate (LLFR,
the forward rate at the FSP) and the Ultimate Forward Rate (UFR), with the weight on the LLFR fading at the
convergence speed alpha. Market information past the FSP therefore keeps more weight than under Smith-Wilson,
so where the forward rate at the FSP sits below the UFR, long rates come out lower and the best estimate of
long-dated liabilities higher.

The formula is as follows:

$$
f(\text{FSP},\; \text{FSP} + h) = \text{UFR}_{c} + (\text{LLFR} - \text{UFR}_{c}) \cdot B(\alpha,\; h),\;\; \text{with}\; B (\alpha,\; h) = (1 - \exp(- \alpha \cdot h)) / (\alpha \cdot h)
$$

$$
z_{c}(\text{FSP} + h) = (\text{FSP} \cdot z_{c}(\text{FSP}) + h \cdot f(\text{FSP},\; \text{FSP} + h)) / (\text{FSP} + h)
$$

$$
z(\text{FSP} + h) = \exp(z_{c}(\text{FSP} + h)) - 1,\;\; \text{with UFR}_{c} = \ln(1 + \text{UFR}) \text{and}\; z_{c} (t) = \ln(1 + z(t))
$$

Where f(FSP, FSP + h) is the continuously compounded forward rate from the FSP for h years and z the annually
compounded zero rate (RFR Technical Documentation EIOPA-BoS-26-198, paragraphs 8.5.5-8.5.8). The LLFR is EIOPA's
swap-volume-weighted average of the one-year forward just before the FSP and the forwards from the FSP to longer
liquid maturities; those volumes come from EIOPA's annual liquidity assessment, so by default the LLFR is the
one-year forward just before the FSP, EIOPA's rule when no liquid maturity lies beyond the FSP. Pass EIOPA's
published LLFR when it differs. The defaults are EIOPA's: alpha "equals 40% for the Swedish Krona and 11% for all
other currencies" (paragraph 8.1.5; Table 4 phases it in from 20% in 2027 for undertakings that apply the
phasing-in), and the euro's FSP is 20 years with an LLFR weight of 100% on the forward just before it (Table 2).

**As an example:**

```python
from financescenarios import eiopa_extrapolation, eiopa_risk_free_curve

# `toolkit` as in the `eiopa_risk_free_curve` example.
published = eiopa_risk_free_curve(toolkit, country="Euro Area", as_of="2026-09")
amended = eiopa_extrapolation(published, ultimate_forward_rate=0.033)
```

**References:**

- EIOPA (2026). "RFR Technical Documentation" (EIOPA-BoS-26-198), applicable from 30 January 2027, section 8.5. <https://www.eiopa.europa.eu/eiopa-publishes-rfr-technical-documentation-become-applicable-30-january-2027-2026-05-26_en>
- European Commission (2025). "Commission Delegated Regulation (EU) 2026/269", amending Delegated Regulation (EU) 2015/35 (Articles 43a and 46). <http://data.europa.eu/eli/reg_del/2026/269/oj>
- European Parliament and Council (2024). "Directive (EU) 2025/2", amending Directive 2009/138/EC (Article 77a). <http://data.europa.eu/eli/dir/2025/2/oj>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
eiopa_extrapolation(
    base_curve: pl.DataFrame,
    ultimate_forward_rate: float,
    first_smoothing_point: int = 20,
    convergence: float = 0.11,
    last_liquid_forward_rate: float | None = None,
) -> pl.DataFrame
```

**Args:**

- <u>base_curve (pl.DataFrame):</u> the curve up to at least the FSP, "maturity" (years) and "rate" (annually compounded), e.g. `eiopa_risk_free_curve(toolkit, curve="spot_no_va")`.
- <u>ultimate_forward_rate (float):</u> the currency's UFR, annually compounded, e.g. 0.033 for 3.3%.
- <u>first_smoothing_point (int):</u> the FSP in whole years; 20 by default, the euro's.
- <u>convergence (float):</u> alpha, 0.11 by default (0.40 for the Swedish krona; higher under the phase-in).
- <u>last_liquid_forward_rate (float &#124; None):</u> the LLFR, continuously compounded; None takes the one-year forward just before the FSP.

**Returns:**

<u>pl.DataFrame:</u> "maturity" (1 to 150 years) and "rate" (annually compounded): the curve as given up to the FSP and extrapolated beyond it.

**Raises:**

- <u>ValueError:</u> if the curve lacks a maturity up to the FSP, or `convergence` is not positive.

</details>

### curve_discount_factors

Compute discount factors from a published interest-rate curve: the value today of 1 paid at each time `t`.

This reads the value off a curve such as EIOPA's risk-free curve (see `eiopa_risk_free_curve`) rather than off the
simulated rates. A 3% rate at ten years, for example, values 1 paid then at 1.03 ** -10 = 0.744.

The formula is as follows:

$$
\operatorname{DF}(t) = (1 + r(t)) ^{-t}
$$

Where r(t) is the curve's annually compounded rate, like EIOPA's, read linearly between the curve's maturities and
held flat before the first and after the last.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
curve_discount_factors(discount_curve: pl.DataFrame, times: np.ndarray) -> np.ndarray
```

**Args:**

- <u>discount_curve (pl.DataFrame):</u> a "maturity" column (years, increasing) and a "rate" column (decimals).
- <u>times (np.ndarray):</u> the times in years to discount from, e.g. a run's `time_grid`.

**Returns:**

<u>np.ndarray:</u> one discount factor per time, 1 at t = 0.

**Raises:**

- <u>ValueError:</u> if the curve lacks the two columns, is empty, unsorted or holds non-finite values.

</details>

### best_estimate

Compute the best estimate of a stream of future payments: their average present value across scenarios, the value
Solvency II asks an insurer to hold for what it owes (Article 77).

On a risk-neutral run the average is the market-consistent value: what the obligation would cost to hand over to
another party at today's prices. The standard error says how precise that number is, and should be small next to
the materiality of the result; more scenarios shrink it. Payments can be fixed or differ per scenario, such as
inflation-linked or profit-sharing benefits; when they do, the gap between this average and the value on one
central scenario is the time value of the options and guarantees the insurer has written. To discount with
EIOPA's risk-free curve instead, as Solvency II prescribes (Article 77(2)), pass `discount_curve`.

The formula is as follows:

$$
\text{PV}_{i} = \text{CF}_{i}(t_{0}) \cdot D_{i}(t_{0}) + \text{CF}_{i}(t_{1}) \cdot D_{i}(t_{1}) + ... + \text{CF}_{i}(T) \cdot D_{i}(T)
$$

$$
\text{BE} = \operatorname{mean}(\text{PV}_{i})
$$

$$
\text{SE} = \operatorname{std}(\text{PV}_{i}) / \sqrt{n}
$$

Where D_i is scenario i's discount factor (see `martingale_test`), or (1 + r(t)) ** -t on a `discount_curve`, and
n the number of scenarios; when the scenarios come in antithetic pairs SE is taken over the n / 2 pair averages.

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

Which returns (calibrated on 2026-10-14):

| annuity | best_estimate | standard_error | p0.5 | p99.5 |
|:--------|--------------:|---------------:|-----:|------:|
| level | 80,532.45 | 0.00 | 80,532.45 | 80,532.45 |
| inflation-indexed | 93,976.96 | 6.15 | 83,336.15 | 106,135.94 |

Indexing the annuity to inflation makes it about 17% dearer, and unlike the level annuity its value is uncertain:
the 99.5th percentile is 13% above the best estimate.

**References:**

- European Parliament and Council (2009). "Directive 2009/138/EC (Solvency II)", Articles 76-77. <https://eur-lex.europa.eu/eli/dir/2009/138/oj>
- EIOPA (2015, updated 2023). "Guidelines on valuation of technical provisions." <https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en>
- Wüthrich, M.V., Merz, M. (2013). "State Price Deflators and Stochastic Discounting", chapter 2 of "Financial Modeling, Actuarial Valuation and Solvency in Insurance." Springer. <https://doi.org/10.1007/978-3-642-31392-9_2>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
best_estimate(
    scenario_set: ScenarioSet,
    cashflows: np.ndarray | Sequence[float],
    short_rate: str | None,
    percentiles: Sequence[float] = _DEFAULT_PERCENTILES,
    discount_curve: pl.DataFrame | None = None,
) -> BestEstimateResult
```

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

</details>

### solvency_capital_requirement

Compute the Solvency II capital requirement (SCR) the way an internal model does: the loss of own funds over one
year that is exceeded only once in 200 years (Article 101).

Own funds are assets minus what is owed, the insurer's buffer. The SCR is the 99.5% one-year Value-at-Risk of that
buffer: the capital that keeps the insurer able to pay policyholders over the coming year in all but the worst
0.5% of outcomes. The `solvency_ratio`, own funds divided by the SCR, is the headline number
insurers publish: above 1 the buffer covers the 1-in-200 loss, below 1 the supervisor requires a recovery plan.

The SCR says nothing about how bad the worst 0.5% are; the expected shortfall does, and a large gap between the
two points to a tail driven by a few extreme scenarios. The probability of ruin is the share of scenarios in
which the buffer is gone after one year.

The formula is as follows:

$$
L_{i} = \text{OF}_{i}(0) - D_{i}(h) \cdot \text{OF}_{i}(h)
$$

$$
\text{SCR} = \max(\text{VaR}_{0.995}(L),\; 0)
$$

$$
\text{ES} = \operatorname{mean}(L_{i} \;\text{given}\; L_{i} \geq \text{VaR}_{0.995}(L))
$$

Where OF is own funds, h the horizon, D_i the discount factor back to today (1 without `short_rate`) and VaR the
empirical quantile of the losses at `confidence`. Check another seed too: with 2,000 scenarios only 10 lie beyond it.

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

- European Parliament and Council (2009). "Directive 2009/138/EC (Solvency II)", Article 101(3). <https://eur-lex.europa.eu/eli/dir/2009/138/oj>
- Wüthrich, M.V., Merz, M. (2013). "Solvency", chapter 9 of "Financial Modeling, Actuarial Valuation and Solvency in Insurance." Springer. <https://doi.org/10.1007/978-3-642-31392-9_9>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
solvency_capital_requirement(
    scenario_set: ScenarioSet,
    own_funds: str | np.ndarray,
    horizon_years: float = 1.0,
    confidence: float = _SOLVENCY_II_CONFIDENCE,
    short_rate: str | None = None,
) -> SolvencyCapitalResult
```

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

</details>

### interest_rate_scr

Compute the interest rate capital of a liability under the Solvency II standard formula: how much more it is worth
when rates move by the regulator's prescribed shocks.

The liability is valued on EIOPA's basic risk-free curve and on its two shocked curves, up and down. Lower rates
make future payments dearer today, so for most liabilities the downward shock binds. The answer is the capital the
standard formula sets aside for this one risk, before it is combined with the others. Only the liability is
revalued: for the full interest rate module, revalue the assets on the same curves too, since what matters is the
mismatch. An insurer whose bonds match the duration of its liabilities loses little under either shock.

The formula is as follows:

$$
\text{SCR} = \max(\text{BE\_up} - \text{BE},\; \text{BE\_down} - \text{BE},\; 0)
$$

Where BE, BE_up and BE_down are the best estimates on the base, upward-shocked and downward-shocked curves
(Delegated Regulation 2015/35, Articles 165-167). Positive cashflows are payments out, as in `best_estimate`.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
interest_rate_scr(
    scenario_set: ScenarioSet,
    cashflows: np.ndarray | Sequence[float],
    base_curve: pl.DataFrame,
    up_curve: pl.DataFrame,
    down_curve: pl.DataFrame,
) -> InterestRateScrResult
```

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

</details>

{% raw %}
### equity_scr

Compute the equity risk capital of the Solvency II standard formula: the loss on an insurer's shares after the
regulator's prescribed stock market fall.

Type 1 equities (listed in the European Economic Area or the OECD) fall by 39% and type 2 equities (all others:
unlisted shares, private equity, hedge funds, commodities) by 49%, each plus EIOPA's symmetric adjustment. That
adjustment, the "equity dampener", raises the shock after a rally and lowers it after a fall, so insurers are not
forced to sell into a falling market; EIOPA publishes it every month (see `eiopa_symmetric_adjustment`). It is
capped at 10 points either way until 29 January 2027 and at 13 points from 30 January 2027 (Delegated Regulation
(EU) 2026/269, point (51): "The symmetric adjustment shall not be lower than – 13 % or higher than 13 %"), so pass
`valuation_date` to apply the cap in force on that date (see `symmetric_adjustment_cap`).

The two losses combine with a 0.75 correlation, so the total is less than their sum (Delegated Regulation 2015/35,
Articles 168-169). Strategic participations, long-term equity investments and the transitional measure are not
covered.

The formula is as follows:

$$
L_{1} = (0.39 + \text{SA}) \cdot V_{1}
$$

$$
L_{2} = (0.49 + \text{SA}) \cdot V_{2}
$$

$$
\text{SCR} = \sqrt{L_{1} ^{2} + 2 \cdot 0.75 \cdot L_{1} \cdot L_{2} + L_{2} ^{2}}
$$

Where V1 and V2 are the market values of type 1 and type 2 equities and SA the symmetric adjustment.

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
- European Commission (2025). "Commission Delegated Regulation (EU) 2026/269", Article 1, point (51) (the 13% cap from 30 January 2027). <http://data.europa.eu/eli/reg_del/2026/269/oj>
- EIOPA. "Symmetric adjustment of the equity capital charge." <https://www.eiopa.europa.eu/tools-and-data/symmetric-adjustment-equity-capital-charge_en>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
equity_scr(
    type_1_value: float,
    type_2_value: float = 0.0,
    symmetric_adjustment: float = 0.0,
    valuation_date: date | str | None = None,
) -> EquityScrResult
```

**Args:**

- <u>type_1_value (float):</u> the market value of type 1 equity holdings.
- <u>type_2_value (float):</u> the market value of type 2 equity holdings; 0.0 by default.
- <u>symmetric_adjustment (float):</u> EIOPA's symmetric adjustment as a decimal (0.0771 for 7.71 points), within the cap in force; 0.0 by default.
- <u>valuation_date (date &#124; str &#124; None):</u> the valuation date, which sets the cap: 0.10 before 30 January 2027, 0.13 from it; None by default, which keeps the 0.10 cap.

**Returns:**

<u>EquityScrResult:</u> `type_1_charge` and `type_2_charge` (the shocks), `type_1_scr` and `type_2_scr` (the losses) and `scr`, the combined equity risk capital.

**Raises:**

- <u>ValueError:</u> if a value is negative or not finite, or the adjustment lies outside the cap in force.

</details>
{% endraw %}

### liability_values

What the payments not yet made are worth at each date of each scenario, the one due that date included (the assets
still hold it), discounted at that future's own short rate on that date as if it stayed flat. This is how the SCR
revalues the liabilities: when rates fall, they are worth more, and own funds (assets minus liabilities) fall
unless the assets move the same way.

The formula is as follows:

$$
V_{i}(t) = \text{CF}_{i}(t) + \text{CF}_{i}(t + \text{dt}) \cdot \exp(- r_{i}(t) \cdot \text{dt}) + ... + \text{CF}_{i}(T) \cdot \exp(- r_{i}(t) \cdot (T - t))
$$

Where r_i(t) is scenario i's short rate at t, held flat over the remaining term.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
liability_values(
    scenario_set: ScenarioSet,
    cashflows: np.ndarray | Sequence[float],
    short_rate: str,
) -> np.ndarray
```

**Args:**

- <u>scenario_set (ScenarioSet):</u> the run, usually real-world.
- <u>cashflows (np.ndarray &#124; Sequence[float]):</u> one amount per date (t0 included), or one schedule per simulation, shaped (n_simulations, n_steps + 1).
- <u>short_rate (str):</u> the rate factor to discount with.

**Returns:**

<u>np.ndarray:</u> shaped (n_simulations, n_steps + 1), the value at each date of every payment from that date on.

</details>
