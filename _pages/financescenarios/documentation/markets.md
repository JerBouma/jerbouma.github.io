---
title: Markets and Credit
seo_title: "Markets and Credit Documentation | Finance Scenarios"
seo_title_suffix: false
excerpt: "How the default model sets equities, currencies, gold, oil and house prices: regimes timed on long indices, returns on the short rate plus a long-run premium, purchasing power parity, and how every number is derived from data."
description: "Equities, FX, commodities and real estate in Finance Scenarios: the theory, the sourced and fitted numbers, the charts that derive them, and the dividend, credit spread and rating migration models."
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

How far can equities fall and for how long, what does a currency add to that, and what moves house prices? In the default model each equity market switches between calm and turbulent regimes timed on decades of its own index, turbulence is likelier when inflation is high, and every market earns the simulated short rate plus a long-run premium. The euro and the pound revert to purchasing power parity, the yen and gold have no trend of their own, oil swings around a level, and house prices slow after the long rate rises.

This page explains the theory of each, then derives every number: what it is, whether it comes from a published source, a fit on data or a judgement, and the chart that shows it. The numbers come from one calibration of the default settings and factor set, made on 17 October 2026. [Interest rates](/projects/financescenarios/docs/interest-rates) and [the economy](/projects/financescenarios/docs/economy) have their own pages, and every option is in the [API reference](/projects/financescenarios/docs/reference).

<div class="ca-nav">
  <a href="#equities"><i class="fas fa-chart-line" aria-hidden="true"></i>Equities</a>
  <a href="#fx"><i class="fas fa-coins" aria-hidden="true"></i>FX</a>
  <a href="#commodities"><i class="fas fa-bottle-water" aria-hidden="true"></i>Commodities</a>
  <a href="#real-estate"><i class="fas fa-building" aria-hidden="true"></i>Real estate</a>
  <a href="#dividend-yield-and-dividend-growth"><i class="fas fa-percentage" aria-hidden="true"></i>Dividends</a>
  <a href="#credit-spreads"><i class="fas fa-arrow-trend-up" aria-hidden="true"></i>Credit spreads</a>
  <a href="#credit-migration-and-default"><i class="fas fa-shield-halved" aria-hidden="true"></i>Credit migration</a>
  <a href="#run-it"><i class="fas fa-terminal" aria-hidden="true"></i>Run it</a>
  <a href="#references"><i class="fas fa-book" aria-hidden="true"></i>References</a>
</div>

## Equities

### Calm and Turbulent Regimes

Markets alternate between calm stretches of steady gains and turbulent ones of losses and large swings. The model is the regime-switching lognormal model of [Hardy (2001, section 3, pp. 42-43)](https://doi.org/10.1080/10920277.2001.10595984){:target="_blank"}: in regime $$k$$ the monthly log return is normal with its own mean $$\mu_k$$ and volatility $$\sigma_k$$, and a Markov chain decides each month whether to stay or switch.

<div class="fs-facts">
  <div><span>Default model</span><b>Regime-switching lognormal, two regimes</b></div>
  <div><span>Regimes timed on</span><b>A long index of each market</b></div>
  <div><span>Expected return</span><b>The US short rate plus 3.77%</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/reference/equities">Equities</a></div>
</div>

$$
\ln\frac{S_{t+\Delta t}}{S_t} \,\Big|\, s_t = k \;\sim\; N\!\left(\mu_k \Delta t,\; \sigma_k^2 \Delta t\right)
$$

A mix of a low- and a high-volatility normal has fatter tails than one normal of the same variance, regimes persist so turbulent months cluster, and drawdowns run over several months, which is what a guarantee or a funding ratio feels. Two regimes are enough: on monthly S&P 500 and TSE 300 returns a third regime barely improves the fit for the TSE 300 and only slightly for the S&P 500 (Hardy, 2001, section 3, p. 43). The regimes are estimated with the Baum-Welch algorithm and every market shares one stream of switches, so they enter and leave crises together.

### Timed on a Long Index, Scaled to the Fund

Twenty-five years of an exchange-traded fund hold two or three bear markets, too few to say how often they come and how long they last. An index with sixty to eighty years holds a dozen. So each fund's regimes are timed on a long index of its market, and the fund keeps its own average return and volatility: the index's regimes are shifted and scaled together, the same map for every regime, so that in the long run the fund's log return has exactly the mean $$m_f$$ and variance $$v_f$$ it had since 2000.

$$
m = \sum_k \pi_k \mu_k, \quad v = \sum_k \pi_k \left(\sigma_k^2 + (\mu_k - m)^2\right), \quad c = \sqrt{v_f / v}, \quad \mu'_k = m_f + c\,(\mu_k - m), \quad \sigma'_k = c\,\sigma_k
$$

Here $$\pi_k$$ are the index's long-run regime shares. The switching chances, the share of time in each regime and how far apart the regimes lie in units of volatility are the index's; the level and the size of the swings are the fund's. Today's regime is the one the fund's own recent returns point to under the scaled regimes (Hamilton's filter).

The chart shades the US market's turbulent months since 1946, and shows SPY since 2000 under the same regimes:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/markets/equity-regimes" alt="The US stock market since 1946 with its turbulent months shaded, and SPY since 2000 under the same regimes" %}

The long index behind each fund, and the regimes it gives:

| Fund | Long index that times the regimes | From | Turbulent share | Turbulent / calm spell (months) |
|:--|:--|--:|--:|--:|
| US Broad (SPY) | CRSP value-weighted US market, [Ken French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html){:target="_blank"} | 1946 | 20% | 6.3 / 25.1 |
| Small Cap (IWM) | The same market plus the size factor SMB ([Fama and French, 1993, section 2.1.2, p. 9](https://doi.org/10.1016/0304-405X(93)90023-5){:target="_blank"}) | 1946 | 27% | 8.8 / 24.2 |
| Europe (VGK) | Ken French's European market, in US dollars with dividends | 1990 | 27% | 8.9 / 23.8 |
| Japan (EWJ) | The Nikkei 225 (Yahoo Finance), a price index | 1965 | 45% | 11.3 / 13.9 |
| Emerging Markets (EEM) | The fund's own history | 2003 | 10% | 6.6 / 57.4 |

The US histories start in 1946, a judgement: stocks did badly through the falling prices of the 1930s, and with the 1929-34 bear market in the sample high inflation would look nearly harmless (see below). The Nikkei 225 has no dividends; its dividend yield adds about the same to every month, so it barely moves the timing of the regimes, the only part this history is used for.

### Turbulence Is Likelier When Inflation Is High

Stocks have done badly when inflation runs high ([Fama and Schwert, 1977, Table 5, p. 128](https://doi.org/10.1016/0304-405X(77)90014-9){:target="_blank"}): on US data since 1947 their real return was about -1.5% a year in years with inflation above 5%, against about 12% below 3%. For the US markets the chance of switching regime therefore depends on the simulated inflation, the time-varying transition probabilities of [Filardo (1994)](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}:

$$
P(s_{t+1} = j \mid s_t = i, \pi_t) = \frac{e^{\theta_{ij} + \gamma_{ij}\pi_t}}{\sum_k e^{\theta_{ik} + \gamma_{ik}\pi_t}}
$$

The intercepts $$\theta_{ij}$$ and slopes $$\gamma_{ij}$$ are fitted by the expectation-maximisation algorithm of [Diebold, Lee and Weinbach (1994, section 3)](https://doi.org/10.1093/oso/9780198773917.003.0010){:target="_blank"} on the CRSP market's monthly total return and Shiller's CPI inflation since 1946, with the regimes held at the index's own. Recent decades hold too few high-inflation years to estimate it; the history since 1946 holds the late 1940s, the 1970s and 2021-22.

For US stocks:

<div class="ca-nums fs-nums">
  <span><b>3.1%</b>chance a calm month turns turbulent at 2% inflation</span>
  <span><b>31.7%</b>the same chance at 8% inflation</span>
  <span><b>17%</b>of the time turbulent at a steady 2%</span>
  <span><b>59%</b>of the time turbulent at a steady 8%</span>
</div>

Read through the fitted model, 72% of the months since 1946 with inflation above 6% were turbulent, against 13% of those below 3%. The chart sets the fitted long-run share of turbulent months at each inflation rate against the share in history:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/markets/turbulence-inflation" alt="The fitted long-run share of turbulent months at each inflation rate, against the share in history by inflation bucket" %}

### Every Market Earns the Short Rate plus a Premium

A fund's own average return since 2000 is one draw of 25 years, and carrying it forward for decades is a view, not a fact. Each market instead earns the simulated short rate plus a long-run premium, so its expected return rises and falls with rates, as in [Hibbert, Mowbray and Turnbull (2001, section 5.2.1)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"}. The premium is 3.77% a year, equity's geometric mean return above bills across 16 countries, equally weighted, from 1870 to 2015 ([Jordà, Knoll, Kuvshinov, Schularick and Taylor, 2019, Table II](https://doi.org/10.1093/qje/qjz012){:target="_blank"}).

Each regime's mean is shifted by the same amount, so the regimes keep their spacing and the long-run geometric return is the short rate plus 3.77%:

$$
\mu'_k = \mu_k - \sum_j \pi_j \mu_j + \ln(1 + 0.0377), \qquad \ln\frac{S_{t+\Delta t}}{S_t} = (\mu'_k + r_{t+\Delta t})\,\Delta t + \sigma_k \sqrt{\Delta t}\,z_t
$$

The premium is geometric because the model compounds log returns; Table II's arithmetic premium of 5.85% with a volatility of 21.27% gives about 3.6% geometric, close to its geometric 3.77%. Every fund is listed in US dollars, so every one earns the US short rate (the Taylor-rule rate), as interest-rate parity implies for an investor holding them in dollars.

### How Each Number Is Set

Every equity number, what kind it is and why:

| Number | Value | Kind | Why |
|:--|:--|:--|:--|
| Regimes | 2 | Judgement | A third adds little to the fit ([Hardy, 2001, section 3, p. 43](https://doi.org/10.1080/10920277.2001.10595984){:target="_blank"}) |
| Shared regimes | One stream for every market | Judgement | Markets enter and leave crises together, which brings simulated equity correlations close to the fitted ones ([Ahlgrim, D'Arcy and Gorvett, 2005, section 3](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}) |
| Long indices and their starts | Table above | Judgement | The longest monthly index of each market that is keyless |
| US start year | 1946 | Judgement | After the deflation of the 1930s |
| Regime means, volatilities, switching | Per fund | Fitted | Baum-Welch on the index, scaled to the fund's mean and variance since 2000 |
| Inflation slopes $$\gamma$$ (US Broad, Small Cap) | +0.45 and +0.20 on the log-odds of a calm month turning turbulent, per point of inflation | Fitted | Expectation-maximisation, CRSP market and Shiller CPI since 1946 |
| Equity premium | 3.77% (geometric) | Sourced | [Jordà et al. (2019, Table II)](https://doi.org/10.1093/qje/qjz012){:target="_blank"} |
| Risk-free part | The simulated US short rate | Model choice | Dollar-listed funds; interest-rate parity |

### Other Equity Models

Four other equity models are options:

| Model | What it does |
|:--|:--|
| Returns above cash ([Hibbert, Mowbray and Turnbull, 2001](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"}) | The regimes fitted on returns in excess of a short rate, with the simulated short rate added back. |
| Price from dividends ([Wilkie, 1986](https://doi.org/10.1017/S0071368600009009){:target="_blank"}) | The dividend index over the dividend yield, the last link of Wilkie's cascade. |
| KNW | The equity leg of the [KNW model](/projects/financescenarios/docs/knw), with stochastic volatility shared with rates and inflation. |
| Risk-neutral | For valuing options and guarantees, a geometric Brownian motion drifting at the short rate less the dividend yield, with an implied, SVI, realised or Heston volatility; the [Equities reference](/projects/financescenarios/docs/reference/equities) has the sources. |

<div class="fs-ref"><a href="/projects/financescenarios/docs/reference/equities"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Equities API</a></div>

## FX

### Purchasing Power Parity for the Euro and the Pound

Over a few years an exchange rate moves like a random walk, but over decades it is pulled back toward purchasing power parity: a currency that buys much more abroad than it usually does loses that edge. The studies [Rogoff (1996, section 5.B, p. 656)](https://ideas.repec.org/a/aea/jeclit/v34y1996i2p647-668.html){:target="_blank"} surveys agree on a half-life of three to five years for real exchange rates, and cross-country panels find about four (section 5.C, p. 657). The default takes four years.

<div class="fs-facts">
  <div><span>Series</span><b>Each currency against the US dollar</b></div>
  <div><span>Data</span><b>BIS end-of-month rates, OECD consumer prices</b></div>
  <div><span>Default model</span><b>Purchasing power parity for the euro and the pound; a random walk for the yen</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/reference/fx">FX</a></div>
</div>

The real exchange rate is the nominal rate (foreign currency per US dollar) adjusted for the two price levels, $$q_t = \ln S_t - \ln(P^f_t / P^{us}_t)$$. It reverts to its average since 2000 at $$\kappa = \ln 2 / 4 = 0.173$$ a year, and the nominal rate also moves with the two simulated inflation rates:

$$
q_{t+\Delta t} = \bar q + (q_t - \bar q)\,e^{-\kappa\Delta t} + \sigma\sqrt{\frac{1 - e^{-2\kappa\Delta t}}{2\kappa}}\;z_t, \qquad S_{t+\Delta t} = S_t \exp\!\left((\pi^f_t - \pi^{us}_t)\,\Delta t + q_{t+\Delta t} - q_t\right)
$$

The volatility $$\sigma$$ is the nominal rate's monthly volatility since 2000: the short-run volatility of real exchange rates is of the same order as that of nominal ones (Rogoff, 1996, section 1, p. 647). The rates are the Bank for International Settlements' end-of-month rates ([BIS](https://data.bis.org/topics/XRU){:target="_blank"}); changes of monthly averages would keep only about two thirds of a random walk's variance ([Working, 1960](https://doi.org/10.2307/1907574){:target="_blank"}). The price indices are the OECD's consumer price indices of the United States, Germany (for the euro, as the euro area's inflation series) and the United Kingdom.

The chart shows the euro and pound real exchange rates since 2000 against their average, with the expected pull back at a four-year half-life:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/markets/fx-ppp" alt="The euro and pound real exchange rates since 2000 against their average, with the expected pull back at a four-year half-life" %}

Today, in real terms, the dollar buys more than its average since 2000:

<div class="ca-nums fs-nums">
  <span><b>11%</b>more euros</span>
  <span><b>10%</b>more pounds</span>
</div>

The median scenario has the dollar losing half of that edge in four years.

### No Trend for the Yen

The yen has no Japanese inflation series in the default to measure its real rate against, so it is a random walk with no trend: its drift is $$\sigma^2/2$$, so the median stays at today's rate. A random walk forecasts exchange rates at least as well as structural models ([Meese and Rogoff, 1983, section 4, Table 1, p. 13](https://doi.org/10.1016/0022-1996(83)90017-X){:target="_blank"}), and a fitted trend would carry a currency view forward for decades.

How each FX number is set:

| Number | Value | Kind | Why |
|:--|:--|:--|:--|
| Half-life of the real rate | 4 years | Sourced | [Rogoff (1996, sections 5.B and 5.C, pp. 656-657)](https://ideas.repec.org/a/aea/jeclit/v34y1996i2p647-668.html){:target="_blank"} |
| Anchor $$\bar q$$ | The average real rate since 2000 | Judgement | The calibration window; today's distance from it is -0.105 (euro) and -0.095 (pound) in logs |
| Volatility | Euro 9.3%, pound 8.6%, yen 9.3% a year | Fitted | End-of-month rates since 2000 |
| Yen | Random walk | Sourced | [Meese and Rogoff (1983, section 4, Table 1, p. 13)](https://doi.org/10.1016/0022-1996(83)90017-X){:target="_blank"} |

Other drifts are options: the sample's own trend, or uncovered interest-rate parity, $$d\ln S_t = (r^f_t - r^{us}_t - \tfrac{1}{2}\sigma^2)\,dt + \sigma\,dW_t$$, which [Fama (1984, Table 2, p. 326)](https://doi.org/10.1016/0304-3932(84)90046-1){:target="_blank"} finds history does not support.

<div class="fs-ref"><a href="/projects/financescenarios/docs/reference/fx"><i class="fas fa-book" aria-hidden="true"></i>Full reference: FX API</a></div>

## Commodities

### Gold: A Random Walk in Real Terms

Gold has no level its real price returns to. About 2,500 tonnes are mined a year, some 1.5% of the 171,300 tonnes above ground, so supply barely responds to price ([Erb and Harvey, 2013, pp. 28-29](https://doi.org/10.2469/faj.v69.n4.1){:target="_blank"}); the "golden constant" of a long-run real return near zero rests on centuries of data (p. 11), while the real price swings as much as the nominal one (p. 12), and a pull fitted on a short sample rests on one episode (p. 15). A mean-reverting fit on gold futures since 2000 settles at about 24,000 USD an ounce with a 21-year half-life: no credible level.

<div class="fs-facts">
  <div><span>Gold</span><b>A random walk in real terms</b></div>
  <div><span>Brent</span><b>One-factor mean reversion in logs</b></div>
  <div><span>Alternative</span><b>Schwartz-Smith two factor</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/reference/commodities">Commodities</a></div>
</div>

The default therefore makes gold a random walk in real terms: it keeps pace with the simulated US inflation and adds a drift of $$\sigma^2/2$$, so its median real price stays flat:

$$
S_{t+\Delta t} = S_t \exp\!\left(\pi_t\,\Delta t + \sigma\sqrt{\Delta t}\,z_t\right)
$$

The volatility, 17.9% a year, comes from the daily gold futures price (GC=F) since 2000. The chart shows gold's price in today's US dollars an ounce since 1971:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/markets/gold-real" alt="Gold's price in today's US dollars an ounce since 1971" %}

### Brent: Pulled toward a Level

An oil price is pulled toward a level set by the cost of production: high prices bring new supply, low prices cut it. The log price follows the one-factor model of [Schwartz (1997)](https://doi.org/10.1111/j.1540-6261.1997.tb02721.x){:target="_blank"}, which keeps the price positive:

$$
dX_t = a(\theta - X_t)\,dt + \sigma\,dW_t, \qquad X_t = \ln S_t
$$

Fitted on daily Brent futures (BZ=F) since July 2007, the long-run median $$e^{\theta}$$ is 77 USD a barrel, a shock halves in 12 months, and the volatility is 38.3% a year. Brent rather than WTI: the WTI front-month future closed at -37.63 USD on 20 April 2020, a price the log model cannot take. The chart shows Brent since 1990 with the fitted long-run median:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/markets/brent" alt="Brent crude since 1990 with the fitted long-run median" %}

How each commodity number is set:

| Number | Value | Kind | Why |
|:--|:--|:--|:--|
| Gold model | Random walk in real terms | Sourced | [Erb and Harvey (2013, pp. 11-15, 28-29)](https://doi.org/10.2469/faj.v69.n4.1){:target="_blank"} |
| Gold volatility | 17.9% | Fitted | Daily GC=F since 2000 |
| Brent level, speed, volatility | 77 USD, 0.67 a year, 38.3% | Fitted | Daily BZ=F since July 2007, [Schwartz (1997)](https://doi.org/10.1111/j.1540-6261.1997.tb02721.x){:target="_blank"} |

The two-factor model of [Schwartz and Smith (2000)](https://doi.org/10.1287/mnsc.46.7.893.12034){:target="_blank"}, a short-term deviation that fades plus a long-term level that drifts, fitted to the futures curve, is an option, also risk-neutral.

<div class="fs-ref"><a href="/projects/financescenarios/docs/reference/commodities"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Commodities API</a></div>

## Real Estate

House-price growth, not the price level, reverts to a long-run rate, as in eq. 3.18 of [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf#page=21){:target="_blank"}: a price index has no level to return to over decades, and booms fade in growth while leaving a mark on the level. In the default, growth also responds to the long rate a year earlier. Higher rates make mortgages dearer and cool the housing market with a delay: [Iacoviello (2005, section I, Figure 1, p. 741)](https://doi.org/10.1257/0002828054201477){:target="_blank"} finds that tighter money lowers real house prices in US data from 1974 to 2003.

<div class="fs-facts">
  <div><span>Series</span><b>US house-price growth over the past year</b></div>
  <div><span>Data</span><b>OECD house prices and the OECD US 10-year rate</b></div>
  <div><span>Model</span><b>Mean-reverting growth, linked to the long rate a year earlier</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/reference/real-estate">Real estate</a></div>
</div>

$$
g_{t+\Delta t} = \theta + (g_t - \theta)\,e^{-a\Delta t} + w\,\beta\,\Delta L_{t-\ell} + \sigma\sqrt{\frac{1 - e^{-2a\Delta t}}{2a}}\;z_t
$$

Here $$g_t$$ is US house-price growth over the past year (the OECD's nominal house price index), $$\Delta L_{t-\ell}$$ the simulated US long rate's change $$\ell$$ = 1 year earlier, and $$w$$ spreads a yearly sensitivity over the steps. The sensitivity is fitted on the longest record, from 1971: each quarter's growth regressed on its own value a year earlier and the long rate's change over the year ending a year earlier,

$$
g_t = c + Q\,g_{t-4} + \beta\,(L_{t-4} - L_{t-8}) + e_t
$$

which gives $$\beta$$ = -0.86: a 1-point rise in the long rate slows house-price growth by about 0.86 points a year later. Scanning the lag from 0 to 8 quarters, four explains the most (a partial R² of 8%), with three quarters close behind. The chart plots house-price growth against the long rate's change a year earlier, and the sensitivity at every lag from 0 to 8 quarters:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/markets/house-prices-rates" alt="US house-price growth against the long rate's change a year earlier with the fitted line, and the sensitivity at every lag from 0 to 8 quarters" %}

How each real-estate number is set:

| Number | Value | Kind | Why |
|:--|:--|:--|:--|
| Lag | 4 quarters | Judgement | The lag that explains the most on US data since 1971 (chart) |
| Sensitivity $$\beta$$ | -0.86 (standard error 0.20) | Fitted | OECD house prices and the OECD US 10-year rate, 1973Q1-2026Q2 |
| Minimum sample | 80 quarters | Judgement | Twenty years before the link is fitted |
| Speed, long-run growth, volatility | 0.37 a year, 4.3%, 4.8% | Fitted | OECD US house prices since 2000, read a year apart; the volatility net of what the link explains, keeping at least half of it |

The path is price growth only; rental income is added when real estate is held as an asset (see [portfolio](/projects/financescenarios/docs/portfolio#what-a-portfolio-can-hold)).

<div class="fs-ref"><a href="/projects/financescenarios/docs/reference/real-estate"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Real estate API</a></div>

## Dividend Yield and Dividend Growth

### Dividend Yield {#dividend-yield}

When dividend income matters on its own, the yield is simulated separately from the equity's total return. Following eq. 3.17 of [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf#page=20){:target="_blank"}, who follow [Wilkie (1986)](https://doi.org/10.1017/S0071368600009009){:target="_blank"} and [Hibbert, Mowbray and Turnbull (2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"}, the log of the yield mean-reverts, so the yield stays positive:

$$
d\ln y_t = a(\theta - \ln y_t)\,dt + \sigma\,dW_t
$$

SPY on 2026-10-04:

<div class="ca-nums fs-nums">
  <span><b>0.99%</b>starting yield</span>
  <span><b>1.39%</b>long-run yield</span>
  <span><b>4.7 years</b>half-life of a gap</span>
</div>

On 1871-2003 data the paper found the speed statistically indistinguishable from zero, so a short window may show no reversion at all. A belief about the normal level is a log too ($$\ln 0.02$$ for 2%). An optional term on the same step's change in inflation, as in Wilkie, links the yield to inflation.

### Dividend Growth (Wilkie)

[Wilkie's (1986)](https://doi.org/10.1017/S0071368600009009){:target="_blank"} model is a one-way cascade: inflation, then dividend yield, dividend growth and the share price (dividend index divided by yield). Dividend growth is his "Reduced Standard Basis" equation ([section 3.9](https://doi.org/10.1017/S0071368600009009){:target="_blank"}), a slightly simpler form that he found gives very similar long-term results, with $$\Delta\ln Q_t$$ the force of inflation (the log change in the price index):

$$
\Delta \ln D_t = \mu_D + w\,M_t + x\,\Delta\ln Q_t + y\,\varepsilon^Y_{t-1} + \sigma_D\,z_t, \qquad w + x = 1
$$

Term by term:

| Term | Wilkie | Economics |
|:-----|:-------|:----------|
| $$\mu_D$$ | DMU | Real dividend growth |
| $$w\,M_t$$ | DW | Smoothed inflation, $$M_t = 0.2\,\Delta\ln Q_t + 0.8\,M_{t-1}$$ a year: dividends catch up with prices over time |
| $$x\,\Delta\ln Q_t$$ | DX | Part of this period's inflation passes straight into dividends |
| $$y\,\varepsilon^Y_{t-1}$$ | DY | Last period's dividend yield surprise: prices anticipate dividend changes, so the yield moves first |
| $$\sigma_D\,z_t$$ | DSD | The dividend index's own shock |

The two inflation weights add up to one, Wilkie's unit gain ([section 3.7](https://doi.org/10.1017/S0071368600009009){:target="_blank"}): in the long run dividends, and so share prices, keep their real value. The fit imposes it, fixes the smoothing weight at Wilkie's 0.2 a year (converted to the data's step) and estimates the rest by one regression.

The whole cascade runs one way, from inflation to the share price:

<div class="fs-diagram">
<div class="fs-links">
  <div class="fs-links__row">
    <div class="fs-node is-accent"><b>Inflation</b></div>
    <div class="fs-links__to">
      <div class="fs-link"><em>optional</em><div class="fs-node"><b>Dividend yield</b></div></div>
      <div class="fs-link"><em></em><div class="fs-node"><b>Dividend growth</b></div></div>
    </div>
  </div>
  <div class="fs-links__row">
    <div class="fs-node"><b>Dividend yield</b></div>
    <div class="fs-links__to">
      <div class="fs-link"><em>last surprise</em><div class="fs-node"><b>Dividend growth</b></div></div>
      <div class="fs-link"><em></em><div class="fs-node"><b>Share price</b><small>dividend index over yield</small></div></div>
    </div>
  </div>
  <div class="fs-links__row">
    <div class="fs-node"><b>Dividend growth</b></div>
    <div class="fs-links__to">
      <div class="fs-link"><em></em><div class="fs-node"><b>Share price</b><small>dividend index over yield</small></div></div>
    </div>
  </div>
</div>
</div>

Wilkie fitted 1919-1982 UK data; the shipped Wilkie factor set applies the same equations to US data.

<div class="fs-ref"><a href="/projects/financescenarios/docs/reference/dividend-yield"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Dividend yield API</a></div>
<div class="fs-ref"><a href="/projects/financescenarios/docs/reference/dividend-growth"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Dividend growth API</a></div>

## Credit Spreads

A credit spread is the extra yield a company pays over government debt: expected default losses plus a risk and liquidity premium that widens sharply in a downturn. The spread reverts to a normal level as an Ornstein-Uhlenbeck process. Fitting it in logs is a modeling judgement rather than a published specification: it keeps the spread positive and makes its swings proportional to its level, so wide spreads are the most volatile and the distribution is skewed toward sharp widenings:

$$
d\ln s_t = a(\theta - \ln s_t)\,dt + \sigma\,dW_t
$$

<div class="fs-facts">
  <div><span>Model</span><b>Mean reversion in logs (Ornstein-Uhlenbeck)</b></div>
  <div><span>Data</span><b>ICE BofA, Moody's, Bundesbank, RBA, ECB</b></div>
  <div><span>Longest US history</span><b>Moody's, monthly from 1953</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/reference/credit">Credit</a></div>
</div>

A series that has touched zero or below is fitted on its level instead. The 7-10 year investment-grade spread on 2026-10-04:

<div class="ca-nums fs-nums">
  <span><b>1.05%</b>starting spread</span>
  <span><b>1.01%</b>long-run median</span>
  <span><b>3 months</b>half-life of a gap</span>
</div>

That speed comes from three years of monthly data, too few for a reliable estimate, and short samples tend to overstate how fast a series reverts; the Moody's series, monthly from 1953, gives a steadier read. Business-cycle conditioning lets spreads widen as a simulated path turns down, but that variant, like GARCH volatility, is fitted on the spread level rather than its log, so it can turn negative.

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

For a whole spread curve rather than buckets, see the [credit term structure API](/projects/financescenarios/docs/reference/credit-term-structure).

<div class="fs-ref"><a href="/projects/financescenarios/docs/reference/credit"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Credit API</a></div>

## Credit Migration and Default

Spreads price credit risk; migration models the events: downgrades, defaults and losses on a bond portfolio by rating. Each borrower's credit quality is a standard normal variable: a shared credit cycle $$Z$$ with weight $$\sqrt{\rho}$$, for asset correlation $$\rho$$, plus the borrower's own luck. A through-the-cycle transition matrix sets each rating's thresholds for upgrade, downgrade and default. In a year with cycle $$Z$$, a rating with long-run default probability $$p$$ defaults with probability

$$
p(Z) = \Phi\!\left(\frac{\Phi^{-1}(p) - \sqrt{\rho}\,Z}{\sqrt{1-\rho}}\right)
$$

where $$\Phi$$ is the standard normal distribution function. The same shift applies to every threshold, so a bad year ($$Z$$ below zero) moves every rating toward downgrade and default at once. This is the one-factor approach of [Kim (1999)](https://www.msci.com/www/research-report/a-way-to-condition-transition/018440984){:target="_blank"}, in the Markov rating framework of [Jarrow, Lando and Turnbull (1997)](https://doi.org/10.1093/rfs/10.2.481){:target="_blank"}, and the same formula that underlies the Basel IRB capital charge.

<div class="fs-facts">
  <div><span>Model</span><b>One-factor credit cycle on a rating transition matrix</b></div>
  <div><span>Data</span><b>ESMA CEREP rating statistics</b></div>
  <div><span>PD floor</span><b>0.05%, the CRR3 corporate PD floor</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/reference/credit-migration">Credit migration</a></div>
</div>

The data are ESMA's [CEREP](https://registers.esma.europa.eu/cerep-publication){:target="_blank"} rating agency statistics, which lag one to two years. The cycle is backed out year by year from default rates, then simulated as mean-reverting around zero (the through-the-cycle average) and correlated with the other factors. Every rating's long-run default probability is floored at 0.05%, so one that never defaulted in the sample still carries some risk. That is the corporate PD input floor of CRR3 ([Regulation (EU) 2024/1623, Article 1, point (86)(a)](https://eur-lex.europa.eu/eli/reg/2024/1623/oj/eng){:target="_blank"}), which from 2025 replaced the 0.03% of the original [CRR Article 160(1)](https://eur-lex.europa.eu/eli/reg/2013/575/oj){:target="_blank"}.

The 0.03% floor remains available for a Basel II comparison. The transition matrix pools the rating changes of every year in the history, not only the latest ones, so it reflects an average year across good and bad ones, as Basel asks of PD estimation: the longest relevant observation period, with a representative mix of good and bad years ([Basel Framework, CRE36.79](https://www.bis.org/basel_framework/chapter/CRE/36.htm){:target="_blank"}).

On S&P corporate ratings from 2000 to 2025:

<div class="ca-nums fs-nums">
  <span><b>0.10</b>asset correlation</span>
  <span><b>8 months</b>half-life of a shock to the cycle</span>
</div>

The worst years came out as 2009, 2001, 2020 and 2002.

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
credit_migration:
  enabled: true
  agency: S&P
```

With migration enabled, a portfolio's ratings, defaults and losses follow from each scenario:

```python
from financescenarios import rating_migration

# share in each rating, defaults and loss after 40% recovery, per scenario and year
migration = rating_migration(result, {"A": 40, "BBB": 50, "BB": 10}, recovery_rate=0.4)
migration.summary()
```

<div class="fs-callout fs-callout--limits" markdown="1">
<p class="fs-callout__title">Limits</p>

- Spreads are not derived from the ratings: model them separately as [credit spreads](#credit-spreads).
- Recovery is fixed rather than falling in downturns.
- One cycle drives all sectors and regions.
</div>

<div class="fs-ref"><a href="/projects/financescenarios/docs/reference/credit-migration"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Credit migration API</a></div>

## Run It

Calibrating the default settings and factor set gives every number on this page, and a run checks them against history:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(api_key="FINANCIAL_MODELING_PREP_KEY")  # the default settings and factor set
calibration = scenarios.calibrate()

calibration.calibrated_params["us_broad"]  # the scaled regimes, the premium shift and the inflation-driven switching
calibration.calibrated_params["eur"]  # the purchasing power parity speed and today's distance from the anchor
calibration.calibrated_params["real_estate"]  # growth's reversion and its link to the long rate

result = scenarios.simulate(calibration=calibration, n_simulations=2000, seed=42)
scenarios.check_relationships(result)  # do stocks do worse when inflation is high, as in history?
```

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">15</span></summary>

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. [casact.org](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}
- Diebold, F.X., Lee, J.-H., Weinbach, G.C. (1994). "Regime Switching with Time-Varying Transition Probabilities." In Hargreaves, C. (ed.), Nonstationary Time Series Analysis and Cointegration, 283-302. [doi.org](https://doi.org/10.1093/oso/9780198773917.003.0010){:target="_blank"}
- Erb, C.B., Harvey, C.R. (2013). "The Golden Dilemma." Financial Analysts Journal, 69(4), 10-42. [doi.org](https://doi.org/10.2469/faj.v69.n4.1){:target="_blank"}
- Fama, E.F., French, K.R. (1993). "Common Risk Factors in the Returns on Stocks and Bonds." Journal of Financial Economics, 33(1), 3-56. [doi.org](https://doi.org/10.1016/0304-405X(93)90023-5){:target="_blank"}
- Fama, E.F., Schwert, G.W. (1977). "Asset Returns and Inflation." Journal of Financial Economics, 5(2), 115-146. [doi.org](https://doi.org/10.1016/0304-405X(77)90014-9){:target="_blank"}
- Filardo, A.J. (1994). "Business-Cycle Phases and Their Transitional Dynamics." Journal of Business & Economic Statistics, 12(3), 299-308. [doi.org](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}
- French, K.R. Data Library. [dartmouth.edu](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html){:target="_blank"}
- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. [doi.org](https://doi.org/10.1080/10920277.2001.10595984){:target="_blank"}
- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert Limited. [ressources-actuarielles.net](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"}
- Iacoviello, M. (2005). "House Prices, Borrowing Constraints, and Monetary Policy in the Business Cycle." American Economic Review, 95(3), 739-764. [doi.org](https://doi.org/10.1257/0002828054201477){:target="_blank"}
- Jordà, Ò., Knoll, K., Kuvshinov, D., Schularick, M., Taylor, A.M. (2019). "The Rate of Return on Everything, 1870-2015." Quarterly Journal of Economics, 134(3), 1225-1298. [doi.org](https://doi.org/10.1093/qje/qjz012){:target="_blank"}
- Meese, R.A., Rogoff, K. (1983). "Empirical Exchange Rate Models of the Seventies: Do They Fit Out of Sample?" Journal of International Economics, 14(1-2), 3-24. [doi.org](https://doi.org/10.1016/0022-1996(83)90017-X){:target="_blank"}
- Rogoff, K. (1996). "The Purchasing Power Parity Puzzle." Journal of Economic Literature, 34(2), 647-668. [ideas.repec.org](https://ideas.repec.org/a/aea/jeclit/v34y1996i2p647-668.html){:target="_blank"}
- Schwartz, E.S. (1997). "The Stochastic Behavior of Commodity Prices: Implications for Valuation and Hedging." The Journal of Finance, 52(3), 923-973. [doi.org](https://doi.org/10.1111/j.1540-6261.1997.tb02721.x){:target="_blank"}
- Working, H. (1960). "Note on the Correlation of First Differences of Averages in a Random Chain." Econometrica, 28(4), 916-918. [doi.org](https://doi.org/10.2307/1907574){:target="_blank"}

</details>
