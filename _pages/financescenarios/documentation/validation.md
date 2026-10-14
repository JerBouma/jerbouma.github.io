---
title: Validation
seo_title: Validation Documentation – Finance Scenarios
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

A scenario set is only useful if you can defend it to a model validator, an auditor or a regulator. That takes three kinds of evidence: the simulation does what the model's mathematics says, the scenarios fit the history they were calibrated on (or, for a valuation run, market prices), and they land near independent outside references. This page covers each, what a failure means, and what is not validated.

## The Simulation Reproduces the Model

The strongest evidence compares simulated output with a result derived independently of the code.

**Long-run moments.** Most rate-type factors are mean-reverting (Ornstein-Uhlenbeck), which has a known long-run distribution:

$$
dx_t = a(\theta - x_t)\,dt + \sigma\,dW_t \quad\Rightarrow\quad \mathbb{E}[x_\infty] = \theta,\qquad \operatorname{Var}[x_\infty] = \frac{\sigma^2}{2a}
$$

Here $$a$$ is the mean-reversion speed, $$\theta$$ the long-run level and $$\sigma$$ the volatility. For CIR the long-run variance is $$\sigma^2\theta/(2a)$$. Each mean-reverting factor's simulated mean and standard deviation at the horizon are compared with these values, allowing three standard errors of Monte Carlo noise. A gap is not always a fault: with a horizon shorter than about three time constants ($$1/a$$) the factor has not settled yet, and a factor on a belief path is deliberately steered elsewhere. A gap that remains points to the discretization or the calibration.

**Boundary behavior.** Hull-White rates are Gaussian and can go negative, as they should. CIR rates can dip very slightly below zero because of the full-truncation scheme, the least biased of those compared by Lord, Koekkoek and van Dijk (2010); see [time stepping](/projects/financescenarios/docs/simulation-engine#time-stepping).

> "The full truncation scheme by far outperforms all biased schemes in terms of bias, root-mean-squared error, and hence should be the preferred discretisation method for simulation of the Heston model and extensions thereof."
> <cite>[Lord, Koekkoek and van Dijk (2006), A comparison of biased simulation schemes for stochastic volatility models, Tinbergen Institute Discussion Paper TI 2006-046/4, abstract](https://repub.eur.nl/pub/7738/2006-0464.pdf#page=3)</cite>

**Correlations.** The correlated shocks reproduce their target: 50,000 draws with a target of 0.6 land within 0.02. Across a full run, the simulated factor moves are compared with the calibrated matrix (see the checks below); pairs where a model links one factor's drift to the other legitimately differ, so they are reported but not graded. This is the correlation test EIOPA lists for a generator.

> "(c) Correlation tests: comparison of the simulated correlations with the historical correlations."
> <cite>[EIOPA, Guidelines on valuation of technical provisions (EIOPA-BoS-14/166), Guideline 58, paragraph 1.105](https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en)</cite>

## Market Consistency: The Martingale Test

A risk-neutral run used for valuation must reproduce today's prices: discounted along each scenario's own short rate, with dividends added back, a traded asset must on average be worth today's price at every future date. Passing shows the drift is risk neutral; it does not show that option prices are reproduced, since outside an equity with Heston volatility the volatility is a single number with no smile. Most dates failing usually means a real-world run or a missing dividend yield. The formula, a worked example and the matching bond-price check against EIOPA's curve are on the [Solvency II page](/projects/financescenarios/docs/solvency#martingale-test-example).

## Checking a Run Against History

The same checks run on every published calibration and on any run of your own. Each passes, warns or fails, with the numbers and what they mean. They are screens for errors in the fit or the implementation, not acceptance criteria for the model. The bands are wide on purpose: mean-reverting, regime-switching and GARCH factors legitimately move a little differently at another step size than their history, and a correlation gap above 0.25 points to a wiring problem rather than noise. A factor fitted on a longer history than the recent window is reported but not graded on volatility.

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

A "warn" is worth a look, not a reason to discard the run. The run itself also warns when a correlation was set to 0 because two factors shared fewer than 5 observations, when two factors correlate above 0.98 (usually the same driver configured twice), and when a filter leaves too few scenarios for percentiles to mean much. See [How the Correlations Are Estimated](/projects/financescenarios/docs/simulation-engine#how-the-correlations-are-estimated).

## External Benchmarks

The checks above compare the model with itself and its own data. The benchmarks below compare a calibrated factor with independent sources. Each reference embeds its own model choices, so a gap is not automatically an error, but a large or systematic one needs explaining.

- **NAIC GOES.** The US statutory scenario set, generated by Conning for the NAIC and prescribed for VM-20/21/22 reserve calculations. A US Treasury rate's simulated percentile bands are compared with NAIC's published percentile grid for the matching tenor. A failure usually means the long-run level or the volatility differs from what US regulators consider a reasonable real-world spread of rates.
- **DNB scenario set.** De Nederlandsche Bank publishes a scenario set every quarter: 20,000 scenarios over 100 years from the Commissie Parameters 2022 model, both real world (the P-set) and market consistent (the Q-set, calibrated to market prices including swaptions). A run's interest rate, inflation or equity is compared with it at every whole year, quantile by quantile: rates and inflation by level, equities by yearly return. It is a regulator-reviewed reference for a euro run and the only free swaption-consistent one. The same sets (and NAIC GOES rates) can also replace factors in a run (see the [configuration reference](/projects/financescenarios/docs/reference/configuration)).
- **Corporate bond panel.** Credit spreads are fitted to one aggregate index per maturity bucket. The Open Source Bond Asset Pricing panel (Dickerson, Robotti and Rossetti; built on TRACE trades from 2002 to 2025, tens of millions of bond-date rows) shows the spread distribution of the individual bonds underneath. The comparison shows whether the aggregate's fitted level and volatility represent the real dispersion or smooth over fatter tails and idiosyncratic widening. The public data has no credit ratings, so it validates spread levels, not rating migration.
- **Option-implied densities.** A risk-neutral equity's simulated terminal-price distribution is compared with the market's own risk-neutral density at the nearest listed expiration, extracted from option prices with the [Breeden-Litzenberger (1978)](https://doi.org/10.1086/296025) result. Both sides come from the same market, so this tests the flat-volatility lognormal assumption rather than providing an outside view. The headline number is the Wasserstein distance (how far apart the two terminal-price views are, on average, in price units); a Kolmogorov-Smirnov statistic flags a sharp local tail mismatch the average could hide. Expect a gap: the market's density is skewed and fat-tailed, the model's is not.

## Published Calibrations {#published-calibrations}

A published calibration is fixed under a version tag, passes the checks above before release, and records its data window, package versions and a hash of its configuration. A run can then state exactly which calibration it used, and anyone can reproduce its scenarios offline. A release whose configuration no longer matches its hash is refused rather than silently mixing two sets of assumptions. Reference calibrations are meant to be published once a year, the minimum frequency EIOPA sets for these tests.

> "Insurance and reinsurance undertakings should ensure that the tests of accuracy, robustness and market consistency of the ESG are performed on a regular basis and at least annually."
> <cite>[EIOPA, Guidelines on valuation of technical provisions (EIOPA-BoS-14/166), Guideline 58, paragraph 1.106](https://www.eiopa.europa.eu/publications/guidelines-valuation-technical-provisions_en)</cite>

Downloading and simulating a release is covered in the [runs and releases reference](/projects/financescenarios/docs/reference/runs-and-releases).

## What Is Not Validated

- **Dependence is one linear correlation matrix**, constant over the horizon. A Student-t shock distribution adds joint tail risk through one shared t-copula (see [fat tails](/projects/financescenarios/docs/simulation-engine#fat-tails-and-tail-dependence)), but tail dependence that differs by pair or is asymmetric is not captured.
- **Risk-neutral calibration is limited in scope.** Interest rates, inflation, equities, FX and commodities can be calibrated risk neutral, but without a full arbitrage-free volatility surface; see the [measures section of the configuration page](/projects/financescenarios/docs/configuration#real-world-and-risk-neutral-measures).
- **Judgment calls are not checked for economic sense.** The number of equity regimes and every belief override are the user's choice; only their shape is checked, not whether they are reasonable.
- **No out-of-sample backtest.** Nothing checks how often realized history fell inside the bands a calibration would have predicted at the time. Historical paths can be fetched in the same shape as a run for a portfolio backtest, but a coverage test of the bands is left to the user.
- **No scenario reduction or moment matching.** Every simulated path is returned as drawn; none are selected or reweighted to match target moments with fewer scenarios.
