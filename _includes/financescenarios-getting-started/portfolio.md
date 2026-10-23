## Getting Started

The Portfolio module answers what the scenarios mean for a sum of money. Given target weights, it follows a portfolio's value through every scenario, step by step, with rebalancing, fees, deposits and withdrawals. It never changes the run, so one set of scenarios can test many allocations, and the same calls work on history, so a mix can be checked against what prices actually did.

This section uses the run from the [overview](/projects/financescenarios/docs): the default settings and factor set, calibrated on 19 October 2026, with 2,000 scenarios and seed 42.

### A 60/40 Portfolio

Thirteen ready-made mixes ship with the package, from the textbook 60/40 to Ray Dalio's All Weather, Harry Browne's Permanent Portfolio and a target-date glide path. To list them:

```python
from financescenarios import list_presets

list_presets(kind="portfolios")
```

Which gives, among others:

| id | description |
|:---|:------------|
| all_weather | Ray Dalio's mix: 30% US stocks, 55% Treasuries for his 40% l… |
| balanced_60_40 | The textbook mix: 60% US stocks and 40% US Treasury bonds. |
| bogleheads_three_fund | The Bogleheads' three funds: 40% US stocks, 20% internationa… |
| permanent_portfolio | Harry Browne's four quarters: US stocks, long US Treasuries,… |
| target_date_glidepath | A target-date fund on Vanguard's glide path: 90% stocks unti… |

The 60/40 holds US stocks and US Treasuries, priced as a bond fund with a duration of 5.4 years. To put 100,000 in it, rebalanced once a year:

```python
from financescenarios import Portfolio, Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
result = scenarios.simulate(n_simulations=2000, seed=42)

portfolio = Portfolio.from_preset(result, preset="balanced_60_40")
values = portfolio.compute(initial_value=100_000, rebalance_every=12)

values.describe()
```

Which returns the portfolio's yearly return over the five years and what each holding earned on its own:

| factor | metric | terminal_mean | terminal_q05 | terminal_q95 |
|:-------|:-------|--------------:|-------------:|-------------:|
| portfolio | annualized | 0.0730 | -0.0093 | 0.1465 |
| us_broad_value | annualized | 0.0849 | -0.0569 | 0.2082 |
| united_states_long_rate_value | annualized | 0.0487 | 0.0122 | 0.0784 |

The 60/40 earns 7.30% a year on average, between the stocks' 8.49% and the Treasury fund's 4.87%, and its 90% range of -0.93% to 14.65% a year is far narrower than the stocks' -5.69% to 20.82%. In money, 100,000 grows to 144,923 on average and to 143,349 in the median scenario. To follow the value in money rather than as a return:

```python
values.plot(levels=True)
```

When plotted:

{% include ft-chart.html id="portfolio-value" src="/assets/data/financescenarios-guides/portfolio.json" label="Median, 25-75% and 5-95% band of the value of 100,000 in a 60/40 portfolio rebalanced once a year, over five years" %}

### Risk along the Way

The end value hides the road to it. `risk_metrics` gives the deepest fall from a peak per scenario, the five-year Value at Risk and Conditional Value at Risk (losses as positive numbers), the yearly volatility and the chance of ending with a loss. To calculate them:

```python
risk = portfolio.risk_metrics()
```

Which gives a five-year VaR at 95% of 4.54%, so one scenario in twenty loses 4.54% or more of the 100,000, and a CVaR of 14.36%, the average loss in those scenarios. The yearly volatility is 8.19% and 6.75% of the scenarios end below 100,000. The falls along the way are deeper: the median scenario drops 11.1% from a peak at some point and one in twenty drops 27.9% or more. When plotted, the deepest fall at five percentiles of the scenarios:

{% include ft-chart.html id="portfolio-drawdown" src="/assets/data/financescenarios-guides/portfolio.json" label="Deepest fall from a peak of the 60/40 portfolio within five years at the 5th, 25th, 50th, 75th and 95th percentile of the scenarios" %}

### Reaching a Goal

`summary` adds the chance of reaching a goal and when it is reached. To test a goal of 150,000:

```python
summary = portfolio.summary(goal_value=150_000)

summary.goal_probability
```

Which gives a probability of 47.9%, reached after 3.75 years in the median of the scenarios that get there. When plotted, the value after five years across the 2,000 scenarios:

{% include ft-chart.html id="portfolio-end-values" src="/assets/data/financescenarios-guides/portfolio.json" label="Distribution of the value of the 60/40 portfolio after five years, with the goal of 150,000, the median and the 5th percentile" %}

### A Mix of Your Own

Any variable of the run with a price can be held, at any weight. Bonds are priced from their yield with a duration, a yearly fee comes off the value, and `rebalance_band` trades only when a weight drifts more than that far from its target instead of on a calendar. To hold 50% stocks, 30% Treasuries and 20% gold with a fee of 0.2% a year and a band of 5 points:

```python
custom = portfolio.compute(
    {"us_broad": 0.5, "united_states_long_rate": 0.3, "gold": 0.2},
    initial_value=100_000,
    durations={"united_states_long_rate": 5.4},
    fee_rate=0.002,
    rebalance_band=0.05,
)
custom.describe()
```

Which gives:

| factor | metric | terminal_mean | terminal_q05 | terminal_q95 |
|:-------|:-------|--------------:|-------------:|-------------:|
| portfolio | annualized | 0.0655 | -0.0072 | 0.1350 |
| us_broad_value | annualized | 0.0827 | -0.0587 | 0.2058 |
| united_states_long_rate_value | annualized | 0.0466 | 0.0102 | 0.0762 |
| gold_value | annualized | 0.0287 | -0.1017 | 0.1692 |

After fees the mix returns 6.55% a year on average against 7.30% for the 60/40, and gold is its widest holding, from -10.17% to 16.92% a year. `weight_drift_summary` confirms that the band holds: no weight drifts more than 5.0 points from its target in any scenario.

### Saving and Withdrawing

Deposits and withdrawals are cashflow rules: an amount, how often and from when to when. With withdrawals the order of good and bad years matters, not just the average. To add 5,000 in each of the first two years and withdraw 30,000 a year from year two, first fixed and then indexed to each scenario's own US inflation:

```python
plan = [
    portfolio.cashflow_rule(5_000, every_years=1, start_year=0, end_year=1),
    portfolio.cashflow_rule(-30_000, every_years=1, start_year=2),
]
funded = portfolio.compute(initial_value=100_000, rebalance_every=12, cashflow_rules=plan)
success = portfolio.withdrawal_success()

indexed = portfolio.compute(
    initial_value=100_000, rebalance_every=12, cashflow_rules=plan, inflation_factor="united_states_inflation"
)
success_indexed = portfolio.withdrawal_success()
```

With fixed withdrawals the money lasts the five years in 82.7% of the scenarios, with a median of 28,409 left; indexed to inflation, it lasts in 65.1%, with 22,354 left. When plotted, the value in both plans:

{% include ft-chart.html id="portfolio-withdrawals" src="/assets/data/financescenarios-guides/portfolio.json" label="Median and 5-95% band of the portfolio value with fixed withdrawals and with withdrawals indexed to US inflation, over five years" %}

### A Glidepath

A glidepath moves the weights over time, as a target-date fund does. Checkpoints give the weights at chosen years and the portfolio rebalances towards the line between them. To go from 90% stocks today to 40% in year five, rebalanced monthly:

```python
from financescenarios import GlidepathCheckpoint

checkpoints = [
    GlidepathCheckpoint(year=0, weights={"us_broad": 0.9, "united_states_long_rate": 0.1}),
    GlidepathCheckpoint(year=5, weights={"us_broad": 0.4, "united_states_long_rate": 0.6}),
]
glidepath = portfolio.compute_glidepath(
    checkpoints, initial_value=100_000, rebalance_every=1, durations={"united_states_long_rate": 5.4}
)
glidepath.describe(levels=True)
```

Which gives an average end value of 146,467, while the stocks shrink from 90,000 to 58,587 on average and the Treasuries grow from 10,000 to 87,880. When plotted, the median value of each holding:

{% include ft-chart.html id="portfolio-glidepath" src="/assets/data/financescenarios-guides/portfolio.json" label="Median value of US stocks and US Treasuries in a glidepath from 90% to 40% stocks over five years" %}

### Backtesting against History

`Portfolio.backtest` puts mixes through what their holdings actually did, as one historical scenario per mix, and lines them up on the dates every one of them has a price, so no mix skips a crisis the others go through. Every call above works on it. To backtest three mixes, rebalanced once a year:

```python
backtest = Portfolio.backtest(scenarios, ["balanced_60_40", "all_weather", "permanent_portfolio"])
history = backtest.compute(initial_value=100_000, rebalance_every=12)

backtest.risk_metrics(history)  # one row per mix
history.plot(levels=True)
```

From August 2000 to October 2026, 100,000 grew to 545,709 in the 60/40, 542,561 in All Weather and 555,564 in the Permanent Portfolio, about 6.7% a year each, but on different roads: the deepest falls were 27.8%, 21.1% and 15.0%. When plotted:

{% include ft-chart.html id="portfolio-backtest" src="/assets/data/financescenarios-guides/portfolio.json" label="Value of 100,000 in the 60/40, All Weather and the Permanent Portfolio month by month since August 2000, rebalanced once a year" %}

`factor_exposure` regresses each mix's monthly returns on the five [Fama-French factors](https://doi.org/10.1016/j.jfineco.2014.10.010){:target="_blank"} from [Ken French's data library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html){:target="_blank"}. To calculate it:

```python
backtest.factor_exposure()
```

Which returns:

| portfolio | Mkt-RF | SMB | HML | RMW | CMA | alpha | r_squared | observations |
|:----------|-------:|----:|----:|----:|----:|------:|----------:|-------------:|
| 60/40 Balanced | 0.5369 | -0.0687 | -0.0447 | 0.1215 | -0.0116 | 0.0007 | 0.8615 | 312 |
| All Weather | 0.2039 | -0.0620 | -0.1435 | 0.2162 | 0.0335 | 0.0029 | 0.1318 | 312 |
| Permanent Portfolio | 0.2173 | -0.0615 | -0.1418 | 0.2017 | 0.0473 | 0.0033 | 0.1240 | 312 |

The 60/40 carries a market beta of 0.54, more than twice that of the other two, and the stock market explains 86% of its moves against 13% and 12% of theirs. As a check, the same regression on 100% US stocks gives a beta of 1.00 and an R-squared of 0.99. When plotted:

{% include ft-chart.html id="portfolio-exposure" src="/assets/data/financescenarios-guides/portfolio.json" label="Loadings of the 60/40, All Weather and the Permanent Portfolio on the five Fama-French factors, August 2000 to October 2026" %}

`benchmark` sets each mix against a benchmark on the same dates. To compare the three with holding US stocks only:

```python
stocks_only = backtest.compute({"us_broad": 1.0}, initial_value=100_000, rebalance_every=12)

backtest.benchmark(history, stocks_only, benchmark_weights={"us_broad": 1.0})
```

Which returns:

| portfolio | tracking_error | correlation | beta | relative_cagr | relative_sharpe_ratio | active_share |
|:----------|---------------:|------------:|-----:|--------------:|----------------------:|-------------:|
| 60/40 Balanced | 0.0688 | 0.9725 | 0.5628 | -0.0156 | 0.1854 | 0.4000 |
| All Weather | 0.1365 | 0.4313 | 0.2267 | -0.0158 | 0.2538 | 0.7000 |
| Permanent Portfolio | 0.1329 | 0.4688 | 0.2169 | -0.0149 | 0.3737 | 0.7500 |

Each mix gave up about 1.5 points a year of return against stocks alone and gained in Sharpe ratio, the Permanent Portfolio the most at 0.37.

{% include ft-charts-script.html %}
