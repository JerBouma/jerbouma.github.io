## How It Works

This page explains the theory behind both, then derives every number they use: what it is, whether it comes from a published source, from a fit on data or from a judgement, and the chart that shows it. The other rate models (Hull-White, CIR, Wilkie, Hibbert, Nelson-Siegel curves, HJM) are summarised after that, followed by the two models of rates and inflation together: KNW, fitted on history, and DNB's CP2022, with DNB's own parameters. Argument lists are in the reference pages for [InterestRates](#interestrates) and the [configuration classes](/projects/financescenarios/docs/configuration#configuration-classes).

The numbers below come from one calibration of the default settings and factor set, made on 19 October 2026, the same one the README and the Getting Started section above use.

### The Short Rate Follows a Policy Rule

A short rate that reverts to one fixed level ignores why rates move: central banks raise them when inflation runs above target and cut them when unemployment rises. A rule makes that link explicit, so a scenario with an inflation surge also has rising rates, and a recession has falling ones.

<div class="fs-facts">
  <div><span>Series</span><b>The 3-month rate of each currency</b></div>
  <div><span>Reads</span><b>The scenario's inflation and unemployment</b></div>
  <div><span>Default model</span><b>The Fed's inertial rule, from the market's path, with a floor</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/interest-rates">InterestRates</a></div>
</div>

#### The Rule

[Taylor (1993, p. 202, eq. 1)](https://doi.org/10.1016/0167-2231(93)90009-L){:target="_blank"} showed that a simple rule tracked the federal funds rate from 1987 to 1992: the neutral real rate plus inflation, plus half of inflation's gap to target, plus half of the output gap. The balanced-approach rule the Federal Reserve also reports gives the output gap twice that weight, a full point ([Board of Governors of the Federal Reserve System, 2018, table "Examples of Policy Rules"](https://www.federalreserve.gov/monetarypolicy/policy-rules-and-how-policymakers-use-them.htm){:target="_blank"}). The [Monetary Policy Report (2026, Box 4, Table A)](https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-part2.htm){:target="_blank"} writes both rules with the unemployment gap in place of the output gap, through Okun's law (note 3 of the box): a weight of 1 for Taylor's rule and 2 for the balanced approach. The balanced-approach rule is the one each scenario follows:

$$
R^*_t = r^* + \pi_t + 0.5\,(\pi_t - \pi^*) - 2.0\,(u_t - u^*)
$$

Here $$\pi_t$$ is the scenario's inflation over the past year, $$\pi^*$$ the 2% target, $$u_t$$ its unemployment rate, $$u^*$$ the longer-run unemployment rate and $$r^*$$ the neutral real rate. With inflation 3 points above target, the rule asks for 4.5 points more; with unemployment 1 point above its longer-run rate, for 2 points less.

#### Gradual Adjustment

Central banks move in steps, not to the rule's rate at once. The Federal Reserve's inertial rule keeps 85% of last quarter's rate and moves 15% of the way to the balanced-approach rule, $$R_t = 0.85\,R_{t-1} + 0.15\,R^*_t$$ (the same table of the [Board of Governors, 2018](https://www.federalreserve.gov/monetarypolicy/policy-rules-and-how-policymakers-use-them.htm){:target="_blank"}). That published rule is the default as it stands. Written as a continuous process, the rate closes its gap to the rule at speed $$\kappa = -\ln(0.85)/0.25 = 0.65$$ a year, so a gap halves in about 1.1 years:

$$
s_{t+\Delta t} = R^*_t + (s_t - R^*_t)\,e^{-\kappa \Delta t} + \sigma \sqrt{\frac{1 - e^{-2\kappa\Delta t}}{2\kappa}}\;\varepsilon_t
$$

The shock $$\varepsilon_t$$ is the rate's own surprise, correlated with every other factor, and $$\sigma$$ its size. The rule reads inflation and unemployment as they stand at the start of each step, as a central bank sets its rate on the latest data.

#### The Floor and the Shadow Rate

A central bank cannot cut much below its lowest rate. The model keeps an unconstrained shadow rate $$s_t$$ that follows the rule, and the observed rate is $$r_t = \max(s_t, \text{ELB})$$, the shadow-rate idea of [Black (1995, section I, p. 1372)](https://doi.org/10.1111/j.1540-6261.1995.tb05182.x){:target="_blank"}. In a deep recession the shadow rate falls well below the floor, so the rate stays there until the rule climbs back above it, as the federal funds rate did from 2008 to 2015.

The chart below runs the rule on each currency's own history since 2000, with the calibrated numbers: the grey line is the rule's prescription, the orange line that prescription reached gradually at 0.65 a year, the blue line the 3-month rate. The reached rule stayed 1.4, 2.2 and 2.4 points from the US, German and UK rate on average (root mean square), against 2.9, 3.0 and 3.7 for the prescription itself. The largest misses are the euro area and the United Kingdom before 2008, when the rule called for lower rates than the ECB and the Bank of England set; the United Kingdom from 2017 to 2019, when it called for 3% to 4% while Bank Rate stayed below 1%; and 2021-2023, when the rule called for far higher rates than any of the three central banks set.

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/taylor-rule" alt="The balanced-approach rule's prescription, the rule reached at the inertial speed and the 3-month rate for the US, the euro area and the UK since 2000" %}

#### How Each Number Is Set

Each number in the rule, where it comes from and why it has this value:

| Number | Value | Kind | Why this value |
|:--|:--|:--|:--|
| Inflation-gap weight | 0.5 | Sourced | [Taylor (1993, p. 202, eq. 1)](https://doi.org/10.1016/0167-2231(93)90009-L){:target="_blank"}; [Federal Reserve (2026, Box 4, Table A)](https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-part2.htm){:target="_blank"} |
| Unemployment-gap weight | 2.0 | Sourced | The balanced-approach rule inside the Federal Reserve's inertial rule, [Board of Governors (2018)](https://www.federalreserve.gov/monetarypolicy/policy-rules-and-how-policymakers-use-them.htm){:target="_blank"}, written with the unemployment gap through Okun's law, [Federal Reserve (2026, Box 4, Table A and note 3)](https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-part2.htm){:target="_blank"}. Taylor's 1.0 is an option. |
| Adjustment speed | 0.65 a year | Sourced | The inertial rule's 0.85 of last quarter's rate, [Board of Governors (2018)](https://www.federalreserve.gov/monetarypolicy/policy-rules-and-how-policymakers-use-them.htm){:target="_blank"}. A speed fitted on the US bill rate is unstable: from 1987 to 2012 the slope even turns negative. |
| Inflation target | 2% (USD, EUR, GBP) | Sourced | [FOMC (2026, Statement on Longer-Run Goals, paragraph 4)](https://www.federalreserve.gov/monetarypolicy/files/fomc_longerrungoals.pdf){:target="_blank"}; [ECB (2021, strategy statement, paragraph 5)](https://www.ecb.europa.eu/home/search/review/html/ecb.strategyreview_monpol_strategy_statement.en.html){:target="_blank"}; [HM Treasury (2025, remit letter, paragraph 4)](https://www.gov.uk/government/publications/monetary-policy-remit-budget-2025/letter-from-chancellor-of-the-exchequer-to-govenor-of-the-bank-of-england){:target="_blank"}. The Federal Reserve's 2% refers to PCE prices, which have tended to run a little below the CPI the model reads. |
| Neutral real rate, USD | 1.2% | Sourced | The FOMC's longer-run federal funds rate of 3.2% less its 2% longer-run inflation, [Summary of Economic Projections (16 September 2026, Table 1)](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm){:target="_blank"} |
| Neutral real rate, EUR | 0.09% | Sourced | The Holston-Laubach-Williams estimate for the euro area in 2026Q2, [Federal Reserve Bank of New York (2026, HLW estimates)](https://www.newyorkfed.org/research/policy/rstar){:target="_blank"} |
| Neutral real rate, GBP | 1.0% | Judgement | The midpoint of the Bank of England's range: 2-3% nominal in 2018 plus 25-75 basis points since, less 2% inflation, [Bank of England (2025, Monetary Policy Report February 2025, Box A)](https://www.bankofengland.co.uk/monetary-policy-report/2025/february-2025){:target="_blank"}. The Bank publishes a range, not a point. |
| Longer-run unemployment $$u^*$$ | US 4.2%, euro 7.16%, UK 4.21% | Sourced | The FOMC's median, [Summary of Economic Projections (16 September 2026, Table 1)](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm){:target="_blank"}; the European Commission's NAWRU for 2027 for France (the euro area's rule reads French unemployment) and the UK, [AMECO ZNAWRU, Spring 2026 forecast](https://ec.europa.eu/economy_finance/ameco/wq/series?fullVariable=1.0.0.0.ZNAWRU&countries=FRA,GBR,DEU&years=2027&lastYear=0&yearOrder=ASC){:target="_blank"} |
| Floor, USD | 0% | Sourced | The federal funds target range of 0 to 0.25%, 16 December 2008 to 2015 and 16 March 2020 to 2022, [Federal Reserve (open market operations)](https://www.federalreserve.gov/monetarypolicy/openmarket.htm){:target="_blank"} |
| Floor, EUR | -0.50% | Sourced | The ECB's deposit facility rate from 18 September 2019 to 27 July 2022, its lowest, [ECB (key interest rates)](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/html/index.en.html){:target="_blank"} |
| Floor, GBP | 0.10% | Sourced | Bank Rate from 19 March 2020 to 16 December 2021, its lowest, [Bank of England (Bank Rate history)](https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp){:target="_blank"} |
| At the floor | Within 25 basis points | Judgement | Months that start within 25 basis points of the floor (or of zero, if the floor is below it) while the rule prescribed less are left out of the volatility fit: the rate could not follow the rule there. The Federal Reserve's range was 0-0.25%, and a euro rate held at 0% in 2012-2014 was at the floor of the time. |
| Volatility | USD 0.89%, EUR 0.81%, GBP 0.82% a year | Fitted | The standard deviation of each month's change less the part the rule explains, scaled to a yearly Ornstein-Uhlenbeck volatility, on each 3-month rate since 2000. 99 US, 96 euro and 7 UK months held at the floor are left out (shaded in the chart above). |

The neutral real rates come from different kinds of source, and the chart shows both. For the dollar, the FOMC's own longer-run projection: the median has risen from 2.5% in 2019-2023 to 3.2% today. For the euro, the one-sided estimate of the Holston-Laubach-Williams model, which fell from about 2% before 2008 to near zero. For the pound, no official point estimate exists, so the midpoint of the Bank of England's range is a judgement.

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/neutral-rates" alt="The FOMC's longer-run federal funds rate and the neutral real rate it implies since 2012; the euro-area Holston-Laubach-Williams estimate and the UK's 1.0% since 2000" %}

Each floor is the lowest policy rate its central bank has set, and the 3-month rates the model reads sat at or near those floors for years:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/lower-bounds" alt="The US, German and UK 3-month rates since 2000 with each central bank's lowest policy rate" %}

The rule measures slack from the official longer-run unemployment rate, as the published rules do. Only an entry without an official rate falls back to its unemployment's calm level, the floor recessions push unemployment up from (see [the economy page](/projects/financescenarios/docs/economy#euro-area-unemployment)). On the market's path below, that level cancels out of the rule's target anyway.

With inflation at target and unemployment at $$u^*$$, the rule settles at $$r^* + \pi^*$$:

<div class="ca-nums fs-nums">
  <span><b>3.2%</b>dollar</span>
  <span><b>2.09%</b>euro</span>
  <span><b>3.0%</b>pound</span>
</div>

These are the values a run reads today. A calibration as of a past date, which is what every backtest on the validation page is, reads each of them as it had been published by that date: the neutral real rate from the New York Fed's real-time estimates ([Federal Reserve Bank of New York, r-star](https://www.newyorkfed.org/research/policy/rstar){:target="_blank"}), for the dollar until the FOMC first projected the longer-run federal funds rate in January 2012 and for the pound until the Bank of England published its range in 2018, the longer-run unemployment rate and the NAWRU from the projections and AMECO releases of the time, and the target and the floor then in force. A rule fitted at the end of 2007 reads a US neutral real rate of 2.14%, the Laubach-Williams estimate published on 20 December 2007, where a run today reads 1.2%. The [dated values](/projects/financescenarios/docs/validation#dated-values) section of the validation page shows each of these histories with its sources.

### The Rule Starts from the Market's Expected Path

A rule on its own starts every scenario on the rule's own expected path, wherever today's rate is: with US inflation a little above target, the path climbs or falls toward 3.2% within a year or two, whatever the bond market prices. The yield curve already says where investors expect the short rate to go, so the default reads that expectation off the curve and lets the rule act only on what the market could not know: each scenario's own inflation and unemployment surprises.

#### Forward Rates Less the Term Premium

A forward rate is what the curve lets you lock in today for borrowing in a future year, so it is the short rate expected for that year plus a premium for bearing interest-rate risk until then. [Adrian, Crump and Moench (2013, section 2.4)](https://doi.org/10.1016/j.jfineco.2013.04.009){:target="_blank"} split each yield into the average short rate expected over the bond's life and that term premium. Taking the premium's forward part out of each year's forward rate leaves the expected path:

$$
m\!\left(n - \tfrac{1}{2}\right) = \underbrace{n\,z(n) - (n-1)\,z(n-1)}_{\text{forward rate for year } n} - \underbrace{\big(n\,\text{TP}(n) - (n-1)\,\text{TP}(n-1)\big)}_{\text{its premium}}, \qquad m(0) = r_0
$$

with $$z(n)$$ the continuously compounded zero rate and $$\text{TP}(n)$$ the term premium of an $$n$$-year yield. Without the premium, the forward rates themselves would be read as expected short rates, and a long rate built on them would carry the premium twice. The curves are the New York Fed's own fit of the Treasury zero curve for the dollar (the yields its premium is estimated on), the Deutsche Bundesbank's zero curve of Federal securities for the euro ([Deutsche Bundesbank, term structure of interest rates](https://www.bundesbank.de/en/statistics/money-and-capital-markets/interest-rates-and-yields/term-structure-of-interest-rates){:target="_blank"}) and the Bank of England's gilt spot curve for the pound ([Bank of England, yield curves](https://www.bankofengland.co.uk/statistics/yield-curves){:target="_blank"}), each on the calibration day. The dollar's path past today is quoted as the 13-week bill's bank discount rate, the basis ^IRX quotes ([US Treasury, Daily Treasury Bill Rates](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_bill_rates&field_tdr_date_value=202610){:target="_blank"}), so it starts on the basis of today's rate.

#### Each Currency's Own Term Premium

The New York Fed publishes the dollar's premium. For the euro and the pound no official estimate exists, so each gets its own, from the same method run on its own curve, as [Malik and Meldrum (2016, section 3)](https://doi.org/10.1016/j.jbankfin.2016.02.006){:target="_blank"} run it on gilts. The regressions of [Adrian, Crump and Moench (2013, sections 2.3-3.1)](https://doi.org/10.1016/j.jfineco.2013.04.009){:target="_blank"} take three steps:

1. Five principal components of the 3- to 120-month yields are the curve's pricing factors, and a vector autoregression moves them from month to month.
2. The monthly excess returns of twelve zero-coupon bonds (6, 12, ..., 60, 84 and 120 months) over the short rate are regressed on the factors' innovations and their lagged values.
3. A cross-sectional regression of those coefficients gives the prices of risk, and the term premium of each maturity is its yield less the yield the model gives with the prices of risk set to zero.

The curves are the Bundesbank's month-end curve from September 1972 and the Bank of England's from January 1970, both keyless. The short rate is each country's OECD 3-month rate, the rate the euro and pound short rates simulate; below a curve's first maturity, yields are filled linearly from it, as Malik and Meldrum (2016, note 2) fill the gilt curve from Bank Rate. The sample stops at the calibration date, so a backtest never sees a later month. When the fit cannot be made (fewer than 120 months, no readable short rate, or fitted yields more than 50 basis points off the curve on average), the Treasury premium stands in: term premia move together across countries ([Wright, 2011](https://doi.org/10.1257/aer.101.4.1514){:target="_blank"}; [Jotikasthira, Le and Lundblad, 2015](https://doi.org/10.1016/j.jfineco.2014.09.004){:target="_blank"}).

The code is checked against a known answer: run on the Treasury curve of [Gürkaynak, Sack and Wright (2007)](https://doi.org/10.1016/j.jmoneco.2007.06.029){:target="_blank"} with the 3-month bill as the short rate, it reproduces the New York Fed's ACMTP10 over 1961-2026 to -0.2 basis points on average (4.1 basis points mean absolute error, 16 at most), and on a synthetic one-factor affine curve it recovers the true 10-year premium within 1 basis point.

| | Euro (Bundesbank curve) | Pound (Bank of England curve) |
|:--|--:|--:|
| Months fitted | 649 (September 1972 to September 2026) | 482 (January 1986 to February 2026) |
| Yields fitted within (RMSE) | 5.2 basis points | 5.7 basis points |
| 10-year premium, mean (standard deviation) | 1.22% (1.07) | 1.13% (1.20) |
| 10-year premium, last month-end | 0.37% | 0.90% |
| Correlation with the US ACMTP10 | 0.58 | 0.89 |

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/own-term-premia" alt="The euro and pound 10-year term premia from their own government curves against the New York Fed's ACMTP10, month-ends since 1972" %}

The premia rose with the inflation of the 1970s and 1980s and fell toward zero in the 2010s, as the dollar's did; the pound's follows the dollar's more closely than the euro's. The simulated euro and pound rates are interbank rates, which sit above the government 3-month zero rate (Germany by about 9 basis points before 1999 and 30 since, the UK by 33), and that spread sits in the estimated premium, as the bill-to-curve gap sits in the New York Fed's.

#### When the OECD Print Is Stale

The OECD's 3-month rate comes out with a lag, and for the pound it stopped at February 2026. Starting a run on 19 October 2026 from that print would start the pound at 3.62%, while the 6-month gilt zero rate had since gone from 3.45% to 4.18%. When a euro or pound print is more than a full month old, the run starts from it carried forward with a fresher rate of the same currency, keeping its level:

$$
r_0 = r^{\text{OECD}}_{\text{last}} + \big(x_{\text{last full month}} - x_{\text{OECD's last month}}\big)
$$

where $$x$$ is the 3-month point between the overnight benchmark and the shortest maturity of the month-end government curve, interpolated linearly in maturity. For the pound that is SONIA's monthly average ([Bank of England, SONIA](https://www.bankofengland.co.uk/markets/sonia-benchmark){:target="_blank"}) and the 6-month zero of the gilt curve, so the point sits halfway; for the euro the euro short-term rate's monthly average ([ECB, euro short-term rate](https://www.ecb.europa.eu/stats/financial_markets_and_interest_rates/euro_short-term_rate/html/index.en.html){:target="_blank"}) and the 1-year zero of the Bundesbank curve, so it sits a quarter of the way. The weights follow from the maturities and are not fitted. The overnight rate alone misses the policy changes a 3-month rate already prices, and the curve's shortest point alone overstates its moves (it would put the pound at 4.35%, well above Bank Rate at 3.75%). Carried six months forward from every past month, the 3-month point lands 16 basis points from the rate the OECD later printed for the UK since 2015 (the stale print: 67) and 12 for Germany since November 2019 (stale: 84).

On the calibration day the pound starts at 3.99%: February's 3.62% carried to September with the 0.37-point rise of the 3-month point. Germany's OECD series runs to September, so the euro start is the print itself, and the dollar starts from the daily ^IRX. Only the start moves, with what reads it (the market path's first point and the short end of today's curve in the pound's own premium); the policy rule, the correlations and the term premia are still fitted on the rates as the OECD printed them.

#### Past the Curve

The curve is read for ten years, the longest maturity the premium is estimated for. After that the path closes its gap to the rule's steady state at the short rate's own speed of mean reversion $$a$$, the speed the 10-year rate reads it with below, so the path and the long rate describe one expected path ([Vasicek, 1977, section 5, eq. 25](https://doi.org/10.1016/0304-405x(77)90016-2){:target="_blank"}; [Campbell and Shiller, 1991](https://doi.org/10.2307/2298008){:target="_blank"}):

$$
m(H + s) = m_{ss} + \big(m(H) - m_{ss}\big)\,e^{-a s}, \qquad H = 10 \text{ years}, \quad m_{ss} = r^* + \pi^*
$$

This speed replaces the convergence speed of EIOPA's risk-free curves ([EIOPA, RFR technical documentation, 2026](https://www.eiopa.europa.eu/eiopa-publishes-rfr-technical-documentation-become-applicable-30-january-2027-2026-05-26_en){:target="_blank"}), which belongs to EIOPA's method for extrapolating a curve, not to how the short rate is expected to move. With $$a$$ at 0.057 (dollar), 0.133 (euro) and 0.043 (pound) a year, a gap at ten years halves in 12, 5 and 16 years.

On the calibration day the dollar path rises from today's 4.08% to 4.43% in the second year and is back at 4.07% in the tenth; the euro's peaks at 3.43% and the pound's, from its carried-forward 3.99%, at 5.17%. Past the curve each heads for its steady state, which the pound and the dollar, with the slowest speeds, are still well above after thirty years (the dollar at 3.48%).

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/market-path" alt="The expected short rate for the dollar, the euro and the pound: forward rates less the term premium for ten years, then converging to the rule's steady state" %}

#### The Rule Acts on the Surprises

Each scenario's rate follows the market path $$m(t)$$, and the rule acts on the gap between that scenario's inflation and unemployment and their expected paths $$\bar\pi(t)$$ and $$\bar u(t)$$:

$$
R^*_t = m(t) + R^{\text{rule}}(\pi_t, u_t) - R^{\text{rule}}(\bar\pi_t, \bar u_t)
$$

This is the deterministic shift of [Brigo and Mercurio (2001)](https://doi.org/10.1007/pl00013541){:target="_blank"}: the model starts from any expected path while its dynamics stay its own. The rule's weights, speed, volatility and floor are unchanged, but what the market already priced in is not counted again. A scenario whose inflation and unemployment stay on their expected paths follows the market's path, and a regime that lifts inflation by a point in every scenario lifts the rate's target by 1.5 points, as the rule's own path would. The expected paths are the calibrated model's median inflation and unemployment without regimes, beliefs or shocks, worked out once at calibration from 4,000 scenarios and stored with it; the median, because inflation's rare high spells lift its average above where most scenarios are. The level $$u^*$$ the rule measures slack from appears in both terms, so it cancels.

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">The starting premium's quoting basis</p>

On 15 October 2026 the US 10-year term premium at the start of a run, the 10-year yield less the expected path, sat 11 basis points above the New York Fed's ACMTP10. About 2.4 basis points of that is ^TNX quoting a par yield where the path is read off zero rates, and about 8.5 the 13-week bill's bank discount quote. Converting ^TNX alone would leave the term premium fitted on unconverted OECD history, an inconsistency of the same size, so both legs and that history would have to be converted together; for now the gap stays.
</div>

### The Long Rate Is the Expected Short-Rate Path plus a Term Premium

Two rates that each revert on their own, linked only by correlated shocks, let the gap between them wander: a simulated curve can invert at random and stay inverted for decades. Building the long rate on the short rate ties the curve together. The curve then inverts when the short rate jumps and steepens again as it falls back, as it has done historically.

<div class="fs-facts">
  <div><span>Series</span><b>The 10-year rate of each currency</b></div>
  <div><span>Fitted on</span><b>OECD 10-year and 3-month rates, yearly 1950-2025</b></div>
  <div><span>Default model</span><b>Expected short-rate path plus a term premium</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/interest-rates">InterestRates</a></div>
</div>

#### The Expected Path

Under the expectations hypothesis, a long yield is the short rate expected over the bond's life, plus a term premium for holding the longer bond ([Campbell and Shiller, 1991, section 2, eq. 1](https://doi.org/10.2307/2298008){:target="_blank"}). If the short rate's gap to its long-run level $$\theta$$ fades at speed $$a$$, the average expected short rate over $$m$$ years is a weighted mix of today's rate and that level, the same weight as in the yield of [Vasicek (1977, section 5, eq. 25)](https://doi.org/10.1016/0304-405x(77)90016-2){:target="_blank"}:

$$
\text{EP}_t = D\,r_t + (1 - D)\,\theta, \qquad D = \frac{1 - e^{-a m}}{a m}
$$

$$D$$ is the share of a short-rate move a 10-year yield carries. In the fit, $$\theta$$ is the rule's steady state ($$r^* + \pi^*$$); in a run on the market's path, the expected path averages that path over the bond's life and adds the share of today's gap to it still expected, $$\text{EP}_t = \bar m_t + D\,(r_t - m_t)$$.

<div class="fs-callout" markdown="1">
<p class="fs-callout__title">Two different speeds</p>

The speed $$a$$ in $$D$$ is the short rate's own persistence, not the rule's 0.65. The rule's speed is how fast the rate closes its gap to a target that inflation and unemployment keep moving; how long a gap in the short rate itself lasts, which is what bond markets price, depends on how persistent those drivers are.
</div>

The speed is fitted as a mean-reverting (Hull-White) process on each country's OECD 3-month rate, yearly from 1950 to 2025. A least-squares speed is biased upward in a sample of any realistic length, by about 4/T a year for T years of data ([Tang and Chen, 2009, Theorem 3.1.1](https://doi.org/10.1016/j.jeconom.2008.11.001){:target="_blank"}), so that bias is taken off: the plain fits of 0.114 a year for the US, 0.192 for Germany and 0.099 for the UK become 0.057, 0.133 and 0.043. A 10-year yield then carries 0.76, 0.55 and 0.81 of a short-rate move, against 0.60, 0.44 and 0.63 at the plain speeds. The rule's 0.65 would give 0.15.

An outside check: the New York Fed's expected average short rate over ten years, the risk-neutral yield of [Adrian, Crump and Moench (2013, section 2.4)](https://doi.org/10.1016/j.jfineco.2013.04.009){:target="_blank"} (series ACMRNY10, [Federal Reserve Bank of New York, Treasury Term Premia](https://www.newyorkfed.org/research/data_indicators/term-premia-tabs){:target="_blank"}), moves 0.59 for every point the 3-month bill moves, monthly from June 1961 to September 2026. The plain US weight of 0.60 is close to it; the corrected 0.76 is higher, so in the model a short-rate move lasts longer in the 10-year yield than in the New York Fed's estimate, and the same-step response below takes part of it back.

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/expected-path-weight" alt="The weight of today's short rate in the 10-year expected path against the short rate's speed, with each country's fitted speed before and after the bias correction and the New York Fed's estimate" %}

#### The Term Premium

What is left of the long rate after the expected path is the term premium, $$\text{TP}_t = L_t - \text{EP}_t$$. It reverts toward a long-run level, moves with the short rate's gap to its own level, and responds to the short rate's change in the same step:

$$
\text{TP}_{t+1} = c + \phi\,\text{TP}_t + \psi\,(r_t - \theta) + \gamma\,(r_{t+1} - r_t) + e_{t+1}
$$

One least-squares regression on each country's OECD 10-year and 3-month rates, yearly from 1950 to 2025, gives every parameter: the speed $$\kappa = -\ln\phi$$, the long-run premium $$\tau = c/(1-\phi)$$ (the premium when the short rate sits at its level), the sensitivity $$\beta = \psi/(1-\phi)$$, the same-step response $$\gamma$$ and the volatility $$\sigma$$ of the residual, scaled to a yearly Ornstein-Uhlenbeck volatility. This yearly premium is the one the 10-year rate simulates; the month-end premia of the market path above are what is taken out of today's curve.

| Parameter | United States | Germany (euro) | United Kingdom | Kind |
|:--|--:|--:|--:|:--|
| Expected-path speed $$a$$, per year | 0.057 | 0.133 | 0.043 | Fitted, OECD 3-month rate 1950-2025, less Tang and Chen's bias |
| Weight $$D$$ (10 years) | 0.76 | 0.55 | 0.81 | Derived from $$a$$ |
| Long-run premium $$\tau$$ | 1.34% | 0.94% | 1.03% | Fitted |
| Sensitivity to the short rate's gap $$\beta$$ | 0.25 | 0.48 | 0.09 | Fitted |
| Same-step response $$\gamma$$ | -0.27 | -0.19 | -0.43 | Fitted |
| Premium's speed $$\kappa$$, per year | 0.36 | 0.22 | 0.18 | Fitted |
| Premium's volatility $$\sigma$$ | 0.60% | 0.63% | 0.80% | Fitted |
| Years in the fit | 76 | 76 | 76 | |

The chart splits each country's 10-year yield into the expected path and the premium. The premium was largest from the mid-1970s to the early 1990s, when holding a long bond meant carrying inflation risk, and near or below zero around 2020; Germany's was also large in the 1950s and 1960s. Each premium averages more than its $$\tau$$ (1.52%, 2.09% and 1.26%) because the short rate averaged above the rule's steady state over these years, and $$\beta$$ adds to the premium when it does.

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/long-rate-decomposition" alt="OECD 10-year and 3-month rates since 1950 with the expected-path component and the term premium for the US, Germany and the UK" %}

The US premium can be set against the New York Fed's, which comes from a five-factor no-arbitrage model of the whole Treasury curve rather than from two rates. Over 1962-2025 the two correlate 0.92 in yearly averages. Ours averages 1.66% against ACM's 1.45%; the fitted long-run premium $$\tau$$ is 1.34%. The same-step response is larger than ACM's: their premium falls 0.12 for every point the 3-month bill rises, in yearly-average changes from 1962 to 2025, against our $$\gamma$$ of -0.27 for the US, which offsets most of the larger weight $$D$$: a short-rate jump still lifts the 10-year by $$D + \gamma = 0.49$$ at once.

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/term-premium-acm" alt="The fitted US 10-year term premium against the New York Fed's ACM term premium, yearly 1962-2025" %}

#### In the Simulation

Each month the premium moves toward its target $$\tau + \beta\,(r_t - \theta)$$ at speed $$\kappa$$, takes $$\gamma$$ of the short rate's change and a shock of its own; the long rate is the expected path plus the premium:

$$
\text{TP}_{t+\Delta t} = \text{TP}^*_t + (\text{TP}_t - \text{TP}^*_t)\,e^{-\kappa\Delta t} + \gamma\,(r_{t+\Delta t} - r_t) + \sigma\sqrt{\tfrac{1 - e^{-2\kappa\Delta t}}{2\kappa}}\;z_t, \qquad L_{t+\Delta t} = \text{EP}_{t+\Delta t} + \text{TP}_{t+\Delta t}
$$

A 1-point jump in the short rate therefore lifts the 10-year at once by $$D + \gamma$$, and then by more or less as the premium follows the short rate's gap and the gap fades at the rule's speed. With every shock set to zero, the US 10-year rises:

<div class="ca-nums fs-nums">
  <span><b>0.49 pp</b>in the first month</span>
  <span><b>0.38 pp</b>after a year</span>
  <span><b>0.21 pp</b>after three years</span>
</div>

The same response for the US, Germany and the UK:

{% include theme-image.html src="/assets/images/projects/financescenarios/docs/interest-rates/shock-response" alt="The response of the 10-year yield to a 1-point jump in the short rate for the US, Germany and the UK" %}

### Data Choices

Which data each rate is fitted on, and why:

| Choice | Kind | Why |
|:--|:--|:--|
| The US short rate is the 13-week Treasury bill (^IRX), monthly | Judgement | A market rate the policy rate drives, daily and keyless; [Ahlgrim, D'Arcy and Gorvett (2005, section 3)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"} likewise use the three-month Treasury rate for the short rate |
| The euro area's rates are Germany's (OECD, monthly) | Judgement | The euro area's largest economy and its benchmark Bund |
| The euro area's rule reads German inflation (quarterly) and French unemployment | Judgement | German unemployment fell structurally after the mid-2000s labour reforms; see [the economy page](/projects/financescenarios/docs/economy#euro-area-unemployment) |
| The market path reads each government curve for ten years | Judgement | Ten years is the longest maturity the term premia are estimated for |
| The euro and pound premia come from their own month-end curves over each OECD 3-month rate | Judgement | No official premium exists for either; their own curves price their own risk, and the 3-month rate is the one each short rate simulates. The US premium stands in only when the fit cannot be made |
| The term premium and the expected-path speed are fitted on the OECD's yearly rates since 1950 | Judgement | Seventy-six years hold the high-inflation decades, the low-rate 2010s and the 2022 rise; a window since 2000 holds one rate cycle |
| The rule's volatility and every starting value come from data since 2000 | Judgement | The settings' calibration window: two full bear markets (2000-02, 2008-09) and the sector ETFs' history |

### Other Rate Models

The default is one choice among several; each of these is an option on an interest rate in the factor set or a factor of its own.

**Hull-White (Vasicek).** The rate reverts to one long-run level $$\theta$$ at speed $$a$$ with constant volatility, $$dr_t = a(\theta - r_t)\,dt + \sigma\,dW_t$$ ([Vasicek, 1977](https://doi.org/10.1016/0304-405x(77)90016-2){:target="_blank"}; [Hull and White, 1990](https://doi.org/10.1093/rfs/3.4.573){:target="_blank"}). It is the general-purpose model, supports GARCH volatility ([Bollerslev, 1986, section 3, eq. 8, p. 311](https://doi.org/10.1016/0304-4076(86)90063-1){:target="_blank"}), beliefs, a zero floor, a long history (OECD rates since 1950, UK rates since 1694) and a long-run anchor on EIOPA's forward curve ([Solvency II Directive, Article 77a](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02009L0138-20250117#art_77a){:target="_blank"}). It is also the risk-neutral short rate: with a time-dependent $$\theta$$ that reproduces today's Treasury or EIOPA curve ([Brigo and Mercurio, 2006, section 3.3](https://doi.org/10.1007/978-3-540-34604-3){:target="_blank"}), the curve a Solvency II best estimate discounts with ([Article 77(2)](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02009L0138-20250117#art_77){:target="_blank"}).

**Cox-Ingersoll-Ross.** Shocks scale with the square root of the rate, so rates stay positive when the Feller condition holds and calm down near zero ([Cox, Ingersoll and Ross, 1985, section 3, eq. 17, p. 391](https://doi.org/10.2307/1911242){:target="_blank"}).

**Wilkie consols.** The long yield as expected inflation plus a positive real part, from [Wilkie's (1986, section 3.15)](https://doi.org/10.1017/S0071368600009009){:target="_blank"} actuarial model; it needs long yields above average inflation throughout the fit.

**Hibbert two-factor.** The short rate reverts to a slower-moving rate rather than a fixed level ([Hibbert, Mowbray and Turnbull, 2001, section 5.1.1, p. 15](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf#page=15){:target="_blank"}).

**KNW.** The nominal rate and inflation as one coupled system, with optional shared stochastic volatility; see [the KNW models](#knw-models).

**CP2022.** De Nederlandsche Bank's model of the same system with DNB's quarterly parameters; see [CP2022](#cp2022-model).

**Nelson-Siegel curves.** A whole government curve as level, slope and curvature factors ([Nelson and Siegel, 1987](https://doi.org/10.1086/296409){:target="_blank"}; [Diebold and Li, 2006, section 3.2](https://doi.org/10.1016/j.jeconom.2005.03.005){:target="_blank"}), each simulated as its own mean-reverting factor, with a corporate spread curve on top; see [TermStructure](#termstructure) and [CreditTermStructure](/projects/financescenarios/docs/markets#credittermstructure).

**HJM.** An arbitrage-free forward curve whose drift follows from its volatility ([Heath, Jarrow and Morton, 1992, section 4, Proposition 3, p. 86](https://doi.org/10.2307/2951677){:target="_blank"}), with two Hull-White factors (G2++) fitted to how historical forwards moved together; see [Hjm](#hjm).

### The KNW Models: Rates and Inflation Together {#knw-models}

A pension fund with inflation-indexed benefits, discounted at nominal rates, is exposed to the joint behavior of rates and inflation more than to either one alone. The KNW models simulate the two as one system: today's inflation shapes where rates go next, and today's rate shapes where inflation goes next.

They follow the term-structure model of [Koijen, Nijman and Werker (2010)](https://doi.org/10.1093/rfs/hhp058){:target="_blank"}, which the Dutch Commissie Parameters extends in its CP2022 model ([Commissie Parameters, 2022, Technical Appendix, p. 1](https://open.overheid.nl/repository/ronl-f2685a42fd0bf01d5821446bcda34e719fdf7ef1/1/pdf/bijlage-2-technische-appendix.pdf#page=1){:target="_blank"}), the model behind the scenario sets De Nederlandsche Bank (DNB) publishes for Dutch pension funds.

Finance Scenarios implements a discrete, reduced-form approximation inspired by both: a VAR on the observed short rate and inflation, fitted by least squares, not the latent-factor model those papers filter from the yield curve. For the single-factor short-rate models and the Nelson-Siegel curve, see [other rate models](#other-rate-models).

#### Why Model Rates and Inflation Together

Correlated shocks only link the surprises of the same month. They say nothing about how today's level of inflation pushes rates over the next years, the channel that matters for long-dated, inflation-linked liabilities.

Here the two state variables are the nominal short rate and year-over-year CPI inflation, which stands in for expected inflation. Their link reflects the Fisher logic that a nominal yield is roughly a real yield, plus expected inflation, plus an inflation risk premium:

$$
y^{\text{nom}}_t(\tau) \approx y^{\text{real}}_t(\tau) + \mathbb{E}_t[\bar\pi_{t,\tau}] + \text{IRP}_t(\tau)
$$

Persistent inflation tends to lift nominal rates, and a high real rate tends to cool inflation. Coupling the two in the drift keeps rates, inflation and the implied real rate consistent along every path and gives the pair one joint long-run level. The other options in Finance Scenarios link the two in one direction only (the Wilkie cascade, or conditioning inflation on the rate change); KNW goes both ways and uses the other variable's level, not its change.

#### The Three Variants

Each variant adds one layer to the one before:

| Variant | What it adds | Use it for |
|:--|:--|:--|
| KNW (`knw`) | Two-way coupling at constant volatility | The interpretable core; a first look at the joint dynamics |
| KNW with stochastic volatility (`knw_sv`) | A shared hidden turbulence factor $$v$$ that scales volatility and shifts the drift; optional equity leg | Calm and stressed regimes that hit rates, inflation and equity at once |
| Risk-neutral KNW (`knw_sv` with `measure: risk_neutral`) | A market price of risk fitted to the Treasury curve, closed-form bond prices, a stochastic deflator | Valuation, and a model yield curve at any maturity |

Each builds on the previous one: with the turbulence terms at zero, KNW with stochastic volatility is plain KNW exactly. Parameter details are in the reference pages for [Knw](#knw), [KnwSv](#knwsv) and [KnwSvQ](#knwsvq).

<div class="fs-diagram">
<div class="fs-links">
  <div class="fs-links__row">
    <div class="fs-node is-accent"><b>Turbulence v</b><small>hidden, shared by all three</small></div>
    <div class="fs-links__to">
      <div class="fs-link"><em>drift and volatility</em><div class="fs-node"><b>Interest rate</b></div></div>
      <div class="fs-link"><em>drift and volatility</em><div class="fs-node"><b>Inflation</b></div></div>
      <div class="fs-link"><em>volatility</em><div class="fs-node"><b>Equity</b><small>optional</small></div></div>
    </div>
  </div>
  <div class="fs-links__row">
    <div class="fs-node"><b>Interest rate</b></div>
    <div class="fs-links__to">
      <div class="fs-link is-both"><em><i></i>last period's level</em><div class="fs-node"><b>Inflation</b></div></div>
      <div class="fs-link"><em>short rate plus premium</em><div class="fs-node"><b>Equity</b><small>optional</small></div></div>
    </div>
  </div>
</div>
</div>

Turbulence drives every leg and is never driven back. Plain KNW keeps only the two-way arrow between rate and inflation.

#### KNW: Two-Way Coupling

Each leg is a regression on last period's level of both variables, a bivariate VAR(1) ([Lütkepohl, 2005](https://doi.org/10.1007/978-3-540-27752-1){:target="_blank"}):

$$
\begin{pmatrix} r_t \\ \pi_t \end{pmatrix}
= c + \Phi \begin{pmatrix} r_{t-1} \\ \pi_{t-1} \end{pmatrix} + \begin{pmatrix} \sigma_r\,\varepsilon^r_t \\ \sigma_\pi\,\varepsilon^\pi_t \end{pmatrix}
$$

$$r_t$$ is the nominal short rate and $$\pi_t$$ year-over-year CPI inflation. The diagonal of $$\Phi$$ is each variable's own persistence, the off-diagonal terms the cross-coupling: how much of the other variable's level spills over. $$c$$ holds two intercepts and $$\sigma$$ the size of each period's surprise.

<div class="fs-facts">
  <div><span>Variables</span><b>Nominal short rate and year-over-year CPI inflation</b></div>
  <div><span>Model</span><b>Bivariate VAR(1)</b></div>
  <div><span>Fit</span><b>Ordinary least squares, on deviations from the averages</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/interest-rates">Knw</a></div>
</div>

There is no long-run mean per leg. The pair settles jointly at $$(I - \Phi)^{-1}c$$, and the system must be stable: if a shock would never die out (the largest eigenvalue of $$\Phi$$ is 1 or more), the fit stops with an error. Both legs are fitted by ordinary least squares on the dates both series cover, on deviations from the history's averages ([Lütkepohl, 2005](https://doi.org/10.1007/978-3-540-27752-1){:target="_blank"}, section 3.3), so the pair settles at those averages. Fitting a free intercept per leg instead lets a pair this persistent amplify where the sample happens to start and end.

On 146 quarters of the US OECD short rate and CPI growth, 1990Q1 to 2026Q2 (calibrated on 2026-10-14):

| leg | intercept | own persistence | cross coupling | volatility |
|:----|----------:|----------------:|---------------:|-----------:|
| interest rate | -0.0005 | 0.9432 | 0.0803 | 0.0043 |
| inflation | 0.0037 | 0.8890 | -0.0206 | 0.0073 |

One percentage point more inflation adds 0.080 points to next quarter's rate, in line with central banks raising rates when inflation runs high, though a reduced-form regression cannot single out that channel. A higher rate nudges inflation down only slightly. How fast, and where, the pair settles:

<div class="ca-nums fs-nums">
  <span><b>8 quarters</b>half-life of a joint shock</span>
  <span><b>3.04%</b>long-run rate</span>
  <span><b>2.72%</b>long-run inflation</span>
  <span><b>0.3%</b>long-run real short rate</span>
</div>

That real rate is below the 1.0% in the Federal Reserve's longer-run projections (a 3.0% federal funds rate against 2.0% PCE inflation in the [September 2025 Summary of Economic Projections](https://www.federalreserve.gov/monetarypolicy/files/fomcprojtabl20250917.pdf){:target="_blank"}, Table 1), because the sample includes the zero-rate years 2009-2015 and 2020-2021, and with 36 years of data the long-run levels carry a sampling error of about 0.6 percentage points.

<div class="fs-callout" markdown="1">
A belief cannot override the long-run levels, since they are a joint property of both legs; the history window the pair is fitted on is the lever.
</div>

<div class="fs-ref"><a href="#knw"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Knw</a></div>

#### Stochastic Volatility

Markets alternate between calm and stressed spells; plain KNW gives every period the same randomness. The stochastic-volatility variant adds DNB's hidden variance factor $$v_t$$, the square of the volatility ([Commissie Parameters, 2022, Technical Appendix, section 1](https://open.overheid.nl/repository/ronl-f2685a42fd0bf01d5821446bcda34e719fdf7ef1/1/pdf/bijlage-2-technische-appendix.pdf#page=1){:target="_blank"}), a CIR process ([Cox, Ingersoll and Ross, 1985](https://doi.org/10.2307/1911242){:target="_blank"}) of the kind [Heston (1993)](https://doi.org/10.1093/rfs/6.2.327){:target="_blank"} uses for variance: mean-reverting and never negative.

<div class="fs-facts">
  <div><span>Turbulence</span><b>One hidden CIR variance factor, shared by every leg</b></div>
  <div><span>Estimated from</span><b>The past year's squared surprises</b></div>
  <div><span>Simulation</span><b>Andersen's Quadratic-Exponential scheme</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/interest-rates">KnwSv</a></div>
</div>

$$
dv_t = a_v(\theta_v - v_t)\,dt + \sigma_v\sqrt{v_t}\,dW^v_t
$$

Each leg reads last period's $$v$$ twice, in its drift and in its variance:

$$
r_t = c_r + \lambda_r v_{t-1} + \phi_{rr} r_{t-1} + \phi_{r\pi}\pi_{t-1} + \sqrt{h_r + \eta_r v_{t-1}}\;\varepsilon^r_t
$$

with the same shape for inflation. $$\lambda$$ lets turbulence move the expected level, as in DNB's model, $$h$$ is the calm-state variance and $$\eta$$ how strongly variance rises with turbulence. Because one $$v$$ drives every leg, volatility in rates, inflation and equity rises and falls together: the clustering of stress across asset classes that a constant-volatility model misses.

**Estimating turbulence.** DNB recovers $$v$$ from market yields on each date. Finance Scenarios estimates it from the pair's own history: the average of plain KNW's squared surprises over the past year (four quarters, or twelve months), lagged one period, is the proxy for $$v$$. The one-year window follows [Engle's (1982)](https://doi.org/10.2307/1912773){:target="_blank"} four-quarter ARCH model of inflation variance. A CIR process is fitted to that proxy and both legs are refitted with it as an extra input; if neither leg's variance rises with $$v$$, the fit suggests plain KNW. Simulation uses [Andersen's (2008)](https://doi.org/10.21314/jcf.2008.189){:target="_blank"} Quadratic-Exponential scheme, which keeps $$v$$ non-negative with little bias; DNB's model uses Andersen's scheme too, with a martingale correction ([Commissie Parameters, 2022, Technical Appendix, section 9.1](https://open.overheid.nl/repository/ronl-f2685a42fd0bf01d5821446bcda34e719fdf7ef1/1/pdf/bijlage-2-technische-appendix.pdf#page=8){:target="_blank"}).

Turbulence is the variance of a quarter's combined rate and inflation surprise. On the same US quarterly data (calibrated on 2026-10-05):

<div class="ca-nums fs-nums">
  <span><b>1.7 years</b>half-life of turbulence</span>
  <span><b>0.3 pp</b>a quarter's surprise today</span>
  <span><b>0.8 pp</b>at the long-run level</span>
</div>

The pair starts calmer than usual. Inflation responds most: its standard deviation is 0.31% a quarter at $$v = 0$$ and 0.68% at the long-run level. The Feller condition $$2a_v\theta_v \ge \sigma_v^2$$ fails on this fit, so simulated turbulence touches zero more often than its long-run distribution suggests.

#### The Equity Leg

An equity index on the same turbulence factor becomes volatile when rates and inflation do. Following DNB's equity row, each period's log return is the simulated short rate plus a constant risk premium, with variance linked to $$v$$:

$$
\ln\frac{S_t}{S_{t-1}} = r_{t-1}\,\Delta t + \mu - \tfrac{1}{2}h_{t-1} + \sqrt{h_{t-1}}\,\varepsilon^S_t, \qquad h_{t-1} = h_S + \eta_S v_{t-1}
$$

$$\Delta t$$ is the period length in years and $$\mu$$ the premium per period, corrected for volatility drag. Over the S&P 500's quarterly history since 1990 (calibrated on 2026-10-05):

<div class="ca-nums fs-nums">
  <span><b>1.59%</b>a quarter above the short rate, about 6.4% a year</span>
  <span><b>13%</b>yearly volatility with no turbulence</span>
  <span><b>15.3%</b>at the long-run level</span>
</div>

The equity leg runs under the real-world measure only.

<div class="fs-ref"><a href="#knwsv"><i class="fas fa-book" aria-hidden="true"></i>Full reference: KnwSv</a></div>

#### The Risk-Neutral Version

A real-world run answers "where might rates go?"; valuing liabilities asks "what is a future cash flow worth today?". The bridge is the market price of risk, the extra return investors demand per unit of each risk. The risk-neutral version fits it so that the model's yields match the 13-week, 5, 10 and 30-year US Treasury yields over the historical sample. It changes only the drift, through five premiums: one on turbulence's mean-reversion speed, and a constant and a turbulence-proportional premium per leg. Premiums that depend on a constant and on $$v$$ only are the completely affine form of [Duffie and Kan (1996)](https://doi.org/10.1111/j.1467-9965.1996.tb00123.x){:target="_blank"}. DNB uses the richer essentially affine form of [Duffee (2002)](https://doi.org/10.1111/1540-6261.00426){:target="_blank"}, whose time-varying bond risk premia are what KNW (2010) is about ([Koijen, Nijman and Werker, 2010](https://doi.org/10.1093/rfs/hhp058){:target="_blank"}); its extra parameters are hard to pin down on a short quarterly sample and a nominal curve alone.

<div class="fs-facts">
  <div><span>Fitted to</span><b>13-week, 5, 10 and 30-year US Treasury yields</b></div>
  <div><span>Market price of risk</span><b>Five premiums, completely affine</b></div>
  <div><span>Bond prices</span><b>Closed form, at any whole number of periods</b></div>
  <div><span>Reference</span><a href="/projects/financescenarios/docs/interest-rates">KnwSvQ</a></div>
</div>

Zero-coupon prices follow from an affine recursion, for a bond $$n$$ periods out:

$$
P_t(n) = \exp\!\big(A_n + B^v_n v_t + B^r_n r_t + B^\pi_n \pi_t\big)
$$

That gives a model yield at any whole number of periods, including maturities the Treasury data does not quote. A monthly or quarterly pair works; a yearly one does not, since the 13-week yield is not a whole number of years.

```python
from financetoolkit import Toolkit

from financescenarios.models.knw_sv.knw_sv_controller import KnwSv
from financescenarios.models.knw_sv_q.knw_sv_q_controller import KnwSvQ

toolkit = Toolkit(
    ["^IRX", "^FVX", "^TNX", "^TYX"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1990-01-01"
)
knw_sv = KnwSv(toolkit)
knw_sv.calibrate_triple("interest_rate", "inflation", period="quarterly")  # real-world fit

knw_sv_q = KnwSvQ(toolkit)
knw_sv_q.calibrate_mpr(knw_sv, "interest_rate", "inflation", period="quarterly")  # market price of risk

for tenor in [0.25, 1, 5, 10, 30]:
    print(tenor, knw_sv_q.zero_coupon_yield("interest_rate", tenor))
```

In one fit (calibrated on 2026-10-14) the curve started at the 3.75% short rate, rose to about 4.5% at five years and flattened near 4.8% beyond ten, below the latest Treasury yields, since the premiums are fitted across the whole history.

<div class="fs-callout fs-callout--limits" markdown="1">
<p class="fs-callout__title">Limits</p>

- The closed-form prices and the market price of risk include the correlation between rate and inflation shocks, estimated from the same changes as the run's correlation matrix, so model bond prices and simulated discount factors agree. Turbulence's own shock is independent of both.
- The inflation risk premium is weakly identified: the price of unexpected inflation risk cannot be identified from nominal yields alone ([Koijen, Nijman and Werker, 2010](https://doi.org/10.1093/rfs/hhp058){:target="_blank"}), so without a real (TIPS) curve or inflation swaps nothing separates real rates from the inflation premium. Judge the fit by how well it reprices nominal yields, not by the individual premiums.
</div>

##### The Stochastic Deflator

A deflator values a liability straight off a real-world run, so you don't need a second, risk-neutral simulation. Following [Cheng and Planchet (2018)](https://hal.science/hal-01730072){:target="_blank"}, $$D(T)$$ combines discounting at the simulated short rate with a path weight that turns real-world paths into risk-neutral ones; the value of a cash flow $$X_T$$ is the path average of $$D(T)\,X_T$$.

The weight leaves out turbulence's shock, so the deflator is only accurate when the turbulence premium is small. On the live US fit that premium is large (38.5% of turbulence's speed), and the deflator's average misses the model's own bond prices by about 2% at one year and 5% at five (0.9827 against 0.9620, and 0.7606 against 0.7996); the fit warns when the premium is this large. The deflator is available in Python only; the [KnwSvQ reference](#knwsvq) has a worked example.

<div class="fs-ref"><a href="#knwsvq"><i class="fas fa-book" aria-hidden="true"></i>Full reference: KnwSvQ</a></div>

#### Configuring a KNW Run

A KNW pair is a rate entry and an inflation entry that name each other and use the same method. The fitted coefficients are a recursion applied once per period, with no time step to rescale, so the simulation frequency must equal the fitting period (monthly, quarterly or yearly); the configuration rejects a mismatch.

The settings profile sets the step and the history the pair is fitted on:

```yaml
# my-project/settings/knw.yaml (a settings profile)
start_date: 2026-10-01
engine:
  frequency: quarterly          # must equal the pair's period
toolkit:
  start_date: 1990-01-01        # history used for the fit
```

The factor set holds the pair and the optional equity leg:

```yaml
# my-project/factor-sets/knw.yaml (a factor set)
interest_rates:
  - name: interest_rate
    source: oecd
    country: United States
    term: short
    period: quarterly
    method: knw_sv
    inflation_name: inflation
    # measure: risk_neutral     # on both legs, without the equity entry, for the risk-neutral version

inflation:
  - name: inflation
    country: United States
    period: quarterly
    method: knw_sv
    interest_rate_name: interest_rate

equities:
  - name: equity
    ticker: SPY
    period: quarterly
    method: knw_sv
    nominal_rate_name: interest_rate
```

```python
from financescenarios import Scenarios, load_config

result = Scenarios.from_config(
    load_config("my-project/settings/knw.yaml", "my-project/factor-sets/knw.yaml")
).simulate(years=30)
```

<div class="fs-callout fs-callout--limits" markdown="1">
<p class="fs-callout__title">Limits</p>

- Beliefs, GARCH and business-cycle conditioning are not available: the long-run level is a joint property of both legs, so there is no single long-run mean to override.
- The equity leg needs a real-world rate.
</div>

#### How It Compares with DNB's CP2022

The [CP2022 Technical Appendix](https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix){:target="_blank"} specifies DNB's full model, which the package also runs as written, with DNB's own parameters ([CP2022](#cp2022-model) below). KNW is the version fitted on a pair's own history, for any country. How the two compare:

| Aspect | DNB CP2022 | Finance Scenarios |
|:--|:--|:--|
| Rate and inflation coupling | Full 2x2 matrix | Same |
| Stochastic volatility | Heston-type factor scaling rate, inflation, equity and CPI index | Same structure |
| How turbulence is recovered | Treated as observed, with the rate and expected inflation backed out of a nominal and a real yield | Past year's average of the pair's squared surprises |
| Leverage effect | Turbulence shocks correlated with rate and inflation shocks | Not fitted: independent |
| Equity | Premium and variance constrained by option-implied volatility | Fitted on price history only |
| CPI index row | Modeled | Not modeled |
| Risk-neutral measure | Essentially affine, fitted to nominal and real yields and constrained by option, swaption and inflation-cap implied volatilities | Completely affine, fitted to four nominal Treasury yields |

Without real yields or rate and inflation derivatives data, the risk-neutral version is fitted to the nominal yield curve, standard affine term-structure practice. It is a genuine change of measure, but on different data, so it is a different model from DNB's own, not a simplified copy.

#### References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">10</span></summary>

- Koijen, R.S.J., Nijman, T.E., Werker, B.J.M. (2010). [When Can Life Cycle Investors Benefit from Time-Varying Bond Risk Premia?](https://doi.org/10.1093/rfs/hhp058){:target="_blank"} The Review of Financial Studies, 23(2), 741-780.
- Commissie Parameters (2022). [Technical Appendix: Specification of the CP2022 Model](https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix){:target="_blank"}.
- Heston, S.L. (1993). [A Closed-Form Solution for Options with Stochastic Volatility with Applications to Bond and Currency Options](https://doi.org/10.1093/rfs/6.2.327){:target="_blank"}. The Review of Financial Studies, 6(2), 327-343.
- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). [A Theory of the Term Structure of Interest Rates](https://doi.org/10.2307/1911242){:target="_blank"}. Econometrica, 53(2), 385-407.
- Andersen, L. (2008). [Simple and Efficient Simulation of the Heston Stochastic Volatility Model](https://doi.org/10.21314/jcf.2008.189){:target="_blank"}. Journal of Computational Finance, 11(3), 1-42.
- Duffie, D., Kan, R. (1996). [A Yield-Factor Model of Interest Rates](https://doi.org/10.1111/j.1467-9965.1996.tb00123.x){:target="_blank"}. Mathematical Finance, 6(4), 379-406.
- Duffee, G.R. (2002). [Term Premia and Interest Rate Forecasts in Affine Models](https://doi.org/10.1111/1540-6261.00426){:target="_blank"}. Journal of Finance, 57(1), 405-443.
- Cheng, P.-K., Planchet, F. (2018). [Stochastic Deflator for an Economic Scenario Generator with Five Factors](https://hal.science/hal-01730072){:target="_blank"}. HAL preprint.
- Engle, R.F. (1982). [Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation](https://doi.org/10.2307/1912773){:target="_blank"}. Econometrica, 50(4), 987-1007.
- Lütkepohl, H. (2005). [New Introduction to Multiple Time Series Analysis](https://doi.org/10.1007/978-3-540-27752-1){:target="_blank"}. Springer.

</details>

### DNB's CP2022 Model {#cp2022-model}

Dutch pension funds test their plans on the scenario sets De Nederlandsche Bank (DNB) publishes every quarter: 20,000 scenarios over 100 years from the CP2022 model of the [Commissie Parameters (2022)](https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix){:target="_blank"}. `method: cp2022` runs that model as its Technical Appendix writes it, with the parameters DNB publishes, so a run can rebuild DNB's real-world set or put DNB's economy next to factors of its own.

#### The Model

Three state variables move together: a Heston variance $$v$$, the nominal short rate $$r$$ and expected euro-area inflation $$\pi$$. They revert to their long-run levels through a 3 x 3 matrix $$K$$, so each one's level pulls on the others, and their five shocks are scaled by the variance (Technical Appendix, eqs. 1-6):

$$
dX_t = K\,(\mathbb{E}[X_\infty] - X_t)\,dt + \Sigma(v_t)\,dW_t, \qquad X_t = (v_t, r_t, \pi_t)
$$

The log equity index and the log HICP drift at $$r + \eta_S$$ and $$\pi + \eta_\Pi$$ less half their variance and load on the same shocks, so equity falls when turbulence rises. Nominal and real zero rates of every maturity are exponential-affine in the state, from the Riccati equations of section 10 (eqs. 14-19 and 76-79); they give back DNB's published tables to within 2e-6. Dutch CPI inflation is the HICP's plus a spread that follows CPB's forecasts and then 2% (section 8, eqs. 48-55). The run steps the model monthly with the appendix's own scheme (section 9.1, eqs. 51-53), with [Andersen's (2008)](https://doi.org/10.21314/jcf.2008.189){:target="_blank"} quadratic-exponential step for the variance.

#### The Parameters

Each quarterly workbook DNB publishes carries the model's parameters on its `0_Parameters` sheet, next to the term-structure functions of the nominal and real curves and the paths of the three state variables. The package stores each quarter as a vintage, and a run reads the one DNB had published by its calibration date; `python -m financescenarios.anchors update` checks DNB's page and stores a new quarter. The 2026Q4 set ships with the package.

The parameters can also be backed out of a set's own 20,000 paths: `estimate_cp2022` matches the exact yearly moments of the monthly scheme to regressions of the yearly moves on the starting state, by minimum distance, with the Commissie's constraints imposed. On the 2026Q4 set every well-identified parameter comes back within about two standard errors of DNB's:

| Parameter | DNB | Estimated (standard error) |
|:--|--:|--:|
| $$K_{vv}$$ | 2.7889 | 2.7892 (0.018) |
| $$K_{rr}$$ | 0.4827 | 0.4847 (0.0011) |
| $$K_{\pi r}$$ | -0.9213 | -0.9242 (0.0027) |
| $$K_{\pi\pi}$$ | 0.5955 | 0.5949 (0.0017) |
| $$\mathbb{E}[v]$$ | 0.05407 | 0.05408 (0.00005) |
| Equity volatility at $$\mathbb{E}[v]$$ | 15.53% | 15.53% (0.01) |

A variance reverting at a speed of 2.79 a year halves its distance to the long-run level in about three months.

#### In a Run

Rates (`maturity` 1 to 100 years, `curve: nominal` or the euro-area `real` curve), inflation (`index: hicp` or `dutch_cpi`) and one equity take `method: cp2022`, and every such entry is an output of the same model. Its equity, HICP and shortest rate carry the run's correlated draws, and the model turns those into its five independent shocks, so the model's own correlations hold exactly while any other factor in the set correlates with it through the usual estimate on history. The `dnb` factor set holds the euro 1-, 5-, 10-, 20- and 30-year nominal rates, the real 10-year rate, euro-area and Dutch inflation and world equity; the `dnb` settings run it monthly over 100 years with 2,000 scenarios.

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(settings="dnb", factor_set="dnb")
result = scenarios.simulate()
```

A rate entry of your own:

```yaml
# my-project/factor-sets/my_factors.yaml (a factor set)
interest_rates:
  - name: euro_10y
    method: cp2022
    curve: nominal
    maturity: 10
    currency: EUR
```

#### Against DNB's 2026Q4 Set

The `dnb` set with 2,000 scenarios against DNB's 20,000, in percent, run / DNB:

| Variable | Year | Mean | Standard deviation | 5th percentile | Median | 95th percentile |
|:--|--:|--:|--:|--:|--:|--:|
| Nominal 1-year rate | 1 | 2.73 / 2.77 | 0.90 / 0.91 | 1.44 / 1.43 | 2.63 / 2.68 | 4.34 / 4.37 |
| | 10 | 1.54 / 1.54 | 1.45 / 1.45 | -0.63 / -0.73 | 1.50 / 1.49 | 3.95 / 4.01 |
| | 100 | 1.02 / 1.01 | 1.54 / 1.52 | -1.44 / -1.40 | 1.01 / 0.97 | 3.59 / 3.58 |
| Nominal 10-year rate | 1 | 3.21 / 3.22 | 0.69 / 0.69 | 2.15 / 2.14 | 3.18 / 3.20 | 4.41 / 4.38 |
| | 10 | 2.31 / 2.31 | 1.29 / 1.29 | 0.27 / 0.22 | 2.30 / 2.29 | 4.47 / 4.48 |
| | 100 | 2.01 / 2.01 | 1.39 / 1.37 | -0.28 / -0.22 | 2.01 / 1.98 | 4.27 / 4.30 |
| Real 10-year rate | 1 | 1.02 / 1.03 | 0.67 / 0.67 | 0.03 / 0.01 | 0.97 / 0.98 | 2.21 / 2.20 |
| | 30 | 0.04 / 0.00 | 1.07 / 1.08 | -1.68 / -1.70 | 0.03 / -0.03 | 1.84 / 1.84 |
| Euro-area inflation | 1 | 2.44 / 2.48 | 0.93 / 0.96 | 1.06 / 1.05 | 2.40 / 2.41 | 4.02 / 4.14 |
| | 100 | 1.97 / 2.02 | 1.17 / 1.18 | 0.22 / 0.25 | 1.91 / 1.95 | 3.96 / 4.06 |
| Dutch inflation | 1 | 2.85 / 2.85 | 0.93 / 0.96 | 1.46 / 1.42 | 2.81 / 2.78 | 4.44 / 4.53 |
| Equity, return that year | 1 | 9.13 / 8.45 | 13.65 / 14.21 | -15.70 / -17.34 | 10.47 / 10.03 | 29.60 / 28.94 |
| | 100 | 6.29 / 6.54 | 15.16 / 15.32 | -20.92 / -21.02 | 8.02 / 8.08 | 27.04 / 28.70 |
| Equity, annualized over 100 years | 100 | 5.62 / 5.57 | 1.63 / 1.63 | 2.79 / 2.84 | 5.65 / 5.61 | 8.19 / 8.22 |

The correlations match as well: equity against the 1-year rate is -0.47 against DNB's -0.49 in year 1, inflation against the 10-year rate 0.28 against 0.25, and the real against the nominal 10-year rate 0.93 against 0.93. The gaps that remain are within two or three Monte Carlo standard errors of 2,000 scenarios; with 20,000, year 1 gives an equity return of 8.49% against DNB's 8.45%. `Dnb.compare_moments` and `Dnb.compare_correlations` (see [external benchmarks](/projects/financescenarios/docs/validation#external-benchmarks)) set any run beside DNB's set this way.

<div class="fs-callout fs-callout--limits" markdown="1">
<p class="fs-callout__title">Limits</p>

- Real world only. DNB's market-consistent set is calibrated to equity options, swaptions and inflation caps and floors (eq. 25), which needs paid market data. `external_scenario_source` with `provider: dnb` still reads DNB's own paths, either set.
- DNB's sets carry a long-run equity return of ln(1.054), the advice's 5.4% before costs, where eq. 41 states 5.2% after them; DNB's page says to take the 20 basis points of costs off for net returns.
- The term-structure functions carry the fit to DNB's valuation-date curves, whose monthly inputs are not published. Between whole years they are interpolated linearly, so rates are exact at every whole year and close in between.
- The model's scheme is monthly, so a run with `cp2022` entries steps monthly.
</div>

### References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">41</span></summary>

- Adrian, T., Crump, R.K., Moench, E. (2013). "Pricing the Term Structure with Linear Regressions." Journal of Financial Economics, 110(1), 110-138. [doi.org](https://doi.org/10.1016/j.jfineco.2013.04.009){:target="_blank"}
- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. [casact.org](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf){:target="_blank"}
- Andersen, L. (2008). "Simple and Efficient Simulation of the Heston Stochastic Volatility Model." Journal of Computational Finance, 11(3), 1-42. [doi.org](https://doi.org/10.21314/jcf.2008.189){:target="_blank"}
- Bank of England. Bank Rate history and data. [bankofengland.co.uk](https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp){:target="_blank"}
- Bank of England. Yield curves: nominal spot curve of gilts, daily and month-end. [bankofengland.co.uk](https://www.bankofengland.co.uk/statistics/yield-curves){:target="_blank"}
- Bank of England (2025). Monetary Policy Report, February 2025, Box A. [bankofengland.co.uk](https://www.bankofengland.co.uk/monetary-policy-report/2025/february-2025){:target="_blank"}
- Black, F. (1995). "Interest Rates as Options." The Journal of Finance, 50(5), 1371-1376. [doi.org](https://doi.org/10.1111/j.1540-6261.1995.tb05182.x){:target="_blank"}
- Board of Governors of the Federal Reserve System. Open Market Operations: federal funds target ranges. [federalreserve.gov](https://www.federalreserve.gov/monetarypolicy/openmarket.htm){:target="_blank"}
- Board of Governors of the Federal Reserve System (2018). Policy Rules and How Policymakers Use Them. [federalreserve.gov](https://www.federalreserve.gov/monetarypolicy/policy-rules-and-how-policymakers-use-them.htm){:target="_blank"}
- Board of Governors of the Federal Reserve System (2026). Monetary Policy Report, July 2026, Part 2, Box 4. [federalreserve.gov](https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-part2.htm){:target="_blank"}
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." Journal of Econometrics, 31(3), 307-327. [doi.org](https://doi.org/10.1016/0304-4076(86)90063-1){:target="_blank"}
- Brigo, D., Mercurio, F. (2001). "A Deterministic-Shift Extension of Analytically-Tractable and Time-Homogeneous Short-Rate Models." Finance and Stochastics, 5(3), 369-387. [doi.org](https://doi.org/10.1007/pl00013541){:target="_blank"}
- Brigo, D., Mercurio, F. (2006). Interest Rate Models: Theory and Practice (2nd ed.). Springer Finance. [doi.org](https://doi.org/10.1007/978-3-540-34604-3){:target="_blank"}
- Campbell, J.Y., Shiller, R.J. (1991). "Yield Spreads and Interest Rate Movements: A Bird's Eye View." The Review of Economic Studies, 58(3), 495-514. [doi.org](https://doi.org/10.2307/2298008){:target="_blank"}
- Commissie Parameters (2022). "Technical Appendix: Specification of the CP2022 Model." [rijksoverheid.nl](https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix){:target="_blank"}
- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). "A Theory of the Term Structure of Interest Rates." Econometrica, 53(2), 385-407. [doi.org](https://doi.org/10.2307/1911242){:target="_blank"}
- Deutsche Bundesbank. Term structure of interest rates on listed Federal securities (method by Svensson), daily and monthly. [bundesbank.de](https://www.bundesbank.de/en/statistics/money-and-capital-markets/interest-rates-and-yields/term-structure-of-interest-rates){:target="_blank"}
- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. [doi.org](https://doi.org/10.1016/j.jeconom.2005.03.005){:target="_blank"}
- EIOPA (2026). Technical documentation of the methodology to derive EIOPA's risk-free interest rate term structures, applicable from 30 January 2027. [eiopa.europa.eu](https://www.eiopa.europa.eu/eiopa-publishes-rfr-technical-documentation-become-applicable-30-january-2027-2026-05-26_en){:target="_blank"}
- European Central Bank (2021). The ECB's monetary policy strategy statement, 8 July 2021. [ecb.europa.eu](https://www.ecb.europa.eu/home/search/review/html/ecb.strategyreview_monpol_strategy_statement.en.html){:target="_blank"}
- European Central Bank. Official interest rates: key ECB interest rates. [ecb.europa.eu](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/html/index.en.html){:target="_blank"}
- European Commission (2026). AMECO, Spring 2026 forecast: ZNAWRU. [ec.europa.eu](https://ec.europa.eu/economy_finance/ameco/wq/series?fullVariable=1.0.0.0.ZNAWRU&countries=FRA,GBR,DEU&years=2027&lastYear=0&yearOrder=ASC){:target="_blank"}
- European Parliament and Council (2009). "Directive 2009/138/EC (Solvency II)", consolidated text of 17 January 2025, Articles 77 and 77a. [eur-lex.europa.eu](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02009L0138-20250117){:target="_blank"}
- Federal Open Market Committee (2026). Statement on Longer-Run Goals and Monetary Policy Strategy. [federalreserve.gov](https://www.federalreserve.gov/monetarypolicy/files/fomc_longerrungoals.pdf){:target="_blank"}
- Federal Open Market Committee (2026). Summary of Economic Projections, 16 September 2026, Table 1. [federalreserve.gov](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm){:target="_blank"}
- Federal Reserve Bank of New York (2026). Measuring the natural rate of interest: Holston-Laubach-Williams and Laubach-Williams estimates, current and real-time. [newyorkfed.org](https://www.newyorkfed.org/research/policy/rstar){:target="_blank"}
- Federal Reserve Bank of New York (2026). Treasury Term Premia (ACMTP10, ACMRNY10). [newyorkfed.org](https://www.newyorkfed.org/research/data_indicators/term-premia-tabs){:target="_blank"}
- Gürkaynak, R.S., Sack, B., Wright, J.H. (2007). "The U.S. Treasury Yield Curve: 1961 to the Present." Journal of Monetary Economics, 54(8), 2291-2304. [doi.org](https://doi.org/10.1016/j.jmoneco.2007.06.029){:target="_blank"}
- Heath, D., Jarrow, R., Morton, A. (1992). "Bond Pricing and the Term Structure of Interest Rates: A New Methodology for Contingent Claims Valuation." Econometrica, 60(1), 77-105. [doi.org](https://doi.org/10.2307/2951677){:target="_blank"}
- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert Limited. [ressources-actuarielles.net](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf){:target="_blank"}
- HM Treasury (2025). Monetary policy remit: Budget 2025, letter from the Chancellor of the Exchequer to the Governor of the Bank of England, 26 November 2025. [gov.uk](https://www.gov.uk/government/publications/monetary-policy-remit-budget-2025/letter-from-chancellor-of-the-exchequer-to-govenor-of-the-bank-of-england){:target="_blank"}
- Hull, J., White, A. (1990). "Pricing Interest-Rate-Derivative Securities." The Review of Financial Studies, 3(4), 573-592. [doi.org](https://doi.org/10.1093/rfs/3.4.573){:target="_blank"}
- Jotikasthira, C., Le, A., Lundblad, C. (2015). "Why Do Term Structures in Different Currencies Co-move?" Journal of Financial Economics, 115(1), 58-83. [doi.org](https://doi.org/10.1016/j.jfineco.2014.09.004){:target="_blank"}
- Malik, S., Meldrum, A. (2016). "Evaluating the Robustness of UK Term Structure Decompositions Using Linear Regression Methods." Journal of Banking & Finance, 67, 85-102. [doi.org](https://doi.org/10.1016/j.jbankfin.2016.02.006){:target="_blank"}
- Nelson, C.R., Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." The Journal of Business, 60(4), 473-489. [doi.org](https://doi.org/10.1086/296409){:target="_blank"}
- Tang, C.Y., Chen, S.X. (2009). "Parameter Estimation and Bias Correction for Diffusion Processes." Journal of Econometrics, 149(1), 65-81. [doi.org](https://doi.org/10.1016/j.jeconom.2008.11.001){:target="_blank"}
- Taylor, J.B. (1993). "Discretion versus Policy Rules in Practice." Carnegie-Rochester Conference Series on Public Policy, 39, 195-214. [doi.org](https://doi.org/10.1016/0167-2231(93)90009-L){:target="_blank"}
- U.S. Department of the Treasury. Daily Treasury Bill Rates: bank discount rate and coupon equivalent. [treasury.gov](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_bill_rates&field_tdr_date_value=202610){:target="_blank"}
- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. [doi.org](https://doi.org/10.1016/0304-405x(77)90016-2){:target="_blank"}
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. [doi.org](https://doi.org/10.1017/S0071368600009009){:target="_blank"}
- Wright, J.H. (2011). "Term Premia and Inflation Uncertainty: Empirical Evidence from an International Panel Dataset." American Economic Review, 101(4), 1514-1534. [doi.org](https://doi.org/10.1257/aer.101.4.1514){:target="_blank"}

</details>
