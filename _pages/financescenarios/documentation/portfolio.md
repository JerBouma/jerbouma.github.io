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

Rents are about half of housing's long-run return, so leaving them out makes property look like a poor investment: across 16 countries from 1870 to 2015, rental income averaged 5.49% a year of an 11.22% nominal total return, and 5.26% since 1950 ([Jordà, Knoll, Kuvshinov, Schularick and Taylor, 2017, Table 6](https://doi.org/10.24148/wp2017-25){:target="_blank"}). The 5% default sits a little below that history; set your own per holding.

With holdings in several currencies, each equity, commodity and real-estate holding can be converted into the reporting currency first, so a euro equity in a dollar portfolio carries the currency return too. Rates are never converted (see [units](/projects/financescenarios/docs/units)).

## Buy-and-Hold Versus Rebalancing

- **Buy-and-hold** sets the weights once. Each holding then grows with its own asset, so the mix drifts toward whatever performs best. Over a long horizon a 60/40 drifts into a mostly equity portfolio.
- **Calendar rebalancing** resets the holdings to target every N steps: the constant-mix discipline of selling what rose and buying what fell ([Perold and Sharpe, 1988](https://doi.org/10.2469/faj.v44.n1.16){:target="_blank"}).
- **Band rebalancing** trades only when a holding drifts more than a set distance from its target (say 5 percentage points). Each scenario triggers on its own, so trading happens when markets move, not when the calendar says.

**The rebalancing premium and volatility drag.** This is standard portfolio theory rather than a separate calculation in the package; it explains why the simulated rebalanced and buy-and-hold paths differ. An asset's long-run (geometric) growth rate is lower than its average (arithmetic) return by roughly half its variance:

$$
g \approx \mu - \tfrac{1}{2}\sigma^2
$$

where $$\mu$$ is the arithmetic return per year and $$\sigma$$ the volatility. A constant-mix portfolio suffers the same drag, but on its own variance $$\sigma_p^2$$, which diversification makes smaller than the weighted average of the assets' variances. Its growth rate therefore beats the weighted average of the assets' growth rates by approximately

$$
\tfrac{1}{2}\left(\sum_i w_i \sigma_i^2 - \sigma_p^2\right) \geq 0
$$

with $$w_i$$ the target weights (non-negative, summing to 1) and $$\sigma_i$$ each asset's volatility. That is the rebalancing (or diversification) premium: largest for volatile, weakly correlated assets, and zero only when the assets are perfectly correlated and equally volatile. Buy-and-hold forgoes it but lets winners run, so it keeps more upside when one asset steadily outgrows the others.

The example run shows the trade-off. A mix of 60% US equities and 40% cash ended at almost the same 5th percentile (about 426 from 100) under both approaches, but buy-and-hold had a far higher 95th percentile (5,925 against 2,996), because it ends up holding mostly equities and takes the equity risk that comes with that.

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

This is first-order duration only: convexity is ignored, and compounding the return as a log return understates a very large one-step loss. On monthly or weekly steps both effects are small.

```python
bonds = portfolio.compute({"united_states_long_rate": 1.0}, durations={"united_states_long_rate": 7.0})
```

## Glidepaths

A target-date or lifecycle plan moves from growth to safety as the target date nears. Target weights are set at a few checkpoints, move in a straight line between them, and the portfolio is rebalanced to the moving target.

In the example run, gliding from 90% to 30% equities over 30 years ended at a median of 1,210, close to a yearly rebalanced 60/40 equity-cash mix's 1,183, with more of the risk taken early, when the amount at stake is smallest.

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

VaR, Expected Shortfall and the probability of loss describe the total return over the whole horizon: on a 30-year run that is a 30-year outcome, not a one-year loss. With cashflows they mix returns with deposits and withdrawals. All values are nominal unless deflated by a scenario's own cumulative inflation, which gives the value in today's money; in the example run a saver's median portfolio was worth 1,064,686 after 20 years in nominal terms, and markedly less once deflated by its own inflation.

In the example run, rebalancing the 60/40 equity-cash mix yearly with a 0.2% fee lowered the median worst drawdown from -23.84% to -17.25% and the annualized volatility from 13.21% to 10.45%, at the cost of a lower median CAGR (8.37% against 9.28%): the buy-and-hold portfolio earned more because it had drifted into more equity risk.

```python
risk = portfolio.risk_metrics(yearly)
summary = portfolio.summary(
    plan, goal_value=1_000_000.0, inflation_factor="united_states_inflation", real_value_year=20
)
```

## Benchmarks and Backtests

A simulation says what could happen; a backtest says what did. The same rebalancing, cashflow and fee rules run on realized history, one path instead of thousands. Use it as a check on the simulation, not as a forecast.

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

Factor exposure shows what a portfolio actually behaved like over history: how you check a mandate or explain performance. The portfolio's excess return is regressed on the Fama-French factors by ordinary least squares:

$$
R_t - R_{f,t} = \alpha + \sum_i \beta_i F_{i,t} + \varepsilon_t
$$

where $$R_t - R_{f,t}$$ is the return above the risk-free rate, $$\alpha$$ the part the factors do not explain, and $$\beta_i$$ the loading on factor $$F_i$$: the market (Mkt-RF), small versus large companies (SMB), cheap versus expensive (HML), robust versus weak profitability (RMW) and companies that invest conservatively versus aggressively (CMA). The model is the three-factor one of [Fama and French (1993)](https://doi.org/10.1016/0304-405X(93)90023-5){:target="_blank"} or the five-factor one of [Fama and French (2015)](https://doi.org/10.1016/j.jfineco.2014.10.010){:target="_blank"} (the default), with factor data from Kenneth French's [Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html){:target="_blank"}.

> "RMW (Robust Minus Weak) is the average return on the two robust operating profitability portfolios minus the average return on the two weak operating profitability portfolios, … CMA (Conservative Minus Aggressive) is the average return on the two conservative investment portfolios minus the average return on the two aggressive investment portfolios, …"
> <cite>[Kenneth R. French, Data Library, Description of Fama/French 5 Factors (2x3)](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_5_factors_2x3.html)</cite>

On monthly history from 2004-01 to 2026-10, 100% SPY showed a market beta of 0.997 and an R-squared of 0.996, with a slight large-company tilt (SMB -0.12). 60% SPY and 40% cash (the US short rate), rebalanced yearly, showed a market beta of 0.594, close to its equity weight. A "balanced" portfolio with a beta near 1 would be an equity portfolio in disguise.

```python
exposure = backtest.factor_exposure(model="five_factor")
```

Limits:

- Only realized returns can be regressed; a simulated scenario has no calendar to line up with real factor history.
- The factors are US equity factors. A non-US portfolio's betas describe its co-movement with the US market, not its own market's style.
- The three- and five-factor files build SMB differently, so the two models give slightly different size betas.

Charts of the holdings' values and of weight drift are covered on the [plotting page](/projects/financescenarios/docs/plotting).

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
