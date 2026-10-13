---
title: Inflation, Labor and Longevity
seo_title: Inflation, Labor and Longevity – Finance Scenarios
excerpt: "The economics behind the inflation, unemployment, business-cycle and mortality models in Finance Scenarios: what each assumes, how they link and where they stop."
description: "How Finance Scenarios models inflation, unemployment, the business cycle and longevity: the theory, the links between them, the papers and the limits."
author_profile: false
permalink: /projects/financescenarios/docs/economy
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Many liabilities are driven by the economy rather than by markets: pensions are indexed to prices, claims move with the labor market, and annuities run for as long as people live. This page covers inflation, unemployment, the business cycle and mortality.

Each factor is fitted to its own history and simulated with correlated shocks alongside everything else (see the [simulation engine](/projects/financescenarios/docs/simulation-engine)). Some are also linked directly, in one direction: inflation moves unemployment, and the business cycle moves inflation, rates, spreads and equity regimes. The data are official statistics (OECD, or the Global Macro Database outside it), with no API key.

## Inflation

Inflation sets the real value of every nominal cash flow, so it sits at the top of the model. Following [Wilkie (1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf){:target="_blank"} and [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}, inflation drives other variables, such as unemployment and, in Wilkie's setup, dividends, rather than the other way around.

The series is headline CPI inflation, year over year. Consecutive monthly readings share eleven of their twelve months, so the series is smooth, the convention most scenario generators calibrate on.

### Mean Reversion to a Target (the Default)

The default treats inflation as an Ornstein-Uhlenbeck process ([Uhlenbeck and Ornstein, 1930](https://doi.org/10.1103/PhysRev.36.823){:target="_blank"}):

$$
d\pi_t = a(\theta - \pi_t)\,dt + \sigma\,dW_t
$$

Here $$\pi_t$$ is inflation, $$\theta$$ the long-run level it settles around, $$a$$ the speed of the pull back, and $$\sigma$$ the size of the shocks. A shock halves in $$\ln 2 / a$$ years.

Central banks target a level, and deviations from it are temporary. Calibrated on US data from 2000 onward, inflation started at 3.40% and was pulled toward 2.66%, halving any gap in about 1.7 years. The shocks are normal and nothing floors the rate, so deflation can occur, as it has in history, and the tails are no fatter than a normal distribution's.

A view on the anchor, such as a credible 2% target, goes in as a belief:

```yaml
inflation:
  - name: us_inflation
    country: United States
    beliefs:
      long_run_mean: 0.02  # anchor at 2% instead of the fitted level
```

Two extensions address the main weaknesses of a constant-volatility fit on a recent window:

- **Volatility clustering.** A GARCH(1,1) volatility ([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1){:target="_blank"}) lets calm and turbulent spells persist, as in the 1970s against the 2010s.
- **Short samples.** Twenty-five calm years understate how far inflation can drift. The dynamics can instead be fitted on UK inflation from 1209 (the Bank of England's millennium dataset) or US inflation from 1872 (Shiller's data), starting from today's rate.

### Wilkie's AR(1)

Wilkie's original model is the discrete-time version of the same idea: each year keeps a fixed share $$a$$ of last year's gap to the mean $$\mu$$, plus a shock.

$$
I_t = \mu + a\,(I_{t-1} - \mu) + \sigma\,z_t
$$

On US monthly data, 97% of each month's gap carried into the next. The reason to choose it is the rest of Wilkie's cascade: dividend yield, dividend growth and the long-term (consols) yield all follow from the inflation path. The consols yield tracks a slow moving average of past inflation plus a real part (Wilkie's equations 3.12 and 3.13), so it needs a history in which long yields stay above inflation; the shipped `wilkie` settings fit on 1995-2007. The model runs only at the period it was fitted on.

### Hibbert's Two-Factor Model

In [Hibbert, Mowbray and Turnbull (2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"}, inflation reverts to a slower-moving "expected inflation" level rather than a fixed number, so the anchor itself drifts. That suits long horizons in which a shift in monetary policy is plausible.

The paper estimates expected inflation with a Kalman filter. Finance Scenarios uses an observable stand-in: the same country's yearly inflation, simulated as its own correlated factor, or an exponentially weighted average of the path. Hibbert's fixed cross-factor correlations and closed-form bond prices are not replicated, and on year-over-year data most of the movement ends up in the target. The yearly target needs a long history (the shipped settings start in 2000).

### Links to Interest Rates and the Business Cycle

Inflation can respond directly to a move in another variable over the same step, beyond what the correlation matrix captures:

- **Interest rates.** A term on the change in a paired short rate, so rate moves pass through to prices.
- **The business cycle.** A term on the change in the leading indicator (see below), so inflation picks up in booms and eases in slowdowns.

Both links run one way: the rate or the indicator moves inflation, not the reverse. If rates and inflation should drive each other, with the short rate and inflation fitted jointly as one system, use the [KNW model](/projects/financescenarios/docs/knw).

```yaml
inflation:
  - name: us_inflation
    country: United States
    condition_on_interest_rate: true
    interest_rate_name: short_rate  # an interest_rates entry
```

### Market-Implied Inflation (Risk-Neutral)

Everything above is real-world inflation. To value inflation-linked cash flows consistently with market prices you need the breakeven instead: the gap between a nominal and an inflation-protected government yield of the same maturity. It includes an inflation risk premium, so it is not a forecast.

Finance Scenarios fits a [Nelson-Siegel (1987)](https://doi.org/10.1086/296409){:target="_blank"} curve (level, slope and hump) to the latest breakevens, with the decay parameter fixed as in [Diebold and Li (2006)](https://doi.org/10.1016/j.jeconom.2005.03.005){:target="_blank"}. Every path then follows that curve's forward rates, with no randomness.

| Market | Source | Maturities | Index |
|:--|:--|:--|:--|
| United States | US Treasury, nominal minus TIPS | 5 to 30 years | US CPI |
| United Kingdom | Bank of England implied inflation curve | 3 to 40 years | RPI |
| Germany / euro area | Bundesbank, nominal minus inflation-linked | 5 to 15 years | Euro area HICP ex tobacco |

Nothing is quoted below five years (three in the UK), so the first years are extrapolated. The UK curve measures RPI, which has run above CPI.

```yaml
inflation:
  - name: uk_breakeven
    country: United Kingdom
    measure: risk_neutral
```

A whole-run risk-neutral simulation keeps inflation real-world, so benefits can still be indexed to it. For a stochastic risk-neutral inflation leg, use the KNW model with stochastic volatility.

### Limits

Only headline CPI is modeled, with no core or sector indices. The default data window is about five years, too short for a stable fit, so set an early `start_date`. Full reference: [Inflation](/projects/financescenarios/docs/reference/inflation).

## Unemployment

Unemployment drives wage-linked benefits, disability claims and credit losses. The model is the unemployment equation of [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}: unemployment reverts to a long-run rate, plus a term on the change in inflation over the same step.

$$
du_t = \kappa(\mu - u_t)\,dt + \alpha\,d\pi_t + \gamma\,dL_t + \sigma\,dW_t
$$

Here $$u_t$$ is the unemployment rate, $$\mu$$ its long-run level and $$\kappa$$ the speed of reversion. The $$\alpha$$ term is a Phillips curve ([Phillips, 1958](https://doi.org/10.1111/j.1468-0335.1958.tb00003.x){:target="_blank"}): when inflation rises, unemployment tends to fall, so $$\alpha$$ is expected to be negative. The optional $$\gamma$$ term links unemployment to the leading indicator $$L_t$$, in the spirit of Okun's law: when activity picks up, unemployment falls.

Both terms read the moves already simulated on the same path, so the variables stay consistent scenario by scenario.

Calibrated on US data from 2000 onward, unemployment started at 4.27% and was pulled toward 5.67% with a half-life of about 1.3 years. The fitted inflation sensitivity was -0.34: a one-point rise in inflation went with roughly a third of a point fall in unemployment, as the Phillips curve expects.

```yaml
unemployment:
  - name: us_unemployment
    country: United States
    inflation_name: us_inflation  # the paired inflation entry
    beliefs:
      long_run_mean: 0.045        # your view of the natural rate
```

### Limits

- **The Phillips sign is not forced.** The curve has been unstable since the 1970s, and fits reflect that: Brazil, on yearly data, came out slightly positive. Override `inflation_sensitivity` with a belief if that conflicts with your view.
- **Trends make poor anchors.** German unemployment fell steadily for fifteen years after 2000, and a quarterly fit gave almost no mean reversion and a negative long-run level. Set the level and speed yourself, or use a proxy country: the shipped `core` set uses France for the euro area.

Full reference: [Unemployment](/projects/financescenarios/docs/reference/unemployment).

## The Leading Indicator and the Business Cycle

The leading indicator gives the model an explicit business cycle, so other factors move with booms and slowdowns, not only through average correlations. It is the OECD Composite Leading Indicator, designed to turn ahead of the economy, published detrended around 100. Mean reversion holds largely by construction, so it uses the same Ornstein-Uhlenbeck process as default inflation. It covers about 22 countries and country groups.

```yaml
leading_indicator:
  enabled: true
  country: United States
```

### Conditioning on the Cycle

On its own the indicator is one more correlated factor. It earns its place when other factors condition on it. For interest rates, inflation, real estate, credit spreads, commodities and dividend yields, the step-to-step change in the indicator enters the drift:

$$
dX_t = \kappa(\mu - X_t)\,dt + \beta\,dL_t + \sigma\,dW_t
$$

The sensitivity $$\beta$$ is fitted from history. When a simulated path turns down, spreads widen and rates fall on that path, so recessions look like recessions across asset classes at the same time.

Two factors use the cycle differently:

- **Unemployment** adds it as a second term next to inflation (the $$\gamma$$ term above).
- **Equities** have no drift to extend. Instead the indicator's level changes the chance of switching between calm and crisis regimes, the time-varying transition probabilities of [Filardo (1994)](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}. See [markets](/projects/financescenarios/docs/markets).

A conditioned factor is fitted at the indicator's frequency, is used as fitted (no beliefs) and has constant volatility. Full reference: [LeadingIndicator](/projects/financescenarios/docs/reference/leading-indicator).

## Mortality and Longevity

Longevity risk is the risk that people live longer than a pension fund or annuity provider expected. Mortality has fallen for decades, but not at a steady pace, and that uncertain trend is what this factor captures.

### The Cairns-Blake-Dowd Model

Finance Scenarios uses the two-factor model of [Cairns, Blake and Dowd (2006)](https://doi.org/10.1111/j.1539-6975.2006.00195.x){:target="_blank"}, often called CBD:

$$
\operatorname{logit} q(x,t) = \kappa_1(t) + \kappa_2(t)\,(x - \bar{x})
$$

Here $$q(x,t)$$ is the one-year probability of death at age $$x$$ in year $$t$$, and $$\bar{x}$$ the middle of the fitted age range. $$\kappa_1$$ is the level, moving mortality at every age alike. $$\kappa_2$$ is the age slope: a higher slope means older ages move more than younger ones. Both are simulated, and correlated with rates, equities and the rest.

Unlike the other factors on this page, $$\kappa_1$$ and $$\kappa_2$$ do not revert. Each is a random walk with drift, as in the paper:

$$
\kappa_i(t+1) = \kappa_i(t) + \mu_i + \sigma_i\,z_i(t)
$$

Mortality improvement is a sustained trend over decades. The drift $$\mu_i$$ carries it forward, and the shocks put realistic uncertainty around it that widens with the horizon, which is what drives a longevity capital charge.

A fit on 40 years (1985 to 2024) of Dutch population death probabilities at ages 60 to 84 gave a level drift of -0.0153: death rates fall roughly 1.5% a year at every age. A 72-year-old in 2024 had a 1.9% chance of dying within the year, each extra year of age raised that by about 12%, and a 65-year-old's 0.89% drifts to about 0.75% in ten years.

### Data

Mortality is opt-in. Life tables come from Eurostat (European countries, yearly, from 1960 for most) or from your own table, for example from the [Human Mortality Database](https://www.mortality.org/){:target="_blank"} or a national statistics office. The default ages 60 to 84 are deliberate: the logit-linear shape is built for older ages, and many countries grouped "85 and over" until the 2010s.

```yaml
mortality:
  enabled: true
  source: eurostat
  country: Netherlands
  sex: total
  min_age: 60
  max_age: 84
  beliefs:
    kappa1:
      drift: -0.02  # death rates fall about 2% a year at every age
```

With your own table, pass one-year death probabilities ($$q_x$$), not central death rates ($$m_x$$). Both look plausible, but $$m_x$$ biases the fit by about 2% at age 90, which matters for a pension liability. To read a death rate at a given age back from the simulated factors:

```python
from financescenarios.factors.mortality.mortality_model import cbd_mortality_rate

q_70 = cbd_mortality_rate(
    result["mortality_level"], result["mortality_slope"],
    age=70, mean_age=scenarios.mortality.params.mean_age,
)  # one death probability per scenario and year
```

### Limits

- No cohort effects (one generation improving differently from its neighbors), and no Lee-Carter alternative.
- The straight-line shape holds locally: a death rate far outside the fitted ages, such as age 30 from a 60 to 89 fit, is not supported.
- With only two ages the fit is perfect by construction and says nothing about fit quality. The CBD paper fits ages 60 to 89.
- Mortality data are yearly, so with a short table its correlation with the other factors rests on few points.

Full reference: [Mortality](/projects/financescenarios/docs/reference/mortality).

## References

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. [casact.org](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." Journal of Econometrics, 31(3), 307-327. [doi.org](https://doi.org/10.1016/0304-4076(86)90063-1){:target="_blank"}
- Cairns, A.J.G., Blake, D., Dowd, K. (2006). "A Two-Factor Model for Stochastic Mortality with Parameter Uncertainty: Theory and Calibration." Journal of Risk and Insurance, 73(4), 687-718. [doi.org](https://doi.org/10.1111/j.1539-6975.2006.00195.x){:target="_blank"}
- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. [doi.org](https://doi.org/10.1016/j.jeconom.2005.03.005){:target="_blank"}
- Filardo, A.J. (1994). "Business-Cycle Phases and Their Transitional Dynamics." Journal of Business & Economic Statistics, 12(3), 299-308. [doi.org](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}
- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert Limited. [ressources-actuarielles.net](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"}
- Nelson, C.R., Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." Journal of Business, 60(4), 473-489. [doi.org](https://doi.org/10.1086/296409){:target="_blank"}
- Phillips, A.W. (1958). "The Relation Between Unemployment and the Rate of Change of Money Wage Rates in the United Kingdom, 1861-1957." Economica, 25(100), 283-299. [doi.org](https://doi.org/10.1111/j.1468-0335.1958.tb00003.x){:target="_blank"}
- Uhlenbeck, G.E., Ornstein, L.S. (1930). "On the Theory of the Brownian Motion." Physical Review, 36(5), 823-841. [doi.org](https://doi.org/10.1103/PhysRev.36.823){:target="_blank"}
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. [soa.org](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf){:target="_blank"}
