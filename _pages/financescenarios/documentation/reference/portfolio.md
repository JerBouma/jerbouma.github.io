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

Read a finished run through an investment portfolio: allocations, cashflows, glidepaths, risk metrics and factor exposure.

```python
from financescenarios import Portfolio, CashflowRule, GlidepathCheckpoint, PortfolioSummary, PortfolioPreset, load_portfolio_library, load_portfolio_preset, compute_portfolio_factor_exposure
```

## Portfolio

Turn simulated (or historical) markets into the value of an actual investment portfolio: pick a weight per asset,
say 60% US equities and 40% US bonds, and see what the portfolio and each holding are worth in every scenario.

The scenario generator answers "what could markets do?"; `Portfolio` answers "what would that mean for my money?":
will the money last, will a goal be reached, what is it worth after inflation and how deep are the falls. It never
calibrates, simulates or changes the run it is given.

A holding can be anything with a price or a return: equities, commodities, interest rates, credit and real estate
(`investable_factors` lists them). An interest rate holding earns its rate like cash, or is priced as a bond fund
when given a duration; a credit holding earns a government yield plus its spread less default losses; real estate
earns its price growth plus rents. Inflation, unemployment and other economic series cannot be held.

Left alone (buy-and-hold), every holding grows with its own asset, so the weights drift towards whatever did best
and the portfolio's risk drifts with them. Rebalancing resets every holding to its target weight, selling what rose
and buying what fell: the "constant-mix" strategy of
[Perold and Sharpe (1988)](https://doi.org/10.2469/faj.v44.n1.16). That choice shapes the whole distribution, not
just the average: buy-and-hold lets the winners run, so its best outcomes are far better, while constant-mix keeps
the risk where you set it, gains in markets that swing back and forth and lags in markets that trend one way.

The result works like any run: a "portfolio" path with the total value and one "<factor>_value" path per holding.
A holding's path is the money held in it, but its returns are what the asset itself earned, since rebalancing moves
money in and out of a holding.

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
| `base_rates` | auto | The government rate each credit holding's spread sits on. |
| `default_loss_rate` | by rating | Yearly loss to defaults on a credit holding. |
| `income_yield` | `0.05` | Yearly net rental yield on a real estate holding. |
| `config` | `None` | Convert holdings into the run's reporting currency. |

Mixes that change over time use `compute_glidepath()`, ready-made mixes ship as presets (`from_preset()`), and on
history (`backtest()`) the same calls give a backtest. Given several presets, one `Portfolio` holds them all on the
same run, so every read compares them side by side.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Portfolio(
    scenario_set: ScenarioSet,
    config: ScenariosConfig | None = None,
    category_map: dict[str, str] | None = None,
    preset: PortfolioPreset | Sequence[PortfolioPreset] | None = None,
)
```

</details>

## Portfolio.from_preset

Build a Portfolio from one of the ready-made mixes, so you pick a strategy by name instead of typing weights.

Ask for "balanced_60_40" and you get the textbook 60/40 portfolio, with a description of why those weights. The
preset becomes the portfolio's default mix, so `compute()` needs no weights, and a glidepath preset runs as a
glidepath. Fourteen presets ship with the package, among them `balanced_60_40`, `all_weather`,
`bogleheads_three_fund`, `permanent_portfolio` and `target_date_glidepath`;
`list_presets(kind="portfolios")` lists them all. Copy one into a local `portfolios/` folder to make your own;
a local folder wins over the bundled one.

The presets hold factors of the broad factor set (`us_broad`, `united_states_long_rate`, `gold`, ...). On a run
without one of them, `compute()` names the missing factor. A list of presets holds them all on the same run, so
`compute()` gives one value path per preset and the reads compare them row by row.

Also known as: model portfolio, named allocation, strategic asset allocation template.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
Portfolio.from_preset(
    scenario_set: ScenarioSet,
    preset: str | PortfolioPreset | Sequence[str | PortfolioPreset],
    config: ScenariosConfig | None = None,
    portfolios_dir: str | Path = 'portfolios',
    category_map: dict[str, str] | None = None,
) -> 'Portfolio'
```

**Args:**

- <u>scenario_set (ScenarioSet):</u> the run to build the portfolio on.
- <u>preset (str &#124; PortfolioPreset &#124; Sequence[str &#124; PortfolioPreset]):</u> a preset id such as "balanced_60_40" (".yaml" optional), a loaded preset, or a list of either to compare.
- <u>config (ScenariosConfig &#124; None):</u> the run's config, to convert currencies (see the class). Defaults to None.
- <u>portfolios_dir (str &#124; Path):</u> the folder presets are read from; the bundled presets when it does not exist. Defaults to "portfolios".
- <u>category_map (dict[str, str] &#124; None):</u> factor name to category, for a hand-built run. Defaults to None.

**Returns:**

<u>Portfolio:</u> a portfolio whose `compute()` uses the preset's mix, or each listed preset's.

**Raises:**

- <u>FileNotFoundError:</u> if no such preset exists.
- <u>pydantic.ValidationError:</u> if the preset file is invalid, for example weights that don't sum to 1.0.
- <u>ValueError:</u> if a list of presets is empty or names the same preset twice.

</details>

## Portfolio.backtest

Build one or more ready-made mixes on what markets actually did, naming each preset once, so `compute()` is a
backtest.

A backtest asks how a strategy would have done in the past. It fetches the history of exactly the presets'
holdings, lines them up on one calendar and builds the portfolios on it. Every read then works as on simulated
scenarios, with one path instead of thousands: `compute()`, `risk_metrics()`, `factor_exposure()` and
`benchmark()`. One path is one draw from history, so read it as a check on the simulation (does the strategy
behave in the past as the scenarios say it should?), not as a forecast.

Several presets share one calendar: the dates on which every holding of every preset has a price. That makes
the comparison fair, since no mix gets a crisis the others skip, but a holding with a short history (gold,
say) shortens the window for all of them. Each reads one row per preset, and `portfolios` gives each on its
own, with exactly the values of a backtest of that preset alone on the same dates.

Also known as: historical simulation, strategy backtest.

**As an example:**

```python
from financescenarios import Portfolio, Scenarios

scenarios = Scenarios.from_profiles()
portfolio = Portfolio.backtest(scenarios, ["balanced_60_40", "all_weather", "permanent_portfolio"])
portfolio.factor_exposure()
portfolio.compute(initial_value=100_000, rebalance_every=12).plot(levels=True)
```

Which returns (backtested on 2026-10-14, 315 monthly dates from 2000-08-01 to 2026-10-01) one row of factor
loadings per portfolio (see `factor_exposure()`) and one chart with a line per portfolio. Rebalanced yearly,
100,000 grew to 550,844 in the 60/40, 541,700 in All Weather and 555,950 in the Permanent Portfolio: the same
end within 3%, with the 60/40 carrying more than twice the stock market risk of the other two.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
Portfolio.backtest(
    scenarios: 'Scenarios',
    preset: str | PortfolioPreset | Sequence[str | PortfolioPreset],
    period: str = 'monthly',
    portfolios_dir: str | Path = 'portfolios',
) -> 'Portfolio'
```

**Args:**

- <u>scenarios (Scenarios):</u> the `Scenarios` to fetch history through, e.g. `Scenarios.from_profiles()`.
- <u>preset (str &#124; PortfolioPreset &#124; Sequence[str &#124; PortfolioPreset]):</u> a preset id such as "balanced_60_40", a loaded preset, or a list of either to compare.
- <u>period (str):</u> the calendar to line the history up on: "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "monthly".
- <u>portfolios_dir (str &#124; Path):</u> the folder presets are read from; the bundled presets when it does not exist. Defaults to "portfolios".

**Returns:**

<u>Portfolio:</u> the presets' portfolios on history; `compute()` without weights gives the backtest.

**Raises:**

- <u>FileNotFoundError:</u> if no such preset exists.
- <u>ValueError:</u> if `scenarios` has no Finance Toolkit, the holdings share too few dates, or a list of presets is empty or names the same preset twice.
- <u>KeyError:</u> if a holding has no history.

</details>

## Portfolio.preset

The ready-made mix this portfolio uses by default, if it was built with `from_preset()` on one preset; None
otherwise (`presets` lists several).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
portfolio.preset  # property -> PortfolioPreset | None
```

</details>

## Portfolio.presets

Every ready-made mix this portfolio holds: the one preset, each of a list, or none.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
portfolio.presets  # property -> list[PortfolioPreset]
```

</details>

## Portfolio.portfolios

One Portfolio per preset, by the preset's name, all on this same run: the way to read one of several
presets on its own, for example its `weight_drift()` or `withdrawal_success()`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
portfolio.portfolios  # property -> dict[str, 'Portfolio']
```

</details>

## Portfolio.investable_factors

Every factor in this run that a holding can name: its equities, commodities, interest rates, credit and real
estate. Inflation, unemployment and other economic series are left out, since they cannot be held.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
portfolio.investable_factors  # property -> list[str]
```

</details>

## Portfolio.cashflow_rule

Build a recurring deposit or withdrawal from a description in years, such as "deposit 10,000 a year for 15 years".

A positive amount is a deposit, a negative one a withdrawal. Stating it in years keeps a rule meaning the same
whether the run steps monthly, quarterly or yearly; the steps are worked out against this run's own dates. A life
plan is several rules, for example one that saves for 15 years and one that withdraws after that. Pass the rules
to `compute()` as `cashflow_rules`.

`end_year` is included; `years=range(0, 15)` is the Python way, end excluded: years 0 to 14, as `end_year=14`.
`CashflowRule.yearly()` works without a Portfolio.

Also known as: contribution plan, withdrawal plan, savings plan, decumulation schedule.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
cashflow_rule(
    amount: float,
    every_years: float = 1.0,
    start_year: float = 0.0,
    end_year: float | None = None,
    years: range | None = None,
) -> CashflowRule
```

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

</details>

## Portfolio.compute

Build a portfolio from a target weight per factor and see its value in every scenario.

Give it `{"us_broad": 0.6, "united_states_short_rate": 0.4}` to see that 60/40 portfolio's value in every
scenario; without options it is bought once and held. Rebalancing, fees, trading costs and cashflows are the
levers that turn the same market scenarios into a different spread of outcomes for the investor.

Interest rate holdings earn their rate like cash, unless `durations` prices them as a bond fund, which a rate
rise marks down at once ([Redington, 1952](https://doi.org/10.1017/S0020268100052811)). Without a duration a
long-bond holding carries no price risk, so the portfolio looks safer than a real bond fund would be:

```text
return(t) = -duration * (y(t) - y(t-1)) + y(t-1) * dt
```

A bond fund earns the yield at its own maturity, so a short rate given a duration is priced off the US yield
curve at that maturity, or else the same country's long rate, when the run has one (and warns when it has not).
A credit holding earns the government yield its spread sits on plus the spread, as ICE BofA quotes its spreads
over the Treasury curve: the curve at the holding's duration when the run has it, else a long rate of its
currency. Defaults then cost it Moody's average yearly loss for its rating (`portfolio_model.CREDIT_LOSS_RATES`,
0.11% for the investment-grade ICE BofA US Corporate Index, 2.98% for speculative grade), a small share of an
investment-grade spread ([Elton et al., 2001](https://doi.org/10.1111/0022-1082.00324)). A real estate holding
adds a 5% net rental yield to its price growth: 5.49% across 16 countries over 1870-2015
([Jorda et al., 2019](https://doi.org/10.1093/qje/qjz012)) and 4.8% on the NCREIF Property Index in 2025.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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
    base_rates: dict[str, str | None] | None = None,
    default_loss_rate: float | dict[str, float] | None = None,
    income_yield: float | dict[str, float] | None = None,
) -> ScenarioSet
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
- <u>base_rates (dict[str, str &#124; None] &#124; None):</u> per credit holding, the interest rate its spread sits on, or None for the spread alone. Defaults to None, a long rate of the spread's currency, else a short rate.
- <u>default_loss_rate (float &#124; dict[str, float] &#124; None):</u> yearly loss to defaults net of recoveries, flat or per credit holding. Defaults to None, Moody's loss rate for the config's rating, else investment grade.
- <u>income_yield (float &#124; dict[str, float] &#124; None):</u> yearly net rental yield, flat or per real estate holding; 0.0 gives price growth only. Defaults to None, 5%.

**Returns:**

<u>ScenarioSet:</u> a new run with "portfolio" (the total value) and "<factor>_value" (each holding's value). On several presets and no weights, one path per preset named after it, such as "60/40 Balanced".

**Raises:**

- <u>ValueError:</u> if a weight, factor or option is invalid, or there are no weights and no preset.
- <u>KeyError:</u> if a factor is not in this run.

</details>

## Portfolio.compute_glidepath

Build a portfolio whose target mix changes over time, like a target-date fund that starts mostly in equities and
moves into bonds as the target date nears.

Give the weights at a few years (`GlidepathCheckpoint`, each summing to 1.0); in between, the target moves in a
straight line, and before the first and after the last checkpoint it stays flat. Everything else works as in
`compute()`, except that the portfolio must be rebalanced, or it would ignore the moving target.

A glidepath takes risk while the pot is small and time is long, and sheds it as the pot grows and the date
nears, so a late crash hits a portfolio that holds less equity. Compared with a fixed mix of the same average
weight, that narrows the spread of outcomes near the target date at the cost of some upside.

Also known as: lifecycle fund, target-date fund, de-risking path.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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
    base_rates: dict[str, str | None] | None = None,
    default_loss_rate: float | dict[str, float] | None = None,
    income_yield: float | dict[str, float] | None = None,
) -> ScenarioSet
```

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
- <u>base_rates (dict[str, str &#124; None] &#124; None):</u> as in `compute()`. Defaults to None.
- <u>default_loss_rate (float &#124; dict[str, float] &#124; None):</u> as in `compute()`. Defaults to None.
- <u>income_yield (float &#124; dict[str, float] &#124; None):</u> as in `compute()`. Defaults to None.

**Returns:**

<u>ScenarioSet:</u> the same shape as `compute()` returns.

**Raises:**

- <u>ValueError:</u> if no checkpoints are given and there is no glidepath preset, the checkpoints name different factors, `rebalance_every` is below 1, or another input is invalid as in `compute()`.
- <u>KeyError:</u> if a factor, or `inflation_factor`, is not in this run.

</details>

## Portfolio.withdrawal_success

Check whether a plan with withdrawals lasts: how often money is left at the end, when it typically runs out
otherwise, and how much the scenarios that make it end with.

This answers "will my retirement savings last?". A success rate of 0.90 means that in 9 out of 10 market
scenarios the plan pays every withdrawal to the end; the other 10% is the risk of outliving the money, and the
median depletion year says how early that tends to happen. A plan is usually judged against a target rate
(say 85-95%) and adjusted through the spending level, the mix or the retirement date until it clears it. The
survivors' end values show the other side: a high success rate with large leftovers suggests room to spend
more. Without withdrawals nothing runs out and the rate is 1.0; on a historical backtest it is a plain yes or no.

Also known as: retirement success rate, probability of ruin (its complement), safe withdrawal analysis.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
withdrawal_success(portfolio_scenario_set: ScenarioSet | None = None) -> WithdrawalSuccessMetrics
```

**Args:**

- <u>portfolio_scenario_set (ScenarioSet &#124; None):</u> a `compute()` or `compute_glidepath()` result. Defaults to None, the latest one this portfolio computed.

**Returns:**

<u>WithdrawalSuccessMetrics:</u> `success_rate` (share of scenarios with money left at the end), `median_depletion_year` (median year the others run out, None if none do) and `terminal_value_percentiles` (5th to 95th percentile of the final value, over the scenarios that last only).

**Raises:**

- <u>ValueError:</u> if nothing has been computed yet.

</details>

## Portfolio.goal_probability

Find the probability that the portfolio reaches a target value, by a given year or at any point.

This answers "what are the chances I reach one million?", the saving-side counterpart of `withdrawal_success()`.
A probability of 0.6 means 60% of the scenarios get there and 40% fall short: the shortfall risk the saver
carries, which a higher savings rate, a longer horizon or more risk can trade against. Without `target_year` it
counts the scenarios that reach the target at any point and says when they typically get there; with it, the
scenarios at or above the target in that year, which is the stricter test when the money is needed on a date.
Values are nominal; `real_value()` gives today's money.

Also known as: goal-based planning probability, shortfall probability (its complement).

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
goal_probability(
    portfolio_scenario_set: ScenarioSet,
    target_value: float,
    target_year: float | None = None,
) -> GoalProbability
```

**Args:**

- <u>portfolio_scenario_set (ScenarioSet):</u> a `compute()` or `compute_glidepath()` result.
- <u>target_value (float):</u> the value to reach.
- <u>target_year (float &#124; None):</u> the year to check, snapped to the nearest step. Defaults to None, any point in the run.

**Returns:**

<u>GoalProbability:</u> `probability` (share of scenarios that reach the target) and `median_year_reached` (median year they first do; None with `target_year`, or when none do).

**Raises:**

- <u>ValueError:</u> if `target_value` is not positive, or `target_year` falls outside the run.

</details>

## Portfolio.factor_exposure

Measure what this portfolio actually behaved like over history: its loading (Beta) on each of the Fama-French
factors, from a regression of its historical excess returns.

A market Beta of 0.66 means the portfolio moved about 0.66% for every 1% the stock market moved; the others show a
tilt toward small (SMB), cheap (HML), profitable (RMW) or conservative (CMA) companies. R-squared says how much of
its ups and downs these factors explain. It checks whether a mix delivers the exposures it is meant to: a
"balanced" portfolio with a market Beta near 1 is an equity portfolio in disguise, and an unintended value or
size tilt is a bet nobody chose. On several presets it gives one row per preset, over the same dates.

**As an example:**

```python
portfolio = Portfolio.backtest(scenarios, ["balanced_60_40", "all_weather", "permanent_portfolio"])
portfolio.factor_exposure()
```

Which returns, on the default settings and factor set (backtested on 2026-10-14, monthly, 2000-08-01 to
2026-10-01, 312 observations):

| portfolio | Mkt-RF | SMB | HML | RMW | CMA | r_squared |
|:----------|-------:|----:|----:|----:|----:|----------:|
| 60/40 Balanced | 0.5370 | -0.0687 | -0.0450 | 0.1215 | -0.0111 | 0.8616 |
| All Weather | 0.2043 | -0.0621 | -0.1444 | 0.2166 | 0.0344 | 0.1324 |
| Permanent Portfolio | 0.2175 | -0.0615 | -0.1424 | 0.2018 | 0.0479 | 0.1244 |

The 60/40 is mostly a stock market portfolio; the other two hold so much in bonds and gold that the equity
factors explain little more than a tenth of their swings.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
factor_exposure(
    portfolio_scenario_set: ScenarioSet | None = None,
    model: Literal['three_factor', 'five_factor'] = 'five_factor',
) -> pl.DataFrame
```

**Args:**

- <u>portfolio_scenario_set (ScenarioSet &#124; None):</u> a `compute()` result on history. Defaults to None, which computes this portfolio's own mix first.
- <u>model (str):</u> "five_factor" ([Fama and French, 2015](https://doi.org/10.1016/j.jfineco.2014.10.010)) or "three_factor" ([Fama and French, 1993](https://doi.org/10.1016/0304-405X(93)90023-5)). Defaults to "five_factor".

**Returns:**

<u>pl.DataFrame:</u> one row per portfolio with 'portfolio', one column per factor, 'alpha' (the return per period no factor explains), 'r_squared', 'observations' and the 'from' and 'to' dates.

**Raises:**

- <u>ValueError:</u> if the run is simulated scenarios rather than history (more than one path).

</details>

## Portfolio.risk_metrics

Measure how bumpy the ride is and how bad it can get: drawdowns, Value at Risk, volatility, growth rates and the
chance of a loss.

It reports the deepest fall from a previous high in each scenario, the loss in the worst 5% of scenarios, how much
the value swings per year, the yearly growth rate to plan around and the chance of ending below the start, all
counted over the simulated paths. The Expected Shortfall (CVaR) averages the worst 5% instead of taking their edge
([Artzner et al., 1999](https://doi.org/10.1111/1467-9965.00068)). VaR, CVaR and the chance of a loss cover the
whole run, deposits and withdrawals included, so on a 30-year run they describe a 30-year outcome, not a
one-year capital number. The drawdown is often the figure that matters most in practice: it is the paper loss
an investor has to sit through without selling, and for a plan with withdrawals a deep early fall does lasting
damage. On several presets it gives one row per preset: on the backtest of `backtest()`'s example, the 60/40's
deepest fall was 27.8%, All Weather's 21.1% and the Permanent Portfolio's 15.0%.

Also known as: Value at Risk, Expected Shortfall, maximum drawdown.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
risk_metrics(portfolio_scenario_set: ScenarioSet | None = None) -> Any
```

**Args:**

- <u>portfolio_scenario_set (ScenarioSet &#124; None):</u> a `compute()` or `compute_glidepath()` result. Defaults to None, the latest one this portfolio computed.

**Returns:**

<u>PortfolioRiskMetrics:</u> `max_drawdown_percentiles` (worst fall from a high, a negative fraction), `value_at_risk_95` and `conditional_value_at_risk_95` (loss over the whole run, negative for a gain), `annualized_volatility`, `cagr_percentiles` (yearly growth rate) and `probability_of_loss`. On several presets, a pl.DataFrame with one row per portfolio and those figures as columns ("max_drawdown_50", "value_at_risk_95", ...).

**Raises:**

- <u>ValueError:</u> if nothing has been computed yet.

</details>

## Portfolio.real_value

Value the portfolio in today's money at a given year, taking out each scenario's own inflation.

One million in 20 years is not one million of today's money. This divides every scenario's portfolio value by that
same scenario's cumulative inflation, `real value = nominal value / inflation index`, so the answer is in today's
purchasing power and is a range, not one number. It is the mirror image of `compute()`'s `inflation_factor`, which
raises the cashflows going in.

Also known as: inflation-adjusted value, real wealth, purchasing-power value.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
real_value(
    portfolio_scenario_set: ScenarioSet,
    inflation_factor: str,
    year: float,
) -> RealValueSummary
```

**Args:**

- <u>portfolio_scenario_set (ScenarioSet):</u> a `compute()` or `compute_glidepath()` result.
- <u>inflation_factor (str):</u> the simulated inflation to deflate by, such as "united_states_inflation"; it does not need to be a holding.
- <u>year (float):</u> the year to value at, snapped to the nearest step.

**Returns:**

<u>RealValueSummary:</u> `year` (the step actually used), `mean` and `percentiles` (5th to 95th) of the real value.

**Raises:**

- <u>KeyError:</u> if `inflation_factor` is not in this run.
- <u>ValueError:</u> if `year` falls outside the run, or `inflation_factor` is a price rather than a rate.

</details>

## Portfolio.weight_drift

Show how far each holding's weight has wandered from its target, at every step of every scenario.

A 60/40 portfolio is only exactly 60/40 right after a rebalance. In between, and forever in a buy-and-hold
portfolio, the weights wander as one asset outgrows the other: +0.10 means the holding is 10 points above its
target. The target is the one the result was computed with (fixed, or the glidepath's at each step), so no mix is
passed here. A scenario that ran out of money has a drift of 0.

Also known as: allocation drift, weight deviation, tracking to target.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
weight_drift(portfolio_scenario_set: ScenarioSet | None = None) -> dict[str, np.ndarray]
```

**Args:**

- <u>portfolio_scenario_set (ScenarioSet &#124; None):</u> a `compute()` or `compute_glidepath()` result. Defaults to None, the latest one this portfolio computed.

**Returns:**

<u>dict[str, np.ndarray]:</u> factor name to actual minus target weight, one row per scenario and one column per step.

**Raises:**

- <u>ValueError:</u> if nothing has been computed yet, or the result holds no holdings.
- <u>RuntimeError:</u> if the result carries no target weights and this portfolio has computed nothing yet.

</details>

## Portfolio.weight_drift_summary

Sum up how far each holding wandered from its target weight, in one table with one row per holding.

`weight_drift()` gives a number for every step of every scenario; this boils it down to what you usually want
to know. Is the holding above or below its target on average? How far off does it get at worst? And in how many
scenarios does it ever wander past a tolerance, 5 points by default? Left alone, a 60/40 portfolio's equity
holding drifts up as stocks outgrow bonds; rebalanced with `rebalance_band=0.05`, no holding ever passes 5
points, so its share past the threshold is 0. Drift is risk nobody decided to take, so the table helps set a
rebalancing policy: how often, or how wide a band, keeps the portfolio within its mandate.

Also known as: allocation drift report, rebalancing check.

**As an example:**

```python
# portfolio: the Portfolio of compute()'s example (30 yearly steps)
bought_and_held = portfolio.compute({"us_broad": 0.6, "united_states_short_rate": 0.4})
portfolio.weight_drift_summary(bought_and_held)
```

Which returns one row for "us_broad" and one for "united_states_short_rate". The two drift by the same amount
in opposite directions, since the weights always add up to 1.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
weight_drift_summary(
    portfolio_scenario_set: ScenarioSet | None = None,
    threshold: float = 0.05,
) -> pl.DataFrame
```

**Args:**

- <u>portfolio_scenario_set (ScenarioSet &#124; None):</u> a `compute()` or `compute_glidepath()` result. Defaults to None, the latest one this portfolio computed.
- <u>threshold (float):</u> the drift, as a weight, that counts as wandering off. Defaults to 0.05, 5 points.

**Returns:**

<u>pl.DataFrame:</u> one row per holding: "holding", "target_weight" (at the start; a glidepath's target moves), "mean_drift" (over every step and scenario), "max_drift" (the largest drift either way, as a positive number) and "share_past_threshold" (the share of scenarios whose drift ever goes past `threshold`).

**Raises:**

- <u>ValueError:</u> if nothing has been computed yet, or `threshold` is not between 0 and 1.
- <u>RuntimeError:</u> if the run passed is not a `compute()` result and this portfolio has computed nothing yet.

</details>

## Portfolio.summary

Get every read of a computed portfolio in one call: risk, whether the money lasts, and optionally the chance of
reaching a goal and the value after inflation.

Risk (`risk_metrics()`), whether the money lasts (`withdrawal_success()`) and the end value across all
scenarios (`median_end_value`, `percentile(q)`) are always filled in. The real value needs both an
`inflation_factor` and a `real_value_year`, and the goal probability needs a `goal_value`; otherwise they are
None. Together they make the one-page view of a plan: what it may end at, how rough the ride is, whether it
lasts and what it buys after inflation.

Also known as: portfolio report, outcome summary.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
summary(
    portfolio_scenario_set: ScenarioSet | None = None,
    goal_value: float | None = None,
    goal_year: float | None = None,
    inflation_factor: str | None = None,
    real_value_year: float | None = None,
) -> PortfolioSummary
```

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

</details>

## Portfolio.benchmark

Compare this portfolio with another one: how closely it tracks it, how much it moves with it, and whether it grew
faster or earned more per unit of risk.

The benchmark is any portfolio: a market index, another mix on the same run, or the same mix over other dates.
Tracking error is how much the two drift apart per year; correlation and Beta say how much this one moves with
the other (a Beta of 0.6 means 0.6% for every 1% of the benchmark). Relative CAGR and relative Sharpe ratio
([Sharpe, 1966](https://doi.org/10.1086/294846)) are this one's growth rate and return per unit of risk minus the
benchmark's. Active share is the part of the mix that differs
([Cremers and Petajisto, 2009](https://doi.org/10.1093/rfs/hhp057)). The two are compared over the dates they
share. On simulated scenarios tracking error is measured within each scenario and the median reported
(`tracking_error_percentiles` gives its spread), since that is the deviation an investor lives through; the
other figures compare the two average paths. A low tracking error with a
positive relative Sharpe ratio is the case for a mix that stays close to its benchmark while using its risk
better; a large tracking error is risk relative to the benchmark that has to be paid for. A result of several
presets compares each with the benchmark, one row per preset: against SPY on the backtest of `backtest()`'s
example, the 60/40 has a Beta of 0.56 and the Permanent Portfolio 0.22.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
benchmark(
    portfolio_scenario_set: ScenarioSet,
    benchmark_scenario_set: ScenarioSet,
    weights: dict[str, float] | None = None,
    benchmark_weights: dict[str, float] | None = None,
) -> Any
```

**Args:**

- <u>portfolio_scenario_set (ScenarioSet):</u> this portfolio's `compute()` or `compute_glidepath()` result.
- <u>benchmark_scenario_set (ScenarioSet):</u> the result of the portfolio to compare against.
- <u>weights (dict[str, float] &#124; None):</u> this portfolio's target weights, for active share. Defaults to None, the fixed preset's, else the result's own mix.
- <u>benchmark_weights (dict[str, float] &#124; None):</u> the benchmark's target weights. Defaults to None, its result's own mix (none for a glidepath).

**Returns:**

<u>RelativeMetrics:</u> `tracking_error`, `correlation`, `beta`, `relative_cagr`, `relative_sharpe_ratio` and `active_share`. On several presets, a pl.DataFrame with one row per portfolio and those as columns.

**Raises:**

- <u>ValueError:</u> if the two share fewer than two dates, or `weights` is given for several presets.

</details>

## CashflowRule

A recurring deposit (positive `amount`) or withdrawal (negative `amount`), paid every `every` steps from
`start_step` through `end_step` (None runs to the end). `Portfolio.cashflow_rule()` builds one from years instead
of steps; a plan that saves first and withdraws later is two rules.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class CashflowRule(BaseModel):
    amount: float = Field(description='Positive = contribution/inflow, negative = withdrawal/outflow, per occurrence.')
    every: int = Field(ge=1, description='Steps between occurrences.')
    start_step: int = Field(default=0, ge=0)
    end_step: int | None = Field(default=None, ge=0, description='Inclusive. None = through the end of the horizon.')
```

</details>

## CashflowRule.yearly

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

**As an example:**

```python
from financescenarios import CashflowRule

save = CashflowRule.yearly(10_000, years=range(0, 15))
spend = CashflowRule.yearly(-40_000, years=range(15, 31))
```

On a 30-year yearly run, `save` deposits 10,000 in years 0 to 14 and `spend` withdraws 40,000 a year from year
15 through year 30, the last date of the run: the plan of `Portfolio.cashflow_rule()`'s example.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
CashflowRule.yearly(
    amount: float,
    years: range | None = None,
    steps_per_year: int = 1,
) -> 'CashflowRule'
```

**Args:**

- <u>amount (float):</u> the amount each time; positive deposits, negative withdraws.
- <u>years (range &#124; None):</u> the years it is paid, end excluded; the range's step is the gap in years. Defaults to None, every year from the start to the end of the run.
- <u>steps_per_year (int):</u> the run's steps in one year: 1 yearly, 4 quarterly, 12 monthly. Defaults to 1.

**Returns:**

<u>CashflowRule:</u> the rule in steps (`amount`, `every`, `start_step`, `end_step`).

**Raises:**

- <u>ValueError:</u> if `amount` is not a finite number, `steps_per_year` is below 1, or `years` is empty, counts down or starts before year 0.

</details>

## GlidepathCheckpoint

One point on a glidepath: the portfolio's target weights at `year` years from the start, summing to 1.0.
Between two checkpoints the weights move in a straight line; see `Portfolio.compute_glidepath()`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class GlidepathCheckpoint(BaseModel):
    year: float = Field(ge=0)
    weights: dict[str, float] = Field(description='factor name -> target weight at this checkpoint, summing to 1.0.')
```

</details>

## PortfolioSummary

Every read of a computed portfolio in one object, from `Portfolio.summary()`.

`risk` and `withdrawal_success` are always there. `goal_probability` is there when the summary was asked with a
`goal_value`, and `real_value` when it was asked with an inflation factor and a year; otherwise they are None.
`goal()` returns the goal read directly, and raises when no goal was given.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class PortfolioSummary(BaseModel):
    risk: PortfolioRiskMetrics = Field(description='Drawdown/VaR/CVaR/volatility, always computed.')
    withdrawal_success: WithdrawalSuccessMetrics = Field(description='Depletion/survival summary. Well defined for any portfolio: with no withdrawals, nothing depletes and success_rate is 1.0.')
    goal_probability: GoalProbability | None = Field(default=None, description='Set only when a goal value was given.')
    real_value: RealValueSummary | None = Field(default=None, description='Set only when an inflation factor and year were given.')
    end_value_percentiles: dict[str, float] = Field(default_factory=dict, description='5/25/50/75/95th percentile of the last value across every scenario, a scenario that ran out counting as 0. Portfolio.summary() always fills it; empty on a summary built by hand without it.')
```

</details>

## PortfolioSummary.median_end_value

The median portfolio value at the end of the run across all scenarios, the same as `percentile(0.5)`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
portfoliosummary.median_end_value  # property -> float
```

</details>

## PortfolioSummary.percentile

The end value at fraction `q` (0.05, 0.25, 0.5, 0.75 or 0.95) across all scenarios, a scenario that ran out
counting as 0; a ValueError for any other `q`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
percentile(q: float) -> float
```

</details>

## PortfolioSummary.goal

The goal read of a summary asked with a `goal_value`; a ValueError when no goal was given.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
goal() -> GoalProbability
```

</details>

## PortfolioPreset

A ready-made portfolio mix, such as "60/40 Balanced": either fixed weights (`sleeves`) or weights that move over
time (`checkpoints`), exactly one of the two. Each ships as a YAML file under `portfolios/`; pick one with
`Portfolio.from_preset()`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
class PortfolioPreset(BaseModel):
    name: str = Field(min_length=1, description="A short, human-readable label, e.g. '60/40 Balanced'.")
    description: str = Field(default='', description='What this portfolio represents and why these weights were chosen.')
    sleeves: list[PortfolioPresetSleeve] | None = Field(default=None, description='factor -> weight, summing to 1.0. Mutually exclusive with checkpoints.')
    checkpoints: list[GlidepathCheckpoint] | None = Field(default=None, description="The glidepath's waypoints. Mutually exclusive with sleeves.")
    durations: dict[str, float] | None = Field(default=None, description="Bond sleeve -> constant duration in years, so it is priced as a government bond fund rather than rolled as cash (see `Portfolio.compute`'s `durations`). None rolls every rate sleeve as cash.")
```

**Attributes:**

- <u>name (str):</u> a short label, e.g. "60/40 Balanced".
- <u>description (str):</u> what the mix is and why these weights.
- <u>sleeves (list[PortfolioPresetSleeve] &#124; None):</u> factor and weight per holding, summing to 1.0; None for a glidepath.
- <u>checkpoints (list[GlidepathCheckpoint] &#124; None):</u> the glidepath's target weights by year; None for a fixed mix.
- <u>durations (dict[str, float] &#124; None):</u> duration in years per bond holding, so it is priced as a bond fund; None earns every rate like cash.

</details>

## PortfolioPreset.is_glidepath

Whether the mix moves over time (dated checkpoints, run with `compute_glidepath()`) rather than staying
fixed (sleeves, run with `compute()`).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
portfoliopreset.is_glidepath  # property -> bool
```

</details>

## load_portfolio_library

Load every portfolio preset in a folder, keyed by its id: the file name without ".yaml", which is what
`Portfolio.from_preset()` takes. `list_presets(kind="portfolios")` shows the same presets as a table.

**As an example:**

```python
from financescenarios import load_portfolio_library

presets = load_portfolio_library()
presets["all_weather"].description
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
load_portfolio_library(directory: str | Path = 'portfolios') -> dict[str, PortfolioPreset]
```

**Args:**

- <u>directory (str &#124; Path):</u> the portfolios folder; the bundled presets when it does not exist. Defaults to "portfolios".

**Returns:**

<u>dict[str, PortfolioPreset]:</u> every preset by id, in alphabetical order.

**Raises:**

- <u>FileNotFoundError:</u> if the folder does not exist and the package ships none of that name.
- <u>pydantic.ValidationError:</u> if a file is not a valid preset.

</details>

## load_portfolio_preset

Load one portfolio preset by its id, such as "balanced_60_40", following its `extends:` chain if it has one.

`Portfolio.from_preset()` calls this for you. A preset can extend another and change only what differs: the files
in the chain are merged, the extending file winning, the same way as for settings and regimes.

**As an example:**

```python
from financescenarios import load_portfolio_preset

load_portfolio_preset("portfolios", "balanced_60_40").description
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
load_portfolio_preset(directory: str | Path, filename: str) -> PortfolioPreset
```

**Args:**

- <u>directory (str &#124; Path):</u> the portfolios folder; the bundled presets when it does not exist.
- <u>filename (str):</u> the preset's file name, e.g. "balanced_60_40.yaml" (".yaml" optional).

**Returns:**

<u>PortfolioPreset:</u> the preset with its `extends` chain merged in.

**Raises:**

- <u>FileNotFoundError:</u> if the file, or one it extends, does not exist.
- <u>ValueError:</u> if the `extends` chain loops, or no file in it sets `name`.
- <u>pydantic.ValidationError:</u> if the preset is invalid, for example weights that don't sum to 1.0.

</details>

## compute_portfolio_factor_exposure

Measure what kind of investments a portfolio behaves like, by regressing its historical returns on the Fama-French
factors.

The answer is one Beta per factor: how strongly the portfolio moves with the stock market (Mkt-RF, its return above
the risk-free rate), and with small (SMB), cheap (HML), profitable (RMW) and conservatively investing (CMA)
companies. A market Beta of 1.0 means moving one for one with the market; R-squared is the share of the moves the
factors explain. It needs real history, not simulated scenarios, and the factors are US ones.

Read it as a check on what a strategy really holds: the intercept is the return per period the factors do not
explain (alpha), and a low R-squared means the portfolio carries risks these equity factors do not capture, such
as the interest-rate risk of a long bond fund or the currency risk of foreign holdings.

The return above the risk-free rate is regressed with ordinary least squares on the three factors of
[Fama and French (1993)](https://doi.org/10.1016/0304-405X(93)90023-5) or the five of
[Fama and French (2015)](https://doi.org/10.1016/j.jfineco.2014.10.010), from Ken French's
[Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html). Each daily factor
return f_i is compounded over the portfolio's period into F_i; R_p is the portfolio's return over that period, R_f
the risk-free rate's, alpha the intercept and epsilon the residual.

The formula is as follows:
- F_i = prod(1 + f_i) - 1
- R_p - R_f = alpha + sum(beta_i * F_i) + epsilon

Also known as: Fama-French regression, style analysis.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
compute_portfolio_factor_exposure(
    dates: list[date],
    values: list[float],
    model: Literal['three_factor', 'five_factor'] = 'five_factor',
) -> FactorExposureResult
```

**Args:**

- <u>dates (list[date]):</u> the portfolio's dates, oldest first.
- <u>values (list[float]):</u> the portfolio's value at each date.
- <u>model (str):</u> "five_factor" (Mkt-RF, SMB, HML, RMW, CMA) or "three_factor" (Mkt-RF, SMB, HML). Defaults to "five_factor".

**Returns:**

<u>FactorExposureResult:</u> `factors`, `slopes` (one Beta per factor), `intercept` (the return per period no factor explains), `r_squared`, `mean_squared_error` and `n_observations`.

**Raises:**

- <u>ValueError:</u> if `dates` and `values` differ in length, hold fewer than two points, or barely overlap with Ken French's file.

</details>

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

### resolve_glidepath_weights

Interpolate a glidepath's target weight per factor at every date of a run: in a straight line between two
checkpoints, flat at the first checkpoint's weights before it and at the last one's after it.

The formula is as follows:

$$
w_{k}(t) = w_{k}(t_{j}) + (t - t_{j}) / (t_{j} + 1 - t_{j}) \cdot (w_{k}(t_{j} + 1) - w_{k}(t_{j}))
$$

Where t_j and t_j+1 are the checkpoint years either side of t. The weights still sum to 1 at every t, since each
checkpoint's do.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
resolve_glidepath_weights(
    checkpoints: list[GlidepathCheckpoint],
    time_grid: np.ndarray,
) -> dict[str, np.ndarray]
```

**Args:**

- <u>checkpoints (list[GlidepathCheckpoint]):</u> the target weights at chosen years.
- <u>time_grid (np.ndarray):</u> the run's dates, in years from the start.

**Returns:**

<u>dict[str, np.ndarray]:</u> holding name to its target weight at each date.

**Raises:**

- <u>ValueError:</u> if `checkpoints` is empty, two share a year, or they do not all name the same factors.

</details>

### duration_growth_factor

Price a bond fund that keeps a constant duration from a simulated yield or spread: a rise in rates marks it down
at once by about duration times the rise, after which it earns the new, higher yield.

This is a rolling fund (a TLT-style ETF), not one bond held to maturity, so the duration never shortens and the
fund keeps its interest-rate risk for the whole run. A rate holding without a duration instead rolls like a
floating-rate note, with no price effect at all: the difference between holding cash and holding bonds.

The formula is as follows:

$$
r(t) = - D \cdot (y(t) - y(t - \text{dt})) + y(t - \text{dt}) \cdot \text{dt}
$$

$$
G(t) = \exp(r(\text{dt}) + r(2 \cdot \text{dt}) + ... + r(t))
$$

Where D is the modified duration and y the simulated yield. Compounding r as a log return understates a large
one-step loss (a 200bp rise at duration 17 gives exp(-0.34) = 0.71, not 0.66); convexity, missing here, works the
other way. For pricing individual bonds off the whole simulated curve, see `BondPricer`.

**References:**

- Redington, F.M. (1952). "Review of the Principles of Life-Office Valuations." Journal of the Institute of Actuaries, 78(3), 286-340. <https://doi.org/10.1017/S0020268100052811>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
duration_growth_factor(rate_path: np.ndarray, time_step: float, duration: float) -> np.ndarray
```

**Args:**

- <u>rate_path (np.ndarray):</u> the simulated yield or spread per scenario and date, in decimals.
- <u>time_step (float):</u> the years between steps.
- <u>duration (float):</u> the fund's modified duration in years, e.g. about 15 for 20+ year Treasuries or 6 for an aggregate bond index (iShares TLT 14.69 and AGG 5.69 years effective duration on 9 October 2026, ishares.com fund pages); above 0.

**Returns:**

<u>np.ndarray:</u> the fund's growth index per scenario and date, 1.0 at the start.

**Raises:**

- <u>ValueError:</u> if duration is not above 0.

</details>

### credit_growth_factor

Price a corporate bond holding from its simulated credit spread: it earns the government yield plus the spread,
loses a little to defaults each year, and, held as a bond fund, is marked down at once when yields or spreads rise.

A credit spread is not itself a return. A corporate bond investor earns the risk-free yield the spread sits on plus
the spread, less what defaults cost after recoveries. For investment-grade bonds that loss is a small part of the
spread: expected default explains a surprisingly small part of it
([Elton, Gruber, Agrawal and Mann, 2001](https://doi.org/10.1111/0022-1082.00324)), and over 1982-2004 Moody's
investment-grade issuers lost 0.55% of par over five years against 14.88% for speculative grade (Moody's, 2005,
Exhibit 11). Across all ratings since 1866 spreads ran about twice the losses
([Giesecke, Longstaff, Schaefer and Strebulaev, 2011](https://doi.org/10.1016/j.jfineco.2011.01.011)), so taking
half of an investment-grade spread as loss would overstate it several times over. The default is therefore Moody's
loss rate for investment grade, 0.11% a year; pass the rating's rate from `CREDIT_LOSS_RATES` for other bonds.
Without a duration the holding rolls like a floating-rate note and spread moves carry no price effect; with one, a
widening of 1% costs about the duration in percent at once, the main source of losses in a credit sell-off.

The formula is as follows:

$$
y(t) = b(t) + s(t)
$$

$$
r(t) = - D \cdot (y(t) - y(t - \text{dt})) + (y(t - \text{dt}) - L) \cdot \text{dt}
$$

$$
G(t) = \exp(r(\text{dt}) + r(2 \cdot \text{dt}) + ... + r(t))
$$

Where b is the government yield, s the credit spread, D the duration (0 for a floating-rate holding) and L the
yearly default loss net of recoveries. With a constant yield, spread and no losses the holding grows as
exp((b + s) * t).

**As an example:**

```python
import numpy as np

spread = np.full((1, 11), 0.02)
spread[:, 6:] = 0.03  # a one-point widening after five years
growth = credit_growth_factor(spread, 1.0, base_yield=np.full((1, 11), 0.04), duration=6.0, default_loss_rate=0.0)
```

Which returns a growth index that rises by 6.2% a year (4% government yield plus a 2% spread), stands still in the
year the spread widens by one point (its 6% price loss eats that year's carry), then rises by 7.3% a year.

**References:**

- Elton, E.J., Gruber, M.J., Agrawal, D., Mann, C. (2001). "Explaining the Rate Spread on Corporate Bonds." The Journal of Finance, 56(1), 247-277. <https://doi.org/10.1111/0022-1082.00324>
- Giesecke, K., Longstaff, F.A., Schaefer, S., Strebulaev, I. (2011). "Corporate Bond Default Risk: A 150-Year Perspective." Journal of Financial Economics, 102(2), 233-250. <https://doi.org/10.1016/j.jfineco.2011.01.011>
- Moody's Investors Service (2005). "Default and Recovery Rates of Corporate Bond Issuers, 1920-2004." Special Comment, Exhibit 11. <https://www.bu.edu/econ/files/2015/01/Moodys_Default_1920-2004.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
credit_growth_factor(
    spread_path: np.ndarray,
    time_step: float,
    base_yield: np.ndarray | None = None,
    duration: float | None = None,
    default_loss_rate: float | None = None,
) -> np.ndarray
```

**Args:**

- <u>spread_path (np.ndarray):</u> the simulated credit spread per scenario and date, in decimals.
- <u>time_step (float):</u> the years between dates.
- <u>base_yield (np.ndarray &#124; None):</u> the government yield the spread sits on, per scenario and date. Defaults to None, the spread alone: an excess return over government bonds.
- <u>duration (float &#124; None):</u> the bond fund's duration in years. Defaults to None, a floating-rate holding.
- <u>default_loss_rate (float &#124; None):</u> the yearly loss to defaults net of recoveries, e.g. 0.004 for 0.4%. Defaults to None, Moody's investment-grade rate of 0.11% a year (`CREDIT_LOSS_RATES["investment_grade"]`).

**Returns:**

<u>np.ndarray:</u> the holding's growth index per scenario and date, 1.0 at the start.

**Raises:**

- <u>ValueError:</u> if duration is not above 0, or the default loss rate is negative.

</details>

### growth_factor

Turn one factor's simulated path into what one unit invested in it grows to, 1.0 at the start, whether the factor
is a price (a stock index, gold) or a rate (a yield, a credit spread, house-price growth).

Each asset class earns what an investor in it actually earns. A price grows with itself. An interest rate is held
like cash (a floating-rate note earning the rate each step) or, with a duration, as a bond fund that loses value
when yields rise (`duration_growth_factor`). A credit spread earns the government yield it sits on plus the spread
less default losses (`credit_growth_factor`). Real estate earns its price growth plus a net rental yield: rents are
about half of housing's long-run return, 5.49% of 11.22% a year across 16 countries over 1870-2015
([Jorda, Knoll, Kuvshinov, Schularick and Taylor, 2019](https://doi.org/10.1093/qje/qjz012); Table 6 of the
[working paper](https://doi.org/10.24148/wp2017-25)), so leaving them out makes property look like a poor
investment. The 5% default sits between that history and today's 4.8% income return on the NCREIF Property Index.

The formula is as follows:

$$
G(t) = P(t) / P(0)
$$

$$
G(t) = \exp((r(t_{0}) + r(t_{1}) + ... + r(t - \text{dt})) \cdot \text{dt})
$$

$$
G(t) = H(t) / H(0) \cdot \exp(q \cdot t)
$$

The first applies to a price (equities, commodities), the second to an interest rate held as cash and the third
to real estate, where H is the house-price index compounded from the simulated growth rate and q the net rental
yield.

**References:**

- Jorda, O., Knoll, K., Kuvshinov, D., Schularick, M., Taylor, A.M. (2019). "The Rate of Return on Everything, 1870-2015." The Quarterly Journal of Economics, 134(3), 1225-1298. <https://doi.org/10.1093/qje/qjz012>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
growth_factor(
    scenario_set: ScenarioSet,
    factor_name: str,
    factor_type: str,
    reporting: 'Reporting | None' = None,
    duration: float | None = None,
    base_yield: np.ndarray | None = None,
    default_loss_rate: float | None = None,
    income_yield: float | None = None,
) -> np.ndarray
```

**Args:**

- <u>scenario_set (ScenarioSet):</u> the run to read from.
- <u>factor_name (str):</u> the factor to hold.
- <u>factor_type (str):</u> the factor's asset class: equities, commodities, interest_rates, credit or real_estate.
- <u>reporting (Reporting &#124; None):</u> converts a foreign equity, commodity or real estate holding into the reporting currency, so it carries its exchange-rate return. Defaults to None, each factor in its own currency.
- <u>duration (float &#124; None):</u> for a rate or credit holding, the duration of the bond fund it stands for. Defaults to None, held like cash.
- <u>base_yield (np.ndarray &#124; None):</u> for a credit holding, the government yield its spread sits on; for a rate holding with a duration, the yield at that duration to price the fund off instead of the factor itself. Defaults to None.
- <u>default_loss_rate (float &#124; None):</u> for a credit holding, the yearly loss to defaults. Defaults to None, Moody's investment-grade rate of 0.11%.
- <u>income_yield (float &#124; None):</u> for a real estate holding, the yearly net rental yield. Defaults to None, 5%.

**Returns:**

<u>np.ndarray:</u> the growth index per scenario and date, 1.0 at the start.

**Raises:**

- <u>KeyError:</u> if `factor_name` is not in the run.
- <u>ValueError:</u> if `factor_type` is not a sleeve type, `duration` is not above 0, or a yield or loss is invalid.

</details>

### build_cashflow_schedule

Combine deposit and withdrawal rules into one plan: the net amount paid in (+) or taken out (-) at every date.

The formula is as follows:

$$
\operatorname{CF}(t) = a_{1} \cdot I_{1}(t) + a_{2} \cdot I_{2}(t) + ... + a_{R} \cdot I_{R}(t)
$$

Where a_r is rule r's `amount` and I_r(t) is 1 on every `every`-th step from its `start_step` through its
`end_step`, else 0.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
build_cashflow_schedule(n_steps: int, rules: list[CashflowRule]) -> np.ndarray
```

**Args:**

- <u>n_steps (int):</u> the number of steps in the run.
- <u>rules (list[CashflowRule]):</u> the deposits and withdrawals; an empty list gives no cashflows.

**Returns:**

<u>np.ndarray:</u> the net cashflow at each date, 0.0 where nothing is paid.

**Raises:**

- <u>ValueError:</u> if a rule starts or ends outside the run.

</details>

### build_inflation_indexed_cashflow_schedule

Grow a cashflow schedule with each scenario's own inflation, so an amount is read in today's money: a withdrawal
that keeps its purchasing power rather than a fixed sum that inflation erodes.

The formula is as follows:

$$
\text{CF}_{i}(t) = \operatorname{CF}(t) \cdot I_{i}(t)
$$

Where I_i is scenario i's cumulative inflation index, 1 at the start. Because each scenario carries its own
inflation, a high-inflation scenario also has the largest withdrawals, which is exactly the risk a retiree with
fixed real spending runs.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
build_inflation_indexed_cashflow_schedule(
    nominal_schedule: np.ndarray,
    inflation_index: np.ndarray,
) -> np.ndarray
```

**Args:**

- <u>nominal_schedule (np.ndarray):</u> the amount per date in today's money.
- <u>inflation_index (np.ndarray):</u> the cumulative inflation index per scenario and date.

**Returns:**

<u>np.ndarray:</u> the cashflow per scenario and date, in money of the day.

**Raises:**

- <u>ValueError:</u> if the two cover a different number of steps.

</details>

### holding_growth_paths

What each holding earns on its own: its growth index, priced exactly as the portfolio prices it (same reporting
currency, bond duration and fee), but never traded. Rebalancing moves money in and out of a holding, so its value
says little about how the asset did; this index is the asset's own return.

The formula is as follows:

$$
H_{k}(t) = G_{k}(t) / G_{k}(0) \cdot \exp(- f_{k} \cdot t)
$$

Where G_k is holding k's growth index (`growth_factor`), f_k its yearly fee and t the years since the start.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
holding_growth_paths(
    scenario_set: ScenarioSet,
    sleeve_factor_types: dict[str, str],
    reporting: 'Reporting | None' = None,
    durations: dict[str, float] | None = None,
    fee_rate: float | dict[str, float] = 0.0,
    sleeve_growth: dict[str, np.ndarray] | None = None,
) -> dict[str, np.ndarray]
```

**Args:**

- <u>scenario_set (ScenarioSet):</u> the run the portfolio is built on.
- <u>sleeve_factor_types (dict[str, str]):</u> holding name to its asset class.
- <u>reporting (Reporting &#124; None):</u> converts a foreign-currency holding into the reporting currency.
- <u>durations (dict[str, float] &#124; None):</u> the bond fund duration per rate or credit holding.
- <u>fee_rate (float &#124; dict[str, float]):</u> the yearly fee, flat or per holding.
- <u>sleeve_growth (dict[str, np.ndarray] &#124; None):</u> the holdings' growth indices from `sleeve_growth_factors`, when already computed for the portfolio itself; None (the default) computes them here.

**Returns:**

<u>dict[str, np.ndarray]:</u> holding name to its growth index per scenario and date, 1 at the start.

</details>

### compute_portfolio_paths

Combine one or more simulated factors into a weighted portfolio, held buy-and-hold or rebalanced to a fixed mix.

Each holding starts at its weight times `initial_value` and grows with its own asset, net of fees. A rebalance
resets the target weights, selling winners and buying losers (a constant-mix strategy). Deposits buy the target
mix, withdrawals are taken pro rata, and a scenario that runs out of money stays at 0: there is no recovery after
ruin, as for a real retiree.

The formula is as follows:

$$
V_{k}(t) = V_{k}(t - \text{dt}) \cdot G_{k}(t) / G_{k}(t - \text{dt}) \cdot \exp(- f_{k} \cdot \text{dt})
$$

$$
V(t) = V_{1}(t) + V_{2}(t) + ... + V_{K}(t)
$$

$$
\operatorname{turnover}(t) = 1 / 2 \cdot (\operatorname{abs}(w_{1} \cdot V(t) - V_{1}(t)) + ... + \operatorname{abs}(w_{K} \cdot V(t) - V_{K}(t)))
$$

$$
V_{k}(t) = w_{k} \cdot (V(t) - c \cdot \operatorname{turnover}(t)) \text{on}\; a \;\text{rebalance}
$$

Where G_k is holding k's growth index (`growth_factor`), f_k its yearly fee, w_k its target weight and c the
`transaction_cost_rate`; halving the trades counts a sale and its matching buy once.

**References:**

- Perold, A.F., Sharpe, W.F. (1988). "Dynamic Strategies for Asset Allocation." Financial Analysts Journal, 44(1), 16-27. <https://doi.org/10.2469/faj.v44.n1.16>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
compute_portfolio_paths(
    scenario_set: ScenarioSet,
    sleeve_factor_types: dict[str, str],
    weights: dict[str, float],
    initial_value: float = 100.0,
    rebalance_every: int | None = None,
    cashflow_schedule: np.ndarray | None = None,
    fee_rate: float | dict[str, float] = 0.0,
    reporting: 'Reporting | None' = None,
    durations: dict[str, float] | None = None,
    rebalance_band: float | None = None,
    transaction_cost_rate: float = 0.0,
    sleeve_growth: dict[str, np.ndarray] | None = None,
) -> tuple[np.ndarray, dict[str, np.ndarray]]
```

**Args:**

- <u>scenario_set (ScenarioSet):</u> the run the holdings are read from.
- <u>sleeve_factor_types (dict[str, str]):</u> holding name to its asset class.
- <u>weights (dict[str, float]):</u> holding name to target weight, each >= 0, summing to 1.
- <u>initial_value (float):</u> the portfolio's value at the start; 100.0 by default.
- <u>rebalance_every (int &#124; None):</u> steps between rebalances; None (the default) is buy-and-hold.
- <u>cashflow_schedule (np.ndarray &#124; None):</u> the deposit (+) or withdrawal (-) per date, the same in every scenario or one per scenario; None by default.
- <u>fee_rate (float &#124; dict[str, float]):</u> the yearly fee, flat or per holding (0 for any not named); 0.0 by default.
- <u>reporting (Reporting &#124; None):</u> converts holdings into the reporting currency; None by default.
- <u>durations (dict[str, float] &#124; None):</u> the bond fund duration per rate or credit holding; None by default.
- <u>rebalance_band (float &#124; None):</u> the weight drift, e.g. 0.05, that also triggers a rebalance; None by default.
- <u>transaction_cost_rate (float):</u> the cost per unit of one-way turnover on a rebalance; 0.0 by default.
- <u>sleeve_growth (dict[str, np.ndarray] &#124; None):</u> precomputed growth indices (`sleeve_growth_factors`), so the same ones can be reused for `holding_growth_paths`; None (the default) computes them.

**Returns:**

<u>tuple[np.ndarray, dict[str, np.ndarray]]:</u> the portfolio's total value and each holding's value, per scenario and date.

**Raises:**

- <u>ValueError:</u> if the weights name other factors than the holdings, do not sum to 1, or an argument is out of range.
- <u>KeyError:</u> if a factor is not in the run.

</details>

### compute_weight_drift

Actual minus target weight per holding, at every date of every scenario: how far the portfolio has drifted from
its intended allocation since the last rebalance, or since the start for buy-and-hold. Drift is risk nobody chose:
a 60/40 that has drifted to 75/25 carries equity risk its mandate does not allow.

The formula is as follows:

$$
d_{k}(t) = V_{k}(t) / V(t) - w_{k}(t)
$$

Where V_k is holding k's value, V the portfolio's and w_k(t) its target weight: constant for
`compute_portfolio_paths`, from `resolve_glidepath_weights` for a glidepath.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
compute_weight_drift(
    sleeve_values: dict[str, np.ndarray],
    portfolio_value: np.ndarray,
    weight_schedule: dict[str, np.ndarray],
) -> dict[str, np.ndarray]
```

**Args:**

- <u>sleeve_values (dict[str, np.ndarray]):</u> holding name to its value per scenario and date.
- <u>portfolio_value (np.ndarray):</u> the portfolio's total value per scenario and date.
- <u>weight_schedule (dict[str, np.ndarray]):</u> holding name to its target weight at every date.

**Returns:**

<u>dict[str, np.ndarray]:</u> holding name to actual minus target weight per scenario and date; 0.0 once a scenario has run out of money, where a weight means nothing.

</details>

### compute_withdrawal_success_metrics

Summarize a plan with withdrawals across scenarios: how often it lasts the full horizon, when it typically runs
out in the scenarios that don't, and what the survivors end up with. The success rate is the complement of the
probability of ruin; read together with the depletion year it says not just how often a plan fails but how early.

The formula is as follows:

$$
\text{success\_rate} = \operatorname{mean}(1 \left[V_{i}(T) > 0\right])
$$

$$
\tau_{i} = \min(t \;\text{such that}\; V_{i} (t) = 0)
$$

Where V_i is scenario i's value and T the run's end; the median depletion year is the median of tau_i over the
scenarios that ran out, and the percentiles are taken over V_i(T) of those that did not.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
compute_withdrawal_success_metrics(
    portfolio_value: np.ndarray,
    time_grid: np.ndarray,
) -> WithdrawalSuccessMetrics
```

**Args:**

- <u>portfolio_value (np.ndarray):</u> the portfolio's value per scenario and date, withdrawals included.
- <u>time_grid (np.ndarray):</u> the run's dates, in years from the start.

**Returns:**

<u>WithdrawalSuccessMetrics:</u> the success rate, median depletion year and the survivors' end values.

</details>

### compute_goal_probability

The probability that a portfolio reaches a target value, either in a given year or at any point over the run.
Its complement is the shortfall probability: the share of scenarios in which the saver does not get there.

The formula is as follows:

$$
p = \operatorname{mean}(1 \left[V_{i}(s) \geq G\right])
$$

$$
p = \operatorname{mean}(1 \left[\max(V_{i}(0),\; ...,\; V_{i}(T)) \geq G\right])
$$

Where the first applies with `target_year` (s the simulated step nearest to it) and the second without, V_i is
scenario i's value and G the `target_value`. Without a year, the median year reached is the median over the
reaching scenarios of the first step with V_i(t) >= G.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
compute_goal_probability(
    portfolio_value: np.ndarray,
    time_grid: np.ndarray,
    target_value: float,
    target_year: float | None = None,
) -> GoalProbability
```

**Args:**

- <u>portfolio_value (np.ndarray):</u> the portfolio's value per scenario and date.
- <u>time_grid (np.ndarray):</u> the run's dates, in years from the start.
- <u>target_value (float):</u> the value to reach.
- <u>target_year (float &#124; None):</u> the year to check, snapped to the nearest date. Defaults to None, any point in the run.

**Returns:**

<u>GoalProbability:</u> the probability and the median year the target is first reached.

</details>

### compute_real_value

Value a portfolio in today's money at a given year, dividing each scenario's value by that scenario's own
cumulative inflation. The range then reflects how inflation and returns move together in each scenario, which
deflating the nominal median by average inflation would miss.

The formula is as follows:

$$
R_{i}(t) = V_{i}(t) / I_{i}(t)
$$

Where R_i is scenario i's real value, V_i its nominal value and I_i its cumulative inflation index, 1 at the start;
the summary gives the mean and percentiles of R_i across scenarios at the step nearest to `year`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
compute_real_value(
    portfolio_value: np.ndarray,
    time_grid: np.ndarray,
    inflation_index: np.ndarray,
    year: float,
) -> RealValueSummary
```

**Args:**

- <u>portfolio_value (np.ndarray):</u> the portfolio's value per scenario and date.
- <u>time_grid (np.ndarray):</u> the run's dates, in years from the start.
- <u>inflation_index (np.ndarray):</u> the cumulative inflation index per scenario and date, 1.0 at the start.
- <u>year (float):</u> the year to value at, snapped to the nearest date.

**Returns:**

<u>RealValueSummary:</u> the mean and percentiles of the real value.

</details>

{% raw %}
### compute_portfolio_risk_metrics

Summarize a portfolio's risk across scenarios: the worst fall from a high (drawdown), the loss over the whole run in
a bad scenario (VaR and CVaR), the yearly growth rate (CAGR) and the volatility. All are read off the simulated
values themselves, with no assumed return distribution.

The formula is as follows:

$$
\text{DD}_{i} = \min(V_{i}(t) / \max(V_{i}(0),\; ...,\; V_{i}(t)) - 1)
$$

$$
R_{i} = V_{i}(T) / V_{i}(0) - 1
$$

$$
\text{VaR}_{95} = - q_{0.05}(R)
$$

$$
\text{CVaR}_{95} = - \operatorname{mean}(R_{i} \;\text{given}\; R_{i} \leq q_{0.05}(R))
$$

$$
\text{CAGR}_{i} = (1 + R_{i}) ^{1 / T} - 1
$$

$$
\sigma = \operatorname{std}(V(t) / V(t - \text{dt}) - 1) / \sqrt{\text{dt}}
$$

Where V_i is scenario i's value, T the run's length in years, q_0.05 the 5th percentile across scenarios and sigma
pooled over every scenario and step. A scenario that ends at or below 0 has a CAGR of -1.

**References:**

- Artzner, P., Delbaen, F., Eber, J-M., Heath, D. (1999). "Coherent Measures of Risk." Mathematical Finance, 9(3), 203-228. <https://doi.org/10.1111/1467-9965.00068>
- Acerbi, C., Tasche, D. (2002). "On the coherence of expected shortfall." Journal of Banking & Finance, 26(7), 1487-1503. <https://doi.org/10.1016/S0378-4266(02>)00283-2

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
compute_portfolio_risk_metrics(
    portfolio_value: np.ndarray,
    time_grid: np.ndarray,
) -> PortfolioRiskMetrics
```

**Args:**

- <u>portfolio_value (np.ndarray):</u> the portfolio's value per scenario and date.
- <u>time_grid (np.ndarray):</u> the run's dates, in years from the start.

**Returns:**

<u>PortfolioRiskMetrics:</u> the drawdown, VaR, CVaR, volatility, CAGR and probability-of-loss figures.

</details>
{% endraw %}
