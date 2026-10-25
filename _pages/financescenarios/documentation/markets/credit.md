---
title: Credit
seo_title: "Credit | Finance Scenarios"
seo_title_suffix: false
excerpt: "How Finance Scenarios simulates credit: spreads that revert in logs, a Nelson-Siegel spread curve over the government curve, and rating migration and default driven by one credit cycle as in the Basel formula."
description: "Credit in Finance Scenarios: log Ornstein-Uhlenbeck spreads and their data, the credit term structure, the one-factor credit cycle on a rating transition matrix, the CRR3 PD floor and default losses by rating."
author_profile: false
permalink: /projects/financescenarios/docs/markets/credit
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/markets
redirect_from:
    - /projects/financescenarios/docs/reference/credit
    - /projects/financescenarios/docs/reference/credit-migration
    - /projects/financescenarios/docs/reference/credit-term-structure
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-markets"
---

A corporate bond earns more than a government bond because it can default. That extra yield, the credit spread, is expected default losses plus a risk and liquidity premium that widens sharply in a downturn. Finance Scenarios models credit three ways: spreads by maturity or rating, a whole spread curve over the government curve, and the defaults themselves, as a portfolio's ratings migrate through a simulated credit cycle. All three are opt-in; the shipped factor sets leave credit off.

<div class="fs-facts">
  <div><span>Spreads</span><b>Mean reversion in logs (Ornstein-Uhlenbeck)</b></div>
  <div><span>Spread curve</span><b>Dynamic Nelson-Siegel over the government curve</b></div>
  <div><span>Migration</span><b>One-factor credit cycle on a rating transition matrix</b></div>
</div>

## Credit Spreads

A spread reverts to a normal level as an Ornstein-Uhlenbeck process in logs:

$$
d\ln s_t = a(\theta - \ln s_t)\,dt + \sigma\,dW_t
$$

Fitting it in logs is a modeling choice rather than a published specification: it keeps the spread positive and makes its swings proportional to its level, so wide spreads are the most volatile and the distribution is skewed toward sharp widenings; $$e^\theta$$ is the long-run median spread. It is fitted like every mean-reverting factor, by regressing each log spread on the one before, with the speed's small-sample bias taken off ([Tang and Chen, 2009, Theorem 3.1.1](https://doi.org/10.1016/j.jeconom.2008.11.001){:target="_blank"}), and stepped with the exact transition. A series that has touched zero or below is fitted on its level instead, and so are the GARCH and business-cycle variants, which can then turn negative. The spread data:

| Data | History |
|:--|:--|
| ICE BofA US option-adjusted spreads by maturity or rating (`AAA` to `CCC`) | Last three years only (FRED), too short for stable correlations, so the shipped factor sets leave credit off |
| Moody's `Aaa` and `Baa` yields over the 10-year Treasury | Monthly from 1953 |
| Corporate spreads for Germany ([Bundesbank](https://www.bundesbank.de/en/statistics/money-and-capital-markets){:target="_blank"}) and Australia ([RBA table F3](https://www.rba.gov.au/statistics/tables/){:target="_blank"}) | Monthly, from 1957 and 2005 |
| ECB cost of new bank loans to euro area companies ([ECB MIR](https://data.ecb.europa.eu/data/datasets/MIR){:target="_blank"}), a rate rather than a spread | Monthly from 2003 |

Euro and UK spreads by rating are not available: those indices are licensed.

## The Spread Curve

For a whole curve rather than buckets, the spread at maturity $$\tau$$ is a Nelson-Siegel curve of its own, as [Yu and Zivot (2011)](https://doi.org/10.1016/j.ijforecast.2010.04.002){:target="_blank"} apply the model of [Diebold and Li (2006)](https://doi.org/10.1016/j.jeconom.2005.03.005){:target="_blank"} to corporate spreads:

$$
s(\tau) = L + S\,B(\tau) + C\,\big(B(\tau) - e^{-\lambda\tau}\big), \qquad B(\tau) = \frac{1 - e^{-\lambda\tau}}{\lambda\tau}
$$

Each date's spreads are fitted across maturities by least squares, and the level, slope and curvature each revert as an Ornstein-Uhlenbeck process, exactly as those of the [Treasury curve](/projects/financescenarios/docs/interest-rates/yield-curve) do. The decay $$\lambda$$ is the government curve's 0.7308, so the two curves add factor by factor: the risky curve's level is the government level plus the credit level, and likewise for slope and curvature. The factors are Gaussian, so a spread can turn negative. The curves come from the Treasury's High Quality Market corporate bond spreads (2, 5, 10 and 30 years, investment grade, monthly, which need a FRED API key) or from the Open Source Bond Asset Pricing panel of TRACE trades from 2002 to 2025, a download of about 1.8 GB.

## Credit Migration and Default

Spreads price credit risk; migration models the events: downgrades, defaults and losses on a bond portfolio by rating. Each borrower's credit quality is a standard normal variable, a shared credit cycle $$Z$$ with weight $$\sqrt{\rho}$$ for asset correlation $$\rho$$ plus the borrower's own luck. A through-the-cycle transition matrix sets each rating's thresholds for upgrade, downgrade and default. In a year with cycle $$Z$$, a rating with long-run default probability $$p$$ defaults with probability

$$
p(Z) = \Phi\!\left(\frac{\Phi^{-1}(p) - \sqrt{\rho}\,Z}{\sqrt{1-\rho}}\right)
$$

where $$\Phi$$ is the standard normal distribution function. The same shift applies to every rating's threshold for "this rating or worse", so a bad year ($$Z$$ below zero) moves every rating toward downgrade and default at once. This is the one-factor approach of [Kim (1999)](https://www.msci.com/www/research-report/a-way-to-condition-transition/018440984){:target="_blank"} in the Markov rating framework of [Jarrow, Lando and Turnbull (1997)](https://doi.org/10.1093/rfs/10.2.481){:target="_blank"}, and the formula behind the Basel capital charge under the internal ratings-based (IRB) approach.

The data are ESMA's [CEREP](https://registers.esma.europa.eu/cerep-publication){:target="_blank"} rating agency statistics, which lag one to two years. The transition matrix pools the rating changes of every year in the history, so it reflects an average year across good and bad ones, as Basel asks of the estimation of probabilities of default (PD): the longest relevant observation period, with a representative mix of good and bad years ([Basel Framework, CRE36.79](https://www.bis.org/basel_framework/chapter/CRE/36.htm){:target="_blank"}). Each rating's long-run default probability is the average of its yearly default rates, floored at 0.05% so that a rating that never defaulted in the sample still carries some risk. That is the corporate PD input floor of CRR3 ([Regulation (EU) 2024/1623, Article 1, point (86)(a)](https://eur-lex.europa.eu/eli/reg/2024/1623/oj/eng){:target="_blank"}), which replaced the 0.03% of the original [CRR Article 160(1)](https://eur-lex.europa.eu/eli/reg/2013/575/oj){:target="_blank"}; the older floor remains available in Python (`pd_floor=0.0003`) for a Basel II comparison.

The cycle is backed out of the default rates year by year: for a given $$\rho$$, each year's $$Z$$ is the value whose conditional default probabilities come closest to that year's default rates per rating, weighted by $$1/(p(1-p))$$, and $$\rho$$ is set so the backed-out cycle has a variance of one. The yearly $$Z$$ is then fitted as an Ornstein-Uhlenbeck process around zero, the through-the-cycle average, and simulated with the rest of the run. Its speed $$a$$ comes from the fit, and its volatility is set to $$\sqrt{2a}$$ so the cycle keeps the variance of one the one-factor model assumes; the fit's own residual volatility gave it a variance of 1.25, which lifted the average default probability to 1.15 times the long-run one.

A portfolio's holdings migrate a year at a time through the matrix of each simulated year's $$Z$$. The loss is the cumulative share in default times the exposure times one minus the recovery rate, which is 40% for every rating unless set otherwise.

<div class="fs-callout fs-callout--limits" markdown="1">
<p class="fs-callout__title">Limits</p>

- Spreads are not derived from the ratings: model them separately as [credit spreads](#credit-spreads).
- Recovery is fixed rather than falling in downturns, and the same for every rating.
- One cycle drives all sectors and regions.
</div>

## Examples

### A Spread

The default factor set holds no credit spread, so the spread is calibrated on its own, on the ICE BofA indices through FRED. To fit the 7 to 10-year investment-grade spread and the BB spread on monthly data:

```python
from financetoolkit import Toolkit

from financescenarios.factors.credit.credit_controller import Credit

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY")  # the FRED key comes from the FRED_API_KEY variable
credit = Credit(toolkit)

credit.calibrate("ig_7_10y", maturity_bucket="7-10 Years", period="monthly")
credit.calibrate("high_yield_bb", dimension="rating", rating_bucket="BB", period="monthly")
```

Which returns, calibrated on 24 October 2026:

| name | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-----|---------------------:|--------------:|-----------:|--------------:|
| ig_7_10y | 1.4350 | -4.6009 | 0.2144 | 0.0103 |
| high_yield_bb | 4.7060 | -4.0030 | 0.3472 | 0.0196 |

The investment-grade spread starts at 1.03% and is pulled toward $$e^{-4.6009}$$ = 1.00%, a gap halving in about six months; the BB spread starts at 1.96% and heads to 1.83%. Three years of monthly data are too few for a steady speed: the bias correction takes the plain estimates of about 3 and 6.5 a year down to these. To simulate a spread next to the rest of a run:

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
credit:
  - name: ig_7_10y
    maturity_bucket: 7-10 Years
    period: monthly
```

### Defaults in a Portfolio

The credit cycle needs a run with `credit_migration` switched on. To calibrate a small yearly configuration with the credit cycle of S&P's ratings, run it ten years ahead, and follow a portfolio of 40% A, 50% BBB and 10% BB bonds:

```python
from datetime import date

from financescenarios import Scenarios, ScenariosConfig, rating_migration

config = ScenariosConfig.model_validate({
    "start_date": date(2026, 1, 1),
    "engine": {"n_simulations": 2000, "n_steps": 10, "frequency": "yearly", "seed": 42},
    "toolkit": {"start_date": date(2000, 1, 1)},
    "interest_rates": [{"name": "us_short_rate", "country": "United States", "source": "oecd", "period": "yearly"}],
    "inflation": [{"name": "inflation", "country": "United States", "period": "yearly"}],
    "equities": [{"name": "us_stocks", "ticker": "^GSPC", "period": "yearly"}],
    "credit_migration": {"enabled": True, "agency": "S&P"},
})
scenarios = Scenarios.from_config(config, api_key="FINANCIAL_MODELING_PREP_KEY")
result = scenarios.simulate(config, calibration=scenarios.calibrate(config))

migration = rating_migration(result, {"A": 40, "BBB": 50, "BB": 10}, recovery_rate=0.4)
migration.summary()
```

Which fits, on S&P's corporate ratings since 2000 (calibrated on 24 October 2026), an asset correlation of 0.10 and a cycle whose shocks halve in about a year. The summary gives the defaulted share and the loss per year; after ten years the portfolio has lost 1.87 of every 100 in the median scenario, 5.56 at the 95th percentile and 8.90 at the 99.5th, against a mean of 2.27: a bad credit cycle makes the tail far heavier than the average. When plotted, the loss per year:

{% include ft-chart.html id="credit-defaults" src="/assets/data/financescenarios-guides/credit.json" label="Median, 95th and 99.5th percentile of the cumulative default loss of a portfolio of 40% A, 50% BBB and 10% BB bonds after 40% recovery, year by year over ten years" %}

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">12</span></summary>

- Basel Committee on Banking Supervision. Basel Framework, CRE36: IRB approach: minimum requirements to use IRB approach. [bis.org](https://www.bis.org/basel_framework/chapter/CRE/36.htm){:target="_blank"}
- Deutsche Bundesbank. Money and capital markets statistics. [bundesbank.de](https://www.bundesbank.de/en/statistics/money-and-capital-markets){:target="_blank"}
- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. [doi.org](https://doi.org/10.1016/j.jeconom.2005.03.005){:target="_blank"}
- European Central Bank. MFI interest rate statistics (MIR). [data.ecb.europa.eu](https://data.ecb.europa.eu/data/datasets/MIR){:target="_blank"}
- European Securities and Markets Authority. CEREP: central repository of credit rating agencies' statistics. [registers.esma.europa.eu](https://registers.esma.europa.eu/cerep-publication){:target="_blank"}
- European Union (2013). Regulation (EU) No 575/2013 (Capital Requirements Regulation). [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/reg/2013/575/oj){:target="_blank"}
- European Union (2024). Regulation (EU) 2024/1623 amending Regulation (EU) No 575/2013 (CRR3). [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/reg/2024/1623/oj/eng){:target="_blank"}
- Jarrow, R.A., Lando, D., Turnbull, S.M. (1997). "A Markov Model for the Term Structure of Credit Risk Spreads." The Review of Financial Studies, 10(2), 481-523. [doi.org](https://doi.org/10.1093/rfs/10.2.481){:target="_blank"}
- Kim, J. (1999). "A Way to Condition the Transition Matrix on Wind." RiskMetrics Group (MSCI). [msci.com](https://www.msci.com/www/research-report/a-way-to-condition-transition/018440984){:target="_blank"}
- Reserve Bank of Australia. Statistical tables (F3: aggregate measures of Australian corporate bond spreads and yields). [rba.gov.au](https://www.rba.gov.au/statistics/tables/){:target="_blank"}
- Tang, C.Y., Chen, S.X. (2009). "Parameter Estimation and Bias Correction for Diffusion Processes." Journal of Econometrics, 149(1), 65-81. [doi.org](https://doi.org/10.1016/j.jeconom.2008.11.001){:target="_blank"}
- Yu, W.-C., Zivot, E. (2011). "Forecasting the Term Structures of Treasury and Corporate Yields Using Dynamic Nelson-Siegel Models." International Journal of Forecasting, 27(2), 579-591. [doi.org](https://doi.org/10.1016/j.ijforecast.2010.04.002){:target="_blank"}

</details>

{% include ft-charts-script.html %}
