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

An insurer's two Solvency II jobs on one pair of runs, read as one table: proving the market-consistent run
reproduces today's prices, valuing the liabilities (the best estimate, Article 77) on it, and measuring the
capital needed to survive a 1-in-200 year (the SCR, Article 101) on the real-world run.

In plain terms: how much is owed, valued at today's market prices, and is there enough capital to keep paying
it after a very bad year?

**As an example:**

```python
risk_neutral = scenarios.simulate(n_simulations=1_000, measure="risk_neutral")
solvency = Solvency(real_world=result, risk_neutral=risk_neutral)
solvency.report(cashflows=[10_000] * 5, assets=assets)
```

## report

```python
report(
    cashflows: Sequence[float] | np.ndarray,
    assets: ScenarioSet | str | np.ndarray,
    horizon_years: float = 1.0,
    price_tolerance: float = 0.02,
) -> pl.DataFrame
```

Every Solvency II read in one table: 'item', 'value' (formatted to read) and 'meaning'.

**Args:**

- <u>cashflows (Sequence[float] &#124; np.ndarray):</u> what is paid: one amount per year (`[10_000] * 5`, paid at each year end), or one amount per date of the run, t0 included.
- <u>assets (ScenarioSet &#124; str &#124; np.ndarray):</u> what backs it on the real-world run: a `Portfolio.compute()` result, a factor name, or a value path array shaped (n_simulations, n_steps + 1).
- <u>horizon_years (float):</u> the capital requirement's horizon, one year under Solvency II.
- <u>price_tolerance (float):</u> how far the discounted price may drift from today's, as a fraction, before the run counts as not market consistent; 2% by default. A pass/fail per date at a 95% band fails some dates by chance once there are thousands of scenarios, so the size of the gap is what counts.

**Returns:**

<u>pl.DataFrame:</u> the market-consistency check (when there is an equity to price), the best estimate, own funds today, the SCR and the solvency ratio.

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

Where own funds could be after `horizon_years` across every real-world scenario, discounted to today, with
today's own funds and the 1-in-200 outcome marked: the gap between them is the SCR `report()` gives.

**Args:**

- <u>cashflows, assets:</u> as for `report()`.
- <u>horizon_years (float):</u> the capital requirement's horizon, one year under Solvency II.
- <u>confidence (float):</u> the level the SCR is read at, 99.5% under Solvency II.
- <u>ax:</u> an existing matplotlib Axes to draw into; a new figure otherwise.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the chart.

## write_files

```python
write_files(
    directory: str | Path,
    step_stride: int = 1,
    file_format: Literal['csv', 'xlsx'] = 'csv',
)
```

Write both runs the way liability and ALM systems load them (see `write_scenario_files`): one file per
variable, one row per trial, under `real_world/` and `risk_neutral/`.

**Args:**

- <u>directory (str &#124; Path):</u> the folder to write into.
- <u>step_stride (int):</u> keep every n-th date, e.g. 12 for yearly columns from a monthly run.
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

Compute the best estimate of a cashflow schedule: the probability-weighted average of its present value
across scenarios, each scenario discounted with its own bank-account deflator (Solvency II Article 77).
Positive cashflows are outgo for a liability.

In plain terms: this is what an insurer must hold today, on average, to pay a stream of future benefits. Each
scenario discounts the benefits with its own interest rates, and the best estimate is the average over all
scenarios; with a risk-neutral run that average is the market-consistent value Solvency II asks for. The
standard error says how precise that average is: a best estimate of 93,142 with a standard error of 4 is pinned
down to within about 8 either way (two standard errors), so it tells you whether `engine.n_simulations` is
enough for the precision the provision is reported to. The percentiles show how widely the present value
spreads across scenarios.

`cashflows` is either one deterministic schedule (an amount per date, t0 included) or a scenario-dependent
array of shape (n_simulations, n_steps + 1). The second is how inflation-linked or asset-share benefits enter:
build them from the run itself, e.g. a benefit indexed with
`result.cumulative_index("united_states_inflation", initial_index=1.0)`.

Also known as: best estimate liability (BEL), market-consistent value of liabilities, technical provision
(before the risk margin).

**Args:**

- <u>scenario_set (ScenarioSet):</u> a simulated run (risk-neutral for a market-consistent best estimate).
- <u>cashflows (np.ndarray &#124; Sequence[float]):</u> either one deterministic schedule of length n_steps + 1 (the amount paid at each date, t0 included), or a scenario-dependent array of shape (n_simulations, n_steps + 1), e.g. an inflation-indexed benefit built from `cumulative_index()`.
- <u>short_rate (str &#124; None):</u> the rate factor to discount with, scenario by scenario; None when `discount_curve` is given.
- <u>percentiles (Sequence[float]):</u> present-value quantiles to report, each in [0, 1].
- <u>discount_curve (pl.DataFrame &#124; None):</u> a published spot-rate curve to discount with instead, the same in every scenario: the Solvency II route, where technical provisions are discounted with EIOPA's risk-free curve (Article 77(2)), see `solvency_controller.eiopa_risk_free_curve`. Scenario-dependent cashflows still vary by scenario.

**Returns:**

<u>BestEstimateResult:</u> best estimate, its standard error, dispersion and percentiles.

**Raises:**

- <u>ValueError:</u> if `cashflows` does not match the run's time grid or holds a non-finite amount.

**Notes:**

- The best estimate is market consistent only when `short_rate` was simulated with `measure: "risk_neutral"`;
  on a real-world run the same number is a real-world discounted expectation.
- A cashflow at t0 is counted undiscounted (D(0) = 1).
- This is the best estimate alone: the risk margin that completes the technical provisions (Article 77) is not
  computed.

**As an example:**

```python
import numpy as np

from financescenarios import best_estimate

# `result` is the risk-neutral run built in the `martingale_test` example (monthly steps, ten years).
annuity = np.zeros(len(result.time_grid))
annuity[12::12] = 10_000.0  # 10,000 a year at each year end
level = best_estimate(result, annuity, short_rate="united_states_short_rate")

index = result.cumulative_index("united_states_inflation", initial_index=1.0).drop("scenario").to_numpy()
indexed = best_estimate(result, annuity * index, short_rate="united_states_short_rate")
```

Which returns (calibrated on 2026-10-04):

| annuity | best_estimate | standard_error | std | p0.5 | p50 | p99.5 |
|:--------|--------------:|---------------:|----:|-----:|----:|------:|
| level | 80,811.82 | 0.00 | 0.00 | 80,811.82 | 80,811.82 | 80,811.82 |
| inflation-indexed | 93,142.15 | 4.05 | 3,760.98 | 83,990.68 | 93,057.01 | 103,236.21 |

Ten yearly payments of 10,000 are worth 80,812 today at the flat 3.99% risk-neutral short rate, the same in
every scenario. Indexing the payments to simulated US inflation raises the best estimate to 93,142 and spreads
it from about 84,000 to 103,000 across scenarios; a standard error of 4 means 2,000 scenarios pin that average
down well within the rounding a provision is reported to.

**References:**

- European Parliament and Council (2009). "Directive 2009/138/EC (Solvency II)", Articles 76-77. <https://eur-lex.europa.eu/eli/dir/2009/138/oj>
- EIOPA (2015, updated 2023). "Guidelines on valuation of technical provisions." <https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en>
- Wüthrich, M.V., Merz, M. (2013). "Financial Modeling, Actuarial Valuation and Solvency in Insurance." Springer. <https://doi.org/10.1007/978-3-642-31392-9>

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

Compute the Solvency II capital requirement as an internal model defines it (Article 101): the Value-at-Risk
of the loss in basic own funds over one year at 99.5% confidence, the 1-in-200-year event. Per scenario,
loss = OF(0) - D(h) * OF(h), with D the bank-account deflator when `short_rate` is given (the change in own
funds is then measured in t0 money) and 1 otherwise (undiscounted); SCR = quantile(loss, confidence), floored
at 0.

In plain terms: own funds are what is left when liabilities are subtracted from assets, the insurer's buffer.
The SCR is the loss of that buffer over the next year that is exceeded in only one scenario in 200, the amount
of capital needed to survive all but the worst 0.5% of years. The `solvency_ratio`, own funds divided by the
SCR, is the headline number insurers publish: above 1 (100%) the buffer covers the 1-in-200 loss, so a ratio of
0.79 means the buffer covers only 79% of it. `expected_shortfall` is the average loss in the scenarios beyond
the SCR, how bad the bad tail is, and `probability_of_ruin` is the share of scenarios where own funds turn
negative by the horizon.

`own_funds` takes a factor name or any array of the run's shape, so an asset side from `Portfolio.compute()`
and a liability side from `best_estimate` projections (or your own model) combine by plain subtraction.

Also known as: SCR, one-year 99.5% Value-at-Risk, internal-model capital requirement, economic capital.

**Args:**

- <u>scenario_set (ScenarioSet):</u> a real-world run spanning at least `horizon_years`.
- <u>own_funds (str &#124; np.ndarray):</u> a factor name, or an own-funds path array of shape (n_simulations, n_steps + 1), e.g. a `Portfolio.compute()` asset value minus a liability path.
- <u>horizon_years (float):</u> the risk horizon, 1 year under Solvency II.
- <u>confidence (float):</u> the VaR level, in (0, 1).
- <u>short_rate (str &#124; None):</u> the rate factor to discount OF(h) back to t0 with.

**Returns:**

<u>SolvencyCapitalResult:</u> SCR, own funds, solvency ratio, expected shortfall and the probability that discounted own funds turn negative.

**Raises:**

- <u>ValueError:</u> if `confidence` is not in (0, 1), the horizon is not positive or lies outside the run, or an own-funds array does not match the run's shape or holds a non-finite value.

**Notes:**

- Run it on a real-world run (the default `measure`): the SCR is a projection of how markets are likely to
  move, not a market-consistent price.
- `horizon_years` snaps to the nearest grid point; the result's `horizon_years` reports the one used.
- This is the internal-model reading of Article 101 on a single stochastic run. It is not the standard formula:
  there is no module aggregation, no loss-absorbing capacity of technical provisions or deferred taxes, and no
  nested revaluation of liabilities inside each one-year scenario. Building the own-funds path (asset-liability
  projection, management actions, taxes) is the caller's model.
- A 99.5% quantile needs sample size: with 2,000 simulations only 10 scenarios sit beyond it, so check the
  result's stability across seeds (`Scenarios.simulate(seed=...)`) before relying on it.

**As an example:**

```python
from datetime import date

from financescenarios import Scenarios, solvency_capital_requirement
from financescenarios.config.config_model import ScenariosConfig

config = ScenariosConfig.model_validate(
    {
        "start_date": date(2026, 10, 1),
        "engine": {"n_simulations": 2000, "n_steps": 12, "frequency": "monthly", "seed": 42},
        "interest_rates": {"countries": [{"name": "United States"}]},
        "inflation": {"countries": [{"name": "United States"}]},
        "unemployment": {"countries": [{"name": "United States"}]},
        "equities": [{"name": "us_broad", "ticker": "SPY", "period": "monthly"}],
    }
)
scenarios = Scenarios.from_config(config)
calibration = scenarios.calibrate(config)
result = scenarios.simulate(config, calibration=calibration)

# 1,000,000 invested in SPY against a liability of 800,000 that grows at the short rate.
equity = result["us_broad"]
assets = 1_000_000.0 * equity / equity[:, [0]]
liabilities = 800_000.0 / result.discount_factor_paths("united_states_short_rate")
scr = solvency_capital_requirement(
    result, assets - liabilities, horizon_years=1.0, short_rate="united_states_short_rate"
)
```

Which returns (calibrated on 2026-10-04), over four seeds (`scenarios.simulate(config, calibration, seed=...)`):

| seed | scr | own_funds | solvency_ratio | expected_shortfall | probability_of_ruin |
|-----:|----:|----------:|---------------:|-------------------:|--------------------:|
| 42 | 254,117.61 | 200,000.00 | 0.7870 | 286,195.26 | 0.0220 |
| 1 | 284,116.51 | 200,000.00 | 0.7039 | 302,668.72 | 0.0220 |
| 2 | 250,819.02 | 200,000.00 | 0.7974 | 271,585.00 | 0.0245 |
| 3 | 256,026.45 | 200,000.00 | 0.7812 | 287,009.99 | 0.0205 |

The 1-in-200 one-year loss on this all-equity balance sheet is about a quarter of the assets, 254,118 at the
default seed, more than the 200,000 of own funds, so the solvency ratio is 79% and about 2% of scenarios end
the year insolvent. Across seeds the SCR moves between 250,819 and 284,117, a 13% spread that comes from
having only 10 scenarios beyond the quantile: the reason to check seeds, or raise `n_simulations`.

**References:**

- European Parliament and Council (2009). "Directive 2009/138/EC (Solvency II)", Article 101. <https://eur-lex.europa.eu/eli/dir/2009/138/oj>
- Wüthrich, M.V., Merz, M. (2013). "Financial Modeling, Actuarial Valuation and Solvency in Insurance." Springer. <https://doi.org/10.1007/978-3-642-31392-9>

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

The interest rate risk capital of a liability under the Solvency II standard formula: its best estimate on the
base risk-free curve and on the two shocked curves EIOPA publishes, and the larger increase of the two (Delegated
Regulation 2015/35, Articles 165-167). Positive cashflows are outgo, as in `best_estimate`.

In plain terms: how much more the insurer would have to hold if interest rates moved by the regulator's
prescribed stress. Lower rates make future payments dearer today, so for most liabilities the downward shock
binds. The answer is the capital the standard formula sets aside for that one risk, before it is combined
with the others.

**Args:**

- <u>scenario_set (ScenarioSet):</u> the run whose time grid (and, for scenario-dependent cashflows, whose scenarios) the cashflows follow.
- <u>cashflows (np.ndarray &#124; Sequence[float]):</u> as in `best_estimate`.
- <u>base_curve (pl.DataFrame):</u> the basic risk-free curve, e.g. `eiopa_risk_free_curve(toolkit, curve="spot_no_va")`.
- <u>up_curve (pl.DataFrame):</u> the curve after the upward shock (`curve="shock_up"`).
- <u>down_curve (pl.DataFrame):</u> the curve after the downward shock (`curve="shock_down"`).

**Returns:**

<u>InterestRateScrResult:</u> the three best estimates, the SCR and which shock binds.

**Raises:**

- <u>ValueError:</u> if a curve or the cashflows are malformed (see `best_estimate`).

**Notes:**

- Only the liability side is revalued: for the full interest rate module, revalue the assets on the same curves
  and take the larger fall in assets minus liabilities.
- This uses EIOPA's published shocked curves; a scenario-based (internal model) capital comes from
  `solvency_capital_requirement` on a real-world run instead.

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

The equity risk capital of the Solvency II standard formula: the loss on an insurer's equities when type 1
equities (listed in the European Economic Area or OECD) fall by 39% and type 2 equities (all others: unlisted,
private equity, hedge funds, commodities) by 49%, each plus EIOPA's symmetric adjustment, combined with a 0.75
correlation (Delegated Regulation 2015/35, Articles 168-169).

In plain terms: how much capital the regulator's simplified formula asks an insurer to hold against a stock
market crash. The symmetric adjustment, or "equity dampener", raises the shock by up to 10 points after a
rally and lowers it by up to 10 points after a fall, so insurers are not forced to sell into a falling market;
EIOPA publishes it every month (`solvency_controller.eiopa_symmetric_adjustment`).

**Args:**

- <u>type_1_value (float):</u> the market value of type 1 equity holdings.
- <u>type_2_value (float):</u> the market value of type 2 equity holdings.
- <u>symmetric_adjustment (float):</u> EIOPA's symmetric adjustment as a decimal (0.0771 for 7.71 points), between -0.10 and 0.10.

**Returns:**

<u>EquityScrResult:</u> the two charges, the loss on each type and the combined equity risk capital.

**Raises:**

- <u>ValueError:</u> if a value is negative or not finite, or the adjustment lies outside [-0.10, 0.10].

**Notes:**

- Strategic participations (a 22% shock), long-term equity investments and the transitional measure are not
  modelled; treat such holdings separately.
- A scenario-based (internal model) view of the same risk comes from `solvency_capital_requirement` on a
  real-world run.

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

Run EIOPA's market-consistency check on a risk-neutral run: the deflated total-return value of a traded asset
must be a martingale, E[D(t) * S(t) * exp(q * t)] = S(0) at every projection date t, up to Monte Carlo noise.
The dividend yield `q` is added back so the test is on total return, not on the price alone.

In plain terms: in market-consistent scenarios no asset beats the risk-free cash account on average. Take the
asset's simulated value at a future date, discount it back along each scenario with that scenario's own
short rate, and average across scenarios: the result must equal today's price. A martingale is exactly that,
a process whose expected future value, in today's money, is its value now. EIOPA's guidelines on technical
provisions expect an economic scenario generator used for valuation to pass this test. A ratio of 1.002 at
year 5, for example, means the deflated asset is 0.2% richer than today's price on average; whether that is a
failure depends on the band around it.

Each date gets a two-sided normal band, `deflated_mean +/- z * standard_error`, with z = 1.96 at the default
95% `confidence`, and the date passes when S(0) lies inside it. Under antithetic variates (paired +/- shocks)
the standard error is computed from the pair averages, the actual independent unit, so antithetic runs get
the tighter band they earned rather than an overstated one. The result's `table` holds one row per date:
`date`, `time` (years), `deflated_mean`, `ratio` (deflated_mean / S(0)), `standard_error`, `lower`, `upper`
and `within_band`.

Also known as: martingale test, market-consistency test, deflated price test.

**Args:**

- <u>scenario_set (ScenarioSet):</u> a simulated run, normally with `measure: "risk_neutral"`.
- <u>asset (str):</u> a price-level factor (an equity, commodity or FX path).
- <u>short_rate (str):</u> the rate factor to deflate with (an annualized decimal).
- <u>dividend_yield (float):</u> the continuous yield `q` the asset's price drift was reduced by (the risk-neutral equity drift is r - q), added back so the test is on total return. 0.0 for a non-dividend asset.
- <u>confidence (float):</u> two-sided level of each date's normal band, in (0, 1).

**Returns:**

<u>MartingaleTestResult:</u> pass/fail, pass rate, the largest deviation, and the table.

**Raises:**

- <u>KeyError:</u> if either factor is not in the run.
- <u>ValueError:</u> if `confidence` is not in (0, 1), `dividend_yield` is not finite, `asset` is not a price, the asset starts at a non-positive value, or `short_rate` is a price rather than a rate.

**Notes:**

- `passed` and `pass_rate` count only the dates after t0: at t0 the band has zero width and S(0) is the
  deflated value itself, so its `within_band` flag can read False from floating-point rounding alone.
- `passed` asks for S(0) inside *every* date's band, a strict test: neighboring dates share most of their
  paths, so one unlucky batch of scenarios can push a run of consecutive dates out together. Check the
  `pass_rate`, the size of `max_abs_deviation` and another seed before calling a run broken.
- A run that fails at many dates has an asset drift that is not the short rate net of `q`: typically a
  real-world run tested by mistake, or a `q` that does not match the one the risk-neutral equity drift used
  (see how `Equities.calibrate_risk_neutral` sources `r` and `q`; `q` is the matching `dividend_yield[]`
  entry's `initial_value`).

**As an example:**

```python
from datetime import date

from financescenarios import Scenarios, martingale_test
from financescenarios.config.config_model import ScenariosConfig

config = ScenariosConfig.model_validate(
    {
        "start_date": date(2026, 10, 1),
        "engine": {"n_simulations": 2000, "n_steps": 120, "frequency": "monthly", "seed": 42, "antithetic": True},
        "toolkit": {"start_date": date(2010, 1, 1)},
        "interest_rates": {"defaults": {"measure": "risk_neutral"}, "countries": [{"name": "United States"}]},
        "inflation": {"countries": [{"name": "United States"}]},
        "unemployment": {"countries": [{"name": "United States"}]},
        "equities": [
            {"name": "us_broad", "ticker": "SPY", "measure": "risk_neutral", "volatility_source": "realized"}
        ],
        "dividend_yield": [{"name": "spy_yield", "ticker": "SPY"}],
    }
)
scenarios = Scenarios.from_config(config)
calibration = scenarios.calibrate(config)
result = scenarios.simulate(config, calibration=calibration)

dividend_yield = calibration.calibrated_params["spy_yield"].initial_value
test = martingale_test(result, "us_broad", "united_states_short_rate", dividend_yield=dividend_yield)
test.table.filter(test.table["time"].is_in([1.0, 2.0, 5.0, 10.0]))
```

Which returns (calibrated on 2026-10-04), with `passed` False, `pass_rate` 0.825 and `max_abs_deviation` 0.0091:

| date | time | deflated_mean | ratio | standard_error | lower | upper | within_band |
|:-----|-----:|--------------:|------:|---------------:|------:|------:|:------------|
| 2027-10-01 | 1 | 768.89 | 0.9990 | 0.3218 | 768.26 | 769.52 | false |
| 2028-09-30 | 2 | 769.37 | 0.9996 | 0.7031 | 767.99 | 770.74 | true |
| 2031-10-01 | 5 | 769.15 | 0.9994 | 1.7385 | 765.74 | 772.55 | true |
| 2036-09-30 | 10 | 763.65 | 0.9922 | 3.1574 | 757.47 | 769.84 | true |

SPY starts at 769.64 with r = 3.99% and q = 0.99%, so its risk-neutral price drift is 3.01%. Deflated and with
the dividends added back it stays within 0.9% of 769.64 for all ten years, but 21 of 120 monthly dates (a few
around year one and a run between years 7.7 and 10) fall just outside their tight 95% band, so the strict test
fails at this seed. At seeds 2 and 3 it passes at every date, and at 99% confidence it passes for seed 42 too:
Monte Carlo noise, not a wrong drift. Leaving out `q` fails every date, drifting up to 10% away from S(0) by
year 10, the signature of a dividend-yield mismatch.

**References:**

- EIOPA (2015, updated 2023). "Guidelines on valuation of technical provisions." <https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en>
- Varnell, E.M. (2011). "Economic Scenario Generators and Solvency II." British Actuarial Journal, 16(1), 121-159. <https://doi.org/10.1017/S1357321711000079>
- Wüthrich, M.V., Merz, M. (2013). "Financial Modeling, Actuarial Valuation and Solvency in Insurance." Springer. <https://doi.org/10.1007/978-3-642-31392-9>

## market_consistency_check

```python
market_consistency_check(
    scenario_set: ScenarioSet,
    short_rate: str,
    discount_curve: pl.DataFrame,
) -> pl.DataFrame
```

Set the zero-coupon curve a risk-neutral run implies beside a published risk-free curve, at every whole year of
the run: the curve-side market-consistency test of a Solvency II economic scenario generator (EIOPA's guidelines
on valuation ask the scenarios to reproduce the risk-free curve they are calibrated to).

In plain terms: do the simulated interest rates price bonds the way the official curve says they should? A
difference inside about two standard errors at every maturity means yes; a steady gap means the run was
calibrated to a different curve (e.g. Treasury yields rather than EIOPA's) or the short rate is not risk
neutral.

**Args:**

- <u>scenario_set (ScenarioSet):</u> a risk-neutral run.
- <u>short_rate (str):</u> its short-rate factor.
- <u>discount_curve (pl.DataFrame):</u> the curve to compare with, "maturity" and "rate" columns, annually compounded like EIOPA's.

**Returns:**

<u>pl.DataFrame:</u> "maturity", "model_rate" (annually compounded, from the Monte Carlo bond price), "curve_rate", "difference" (model minus curve) and "standard_error" (of the model rate).

**Raises:**

- <u>KeyError:</u> if `short_rate` is not in the run.
- <u>ValueError:</u> if the curve is malformed or the run is shorter than a year.

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

One EIOPA risk-free interest rate term structure, the curve European insurers must discount their liabilities
with under Solvency II (Directive 2009/138/EC, Article 77(2)), as a maturity/rate table ready for
`best_estimate(..., discount_curve=...)`, `interest_rate_scr` and `market_consistency_check`.

In plain terms: the official interest rate for every maturity from 1 to 150 years that a European insurer must
use to value what it owes. Past the last maturity where bonds trade freely (20 years for the euro), the curve
bends toward a fixed long-term rate the regulator sets, the ultimate forward rate.

The data come through the Finance Toolkit (`fixedincome.get_eiopa_risk_free_rate`), with no API key: one
release a month from January 2023, for the euro and every European Economic Area currency plus the Swiss
franc, pound, Australian, Canadian and US dollar, yen and a few others. Rates are annually compounded decimals.

Also known as: EIOPA RFR, Solvency II discount curve, risk-free rate term structure, UFR curve.

**Args:**

- <u>toolkit (Toolkit):</u> the Finance Toolkit `Toolkit`; its start and end dates bound the releases read.
- <u>country (str):</u> the currency area as EIOPA names it, e.g. "Euro Area", "United Kingdom", "United States".
- <u>curve (str):</u> "spot_no_va" (the basic curve, default), "spot_with_va" (with the volatility adjustment), "shock_up" or "shock_down" (after the standard formula's interest rate shocks).
- <u>as_of (date &#124; str &#124; None):</u> the month of the release, e.g. "2026-09"; the latest available by default.

**Returns:**

<u>pl.DataFrame:</u> "maturity" (years) and "rate" (decimal), one row per published maturity.

**Raises:**

- <u>ValueError:</u> if `curve` is unknown, nothing comes back for `country`, or `as_of` has no release.

**References:**

- EIOPA. "Risk-free interest rate term structures." <https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en>
- European Parliament and Council (2009). "Directive 2009/138/EC (Solvency II)", Article 77. <https://eur-lex.europa.eu/eli/dir/2009/138/oj>

## eiopa_symmetric_adjustment

```python
eiopa_symmetric_adjustment(toolkit: Toolkit, as_of: date | str | None = None) -> float
```

EIOPA's symmetric adjustment of the Solvency II equity capital charge (the "equity dampener") at the end of a
month, ready for `solvency_model.equity_scr(..., symmetric_adjustment=...)`.

In plain terms: the number of percentage points EIOPA adds to (after a rally) or takes off (after a fall) the
39% and 49% equity shocks of the standard formula, between -10 and +10, based on where equity prices stand
against their three-year average.

The data come through the Finance Toolkit (`fixedincome.get_eiopa_symmetric_adjustment`), daily from 1991,
with no API key; this reads the month-end value insurers apply at that reporting date.

**Args:**

- <u>toolkit (Toolkit):</u> the Finance Toolkit `Toolkit`; its start and end dates bound the history read.
- <u>as_of (date &#124; str &#124; None):</u> the month, e.g. "2026-09"; the latest available by default.

**Returns:**

<u>float:</u> the symmetric adjustment as a decimal (0.0771 for 7.71 points).

**Raises:**

- <u>ValueError:</u> if nothing comes back or `as_of` has no value.

**References:**

- EIOPA. "Symmetric adjustment of the equity capital charge." <https://www.eiopa.europa.eu/tools-and-data/symmetric-adjustment-equity-capital-charge_en>

## zero_coupon_curve

```python
zero_coupon_curve(scenario_set: ScenarioSet, short_rate: str) -> pl.DataFrame
```

Compute the zero-coupon bond curve a simulated short rate implies: the Monte Carlo price P(0, t) = E[D(t)] at
every date, its standard error, and the continuously compounded spot rate -ln P(0, t) / t.

In plain terms: this is what the scenarios say a bond paying 1 at date t is worth today, and the yield that
price implies. A price of 0.82 at five years, for example, means 1 paid in five years is worth 0.82 today, a
spot rate of -ln(0.82) / 5 = 4.0% a year. Under a risk-neutral run it is the curve the scenarios price bonds
off, so setting it beside the input term structure (or the EIOPA risk-free rate curve you calibrated to) is the
curve-side martingale check: a gap wider than a few standard errors means the time discretization or the
curve fit is off. With `risk_neutral_forward_curve: true` the expected short-rate path is built to reproduce
today's forward curve, so this table should line up with that input curve.

Also known as: Monte Carlo discount curve, model-implied term structure, zero curve.

**Args:**

- <u>scenario_set (ScenarioSet):</u> a simulated run.
- <u>short_rate (str):</u> the rate factor to integrate (an annualized decimal).

**Returns:**

<u>pl.DataFrame:</u> "date", "maturity" (years), "price", "standard_error", "spot_rate" (null at maturity 0).

**Raises:**

- <u>KeyError:</u> if `short_rate` is not in the run.
- <u>ValueError:</u> if `short_rate` is a price rather than a rate.

**Notes:**

- Under antithetic variates the standard error is computed from pair averages, as in `martingale_test`.
- No EIOPA risk-free rate curve is bundled or fetched; the comparison curve is the caller's.

**As an example:**

```python
from financescenarios import zero_coupon_curve

# `result` is the risk-neutral run built in the `martingale_test` example.
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

With the default `risk_neutral_forward_curve: false` the risk-neutral short rate is a flat path at today's
13-week Treasury yield, 3.993%, so every maturity prices off exactly that rate with no Monte Carlo error; a
stochastic short rate gives a sloped curve and nonzero standard errors.

**References:**

- Varnell, E.M. (2011). "Economic Scenario Generators and Solvency II." British Actuarial Journal, 16(1), 121-159. <https://doi.org/10.1017/S1357321711000079>
- Wüthrich, M.V., Merz, M. (2013). "Financial Modeling, Actuarial Valuation and Solvency in Insurance." Springer. <https://doi.org/10.1007/978-3-642-31392-9>

## curve_discount_factors

```python
curve_discount_factors(discount_curve: pl.DataFrame, times: np.ndarray) -> np.ndarray
```

Discount factors from a spot-rate curve, `(1 + r(t)) ** -t` with `r` interpolated linearly between the curve's
maturities and held flat beyond its first and last: the annually compounded convention of the EIOPA risk-free
curves (`solvency_controller.eiopa_risk_free_curve`).

In plain terms: the value today of 1 paid at each time `t`, read off a published interest-rate curve rather
than off the simulated rates. A 3% rate at ten years, for example, values 1 paid then at 1.03 ** -10 = 0.744.

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

Write a run as actuarial scenario files: per variable, one row per trial (1-based, the convention economic
scenario generator vendors ship) and one column per projection time in years ("0", "0.0833", ..., "10"), plus
an `index` table naming each variable's label, category and unit. Columns are keyed by time rather than date so
a file reads the same whatever the run's start date.

In plain terms: this hands the simulated scenarios to the system that projects the insurer's liabilities. Most
such systems load scenarios as a table per variable with one row per scenario and one column per year, which is
exactly what this writes, so a run can feed a liability model without any reshaping.

Also known as: ESG scenario file export, actuarial scenario files, scenario set output.

**Args:**

- <u>scenario_set (ScenarioSet):</u> the run to export.
- <u>directory (str &#124; Path):</u> destination directory, created if missing.
- <u>factors (Sequence[str] &#124; None):</u> variables to write; every factor by default.
- <u>file_format ("csv" &#124; "xlsx"):</u> "csv" writes `<variable>.csv` files and `index.csv`; "xlsx" writes one `scenarios.xlsx` workbook with an `index` sheet and one sheet per variable (names cut to Excel's 31 characters).
- <u>step_stride (int):</u> keep every n-th time point, e.g. 12 on a monthly run for the annual grid most liability models project on. Time 0 is always kept.

**Returns:**

<u>list[Path]:</u> every file written, the index first.

**Raises:**

- <u>KeyError:</u> if a requested factor is not in the run.
- <u>ValueError:</u> if `step_stride` < 1, `file_format` is unknown, or two variables collide on the same 31-character worksheet name.

**Notes:**

- The `unit` column reads "annualized decimal rate" for a rate factor (0.04 is 4% a year), "price level"
  for a factor that simulates a price directly (an equity, FX rate, commodity or dividend index) and "index
  level" for the leading indicator; see the units documentation.
- The Excel workbook is written in streaming mode, so cells are not all held in memory, but a sheet still holds
  `n_simulations` rows per variable: prefer CSV for large runs.
- The files hold the run as simulated: a risk-neutral run for market-consistent valuation, a real-world run for
  projections, so either can be handed to a liability model.

**As an example:**

```python
from financescenarios import write_scenario_files

# `result` is the risk-neutral run built in `solvency_model.martingale_test`'s example (monthly, ten years).
write_scenario_files(result, "esg_output", step_stride=12)  # annual CSVs
write_scenario_files(result, "esg_output", file_format="xlsx", step_stride=12)  # one workbook
```

Which writes (calibrated on 2026-10-04) `index.csv` plus `united_states_inflation.csv`,
`united_states_short_rate.csv`, `united_states_unemployment.csv`, `us_broad.csv` and `spy_yield.csv`, with
`index.csv` reading:

| variable | label | category | unit |
|:---------|:------|:---------|:-----|
| united_states_inflation | Inflation — United States | inflation | annualized decimal rate |
| united_states_short_rate | Short Rate — United States | interest_rates | annualized decimal rate |
| united_states_unemployment | Unemployment — United States | unemployment | annualized decimal rate |
| us_broad | US Broad — Equity | equities | price level |
| spy_yield | Spy Yield — Dividend Yield | dividend_yield | annualized decimal rate |

and `united_states_short_rate.csv` starting:

| trial | 0 | 1 | 2 | ... | 10 |
|------:|--:|--:|--:|:---:|---:|
| 1 | 0.03993 | 0.03993 | 0.03993 | ... | 0.03993 |
| 2 | 0.03993 | 0.03993 | 0.03993 | ... | 0.03993 |
| 3 | 0.03993 | 0.03993 | 0.03993 | ... | 0.03993 |

Each variable is a 2,000-row file with one column per year from 0 to 10: `step_stride=12` kept every twelfth
monthly step, the annual grid most liability models project on. The short rate is flat at 3.993% because a
risk-neutral rate without `risk_neutral_forward_curve` is today's level held fixed.
