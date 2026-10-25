---
title: Portfolio
seo_title: "Portfolio | Finance Scenarios"
seo_title_suffix: false
excerpt: "How Finance Scenarios turns scenarios into the value of a sum of money: target weights followed through every scenario with rebalancing, fees, bond duration, deposits, withdrawals and glidepaths."
description: "Portfolios in Finance Scenarios: what can be held, buy-and-hold against rebalancing and the rebalancing premium, costs, bonds priced by duration, cashflows and sequence risk, glidepaths, and a 60/40 in a run."
author_profile: false
permalink: /projects/financescenarios/docs/portfolio
classes: wide-sidebar
layout: single
redirect_from:
    - /projects/financescenarios/portfolio-notebook
    - /projects/financescenarios/docs/reference/portfolio
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-portfolio"
---

The scenarios say what markets could do; a portfolio says what that means for a sum of money. Given target weights, it follows the value through every scenario, step by step, with rebalancing, fees, deposits and withdrawals, and with weights that can glide over time. It never changes the run, so one set of scenarios can test many allocations, and the same rules run on history as a [backtest](/projects/financescenarios/docs/portfolio/backtests). Measuring how risky each allocation is has a page of its own: [Risk Metrics](/projects/financescenarios/docs/portfolio/risk).

## A 60/40 Portfolio

The examples on this page use the run from the [overview](/projects/financescenarios/docs#simulating-scenarios): the default settings and factor set, calibrated on 25 October 2026, with 2,000 scenarios and seed 42. Thirteen ready-made mixes ship with the package, from the textbook 60/40 to Ray Dalio's All Weather, Harry Browne's Permanent Portfolio and a target-date glidepath. To list them:

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

Which returns the portfolio's annualized return over the five years and what each holding earned on its own:

| factor | metric | terminal_mean | terminal_q05 | terminal_q95 |
|:-------|:-------|--------------:|-------------:|-------------:|
| portfolio | annualized | 0.0721 | -0.0098 | 0.1461 |
| us_broad_value | annualized | 0.0844 | -0.0572 | 0.2076 |
| united_states_long_rate_value | annualized | 0.0470 | 0.0090 | 0.0784 |

The 60/40 earns 7.21% a year on average, between the stocks' 8.44% and the Treasury fund's 4.70%, and its 90% range of -0.98% to 14.61% a year is far narrower than the stocks' -5.72% to 20.76%. In money, 100,000 grows to 144,358 on average and to 142,899 in the median scenario. When plotted, the value over the five years:

{% include ft-chart.html id="portfolio-value" src="/assets/data/financescenarios-guides/portfolio.json" label="Median, 25-75% and 5-95% band of the value of 100,000 in a 60/40 portfolio rebalanced once a year, over five years" %}

## What a Portfolio Can Hold

Only assets you could own can be held, and how a holding grows depends on what it is:

| Kind | Examples | How a holding grows |
|---|---|---|
| Price factors | Equities, commodities | Along the simulated price path. |
| Interest rates | Short and long rates | The rate is compounded like a rolled money-market holding or, with a duration, priced as a bond fund ([below](#bonds-cash-roll-or-duration)). |
| Credit | Spreads by maturity or rating | The government yield the spread sits on, plus the spread, less the yearly default loss for its rating. With a duration, a rise in the spread or in the government yield also marks the holding down at once. |
| Real estate | House-price growth | Price growth plus a 5% net rental yield, accrued continuously (about 5.1% a year compounded). |
| Not investable | Inflation, unemployment, dividend yields, FX | Cannot be held, only used as inputs (for example to index cashflows). |

A spread is not a return. A corporate bond earns the risk-free yield plus the spread, less what defaults cost after recoveries, and for investment grade that loss is a small part of the spread. The default loss is Moody's average five-year credit loss for the holding's rating, net of recoveries, spread evenly over the five years ([Moody's, 2005, Exhibit 11](https://www.bu.edu/econ/files/2015/01/Moodys_Default_1920-2004.pdf){:target="_blank"}): 0.11% a year for investment grade, 2.98% for speculative grade, or a rate you set. The government yield is a long rate in the spread's currency. For a US spread with a duration, when the run has the US yield curve, it is the curve at the holding's duration instead, since spreads are quoted over Treasuries of matching maturity. Without a long rate it falls back to the short rate, and a run without any rate earns the spread less losses, an excess return over government bonds.

Rents are about half of housing's long-run return, so leaving them out makes property look like a poor investment: across 16 countries from 1870 to 2015, rental income averaged 5.50% a year of an 11.05% total return, 5.22% since 1950 and 5.33% in the United States ([Jordà, Knoll, Kuvshinov, Schularick and Taylor, 2019, Tables VIII, IX and A.20](https://doi.org/10.1093/qje/qjz012){:target="_blank"}). The 5% default sits between that history and the 4.8% income return of the NCREIF Property Index over 2025; set your own per holding.

With holdings in several currencies, each equity, commodity and real-estate holding can be converted into the reporting currency first, so a euro equity in a dollar portfolio carries the currency return too. Rates are never converted (see [units](/projects/financescenarios/docs/units)).

## Rebalancing

A portfolio can keep to its weights in three ways:

<div class="ca-cards ca-cards--3">
  <div><i class="ca-icon fas fa-arrow-trend-up" aria-hidden="true"></i><p class="ca-card-title">Buy-and-hold</p><p>Sets the weights once. Each holding then grows with its own asset, so the mix drifts toward whatever performs best. Over a long horizon a 60/40 drifts into a mostly equity portfolio.</p></div>
  <div><i class="ca-icon fas fa-calendar-days" aria-hidden="true"></i><p class="ca-card-title">Calendar rebalancing</p><p>Resets the holdings to target every N steps: the constant-mix discipline of selling what rose and buying what fell (<a href="https://doi.org/10.2469/faj.v44.n1.16" target="_blank">Perold and Sharpe, 1988</a>).</p></div>
  <div><i class="ca-icon fas fa-sliders-h" aria-hidden="true"></i><p class="ca-card-title">Band rebalancing</p><p>Trades only when a holding drifts more than a set distance from its target (say 5 percentage points). Each scenario triggers on its own, so trading happens when markets move, not when the calendar says.</p></div>
</div>

An asset's long-run (geometric) growth rate is lower than its average (arithmetic) return by roughly half its variance:

$$
g \approx \mu - \tfrac{1}{2}\sigma^2
$$

where $$\mu$$ is the arithmetic return per year and $$\sigma$$ the volatility. A constant-mix portfolio suffers the same drag, but on its own variance $$\sigma_p^2$$, which diversification makes smaller than the weighted average of the assets' variances. Its growth rate therefore beats the weighted average of the assets' growth rates by approximately

$$
\tfrac{1}{2}\left(\sum_i w_i \sigma_i^2 - \sigma_p^2\right) \geq 0
$$

with $$w_i$$ the target weights (non-negative, summing to 1) and $$\sigma_i$$ each asset's volatility. That is the rebalancing (or diversification) premium: largest for volatile, weakly correlated assets, and zero only when the assets are perfectly correlated and equally volatile. Buy-and-hold forgoes it but lets winners run, so it keeps more upside when one asset steadily outgrows the others.

That premium is standard portfolio theory, not a separate calculation in the package: it is why the simulated rebalanced and buy-and-hold paths differ. To see it, the same calibration can be simulated 30 years ahead, with 100 in 60% US stocks and 40% cash (the US short rate), bought and held and rebalanced yearly:

```python
from financescenarios import CalibrationResult

long_run = scenarios.simulate(
    calibration=CalibrationResult.load("calibration.json"), years=30, n_simulations=2000, seed=42
)
long_portfolio = Portfolio(long_run)
weights = {"us_broad": 0.6, "united_states_short_rate": 0.4}

buy_and_hold = long_portfolio.compute(weights, initial_value=100.0)
yearly = long_portfolio.compute(weights, initial_value=100.0, rebalance_every=12)
```

After 30 years the two end at:

<div class="ca-nums fs-nums">
  <span><b>206 / 193</b>5th percentile, rebalanced yearly / buy-and-hold</span>
  <span><b>752 / 833</b>median</span>
  <span><b>2,617 / 3,971</b>95th percentile</span>
</div>

Rebalancing lifts the bad outcomes and caps the good ones. Buy-and-hold has the higher median and the far higher 95th percentile because it drifts into stocks: its median scenario holds 83% stocks after 30 years, against the rebalanced 60%. In growth per year, rebalancing is ahead up to the 25th percentile and behind from the median up. When plotted, the growth per year at each percentile of the value after 30 years:

{% include ft-chart.html id="portfolio-rebalancing" src="/assets/data/financescenarios-guides/portfolio-theory.json" label="Growth per year at the 5th to 95th percentile of the value after thirty years of 100 in 60% US stocks and 40% cash, rebalanced yearly and bought and held" %}

### A Mix of Your Own

Any mix of the assets above can be held, with weights that are not negative and sum to one. To hold 50% stocks, 30% Treasuries priced as a bond fund and 20% gold, with a fee of 0.2% a year, rebalanced only when a weight drifts more than 5 points from its target:

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
| portfolio | annualized | 0.0648 | -0.0084 | 0.1343 |
| us_broad_value | annualized | 0.0822 | -0.0591 | 0.2052 |
| united_states_long_rate_value | annualized | 0.0449 | 0.0070 | 0.0762 |
| gold_value | annualized | 0.0287 | -0.1020 | 0.1698 |

After fees the mix returns 6.48% a year on average against 7.21% for the 60/40, and gold has the widest range of its holdings, from -10.20% to 16.98% a year. `weight_drift_summary` confirms that the band holds: no weight drifts more than 5.0 points from its target in any scenario.

## Costs

An annual fee is charged continuously, as $$e^{-f\,\Delta t}$$ per step for a fee rate $$f$$ and a step of $$\Delta t$$ years. It compounds: 1% a year removes about 26% of the final value over 30 years ($$1 - e^{-0.3}$$). Trading costs apply only when a rebalance trades, on the one-way turnover, so frequent rebalancing has to earn its premium net of costs. Each step applies growth net of fees, then any rebalance net of trading costs, then any cashflow. On the 30-year run, to rebalance yearly at a fee of 0.2% a year, or only when a weight drifts 5 points from its target at trading costs of 0.1%:

```python
yearly_fee = long_portfolio.compute(weights, initial_value=100.0, rebalance_every=12, fee_rate=0.002)
banded = long_portfolio.compute(weights, initial_value=100.0, rebalance_band=0.05, transaction_cost_rate=0.001)
```

The fee of 0.2% takes the rebalanced median from 752 to 708.

## Bonds: Cash Roll or Duration

By default a rate holding compounds its yield with no price effect, like a floating-rate note: a rate rise only raises future income. Giving it a duration prices it as a constant-duration bond fund instead, so a rate rise marks it down at once and it then earns the higher yield ([Redington, 1952](https://doi.org/10.1017/S0020268100052811){:target="_blank"}). Each step's return is

$$
r_t = -D\,(y_t - y_{t-1}) + y_{t-1}\,\Delta t
$$

where $$D$$ is the modified duration and $$y$$ the simulated yield: the price effect of the yield change plus the interest earned. The fund rolls to keep its duration constant, like a long-Treasury ETF, rather than aging like a single bond.

A bond fund earns the yield at its own maturity, so $$y$$ should be a long rate, such as the 10-year yield in the default factor set. Three-month bills follow policy rates rather than long yields, so a short rate given a duration is priced off a longer yield: a US short rate off the US yield curve at that duration when the run has the curve, and any other short rate, or a US one without the curve, off the same country's long rate. Only a run with neither prices it off the bill rate itself, with a warning.

<div class="fs-callout fs-callout--limits" markdown="1">
<p class="fs-callout__title">Limits</p>

- This is first-order duration only: convexity is ignored.
- Compounding the return as a log return understates a very large one-step loss.

On monthly or weekly steps both effects are small.
</div>

To hold the US 10-year Treasury as a bond fund with a duration of seven years:

```python
bonds = portfolio.compute({"united_states_long_rate": 1.0}, durations={"united_states_long_rate": 7.0})
```

## Cashflows and Sequence Risk

Deposits and withdrawals turn a return distribution into a plan: save for 15 years, then live off the portfolio. Rules are stated in years, so they mean the same whether the run steps monthly or yearly. A deposit buys the target mix; a withdrawal is taken pro rata. A portfolio that hits zero stays at zero.

With withdrawals, the **order** of returns matters, not only their average. A crash early in the withdrawal phase forces selling at low prices, and the units sold never recover; the same crash late does far less damage. That is sequence-of-returns risk, and why a plan has to be tested on paths rather than on an expected return. Cashflows can be indexed to each scenario's own simulated inflation, deposits and withdrawals alike, so they keep their purchasing power. To start with 100,000 in 60% stocks and 40% cash, save 10,000 a year for 15 years and then withdraw 40,000 a year over 30 years, once fixed and once indexed to US inflation:

```python
rules = [
    long_portfolio.cashflow_rule(10_000, every_years=1, end_year=14),  # save 10,000 a year for 15 years
    long_portfolio.cashflow_rule(-40_000, every_years=1, start_year=15),  # then withdraw 40,000 a year
]
fixed = long_portfolio.compute(weights, initial_value=100_000.0, rebalance_every=12, cashflow_rules=rules)
fixed_success = long_portfolio.withdrawal_success(fixed)

indexed = long_portfolio.compute(
    weights,
    initial_value=100_000.0,
    rebalance_every=12,
    cashflow_rules=rules,
    inflation_factor="united_states_inflation",  # an annual rate (0.024 is 2.4%), not a price index
)
indexed_success = long_portfolio.withdrawal_success(indexed)
```

The money lasts the 30 years in 72.3% of the scenarios with fixed withdrawals and in 43.2% when they rise with inflation; in the scenarios where it runs out, it does so after 25 and 24 years in the median. When plotted, the share of scenarios with money left in each year:

{% include ft-chart.html id="portfolio-plan" src="/assets/data/financescenarios-guides/portfolio-theory.json" label="Share of scenarios in which a portfolio that saves 10,000 a year for 15 years and then withdraws 40,000 a year still holds money, year by year, with withdrawals fixed and indexed to US inflation" %}

## Glidepaths

A target-date or lifecycle plan moves from growth to safety as the target date nears. Target weights are set at a few checkpoints, move in a straight line between them, and the portfolio is rebalanced to the moving target. The `target_date_glidepath` preset follows Vanguard's Target Retirement funds: 90% stocks until 25 years before the target date, 50% at it and 30% seven years after. On the 30-year run, gliding from 90% to 30% stocks ends at a median of 759 from 100, close to the 752 of 60% stocks and 40% cash rebalanced yearly, with more of the risk taken early, when the amount at stake is smallest.

On the five-year run, to go from 90% stocks and 10% Treasuries today to 40% stocks in year five, rebalanced monthly:

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

Which gives an average end value of 146,225, while the stocks shrink from 90,000 to 58,490 on average and the Treasuries grow from 10,000 to 87,735. When plotted, the median value of each holding year by year:

{% include ft-chart.html id="portfolio-glidepath" src="/assets/data/financescenarios-guides/portfolio.json" label="Median value of US stocks and US Treasuries in a glidepath from 90% to 40% stocks over five years" %}

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">4</span></summary>

- Jordà, Ò., Knoll, K., Kuvshinov, D., Schularick, M., Taylor, A.M. (2019). "The Rate of Return on Everything, 1870-2015." Quarterly Journal of Economics, 134(3), 1225-1298. [doi.org](https://doi.org/10.1093/qje/qjz012){:target="_blank"}
- Moody's Investors Service (2005). "Default and Recovery Rates of Corporate Bond Issuers, 1920-2004." Special Comment, Exhibit 11. [bu.edu](https://www.bu.edu/econ/files/2015/01/Moodys_Default_1920-2004.pdf){:target="_blank"}
- Perold, A.F., Sharpe, W.F. (1988). "Dynamic Strategies for Asset Allocation." Financial Analysts Journal, 44(1), 16-27. [https://doi.org/10.2469/faj.v44.n1.16](https://doi.org/10.2469/faj.v44.n1.16){:target="_blank"}
- Redington, F.M. (1952). "Review of the Principles of Life-Office Valuations." Journal of the Institute of Actuaries, 78(3), 286-340. [https://doi.org/10.1017/S0020268100052811](https://doi.org/10.1017/S0020268100052811){:target="_blank"}

</details>

{% include ft-charts-script.html %}
