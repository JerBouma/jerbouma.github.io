## Getting Started

The Solvency module values what an insurer or pension fund owes and the capital it needs under [Solvency II](https://eur-lex.europa.eu/eli/dir/2009/138/oj){:target="_blank"}. The best estimate of a liability needs a run priced like today's market, a risk-neutral run; the one-year Solvency Capital Requirement (SCR) at 99.5% needs a run of how markets are likely to move, a real-world run. `Solvency` takes one of each and reports both.

This section uses the run from the [overview](/projects/financescenarios/docs) as the real-world run: the default settings and factor set, calibrated on 19 October 2026, with 2,000 scenarios and seed 42.

### A Risk-Neutral Run

The same factor set simulates under the risk-neutral measure with `measure="risk_neutral"`. The short rate then follows a Hull-White process that reproduces EIOPA's risk-free curve, every stock market earns that rate less its dividend yield, and inflation moves around the bond market's breakeven curve. To simulate both runs:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
result = scenarios.simulate(n_simulations=2000, seed=42)
risk_neutral = scenarios.simulate(n_simulations=2000, seed=42, measure="risk_neutral")

risk_neutral.describe()
```

Which returns 17 variables: the three economies' inflation and unemployment, the US short rate, the five stock markets and a dividend yield for each; the long rates, currencies, commodities, house prices and the yield-curve factors have no risk-neutral form in this factor set and are left out. The US short rate starts at 4.44% and averages 4.89% after five years, with a 90% range of 1.97% to 7.87%, narrower than the real-world run's 0% to 10.99%. US stocks return 2.92% a year on average against 8.49% in the real-world run: risk-neutral, they earn the short rate less their dividend yield of 0.99%, with no equity premium. When plotted, the US short rate and the US stock price in both runs:

{% include ft-chart.html id="solvency-risk-neutral" src="/assets/data/financescenarios-guides/solvency.json" label="Median and 5-95% band of the US short rate and the US stock price in the real-world and the risk-neutral run over five years" %}

### The Martingale Test

A risk-neutral run is fit for valuation only if it reproduces today's prices: discounted along each scenario with its own short rate, a traded asset must on average be worth today's price at every date. `martingale_test` checks that date by date, with a confidence band from the Monte Carlo standard error. To test US stocks:

```python
from financescenarios import martingale_test

test = martingale_test(
    risk_neutral, asset="us_broad", short_rate="united_states_short_rate", dividend_yield=0.0099
)
test.table
```

Which passes: the discounted mean stays within 1.0% of today's price of $763.25 at every date, and 85% of the 61 dates fall within their own 95% band; corrected for testing 61 dates at once ([Holm, 1979](https://www.jstor.org/stable/4615733){:target="_blank"}), no date rejects. When plotted, the discounted mean price as a ratio to today's, with the band:

{% include ft-chart.html id="solvency-martingale" src="/assets/data/financescenarios-guides/solvency.json" label="Discounted mean US stock price in the risk-neutral run as a ratio to today's price, with its 95% Monte Carlo band, over five years" %}

### Best Estimate, Own Funds and the SCR

`report` values a stream of payments on the risk-neutral run, sets it against the assets that back it on the real-world run and reads the SCR off the one-year distribution of own funds. To value 10,000 a year for five years, backed by 60,000 in the 60/40 portfolio:

```python
from financescenarios import Portfolio, Solvency

solvency = Solvency(real_world=result, risk_neutral=risk_neutral)

assets = Portfolio.from_preset(result, preset="balanced_60_40").compute(initial_value=60_000, rebalance_every=12)
solvency.report(cashflows=[10_000] * 5, assets=assets)
```

Which returns:

| item | value | meaning |
|:-----|:------|:--------|
| market consistent | passed (largest gap 1.0%) | discounted back, us_broad stays within 2% of today's price |
| best estimate | 43,514 | what the payments are worth today |
| own funds | 15,683 | assets minus what is owed, today |
| SCR (1 in 200 year) | 13,619 | the capital that survives a 1-in-200 bad year |
| solvency ratio | 1.15 | own funds / SCR; above 1 means enough capital |

The five payments of 10,000 are worth 43,514 today, so the 60,000 leaves own funds of 15,683. In the worst one-year scenario in 200 they fall to 2,064, discounted to today, and the gap of 13,619 is the SCR, which the own funds cover 1.15 times. To draw where own funds could be after one year:

```python
solvency.plot(cashflows=[10_000] * 5, assets=assets)
```

When plotted, with today's own funds and the 1-in-200 outcome marked:

{% include ft-chart.html id="solvency-own-funds" src="/assets/data/financescenarios-guides/solvency.json" label="Distribution of own funds after one year across 2,000 real-world scenarios, discounted to today, with today's own funds and the 1-in-200 outcome" %}

### The Standard Formula

Next to the internal-model view above, the standard formula applies shocks set by regulation. `equity_scr` gives the equity risk charge of [Commission Delegated Regulation (EU) 2015/35](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj){:target="_blank"} (Articles 168-172), with the symmetric adjustment that EIOPA publishes each month. To calculate it for 1,000,000 in type 1 equities (listed in the EEA or the OECD) and 250,000 in type 2 (everything else), with a symmetric adjustment of 7.71%:

```python
from financescenarios import equity_scr

equity_scr(type_1_value=1_000_000, type_2_value=250_000, symmetric_adjustment=0.0771)
```

Which gives charges of 46.71% and 56.71% (the 39% and 49% base charges plus the adjustment), losses of 467,100 and 141,775, and an equity SCR of 581,048: less than their sum of 608,875, since the two types do not fall perfectly together. `interest_rate_scr` does the same for interest rates, with EIOPA's shocked curves from `eiopa_risk_free_curve`, and `write_files` exports both runs as the scenario files liability and ALM systems load.

{% include ft-charts-script.html %}
