## Getting Started

The Interest Rates module simulates a short rate and a 10-year rate per currency. In the default factor set the short rate follows a monetary-policy rule on each scenario's own inflation and unemployment, starting from the path the bond market expects, and the 10-year rate is that expected path plus a term premium. So a scenario with high inflation gets high rates, and the curve's slope moves the way central banks and bond markets make it move.

This section uses the run from the [overview](/projects/financescenarios/docs): the default settings and factor set, calibrated on 19 October 2026, with 2,000 scenarios and seed 42.

### The Short and Long Rates

The default factor set has a short rate (the 3-month rate) and a 10-year government rate for the US, the euro area (German Bunds) and the UK. To simulate them and get the rows that belong to them:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
result = scenarios.simulate(n_simulations=2000, seed=42)

result.describe()
```

Which gives, for the six rates:

| factor | initial | terminal_mean | terminal_q05 | terminal_q95 |
|:-------|--------:|--------------:|-------------:|-------------:|
| united_states_short_rate | 0.0408 | 0.0459 | 0.0000 | 0.1099 |
| united_states_long_rate | 0.0511 | 0.0579 | 0.0180 | 0.1072 |
| eurozone_short_rate | 0.0264 | 0.0359 | -0.0050 | 0.0901 |
| eurozone_long_rate | 0.0347 | 0.0416 | 0.0123 | 0.0786 |
| united_kingdom_short_rate | 0.0399 | 0.0395 | 0.0010 | 0.0839 |
| united_kingdom_long_rate | 0.0524 | 0.0481 | 0.0176 | 0.0821 |

The 5th percentile of each short rate sits on its floor after five years: 0% for the US, -0.5% for the euro area and 0.1% for the UK, the lowest policy rate each central bank has set. The 95th percentiles reach 11.0%, 9.0% and 8.4%, the scenarios in which inflation took off. When plotted, the short rates:

{% include ft-chart.html id="interest-rates-short" src="/assets/data/financescenarios-guides/interest-rates.json" label="Median and 5-95% band of the short rate of the US, the euro area and the UK over five years" %}

The 10-year rates move less, as each is the average of the short rates expected over ten years plus a premium. When plotted:

{% include ft-chart.html id="interest-rates-long" src="/assets/data/financescenarios-guides/interest-rates.json" label="Median and 5-95% band of the 10-year rate of the US, the euro area and the UK over five years" %}

### What the Policy Rule Reads

`calibrate` returns every fitted and sourced number, per variable. The short rate's parameters hold the rule: its weights on the inflation and unemployment gaps, the neutral real rate, the inflation target, the longer-run unemployment rate and the floor, and the calibration notes say where each comes from. To read them for the US:

```python
calibration = scenarios.calibrate()

calibration.calibrated_params["united_states_short_rate"]

calibration.calibration_notes["united_states_short_rate"]
```

Which shows the balanced-approach rule the Federal Reserve reports in its [Monetary Policy Report (2026, Box 4, Table A)](https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-part2.htm){:target="_blank"}, with weights of 0.5 on the inflation gap and 2.0 on the unemployment gap, and the numbers it reads per economy:

| | US | Euro area | UK |
|:--|--:|--:|--:|
| Neutral real rate | 1.20% | 0.09% | 1.00% |
| Inflation target | 2.00% | 2.00% | 2.00% |
| Longer-run unemployment | 4.20% | 7.16% | 4.21% |
| Floor | 0.00% | -0.50% | 0.10% |
| Rule's steady state | 3.20% | 2.09% | 3.00% |

Each run starts from the market's expected path, read from that day's government curve: for the US, the New York Fed's fit of the Treasury curve of 15 October 2026 expects the short rate at 4.32%, 4.42%, 4.27% and 4.07% in one, two, five and ten years, after which the path heads to the rule's steady state of 3.20%. The euro area's path comes from the Bundesbank's curve and the UK's from the Bank of England's. The path of each currency is stored with the calibration:

```python
for country in ["united_states", "eurozone", "united_kingdom"]:
    market_path = calibration.calibrated_params[f"{country}_short_rate"].market_path
    print(country, market_path.times, market_path.rates)
```

When plotted, the three expected paths over the next ten years:

{% include ft-chart.html id="interest-rates-market-path" src="/assets/data/financescenarios-guides/interest-rates.json" label="Expected short-rate path of the US, the euro area and the UK over ten years, from each central bank's government curve" %}

The 10-year rate's own parameters hold its term premium and how much of a short-rate move it carries. To read them:

```python
calibration.calibrated_params["united_states_long_rate"]

calibration.calibration_notes["united_states_long_rate"]
```

Which gives a long-run term premium of 1.34% for the US, 0.94% for the euro area and 1.03% for the UK. A 10-year yield carries 0.76 of a short-rate move in the US, 0.55 in the euro area and 0.81 in the UK, from how fast each country's short rate has reverted since 1950.

### The Slope of the Curve

The paths of a run are plain arrays, one row per scenario and one column per date, so anything built from two variables is one line away. The slope of the curve is the 10-year rate minus the short rate, and a negative slope is an inverted curve. To compute it and the share of scenarios in which the curve is inverted at each date:

```python
countries = {"US": "united_states", "Euro area": "eurozone", "UK": "united_kingdom"}

spread = {
    name: result.paths[f"{country}_long_rate"] - result.paths[f"{country}_short_rate"]
    for name, country in countries.items()
}
inverted = {name: (paths < 0).mean(axis=0) for name, paths in spread.items()}
```

Every curve starts upward sloping, by 1.03 percentage points in the US, 0.83 in the euro area and 1.25 in the UK, and the median US slope is still 1.26 points after five years. When plotted:

{% include ft-chart.html id="interest-rates-spread" src="/assets/data/financescenarios-guides/interest-rates.json" label="Median and 5-95% band of the 10-year rate minus the short rate of the US, the euro area and the UK over five years" %}

The share of inverted curves follows the market's expected path. The Bank of England's curve expects UK short rates to rise to 4.95% within a year, so after one year 58% of the UK scenarios have an inverted curve, against 37% in the euro area and 10% in the US; after five years it is 31%, 31% and 15%. When plotted:

{% include ft-chart.html id="interest-rates-inversion" src="/assets/data/financescenarios-guides/interest-rates.json" label="Share of the 2,000 scenarios in which the 10-year rate is below the short rate, for the US, the euro area and the UK" %}

### The Rule at Work: An Inflation Shock

Because the short rate follows a rule on inflation, a scenario in which inflation jumps also gets the rate rises that answer it. `shock_regime` builds a one-variable what-if: here US inflation heads to 8% within a year and back onto its usual path by year five, while every scenario keeps its own randomness. To run it on the same calibration and compare the medians after five years:

```python
from financescenarios import compare_runs, shock_regime

regime = shock_regime("inflation", 0.08, calibration=calibration)
shocked = scenarios.simulate(regime=regime, calibration=calibration, n_simulations=2000, seed=42)

compare_runs(
    {"baseline": result, "inflation_at_8": shocked},
    statistic="terminal_median",
    factors=["united_states_inflation", "united_states_short_rate", "united_states_long_rate"],
)
```

Which returns:

| factor | baseline | inflation_at_8 |
|:-------|---------:|---------------:|
| united_states_inflation | 0.0181 | 0.0181 |
| united_states_short_rate | 0.0439 | 0.0612 |
| united_states_long_rate | 0.0562 | 0.0793 |

The median inflation is 7.64% after one year against 2.71% in the baseline and 4.66% after three, and is back on the baseline's 1.81% after five. The rule answers with a lag: the median short rate rises from 4.33% to 6.24% in the first year and to 8.71% after three, and is still 6.12% after five years, when inflation has long come back. When plotted, the short rate and inflation in both runs:

{% include ft-chart.html id="interest-rates-shock" src="/assets/data/financescenarios-guides/interest-rates.json" label="Median and 5-95% band of the US short rate and US inflation in the baseline and with inflation at 8% within a year" %}

The term structure (Nelson-Siegel level, slope and curvature), the arbitrage-free HJM forward curve and the KNW models of rates and inflation together are switched on per factor set; How It Works below covers each.

{% include ft-charts-script.html %}
