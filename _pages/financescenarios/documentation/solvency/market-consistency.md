---
title: Market Consistency
seo_title: "Market Consistency | Finance Scenarios"
seo_title_suffix: false
excerpt: "How Finance Scenarios values under Solvency II: a risk-neutral run that reproduces today's prices, the bank-account deflator, the martingale test with Holm's adjustment, and EIOPA's risk-free curve with its ultimate forward rate."
description: "Market consistency in Finance Scenarios: real-world and risk-neutral runs, the deflator, the martingale test of Solvency II and EIOPA's guidelines, Holm's step-down adjustment, and EIOPA's curve and UFR."
author_profile: false
permalink: /projects/financescenarios/docs/solvency
classes: wide-sidebar
layout: single
redirect_from:
    - /projects/financescenarios/docs/reference/solvency
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-solvency"
---

Solvency II asks two questions of an insurer. What is owed, valued at today's market prices: the best estimate of [Article 77](https://eur-lex.europa.eu/eli/dir/2009/138/oj){:target="_blank"}? And is there enough capital to keep paying after a 1-in-200 bad year: the Solvency Capital Requirement of Article 101? The first needs scenarios priced like today's market, a risk-neutral run; the second needs scenarios of how markets are likely to move, a real-world run. This page covers the risk-neutral run, the test that it is fit for valuation and EIOPA's risk-free curve; [Best Estimate and SCR](/projects/financescenarios/docs/solvency/capital) puts both runs to work.

## Two Kinds of Run

Each run answers its own question:

| Job | Run | Why that run |
|:----|:----|:-------------|
| Best estimate of a liability | Risk neutral (or EIOPA's curve) | A value must reproduce today's market prices, whatever investors expect to earn. |
| Proof the run is fit for valuation | Risk neutral | The martingale test: discounted assets must be worth today's price on average. |
| One-year SCR, internal-model view | Real world | The 1-in-200 loss is about how markets are likely to move, risk premia included. |
| SCR, standard formula | EIOPA's prescribed shocks | Interest rate and equity shocks set by regulation, not by a model. |

Both runs discount along each scenario with the bank-account deflator, the value today of 1 paid at time $$t_k$$:

$$
D(t_k) = \exp\Big(-\sum_{j < k} r(t_j)\,\Delta t\Big), \qquad D(0) = 1
$$

where $$r(t_j)$$ is the simulated short rate at the start of each step and $$\Delta t$$ the step length in years. On a risk-neutral run this deflator gives market prices. On a real-world run it gives a discounted expectation, which is what a one-year projection needs but is not a price.

## A Risk-Neutral Run {#martingale-test-example}

`simulate(measure="risk_neutral")` turns a factor set into a valuation run. The run's first short rate becomes a [Hull-White rate fitted to EIOPA's risk-free curve](/projects/financescenarios/docs/interest-rates/other-models#risk-neutral-hull-white) for its currency, the dollar's in the default factor set; every stock market earns that rate less its dividend yield; and inflation moves around the bond market's [breakeven curve](/projects/financescenarios/docs/economy#other-inflation-models), so the expected price index is the breakeven index. Unemployment keeps its own model, with its links to other factors cut, and the rest is left out: a valuation run keeps one short rate, and an exchange rate would need two. Rates and inflation get their volatility from history, so guarantees and capped indexation get a time value.

The examples on this page use the run from the [overview](/projects/financescenarios/docs#simulating-scenarios) as the real-world run: the default settings and factor set, calibrated on 19 October 2026, with 2,000 scenarios and seed 42. To simulate both:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
result = scenarios.simulate(n_simulations=2000, seed=42)
risk_neutral = scenarios.simulate(n_simulations=2000, seed=42, measure="risk_neutral")

risk_neutral.describe()
```

Which returns 17 variables: the three economies' inflation and unemployment, the US short rate, and the five stock markets with a dividend yield for each. The US short rate starts at 4.44% and averages 4.89% after five years, with a 90% range of 1.97% to 7.87%, narrower than the real-world run's 0% to 10.99%. US stocks return 2.92% a year on average against 8.49% in the real-world run: risk-neutral, they earn the short rate less their dividend yield of 0.99% and less half their variance in log terms, with no equity premium. When plotted, the US short rate and the US stock price in both runs:

{% include ft-chart.html id="solvency-risk-neutral" src="/assets/data/financescenarios-guides/solvency.json" label="Median and 5-95% band of the US short rate and the US stock price in the real-world and the risk-neutral run over five years" %}

## The Martingale Test

A value is only market consistent if the scenarios reproduce today's prices: a generator used under Solvency II must produce asset prices consistent with those observed in financial markets and assume no arbitrage ([Delegated Regulation (EU) 2015/35, Article 22(3)](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj#art_22){:target="_blank"}). EIOPA's [guidelines on valuation of technical provisions](https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en){:target="_blank"} (Guideline 58, paragraph 1.105) name the martingale test among the checks on a generator used for valuation, for each asset class used in the calibration and for some simple investment strategies.

<div class="fs-facts">
  <div><span>Run</span><b>Risk neutral</b></div>
  <div><span>Checks</span><b>Discounted price, dividends added back</b></div>
  <div><span>Verdict</span><b>Holm-adjusted p-values at 5%</b></div>
</div>

If an asset beats the risk-free cash account on average, every option and guarantee written on it is mispriced, and so is the best estimate. The test is that the discounted price, dividends added back, is a martingale: on average it stays at today's price ([Varnell, 2011](https://doi.org/10.1017/S1357321711000079){:target="_blank"}):

$$
\mathbb{E}\left[ D(t)\, S(t)\, e^{q t} \right] = S(0) \quad \text{at every date } t
$$

where $$S$$ is the asset price and $$q$$ its dividend yield. Each date after the start gets a 95% confidence band around the simulated mean, from the Monte Carlo standard error, and a p-value for the gap between that mean and $$S(0)$$.

With many dates each tested at 95%, a correct run still misses some by chance, and requiring every date to pass would fail a true martingale far more often than one time in twenty. The verdict therefore uses [Holm's (1979)](https://www.jstor.org/stable/4615733){:target="_blank"} step-down adjustment for testing many dates at once: the run fails only when the smallest adjusted p-value drops below 5%, which keeps the chance of wrongly failing a correct run at 5% at most, however closely neighboring dates are related. The stricter rule, every date passing, remains available. Neighboring dates share their paths, so misses come in runs and the share of dates inside their band swings from seed to seed: that is Monte Carlo noise, not a wrong drift.

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">When the test really fails</p>

Failing at most dates means the drift is wrong, typically a real-world run tested by mistake; leaving out the dividend yield makes nearly every date fail.
</div>

The one-table summary of [Best Estimate and SCR](/projects/financescenarios/docs/solvency/capital#scr-example) also applies a practical criterion: the run counts as market consistent when the largest gap stays within 2% of today's price.

The rates side has the same test: the bond prices the run implies, $$P(0, t) = \mathbb{E}[D(t)]$$, should match the curve the run was fitted to within about two standard errors.

## EIOPA's Curve and the Ultimate Forward Rate

Solvency II prescribes the discount curve: EIOPA's risk-free term structure, published monthly per currency for maturities of 1 to 150 years ([RFR Technical Documentation, EIOPA-BoS-25-599, paragraph 9.1.6](https://www.eiopa.europa.eu/document/download/f7fca58f-4d24-4441-ac60-de562bf26d77_en#page=43){:target="_blank"}), with or without the volatility adjustment, plus the up and down shocked curves of the standard formula. The package reads it as published, from January 2023 onward.

Market rates are used up to the last liquid point, the longest maturity whose market is deep and liquid enough: 20 years for the euro, the only currency where a residual volume criterion sets it ([paragraph 9.2.1](https://www.eiopa.europa.eu/document/download/f7fca58f-4d24-4441-ac60-de562bf26d77_en#page=44){:target="_blank"}), and 30 for the US dollar ([Table 8](https://www.eiopa.europa.eu/document/download/f7fca58f-4d24-4441-ac60-de562bf26d77_en#page=44){:target="_blank"}).

Beyond it EIOPA extrapolates with the Smith-Wilson method ([paragraph 9.1.1](https://www.eiopa.europa.eu/document/download/f7fca58f-4d24-4441-ac60-de562bf26d77_en#page=43){:target="_blank"}) so that forward rates converge to the ultimate forward rate (UFR), a long-term rate the regulator sets: an expected real rate, the same for every currency, plus a currency-specific expected inflation rate ([Annex E, paragraph E.3.3](https://www.eiopa.europa.eu/document/download/f7fca58f-4d24-4441-ac60-de562bf26d77_en#page=123){:target="_blank"}).

For long-dated liabilities the UFR, not the market, drives much of the value. The euro curve for September 2026, extrapolated beyond 20 years:

| Maturity (years) | 1 | 10 | 20 | 60 | 150 |
|:---------|--:|---:|---:|---:|----:|
| Spot rate | 3.27% | 3.58% | 3.60% | 3.42% | 3.35% |

A whole-run risk-neutral simulation reproduces the curve of its short rate's currency: its Hull-White short rate is centered on the path EIOPA's forwards imply, so the average discount factor across scenarios returns EIOPA's bond prices at every maturity up to the run's horizon, the UFR-driven long end included for a long run.

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">From 30 January 2027</p>

The Solvency II review (Directive (EU) 2025/2 and Delegated Regulation (EU) 2026/269), which applies from 30 January 2027, replaces Smith-Wilson: beyond the first smoothing point (still 20 years for the euro), each forward rate is a weighted average of a last liquid forward rate and the UFR, so market rates keep more weight; from 40 years past the first smoothing point the UFR must carry at least 77.5% of the weight ([Directive (EU) 2025/2, Article 1, point (39), replacing Article 77a(1) of the Solvency II Directive](https://eur-lex.europa.eu/eli/dir/2025/2/oj){:target="_blank"}). The convergence speed is set by regulation: a parameter of 11% for every currency except the Swedish krona, at 40% ([RFR Technical Documentation, EIOPA-BoS-26-198, paragraph 8.1.5](https://www.eiopa.europa.eu/eiopa-publishes-rfr-technical-documentation-become-applicable-30-january-2027-2026-05-26_en){:target="_blank"}).

From the first smoothing point $$T_1$$, the forward rate $$h$$ years beyond it blends the last liquid forward rate (for the euro the forward from 19 to 20 years) into the UFR:

$$
f(T_1 + h) = \text{UFR} + (\text{LLFR} - \text{UFR})\,\frac{1 - e^{-\alpha h}}{\alpha h}
$$

With $$\alpha$$ = 11%, the UFR's weight 40 years past the first smoothing point is 77.55%. An optional phase-in uses a higher convergence parameter for a transition period, which brings the forwards to the UFR sooner.
</div>

The package reads whichever curve EIOPA publishes, so the change arrives with EIOPA's own curves. To measure its effect on a best estimate before then, the new method can be applied to a current curve: the published rates up to the first smoothing point, then forwards that blend the last liquid forward rate into the UFR at EIOPA's speed of 11%. Where the forward at 20 years sits below the UFR, long rates come out lower and the best estimate of long-dated liabilities higher.

## Examples

Both examples check the risk-neutral run of [A Risk-Neutral Run](#martingale-test-example).

### Testing US Stocks

`martingale_test` checks the risk-neutral run date by date. To test US stocks, with the dividend yield of 0.99% the run was fitted with:

```python
from financescenarios import martingale_test

test = martingale_test(
    risk_neutral, asset="us_broad", short_rate="united_states_short_rate", dividend_yield=0.0099
)
test.table
```

Which passes: the discounted mean stays within 1.0% of today's price of $763.25 at every date, and 51 of the 60 monthly dates, 85%, fall within their own 95% band; corrected for testing 60 dates at once, no date is rejected (the smallest adjusted p-value is 0.87). When plotted, the discounted mean price as a ratio to today's, with the band:

{% include ft-chart.html id="solvency-martingale" src="/assets/data/financescenarios-guides/solvency.json" label="Discounted mean US stock price in the risk-neutral run as a ratio to today's price, with its 95% Monte Carlo band, over five years" %}

### Bond Prices against EIOPA's Curve

The deflator's average is the price of a zero-coupon bond. To read it off at whole years:

```python
deflator = risk_neutral.discount_factor_paths("united_states_short_rate")

{year: deflator[:, risk_neutral.step_at(year)].mean() for year in [1.0, 2.0, 3.0, 4.0, 5.0]}
```

Which gives, against the prices of EIOPA's dollar curve, $$(1 + s_T)^{-T}$$:

| Maturity (years) | 1 | 2 | 3 | 4 | 5 |
|:--|--:|--:|--:|--:|--:|
| Run, $$\mathbb{E}[D(T)]$$ | 0.9564 | 0.9109 | 0.8679 | 0.8275 | 0.7888 |
| EIOPA | 0.9566 | 0.9114 | 0.8688 | 0.8287 | 0.7900 |
| Monte Carlo standard error | 0.0001 | 0.0003 | 0.0005 | 0.0007 | 0.0009 |

Every maturity lands within two standard errors of EIOPA's price.

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">8</span></summary>

- EIOPA (2014). Guidelines on Valuation of Technical Provisions (EIOPA-BoS-14/166). [eiopa.europa.eu](https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en){:target="_blank"}
- EIOPA (2025). Technical Documentation of the Methodology to Derive EIOPA's Risk-Free Interest Rate Term Structures (EIOPA-BoS-25-599). [eiopa.europa.eu](https://www.eiopa.europa.eu/document/download/f7fca58f-4d24-4441-ac60-de562bf26d77_en){:target="_blank"}
- EIOPA (2026). Technical documentation of the methodology to derive EIOPA's risk-free interest rate term structures, applicable from 30 January 2027. [eiopa.europa.eu](https://www.eiopa.europa.eu/eiopa-publishes-rfr-technical-documentation-become-applicable-30-january-2027-2026-05-26_en){:target="_blank"}
- European Commission (2015). "Commission Delegated Regulation (EU) 2015/35", Articles 165-167 (interest rate risk) and 168-172 (equity risk and symmetric adjustment). [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj){:target="_blank"}
- European Parliament and Council (2009). "Directive 2009/138/EC (Solvency II)", Articles 76-77 (technical provisions, best estimate) and 101 (SCR at 99.5% over one year). [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/dir/2009/138/oj){:target="_blank"}
- European Parliament and Council (2024). "Directive (EU) 2025/2", amending Directive 2009/138/EC, Articles 77(6)-(7), 77a and 106(3), applying from 30 January 2027. [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/dir/2025/2/oj){:target="_blank"}
- Holm, S. (1979). "A Simple Sequentially Rejective Multiple Test Procedure." Scandinavian Journal of Statistics, 6(2), 65-70. [jstor.org](https://www.jstor.org/stable/4615733){:target="_blank"}
- Varnell, E.M. (2011). "Economic Scenario Generators and Solvency II." British Actuarial Journal, 16(1), 121-159. [doi.org](https://doi.org/10.1017/S1357321711000079){:target="_blank"}

</details>

{% include ft-charts-script.html %}
