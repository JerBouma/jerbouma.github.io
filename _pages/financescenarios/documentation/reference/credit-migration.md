---
title: "CreditMigration"
seo_title: "CreditMigration Reference – Finance Scenarios"
excerpt: "A credit cycle driving rating migrations and defaults."
description: "A credit cycle driving rating migrations and defaults."
author_profile: false
permalink: /projects/financescenarios/docs/reference/credit-migration
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

A credit cycle driving rating migrations and defaults.

```python
from financescenarios import rating_migration
from financescenarios.factors.credit_migration.credit_migration_controller import CreditMigration
```

## CreditMigration

The Credit Migration module simulates how corporate credit ratings move and default over time, driven by a simulated
credit cycle: the `credit_cycle` factor, an index that is high in good years (few downgrades and defaults) and low in
bad ones.

A bond rated BBB has a small chance of defaulting each year, but those chances are not independent across bonds or
years: in a recession many companies are downgraded and default together. This factor captures that shared swing.
Every rating's chance of an upgrade, a downgrade or default in a year follows from that year's cycle value, so
defaults bunch in the scenarios and years where the cycle turns bad. `rating_migration` then rolls a bond portfolio's
rating mix forward along the cycle, giving the share defaulted and the loss in every scenario.

The model is the one-factor ("Vasicek") credit-cycle model of rating migration
([Vasicek, 2002](https://www.risk.net/risk-management/credit-risk/1500333/loan-portfolio-value); Belkin, Suchower and
Forest 1998, as presented in
[Kim, 1999](https://www.msci.com/www/research-report/a-way-to-condition-transition/018440984)), the structure behind
the Basel internal-ratings formula. A share of every borrower's credit quality, the `asset_correlation`, moves with
the shared cycle; the rest is its own luck. The cycle is fitted year by year from default rates and simulated as a
mean-reverting process around 0, so bad years cluster but the economy recovers, and it is correlated with the other
factors, so a weak credit cycle can come with falling equities and wider spreads in the same scenario. A one-factor
model is a sensible choice here: default history is short and sparse, and one shared driver captures the common
year-to-year swing in default rates across ratings.

The data come from CEREP, the European Securities and Markets Authority's central repository of credit rating
statistics, through the Finance Toolkit, with no API key needed: every agency registered in the EU (S&P, Moody's,
Fitch and others) in its own rating scale. On S&P's corporate ratings from 2000 to 2025 the worst years come out
as 2009, 2001, 2020 and 2002, the asset correlation is about 0.10, and a shock to the cycle halves in about 8
months. That correlation sits below Basel's supervisory 12% to 24% for corporates, which is set to be prudent
([BCBS, 2005](https://www.bis.org/bcbs/irbriskweight.pdf), section 5.2); a half-life well under a year means the
yearly cycle values are close to independent from one year to the next.

The matrix pools every year of the default-rate history, as Basel CRE36.79 asks of PD estimation: the observation
period covers at least five years for at least one source, a longer relevant and material period is used whenever
one is available, and the data hold a representative mix of good and bad years
([BCBS, CRE36.79](https://www.bis.org/basel_framework/chapter/CRE/36.htm)). One choice is judgement rather than
taken from a source: the cycle is simulated as a mean-reverting process held at a long-run mean of 0, so the
simulated matrix averages back to the through-the-cycle one.

It does not derive spreads from the ratings (use `credit` for spreads by rating), recovery rates are a fixed input of
`rating_migration`, and the cycle is one index for all sectors and regions.

The `credit_migration` keys of a factor set and their defaults are listed on the reference page
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/reference/configuration-classes).

**References:**

- Vasicek, O. (2002). "Loan portfolio value." Risk, December 2002. <https://www.risk.net/risk-management/credit-risk/1500333/loan-portfolio-value>
- Kim, J. (1999). "A Way to Condition the Transition Matrix on Wind." RiskMetrics Group (MSCI). <https://www.msci.com/www/research-report/a-way-to-condition-transition/018440984>
- ESMA. "CEREP: Central Repository of credit rating activity." <https://registers.esma.europa.eu/cerep-publication/>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
CreditMigration(toolkit: Toolkit)
```

</details>

## calibrate

Calibrate the credit cycle from an agency's rating history: the average one-year transition matrix, the asset
correlation and the yearly cycle, which is then fitted as a mean-reverting process.

The transition matrix pools the agency's rating changes over every year of the default-rate history, so it
reflects how often each rating is upgraded, downgraded or defaults in an average year across good and bad years
(Basel CRE36.79 requires the longer observation period wherever one is available). The
asset correlation and the historical cycle come from the default rates per rating
([Vasicek, 2002](https://www.risk.net/risk-management/credit-risk/1500333/loan-portfolio-value);
[Kim, 1999](https://www.msci.com/www/research-report/a-way-to-condition-transition/018440984)): they measure
how strongly good and bad years move all ratings together. A higher correlation means more years like 2009 in
the scenarios and a fatter tail of portfolio losses; a faster mean reversion means downturns pass sooner.

The default-rate history spans the Toolkit's start and end dates (CEREP covers 1989 onward, S&P's own reporting
starts in 2000); a long history matters, since it needs several recessions to pin down the correlation. CEREP
answers slowly, so the first calibration takes a few minutes.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.credit_migration.credit_migration_controller import CreditMigration

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2000-01-01")
credit_migration = CreditMigration(toolkit)

params = credit_migration.calibrate(agency="S&P", rating_type="corporate")
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(
    agency: str = 'S&P',
    rating_type: str = 'corporate',
    region: str | None = None,
    matrix_years: int | None = None,
    pd_floor: float = PD_FLOOR,
) -> CreditCycleParams
```

**Args:**

- <u>agency (str):</u> the rating agency as CEREP names it, e.g. "S&P", "Moody's", "Fitch". Defaults to "S&P".
- <u>rating_type (str):</u> "corporate", "sovereign", "structured_finance" or "covered_bonds". Defaults to "corporate".
- <u>region (str &#124; None):</u> limit to rated entities in one region, e.g. "Europe". Defaults to None (all regions).
- <u>matrix_years (int &#124; None):</u> how many recent years of transition counts to pool, at least 1. Defaults to None: every year from the first year of the default-rate history, the same window as the default probabilities (Basel CRE36.79).
- <u>pd_floor (float):</u> the lowest one-year default probability any rating gets. Defaults to 0.0005, the Basel III / CRR3 corporate floor; 0.0003 gives the Basel II floor.

**Returns:**

<u>CreditCycleParams:</u> the cycle's `mean_reversion_speed`, `long_run_mean` (0), `volatility` and `initial_value`, plus `ratings`, `transition_matrix`, `asset_correlation` and `agency`.

**Raises:**

- <u>ValueError:</u> if `matrix_years` is below 1, or CEREP returns no transition counts or too few years of default rates.

</details>

## params

The calibrated credit cycle: its mean-reverting process, average transition matrix and asset correlation.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
creditmigration.params  # property -> CreditCycleParams
```

**Raises:**

- <u>RuntimeError:</u> if the cycle has not been calibrated yet.

</details>

## cycle

The historical credit cycle, one value per year: strongly negative in years such as 2001 and 2009, when
defaults spiked. Raises a `RuntimeError` before calibration.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
creditmigration.cycle  # property -> pl.DataFrame
```

</details>

## changes

The yearly changes of the historical cycle, the input for its correlation with the other factors.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
creditmigration.changes  # property -> pl.DataFrame
```

</details>

## step_function

The one-step move of the cycle: an exact mean-reverting (Ornstein-Uhlenbeck) step back toward 0.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
creditmigration.step_function  # property
```

</details>

## rating_migration

Roll a bond portfolio's rating mix forward through a run's simulated credit cycle, one year at a time: the share of
the portfolio in each rating and in default, and the loss to default, in every simulation and year.

Given, say, 40% A-rated, 50% BBB and 10% BB bonds, this shows how much of the portfolio has been downgraded or has
defaulted after each year in every scenario, and what that costs once the recovery on defaulted bonds is counted. Each
simulated year's cycle value picks that year's transition matrix, so a bad year pushes every rating toward downgrade
and default at once. Scenarios with a bad credit cycle therefore carry far more defaults than the average, and the gap
between the mean and a high quantile in `summary()` shows how large that tail is.

**As an example:**

```python
from financescenarios import rating_migration

# result: the ScenarioSet of a run with credit_migration.enabled: true
migration = rating_migration(result, {"A": 40, "BBB": 50, "BB": 10})
migration.summary()
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
rating_migration(
    scenario_set: ScenarioSet,
    holdings: Mapping[str, float],
    recovery_rate: float = 0.4,
    params: CreditCycleParams | None = None,
) -> RatingMigrationResult
```

**Args:**

- <u>scenario_set (ScenarioSet):</u> a run with `credit_migration.enabled: true`, so it holds `credit_cycle`.
- <u>holdings (Mapping[str, float]):</u> exposure per starting rating, e.g. {"A": 40, "BBB": 50, "BB": 10}.
- <u>recovery_rate (float):</u> the share of a defaulted exposure recovered, in [0, 1). Defaults to 0.4, the senior unsecured bond recovery by the rating held a year before default: "$39.0" per $100 par for all ratings, 1982-2004, in Moody's (2005) Exhibit 28 (https://www.bu.edu/econ/files/2015/01/Moodys_Default_1920-2004.pdf).
- <u>params (CreditCycleParams &#124; None):</u> the calibrated cycle. Defaults to None, which takes it from the run; pass `calibration.calibrated_params["credit_cycle"]` for a run read back from disk.

**Returns:**

<u>RatingMigrationResult:</u> `distribution`, `cumulative_default` and `loss` per simulation and whole year, with `summary()` for the mean and quantiles per year.

**Raises:**

- <u>KeyError:</u> if the run has no `credit_cycle`.
- <u>ValueError:</u> if the calibrated cycle is not available, a holding names an unknown rating or is negative, or the recovery rate is outside [0, 1).

</details>

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

### conditional_default_rate

The default rate of a rating in a year with credit-cycle value Z, from Vasicek's one-factor model: a high Z is a
good year with fewer defaults, a low Z a recession with many.

Every borrower's credit quality is a standard normal variable, part shared cycle and part its own luck, and it
defaults when that quality falls below the threshold set by its long-run default rate PD. The asset correlation rho is
the shared part: the higher it is, the more a bad year lifts every default rate at once, and the fatter the tail of
portfolio losses. The long-run PD is still the average across years, so the model redistributes defaults over good and
bad years rather than adding to them. This is the structure behind the Basel internal-ratings formula, where Vasicek's
extension of Merton's model to an asymptotic single risk factor portfolio model is the basis (BCBS, 2005, An
Explanatory Note on the Basel II IRB Risk Weight Functions, section 4.2, https://www.bis.org/bcbs/irbriskweight.pdf).
Basel's supervisory corporate rho moves between limit correlations of 12% and 24% (section 5.2), a deliberately
prudent value; rho here is fitted to default history.

The formula is as follows:

$$
\operatorname{PD}(Z) = \Phi((\Phi ^{-1} (\text{PD}) - \sqrt{\rho} \cdot Z) / \sqrt{1 - \rho})
$$

Where Phi is the standard normal CDF and rho the asset correlation
([Vasicek, 2002](https://www.risk.net/risk-management/credit-risk/1500333/loan-portfolio-value)).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
conditional_default_rate(
    probability: np.ndarray,
    asset_correlation: float,
    cycle: np.ndarray,
) -> np.ndarray
```

</details>

### fit_credit_cycle

Read the credit cycle off history: the asset correlation and one cycle value per year, from the default rates per
rating (Belkin, Suchower and Forest 1998, as presented in
[Kim, 1999](https://www.msci.com/www/research-report/a-way-to-condition-transition/018440984): a one-parameter
representation of transition matrices, built on a credit cycle index for the credit state of the market as a
whole).

Each year's cycle value is the one that best explains that year's default rates across all ratings at once, so
years such as 2009 and 2001 come out strongly negative and quiet years positive. The asset correlation is the one at
which those yearly values have unit variance, as the model assumes: if defaults swing a lot from year to year, a
higher correlation is needed to explain it. Rare defaults in the top ratings carry little information, so each
rating is weighted by the binomial variance of its long-run rate.

The formula is as follows:

$$
Z_{t} = \operatorname{argmin}(\operatorname{sum}(w_{k} \cdot (\text{DR}_{k} - \text{PD}_{k}(Z)) ^{2})),\;\; \text{over ratings k in year t}
$$

$$
w_{k} = 1 / (\text{PD}_{k} \cdot (1 - \text{PD}_{k}))
$$

$$
\operatorname{var}(Z_{t}) = 1,\;\; \text{solved for rho}
$$

Where DR_k is the observed default rate, PD_k the long-run rate, PD_k(Z) is `conditional_default_rate` and the
weights are the binomial variance of each rating's long-run rate.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_credit_cycle(
    default_rates: pl.DataFrame,
    default_probabilities: Mapping[str, float],
) -> tuple[float, pl.DataFrame]
```

**Args:**

- <u>default_rates (pl.DataFrame):</u> the observed default rate per rating and year, as decimals.
- <u>default_probabilities (Mapping[str, float]):</u> the long-run default rate per rating.

**Returns:**

<u>tuple[float, pl.DataFrame]:</u> the asset correlation, and the cycle value per year.

**Raises:**

- <u>ValueError:</u> if fewer than five years are given, or no correlation gives the index unit variance.

</details>

{% raw %}
### conditional_transition_matrix

The one-year rating transition matrix in a year with credit-cycle value Z (Belkin, Suchower and Forest 1998; see
[Kim, 1999](https://www.msci.com/www/research-report/a-way-to-condition-transition/018440984)).

The average through-the-cycle matrix is what an agency reports; this conditions it on the state of the economy.
Each row's cumulative probabilities, counted from default upward, become thresholds on a standard normal credit
quality, as in CreditMetrics, and the cycle shifts that quality by sqrt(rho) * Z. A bad year (Z below 0) moves
weight from upgrades toward downgrades and default for every rating at once; a good year does the reverse. Because
the same Z drives every row, downgrades and defaults bunch in the same years, which is what makes a credit
portfolio's loss distribution fat-tailed.

The formula is as follows:

$$
C_{j} = \operatorname{sum}(M_{k} \;\text{for}\; k \;\text{from}\; j \;\text{down to default})
$$

$$
C_{j}(Z) = \Phi((\Phi ^{-1} (C_{j}) - \sqrt{\rho} \cdot Z) / \sqrt{1 - \rho})
$$

$$
M_{j}(Z) = C_{j}(Z) - C_{\text{next}}(Z)
$$

Where M is one row of the matrix, j a rating and C_next the cumulative probability of the next-worse state.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
conditional_transition_matrix(
    matrix: np.ndarray,
    asset_correlation: float,
    cycle: np.ndarray,
) -> np.ndarray
```

**Args:**

- <u>matrix (np.ndarray):</u> the average through-the-cycle transition matrix, best rating first and default last.
- <u>asset_correlation (float):</u> rho, the share of credit quality that moves with the cycle.
- <u>cycle (np.ndarray):</u> the credit-cycle values Z to condition on.

**Returns:**

<u>np.ndarray:</u> one transition matrix per cycle value, every row summing to 1.

</details>
{% endraw %}

### migrate_ratings

Roll a portfolio's rating mix forward one year at a time along simulated credit cycles: each scenario's cycle
value in a year picks that year's transition matrix, so downgrades and defaults bunch in the scenarios and years
where the cycle turns bad, as they do in recessions. A portfolio downgraded in a bad year starts the next year
from a weaker mix, so a run of bad years compounds. Losses apply a fixed recovery rate to the defaulted share.
Recovery in fact falls when defaults rise (Moody's, 2005, Exhibit 10, fits a recovery rate of 0.52 minus 6.9
times the default rate), so a fixed rate understates the loss in the worst years.

The formula is as follows:

$$
d_{t} = d_{t-1} \cdot M(Z_{t})
$$

$$
\text{loss}_{t} = D_{t} \cdot \text{exposure} \cdot (1 - R)
$$

Where d_t is the row vector of rating shares, M(Z_t) is `conditional_transition_matrix`, D_t the share in default
and R the recovery rate.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
migrate_ratings(
    cycle_paths: np.ndarray,
    params: CreditCycleParams,
    holdings: Mapping[str, float],
    recovery_rate: float = 0.4,
) -> RatingMigrationResult
```

**Args:**

- <u>cycle_paths (np.ndarray):</u> the simulated `credit_cycle` per scenario at each whole year; the value at the end of a year drives that year's transitions.
- <u>params (CreditCycleParams):</u> the calibrated cycle, matrix and asset correlation.
- <u>holdings (Mapping[str, float]):</u> exposure per starting rating, e.g. {"A": 40, "BBB": 50, "BB": 10}.
- <u>recovery_rate (float):</u> the share of a defaulted exposure recovered, in [0, 1). Defaults to 0.4 (Moody's, 2005, Exhibit 28: senior unsecured bonds recover "$39.0" per $100 par, all ratings held a year before default).

**Returns:**

<u>RatingMigrationResult:</u> the rating shares, cumulative default share and loss per scenario and year.

**Raises:**

- <u>ValueError:</u> if a holding names an unknown rating, is negative, or the recovery rate is outside [0, 1).

</details>
