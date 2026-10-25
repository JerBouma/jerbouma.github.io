---
title: Best Estimate and SCR
seo_title: "Best Estimate and SCR | Finance Scenarios"
seo_title_suffix: false
excerpt: "How Finance Scenarios computes the Solvency II best estimate on a risk-neutral run and the Solvency Capital Requirement as the 99.5% one-year loss of own funds on a real-world run, next to the standard formula."
description: "The best estimate and SCR in Finance Scenarios: Article 77 valuation, Article 101 capital, the internal-model one-year VaR of own funds, the standard formula's interest rate and equity modules, and a run."
author_profile: false
permalink: /projects/financescenarios/docs/solvency/capital
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/solvency
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-solvency"
---

The best estimate is what a liability is worth at today's market prices; the Solvency Capital Requirement is the capital that keeps it paid after a 1-in-200 bad year. Finance Scenarios computes the first on a risk-neutral run and the second on a real-world run, the two runs of [Market Consistency](/projects/financescenarios/docs/solvency), and sets the standard formula's prescribed shocks beside them.

## Best Estimate

Article 77(2) of the [Solvency II Directive](https://eur-lex.europa.eu/eli/dir/2009/138/oj){:target="_blank"} defines the best estimate as the probability-weighted average of future cash flows, discounted at the relevant risk-free curve.

<div class="fs-facts">
  <div><span>Run</span><b>Risk neutral</b></div>
  <div><span>Discounting</span><b>EIOPA's curve, or the simulated short rate</b></div>
  <div><span>Output</span><b>Best estimate, standard error and percentiles</b></div>
</div>

Across scenarios, that is the risk-neutral expectation of the discounted future cash flows:

$$
BE = \mathbb{E}^{Q}\Big[\sum_t D(t)\, CF(t)\Big]
$$

where $$CF(t)$$ is the amount paid at time $$t$$, $$D(t)$$ the scenario's deflator and $$Q$$ the risk-neutral measure. Discounting on EIOPA's curve instead applies $$(1 + s_t)^{-t}$$ to each scenario's cash flows, as Article 77(2) requires. Along the simulated short rate of a whole risk-neutral run the two agree on average, and cash flows that depend on the path of rates or equities, such as guarantees and profit sharing, are generated and discounted consistently with it.

For fixed cash flows this collapses to discounting on a curve, which is why plain Solvency II valuation uses EIOPA's curve directly. Scenarios earn their place when cash flows depend on the path: inflation-linked benefits, profit sharing, guarantees and options. From 30 January 2027 the Directive says so explicitly: where contracts include options and guarantees, the best estimate must reflect possible deviations from the expected outcome, not only the expected outcome itself ([Directive (EU) 2025/2, Article 1, point (38), adding Article 77(7)](https://eur-lex.europa.eu/eli/dir/2025/2/oj){:target="_blank"}).

The time value of those guarantees depends on how much rates and inflation move, and there the run falls short of a full market-consistent calibration, which EIOPA expects to be based on current data from deep, liquid and transparent financial markets ([Guidelines on valuation of technical provisions, Guideline 57, paragraph 1.101](https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en){:target="_blank"}).

<div class="fs-callout fs-callout--limits" markdown="1">
<p class="fs-callout__title">Limits</p>

Without swaption or inflation-option prices, the rate's volatility is fitted to how much yields across the curve have moved in history ([Other Rate Models](/projects/financescenarios/docs/interest-rates/other-models#risk-neutral-hull-white)), and inflation's to its own history. Treat the resulting cost of guarantees as indicative, and replace the volatility with a swaption-implied one for a reported best estimate.
</div>

### Example {#best-estimate-example}

The examples on this page use the two runs of [Market Consistency](/projects/financescenarios/docs/solvency#martingale-test-example): the real-world run of the overview, calibrated on 25 October 2026, and its risk-neutral run, 2,000 scenarios each with seed 42. To value 10,000 a year for five years, level and indexed to each scenario's own US inflation:

```python
import numpy as np

from financescenarios import best_estimate

annuity = np.zeros(len(risk_neutral.time_grid))
for year in [1.0, 2.0, 3.0, 4.0, 5.0]:
    annuity[risk_neutral.step_at(year)] = 10_000.0

level = best_estimate(risk_neutral, annuity, short_rate="united_states_short_rate")

index = risk_neutral.cumulative_index("united_states_inflation", initial_index=1.0).drop("scenario").to_numpy()
indexed = best_estimate(risk_neutral, annuity * index, short_rate="united_states_short_rate")
```

Which returns:

| annuity | best estimate | standard error | 0.5th percentile | 99.5th percentile |
|:--------|--------------:|---------------:|-----------------:|------------------:|
| level | 43,514 | 25 | 40,841 | 46,544 |
| inflation-indexed | 46,765 | 38 | 42,673 | 51,401 |

The five level payments are worth 43,514, close to the 43,556 that EIOPA's dollar bond prices give for 10,000 a year; across scenarios their discounted value spreads from about 41,000 to 46,500 as the rate moves, but the average is the market's price. Indexed to inflation they are worth 46,765, 7.5% more, and the standard errors of 25 and 38 show that 2,000 scenarios are plenty.

## Solvency Capital Requirement

Article 101(3) of the [Solvency II Directive](https://eur-lex.europa.eu/eli/dir/2009/138/oj){:target="_blank"} calibrates the SCR to the 99.5% Value-at-Risk of basic own funds, assets less liabilities, over one year. The internal-model reading takes that quantile of the simulated one-year loss on a real-world run:

$$
L = OF(0) - D(h)\, OF(h), \qquad \text{SCR} = \max\big(q_{99.5\%}(L),\, 0\big)
$$

where $$OF$$ is own funds, $$h$$ the one-year horizon, $$D(h)$$ the deflator back to today and $$q_{99.5\%}$$ the empirical quantile across scenarios. The Expected Shortfall beyond the SCR shows how bad the tail is past the 1-in-200 point. The own-funds path is yours to build: assets from a [portfolio](/projects/financescenarios/docs/portfolio), liabilities from your own projection, or the payments `report` values for you.

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">Check several seeds</p>

With 2,000 scenarios only 10 lie beyond the 99.5% quantile, so the SCR moves with the seed: in the example below it ranges from 12,279 to 13,461 across five seeds. Use several seeds, or more scenarios, before relying on it.
</div>

### Example {#scr-example}

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
| market consistent | passed (largest gap 1.2%) | discounted back, us_broad stays within 2% of today's price |
| best estimate | 43,514 | what the payments are worth today |
| own funds | 15,624 | assets minus what is owed, today |
| SCR (1 in 200 year) | 13,066 | the capital that survives a 1-in-200 bad year |
| solvency ratio | 1.20 | own funds / SCR; above 1 means enough capital |

The best estimate is the risk-neutral value of the payments. Own funds are measured on the real-world run, the same way today and after a year: the payments still to come are discounted at each scenario's short rate held flat, 44,376 today at the 4.03% short rate, so the 60,000 leaves own funds of 15,624. In the worst one-year scenario in 200 they fall to 2,558, discounted to today, and the gap of 13,066 is the SCR, which the own funds cover 1.20 times. When plotted, where own funds could be after one year, with today's level and the 1-in-200 outcome marked:

{% include ft-chart.html id="solvency-own-funds" src="/assets/data/financescenarios-guides/solvency.json" label="Distribution of own funds after one year across 2,000 real-world scenarios, discounted to today, with today's own funds and the 1-in-200 outcome" %}

## The Standard Formula

The standard formula replaces the simulation with prescribed shocks ([Delegated Regulation (EU) 2015/35](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj){:target="_blank"}), each calibrated to the same 1-in-200 year: a 99.5% Value-at-Risk over one year ([Solvency II Directive, Article 104(4)](https://eur-lex.europa.eu/eli/dir/2009/138/oj){:target="_blank"}). Two of its sub-modules can be set beside the scenario-based SCR.

**Interest rate risk** (Articles 165 to 167) revalues the liability on EIOPA's basic curve and on its published up and down shocked curves of the same currency, and takes the larger increase ([Delegated Regulation (EU) 2015/35, Article 165(1)](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj#art_165){:target="_blank"}):

$$
\text{SCR}_{ir} = \max\left(BE_{up} - BE,\; BE_{down} - BE,\; 0\right)
$$

Lower rates make future payments dearer, so for most liabilities the down shock binds. A liability in several currencies takes one calculation per currency, and the full sub-module revalues the assets on the same curves.

**Equity risk** (Articles 168 to 172) applies a fixed fall plus EIOPA's symmetric adjustment ([Delegated Regulation (EU) 2015/35, Article 169(1) and (2)](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj#art_169){:target="_blank"}):

| | Shock | Covers |
|:--|:------|:-------|
| Type 1 | 39% plus the symmetric adjustment | Equities listed in the European Economic Area or the OECD |
| Type 2 | 49% plus the symmetric adjustment | All others: unlisted shares, private equity, hedge funds, commodities |

The symmetric adjustment, the "equity dampener", raises both shocks after a rally and lowers them after a fall, so insurers are not pushed to sell into a falling market. It is capped at 10 points either way ([Delegated Regulation (EU) 2015/35, Article 172(4)](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj#art_172){:target="_blank"}), and at 13 points from 30 January 2027 ([Delegated Regulation (EU) 2026/269, Article 1, point (51)](https://eur-lex.europa.eu/eli/reg_del/2026/269/oj){:target="_blank"}). The package applies the cap in force on the valuation date, 10 points when no date is given, and refuses an adjustment beyond it.

The type 1 and type 2 losses, $$L_1$$ and $$L_2$$, combine with a correlation of 0.75:

$$
\text{SCR}_{eq} = \sqrt{L_1^2 + 2 \cdot 0.75 \cdot L_1 L_2 + L_2^2}
$$

The internal-model view and the standard formula can land far apart: the model's 1-in-200 year comes from equity regimes fitted on the history of each market's exchange-traded fund since 2000, while the standard formula prescribes one shock calibrated by the regulator on long equity histories, raised further after a rally by the symmetric adjustment.

### Example {#standard-formula-example}

`equity_scr` gives the equity charge with the symmetric adjustment EIOPA publishes each month. To calculate it for 1,000,000 in type 1 equities and 250,000 in type 2, with the September 2026 adjustment of 7.71 points:

```python
from financescenarios import equity_scr

equity_scr(type_1_value=1_000_000, type_2_value=250_000, symmetric_adjustment=0.0771)
```

Which gives charges of 46.71% and 56.71% (the 39% and 49% base charges plus the adjustment), losses of 467,100 and 141,775, and an equity SCR of 581,048: less than their sum of 608,875, since the two types do not fall perfectly together. `interest_rate_scr` does the same for interest rates, with EIOPA's shocked curves from `eiopa_risk_free_curve`.

## Scenario Files and Currencies

Runs export in the shape liability and asset-liability management (ALM) systems load: one file per variable, one row per scenario, one column per period, plus each variable's [unit](/projects/financescenarios/docs/units). `write_files` exports the risk-neutral run for valuation and the real-world run for projections. The valuation does not convert currencies, so assets, liabilities and the discount rate must share one; convert prices to the reporting currency first.

## What Is Simplified

What the package covers, and what it leaves to you:

| Area | What Finance Scenarios does | What it leaves to you |
|:-----|:----------------------------|:----------------------|
| Technical provisions | The best estimate | The risk margin |
| SCR, internal-model view | A one-run 99.5% VaR of the own-funds path you supply | The asset-liability projection, management actions, the loss-absorbing capacity of technical provisions and deferred taxes, and nested market-consistent revaluation of liabilities inside each one-year scenario (or a proxy such as least-squares Monte Carlo) |
| SCR, standard formula | The interest rate sub-module (liability side) and the equity sub-module | The asset side of interest rate risk, every other module, and the aggregation across them |
| Equity risk | Type 1 and type 2 shocks with the symmetric adjustment | Strategic participations, long-term equity investments, the transitional measure |
| Liabilities in `report` | Revalued at each scenario's short rate, held flat | A full yield curve per scenario |
| Market consistency | The drift: rates grow at the risk-free rate, equities at that rate less their dividend yield, inflation around its breakeven curve | Option prices across strikes, except for an equity with Heston volatility; rate and inflation volatilities come from history, not swaption or inflation-option prices |
| Risk-free curve | Fetches EIOPA's curves, with or without the volatility adjustment, fits the simulated short rate to them, and applies the 2027 extrapolation to a current curve | The matching adjustment and transitional measures |

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">5</span></summary>

- EIOPA (2014). Guidelines on Valuation of Technical Provisions (EIOPA-BoS-14/166). [eiopa.europa.eu](https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en){:target="_blank"}
- European Commission (2015). "Commission Delegated Regulation (EU) 2015/35", Articles 165-167 (interest rate risk) and 168-172 (equity risk and symmetric adjustment). [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj){:target="_blank"}
- European Commission (2025). "Commission Delegated Regulation (EU) 2026/269", amending Delegated Regulation (EU) 2015/35, Articles 46, 46a and 172(4), applying from 30 January 2027. [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/reg_del/2026/269/oj){:target="_blank"}
- European Parliament and Council (2009). "Directive 2009/138/EC (Solvency II)", Articles 76-77 (technical provisions, best estimate) and 101 (SCR at 99.5% over one year). [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/dir/2009/138/oj){:target="_blank"}
- European Parliament and Council (2024). "Directive (EU) 2025/2", amending Directive 2009/138/EC, Articles 77(6)-(7), 77a and 106(3), applying from 30 January 2027. [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/dir/2025/2/oj){:target="_blank"}

</details>

{% include ft-charts-script.html %}
