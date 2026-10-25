---
title: Risk Metrics
seo_title: "Risk Metrics | Finance Scenarios"
seo_title_suffix: false
excerpt: "How Finance Scenarios measures a portfolio's risk across the scenarios: drawdowns, Value at Risk and Expected Shortfall over the horizon, volatility, growth rates and the chance of reaching a goal or running out of money."
description: "Portfolio risk metrics in Finance Scenarios: maximum drawdown, Value at Risk, Expected Shortfall as a coherent measure, volatility, CAGR, the probability of loss and shortfall, real values, and a 60/40 in a run."
author_profile: false
permalink: /projects/financescenarios/docs/portfolio/risk
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/portfolio
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-portfolio"
---

How much a portfolio earns on average says little about how it gets there. Risk metrics read the whole distribution of paths: how far the value falls from a peak along the way, how bad the bad outcomes are, how bumpy the ride is, and how often the money runs out or a goal is missed. All of them are counted on the simulated paths, not from a formula that assumes normal returns, so fat tails and regime shifts carry through.

## The Metrics

With $$V_i(t)$$ the value of scenario $$i$$ at time $$t$$, cashflows included, and $$T$$ the horizon in years, each metric is:

| Metric | Formula | Question it answers |
|:--|:--|:--|
| Maximum drawdown | $$DD_i = \min_t \Big(\frac{V_i(t)}{\max_{s \le t} V_i(s)} - 1\Big)$$, reported as percentiles across scenarios | How far does the value fall from a peak? |
| Total return | $$R_i = V_i(T)/V_i(0) - 1$$ | What does each scenario end with? |
| Value at Risk (95%) | $$\text{VaR}_{95} = -q_{0.05}(R)$$ | What loss is exceeded in only 5% of scenarios? |
| Expected Shortfall (95%) | $$\text{ES}_{95} = -\mathbb{E}\big[R \mid R \le q_{0.05}(R)\big]$$ | How bad is the average loss in that worst 5%? |
| Annualized volatility | The standard deviation of every step's return $$V_i(t)/V_i(t - \Delta t) - 1$$, pooled over scenarios and steps, over $$\sqrt{\Delta t}$$ | How bumpy is the ride? |
| CAGR | $$\max(1 + R_i, 0)^{1/T} - 1$$, so a scenario that runs out counts as -100% | What growth rate does each scenario compound at? |
| Probability of loss | The share of scenarios with $$R_i < 0$$ | How often does the portfolio end below where it started? |
| Withdrawal success | The share of scenarios with $$V_i(T) > 0$$ | How often does the money last? |
| Goal probability | The share of scenarios with $$\max_t V_i(t) \ge G$$, or $$V_i(t_G) \ge G$$ for a goal year $$t_G$$ | How often is a goal reached, at any point or by a date? |

Expected Shortfall, unlike VaR, is a coherent risk measure: the shortfall of two portfolios combined is never more than the sum of their separate shortfalls ([Artzner, Delbaen, Eber and Heath, 1999](https://doi.org/10.1111/1467-9965.00068){:target="_blank"}; [Acerbi and Tasche, 2002](https://doi.org/10.1016/S0378-4266(02)00283-2){:target="_blank"}). A probability of shortfall is the complement of the last two: one minus the withdrawal success or the goal probability.

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">Read them over the whole horizon</p>

Every metric is computed on the value path, cashflows included, and VaR, Expected Shortfall and the probability of loss describe the total return over the whole horizon: on a 30-year run that is a 30-year outcome, not a one-year loss. With cashflows they mix returns with deposits and withdrawals, and $$V_i(0)$$ is the value after any cashflow at the start.
</div>

All values are nominal unless deflated by each scenario's own price index, $$V_i(t)/I_i(t)$$ with $$I_i(t) = \exp\big(\sum_{s < t}\ln(1 + \pi_{i,s})\,\Delta t\big)$$, which gives the value in today's money. On a 30-year run from the calibration of the [overview](/projects/financescenarios/docs#simulating-scenarios), a saver who starts with 100,000 in 60% US stocks and 40% cash and adds 10,000 a year has 879,624 after 20 years in the median scenario, and 550,965 in today's money.

## Rebalancing against Buy-and-Hold

Rebalancing trades some return for less risk. On the same 30-year run, 60% stocks and 40% cash bought and held against rebalanced yearly with a fee of 0.2%:

<div class="ca-nums fs-nums">
  <span><b>&minus;27.9% &rarr; &minus;23.0%</b>median worst drawdown</span>
  <span><b>9.60% &rarr; 8.19%</b>annualized volatility</span>
  <span><b>7.32% &rarr; 6.74%</b>median CAGR</span>
</div>

The lower drawdown and volatility come at the cost of a lower median CAGR: the buy-and-hold portfolio earns more because it drifts into stocks. With `long_portfolio` on the 30-year run and `weights` holding 60% stocks and 40% cash, as set up in [Rebalancing](/projects/financescenarios/docs/portfolio#rebalancing), to compute both and the saver's value in today's money:

```python
buy_and_hold = long_portfolio.compute(weights, initial_value=100.0)
yearly_fee = long_portfolio.compute(weights, initial_value=100.0, rebalance_every=12, fee_rate=0.002)
long_portfolio.risk_metrics(buy_and_hold)
long_portfolio.risk_metrics(yearly_fee)

saving = long_portfolio.compute(
    weights,
    initial_value=100_000.0,
    rebalance_every=12,
    cashflow_rules=[long_portfolio.cashflow_rule(10_000, every_years=1)],
)
long_portfolio.summary(saving, inflation_factor="united_states_inflation", real_value_year=20)
```

## Examples

The examples below put 100,000 in the 60/40 portfolio of the [Portfolio](/projects/financescenarios/docs/portfolio#a-6040-portfolio) page, rebalanced once a year, on the run from the [overview](/projects/financescenarios/docs#simulating-scenarios): the default settings and factor set, calibrated on 25 October 2026, with 2,000 scenarios and seed 42.

### Risk along the Way

The end value hides the road to it. `risk_metrics` gives the deepest fall from a peak per scenario, the five-year Value at Risk and Expected Shortfall (losses as positive numbers), the yearly volatility and the chance of ending with a loss. To put 100,000 in the 60/40 and calculate them:

```python
from financescenarios import Portfolio, Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
result = scenarios.simulate(n_simulations=2000, seed=42)

portfolio = Portfolio.from_preset(result, preset="balanced_60_40")
values = portfolio.compute(initial_value=100_000, rebalance_every=12)

risk = portfolio.risk_metrics()
```

Which gives a five-year VaR at 95% of 4.82%, so one scenario in twenty loses 4.82% or more of the 100,000, and an Expected Shortfall of 14.78%, the average loss in those scenarios. The yearly volatility is 8.27%, and 6.95% of the scenarios end below 100,000. The falls along the way are deeper: the median scenario drops 11.2% from a peak at some point and one in twenty drops 28.3% or more. When plotted, the deepest fall at five percentiles of the scenarios:

{% include ft-chart.html id="portfolio-drawdown" src="/assets/data/financescenarios-guides/portfolio.json" label="Deepest fall from a peak of the 60/40 portfolio within five years at the 5th, 25th, 50th, 75th and 95th percentile of the scenarios" %}

### Reaching a Goal

`summary` adds the chance of reaching a goal at some point within the run and when it is reached; `goal_year` asks instead whether the value is above the goal on a date. To test a goal of 150,000:

```python
summary = portfolio.summary(goal_value=150_000)

summary.goal_probability
```

Which gives a probability of 47.3% that the 60/40 reaches 150,000 within the five years, after 3.79 years in the median of the scenarios that get there. When plotted, the value after five years across the 2,000 scenarios:

{% include ft-chart.html id="portfolio-end-values" src="/assets/data/financescenarios-guides/portfolio.json" label="Distribution of the value of the 60/40 portfolio after five years, with the goal of 150,000, the median and the 5th percentile" %}

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">2</span></summary>

- Acerbi, C., Tasche, D. (2002). "On the coherence of expected shortfall." Journal of Banking & Finance, 26(7), 1487-1503. [https://doi.org/10.1016/S0378-4266(02)00283-2](https://doi.org/10.1016/S0378-4266(02)00283-2){:target="_blank"}
- Artzner, P., Delbaen, F., Eber, J-M., Heath, D. (1999). "Coherent Measures of Risk." Mathematical Finance, 9(3), 203-228. [https://doi.org/10.1111/1467-9965.00068](https://doi.org/10.1111/1467-9965.00068){:target="_blank"}

</details>

{% include ft-charts-script.html %}
