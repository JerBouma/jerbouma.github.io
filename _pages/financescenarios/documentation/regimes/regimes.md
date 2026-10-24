---
title: Regimes
seo_title: "Regimes | Finance Scenarios"
seo_title_suffix: false
excerpt: "How a stress story enters Finance Scenarios: beliefs change an assumption before simulating, targets keep the scenarios that fit the story afterwards, and 39 regimes ship ready to run."
description: "Regimes in Finance Scenarios: beliefs and targets, steered paths after Brigo and Mercurio and Boyle, Broadie and Glasserman, how a crash reaches other markets after Kupiec, how targets rank and keep scenarios, and runs of shipped regimes."
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

Thirty-nine regimes ship with the package: historical episodes such as Black Monday, the 2008 crisis and the 2022 inflation surge, the stress tests of the Federal Reserve, the European Systemic Risk Board (ESRB) and the Bank of England ([Stress Tests](/projects/financescenarios/docs/regimes/stress-tests)), and stylized stories. Twelve of them:

| Regime | The story | How |
|:-------|:----------|:----|
| `financial_crisis` | 2007-09 replayed: stocks everywhere down more than half in seventeen months, unemployment to 10%, the bill at zero for seven years, house prices falling 7% a year | Beliefs |
| `credit_crunch` | Bank stocks collapse and the market follows (needs the `broad` set) | Both |
| `oil_crisis` | The 1973 embargo replayed: inflation to 12% in a year and 5.5% by year three, the bill to 9% and back, unemployment to 9%, US stocks down 43% and the world's markets following | Beliefs |
| `oil_shock` | A rise of about three points in US inflation over the half year to year two, then business as usual | Beliefs |
| `soft_landing` | Inflation's median eases to 2% by year five and stays there | Beliefs |
| `rate_cut_cycle` | Short rates cut 5 points over two and a half years, the median of the Fed's six easing cycles from 1984 to 2020, then the policy rule again | Beliefs |
| `yield_curve_inversion` | The curve inverts within six months, short yields about one and a half points above the ten-year, then slowly rights itself | Beliefs |
| `real_estate_crash` | House-price growth falls to -8% within a year and back to zero over the four years after | Beliefs |
| `currency_crisis` | The Indian rupee devalues about 17% a year against the dollar for two and a third years, as in 2011-13 (needs `broad`) | Beliefs |
| `tech_selloff` | Tech stocks fall about a fifth in a year while the wider market holds up (needs `broad`) | Beliefs |
| `commodity_supercycle` | Oil rises sevenfold over six and a half years, as Brent did from 2002 to its 2008 record | Beliefs |
| `ai_tech_boom` | The scenarios where US stocks gain the most over two years, the top 9% where 2023-24's 53% rise sits | Targets |

`list_presets(kind="regimes")` lists them all and `search_regimes` finds them from a few words. To list them and search for high inflation:

```python
from financescenarios import list_presets, search_regimes

list_presets(kind="regimes")

search_regimes("high inflation")
```

The search returns the best matches first:

| id | name | category | description |
|:---|:-----|:---------|:------------|
| persistent_inflation | Persistent High Inflation | inflation | US inflation climbs towards 6.6% and stays high instead of r… |
| oil_crisis | Oil Crisis | inflation | US inflation climbs to 12% within a year and eases to 5.5% b… |
| stagflation_1970s | 1970s Stagflation | inflation | Inflation climbs towards 9% and unemployment towards 7.3% wh… |
| volcker_shock | Volcker Shock | rates | Short rates replay 1979-82's climb to 16% while inflation ri… |
| inflation_shock_2022 | 2022 Inflation and Rate Hikes | inflation | Inflation climbs to 9% and falls back to 3% within a year, s… |

## Beliefs as a Path

A long-run level can follow a term structure instead of a single number: anchors at chosen horizons, interpolated in between. Before the first anchor the level holds at that anchor's value; after the last it holds there too, unless a chosen period fades it back to the calibrated level. On a policy-rule or expected-path rate the path prescribes the rate itself, and on regime-switching inflation it moves both regimes' levels. Which factors accept beliefs is set out under [Beliefs](/projects/financescenarios/docs/configuration/beliefs).

Because the factor still mean-reverts, it is pulled toward the moving level rather than set to it: a fast-reverting factor tracks the path closely, a slow one lags it, and a level path alone reaches its number late or not at all. On the default calibration, a long-run level of 12% took US inflation only to 8.2% after a year. A regime that names a number therefore does two things.

First, it moves the scenarios' median to the number on the date it names, with a shock in `median` mode. Every scenario shifts by the same amount, the gap between the number and the median on that date, so the number holds whatever the calibrated speed, while each scenario keeps its distance from it and the spread stays as the model drew it. This is the first-moment matching of [Boyle, Broadie and Glasserman (1997, section 2.4)](https://doi.org/10.1016/S0165-1889(97)00028-6){:target="_blank"}, with the median in place of the mean so that a skewed factor's middle scenario is the one on the number.

Second, it walks there instead of landing in one month (`steer_from`). A level reached in one step is a cliff that history does not show: US unemployment's largest one-month rise outside 2020 is 1.3 points, and no shipped regime moves a median further in one month than its own series has. From the year a leg starts, every scenario moves by one amount each month, the gap between a straight line to the number and the scenarios' median, so the median follows the line and lands on the number on its date. Adding the same function of time to every scenario is the deterministic shift of [Brigo and Mercurio (2001, section 2, eq. 3)](https://doi.org/10.1007/pl00013541){:target="_blank"}; on a mean-reverting factor it is the moving long-run level whose expected path $$m_t$$ is the line. With $$b$$ the line's slope per year, $$\Delta t$$ the step and $$a$$ the factor's speed of reversion, the level held over each step is

$$
\theta_t = m_t + \frac{b\,\Delta t}{1 - e^{-a\,\Delta t}}
$$

which inverts the exact step $$m_{t+\Delta t} = \theta_t + (m_t - \theta_t)\,e^{-a\Delta t}$$ for $$m_{t+\Delta t} = m_t + b\,\Delta t$$. Each scenario keeps its own distance from the median, so the spread stays as the model drew it, and after the last leg the factor follows its own dynamics again.

A shock in `absolute` mode sets every scenario to the number instead, which closes the spread on that date. The supervisors' published paths use it, as each is a single deterministic scenario, with the median walking in a straight line between two published values. `shock_regime` steers the long-run level of a mean-reverting factor as above and adds no shock; for a factor it cannot steer, such as the default factor set's policy-rule rates, it walks the median to the level and back.

Oil Crisis walks inflation's median along the 1973 embargo's path: 12% at year one (US CPI inflation peaked at 12.2% in November 1974) and 5.5% at year three (October 1976), every scenario keeping its distance from the median, then 2.5% by year eight, a return to normal a little above the 2.3% ten-year CPI forecast of the Philadelphia Fed's Survey of Professional Forecasters (Q3 2026). The long-run level holds each number, so the factor stays near it once the median has arrived:

```yaml
# my-project/regimes/oil_crisis.yaml (a stress regime)
name: Oil Crisis
conditional_equities: true   # the other stock markets follow US stocks (below)
beliefs:
  inflation.united_states_inflation:
    long_run_mean:
      anchors: {1.0: 0.12, 3.0: 0.055, 8.0: 0.025}
    shocks:   # the median walks in straight lines: to 12% at year one, 5.5% at three, 2.5% at eight
      - {year: 1.0, magnitude: 0.12, mode: median, steer_from: 0.0}
      - {year: 3.0, magnitude: 0.055, mode: median, steer_from: 1.0}
      - {year: 8.0, magnitude: 0.025, mode: median, steer_from: 3.0}
```

The shipped regime walks the 3-month bill (9.0% at month ten, 5.6% at month eighteen, 4.4% at month thirty-eight) and unemployment (9.0% at month nineteen) the same way, from FRED, and takes the S&P 500's 43% fall over four quarters, from its daily closes. `relative: true` states a recorded change from the start instead of a level, as Rate Cut Cycle cuts the short rate by 5.03 points; on a stock, currency or commodity a median shock is the median's log return from the start.

Targets select scenarios after the shocks, so the median of the scenarios a regime keeps can sit away from its number; the replays therefore carry no targets. Real Estate Crash walks the median of house-price growth to -8% after a year and back to zero by year five the same way, and Yield Curve Inversion the curve's slope to its path at each of its two quarters. A regime that sets only a level, such as Persistent Inflation, describes where a factor settles rather than when it gets there, and leaves the pace to the calibration.

Rates in a regime are annualized decimals (0.12 is 12% a year; see [units](/projects/financescenarios/docs/units)). A belief or target naming a factor that is not in the run is refused, so a regime written for one factor set fails loudly on another. A regime can also extend another and state only what differs, as a regime of your own can.

<div class="fs-callout" markdown="1">
Check a factor's calibrated level before choosing anchors.
</div>

## Other Markets in a Crash

A crash rarely stays in one market, but a replay can only state the moves history recorded, and most of the dollar-priced funds the default set holds did not trade in 1973 or 1987. With `conditional_equities: true`, every equity a regime gives no shocks of its own moves by its expected move given the shocked ones, under the run's own correlations: the conditional stress of [Kupiec (1998)](https://doi.org/10.3905/jod.1998.408008){:target="_blank"}, in the form [Packham and Woebbeking (2019, section 2.2)](https://doi.org/10.1016/j.jbankfin.2019.01.020){:target="_blank"} state it:

$$
\mathbb{E}[r_p \mid r_c = s] = \Sigma_{pc}\,\Sigma_{cc}^{-1}\,s
$$

with $$s$$ the shocked ("core") equities' moves on a date and $$\Sigma$$ the run's covariance of the equities' returns. With one shocked market the move is its beta times the shock, $$\rho\,\sigma_p/\sigma_c$$ per unit, so a market that has moved closely with US stocks falls almost as far and a loosely tied one only part of the way. Only the mean moves: each scenario keeps the model's own randomness around it. Black Monday, Oil Crisis and the Fed, Bank of England and ESRB stress tests use it; the dot-com bust and Financial Crisis carry the recorded falls of the funds that traded then and use it for the rest, and COVID carries recorded moves for every market. Under Oil Crisis, where 100 in US stocks is worth 59.1 in the median scenario after a year, 100 in European stocks is worth 65.1, in Japanese stocks 78.5 and in emerging markets 64.1, against 109.4 to 112.3 in the baseline.

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

A targeted regime keeps only part of each draw, about 9% for AI and Tech Boom, so the run draws batches until 2,000 scenarios fit (24,000 draws in three batches on the 19 October 2026 calibration). The stressed percentiles then rest on as many scenarios as the baseline's. Each batch ranks its own draws, so "the worst 30%" means the worst 30% of a batch, not of all draws pooled: each batch's cutoff carries its own sampling noise, most in the first batch, so the stressed quantiles are close to, not exactly, those of one large ranked run.

## Reading a Stressed Run

A stressed run is read against the baseline, factor by factor on the same scale, as `compare_runs` does in the examples below. Four points to keep in mind:

- **Belief-driven runs are conditional, not likely.** The percentiles describe uncertainty given the story, not the probability of the story. Don't read a stressed 99.5% quantile as a capital number.
- **Targets select by rank, not by level.** Sequential targets keep a fixed share (30% of 30% is 9%) whatever the correlations, so the share says nothing about how likely the story is. In joint mode the share kept is the model's own estimate of how often the combination occurs; if it is tiny, the story is far in the tail of the calibration. When a run is filtered directly (`filter`, `filter_narrative`), fewer than 30 scenarios left raises a warning, because their percentiles are noise; a regime run draws until it has as many as asked for.
- **The other factors are the point.** The factors the regime did not touch move through the calibrated correlations (beliefs) or as they did on the selected paths (targets). That is where a narrative test adds information over a single-factor shock.
- **Recovery is an assumption.** After a stress-test path ends, factors fade back to calibration over a chosen period, and a prescribed policy rate converges onto its usual path before its rule takes over; a longer period means a more persistent stress.

## Examples

Every run below uses the calibration of the [overview](/projects/financescenarios/docs#simulating-scenarios): the default settings and factor set, calibrated on 19 October 2026, with 2,000 scenarios and seed 42.

### Beliefs Only: A Soft Landing

Soft Landing walks the median of US inflation in a straight line to 2% by year five and holds it there, and filters nothing out. To run it next to the baseline and compare the averages after five years:

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
| united_states_inflation | 0.0234 | 0.0253 |
| united_states_short_rate | 0.0459 | 0.0510 |
| us_broad | 0.0849 | 0.0822 |

The median lands on 2.00% after five years, but on this calibration the baseline's own median falls faster, to 1.81%, so the landing runs a little hotter than the baseline: inflation averages 2.53% after five years instead of 2.34%, and the short rate follows it through the policy rule, to 5.10% from 4.59%. A belief moves the center of the range rather than its width. When plotted:

{% include ft-chart.html id="regimes-soft-landing" src="/assets/data/financescenarios-guides/regimes.json" label="Median and 5-95% band of US inflation in the baseline and under Soft Landing over five years" %}

### A Replay: The Financial Crisis

Financial Crisis replays 2007-09 from today: US stocks and the default set's dollar-priced funds fall as far as they did from October 2007 to March 2009, in six steps over seventeen months, unemployment's median walks to 10% by year two, the short rate's to zero within fourteen months, where it stays to year eight, and house-price growth to -7.2% after a year. It keeps every scenario. To run it:

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
| us_broad | 0.0849 | -0.1158 |
| united_states_unemployment | 0.0553 | 0.0813 |
| united_states_short_rate | 0.0459 | 0.0032 |
| united_states_inflation | 0.0234 | 0.0234 |

In the median scenario 100 in US stocks is worth 47.6 after seventeen months and 54.7 after five years, a loss of 11.58% a year on average instead of a gain of 8.49%, and 100 in European stocks 37.5 at the low. Unemployment reaches 10.0% after two years and averages 8.13% after five instead of 5.53%, and the short rate stays near zero, at 0.32%. Inflation, which the regime does not name, averages 2.34% as in the baseline. When plotted, one variable per tab, US stocks as the value of 100:

{% include ft-chart.html id="regimes-financial-crisis" src="/assets/data/financescenarios-guides/regimes.json" label="Median and 5-95% band of the value of 100 in US stocks, US unemployment and the US short rate in the baseline and under Financial Crisis over five years" %}

### Steered Paths: Oil Crisis

Oil Crisis walks the median of US inflation to 12% after a year and 5.5% after three, as after the 1973 embargo, then toward 2.5% by year eight, and walks the 3-month bill and unemployment along their 1973-76 paths while US stocks fall 43% and the other markets follow. Two other inflation stories run beside it: Oil Shock, which adds about three points to US inflation over the half year to year two, and 2022 Inflation and Rate Hikes, which replays the 2021-23 surge to 9% and back. To run all three:

```python
runs = {"baseline": result}
for regime in ("oil_shock", "oil_crisis", "inflation_shock_2022"):
    runs[regime] = scenarios.simulate(regime=regime, n_simulations=2000, seed=42)

compare_runs(runs, factors=["united_states_inflation", "united_states_short_rate", "us_broad"])
```

Which returns:

| factor | baseline | oil_shock | oil_crisis | inflation_shock_2022 |
|:-------|---------:|----------:|-----------:|---------------------:|
| united_states_inflation | 0.0234 | 0.0274 | 0.0483 | 0.0295 |
| united_states_short_rate | 0.0459 | 0.0560 | 0.0427 | 0.0449 |
| us_broad | 0.0849 | 0.0803 | 0.0086 | 0.0829 |

Oil Crisis puts the median of US inflation at 12.00% after one year and 5.50% after three, and inflation averages 4.83% after five years. The short rate follows the bill rather than the rule, a negative real rate as in 1974: a median of 8.12% after a year, 5.61% after eighteen months and 4.25% after five years, an average of 4.27% against the baseline's 4.59%. Unemployment's median reaches 8.75% after eighteen months, and 100 in US stocks is worth 59.1 after a year and 102.7 after five, a return of 0.86% a year. When plotted, US inflation in the four runs:

{% include ft-chart.html id="regimes-inflation" src="/assets/data/financescenarios-guides/regimes.json" label="Median and 5-95% band of US inflation in the baseline and under Oil Shock, Oil Crisis and 2022 Inflation and Rate Hikes over five years" %}

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers cited on this page</b> <span class="ft-details__meta">4</span></summary>

- Boyle, P., Broadie, M., Glasserman, P. (1997). "Monte Carlo Methods for Security Pricing." Journal of Economic Dynamics and Control, 21(8-9), 1267-1321. [doi.org](https://doi.org/10.1016/S0165-1889(97)00028-6){:target="_blank"}
- Brigo, D., Mercurio, F. (2001). "A Deterministic-Shift Extension of Analytically-Tractable and Time-Homogeneous Short-Rate Models." Finance and Stochastics, 5(3), 369-387. [doi.org](https://doi.org/10.1007/pl00013541){:target="_blank"}
- Kupiec, P.H. (1998). "Stress Testing in a Value at Risk Framework." The Journal of Derivatives, 6(1), 7-24. [doi.org](https://doi.org/10.3905/jod.1998.408008){:target="_blank"}
- Packham, N., Woebbeking, F. (2019). "A Factor-Model Approach for Correlation Scenarios and Correlation Stress Testing." Journal of Banking & Finance, 101, 92-103. [doi.org](https://doi.org/10.1016/j.jbankfin.2019.01.020){:target="_blank"}

</details>

{% include ft-charts-script.html %}
