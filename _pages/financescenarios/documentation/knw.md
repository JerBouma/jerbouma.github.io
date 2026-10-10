---
title: KNW Models
seo_title: KNW Models Documentation – Finance Scenarios
excerpt: "The Koijen-Nijman-Werker family behind De Nederlandsche Bank's scenario sets: interest rates and inflation fitted as one coupled system, optionally with shared stochastic volatility, an equity leg and a risk-neutral version fitted to the yield curve."
description: "How Finance Scenarios models interest rates and inflation jointly, KNW style: the knw, knw_sv and risk-neutral variants, their calibration and their limits."
author_profile: false
permalink: /projects/financescenarios/docs/knw
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

{% include mermaid.html %}

Most interest-rate and inflation models in Finance Scenarios treat the two as separate processes that only move together through correlated shocks. The KNW models instead let each one's next value depend on the current level of both: high inflation today feeds into next period's rate, and today's rate feeds into next period's inflation. They are based on the term-structure model of [Koijen, Nijman and Werker (2010)](https://doi.org/10.1093/rfs/hhp058){:target="_blank"}, which De Nederlandsche Bank (DNB), the Dutch central bank, extends in its CP2022 scenario model, the scenario set Dutch pension funds and insurers are regulated against.

There are three variants, each building on the previous one. `knw` couples the rate and inflation with constant volatility. `knw_sv` adds a shared, hidden "turbulence" factor that makes both swing harder in stressed periods, with an optional equity index that reads the same turbulence. The risk-neutral version fits a market price of risk to the Treasury yield curve, so the same model can price bonds and value cash flows. For the single-factor short-rate models and the Nelson-Siegel yield curve, see [interest rates](/projects/financescenarios/docs/interest-rates).

## Why Model Rates and Inflation Together

If you value inflation-linked liabilities against a nominal bond portfolio, the relationship between the two drivers matters as much as each one on its own.

Correlated shocks only link the *surprises*: a rate shock this month tends to come with an inflation shock this month. They say nothing about how today's level of inflation shapes where rates go next. The Wilkie cascade and the `condition_on_interest_rate` option on an inflation entry let one variable drive the other, in one direction only. The KNW models go both ways:

| | `condition_on_interest_rate` | `method: knw` |
|:--|:--|:--|
| Direction | One way: inflation reads the rate | Two ways: each reads the other |
| What is read | The rate's change from one step to the next | The other variable's level |
| Fit | One regression for inflation | Two regressions fitted jointly |

As a result the pair settles toward one joint long-run level, consistent between the two legs by construction.

## The Three Variants

Choosing a variant is a trade-off between fidelity to DNB's model and the data and calibration effort each one needs.

| Variant | How you select it | What it adds | Reference |
|:--|:--|:--|:--|
| KNW | `method: knw` on the rate and inflation entry | Two-way coupling at constant volatility | [Knw](/projects/financescenarios/docs/reference/knw) |
| KNW with stochastic volatility | `method: knw_sv` on both entries | A shared turbulence factor `v` that scales volatility and shifts the drift; optional equity leg | [KnwSv](/projects/financescenarios/docs/reference/knw-sv) |
| Risk-neutral KNW | `method: knw_sv` plus `measure: risk_neutral` on both entries | A market price of risk fitted to the yield curve, closed-form bond prices and a stochastic deflator | [KnwSvQ](/projects/financescenarios/docs/reference/knw-sv-q) |

The stochastic-volatility parameters are a strict superset of the plain KNW ones: set the two turbulence terms to zero on both legs and `knw_sv` reduces exactly to `knw`. The risk-neutral version is built on top of `knw_sv`, so there is no risk-neutral version of the constant-volatility model.

## How the Factors Drive Each Other

A picture of who reads whom makes it easier to see why some configurations are allowed and others are rejected.

{% raw %}
<div class="mermaid">
flowchart TD
    v["Turbulence v (hidden, shared)"]
    r[Interest rate]
    pi[Inflation]
    eq["Equity (optional)"]
    v -->|"drift and volatility"| r
    v -->|"drift and volatility"| pi
    v -->|volatility| eq
    r <-->|"last period's level"| pi
    r -->|"drift: short rate plus premium"| eq
</div>
{% endraw %}

The rate and inflation each read only the other's value from the start of the step, so the engine can step them in either order. `v` drives every leg and is never driven back, and the equity leg reads `v` and the rate without influencing either. In `knw` only the two-way arrow between rate and inflation remains.

`v` has no observed history, so it is kept out of the simulated factors and the correlation matrix. It lives privately inside the pair, shared by every leg that uses it.

## KNW: Two-Way Coupling at Constant Volatility

This is the smallest piece of DNB's model you can run and the easiest to interpret, so start here.

Each leg is a linear regression on the previous value of both variables. In plain text:

```text
rate(t)      = intercept_r  + own_persistence_r  * rate(t-1) + cross_coupling_r  * inflation(t-1) + noise
inflation(t) = intercept_pi + own_persistence_pi * inflation(t-1) + cross_coupling_pi * rate(t-1) + noise
```

Econometricians call this a bivariate VAR(1) ([Lütkepohl, 2005](https://doi.org/10.1007/978-3-540-27752-1){:target="_blank"}). For each leg you get four parameters:

- `own_persistence`: how much of its own last value carries over. At 0.9 a quarter, half of a deviation is gone after about 6.6 quarters, ignoring the cross effect.
- `cross_coupling`: how much of the other leg's last value spills into it.
- `intercept`: a constant.
- `volatility`: the size of the random surprise per period.

There is no long-run mean per leg: the pair's long-run levels are `(I - Phi)^-1 c`, where `Phi` holds the four persistence and coupling terms and `c` the two intercepts. Rates and inflation are decimals (0.04 is 4%), inflation being year-over-year CPI growth.

**Calibration.** Both legs are fitted by ordinary least squares on the same inputs, which makes fitting each one separately already efficient. Only the dates both series cover are used: fewer than 5 raise an error, fewer than 10 a warning. The system must also settle down over time; if a shock would never die out (the largest eigenvalue of `Phi` is 1 or more), the fit raises an error.

**An example.** Fitted on 146 quarters of the US OECD short rate and CPI growth, 1990Q1 to 2026Q2 (calibrated on 2026-10-05):

| leg | intercept | own_persistence | cross_coupling | volatility |
|:----|----------:|----------------:|---------------:|-----------:|
| interest_rate | -0.0009 | 0.9397 | 0.0918 | 0.0044 |
| inflation | 0.0036 | 0.8910 | -0.0246 | 0.0073 |

One percentage point more inflation adds 0.092 points to next quarter's rate, while a higher rate nudges inflation down slightly. A joint shock halves in about 8 quarters, and the pair settles at a 2.60% rate and 2.74% inflation in the long run. Both legs start from their last observation.

## KNW With Stochastic Volatility

Markets alternate between calm and stressed spells, while plain KNW gives every period the same amount of randomness.

`knw_sv` brings back the hidden variance factor `v` from DNB's model. `v` follows a CIR process ([Cox, Ingersoll and Ross, 1985](https://doi.org/10.2307/1911242){:target="_blank"}), the mean-reverting, never-negative variance process of [Heston (1993)](https://doi.org/10.1093/rfs/6.2.327){:target="_blank"}. Each leg now reads last period's `v` in two places:

```text
rate(t) = intercept + variance_coupling * v(t-1)
          + own_persistence * rate(t-1) + cross_coupling * inflation(t-1)
          + sqrt(base_variance + variance_sensitivity * v(t-1)) * shock
```

Inflation has the same shape with its own parameters. Reading the new terms:

- `variance_coupling`: how much the level of `v` shifts the leg's expected next value. DNB's model does not force this to zero, so turbulence moves the level as well as the noise.
- `base_variance` and `variance_sensitivity`: the leg's variance per period is `base_variance + variance_sensitivity * v`. These are per-period variances.
- `v`'s own parameters: a long-run mean (its normal level), a mean-reversion speed (a spike halves in ln 2 / speed years) and a volatility.

**Estimating `v` from history.** DNB recovers `v` by inverting its closed-form yield curve against market yields on every date. Finance Scenarios estimates it from the pair's own history instead, in five stages:

1. Fit plain KNW and keep each period's squared surprises.
2. Average them over the trailing four periods as a stand-in for `v`, lagged one period so a surprise is never used to explain itself.
3. Fit a CIR process to that stand-in.
4. Refit both legs with last period's `v` as an extra input, giving `variance_coupling` and updated persistence and coupling terms.
5. Regress each leg's squared surprises on last period's `v` for `base_variance` and `variance_sensitivity`, with both kept at zero or above.

You need at least 11 overlapping observations. If neither leg's variance rises with `v`, both sensitivities come out at zero and a warning suggests `method: knw` instead.

**Simulating `v`.** `v` is stepped with [Andersen's (2008)](https://doi.org/10.21314/jcf.2008.189){:target="_blank"} Quadratic-Exponential scheme, which is nearly free of bias and never goes negative. That matters because every leg's volatility depends on `v`.

**An example.** On the same US quarterly data since 1990 (calibrated on 2026-10-05), `v` has a mean-reversion speed of 0.40, so turbulence halves in about 1.7 years. Its current value (0.0000094) sits well below its long-run level (0.0000627), so the pair starts calmer than usual. Inflation responds most: its standard deviation is 0.31% a quarter at `v = 0` and 0.68% at `v`'s long-run level. The fit also warned that the Feller condition fails (`2 * speed * long_run_mean < volatility^2`), which means simulated `v` touches zero more often than its long-run distribution suggests.

Because neighboring four-period averages overlap, `v`'s fitted parameters are biased downward on very long histories (past roughly 2,000 quarters). At the 100 to 400 quarterly observations real OECD and FRED data offer, the fit is essentially unbiased in testing.

## The Equity Leg

If equities and rates should become volatile at the same time in your scenarios, an equity leg on the shared `v` gives you that link without extra hidden state.

An equity entry with `method: knw_sv` follows the equity row of DNB's model: its expected log return each period is the simulated short rate plus a constant risk premium, and its variance is `base_variance + variance_sensitivity * v`. In formula form, `d ln(S) = (r + risk_premium - 0.5 * var) dt + sqrt(var) dW`.

The fit uses price history only: `risk_premium` from the average return above the short rate, corrected for volatility drag, and the variance terms from a regression on last period's `v`. At least 6 dates must overlap with the pair.

Over the S&P 500's quarterly history since 1990 (calibrated on 2026-10-05), the index earned 1.59% a quarter above the short rate, about 6.4% a year. Its volatility is about 13% a year at `v = 0` and 15.3% at `v`'s long-run level, so equity turbulence rises with the pair's.

The equity leg runs under the real-world measure only. A config that pairs it with a risk-neutral rate is rejected.

## The Risk-Neutral Version

A real-world run answers "where might rates go?", while valuing liabilities needs "what is a future cash flow worth today?", and the market price of risk is the bridge between the two.

The market price of risk is the extra return investors demand for bearing each source of risk. The risk-neutral version fits it so that the model's yields match the 13-week, 5-year, 10-year and 30-year US Treasury yields on every historical date. It has five parameters, all of which change only the drift:

- `risk_premium_v`: under the risk-neutral measure, `v` mean-reverts at its real-world speed plus this premium.
- Two constant premiums, one per leg: shift that leg's expected next value by a fixed amount per period.
- Two variance premiums, one per leg: shift it in proportion to `v`.

Everything else is identical under both measures, so the risk-neutral parameters simulate with the same machinery as the real-world ones. The premiums depend on a constant and on `v` only, a completely affine price of risk ([Duffie and Kan, 1996](https://doi.org/10.1111/j.1467-9965.1996.tb00123.x){:target="_blank"}). DNB uses the richer essentially affine form of [Duffee (2002)](https://doi.org/10.1111/1540-6261.00426){:target="_blank"}, but a short quarterly sample cannot reliably pin down the twelve parameters that form needs.

**Calibration.** A nonlinear least-squares fit minimizes the squared gap between model and observed yields, summed over all four maturities. Each maturity must be a whole number of periods, so a monthly or quarterly pair works and a yearly pair raises an error (13 weeks is a quarter of a year). At least 10 dates must overlap.

**Bond prices and the yield curve.** Zero-coupon bond prices come from a discrete-time recursion, `exp(A[n] + Bv[n]*v + Br[n]*r + Bpi[n]*pi)` for a bond `n` periods out, evaluated at the pair's current state. That gives you a model yield curve at any maturity that is a whole number of periods, including maturities the Treasury panel does not quote. The one-period yield equals today's short rate.

```python
from financetoolkit import Toolkit

from financescenarios.models.knw_sv.knw_sv_controller import KnwSv
from financescenarios.models.knw_sv_q.knw_sv_q_controller import KnwSvQ

toolkit = Toolkit(
    ["^IRX", "^FVX", "^TNX", "^TYX"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1990-01-01"
)
knw_sv = KnwSv(toolkit)
knw_sv.calibrate_triple("interest_rate", "inflation", period="quarterly")

knw_sv_q = KnwSvQ(toolkit)
knw_sv_q.calibrate_mpr(knw_sv, "interest_rate", "inflation", period="quarterly")

for tenor in [0.25, 1, 5, 10, 30]:
    print(tenor, knw_sv_q.zero_coupon_yield("interest_rate", tenor))
```

In one fit (calibrated on 2026-10-04) the curve started at the 3.75% short rate, rose to 4.53% at five years and flattened just under 5% beyond ten, below the latest Treasury yields, since the premiums are fitted across the whole history.

**Accuracy limits.**

- The closed-form prices assume the rate's and inflation's shocks are uncorrelated. The Monte Carlo engine still applies the full correlation matrix; only the pricing formula leaves it out.
- The inflation premiums, especially the variance one, are weakly identified. Inflation reaches nominal bond prices only through its effect on the rate. A real (TIPS) curve or inflation swaps would fix this; neither is in the project's data.
- On a short sample, judge the fit by how closely it reprices the yields; the individual premiums are less reliable.

## The Stochastic Deflator

A deflator lets you value a liability straight off a real-world run, so you do not need a second, risk-neutral simulation when you want both views.

Following [Cheng and Planchet (2018)](https://hal.science/hal-01730072){:target="_blank"}, the deflator `D(T)` combines discounting at the simulated short rate with a per-path weight that reweights real-world paths into risk-neutral ones. Multiply a cash flow at `T` by `D(T)` on the same path and average across paths to get its value today.

Each step reweights the rate's and inflation's realized shocks. `v`'s own shock is not reweighted, which means the deflator treats the price of turbulence risk as zero. Its accuracy therefore depends on `risk_premium_v`:

- At `risk_premium_v = 0`, the average of `D(T)` over 40,000 to 60,000 paths matches the closed-form bond price within about 0.1% to 2%, up to a 10-year maturity.
- With a realistic nonzero premium of about 15% of `v`'s mean-reversion speed, the average undershoots the closed-form price by about 1% at 2 years, 8% at 5 years and 20% at 10 years.

Rely on it only when `risk_premium_v` is small relative to `v`'s mean-reversion speed, or for short maturities; the calibration warns past 5% of that speed. On the live US fit the premium was far past that, and the deflator average collapsed toward zero, while plain discounting at the simulated short rate stayed close.

For now the deflator is Python-only. The engine does not store `v`'s path, so you simulate and record `v`, the rate and inflation yourself; the [KnwSvQ reference](/projects/financescenarios/docs/reference/knw-sv-q) has a worked example.

## Configuring a KNW Run

The config checks the rules below at load time, because a mistake here would distort a run without any error.

A KNW pair is two entries, one under `interest_rates` and one under `inflation`, that name each other. A minimal factor set, for example `factor-sets/knw.yaml`:

```yaml
name: KNW
description: "US short rate and inflation coupled both ways, with an equity leg on the shared turbulence."

interest_rates:
  - name: interest_rate
    source: oecd
    country: United States
    term: short
    period: quarterly
    method: knw_sv
    inflation_name: inflation

inflation:
  - name: inflation
    country: United States
    period: quarterly
    method: knw_sv
    interest_rate_name: interest_rate

equities:
  - name: equity
    ticker: SPY
    period: quarterly
    method: knw_sv
    nominal_rate_name: interest_rate

unemployment:
  - name: unemployment
    country: United States
    inflation_name: inflation
```

And a settings profile that runs at the same frequency, for example `settings/quarterly.yaml` next to the `default.yaml` that `scaffold_project()` copies into your project:

```yaml
name: Quarterly
description: "Default, stepped quarterly to match a KNW factor set."
extends: default.yaml

engine:
  frequency: quarterly
```

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(settings="quarterly", factor_set="knw")
result = scenarios.simulate(years=30)
```

For plain KNW, set `method: knw` on both entries and drop the equity entry. For the risk-neutral version, add `measure: risk_neutral` to both the rate and the inflation entry; the four Treasury tickers are added to the run automatically, and the fitted risk-neutral parameters replace the real-world ones before simulating.

The config rejects:

- **An incomplete pairing.** Both entries must use the same method and name each other (`inflation_name` on the rate, `interest_rate_name` on inflation). `knw` pairs only with `knw`, and `knw_sv` only with `knw_sv`.
- **A mismatched period.** Both entries, and a `knw_sv` equity leg, must share one `period`, and it must equal `engine.frequency`. Only `monthly`, `quarterly` and `yearly` are supported, since the OECD series have no daily or weekly data.
- **A mismatched measure.** On a `knw_sv` pair, the rate and inflation entries must use the same `measure`, since the market price of risk is fitted for the whole system at once.
- **Unsupported options.** Belief overrides, `volatility_model: garch` and `condition_on_business_cycle` on either entry, and `condition_on_interest_rate` on the inflation entry. Beliefs are excluded because the long-run level depends on both legs together, so there is no single long-run mean to override.
- **A risk-neutral equity leg.** A `knw_sv` equity entry cannot name a rate entry with `measure: risk_neutral`.

**Why the frequency rule matters.** The fitted coefficients are a recursion applied once per period, with no time step to rescale. Run a quarterly fit at a monthly engine frequency and the recursion compounds three times too fast. This was confirmed against DNB's CP2022 scenario set: the equity leg overshot DNB's median by 15 to 20 percentage points a year at a monthly engine frequency, and by 0.5 to 1.6 points once the engine was matched to quarterly.

## Using the Classes Directly

Calling the calibration classes yourself is useful when you want to inspect the fitted parameters before committing to a full run.

```python
from financetoolkit import Toolkit

from financescenarios.factors.equities.equities_controller import fetch_equity_prices
from financescenarios.models.knw.knw_controller import Knw
from financescenarios.models.knw_sv.knw_sv_controller import KnwSv

toolkit = Toolkit(["^GSPC"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1990-01-01")

knw = Knw(toolkit)
rate_params, inflation_params = knw.calibrate_pair("interest_rate", "inflation", period="quarterly")

knw_sv = KnwSv(toolkit)
v_params, rate_params, inflation_params = knw_sv.calibrate_triple(
    "interest_rate", "inflation", period="quarterly"
)

dates, prices = fetch_equity_prices(toolkit, "^GSPC", "quarterly")
equity_params = knw_sv.calibrate_equity_leg(
    "equity", "interest_rate", "inflation", prices, dates, period="quarterly"
)
```

The rate and inflation data come through the Finance Toolkit without an API key. The rate leg defaults to the US OECD short rate; pass `interest_rate_source="ticker"` for a Yahoo Finance Treasury-yield ticker, or `interest_rate_country` and `interest_rate_term` for another country or the long rate. Inflation is OECD consumer price index growth for `inflation_country`. One instance holds any number of pairs.

## How It Compares With DNB's CP2022

If you use these models alongside DNB's official scenario set, you need to know where they follow it and where they take a different route.

The [CP2022 Technical Appendix](https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix){:target="_blank"} specifies DNB's full model.

| Aspect | DNB CP2022 | Finance Scenarios |
|:--|:--|:--|
| Rate and inflation coupling | Full 2x2 matrix | Same (`knw`, `knw_sv`) |
| Stochastic volatility | Heston-type factor `v` scaling rate, inflation, equity and CPI index | Same structure in `knw_sv`; `knw` folds `v`'s constant contribution into the intercepts |
| How `v` is recovered | Inverted from market yields on each date | Rolling average of the pair's squared surprises, a different estimate |
| Leverage effect | Shocks to `v` correlated with rate and inflation shocks | Not fitted: `v`'s shocks are independent of the legs' shocks |
| Equity | Risk premium and variance constrained by option-implied volatility | Fitted on price history only |
| CPI index row | Modeled | Not modeled |
| Risk-neutral measure | Essentially affine price of risk, fitted to option, swaption and inflation-cap prices | Completely affine price of risk, fitted to the Treasury yield curve |
| Yield curve | Closed form for any maturity from the affine model | Closed form in the risk-neutral version; the separate yield curve factor uses an unrelated Nelson-Siegel fit |

The project has no rate or inflation derivatives data, so the risk-neutral version is fitted to the yield curve, standard affine term-structure practice. It is a genuine change of measure on different data, and a different model from DNB's own.

## Further Reading

- Koijen, R.S.J., Nijman, T.E., Werker, B.J.M. (2010). [When Can Life Cycle Investors Benefit from Time-Varying Bond Risk Premia?](https://doi.org/10.1093/rfs/hhp058){:target="_blank"} The Review of Financial Studies, 23(2), 741-780.
- Commissie Parameters (2022). [Technical Appendix: Specification of the CP2022 Model](https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix){:target="_blank"}.
- Heston, S.L. (1993). [A Closed-Form Solution for Options with Stochastic Volatility with Applications to Bond and Currency Options](https://doi.org/10.1093/rfs/6.2.327){:target="_blank"}. The Review of Financial Studies, 6(2), 327-343.
- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). [A Theory of the Term Structure of Interest Rates](https://doi.org/10.2307/1911242){:target="_blank"}. Econometrica, 53(2), 385-407.
- Andersen, L. (2008). [Simple and Efficient Simulation of the Heston Stochastic Volatility Model](https://doi.org/10.21314/jcf.2008.189){:target="_blank"}. Journal of Computational Finance, 11(3), 1-42.
- Duffie, D., Kan, R. (1996). [A Yield-Factor Model of Interest Rates](https://doi.org/10.1111/j.1467-9965.1996.tb00123.x){:target="_blank"}. Mathematical Finance, 6(4), 379-406.
- Duffee, G.R. (2002). [Term Premia and Interest Rate Forecasts in Affine Models](https://doi.org/10.1111/1540-6261.00426){:target="_blank"}. Journal of Finance, 57(1), 405-443.
- Cheng, P.-K., Planchet, F. (2018). [Stochastic Deflator for an Economic Scenario Generator with Five Factors](https://hal.science/hal-01730072){:target="_blank"}. HAL preprint.
- Lütkepohl, H. (2005). [New Introduction to Multiple Time Series Analysis](https://doi.org/10.1007/978-3-540-27752-1){:target="_blank"}. Springer.
