## Getting Started

The Economy module simulates inflation, unemployment, the business cycle and longevity. In the default factor set inflation switches between calm and high-inflation spells, and unemployment between expansions and recessions; both feed the short rate's policy rule, so every scenario's rates, stocks and liabilities follow its own economy.

This section uses the run from the [overview](/projects/financescenarios/docs): the default settings and factor set, calibrated on 19 October 2026, with 2,000 scenarios and seed 42.

### Inflation in Three Economies

The default factor set simulates year-over-year consumer price inflation for the US, the euro area (fitted on Germany's long record) and the UK. To simulate them and read them off after one, three and five years:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
result = scenarios.simulate(n_simulations=2000, seed=42)

result.horizon_summary(
    [1, 3, 5], factors=["united_states_inflation", "eurozone_inflation", "united_kingdom_inflation"]
)
```

Which gives, among other columns:

| factor | horizon | q0.05 | q0.5 | q0.95 |
|:-------|--------:|------:|-----:|------:|
| united_states_inflation | 1 | 0.0076 | 0.0271 | 0.0622 |
| united_states_inflation | 3 | -0.0037 | 0.0200 | 0.0740 |
| united_states_inflation | 5 | -0.0064 | 0.0181 | 0.0770 |
| eurozone_inflation | 1 | 0.0057 | 0.0210 | 0.0484 |
| eurozone_inflation | 3 | -0.0012 | 0.0166 | 0.0549 |
| eurozone_inflation | 5 | -0.0027 | 0.0157 | 0.0541 |
| united_kingdom_inflation | 1 | 0.0098 | 0.0232 | 0.0585 |
| united_kingdom_inflation | 3 | 0.0041 | 0.0185 | 0.0565 |
| united_kingdom_inflation | 5 | 0.0020 | 0.0169 | 0.0525 |

Inflation starts at 3.74% in the US, 2.97% in the euro area and 3.24% in the UK, and the median falls to between 1.57% and 1.81% after five years. The bands are lopsided: the US 95th percentile rises from 6.22% to 7.70% while the median falls, because a minority of scenarios enter a high-inflation spell. When plotted:

{% include ft-chart.html id="economy-inflation" src="/assets/data/financescenarios-guides/economy.json" label="Median and 5-95% band of inflation in the US, the euro area and the UK over five years" %}

### The Regimes Behind It

The fitted parameters show the two regimes. To read them for the US:

```python
calibration = scenarios.calibrate()

calibration.calibrated_params["united_states_inflation"]
```

Which shows a calm regime at 1.21% and a high-inflation regime at 6.59%, whose shocks are 2.7 times as large (1.09% against 2.96%), and a chance of 13% that the economy is in the high regime today. The two levels are set so that the long-run mean meets the long-run expectation of 2.3% for the US; the euro area and the UK are anchored to 2.0%. The derivation of every number is in How It Works below.

The share of scenarios in a high-inflation spell is what the regimes add over a single mean-reverting model. To count, at every date, the scenarios with inflation above 5%:

```python
countries = {"US": "united_states", "Euro area": "eurozone", "UK": "united_kingdom"}

above_5 = {name: (result.paths[f"{country}_inflation"] > 0.05).mean(axis=0) for name, country in countries.items()}
```

After five years 12.1% of the US scenarios, 7.0% of the euro-area scenarios and 5.9% of the UK scenarios have inflation above 5%. When plotted:

{% include ft-chart.html id="economy-high-inflation" src="/assets/data/financescenarios-guides/economy.json" label="Share of the 2,000 scenarios with inflation above 5% in the US, the euro area and the UK" %}

### Unemployment {#unemployment-rate}

Unemployment reverts to its longer-run rate and, in the US and the UK, switches between expansions and recessions; in the US a fall in the stock market makes a recession likelier. To read it off after one, three and five years:

```python
result.horizon_summary(
    [1, 3, 5], factors=["united_states_unemployment", "eurozone_unemployment", "united_kingdom_unemployment"]
)
```

Which gives:

| factor | horizon | q0.05 | q0.5 | q0.95 |
|:-------|--------:|------:|-----:|------:|
| united_states_unemployment | 1 | 0.0350 | 0.0429 | 0.0566 |
| united_states_unemployment | 3 | 0.0330 | 0.0472 | 0.0814 |
| united_states_unemployment | 5 | 0.0337 | 0.0515 | 0.0894 |
| eurozone_unemployment | 1 | 0.0701 | 0.0795 | 0.0888 |
| eurozone_unemployment | 3 | 0.0644 | 0.0775 | 0.0905 |
| eurozone_unemployment | 5 | 0.0614 | 0.0760 | 0.0909 |
| united_kingdom_unemployment | 1 | 0.0442 | 0.0489 | 0.0601 |
| united_kingdom_unemployment | 3 | 0.0412 | 0.0497 | 0.0822 |
| united_kingdom_unemployment | 5 | 0.0402 | 0.0516 | 0.0961 |

US unemployment starts at 4.2% and its median drifts up to 5.15% over five years, while the 95th percentile reaches 8.94%: recessions push unemployment up fast and it comes down slowly. The euro area, fitted on France without regimes, stays in a narrow band around 7.6%. When plotted:

{% include ft-chart.html id="economy-unemployment" src="/assets/data/financescenarios-guides/economy.json" label="Median and 5-95% band of unemployment in the US, the euro area and the UK over five years" %}

The US recession regime is fitted on monthly data since 1955 and puts 12.4% of months in recession; once in it, the economy stays the next month with a chance of 87%. To count the scenarios in which unemployment has risen by a point or more from today's level:

```python
rise = {
    name: (result.paths[f"{country}_unemployment"] - result.paths[f"{country}_unemployment"][:, :1] >= 0.01).mean(axis=0)
    for name, country in countries.items()
}
```

That share grows from 10% after one year to 35% after three and 49% after five in the US, against 6%, 23% and 34% in the UK and at most 6% in the euro area. When plotted:

{% include ft-chart.html id="economy-unemployment-rise" src="/assets/data/financescenarios-guides/economy.json" label="Share of the 2,000 scenarios in which unemployment is at least one percentage point above today's level, for the US, the euro area and the UK" %}

### The Leading Indicator

The OECD's composite leading indicator for the US measures the business cycle on a scale around 100. In the default factor set it is simulated as a mean-reverting level; with business-cycle conditioning switched on, it also moves the drift of inflation, rates and credit spreads and the chance of an equity crisis. To read its fitted parameters:

```python
calibration.calibrated_params["leading_indicator"]
```

Which gives a long-run level of 99.74, a speed of 0.35 a year and a yearly volatility of 1.34 points, from a start at 101.0. After five years the 90% range runs from 97.4 to 102.5. When plotted:

{% include ft-chart.html id="economy-leading-indicator" src="/assets/data/financescenarios-guides/economy.json" label="Median, 25-75% and 5-95% band of the OECD composite leading indicator of the US over five years" %}

Mortality improvements, with the Cairns-Blake-Dowd model, are switched on per factor set; How It Works below covers the model and its data.

{% include ft-charts-script.html %}
