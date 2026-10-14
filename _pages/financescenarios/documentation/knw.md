---
title: KNW Models
seo_title: "KNW Models Documentation | Finance Scenarios"
seo_title_suffix: false
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

They follow the term-structure model of [Koijen, Nijman and Werker (2010)](https://doi.org/10.1093/rfs/hhp058){:target="_blank"}, which the Dutch Commissie Parameters extends in its CP2022 model ([Technical Appendix, p. 1](https://open.overheid.nl/repository/ronl-f2685a42fd0bf01d5821446bcda34e719fdf7ef1/1/pdf/bijlage-2-technische-appendix.pdf#page=1){:target="_blank"}), the model behind the scenario sets De Nederlandsche Bank (DNB) publishes for Dutch pension funds.

Finance Scenarios implements a discrete, reduced-form approximation inspired by both: a VAR on the observed short rate and inflation, fitted by least squares, not the latent-factor model those papers filter from the yield curve. For the single-factor short-rate models and the Nelson-Siegel curve, see [interest rates](/projects/financescenarios/docs/interest-rates).

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
    v["<b>Turbulence v</b><small>hidden, shared by all three</small>"]
    r["<b>Interest rate</b>"]
    pi["<b>Inflation</b>"]
    eq["<b>Equity</b><small>optional</small>"]
    v -->|drift and volatility| r
    v -->|drift and volatility| pi
    v -->|volatility| eq
    r <-->|last period's level| pi
    r -->|drift: short rate plus premium| eq
    class v accent
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

There is no long-run mean per leg. The pair settles jointly at $$(I - \Phi)^{-1}c$$, and the system must be stable: if a shock would never die out (the largest eigenvalue of $$\Phi$$ is 1 or more), the fit stops with an error. Both legs are fitted by ordinary least squares on the dates both series cover, on deviations from the history's averages ([Lütkepohl, 2005](https://doi.org/10.1007/978-3-540-27752-1){:target="_blank"}, section 3.3), so the pair settles at those averages. Fitting a free intercept per leg instead lets a pair this persistent amplify where the sample happens to start and end.

On 146 quarters of the US OECD short rate and CPI growth, 1990Q1 to 2026Q2 (calibrated on 2026-10-14):

| leg | intercept | own persistence | cross coupling | volatility |
|:----|----------:|----------------:|---------------:|-----------:|
| interest rate | -0.0005 | 0.9432 | 0.0803 | 0.0043 |
| inflation | 0.0037 | 0.8890 | -0.0206 | 0.0073 |

One percentage point more inflation adds 0.080 points to next quarter's rate, in line with central banks raising rates when inflation runs high, though a reduced-form regression cannot single out that channel. A higher rate nudges inflation down only slightly. A joint shock halves in about 8 quarters, and the pair settles at a 3.04% rate and 2.72% inflation: a long-run real short rate of about 0.3%. That is below the 1.0% in the Federal Reserve's longer-run projections (a 3.0% federal funds rate against 2.0% PCE inflation in the [September 2025 Summary of Economic Projections](https://www.federalreserve.gov/monetarypolicy/files/fomcprojtabl20250917.pdf){:target="_blank"}, Table 1), because the sample includes the zero-rate years 2009-2015 and 2020-2021, and with 36 years of data the long-run levels carry a sampling error of about 0.6 percentage points. A belief cannot override them, since the long-run levels are a joint property of both legs; the history window the pair is fitted on is the lever.

## Stochastic Volatility

Markets alternate between calm and stressed spells; plain KNW gives every period the same randomness. The stochastic-volatility variant adds DNB's hidden variance factor $$v_t$$, the square of the volatility ([CP2022 Technical Appendix, section 1, p. 1](https://open.overheid.nl/repository/ronl-f2685a42fd0bf01d5821446bcda34e719fdf7ef1/1/pdf/bijlage-2-technische-appendix.pdf#page=1){:target="_blank"}), a CIR process ([Cox, Ingersoll and Ross, 1985](https://doi.org/10.2307/1911242){:target="_blank"}) of the kind [Heston (1993)](https://doi.org/10.1093/rfs/6.2.327){:target="_blank"} uses for variance: mean-reverting and never negative.

$$
dv_t = a_v(\theta_v - v_t)\,dt + \sigma_v\sqrt{v_t}\,dW^v_t
$$

Each leg reads last period's $$v$$ twice, in its drift and in its variance:

$$
r_t = c_r + \lambda_r v_{t-1} + \phi_{rr} r_{t-1} + \phi_{r\pi}\pi_{t-1} + \sqrt{h_r + \eta_r v_{t-1}}\;\varepsilon^r_t
$$

with the same shape for inflation. $$\lambda$$ lets turbulence move the expected level, as in DNB's model, $$h$$ is the calm-state variance and $$\eta$$ how strongly variance rises with turbulence. Because one $$v$$ drives every leg, volatility in rates, inflation and equity rises and falls together: the clustering of stress across asset classes that a constant-volatility model misses.

**Estimating turbulence.** DNB recovers $$v$$ from market yields on each date. Finance Scenarios estimates it from the pair's own history: the average of plain KNW's squared surprises over the past year (four quarters, or twelve months), lagged one period, is the proxy for $$v$$. The one-year window follows [Engle's (1982)](https://doi.org/10.2307/1912773){:target="_blank"} four-quarter ARCH model of inflation variance. A CIR process is fitted to that proxy and both legs are refitted with it as an extra input; if neither leg's variance rises with $$v$$, the fit suggests plain KNW. Simulation uses [Andersen's (2008)](https://doi.org/10.21314/jcf.2008.189){:target="_blank"} Quadratic-Exponential scheme, which keeps $$v$$ non-negative with little bias; DNB's model uses Andersen's scheme too, with a martingale correction ([CP2022 Technical Appendix, section 9.1, p. 8](https://open.overheid.nl/repository/ronl-f2685a42fd0bf01d5821446bcda34e719fdf7ef1/1/pdf/bijlage-2-technische-appendix.pdf#page=8){:target="_blank"}).

On the same US quarterly data (calibrated on 2026-10-05), turbulence halves in about 1.7 years. Turbulence is the variance of a quarter's combined rate and inflation surprise. Today it corresponds to a surprise of about 0.3 percentage points a quarter, against about 0.8 at its long-run level, so the pair starts calmer than usual. Inflation responds most: its standard deviation is 0.31% a quarter at $$v = 0$$ and 0.68% at the long-run level. The Feller condition $$2a_v\theta_v \ge \sigma_v^2$$ fails on this fit, so simulated turbulence touches zero more often than its long-run distribution suggests.

## The Equity Leg

An equity index on the same turbulence factor becomes volatile when rates and inflation do. Following DNB's equity row, each period's log return is the simulated short rate plus a constant risk premium, with variance linked to $$v$$:

$$
\ln\frac{S_t}{S_{t-1}} = r_{t-1}\,\Delta t + \mu - \tfrac{1}{2}h_{t-1} + \sqrt{h_{t-1}}\,\varepsilon^S_t, \qquad h_{t-1} = h_S + \eta_S v_{t-1}
$$

$$\Delta t$$ is the period length in years and $$\mu$$ the premium per period, corrected for volatility drag. Over the S&P 500's quarterly history since 1990 (calibrated on 2026-10-05), the index earned 1.59% a quarter above the short rate, about 6.4% a year, with volatility of about 13% a year at $$v = 0$$ and 15.3% at the long-run level. The equity leg runs under the real-world measure only.

## The Risk-Neutral Version

A real-world run answers "where might rates go?"; valuing liabilities asks "what is a future cash flow worth today?". The bridge is the market price of risk, the extra return investors demand per unit of each risk. The risk-neutral version fits it so that the model's yields match the 13-week, 5, 10 and 30-year US Treasury yields over the historical sample. It changes only the drift, through five premiums: one on turbulence's mean-reversion speed, and a constant and a turbulence-proportional premium per leg. Premiums that depend on a constant and on $$v$$ only are the completely affine form of [Duffie and Kan (1996)](https://doi.org/10.1111/j.1467-9965.1996.tb00123.x){:target="_blank"}. DNB uses the richer essentially affine form of [Duffee (2002)](https://doi.org/10.1111/1540-6261.00426){:target="_blank"}, whose time-varying bond risk premia are what KNW (2010) is about ([Netspar Discussion Paper 2006-017, section 1.1, p. 6](https://www.netspar.nl/wp-content/uploads/werkernijman06017.pdf){:target="_blank"}); its extra parameters are hard to pin down on a short quarterly sample and a nominal curve alone.

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

In one fit (calibrated on 2026-10-14) the curve started at the 3.75% short rate, rose to about 4.5% at five years and flattened near 4.8% beyond ten, below the latest Treasury yields, since the premiums are fitted across the whole history.

**Limits.**

- The closed-form prices and the market price of risk include the correlation between rate and inflation shocks, estimated from the same changes as the run's correlation matrix, so model bond prices and simulated discount factors agree. Turbulence's own shock is independent of both.
- The inflation risk premium is weakly identified: the price of unexpected inflation risk cannot be identified from nominal yields alone ([Koijen, Nijman and Werker, section 1.4, p. 11](https://www.netspar.nl/wp-content/uploads/werkernijman06017.pdf){:target="_blank"}), so without a real (TIPS) curve or inflation swaps nothing separates real rates from the inflation premium. Judge the fit by how well it reprices nominal yields, not by the individual premiums.

### The Stochastic Deflator

A deflator values a liability straight off a real-world run, so you don't need a second, risk-neutral simulation. Following [Cheng and Planchet (2018)](https://hal.science/hal-01730072){:target="_blank"}, $$D(T)$$ combines discounting at the simulated short rate with a path weight that turns real-world paths into risk-neutral ones; the value of a cash flow $$X_T$$ is the path average of $$D(T)\,X_T$$.

The weight leaves out turbulence's shock, so the deflator is only accurate when the turbulence premium is small. On the live US fit that premium is large (38.5% of turbulence's speed), and the deflator's average misses the model's own bond prices by about 2% at one year and 5% at five (0.9827 against 0.9620, and 0.7606 against 0.7996); the fit warns when the premium is this large. The deflator is available in Python only; the [KnwSvQ reference](/projects/financescenarios/docs/reference/knw-sv-q) has a worked example.

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
| How turbulence is recovered | Treated as observed, with the rate and expected inflation backed out of a nominal and a real yield | Past year's average of the pair's squared surprises |
| Leverage effect | Turbulence shocks correlated with rate and inflation shocks | Not fitted: independent |
| Equity | Premium and variance constrained by option-implied volatility | Fitted on price history only |
| CPI index row | Modeled | Not modeled |
| Risk-neutral measure | Essentially affine, fitted to nominal and real yields and constrained by option, swaption and inflation-cap implied volatilities | Completely affine, fitted to four nominal Treasury yields |

Without real yields or rate and inflation derivatives data, the risk-neutral version is fitted to the nominal yield curve, standard affine term-structure practice. It is a genuine change of measure, but on different data, so it is a different model from DNB's own, not a simplified copy.

## References

- Koijen, R.S.J., Nijman, T.E., Werker, B.J.M. (2010). [When Can Life Cycle Investors Benefit from Time-Varying Bond Risk Premia?](https://doi.org/10.1093/rfs/hhp058){:target="_blank"} The Review of Financial Studies, 23(2), 741-780.
- Commissie Parameters (2022). [Technical Appendix: Specification of the CP2022 Model](https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix){:target="_blank"}.
- Heston, S.L. (1993). [A Closed-Form Solution for Options with Stochastic Volatility with Applications to Bond and Currency Options](https://doi.org/10.1093/rfs/6.2.327){:target="_blank"}. The Review of Financial Studies, 6(2), 327-343.
- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). [A Theory of the Term Structure of Interest Rates](https://doi.org/10.2307/1911242){:target="_blank"}. Econometrica, 53(2), 385-407.
- Andersen, L. (2008). [Simple and Efficient Simulation of the Heston Stochastic Volatility Model](https://doi.org/10.21314/jcf.2008.189){:target="_blank"}. Journal of Computational Finance, 11(3), 1-42.
- Duffie, D., Kan, R. (1996). [A Yield-Factor Model of Interest Rates](https://doi.org/10.1111/j.1467-9965.1996.tb00123.x){:target="_blank"}. Mathematical Finance, 6(4), 379-406.
- Duffee, G.R. (2002). [Term Premia and Interest Rate Forecasts in Affine Models](https://doi.org/10.1111/1540-6261.00426){:target="_blank"}. Journal of Finance, 57(1), 405-443.
- Cheng, P.-K., Planchet, F. (2018). [Stochastic Deflator for an Economic Scenario Generator with Five Factors](https://hal.science/hal-01730072){:target="_blank"}. HAL preprint.
- Engle, R.F. (1982). [Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation](https://doi.org/10.2307/1912773){:target="_blank"}. Econometrica, 50(4), 987-1007.
- Lütkepohl, H. (2005). [New Introduction to Multiple Time Series Analysis](https://doi.org/10.1007/978-3-540-27752-1){:target="_blank"}. Springer.
