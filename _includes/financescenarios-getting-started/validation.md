## Getting Started

The Validation module asks the two questions a model validator asks of a scenario generator: does a run behave like the economy it describes, and would the model have held what actually happened, had it been fitted in the past on only what was known then? It measures the same relationships on history and on every scenario, sets each variable against the extremes of its longest record, checks the fitted parameters, and refits the whole model as of past dates to score what came next.

This section uses the calibration from the [overview](/projects/financescenarios/docs): the default settings and factor set, calibrated on 19 October 2026, with seed 42. The checks against history need many year-end observations per scenario, so they run 30 years ahead with 1,000 scenarios.

### A Run over Thirty Years

`validate` and `diagnose`, on the [overview](/projects/financescenarios/docs#checking-the-run), check a run against its own model. The checks below set it against history instead. To simulate 1,000 scenarios over 30 years:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
result = scenarios.simulate(n_simulations=1000, years=30, seed=42)
```

### Macro Relationships

`check_relationships` measures each macro relationship the same way on decades of history and on every scenario, such as how far the policy rate answers inflation or whether an inverted curve comes before higher unemployment, and grades the scenarios' median against history's estimate and its uncertainty. To run it:

```python
relationships = scenarios.check_relationships(result)

relationships.select("relationship", "region", "status", "history", "simulated_median")
```

Which returns 26 rows, of which the US ones are:

| relationship | status | history | simulated_median |
|:-------------|:-------|--------:|-----------------:|
| Policy rate reacts to inflation | warn | 0.4522 | 0.2136 |
| Policy rate reacts to unemployment | pass | -0.5787 | -0.3812 |
| Rates near neutral at target, higher above it | pass | 0.0570 | 0.0336 |
| Phillips curve | pass | -0.5923 | -0.3195 |
| Bear markets come with rising unemployment | warn | -0.4096 | -0.1175 |
| Long rate moves with the short rate | pass | 0.3303 | 0.5820 |
| Inverted curve precedes higher unemployment | warn | -0.6712 | -0.2604 |
| Real equity returns fall with high inflation | pass | -0.1525 | -0.0804 |
| Higher rates slow house prices | pass | -0.9628 | -0.8992 |
| Oil prices pass into inflation | warn | 0.0440 | 0.0115 |

Twenty of the 26 relationships pass and six warn; none fails. Every sign matches history in the US, and what warns is a link that is there but weaker: the policy rate answers inflation with a slope of 0.21 against history's 0.45, bear markets come with rising unemployment at -0.12 against -0.41, and oil passes into inflation at 0.012 against 0.044. Outside the US, the euro-area policy rate answers inflation more strongly than history did (0.24 against 0.04) and the UK's inverted curve foreshadows unemployment more weakly (-0.11 against -0.45). When plotted, the US relationships:

{% include ft-chart.html id="validation-relationships" src="/assets/data/financescenarios-guides/validation.json" label="Ten US macro relationships measured on history and as the median across 1,000 scenarios over thirty years" %}

### History's Extremes and Parameter Guardrails

`check_realism` reads each variable at year ends against its longest record: its lowest and highest levels, its largest one-year rises and falls, its deepest drawdowns and its longest stretches at the lower bound or with an inverted curve. It flags a tail that the scenarios reach too rarely ("tail too thin") or too often ("tail too fat"). With `summary=True` it returns one row per variable. To run it:

```python
scenarios.check_realism(result, summary=True)
```

Which flags every variable somewhere: 5 of the 23 warn and 18 fail. Most flags are thin tails: over 30 years the scenarios reach history's record years less often than history's own windows did, for most of the rates and the unemployment of all three economies, house prices, Japanese stocks and crude oil's largest one-year rise. A few go the other way, such as low inflation in the US and the UK. How It Works below describes every test.

`check_parameters` puts guardrails on the fitted parameters themselves: fits at a bound, half-lives, long-run levels against history's range, volatility against the history behind the fit, and the equity crisis regimes against the same model fitted on the long US record. To list the ones that flag:

```python
scenarios.check_parameters(result, flagged_only=True)
```

Which returns six warnings and no failures. UK inflation, fitted on its inflation-targeting era from 1993, swings 0.51 times as much as in its longer history; euro-area unemployment settles at 7.16%, just below the 7.20% to 10.90% of the French history it was fitted on; the euro-area short rate swings 1.67 times its calibration history and the UK long rate 0.64 times; and Japan's stock market is in its crisis regime 44.9% of the time against 16.5% in the long US record, with calm spells of 1.16 years against 3.39.

### Back to the End of 2007

The harder test refits the model in the past. `out_of_sample` cuts every series at a date, fits the model on the history before it with the published values known that day, such as the neutral rate in the policy rule, and simulates from that day's values; the table sets each year-end against what happened. To run it from the end of 2007 for six variables:

```python
factors = [
    "us_broad",
    "united_states_unemployment",
    "united_states_short_rate",
    "united_states_long_rate",
    "united_states_inflation",
    "united_kingdom_inflation",
]
crisis = scenarios.out_of_sample(as_of="2007-12-31", years=5, n_simulations=1000, seed=42, factors=factors)

crisis.table.select("factor", "date", "realized", "p5", "p50", "p95", "pit")
crisis.scores.select("factor", "coverage_50", "coverage_90", "pit_mean", "crps_skill")
```

The financial crisis falls largely outside the scenarios, because of its speed. US unemployment reached 7.3% at the end of 2008 and 9.9% at the end of 2009, while one scenario in twenty went above 6.36% and 7.45%; it was back inside the 90% band only in 2011, at 8.5%. The short rate was cut to 0.11% within the year against a 5th percentile of 1.05%, and US stocks were down 36.8% by the end of 2008 against a 5th percentile of -12.0%. In the scores, the 90% band held four of the five years for both rates and US inflation, three for stocks and two for unemployment and UK inflation; on CRPS the scenarios beat a no-change forecast for every variable except stocks. When plotted, one variable per tab:

{% include ft-chart.html id="validation-crisis" src="/assets/data/financescenarios-guides/validation.json" label="5th percentile, median and 95th percentile of six US and UK variables at each year end from 2008 to 2012, fitted on what was known at the end of 2007, against what happened" %}

What the fit knew is in the run's notes, each value with its source. To print the ones the US policy rule read:

```python
for note in crisis.notes:
    if note.startswith("united_states_short_rate:"):
        print(note)
```

Which shows, among others, a neutral real rate of 2.14% as known on 31 December 2007 (today 1.20%), from the New York Fed's real-time Laubach-Williams estimate published on 20 December 2007, and a longer-run unemployment rate of 5.01% (today 4.20%), from the earliest published vintage of the Congressional Budget Office's estimate. A backtest that read today's values would carry into 2007 what was learned only afterwards.

### Back to the End of 2019

The same test from the end of 2019 covers the pandemic and the inflation that followed. To run it:

```python
pandemic = scenarios.out_of_sample(as_of="2019-12-31", years=5, n_simulations=1000, seed=42, factors=factors)

pandemic.scores.select("factor", "coverage_50", "coverage_90", "pit_mean", "crps_skill")
```

Here the scenarios hold more. US stocks stay inside the 90% band in all five years, through the 2020 crash and the rally after it. The jump in US unemployment to 6.7% at the end of 2020 is above the band's 5.34%, and the cut to zero lies below it at first (0.07% against a 5th percentile of 0.38%); from 2021 both are inside. The inflation that followed does not fit: US inflation of 7.04% at the end of 2021 is above the 95th percentile of 4.07%, and UK inflation, fitted on its calm years since 1993, is above its narrow band from 2021 to 2024, at 9.24% in 2022 against 3.30%. When plotted:

{% include ft-chart.html id="validation-pandemic" src="/assets/data/financescenarios-guides/validation.json" label="5th percentile, median and 95th percentile of six US and UK variables at each year end from 2020 to 2024, fitted on what was known at the end of 2019, against what happened" %}

### Every Four Years since 2003

One crisis is an anecdote. `out_of_sample_many` runs the same test from several origins and scores every variable across them; with origins four years apart and four-year runs, the forecasts do not overlap and every year from 2004 to 2023 is scored once. To run it for all 27 variables:

```python
evaluation = scenarios.out_of_sample_many(
    origins=["2003-12-31", "2007-12-31", "2011-12-31", "2015-12-31", "2019-12-31"],
    years=4,
    n_simulations=1000,
    seed=42,
)
evaluation.scores.select("factor", "origins", "coverage_50", "coverage_90", "pit_mean", "crps_skill")
```

A 90% band should hold 90% of the years. US and euro-area inflation hold 85% and UK inflation 60%; the US short and long rates hold 90% and the UK short rate 85%, while the euro-area rates hold 50% and 70% and ended below the middle of the scenarios in most years, with PIT means of 0.33 and 0.39. Unemployment's bands are too narrow in the US and the euro area (50%), as are US house prices' (50%); US stocks hold 85%. On CRPS every variable beats a no-change forecast except UK unemployment. Small caps, gold, European and emerging-market stocks and oil have shorter histories and enter from later origins. When plotted:

{% include ft-chart.html id="validation-coverage" src="/assets/data/financescenarios-guides/validation.json" label="Share of the years from 2004 to 2023 inside the 90% band per variable, five origins four years apart, against the 90% it should hold" %}

How It Works below covers the theory behind each check, the martingale test of a risk-neutral run, the external benchmarks and what is not validated.

{% include ft-charts-script.html %}
