---
title: "FX"
seo_title: "FX Reference – Finance Scenarios"
excerpt: "Exchange rates, one per currency against the US dollar."
description: "Exchange rates, one per currency against the US dollar."
author_profile: false
permalink: /projects/financescenarios/docs/reference/fx
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Exchange rates, one per currency against the US dollar. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.factors.fx.fx_controller import FX
```

```python
FX(toolkit: Toolkit)
```

The FX module simulates exchange rates: how many units of a foreign currency one US
dollar buys, such as euros, yen or pounds per dollar, and how that rate could move over
the years ahead.

In plain terms: add one or more currency pairs to a run, and each becomes a variable in
the simulated scenarios, linked to interest rates, equities and the rest through the
correlation matrix. That is what a portfolio holding foreign assets, or a report in a
currency other than the dollar, needs. It is opt-in: `fx` is an empty list by default,
and each entry is calibrated independently and named by its own `name`.

The model is a geometric Brownian motion (GBM): a random walk in the logarithm of the
rate, so the simulated rate can rise or fall without limit but never turns negative,

```text
d(log S) = (mu - 0.5 * sigma^2) dt + sigma * dW
```

where `mu` (`drift`) is the annualized expected log-return and `sigma`
(`volatility`) the annualized log-return volatility. Unlike every other factor here
(interest rates, inflation, unemployment, real estate, credit spreads, the leading
indicator, the yield curve), an exchange rate has no natural long-run level to revert to
over a multi-decade horizon, so it is not mean-reverting. The standard treatment,
surveyed in
[Gorvett (2001)](https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf),
is GBM: the same lognormal shape the equity module uses for stock prices, without the
regime switching.

Options that change the model:

- `drift_mode="irp"`: instead of a fixed historical drift, the drift at every
  simulated step is the gap between two simulated short rates, foreign minus domestic,
  following uncovered interest rate parity (the currency with the higher interest rate
  is expected to depreciate by roughly the rate gap). This is the one place FX depends
  directly on other factors; see `calibrate`.
- `measure="risk_neutral"`: a static drift from covered interest rate parity (the
  no-arbitrage link between the spot rate, the forward rate and the two interest
  rates), set once from today's rate levels; see `calibrate_risk_neutral`.
- `source="gmdb"`: the Global Macro Database instead of the OECD, for countries
  outside the OECD roster such as Brazil, India or China, at yearly frequency only.

Data: `Toolkit.economics.get_exchange_rates(countries=..., period=...,
gmdb_source=...)`, quoted as national currency per US dollar. The default OECD series
covers the major economies (Euro area, United Kingdom, Japan, Switzerland, Canada,
Australia, ...), not a single US trading partner. It is keyed by currency *area*, not
member state: use `EA20` for the euro area, not `Germany`, which has no exchange-rate
series of its own here even though it is a valid `country` for interest rates,
inflation and unemployment. No API key is needed. The OECD API rate-limits bursts of
requests; a rate-limited fetch comes back empty and the calibration fails for that
entry, so wait a minute and retry.

What it does not do: each pair is one more correlated factor, not a full multi-currency
re-architecture in which every other factor is re-denominated per currency. Apart from
`drift_mode="irp"`, an FX entry has no cascade dependency on any other factor. There is
no FX options data source, so volatility is always historical (no implied volatility).

Configuration (`fx[i]` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `name` | `fx` | The factor's name in the simulated output; unique across the list. |
| `country` | `EA20` | The country or currency area paired against the US dollar. |
| `currency` | `null` | Quoted currency (e.g. `EUR`) for reporting; else from a same-country rate or `EA20`. |
| `source` | `oecd` | `oecd` or `gmdb` (Global Macro Database, `period: yearly` only). |
| `period` | `monthly` | `monthly`, `quarterly` or `yearly` for `oecd`; `yearly` for `gmdb`. |
| `measure` | `real_world` | `real_world` (historical fit) or `risk_neutral` (covered parity drift). |
| `drift_mode` | `historical` | `historical` (fitted drift), `irp` (per-step rate gap) or `random_walk` (no trend). |
| `domestic_rate_name` | `null` | Required with `drift_mode: irp`: the `interest_rates[].name` of the USD leg. |
| `foreign_rate_name` | `null` | With `drift_mode: irp`: the foreign leg; defaults to `<country>_short_rate`. |
| `beliefs.drift` | `null` | Override the fitted annualized log-return drift. |
| `beliefs.volatility` | `null` | Override the fitted volatility; must be > 0. |

`domestic_rate_name` has no natural default, since several `interest_rates` entries may
exist and none is canonically "the USD one". `foreign_rate_name` defaults to this
entry's `country`, slugified, plus `_short_rate` (e.g. `ea20_short_rate`), the same
auto-pairing convention `unemployment[i].inflation_name` uses. Whenever any entry uses
`drift_mode: irp`, both names must resolve to configured `interest_rates[].name`
entries, checked when the configuration is validated. A `gmdb` entry with a monthly or
quarterly `period` is rejected up front rather than silently truncated to yearly.

Beliefs: a field left `null` keeps the calibrated value; the substitution happens per
entry in `config_model.apply_fx_beliefs`. In a regime YAML, address one entry's beliefs
with a dotted `"fx.<name>"` key. `beliefs.drift` together with `drift_mode: irp` is
rejected at validation (the per-step rate gap replaces the drift, so the override
would be silently ignored); only `beliefs.volatility` applies there. Any belief on a
`measure: risk_neutral` entry is rejected too (see `calibrate_risk_neutral`).

**References:**

- Gorvett, R.W. (2001). "Foreign Exchange Rate Risk: Institutional Issues and Stochastic Modeling." CAS Discussion Paper Program. <https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf>

## calibrate

```python
calibrate(
    name: str,
    country: str = 'EA20',
    period: str = 'monthly',
    source: str = 'oecd',
    drift_mode: str = 'historical',
) -> FXParams
```

Calibrate one currency pair from its history: fetch the USD exchange rate against
`country`'s currency and fit its expected annual log-return (`drift`) and how much
it swings (`volatility`).

In plain terms: this learns from the past how far and how fast a currency has
moved against the dollar, so the simulated scenarios move by similar amounts. A
volatility of 0.06 means a typical year moves the rate by about 6% either way; a
drift near 0 means no built-in tendency for the dollar to strengthen or weaken.

The fit is the standard closed-form maximum-likelihood estimate for GBM
(`fx_model.fit_fx_process`), no regression needed: the sample standard deviation
of log-returns, annualized by the time step, is the volatility, and their sample
mean, annualized, plus `0.5 * volatility^2`, is the drift. `initial_value` is the
last observed rate, in units of the foreign currency per US dollar. Simulation uses
the *exact* one-step solution (`fx_model.step_fx_process`), not an Euler-Maruyama
approximation,

```text
S_next = S * exp((mu - 0.5 * sigma^2) * dt + sigma * sqrt(dt) * shock)
```

so the simulated rate is always strictly positive and no discretization error is
introduced.

With `drift_mode="irp"`, the fixed drift is instead replaced at every simulated
step by the instantaneous gap between two already-simulated short rates, foreign
minus domestic. This is uncovered interest rate parity (UIP): the currency with
the higher interest rate is expected to depreciate against the lower-rate one by
roughly the rate gap, the no-arbitrage benchmark that equates a covered forward
position with an uncovered spot position. Because the rate is quoted as foreign
currency per USD, a *higher* USD rate makes the quote fall (US rate 5%, euro rate
0% drives the euros-per-dollar quote down). It is the dynamic, real-world
counterpart of the static covered-parity drift `calibrate_risk_neutral` sets once;
the two could both be set, but `drift_mode="irp"` under the real-world measure,
with volatility still fitted from history, is the combination anyone would want.
Mechanically, it mirrors business-cycle conditioning generalized from one
covariate to a rate differential:

- `fx_model.fit_fx_process_irp` fits only `volatility` and `initial_value`, with
  the same log-return calculation; the `drift` it returns is the historical GBM
  drift, kept only as an audit figure for comparing fitted and implied drift.
- `fx_model.step_fx_process_irp` is the same exact GBM step with `drift` replaced by
  the step's rate differential.
- `scenarios_controller.py` gives the entry a real dependency on
  `domestic_rate_name` and the resolved `foreign_rate_name`, so within each step
  both rates are simulated first and their already-advanced *levels* (not their
  step-to-step changes) form the differential.

Also known as: geometric Brownian motion FX model, lognormal exchange-rate model,
random-walk exchange rate.

**Args:**

- <u>name (str):</u> this pair's name, used to key params()/changes() and as the factor name in the simulation (e.g. "eur", "jpy", "gbp").
- <u>country (str):</u> the country whose currency to pair against the US dollar (the exchange rate is quoted as units of that currency per USD). Use "EA20" for the euro area with source="oecd".
- <u>period (str):</u> sampling frequency of the underlying data ("monthly", "quarterly", "yearly" for source="oecd"; "yearly" only for source="gmdb"), determines the time step used to fit.
- <u>source (str):</u> "oecd" (the default, Finance Toolkit's OECD exchange rate) or "gmdb" (its Global Macro Database, which covers countries outside the OECD roster, period="yearly" only).
- <u>drift_mode (str):</u> "historical" (default, fit_fx_process: a fixed GBM drift consumed by step_fx_process), "random_walk" (fit_fx_process_random_walk: the historical volatility with no trend, so the median rate stays flat) or "irp" (fit_fx_process_irp: fits volatility only, since a drift_mode="irp" entry's drift is replaced every simulated step by the dynamic foreign-minus-domestic short-rate differential, wired downstream in scenarios_controller.py, which is the only place that sees both this FX pair and the two interest_rates entries it depends on). Mirrors how interest_rates_controller.InterestRates.calibrate() branches its own fitter on volatility_model/business_cycle_covariate.

**Returns:**

<u>FXParams:</u> the calibrated process parameters.

**Raises:**

- <u>ValueError:</u> if period, source, or drift_mode is not recognized, period isn't "yearly" for source="gmdb", Finance Toolkit returns no exchange rate for `country` (an individual euro-area member under source="oecd", an unsupported country, or a rate-limited OECD request), or fewer than 3 observations or a non-positive rate reach the fit.

**Notes:**

- The OECD series has no column for an individual eurozone member, so
  `country="Germany"` fails with a hint to use `"EA20"`, or `source="gmdb"`
  (yearly) for a national series.
- The Global Macro Database is annual only; everything else (`drift_mode`,
  beliefs, `measure="risk_neutral"`) works the same as with the OECD source.
- `changes(name)` holds the dated log-changes in the rate, reused for the
  correlation matrix without a second fetch.
- The `irp` volatility is the plain historical log-return volatility, not a
  residual volatility after removing the UIP-implied return; that refinement is
  known and not implemented.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.fx.fx_controller import FX

toolkit = Toolkit(["AAPL"])
fx = FX(toolkit)

fx.calibrate("eur", country="EA20", period="monthly")
fx.calibrate("jpy", country="Japan", period="monthly")
fx.calibrate("gbp", country="United Kingdom", period="monthly")
fx.calibrate("brl", country="Brazil", period="yearly", source="gmdb")
```

Which returns (calibrated on 2026-10-04):

| name | drift | volatility | initial_value |
|:-----|------:|-----------:|--------------:|
| eur | 0.0019 | 0.0593 | 0.8625 |
| jpy | 0.0740 | 0.0867 | 158.7871 |
| gbp | 0.0043 | 0.0635 | 0.7383 |
| brl | -0.0145 | 0.0624 | 5.0517 |

A dollar buys 0.86 euros, 158.79 yen, 0.74 pounds and 5.05 reais today. Over the
Toolkit's default five-year window the yen has the largest swings (8.7% a year)
and a drift of 7.4% a year, the dollar's strong run against it in that window; the
euro and pound pairs drift close to zero. The yearly reais fit rests on only five
annual observations, so treat it as indicative, or widen `start_date`.

**References:**

- Gorvett, R.W. (2001). "Foreign Exchange Rate Risk: Institutional Issues and Stochastic Modeling." CAS Discussion Paper Program. <https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf>

## calibrate_risk_neutral

```python
calibrate_risk_neutral(
    name: str,
    domestic_rate: float,
    foreign_rate: float,
    volatility_source: str = 'historical',
    country: str = 'EA20',
    period: str = 'monthly',
    source: str = 'oecd',
) -> FXParams
```

Calibrate one currency pair under the risk-neutral (Q) measure: the drift is set by
covered interest rate parity from today's two interest rates, and the volatility is
the historical one.

In plain terms: a risk-neutral run asks what drift is consistent with today's
market prices, so that anything priced off the simulated exchange rate admits no
arbitrage, rather than how the rate has behaved. For a currency pair that drift is
fixed by the two interest rates: holding the higher-rate currency earns more
interest, so its forward price must be lower, and the drift is the foreign rate
minus the domestic (USD) rate. With a 4.25% US rate and a 2% euro rate, the
euros-per-dollar quote drifts down about 2.25% a year.

Covered interest rate parity is the no-arbitrage condition equating the forward
premium or discount on an exchange rate to the interest-rate differential between
the two currencies. Because the OECD quotes foreign currency per USD, the drift is
`foreign_rate - domestic_rate`, the same sign as `drift_mode="irp"`. Volatility
is unchanged from the historical GBM fit (`fx_model.fit_fx_process`): the parity
pins down only the drift, and a change of drift (a Girsanov change of measure)
leaves a GBM's volatility untouched. There is no FX options data source, so no
implied volatility.

This is a *static* drift computed once at calibration, not the dynamic per-step
conditioning of `drift_mode="irp"`. It adds no dependency and no new step
function: `fx_model.step_fx_process` is reused unchanged, and the result is a
plain `FXParams`, indistinguishable in shape from a real-world one.

`domestic_rate` and `foreign_rate` are not fetched here. In a configured run,
`calibration_controller.Calibration.calibrate_all()` passes the current levels of
the already-calibrated `interest_rates[]` entries whose `country` is
`"United States"` (domestic) and whose `country` matches this entry's `country`
(foreign), so "what counts as r today" is defined in exactly one place; a missing
entry for either leg raises a `ValueError` at calibration time.

Also known as: covered interest parity (CIP) drift, risk-neutral FX, Q-measure
exchange rate.

**Args:**

- <u>name (str):</u> this pair's name, used to key params()/changes() and as the factor name in the simulation.
- <u>domestic_rate (float):</u> today's domestic (USD) short rate (annualized, decimal fraction).
- <u>foreign_rate (float):</u> today's foreign short rate for `country` (annualized, decimal fraction).
- <u>volatility_source (str):</u> only "historical" is supported in v1 (no FX options data source exists to offer an implied alternative); kept as an explicit parameter for symmetry with Equities.calibrate_risk_neutral() and to make v1's single supported value self-documenting rather than implicit. Not a factor-set key; programmatic use only.
- <u>country (str):</u> the country whose currency to pair against the US dollar; same meaning as calibrate(), used to fetch the historical series volatility/initial_value are derived from.
- <u>period (str):</u> sampling frequency of the underlying data; same meaning as calibrate().
- <u>source (str):</u> "oecd" (the default) or "gmdb"; same meaning as calibrate().

**Returns:**

<u>FXParams:</u> drift = foreign_rate - domestic_rate, volatility and initial_value from the historical GBM fit.

**Raises:**

- <u>ValueError:</u> if volatility_source is not "historical", period or source is not recognized, period isn't "yearly" for source="gmdb", or no exchange rate comes back for `country`.

**Notes:**

- Configured through `fx[i].measure: risk_neutral`. Combining it with a non-empty
  `beliefs` block raises at configuration validation
  (`config_model._validate_no_beliefs_when_risk_neutral`): a risk-neutral drift is
  meant to match an observable market input exactly, and silently ignoring an
  override that is structurally compatible with `FXParams` would look as though it
  had been honored.
- Credit and single-factor commodities have no risk-neutral mode; equities,
  interest rates, inflation and Schwartz-Smith commodities do, each opted into per
  entry with its own `measure`.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.fx.fx_controller import FX

toolkit = Toolkit(["AAPL"])
fx = FX(toolkit)

fx.calibrate_risk_neutral("eur_q", domestic_rate=0.0425, foreign_rate=0.0200, country="EA20")
```

Which returns (calibrated on 2026-10-04):

| name | drift | volatility | initial_value |
|:-----|------:|-----------:|--------------:|
| eur_q | -0.0225 | 0.0593 | 0.8625 |

The drift is 2.00% - 4.25% = -2.25% a year: the euros-per-dollar quote is expected
to fall, while volatility and today's rate are exactly the historical fit of
`calibrate("eur", ...)` above.

**References:**

- Gorvett, R.W. (2001). "Foreign Exchange Rate Risk: Institutional Issues and Stochastic Modeling." CAS Discussion Paper Program. <https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf>

## names

```python
fx.names  # property -> list[str]
```

The names of every currency pair calibrated so far, in calibration order.

## params

```python
params(name: str) -> FXParams
```

The calibrated process parameters for one currency pair.

**Args:**

- <u>name (str):</u> the pair's name, as passed to calibrate().

**Raises:**

- <u>RuntimeError:</u> if calibrate(name, ...) hasn't been called yet.

## step_function

```python
fx.step_function  # property
```

The GBM step function for the FX process (stateless, shared across every pair).

## changes

```python
changes(name: str) -> pl.DataFrame
```

Dated period-over-period log-changes in one currency pair's exchange rate,
from the same data calibrate() already fetched, reused for cross-factor
correlation estimation (Dependence) instead of triggering a second
Finance Toolkit fetch.

**Args:**

- <u>name (str):</u> the pair's name, as passed to calibrate().

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` (pl.Date) and `value` (f64); see helpers.dated_changes().

**Raises:**

- <u>RuntimeError:</u> if calibrate(name, ...) hasn't been called yet.
