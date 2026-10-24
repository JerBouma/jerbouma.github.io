---
title: Expected Path
seo_title: "Expected Path | Finance Scenarios"
seo_title_suffix: false
excerpt: "Where the short rate starts from: the path the bond market expects, read off each government curve as forward rates less the term premium, with each currency's own premium from the regressions of Adrian, Crump and Moench."
description: "The market's expected short-rate path in Finance Scenarios: forward rates less the term premium, each currency's own ACM term premium, a stale OECD print, the path past the curve and the rule acting on surprises."
author_profile: false
permalink: /projects/financescenarios/docs/interest-rates/expected-path
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/interest-rates
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-interest-rates"
---

On its own, the policy rule sends every scenario along the rule's own expected path from wherever today's rate is: with US inflation a little above target, the path climbs or falls toward 3.2% within a year or two, whatever the bond market prices. The yield curve already says where investors expect the short rate to go, so the default reads that expectation off the curve and lets the rule act only on what the market could not know: each scenario's own inflation and unemployment surprises. This page covers how the path is read off each government curve, how it continues past the curve, and how the rule acts on top of it.

## Forward Rates Less the Term Premium

A forward rate is what the curve lets you lock in today for borrowing in a future year, so it is the short rate expected for that year plus a premium for bearing interest-rate risk until then. [Adrian, Crump and Moench (2013, section 2.4)](https://doi.org/10.1016/j.jfineco.2013.04.009){:target="_blank"} split each yield into the average short rate expected over the bond's life and that term premium. Taking the premium's forward part out of each year's forward rate leaves the expected path:

$$
m\!\left(n - \tfrac{1}{2}\right) = \underbrace{n\,z(n) - (n-1)\,z(n-1)}_{\text{forward rate for year } n} - \underbrace{\big(n\,\text{TP}(n) - (n-1)\,\text{TP}(n-1)\big)}_{\text{its premium}}, \qquad m(0) = r_0
$$

with $$z(n)$$ the continuously compounded zero rate and $$\text{TP}(n)$$ the term premium of an $$n$$-year yield. If the premium were left in, the forward rates themselves would be read as expected short rates, and a long rate built on them would carry the premium twice. The curves are the New York Fed's own fit of the Treasury zero curve for the dollar (the yields its premium is estimated on), the Deutsche Bundesbank's zero curve of German Federal securities for the euro ([Deutsche Bundesbank, term structure of interest rates](https://www.bundesbank.de/en/statistics/money-and-capital-markets/interest-rates-and-yields/term-structure-of-interest-rates){:target="_blank"}) and the Bank of England's gilt spot curve for the pound ([Bank of England, yield curves](https://www.bankofengland.co.uk/statistics/yield-curves){:target="_blank"}), each on the calibration day. Past today, the dollar's path is quoted as the 13-week bill's bank discount rate, the basis ^IRX quotes on ([US Treasury, Daily Treasury Bill Rates](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_bill_rates&field_tdr_date_value=202610){:target="_blank"}), so the path and the rate it starts from share one basis.

## Each Currency's Own Term Premium

The New York Fed publishes the dollar's premium. For the euro and the pound no official estimate exists, so each gets its own, from the same method run on its own curve, as [Malik and Meldrum (2016, section 3)](https://doi.org/10.1016/j.jbankfin.2016.02.006){:target="_blank"} run it on gilts. The regressions of [Adrian, Crump and Moench (2013, sections 2.3-3.1)](https://doi.org/10.1016/j.jfineco.2013.04.009){:target="_blank"} take three steps:

1. Five principal components of the 3- to 120-month yields are the curve's pricing factors, and a vector autoregression moves them from month to month.
2. The monthly excess returns of twelve zero-coupon bonds (6, 12, ..., 60, 84 and 120 months) over the short rate are regressed on a constant, the factors' innovations (their unexpected moves) and the factors' lagged levels.
3. A cross-sectional regression of those coefficients gives the prices of risk, and the term premium of each maturity is the yield the fitted model gives less the yield it gives with the prices of risk set to zero, read each month from that month's factors.

The curves are the Bundesbank's month-end curve from September 1972 and the Bank of England's from January 1970, neither of which needs an API key. The short rate is each country's OECD 3-month rate, the rate the euro and pound short rates simulate; below a curve's first maturity, yields are filled in linearly from that short rate, as Malik and Meldrum (2016, note 2) fill the gilt curve from Bank Rate. The sample stops at the calibration date, so a backtest never sees a later month. When the fit cannot be made (fewer than 120 months, no readable short rate, or fitted yields more than 50 basis points off the curve on average), the Treasury premium stands in: term premia move together across countries ([Wright, 2011](https://doi.org/10.1257/aer.101.4.1514){:target="_blank"}; [Jotikasthira, Le and Lundblad, 2015](https://doi.org/10.1016/j.jfineco.2014.09.004){:target="_blank"}).

The code is checked against a known answer: run on the Treasury curve of [Gürkaynak, Sack and Wright (2007)](https://doi.org/10.1016/j.jmoneco.2007.06.029){:target="_blank"} with the 3-month bill as the short rate, it reproduces the New York Fed's 10-year term premium (ACMTP10) over 1961-2026 to -0.2 basis points on average (4.1 basis points mean absolute error, 16 at most), and on a synthetic one-factor affine curve it recovers the true 10-year premium within 1 basis point. For the euro and the pound, the fits give:

| | Euro (Bundesbank curve) | Pound (Bank of England curve) |
|:--|--:|--:|
| Months fitted | 649 (September 1972 to September 2026) | 482 (January 1986 to February 2026) |
| Yields fitted within (RMSE) | 5.2 basis points | 5.7 basis points |
| 10-year premium, mean (standard deviation) | 1.22% (1.07) | 1.13% (1.20) |
| 10-year premium, last month-end | 0.37% | 0.90% |
| Correlation with the US ACMTP10 | 0.58 | 0.89 |

The chart sets both premia against the New York Fed's:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/own-term-premia" alt="The euro and pound 10-year term premia from their own government curves against the New York Fed's ACMTP10, month-ends since 1972" %}

The premia rose with the inflation of the 1970s and 1980s and fell toward zero in the 2010s, as the dollar's did; the pound's follows the dollar's more closely than the euro's. The simulated euro and pound rates are interbank rates, which sit above the government 3-month zero rate (Germany by about 9 basis points before 1999 and 30 since, the UK by 33), and that spread sits in the estimated premium, as the bill-to-curve gap sits in the New York Fed's.

## When the OECD Print Is Stale

The OECD's 3-month rate comes out with a lag, and for the pound it stopped at February 2026. Starting a run on 19 October 2026 from that print would start the pound at 3.62%, while the 6-month gilt zero rate had since gone from 3.45% to 4.18%. When a euro or pound print is more than a full month old, the run starts from that print carried forward by the change in a fresher rate of the same currency, so the OECD level is kept:

$$
r_0 = r^{\text{OECD}}_{\text{last}} + \big(x_{\text{latest}} - x_{\text{OECD's last month}}\big)
$$

where $$x$$ is the fresher rate: the 3-month point between the overnight benchmark and the shortest maturity of the month-end government curve, interpolated linearly in maturity. $$x_{\text{latest}}$$ is its value in the latest month it covers before the calibration month. For the pound the two ends are SONIA's monthly average ([Bank of England, SONIA](https://www.bankofengland.co.uk/markets/sonia-benchmark){:target="_blank"}) and the 6-month zero of the gilt curve, so the point sits halfway; for the euro the monthly average of the euro short-term rate, €STR ([ECB, euro short-term rate](https://www.ecb.europa.eu/stats/financial_markets_and_interest_rates/euro_short-term_rate/html/index.en.html){:target="_blank"}) and the 1-year zero of the Bundesbank curve, so it sits a quarter of the way. The weights follow from the maturities and are not fitted. The overnight rate alone misses the policy changes a 3-month rate already prices, and the curve's shortest point alone overstates its moves (it would put the pound at 4.35%, well above Bank Rate at 3.75%). Carried six months forward from every past month, the 3-month point lands 16 basis points from the rate the OECD later printed for the UK since 2015 (against 67 for the stale print) and 12 for Germany since November 2019 (against 84).

On the calibration day the pound starts at 3.99%: February's 3.62% carried to September with the 0.37-point rise of the 3-month point. Germany's OECD series runs to September, so the euro start is the print itself, and the dollar starts from the daily ^IRX. Only the starting rate changes, along with what reads it (the market path's first point and the short end of today's curve in the pound's own premium); the policy rule, the correlations and the term premia are still fitted on the rates as the OECD printed them.

## Past the Curve

The curve is read for ten years, the longest maturity the premium is estimated for. After that the path closes its gap to the rule's steady state at the short rate's own speed of mean reversion $$a$$, the speed the [long rate](/projects/financescenarios/docs/interest-rates/long-rate#the-expected-path) reads it with, so the path and the long rate describe one expected path ([Vasicek, 1977, section 5, eq. 25](https://doi.org/10.1016/0304-405x(77)90016-2){:target="_blank"}; [Campbell and Shiller, 1991](https://doi.org/10.2307/2298008){:target="_blank"}):

$$
m(H + s) = m_{ss} + \big(m(H) - m_{ss}\big)\,e^{-a s}, \qquad H = 10 \text{ years}, \quad m_{ss} = \max(r^* + \pi^*, \text{floor})
$$

The speed is the short rate's own rather than the convergence speed of EIOPA's risk-free curves ([EIOPA, RFR technical documentation, 2026](https://www.eiopa.europa.eu/eiopa-publishes-rfr-technical-documentation-become-applicable-30-january-2027-2026-05-26_en){:target="_blank"}), which belongs to EIOPA's method for extrapolating a curve, not to how the short rate is expected to move. With $$a$$ at 0.057 (dollar), 0.133 (euro) and 0.043 (pound) a year, a gap at ten years halves in 12, 5 and 16 years.

On the calibration day the dollar path rises from today's 4.08% to a peak of 4.43% in the second year and is back at 4.07% in the tenth; the euro's peaks at 3.43% and the pound's, from its carried-forward 3.99%, at 5.17%. Past the curve each heads for its steady state, which the pound and the dollar, with the slowest speeds, are still well above after thirty years (the dollar at 3.48%). The chart shows the three paths, on the curve for ten years and past it after that:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/market-path" alt="The expected short rate for the dollar, the euro and the pound: forward rates less the term premium for ten years, then converging to the rule's steady state" %}

## The Rule Acts on the Surprises

Each scenario's rate follows the market path $$m(t)$$, and the rule acts on the gap between that scenario's inflation and unemployment and their expected paths $$\bar\pi_t$$ and $$\bar u_t$$. In the step of the [short rate](/projects/financescenarios/docs/interest-rates#the-policy-rule), a target built on the market path takes the place of the rule's prescription $$R^*(\pi_t, u_t)$$:

$$
\tilde R_t = m(t) + R^*(\pi_t, u_t) - R^*(\bar\pi_t, \bar u_t)
$$

and each step adds the path's own move, so a scenario whose inflation and unemployment stay on their expected paths stays on the market's path instead of lagging behind it:

$$
s_{t+\Delta t} = \tilde R_t + (s_t - \tilde R_t)\,e^{-\kappa \Delta t} + \big(m(t + \Delta t) - m(t)\big) + \sigma \sqrt{\frac{1 - e^{-2\kappa\Delta t}}{2\kappa}}\;\varepsilon_t
$$

This is the deterministic shift of [Brigo and Mercurio (2001)](https://doi.org/10.1007/pl00013541){:target="_blank"}: the model starts from any expected path while its dynamics stay its own. The rule's weights, speed, volatility and floor are unchanged, but what the market already priced in is not counted again. A regime that lifts inflation by a point in every scenario lifts the rate's target by 1.5 points, as the rule's own path would. The expected paths are the calibrated model's median inflation and unemployment without regimes, beliefs or shocks, worked out once at calibration from 4,000 scenarios and stored with it. They are medians because inflation's rare high spells lift its average above where most scenarios are. The level $$u^*$$ the rule measures slack from appears in both terms, so it cancels.

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">The starting premium's quoting basis</p>

On 15 October 2026 the US 10-year term premium at the start of a run, the 10-year yield less the expected path, sat 11 basis points above the New York Fed's ACMTP10. About 2.4 basis points of that is ^TNX quoting a par yield where the path is read off zero rates, and about 8.5 the 13-week bill's bank discount quote. Converting ^TNX alone would leave the term premium fitted on unconverted OECD history, an inconsistency of the same size. Both legs and that history would have to be converted together, so the gap is left in place.
</div>

## Data Choices

Which data the path is read from, and why:

| Choice | Kind | Why |
|:--|:--|:--|
| The market path reads each government curve for ten years | Judgement | Ten years is the longest maturity the term premia are estimated for |
| The euro and pound premia come from their own month-end curves over each OECD 3-month rate | Judgement | No official premium exists for either; their own curves price their own risk, and the 3-month rate is the one each short rate simulates. The US premium stands in only when the fit cannot be made |

## Example

The path of each currency is stored with the calibration. To read it from the calibration of 19 October 2026 that the [overview](/projects/financescenarios/docs#keeping-a-run) saved:

```python
from financescenarios import CalibrationResult

calibration = CalibrationResult.load("calibration.json")

for country in ["united_states", "eurozone", "united_kingdom"]:
    market_path = calibration.calibrated_params[f"{country}_short_rate"].market_path
    print(country, market_path.times, market_path.rates)
```

Which gives, for the US, a short rate of 4.32%, 4.42%, 4.27% and 4.07% in one, two, five and ten years, from the New York Fed's fit of the Treasury curve of 15 October 2026, after which the path heads to the rule's steady state of 3.20%. The euro area's path comes from the Bundesbank's curve and the UK's from the Bank of England's. When plotted, the three paths over the next ten years:

{% include ft-chart.html id="interest-rates-market-path" src="/assets/data/financescenarios-guides/interest-rates.json" label="Expected short-rate path of the US, the euro area and the UK over ten years, from each central bank's government curve" %}

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">14</span></summary>

- Adrian, T., Crump, R.K., Moench, E. (2013). "Pricing the Term Structure with Linear Regressions." Journal of Financial Economics, 110(1), 110-138. [doi.org](https://doi.org/10.1016/j.jfineco.2013.04.009){:target="_blank"}
- Bank of England. SONIA interest rate benchmark. [bankofengland.co.uk](https://www.bankofengland.co.uk/markets/sonia-benchmark){:target="_blank"}
- Bank of England. Yield curves: nominal spot curve of gilts, daily and month-end. [bankofengland.co.uk](https://www.bankofengland.co.uk/statistics/yield-curves){:target="_blank"}
- Brigo, D., Mercurio, F. (2001). "A Deterministic-Shift Extension of Analytically-Tractable and Time-Homogeneous Short-Rate Models." Finance and Stochastics, 5(3), 369-387. [doi.org](https://doi.org/10.1007/pl00013541){:target="_blank"}
- Campbell, J.Y., Shiller, R.J. (1991). "Yield Spreads and Interest Rate Movements: A Bird's Eye View." The Review of Economic Studies, 58(3), 495-514. [doi.org](https://doi.org/10.2307/2298008){:target="_blank"}
- Deutsche Bundesbank. Term structure of interest rates on listed Federal securities. [bundesbank.de](https://www.bundesbank.de/en/statistics/money-and-capital-markets/interest-rates-and-yields/term-structure-of-interest-rates){:target="_blank"}
- EIOPA (2026). Technical documentation of the methodology to derive EIOPA's risk-free interest rate term structures, applicable from 30 January 2027. [eiopa.europa.eu](https://www.eiopa.europa.eu/eiopa-publishes-rfr-technical-documentation-become-applicable-30-january-2027-2026-05-26_en){:target="_blank"}
- European Central Bank. Euro short-term rate (€STR). [ecb.europa.eu](https://www.ecb.europa.eu/stats/financial_markets_and_interest_rates/euro_short-term_rate/html/index.en.html){:target="_blank"}
- Gürkaynak, R.S., Sack, B., Wright, J.H. (2007). "The U.S. Treasury Yield Curve: 1961 to the Present." Journal of Monetary Economics, 54(8), 2291-2304. [doi.org](https://doi.org/10.1016/j.jmoneco.2007.06.029){:target="_blank"}
- Jotikasthira, C., Le, A., Lundblad, C. (2015). "Why Do Term Structures in Different Currencies Co-move?" Journal of Financial Economics, 115(1), 58-83. [doi.org](https://doi.org/10.1016/j.jfineco.2014.09.004){:target="_blank"}
- Malik, S., Meldrum, A. (2016). "Evaluating the Robustness of UK Term Structure Decompositions Using Linear Regression Methods." Journal of Banking & Finance, 67, 85-102. [doi.org](https://doi.org/10.1016/j.jbankfin.2016.02.006){:target="_blank"}
- U.S. Department of the Treasury. Daily Treasury Bill Rates: bank discount rate and coupon equivalent. [home.treasury.gov](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_bill_rates&field_tdr_date_value=202610){:target="_blank"}
- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. [doi.org](https://doi.org/10.1016/0304-405x(77)90016-2){:target="_blank"}
- Wright, J.H. (2011). "Term Premia and Inflation Uncertainty: Empirical Evidence from an International Panel Dataset." American Economic Review, 101(4), 1514-1534. [doi.org](https://doi.org/10.1257/aer.101.4.1514){:target="_blank"}

</details>

{% include ft-charts-script.html %}
