---
title: Mortality
seo_title: "Mortality | Finance Scenarios"
seo_title_suffix: false
excerpt: "How Finance Scenarios simulates longevity: the two-factor model of Cairns, Blake and Dowd on one-year death probabilities, with the level and the age slope as random walks with drift."
description: "Mortality in Finance Scenarios: the Cairns-Blake-Dowd model, its random walks with drift, Eurostat life tables or your own, and a fit on German population mortality."
author_profile: false
permalink: /projects/financescenarios/docs/economy/mortality
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/economy
redirect_from:
    - /projects/financescenarios/docs/reference/mortality
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-economy"
---

Longevity risk is the risk that people live longer than a pension fund or annuity provider expected. Mortality has fallen for decades, but not at a steady pace, and that uncertain trend is what this factor captures: every scenario gets its own path of death rates by age, correlated with rates, inflation and markets. The factor is opt-in.

<div class="fs-facts">
  <div><span>Series</span><b>One-year death probabilities by age</b></div>
  <div><span>Data</span><b>Eurostat, or your own life table</b></div>
  <div><span>Model</span><b>Cairns-Blake-Dowd, two factors</b></div>
</div>

## The Model

Finance Scenarios uses the two-factor model of [Cairns, Blake and Dowd (2006)](https://doi.org/10.1111/j.1539-6975.2006.00195.x){:target="_blank"}:

$$
\operatorname{logit} q(x, t) = \ln\frac{q(x, t)}{1 - q(x, t)} = \kappa_1(t) + \kappa_2(t)\,(x - \bar{x})
$$

Here $$q(x, t)$$ is the one-year probability of death at age $$x$$ in year $$t$$ and $$\bar{x}$$ the mean of the fitted ages. $$\kappa_1$$ is the level, which moves mortality at every age alike, and $$\kappa_2$$ the age slope: $$e^{\kappa_2}$$ is how much the odds of dying grow with each extra year of age. The logit keeps every probability between 0 and 1, and the straight line in age describes mortality well from about 60 upward, the ages that drive pension and annuity values.

Mortality improvement is a trend over decades rather than a level to return to, so each factor is a random walk with drift, as in [Cairns, Blake and Dowd (2006, p. 692, eq. 2)](https://doi.org/10.1111/j.1539-6975.2006.00195.x){:target="_blank"}:

$$
\kappa_i(t + 1) = \kappa_i(t) + \mu_i + \sigma_i\,z_i(t)
$$

A random walk's uncertainty grows with the horizon, so the range of death rates after 30 years is far wider than after five: the longevity risk a long-dated liability carries. In the paper the two shocks $$z_1$$ and $$z_2$$ are correlated; here each factor is fitted on its own, and their correlation, with each other and with everything else in the run, comes from the [correlation matrix](/projects/financescenarios/docs/dependence) of their yearly changes.

## The Fit

Each calendar year's death probabilities are regressed on age by ordinary least squares, $$\operatorname{logit} q(x, t) = \kappa_1(t) + \kappa_2(t)\,(x - \bar x) + e$$, as Cairns, Blake and Dowd do, which gives one value of each factor per year. The drift and volatility are then the mean and the standard deviation of the yearly changes, $$\mu_i = \overline{\Delta\kappa_i}$$ and $$\sigma_i = \operatorname{sd}(\Delta\kappa_i)$$, and the run starts from the last year's values. The factor runs in yearly steps only.

Life tables come from Eurostat's `demo_mlifetable` (from 1960 for most countries of the European Economic Area), or from your own table of one-year death probabilities ($$q_x$$, not central death rates), for example from the [Human Mortality Database](https://www.mortality.org/){:target="_blank"}. The fit uses every single age from 60 to 84 by default. Eurostat's tables end in an open 85-and-over group before 2014, so a higher top age keeps only recent years.

<div class="fs-callout fs-callout--limits" markdown="1">
<p class="fs-callout__title">Limits</p>

- No cohort effects and no Lee-Carter alternative.
- The straight-line shape holds only near the fitted ages; reading a death rate outside them warns.
</div>

## Example

The default factor set leaves mortality off, so this example calibrates a small yearly configuration of its own: the US short rate, inflation and unemployment, the S&P 500 and German mortality, fitted on history since 1985, calibrated on 24 October 2026 and run 30 years ahead. To switch mortality on and read the one-year death probability at 65 and 80 off the simulated factors:

```python
from datetime import date

from financescenarios import Scenarios, ScenariosConfig
from financescenarios.factors.mortality.mortality_model import cbd_mortality_rate

config = ScenariosConfig.model_validate({
    "start_date": date(2026, 1, 1),
    "engine": {"n_simulations": 2000, "n_steps": 30, "frequency": "yearly", "seed": 42},
    "toolkit": {"start_date": date(1985, 1, 1)},
    "interest_rates": [{"name": "us_short_rate", "country": "United States", "source": "oecd", "period": "yearly"}],
    "inflation": [{"name": "inflation", "country": "United States", "period": "yearly"}],
    "equities": [{"name": "us_stocks", "ticker": "^GSPC", "period": "yearly"}],
    "mortality": {"enabled": True, "source": "eurostat", "country": "Germany"},
})
scenarios = Scenarios.from_config(config, api_key="FINANCIAL_MODELING_PREP_KEY")
calibration = scenarios.calibrate(config)
result = scenarios.simulate(config, calibration=calibration)

calibration.calibrated_params["mortality_level"]
calibration.calibrated_params["mortality_slope"]

q_65 = cbd_mortality_rate(result.paths["mortality_level"], result.paths["mortality_slope"], age=65, mean_age=72.0)
q_80 = cbd_mortality_rate(result.paths["mortality_level"], result.paths["mortality_slope"], age=80, mean_age=72.0)
```

Which gives, on German population mortality from 1985 to 2024 at every age from 60 to 84 (a mean age of 72):

| Factor | Drift $$\mu$$ | Volatility $$\sigma$$ | Today |
|:--|--:|--:|--:|
| Level $$\kappa_1$$ | -0.0142 | 0.0361 | -3.8250 |
| Slope $$\kappa_2$$ | -0.0003 | 0.0010 | 0.0958 |

A drift of -0.014 in the level means the odds of dying fall about 1.4% a year at every age. A 65-year-old has a 1.10% chance of dying within the year today; in the median scenario that falls to 0.98% after ten years and 0.76% after thirty, with nine scenarios in ten between 0.55% and 1.06%. At 80 it falls from 4.48% to 3.84% and 2.81%, between 2.03% and 3.89% after thirty years. When plotted, one age per tab:

{% include ft-chart.html id="mortality-death-probability" src="/assets/data/financescenarios-guides/mortality.json" label="Median, 25-75% and 5-95% band of the one-year death probability in Germany at 65 and at 80 over thirty years" %}

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">2</span></summary>

- Cairns, A.J.G., Blake, D., Dowd, K. (2006). "A Two-Factor Model for Stochastic Mortality with Parameter Uncertainty: Theory and Calibration." Journal of Risk and Insurance, 73(4), 687-718. [doi.org](https://doi.org/10.1111/j.1539-6975.2006.00195.x){:target="_blank"}
- Human Mortality Database. [mortality.org](https://www.mortality.org/){:target="_blank"}

</details>

{% include ft-charts-script.html %}
