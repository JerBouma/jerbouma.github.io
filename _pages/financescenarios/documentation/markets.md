---
title: Markets and Credit
seo_title: "Markets and Credit Documentation | Finance Scenarios"
seo_title_suffix: false
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

How far can equities fall and for how long, what does a currency or a credit spread add to that, and how many bonds default in a bad year? This page sets out how equities, exchange rates, commodities, real estate, dividends, credit spreads and rating migration are modeled. Each is fitted to its own history and moves with everything else through the correlation matrix (see the [simulation engine](/projects/financescenarios/docs/simulation-engine)). [Interest rates](/projects/financescenarios/docs/interest-rates) and [the economy](/projects/financescenarios/docs/economy) have their own pages, and every option is in the [API reference](/projects/financescenarios/docs/reference).

## Equities

### Regime Switching (the Default)

Markets alternate between calm stretches of steady gains and turbulent ones of losses and large swings. The default is the regime-switching lognormal model of [Hardy (2001)](https://doi.org/10.1080/10920277.2001.10595984){:target="_blank"}: in regime $$k$$ the log return is normal with its own mean $$\mu_k$$ and volatility $$\sigma_k$$, and a Markov chain decides each period whether to stay or switch.

$$
\ln\frac{S_{t+\Delta t}}{S_t} \,\Big|\, s_t = k \;\sim\; N\!\left(\mu_k \Delta t,\; \sigma_k^2 \Delta t\right)
$$

Hardy fitted it by maximum likelihood to monthly S&P 500 and TSX 300 returns ([abstract](https://www.casact.org/abstract/regime-switching-model-long-term-stock-returns){:target="_blank"}).

This suits long-horizon risk: a mix of a low- and a high-volatility normal has fatter tails than one normal of the same variance, regimes persist so turbulent months cluster (2008, 2020), and drawdowns run over several periods, which is what a guarantee or funding ratio feels.

The regimes are estimated with the Baum-Welch algorithm ([Baum et al., 1970](https://doi.org/10.1214/aoms/1177697196){:target="_blank"}), and the simulation starts in the regime most likely today. SPY calibrated from 2005 on 2026-10-04 gave:

| Regime | Annual mean log return | Annual volatility | Average stay |
|:-------|------------:|------------------:|-------------:|
| Turbulent | -0.1% | 20.2% | about 8 months |
| Calm | 18.5% | 7.9% | about 10 months |

Transition probabilities are rescaled to the simulation step through the matrix's generator ([Israel, Rosenthal and Wei, 2001](https://doi.org/10.1111/1467-9965.00114){:target="_blank"}), so a monthly fit simulated weekly keeps the same expected time in each regime. By default all equity markets share one stream of switches, so they enter and leave crises together.

The limits: within a regime returns are lognormal, so the tails come only from the mixture, and a rarely visited regime is poorly estimated.

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
equities:
  - name: us_broad
    ticker: SPY
    n_regimes: 2
```

### Linking Regimes to the Business Cycle

With business-cycle conditioning, the probability of switching regime depends on the leading indicator's level: the time-varying transition probabilities of [Filardo (1994)](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}. For SPY, the chance of leaving the calm regime in a month rose from 5.8% at an indicator of 105 to 8.9% at 95, so a weakening economy shortens calm stretches from about 17 to 11 months and crises start more often in simulated downturns. The estimate takes the simpler two-step route of [Diebold, Lee and Weinbach (1994)](https://doi.org/10.1093/oso/9780198773917.003.0010){:target="_blank"}: first the regimes, then a logit of the next regime on the indicator.

These stays are longer than the 10 months of the plain fit above, mainly because the logit counts switches between each month's most likely regime, which ignores brief one-month visits that the plain fit's transition probabilities include. Read the conditioning as relative: calm stretches about a third shorter in a weak economy than in a strong one.

### Long Histories: Shiller and JST

A window from 2005 misses the 1930s, the wars and the 1970s. For runs of 50 to 100 years the regimes can be fitted on [Shiller's](https://shillerdata.com/){:target="_blank"} US total returns (monthly, from 1871) or the [Jordà-Schularick-Taylor](https://doi.org/10.1093/qje/qjz012){:target="_blank"} equity returns of 18 countries (yearly, from 1870; non-commercial use only), while today's price and the correlations still come from the ticker.

### Alternative Equity Models

- **Hibbert: returns above cash.** The same two regimes, fitted on returns in excess of a short rate, as in [Hibbert, Mowbray and Turnbull (2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"}. The simulated short rate is added back, so equity returns move with rates. Against the 13-week bill, SPY's calm regime earned 16.5% a year above cash and its turbulent regime 1.5% below it.
- **Wilkie: price from dividends.** The simulated dividend index divided by the simulated dividend yield, the last link of [Wilkie's (1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf){:target="_blank"} cascade (see [below](#dividend-yield-and-dividend-growth)).
- **KNW: shared stochastic volatility.** The equity leg of the [KNW model](/projects/financescenarios/docs/knw), fitted together with its interest rate, with variance driven by a volatility factor shared with rates and inflation.

### Risk-Neutral Equities

To value options or guarantees, scenarios must reproduce today's market prices. Under the risk-neutral measure the expected price growth is the risk-free rate minus the dividend yield, and the process is a geometric Brownian motion as in [Black and Scholes (1973)](https://doi.org/10.1086/260062){:target="_blank"} and [Merton (1973)](https://doi.org/10.2307/3003143){:target="_blank"}:

$$
d\ln S_t = \left(r - q - \tfrac{1}{2}\sigma^2\right)dt + \sigma\,dW_t
$$

Here $$r$$ is today's short rate, $$q$$ today's dividend yield of the same ticker (from a dividend yield entry) and $$\sigma$$ the volatility, taken from:

| Source | Where $$\sigma$$ comes from | Good for |
|:-------|:-----------------------|:---------|
| Implied (default) | At-the-money implied volatility of one expiration, at least a week out | Liquid index options |
| SVI | At-the-money point of the fitted surface ([Gatheral and Jacquier, 2014](https://doi.org/10.1080/14697688.2013.819986){:target="_blank"}) | Smoothing quote noise |
| Realized | Historical return volatility | Tickers without liquid options |
| Heston | A stochastic variance ([Heston, 1993](https://doi.org/10.1093/rfs/6.2.327){:target="_blank"}) fitted to one- to twelve-month options | Keeping the smile and term structure |

For SPY on 2026-10-04 the bill rate was 3.99% and the dividend yield entry started at 0.99% (twelve months of dividends over the price, averaged over the last month, the same level used [below](#dividend-yield)), a drift of about 3.0%. The implied, SVI and realized volatilities came out between 13.5% and 14.9%. Beliefs don't apply here: the entry must match market prices.

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
equities:
  - name: us_broad
    ticker: SPY
    measure: risk_neutral
    volatility_source: svi
dividend_yield:
  - name: spy_yield
    ticker: SPY
```

Reference: [Equities API](/projects/financescenarios/docs/reference/equities).

## FX

An exchange rate has no natural long-run level over decades, so it is not modeled as mean-reverting. Each pair is a geometric Brownian motion against the US dollar, the standard treatment surveyed by [Gorvett (2001)](https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf){:target="_blank"}; the rate stays positive and its tails are lognormal. What matters is the drift:

| Drift | Assumption | When to use it |
|:------|:-----------|:---------------|
| Random walk (default) | No trend: the median stays at today's rate | Most uses; a random walk forecasts at least as well as structural models ([Meese and Rogoff, 1983](https://doi.org/10.1016/0022-1996(83)90017-X){:target="_blank"}) |
| Historical | The sample's own trend continues | A deliberate currency view, over short horizons |
| Interest-rate parity | Each step, the gap between the two simulated short rates | Currency moves that follow rate differentials |

A fitted trend is a currency view carried forward for decades: on 2021-2026 data the yen would get a 7.1% yearly drift from the dollar's strong run against it. Over long horizons Barrie & Hibbert's model instead ties exchange rates to purchasing power, which rules out a lasting trend of their own ([Hibbert, Mowbray and Turnbull, 2001, section 9.3, p. 69](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf#page=69){:target="_blank"}).

The volatility comes from the rate at the end of each month (or quarter or year), published by the BIS. The OECD publishes averages over each period, and changes of averages keep only about two-thirds of a random walk's variance ([Working, 1960](https://doi.org/10.2307/1907574){:target="_blank"}): on monthly data since 2021 the euro's volatility is 7.4% from month-end rates against 5.9% from the averages, the yen's 10.8% against 8.6%. The yearly Global Macro Database has averages only, so there the volatility is scaled up by Working's factor; `end_of_period: false` fits the averages as published.

Under uncovered interest-rate parity the higher-yielding currency is expected to depreciate by the rate gap, so both currencies earn the same in expectation:

$$
d\ln S_t = \left(r^f_t - r^d_t - \tfrac{1}{2}\sigma^2\right)dt + \sigma\,dW_t
$$

Here $$S_t$$ is foreign currency per dollar, $$r^f_t$$ the foreign and $$r^d_t$$ the US short rate, both read from the same simulated path. A higher foreign rate pushes the quote up (the foreign currency weakens); a higher US rate pushes it down. Uncovered parity often fails empirically (the carry trade profits from that), one more reason the random walk is the default.

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
fx:
  - name: eur
    country: EA20  # keyed by currency area, so the euro is EA20
    drift_mode: irp
    domestic_rate_name: united_states_short_rate
    foreign_rate_name: eurozone_short_rate
```

Under the risk-neutral measure the drift is fixed at today's foreign minus US short rate (covered interest parity), and the volatility comes from history. Reference: [FX API](/projects/financescenarios/docs/reference/fx).

## Commodities

A commodity price is pulled toward a level set by production cost: high prices bring new supply, low prices cut production. Storage costs and the convenience yield (the benefit of holding the physical good) tie spot and futures prices together, the core of [Schwartz (1997)](https://doi.org/10.1111/j.1540-6261.1997.tb02721.x){:target="_blank"}.

### Single Factor (the Default)

The log price reverts to one long-run level, as in the one-factor model of [Schwartz (1997, abstract, p. 923)](https://afajof.org/issue/volume-52-issue-3){:target="_blank"}, which keeps the price positive and its distribution lognormal:

$$
dX_t = a(\theta - X_t)\,dt + \sigma\,dW_t, \qquad X_t = \ln S_t
$$

Here $$a$$ is the speed of reversion and $$\theta$$ the long-run log price, so $$e^{\theta}$$ is the long-run median price; a belief of a 70 USD median is written as $$\ln 70$$. On 2026-10-04 crude oil started at 91.11 USD and was pulled toward 67.06 USD, with a shock halving in about six months.

### Schwartz-Smith Two Factor

One reversion speed cannot describe both a supply outage that clears in months and a lasting shift in cost. [Schwartz and Smith (2000)](https://doi.org/10.1287/mnsc.46.7.893.12034){:target="_blank"} split the log price into a short-term deviation $$\chi_t$$ that fades and a long-term level $$\xi_t$$ that drifts as a random walk:

$$
\ln S_t = \chi_t + \xi_t, \qquad d\chi_t = -a\,\chi_t\,dt + \sigma_\chi\,dW^\chi_t, \qquad d\xi_t = \mu_\xi\,dt + \sigma_\xi\,dW^\xi_t
$$

The two shocks are correlated. Long-dated futures reflect almost only $$\xi_t$$ and the gap between short and long contracts reflects $$\chi_t$$, so the futures curve separates the two ([Schwartz and Smith, 2000, abstract, p. 893](https://jimsmith.host.dartmouth.edu/wp-content/uploads/2022/04/Short-term_Long-term_Model.pdf#page=1){:target="_blank"}).

The volatilities are fitted to the listed futures (crude oil, natural gas, gold, silver, copper, corn, wheat and soybeans). Fitted on spot prices alone, with a moving average standing in for the long-term level, the long-term volatility comes out far too low, because the averaging smooths it away.

The risk-neutral version keeps the same volatilities and fits only the two drift terms to today's futures prices: a backwardated curve gives a falling long-term level, a contango curve a rising one. The fit uses the first twelve monthly contracts, and the drift it finds is held for the whole horizon. On 2026-10-04 crude fell from 91.11 USD (November 2026) to 77.90 USD (September 2027), so the long-term level drifted down about 17.7% a year, against 2.5% a year in the real-world fit. A steep front-end backwardation is thus carried well past the last contract; for long horizons, read it as a pricing input, not as a path for the oil price.

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
commodities:
  - name: oil
    ticker: CL=F
    method: schwartz_smith
```

### Limits

A trending price over a short window has no mean reversion to fit: gold sampled monthly from 2016 fails, while on daily prices since 2000 it reverts, very slowly. With GARCH volatility or business-cycle conditioning the single-factor model is fitted on the price level rather than its log, so positivity is no longer guaranteed. Schwartz's convenience-yield and stochastic-rate variants are not implemented. Reference: [Commodities API](/projects/financescenarios/docs/reference/commodities).

## Real Estate

The model follows eq. 3.18 of [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf#page=21){:target="_blank"}: the year-over-year growth rate of property prices, not the price level, reverts to a long-run rate, since a price index has no level to return to over decades. Booms fade in growth but leave a permanent mark on the price level. The paper fitted it on quarterly NCREIF returns from 1978 to 2001.

The simulated path is price growth only. Rental income, about half of housing's long-run return, is added when real estate is held as an asset (see [portfolio](/projects/financescenarios/docs/portfolio#what-a-portfolio-can-hold)).

The data are OECD residential house-price growth for many countries, or for the United States the IMF's commercial property index on FRED ([`COMREPUSQ159N`](https://fred.stlouisfed.org/series/COMREPUSQ159N){:target="_blank"}; quarterly, needs a FRED key). Where the paper fits quarterly returns, this fits year-over-year growth read each quarter, so residential and commercial sit on one scale. Neighbouring readings then share three of their four quarters, so, as for [inflation](/projects/financescenarios/docs/economy#inflation), each is regressed on the reading a year earlier. On 2026-10-14, US house prices were 2.1% above a year earlier and pulled toward 4.3% a year, with a boom or slump fading by half in about 1.9 years; the quarter-to-quarter fit said 5.7 years. Commercial property reverted within about five months, with about twice the yearly volatility.

Neither source matches the paper's appraisal-based NCREIF index; appraisals smooth prices and understate volatility, and there is no open equivalent (see [coverage](/projects/financescenarios/docs/coverage)). Reference: [Real estate API](/projects/financescenarios/docs/reference/real-estate).

## Dividend Yield and Dividend Growth

### Dividend Yield {#dividend-yield}

When dividend income matters on its own, the yield is simulated separately from the equity's total return. Following eq. 3.17 of [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf#page=20){:target="_blank"}, who follow Wilkie (1986) and Hibbert, Mowbray and Turnbull (2001), the log of the yield mean-reverts, so the yield stays positive:

$$
d\ln y_t = a(\theta - \ln y_t)\,dt + \sigma\,dW_t
$$

On 2026-10-04 SPY yielded 0.99% and was pulled toward 1.39% with a half-life of about 4.7 years. The paper found the speed "not significantly different from zero" on 1871-2003 data, so a short window may show no reversion at all. A belief about the normal level is a log too ($$\ln 0.02$$ for 2%). An optional term on the same step's change in inflation, as in Wilkie, links the yield to inflation.

### Dividend Growth (Wilkie)

[Wilkie's (1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf){:target="_blank"} model is a one-way cascade: inflation, then dividend yield, dividend growth and the share price (dividend index divided by yield). Dividend growth is his "Reduced Standard Basis" equation ([section 3.9](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf#page=4){:target="_blank"}), a slightly simpler form that he found gives very similar long-term results, with $$\Delta\ln Q_t$$ the force of inflation (the log change in the price index):

$$
\Delta \ln D_t = \mu_D + w\,M_t + x\,\Delta\ln Q_t + y\,\varepsilon^Y_{t-1} + \sigma_D\,z_t, \qquad w + x = 1
$$

| Term | Wilkie | Economics |
|:-----|:-------|:----------|
| $$\mu_D$$ | DMU | Real dividend growth |
| $$w\,M_t$$ | DW | Smoothed inflation, $$M_t = 0.2\,\Delta\ln Q_t + 0.8\,M_{t-1}$$ a year: dividends catch up with prices over time |
| $$x\,\Delta\ln Q_t$$ | DX | Part of this period's inflation passes straight into dividends |
| $$y\,\varepsilon^Y_{t-1}$$ | DY | Last period's dividend yield surprise: prices anticipate dividend changes, so the yield moves first |
| $$\sigma_D\,z_t$$ | DSD | The dividend index's own shock |

The two inflation weights add up to one, Wilkie's unit gain ([section 3.7](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf#page=4){:target="_blank"}): in the long run dividends, and so share prices, keep their real value. The fit imposes it, fixes the smoothing weight at Wilkie's 0.2 a year (converted to the data's step) and estimates the rest by one regression.


Wilkie fitted 1919-1982 UK data; the shipped Wilkie factor set applies the same equations to US data.

References: [Dividend yield API](/projects/financescenarios/docs/reference/dividend-yield), [Dividend growth API](/projects/financescenarios/docs/reference/dividend-growth).

## Credit Spreads

A credit spread is the extra yield a company pays over government debt: expected default losses plus a risk and liquidity premium that widens sharply in a downturn. The spread reverts to a normal level as an Ornstein-Uhlenbeck process. Fitting it in logs is a modeling judgement rather than a published specification: it keeps the spread positive and makes its swings proportional to its level, so wide spreads are the most volatile and the distribution is skewed toward sharp widenings:

$$
d\ln s_t = a(\theta - \ln s_t)\,dt + \sigma\,dW_t
$$

A series that has touched zero or below is fitted on its level instead. On 2026-10-04 the 7-10 year investment-grade spread started at 1.05% and was pulled toward a median of 1.01%, with a half-life of about three months. That speed comes from three years of monthly data, too few for a reliable estimate, and short samples tend to overstate how fast a series reverts; the Moody's series, monthly from 1953, gives a steadier read. Business-cycle conditioning lets spreads widen as a simulated path turns down, but that variant, like GARCH volatility, is fitted on the spread level rather than its log, so it can turn negative.

| Data | History |
|:--|:--|
| ICE BofA US option-adjusted spreads by maturity or rating (`AAA` to `CCC`) | Last three years only (FRED), too short for stable correlations, so the shipped factor sets leave credit off |
| Moody's `Aaa` and `Baa` yields over the 10-year Treasury | Monthly from 1953 |
| Corporate spreads for Germany ([Bundesbank](https://www.bundesbank.de/en/statistics/money-and-capital-markets){:target="_blank"}) and Australia ([RBA table F3](https://www.rba.gov.au/statistics/tables/){:target="_blank"}) | Monthly, from 1957 and 2005 |
| ECB cost of new bank loans to euro area companies ([ECB MIR](https://data.ecb.europa.eu/data/datasets/MIR){:target="_blank"}), a rate rather than a spread | Monthly from 2003 |

Euro and UK spreads by rating are not available: those indices are licensed.

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
credit:
  - name: baa_aaa
    dimension: moodys
    rating_bucket: Baa - Aaa
    period: monthly
```

For a whole spread curve rather than buckets, see the [credit term structure API](/projects/financescenarios/docs/reference/credit-term-structure). Reference: [Credit API](/projects/financescenarios/docs/reference/credit).

## Credit Migration and Default

Spreads price credit risk; migration models the events: downgrades, defaults and losses on a bond portfolio by rating. Each borrower's credit quality is a standard normal variable: a shared credit cycle $$Z$$ with weight $$\sqrt{\rho}$$, for asset correlation $$\rho$$, plus the borrower's own luck. A through-the-cycle transition matrix sets each rating's thresholds for upgrade, downgrade and default. In a year with cycle $$Z$$, a rating with long-run default probability $$p$$ defaults with probability

$$
p(Z) = \Phi\!\left(\frac{\Phi^{-1}(p) - \sqrt{\rho}\,Z}{\sqrt{1-\rho}}\right)
$$

where $$\Phi$$ is the standard normal distribution function. The same shift applies to every threshold, so a bad year ($$Z$$ below zero) moves every rating toward downgrade and default at once. This is the one-factor approach of [Kim (1999)](https://www.msci.com/www/research-report/a-way-to-condition-transition/018440984){:target="_blank"}, in the Markov rating framework of [Jarrow, Lando and Turnbull (1997)](https://doi.org/10.1093/rfs/10.2.481){:target="_blank"}, and the same formula that underlies the Basel IRB capital charge.

The data are ESMA's [CEREP](https://registers.esma.europa.eu/cerep-publication){:target="_blank"} rating agency statistics, which lag one to two years. The cycle is backed out year by year from default rates, then simulated as mean-reverting around zero (the through-the-cycle average) and correlated with the other factors. Every rating's long-run default probability is floored at 0.05%, so one that never defaulted in the sample still carries some risk. That is the corporate PD input floor of CRR3 ([Regulation (EU) 2024/1623, Article 1, point (86)(a)](https://eur-lex.europa.eu/eli/reg/2024/1623/oj/eng){:target="_blank"}), which from 2025 replaced the 0.03% of the original [CRR Article 160(1)](https://eur-lex.europa.eu/eli/reg/2013/575/oj){:target="_blank"}.

The 0.03% floor remains available for a Basel II comparison. The transition matrix pools the rating changes of every year in the history, not only the latest ones, so it reflects an average year across good and bad ones, as Basel asks of PD estimation: the longest relevant observation period, with a representative mix of good and bad years ([Basel Framework, CRE36.79](https://www.bis.org/basel_framework/chapter/CRE/36.htm){:target="_blank"}).

On S&P corporate ratings from 2000 to 2025, the worst years came out as 2009, 2001, 2020 and 2002, the asset correlation was about 0.10, and a shock to the cycle halved in about eight months.

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
credit_migration:
  enabled: true
  agency: S&P
```

```python
from financescenarios import rating_migration

# share in each rating, defaults and loss after 40% recovery, per scenario and year
migration = rating_migration(result, {"A": 40, "BBB": 50, "BB": 10}, recovery_rate=0.4)
migration.summary()
```

The limits: spreads are not derived from the ratings (model them separately as [credit spreads](#credit-spreads)), recovery is fixed rather than falling in downturns, and one cycle drives all sectors and regions. Reference: [Credit migration API](/projects/financescenarios/docs/reference/credit-migration).
