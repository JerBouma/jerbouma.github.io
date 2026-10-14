---
title: "Inflation"
seo_title: "Inflation Reference | Finance Scenarios"
seo_title_suffix: false
excerpt: "Consumer price inflation, one per country or region."
description: "Consumer price inflation, one per country or region."
author_profile: false
permalink: /projects/financescenarios/docs/reference/inflation
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Consumer price inflation, one per country or region.

```python
from financescenarios.factors.inflation.inflation_controller import Inflation
```

The Inflation module simulates consumer price inflation for one or more countries: the driver of indexed
liabilities, real returns and purchasing power.

The model assumes inflation is pulled back toward a long-run level after a shock, as it was after the 2022 surge
once central banks responded, and that the pull is steady rather than abrupt. That gives scenarios a realistic
spread: a spike decays over a few years instead of persisting forever, while the long-run level anchors 30-year
projections. Inflation can turn negative, so deflation scenarios are possible. Because inflation sits at the root
of the economy in actuarial models such as [Wilkie (1986)][wilkie-1986] and
[Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf),
it can drive interest rates, dividends and property; `ScenarioSet.cumulative_index` turns a path into a price
index.

The default model is the Ornstein-Uhlenbeck process `dpi = a(theta - pi)dt + sigma*dW`: `a` is how fast a gap to
the long-run level `theta` closes and `sigma` the size of the random swings
([Uhlenbeck and Ornstein, 1930](https://doi.org/10.1103/PhysRev.36.823)). `method` picks the process:

| Method | What it is |
|:-------|:-----------|
| `ou` (default) | The model above; inflation can go negative. |
| `wilkie_ar1` | Each period keeps a fixed share of last period's gap to the mean ([Wilkie, 1986][wilkie-1986]). |
| `hibbert_two_factor` | Pulled toward a moving "expected inflation" level ([Hibbert et al., 2001][hibbert-2001]). |
| `knw` | Linked both ways with a paired interest rate; fitted by `Knw`. |
| `knw_sv` | `knw` with a shared, randomly changing volatility; fitted by `KnwSv`. |

[wilkie-1986]: https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf
[hibbert-2001]: https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf

For `ou`, `volatility_model: garch` lets calm and turbulent periods alternate, which fattens the tails
([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1)); `condition_on_business_cycle` and
`condition_on_interest_rate` tie inflation to the leading indicator or a paired interest rate; and
`measure: risk_neutral` moves inflation around the breakeven inflation the bond market prices today, with its
historical volatility (see `calibrate_risk_neutral`).

The data are the Finance Toolkit's Consumer Price Index, year over year, with no API key needed: 0.034 means
prices are 3.4% higher than a year ago. `source: oecd` covers the roughly 38 OECD members; `source: gmdb`
(the Global Macro Database) adds countries such as Brazil and India, yearly only. Only headline inflation is
modeled.

The `inflation[i]` keys of a factor set and their defaults are listed on the reference page
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/reference/configuration-classes).

Beliefs are annual decimals (`long_run_mean: 0.09` is 9% a
year) and apply only to the constant-volatility `ou` fit, not with `risk_neutral`; a regime file addresses one
entry as `"inflation.<name>"`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Inflation(toolkit: Toolkit)
```

</details>

## calibrate

Calibrate one country's inflation process from its history: how fast inflation returns to its normal level
(`mean_reversion_speed`), what that level is (`long_run_mean`) and how much it swings (`volatility`).

The parameters come from the country's own Consumer Price Index history, so simulated inflation spikes and
settles the way it has in that economy: a high-inflation country such as Brazil gets a higher anchor and
wider swings than the United States. The `ou` fit regresses each value on the value a year earlier, which
measures how strongly inflation has been pulled back after deviations ([Uhlenbeck and Ornstein,
1930](https://doi.org/10.1103/PhysRev.36.823)): two neighbouring monthly year-over-year rates share 11 months of
price changes, so a month-to-month fit would read that overlap as slow mean reversion. `wilkie_ar1` gives a
`persistence`, the share of last period's gap to the mean carried into this one, from the same year-apart
regression, so the two methods agree on the same history. Values are annual decimals and every path starts from
`initial_value`, the latest observed rate. The long-run level is only as good as the history behind it, so use
an early `start_date`: five years cover too few inflation cycles.

`hibbert_two_factor` assumes inflation is pulled toward an expected-inflation level that itself drifts, which
keeps regime shifts such as the 1970s or the 2010s low-inflation decade inside the scenario set.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.inflation.inflation_controller import Inflation

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2000-01-01")
inflation = Inflation(toolkit)

inflation.calibrate("united_states_inflation", country="United States")
inflation.calibrate("brazil_inflation", country="Brazil", source="gmdb", period="yearly")
```

Which returns (calibrated on 2026-10-14):

| name | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-----|---------------------:|--------------:|-----------:|--------------:|
| united_states_inflation | 1.1818 | 0.0257 | 0.0269 | 0.0340 |
| brazil_inflation | 1.0904 | 0.0615 | 0.0387 | 0.0502 |

US inflation starts at 3.40% and is pulled toward 2.57%, halving a gap in about seven months: since 2000, a
value regressed on the value a year earlier keeps only 26% of its gap. The month-to-month fit (`ou_fit="step"`)
gives a speed of 0.4150, a gap halving in 1.7 years, because it reads the overlap of monthly rates as
persistence; the yearly series, which has no overlap, gives 0.887.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(
    name: str,
    country: str = 'United States',
    period: str = 'monthly',
    source: str = 'oecd',
    method: str = 'ou',
    volatility_model: str = 'constant',
    business_cycle_covariate: pl.Series | None = None,
    business_cycle_covariate_dates: pl.Series | None = None,
    target_source: str = 'coarser_period',
    target_period: str = 'yearly',
    target_smoothing: float = 0.05,
    ou_fit: str = 'year_apart',
) -> OUParams | GARCHParams | OUCovariateParams | AR1Params | MovingTargetOUParams
```

**Args:**

- <u>name (str):</u> the entry's name.
- <u>country (str):</u> the country, default "United States".
- <u>period (str):</u> "monthly" (default), "quarterly" or "yearly"; only "yearly" for "gmdb".
- <u>source (str):</u> "oecd" (default) or "gmdb" (the Global Macro Database).
- <u>method (str):</u> "ou" (default), "wilkie_ar1" or "hibbert_two_factor".
- <u>volatility_model (str):</u> "constant" (default) or "garch".
- <u>business_cycle_covariate (pl.Series &#124; None):</u> the leading indicator or paired interest rate inflation moves with, default None.
- <u>business_cycle_covariate_dates (pl.Series &#124; None):</u> the dates of that series; required with it.
- <u>target_source (str):</u> the "hibbert_two_factor" target: "coarser_period" (default, the same inflation at `target_period`) or "ewma" (a smoothed average of its own history).
- <u>target_period (str):</u> "quarterly" or "yearly" (default) for "coarser_period", coarser than `period`.
- <u>target_smoothing (float):</u> the "ewma" weight on each new observation, between 0 and 1, default 0.05, a judgement (a memory of about 20 observations; the paper's target is unobserved).
- <u>ou_fit (str):</u> how the "ou" fits (constant volatility, "garch" or a covariate) and the "hibbert_two_factor" legs read persistence: "year_apart" (default) regresses each value on the value a year earlier, "step" on the previous observation, which reads the overlap of monthly year-over-year rates as slow mean reversion (the fit before October 2026). Yearly data give the same result either way.

**Returns:**

<u>OUParams &#124; GARCHParams &#124; OUCovariateParams &#124; AR1Params &#124; MovingTargetOUParams:</u> the fitted parameters, including `initial_value`.

**Raises:**

- <u>ValueError:</u> if an option is unknown or two options clash, no data come back, or the history is too short or shows no pull toward a normal level.

</details>

## calibrate_risk_neutral

Calibrate risk-neutral inflation: random around the breakeven curve the bond market prices today, so the
expected price index matches market prices and caps and floors on indexation get a time value.

The gap between a nominal government bond yield and an inflation-protected one of the same maturity, the
"breakeven", is the inflation the bond market prices in. It is a curve, not one number, because expected
inflation differs by horizon. Inflation that followed it exactly in every scenario would value a plain
inflation-linked cashflow correctly but give a capped or floored one (limited price indexation, a 0%-5%
pension increase) no time value, since a cap above the curve would never be hit. So by default inflation
moves randomly around the curve with the speed and volatility of the country's own consumer price history,
corrected so the expected price index still grows as the curve says (see `BreakevenInflationParams`). The
volatility is historical because the Finance Toolkit has no prices of inflation caps and floors to imply one
from; treat the time value as indicative. This is what `measure: risk_neutral` selects with `method: ou`.

The curve is a [Nelson-Siegel (1987)](https://doi.org/10.1086/296409) fit (a long-run level, a slope and a hump)
on the latest date every maturity is quoted. The data come from the US Treasury, the Bank of England and, for
Germany, the Bundesbank's federal securities yields (inflation-linked minus nominal), with no API key needed.
The shortest breakeven is three (UK) or five years out (US, Germany); before it the curve holds the fitted
breakeven at that maturity flat, the constant-forward rule EIOPA uses before its first quoted maturity (RFR
Technical Documentation EIOPA-BoS-26/198, Annex D.8.2-D.8.3, where a constant forward makes every forward
and every spot rate before the first maturity t1 equal to the spot rate r_t1 at t1), rather than
extrapolate the Nelson-Siegel forward to today.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.inflation.inflation_controller import Inflation

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2005-01-01")
inflation = Inflation(toolkit)

inflation.calibrate_risk_neutral("us_breakeven")
```

Which returns (calibrated on 2026-10-14):

| name | level | slope | curvature | initial_value | mean_reversion_speed | volatility |
|:-----|------:|------:|----------:|--------------:|---------------------:|-----------:|
| us_breakeven | 0.0237 | -0.0001 | -0.0015 | 0.0237 | 1.1456 | 0.0289 |

The breakeven curve is close to flat at 2.37%. Inflation scatters around it with a long-run spread of
0.0289 / sqrt(2 x 1.1456) = 1.91%, in line with the 1.87% spread of US inflation since 2005.

**References:**

- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. <https://doi.org/10.1016/j.jeconom.2005.03.005>
- Jarrow, R., Yildirim, Y. (2003). "Pricing Treasury Inflation Protected Securities and Related Derivatives using an HJM Model." Journal of Financial and Quantitative Analysis, 38(2), 337-358. <https://doi.org/10.2307/4126754>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_risk_neutral(
    name: str,
    decay: float = 0.7308,
    country: str = 'United States',
    volatility: str = 'history',
    source: str = 'oecd',
    period: str = 'monthly',
) -> DeterministicPathParams | BreakevenInflationParams
```

**Args:**

- <u>name (str):</u> the entry's name, also its factor name in the simulation.
- <u>decay (float):</u> the Nelson-Siegel decay, which sets where the hump sits, default 0.7308; fixed rather than fitted, from Diebold and Li (2006, section 3 of NBER w10048), whose λ of 0.0609 a month puts the medium-term factor's peak loading at 30 months; 0.0609 a month × 12 = 0.7308 a year.
- <u>country (str):</u> "United States" (default, 5 to 30 years), "United Kingdom" (3 to 40 years, against the Retail Prices Index), or "Germany" or "Euro Area" (German bonds paying euro area inflation).
- <u>volatility (str):</u> "history" (default) for random inflation around the curve, or "none" to follow the curve exactly in every scenario.
- <u>source (str):</u> "oecd" (default) or "gmdb", the consumer price history the volatility is fitted on.
- <u>period (str):</u> the frequency of that history, default "monthly".

**Returns:**

<u>BreakevenInflationParams &#124; DeterministicPathParams:</u> the curve's `level`, `slope`, `curvature` and `decay`, `initial_value` (today's rate) and, with volatility "history", `mean_reversion_speed` and `volatility`.

**Raises:**

- <u>ValueError:</u> if `country`, `decay`, `volatility`, `source` or `period` is not valid, or no date has every maturity quoted (for the United States, an `end_date` before February 2010).

</details>

## names

The names of every inflation entry calibrated so far, in calibration order.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
inflation.names  # property -> list[str]
```

</details>

## params

The calibrated parameters for one inflation entry.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
params(
    name: str,
) -> OUParams | GARCHParams | OUCovariateParams | AR1Params | MovingTargetOUParams | DeterministicPathParams
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

</details>

## step_function

The one-period inflation update for a method: Wilkie's AR(1) for "wilkie_ar1" and the exact
Ornstein-Uhlenbeck step otherwise.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
Inflation.step_function(method: str)
```

**Args:**

- <u>method (str):</u> "ou" or "wilkie_ar1".

</details>

## series

The historical inflation rate for one entry. Factors that respond to the level of inflation, such as the
dividend yield's `condition_on_inflation`, are fitted against it.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
series(name: str) -> pl.Series
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

</details>

## dates

The dates that go with `series(name)`, in the same order, so another factor can match its own data to this
inflation rate by date rather than by position.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
dates(name: str) -> pl.Series
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

</details>

## changes

Dated period-over-period changes in one entry's inflation rate: the history its correlations with the other
factors are estimated from.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
changes(name: str) -> pl.DataFrame
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

</details>

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

### fit_wilkie_ar1

Fit Wilkie's (1986) inflation AR(1) on year-apart observations, and scale it to the simulation step.

Wilkie's persistence QA is a yearly coefficient: the share of this year's gap to the long-run mean that is left next
year. Year-over-year inflation sampled monthly overlaps: two neighbouring months share 11 of their 12 months of
price changes, so a month-to-month regression measures that overlap rather than how inflation itself fades, and
reads 0.9 to 0.99 a month even when a shock is gone within a year. Here each value is regressed on the value one
year earlier instead, which measures exactly what QA means. Wilkie's own values on UK data (yearly from 1919 to 1982,
section 2.11) are QMU = 0.05, QA = 0.6 and QSD = 0.05 (section 3.4); a fit on a short, calm
history can land far from them, as US inflation from 1995 to 2007 does (QA near 0, QSD 0.8%), so check the fitted
values against that benchmark. US inflation since 1919 (Shiller's yearly series, `history_source: shiller`) gives
QMU 2.6%, QA 0.54 and QSD 3.4%, which is what the shipped Wilkie preset uses.

The yearly AR(1) is then stepped at the run's frequency with a persistence per step chosen so that the long-run
uncertainty of the price level stays Wilkie's: an average of simulated inflation over many years varies as much as
it does in the yearly model, so indexed cash flows far out carry the right spread. For persistent inflation (QA of
0.6 or more) this per-step value is within 0.001 of QA^(1/k), so sampled once a year the simulated inflation is
Wilkie's AR(1) again. When a year keeps little of the year before, it stays near 0.85 a month, so neighbouring
months still move together as overlapping year-over-year rates do, where a plain k-th root would make every month
an independent draw and understate the price level's spread. The shock is scaled so the spread of inflation
itself, QSD / sqrt(1 - QA^2), stays the same.

The formula is as follows:

$$
I_{t} = \text{QMU} + \text{QA} \cdot (I_{t-1} - \text{QMU}) + \text{QSD} \cdot e_{t}
$$

$$
(1 + \phi) / (1 - \phi) = k \cdot (1 + \text{QA}) / (1 - \text{QA})
$$

$$
\sigma = \text{QSD} \cdot \sqrt{(1 - \phi ^{2}) / (1 - \text{QA} ^{2})}
$$

Where t counts years, so I_t-1 is year-over-year inflation one year (k observations) before I_t, k is the number
of observations per year (12 monthly, 4 quarterly, 1 yearly), QMU the long-run mean, QA and QSD the yearly
persistence and shock size fitted by least squares on all year-apart pairs, and phi and sigma the persistence and
shock size per step the simulation uses. The second line equates the long-run variance of the two processes'
averages. With yearly data, phi = QA and this is Wilkie's own fit.

**References:**

- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. Sections 3.3-3.4. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_wilkie_ar1(inflation_rate: pl.Series, steps_per_year: int = 1) -> AR1Params
```

**Args:**

- <u>inflation_rate (pl.Series):</u> the year-over-year inflation history, evenly spaced, as decimals.
- <u>steps_per_year (int):</u> observations per year, which is also the simulation's steps per year. Defaults to 1.

**Returns:**

<u>AR1Params:</u> the long-run mean, the persistence and shock size per step, and the latest inflation rate.

**Raises:**

- <u>ValueError:</u> if the history is too short, or the yearly persistence is not between -1 and 1, so inflation would not settle at a long-run level.

</details>

### wilkie_ar1_per_step

Turn a yearly inflation AR(1) (Wilkie's QMU, QA, QSD) into the per-step AR(1) a monthly or quarterly run steps
with, keeping the long-run spread of inflation and of the price level; see `fit_wilkie_ar1` for the reasoning.

The formula is as follows:

$$
(1 + \phi) / (1 - \phi) = k \cdot (1 + \text{QA}) / (1 - \text{QA})
$$

$$
\sigma = \text{QSD} \cdot \sqrt{(1 - \phi ^{2}) / (1 - \text{QA} ^{2})}
$$

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
wilkie_ar1_per_step(yearly: AR1Params, steps_per_year: int) -> AR1Params
```

**Args:**

- <u>yearly (AR1Params):</u> the yearly fit, persistence QA and shock size QSD per year.
- <u>steps_per_year (int):</u> k, the simulation's steps per year; 1 returns `yearly` unchanged.

**Returns:**

<u>AR1Params:</u> the same long-run mean and starting value, with the persistence and shock size per step.

</details>

### fit_inflation_ou

Fit the Ornstein-Uhlenbeck inflation process on year-apart observations, so the overlap of monthly
year-over-year rates does not pass for slow mean reversion.

Two neighbouring monthly year-over-year rates share 11 of their 12 months of price changes, so a month-to-month
fit reads that overlap as persistence. On US inflation since 1960 it gives a speed of 0.13 a year, which keeps 88%
of a gap after a year, where the data keep 73% (a value regressed on the value a year earlier); since 2000 it keeps
66% where the data keep 26%. Too slow a pull leaves a spike in place for years and overstates long-run price-level
uncertainty. This fit is `fit_wilkie_ar1` written as an OU process: an OU stepped at the data's frequency makes the
same moves as Wilkie's per-step AR(1), so the two methods agree on the same history. With yearly data it is the
plain exact OU fit (`fit_ou_process`). Ahlgrim, D'Arcy and Gorvett (2005, section 3) do the same for their OU
inflation, choosing its parameters from annual regressions because monthly data are noisy: they find a speed of
0.37 on 1913-2001 and 0.47 on 1946-2001 and choose 0.4; this fit gives 0.32 on US inflation since 1960.

The formula is as follows:

$$
a = - k \cdot \ln(\phi)
$$

$$
\sigma = \text{sigma\_step} \cdot \sqrt{2 \cdot a / (1 - \phi ^{2})}
$$

Where phi and sigma_step are the per-step persistence and shock size of `fit_wilkie_ar1` and k the observations
per year, so the stationary spread sigma / sqrt(2a) equals that of the data.

**References:**

- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. Sections 3.3-3.4. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>
- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. Section 3. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_inflation_ou(inflation_rate: pl.Series, steps_per_year: int = 1) -> OUParams
```

**Args:**

- <u>inflation_rate (pl.Series):</u> the year-over-year inflation history, evenly spaced, as decimals.
- <u>steps_per_year (int):</u> observations per year (12 monthly, 4 quarterly, 1 yearly). Defaults to 1.

**Returns:**

<u>OUParams:</u> the yearly mean-reversion speed, long-run mean, yearly volatility and the latest inflation rate.

**Raises:**

- <u>ValueError:</u> if the history is too short, or inflation shows no pull toward a long-run level (with yearly data, a year-apart persistence of zero or below, which an OU process cannot hold).

</details>

### step_ar1

Move inflation one period forward under Wilkie's (1986) model, the classic UK actuarial inflation model.

Wilkie models the force of inflation (the log change in the price index) as an AR(1): each period keeps a fixed
share of last period's gap to the long-run mean and adds a normal shock. A persistence near one means shocks fade
slowly, so scenarios can show long stretches of high or low inflation; the stationary spread of inflation is
QSD / sqrt(1 - QA^2), wider than one period's shock.

The formula is as follows:

$$
I_{t} = \text{QMU} + \text{QA} \cdot (I_{t-1} - \text{QMU}) + \text{QSD} \cdot z_{t}
$$

Where I_t is the inflation rate, QMU is `long_run_mean`, QA is `persistence` and QSD is `volatility`, all per
simulation step. Wilkie's persistence is yearly; at a monthly or quarterly step the fit (`fit_wilkie_ar1`) turns
it into a per-step value with the same long-run spread of inflation and of the price level. The
simulation frequency must equal the entry's `period`.

**References:**

- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. Sections 3.3-3.4. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_ar1(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: AR1Params,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> this period's inflation rate.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw.
- <u>time_step (float):</u> not used; the period is fixed by the calibration.
- <u>params (AR1Params):</u> calibrated long-run mean, persistence, and volatility.

**Returns:**

<u>np.ndarray:</u> inflation one period later.

</details>

### step_ou

Move inflation one step forward under the Ornstein-Uhlenbeck process d(pi_t) = a * (theta - pi_t) * dt + sigma *
dW_t, the default inflation model.

Inflation is pulled toward its long-run level theta at speed a: a gap halves in ln(2) / a years, and the
long-run spread of inflation around theta is sigma / sqrt(2a). This matches how inflation behaves under a
central bank with a target, where shocks fade over a few years, and is the inflation generator of Ahlgrim and
D'Arcy (2012). The step uses the exact transition (as for the Vasicek short rate), so the result is the same
whether you simulate monthly or yearly.

The formula is as follows:

$$
\pi(t + \text{dt}) = \theta + (\pi(t) - \theta) \cdot \exp(- a \cdot \text{dt}) + \sigma \cdot \sqrt{(1 - \exp(- 2 \cdot a \cdot \text{dt})) / (2 \cdot a)} \cdot z
$$

Where a is `mean_reversion_speed`, theta `long_run_mean`, sigma `volatility` and z a standard normal draw.
Nothing stops inflation from going negative, so deflation scenarios occur with the probability the history
implies.

**References:**

- Ahlgrim, K.C., D'Arcy, S.P. (2012). "A User's Guide to the Inflation Generator." Casualty Actuarial Society, Canadian Institute of Actuaries, Society of Actuaries. <https://www.soa.org/globalassets/assets/files/research/projects/research-2012-02-effect-deflation-user-guide.pdf>
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>
- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. Section 5, eqs. (25)-(26), p. 185: the exact transition used here. <https://doi.org/10.1016/0304-405X(77>)90016-2

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_ou(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: OUParams,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's inflation rate.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw.
- <u>time_step (float):</u> the step length, in years.
- <u>params (OUParams):</u> calibrated mean-reversion speed, long-run mean, and volatility.

**Returns:**

<u>np.ndarray:</u> inflation one step later.

</details>

### breakeven_forward

Today's breakeven inflation forward at each horizon: the Nelson-Siegel forward from the shortest quoted maturity
on, and the fitted breakeven at that maturity held flat before it.

Breakevens are quoted from three (UK) or five years (US, Germany) out, so a Nelson-Siegel forward read at shorter
horizons is an extrapolation the data do not support: on 2026-10-14 it started the German curve at 5.72% against
a 2.28% five-year quote, and the UK one at 7.76% against a 4.03% three-year quote. Below the shortest maturity the
forward is held at the fitted yield there, the constant-forward rule EIOPA applies before its first quoted
maturity (RFR Technical Documentation EIOPA-BoS-26/198, Annex D.8.2, where a constant forward sets f_j-1,j = f_j =
f_1 = r_t1 for j = 1, 2, ..., t1, and D.8.3, which gives the spot rates z_j = r_t1 for the same j).
The accumulated forward to the shortest maturity is unchanged, so every breakeven yield from that maturity on is
still the Nelson-Siegel one and inflation-linked cashflows from there are priced as before.

The formula is as follows:

$$
f_{BE}(t) = y_{NS}(T_{1}) \text{for}\; t < T_{1}
$$

$$
f_{BE}(t) = L + S \cdot \exp(- \lambda \cdot t) + C \cdot \lambda \cdot t \cdot \exp(- \lambda \cdot t) \text{for}\; t \geq T_{1}
$$

Where T1 is `params.shortest_maturity` and y_NS the Nelson-Siegel yield; with T1 = 0 this is the plain forward.

**References:**

- EIOPA (2026). "RFR Technical Documentation", EIOPA-BoS-26/198, Annex D.8. <https://www.eiopa.europa.eu/eiopa-publishes-rfr-technical-documentation-become-applicable-30-january-2027-2026-05-26_en>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
breakeven_forward(
    elapsed_time: float | np.ndarray,
    params: DeterministicPathParams,
) -> float | np.ndarray
```

**Args:**

- <u>elapsed_time (float &#124; np.ndarray):</u> years since the valuation date.
- <u>params (DeterministicPathParams):</u> today's breakeven curve and its shortest quoted maturity.

**Returns:**

<u>float &#124; np.ndarray:</u> the breakeven forward, one value per time given.

</details>

### breakeven_inflation_centre

The path risk-neutral inflation is centred on: the breakeven forward minus the convexity correction that keeps
the expected price index on the breakeven curve.

The formula is as follows:

$$
\alpha_{I}(t) = f_{BE}(0,\; t) - \sigma ^{2} / (2 \cdot a ^{2}) \cdot (1 - \exp(- a \cdot t)) ^{2}
$$

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
breakeven_inflation_centre(
    elapsed_time: float | np.ndarray,
    params: BreakevenInflationParams,
) -> float | np.ndarray
```

**Args:**

- <u>elapsed_time (float &#124; np.ndarray):</u> years since the valuation date.
- <u>params (BreakevenInflationParams):</u> today's breakeven curve and the historical speed and volatility.

**Returns:**

<u>float &#124; np.ndarray:</u> alpha_I(t), one value per time given.

</details>

### step_breakeven_inflation

Move risk-neutral inflation one step: its gap to the breakeven-implied path decays at the fitted speed and takes a
normal shock, the exact Ornstein-Uhlenbeck transition.

The formula is as follows:

$$
\pi(t + \text{dt}) = \alpha_{I}(t + \text{dt}) + (\pi(t) - \alpha_{I}(t)) \cdot \exp(- a \cdot \text{dt}) + s \cdot z
$$

$$
s = \sigma \cdot \sqrt{(1 - \exp(- 2 \cdot a \cdot \text{dt})) / (2 \cdot a)}
$$

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_breakeven_inflation(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    elapsed_time: float,
    params: BreakevenInflationParams,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> this step's inflation in each scenario.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw.
- <u>time_step (float):</u> the step length, in years.
- <u>elapsed_time (float):</u> years since the valuation date at the start of this step.
- <u>params (BreakevenInflationParams):</u> today's breakeven curve and the historical speed and volatility.

**Returns:**

<u>np.ndarray:</u> inflation one step later.

</details>
