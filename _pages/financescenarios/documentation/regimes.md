---
title: Regimes
seo_title: Stress Regimes Documentation – Finance Scenarios
excerpt: "A regime is a named stress narrative, such as an oil crisis or a regulator's adverse scenario. It changes the economics before simulating, keeps only the scenarios that fit the story afterwards, or both."
description: "Stress narratives in Finance Scenarios: belief overrides of drift and volatility, conditioning on a story, Fed and ESRB stress tests, and reading the results."
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

**Change the economics before simulating (beliefs).** A belief overrides a calibrated parameter: the long-run level a rate or inflation reverts to, the speed of that reversion, the volatility, an equity's regime means and volatilities, or a one-off shock at a given year. Every scenario is then simulated under the new assumption, with its own randomness and with the calibrated correlations intact.

**Condition on the outcome after simulating (targets).** A target keeps only the scenarios that land in a quantile range of one or more factors, such as the top 30% of short rates and the bottom 30% of equity returns. Nothing about the model changes: you look at the part of the baseline distribution where the story happens, and every other factor comes along on those same paths.

The distinction mirrors the one Solvency II draws between a stress test (a single prescribed shock) and scenario analysis (a combination of correlated, internally consistent shocks). Beliefs reshape the distribution; targets select from it.

| | Beliefs | Targets |
|:--|:--|:--|
| Acts on | the model's parameters | the simulated paths |
| Probability of the story | assumed (you impose it) | inside the base run (you pick its tail) |
| Other factors | move through the correlations | come along on the selected paths |
| Best for | a view on levels, a regulator's path, a shock | "what else happens when X happens" |

## Beliefs as a Path

A long-run level can follow a term structure instead of a single number: anchors at chosen horizons, interpolated in between, and an optional period over which it fades back to the calibrated level after the last anchor. Because the factor still mean-reverts, it is pulled towards the moving target rather than set to it, so a fast-reverting factor tracks the path closely and a slow one lags it. A path applies to constant-volatility factors; it does not combine with GARCH volatility or business-cycle conditioning.

The shipped Oil Crisis regime uses both mechanisms: inflation is pulled to 9% in year one and eased back to 2.5% by year eight, and the run is then narrowed to high-rate, weak-equity scenarios.

```yaml
name: Oil Crisis
beliefs:
  inflation.united_states_inflation:
    long_run_mean:
      anchors: {1.0: 0.09, 3.0: 0.05, 8.0: 0.025}
targets:
  united_states_short_rate: [0.7, 1.0]   # top 30% by average short rate
  us_broad: [0.0, 0.3]                   # bottom 30% by equity return
```

Rates are annualized decimals (0.09 is 9% a year) and prices are levels; see [units](/projects/financescenarios/docs/units). Check a factor's calibrated level before choosing anchors. A belief naming a factor that is not in the run is refused, so a regime written for one factor set fails loudly on another. A regime can also extend another, stating only what differs (Rate Cut Cycle extends Soft Landing this way).

## How Targets Rank Scenarios

Each target ranks every scenario by one statistic over a window (the whole horizon by default): a rate by its average level, a price (equity, FX, commodity) by its annualized return from the window's first date to its last. Start-to-end is deliberate: a return annualized over a single month swings so widely that an average of since-start returns would really rank the first few months.

Several targets apply in sequence by default, each to what the previous one left, so a top-30% rate filter followed by a bottom-30% equity filter keeps about 9% of the run. Joint mode instead ranks each target against the full run and keeps only the overlap, so the share kept depends on how the factors co-move and can be much smaller.

## Running a Regime {#driving-a-regime-from-the-library}

A regime is named by its file name, on the instance or on a single run. Its beliefs change what is simulated; its targets keep the scenarios that fit.

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

- **Federal Reserve**: the supervisory scenario for the United States, 13 quarters of the 3-month and 10-year Treasury rates, CPI inflation, unemployment and the stock market.
- **ESRB**: the European Systemic Risk Board's scenario for the EBA's EU-wide bank stress test, three years of the long-term rate, inflation, unemployment and stock prices for every EU member and the main other economies.

The published path becomes beliefs, not a single deterministic path. Each interest rate, inflation and unemployment factor follows the scenario for its own country: by default it is set to the published value at each period end and its long-run level follows the scenario in between, so even a slow-moving short rate really falls to the Federal Reserve's 0.1%. A gentler option steers only the long-run level. Either way the factor returns to its calibrated level over five years (by default) after the scenario ends, and the usual randomness stays around the path, so you get a distribution around the regulator's story rather than one line.

Equities follow the scenario's stock market as one-off price jumps, after which the equity model carries on. The Federal Reserve's stock path is used as the adverse level against its own baseline, so the shock is the stress and not the baseline's growth; the ESRB's is the fall from the starting point. Each equity maps to one published region (the United States or the European Union by default, configurable per equity), and the stock path starts at the run's start so the fall always lands inside the run.

```python
from financescenarios import Scenarios, stress_test_regime

regime = stress_test_regime(toolkit, config, authority="federal_reserve", scenario="adverse")
stressed = Scenarios.from_config(config, toolkit=toolkit, regime=regime).simulate()
```

Not every factor can be steered. The scenario acts through the long-run level, so only factors that have one follow it: real-world interest rates under Hull-White or CIR, inflation under the plain mean-reverting model, and unemployment. Other models and every risk-neutral factor keep their calibration; risk-neutral equities are left alone because their drift is the simulated short rate. The Federal Reserve covers only the United States, so under it only US entries move. Its inflation is an annualized quarter-on-quarter rate, while this project's is year over year: the same scale, but it reacts sooner.

## Reading the Results Against the Base Run

Read a stressed run against the baseline, factor by factor on the same scale. On the `default` set, the median US broad-market price after a year is 0.50 times the start under the Federal Reserve's 2026 adverse scenario and 0.57 times under the ESRB's, against 1.14 unstressed. On the US factors of the `us_only` set, the 2026 severely adverse scenario puts the short rate at 0.1% within a year and unemployment at about 9.8% after two, against 3.7% and 5.5% in the unstressed run.

- **Belief-driven runs are conditional, not likely.** The percentiles describe uncertainty given the story, not the probability of the story. Don't read a stressed 99.5% quantile as a capital number.
- **Targets select by rank, not by level.** Sequential targets keep a fixed share (30% of 30% is 9%) whatever the correlations, so the share says nothing about how likely the story is. In joint mode the share kept is the model's own estimate of how often the combination occurs; if it is tiny, the story is far in the tail of the calibration, and a filter that leaves fewer than 30 scenarios raises a warning because its percentiles are noise.
- **The other factors are the point.** Look at the factors the regime did not touch: they move through the calibrated correlations (beliefs) or as they did on the selected paths (targets), which is where a narrative test adds information over a single-factor shock.
- **Recovery is an assumption.** After a stress-test path ends, factors fade back to calibration over a chosen period. A longer convergence period means a more persistent stress.

## Climate Scenarios

A climate pathway is an overlay rather than a regime: enabling it in a factor set adds an NGFS scenario's deviation from its baseline (Net Zero 2050, Delayed Transition, Current Policies and others) to each interest rate, inflation, unemployment and equity factor after simulating, and can add the scenario's carbon price as a factor. It combines with a regime: the regime shapes the scenarios, the climate pathway shifts them.
