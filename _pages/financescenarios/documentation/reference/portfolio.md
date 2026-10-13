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

Turn simulated (or historical) markets into the value of an actual investment portfolio: pick a weight per asset,
say 60% US equities and 40% US bonds, and see what the portfolio and each holding are worth in every scenario.

The scenario generator answers "what could markets do?"; `Portfolio` answers "what would that mean for my money?":
will the money last, will a goal be reached, what is it worth after inflation and how deep are the falls. It never
calibrates, simulates or changes the run it is given.

A holding can be anything with a price or a return: equities, commodities, interest rates, credit and real estate
(`investable_factors` lists them). An interest rate or credit holding earns its rate like cash, or is priced as a
bond fund when given a duration. Inflation, unemployment and other economic series cannot be held.

Left alone (buy-and-hold), every holding grows with its own asset, so the weights drift. Rebalancing resets every
holding to its target weight, selling what rose and buying what fell: the "constant-mix" strategy of
[Perold and Sharpe (1988)](https://doi.org/10.2469/faj.v44.n1.16).

`compute()` returns a new `ScenarioSet` with a "portfolio" path and one "<factor>_value" path per holding, so it
works like any run. A holding's path is the money held in it, but its returns are what the asset itself earned:
rebalancing moves money in and out of a holding, so its value alone says little about how the asset did.

| Option | Default | Meaning |
|:-------|:--------|:--------|
| `weights` | preset | Factor name to target weight, summing to 1.0. |
| `initial_value` | `100.0` | The value at the start. |
| `rebalance_every` | `None` | Steps between rebalances; `None` is buy-and-hold. |
| `rebalance_band` | `None` | Also rebalance when a weight drifts this far from target. |
| `transaction_cost_rate` | `0.0` | Cost as a fraction of the amount traded. |
| `cashflow_rules` | `None` | Recurring deposits and withdrawals, see `cashflow_rule()`. |
| `inflation_factor` | `None` | Raise every cashflow with this simulated inflation. |
| `fee_rate` | `0.0` | Yearly fee on assets, flat or per holding. |
| `durations` | `None` | Price a rate or credit holding as a bond fund of this duration. |
| `config` | `None` | Convert holdings into the run's reporting currency. |

Mixes that change over time use `compute_glidepath()`, ready-made mixes ship as presets (`from_preset()`), and on
history (`backtest()`) the same calls give a backtest.

**As an example:**

```python
portfolio = Portfolio.from_preset(result, preset="balanced_60_40")  # list_presets(kind="portfolios") shows all 14
values = portfolio.compute(initial_value=100_000, rebalance_every=12)
values.describe()
```

Which returns, on a five-year run of the default settings and factor set:

| factor | category | terminal_mean | terminal_q05 | terminal_q95 |
|:-------|:---------|--------------:|-------------:|-------------:|
| portfolio | portfolio | 0.0837 | -0.0000 | 0.1611 |
| us_broad_value | holding | 0.0983 | -0.0465 | 0.2321 |
| united_states_long_rate_value | holding | 0.0546 | 0.0334 | 0.0756 |

The 60/40 earns 8.37% a year on average, between its stocks' 9.83% and its bond fund's 5.46%.

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

Build a Portfolio from one of the ready-made mixes, so you pick a strategy by name instead of typing weights.

Ask for "balanced_60_40" and you get the textbook 60/40 portfolio, with a description of why those weights. The
preset becomes the portfolio's default mix, so `compute()` needs no weights, and a glidepath preset runs as a
glidepath. Fourteen presets ship with the package, among them `balanced_60_40`, `all_weather`,
`bogleheads_three_fund`, `permanent_portfolio` and `target_date_glidepath`;
`list_presets(kind="portfolios")` lists them all. Copy one into a local `portfolios/` folder to make your own;
a local folder wins over the bundled one.

The presets hold factors of the broad factor set (`us_broad`, `united_states_long_rate`, `gold`, ...). On a run
without one of them, `compute()` names the missing factor.

Also known as: model portfolio, named allocation, strategic asset allocation template.

**Args:**

- <u>scenario_set (ScenarioSet):</u> the run to build the portfolio on.
- <u>preset (str &#124; PortfolioPreset):</u> a preset id such as "balanced_60_40" (".yaml" optional), or a loaded preset.
- <u>config (ScenariosConfig &#124; None):</u> the run's config, to convert currencies (see the class). Defaults to None.
- <u>portfolios_dir (str &#124; Path):</u> the folder presets are read from; the bundled presets when it does not exist. Defaults to "portfolios".
- <u>category_map (dict[str, str] &#124; None):</u> factor name to category, for a hand-built run. Defaults to None.

**Returns:**

<u>Portfolio:</u> a portfolio whose `compute()` uses the preset's mix.

**Raises:**

- <u>FileNotFoundError:</u> if no such preset exists.
- <u>pydantic.ValidationError:</u> if the preset file is invalid, for example weights that don't sum to 1.0.

**As an example:**

```python
from financescenarios import Portfolio, Scenarios

result = Scenarios.from_profiles().simulate()
portfolio = Portfolio.from_preset(result, preset="balanced_60_40")
portfolio.preset.description
values = portfolio.compute(initial_value=100_000, rebalance_every=12)
```

Which returns the description "The textbook mix: 60% US stocks and 40% US Treasury bonds.", and `values` holds
"portfolio", "us_broad_value" and "united_states_long_rate_value"; the class example shows what each earned.

## Portfolio.backtest

```python
Portfolio.backtest(
    scenarios: 'Scenarios',
    preset: str | PortfolioPreset,
    period: str = 'monthly',
    portfolios_dir: str | Path = 'portfolios',
) -> 'Portfolio'
```

Build a ready-made mix on what markets actually did, naming the preset once, so its `compute()` is a backtest.

A backtest asks how a strategy would have done in the past. Without this, the preset is named twice: once to
fetch the history of its holdings, once to build the portfolio on it. This fetches the history of exactly the
preset's holdings through `Scenarios.history()`, lines them up on one calendar, and returns the portfolio built
on it with `from_preset()`. Every read then works as on simulated scenarios, with one path instead of
thousands: `compute()`, `risk_metrics()`, `factor_exposure()` and `benchmark()`.

Also known as: historical simulation, strategy backtest.

**Args:**

- <u>scenarios (Scenarios):</u> the `Scenarios` to fetch history through, e.g. `Scenarios.from_profiles()`.
- <u>preset (str &#124; PortfolioPreset):</u> a preset id such as "balanced_60_40", or a loaded preset.
- <u>period (str):</u> the calendar to line the history up on: "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "monthly".
- <u>portfolios_dir (str &#124; Path):</u> the folder presets are read from; the bundled presets when it does not exist. Defaults to "portfolios".

**Returns:**

<u>Portfolio:</u> the preset's portfolio on history; `compute()` without weights gives the backtest.

**Raises:**

- <u>FileNotFoundError:</u> if no such preset exists.
- <u>ValueError:</u> if `scenarios` has no Finance Toolkit, or the holdings share too few dates.
- <u>KeyError:</u> if a holding has no history.

**As an example:**

```python
from financescenarios import Portfolio, Scenarios

portfolio = Portfolio.backtest(Scenarios.from_profiles(), preset="balanced_60_40")
values = portfolio.compute(initial_value=100_000, rebalance_every=12)
portfolio.factor_exposure()
```

This is the same as `Portfolio.from_preset(scenarios.history(portfolio="balanced_60_40"), "balanced_60_40")`.

## Portfolio.preset

```python
portfolio.preset  # property -> PortfolioPreset | None
```

The ready-made mix this portfolio uses by default, if it was built with `from_preset()`; None otherwise.

## Portfolio.investable_factors

```python
portfolio.investable_factors  # property -> list[str]
```

Every factor in this run that a holding can name: its equities, commodities, interest rates, credit and real
estate. Inflation, unemployment and other economic series are left out, since they cannot be held.

## Portfolio.cashflow_rule

```python
cashflow_rule(
    amount: float,
    every_years: float = 1.0,
    start_year: float = 0.0,
    end_year: float | None = None,
    years: range | None = None,
) -> CashflowRule
```

Build a recurring deposit or withdrawal from a description in years, such as "deposit 10,000 a year for 15 years".

A positive amount is a deposit, a negative one a withdrawal. Stating it in years keeps a rule meaning the same
whether the run steps monthly, quarterly or yearly; the steps are worked out against this run's own dates. A life
plan is several rules, for example one that saves for 15 years and one that withdraws after that. Pass the rules
to `compute()` as `cashflow_rules`.

`end_year` is included; `years=range(0, 15)` is the Python way, end excluded: years 0 to 14, as `end_year=14`.
`CashflowRule.yearly()` works without a Portfolio.

Also known as: contribution plan, withdrawal plan, savings plan, decumulation schedule.

**Args:**

- <u>amount (float):</u> the amount each time; positive deposits, negative withdraws.
- <u>every_years (float):</u> years between payments, e.g. 1/12 monthly or 0.25 quarterly. Defaults to 1.0. A cadence finer than the run's steps gives one payment per step, with a warning.
- <u>start_year (float):</u> the first year it is paid, snapped to the nearest step. Defaults to 0.0.
- <u>end_year (float &#124; None):</u> the last year it is paid, snapped to the nearest step. Defaults to None, the end of the run.
- <u>years (range &#124; None):</u> the years paid, end excluded, instead of the three above. Defaults to None.

**Returns:**

<u>CashflowRule:</u> the rule in steps of this run (`amount`, `every`, `start_step`, `end_step`).

**Raises:**

- <u>ValueError:</u> if `amount` is not a finite number, `every_years` is not positive, a year falls outside the run, or `years` comes with another year argument.

**As an example:**

```python
# portfolio: the Portfolio of compute()'s example (30 yearly steps)
contribute = portfolio.cashflow_rule(10_000, every_years=1, end_year=14)
withdraw = portfolio.cashflow_rule(-40_000, every_years=1, start_year=15)
```

Which returns:

| rule | amount | every | start_step | end_step |
|:-----|-------:|------:|-----------:|---------:|
| contribute | 10000.0 | 1 | 0 | 14 |
| withdraw | -40000.0 | 1 | 15 | None |

The saver deposits 10,000 in years 0 to 14 and withdraws 40,000 a year from year 15 to the end; on monthly steps
the same call gives `every=12`. See `withdrawal_success()` for how this plan fares.

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

Build a portfolio from a target weight per factor and see its value in every scenario.

Give it `{"us_broad": 0.6, "united_states_short_rate": 0.4}` to see that 60/40 portfolio's value in every
scenario; without options it is bought once and held.

Interest rate and credit holdings earn their rate like cash, unless `durations` prices them as a bond fund, which
a rate rise marks down at once ([Redington, 1952](https://doi.org/10.1017/S0020268100052811)):

```text
return(t) = -duration * (y(t) - y(t-1)) + y(t-1) * dt
```

**Args:**

- <u>weights (dict[str, float] &#124; None):</u> factor name to target weight, summing to 1.0. Defaults to the preset's mix.
- <u>initial_value (float):</u> the value at the start. Defaults to 100.0.
- <u>rebalance_every (int &#124; None):</u> steps between rebalances. Defaults to None, buy-and-hold.
- <u>cashflow_rules (list[CashflowRule] &#124; None):</u> deposits and withdrawals, see `cashflow_rule()`. Defaults to None.
- <u>fee_rate (float &#124; dict[str, float]):</u> yearly fee on assets, flat or per holding. Defaults to 0.0.
- <u>durations (dict[str, float] &#124; None):</u> bond duration in years per rate or credit holding; a long rate without one warns. Defaults to None.
- <u>rebalance_band (float &#124; None):</u> also rebalance when a weight drifts this far from target. Defaults to None.
- <u>transaction_cost_rate (float):</u> cost as a fraction of the amount traded. Defaults to 0.0.
- <u>inflation_factor (str &#124; None):</u> an inflation factor every cashflow rises with. Defaults to None.

**Returns:**

<u>ScenarioSet:</u> a new run with "portfolio" (the total value) and "<factor>_value" (each holding's value).

**Raises:**

- <u>ValueError:</u> if a weight, factor or option is invalid, or there are no weights and no preset.
- <u>KeyError:</u> if a factor is not in this run.

**As an example:**

```python
# scenario_set: 1,000 scenarios over 30 yearly steps of SPY ("us_broad"), the US short rate and inflation
portfolio = Portfolio(scenario_set)
weights = {"us_broad": 0.6, "united_states_short_rate": 0.4}
buy_and_hold = portfolio.compute(weights, initial_value=100.0)
rebalanced = portfolio.compute(weights, initial_value=100.0, rebalance_every=1, fee_rate=0.002)
```

Which returns (simulated on 2026-10-04) the value after 30 years:

| portfolio | 5% | median | 95% |
|:----------|---:|-------:|----:|
| buy-and-hold | 425.73 | 1432.81 | 5924.76 |
| rebalanced yearly, 0.2% fee | 426.07 | 1113.70 | 2995.75 |

Buy-and-hold drifts into equities: about the same bad outcomes, far better good ones.

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

Build a portfolio whose target mix changes over time, like a target-date fund that starts mostly in equities and
moves into bonds as the target date nears.

Give the weights at a few years (`GlidepathCheckpoint`, each summing to 1.0); in between, the target moves in a
straight line, and before the first and after the last checkpoint it stays flat. Everything else works as in
`compute()`, except that the portfolio must be rebalanced, or it would ignore the moving target.

Also known as: lifecycle fund, target-date fund, de-risking path.

**Args:**

- <u>checkpoints (list[GlidepathCheckpoint] &#124; None):</u> the target weights at chosen years, all naming the same factors. Defaults to None, this portfolio's glidepath preset.
- <u>initial_value (float):</u> the portfolio's value at the start. Defaults to 100.0.
- <u>rebalance_every (int):</u> steps between rebalances to the current target, at least 1. Defaults to 1.
- <u>cashflow_rules (list[CashflowRule] &#124; None):</u> as in `compute()`. Defaults to None.
- <u>fee_rate (float &#124; dict[str, float]):</u> as in `compute()`. Defaults to 0.0.
- <u>durations (dict[str, float] &#124; None):</u> as in `compute()`. Defaults to None.
- <u>rebalance_band (float &#124; None):</u> as in `compute()`. Defaults to None.
- <u>transaction_cost_rate (float):</u> as in `compute()`. Defaults to 0.0.
- <u>inflation_factor (str &#124; None):</u> as in `compute()`. Defaults to None.

**Returns:**

<u>ScenarioSet:</u> the same shape as `compute()` returns.

**Raises:**

- <u>ValueError:</u> if no checkpoints are given and there is no glidepath preset, the checkpoints name different factors, `rebalance_every` is below 1, or another input is invalid as in `compute()`.
- <u>KeyError:</u> if a factor, or `inflation_factor`, is not in this run.

**As an example:**

```python
from financescenarios import GlidepathCheckpoint

# portfolio: the Portfolio of compute()'s example (30 yearly steps)
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

The equity share glides from 90% to 30%, 2 points a year; after 30 years the median portfolio is worth 1,210.

## Portfolio.withdrawal_success

```python
withdrawal_success(portfolio_scenario_set: ScenarioSet | None = None) -> WithdrawalSuccessMetrics
```

Check whether a plan with withdrawals lasts: how often money is left at the end, when it typically runs out
otherwise, and how much the scenarios that make it end with.

This answers "will my retirement savings last?". A portfolio that runs out stays at 0, so its last value alone
says whether a scenario ever ran out. Without withdrawals nothing runs out and the success rate is 1.0; on a
historical backtest (one path) the answer is a plain yes or no.

Also known as: retirement success rate, probability of ruin (its complement), safe withdrawal analysis.

**Args:**

- <u>portfolio_scenario_set (ScenarioSet &#124; None):</u> a `compute()` or `compute_glidepath()` result. Defaults to None, the latest one this portfolio computed.

**Returns:**

<u>WithdrawalSuccessMetrics:</u> `success_rate` (share of scenarios with money left at the end), `median_depletion_year` (median year the others run out, None if none do) and `terminal_value_percentiles` (5th to 95th percentile of the final value, over the scenarios that last only).

**Raises:**

- <u>ValueError:</u> if nothing has been computed yet.

**As an example:**

```python
# portfolio: the Portfolio of compute()'s example (30 yearly steps)
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

Saving 10,000 a year for 15 years on top of 100,000, then spending 40,000 a year, the money lasts 30 years in
91.7% of the scenarios when the 40,000 is fixed, but only in 58% when it rises with inflation.

## Portfolio.goal_probability

```python
goal_probability(
    portfolio_scenario_set: ScenarioSet,
    target_value: float,
    target_year: float | None = None,
) -> GoalProbability
```

Find the probability that the portfolio reaches a target value, by a given year or at any point.

This answers "what are the chances I reach one million?", the saving-side counterpart of `withdrawal_success()`.
Without `target_year` it counts the scenarios that reach the target at any point and says when they typically get
there; with it, the scenarios at or above the target in that year. Values are nominal; `real_value()` gives
today's money.

Also known as: goal-based planning probability, shortfall probability (its complement).

**Args:**

- <u>portfolio_scenario_set (ScenarioSet):</u> a `compute()` or `compute_glidepath()` result.
- <u>target_value (float):</u> the value to reach.
- <u>target_year (float &#124; None):</u> the year to check, snapped to the nearest step. Defaults to None, any point in the run.

**Returns:**

<u>GoalProbability:</u> `probability` (share of scenarios that reach the target) and `median_year_reached` (median year they first do; None with `target_year`, or when none do).

**Raises:**

- <u>ValueError:</u> if `target_value` is not positive, or `target_year` falls outside the run.

**As an example:**

```python
# portfolio: the Portfolio of compute()'s example (30 yearly steps)
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

Starting with 100,000 and saving 10,000 a year in a rebalanced 60/40, the portfolio passes one million at some
point in 97.7% of the scenarios, typically after 20 years; it is above one million in year 20 itself in 57.7%.

## Portfolio.factor_exposure

```python
factor_exposure(
    portfolio_scenario_set: ScenarioSet | None = None,
    model: Literal['three_factor', 'five_factor'] = 'five_factor',
) -> pl.DataFrame
```

Measure what this portfolio actually behaved like over history: its loading (Beta) on each of the Fama-French
factors, from a regression of its historical returns (see `compute_portfolio_factor_exposure()`).

A market Beta of 0.66 means the portfolio moved about 0.66% for every 1% the stock market moved; the others show a
tilt toward small (SMB), cheap (HML), profitable (RMW) or conservative (CMA) companies. R-squared says how much of
its ups and downs these factors explain.

**Args:**

- <u>portfolio_scenario_set (ScenarioSet &#124; None):</u> a `compute()` result on history. Defaults to None, which computes this portfolio's own mix first.
- <u>model (str):</u> "five_factor" ([Fama and French, 2015](https://doi.org/10.1016/j.jfineco.2014.10.010)) or "three_factor" ([Fama and French, 1993](https://doi.org/10.1016/0304-405X(93)90023-5)). Defaults to "five_factor".

**Returns:**

<u>pl.DataFrame:</u> one row with 'portfolio', one column per factor, 'alpha' (the return per period no factor explains), 'r_squared', 'observations' and the 'from' and 'to' dates.

**Raises:**

- <u>ValueError:</u> if the run is simulated scenarios rather than history (more than one path).

**As an example:**

```python
history = scenarios.history(portfolio="balanced_60_40")
Portfolio.from_preset(history, preset="balanced_60_40").factor_exposure()
```

Which returns, on the default settings and factor set (monthly, 2000-01-01 to 2026-10-01):

| portfolio | Mkt-RF | SMB | HML | RMW | CMA | r_squared | observations |
|:----------|-------:|----:|----:|----:|----:|----------:|-------------:|
| 60/40 Balanced | 0.5399 | -0.0714 | -0.0420 | 0.1201 | -0.0168 | 0.8654 | 319 |

## Portfolio.risk_metrics

```python
risk_metrics(portfolio_scenario_set: ScenarioSet | None = None) -> PortfolioRiskMetrics
```

Measure how bumpy the ride is and how bad it can get: drawdowns, Value at Risk, volatility, growth rates and the
chance of a loss.

It reports the deepest fall from a previous high in each scenario, the loss in the worst 5% of scenarios, how much
the value swings per year, the yearly growth rate to plan around and the chance of ending below the start, all
counted over the simulated paths. The Expected Shortfall (CVaR) averages the worst 5% instead of taking their edge
([Artzner et al., 1999](https://doi.org/10.1111/1467-9965.00068)). VaR, CVaR and the chance of a loss cover the
whole run, deposits and withdrawals included, so on a 30-year run they describe a 30-year outcome.

Also known as: Value at Risk, Expected Shortfall, maximum drawdown.

**Args:**

- <u>portfolio_scenario_set (ScenarioSet &#124; None):</u> a `compute()` or `compute_glidepath()` result. Defaults to None, the latest one this portfolio computed.

**Returns:**

<u>PortfolioRiskMetrics:</u> `max_drawdown_percentiles` (worst fall from a high, a negative fraction), `value_at_risk_95` and `conditional_value_at_risk_95` (loss over the whole run, negative for a gain), `annualized_volatility`, `cagr_percentiles` (yearly growth rate) and `probability_of_loss`.

**Raises:**

- <u>ValueError:</u> if nothing has been computed yet.

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
| value_at_risk_95 | -3.2573 | -3.2607 |
| annualized_volatility | 13.21% | 10.45% |
| CAGR, median | 9.28% | 8.37% |
| probability_of_loss | 0.0 | 0.0 |

Over 30 years neither portfolio loses money in any scenario: a VaR of -3.26 is a gain of 326% even at the 5th
percentile. Rebalancing back to 60/40 cuts the median worst fall from 24% to 17% and the yearly swings from 13.2%
to 10.4%, in exchange for a lower median growth rate.

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

Value the portfolio in today's money at a given year, taking out each scenario's own inflation.

One million in 20 years is not one million of today's money. This divides every scenario's portfolio value by that
same scenario's cumulative inflation, `real value = nominal value / inflation index`, so the answer is in today's
purchasing power and is a range, not one number. It is the mirror image of `compute()`'s `inflation_factor`, which
raises the cashflows going in.

Also known as: inflation-adjusted value, real wealth, purchasing-power value.

**Args:**

- <u>portfolio_scenario_set (ScenarioSet):</u> a `compute()` or `compute_glidepath()` result.
- <u>inflation_factor (str):</u> the simulated inflation to deflate by, such as "united_states_inflation"; it does not need to be a holding.
- <u>year (float):</u> the year to value at, snapped to the nearest step.

**Returns:**

<u>RealValueSummary:</u> `year` (the step actually used), `mean` and `percentiles` (5th to 95th) of the real value.

**Raises:**

- <u>KeyError:</u> if `inflation_factor` is not in this run.
- <u>ValueError:</u> if `year` falls outside the run, or `inflation_factor` is a price rather than a rate.

**As an example:**

```python
# saver: the portfolio of goal_probability()'s example
portfolio.real_value(saver, inflation_factor="inflation", year=20)
```

Which returns (simulated on 2026-10-04):

| year | mean | 5% | 25% | median | 75% | 95% |
|-----:|-----:|---:|----:|-------:|----:|----:|
| 20.0 | 694,005 | 306,366 | 464,152 | 636,645 | 841,980 | 1,357,857 |

In nominal terms the saver's median portfolio is worth 1,064,686 after 20 years; in today's money that median is
636,645, so inflation takes away about 40% of the purchasing power over those 20 years.

## Portfolio.weight_drift

```python
weight_drift(portfolio_scenario_set: ScenarioSet | None = None) -> dict[str, np.ndarray]
```

Show how far each holding's weight has wandered from its target, at every step of every scenario.

A 60/40 portfolio is only exactly 60/40 right after a rebalance. In between, and forever in a buy-and-hold
portfolio, the weights wander as one asset outgrows the other: +0.10 means the holding is 10 points above its
target. The target is the one the result was computed with (fixed, or the glidepath's at each step), so no mix is
passed here. A scenario that ran out of money has a drift of 0.

Also known as: allocation drift, weight deviation, tracking to target.

**Args:**

- <u>portfolio_scenario_set (ScenarioSet &#124; None):</u> a `compute()` or `compute_glidepath()` result. Defaults to None, the latest one this portfolio computed.

**Returns:**

<u>dict[str, np.ndarray]:</u> factor name to actual minus target weight, one row per scenario and one column per step.

**Raises:**

- <u>ValueError:</u> if nothing has been computed yet, or the result holds no holdings.
- <u>RuntimeError:</u> if the result carries no target weights and this portfolio has computed nothing yet.

**As an example:**

```python
# portfolio: the Portfolio of compute()'s example (30 yearly steps)
result = portfolio.compute({"us_broad": 0.6, "united_states_short_rate": 0.4})
drift = portfolio.weight_drift(result)["us_broad"]
```

Which returns (simulated on 2026-10-04), the equity holding's drift when bought and held:

| year | mean | 5% | median | 95% |
|-----:|-----:|---:|-------:|----:|
| 1 | 0.0154 | -0.06 | 0.02 | 0.06 |
| 10 | 0.1188 | -0.09 | 0.14 | 0.26 |
| 30 | 0.2551 | -0.01 | 0.29 | 0.38 |

Left alone, the 60% equity holding is typically 89% of the portfolio after 30 years (60% + 29 points). With
`rebalance_every=1` the drift is 0 at every yearly step, and with `rebalance_band=0.05` it never exceeds 5 points.
`weight_drift_summary()` boils this down to one row per holding.

## Portfolio.weight_drift_summary

```python
weight_drift_summary(
    portfolio_scenario_set: ScenarioSet | None = None,
    threshold: float = 0.05,
) -> pl.DataFrame
```

Sum up how far each holding wandered from its target weight, in one table with one row per holding.

`weight_drift()` gives a number for every step of every scenario; this boils it down to what you usually want
to know. Is the holding above or below its target on average? How far off does it get at worst? And in how many
scenarios does it ever wander past a tolerance, 5 points by default? Left alone, a 60/40 portfolio's equity
holding drifts up as stocks outgrow bonds; rebalanced with `rebalance_band=0.05`, no holding ever passes 5
points, so its share past the threshold is 0.

Also known as: allocation drift report, rebalancing check.

**Args:**

- <u>portfolio_scenario_set (ScenarioSet &#124; None):</u> a `compute()` or `compute_glidepath()` result. Defaults to None, the latest one this portfolio computed.
- <u>threshold (float):</u> the drift, as a weight, that counts as wandering off. Defaults to 0.05, 5 points.

**Returns:**

<u>pl.DataFrame:</u> one row per holding: "holding", "target_weight" (at the start; a glidepath's target moves), "mean_drift" (over every step and scenario), "max_drift" (the largest drift either way, as a positive number) and "share_past_threshold" (the share of scenarios whose drift ever goes past `threshold`).

**Raises:**

- <u>ValueError:</u> if nothing has been computed yet, or `threshold` is not between 0 and 1.
- <u>RuntimeError:</u> if the run passed is not a `compute()` result and this portfolio has computed nothing yet.

**As an example:**

```python
# portfolio: the Portfolio of compute()'s example (30 yearly steps)
bought_and_held = portfolio.compute({"us_broad": 0.6, "united_states_short_rate": 0.4})
portfolio.weight_drift_summary(bought_and_held)
```

Which returns one row for "us_broad" and one for "united_states_short_rate". The two drift by the same amount
in opposite directions, since the weights always add up to 1.

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

Get every read of a computed portfolio in one call: risk, whether the money lasts, and optionally the chance of
reaching a goal and the value after inflation.

Risk (`risk_metrics()`), whether the money lasts (`withdrawal_success()`) and the end value across all
scenarios (`median_end_value`, `percentile(q)`) are always filled in. The real value needs both an
`inflation_factor` and a `real_value_year`, or it is None. With a `goal_value`, `goal_probability` is always
set, and `summary.goal()` returns it typed as never None; without one it is None. Each read is also available
on its own.

Also known as: portfolio report, outcome summary.

**Args:**

- <u>portfolio_scenario_set (ScenarioSet &#124; None):</u> a `compute()` or `compute_glidepath()` result. Defaults to None, the latest one this portfolio computed.
- <u>goal_value (float &#124; None):</u> a target value; when given, `goal_probability` is always set. Defaults to None.
- <u>goal_year (float &#124; None):</u> the year to check the goal at, snapped to the nearest step. Defaults to None, any point in the run.
- <u>inflation_factor (str &#124; None):</u> the simulated inflation to deflate by, for `real_value`. Defaults to None.
- <u>real_value_year (float &#124; None):</u> the year to report the real value at. Defaults to None.

**Returns:**

<u>PortfolioSummary:</u> `risk`, `withdrawal_success`, `goal_probability`, `real_value` and `end_value_percentiles`.

**Raises:**

- <u>KeyError:</u> if `inflation_factor` is not in this run.
- <u>ValueError:</u> if nothing has been computed yet, or a value or year is out of range.

**As an example:**

```python
# saver: the portfolio of goal_probability()'s example
summary = portfolio.summary(saver, goal_value=1_000_000.0, inflation_factor="inflation", real_value_year=20)
```

Which returns (simulated on 2026-10-04):

| field | value |
|:------|------:|
| risk.max_drawdown_percentile(0.5) | -13.74% |
| risk.cagr_percentile(0.5) | 11.11% |
| withdrawal_success.success_rate | 1.0 |
| goal().probability | 0.977 |
| goal().median_year_reached | 20.0 |
| real_value.median | 636,645 |

The saver never withdraws, so every scenario "succeeds". The median growth rate of 11.1% is higher than the 8.4%
in `risk_metrics()`'s example, because the yearly deposits count as growth of the value.

## Portfolio.benchmark

```python
benchmark(
    portfolio_scenario_set: ScenarioSet,
    benchmark_scenario_set: ScenarioSet,
    weights: dict[str, float] | None = None,
    benchmark_weights: dict[str, float] | None = None,
) -> RelativeMetrics
```

Compare this portfolio with another one: how closely it tracks it, how much it moves with it, and whether it grew
faster or earned more per unit of risk.

The benchmark is any portfolio: a market index, another mix on the same run, or the same mix over other dates.
Tracking error is how much the two drift apart per year; correlation and Beta say how much this one moves with
the other (a Beta of 0.6 means 0.6% for every 1% of the benchmark). Relative CAGR and relative Sharpe ratio
([Sharpe, 1966](https://doi.org/10.1086/294846)) are this one's growth rate and return per unit of risk minus the
benchmark's. Active share is the part of the mix that differs
([Cremers and Petajisto, 2009](https://doi.org/10.1093/rfs/hhp057)). The two are compared over the dates they
share; on simulated scenarios each side is first averaged into its mean path, so the figures describe the two
average paths.

**Args:**

- <u>portfolio_scenario_set (ScenarioSet):</u> this portfolio's `compute()` or `compute_glidepath()` result.
- <u>benchmark_scenario_set (ScenarioSet):</u> the result of the portfolio to compare against.
- <u>weights (dict[str, float] &#124; None):</u> this portfolio's target weights, for active share. Defaults to None, the fixed preset's, else the result's own mix.
- <u>benchmark_weights (dict[str, float] &#124; None):</u> the benchmark's target weights. Defaults to None, its result's own mix (none for a glidepath).

**Returns:**

<u>RelativeMetrics:</u> `tracking_error`, `correlation`, `beta`, `relative_cagr`, `relative_sharpe_ratio` and `active_share`.

**Raises:**

- <u>ValueError:</u> if the two share fewer than two dates.

**As an example:**

```python
# backtest: the monthly SPY and US short rate history of build_synthetic_scenario_set()'s example
weights = {"us_broad": 0.6, "united_states_short_rate": 0.4}
portfolio = Portfolio(backtest)
balanced = portfolio.compute(weights, initial_value=100.0, rebalance_every=12)
spy_only = portfolio.compute({"us_broad": 1.0}, initial_value=100.0)
portfolio.benchmark(balanced, spy_only)  # each result knows its weights
```

Which returns (backtested on 2026-10-04, 274 monthly dates from 2004-01-01 to 2026-10-01):

| tracking_error | correlation | beta | relative_cagr | relative_sharpe_ratio | active_share |
|---------------:|------------:|-----:|--------------:|----------------------:|-------------:|
| 5.91% | 0.9986 | 0.5942 | -3.27% | 0.1023 | 0.40 |

The 60/40, rebalanced every 12 months, moves almost in lockstep with SPY with 59% of its swings, and grew 3.3
points a year slower yet earned slightly more return per unit of risk.

## CashflowRule

```python
class CashflowRule(BaseModel):
    amount: float = Field(description='Positive = contribution/inflow, negative = withdrawal/outflow, per occurrence.')
    every: int = Field(ge=1, description='Steps between occurrences.')
    start_step: int = Field(default=0, ge=0)
    end_step: int | None = Field(default=None, ge=0, description='Inclusive. None = through the end of the horizon.')
```

A recurring deposit (positive `amount`) or withdrawal (negative `amount`), paid every `every` steps from
`start_step` through `end_step` (None runs to the end). `Portfolio.cashflow_rule()` builds one from years instead
of steps; a plan that saves first and withdraws later is two rules.

## CashflowRule.yearly

```python
CashflowRule.yearly(
    amount: float,
    years: range | None = None,
    steps_per_year: int = 1,
) -> 'CashflowRule'
```

Build a deposit or withdrawal from a Python `range` of years, such as "10,000 a year in years 0 to 14".

`range(0, 15)` is years 0 to 14, fifteen payments: the end is left out, as everywhere in Python, while
`end_step` and `Portfolio.cashflow_rule(end_year=...)` include it. `range(0, 15, 5)` pays in years 0, 5 and 10.
A rule counts in steps of the run, so `steps_per_year` says how many steps make a year. When you have the
Portfolio at hand, `portfolio.cashflow_rule(amount, years=range(...))` takes the same range and reads the step
size off the run itself, so it cannot be set wrong.

These three give the same rule on a monthly run:

| call | every | start_step | end_step |
|:-----|------:|-----------:|---------:|
| `CashflowRule.yearly(10_000, range(0, 15), steps_per_year=12)` | 12 | 0 | 168 |
| `portfolio.cashflow_rule(10_000, years=range(0, 15))` | 12 | 0 | 168 |
| `portfolio.cashflow_rule(10_000, end_year=14)` | 12 | 0 | 168 |

**Args:**

- <u>amount (float):</u> the amount each time; positive deposits, negative withdraws.
- <u>years (range &#124; None):</u> the years it is paid, end excluded; the range's step is the gap in years. Defaults to None, every year from the start to the end of the run.
- <u>steps_per_year (int):</u> the run's steps in one year: 1 yearly, 4 quarterly, 12 monthly. Defaults to 1.

**Returns:**

<u>CashflowRule:</u> the rule in steps (`amount`, `every`, `start_step`, `end_step`).

**Raises:**

- <u>ValueError:</u> if `amount` is not a finite number, `steps_per_year` is below 1, or `years` is empty, counts down or starts before year 0.

**As an example:**

```python
from financescenarios import CashflowRule

save = CashflowRule.yearly(10_000, years=range(0, 15))
spend = CashflowRule.yearly(-40_000, years=range(15, 31))
```

On a 30-year yearly run, `save` deposits 10,000 in years 0 to 14 and `spend` withdraws 40,000 a year from year
15 through year 30, the last date of the run: the plan of `Portfolio.cashflow_rule()`'s example.

## GlidepathCheckpoint

```python
class GlidepathCheckpoint(BaseModel):
    year: float = Field(ge=0)
    weights: dict[str, float] = Field(description='factor name -> target weight at this checkpoint, summing to 1.0.')
```

One point on a glidepath: the portfolio's target weights at `year` years from the start, summing to 1.0.
Between two checkpoints the weights move in a straight line; see `Portfolio.compute_glidepath()`.

## PortfolioSummary

```python
class PortfolioSummary(BaseModel):
    risk: PortfolioRiskMetrics = Field(description='Drawdown/VaR/CVaR/volatility, always computed.')
    withdrawal_success: WithdrawalSuccessMetrics = Field(description='Depletion/survival summary. Well defined for any portfolio: with no withdrawals, nothing depletes and success_rate is 1.0.')
    goal_probability: GoalProbability | None = Field(default=None, description='Set only when a goal value was given.')
    real_value: RealValueSummary | None = Field(default=None, description='Set only when an inflation factor and year were given.')
    end_value_percentiles: dict[str, float] = Field(default_factory=dict, description='5/25/50/75/95th percentile of the last value across every scenario, a scenario that ran out counting as 0. Portfolio.summary() always fills it; empty on a summary built by hand without it.')
```

Every read of a computed portfolio in one object, from `Portfolio.summary()`.

`risk` and `withdrawal_success` are always there. `goal_probability` is there when the summary was asked with a
`goal_value`, and `real_value` when it was asked with an inflation factor and a year; otherwise they are None.
`goal()` returns the goal read without the None check, and raises when no goal was given.

The percentile reads take a fraction instead of a text key: `percentile(0.5)` is the median end value across all
scenarios, a scenario that ran out counting as 0, and `median_end_value` is the same number.

**As an example:**

```python
summary = portfolio.summary(saver, goal_value=1_000_000.0)
summary.median_end_value         # the median value at the end of the run
summary.percentile(0.05)         # the end value in a bad (5th percentile) scenario
summary.goal().probability       # the chance of reaching one million
summary.risk.cagr_percentile(0.5)
```

## PortfolioSummary.median_end_value

```python
portfoliosummary.median_end_value  # property -> float
```

The median portfolio value at the end of the run across all scenarios, the same as `percentile(0.5)`.

## PortfolioSummary.percentile

```python
percentile(q: float) -> float
```

The end value at fraction `q` (0.05, 0.25, 0.5, 0.75 or 0.95) across all scenarios, a scenario that ran out
counting as 0; a ValueError for any other `q`.

## PortfolioSummary.goal

```python
goal() -> GoalProbability
```

The goal read, never None: `goal_probability` of a summary asked with a `goal_value`, or a ValueError
saying to pass one.

## PortfolioPreset

```python
class PortfolioPreset(BaseModel):
    name: str = Field(min_length=1, description="A short, human-readable label, e.g. '60/40 Balanced'.")
    description: str = Field(default='', description='What this portfolio represents and why these weights were chosen.')
    sleeves: list[PortfolioPresetSleeve] | None = Field(default=None, description='factor -> weight, summing to 1.0. Mutually exclusive with checkpoints.')
    checkpoints: list[GlidepathCheckpoint] | None = Field(default=None, description="The glidepath's waypoints. Mutually exclusive with sleeves.")
    durations: dict[str, float] | None = Field(default=None, description="Bond sleeve -> constant duration in years, so it is priced as a government bond fund rather than rolled as cash (see `Portfolio.compute`'s `durations`). None rolls every rate sleeve as cash.")
```

A ready-made portfolio mix, such as "60/40 Balanced": either fixed weights (`sleeves`) or weights that move over
time (`checkpoints`), exactly one of the two. Each ships as a YAML file under `portfolios/`; pick one with
`Portfolio.from_preset()`.

**Attributes:**

- <u>name (str):</u> a short label, e.g. "60/40 Balanced".
- <u>description (str):</u> what the mix is and why these weights.
- <u>sleeves (list[PortfolioPresetSleeve] &#124; None):</u> factor and weight per holding, summing to 1.0; None for a glidepath.
- <u>checkpoints (list[GlidepathCheckpoint] &#124; None):</u> the glidepath's target weights by year; None for a fixed mix.
- <u>durations (dict[str, float] &#124; None):</u> duration in years per bond holding, so it is priced as a bond fund; None earns every rate like cash.

## PortfolioPreset.is_glidepath

```python
portfoliopreset.is_glidepath  # property -> bool
```

Whether the mix moves over time (dated checkpoints, run with `compute_glidepath()`) rather than staying
fixed (sleeves, run with `compute()`).

## load_portfolio_library

```python
load_portfolio_library(directory: str | Path = 'portfolios') -> dict[str, PortfolioPreset]
```

Load every portfolio preset in a folder, keyed by its id: the file name without ".yaml", which is what
`Portfolio.from_preset()` takes. `list_presets(kind="portfolios")` shows the same presets as a table.

**Args:**

- <u>directory (str &#124; Path):</u> the portfolios folder; the bundled presets when it does not exist. Defaults to "portfolios".

**Returns:**

<u>dict[str, PortfolioPreset]:</u> every preset by id, in alphabetical order.

**Raises:**

- <u>FileNotFoundError:</u> if the folder does not exist and the package ships none of that name.
- <u>pydantic.ValidationError:</u> if a file is not a valid preset.

**As an example:**

```python
from financescenarios import load_portfolio_library

presets = load_portfolio_library()
presets["all_weather"].description
```

## load_portfolio_preset

```python
load_portfolio_preset(directory: str | Path, filename: str) -> PortfolioPreset
```

Load one portfolio preset by its id, such as "balanced_60_40", following its `extends:` chain if it has one.

`Portfolio.from_preset()` calls this for you. A preset can extend another and change only what differs: the files
in the chain are merged, the extending file winning, the same way as for settings and regimes.

**Args:**

- <u>directory (str &#124; Path):</u> the portfolios folder; the bundled presets when it does not exist.
- <u>filename (str):</u> the preset's file name, e.g. "balanced_60_40.yaml" (".yaml" optional).

**Returns:**

<u>PortfolioPreset:</u> the preset with its `extends` chain merged in.

**Raises:**

- <u>FileNotFoundError:</u> if the file, or one it extends, does not exist.
- <u>ValueError:</u> if the `extends` chain loops, or no file in it sets `name`.
- <u>pydantic.ValidationError:</u> if the preset is invalid, for example weights that don't sum to 1.0.

**As an example:**

```python
from financescenarios import load_portfolio_preset

load_portfolio_preset("portfolios", "balanced_60_40").description
```

## compute_portfolio_factor_exposure

```python
compute_portfolio_factor_exposure(
    dates: list[date],
    values: list[float],
    model: Literal['three_factor', 'five_factor'] = 'five_factor',
) -> FactorExposureResult
```

Measure what kind of investments a portfolio behaves like, by regressing its historical returns on the Fama-French
factors.

The answer is one Beta per factor: how strongly the portfolio moves with the stock market (Mkt-RF, its return above
the risk-free rate), and with small (SMB), cheap (HML), profitable (RMW) and conservatively investing (CMA)
companies. A market Beta of 1.0 means moving one for one with the market; R-squared is the share of the moves the
factors explain. It needs real history, not simulated scenarios, and the factors are US ones.

The return above the risk-free rate is regressed with ordinary least squares on the three factors of
[Fama and French (1993)](https://doi.org/10.1016/0304-405X(93)90023-5) or the five of
[Fama and French (2015)](https://doi.org/10.1016/j.jfineco.2014.10.010), from Ken French's
[Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html), compounded over each of
the portfolio's periods:

```text
Excess Return = Intercept + sum(Beta_i * Factor_i) + Residual
```

Also known as: Fama-French regression, style analysis.

**Args:**

- <u>dates (list[date]):</u> the portfolio's dates, oldest first.
- <u>values (list[float]):</u> the portfolio's value at each date.
- <u>model (str):</u> "five_factor" (Mkt-RF, SMB, HML, RMW, CMA) or "three_factor" (Mkt-RF, SMB, HML). Defaults to "five_factor".

**Returns:**

<u>FactorExposureResult:</u> `factors`, `slopes` (one Beta per factor), `intercept` (the return per period no factor explains), `r_squared`, `mean_squared_error` and `n_observations`.

**Raises:**

- <u>ValueError:</u> if `dates` and `values` differ in length, hold fewer than two points, or barely overlap with Ken French's file.

**As an example:**

```python
from financescenarios import Portfolio, compute_portfolio_factor_exposure

# backtest: the monthly SPY and US short rate history of build_synthetic_scenario_set()'s example
spy_only = Portfolio(backtest).compute({"us_broad": 1.0})
balanced = Portfolio(backtest).compute({"us_broad": 0.6, "united_states_short_rate": 0.4}, rebalance_every=12)
for result in (spy_only, balanced):
    compute_portfolio_factor_exposure(result.dates, result.paths["portfolio"][0].tolist())
```

Which returns (backtested on 2026-10-04, monthly from 2004-01-01 to 2026-10-01):

| portfolio | Mkt-RF | SMB | HML | RMW | CMA | r_squared | n_observations |
|:----------|-------:|----:|----:|----:|----:|----------:|---------------:|
| 100% SPY | 0.9971 | -0.1231 | 0.0243 | 0.0457 | 0.0239 | 0.9963 | 271 |
| 60/40 | 0.5938 | -0.0741 | 0.0061 | 0.0256 | 0.0235 | 0.9934 | 271 |

SPY's market Beta is 0.997, as it should be for the US market itself; the 60/40 carries about 60% of it.
