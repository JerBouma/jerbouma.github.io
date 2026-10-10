---
title: "Portfolio"
seo_title: "Portfolio Reference – Finance Scenarios"
excerpt: "Read a finished run through an investment portfolio: allocations, cashflows, glidepaths, risk metrics and factor exposure."
description: "Read a finished run through an investment portfolio: allocations, cashflows, glidepaths, risk metrics and factor exposure."
author_profile: false
permalink: /projects/financescenarios/docs/reference/portfolio
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Read a finished run through an investment portfolio: allocations, cashflows, glidepaths, risk metrics and factor exposure. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios import Portfolio, CashflowRule, GlidepathCheckpoint, PortfolioSummary, PortfolioPreset, load_portfolio_library, load_portfolio_preset, compute_portfolio_factor_exposure
```

## Portfolio

```python
Portfolio(
    scenario_set: ScenarioSet,
    config: ScenariosConfig | None = None,
    category_map: dict[str, str] | None = None,
    preset: PortfolioPreset | None = None,
)
```

The Portfolio module turns simulated (or historical) markets into the value of an actual
investment portfolio: pick a weight per asset, say 60% US equities and 40% US government
bonds, and it returns how that portfolio's value would develop in every simulated scenario,
together with the value of each holding ("sleeve") on its own.

```python
portfolio = Portfolio.from_preset(result, preset="balanced_60_40")    # list_presets(kind="portfolios") shows them all
values = portfolio.compute(initial_value=100_000, rebalance_every=12)
values.describe()                                              # the portfolio's return, and each holding's value
portfolio.risk_metrics()                                       # drawdown, VaR and loss probability
```

In plain terms: the scenario generator answers "what could markets do?"; this module answers
"what would that mean for my money?". It supports buy-and-hold and rebalanced portfolios,
allocations that shift over time (target-date glidepaths), regular savings and retirement
withdrawals, fees and trading costs, and then reads the result back as plain answers: how
likely the money lasts, how likely a goal is reached, what it is worth after inflation, how
deep the drawdowns are, and how far the weights drift. It is entirely optional and read-only:
it never calibrates or simulates anything and never changes the `ScenarioSet` it is given.

What a sleeve can hold. Every sleeve's asset class ("category") is read off the scenario set
itself: `Scenarios.simulate()` stamps each path's category onto its result
(`ScenarioSet.factor_categories`, round-tripped by `run_io_controller`), so a `ScenarioSet`
is the only thing a `Portfolio` needs. Only categories you can actually hold are accepted
(`portfolio_model.INVESTABLE_FACTOR_TYPES`), and they split in two:

- Level (price) factors, `equities` and `commodities`, simulate a price directly, so a
  sleeve's growth is that price path rebased to 1.0 at the start.
- Rate factors, `interest_rates`, `credit` and `real_estate`, simulate a rate, not a price.
  Their growth is `ScenarioSet.cumulative_index(factor, initial_index=1.0)`, the engine's
  rate-to-index transform, which treats the rate as the return of a rolled money-market or
  floating-rate holding. `real_estate` belongs here because its simulated path is a
  house-price *growth rate*, the same fork `Reporting.convert("real_estate")` makes.

Every other category (`inflation`, `unemployment`, `dividend_yield`, `yield_curve`,
`leading_indicator`, `fx`, ...) is not something a portfolio can hold, and `compute()` raises
a `ValueError` rather than silently letting a caller allocate to "inflation". A "strategic
allocation" (one factor per broad asset class: a country's equity index, its short rate, a
credit bucket) and a sector portfolio (several `equities` factors such as the US GICS sector
clouds `tech`, `financials`, `energy` of the broad factor set) are the same weighted-sleeve
computation over a different selection; there is no separate sector code path.

How the portfolio moves. Each sleeve starts at `weight * initial_value`. With buy-and-hold
(`rebalance_every=None`, the default) each sleeve then simply grows with its own asset, so the
weights only hold at the start: `sleeve(t) = weight * initial_value * growth(t)`. With
periodic rebalancing (`rebalance_every=N`) every sleeve is reset to `weight * portfolio value`
every N steps, the "constant-mix" discipline of selling what rose and buying what fell
([Perold and Sharpe, 1988](https://doi.org/10.2469/faj.v44.n1.16)); `rebalance_every=1`
blends every sleeve's return each step. With a tolerance band (`rebalance_band=X`), a
simulation rebalances the moment any sleeve's *actual* weight is more than X (absolute,
0.05 for 5 points) away from its target, the "5/25 rule" discipline; drift depends on the
path, so each simulation triggers on its own. A band can be used alone or with a calendar,
whichever fires first. The portfolio value is the sum of the sleeves, with no interaction
between sleeves beyond what rebalancing introduces.

Options that change the result:

- Glidepath (`compute_glidepath()`): the target weights themselves move over the horizon,
  starting aggressive and gliding to conservative as a target date approaches.
- Cashflows (`cashflow_rules`, built with `cashflow_rule()`): regular contributions and
  withdrawals, optionally indexed to a simulated inflation factor (`inflation_factor`) so a
  withdrawal keeps its purchasing power. A portfolio that is emptied stays at exactly 0.
- Fees (`fee_rate`): an annual expense ratio charged on assets every step.
- Transaction costs (`transaction_cost_rate`): a fraction of the amount traded, charged only
  when a rebalance actually happens.
- Bond duration (`durations`): price a government or corporate bond sleeve as a
  constant-duration bond fund, so a rate rise marks its price down, instead of the default
  floating-rate roll.
- Multiple currencies (`config`): convert each foreign-currency sleeve into the run's
  reporting currency before weighting.

Reading the result. `compute()` returns a new `ScenarioSet` holding `"portfolio"` and one
`"<factor>_value"` path per sleeve, so every existing `ScenarioSet` method (`to_dataframe()`,
`summary_statistics()`, `.plot()`, ...) works on it. On top of that, `withdrawal_success()`,
`goal_probability()`, `real_value()`, `risk_metrics()` and `weight_drift()` each answer one
question, `summary()` answers them all at once, and `benchmark()` compares two portfolios.
Named allocations (60/40, All Weather, a target-date glidepath, ...) ship as presets; see
`from_preset()`.

Historical backtesting. `historical_data.backtest_model.build_synthetic_scenario_set` puts
*realized* history into a single-path (`n_simulations=1`) `ScenarioSet`, so the exact same
rebalance, cashflow and fee engine answers "what would this allocation actually have done".
No calibration or simulation is involved: every sleeve's (and `inflation_factor`'s) raw
history, from `historical_data_controller.fetch_historical_data`, is resampled onto one
common calendar (`period`, default `"monthly"`) and kept only on the dates every factor has
an observation for. Each factor keeps its own native frequency (equities monthly by default,
interest rates daily, `real_estate` quarterly), so mixing in a coarse factor at a finer
`period` truncates the whole backtest to the dates the coarsest factor printed; nothing is
forward-filled or invented, so pick `period` to match the coarsest sleeve. With one path,
every cross-simulation statistic (VaR/CVaR and drawdown percentiles, `success_rate`,
`goal_probability`, `real_value` bands) collapses to one repeated number, not an error, just
not a distribution, while path-based reads such as CAGR, volatility, drawdown and the
factor exposure below stay fully meaningful. The synthetic set is labelled
`"historical:<first date>..<last date>"` instead of a real `run_id`, since nothing was
simulated or written to `runs/`. This is different from overlaying history on a simulated
fan chart as a calibration check, which involves no portfolio at all.

Factor exposure. `factor_exposure_controller.compute_portfolio_factor_exposure` regresses a
backtest's realized returns on the Fama-French factors to show its style (market, size,
value, profitability, investment Betas); see that function. It only makes sense for
realized history: a simulated scenario has no calendar to line up with a real factor history.

Why a separate package and not a `ScenarioSet` method: the engine is asset-class agnostic,
and which factor is investable or which category it belongs to are domain concepts it has
no need to know. This follows the project's one-package-per-concern pattern, like
`financescenarios.reporting`.

What it does not do: it never recalibrates or resimulates, so nothing here changes the
underlying run. Bond sleeves are priced by first-order duration at most; full curve-based
bond pricing with convexity (`financescenarios.bond_pricing`'s Nelson-Siegel curve
reconstruction, which needs `yield_curve`/`credit_term_structure` enabled) is not wired in.
Rate factors are never currency-converted, since a percentage has no currency.

Configuration. Nothing here is a `ScenariosConfig` field: a portfolio is built after the
fact from an already-written run, through these arguments of `__init__`/`compute()`:

| Key | Default | Meaning |
|:----|:--------|:--------|
| `weights` | preset | Factor name to target weight, each >= 0, summing to 1.0. |
| `initial_value` | `100.0` | The portfolio's total value at the start. |
| `rebalance_every` | `None` | Steps between rebalances; `None` is buy-and-hold. |
| `rebalance_band` | `None` | Rebalance when any weight drifts more than this from target. |
| `transaction_cost_rate` | `0.0` | Fraction of the amount traded, charged per rebalance. |
| `cashflow_rules` | `None` | Recurring contributions (positive) and withdrawals (negative). |
| `inflation_factor` | `None` | Index every cashflow to this simulated inflation factor. |
| `fee_rate` | `0.0` | Annual fee on assets, flat or per sleeve. |
| `durations` | `None` | Constant duration (years) per `interest_rates`/`credit` sleeve. |
| `config` | `None` | The run's config, for converting sleeves into the reporting currency. |
| `category_map` | `None` | Factor name to category, for a hand-built `ScenarioSet`. |

Changing any of these has no effect on the run's own simulation. Every read on top of the
result (`withdrawal_success`, `goal_probability`, `weight_drift`, `real_value`,
`risk_metrics`, `summary`, `benchmark`) is an explicit call on the computed result.

**References:**

- Perold, A.F., Sharpe, W.F. (1988). "Dynamic Strategies for Asset Allocation." Financial Analysts Journal, 44(1), 16-27. <https://doi.org/10.2469/faj.v44.n1.16>
- Redington, F.M. (1952). "Review of the Principles of Life-Office Valuations." Journal of the Institute of Actuaries, 78(3), 286-340. <https://doi.org/10.1017/S0020268100052811>
- Artzner, P., Delbaen, F., Eber, J-M., Heath, D. (1999). "Coherent Measures of Risk." Mathematical Finance, 9(3), 203-228. <https://doi.org/10.1111/1467-9965.00068>
- Fama, E.F., French, K.R. (2015). "A five-factor asset pricing model." Journal of Financial Economics, 116(1), 1-22. <https://doi.org/10.1016/j.jfineco.2014.10.010>
- Cremers, K.J.M., Petajisto, A. (2009). "How Active Is Your Fund Manager? A New Measure That Predicts Performance." Review of Financial Studies, 22(9), 3329-3365. <https://doi.org/10.1093/rfs/hhp057>

## Portfolio.from_preset

```python
Portfolio.from_preset(
    scenario_set: ScenarioSet,
    preset: str | PortfolioPreset,
    config: ScenariosConfig | None = None,
    portfolios_dir: str | Path = 'portfolios',
    category_map: dict[str, str] | None = None,
) -> 'Portfolio'
```

Build a Portfolio around one of the named allocations under `portfolios/`
(60/40, All Weather, a target-date glidepath, ...), so a caller picks a
strategy by name instead of restating weights.

In plain terms: instead of typing `{"us_broad": 0.6, "united_states_short_rate": 0.4}`,
ask for `"balanced_60_40"` and get the textbook 60/40 portfolio, with a description of
why those weights. The preset becomes the instance's default allocation, so `compute()`
needs no weights, and a glidepath preset sends itself to `compute_glidepath()`.

Fourteen presets ship with the package, one YAML file each (`name`, `description`, and
exactly one of `sleeves: [{factor_name, weight}]` or `checkpoints: [{year, weights}]`),
with the filename stem as the id: `all_weather`, `balanced_60_40`, `barbell`,
`bogleheads_three_fund`, `buffett_90_10`, `conservative_income`, `endowment_model` (with the
`private_markets` factor set), `global_60_40`,
`global_equity_growth`, `golden_butterfly`, `permanent_portfolio`, `small_cap_value_tilt`,
`target_date_glidepath` (the one glidepath) and `us_equity_sectors`. List them with
`portfolio_preset_controller.load_all("portfolios")`. Copy one into your own
`portfolios/` directory to start an allocation of your own; a local directory always
wins over the bundled copy, the same as for `settings/`, `factor-sets/` and `regimes/`.

Also known as: model portfolio, named allocation, strategic asset allocation template.

**Args:**

- <u>scenario_set (ScenarioSet):</u> the simulation to build a portfolio from.
- <u>preset (str &#124; PortfolioPreset):</u> a preset id to load from `portfolios_dir` (the ".yaml" suffix is optional), or an already-loaded `PortfolioPreset`.
- <u>config (ScenariosConfig &#124; None):</u> see `__init__`.
- <u>portfolios_dir (str &#124; Path):</u> the presets directory. Falls back to the copy bundled in the package when no such directory exists here (see `profiles_controller.resolve_directory()`), so this works from a plain `pip install` too.
- <u>category_map (dict[str, str] &#124; None):</u> see `__init__`.

**Returns:**

<u>Portfolio:</u> an instance whose `compute()` defaults to this preset's own allocation: its sleeves, or its glidepath checkpoints.

**Raises:**

- <u>FileNotFoundError:</u> if no such preset file exists.
- <u>pydantic.ValidationError:</u> if the preset file isn't a valid PortfolioPreset.

**Notes:**

- Every shipped preset names factors from the broad factor set
  (`factor-sets/broad.yaml`), such as `us_broad`, `united_states_short_rate`, `gold`
  or `europe`, the same assumption `regimes/*.yaml` makes. Against a run built from a
  different factor set, `compute()` raises the usual "not a configured factor" error for
  any sleeve the run does not have; presets do not change that error path.
- Weights are checked to sum to 1.0 when the file is loaded (per sleeve list or per
  glidepath checkpoint), with the same tolerance as `compute()`.
- `extends:` chains resolve the same way as for regimes; see
  `portfolio_preset_controller.load_one()`.

**As an example:**

```python
from financescenarios import Portfolio

# scenario_set: the 30-year yearly run built in compute()'s example
portfolio = Portfolio.from_preset(scenario_set, preset="balanced_60_40")
result = portfolio.compute(initial_value=100.0, rebalance_every=1)

portfolio                      # Portfolio(2 investable factors, preset '60/40 Balanced')
portfolio.preset.description   # why these weights
portfolio.investable_factors   # ['united_states_short_rate', 'us_broad']
```

Which returns (simulated on 2026-10-04), the portfolio value after 30 years:

| preset | 5th percentile | median | 95th percentile |
|:-------|---------------:|-------:|----------------:|
| 60/40 Balanced, rebalanced yearly | 452.42 | 1182.57 | 3180.99 |

The preset reads "The textbook mix: 60% US stocks and 40% US Treasury bonds." Rebalanced every
year, 100 grew to a median of about 1,183 over 30 years, and in 90% of the simulated scenarios to
between roughly 450 and 3,180. That run predates the bond durations: its 40% was still rolled
as cash, so the same call now gives somewhat different numbers.

## Portfolio.preset

```python
portfolio.preset  # property -> PortfolioPreset | None
```

The named allocation this instance defaults to, if built via `from_preset()`.

## Portfolio.investable_factors

```python
portfolio.investable_factors  # property -> list[str]
```

Every factor in this run a sleeve may actually name: the simulated,
priced ones (`portfolio_model.INVESTABLE_FACTOR_TYPES`), skipping the
inflation/unemployment/latent-state series that have no holding meaning.

## Portfolio.cashflow_rule

```python
cashflow_rule(
    amount: float,
    every_years: float = 1.0,
    start_year: float = 0.0,
    end_year: float | None = None,
) -> CashflowRule
```

A `CashflowRule` stated in years rather than engine steps: "contribute
1,000 a month for the first 30 years" without first working out how many
steps a month is at this run's own frequency.

In plain terms: a cashflow rule is a recurring deposit (positive amount) or withdrawal
(negative amount). This builds one from a calendar description, so the same rule keeps
meaning the same thing whether the run steps monthly, quarterly or yearly; the step
arithmetic is resolved against this run's own time grid.

A life-cycle plan is several rules, not one schedule with a sign change baked in: "save
every year for 15 years, then withdraw every year" is one positive and one negative
rule. `compute()`/`compute_glidepath()` add the rules up into one per-step schedule
(`portfolio_model.build_cashflow_schedule`). How a contribution is invested, how a
withdrawal is funded and what happens when the money runs out is described in
`compute()`.

Also known as: contribution plan, withdrawal plan, savings plan, decumulation schedule.

**Args:**

- <u>amount (float):</u> positive contributes, negative withdraws, per occurrence.
- <u>every_years (float):</u> years between occurrences (1/12 monthly, 0.25 quarterly, 1.0 yearly). Rounded to the nearest whole step, never below one step; asking for monthly cashflows on a yearly grid gives one a year, not twelve.
- <u>start_year (float):</u> the first year this rule fires, snapped to the nearest step.
- <u>end_year (float &#124; None):</u> the last year it fires, snapped to the nearest step. None (the default) runs to the end of the horizon.

**Returns:**

<u>CashflowRule:</u> with `every`/`start_step`/`end_step` resolved against this run's own time grid.

**Raises:**

- <u>ValueError:</u> if `every_years` isn't positive, or `start_year`/`end_year` falls outside the simulated horizon.

**Notes:**

- A cadence finer than the grid (monthly cashflows on a yearly run) fires once per step
  rather than silently multiplying, and the amount is not rescaled; a warning says so,
  so aggregate the amount per step yourself in that case.
- A year outside the horizon raises instead of being clamped.
- `CashflowRule(amount, every, start_step, end_step)` can also be built directly in
  engine steps; `end_step` is inclusive and `None` runs to the end of the horizon.

**As an example:**

```python
# portfolio: Portfolio(scenario_set) on the 30-year yearly run of compute()'s example
contribute = portfolio.cashflow_rule(10_000, every_years=1, end_year=14)
withdraw = portfolio.cashflow_rule(-40_000, every_years=1, start_year=15)
```

Which returns (on 2026-10-04):

| rule | amount | every | start_step | end_step |
|:-----|-------:|------:|-----------:|---------:|
| contribute | 10000.0 | 1 | 0 | 14 |
| withdraw | -40000.0 | 1 | 15 | None |

On a yearly grid one year is one step, so the saver deposits 10,000 at steps 0 to 14
and withdraws 40,000 every year from step 15 to the end of the 30-year horizon; on a
monthly grid the same call would give `every=12`. See `withdrawal_success()` for how
this plan fares.

## Portfolio.compute

```python
compute(
    weights: dict[str, float] | None = None,
    initial_value: float = 100.0,
    rebalance_every: int | None = None,
    cashflow_rules: list[CashflowRule] | None = None,
    fee_rate: float | dict[str, float] = 0.0,
    durations: dict[str, float] | None = None,
    rebalance_band: float | None = None,
    transaction_cost_rate: float = 0.0,
    inflation_factor: str | None = None,
) -> ScenarioSet
```

Build a portfolio value path from a target weight per factor: every simulated scenario
of the chosen assets is combined into the value of one portfolio, plus the value of
each sleeve.

In plain terms: give it `{"us_broad": 0.6, "united_states_short_rate": 0.4}` and 100,
and it returns 1,000 possible paths of what that 60/40 portfolio is worth each year.
Rebalancing, regular savings or withdrawals, fees and trading costs are all optional
arguments; without them the portfolio is bought once and held.

How each step is applied, in order (`portfolio_model._run_schedule`):

1. Growth: every sleeve grows with its own asset (see the class docstring for how price
   and rate factors become growth), minus the fee. An annual `fee_rate` is charged on
   the sleeve's assets every step as `exp(-fee_rate * dt)`, with `dt` that step's own
   length in years, since the time grid is not always evenly spaced.
2. Rebalance, when the calendar (`rebalance_every`) or the band (`rebalance_band`) says
   so: sleeves are reset to target weight. A `transaction_cost_rate` is then charged on
   the one-way turnover, `0.5 * sum(|target value - actual value|)` over sleeves (buying
   one sleeve and selling another is one trade, not two), and deducted from the total
   before it is split back out. Unlike the fee, it only bites when a trade happens.
3. Cashflow: a contribution buys the step's target mix; a withdrawal is taken from each
   sleeve in proportion to what it currently holds, so a drifted sleeve is never sold
   below zero. If the portfolio's value is then 0 or less it is set to exactly 0.0 and
   stays there (later growth of 0.0 is still 0.0), and a ruined portfolio receives no
   further contributions. The fee in step 1 is charged before the cashflow lands, so a
   fresh contribution is not charged that step's fee.

With `inflation_factor`, every cashflow amount is read in today's money: the schedule is
multiplied by that simulation's own cumulative inflation
(`ScenarioSet.cumulative_index(inflation_factor, initial_index=1.0)`), so a withdrawal of
40,000 grows with prices in each scenario instead of eroding. The factor need not be a
sleeve, and it is ignored when no `cashflow_rules` are given.

With `durations`, a government or corporate bond sleeve is priced as a constant-duration
bond fund (`portfolio_model.duration_growth_factor`): each step's return is
`-duration * (y(t) - y(t-1)) + y(t-1) * dt`, the price effect of the yield change plus
the interest earned, so a rate rise immediately marks the sleeve down by roughly
`duration * rise` and then earns the higher rate going forward
([Redington, 1952](https://doi.org/10.1017/S0020268100052811)). This is a rolling fund
whose duration stays constant (like a long-treasury ETF), not one bond ageing to
maturity. Without it, the default floating-rate roll compounds the rate with no price
effect at all: a rate spike only raises future growth.

With `config` given to `Portfolio(...)`, each `equities`/`commodities` sleeve, and a
`real_estate` sleeve's compounded price index, is converted from its own currency
(`EquityConfig.currency`, ...) into `config.reporting.reporting_currency` before being
weighted, so a euro equity in a dollar portfolio carries the euro/dollar return too (see
`reporting_controller.Reporting`). Rate factors are never converted. Without `config`,
every sleeve's native units are combined directly.

Also known as: portfolio simulation, asset allocation backtest, constant-mix or
buy-and-hold strategy, strategic asset allocation.

**Args:**

- <u>weights (dict[str, float] &#124; None):</u> factor name -> portfolio weight, each >= 0, summing to 1.0. Every key must be a simulated, investable factor in this run (see `portfolio_model.INVESTABLE_FACTOR_TYPES`). Defaults to this instance's own preset (see `from_preset()`); a glidepath preset is dispatched straight to `compute_glidepath()`, since "the preset's allocation" is what's being asked for either way.
- <u>initial_value (float):</u> the portfolio's total value at t=0.
- <u>rebalance_every (int &#124; None):</u> steps between rebalances back to target weight. None (the default) means buy-and-hold, no rebalancing.
- <u>cashflow_rules (list[CashflowRule] &#124; None):</u> recurring contributions (positive `amount`) and/or withdrawals (negative `amount`); see `portfolio_model.CashflowRule`/`build_cashflow_schedule`. None (the default) means no cashflows. A simulation whose value is depleted by a withdrawal is clamped to exactly 0.0 and stays there (see `portfolio_model._apply_cashflow_and_ruin`).
- <u>fee_rate (float &#124; dict[str, float]):</u> an annualized expense-ratio drag charged against every sleeve's own growth (see `portfolio_model.compute_portfolio_paths`'s own `fee_rate`). A flat `float` (the default, 0.0) applies to every sleeve; a `dict[str, float]` sets a per-sleeve rate, defaulting to 0.0 for any sleeve not named.
- <u>durations (dict[str, float] &#124; None):</u> factor name -> constant duration (years), for interest_rates/credit sleeves only; prices that sleeve as a constant-duration bond total-return index instead of the default floating-rate-note roll (see `portfolio_model.duration_growth_factor`). None (the default) keeps every sleeve's existing pricing.
- <u>rebalance_band (float &#124; None):</u> an additional, tolerance-based rebalance trigger alongside `rebalance_every`; see `portfolio_model.compute_portfolio_paths`'s own `rebalance_band`. None (the default) means no band.
- <u>transaction_cost_rate (float):</u> a one-way turnover cost charged whenever a rebalance fires; see `portfolio_model.compute_portfolio_paths`'s own `transaction_cost_rate`. 0.0 (the default) means no cost.
- <u>inflation_factor (str &#124; None):</u> a simulated factor (need not be an investable sleeve) whose own path scales every `CashflowRule.amount` into a per-simulation, inflation-indexed schedule; see `_resolve_cashflow_schedule`. None (the default) keeps every cashflow at its stated nominal amount, the pre-existing behavior.

**Returns:**

<u>ScenarioSet:</u> a new `ScenarioSet` (same dates/time_grid/n_simulations/ seed as the source) whose `paths` holds `"portfolio"` (the summed value path) plus `"<factor_name>_value"` for every sleeve, so a portfolio reads through the same `ScenarioSet` machinery as any other simulated factor.

**Raises:**

- <u>ValueError:</u> if `weights` is omitted and this instance has no preset, a weight's factor isn't in `category_map`, names a non-investable category (e.g. `"inflation"`), a weight is negative, the weights don't sum to ~1.0, `rebalance_every` is not None and < 1, a cashflow rule's start_step/end_step falls outside the run's horizon, `fee_rate` is a dict naming a factor not in `weights`, `rebalance_band` is not None and <= 0, or `transaction_cost_rate` is negative.
- <u>KeyError:</u> if a factor name isn't present in `scenario_set.paths` (including `inflation_factor`, if given).

**Notes:**

- `durations` is only valid on `interest_rates`/`credit` sleeves; naming any other
  sleeve raises. The duration index compounds the simple per-step return as if it were
  a log return, which understates a very large one-step loss (a 2-point spike at
  duration 17 gives exp(-0.32) = 0.73 instead of 0.68), and convexity is ignored.
- A cashflow amount scaled by `inflation_factor` turns the schedule into one per
  simulation, since every simulated inflation path differs; the ruin handling above is
  unchanged. An inflation factor averaging above 50% a year is warned about, since it
  most likely holds percentage points rather than decimals.
- `fee_rate` as a dict sets a rate per sleeve; a sleeve not named pays 0.0.
- A glidepath preset given through `from_preset()` is dispatched to
  `compute_glidepath()`, with `rebalance_every` defaulting to 1.

**As an example:**

```python
from datetime import date

from financescenarios import Portfolio, Scenarios
from financescenarios.config.config_model import (
    EngineConfig,
    EquityConfig,
    InflationConfig,
    InterestRateConfig,
    ScenariosConfig,
    ToolkitConfig,
)

config = ScenariosConfig(
    start_date=date(2026, 10, 1),
    engine=EngineConfig(n_simulations=1000, n_steps=30, frequency="yearly", seed=42),
    toolkit=ToolkitConfig(start_date=date(2000, 1, 1)),
    interest_rates=[
        InterestRateConfig(name="united_states_short_rate", country="United States", currency="USD")
    ],
    inflation=[InflationConfig(name="inflation", country="United States", currency="USD")],
    equities=[EquityConfig(name="us_broad", ticker="SPY", currency="USD")],
)
scenario_set = Scenarios.from_config(config).simulate()

portfolio = Portfolio(scenario_set)
weights = {"us_broad": 0.6, "united_states_short_rate": 0.4}
buy_and_hold = portfolio.compute(weights, initial_value=100.0)
rebalanced = portfolio.compute(weights, initial_value=100.0, rebalance_every=1, fee_rate=0.002)
```

Which returns (simulated on 2026-10-04), the `"portfolio"` path's 5th, 50th and 95th
percentile across the 1,000 simulations:

| year | buy-and-hold, 5% | median | 95% | rebalanced yearly, 0.2% fee, 5% | median | 95% |
|-----:|-----------------:|-------:|----:|--------------------------------:|-------:|----:|
| 0 | 100.00 | 100.00 | 100.00 | 100.00 | 100.00 | 100.00 |
| 1 | 89.63 | 110.75 | 122.86 | 89.45 | 110.53 | 122.62 |
| 5 | 100.75 | 149.65 | 222.58 | 100.78 | 148.60 | 208.82 |
| 10 | 124.83 | 229.29 | 445.23 | 125.53 | 222.61 | 376.17 |
| 20 | 219.56 | 560.95 | 1705.53 | 221.15 | 491.83 | 1068.01 |
| 30 | 425.73 | 1432.81 | 5924.76 | 426.07 | 1113.70 | 2995.75 |

Both portfolios start at 100 and have almost the same bad outcomes (about 426 after 30
years at the 5th percentile). Left alone, the buy-and-hold portfolio drifts toward
equities as they outgrow bonds, so its good outcomes are far better (5,925 versus 2,996
at the 95th percentile) at the cost of more risk; the rebalanced one stays 60/40.
`result.paths` also holds `"us_broad_value"` and `"united_states_short_rate_value"`.

Pricing a 100% bond portfolio with `durations={"united_states_short_rate": 7.0}`
instead of the default floating-rate roll, on the same run:

| year | floating-rate roll, 5% | median | 95% | duration 7, 5% | median | 95% |
|-----:|-----------------------:|-------:|----:|---------------:|-------:|----:|
| 1 | 104.07 | 104.07 | 104.07 | 96.32 | 103.73 | 111.72 |
| 2 | 107.22 | 108.36 | 109.52 | 97.71 | 107.36 | 118.66 |
| 10 | 127.61 | 152.29 | 180.26 | 129.23 | 147.34 | 167.88 |
| 30 | 181.32 | 381.87 | 802.99 | 205.27 | 365.91 | 643.58 |

The floating-rate roll earns today's 4.0% rate in year one whatever happens, while the
duration-7 fund can lose almost 4% or gain almost 12% in that year as rates move; its
median worst drawdown is 7.0%, against none for the floating-rate roll.

**References:**

- Perold, A.F., Sharpe, W.F. (1988). "Dynamic Strategies for Asset Allocation." Financial Analysts Journal, 44(1), 16-27. <https://doi.org/10.2469/faj.v44.n1.16>
- Redington, F.M. (1952). "Review of the Principles of Life-Office Valuations." Journal of the Institute of Actuaries, 78(3), 286-340. <https://doi.org/10.1017/S0020268100052811>

## Portfolio.compute_glidepath

```python
compute_glidepath(
    checkpoints: list[GlidepathCheckpoint] | None = None,
    initial_value: float = 100.0,
    rebalance_every: int = 1,
    cashflow_rules: list[CashflowRule] | None = None,
    fee_rate: float | dict[str, float] = 0.0,
    durations: dict[str, float] | None = None,
    rebalance_band: float | None = None,
    transaction_cost_rate: float = 0.0,
    inflation_factor: str | None = None,
) -> ScenarioSet
```

Build a glidepath portfolio value path: a target weight per factor
that changes over the horizon (the lifecycle/target-date-fund pattern),
interpolated from `checkpoints`.

In plain terms: a target-date fund starts aggressive, mostly equities, while the target
date is far away, and glides toward conservative, mostly bonds, as it approaches. Give
the weights at a few years (`GlidepathCheckpoint(year, weights)`, each summing to 1.0)
and the target at every step in between is filled in on a straight line.

Between two checkpoints the weights are interpolated linearly, and they stay flat at the
first checkpoint's weights before it and at the last one's after it
(`portfolio_model.resolve_glidepath_weights`, the same `np.interp` convention a
`BeliefPath`'s year anchors use, applied to a whole set of weights per year). Everything
else (rebalancing, cashflows, fees, costs, durations) works exactly as in `compute()`,
through the same step loop; a glidepath is simply a portfolio whose target differs by
step. The one difference: `rebalance_every` cannot be `None` (buy-and-hold), since a
portfolio that is never rebalanced would ignore the glidepath after the first step.

Also known as: lifecycle fund, target-date fund, de-risking path.

**Args:**

- <u>checkpoints (list[portfolio_model.GlidepathCheckpoint] &#124; None):</u> the glidepath's waypoints; every checkpoint must name the same set of factors, each a simulated, investable factor in this run. Defaults to this instance's own glidepath preset, if it has one (see `from_preset()`).
- <u>initial_value (float):</u> the portfolio's total value at t=0.
- <u>rebalance_every (int):</u> steps between rebalances to the glidepath's current target weight. Must be >= 1; there is no "buy and hold" reading of a moving target.
- <u>cashflow_rules (list[CashflowRule] &#124; None):</u> same as `compute()`'s own `cashflow_rules`.
- <u>fee_rate (float &#124; dict[str, float]):</u> same as `compute()`'s own `fee_rate`.
- <u>durations (dict[str, float] &#124; None):</u> same as `compute()`'s own `durations`.
- <u>rebalance_band (float &#124; None):</u> same as `compute()`'s own `rebalance_band`.
- <u>transaction_cost_rate (float):</u> same as `compute()`'s own `transaction_cost_rate`.
- <u>inflation_factor (str &#124; None):</u> same as `compute()`'s own `inflation_factor`.

**Returns:**

<u>ScenarioSet:</u> same shape as `compute()`'s return value.

**Raises:**

- <u>ValueError:</u> if `checkpoints` is omitted and this instance has no glidepath preset, `checkpoints` is empty, don't all name the same factors, name a factor that isn't in `category_map` or isn't an investable category, `rebalance_every` < 1, a cashflow rule's start_step/end_step falls outside the run's horizon, `fee_rate` is a dict naming a factor not in `checkpoints`, `rebalance_band` is not None and <= 0, or `transaction_cost_rate` is negative.
- <u>KeyError:</u> if a factor name isn't present in `scenario_set.paths` (including `inflation_factor`, if given).

**Notes:**

- Every checkpoint must name exactly the same factors, otherwise a factor would have no
  weight somewhere along the way.
- With the default `rebalance_every=1` the portfolio is reset to the moving target every
  step; a `rebalance_band` only matters with a coarser calendar.

**As an example:**

```python
from financescenarios import GlidepathCheckpoint

# portfolio: Portfolio(scenario_set) on the 30-year yearly run of compute()'s example
checkpoints = [
    GlidepathCheckpoint(year=0, weights={"us_broad": 0.9, "united_states_short_rate": 0.1}),
    GlidepathCheckpoint(year=30, weights={"us_broad": 0.3, "united_states_short_rate": 0.7}),
]
result = portfolio.compute_glidepath(checkpoints, initial_value=100.0, rebalance_every=1)
equity_weight = result.paths["us_broad_value"] / result.paths["portfolio"]
```

Which returns (simulated on 2026-10-04):

| year | mean equity weight |
|-----:|-------------------:|
| 0 | 0.90 |
| 10 | 0.70 |
| 20 | 0.50 |
| 30 | 0.30 |

The equity share glides from 90% to 30% in a straight line, 2 points a year. After 30
years the portfolio is worth 1,210 at the median (409.66 at the 5th and 3,373.56 at the
95th percentile), close to the 60/40 portfolio's 1,183 but with more of the risk taken
early. `Portfolio.from_preset(scenario_set, preset="target_date_glidepath").compute()` gives
exactly the same result.

## Portfolio.withdrawal_success

```python
withdrawal_success(portfolio_scenario_set: ScenarioSet | None = None) -> WithdrawalSuccessMetrics
```

Success-probability summary for a decumulation run: how often the
portfolio lasts the full horizon, when it typically runs out
otherwise, and what survivors end up with.

In plain terms: "will my retirement savings last?". For a portfolio with withdrawals,
this counts the simulated scenarios in which money is still left at the end, says in which
year the money typically runs out in the others, and shows how much is left in the ones
that make it.

The three fields of the result:

- `success_rate`: the share of simulations whose final value is above 0. Because a
  depleted portfolio is clamped to exactly 0.0 and stays there, the final step alone
  tells whether a simulation ever ran out.
- `median_depletion_year`: among the simulations that ran out, the median year in which
  each first hit 0.0; `None` if none did.
- `terminal_value_percentiles`: the 5th/25th/50th/75th/95th percentile of the final value
  over the *surviving* simulations only, so it reads as "how much do survivors end up
  with" rather than being pulled down by the failures, which `success_rate` already
  counts. Empty if none survived.

Also known as: retirement success rate, probability of ruin (its complement), safe
withdrawal analysis, sustainable spending test.

**Args:**

- <u>portfolio_scenario_set (ScenarioSet):</u> a `compute()`/ `compute_glidepath()` result; its `"portfolio"` path is what's summarized.

**Returns:**

<u>WithdrawalSuccessMetrics:</u> see `portfolio_model.WithdrawalSuccessMetrics`.

**Notes:**

- Works on any computed portfolio: without withdrawals nothing depletes and
  `success_rate` is 1.0.
- On a single-path historical backtest the result is a single yes or no, not a rate.

**As an example:**

```python
# portfolio: Portfolio(scenario_set) on the 30-year yearly run of compute()'s example
weights = {"us_broad": 0.6, "united_states_short_rate": 0.4}
rules = [
    portfolio.cashflow_rule(10_000, every_years=1, end_year=14),
    portfolio.cashflow_rule(-40_000, every_years=1, start_year=15),
]
indexed = portfolio.compute(
    weights, initial_value=100_000.0, rebalance_every=1, cashflow_rules=rules, inflation_factor="inflation"
)
nominal = portfolio.compute(weights, initial_value=100_000.0, rebalance_every=1, cashflow_rules=rules)

portfolio.withdrawal_success(indexed)
portfolio.withdrawal_success(nominal)
```

Which returns (simulated on 2026-10-04):

| cashflows | success_rate | median_depletion_year | survivors 5% | survivors median | survivors 95% |
|:----------|-------------:|----------------------:|-------------:|-----------------:|--------------:|
| inflation-indexed | 0.580 | 26.0 | 80,313 | 858,137 | 3,887,958 |
| fixed nominal | 0.917 | 27.0 | 141,623 | 1,055,481 | 4,114,358 |

Saving 10,000 a year for 15 years on top of 100,000, then spending 40,000 a year, the
money lasts the full 30 years in 91.7% of the scenarios when the 40,000 is a fixed amount,
but only in 58% when it rises with inflation to keep its purchasing power. When the
money runs out, it typically does so around year 26.

## Portfolio.goal_probability

```python
goal_probability(
    portfolio_scenario_set: ScenarioSet,
    target_value: float,
    target_year: float | None = None,
) -> GoalProbability
```

Probability this portfolio reaches `target_value`, either by
`target_year` or, if omitted, at any point across the whole horizon.

In plain terms: "what are the chances I reach one million?". The saving-side
counterpart of `withdrawal_success()`, read straight off the computed portfolio paths.

The two fields of the result:

- `probability`: with `target_year`, the share of simulations whose value at the step
  nearest that year is at least `target_value`; without it (the default), the share that
  reach it at *any* point in the horizon, the "will I ever hit my number" question.
- `median_year_reached`: among the simulations that reach the target, the median year in
  which each first does. Only meaningful without `target_year` (with it, every success is
  measured at the same step), so it is `None` then, and also when nobody reaches it.

Also known as: goal-based planning probability, probability of reaching a target,
shortfall probability (its complement).

**Args:**

- <u>portfolio_scenario_set (ScenarioSet):</u> a `compute()`/ `compute_glidepath()` result; its `"portfolio"` path is what's checked.
- <u>target_value (float):</u> the dollar value to check against.
- <u>target_year (float &#124; None):</u> the year to evaluate at, snapped to the nearest simulated step. None (the default) checks every step across the horizon instead of just one.

**Returns:**

<u>GoalProbability:</u> see `portfolio_model.GoalProbability`.

**Notes:**

- The value is nominal; use `real_value()` to ask the same question in today's money.
- The "first step a condition holds" search is shared with depletion detection
  (`portfolio_model._first_step_reaching`), vectorized across all simulations.

**As an example:**

```python
# portfolio: Portfolio(scenario_set) on the 30-year yearly run of compute()'s example
saver = portfolio.compute(
    {"us_broad": 0.6, "united_states_short_rate": 0.4},
    initial_value=100_000.0,
    rebalance_every=1,
    cashflow_rules=[portfolio.cashflow_rule(10_000, every_years=1)],
)
portfolio.goal_probability(saver, target_value=1_000_000.0)
portfolio.goal_probability(saver, target_value=1_000_000.0, target_year=20)
```

Which returns (simulated on 2026-10-04):

| target_year | probability | median_year_reached |
|:------------|------------:|--------------------:|
| None (any time in 30 years) | 0.977 | 20.0 |
| 20 | 0.577 | None |

Starting with 100,000 and saving 10,000 every year in a rebalanced 60/40 portfolio, the
portfolio passes one million at some point in 97.7% of the scenarios, typically after 20
years; it is above one million in year 20 itself in 57.7% of them.

## Portfolio.factor_exposure

```python
factor_exposure(
    portfolio_scenario_set: ScenarioSet | None = None,
    model: Literal['three_factor', 'five_factor'] = 'five_factor',
) -> pl.DataFrame
```

What this portfolio actually behaved like over history: its loading (Beta) on each of Ken French's
Fama-French factors, regressed on its own historical returns (see `compute_portfolio_factor_exposure`).

In plain terms: a market Beta of 0.66 means the portfolio moved about 0.66% for every 1% the stock market
moved; the others show a tilt toward small (SMB), cheap (HML), profitable (RMW) or conservative (CMA)
companies. R-squared says how much of its ups and downs these factors explain.

**Args:**

- <u>portfolio_scenario_set (ScenarioSet &#124; None):</u> a `compute()` result on history; None computes this Portfolio's own allocation first.
- <u>model (str):</u> "five_factor" (Fama and French 2015, the default) or "three_factor" (Fama and French 1993).

**Returns:**

<u>pl.DataFrame:</u> one row: 'portfolio', one column per factor, 'alpha' (the return no factor explains, per period), 'r_squared', 'observations' and the 'from'/'to' dates.

**Raises:**

- <u>ValueError:</u> if the run is simulated scenarios rather than history (more than one path).

**As an example:**

```python
history = scenarios.history(portfolio="balanced_60_40")
Portfolio.from_preset(history, preset="balanced_60_40").factor_exposure()
```

## Portfolio.risk_metrics

```python
risk_metrics(portfolio_scenario_set: ScenarioSet | None = None) -> PortfolioRiskMetrics
```

Distributional risk summary (drawdown, VaR/CVaR, volatility) for this
portfolio; unlike `withdrawal_success`/`goal_probability`, applies
to any computed portfolio, cashflows or not.

In plain terms: how bumpy is the ride and how bad can it get? It reports the deepest fall
from a previous high in each scenario, the loss in the worst 5% of scenarios, how much the
value swings per year, the yearly return to plan around, and the chance of ending with
less than you started with. Everything is counted over the simulated paths themselves,
not from a formula that assumes returns follow a particular distribution.

The fields of the result:

- `max_drawdown_percentiles`: the 5th/25th/50th/75th/95th percentile, across simulations,
  of each simulation's worst peak-to-trough fall (`value / running maximum - 1`, its
  minimum), a negative fraction; 0.0 means it never fell.
- `value_at_risk_95`: the total-return loss over the whole horizon that 95% of
  simulations do not exceed, the negative of the 5th percentile of
  `final / initial - 1`. A negative number means even the worst 5% gained.
- `conditional_value_at_risk_95`: the average loss in the worst 5% of simulations (the
  expected shortfall), always at least the VaR, since it averages over the tail rather
  than taking its edge ([Artzner et al., 1999](https://doi.org/10.1111/1467-9965.00068)).
- `annualized_volatility`: the standard deviation of simple per-step returns, pooled over
  every simulation and step and annualized by the average step length; one figure for the
  whole horizon, not a term structure. Steps after a ruin (value 0) are left out.
- `cagr_percentiles`: percentiles of each simulation's compound annual growth rate,
  `(final / initial) ** (1 / years) - 1`, the "what return should I plan around" read; a
  simulation ending at or below zero counts as -1.0.
- `probability_of_loss`: the share of simulations ending below their starting value, in
  nominal terms.

Also known as: Value at Risk, Expected Shortfall, tail risk, maximum drawdown, CAGR
distribution.

**Args:**

- <u>portfolio_scenario_set (ScenarioSet):</u> a `compute()`/ `compute_glidepath()` result; its `"portfolio"` path is what's summarized.

**Returns:**

<u>PortfolioRiskMetrics:</u> see `portfolio_model.PortfolioRiskMetrics`.

**Notes:**

- VaR, CVaR and the loss probability are measured on the total return over the whole
  horizon, so on a long run they describe a 30-year outcome, not a one-year loss.
- Cashflows move the value too, so on a saving or spending plan these figures mix
  returns with deposits and withdrawals.
- On a single-path backtest every percentile is the same number.

**As an example:**

```python
# buy_and_hold, rebalanced: the two portfolios of compute()'s example
portfolio.risk_metrics(buy_and_hold)
portfolio.risk_metrics(rebalanced)
```

Which returns (simulated on 2026-10-04):

| metric | buy-and-hold | rebalanced yearly, 0.2% fee |
|:-------|-------------:|----------------------------:|
| max drawdown, median | -23.84% | -17.25% |
| max drawdown, 5th percentile | -40.96% | -31.33% |
| value_at_risk_95 | -3.2573 | -3.2607 |
| conditional_value_at_risk_95 | -2.1460 | -2.1947 |
| annualized_volatility | 13.21% | 10.45% |
| CAGR, median | 9.28% | 8.37% |
| CAGR, 5th percentile | 4.95% | 4.95% |
| probability_of_loss | 0.0 | 0.0 |

Over 30 years neither portfolio loses money in any simulation: 95% of them end at least
4.26 times higher (a VaR of -3.26 is a gain of 326%). The difference is the ride:
rebalancing back to 60/40 cuts the median worst fall from 24% to 17% and the yearly
swings from 13.2% to 10.4%, in exchange for a lower median growth rate (8.4% against
9.3%) as the buy-and-hold portfolio drifts into equities.

**References:**

- Artzner, P., Delbaen, F., Eber, J-M., Heath, D. (1999). "Coherent Measures of Risk." Mathematical Finance, 9(3), 203-228. <https://doi.org/10.1111/1467-9965.00068>
- Acerbi, C., Tasche, D. (2002). "On the coherence of expected shortfall." Journal of Banking & Finance, 26(7), 1487-1503. <https://doi.org/10.1016/S0378-4266(02>)00283-2

## Portfolio.real_value

```python
real_value(
    portfolio_scenario_set: ScenarioSet,
    inflation_factor: str,
    year: float,
) -> RealValueSummary
```

This portfolio's inflation-adjusted (real, today's-dollars) value at
`year`: deflates the already-computed nominal `"portfolio"` path by
`inflation_factor`'s own simulated path, per simulation. The mirror
image of `compute()`'s own `inflation_factor` (which inflates
cashflows going in); this reads what a nominal value coming out is
actually worth.

In plain terms: one million in 20 years is not one million of today's money. This divides
each simulated portfolio value by that same simulation's cumulative inflation,
`real_value(t) = nominal_value(t) / inflation_index(t)`, with the index from
`ScenarioSet.cumulative_index(inflation_factor, initial_index=1.0)`, so the answer is in
today's purchasing power. Both the portfolio and the inflation path differ per
simulation, so the result is a distribution, not one number.

The fields of the result: `year`, the simulated year actually used after snapping to the
nearest step (the same convention as `goal_probability()`'s `target_year`), and `mean` and
`percentiles` (5th/25th/50th/75th/95th) of the real value across simulations.

Also known as: inflation-adjusted value, real wealth, purchasing-power value, deflated
value.

**Args:**

- <u>portfolio_scenario_set (ScenarioSet):</u> a `compute()`/ `compute_glidepath()` result; its `"portfolio"` path is what's deflated.
- <u>inflation_factor (str):</u> a simulated factor in this run (need not be an investable sleeve) whose own path deflates the nominal value, read directly off this `Portfolio`'s own source `ScenarioSet`, the same way `compute()`'s `inflation_factor` is.
- <u>year (float):</u> the year to evaluate at, snapped to the nearest simulated step.

**Returns:**

<u>RealValueSummary:</u> see `portfolio_model.RealValueSummary`.

**Raises:**

- <u>KeyError:</u> if inflation_factor is not a key in scenario_set.paths.

**Notes:**

- The inflation factor is read as an annualized decimal rate (0.024 for 2.4%); a series
  averaging above 50% a year is warned about as a likely percentage-point mistake, but
  never rescaled, since real hyperinflation looks the same.
- It is an optional read on the result, never computed as part of `compute()`.

**As an example:**

```python
# saver: the portfolio of goal_probability()'s example
portfolio.real_value(saver, inflation_factor="inflation", year=20)
```

Which returns (simulated on 2026-10-04):

| year | mean | 5% | 25% | median | 75% | 95% |
|-----:|-----:|---:|----:|-------:|----:|----:|
| 20.0 | 694,005 | 306,366 | 464,152 | 636,645 | 841,980 | 1,357,857 |

In nominal terms the saver's median portfolio is worth 1,064,686 after 20 years; in
today's money that median is 636,645, so inflation takes away about 40% of the
purchasing power over those 20 years.

## Portfolio.weight_drift

```python
weight_drift(portfolio_scenario_set: ScenarioSet | None = None) -> dict[str, np.ndarray]
```

Actual minus target weight, per sleeve, at every step, for the most
recent `compute()`/`compute_glidepath()` call on this `Portfolio`
instance; see `portfolio_model.compute_weight_drift`. `portfolio_scenario_set`
must be that call's own return value (its `"<factor>_value"` paths are
read back directly); this method doesn't re-derive the target weight
from scratch, it reuses whichever allocation this instance last
computed against.

In plain terms: a 60/40 portfolio is only exactly 60/40 right after it is rebalanced. In
between, and forever in a buy-and-hold portfolio, the weights wander as one asset outgrows
the other. This shows by how much, per sleeve, per simulation and per step: +0.10 means
the sleeve is 10 points above its target.

The target is whatever the last `compute()`/`compute_glidepath()` call on this instance
used (a fixed weight, or the glidepath's weight at each step), kept on the instance, so no
allocation is passed here. Where the portfolio is worth nothing (a ruined simulation) the
drift is 0.0, since a weight means nothing for an empty portfolio.

Also known as: allocation drift, weight deviation, tracking to target.

**Args:**

- <u>portfolio_scenario_set (ScenarioSet):</u> a `compute()`/ `compute_glidepath()` result from this same `Portfolio` instance.

**Returns:**

<u>dict[str, np.ndarray]:</u> factor name -> shape (n_simulations, n_steps + 1), `actual_weight - target_weight` at every step.

**Raises:**

- <u>RuntimeError:</u> if `compute()`/`compute_glidepath()` hasn't been called yet on this instance.

**Notes:**

- The result is the raw arrays; summarize them yourself (a mean or percentile per step
  with numpy). It deliberately does not go through `metrics_controller.compute_factor_metrics`,
  which `"portfolio"` and the sleeves can use: those Finance Toolkit metrics (drawdown, Sharpe)
  assume a positive price series and are meaningless, or fail, on a signed weight gap.
- Pass the result of the *latest* compute call on the same instance; an older result
  would be compared against the wrong target.

**As an example:**

```python
# portfolio: Portfolio(scenario_set) on the 30-year yearly run of compute()'s example
result = portfolio.compute({"us_broad": 0.6, "united_states_short_rate": 0.4})
drift = portfolio.weight_drift(result)["us_broad"]
```

Which returns (simulated on 2026-10-04), the equity sleeve's drift for buy-and-hold:

| year | mean | 5% | median | 95% |
|-----:|-----:|---:|-------:|----:|
| 0 | 0.0000 | 0.00 | 0.00 | 0.00 |
| 1 | 0.0154 | -0.06 | 0.02 | 0.06 |
| 5 | 0.0627 | -0.09 | 0.07 | 0.18 |
| 10 | 0.1188 | -0.09 | 0.14 | 0.26 |
| 20 | 0.1981 | -0.03 | 0.23 | 0.34 |
| 30 | 0.2551 | -0.01 | 0.29 | 0.38 |

Left alone, the 60% equity sleeve is typically 89% of the portfolio after 30 years
(60% + 29 points). With `rebalance_every=1` the drift is 0 at every yearly step, and
with `rebalance_band=0.05` it never exceeds 5 points.

## Portfolio.summary

```python
summary(
    portfolio_scenario_set: ScenarioSet | None = None,
    goal_value: float | None = None,
    goal_year: float | None = None,
    inflation_factor: str | None = None,
    real_value_year: float | None = None,
) -> PortfolioSummary
```

Every distributional read of a computed portfolio in one call: risk and
depletion always, plus the goal probability and the real (inflation-adjusted)
value when a target for each is given. The "how did this allocation do"
counterpart to `compute()`, so a caller doesn't have to know which of
`risk_metrics`/`withdrawal_success`/`goal_probability`/`real_value` to reach
for first; each remains available on its own.

In plain terms: one call for the full report card of a portfolio. Risk
(`risk_metrics()`) and depletion (`withdrawal_success()`) are always filled in; the goal
probability needs a `goal_value` and the real value needs both an `inflation_factor` and a
`real_value_year`, since the portfolio cannot guess those targets, and they are `None`
otherwise.

Also known as: portfolio report, outcome summary.

**Args:**

- <u>portfolio_scenario_set (ScenarioSet):</u> a `compute()`/`compute_glidepath()` result; its `"portfolio"` path is what's summarized.
- <u>goal_value (float &#124; None):</u> a target dollar value; without it, `goal_probability` is left None.
- <u>goal_year (float &#124; None):</u> the year to check `goal_value` at, snapped to the nearest simulated step. None checks the whole horizon.
- <u>inflation_factor (str &#124; None):</u> a simulated factor to deflate by; without it (or without `real_value_year`), `real_value` is left None.
- <u>real_value_year (float &#124; None):</u> the year to report real value at, snapped to the nearest simulated step.

**Returns:**

<u>PortfolioSummary:</u> see `portfolio_model.PortfolioSummary`.

**Raises:**

- <u>KeyError:</u> if `inflation_factor` isn't a factor in this run.

**As an example:**

```python
# saver: the portfolio of goal_probability()'s example
summary = portfolio.summary(saver, goal_value=1_000_000.0, inflation_factor="inflation", real_value_year=20)
```

Which returns (simulated on 2026-10-04):

| field | value |
|:------|------:|
| risk.max_drawdown_percentiles["50"] | -13.74% |
| risk.cagr_percentiles["50"] | 11.11% |
| withdrawal_success.success_rate | 1.0 |
| goal_probability.probability | 0.977 |
| goal_probability.median_year_reached | 20.0 |
| real_value.percentiles["50"] | 636,645 |

The saver never withdraws, so every simulation "succeeds"; the goal and real-value
figures are the same as those of `goal_probability()` and `real_value()`. The median
growth rate of 11.1% is higher than the 8.4% of the rebalanced portfolio in
`risk_metrics()`'s example, because the yearly deposits count as growth of the value.

## Portfolio.benchmark

```python
benchmark(
    portfolio_scenario_set: ScenarioSet,
    benchmark_scenario_set: ScenarioSet,
    weights: dict[str, float] | None = None,
    benchmark_weights: dict[str, float] | None = None,
) -> RelativeMetrics
```

Compare one computed portfolio against another: tracking error,
correlation, Beta, and relative CAGR/Sharpe, plus active share when both
allocations are given. Both sides are read as their cross-simulation mean
value path (the same series a fan chart's centre line draws), so this works
for a simulated run and a single-path historical backtest alike.

"Benchmark" here just means the portfolio being compared against: a
market-index sleeve, a different allocation over the same run, or the same
allocation over a different one; nothing about it is privileged.

In plain terms: how does my portfolio compare with the alternative? Tracking error is how
much the two drift apart per year; correlation and Beta say how much mine moves with
the other (a Beta of 0.6 means it moves 0.6% for every 1% of the benchmark); relative CAGR
and relative Sharpe ratio say by how much mine grew faster per year and earned more
return per unit of risk ([Sharpe, 1966](https://doi.org/10.1086/294846)), positive meaning
mine is ahead; and active share is how much of the allocation differs.

How each is computed (`benchmark_model.compute_relative_metrics`, pure NumPy, no new
data): over the dates both portfolios share, the period-to-period returns of each give
tracking error (the standard deviation of the return difference, annualized by the
shared dates' average spacing), correlation and Beta (covariance over benchmark
variance); relative CAGR and Sharpe are this portfolio's figure minus the benchmark's.
Active share is a separate, point-in-time read of the allocations, half the sum of the
absolute weight differences per factor
([Cremers and Petajisto, 2009](https://doi.org/10.1093/rfs/hhp057)).

Each portfolio keeps its own dates and the comparison runs over their intersection. Two
portfolios on the same simulated run share every date, but two backtests can differ: a
sleeve with less history truncates its own portfolio's window. Comparing "60/40
Balanced" (from 2000-01) with "Global 60/40" (from 2005-03, its European and emerging
sleeves have less history) is a real case that an earlier exact-date requirement failed.

Also known as: relative performance, active risk, tracking error analysis, benchmark
comparison.

**Args:**

- <u>portfolio_scenario_set (ScenarioSet):</u> this portfolio's own `compute()`/`compute_glidepath()` result.
- <u>benchmark_scenario_set (ScenarioSet):</u> the reference portfolio's result.
- <u>weights (dict[str, float] &#124; None):</u> this portfolio's target weights, for active share. Defaults to the preset's own weights when this instance was built from a static preset.
- <u>benchmark_weights (dict[str, float] &#124; None):</u> the reference's target weights. Active share is None unless both are available.

**Returns:**

<u>RelativeMetrics:</u> see `benchmark_model.RelativeMetrics`.

**Raises:**

- <u>ValueError:</u> if the two share fewer than 2 dates.

**Notes:**

- On a simulated run both sides are reduced to their *mean* path across simulations,
  which averages away most of the year-to-year noise; tracking error and the Sharpe
  difference then describe the two average paths, not the risk inside any one scenario.
  On a single-path historical backtest they mean what they usually mean.
- Active share is `None` unless both allocations are known; this portfolio's own weights
  default to its static preset's weights.

**As an example:**

```python
from datetime import date

from financescenarios import Portfolio
from financescenarios.config.config_model import EquityConfig, InterestRateConfig, ScenariosConfig, ToolkitConfig
from financescenarios.historical_data.backtest_model import build_synthetic_scenario_set
from financescenarios.historical_data.historical_data_controller import fetch_historical_data
from financescenarios.scenarios_controller import build_toolkit

config = ScenariosConfig(
    start_date=date(2000, 1, 1),
    toolkit=ToolkitConfig(start_date=date(2000, 1, 1)),
    interest_rates=[
        InterestRateConfig(name="united_states_short_rate", country="United States", currency="USD")
    ],
    equities=[EquityConfig(name="us_broad", ticker="SPY", currency="USD")],
)
history = fetch_historical_data(config, build_toolkit(config))
backtest = build_synthetic_scenario_set(history, ["us_broad", "united_states_short_rate"], period="monthly")

portfolio = Portfolio.from_preset(backtest, preset="balanced_60_40")
balanced = portfolio.compute(initial_value=100.0, rebalance_every=12)
spy_only = Portfolio(backtest).compute({"us_broad": 1.0}, initial_value=100.0)
relative = portfolio.benchmark(balanced, spy_only, benchmark_weights={"us_broad": 1.0})
```

Which returns (backtested on 2026-10-04, 274 monthly dates from 2004-01-01 to
2026-10-01):

| tracking_error | correlation | beta | relative_cagr | relative_sharpe_ratio | active_share |
|---------------:|------------:|-----:|--------------:|----------------------:|-------------:|
| 5.91% | 0.9986 | 0.5942 | -3.27% | 0.1023 | 0.40 |

The 60/40 portfolio, rebalanced every 12 months, moves almost in lockstep with SPY
(correlation 0.999) but with only 59% of its swings. It grew 3.3 points a year slower
(100 became 519 against SPY's 1,027) yet earned slightly more return per unit of risk,
and 40% of its allocation differs from SPY's.

**References:**

- Sharpe, W.F. (1966). "Mutual Fund Performance." The Journal of Business, 39(S1), 119-138. <https://doi.org/10.1086/294846>
- Cremers, K.J.M., Petajisto, A. (2009). "How Active Is Your Fund Manager? A New Measure That Predicts Performance." Review of Financial Studies, 22(9), 3329-3365. <https://doi.org/10.1093/rfs/hhp057>

## CashflowRule

```python
class CashflowRule(BaseModel):
    amount: float = Field(description='Positive = contribution/inflow, negative = withdrawal/outflow, per occurrence.')
    every: int = Field(ge=1, description='Steps between occurrences.')
    start_step: int = Field(default=0, ge=0)
    end_step: int | None = Field(default=None, ge=0, description='Inclusive. None = through the end of the horizon.')
```

One recurring contribution (`amount` > 0) or withdrawal (`amount` < 0),
occurring every `every` steps from `start_step` through `end_step`
inclusive (`end_step=None` means through the end of the horizon). A
single life-cycle run composes several rules into one schedule via
`build_cashflow_schedule`, e.g. contribute every step 0-120, then
withdraw every step 121-360, expressed as two rules rather than one
schedule with a sign change baked in.

## GlidepathCheckpoint

```python
class GlidepathCheckpoint(BaseModel):
    year: float = Field(ge=0)
    weights: dict[str, float] = Field(description='factor name -> target weight at this checkpoint, summing to 1.0.')
```

One waypoint in a glidepath: at `year` years from t0, the portfolio's target
weights are exactly `weights`, interpolated piecewise-linearly against
neighboring checkpoints everywhere in between (see `resolve_glidepath_weights`).

## PortfolioSummary

```python
class PortfolioSummary(BaseModel):
    risk: PortfolioRiskMetrics = Field(description='Drawdown/VaR/CVaR/volatility, always computed.')
    withdrawal_success: WithdrawalSuccessMetrics = Field(description='Depletion/survival summary. Well defined for any portfolio: with no withdrawals, nothing depletes and success_rate is 1.0.')
    goal_probability: GoalProbability | None = Field(default=None, description='Set only when a goal value was given.')
    real_value: RealValueSummary | None = Field(default=None, description='Set only when an inflation factor and year were given.')
```

Every distributional read a computed portfolio supports, in one object;
see `portfolio_controller.Portfolio.summary()`. `goal_probability` and
`real_value` are None unless that call asked for them (each needs a target
the portfolio itself can't infer).

## PortfolioPreset

```python
class PortfolioPreset(BaseModel):
    name: str = Field(min_length=1, description="A short, human-readable label, e.g. '60/40 Balanced'.")
    description: str = Field(default='', description='What this portfolio represents and why these weights were chosen.')
    sleeves: list[PortfolioPresetSleeve] | None = Field(default=None, description='factor -> weight, summing to 1.0. Mutually exclusive with checkpoints.')
    checkpoints: list[GlidepathCheckpoint] | None = Field(default=None, description="The glidepath's waypoints. Mutually exclusive with sleeves.")
    durations: dict[str, float] | None = Field(default=None, description="Bond sleeve -> constant duration in years, so it is priced as a government bond fund rather than rolled as cash (see `Portfolio.compute`'s `durations`). None rolls every rate sleeve as cash.")
```

A named, built-in portfolio: either a static allocation (`sleeves`) or a
glidepath (`checkpoints`), exactly one of the two. See module docstring.

**Attributes:**

- <u>name (str):</u> a short, human-readable label, e.g. "60/40 Balanced".
- <u>description (str):</u> what this portfolio represents and why these weights (or glidepath) were chosen. Free text, purely documentation.
- <u>sleeves (list[PortfolioPresetSleeve] &#124; None):</u> factor -> weight, summing to 1.0. Set for a static preset, `None` for a glidepath one.
- <u>checkpoints (list[GlidepathCheckpoint] &#124; None):</u> the glidepath's waypoints. Set for a glidepath preset, `None` for a static one.

## PortfolioPreset.is_glidepath

```python
portfoliopreset.is_glidepath  # property -> bool
```

*No docstring.*

## load_portfolio_library

```python
load_portfolio_library(directory: str | Path = 'portfolios') -> dict[str, PortfolioPreset]
```

Load every portfolio preset in a directory, keyed by its id (the filename
stem, which is what `Portfolio.from_preset()` takes): the
"show me what's available" counterpart to `load_one()`, mirroring
`regimes_controller.RegimeLibrary.load()` and `profiles_controller.load_all()`.

**Args:**

- <u>directory (str &#124; Path):</u> the portfolios directory. Falls back to the copy bundled in the package when no such directory exists here (see `profiles_controller.resolve_directory()`).

**Returns:**

<u>dict[str, PortfolioPreset]:</u> every preset, keyed by filename stem, in sorted order.

**Raises:**

- <u>FileNotFoundError:</u> if neither `directory` nor a packaged copy of it exists.
- <u>pydantic.ValidationError:</u> if any file isn't a valid PortfolioPreset.

## load_portfolio_preset

```python
load_portfolio_preset(directory: str | Path, filename: str) -> PortfolioPreset
```

Load exactly one portfolio preset, resolving its `extends` chain if it
has one, but never scanning the rest of `directory`. This is the path a
single caller should use to pick one preset by id; see
financescenarios.profiles.profiles_controller.load_all() for the "list everything" (picker UI)
case.

**Args:**

- <u>directory (str &#124; Path):</u> the portfolios directory.
- <u>filename (str):</u> the preset's own YAML filename, e.g. "balanced_60_40.yaml" (the ".yaml" suffix is optional).

**Returns:**

<u>PortfolioPreset:</u> the fully resolved preset (extends chain merged in, `name` required at the end of that chain).

**Raises:**

- <u>FileNotFoundError:</u> if `filename`, or a file named in its `extends` chain, doesn't exist in `directory`.
- <u>ValueError:</u> if the `extends` chain is circular, or no file in the chain sets `name`.
- <u>pydantic.ValidationError:</u> if the resolved fields don't form a valid PortfolioPreset (e.g. weights don't sum to 1.0).

## compute_portfolio_factor_exposure

```python
compute_portfolio_factor_exposure(
    dates: list[date],
    values: list[float],
    model: Literal['three_factor', 'five_factor'] = 'five_factor',
) -> FactorExposureResult
```

Fetch Ken French's daily factor file and regress a portfolio's own realized return
series (`dates`/`values`) against it; see factor_exposure_model.compute_factor_exposure.

In plain terms: what kind of investments does this portfolio behave like? The answer is a
set of Betas, one per factor: how strongly the portfolio moves with the stock market as a
whole (Mkt-RF, the market return above the risk-free rate), with small versus large companies
(SMB), cheap versus expensive companies (HML), profitable versus unprofitable ones (RMW) and
conservative versus aggressive investors (CMA). A market Beta of 1.0 means the portfolio moves
one for one with the market; a Beta near 0 on the others means no size, value, profitability
or investment tilt. This is a style read, not portfolio construction.

The portfolio's excess return (its return minus the risk-free rate "RF") is regressed on the
factor returns with ordinary least squares, `Excess Return = Intercept + sum(Beta_i *
Factor_i) + Residual`, the model of [Fama and French (1993)](https://doi.org/10.1016/0304-405X(93)90023-5)
with three factors or [Fama and French (2015)](https://doi.org/10.1016/j.jfineco.2014.10.010)
with five. The fit itself is the Finance Toolkit's
`performance_model.get_fama_and_french_model_multi`, reused rather than reimplemented, and
the factor file comes from `performance_model.obtain_fama_and_french_dataset` (or
`obtain_fama_and_french_three_factor_dataset`), a live download from Kenneth French's data
library at Dartmouth, cached by the Finance Toolkit.

Ken French's file is daily, while a backtest can be on any calendar. Each portfolio return
is therefore matched against the daily factor returns *compounded* over the same window
(`(1 + r_1) * (1 + r_2) * ... - 1`), not a single day's value, so any calendar works without
a separate resampling step. Coarser-than-daily dates are period-start labels holding the
period's last value, so the window is shifted one label forward; see the
`factor_exposure_model` module docstring for why missing this shift silently gives a
pure-SPY Beta of ~0.03 instead of ~1.0.

The result (`FactorExposureResult`) holds `factors`, `intercept` (the average excess return
per period not explained by the factors), `slopes` (one Beta per factor), `r_squared` (the
share of the return variation the factors explain), `mean_squared_error` and
`n_observations`.

Also known as: Fama-French regression, style analysis, factor loadings, factor attribution.

**Args:**

- <u>dates (list[date]):</u> the portfolio's own observation dates, ascending.
- <u>values (list[float]):</u> the portfolio's own dollar value at each date.
- <u>model (str):</u> "five_factor" (Mkt-RF/SMB/HML/RMW/CMA, the default) or "three_factor" (Mkt-RF/SMB/HML; its own SMB differs from the five-factor file's, see obtain_fama_and_french_three_factor_dataset).

**Returns:**

FactorExposureResult

**Raises:**

- <u>ValueError:</u> see compute_factor_exposure.

**Notes:**

- Only meaningful for a realized return series, such as a historical backtest
  (`backtest_model.build_synthetic_scenario_set`): a simulated scenario has no calendar to line
  up with real factor history. It is a downstream read on a backtest's dates, like
  `weight_drift`/`real_value` are on a computed portfolio.
- The three-factor SMB differs from the five-factor file's SMB; see the Finance Toolkit's
  `obtain_fama_and_french_three_factor_dataset`.
- Ken French's file is not always fully up to date, so the latest portfolio dates can fall
  outside it; too little overlap raises a `ValueError`.
- The factors are US equity factors; a non-US portfolio's Betas describe its co-movement
  with the US market, not its own market's style.

**As an example:**

```python
from datetime import date

from financescenarios import Portfolio
from financescenarios.config.config_model import EquityConfig, InterestRateConfig, ScenariosConfig, ToolkitConfig
from financescenarios.historical_data.backtest_model import build_synthetic_scenario_set
from financescenarios.historical_data.historical_data_controller import fetch_historical_data
from financescenarios.portfolio.factor_exposure.factor_exposure_controller import (
    compute_portfolio_factor_exposure,
)
from financescenarios.scenarios_controller import build_toolkit

config = ScenariosConfig(
    start_date=date(2000, 1, 1),
    toolkit=ToolkitConfig(start_date=date(2000, 1, 1)),
    interest_rates=[InterestRateConfig(name="united_states_short_rate", country="United States", currency="USD")],
    equities=[EquityConfig(name="us_broad", ticker="SPY", currency="USD")],
)
history = fetch_historical_data(config, build_toolkit(config))
backtest = build_synthetic_scenario_set(history, ["us_broad", "united_states_short_rate"], period="monthly")

spy_only = Portfolio(backtest).compute({"us_broad": 1.0})
balanced = Portfolio.from_preset(backtest, preset="balanced_60_40").compute(rebalance_every=12)
for result in (spy_only, balanced):
    compute_portfolio_factor_exposure(result.dates, result.paths["portfolio"][0].tolist())
```

Which returns (backtested on 2026-10-04, monthly from 2004-01-01 to 2026-10-01):

| portfolio | Mkt-RF | SMB | HML | RMW | CMA | intercept | r_squared | n_observations |
|:----------|-------:|----:|----:|----:|----:|----------:|----------:|---------------:|
| 100% SPY | 0.9971 | -0.1231 | 0.0243 | 0.0457 | 0.0239 | -0.000348 | 0.9963 | 271 |
| 60/40 Balanced | 0.5938 | -0.0741 | 0.0061 | 0.0256 | 0.0235 | -0.000066 | 0.9934 | 271 |

SPY's market Beta is 0.997, as it should be for a fund that is the US market, with a slight
large-company tilt (SMB -0.12) and no value, profitability or investment tilt; the factors
explain 99.6% of its monthly moves. The 60/40 portfolio carries about 60% of that market
exposure, as its equity weight says. With `model="three_factor"` SPY's Betas are 0.9920,
-0.1392 and 0.0134 (R-squared 0.9958).

**References:**

- Fama, E.F., French, K.R. (1993). "Common risk factors in the returns on stocks and bonds." Journal of Financial Economics, 33(1), 3-56. <https://doi.org/10.1016/0304-405X(93>)90023-5
- Fama, E.F., French, K.R. (2015). "A five-factor asset pricing model." Journal of Financial Economics, 116(1), 1-22. <https://doi.org/10.1016/j.jfineco.2014.10.010>
- French, K.R. "Data Library." Tuck School of Business at Dartmouth. <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html>
