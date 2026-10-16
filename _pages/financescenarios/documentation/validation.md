---
title: Validation
seo_title: "Validation Documentation | Finance Scenarios"
seo_title_suffix: false
excerpt: "How to trust a run: whether the scenarios reproduce the model's own long-run moments and correlations, pass the martingale test, and land near outside benchmarks such as NAIC GOES, DNB, a bond panel and option-implied densities."
description: "How to trust a Finance Scenarios run: long-run moments, correlations, martingale test, NAIC GOES, DNB, bond-panel and option-implied benchmarks, and limits."
author_profile: false
permalink: /projects/financescenarios/docs/validation
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

A scenario set is only useful if you can defend it to a model validator, an auditor or a regulator. That takes three kinds of evidence:

<div class="ca-cards ca-cards--3">
  <div><i class="ca-icon fas fa-square-root-variable" aria-hidden="true"></i><p class="ca-card-title">The model</p><p>The simulation does what the model's mathematics says (<a href="#the-simulation-reproduces-the-model">the simulation reproduces the model</a>).</p></div>
  <div><i class="ca-icon fas fa-history" aria-hidden="true"></i><p class="ca-card-title">History or prices</p><p>The scenarios fit the history they were calibrated on (<a href="#checking-a-run-against-history">checks against history</a>) or, for a valuation run, market prices (<a href="#market-consistency-the-martingale-test">the martingale test</a>).</p></div>
  <div><i class="ca-icon fas fa-scale-balanced" aria-hidden="true"></i><p class="ca-card-title">Outside references</p><p>They land near independent outside references (<a href="#external-benchmarks">external benchmarks</a>).</p></div>
</div>

This page covers each, what a failure means, and what is not validated.

## The Simulation Reproduces the Model {#the-simulation-reproduces-the-model}

The strongest evidence compares simulated output with a result derived independently of the code.

**Long-run moments.** Most rate-type factors are mean-reverting (Ornstein-Uhlenbeck), which has a known long-run distribution:

$$
dx_t = a(\theta - x_t)\,dt + \sigma\,dW_t \quad\Rightarrow\quad \mathbb{E}[x_\infty] = \theta,\qquad \operatorname{Var}[x_\infty] = \frac{\sigma^2}{2a}
$$

Here $$a$$ is the mean-reversion speed, $$\theta$$ the long-run level and $$\sigma$$ the volatility. For CIR the long-run variance is $$\sigma^2\theta/(2a)$$. Each mean-reverting factor's simulated mean and standard deviation at the horizon are compared with these values, allowing three standard errors of Monte Carlo noise. A gap is not always a fault: with a horizon shorter than about three time constants ($$1/a$$) the factor has not settled yet, and a factor on a belief path is deliberately steered elsewhere. A gap that remains points to the discretization or the calibration.

**Boundary behavior.** Hull-White rates are Gaussian and can go negative, as they should. CIR rates can dip very slightly below zero because of the full-truncation scheme, the least biased of those compared by [Lord, Koekkoek and van Dijk (2010)](https://doi.org/10.1080/14697680802392496){:target="_blank"}; see [time stepping](/projects/financescenarios/docs/simulation-engine#time-stepping).

**Correlations.** The correlated shocks reproduce their target: 50,000 draws with a target of 0.6 land within 0.02. Across a full run, the simulated factor moves are compared with the calibrated matrix (see the checks below); pairs where a model links one factor's drift to the other legitimately differ, so they are reported but not graded. This is the correlation test EIOPA lists for a generator: simulated against historical correlations ([Guidelines on valuation of technical provisions, EIOPA-BoS-14/166, Guideline 58, paragraph 1.105](https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en){:target="_blank"}).

## Market Consistency: The Martingale Test {#market-consistency-the-martingale-test}

A risk-neutral run used for valuation must reproduce today's prices: discounted along each scenario's own short rate, with dividends added back, a traded asset must on average be worth today's price at every future date. Passing shows the drift is risk neutral; it does not show that option prices are reproduced, since outside an equity with Heston volatility the volatility is a single number with no smile. With many dates tested at once, a correct run misses a few by chance, so the verdict adjusts for that ([Holm, 1979](https://www.jstor.org/stable/4615733){:target="_blank"}) rather than requiring every date to pass. The formula, a worked example and the matching bond-price check against EIOPA's curve are on the [Solvency II page](/projects/financescenarios/docs/solvency#martingale-test-example).

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">Most dates failing?</p>

Most dates failing usually means a real-world run or a missing dividend yield.
</div>

## Checking a Run Against History {#checking-a-run-against-history}

The same checks run on every published calibration and on any run of your own. Each passes, warns or fails, with the numbers and what they mean. They are screens for errors in the fit or the implementation, not acceptance criteria for the model.

The bands are wide on purpose: mean-reverting, regime-switching and GARCH factors legitimately move a little differently at another step size than their history, and a correlation gap above 0.25 points to a wiring problem rather than noise. A factor fitted on a longer history than the recent window is reported but not graded on volatility. Year-over-year rates (inflation, house-price growth) are compared on their changes over a year, in history and simulation alike: neighboring monthly readings share 11 of their 12 months, so their month-to-month changes understate how much they really move. The checks:

| Check | Warns or fails when | What a failure implies |
|:------|:--------------------|:-----------------------|
| Every factor calibrated | A configured factor's fit failed and it was left out (warn). | The run is missing a risk driver; read the reason before using it. |
| Parameters in a plausible range | A rate's long-run level is outside -5% to 25%, or a half-life outside about a week to 50 years (warn). | The fit is suspect, often from a short or unusual history, not necessarily wrong. |
| Valid correlation matrix | Not symmetric, no unit diagonal or a negative eigenvalue (fail). | The joint distribution is not well defined. |
| Simulation reproduces the correlations | A pair the model does not link directly misses its calibrated correlation by over 0.1 (warn) or 0.25 (fail). | Diversification between those factors is misstated. |
| Simulated volatility matches history | A factor's simulated yearly volatility is outside 0.67-1.5 times its history's (warn) or 0.33-3 times (fail). | Tails are too narrow or too wide for that factor. |
| Reproducible under a seed | Two runs with the same seed differ (fail; published calibrations only). | Results cannot be replayed for audit. |
| Every path is finite | Any path holds NaN or infinity (fail). | A numerical breakdown; the run should not be used. |

```python
result = scenarios.simulate(n_simulations=2000)
scenarios.validate(result)   # one row per check: status, detail, meaning
```

<div class="fs-callout" markdown="1">
A "warn" is worth a look, not a reason to discard the run.
</div>

The run itself also warns when a correlation was set to 0 because two factors shared fewer than 5 observations, when two factors correlate above 0.98 (usually the same driver configured twice), and when a filter leaves too few scenarios for percentiles to mean much. See [How the Correlations Are Estimated](/projects/financescenarios/docs/simulation-engine#how-the-correlations-are-estimated).

## External Benchmarks {#external-benchmarks}

The checks above compare the model with itself and its own data. The benchmarks below compare a calibrated factor with independent sources. Each reference embeds its own model choices, so a gap is not automatically an error, but a large or systematic one needs explaining. Four references are used:

| Benchmark | What is compared | Note |
|:----------|:-----------------|:-----|
| NAIC GOES | A US Treasury rate's simulated percentile bands | A set of differences, not a pass or fail |
| DNB scenario set | A run's interest rate, inflation or equity, quantile by quantile at every whole year | A regulator-reviewed reference for a euro run |
| Corporate bond panel | Credit spread levels and their dispersion across individual bonds | Validates spread levels, not rating migration |
| Option-implied densities | A risk-neutral equity's terminal-price distribution | Tests the flat-volatility lognormal assumption |

- **NAIC GOES.** The Generator of Economic Scenarios, the prescribed generator of the NAIC Valuation Manual for US principle-based reserves (VM-20 for life, VM-21 for variable annuities), run by Conning for the NAIC. Prescribed is not mandatory: a company may use its own generator if the result meets the Valuation Manual's standard in section 2.G ([NAIC Valuation Manual, 2026 edition, VM-20 Appendix 1, Section E](https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf#page=132){:target="_blank"}).

  A US Treasury rate's simulated percentile bands are compared with the percentile grid of NAIC's 10,000-scenario set for the matching tenor; the result is a set of differences, not a pass or fail. A large gap usually means the long-run level or the volatility differs from what US regulators consider a reasonable real-world spread of rates.
- **DNB scenario set.** De Nederlandsche Bank publishes a scenario set every quarter: 20,000 scenarios over 100 years from the Commissie Parameters 2022 model, both real world (the P-set) and market consistent (the Q-set, calibrated to market prices including swaptions). A run's interest rate, inflation or equity is compared with it at every whole year, quantile by quantile: rates and inflation by level, equities by yearly return. It is a regulator-reviewed reference for a euro run and the only free swaption-consistent one. The same sets, and NAIC's 16 deterministic stress scenarios for US rates (the set of the Valuation Manual's Stochastic Exclusion Ratio Test, SERT), can also replace factors in a run (see the [configuration reference](/projects/financescenarios/docs/reference/configuration)).
- **Corporate bond panel.** Credit spreads are fitted to one aggregate index per maturity bucket. The Open Source Bond Asset Pricing panel (Dickerson, Robotti and Rossetti; built on TRACE trades from 2002 to 2025, tens of millions of bond-date rows) shows the spread distribution of the individual bonds underneath. The comparison shows whether the aggregate's fitted level and volatility represent the real dispersion or smooth over fatter tails and idiosyncratic widening. The public data has no credit ratings, so it validates spread levels, not rating migration.
- **Option-implied densities.** A risk-neutral equity's simulated terminal-price distribution is compared with the market's own risk-neutral density at the nearest listed expiration, extracted from option prices with the [Breeden-Litzenberger (1978)](https://doi.org/10.1086/296025) result. Both sides come from the same market, so this tests the flat-volatility lognormal assumption rather than providing an outside view. The headline number is the Wasserstein distance (how far apart the two terminal-price views are, on average, in price units); a Kolmogorov-Smirnov statistic flags a sharp local tail mismatch the average could hide. Expect a gap: the market's density is skewed and fat-tailed, the model's is not.

## Published Calibrations {#published-calibrations}

A published calibration is fixed under a version tag, passes the checks above before release, and records its data window, package versions and a hash of its configuration. A run can then state exactly which calibration it used, and anyone can reproduce its scenarios offline. A release whose configuration no longer matches its hash is refused rather than silently mixing two sets of assumptions. Reference calibrations are meant to be published once a year, the minimum frequency EIOPA sets for these tests ([Guidelines on valuation of technical provisions, Guideline 58, paragraph 1.106](https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en){:target="_blank"}).

Downloading and simulating a release is covered in the runs and releases reference.

<div class="fs-ref"><a href="/projects/financescenarios/docs/reference/runs-and-releases"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Runs and releases</a></div>

## What Is Not Validated {#what-is-not-validated}

<div class="fs-callout fs-callout--limits" markdown="1">
- **Dependence is one linear correlation matrix**, constant over the horizon. A Student-t shock distribution adds joint tail risk through one shared t-copula (see [fat tails](/projects/financescenarios/docs/simulation-engine#fat-tails-and-tail-dependence)), but tail dependence that differs by pair or is asymmetric is not captured.
- **Risk-neutral calibration is limited in scope.** Interest rates, inflation, equities, FX and commodities can be calibrated risk neutral, but without a full arbitrage-free volatility surface: rate and inflation volatilities come from history, not from swaption or inflation-option prices, so the time value of guarantees is indicative; see the [measures section of the configuration page](/projects/financescenarios/docs/configuration#real-world-and-risk-neutral-measures).
- **Judgment calls are not checked for economic sense.** The number of equity regimes and every belief override are the user's choice; only their shape is checked, not whether they are reasonable.
- **No out-of-sample backtest.** Nothing checks how often realized history fell inside the bands a calibration would have predicted at the time. Historical paths can be fetched in the same shape as a run for a portfolio backtest, but a coverage test of the bands is left to the user.
- **No scenario reduction or moment matching.** Every simulated path is returned as drawn; none are selected or reweighted to match target moments with fewer scenarios.
</div>
