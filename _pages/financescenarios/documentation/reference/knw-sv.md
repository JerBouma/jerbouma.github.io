---
title: "KnwSv"
seo_title: "KnwSv Reference – Finance Scenarios"
excerpt: "The KNW model with stochastic volatility."
description: "The KNW model with stochastic volatility."
author_profile: false
permalink: /projects/financescenarios/docs/reference/knw-sv
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

The KNW model with stochastic volatility. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.models.knw_sv.knw_sv_controller import KnwSv
```

```python
KnwSv(toolkit: Toolkit)
```

The KnwSv module simulates the interest rate and inflation as a two-way coupled pair, like `Knw`, plus a shared,
hidden "market nervousness" factor `v` that makes both swing harder in turbulent periods and calmer in quiet ones.

`Knw` gives the rate and inflation a fixed amount of randomness every period. Real markets have spells of calm and
stress, which the CP2022 model of De Nederlandsche Bank (DNB), the Dutch central bank, captures with a random
variance factor scaling the volatility of everything; this class brings it back. One instance holds any number of
pairs, one `calibrate_triple()` call each.

The model is the stochastic-volatility form of [Koijen, Nijman & Werker (2010)](https://doi.org/10.1093/rfs/hhp058)
that the [CP2022 Technical Appendix (2022)](
https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix) specifies (eq. 2-5).
`v` follows a CIR process ([Cox, Ingersoll & Ross, 1985](https://doi.org/10.2307/1911242)), the mean-reverting,
never-negative variance process of [Heston (1993)](https://doi.org/10.1093/rfs/6.2.327), and both legs read its
previous level in their drift and variance:

```text
r(t)  = c_r  + gamma_r*v(t-1)  + phi_rr*r(t-1)   + phi_r_pi*pi(t-1)
        + sqrt(base_r  + sens_r*v(t-1))*z_r(t)
pi(t) = c_pi + gamma_pi*v(t-1) + phi_pi_r*r(t-1) + phi_pipi*pi(t-1)
        + sqrt(base_pi + sens_pi*v(t-1))*z_pi(t)
```

With `variance_coupling` (gamma) and `variance_sensitivity` (sens) at zero this is exactly `Knw`. `v` is simulated
with [Andersen's (2008)](https://doi.org/10.21314/jcf.2008.189) QE scheme, which never goes negative.

Unlike DNB, which recovers `v` from market yields, `v` is estimated here from history: a rolling average of the
pair's squared surprises. An optional equity leg (`calibrate_equity_leg`) reads the same `v`, so stock and rate
turbulence rise together: it earns the short rate plus a constant risk premium, with variance scaled by `v`, fit
on price history only (DNB also uses option prices).

Configuration (both entries of a pair, plus an optional equity entry, in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `interest_rates[i].method` | `hull_white` | Set to `knw_sv` to make this entry the pair's rate leg. |
| `interest_rates[i].inflation_name` | `inflation` | The `name` of the paired `inflation[j]` entry. |
| `interest_rates[i].period` | `daily` | Shared by every entry using this `v`, equal to `engine.frequency`. |
| `inflation[j].method` | `ou` | Set to `knw_sv` to make this entry the pair's inflation leg. |
| `inflation[j].interest_rate_name` | `interest_rate` | The `name` of the paired `interest_rates[i]` entry. |
| `equities[k].method` | (regime switching) | Set to `knw_sv` for an equity leg on the pair's `v`. |
| `equities[k].nominal_rate_name` | `null` | Required for `knw_sv`: the pair's rate entry `name`. |

Data sources and pairing rules are as for `Knw`, and a `knw_sv` entry's partner must also be `knw_sv`. Every
entry sharing a `v`, the equity leg included, must use one `period` equal to `engine.frequency`, which the config
enforces: a mismatch compounds the fit too fast or too slow. `measure: risk_neutral` on both entries simulates
under `KnwSvQ`'s Q-measure; an equity leg cannot name such a rate.

**References:**

- Koijen, R.S.J., Nijman, T.E., Werker, B.J.M. (2010). "When Can Life Cycle Investors Benefit from Time-Varying Bond Risk Premia?" The Review of Financial Studies, 23(2), 741-780. <https://doi.org/10.1093/rfs/hhp058>
- Commissie Parameters (2022). "Technical Appendix: Specification of the CP2022 Model." <https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix>

## calibrate_triple

```python
calibrate_triple(
    interest_rate_name: str,
    inflation_name: str,
    period: str,
    interest_rate_source: str = 'oecd',
    interest_rate_ticker: str = '^IRX',
    interest_rate_country: str = 'United States',
    interest_rate_term: str = 'short',
    inflation_country: str = 'United States',
) -> tuple[OUParams, KnwSvLegParams, KnwSvLegParams]
```

Calibrate one `v`, interest rate and inflation triple: fetch both histories, estimate the hidden turbulence
factor `v`, and fit how each leg depends on `v`, itself and the other leg.

`v_params` give the turbulence's normal level (`long_run_mean`), how fast a spike fades (`mean_reversion_speed`,
a half-life of ln 2 / speed years) and how jumpy it is (`volatility`). A leg's `variance_sensitivity` says how
much its per-period variance grows with `v`, and `variance_coupling` how much `v` shifts its expected next
value; the rest reads as in `Knw.calibrate_pair`.

The surprises of a constant-volatility fit, averaged over four periods and lagged one, stand in for `v`; a CIR
process ([Cox, Ingersoll & Ross, 1985](https://doi.org/10.2307/1911242)) is fit to that, and both legs are
refit with `v` as an extra input. If no leg's variance rises with `v`, a warning suggests `method: knw`. `v`'s
parameters are stored under `variance_factor_name(interest_rate_name)`.

**Args:**

- <u>interest_rate_name (str):</u> the rate leg's name, its key in `params()` and the simulation.
- <u>inflation_name (str):</u> the inflation leg's name.
- <u>period (str):</u> the shared sampling frequency, also the simulation's: "monthly", "quarterly" or "yearly".
- <u>interest_rate_source (str):</u> "oecd" or "ticker", as in `Knw.calibrate_pair`. Defaults to "oecd".
- <u>interest_rate_ticker (str):</u> the ticker for the "ticker" source. Defaults to "^IRX".
- <u>interest_rate_country (str):</u> the country for the "oecd" source. Defaults to "United States".
- <u>interest_rate_term (str):</u> "short" or "long" OECD rate. Defaults to "short".
- <u>inflation_country (str):</u> the country of the OECD consumer price index. Defaults to "United States".

**Returns:**

<u>tuple[OUParams, KnwSvLegParams, KnwSvLegParams]:</u> (v_params, interest_rate_params, inflation_params).

**Raises:**

- <u>ValueError:</u> if fewer than 11 dates overlap, or the fitted coupling is not stationary.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.models.knw_sv.knw_sv_controller import KnwSv

toolkit = Toolkit(["^IRX"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1990-01-01")
knw_sv = KnwSv(toolkit)

knw_sv.calibrate_triple("interest_rate", "inflation", period="quarterly")
```

Which returns (calibrated on 2026-10-05):

| | mean_reversion_speed | long_run_mean | initial_value |
|:--|---------------------:|--------------:|--------------:|
| v | 0.3988 | 0.0000627 | 0.0000094 |

| leg | variance_coupling | base_variance | variance_sensitivity |
|:----|------------------:|--------------:|---------------------:|
| interest_rate | -5.5025 | 0.0000152 | 0.0322 |
| inflation | -0.2861 | 0.0000099 | 0.5858 |

`v` halves in about 1.7 years and sits below its normal level, so the pair is calmer than usual.

## calibrate_equity_leg

```python
calibrate_equity_leg(
    equity_name: str,
    interest_rate_name: str,
    inflation_name: str,
    equity_prices: pl.Series,
    equity_dates: pl.Series,
    period: str,
) -> KnwSvEquityParams
```

Calibrate an equity index that shares an already calibrated knw_sv pair's turbulence factor `v`.

The index earns the simulated short rate plus a constant risk premium, and its swings grow when `v` is high.
`risk_premium` is the extra log return per period over the short rate (0.02 a quarter is roughly 8% a year),
`base_variance` the per-period variance when `v` is zero, and `variance_sensitivity` how much variance each
unit of `v` adds. Without a link to `v`, `variance_sensitivity` is 0 and a warning says so.

This is the equity row of DNB's [CP2022 Technical Appendix](
https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix) (eq. 4-5), a
[Heston (1993)](https://doi.org/10.1093/rfs/6.2.327) style index on a random short rate:
`d ln(S) = (r + risk_premium - 0.5*var)dt + sqrt(var)dW`, with `var = base_variance + variance_sensitivity*v`.
It is fit on price history only, where DNB also uses option prices, and runs under the real-world measure only.

**Args:**

- <u>equity_name (str):</u> the equity leg's name, its key in `params()` and the simulation.
- <u>interest_rate_name (str):</u> the rate leg's name of the already calibrated pair to share `v` with.
- <u>inflation_name (str):</u> the same pair's inflation leg's name.
- <u>equity_prices (pl.Series):</u> historical index levels (not returns).
- <u>equity_dates (pl.Series):</u> the dates of `equity_prices`, same length.
- <u>period (str):</u> the pair's sampling frequency as passed to `calibrate_triple`: "monthly", "quarterly" or "yearly".

**Returns:**

<u>KnwSvEquityParams:</u> `risk_premium`, `base_variance`, `variance_sensitivity` and `initial_value` (the last price).

**Raises:**

- <u>ValueError:</u> if `period` is not supported, the prices and dates differ in length, or fewer than 6 dates overlap with the pair.
- <u>RuntimeError:</u> if `calibrate_triple` has not been run for this pair.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.equities.equities_controller import fetch_equity_prices
from financescenarios.models.knw_sv.knw_sv_controller import KnwSv

toolkit = Toolkit(["^GSPC"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1990-01-01")
knw_sv = KnwSv(toolkit)
knw_sv.calibrate_triple("interest_rate", "inflation", period="quarterly")

dates, prices = fetch_equity_prices(toolkit, "^GSPC", "quarterly")
knw_sv.calibrate_equity_leg("equity", "interest_rate", "inflation", prices, dates, period="quarterly")
```

Which returns (calibrated on 2026-10-05):

| name | risk_premium | base_variance | variance_sensitivity | initial_value |
|:-----|-------------:|--------------:|---------------------:|--------------:|
| equity | 0.0159 | 0.0042 | 26.0769 | 7773.95 |

The S&P 500 earned 1.59% a quarter above the short rate, with a volatility of about 13% a year at `v = 0` and
15.3% at `v`'s long-run level.

## names

```python
knwsv.names  # property -> list[str]
```

The names of everything calibrated so far, in calibration order: both legs of every pair, each pair's
`v` (see `variance_factor_name`) and any equity leg.

## params

```python
params(name: str) -> OUParams | KnwSvLegParams
```

The calibrated parameters of one knw_sv leg or `v`: an `OUParams` for `v`, a `KnwSvLegParams` for an
interest rate or inflation leg, a `KnwSvEquityParams` for an equity leg.

**Args:**

- <u>name (str):</u> the leg's name, or `variance_factor_name(interest_rate_name)` for a pair's `v`.

**Raises:**

- <u>RuntimeError:</u> if nothing has been calibrated under this name yet.

## series

```python
series(name: str) -> pl.Series
```

The historical series one knw_sv leg was calibrated on (`v` has no series of its own).

**Args:**

- <u>name (str):</u> the leg's name, as passed to calibrate_triple().

**Raises:**

- <u>RuntimeError:</u> if calibrate_triple(...) naming this leg hasn't been called yet.

## dates

```python
dates(name: str) -> pl.Series
```

The dates paired with series(name), same length and order.

**Args:**

- <u>name (str):</u> the leg's name, as passed to calibrate_triple().

**Raises:**

- <u>RuntimeError:</u> if calibrate_triple(...) naming this leg hasn't been called yet.

## changes

```python
changes(name: str) -> pl.DataFrame
```

The dated period-over-period changes of one knw_sv leg, used to estimate its correlation with other factors
without fetching the data again.

**Args:**

- <u>name (str):</u> the leg's name, as passed to calibrate_triple().

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if calibrate_triple(...) naming this leg hasn't been called yet.
