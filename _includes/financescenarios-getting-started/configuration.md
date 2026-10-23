## Getting Started

The Configuration module holds every choice behind a run: how far ahead and in what steps, how many scenarios, which history the models learn from, what gets simulated, and where your own judgement replaces the fit. The ready-made profiles cover the common cases; every choice can also be changed in a few lines of Python or in a YAML file of your own.

This section uses the run from the [overview](/projects/financescenarios/docs): the default settings and factor set, calibrated on 19 October 2026, with 2,000 scenarios and seed 42.

### Loading a Configuration

A run combines a settings profile with a factor set, and `load_profiles` returns the configuration they make together without calibrating anything. `describe` then lists what it simulates, per category. To load the default configuration and the broad factor set and describe both:

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

The default settings simulate 2,000 scenarios in monthly steps over five years and fit on history since 2000, with longer records where a factor needs them. The broad factor set holds 68 variables against the default's 27: rates and inflation for Japan, Canada, Australia and India as well, 23 stock markets including the US sectors and styles, eight currencies, five commodities and SPY's dividend yield. When plotted, the number of variables per category:

{% include ft-chart.html id="configuration-factor-sets" src="/assets/data/financescenarios-guides/configuration.json" label="Number of simulated variables per category in the default and the broad factor set" %}

### Horizon, Steps and the Number of Scenarios

`simulate` takes the number of scenarios and the horizon in years for one call, without changing the profile. A saved calibration can be reused at any horizon, so a 30-year run needs no new download or fit. To simulate 1,000 scenarios over 30 years from the calibration of the overview and read them off after 5, 10 and 30 years:

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
| united_states_short_rate | 5 | 0.0462 | 0.0000 | 0.0438 | 0.1114 |
| united_states_short_rate | 10 | 0.0465 | 0.0000 | 0.0437 | 0.1188 |
| united_states_short_rate | 30 | 0.0418 | 0.0000 | 0.0360 | 0.1100 |
| united_states_long_rate | 5 | 0.0586 | 0.0189 | 0.0559 | 0.1098 |
| united_states_long_rate | 10 | 0.0592 | 0.0136 | 0.0558 | 0.1211 |
| united_states_long_rate | 30 | 0.0553 | 0.0128 | 0.0515 | 0.1150 |
| united_states_inflation | 5 | 0.0229 | -0.0086 | 0.0185 | 0.0733 |
| united_states_inflation | 10 | 0.0232 | -0.0073 | 0.0173 | 0.0786 |
| united_states_inflation | 30 | 0.0248 | -0.0056 | 0.0180 | 0.0812 |

After ten years the ranges barely widen: each variable has reached the distribution its model settles in, with the median short rate at 3.60% and the 10-year rate at 5.15% after thirty years. When plotted:

{% include ft-chart.html id="configuration-thirty-years" src="/assets/data/financescenarios-guides/configuration.json" label="Median and 5-95% band of the US short rate, the US 10-year rate and US inflation over thirty years, 1,000 scenarios" %}

A seed makes a run repeatable; another seed shows how much of a result is Monte Carlo noise. The `se` column of `summary_statistics` gives that noise directly: the standard error of the mean, which halves when the number of scenarios is four times as large. To simulate the five-year return of US stocks with five seeds at 500 and at 2,000 scenarios:

```python
for n_simulations in (500, 2000):
    for seed in range(1, 6):
        run = scenarios.simulate(calibration=calibration, n_simulations=n_simulations, seed=seed)
        print(n_simulations, seed, run.summary_statistics("us_broad").tail(1).select("mean", "se"))
```

With 500 scenarios the mean ranges from 7.99% to 9.39% a year across the five seeds, with a standard error of about 0.35 points; with 2,000 it ranges from 8.29% to 8.92%, with a standard error of about 0.18 points. When plotted:

{% include ft-chart.html id="configuration-seeds" src="/assets/data/financescenarios-guides/configuration.json" label="Mean five-year annualized return of US stocks for seeds 1 to 5 at 500 and at 2,000 scenarios" %}

### Beliefs: Your View over the Fit

A belief replaces part of the fit with your own view. A fixed value, such as a long-run inflation rate of 3%, changes the calibration and needs `calibrate(config)` again; a path of long-run levels and a one-off shock apply at simulation time, so they reuse a saved calibration. To pull US inflation's long-run level to 4% in year two and back to 2% by year five, with a jump of two points in year one:

```python
from financescenarios import BeliefPath, OUBeliefs, Shock, compare_runs

beliefs = OUBeliefs(
    long_run_mean=BeliefPath(anchors={2.0: 0.04, 5.0: 0.02}),
    shocks=[Shock(year=1.0, magnitude=0.02)],
)
us_inflation = config.inflation[0].model_copy(update={"beliefs": beliefs})
believed = config.model_copy(update={"inflation": [us_inflation, *config.inflation[1:]]})

result = scenarios.simulate(calibration=calibration, n_simulations=2000, seed=42)
with_belief = scenarios.simulate(believed, calibration=calibration, n_simulations=2000, seed=42)

with_belief.horizon_summary([1, 2, 3, 5], factors=["united_states_inflation"])
compare_runs(
    {"fitted": result, "belief": with_belief},
    statistic="terminal_median",
    factors=["united_states_inflation", "united_states_short_rate", "us_broad"],
)
```

The median US inflation is 5.50% after one year against 2.71% without the belief, 4.45% after two, 3.85% after three and 2.52% after five, against 1.81%. Every variable linked to inflation follows: the median short rate after five years is 6.06% against 4.39%, and US stocks return 7.94% a year against 8.73%. When plotted:

{% include ft-chart.html id="configuration-belief" src="/assets/data/financescenarios-guides/configuration.json" label="Median and 5-95% band of US inflation as fitted and with a belief path and a shock, over five years" %}

A [regime](/projects/financescenarios/docs/regimes) packages beliefs like these, together with the scenarios to keep, as a named story.

### A Configuration in Code

Profiles are a starting point; a `ScenariosConfig` can also be written from scratch, one entry per variable. To simulate the US short rate, US inflation and SPY over ten years, fitted on history since 1990:

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

A configuration of your own calibrates on the day it runs, so its numbers are from 23 October 2026 rather than the calibration of the other sections. Unemployment always comes along with inflation. Which returns:

| factor | category | metric | initial | terminal_mean | terminal_q05 | terminal_q95 |
|:-------|:---------|:-------|--------:|--------------:|-------------:|-------------:|
| inflation | inflation | rate | 0.0374 | 0.0260 | 0.0001 | 0.0486 |
| us_short_rate | interest_rates | rate | 0.0402 | 0.0284 | -0.0104 | 0.0694 |
| unemployment | unemployment | rate | 0.0420 | 0.0541 | 0.0261 | 0.0812 |
| us_broad | equities | annualized |  | 0.1132 | 0.0157 | 0.1930 |

Over ten years SPY returns 11.32% a year on average with these three variables alone against 8.49% over five years in the default factor set; runs compare only when they share their setup.

To keep a configuration as files, `scaffold_project("my-project")` copies the shipped settings profiles, factor sets, regimes and portfolios into a folder with a `.env` for the keys; `Scenarios.from_config_file` and `load_config` read them back. How It Works below describes every option those files take.

{% include ft-charts-script.html %}
