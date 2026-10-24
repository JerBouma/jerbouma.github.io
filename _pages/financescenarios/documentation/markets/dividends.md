---
title: Dividends
seo_title: "Dividends | Finance Scenarios"
seo_title_suffix: false
excerpt: "How Finance Scenarios simulates dividends: a mean-reverting log dividend yield after Ahlgrim, D'Arcy and Gorvett, and dividend growth in Wilkie's cascade from inflation to share prices."
description: "Dividends in Finance Scenarios: the log dividend yield as an Ornstein-Uhlenbeck process, Wilkie's dividend growth with smoothed inflation and the unit gain, and the cascade to share prices."
author_profile: false
permalink: /projects/financescenarios/docs/markets/dividends
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/markets
redirect_from:
    - /projects/financescenarios/docs/reference/dividend-yield
    - /projects/financescenarios/docs/reference/dividend-growth
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-markets"
---

A stock's total return is price plus dividends, and for most runs that is all a portfolio needs. When the dividend income matters on its own, for an income target, a pension that pays out of dividends or a model that values shares from their dividends, it is simulated separately: the dividend yield as a mean-reverting factor, and dividend growth in the cascade of [Wilkie (1986)](https://doi.org/10.1017/S0071368600009009){:target="_blank"}, in which inflation drives dividends and dividends drive share prices.

## Dividend Yield {#dividend-yield}

Following eq. 3.17 of [Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf#page=20){:target="_blank"}, who follow Wilkie and [Hibbert, Mowbray and Turnbull (2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"}, the log of the yield $$Y_t$$ mean-reverts, so the yield stays positive:

$$
d\ln Y_t = a(\theta - \ln Y_t)\,dt + \sigma\,dW_t
$$

It is fitted by regressing each log yield on the one before and stepped with the exact transition; $$e^\theta$$ is the long-run median yield. A belief about the normal level is set in logs too ($$\ln 0.02$$ for 2%). For SPY, fitted on 4 October 2026:

<div class="ca-nums fs-nums">
  <span><b>0.99%</b>starting yield</span>
  <span><b>1.39%</b>long-run median yield</span>
  <span><b>4.7 years</b>half-life of a gap</span>
</div>

On 1871-2003 data Ahlgrim, D'Arcy and Gorvett found the speed statistically indistinguishable from zero, so a short window may show no reversion at all. An optional inflation term links the yield to inflation: by default on the same step's change in inflation, or on its level, the form Wilkie uses (`inflation_term: level`).

## Dividend Growth (Wilkie)

Wilkie's model is a one-way cascade: inflation, then the dividend yield, dividend growth and the share price (the dividend index divided by the yield). Dividend growth is his Reduced Standard Basis equation ([section 3.9](https://doi.org/10.1017/S0071368600009009){:target="_blank"}), a slightly simpler form that he found gives very similar long-term results:

$$
\Delta \ln D_t = \mu_D + d_W\,M_t + d_X\,\Delta\ln Q_t + d_Y\,\varepsilon^Y_{t-1} + \sigma_D\,z_t, \qquad d_W + d_X = 1
$$

with $$D_t$$ the dividend index and $$\Delta\ln Q_t$$ the inflation over the step: in the `wilkie` factor set Wilkie's force of inflation (the log change of the price index), elsewhere the paired inflation rate times the step. Term by term:

| Term | Wilkie | Economics |
|:-----|:-------|:----------|
| $$\mu_D$$ | DMU | Real dividend growth |
| $$d_W\,M_t$$ | DW | Smoothed inflation, $$M_t = 0.2\,\Delta\ln Q_t + 0.8\,M_{t-1}$$ a year: dividends catch up with prices over time |
| $$d_X\,\Delta\ln Q_t$$ | DX | Part of this period's inflation passes straight into dividends |
| $$d_Y\,\varepsilon^Y_{t-1}$$ | DY | The dividend yield's earlier surprise: prices anticipate dividend changes, so the yield moves first. By default the surprise one step back; a year back, as Wilkie reads it, with `yield_residual_lag: year` |
| $$\sigma_D\,z_t$$ | DSD | The dividend index's own shock |

The two inflation weights add up to one, Wilkie's unit gain ([section 3.7](https://doi.org/10.1017/S0071368600009009){:target="_blank"}): in the long run dividends, and so share prices, keep their real value. The fit imposes the unit gain, fixes the smoothing weight at Wilkie's 0.2 a year (converted to the step as $$1 - 0.8^{\Delta t}$$) and estimates the rest by one regression.

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

Wilkie fitted UK data from 1919 to 1982. The `wilkie` factor set runs his equations with his published parameters from his neutral start, dated 1986, and reads no data.

## Example

The `wilkie` settings and factor set run Wilkie's whole cascade, 1,000 scenarios of 100 years in yearly steps, with no data and no API key ([Published Models](/projects/financescenarios/docs/validation/published-models)). To run it and read the dividend yield and dividend growth off after 1, 10 and 30 years:

```python
from financescenarios import Scenarios

wilkie = Scenarios.from_profiles(settings="wilkie", factor_set="wilkie").simulate(seed=42)

wilkie.horizon_summary([1, 10, 30], factors=["dividend_yield", "dividend_growth"])
```

Which gives, among other columns, the yield as a rate and dividend growth as the yearly growth of the dividend index since the start:

| factor | horizon | q0.05 | q0.5 | q0.95 |
|:-------|--------:|------:|-----:|------:|
| dividend_yield | 1 | 0.0314 | 0.0427 | 0.0586 |
| dividend_yield | 10 | 0.0284 | 0.0424 | 0.0629 |
| dividend_yield | 30 | 0.0292 | 0.0431 | 0.0625 |
| dividend_growth | 1 | -0.1161 | 0.0514 | 0.2383 |
| dividend_growth | 10 | -0.0236 | 0.0536 | 0.1288 |
| dividend_growth | 30 | -0.0001 | 0.0506 | 0.1038 |

The yield holds near its 4.3% start in the median scenario, within a band of about 3% to 6%. Dividends grow by about 5% a year in the median scenario, close to Wilkie's mean inflation of 5%, which the unit gain passes through, and the range of their yearly growth narrows with the horizon as good and bad years average out. When plotted, one variable per tab:

{% include ft-chart.html id="dividends-wilkie" src="/assets/data/financescenarios-guides/published-models.json" label="Median, 25-75% and 5-95% band of the dividend yield and of the yearly growth of the dividend index in Wilkie's model over 100 years" %}

To simulate SPY's dividend yield next to the default run instead, add an entry to a factor set of your own; the `broad` set holds one:

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
dividend_yield:
  - name: spy_yield
    ticker: SPY
```

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">3</span></summary>

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. [casact.org](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}
- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert Limited. [ressources-actuarielles.net](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"}
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. [doi.org](https://doi.org/10.1017/S0071368600009009){:target="_blank"}

</details>

{% include ft-charts-script.html %}
