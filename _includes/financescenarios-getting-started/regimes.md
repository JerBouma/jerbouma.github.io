## Getting Started

The Regimes module tells a stress story to a run. A regime has two levers: **beliefs** change an assumption before simulating ("inflation heads to 12% within a year"), and **targets** keep the scenarios that fit the story afterwards ("the weakest 20% for stocks"). Because targets are quantiles of what the model itself produces, the kept scenarios stay ones the model finds plausible, and a run under a regime still returns the number of scenarios asked for.

This section uses the run from the [overview](/projects/financescenarios/docs) as the baseline: the default settings and factor set, calibrated on 19 October 2026, with 2,000 scenarios and seed 42. Every regime below runs on that same calibration and seed.

### The Shipped Regimes

Forty regimes ship with the package: historical episodes such as Black Monday, the 2008 crisis and the 2022 inflation surge, the stress tests of the Federal Reserve, the ESRB and the Bank of England, and stylized stories such as a soft landing or a tech selloff. `search_regimes` finds them by a few words. To list them all and search for high inflation:

```python
from financescenarios import list_presets, search_regimes

list_presets(kind="regimes")

search_regimes("high inflation")
```

Which returns the best matches first:

| id | name | category | description |
|:---|:-----|:---------|:------------|
| persistent_inflation | Persistent High Inflation | inflation | US inflation settles near 6.6% for the whole run instead … |
| oil_crisis | Oil Crisis | inflation | US inflation climbs to 12% within a year and eases to 5.5% b… |
| stagflation_1970s | 1970s Stagflation | inflation | Inflation near 9% and unemployment averaging 7.3% for … |
| volcker_shock | Volcker Shock | rates | Short rates replay 1979-82's climb to 16% while inflation … |
| inflation_shock_2022 | 2022 Inflation and Rate Hikes | inflation | Inflation climbs to 9% and falls back to 3% within a year, … |

### Beliefs Only: A Soft Landing

Soft Landing moves US inflation's long-run level along a path that reaches 2% by year five, and filters nothing out. To run it next to the baseline and compare the averages after five years:

```python
from financescenarios import Scenarios, compare_runs

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
result = scenarios.simulate(n_simulations=2000, seed=42)
soft_landing = scenarios.simulate(regime="soft_landing", n_simulations=2000, seed=42)

compare_runs(
    {"baseline": result, "soft_landing": soft_landing},
    factors=["united_states_inflation", "united_states_short_rate", "us_broad"],
)
```

Which returns:

| factor | baseline | soft_landing |
|:-------|---------:|-------------:|
| united_states_inflation | 0.0234 | 0.0205 |
| united_states_short_rate | 0.0459 | 0.0428 |
| us_broad | 0.0849 | 0.0854 |

Inflation averages 2.05% after five years instead of 2.34%, and the short rate follows it down through the policy rule, from 4.59% to 4.28%. A belief moves the centre of the range rather than its width. When plotted:

{% include ft-chart.html id="regimes-soft-landing" src="/assets/data/financescenarios-guides/regimes.json" label="Median and 5-95% band of US inflation in the baseline and under Soft Landing over five years" %}

### Targets Only: A Financial Crisis

Financial Crisis changes no assumption. It keeps the scenarios in which US stocks are in their weakest 20%, US unemployment in its highest 20% and the short rate in its lowest 30%, all at once. Few scenarios meet all three, so the run draws as many as it takes for 2,000 to fit. To run it:

```python
financial_crisis = scenarios.simulate(regime="financial_crisis", n_simulations=2000, seed=42)

compare_runs(
    {"baseline": result, "financial_crisis": financial_crisis},
    factors=["us_broad", "united_states_unemployment", "united_states_short_rate", "united_states_inflation"],
)
```

Which returns:

| factor | baseline | financial_crisis |
|:-------|---------:|-----------------:|
| us_broad | 0.0849 | -0.0394 |
| united_states_unemployment | 0.0553 | 0.0830 |
| united_states_short_rate | 0.0459 | 0.0020 |
| united_states_inflation | 0.0234 | 0.0168 |

US stocks lose 3.94% a year instead of gaining 8.49%, unemployment averages 8.30% instead of 5.53% and the short rate is cut to 0.20%, while inflation, which no target names, comes out lower as well, at 1.68%: the kept scenarios carry the links of the model with them. When plotted, one variable per tab:

{% include ft-chart.html id="regimes-financial-crisis" src="/assets/data/financescenarios-guides/regimes.json" label="Median and 5-95% band of the US stock market return, US unemployment and the US short rate in the baseline and under Financial Crisis over five years" %}

### Both at Once: Oil Shock, Oil Crisis and Climate Collapse

Most stories use both levers. Oil Shock adds a one-off jump of three points to US inflation in year two; Oil Crisis moves the median of US inflation to 12% after a year and 5.5% after three, as after the 1973 embargo, then back towards 2.5% by year eight, and keeps the scenarios with high short rates and weak stocks; Climate Collapse keeps the scenarios with the highest inflation and the weakest stocks. To run all three:

```python
runs = {"baseline": result}
for regime in ("oil_shock", "oil_crisis", "climate_collapse"):
    runs[regime] = scenarios.simulate(regime=regime, n_simulations=2000, seed=42)

compare_runs(runs, factors=["united_states_inflation", "united_states_short_rate", "us_broad"])
```

Which returns:

| factor | baseline | oil_shock | oil_crisis | climate_collapse |
|:-------|---------:|----------:|-----------:|-----------------:|
| united_states_inflation | 0.0234 | 0.0279 | 0.0592 | 0.0475 |
| united_states_short_rate | 0.0459 | 0.0570 | 0.1153 | 0.0671 |
| us_broad | 0.0849 | 0.0798 | -0.0126 | -0.0341 |

Oil Crisis steers inflation's long-run level so its expected path runs straight to 12% after one year and 5.5% after three, and on those dates moves every scenario by the same amount so that their median lands on the number while each keeps its distance from it. The scenarios it then keeps, those with high short rates and weak stocks, run hotter: a median of 12.98% after one year and 7.42% after three, and an average of 5.92% after five years. The short rate answers through the policy rule, to a median of 8.33% after one year and 14.18% after three and an average of 11.53% after five, and US stocks lose 1.26% a year. When plotted, US inflation in the four runs:

{% include ft-chart.html id="regimes-inflation" src="/assets/data/financescenarios-guides/regimes.json" label="Median and 5-95% band of US inflation in the baseline and under Oil Shock, Oil Crisis and Climate Collapse over five years" %}

### A Regulator's Stress Test

The stress tests of the Federal Reserve, the ESRB and the Bank of England ship as regimes that steer the scenarios along the published path. The Federal Reserve's 2026 severely adverse scenario takes US unemployment to 10%, US stocks down almost 60%, house prices down 30% and the short rate to 0.1%. To run it and compare the medians after five years:

```python
fed = scenarios.simulate(regime="fed_severely_adverse_2026", n_simulations=2000, seed=42)

compare_runs(
    {"baseline": result, "fed_severely_adverse_2026": fed},
    statistic="terminal_median",
    factors=["united_states_unemployment", "us_broad", "united_states_short_rate", "united_states_long_rate"],
)
```

Which returns:

| factor | baseline | fed_severely_adverse_2026 |
|:-------|---------:|--------------------------:|
| united_states_unemployment | 0.0515 | 0.0752 |
| us_broad | 0.0873 | -0.0032 |
| united_states_short_rate | 0.0439 | 0.0000 |
| united_states_long_rate | 0.0562 | 0.0266 |

On the published dates every scenario is on the regulator's path: unemployment at 7.2% after six months, 9.0% after one year and 9.8% after two, the short rate at 0.1% for three years and the 10-year rate between 2.3% and 2.7%. Stocks fall 52% in the median scenario over the first year and recover from there, to a return of -0.32% a year over five years. Between and after the published dates each scenario moves on with its own randomness. When plotted:

{% include ft-chart.html id="regimes-fed" src="/assets/data/financescenarios-guides/regimes.json" label="Median and 5-95% band of US unemployment, the US stock market return and the US short and 10-year rates in the baseline and under the Fed's 2026 severely adverse scenario over five years" %}

### A What-If of Your Own

A one-variable question, such as "what if inflation hit 8% within a year?", does not need a regime file: `shock_regime` builds one from the variable, the level and the timing, and the [Interest Rates](/projects/financescenarios/docs/interest-rates) page runs it. `load_regime` returns a shipped regime as an object to inspect or change, `RegimeLibrary` holds your own, and `stress_test_regime` builds a regime from a regulator's published scenario of another year. How It Works below describes every field.

{% include ft-charts-script.html %}
