---
title: Simulation Engine
seo_title: "Simulation Engine Documentation | Finance Scenarios"
seo_title_suffix: false
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

<div class="ca-nav">
  <a href="#correlated-shocks"><i class="fas fa-shuffle" aria-hidden="true"></i>Correlated shocks</a>
  <a href="#fat-tails-and-tail-dependence"><i class="fas fa-bolt" aria-hidden="true"></i>Fat tails</a>
  <a href="#time-stepping"><i class="fas fa-clock" aria-hidden="true"></i>Time stepping</a>
  <a href="#how-the-correlations-are-estimated"><i class="fas fa-project-diagram" aria-hidden="true"></i>Correlations</a>
  <a href="#monte-carlo-error"><i class="fas fa-calculator" aria-hidden="true"></i>Monte Carlo error</a>
  <a href="#numerical-settings"><i class="fas fa-sliders-h" aria-hidden="true"></i>Numerical settings</a>
  <a href="#scenarioset"><i class="fas fa-layer-group" aria-hidden="true"></i>Working with a run</a>
</div>

## Correlated Shocks {#correlated-shocks}

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

where $$\nu$$ is the degrees of freedom. When $$W_t$$ is small, all factors take a large shock at once, so extreme moves cluster across factors (tail dependence). A Gaussian copula has no tail dependence for any correlation below one, while the t copula has it even at zero or negative correlation ([Demarta and McNeil, 2005, section 3.2](https://doi.org/10.1111/j.1751-5823.2005.tb00254.x){:target="_blank"}). The $$\nu - 2$$ keeps the variance at one, so every fitted volatility keeps its meaning and only the tails change.

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">Choosing the degrees of freedom</p>

Lower $$\nu$$ means fatter tails and must exceed 2. The default of 12 is the value [Kole, Koedijk and Verbeek (2007)](https://doi.org/10.1016/j.jbankfin.2006.09.010){:target="_blank"} fit to daily stock, government bond and real estate returns (12.1 in their Table 2), a portfolio for which their tests favor the Student-t copula and reject both the Gaussian and the Gumbel copula. Values near 5, often quoted, belong to shorter horizons: [Breymann, Dias and Embrechts (2003)](https://doi.org/10.1080/713666155){:target="_blank"} find 4.3 to 5.7 for hourly to daily DEM/JPY returns.
</div>

Normal shocks are the default. The scale is drawn independently at every step. With monthly steps, twelve fat-tailed shocks partly average out over a year, so Student-t shocks add less to a one-year 99.5% figure than the monthly tails suggest.

```yaml
# my-project/settings/my_settings.yaml (a settings profile)
engine:
  shock_distribution: student_t   # default: gaussian
  degrees_of_freedom: 12.0      # the default
```

Equity crises cluster a second way: with shared equity regimes (on in the shipped settings), all markets enter and leave their crisis regime together, which brings simulated equity correlations much closer to the fitted ones.

## Time Stepping {#time-stepping}

The horizon is cut into steps of equal length $$\Delta t$$, from daily to yearly. The shipped settings use:

<div class="ca-nums fs-nums">
  <span><b>2,000</b>scenarios</span>
  <span><b>Monthly</b>steps</span>
  <span><b>5 years</b>horizon</span>
</div>

Factors are stepped in cascade order, so a driver such as inflation is known before the factors that react to it. Each factor is stepped one of three ways:

| Factors | Step |
|:--------|:-----|
| Mean-reverting: rates under Hull-White, inflation, spreads, log commodity prices, log dividend yields | The exact solution of the Ornstein-Uhlenbeck process |
| Prices: equities, currencies | Exact, in log space |
| CIR rates and factors with GARCH volatility | An Euler step, so a shorter step is more accurate |

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

<ol class="ca-steps">
  <li markdown="span">**Mixed frequencies.** Changes are summed up to the coarser frequency and matched on calendar date, the way twelve monthly log returns add up to a yearly one.</li>
  <li markdown="span">**Pairwise windows.** Each pair uses the dates those two factors share, so a short series only weakens its own pairs. A pair with fewer than 5 shared observations is set to zero; fewer than 12, or a correlation above 0.98 (usually the same series configured twice), is flagged.</li>
  <li markdown="span">**Shrinkage.** Sample correlations are noisy, more so with many factors, so they are pulled toward a simpler target, trading a little bias for much less noise: by default the correlations themselves, not the covariances, toward zero by a data-driven amount ([Schäfer and Strimmer, 2005, section 2.4, eq. 10](https://doi.org/10.2202/1544-6115.1175){:target="_blank"}), larger when correlations rest on few observations; a fixed share instead pulls them toward their average correlation ([Ledoit and Wolf, 2004](http://www.ledoit.net/Honey_2004.pdf){:target="_blank"}), a target built for stocks that suits a mix of rates, inflation, equities and currencies less well.</li>
  <li markdown="span">**Repair.** A matrix built from different windows can be internally inconsistent (not positive definite) and then has no Cholesky factor. It is moved to the nearest valid correlation matrix, the nearest symmetric positive semidefinite matrix with unit diagonal ([Higham, 2002](https://doi.org/10.1093/imanum/22.3.329){:target="_blank"}), and the size of the repair is reported.</li>
</ol>

<div class="fs-callout fs-callout--limits" markdown="1">
<p class="fs-callout__title">Limits</p>

The matrix is linear and constant over the horizon: correlations do not rise in a crisis except through the Student-t shocks and shared equity regimes above.
</div>

## Monte Carlo Error {#monte-carlo-error}

A run of $$n$$ scenarios estimates a distribution with sampling error. For a mean, the standard error is

$$
\text{se} = \frac{s}{\sqrt{n}}
$$

with $$s$$ the standard deviation across scenarios. Halving the error takes four times as many scenarios. Tail percentiles are less precise still, because they rest on few scenarios: the 1st percentile of 1,000 scenarios is set by about ten of them.

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">A practical check</p>

Rerun with several seeds and see how much the number you report moves.
</div>

**Antithetic variates** reduce that error without more random draws. Every shock $$Z$$ is paired with its mirror image $$-Z$$ (under Student-t, a large common scale is also paired with a small one), so each pair's errors partly cancel; the standard error is then computed from the independent pair averages. On the default factor set it cut the seed-to-seed spread of a 60/40 portfolio's five-year 5th percentile by about a quarter. It is off in the shipped settings and needs an even number of scenarios.

Reading the standard error and rerunning with other seeds:

```python
result = scenarios.simulate(n_simulations=2000)
result.summary_statistics("united_states_short_rate")   # mean, std, se and percentiles per date

calibration = scenarios.calibrate()                      # fit once, then vary only the seed
reruns = [scenarios.simulate(calibration=calibration, seed=seed) for seed in range(5)]
```

## Numerical Settings {#numerical-settings}

Some numbers in a run have no economic meaning: they decide how precisely the engine and the fits do their work, not what the model says. They are settings, listed here so a run can be reproduced and defended, with the reason for each value.

### The Run

The settings of the run itself:

| Setting | Default | Kind | Why |
|:--|:--|:--|:--|
| Scenarios | 2,000 | Sourced minimum, judgement above it | The NAIC Valuation Manual's VM-21, Section 8.F, notes that straight Monte Carlo typically uses at least 1,000 scenarios, as cited in the [NAIC GOES Subgroup's SERT exposure (16 October 2024)](https://content.naic.org/sites/default/files/inline-files/GOES%20SG%20SERT%20Scenario,%20DR,%20and%20Scenario%20Statistics%20Exposure%20101624%20(1).pdf){:target="_blank"}. 2,000 keeps 100 paths in a 5% tail; NAIC's own set has 10,000 and DNB's 20,000 |
| Step | One month | Setting | Most of the data are monthly, and the regimes are fitted month by month |
| Horizon | 60 steps (five years) | Judgement | A business-planning horizon; the horizon setting changes it |
| Seed | 42 | Setting | Any fixed seed makes a run reproducible; each regime chain draws from its own stream, offset from the seed |
| Start date | 2026-01-01 | Setting | A fixed, reproducible jump-off date |
| Calibration window | Since 2000 | Judgement | Two full bear markets (2000-02 and 2008-09); longer records are read where a factor needs them, such as the term premium on OECD rates since 1950 |
| Shock distribution | Normal | Setting | Student-t shocks are an option (above) |
| Antithetic variates | Off | Setting | An option (above) |

### Correlations

The settings behind the correlation matrix:

| Setting | Default | Kind | Why |
|:--|:--|:--|:--|
| Estimation | Pairwise, each pair on the dates both share | Judgement | A short series weakens only its own pairs |
| Too few shared observations | Fewer than 5: the pair is set to 0; fewer than 12: flagged | Judgement | A correlation from a handful of points is noise |
| Same series twice | A correlation above 0.98 is flagged | Judgement | Usually one driver configured twice |
| Shrinkage | Toward zero, intensity from the data: 0.067 in the default calibration | Fitted | [Schäfer and Strimmer (2005, section 2.4, eq. 10)](https://doi.org/10.2202/1544-6115.1175){:target="_blank"}: their target D, with the intensity the summed variance of the correlations over their summed squares. Each correlation's variance uses the large-sample formula $$(1 - r_{ij}^2)^2/(n_{ij} - 1)$$ with the pair's own overlap, where they estimate it from the data (Appendix A) |
| Repair | Nearest correlation matrix, at most 100 iterations, tolerance $$10^{-8}$$: a change of 1.0e-14 in the default calibration | Setting | [Higham (2002, Algorithm 3.3)](https://doi.org/10.1093/imanum/22.3.329){:target="_blank"} with Dykstra's correction; the tolerance is that of his section 4 example, which converges in 19 iterations |
| Cholesky safety net | Up to 20 tries, adding a diagonal term ten times larger each time, at most 0.9 | Setting | Only for a matrix that is still not positive definite after the repair |

With $$\lambda$$ = 0.067, every correlation in the default calibration is 6.7% smaller than its sample value.

### Optimiser Settings

The fits use iterative optimisers. Their limits and starting points change how fast a fit converges, not what it converges to; where a likelihood has several maxima, the fit starts from several points and keeps the best. Each fit's method, limits and starting points:

| Fit | Method | Limits | Start |
|:--|:--|:--|:--|
| Equity regimes | Baum-Welch ([Baum, Petrie, Soules and Weiss, 1970](https://doi.org/10.1214/aoms/1177697196){:target="_blank"}) | 2,000 iterations, tolerance $$10^{-6}$$; volatility floor $$10^{-6}$$ | Each regime on one quantile slice of the sorted returns, equal switching |
| Inflation-driven switching | Expectation-maximisation ([Diebold, Lee and Weinbach, 1994](https://doi.org/10.1093/oso/9780198773917.003.0010){:target="_blank"}) | 500 iterations (the post-war fit converges in about 100), tolerance $$10^{-6}$$; a ridge penalty of 0.01 on the logit | A 90% chance of staying put |
| Inflation regimes | Maximum likelihood, Powell's method | 4,000 evaluations; tolerances $$10^{-6}$$ (parameters) and $$10^{-9}$$ (likelihood) | Three starts (the high regime's level, the shock sizes and the stay chances), scaled to a one-regime fit |
| Unemployment regimes | Maximum likelihood, L-BFGS-B | 2,000 iterations | Three splits of the months (by the residual's sign, its size, short recessions), two more with the equity link |
| Inflation's long-run median | Stationary vector of a (bin, regime) chain | Bins an eighth of a month's shock wide, six long-run spreads either side, at most 2,000 bins; median tolerance $$10^{-7}$$ | Finer bins move the US median by 0.2 basis points |

## Working with a Run {#scenarioset}

A run holds every factor's paths. A rate reads as an annualized rate and a price as its annualized return since the start (see [units](/projects/financescenarios/docs/units)). Filtering keeps whole scenarios, so a "high inflation, weak equities" subset still has consistent rates, spreads and currencies.

```python
result.horizon_summary([1, 3, 5])                        # percentiles of every factor at 1, 3 and 5 years

# stagflation: top 20% of US inflation, then the bottom 20% of US equities among those
stagflation = result.filter_narrative({"united_states_inflation": (0.8, 1.0), "us_broad": (0.0, 0.2)})

result.simulated_correlation()                           # compare with the fitted matrix
```

A long enough run also checks itself: each mean-reverting factor's simulated mean and spread at the horizon are compared with their theoretical long-run values (see [validation](/projects/financescenarios/docs/validation)). [Regimes](/projects/financescenarios/docs/regimes) covers narratives in depth, and the reference lists everything a run offers.

<div class="fs-ref"><a href="/projects/financescenarios/docs/reference/scenario-set"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Scenario set</a></div>
