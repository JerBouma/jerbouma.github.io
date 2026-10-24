---
title: Yield Curve
seo_title: "Yield Curve | Finance Scenarios"
seo_title_suffix: false
excerpt: "How Finance Scenarios simulates a whole yield curve: the dynamic Nelson-Siegel model of Diebold and Li for real-world curves, and a two-factor Heath-Jarrow-Morton forward curve that is arbitrage-free by construction."
description: "The yield curve in Finance Scenarios: dynamic Nelson-Siegel level, slope and curvature, the bias-corrected speeds, the two-factor Gaussian HJM (G2++) forward curve, and the simulated curve of a run."
author_profile: false
permalink: /projects/financescenarios/docs/interest-rates/yield-curve
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/interest-rates
redirect_from:
    - /projects/financescenarios/docs/reference/term-structure
    - /projects/financescenarios/docs/reference/hjm
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-interest-rates"
---

The short and the long rate say where the curve starts and ends; bonds and liabilities sit at every maturity in between. Two models simulate the whole curve. The dynamic Nelson-Siegel model of [Diebold and Li (2006)](https://doi.org/10.1016/j.jeconom.2005.03.005){:target="_blank"}, in the default factor set, moves the curve the way history moved it. A two-factor Heath-Jarrow-Morton forward curve is arbitrage-free by construction, for valuation against today's curve.

<div class="fs-facts">
  <div><span>Series</span><b>The US Treasury curve, 3 months to 30 years</b></div>
  <div><span>Default model</span><b>Dynamic Nelson-Siegel: level, slope and curvature</b></div>
  <div><span>Alternative</span><b>Two-factor Gaussian HJM (G2++)</b></div>
</div>

## The Nelson-Siegel Curve

[Nelson and Siegel (1987)](https://doi.org/10.1086/296409){:target="_blank"} describe a whole curve with three numbers. The yield at maturity $$\tau$$ is

$$
y(\tau) = L + S\,B(\tau) + C\,\big(B(\tau) - e^{-\lambda\tau}\big), \qquad B(\tau) = \frac{1 - e^{-\lambda\tau}}{\lambda\tau}
$$

and the forward rate $$f(\tau) = L + S\,e^{-\lambda\tau} + C\,\lambda\tau\,e^{-\lambda\tau}$$. The level $$L$$ is the yield at the long end, the slope $$S$$ the short end less the long ($$y(0) = L + S$$, so an upward-sloping curve has a negative slope), and the curvature $$C$$ the hump, whose loading peaks where $$\lambda$$ puts it. Almost all of a government curve's day-to-day movement is a parallel shift, a change in steepness or a change in the hump, so three numbers move every maturity consistently: no scenario has a 9-year yield that jumps while the 10-year stands still.

The decay $$\lambda$$ is set, not fitted: 0.7308 a year, the 0.0609 a month of [Diebold and Li (2006, section 3.2)](https://doi.org/10.1016/j.jeconom.2005.03.005){:target="_blank"}, which puts the curvature's peak near 30 months. On each date the three factors are then the least-squares fit of the quoted yields on the loadings $$1$$, $$B(\tau)$$ and $$B(\tau) - e^{-\lambda\tau}$$ (section 3). The default reads the 13-week bill (^IRX) and the 5, 10 and 30-year Treasury yields (^FVX, ^TNX, ^TYX), each as a zero yield; the Treasury's par curve from 1 month to 30 years and the government curves of the euro area, Germany, the UK, Japan, Canada, Sweden and Norway can be read instead. A date missing a maturity is left out, and at least three maturities are needed.

## The Factors over Time

Each factor reverts to its own long-run level at its own speed, a mean-reverting (Ornstein-Uhlenbeck) process stepped with its exact transition:

$$
\beta_{t+\Delta t} = \theta + (\beta_t - \theta)\,e^{-a\Delta t} + \sigma\sqrt{\frac{1 - e^{-2a\Delta t}}{2a}}\;z_t
$$

for $$\beta$$ the level, slope or curvature. The speed $$a$$, level $$\theta$$ and volatility $$\sigma$$ come from a regression of each day's change on the previous day's value, with the speed's small-sample bias taken off ([Tang and Chen, 2009, Theorem 3.1.1](https://doi.org/10.1016/j.jeconom.2008.11.001){:target="_blank"}; see [Commodities](/projects/financescenarios/docs/markets/commodities#correcting-the-speed-for-a-short-sample)). On daily data since 2000 the slope is the slowest, with a half-life of about seven years, against three and a half for the level and just over one for the curvature:

| Factor | Today | Long-run level $$\theta$$ | Speed $$a$$, per year | Volatility $$\sigma$$ |
|:--|--:|--:|--:|--:|
| Level $$L$$ | 5.52% | 4.03% | 0.20 | 0.88% |
| Slope $$S$$ | -1.49% | -2.12% | 0.10 | 1.20% |
| Curvature $$C$$ | -1.04% | -3.41% | 0.58 | 3.04% |

So the scenarios show long swings in how high and how steep the curve is, with a hump that comes and goes within a year or two, and the curve drifts back toward its usual upward slope. The shocks are normally distributed, so yields can go negative and the curve can invert, as both have done in history.

The three factors link to the rest of the run only through the correlation matrix. No equation ties the curve's short end to the [policy-rule short rate](/projects/financescenarios/docs/interest-rates) or its 10-year yield to the [long rate](/projects/financescenarios/docs/interest-rates/long-rate): the curve reverts to its averages since 2000, the rates to today's neutral rates and term premia, and the two can drift apart. Nothing guarantees the curve is free of arbitrage between maturities either. It is a real-world description of how the curve moves; for prices that must be consistent across maturities, use the HJM curve below.

## The HJM Forward Curve

The real-world rate models here set their drift, the direction rates tend to move, separately from their volatility. In the framework of [Heath, Jarrow and Morton (1992)](https://doi.org/10.2307/2951677){:target="_blank"} the drift of the forward curve follows from its volatility, so once the volatility is chosen, no riskless arbitrage between maturities is possible and the drift is never fitted. Finance Scenarios uses two factors whose volatility fades with the time to maturity $$x$$, $$\sigma_i(x) = \sigma_i e^{-\kappa_i x}$$: the two-factor Gaussian model of [Hull and White (1994)](https://doi.org/10.3905/jod.1994.407908){:target="_blank"}, G2++ in [Brigo and Mercurio (2006, chapter 4)](https://doi.org/10.1007/978-3-540-34604-3){:target="_blank"}. Its two states start at zero and revert to zero,

$$
dx_i = (\sigma_i\lambda_i - \kappa_i x_i)\,dt + \sigma_i\,dW_i, \qquad dW_1\,dW_2 = \rho\,dt
$$

with $$\lambda_i$$ a market price of risk, zero by default, and rebuild the forward rate for borrowing $$x$$ years after date $$t$$:

$$
f(t, t + x) = f_0(t + x) + e^{-\kappa_1 x}\,x_1(t) + e^{-\kappa_2 x}\,x_2(t) + \Phi(t, x)
$$

Here $$f_0$$ is today's forward curve, a Nelson-Siegel fit to today's four Treasury yields, and $$\Phi$$ the convexity term the no-arbitrage condition supplies:

$$
\Phi(t, x) = \sum_{i, j} \rho_{ij}\,\frac{\sigma_i\sigma_j}{\kappa_j}\Big(K(\kappa_i) - K(\kappa_i + \kappa_j)\Big), \qquad K(k) = e^{-kx}\,\frac{1 - e^{-kt}}{k}, \quad \rho_{ii} = 1, \ \rho_{12} = \rho
$$

Both states and $$\Phi$$ start at zero, so the model starts exactly on today's curve, and with no market price of risk it is risk neutral: it holds no term premium.

The volatilities are fitted to how history's forward curves moved. Each date's Treasury yields get a Nelson-Siegel fit, whose forward rates are read at 12 maturities from 3 months to 30 years, and their changes give a covariance matrix $$\Sigma$$. For given speeds the two volatilities and $$\rho$$ follow from $$\Sigma$$ in closed form; the speeds are searched on a grid of 80 by 80 with $$\kappa_2 > 1.2\,\kappa_1$$, between 0.01 and 6 a year, then refined by least squares on the relative distance between the model's covariance and $$\Sigma$$. A fit that leaves more than 35% of that distance, or a speed at a bound, raises a warning.

<div class="fs-callout fs-callout--limits" markdown="1">
<p class="fs-callout__title">Limits</p>

- The two factors' shocks over a step are drawn with the correlation that gives the states the fitted $$\rho$$, from the exact covariance of the G2++ states ([Brigo and Mercurio, 2006, section 4.2](https://doi.org/10.1007/978-3-540-34604-3){:target="_blank"}), so the simulated states and the convexity term $$\Phi$$ share one $$\rho$$; when the run's correlation matrix is repaired that pair is held and the others move around it. A belief on `factor_correlation` changes both.
- The factors are Gaussian, so forward rates can go negative.
- The slow first factor settles only over decades, so the spread of long rates keeps widening for a long time: suited to valuation, less so to a long real-world projection.
- It is switched off in the shipped factor sets (`hjm.enabled`).
</div>

## Example

The example uses the run from the [overview](/projects/financescenarios/docs#simulating-scenarios): the default settings and factor set, calibrated on 19 October 2026, with 2,000 scenarios and seed 42. The simulated level, slope and curvature give the yield at any maturity in every scenario and month. To read the curve from 3 months to 30 years:

```python
from financescenarios import Scenarios
from financescenarios.factors.term_structure.term_structure_model import nelson_siegel_yield

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
result = scenarios.simulate(n_simulations=2000, seed=42)

decay = scenarios.config.yield_curve.decay
curve = {
    tenor: nelson_siegel_yield(
        result.paths["rate_level"], result.paths["rate_slope"], result.paths["rate_curvature"],
        tenor=tenor, decay=decay,
    )
    for tenor in [0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30]
}
```

Which gives today's curve rising from 4.08% at 3 months to 5.18% at 10 years and 5.41% at 30 years. The median scenario's curve comes down and steepens: after five years it runs from 2.74% at 3 months to 3.95% at 10 years and 4.38% at 30 years, as the level reverts to its average since 2000. When plotted, the median curve today, after one year and after five years:

{% include ft-chart.html id="yield-curve-median" src="/assets/data/financescenarios-guides/yield-curve.json" label="Median simulated Treasury curve from 3 months to 30 years, today, after one year and after five years" %}

The spread across scenarios is wide at every maturity: after five years nine scenarios in ten have a 10-year yield between 1.95% and 5.95%, and in a quarter of them (25.5%) it is below the 3-month yield, an inverted curve. When plotted, the curve after five years:

{% include ft-chart.html id="yield-curve-five-years" src="/assets/data/financescenarios-guides/yield-curve.json" label="Median, 25-75% and 5-95% band of the simulated Treasury curve from 3 months to 30 years after five years" %}

To simulate the HJM curve instead, switch it on in a factor set of your own:

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
hjm:
  enabled: true
```

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">6</span></summary>

- Brigo, D., Mercurio, F. (2006). Interest Rate Models: Theory and Practice (2nd ed.). Springer Finance. [doi.org](https://doi.org/10.1007/978-3-540-34604-3){:target="_blank"}
- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. [doi.org](https://doi.org/10.1016/j.jeconom.2005.03.005){:target="_blank"}
- Heath, D., Jarrow, R., Morton, A. (1992). "Bond Pricing and the Term Structure of Interest Rates: A New Methodology for Contingent Claims Valuation." Econometrica, 60(1), 77-105. [doi.org](https://doi.org/10.2307/2951677){:target="_blank"}
- Hull, J., White, A. (1994). "Numerical Procedures for Implementing Term Structure Models II: Two-Factor Models." The Journal of Derivatives, 2(2), 37-48. [doi.org](https://doi.org/10.3905/jod.1994.407908){:target="_blank"}
- Nelson, C.R., Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." The Journal of Business, 60(4), 473-489. [doi.org](https://doi.org/10.1086/296409){:target="_blank"}
- Tang, C.Y., Chen, S.X. (2009). "Parameter Estimation and Bias Correction for Diffusion Processes." Journal of Econometrics, 149(1), 65-81. [doi.org](https://doi.org/10.1016/j.jeconom.2008.11.001){:target="_blank"}

</details>

{% include ft-charts-script.html %}
