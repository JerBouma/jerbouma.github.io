---
title: Beliefs
seo_title: "Beliefs | Finance Scenarios"
seo_title_suffix: false
excerpt: "How expert judgement enters a Finance Scenarios run: a belief replaces one fitted parameter, a path moves a long-run level over time, a shock moves the scenarios on a date, and an anchor ties long-run rates to EIOPA's or DNB's curves."
description: "Beliefs in Finance Scenarios: long-run levels, paths and shocks over the fit, anchors to EIOPA and DNB, a zero lower bound, GARCH volatility, business-cycle conditioning and correlations stated as values."
author_profile: false
permalink: /projects/financescenarios/docs/configuration/beliefs
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/configuration
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-configuration"
---

Every number in a run is fitted on history unless you say otherwise. A belief is how you say otherwise: it replaces one fitted parameter with your own value, moves a long-run level along a path, or shifts the scenarios on a date, and keeps the rest of the fit. Long-run rates can also be anchored to an official curve, rates can be held at or above zero, volatility can cluster, and correlations can be stated rather than estimated.

## A Belief over the Fit {#expert-judgement}

A fitted parameter is an estimate from one stretch of history; a long-run view is a judgement. The typical belief is the long-run level of rates or inflation: you set where it heads, and the data still sets how fast it gets there and how much it swings around it. Values are annualized decimals (0.035 is 3.5%, see [units](/projects/financescenarios/docs/units)). A fixed value, such as a long-run inflation rate of 3%, changes the calibration and needs `calibrate(config)` again; a path and a shock apply at simulation time, so they reuse a saved calibration.

## Paths

The long-run level can follow a path instead of one number: anchors at chosen years, $$\theta(t_1), \theta(t_2), \dots$$, joined by straight lines. Before the first anchor the level holds at its value, and after the last it holds there too, unless `converge_over_years` brings it back to the fitted level in a straight line over that many years. Because the factor still mean-reverts, it is pulled toward the moving level rather than set to it: a fast-reverting factor tracks the path closely, a slow one lags it ([Regimes](/projects/financescenarios/docs/regimes#beliefs-as-a-path) shows how to steer the level so the factor itself runs along a path). The default factor set's [policy-rule short rates](/projects/financescenarios/docs/interest-rates) and [expected-path long rates](/projects/financescenarios/docs/interest-rates/long-rate) take no single long-run level: on them a path prescribes the rate itself, and the neutral real rate or the term premium is the belief to set instead. On regime-switching inflation a path moves both regimes' levels by the same amount.

## Shocks

A factor can take a one-off shock in a given year, after which it moves on from the new level with its own dynamics. On the step $$k$$ nearest the year, after that step's own move, a shock of magnitude $$m$$ does one of three things, depending on its mode:

$$
x^{(i)}_k \leftarrow x^{(i)}_k + m \quad (\text{additive, the default}), \qquad x^{(i)}_k \leftarrow x^{(i)}_k + \big(m - \operatorname{median}_j x^{(j)}_k\big) \quad (\texttt{median}), \qquad x^{(i)}_k \leftarrow m \quad (\texttt{absolute})
$$

across the scenarios $$i$$: a fixed jump, a move of every scenario by one amount so their median lands on $$m$$, or every scenario set to $$m$$. For an equity, a currency or a commodity the shock is a log return: an additive one applies as $$S^{(i)}_k \leftarrow S^{(i)}_k\,e^{m}$$, and in `median` mode $$m$$ is the median's log return from the start; `absolute` does not apply to a price. With `steer_from`, a `median` or `absolute` shock walks the median in a straight line to $$m$$ from that year instead of landing in one step, and `relative: true` reads $$m$$ as a change from the starting median rather than a level ([Regimes](/projects/financescenarios/docs/regimes#beliefs-as-a-path)). That is how a stress narrative enters a real-world run; [regimes](/projects/financescenarios/docs/regimes) package such stories. A path and a shock together, in a factor set:

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
inflation:
  defaults:                 # every country's inflation; a regime can target one
    beliefs:
      long_run_mean:
        anchors:            # year: level, a straight line in between
          5.0: 0.06         # 6% from the start to year 5
          10.0: 0.02        # down to 2% by year 10
      shocks:
        - year: 2.0
          magnitude: 0.03   # +3 percentage points in year 2
```

<div class="fs-callout fs-callout--limits" markdown="1">
<p class="fs-callout__title">Limits</p>

- Beliefs don't apply to risk-neutral factors, which exist to match the market.
- A factor with GARCH volatility or conditioned on the business cycle ignores its fixed beliefs.
</div>

## Anchoring Long-Run Rate Levels {#anchoring-long-run-rate-levels}

Instead of your own view, the long-run level of a real-world Hull-White or CIR rate with constant volatility can follow an official path. Anchored to EIOPA, it follows the forward rates of EIOPA's risk-free curve for its currency (USD, EUR or GBP): at year $$t$$ the level is $$F(t, m)$$, the forward rate for $$m$$ years from year $$t$$, with $$m$$ = 1 for a short rate and 10 for a long one ([Other Rate Models](/projects/financescenarios/docs/interest-rates/other-models#hull-white-vasicek) gives the formula). EIOPA's curve follows market rates up to the last liquid point (the longest maturity with a deep and liquid market), 30 years for the dollar, 20 for the euro and 50 for sterling ([EIOPA's RFR technical documentation, EIOPA-BoS-25-599, section 9.2.2 and Tables 7-8](https://www.eiopa.europa.eu/document/download/f7fca58f-4d24-4441-ac60-de562bf26d77_en#page=44){:target="_blank"}), and converges to the [ultimate forward rate](https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en){:target="_blank"} beyond it. Over a few decades a short rate's anchor therefore follows market forwards, while a euro long rate's 10-year forward is extrapolated from year 10 on.

Anchored to DNB (euro only), the level follows the median of [De Nederlandsche Bank's](https://www.dnb.nl/voor-de-sector/open-boek-toezicht/sectoren/pensioenfondsen/){:target="_blank"} pension scenario set. With either anchor the speed and volatility stay fitted, and an explicit belief still takes precedence. The default factor set's rates follow the policy rule and the expected path, so they take no anchor. In a factor set of your own, for every rate:

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
interest_rates:
  defaults:
    long_run_anchor: eiopa   # or dnb, for euro rates
```

## Keeping Rates at or Above Zero {#keeping-rates-at-or-above-zero}

Gaussian rate models let rates go well below zero, and Hull-White rates have no floor by default, since negative rates did happen (a CIR rate's volatility shrinks to nothing at zero, which keeps it at or just above zero). A zero lower bound, or any floor, turns the model into a shadow rate $$s_t$$, an unobserved rate that follows the model without the floor, while the observed rate is $$\max(s_t, \text{floor})$$, so rates linger at the floor as policy rates did ([Other Rate Models](/projects/financescenarios/docs/interest-rates/other-models#hull-white-vasicek)). The default factor set's policy-rule short rates have each central bank's lowest rate as their floor ([Short Rate](/projects/financescenarios/docs/interest-rates#the-floor-and-the-shadow-rate)). A floor applies to real-world rates only.

## Volatility That Clusters and the Business Cycle {#business-cycle-conditioning}

By default a factor's volatility is constant and its drift ignores the business cycle. Two alternatives change that, though not both on one factor:

<div class="ca-cards">
  <div><i class="ca-icon fas fa-pulse" aria-hidden="true"></i><p class="ca-card-title">GARCH volatility</p><p>Volatility clusters, so calm periods stay calm and turbulent ones stay turbulent (<a href="https://doi.org/10.1016/0304-4076(86)90063-1" target="_blank">Bollerslev, 1986</a>; the recursion is on <a href="/projects/financescenarios/docs/interest-rates/other-models#hull-white-vasicek">Other Rate Models</a>).</p></div>
  <div><i class="ca-icon fas fa-gauge" aria-hidden="true"></i><p class="ca-card-title">The business cycle</p><p>A factor's drift follows the leading indicator's step-to-step change, so inflation or rates move with the business cycle (<a href="/projects/financescenarios/docs/economy/business-cycle#conditioning-on-the-cycle">conditioning on the cycle</a>).</p></div>
</div>

To switch on the cycle, or GARCH instead:

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
leading_indicator:
  enabled: true

inflation:
  defaults:
    condition_on_business_cycle: true   # or volatility_model: garch
```

## Correlations Stated as Values {#correlations-stated-as-values}

By default every pair of factors gets the correlation of its historical changes, shrunk toward zero ([Dependence](/projects/financescenarios/docs/dependence)). A factor set can state pairs instead, the way a published model does. The pairs it does not list keep their estimates (`unlisted: history`, the default) or are set to zero (`unlisted: zero`):

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
correlations:
  fixed:
    - factors: [united_states_short_rate, united_states_inflation]
      value: 0.5
  unlisted: history   # or zero: every pair not listed is uncorrelated
```

The stated pairs replace the estimates after the shrinkage, and the matrix is then repaired to the nearest valid correlation matrix ([Higham, 2002](https://doi.org/10.1093/imanum/22.3.329){:target="_blank"}), so a set of pairs that cannot hold together is moved as little as possible.

## Example

Because a path and a shock apply at simulation time, the example reuses the [overview's](/projects/financescenarios/docs#keeping-a-run) saved calibration. To hold US inflation's long-run level at 4% for two years and bring it down to 2% by year five, with a jump of two points in year one:

```python
from financescenarios import BeliefPath, CalibrationResult, OUBeliefs, Scenarios, Shock, compare_runs, load_profiles

config = load_profiles(settings_id="default", factor_set_id="default")
scenarios = Scenarios.from_config(config, api_key="FINANCIAL_MODELING_PREP_KEY")
calibration = CalibrationResult.load("calibration.json")

beliefs = OUBeliefs(
    long_run_mean=BeliefPath(anchors={2.0: 0.04, 5.0: 0.02}),
    shocks=[Shock(year=1.0, magnitude=0.02)],
)
us_inflation = config.inflation[0].model_copy(update={"beliefs": beliefs})
believed = config.model_copy(update={"inflation": [us_inflation, *config.inflation[1:]]})

result = scenarios.simulate(calibration=calibration, n_simulations=2000, seed=42)
with_belief = scenarios.simulate(believed, calibration=calibration, n_simulations=2000, seed=42)

with_belief.horizon_summary([1, 2, 3, 5], factors=["united_states_inflation"])
compare_runs(
    {"fitted": result, "belief": with_belief},
    statistic="terminal_median",
    factors=["united_states_inflation", "united_states_short_rate", "us_broad"],
)
```

Median US inflation is 5.50% after one year against 2.71% without the belief, 4.45% after two, 3.85% after three and 2.52% after five, against 1.81%. Every variable linked to inflation follows: the median short rate after five years is 6.06% against 4.39%, and US stocks return 7.94% a year against 8.73%. When plotted:

{% include ft-chart.html id="configuration-belief" src="/assets/data/financescenarios-guides/configuration.json" label="Median and 5-95% band of US inflation as fitted and with a belief path and a shock, over five years" %}

A [regime](/projects/financescenarios/docs/regimes) packages beliefs like these, together with the scenarios to keep, as a named story.

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">5</span></summary>

- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." Journal of Econometrics, 31(3), 307-327. [doi.org](https://doi.org/10.1016/0304-4076(86)90063-1){:target="_blank"}
- De Nederlandsche Bank. Pension funds: scenario sets. [dnb.nl](https://www.dnb.nl/voor-de-sector/open-boek-toezicht/sectoren/pensioenfondsen/){:target="_blank"}
- EIOPA (2025). Technical Documentation of the Methodology to Derive EIOPA's Risk-Free Interest Rate Term Structures (EIOPA-BoS-25-599). [eiopa.europa.eu](https://www.eiopa.europa.eu/document/download/f7fca58f-4d24-4441-ac60-de562bf26d77_en){:target="_blank"}
- EIOPA. Risk-free interest rate term structures. [eiopa.europa.eu](https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en){:target="_blank"}
- Higham, N.J. (2002). "Computing the Nearest Correlation Matrix: A Problem from Finance." IMA Journal of Numerical Analysis, 22(3), 329-343. [doi.org](https://doi.org/10.1093/imanum/22.3.329){:target="_blank"}

</details>

{% include ft-charts-script.html %}
