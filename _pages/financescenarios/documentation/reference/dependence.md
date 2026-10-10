---
title: "Dependence"
seo_title: "Dependence Reference – Finance Scenarios"
excerpt: "The correlation matrix that links every factor: estimation, shrinkage and repair."
description: "The correlation matrix that links every factor: estimation, shrinkage and repair."
author_profile: false
permalink: /projects/financescenarios/docs/reference/dependence
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

The correlation matrix that links every factor: estimation, shrinkage and repair. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.dependence.dependence_controller import Dependence
```

```python
Dependence(shrinkage: float | str = 0.1)
```

The Dependence module ties the factors together: it measures how every calibrated factor
has historically moved alongside every other one, and turns that into the correlation
matrix the simulation engine uses to draw linked random shocks. Without it, interest
rates, inflation, equities and unemployment would each be simulated on their own.

In plain terms: in a simulated scenario where inflation surprises on the upside, you also
want to see the interest rate, equity and unemployment moves that have historically come
with high inflation, not a random mix. This module makes that happen. It runs
automatically inside `Scenarios.calibrate()`/`Scenarios.simulate()`, so most users only
meet its result: `CalibrationResult.correlation_matrix` (and its `.plot_correlation_matrix()`).

A correlation matrix is a table where entry (i, j) is the correlation between factor i
and factor j: a number between -1 and 1 that says how strongly two series move together,
1 meaning perfectly together, -1 perfectly opposite and 0 no linear relationship. Every
always-on factor (each interest rate, inflation, equity and unemployment entry) is in it,
and so is every opt-in factor that is enabled or configured (`yield_curve`'s three
factors, `real_estate`, every `credit` entry, `leading_indicator`, every `fx` entry, and
so on). The broad factor set's 23 equity "clouds" alone already make it far larger than
the 4 x 4 a single-equity setup produces, but it is built and repaired the same way at
any size. The correlations are estimated from each factor's own historical *changes*
(short-rate changes, inflation changes, equity log-returns, unemployment-rate changes),
taken from the data each factor controller already fetched, so no second download is made.

Building the matrix takes three steps:

1. Estimate. By default (`calibrate_pairwise`, `engine.correlation_method: pairwise`)
   each pair of factors is correlated over just the calendar dates the two have in
   common, at the coarser of their two frequencies, so a factor with a short history only
   weakens the pairs it is part of. The alternative (`calibrate`,
   `engine.correlation_method: complete_case`) first cuts every factor down to the one
   window they all share and correlates them together. Series are always lined up by
   *date*, never by position, so daily rates, yearly inflation and monthly equities are
   first summed up to the coarser period and then matched on the calendar.
2. Shrink. Plain (Pearson) sample correlation gets noisy once the number of factors is
   large compared with the number of overlapping observations, a real risk with many
   equity, fx and credit entries. The sample matrix is blended toward a
   constant-correlation target, every off-diagonal entry replaced by the average pairwise
   correlation, as in [Ledoit & Wolf (2004)](http://www.ledoit.net/Honey_2004.pdf): a
   little bias for a large drop in estimation noise, and a better-conditioned matrix for
   the Cholesky decomposition that follows. The blend weight `shrinkage` is fixed
   (default 0.1). With `engine.correlation_shrinkage: auto` it is chosen from the data instead: the
   [Schafer and Strimmer (2005)](https://doi.org/10.2202/1544-6115.1175) intensity, toward no correlation,
   larger when correlations rest on few observations. Trained on the broad factor set's history before
   2012 or 2016 and scored on the years after, it cut the correlation error by 7.5% and 1.6%.
3. Repair. A matrix assembled from series of different frequencies, or from per-pair
   windows of different lengths, may not be positive semi-definite: the property that no
   combination of the correlated factors can have a negative variance. The Cholesky
   decomposition used downstream to generate correlated shocks needs it (strictly,
   positive *definite*). The matrix is moved to the nearest valid correlation matrix with
   [Higham's (2002)](https://doi.org/10.1093/imanum/22.3.329) alternating-projections
   algorithm. This is a numerical safeguard, not a modelling choice: a valid matrix comes
   back unchanged.

The matrix is always a *linear* correlation structure: it says how strongly two factors'
changes move together on average, nothing about whether their most extreme moves tend to
coincide. Which distribution it then correlates is a separate engine setting:
`engine.shock_distribution: gaussian` (the default) correlates normally distributed
shocks, under which joint extreme moves are never more likely than a Gaussian implies;
`student_t` correlates a multivariate Student-t distribution with the same matrix, a
t-copula ([Demarta & McNeil, 2005](https://doi.org/10.1111/j.1751-5823.2005.tb00254.x)),
adding genuine tail dependence (extremes that tend to arrive together), not just fatter
tails per factor. Correlating the random shocks of several factors this way follows the
multi-factor models of Wilkie (1986) and Ahlgrim, D'Arcy & Gorvett (2005), both linked
under References.

There is no data source of its own: the inputs are the dated change series every factor
controller exposes through its `changes`. Pairwise correlation is computed with Polars'
own Pearson correlation, the same plain calculation Finance Toolkit's
`get_correlation_matrix()` delegates to, so the data never leaves Polars/NumPy.

What it does not do: asymmetric or pair-specific tail behavior that a single shared
t-copula parameter cannot express, such as the patchwork copulas of
[Pfeifer & Ragulina (2021)](https://doi.org/10.1515/demo-2021-0115) or the dependent
Conditional-VaR of [Josaphat & Syuhada (2020)](https://arxiv.org/abs/2009.02904); those
remain natural next steps. Correlations are also constant over the simulation horizon.

Configuration (`engine` in a settings profile; the dependence step has no factor-set keys):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `engine.correlation_method` | `pairwise` | `pairwise` (`calibrate_pairwise`) or `complete_case` (`calibrate`). |
| `engine.shock_distribution` | `gaussian` | `gaussian` or `student_t`: which distribution the matrix correlates. |
| `engine.degrees_of_freedom` | `5.0` | Student-t degrees of freedom; lower means fatter, more joint tails. |
| `engine.correlation_shrinkage` | `0.1` | A share in [0, 1] toward the mean correlation, or `auto` (data-driven). |

`Scenarios` builds `Dependence(shrinkage=engine.correlation_shrinkage)` for every calibration and records
the intensity used and the repair size on the result (`correlation_shrinkage`, `correlation_repair`).

**References:**

- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>
- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the CAS, 92. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Ledoit, O., Wolf, M. (2004). "Honey, I Shrunk the Sample Covariance Matrix." Journal of Portfolio Management, 30(4), 110-119. <http://www.ledoit.net/Honey_2004.pdf>
- Schafer, J., Strimmer, K. (2005). "A Shrinkage Approach to Large-Scale Covariance Matrix Estimation and Implications for Functional Genomics." Statistical Applications in Genetics and Molecular Biology, 4(1). <https://doi.org/10.2202/1544-6115.1175>
- Higham, N.J. (2002). "Computing the Nearest Correlation Matrix: A Problem from Finance." IMA Journal of Numerical Analysis, 22(3), 329-343. <https://doi.org/10.1093/imanum/22.3.329>
- Demarta, S., McNeil, A.J. (2005). "The t Copula and Related Copulas." International Statistical Review, 73(1), 111-129. <https://doi.org/10.1111/j.1751-5823.2005.tb00254.x>
- Pfeifer, D., Ragulina, O. (2021). "Generating Unfavourable VaR Scenarios under Solvency II with Patchwork Copulas." Dependence Modeling, 9, 327-346. <https://doi.org/10.1515/demo-2021-0115>
- Josaphat, B., Syuhada, K. (2020). "Dependent Conditional Value-at-Risk for Aggregate Risk Models." arXiv:2009.02904. <https://arxiv.org/abs/2009.02904>

## fallback_pairs

```python
dependence.fallback_pairs  # property -> list[str]
```

Pairs the last calibrate_pairwise() call defaulted to 0.0 (assumed
uncorrelated) for lack of a reliable overlap; see
dependence_model.build_pairwise_correlation_matrix()'s own docstring.
Always empty after calibrate() (the complete-case path has no such
fallback: every pair either has a real estimate or the whole calibration
fails outright), and before either has been called.

## shrinkage_used

```python
dependence.shrinkage_used  # property -> float | None
```

The shrinkage intensity the last calibration applied (the computed one for "auto").

## repair

```python
dependence.repair  # property -> float | None
```

How far the last calibration's shrunk matrix moved to become valid (Frobenius norm; 0 if it was).

## calibrate

```python
calibrate(factor_series: dict[str, pl.Series]) -> pl.DataFrame
```

Build the cross-factor correlation matrix from series that are already aligned onto
one shared set of dates (complete-case estimation), then shrink it and repair it into
a valid correlation matrix.

In plain terms: hand it one equally long history per factor, covering the same
periods, and it returns how strongly each pair has moved together, cleaned up so the
simulation engine can use it. This is the `engine.correlation_method: complete_case`
path; every real run uses `calibrate_pairwise` by default, and this method remains
for direct use and for that setting.

Because every entry comes from the same underlying observations, the sample matrix is
positive semi-definite by construction and rarely needs repair, and there are never
fallback pairs (`fallback_pairs` is reset to empty). The cost is that one
short-history or coarse-period factor shrinks the window every other pair is
estimated from. The series are typically produced by
`dependence_model.align_factor_series_by_date`, which sums every factor's changes up
to the coarsest period in play and inner-joins them on calendar date.

Also known as: complete-case correlation, listwise-deletion correlation matrix.

**Args:**

- <u>factor_series (dict[str, pl.Series]):</u> factor name -> aligned historical series (e.g. short-rate changes, inflation changes, equity log-returns), all the same length and covering the same dates.

**Returns:**

<u>pl.DataFrame:</u> the validated N x N correlation matrix, shrunk (see __init__) and PSD-repaired if needed: a `factor` column plus one numeric column per factor, in input order.

**Raises:**

- <u>ValueError:</u> if fewer than two factors are supplied, the series are not all the same length, a series is constant (zero variance), `shrinkage` is outside [0, 1], or the matrix cannot be repaired into a strictly positive-definite one.

**Notes:**

- A warning is logged when there are fewer than 3 x N^2 observations for N
  factors (the estimate may be noisy), and when a pair's correlation exceeds 0.98
  in absolute value, which usually means the same driver is configured twice.
- The input series must be free of nulls; every controller's `changes` already is.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.dependence.dependence_controller import Dependence
from financescenarios.dependence.dependence_model import align_factor_series_by_date
from financescenarios.factors.equities.equities_controller import Equities

toolkit = Toolkit(
    ["SPY", "TLT", "GLD"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2005-01-01", benchmark_ticker=None
)
equities = Equities(toolkit)
equities.calibrate("us_stocks", "SPY", period="monthly")
equities.calibrate("us_treasuries", "TLT", period="monthly")
equities.calibrate("gold", "GLD", period="monthly")

aligned, diagnostics = align_factor_series_by_date(
    {name: equities.changes(name) for name in equities.names}, {name: "monthly" for name in equities.names}
)
dependence = Dependence()
dependence.calibrate(aligned)
```

Which returns (calibrated on 2026-10-04):

| factor | us_stocks | us_treasuries | gold |
|:-------|----------:|--------------:|-----:|
| us_stocks | 1.0000 | -0.0552 | 0.0934 |
| us_treasuries | -0.0552 | 1.0000 | 0.2201 |
| gold | 0.0934 | 0.2201 | 1.0000 |

All three ETFs have the same 261 monthly returns (February 2005 to October 2026), so
`diagnostics.aligned_length` is 261 and nothing is lost to alignment. The result is
identical to the `calibrate_pairwise` example, as it should be when every factor
covers the same dates.

**References:**

- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>
- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the CAS, 92. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Ledoit, O., Wolf, M. (2004). "Honey, I Shrunk the Sample Covariance Matrix." Journal of Portfolio Management, 30(4), 110-119. <http://www.ledoit.net/Honey_2004.pdf>
- Higham, N.J. (2002). "Computing the Nearest Correlation Matrix: A Problem from Finance." IMA Journal of Numerical Analysis, 22(3), 329-343. <https://doi.org/10.1093/imanum/22.3.329>

## calibrate_pairwise

```python
calibrate_pairwise(
    factor_series: dict[str, pl.DataFrame],
    factor_periods: dict[str, str],
) -> pl.DataFrame
```

Build the cross-factor correlation matrix with pairwise-complete estimation, then
shrink it and repair it into a valid correlation matrix. This is the default path
every `Scenarios` run uses (`engine.correlation_method: pairwise`).

In plain terms: each pair of factors is correlated over just the dates the two have
in common, so a factor with only a few years of data (a new credit bucket, a young
commodity ticker, a quarterly-only country) weakens only the correlations it is part
of. Two long-history equities still correlate over their full shared history.

For every pair, both series are summed up to the coarser of the two factors' own
periods (daily rate changes become yearly sums when paired with yearly inflation)
and inner-joined on calendar date. A pair with fewer than 5 overlapping observations,
or one side constant within the overlap, cannot be estimated reliably (with 2 points a
correlation is forced to exactly +1 or -1), so it is set to 0.0, assumed uncorrelated,
and listed in `fallback_pairs`. A matrix built from windows of different lengths is
not guaranteed positive semi-definite, which is what the Higham repair step that
follows is for.

Also known as: pairwise-complete correlation, pairwise deletion.

**Args:**

- <u>factor_series (dict[str, pl.DataFrame]):</u> factor name -> two-column frame (`date`: pl.Date, `value`: f64), *not* pre-aligned; each controller's own changes()/changes property already returns this shape, the same input align_factor_series_by_date() takes.
- <u>factor_periods (dict[str, str]):</u> factor name -> that factor's own configured calibration period ("daily", "weekly", "monthly", "quarterly" or "yearly"), same keys as factor_series.

**Returns:**

<u>pl.DataFrame:</u> the validated N x N correlation matrix, shrunk and PSD-repaired if needed; the same shape calibrate() returns.

**Raises:**

- <u>ValueError:</u> if fewer than two factors are supplied, a factor's own full history is constant (a real data problem, not an alignment artifact), `shrinkage` is outside [0, 1], or the matrix cannot be repaired into a strictly positive-definite one.

**Notes:**

- Warnings are logged for fallback pairs, for pairs estimated from fewer than 12
  overlapping observations, and for pairs whose correlation exceeds 0.98 in absolute
  value (usually the same ticker configured twice). Long pair lists are capped at 12
  names with an "and N more" tail.
- The shortest factor history is logged at DEBUG level, for a quick view of which
  factor is most data-limited.
- Summing changes to a coarser period is correct because every factor's `changes`
  are additive increments (rate differences, log-returns), the same way twelve
  monthly log-returns add up to the annual one.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.dependence.dependence_controller import Dependence
from financescenarios.factors.equities.equities_controller import Equities

toolkit = Toolkit(
    ["SPY", "TLT", "GLD"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2005-01-01", benchmark_ticker=None
)
equities = Equities(toolkit)
equities.calibrate("us_stocks", "SPY", period="monthly")
equities.calibrate("us_treasuries", "TLT", period="monthly")
equities.calibrate("gold", "GLD", period="monthly")

dependence = Dependence()
dependence.calibrate_pairwise(
    {name: equities.changes(name) for name in equities.names}, {name: "monthly" for name in equities.names}
)
```

Which returns (calibrated on 2026-10-04):

| factor | us_stocks | us_treasuries | gold |
|:-------|----------:|--------------:|-----:|
| us_stocks | 1.0000 | -0.0552 | 0.0934 |
| us_treasuries | -0.0552 | 1.0000 | 0.2201 |
| gold | 0.0934 | 0.2201 | 1.0000 |

Over 261 monthly returns, US stocks and long Treasuries barely move together
(-0.06), while gold leans slightly toward Treasuries (0.22). These are the shrunk
values: the raw sample correlations were -0.0709, 0.0942 and 0.2350, each moved 10%
of the way toward their average of 0.0861 (`Dependence(shrinkage=0)` returns the raw
ones). `fallback_pairs` is empty, since every pair shares all 261 months.

**References:**

- Ledoit, O., Wolf, M. (2004). "Honey, I Shrunk the Sample Covariance Matrix." Journal of Portfolio Management, 30(4), 110-119. <http://www.ledoit.net/Honey_2004.pdf>
- Higham, N.J. (2002). "Computing the Nearest Correlation Matrix: A Problem from Finance." IMA Journal of Numerical Analysis, 22(3), 329-343. <https://doi.org/10.1093/imanum/22.3.329>

## correlation_matrix

```python
dependence.correlation_matrix  # property -> pl.DataFrame
```

The last-calibrated, PSD-validated correlation matrix.

**Raises:**

- <u>RuntimeError:</u> if calibrate() hasn't been called yet.

## to_numpy

```python
to_numpy() -> np.ndarray
```

The correlation matrix as a plain N x N NumPy array, for Cholesky decomposition.

**Raises:**

- <u>RuntimeError:</u> if calibrate() hasn't been called yet.
