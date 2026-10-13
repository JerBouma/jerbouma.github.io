---
title: KNW Models
seo_title: KNW Models Documentation – Finance Scenarios
excerpt: "The Koijen-Nijman-Werker family behind the Dutch CP2022 scenario model: nominal rates and inflation as one coupled system, shared stochastic volatility, an equity leg and a risk-neutral version fitted to the yield curve."
description: "Nominal rates and inflation as one coupled system, KNW style: two-way coupling, stochastic volatility, the risk-neutral version and how it compares with DNB."
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

A pension fund with inflation-indexed benefits, discounted at nominal rates, is exposed to the joint behavior of rates and inflation more than to either one alone. The KNW models simulate the two as one system: today's inflation shapes where rates go next, and today's rate shapes where inflation goes next.

They follow the term-structure model of [Koijen, Nijman and Werker (2010)](https://doi.org/10.1093/rfs/hhp058){:target="_blank"}, which the Dutch Commissie Parameters extends in its CP2022 model, the model behind the scenario sets De Nederlandsche Bank (DNB) publishes for Dutch pension funds. For the single-factor short-rate models and the Nelson-Siegel curve, see [interest rates](/projects/financescenarios/docs/interest-rates).

## Why Model Rates and Inflation Together

Correlated shocks only link the surprises of the same month. They say nothing about how today's level of inflation pushes rates over the next years, the channel that matters for long-dated, inflation-linked liabilities.

Here the two state variables are the nominal short rate and year-over-year CPI inflation, which stands in for expected inflation. Their link reflects the Fisher logic that a nominal yield is roughly a real yield, plus expected inflation, plus an inflation risk premium:

$$
y^{\text{nom}}_t(\tau) \approx y^{\text{real}}_t(\tau) + \mathbb{E}_t[\bar\pi_{t,\tau}] + \text{IRP}_t(\tau)
$$

Persistent inflation tends to lift nominal rates, and a high real rate tends to cool inflation. Coupling the two in the drift keeps rates, inflation and the implied real rate consistent along every path and gives the pair one joint long-run level. The other options in Finance Scenarios link the two in one direction only (the Wilkie cascade, or conditioning inflation on the rate change); KNW goes both ways and uses the other variable's level, not its change.

## The Three Variants

| Variant | What it adds | Use it for |
|:--|:--|:--|
| KNW (`knw`) | Two-way coupling at constant volatility | The interpretable core; a first look at the joint dynamics |
| KNW with stochastic volatility (`knw_sv`) | A shared hidden turbulence factor $$v$$ that scales volatility and shifts the drift; optional equity leg | Calm and stressed regimes that hit rates, inflation and equity at once |
| Risk-neutral KNW (`knw_sv` with `measure: risk_neutral`) | A market price of risk fitted to the Treasury curve, closed-form bond prices, a stochastic deflator | Valuation, and a model yield curve at any maturity |

Each builds on the previous one: with the turbulence terms at zero, KNW with stochastic volatility is plain KNW exactly. Parameter details are in the reference pages for [Knw](/projects/financescenarios/docs/reference/knw), [KnwSv](/projects/financescenarios/docs/reference/knw-sv) and [KnwSvQ](/projects/financescenarios/docs/reference/knw-sv-q).

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

Turbulence drives every leg and is never driven back. Plain KNW keeps only the two-way arrow between rate and inflation.

## KNW: Two-Way Coupling

Each leg is a regression on last period's level of both variables, a bivariate VAR(1) ([Lütkepohl, 2005](https://doi.org/10.1007/978-3-540-27752-1){:target="_blank"}):

$$
\begin{pmatrix} r_t \\ \pi_t \end{pmatrix}
= c + \Phi \begin{pmatrix} r_{t-1} \\ \pi_{t-1} \end{pmatrix} + \begin{pmatrix} \sigma_r\,\varepsilon^r_t \\ \sigma_\pi\,\varepsilon^\pi_t \end{pmatrix}
$$

$$r_t$$ is the nominal short rate and $$\pi_t$$ year-over-year CPI inflation. The diagonal of $$\Phi$$ is each variable's own persistence, the off-diagonal terms the cross-coupling: how much of the other variable's level spills over. $$c$$ holds two intercepts and $$\sigma$$ the size of each period's surprise.

There is no long-run mean per leg. The pair settles jointly at $$(I - \Phi)^{-1}c$$, and the system must be stable: if a shock would never die out (the largest eigenvalue of $$\Phi$$ is 1 or more), the fit stops with an error. Both legs are fitted by ordinary least squares on the dates both series cover.

On 146 quarters of the US OECD short rate and CPI growth, 1990Q1 to 2026Q2 (calibrated on 2026-10-05):

| leg | intercept | own persistence | cross coupling | volatility |
|:----|----------:|----------------:|---------------:|-----------:|
| interest rate | -0.0009 | 0.9397 | 0.0918 | 0.0044 |
| inflation | 0.0036 | 0.8910 | -0.0246 | 0.0073 |

One percentage point more inflation adds 0.092 points to next quarter's rate, in line with central banks raising rates when inflation runs high, though a reduced-form regression cannot single out that channel. A higher rate nudges inflation down only slightly. A joint shock halves in about 8 quarters, and the pair settles at a 2.60% rate and 2.74% inflation: a long-run rate just below long-run inflation, which reflects the long near-zero-rate spell in the sample.

## Stochastic Volatility

Markets alternate between calm and stressed spells; plain KNW gives every period the same randomness. The stochastic-volatility variant adds DNB's hidden variance factor $$v_t$$, a CIR process ([Cox, Ingersoll and Ross, 1985](https://doi.org/10.2307/1911242){:target="_blank"}) of the kind [Heston (1993)](https://doi.org/10.1093/rfs/6.2.327){:target="_blank"} uses for variance: mean-reverting and never negative.

$$
dv_t = a_v(\theta_v - v_t)\,dt + \sigma_v\sqrt{v_t}\,dW^v_t
$$

Each leg reads last period's $$v$$ twice, in its drift and in its variance:

$$
r_t = c_r + \lambda_r v_{t-1} + \phi_{rr} r_{t-1} + \phi_{r\pi}\pi_{t-1} + \sqrt{h_r + \eta_r v_{t-1}}\;\varepsilon^r_t
$$

with the same shape for inflation. $$\lambda$$ lets turbulence move the expected level, as in DNB's model, $$h$$ is the calm-state variance and $$\eta$$ how strongly variance rises with turbulence. Because one $$v$$ drives every leg, volatility in rates, inflation and equity rises and falls together: the clustering of stress across asset classes that a constant-volatility model misses.

**Estimating turbulence.** DNB recovers $$v$$ from market yields on each date. Finance Scenarios estimates it from the pair's own history: a trailing four-period average of plain KNW's squared surprises, lagged one period, is the proxy for $$v$$. A CIR process is fitted to that proxy and both legs are refitted with it as an extra input; if neither leg's variance rises with $$v$$, the fit suggests plain KNW. Simulation uses [Andersen's (2008)](https://doi.org/10.21314/jcf.2008.189){:target="_blank"} Quadratic-Exponential scheme, which keeps $$v$$ non-negative with little bias.

On the same US quarterly data (calibrated on 2026-10-05), turbulence halves in about 1.7 years. Its current value (0.0000094) is well below its long-run level (0.0000627), so the pair starts calmer than usual. Inflation responds most: its standard deviation is 0.31% a quarter at $$v = 0$$ and 0.68% at the long-run level. The Feller condition $$2a_v\theta_v \ge \sigma_v^2$$ fails on this fit, so simulated turbulence touches zero more often than its long-run distribution suggests.

## The Equity Leg

An equity index on the same turbulence factor becomes volatile when rates and inflation do. Following DNB's equity row, each period's log return is the simulated short rate plus a constant risk premium, with variance linked to $$v$$:

$$
\ln\frac{S_t}{S_{t-1}} = r_{t-1}\,\Delta t + \mu - \tfrac{1}{2}h_{t-1} + \sqrt{h_{t-1}}\,\varepsilon^S_t, \qquad h_{t-1} = h_S + \eta_S v_{t-1}
$$

$$\Delta t$$ is the period length in years and $$\mu$$ the premium per period, corrected for volatility drag. Over the S&P 500's quarterly history since 1990 (calibrated on 2026-10-05), the index earned 1.59% a quarter above the short rate, about 6.4% a year, with volatility of about 13% a year at $$v = 0$$ and 15.3% at the long-run level. The equity leg runs under the real-world measure only.

## The Risk-Neutral Version

A real-world run answers "where might rates go?"; valuing liabilities asks "what is a future cash flow worth today?". The bridge is the market price of risk, the extra return investors demand per unit of each risk. The risk-neutral version fits it so that the model's yields match the 13-week, 5, 10 and 30-year US Treasury yields over the historical sample. It changes only the drift, through five premiums: one on turbulence's mean-reversion speed, and a constant and a turbulence-proportional premium per leg. Premiums that depend on a constant and on $$v$$ only are the completely affine form of [Duffie and Kan (1996)](https://doi.org/10.1111/j.1467-9965.1996.tb00123.x){:target="_blank"}. DNB uses the richer essentially affine form of [Duffee (2002)](https://doi.org/10.1111/1540-6261.00426){:target="_blank"}, whose time-varying bond risk premia are what KNW (2010) is about; its extra parameters are hard to pin down on a short quarterly sample and a nominal curve alone.

Zero-coupon prices follow from an affine recursion, for a bond $$n$$ periods out:

$$
P_t(n) = \exp\!\big(A_n + B^v_n v_t + B^r_n r_t + B^\pi_n \pi_t\big)
$$

That gives a model yield at any whole number of periods, including maturities the Treasury data does not quote. A monthly or quarterly pair works; a yearly one does not, since the 13-week yield is not a whole number of years.

```python
from financetoolkit import Toolkit

from financescenarios.models.knw_sv.knw_sv_controller import KnwSv
from financescenarios.models.knw_sv_q.knw_sv_q_controller import KnwSvQ

toolkit = Toolkit(
    ["^IRX", "^FVX", "^TNX", "^TYX"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1990-01-01"
)
knw_sv = KnwSv(toolkit)
knw_sv.calibrate_triple("interest_rate", "inflation", period="quarterly")  # real-world fit

knw_sv_q = KnwSvQ(toolkit)
knw_sv_q.calibrate_mpr(knw_sv, "interest_rate", "inflation", period="quarterly")  # market price of risk

for tenor in [0.25, 1, 5, 10, 30]:
    print(tenor, knw_sv_q.zero_coupon_yield("interest_rate", tenor))
```

In one fit (calibrated on 2026-10-04) the curve started at the 3.75% short rate, rose to about 4.5% at five years and flattened just under 5% beyond ten, below the latest Treasury yields, since the premiums are fitted across the whole history.

**Limits.**

- The closed-form prices assume uncorrelated rate and inflation shocks; the simulation still uses the full correlation matrix.
- The inflation risk premium is weakly identified: without a real (TIPS) curve or inflation swaps, nothing separates real rates from the inflation premium. Judge the fit by how well it reprices nominal yields, not by the individual premiums.

### The Stochastic Deflator

A deflator values a liability straight off a real-world run, so you don't need a second, risk-neutral simulation. Following [Cheng and Planchet (2018)](https://hal.science/hal-01730072){:target="_blank"}, $$D(T)$$ combines discounting at the simulated short rate with a path weight that turns real-world paths into risk-neutral ones; the value of a cash flow $$X_T$$ is the path average of $$D(T)\,X_T$$.

The weight covers the rate and inflation shocks but not turbulence's, so accuracy depends on the turbulence premium. With that premium at zero, the average deflator matches closed-form bond prices within about 0.1% to 2% up to ten years. With a premium of about 15% of turbulence's mean-reversion speed, it undershoots by about 1% at 2 years, 8% at 5 years and 20% at 10 years. On the live US fit the premium was about two-thirds of that speed and the average deflator collapsed toward zero, so it is not usable there; the fit warns once the premium passes 5% of the speed. The deflator is available in Python only; the [KnwSvQ reference](/projects/financescenarios/docs/reference/knw-sv-q) has a worked example.

## Configuring a KNW Run

A KNW pair is a rate entry and an inflation entry that name each other and use the same method. The fitted coefficients are a recursion applied once per period, with no time step to rescale, so the simulation frequency must equal the fitting period (monthly, quarterly or yearly); the configuration rejects a mismatch.

```yaml
# knw.yaml
start_date: 2026-10-01
engine:
  frequency: quarterly          # must equal the pair's period
toolkit:
  start_date: 1990-01-01        # history used for the fit

interest_rates:
  - name: interest_rate
    source: oecd
    country: United States
    term: short
    period: quarterly
    method: knw_sv
    inflation_name: inflation
    # measure: risk_neutral     # on both legs, without the equity entry, for the risk-neutral version

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
```

```python
from financescenarios import Scenarios, load_config

result = Scenarios.from_config(load_config("knw.yaml")).simulate(years=30)
```

Beliefs, GARCH and business-cycle conditioning are not available: the long-run level is a joint property of both legs, so there is no single long-run mean to override. The equity leg needs a real-world rate.

## How It Compares with DNB's CP2022

The [CP2022 Technical Appendix](https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix){:target="_blank"} specifies DNB's full model.

| Aspect | DNB CP2022 | Finance Scenarios |
|:--|:--|:--|
| Rate and inflation coupling | Full 2x2 matrix | Same |
| Stochastic volatility | Heston-type factor scaling rate, inflation, equity and CPI index | Same structure |
| How turbulence is recovered | Inverted from market yields on each date | Rolling average of the pair's squared surprises |
| Leverage effect | Turbulence shocks correlated with rate and inflation shocks | Not fitted: independent |
| Equity | Premium and variance constrained by option-implied volatility | Fitted on price history only |
| CPI index row | Modeled | Not modeled |
| Risk-neutral measure | Essentially affine, fitted to option, swaption and inflation-cap prices | Completely affine, fitted to the Treasury yield curve |

Without rate or inflation derivatives data, the risk-neutral version is fitted to the yield curve, standard affine term-structure practice. It is a genuine change of measure, but on different data, so it is a different model from DNB's own, not a simplified copy.

## References

- Koijen, R.S.J., Nijman, T.E., Werker, B.J.M. (2010). [When Can Life Cycle Investors Benefit from Time-Varying Bond Risk Premia?](https://doi.org/10.1093/rfs/hhp058){:target="_blank"} The Review of Financial Studies, 23(2), 741-780.
- Commissie Parameters (2022). [Technical Appendix: Specification of the CP2022 Model](https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix){:target="_blank"}.
- Heston, S.L. (1993). [A Closed-Form Solution for Options with Stochastic Volatility with Applications to Bond and Currency Options](https://doi.org/10.1093/rfs/6.2.327){:target="_blank"}. The Review of Financial Studies, 6(2), 327-343.
- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). [A Theory of the Term Structure of Interest Rates](https://doi.org/10.2307/1911242){:target="_blank"}. Econometrica, 53(2), 385-407.
- Andersen, L. (2008). [Simple and Efficient Simulation of the Heston Stochastic Volatility Model](https://doi.org/10.21314/jcf.2008.189){:target="_blank"}. Journal of Computational Finance, 11(3), 1-42.
- Duffie, D., Kan, R. (1996). [A Yield-Factor Model of Interest Rates](https://doi.org/10.1111/j.1467-9965.1996.tb00123.x){:target="_blank"}. Mathematical Finance, 6(4), 379-406.
- Duffee, G.R. (2002). [Term Premia and Interest Rate Forecasts in Affine Models](https://doi.org/10.1111/1540-6261.00426){:target="_blank"}. Journal of Finance, 57(1), 405-443.
- Cheng, P.-K., Planchet, F. (2018). [Stochastic Deflator for an Economic Scenario Generator with Five Factors](https://hal.science/hal-01730072){:target="_blank"}. HAL preprint.
- Lütkepohl, H. (2005). [New Introduction to Multiple Time Series Analysis](https://doi.org/10.1007/978-3-540-27752-1){:target="_blank"}. Springer.
