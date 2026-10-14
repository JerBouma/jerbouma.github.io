---
title: Simulation Engine
seo_title: Simulation Engine Documentation – Finance Scenarios
excerpt: "The Monte Carlo engine behind every run: correlated and fat-tailed shocks, exact time stepping, antithetic variates, Monte Carlo error, and how correlations are estimated."
description: "The Finance Scenarios Monte Carlo engine: correlated and fat-tailed shocks, exact time stepping, antithetic variates and Monte Carlo error."
author_profile: false
permalink: /projects/financescenarios/docs/simulation-engine
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

How are the scenarios drawn, and how far can you trust a percentile read from them? The engine draws random shocks that move together the way history says they should and steps every factor forward one period at a time; each repetition is one scenario, and thousands of them form a distribution of outcomes.

The guides on [interest rates](/projects/financescenarios/docs/interest-rates), [the economy](/projects/financescenarios/docs/economy) and [markets](/projects/financescenarios/docs/markets) cover each model; this page covers what they share.

## Correlated Shocks

Each factor receives one random shock per step and scenario. Drawn independently, the factors would move on their own. To give them their historical co-movement, independent standard normal draws $$Z_t$$ are multiplied by the Cholesky factor $$L$$ of the correlation matrix $$R$$:

$$
\varepsilon_t = L\,Z_t, \qquad L L^\top = R
$$

The shocks $$\varepsilon_t$$ have unit variance and exactly the correlations in $$R$$, so a scenario with falling equities tends to show the spread, rate and currency moves history saw alongside one.

## Fat Tails {#fat-tails-and-tail-dependence}

Normal shocks have thin tails and almost never produce extreme moves in several factors at once, yet "everything sells off together" is exactly what a stress test is about. Student-t shocks ([Demarta and McNeil, 2005](https://doi.org/10.1111/j.1751-5823.2005.tb00254.x)) scale every factor's shock at a step by the same random draw:

$$
T_t = \varepsilon_t \sqrt{\frac{\nu - 2}{W_t}}, \qquad W_t \sim \chi^2_\nu
$$

where $$\nu$$ is the degrees of freedom. When $$W_t$$ is small, all factors take a large shock at once, so extreme moves cluster across factors (tail dependence). The $$\nu - 2$$ keeps the variance at one, so every fitted volatility keeps its meaning and only the tails change. Lower $$\nu$$ means fatter tails and must exceed 2; 5 is a common choice for financial returns, not a fitted value. Normal shocks are the default.

The scale is drawn independently at every step. With monthly steps, twelve fat-tailed shocks partly average out over a year, so Student-t shocks add less to a one-year 99.5% figure than the monthly tails suggest.

```yaml
engine:
  shock_distribution: student_t   # default: gaussian
  degrees_of_freedom: 5.0
```

Equity crises cluster a second way: with shared equity regimes (on in the shipped settings), all markets enter and leave their crisis regime together, which brings simulated equity correlations much closer to the fitted ones.

## Time Stepping

The horizon is cut into steps of equal length $$\Delta t$$, from daily to yearly; the shipped settings use 2,000 scenarios, monthly steps and five years. Factors are stepped in cascade order, so a driver such as inflation is known before the factors that react to it.

Mean-reverting factors (rates under Hull-White, inflation, spreads, log commodity prices, log dividend yields) are stepped with the exact solution of the Ornstein-Uhlenbeck process:

$$
x_{t+\Delta t} = \theta + (x_t - \theta)\, e^{-a \Delta t} + \sigma \sqrt{\frac{1 - e^{-2 a \Delta t}}{2a}}\; \varepsilon_t
$$

where $$\theta$$ is the long-run level, $$a$$ the speed of mean reversion, $$\sigma$$ the volatility and $$\varepsilon_t$$ the correlated shock. Each step closes a share $$1 - e^{-a\Delta t}$$ of the gap to $$\theta$$, and the long-run standard deviation settles at $$\sigma/\sqrt{2a}$$. Because the transition is exact, the step length adds no error: for a stand-alone factor, a yearly step gives the same year-end distribution as twelve monthly ones. Factors that react to another factor's path, regime switches and Student-t shocks do depend on the step. A rate stepped this way is Gaussian and can go negative; a factor modeled in logs stays positive.

Prices (equities, currencies) are stepped exactly in log space, so they stay positive and their returns are lognormal:

$$
S_{t+\Delta t} = S_t \exp\!\left(m\,\Delta t + \sigma\sqrt{\Delta t}\,\varepsilon_t\right)
$$

where $$m$$ is the expected log return per year and $$\sigma$$ the volatility. For an equity both belong to the regime it is in at that step; for a currency $$m = \mu - \tfrac{1}{2}\sigma^2$$, with $$\mu$$ its drift.

CIR rates and factors with GARCH volatility use an Euler step instead, so for them a shorter step is more accurate. CIR uses the full-truncation scheme of [Lord, Koekkoek and van Dijk (2010)](https://doi.org/10.1080/14697680802392496): drift and volatility are computed from the rate floored at zero, but the rate itself is not floored, so a path can dip slightly below zero, more often than the exact CIR process would.

## How the Correlations Are Estimated {#how-the-correlations-are-estimated}

The correlation matrix comes from the same historical changes each factor was fitted on (changes in a rate, log returns of a price), so it describes the shocks it drives.

- **Mixed frequencies.** Changes are summed up to the coarser frequency and matched on calendar date, the way twelve monthly log returns add up to a yearly one.
- **Pairwise windows.** Each pair uses the dates those two factors share, so a short series only weakens its own pairs. A pair with fewer than 5 shared observations is set to zero; fewer than 12, or a correlation above 0.98 (usually the same series configured twice), is flagged.
- **Shrinkage.** Sample correlations are noisy, more so with many factors, so they are pulled toward a simpler target, trading a little bias for much less noise: toward zero by a data-driven amount ([Schäfer and Strimmer, 2005](https://doi.org/10.2202/1544-6115.1175)) in the shipped settings, or toward the average correlation by a fixed share ([Ledoit and Wolf, 2004](http://www.ledoit.net/Honey_2004.pdf){:target="_blank"}).
- **Repair.** A matrix built from different windows can be internally inconsistent (not positive definite) and then has no Cholesky factor. It is moved to the nearest valid correlation matrix ([Higham, 2002](https://doi.org/10.1093/imanum/22.3.329){:target="_blank"}) and the size of the repair is reported.

The matrix is linear and constant over the horizon: correlations do not rise in a crisis except through the Student-t shocks and shared equity regimes above.

## Monte Carlo Error

A run of $$n$$ scenarios estimates a distribution with sampling error. For a mean, the standard error is

$$
\text{se} = \frac{s}{\sqrt{n}}
$$

with $$s$$ the standard deviation across scenarios. Halving the error takes four times as many scenarios. Tail percentiles are less precise still, because they rest on few scenarios: the 1st percentile of 1,000 scenarios is set by about ten of them. A practical check is to rerun with several seeds and see how much the number you report moves.

**Antithetic variates** reduce that error without more random draws. Every shock $$Z$$ is paired with its mirror image $$-Z$$ (under Student-t, a large common scale is also paired with a small one), so each pair's errors partly cancel; the standard error is then computed from the independent pair averages. On the default factor set it cut the seed-to-seed spread of a 60/40 portfolio's five-year 5th percentile by about a quarter. It is off in the shipped settings and needs an even number of scenarios.

```python
result = scenarios.simulate(n_simulations=2000)
result.summary_statistics("united_states_short_rate")   # mean, std, se and percentiles per date

calibration = scenarios.calibrate()                      # fit once, then vary only the seed
reruns = [scenarios.simulate(calibration=calibration, seed=seed) for seed in range(5)]
```

## Working with a Run {#scenarioset}

A run holds every factor's paths. A rate reads as an annualized rate and a price as its annualized return since the start (see [units](/projects/financescenarios/docs/units)). Filtering keeps whole scenarios, so a "high inflation, weak equities" subset still has consistent rates, spreads and currencies.

```python
result.horizon_summary([1, 3, 5])                        # percentiles of every factor at 1, 3 and 5 years

# stagflation: top 20% of US inflation, then the bottom 20% of US equities among those
stagflation = result.filter_narrative({"united_states_inflation": (0.8, 1.0), "us_broad": (0.0, 0.2)})

result.simulated_correlation()                           # compare with the fitted matrix
```

A long enough run also checks itself: each mean-reverting factor's simulated mean and spread at the horizon are compared with their theoretical long-run values (see [validation](/projects/financescenarios/docs/validation)). [Regimes](/projects/financescenarios/docs/regimes) covers narratives in depth, and the [reference](/projects/financescenarios/docs/reference/scenario-set) lists everything a run offers.
