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

Solvency II asks two questions. What is owed, valued at today's market prices (the best estimate, Article 77)? And is there enough capital to keep paying it after a 1-in-200 bad year (the Solvency Capital Requirement or SCR, Article 101)? They need two different kinds of scenarios.

| Job | Run | Why that run |
|:----|:----|:-------------|
| Best estimate of a liability | Risk neutral (or EIOPA's curve) | A value must reproduce today's market prices, whatever investors expect to earn. |
| Proof the run is fit for valuation | Risk neutral | The martingale test: discounted assets must be worth today's price on average. |
| One-year SCR, internal-model view | Real world | The 1-in-200 loss is about how markets are likely to move, risk premia included. |
| SCR, standard formula | EIOPA's prescribed shocks | Interest rate and equity shocks set by regulation, not by a model. |

A *risk-neutral* run grows every traded asset at the risk-free rate on average: rates follow today's curve and equities grow at that rate minus their dividend yield (see [configuration](/projects/financescenarios/docs/configuration#real-world-and-risk-neutral-measures)). A *real-world* run keeps the risk premia and mean reversion the model was calibrated on.

Both are discounted along each scenario with the bank account, the value today of 1 paid at time $$t$$:

$$
D(t) = \exp\left(-\sum_{s < t} r_s \, \Delta t\right)
$$

where $$r_s$$ is the simulated short rate and $$\Delta t$$ the step length in years. On a risk-neutral run this deflator gives market prices. On a real-world run it gives a discounted expectation, which is what a one-year projection needs but is not a price.

## The Example Run {#martingale-test-example}

The results on this page and in the [Solvency reference](/projects/financescenarios/docs/reference/solvency) come from one risk-neutral run: SPY and US rates, inflation and unemployment, 2,000 scenarios, monthly over ten years, seed 42, calibrated on 2026-10-04. SPY's dividend yield is its own entry so the martingale test can add it back.

```python
from datetime import date

import numpy as np

from financescenarios import Scenarios, best_estimate, martingale_test
from financescenarios.config.config_model import ScenariosConfig

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

The risk-neutral short rate is today's 13-week Treasury yield, 3.993%, held flat, so bond prices carry no Monte Carlo error.

## Market Consistency: The Martingale Test

A value is only market consistent if the scenarios reproduce today's prices; EIOPA's guidelines expect this of a generator used for valuation. If the scenarios let an asset beat the risk-free cash account on average, every option and guarantee written on that asset is mispriced, and so is the best estimate. The test is that the discounted price, dividends added back, is a martingale ([Varnell, 2011](https://doi.org/10.1017/S1357321711000079){:target="_blank"}):

$$
\mathbb{E}\left[ D(t)\, S(t)\, e^{q t} \right] = S(0) \quad \text{at every date } t
$$

where $$S$$ is the asset price and $$q$$ its dividend yield. Each date passes when $$S(0)$$ lies inside a 95% confidence band around the simulated mean.

The example run fails strictly (82.5% of dates pass, largest gap 0.91%):

| date | ratio to today's price | within band |
|:-----|-----:|:------------|
| 2027-10-01 | 0.9990 | false |
| 2028-09-30 | 0.9996 | true |
| 2031-10-01 | 0.9994 | true |
| 2036-09-30 | 0.9922 | true |

SPY stays within 0.9% of today's price for all ten years, yet 21 of 120 dates fall just outside a very tight band. Seeds 2 and 3 pass everywhere and seed 42 passes at 99% confidence: Monte Carlo noise, not a wrong drift. Failing at most dates means the drift is wrong, typically a real-world run tested by mistake; leaving out the dividend yield makes every date fail.

The rates side has the same test: the bond prices the run implies, $$P(0,t) = \mathbb{E}[D(t)]$$, should match the published curve within about two standard errors. On the example run every maturity prices off the flat 3.993%, from 0.9609 at one year to 0.6708 at ten.

## EIOPA's Curve and the Ultimate Forward Rate

Solvency II prescribes the discount curve: EIOPA's risk-free term structure, published monthly per currency for 1 to 150 years, with or without the volatility adjustment, plus shocked versions for the standard formula. It is read as published, from January 2023 onward.

Market rates are used up to the last liquid point, 20 years for the euro. Beyond it EIOPA extrapolates with the Smith-Wilson method so that forward rates converge to the ultimate forward rate (UFR), a long-term rate the regulator sets. For long-dated liabilities the UFR, not the market, drives much of the value. The euro curve for September 2026:

| maturity (years) | 1 | 10 | 20 | 60 | 150 |
|:---------|--:|---:|---:|---:|----:|
| spot rate | 3.27% | 3.58% | 3.60% | 3.42% | 3.35% |

The simulated risk-neutral rate is fitted to its own market data, not to EIOPA's curve; comparing the two shows how far apart they are.

## Best Estimate

The best estimate is the risk-neutral expectation of the discounted future cashflows:

$$
BE = \mathbb{E}^{Q}\left[\sum_t D(t)\, CF(t)\right]
$$

where $$CF(t)$$ is the amount paid at time $$t$$ and $$Q$$ the risk-neutral measure. For fixed cashflows this collapses to discounting on a curve, which is why plain Solvency II valuation uses EIOPA's curve directly. Scenarios earn their place when cashflows depend on the path: inflation-linked benefits, profit sharing, guarantees and options.

The example shows the difference:

| annuity | best estimate | standard error | 0.5th percentile | 99.5th percentile |
|:--------|--------------:|---------------:|-----:|------:|
| level | 80,811.82 | 0.00 | 80,811.82 | 80,811.82 |
| inflation-indexed | 93,142.15 | 4.05 | 83,990.68 | 103,236.21 |

Ten yearly payments of 10,000 are worth 80,812 at a flat 3.99%; indexed to simulated inflation, 93,142, ranging from about 84,000 to 103,000 across scenarios. A standard error of 4 shows 2,000 scenarios are plenty. Discounting on EIOPA's curve instead is a single switch. The risk margin is not computed.

## Solvency Capital Requirement

The internal-model reading of Article 101 is the 99.5% Value-at-Risk of the one-year loss in own funds (assets minus liabilities), measured on a real-world run:

$$
L = OF(0) - D(h)\, OF(h), \qquad \text{SCR} = \max\left(q_{99.5\%}(L),\, 0\right)
$$

where $$OF$$ is own funds, $$h$$ the one-year horizon, $$D(h)$$ discounts back to today and $$q_{99.5\%}$$ is the empirical quantile across scenarios. The Expected Shortfall beyond the SCR shows how bad the tail is past the 1-in-200 point.

On a one-year real-world run of SPY and US rates, 1,000,000 in SPY against a liability of 800,000 growing at the short rate gave an SCR of about a quarter of the assets, more than the 200,000 of own funds: a solvency ratio of 79% at seed 42. Across four seeds the SCR ranged from 250,819 to 284,117, because only 10 of 2,000 scenarios lie beyond the 99.5% quantile. Check several seeds, or raise the number of scenarios, before relying on it.

The own-funds path is yours to build: assets from a [portfolio](/projects/financescenarios/docs/portfolio), liabilities from your own projection. A full internal model would also revalue the liabilities market-consistently inside every one-year scenario (nested stochastics, or a proxy such as least-squares Monte Carlo); that is not done here.

## Standard Formula: Interest Rate and Equity Risk

The standard formula replaces the simulation with prescribed shocks ([Delegated Regulation 2015/35](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj){:target="_blank"}). Two sub-modules are available to set beside the scenario-based SCR.

**Interest rate risk** (Articles 165 to 167) revalues the liability on EIOPA's base curve and on its upward and downward shocked curves and takes the larger increase:

$$
\text{SCR}_{ir} = \max\left(BE_{up} - BE,\; BE_{down} - BE,\; 0\right)
$$

Lower rates make future payments dearer, so for most liabilities the down shock binds. Only the liability side is revalued; the assets must be revalued on the same curves for the full sub-module.

**Equity risk** (Articles 168 to 169) applies a fixed fall plus EIOPA's symmetric adjustment:

| | Shock | Covers |
|:--|:------|:-------|
| Type 1 | 39% plus the symmetric adjustment | Equities listed in the European Economic Area or the OECD |
| Type 2 | 49% plus the symmetric adjustment | All others: unlisted shares, private equity, hedge funds, commodities |

The symmetric adjustment, the "equity dampener", raises both shocks by up to 10 points after a rally and lowers them by up to 10 points after a fall, so insurers are not pushed to sell into a falling market. The two losses $$L_1$$ and $$L_2$$ combine with a correlation of 0.75:

$$
\text{SCR}_{eq} = \sqrt{L_1^2 + 2 \cdot 0.75 \cdot L_1 L_2 + L_2^2}
$$

With the September 2026 adjustment of 7.71 points, 1,000,000 of type 1 and 250,000 of type 2 equity face shocks of 46.71% and 56.71%, and an equity charge of 581,048, less than the 608,875 sum of the two losses.

## Scenario Files and Currencies

Runs export in the shape liability and ALM systems load: one file per variable, one row per trial, one column per period, plus each variable's [unit](/projects/financescenarios/docs/units). Export the risk-neutral run for valuation and the real-world run for projections. Nothing converts currencies: assets, liabilities and the discount rate must share one. Market consistency, best estimate, own funds, SCR and solvency ratio can also be read off a pair of runs in one table; see the [Solvency reference](/projects/financescenarios/docs/reference/solvency).

## What Is Simplified

| Area | What Finance Scenarios does | What it leaves to you |
|:-----|:----------------------------|:----------------------|
| Technical provisions | The best estimate | The risk margin |
| SCR, internal-model view | A one-run 99.5% VaR of the own-funds path you supply | The asset-liability projection, management actions, taxes, loss-absorbing capacity of technical provisions and deferred taxes, and nested revaluation of liabilities inside each one-year scenario |
| SCR, standard formula | The interest rate sub-module (liability side) and the equity sub-module | Every other module, and the aggregation across them |
| Equity risk | Type 1 and type 2 shocks with the symmetric adjustment | Strategic participations, long-term equity investments, the transitional measure |
| Liabilities in the combined table | Revalued at each scenario's short rate, held flat | A full yield curve per scenario |
| Market consistency | The drift: rates and equities grow at the risk-free rate | Option prices across strikes, except for an equity with Heston volatility; elsewhere volatility is a single number |
| Risk-free curve | Fetches EIOPA's curves and compares against them | Calibrating the simulated short rate to EIOPA's curve |

Check market consistency on every risk-neutral run before valuing on it, and check the SCR at more than one seed.

## References

- European Parliament and Council (2009). "Directive 2009/138/EC (Solvency II)", Articles 76-77 (technical provisions, best estimate) and 101 (SCR at 99.5% over one year). [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/dir/2009/138/oj){:target="_blank"}
- European Commission (2015). "Commission Delegated Regulation (EU) 2015/35", Articles 165-167 (interest rate risk) and 168-172 (equity risk and symmetric adjustment). [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj){:target="_blank"}
- EIOPA (2015, updated 2023). "Guidelines on valuation of technical provisions." [eiopa.europa.eu](https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en){:target="_blank"}
- EIOPA. "Risk-free interest rate term structures." [eiopa.europa.eu](https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en){:target="_blank"}
- EIOPA. "Symmetric adjustment of the equity capital charge." [eiopa.europa.eu](https://www.eiopa.europa.eu/tools-and-data/symmetric-adjustment-equity-capital-charge_en){:target="_blank"}
- Varnell, E.M. (2011). "Economic Scenario Generators and Solvency II." British Actuarial Journal, 16(1), 121-159. [doi.org](https://doi.org/10.1017/S1357321711000079){:target="_blank"}
- Wüthrich, M.V., Merz, M. (2013). "Financial Modeling, Actuarial Valuation and Solvency in Insurance." Springer. [doi.org](https://doi.org/10.1007/978-3-642-31392-9){:target="_blank"}
