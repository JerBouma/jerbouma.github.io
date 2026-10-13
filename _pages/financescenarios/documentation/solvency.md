---
title: Solvency II
seo_title: Solvency II Documentation – Finance Scenarios
excerpt: "How Finance Scenarios values liabilities on a risk-neutral run and measures the one-year capital requirement on a real-world run, with the martingale test, EIOPA curves, standard-formula interest rate and equity risk, and scenario files."
description: "Best estimate, own funds and the SCR under Solvency II with Finance Scenarios: the martingale test, EIOPA curves and where the rules are simplified."
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

Solvency II, the European insurance rulebook, asks two questions. How much is owed, valued at today's market prices (the best estimate, Article 77)? And is there enough capital to keep paying it after a 1-in-200 bad year (the Solvency Capital Requirement or SCR, Article 101)? Finance Scenarios answers both on a simulated run, checks that the run is fit for valuation, and writes scenario files for liability and ALM systems.

The two questions need two kinds of run. A *real-world* run projects how markets are likely to move; the one-year loss is measured on it. A *risk-neutral* run grows every traded asset at the risk-free rate on average, so it reproduces today's prices; liabilities are valued on it.

## Two Runs, Two Jobs

| Job | Run | Function |
|:----|:----|:---------|
| Prove the run is market consistent | risk neutral | `martingale_test`, `zero_coupon_curve`, `market_consistency_check` |
| Value a liability (best estimate) | risk neutral, or EIOPA's curve | `best_estimate` |
| One-year capital requirement (internal-model view) | real world | `solvency_capital_requirement` |
| Standard-formula interest rate risk | EIOPA's base and shocked curves | `interest_rate_scr` |
| Standard-formula equity risk | EIOPA's symmetric adjustment | `equity_scr` |
| Fetch EIOPA data | none | `eiopa_risk_free_curve`, `eiopa_symmetric_adjustment` |
| Hand the scenarios to a liability model | either | `write_scenario_files` |
| All of the above in one table | both | `Solvency` |

Every function discounts along each scenario with the bank account: the value today of 1 paid at time $$t$$ is $$D(t) = \exp\left(-\sum r \, \Delta t\right)$$, built from the simulated short rate. On a risk-neutral run that is a market price; on a real-world run it is a discounted expectation, fine for a one-year SCR but not a price.

Get a risk-neutral run with `scenarios.simulate(measure="risk_neutral")`, which builds the market-consistent version of your configuration (rates follow today's forward curve, equities grow at that rate minus their dividend yield), or per entry with `measure: "risk_neutral"` (see [configuration](/projects/financescenarios/docs/configuration#real-world-and-risk-neutral-measures)).

## The martingale_test Example Run {#martingale-test-example}

The examples on this page and in the reference reuse one run: SPY and US rates, inflation and unemployment, 2,000 scenarios, monthly over ten years, seed 42. The short rate and SPY are risk neutral, and SPY's dividend yield is its own entry so the test can add it back.

```python
from datetime import date

from financescenarios import Scenarios, martingale_test
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

dividend_yield = calibration.calibrated_params["spy_yield"].initial_value
test = martingale_test(result, "us_broad", "united_states_short_rate", dividend_yield=dividend_yield)
test.table.filter(test.table["time"].is_in([1.0, 2.0, 5.0, 10.0]))
```

The risk-neutral short rate here is today's 13-week Treasury yield, 3.993%, held flat (no `risk_neutral_forward_curve: true`), so bond prices carry no Monte Carlo error.

## Market Consistency: The Martingale Test

Before valuing on a risk-neutral run, check that it reproduces today's prices; EIOPA's guidelines expect this of a generator used for valuation. On average no asset may beat the risk-free cash account: discounted along each scenario's short rate, with dividends added back, the price must average to today's price ([Varnell, 2011](https://doi.org/10.1017/S1357321711000079){:target="_blank"}). The formula is as follows:

$$
\mathbb{E}\left[ D(t)\, S(t)\, e^{q t} \right] = S(0) \quad \text{at every date } t
$$

where $$q$$ is the dividend yield. Each date passes when $$S(0)$$ lies inside a 95% band around the simulated mean. The result holds `passed` (every date inside), `pass_rate`, `max_abs_deviation` (the largest gap, as a fraction) and a per-date `table`. `passed` is strict, since neighbouring dates share their paths; check `pass_rate` and another seed before calling a run broken. Failing at most dates means the drift is wrong, usually a real-world run tested by mistake.

**The example result** (calibrated on 2026-10-04), with `passed` False, `pass_rate` 0.825 and `max_abs_deviation` 0.0091:

| date | time | deflated_mean | ratio | standard_error | lower | upper | within_band |
|:-----|-----:|--------------:|------:|---------------:|------:|------:|:------------|
| 2027-10-01 | 1 | 768.89 | 0.9990 | 0.3218 | 768.26 | 769.52 | false |
| 2028-09-30 | 2 | 769.37 | 0.9996 | 0.7031 | 767.99 | 770.74 | true |
| 2031-10-01 | 5 | 769.15 | 0.9994 | 1.7385 | 765.74 | 772.55 | true |
| 2036-09-30 | 10 | 763.65 | 0.9922 | 3.1574 | 757.47 | 769.84 | true |

SPY stays within 0.9% of its starting 769.64 for all ten years, yet 21 of 120 monthly dates fall just outside their tight band. Seeds 2 and 3 pass everywhere, and seed 42 passes at 99% confidence: Monte Carlo noise, not a wrong drift. Leave out `q` and every date fails.

## The Rates Side: Model Curve Against EIOPA's Curve

For liabilities the question is whether the simulated rates price bonds the way the official curve does. `zero_coupon_curve(result, short_rate)` gives the bond prices a run implies, $$P(0,t) = \mathbb{E}[D(t)]$$, with their standard error and spot rate. On the example run every maturity prices off the flat 3.993%:

```python
from financescenarios import zero_coupon_curve

# `result` is the run from the martingale_test example.
curve = zero_coupon_curve(result, "united_states_short_rate")
curve.filter(curve["maturity"].is_in([1.0, 2.0, 5.0, 10.0]))
```

| maturity | price | standard_error | spot_rate |
|---------:|------:|---------------:|----------:|
| 1 | 0.9609 | 0.0000 | 0.03993 |
| 2 | 0.9232 | 0.0000 | 0.03993 |
| 5 | 0.8190 | 0.0000 | 0.03993 |
| 10 | 0.6708 | 0.0000 | 0.03993 |

`market_consistency_check(result, short_rate, discount_curve)` sets that curve beside a published one at every whole year: a `difference` within about two standard errors means the rates are consistent.

**EIOPA's curves.** `eiopa_risk_free_curve(toolkit, country, curve, as_of)` fetches the risk-free curve European insurers must discount with, monthly from January 2023, for the euro, the pound, the dollar, the yen and other currencies, from 1 to 150 years, without an API key. `curve` is `spot_no_va` (default), `spot_with_va`, `shock_up` or `shock_down`.

```python
from financetoolkit import Toolkit

from financescenarios import eiopa_risk_free_curve

toolkit = Toolkit(["AAPL"], start_date="2023-01-01")
curve = eiopa_risk_free_curve(toolkit, country="Euro Area", as_of="2026-09")
curve.filter(curve["maturity"].is_in([1.0, 10.0, 20.0, 60.0, 150.0]))
```

| maturity | 1 | 10 | 20 | 60 | 150 |
|:---------|--:|---:|---:|---:|----:|
| rate | 0.0327 | 0.0358 | 0.0360 | 0.0342 | 0.0335 |

Past 20 years, the last maturity where euro bonds trade freely, the curve bends toward the regulator's ultimate forward rate.

## Best Estimate

The best estimate is what the insurer owes, on the balance sheet. `best_estimate(run, cashflows, short_rate)` averages each scenario's present value, $$\sum_t D(t)\, CF(t)$$, with its standard error, spread and percentiles. Positive amounts are payments out. Cashflows are one schedule for all scenarios (one amount per date), or one per scenario, which is how inflation-linked benefits come in:

```python
import numpy as np

from financescenarios import best_estimate

# `result` is the run from the martingale_test example (monthly steps, ten years).
annuity = np.zeros(len(result.time_grid))
annuity[12::12] = 10_000.0  # 10,000 a year at each year end
level = best_estimate(result, annuity, short_rate="united_states_short_rate")

index = result.cumulative_index("united_states_inflation", initial_index=1.0).drop("scenario").to_numpy()
indexed = best_estimate(result, annuity * index, short_rate="united_states_short_rate")
```

Which returns (calibrated on 2026-10-04):

| annuity | best_estimate | standard_error | std | p0.5 | p50 | p99.5 |
|:--------|--------------:|---------------:|----:|-----:|----:|------:|
| level | 80,811.82 | 0.00 | 0.00 | 80,811.82 | 80,811.82 | 80,811.82 |
| inflation-indexed | 93,142.15 | 4.05 | 3,760.98 | 83,990.68 | 93,057.01 | 103,236.21 |

Ten yearly payments of 10,000 are worth 80,812 at a flat 3.99%; indexed to simulated inflation, 93,142, ranging from about 84,000 to 103,000. The standard error of 4 tells you whether `n_simulations` is enough.

To discount with EIOPA's curve, as Solvency II prescribes, pass `discount_curve=` and `short_rate=None`. The risk margin is not computed.

## Solvency Capital Requirement

`solvency_capital_requirement(run, own_funds, horizon_years=1.0, short_rate=None)` is the internal-model reading of Article 101: the 99.5% Value-at-Risk of the one-year loss in own funds (assets minus liabilities), on a real-world run. The formula is as follows:

$$
\text{loss} = OF(0) - D(h)\, OF(h), \qquad \text{SCR} = \max\left(q_{99.5\%}(\text{loss}),\, 0\right)
$$

With `short_rate` given, $$D$$ discounts the loss into today's money; otherwise it is 1. The result holds:

| Field | Meaning |
|:------|:--------|
| `scr` | The 1-in-200 one-year loss of own funds. |
| `own_funds` | Own funds today. |
| `solvency_ratio` | `own_funds / scr`; above 1 means the buffer covers the 1-in-200 loss. Empty when the SCR is 0. |
| `expected_shortfall` | The average loss in the scenarios beyond the SCR: how bad the bad tail is. |
| `probability_of_ruin` | The share of scenarios where discounted own funds are negative at the horizon. |
| `horizon_years` | The horizon actually used: the nearest date of the run. |

`own_funds` takes a factor name or any array shaped like the run, so an asset side from `Portfolio.compute()` and your own liability projection combine by subtraction.

**An example** on its own real-world run of one year: 1,000,000 in SPY against a liability of 800,000 growing at the short rate.

```python
from datetime import date

from financescenarios import Scenarios, solvency_capital_requirement
from financescenarios.config.config_model import ScenariosConfig

config = ScenariosConfig.model_validate(
    {
        "start_date": date(2026, 10, 1),
        "engine": {"n_simulations": 2000, "n_steps": 12, "frequency": "monthly", "seed": 42},
        "interest_rates": {"countries": [{"name": "United States"}]},
        "inflation": {"countries": [{"name": "United States"}]},
        "unemployment": {"countries": [{"name": "United States"}]},
        "equities": [{"name": "us_broad", "ticker": "SPY", "period": "monthly"}],
    }
)
scenarios = Scenarios.from_config(config, api_key="FINANCIAL_MODELING_PREP_KEY")
calibration = scenarios.calibrate(config)
result = scenarios.simulate(config, calibration=calibration)

equity = result["us_broad"]
assets = 1_000_000.0 * equity / equity[:, [0]]
liabilities = 800_000.0 / result.discount_factor_paths("united_states_short_rate")
scr = solvency_capital_requirement(
    result, assets - liabilities, horizon_years=1.0, short_rate="united_states_short_rate"
)
```

Which returns (calibrated on 2026-10-04), over four seeds (`scenarios.simulate(config, calibration, seed=...)`):

| seed | scr | own_funds | solvency_ratio | expected_shortfall | probability_of_ruin |
|-----:|----:|----------:|---------------:|-------------------:|--------------------:|
| 42 | 254,117.61 | 200,000.00 | 0.7870 | 286,195.26 | 0.0220 |
| 1 | 284,116.51 | 200,000.00 | 0.7039 | 302,668.72 | 0.0220 |
| 2 | 250,819.02 | 200,000.00 | 0.7974 | 271,585.00 | 0.0245 |
| 3 | 256,026.45 | 200,000.00 | 0.7812 | 287,009.99 | 0.0205 |

The 1-in-200 loss is about a quarter of the assets, more than the 200,000 of own funds: a solvency ratio of 79%. Across seeds the SCR moves by 13%, because only 10 of 2,000 scenarios sit beyond the 99.5% quantile; check other seeds or raise `n_simulations` before relying on it.

## Standard Formula: Interest Rate and Equity Risk

Two standard-formula sub-modules are available to set beside the scenario-based SCR.

**Interest rate risk.** `interest_rate_scr(run, cashflows, base_curve, up_curve, down_curve)` values a liability on EIOPA's base curve and its two shocked curves and takes the larger increase ([Delegated Regulation 2015/35](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj){:target="_blank"}, Articles 165 to 167). The formula is as follows:

$$
\text{SCR} = \max\left(BE_{up} - BE,\; BE_{down} - BE,\; 0\right)
$$

For most liabilities the down shock binds; `binding_shock` says which.

```python
from financescenarios import eiopa_risk_free_curve, interest_rate_scr

# `result` and `annuity` as in the best estimate example, `toolkit` as in the EIOPA curve example.
base, up, down = (eiopa_risk_free_curve(toolkit, curve=name) for name in ("spot_no_va", "shock_up", "shock_down"))
interest_rate_scr(result, annuity, base, up, down)
```

Only the liability is revalued; revalue the assets on the same curves for the full sub-module.

**Equity risk.** `equity_scr(type_1_value, type_2_value, symmetric_adjustment)` applies the standard formula's equity shocks (Articles 168 to 169):

| | Shock | Covers |
|:--|:------|:-------|
| Type 1 | 39% plus the symmetric adjustment | Equities listed in the European Economic Area or the OECD |
| Type 2 | 49% plus the symmetric adjustment | All others: unlisted shares, private equity, hedge funds, commodities |

The two losses combine with a 0.75 correlation. The formula is as follows:

$$
\text{SCR}_{eq} = \sqrt{L_1^2 + 2 \cdot 0.75 \cdot L_1 L_2 + L_2^2}
$$

The symmetric adjustment raises both shocks by up to 10 points after a rally and lowers them after a fall. `eiopa_symmetric_adjustment(toolkit, as_of)` fetches it; for September 2026 it is 0.0771.

```python
from financescenarios import equity_scr

equity_scr(type_1_value=1_000_000, type_2_value=250_000, symmetric_adjustment=0.0771)
```

This gives shocks of 46.71% and 56.71% and an equity risk capital of 581,048, less than the 608,875 sum. Strategic participations, long-term equity investments and the transitional measure are not modelled, and aggregating with the rest of the standard formula is up to you.

## One Table With Solvency

`Solvency(real_world, risk_neutral)` takes a pair of runs and `report(cashflows, assets)` puts everything above in one table:

```python
from financescenarios import Portfolio, Scenarios, Solvency

scenarios = Scenarios.from_profiles(settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY")
result = scenarios.simulate(n_simulations=2000)

# The same factors priced the way markets price them today, for valuing what is owed
risk_neutral = scenarios.simulate(n_simulations=2000, measure="risk_neutral")
solvency = Solvency(real_world=result, risk_neutral=risk_neutral)

# Pay out 10,000 a year for five years, backed by 60,000 invested in the 60/40
assets = Portfolio.from_preset(result, preset="balanced_60_40").compute(initial_value=60_000, rebalance_every=12)
solvency.report(cashflows=[10_000] * 5, assets=assets)
```

| item | value | meaning |
|:-----|:------|:--------|
| market consistent | passed (largest gap 1.0%) | discounted back, us_broad stays within 2% of today's price |
| best estimate | 43,444 | what the payments are worth today |
| own funds | 15,635 | assets minus what is owed, today |
| SCR (1 in 200 year) | 12,453 | the capital that survives a 1-in-200 bad year |
| solvency ratio | 1.26 | own funds / SCR; above 1 means enough capital |

The market-consistency row is the martingale test on the risk-neutral run's first equity (passing within 2%), the best estimate is valued on the risk-neutral run, and the SCR on the real-world run, with the liabilities revalued at each scenario's short rate so falling rates raise them. `solvency.plot(cashflows, assets)` charts own funds after a year with the 1-in-200 outcome marked, and `solvency.write_files(directory)` writes both runs as scenario files.

## Currencies

None of these functions converts currencies, so assets, liabilities and the discount rate must share one currency. `Portfolio.compute()` already reports in the run's reporting currency, `Reporting(result, config).convert(factor)` converts a single price factor, and the liabilities should be discounted with the short rate and EIOPA curve of their own currency.

## Scenario Files for Liability Models

`write_scenario_files(run, directory)` writes the scenarios in the shape actuarial and ALM systems load: one file per variable, one row per trial (numbered from 1) and one column per year, plus an `index` naming each variable's unit (see [units](/projects/financescenarios/docs/units)).

```python
from financescenarios import write_scenario_files

# `result` is the run from the martingale_test example (monthly, ten years).
write_scenario_files(result, "esg_output", step_stride=12)  # annual CSVs
write_scenario_files(result, "esg_output", file_format="xlsx", step_stride=12)  # one workbook
```

`step_stride=12` keeps every twelfth monthly step and `factors=` limits the export. Write a risk-neutral run for valuation and a real-world run for projections.

## What Is Simplified

| Area | What Finance Scenarios does | What it leaves to you |
|:-----|:----------------------------|:----------------------|
| Technical provisions | The best estimate | The risk margin |
| SCR, internal-model view | A one-run 99.5% VaR of the own-funds path you supply | The asset-liability projection, management actions, taxes, loss-absorbing capacity of technical provisions and deferred taxes, and nested revaluation of liabilities inside each one-year scenario |
| SCR, standard formula | The interest rate sub-module (liability side) and the equity sub-module | Every other module, and the aggregation across them |
| Equity risk | Type 1 and type 2 shocks with the symmetric adjustment | Strategic participations, long-term equity investments, the transitional measure |
| Liabilities in `Solvency` | Revalued at each scenario's short rate, held flat | A full yield curve per scenario |
| Market consistency | The drift: rates and equities grow at the risk-free rate | Option prices across strikes, except for an equity with `volatility_source: heston`; elsewhere volatility is a single number |
| Risk-free curve | Fetches EIOPA's curves and compares against them | Calibrating the simulated short rate to EIOPA's curve; the risk-neutral rate is fitted to its own market data |

Check market consistency on every risk-neutral run before valuing on it, and check the SCR at more than one seed.

## References

- European Parliament and Council (2009). "Directive 2009/138/EC (Solvency II)", Articles 76-77 (technical provisions, best estimate) and 101 (SCR at 99.5% over one year). [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/dir/2009/138/oj){:target="_blank"}
- European Commission (2015). "Commission Delegated Regulation (EU) 2015/35", Articles 165-167 (interest rate risk) and 168-172 (equity risk and symmetric adjustment). [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj){:target="_blank"}
- EIOPA (2015, updated 2023). "Guidelines on valuation of technical provisions." [eiopa.europa.eu](https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en){:target="_blank"}
- EIOPA. "Risk-free interest rate term structures." [eiopa.europa.eu](https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en){:target="_blank"}
- EIOPA. "Symmetric adjustment of the equity capital charge." [eiopa.europa.eu](https://www.eiopa.europa.eu/tools-and-data/symmetric-adjustment-equity-capital-charge_en){:target="_blank"}
- Varnell, E.M. (2011). "Economic Scenario Generators and Solvency II." British Actuarial Journal, 16(1), 121-159. [doi.org](https://doi.org/10.1017/S1357321711000079){:target="_blank"}
- Wüthrich, M.V., Merz, M. (2013). "Financial Modeling, Actuarial Valuation and Solvency in Insurance." Springer. [doi.org](https://doi.org/10.1007/978-3-642-31392-9){:target="_blank"}

For every argument and return field, see the [Solvency reference](/projects/financescenarios/docs/reference/solvency).
