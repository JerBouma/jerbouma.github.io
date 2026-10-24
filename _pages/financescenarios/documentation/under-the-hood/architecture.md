---
title: How a Run Is Built
seo_title: "How a Run Is Built | Finance Scenarios"
seo_title_suffix: false
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
    nav: "financescenarios-docs-architecture"
---

Where does each number in a run come from? A scenario set is built in five steps: collect history, calibrate each factor on its own, estimate how the factors depend on each other, simulate them jointly, and read the result. Each step can be inspected or overridden, so every number can be traced back to its source.

<div class="fs-diagram">
<div class="fs-flow__side"><div class="fs-node"><b>Your beliefs</b><small>long-run levels, anchors</small></div><span>override the fit at step 2</span></div>
<ol class="fs-flow">
  <li class="fs-node"><b><a href="#data">Data</a></b><small>history per factor</small></li>
  <li class="fs-node"><b><a href="#calibration">Calibration</a></b><small>one model per factor</small></li>
  <li class="fs-node"><b><a href="#dependence">Dependence</a></b><small>cascade and correlations</small></li>
  <li class="fs-node is-accent"><b><a href="#correlated-simulation">Correlated simulation</a></b><small>thousands of scenarios</small></li>
  <li class="fs-node"><b><a href="#outputs">Outputs</a></b><small>fan charts, portfolios, SCR</small></li>
</ol>
</div>

## 1. Data {#data}

Every factor is fitted on its own history, fetched through the [Finance Toolkit](https://github.com/JerBouma/FinanceToolkit){:target="_blank"}. Each series keeps its natural frequency (monthly, quarterly or yearly):

| Factors | History |
|:--------|:--------|
| Rates, inflation and unemployment | OECD and Global Macro Database series and market yields |
| Equities, currencies and commodities | Market prices |
| Credit | ICE BofA and Moody's indices |

How much history to use is a modeling choice: the default factor set fits its long rates' term premium on OECD data since 1950, and some factors can go back to the 1870s or further ([long history](/projects/financescenarios/docs/configuration#long-history)).

## 2. Calibration {#calibration}

Each factor gets a model suited to how it behaves, and that model's parameters are estimated from its history:

| Factors | Model | What the fit gives |
|:--------|:------|:-------------------|
| **Rates** | A central bank's policy rule for short rates; the expected short-rate path plus a mean-reverting term premium for long rates | The rule's weights, targets and floors come from the central banks; the fit gives the rule's volatility and the term premium's level, speed and volatility. |
| **Inflation and unemployment** | Mean reversion with two regimes: calm and high inflation, expansions and recessions | Maximum likelihood through Hamilton's filter gives each regime's level and volatility, the persistence and the chances of switching. |
| **Other mean-reverting factors**: credit spreads, house prices, dividend yields, the business cycle | Ornstein-Uhlenbeck process | A regression of each value on an earlier one gives the long-run level, the speed of reversion and the volatility. |
| **Equities** | Regime-switching lognormal model ([Hardy, 2001](https://doi.org/10.1080/10920277.2001.10595984){:target="_blank"}) | A calm and a crisis regime, each with its own return and volatility, and the probabilities of switching between them. |
| **Other factors** | Their own published models: Nelson-Siegel for the curve, Schwartz for commodities, Cairns-Blake-Dowd for mortality | Each has its own page, listed in the [overview](/projects/financescenarios/docs). |

Among the mean-reverting factors, inflation and house-price growth are year-over-year rates whose neighboring readings share most of their months. For them the earlier value is the one a year before, so the overlap is not mistaken for slow mean reversion.

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">A starting point, not a verdict</p>

A fit is only as good as its data. Your own views override the fitted values where you set them: a central bank's inflation target as the long-run level, or EIOPA's risk-free curve as the anchor for a rate's long-run level ([Beliefs](/projects/financescenarios/docs/configuration/beliefs)).
</div>

A factor whose fit fails, for example because a short window shows no mean reversion, is left out together with every factor that depends on it, and the run reports why.

## 3. Dependence {#dependence}

Fitted one by one, the factors would move independently, and a scenario could combine an equity crash with tightening credit spreads. Two mechanisms link them, following [Wilkie (1986)](https://doi.org/10.1017/S0071368600009009){:target="_blank"} and [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}.

**The economic cascade.** Where economic theory says one variable drives another, the driver's simulated path enters the other's equation directly. The default factor set uses the first eight links; the rest are options:

| Driver | Follower | Link |
|:-------|:---------|:-----|
| Inflation and unemployment | Short rates | The policy rule ([Short Rate](/projects/financescenarios/docs/interest-rates)) |
| The short rate | Long rates | The expected path plus a term premium ([Long Rate](/projects/financescenarios/docs/interest-rates/long-rate)) |
| The short rate and inflation | Equities | The short rate plus a premium, with turbulence likelier when inflation is high ([Equities](/projects/financescenarios/docs/markets)) |
| Equities | US unemployment | A recession likelier after a stock-market fall ([Unemployment](/projects/financescenarios/docs/economy/unemployment)) |
| Changes in inflation | Unemployment | The Phillips-curve term of Ahlgrim, D'Arcy and Gorvett |
| The long rate a year earlier | House-price growth | Higher rates slow house prices ([Real Estate](/projects/financescenarios/docs/markets/real-estate)) |
| The two inflation rates | The euro and the pound | Purchasing power parity ([Currencies](/projects/financescenarios/docs/markets/currencies)) |
| Inflation | Gold | A random walk in real terms ([Commodities](/projects/financescenarios/docs/markets/commodities)) |
| Inflation | Interest rates | Wilkie's consols yield and the KNW models |
| The rate gap between two currencies | Their exchange rate | Interest-rate parity |
| Inflation | Dividend growth, and share prices derived from dividends | Wilkie's cascade ([Dividends](/projects/financescenarios/docs/markets/dividends)) |
| The leading indicator | Inflation, rates, spreads, commodities, dividend yields, unemployment and the chance of an equity crisis | Business-cycle conditioning ([Business Cycle](/projects/financescenarios/docs/economy/business-cycle)) |

**The correlation matrix.** Everything else is linked through the correlation of the factors' random shocks, estimated from each factor's historical changes: changes in a rate, log returns of a price, and step-to-step changes for year-over-year rates and credit spreads, whatever form the factor is fitted in. Each pair uses the dates those two factors share, so a short series only weakens its own correlations. Because sample correlations between dozens of factors are noisy, they are shrunk toward zero by an amount chosen from the data ([Schäfer and Strimmer, 2005](https://doi.org/10.2202/1544-6115.1175){:target="_blank"}) and then repaired into a valid correlation matrix ([Higham, 2002](https://doi.org/10.1093/imanum/22.3.329){:target="_blank"}); [Dependence](/projects/financescenarios/docs/dependence) has the details.

Factors with no theoretical driver, such as the yield-curve factors, oil, credit spreads and mortality, are linked only through correlations. That follows their source papers: [Diebold and Li (2006)](https://doi.org/10.1016/j.jeconom.2005.03.005){:target="_blank"} specify the curve factors as their own system, and [Cairns, Blake and Dowd (2006)](https://doi.org/10.1111/j.1539-6975.2006.00195.x){:target="_blank"} model mortality improvement independently of markets.

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">The tails</p>

The matrix is constant over the horizon and captures linear co-movement. Two additions address the tails: equity markets can share their crisis regime, so they enter and leave crises together, and Student-t shocks make extreme moves coincide more often than a normal distribution allows ([fat tails](/projects/financescenarios/docs/dependence#fat-tails-and-tail-dependence)).
</div>

## 4. Correlated Simulation {#correlated-simulation}

The correlated shocks for the whole horizon are drawn first. Then the run moves forward one step at a time, and within each step the factors are updated in a fixed order: a driver always before the factors that react to it, so they read its value for that same month. Inflation comes first, preceded only by the leading indicator when business-cycle conditioning is on. The order in the default factor set (a factor set skips any step it does not use):

<div class="fs-diagram">
<ol class="fs-flow fs-flow--vertical fs-flow--plain fs-flow--compact">
  <li class="fs-node"><b>Correlated shocks for this month</b><small>one per factor, drawn jointly</small></li>
  <li class="fs-node"><b>0. Leading indicator</b><small>only with business-cycle conditioning</small></li>
  <li class="fs-node is-accent"><b>1. Inflation</b><small>the cascade starts here</small></li>
  <li class="fs-node"><b>2. Interest rates</b><small>the policy rule reads inflation and unemployment; long rates read the short rate</small></li>
  <li class="fs-node"><b>3. Unemployment</b><small>reads inflation and past equity returns</small></li>
  <li class="fs-node"><b>4. Dividends, Wilkie-style</b><small>read inflation</small></li>
  <li class="fs-node"><b>5. Equities</b><small>earn the short rate; switching reads inflation</small></li>
  <li class="fs-node"><b>6. Exchange rates</b><small>purchasing power parity reads both inflation rates</small></li>
  <li class="fs-node"><b>7. The rest</b><small>commodities, yield curve, credit, real estate, mortality</small></li>
</ol>
<p class="fs-diagram__note">Then the next month, starting again from its shocks.</p>
</div>

The order guarantees that a driver is known before anything that needs it; it does not mean each step reads the one above it. Where a box names a link, the factor's equation reads that driver's value for the month. A rule or a link that reads another factor's value at the start of the step, as the policy rule and house prices do, reads the step before. A factor with no link in its equation is tied to the rest through the correlated shocks only. With business-cycle conditioning, the leading indicator also drives rates, spreads and the chance of an equity crisis. The [simulation engine](/projects/financescenarios/docs/simulation-engine) covers the mathematics of each step.

<div class="fs-callout" markdown="1">
One exception reverses the first two steps: an inflation entry configured to follow its interest rate is stepped after that rate.
</div>

## 5. Outputs {#outputs}

The result is a scenario set: every factor's paths, reported in one consistent unit (rates as annualized decimals, prices as annualized returns since the start; see [units](/projects/financescenarios/docs/units)). From there:

<div class="ca-cards ca-cards--3">
  <div><i class="ca-icon fas fa-shuffle" aria-hidden="true"></i><p class="ca-card-title">Regimes</p><p><a href="/projects/financescenarios/docs/regimes">Regimes</a> keep the scenarios that tell a stress story, such as stagflation.</p></div>
  <div><i class="ca-icon fas fa-chart-pie" aria-hidden="true"></i><p class="ca-card-title">Portfolio</p><p><a href="/projects/financescenarios/docs/portfolio">Portfolio</a> turns the paths into the value of an investment mix with cashflows and rebalancing.</p></div>
  <div><i class="ca-icon fas fa-shield-halved" aria-hidden="true"></i><p class="ca-card-title">Solvency</p><p><a href="/projects/financescenarios/docs/solvency">Solvency</a> values liabilities on a risk-neutral run and computes the SCR.</p></div>
</div>

Prices can be converted into one reporting currency after the simulation, without touching the calibration or the correlations.

A real-world calibration can be saved and replayed, so the same fitted model can be simulated again with more scenarios or another seed, without downloading or fitting anything. The five steps in code:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(settings="default", factor_set="default")

calibration = scenarios.calibrate()            # steps 1-3: data, fit, dependence
calibration.save("calibration.json")          # replay later without downloading

result = scenarios.simulate(calibration=calibration, n_simulations=10_000)   # step 4
result.describe()                                                            # step 5
```

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">7</span></summary>

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. [casact.org](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}
- Cairns, A.J.G., Blake, D., Dowd, K. (2006). "A Two-Factor Model for Stochastic Mortality with Parameter Uncertainty: Theory and Calibration." Journal of Risk and Insurance, 73(4), 687-718. [doi.org](https://doi.org/10.1111/j.1539-6975.2006.00195.x){:target="_blank"}
- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. [doi.org](https://doi.org/10.1016/j.jeconom.2005.03.005){:target="_blank"}
- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. [doi.org](https://doi.org/10.1080/10920277.2001.10595984){:target="_blank"}
- Higham, N.J. (2002). "Computing the Nearest Correlation Matrix: A Problem from Finance." IMA Journal of Numerical Analysis, 22(3), 329-343. [doi.org](https://doi.org/10.1093/imanum/22.3.329){:target="_blank"}
- Schafer, J., Strimmer, K. (2005). "A Shrinkage Approach to Large-Scale Covariance Matrix Estimation and Implications for Functional Genomics." Statistical Applications in Genetics and Molecular Biology, 4(1). [doi.org](https://doi.org/10.2202/1544-6115.1175){:target="_blank"}
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. [doi.org](https://doi.org/10.1017/S0071368600009009){:target="_blank"}

</details>
