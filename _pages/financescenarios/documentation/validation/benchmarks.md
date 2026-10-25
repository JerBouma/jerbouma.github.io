---
title: Benchmarks
seo_title: "Benchmarks | Finance Scenarios"
seo_title_suffix: false
excerpt: "How Finance Scenarios compares a run with outside references: NAIC's GOES and its acceptance criteria, DNB's scenario sets, a corporate bond panel and option-implied densities."
description: "External benchmarks for Finance Scenarios: NAIC's Generator of Economic Scenarios and its acceptance criteria T1 to T6 and E1, DNB's P and Q sets, the Open Source Bond Asset Pricing panel and Breeden-Litzenberger densities."
author_profile: false
permalink: /projects/financescenarios/docs/validation/benchmarks
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/validation
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-validation"
---

The [checks against history](/projects/financescenarios/docs/validation) compare the model with itself and its own data. Benchmarks compare a calibrated factor with independent sources: the generators regulators prescribe, a panel of individual bonds and the option market. Each reference embeds its own model choices, so a gap is not automatically an error, but a large or systematic one needs explaining. This page sets out the four references and holds the `goes` factor set to the acceptance criteria of NAIC's own generator.

## Four References

Each reference checks a different part of a run:

| Benchmark | What is compared | Note |
|:----------|:-----------------|:-----|
| NAIC GOES | A US Treasury rate's simulated percentile bands, and a run against GOES's own acceptance criteria | Differences by percentile, and a pass or fail per criterion |
| DNB scenario set | A run's interest rate, inflation or equity, quantile by quantile at every whole year | A regulator-reviewed reference for a euro run |
| Corporate bond panel | Credit spread levels and their dispersion across individual bonds | Validates spread levels, not rating migration |
| Option-implied densities | A risk-neutral equity's terminal-price distribution | Tests the flat-volatility lognormal assumption |

- **NAIC GOES.** The Generator of Economic Scenarios, the prescribed generator of the NAIC Valuation Manual for US principle-based reserves (VM-20 for life, VM-21 for variable annuities), run by Conning for the NAIC. Prescribed is not mandatory: a company may use its own generator if the result meets the Valuation Manual's standard in section 2.G ([NAIC Valuation Manual, 2026 edition, VM-20 Appendix 1, Section E](https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf#page=132){:target="_blank"}).

  A US Treasury rate's simulated percentile bands are compared with the percentile grid of NAIC's 10,000-scenario set for the matching tenor; the result is a set of differences, not a pass or fail. A large gap usually means the long-run level or the volatility differs from what US regulators consider a reasonable real-world spread of rates. `check_acceptance` adds the pass or fail: it holds the run to the criteria NAIC holds GOES itself to ([below](#goes-acceptance-criteria)).
- **DNB scenario set.** De Nederlandsche Bank publishes a scenario set every quarter: 20,000 scenarios over 100 years from the CP2022 model of the Commissie Parameters (2022), both real world (the P-set) and market consistent (the Q-set, calibrated to market prices including swaptions). A run's interest rate, inflation or equity is compared with it at every whole year, quantile by quantile: rates and inflation by level, equities by yearly return. It is a regulator-reviewed reference for a euro run and the only free swaption-consistent one. `Dnb.compare_moments` and `Dnb.compare_correlations` set a run's means, standard deviations, percentiles and correlations beside the set's, year by year; the `dnb` factor set, which runs DNB's own model ([CP2022](/projects/financescenarios/docs/interest-rates/cp2022)), lands within Monte Carlo error of it. The same sets, and NAIC's 16 deterministic stress scenarios for US rates (the set of the Valuation Manual's Stochastic Exclusion Ratio Test, SERT), can also replace factors in a run (`external_scenario_source` in a factor set).
- **Corporate bond panel.** Credit spreads are fitted to one aggregate index per maturity bucket. The [Open Source Bond Asset Pricing](https://openbondassetpricing.com/){:target="_blank"} panel of Dickerson, Robotti and Rossetti, built on the TRACE reports of US corporate bond trades from 2002 to 2025 (tens of millions of bond-date rows), gives the spread distribution of the individual bonds underneath. The comparison shows whether the aggregate's fitted level and volatility represent the real dispersion or smooth over fatter tails and idiosyncratic widening. The public data has no credit ratings, so it validates spread levels, not rating migration.
- **Option-implied densities.** A risk-neutral equity's simulated terminal-price distribution is compared with the market's own risk-neutral density at the nearest listed expiration, extracted from call prices $$C(K)$$ across strikes with the result of [Breeden and Litzenberger (1978)](https://doi.org/10.1086/296025){:target="_blank"}, $$f(K) = e^{rT}\,\partial^2 C/\partial K^2$$. Both sides come from the same market, so this tests the flat-volatility lognormal assumption rather than providing an outside view. The headline number is the Wasserstein distance $$W_1 = \int \lvert F_{\text{sim}}(K) - F_{\text{mkt}}(K)\rvert\,dK$$ between the two distribution functions, how far apart the two terminal-price views are on average, in price units; a Kolmogorov-Smirnov statistic flags a sharp local tail mismatch the average could hide. Expect a gap: the market's density is skewed and fat-tailed, the model's lognormal one is not.

## GOES Acceptance Criteria {#goes-acceptance-criteria}

NAIC holds GOES itself to a set of acceptance criteria, published with each release on its workbook's `Acceptance Criteria_Dashboard` sheet. A company that uses its own generator must meet the Valuation Manual's requirements ([VM-20, Appendix 1](https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf#page=132){:target="_blank"}), so holding a run to the bar GOES clears shows how close it comes. `NaicGoes.check_acceptance` reads the thresholds from the release, so they follow NAIC's revisions, and checks:

| Criterion | What it checks |
|:--|:--|
| T1 | The upper tail: the 99.5th percentile of the 1-year and 20-year yields, and the share of scenarios that ever cross the cap |
| T2 | Negative rates: the lowest 1-year and 20-year yields |
| T4 | Low for long: the share of scenarios whose 20-year yield averages below a floor for ten and thirty years |
| T5 | The spread of the 20-year yield's 10-year and 30-year geometric averages: their 1st and 99th percentiles, against bounds interpolated at the run's mean starting 20-year yield |
| T6 | Mean reversion: the 1-year and 20-year medians in year 30 |
| E1 | The S&P 500's gross wealth factors, percentile by percentile |

The criteria are written on the 1-year and 20-year yields, which no index quotes; a run that does not simulate them reads them off its neighboring tenors in a straight line (3-month and 5-year, 10-year and 30-year). E1 publishes targets but no tolerance, so each percentile passes within 10% of its target (`tolerance`), a judgment: GOES's own factors sit within 7.2% of the targets from the 1st to the 99th percentile.

The `goes` factor set is built on what NAIC and the American Academy of Actuaries publish. Its 3-month, 5-year, 10-year and 30-year yields are each a one-factor CIR: the speed is $$\ln 2 / 15$$, the 15-year half-life behind T6; the long-run level is GOES's mean over years 20 to 30; and the volatility is set so that the model's year-30 median, computed exactly from the CIR distribution, equals GOES's (the simulated medians differ by Monte Carlo noise). Its stocks are fitted on Shiller's S&P total return since 1946, shifted so the long-run return is E1's own median: 7.41% a year in log terms ($$\ln(9.23)/30$$, GOES's 3.73% cash plus 3.68%), or 7.69% compounded. They earn their premium over that long-run level rather than over the simulated rate, as the GOES Subgroup decided when it removed the old generator's equity-rate link. To hold the set to the release of 30 September 2026 with 10,000 scenarios:

```python
from financescenarios import Scenarios
from financescenarios.validation.naic_goes.naic_goes_controller import NaicGoes

scenarios = Scenarios.from_profiles(settings="goes", factor_set="goes")
result = scenarios.simulate(years=30, n_simulations=10_000)
NaicGoes(vintage="20260930").check_acceptance(result, scenarios.config, equity_name="us_broad")
```

Which gives, next to GOES's own figures:

| Check | GOES | `goes` set |
|:--|--:|--:|
| 3-month yield, 50th / 95th / 99th percentile in year 30 | 2.80 / 10.88 / 15.42% | 2.77 / 10.85 / 15.95% |
| 3-month yield, 50th / 95th / 99th percentile in year 10 | 3.21 / 10.61 / 14.13% | 3.39 / 9.59 / 13.21% |
| 10-year yield, 50th / 99th percentile in year 30 | 4.50 / 14.83% | 4.43 / 14.45% |
| T1: 1-year 99.5th percentile, highest (at most 18%) | 17.65% | 16.79%, pass |
| T1: 20-year 99.5th percentile, highest (at most 17%) | 16.41% | 16.06%, pass |
| T1: share ever above the cap, 1-year / 20-year (at most 0.5%) | 3.06 / 2.57% | 1.47 / 1.38%, fail |
| T2: lowest 1-year (at least -1%) | pass | -0.02%, pass |
| T2: lowest 20-year (at least 0%) | pass | 0.01%, pass |
| T4: low for long over 10 / 30 years (at least 7.5 / 3.75%) | 3.44 / 2.87%, fail | 0.00 / 0.63%, fail |
| T5: 99th percentile of the 20-year averages, 10 / 30 years | 10.01 / 10.61% | 8.97 / 10.79%, fail / pass (bounds 9.04 / 10.57%) |
| T6: 1-year median in year 30 (1.31 to 3.35%) | 3.09% | 3.07%, pass |
| T6: 20-year median in year 30 (3.35 to 4.89%) | 4.83% | 4.69%, pass |
| E1: median gross wealth factor in year 30 (9.23) | 9.26 | 9.00 |
| E1: percentiles within 10% of their targets | 40 of 40 | 40 of 40 |

<div class="fs-callout fs-callout--limits" markdown="1">
<p class="fs-callout__title">Where the <code>goes</code> set still misses GOES</p>

- **T4, low for long.** GOES fails it too. A CIR 20-year rate almost never averages below 1.45% for ten years; GOES gets closer with its flooring mechanisms.
- **T1's share of scenarios ever above the cap.** It is 1.5% against a limit of 0.5%, though GOES's own share is 3.06% and the dashboard does not judge it.
- **T5's upper tail** is about 0.1 point short for the 10-year averages; the 30-year averages now clear their bound. The bounds are interpolated at the run's own starting 20-year yield, about 5.1%, not GOES's 5.68%.
- **The first ten years** are narrower than GOES's: the 3-month 99th percentile is 13.2% against 14.1% in year 10. One CIR factor per tenor cannot widen the early years without overshooting year 30, and NAIC publishes neither a two-factor specification nor its parameters.
- **Corporate bond funds** (C1) are not modeled.
</div>

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">3</span></summary>

- Breeden, D.T., Litzenberger, R.H. (1978). "Prices of State-Contingent Claims Implicit in Option Prices." The Journal of Business, 51(4), 621-651. [doi.org](https://doi.org/10.1086/296025){:target="_blank"}
- Dickerson, A., Robotti, C., Rossetti, G. Open Source Bond Asset Pricing: TRACE corporate bond data. [openbondassetpricing.com](https://openbondassetpricing.com/){:target="_blank"}
- NAIC (2026). "Valuation Manual", 1 January 2026 edition: VM-20 Section 7.G and Appendix 1; VM-21 Section 8. [content.naic.org](https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf){:target="_blank"}

</details>
