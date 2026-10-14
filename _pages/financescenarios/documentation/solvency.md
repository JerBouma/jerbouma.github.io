---
title: Solvency II
seo_title: Solvency II Documentation – Finance Scenarios
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

Solvency II asks two questions. What is owed, valued at today's market prices (the best estimate, Article 77)? And is there enough capital to keep paying after a 1-in-200 bad year (the Solvency Capital Requirement or SCR, Article 101)? They need different kinds of scenarios.

| Job | Run | Why that run |
|:----|:----|:-------------|
| Best estimate of a liability | Risk neutral (or EIOPA's curve) | A value must reproduce today's market prices, whatever investors expect to earn. |
| Proof the run is fit for valuation | Risk neutral | The martingale test: discounted assets must be worth today's price on average. |
| One-year SCR, internal-model view | Real world | The 1-in-200 loss is about how markets are likely to move, risk premia included. |
| SCR, standard formula | EIOPA's prescribed shocks | Interest rate and equity shocks set by regulation, not by a model. |

A *risk-neutral* run grows every traded asset at the risk-free short rate on average, equity prices at that rate minus their dividend yield. A whole-run risk-neutral simulation puts the short rate on a Hull-White process that reproduces EIOPA's risk-free curve for the euro, the pound and the US dollar (the Treasury curve for other currencies), and moves inflation randomly around the bond market's breakeven curve, so the expected price index is the breakeven index; both get their volatility from history, so guarantees and capped indexation get a time value. An entry switched to risk-neutral on its own holds today's rate flat instead (for the US, the 13-week Treasury yield); see [configuration](/projects/financescenarios/docs/configuration#real-world-and-risk-neutral-measures). A *real-world* run keeps the risk premia and mean reversion the model was calibrated on.

Both discount along each scenario with the bank-account deflator, the value today of 1 paid at time $$t$$:

$$
D(t) = \exp\left(-\sum_{s < t} r_s \, \Delta t\right)
$$

where $$r_s$$ is the simulated short rate and $$\Delta t$$ the step length in years. On a risk-neutral run this deflator gives market prices. On a real-world run it gives a discounted expectation, which is what a one-year projection needs but is not a price.

## The Example Run {#martingale-test-example}

The results on this page and in the [Solvency reference](/projects/financescenarios/docs/reference/solvency) come from one risk-neutral run: SPY and US rates, inflation and unemployment, 2,000 scenarios, monthly over ten years, seed 42, calibrated on 2026-10-14. SPY's dividend yield is its own entry so the martingale test can add it back.

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

The example switches the short rate to risk-neutral on its own, so it is today's 13-week Treasury yield, 4.06%, held flat, and bond prices carry no Monte Carlo error.

## Market Consistency: The Martingale Test

A value is only market consistent if the scenarios reproduce today's prices.

> "Where insurance and reinsurance undertakings use a model to produce projections of future financial market parameters, it shall comply with all of the following requirements: (a) it generates asset prices that are consistent with asset prices observed in financial markets; (b) it assumes no arbitrage opportunity; …"
> <cite>[Delegated Regulation (EU) 2015/35, Article 22(3)](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj#art_22)</cite>

EIOPA's guidelines name the martingale test among the checks on a generator used for valuation.

> "To demonstrate the market consistency properties of the ESG, at least some of the following tests should be carried out on the set of scenarios generated by the ESG used for valuation: … (b) Martingale tests: verify the Martingale test for the asset classes (equity, bonds, property, exchange rates, etc.) that have been used in the calibration process of the ESG, and for some simple portfolio investment strategies;"
> <cite>[EIOPA, Guidelines on valuation of technical provisions (EIOPA-BoS-14/166), Guideline 58, paragraph 1.105](https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en)</cite>

If an asset beats the risk-free cash account on average, every option and guarantee written on it is mispriced, and so is the best estimate. The test is that the discounted price, dividends added back, is a martingale ([Varnell, 2011](https://doi.org/10.1017/S1357321711000079){:target="_blank"}):

$$
\mathbb{E}\left[ D(t)\, S(t)\, e^{q t} \right] = S(0) \quad \text{at every date } t
$$

where $$S$$ is the asset price and $$q$$ its dividend yield. Each date gets a 95% confidence band around the simulated mean and a p-value for the gap between that mean and $$S(0)$$.

With 120 dates each tested at 95%, a correct run still misses about six of them by chance, so requiring every date to pass would fail a true martingale about half the time. The verdict therefore uses [Holm's (1979)](https://www.jstor.org/stable/4615733){:target="_blank"} step-down adjustment for testing many dates at once: the run fails only when the smallest adjusted p-value drops below 5%, which keeps the chance of wrongly failing a correct run at 5% however closely neighboring dates are related. The stricter every-date rule remains available (`criterion="every_date"`). The pass rate is reported beside the 95% a correct drift gives on average. The example run passes 80% of dates, with a largest gap of 0.94%.

| date | ratio to today's price | within band |
|:-----|-----:|:------------|
| 2027-10-01 | 0.9990 | false |
| 2031-10-01 | 0.9992 | true |
| 2036-09-30 | 0.9918 | false |

SPY stays within 0.94% of today's price for all ten years, yet 24 of 120 dates fall just outside a very tight band. Neighboring dates share their paths, so misses come in runs and the pass rate swings from seed to seed. That is Monte Carlo noise, not a wrong drift. Failing at most dates means the drift is wrong, typically a real-world run tested by mistake; leaving out the dividend yield makes every date fail.

The one-table Solvency II summary on the [overview page](/projects/financescenarios) uses a practical criterion instead: the run counts as market consistent when the largest gap stays within 2% of today's price. By that measure the example run, at 0.94%, passes.

The rates side has the same test: the bond prices the run implies, $$P(0,t) = \mathbb{E}[D(t)]$$, should match the published curve within about two standard errors. On the example run every maturity prices off the flat 4.06%, from 0.9602 at one year to 0.6663 at ten, so a comparison with EIOPA's curve mostly shows the gap between US Treasury and EIOPA rates.

## EIOPA's Curve and the Ultimate Forward Rate

Solvency II prescribes the discount curve: EIOPA's risk-free term structure, published monthly per currency for maturities of 1 to 150 years, with or without the volatility adjustment, plus the up and down shocked curves of the standard formula. The package reads it as published, from January 2023 onward.

> "EIOPA publishes the risk-free interest rates for integer maturities from one year to 150 years."
> <cite>[EIOPA, RFR Technical Documentation (EIOPA-BoS-25-599), paragraph 9.1.6](https://www.eiopa.europa.eu/document/download/f7fca58f-4d24-4441-ac60-de562bf26d77_en#page=43)</cite>

Market rates are used up to the last liquid point, 20 years for the euro and 30 for the US dollar.

> "The residual volume criterion is used to derive the LLP for the euro only. For that currency, it gives an LLP of 20 years."
> <cite>[EIOPA, RFR Technical Documentation (EIOPA-BoS-25-599), paragraph 9.2.1; US dollar in Table 8](https://www.eiopa.europa.eu/document/download/f7fca58f-4d24-4441-ac60-de562bf26d77_en#page=44)</cite>

Beyond it EIOPA extrapolates with the Smith-Wilson method so that forward rates converge to the ultimate forward rate (UFR), a long-term rate the regulator sets.

> "Both the interpolation between these maturities, where necessary, and the extrapolation beyond the last liquid point are based on the Smith-Wilson methodology."
> <cite>[EIOPA, RFR Technical Documentation (EIOPA-BoS-25-599), paragraph 9.1.1](https://www.eiopa.europa.eu/document/download/f7fca58f-4d24-4441-ac60-de562bf26d77_en#page=43)</cite>

> "For each currency the UFR before limitation of the annual change is the sum of an expected real rate and an expected inflation rate. The expected real rate is the same for each currency. The expected inflation rate is currency specific."
> <cite>[EIOPA, RFR Technical Documentation (EIOPA-BoS-25-599), Annex E, paragraph E.3.3](https://www.eiopa.europa.eu/document/download/f7fca58f-4d24-4441-ac60-de562bf26d77_en#page=123)</cite>

For long-dated liabilities the UFR, not the market, drives much of the value. The euro curve for September 2026, extrapolated beyond 20 years:

| maturity (years) | 1 | 10 | 20 | 60 | 150 |
|:---------|--:|---:|---:|---:|----:|
| spot rate | 3.27% | 3.58% | 3.60% | 3.42% | 3.35% |

A whole-run risk-neutral simulation reproduces this curve: its Hull-White short rate reverts toward the path EIOPA's forwards imply, so the average discount factor across scenarios returns EIOPA's bond prices at every maturity, the UFR-driven long end included. The example above holds the Treasury bill rate flat instead.

The Solvency II review (Directive (EU) 2025/2 and Delegated Regulation (EU) 2026/269), which applies from 30 January 2027, replaces Smith-Wilson: beyond the first smoothing point (still 20 years for the euro), each forward rate is a weighted average of a last liquid forward rate and the UFR, so market rates keep more weight. The convergence speed is set by regulation:

> "In accordance with Articles 46(1b) and 46a of the Delegated Regulation, the convergence parameter α equals 40% for the Swedish Krona and 11% for all other currencies, except when insurance or reinsurance undertakings are allowed to apply the phasing-in mechanism referred to in Article 77a(2) of the Solvency II Directive."
> <cite>[EIOPA, RFR Technical Documentation (EIOPA-BoS-26-198), paragraph 8.1.5](https://www.eiopa.europa.eu/eiopa-publishes-rfr-technical-documentation-become-applicable-30-january-2027-2026-05-26_en)</cite>

An optional phase-in slows the convergence until 2032.

> "The extrapolated forward rate shall be equal to a weighted average of a liquid forward rate and the UFR. The liquid forward rate shall be based on one or a set of forward rates in relation to the longest maturities for which the relevant financial instrument can be observed in a deep, liquid and transparent market. For maturities of at least 40 years past the first smoothing point the weight of the UFR shall be at least 77,5 %."
> <cite>[Directive (EU) 2025/2, Article 1, point (39), replacing Article 77a(1) of Directive 2009/138/EC](https://eur-lex.europa.eu/eli/dir/2025/2/oj)</cite>

The package reads whichever curve EIOPA publishes, so the change arrives with EIOPA's own curves. To measure its effect on a best estimate before then, the new method can be applied to a current curve: the published rates up to the first smoothing point, then forwards that blend the last liquid forward rate into the UFR at EIOPA's speed of 11%. Where the forward at 20 years sits below the UFR, long rates come out lower and the best estimate of long-dated liabilities higher.

## Best Estimate

The best estimate is the risk-neutral expectation of the discounted future cashflows:

$$
BE = \mathbb{E}^{Q}\left[\sum_t D(t)\, CF(t)\right]
$$

where $$CF(t)$$ is the amount paid at time $$t$$ and $$Q$$ the risk-neutral measure.

> "The best estimate shall correspond to the probability-weighted average of future cash-flows, taking account of the time value of money (expected present value of future cash-flows), using the relevant risk-free interest rate term structure."
> <cite>[Directive 2009/138/EC, Article 77(2)](https://eur-lex.europa.eu/eli/dir/2009/138/oj)</cite>

For fixed cashflows this collapses to discounting on a curve, which is why plain Solvency II valuation uses EIOPA's curve directly. Scenarios earn their place when cashflows depend on the path: inflation-linked benefits, profit sharing, guarantees and options.

> "Where insurance and reinsurance contracts include financial options and guarantees, the methods used to calculate the best estimate shall appropriately reflect that the present value of cash flows arising from those contracts may depend both on the expected outcome of future events and developments and on potential deviations of the actual outcome from the expected outcome in certain scenarios."
> <cite>[Directive (EU) 2025/2, Article 1, point (38), adding Article 77(7) to Directive 2009/138/EC (applies from 30 January 2027)](https://eur-lex.europa.eu/eli/dir/2025/2/oj)</cite>

| annuity | best estimate | standard error | 0.5th percentile | 99.5th percentile |
|:--------|--------------:|---------------:|-----:|------:|
| level | 80,532.45 | 0.00 | 80,532.45 | 80,532.45 |
| inflation-indexed | 93,976.96 | 6.15 | 83,336.15 | 106,135.94 |

Ten yearly payments of 10,000 are worth 80,532 at the flat 4.06%, with no spread across scenarios. Indexed to simulated inflation they are worth 93,977, about 17% more, ranging from about 83,000 to 106,000 across scenarios; a standard error of 6 shows 2,000 scenarios are plenty.

For Solvency II, the discount curve matters. Passing EIOPA's curve to the best estimate discounts each scenario's cashflows on that curve, as Article 77(2) requires. Without it, discounting runs along the simulated short rate: on a whole-run risk-neutral simulation that rate reproduces EIOPA's curve on average, so cashflows that depend on the path of rates or equities (guarantees, profit sharing) are generated and discounted consistently with it. In the example, which holds today's Treasury bill rate flat, they are not.

The time value of those guarantees depends on how much rates and inflation move, and there the run falls short of a full market-consistent calibration. EIOPA asks for market data:

> "Insurance and reinsurance undertakings should ensure that the calibration process of an ESG used for a market consistent valuation is based on data from financial markets that are deep, liquid and transparent as defined in Article 1 of Commission Delegated Regulation 2015/35 and that reflect the current market conditions."
> <cite>[EIOPA, Guidelines on valuation of technical provisions (EIOPA-BoS-14/166), Guideline 57, paragraph 1.101](https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en)</cite>

Without swaption or inflation-option prices, the rate's volatility is fitted to how much yields across the curve have moved in history (fitted on US Treasuries since 2005, a short-rate volatility of 0.90% a year, which moves the 13-week, 5, 10 and 30-year yields by 89, 82, 75 and 55 basis points a year, against the 69, 87, 85 and 79 they actually moved), and inflation's to its own history. Treat the resulting cost of guarantees as indicative, and replace the volatility with a swaption-implied one for a reported best estimate.

## Solvency Capital Requirement

Article 101 calibrates the SCR to the 99.5% Value-at-Risk of basic own funds (assets minus liabilities) over one year.

> "It shall correspond to the Value-at-Risk of the basic own funds of an insurance or reinsurance undertaking subject to a confidence level of 99,5 % over a one-year period."
> <cite>[Directive 2009/138/EC, Article 101(3)](https://eur-lex.europa.eu/eli/dir/2009/138/oj)</cite>

The internal-model reading takes that quantile of the simulated one-year loss on a real-world run:

$$
L = OF(0) - D(h)\, OF(h), \qquad \text{SCR} = \max\left(q_{99.5\%}(L),\, 0\right)
$$

where $$OF$$ is own funds, $$h$$ the one-year horizon, $$D(h)$$ the deflator back to today and $$q_{99.5\%}$$ the empirical quantile across scenarios. The Expected Shortfall beyond the SCR shows how bad the tail is past the 1-in-200 point.

On a one-year real-world run of SPY and US rates, 1,000,000 in SPY against a liability of 800,000 growing at the short rate gave an SCR of about a quarter of the assets, more than the 200,000 of own funds: a solvency ratio of 79% at seed 42. That is well below the standard formula's 46.71% type 1 shock [below](#standard-formula-interest-rate-and-equity-risk): the model's 1-in-200 year comes from regimes fitted on SPY since 2005, a period of strong calm-regime returns, while the standard formula prescribes one shock calibrated by the regulator on long equity histories, raised further after a rally by the symmetric adjustment. Across four seeds the SCR ranged from 250,819 to 284,117, because only 10 of 2,000 scenarios lie beyond the 99.5% quantile. Check several seeds, or use more scenarios, before relying on it.

The own-funds path is yours to build: assets from a [portfolio](/projects/financescenarios/docs/portfolio), liabilities from your own projection.

## Standard Formula: Interest Rate and Equity Risk

The standard formula replaces the simulation with prescribed shocks ([Delegated Regulation 2015/35](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj){:target="_blank"}), each calibrated to the same 1-in-200 year.

> "Each of the risk modules referred to in paragraph 1 shall be calibrated using a Value-at-Risk measure, with a 99,5 % confidence level, over a one-year period."
> <cite>[Directive 2009/138/EC, Article 104(4)](https://eur-lex.europa.eu/eli/dir/2009/138/oj)</cite>

Two of its sub-modules can be set beside the scenario-based SCR.

**Interest rate risk** (Articles 165 to 167) revalues the liability on EIOPA's basic curve and on its published up and down shocked curves, and takes the larger increase:

$$
\text{SCR}_{ir} = \max\left(BE_{up} - BE,\; BE_{down} - BE,\; 0\right)
$$

> "The capital requirement for interest rate risk … shall be equal to the larger of the following: (a) the sum, over all currencies, of the capital requirements for the risk of an increase in the term structure of interest rates … (b) the sum, over all currencies, of the capital requirements for the risk of a decrease in the term structure of interest rates …"
> <cite>[Delegated Regulation (EU) 2015/35, Article 165(1)](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj#art_165)</cite>

Lower rates make future payments dearer, so for most liabilities the down shock binds. For the full sub-module, revalue the assets on the same curves.

**Equity risk** (Articles 168 to 172) applies a fixed fall plus EIOPA's symmetric adjustment:

| | Shock | Covers |
|:--|:------|:-------|
| Type 1 | 39% plus the symmetric adjustment | Equities listed in the European Economic Area or the OECD |
| Type 2 | 49% plus the symmetric adjustment | All others: unlisted shares, private equity, hedge funds, commodities |

> "The capital requirement for type 1 equities … shall be equal to the loss in the basic own funds that would result from the following instantaneous decreases: … (b) an instantaneous decrease equal to the sum of 39 % and the symmetric adjustment as referred to in Article 172 of this Regulation, in the value of type 1 equities other than those referred to in point (a)."
> <cite>[Delegated Regulation (EU) 2015/35, Article 169(1); 49% for type 2 in Article 169(2)](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj#art_169)</cite>

The symmetric adjustment, the "equity dampener", raises both shocks after a rally and lowers them after a fall, so insurers are not pushed to sell into a falling market. It is capped at 10 points either way, and at 13 points from 30 January 2027; given a valuation date, the cap in force on that date applies.

> "The symmetric adjustment shall not be lower than – 10 % or higher than 10 %."
> <cite>[Delegated Regulation (EU) 2015/35, Article 172(4)](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj#art_172)</cite>

> "The symmetric adjustment shall not be lower than – 13 % or higher than 13 %."
> <cite>[Delegated Regulation (EU) 2026/269, Article 1, point (51), replacing Article 172(4) of Delegated Regulation (EU) 2015/35 (applies from 30 January 2027)](https://eur-lex.europa.eu/eli/reg_del/2026/269/oj)</cite>

The two losses $$L_1$$ and $$L_2$$ combine with a correlation of 0.75:

$$
\text{SCR}_{eq} = \sqrt{L_1^2 + 2 \cdot 0.75 \cdot L_1 L_2 + L_2^2}
$$

With the September 2026 adjustment of 7.71 points, 1,000,000 of type 1 and 250,000 of type 2 equity face shocks of 46.71% and 56.71%, and an equity charge of 581,048, less than the 608,875 sum of the two losses.

## Scenario Files and Currencies

Runs export in the shape liability and ALM systems load: one file per variable, one row per scenario, one column per period, plus each variable's [unit](/projects/financescenarios/docs/units). Export the risk-neutral run for valuation and the real-world run for projections. The valuation does not convert currencies, so assets, liabilities and the discount rate must share one; convert prices to the reporting currency first. The [Solvency reference](/projects/financescenarios/docs/reference/solvency) shows how to summarize such a pair of runs in one table.

## What Is Simplified

| Area | What Finance Scenarios does | What it leaves to you |
|:-----|:----------------------------|:----------------------|
| Technical provisions | The best estimate | The risk margin |
| SCR, internal-model view | A one-run 99.5% VaR of the own-funds path you supply | The asset-liability projection, management actions, the loss-absorbing capacity of technical provisions and deferred taxes, and nested market-consistent revaluation of liabilities inside each one-year scenario (or a proxy such as least-squares Monte Carlo) |
| SCR, standard formula | The interest rate sub-module (liability side) and the equity sub-module | The asset side of interest rate risk, every other module, and the aggregation across them |
| Equity risk | Type 1 and type 2 shocks with the symmetric adjustment | Strategic participations, long-term equity investments, the transitional measure |
| Liabilities in the combined table | Revalued at each scenario's short rate, held flat | A full yield curve per scenario |
| Market consistency | The drift: rates and equities grow at the risk-free rate, inflation around its breakeven curve | Option prices across strikes, except for an equity with Heston volatility; rate and inflation volatilities come from history, not swaption or inflation-option prices |
| Risk-free curve | Fetches EIOPA's curves, fits the simulated short rate to them, and applies the 2027 extrapolation to a current curve | The volatility adjustment, matching adjustment and transitional measures |

## References

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
