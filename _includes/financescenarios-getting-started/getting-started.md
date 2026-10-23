## Getting Started

Finance Scenarios fits interest rates, inflation, unemployment, equities, currencies and commodities to their history and simulates thousands of joint futures of them, so a question such as "where could rates and stocks be in five years?" gets a distribution rather than a single forecast. This section covers the basics: choosing a run, simulating it, reading the result, checking it and keeping it. Each module's own page opens with a Getting Started section of its own.

Every page uses one run: the default settings and the default factor set, calibrated on 19 October 2026, with 2,000 scenarios and seed 42. Live data moves, so a run on another day gives slightly different numbers.

### Data and API Keys

Most of the history comes from Financial Modeling Prep through the [Finance Toolkit](https://github.com/JerBouma/FinanceToolkit): stock markets, government bond yields, commodities and dividends. The free plan allows 250 requests a day, five years of data and US-listed securities only, which is enough to try it out; the longer histories and markets outside the US need a paid plan. You can get a key [through this link](/fmp){:target="_blank"}, which also gives 15% off the paid plans and supports the project. A free [FRED key](https://fred.stlouisfed.org/docs/api/api_key.html){:target="_blank"} is optional and adds US corporate bond spreads and commercial property prices. The OECD, central-bank and Ken French data need no key at all.

### Choosing a Run

Every run combines two ready-made profiles: a **settings** profile, which says how the run goes (how many scenarios, how far ahead, how much history to learn from), and a **factor set**, which says what gets simulated. A **regime** can add a stress story and a **portfolio** reads the scenarios through an investment mix; both have their own page. To list the settings profiles:

```python
from financescenarios import list_presets

list_presets(kind="settings")  # or "factor-sets", "regimes", "portfolios"
```

Which returns each profile with what it is for:

| id | description |
|:---|:------------|
| default | 2,000 scenarios, one step a month, five years ahead, fitted … |
| goes | Default, but fitted on history since 2019 only; pair it with… |
| long_horizon | Default with 500 scenarios instead of 2,000, so multi-decade… |
| wilkie | Default, fitted on 1995 to 2007 only, as the wilkie set need… |

The factor sets range from `default` (the US, the euro area and the UK, each factor fitted to its long history and linked the way the economy is) to `broad` (more countries, US sectors and styles, more commodities and currencies), with `goes`, `ahlgrim`, `hibbert`, `wilkie` and `dnb` as published generators and models written the way their authors did. The [Configuration](/projects/financescenarios/docs/configuration) page describes each.

### Simulating Scenarios

Everything starts with a `Scenarios` instance. The API keys go in here, as with the Finance Toolkit; leave them out to read them from your environment or a `.env` file. `simulate` collects the history, fits every factor, estimates how the factors move together and draws the scenarios. To simulate 2,000 scenarios of the default factor set:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(
    settings="default",
    factor_set="default",
    api_key="FINANCIAL_MODELING_PREP_KEY",
    fred_api_key="FRED_KEY",  # optional
)
result = scenarios.simulate(n_simulations=2000, seed=42)

result.describe()
```

Which returns where each of the 27 variables starts and where it ends up after five years, of which six are shown below. Rates are yearly rates and anything with a price the annualized return from today, written as decimals (0.0459 is 4.59%):

| factor | category | metric | initial | terminal_mean | terminal_q05 | terminal_q95 |
|:-------|:---------|:-------|--------:|--------------:|-------------:|-------------:|
| united_states_inflation | inflation | rate | 0.0374 | 0.0234 | -0.0064 | 0.0770 |
| united_states_short_rate | interest_rates | rate | 0.0408 | 0.0459 | 0.0000 | 0.1099 |
| united_states_unemployment | unemployment | rate | 0.0420 | 0.0553 | 0.0337 | 0.0894 |
| us_broad | equities | annualized |  | 0.0849 | -0.0569 | 0.2082 |
| europe | equities | annualized |  | 0.0933 | -0.0753 | 0.2487 |
| gold | commodities | annualized |  | 0.0308 | -0.0999 | 0.1716 |

US inflation starts at 3.74% and averages 2.34% after five years, the US short rate starts at 4.08% and averages 4.59%, and US stocks return 8.49% a year on average, with one scenario in twenty below -5.69% a year. To draw the median of three of them with the bands that hold half and nine in ten of the scenarios:

```python
result.plot(["united_states_short_rate", "united_states_inflation", "us_broad"])
```

When plotted, one variable per tab:

{% include ft-chart.html id="scenarios-overview" src="/assets/data/financescenarios-guides/getting-started.json" label="Median, 25-75% and 5-95% bands of the US short rate, US inflation and the annualized US stock market return over five years" %}

### Reading the Distribution

`summary_statistics` gives one variable's mean, standard deviation, Monte Carlo standard error and percentiles at every date, and `horizon_summary` reads the same off at chosen horizons. To get both:

```python
result.summary_statistics("united_states_short_rate")

result.horizon_summary([1, 3, 5], factors=["us_broad", "united_states_inflation"])
```

The first returns a row per month; its last three rows show that the short rate's mean is known to within 0.08 percentage points (the `se` column) after five years:

| date | mean | std | se | q0.05 | q0.25 | q0.5 | q0.75 | q0.95 |
|:-----|-----:|----:|---:|------:|------:|-----:|------:|------:|
| 2030-11-01 | 0.0459 | 0.0341 | 0.0008 | 0.0000 | 0.0204 | 0.0437 | 0.0650 | 0.1095 |
| 2030-12-02 | 0.0458 | 0.0343 | 0.0008 | 0.0000 | 0.0198 | 0.0435 | 0.0651 | 0.1089 |
| 2031-01-01 | 0.0459 | 0.0345 | 0.0008 | 0.0000 | 0.0196 | 0.0439 | 0.0659 | 0.1099 |

The second returns a row per variable and horizon:

| factor | horizon | mean | std | q0.05 | q0.25 | q0.5 | q0.75 | q0.95 |
|:-------|--------:|-----:|----:|------:|------:|-----:|------:|------:|
| us_broad | 1 | 0.0917 | 0.1570 | -0.1785 | -0.0053 | 0.0968 | 0.1973 | 0.3361 |
| us_broad | 3 | 0.0859 | 0.0985 | -0.0795 | 0.0241 | 0.0914 | 0.1555 | 0.2387 |
| us_broad | 5 | 0.0849 | 0.0806 | -0.0569 | 0.0337 | 0.0873 | 0.1393 | 0.2082 |
| united_states_inflation | 1 | 0.0294 | 0.0170 | 0.0076 | 0.0193 | 0.0271 | 0.0364 | 0.0622 |
| united_states_inflation | 3 | 0.0245 | 0.0234 | -0.0037 | 0.0102 | 0.0200 | 0.0322 | 0.0740 |
| united_states_inflation | 5 | 0.0234 | 0.0254 | -0.0064 | 0.0077 | 0.0181 | 0.0312 | 0.0770 |

A return read as a yearly average narrows with the horizon: the 90% range of US stocks runs from -17.85% to 33.61% over one year and from -5.69% to 20.82% a year over five, while inflation's range widens from 0.76%-6.22% to -0.64%-7.70% as it moves away from today's reading. When plotted, the stock market rows:

{% include ft-chart.html id="scenarios-horizons" src="/assets/data/financescenarios-guides/getting-started.json" label="5th percentile, median and 95th percentile of the annualized US stock market return after one, three and five years" %}

To see where the five-year return lands across all 2,000 scenarios:

```python
result.plot("us_broad", kind="distribution")
```

Which counts the scenarios per percentage point of yearly return. The median is 8.73% a year and 14% of the scenarios end with a loss. When plotted:

{% include ft-chart.html id="scenarios-equity-distribution" src="/assets/data/financescenarios-guides/getting-started.json" label="Distribution of the five-year annualized US stock market return across 2,000 scenarios, with the 5th percentile, median and 95th percentile" %}

### Individual Scenarios

A percentile band is not a path: no single scenario follows the median. `to_dataframe` returns every scenario of a variable, one row per scenario and one column per date, ready for your own valuation or ALM model. To get the US short rate's paths:

```python
paths = result.to_dataframe("united_states_short_rate")

paths.select(paths.columns[:6]).head()
```

Which returns the first five scenarios over the first four months:

| scenario | 2026-01-01 | 2026-01-31 | 2026-03-03 | 2026-04-02 | 2026-05-03 |
|---------:|-----------:|-----------:|-----------:|-----------:|-----------:|
| 0 | 0.0408 | 0.0431 | 0.0490 | 0.0526 | 0.0491 |
| 1 | 0.0408 | 0.0441 | 0.0426 | 0.0429 | 0.0424 |
| 2 | 0.0408 | 0.0416 | 0.0446 | 0.0450 | 0.0473 |
| 3 | 0.0408 | 0.0422 | 0.0435 | 0.0435 | 0.0436 |
| 4 | 0.0408 | 0.0450 | 0.0433 | 0.0412 | 0.0437 |

When plotted, the same five scenarios over all five years:

{% include ft-chart.html id="scenarios-paths" src="/assets/data/financescenarios-guides/getting-started.json" label="The US short rate in the first five of 2,000 scenarios over five years" %}

### Checking the Run

Before relying on a run it is worth knowing how far to trust it. `validate` runs six checks on the calibration and the simulation, and `diagnose` sets each mean-reverting variable's simulated mean and spread against the ones its own model implies in the long run. To run both:

```python
scenarios.validate(result)

result.diagnose()
```

Which returns, for the checks:

| check | status | detail |
|:------|:-------|:-------|
| Every factor calibrated | pass | every factor calibrated |
| Parameters in a plausible range | pass | every long-run level and half-life in range |
| Valid correlation matrix | pass | 27 factors, smallest eigenvalue 1.14e-01, symmetric True, unit diagonal True; shrinkage 0.15; repair 0.00 |
| Simulation reproduces the correlations | warn | largest gap 0.103 (eurozone_inflation/united_kingdom_inflation) |
| Simulated volatility matches history | warn | 16 factors compared, median ratio 0.99; outside 0.67-1.50x: eurozone_short_rate 1.72x |
| Every path is finite | pass | 27 factors, all finite |

Four checks pass and two warn: the euro-area and UK inflation correlation comes out 0.103 away from the one it was given, and the euro-area short rate moves 1.72 times as much as in its history. `diagnose` returns a row for each of the nine variables with long-run moments; three of them, US and UK unemployment and the yield curve's slope, are flagged because they settle slowly, with half-lives of 2.9, 5.1 and 7.3 years against a five-year run, so a gap is expected. The [Validation](/projects/financescenarios/docs/validation) page goes much further: whether the factors move together the way the economy does, whether they stay within what history has seen, and whether a model fitted in the past would have held what happened next.

### Keeping a Run

A calibration downloads and fits everything, which takes about two minutes; the simulation itself takes under a second. `calibrate` returns the fitted calibration, which can be saved and passed back to `simulate`, and the same seed then gives back exactly the same scenarios. `save` stores a whole run, its settings and its calibration in a folder of its own, and `read_run` reads it back without calibrating or simulating anything. To do both:

```python
from financescenarios import CalibrationResult, read_run

calibration = scenarios.calibrate()
calibration.save("calibration.json")

calibration = CalibrationResult.load("calibration.json")
result = scenarios.simulate(calibration=calibration, n_simulations=2000, seed=42)

path = scenarios.save(result, "results/")
result = read_run(path)
```

Every page of this documentation runs on the calibration of 19 October 2026 this way, and reading the saved run back gives the same 2,000 scenarios of 27 variables, value for value.

The module pages build on this run: [Configuration](/projects/financescenarios/docs/configuration) changes the horizon, the history and the beliefs, [Interest Rates](/projects/financescenarios/docs/interest-rates), [Economy](/projects/financescenarios/docs/economy) and [Markets](/projects/financescenarios/docs/markets) look at each group of variables, [Regimes](/projects/financescenarios/docs/regimes) adds stress stories, [Portfolio](/projects/financescenarios/docs/portfolio) and [Solvency](/projects/financescenarios/docs/solvency) read the scenarios through an investment mix and a balance sheet, and [Validation](/projects/financescenarios/docs/validation) tests the model against history.

{% include ft-charts-script.html %}
