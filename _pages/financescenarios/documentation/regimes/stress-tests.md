---
title: Stress Tests
seo_title: "Stress Tests | Finance Scenarios"
seo_title_suffix: false
excerpt: "How the stress tests of the Federal Reserve, the ESRB and the Bank of England run in Finance Scenarios: the published path becomes beliefs that every scenario meets on its dates, with each scenario's own randomness around it."
description: "Supervisory stress tests in Finance Scenarios: the Fed's and the ESRB's scenarios as regimes, how rates, inflation, unemployment and equities follow the published path, the NGFS climate overlay and a run of the Fed's 2026 severely adverse scenario."
author_profile: false
permalink: /projects/financescenarios/docs/regimes/stress-tests
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/regimes
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-regimes"
---

The supervisory stress tests publish a path for the economy over the next few years: where rates, inflation, unemployment and stock prices go in an adverse scenario. Each runs as a regime that holds every scenario to that path on its published dates, with each scenario's own randomness around it and after it, so the result is a distribution around the regulator's story rather than one line. The Federal Reserve's 2026 scenario, the ESRB's 2025 scenario and the Bank of England's 2025 stress test ship as regimes, and `stress_test_regime` builds one from a published scenario of another year. A climate pathway can be laid over a run as well.

## The Published Scenarios

Instead of writing a recession by hand, a regime can follow a regulator's published scenario, fetched through the Finance Toolkit with no API key:

<div class="ca-cards">
  <div><i class="ca-icon fas fa-landmark" aria-hidden="true"></i><p class="ca-card-title">Federal Reserve</p><p>The US supervisory scenarios, baseline and severely adverse: 13 quarters, from the first quarter of 2026 to the first quarter of 2029, of the 3-month and 10-year Treasury rates, CPI inflation, unemployment and the stock market (<a href="https://www.federalreserve.gov/publications/files/2026-final-supervisory-stress-test-scenarios-20260204.pdf#page=13" target="_blank">Federal Reserve, 2026 Supervisory Stress Test Scenarios, p. 7</a>).</p></div>
  <div><i class="ca-icon fas fa-earth-europe" aria-hidden="true"></i><p class="ca-card-title">ESRB</p><p>The European Systemic Risk Board's scenario for the European Banking Authority's (EBA) <a href="https://www.eba.europa.eu/publications-and-media/press-releases/eba-launches-its-2025-eu-wide-stress-test" target="_blank">2025 EU-wide bank stress test</a>: three years (2025 to 2027) of the long-term rate, inflation, unemployment and stock prices for every EU member and the main other economies.</p></div>
</div>

## The Path Becomes Beliefs

The published path is turned into beliefs rather than run as one deterministic path. Each interest rate, inflation and unemployment factor follows the scenario for its own country. With published values $$v_k$$ at horizons $$h_k$$, the factor's long-run level runs through them in straight lines, $$\theta(h_k) = v_k$$, and on each date every scenario is set to the value, a shock in `absolute` mode:

$$
X^{(i)}_{h_k} = v_k \quad \text{for every scenario } i
$$

So every scenario meets the published values, even a slow-moving short rate. Between two published values the median walks in a straight line from one to the next, so a path a year apart arrives month by month rather than in one step, and after the last one each scenario moves on with its own randomness. Every path is laid over the run from its start; the ESRB's values are annual averages, so each is dated at the middle of its year, and the Federal Reserve's quarterly values keep their quarter's end. A gentler option (`follow="target"` in `stress_test_regime`) moves only the long-run level, and the factor drifts toward the values at its own speed. After the last value the long-run level returns to its calibrated value in a straight line over five years by default, and the factor follows it at its own speed; a [policy-rule short rate](/projects/financescenarios/docs/interest-rates) or an [expected-path long rate](/projects/financescenarios/docs/interest-rates/long-rate) is prescribed by the path up to its last value, then converges in a straight line onto its usual path before its rule or expected path takes over; while prescribed, the rate takes each move of the path rather than chasing it at the rule's speed.

## Equities Follow the Published Market

Equities follow the published stock market as one-off jumps in the log price, after which the equity model carries on. The published log level $$\ell_k$$ is $$\ln(\text{adverse}_k/\text{baseline}_k)$$ for the Federal Reserve, so normal growth is not counted as stress, and $$\ln(1 + d_k)$$ for the ESRB, with $$d_k$$ its published fall from the start. Each period adds

$$
J_k = \ell_k - \ell_{k-1}
$$

to every scenario's log price on its date. Every real-world equity follows one region's market, whatever its own: by default the United States or the European Union, depending on the scenario. For the Dow Jones Total Stock Market Index under the Federal Reserve's 2026 scenarios ([Federal Reserve, 2026 Supervisory Stress Test Scenarios, p. 4](https://www.federalreserve.gov/publications/files/2026-final-supervisory-stress-test-scenarios-20260204.pdf#page=10){:target="_blank"}):

<div class="ca-nums fs-nums">
  <span><b>31,161</b>at the end of 2026, severely adverse</span>
  <span><b>70,592</b>at the end of 2026, baseline</span>
  <span><b>56%</b>lower than the baseline</span>
  <span><b>about 58%</b>fall in the first three quarters</span>
</div>

## Another Year's Scenario

For a published scenario that does not ship as a regime, such as another year's, `stress_test_regime` builds the regime itself. To build the Federal Reserve's severely adverse scenario this way and run it:

```python
from financescenarios import Scenarios, build_toolkit, load_profiles, stress_test_regime

config = load_profiles(settings_id="default", factor_set_id="default")
toolkit = build_toolkit(config, api_key="FINANCIAL_MODELING_PREP_KEY")

# authority="esrb" with scenario="adverse" for the EBA test
regime = stress_test_regime(toolkit, config, authority="federal_reserve", scenario="severely_adverse")
stressed = Scenarios.from_config(config, toolkit=toolkit, regime=regime).simulate()
```

<div class="fs-callout fs-callout--limits" markdown="1">
<p class="fs-callout__title">Limits</p>

- `stress_test_regime` steers real-world interest rates under Hull-White or CIR (the default's policy-rule short rates and expected-path long rates among them), inflation under the plain mean-reverting model or the default's regime-switching one (moving both regimes' levels), and unemployment. Other models and every risk-neutral factor keep their calibration.
- The Federal Reserve's scenario covers only the United States: its rates, inflation and unemployment move only the US factors, while every real-world equity follows the US stock market.
- The shipped regimes go further than `stress_test_regime`: they also set house prices and currencies from the published scenarios, and the Bank of England's sets oil. Rather than move every equity with one region's market, they move the others by their expected move given it ([Regimes](/projects/financescenarios/docs/regimes#other-markets-in-a-crash)).
- The Federal Reserve's inflation is an annualized quarter-on-quarter rate ([Federal Reserve, 2026 Supervisory Stress Test Scenarios, p. 8](https://www.federalreserve.gov/publications/files/2026-final-supervisory-stress-test-scenarios-20260204.pdf#page=14){:target="_blank"}), while this package's is year over year. `stress_test_regime` uses the published values as they are: quarter-on-quarter inflation moves sooner and further than year over year, so the simulated inflation peaks earlier and higher than the scenario's own year-over-year path would. The shipped Fed Severely Adverse 2026 regime converts them, building the CPI level from the 2025 quarterly averages of [FRED's CPIAUCSL](https://fred.stlouisfed.org/series/CPIAUCSL){:target="_blank"}: 2.5% in the first quarter, 1.6% by the fourth and 1.1-1.3% after, against the Fed's 2.5% falling to 1.0%.
</div>

## Climate Scenarios

A climate pathway is an overlay rather than a regime. Enabled in a factor set, it shifts each interest rate, inflation, unemployment and equity factor by the deviation $$\delta_t$$ of a climate scenario of the Network for Greening the Financial System (NGFS), such as Net Zero 2050, Delayed Transition or Current Policies, from the NGFS baseline. The deviation is measured from the run's start, interpolated between the NGFS years and held after the last:

$$
x_t \leftarrow x_t + (\delta_t - \delta_0) \quad \text{for rates}, \qquad S_t \leftarrow S_t\,\frac{1 + \delta_t}{1 + \delta_0} \quad \text{for equities}
$$

Short rates follow the NGFS scenario's policy rate, long rates its long-term interest rate, and every equity one country's equity index, the United States by default. The shift is the same in every scenario, and the scenario's carbon price can be added as a factor. It combines with a regime: the climate pathway shifts the scenarios before the regime's targets select from them. There is no climate regime: an NGFS pathway through this overlay is the sourced way to run one.

## Example

The example uses the run from the [overview](/projects/financescenarios/docs#simulating-scenarios): the default settings and factor set, calibrated on 25 October 2026, with 2,000 scenarios and seed 42. The Federal Reserve's 2026 severely adverse scenario takes US unemployment to 10%, US stocks down almost 60%, house prices down 30% and the short rate to 0.1%. To run it next to the baseline and compare the medians after five years:

```python
from financescenarios import Scenarios, compare_runs

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
result = scenarios.simulate(n_simulations=2000, seed=42)

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
| united_states_unemployment | 0.0514 | 0.0753 |
| us_broad | 0.0870 | -0.0040 |
| united_states_short_rate | 0.0436 | 0.0153 |
| united_states_long_rate | 0.0567 | 0.0282 |

On the published dates every scenario is on the regulator's path: unemployment at 7.2% after six months, 9.0% after one year and 9.8% after two, the short rate at 2.5% after the first quarter and at 0.1% from six months to three and a quarter years, and the 10-year rate at 3.1% after the first quarter and between 2.3% and 2.7% after that. Stocks fall 57% in the median scenario over the first three quarters, 100 becoming 43.4, and recover from there, to 98.0 after five years, a return of -0.40% a year; the run's other markets follow through their correlations, European stocks to 43.9. Between the published dates the median walks in a straight line, and after the last one the short rate converges onto its usual path over five years, so it is still low after five, at a median of 1.53%. When plotted, US stocks as the value of 100:

{% include ft-chart.html id="regimes-fed" src="/assets/data/financescenarios-guides/regimes.json" label="Median and 5-95% band of US unemployment, the value of 100 in US stocks and the US short and 10-year rates in the baseline and under the Fed's 2026 severely adverse scenario over five years" %}

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">2</span></summary>

- Board of Governors of the Federal Reserve System (2026). "2026 Final Supervisory Stress Test Scenarios." [federalreserve.gov](https://www.federalreserve.gov/publications/files/2026-final-supervisory-stress-test-scenarios-20260204.pdf){:target="_blank"}
- European Banking Authority (2025). EBA launches its 2025 EU-wide stress test. [eba.europa.eu](https://www.eba.europa.eu/publications-and-media/press-releases/eba-launches-its-2025-eu-wide-stress-test){:target="_blank"}

</details>

{% include ft-charts-script.html %}
