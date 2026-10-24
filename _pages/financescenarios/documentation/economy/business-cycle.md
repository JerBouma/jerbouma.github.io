---
title: Business Cycle
seo_title: "Business Cycle | Finance Scenarios"
seo_title_suffix: false
excerpt: "How Finance Scenarios gives a run an explicit business cycle: the OECD Composite Leading Indicator as a mean-reverting level whose changes can move the drift of rates, inflation, spreads and the chance of an equity crisis."
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
  <div><span>Model</span><b>Mean reversion around 100</b></div>
</div>

## The Leading Indicator

The indicator $$L_t$$ reverts to its long-run level as an Ornstein-Uhlenbeck process ([Vasicek, 1977, section 5](https://doi.org/10.1016/0304-405x(77)90016-2){:target="_blank"}):

$$
dL_t = a(\theta - L_t)\,dt + \sigma\,dW_t
$$

It is fitted like every other mean-reverting factor. A regression of each month's change on the level before it, $$L_t - L_{t-1} = c + b\,L_{t-1} + e_t$$, gives the speed $$a = -\ln(1 + b)/\Delta t$$ less the small-sample bias of [Tang and Chen (2009, Theorem 3.1.1)](https://doi.org/10.1016/j.jeconom.2008.11.001){:target="_blank"}, the level $$\theta = c/(-b)$$, and the volatility from the residuals. The run steps it with the exact transition. A quarterly or yearly run averages the monthly readings; GARCH volatility and beliefs are options. Switching it on takes one entry in a factor set:

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
leading_indicator:
  enabled: true
  country: United States
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

The example uses the run from the [overview](/projects/financescenarios/docs#simulating-scenarios): the default settings and factor set, calibrated on 19 October 2026, with 2,000 scenarios and seed 42. The default factor set simulates the OECD Composite Leading Indicator for the US as a mean-reverting level, with no factor conditioned on it. To read its fitted parameters and its range after five years:

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

Which gives a long-run level of 99.74, a speed of 0.35 a year and a yearly volatility of 1.34 points, starting from 101.0, and a 90% range of 97.4 to 102.5 after five years. When plotted:

{% include ft-chart.html id="economy-leading-indicator" src="/assets/data/financescenarios-guides/economy.json" label="Median, 25-75% and 5-95% band of the OECD composite leading indicator of the US over five years" %}

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">7</span></summary>

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. [casact.org](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}
- Diebold, F.X., Lee, J.-H., Weinbach, G.C. (1994). "Regime Switching with Time-Varying Transition Probabilities." In Hargreaves, C. (ed.), Nonstationary Time Series Analysis and Cointegration, 283-302. [doi.org](https://doi.org/10.1093/oso/9780198773917.003.0010){:target="_blank"}
- Filardo, A.J. (1994). "Business-Cycle Phases and Their Transitional Dynamics." Journal of Business & Economic Statistics, 12(3), 299-308. [doi.org](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}
- Frisch, R., Waugh, F.V. (1933). "Partial Time Regressions as Compared with Individual Trends." Econometrica, 1(4), 387-401. [doi.org](https://doi.org/10.2307/1907330){:target="_blank"}
- Lovell, M.C. (1963). "Seasonal Adjustment of Economic Time Series and Multiple Regression Analysis." Journal of the American Statistical Association, 58(304), 993-1010. [doi.org](https://doi.org/10.1080/01621459.1963.10480682){:target="_blank"}
- Tang, C.Y., Chen, S.X. (2009). "Parameter Estimation and Bias Correction for Diffusion Processes." Journal of Econometrics, 149(1), 65-81. [doi.org](https://doi.org/10.1016/j.jeconom.2008.11.001){:target="_blank"}
- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. [doi.org](https://doi.org/10.1016/0304-405x(77)90016-2){:target="_blank"}

</details>

{% include ft-charts-script.html %}
