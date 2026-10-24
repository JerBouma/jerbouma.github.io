---
title: Dated Values
seo_title: "Dated Values | Finance Scenarios"
seo_title_suffix: false
excerpt: "Why a backtest in Finance Scenarios reads every published value as it stood on the day it starts from: the neutral rate, the natural rate of unemployment, inflation expectations, targets, floors and the equity premium."
description: "Dated values in Finance Scenarios: real-time vintages of the neutral real rate, longer-run unemployment and the NAWRU, survey inflation expectations, targets, lower bounds and the equity premium, and what a 2007 fit read."
author_profile: false
permalink: /projects/financescenarios/docs/validation/dated-values
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/validation
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-validation"
---

A backtest is only honest if the model it fits could have been built on the day it starts from. Cutting every data series at that date is the obvious half. The other half is easy to miss: a calibration also reads values that are published rather than fitted, such as the neutral real rate of the policy rule, the natural rate of unemployment, long-run inflation expectations, the inflation target, the lowest policy rate and the long-run equity premium. Read as they stand today, they carry what happened afterwards into the past. A 2007 fit that reads today's neutral rate has already learned what the decade after 2007 taught. This page shows how each of these values is read as of a past date and how far they moved.

## Reading Values as Published

A calibration as of a past date therefore reads each of these values as it had been published by that date, from its official history. Every release becomes a row from the day it was published, and a run as of a date reads the latest row on or before it. The run's notes list each value it read with its source and release. A run of today reads today's values.

| Value | Read today | How a past date reads it | Rows |
|:--|:--|:--|--:|
| Neutral real rate, US | 1.2% | From 25 January 2012: the FOMC's median longer-run federal funds rate less its 2% goal, from each [Summary of Economic Projections](https://fred.stlouisfed.org/series/FEDTARMDLR){:target="_blank"}. Before: the New York Fed's [real-time Laubach-Williams estimates](https://www.newyorkfed.org/research/policy/rstar){:target="_blank"}, the last quarter's one-sided estimate of each vintage from its publication date (8 July 2005 to 27 October 2011) | 263 |
| Neutral real rate, euro area | 0.09% | The New York Fed's real-time Holston-Laubach-Williams estimates, each vintage from its publication date (3 March 2016 to 26 August 2026) | 210 |
| Neutral real rate, UK | 1.0% | The Holston-Laubach-Williams real-time estimates from March 2016 to May 2018; then the midpoint of the Bank of England's range: 0.5% from 2 August 2018 ([Inflation Report August 2018, Box 6](https://www.bankofengland.co.uk/inflation-report/2018/august-2018){:target="_blank"}), 1.0% from 6 February 2025 ([Monetary Policy Report February 2025, Box A](https://www.bankofengland.co.uk/monetary-policy-report/2025/february-2025){:target="_blank"}) | 232 |
| Longer-run unemployment, US | 4.2% | The FOMC's median from 17 June 2015 and the midpoint of its central tendency from 18 February 2009 ([FRED UNRATEMDLR and UNRATECTMLR](https://fred.stlouisfed.org/series/UNRATEMDLR){:target="_blank"}); before 2009, the Congressional Budget Office's noncyclical rate in its [earliest ALFRED vintage](https://alfred.stlouisfed.org/series?seid=NROU){:target="_blank"} (2 February 2011) | 311 |
| NAWRU (natural rate of unemployment): France, UK, Germany | 7.16%, 4.21%, 3.48% | Each release in the European Commission's [AMECO archive](https://economy-finance.ec.europa.eu/economic-research-and-databases/economic-databases/ameco-database/ameco-archive_en){:target="_blank"}, Spring 2011 to Autumn 2025, the NAWRU for its last forecast year; Spring 2026 today | 220 |
| Long-run inflation expectations, US | 2.3% | The [Survey of Professional Forecasters'](https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/inflation-forecasts){:target="_blank"} median 10-year CPI inflation from each release date since 1991Q4; before, the Blue Chip Economic Indicators and the Livingston Survey from 1979Q4 | 166 |
| Long-run inflation expectations, euro area | 2.0% | The [ECB Survey of Professional Forecasters'](https://data.ecb.europa.eu/data/datasets/SPF){:target="_blank"} longer-term HICP expectation, each round since 1999Q1 | 105 |
| Inflation target and the UK's expectation | 2% | The target in force: the Federal Reserve's 2% from 25 January 2012 ([FOMC, Statement on Longer-Run Goals](https://www.federalreserve.gov/monetarypolicy/files/fomc_longerrungoals.pdf){:target="_blank"}) and [Taylor's (1993, p. 202)](https://doi.org/10.1016/0167-2231(93)90009-L){:target="_blank"} 2% before; the ECB's 2% (below 2% from 13 October 1998, below but close to 2% from 8 May 2003, a symmetric 2% from 8 July 2021); the UK's 2.5% RPIX until 10 December 2003, then 2% CPI ([Bank of England, Inflation Report February 2004](https://www.bankofengland.co.uk/inflation-report/2004/february-2004){:target="_blank"}) | 12 |
| Lowest policy rate | US 0%, euro -0.50%, UK 0.10% | Zero, then the floor each central bank set: the federal funds range of 0 to 0.25% from 16 December 2008, the ECB's [deposit facility rate](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/html/index.en.html){:target="_blank"} at each cut from 0% on 11 July 2012 to -0.50% on 18 September 2019, [Bank Rate](https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp){:target="_blank"} at 0.10% from 19 March 2020, the UK's lowest | 11 |
| Long-run equity premium | 3.77% | [Jordà, Knoll, Kuvshinov, Schularick and Taylor (2019, Table II)](https://doi.org/10.1093/qje/qjz012){:target="_blank"} from 2019; before, the same statistic on the [JST Macrohistory Database](https://www.macrohistory.net/database/){:target="_blank"} up to each year, from 1900 to 2018 | 120 |

Before a table's first real-time release (mid-2005 for the US neutral rate, 2016 for the euro area's, 2009 for US unemployment, mid-2011 for the NAWRU), an earlier estimate stands in. For the neutral rates it is the first vintage's one-sided estimate for that quarter: made later, but on data only up to that quarter, the closest to real time there is. For longer-run unemployment and the NAWRU it is the 2011 vintages of the Congressional Budget Office and the European Commission, which estimated those earlier years with later data.

## How Far They Moved

The neutral rate matters most. At 11 of the 15 pairs of origin and currency (the ends of 2003, 2007, 2011, 2015 and 2019, for three currencies), the backtests read a neutral rate above today's. At the end of 2007 the Laubach-Williams estimate published on 20 December read 2.14% for the US, against 1.2% today, and the first Holston-Laubach-Williams vintage puts the euro area's at 2.24%, against 0.09%. The FOMC's own projection of the longer-run funds rate stood at 4.3% in January 2012, 2.3 points above its goal, and fell to 2.5% only in 2019. A policy rule given those numbers expects rates to return to normal, as the FOMC's projections did through the 2010s, while rates stayed near zero. The chart shows the neutral real rate as known on each day, with the value each origin reads:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/validation/dated-neutral-rates" alt="The neutral real rate as known on each day since 2000 for the US, the euro area and the UK, with the value each backtest origin reads and today's value" %}

Long-run inflation expectations moved far less once they had come down: US forecasters expected 6.9% a year over the next decade at the end of 1979, but since 1999 their expectation has stayed between 2.0% and 3.0% (2.3% today), and the euro area's between 1.6% and 2.2%. The chart shows them as published:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/validation/dated-inflation-expectations" alt="Long-run inflation expectations as published since 1979: the US 10-year CPI expectation, the ECB survey's longer-term expectation and the UK target" %}

The natural rate of unemployment was revised with what unemployment did: France's NAWRU read 8.8% at the end of 2007, 10.0% at the end of 2015 and 7.16% today; the UK's 6.0%, 5.8% and 4.21%. The chart shows the natural rates as known on each day:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/validation/dated-unemployment" alt="The US longer-run unemployment rate and the French and UK NAWRU as known on each day since 2000" %}

The equity premium on the data up to each year ranges from 0.74% (up to 1932) to 4.10% (up to 1999); a backtest from the end of 2007 reads 3.96%, one from the end of 2019 the published 3.77%. The chart shows the premium on the data up to each year:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/validation/dated-equity-premium" alt="The long-run equity premium computed on the JST data up to each year from 1900 to 2018, and the published 3.77%" %}

## Example

A backtest as of the end of 2007 shows what a dated read changes. To fit the default model, with the calibration settings of the [overview](/projects/financescenarios/docs#simulating-scenarios), on what was known on 31 December 2007 and print the values the US policy rule read:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
crisis = scenarios.out_of_sample(as_of="2007-12-31", years=5, n_simulations=1000, seed=42)

for note in crisis.notes:
    if note.startswith("united_states_short_rate:"):
        print(note)
```

Which shows, among other values, a neutral real rate of 2.14% as known on 31 December 2007 (today 1.20%), from the New York Fed's real-time Laubach-Williams estimate published on 20 December 2007, and a longer-run unemployment rate of 5.01% (today 4.20%), from the earliest published vintage of the Congressional Budget Office's estimate.

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">16</span></summary>

- Bank of England (2004). Inflation Report, February 2004. [bankofengland.co.uk](https://www.bankofengland.co.uk/inflation-report/2004/february-2004){:target="_blank"}
- Bank of England (2018). Inflation Report, August 2018, Box 6. [bankofengland.co.uk](https://www.bankofengland.co.uk/inflation-report/2018/august-2018){:target="_blank"}
- Bank of England (2025). Monetary Policy Report, February 2025, Box A. [bankofengland.co.uk](https://www.bankofengland.co.uk/monetary-policy-report/2025/february-2025){:target="_blank"}
- Bank of England. Bank Rate history and data. [bankofengland.co.uk](https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp){:target="_blank"}
- European Central Bank. Official interest rates: key ECB interest rates. [ecb.europa.eu](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/html/index.en.html){:target="_blank"}
- European Central Bank. Survey of Professional Forecasters (data). [data.ecb.europa.eu](https://data.ecb.europa.eu/data/datasets/SPF){:target="_blank"}
- European Commission. AMECO archive. [economy-finance.ec.europa.eu](https://economy-finance.ec.europa.eu/economic-research-and-databases/economic-databases/ameco-database/ameco-archive_en){:target="_blank"}
- Federal Open Market Committee (2026). Statement on Longer-Run Goals and Monetary Policy Strategy. [federalreserve.gov](https://www.federalreserve.gov/monetarypolicy/files/fomc_longerrungoals.pdf){:target="_blank"}
- Federal Reserve Bank of New York (2026). Measuring the natural rate of interest: Holston-Laubach-Williams and Laubach-Williams estimates, current and real-time. [newyorkfed.org](https://www.newyorkfed.org/research/policy/rstar){:target="_blank"}
- Federal Reserve Bank of Philadelphia. Inflation forecasts, real-time data research. [philadelphiafed.org](https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/inflation-forecasts){:target="_blank"}
- Federal Reserve Bank of St. Louis. ALFRED: Noncyclical Rate of Unemployment (NROU), vintages. [alfred.stlouisfed.org](https://alfred.stlouisfed.org/series?seid=NROU){:target="_blank"}
- Federal Reserve Bank of St. Louis. FRED: FOMC Summary of Economic Projections, longer-run federal funds rate (FEDTARMDLR). [fred.stlouisfed.org](https://fred.stlouisfed.org/series/FEDTARMDLR){:target="_blank"}
- Federal Reserve Bank of St. Louis. FRED: FOMC Summary of Economic Projections, longer-run unemployment rate (UNRATEMDLR). [fred.stlouisfed.org](https://fred.stlouisfed.org/series/UNRATEMDLR){:target="_blank"}
- Jordà, Ò., Knoll, K., Kuvshinov, D., Schularick, M., Taylor, A.M. (2019). "The Rate of Return on Everything, 1870-2015." Quarterly Journal of Economics, 134(3), 1225-1298. [doi.org](https://doi.org/10.1093/qje/qjz012){:target="_blank"}
- Jordà-Schularick-Taylor Macrohistory Database. [macrohistory.net](https://www.macrohistory.net/database/){:target="_blank"}
- Taylor, J.B. (1993). "Discretion versus Policy Rules in Practice." Carnegie-Rochester Conference Series on Public Policy, 39, 195-214. [doi.org](https://doi.org/10.1016/0167-2231(93)90009-L){:target="_blank"}

</details>
