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

An insurer uses an economic scenario generator to answer two questions that Solvency II, the European insurance rulebook, names separately. How much is owed, valued at today's market prices? And is there enough capital to keep paying it after a very bad year? The first is the best estimate of the technical provisions (Article 77 of the Directive). The second is the Solvency Capital Requirement, or SCR (Article 101). Finance Scenarios gives you both on any simulated run, plus a check that the run is fit for valuation and scenario files for liability and ALM systems.

The two questions need two different kinds of scenarios. A *real-world* run projects how markets are likely to move, with drifts and volatilities fitted to history; that is the run you measure the one-year loss on. A *risk-neutral* run is adjusted so that every traded asset grows on average at the risk-free rate, which makes it reproduce today's prices; that is the run you value liabilities on. Every section below says which run it expects.

## Two Runs, Two Jobs

Knowing which function belongs to which run is most of what it takes to use this module correctly.

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

Every function discounts with the pathwise bank-account deflator: the value today of one unit paid at time `t` along one scenario, `D(t) = exp(-sum of r * dt)`, built from the simulated short rate (see [`ScenarioSet.discount_factor_paths`](/projects/financescenarios/docs/reference/scenario-set)). On a risk-neutral run that gives a market-consistent price. On a real-world run it gives a real-world discounted expectation, which suits a one-year SCR projection but is not a market price. A real-world stochastic deflator exists only for the `knw_sv` rates and inflation pair (see [KNW-SV under Q](/projects/financescenarios/docs/reference/knw-sv-q)).

There are two ways to get a risk-neutral run:

- **`scenarios.simulate(measure="risk_neutral")`** builds the market-consistent version of your configuration for you. The first interest rate follows today's forward curve (a Hull-White rate with `risk_neutral_forward_curve: true`) and every equity grows at that rate minus its dividend yield. Factors without a traded price, such as credit, are left out; inflation and unemployment stay real-world so benefits can still be indexed to them.
- **`measure: "risk_neutral"` per entry** in the configuration, as in the example run below, lets you choose each factor's treatment yourself. See [Real-world and risk-neutral measures](/projects/financescenarios/docs/configuration#real-world-and-risk-neutral-measures) for what each factor supports.

## The martingale_test Example Run {#martingale-test-example}

Several examples in the reference refer to "the run from the `martingale_test` example"; this is that run, so you can reproduce every number quoted for it.

It simulates SPY and US interest rates, inflation and unemployment: 2,000 scenarios, monthly over ten years (120 steps), seed 42, with paired (antithetic) shocks and history from 2010. The short rate and the equity are risk neutral, and SPY's dividend yield is its own entry so the test can add it back.

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

In this run the risk-neutral short rate is today's 13-week Treasury yield, 3.993%, held flat, because the configuration does not set `risk_neutral_forward_curve: true`. Bond prices therefore carry no Monte Carlo error. The run's variables are `united_states_short_rate`, `united_states_inflation`, `united_states_unemployment`, `us_broad` and `spy_yield`. The test results are in the next section; the zero-coupon curve, best estimate and scenario-file examples reuse `result` from this block.

## Market Consistency: The Martingale Test

Before you value anything on a risk-neutral run, you need evidence that it actually reproduces today's prices; EIOPA's guidelines on technical provisions expect a scenario generator used for valuation to pass this test.

In market-consistent scenarios no asset beats the risk-free cash account on average. Discount the asset's simulated price back along each scenario's own short rate, add back the dividends, and average: the result must equal today's price, up to Monte Carlo noise:

```
E[ D(t) * S(t) * exp(q * t) ] = S(0)   at every date t
```

Here `q` is the dividend yield the risk-neutral equity drift was reduced by (the drift is `r - q`), added back so the test is on total return ([Varnell, 2011](https://doi.org/10.1017/S1357321711000079){:target="_blank"}).

Each date gets a two-sided normal band, `deflated_mean +/- z * standard_error` (`z = 1.96` at the default 95% `confidence`), and passes when `S(0)` lies inside it. Under antithetic shocks the standard error comes from pair averages, the actual independent unit.

The result holds `passed`, `pass_rate`, `max_abs_deviation` (the largest gap from today's price, as a fraction) and a per-date `table`.

- `passed` and `pass_rate` skip the start date, where the band has zero width.
- `passed` asks for every date inside its band, which is strict: neighboring dates share most of their paths, so one unlucky batch can push several out together. Look at `pass_rate`, `max_abs_deviation` and another seed before calling a run broken.
- Failing at many dates means the drift is not `r - q`: usually a real-world run tested by mistake, or a `q` that does not match the `initial_value` of the matching `dividend_yield` entry.

**The example result** (calibrated on 2026-10-04), with `passed` False, `pass_rate` 0.825 and `max_abs_deviation` 0.0091:

| date | time | deflated_mean | ratio | standard_error | lower | upper | within_band |
|:-----|-----:|--------------:|------:|---------------:|------:|------:|:------------|
| 2027-10-01 | 1 | 768.89 | 0.9990 | 0.3218 | 768.26 | 769.52 | false |
| 2028-09-30 | 2 | 769.37 | 0.9996 | 0.7031 | 767.99 | 770.74 | true |
| 2031-10-01 | 5 | 769.15 | 0.9994 | 1.7385 | 765.74 | 772.55 | true |
| 2036-09-30 | 10 | 763.65 | 0.9922 | 3.1574 | 757.47 | 769.84 | true |

SPY starts at 769.64 with `r` = 3.99% and `q` = 0.99%. Discounted, with dividends added back, it stays within 0.9% of 769.64 for all ten years, yet 21 of 120 monthly dates fall just outside their tight 95% band, so the strict test fails at this seed. At seeds 2 and 3 it passes at every date, and at 99% confidence it passes for seed 42 too: Monte Carlo noise rather than a wrong drift. Leave out `q` and every date fails, drifting up to 10% from `S(0)` by year 10.

## The Rates Side: Model Curve Against EIOPA's Curve

The martingale test checks an equity; for liabilities the more important question is whether the simulated rates price bonds the way the official curve does.

`zero_coupon_curve(result, short_rate)` gives the bond curve a run implies: the price `P(0, t) = E[D(t)]` of a bond paying 1 at each date, its standard error, and the continuously compounded spot rate `-ln P(0, t) / t`. On the example run every maturity prices off the flat 3.993%:

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

With `risk_neutral_forward_curve: true` the table should line up with today's input curve; a gap wider than a few standard errors means the time steps are too coarse or the curve fit is off.

`market_consistency_check(result, short_rate, discount_curve)` sets that model curve beside a published curve at every whole year of the run. It returns `model_rate`, `curve_rate` (both annually compounded), their `difference` and a `standard_error`. A difference inside about two standard errors at every maturity means the rates are consistent; a steady gap means the run was calibrated to a different curve (Treasury yields rather than EIOPA's, say) or the short rate is not risk neutral.

**EIOPA's curves.** `eiopa_risk_free_curve(toolkit, country, curve, as_of)` fetches the risk-free term structure European insurers must discount with (Article 77(2)), through the Finance Toolkit and without an API key. There is one release a month from January 2023, for the euro, every European Economic Area currency, the pound, the Swiss franc, the US, Canadian and Australian dollar, the yen and a few others, with annually compounded rates from 1 to 150 years. `curve` picks one of four: `spot_no_va` (the basic curve, default), `spot_with_va` (with the volatility adjustment), `shock_up` and `shock_down` (after the standard formula's interest rate shocks).

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

The best estimate is the number on the balance sheet for what the insurer owes, so it is the number you most need to be able to explain.

`best_estimate(run, cashflows, short_rate)` computes each scenario's present value, `sum of D(t) * cashflow(t)`, and averages across scenarios. Positive amounts are payments out. It also returns the `standard_error` of that average, the spread across scenarios (`std`) and `percentiles`.

Cashflows come in two shapes:

- One schedule for every scenario: one amount per date of the run, the start included (undiscounted).
- One schedule per scenario, shaped `(n_simulations, n_steps + 1)`: how inflation-linked or asset-share benefits enter, built from the run itself.

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

Ten yearly payments of 10,000 are worth 80,812 at the flat 3.99% short rate. Indexed to simulated US inflation they are worth 93,142, spread from about 84,000 to 103,000. A standard error of 4 pins that average to within about 8 either way, which tells you whether `engine.n_simulations` is enough for the precision you report to.

**Discounting with EIOPA's curve.** Solvency II prescribes EIOPA's risk-free curve for technical provisions. Pass `discount_curve=` (such as the output of `eiopa_risk_free_curve`) and `short_rate=None` to discount every scenario with that curve instead: `(1 + r(t)) ** -t`, with `r` interpolated linearly and held flat beyond the first and last maturity.

**Keep in mind.** The best estimate is market consistent only when the short rate was simulated risk neutral; on a real-world run the same number is a real-world discounted expectation. And this is the best estimate alone: the risk margin that completes the technical provisions is not computed.

## Solvency Capital Requirement

The SCR is the capital an insurer must hold, and the solvency ratio built on it is the number insurers publish, so it is worth understanding exactly what goes into it here.

`solvency_capital_requirement(run, own_funds, horizon_years=1.0, short_rate=None)` follows the internal-model reading of Article 101: the 99.5% Value-at-Risk of the loss in own funds over one year. Per scenario:

```
loss = OF(0) - D(h) * OF(h)
SCR  = 99.5% quantile of loss, floored at 0
```

`OF` is own funds (assets minus liabilities) and `h` the horizon. With `short_rate` given, `D` is the bank-account deflator, so the change is measured in today's money; without it, `D` is 1. Run this on a real-world run: the SCR is a projection of how markets are likely to move.

The result holds:

| Field | Meaning |
|:------|:--------|
| `scr` | The 1-in-200 one-year loss of own funds. |
| `own_funds` | Own funds today. |
| `solvency_ratio` | `own_funds / scr`; above 1 means the buffer covers the 1-in-200 loss. Empty when the SCR is 0. |
| `expected_shortfall` | The average loss in the scenarios beyond the SCR: how bad the bad tail is. |
| `probability_of_ruin` | The share of scenarios where discounted own funds are negative at the horizon. |
| `horizon_years` | The horizon actually used: the nearest date of the run. |

`own_funds` takes a factor name or any array shaped like the run, so an asset side from `Portfolio.compute()` and your own liability projection combine by subtraction.

**An example.** This needs its own run: one year of monthly real-world steps. It holds 1,000,000 in SPY against a liability of 800,000 that grows at the short rate.

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

The 1-in-200 loss on this all-equity balance sheet is about a quarter of the assets, more than the 200,000 of own funds: a solvency ratio of 79%, with about 2% of scenarios insolvent after a year. Across seeds the SCR moves by 13%, because with 2,000 scenarios only 10 sit beyond the 99.5% quantile. Check other seeds, or raise `n_simulations`, before you rely on it.

## Standard Formula: Interest Rate and Equity Risk

Many insurers report on the standard formula rather than an internal model, so two of its sub-modules are available as stand-alone calculations you can set beside the scenario-based SCR.

**Interest rate risk.** `interest_rate_scr(run, cashflows, base_curve, up_curve, down_curve)` values a liability on EIOPA's basic risk-free curve and on its two shocked curves, then takes the larger increase:

```
SCR = max(BE_up - BE, BE_down - BE, 0)
```

This follows Articles 165 to 167 of [Delegated Regulation 2015/35](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj){:target="_blank"}. Lower rates make future payments dearer today, so for most liabilities the downward shock binds; the result's `binding_shock` says which. The run only supplies the dates and, for scenario-dependent cashflows, the scenarios; discounting uses the three curves.

```python
from financescenarios import eiopa_risk_free_curve, interest_rate_scr

# `result` and `annuity` as in the best estimate example, `toolkit` as in the EIOPA curve example.
base, up, down = (eiopa_risk_free_curve(toolkit, curve=name) for name in ("spot_no_va", "shock_up", "shock_down"))
interest_rate_scr(result, annuity, base, up, down)
```

Only the liability is revalued. For the full interest rate sub-module, revalue the assets on the same curves and take the larger fall in assets minus liabilities.

**Equity risk.** `equity_scr(type_1_value, type_2_value, symmetric_adjustment)` applies the standard formula's equity shocks (Articles 168 to 169):

| | Shock | Covers |
|:--|:------|:-------|
| Type 1 | 39% plus the symmetric adjustment | Equities listed in the European Economic Area or the OECD |
| Type 2 | 49% plus the symmetric adjustment | All others: unlisted shares, private equity, hedge funds, commodities |

The two losses `L1` and `L2` combine with a 0.75 correlation, `sqrt(L1^2 + 2 * 0.75 * L1 * L2 + L2^2)`, so the total is less than their sum. The symmetric adjustment, or "equity dampener", raises both shocks by up to 10 points after a rally and lowers them by up to 10 points after a fall, so insurers are not forced to sell into a falling market. `eiopa_symmetric_adjustment(toolkit, as_of)` fetches EIOPA's month-end value, again without an API key; for September 2026 it is 0.0771.

```python
from financescenarios import equity_scr

equity_scr(type_1_value=1_000_000, type_2_value=250_000, symmetric_adjustment=0.0771)
```

This gives shocks of 46.71% and 56.71%, losses of 467,100 and 141,775, and an equity risk capital of 581,048, less than the sum of the two (608,875) because the two types do not fall perfectly together. Strategic participations (a 22% shock), long-term equity investments and the transitional measure are not modelled; treat such holdings separately.

There is no aggregation across sub-modules or risk modules: combining these two numbers with the rest of the standard formula is up to you.

## One Table With Solvency

`Solvency` puts the reads above into one table, so you see the whole picture at once.

`Solvency(real_world, risk_neutral)` takes a pair of runs of the same factors. `report(cashflows, assets)` then returns one row per read, with an `item`, a formatted `value` and a plain `meaning`:

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

What happens behind each row:

- **Market consistent.** The martingale test on the risk-neutral run's first equity (or the `asset` you name), with its dividend yield taken from the calibration. The row passes when `max_abs_deviation` is within `price_tolerance`, 2% by default. It is left out when the risk-neutral run has no equity.
- **Best estimate.** `best_estimate` on the risk-neutral run, discounted with its first interest rate (or the `short_rate` you name).
- **Own funds, SCR and solvency ratio.** `solvency_capital_requirement` on the real-world run over `horizon_years` (one year by default), with own funds equal to `assets` minus the payments still due. Those payments are revalued at every date of every scenario at that scenario's short rate on that date, held flat across maturities. So when rates fall, the liabilities rise and own funds fall unless the assets move the same way. Because of this, today's own funds use today's short rate rather than the best estimate in the row above.

`cashflows` is one amount per year (`[10_000] * 5`, paid at each year end) or one per date of the run. `solvency.plot(cashflows, assets)` charts own funds after one year with the 1-in-200 outcome marked (see [Plotting](/projects/financescenarios/docs/plotting)), and `solvency.write_files(directory)` writes both runs as scenario files.

## Currencies

Every function on this page takes numbers as they are: none of them converts currencies. Assets, liabilities and the discount rate must therefore be in the same currency before they meet.

- `Portfolio.compute()` already puts every holding in the run's reporting currency (`reporting.reporting_currency`, `USD` by default) before weighting, using each scenario's own simulated exchange rate.
- For a single factor, `Reporting(result, config).convert("jp_equity")` returns its paths in the reporting currency. Only prices are converted; a rate stays a rate. See [Reporting](/projects/financescenarios/docs/reference/reporting).
- Discount with the short rate of the currency the liabilities are in, and fetch EIOPA's curve for that currency (`country="United Kingdom"`, for example).

## Scenario Files for Liability Models

Liabilities are usually projected in a dedicated actuarial or ALM system, so the scenarios need to leave Python in a shape it loads without reshaping.

`write_scenario_files(run, directory)` writes one file per variable, one row per trial (numbered from 1, the convention scenario vendors ship) and one column per projection time in years. An `index` table names each variable's label, category and unit: "annualized decimal rate" for a rate (0.04 is 4% a year), "price level" for a simulated price such as an equity, FX rate, commodity or dividend index, and "index level" for the leading indicator (see [Units](/projects/financescenarios/docs/units)).

```python
from financescenarios import write_scenario_files

# `result` is the run from the martingale_test example (monthly, ten years).
write_scenario_files(result, "esg_output", step_stride=12)  # annual CSVs
write_scenario_files(result, "esg_output", file_format="xlsx", step_stride=12)  # one workbook
```

On the example run this writes `index.csv` plus one 2,000-row file per variable with columns for years 0 to 10: `step_stride=12` keeps every twelfth monthly step. `factors=` limits the export to the variables you name.

Write a risk-neutral run for valuation and a real-world run for projections. Prefer CSV for large runs: each Excel sheet holds one row per scenario.

## What Is Simplified

Knowing where the module stops tells you which results stand on their own and which need your own model around them.

| Area | What Finance Scenarios does | What it leaves to you |
|:-----|:----------------------------|:----------------------|
| Technical provisions | The best estimate | The risk margin |
| SCR, internal-model view | A one-run 99.5% VaR of the own-funds path you supply | The asset-liability projection, management actions, taxes, loss-absorbing capacity of technical provisions and deferred taxes, and nested revaluation of liabilities inside each one-year scenario |
| SCR, standard formula | The interest rate sub-module (liability side) and the equity sub-module | Every other module, and the aggregation across them |
| Equity risk | Type 1 and type 2 shocks with the symmetric adjustment | Strategic participations, long-term equity investments, the transitional measure |
| Liabilities in `Solvency` | Revalued at each scenario's short rate, held flat | A full yield curve per scenario |
| Market consistency | The drift: rates and equities grow at the risk-free rate | Option prices across strikes, except for an equity with `volatility_source: heston`; elsewhere volatility is a single number |
| Risk-free curve | Fetches EIOPA's curves and compares against them | Calibrating the simulated short rate to EIOPA's curve; the risk-neutral rate is fitted to its own market data |

Two habits make the results more trustworthy. Check market consistency on every risk-neutral run before valuing on it. And check the SCR at more than one seed, or with more scenarios, because a 99.5% quantile rests on very few of them.

## References

- European Parliament and Council (2009). "Directive 2009/138/EC (Solvency II)", Articles 76-77 (technical provisions, best estimate) and 101 (SCR at 99.5% over one year). [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/dir/2009/138/oj){:target="_blank"}
- European Commission (2015). "Commission Delegated Regulation (EU) 2015/35", Articles 165-167 (interest rate risk) and 168-172 (equity risk and symmetric adjustment). [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/reg_del/2015/35/oj){:target="_blank"}
- EIOPA (2015, updated 2023). "Guidelines on valuation of technical provisions." [eiopa.europa.eu](https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en){:target="_blank"}
- EIOPA. "Risk-free interest rate term structures." [eiopa.europa.eu](https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en){:target="_blank"}
- EIOPA. "Symmetric adjustment of the equity capital charge." [eiopa.europa.eu](https://www.eiopa.europa.eu/tools-and-data/symmetric-adjustment-equity-capital-charge_en){:target="_blank"}
- Varnell, E.M. (2011). "Economic Scenario Generators and Solvency II." British Actuarial Journal, 16(1), 121-159. [doi.org](https://doi.org/10.1017/S1357321711000079){:target="_blank"}
- Wüthrich, M.V., Merz, M. (2013). "Financial Modeling, Actuarial Valuation and Solvency in Insurance." Springer. [doi.org](https://doi.org/10.1007/978-3-642-31392-9){:target="_blank"}

For every argument and return field, see the [Solvency reference](/projects/financescenarios/docs/reference/solvency).
