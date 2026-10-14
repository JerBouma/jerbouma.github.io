---
title: How a Run Is Built
seo_title: How a Run Is Built – Finance Scenarios
excerpt: "How a scenario set is built: history for every factor, a calibration per factor, the dependence between them through the economic cascade and a correlation matrix, a correlated simulation, and the outputs."
description: "How Finance Scenarios builds a scenario set: data, calibration of each factor, correlations and the economic cascade, correlated simulation and outputs."
author_profile: false
permalink: /projects/financescenarios/docs/architecture
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

{% include mermaid.html %}

Where does each number in a run come from? A scenario set is built in five steps: collect history, calibrate each factor on its own, estimate how the factors depend on each other, simulate them jointly, and read the result. Each step can be inspected or overridden, so every number can be traced back to its source.

{% raw %}
<div class="mermaid">
flowchart TD
    data["<b>1. Data</b><small>history per factor</small>"] --> calibration["<b>2. Calibration</b><small>one model per factor</small>"]
    beliefs["<b>Your beliefs</b><small>long-run levels, anchors</small>"] -.-> calibration
    calibration --> dependence["<b>3. Dependence</b><small>cascade and correlations</small>"]
    dependence --> simulation["<b>4. Correlated simulation</b><small>thousands of scenarios</small>"]
    simulation --> outputs["<b>5. Outputs</b><small>fan charts, portfolios, SCR</small>"]
    class simulation accent
</div>
{% endraw %}

## 1. Data

Every factor is fitted on its own history, fetched through the [Finance Toolkit](https://github.com/JerBouma/FinanceToolkit): OECD and Global Macro Database series and market yields for rates, inflation and unemployment, market prices for equities, currencies and commodities, ICE BofA and Moody's indices for credit. Each series keeps its natural frequency (monthly, quarterly or yearly).

How much history to use is a modeling choice: the default factor set fits rate dynamics on OECD data since 1950, and some factors can go back to the 1870s or further ([long history](/projects/financescenarios/docs/configuration#long-history)).

## 2. Calibration

Each factor gets a model suited to how it behaves, and that model's parameters are estimated from its history:

- **Mean-reverting factors** (rates, inflation, spreads, unemployment, house prices) are fitted as an Ornstein-Uhlenbeck process: a regression of each value on an earlier one gives the long-run level, the speed of reversion and the volatility. For inflation and house-price growth, year-over-year rates whose neighbouring readings share most of their months, the earlier value is the one a year before, so the overlap does not pass for slow reversion.
- **Equities** are fitted as a regime-switching lognormal model ([Hardy, 2001](https://doi.org/10.1080/10920277.2001.10595984){:target="_blank"}): a calm and a crisis regime, each with its own return and volatility, and the probabilities of switching between them.
- **Other factors** follow their own published models (Nelson-Siegel for the curve, Schwartz for commodities, Cairns-Blake-Dowd for mortality); the [guides](/projects/financescenarios/docs) cover each.

A fit is only as good as its data, so the fitted values are a starting point, not a verdict. Your own views override them where you set them: a central bank's inflation target as the long-run level, or EIOPA's risk-free curve as the anchor for long-run rates (as in the default factor set). A factor whose fit fails, for example because a short window shows no mean reversion, is left out together with every factor that depends on it, and the run reports why.

## 3. Dependence {#dependence}

Fitted one by one, the factors would move independently, and a scenario could combine an equity crash with tightening credit spreads. Two mechanisms link them, following [Wilkie (1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf) and [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf).

**The economic cascade.** Where economic theory says one variable drives another, the driver's simulated path enters the other's equation directly:

- Unemployment responds to changes in its paired inflation rate, as in the Phillips-curve term of Ahlgrim, D'Arcy and Gorvett.
- In the Wilkie and KNW models, interest rates follow inflation.
- Under interest-rate parity, an exchange rate drifts with the rate gap between its two currencies.
- Wilkie-style dividend growth follows inflation, and equity prices can be derived from dividends.
- With business-cycle conditioning, the leading indicator drives inflation, rates, spreads and the chance of an equity crisis.

**The correlation matrix.** Everything else is linked through the correlation of the factors' random shocks, estimated from the same historical changes each factor was fitted on (changes in a rate, log returns of a price). Each pair uses the dates those two factors share, so a short series only weakens its own correlations. Because sample correlations between dozens of factors are noisy, they are shrunk toward zero by an amount chosen from the data ([Schäfer and Strimmer, 2005](https://doi.org/10.2202/1544-6115.1175)) and then repaired into a valid correlation matrix ([Higham, 2002](https://doi.org/10.1093/imanum/22.3.329){:target="_blank"}); [simulation engine](/projects/financescenarios/docs/simulation-engine#how-the-correlations-are-estimated) has the details.

Factors with no theoretical driver, such as the yield-curve factors, real estate, commodities and mortality, are linked only through correlations. That follows their source papers: Diebold and Li specify the curve factors as their own system, Ahlgrim, D'Arcy and Gorvett found real estate's dependence on inflation not significant, and Cairns, Blake and Dowd model mortality improvement independently of markets.

The matrix is constant over the horizon and captures linear co-movement. Two additions address the tails: equity markets can share their crisis regime, so they enter and leave crises together, and Student-t shocks make extreme moves coincide more often than a normal distribution allows ([fat tails](/projects/financescenarios/docs/simulation-engine#fat-tails-and-tail-dependence)).

## 4. Correlated Simulation

The correlated shocks for the whole horizon are drawn first. Then the run moves forward one step at a time, and within each step the factors are updated in a fixed order: a driver always before the factors that react to it, so they read its value for that same month. Inflation comes first, preceded only by the leading indicator when business-cycle conditioning is on. The diagram shows the order of the default factor set; a step a factor set does not use is skipped.

{% raw %}
<div class="mermaid">
flowchart TD
    shocks["<b>Correlated shocks for this month</b><small>one per factor, drawn jointly</small>"] --> indicator
    indicator["<b>0. Leading indicator</b><small>only with business-cycle conditioning</small>"] --> inflation
    inflation["<b>1. Inflation</b><small>the cascade starts here</small>"] --> rates
    rates["<b>2. Interest rates</b><small>Wilkie and KNW rates read inflation</small>"] --> unemployment
    unemployment["<b>3. Unemployment</b><small>reads inflation: Phillips curve</small>"] --> dividends
    dividends["<b>4. Dividends, Wilkie-style</b><small>read inflation</small>"] --> equities
    equities["<b>5. Equities</b><small>Wilkie share prices read dividends</small>"] --> fx
    fx["<b>6. Exchange rates</b><small>interest-rate parity reads both rates</small>"] --> rest
    rest["<b>7. Linked by the shocks only</b><small>commodities, yield curve, credit,<br/>real estate, mortality</small>"] --> next
    next["<b>Next month</b>"] -.-> shocks
    class inflation accent
</div>
{% endraw %}

The order guarantees that a driver is known before anything that needs it; it does not mean each step reads the one above it. Where the box names a link, the factor's equation reads that driver's value for the month. Elsewhere, for most rate and equity models, the link to inflation runs through the correlated shocks. With business-cycle conditioning, the leading indicator also drives rates, spreads and the chance of an equity crisis. One exception reverses the first two steps: an inflation factor set to follow its interest rate is stepped after that rate. The [simulation engine](/projects/financescenarios/docs/simulation-engine) covers the maths of each step.

## 5. Outputs

The result is a scenario set: every factor's paths, reported in one consistent unit (rates as annualized decimals, prices as annualized returns since the start; see [units](/projects/financescenarios/docs/units)). From there:

- [Regimes](/projects/financescenarios/docs/regimes) keep the scenarios that tell a stress story, such as stagflation.
- [Portfolio](/projects/financescenarios/docs/portfolio) turns the paths into the value of an investment mix with cashflows and rebalancing.
- [Solvency](/projects/financescenarios/docs/solvency) values liabilities on a risk-neutral run and computes the SCR.
- Prices are converted into one reporting currency after the simulation, without touching the calibration or correlations.

A real-world calibration can be saved and replayed, so the same fitted model can be simulated again with more scenarios or another seed, without downloading or fitting anything.

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(settings="default", factor_set="us_only")

calibration = scenarios.calibrate()            # steps 1-3: data, fit, dependence
calibration.save("calibration.json")          # replay later without downloading

result = scenarios.simulate(calibration=calibration, n_simulations=10_000)   # step 4
result.describe()                                                            # step 5
```
