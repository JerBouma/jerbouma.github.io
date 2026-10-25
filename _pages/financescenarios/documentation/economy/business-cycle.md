---
title: Business Cycle
seo_title: "Business Cycle | Finance Scenarios"
seo_title_suffix: false
excerpt: "How Finance Scenarios gives a run an explicit business cycle: the OECD Composite Leading Indicator as a stochastic cycle around 100 whose changes can move the drift of rates, inflation, spreads and the chance of an equity crisis."
description: "The business cycle in Finance Scenarios: the OECD leading indicator, conditioning a factor's drift on the cycle, unemployment's cycle links fitted in one regression, and the leading indicator in a run."
author_profile: false
permalink: /projects/financescenarios/docs/economy/business-cycle
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/economy
redirect_from:
    - /projects/financescenarios/docs/reference/leading-indicator
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-economy"
---

Average correlations say that spreads widen when stocks fall, but not that both happen because the economy turned. The leading indicator gives the model an explicit business cycle: a simulated booms-and-slowdowns variable that other factors can follow, so a downturn moves rates, spreads and equities on the same path. It is the OECD Composite Leading Indicator, designed to turn ahead of the economy and published detrended, around 100, for about 22 countries and groups. This page covers the indicator's model and the ways other factors can follow it.

<div class="fs-facts">
  <div><span>Series</span><b>OECD Composite Leading Indicator</b></div>
  <div><span>Coverage</span><b>About 22 countries and groups</b></div>
  <div><span>Model</span><b>A stochastic cycle around 100</b></div>
</div>

## The Leading Indicator

The OECD builds the indicator as a band-pass filtered cycle: its filter keeps swings of 12 to 120 months ([OECD, 2012, p. 7](https://www.oecd.org/content/dam/oecd/en/data/methods/OECD-System-of-Composite-Leading-Indicators.pdf){:target="_blank"}). So the indicator does not just drift back to 100, it overshoots: the US indicator since 1955 is correlated 0.98 with itself a month later, 0.06 a year later, -0.33 two years later and -0.18 three years later. A mean-reverting (Ornstein-Uhlenbeck) process only decays toward its level, so it keeps 0.82 a year later and 0.67 two years later. The indicator $$L_t$$ is therefore the first-order stochastic cycle of [Harvey, Trimbur and van Dijk (2005, section 2.1, eq. 3)](https://repub.eur.nl/pub/6913){:target="_blank"}, published in the Journal of Econometrics in 2007: a damped wave around its long-run level $$\theta$$ whose amplitude and timing are hit by shocks,

$$
\begin{pmatrix} \psi_t \\ \psi^*_t \end{pmatrix} = e^{-a\Delta t} \begin{pmatrix} \cos\lambda & \sin\lambda \\ -\sin\lambda & \cos\lambda \end{pmatrix} \begin{pmatrix} \psi_{t-\Delta t} \\ \psi^*_{t-\Delta t} \end{pmatrix} + \begin{pmatrix} \kappa_t \\ \kappa^*_t \end{pmatrix}, \qquad \psi_t = L_t - \theta, \quad \lambda = \frac{2\pi\Delta t}{P}
$$

with $$a$$ the speed at which the wave dies out, $$P$$ its period in years, $$\psi^*_t$$ a partner that carries the wave's phase and $$\kappa_t$$, $$\kappa^*_t$$ independent shocks of equal variance. Its autocorrelation $$\tau$$ years apart follows from that equation:

$$
\text{corr}(L_t, L_{t+\tau}) = e^{-a\tau}\cos(2\pi\tau/P)
$$

Readings less than a year apart share the OECD filter's 12-month window, so their month-to-month moves are mostly the filter's. The speed and the period therefore solve the autocorrelations one and two years apart, which gives the same cycle on monthly and quarterly readings: on the US history since 1955 a speed of 0.54 and 0.53 a year with a period of 4.3 years, reproducing the 0.06 and -0.33. The level $$\theta$$ is the history's mean, and the volatility $$\sigma$$ sets the long-run spread $$\sigma/\sqrt{2a}$$. The run steps the cycle with one shock a step through the innovations form of the Kalman filter ([Durbin and Koopman, 2012, section 4.3](https://doi.org/10.1093/acprof:oso/9780199641178.001.0001){:target="_blank"}): each reading is drawn given every earlier one, the partner follows from it, and every scenario starts where the filter puts the indicator in its cycle, rising or falling. Beliefs are an option; `method: ou` keeps the mean-reverting process, which can also take GARCH volatility. Switching it on takes one entry in a factor set:

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
leading_indicator:
  enabled: true
  country: United States
  method: stochastic_cycle   # ou: the mean-reverting process
```

## Conditioning on the Cycle

A factor can follow the cycle: with `condition_on_business_cycle`, the indicator's change over each step enters the factor's drift:

$$
dX_t = a(\theta - X_t)\,dt + \beta\,dL_t + \sigma\,dW_t
$$

Here $$X_t$$ is the factor's level: a Hull-White interest rate, inflation, house-price growth, and the level, not the log, of a credit spread, a commodity price or a dividend yield. $$\beta$$ comes from the same regression as the rest of the fit, $$X_t - X_{t-1} = c + b\,X_{t-1} + \beta\,(L_t - L_{t-1}) + e_t$$, the form of the inflation term of [Ahlgrim, D'Arcy and Gorvett (2005, eq. 3.21)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}; for a year-over-year rate read a year apart, the yearly slope is converted to the step. Its sign comes from the data: a spread that widened when the indicator fell gets a negative $$\beta$$, so a simulated downturn widens it on the same path. The indicator is simulated first in each step, and its change is added to the step in full, not decayed by the mean reversion. With the indicator in the regression the speed gets no bias correction, GARCH volatility cannot be combined with it, and beliefs do not apply. A CIR rate refuses it, since its fit has no covariate term.

## Unemployment's Cycle Links

Unemployment modeled without regimes, as for the euro area, can also react to a stock-market fall, a flat yield curve or the indicator itself. Those links are fitted in one regression together with the pull back to the calm level and the Phillips-curve term, not in two steps on the residuals of a first fit: a second-step regression on residuals gives the right slope only when the link is uncorrelated with the first step's regressors, which the Frisch-Waugh-Lovell theorem makes precise ([Frisch and Waugh, 1933](https://doi.org/10.2307/1907330){:target="_blank"}; [Lovell, 1963](https://doi.org/10.1080/01621459.1963.10480682){:target="_blank"}).

## Equity Crises That Follow the Cycle

An equity market's chance of switching between its calm and turbulent regimes can follow the indicator's level instead of inflation. These are the time-varying transition probabilities of [Filardo (1994)](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}, fitted together with the regimes by the expectation-maximization algorithm of [Diebold, Lee and Weinbach (1994)](https://doi.org/10.1093/oso/9780198773917.003.0010){:target="_blank"} (see [Equities](/projects/financescenarios/docs/markets#turbulence-is-likelier-when-inflation-is-high) for the logit). On SPY since 2005, a calm month turns turbulent with a chance of 5.4% at an indicator of 105 and 27.7% at 95. A two-step fit, which first labels each month by its likelier regime and then fits a logit, gives 5.8% and 8.8%: labeling throws away how unsure each month's regime is, and flattens the link.

<div class="fs-callout" markdown="1">
The default factor set leaves these links off. It ties its rates, unemployment and equities together through the balanced-approach policy rule, the equity link of unemployment and inflation-driven equity switching instead.
</div>

## Example

The example uses the run from the [overview](/projects/financescenarios/docs#simulating-scenarios): the default settings and factor set, calibrated on 25 October 2026, with 2,000 scenarios and seed 42. The default factor set simulates the OECD Composite Leading Indicator for the US as a stochastic cycle, with no factor conditioned on it. To read its fitted parameters and its range after five years:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
calibration = scenarios.calibrate()
result = scenarios.simulate(calibration=calibration, n_simulations=2000, seed=42)

calibration.calibrated_params["leading_indicator"]
result.horizon_summary([5], factors=["leading_indicator"])
```

Which gives a long-run level of 99.77, a speed of 0.67 a year, a period of 4.25 years and a volatility of 1.58 points a year (a long-run spread of 1.36 points), starting from 101.0, and a 90% range of 97.4 to 102.0 after five years. When plotted:

{% include ft-chart.html id="economy-leading-indicator" src="/assets/data/financescenarios-guides/economy.json" label="Median, 25-75% and 5-95% band of the OECD composite leading indicator of the US over five years" %}

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">8</span></summary>

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. [casact.org](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}
- Diebold, F.X., Lee, J.-H., Weinbach, G.C. (1994). "Regime Switching with Time-Varying Transition Probabilities." In Hargreaves, C. (ed.), Nonstationary Time Series Analysis and Cointegration, 283-302. [doi.org](https://doi.org/10.1093/oso/9780198773917.003.0010){:target="_blank"}
- Durbin, J., Koopman, S.J. (2012). Time Series Analysis by State Space Methods (2nd ed.). Oxford University Press. [doi.org](https://doi.org/10.1093/acprof:oso/9780199641178.001.0001){:target="_blank"}
- Filardo, A.J. (1994). "Business-Cycle Phases and Their Transitional Dynamics." Journal of Business & Economic Statistics, 12(3), 299-308. [doi.org](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}
- Frisch, R., Waugh, F.V. (1933). "Partial Time Regressions as Compared with Individual Trends." Econometrica, 1(4), 387-401. [doi.org](https://doi.org/10.2307/1907330){:target="_blank"}
- Harvey, A.C., Trimbur, T.M., van Dijk, H.K. (2005). "Trends and Cycles in Economic Time Series: A Bayesian Approach." Econometric Institute Report EI 2005-27; published in the Journal of Econometrics, 140(2), 618-649 (2007). [repub.eur.nl](https://repub.eur.nl/pub/6913){:target="_blank"}
- Lovell, M.C. (1963). "Seasonal Adjustment of Economic Time Series and Multiple Regression Analysis." Journal of the American Statistical Association, 58(304), 993-1010. [doi.org](https://doi.org/10.1080/01621459.1963.10480682){:target="_blank"}
- OECD (2012). "OECD System of Composite Leading Indicators." [oecd.org](https://www.oecd.org/content/dam/oecd/en/data/methods/OECD-System-of-Composite-Leading-Indicators.pdf){:target="_blank"}

</details>

{% include ft-charts-script.html %}
