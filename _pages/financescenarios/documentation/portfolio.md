---
title: Portfolio
seo_title: "Portfolio Documentation | Finance Scenarios"
seo_title_suffix: false
excerpt: "How simulated returns become the value of a real portfolio: rebalancing and the rebalancing premium, cashflows and sequence risk, glidepaths, fees, risk metrics, backtests and factor exposure."
description: "From scenario returns to portfolio value: rebalancing, cashflows and sequence risk, glidepaths, fees, VaR and Expected Shortfall, backtests and factor exposure."
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

The scenario generator answers "what could markets do?". A portfolio answers "what would that mean for this money?": given target weights, it follows the portfolio's value through every scenario, applying rebalancing, fees, deposits and withdrawals step by step. It never changes the run, so one set of scenarios can test many allocations.

```python
from financescenarios import Portfolio, Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
scenario_set = scenarios.simulate(years=30)

portfolio = Portfolio(scenario_set)
result = portfolio.compute({"us_broad": 0.6, "united_states_short_rate": 0.4}, initial_value=100.0)
```

The numbers on this page come from one example run: 1,000 scenarios over 30 yearly steps of US stocks (SPY), the US short rate and US inflation, starting 2026-10-01 and simulated on 2026-10-04. Its "60/40" is 60% equities and 40% cash (the short rate); the 60/40 preset [below](#glidepaths) holds Treasuries instead. They show how the choices compare; other runs give other numbers. Every option is listed in the [Portfolio reference](/projects/financescenarios/docs/reference/portfolio).

<div class="ca-nav">
  <a href="#what-a-portfolio-can-hold"><i class="fas fa-layer-group" aria-hidden="true"></i>Holdings</a>
  <a href="#buy-and-hold-versus-rebalancing"><i class="fas fa-scale-balanced" aria-hidden="true"></i>Rebalancing</a>
  <a href="#cashflows-and-sequence-risk"><i class="fas fa-coins" aria-hidden="true"></i>Cashflows</a>
  <a href="#bonds-cash-roll-or-duration"><i class="fas fa-landmark" aria-hidden="true"></i>Bonds</a>
  <a href="#glidepaths"><i class="fas fa-arrow-trend-down" aria-hidden="true"></i>Glidepaths</a>
  <a href="#risk-metrics"><i class="fas fa-gauge-high" aria-hidden="true"></i>Risk metrics</a>
  <a href="#benchmarks-and-backtests"><i class="fas fa-history" aria-hidden="true"></i>Backtests</a>
  <a href="#factor-exposure"><i class="fas fa-magnifying-glass" aria-hidden="true"></i>Factor exposure</a>
</div>

## What a Portfolio Can Hold

Only assets you could own can be held, and how a holding grows depends on what it is:

| Kind | Examples | How a holding grows |
|---|---|---|
| Price factors | Equities, commodities | Along the simulated price path. |
| Interest rates | Short and long rates | The rate is compounded like a rolled money-market holding or, with a duration, priced as a bond fund ([below](#bonds-cash-roll-or-duration)). |
| Credit | Spreads by maturity or rating | The government yield the spread sits on, plus the spread, less the yearly default loss for its rating. With a duration, a widening also marks the holding down at once. |
| Real estate | House-price growth | Price growth plus a 5% net rental yield. |
| Not investable | Inflation, unemployment, dividend yields, FX | Cannot be held, only used as inputs (for example to index cashflows). |

A spread is not a return. A corporate bond earns the risk-free yield plus the spread, less what defaults cost after recoveries, and for investment grade that loss is a small part of the spread. The default loss is Moody's average five-year credit loss for the holding's rating, net of recoveries, spread evenly over the five years ([Moody's, 2005, Exhibit 11](https://www.bu.edu/econ/files/2015/01/Moodys_Default_1920-2004.pdf){:target="_blank"}): 0.11% a year for investment grade, 2.98% for speculative grade, or a rate you set. The government yield is a long rate in the spread's currency or, when the run has the US yield curve, the curve at the holding's duration, since spreads are quoted over Treasuries of matching maturity. A run without any rate earns the spread less losses, an excess return over government bonds.

Rents are about half of housing's long-run return, so leaving them out makes property look like a poor investment: across 16 countries from 1870 to 2015, rental income averaged 5.50% a year of an 11.05% total return, 5.22% since 1950 and 5.33% in the United States ([Jordà, Knoll, Kuvshinov, Schularick and Taylor, 2019, Tables VIII, IX and A.20](https://doi.org/10.1093/qje/qjz012){:target="_blank"}). The 5% default sits between that history and the 4.8% income return of the NCREIF Property Index over 2025; set your own per holding.

With holdings in several currencies, each equity, commodity and real-estate holding can be converted into the reporting currency first, so a euro equity in a dollar portfolio carries the currency return too. Rates are never converted (see [units](/projects/financescenarios/docs/units)).

## Buy-and-Hold Versus Rebalancing

<div class="ca-cards ca-cards--3">
  <div><i class="ca-icon fas fa-arrow-trend-up" aria-hidden="true"></i><p class="ca-card-title">Buy-and-hold</p><p>Sets the weights once. Each holding then grows with its own asset, so the mix drifts toward whatever performs best. Over a long horizon a 60/40 drifts into a mostly equity portfolio.</p></div>
  <div><i class="ca-icon fas fa-calendar-days" aria-hidden="true"></i><p class="ca-card-title">Calendar rebalancing</p><p>Resets the holdings to target every N steps: the constant-mix discipline of selling what rose and buying what fell (<a href="https://doi.org/10.2469/faj.v44.n1.16" target="_blank">Perold and Sharpe, 1988</a>).</p></div>
  <div><i class="ca-icon fas fa-sliders-h" aria-hidden="true"></i><p class="ca-card-title">Band rebalancing</p><p>Trades only when a holding drifts more than a set distance from its target (say 5 percentage points). Each scenario triggers on its own, so trading happens when markets move, not when the calendar says.</p></div>
</div>

**The rebalancing premium and volatility drag.** This is standard portfolio theory rather than a separate calculation in the package; it explains why the simulated rebalanced and buy-and-hold paths differ. An asset's long-run (geometric) growth rate is lower than its average (arithmetic) return by roughly half its variance:

$$
g \approx \mu - \tfrac{1}{2}\sigma^2
$$

where $$\mu$$ is the arithmetic return per year and $$\sigma$$ the volatility. A constant-mix portfolio suffers the same drag, but on its own variance $$\sigma_p^2$$, which diversification makes smaller than the weighted average of the assets' variances. Its growth rate therefore beats the weighted average of the assets' growth rates by approximately

$$
\tfrac{1}{2}\left(\sum_i w_i \sigma_i^2 - \sigma_p^2\right) \geq 0
$$

with $$w_i$$ the target weights (non-negative, summing to 1) and $$\sigma_i$$ each asset's volatility. That is the rebalancing (or diversification) premium: largest for volatile, weakly correlated assets, and zero only when the assets are perfectly correlated and equally volatile. Buy-and-hold forgoes it but lets winners run, so it keeps more upside when one asset steadily outgrows the others.

The example run shows the trade-off. A mix of 60% US equities and 40% cash, starting from 100:

<div class="ca-nums fs-nums">
  <span><b>about 426</b>5th percentile, under both approaches</span>
  <span><b>5,925</b>95th percentile, buy-and-hold</span>
  <span><b>2,996</b>95th percentile, rebalanced</span>
</div>

Buy-and-hold had the far higher 95th percentile because it ends up holding mostly equities and takes the equity risk that comes with that.

**Costs.** An annual fee is charged continuously, as $$e^{-f\,\Delta t}$$ per step for a fee rate $$f$$ and step length $$\Delta t$$ in years. It compounds: 1% a year removes about 26% of the final value over 30 years ($$1 - e^{-0.3}$$). Trading costs apply only when a rebalance trades, on the one-way turnover, so frequent rebalancing has to earn its premium net of costs.

```python
weights = {"us_broad": 0.6, "united_states_short_rate": 0.4}

buy_and_hold = portfolio.compute(weights, initial_value=100.0)
yearly = portfolio.compute(weights, initial_value=100.0, rebalance_every=1, fee_rate=0.002)
banded = portfolio.compute(weights, initial_value=100.0, rebalance_band=0.05, transaction_cost_rate=0.001)
```

Each step applies growth net of fees, then any rebalance net of trading costs, then any cashflow.

## Cashflows and Sequence Risk

Deposits and withdrawals turn a return distribution into a plan: save for 15 years, then live off the portfolio. Rules are stated in years, so they mean the same whether the run steps monthly or yearly. A deposit buys the target mix; a withdrawal is taken pro rata. A portfolio that hits zero stays at zero.

With withdrawals, the **order** of returns matters, not only their average. A crash early in the withdrawal phase forces selling at low prices, and the units sold never recover; the same crash late does far less damage. That is sequence-of-returns risk, and why a plan has to be tested on paths, not on an expected return.

Withdrawals can be indexed to each scenario's own simulated inflation, so they keep their purchasing power. This matters a lot: in the example run (100,000 to start, 10,000 a year saved for 15 years, then 40,000 a year withdrawn), the money lasted 30 years in 91.7% of scenarios with a fixed nominal withdrawal, and far less often when the withdrawal rose with inflation.

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
    inflation_factor="united_states_inflation",  # an annual rate (0.024 is 2.4%), not a price index
)
```

## Bonds: Cash Roll or Duration

By default a rate holding compounds its yield with no price effect, like a floating-rate note: a rate rise only raises future income. Giving it a duration prices it as a constant-duration bond fund instead, so a rate rise marks it down at once and it then earns the higher yield ([Redington, 1952](https://doi.org/10.1017/S0020268100052811){:target="_blank"}). Each step's return is

$$
r_t = -D\,(y_t - y_{t-1}) + y_{t-1}\,\Delta t
$$

where $$D$$ is the modified duration and $$y$$ the simulated yield: the price effect of the yield change plus the interest earned. The fund rolls to keep its duration constant, like a long-Treasury ETF, rather than ageing like a single bond.

A bond fund earns the yield at its own maturity, so $$y$$ should be a long rate, such as the 10-year yield in the default factor set. Three-month bills follow policy rates rather than long yields, so a short rate given a duration is priced off the US yield curve at that duration when the run has the curve, else off the same country's long rate; only a run with neither prices it off the bill rate itself, with a warning. In the example run, which has only the short rate, the cash roll earned the starting 4.0% in year one in every scenario.

<div class="fs-callout fs-callout--limits" markdown="1">
<p class="fs-callout__title">Limits</p>

- This is first-order duration only: convexity is ignored.
- Compounding the return as a log return understates a very large one-step loss.

On monthly or weekly steps both effects are small.
</div>

```python
bonds = portfolio.compute({"united_states_long_rate": 1.0}, durations={"united_states_long_rate": 7.0})
```

## Glidepaths

A target-date or lifecycle plan moves from growth to safety as the target date nears. Target weights are set at a few checkpoints, move in a straight line between them, and the portfolio is rebalanced to the moving target.

In the example run, gliding from 90% to 30% equities over 30 years:

<div class="ca-nums fs-nums">
  <span><b>1,210</b>median end value, the glidepath</span>
  <span><b>1,183</b>yearly rebalanced 60/40 equity-cash mix</span>
</div>

The two end close together, with the glidepath taking more of the risk early, when the amount at stake is smallest.

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

Well-known allocations ship as presets, such as a 60/40, the all-weather and permanent portfolios, a three-fund portfolio, an endowment model, Taleb's barbell (85% Treasury bills, 15% small-cap and growth stocks) and a target-date glidepath. The glidepath follows Vanguard's Target Retirement funds: 90% equities until 25 years before the target date, 50% at it and 30% seven years after. The 60/40 preset holds 60% US equities and 40% US Treasuries: the 10-year yield priced as a bond fund of duration 5.4 years, about that of a broad Treasury ETF.

```python
result = Portfolio.from_preset(scenario_set, preset="balanced_60_40").compute()
```

## Risk Metrics

All metrics are counted over the simulated paths, not from a formula that assumes normal returns, so fat tails and regime shifts carry through.

| Metric | Question it answers |
|---|---|
| Maximum drawdown | How far does the value fall from a peak? Reported as percentiles across scenarios of each scenario's worst fall. |
| Value-at-Risk (95%) | What loss is exceeded in only 5% of scenarios? |
| Expected Shortfall (95%) | How bad is the average loss in that worst 5%? A coherent risk measure, unlike VaR ([Artzner et al., 1999](https://doi.org/10.1111/1467-9965.00068){:target="_blank"}; [Acerbi and Tasche, 2002](https://doi.org/10.1016/S0378-4266(02)00283-2){:target="_blank"}). |
| Annualized volatility | How bumpy is the ride, pooled over all scenarios and steps? |
| CAGR percentiles | What growth rate does each scenario compound at? A scenario ending at or below zero counts as -100%. |
| Probability of loss | How often does the portfolio end below its starting value? |
| Probability of shortfall | How often does the money run out, or a target (say one million) not get reached? |

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">Read them over the whole horizon</p>

VaR, Expected Shortfall and the probability of loss describe the total return over the whole horizon: on a 30-year run that is a 30-year outcome, not a one-year loss. With cashflows they mix returns with deposits and withdrawals.
</div>

All values are nominal unless deflated by a scenario's own cumulative inflation, which gives the value in today's money; in the example run a saver's median portfolio was worth 1,064,686 after 20 years in nominal terms, and markedly less once deflated by its own inflation.

In the example run, rebalancing the 60/40 equity-cash mix yearly with a 0.2% fee, against buy-and-hold:

<div class="ca-nums fs-nums">
  <span><b>&minus;23.84% &rarr; &minus;17.25%</b>median worst drawdown</span>
  <span><b>13.21% &rarr; 10.45%</b>annualized volatility</span>
  <span><b>9.28% &rarr; 8.37%</b>median CAGR</span>
</div>

The lower drawdown and volatility came at the cost of a lower median CAGR: the buy-and-hold portfolio earned more because it had drifted into more equity risk.

```python
risk = portfolio.risk_metrics(yearly)
summary = portfolio.summary(
    plan, goal_value=1_000_000.0, inflation_factor="united_states_inflation", real_value_year=20
)
```

## Benchmarks and Backtests

A simulation says what could happen; a backtest says what did. The same rebalancing, cashflow and fee rules run on realized history, one path instead of thousands.

<div class="fs-callout" markdown="1">
Use a backtest as a check on the simulation, not as a forecast.
</div>

History is lined up on the dates every holding shares, so pick a frequency that matches the least frequently published series. With one path, statistics across scenarios (VaR, Expected Shortfall, success rates) collapse to a single number, while CAGR, volatility, drawdown and factor exposure stay fully meaningful.

```python
backtest = Portfolio.backtest(scenarios, preset="balanced_60_40", period="monthly")
values = backtest.compute(rebalance_every=12)
```

Several presets can be backtested together. They share one calendar, the dates on which every holding of every preset has a price, so no mix gets a crisis the others skip; a holding with a short history shortens the window for all of them. Each read (risk metrics, factor exposure, the comparison with a benchmark) then gives one row per preset, and the chart draws one line per portfolio on a shared axis.

```python
presets = ["balanced_60_40", "all_weather", "permanent_portfolio"]
comparison = Portfolio.backtest(scenarios, presets, period="monthly")
comparison.compute(initial_value=100_000, rebalance_every=12).plot(levels=True)
comparison.risk_metrics()   # one row per preset
```

Against a benchmark (an index, another mix, or the same mix over other dates) the comparison covers tracking error, correlation, beta, the differences in CAGR and Sharpe ratio ([Sharpe, 1966](https://doi.org/10.1086/294846){:target="_blank"}) and active share, half the sum of the absolute weight differences ([Cremers and Petajisto, 2009](https://doi.org/10.1093/rfs/hhp057){:target="_blank"}). On a simulated run tracking error is measured within each scenario, the deviation a manager actually lives through, and the median is reported with its spread across scenarios; averaging the scenarios first would cancel most of the deviations. Correlation and beta there compare the two mean paths, so they describe the average scenario rather than any single one; read them on a backtest.

## Factor Exposure

Factor exposure shows what a portfolio actually behaved like over history: how you check a mandate or explain performance.

<div class="fs-facts">
  <div><span>Input</span><b>Realized returns (a backtest)</b></div>
  <div><span>Method</span><b>Ordinary least squares on excess returns</b></div>
  <div><span>Model</span><b>Fama-French five factors (default) or three</b></div>
  <div><span>Data</span><b>Kenneth French's Data Library</b></div>
</div>

The portfolio's excess return is regressed on the Fama-French factors by ordinary least squares:

$$
R_t - R_{f,t} = \alpha + \sum_i \beta_i F_{i,t} + \varepsilon_t
$$

where $$R_t - R_{f,t}$$ is the return above the risk-free rate, $$\alpha$$ the part the factors do not explain, and $$\beta_i$$ the loading on factor $$F_i$$: the market (Mkt-RF), small versus large companies (SMB), cheap versus expensive (HML), robust versus weak profitability (RMW) and companies that invest conservatively versus aggressively (CMA). The model is the three-factor one of [Fama and French (1993)](https://doi.org/10.1016/0304-405X(93)90023-5){:target="_blank"} or the five-factor one of [Fama and French (2015)](https://doi.org/10.1016/j.jfineco.2014.10.010){:target="_blank"} (the default), with factor data from Kenneth French's [Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html){:target="_blank"}, which defines each factor in its [description of the Fama/French 5 factors (2x3)](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_5_factors_2x3.html){:target="_blank"}.

On monthly history from 2004-01 to 2026-10:

<div class="ca-nums fs-nums">
  <span><b>0.997</b>market beta, 100% SPY</span>
  <span><b>0.996</b>R-squared, 100% SPY</span>
  <span><b>&minus;0.12</b>SMB: a slight large-company tilt</span>
  <span><b>0.594</b>market beta, 60% SPY and 40% cash</span>
</div>

The 60/40 mix (the US short rate as cash, rebalanced yearly) showed a market beta close to its equity weight. A "balanced" portfolio with a beta near 1 would be an equity portfolio in disguise.

```python
exposure = backtest.factor_exposure(model="five_factor")
```

<div class="fs-callout fs-callout--limits" markdown="1">
<p class="fs-callout__title">Limits</p>

- Only realized returns can be regressed; a simulated scenario has no calendar to line up with real factor history.
- The factors are US equity factors. A non-US portfolio's betas describe its co-movement with the US market, not its own market's style.
- The three- and five-factor files build SMB differently, so the two models give slightly different size betas.
</div>

Charts of the holdings' values and of weight drift are covered on the [plotting page](/projects/financescenarios/docs/plotting).

<div class="fs-ref"><a href="/projects/financescenarios/docs/reference/portfolio"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Portfolio</a></div>

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">9</span></summary>

- Acerbi, C., Tasche, D. (2002). "On the coherence of expected shortfall." Journal of Banking & Finance, 26(7), 1487-1503. [https://doi.org/10.1016/S0378-4266(02)00283-2](https://doi.org/10.1016/S0378-4266(02)00283-2){:target="_blank"}
- Artzner, P., Delbaen, F., Eber, J-M., Heath, D. (1999). "Coherent Measures of Risk." Mathematical Finance, 9(3), 203-228. [https://doi.org/10.1111/1467-9965.00068](https://doi.org/10.1111/1467-9965.00068){:target="_blank"}
- Cremers, K.J.M., Petajisto, A. (2009). "How Active Is Your Fund Manager? A New Measure That Predicts Performance." Review of Financial Studies, 22(9), 3329-3365. [https://doi.org/10.1093/rfs/hhp057](https://doi.org/10.1093/rfs/hhp057){:target="_blank"}
- Fama, E.F., French, K.R. (1993). "Common risk factors in the returns on stocks and bonds." Journal of Financial Economics, 33(1), 3-56. [https://doi.org/10.1016/0304-405X(93)90023-5](https://doi.org/10.1016/0304-405X(93)90023-5){:target="_blank"}
- Fama, E.F., French, K.R. (2015). "A five-factor asset pricing model." Journal of Financial Economics, 116(1), 1-22. [https://doi.org/10.1016/j.jfineco.2014.10.010](https://doi.org/10.1016/j.jfineco.2014.10.010){:target="_blank"}
- French, K.R. "Data Library." Tuck School of Business at Dartmouth. [https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html){:target="_blank"}
- Perold, A.F., Sharpe, W.F. (1988). "Dynamic Strategies for Asset Allocation." Financial Analysts Journal, 44(1), 16-27. [https://doi.org/10.2469/faj.v44.n1.16](https://doi.org/10.2469/faj.v44.n1.16){:target="_blank"}
- Redington, F.M. (1952). "Review of the Principles of Life-Office Valuations." Journal of the Institute of Actuaries, 78(3), 286-340. [https://doi.org/10.1017/S0020268100052811](https://doi.org/10.1017/S0020268100052811){:target="_blank"}
- Sharpe, W.F. (1966). "Mutual Fund Performance." The Journal of Business, 39(S1), 119-138. [https://doi.org/10.1086/294846](https://doi.org/10.1086/294846){:target="_blank"}

</details>
