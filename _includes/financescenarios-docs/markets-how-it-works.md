## How It Works

This page explains the theory of each, then derives every number: what it is, whether it comes from a published source, a fit on data or a judgement, and the chart that shows it. The numbers come from one calibration of the default settings and factor set, made on 19 October 2026. [Interest rates](/projects/financescenarios/docs/interest-rates) and [the economy](/projects/financescenarios/docs/economy) have their own pages, and every option is in the [reference](#reference) at the end of this page.

### Equities {#equity-markets}

#### Calm and Turbulent Regimes

Markets alternate between calm stretches of steady gains and turbulent ones of losses and large swings. The model is the regime-switching lognormal model of [Hardy (2001, section 3, pp. 42-43)](https://doi.org/10.1080/10920277.2001.10595984){:target="_blank"}: in regime $$k$$ the monthly log return is normal with its own mean $$\mu_k$$ and volatility $$\sigma_k$$, and a Markov chain decides each month whether to stay or switch.

<div class="fs-facts">
  <div><span>Default model</span><b>Regime-switching lognormal, two regimes</b></div>
  <div><span>Regimes timed on</span><b>A long index of each market</b></div>
  <div><span>Expected return</span><b>The US short rate plus 3.77%</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/markets">Equities</a></div>
</div>

$$
\ln\frac{S_{t+\Delta t}}{S_t} \,\Big|\, s_t = k \;\sim\; N\!\left(\mu_k \Delta t,\; \sigma_k^2 \Delta t\right)
$$

A mix of a low- and a high-volatility normal has fatter tails than one normal of the same variance, regimes persist so turbulent months cluster, and drawdowns run over several months, which is what a guarantee or a funding ratio feels. Two regimes are enough: on monthly S&P 500 and TSE 300 returns a third regime barely improves the fit for the TSE 300 and only slightly for the S&P 500 (Hardy, 2001, section 3, p. 43). The regimes are estimated with the Baum-Welch algorithm and every market shares one stream of switches, so they enter and leave crises together.

#### Timed on a Long Index, Fitted on the Fund

Twenty-five years of an exchange-traded fund hold two or three bear markets, too few to say how often they come and how long they last. An index with sixty to eighty years holds a dozen. So the long index of each market sets how the market switches: its chances of staying calm or turbulent, and with them the share of time in each regime and the length of a spell, are fitted on the index and then held fixed. The fund sets the rest. Each regime's mean and volatility are Hardy's model fitted on the fund's own monthly log returns $$r_t$$ by maximum likelihood under the index's switching: the expectation-maximisation algorithm with only the means and volatilities free. Hamilton's filter and smoother give each month's chance $$w_{tk}$$ of each regime, each regime takes the weighted mean and variance of the returns, and the two steps repeat until the likelihood stops rising:

$$
w_{tk} = P(s_t = k \mid r_1, \dots, r_T), \qquad \mu_k = \frac{1}{\Delta t}\,\frac{\sum_t w_{tk}\, r_t}{\sum_t w_{tk}}, \qquad \sigma_k^2 = \frac{1}{\Delta t}\,\frac{\sum_t w_{tk}\,(r_t - \mu_k \Delta t)^2}{\sum_t w_{tk}}
$$

The fit starts from the index's regimes shifted and scaled to the fund's mean and variance. It is the published estimator ([Hardy, 2001, section 3](https://doi.org/10.1080/10920277.2001.10595984){:target="_blank"}; [Hamilton, 1989](https://doi.org/10.2307/1912559){:target="_blank"}) with one constraint, the index's switching, rather than a map of the index's regimes onto the fund. Today's regime is the one the fund's own recent returns point to.

The fund's twenty-odd years then set each regime's level and swings on their own, and that has a cost for Japan. On year-end backtests from 2000 to 2022, four years ahead, EWJ's CRPS skill on the 18 holdout origins fell from +0.25 under the earlier shift-and-scale map to +0.06, while Europe's rose from +0.25 to +0.34 and the US funds' held (the scores are explained on the [validation page](/projects/financescenarios/docs/validation)).

The chart shades the US market's turbulent months since 1946, and shows SPY since 2000 under the same switching, with each regime's level and swings fitted on SPY's own returns:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/markets/equity-regimes" alt="The US stock market since 1946 with its turbulent months shaded, and SPY since 2000 under the same switching with its regimes fitted on its own returns" %}

The long index behind each fund, and the regimes it gives:

| Fund | Long index that times the regimes | From | Turbulent share | Turbulent / calm spell (months) |
|:--|:--|--:|--:|--:|
| US Broad (SPY) | CRSP value-weighted US market, [Ken French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html){:target="_blank"} | 1946 | 20% | 6.3 / 25.1 |
| Small Cap (IWM) | The same market plus the size factor SMB ([Fama and French, 1993, section 2.1.2, p. 9](https://doi.org/10.1016/0304-405X(93)90023-5){:target="_blank"}) | 1946 | 27% | 8.8 / 24.2 |
| Europe (VGK) | Ken French's European market, in US dollars with dividends | 1990 | 27% | 8.9 / 23.8 |
| Japan (EWJ) | The Nikkei 225 (Yahoo Finance), a price index | 1965 | 45% | 11.4 / 14.0 |
| Emerging Markets (EEM) | The fund's own history | 2003 | 10% | 6.6 / 57.4 |

The two US funds switch with inflation (next section), so their share and spells depend on it; the table gives them at the average inflation of each fund's own years. With the switching held fixed, the CRSP market since 1946 is turbulent 28% of months, in spells of 8.2 months against 21.1 calm (the chart).

The US histories start in 1946, a judgement: stocks did badly through the falling prices of the 1930s, and with the 1929-34 bear market in the sample high inflation would look nearly harmless (see below). The Nikkei 225 has no dividends; its dividend yield adds about the same to every month, so it barely moves the timing of the regimes, the only part this history is used for.

#### Turbulence Is Likelier When Inflation Is High

Stocks have done badly when inflation runs high ([Fama and Schwert, 1977, Table 5, p. 128](https://doi.org/10.1016/0304-405X(77)90014-9){:target="_blank"}): on US data since 1947 their real return was about -1.5% a year in years with inflation above 5%, against about 12% below 3%. For the US markets the chance of switching regime therefore depends on the simulated inflation, the time-varying transition probabilities of [Filardo (1994)](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}:

$$
P(s_{t+1} = j \mid s_t = i, \pi_t) = \frac{e^{\theta_{ij} + \gamma_{ij}\pi_t}}{\sum_k e^{\theta_{ik} + \gamma_{ik}\pi_t}}
$$

The intercepts $$\theta_{ij}$$ and slopes $$\gamma_{ij}$$ are fitted by the expectation-maximisation algorithm of [Diebold, Lee and Weinbach (1994, section 3)](https://doi.org/10.1093/oso/9780198773917.003.0010){:target="_blank"} on the CRSP market's monthly total return and Shiller's CPI inflation since 1946, with the regimes held at the index's own: the E-step reads each month's regime chances through the switching at that month's inflation, and the M-step refits each row's logit on those chances, so regimes and switching come from one likelihood. Recent decades hold too few high-inflation years to estimate it; the history since 1946 holds the late 1940s, the 1970s and 2021-22.

For US stocks:

<div class="ca-nums fs-nums">
  <span><b>3.1%</b>chance a calm month turns turbulent at 2% inflation</span>
  <span><b>31.7%</b>the same chance at 8% inflation</span>
  <span><b>17%</b>of the time turbulent at a steady 2%</span>
  <span><b>59%</b>of the time turbulent at a steady 8%</span>
</div>

Read through the fitted model, 72% of the months since 1946 with inflation above 6% were turbulent, against 13% of those below 3%. The chart sets the fitted long-run share of turbulent months at each inflation rate against the share in history:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/markets/turbulence-inflation" alt="The fitted long-run share of turbulent months at each inflation rate, against the share in history by inflation bucket" %}

#### Every Market Earns the Short Rate plus a Premium

A fund's own average return since 2000 is one draw of 25 years, and carrying it forward for decades is a view, not a fact. Each market instead earns the simulated short rate plus a long-run premium, so its expected return rises and falls with rates, as in [Hibbert, Mowbray and Turnbull (2001, section 5.2.1)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"}. The premium is 3.77% a year, equity's geometric mean return above bills across 16 countries, equally weighted, from 1870 to 2015 ([Jordà, Knoll, Kuvshinov, Schularick and Taylor, 2019, Table II](https://doi.org/10.1093/qje/qjz012){:target="_blank"}).

Each regime's mean is shifted by the same amount, so the regimes keep their spacing and the long-run geometric return is the short rate plus 3.77%:

$$
\mu'_k = \mu_k - \sum_j \pi_j \mu_j + \ln(1 + 0.0377), \qquad \ln\frac{S_{t+\Delta t}}{S_t} = (\mu'_k + r_t)\,\Delta t + \sigma_k \sqrt{\Delta t}\,z_t
$$

The premium is geometric because the model compounds log returns; Table II's arithmetic premium of 5.85% with a volatility of 21.27% gives about 3.6% geometric, close to its geometric 3.77%. Every fund is listed in US dollars, so every one earns the US short rate (the policy-rule rate of the [interest rates page](/projects/financescenarios/docs/interest-rates)), as interest-rate parity implies for an investor holding them in dollars. The rate is the one at the start of each step, $$r_t$$, known when the step begins, as discounting and the risk-neutral steps read it; the rate at the end of the step would add a correlation between the step's return and the rate's own shock that no data show.

#### Earning the Premium over the Run's Own Inflation

For the US funds the shares $$\pi_j$$ in that shift are not fixed: they depend on the inflation the scenarios simulate. Taking them at one inflation level, the average over the fund's own years, leaves something out. The switching is a logit in inflation, and it is convex: the months of high inflation add more turbulence than the months of low inflation take away. A run then spends more time turbulent than that one level suggests, and earns less than the premium. Jordà et al.'s premium is an average over every inflation history saw, so the model should earn it on average over the inflation it simulates.

The shift is therefore set on the shares the run's own inflation gives, a simulated method of moments ([McFadden, 1989](https://doi.org/10.2307/1913621){:target="_blank"}; [Duffie and Singleton, 1993](https://doi.org/10.2307/2951768){:target="_blank"}). A pilot run simulates the calibrated US inflation alone, 2,000 paths of 100 years, and carries the expected regime probabilities along every path; the shares are their average after the first 30 years, once today's regime and inflation have worn off:

$$
p_{t+1} = p_t\,P(\pi_t), \qquad \pi^{\text{sim}} = \frac{1}{N\,(T - T_0)} \sum_{n=1}^{N} \sum_{t > T_0} p^{(n)}_t
$$

where $$P(\pi_t)$$ is the switching matrix at path $$n$$'s inflation in month $$t$$. The regime chain itself is never drawn, so the only sampling noise is inflation's.

On this calibration the pilot's inflation averages 2.3% and is above 5% in 12% of months. Along it US stocks are turbulent 21.1% of the time, against 20.2% at the inflation of SPY's own years. The gap looks small, but the regimes lie far apart: with the shift at 20.2%, the default's US stocks earn 3.44% a year over the short rate instead of the 3.70% that 3.77% promises (ln 1.0377). The known answer is the default run itself. Over 2,000 scenarios of 30 years, US stocks earn a mean log return over the simulated short rate of 3.70% (standard error 0.07%), the target within one standard error; the shift at the fund's years' shares misses it by 3.5 standard errors. Small caps follow inflation less steeply: they are turbulent 26.6% of the time along simulated inflation and 26.7% at their own years' level, and earn 3.75% (standard error 0.09%).

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/markets/equity-premium" alt="The expected share of turbulent months along the pilot run of US inflation against the share at the fund's own years' inflation, and the mean log return over the short rate of US stocks in 30-year runs with each shift" %}

The gap grows with simulated inflation: before US inflation was anchored on its long-run mean (see [the economy page](/projects/financescenarios/docs/economy)), the run's higher inflation kept US stocks turbulent 24% of the time and the old shift earned about 2.7% a year.

#### How Each Number Is Set

Every equity number, what kind it is and why:

| Number | Value | Kind | Why |
|:--|:--|:--|:--|
| Regimes | 2 | Judgement | A third adds little to the fit ([Hardy, 2001, section 3, p. 43](https://doi.org/10.1080/10920277.2001.10595984){:target="_blank"}) |
| Shared regimes | One stream for every market | Judgement | Markets enter and leave crises together, which brings simulated equity correlations close to the fitted ones ([Ahlgrim, D'Arcy and Gorvett, 2005, section 3](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}) |
| Long indices and their starts | Table above | Judgement | The longest monthly index of each market that is keyless |
| US start year | 1946 | Judgement | After the deflation of the 1930s |
| Switching chances | Per index | Fitted | Baum-Welch on the long index, held fixed |
| Regime means and volatilities | Per fund | Fitted | Hardy's model by maximum likelihood on the fund's monthly returns since 2000, under the index's switching |
| Inflation slopes $$\gamma$$ (US Broad, Small Cap) | +0.45 and +0.20 on the log-odds of a calm month turning turbulent, per point of inflation | Fitted | Expectation-maximisation, CRSP market and Shiller CPI since 1946 |
| Equity premium | 3.77% (geometric) | Sourced | [Jordà et al. (2019, Table II)](https://doi.org/10.1093/qje/qjz012){:target="_blank"} |
| Regime shares the premium is earned over | US Broad 21.1% turbulent, Small Cap 26.6% | Fitted | Simulated moments: a pilot run of the calibrated US inflation, 2,000 paths, 100 years, the first 30 left out |
| Risk-free part | The simulated US short rate at the start of each step | Model choice | Dollar-listed funds; interest-rate parity |

#### Other Equity Models

Four other equity models are options:

| Model | What it does |
|:--|:--|
| Returns above cash ([Hibbert, Mowbray and Turnbull, 2001](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"}) | The regimes fitted on returns in excess of a short rate, with the simulated short rate added back. |
| Price from dividends ([Wilkie, 1986](https://doi.org/10.1017/S0071368600009009){:target="_blank"}) | The dividend index over the dividend yield, the last link of Wilkie's cascade. |
| KNW | The equity leg of the [KNW model](/projects/financescenarios/docs/interest-rates#knw-models), with stochastic volatility shared with rates and inflation. |
| Risk-neutral | For valuing options and guarantees, a geometric Brownian motion drifting at the short rate less the dividend yield, with an implied, SVI, realised or Heston volatility (below); the [Equities reference](#equities) has the sources. |
| Switching with the business cycle | Instead of inflation, the switching chances follow the OECD's US leading indicator ([Filardo, 1994](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}), fitted together with the regimes by the same joint expectation-maximisation of Diebold, Lee and Weinbach. On SPY since 2005, a calm month turns turbulent with a chance of 5.4% at an indicator of 105 and 27.7% at 95. The earlier two-step fit, which first labelled each month by its likelier regime and then fitted a logit, gave 5.8% and 8.8%: labelling throws away how unsure each month's regime is, and flattens the link. |

#### The Implied Volatility

`volatility_source: implied` reads each equity's volatility from its option chain at the first expiration at least a week out. The at-the-money volatility is the average of the out-of-the-money call and put on either side of the price. The quote nearest the price is not used on its own: for a thinly traded fund it is often an in-the-money call whose last trade is stale, and it inverts to a number far from the market's. A warning names any implied volatility more than twice or less than half the realized one. On the option chains of late October 2026:

| Fund | Nearest quote | Out-of-the-money average | Realized |
|:--|--:|--:|--:|
| SPY | 17.8% | 17.6% | 15.2% |
| IWM | 23.2% | 23.5% | 20.1% |
| VGK | 23.0% | 18.9% | 18.6% |
| EWJ | 27.9% | 23.7% | 16.2% |
| EEM | 66.8% | 32.0% | 20.9% |

#### Heston Paths at a Monthly Step

Heston's (1993) stochastic volatility, fitted to option prices, often has a fast variance: in the [Equities reference](#equities) example it reverts at a speed of 14.6 a year, so at a monthly step the speed times the step is above one. A full-truncation Euler step, which sets a negative variance to zero, then overshoots, and the paths no longer reproduce the prices they were fitted to. The paths therefore step with the quadratic-exponential scheme of [Andersen (2008)](https://doi.org/10.21314/jcf.2008.189){:target="_blank"}, which draws the next variance from a distribution matched to its exact mean and variance and never goes negative, with the martingale correction that keeps the discounted price a martingale ([van Haastrecht and Pelsser, 2010, section 4.2](https://doi.org/10.1142/S0219024910005668){:target="_blank"}). On that example's fit, one-year calls priced from 200,000 monthly paths against [Heston's (1993)](https://doi.org/10.1093/rfs/6.2.327){:target="_blank"} closed form:

| Strike | 80 | 90 | 100 | 110 | 120 |
|:--|--:|--:|--:|--:|--:|
| Full-truncation Euler | 0.0% | +0.6% | +2.4% | +7.3% | +18.1% |
| QE with martingale correction | -0.1% | -0.1% | -0.1% | -1.2% | -3.6% |

The errors are relative to the closed-form price; the remaining error of the QE scheme sits in the far out-of-the-money calls, whose prices are small.

<div class="fs-ref"><a href="#equities"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Equities API</a></div>

### FX {#currencies}

#### Purchasing Power Parity for the Euro and the Pound

Over a few years an exchange rate moves like a random walk, but over decades it is pulled back toward purchasing power parity: a currency that buys much more abroad than it usually does loses that edge. The studies [Rogoff (1996, section 5.B, p. 656)](https://ideas.repec.org/a/aea/jeclit/v34y1996i2p647-668.html){:target="_blank"} surveys agree on a half-life of three to five years for real exchange rates, and cross-country panels find about four (section 5.C, p. 657). The default takes four years.

<div class="fs-facts">
  <div><span>Series</span><b>Each currency against the US dollar</b></div>
  <div><span>Data</span><b>BIS end-of-month rates, OECD consumer prices</b></div>
  <div><span>Default model</span><b>Purchasing power parity for the euro and the pound; a random walk for the yen</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/markets">FX</a></div>
</div>

The real exchange rate is the nominal rate (foreign currency per US dollar) adjusted for the two price levels, $$q_t = \ln S_t - \ln(P^f_t / P^{us}_t)$$. It reverts to its average since 2000 at $$\kappa = \ln 2 / 4 = 0.173$$ a year, and the nominal rate also moves with the two simulated inflation rates:

$$
q_{t+\Delta t} = \bar q + (q_t - \bar q)\,e^{-\kappa\Delta t} + \sigma\sqrt{\frac{1 - e^{-2\kappa\Delta t}}{2\kappa}}\;z_t, \qquad S_{t+\Delta t} = S_t \exp\!\left(\left[\ln(1 + \pi^f_t) - \ln(1 + \pi^{us}_t)\right]\Delta t + q_{t+\Delta t} - q_t\right)
$$

Inflation is a rate over a year, so a price index grows by $$\ln(1 + \pi)$$ a year, the log change [Ahlgrim, D'Arcy and Gorvett (2005, section 3, eq. 3.7)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"} model: the two price levels in $$q_t$$ move the way the simulated price indices do.

The volatility $$\sigma$$ is the nominal rate's monthly volatility since 2000: the short-run volatility of real exchange rates is of the same order as that of nominal ones (Rogoff, 1996, section 1, p. 647). The rates are the Bank for International Settlements' end-of-month rates ([BIS](https://data.bis.org/topics/XRU){:target="_blank"}); changes of monthly averages would keep only about two thirds of a random walk's variance ([Working, 1960](https://doi.org/10.2307/1907574){:target="_blank"}). The price indices are the OECD's consumer price indices of the United States, Germany (for the euro, as the euro area's inflation series) and the United Kingdom.

The chart shows the euro and pound real exchange rates since 2000 against their average, with the expected pull back at a four-year half-life:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/markets/fx-ppp" alt="The euro and pound real exchange rates since 2000 against their average, with the expected pull back at a four-year half-life" %}

Today, in real terms, the dollar buys more than its average since 2000:

<div class="ca-nums fs-nums">
  <span><b>11%</b>more euros</span>
  <span><b>10%</b>more pounds</span>
</div>

The median scenario has the dollar losing half of that edge in four years.

How sure is the anchor? For a process that reverts at speed $$\kappa$$, the average of $$T$$ years has a standard error of about $$\sigma / (\kappa\sqrt{T})$$: 0.104 for the euro and 0.096 for the pound over 27 years, as large as today's distance from the anchor. Today's level lies within one standard error of the historical average, so the data alone cannot tell the two apart. The anchor stays on the historical average, where the parity literature [Rogoff (1996)](https://ideas.repec.org/a/aea/jeclit/v34y1996i2p647-668.html){:target="_blank"} surveys measures it. Anchoring on today's level instead, the `today` option, turns the pull off and leaves a random walk around today; on year-end backtests from 2000 to 2022 that lowered the euro's four-year CRPS skill from +0.39 to +0.30.

#### No Trend for the Yen

The yen has no Japanese inflation series in the default to measure its real rate against, so it is a random walk with no trend: its drift is $$\sigma^2/2$$, so the median stays at today's rate. A random walk forecasts exchange rates at least as well as structural models ([Meese and Rogoff, 1983, section 4, Table 1, p. 13](https://doi.org/10.1016/0022-1996(83)90017-X){:target="_blank"}), and a fitted trend would carry a currency view forward for decades.

How each FX number is set:

| Number | Value | Kind | Why |
|:--|:--|:--|:--|
| Half-life of the real rate | 4 years | Sourced | [Rogoff (1996, sections 5.B and 5.C, pp. 656-657)](https://ideas.repec.org/a/aea/jeclit/v34y1996i2p647-668.html){:target="_blank"} |
| Anchor $$\bar q$$ | The average real rate since 2000 | Judgement | The calibration window; today's distance from it is -0.105 (euro) and -0.095 (pound) in logs |
| Volatility | Euro 9.3%, pound 8.6%, yen 9.3% a year | Fitted | End-of-month rates since 2000 |
| Yen | Random walk | Sourced | [Meese and Rogoff (1983, section 4, Table 1, p. 13)](https://doi.org/10.1016/0022-1996(83)90017-X){:target="_blank"} |

Other drifts are options: the sample's own trend, or uncovered interest-rate parity, $$d\ln S_t = (r^f_t - r^{us}_t - \tfrac{1}{2}\sigma^2)\,dt + \sigma\,dW_t$$, which [Fama (1984, Table 2, p. 326)](https://doi.org/10.1016/0304-3932(84)90046-1){:target="_blank"} finds history does not support. That drift gives the same expected return in either currency to an investor who counts in euros; one who counts in dollars expects $$\sigma^2$$ a year more, since the expected rate and the expected value of its inverse cannot both grow at the rate gap ([Siegel, 1972](https://doi.org/10.2307/1880565){:target="_blank"}).

#### Risk-Neutral Exchange Rates

For valuing, an exchange rate must drift so that a foreign deposit, converted into dollars and discounted at the US rate, is worth what it costs: the dollar is the measure, as for every other price in a valuation run. In [Garman and Kohlhagen (1983)](https://doi.org/10.1016/S0261-5606(83)80001-1){:target="_blank"} the dollar price of a unit of foreign currency, $$Y = 1/S$$, drifts at $$r^{us} - r^f$$. The model quotes $$S$$, foreign currency per dollar, and by Itô's lemma $$S = 1/Y$$ then drifts at the gap the other way plus the variance:

$$
\frac{dS_t}{S_t} = \left(r^f_t - r^{us}_t + \sigma^2\right)dt + \sigma\,dW_t
$$

with both rates the simulated ones at the start of each step. Leaving out the $$\sigma^2$$, as a drift of $$r^f - r^{us}$$ does, is risk-neutral for an investor who counts in euros, not in dollars, and overstates the dollar value of foreign holdings by $$e^{\sigma^2 T}$$: about 9% at 10 years at the euro's 9.3% volatility. The known answer: a 10-year euro deposit, converted to dollars and discounted at the simulated US rate, has a mean of 1.

<div class="fs-ref"><a href="#fx"><i class="fas fa-book" aria-hidden="true"></i>Full reference: FX API</a></div>

### Commodities {#commodity-prices}

#### Gold: A Random Walk in Real Terms

Gold has no level its real price returns to. About 2,500 tonnes are mined a year, some 1.5% of the 171,300 tonnes above ground, so supply barely responds to price ([Erb and Harvey, 2013, pp. 28-29](https://doi.org/10.2469/faj.v69.n4.1){:target="_blank"}); the "golden constant" of a long-run real return near zero rests on centuries of data (p. 11), while the real price swings as much as the nominal one (p. 12), and a pull fitted on a short sample rests on one episode (p. 15). A mean-reverting fit on gold futures since 2000 settles at about 24,000 USD an ounce with a 21-year half-life: no credible level.

<div class="fs-facts">
  <div><span>Gold</span><b>A random walk in real terms</b></div>
  <div><span>Brent</span><b>One-factor mean reversion in logs</b></div>
  <div><span>Alternative</span><b>Schwartz-Smith two factor</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/markets">Commodities</a></div>
</div>

The default therefore makes gold a random walk in real terms: it keeps pace with the simulated US price index, which grows by $$\ln(1 + \pi_t)$$ a year, and adds a drift of $$\sigma^2/2$$, so its median real price stays flat:

$$
S_{t+\Delta t} = S_t \exp\!\left(\ln(1 + \pi_t)\,\Delta t + \sigma\sqrt{\Delta t}\,z_t\right)
$$

The volatility, 17.9% a year, comes from the daily gold futures price (GC=F) since 2000. The chart shows gold's price in today's US dollars an ounce since 1971:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/markets/gold-real" alt="Gold's price in today's US dollars an ounce since 1971" %}

#### Brent: Pulled toward a Level

An oil price is pulled toward a level set by the cost of production: high prices bring new supply, low prices cut it. The log price follows the one-factor model of [Schwartz (1997)](https://doi.org/10.1111/j.1540-6261.1997.tb02721.x){:target="_blank"}, which keeps the price positive:

$$
dX_t = a(\theta - X_t)\,dt + \sigma\,dW_t, \qquad X_t = \ln S_t
$$

Fitted on daily Brent futures (BZ=F) since July 2007, the long-run median $$e^{\theta}$$ is 77 USD a barrel, a shock halves in 1.5 years, and the volatility is 38.3% a year. Brent rather than WTI: the WTI front-month future closed at -37.63 USD on 20 April 2020, a price the log model cannot take. The chart shows Brent since 1990 with the fitted long-run median:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/markets/brent" alt="Brent crude since 1990 with the fitted long-run median" %}

#### Correcting the Speed for a Short Sample

The speed comes from regressing each day's change in the log price on the day before's level. That estimate is biased upward in any sample of realistic length: a series that wanders for a few years looks like it is being pulled back faster than it is. [Tang and Chen (2009, Theorem 3.1.1)](https://doi.org/10.1016/j.jeconom.2008.11.001){:target="_blank"} give the bias of the maximum-likelihood speed of an Ornstein-Uhlenbeck process whose level is estimated too, over $$T$$ years of steps $$\Delta t$$ apart:

$$
E(\hat a) - a \approx \frac{B_1}{T}, \qquad B_1 = \frac{5}{2} + e^{a\Delta t} + \frac{1}{2}e^{2a\Delta t}
$$

As the step shrinks $$B_1$$ tends to 4, so the bias is about $$4/T$$ a year whatever the frequency: twenty years of daily data add about 0.2 to the speed. The fit takes $$B_1/T$$, evaluated at the estimate, off the speed, and reads the volatility again at the corrected speed so one step's spread stays the one the data show. Brent's 19 years of daily prices give a plain speed of 0.67 and a corrected one of 0.46: the half-life of a shock rises from 1.0 to 1.5 years. The correction applies to every plain mean-reverting fit, among them the US Treasury curve's level, slope and curvature (from 0.35, 0.24 and 0.73 to 0.20, 0.10 and 0.58 a year). It leaves out regressions with extra columns and the fits read a year apart (house prices below), which the theorem does not cover. When the correction would remove all mean reversion, as it can on five years of data, the plain speed is kept with a warning: the sample cannot tell the series from a random walk.

The chart simulates the plain estimator on paths with Brent's corrected speed of 0.46 and shows the default's daily fits before and after:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/markets/ou-speed-bias" alt="The average plain and corrected mean-reversion speed of simulated paths against the years of data, and the default's Brent and Treasury curve speeds before and after the correction" %}

At 20 years the plain estimate averages 0.68 against a true 0.46, and the corrected one 0.48. At five years the correction would leave no pull in many samples, which keep the plain speed, so the average stays above the truth.

How each commodity number is set:

| Number | Value | Kind | Why |
|:--|:--|:--|:--|
| Gold model | Random walk in real terms | Sourced | [Erb and Harvey (2013, pp. 11-15, 28-29)](https://doi.org/10.2469/faj.v69.n4.1){:target="_blank"} |
| Gold volatility | 17.9% | Fitted | Daily GC=F since 2000 |
| Brent level, speed, volatility | 77 USD, 0.46 a year, 38.3% | Fitted | Daily BZ=F since July 2007, [Schwartz (1997)](https://doi.org/10.1111/j.1540-6261.1997.tb02721.x){:target="_blank"}, speed corrected for the sample's length ([Tang and Chen, 2009](https://doi.org/10.1016/j.jeconom.2008.11.001){:target="_blank"}) |

The two-factor model of [Schwartz and Smith (2000)](https://doi.org/10.1287/mnsc.46.7.893.12034){:target="_blank"}, a short-term deviation that fades plus a long-term level that drifts, fitted to the futures curve, is an option, also risk-neutral.

<div class="fs-ref"><a href="#commodities"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Commodities API</a></div>

### Real Estate

House-price growth, not the price level, reverts to a long-run rate, as in eq. 3.18 of [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf#page=21){:target="_blank"}: a price index has no level to return to over decades, and booms fade in growth while leaving a mark on the level. In the default, growth also responds to the long rate a year earlier. Higher rates make mortgages dearer and cool the housing market with a delay: [Iacoviello (2005, section I, Figure 1, p. 741)](https://doi.org/10.1257/0002828054201477){:target="_blank"} finds that tighter money lowers real house prices in US data from 1974 to 2003.

<div class="fs-facts">
  <div><span>Series</span><b>US house-price growth over the past year</b></div>
  <div><span>Data</span><b>OECD house prices and the OECD US 10-year rate</b></div>
  <div><span>Model</span><b>Mean-reverting growth, linked to the long rate a year earlier</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/markets">Real estate</a></div>
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

The path is price growth only; rental income is added when real estate is held as an asset (see [portfolio](/projects/financescenarios/docs/portfolio#what-a-portfolio-can-hold)). The price index compounds the simulated growth as $$\ln(1 + g_t)$$ a year, the log change of eq. 3.7 of Ahlgrim, D'Arcy and Gorvett, so a steady 4% gives $$1.04^T$$.

#### Calm and Turbulent House Prices

House prices do not swing with one steady volatility: long quiet stretches alternate with booms and busts. The `regime_switching` volatility option lets the size of the shocks switch between a calm and a turbulent regime, fitted the way [Crawford and Fratantoni (2003)](https://doi.org/10.1111/1540-6229.00064){:target="_blank"} fit theirs: on quarter-on-quarter growth, an autoregression whose shock size follows a two-regime Markov chain, by maximum likelihood through [Hamilton's (1989)](https://doi.org/10.2307/1912559){:target="_blank"} filter:

$$
x_t = \ln(1 + q_t) = c + \phi\,x_{t-1} + s_{k_t}\,e_t, \qquad e_t \sim N(0, 1), \qquad P(k_{t+1} = j \mid k_t = i) = p_{ij}
$$

Quarterly growth, not growth over the past year read every quarter: each year-over-year reading shares three quarters with the one before, so its residuals are strongly autocorrelated, and two regimes then beat one even on data with a single constant volatility. On simulated samples of US length with no regimes at all, year-apart residuals gave the two regimes a log-likelihood gain of about 57; quarterly growth gives one close to zero. The regimes' shock sizes are then scaled so their long-run average variance is the growth process's own, and the switching chances are converted to the scenario's step. Fitted on the OECD's US index, 1970 to 2026 (224 quarters):

| | Calm | Turbulent |
|:--|--:|--:|
| Shock size a quarter | 0.24% | 1.02% |
| Volatility in the scenarios, a year | 1.2% | 5.0% |
| Chance of staying, a quarter | 0.960 | 0.970 |
| Average spell | 6.2 years | 8.4 years |
| Long-run share | 42% | 58% |

The two regimes raise the log-likelihood by 61.3 over one constant volatility. A parametric bootstrap checks whether that could be chance: 200 samples simulated from the constant-volatility autoregression fitted to the same data, each fitted both ways, give gains with a median of 0.0 and a largest of 7.1, so none reaches 61.3 (bootstrap p = 0.005). The turbulent regime holds the 1970s and early 1980s, the early 1990s, the bust from 2006 to 2014 and the swings since 2020; today the index is in it.

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/markets/house-price-regimes" alt="US quarter-on-quarter house-price growth since 1970 with the quarters in the turbulent regime shaded" %}

The default keeps one constant volatility, read a year apart with the rate link above; the regimes are an option for a run that should hold housing busts as long quiet stretches and short wild ones.

<div class="fs-ref"><a href="#realestate"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Real estate API</a></div>

### Dividend Yield and Dividend Growth

#### Dividend Yield {#dividend-yield}

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

#### Dividend Growth (Wilkie)

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

<div class="fs-ref"><a href="#dividendyield"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Dividend yield API</a></div>
<div class="fs-ref"><a href="#dividendgrowth"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Dividend growth API</a></div>

### Credit Spreads

A credit spread is the extra yield a company pays over government debt: expected default losses plus a risk and liquidity premium that widens sharply in a downturn. The spread reverts to a normal level as an Ornstein-Uhlenbeck process. Fitting it in logs is a modeling judgement rather than a published specification: it keeps the spread positive and makes its swings proportional to its level, so wide spreads are the most volatile and the distribution is skewed toward sharp widenings:

$$
d\ln s_t = a(\theta - \ln s_t)\,dt + \sigma\,dW_t
$$

<div class="fs-facts">
  <div><span>Model</span><b>Mean reversion in logs (Ornstein-Uhlenbeck)</b></div>
  <div><span>Data</span><b>ICE BofA, Moody's, Bundesbank, RBA, ECB</b></div>
  <div><span>Longest US history</span><b>Moody's, monthly from 1953</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/markets">Credit</a></div>
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

For a whole spread curve rather than buckets, see the [credit term structure API](#credittermstructure).

<div class="fs-ref"><a href="#credit"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Credit API</a></div>

### Credit Migration and Default

Spreads price credit risk; migration models the events: downgrades, defaults and losses on a bond portfolio by rating. Each borrower's credit quality is a standard normal variable: a shared credit cycle $$Z$$ with weight $$\sqrt{\rho}$$, for asset correlation $$\rho$$, plus the borrower's own luck. A through-the-cycle transition matrix sets each rating's thresholds for upgrade, downgrade and default. In a year with cycle $$Z$$, a rating with long-run default probability $$p$$ defaults with probability

$$
p(Z) = \Phi\!\left(\frac{\Phi^{-1}(p) - \sqrt{\rho}\,Z}{\sqrt{1-\rho}}\right)
$$

where $$\Phi$$ is the standard normal distribution function. The same shift applies to every threshold, so a bad year ($$Z$$ below zero) moves every rating toward downgrade and default at once. This is the one-factor approach of [Kim (1999)](https://www.msci.com/www/research-report/a-way-to-condition-transition/018440984){:target="_blank"}, in the Markov rating framework of [Jarrow, Lando and Turnbull (1997)](https://doi.org/10.1093/rfs/10.2.481){:target="_blank"}, and the same formula that underlies the Basel IRB capital charge.

<div class="fs-facts">
  <div><span>Model</span><b>One-factor credit cycle on a rating transition matrix</b></div>
  <div><span>Data</span><b>ESMA CEREP rating statistics</b></div>
  <div><span>PD floor</span><b>0.05%, the CRR3 corporate PD floor</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/markets">Credit migration</a></div>
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

<div class="fs-ref"><a href="#creditmigration"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Credit migration API</a></div>

### References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">25</span></summary>

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. [casact.org](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}
- Andersen, L. (2008). "Simple and Efficient Simulation of the Heston Stochastic Volatility Model." Journal of Computational Finance, 11(3), 1-42. [doi.org](https://doi.org/10.21314/jcf.2008.189){:target="_blank"}
- Crawford, G.W., Fratantoni, M.C. (2003). "Assessing the Forecasting Performance of Regime-Switching, ARIMA and GARCH Models of House Prices." Real Estate Economics, 31(2), 223-243. [doi.org](https://doi.org/10.1111/1540-6229.00064){:target="_blank"}
- Diebold, F.X., Lee, J.-H., Weinbach, G.C. (1994). "Regime Switching with Time-Varying Transition Probabilities." In Hargreaves, C. (ed.), Nonstationary Time Series Analysis and Cointegration, 283-302. [doi.org](https://doi.org/10.1093/oso/9780198773917.003.0010){:target="_blank"}
- Duffie, D., Singleton, K.J. (1993). "Simulated Moments Estimation of Markov Models of Asset Prices." Econometrica, 61(4), 929-952. [doi.org](https://doi.org/10.2307/2951768){:target="_blank"}
- Erb, C.B., Harvey, C.R. (2013). "The Golden Dilemma." Financial Analysts Journal, 69(4), 10-42. [doi.org](https://doi.org/10.2469/faj.v69.n4.1){:target="_blank"}
- Fama, E.F., French, K.R. (1993). "Common Risk Factors in the Returns on Stocks and Bonds." Journal of Financial Economics, 33(1), 3-56. [doi.org](https://doi.org/10.1016/0304-405X(93)90023-5){:target="_blank"}
- Fama, E.F., Schwert, G.W. (1977). "Asset Returns and Inflation." Journal of Financial Economics, 5(2), 115-146. [doi.org](https://doi.org/10.1016/0304-405X(77)90014-9){:target="_blank"}
- Filardo, A.J. (1994). "Business-Cycle Phases and Their Transitional Dynamics." Journal of Business & Economic Statistics, 12(3), 299-308. [doi.org](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}
- French, K.R. Data Library. [dartmouth.edu](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html){:target="_blank"}
- Garman, M.B., Kohlhagen, S.W. (1983). "Foreign Currency Option Values." Journal of International Money and Finance, 2(3), 231-237. [doi.org](https://doi.org/10.1016/S0261-5606(83)80001-1){:target="_blank"}
- van Haastrecht, A., Pelsser, A. (2010). "Efficient, Almost Exact Simulation of the Heston Stochastic Volatility Model." International Journal of Theoretical and Applied Finance, 13(1), 1-43. [doi.org](https://doi.org/10.1142/S0219024910005668){:target="_blank"}
- Hamilton, J.D. (1989). "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle." Econometrica, 57(2), 357-384. [doi.org](https://doi.org/10.2307/1912559){:target="_blank"}
- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. [doi.org](https://doi.org/10.1080/10920277.2001.10595984){:target="_blank"}
- Heston, S.L. (1993). "A Closed-Form Solution for Options with Stochastic Volatility with Applications to Bond and Currency Options." Review of Financial Studies, 6(2), 327-343. [doi.org](https://doi.org/10.1093/rfs/6.2.327){:target="_blank"}
- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert Limited. [ressources-actuarielles.net](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"}
- Iacoviello, M. (2005). "House Prices, Borrowing Constraints, and Monetary Policy in the Business Cycle." American Economic Review, 95(3), 739-764. [doi.org](https://doi.org/10.1257/0002828054201477){:target="_blank"}
- Jordà, Ò., Knoll, K., Kuvshinov, D., Schularick, M., Taylor, A.M. (2019). "The Rate of Return on Everything, 1870-2015." Quarterly Journal of Economics, 134(3), 1225-1298. [doi.org](https://doi.org/10.1093/qje/qjz012){:target="_blank"}
- McFadden, D. (1989). "A Method of Simulated Moments for Estimation of Discrete Response Models Without Numerical Integration." Econometrica, 57(5), 995-1026. [doi.org](https://doi.org/10.2307/1913621){:target="_blank"}
- Meese, R.A., Rogoff, K. (1983). "Empirical Exchange Rate Models of the Seventies: Do They Fit Out of Sample?" Journal of International Economics, 14(1-2), 3-24. [doi.org](https://doi.org/10.1016/0022-1996(83)90017-X){:target="_blank"}
- Rogoff, K. (1996). "The Purchasing Power Parity Puzzle." Journal of Economic Literature, 34(2), 647-668. [ideas.repec.org](https://ideas.repec.org/a/aea/jeclit/v34y1996i2p647-668.html){:target="_blank"}
- Schwartz, E.S. (1997). "The Stochastic Behavior of Commodity Prices: Implications for Valuation and Hedging." The Journal of Finance, 52(3), 923-973. [doi.org](https://doi.org/10.1111/j.1540-6261.1997.tb02721.x){:target="_blank"}
- Siegel, J.J. (1972). "Risk, Interest Rates and the Forward Exchange." Quarterly Journal of Economics, 86(2), 303-309. [doi.org](https://doi.org/10.2307/1880565){:target="_blank"}
- Tang, C.Y., Chen, S.X. (2009). "Parameter Estimation and Bias Correction for Diffusion Processes." Journal of Econometrics, 149(1), 65-81. [doi.org](https://doi.org/10.1016/j.jeconom.2008.11.001){:target="_blank"}
- Working, H. (1960). "Note on the Correlation of First Differences of Averages in a Random Chain." Econometrica, 28(4), 916-918. [doi.org](https://doi.org/10.2307/1907574){:target="_blank"}

</details>
