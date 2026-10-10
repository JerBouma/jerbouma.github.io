---
title: Portfolio
seo_title: Portfolio Documentation – Finance Scenarios
excerpt: "Turn a finished run into the value of an actual portfolio: rebalancing, savings and withdrawals, bond durations, glidepaths, risk reads, benchmarks and backtests."
description: "How Finance Scenarios turns simulated markets into a portfolio's value: rebalancing, cashflows, glidepaths, risk metrics, benchmarks and backtests."
author_profile: false
permalink: /projects/financescenarios/docs/portfolio
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

The scenario generator answers "what could markets do?". The `Portfolio` class answers the next question: "what would that mean for my money?". You pick a weight per asset, say 60% US equities and 40% US government bonds, and it returns how that portfolio's value develops in every simulated scenario, together with the value of each holding on its own. On top of that result it answers plain questions: how likely the money lasts, how likely a goal is reached, what the portfolio is worth after inflation, how deep the drawdowns go and how far the weights drift.

A portfolio reads a finished run. It never calibrates or simulates anything and never changes the `ScenarioSet` it is given. None of its settings are part of the run's [configuration](/projects/financescenarios/docs/configuration): you build a portfolio after the fact, from a run you just simulated or one you saved and read back. The full list of arguments is in the [Portfolio reference](/projects/financescenarios/docs/reference/portfolio).

```python
from financescenarios import Portfolio, Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
scenario_set = scenarios.simulate(years=30)

portfolio = Portfolio(scenario_set)
result = portfolio.compute({"us_broad": 0.6, "united_states_long_rate": 0.4}, initial_value=100.0)
```


The numbers on this page come from one example run: 1,000 scenarios over 30 yearly steps of US stocks (SPY), the US short rate and US inflation, starting 2026-10-01 and simulated on 2026-10-04. They show how the features compare; your own runs will give different numbers.

## What a Portfolio Can Hold

You need to know which factors are investable, because a portfolio only accepts assets you could actually own.

Every factor in a run carries its asset class, stamped on by the simulation and kept when the run is saved, so the run is all a `Portfolio` needs. `portfolio.investable_factors` lists what you can hold. For a `ScenarioSet` you built by hand, pass the `config` that produced it or a `category_map` (factor name to category).

The investable categories split in two:

| Kind | Categories | How a holding grows |
|---|---|---|
| Price factors | `equities`, `commodities` | The simulated price path, rebased to 1.0 at the start. |
| Rate factors | `interest_rates`, `credit`, `real_estate` | The rate is compounded, as the return of a rolled money-market or floating-rate holding. Real estate belongs here because its simulated path is a house-price growth rate. |

Everything else (inflation, unemployment, dividend yields, FX and so on) cannot be held. Allocating to it raises an error that lists the factors you can hold in this run. A strategic allocation and a sector portfolio (several equity factors such as `tech` and `energy`) are the same computation over a different selection.

## Buy-and-Hold and Rebalancing

Rebalancing is the main lever on how a portfolio's risk changes over time, so you choose it explicitly.

Each holding starts at `weight * initial_value`. From there:

- **Buy-and-hold** (`rebalance_every=None`, the default). Each holding grows with its own asset; the weights only hold at the start.
- **Calendar rebalancing** (`rebalance_every=N`). Every N steps each holding is reset to `weight * portfolio value`: the constant-mix discipline of selling what rose and buying what fell ([Perold and Sharpe, 1988](https://doi.org/10.2469/faj.v44.n1.16){:target="_blank"}). `rebalance_every=1` rebalances every step.
- **Band rebalancing** (`rebalance_band=X`). A scenario rebalances as soon as any holding's actual weight is more than X away from its target, in absolute terms (0.05 means 5 percentage points). Each scenario triggers on its own. Combined with a calendar, whichever fires first wins.

Two kinds of cost apply:

- **`fee_rate`** is an annual fee on assets, charged every step as `exp(-fee_rate * dt)`, where `dt` is that step's length in years. It can be one number for every holding or a dict with a rate per holding (unnamed holdings pay nothing).
- **`transaction_cost_rate`** is charged only when a rebalance trades, on the one-way turnover `0.5 * sum(|target value - actual value|)`. Buying one holding and selling another counts as one trade, not two.

Each step applies growth (net of the fee), then any rebalance (net of trading costs), then any cashflow.

```python
weights = {"us_broad": 0.6, "united_states_short_rate": 0.4}

buy_and_hold = portfolio.compute(weights, initial_value=100.0)
rebalanced = portfolio.compute(weights, initial_value=100.0, rebalance_every=1, fee_rate=0.002)
banded = portfolio.compute(weights, initial_value=100.0, rebalance_band=0.05, transaction_cost_rate=0.001)
```

On a run of 1,000 scenarios over 30 yearly steps, the first two portfolios ended at almost the same 5th percentile (about 426 from 100). The buy-and-hold one drifts toward equities as they outgrow the short rate, so its 95th percentile was far higher (5,925 against 2,996), at the cost of more risk.

## Saving and Withdrawing

Cashflows let you test a real plan, such as saving for 15 years and then living off the portfolio.

A cashflow rule is a recurring deposit (positive amount) or withdrawal (negative amount). `portfolio.cashflow_rule()` builds one from a description in years, so a rule means the same thing whether the run steps monthly, quarterly or yearly. A life plan is several rules, one per phase:

```python
rules = [
    portfolio.cashflow_rule(10_000, every_years=1, end_year=14),     # save 10,000 a year for 15 years
    portfolio.cashflow_rule(-40_000, every_years=1, start_year=15),  # then withdraw 40,000 a year
]
plan = portfolio.compute(
    weights,
    initial_value=100_000.0,
    rebalance_every=1,
    cashflow_rules=rules,
    inflation_factor="united_states_inflation",
)
```

How the rules behave:

- `every_years` is rounded to whole steps, never less than one. A cadence finer than the run (monthly cashflows on a yearly run) fires once per step without scaling the amount up; a warning tells you so.
- `start_year` and `end_year` snap to the nearest step; a year outside the run raises an error.
- A contribution buys the target mix; a withdrawal is taken from each holding in proportion to what it holds.
- If the portfolio's value reaches zero or less, it is set to exactly 0.0 and stays there. A ruined portfolio receives no further contributions.

**Inflation-indexed cashflows.** With `inflation_factor`, every amount is read in today's money: the schedule is multiplied by each scenario's own cumulative inflation, so a 40,000 withdrawal keeps its purchasing power in every scenario. The inflation factor need not be a holding, and it must be an annualized decimal rate (0.024 means 2.4%), not a price index. An average above 50% a year triggers a warning about a likely units mistake, but nothing is rescaled, since genuine hyperinflation looks the same.

The indexing matters. In the example run (100,000 to start, 10,000 a year saved for 15 years, then 40,000 a year withdrawn), the money lasted 30 years in 91.7% of scenarios with a fixed nominal withdrawal, and in 58% when the withdrawal rose with inflation.

## Bonds: Cash Roll or Duration

This setting decides whether a rate rise hurts your bond holding today or only helps it later, which changes short-term risk materially.

By default an interest-rate or credit holding compounds its rate with no price effect, like a floating-rate note or a money-market fund. A rate spike only raises future growth.

With `durations` (factor name to a duration in years, for interest-rate and credit holdings only), the holding is priced as a constant-duration bond fund. Each step's return is

```
return(t) = -duration * (y(t) - y(t-1)) + y(t-1) * dt
```

the price effect of the yield change plus the interest earned. A rate rise marks the holding down by roughly `duration * rise` at once, after which it earns the higher yield ([Redington, 1952](https://doi.org/10.1017/S0020268100052811){:target="_blank"}). This is a rolling fund whose duration stays constant, like a long-Treasury ETF, not a single bond ageing towards maturity.

```python
bonds = portfolio.compute({"united_states_short_rate": 1.0}, durations={"united_states_short_rate": 7.0})
```

In the example run, the floating-rate roll earned the starting 4.0% in year one in every scenario. At duration 7, the same position ranged from 96.32 to 111.72 (5th to 95th percentile) after one year, with a median worst drawdown of 7.0% against none for the roll.

Two approximations to keep in mind:

- The return is compounded as if it were a log return, which understates a very large one-step loss. A 2-point rate spike at duration 17 gives `exp(-0.32) = 0.73` instead of `0.68`. For the small steps of a monthly or weekly run the difference is negligible.
- Convexity is ignored: this is first-order duration only. Full curve-based bond pricing is not wired into the portfolio.

## Several Currencies

If you hold assets in more than one currency, pass the run's `config` so returns are measured in one currency.

With `Portfolio(scenario_set, config=config)`, each equity, commodity and real-estate holding is converted into the run's reporting currency before it is weighted, so a euro equity in a dollar portfolio carries the euro/dollar return too. Rate factors are never converted, since a percentage has no currency. Without `config`, holdings are combined in their native units. See [units](/projects/financescenarios/docs/units).

## What the Result Holds

`compute()` returns a new `ScenarioSet` with the same dates, number of scenarios and seed as the run. It holds a `"portfolio"` path and one `"<factor>_value"` path per holding, so every `ScenarioSet` method (`describe()`, `to_dataframe()`, `summary_statistics()`, `plot()`) works on it. See the [ScenarioSet reference](/projects/financescenarios/docs/reference/scenario-set).

A holding's path is the money in it, which rebalancing moves in and out. Its returns are read from the holding's own growth index instead, priced the same way (currency, duration, fee) but never traded, so they show what the holding itself earned.

## Glidepaths

A glidepath lets you model a target-date or lifecycle plan, where the mix moves from growth to safety as the target date nears.

You give the target weights at a few years with `GlidepathCheckpoint(year, weights)`, each summing to 1.0. Between checkpoints the weights move in a straight line; before the first and after the last they stay flat.

```python
from financescenarios import GlidepathCheckpoint

glide = portfolio.compute_glidepath(
    [
        GlidepathCheckpoint(year=0, weights={"us_broad": 0.9, "united_states_short_rate": 0.1}),
        GlidepathCheckpoint(year=30, weights={"us_broad": 0.3, "united_states_short_rate": 0.7}),
    ],
    initial_value=100.0,
)
```

Rebalancing, cashflows, fees, trading costs and durations work exactly as in `compute()`. Two differences:

- The portfolio must be rebalanced (`rebalance_every` cannot be `None`), or it would ignore the moving target. The default is every step.
- Every checkpoint must name exactly the same factors.

In the example run, gliding from 90% to 30% equities over 30 years ended at a median of 1,210, close to a yearly rebalanced 60/40's 1,183 on the same run, with more of the risk taken early.

## Ready-Made Portfolios

Presets let you start from a well-known allocation by name instead of typing weights.

Fourteen presets ship with the package: `all_weather`, `balanced_60_40`, `barbell`, `bogleheads_three_fund`, `buffett_90_10`, `conservative_income`, `endowment_model` (which uses the `private_markets` factor set), `global_60_40`, `global_equity_growth`, `golden_butterfly`, `permanent_portfolio`, `small_cap_value_tilt`, `target_date_glidepath` (the one glidepath) and `us_equity_sectors`. `list_presets(kind="portfolios")` lists them.

```python
portfolio = Portfolio.from_preset(scenario_set, preset="balanced_60_40")
result = portfolio.compute()  # no weights needed: the preset's mix is the default
```

A glidepath preset runs through `compute_glidepath()`. The presets name factors from the broad factor set, such as `us_broad`, `united_states_long_rate` and `gold`; on a run without one of them, `compute()` names the missing factor.

A preset is a small YAML file with a `name`, a `description` and either `sleeves` (a fixed mix) or `checkpoints` (a glidepath), plus optional `durations` for its bond holdings. The 60/40 preset holds 60% `us_broad` and 40% `united_states_long_rate` at a duration of 5.4 years. To make your own, copy one into a local `portfolios/` folder, which wins over the bundled copy; `extends:` works as for [regimes](/projects/financescenarios/docs/regimes).

## Reading the Result

Each read answers one question a client, trustee or board would ask.

### Will the Money Last?

`withdrawal_success()` tests a spending plan.

| Field | Meaning |
|---|---|
| `success_rate` | Share of scenarios with money left at the end. Since a depleted portfolio stays at 0.0, the final step tells whether a scenario ever ran out. |
| `median_depletion_year` | Among scenarios that ran out, the median year they first hit zero. `None` if none did. |
| `terminal_value_percentiles` | 5th to 95th percentile of the final value over the surviving scenarios only, so failures do not drag it down. |

Without withdrawals nothing runs out and `success_rate` is 1.0.

### Will I Reach My Goal?

`goal_probability(result, target_value, target_year=None)` answers "what are the chances I reach one million?".

- Without `target_year`, `probability` is the share of scenarios that reach the target at any point, and `median_year_reached` is when they typically get there.
- With `target_year`, it is the share at or above the target in the step nearest that year, and `median_year_reached` is `None`.

Values are nominal.

### What Is It Worth in Today's Money?

`real_value(result, inflation_factor, year)` divides each scenario's portfolio value by that same scenario's cumulative inflation: `real_value(t) = nominal_value(t) / inflation_index(t)`. The result is a distribution: the `year` actually used (snapped to the nearest step), the `mean` and the 5th to 95th `percentiles`. In the example run a saver's median portfolio was worth 1,064,686 in nominal terms after 20 years and 636,645 in today's money.

### How Bumpy Is the Ride?

`risk_metrics()` counts everything over the simulated paths themselves, not from a formula that assumes returns follow a particular distribution.

| Field | Meaning |
|---|---|
| `max_drawdown_percentiles` | Percentiles across scenarios of each scenario's worst peak-to-trough fall, as a negative fraction. |
| `value_at_risk_95` | The total-return loss over the whole horizon that 95% of scenarios do not exceed. A negative number means even the worst 5% gained. |
| `conditional_value_at_risk_95` | The average loss in the worst 5% of scenarios, the Expected Shortfall ([Artzner et al., 1999](https://doi.org/10.1111/1467-9965.00068){:target="_blank"}; [Acerbi and Tasche, 2002](https://doi.org/10.1016/S0378-4266(02)00283-2){:target="_blank"}). |
| `annualized_volatility` | Standard deviation of per-step returns, pooled over all scenarios and steps and annualized. One figure for the whole horizon. |
| `cagr_percentiles` | Percentiles of each scenario's compound annual growth rate, `(final / initial) ** (1 / years) - 1`. A scenario ending at or below zero counts as -1.0. |
| `probability_of_loss` | Share of scenarios ending below their starting value, in nominal terms. |

VaR, CVaR and the loss probability describe the total return over the whole horizon: on a 30-year run, a 30-year outcome, not a one-year loss. With cashflows, the figures mix returns with deposits and withdrawals.

In the example run, rebalancing the 60/40 yearly with a 0.2% fee lowered the median worst drawdown from -23.84% to -17.25% and the annualized volatility from 13.21% to 10.45%, at the cost of a lower median CAGR (8.37% against 9.28%).

### How Far Do the Weights Drift?

`weight_drift()` returns actual minus target weight per holding, for every scenario and step, as raw arrays you summarize yourself. A ruined scenario has drift 0.0. For the buy-and-hold 60/40 in the example run, the equity holding's median drift grew to +0.29 after 30 years.

### Everything at Once

`summary()` returns a `PortfolioSummary` with `risk` and `withdrawal_success` always filled in. `goal_probability` needs a `goal_value`, and `real_value` needs both an `inflation_factor` and a `real_value_year`; otherwise they are `None`.

```python
summary = portfolio.summary(
    plan, goal_value=1_000_000.0, inflation_factor="united_states_inflation", real_value_year=20
)
```

## Comparing With a Benchmark

Use `benchmark()` when the question is relative: does this mix track, beat or lag another one?

The benchmark is any other portfolio: a market index holding, a different mix on the same run, or the same mix over other dates. Over the dates both share, `benchmark(result, benchmark_result)` returns:

| Field | Meaning |
|---|---|
| `tracking_error` | Annualized standard deviation of the return difference. |
| `correlation`, `beta` | How much this portfolio moves with the benchmark (Beta is covariance over benchmark variance). |
| `relative_cagr`, `relative_sharpe_ratio` | This portfolio's figure minus the benchmark's; positive means ahead ([Sharpe, 1966](https://doi.org/10.1086/294846){:target="_blank"}). |
| `active_share` | Half the sum of the absolute weight differences per factor ([Cremers and Petajisto, 2009](https://doi.org/10.1093/rfs/hhp057){:target="_blank"}). `None` unless both sets of weights are known. |

On a simulated run, both sides are first reduced to their mean path across scenarios, so tracking error and the Sharpe difference describe the two average paths, not the risk inside any one scenario. On a historical backtest they mean what they usually mean.

Two backtests can cover different dates, since a holding with less history shortens its portfolio's window; the comparison uses the shared dates.

## Backtesting Against History

A backtest shows what an allocation actually would have done, using the same rebalancing, cashflow and fee rules as the simulation.

`Scenarios.history()` puts realized history into a `ScenarioSet` with a single path. No calibration or simulation is involved.

```python
history = scenarios.history(portfolio="balanced_60_40", period="monthly")
backtest = Portfolio.from_preset(history, preset="balanced_60_40").compute(rebalance_every=12)
```

How the series are lined up:

- Each factor is resampled onto one common calendar (`period`: daily, weekly, monthly, quarterly or yearly) by taking the last observation in each period. Each date is labeled with the start of its period.
- Only dates on which every factor has a value are kept. A factor published less often than `period` leaves gaps that drop out rather than being forward-filled, so pick `period` to match the least frequent holding.

With one path, every statistic across scenarios (VaR, CVaR, percentiles, `success_rate`) collapses to one number, while path-based reads such as CAGR, volatility, drawdown and factor exposure stay fully meaningful. The [history and metrics reference](/projects/financescenarios/docs/reference/history-and-metrics) covers `fetch_historical_data()` and `build_synthetic_scenario_set()` if you want to build the backtest yourself.

## Factor Exposure

Factor exposure tells you what kind of investments a backtested portfolio behaved like, which is useful for checking a mandate or explaining performance.

`factor_exposure()` regresses the portfolio's excess return (its return minus the risk-free rate) on the Fama-French factors with ordinary least squares:

```
Excess Return = Intercept + sum(Beta_i * Factor_i) + Residual
```

using the three-factor model of [Fama and French (1993)](https://doi.org/10.1016/0304-405X(93)90023-5){:target="_blank"} or the five-factor model of [Fama and French (2015)](https://doi.org/10.1016/j.jfineco.2014.10.010){:target="_blank"} (the default). The Betas measure co-movement with the market above the risk-free rate (Mkt-RF), small versus large companies (SMB), cheap versus expensive (HML), profitable versus unprofitable (RMW) and conservative versus aggressive investors (CMA). The regression is the Finance Toolkit's, with factor data from Kenneth French's [Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html){:target="_blank"}.

```python
exposure = Portfolio.from_preset(history, preset="balanced_60_40").factor_exposure(model="five_factor")
```

The result holds the `factors`, the `intercept` (the average excess return per period the factors do not explain), the `slopes` (one Beta per factor), `r_squared`, `mean_squared_error` and `n_observations`.

The factor file is daily, so each portfolio return is matched against the factor returns compounded over the same window, on any backtest calendar.

On monthly history from 2004-01 to 2026-10, 100% SPY showed a market Beta of 0.997 and an R-squared of 0.996, with a slight large-company tilt (SMB -0.12). A 60/40 of SPY and the US short rate, rebalanced every 12 months, showed a market Beta of 0.594, close to its equity weight.

Caveats:

- Only meaningful for realized returns. A simulated scenario has no calendar to line up with real factor history.
- The French data is not always fully up to date, so the latest dates can fall outside it. Too little overlap raises an error.
- The factors are US equity factors. A non-US portfolio's Betas describe its co-movement with the US market, not its own market's style.
- The three-factor and five-factor files build SMB differently, so the two models give slightly different size Betas.

## Charts

Two charts show what happens inside the portfolio; the [plotting page](/projects/financescenarios/docs/plotting) covers charts in general.

- `plot_sleeve_values(result)`, or `result.plot(kind="sleeves")`, draws the median value of each holding as a stacked area. The median is taken per holding, so the stack shows a typical make-up rather than any single scenario, and the layers need not add up to the median portfolio value. Past eight holdings, the rest are grouped as "Other".
- `plot_weight_drift(result, portfolio.weight_drift(result))` draws each holding's median drift from its target around a zero line, in the same colors.

`result.plot()` draws the portfolio's fan chart.

## Performance Metrics for One Path

For a classic performance report on one value path, such as a percentile band or a backtest, `compute_price_performance_metrics(values, time_grid)` returns growth, volatility, Sharpe and Sortino ratios, drawdowns and Value-at-Risk.

- The path must stay above zero. One that starts at or below zero (a holding with no weight at the start of a glidepath) or has fewer than two dates returns NaN for every field. A single ratio can also be NaN, such as the Calmar ratio of a path that never falls.
- Ratios and volatility are annualized from the spacing of `time_grid`, assumed even.
- Its Value-at-Risk is the tail of one path's own returns over time. `compute_factor_metrics()` instead measures the spread of end-of-run outcomes across scenarios, which suits factors like interest rates that can cross zero.

## References

- Acerbi, C., Tasche, D. (2002). "On the coherence of expected shortfall." Journal of Banking & Finance, 26(7), 1487-1503. [https://doi.org/10.1016/S0378-4266(02)00283-2](https://doi.org/10.1016/S0378-4266(02)00283-2){:target="_blank"}
- Artzner, P., Delbaen, F., Eber, J-M., Heath, D. (1999). "Coherent Measures of Risk." Mathematical Finance, 9(3), 203-228. [https://doi.org/10.1111/1467-9965.00068](https://doi.org/10.1111/1467-9965.00068){:target="_blank"}
- Cremers, K.J.M., Petajisto, A. (2009). "How Active Is Your Fund Manager? A New Measure That Predicts Performance." Review of Financial Studies, 22(9), 3329-3365. [https://doi.org/10.1093/rfs/hhp057](https://doi.org/10.1093/rfs/hhp057){:target="_blank"}
- Fama, E.F., French, K.R. (1993). "Common risk factors in the returns on stocks and bonds." Journal of Financial Economics, 33(1), 3-56. [https://doi.org/10.1016/0304-405X(93)90023-5](https://doi.org/10.1016/0304-405X(93)90023-5){:target="_blank"}
- Fama, E.F., French, K.R. (2015). "A five-factor asset pricing model." Journal of Financial Economics, 116(1), 1-22. [https://doi.org/10.1016/j.jfineco.2014.10.010](https://doi.org/10.1016/j.jfineco.2014.10.010){:target="_blank"}
- French, K.R. "Data Library." Tuck School of Business at Dartmouth. [https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html){:target="_blank"}
- Perold, A.F., Sharpe, W.F. (1988). "Dynamic Strategies for Asset Allocation." Financial Analysts Journal, 44(1), 16-27. [https://doi.org/10.2469/faj.v44.n1.16](https://doi.org/10.2469/faj.v44.n1.16){:target="_blank"}
- Redington, F.M. (1952). "Review of the Principles of Life-Office Valuations." Journal of the Institute of Actuaries, 78(3), 286-340. [https://doi.org/10.1017/S0020268100052811](https://doi.org/10.1017/S0020268100052811){:target="_blank"}
- Sharpe, W.F. (1966). "Mutual Fund Performance." The Journal of Business, 39(S1), 119-138. [https://doi.org/10.1086/294846](https://doi.org/10.1086/294846){:target="_blank"}
