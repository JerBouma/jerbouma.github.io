---
title: Dependence
seo_title: "Dependence | Finance Scenarios"
seo_title_suffix: false
excerpt: "How Finance Scenarios ties the factors together: correlated shocks through a Cholesky factor, correlations estimated pairwise and shrunk toward zero, a repaired matrix, and Student-t shocks for joint tails."
description: "Dependence in Finance Scenarios: the Cholesky factor, mixed frequencies and pairwise windows, Schafer-Strimmer shrinkage with a fat-tail-robust variance, Higham's nearest correlation matrix and the Student-t copula."
author_profile: false
permalink: /projects/financescenarios/docs/dependence
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/architecture
redirect_from:
    - /projects/financescenarios/docs/reference/dependence
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-architecture"
---

Fitted one by one, the factors would move independently, and a scenario could combine an equity crash with tightening credit spreads. Where theory says one variable drives another, its simulated path enters the other's equation ([How a Run Is Built](/projects/financescenarios/docs/architecture#dependence)); everything else is tied together by one correlation matrix of the factors' historical shocks. This page covers how that matrix is estimated, made usable and turned into correlated shocks, and how Student-t shocks make extreme moves coincide.

## Correlated Shocks {#correlated-shocks}

Each factor receives one random shock per step and scenario. To give the shocks their historical co-movement, independent standard normal draws $$Z_t$$ are multiplied by the Cholesky factor $$L$$ of the correlation matrix $$R$$, a lower-triangular matrix that acts as its square root:

$$
\varepsilon_t = L\,Z_t, \qquad L L^\top = R
$$

The shocks $$\varepsilon_t$$ have unit variance and exactly the correlations in $$R$$, so a scenario with falling equities tends to show the spread, rate and currency moves that came with falling equities in the past.

## How the Correlations Are Estimated {#how-the-correlations-are-estimated}

The correlation matrix comes from each factor's historical changes: changes in a rate, log returns of a price, and step-to-step changes for year-over-year rates and credit spreads, whatever form the factor is fitted in. Four steps turn them into a matrix:

<ol class="ca-steps">
  <li markdown="span">**Mixed frequencies.** Changes are summed up to the coarser frequency and matched on calendar date, the way twelve monthly log returns add up to a yearly one.</li>
  <li markdown="span">**Pairwise windows.** Each pair uses the dates those two factors share, so a short series only weakens its own pairs. A pair with fewer than 5 shared observations is set to zero; fewer than 12, or a correlation above 0.98 (usually the same series configured twice), is flagged.</li>
  <li markdown="span">**Shrinkage.** Sample correlations are noisy, more so with many factors, so they are pulled toward a simpler target, trading a little bias for much less noise. By default the correlations themselves, not the covariances, are pulled toward zero by an amount estimated from the data, larger when correlations rest on few observations or fat-tailed data (see Shrinkage below). A fixed share instead pulls them toward their average correlation ([Ledoit and Wolf, 2004](http://www.ledoit.net/Honey_2004.pdf){:target="_blank"}), a target built for stocks that suits a mix of rates, inflation, equities and currencies less well.</li>
  <li markdown="span">**Repair.** A matrix built from different windows can be internally inconsistent (not positive definite) and then has no Cholesky factor. When the shrunk matrix is one, the sample matrix is repaired first, moved to the nearest valid correlation matrix, the nearest symmetric positive semidefinite matrix with unit diagonal ([Higham, 2002](https://doi.org/10.1093/imanum/22.3.329){:target="_blank"}), and shrunk after. The other order leaves the matrix nearly singular, as the nearest correlation matrix has a zero eigenvalue for every nonpositive one of the matrix it repairs ([Higham (2002, Theorem 2.5)](https://doi.org/10.1093/imanum/22.3.329){:target="_blank"}). Shrunk after the repair, its smallest eigenvalue is at least the intensity times the target's, by Weyl's inequality ([Horn and Johnson (2013, Theorem 4.3.1)](https://doi.org/10.1017/CBO9781139020411){:target="_blank"}). A matrix that shrinking already makes valid, as in the default calibration, is left as it is. The size of the repair is reported.</li>
</ol>

<div class="fs-callout fs-callout--limits" markdown="1">
<p class="fs-callout__title">Limits</p>

The matrix is linear and constant over the horizon: correlations do not rise in a crisis except through the Student-t shocks and shared equity regimes below.
</div>

## Shrinkage

A correlation estimated on a few years of monthly data is noisy, and a run that takes it at face value builds diversification or concentration into the scenarios that the data never showed. So the calibrated matrix is pulled toward zero, every correlation by the same share $$\lambda$$: $$\tilde r_{ij} = (1 - \lambda)\,r_{ij}$$. The intensity $$\lambda$$ is the one [Schäfer and Strimmer (2005, section 2.4, eq. 10)](https://doi.org/10.2202/1544-6115.1175){:target="_blank"} derive in closed form, the summed sampling variance of the correlations over their summed squares:

$$
\lambda = \min\!\left(1,\; \frac{\sum_{i<j} \widehat{\operatorname{Var}}(r_{ij})}{\sum_{i<j} r_{ij}^2}\right)
$$

summed over the pairs with at least 5 shared observations. The intensity is the share of the correlations' size that is estimation noise, so it is only as good as the variance estimate. The textbook variance of a correlation, $$(1 - r_{ij}^2)^2/(n_{ij} - 1)$$ on $$n_{ij}$$ shared observations, assumes normal data. Monthly returns and rate changes have fat tails: a few large joint moves make a correlation less certain than in a normal sample of the same size. Schäfer and Strimmer's own estimator (their Appendix A) reads the variance from the data: each pair is standardized over its overlap, $$z_{i,k}$$ and $$z_{j,k}$$, and the variance of its correlation is the spread of their products,

$$
\widehat{\operatorname{Var}}(r_{ij}) = \frac{n_{ij}}{(n_{ij}-1)^3} \sum_{k} (w_k - \bar{w})^2, \qquad w_k = z_{i,k}\, z_{j,k}
$$

The chart sets both estimates against the true variance, from 4,000 samples of 120 months:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/validation/correlation-variance" alt="The normal-theory and Schafer-Strimmer Appendix A estimates of a correlation's sampling variance, divided by the true variance, for normal and Student-t(5) data at true correlations of 0, 0.3 and 0.6" %}

With Student-t tails of 5 degrees of freedom the normal-theory formula reads 0.46 times the true variance, about half, at every correlation; Appendix A reads 0.99 at a true correlation of zero. For normal data Appendix A gives $$(1 + r^2)/n$$ against a true $$(1 - r^2)^2/n$$, so it errs on the high side as the correlation grows, because it leaves out what standardizing takes away: in the chart's samples it reads 1.30 times the true variance at 0.3 and 3.33 times at 0.6. The error is on the side of shrinking more, and most pairs in a scenario set have small correlations. On the default factor set the intensity is 0.155, against 0.067 with the normal-theory formula: every correlation is 15.5% smaller than its sample value.

## How Each Number Is Set

The settings behind the correlation matrix, and the reason for each:

| Setting | Default | Kind | Why |
|:--|:--|:--|:--|
| Estimation | Pairwise, each pair on the dates both share | Judgement | A short series weakens only its own pairs |
| Too few shared observations | Fewer than 5: the pair is set to 0; fewer than 12: flagged | Judgement | A correlation from a handful of points is noise |
| Same series twice | A correlation above 0.98 is flagged | Judgement | Usually one driver configured twice |
| Shrinkage | Toward zero, intensity from the data: 0.155 in the default calibration | Fitted | [Schäfer and Strimmer (2005, section 2.4, eq. 10; Appendix A)](https://doi.org/10.2202/1544-6115.1175){:target="_blank"}: their target D, with the intensity the summed variance of the correlations over their summed squares. Each correlation's variance is estimated from the pair's own data over its own overlap, as in their Appendix A |
| Repair | Nearest correlation matrix, at most 100 iterations, tolerance $$10^{-8}$$, of the sample matrix and before shrinking, only when the shrunk matrix is not valid: a change of 1.1e-14 in the default calibration, which shrinking already makes valid | Setting | [Higham (2002, Algorithm 3.3)](https://doi.org/10.1093/imanum/22.3.329){:target="_blank"} with Dykstra's correction; the tolerance is that of his section 4 example, which converges in 19 iterations. Repairing first and shrinking after keeps the smallest eigenvalue at least the intensity times the target's ([Horn and Johnson (2013, Theorem 4.3.1)](https://doi.org/10.1017/CBO9781139020411){:target="_blank"}), where repairing the shrunk matrix left it nearly singular ([Higham (2002, Theorem 2.5)](https://doi.org/10.1093/imanum/22.3.329){:target="_blank"}) |
| Cholesky safety net | Up to 20 tries of $$(1 - j)R + jI$$, with $$j$$ from $$10^{-8}$$ and ten times larger each try, at most 0.9 | Setting | Only for a matrix that is still not positive definite after the repair and shrinkage; it blends the whole matrix toward the identity |

## Fat Tails {#fat-tails-and-tail-dependence}

Normal shocks have thin tails and almost never produce extreme moves in several factors at once, yet "everything sells off together" is exactly what a stress test is about. Student-t shocks ([Demarta and McNeil, 2005](https://doi.org/10.1111/j.1751-5823.2005.tb00254.x){:target="_blank"}) scale every factor's shock at a step by the same random draw:

$$
T_t = \varepsilon_t \sqrt{\frac{\nu - 2}{W_t}}, \qquad W_t \sim \chi^2_\nu
$$

where $$\nu$$ is the degrees of freedom. When $$W_t$$ is small, all factors take a large shock at once, so extreme moves cluster across factors (tail dependence). Normal shocks (a Gaussian copula) have no tail dependence for any correlation below one, while Student-t shocks (a t copula) have it even at zero or negative correlation ([Demarta and McNeil, 2005, section 3.2](https://doi.org/10.1111/j.1751-5823.2005.tb00254.x){:target="_blank"}). The $$\nu - 2$$ keeps the variance at one, so every fitted volatility keeps its meaning and only the tails change.

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">Choosing the degrees of freedom</p>

Lower $$\nu$$ means fatter tails; it must exceed 2. The default of 12 is the value [Kole, Koedijk and Verbeek (2007)](https://doi.org/10.1016/j.jbankfin.2006.09.010){:target="_blank"} fit to daily stock, government bond and real estate returns (12.1 in their Table 2), a portfolio for which their tests favor the Student-t copula and reject both the Gaussian and the Gumbel copula. Values near 5, often quoted, belong to shorter horizons: [Breymann, Dias and Embrechts (2003)](https://doi.org/10.1080/713666155){:target="_blank"} find 4.3 to 5.7 for hourly to daily DEM/JPY returns.
</div>

Normal shocks are the default. The common scale $$W_t$$ is drawn independently at every step. With monthly steps, twelve fat-tailed shocks partly average out over a year, so Student-t shocks add less to a one-year 99.5% figure than the monthly tails suggest. To switch them on in a settings profile:

```yaml
# my-project/settings/my_settings.yaml (a settings profile)
engine:
  shock_distribution: student_t   # default: gaussian
  degrees_of_freedom: 12.0      # the default
```

Equity crises cluster a second way: with shared equity regimes (on in the shipped settings), every market draws its regime switches from one stream of random numbers, so the markets tend to enter and leave their crisis regimes together, which brings simulated equity correlations much closer to the fitted ones ([Equities](/projects/financescenarios/docs/markets#calm-and-turbulent-regimes)).

## Example

The example uses the calibration from the [overview](/projects/financescenarios/docs#keeping-a-run), made on 25 October 2026. `correlation_frame` returns the correlation matrix as a table, one row and one column per variable. To read it from the saved calibration:

```python
from financescenarios import CalibrationResult

calibration = CalibrationResult.load("calibration.json")

calibration.correlation_frame()
```

US and European stocks have a correlation of 0.72, oil moves with stocks (0.32 in the US, 0.35 in Europe) and with US inflation (0.26), and European stocks move against the euro (-0.54): the euro is measured here as euros per dollar, so European stocks tend to fall when the dollar strengthens. When plotted, nine of the 27 variables:

{% include ft-chart.html id="markets-correlation" src="/assets/data/financescenarios-guides/markets.json" label="Correlations of the fitted shocks of US inflation, the US short and 10-year rates, US unemployment, US and European stocks, the euro, gold and crude oil" %}

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">7</span></summary>

- Breymann, W., Dias, A., Embrechts, P. (2003). "Dependence Structures for Multivariate High-Frequency Data in Finance." Quantitative Finance, 3(1), 1-14. [doi.org](https://doi.org/10.1080/713666155){:target="_blank"}
- Demarta, S., McNeil, A.J. (2005). "The t Copula and Related Copulas." International Statistical Review, 73(1), 111-129. [doi.org](https://doi.org/10.1111/j.1751-5823.2005.tb00254.x){:target="_blank"}
- Higham, N.J. (2002). "Computing the Nearest Correlation Matrix: A Problem from Finance." IMA Journal of Numerical Analysis, 22(3), 329-343. [doi.org](https://doi.org/10.1093/imanum/22.3.329){:target="_blank"}
- Horn, R.A., Johnson, C.R. (2013). "Matrix Analysis." 2nd edition. Cambridge University Press. [doi.org](https://doi.org/10.1017/CBO9781139020411){:target="_blank"}
- Kole, E., Koedijk, K., Verbeek, M. (2007). "Selecting Copulas for Risk Management." Journal of Banking & Finance, 31(8), 2405-2423. [doi.org](https://doi.org/10.1016/j.jbankfin.2006.09.010){:target="_blank"}
- Ledoit, O., Wolf, M. (2004). "Honey, I Shrunk the Sample Covariance Matrix." The Journal of Portfolio Management, 30(4), 110-119. [ledoit.net](http://www.ledoit.net/Honey_2004.pdf){:target="_blank"}
- Schafer, J., Strimmer, K. (2005). "A Shrinkage Approach to Large-Scale Covariance Matrix Estimation and Implications for Functional Genomics." Statistical Applications in Genetics and Molecular Biology, 4(1). [doi.org](https://doi.org/10.2202/1544-6115.1175){:target="_blank"}

</details>

{% include ft-charts-script.html %}
