---
title: Equities
seo_title: "Equities | Finance Scenarios"
seo_title_suffix: false
excerpt: "How Finance Scenarios simulates stock markets: Hardy's regime-switching lognormal model timed on decades of each market's index, switching that follows inflation, and a long-run premium over the simulated short rate."
description: "Equities in Finance Scenarios: calm and turbulent regimes, timing on a long index with the fund's own means and volatilities, inflation-driven switching, the equity premium over the short rate, risk-neutral equities and a run."
author_profile: false
permalink: /projects/financescenarios/docs/markets
classes: wide-sidebar
layout: single
redirect_from:
    - /projects/financescenarios/docs/reference/equities
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-markets"
---

How far can stocks fall, for how long, and what do they earn on the way? A single bell curve of monthly returns gets all three wrong: crashes cluster, bear markets run for months, and returns move with rates and inflation. In the default model each stock market therefore switches between calm and turbulent regimes whose timing is fitted on decades of its own index; turbulence is likelier when inflation is high, and every market earns the simulated short rate plus a long-run premium. For valuing options and guarantees, a risk-neutral model takes its place.

<div class="fs-facts">
  <div><span>Default model</span><b>Regime-switching lognormal, two regimes</b></div>
  <div><span>Regimes timed on</span><b>A long index of each market</b></div>
  <div><span>Expected return</span><b>The US short rate plus 3.77%</b></div>
</div>

## Calm and Turbulent Regimes

Markets alternate between calm stretches of steady gains and turbulent ones of losses and large swings. The model is the regime-switching lognormal model of [Hardy (2001, section 3, pp. 42-43)](https://doi.org/10.1080/10920277.2001.10595984){:target="_blank"}: in regime $$k$$ the monthly log return is normal with its own mean $$\mu_k$$ and volatility $$\sigma_k$$, and a Markov chain decides each month whether to stay or switch:

$$
\ln\frac{S_{t+\Delta t}}{S_t} \,\Big|\, s_{t+\Delta t} = k \;\sim\; N\!\left(\mu_k \Delta t,\; \sigma_k^2 \Delta t\right)
$$

with $$s_{t+\Delta t}$$ the regime the market is in over the step. A mix of a low- and a high-volatility normal distribution has fatter tails than one normal of the same variance, regimes persist so turbulent months cluster, and drawdowns run over several months, which is what hits a guarantee or a funding ratio. Two regimes are enough: on monthly S&P 500 and TSE 300 returns a third regime barely improves the fit for the TSE 300 and only slightly for the S&P 500 (Hardy, 2001, section 3, p. 43).

The regimes are estimated with the Baum-Welch algorithm, the expectation-maximization algorithm for hidden Markov models. Every market draws its switches from one shared stream of random numbers, each with its own switching chances and starting regime, so the markets tend to enter and leave crises together.

Regimes fitted on a fund's own history have to earn their place. The likelihood has several local maxima, so the algorithm also starts from the history's calm and turbulent stretches and keeps whichever start fits best ([Harris, 1999, section 1, p. 48](https://doi.org/10.2143/AST.29.1.504606){:target="_blank"}). The two regimes must then beat a single one by the Schwarz Bayes criterion of [Hardy (2001, section 5.2.3)](https://doi.org/10.1080/10920277.2001.10595984){:target="_blank"}: half the log of the sample size for each extra parameter, which a parametric bootstrap puts at roughly a 2% test. A likelihood-ratio test has no chi-square reference here, since the switching chances mean nothing under one regime ([Hansen, 1992, section 1, p. S62](https://doi.org/10.1002/jae.3950070506){:target="_blank"}). A fund that falls short gets the one-regime mean and volatility in both regimes: gold (GLD), healthcare (XLV) and India (INDA) in the bundled sets.

## Timed on a Long Index, Fitted on the Fund

Twenty-five years of an exchange-traded fund's history hold two or three bear markets, too few to say how often they come and how long they last. An index with sixty to eighty years of history holds a dozen. So the long index of each market sets how the market switches: its chances of staying calm or turbulent, and with them the share of time in each regime and the length of a spell, are fitted on the index and then held fixed.

The fund sets the rest. Each regime's mean and volatility come from Hardy's model fitted on the fund's own monthly log returns $$y_t$$ by maximum likelihood, with the index's switching held fixed: the expectation-maximization algorithm with only the means and volatilities free. Hamilton's filter and smoother give each month's chance $$w_{tk}$$ of each regime, each regime takes the weighted mean and variance of the returns, and the two steps repeat until the likelihood stops rising:

$$
w_{tk} = P(s_t = k \mid y_1, \dots, y_T), \qquad \mu_k = \frac{1}{\Delta t}\,\frac{\sum_t w_{tk}\, y_t}{\sum_t w_{tk}}, \qquad \sigma_k^2 = \frac{1}{\Delta t}\,\frac{\sum_t w_{tk}\,(y_t - \mu_k \Delta t)^2}{\sum_t w_{tk}}
$$

The fit starts from the index's regimes shifted and scaled to the fund's mean and variance. It is the published estimator ([Hardy, 2001, section 3](https://doi.org/10.1080/10920277.2001.10595984){:target="_blank"}; [Hamilton, 1989](https://doi.org/10.2307/1912559){:target="_blank"}) with one constraint, the index's switching, rather than a map of the index's regimes onto the fund. Today's regime is the one the fund's own recent returns point to.

The fund's twenty-odd years then set each regime's level and swings on their own, and that has a cost for Japan. On year-end backtests from 2000 to 2022, four years ahead, EWJ's CRPS skill (how much its scenarios improve on a forecast of no change) on the 18 holdout origins is +0.06, against +0.25 when the index's regimes are shifted and scaled onto the fund instead. Europe's is +0.34 against +0.25, and the US funds' are about the same either way (the scores are explained on [Out of Sample](/projects/financescenarios/docs/validation/out-of-sample)).

The chart shades the US market's turbulent months since 1946, and shows SPY since 2000 under the same switching, with each regime's level and swings fitted on SPY's own returns:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/markets/equity-regimes" alt="The US stock market since 1946 with its turbulent months shaded, and SPY since 2000 under the same switching with its regimes fitted on its own returns" %}

The long index behind each fund, and the regimes it gives:

| Fund | Long index that times the regimes | From | Turbulent share | Turbulent / calm spell (months) |
|:--|:--|--:|--:|--:|
| US Broad (SPY) | CRSP value-weighted US market, [Ken French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html){:target="_blank"} | 1946 | 20% | 6.3 / 25.0 |
| Small Cap (IWM) | The same market plus the size factor SMB ([Fama and French, 1993, section 2.1.2, p. 9](https://doi.org/10.1016/0304-405X(93)90023-5){:target="_blank"}) | 1946 | 27% | 8.8 / 24.2 |
| Europe (VGK) | Ken French's European market, in US dollars with dividends | 1990 | 27% | 8.9 / 23.8 |
| Japan (EWJ) | The Nikkei 225 (Yahoo Finance), a price index | 1965 | 45% | 12.0 / 14.5 |
| Emerging Markets (EEM) | The fund's own history | 2003 | 10% | 6.6 / 57.5 |

The two US funds switch with inflation (next section), so their share and spells depend on it; the table gives them at the average inflation of each fund's own years. With the switching held fixed, the CRSP market since 1946 is turbulent 28% of months, in turbulent spells of 8.2 months against calm ones of 21.1 (the chart).

The US histories start in 1946 by choice: stocks did badly through the falling prices of the 1930s, and with the 1929-34 bear market in the sample high inflation would look nearly harmless (next section). The Nikkei 225 is a price index without dividends; the dividend yield would add about the same to every month, so leaving it out barely moves the timing of the regimes, the only thing this history is used for.

## Turbulence Is Likelier When Inflation Is High

Stocks have done badly when inflation runs high ([Fama and Schwert, 1977, Table 5, p. 128](https://doi.org/10.1016/0304-405X(77)90014-9){:target="_blank"}). On US data since 1947 the same holds: the real return was about -1.5% a year in years with inflation above 5%, against about 12% below 3%. For the US markets the chance of switching regime therefore depends on the simulated inflation, the time-varying transition probabilities of [Filardo (1994)](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}:

$$
P(s_{t+1} = j \mid s_t = i, \pi_t) = \frac{e^{\alpha_{ij} + \gamma_{ij}\pi_t}}{\sum_k e^{\alpha_{ik} + \gamma_{ik}\pi_t}}
$$

with $$\pi_t$$ the simulated year-over-year inflation, as a decimal, and the turbulent regime the reference whose coefficients are zero. The intercepts $$\alpha_{ij}$$ and slopes $$\gamma_{ij}$$ are fitted by the expectation-maximization algorithm of [Diebold, Lee and Weinbach (1994, section 3)](https://doi.org/10.1093/oso/9780198773917.003.0010){:target="_blank"} on the CRSP market's monthly total return and Shiller's CPI inflation since 1946, with the regimes held at the index's own. The expectation step reads each month's regime chances through the switching at that month's inflation, and the maximization step refits each row's logit on those chances, so regimes and switching come from one likelihood. Recent decades hold too few high-inflation years to estimate it; the history since 1946 holds the late 1940s, the 1970s and 2021-22.

For US stocks:

<div class="ca-nums fs-nums">
  <span><b>3.1%</b>chance a calm month turns turbulent at 2% inflation</span>
  <span><b>31.8%</b>the same chance at 8% inflation</span>
  <span><b>17%</b>of the time turbulent at a steady 2%</span>
  <span><b>59%</b>of the time turbulent at a steady 8%</span>
</div>

Read through the fitted model, 72% of the months since 1946 with inflation above 6% were turbulent, against 13% of those below 3%. The chart sets the fitted long-run share of turbulent months at each inflation rate against the share in history:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/markets/turbulence-inflation" alt="The fitted long-run share of turbulent months at each inflation rate, against the share in history by inflation bucket" %}

## Every Market Earns the Short Rate plus a Premium

A fund's own average return since 2000 is one draw of 25 years, and carrying it forward for decades is a view, not a fact. Each market instead earns the simulated short rate plus a long-run premium, so its expected return rises and falls with rates, as in [Hibbert, Mowbray and Turnbull (2001, section 5.2.1)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"}. The premium is 3.77% a year, equity's geometric mean return above bills across 16 countries, equally weighted, from 1870 to 2015 ([Jordà, Knoll, Kuvshinov, Schularick and Taylor, 2019, Table II](https://doi.org/10.1093/qje/qjz012){:target="_blank"}).

Each regime's mean is shifted by the same amount, so the regimes keep their spacing and the long-run geometric return is the short rate plus 3.77%, with $$w_j$$ the long-run share of regime $$j$$ and $$r_t$$ the short rate:

$$
\mu'_k = \mu_k - \sum_j w_j \mu_j + \ln(1 + 0.0377), \qquad \ln\frac{S_{t+\Delta t}}{S_t} = (\mu'_k + r_t)\,\Delta t + \sigma_k \sqrt{\Delta t}\,z_t
$$

The premium is geometric because the model compounds log returns; Table II's arithmetic premium of 5.85% with a volatility of 21.27% gives about 3.6% geometric, close to its geometric 3.77%. Every fund is listed in US dollars, so every one earns the US short rate (the policy-rule rate on [Short Rate](/projects/financescenarios/docs/interest-rates)), as interest-rate parity implies for an investor holding them in dollars. The rate is the one at the start of each step, $$r_t$$, known when the step begins, as discounting and the risk-neutral steps read it; the rate at the end of the step would add a correlation between the step's return and the rate's own shock that no data show.

## Earning the Premium over the Run's Own Inflation

For the US funds the shares $$w_j$$ in that shift are not fixed: they depend on the inflation the scenarios simulate. Taking them at one inflation level, the average over the fund's own years, leaves something out. The switching is a logit in inflation, and it is convex: the months of high inflation add more turbulence than the months of low inflation take away. A run then spends more time turbulent than that one level suggests, and earns less than the premium. Jordà et al.'s premium is an average over all the inflation history has seen, so the model should earn it on average over the inflation it simulates.

The shift is therefore set on the shares the run's own inflation gives, a simulated method of moments ([McFadden, 1989](https://doi.org/10.2307/1913621){:target="_blank"}; [Duffie and Singleton, 1993](https://doi.org/10.2307/2951768){:target="_blank"}). A pilot run simulates the calibrated US inflation alone, 2,000 paths of 100 years, and carries the expected regime probabilities along every path; the shares are their average after the first 30 years, once today's regime and inflation have worn off:

$$
p_{t+1} = p_t\,P(\pi_t), \qquad w^{\text{sim}} = \frac{1}{N\,(T - T_0)} \sum_{n=1}^{N} \sum_{t > T_0} p^{(n)}_t
$$

where $$P(\pi_t)$$ is the switching matrix at path $$n$$'s inflation in month $$t$$. The regime chain itself is never drawn, so the only sampling noise is inflation's.

On this calibration the pilot's inflation averages 2.3% and is above 5% in 12% of months. Along it US stocks are turbulent 21.1% of the time, against 20.2% at the inflation of SPY's own years. The gap looks small, but the regimes lie far apart: with the shift at 20.2%, US stocks would earn 3.44% a year over the short rate instead of the 3.70% that 3.77% promises (ln 1.0377). The default run confirms the target: over 2,000 scenarios of 30 years, US stocks earn a mean log return over the simulated short rate of 3.70% (standard error 0.07%), the target within one standard error; the shift at the fund's years' shares misses it by 3.5 standard errors. Small caps follow inflation less steeply: they are turbulent 26.6% of the time along simulated inflation and 26.7% at their own years' level, and earn 3.75% (standard error 0.09%).

The chart sets the expected share of turbulent months along the pilot run against the share at the fund's own years' inflation, and shows the mean log return of US stocks over the short rate in 30-year runs with each shift:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/markets/equity-premium" alt="The expected share of turbulent months along the pilot run of US inflation against the share at the fund's own years' inflation, and the mean log return over the short rate of US stocks in 30-year runs with each shift" %}

The gap grows with simulated inflation: with US inflation left at its fitted long-run mean rather than anchored to expectations (see [Inflation](/projects/financescenarios/docs/economy#anchoring-the-mean-to-expectations)), the run's higher inflation keeps US stocks turbulent 24% of the time, and the shift at the fund's years' shares earns about 2.7% a year.

## How Each Number Is Set

Every equity number, what kind it is and why:

| Number | Value | Kind | Why |
|:--|:--|:--|:--|
| Regimes | 2 | Judgement | A third adds little to the fit ([Hardy, 2001, section 3, p. 43](https://doi.org/10.1080/10920277.2001.10595984){:target="_blank"}) |
| Shared regimes | One stream for every market | Judgement | Markets enter and leave crises together, which brings simulated equity correlations close to the fitted ones ([Ahlgrim, D'Arcy and Gorvett, 2005, section 3](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}) |
| Long indices and their starts | Table above | Judgement | The longest monthly index of each market that needs no API key |
| US start year | 1946 | Judgement | After the deflation of the 1930s |
| Switching chances | Per index | Fitted | Baum-Welch on the long index, held fixed; for US Broad and Small Cap the inflation logit below; for Emerging Markets, the fund's own history |
| Regime means and volatilities | Per fund | Fitted | Hardy's model by maximum likelihood on the fund's monthly returns since 2000, under the index's switching |
| Inflation slopes $$\gamma$$ (US Broad, Small Cap) | +0.45 and +0.20 on the log-odds of a calm month turning turbulent rather than staying calm, per percentage point of inflation | Fitted | Expectation-maximization, CRSP market and Shiller CPI since 1946 |
| Equity premium | 3.77% (geometric) | Sourced | [Jordà et al. (2019, Table II)](https://doi.org/10.1093/qje/qjz012){:target="_blank"} |
| Regime shares the premium is earned over | US Broad 21.1% turbulent, Small Cap 26.6% | Fitted | Simulated moments: a pilot run of the calibrated US inflation, 2,000 paths, 100 years, the first 30 left out |
| Risk-free part | The simulated US short rate at the start of each step | Model choice | Dollar-listed funds; interest-rate parity |

## Other Equity Models

Other real-world equity models are options:

| Model | What it does |
|:--|:--|
| Returns above cash ([Hibbert, Mowbray and Turnbull, 2001](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"}) | The regimes fitted on returns in excess of a short rate, with the simulated short rate added back. |
| Price from dividends ([Wilkie, 1986](https://doi.org/10.1017/S0071368600009009){:target="_blank"}) | The dividend index over the dividend yield, the last link of Wilkie's cascade. |
| KNW | The equity leg of the [KNW models](/projects/financescenarios/docs/interest-rates/knw), with stochastic volatility shared with rates and inflation. |
| Switching with the business cycle | Instead of inflation, the switching chances follow the level of the OECD's US leading indicator ([Filardo, 1994](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}), fitted together with the regimes; see [Business Cycle](/projects/financescenarios/docs/economy/business-cycle#equity-crises-that-follow-the-cycle). |
| CP2022 | DNB's equity model, driven by the variance, rate and inflation of [CP2022](/projects/financescenarios/docs/interest-rates/cp2022). |

## Risk-Neutral Equities

For valuing options and guarantees, an equity must grow at the risk-free rate on average, less the dividends it pays out. A risk-neutral equity is a geometric Brownian motion at the simulated short rate $$r_t$$ less the dividend yield $$q$$,

$$
\frac{dS_t}{S_t} = (r_t - q)\,dt + \sigma\,dW_t
$$

with $$r_t$$ the run's first interest-rate factor at the start of each step and $$q$$ today's dividend yield of a `dividend_yield` entry for the same ticker, held flat; that entry is required. The volatility $$\sigma$$ comes from the option market (`volatility_source: implied`, below), from the near-the-money point of the Finance Toolkit's SVI (stochastic volatility inspired) surface at its longest expiry (`svi`), from the standard deviation of monthly log returns over the whole history (`realized`), or from Heston's stochastic volatility (below). The [martingale test](/projects/financescenarios/docs/solvency#the-martingale-test) checks that a run reproduces today's price this way.

### The Implied Volatility

With `volatility_source: implied`, each equity's volatility is read from its option chain at the first expiration at least a week out. The at-the-money volatility is the average of the out-of-the-money call and put on either side of the price. The quote nearest the price is not used on its own: for a thinly traded fund it is often an in-the-money call whose last trade is stale, and its implied volatility is far from the market's. A warning names any implied volatility more than twice or less than half the realized one. On the option chains of late October 2026, the nearest quote, the out-of-the-money average and the realized volatility are:

| Fund | Nearest quote | Out-of-the-money average | Realized |
|:--|--:|--:|--:|
| SPY | 17.8% | 17.6% | 15.2% |
| IWM | 23.2% | 23.5% | 20.1% |
| VGK | 23.0% | 18.9% | 18.6% |
| EWJ | 27.9% | 23.7% | 16.2% |
| EEM | 66.8% | 32.0% | 20.9% |

### Heston's Stochastic Volatility

A flat volatility treats a 20% fall and a 20% rise as equally likely and every horizon as equally uncertain. Option prices disagree: crash protection costs more than a bet on a rally (the skew), and a year's volatility differs from a month's (the term structure). In [Heston's (1993)](https://doi.org/10.1093/rfs/6.2.327){:target="_blank"} model the variance itself moves, returns to a long-run level and rises when prices fall:

$$
\frac{dS_t}{S_t} = (r_t - q)\,dt + \sqrt{v_t}\,dW^S_t, \qquad dv_t = \kappa(\theta - v_t)\,dt + \xi\sqrt{v_t}\,dW^v_t, \qquad dW^S_t\,dW^v_t = \rho\,dt
$$

with $$v_t$$ the variance, $$\kappa$$ its speed of mean reversion, $$\theta$$ its long-run level, $$\xi$$ the volatility of variance and $$\rho$$ the correlation that makes the skew. The calibration fits these five to the Finance Toolkit's smoothed volatility surface at the expirations nearest 1, 2, 3, 6, 9 and 12 months, on strikes within 20% of today's price; without usable options data it falls back to the realized volatility. To fit SPY:

```python
from financetoolkit import Toolkit

from financescenarios.factors.equities.equities_controller import Equities

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", benchmark_ticker=None)
params = Equities(toolkit).calibrate_heston("spy", "SPY", risk_free_rate=0.0399, dividend_yield=0.0115)
```

Which returns, on the 545 quotes of 7 October 2026:

| Parameter | Value |
|:--|--:|
| Initial variance $$v_0$$ | 0.0201 |
| Speed $$\kappa$$ | 14.62 |
| Long-run variance $$\theta$$ | 0.0219 |
| Volatility of variance $$\xi$$ | 1.18 |
| Correlation $$\rho$$ | -0.51 |
| Fit error | 0.0050 |

Today's volatility is 14.2% (the square root of 0.0201) and the long-run level 14.8%; the correlation of -0.51 produces the skew.

### Heston Paths at a Monthly Step

A variance fitted to option prices often reverts fast: in the fit above it reverts at a speed of 14.6 a year, so at a monthly step the speed times the step is above one. A full-truncation Euler step, which sets a negative variance to zero, then overshoots, and the paths no longer reproduce the prices they were fitted to. The paths therefore step with the quadratic-exponential (QE) scheme of [Andersen (2008)](https://doi.org/10.21314/jcf.2008.189){:target="_blank"}, which draws the next variance from a distribution matched to its exact mean and variance and never goes negative. A martingale correction keeps the discounted price a martingale, its expected value equal to today's price ([van Haastrecht and Pelsser, 2010, section 4.2](https://doi.org/10.1142/S0219024910005668){:target="_blank"}). On that fit, the error of one-year calls priced from 200,000 monthly paths, relative to [Heston's (1993)](https://doi.org/10.1093/rfs/6.2.327){:target="_blank"} closed-form price:

| Strike | 80 | 90 | 100 | 110 | 120 |
|:--|--:|--:|--:|--:|--:|
| Full-truncation Euler | 0.0% | +0.6% | +2.4% | +7.3% | +18.1% |
| QE with martingale correction | -0.1% | -0.1% | -0.1% | -1.2% | -3.6% |

The QE scheme's remaining error sits in the far out-of-the-money calls, whose prices are small.

## Examples

The examples on this page use the run from the [overview](/projects/financescenarios/docs#simulating-scenarios): the default settings and factor set, calibrated on 25 October 2026, with 2,000 scenarios and seed 42.

### Five Stock Markets

The default factor set holds five stock markets, each fitted to one fund: US stocks (SPY), US small caps (IWM), Europe (VGK), Japan (EWJ) and emerging markets (EEM). To simulate them:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
result = scenarios.simulate(n_simulations=2000, seed=42)

result.describe()
```

Which gives, for the stock markets, the annualized return from today to the end of the run:

| factor | terminal_mean | terminal_q05 | terminal_q95 |
|:-------|--------------:|-------------:|-------------:|
| us_broad | 0.0844 | -0.0572 | 0.2076 |
| small_cap | 0.0930 | -0.0772 | 0.2644 |
| europe | 0.0928 | -0.0757 | 0.2482 |
| japan | 0.0944 | -0.0527 | 0.2376 |
| emerging_markets | 0.0929 | -0.0995 | 0.2717 |

Every market returns between 8.44% and 9.44% a year on average, and they differ mostly in their spread: one emerging-market scenario in twenty loses more than 9.95% a year, against 5.72% for US stocks. When plotted, the 5th percentile, median and 95th percentile per market:

{% include ft-chart.html id="markets-equity-returns" src="/assets/data/financescenarios-guides/markets.json" label="5th percentile, median and 95th percentile of the five-year annualized return of US stocks, US small caps, European, Japanese and emerging-market stocks" %}

The fitted parameters show the two regimes. To read them for US stocks:

```python
calibration = scenarios.calibrate()

calibration.calibrated_params["us_broad"]
```

Which shows a calm regime with a yearly return of 9.32% and a volatility of 9.9%, and a turbulent regime with -17.24% and 21.6%. In the long run the market is turbulent 21% of the time, and a turbulent month is followed by another with a chance of 84%, so bad months cluster.

The simulated paths also give the value of an investment over time: with `levels=True`, `metric_paths` returns each fund's price paths as an array. To follow 100 invested in three of the markets:

```python
def growth_of_100(factor):
    prices = result.metric_paths(factor, levels=True)
    return 100 * prices / prices[:, :1]

index = {name: growth_of_100(factor) for name, factor in
         {"US": "us_broad", "Europe": "europe", "Emerging markets": "emerging_markets"}.items()}
```

When plotted, the median and 5-95% band of each:

{% include ft-chart.html id="markets-equity-index" src="/assets/data/financescenarios-guides/markets.json" label="Median and 5-95% band of the value of 100 invested in US, European and emerging-market stocks over five years" %}

The same arrays give the deepest fall from a peak that each scenario goes through, the drawdown an investor has to sit out on the way. To compute it per market:

```python
import numpy as np

markets = {"US": "us_broad", "US small caps": "small_cap", "Europe": "europe", "Japan": "japan",
           "Emerging markets": "emerging_markets"}

for name, factor in markets.items():
    level = growth_of_100(factor)
    worst = (level / np.maximum.accumulate(level, axis=1) - 1).min(axis=1)
    print(name, np.quantile(worst, [0.05, 0.5, 0.95]))
```

The median US scenario falls 19.6% from a peak at some point within five years and one in twenty falls 47.3% or more, against 27.2% and 60.8% for emerging markets. When plotted:

{% include ft-chart.html id="markets-drawdown" src="/assets/data/financescenarios-guides/markets.json" label="Worst 5%, median and best 5% of the deepest fall from a peak within five years, per stock market" %}

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">18</span></summary>

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. [casact.org](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}
- Andersen, L. (2008). [Simple and Efficient Simulation of the Heston Stochastic Volatility Model](https://doi.org/10.21314/jcf.2008.189){:target="_blank"}. Journal of Computational Finance, 11(3), 1-42.
- Diebold, F.X., Lee, J.-H., Weinbach, G.C. (1994). "Regime Switching with Time-Varying Transition Probabilities." In Hargreaves, C. (ed.), Nonstationary Time Series Analysis and Cointegration, 283-302. [doi.org](https://doi.org/10.1093/oso/9780198773917.003.0010){:target="_blank"}
- Duffie, D., Singleton, K.J. (1993). "Simulated Moments Estimation of Markov Models of Asset Prices." Econometrica, 61(4), 929-952. [doi.org](https://doi.org/10.2307/2951768){:target="_blank"}
- Fama, E.F., French, K.R. (1993). "Common Risk Factors in the Returns on Stocks and Bonds." Journal of Financial Economics, 33(1), 3-56. [doi.org](https://doi.org/10.1016/0304-405X(93)90023-5){:target="_blank"}
- Fama, E.F., Schwert, G.W. (1977). "Asset Returns and Inflation." Journal of Financial Economics, 5(2), 115-146. [doi.org](https://doi.org/10.1016/0304-405X(77)90014-9){:target="_blank"}
- Filardo, A.J. (1994). "Business-Cycle Phases and Their Transitional Dynamics." Journal of Business & Economic Statistics, 12(3), 299-308. [doi.org](https://doi.org/10.1080/07350015.1994.10524545){:target="_blank"}
- Hamilton, J.D. (1989). "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle." Econometrica, 57(2), 357-384. [doi.org](https://doi.org/10.2307/1912559){:target="_blank"}
- Hansen, B.E. (1992). "The Likelihood Ratio Test Under Nonstandard Conditions: Testing the Markov Switching Model of GNP." Journal of Applied Econometrics, 7(S1), S61-S82. [doi.org](https://doi.org/10.1002/jae.3950070506){:target="_blank"}
- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. [doi.org](https://doi.org/10.1080/10920277.2001.10595984){:target="_blank"}
- Harris, G.R. (1999). "Markov Chain Monte Carlo Estimation of Regime Switching Vector Autoregressions." ASTIN Bulletin, 29(1), 47-79. [doi.org](https://doi.org/10.2143/AST.29.1.504606){:target="_blank"}
- Heston, S.L. (1993). [A Closed-Form Solution for Options with Stochastic Volatility with Applications to Bond and Currency Options](https://doi.org/10.1093/rfs/6.2.327){:target="_blank"}. The Review of Financial Studies, 6(2), 327-343.
- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert Limited. [ressources-actuarielles.net](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"}
- Jordà, Ò., Knoll, K., Kuvshinov, D., Schularick, M., Taylor, A.M. (2019). "The Rate of Return on Everything, 1870-2015." Quarterly Journal of Economics, 134(3), 1225-1298. [doi.org](https://doi.org/10.1093/qje/qjz012){:target="_blank"}
- Kenneth R. French. Data Library. [mba.tuck.dartmouth.edu](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html){:target="_blank"}
- McFadden, D. (1989). "A Method of Simulated Moments for Estimation of Discrete Response Models Without Numerical Integration." Econometrica, 57(5), 995-1026. [doi.org](https://doi.org/10.2307/1913621){:target="_blank"}
- van Haastrecht, A., Pelsser, A. (2010). "Efficient, Almost Exact Simulation of the Heston Stochastic Volatility Model." International Journal of Theoretical and Applied Finance, 13(1), 1-43. [doi.org](https://doi.org/10.1142/S0219024910005668){:target="_blank"}
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. [doi.org](https://doi.org/10.1017/S0071368600009009){:target="_blank"}

</details>

{% include ft-charts-script.html %}
