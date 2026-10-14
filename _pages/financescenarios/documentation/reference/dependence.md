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

The correlation matrix that links every factor: estimation, shrinkage and repair.

```python
from financescenarios.dependence.dependence_controller import Dependence
```

Ties the factors together: measures how every factor has moved alongside every other one, and turns that into the
correlation matrix the simulation uses to draw linked random shocks.

In a scenario where inflation surprises on the upside, you also want the interest rate, equity and unemployment
moves that have historically come with high inflation, not a random mix. A correlation matrix holds that: entry (i,
j) is a number between -1 and 1 that says how strongly factors i and j move together (1 fully together, -1 fully
opposite, 0 no linear link). It is estimated from each factor's historical changes (rate changes, equity log
returns), not levels, since two persistent levels can look related by chance alone. Every run builds it, so most
users only meet its result, `CalibrationResult.correlation_matrix`. The matrix is what makes diversification in the
scenarios realistic: a portfolio's spread of outcomes depends on how its assets move together, not just on how much
each one moves.

Building the matrix takes three steps:

1. Estimate. By default each pair of factors is correlated over the dates the two share, at the coarser of their
   two frequencies, so a short history only weakens its own pairs (`calibrate_pairwise`). The alternative cuts
   every factor to the one window they all share (`calibrate`).
2. Shrink. With many factors and few shared observations, sample correlations get noisy, so by default every
   correlation is pulled toward zero by an intensity chosen from the data, following
   [Schafer and Strimmer (2005)](https://doi.org/10.2202/1544-6115.1175), whose target D shrinks the
   off-diagonal entries to zero (section 3): the shorter the shared history, the stronger the pull. A fixed
   share instead blends toward the average correlation, as in
   [Ledoit & Wolf (2004)](http://www.ledoit.net/Honey_2004.pdf), a target they built for stocks and rule out for
   assets from different classes such as stocks and bonds (footnote 4), which is what a factor set of rates,
   inflation, equities and currencies is.
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
| `engine.degrees_of_freedom` | `12.0` | Student-t degrees of freedom; lower means fatter, more joint tails. |
| `engine.correlation_shrinkage` | `auto` | `auto` (data-driven, toward zero) or a share in [0, 1] toward the mean. |

**References:**

- Ledoit, O., Wolf, M. (2004). "Honey, I Shrunk the Sample Covariance Matrix." Journal of Portfolio Management, 30(4), 110-119. <http://www.ledoit.net/Honey_2004.pdf>
- Schafer, J., Strimmer, K. (2005). "A Shrinkage Approach to Large-Scale Covariance Matrix Estimation and Implications for Functional Genomics." Statistical Applications in Genetics and Molecular Biology, 4(1). <https://doi.org/10.2202/1544-6115.1175>
- Higham, N.J. (2002). "Computing the Nearest Correlation Matrix: A Problem from Finance." IMA Journal of Numerical Analysis, 22(3), 329-343. <https://doi.org/10.1093/imanum/22.3.329>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Dependence(shrinkage: float | str = 'auto')
```

</details>

## fallback_pairs

The "factor_a/factor_b" pairs the last `calibrate_pairwise()` set to zero correlation (assumed unrelated), because
they shared fewer than 5 observations or one side never moved. Always empty after `calibrate()`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
dependence.fallback_pairs  # property -> list[str]
```

</details>

## shrinkage_used

The shrinkage intensity the last calibration applied (the computed one for "auto").

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
dependence.shrinkage_used  # property -> float | None
```

</details>

## repair

How far the last calibration's matrix had to move to become a valid correlation matrix (the Frobenius norm, the
size of the change across all entries); 0 when it already was.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
dependence.repair  # property -> float | None
```

</details>

## calibrate

Build the correlation matrix from series already lined up on one shared set of dates, then shrink and repair it.

This is `engine.correlation_method: complete_case`: every factor contributes the same dates, and the result
says how strongly each pair has moved together over that common window. Every pair uses the same
observations, so the matrix rarely needs repair and no pair falls back to zero. The cost is that one short or
coarse factor shortens the window for every other pair; runs use `calibrate_pairwise` by default.

**As an example:**

With `equities` built as in `calibrate_pairwise`.

```python
from financescenarios.dependence.dependence_controller import Dependence
from financescenarios.dependence.dependence_model import align_factor_series_by_date

aligned, diagnostics = align_factor_series_by_date(
    {name: equities.changes(name) for name in equities.names}, {name: "monthly" for name in equities.names}
)
dependence = Dependence()
dependence.calibrate(aligned)
```

Which returns (calibrated on 2026-10-14):

| factor | us_stocks | us_treasuries | gold |
|:-------|----------:|--------------:|-----:|
| us_stocks | 1.0000 | -0.0594 | 0.0790 |
| us_treasuries | -0.0594 | 1.0000 | 0.1973 |
| gold | 0.0790 | 0.1973 | 1.0000 |

All three funds cover the same 261 months, so the result matches `calibrate_pairwise`, as it should.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(factor_series: dict[str, pl.Series]) -> pl.DataFrame
```

**Args:**

- <u>factor_series (dict[str, pl.Series]):</u> factor name -> its historical changes (rate changes, equity log returns), all the same length, covering the same dates and without missing values.

**Returns:**

<u>pl.DataFrame:</u> the N x N correlation matrix, a "factor" column plus one column per factor, in input order.

**Raises:**

- <u>ValueError:</u> if fewer than two factors are given, the series differ in length, a series never changes, or the matrix cannot be repaired.

</details>

## calibrate_pairwise

Build the correlation matrix pair by pair, each pair over the dates the two factors share, then shrink and repair
it. This is the default for every run (`engine.correlation_method: pairwise`).

A factor with only a few years of data, such as a young commodity ticker or a quarterly-only country, then weakens
only its own pairs, while two long-history equities still use their full shared history. For each pair, both
series are summed up to the coarser of the two frequencies and matched on calendar date. A pair with fewer than 5
shared observations, or one side that never moves, is set to 0 (assumed unrelated) and listed in `fallback_pairs`.

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

Which returns (calibrated on 2026-10-14):

| factor | us_stocks | us_treasuries | gold |
|:-------|----------:|--------------:|-----:|
| us_stocks | 1.0000 | -0.0594 | 0.0790 |
| us_treasuries | -0.0594 | 1.0000 | 0.1973 |
| gold | 0.0790 | 0.1973 | 1.0000 |

Over 261 monthly returns, US stocks and long Treasuries barely move together (-0.06), while gold leans slightly
toward Treasuries (0.20). The data set the pull toward zero at 16% (`shrinkage_used`), from raw correlations of
-0.07, 0.09 and 0.23; `Dependence(shrinkage=0)` returns the raw ones.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_pairwise(
    factor_series: dict[str, pl.DataFrame],
    factor_periods: dict[str, str],
) -> pl.DataFrame
```

**Args:**

- <u>factor_series (dict[str, pl.DataFrame]):</u> factor name -> its historical changes, a `date` and a `value` column, not lined up beforehand.
- <u>factor_periods (dict[str, str]):</u> factor name -> its data frequency: "daily", "weekly", "monthly", "quarterly" or "yearly".

**Returns:**

<u>pl.DataFrame:</u> the N x N correlation matrix, a "factor" column plus one column per factor.

**Raises:**

- <u>ValueError:</u> if fewer than two factors are given, a factor's whole history never changes, or the matrix cannot be repaired.

</details>

## correlation_matrix

The last calibrated correlation matrix: a "factor" column plus one column per factor.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
dependence.correlation_matrix  # property -> pl.DataFrame
```

**Raises:**

- <u>RuntimeError:</u> if neither `calibrate()` nor `calibrate_pairwise()` has run yet.

</details>

## to_numpy

The correlation matrix as a plain N x N NumPy array, the form the simulation draws its shocks with.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
to_numpy() -> np.ndarray
```

**Raises:**

- <u>RuntimeError:</u> if neither `calibrate()` nor `calibrate_pairwise()` has run yet.

</details>

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

### build_pairwise_correlation_matrix

Build the correlation matrix pair by pair: each pair of factors is correlated over the dates the two have in
common, at the coarser of their two frequencies, rather than cutting every factor down to one shared window.

This is the practice Higham (2002, section 1) describes for stock correlations, each pair using only the days on
which both stocks have data, followed by a repair to the nearest valid matrix. Histories
differ a lot in length: an equity index goes back decades, a credit bucket or a quarterly-only country a few
years. Using each pair's own overlap means one short or coarse factor only weakens the correlations it is
part of, while two long-history factors keep their full shared record, so long-run relationships (stocks versus
bonds, rates versus inflation) are estimated on as much data as exists. The price is that a matrix built from
windows of different lengths need not be a valid correlation matrix, so it is repaired afterwards with
`nearest_correlation_matrix`.

The formula is as follows:

$$
r_{ij} = (n \cdot S_{xy} - S_{x} \cdot S_{y}) / \sqrt{(n \cdot S_{xx} - S_{x} ^{2}) \cdot (n \cdot S_{yy} - S_{y} ^{2})}
$$

Where n is the pair's overlap and S_x, S_y, S_xx, S_yy, S_xy the sums of x, y, x^2, y^2 and
x * y over it. Pairs with fewer than 5 overlapping observations, or constant over the overlap,
are set to 0.0 and listed in the diagnostics: a judgement that no evidence of dependence means none is
simulated, rather than letting a 2- to 4-point estimate swing anywhere between -1 and 1.

**References:**

- Higham, N.J. (2002). "Computing the Nearest Correlation Matrix: A Problem from Finance." IMA Journal of Numerical Analysis, 22(3), 329-343. <https://doi.org/10.1093/imanum/22.3.329>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
build_pairwise_correlation_matrix(
    factor_series: dict[str, pl.DataFrame],
    factor_periods: dict[str, str],
) -> tuple[pl.DataFrame, PairwiseAlignmentDiagnostics]
```

**Args:**

- <u>factor_series (dict[str, pl.DataFrame]):</u> each factor's dated historical changes (rate changes, log returns).
- <u>factor_periods (dict[str, str]):</u> each factor's data frequency, "daily" up to "yearly".

**Returns:**

<u>tuple[pl.DataFrame, PairwiseAlignmentDiagnostics]:</u> the correlation matrix, with a "factor" column and one column per factor, and per pair the number of observations used and any pairs set to zero.

**Raises:**

- <u>ValueError:</u> if fewer than 2 factors are given, or a factor's own full history never changes.

</details>

### optimal_shrinkage_intensity

How far to shrink the correlations toward zero, chosen from the data itself
([Schafer and Strimmer, 2005](https://doi.org/10.2202/1544-6115.1175)): the more uncertain the estimated
correlations are relative to their size, the more they are pulled in.

A correlation estimated from a few years of monthly data is noisy, and a simulation that takes it at face value
builds spurious diversification or concentration into the scenarios. This sets the shrinkage intensity to the
share of the correlations' size that is estimation noise, so pairs with a short overlap push it up and a long,
clean history leaves the matrix close to the sample one. It is what `engine.correlation_shrinkage: auto` uses.
Shrinking toward zero is Schafer and Strimmer's target D (section 3), whose intensity has a simple closed form
(eq. 10): the summed variance of the correlations over their summed squares. Where they estimate each
Var(r_ij) from the data (Appendix A), this uses the large-sample formula below, as pairs differ in overlap.

The formula is as follows:

$$
\lambda = \min(1,\; \operatorname{sum}(\operatorname{Var}(r_{ij})) / \operatorname{sum}(r_{ij} ^{2}))
$$

$$
\operatorname{Var}(r_{ij}) = (1 - r_{ij} ^{2}) ^{2} / (n_{ij} - 1)
$$

Where r_ij is the correlation of pair (i, j), n_ij that pair's own overlap, and Var(r_ij) the
large-sample variance of a Pearson correlation.

**References:**

- Schafer, J., Strimmer, K. (2005). "A Shrinkage Approach to Large-Scale Covariance Matrix Estimation and Implications for Functional Genomics." Statistical Applications in Genetics and Molecular Biology, 4(1). <https://doi.org/10.2202/1544-6115.1175>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
optimal_shrinkage_intensity(
    matrix: np.ndarray,
    factor_names: list[str],
    pair_overlaps: dict[str, int],
) -> float
```

**Args:**

- <u>matrix (np.ndarray):</u> the sample correlation matrix.
- <u>factor_names (list[str]):</u> the factors in the matrix's row and column order.
- <u>pair_overlaps (dict[str, int]):</u> the number of observations behind each pair, keyed "a/b".

**Returns:**

<u>float:</u> the shrinkage intensity, between 0 and 1.

</details>

{% raw %}
### shrink_correlation_matrix

Blend the sample correlation matrix with one in which every pair has the average correlation, as in
[Ledoit and Wolf (2004)](https://doi.org/10.3905/jpm.2004.110).

With many factors and limited history, sample correlations are noisy: some pairs look more related, others less,
than they really are, purely by chance. Pulling every correlation part of the way toward the common average
trades a little bias for much less estimation error, and gives a better-behaved matrix, so the scenarios do not
lean on correlations the data cannot support. The target is Ledoit and Wolf's (section 3.2), which estimates the
common constant correlation as the average of all the sample correlations.

The 10% default is a judgement, not a published value. Ledoit and Wolf derive the optimal intensity from the
data (Appendix B: it behaves asymptotically like a constant over T, so it falls as the history grows), and they
built this target for stocks and rule it out for assets from different classes such as stocks and bonds
(footnote 4). That is why runs default to `engine.correlation_shrinkage: auto`,
which shrinks a mixed set of rates, inflation and equities toward zero correlation by a data-driven intensity
(`optimal_shrinkage_intensity`); this blend is what a fixed share selects.

The formula is as follows:

$$
R_{\text{shrunk}} = (1 - \delta) \cdot R + \delta \cdot F
$$

$$
F_{ij} = \operatorname{mean}(R_{kl} \;\text{for}\; k \neq l) \text{for}\; i \neq j,\;\; F_{ii} = 1
$$

Where R is the sample correlation matrix and delta the shrinkage intensity.

**References:**

- Ledoit, O., Wolf, M. (2004). "Honey, I Shrunk the Sample Covariance Matrix." Journal of Portfolio Management, 30(4), 110-119. <https://doi.org/10.3905/jpm.2004.110>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
shrink_correlation_matrix(matrix: np.ndarray, shrinkage: float = 0.1) -> np.ndarray
```

**Args:**

- <u>matrix (np.ndarray):</u> the sample correlation matrix.
- <u>shrinkage (float):</u> the share in [0, 1] taken from the average-correlation matrix; 0 leaves the sample matrix unchanged, 1 replaces it entirely.

**Returns:**

<u>np.ndarray:</u> the shrunk correlation matrix, which can still need `nearest_correlation_matrix` to be valid.

**Raises:**

- <u>ValueError:</u> if shrinkage is not in [0, 1].

</details>
{% endraw %}

### nearest_correlation_matrix

Repair a correlation matrix that is not internally consistent into the nearest one that is, with
[Higham's (2002)](https://doi.org/10.1093/imanum/22.3.329) alternating projections.

Correlations estimated pair by pair over different windows can contradict each other: A strongly linked to B and
B to C, but A and C unrelated. Such a matrix implies that some portfolio of the factors has a negative variance,
and no set of correlated scenarios can be drawn from it. This finds the valid matrix closest to the estimated one,
so every correlation moves as little as possible; a matrix that is already valid comes back unchanged. All
eigenvalues are kept slightly above zero, so no combination of factors is treated as riskless.

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

Where Q * Lambda * Q' is the eigendecomposition of R_k, P_S the projection onto positive semi-definite matrices
and P_U onto those with a unit diagonal: Higham's Algorithm 3.3, in which dS_k-1 is Dykstra's correction. The
iteration stops once Y changes by less than `tolerance`; the default 1e-8 is the one of his section 4 example,
where Algorithm 3.3 converges in 19 iterations, and 100 rounds leave ample room. In the rare
case the result is still not strictly valid, it is blended toward no correlation in growing steps until it is.

**References:**

- Higham, N.J. (2002). "Computing the Nearest Correlation Matrix: A Problem from Finance." IMA Journal of Numerical Analysis, 22(3), 329-343. <https://doi.org/10.1093/imanum/22.3.329>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
nearest_correlation_matrix(
    matrix: np.ndarray,
    max_iterations: int = 100,
    tolerance: float = 1e-08,
) -> np.ndarray
```

**Args:**

- <u>matrix (np.ndarray):</u> the estimated correlation matrix, symmetric with ones on the diagonal.
- <u>max_iterations (int):</u> the most projection rounds to run.
- <u>tolerance (float):</u> the change between rounds below which the repair stops.

**Returns:**

<u>np.ndarray:</u> the nearest valid correlation matrix.

**Raises:**

- <u>ValueError:</u> if even a 90% blend toward no correlation is not valid, a sign of a fundamentally broken input.

</details>
