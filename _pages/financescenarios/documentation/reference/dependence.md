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

Ties the factors together: measures how every factor has moved alongside every other one, and turns that into the
correlation matrix the simulation uses to draw linked random shocks.

In a scenario where inflation surprises on the upside, you also want the interest rate, equity and unemployment
moves that have historically come with high inflation, not a random mix. A correlation matrix holds that: entry
(i, j) is a number between -1 and 1 that says how strongly factors i and j move together (1 fully together, -1
fully opposite, 0 no linear link). It is estimated from each factor's historical changes (rate changes, equity log
returns), taken from the data each factor already fetched. It runs inside `Scenarios.calibrate()` and
`Scenarios.simulate()`, so most users only meet its result, `CalibrationResult.correlation_matrix`.

Building the matrix takes three steps:

1. Estimate. By default each pair of factors is correlated over the dates the two share, at the coarser of their
   two frequencies, so a short history only weakens its own pairs (`calibrate_pairwise`). The alternative cuts
   every factor to the one window they all share (`calibrate`).
2. Shrink. With many factors and few shared observations, sample correlations get noisy, so the matrix is blended
   toward one where every pair has the average correlation, as in
   [Ledoit & Wolf (2004)](http://www.ledoit.net/Honey_2004.pdf), by 10% by default. With `auto` the blend is chosen
   from the data instead, toward no correlation, following
   [Schafer and Strimmer (2005)](https://doi.org/10.2202/1544-6115.1175).
3. Repair. A matrix pieced together from different windows may not be a valid correlation matrix, one where no mix
   of factors has a negative variance. It is moved to the nearest valid one with
   [Higham's (2002)](https://doi.org/10.1093/imanum/22.3.329) method; a valid matrix comes back unchanged.

The matrix describes average co-movement only. Whether extreme moves tend to arrive together is set by
`engine.shock_distribution`: `gaussian` (default) or `student_t`, a t-copula
([Demarta & McNeil, 2005](https://doi.org/10.1111/j.1751-5823.2005.tb00254.x)) that makes joint extremes more
likely. Correlations stay constant over the horizon.

| Key (`engine` in a settings profile) | Default | Meaning |
|:----|:--------|:--------|
| `engine.correlation_method` | `pairwise` | `pairwise` (`calibrate_pairwise`) or `complete_case` (`calibrate`). |
| `engine.shock_distribution` | `gaussian` | `gaussian` or `student_t`: which distribution the matrix correlates. |
| `engine.degrees_of_freedom` | `5.0` | Student-t degrees of freedom; lower means fatter, more joint tails. |
| `engine.correlation_shrinkage` | `0.1` | A share in [0, 1] toward the mean correlation, or `auto` (data-driven). |

**References:**

- Ledoit, O., Wolf, M. (2004). "Honey, I Shrunk the Sample Covariance Matrix." Journal of Portfolio Management, 30(4), 110-119. <http://www.ledoit.net/Honey_2004.pdf>
- Schafer, J., Strimmer, K. (2005). "A Shrinkage Approach to Large-Scale Covariance Matrix Estimation and Implications for Functional Genomics." Statistical Applications in Genetics and Molecular Biology, 4(1). <https://doi.org/10.2202/1544-6115.1175>
- Higham, N.J. (2002). "Computing the Nearest Correlation Matrix: A Problem from Finance." IMA Journal of Numerical Analysis, 22(3), 329-343. <https://doi.org/10.1093/imanum/22.3.329>

## fallback_pairs

```python
dependence.fallback_pairs  # property -> list[str]
```

The "factor_a/factor_b" pairs the last `calibrate_pairwise()` set to zero correlation (assumed unrelated), because
they shared fewer than 5 observations or one side never moved. Always empty after `calibrate()`.

## shrinkage_used

```python
dependence.shrinkage_used  # property -> float | None
```

The shrinkage intensity the last calibration applied (the computed one for "auto").

## repair

```python
dependence.repair  # property -> float | None
```

How far the last calibration's matrix had to move to become a valid correlation matrix (the Frobenius norm, the
size of the change across all entries); 0 when it already was.

## calibrate

```python
calibrate(factor_series: dict[str, pl.Series]) -> pl.DataFrame
```

Build the correlation matrix from series already lined up on one shared set of dates, then shrink and repair it.

This is the `engine.correlation_method: complete_case` route: hand it one equally long history per factor,
covering the same dates, and it returns how strongly each pair has moved together. Every pair uses the same
observations, so the matrix rarely needs repair and no pair falls back to zero. The cost is that one short or
coarse factor shortens the window for every other pair; runs use `calibrate_pairwise` by default.

Also known as: complete-case correlation, listwise deletion.

**Args:**

- <u>factor_series (dict[str, pl.Series]):</u> factor name -> its historical changes (rate changes, equity log returns), all the same length, covering the same dates and without missing values.

**Returns:**

<u>pl.DataFrame:</u> the N x N correlation matrix, a "factor" column plus one column per factor, in input order.

**Raises:**

- <u>ValueError:</u> if fewer than two factors are given, the series differ in length, a series never changes, or the matrix cannot be repaired.
- <u>As an example, with `equities` built as in `calibrate_pairwise`:</u> 
- ```python
- from financescenarios.dependence.dependence_controller import Dependence
- from financescenarios.dependence.dependence_model import align_factor_series_by_date
- <u>aligned, diagnostics = align_factor_series_by_date( {name:</u> equities.changes(name) for name in equities.names}, {name: "monthly" for name in equities.names}
- )
- dependence = Dependence()
- dependence.calibrate(aligned)
- ```
- <u>Which returns (calibrated on 2026-10-04):</u> 
- | factor | us_stocks | us_treasuries | gold |
- <u>&#124;:</u> -------|----------:|--------------:|-----:|
- | us_stocks | 1.0000 | -0.0552 | 0.0934 |
- | us_treasuries | -0.0552 | 1.0000 | 0.2201 |
- | gold | 0.0934 | 0.2201 | 1.0000 |
- All three funds cover the same 261 months, so the result matches `calibrate_pairwise`, as it should.

## calibrate_pairwise

```python
calibrate_pairwise(
    factor_series: dict[str, pl.DataFrame],
    factor_periods: dict[str, str],
) -> pl.DataFrame
```

Build the correlation matrix pair by pair, each pair over the dates the two factors share, then shrink and repair
it. Every `Scenarios` run uses this by default (`engine.correlation_method: pairwise`).

A factor with only a few years of data, such as a young commodity ticker or a quarterly-only country, then weakens
only its own pairs, while two long-history equities still use their full shared history. For each pair, both
series are summed up to the coarser of the two frequencies and matched on calendar date. A pair with fewer than 5
shared observations, or one side that never moves, is set to 0 (assumed unrelated) and listed in `fallback_pairs`.

Also known as: pairwise-complete correlation, pairwise deletion.

**Args:**

- <u>factor_series (dict[str, pl.DataFrame]):</u> factor name -> its historical changes, a `date` and a `value` column, not lined up beforehand.
- <u>factor_periods (dict[str, str]):</u> factor name -> its data frequency: "daily", "weekly", "monthly", "quarterly" or "yearly".

**Returns:**

<u>pl.DataFrame:</u> the N x N correlation matrix, a "factor" column plus one column per factor.

**Raises:**

- <u>ValueError:</u> if fewer than two factors are given, a factor's whole history never changes, or the matrix cannot be repaired.

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

Over 261 monthly returns, US stocks and long Treasuries barely move together (-0.06), while gold leans slightly
toward Treasuries (0.22). These are shrunk 10% toward the average correlation; `Dependence(shrinkage=0)` returns
the raw ones.

## correlation_matrix

```python
dependence.correlation_matrix  # property -> pl.DataFrame
```

The last calibrated correlation matrix: a "factor" column plus one column per factor.

**Raises:**

- <u>RuntimeError:</u> if neither `calibrate()` nor `calibrate_pairwise()` has run yet.

## to_numpy

```python
to_numpy() -> np.ndarray
```

The correlation matrix as a plain N x N NumPy array, the form the simulation draws its shocks with.

**Raises:**

- <u>RuntimeError:</u> if neither `calibrate()` nor `calibrate_pairwise()` has run yet.

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

### build_pairwise_correlation_matrix

```python
build_pairwise_correlation_matrix(
    factor_series: dict[str, pl.DataFrame],
    factor_periods: dict[str, str],
) -> tuple[pl.DataFrame, PairwiseAlignmentDiagnostics]
```

Build the cross-factor correlation matrix from pairwise-complete observations: each pair's
correlation comes from that pair's own calendar overlap, resampled to the coarser of its two
periods, instead of first cutting every factor down to one shared window
(`align_factor_series_by_date` plus `build_correlation_matrix`, the complete-case
alternative). One short-history or coarse-period factor, such as a new credit bucket or a
quarterly-only country, then only shortens the pairs it is in.

A matrix built from per-pair windows of different lengths is not guaranteed positive
semi-definite; `nearest_correlation_matrix` repairs it downstream in `Dependence.calibrate()`.

The formula is as follows:

$$
r_{ij} = (n \cdot S_{xy} - S_{x} \cdot S_{y}) / \sqrt{(n \cdot S_{xx} - S_{x} ^{2}) \cdot (n \cdot S_{yy} - S_{y} ^{2})}
$$

Where n is the pair's overlap and S_x, S_y, S_xx, S_yy, S_xy the sums of x, y, x^2, y^2 and
x * y over it. Pairs with fewer than 5 overlapping observations, or constant over the overlap,
are set to 0.0 and listed in the diagnostics.

**Args:**

- <u>factor_series (dict[str, pl.DataFrame]):</u> factor name -> two-column frame (`date`: pl.Date, `value`: f64), sorted ascending, no nulls; the same shape align_factor_series_by_date() takes.
- <u>factor_periods (dict[str, str]):</u> factor name -> that factor's own configured calibration period, same keys as factor_series.

**Returns:**

<u>tuple[pl.DataFrame, PairwiseAlignmentDiagnostics]:</u> an N x N correlation matrix (a "factor" column plus one numeric column per factor, same shape build_correlation_matrix() returns) and alignment diagnostics.

**Raises:**

- <u>ValueError:</u> if factor_series has fewer than 2 factors, or any factor's own full history (at its own period, never truncated by another factor) is constant: a genuine data problem, not an alignment artifact.

### optimal_shrinkage_intensity

```python
optimal_shrinkage_intensity(
    matrix: np.ndarray,
    factor_names: list[str],
    pair_overlaps: dict[str, int],
) -> float
```

The data-driven shrinkage intensity of Schafer and Strimmer (2005) for a correlation matrix
shrunk toward the identity: the summed estimation variance of
the off-diagonal correlations over their summed squares, capped at 1. Pairs estimated from few
observations have a large variance and so pull the intensity up.

The formula is as follows:

$$
\lambda = \min(1,\; \operatorname{sum}(\operatorname{Var}(r_{ij})) / \operatorname{sum}(r_{ij} ^{2}))
$$

$$
\operatorname{Var}(r_{ij}) = (1 - r_{ij} ^{2}) ^{2} / (n_{ij} - 1)
$$

Where r_ij is the correlation of pair (i, j), n_ij that pair's own overlap, and Var(r_ij) the
large-sample variance of a Pearson correlation.

**Args:**

- <u>matrix (np.ndarray):</u> the sample correlation matrix.
- <u>factor_names (list[str]):</u> the matrix's row and column order.
- <u>pair_overlaps (dict[str, int]):</u> "a/b" -> the number of observations that pair was estimated from.

**Returns:**

<u>float:</u> the intensity in [0, 1].

**References:**

- Schafer, J., Strimmer, K. (2005). "A Shrinkage Approach to Large-Scale Covariance Matrix Estimation and Implications for Functional Genomics." Statistical Applications in Genetics and Molecular Biology, 4(1). <https://doi.org/10.2202/1544-6115.1175>

### shrink_correlation_matrix

```python
shrink_correlation_matrix(matrix: np.ndarray, shrinkage: float = 0.1) -> np.ndarray
```

Linearly shrink a sample correlation matrix toward a constant-correlation target (Ledoit and
Wolf, 2004): with many factors and few overlapping observations, sample correlations are
noisy, and shrinkage trades a little bias for much less estimation variance and a
better-conditioned matrix for the Cholesky step. The intensity here is fixed, not Ledoit and
Wolf's data-driven optimum (see `optimal_shrinkage_intensity` for that toward the identity).

The formula is as follows:

$$
\text{R\_shrunk} = (1 - \delta) \cdot R + \delta \cdot F
$$

$$
F_{ij} = \operatorname{mean}(R_{kl} \;\text{for}\; k \neq l) \text{for}\; i \neq j,\;\; F_{ii} = 1
$$

Where R is the sample correlation matrix and delta the shrinkage intensity.

**Args:**

- <u>matrix (np.ndarray):</u> a symmetric sample correlation matrix, unit diagonal.
- <u>shrinkage (float):</u> shrinkage intensity in [0, 1]; 0 leaves matrix unchanged, 1 replaces it entirely with the constant-correlation target.

**Returns:**

<u>np.ndarray:</u> the shrunk correlation matrix, symmetric with unit diagonal; not guaranteed positive semi-definite on its own, so it should still be passed through nearest_correlation_matrix() afterward, same as an unshrunk sample matrix would be.

**Raises:**

- <u>ValueError:</u> if shrinkage is not in [0, 1].

**References:**

- Ledoit, O., Wolf, M. (2004). "Honey, I Shrunk the Sample Covariance Matrix." Journal of Portfolio Management, 30(4), 110-119. <https://doi.org/10.3905/jpm.2004.110>

### nearest_correlation_matrix

```python
nearest_correlation_matrix(
    matrix: np.ndarray,
    max_iterations: int = 100,
    tolerance: float = 1e-08,
) -> np.ndarray
```

Repair a matrix that should be a correlation matrix but may not be positive semi-definite
(e.g. one assembled pair by pair from different overlaps) into the nearest valid one, via
Higham's (2002) alternating projections with Dykstra's correction. Eigenvalues are floored at
a small positive value rather than 0, because the Cholesky step downstream needs a strictly
positive-definite matrix.

The formula is as follows:

$$
R_{k} = \text{Y\_k-1} - \text{dS\_k-1}
$$

$$
X_{k} = P_{S}(R_{k}) = Q \cdot \max(\text{Lambda},\; \text{floor}) \cdot Q'
$$

$$
\text{dS}_{k} = X_{k} - R_{k}
$$

$$
Y_{k} = P_{U}(X_{k}),\;\; \text{X\_k with its diagonal set to 1}
$$

Where Q * Lambda * Q' is the eigendecomposition of R_k, P_S the projection onto PSD matrices
and P_U onto unit-diagonal ones. Iteration stops once the Frobenius change in Y falls below
`tolerance`, or warns after `max_iterations`. A valid input comes back unchanged; a repair is
logged with its size. If Cholesky still rejects the result, it is blended toward the identity
in growing steps until accepted.

**Args:**

- <u>matrix (np.ndarray):</u> a symmetric matrix with unit diagonal that may not be PSD.
- <u>max_iterations (int):</u> maximum alternating-projection iterations.
- <u>tolerance (float):</u> convergence tolerance on the Frobenius norm change per iteration.

**Returns:**

<u>np.ndarray:</u> the nearest valid correlation matrix (symmetric, strictly positive-definite, unit diagonal).

**Raises:**

- <u>ValueError:</u> if even a 90% blend toward the identity matrix is not strictly positive-definite (a fundamentally, not marginally, invalid input).

**References:**

- Higham, N.J. (2002). "Computing the Nearest Correlation Matrix: A Problem from Finance." IMA Journal of Numerical Analysis, 22(3), 329-343. <https://doi.org/10.1093/imanum/22.3.329>
