---
title: Markets and Credit
seo_title: Markets and Credit Documentation – Finance Scenarios
excerpt: "The theory behind the equity, FX, commodity, real estate, dividend, credit spread and rating migration models in Finance Scenarios: what each assumes, what it implies and where it stops."
description: "How Finance Scenarios models equities, FX, commodities, real estate, dividends, credit spreads and rating migration: assumptions, papers and limits."
author_profile: false
permalink: /projects/financescenarios/docs/markets
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

This page covers equities, exchange rates, commodities, real estate, dividends, credit spreads and rating migration. Each is fitted to its own history and moves with everything else through the correlation matrix (see the [simulation engine](/projects/financescenarios/docs/simulation-engine)). Interest rates and the economy have their own pages: [interest rates](/projects/financescenarios/docs/interest-rates) and [economy](/projects/financescenarios/docs/economy). Every option and parameter is in the [API reference](/projects/financescenarios/docs/reference).

## Equities

### Regime Switching (the Default)

Markets alternate between calm stretches with steady gains and turbulent ones with losses and large swings. The default is the regime-switching lognormal model of [Hardy (2001)](https://doi.org/10.1080/10920277.2001.10595984){:target="_blank"}: in each regime $$k$$ the log return is normal with its own mean $$\mu_k$$ and volatility $$\sigma_k$$, and a Markov chain decides each period whether to stay or switch.

$$
\ln\frac{S_{t+\Delta t}}{S_t} \,\Big|\, s_t = k \;\sim\; N\!\left(\mu_k \Delta t,\; \sigma_k^2 \Delta t\right)
$$

Why this works for long-horizon risk:

- **Fat tails.** A mixture of a low- and a high-volatility normal has more mass in the center and in the tails than one normal with the same variance.
- **Volatility clustering.** Regimes persist, so a turbulent month tends to follow another, as in 2008 or 2020.
- **Realistic drawdowns.** A guarantee or funding ratio cares how long a crisis lasts, not only how deep one year falls.

The regimes are estimated with the Baum-Welch algorithm ([Baum et al., 1970](https://doi.org/10.1214/aoms/1177697196){:target="_blank"}), and the simulation starts in the regime most likely at the last observation. SPY calibrated from 2005 on 2026-10-04 gave:

| Regime | Annual mean | Annual volatility | Average stay |
|:-------|------------:|------------------:|-------------:|
| Turbulent | -0.1% | 20.2% | about 8 months |
| Calm | 18.5% | 7.9% | about 10 months |

Transition probabilities are rescaled to the simulation step ([Israel, Rosenthal and Wei, 2001](https://doi.org/10.1111/1467-9965.00114){:target="_blank"}), so a monthly fit simulated weekly keeps the same expected time in each regime. Equity markets can share one stream of switches, so they enter and leave crises together.

```yaml
equities:
  - name: us_broad
    ticker: SPY
    n_regimes: 2
  - name: europe
    ticker: VGK
```

The limits: within a regime returns are lognormal, so the tails come only from the mixture, and there is no volatility smile in the real-world process. A rarely visited regime is poorly estimated.

### Linking Regimes to the Business Cycle

With business-cycle conditioning, the probability of switching regime depends on the leading indicator's level, following [Filardo (1994)](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}. For SPY, the chance of leaving the calm regime in a month rose from 5.8% at an indicator of 105 to 8.9% at 95, so a weakening economy shortens calm stretches from about 17 to 11 months. Crises then start more often in simulated downturns.

The regimes are fitted first and the switching logit second, a simpler route than the joint estimate of Filardo and of [Diebold, Lee and Weinbach (1994)](https://doi.org/10.1093/oso/9780198773917.003.0010){:target="_blank"}.

### Long Histories: Shiller and JST

A window from 2005 misses the 1930s, the wars and the 1970s. For runs of 50 to 100 years the regimes can instead be fitted on [Shiller's](https://shillerdata.com/){:target="_blank"} US total-return series (monthly, from 1871) or the [Jordà-Schularick-Taylor](https://doi.org/10.1093/qje/qjz012){:target="_blank"} equity returns of 18 countries (yearly, from 1870), while today's price and the correlations still come from the ticker. The JST database is licensed for non-commercial use only (CC BY-NC-SA 4.0).

### Alternative Equity Models

- **Hibbert: returns above cash.** The same two regimes, fitted on returns in excess of a short rate, as in [Hibbert, Mowbray and Turnbull (2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"}. The simulated short rate is added back, so equity returns move with rates. Against the 13-week bill, SPY's calm regime earned 16.5% a year above cash and its turbulent regime 1.5% below it.
- **Wilkie: price from dividends.** No fit of its own: the price is the simulated dividend index divided by the simulated dividend yield, the last link of [Wilkie's (1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf){:target="_blank"} cascade. See [Dividend Yield and Dividend Growth](#dividend-yield-and-dividend-growth).
- **KNW: shared stochastic volatility.** A short rate plus a constant risk premium, with variance driven by the volatility factor shared with rates and inflation. See [KNW models](/projects/financescenarios/docs/knw).

### Risk-Neutral Equities

To value options or guarantees, prices must be consistent with today's market. Under the risk-neutral measure the expected return is the risk-free rate minus the dividend yield, and the process is a geometric Brownian motion in the spirit of [Black and Scholes (1973)](https://doi.org/10.1086/260062){:target="_blank"} and [Merton (1973)](https://doi.org/10.2307/3003143){:target="_blank"}:

$$
d\ln S_t = \left(r - q - \tfrac{1}{2}\sigma^2\right)dt + \sigma\,dW_t
$$

Here $$r$$ is the current short rate, $$q$$ the dividend yield of the same ticker and $$\sigma$$ a single volatility. The volatility can come from:

| Source | Where $$\sigma$$ comes from | Good for |
|:-------|:-----------------------|:---------|
| Implied (default) | At-the-money implied volatility of one expiration, at least a week out | Liquid index options |
| SVI | At-the-money point of the fitted volatility surface ([Gatheral and Jacquier, 2014](https://doi.org/10.1080/14697688.2013.819986){:target="_blank"}) | Smoothing single-quote noise |
| Realized | Standard deviation of historical returns | ETFs without liquid options |
| Heston | The [Heston (1993)](https://doi.org/10.1093/rfs/6.2.327){:target="_blank"} stochastic-volatility model, fitted to the surface from one to twelve months | Keeping the smile and term structure |

For SPY on 2026-10-04, with a 3.99% bill rate and a 1.15% dividend yield, the drift was 2.84% and the four sources agreed within about three points (13.5% to 16.2%).

```yaml
equities:
  - name: us_broad
    ticker: SPY
    measure: risk_neutral
    volatility_source: svi
dividend_yield:
  - name: spy_yield
    ticker: SPY
```

Beliefs don't apply here: the entry must match market prices. Reference: [Equities API](/projects/financescenarios/docs/reference/equities).

## FX

An exchange rate has no natural long-run level over decades, so it is not mean-reverting. Each pair is a geometric Brownian motion against the US dollar, the standard treatment surveyed by [Gorvett (2001)](https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf){:target="_blank"}, so the rate stays positive.

What matters is the drift:

| Drift | Assumption | When to use it |
|:------|:-----------|:---------------|
| Historical (default) | The sample's own trend continues | Short horizons, or when you trust the window's trend |
| Random walk | No trend: the median stays at today's rate | Long horizons; [Meese and Rogoff (1983)](https://doi.org/10.1016/0022-1996(83)90017-X){:target="_blank"} found a random walk forecasts at least as well as structural models |
| Interest-rate parity | Each step, the gap between the two simulated short rates | When currency moves should follow rate differentials |

Under uncovered interest-rate parity, the higher-yielding currency is expected to depreciate by the rate gap, so either currency earns the same in expectation:

$$
d\ln S_t = \left(r^f_t - r^d_t - \tfrac{1}{2}\sigma^2\right)dt + \sigma\,dW_t
$$

Here $$S_t$$ is foreign currency per dollar, $$r^f_t$$ the foreign and $$r^d_t$$ the US short rate, both read from the same simulated path. A higher US rate pushes the quote down. Empirically, uncovered parity often fails over short horizons (the carry trade exists because of that), so the random walk is the shipped default for long-horizon work.

```yaml
fx:
  - name: eur
    country: EA20  # keyed by currency area, so the euro is EA20
    drift_mode: irp
    domestic_rate_name: united_states_short_rate
    foreign_rate_name: eurozone_short_rate
```

Under the risk-neutral measure, the drift is fixed at the foreign minus US short rate at calibration (covered interest parity). Volatility stays historical, since there is no FX options source. Reference: [FX API](/projects/financescenarios/docs/reference/fx).

## Commodities

A commodity price is pulled toward a level set by production and storage: high prices bring new supply, low prices cut production. Storage costs and the convenience yield (the benefit of holding the physical good) tie spot and futures prices together, the core result of [Schwartz (1997)](https://doi.org/10.1111/j.1540-6261.1997.tb02721.x){:target="_blank"}.

### Single Factor (the Default)

The log price reverts to one long-run level, which keeps the price positive:

$$
dX_t = \kappa(\mu - X_t)\,dt + \sigma\,dW_t, \qquad X_t = \ln S_t
$$

$$e^{\mu}$$ is the long-run median price. On 2026-10-04 crude oil started at 91.11 USD and was pulled toward 67.06 USD, with a shock halving in about six months. Because $$\mu$$ is a log price, a belief of a 70 USD median is written as $$\ln 70$$.

### Schwartz-Smith Two Factor

One reversion speed cannot describe both a supply disruption that clears in months and a lasting shift in demand or cost. [Schwartz and Smith (2000)](https://doi.org/10.1287/mnsc.46.7.893.12034){:target="_blank"} split the log price into a short-term deviation $$\chi_t$$ that fades and a long-term equilibrium level $$\xi_t$$ that drifts:

$$
\ln S_t = \chi_t + \xi_t, \qquad d\chi_t = -\kappa\,\chi_t\,dt + \sigma_\chi\,dW^\chi_t, \qquad d\xi_t = \mu_\xi\,dt + \sigma_\xi\,dW^\xi_t
$$

The two shocks are correlated. Near-dated futures reflect both factors, long-dated ones almost only the long-term one, so the futures curve identifies them. The volatilities come from the curve where one is listed (crude oil, natural gas, gold, silver, copper, corn, wheat and soybeans); spot prices alone understate the long-term volatility about tenfold.

The risk-neutral version keeps the same volatilities and fits only the two drift terms to today's futures prices. On 2026-10-04 the steeply backwardated crude curve implied the long-term level falling about 17.7% a year, against 2.5% in the real-world fit.

```yaml
commodities:
  - name: oil
    ticker: CL=F
    method: schwartz_smith
```

### Limits

A trending price over a short window has no mean reversion to fit: gold sampled monthly from 2016 fails, while on daily prices since 2000 it reverts, very slowly. Schwartz's convenience-yield and stochastic-rate variants are not implemented. Reference: [Commodities API](/projects/financescenarios/docs/reference/commodities).

## Real Estate

The model follows eq. 3.18 of [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}: the growth rate of property prices mean-reverts to a long-run rate. Booms fade in growth but leave a permanent mark on the price level. The authors found inflation insignificant as a direct driver, so real estate links to the rest only through correlations.

Two series are available: OECD residential house-price growth for many countries, and for the United States FRED's commercial property index ([`COMREPUSQ159N`](https://fred.stlouisfed.org/series/COMREPUSQ159N){:target="_blank"}, from the IMF; quarterly, needs a FRED key).

On 2026-10-06, US house prices were 2.1% above a year earlier and pulled toward 3.4% a year, with a boom or slump fading by half in about 5.7 years. Commercial property grew faster (6.6%) but toward a lower 2.5%, reverted within about a year and was almost four times as volatile, as a transaction-based series would be.

Neither source matches the paper, which used NCREIF's appraisal-based index; appraisals smooth prices and understate volatility, and there is no open equivalent (see [coverage](/projects/financescenarios/docs/coverage)). Reference: [Real estate API](/projects/financescenarios/docs/reference/real-estate).

## Dividend Yield and Dividend Growth

### Dividend Yield

When dividend income matters on its own, the yield is simulated separately from the equity's total return. Following eq. 3.17 of [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}, the log of the yield mean-reverts, so the yield stays positive:

$$
d\ln y_t = \kappa(\mu - \ln y_t)\,dt + \sigma\,dW_t
$$

On 2026-10-04 SPY yielded 0.99% and was pulled toward 1.39% with a half-life of about 4.7 years. The source paper found the speed "not significantly different from zero" on 1871-2003 data, so a short window may show no reversion at all. A belief about the normal level is a log too: a 2% target is $$\ln 0.02 \approx -3.9$$. An optional inflation term, as in Wilkie, links the yield to an inflation entry.

### Dividend Growth (Wilkie)

[Wilkie's (1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf){:target="_blank"} model is a one-way cascade: inflation, then dividend yield, dividend growth and the share price (dividend index divided by yield). Dividend growth is Wilkie's "Reduced Basis" equation:

$$
\Delta \ln D_t = \mu_D + w\,\Delta\ln Q_t + x\,M_{t-1} + y\,\varepsilon^Y_{t-1} + \sigma_D\,z_t
$$

| Term | Wilkie | Economics |
|:-----|:-------|:----------|
| $$\mu_D$$ | DMU | Real dividend growth |
| $$w\,\Delta\ln Q_t$$ | DW | Part of this year's inflation passes straight into dividends |
| $$x\,M_{t-1}$$ | DX | A slow moving average of past inflation, so dividends keep catching up with prices over time |
| $$y\,\varepsilon^Y_{t-1}$$ | DY | Last year's surprise in the dividend yield: prices anticipate dividend changes, so the yield moves first |
| $$\sigma_D\,z_t$$ | DSD | The dividend index's own shock |

The moving-average weight is fixed at Wilkie's 0.2; the rest is fitted by one regression. Wilkie fitted 1919-1982 UK data; the shipped `wilkie` preset applies the same equations to US data.

```yaml
dividend_growth:
  - name: dividend_growth
    ticker: JNJ
    inflation_name: inflation
    dividend_yield_name: dividend_yield
```

References: [Dividend yield API](/projects/financescenarios/docs/reference/dividend-yield), [Dividend growth API](/projects/financescenarios/docs/reference/dividend-growth).

## Credit Spreads

A credit spread is the extra yield a company pays over government debt: compensation for expected default losses, plus a risk and liquidity premium that widens sharply in a downturn. Each spread bucket mean-reverts in logs, which keeps it positive and makes its swings proportional to its level: wide spreads are also the most volatile:

$$
d\ln s_t = \kappa(\mu - \ln s_t)\,dt + \sigma\,dW_t
$$

Spreads revert quickly: on 2026-10-04 the 7-10 year investment-grade spread started at 1.05% and was pulled toward 1.01% with a half-life of about three months. Conditioning on the business cycle lets spreads widen as a simulated path turns down.

The data: ICE BofA US option-adjusted spreads by maturity or rating (`AAA` to `CCC`), Moody's `Aaa` and `Baa` yields over Treasuries from 1953, German ([Bundesbank](https://www.bundesbank.de/en/statistics/money-and-capital-markets){:target="_blank"}) and Australian ([RBA table F3](https://www.rba.gov.au/statistics/tables/){:target="_blank"}) corporate spreads, and the ECB's cost of new bank loans to companies ([ECB MIR](https://data.ecb.europa.eu/data/datasets/MIR){:target="_blank"}).

FRED serves only the last three years of the ICE BofA indices, too short for a reliable correlation with yearly factors, so the shipped factor sets leave credit off. The Moody's and corporate series cover several credit cycles. There is no euro or UK spread by rating, since those indices are licensed.

```yaml
credit:
  - name: baa_aaa
    dimension: moodys
    rating_bucket: Baa - Aaa
```

For a full spread curve rather than buckets, see the [credit term structure API](/projects/financescenarios/docs/reference/credit-term-structure). Reference: [Credit API](/projects/financescenarios/docs/reference/credit).

## Credit Migration and Default

Spreads price credit risk; migration models the events: downgrades, defaults and losses on a bond portfolio by rating.

Each borrower's credit quality is a standard normal draw made of two parts: a shared credit cycle $$Z$$, weighted by the asset correlation $$\rho$$, and the borrower's own luck. A through-the-cycle transition matrix sets each rating's thresholds for upgrade, downgrade and default. In a given year, the default probability of a rating with long-run default probability $$p$$ becomes

$$
p(Z) = \Phi\!\left(\frac{\Phi^{-1}(p) - \sqrt{\rho}\,Z}{\sqrt{1-\rho}}\right)
$$

where $$\Phi$$ is the standard normal distribution function. The same shift applies to every threshold, so a bad year ($$Z$$ low) moves every rating toward downgrade and default at once. This is the one-factor approach described by [Kim (1999)](https://www.msci.com/www/research-report/a-way-to-condition-transition/018440984){:target="_blank"}, in the Markov rating framework of [Jarrow, Lando and Turnbull (1997)](https://doi.org/10.1093/rfs/10.2.481){:target="_blank"}, and the same formula that underlies the Basel IRB capital charge.

The data is ESMA's [CEREP](https://registers.esma.europa.eu/cerep-publication){:target="_blank"} repository of rating agency statistics. The cycle is backed out year by year from default rates, then simulated as mean-reverting around zero, the through-the-cycle average. A rating that never defaulted in the sample gets Basel's 0.03% floor ([CRR Article 160(1)](https://eur-lex.europa.eu/eli/reg/2013/575/oj){:target="_blank"}). CEREP publishes a year's statistics during the next year, so the latest year can lag.

On S&P corporate ratings from 2000 to 2025, the worst years came out as 2009, 2001, 2020 and 2002, the asset correlation was about 0.10, and a shock to the cycle halved in about eight months.

```yaml
credit_migration:
  enabled: true
  agency: S&P
  matrix_years: 10  # years of transitions pooled into the matrix
```

```python
from financescenarios import rating_migration

# share in each rating, defaults and loss after 40% recovery, per scenario and year
migration = rating_migration(result, {"A": 40, "BBB": 50, "BB": 10}, recovery_rate=0.4)
migration.summary()
```

The limits: spreads are not derived from the ratings (use [credit spreads](#credit-spreads) for that), recovery is a fixed input rather than falling in downturns, and the cycle is one index for all sectors and regions. Reference: [Credit migration API](/projects/financescenarios/docs/reference/credit-migration).
