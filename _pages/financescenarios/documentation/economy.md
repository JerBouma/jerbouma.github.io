---
title: Inflation, Labor and Longevity
seo_title: Inflation, Labor and Longevity – Finance Scenarios
excerpt: "How Finance Scenarios models inflation, unemployment, the business cycle and mortality: the methods on offer, when to use each, their limits and the papers behind them."
description: "How Finance Scenarios simulates inflation, unemployment, the business cycle and longevity: each model, when to use it, its limits and its sources."
author_profile: false
permalink: /projects/financescenarios/docs/economy
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Interest rates and equity returns get most of the attention in a scenario set, but many liabilities are driven by the economy around them. Pensions are indexed to prices, wage growth and claims move with the labor market, and annuities run for as long as people live. This page covers the four factors that describe that economy in Finance Scenarios: inflation, unemployment, the leading indicator of the business cycle, and mortality.

Each factor is fitted to its own history, then simulated alongside every other factor with correlated random shocks (see the [simulation engine](/projects/financescenarios/docs/simulation-engine)). Inflation, unemployment and the leading indicator come from official statistics through the Finance Toolkit, with no API key needed. For each factor you will find what the model does in plain words, when you would pick it, what it assumes, and the papers it comes from. The full list of arguments and fields sits in the API reference pages linked from each section.

## Inflation

Inflation sets the real value of every nominal cash flow, so it is usually the first variable a pension or insurance model needs.

In Finance Scenarios, inflation sits at the top of the model, following [Wilkie (1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf){:target="_blank"} and [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}: inflation drives other parts of the model, such as unemployment and, in Wilkie's setup, dividends, rather than the other way around.

### The Data

Each inflation entry is the year-over-year growth of a country's Consumer Price Index: this month's price level against the same month a year earlier. That is the headline rate statistics offices publish. A reading of 0.034 means prices are 3.4% higher than a year ago, on the same annual decimal scale as interest rates.

Two sources are available, neither of which needs an API key:

- `source: oecd` (the default) covers the roughly 38 OECD members at monthly, quarterly or yearly frequency.
- `source: gmdb` uses the Global Macro Database, which also covers countries such as Brazil, India and China. It is annual only, so the entry needs `period: yearly`, and its most recent year can be an IMF projection rather than an outturn.

Consecutive monthly readings share eleven of their twelve months, so the series is smooth, the convention most economic scenario generators calibrate on.

You can model several countries at once. `inflation` is a list, and each entry becomes its own factor, linked to the others through the correlation matrix. The shipped profiles use the shorter `defaults` and `countries` shape described in [configuration](/projects/financescenarios/docs/configuration), where `name: Eurozone` becomes the factor `eurozone_inflation`.

### Mean Reversion to a Target (the Default)

The default `method: ou` treats inflation as an Ornstein-Uhlenbeck process ([Uhlenbeck and Ornstein, 1930](https://doi.org/10.1103/PhysRev.36.823){:target="_blank"}): each period, inflation is pulled part of the way back toward a long-run level, plus a random shock. Three numbers describe it:

- `long_run_mean`: the level inflation settles around.
- `mean_reversion_speed`: how hard it is pulled back. `ln 2 / mean_reversion_speed` is the half-life of a shock in years.
- `volatility`: the size of the random shocks.

Every simulated path starts from the latest observed rate. Calibrated on US data from 2000 onward, inflation started at 3.40% and was pulled toward 2.66%, halving any gap in about 1.7 years. Nothing floors the rate, so deflation can occur, as it has in history.

Use it when you want a simple inflation process with a clear anchor. If you hold a view on that anchor, override it with a belief:

```yaml
inflation:
  - name: us_inflation
    country: United States
    period: monthly
    beliefs:
      long_run_mean: 0.02        # anchor at 2% a year instead of the fitted level
      mean_reversion_speed: null # null keeps the fitted value
      volatility: null
```

Beliefs are stated on the annual scale and apply only to this constant-volatility fit. In a [regime](/projects/financescenarios/docs/regimes) file you address one entry's beliefs with a dotted key such as `"inflation.us_inflation"`.

Two options change how the default process behaves:

- `volatility_model: garch` replaces the fixed volatility with a GARCH(1,1) process ([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1){:target="_blank"}), so calm and turbulent inflation spells each persist. Beliefs then no longer apply.
- `history_source` fits the speed, volatility and long-run level on centuries of data instead of the recent window: `millennium` for UK consumer price inflation from 1209, or `shiller` for US inflation from 1872. Today's starting level still comes from current data. `history_start_year` drops the early years, for example everything before 1900.

### Wilkie's AR(1)

`method: wilkie_ar1` is Wilkie's original inflation model: each period's value keeps a fixed share of last period's gap to the mean (`persistence`), plus a shock. On the same US data, 97% of each month's gap carried into the next month. The economics are close to the default; the difference is that Wilkie's version is fitted directly in discrete steps.

Choose it when you want to reproduce the Wilkie framework as a whole. In that cascade, the dividend yield, dividend growth and the long-term (consols) yield are each computed directly from the inflation path, on top of any correlation. The shipped `wilkie` factor set and settings profile set this up for you. The model has no time step to rescale, so the engine's `frequency` must equal the entry's `period`. It cannot be combined with GARCH, business-cycle conditioning or belief overrides.

### Hibbert's Two-Factor Model

`method: hibbert_two_factor` follows [Hibbert, Mowbray and Turnbull (2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"}. Actual inflation reverts to a second, slower-moving "expected inflation" level instead of to a fixed number, so the anchor itself drifts over time. This suits long horizons where you do not want to assume that inflation always returns to the same level.

The paper estimates expected inflation with a Kalman filter, which Finance Scenarios does not have. `target_source` picks an observable stand-in instead:

- `coarser_period` (the default) uses the same country's inflation at a coarser frequency (`target_period`, yearly by default) as the slow target, simulated as its own correlated factor named `<name>_target`.
- `ewma` uses an exponentially weighted moving average of the entry's own path, with `target_smoothing` (default 0.05) as the weight on each new observation. Smaller values give a slower target.

Keep the limits in mind. Hibbert's fixed cross-factor correlations and closed-form bond prices are not replicated; correlations come from the same estimated matrix as every other factor. On year-over-year data the smoothed target tracks inflation closely, so most of the movement sits in the target. The method also needs a long history: pass an early `start_date` (the shipped settings use 2000-01-01), or the yearly target has too few points to fit. GARCH, business-cycle conditioning and beliefs are not available here.

### Conditioning on Interest Rates or the Business Cycle

Two switches add a term that lets inflation respond to another variable's move over the same step:

- `condition_on_interest_rate: true` adds a term on the change in a paired short rate, named by `interest_rate_name`. Calibration then runs at that rate's period.
- `condition_on_business_cycle: true` adds a term on the change in the leading indicator (see below). It requires `leading_indicator.enabled: true`.

```yaml
interest_rates:
  - name: short_rate
    ticker: "^IRX"

inflation:
  - name: us_inflation
    country: United States
    condition_on_interest_rate: true
    interest_rate_name: short_rate
```

Both are one-way links: the rate or the indicator moves inflation, not the reverse. Use the interest-rate link when you want rate moves to feed through to prices beyond what the correlation matrix already captures. If you want rates and inflation to drive each other, with both levels fitted jointly, use the KNW model instead, set with `method: knw` or `method: knw_sv`; it is covered on the [KNW page](/projects/financescenarios/docs/knw). The two conditioning switches cannot be combined with each other, with GARCH, or with `knw`, and a conditioned entry is used as fitted, without beliefs.

### Market-Implied Inflation (Risk-Neutral)

Everything above describes real-world inflation: how prices might plausibly move. To value inflation-linked cash flows in line with market prices you need the inflation the bond market prices in instead. That is the breakeven: the gap between a nominal government bond yield and an inflation-protected one of the same maturity.

Set `measure: risk_neutral` with `method: ou` to use it:

```yaml
inflation:
  - name: uk_breakeven
    country: United Kingdom
    measure: risk_neutral
```

Finance Scenarios fits a [Nelson-Siegel (1987)](https://doi.org/10.1086/296409){:target="_blank"} curve, with a long-run level, a slope and a hump, to the latest date on which every maturity is quoted. Every simulated path then follows that curve's forward rates, with no randomness, no mean reversion and no beliefs. The curve's decay parameter is fixed rather than fitted, following [Diebold and Li (2006)](https://doi.org/10.1016/j.jeconom.2005.03.005){:target="_blank"}, and can be set with `tips_breakeven_decay` (default 0.7308).

Three curves are available, all read without an API key:

| `country` | Source | Maturities fitted | Inflation index |
|:--|:--|:--|:--|
| `United States` (default) | US Treasury, nominal minus TIPS yields | 5, 7, 10, 20 and 30 years | US CPI |
| `United Kingdom` | Bank of England implied inflation spot curve | 3 to 40 years | Retail Prices Index (RPI) |
| `Germany` or `Euro Area` | Bundesbank, German nominal minus inflation-linked yields | 5, 7, 10 and 15 years | Euro area HICP excluding tobacco |

A few points to watch:

- No US or German breakeven is quoted below five years, and no UK one below three, so the first years of the path are extrapolated from the fitted curve rather than quoted by the market. A warning is logged when today's value lands more than a percentage point away from the shortest quoted breakeven.
- The UK curve measures RPI, which has run above CPI inflation.
- A breakeven can be negative, and nothing floors it.
- The entry must keep the default `source` and `period`, constant volatility, no conditioning and no beliefs, since none of them apply to a market snapshot. The configuration rejects them when it loads.

The breakeven route is also not what `simulate(measure="risk_neutral")` does to inflation: that call keeps inflation as configured, real-world, so benefits can still be indexed to it. For a risk-neutral inflation leg with its own dynamics, the KNW model with stochastic volatility (`method: knw_sv` with `measure: risk_neutral`) offers that; see the [KNW page](/projects/financescenarios/docs/knw).

### What Inflation Does Not Cover

Finance Scenarios models headline CPI inflation only, with no core or sector price indices. The default data window of the Finance Toolkit is about five years, which is short for a stable fit, so set an early `start_date` in your settings profile.

The full reference is on the [Inflation](/projects/financescenarios/docs/reference/inflation) page.

## Unemployment

Unemployment matters for anything tied to the labor market, such as wage-linked benefits, disability claims or credit losses, and it gives you a second view of the economy alongside inflation.

The model is the unemployment equation of [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}: unemployment reverts to a long-run level, like the default inflation model, with one added term for the change in inflation over the same step. That term is a Phillips curve, named after [Phillips (1958)](https://doi.org/10.1111/j.1468-0335.1958.tb00003.x){:target="_blank"}: rising inflation tends to go with falling unemployment.

In one line, each step is:

`change in unemployment = pull toward the long-run level + inflation_sensitivity * change in inflation + random shock`

### How It Links to Inflation

Each unemployment entry is paired with one inflation entry through `inflation_name`. During the simulation, the unemployment step reads that inflation factor's simulated move for the same step, so the two stay consistent path by path. The calibration fits both effects together in one regression of each period's change in unemployment on the previous level and the same period's change in inflation, with the two series matched by date.

Calibrated on US data from 2000 onward, unemployment started at 4.27% and was pulled toward 5.67% with a half-life of about 1.3 years. The fitted `inflation_sensitivity` was -0.34: a one-point rise in inflation over a step went with roughly a third of a point fall in unemployment, as the Phillips curve expects.

An unemployment entry has no `period` of its own. It always uses its paired inflation entry's period, so the two series share one frequency. With `source: gmdb` (for countries outside the OECD), that paired inflation entry must be yearly.

```yaml
unemployment:
  - name: us_unemployment
    country: United States
    inflation_name: us_inflation  # must match an inflation entry's name
    beliefs:
      long_run_mean: 0.045        # your own view of the normal rate
```

Every factor set needs at least one unemployment entry. In the `defaults` and `countries` shape, `inflation_name` defaults to the same country's inflation factor.

### Limits and When to Override

The fitted sign of the Phillips curve is not forced. Brazil, fitted on yearly Global Macro Database data, came out slightly positive. If that conflicts with your view, set `beliefs.inflation_sensitivity`, which may take any sign.

A history with a long one-way trend gives a poor anchor. German unemployment fell steadily for fifteen years after 2000, and a quarterly fit gave a mean reversion speed near zero and a negative long-run mean. In such a case, set `beliefs.long_run_mean` and `beliefs.mean_reversion_speed` yourself, or use another country as a proxy: the shipped `core` factor set uses France for the euro area for this reason.

The full reference is on the [Unemployment](/projects/financescenarios/docs/reference/unemployment) page.

## The Leading Indicator and the Business Cycle

The leading indicator gives the model an explicit business cycle, so that other factors can move with booms and slowdowns instead of only being correlated with each other.

The factor is the OECD Composite Leading Indicator, an index designed to turn ahead of the economy. The OECD publishes it already detrended and scaled to swing around a long-run average of 100, so mean reversion holds largely by construction. Finance Scenarios models it with the same mean-reverting process as default inflation, with an optional GARCH volatility. The data are monthly, without an API key, and cover about 22 countries and country groups, fewer than most OECD series. A quarterly or yearly `period` averages the monthly readings.

```yaml
leading_indicator:
  enabled: true
  country: United States
  period: monthly
```

On its own, the indicator is one more correlated factor.

### Business-Cycle Conditioning

The indicator becomes more useful when other factors condition on it. Setting `condition_on_business_cycle: true` on an interest rate, inflation, real estate, credit, commodity or dividend yield entry adds a term on the indicator's step-to-step change:

`change in factor = pull toward its long-run level + sensitivity * change in leading indicator + random shock`

The sensitivity is fitted from history. Use it when you want, for example, credit spreads to widen and rates to fall as the cycle turns down, in a way that follows the simulated cycle rather than only the average correlation.

The rules:

- It requires `leading_indicator.enabled: true`.
- The conditioned entry is calibrated at `leading_indicator.period`, so the two series line up by date. That period must be one the factor supports: real estate only works at quarterly or yearly, so the default monthly indicator cannot condition it.
- It cannot be combined with GARCH volatility on the same factor, and a conditioned entry is used as fitted, without beliefs.

Two factors work differently:

- **Unemployment** adds the indicator as a second term next to its inflation term, so the fit estimates both sensitivities at once. Here `leading_indicator.period` must equal the paired inflation entry's period.
- **Equities** have no drift term to extend, so the indicator's level instead changes the chance of switching between calm and crisis regimes, the time-varying transition probabilities of [Filardo (1994)](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}. See [markets](/projects/financescenarios/docs/markets).

The full reference is on the [LeadingIndicator](/projects/financescenarios/docs/reference/leading-indicator) page.

## Mortality and Longevity

Longevity risk is the risk that people live longer than a pension fund or annuity provider expected. Mortality has fallen for decades, but not at a fixed pace, and that uncertain trend is what this factor captures.

### The Cairns-Blake-Dowd Model

Finance Scenarios uses the two-factor model of [Cairns, Blake and Dowd (2006)](https://doi.org/10.1111/j.1539-6975.2006.00195.x){:target="_blank"}, often called CBD. Each calendar year, the one-year probability of death at each age is described by two numbers:

- **Level** (`kappa1`): moves mortality up or down at every age alike.
- **Age slope** (`kappa2`): how steeply mortality rises with age. A higher slope means older ages move more than younger ones.

In formula terms, `logit(q) = kappa1 + kappa2 * (age - mean_age)`, where `q` is the one-year probability of death and `mean_age` is the middle of the fitted age range. The two factors are simulated as `mortality_level` and `mortality_slope`, linked to rates, equities and the rest through the correlation matrix.

Unlike the other factors on this page, the two do not revert to a normal level. Each is a random walk with drift, as in the CBD paper: mortality improvement is a sustained trend over decades, and the drift carries that trend forward with realistic surprises around it.

As an example, a fit on 40 years (1985 to 2024) of Dutch death probabilities at ages 60 to 84 gave a level drift of -0.0153. That means death rates fall by roughly 1.5% a year at every age. A 72-year-old in 2024 had a 1.9% chance of dying within the year, each extra year of age raised that by about 12%, and a 65-year-old's 0.89% drifts to about 0.75% in ten years.

### Getting the Data

Mortality is opt-in and stays off in the shipped factor sets. There are two ways to feed it:

**Eurostat.** With `source: eurostat`, the life table of a European Economic Area country is fetched through the Finance Toolkit, yearly from 1960 for most countries, with no API key:

```yaml
mortality:
  enabled: true
  source: eurostat
  country: Netherlands
  sex: total      # total, male or female
  min_age: 60
  max_age: 84
```

The default age range of 60 to 84 is deliberate. The model's straight-line shape is built for older ages, and many countries published single ages only up to an "85 and over" group until the 2010s (Germany until 2013), so a higher `max_age` keeps only recent years. The maximum is 94.

**Your own table.** With `source: supplied`, the default, you pass a historical table yourself, for any country: from the [Human Mortality Database](https://www.mortality.org/){:target="_blank"}, a Society of Actuaries table or a national statistics office.

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles("default", "my_factor_set")  # mortality.enabled: true
result = scenarios.simulate(
    mortality_rates=mortality_rates,  # Polars DataFrame: one row per year, one column per age
    mortality_ages=[60.0, 65.0, 70.0, 75.0, 80.0, 85.0],
    mortality_years=list(range(1985, 2025)),  # optional: the year of each row
)
```

Pass one-year death probabilities (`qx` in the Human Mortality Database), not central death rates (`Mx`). Both look plausible, but `Mx` biases the fit by about 2% at age 90, which matters for a pension liability. If you leave out `mortality_years`, the last row is assumed to be the most recent completed year.

### Reading a Death Rate Back

To turn simulated paths into a death rate at a given age, use `cbd_mortality_rate` with the fitted mean age:

```python
from financescenarios.factors.mortality.mortality_model import cbd_mortality_rate

q_70 = cbd_mortality_rate(
    result["mortality_level"],
    result["mortality_slope"],
    age=70,
    mean_age=scenarios.mortality.params.mean_age,
)
```

It returns one death probability per scenario and step.

### Beliefs and Limits

You can override each factor's drift and volatility, in logit units per year:

```yaml
mortality:
  beliefs:
    kappa1:
      drift: -0.02     # death rates fall about 2% a year at every age
      volatility: null # null keeps the fitted value
```

The limits:

- Cohort effects, where one generation's mortality improves differently from its neighbors, are not modeled, and there is no Lee-Carter alternative.
- The straight-line shape holds locally. Reading a death rate far outside the fitted ages, such as age 30 from a 60 to 89 fit, is not supported by the calibration.
- With only two ages the fit is perfect by construction and tells you nothing about fit quality. The CBD paper itself fits ages 60 to 89.
- Mortality data are yearly, so with a short table its correlation with the other factors rests on few points.

The full reference is on the [Mortality](/projects/financescenarios/docs/reference/mortality) page.

## References

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. [Link](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." Journal of Econometrics, 31(3), 307-327. [Link](https://doi.org/10.1016/0304-4076(86)90063-1){:target="_blank"}
- Cairns, A.J.G., Blake, D., Dowd, K. (2006). "A Two-Factor Model for Stochastic Mortality with Parameter Uncertainty: Theory and Calibration." Journal of Risk and Insurance, 73(4), 687-718. [Link](https://doi.org/10.1111/j.1539-6975.2006.00195.x){:target="_blank"}
- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. [Link](https://doi.org/10.1016/j.jeconom.2005.03.005){:target="_blank"}
- Filardo, A.J. (1994). "Business-Cycle Phases and Their Transitional Dynamics." Journal of Business & Economic Statistics, 12(3), 299-308. [Link](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}
- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert Limited. [Link](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"}
- Nelson, C.R., Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." Journal of Business, 60(4), 473-489. [Link](https://doi.org/10.1086/296409){:target="_blank"}
- Phillips, A.W. (1958). "The Relation Between Unemployment and the Rate of Change of Money Wage Rates in the United Kingdom, 1861-1957." Economica, 25(100), 283-299. [Link](https://doi.org/10.1111/j.1468-0335.1958.tb00003.x){:target="_blank"}
- Uhlenbeck, G.E., Ornstein, L.S. (1930). "On the Theory of the Brownian Motion." Physical Review, 36(5), 823-841. [Link](https://doi.org/10.1103/PhysRev.36.823){:target="_blank"}
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. [Link](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf){:target="_blank"}
