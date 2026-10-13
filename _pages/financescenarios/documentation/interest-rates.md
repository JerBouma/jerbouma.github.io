---
title: Interest Rates and Yield Curves
seo_title: Interest Rates Documentation – Finance Scenarios
excerpt: "Short-rate models (Vasicek/Hull-White, CIR, Wilkie, Hibbert), what each implies for negative rates and mean reversion, Nelson-Siegel government and credit curves, and HJM."
description: "Short-rate models, Nelson-Siegel yield and credit curves and the HJM forward curve in Finance Scenarios: assumptions, implications and limits."
author_profile: false
permalink: /projects/financescenarios/docs/interest-rates
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Interest rates discount liabilities, drive bond returns and set the risk-free rate for equities and currencies. Finance Scenarios models them at three levels of detail: a single rate per country (a short-rate model), a whole government curve (Nelson-Siegel), and an arbitrage-free forward curve (HJM). A corporate spread curve can sit on top of the government curve.

Every model is fitted to market or official data, so simulated rates start from today's level and move the way history says they move. Parameter lists are in the reference pages for [InterestRates](/projects/financescenarios/docs/reference/interest-rates), [TermStructure](/projects/financescenarios/docs/reference/term-structure), [CreditTermStructure](/projects/financescenarios/docs/reference/credit-term-structure) and [Hjm](/projects/financescenarios/docs/reference/hjm).

## Short-Rate Models

A short-rate model is enough when you need one rate per country, such as a 3-month bill rate or a 10-year yield, around a normal level. Each rate is its own factor, correlated with everything else in the run.

```yaml
interest_rates:
  defaults:
    method: hull_white
  countries:
    - name: United States        # 13-week Treasury bill
    - name: United States
      ticker: "^TNX"             # 10-year Treasury yield
      term: long
    - name: Eurozone
      source: oecd
      country: Germany
```

### Hull-White (Vasicek)

The default model pulls the rate toward a long-run level $$\theta$$ at speed $$a$$, with normally distributed shocks of constant size $$\sigma$$:

$$
dr_t = a(\theta - r_t)\,dt + \sigma\,dW_t
$$

Because the shock size does not depend on the rate's level, the distribution of future rates is normal and has a left tail below zero. That is a feature after the euro, Swiss franc and yen experience of the 2010s, and a drawback when negative rates are implausible.

The speed is easiest to read as a half-life: a deviation from $$\theta$$ halves in $$\ln 2 / a$$ years. On the 13-week US Treasury bill (calibrated 2026-10-04), the rate started at 3.99% and was pulled toward 4.88% with a half-life of about eleven months, swinging by about 0.7 percentage points a year. Simulation uses the exact transition, so the step size adds no discretization error.

In a real-world run this is [Vasicek (1977)](https://doi.org/10.1016/0304-405x(77)90016-2){:target="_blank"} with one fixed level. The [Hull-White (1990)](https://doi.org/10.1093/rfs/3.4.573){:target="_blank"} extension, where $$\theta$$ becomes a time-dependent path that reproduces today's curve, is used in the risk-neutral mode. It is the general-purpose choice and the only short-rate model that supports every option on this page.

### Cox-Ingersoll-Ross

[Cox, Ingersoll and Ross (1985)](https://doi.org/10.2307/1911242){:target="_blank"} keep the same pull toward $$\theta$$ but scale the shocks by the square root of the rate:

$$
dr_t = a(\theta - r_t)\,dt + \sigma\sqrt{r_t}\,dW_t
$$

Volatility is level-dependent: as rates fall toward zero their swings shrink, and in a high-rate world they swing harder. The continuous process stays strictly positive when the Feller condition $$2a\theta \ge \sigma^2$$ holds; the fit warns when it does not. Because $$\sigma$$ is per unit of $$\sqrt{r}$$, it is not comparable with Hull-White's: 0.0448 on the 13-week bill is about 0.9 percentage points a year at a 4% rate.

Negative historical observations are floored at zero before fitting, and the simulation is an Euler approximation, so a path can dip marginally below zero. Use CIR when rates should stay positive and calm down in a low-rate environment. It has no GARCH or risk-neutral version.

### Wilkie Consols

The long government bond yield from [Wilkie's (1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf){:target="_blank"} actuarial model splits the observed yield $$C_t$$ into expected inflation and a hidden real yield $$CN_t$$:

$$
C_t = CW\,CM_t + CN_t, \qquad
CM_t = CD\,I_t + (1 - CD)\,CM_{t-1}, \qquad
\ln CN_t = \ln CMU + CA1\,(\ln CN_{t-1} - \ln CMU) + CSD\,\varepsilon_t
$$

Here $$I_t$$ is the force of inflation (the log change in the price index) from the paired inflation factor and $$CM_t$$ an exponentially weighted average of it, a simple adaptive model of inflation expectations. $$CW = 1$$ and $$CD = 0.05$$ are fixed at Wilkie's published values, so all expected inflation passes into the yield. The real part $$CN_t$$ mean-reverts in logs toward $$CMU$$ with persistence $$CA1$$, so it is always positive. This is the paper's reduced basis, where the real part is a plain AR(1).

That positivity is also its main limit: the yield must exceed average inflation over the whole fit window. US long yields sat at or below average inflation from 2008 to 2017, so the shipped Wilkie profile fits on 1995-2007 only. Use it to reproduce the Wilkie framework.

### Hibbert Two-Factor

[Hibbert, Mowbray and Turnbull (2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"} let the short rate revert toward a second, slower-moving rate $$m_t$$ instead of a fixed level:

$$
dr_t = a(m_t - r_t)\,dt + \sigma\,dW_t
$$

There is no single long-run level: the short end follows the long end, the way policy rates track the market's view of the medium term. The paper filters $$m_t$$ as a hidden state; Finance Scenarios approximates it with observable data, by default the same country's long-term rate (its own mean-reverting factor), or an exponentially weighted average of the short rate's history. It is real-world only and does not reproduce the paper's fixed correlations or closed-form bond prices.

### KNW

The KNW models simulate the nominal rate and inflation as one coupled system, each driven by the other's level, with optional shared stochastic volatility. See [KNW models](/projects/financescenarios/docs/knw).

### Comparing the Short-Rate Models

| Model | Can go negative? | Reverts toward | Volatility | Best for |
|:------|:-----------------|:---------------|:-----------|:---------|
| Hull-White (Vasicek) | Yes | A fixed level, or an anchor path | Constant, or GARCH | General use; supports every option |
| Cox-Ingersoll-Ross | No in theory if Feller holds; a simulated path can dip marginally below | A fixed level | Scales with $$\sqrt{r}$$ | Positive rates, smaller swings near zero |
| Wilkie consols | The real part cannot | A fixed level for the log real yield | Constant | Reproducing Wilkie (1986) |
| Hibbert two-factor | Yes | A moving target: the long rate | Constant | Short rates that follow long rates |
| KNW | Yes | A joint level with inflation | Constant, or shared stochastic | Rates and inflation that drive each other |

## Data and Long-Run Levels

None of the short-rate sources needs an API key: Yahoo Finance Treasury yields (13-week, 5, 10 and 30 years) give daily US data, the OECD short and long rates cover about 38 member countries monthly, and the Global Macro Database adds yearly rates for countries outside the OECD, such as Brazil, India and China.

A recent five- or ten-year window says little about a rate's long-run level: the half-life is often years, so the sample holds only a handful of independent cycles. Two remedies apply to real-world Hull-White and CIR entries:

- **Long history.** Fit speed, volatility and long-run level on decades or centuries of yearly data (OECD from 1950, UK rates from 1694, bill rates across countries from 1870), while today's level still comes from current data.
- **Long-run anchor.** Replace the single fitted $$\theta$$ with a path of forward rates from EIOPA's risk-free curve for USD, EUR or GBP, ending at the ultimate forward rate (UFR), so simulated rates converge where the Solvency II curve says they should. An alternative follows the median of De Nederlandsche Bank's scenario set for euro rates.

The shipped default factor set uses both. See [Long history](/projects/financescenarios/docs/configuration#long-history) and [Anchoring long-run rate levels](/projects/financescenarios/docs/configuration#anchoring-long-run-rate-levels).

## Your Own Views

A belief replaces one fitted parameter and keeps the rest, for example a house view on the long-run level:

```yaml
interest_rates:
  countries:
    - name: United States
      beliefs:
        long_run_mean: 0.035
```

Beliefs apply to Hull-White and CIR with constant volatility. They are rejected for risk-neutral rates, where they would break the match to market prices.

## Keeping Rates at or Above Zero

The zero lower bound follows the shadow-rate idea of [Black (1995)](https://doi.org/10.1111/j.1540-6261.1995.tb05182.x){:target="_blank"}: the model evolves an unconstrained shadow rate $$s_t$$, and the observed rate is $$r_t = \max(s_t, 0)$$. A rate at zero only climbs back once the shadow rate does, so it can stay at zero for a long spell, as policy rates did after 2008.

```yaml
interest_rates:
  countries:
    - name: Eurozone
      source: oecd
      country: Germany
      zero_lower_bound: true
```

It is off by default, because negative rates did happen. It is real-world only, since a floor breaks a risk-neutral rate's exact fit to today's curve.

## Time-Varying Volatility (GARCH)

With [GARCH(1,1)](https://doi.org/10.1016/0304-4076(86)90063-1){:target="_blank"} (Bollerslev, 1986) the Hull-White drift stays, but the variance of the next shock depends on the last one:

$$
h_{t+1} = \omega + \alpha\,\varepsilon_t^2 + \beta\,h_t, \qquad \alpha + \beta < 1
$$

A large move raises next period's variance, which then fades back toward its long-run value. Calm and turbulent periods cluster, and rate changes get fatter tails than under constant volatility. It is available for Hull-White only and is used as fitted, without beliefs.

## Business-Cycle Conditioning

Rates can also respond to the economy on top of their own mean reversion, through a drift term on the change in the leading indicator whose sign and size are fitted on history. See [conditioning on the cycle](/projects/financescenarios/docs/economy#conditioning-on-the-cycle).

## Real-World and Risk-Neutral Rates

Market-consistent valuation, such as a Solvency II best estimate, needs rates whose expected discounting reproduces today's bond prices. Hull-White has two risk-neutral versions:

- **Flat path.** Today's rate is held constant along every path; no speed or volatility is fitted, since no market price would discipline them.
- **Forward curve.** $$\theta$$ becomes a time-dependent path chosen so that the model reproduces today's forward curve (a Nelson-Siegel fit to the four Treasury yields), following [Brigo and Mercurio (2006, section 3.3)](https://doi.org/10.1007/978-3-540-34604-3){:target="_blank"}.

```yaml
interest_rates:
  countries:
    - name: United States
      measure: risk_neutral
      risk_neutral_forward_curve: true
```

The main simplification: speed and volatility in forward-curve mode are historical, since there are no cap or swaption prices to fit. See [Real-world and risk-neutral measures](/projects/financescenarios/docs/configuration#real-world-and-risk-neutral-measures).

## The Nelson-Siegel Yield Curve

Repricing a bond portfolio or a liability profile along each scenario needs yields at every maturity that move together consistently. The dynamic Nelson-Siegel model of [Diebold and Li (2006)](https://doi.org/10.1016/j.jeconom.2005.03.005){:target="_blank"}, built on [Nelson and Siegel (1987)](https://doi.org/10.1086/296409){:target="_blank"}, writes the yield at maturity $$\tau$$ as three factors:

$$
y(\tau) = L + S\,\frac{1 - e^{-\lambda\tau}}{\lambda\tau} + C\left(\frac{1 - e^{-\lambda\tau}}{\lambda\tau} - e^{-\lambda\tau}\right)
$$

- **Level** $$L$$ moves every maturity equally: a parallel shift. It is the long end of the curve and tracks long-run inflation expectations and the neutral rate.
- **Slope** $$S$$ moves short maturities more than long ones. The very short end is $$L + S$$, so a negative slope is a normal upward curve and a positive one an inverted curve; it moves with monetary policy and the cycle.
- **Curvature** $$C$$ moves medium maturities most: a hump or a trough in the belly of the curve.

The decay $$\lambda$$ (0.7308 by default, as in Diebold and Li) fixes where the curvature loading peaks. The factors are fitted to observed yields on every historical date, then each is simulated as its own mean-reverting process, correlated with the rest of the model.

```yaml
yield_curve:
  enabled: true
  source: government
  country: Germany
  period: monthly
```

The curve can come from the four Yahoo Treasury yields, the official 12-maturity US Treasury par curve (which needs an FMP key), or the official government curve of the United States, the Euro Area (ECB), Germany, the United Kingdom, Japan, Canada, Sweden or Norway. The simulated factors convert to a yield at any maturity, and to statistics such as how often the curve inverts:

```python
from financescenarios import Scenarios
from financescenarios.factors.term_structure.term_structure_model import (
    curve_inversion_frequency,
    nelson_siegel_yield,
)

# Every shipped factor set built on broad (default, core, us_only) includes the Nelson-Siegel curve
result = Scenarios.from_profiles(settings="default", factor_set="default").simulate(n_simulations=1000)
level, slope, curvature = (result.paths[name] for name in ("rate_level", "rate_slope", "rate_curvature"))

ten_year = nelson_siegel_yield(level, slope, curvature, tenor=10.0, decay=0.7308)  # scenarios x steps
inverted = curve_inversion_frequency(level, slope, curvature, short_tenor=0.25, long_tenor=10.0, decay=0.7308)
```

### Limits

- Four Yahoo maturities capture level, slope and curvature, not precise pricing, and their daily slope is noisy (a half-life of about 1.5 months on 2021-2026 data, against about 1.5 years on the Treasury curve).
- The Bank of England curve has only the 5, 10 and 20-year points, so the UK short end is an extrapolation. Japanese yields have risen steadily since 2000, so the level shows no mean reversion and the fit stops with an error.
- The factors are statistical and real-world, with no guarantee against arbitrage between maturities; for that, use HJM.
- Yields are used as quoted (semiannual, bond-equivalent), not converted to continuous compounding.

## The Credit Spread Curve

A corporate bond is discounted at the government curve plus a spread for default and liquidity risk. The credit curve applies the same Nelson-Siegel model to corporate spreads, adding credit level, slope and curvature factors. With the same $$\lambda$$ on both curves, their sum is again a Nelson-Siegel curve: the discount curve for risky bonds.

```yaml
credit_term_structure:
  enabled: true
  source: hqm
  period: monthly
```

Two sources are available:

- The US Treasury's [High Quality Market corporate bond curve](https://home.treasury.gov/data/treasury-coupon-issues-and-corporate-bond-yield-curves){:target="_blank"} minus the Treasury par curve, monthly from 1984: an investment-grade (AAA to A) spread curve, the one US pension plans discount with. It needs a free FRED key.
- The [Open Source Bond Asset Pricing](https://openbondassetpricing.com/){:target="_blank"} panel of US corporate bond trades (TRACE), July 2002 to March 2025, with spreads over the government curve of [Liu and Wu (2021)](https://doi.org/10.1016/j.jfineco.2021.05.059){:target="_blank"}. The curve starts from the panel's last month, not today.

Monthly data is the default: daily single-bond spreads carry bid/ask bounce that would fit an unrealistically fast mean reversion.

Limits: the bond panel has no ratings, so its curve averages across all bonds (for rating migration see [CreditMigration](/projects/financescenarios/docs/reference/credit-migration)). The factors are not arbitrage-free; neither the arbitrage-free Nelson-Siegel model of [Christensen, Diebold and Rudebusch (2011)](https://doi.org/10.1016/j.jeconom.2011.02.011){:target="_blank"} nor the [Svensson (1994)](https://doi.org/10.3386/w4871){:target="_blank"} extension is implemented, and default intensities in the sense of [Duffie and Singleton (1999)](https://doi.org/10.1093/rfs/12.4.687){:target="_blank"} are not modeled.

## HJM: An Arbitrage-Free Forward Curve

Every other rate model here learns its drift from history. In [Heath, Jarrow and Morton (1992)](https://doi.org/10.2307/2951677){:target="_blank"} you specify only how volatile each forward rate $$f(t,T)$$ is, and absence of arbitrage then fixes the drift under the risk-neutral measure:

$$
df(t,T) = \alpha(t,T)\,dt + \sigma(t,T)\,dW_t, \qquad \alpha(t,T) = \sigma(t,T)\int_t^T \sigma(t,u)\,du
$$

The drift is the convexity adjustment that makes discounted bond prices martingales, not a free parameter. Use HJM when the simulated curve must be arbitrage-free by construction, as in market-consistent valuation; use the Nelson-Siegel curve when curves should behave like history.

Finance Scenarios uses two correlated factors whose volatility fades with time to maturity $$x$$ as $$\sigma_i e^{-\kappa_i x}$$, which makes it the two-factor Hull-White (G2++) model ([Hull and White, 1994](https://doi.org/10.3905/jod.1994.407908){:target="_blank"}; [Brigo and Mercurio, 2006](https://doi.org/10.1007/978-3-540-34604-3){:target="_blank"}, chapters 3-4). Both factors start at zero on top of today's forward curve (a Nelson-Siegel fit to the Treasury yields), so the model reproduces today's curve exactly at every maturity.

```yaml
hjm:
  enabled: true
  period: daily
  kappa_bounds: [0.01, 6.0]   # search range for the volatility decays
```

The volatilities, decays and correlation are chosen so that the model's forward-rate covariance best matches how historical forwards from 3 months to 30 years moved together, in the principal-component spirit of [Litterman and Scheinkman (1991)](https://doi.org/10.3905/jfi.1991.692347){:target="_blank"}. On daily data from October 2021 to October 2026, factor 1 was a slow, level-like movement (1.32% a year, fading little across 30 years) and factor 2 a fast short-end movement (5.18% a year, halved within five months of maturity). Ten years out, convexity added 0.56 to 1.44 percentage points to the expected forward rate, rising with maturity.

### Assumptions and Limits

- **Zero term premium by default.** Future rates equal today's forwards plus convexity, with no extra yield for holding long bonds. All other rate factors are real-world, so adding HJM to a real-world run mixes two measures.
- **Long horizons.** The slow factor often fits near its lowest allowed decay, which makes convexity and the spread of long rates grow for decades; a 50-year projection there is not credible. Raising the lower decay bound (for example to 0.03-0.10) is defensible.
- **Limited shapes.** Volatility can only fall with maturity, while observed volatility curves are usually humped. Without cap or swaption prices, volatility is fitted to history, and the fast factor's decay is weakly identified.
