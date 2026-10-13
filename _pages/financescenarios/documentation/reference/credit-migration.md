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
mean-reverting process around 0 that joins the run's correlation matrix like any other factor.

The data come from CEREP, the European Securities and Markets Authority's central repository of credit rating
statistics, through the Finance Toolkit (`fixedincome.get_rating_transition_matrix` and `get_default_rates`), no API
key: every agency registered in the EU (S&P, Moody's, Fitch and others) in its own rating scale. On S&P's corporate
ratings from 2000 to 2025 the worst years come out as 2009, 2001, 2020 and 2002, the asset correlation is about 0.10,
and a shock to the cycle halves in about 8 months.

It does not derive spreads from the ratings (use `credit` for spreads by rating), recovery rates are a fixed input of
`rating_migration`, and the cycle is one index for all sectors and regions.

Configuration (`credit_migration` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `enabled` | `false` | Adds the `credit_cycle` factor. |
| `agency` | `S&P` | The rating agency, e.g. `S&P`, `Moody's`, `Fitch`. |
| `rating_type` | `corporate` | `corporate`, `sovereign`, `structured_finance` or `covered_bonds`. |
| `region` | `null` | Limit to rated entities in a region, e.g. `Europe`; all by default. |
| `matrix_years` | `10` | Years of transition counts pooled into the average transition matrix. |
| `beliefs` | none | Override the cycle's `long_run_mean` (-0.5: a lasting downturn), speed, volatility, shocks. |

**References:**

- Vasicek, O. (2002). "Loan portfolio value." Risk, December 2002. <https://www.risk.net/risk-management/credit-risk/1500333/loan-portfolio-value>
- Kim, J. (1999). "A Way to Condition the Transition Matrix on Wind." RiskMetrics Group (MSCI). <https://www.msci.com/www/research-report/a-way-to-condition-transition/018440984>
- ESMA. "CEREP: Central Repository of credit rating activity." <https://registers.esma.europa.eu/cerep-publication/>

## calibrate

```python
calibrate(
    agency: str = 'S&P',
    rating_type: str = 'corporate',
    region: str | None = None,
    matrix_years: int = 10,
) -> CreditCycleParams
```

Calibrate the credit cycle: pool the agency's recent rating changes into an average one-year transition matrix,
fit the yearly cycle index and the asset correlation from the default rates per rating, and fit the index as a
mean-reverting process.

This learns how often each rating has been upgraded, downgraded or defaulted in an average year, and how strongly
good and bad years swing all of those together. The transition matrix has a row per starting rating and a column
per rating a year later, ending in default; the asset correlation says how much of each borrower's credit quality
moves with the cycle.

CEREP answers slowly (up to half a minute per year), so the first calibration takes a few minutes; each year is
cached afterwards. The default-rate history spans the Toolkit's start and end dates (CEREP covers 1989 onward,
S&P's own reporting starts in 2000).

**Args:**

- <u>agency (str):</u> the rating agency as CEREP names it, e.g. "S&P", "Moody's", "Fitch". Defaults to "S&P".
- <u>rating_type (str):</u> "corporate", "sovereign", "structured_finance" or "covered_bonds". Defaults to "corporate".
- <u>region (str &#124; None):</u> limit to rated entities in one region, e.g. "Europe". Defaults to None (all regions).
- <u>matrix_years (int):</u> how many recent years of transition counts to pool, at least 1. Defaults to 10.

**Returns:**

<u>CreditCycleParams:</u> the cycle's `mean_reversion_speed`, `long_run_mean` (0), `volatility` and `initial_value`, plus `ratings`, `transition_matrix`, `asset_correlation` and `agency`.

**Raises:**

- <u>ValueError:</u> if `matrix_years` is below 1, or CEREP returns no transition counts or too few years of default rates.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.credit_migration.credit_migration_controller import CreditMigration

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2000-01-01")
credit_migration = CreditMigration(toolkit)

params = credit_migration.calibrate(agency="S&P", rating_type="corporate")
```

## params

```python
creditmigration.params  # property -> CreditCycleParams
```

The last-calibrated credit cycle: its mean-reverting process, transition matrix and asset correlation.

**Raises:**

- <u>RuntimeError:</u> if `calibrate()` has not been called yet.

## cycle

```python
creditmigration.cycle  # property -> pl.DataFrame
```

The fitted yearly credit-cycle index, with columns `year` and `cycle`; raises a `RuntimeError` before
`calibrate()`.

## changes

```python
creditmigration.changes  # property -> pl.DataFrame
```

Dated yearly changes of the cycle index, used to estimate its correlation with the other factors.

## step_function

```python
creditmigration.step_function  # property
```

The function that moves the cycle index one time step (an exact Ornstein-Uhlenbeck step).

## rating_migration

```python
rating_migration(
    scenario_set: ScenarioSet,
    holdings: Mapping[str, float],
    recovery_rate: float = 0.4,
    params: CreditCycleParams | None = None,
) -> RatingMigrationResult
```

Roll a bond portfolio's rating mix forward through a run's simulated credit cycle, one year at a time: the share of
the portfolio in each rating and in default, and the loss to default, in every simulation and year.

Given, say, 40% A-rated, 50% BBB and 10% BB bonds, this shows how much of the portfolio has been downgraded or has
defaulted after each year in every scenario, and what that costs once the recovery on defaulted bonds is counted. Each
simulated year's cycle value picks that year's transition matrix, so a bad year pushes every rating toward downgrade
and default at once. Scenarios with a bad credit cycle therefore carry far more defaults than the average, and the gap
between the mean and a high quantile in `summary()` shows how large that tail is.

**Args:**

- <u>scenario_set (ScenarioSet):</u> a run with `credit_migration.enabled: true`, so it holds `credit_cycle`.
- <u>holdings (Mapping[str, float]):</u> exposure per starting rating, e.g. {"A": 40, "BBB": 50, "BB": 10}.
- <u>recovery_rate (float):</u> the share of a defaulted exposure recovered, in [0, 1). Defaults to 0.4, a common assumption for senior unsecured corporate bonds.
- <u>params (CreditCycleParams &#124; None):</u> the calibrated cycle. Defaults to None, which reads it from the run itself; pass `calibration.calibrated_params["credit_cycle"]` for a run read back from disk.

**Returns:**

<u>RatingMigrationResult:</u> `distribution`, `cumulative_default` and `loss` per simulation and whole year, with `summary()` for the mean and quantiles per year.

**Raises:**

- <u>KeyError:</u> if the run has no `credit_cycle`.
- <u>ValueError:</u> if the calibrated cycle is not available, a holding names an unknown rating or is negative, or the recovery rate is outside [0, 1).

**As an example:**

```python
from financescenarios import rating_migration

# result: the ScenarioSet of a run with credit_migration.enabled: true
migration = rating_migration(result, {"A": 40, "BBB": 50, "BB": 10})
migration.summary()
```
