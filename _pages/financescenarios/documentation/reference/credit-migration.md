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

A credit cycle driving rating migrations and defaults. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios import rating_migration
from financescenarios.factors.credit_migration.credit_migration_controller import CreditMigration
```

## CreditMigration

```python
CreditMigration(toolkit: Toolkit)
```

The Credit Migration module simulates how corporate credit ratings move and default over time, driven by a
simulated credit cycle: the `credit_cycle` factor, a standard normal index that is high in good years (few
downgrades and defaults) and low in bad ones. Every rating's chance of being upgraded, downgraded or defaulting
in a given year follows from that year's cycle value, so defaults bunch in the scenarios and years where the
cycle turns bad, as they do in recessions.

In plain terms: a bond rated BBB has a small chance of defaulting each year, but those chances are not
independent across bonds or years; in a recession many companies are downgraded and default together. This
factor captures that shared swing, and `rating_migration` rolls a bond portfolio's rating mix forward along it
to give the share defaulted and the loss in every scenario.

The model is the one-factor ("Vasicek") credit-cycle model of rating migration
([Vasicek, 2002](https://www.risk.net/risk-management/credit-risk/1500333/loan-portfolio-value); Belkin, Suchower and
Forest 1998, as presented and extended in
[Kim, 1999](https://www.msci.com/www/research-report/a-way-to-condition-transition/018440984)), the same structure
behind the Basel internal-ratings formula. A borrower's credit quality is a
standard normal variable; a share `asset_correlation` (rho) of it is the shared cycle Z, the rest its own luck.
Each rating's one-year moves are cut-offs on that quality, set by the through-the-cycle transition matrix, so a
year's Z shifts every row of the matrix at once.

Data come from CEREP, the European Securities and Markets Authority's central repository of credit rating
statistics, through the Finance Toolkit (`fixedincome.get_rating_transition_matrix` and `get_default_rates`), no
API key: every agency registered in the EU (S&P, Moody's, Fitch and others) in its own scale. The
through-the-cycle matrix pools the last `matrix_years` years of transition counts; its default column is
replaced by each rating's average yearly default rate, since the matrix compares only start and end ratings
(a borrower that defaulted and was re-rated within the year would not count). CC and C are folded into CCC and
selective default into default; withdrawn ratings are left out. Each rating's default probability is the
average of its own yearly default rates (CC and C, thinly populated, are not mixed into CCC there), and a
rating that never defaulted in the sample is given Basel's 0.03% floor. Z is then fitted year by year from the
default rates across ratings, rho chosen so Z has unit variance, and Z's yearly path is fitted as a
mean-reverting (Ornstein-Uhlenbeck) process around 0, the model's own mean, that joins the run's correlation
matrix like any other factor. On S&P's corporate ratings from 2000 to 2025 the worst years come out as 2009,
2001, 2020 and 2002, the asset correlation is about 0.10, and a shock to the cycle halves in about 8 months.

What it does not do: spreads are not derived from the ratings (use `credit` for spreads by rating, including
Moody's Aaa and Baa from 1953); recovery rates are a fixed input of `rating_migration`, not modelled; and the
cycle is one index for all sectors and regions.

Configuration (`credit_migration` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `enabled` | `false` | Adds the `credit_cycle` factor. |
| `agency` | `S&P` | The rating agency, e.g. `S&P`, `Moody's`, `Fitch`. |
| `rating_type` | `corporate` | `corporate`, `sovereign`, `structured_finance` or `covered_bonds`. |
| `region` | `null` | Limit to rated entities in a region, e.g. `Europe`; all by default. |
| `matrix_years` | `10` | Years of transition counts pooled into the through-the-cycle matrix. |
| `beliefs` | none | Override the cycle's `long_run_mean` (-0.5: a lasting downturn), speed, volatility, shocks. |

**References:**

- Vasicek, O. (2002). "Loan portfolio value." Risk, December 2002. <https://www.risk.net/risk-management/credit-risk/1500333/loan-portfolio-value>
- Kim, J. (1999). "A Way to Condition the Transition Matrix on Wind." RiskMetrics Group (MSCI). Builds the credit cycle index and conditional transition matrices on Belkin, Suchower and Forest's (1998) one-parameter representation, which has no public copy. <https://www.msci.com/www/research-report/a-way-to-condition-transition/018440984>
- Jarrow, R.A., Lando, D., Turnbull, S.M. (1997). "A Markov Model for the Term Structure of Credit Risk Spreads." Review of Financial Studies, 10(2), 481-523. <https://doi.org/10.1093/rfs/10.2.481>
- ESMA. "CEREP: Central Repository of credit rating activity." <https://registers.esma.europa.eu/cerep-publication/>
- Regulation (EU) No 575/2013 (Capital Requirements Regulation), Article 160(1), the 0.03% probability-of-default floor. <https://eur-lex.europa.eu/eli/reg/2013/575/oj>

## calibrate

```python
calibrate(
    agency: str = 'S&P',
    rating_type: str = 'corporate',
    region: str | None = None,
    matrix_years: int = 10,
) -> CreditCycleParams
```

Calibrate the credit cycle: pool the agency's recent transition counts into a through-the-cycle matrix, fit
the yearly cycle index and the asset correlation from its default rates per rating, and fit the index as a
mean-reverting process.

In plain terms: this learns how often each rating has been upgraded, downgraded or defaulted in an average
year, and how strongly good and bad years swing all of those together.

**Args:**

- <u>agency (str):</u> the rating agency as CEREP names it, e.g. "S&P", "Moody's", "Fitch".
- <u>rating_type (str):</u> "corporate", "sovereign", "structured_finance" or "covered_bonds".
- <u>region (str &#124; None):</u> limit to one region of rated entities; all by default.
- <u>matrix_years (int):</u> how many recent years of transition counts to pool, at least 1.

**Returns:**

<u>CreditCycleParams:</u> the cycle's mean-reverting process (yearly), the matrix and the asset correlation.

**Raises:**

- <u>ValueError:</u> if `matrix_years` is below 1, or CEREP returns no counts or too few years of default rates.

**Notes:**

- CEREP answers slowly (up to half a minute per year), so the first calibration takes a few minutes; each
  year is cached afterwards.
- The default-rate history spans the Toolkit's start and end dates (CEREP covers 1989 onward; S&P's own
  reporting starts in 2000).

## params

```python
creditmigration.params  # property -> CreditCycleParams
```

The last-calibrated credit cycle.

**Raises:**

- <u>RuntimeError:</u> if calibrate() hasn't been called yet.

## cycle

```python
creditmigration.cycle  # property -> pl.DataFrame
```

The fitted yearly credit-cycle index, "year" and "cycle".

## changes

```python
creditmigration.changes  # property -> pl.DataFrame
```

Dated yearly changes of the cycle index, for the cross-factor correlation.

## step_function

```python
creditmigration.step_function  # property
```

The cycle's exact Ornstein-Uhlenbeck step.

## rating_migration

```python
rating_migration(
    scenario_set: ScenarioSet,
    holdings: Mapping[str, float],
    recovery_rate: float = 0.4,
    params: CreditCycleParams | None = None,
) -> RatingMigrationResult
```

Roll a bond portfolio's rating mix forward through a run's simulated credit cycle, one year at a time: the share
of the portfolio in each rating and in default, and the loss to default, in every simulation and year.

In plain terms: given, say, 40% A-rated, 50% BBB and 10% BB bonds, this says how much of the portfolio has been
downgraded or has defaulted after each year in every scenario, and what that costs once the recovery on defaulted
bonds is taken into account. Scenarios with a bad credit cycle carry far more defaults than the average.

**Args:**

- <u>scenario_set (ScenarioSet):</u> a run with `credit_migration.enabled: true` (it holds `credit_cycle`).
- <u>holdings (Mapping[str, float]):</u> exposure per starting rating, e.g. {"A": 40, "BBB": 50, "BB": 10}.
- <u>recovery_rate (float):</u> the share of a defaulted exposure recovered, in [0, 1); 40% is a common assumption for senior unsecured corporate bonds.
- <u>params (CreditCycleParams &#124; None):</u> the calibrated cycle; read from the run itself by default, so pass `calibration.calibrated_params["credit_cycle"]` for a run read back from disk.

**Returns:**

<u>RatingMigrationResult:</u> `distribution`, `cumulative_default` and `loss` per simulation and whole year, with `summary()` for the mean and quantiles per year.

**Raises:**

- <u>KeyError:</u> if the run has no `credit_cycle`.
- <u>ValueError:</u> if the calibrated cycle is not available or the holdings are invalid.

**As an example:**

```python
from financescenarios.factors.credit_migration.credit_migration_model import rating_migration

migration = rating_migration(result, {"A": 40, "BBB": 50, "BB": 10})
migration.summary()
```
