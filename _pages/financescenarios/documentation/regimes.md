---
title: Regimes
seo_title: Stress Regimes Documentation – Finance Scenarios
excerpt: "A regime is a named stress narrative, such as an oil crisis or a regulator's adverse scenario. It changes the economics before simulating, keeps only the scenarios that fit the story afterwards, or both."
description: "Stress narratives in Finance Scenarios: belief overrides before simulating, conditioning on a story after, Fed and ESRB stress tests, reading the results."
author_profile: false
permalink: /projects/financescenarios/docs/regimes
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

A regime is a named stress narrative, such as an oil crisis, a financial crisis or a regulator's adverse scenario, written down once and reused across runs. It does not value anything itself: it produces a set of scenarios that your own valuation, ALM or capital model then runs on.

## Two Ways to Tell a Story

**Change the economics before simulating (beliefs).** A belief overrides a calibrated parameter: the long-run level a rate or inflation reverts to, the speed of that reversion, the volatility, an equity's bull and bear means and volatilities, or a one-off shock at a given year. Every scenario is then simulated under the new assumption, with its own randomness and the calibrated correlations intact.

**Condition on the outcome after simulating (targets).** A target keeps only the scenarios that land in a quantile range of one or more factors, such as the top 30% of short rates and the bottom 30% of equity returns. The model is unchanged: you look at the part of the baseline distribution where the story happens, and every other factor comes along on those same paths.

This is the difference between a stress test (an imposed shock) and scenario analysis (a combination of internally consistent moves): beliefs reshape the distribution, targets select from it.

| | Beliefs | Targets |
|:--|:--|:--|
| Acts on | the model's parameters | the simulated paths |
| Probability of the story | assumed (you impose it) | inside the base run (you pick its tail) |
| Other factors | move through the correlations | come along on the selected paths |
| Best for | a view on levels, a regulator's path, a shock | "what else happens when X happens" |

## Shipped Regimes

| Regime | The story | How |
|:-------|:----------|:----|
| `financial_crisis` | Stocks fall, unemployment rises and rates are cut, all at once | Targets |
| `credit_crunch` | Bank stocks collapse and the market follows (needs the `broad` set) | Both |
| `oil_crisis` | Inflation pulled to 9% in year one and back to 2.5% by year eight, with high rates and weak stocks | Both |
| `oil_shock` | A one-off three-point jump in US inflation in year two, then business as usual | Beliefs |
| `soft_landing` | Inflation eases smoothly to 2% by year five and stays there | Beliefs |
| `rate_cut_cycle` | Soft landing, then inflation drifts to 2.5% by year ten and back to its usual level | Beliefs |
| `yield_curve_inversion` | Short rates two points above long ones within six months, then the curve slowly rights itself | Both |
| `real_estate_crash` | House-price growth falls to -8% within a year and recovers over four | Both |
| `currency_crisis` | The Brazilian real devalues about 22% a year against the dollar (needs `us_only` or `broad`) | Both |
| `tech_selloff` | Tech stocks fall while the wider market holds up (needs `broad`) | Both |
| `commodity_supercycle` | A long oil boom: crude oil earns a top-quarter return | Targets |
| `climate_collapse` | A rough stand-in for a climate shock: the highest US inflation with the weakest US stocks | Targets |

## Beliefs as a Path

A long-run level can follow a term structure instead of a single number: anchors at chosen horizons, interpolated in between, and an optional period over which it fades back to the calibrated level after the last anchor. Because the factor still mean-reverts, it is pulled towards the moving target rather than set to it: a fast-reverting factor tracks the path closely, a slow one lags it. A path applies to constant-volatility factors only, not to GARCH volatility or business-cycle conditioning.

Oil Crisis uses both mechanisms:

```yaml
name: Oil Crisis
beliefs:
  inflation.united_states_inflation:
    long_run_mean:
      anchors: {1.0: 0.09, 3.0: 0.05, 8.0: 0.025}   # year: target inflation
targets:
  united_states_short_rate: [0.7, 1.0]   # top 30% by average short rate
  us_broad: [0.0, 0.3]                   # bottom 30% by equity return
```

Rates are annualized decimals (0.09 is 9% a year); see [units](/projects/financescenarios/docs/units). Check a factor's calibrated level before choosing anchors. A belief naming a factor that is not in the run is refused, so a regime written for one factor set fails loudly on another. A regime can extend another and state only what differs, as Rate Cut Cycle does with Soft Landing.

## How Targets Rank Scenarios

Each target ranks every scenario by one statistic over a window (the whole horizon by default): a rate by its average level, a price (equity, FX, commodity) by its annualized return from the window's first date to its last. Start-to-end is deliberate: a return annualized over a single month swings so widely that an average of since-start returns would really rank the first few months.

By default targets apply in sequence, each to what the previous one left, so a top-30% rate filter followed by a bottom-30% equity filter keeps about 9% of the run. Joint mode instead ranks each target against the full run and keeps the overlap, so the share kept depends on how the factors co-move and can be much smaller.

## Running a Regime {#driving-a-regime-from-the-library}

```python
from financescenarios import Scenarios, list_presets

list_presets(kind="regimes")   # the shipped regimes

scenarios = Scenarios.from_profiles(settings="default", factor_set="default")
baseline = scenarios.simulate(n_simulations=2000)
oil_crisis = scenarios.simulate(regime="oil_crisis", n_simulations=2000)
```

A targeted regime keeps only part of each draw, about 9% for Oil Crisis, so the run draws batches until 2,000 scenarios fit (about 22,700 draws here). The stressed percentiles then rest on as many scenarios as the baseline's. Each batch ranks its own draws, so "the worst 30%" means the worst 30% of a batch.

## Official Stress Tests as Regimes

Instead of writing a recession by hand, a regime can follow a regulator's published scenario, fetched through the Finance Toolkit with no API key:

- **Federal Reserve**: the US supervisory scenario, 13 quarters of the 3-month and 10-year Treasury rates, CPI inflation, unemployment and the stock market.
- **ESRB**: the European Systemic Risk Board's scenario for the EBA's EU-wide bank stress test, three years of the long-term rate, inflation, unemployment and stock prices for every EU member and the main other economies.

The published path becomes beliefs, not one deterministic path. Each interest rate, inflation and unemployment factor follows the scenario for its own country: by default it is set to the published value at each period end and its long-run level follows the scenario in between, so every scenario hits the published values, even for a slow-moving short rate. A gentler option steers only the long-run level. Afterwards each factor returns to its calibrated level over five years by default, and the usual randomness stays around the path, so you get a distribution around the regulator's story rather than one line.

Equities follow the published stock market as one-off price jumps, after which the equity model carries on. For the Federal Reserve the shock is the adverse path relative to its own baseline, so normal growth is not counted as stress; for the ESRB it is the published fall from the starting point. Each equity follows one region, the United States or the European Union by default.

```python
from financescenarios import Scenarios, build_toolkit, load_profiles, stress_test_regime

config = load_profiles(settings_id="default", factor_set_id="default")
toolkit = build_toolkit(config, api_key="FINANCIAL_MODELING_PREP_KEY")

regime = stress_test_regime(toolkit, config, authority="federal_reserve", scenario="adverse")  # or "esrb"
stressed = Scenarios.from_config(config, toolkit=toolkit, regime=regime).simulate()
```

Only factors with a long-run level can follow the scenario: real-world interest rates under Hull-White or CIR, inflation under the plain mean-reverting model, and unemployment. Other models and every risk-neutral factor keep their calibration. The Federal Reserve covers only the United States, so under it only US factors move. Its inflation is an annualized quarter-on-quarter rate, while this package's is year over year: the same scale, but it reacts sooner.

## Reading the Results Against the Base Run

Compare a stressed run with the baseline, factor by factor on the same scale. The size of the stress shows there: the Federal Reserve's 2026 adverse scenario, for example, takes US stocks about 50% below where they would otherwise be after a year.

- **Belief-driven runs are conditional, not likely.** The percentiles describe uncertainty given the story, not the probability of the story. Don't read a stressed 99.5% quantile as a capital number.
- **Targets select by rank, not by level.** Sequential targets keep a fixed share (30% of 30% is 9%) whatever the correlations, so the share says nothing about how likely the story is. In joint mode the share kept is the model's own estimate of how often the combination occurs; if it is tiny, the story is far in the tail of the calibration. Fewer than 30 scenarios left raises a warning, because their percentiles are noise.
- **The other factors are the point.** The factors the regime did not touch move through the calibrated correlations (beliefs) or as they did on the selected paths (targets). That is where a narrative test adds information over a single-factor shock.
- **Recovery is an assumption.** After a stress-test path ends, factors fade back to calibration over a chosen period; a longer period means a more persistent stress.

## Climate Scenarios

A climate pathway is an overlay rather than a regime. Enabled in a factor set, it adds an NGFS scenario's deviation from its baseline (Net Zero 2050, Delayed Transition, Current Policies and others) to each interest rate, inflation, unemployment and equity factor after simulating, and can add the scenario's carbon price as a factor. It combines with a regime: the regime shapes the scenarios, the climate pathway shifts them.
