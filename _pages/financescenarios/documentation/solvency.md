---
title: Solvency II
seo_title: "Solvency II Documentation | Finance Scenarios"
seo_title_suffix: false
excerpt: "Solvency II with Finance Scenarios: the best estimate on a risk-neutral run, the martingale test, EIOPA curves and the UFR, the one-year 99.5% SCR on a real-world run against the standard formula, and what is simplified."
description: "Best estimate, martingale test, EIOPA curves and the SCR under Solvency II: real-world VaR against the standard formula, and where the rules are simplified."
author_profile: false
permalink: /projects/financescenarios/docs/solvency
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Solvency II asks two questions. What is owed, valued at today's market prices (the best estimate, Article 77)? And is there enough capital to keep paying after a 1-in-200 bad year (the Solvency Capital Requirement or SCR, Article 101)? They need different kinds of scenarios:

| Job | Run | Why that run |
|:----|:----|:-------------|
| Best estimate of a liability | Risk neutral (or EIOPA's curve) | A value must reproduce today's market prices, whatever investors expect to earn. |
| Proof the run is fit for valuation | Risk neutral | The martingale test: discounted assets must be worth today's price on average. |
| One-year SCR, internal-model view | Real world | The 1-in-200 loss is about how markets are likely to move, risk premia included. |
| SCR, standard formula | EIOPA's prescribed shocks | Interest rate and equity shocks set by regulation, not by a model. |

<div class="ca-nav">
  <a href="#martingale-test-example"><i class="fas fa-vial" aria-hidden="true"></i>Example run</a>
  <a href="#market-consistency-the-martingale-test"><i class="fas fa-check" aria-hidden="true"></i>Martingale test</a>
  <a href="#eiopas-curve-and-the-ultimate-forward-rate"><i class="fas fa-chart-line" aria-hidden="true"></i>EIOPA curve and UFR</a>
  <a href="#best-estimate"><i class="fas fa-calculator" aria-hidden="true"></i>Best estimate</a>
  <a href="#solvency-capital-requirement"><i class="fas fa-shield-halved" aria-hidden="true"></i>SCR</a>
  <a href="#standard-formula-interest-rate-and-equity-risk"><i class="fas fa-building-columns" aria-hidden="true"></i>Standard formula</a>
  <a href="#scenario-files-and-currencies"><i class="fas fa-file-alt" aria-hidden="true"></i>Scenario files</a>
  <a href="#what-is-simplified"><i class="fas fa-list-check" aria-hidden="true"></i>What is simplified</a>
</div>

<div class="ca-cards">
  <div><i class="ca-icon fas fa-scale-balanced" aria-hidden="true"></i><p class="ca-card-title">Risk neutral</p><p>Grows every traded asset at the risk-free short rate on average, equity prices at that rate minus their dividend yield.</p></div>
  <div><i class="ca-icon fas fa-globe" aria-hidden="true"></i><p class="ca-card-title">Real world</p><p>Keeps the risk premia and mean reversion the model was calibrated on.</p></div>
</div>

A whole-run risk-neutral simulation puts the short rate on a Hull-White process that reproduces EIOPA's risk-free curve for the euro, the pound and the US dollar (the Treasury curve for other currencies), and moves inflation randomly around the bond market's breakeven curve, so the expected price index is the breakeven index; both get their volatility from history, so guarantees and capped indexation get a time value. An entry switched to risk-neutral on its own holds today's rate flat instead (for the US, the 13-week Treasury yield); see [configuration](/projects/financescenarios/docs/configuration#real-world-and-risk-neutral-measures).

Both discount along each scenario with the bank-account deflator, the value today of 1 paid at time $$t$$:

$$
D(t) = \exp\left(-\sum_{s < t} r_s \, \Delta t\right)
$$

where $$r_s$$ is the simulated short rate and $$\Delta t$$ the step length in years. On a risk-neutral run this deflator gives market prices. On a real-world run it gives a discounted expectation, which is what a one-year projection needs but is not a price.

## The Example Run {#martingale-test-example}

The results on this page and in the [Solvency reference](/projects/financescenarios/docs/reference/solvency) come from one risk-neutral run: SPY and US rates, inflation and unemployment, 2,000 scenarios, monthly over ten years, seed 42, calibrated on 2026-10-19. SPY's dividend yield is its own entry so the martingale test can add it back.

```python
from datetime import date

import numpy as np

from financescenarios import Scenarios, ScenariosConfig, best_estimate, martingale_test

config = ScenariosConfig.model_validate(
    {
        "start_date": date(2026, 10, 1),
        "engine": {"n_simulations": 2000, "n_steps": 120, "frequency": "monthly", "seed": 42, "antithetic": True},
        "toolkit": {"start_date": date(2010, 1, 1)},
        "interest_rates": {"defaults": {"measure": "risk_neutral"}, "countries": [{"name": "United States"}]},
        "inflation": {"countries": [{"name": "United States"}]},
        "unemployment": {"countries": [{"name": "United States"}]},
        "equities": [
            {"name": "us_broad", "ticker": "SPY", "measure": "risk_neutral", "volatility_source": "realized"}
        ],
        "dividend_yield": [{"name": "spy_yield", "ticker": "SPY"}],
    }
)
scenarios = Scenarios.from_config(config, api_key="FINANCIAL_MODELING_PREP_KEY")
calibration = scenarios.calibrate(config)
result = scenarios.simulate(config, calibration=calibration)

# Is the run market consistent?
dividend_yield = calibration.calibrated_params["spy_yield"].initial_value
test = martingale_test(result, "us_broad", "united_states_short_rate", dividend_yield=dividend_yield)

# Best estimate of 10,000 a year for ten years, level and indexed to simulated inflation
annuity = np.zeros(len(result.time_grid))
annuity[12::12] = 10_000.0
level = best_estimate(result, annuity, short_rate="united_states_short_rate")
index = result.cumulative_index("united_states_inflation", initial_index=1.0).drop("scenario").to_numpy()
indexed = best_estimate(result, annuity * index, short_rate="united_states_short_rate")
```

The example switches the short rate to risk-neutral on its own, so it is today's 13-week Treasury yield, 4.08%, held flat, and bond prices carry no Monte Carlo error.

## Market Consistency: The Martingale Test

A value is only market consistent if the scenarios reproduce today's prices: a generator used under Solvency II must produce asset prices consistent with those observed in financial markets and assume no arbitrage ([Delegated Regulation (EU) 2015/35, Article 22(3)](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj#art_22){:target="_blank"}).

EIOPA's [guidelines on valuation of technical provisions](https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en){:target="_blank"} (Guideline 58, paragraph 1.105) name the martingale test among the checks on a generator used for valuation, for each asset class used in the calibration and for some simple investment strategies.

<div class="fs-facts">
  <div><span>Run</span><b>Risk neutral</b></div>
  <div><span>Checks</span><b>Discounted price, dividends added back</b></div>
  <div><span>Verdict</span><b>Holm-adjusted p-values at 5%</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/reference/solvency">Solvency</a></div>
</div>

If an asset beats the risk-free cash account on average, every option and guarantee written on it is mispriced, and so is the best estimate. The test is that the discounted price, dividends added back, is a martingale ([Varnell, 2011](https://doi.org/10.1017/S1357321711000079){:target="_blank"}):

$$
\mathbb{E}\left[ D(t)\, S(t)\, e^{q t} \right] = S(0) \quad \text{at every date } t
$$

where $$S$$ is the asset price and $$q$$ its dividend yield. Each date gets a 95% confidence band around the simulated mean and a p-value for the gap between that mean and $$S(0)$$.

With 120 dates each tested at 95%, a correct run still misses about six of them by chance, so requiring every date to pass would fail a true martingale about half the time. The verdict therefore uses [Holm's (1979)](https://www.jstor.org/stable/4615733){:target="_blank"} step-down adjustment for testing many dates at once: the run fails only when the smallest adjusted p-value drops below 5%, which keeps the chance of wrongly failing a correct run at 5% however closely neighboring dates are related. The stricter rule, every date passing, remains available. The pass rate is reported beside the 95% a correct drift gives on average. The example run:

<div class="ca-nums fs-nums">
  <span><b>82%</b>of dates pass</span>
  <span><b>0.92%</b>largest gap to today's price</span>
  <span><b>22 of 120</b>dates just outside the band</span>
</div>

Three of those dates:

| date | ratio to today's price | within band |
|:-----|-----:|:------------|
| 2027-10-01 | 0.9990 | false |
| 2031-10-01 | 0.9993 | true |
| 2036-09-30 | 0.9921 | true |

SPY stays within 0.92% of today's price for all ten years, yet 22 of 120 dates fall just outside a very tight band. Neighboring dates share their paths, so misses come in runs and the pass rate swings from seed to seed. That is Monte Carlo noise, not a wrong drift.

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">When the test really fails</p>

Failing at most dates means the drift is wrong, typically a real-world run tested by mistake; leaving out the dividend yield makes every date fail.
</div>

The one-table Solvency II summary on the [overview page](/projects/financescenarios) uses a practical criterion instead: the run counts as market consistent when the largest gap stays within 2% of today's price. By that measure the example run, at 0.92%, passes.

The rates side has the same test: the bond prices the run implies, $$P(0,t) = \mathbb{E}[D(t)]$$, should match the published curve within about two standard errors. On the example run every maturity prices off the flat 4.08%, from 0.9600 at one year to 0.6652 at ten, so a comparison with EIOPA's curve mostly shows the gap between US Treasury and EIOPA rates.

## EIOPA's Curve and the Ultimate Forward Rate

Solvency II prescribes the discount curve: EIOPA's risk-free term structure, published monthly per currency for maturities of 1 to 150 years ([RFR Technical Documentation, EIOPA-BoS-25-599, paragraph 9.1.6](https://www.eiopa.europa.eu/document/download/f7fca58f-4d24-4441-ac60-de562bf26d77_en#page=43){:target="_blank"}), with or without the volatility adjustment, plus the up and down shocked curves of the standard formula. The package reads it as published, from January 2023 onward.

Market rates are used up to the last liquid point: 20 years for the euro, the only currency where a residual volume criterion sets it ([paragraph 9.2.1](https://www.eiopa.europa.eu/document/download/f7fca58f-4d24-4441-ac60-de562bf26d77_en#page=44){:target="_blank"}), and 30 for the US dollar ([Table 8](https://www.eiopa.europa.eu/document/download/f7fca58f-4d24-4441-ac60-de562bf26d77_en#page=44){:target="_blank"}).

Beyond it EIOPA extrapolates with the Smith-Wilson method ([paragraph 9.1.1](https://www.eiopa.europa.eu/document/download/f7fca58f-4d24-4441-ac60-de562bf26d77_en#page=43){:target="_blank"}) so that forward rates converge to the ultimate forward rate (UFR), a long-term rate the regulator sets: an expected real rate, the same for every currency, plus a currency-specific expected inflation rate ([Annex E, paragraph E.3.3](https://www.eiopa.europa.eu/document/download/f7fca58f-4d24-4441-ac60-de562bf26d77_en#page=123){:target="_blank"}).

For long-dated liabilities the UFR, not the market, drives much of the value. The euro curve for September 2026, extrapolated beyond 20 years:

| maturity (years) | 1 | 10 | 20 | 60 | 150 |
|:---------|--:|---:|---:|---:|----:|
| spot rate | 3.27% | 3.58% | 3.60% | 3.42% | 3.35% |

A whole-run risk-neutral simulation reproduces this curve: its Hull-White short rate reverts toward the path EIOPA's forwards imply, so the average discount factor across scenarios returns EIOPA's bond prices at every maturity, the UFR-driven long end included. The example above holds the Treasury bill rate flat instead.

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">From 30 January 2027</p>

The Solvency II review (Directive (EU) 2025/2 and Delegated Regulation (EU) 2026/269), which applies from 30 January 2027, replaces Smith-Wilson: beyond the first smoothing point (still 20 years for the euro), each forward rate is a weighted average of a last liquid forward rate and the UFR, so market rates keep more weight; from 40 years past the first smoothing point the UFR must carry at least 77.5% of it ([Directive (EU) 2025/2, Article 1, point (39), replacing Article 77a(1) of the Solvency II Directive](https://eur-lex.europa.eu/eli/dir/2025/2/oj){:target="_blank"}). The convergence speed is set by regulation: a parameter of 11% for every currency except the Swedish krona, at 40% ([RFR Technical Documentation, EIOPA-BoS-26-198, paragraph 8.1.5](https://www.eiopa.europa.eu/eiopa-publishes-rfr-technical-documentation-become-applicable-30-january-2027-2026-05-26_en){:target="_blank"}).

An optional phase-in slows the convergence until 2032.
</div>

The package reads whichever curve EIOPA publishes, so the change arrives with EIOPA's own curves. To measure its effect on a best estimate before then, the new method can be applied to a current curve: the published rates up to the first smoothing point, then forwards that blend the last liquid forward rate into the UFR at EIOPA's speed of 11%. Where the forward at 20 years sits below the UFR, long rates come out lower and the best estimate of long-dated liabilities higher.

## Best Estimate

Article 77(2) of the [Solvency II Directive](https://eur-lex.europa.eu/eli/dir/2009/138/oj){:target="_blank"} defines the best estimate as the probability-weighted average of future cash flows, discounted at the relevant risk-free curve.

<div class="fs-facts">
  <div><span>Run</span><b>Risk neutral</b></div>
  <div><span>Discounting</span><b>EIOPA's curve, or the simulated short rate</b></div>
  <div><span>Output</span><b>Best estimate, standard error, 0.5th and 99.5th percentiles</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/reference/solvency">Solvency</a></div>
</div>

Across scenarios, that is the risk-neutral expectation of the discounted future cashflows:

$$
BE = \mathbb{E}^{Q}\left[\sum_t D(t)\, CF(t)\right]
$$

where $$CF(t)$$ is the amount paid at time $$t$$ and $$Q$$ the risk-neutral measure.

For fixed cashflows this collapses to discounting on a curve, which is why plain Solvency II valuation uses EIOPA's curve directly. Scenarios earn their place when cashflows depend on the path: inflation-linked benefits, profit sharing, guarantees and options. From 30 January 2027 the Directive says so explicitly: where contracts include options and guarantees, the best estimate must reflect possible deviations from the expected outcome, not only the expected outcome itself ([Directive (EU) 2025/2, Article 1, point (38), adding Article 77(7)](https://eur-lex.europa.eu/eli/dir/2025/2/oj){:target="_blank"}).

The example run's two annuities:

| annuity | best estimate | standard error | 0.5th percentile | 99.5th percentile |
|:--------|--------------:|---------------:|-----:|------:|
| level | 80,461.77 | 0.00 | 80,461.77 | 80,461.77 |
| inflation-indexed | 93,989.53 | 4.84 | 83,577.47 | 105,641.07 |

Ten yearly payments of 10,000 are worth 80,462 at the flat 4.08%, with no spread across scenarios. Indexed to simulated inflation they are worth 93,990, about 17% more, ranging from about 84,000 to 106,000 across scenarios; a standard error of 5 shows 2,000 scenarios are plenty.

For Solvency II, the discount curve matters. Passing EIOPA's curve to the best estimate discounts each scenario's cashflows on that curve, as Article 77(2) requires. Without it, discounting runs along the simulated short rate: on a whole-run risk-neutral simulation that rate reproduces EIOPA's curve on average, so cashflows that depend on the path of rates or equities (guarantees, profit sharing) are generated and discounted consistently with it. In the example, which holds today's Treasury bill rate flat, they are not.

The time value of those guarantees depends on how much rates and inflation move, and there the run falls short of a full market-consistent calibration, which EIOPA wants based on current data from deep, liquid and transparent financial markets ([Guidelines on valuation of technical provisions, Guideline 57, paragraph 1.101](https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en){:target="_blank"}).

<div class="fs-callout fs-callout--limits" markdown="1">
<p class="fs-callout__title">Limits</p>

Without swaption or inflation-option prices, the rate's volatility is fitted to how much yields across the curve have moved in history (fitted on US Treasuries since 2005, a short-rate volatility of 0.90% a year, which moves the 13-week, 5, 10 and 30-year yields by 89, 82, 76 and 55 basis points a year, against the 69, 87, 85 and 80 they actually moved), and inflation's to its own history. Treat the resulting cost of guarantees as indicative, and replace the volatility with a swaption-implied one for a reported best estimate.
</div>

## Solvency Capital Requirement

Article 101(3) of the [Solvency II Directive](https://eur-lex.europa.eu/eli/dir/2009/138/oj){:target="_blank"} calibrates the SCR to the 99.5% Value-at-Risk of basic own funds (assets minus liabilities) over one year.

The internal-model reading takes that quantile of the simulated one-year loss on a real-world run:

$$
L = OF(0) - D(h)\, OF(h), \qquad \text{SCR} = \max\left(q_{99.5\%}(L),\, 0\right)
$$

where $$OF$$ is own funds, $$h$$ the one-year horizon, $$D(h)$$ the deflator back to today and $$q_{99.5\%}$$ the empirical quantile across scenarios. The Expected Shortfall beyond the SCR shows how bad the tail is past the 1-in-200 point.

On a one-year real-world run of SPY and US rates, 1,000,000 in SPY against a liability of 800,000 growing at the short rate:

<div class="ca-nums fs-nums">
  <span><b>about 25%</b>SCR as a share of the assets</span>
  <span><b>200,000</b>own funds, less than the SCR</span>
  <span><b>79%</b>solvency ratio at seed 42</span>
</div>

That is well below the standard formula's 46.71% type 1 shock [below](#standard-formula-interest-rate-and-equity-risk): the model's 1-in-200 year comes from regimes fitted on SPY since 2005, a period of strong calm-regime returns, while the standard formula prescribes one shock calibrated by the regulator on long equity histories, raised further after a rally by the symmetric adjustment.

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">Check several seeds</p>

Across four seeds the SCR ranged from 250,990 to 279,128, because only 10 of 2,000 scenarios lie beyond the 99.5% quantile. Check several seeds, or use more scenarios, before relying on it.
</div>

The own-funds path is yours to build: assets from a [portfolio](/projects/financescenarios/docs/portfolio), liabilities from your own projection.

## Standard Formula: Interest Rate and Equity Risk

The standard formula replaces the simulation with prescribed shocks ([Delegated Regulation 2015/35](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj){:target="_blank"}), each calibrated to the same 1-in-200 year: a 99.5% Value-at-Risk over one year ([Solvency II Directive, Article 104(4)](https://eur-lex.europa.eu/eli/dir/2009/138/oj){:target="_blank"}).

Two of its sub-modules can be set beside the scenario-based SCR.

**Interest rate risk** (Articles 165 to 167) revalues the liability on EIOPA's basic curve and on its published up and down shocked curves, and takes the larger increase, each summed over currencies ([Delegated Regulation (EU) 2015/35, Article 165(1)](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj#art_165){:target="_blank"}):

$$
\text{SCR}_{ir} = \max\left(BE_{up} - BE,\; BE_{down} - BE,\; 0\right)
$$

Lower rates make future payments dearer, so for most liabilities the down shock binds. For the full sub-module, revalue the assets on the same curves.

**Equity risk** (Articles 168 to 172) applies a fixed fall plus EIOPA's symmetric adjustment ([Delegated Regulation (EU) 2015/35, Article 169(1) and (2)](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj#art_169){:target="_blank"}):

| | Shock | Covers |
|:--|:------|:-------|
| Type 1 | 39% plus the symmetric adjustment | Equities listed in the European Economic Area or the OECD |
| Type 2 | 49% plus the symmetric adjustment | All others: unlisted shares, private equity, hedge funds, commodities |

The symmetric adjustment, the "equity dampener", raises both shocks after a rally and lowers them after a fall, so insurers are not pushed to sell into a falling market. It is capped at 10 points either way ([Delegated Regulation (EU) 2015/35, Article 172(4)](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj#art_172){:target="_blank"}), and at 13 points from 30 January 2027 ([Delegated Regulation (EU) 2026/269, Article 1, point (51)](https://eur-lex.europa.eu/eli/reg_del/2026/269/oj){:target="_blank"}); given a valuation date, the cap in force on that date applies.

The two losses $$L_1$$ and $$L_2$$ combine with a correlation of 0.75:

$$
\text{SCR}_{eq} = \sqrt{L_1^2 + 2 \cdot 0.75 \cdot L_1 L_2 + L_2^2}
$$

With the September 2026 adjustment of 7.71 points, 1,000,000 of type 1 and 250,000 of type 2 equity:

<div class="ca-nums fs-nums">
  <span><b>46.71%</b>type 1 shock</span>
  <span><b>56.71%</b>type 2 shock</span>
  <span><b>581,048</b>equity charge</span>
  <span><b>608,875</b>sum of the two losses</span>
</div>

The charge is less than the sum of the two losses.

## Scenario Files and Currencies

Runs export in the shape liability and ALM systems load: one file per variable, one row per scenario, one column per period, plus each variable's [unit](/projects/financescenarios/docs/units). Export the risk-neutral run for valuation and the real-world run for projections. The valuation does not convert currencies, so assets, liabilities and the discount rate must share one; convert prices to the reporting currency first. The [Solvency reference](/projects/financescenarios/docs/reference/solvency) shows how to summarize such a pair of runs in one table.

## What Is Simplified

What the package covers, and what it leaves to you:

| Area | What Finance Scenarios does | What it leaves to you |
|:-----|:----------------------------|:----------------------|
| Technical provisions | The best estimate | The risk margin |
| SCR, internal-model view | A one-run 99.5% VaR of the own-funds path you supply | The asset-liability projection, management actions, the loss-absorbing capacity of technical provisions and deferred taxes, and nested market-consistent revaluation of liabilities inside each one-year scenario (or a proxy such as least-squares Monte Carlo) |
| SCR, standard formula | The interest rate sub-module (liability side) and the equity sub-module | The asset side of interest rate risk, every other module, and the aggregation across them |
| Equity risk | Type 1 and type 2 shocks with the symmetric adjustment | Strategic participations, long-term equity investments, the transitional measure |
| Liabilities in the combined table | Revalued at each scenario's short rate, held flat | A full yield curve per scenario |
| Market consistency | The drift: rates and equities grow at the risk-free rate, inflation around its breakeven curve | Option prices across strikes, except for an equity with Heston volatility; rate and inflation volatilities come from history, not swaption or inflation-option prices |
| Risk-free curve | Fetches EIOPA's curves, fits the simulated short rate to them, and applies the 2027 extrapolation to a current curve | The volatility adjustment, matching adjustment and transitional measures |

<div class="fs-ref"><a href="/projects/financescenarios/docs/reference/solvency"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Solvency</a></div>

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">12</span></summary>

- European Parliament and Council (2009). "Directive 2009/138/EC (Solvency II)", Articles 76-77 (technical provisions, best estimate) and 101 (SCR at 99.5% over one year). [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/dir/2009/138/oj){:target="_blank"}
- European Commission (2015). "Commission Delegated Regulation (EU) 2015/35", Articles 165-167 (interest rate risk) and 168-172 (equity risk and symmetric adjustment). [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj){:target="_blank"}
- European Parliament and Council (2024). "Directive (EU) 2025/2", amending Directive 2009/138/EC, Articles 77(6)-(7), 77a and 106(3), applying from 30 January 2027. [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/dir/2025/2/oj){:target="_blank"}
- European Commission (2025). "Commission Delegated Regulation (EU) 2026/269", amending Delegated Regulation (EU) 2015/35, Articles 46, 46a and 172(4), applying from 30 January 2027. [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/reg_del/2026/269/oj){:target="_blank"}
- EIOPA (2015, updated 2023). "Guidelines on valuation of technical provisions." [eiopa.europa.eu](https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en){:target="_blank"}
- EIOPA. "Risk-free interest rate term structures." [eiopa.europa.eu](https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en){:target="_blank"}
- EIOPA (2026). "RFR Technical Documentation" (EIOPA-BoS-26-198), applicable from 30 January 2027, section 8. [eiopa.europa.eu](https://www.eiopa.europa.eu/eiopa-publishes-rfr-technical-documentation-become-applicable-30-january-2027-2026-05-26_en){:target="_blank"}
- EIOPA (2025). "RFR Technical Documentation" (EIOPA-BoS-25-599), sections 9.1-9.4 and Annex E. [eiopa.europa.eu](https://www.eiopa.europa.eu/document/download/f7fca58f-4d24-4441-ac60-de562bf26d77_en){:target="_blank"}
- EIOPA. "Symmetric adjustment of the equity capital charge." [eiopa.europa.eu](https://www.eiopa.europa.eu/tools-and-data/symmetric-adjustment-equity-capital-charge_en){:target="_blank"}
- Holm, S. (1979). "A Simple Sequentially Rejective Multiple Test Procedure." Scandinavian Journal of Statistics, 6(2), 65-70. [jstor.org](https://www.jstor.org/stable/4615733){:target="_blank"}
- Varnell, E.M. (2011). "Economic Scenario Generators and Solvency II." British Actuarial Journal, 16(1), 121-159. [doi.org](https://doi.org/10.1017/S1357321711000079){:target="_blank"}
- Wüthrich, M.V., Merz, M. (2013). "Financial Modeling, Actuarial Valuation and Solvency in Insurance." Springer. [doi.org](https://doi.org/10.1007/978-3-642-31392-9){:target="_blank"}

</details>
