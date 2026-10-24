---
title: Other Rate Models
seo_title: "Other Rate Models | Finance Scenarios"
seo_title_suffix: false
excerpt: "The other short-rate models of Finance Scenarios: Hull-White (Vasicek), Cox-Ingersoll-Ross, Wilkie's consols yield and the two-factor model of Hibbert, Mowbray and Turnbull, with their equations, fits and a run of each."
description: "Hull-White, CIR, Wilkie consols and the Hibbert two-factor model in Finance Scenarios: the equations, the exact and full-truncation steps, the risk-neutral Hull-White fit to EIOPA's curve, and the zero lower bound."
author_profile: false
permalink: /projects/financescenarios/docs/interest-rates/other-models
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/interest-rates
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-interest-rates"
---

The default short rate follows a [policy rule](/projects/financescenarios/docs/interest-rates) and the default long rate is its [expected path plus a term premium](/projects/financescenarios/docs/interest-rates/long-rate). Each rate entry of a factor set can take another model instead: one that reverts to a single level, one that keeps rates positive, Wilkie's consols yield, or Hibbert's two-factor model, in which the short rate chases a slower-moving target. The joint models of rates and inflation have pages of their own: [KNW](/projects/financescenarios/docs/interest-rates/knw) and [CP2022](/projects/financescenarios/docs/interest-rates/cp2022).

## Hull-White (Vasicek)

The general-purpose model reverts to one long-run level $$\theta$$ at speed $$a$$ with a constant volatility $$\sigma$$ ([Vasicek, 1977, section 5](https://doi.org/10.1016/0304-405x(77)90016-2){:target="_blank"}; [Hull and White, 1990](https://doi.org/10.1093/rfs/3.4.573){:target="_blank"}):

$$
dr_t = a(\theta - r_t)\,dt + \sigma\,dW_t, \qquad r_{t+\Delta t} = \theta + (r_t - \theta)\,e^{-a\Delta t} + \sigma\sqrt{\frac{1 - e^{-2a\Delta t}}{2a}}\;z_t
$$

The second form is the exact transition the run steps with. The fit regresses each change on the level before it, $$\Delta r_t = c + b\,r_{t-1} + e_t$$, which gives $$a = -\ln(1 + b)/\Delta t$$ less the small-sample bias of [Tang and Chen (2009, Theorem 3.1.1)](https://doi.org/10.1016/j.jeconom.2008.11.001){:target="_blank"}, $$\theta = c/(-b)$$, and $$\sigma$$ from the residuals at the corrected speed. The history it is fitted on is a market rate (the 13-week bill by default), an OECD rate or the Global Macro Database, and can reach back further: OECD rates since 1950, Bank Rate since 1694 or the Jordà-Schularick-Taylor panel since 1870 (see [Configuration](/projects/financescenarios/docs/configuration#long-history)).

Three options change the model:

- **A floor.** A zero lower bound, or any floor, turns the rate into a shadow rate $$s_t$$ that follows the model unfloored, with the observed rate $$r_t = \max(s_t, \text{floor})$$, the idea of [Black (1995)](https://doi.org/10.1111/j.1540-6261.1995.tb05182.x){:target="_blank"}. Rates then linger at the floor as policy rates did. CIR rates can take a floor too.
- **An anchor.** The long-run level can follow the risk-free forward rates of EIOPA, the EU's insurance supervisor, for the currency (USD, EUR or GBP) instead of one number, $$\theta(t) = F(t, m)$$, the forward rate for $$m$$ years from year $$t$$ ($$m$$ = 1 for a short rate, 10 for a long one), with $$F(t, m) = \exp\{(\ln P(t) - \ln P(t + m))/m\} - 1$$ read off EIOPA's discount factors $$P$$. DNB's median path is the alternative for the euro ([Beliefs](/projects/financescenarios/docs/configuration/beliefs#anchoring-long-run-rate-levels)).
- **GARCH volatility.** The variance $$h_t$$ follows last period's surprise and its own past, so calm and turbulent spells cluster: $$h_{t+1} = \omega + \alpha\,\varepsilon_t^2 + \beta\,h_t$$ ([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1){:target="_blank"}), fitted by Gaussian quasi-maximum likelihood with $$\alpha + \beta < 1$$. The drift is then an Euler step, $$r_{t+\Delta t} = r_t + a(\theta - r_t)\Delta t + \sqrt{h_t\,\Delta t}\;z_t$$, fitted without the bias correction. The run must step at the fit's own frequency, and beliefs, the long history, the anchor and the policy rule are not available.

## Risk-Neutral Hull-White

To value a cash flow at today's market prices, the short rate must reproduce today's curve on average. The risk-neutral rate is the Hull-White process shifted onto the curve ([Brigo and Mercurio, 2006, section 3.3](https://doi.org/10.1007/978-3-540-34604-3){:target="_blank"}):

$$
r_t = x_t + \alpha(t), \qquad dx_t = -a\,x_t\,dt + \sigma\,dW_t, \quad x_0 = 0, \qquad \alpha(t) = f^M(0, t) + \frac{\sigma^2}{2a^2}\big(1 - e^{-at}\big)^2
$$

with $$f^M(0, t)$$ today's instantaneous forward curve. Each step moves the rate exactly around that center, $$r_{t+\Delta t} = \alpha(t + \Delta t) + (r_t - \alpha(t))\,e^{-a\Delta t} + \sigma\sqrt{(1 - e^{-2a\Delta t})/2a}\;z_t$$, so the average discount factor returns today's bond prices. The curve is EIOPA's risk-free curve for the dollar, the euro and the pound, read as zero rates $$s_i$$ with piecewise-flat forwards $$f_i = (T_i z_i - T_{i-1} z_{i-1})/(T_i - T_{i-1})$$, $$z_i = \ln(1 + s_i)$$, so its prices are reproduced at EIOPA's maturities. For other currencies the curve is a Nelson-Siegel fit to today's Treasury yields.

Without swaption prices, the volatility comes from history. The speed $$a$$ is the short rate's own; a Hull-White rate moves an $$n$$-year yield by $$\sigma\,g(n)$$ with $$g(n) = (1 - e^{-an})/(an)$$, so $$\sigma$$ is set to match the volatilities $$\hat v_i$$ of the 13-week, 5, 10 and 30-year Treasury yields' monthly changes, in relative terms:

$$
\sigma^* = \arg\min_\sigma \sum_i \left(\frac{\sigma\,g(n_i) - \hat v_i}{\hat v_i}\right)^2 = \frac{\sum_i g(n_i)/\hat v_i}{\sum_i \big(g(n_i)/\hat v_i\big)^2}
$$

This is the short rate a risk-neutral run (`simulate(measure="risk_neutral")`) uses, and [Market Consistency](/projects/financescenarios/docs/solvency) runs it.

## Cox-Ingersoll-Ross

In the model of [Cox, Ingersoll and Ross (1985)](https://doi.org/10.2307/1911242){:target="_blank"} the shocks scale with the square root of the rate, so they calm down near zero:

$$
dr_t = a(\theta - r_t)\,dt + \sigma\sqrt{r_t}\,dW_t
$$

In continuous time the rate stays positive when the Feller condition $$2a\theta \ge \sigma^2$$ holds; the fit warns when it does not. The speed and level come from the same regression as Hull-White's, and the volatility from the residuals scaled by the square root of the rate, $$\sigma = \operatorname{sd}\big(e_t/\sqrt{r_{t-1}}\big)/\sqrt{\Delta t}$$, the square-root case of [Chan, Karolyi, Longstaff and Sanders (1992)](https://doi.org/10.1111/j.1540-6261.1992.tb04011.x){:target="_blank"}. The run steps with the full-truncation scheme of [Lord, Koekkoek and van Dijk (2010)](https://doi.org/10.1080/14697680802392496){:target="_blank"},

$$
r^+_t = \max(r_t, 0), \qquad r_{t+\Delta t} = r_t + a(\theta - r^+_t)\,\Delta t + \sigma\sqrt{r^+_t\,\Delta t}\;z_t
$$

which floors the rate inside the drift and the volatility but not the rate itself, so a path can dip slightly below zero even when the Feller condition holds. The `goes` factor set holds one CIR process per Treasury maturity, set to the bands of the generator prescribed by the NAIC, the US National Association of Insurance Commissioners ([Benchmarks](/projects/financescenarios/docs/validation/benchmarks#goes-acceptance-criteria)).

## Wilkie's Consols Yield

[Wilkie (1986, sections 3.12-3.15)](https://doi.org/10.1017/S0071368600009009){:target="_blank"} writes the long yield, the yield on consols (undated UK government bonds), as a part that follows inflation plus a real part:

$$
C_t = W\cdot M_t + N_t, \qquad M_t = d\,I_t + (1 - d)\,M_{t-1}, \qquad \ln N_t = \ln\mu_N + \phi\,(\ln N_{t-1} - \ln\mu_N) + \sigma_N\,z_t
$$

$$M_t$$, an exponentially weighted average of inflation $$I_t$$, stands for the expected inflation the market prices, and $$N_t$$ is the real part, positive by construction. The weights follow Wilkie's Reduced Standard Basis (section 3.15): $$W = 1$$ and $$d = 1 - (1 - 0.05)^{\Delta t}$$. The real part's $$\mu_N$$, $$\phi$$ and $$\sigma_N$$ come from a regression of $$\ln N_t$$ on its value a step earlier, which needs $$C_t - W M_t > 0$$ at every observation: long yields above expected inflation throughout the fit. On US data, that holds only for a fit that ends before 2008. Wilkie's minimum yield of 0.5% can be switched on.

## Hibbert's Two-Factor Model

In [Hibbert, Mowbray and Turnbull (2001, section 5.1.1, p. 15)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf#page=15){:target="_blank"} the short rate reverts not to a fixed level but to a target that itself moves:

$$
dr_t = a\,(m_t - r_t)\,dt + \sigma\,dW_t
$$

By default the target $$m_t$$ is an observed long rate (^TNX, or an OECD long rate), simulated as a mean-reverting (Ornstein-Uhlenbeck) factor of its own; an exponentially weighted average of the rate's own path, $$m_t = 0.05\,r_t + 0.95\,m_{t-1}$$, is the alternative. The short rate's pull toward the target, the fast leg, is fitted by a regression through the origin of each change on the gap to the target, $$\Delta r_t = k\,(m_{t-1} - r_{t-1}) + e_t$$, with $$a = k/\Delta t$$, and simulated with an Euler step. The paper applies the structure to the real rate and adds inflation; a rate entry can do the same (`real_rate: true`), and the `hibbert` and `ahlgrim` factor sets run it that way.

## Example

The `hibbert`, `ahlgrim` and `wilkie` factor sets run their papers' models with the papers' own parameters and read no data, so they need no calibration and no API key ([Published Models](/projects/financescenarios/docs/validation/published-models)). The `hibbert` set holds Hibbert's two-factor real rate plus inflation, `ahlgrim` Ahlgrim, D'Arcy and Gorvett's version of it with a floor at zero, and `wilkie` Wilkie's consols yield. Each starts on its paper's date and runs its paper's horizon: Hibbert's from 2001 for 30 years in monthly steps, Ahlgrim's from 2004 for 50 years in monthly steps and Wilkie's from 1986 for 100 years in yearly steps. To run all three and read the rates off after 1, 10 and 30 years:

```python
from financescenarios import Scenarios

runs = {
    name: Scenarios.from_profiles(settings=name, factor_set=name).simulate(seed=42)
    for name in ("hibbert", "ahlgrim", "wilkie")
}

runs["hibbert"].horizon_summary([1, 10, 30], factors=["short_rate"])
runs["ahlgrim"].horizon_summary([1, 10, 30], factors=["interest_rate"])
runs["wilkie"].horizon_summary([1, 10, 30], factors=["consols_rate"])
```

Which gives, among other columns:

| factor | horizon | q0.05 | q0.5 | q0.95 |
|:-------|--------:|------:|-----:|------:|
| short_rate (Hibbert) | 1 | 0.0338 | 0.0502 | 0.0668 |
| short_rate (Hibbert) | 10 | -0.0031 | 0.0493 | 0.1021 |
| short_rate (Hibbert) | 30 | -0.0182 | 0.0499 | 0.1254 |
| interest_rate (Ahlgrim) | 1 | 0.0000 | 0.0280 | 0.0836 |
| interest_rate (Ahlgrim) | 10 | 0.0000 | 0.0670 | 0.1553 |
| interest_rate (Ahlgrim) | 30 | 0.0000 | 0.0762 | 0.1713 |
| consols_rate (Wilkie) | 1 | 0.0758 | 0.0856 | 0.0965 |
| consols_rate (Wilkie) | 10 | 0.0568 | 0.0858 | 0.1217 |
| consols_rate (Wilkie) | 30 | 0.0497 | 0.0850 | 0.1260 |

Hibbert's rate stays centered on its 5% start, 2.5% real plus 2.5% inflation, while its band widens for decades as the slow target wanders; after 30 years one scenario in ten is below zero. Ahlgrim's starts at the 1% of the paper's workbook, climbs toward the model's 7.6% (2.8% real plus 4.8% inflation) and never goes below its floor. Wilkie's consols yield holds near 8.5%, the real part's 3.5% on top of expected inflation of 5%. When plotted, one model per tab:

{% include ft-chart.html id="other-models-rates" src="/assets/data/financescenarios-guides/published-models.json" label="Median, 25-75% and 5-95% band of the nominal short rate in Hibbert, Mowbray and Turnbull's and in Ahlgrim, D'Arcy and Gorvett's model, and of Wilkie's consols yield" %}

A model of your own picks the method on a rate entry:

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
interest_rates:
  - name: us_short_rate
    country: United States
    currency: USD
    method: cir            # or hull_white, wilkie_consols, hibbert_two_factor
    zero_lower_bound: true
```

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">11</span></summary>

- Black, F. (1995). "Interest Rates as Options." The Journal of Finance, 50(5), 1371-1376. [doi.org](https://doi.org/10.1111/j.1540-6261.1995.tb05182.x){:target="_blank"}
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." Journal of Econometrics, 31(3), 307-327. [doi.org](https://doi.org/10.1016/0304-4076(86)90063-1){:target="_blank"}
- Brigo, D., Mercurio, F. (2006). Interest Rate Models: Theory and Practice (2nd ed.). Springer Finance. [doi.org](https://doi.org/10.1007/978-3-540-34604-3){:target="_blank"}
- Chan, K.C., Karolyi, G.A., Longstaff, F.A., Sanders, A.B. (1992). "An Empirical Comparison of Alternative Models of the Short-Term Interest Rate." The Journal of Finance, 47(3), 1209-1227. [doi.org](https://doi.org/10.1111/j.1540-6261.1992.tb04011.x){:target="_blank"}
- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). [A Theory of the Term Structure of Interest Rates](https://doi.org/10.2307/1911242){:target="_blank"}. Econometrica, 53(2), 385-407.
- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert Limited. [ressources-actuarielles.net](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"}
- Hull, J., White, A. (1990). "Pricing Interest-Rate-Derivative Securities." The Review of Financial Studies, 3(4), 573-592. [doi.org](https://doi.org/10.1093/rfs/3.4.573){:target="_blank"}
- Lord, R., Koekkoek, R., van Dijk, D. (2010). "A Comparison of Biased Simulation Schemes for Stochastic Volatility Models." Quantitative Finance, 10(2), 177-194. [doi.org](https://doi.org/10.1080/14697680802392496){:target="_blank"}
- Tang, C.Y., Chen, S.X. (2009). "Parameter Estimation and Bias Correction for Diffusion Processes." Journal of Econometrics, 149(1), 65-81. [doi.org](https://doi.org/10.1016/j.jeconom.2008.11.001){:target="_blank"}
- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. [doi.org](https://doi.org/10.1016/0304-405x(77)90016-2){:target="_blank"}
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. [doi.org](https://doi.org/10.1017/S0071368600009009){:target="_blank"}

</details>

{% include ft-charts-script.html %}
