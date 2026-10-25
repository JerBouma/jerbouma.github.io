---
title: Simulation Engine
seo_title: "Simulation Engine | Finance Scenarios"
seo_title_suffix: false
excerpt: "How Finance Scenarios steps a run forward: exact Ornstein-Uhlenbeck and lognormal transitions, price indices that compound with ln(1 + inflation), Andersen's QE scheme for Heston, Euler steps, Monte Carlo error and the numerical settings."
description: "The simulation engine of Finance Scenarios: time stepping, exact transitions, the rate a step reads, Heston's QE scheme, full-truncation Euler, Monte Carlo error and antithetic variates, numerical and optimiser settings."
author_profile: false
permalink: /projects/financescenarios/docs/simulation-engine
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/architecture
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-architecture"
---

How is a run stepped forward, and how far can you trust a percentile read from it? Once the correlated shocks are drawn ([Dependence](/projects/financescenarios/docs/dependence)), the engine steps every factor forward one period at a time; each path through the horizon is one scenario, and thousands of them form a distribution of outcomes. Each model has its own page; this page covers what they share: the step schemes, the Monte Carlo error and the numerical settings behind them.

## Time Stepping {#time-stepping}

The horizon is cut into steps of equal length $$\Delta t$$, from daily to yearly. The default settings profile uses:

<div class="ca-nums fs-nums">
  <span><b>2,000</b>scenarios</span>
  <span><b>Monthly</b>steps</span>
  <span><b>5 years</b>horizon</span>
</div>

Factors are stepped in cascade order, so a driver such as inflation is known before the factors that react to it. Each factor is stepped one of these ways:

| Factors | Step |
|:--------|:-----|
| Mean-reverting: rates under Hull-White, inflation, spreads, log commodity prices, log dividend yields | The exact solution of the Ornstein-Uhlenbeck process |
| Prices: equities, currencies | Exact, in log space |
| Growth rates: inflation, house prices | Stepped as a rate; their index compounds by $$\ln(1 + \pi)$$ |
| Heston equities (risk-neutral) | Andersen's quadratic-exponential scheme with its martingale correction |
| CIR rates and factors with GARCH volatility | An Euler step, so a shorter step is more accurate |

For mean-reverting factors the exact Ornstein-Uhlenbeck step is:

$$
x_{t+\Delta t} = \theta + (x_t - \theta)\, e^{-a \Delta t} + \sigma \sqrt{\frac{1 - e^{-2 a \Delta t}}{2a}}\; \varepsilon_t
$$

where $$\theta$$ is the long-run level, $$a$$ the speed of mean reversion, $$\sigma$$ the volatility and $$\varepsilon_t$$ the correlated shock. Each step closes a share $$1 - e^{-a\Delta t}$$ of the gap to $$\theta$$, and the long-run standard deviation settles at $$\sigma/\sqrt{2a}$$. Because the transition is exact, the step length adds no error: for a stand-alone factor, a yearly step gives the same year-end distribution as twelve monthly ones. The step does matter for factors that react to another factor's path, and with regime switches or Student-t shocks. A rate stepped this way is Gaussian and can go negative; a factor modeled in logs stays positive.

Prices (equities, currencies) are stepped exactly in log space, so they stay positive and their returns are lognormal:

$$
S_{t+\Delta t} = S_t \exp\!\left(m\,\Delta t + \sigma\sqrt{\Delta t}\,\varepsilon_t\right)
$$

where $$m$$ is the expected log return per year and $$\sigma$$ the volatility. For an equity, $$m$$ and $$\sigma$$ are those of the regime it is in over the step, with the short rate at the start of the step added to $$m$$; for a currency $$m$$ is its drift less $$\tfrac{1}{2}\sigma^2$$, where the drift is the historical or random-walk drift, the rate gap under interest-rate parity, or the inflation gap plus the real rate's pull under purchasing power parity ([Currencies](/projects/financescenarios/docs/markets/currencies)).

### Price Indices Compound with ln(1 + π) {#price-indices}

Inflation and house-price growth are year-over-year rates: the growth of an index over the past year. The index they build compounds continuously at $$\ln(1 + \pi_t)$$, the log growth that rate implies, as [Ahlgrim, D'Arcy and Gorvett (2005, section 3, eq. 3.7)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"} and [Wilkie (1986)](https://doi.org/10.1017/S0071368600009009){:target="_blank"} model it:

$$
P_{t+\Delta t} = P_t \exp\!\big(\ln(1 + \pi_t)\,\Delta t\big)
$$

so inflation held at 4% gives $$1.04^T$$, the index a year-over-year rate of 4% describes. Compounding the rate itself, $$\exp(\sum \pi_t \Delta t)$$, treats a simple rate as a continuously compounded one and overstates the index: by about 1.3% over 30 years at 3% inflation. The same log growth drives every factor that reads a price index: the price gap behind purchasing power parity for currencies, gold's real drift and house prices. The fits read the same simple year-over-year rates the simulation produces, so fit and simulation agree.

Market-implied (risk-neutral) inflation steps the force of inflation, $$x_t = \ln(1 + \pi_t)$$, around the breakeven curve with the exact Ornstein-Uhlenbeck transition, so the expected index stays on the market's breakeven curve at every maturity, exactly in the limit of a small step: the convexity term is the continuous-time one, and the index sums the rate at the start of each step.

### Which Rate a Step Reads {#rate-timing}

A factor that earns a rate over a step reads the rate at the start of that step, the rate known when the step begins. Stocks, which earn the short rate plus a premium, and the real-world exchange-rate step under interest-rate parity read the short rate this way. So do discounting (a discount factor sums the rate at the start of each step) and the risk-neutral equity and exchange-rate steps. Reading the end-of-step rate instead would let a stock earn a rate that was not yet known when its step began.

### Heston's Variance: Andersen's QE Scheme {#heston-qe}

A risk-neutral equity under Heston's stochastic volatility is stepped with the quadratic-exponential (QE) scheme of [Andersen (2008, section 3.2)](https://doi.org/10.21314/jcf.2008.189){:target="_blank"} with its martingale correction ([van Haastrecht and Pelsser, 2010, section 4.2, eq. 61](https://doi.org/10.1142/S0219024910005668){:target="_blank"}). A variance fitted to an option surface often reverts to its long-run level within a step or two at a monthly step, and an Euler step with full truncation then gets it badly wrong. QE draws the next variance from a distribution with the exact conditional mean and variance, moves the log price with the variance integrated over the step by the trapezoid rule, and the correction keeps the expected discounted price at its starting value over each step (a martingale). [Equities](/projects/financescenarios/docs/markets#heston-paths-at-a-monthly-step) sets both schemes against Heston's closed-form call prices on a fit to SPY's options.

The KNW model with stochastic volatility steps its variance with the same scheme, without the correction.

### Euler Steps

CIR rates and factors with GARCH volatility use an Euler step instead, which applies the drift and volatility at the start of a step to the whole step. A CIR rate is more accurate on a shorter step; a GARCH factor must step at the frequency it was fitted at. CIR uses the full-truncation scheme of [Lord, Koekkoek and van Dijk (2010)](https://doi.org/10.1080/14697680802392496){:target="_blank"}: drift and volatility are computed from the rate floored at zero, but the rate itself is not floored, so a path can dip slightly below zero, which the exact CIR process never does.

## Monte Carlo Error {#monte-carlo-error}

A run of $$n$$ scenarios estimates a distribution with sampling error. For a mean, the standard error is

$$
\text{se} = \frac{s}{\sqrt{n}}
$$

with $$s$$ the standard deviation across scenarios. Halving the error takes four times as many scenarios. Tail percentiles are less precise still, because they rest on few scenarios: the 1st percentile of 1,000 scenarios is set by about ten of them.

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">A practical check</p>

Rerun with several seeds and see how much the number you report moves.
</div>

**Antithetic variates** reduce that error without more random draws. Every shock $$Z$$ is paired with its mirror image $$-Z$$ (under Student-t, a large common scale is also paired with a small one), so each pair's errors partly cancel; the standard error is then computed from the independent pair averages. On the default factor set they cut the seed-to-seed spread of a 60/40 portfolio's five-year 5th percentile by about a quarter. They are off in the shipped settings and need an even number of scenarios.

To read the standard error and rerun with other seeds:

```python
result = scenarios.simulate(n_simulations=2000)
result.summary_statistics("united_states_short_rate")   # mean, std, se and percentiles per date

calibration = scenarios.calibrate()                      # fit once, then vary only the seed
reruns = [scenarios.simulate(calibration=calibration, seed=seed) for seed in range(5)]
```

## Numerical Settings

The settings of the run itself, and the reason for each:

| Setting | Default | Kind | Why |
|:--|:--|:--|:--|
| Scenarios | 2,000 | Sourced minimum, judgement above it | The NAIC Valuation Manual's VM-21, Section 8.F, notes that straight Monte Carlo typically uses at least 1,000 scenarios, as cited in the [NAIC GOES Subgroup's SERT exposure (16 October 2024)](https://content.naic.org/sites/default/files/inline-files/GOES%20SG%20SERT%20Scenario,%20DR,%20and%20Scenario%20Statistics%20Exposure%20101624%20(1).pdf){:target="_blank"}. 2,000 keeps 100 paths in a 5% tail; NAIC's own set has 10,000 and DNB's 20,000 |
| Step | One month | Setting | Most of the data are monthly, and the regimes are fitted month by month |
| Horizon | 60 steps (five years) | Judgement | A business-planning horizon; the horizon setting changes it |
| Seed | 42 | Setting | Any fixed seed makes a run reproducible; each regime chain draws from its own stream, offset from the seed |
| Start date | 2026-01-01 | Setting | A fixed, reproducible jump-off date |
| Calibration window | Since 2000 | Judgement | Two full bear markets (2000-02 and 2008-09); longer records are read where a factor needs them, such as the term premium on OECD rates since 1950 |
| Shock distribution | Normal | Setting | Student-t shocks are an option ([Dependence](/projects/financescenarios/docs/dependence#fat-tails-and-tail-dependence)) |
| Antithetic variates | Off | Setting | An option (above) |

## Optimiser Settings

The fits use iterative optimisers. Their limits and starting points change how fast a fit converges, not what it converges to; where a likelihood has several maxima, the fit starts from several points and keeps the best. Each fit's method, limits and starting points:

| Fit | Method | Limits | Start |
|:--|:--|:--|:--|
| Equity regimes | Baum-Welch ([Baum, Petrie, Soules and Weiss, 1970](https://doi.org/10.1214/aoms/1177697196){:target="_blank"}) | 2,000 iterations, tolerance $$10^{-6}$$; volatility floor $$10^{-6}$$ | Each regime on one quantile slice of the sorted returns, equal switching |
| Inflation-driven and business-cycle switching | Expectation-maximisation, regimes and switching fitted jointly ([Diebold, Lee and Weinbach, 1994](https://doi.org/10.1093/oso/9780198773917.003.0010){:target="_blank"}) | 500 iterations (the post-war fit converges in about 100), tolerance $$10^{-6}$$; a ridge penalty of 0.01 on the logit | The plain expectation-maximisation fit; a 90% chance of staying put when the regimes' means and volatilities are held fixed |
| Inflation regimes | Maximum likelihood, Powell's method | 4,000 evaluations; tolerances $$10^{-6}$$ (parameters) and $$10^{-9}$$ (likelihood) | Three starts (the high regime's level, the shock sizes and the stay chances), scaled to a one-regime fit |
| Unemployment regimes | Maximum likelihood, L-BFGS-B | 2,000 iterations | Three splits of the months (by the residual's sign, its size, short recessions), two more with the equity link |
| Inflation's long-run median (a diagnostic; the anchor sets the mean, in closed form) | Stationary vector of a (bin, regime) chain | Bins an eighth of a month's shock wide, six long-run spreads either side, at most 2,000 bins; the median interpolated inside the bin where the distribution crosses one half | Finer bins move the US median by 0.2 basis points |

## Example {#scenarioset}

The example uses the run from the [overview](/projects/financescenarios/docs#simulating-scenarios): the default settings and factor set, calibrated on 25 October 2026, with 2,000 scenarios and seed 42. A run holds every factor's paths, and filtering keeps whole scenarios, so a "high inflation, weak stocks" subset still has consistent rates, unemployment and currencies. To keep the 20% of scenarios with the highest US inflation, then the 20% of those with the weakest US stocks, and compare the medians after five years:

```python
from financescenarios import Scenarios, compare_runs

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
result = scenarios.simulate(n_simulations=2000, seed=42)

stagflation = result.filter_narrative({"united_states_inflation": (0.8, 1.0), "us_broad": (0.0, 0.2)})

compare_runs(
    {"baseline": result, "stagflation": stagflation},
    statistic="terminal_median",
    factors=["united_states_inflation", "us_broad", "united_states_short_rate", "united_states_unemployment", "gold"],
)
```

Which returns:

| factor | baseline | stagflation |
|:-------|---------:|------------:|
| united_states_inflation | 0.0181 | 0.0411 |
| us_broad | 0.0870 | -0.0420 |
| united_states_short_rate | 0.0436 | 0.0626 |
| united_states_unemployment | 0.0514 | 0.0700 |
| gold | 0.0270 | 0.0328 |

The 80 scenarios kept, 4% of the run, end with inflation of 4.11% and stocks losing 4.20% a year in the median, and the factors no filter named come along on the same paths: the policy rule set the short rate higher, at 6.26%, unemployment rose to 7.00%, and gold, which follows inflation, returned 3.28% a year against 2.70%. [Regimes](/projects/financescenarios/docs/regimes) builds such stories into named, reusable runs.

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">8</span></summary>

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. [casact.org](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}
- Andersen, L. (2008). [Simple and Efficient Simulation of the Heston Stochastic Volatility Model](https://doi.org/10.21314/jcf.2008.189){:target="_blank"}. Journal of Computational Finance, 11(3), 1-42.
- Baum, L.E., Petrie, T., Soules, G., Weiss, N. (1970). "A Maximization Technique Occurring in the Statistical Analysis of Probabilistic Functions of Markov Chains." The Annals of Mathematical Statistics, 41(1), 164-171. [doi.org](https://doi.org/10.1214/aoms/1177697196){:target="_blank"}
- Diebold, F.X., Lee, J.-H., Weinbach, G.C. (1994). "Regime Switching with Time-Varying Transition Probabilities." In Hargreaves, C. (ed.), Nonstationary Time Series Analysis and Cointegration, 283-302. [doi.org](https://doi.org/10.1093/oso/9780198773917.003.0010){:target="_blank"}
- Lord, R., Koekkoek, R., van Dijk, D. (2010). "A Comparison of Biased Simulation Schemes for Stochastic Volatility Models." Quantitative Finance, 10(2), 177-194. [doi.org](https://doi.org/10.1080/14697680802392496){:target="_blank"}
- NAIC GOES Subgroup (2024). SERT Scenario, DR and Scenario Statistics Exposure, 16 October 2024. [content.naic.org](https://content.naic.org/sites/default/files/inline-files/GOES%20SG%20SERT%20Scenario,%20DR,%20and%20Scenario%20Statistics%20Exposure%20101624%20(1).pdf){:target="_blank"}
- van Haastrecht, A., Pelsser, A. (2010). "Efficient, Almost Exact Simulation of the Heston Stochastic Volatility Model." International Journal of Theoretical and Applied Finance, 13(1), 1-43. [doi.org](https://doi.org/10.1142/S0219024910005668){:target="_blank"}
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. [doi.org](https://doi.org/10.1017/S0071368600009009){:target="_blank"}

</details>
