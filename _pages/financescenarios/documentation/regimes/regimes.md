---
title: Regimes
seo_title: "Regimes | Finance Scenarios"
seo_title_suffix: false
excerpt: "How a stress story enters Finance Scenarios: beliefs change an assumption before simulating, targets keep the scenarios that fit the story afterwards, and forty regimes ship ready to run."
description: "Regimes in Finance Scenarios: beliefs and targets, steering a long-run level along a path, median shocks after Boyle, Broadie and Glasserman, how targets rank and keep scenarios, and runs of shipped regimes."
author_profile: false
permalink: /projects/financescenarios/docs/regimes
classes: wide-sidebar
layout: single
redirect_from:
    - /projects/financescenarios/regimes-notebook
    - /projects/financescenarios/docs/reference/regimes
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-regimes"
---

A regime is a named stress story, such as an oil crisis, a financial crisis or a regulator's adverse scenario, written down once and reused across runs. It has two levers: **beliefs** change an assumption before simulating ("inflation heads to 12% within a year"), and **targets** keep the scenarios that fit the story afterwards ("the weakest 30% for stocks"). Because targets are quantiles of what the model itself produces, the scenarios kept stay ones the model finds plausible, and a run under a regime still returns as many scenarios as asked for. A regime values nothing itself: it produces the scenarios your own valuation, ALM or capital model runs on.

## Two Ways to Tell a Story

<div class="ca-cards">
  <div><i class="ca-icon fas fa-sliders-h" aria-hidden="true"></i><p class="ca-card-title">Beliefs: change the economics before simulating</p><p>A belief overrides a calibrated parameter: the long-run level a rate or inflation reverts to, the speed of that reversion, the volatility, an equity's bull and bear means and volatilities, or a one-off shock at a given year. Every scenario is then simulated under the new assumption, with its own randomness and the calibrated correlations intact.</p></div>
  <div><i class="ca-icon fas fa-shuffle" aria-hidden="true"></i><p class="ca-card-title">Targets: condition on the outcome after simulating</p><p>A target keeps only the scenarios that land in a quantile range of one or more factors, such as the top 30% of short rates and the bottom 30% of equity returns. The model is unchanged: you look at the part of the baseline distribution where the story happens, and every other factor comes along on those same paths.</p></div>
</div>

This is the difference between a stress test (an imposed shock) and scenario analysis (a combination of internally consistent moves): beliefs reshape the distribution, targets select from it. Side by side:

| | Beliefs | Targets |
|:--|:--|:--|
| Acts on | the model's parameters | the simulated paths |
| Probability of the story | assumed (you impose it) | inside the base run (you pick its tail) |
| Other factors | move through the correlations | come along on the selected paths |
| Best for | a view on levels, a regulator's path, a shock | "what else happens when X happens" |

## Shipped Regimes

Forty regimes ship with the package: historical episodes such as Black Monday, the 2008 crisis and the 2022 inflation surge, the stress tests of the Federal Reserve, the European Systemic Risk Board (ESRB) and the Bank of England ([Stress Tests](/projects/financescenarios/docs/regimes/stress-tests)), and stylized stories. Twelve of the stylized ones:

| Regime | The story | How |
|:-------|:----------|:----|
| `financial_crisis` | The weakest 20% of stock returns, then the highest 20% of unemployment among those, then the lowest 30% of short rates among those | Targets |
| `credit_crunch` | Bank stocks collapse and the market follows (needs the `broad` set) | Both |
| `oil_crisis` | US inflation climbs to 12% within a year and eases to 5.5% by year three, as after the 1973 embargo, then back to 2.5% by year eight, with high rates and weak stocks | Both |
| `oil_shock` | A one-off three-point jump in US inflation in year two, then business as usual | Beliefs |
| `soft_landing` | Inflation's long-run level at 2% throughout, so inflation eases toward it at its own speed | Beliefs |
| `rate_cut_cycle` | Soft landing, then inflation drifts to 2.5% by year ten and back to its usual level; rates keep their own calibration, so the cuts are not imposed (add a rate belief for that) | Beliefs |
| `yield_curve_inversion` | The curve inverts within six months, short yields about one and a half points above the ten-year, then slowly rights itself | Both |
| `real_estate_crash` | House-price growth falls to -8% within a year and recovers over four, then the worst housing scenarios are kept | Both |
| `currency_crisis` | The Indian rupee devalues about 17% a year against the dollar, as in 2011-13 (needs `broad`) | Both |
| `tech_selloff` | The weakest quarter of tech stock returns (needs `broad`) | Both |
| `commodity_supercycle` | A long oil boom: crude oil earns a top-quarter return | Targets |
| `climate_collapse` | A rough stand-in for a climate shock: the highest US inflation with the weakest US stocks | Targets |

`list_presets(kind="regimes")` lists them all and `search_regimes` finds them from a few words. To list them and search for high inflation:

```python
from financescenarios import list_presets, search_regimes

list_presets(kind="regimes")

search_regimes("high inflation")
```

The search returns the best matches first:

| id | name | category | description |
|:---|:-----|:---------|:------------|
| persistent_inflation | Persistent High Inflation | inflation | US inflation settles near 6.6% for the whole run instead … |
| oil_crisis | Oil Crisis | inflation | US inflation climbs to 12% within a year and eases to 5.5% b… |
| stagflation_1970s | 1970s Stagflation | inflation | Inflation near 9% and unemployment averaging 7.3% for … |
| volcker_shock | Volcker Shock | rates | Short rates replay 1979-82's climb to 16% while inflation … |
| inflation_shock_2022 | 2022 Inflation and Rate Hikes | inflation | Inflation climbs to 9% and falls back to 3% within a year, … |

## Beliefs as a Path

A long-run level can follow a term structure instead of a single number: anchors at chosen horizons, interpolated in between. Before the first anchor the level holds at that anchor's value; after the last it holds there too, unless a chosen period fades it back to the calibrated level. On a policy-rule or expected-path rate the path prescribes the rate itself, and on regime-switching inflation it moves both regimes' levels. Which factors accept beliefs is set out under [Beliefs](/projects/financescenarios/docs/configuration/beliefs).

Because the factor still mean-reverts, it is pulled toward the moving level rather than set to it: a fast-reverting factor tracks the path closely, a slow one lags it, and a level path alone reaches its number late or not at all. On the default calibration, a long-run level of 12% took US inflation only to 8.2% after a year. A regime that names a number therefore does two things.

First, it steers the long-run level so that the factor's expected path runs in a straight line to each number. With $$m_t$$ the expected path, $$b$$ its slope per year, $$\Delta t$$ the step and $$a$$ the factor's speed of reversion, the level held over each step is

$$
\theta_t = m_t + \frac{b\,\Delta t}{1 - e^{-a\,\Delta t}}
$$

which inverts the exact step $$m_{t+\Delta t} = \theta_t + (m_t - \theta_t)\,e^{-a\Delta t}$$ for $$m_{t+\Delta t} = m_t + b\,\Delta t$$.

Second, it moves the scenarios' median to the number on the date it names, with a shock in `median` mode. Every scenario shifts by the same amount, the gap between the number and the median on that date, so the number holds whatever the calibrated speed, while each scenario keeps its distance from it and the spread stays as the model drew it. This is the first-moment matching of [Boyle, Broadie and Glasserman (1997, section 2.4)](https://doi.org/10.1016/S0165-1889(97)00028-6){:target="_blank"}, with the median in place of the mean so that a skewed factor's middle scenario is the one on the number. Between those dates each scenario moves with its own randomness.

A shock in `absolute` mode sets every scenario to the number instead, which closes the spread on that date. The supervisors' published paths use it, as each is a single deterministic scenario, and so does `shock_regime` for a factor it cannot steer, such as the default factor set's policy-rule rates; for a mean-reverting factor it steers the level and adds no shock.

Oil Crisis uses both steps, and targets as well. Its path follows US CPI inflation after the 1973 embargo, which peaked at 12.2% in November 1974 and was 5.5% by October 1976; 2.5% by year eight is a return to normal, a little above the 2.3% ten-year CPI forecast of the Philadelphia Fed's Survey of Professional Forecasters (Q3 2026). The anchors are the long-run levels that steer the expected path, worked out for inflation's speed of reversion on the 19 October 2026 calibration:

```yaml
# my-project/regimes/oil_crisis.yaml (a stress regime)
name: Oil Crisis
beliefs:
  inflation.united_states_inflation:
    long_run_mean:   # year: the level that steers the expected path along straight legs
      anchors: {0.0: 0.1667, 0.9167: 0.24, 1.0: 0.0685, 2.9167: 0.0062, 3.0: 0.0455, 7.9167: 0.016, 8.0: 0.025}
    shocks:          # the median at 12% after a year and 5.5% after three
      - {year: 1.0, magnitude: 0.12, mode: median}
      - {year: 3.0, magnitude: 0.055, mode: median}
targets:
  united_states_short_rate: [0.7, 1.0]   # top 30% by average short rate
  us_broad: [0.0, 0.3]                   # bottom 30% by equity return
```

Because the targets select scenarios after the shocks, the median of the scenarios a regime keeps can sit away from its number: the high-rate, weak-stock scenarios Oil Crisis keeps have a median US inflation of 12.98% after a year and 7.42% after three. Real Estate Crash moves the median of house-price growth to -8% after a year the same way, and Yield Curve Inversion moves the median of the curve's slope to its path at each of its two quarters. Regimes that set only a level, such as Persistent Inflation, Soft Landing and Goldilocks, describe where a factor settles rather than when it gets there, and leave the pace to the calibration.

Rates in a regime are annualized decimals (0.12 is 12% a year; see [units](/projects/financescenarios/docs/units)). A belief or target naming a factor that is not in the run is refused, so a regime written for one factor set fails loudly on another. A regime can also extend another and state only what differs, as Rate Cut Cycle does with Soft Landing.

<div class="fs-callout" markdown="1">
Check a factor's calibrated level before choosing anchors.
</div>

## How Targets Rank Scenarios

Each target ranks every scenario by one statistic over a window (the whole horizon by default): a price (equity, FX, commodity, index) by its annualized log return from the window's first date to its last, $$\ln(S_{\text{end}}/S_{\text{start}})/(t_{\text{end}} - t_{\text{start}})$$, and anything else, such as rates and inflation, by its average over the window. The window is shared by every target of a regime. Start-to-end is deliberate: a return annualized over a single month swings so widely that averaging the return since the start over every date would in effect rank the first few months.

Two targets can combine in two ways:

<div class="ca-cards">
  <div><i class="ca-icon fas fa-arrow-right" aria-hidden="true"></i><p class="ca-card-title">In sequence (the default)</p><p>Each target applies to what the previous one left, so a top-30% rate filter followed by a bottom-30% equity filter keeps about 9% of the run.</p></div>
  <div><i class="ca-icon fas fa-layer-group" aria-hidden="true"></i><p class="ca-card-title">Joint</p><p>Ranks each target against the full run and keeps the overlap, so the share kept depends on how the factors co-move and can be much smaller.</p></div>
</div>

## Running a Regime {#driving-a-regime-from-the-library}

A regime is passed to `simulate` by its name, or as an object. To run the baseline and Oil Crisis side by side:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(settings="default", factor_set="default")
baseline = scenarios.simulate(n_simulations=2000)
oil_crisis = scenarios.simulate(regime="oil_crisis", n_simulations=2000)
```

A one-variable question, such as "what if inflation hit 8% within a year?", does not need a regime file: `shock_regime` builds one from the variable, the level and the timing, as the [Short Rate](/projects/financescenarios/docs/interest-rates#an-inflation-shock) page shows. `load_regime` returns a shipped regime as an object to inspect or change, `RegimeLibrary` holds your own, and `stress_test_regime` builds a regime from a regulator's published scenario of another year.

A targeted regime keeps only part of each draw, about 9% for Oil Crisis, so the run draws batches until 2,000 scenarios fit (24,000 draws in three batches on the 19 October 2026 calibration). The stressed percentiles then rest on as many scenarios as the baseline's. Each batch ranks its own draws, so "the worst 30%" means the worst 30% of a batch, not of all draws pooled: each batch's cutoff carries its own sampling noise, most in the first batch, so the stressed quantiles are close to, not exactly, those of one large ranked run.

## Reading a Stressed Run

A stressed run is read against the baseline, factor by factor on the same scale, as `compare_runs` does in the examples below. Four points to keep in mind:

- **Belief-driven runs are conditional, not likely.** The percentiles describe uncertainty given the story, not the probability of the story. Don't read a stressed 99.5% quantile as a capital number.
- **Targets select by rank, not by level.** Sequential targets keep a fixed share (30% of 30% is 9%) whatever the correlations, so the share says nothing about how likely the story is. In joint mode the share kept is the model's own estimate of how often the combination occurs; if it is tiny, the story is far in the tail of the calibration. When a run is filtered directly (`filter`, `filter_narrative`), fewer than 30 scenarios left raises a warning, because their percentiles are noise; a regime run draws until it has as many as asked for.
- **The other factors are the point.** The factors the regime did not touch move through the calibrated correlations (beliefs) or as they did on the selected paths (targets). That is where a narrative test adds information over a single-factor shock.
- **Recovery is an assumption.** After a stress-test path ends, factors fade back to calibration over a chosen period; a longer period means a more persistent stress.

## Examples

Every run below uses the calibration of the [overview](/projects/financescenarios/docs#simulating-scenarios): the default settings and factor set, calibrated on 19 October 2026, with 2,000 scenarios and seed 42.

### Beliefs Only: A Soft Landing

Soft Landing sets US inflation's long-run level to 2%, so inflation eases toward 2% at its own calibrated speed, and filters nothing out. To run it next to the baseline and compare the averages after five years:

```python
from financescenarios import Scenarios, compare_runs

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
result = scenarios.simulate(n_simulations=2000, seed=42)
soft_landing = scenarios.simulate(regime="soft_landing", n_simulations=2000, seed=42)

compare_runs(
    {"baseline": result, "soft_landing": soft_landing},
    factors=["united_states_inflation", "united_states_short_rate", "us_broad"],
)
```

Which returns:

| factor | baseline | soft_landing |
|:-------|---------:|-------------:|
| united_states_inflation | 0.0234 | 0.0205 |
| united_states_short_rate | 0.0459 | 0.0428 |
| us_broad | 0.0849 | 0.0854 |

Inflation averages 2.05% after five years instead of 2.34%, and the short rate follows it down through the policy rule, from 4.59% to 4.28%. A belief moves the center of the range rather than its width. When plotted:

{% include ft-chart.html id="regimes-soft-landing" src="/assets/data/financescenarios-guides/regimes.json" label="Median and 5-95% band of US inflation in the baseline and under Soft Landing over five years" %}

### Targets Only: A Financial Crisis

Financial Crisis changes no assumption. It keeps the 20% of scenarios with the weakest US stocks, then the 20% of those with the highest US unemployment, then the 30% of those with the lowest short rate: 1.2% of each batch, so the run draws as many as it takes for 2,000 to fit. To run it:

```python
financial_crisis = scenarios.simulate(regime="financial_crisis", n_simulations=2000, seed=42)

compare_runs(
    {"baseline": result, "financial_crisis": financial_crisis},
    factors=["us_broad", "united_states_unemployment", "united_states_short_rate", "united_states_inflation"],
)
```

Which returns:

| factor | baseline | financial_crisis |
|:-------|---------:|-----------------:|
| us_broad | 0.0849 | -0.0394 |
| united_states_unemployment | 0.0553 | 0.0830 |
| united_states_short_rate | 0.0459 | 0.0020 |
| united_states_inflation | 0.0234 | 0.0168 |

US stocks lose 3.94% a year instead of gaining 8.49%, unemployment averages 8.30% instead of 5.53% and the short rate is cut to 0.20%, while inflation, which no target names, comes out lower as well, at 1.68%: the kept scenarios carry the model's links between factors with them. When plotted, one variable per tab:

{% include ft-chart.html id="regimes-financial-crisis" src="/assets/data/financescenarios-guides/regimes.json" label="Median and 5-95% band of the US stock market return, US unemployment and the US short rate in the baseline and under Financial Crisis over five years" %}

### Both at Once: Oil Crisis

Oil Crisis uses both levers: it moves the median of US inflation to 12% after a year and 5.5% after three, as after the 1973 embargo, then back toward 2.5% by year eight, and keeps the scenarios with high short rates and weak stocks. Two simpler inflation stories run beside it: Oil Shock, a belief that adds a one-off jump of three points to US inflation in year two, and Climate Collapse, a target that keeps the scenarios with the highest inflation and the weakest stocks. To run all three:

```python
runs = {"baseline": result}
for regime in ("oil_shock", "oil_crisis", "climate_collapse"):
    runs[regime] = scenarios.simulate(regime=regime, n_simulations=2000, seed=42)

compare_runs(runs, factors=["united_states_inflation", "united_states_short_rate", "us_broad"])
```

Which returns:

| factor | baseline | oil_shock | oil_crisis | climate_collapse |
|:-------|---------:|----------:|-----------:|-----------------:|
| united_states_inflation | 0.0234 | 0.0279 | 0.0592 | 0.0475 |
| united_states_short_rate | 0.0459 | 0.0570 | 0.1153 | 0.0671 |
| us_broad | 0.0849 | 0.0798 | -0.0126 | -0.0341 |

Oil Crisis puts the median of US inflation at 12% after one year and 5.5% after three, but the scenarios it then keeps, those with high short rates and weak stocks, run hotter: a median of 12.98% after one year and 7.42% after three, and an average of 5.92% after five years. The short rate answers through the policy rule, to a median of 8.33% after one year and 14.18% after three and an average of 11.53% after five, and US stocks lose 1.26% a year. When plotted, US inflation in the four runs:

{% include ft-chart.html id="regimes-inflation" src="/assets/data/financescenarios-guides/regimes.json" label="Median and 5-95% band of US inflation in the baseline and under Oil Shock, Oil Crisis and Climate Collapse over five years" %}

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and source cited on this page</b> <span class="ft-details__meta">1</span></summary>

- Boyle, P., Broadie, M., Glasserman, P. (1997). "Monte Carlo Methods for Security Pricing." Journal of Economic Dynamics and Control, 21(8-9), 1267-1321. [doi.org](https://doi.org/10.1016/S0165-1889(97)00028-6){:target="_blank"}

</details>

{% include ft-charts-script.html %}
