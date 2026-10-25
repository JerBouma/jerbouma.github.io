---
title: Configuration
seo_title: "Configuration | Finance Scenarios"
seo_title_suffix: false
excerpt: "Every choice behind a Finance Scenarios run: the settings profile and the factor set, the horizon and the step, the number of scenarios, the history the models learn from, the probability measure and the API keys."
description: "How a Finance Scenarios run is configured: settings profiles and factor sets, horizon and step, Monte Carlo error and the number of scenarios, the calibration window, real-world and risk-neutral measures, and API keys."
author_profile: false
permalink: /projects/financescenarios/docs/configuration
classes: wide-sidebar
layout: single
redirect_from:
    - /projects/financescenarios/docs/reference/configuration
    - /projects/financescenarios/docs/reference/configuration-classes
    - /projects/financescenarios/docs/run-files
    - /projects/financescenarios/docs/reference/runs-and-releases
    - /projects/financescenarios/docs/reference/reporting
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-configuration"
---

A scenario set is only as good as the choices behind it: what is simulated, how far ahead and in what steps, how many scenarios, which history the models learn from and under which probability measure. A run takes those choices from two ready-made profiles, a settings profile and a factor set, and every one of them can be changed in a few lines of Python or a YAML file of your own. This page goes through each choice, then shows how to write a configuration of your own and pass the API keys. Where your own judgement should replace a fitted number, a [belief](/projects/financescenarios/docs/configuration/beliefs) does that.

## Settings Profiles and Factor Sets {#settings-profiles-and-factor-sets}

A run combines two profiles:

<div class="ca-cards">
  <div><i class="ca-icon fas fa-sliders-h" aria-hidden="true"></i><p class="ca-card-title">Settings profile: how the run executes</p><p>Start date, horizon, step, number of scenarios and calibration window.</p></div>
  <div><i class="ca-icon fas fa-cubes" aria-hidden="true"></i><p class="ca-card-title">Factor set: what is simulated</p><p>Rates, inflation, markets, which countries, and any views that override the fit.</p></div>
</div>

Keeping them apart lets you rerun the same economy at another horizon, or another economy with the same mechanics. The shipped settings profiles:

| Settings profile | What it is for |
|:-----------------|:---------------|
| `default` | 2,000 scenarios, one step a month, five years ahead, fitted on history since 2000 |
| `long_horizon` | Default with 500 scenarios instead of 2,000, so multi-decade runs stay fast; the length is chosen per run with `simulate(years=30)` |
| `goes` | Default, but fitted on history since 2019 only; pairs with the `goes` factor set to match the NAIC's scenario generator |
| `dnb` | Monthly steps over 100 years, DNB's horizon, with 2,000 scenarios; pairs with the `dnb` factor set |
| `ahlgrim` | The run of Ahlgrim, D'Arcy and Gorvett (2005): from June 2004, 5,000 scenarios, 50 years, one step a month |
| `hibbert` | The run of Hibbert, Mowbray and Turnbull (2001): from March 2001, 1,000 scenarios, 30 years, one step a month |
| `wilkie` | The run of Wilkie (1986): 1,000 scenarios of 100 years in yearly steps, dated 1986 |

And the shipped factor sets:

| Factor set | What it simulates |
|:-----------|:------------------|
| `default` | The US, the euro area and the UK, with global equities, gold, oil and the major currencies, each factor fitted to its long history and linked the way the economy is: a policy-rule short rate on the market's expected path, inflation and unemployment regimes, equities on a long-run premium; the recommended starting point |
| `broad` | Default plus Japan, Canada, Australia and India, US sectors and styles, more countries' equities, silver, copper, natural gas, five more currencies and SPY's dividend yield; the widest and slowest to fit |
| `goes` | The United States as the NAIC's scenario generator (GOES) describes it: four Treasury yields on CIR set to its published bands, stocks on post-war history earning its long-run cash rate plus a premium, inflation, unemployment, commodities, currencies and SPY's dividend yield; see [the GOES acceptance criteria](/projects/financescenarios/docs/validation/benchmarks#goes-acceptance-criteria) |
| `dnb` | De Nederlandsche Bank's real-world scenarios rebuilt with its CP2022 model and its quarterly parameters: euro nominal and real rates, euro and Dutch inflation and world equity; see [CP2022](/projects/financescenarios/docs/interest-rates/cp2022) |
| `ahlgrim`, `hibbert`, `wilkie` | A published model reproduced from its paper's start with the paper's own parameters and no data; see [Published Models](/projects/financescenarios/docs/validation/published-models) |

Each factor set with a settings profile of the same name is meant to run with it. A run picks one of each:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(settings="default", factor_set="default")
result = scenarios.simulate()
```

### What a Configuration Holds

`load_profiles` returns the configuration a settings profile and a factor set make together, without calibrating anything, and `describe` lists what it simulates, per category. To load the default configuration and the one with the broad factor set, and describe both:

```python
from financescenarios import load_profiles

config = load_profiles(settings_id="default", factor_set_id="default")
config.describe()

broad = load_profiles(settings_id="default", factor_set_id="broad")
broad.describe()
```

Which gives, for the default configuration, one row per category:

| category | n_factors | factors |
|:---------|----------:|:--------|
| commodities | 2 | gold, crude_oil |
| equities | 5 | us_broad, small_cap, europe, japan, emerging_markets |
| fx | 3 | eur, gbp, jpy |
| inflation | 3 | united_states_inflation, eurozone_inflation, united_kingdom_… |
| interest_rates | 6 | united_states_short_rate, united_states_long_rate, eurozone_… |
| leading_indicator | 1 | leading_indicator |
| real_estate | 1 | real_estate |
| unemployment | 3 | united_states_unemployment, eurozone_unemployment, united_ki… |
| yield_curve | 3 | rate_level, rate_slope, rate_curvature |

The broad factor set holds 68 variables against the default's 27: rates and inflation for Japan, Canada, Australia and India as well, 23 stock markets including the US sectors and styles, eight currencies, five commodities and SPY's dividend yield. Credit is opt-in in both: spreads by rating come from the ICE BofA indices and need the FRED key. When plotted, the number of variables per category:

{% include ft-chart.html id="configuration-factor-sets" src="/assets/data/financescenarios-guides/configuration.json" label="Number of simulated variables per category in the default and the broad factor set" %}

## Horizon and Step {#horizon-and-step}

The horizon follows the question: one year for a Solvency II view, since the solvency capital requirement is the 99.5% Value-at-Risk of basic own funds over one year ([Solvency II Directive, Article 101(3)](https://eur-lex.europa.eu/eli/dir/2009/138/oj){:target="_blank"}); 15 to 60 years for an ALM study or a pension fund's continuity analysis. The step should match what the liabilities and the investment policy react to: monthly for rebalancing and hedging decisions, yearly for long projections where intra-year noise adds nothing.

Over long horizons the long-run parameters (where rates and inflation revert to, and how fast) dominate, and today's starting point fades.

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">Small biases compound</p>

A 0.5 percentage point difference in the long-run equity return is about 15% of terminal wealth after 30 years.
</div>

### Thirty Years from One Calibration

`simulate` takes the number of scenarios and the horizon in years for one call, without changing the profile. A saved calibration can be reused at any horizon, so a 30-year run needs no new download or fit. To simulate 1,000 scenarios over 30 years from the [overview's](/projects/financescenarios/docs#keeping-a-run) saved calibration and read them off after 5, 10 and 30 years:

```python
from financescenarios import CalibrationResult, Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
calibration = CalibrationResult.load("calibration.json")

long_run = scenarios.simulate(calibration=calibration, years=30, n_simulations=1000, seed=42)
long_run.horizon_summary(
    [5, 10, 30], factors=["united_states_short_rate", "united_states_long_rate", "united_states_inflation"]
)
```

Which gives, among other columns:

| factor | horizon | mean | q0.05 | q0.5 | q0.95 |
|:-------|--------:|-----:|------:|-----:|------:|
| united_states_short_rate | 5 | 0.0458 | 0.0000 | 0.0434 | 0.1108 |
| united_states_short_rate | 10 | 0.0462 | 0.0000 | 0.0431 | 0.1183 |
| united_states_short_rate | 30 | 0.0403 | 0.0000 | 0.0340 | 0.1081 |
| united_states_long_rate | 5 | 0.0592 | 0.0182 | 0.0563 | 0.1123 |
| united_states_long_rate | 10 | 0.0586 | 0.0111 | 0.0547 | 0.1214 |
| united_states_long_rate | 30 | 0.0538 | 0.0097 | 0.0500 | 0.1145 |
| united_states_inflation | 5 | 0.0229 | -0.0086 | 0.0185 | 0.0733 |
| united_states_inflation | 10 | 0.0232 | -0.0073 | 0.0173 | 0.0786 |
| united_states_inflation | 30 | 0.0248 | -0.0056 | 0.0180 | 0.0812 |

After ten years the ranges barely widen: each variable has reached the distribution its model settles in, with the median short rate at 3.40% and the 10-year rate at 5.00% after thirty years. When plotted:

{% include ft-chart.html id="configuration-thirty-years" src="/assets/data/financescenarios-guides/configuration.json" label="Median and 5-95% band of the US short rate, the US 10-year rate and US inflation over thirty years, 1,000 scenarios" %}

## Number of Scenarios {#number-of-scenarios}

A run of $$n$$ scenarios estimates a distribution with sampling error. For a mean, the standard error is

$$
\text{se} = \frac{s}{\sqrt{n}}
$$

with $$s$$ the standard deviation across scenarios, so halving the error takes four times as many scenarios; with antithetic variates (every random shock paired with its mirror image) it comes from the $$n/2$$ pair averages instead. A tail percentile converges far more slowly than the mean: with 2,000 scenarios a 1-in-200 outcome rests on about ten of them. If the figure you report moves more than you could act on when you rerun with another seed, add scenarios or use antithetic variates; the [simulation engine](/projects/financescenarios/docs/simulation-engine#monte-carlo-error) covers both.

A seed makes a run repeatable, and another seed shows how much of a result is Monte Carlo noise; the `se` column of `summary_statistics` is the standard error above. To simulate the five-year return of US stocks with five seeds at 500 and at 2,000 scenarios:

```python
for n_simulations in (500, 2000):
    for seed in range(1, 6):
        run = scenarios.simulate(calibration=calibration, n_simulations=n_simulations, seed=seed)
        print(n_simulations, seed, run.summary_statistics("us_broad").tail(1).select("mean", "se"))
```

With 500 scenarios the mean ranges from 7.95% to 9.35% a year across the five seeds, with a standard error of about 0.34 points; with 2,000 it ranges from 8.24% to 8.87%, with a standard error of about 0.18 points. When plotted:

{% include ft-chart.html id="configuration-seeds" src="/assets/data/financescenarios-guides/configuration.json" label="Mean five-year annualized return of US stocks for seeds 1 to 5 at 500 and at 2,000 scenarios" %}

## Calibration Window {#calibration-window}

Today's data tells the model where things are; the history tells it how they move. The window decides which economic regimes the fitted parameters have seen. A window from 2000 has seen a decade of near-zero rates and low inflation. Rates drift so slowly relative to its length that the speed of mean reversion is barely pinned down, and the long-run level, estimated together with it, swings with small changes in the data. Where US rates settle in each window:

| Window | US short rate | US 10-year | The curve |
|:-------|:--------------|:-----------|:----------|
| Since 2000 | 5.3% | 3.2% | Inverted forever |
| OECD rates since 1950 | 4.5% | 6.0% | Every curve slopes upward again |

The 2000 window's result is an estimate the data barely pins down, not a forecast.

Short windows also understate tail events that did not happen in them. For runs of decades, the speed of mean reversion and the volatility should come from a history that includes the inflation of the 1970s and a few full rate cycles.

### Long History {#long-history}

A factor can be fitted on a long history while the run still starts from today's values; the default factor set fits its long rates' term premium and expected-path speed on the OECD's data since 1950. Older sources go back further:

| Source | Series | From |
|:-------|:-------|:-----|
| [Shiller](https://shillerdata.com/){:target="_blank"} | US equity returns and inflation | The 1870s |
| [Jordà-Schularick-Taylor](https://doi.org/10.1093/qje/qjz012){:target="_blank"} | A panel of returns and bill rates by country (non-commercial licence) | 1870 |
| [Bank of England](https://www.bankofengland.co.uk/statistics/research-datasets){:target="_blank"} | UK series | 1694 for rates, 1209 for prices |

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">Older is not always better</p>

Medieval harvests and the 1923 hyperinflation are rarely what you want. A start year cuts the history short, and the volatility can come from the recent window while the long history sets the mean reversion.
</div>

To fit every rate of a factor set on the OECD's history since 1950, with the swings of the recent window:

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
interest_rates:
  defaults:                  # every country's rates
    history_source: oecd
    history_start_year: 1950
    history_volatility: recent   # swings from the recent window, reversion from the long one
```

## Real-World and Risk-Neutral {#real-world-and-risk-neutral-measures}

Each measure answers its own question:

<div class="ca-cards">
  <div><i class="ca-icon fas fa-globe" aria-hidden="true"></i><p class="ca-card-title">Real-world: what could happen?</p><p>Follows how markets have behaved, risk premia included. For ALM, solvency projections and strategic asset allocation.</p></div>
  <div><i class="ca-icon fas fa-scale-balanced" aria-hidden="true"></i><p class="ca-card-title">Risk-neutral: what is this worth today?</p><p>Grows every asset at the risk-free rate on average, less any income it pays out, so it reproduces today's market prices. For guarantees, options and other embedded features.</p></div>
</div>

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">A classic error</p>

Mixing them up: a risk-neutral run has no equity risk premium, so it says nothing about expected returns, and a real-world run does not price an option correctly. [Merton (1973)](https://doi.org/10.2307/3003143){:target="_blank"} gives the classic no-arbitrage argument and [the SOA (2022)](https://www.soa.org/resources/research-reports/2022/understanding-the-connection/){:target="_blank"} a practical treatment of when each measure fits.
</div>

Every factor is real-world by default; a single factor or a whole run can switch to risk-neutral. A whole risk-neutral run keeps the first short rate, inflation, equities with their dividend yields, and unemployment, and leaves the rest out; unemployment stays real-world, without its links to equities and the yield curve. The other versions in the table apply when an entry is switched on its own. The risk-neutral version of each factor:

| Factor | Risk-neutral version |
|:-------|:---------------------|
| Equities | Grows at the risk-free rate minus the dividend yield; volatility from option prices, an SVI surface, its history or a Heston model fitted to the volatility smile |
| Interest rates | A Hull-White rate that reproduces EIOPA's risk-free curve for the dollar, euro and pound (the Treasury curve otherwise), with its volatility fitted to how much yields across maturities have moved; the default when the whole run is risk-neutral. Switched on for one rate alone: a flat path at today's rate, or the Treasury curve with `risk_neutral_forward_curve` (`risk_neutral_curve: eiopa` for EIOPA's) |
| FX | The interest-rate gap between the two currencies |
| Inflation | Random around the breakeven inflation curve (US, UK, Germany or the euro area) with its historical volatility, so the expected price index matches the curve; part of a whole risk-neutral run. `risk_neutral_volatility: none` follows the curve exactly |
| KNW with stochastic volatility | A market price of risk fitted to the yield curve |
| Commodities (two-factor) | Fitted to the futures curve |
| Unemployment, real estate, leading indicator, mortality, credit | Not available: there is no traded price to match |

To switch a whole run (or a single entry, with `measure: risk_neutral` in a factor set):

```python
result = scenarios.simulate(measure="risk_neutral")   # or measure: risk_neutral on one factor
```

<div class="fs-callout" markdown="1">
A flat rate at today's level is deterministic discounting: it has no rate volatility and ignores the shape of the curve, so it does not value options or guarantees on rates. Use the forward-curve version for those.
</div>

[Market Consistency](/projects/financescenarios/docs/solvency) and [Best Estimate and SCR](/projects/financescenarios/docs/solvency/capital) put the two to work together: a risk-neutral run for the value of a liability, a real-world run for the capital it needs.

<span id="configuration-classes"></span>

## Your Own Configuration {#your-own-configuration}

To keep a configuration as files, `scaffold_project("my-project")` copies the shipped settings profiles, factor sets, regimes and portfolios into a folder with a `.env` for the keys; `Scenarios.from_profiles` and `load_profiles` read them back from their folders. A profile of your own can then start from a shipped one and state only what differs:

<ol class="ca-steps">
  <li markdown="span">Copy the shipped profiles into your own folder: a profile extends a file in its own folder.</li>
  <li markdown="span">Write your profile next to them, naming the file it extends and only the settings that change.</li>
  <li markdown="span">Load it by name from that folder.</li>
</ol>

A settings profile for an ALM study:

```yaml
# my-project/settings/my_alm.yaml (a settings profile)
name: ALM study
extends: default.yaml   # the copy scaffold_project("my-project") wrote next to this file

start_date: 2026-01-01

engine:
  n_simulations: 5000
  n_steps: 360          # 30 years of months: the default set's equity regimes are fitted month by month
  frequency: monthly
  antithetic: true      # paired +/- shocks, less Monte Carlo noise
  seed: 42              # same inputs, same scenarios

toolkit:
  start_date: 1990-01-01   # the calibration window
```

To load it from its folder:

```python
scenarios = Scenarios.from_profiles(
    settings="my_alm", settings_dir="my-project/settings", factor_set="default"
)
```

A profile can also be left out altogether: a `ScenariosConfig` written in code holds one entry per variable. To simulate the US short rate, US inflation and SPY over ten years, fitted on history since 1990:

```python
from datetime import date

from financescenarios import ScenariosConfig
from financescenarios.config.config_model import (
    EngineConfig,
    EquityConfig,
    InflationConfig,
    InterestRateConfig,
    ToolkitConfig,
)

small_config = ScenariosConfig(
    start_date=date(2026, 1, 1),
    toolkit=ToolkitConfig(start_date=date(1990, 1, 1)),
    interest_rates=[InterestRateConfig(name="us_short_rate", country="United States", currency="USD")],
    inflation=[InflationConfig(name="inflation", country="United States", currency="USD")],
    equities=[EquityConfig(name="us_broad", ticker="SPY", currency="USD")],
    engine=EngineConfig(n_simulations=500, n_steps=120, frequency="monthly", seed=42),
)

small_result = Scenarios.from_config(small_config).simulate()
small_result.describe()
```

A configuration of your own calibrates on the day it runs, here 25 October 2026, so its numbers come from a different calibration than the other examples on this page. Every run also holds an unemployment entry, so `describe` returns four variables:

| factor | category | metric | initial | terminal_mean | terminal_q05 | terminal_q95 |
|:-------|:---------|:-------|--------:|--------------:|-------------:|-------------:|
| inflation | inflation | rate | 0.0374 | 0.0260 | 0.0001 | 0.0486 |
| us_short_rate | interest_rates | rate | 0.0403 | 0.0404 | 0.0043 | 0.0795 |
| unemployment | unemployment | rate | 0.0420 | 0.0541 | 0.0264 | 0.0807 |
| us_broad | equities | annualized |  | 0.1129 | 0.0146 | 0.1935 |

Over ten years SPY returns 11.29% a year on average with these three variables alone, against 8.44% over five years in the default factor set: runs compare only when they share their setup.

## API Keys {#secrets}

Profiles never hold API keys. Most factors need none:

| Factors | Data | Key |
|:--------|:-----|:----|
| Inflation, unemployment, real estate, OECD rates | OECD | None |
| FX | The Bank for International Settlements | None |
| Mortality | Eurostat | None |
| Equities, commodities, the yield curve, US market rates (^IRX, ^TNX) | Financial Modeling Prep when a key is given, Yahoo Finance otherwise | Optional |
| Credit spreads, commercial real estate | FRED | A FRED key |

Pass the keys when creating the scenarios, or set `FINANCIAL_MODELING_PREP_API_KEY` and `FRED_API_KEY` in the environment or a `.env` file. To pass them directly:

```python
scenarios = Scenarios.from_profiles(
    settings="default",
    factor_set="default",
    api_key="FINANCIAL_MODELING_PREP_KEY",
    fred_api_key="FRED_KEY",
)
```

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">6</span></summary>

- Bank of England. Research datasets: a millennium of macroeconomic data. [bankofengland.co.uk](https://www.bankofengland.co.uk/statistics/research-datasets){:target="_blank"}
- European Parliament and Council (2009). "Directive 2009/138/EC (Solvency II)", Articles 76-77 (technical provisions, best estimate) and 101 (SCR at 99.5% over one year). [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/dir/2009/138/oj){:target="_blank"}
- Jordà, Ò., Knoll, K., Kuvshinov, D., Schularick, M., Taylor, A.M. (2019). "The Rate of Return on Everything, 1870-2015." Quarterly Journal of Economics, 134(3), 1225-1298. [doi.org](https://doi.org/10.1093/qje/qjz012){:target="_blank"}
- Merton, R.C. (1973). "Theory of Rational Option Pricing." Bell Journal of Economics and Management Science, 4(1), 141-183. [doi.org](https://doi.org/10.2307/3003143){:target="_blank"}
- Shiller, R.J. (2015). "Irrational Exuberance", 3rd edition, Princeton University Press, and its data as updated by the author: monthly US stock prices, dividends, earnings and consumer prices since 1871. [shillerdata.com](https://shillerdata.com/){:target="_blank"}
- Society of Actuaries (2022). Understanding the Connection: Real-World and Risk-Neutral Scenario Generation. [soa.org](https://www.soa.org/resources/research-reports/2022/understanding-the-connection/){:target="_blank"}

</details>

{% include ft-charts-script.html %}
