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

A pension fund with inflation-indexed benefits, discounted at nominal rates, is exposed to the joint behavior of rates and inflation more than to either one alone. The KNW models simulate the two as one system: today's inflation shapes where rates go next, and today's rate shapes where inflation goes next.

They follow the term-structure model of [Koijen, Nijman and Werker (2010)](https://doi.org/10.1093/rfs/hhp058){:target="_blank"}, which the Dutch Commissie Parameters extends in its CP2022 model ([Commissie Parameters, 2022, Technical Appendix, p. 1](https://open.overheid.nl/repository/ronl-f2685a42fd0bf01d5821446bcda34e719fdf7ef1/1/pdf/bijlage-2-technische-appendix.pdf#page=1){:target="_blank"}), the model behind the scenario sets De Nederlandsche Bank (DNB) publishes for Dutch pension funds.

Finance Scenarios implements a discrete, reduced-form approximation inspired by both: a VAR on the observed short rate and inflation, fitted by least squares, not the latent-factor model those papers filter from the yield curve. For the single-factor short-rate models and the Nelson-Siegel curve, see [interest rates](/projects/financescenarios/docs/interest-rates).

<div class="ca-nav">
  <a href="#knw-two-way-coupling"><i class="fas fa-shuffle" aria-hidden="true"></i>Two-way coupling</a>
  <a href="#stochastic-volatility"><i class="fas fa-pulse" aria-hidden="true"></i>Stochastic volatility</a>
  <a href="#the-equity-leg"><i class="fas fa-chart-line" aria-hidden="true"></i>Equity leg</a>
  <a href="#the-risk-neutral-version"><i class="fas fa-scale-balanced" aria-hidden="true"></i>Risk-neutral version</a>
  <a href="#configuring-a-knw-run"><i class="fas fa-sliders-h" aria-hidden="true"></i>Configuring a run</a>
  <a href="#how-it-compares-with-dnbs-cp2022"><i class="fas fa-landmark" aria-hidden="true"></i>Compared with DNB</a>
</div>

## Why Model Rates and Inflation Together

Correlated shocks only link the surprises of the same month. They say nothing about how today's level of inflation pushes rates over the next years, the channel that matters for long-dated, inflation-linked liabilities.

Here the two state variables are the nominal short rate and year-over-year CPI inflation, which stands in for expected inflation. Their link reflects the Fisher logic that a nominal yield is roughly a real yield, plus expected inflation, plus an inflation risk premium:

$$
y^{\text{nom}}_t(\tau) \approx y^{\text{real}}_t(\tau) + \mathbb{E}_t[\bar\pi_{t,\tau}] + \text{IRP}_t(\tau)
$$

Persistent inflation tends to lift nominal rates, and a high real rate tends to cool inflation. Coupling the two in the drift keeps rates, inflation and the implied real rate consistent along every path and gives the pair one joint long-run level. The other options in Finance Scenarios link the two in one direction only (the Wilkie cascade, or conditioning inflation on the rate change); KNW goes both ways and uses the other variable's level, not its change.

## The Three Variants

Each variant adds one layer to the one before:

| Variant | What it adds | Use it for |
|:--|:--|:--|
| KNW (`knw`) | Two-way coupling at constant volatility | The interpretable core; a first look at the joint dynamics |
| KNW with stochastic volatility (`knw_sv`) | A shared hidden turbulence factor $$v$$ that scales volatility and shifts the drift; optional equity leg | Calm and stressed regimes that hit rates, inflation and equity at once |
| Risk-neutral KNW (`knw_sv` with `measure: risk_neutral`) | A market price of risk fitted to the Treasury curve, closed-form bond prices, a stochastic deflator | Valuation, and a model yield curve at any maturity |

Each builds on the previous one: with the turbulence terms at zero, KNW with stochastic volatility is plain KNW exactly. Parameter details are in the reference pages for [Knw](/projects/financescenarios/docs/reference/knw), [KnwSv](/projects/financescenarios/docs/reference/knw-sv) and [KnwSvQ](/projects/financescenarios/docs/reference/knw-sv-q).

<div class="fs-diagram">
<div class="fs-links">
  <div class="fs-links__row">
    <div class="fs-node is-accent"><b>Turbulence v</b><small>hidden, shared by all three</small></div>
    <div class="fs-links__to">
      <div class="fs-link"><em>drift and volatility</em><div class="fs-node"><b>Interest rate</b></div></div>
      <div class="fs-link"><em>drift and volatility</em><div class="fs-node"><b>Inflation</b></div></div>
      <div class="fs-link"><em>volatility</em><div class="fs-node"><b>Equity</b><small>optional</small></div></div>
    </div>
  </div>
  <div class="fs-links__row">
    <div class="fs-node"><b>Interest rate</b></div>
    <div class="fs-links__to">
      <div class="fs-link is-both"><em><i></i>last period's level</em><div class="fs-node"><b>Inflation</b></div></div>
      <div class="fs-link"><em>short rate plus premium</em><div class="fs-node"><b>Equity</b><small>optional</small></div></div>
    </div>
  </div>
</div>
</div>

Turbulence drives every leg and is never driven back. Plain KNW keeps only the two-way arrow between rate and inflation.

## KNW: Two-Way Coupling

Each leg is a regression on last period's level of both variables, a bivariate VAR(1) ([Lütkepohl, 2005](https://doi.org/10.1007/978-3-540-27752-1){:target="_blank"}):

$$
\begin{pmatrix} r_t \\ \pi_t \end{pmatrix}
= c + \Phi \begin{pmatrix} r_{t-1} \\ \pi_{t-1} \end{pmatrix} + \begin{pmatrix} \sigma_r\,\varepsilon^r_t \\ \sigma_\pi\,\varepsilon^\pi_t \end{pmatrix}
$$

$$r_t$$ is the nominal short rate and $$\pi_t$$ year-over-year CPI inflation. The diagonal of $$\Phi$$ is each variable's own persistence, the off-diagonal terms the cross-coupling: how much of the other variable's level spills over. $$c$$ holds two intercepts and $$\sigma$$ the size of each period's surprise.

<div class="fs-facts">
  <div><span>Variables</span><b>Nominal short rate and year-over-year CPI inflation</b></div>
  <div><span>Model</span><b>Bivariate VAR(1)</b></div>
  <div><span>Fit</span><b>Ordinary least squares, on deviations from the averages</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/reference/knw">Knw</a></div>
</div>

There is no long-run mean per leg. The pair settles jointly at $$(I - \Phi)^{-1}c$$, and the system must be stable: if a shock would never die out (the largest eigenvalue of $$\Phi$$ is 1 or more), the fit stops with an error. Both legs are fitted by ordinary least squares on the dates both series cover, on deviations from the history's averages ([Lütkepohl, 2005](https://doi.org/10.1007/978-3-540-27752-1){:target="_blank"}, section 3.3), so the pair settles at those averages. Fitting a free intercept per leg instead lets a pair this persistent amplify where the sample happens to start and end.

On 146 quarters of the US OECD short rate and CPI growth, 1990Q1 to 2026Q2 (calibrated on 2026-10-14):

| leg | intercept | own persistence | cross coupling | volatility |
|:----|----------:|----------------:|---------------:|-----------:|
| interest rate | -0.0005 | 0.9432 | 0.0803 | 0.0043 |
| inflation | 0.0037 | 0.8890 | -0.0206 | 0.0073 |

One percentage point more inflation adds 0.080 points to next quarter's rate, in line with central banks raising rates when inflation runs high, though a reduced-form regression cannot single out that channel. A higher rate nudges inflation down only slightly. How fast, and where, the pair settles:

<div class="ca-nums fs-nums">
  <span><b>8 quarters</b>half-life of a joint shock</span>
  <span><b>3.04%</b>long-run rate</span>
  <span><b>2.72%</b>long-run inflation</span>
  <span><b>0.3%</b>long-run real short rate</span>
</div>

That real rate is below the 1.0% in the Federal Reserve's longer-run projections (a 3.0% federal funds rate against 2.0% PCE inflation in the [September 2025 Summary of Economic Projections](https://www.federalreserve.gov/monetarypolicy/files/fomcprojtabl20250917.pdf){:target="_blank"}, Table 1), because the sample includes the zero-rate years 2009-2015 and 2020-2021, and with 36 years of data the long-run levels carry a sampling error of about 0.6 percentage points.

<div class="fs-callout" markdown="1">
A belief cannot override the long-run levels, since they are a joint property of both legs; the history window the pair is fitted on is the lever.
</div>

<div class="fs-ref"><a href="/projects/financescenarios/docs/reference/knw"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Knw</a></div>

## Stochastic Volatility

Markets alternate between calm and stressed spells; plain KNW gives every period the same randomness. The stochastic-volatility variant adds DNB's hidden variance factor $$v_t$$, the square of the volatility ([Commissie Parameters, 2022, Technical Appendix, section 1](https://open.overheid.nl/repository/ronl-f2685a42fd0bf01d5821446bcda34e719fdf7ef1/1/pdf/bijlage-2-technische-appendix.pdf#page=1){:target="_blank"}), a CIR process ([Cox, Ingersoll and Ross, 1985](https://doi.org/10.2307/1911242){:target="_blank"}) of the kind [Heston (1993)](https://doi.org/10.1093/rfs/6.2.327){:target="_blank"} uses for variance: mean-reverting and never negative.

<div class="fs-facts">
  <div><span>Turbulence</span><b>One hidden CIR variance factor, shared by every leg</b></div>
  <div><span>Estimated from</span><b>The past year's squared surprises</b></div>
  <div><span>Simulation</span><b>Andersen's Quadratic-Exponential scheme</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/reference/knw-sv">KnwSv</a></div>
</div>

$$
dv_t = a_v(\theta_v - v_t)\,dt + \sigma_v\sqrt{v_t}\,dW^v_t
$$

Each leg reads last period's $$v$$ twice, in its drift and in its variance:

$$
r_t = c_r + \lambda_r v_{t-1} + \phi_{rr} r_{t-1} + \phi_{r\pi}\pi_{t-1} + \sqrt{h_r + \eta_r v_{t-1}}\;\varepsilon^r_t
$$

with the same shape for inflation. $$\lambda$$ lets turbulence move the expected level, as in DNB's model, $$h$$ is the calm-state variance and $$\eta$$ how strongly variance rises with turbulence. Because one $$v$$ drives every leg, volatility in rates, inflation and equity rises and falls together: the clustering of stress across asset classes that a constant-volatility model misses.

**Estimating turbulence.** DNB recovers $$v$$ from market yields on each date. Finance Scenarios estimates it from the pair's own history: the average of plain KNW's squared surprises over the past year (four quarters, or twelve months), lagged one period, is the proxy for $$v$$. The one-year window follows [Engle's (1982)](https://doi.org/10.2307/1912773){:target="_blank"} four-quarter ARCH model of inflation variance. A CIR process is fitted to that proxy and both legs are refitted with it as an extra input; if neither leg's variance rises with $$v$$, the fit suggests plain KNW. Simulation uses [Andersen's (2008)](https://doi.org/10.21314/jcf.2008.189){:target="_blank"} Quadratic-Exponential scheme, which keeps $$v$$ non-negative with little bias; DNB's model uses Andersen's scheme too, with a martingale correction ([Commissie Parameters, 2022, Technical Appendix, section 9.1](https://open.overheid.nl/repository/ronl-f2685a42fd0bf01d5821446bcda34e719fdf7ef1/1/pdf/bijlage-2-technische-appendix.pdf#page=8){:target="_blank"}).

Turbulence is the variance of a quarter's combined rate and inflation surprise. On the same US quarterly data (calibrated on 2026-10-05):

<div class="ca-nums fs-nums">
  <span><b>1.7 years</b>half-life of turbulence</span>
  <span><b>0.3 pp</b>a quarter's surprise today</span>
  <span><b>0.8 pp</b>at the long-run level</span>
</div>

The pair starts calmer than usual. Inflation responds most: its standard deviation is 0.31% a quarter at $$v = 0$$ and 0.68% at the long-run level. The Feller condition $$2a_v\theta_v \ge \sigma_v^2$$ fails on this fit, so simulated turbulence touches zero more often than its long-run distribution suggests.

## The Equity Leg

An equity index on the same turbulence factor becomes volatile when rates and inflation do. Following DNB's equity row, each period's log return is the simulated short rate plus a constant risk premium, with variance linked to $$v$$:

$$
\ln\frac{S_t}{S_{t-1}} = r_{t-1}\,\Delta t + \mu - \tfrac{1}{2}h_{t-1} + \sqrt{h_{t-1}}\,\varepsilon^S_t, \qquad h_{t-1} = h_S + \eta_S v_{t-1}
$$

$$\Delta t$$ is the period length in years and $$\mu$$ the premium per period, corrected for volatility drag. Over the S&P 500's quarterly history since 1990 (calibrated on 2026-10-05):

<div class="ca-nums fs-nums">
  <span><b>1.59%</b>a quarter above the short rate, about 6.4% a year</span>
  <span><b>13%</b>yearly volatility with no turbulence</span>
  <span><b>15.3%</b>at the long-run level</span>
</div>

The equity leg runs under the real-world measure only.

<div class="fs-ref"><a href="/projects/financescenarios/docs/reference/knw-sv"><i class="fas fa-book" aria-hidden="true"></i>Full reference: KnwSv</a></div>

## The Risk-Neutral Version

A real-world run answers "where might rates go?"; valuing liabilities asks "what is a future cash flow worth today?". The bridge is the market price of risk, the extra return investors demand per unit of each risk. The risk-neutral version fits it so that the model's yields match the 13-week, 5, 10 and 30-year US Treasury yields over the historical sample. It changes only the drift, through five premiums: one on turbulence's mean-reversion speed, and a constant and a turbulence-proportional premium per leg. Premiums that depend on a constant and on $$v$$ only are the completely affine form of [Duffie and Kan (1996)](https://doi.org/10.1111/j.1467-9965.1996.tb00123.x){:target="_blank"}. DNB uses the richer essentially affine form of [Duffee (2002)](https://doi.org/10.1111/1540-6261.00426){:target="_blank"}, whose time-varying bond risk premia are what KNW (2010) is about ([Koijen, Nijman and Werker, 2010](https://doi.org/10.1093/rfs/hhp058){:target="_blank"}); its extra parameters are hard to pin down on a short quarterly sample and a nominal curve alone.

<div class="fs-facts">
  <div><span>Fitted to</span><b>13-week, 5, 10 and 30-year US Treasury yields</b></div>
  <div><span>Market price of risk</span><b>Five premiums, completely affine</b></div>
  <div><span>Bond prices</span><b>Closed form, at any whole number of periods</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/reference/knw-sv-q">KnwSvQ</a></div>
</div>

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

<div class="fs-callout fs-callout--limits" markdown="1">
<p class="fs-callout__title">Limits</p>

- The closed-form prices and the market price of risk include the correlation between rate and inflation shocks, estimated from the same changes as the run's correlation matrix, so model bond prices and simulated discount factors agree. Turbulence's own shock is independent of both.
- The inflation risk premium is weakly identified: the price of unexpected inflation risk cannot be identified from nominal yields alone ([Koijen, Nijman and Werker, 2010](https://doi.org/10.1093/rfs/hhp058){:target="_blank"}), so without a real (TIPS) curve or inflation swaps nothing separates real rates from the inflation premium. Judge the fit by how well it reprices nominal yields, not by the individual premiums.
</div>

### The Stochastic Deflator

A deflator values a liability straight off a real-world run, so you don't need a second, risk-neutral simulation. Following [Cheng and Planchet (2018)](https://hal.science/hal-01730072){:target="_blank"}, $$D(T)$$ combines discounting at the simulated short rate with a path weight that turns real-world paths into risk-neutral ones; the value of a cash flow $$X_T$$ is the path average of $$D(T)\,X_T$$.

The weight leaves out turbulence's shock, so the deflator is only accurate when the turbulence premium is small. On the live US fit that premium is large (38.5% of turbulence's speed), and the deflator's average misses the model's own bond prices by about 2% at one year and 5% at five (0.9827 against 0.9620, and 0.7606 against 0.7996); the fit warns when the premium is this large. The deflator is available in Python only; the [KnwSvQ reference](/projects/financescenarios/docs/reference/knw-sv-q) has a worked example.

<div class="fs-ref"><a href="/projects/financescenarios/docs/reference/knw-sv-q"><i class="fas fa-book" aria-hidden="true"></i>Full reference: KnwSvQ</a></div>

## Configuring a KNW Run

A KNW pair is a rate entry and an inflation entry that name each other and use the same method. The fitted coefficients are a recursion applied once per period, with no time step to rescale, so the simulation frequency must equal the fitting period (monthly, quarterly or yearly); the configuration rejects a mismatch.

The settings profile sets the step and the history the pair is fitted on:

```yaml
# my-project/settings/knw.yaml (a settings profile)
start_date: 2026-10-01
engine:
  frequency: quarterly          # must equal the pair's period
toolkit:
  start_date: 1990-01-01        # history used for the fit
```

The factor set holds the pair and the optional equity leg:

```yaml
# my-project/factor-sets/knw.yaml (a factor set)
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

With both files in place, one call loads them and simulates 30 years:

```python
from financescenarios import Scenarios, load_config

result = Scenarios.from_config(
    load_config("my-project/settings/knw.yaml", "my-project/factor-sets/knw.yaml")
).simulate(years=30)
```

<div class="fs-callout fs-callout--limits" markdown="1">
<p class="fs-callout__title">Limits</p>

- Beliefs, GARCH and business-cycle conditioning are not available: the long-run level is a joint property of both legs, so there is no single long-run mean to override.
- The equity leg needs a real-world rate.
</div>

## How It Compares with DNB's CP2022

The [CP2022 Technical Appendix](https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix){:target="_blank"} specifies DNB's full model. How the two compare:

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

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">10</span></summary>

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

</details>
