---
title: Interest Rates and Yield Curves
seo_title: Interest Rates Documentation – Finance Scenarios
excerpt: "The short-rate models, their data sources and options, the Nelson-Siegel government and credit curves, and the arbitrage-free HJM forward curve."
description: "How Finance Scenarios simulates interest rates: Hull-White, CIR, Wilkie and Hibbert short rates, Nelson-Siegel yield and credit curves, and HJM."
author_profile: false
permalink: /projects/financescenarios/docs/interest-rates
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Interest rates sit at the center of most scenario sets. They discount liabilities, drive bond returns, set the risk-free rate for equities and currencies, and move together with inflation. Finance Scenarios gives you three ways to model them: a single rate per country (a short-rate model), a whole government yield curve (Nelson-Siegel), and an arbitrage-free forward curve (HJM). A corporate credit spread curve can sit on top of the government curve.

Every model here is fitted to live data through the Finance Toolkit, so simulated rates start from today's level and move the way history says they move. All rates are decimals: `0.04` is 4%. For every parameter and method, see the API reference for [InterestRates](/projects/financescenarios/docs/reference/interest-rates), [TermStructure](/projects/financescenarios/docs/reference/term-structure), [CreditTermStructure](/projects/financescenarios/docs/reference/credit-term-structure) and [Hjm](/projects/financescenarios/docs/reference/hjm).

## Short-Rate Models

A short-rate model is the simplest choice when you need one rate per country, such as a 3-month bill rate or a 10-year yield, that wanders around a normal level.

You configure each rate as an entry under `interest_rates`, and pick the model with `method`. Each entry becomes its own correlated factor, so you can simulate the US short rate, the US 10-year and the euro short rate side by side:

```yaml
interest_rates:
  defaults:
    method: hull_white
  countries:
    - name: United States        # 13-week Treasury bill (^IRX), daily
    - name: United States
      ticker: "^TNX"             # 10-year Treasury yield
      term: long
    - name: Eurozone
      source: oecd
      country: Germany
```

These resolve to factors named `united_states_short_rate`, `united_states_long_rate` and `eurozone_short_rate`. See [configuration](/projects/financescenarios/docs/configuration) for how `defaults` and `countries` combine.

### Hull-White (Vasicek)

The default, `method: hull_white`, pulls the rate toward a long-run level at a fitted speed, with normally distributed swings of a fixed size: `dr = a * (theta - r) * dt + sigma * dW`. Because the swings do not depend on how high the rate is, the rate can go below zero.

In a real-world run this is the [Vasicek (1977)](https://doi.org/10.1016/0304-405x(77)90016-2){:target="_blank"} model with one fixed level. The [Hull-White (1990)](https://doi.org/10.1093/rfs/3.4.573){:target="_blank"} extension, where the level moves over time to match today's curve, is used in the risk-neutral forward-curve mode.

Fitting and simulation both use the model's exact step-to-step transition, so there is no discretization error at any step size. Read the speed as a half-life: `ln 2 / a` years. On the 13-week US Treasury bill (calibrated 2026-10-04), the rate started at 3.99% and was pulled toward 4.88% with a half-life of about eleven months, swinging by about 0.7 percentage points a year.

Pick Hull-White as your default: it works with every option on this page and is the only one of these four models with a risk-neutral version.

### Cox-Ingersoll-Ross

`method: cir` uses the [Cox, Ingersoll and Ross (1985)](https://doi.org/10.2307/1911242){:target="_blank"} process. It shares Hull-White's pull toward a long-run level, but scales the random swings by the square root of the rate, `sigma * sqrt(r)`. As the rate falls toward zero, its swings shrink.

The theoretical process cannot go negative while the Feller condition `2 * a * theta >= sigma^2` holds; the fit warns when it does not. Negative historical observations are floored at 0 before fitting, and the simulation uses a truncated step scheme, so a path can still dip slightly below zero. CIR's `volatility` is per unit of square-root rate: 0.0448 on the 13-week bill, about 0.9 percentage points a year at a 4% rate.

Pick CIR when you want rates to stay positive and swing less in a low-rate world. It does not work with GARCH or a risk-neutral measure.

### Wilkie Consols

`method: wilkie_consols` is the long-term government bond yield from [Wilkie's (1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf){:target="_blank"} actuarial model. The observed yield is split into an inflation part and a hidden real yield:

```
C(t)     = CW * inflation(t) - CW * (1 - CD) * inflation(t-1) + CN(t)
ln CN(t) = ln CMU + CA1 * (ln CN(t-1) - ln CMU) + CSD * noise(t)
```

The inflation part reads the paired inflation entry (`inflation_name`), with `CW` and `CD` fixed at Wilkie's published values. The real yield `CN` mean-reverts in logs, so it stays positive.

That positivity is also the main limit: real long-term yields went negative in most developed markets during 2020-2022, and the fit fails when the hidden real yield is not strictly positive, so the shipped `settings/wilkie.yaml` caps the history at 1995-2019. As a discrete recursion, it also needs the engine's `frequency` to equal the entry's `period`. Only the 1986 original is implemented, not the 1995 extension.

Pick it to reproduce Wilkie's framework, through the shipped `wilkie.yaml` factor set.

### Hibbert Two-Factor

`method: hibbert_two_factor` follows [Hibbert, Mowbray and Turnbull (2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"}. The short rate reverts toward a second, slower-moving rate instead of a fixed level: `d(fast) = a * (target(t) - fast(t)) * dt + sigma * dW`.

The paper extracts that slow target as a hidden state with a Kalman filter. Finance Scenarios approximates it with observable data, chosen by `target_source`:

- `long_term_rate` (default) fetches the same country's long-term rate (`target_ticker`, default `^TNX`, or `target_term` for OECD data), fits it as its own mean-reverting factor named `<name>_target`, and correlates it with everything else.
- `ewma` uses an exponentially weighted moving average of the rate's own history (`target_smoothing`, default 0.05). There is no second fetch or factor.

The fit is a first-order regression, since a moving target has no exact transition, and there is no single long-run level. It is real-world only, takes no beliefs, and does not replicate the paper's fixed correlations or closed-form bond prices. The shipped `hibbert.yaml` factor set selects it.

Pick it when the short end should follow the long end over time.

### KNW

`method: knw` and `method: knw_sv` model the interest rate and inflation together, each driving the other, with an optional shared stochastic volatility. They are fitted jointly with their inflation partner. See the [KNW documentation](/projects/financescenarios/docs/knw) for how they work and when to use them.

### Comparing the Short-Rate Models

| Model | `method` | Can go negative? | Reverts toward | Volatility | Best for |
|:------|:---------|:-----------------|:---------------|:-----------|:---------|
| Hull-White (Vasicek) | `hull_white` | Yes | A fixed long-run level (or an anchor path) | Constant, or GARCH | General use; the only one with every option |
| Cox-Ingersoll-Ross | `cir` | Not in theory if the Feller condition holds; a simulated path can dip slightly below | A fixed long-run level | Scales with the square root of the rate | Positive rates with smaller swings near zero |
| Wilkie consols | `wilkie_consols` | The real-yield part cannot | A fixed level, for the log real yield | Constant | Reproducing Wilkie (1986) |
| Hibbert two-factor | `hibbert_two_factor` | Yes | A moving target: the long rate or a moving average | Constant | Short rates that follow long rates |
| KNW | `knw`, `knw_sv` | See the [KNW page](/projects/financescenarios/docs/knw) | | | Rates and inflation that drive each other |

## Data Sources

The data source decides which countries and frequencies you can use. Every source needs no API key; set it per entry with `source`:

| `source` | Data | Countries | Frequencies |
|:---------|:-----|:----------|:------------|
| `ticker` (default) | A Yahoo Finance Treasury yield: `^IRX` (13-week), `^FVX` (5-year), `^TNX` (10-year) or `^TYX` (30-year) | US only in practice | Daily to yearly; default daily |
| `oecd` | The OECD short- or long-term rate (`term: short` or `long`) of `country` | About 38 OECD members | Monthly, quarterly or yearly; default monthly |
| `gmdb` | The same short or long rate from the Global Macro Database | Also countries outside the OECD, such as Brazil, India and China | Yearly only |

The method and every option below work the same whichever source an entry uses.

### Long History and Long-Run Anchors

A recent window barely pins down a rate's long-run level. Two options help, for real-world `hull_white` and `cir` entries with constant volatility:

- `history_source` fits the speed, volatility and long-run level on decades or centuries of yearly data (`oecd` from 1950, `millennium` for the UK from 1694, `jst` for bill rates from 1870), while today's level still comes from `source`. `history_volatility: recent` keeps the volatility from the recent window.
- `long_run_anchor: eiopa` replaces the single fitted level with a path of forward rates from EIOPA's risk-free curve (USD, EUR or GBP), ending at the ultimate forward rate. `dnb` follows the median of De Nederlandsche Bank's scenario set for euro rates.

The shipped `default` factor set uses both. See [Long history](/projects/financescenarios/docs/configuration#long-history) and [Anchoring long-run rate levels](/projects/financescenarios/docs/configuration#anchoring-long-run-rate-levels) for details.

### Your Own Views

A `beliefs` block replaces one fitted parameter and keeps the rest. Leave a field `null` to keep the fitted value:

```yaml
interest_rates:
  countries:
    - name: United States
      beliefs:
        long_run_mean: 0.035
```

Beliefs apply to `hull_white` and `cir` entries with constant volatility. They do not apply to the Wilkie, Hibbert or KNW methods, GARCH or business-cycle fits, or a risk-neutral measure, where they would undo the match to market prices.

## Keeping Rates At or Above Zero

Use the zero lower bound when your scenarios should never show negative rates, as some scenario generators require.

`zero_lower_bound: true` on an entry floors the rate at 0% the shadow-rate way of [Black (1995)](https://doi.org/10.1111/j.1540-6261.1995.tb05182.x){:target="_blank"}. The model keeps evolving underneath as a shadow rate that may go negative, and every path, discount factor and linked factor sees `max(shadow, 0)`. A rate at zero climbs back from wherever the shadow went, so it can linger at zero the way policy rates did.

```yaml
interest_rates:
  countries:
    - name: Eurozone
      source: oecd
      country: Germany
      zero_lower_bound: true
```

It is off by default, because negative rates did happen in euro, Swiss franc and yen markets. It works on real-world entries only, since a floor breaks a risk-neutral rate's exact fit to today's curve. Today's starting rate is floored too when it is negative.

## Time-Varying Volatility (GARCH)

Use GARCH when you want calm and turbulent periods to cluster, instead of every period having the same volatility.

`volatility_model: garch` keeps Hull-White's pull toward a long-run level but replaces the fixed volatility with a [GARCH(1,1)](https://doi.org/10.1016/0304-4076(86)90063-1){:target="_blank"} process (Bollerslev, 1986): `h(t+1) = omega + alpha * eps(t)^2 + beta * h(t)`. A large shock raises next period's variance, which then fades back toward its long-run value (the fit forces `alpha + beta < 1`).

```yaml
interest_rates:
  countries:
    - name: United States
      method: hull_white
      volatility_model: garch
```

It requires `method: hull_white`, since CIR's square-root scaling is a different volatility rule. It cannot be combined with business-cycle conditioning, and beliefs do not apply: the GARCH fit is used as calibrated.

## Business-Cycle Conditioning

Use business-cycle conditioning when rates should respond to the economy on top of their own mean reversion.

`condition_on_business_cycle: true` adds a drift term on the step-to-step change in the leading indicator, fitted on history. It requires `leading_indicator.enabled: true` and moves the entry's calibration onto the leading indicator's `period`.

```yaml
leading_indicator:
  enabled: true
  period: monthly

interest_rates:
  countries:
    - name: Eurozone
      source: oecd
      country: Germany
      condition_on_business_cycle: true
```

It does not work with GARCH, beliefs, the Wilkie or Hibbert methods, or the risk-neutral measure. See [Business-cycle conditioning](/projects/financescenarios/docs/configuration#business-cycle-conditioning).

## Real-World and Risk-Neutral Rates

Use the risk-neutral measure when you value cash flows against today's market prices, for example a Solvency II best estimate, instead of exploring what could happen.

`measure: risk_neutral` on a `hull_white` entry offers two versions:

- **Flat path (default).** Today's observed rate is held constant along every path. No speed or volatility is fitted, because no market price would discipline them.
- **Forward curve** (`risk_neutral_forward_curve: true`). A stochastic Hull-White rate whose expected path reproduces today's forward curve (a Nelson-Siegel fit to the four Treasury yields), following [Brigo and Mercurio (2006, section 3.3)](https://doi.org/10.1007/978-3-540-34604-3){:target="_blank"}.

```yaml
interest_rates:
  countries:
    - name: United States
      measure: risk_neutral
      risk_neutral_forward_curve: true
```

The main simplification: speed and volatility in forward-curve mode are the historical ones, since there are no cap or swaption prices to fit them to. Beliefs, GARCH, business-cycle conditioning and the zero lower bound are rejected here, and `knw_sv` is the only other method with a risk-neutral version. See [Real-world and risk-neutral measures](/projects/financescenarios/docs/configuration#real-world-and-risk-neutral-measures).

## The Nelson-Siegel Yield Curve

Use the yield curve when you need yields at every maturity that move together consistently, for example to reprice a bond portfolio or a liability profile along each scenario.

The `yield_curve` section simulates a whole government curve with the dynamic Nelson-Siegel model of [Diebold and Li (2006)](https://doi.org/10.1016/j.jeconom.2005.03.005){:target="_blank"}, built on the curve shape of [Nelson and Siegel (1987)](https://doi.org/10.1086/296409){:target="_blank"}. The yield at any maturity is the sum of three factors:

```
yield(tenor) = level + slope * slope_loading(tenor) + curvature * curvature_loading(tenor)
```

- **Level** (`rate_level`) moves every maturity equally: a parallel shift.
- **Slope** (`rate_slope`) moves short maturities more than long ones: steepening and flattening. The very short end is `level + slope`.
- **Curvature** (`rate_curvature`) moves medium maturities most: a hump or a trough.

The loadings depend only on maturity and one `decay` parameter (default 0.7308), which is fixed, as in Diebold and Li.

The three factors are fitted to the observed yields at every historical date, and each series is then modeled as its own mean-reverting process, exactly like a Hull-White short rate. They are linked to the rest of the model through the correlation matrix and accept per-factor `beliefs` (`level`, `slope`, `curvature`).

```yaml
yield_curve:
  enabled: true
  source: government
  country: Germany
  period: monthly
```

### Curve Sources

| `source` | Data | Key | Frequencies |
|:---------|:-----|:----|:------------|
| `yahoo` (default) | The four Yahoo Treasury yields: 13-week, 5, 10 and 30 years | None | Daily to yearly |
| `treasury` | The official US Treasury par curve, 12 maturities from 1 month to 30 years | Financial Modeling Prep | Daily only |
| `government` | The official government curve of `country` | None | Daily, weekly or monthly |

The `government` source is what makes a non-US curve possible. It covers the United States (Treasury), the Euro Area (European Central Bank), Germany (Bundesbank), the United Kingdom (Bank of England), Japan (Ministry of Finance), Canada (Bank of Canada), Sweden (Riksbank) and Norway (Norges Bank), and never falls back to the US curve. `treasury` adds the short-end coverage the Yahoo yields lack, and falls back to Yahoo with a warning if its fetch fails.

### Reading a Simulated Curve

Turn the three simulated factors into a yield at any maturity, and count how often the curve inverts:

```python
from financescenarios import Scenarios
from financescenarios.factors.term_structure.term_structure_model import (
    curve_inversion_frequency,
    nelson_siegel_yield,
)

result = Scenarios.from_profiles(settings="default", factor_set="default").simulate(n_simulations=1000)
level, slope, curvature = (result.paths[name] for name in ("rate_level", "rate_slope", "rate_curvature"))

ten_year = nelson_siegel_yield(level, slope, curvature, tenor=10.0, decay=0.7308)
inverted = curve_inversion_frequency(level, slope, curvature, short_tenor=0.25, long_tenor=10.0, decay=0.7308)
```

`ten_year` has one row per scenario and one column per time step. `negative_spread_frequency` works the same way for the share of negative yields.

### Limits

- The Yahoo source has only four maturities: fine for broad level, slope and curvature moves, not a precision pricing tool. Its daily slope and curvature are noisy (a slope half-life of about 1.5 months on 2021-2026 data, against about 1.5 years on the Treasury curve).
- The Bank of England publishes only the 5, 10 and 20-year maturities, so the UK curve is fitted exactly to three points and its short end is an extrapolation.
- Japanese yields have risen steadily since 2000, so the level shows no mean reversion and the fit stops with an error.
- The factors are statistical and real-world, with no guarantee against arbitrage between maturities. For that, use HJM below.
- Yields are used as quoted (semiannual, bond-equivalent), without converting to continuous compounding.

## The Credit Spread Curve

Use the credit curve when you need corporate spreads at every maturity, so that a corporate bond can be discounted at the government curve plus its own spread.

The `credit_term_structure` section reuses the yield curve's Nelson-Siegel machinery unchanged, fitted to corporate bond spreads over government yields instead of to yields. It adds three correlated factors, `credit_level`, `credit_slope` and `credit_curvature`.

```yaml
credit_term_structure:
  enabled: true
  source: hqm
  period: monthly
```

Keep `decay` equal to `yield_curve.decay` (both default to 0.7308). Nelson-Siegel curves with the same decay add up factor by factor, so the government curve plus the spread curve is again a Nelson-Siegel curve: the discount curve for risky bonds.

### Credit Sources

- `hqm` (default): the US Treasury's [High Quality Market corporate bond curve](https://home.treasury.gov/data/treasury-coupon-issues-and-corporate-bond-yield-curves){:target="_blank"} minus the Treasury par curve, at 2, 5, 10 and 30 years, monthly from 1984. US pension plans discount with it, and it is built from AAA, AA and A bonds, so it is an investment-grade spread curve. It needs a free FRED key; `period` can be monthly, quarterly or yearly.
- `bond_panel`: the [Open Source Bond Asset Pricing](https://openbondassetpricing.com/){:target="_blank"} panel of US corporate bond trades (TRACE), July 2002 to March 2025, with spreads measured against the government curve of [Liu and Wu (2021)](https://doi.org/10.1016/j.jfineco.2021.05.059){:target="_blank"}. It is a one-time 1.8 GB download that needs well over 1 GB of memory, bonds are grouped into the maturities in `tenors`, and the curve starts from the panel's last usable month instead of today.

Monthly is the default because daily single-bond spreads carry bid/ask bounce and illiquid-bond noise that reverts within days, which would fit an unrealistically fast mean reversion.

### Limits

- The bond panel has no rating field, so its curve is the average across all bonds, not one per rating. For ratings moving from BBB to BB to default, see [CreditMigration](/projects/financescenarios/docs/reference/credit-migration).
- The three factors are fitted independently, without the restrictions that would make the curve arbitrage-free. Neither the arbitrage-free Nelson-Siegel variant ([Christensen, Diebold and Rudebusch, 2011](https://doi.org/10.1016/j.jeconom.2011.02.011){:target="_blank"}) nor the four-factor [Svensson (1994)](https://doi.org/10.3386/w4871){:target="_blank"} extension is implemented.
- Default intensities ([Duffie and Singleton, 1999](https://doi.org/10.1093/rfs/12.4.687){:target="_blank"}) are not modeled directly; the curve is a statistical fit.

## HJM: An Arbitrage-Free Forward Curve

Use HJM when the simulated curve must be free of arbitrage between maturities by construction, for example in market-consistent valuation.

Every other rate model here learns its drift from history. In the framework of [Heath, Jarrow and Morton (1992)](https://doi.org/10.2307/2951677){:target="_blank"} you fix how volatile the forward curve is at each maturity, and the no-arbitrage condition dictates the drift.

Finance Scenarios uses two independent factors whose volatility fades with time to maturity `x`: `sigma_i * exp(-kappa_i * x)`. With this choice the model reduces to the two-factor Hull-White (G2++) model ([Hull and White, 1994](https://doi.org/10.3905/jod.1994.407908){:target="_blank"}; [Brigo and Mercurio, 2006](https://doi.org/10.1007/978-3-540-34604-3){:target="_blank"}, chapters 3-4), and each factor (`hjm_factor_1`, `hjm_factor_2`) is a simple mean-reverting process that starts at zero.

The forward rate at maturity `x`, `t` years from now, is rebuilt as:

```
f(t, x) = f_today(t + x) + exp(-kappa_1 * x) * x_1(t) + exp(-kappa_2 * x) * x_2(t) + convexity(t, x)
```

- `f_today` is today's forward curve, from a Nelson-Siegel fit to the four Treasury yields. Reading it at `t + x` makes the curve roll down today's curve over time, which keeps it arbitrage-free.
- The convexity term follows from the no-arbitrage condition and is not a free parameter.

At the start both factors are zero, so the model reproduces today's curve exactly at every maturity.

```yaml
hjm:
  enabled: true
  period: daily
  kappa_bounds: [0.01, 6.0]
```

### How It Is Calibrated

The model fits a Nelson-Siegel curve at every historical date, reads forward rates from 3 months to 30 years, and finds the two volatilities, two decays and one correlation whose implied co-movement best matches how those forwards changed, following the principal-component view of [Litterman and Scheinkman (1991)](https://doi.org/10.3905/jfi.1991.692347){:target="_blank"}.

A factor's effect halves every `ln 2 / kappa` years of maturity. On daily data from October 2021 to October 2026, factor 1 was a slow, level-like movement (1.32% a year, fading little across 30 years) and factor 2 a fast short-end movement (5.18% a year, halved within five months of maturity). Ten years out, convexity added 0.56 to 1.44 percentage points to the expected forward rate, rising with maturity.

Watch `covariance_fit_error` (26% in that fit; above 35% logs a warning). `variance_share` is high almost by construction and says little about whether two factors are enough.

### Assumptions and Limits

- **Risk-neutral, zero term premium by default.** With `market_price_of_risk` at zero, future rates equal today's forwards plus convexity, with no extra yield for holding long bonds. Every other rate factor is real-world, so adding HJM to a real-world run mixes two measures. You can set `market_price_of_risk` per factor as a belief; nothing fits it.
- **Long horizons.** The slow factor often fits near its decay floor, so the convexity term gets large over long projections; a 50-year projection at the floor is not credible. A decay at a bound logs a warning, and raising the floor in `kappa_bounds` (for example to 0.03-0.10) is defensible.
- **The fast factor is weakly identified.** With the shortest maturity at three months, fast decays look alike, so do not read the fitted `kappa_2` as an economic quantity.
- **Limited shapes.** Forward-rate volatility can only fall with maturity, while real volatility curves are usually humped, and two factors cannot create a random hump in the curve. With no cap or swaption prices, volatility is fitted to history at four maturities.
- **Keep the correlation consistent.** If you override `beliefs.factor_correlation`, the convexity term uses your value. It must match the correlation the shocks are drawn with, or the curve is no longer arbitrage-free.

HJM fits its own anchor curve and does not need a `yield_curve` section.
