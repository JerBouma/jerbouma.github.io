---
title: Models
seo_title: "DCF, DuPont and Valuation Models in Python | Finance Toolkit"
seo_title_suffix: false
excerpt: The Models module is meant to execute well-known models such as DUPONT and the Discounted Cash Flow (DCF) model. These models are also directly related to the data retrieved from the Toolkit module.
description: "DuPont analysis, discounted cash flow (DCF), WACC, the Altman Z-Score, the Piotroski F-Score and other valuation models in Python with the Finance Toolkit."
author_profile: false
permalink: /projects/financetoolkit/docs/models
classes: wide-sidebar
layout: single
redirect_from:
    - /models
    - /projects/financetoolkit/models-notebook
    - /projects/financetoolkit/models-module
sidebar:
    nav: "financetoolkit-docs-models"
---

The Models module executes well-known models such as DuPont analysis and the Discounted Cash Flow (DCF) model, using data retrieved from the Toolkit module.

Use it in Claude, ChatGPT or another AI assistant through the [Finance Toolkit MCP](/projects/financetoolkit/mcp), or install the Python package:

```python
pip install financetoolkit -U
```

{% include docs-search.html %}

{% include financetoolkit-getting-started/models.md %}

## get_factor_analysis
Factor analysis (predictive power) of the models: whether the tickers that score high on a model, such as the Piotroski F-Score or the Altman Z-Score, go on to return more than those that score low. Per period, the information coefficient (IC) is the Spearman rank correlation between the model score of the tickers at the end of the period and their return over the following horizon: 1 means the score ranks the later returns perfectly, -1 in reverse and 0 that it says nothing about them. The IC measures skill in Grinold and Kahn's fundamental law of active management, $$\text{IR} \approx \text{IC} \times \sqrt{\text{breadth}}$$: a small but consistent IC across many tickers and periods gives a high information ratio.

The summary has a row per model and horizon with the mean IC, its standard deviation, the IC information ratio (mean divided by standard deviation), the t-statistic of the mean with its p-value, the skewness and excess kurtosis of the IC, the share of periods with a positive IC, the number of periods, the top minus bottom spread (the mean forward return of the highest quantile minus that of the lowest), the annualized alpha and the beta of the factor-weighted long-short portfolio against the equally weighted tickers, the mean turnover of the top and bottom quantiles and the mean rank autocorrelation of the score from one period to the next. With detail, it returns one part of the analysis per period, quantile or group for a single model.

The formula is as follows:

$$
\operatorname{IC}(t) = \text{Spearman rank correlation of} \;f(i,\; t) \;\text{and} \;R(i,\; t,\; t + h) \;\text{over the tickers}\; i,\;\; \text{with } f \text{ the factor and } R \text{ the forward return over the horizon } h
$$

- Demeaned return: R(i, t) − mean R(j, t) over the tickers j (of the group of i)

$$
\text{Portfolio weight:}\;\; w(i,\; t) = \frac{f(i,\; t) - \text{mean} \;f(t)}{\Sigma_{j} \left|f(j,\; t) - \text{mean} \;f(t)\right|}
$$

$$
\text{Portfolio return:}\;\; R_{F}(t) = \Sigma_{i} w(i,\; t) \cdot R(i,\; t,\; t + h)
$$

$$
\text{Alpha and beta:}\;\; R_{F}(t) = \alpha + \beta \cdot R_{U}(t) + \epsilon(t),\;\; \text{with}\;\; R_{U}(t) = \text{mean} \;R(i,\; t,\; t + h)
$$

$$
\text{Annualized Alpha} = (1 + \alpha)^{\frac{\text{periods per year}}{h}} - 1
$$

$$
\text{Per period:}\;\; (1 + \text{mean return})^{\frac{1}{h}} - \frac{1 \;\text{and standard error}}{\sqrt{h}}
$$

$$
\text{Standard error of a quantile} = \text{standard deviation over the periods} \;/ \sqrt{\text{periods}}
$$

The models are calculated per statement period and each period's score applies from the end of the fiscal period, or with point_in_time from the day it was filed, never earlier, so no day uses figures that were not known yet. The returns use the dividend and split adjusted close and start at the close of the period the score belongs to. Each ticker keeps its own history: a ticker without a score or a return in a period is left out of that period only.

**Args:**

- <u>metrics (str &#124; list[str], optional):</u> A model method name with one value per
ticker and period, e.g. "get_piotroski_score", a list of them, or a
collection: "scores" or "all". Defaults to "scores", the Piotroski, Altman Z,
Beneish M, Ohlson O, Zmijewski, Springate, Grover, Fulmer H, Taffler z,
Campbell-Hilscher-Szilagyi, Shumway, Dechow F, Montier C and Mohanram G
scores. "all" adds the accruals ratio, Tobin's Q, the sustainable and internal
growth rates, the magic formula and the Merton distance to default. The
valuation models and the analyses with several components and no score are not
in the collections.
- <u>period (str, optional):</u> The frequency at which the models are evaluated: daily,
weekly, monthly, quarterly or yearly. Defaults to "monthly".
- <u>horizons (list[int] &#124; int &#124; None, optional):</u> The number of periods the forward
returns cover. Defaults to None, which uses about a period, a quarter and a
year ahead (1, 3 and 12 months for monthly).
- <u>quantiles (int, optional):</u> The number of quantiles the tickers are sorted into per
period. Defaults to 5.
- <u>periods_apart (int, optional):</u> The number of periods between the dates the
quantile turnover and the rank autocorrelation compare. Defaults to 1.
- <u>detail (str &#124; None, optional):</u> Returns one part of the analysis of a single model
instead of the summary: "information_coefficient" (per period and horizon),
"information_coefficient_by_month" or "information_coefficient_by_year" (the mean IC
per calendar month or year), "group_information_coefficient" (the IC statistics
within each group, needs group), "quantile_returns" (the mean forward return per
quantile and horizon), "quantile_returns_by_date" (per period),
"quantile_return_statistics" (the mean, its standard error and both per single
period), "quantile_statistics" (the range, mean and count of the factor values in
each quantile), "quantile_turnover" (per period and quantile),
"rank_autocorrelation" (per period), "factor_weights" (the weights of the
factor-weighted long-short portfolio per period and ticker), "factor_returns" (its
return per period and horizon), "cumulative_returns" (the growth of 1 in it and in
each quantile) or "event_returns" (the mean price path of each quantile from the
longest horizon before to the longest horizon after the periods it is formed).
Defaults to None.
- <u>column (str &#124; None, optional):</u> The component to use of a model, e.g.
"Working Capital to Total Assets" of the Altman Z-Score. Defaults to None,
which uses the model's score (its last row).
- <u>group (str &#124; dict &#124; None, optional):</u> The group of each ticker for the group options:
"sector" or "industry" (or another company profile item) from the company profiles
of Financial Modeling Prep, or a dictionary of tickers and their groups. Defaults to
None.
- <u>demeaned (bool, optional):</u> Whether to compare the forward returns with the mean of
the tickers in each period, or with group with the mean of the ticker's group:
a group-neutral analysis, in which the IC is group-adjusted and the
factor-weighted portfolio neutral within each group. Without group the IC
stays the same, as subtracting one mean from every ticker keeps their ranks.
Defaults to False.
- <u>binning (str, optional):</u> How the tickers are sorted into quantiles per period:
"quantile" (equally sized), "equal_width" (bins of equal width between the lowest
and highest value), "zero_aware" (half of the quantiles for the negative and half
for the zero and positive values, for a signal centred on zero; needs an even number
of quantiles) or "group" (equally sized within each group, needs group). Defaults to
"quantile".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
**kwargs: Parameters passed to the models that take them, e.g. trailing=4 or
diluted=False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The summary per model and horizon, or with detail that part of the
analysis of the model.

**Notes:**

- The IC is reported as measured: for a distress score where a higher value means
more risk (Ohlson O, Zmijewski, Beneish M), a negative IC means the riskier
companies went on to return less. Read the sign as the direction of the
relationship.
- Scores that take few values (the Piotroski F-Score from 0 to 9) tie many
tickers; ties are split over adjacent quantiles by the order of the tickers.
- The cross-section is the tickers of the Toolkit, so use at least ten and
preferably twenty or more for a meaningful rank correlation and quantiles.
- A horizon longer than one period makes consecutive returns overlap, which
inflates the t-statistic; judge those horizons by their mean IC and IC
information ratio.
- The groups from the company profiles are today's sector or industry, applied
to every period.
- The factor-weighted portfolio is long-short: its weights sum to zero and their
absolute values to one. A horizon longer than one period makes its returns
overlap too, so its alpha and beta are averages rather than tests.
- The cumulative returns split the capital over as many portfolios as the horizon
has periods, started on consecutive periods and each rebalanced once per
horizon; a value shows when its holding period ends, so the series starts at 1.
- The IC is that of Grinold, R.C. and Kahn, R.N. (2000). "Active Portfolio
Management." 2nd ed. McGraw-Hill; the factor-weighted portfolio, the demeaned
and group-neutral returns that of Qian, E., Hua, R. and Sorensen, E. (2007).
"Quantitative Equity Portfolio Management." Chapman & Hall/CRC; the alpha that
of Jensen, M.C. (1968). "The Performance of Mutual Funds in the Period
1945-1964." Journal of Finance 23(2); the event returns follow MacKinlay, A.C.
(1997). "Event Studies in Economics and Finance." Journal of Economic Literature
35(1).
- Referenced against alphalens-reloaded
([https://github.com/stefan-jansen/alphalens-reloaded](https://github.com/stefan-jansen/alphalens-reloaded){:target="_blank"}). Its top minus bottom
spread is half of the one here (a gross exposure of one rather than two), it
drops a period and ticker without every horizon's return where each horizon
here uses its own, and its event returns average the single-period returns at
each offset where these are the price paths rebased to the period itself.

Also known as: predictive power, information coefficient, factor testing, alpha signal

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "JPM", "JNJ",
     "XOM", "PG", "KO", "WMT", "V", "UNH", "HD", "CVX"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2016-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_factor_analysis(
    ["get_piotroski_score", "get_altman_z_score"], horizons=12
)
```

Which returns:

|                                      |   Mean IC |   IC Standard Deviation |   IC Information Ratio |   t-Statistic |   p-Value |   IC Skewness |   IC Kurtosis |   Positive Share |   Observations |   Top Minus Bottom |   Annualized Alpha |    Beta |   Quantile Turnover |   Rank Autocorrelation |
|:-------------------------------------|----------:|------------------------:|-----------------------:|--------------:|----------:|--------------:|--------------:|-----------------:|---------------:|-------------------:|-------------------:|--------:|--------------------:|-----------------------:|
| ('get_piotroski_score', '12 Months') |   -0.1353 |                  0.3685 |                -0.3672 |       -3.6724 |    0.0004 |        0.3723 |       -0.1763 |             0.31 |            100 |            -0.1482 |             0.0279 | -0.3828 |              0.0787 |                 0.93   |
| ('get_altman_z_score', '12 Months')  |    0.1179 |                  0.3915 |                 0.3011 |        3.0112 |    0.0033 |       -0.657  |       -0.2792 |             0.66 |            100 |             0.1564 |            -0.1619 |  1.2913 |              0.0258 |                 0.9939 |

---

## get_kaplan_zingales_index
Calculates the Kaplan-Zingales (KZ) index of financial constraints, a measure of how hard it is for a firm to fund its investments with external finance, as constructed by Lamont, Polk and Saa-Requejo (2001). Kaplan and Zingales (1997) read the annual reports of the 49 low-dividend manufacturing firms of Fazzari, Hubbard and Petersen (1988), classified every firm-year from not to undoubtedly financially constrained and related the classes to accounting ratios with an ordered logit. Lamont, Polk and Saa-Requejo use Steven Kaplan's re-estimation of that logit on the five ratios available in Compustat as an index.

The formula is as follows:

$$
\text{Cash Flow to Capital} = \frac{\text{Income Before Extraordinary Items} + \text{Depreciation and Amortization}}{\text{Lagged Net PP\&E}}
$$

$$
Q = \frac{\text{Total Assets} + \text{Market Value of Equity} - \text{Common Equity} - \text{Deferred Taxes}}{\text{Total Assets}}
$$

$$
\text{Debt to Total Capital} = \frac{\text{Long-Term Debt} + \text{Short-Term Debt}}{\text{Long-Term Debt} + \text{Short-Term Debt} + \text{Total Shareholder Equity}}
$$

$$
\text{Dividends to Capital} = \frac{\text{Common} + \text{Preferred Dividends}}{\text{Lagged Net PP\&E}}
$$

$$
\text{Cash to Capital} = \frac{\text{Cash and Short-Term Investments}}{\text{Lagged Net PP\&E}}
$$

$$
\text{KZ} = - 1.001909 \cdot \text{Cash Flow to Capital} + 0.2826389 \cdot Q + 3.139193 \cdot \text{Debt to Total Capital} - 39.3678 \cdot \text{Dividends to Capital} - 1.314759 \cdot \text{Cash to Capital}
$$

The variables follow the appendix of Lamont, Polk and Saa-Requejo (Compustat items):

- Income Before Extraordinary Items (item 18): the net income from continuing operations, or the net income where it is not reported.
- Depreciation and Amortization (item 14): that of the cash flow statement.
- Net PP&E (item 8): the net property, plant and equipment at the end of the previous period (on quarterly data, at the start of the trailing window).
- Total Assets (item 6), Common Equity (item 60: the shareholders' equity less the preferred stock), Deferred Taxes (item 74: the deferred tax liabilities), Long-Term Debt (item 9), Short-Term Debt (item 34: the debt in current liabilities), Total Shareholder Equity (item 216: preferred stock included, minority interests excluded), Common and Preferred Dividends (items 21 and 19) and Cash and Short-Term Investments (item 1).
- Market Value of Equity: the close at the end of the fiscal period times the period's weighted average shares (CRSP's December market equity in the paper).

The Kaplan-Zingales index can be interpreted as follows:

- A higher index means a more constrained firm. Lamont, Polk and Saa-Requejo call the top third of firms ranked on the index each year constrained and the bottom third unconstrained; the index has no absolute cut-off.
- Whited and Wu (2006, Table 2) report quartile means of 0.25, 0.77, 1.15 and 1.81 on quarterly Compustat data for 1975-2001, with the cash flow, the dividends, the cash and the long-term debt scaled by total assets instead of capital and total capital, so the levels of this index (ratios to net PP&E) are not comparable to theirs; compare firms by their rank.

**Also known as:** KZ index, Kaplan-Zingales, financing constraints, external finance.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The number of periods the cash flow and the
dividends are summed over, with the capital they are divided by taken that many
periods earlier; the other balances are those at the end of the period. The
window counts calendar periods, so a period without a report makes it NaN.
Defaults to None, which is 4 on quarterly data (a trailing twelve months), as
the index was estimated on yearly statements.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Kaplan-Zingales index and its five ratios per ticker and period.

**Notes:**

- The first period is NaN because the capital is that of the period before.
- Kaplan and Zingales (1997) estimated the logit on low-dividend manufacturing firms
with growing sales; Lamont, Polk and Saa-Requejo apply it to all manufacturing
firms with growing real sales. For other industries (financial firms in particular,
whose PP&E is small) the ratios to capital become large and the index is only
indicative.
- FinancialModelingPrep's net PP&E of some companies includes the right-of-use assets
of operating leases, which Compustat's item 8 leaves out, and for some only in the
fiscal year-end statements (Apple's, by about $10 billion, so its quarterly index
jumps in every fiscal fourth quarter). The ratios to capital are lower where it does.
- The index has been criticized as a measure of constraints: Whited and Wu (2006) and
Hadlock and Pierce (2010) find that it classifies firms with characteristics of
unconstrained firms as constrained, which get_whited_wu_index and
get_size_age_index address.

References:
- Lamont, Owen, Christopher Polk and Jesus Saa-Requejo. "Financial Constraints and Stock
Returns." The Review of Financial Studies, Vol. 14, No. 2, 2001, pp. 529-554.
- Kaplan, Steven N. and Luigi Zingales. "Do Investment-Cash Flow Sensitivities Provide Useful
Measures of Financing Constraints?" The Quarterly Journal of Economics, Vol. 112, No. 1,
1997, pp. 169-215.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "F", "SMP"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2020-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_kaplan_zingales_index().xs("Kaplan-Zingales Index", level=1)
```

Which returns:

|      |     2020 |     2021 |     2022 |     2023 |    2024 |    2025 |
|:-----|---------:|---------:|---------:|---------:|--------:|--------:|
| AAPL | -15.9535 | -12.4285 | -10.9185 | -10.4628 | -9.5516 | -9.3348 |
| F    |   1.4737 |   1.0274 |   0.4525 |  -1.6085 | -0.2481 |  0.3139 |
| SMP  |  -4.1242 |  -7.6728 |  -6.1412 |  -6.2198 | -3.3562 | -2.8463 |

---

## get_whited_wu_index
Calculates the Whited-Wu (WW) index of financial constraints, the shadow value of external funds that Whited and Wu (2006) estimate from the Euler equation of a firm's investment on quarterly Compustat data for 1975-2001. Where the Kaplan-Zingales index comes from a classification of a few firms, this index is the cost of external finance implied by how firms invest, and leaves out Tobin's Q, which measures investment opportunities with much error. Sales growth and the industry's sales growth take its place: a constrained firm is one with good investment opportunities (a growing industry) it cannot fund (it grows less).

The formula is as follows:

$$
\text{CF} = \frac{\text{Income Before Extraordinary Items} + \text{Depreciation and Amortization}}{\text{Total Assets}}
$$

$$
\text{DIVPOS} = 1 \;\text{if the firm paid cash dividends} \;(\text{common or preferred}) \;\text{else}\; 0
$$

$$
\text{TLTD} = \frac{\text{Long-Term Debt}}{\text{Total Assets}}
$$

$$
\text{LNTA} = \ln(\text{Total Assets in millions})
$$

$$
\text{SG} = \frac{\text{Revenue} - \text{Previous Revenue}}{\left|\text{Previous Revenue}\right|}
$$

$$
\text{ISG} = \text{the average SG of the tickers in the firm's industry}
$$

$$
\text{WW} = - 0.091 \cdot \text{CF} - 0.062 \cdot \text{DIVPOS} + 0.021 \cdot \text{TLTD} - 0.044 \cdot \text{LNTA} + 0.102 \cdot \text{ISG} - 0.035 \cdot \text{SG}
$$

The coefficients are those of equation 13 (column 4 of Table 1) of Whited and Wu (2006). The variables are those of Hennessy and Whited (2007) and Farre-Mensa and Ljungqvist (2016):

- Income Before Extraordinary Items: the net income from continuing operations, or the net income where it is not reported.
- Depreciation and Amortization: that of the cash flow statement.
- Total Assets and Long-Term Debt: at the end of the period.
- The sales growth compares with the period before on yearly data and with the same quarter a year earlier on quarterly data, which leaves out the seasons.

The industry sales growth is the average sales growth (equally weighted, the firm itself included) of the tickers in the Toolkit that share the firm's industry in their company profile (FinancialModelingPrep's industry, close to the three-digit SIC industries of Whited and Wu). A firm without industry peers in the Toolkit, or without a profile, uses its own sales growth: add companies of its industry to the tickers for an industry figure.

The Whited-Wu index can be interpreted as follows:

- A higher index means a more constrained firm. As with the Kaplan-Zingales index, the literature calls the top third of firms constrained and the bottom third unconstrained, each year; the index has no absolute cut-off.
- The size term dominates the level: -0.044 * ln(assets in millions) is about -0.20 for a firm with $100 million of assets and -0.51 for one with $100 billion, so the index of most listed firms lies between about -0.6 and -0.1 on yearly data.

**Also known as:** WW index, Whited-Wu, financing constraints, shadow cost of external funds.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The number of periods the cash flow, the dividends
and the revenue are summed over; the balances are those at the end of the period.
The window counts calendar periods, so a period without a report makes it NaN.
Defaults to None, which is a single period: the quarter on quarterly data, as the
index was estimated on quarterly statements.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Whited-Wu index and its six components per ticker and period.

**Notes:**

- The first period (the first four on quarterly data) is NaN because the sales growth
needs a period to compare with.
- On yearly statements the cash flow is a year's, four times a quarter's, so the CF
term weighs more than in the quarterly estimation; this is how the index is
commonly applied to yearly Compustat data (Hennessy and Whited 2007).
- Whited and Wu's Tables 2 and 3 report quartile means of a "structural index" of
0.55 to 0.80, a level equation 13 does not reproduce (it has no constant, and the
Euler equation is estimated in first differences, which leaves the level
unidentified). Compare firms by their rank on the index, as the literature does.
- The total assets are taken in the currency of the statements, so for a company
reporting in a currency other than the US dollar the LNTA term (and the index) shifts
by -0.044 times the log of the exchange rate; compare such companies within their
currency, or retrieve the statements converted to US dollars.

References:
- Whited, Toni M. and Guojun Wu. "Financial Constraints Risk." The Review of Financial Studies,
Vol. 19, No. 2, 2006, pp. 531-559.
- Hennessy, Christopher A. and Toni M. Whited. "How Costly Is External Financing? Evidence from
a Structural Estimation." The Journal of Finance, Vol. 62, No. 4, 2007, pp. 1705-1745.
- Farre-Mensa, Joan and Alexander Ljungqvist. "Do Measures of Financial Constraints Measure
Financial Constraints?" The Review of Financial Studies, Vol. 29, No. 2, 2016, pp. 271-308.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["F", "GM", "LEA", "SMP"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2020-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_whited_wu_index().xs("Whited-Wu Index", level=1)
```

Which returns:

|     |    2020 |    2021 |    2022 |    2023 |    2024 |    2025 |
|:----|--------:|--------:|--------:|--------:|--------:|--------:|
| F   | -0.6137 | -0.6083 | -0.5897 | -0.602  | -0.6054 | -0.6073 |
| GM  | -0.6182 | -0.6054 | -0.6006 | -0.6063 | -0.609  | -0.6122 |
| LEA | -0.4838 | -0.4732 | -0.4797 | -0.4865 | -0.4812 | -0.4755 |
| SMP | -0.3814 | -0.3745 | -0.375  | -0.3751 | -0.3894 | -0.3925 |

---

## get_size_age_index
Calculates the size-age (SA) index of financial constraints of Hadlock and Pierce (2010). They coded the financial constraints of a random sample of firms from the text of their 10-K filings (1995-2004) and found that, of the usual measures, only size and age predict the constraints well: the Kaplan-Zingales ratios do not, once size and age are known. The index is their ordered logit on size and age alone, so it needs no market data and has few of the accounting choices that move the other indices.

The formula is as follows:

$$
\text{Size} = \ln(\min(\text{Total Assets in millions of 2004 dollars},\; \text{4,500}))
$$

$$
\text{Age} = \min(\text{Years Listed},\; 37)
$$

$$
\text{SA} = - 0.737 \cdot \text{Size} + 0.043 \cdot \text{Size}^{2} - 0.040 \cdot \text{Age}
$$

The variables are as follows:

- Total Assets in 2004 dollars: the total assets at the end of the fiscal period divided by the US consumer price index (CPI-U, all items, from the Bank for International Settlements) of the month the period ends in, relative to its 2004 average; a month not published yet uses the latest published month.

- Years Listed: the year of the end of the fiscal period minus the year of the company's IPO date in its profile (FinancialModelingPrep), the count of years a firm has a stock price in Compustat in Hadlock and Pierce. A period before the IPO is NaN.

- The caps are those of Hadlock and Pierce: firms above $4.5 billion of assets or 37 years listed take those values, beyond which size and age hardly add to the prediction.

The size-age index can be interpreted as follows:

- A higher (less negative) index means a more constrained firm: a small, young firm.
- Its lowest value is -4.64, for a firm at both caps ($4.5 billion of 2004 assets and 37 years listed). A new firm with $1 million of 2004 assets has 0, and a smaller one above 0 (its Size is negative). A firm listed 10 years with $100 million of 2004 assets has -2.88.
- As with the other indices, the literature calls the top third of firms constrained and the bottom third unconstrained, each year; the index has no absolute cut-off.

**Also known as:** SA index, Hadlock-Pierce index, HP index, financing constraints.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The size-age index, its Size and Age per ticker and period.

**Notes:**

- The age needs the IPO date of the company profile, which requires an API key; without
it, or for a company whose profile has no IPO date, the Age and the index are NaN (a
warning names the tickers). The IPO date of a company that listed again (after a
spin-off, merger or bankruptcy) is that of the latest listing, so its age counts
from then.
- The total assets are taken in the currency of the statements and deflated with the
US price level, as in Hadlock and Pierce's US sample, so for a company reporting in
another currency the Size is only indicative unless the statements are converted to
US dollars.

References:
- Hadlock, Charles J. and Joshua R. Pierce. "New Evidence on Measuring Financial
Constraints: Moving Beyond the KZ Index." The Review of Financial Studies, Vol. 23, No. 5,
2010, pp. 1909-1940.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "F", "SMP", "ABNB"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2020-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_size_age_index().xs("Size-Age Index", level=1)
```

Which returns:

|      |    2020 |    2021 |    2022 |    2023 |    2024 |    2025 |
|:-----|--------:|--------:|--------:|--------:|--------:|--------:|
| AAPL | -4.6369 | -4.6369 | -4.6369 | -4.6369 | -4.6369 | -4.6369 |
| ABNB | -3.1569 | -3.1969 | -3.2369 | -3.2769 | -3.3169 | -3.3569 |
| F    | -4.6369 | -4.6369 | -4.6369 | -4.6369 | -4.6369 | -4.6369 |
| SMP  | -4.4611 | -4.4875 | -4.4849 | -4.4844 | -4.5306 | -4.5398 |

---

## get_altman_z_score
Calculates the Altman Z-Score, a financial metric used to predict the likelihood of a company going bankrupt. The Altman Z-Score is calculated using several financial ratios, including working capital to total assets, retained earnings to total assets, earnings before interest and taxes (EBIT) to total assets, equity to book value of total liabilities, and (for manufacturers) sales to total assets. Altman estimated four versions, chosen with `model`: the original Z-Score for listed manufacturers, the Z'-Score for private manufacturers, the Z''-Score for non-manufacturers and the Z''-EM score for emerging market companies.

The formula is as follows:

$$
\text{Working Capital to Total Assets} \;(X_{1}) = \frac{\text{Working Capital}}{\text{Total Assets}}
$$

$$
\text{Retained Earnings to Total Assets} \;(X_{2}) = \frac{\text{Retained Earnings}}{\text{Total Assets}}
$$

$$
\text{EBIT to Total Assets} \;(X_{3}) = \frac{\text{EBIT}}{\text{Total Assets}}
$$

$$
\text{Market Value to Total Liabilities} \;(X_{4},\; \text{"original"}) = \frac{\text{Market Value of Equity}}{\text{Total Liabilities}}
$$

$$
\text{Book Value to Total Liabilities} \;(X_{4},\; \text{the other models}) = \frac{\text{Total Shareholder Equity}}{\text{Total Liabilities}}
$$

$$
\text{Sales to Total Assets} \;(X_{5},\; \text{"original"} \;\text{and}\; \text{"private"}) = \frac{\text{Sales}}{\text{Total Assets}}
$$

$$
\text{Original (Altman 1968):}\;\; Z = 1.2 X_{1} + 1.4 X_{2} + 3.3 X_{3} + 0.6 X_{4} + 1.0 X_{5}
$$

$$
\text{Private (Altman 1983):}\;\; Z' = 0.717 X_{1} + 0.847 X_{2} + 3.107 X_{3} + 0.420 X_{4} + 0.998 X_{5}
$$

$$
\text{Non-manufacturing (Altman, Hartzell and Peck 1995):}\;\; Z'' = 6.56 X_{1} + 3.26 X_{2} + 6.72 X_{3} + 1.05 X_{4}
$$

$$
\text{Emerging (Altman 2005):}\;\; Z''_{\text{EM}} = 3.25 + 6.56 X_{1} + 3.26 X_{2} + 6.72 X_{3} + 1.05 X_{4}
$$

The Altman Z-Score can be interpreted with the zones of each model (distress below the lower cut-off, grey zone in between, safe above the upper one):

- Original: distress below 1.81, safe above 2.99.
- Private: distress below 1.23, safe above 2.90.
- Non-manufacturing: distress below 1.10, safe above 2.60.
- Emerging: distress below 4.35, safe above 5.85 (the Z'' zones plus the constant of 3.25, which Altman set so that a score of zero or below matches a bond rated D).

The original Z-Score was estimated on US listed manufacturers, and its thresholds are not meant for banks, insurers or most service companies; the Z''-Score drops the sales term, as asset turnover differs most between industries, so that it fits non-manufacturers, and none of the models is meant for banks or insurers. Share buybacks charged to retained earnings and accumulated losses both lower the retained earnings term, so a company that returns most of its earnings scores lower without being closer to distress, which is why the score is best read as a trend and next to the equity term.

**Also known as:** Altman Z-score, Z'-Score, Z''-Score, Z''-EM, emerging market score, bankruptcy prediction, financial distress score.

**Args:**

- <u>diluted (bool, optional):</u> Whether to use diluted shares outstanding in the market value of equity of
the "original" model. Defaults to True.
- <u>model (str, optional):</u> The model to use: "original" (listed manufacturers, market value of
equity), "private" (Z', book value of equity), "non-manufacturing" (Z'', book value of equity,
no sales term) or "emerging" (Z''-EM, Z'' plus 3.25). Defaults to "original".
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The number of periods the flows are summed over; the balances
are those at the end of the period, the statement-date figures the score was estimated on.
The window counts calendar periods, so a period without a report makes it NaN. Defaults to
None, which is 4 on quarterly data (a trailing twelve months), as the score was estimated
on yearly statements.
- <u>zone (bool, optional):</u> Whether to add a "Zone" row per ticker: "Distress" below the lower cut-off of
the chosen model, "Grey" up to the upper one and "Safe" from it (see above). Not with growth or
standardize. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the Altman Z-Score of the chosen model and its components.

**Notes:**

- The Altman Z-Score is a financial metric used to predict the likelihood of a company going bankrupt.
- The original Z-Score is most effective when used to analyze listed manufacturing companies with
assets of $1 million or more. The Z'-Score uses the book value of equity, so it needs no share
price, and the Z''-Score and Z''-EM score leave out sales to total assets.
- The book value of equity is the Total Shareholder Equity, which excludes minority interests.
- EBIT is the reported Operating Income, as in the EBIT based ratios of the Ratios module.
- The market value of equity is the closing share price at the end of the fiscal period (the
filing day with point_in_time) times the period's weighted average shares, taken at the date
of the balance sheet it is compared with.

References:
- Altman, E. I. (1968). Financial Ratios, Discriminant Analysis and the Prediction of Corporate
Bankruptcy. The Journal of Finance, 23(4), 589-609.
- Altman, E. I. (1983). Corporate Financial Distress: A Complete Guide to Predicting, Avoiding, and
Dealing with Bankruptcy. John Wiley & Sons.
- Altman, E. I. (2000). Predicting Financial Distress of Companies: Revisiting the Z-Score and ZETA
Models. Working paper, New York University.
- Altman, E. I., Hartzell, J. and Peck, M. (1995). Emerging Markets Corporate Bonds: A Scoring System.
Salomon Brothers.
- Altman, E. I. (2005). An Emerging Market Credit Scoring System for Corporate Bonds. Emerging
Markets Review, 6(4), 311-323.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["MCD", "NFLX", "UBER"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_altman_z_score(model="non-manufacturing").xs("Altman Z-Score", level=1)
```

Which returns:

|      |    2021 |    2022 |    2023 |    2024 |   2025 |
|:-----|--------:|--------:|--------:|--------:|-------:|
| MCD  |  5.0735 |  5.1966 |  5.1302 |  5.3948 | 5.1966 |
| NFLX |  2.379  |  2.8961 |  3.3806 |  4.3943 | 5.2949 |
| UBER | -2.0375 | -3.3028 | -1.6181 | -0.0662 | 1.0641 |

---

## get_ohlson_o_score
Calculates the Ohlson O-Score, a financial metric used to predict the likelihood of a company going bankrupt. Unlike the Altman Z-Score, which is built with multiple discriminant analysis, the O-Score's coefficients come from a fitted logistic regression (logit) model. This is why the two models are usually reported side by side rather than one being treated as a replacement for the other: the Z-Score is only meaningful compared against Altman's empirically derived threshold bands, while the O-Score is directly interpretable as a probability of bankruptcy once passed through the logistic transform.

The formula is as follows:

$$
\text{SIZE} = \ln\left(\frac{\text{Total Assets}}{\text{GNP Price-Level Index}}\right)
$$

$$
\text{TLTA} = \frac{\text{Total Liabilities}}{\text{Total Assets}}
$$

$$
\text{WCTA} = \frac{\text{Working Capital}}{\text{Total Assets}}
$$

$$
\text{CLCA} = \frac{\text{Current Liabilities}}{\text{Current Assets}}
$$

$$
\text{OENEG} = 1 \;\text{if Total Liabilities} > \text{Total Assets else}\; 0
$$

$$
\text{NITA} = \frac{\text{Net Income}}{\text{Total Assets}}
$$

$$
\text{FUTL} = \frac{\text{Operating Cash Flow}}{\text{Total Liabilities}}
$$

$$
\text{INTWO} = 1 \;\text{if Net Income was negative for the last two years else}\; 0
$$

$$
\text{CHIN} = \frac{\text{Net Income} \;(t) - \text{Net Income} \;(t-1)}{\left|\text{Net Income} \;(t)\right| + \left|\text{Net Income} \;(t-1)\right|}
$$

$$
\text{O-Score} = - 1.32 - 0.407 \cdot \text{SIZE} + 6.03 \cdot \text{TLTA} - 1.43 \cdot \text{WCTA} + 0.0757 \cdot \text{CLCA} - 1.72 \cdot \text{OENEG} - 2.37 \cdot \text{NITA} - 1.83 \cdot \text{FUTL} + 0.285 \cdot \text{INTWO} - 0.521 \cdot \text{CHIN}
$$

$$
\text{Bankruptcy Probability} = \frac{1}{1 + e^{- \text{O-Score}}}
$$

The Ohlson O-Score can be interpreted as follows:

- Ohlson's (1980) original cutoff is a bankruptcy probability of 0.038 (3.8%), the threshold that minimized the sum of Type I and Type II misclassification errors on his sample. It is deliberately far below the naive 0.50 midpoint because bankruptcy is a rare event. Equivalently, in raw O-Score terms the cutoff sits at ln(0.038 / 0.962), i.e. approximately -3.23.
- A higher probability indicates a higher likelihood of bankruptcy.

**Also known as:** Ohlson O-Score, bankruptcy prediction, financial distress score.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The number of periods the flows are summed over; the balances
are those at the end of the period, the statement-date figures the score was estimated on.
The window counts calendar periods, so a period without a report makes it NaN. Defaults to
None, which is 4 on quarterly data (a trailing twelve months), as the score was estimated
on yearly statements.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the Ohlson O-Score, its bankruptcy probability, and its
components.

**Notes:**

- The GNP Price-Level Index is the US implicit price deflator of the gross national
product (U.S. Bureau of Economic Analysis, NIPA table 1.7.9) rebased to 1968 = 100, as in
Ohlson (1980), of the year each period falls in; a year not published yet uses the latest
published one. It is the US price level for every company, as in Ohlson's US sample, and the
total assets are in the units of the statements, so for companies reporting in another
currency the SIZE term (and the 0.038 cutoff) is only indicative.
- Ohlson's original FUTL term uses "Funds from Operations", an accounting-flow concept that
predates standardized cash flow statements. This implementation approximates Funds from
Operations with Operating Cash Flow, the standard simplification used in modern
reproductions of the O-Score.
- The Beneish M-Score, Altman Z-Score, Piotroski F-Score and Ohlson O-Score are natural
companions, using the same normalized financial statements as their input.
- As with the other bankruptcy and distress models, this is a probabilistic, not a
definitive, indicator and should be combined with further fundamental analysis.

References:
- Ohlson, James A. "Financial Ratios and the Probabilistic Prediction of Bankruptcy." Journal of
Accounting Research, Vol. 18, No. 1, 1980, pp. 109-131.

Note that the first year is NaN because the Change in Net Income and Negative Income
Indicator components require a prior year to compare against. On quarterly data both
compare with the same quarter a year earlier.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["CCL", "RCL", "NCLH"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_ohlson_o_score().xs("Ohlson O-Score", level=1)
```

Which returns:

|      |    2021 |    2022 |    2023 |    2024 |    2025 |
|:-----|--------:|--------:|--------:|--------:|--------:|
| CCL  | -3.1546 | -2.808  | -3.5648 | -4.1767 | -4.1103 |
| NCLH | -1.8134 | -1.4699 | -2.4151 | -2.6099 | -2.3287 |
| RCL  | -2.3939 | -2.4157 | -3.5705 | -3.7051 | -4.0142 |

---

## get_zmijewski_score
Calculates the Zmijewski Score, a financial metric used to predict the likelihood of a company going bankrupt. It is a simpler, three-variable model compared to both the Altman Z-Score and the Ohlson O-Score, and is commonly used as a robustness check when those two models disagree, since it is estimated on a different sample and with a different statistical technique (a probit model rather than discriminant analysis or logistic regression).

The formula is as follows:

$$
\text{Net Income to Total Assets} = \frac{\text{Net Income}}{\text{Total Assets}}
$$

$$
\text{Total Liabilities to Total Assets} = \frac{\text{Total Liabilities}}{\text{Total Assets}}
$$

$$
\text{Current Assets to Current Liabilities} = \frac{\text{Current Assets}}{\text{Current Liabilities}}
$$

$$
X = - 4.336 - 4.513 \cdot \text{Net Income to Total Assets} + 5.679 \cdot \text{Total Liabilities to Total Assets} - 0.004 \cdot \text{Current Assets to Current Liabilities}
$$

$$
\text{Bankruptcy Probability} = \Phi(X),\;\; \text{the standard normal cumulative distribution function}
$$

The Zmijewski Score can be interpreted as follows:

- A higher X (and therefore a higher bankruptcy probability) indicates a higher likelihood of financial distress.

**Also known as:** Zmijewski Score, ZFC score, bankruptcy prediction, financial distress score.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The number of periods the flows are summed over; the balances
are those at the end of the period, the statement-date figures the score was estimated on.
The window counts calendar periods, so a period without a report makes it NaN. Defaults to
None, which is 4 on quarterly data (a trailing twelve months), as the score was estimated
on yearly statements.
- <u>zone (bool, optional):</u> Whether to add a "Zone" row per ticker: "Distress" from a score of 0, a
bankruptcy probability of 0.5 and up (Zmijewski's classification), "Safe" below it. Not with
growth or standardize. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the Zmijewski Score, its bankruptcy probability, and its
components.

**Notes:**

- Unlike the Ohlson O-Score, which uses a logistic (sigmoid) link to convert its score into
a probability, the Zmijewski Score uses a probit link (the standard normal CDF). Applying a
logistic transform to the Zmijewski Score instead would produce an incorrect probability.
- As with the Altman Z-Score, Piotroski F-Score, Beneish M-Score and Ohlson O-Score, this is
a probabilistic, not a definitive, indicator and should be combined with further fundamental
analysis.

References:
- Zmijewski, Mark E. "Methodological Issues Related to the Estimation of Financial Distress
Prediction Models." Journal of Accounting Research, Vol. 22, 1984, pp. 59-82.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["DAL", "UAL", "AAL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_zmijewski_score().xs("Zmijewski Score", level=1)
```

Which returns:

|     |   2021 |   2022 |   2023 |    2024 |    2025 |
|:----|-------:|-------:|-------:|--------:|--------:|
| AAL | 2.1018 | 1.8402 | 1.7502 |  1.6446 |  1.6755 |
| DAL | 1.017  | 0.7425 | 0.2026 | -0.0177 | -0.3885 |
| UAL | 1.0493 | 0.7082 | 0.4288 |  0.1763 |  0.0073 |

---

## get_springate_score
Calculates the Springate Score, a financial metric used to predict the likelihood of a company going bankrupt. It follows the same multiple discriminant analysis methodology as the Altman Z-Score, but was calibrated on a smaller, Canadian-firm sample using four financial ratios instead of five.

The formula is as follows:

$$
\text{Working Capital to Total Assets} = \frac{\text{Working Capital}}{\text{Total Assets}}
$$

$$
\text{EBIT to Total Assets} = \frac{\text{EBIT}}{\text{Total Assets}}
$$

$$
\text{EBT to Current Liabilities} = \frac{\text{Earnings Before Taxes}}{\text{Total Current Liabilities}}
$$

$$
\text{Sales to Total Assets} = \frac{\text{Sales}}{\text{Total Assets}}
$$

$$
\text{Springate Score} = 1.03 \cdot \text{Working Capital to Total Assets} + 3.07 \cdot \text{EBIT to Total Assets} + 0.66 \cdot \text{EBT to Current Liabilities} + 0.4 \cdot \text{Sales to Total Assets}
$$

The Springate Score can be interpreted as follows:

- A Springate Score of less than 0.862 indicates a high likelihood of bankruptcy.
- A Springate Score of greater than 0.862 indicates a low likelihood of bankruptcy.

**Also known as:** Springate Score, S-Score, bankruptcy prediction, financial distress score.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The number of periods the flows are summed over; the balances
are those at the end of the period, the statement-date figures the score was estimated on.
The window counts calendar periods, so a period without a report makes it NaN. Defaults to
None, which is 4 on quarterly data (a trailing twelve months), as the score was estimated
on yearly statements.
- <u>zone (bool, optional):</u> Whether to add a "Zone" row per ticker: "Distress" below Springate's cut-off
of 0.862, "Safe" from it. Not with growth or standardize. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the Springate Score and its components.

**Notes:**

- As with the Altman Z-Score, Piotroski F-Score, Beneish M-Score, Ohlson O-Score and
Zmijewski Score, this is a probabilistic, not a definitive, indicator and should be
combined with further fundamental analysis.
- EBIT is the reported Operating Income, as in the Altman Z-Score calculation elsewhere
in this module.

References:
- Springate, Gordon L.V. "Predicting the Possibility of Failure in a Canadian Firm."
Unpublished M.B.A. Research Project, Simon Fraser University, 1978.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["M", "KSS", "GAP"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_springate_score().xs("Springate Score", level=1)
```

Which returns:

|     |   2021 |   2022 |   2023 |   2024 |
|:----|-------:|-------:|-------:|-------:|
| GAP | 0.8575 | 0.6249 | 0.9346 | 1.1942 |
| KSS | 1.2226 | 0.5896 | 0.809  | 0.6373 |
| M   | 1.2937 | 1.1721 | 0.7495 | 0.9653 |

---

## get_grover_score
Calculates the Grover Score, a financial metric used to predict the likelihood of a company going bankrupt. It was developed by re-estimating the coefficients of a reduced-form Altman Z-Score and adding a Return on Assets term, using a sample that paired each of Altman's original bankrupt firms with a matched non-bankrupt firm from the same industry and year.

The formula is as follows:

$$
\text{Working Capital to Total Assets} = \frac{\text{Working Capital}}{\text{Total Assets}}
$$

$$
\text{EBIT to Total Assets} = \frac{\text{EBIT}}{\text{Total Assets}}
$$

$$
\text{Return on Assets} = \frac{\text{Net Income}}{\text{Total Assets}}
$$

$$
\text{Grover Score} = 1.65 \cdot \text{Working Capital to Total Assets} + 3.404 \cdot \text{EBIT to Total Assets} - 0.016 \cdot \text{Return on Assets} + 0.057
$$

The Grover Score can be interpreted as follows:

- A Grover Score of -0.02 or lower indicates a high likelihood of bankruptcy.
- A Grover Score of 0.01 or higher indicates a low likelihood of bankruptcy (per some secondary sources), leaving a gray area in between the two thresholds.

**Also known as:** Grover Score, G-Score, bankruptcy prediction, financial distress score.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The number of periods the flows are summed over; the balances
are those at the end of the period, the statement-date figures the score was estimated on.
The window counts calendar periods, so a period without a report makes it NaN. Defaults to
None, which is 4 on quarterly data (a trailing twelve months), as the score was estimated
on yearly statements.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the Grover Score and its components.

**Notes:**

- As with the Altman Z-Score, Springate Score, Ohlson O-Score and Zmijewski Score,
this is a probabilistic, not a definitive, indicator and should be combined with
further fundamental analysis.
- EBIT is the reported Operating Income, as in the Altman Z-Score calculation elsewhere
in this module. Return on
Assets uses the point-in-time Total Assets balance (not averaged), matching the
original Grover (2001) specification.

References:
- Grover, Jeffrey S. "Validating the Grover Bankruptcy Model." Doctoral dissertation,
University of North Texas, 2003.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["F", "GM", "STLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_grover_score().xs("Grover Score", level=1)
```

Which returns:

|      |   2021 |   2022 |   2023 |   2024 |    2025 |
|:-----|-------:|-------:|-------:|-------:|--------:|
| F    | 0.2398 | 0.2688 | 0.2442 | 0.2194 |  0.1363 |
| GM   | 0.2379 | 0.2474 | 0.2157 | 0.2846 |  0.1825 |
| STLA | 0.477  | 0.5941 | 0.5796 | 0.2001 | -0.3018 |

---

## get_fulmer_h_score
Calculates the Fulmer H-Score, a financial metric used to predict the likelihood of a company going bankrupt. Unlike the Altman Z-Score, which was built on relatively large, listed manufacturing companies, the Fulmer H-Score was calibrated on a matched-pair sample of small, failed and non-failed U.S. companies, using nine financial ratios selected via step-wise multiple discriminant analysis.

The formula is as follows:

$$
V_{1} = \frac{\text{Retained Earnings}}{\text{Total Assets}}
$$

$$
V_{2} = \frac{\text{Revenue}}{\text{Total Assets}}
$$

$$
V_{3} = \frac{\text{Income Before Tax} \;(\text{EBT})}{\text{Total Equity}}
$$

$$
V_{4} = \frac{\text{Operating Cash Flow}}{\text{Total Liabilities}}
$$

$$
V_{5} = \frac{\text{Total Debt}}{\text{Total Assets}}
$$

$$
V_{6} = \frac{\text{Total Current Liabilities}}{\text{Total Assets}}
$$

$$
V_{7} = \ln(\text{Total Assets} - \text{Goodwill and Intangible Assets})
$$

$$
V_{8} = \frac{\text{Total Current Assets} - \text{Total Current Liabilities}}{\text{Total Liabilities}}
$$

$$
V_{9} = \ln\left(\frac{\text{EBIT}}{\text{Interest Expense}}\right),\;\; \text{with EBIT the reported Operating Income}
$$

$$
\text{H-Score} = 5.528 \cdot V_{1} + 0.212 \cdot V_{2} + 0.073 \cdot V_{3} + 1.270 \cdot V_{4} - 0.120 \cdot V_{5} + 2.335 \cdot V_{6} + 0.575 \cdot V_{7} + 1.083 \cdot V_{8} + 0.894 \cdot V_{9} - 6.075
$$

With `trailing`, the flows are summed over the trailing periods and the balance sheet items are those at the end of the period, the statement-date balances the score was estimated on.

The Fulmer H-Score can be interpreted as follows:

- An H-Score of less than 0 predicts failure.
- An H-Score of greater than 0 predicts non-failure.

**Also known as:** Fulmer H-Score, H factor, bankruptcy prediction, financial distress score.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The number of periods the flows are summed over; the balances
are those at the end of the period, the statement-date figures the score was estimated on.
The window counts calendar periods, so a period without a report makes it NaN. Defaults to
None, which is 4 on quarterly data (a trailing twelve months), as the score was estimated
on yearly statements.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the Fulmer H-Score and its components.

**Notes:**

- Because V7 and V9 involve a natural logarithm, periods where Tangible Total Assets
is zero or negative, where EBIT and Interest Expense do not share the same sign, or
where the company reports no Interest Expense at all, will produce NaN and therefore
no H-Score for that period. This is a structural limitation of the log-linear Fulmer
specification, not a bug — the same kind of limitation documented for the Graham
Number elsewhere in this toolkit.
- Because V7 uses an un-normalized dollar figure, the H-Score is sensitive to the
absolute scale of a company's total assets; treat results for very large companies
(far outside the small-firm sample the model was calibrated on) with additional
caution.
- EBIT is the reported Operating Income, as in the Altman Z-Score calculation elsewhere
in this module.
- As with the Altman Z-Score, Springate Score and Grover Score, this is a
probabilistic, not a definitive, indicator and should be combined with further
fundamental analysis.

References:
- Fulmer, John G., James E. Moon, Thomas A. Gavin, and Michael J. Erwin. "A
Bankruptcy Classification Model for Small Firms." Journal of Commercial Bank
Lending, Vol. 66, No. 11, 1984, pp. 25-37.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["DIS", "FOXA", "CMCSA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_fulmer_h_score().xs("Fulmer H-Score", level=1)
```

Which returns:

|       |    2021 |    2022 |    2023 |    2024 |    2025 |
|:------|--------:|--------:|--------:|--------:|--------:|
| CMCSA | 11.6317 | 11.6248 | 11.7028 | 11.8104 | 11.9431 |
| DIS   | 10.8945 | 11.5241 | 12.0105 | 12.4096 | 12.7101 |
| FOXA  | 10.9776 | 11.0388 | 10.9996 | 11.0274 | 11.8441 |

---

## get_taffler_z_score
Calculates the Taffler z-score, a discriminant model of financial distress estimated on UK listed industrial companies (Taffler, 1983). It combines profitability, working capital, financial risk and liquidity, and Agarwal and Taffler (2007) showed that it kept its predictive ability over 25 years of UK data. A negative score places a company in the at-risk region.

The formula is as follows:

$$
\text{Profit Before Tax to Current Liabilities} \;(X_{1}) = \frac{\text{Income Before Tax}}{\text{Total Current Liabilities}}
$$

$$
\text{Current Assets to Total Liabilities} \;(X_{2}) = \frac{\text{Total Current Assets}}{\text{Total Liabilities}}
$$

$$
\text{Current Liabilities to Total Assets} \;(X_{3}) = \frac{\text{Total Current Liabilities}}{\text{Total Assets}}
$$

$$
\text{Daily Operating Expenses} = \frac{\text{Revenue} - \text{Income Before Tax} - \text{Depreciation and Amortization}}{\text{Days}}
$$

$$
\text{No-Credit Interval} \;(X_{4}) = \frac{\text{Total Current Assets} - \text{Inventory} - \text{Total Current Liabilities}}{\text{Daily Operating Expenses}}
$$

$$
\text{Taffler z-score} = 3.20 + 12.18 X_{1} + 2.50 X_{2} - 10.68 X_{3} + 0.029 X_{4}
$$

The Taffler z-score can be interpreted as follows:

- A score below zero indicates a financial profile like that of companies that failed (at risk).
- A score above zero indicates a solvent profile; the higher, the safer.

**Also known as:** Taffler Z-Score, UK z-score, bankruptcy prediction, financial distress score.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation: flows are
summed over it and balances are those at the end of the period, the statement-date
balances of the paper. The window counts calendar periods, so a period without a
report makes it NaN. Defaults to None, which is 4 on quarterly data (a trailing twelve
months), as the score was estimated on yearly statements.
- <u>zone (bool, optional):</u> Whether to add a "Zone" row per ticker: "Distress" below zero (Taffler's at
risk profile), "Safe" from it. Not with growth or standardize. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the Taffler z-score and its components.

**Notes:**

- The No-Credit Interval is in days. The days are those the flows cover: 365 a year, a quarter of
that for a quarter, times the number of trailing periods.
- Quick assets are the Total Current Assets less Inventory, and the Depreciation and Amortization
stands in for the depreciation of the paper's daily operating expenses.
- Agarwal and Taffler (2007, Table 1) attribute 53% of the discriminating power to X1, 13% to X2, 18%
to X3 and 16% to X4. The coefficients were estimated on UK industrial companies, so the model is not
meant for financial companies and is best read as a trend for companies elsewhere.
- As with the Altman Z-Score and the other scores in this module, this is a probabilistic, not a
definitive, indicator and should be combined with further fundamental analysis.

References:
- Taffler, R. J. (1983). The Assessment of Company Solvency and Performance Using a Statistical
Model. Accounting and Business Research, 13(52), 295-308.
- Agarwal, V. and Taffler, R. J. (2007). Twenty-Five Years of the Taffler z-Score Model: Does It
Really Have Predictive Ability? Accounting and Business Research, 37(4), 285-300.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["M", "KSS", "GAP"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2020-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_taffler_z_score().xs("Taffler Z-Score", level=1)
```

Which returns:

|     |     2020 |   2021 |    2022 |   2023 |   2024 |
|:----|---------:|-------:|--------:|-------:|-------:|
| GAP |  -2.1624 | 0.7496 |  0.1718 | 3.1604 | 5.9418 |
| KSS |   0.4845 | 5.7852 | -0.0302 | 2.4432 | 0.1935 |
| M   | -11.3244 | 3.8969 |  3.4676 | 0.2883 | 2.4301 |

---

## get_merton_distance_to_default
Calculate the distance to default and probability of default with the Merton (1974) structural credit model. Equity is seen as a call option on the company's assets with its debt as strike price: shareholders receive what is left after the debt is repaid. The market value and volatility of the assets, which cannot be observed, are solved from the market value and volatility of the equity:

$$
E = V N(d_{1}) - D e^{- rT} N(d_{2})
$$

$$
\sigma_{E} E = N(d_{1}) \sigma_{V} V
$$

$$
\text{Distance to Default} = \frac{\ln\left(\frac{V}{D}\right) + \left(r - \frac{\sigma_{V}^{2}}{2}\right) T}{\sigma_{V} \sqrt{T}}
$$

$$
\text{Probability of Default} = N(- \text{Distance to Default})
$$

$$
\text{Debt Value} = V - E
$$

$$
\text{Credit Spread} = - \frac{\ln\left(\frac{\text{Debt Value}}{D}\right)}{T} - r
$$

where E is the market capitalization, $$\sigma_{E}$$ the volatility of the share price over the year before, D the default point (short-term debt plus half of the long-term debt, the KMV convention), r the risk free rate and T the time horizon. The distance to default is the number of standard deviations the asset value is above the default point; it reacts to the share price immediately, long before a rating changes. The debt is a risk-free bond with face value D less a put on the assets, so its value is what the assets are worth beyond the equity, and the credit spread is the yield it pays over the risk free rate, both continuously compounded.

The market capitalization, the equity volatility and the risk free rate are measured on the last trading day of each fiscal period (the filing day with point_in_time), the date of the balance sheet the default point comes from.

The risk free rate is the Toolkit's (the 10-year Treasury yield unless set otherwise with `risk_free_rate`) on that day, converted from its semi-annual bond-equivalent quote to continuous compounding, where Vassalou and Xing (2004) and Bharath and Shumway (2008) use the one-year rate for a one-year horizon; the difference moves the distance to default only slightly.

For more information, see the following papers:

- Merton, R.C. (1974). "On the Pricing of Corporate Debt: The Risk Structure of Interest Rates." The Journal of Finance, 29(2), 449-470.
- Crosbie, P. and Bohn, J. (2003). "Modeling Default Risk." Moody's KMV.
- Vassalou, M. and Xing, Y. (2004). "Default Risk in Equity Returns." The Journal of Finance, 59(2), 831-868.
- Bharath, S.T. and Shumway, T. (2008). "Forecasting Default with the Merton Distance to Default Model." The Review of Financial Studies, 21(3), 1339-1369.

The debt value and credit spread are referenced against FinancePy's MertonFirm.

**Also known as:** KMV model, structural credit model, expected default frequency, Merton credit spread.

**Args:**

- <u>time_horizon (float, optional):</u> The horizon in years over which default is
measured. Defaults to 1.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker and period the Equity Value, Equity Volatility, Default
Point, Asset Value, Asset Volatility, Debt Value, Credit Spread (a decimal),
Distance to Default and Probability of Default (a decimal).

**Notes:**

- The probability is the model's risk-neutral probability; it ranks companies by
credit risk well but tends to understate the actual default rate of safe ones.
- Financial companies, whose debt is their raw material, are outside the model's
intended use.
- The credit spread of a one-year horizon is close to zero for all but the riskiest
companies, well below the spreads their bonds trade at, a known shortfall of the
model (Jones, Mason and Rosenfeld, 1984, The Journal of Finance, 39(3)).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["F", "AAPL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_merton_distance_to_default().loc["F"]
```

Which returns:

|                        |        2021 |        2022 |        2023 |        2024 |        2025 |
|:-----------------------|------------:|------------:|------------:|------------:|------------:|
| Equity Value           | 8.37862e+10 | 4.66828e+10 | 4.92598e+10 | 3.98079e+10 | 5.22045e+10 |
| Equity Volatility      | 0.4163      | 0.4912      | 0.3551      | 0.3601      | 0.3313      |
| Default Point          | 9.3892e+10  | 9.45665e+10 | 9.945e+10   | 1.07294e+11 | 1.1133e+11  |
| Asset Value            | 1.76273e+11 | 1.37643e+11 | 1.44969e+11 | 1.42359e+11 | 1.59043e+11 |
| Asset Volatility       | 0.1979      | 0.1675      | 0.1207      | 0.1007      | 0.1088      |
| Debt Value             | 9.24864e+10 | 9.09604e+10 | 9.57091e+10 | 1.02551e+11 | 1.06838e+11 |
| Credit Spread          | 0           | 0.0005      | 0           | 0           | 0           |
| Distance to Default    | 3.1593      | 2.387       | 3.3801      | 3.2055      | 3.6038      |
| Probability of Default | 0.0008      | 0.0085      | 0.0004      | 0.0007      | 0.0002      |

---

## get_campbell_hilscher_szilagyi_score
Calculate the probability of failure of Campbell, Hilscher and Szilagyi (2008), a logit model that combines accounting figures with market data to predict failure: a bankruptcy filing, a delisting or a D (default) rating. It measures profitability and leverage against the market value of the assets rather than the book value, and adds the excess return of the shares, their volatility, the company's size, its cash, its market-to-book ratio and its share price. In the paper it predicts failure better than Shumway's (2001) model and than the Merton distance to default.

The model is the 12-month-ahead logit of Table IV, column (3), of the paper:

$$
\text{LPFD} = - 9.164 - 20.264 \;\text{NIMTAAVG} + 1.416 \;\text{TLMTA} - 7.129 \;\text{EXRETAVG} + 1.411 \;\text{SIGMA} - 0.045 \;\text{RSIZE} - 2.132 \;\text{CASHMTA} + 0.075 \;\text{MB} - 0.058 \;\text{PRICE}
$$

$$
\text{Failure Probability} = \frac{1}{1 + e^{- \text{LPFD}}}
$$

with:

$$
\text{MTA} = \text{Market Value of Equity} + \text{Total Liabilities} \;(\text{the market value of total assets})
$$

$$
\text{NIMTA} = \frac{\text{Quarterly Net Income}}{\text{MTA}},\;\; \text{and NIMTAAVG its average over four quarters with weights that halve every quarter:}\;\; \frac{1 - \phi^{3}}{1 - \phi^{12}} \cdot (\operatorname{NIMTA}(t) + \phi^{3} \;\operatorname{NIMTA}(t-1) + \phi^{6} \;\operatorname{NIMTA}(t-2) + \phi^{9} \;\operatorname{NIMTA}(t-3)),\;\; \phi = 2^{- \frac{1}{3}}
$$

$$
\text{EXRET} = \ln(1 + \text{Return}) - \ln(1 + \text{S\&P 500 Return}) \;\text{per month},\;\; \text{and EXRETAVG its average over twelve months:}\;\; \frac{1 - \phi}{1 - \phi^{12}} \cdot (\operatorname{EXRET}(t) + \phi \;\text{EXRET}(t-1) + \ldots + \phi^{11} \;\operatorname{EXRET}(t-11))
$$

$$
\text{TLMTA} = \frac{\text{Total Liabilities}}{\text{MTA}}
$$

$$
\text{CASHMTA} = \frac{\text{Cash and Short Term Investments}}{\text{MTA}}
$$

$$
\text{MB} = \frac{\text{Market Value of Equity}}{\text{Adjusted Book Equity}},\;\; \text{where}\;\; \text{Adjusted Book Equity} = \text{Book Equity} + 0.1 \cdot (\text{Market Value of Equity} - \text{Book Equity}) \;(\text{Cohen, Polk and Vuolteenaho},\; 2003),\;\; \text{and a value that is still not positive becomes 1}
$$

$$
\text{SIGMA} = \sqrt{\frac{252}{N - 1} \cdot \sum r^{2}},\;\; \text{the annualized volatility around zero of the } N \text{ daily returns of the three months before, NaN with fewer than five non-zero returns}
$$

$$
\text{RSIZE} = \ln\left(\frac{\text{Market Value of Equity}}{\text{Total Market Value of the S\&P}\; 500}\right)
$$

$$
\text{PRICE} = \ln(\min(\text{Share Price},\; 15))
$$

Book Equity is Total Shareholder Equity plus Deferred Tax Liabilities minus Preferred Stock (Davis, Fama and French, 2000), the latter two counted as zero when not reported. The market value of equity is the closing price times the diluted weighted average shares, the returns are total returns (Adj Close) against the S&P 500 total return index (^SP500TR), and every market variable is measured on the day each period's figures apply from (the fiscal period end, or the filing day with point_in_time): no market data after that day is used.

The probability is that of failing in the month 12 months ahead, given that the company survives until then. It is a monthly probability, not the probability of failing within a year. For comparison, between 0.4% and 3.7% of the companies in the paper's sample failed per year from 1983 to 2003 (Table I).

**Also known as:** CHS model, failure probability, distress risk, default probability, LPFD.

**Args:**

- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker and period the eight variables as they enter the model,
the CHS Score (LPFD) and the Failure Probability (a decimal).

**Notes:**

- Winsorization: the paper winsorizes every variable at the 5th and 95th
percentiles of the monthly cross-section of all US companies, which a
calculation per company cannot repeat. Each variable (NIMTA per quarter, EXRET
per month) is clipped instead to the range the winsorized variables span in
the paper's full - <u>sample (Table II, minimum and maximum):</u> NIMTA -0.069 to 0.028,
TLMTA 0.036 to 0.923, EXRET -0.243 to 0.218, RSIZE -13.568 to -6.773, SIGMA
0.153 to 1.353, CASHMTA 0.002 to 0.358, MB 0.358 to 6.471 and PRICE -0.065 to
2.708. The variables are shown clipped, as they enter the score; a company
larger than about 0.1% of the S&P 500 has the largest RSIZE the paper used.
- RSIZE: the total market value of the S&P 500 is the sum of the latest market
capitalizations of its current companies (FinancialModelingPrep, each company
once), scaled back to each date with the S&P 500 price index (^GSPC). This
holds the companies and share counts of the latest date: changes in the index
membership and share counts that S&P offsets with its divisor are not
followed, and the index weighs float-adjusted shares while the total counts all
shares. As RSIZE enters with a coefficient of -0.045, an error of 5% in the
total moves the score by about 0.002. Without an API key that has access to
the constituents, RSIZE and the probability are NaN.
- On yearly statements NIMTAAVG is a quarter of the yearly net income over the
market value of total assets at the year end, equal weights for the four
quarters instead of weights that halve every quarter; on quarterly statements
it is calculated as in the paper. A missing quarter or month leaves the average
NaN where the paper fills it with the cross-sectional mean.
- PRICE uses the split-adjusted closing price, so for a company that split its
shares (or reverse-split them) after the period, the price differs from the
price traded then by the split ratio, which matters only below $15.
- The paper lags the accounting figures by two months so they are known; set
point_in_time on the Toolkit to measure on the filing day instead of the
fiscal period end.
- The coefficients were estimated on US companies from 1963 to 2003 with the S&P
500 as the market. For a company listed in another currency, its market value
is compared with the dollar total of the S&P 500, which moves RSIZE by the log
of the exchange rate (about 0.004 on the score for the euro).

References:
- Campbell, J.Y., Hilscher, J. and Szilagyi, J. (2008). "In Search of Distress Risk."
The Journal of Finance, 63(6), 2899-2939.
- Cohen, R.B., Polk, C. and Vuolteenaho, T. (2003). "The Value Spread." The Journal
of Finance, 58(2), 609-641.
- Davis, J.L., Fama, E.F. and French, K.R. (2000). "Characteristics, Covariances, and
Average Returns: 1929 to 1997." The Journal of Finance, 55(1), 389-406.
- Shumway, T. (2001). "Forecasting Bankruptcy More Accurately: A Simple Hazard
Model." The Journal of Business, 74(1), 101-124.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["F", "AAPL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_campbell_hilscher_szilagyi_score().loc["F"]
```

Which returns:

|                                        |    2021 |    2022 |    2023 |    2024 |    2025 |
|:---------------------------------------|--------:|--------:|--------:|--------:|--------:|
| Net Income to Market Assets (NIMTAAVG) |  0.0153 | -0.0019 |  0.0039 |  0.0052 | -0.0067 |
| Liabilities to Market Assets (TLMTA)   |  0.7133 |  0.82   |  0.8239 |  0.8579 |  0.8291 |
| Excess Return (EXRETAVG)               |  0.0573 | -0.0308 | -0.007  | -0.037  |  0.015  |
| Volatility (SIGMA)                     |  0.4477 |  0.4187 |  0.4069 |  0.3133 |  0.3746 |
| Relative Size (RSIZE)                  | -6.773  | -6.773  | -6.7827 | -7.2053 | -7.0859 |
| Cash to Market Assets (CASHMTA)        |  0.1697 |  0.1699 |  0.1436 |  0.1369 |  0.126  |
| Market to Book (MB)                    |  1.567  |  1.0379 |  1.1113 |  0.8788 |  1.3456 |
| Log Price (PRICE)                      |  2.708  |  2.4536 |  2.5006 |  2.2925 |  2.5741 |
| CHS Score                              | -8.3383 | -7.2758 | -7.5146 | -7.3842 | -7.4308 |
| Failure Probability                    |  0.0002 |  0.0007 |  0.0005 |  0.0006 |  0.0006 |

---

## get_shumway_score
Calculate the bankruptcy probability of Shumway's (2001) hazard model, which combines two accounting ratios of Zmijewski's model with three market variables: the company's size relative to the market, its excess return over the past year and the volatility of its returns that the market does not explain. Shumway estimated it as a discrete-time hazard model (a logit on every firm year), which uses every year a company is observed rather than one per company, and found that the market variables predict bankruptcy better than most accounting ratios.

The model is Table 6 of the paper, panel B (model="combined") or panel A (model="market"):

$$
\text{Combined:}\;\; H = - 13.303 - \frac{1.982 \;\text{NI}}{\text{TA}} + \frac{3.593 \;\text{TL}}{\text{TA}} - 0.467 \;\text{RELSIZE} - 1.809 \;\text{EXRET} + 5.791 \;\text{SIGMA}
$$

$$
\text{Market:}\;\; H = - 12.027 - 0.503 \;\text{RELSIZE} - 2.072 \;\text{EXRET} + 9.834 \;\text{SIGMA}
$$

$$
\text{Bankruptcy Probability} = \frac{e^{H}}{1 + e^{H}}
$$

with:

$$
\frac{\text{NI}}{\text{TA}} = \frac{\text{Net Income}}{\text{Total Assets}}
$$

$$
\frac{\text{TL}}{\text{TA}} = \frac{\text{Total Liabilities}}{\text{Total Assets}}
$$

$$
\text{RELSIZE} = \ln\left(\frac{\text{Market Value of Equity}}{\text{Total Market Value of the S\&P}\; 500}\right)
$$

$$
\text{EXRET} = \text{the return of the shares over the past twelve months} \;(\text{cumulated from the monthly returns}) \;\text{minus that of the S\&P 500 total return index}
$$

$$
\text{SIGMA} = \text{the standard deviation of the residuals of a regression of the twelve monthly returns of the shares on those of the S\&P}\; 500 \left(\text{the standard error of the regression},\; \sqrt{\frac{\sum e^{2}}{12 - 2}}\right),\;\; \text{a monthly figure}
$$

The probability is that of a bankruptcy filing in the year after the period, the statements and market data being known at its end. For comparison, 300 of the 39,745 firm years in Shumway's sample ended in bankruptcy (0.75%).

For more information, see the following sources:

- Shumway, T. (2001). "Forecasting Bankruptcy More Accurately: A Simple Hazard Model." The Journal of Business, 74(1), 101-124.
- Zmijewski, M. E. (1984). "Methodological Issues Related to the Estimation of Financial Distress Prediction Models." Journal of Accounting Research, 22, 59-82.

**Also known as:** Shumway hazard model, hazard model bankruptcy probability, Shumway score.

**Args:**

- <u>model (str, optional):</u> "combined" for the market and accounting variables (Table 6,
panel B) or "market" for the market variables only (panel A), which also works
for companies without statements. Defaults to "combined".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker and period the variables as they enter the model (NI/TA and
TL/TA only for the combined model), the Shumway Score (H) and the Bankruptcy
Probability (a decimal).

**Notes:**

- Truncation: Shumway truncates every variable at the 1st and 99th percentiles of his
sample, which a calculation per company cannot repeat. Each variable is clipped instead
to the range it spans in the paper's sample after - <u>truncation (Table 1, minimum and
maximum):</u> NI/TA -0.329 to 0.231, TL/TA 0.090 to 1.028, RELSIZE -13.616 to -6.115,
EXRET -0.817 to 2.181 and SIGMA 0.030 to 0.325. A company larger than about 0.2% of the
S&P 500 has the largest RELSIZE the paper used.
- The market: Shumway compares with all NYSE and AMEX companies (the value-weighted CRSP
index and their total market value); this uses the S&P 500, its total return index
(^SP500TR) and the total market value of its companies (see
`get_campbell_hilscher_szilagyi_score`), which holds most of the US market value. As
RELSIZE enters with -0.467, a total market value 25% too low moves the score by about
-0.1. Without an API key that has access to the constituents, RELSIZE and the
probability are NaN.
- The market value of equity is the closing price times the diluted weighted average
shares, the returns are total returns (Adj Close), and every market variable is
measured up to the day each period's figures apply - <u>from (the fiscal period end, or the
filing day with point_in_time):</u> no later data is used. Shumway lags the statements by
at least six months so they are known; set point_in_time on the Toolkit to measure on
the filing day instead.
- On quarterly statements the net income is that of the trailing twelve months, as the
model was estimated on yearly figures.
- A month without a price leaves EXRET and SIGMA NaN, where Shumway substitutes the
market return for a missing month.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["F", "AAPL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_shumway_score().loc["F"]
```

Which returns:

|                                     |    2021 |    2022 |    2023 |    2024 |    2025 |
|:------------------------------------|--------:|--------:|--------:|--------:|--------:|
| Net Income to Total Assets (NI/TA)  |  0.0698 | -0.0077 |  0.0159 |  0.0206 | -0.0283 |
| Liabilities to Total Assets (TL/TA) |  0.8108 |  0.8313 |  0.8434 |  0.8427 |  0.8756 |
| Relative Size (RELSIZE)             | -6.2444 | -6.6131 | -6.7763 | -7.1989 | -7.0795 |
| Excess Return (EXRET)               |  1.0878 | -0.2407 | -0.1047 | -0.3812 |  0.2447 |
| Idiosyncratic Volatility (SIGMA)    |  0.111  |  0.0861 |  0.1102 |  0.0533 |  0.036  |
| Shumway Score                       | -8.9366 | -6.2785 | -6.3123 | -5.9556 | -7.0292 |
| Bankruptcy Probability              |  0.0001 |  0.0019 |  0.0018 |  0.0026 |  0.0009 |

---

## get_synthetic_credit_rating
Calculate a synthetic credit rating and the cost of debt that comes with it, from the interest coverage ratio (EBIT divided by interest expense), following Aswath Damodaran. Most companies have no traded bonds or rating of their own; the coverage ratio is the measure that explains ratings best, so it is mapped to the rating that companies with a similar ratio have, and to that rating's default spread over the risk free rate:

- Interest Coverage Ratio = EBIT / Interest Expense
- Rating and Default Spread from Damodaran's synthetic rating table
- Pre-tax Cost of Debt = Risk Free Rate + Default Spread

The table, with this year's default spreads, is read from Damodaran's website. Large and small companies use different coverage ranges, as smaller companies need a higher coverage for the same rating.

For more information, see the following book and data:

- Damodaran, A. (2012). "Investment Valuation." Wiley, 3rd edition, chapter 8.
- Damodaran, A. "Ratings, Interest Coverage Ratios and Default Spread." [https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ratings.html](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ratings.html){:target="_blank"}

**Also known as:** implied credit rating, interest coverage rating, cost of debt.

**Args:**

- <u>firm_type (str, optional):</u> The table to use: "large" (market capitalization above
five billion), "small" (smaller and riskier firms), "financial" (banks and
other financial firms) or "auto", which picks large or small from the market
capitalization of every period. Defaults to "auto".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker and period the Interest Coverage Ratio, Rating, Default
Spread, Risk Free Rate and Pre-tax Cost of Debt.

**Notes:**

- A period without interest expense (reported as zero or not reported) and with a
positive EBIT has an infinite coverage ratio, which Damodaran's tables map to the
highest - <u>rating (Aaa/AAA):</u> there is no interest the operating income has to cover.
Its coverage ratio shows as NaN. This also holds for a company with debt whose
statements do not report its interest separately, such as Apple from its fiscal
year 2024. The rating is NaN where the EBIT (Operating Income) is missing, and for
an operating loss without interest expense, as the coverage ratio then says
nothing about the rating the company would get if it borrowed.
- A coverage ratio below the lowest bound of the table gets the worst rating.
- The market capitalization is compared with five billion in the reporting
currency; for companies that do not report in US dollars, pass the firm type.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["F", "AAPL", "T"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_synthetic_credit_rating()
```

Which returns:

|                                     | 2021     | 2022    | 2023    | 2024     | 2025    |
|:------------------------------------|:---------|:--------|:--------|:---------|:--------|
| ('AAPL', 'Interest Coverage Ratio') | 41.1905  | 40.7496 | 29.062  | nan      | nan     |
| ('AAPL', 'Rating')                  | Aaa/AAA  | Aaa/AAA | Aaa/AAA | Aaa/AAA  | Aaa/AAA |
| ('AAPL', 'Default Spread')          | 0.004    | 0.004   | 0.004   | 0.004    | 0.004   |
| ('AAPL', 'Risk Free Rate')          | 0.0144   | 0.0296  | 0.0397  | 0.0421   | 0.0429  |
| ('AAPL', 'Pre-tax Cost of Debt')    | 0.0184   | 0.0336  | 0.0437  | 0.0461   | 0.0469  |
| ('F', 'Interest Coverage Ratio')    | 2.7915   | 5.0905  | 4.1306  | 4.5695   | 2.0191  |
| ('F', 'Rating')                     | Baa2/BBB | A2/A    | A3/A-   | A2/A     | Ba2/BB  |
| ('F', 'Default Spread')             | 0.0111   | 0.0078  | 0.0089  | 0.0078   | 0.0184  |
| ('F', 'Risk Free Rate')             | 0.0144   | 0.0296  | 0.0397  | 0.0421   | 0.0429  |
| ('F', 'Pre-tax Cost of Debt')       | 0.0255   | 0.0374  | 0.0486  | 0.0499   | 0.0613  |
| ('T', 'Interest Coverage Ratio')    | 3.856    | -0.7472 | 3.7011  | 2.8183   | 3.5511  |
| ('T', 'Rating')                     | A3/A-    | D2/D    | A3/A-   | Baa2/BBB | A3/A-   |
| ('T', 'Default Spread')             | 0.0089   | 0.19    | 0.0089  | 0.0111   | 0.0089  |
| ('T', 'Risk Free Rate')             | 0.0144   | 0.0296  | 0.0397  | 0.0421   | 0.0429  |
| ('T', 'Pre-tax Cost of Debt')       | 0.0233   | 0.2196  | 0.0486  | 0.0532   | 0.0518  |

---

## get_dupont_analysis
Perform a Dupont analysis to breakdown the return on equity (ROE) into its components.

The Dupont analysis is a method used to dissect and understand the factors that drive a company's return on equity (ROE). It breaks down the ROE into three key components: Net Profit Margin, Asset Turnover, and Equity Multiplier. The extended (five-factor) Dupont analysis, method="extended", splits the Net Profit Margin further into three separate drivers - the Tax Burden, the Interest Burden and the Operating Profit Margin - so that the effect of taxation, of financing costs and of operating performance on the return on equity can be read separately.

The formula is as follows:

With method="standard":

$$
\text{Net Profit Margin} = \frac{\text{Net Income}}{\text{Revenue}}
$$

$$
\text{Asset Turnover} = \frac{\text{Revenue}}{\text{Average Total Assets}}
$$

$$
\text{Equity Multiplier} = \frac{\text{Average Total Assets}}{\text{Average Total Shareholder Equity}}
$$

$$
\text{ROE} = \text{Net Profit Margin} \cdot \text{Asset Turnover} \cdot \text{Equity Multiplier}
$$

With method="extended":

$$
\text{Interest Burden Ratio} = \frac{\text{Income Before Tax}}{\text{Operating Income}}
$$

$$
\text{Tax Burden Ratio} = \frac{\text{Net Income}}{\text{Income Before Tax}}
$$

$$
\text{Operating Profit Margin} = \frac{\text{Operating Income}}{\text{Revenue}}
$$

$$
\text{Asset Turnover} = \frac{\text{Revenue}}{\text{Average Total Assets}}
$$

$$
\text{Equity Multiplier} = \frac{\text{Average Total Assets}}{\text{Average Total Shareholder Equity}}
$$

$$
\text{ROE} = \text{Interest Burden Ratio} \cdot \text{Tax Burden Ratio} \cdot \text{Operating Profit Margin} \cdot \text{Asset Turnover} \cdot \text{Equity Multiplier}
$$

The value of the decomposition is in comparing the factors with peers and over time: a retailer earns its return on equity through asset turnover, a software company through its margin and a bank through leverage. A rising return on equity driven only by the Equity Multiplier, for example through share buybacks that shrink equity, is of lower quality than one driven by margin or turnover, and with negative equity the decomposition stops being meaningful.

**Also known as:** DuPont, ROE decomposition, three-factor DuPont, extended DuPont, five-factor DuPont, ROE breakdown.

**Args:**

- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The number of periods to sum flows (income statement items)
over, with the Total Assets and Total Shareholder Equity averaged over the trailing + 1
period ends that open and close those periods, so trailing=1 equals the default average
of the opening and closing balance. E.g. 4 with quarterly data gives the trailing twelve
months (TTM). The window counts calendar periods, so a period without a report makes it
NaN. Defaults to None.
- <u>method (str, optional):</u> "standard" for the three-factor decomposition or "extended" for the
five-factor decomposition. Defaults to "standard".
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing Dupont analysis results, including Net Profit Margin, Asset
Turnover, Equity Multiplier, and the calculated ROE values. With
method="extended" the Interest Burden Ratio, Tax Burden Ratio and Operating
Profit Margin take the place of the Net Profit Margin.

**Notes:**

- The Net Profit Margin is the ratio of Net Income to Total Revenue, indicating the percentage
of revenue that translates into profit.
- The Interest Burden Ratio (Income Before Tax / Operating Income) measures how much of
operating profit survives the cost of debt financing. It equals 1 for a company with no
net interest expense and falls as interest costs rise.
- The Tax Burden Ratio (Net Income / Income Before Tax) measures how much of pre-tax
profit survives taxation, i.e. it equals (1 - Effective Tax Rate).
- The Operating Profit Margin measures operating performance before financing and tax
effects.
- Asset Turnover measures the efficiency of a company's use of its assets to generate sales
revenue.
- The Equity Multiplier measures financial leverage, the use of debt to finance a company's
operations, which can amplify returns as well as risks.
- The equity is the Total Shareholder Equity, which excludes minority interests, as the
Net Income is the income attributable to the shareholders; this is the Return on Equity
of the Ratios module.
- Multiplying the Interest Burden Ratio, Tax Burden Ratio and Operating Profit Margin back
together reproduces the Net Profit Margin, so both decompositions resolve to the same ROE.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["GOOGL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_dupont_analysis()
```

Which returns:

|                   |   2021 |   2022 |   2023 |   2024 |   2025 |
|:------------------|-------:|-------:|-------:|-------:|-------:|
| Net Profit Margin | 0.2951 | 0.212  | 0.2401 | 0.286  | 0.3281 |
| Asset Turnover    | 0.759  | 0.7807 | 0.8009 | 0.821  | 0.7706 |
| Equity Multiplier | 1.4317 | 1.4269 | 1.4228 | 1.4013 | 1.4122 |
| Return on Equity  | 0.3207 | 0.2362 | 0.2736 | 0.3291 | 0.357  |

---

## get_nissim_penman_decomposition
Perform the Nissim and Penman (2001) decomposition of the return on common equity (ROCE) into the return on the operations and the effect of how they are financed.

Where the DuPont analyses split the return on equity into margins, turnover and an equity multiplier that mixes operating and financing liabilities, Nissim and Penman separate the operating activities from the financing activities. The return on common equity becomes the return on net operating assets (RNOA) plus a leverage effect: the financial leverage (FLEV) times the spread between the RNOA and the net borrowing cost (NBC). Borrowing raises the return on equity only while the operations earn more than the debt costs, and a company with net financial assets (negative FLEV) has a return on equity below its RNOA when its financial assets earn less than its operations.

The formula is as follows:

$$
\text{Net Financial Expense} = (\text{Interest Expense} - \text{Interest Income}) \cdot (1 - \text{Effective Tax Rate})
$$

$$
\text{Operating Income} = \text{Net Income} + \text{Net Financial Expense}
$$

$$
\text{Net Financial Obligations} = \text{Total Debt} + \text{Preferred Stock} - \text{Cash and Short Term Investments} - \text{Long Term Investments}
$$

$$
\text{Common Equity} = \text{Total Shareholder Equity} - \text{Preferred Stock}
$$

$$
\text{Net Operating Assets} = \text{Net Financial Obligations} + \text{Common Equity}
$$

$$
\text{Return on Net Operating Assets} \;(\text{RNOA}) = \frac{\text{Operating Income}}{\text{Average Net Operating Assets}}
$$

$$
\text{Net Borrowing Cost} \;(\text{NBC}) = \frac{\text{Net Financial Expense}}{\text{Average Net Financial Obligations}}
$$

$$
\text{Spread} = \text{RNOA} - \text{NBC}
$$

$$
\text{Financial Leverage} \;(\text{FLEV}) = \frac{\text{Average Net Financial Obligations}}{\text{Average Common Equity}}
$$

$$
\text{Leverage Effect} = \text{FLEV} \cdot \text{Spread}
$$

$$
\text{Return on Common Equity} \;(\text{ROCE}) = \text{RNOA} + \text{Leverage Effect}
$$

The balance sheet is split into operating and financial items as follows:

- Financial assets: the cash and cash equivalents, the short term investments and the long term investments. Nissim and Penman treat the marketable securities as financial; the long term investments of the statements are mostly those securities (Apple's long term marketable securities), but also hold equity method stakes (Coca-Cola's bottlers), which Nissim and Penman count as operating and which are financial here.

- Financial obligations: the Total Debt, which holds the short and long term debt and the lease obligations (capital leases are debt in Nissim and Penman), and the preferred stock, which Nissim and Penman treat as a financial claim.

- Common equity: the Total Shareholder Equity minus the preferred stock.

- Operating: everything else, so the net operating assets are the net financial obligations plus the common equity (the operating assets minus the operating liabilities and the minority interest).

**Also known as:** Nissim-Penman decomposition, ROCE decomposition, advanced DuPont analysis.

**Args:**

- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The number of periods to sum the income statement items
over, with the balance sheet items averaged over the trailing + 1 period ends that
open and close those periods, as in the Ratios module. E.g. 4 with quarterly data
gives the trailing twelve months (TTM). The window counts calendar periods, so a
period without a report makes it NaN. Defaults to None, which uses single-period
flows over the average of the opening and closing balance.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the Return on Net Operating Assets, the Net Borrowing
Cost, the Spread, the Financial Leverage, the Leverage Effect and the Return on Common
Equity per ticker and period.

**Notes:**

- Nissim, D. and S. H. Penman, "Ratio Analysis and Equity Valuation: From Research to
Practice," Review of Accounting Studies 6, 2001, pp. 109-154.
- The Return on Common Equity equals Net Income / Average Common Equity exactly, as the
net operating assets are the net financial obligations plus the common equity and the
operating income the net income plus the net financial expense. It differs from the
Return on Equity of the Ratios module only by the preferred stock, which that ratio
keeps in the equity.
- Nissim and Penman add the minority interest to the net operating assets and its share
of the income to the operating income, and multiply the decomposition by a minority
sharing ratio. The statements give no minority share of the income, so the minority
interest is deducted from the net operating assets instead: the operating income and
the net operating assets are both the share of the parent's shareholders, and the
decomposition adds up without a sharing ratio.
- Nissim and Penman use the comprehensive income to common shareholders; the net
income here leaves out the other comprehensive income (such as currency translation
differences). The net financial expense is taxed at the effective tax rate (bounded to
[0, 1], 0 for a pre-tax loss) instead of the marginal statutory rate, and holds no
preferred dividends, which the statements do not report.
- Missing data is treated in two ways. A short or long term investment, preferred
stock or interest income that is not reported is absent and counts as zero (a company
with debt but no interest income is normal). A period with neither an interest
expense nor an interest income (both missing or zero, as in Apple's statements from
fiscal 2024) has an unknown net financial expense rather than a zero one, so the
Return on Net Operating Assets, the Net Borrowing Cost, the Spread, the Leverage
Effect and the Return on Common Equity are NaN for that period (and every trailing
window that holds it); the Financial Leverage remains.
- The Return on Net Operating Assets, the Net Borrowing Cost and the Financial Leverage
are also available as `Toolkit.ratios.get_return_on_net_operating_assets`,
`get_net_borrowing_cost` and `get_financial_leverage`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["KO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_nissim_penman_decomposition()
```

Which returns:

|                                |   2021 |   2022 |   2023 |   2024 |   2025 |
|:-------------------------------|-------:|-------:|-------:|-------:|-------:|
| Return on Net Operating Assets | 0.311  | 0.2795 | 0.3197 | 0.3076 | 0.337  |
| Net Borrowing Cost             | 0.0765 | 0.0299 | 0.0508 | 0.0497 | 0.057  |
| Spread                         | 0.2345 | 0.2496 | 0.2689 | 0.2579 | 0.28   |
| Financial Leverage             | 0.644  | 0.5033 | 0.4032 | 0.4304 | 0.4383 |
| Leverage Effect                | 0.151  | 0.1256 | 0.1085 | 0.111  | 0.1227 |
| Return on Common Equity        | 0.462  | 0.4051 | 0.4282 | 0.4186 | 0.4597 |

---

## get_return_decomposition
The Return Decomposition splits the share price return over a window into the growth of the Earnings per Share and the change of the Price-to-Earnings ratio (the multiple), and adds the dividends paid over the window for the total return. It shows whether a share rose because the company earned more or because investors paid more for the same earnings, e.g. a share whose earnings beat expectations but whose price fell because its multiple contracted.

Since the share price equals the Earnings per Share times the P/E ratio, the price relative over a window is the product of the earnings relative and the multiple relative, which is the earnings and valuation split of equity returns used in return attribution (e.g. Bogle, "Common Sense on Mutual Funds", and the building blocks of Grinold and Kroner, "The Equity Risk Premium", 2002).

The formula is as follows:

$$
1 + \text{Price Return} = (1 + \text{EPS Growth}) \cdot (1 + \text{P/E} \;\text{Change})
$$

$$
\text{EPS Growth} = \frac{\text{EPS}_{t}}{\text{EPS}_{t-\text{lag}}} - 1
$$

$$
\text{P/E} \;\text{Change} = \frac{\frac{\text{Price}_{t}}{\text{EPS}_{t}}}{\frac{\text{Price}_{t-\text{lag}}}{\text{EPS}_{t-\text{lag}}}} - 1
$$

$$
\text{Dividend Return} = \text{Dividends per Share paid over the window} \;/ \;\text{Price}_{t-\text{lag}}
$$

$$
\text{Total Return} = \text{Price Return} + \text{Dividend Return}
$$

With logarithmic=True the parts are log returns that add up: ln(1 + Total Return) = ln(1 + EPS Growth) + ln(1 + P/E Change) + ln(1 + Dividends / Price_t).

**Also known as:** earnings and multiple decomposition, P/E expansion and contraction, multiple expansion, return attribution by earnings growth and re-rating.

**Args:**

- <u>lag (int &#124; None, optional):</u> The number of periods the window spans. Defaults to None,
which compares each period with the same period a year earlier: 1 with annual
data and 4 with quarterly data.
- <u>diluted (bool, optional):</u> Whether to use the diluted Earnings per Share. Defaults to
True.
- <u>trailing (int &#124; None, optional):</u> The number of periods to sum the Net Income over
(and average the shares over). The window counts calendar periods, so a period
without a report makes it NaN. Defaults to None, which uses the trailing twelve
months (4 quarters) with quarterly data and single years with annual data, as
the P/E ratio does.
- <u>logarithmic (bool, optional):</u> Whether to return log returns, which add up, instead of
simple returns, which multiply. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Price Return, EPS Growth, P/E Change, Dividend Return and Total
Return per ticker (rows) and period (columns), as decimals.

**Notes:**

- The share price is the traded Close (adjusted for splits, not for dividends) at the end
of each fiscal period, and the Earnings per Share is the Net Income over the weighted
average (diluted) shares, as in `ratios.get_earnings_per_share`.
- The P/E ratio has no meaning when the earnings are zero or negative, so the EPS Growth
and P/E Change are NaN when the Earnings per Share at either end of the window is not
positive. The Price Return, Dividend Return and Total Return remain; the growth of the
earnings themselves is `ratios.get_earnings_per_share(growth=True)`.
- Dividends are added as paid, without reinvestment, so the Total Return differs slightly
from a return on the dividend-adjusted price.
- The price is the close on the last trading day of each fiscal period (the filing day
with point_in_time), the date the earnings reported for it run up to, and the dividends
are those paid between two such days. The calendar period's close and dividends are
used where the daily prices do not reach those days.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMD", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_return_decomposition()
```

Which returns:

|                             |    2022 |    2023 |    2024 |    2025 |
|:----------------------------|--------:|--------:|--------:|--------:|
| ('AMD', 'Price Return')     | -0.5568 |  1.2759 | -0.1507 |  0.7173 |
| ('AMD', 'EPS Growth')       | -0.6734 | -0.3745 |  0.9075 |  1.6433 |
| ('AMD', 'P/E Change')       |  0.3571 |  2.6387 | -0.5548 | -0.3503 |
| ('AMD', 'Dividend Return')  |  0      |  0      |  0      |  0      |
| ('AMD', 'Total Return')     | -0.5568 |  1.2759 | -0.1507 |  0.7173 |
| ('MSFT', 'Price Return')    | -0.0519 |  0.3259 |  0.3125 |  0.1129 |
| ('MSFT', 'EPS Growth')      |  0.1979 |  0.0039 |  0.2185 |  0.156  |
| ('MSFT', 'P/E Change')      | -0.2085 |  0.3208 |  0.0771 | -0.0373 |
| ('MSFT', 'Dividend Return') |  0.0089 |  0.0104 |  0.0086 |  0.0072 |
| ('MSFT', 'Total Return')    | -0.043  |  0.3363 |  0.3211 |  0.1201 |

---

## get_sustainable_growth_rate
The Sustainable Growth Rate (SGR) is the maximum rate at which a company can grow its revenue, using internally generated funds only, without having to raise additional equity or increase its financial leverage.

The formula is as follows:

$$
\text{Return on Equity} = \frac{\text{Net Income}}{\text{Total Shareholder Equity at the beginning of the period}}
$$

$$
\text{Retention Ratio} = 1 - \text{Dividend Payout Ratio}
$$

$$
\text{SGR} = \text{Return on Equity} \cdot \text{Retention Ratio}
$$

The SGR assumes the company keeps its leverage and pays out only through dividends. Companies that return cash mainly through share buybacks have a low payout ratio on paper and a return on equity inflated by a shrinking equity base, so their SGR overstates what they can fund internally.

**Also known as:** SGR, self-sustainable growth rate.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. The window counts
calendar periods, so a period without a report makes it NaN. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the Sustainable Growth Rate.

**Notes:**

- Growing faster than the SGR without external financing typically requires either
improving profitability, reducing the dividend payout, or increasing leverage.
- Following Higgins ("Analysis for Financial Management"), the Return on Equity is measured
on the equity at the beginning of the - <u>period (the previous period's closing balance, or that of
`trailing` periods back with `trailing` set):</u> the retained earnings then grow that equity by
exactly the SGR. The two forms are equal under the model's assumption that equity grows only
through retained earnings: with that assumption the SGR equals ROE * b / (1 - ROE * b) with the
Return on Equity measured on the ending equity. Share issuance, buybacks and other changes in
equity break the equality.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NKE", "LULU", "DECK"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_sustainable_growth_rate()
```

Which returns:

|      |   2021 |   2022 |   2023 |   2024 |
|:-----|-------:|-------:|-------:|-------:|
| DECK | 0.3129 | 0.3359 | 0.4302 | 0.4584 |
| LULU | 0.3812 | 0.312  | 0.4923 | 0.4288 |
| NKE  | 0.3297 | 0.2001 | 0.2521 | 0.0637 |

---

## get_internal_growth_rate
The Internal Growth Rate (IGR) is the maximum rate at which a company can grow its revenue using only its retained earnings, without raising any external financing (neither debt nor equity).

The formula is as follows:

$$
\text{Return on Assets} = \frac{\text{Net Income}}{\text{Total Assets at the end of the period}}
$$

$$
\text{Retention Ratio} = 1 - \text{Dividend Payout Ratio}
$$

$$
\text{IGR} = \frac{\text{Return on Assets} \cdot \text{Retention Ratio}}{1 - (\text{Return on Assets} \cdot \text{Retention Ratio})}
$$

**Also known as:** IGR.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. The window counts
calendar periods, so a period without a report makes it NaN. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the Internal Growth Rate.

**Notes:**

- The IGR is more conservative than the Sustainable Growth Rate (SGR) since it assumes
no additional debt is raised to fund growth, whereas the SGR assumes the company
maintains its current level of financial leverage.
- The Return on Assets is measured on the Total Assets at the end of the period, as in
Ross, Westerfield and Jaffe ("Corporate Finance"). Under the model's assumption that assets
grow only through retained earnings, the formula equals the Return on Assets on the beginning
Total Assets times the Retention Ratio, the growth the retained earnings add to the beginning
assets, consistent with the beginning-equity definition of the Sustainable Growth Rate. Assets
funded otherwise (new debt, equity or payables) break the equality.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["ADBE", "INTU", "ADSK"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_internal_growth_rate()
```

Which returns:

|      |   2021 |   2022 |   2023 |   2024 |     2025 |
|:-----|-------:|-------:|-------:|-------:|---------:|
| ADBE | 0.2151 | 0.2122 | 0.2229 | 0.2254 |   0.3188 |
| ADSK | 0.0613 | 0.0955 | 0.1006 | 0.1144 | nan      |
| INTU | 0.1004 | 0.0489 | 0.0569 | 0.0639 |   0.0782 |

---

## get_fundamental_growth_rate
Calculate Damodaran's fundamental growth rate of operating income: the growth that a company's reinvestment produces at its return on capital, with the reinvestment rate and the sales-to-capital ratio it is built from. Where the sustainable growth rate grows the equity with the retained net income, this grows the operating income with the capital reinvested in the operations, the growth a discounted cash flow valuation of the firm assumes.

The formula is as follows:

$$
\text{NOPAT} = \text{EBIT} \cdot (1 - \text{Tax Rate})
$$

$$
\text{Net Capital Expenditure} = \text{Capital Expenditure} - \text{Depreciation and Amortization}
$$

$$
\text{Reinvestment} = \text{Net Capital Expenditure} + \text{Change in Working Capital}
$$

$$
\text{Reinvestment Rate} = \frac{\text{Reinvestment}}{\text{NOPAT}}
$$

$$
\text{Invested Capital} = \text{Total Equity} + \text{Total Debt} - \text{Cash and Short Term Investments}
$$

$$
\text{Return on Invested Capital} = \frac{\text{NOPAT}}{\text{Invested Capital at the beginning of the period}}
$$

$$
\text{Fundamental Growth Rate} = \text{Reinvestment Rate} \cdot \text{Return on Invested Capital}
$$

$$
\text{Sales to Capital} = \frac{\text{Revenue}}{\text{Invested Capital at the beginning of the period}}
$$

The reinvestment is NOPAT minus the Free Cash Flow to Firm of `get_free_cash_flow_to_firm`, so a company that reinvests less than its depreciation has a negative reinvestment rate and a negative fundamental growth. The sales-to-capital ratio links revenue growth to the reinvestment it needs: Reinvestment = Change in Revenue / Sales to Capital.

For more information, see the following sources:

- Damodaran, A. (2012). "Investment Valuation." Wiley, 3rd edition, chapter 11 (Estimating Growth) and chapter 12 (Closure in Valuation).

**Also known as:** Damodaran reinvestment rate, fundamental growth, expected growth in EBIT, reinvestment rate times return on capital, sales to capital ratio, sales to invested capital.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The number of periods to sum the flows over, with the
invested capital taken `trailing` periods back. The window counts calendar periods, so
a period without a report makes it NaN. Defaults to None, which is 4 on quarterly data
(a trailing twelve months against the capital a year earlier) and single years on
yearly data.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker the NOPAT, Net Capital Expenditure, Change in Working Capital,
Reinvestment, Reinvestment Rate, Invested Capital (at the beginning of the period), Return
on Invested Capital, Fundamental Growth Rate and Sales to Capital, rates as decimals.

**Notes:**

- The tax rate is the effective tax rate kept within 0 and 1 (0 without a pre-tax profit), as
in `get_economic_value_added`, and EBIT the reported Operating Income.
- The Capital Expenditure is the purchase of property, plant and equipment of the cash flow
statement; Damodaran also counts acquisitions, which are lumpy and left out here. The Change
in Working Capital is that of the cash flow statement (an increase is positive here), the
non-cash working capital Damodaran uses.
- The Invested Capital is Damodaran's: the book value of equity and debt net of cash, at the
beginning of the period, as the return on capital measures the income on the capital already
in place. A non-positive invested capital leaves the return and the ratio NaN, and a
non-positive NOPAT the reinvestment rate.
- This is a different measure from the retention ratio of the Ratios module
(`get_retention_ratio`, 1 minus the dividend payout), the equity counterpart that the
sustainable growth rate multiplies with the return on equity.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["MSFT", "GOOGL", "META"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_fundamental_growth_rate().loc["MSFT"]
```

Which returns:

|                                  |       2021 |         2022 |        2023 |         2024 |        2025 |
|:---------------------------------|-----------:|-------------:|------------:|-------------:|------------:|
| Net Operating Profit After Taxes | 6.0249e+10 |  7.24487e+10 | 7.17226e+10 |  8.94819e+10 | 1.05869e+11 |
| Net Capital Expenditure          | 8.936e+09  |  9.426e+09   | 1.4246e+10  |  2.219e+10   | 3.0398e+10  |
| Change in Working Capital        | 9.36e+08   | -4.46e+08    | 2.388e+09   | -1.824e+09   | 5.35e+09    |
| Reinvestment                     | 9.872e+09  |  8.98e+09    | 1.6634e+10  |  2.0366e+10  | 3.5748e+10  |
| Reinvestment Rate                | 0.1639     |  0.1239      | 0.2319      |  0.2276      | 0.3377      |
| Invested Capital                 | 6.3887e+10 |  9.401e+10   | 1.40193e+11 |  1.74408e+11 | 2.90798e+11 |
| Return on Invested Capital       | 0.9431     |  0.7706      | 0.5116      |  0.5131      | 0.3641      |
| Fundamental Growth Rate          | 0.1545     |  0.0955      | 0.1187      |  0.1168      | 0.1229      |
| Sales to Capital                 | 2.631      |  2.109       | 1.5116      |  1.4055      | 0.9688      |

---

## get_rule_of_40
Calculate the Rule of 40 score: the revenue growth plus the profit margin, the measure of software and other subscription companies that trade growth against profitability. A score of 40% (0.40) or more is seen as healthy: a company growing 30% a year should keep a margin of at least 10%, one that grows 10% a margin of 30%.

The formula is as follows:

$$
\text{Revenue Growth} = \frac{\text{Revenue}}{\text{Revenue a year earlier}} - 1
$$

$$
\text{Free Cash Flow Margin} = \frac{\text{Free Cash Flow}}{\text{Revenue} \;\left(\text{or EBITDA Margin} = \frac{\text{EBITDA}}{\text{Revenue}}\right)}
$$

$$
\text{Rule of 40 Score} = \text{Revenue Growth} + \text{Free Cash Flow Margin} \;(\text{or EBITDA Margin})
$$

The rule comes from venture capital practice for software companies (attributed to Brad Feld, 2015) and has no academic source; investors use the free cash flow margin and the EBITDA margin, which the `margin` parameter chooses between.

For more information, see the following sources:

- Feld, B. (2015). "The Rule of 40% For a Healthy SaaS Company." Feld Thoughts ([https://feld.com/archives/2015/02/rule-40-healthy-saas-company/](https://feld.com/archives/2015/02/rule-40-healthy-saas-company/){:target="_blank"}).

**Also known as:** Rule of 40, 40% rule, growth plus margin, SaaS rule of 40.

**Args:**

- <u>margin (str, optional):</u> The margin to add: "free_cash_flow" (Free Cash Flow / Revenue) or
"ebitda" (EBITDA / Revenue). Defaults to "free_cash_flow".
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The number of periods to sum the revenue and cash flows
over. The window counts calendar periods, so a period without a report makes it NaN.
Defaults to None, which is 4 on quarterly data (a trailing twelve months, its growth
against the trailing twelve months a year earlier) and single years on yearly data.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker the Revenue Growth, the margin (Free Cash Flow Margin or EBITDA
Margin) and the Rule of 40 Score, as decimals.

**Notes:**

- The revenue growth compares with the same period a year earlier (four quarters back on
quarterly data), so the first year has no score. Growth from a negative or zero revenue is
NaN.
- The Free Cash Flow is that of the cash flow statement (Operating Cash Flow minus Capital
Expenditure).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["CRM", "NOW", "ADBE"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_rule_of_40().xs("Rule of 40 Score", level=1)
```

Which returns:

|      |   2021 |   2022 |   2023 |   2024 |     2025 |
|:-----|-------:|-------:|-------:|-------:|---------:|
| ADBE | 0.6627 | 0.5354 | 0.4601 | 0.4741 |   0.5198 |
| CRM  | 0.446  | 0.3848 | 0.3843 | 0.4153 | nan      |
| NOW  | 0.6097 | 0.5287 | 0.5396 | 0.5353 |   0.5535 |

---

## get_piotroski_score
Calculate the Piotroski Score, a comprehensive financial assessment tool that helps investors and analysts evaluate a company's financial health and fundamental strength.

The Piotroski Score was developed by Joseph Piotroski and is based on a set of nine fundamental financial criteria. Each criterion is assigned a score of 0 or 1, and the scores are then summed to calculate the Piotroski Score.

The nine criteria are categorized into three groups:

1. Profitability:
   - Return on Assets (ROA) Criteria: Measures the profitability of the company.
   - Operating Cash Flow Criteria: Evaluates the company's ability to generate cash from its operations.
   - Change in ROA Criteria: Assesses the trend in ROA over time.
   - Accruals Criteria: Examines the quality of earnings.
2. Leverage, Liquidity, and Operating Efficiency:
   - Change in Leverage Criteria: Analyzes changes in the company's leverage (debt).
   - Change in Current Ratio Criteria: Evaluates changes in the current ratio.
   - Number of Shares Criteria: Assesses the issuance of common shares.
3. Operating Efficiency and Asset Utilization:
   - Gross Margin Criteria: Examines the company's gross margin, a measure of profitability.
   - Asset Turnover Ratio Criteria: Evaluates the efficiency of asset utilization and sales generation.

The Piotroski Score is calculated by summing the scores assigned to each of the nine criteria. The maximum possible score is 9, indicating the highest financial strength, while the minimum score is 0, suggesting potential financial weaknesses.

Note that the Piostroski Score has been developed many decades ago and that it is important to always compare the same sectors. E.g. it could be that it is quite normal that a firm issues shares each year which nets a lower score even though it is a normal practice in that sector.

Piotroski designed the F-Score to separate winners from losers among value stocks (high book-to-market), where scores of 8 or 9 marked the strongest companies and scores of 0 or 1 the weakest. Because most criteria compare this year with last year, the score measures the direction of change rather than the level of financial strength, and a single strong year after a weak one can score highly.

Following Piotroski (2000), the Return on Assets, the Operating Cash Flow in the accruals signal and the Asset Turnover are scaled by the total assets at the beginning of the period, while the leverage signal divides long-term debt by the average of the beginning and ending total assets.

The formula is as follows, where (t-1) is the same period a year earlier (the previous column on yearly data, four quarters back on quarterly data, so quarterly comparisons are year over year) and Beginning Total Assets are the total assets at the end of the previous period (`trailing` periods back when set, one year earlier with trailing=4 on quarterly data):

$$
\text{Return on Assets} \;(\text{ROA}) = \frac{\text{Net Income}}{\text{Beginning Total Assets}}
$$

$$
\text{Return on Assets Criteria} = 1 \;\text{if ROA} > 0,\;\; \text{else 0}
$$

$$
\text{Operating Cashflow Criteria} = 1 \;\text{if Operating Cash Flow} > 0,\;\; \text{else 0}
$$

$$
\text{Change in Return on Assets Criteria} = 1 \;\text{if ROA} \;(t) > \text{ROA} \;(t-1),\;\; \text{else 0}
$$

$$
\text{Accruals Criteria} = 1 \;\text{if} \;\frac{\text{Operating Cash Flow}}{\text{Beginning Total Assets}} > \text{ROA},\;\; \text{else 0}
$$

$$
\text{Average Total Assets} = \frac{\text{Beginning Total Assets} + \text{Total Assets}}{2}
$$

$$
\text{Change in Leverage Criteria} = 1 \;\text{if} \;\frac{\text{Long Term Debt}}{\text{Average Total Assets}} \;\text{is lower than in} \;(t-1),\;\; \text{else 0}
$$

$$
\text{Change in Current Ratio Criteria} = 1 \;\text{if} \;\frac{\text{Total Current Assets}}{\text{Total Current Liabilities}} \;\text{is higher than in} \;(t-1),\;\; \text{else 0}
$$

$$
\text{Number of Shares Criteria} = 1 \;\text{if Common Stock Issued} = 0,\;\; \text{else 0}
$$

$$
\text{Gross Margin Criteria} = 1 \;\text{if} \;\frac{\text{Revenue} - \text{Cost of Goods Sold}}{\text{Revenue}} \;\text{is higher than in} \;(t-1),\;\; \text{else 0}
$$

$$
\text{Asset Turnover Criteria} = 1 \;\text{if} \;\frac{\text{Revenue}}{\text{Beginning Total Assets}} \;\text{is higher than in} \;(t-1),\;\; \text{else 0}
$$

$$
\text{Piotroski Score} = \text{SUM} \;\text{of the nine criteria} \;(0 \;\text{to}\; 9)
$$

With `trailing`, the flows (net income, operating cash flow, revenue, cost of goods sold and common stock issued) are summed over the trailing periods, while the balance sheet items (total assets, long term debt, current assets and current liabilities) are taken at the end of each period.

Please see Piotroski, Joseph D. "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers." Journal of Accounting Research, Vol. 38, Supplement, 2000, pp. 1-41.

**Also known as:** Piotroski F-score, financial strength, quality score.

**Args:**

- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. The window
counts calendar periods, so a period without a report makes it NaN. Defaults to None, which
is 4 on quarterly data (a trailing twelve months), as the score was estimated on yearly
statements.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the Piotroski F-Score and its components.

Periods for which the financial statements have not been reported yet are returned as NaN
rather than being scored zero across the board.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["F", "GM", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_piotroski_score().xs("Piotroski Score", level=1)
```

Which returns:

|      |   2022 |   2023 |   2024 |   2025 |
|:-----|-------:|-------:|-------:|-------:|
| F    |      5 |      6 |      6 |      3 |
| GM   |      6 |      6 |      7 |      5 |
| TSLA |      8 |      3 |      4 |      5 |

---

## get_beneish_m_score
The Beneish M-Score is a probabilistic model, developed by Messod Beneish, that uses eight financial ratios derived from a company's financial statements to identify whether a company has manipulated its earnings. It is a natural companion to the Altman Z-Score and Piotroski F-Score, using the same normalized financial statements as its input.

The formula is as follows, where (t-1) is the same period a year earlier (the previous column on yearly data, four quarters back on quarterly data, so quarterly comparisons are year over year):

$$
\text{DSRI} \;(\text{Days Sales in Receivables Index}) = \frac{\left(\frac{\text{Net Receivables}}{\text{Revenue}}\right) (t)}{\left(\frac{\text{Net Receivables}}{\text{Revenue}}\right) (t-1)}
$$

$$
\text{GMI} \;(\text{Gross Margin Index}) = \frac{\text{Gross Margin} \;(t-1)}{\text{Gross Margin} \;(t)},\;\; \text{with}\;\; \text{Gross Margin} = \frac{\text{Revenue} - \text{Cost of Goods Sold}}{\text{Revenue}}
$$

$$
\text{AQI} \;(\text{Asset Quality Index}) = \frac{\text{Asset Quality} \;(t)}{\text{Asset Quality} \;(t-1)},\;\; \text{with}\;\; \text{Asset Quality} = 1 - \frac{\text{Total Current Assets} + \text{Property, Plant and Equipment}}{\text{Total Assets}}
$$

$$
\text{SGI} \;(\text{Sales Growth Index}) = \frac{\text{Revenue} \;(t)}{\text{Revenue} \;(t-1)}
$$

$$
\text{DEPI} \;(\text{Depreciation Index}) = \frac{\text{Depreciation Rate} \;(t-1)}{\text{Depreciation Rate} \;(t)},\;\; \text{with}\;\; \text{Depreciation Rate} = \frac{\text{Depreciation and Amortization}}{\text{Depreciation and Amortization} + \text{Property, Plant and Equipment}}
$$

$$
\text{SGAI} \;(\text{SG\&A Expenses Index}) = \frac{\left(\frac{\text{SG\&A Expenses}}{\text{Revenue}}\right) (t)}{\left(\frac{\text{SG\&A Expenses}}{\text{Revenue}}\right) (t-1)}
$$

$$
\text{LVGI} \;(\text{Leverage Index}) = \frac{\text{Leverage} \;(t)}{\text{Leverage} \;(t-1)},\;\; \text{with}\;\; \text{Leverage} = \frac{\text{Total Current Liabilities} + \text{Long Term Debt}}{\text{Total Assets}}
$$

$$
\text{TATA} \;(\text{Total Accruals to Total Assets}) = \frac{\text{Net Income} - \text{Operating Cash Flow}}{\text{Total Assets}}
$$

$$
\text{M-Score} = - 4.84 + 0.92 \cdot \text{DSRI} + 0.528 \cdot \text{GMI} + 0.404 \cdot \text{AQI} + 0.892 \cdot \text{SGI} + 0.115 \cdot \text{DEPI} - 0.172 \cdot \text{SGAI} + 4.679 \cdot \text{TATA} - 0.327 \cdot \text{LVGI}
$$

With `trailing`, the flows are summed over the trailing periods, while the balance sheet items are taken at the end of each period.

The five-variable model of Beneish (1997), with model="five", leaves out SGAI, LVGI and TATA:

$$
\text{M-Score} \;(\text{five variables}) = - 6.065 + 0.823 \cdot \text{DSRI} + 0.906 \cdot \text{GMI} + 0.593 \cdot \text{AQI} + 0.717 \cdot \text{SGI} + 0.107 \cdot \text{DEPI}
$$

The -1.78 threshold belongs to the eight-variable model; the five-variable version uses -2.22. Fast-growing companies are flagged more often because sales growth itself raises the score, and the model was estimated without financial companies and is not suited to banks and insurers, so a score above the threshold is a prompt to read the accounts, not a finding.

**Also known as:** Beneish M-Score, earnings manipulation score.

**Args:**

- <u>model (str, optional):</u> The model: "eight" for the eight-variable model of Beneish (1999) or
"five" for the five-variable model of Beneish (1997), which returns its five indices
and score. Defaults to "eight".
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. The window
counts calendar periods, so a period without a report makes it NaN. Defaults to None, which
is 4 on quarterly data (a trailing twelve months), as the score was estimated on yearly
statements.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the Beneish M-Score and its components.

**Notes:**

- A M-Score greater than -1.78 suggests that the company is likely to be an earnings
manipulator. A M-Score lower than -1.78 suggests the company is unlikely to be a manipulator.
- As with the Altman Z-Score and Piotroski F-Score, this is a probabilistic, not a
definitive, indicator and should be combined with further fundamental analysis.
- Every index compares the current period with the same period a year earlier, so the first
year of the results (one period on yearly data, four on quarterly data) has no M-Score.
- Total Accruals are Net Income minus Cash Flow from Operations, the cash flow form of
Beneish, Lee and Nichols (2013), rather than the balance sheet form of Beneish (1999).
- The Depreciation Index uses Depreciation and Amortization, since statements report the two
as one line, where Beneish (1999) uses depreciation alone.

References:
- Beneish, Messod D. "Detecting GAAP Violation: Implications for Assessing Earnings
Management among Firms with Extreme Financial Performance." Journal of Accounting and
Public Policy, Vol. 16, No. 3, 1997, pp. 271-309.
- Beneish, Messod D. "The Detection of Earnings Manipulation." Financial Analysts Journal,
Vol. 55, No. 5, 1999, pp. 24-36.
- Beneish, Messod D., Charles M. C. Lee, and D. Craig Nichols. "Earnings Manipulation and
Expected Returns." Financial Analysts Journal, Vol. 69, No. 2, 2013, pp. 57-82.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NFLX", "DIS", "CMCSA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_beneish_m_score().xs("Beneish M-Score", level=1)
```

Which returns:

|       |    2021 |    2022 |    2023 |    2024 |    2025 |
|:------|--------:|--------:|--------:|--------:|--------:|
| CMCSA | -2.6609 | -2.8625 | -2.661  | -2.6852 | -2.734  |
| DIS   | -2.5143 | -2.5357 | -2.6392 | -2.6963 | -2.595  |
| NFLX  | -1.6697 | -1.3345 | -2.5628 | -2.3319 | -2.1611 |

---

## get_magic_formula
Calculate Joel Greenblatt's Magic Formula ranking. Companies are ranked on two measures and the ranks are added; the lowest total combines a good business with a low price:

$$
\text{Earnings Yield} = \frac{\text{EBIT}}{\text{Enterprise Value}} \;(\text{how cheap the company is})
$$

$$
\text{Return on Capital} = \frac{\text{EBIT}}{\text{Net Working Capital} + \text{Net Fixed Assets}} \;(\text{how good the business is})
$$

Net working capital excludes cash and short-term debt, so the return on capital measures the operating business. The ranking is across the Toolkit's tickers, so pass the universe to choose from.

For more information, see the following book:

- Greenblatt, J. (2006). "The Little Book That Beats the Market." Wiley.

**Also known as:** Greenblatt formula, earnings yield and return on capital ranking.

**Args:**

- <u>diluted (bool, optional):</u> Whether to use the diluted share count for the market
capitalization. Defaults to True.
- <u>trailing (int &#124; None, optional):</u> Sum the operating income over this many periods
(e.g. 4 quarters, a trailing twelve months). The enterprise value and the
capital are taken at the period end. The window counts calendar periods, so a
period without a report makes it NaN. Defaults to None, which is 4 for
quarterly data (a year of operating income) and 1 otherwise.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker and period the Earnings Yield, Return on Capital, their
ranks and the Magic Formula Rank (1 is the most attractive).

**Notes:**

- With quarterly data and the default trailing twelve months, the first ranks are in
the fourth quarter of statements. When the statements cover fewer periods, the
result is empty and a warning names the number of periods needed; set an earlier
`start_date` to obtain the ranks.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "GOOGL", "META", "INTC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_magic_formula().xs("Magic Formula Rank", level=1)
```

Which returns:

|       |   2021 |   2022 |   2023 |   2024 |   2025 |
|:------|-------:|-------:|-------:|-------:|-------:|
| AAPL  |      1 |      1 |      1 |      1 |      1 |
| GOOGL |      4 |      2 |      2 |      1 |      4 |
| INTC  |      3 |      5 |      5 |      5 |      5 |
| META  |      1 |      2 |      2 |      3 |      2 |
| MSFT  |      4 |      4 |      4 |      3 |      2 |

---

## get_mohanram_g_score
Calculate Partha Mohanram's G-Score, a score from 0 to 8 that separates winners from losers among growth (low book-to-market) companies, where value measures such as the Piotroski F-Score say little. Each signal is 1 when the company does better than the median of its peers, the Toolkit's tickers:

- Profitability: return on assets (G1) and cash flow return on assets (G2) above the median, and cash flow above net income (G3).
- Naive extrapolation: a lower than median variance of the return on assets (G4) and of revenue growth (G5).
- Accounting conservatism: research and development (G6), capital expenditure (G7) and advertising (G8, selling and marketing expenses) relative to assets above the median, as these investments depress current earnings.

As in the paper, the return on assets, the cash flow return on assets and the three intensities are scaled by the total assets at the start of the year, the variances are taken over the past five years with at least three available, and a signal that cannot be calculated for a company (a missing item, or too short a history) scores 0.

For more information, see the following paper:

- Mohanram, P.S. (2005). "Separating Winners from Losers among Low Book-to-Market Stocks using Financial Statement Analysis." Review of Accounting Studies, 10, 133-170.

**Also known as:** G-Score, growth stock score.

**Args:**

- <u>variance_periods (int, optional):</u> The number of yearly values the variances of
G4 (return on assets) and G5 (revenue growth) are calculated over, of which at
least three (or all, when fewer are asked for) must be available. With
`trailing` the values are `trailing` periods apart (one a year with 4
quarters); without it, one per period. Defaults to 5, the five years of the
paper.
- <u>trailing (int &#124; None, optional):</u> Sum the flows over this many periods (e.g. 4
quarters, a trailing twelve months) and compare with the values `trailing`
periods back, so that with quarterly data every change is year over year.
Balance sheet items are taken at the period end. The window counts calendar
periods, so a period without a report makes it NaN. Defaults to None, which
is 4 for quarterly data (a year) and 1 otherwise; pass 1 for quarterly data
to compare quarter over quarter.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker and period the eight signals and the G-Score.

**Notes:**

- The paper compares with industry medians; here the medians are those of the
tickers given, so pass a peer group of the same industry.
- The variances need three yearly values and revenue growth needs the year before
the first, so the first G-Score is in the fourth year of statements (with
quarterly data, the sixteenth quarter). A company with a shorter history than its
peers scores 0 on G4 and G5. When the statements cover fewer periods than that,
the result is empty and a warning names the number of periods needed; set an
earlier `start_date` to obtain the score.
- The variances are of yearly values, as in the paper (Tables 2 to 4: the variance of
the return on assets and of the annual sales growth over the past three to five
years), also with quarterly data, where the values are trailing years a year apart.
- Net Income stands in for the net income before extraordinary items of the paper, as
the statements do not report extraordinary items separately.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "GOOGL", "META", "NVDA", "ADBE"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_mohanram_g_score().xs("G-Score", level=1)
```

Which returns:

|       |   2023 |   2024 |   2025 |
|:------|-------:|-------:|-------:|
| AAPL  |      4 |      4 |      2 |
| ADBE  |      5 |      5 |      5 |
| GOOGL |      4 |      4 |      6 |
| META  |      6 |      5 |      4 |
| MSFT  |      4 |      5 |      3 |
| NVDA  |      3 |      3 |    nan |

---

## get_dechow_f_score
Calculate the Dechow F-Score, the probability that a company's financial statements are misstated relative to the average company. It was estimated on companies the SEC charged with misstating their earnings, and combines:

- Accrual quality: RSST accruals (the change in non-cash working capital, non-current operating assets and financial assets), the changes in receivables and inventory, and the share of soft assets (assets other than cash and short-term investments and net property, plant and equipment).
- Performance: the change in cash sales and in return on assets.
- Incentives: whether the company issued long-term debt or stock.

Predicted Value = -7.893 + 0.790 RSST Accruals + 2.518 ΔReceivables + 1.191 ΔInventory + 1.979 Soft Assets + 0.171 ΔCash Sales - 0.932 ΔROA + 1.029 Issuance Probability = $$e^{\text{PV}} / (1 + e^{\text{PV}})$$, F-Score = Probability / 0.0037

An F-Score of 1 is average risk; above 1 the risk is elevated, above 1.85 substantial and above 2.45 high.

For more information, see the following paper:

- Dechow, P.M., Ge, W., Larson, C.R. and Sloan, R.G. (2011). "Predicting Material Accounting Misstatements." Contemporary Accounting Research, 28(1), 17-82.

**Also known as:** F-Score (Dechow), misstatement score, earnings manipulation probability.

**Args:**

- <u>trailing (int &#124; None, optional):</u> Sum the flows over this many periods (e.g. 4
quarters, a trailing twelve months) and compare with the values `trailing`
periods back, so that with quarterly data every change is year over year.
Balance sheet items are taken at the period end. The window counts calendar
periods, so a period without a report makes it NaN. Defaults to None, which
is 4 for quarterly data (a year) and 1 otherwise; pass 1 for quarterly data
to compare quarter over quarter.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker and period the seven inputs, the Predicted Value, the
Probability of Misstatement and the F-Score.

**Notes:**

- The paper counts the gross issuance of long-term debt. Where the statements only
report the net issuance (issuance minus repayments), as Financial Modeling Prep's
do, a company that issued debt but repaid more counts as not issuing.
- The model was estimated on yearly statements, so with quarterly data the flows
are summed over the trailing twelve months by default.
- The changes compare with the year before and the change in return on assets with
the return a year back, so the first F-Score is in the third year of statements
(with quarterly data and the default trailing twelve months, the ninth quarter).
When the statements cover fewer periods, the result is empty and a warning names
the number of periods needed; set an earlier `start_date` to obtain the score.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "SMCI"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_dechow_f_score().xs("F-Score", level=1)
```

Which returns:

|      |   2022 |   2023 |   2024 |   2025 |
|:-----|-------:|-------:|-------:|-------:|
| AAPL | 0.4226 | 0.3916 | 0.3913 | 0.3962 |
| MSFT | 0.811  | 0.7759 | 1.018  | 0.8628 |
| SMCI | 2.797  | 0.6471 | 6.128  | 0.8275 |

---

## get_montier_c_score
Calculate James Montier's C-Score, a count from 0 to 6 of warning signs that a company is "cooking the books". Each sign is 1 when present:

- A growing gap between net income and cash flow from operations.
- Rising days sales outstanding: receivables growing faster than sales.
- Rising days sales of inventory: inventory growing faster than cost of sales.
- Rising other current assets relative to revenue, a place to park costs.
- Falling depreciation relative to gross property, plant and equipment, which flatters earnings.
- Total asset growth above 10%, typical of serial acquirers.

Montier found that companies scoring 5 or 6 underperformed the market markedly.

For more information, see the following paper:

- Montier, J. (2008). "Cooking the Books, or, More Sailing Under the Black Flag." Société Générale, Mind Matters.

**Also known as:** C-Score, cooking the books score.

**Args:**

- <u>trailing (int &#124; None, optional):</u> Sum the flows over this many periods (e.g. 4
quarters, a trailing twelve months) and compare with the values `trailing`
periods back, so that with quarterly data every change is year over year.
Balance sheet items are taken at the period end. The window counts calendar
periods, so a period without a report makes it NaN. Defaults to None, which
is 4 for quarterly data (a year) and 1 otherwise; pass 1 for quarterly data
to compare quarter over quarter.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker and period the six signals and the C-Score.

**Notes:**

- Gross property, plant and equipment is reported by Yahoo Finance but not by
Financial Modeling Prep; for a company without it, depreciation is compared with
the net amount, whose ratio also rises as the assets age and so can hide a decline.
- The signs compare with the year before, so the first C-Score is in the second year
of statements (with quarterly data and the default trailing twelve months, the
eighth quarter). When the statements cover fewer periods, the result is empty and a
warning names the number of periods needed; set an earlier `start_date` to obtain
the score.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "SMCI"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_montier_c_score().xs("C-Score", level=1)
```

Which returns:

|      |   2021 |   2022 |   2023 |   2024 |   2025 |
|:-----|-------:|-------:|-------:|-------:|-------:|
| AAPL |      4 |      2 |      3 |      3 |      3 |
| MSFT |      5 |      2 |      5 |      3 |      2 |
| SMCI |      5 |      5 |      2 |      5 |      2 |

---

## get_quality_score
The Quality Score follows the Quality Minus Junk (QMJ) score of Asness, Frazzini and Pedersen (2019): a company is of high quality when it is profitable, growing, safe and pays out to its shareholders. Every measure is ranked across the tickers given in each period and turned into a z-score, each of the four components is the z-score of the average of its measures, and the Quality Score is the z-score of their sum. A positive score is a higher quality than the average of the tickers given.

The measures are as follows (a higher value is a higher quality, so the measures marked "low" enter with a minus sign):

$$
\text{Profitability:}\;\; \text{Gross Profits to Assets} \;\left(\frac{\text{Revenue} - \text{Cost of Goods Sold}}{\text{Total Assets}},\; \text{Novy-Marx}\; 2013\right),\;\; \text{Return on Equity, Return on Assets, Cash Flow to Assets} \;\left(\frac{\text{Operating Cash Flow} - \text{Capital Expenditure}}{\text{Total Assets}}\right),\;\; \text{Gross Margin and low accruals} \;\left(\frac{\text{Operating Cash Flow} - \text{Net Income}}{\text{Total Assets}}\right)
$$

- Growth: the change in Gross Profits to Assets, Return on Equity, Return on Assets, Cash Flow to Assets and Gross Margin over `growth_years`

$$
\text{Safety:}\;\; \text{low Beta (of the period's returns against the benchmark)},\;\; \text{low leverage} \;\left(\frac{\text{Total Debt}}{\text{Total Assets}}\right),\;\; \text{low Ohlson O-Score, high Altman Z-Score and low earnings volatility (the standard deviation of the Return on Equity over growth\_years)}
$$

$$
\text{Payout:}\;\; \text{low equity issuance (-ln of the change in the diluted shares over a year)},\;\; \text{low debt issuance} \;(- \ln \;\text{of the change in Total Debt over a year}) \;\text{and the net payout ratio} \;\left(\frac{\text{Dividends} + \text{Share Repurchases} - \text{Shares Issued}}{\text{Net Income}}\right)
$$

**Also known as:** QMJ, Quality Minus Junk, quality factor, quality composite.

**Args:**

- <u>growth_years (int, optional):</u> The number of years over which the growth and the
earnings volatility are measured. Defaults to 5, as in the paper.
- <u>trailing (int &#124; None, optional):</u> Sum the flows over this many periods. The window
counts calendar periods, so a period without a report makes it NaN. Defaults to
None, which is 4 for quarterly data (a trailing twelve months) and 1 otherwise.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the Toolkit (4 unless set
otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker and period the z-scores of Profitability, Growth, Safety
and Payout, and the Quality Score.

**Notes:**

- The scores are relative to the tickers given: AQR ranks every stock in the market,
while this ranks the tickers passed to the Toolkit, so pass a broad or comparable set
(at least three tickers, preferably many more). With fewer than three, it is empty.
- The growth measures need `growth_years` of earlier statements, so the first Quality
Score is `growth_years` after the first period (with quarterly data, plus the three
quarters of the first trailing year). Set an earlier start_date to obtain it.
- The paper measures growth as the change in profits per share scaled by the assets
of five years earlier; this takes the change in the profitability ratios themselves,
and it leaves out the idiosyncratic volatility of the safety component.
- A ticker without one of the components has no Quality Score.
- Asness, C. S., A. Frazzini and L. H. Pedersen, "Quality Minus Junk," Review of
Accounting Studies 24, 2019, pp. 34-112. Novy-Marx, R., "The Other Side of Value: The
Gross Profitability Premium," Journal of Financial Economics 108(1), 2013, pp. 1-28.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "GOOGL", "META", "NVDA", "INTC", "IBM", "ORCL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2016-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_quality_score().xs("Quality Score", level=1)
```

Which returns:

|       |    2019 |    2020 |    2021 |    2022 |    2023 |    2024 |     2025 |
|:------|--------:|--------:|--------:|--------:|--------:|--------:|---------:|
| AAPL  |  0.6124 |  0.6124 |  1.0206 |  1.4289 |  0.6124 |  0.6124 |   1.3363 |
| GOOGL | -1.0206 | -1.0206 |  0.2041 |  0.6124 |  1.0206 |  1.0206 |   0.8018 |
| IBM   | -1.4289 | -1.4289 | -0.6124 | -0.6124 | -0.6124 | -0.6124 |  -0.2673 |
| INTC  | -0.6124 | -0.6124 | -1.0206 | -1.4289 | -1.4289 | -1.4289 |  -1.3363 |
| META  |  1.0206 |  1.4289 |  1.4289 |  0.2041 | -0.2041 |  0.2041 |   0.2673 |
| MSFT  |  0.2041 |  1.0206 |  0.6124 |  1.0206 |  0.2041 | -0.2041 |  -0.8018 |
| NVDA  |  1.4289 |  0.2041 | -0.2041 | -0.2041 |  1.4289 |  1.4289 | nan      |
| ORCL  | -0.2041 | -0.2041 | -1.4289 | -1.0206 | -1.0206 | -1.0206 | nan      |

---

## get_accrual_quality
Calculate the accrual quality of Dechow and Dichev (2002): how well a company's working capital accruals map into its operating cash flows of the year before, the year itself and the year after. Accruals anticipate cash flows (a sale on credit is collected next year), so accruals that the cash flows do not explain are estimation errors; their standard deviation measures the quality of the accruals and of the earnings they are part of. A higher value means lower quality. Francis et al. (2005) found that companies with poor accrual quality have a higher cost of capital.

The regression is estimated per company over the `window` years before the period:

$$
\text{Delta WC} \;(t) = b_{0} + b_{1} \;\text{CFO} \;(t - 1) + b_{2} \;\text{CFO} \;(t) + b_{3} \;\text{CFO} \;(t + 1) + e (t)
$$

$$
\text{McNichols (2002)},\;\; \text{method} = \text{"mcnichols":} \;\text{Delta WC} \;(t) = b_{0} + b_{1} \;\text{CFO} \;(t - 1) + b_{2} \;\text{CFO} \;(t) + b_{3} \;\text{CFO} \;(t + 1) + b_{4} \Delta \;\text{Revenue} \;(t) + b_{5} \;\text{PP\&E} \;(t) + e (t)
$$

$$
\text{Accrual Quality} = \sigma(e),\;\; \text{the standard deviation of the residuals (ddof=1)}
$$

with ΔWC the increase in working capital (minus the Change in Working Capital of the cash flow statement: the change in receivables and inventory less the change in payables, taxes payable and other working capital) and every variable divided by the average total assets of its year.

For more information, see the following sources:

- Dechow, P. M. and Dichev, I. D. (2002). "The Quality of Accruals and Earnings: The Role of Accrual Estimation Errors." The Accounting Review, 77(Supplement), 35-59.
- McNichols, M. F. (2002). "Discussion of The Quality of Accruals and Earnings: The Role of Accrual Estimation Errors." The Accounting Review, 77(Supplement), 61-69.
- Francis, J., LaFond, R., Olsson, P. and Schipper, K. (2005). "The Market Pricing of Accruals Quality." Journal of Accounting and Economics, 39(2), 295-327.

**Also known as:** Dechow-Dichev model, accruals quality, AQ, DD model, McNichols model.

**Args:**

- <u>method (str, optional):</u> "dechow_dichev" or "mcnichols" (adds the change in revenue and
the property, plant and equipment). Defaults to "dechow_dichev".
- <u>window (int, optional):</u> The number of years every regression is estimated on. Dechow
and Dichev required at least 8 years per company. Defaults to 8.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker and period the Working Capital Accruals and the Cash Flow from
Operations (both over the average total assets) and the Accrual Quality.

**Notes:**

- No look-ahead: the regression needs the cash flow of the year after each accrual, so the
Accrual Quality of period T uses the accruals of the `window` years up to T - 1, whose
next-year cash flow is known at T at the latest. It therefore needs `window` + 2 years of
statements: set a start_date at least that many years back.
- Dechow and Dichev estimate one regression per company over its whole history and
Francis et al. (2005) estimate them per industry and year; this rolls a regression per
company over the window, so the measure is known at each period.
- On quarterly data the flows are summed over the trailing twelve months and the years of
the regression are four quarters apart.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2010-01-01",
    end_date="2025-12-31",
)

# The last six years, each estimated on the eight years before it
toolkit.models.get_accrual_quality().xs("Accrual Quality", level=1).iloc[:, -6:]
```

Which returns:

|      |   2020 |   2021 |   2022 |   2023 |   2024 |   2025 |
|:-----|-------:|-------:|-------:|-------:|-------:|-------:|
| AAPL | 0.0295 | 0.0282 | 0.0291 | 0.0199 | 0.0216 | 0.0216 |
| MSFT | 0.0546 | 0.054  | 0.0346 | 0.0352 | 0.0225 | 0.0197 |

---

## get_earnings_attributes
Calculate the accounting-based earnings attributes of Francis, LaFond, Olsson and Schipper (2004): the persistence, predictability and smoothness of a company's earnings over the past years. Persistent and predictable earnings are more useful to forecast with, and the paper finds that companies with less favourable attributes have a higher cost of equity. Together with the accrual quality (`get_accrual_quality`) they are the paper's accounting attributes.

The formula is as follows, each over the `window` years up to the period:

$$
\text{Persistence} = \phi 1 \;\text{of the regression EPS} \;(t) = \phi 0 + \phi 1 \;\text{EPS} \;(t - 1) + \nu (t)
$$

$$
\text{Predictability} = \sqrt{\sigma^{2}(\nu)},\;\; \text{the square root of the error variance of that regression},\;\; \sqrt{\frac{\sum \nu^{2}}{N - 2}}
$$

$$
\text{Smoothness} = \frac{\sigma\left(\frac{\text{Net Income} \;(t)}{\text{Total Assets} \;(t - 1)}\right)}{\sigma\left(\frac{\text{Cash Flow from Operations} \;(t)}{\text{Total Assets} \;(t - 1)}\right)},\;\; \text{the standard deviations with ddof=1}
$$

with EPS the net income from continuing operations (the earnings before extraordinary items of the paper) over the weighted average shares. A persistence near 1 means earnings shocks last; larger predictability and smoothness values mean less predictable and less smooth earnings (as in the paper, larger values are less desirable).

For more information, see the following sources:

- Francis, J., LaFond, R., Olsson, P. M. and Schipper, K. (2004). "Costs of Equity and Earnings Attributes." The Accounting Review, 79(4), 967-1010.

**Also known as:** earnings persistence, earnings predictability, earnings smoothness, earnings quality attributes, Francis LaFond Olsson Schipper.

**Args:**

- <u>window (int, optional):</u> The number of years of every window; the paper uses 10.
Defaults to 10.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker and period the Persistence, Predictability and Smoothness.

**Notes:**

- The windows only use the years up to the period (no look-ahead) and need every one of
them, plus the year before for the lagged EPS and the beginning total assets: set a
start_date at least `window` + 1 years back.
- The net income from continuing operations falls back on the net income where the
statements do not report it.
- On quarterly data the flows are summed over the trailing twelve months and the years of
the window are four quarters apart.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2010-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_earnings_attributes()
```

Which returns:

|                            |    2018 |    2019 |   2020 |   2021 |   2022 |   2023 |   2024 |   2025 |
|:---------------------------|--------:|--------:|-------:|-------:|-------:|-------:|-------:|-------:|
| ('AAPL', 'Persistence')    |  0.9719 |  0.8779 | 0.8644 | 1.3562 | 1.1528 | 0.9926 | 0.9229 | 1.015  |
| ('AAPL', 'Predictability') |  0.3459 |  0.3408 | 0.3384 | 0.7336 | 0.7608 | 0.7721 | 0.7744 | 0.8457 |
| ('AAPL', 'Smoothness')     |  0.7622 |  0.7474 | 0.7391 | 0.8799 | 0.8643 | 0.9365 | 0.9284 | 1.1048 |
| ('MSFT', 'Persistence')    | -0.0581 | -0.3582 | 0.6982 | 1.1725 | 1.1663 | 1.0312 | 1.0803 | 1.0464 |
| ('MSFT', 'Predictability') |  0.5798 |  1.0244 | 1.2588 | 1.4298 | 1.3595 | 1.4282 | 1.4569 | 1.2686 |
| ('MSFT', 'Smoothness')     |  1.2413 |  1.2008 | 1.2202 | 1.1846 | 1.5726 | 1.616  | 1.4189 | 1.3102 |

---

## get_graham_criteria
Calculate the seven criteria Benjamin Graham sets for the stocks of the defensive investor in The Intelligent Investor (chapter 14), with the number met: an adequate size, a strong financial condition, earnings stability, a dividend record, earnings growth, a moderate price to earnings and a moderate price to assets. Graham meant them as a minimum of quality and a maximum of price for an investor who does not want to analyse companies in depth.

The formula is as follows:

$$
\text{Adequate Size:}\;\; \text{Revenue} \geq \text{minimum\_revenue}
$$

$$
\text{Strong Financial Condition:}\;\; \text{Current Assets} \geq 2 \cdot \text{Current Liabilities and Long Term Debt} \leq \text{Current Assets} - \text{Current Liabilities} \;(\text{net current assets})
$$

- Earnings Stability: a positive Net Income in each of the past 10 years

- Dividend Record: dividends paid in each of the past 20 years

- Earnings Growth: the average EPS of the last 3 years at least a third above the average EPS of the 3 years ending ten years earlier

$$
\text{Moderate Price to Earnings:}\;\; \text{Price} \leq 15 \cdot \text{the average EPS of the last 3 years}
$$

$$
\text{Moderate Price to Assets:}\;\; \frac{\frac{\text{Price}}{\text{Earnings}} \cdot \text{Price}}{\text{Book Value}} \leq 22.5,\;\; \text{with the earnings the average EPS of the last 3 years (Graham's 15 times earnings and 1.5 times book value, a lower multiple of the one allowing a higher multiple of the other)}
$$

$$
\text{Criteria Met} = \text{the number of criteria met};\;\; \text{Criteria Evaluated} = \text{the number that could be evaluated}
$$

Every criterion is 1 when met, 0 when not and NaN when the statements do not go back far enough (the dividend record needs 20 years of statements, the earnings growth 13).

For more information, see the following sources:

- Graham, B. (1973). "The Intelligent Investor." Harper & Row, 4th revised edition, chapter 14 (Stock Selection for the Defensive Investor).

**Also known as:** Graham defensive investor criteria, Graham screen, Graham's seven criteria, defensive stock selection.

**Args:**

- <u>minimum_revenue (float, optional):</u> The yearly revenue of the size criterion, in the
reporting currency. Graham asked for at least $100 million of sales for an
industrial company in 1971, about $800 million in 2025 prices (the US consumer price
index rose about eightfold). Defaults to 800,000,000.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker and period the seven criteria (1, 0 or NaN), Criteria Met and
Criteria Evaluated.

**Notes:**

- Graham's criteria for public utilities differ (debt below twice the equity at book
value instead of the current ratio); these are the criteria for industrial companies.
- The price is the close at the end of the fiscal period (traded, adjusted for splits),
the EPS the diluted EPS and the book value the Total Shareholder Equity over the diluted
weighted average shares. The dividend record counts a year with dividends paid on the
cash flow statement.
- On quarterly data the flows are summed over the trailing twelve months and the years
are four quarters apart.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["KO", "JNJ", "PG"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2000-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_graham_criteria().loc["KO"].iloc[:, -3:]
```

Which returns:

|                            |   2023 |   2024 |   2025 |
|:---------------------------|-------:|-------:|-------:|
| Adequate Size              |      1 |      1 |      1 |
| Strong Financial Condition |      0 |      0 |      0 |
| Earnings Stability         |      1 |      1 |      1 |
| Dividend Record            |      1 |      1 |      1 |
| Earnings Growth            |      0 |      0 |      1 |
| Moderate Price to Earnings |      0 |      0 |      0 |
| Moderate Price to Assets   |      0 |      0 |      0 |
| Criteria Met               |      3 |      3 |      4 |
| Criteria Evaluated         |      7 |      7 |      7 |

---

## get_accruals_ratio
Calculate the accruals ratios: the part of earnings that is not backed by cash, relative to the average of the total assets at the start and the end of the year. Richard Sloan showed that earnings driven by accruals are less persistent than cash earnings and that companies with high accruals earn lower future returns (the accrual anomaly).

- Balance Sheet Accruals Ratio = [(ΔCurrent Assets - ΔCash) - (ΔCurrent Liabilities - ΔShort-term Debt - ΔTaxes Payable) - Depreciation] / Average Total Assets
- Cash Flow Accruals Ratio = (Net Income - Cash Flow from Operations - Cash Flow from Investing) / Average Total Assets

The balance sheet version is Sloan's (1996). The cash flow version, earnings minus free cash flow, takes the accruals from the cash flow statement instead: Hribar and Collins (2002) showed that balance sheet changes misstate accruals when a company acquires, divests or discontinues operations (their own measure is earnings before extraordinary items minus cash flow from operations), and subtracting the investing cash flow as well counts the investment in long-term operating assets as an accrual, as the broad accruals of Richardson, Sloan, Soliman and Tuna (2005) do. Values near zero or negative are a sign of high earnings quality.

For more information, see the following papers:

- Sloan, R.G. (1996). "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows about Future Earnings?" The Accounting Review, 71(3), 289-315.
- Hribar, P. and Collins, D.W. (2002). "Errors in Estimating Accruals: Implications for Empirical Research." Journal of Accounting Research, 40(1), 105-134.
- Richardson, S.A., Sloan, R.G., Soliman, M.T. and Tuna, I. (2005). "Accrual Reliability, Earnings Persistence and Stock Prices." Journal of Accounting and Economics, 39(3), 437-485.

**Also known as:** Sloan ratio, accrual ratio, earnings quality ratio.

**Args:**

- <u>trailing (int &#124; None, optional):</u> Sum the flows over this many periods (e.g. 4
quarters, a trailing twelve months) and compare with the values `trailing`
periods back, so that with quarterly data every change is year over year.
Balance sheet items are taken at the period end. The window counts calendar
periods, so a period without a report makes it NaN. Defaults to None, which
is 4 for quarterly data (a year) and 1 otherwise; pass 1 for quarterly data
to compare quarter over quarter.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker and period the Balance Sheet Accruals Ratio and the Cash
Flow Accruals Ratio.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_accruals_ratio()
```

Which returns:

|                                          |    2021 |    2022 |    2023 |    2024 |    2025 |
|:-----------------------------------------|--------:|--------:|--------:|--------:|--------:|
| ('AAPL', 'Balance Sheet Accruals Ratio') | -0.1047 | -0.0446 | -0.0115 | -0.0285 | -0.108  |
| ('AAPL', 'Cash Flow Accruals Ratio')     |  0.0154 |  0      | -0.0489 | -0.0765 | -0.0405 |
| ('MSFT', 'Balance Sheet Accruals Ratio') | -0.0687 | -0.1109 | -0.0683 | -0.1017 | -0.0735 |
| ('MSFT', 'Cash Flow Accruals Ratio')     |  0.0381 |  0.0401 |  0.0192 |  0.144  |  0.0677 |

---

## get_discretionary_accruals
Calculate the discretionary accruals of the modified Jones model, the part of a company's accruals that its change in revenues and its fixed assets do not explain and that is therefore attributed to management's discretion. Jones (1991) modelled the accruals a company needs as a function of its change in revenues (working capital moves with sales) and its property, plant and equipment (depreciation). Dechow, Sloan and Sweeney (1995) subtracted the change in receivables from the change in revenues, because revenue booked on credit can itself be managed, and found this modified model the most powerful at detecting earnings management. Large positive discretionary accruals point at earnings that were managed up.

The formula is as follows:

$$
\text{Total Accruals} = \frac{\text{Net Income} - \text{Cash Flow from Operations}}{\text{Total Assets}(t-1)}
$$

$$
\text{Estimation:}\;\; \text{Total Accruals} = \frac{a_{1} \cdot 1}{A(t-1)} + \frac{a_{2} \cdot \Delta \;\text{Revenue}}{A(t-1)} + \frac{a_{3} \cdot \text{PPE}}{A(t-1)} + e
$$

$$
\text{Non-Discretionary Accruals} = \frac{a_{1} \cdot 1}{A(t-1)} + \frac{a_{2} \cdot (\Delta \;\text{Revenue} - \Delta \;\text{Receivables})}{A(t-1)} + \frac{a_{3} \cdot \text{PPE}}{A(t-1)}
$$

$$
\text{Discretionary Accruals} = \text{Total Accruals} - \text{Non-Discretionary Accruals}
$$

Here A(t-1) is the total assets at the start of the year, ΔRevenue and ΔReceivables the changes over the year and PPE the property, plant and equipment at the end of it. The coefficients a1, a2 and a3 are estimated with ordinary least squares without an intercept, as in Jones (1991); with intercept=True a constant a0 is added to the estimation and the Non-Discretionary Accruals (Kothari, Leone and Wasley, 2005).

For more information, see the following papers:

- Jones, J.J. (1991). "Earnings Management During Import Relief Investigations." Journal of Accounting Research, 29(2), 193-228.
- Dechow, P.M., Sloan, R.G. and Sweeney, A.P. (1995). "Detecting Earnings Management." The Accounting Review, 70(2), 193-225.
- Kothari, S.P., Leone, A.J. and Wasley, C.E. (2005). "Performance Matched Discretionary Accrual Measures." Journal of Accounting and Economics, 39(1), 163-197.

**Also known as:** modified Jones model, abnormal accruals, Jones model, earnings management.

**Args:**

- <u>method (str, optional):</u> How the coefficients are estimated. "time_series"
estimates them for every year on the company's own earlier years, as Jones
(1991) and Dechow, Sloan and Sweeney (1995) did, with the change in revenues
in the estimation and the change in receivables subtracted only for the year
itself. "cross_section" estimates them per year across the tickers of the
Toolkit, with the change in revenues minus the change in receivables in the
estimation as well, which is meaningful with many companies of one industry.
Defaults to "time_series".
- <u>min_observations (int, optional):</u> The fewest observations a regression is
estimated on: earlier years of the company with "time_series", tickers with
"cross_section". At least 3, the number of coefficients. Defaults to 10, the
minimum estimation period of Dechow, Sloan and Sweeney (1995).
- <u>intercept (bool, optional):</u> Whether to add a constant to the regression, as
Kothari, Leone and Wasley (2005) do, in both methods. It removes the average
level of the accruals from the other coefficients at the cost of a degree of
freedom (one observation more is needed). Defaults to False, the formulation
of Jones (1991) and Dechow, Sloan and Sweeney (1995).
- <u>trailing (int &#124; None, optional):</u> Sum the flows over this many periods (e.g. 4
quarters, a trailing twelve months) and compare with the values `trailing`
periods back, so that with quarterly data every change is year over year.
Balance sheet items are taken at the period end. The window counts calendar
periods, so a period without a report makes it NaN. Defaults to None, which
is 4 for quarterly data (a year) and 1 otherwise; pass 1 for quarterly data
to compare quarter over quarter.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker and period the Total Accruals, Non-Discretionary
Accruals and Discretionary Accruals, as a share of the total assets at the start
of the period. The last two are NaN where fewer than `min_observations`
observations are available.

**Notes:**

- Total accruals are Net Income minus Cash Flow from Operations, the cash flow form
of Hribar and Collins (2002) that the Beneish M-Score's Total Accruals to Total
Assets also uses; Jones (1991) and Dechow, Sloan and Sweeney (1995) derived them
from balance sheet changes, which misstate them around acquisitions and
divestitures.
- Jones (1991) uses gross property, plant and equipment. Where a company's
statements report no gross amount (Financial Modeling Prep's do not), the net
amount is used in every year, as switching between the two would move the ratio.
- The time series design estimates every year on the years before it only (an
expanding window ending a year earlier), so there is no look-ahead. With the
default of 10 observations, the first discretionary accruals are in the twelfth
year of statements (a year for the beginning assets and ten to estimate on), so set
a `start_date` well over a decade back; the Toolkit's data plan may cover fewer
years, in which case only the Total Accruals are returned. Lowering
`min_observations` gives earlier but noisier estimates.
- The cross-section design uses the companies of the same year, so it needs at
least `min_observations` tickers that report every input. Many later papers
estimate it per industry and year and add an intercept (Kothari, Leone and
Wasley, 2005), which `intercept=True` does.
- Without an intercept the PPE term carries the average level of the accruals, so a
company whose PPE intensity or size trends away from its estimation years gets
discretionary accruals of one sign. In the example below AAPL's and MSFT's PPE
averaged about 0.11 of their beginning assets in the estimation years and is 0.15
to 0.17 (AAPL) and 0.24 to 0.45 (MSFT) in the years shown, where their
discretionary accruals are positive in every year. `intercept=True` removes this
level bias within the estimation years at the cost of a degree of freedom, and
gives both companies discretionary accruals of either sign in these years.
- The expanding window of the time series design starts at the first year loaded,
so the estimates, and with them the discretionary accruals, depend on the
`start_date` of the Toolkit.
- On quarterly data the flows are summed over the trailing twelve months and the
time series estimation uses the same quarter of earlier years, so that the
observations do not overlap.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2005-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_discretionary_accruals().loc[:, "2021":]
```

Which returns:

|                                        |    2021 |    2022 |    2023 |    2024 |    2025 |
|:---------------------------------------|--------:|--------:|--------:|--------:|--------:|
| ('AAPL', 'Total Accruals')             | -0.0289 | -0.0637 | -0.0384 | -0.0695 |  0.0014 |
| ('AAPL', 'Non-Discretionary Accruals') | -0.1208 | -0.084  | -0.0696 | -0.0707 | -0.0794 |
| ('AAPL', 'Discretionary Accruals')     |  0.0919 |  0.0203 |  0.0312 |  0.0012 |  0.0808 |
| ('MSFT', 'Total Accruals')             | -0.0513 | -0.0488 | -0.0417 | -0.0738 | -0.067  |
| ('MSFT', 'Non-Discretionary Accruals') | -0.1076 | -0.0973 | -0.1047 | -0.0961 | -0.1061 |
| ('MSFT', 'Discretionary Accruals')     |  0.0563 |  0.0485 |  0.063  |  0.0223 |  0.039  |

---

## get_enterprise_value_breakdown
Calculate the Enterprise Value (EV) breakdown, providing a detailed view of its components.

The Enterprise Value breakdown includes the following components for each quarter or year:

- Share Price: The market price per share of the company's stock.
- Market Capitalization (Market Cap): The total value of a company's outstanding common shares, i.e. the share price multiplied by the shares outstanding. Preferred shares are excluded here and enter as their own component below, so that they are counted once rather than twice.
- Debt: The sum of long-term and short-term debt on the company's balance sheet.
- Preferred Equity: The value of preferred shares, if applicable.
- Minority Interest: The equity value of a subsidiary with less than 50% ownership.
- Cash and Cash Equivalents: The cash and the investments that are readily convertible to cash within three months, such as money market funds and Treasury bills.
- Short Term Investments: The marketable securities that are not cash equivalents.

Cash and marketable securities are deducted together (Damodaran), the same Enterprise Value as toolkit.ratios.get_enterprise_value returns.

The formula is as follows:

$$
\text{Market Capitalization} = \text{Share Price} \cdot \text{Weighted Average Shares Diluted} \;(\text{Weighted Average Shares when diluted} = \text{False}),\;\; \text{with the share price the traded close at the end of each quarter or year}
$$

$$
\text{Enterprise Value} = \text{Market Capitalization} + \text{Total Debt} + \text{Preferred Equity} + \text{Minority Interest} - \text{Cash and Cash Equivalents} - \text{Short Term Investments}
$$

This breakdown is displayed in a DataFrame for each company and includes the option to show growth values as well.

**Also known as:** EV breakdown, enterprise value components, EV bridge.

**Args:**

- <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the Enterprise Value breakdown, including the calculated components.

**Notes:**

- All the inputs must be in the same currency and unit for accurate calculations.
- The Enterprise Value is an important metric used for valuation and investment analysis.
It represents the cost of acquiring the entire business: the equity is bought at its market
value, the debt (and any preferred equity and minority interest) is assumed, and the acquired
cash reduces the effective price, which is why cash is subtracted rather than added.
- Enterprise Value is positive for essentially every going concern. It only turns negative
when a company's cash exceeds its market capitalization plus its debt, which is a sign of a
cash-rich balance sheet priced below its net cash — not of financial distress. A distressed,
heavily indebted company shows the opposite: an Enterprise Value far above its market
capitalization.
- Understanding the Enterprise Value breakdown can provide insights into the sources of a
company's value and potential risks.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["F"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_enterprise_value_breakdown().loc[
    ["Market Capitalization", "Total Debt", "Cash and Cash Equivalents", "Enterprise Value"]
]
```

Which returns:

|                           |        2021 |        2022 |        2023 |        2024 |        2025 |
|:--------------------------|------------:|------------:|------------:|------------:|------------:|
| Market Capitalization     | 8.37862e+10 | 4.66828e+10 | 4.92598e+10 | 3.98079e+10 | 5.22045e+10 |
| Total Debt                | 1.39485e+11 | 1.40474e+11 | 1.51107e+11 | 1.60862e+11 | 1.67573e+11 |
| Cash and Cash Equivalents | 2.054e+10   | 2.5134e+10  | 2.4862e+10  | 2.2935e+10  | 2.3356e+10  |
| Enterprise Value          | 1.73781e+11 | 1.43012e+11 | 1.60221e+11 | 1.62345e+11 | 1.81318e+11 |

---

## get_tobins_q_ratio
Calculate Tobin's Q Ratio, a valuation metric developed by economist James Tobin that compares the market value of a company to the cost of replacing its assets.

The formula is as follows:

$$
\text{Market Value of Equity} = \text{Share Price} \cdot \text{Total Shares Outstanding}
$$

$$
\text{Tobin's}\; Q \;\text{Ratio} = \frac{\text{Market Value of Equity} + \text{Total Liabilities}}{\text{Total Assets}}
$$

Tobin's Q Ratio can be interpreted as follows:

- A Q ratio greater than 1 indicates that the market values the company above the cost of replacing its assets, which can reflect growth expectations, unrecognized intangible value, or overvaluation.
- A Q ratio less than 1 indicates that the market values the company below the cost of replacing its assets, which can reflect undervaluation or declining growth prospects.

Because the book value of assets leaves out most intangibles (brands, software, research), companies built on them show a Q far above 1 without being overvalued in Tobin's sense, so the ratio is most informative within an industry and over time. In macroeconomics the aggregate Q of the corporate sector is read as a signal for investment: a Q above 1 makes new capital worth more than it costs.

**Also known as:** Tobin's Q, Q ratio.

**Args:**

- <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the Market Value of Equity, Total Liabilities,
Total Assets and Tobin's Q Ratio.

**Notes:**

- This implementation approximates the market value of debt with the book value of
Total Liabilities, and the replacement cost of assets with the book value of Total
Assets, consistent with the simplifications used in the Weighted Average Cost of
Capital calculation elsewhere in this module.
- The market value of equity (the share price at the end of the fiscal period times the
period's weighted average shares) and the balances are taken at the end of the period,
the same date, on yearly and quarterly data alike.

References:
- Tobin, James. "A General Equilibrium Approach to Monetary Theory." Journal of Money,
Credit and Banking, Vol. 1, No. 1, 1969, pp. 15-29.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["INTC", "QCOM", "TXN"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_tobins_q_ratio().xs("Tobin's Q Ratio", level=1)
```

Which returns:

|      |   2021 |   2022 |   2023 |   2024 |   2025 |
|:-----|-------:|-------:|-------:|-------:|-------:|
| INTC | 1.6797 | 1.0312 | 1.5308 | 0.9076 | 1.178  |
| QCOM | 4.3523 | 3.2533 | 3.0273 | 4.0076 | 4.3057 |
| TXN  | 7.6086 | 6.0875 | 5.3046 | 5.3769 | 5.1094 |

---

## get_weighted_average_cost_of_capital
The Weighted Average Cost of Capital (WACC) is a financial metric used to estimate the cost of capital for a company. It represents the average rate of return a company must pay to its investors for using their capital. WACC takes into account the cost of both equity and debt, weighted by their respective proportions in the company's capital structure.

The formula is as follows:

$$
\text{Market Value of Equity} = \text{Share Price} \cdot \text{Total Shares Outstanding}
$$

$$
\text{Market Value of Debt} = \text{Total Debt}
$$

$$
\text{Total Market Value} = \text{Market Value of Equity} + \text{Market Value of Debt}
$$

$$
\text{Cost of Equity} = \text{Risk Free Rate} + \text{Beta} \cdot \text{Market Risk Premium}
$$

$$
\text{Cost of Debt} = \frac{\text{Interest Expense}}{\text{Total Debt}}
$$

$$
\text{WACC} = \frac{\text{Market Value of Equity}}{\text{Total Market Value}} \cdot \text{Cost of Equity} + \frac{\text{Market Value of Debt}}{\text{Total Market Value}} \cdot \text{Cost of Debt} \cdot (1 - \text{Corporate Tax Rate})
$$

Cost of Equity (Re): The cost of equity represents the return required by the company's shareholders or equity investors. It is the cost of raising funds by selling equity (such as common stock). The cost of equity is often estimated using methods like the Capital Asset Pricing Model (CAPM) or the Dividend Discount Model (DDM).

Cost of Debt (Rd): The cost of debt is the interest rate the company pays on its outstanding debt. It is the cost of raising funds through borrowing, such as issuing bonds or taking loans. The cost of debt is typically based on the prevailing interest rates in the market and the company's creditworthiness.

Corporate Tax Rate (Tc): The corporate tax rate is the percentage of a company's profits that is paid in taxes. It is used to calculate the tax shield on interest payments. Interest expenses on debt reduce taxable income, and the tax shield represents the tax savings resulting from these deductions.

Market Value of Equity (E): The market value of equity is the total value of the company's outstanding shares of common stock. It is calculated by multiplying the current stock price by the number of shares outstanding.

Market Value of Debt (D): The market value of debt is the total value of the company's outstanding debt obligations, such as bonds and loans. It represents the current market price of the debt instruments.

Total Market Value of Capital (V): The total market value of capital is the sum of the market value of equity and the market value of debt ($$V = E + D$$). It represents the total value of the company's financing, both through equity and debt.

The WACC is the discount rate for the free cash flow to the firm and the hurdle rate for new investments, so analysts usually build it from forward-looking inputs: a long-term government bond yield, an equity risk premium of a few percent, a beta measured over several years and the yield on the company's debt. Small changes matter: in a DCF with 2.5% perpetual growth, moving the WACC from 8% to 9% lowers the terminal value by about 15%.

**Also known as:** WACC, blended cost of capital, discount rate.

**Args:**

- <u>show_full_results (bool, optional):</u> Whether to show the full results or just the WACC values.
Defaults to True.
- <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. The window counts
calendar periods, so a period without a report makes it NaN. Defaults to None.
- <u>market_risk_premium (float &#124; None, optional):</u> The annual equity risk premium the Cost of Equity
uses. Defaults to None, which takes the equity risk premium of each company's country
(Damodaran's Total Equity Risk Premium, see get_market_risk_premium) and, where that is
not available, the benchmark's average return above the risk-free rate over the data.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the WACC values.

**Notes:**

- The Cost of Equity follows from the Capital Asset Pricing - <u>Model (CAPM):</u> the risk-free rate of
the period plus Beta times the market risk premium. That premium defaults to the equity risk
premium of the company's country (Damodaran's Total Equity Risk Premium, about 4.5% for the
United States), today's premium for every period, as the source keeps no history. Without it (no API key, or a country the
table does not cover) it is the benchmark's average return above the risk-free rate over the
data, which a short or strong sample makes large: about 15% a year for the S&P 500 over
2022-2026. Set `market_risk_premium` to use one premium for every company. Beta is estimated
from the period's daily returns. With quarterly data the rates are per quarter, the risk-free yield divided by four.
- With `trailing` set, the Interest Expense is summed over the trailing periods, so the Cost of
Debt covers that span, the risk-free rate and premium of the Cost of Equity are the per-period
rates times `trailing` and the Beta is estimated from the daily returns of the trailing periods.
With quarterly data and trailing=4, every rate is an annual rate on a year of daily returns.
- The Market Value of Debt is approximated as the Total Debt.
- The capital weights are taken at the end of the fiscal period, also with `trailing` set: the
Market Value of Equity is the closing share price on that day times the period's weighted
average shares, and the debt is the Total Debt on the balance sheet of that day.
- The Cost of Debt is the Interest Expense divided by the Total Debt at the end of the period,
so debt raised or repaid during the period moves it away from the rate on the average debt
outstanding. A period with debt but an Interest Expense of 0 (financial statements that
include the interest in another line item or leave it out) has an unknown Cost of Debt, so
its Cost of Debt and Weighted Average Cost of Capital are NaN rather than a WACC that treats
the debt as free. Without any debt the WACC is the Cost of Equity.
- The Corporate Tax Rate is the effective tax rate (Income Tax Expense / Income Before Tax),
kept within 0 and 1 so that a tax benefit does not turn the tax shield negative, and 0 for a
period without a pre-tax profit, which leaves no taxable income for the interest to shield.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["VZ", "T", "TMUS"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2022-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_weighted_average_cost_of_capital().xs(
    "Weighted Average Cost of Capital", level=1
)
```

Which returns:

|      |   2022 |   2023 |   2024 |   2025 |
|:-----|-------:|-------:|-------:|-------:|
| T    | 0.0453 | 0.0457 | 0.0358 | 0.0411 |
| TMUS | 0.0469 | 0.0437 | 0.0447 | 0.0425 |
| VZ   | 0.0304 | 0.0407 | 0.036  | 0.0377 |

---

## get_implied_cost_of_capital
Calculate Easton's (2004) implied cost of equity capital, the expected rate of return on equity at which the share price equals the value of the next two years of earnings expected by analysts. Where the Cost of Equity of `get_weighted_average_cost_of_capital` is the return the Capital Asset Pricing Model (CAPM) requires from a beta and a market risk premium, this is the return the market price itself implies (ex-ante).

The formula is as follows:

$$
\text{PEG:}\;\; r = \sqrt{\frac{\text{EPS}_{2} - \text{EPS}_{1}}{P_{0}}}
$$

$$
\text{MPEG:}\;\; r = A + \sqrt{A^{2} + \frac{\text{EPS}_{2} - \text{EPS}_{1}}{P_{0}}}
$$

$$
A = \frac{\text{DPS}_{1}}{2 \cdot P_{0}}
$$

Where $$\text{EPS}_{1}$$ and $$\text{EPS}_{2}$$ are the analyst consensus (average) EPS estimates of the two fiscal years after the period, $$P_{0}$$ the share price at the end of the period and $$\text{DPS}_{1}$$ the dividends per share of the next year. The MPEG rate is the positive root of Easton's valuation equation $$P_{0} = \text{EPS}_{1} / r + (\text{EPS}_{2} + r \times \text{DPS}_{1} - (1 + r) \times \text{EPS}_{1}) / r^{2}$$, which assumes the abnormal growth in earnings stays constant after the second year; the PEG rate leaves the dividends out ($$\text{DPS}_{1} = 0$$). The rate is a yearly rate, annually compounded.

See: Easton, P. D. (2004). PE Ratios, PEG Ratios, and Estimating the Implied Expected Rate of Return on Equity Capital. The Accounting Review, 79(1), 73-95.

The estimates are the analysts' consensus from FinancialModelingPrep, the same estimates as `get_forward_price_earnings_ratio` of the Ratios module uses, which requires an `api_key` and a Premium FMP subscription. They are fetched once per Toolkit instance. These are the current analyst estimates, also for past periods, so the result of every period, the example below included, changes as analysts revise their estimates.

**Also known as:** implied cost of capital, ICC, PEG / MPEG cost of equity, Easton model.

**Args:**

- <u>modified (bool, optional):</u> Whether to return the MPEG rate, which includes the
dividends and is the version Easton prefers, instead of the PEG rate. Defaults to
True.
- <u>min_analysts (int &#124; None, optional):</u> The minimum number of analysts behind the EPS
consensus of an estimate period; a period that relies on one covered by fewer is
NaN. The number per period is the "Number of Analysts EPS" of
`Toolkit.get_analyst_estimates`. Defaults to None, which keeps every period.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The implied cost of equity capital per ticker (rows) and fiscal period
(columns) as a decimal.

**Notes:**

- $$\text{EPS}_{1}$$ and $$\text{EPS}_{2}$$ of a fiscal year are the consensus estimates of the next two fiscal years.
On quarterly data each is a year of estimates, as in the forward P/E: $$\text{EPS}_{1}$$ the sum of the
estimates of the four quarters after the period and $$\text{EPS}_{2}$$ that of the four quarters after
those.
- $$P_{0}$$ is the traded close (adjusted for splits, not for dividends) on the last trading day up
to the end of the fiscal period, as the other market values of the Models module.
- $$\text{DPS}_{1}$$ is the dividends per share paid over the year up to the end of the fiscal period.
FinancialModelingPrep has no dividend forecasts, and Easton allows the current dividend in
their place; a growth assumption on top would add an input the data does not give. The
dividends move the rate little: A is half the dividend yield.
- The rate is NaN where the estimated earnings do not grow ($$\text{EPS}_{2} \leq \text{EPS}_{1}$$), the price is not
positive or an estimate is missing: the model has no real, positive rate there, so it is
never shown as 0.
- FinancialModelingPrep keeps the latest consensus for every fiscal year, not the consensus as
it stood at the end of each period, so for past periods the estimates may include later
revisions, the same as the forward P/E. Only the latest periods are ex-ante estimates;
earlier ones show the rate the price implied for the earnings now expected for those years.
- On quarterly data FinancialModelingPrep gives estimates for the coming quarters only, and a
rate needs eight quarters of estimates after its period, so only the latest periods have one.
- Without daily data from a year before the start date, the dividends of the first periods
cover less than a year, which is logged.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["KO", "PEP", "MDLZ"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_implied_cost_of_capital()
```

Which returns:

|      |   2021 |   2022 |     2023 |   2024 |   2025 |
|:-----|-------:|-------:|---------:|-------:|-------:|
| KO   | 0.0736 | 0.0665 |   0.0665 | 0.0927 | 0.0679 |
| MDLZ | 0.0793 | 0.0653 | nan      | 0.0695 | 0.0944 |
| PEP  | 0.0803 | 0.071  | nan      | 0.0641 | 0.0589 |

---

## get_economic_value_added
Economic Value Added (EVA) is a measure of a company's financial performance that represents the value created in excess of the required return of the company's capital providers. It captures whether a company is generating returns above its true cost of capital, which distinguishes it from purely accounting-based measures such as Net Income.

The formula is as follows:

$$
\text{NOPAT} = \text{EBIT} \cdot (1 - \text{Corporate Tax Rate})
$$

$$
\text{Invested Capital} = \text{Total Equity} + \text{Total Debt}
$$

$$
\text{Return on Invested Capital} = \frac{\text{NOPAT}}{\text{Invested Capital}}
$$

$$
\text{EVA Spread} = \text{Return on Invested Capital} - \text{Weighted Average Cost of Capital}
$$

$$
\text{EVA} = \text{NOPAT} - (\text{Weighted Average Cost of Capital} \cdot \text{Invested Capital}) = \text{EVA Spread} \cdot \text{Invested Capital}
$$

EVA is mostly used to compare value creation across business units or companies and over time, and as a basis for management compensation. It is equivalent to (Return on Invested Capital - WACC) * Invested Capital, so a company with a high return on capital but a small capital base can create less EVA than a larger, less profitable one.

The EVA Spread, the return on capital above its cost (Stewart, 1991), compares value creation between companies of different sizes.

For more information, see the following sources:

- Stewart, G. B. (1991). "The Quest for Value." HarperBusiness.
- Stern, J. M., Stewart, G. B. and Chew, D. H. (1995). "The EVA Financial Management System." Journal of Applied Corporate Finance, 8(2), 32-46.

**Also known as:** EVA, economic profit, EVA spread, economic spread, ROIC minus WACC.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The number of periods to sum the flows (EBIT, taxes)
over, with the Total Equity and Total Debt averaged over the trailing + 1 period ends
that open and close those periods, so trailing=1 equals the default average of the
opening and closing balance. E.g. 4 with quarterly data gives the trailing twelve
months (TTM). The window counts calendar periods, so a period without a report makes
it NaN. Defaults to None.
- <u>market_risk_premium (float &#124; None, optional):</u> The annual equity risk premium the Cost of Equity
uses. Defaults to None, which takes the equity risk premium of each company's country
(Damodaran's Total Equity Risk Premium, see get_market_risk_premium) and, where that is
not available, the benchmark's average return above the risk-free rate over the data.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the EVA and its components: NOPAT, Invested Capital, the
WACC, the Return on Invested Capital, the EVA Spread and the EVA.

**Notes:**

- A positive EVA indicates that the company is generating returns in excess of its cost of
capital, i.e. it is creating value for its capital providers. A negative EVA indicates the
company is destroying value.
- EBIT is the reported Operating Income, as in the other models of this module and the
EBIT based ratios of the Ratios module.
- The Corporate Tax Rate is the effective tax rate (Income Tax Expense / Income Before Tax)
kept within 0 and 1, and 0 for a period without a pre-tax profit, the same rate the
Weighted Average Cost of Capital uses (see `get_weighted_average_cost_of_capital`).
- Invested Capital is the sum of the average Total Equity and the average Total Debt over
the period ends that open and close the period (the trailing + 1 period ends with
`trailing` set), i.e. the capital employed over the course of the period rather than its
closing balance, consistent with the Return on Invested Capital calculation in the Ratios
module.
- The Weighted Average Cost of Capital comes from `get_weighted_average_cost_of_capital`,
with the market risk premium given by `market_risk_premium` (by default the equity risk
premium of the company's country) and the same `trailing`, so that it
covers the span of the NOPAT (an annual rate for trailing=4 with quarterly data).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["V", "MA", "HD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2022-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_economic_value_added().xs("Economic Value Added", level=1)
```

Which returns:

|    |        2022 |        2023 |        2024 |         2025 |
|:---|------------:|------------:|------------:|-------------:|
| HD | 1.51589e+10 | 1.23635e+10 | 1.2118e+10  | nan          |
| MA | 8.7863e+09  | 9.8349e+09  | 1.15046e+10 |   1.3298e+10 |
| V  | 1.1435e+10  | 1.30387e+10 | 1.5465e+10  |   1.5322e+10 |

---

## get_market_value_added
Market Value Added (MVA) is a measure of a company's financial performance that represents the difference between the current market value of a company (both its equity and its debt) and the total capital that has historically been invested in it. It is the market-priced counterpart to Economic Value Added (EVA): where EVA measures a single period's excess return over the cost of capital, MVA reflects the market's cumulative, forward-looking verdict on all of a company's expected future EVA.

The formula is as follows:

$$
\text{Market Value of Equity} = \text{Share Price} \cdot \text{Total Shares Outstanding}
$$

$$
\text{Invested Capital} = \text{Total Equity} + \text{Total Debt}
$$

$$
\text{MVA} = (\text{Market Value of Equity} + \text{Market Value of Debt}) - \text{Invested Capital}
$$

**Also known as:** MVA, market value added.

**Args:**

- <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The number of periods the Invested Capital is averaged
over. The window counts calendar periods, so a period without a report makes it
NaN. Defaults to None, which uses the closing balances.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the MVA and its components.

**Notes:**

- A positive MVA indicates that the market believes management has created value in
excess of the capital invested in the company. A negative MVA indicates the market
values the company below the capital that has historically been invested in it.
- The Market Value of Debt is approximated as the closing book value of Total Debt,
the same simplification used in the Weighted Average Cost of Capital calculation
elsewhere in this module.
- The Market Value of Equity is the closing share price at the end of the fiscal period
times the period's weighted average shares, and the Invested Capital is the Total
Equity plus the Total Debt on the balance sheet of that day, so both sides of the MVA
have the same date. With the debt at its book value on both sides, it cancels out:
the MVA is the market value of equity minus the book Total Equity.
- With `trailing` set, the Invested Capital is the average of the closing balances of
the trailing periods, while the market values stay those at the end of the period.

References:
- Stern, Joel M., G. Bennett Stewart, and Donald H. Chew. "The EVA Financial
Management System." Journal of Applied Corporate Finance, Vol. 8, No. 2, 1995, pp. 32-46.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["LLY", "JNJ", "MRK"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_market_value_added().xs("Market Value Added", level=1)
```

Which returns:

|     |        2021 |        2022 |        2023 |        2024 |        2025 |
|:----|------------:|------------:|------------:|------------:|------------:|
| JNJ | 3.83418e+11 | 3.93774e+11 | 3.32543e+11 | 2.80894e+11 | 4.22872e+11 |
| LLY | 2.4267e+11  | 3.2017e+11  | 5.15679e+11 | 6.83662e+11 | 9.3853e+11  |
| MRK | 1.56255e+11 | 2.35977e+11 | 2.40039e+11 | 2.06407e+11 | 2.11225e+11 |

---

## get_return_on_incremental_invested_capital
Calculate the Return on Incremental Invested Capital (ROIIC): the growth in after-tax operating profit over the capital invested to produce it. Where the Return on Invested Capital measures the return on all the capital in place, ROIIC measures the return on the newest investments, which shows whether growth creates value: growth adds value only while the ROIIC exceeds the cost of capital.

The formula is as follows, with n the number of years:

$$
\text{NOPAT} = \text{EBIT} \cdot (1 - \text{Tax Rate})
$$

$$
\text{Invested Capital} = \text{Total Equity} + \text{Total Debt}
$$

$$
\text{ROIIC} \;(t) = \frac{\text{NOPAT} \;(t) - \text{NOPAT} \;(t - n)}{\text{Invested Capital} \;(t - 1) - \text{Invested Capital} \;(t - 1 - n)}
$$

Following Mauboussin and Callahan, the invested capital is lagged by a year: the capital invested in a year earns its profit in the years after. A longer span (`years`, often 3 or 5) smooths the lumpy year-to-year changes.

For more information, see the following sources:

- Mauboussin, M. J. and Callahan, D. (2014). "Calculating Return on Invested Capital." Credit Suisse Global Financial Strategies.
- Koller, T., Goedhart, M. and Wessels, D. (2020). "Valuation: Measuring and Managing the Value of Companies." Wiley, 7th edition.

**Also known as:** ROIIC, incremental ROIC, return on new invested capital, RONIC.

**Args:**

- <u>years (int, optional):</u> The number of years n the changes span. Defaults to 1.
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The number of periods to sum the NOPAT over. The window
counts calendar periods, so a period without a report makes it NaN. Defaults to None,
which is 4 on quarterly data (a trailing twelve months, with every lag counted in
years of four quarters) and single years on yearly data.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker the Net Operating Profit After Taxes, the Change in NOPAT, the
Invested Capital (a year earlier), the Change in Invested Capital and the Return on
Incremental Invested Capital (a decimal).

**Notes:**

- NOPAT and the Invested Capital are those of `get_economic_value_added` (the effective tax
rate kept within 0 and 1, EBIT the reported Operating Income), with the Invested Capital at
the period end rather than averaged, as its change is what was invested.
- The ROIIC is NaN where the invested capital did not grow: a ratio on shrinking capital
has no meaning as a return (a fall in NOPAT on less capital would show as a positive return).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["COST", "WMT", "TGT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_return_on_incremental_invested_capital().xs(
    "Return on Incremental Invested Capital", level=1
)
```

Which returns:

|      |   2021 |   2022 |     2023 |    2024 |   2025 |
|:-----|-------:|-------:|---------:|--------:|-------:|
| COST |    nan |    nan |   0.0657 |  0.2493 |    nan |
| TGT  |    nan |    nan |   1.3141 | -0.0469 |    nan |
| WMT  |    nan |    nan | nan      |  0.264  |    nan |

---

## get_owner_earnings
Calculate Warren Buffett's owner earnings: the cash a business could pay its owners while keeping its competitive position and unit volume. Buffett defines them in the 1986 Berkshire Hathaway letter as the reported earnings plus depreciation, depletion and amortization and other non-cash charges, less the average yearly capital expenditure the business needs to keep its position (and any additional working capital that requires).

The formula is as follows:

$$
\text{Owner Earnings} = \text{Net Income} + \text{Depreciation and Amortization} - \text{Maintenance Capital Expenditure} - \text{Change in Working Capital}
$$

$$
\text{Owner Earnings per Share} = \frac{\text{Owner Earnings}}{\text{Weighted Average Shares Diluted}}
$$

The statements do not split the capital expenditure into maintenance and growth, which Buffett himself calls a guess. `method` chooses the estimate of the maintenance part:

- "total": all the capital expenditure, the conservative estimate (owner earnings then differ from the free cash flow only by the non-cash items other than depreciation).
- "greenwald": the capital expenditure minus the growth capital expenditure, the investment the growth in revenue required at the company's ratio of property, plant and equipment to revenue a year earlier (Greenwald et al., 2001): Maintenance Capital Expenditure = Capital Expenditure - PP&E / Revenue (t - 1) * max(Change in Revenue, 0), at least 0.

For more information, see the following sources:

- Buffett, W. E. (1986). "Chairman's Letter." Berkshire Hathaway Inc. Annual Report 1986, appendix on purchase-price accounting adjustments and owner earnings.
- Greenwald, B. C. N., Kahn, J., Sonkin, P. D. and van Biema, M. (2001). "Value Investing: From Graham to Buffett and Beyond." Wiley, chapter 6.

**Also known as:** owner earnings, Buffett owner earnings, maintenance free cash flow.

**Args:**

- <u>method (str, optional):</u> The estimate of the maintenance capital expenditure: "total" or
"greenwald". Defaults to "total".
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The number of periods to sum the flows over. The window
counts calendar periods, so a period without a report makes it NaN. Defaults to None,
which uses single periods (per quarter on quarterly data).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker the Net Income, Depreciation and Amortization, Capital
Expenditure, Maintenance Capital Expenditure, Change in Working Capital, Owner Earnings
and Owner Earnings per Share.

**Notes:**

- The Change in Working Capital is that of the cash flow statement with its sign turned, so
an increase in working capital (a use of cash) is positive and lowers the owner earnings.
- Depreciation and Amortization is that of the cash flow statement; other non-cash charges
(such as share-based compensation) are not added back, as Buffett adds back only the
charges that do not reflect an economic cost.
- With method="greenwald" on quarterly data, the change in revenue is measured against the
same period a year earlier and divided over the four quarters of that year when `trailing`
is not set.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["KO", "PEP", "MDLZ"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_owner_earnings().xs("Owner Earnings", level=1)
```

Which returns:

|      |       2021 |      2022 |      2023 |      2024 |      2025 |
|:-----|-----------:|----------:|----------:|----------:|----------:|
| KO   | 1.1181e+10 | 8.713e+09 | 9.144e+09 | 3.408e+09 | 4.837e+09 |
| MDLZ | 3.799e+09  | 2.405e+09 | 4.553e+09 | 3.557e+09 | 1.556e+09 |
| PEP  | 6.926e+09  | 6.095e+09 | 6.737e+09 | 6.379e+09 | 6.358e+09 |

---

## get_unlevered_beta
Calculate the unlevered (asset) beta of Hamada (1972): the beta each company's shares would have without debt, its business risk apart from its financial leverage. Unlevered betas can be compared across companies with different amounts of debt, averaged over an industry and relevered at a company's own leverage (Damodaran's bottom-up beta, see `wacc_model.get_relevered_beta`).

The formula is as follows:

$$
\text{Levered Beta} = \text{the regression}\; \beta \;\text{of the shares against the benchmark over the period}
$$

$$
\text{Debt to Equity} = \frac{\text{Total Debt}}{\text{Market Value of Equity}}
$$

$$
\text{Unlevered Beta} = \frac{\text{Levered Beta}}{1 + (1 - \text{Tax Rate}) \cdot \text{Debt to Equity}}
$$

For more information, see the following sources:

- Hamada, R. S. (1972). "The Effect of the Firm's Capital Structure on the Systematic Risk of Common Stocks." The Journal of Finance, 27(2), 435-452.
- Damodaran, A. (2012). "Investment Valuation." Wiley, 3rd edition, chapter 8.

**Also known as:** asset beta, unlevered beta, Hamada equation, business risk beta.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The number of periods the beta is measured over (and the
taxes summed over). The window counts calendar periods, so a period without a report
makes it NaN. Defaults to None, which is a single period.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker the Levered Beta, Debt to Equity, Tax Rate and Unlevered Beta.

**Notes:**

- The Levered Beta, the market value of equity and the tax rate are those of
`get_weighted_average_cost_of_capital`: the beta of the daily returns within the period
against the benchmark, the closing price at the fiscal period end times the diluted
weighted average shares, and the effective tax rate kept within 0 and 1 (0 without a
pre-tax profit). The debt is the book value of Total Debt, the usual stand-in for its
market value.
- The debt is assumed to carry no market risk (a debt beta of zero), as Hamada and
Damodaran's bottom-up betas do. Damodaran also corrects the unlevered beta for the cash a
company holds (Unlevered Beta / (1 - Cash / Firm Value)), which this leaves out.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["F", "GM", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_unlevered_beta().xs("Unlevered Beta", level=1)
```

Which returns:

|      |   2021 |   2022 |   2023 |   2024 |   2025 |
|:-----|-------:|-------:|-------:|-------:|-------:|
| F    | 0.4549 | 0.3568 | 0.3472 | 0.2686 | 0.1996 |
| GM   | 0.6333 | 0.4549 | 0.4088 | 0.3555 | 0.3454 |
| TSLA | 1.9416 | 1.7191 | 2.223  | 2.3614 | 2.2258 |

---

## get_capitalized_research_and_development
Capitalize the research and development expenses as Aswath Damodaran does: accounting treats R&D as an expense, while it is an investment whose benefit lasts several years. Every year's R&D becomes an asset amortized straight-line over its amortizable life, which changes the operating income, the net income, the book equity, the invested capital and with them the return on capital of research-intensive companies.

The formula is as follows, with n the amortizable life in years:

$$
\text{Research Asset} \;(t) = \frac{\sum(k = 0 \ldots n - 1) \;\text{R\&D} \;(t - k) \cdot (n - k)}{n}
$$

$$
\text{Amortization} \;(t) = \frac{\sum(k = 1 \ldots n) \;\text{R\&D} \;(t - k)}{n}
$$

$$
\text{Adjusted Operating Income} = \text{Operating Income} + \text{R\&D} - \text{Amortization}
$$

$$
\text{Adjusted Net Income} = \text{Net Income} + \text{R\&D} - \text{Amortization}
$$

$$
\text{Adjusted Total Equity} = \text{Total Equity} + \text{Research Asset}
$$

$$
\text{Adjusted Invested Capital} = \text{Total Equity} + \text{Total Debt} + \text{Research Asset}
$$

$$
\text{Adjusted Return on Invested Capital} = \frac{\text{Adjusted Operating Income} \cdot (1 - \text{Tax Rate})}{\text{Adjusted Invested Capital at the beginning of the period}}
$$

The expense of the current year is not amortized yet, and that of n years ago is written off in full this year, as in Damodaran's R&D converter.

For more information, see the following sources:

- Damodaran, A. (2012). "Investment Valuation." Wiley, 3rd edition, chapter 9.
- Damodaran, A. "R&D Converter" (R&D.xls), [https://pages.stern.nyu.edu/~adamodar/New_Home_Page/spreadsh.htm](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/spreadsh.htm){:target="_blank"}
- Lev, B. and Sougiannis, T. (1996). "The Capitalization, Amortization, and Value-Relevance of R&D." Journal of Accounting and Economics, 21(1), 107-138.

**Also known as:** R&D capitalization, research asset, capitalized R&D, adjusted operating income for R&D.

**Args:**

- <u>amortization_years (int, optional):</u> The amortizable life n of the research asset in
years. Damodaran uses 2 years for software, 3 to 5 for most industries and up to 10
for pharmaceuticals (the life it takes to turn research into products). Defaults to 5.
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker the Research and Development Expenses, Research Asset,
Amortization of Research Asset, Adjusted Operating Income, Adjusted Net Income,
Adjusted Total Equity, Adjusted Invested Capital and Adjusted Return on Invested Capital.

**Notes:**

- The asset needs the expenses of the n years before: with a start date less than n years
back the results are NaN (set an earlier start_date). A year without a reported R&D expense
leaves the years that include it NaN rather than counting it as zero.
- On quarterly data every quarter holds the expenses of the trailing year, the asset and
amortization are those of the years ending with the quarter, and the adjusted incomes are
trailing twelve months figures.
- The tax rate is the effective tax rate kept within 0 and 1 (0 without a pre-tax profit),
as in `get_economic_value_added`. Damodaran notes that the tax benefit of R&D stays that of
the expense, which these adjustments keep by not changing the taxes.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["MRK", "PFE", "LLY"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2015-01-01",
    end_date="2025-12-31",
)

# The last four years, the first with ten years of spending behind them
toolkit.models.get_capitalized_research_and_development(
    amortization_years=10
).loc["MRK"].iloc[:, -4:]
```

Which returns:

|                                     |         2022 |          2023 |        2024 |        2025 |
|:------------------------------------|-------------:|--------------:|------------:|------------:|
| Research and Development Expenses   |   1.3548e+10 |   3.0531e+10  | 1.7938e+10  | 1.2514e+10  |
| Research Asset                      | nan          |   8.18812e+10 | 8.74511e+10 | 8.65212e+10 |
| Amortization of Research Asset      | nan          |   1.00653e+10 | 1.23681e+10 | 1.34439e+10 |
| Adjusted Operating Income           | nan          |   2.34197e+10 | 2.57909e+10 | 2.25561e+10 |
| Adjusted Net Income                 | nan          |   2.08307e+10 | 2.26869e+10 | 1.73241e+10 |
| Adjusted Total Equity               | nan          |   1.19516e+11 | 1.33823e+11 | 1.39183e+11 |
| Adjusted Invested Capital           | nan          |   1.55784e+11 | 1.72093e+11 | 1.89717e+11 |
| Adjusted Return on Invested Capital | nan          | nan           | 0.1423      | 0.1136      |

---

## get_cash_flow_return_on_investment
Calculate the Cash Flow Return on Investment (CFROI) of Bartley Madden (the HOLT model): the internal rate of return of a company's assets seen as one project. The gross investment buys a gross cash flow for every year of the life of the depreciating assets, and the non-depreciating assets (working capital) come back at the end. Where the return on invested capital divides an accounting profit by depreciated book values, the CFROI compares cash flows with the original cost of the assets, which makes companies with old and new assets comparable.

The formula is as follows, solved for the CFROI:

$$
\text{Gross Cash Flow} = \text{Net Income} + \text{Depreciation and Amortization} + \text{Interest Expense}
$$

$$
\text{Depreciating Assets} = \text{Gross Property, Plant and Equipment} \;(\text{Net Property, Plant and Equipment where the gross amount is not reported})
$$

$$
\text{Non-Depreciating Assets} = \text{Total Current Assets} - (\text{Total Current Liabilities} - \text{Short Term Debt})
$$

$$
\text{Gross Investment} = \text{Depreciating Assets} + \text{Non-Depreciating Assets}
$$

$$
\text{Asset Life} = \frac{\text{Depreciating Assets}}{\text{Depreciation and Amortization}}
$$

$$
\text{Gross Investment} = \frac{\sum(t = 1 \ldots \;\text{Asset Life}) \;\text{Gross Cash Flow}}{(1 + \text{CFROI})^{t}} + \frac{\text{Non-Depreciating Assets}}{(1 + \text{CFROI})^{\text{Asset Life}}}
$$

This is the simplified, nominal form of Madden's model that the statements allow. HOLT's CFROI also restates the gross investment and the cash flows for inflation (a real return), capitalizes operating leases and R&D and adds the rental expense to the cash flow; practitioner versions differ in these choices, so the levels are best compared between companies and over time rather than with a published CFROI.

For more information, see the following sources:

- Madden, B. J. (1999). "CFROI Valuation: A Total System Approach to Valuing the Firm." Butterworth-Heinemann.
- Madden, B. J. (2010). "Wealth Creation: A Systems Mindset for Building and Investing in Businesses for the Long Term." Wiley.

**Also known as:** CFROI, HOLT CFROI, cash flow return on investment, Madden CFROI.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker the Gross Cash Flow, Depreciating Assets, Non-Depreciating
Assets, Gross Investment, Asset Life (years) and the Cash Flow Return on Investment (a
decimal per year, annually compounded).

**Notes:**

- The balance sheet items are averaged over the period ends that open and close the year,
as the invested capital of `get_economic_value_added`. On quarterly data the flows are
those of the trailing twelve months, so the CFROI stays a yearly rate.
- FinancialModelingPrep reports the property, plant and equipment net of depreciation. The
net amount understates the original cost and its life (Net PP&E / Depreciation) is the
remaining life of the assets, which gives a remaining-life CFROI. Where the statements
report the gross amount (Yahoo Finance), the gross amount and the full life are used.
- The CFROI is NaN where the life or the gross investment is not positive or no rate
between -99% and 1,000% solves the equation (such as a gross cash flow that never
returns the investment).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["HD", "LOW"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_cash_flow_return_on_investment().loc["HD"]
```

Which returns:

|                                |         2021 |         2022 |        2023 |       2024 |
|:-------------------------------|-------------:|-------------:|------------:|-----------:|
| Gross Cash Flow                |  2.0642e+10  |  2.1697e+10  |  2.0333e+10 | 2.0888e+10 |
| Depreciating Assets            |  3.0917e+10  |  3.18695e+10 |  3.3305e+10 | 3.4666e+10 |
| Non-Depreciating Assets        |  5.2855e+09  |  7.218e+09   |  9.86e+09   | 8.524e+09  |
| Gross Investment               |  3.62025e+10 |  3.90875e+10 |  4.3165e+10 | 4.319e+10  |
| Asset Life                     | 10.8026      | 10.7124      | 10.2572     | 9.2172     |
| Cash Flow Return on Investment |  0.5664      |  0.551       |  0.4637     | 0.4726     |

---

## get_intrinsic_valuation
Intrinsic value is a fundamental concept in finance and investing that represents the true worth or value of an asset, security, or investment, independent of its current market price or prevailing market sentiment. It is a concept often associated with the value investing philosophy, made famous by legendary investors like Benjamin Graham and Warren Buffett. Understanding intrinsic value is crucial for investors looking to make informed decisions about where to allocate their capital.

This functionality uses DCF, or Discounted Cash Flow which is a widely used financial valuation method that allows investors and analysts to estimate the intrinsic value of an investment or business based on its expected future cash flows. It is a fundamental tool in finance and investment analysis, providing a systematic way to assess the present value of future cash flows while considering the time value of money.

The formula is as follows:

$$
\text{Cash Flow Projection}_{t} = \text{Cash Flow}_{t-1} \cdot (1 + \text{Growth Rate})
$$

$$
\text{Terminal Value} = \frac{\text{Last Cash Flow Projection} \cdot (1 + \text{Perpetual Growth Rate})}{\text{Weighted Average Cost of Capital} - \text{Perpetual Growth Rate}}
$$

$$
\text{Enterprise Value} = \text{Sum of Present Value of Cash Flow Projections} + \frac{\text{Terminal Value}}{(1 + \text{Weighted Average Cost of Capital})^{\text{Periods}}}
$$

$$
\text{Equity Value} = \text{Enterprise Value} + \text{Cash and Cash Equivalents} + \text{Short Term Investments} - \text{Total Debt} - \text{Minority Interest} - \text{Preferred Stock}
$$

$$
\text{Intrinsic Value} = \frac{\text{Equity Value}}{\text{Weighted Average Shares Diluted}}
$$

The base cash flow is by default the Free Cash Flow to the Firm (see `get_free_cash_flow_to_firm`), the cash flow available to both debt and equity holders. That is the cash flow the Weighted Average Cost of Capital discounts into an Enterprise Value, from which the debt is then subtracted.

In a five-year DCF the discounted terminal value is often 60% to 80% of the enterprise value, so the result is driven mostly by the gap between the WACC and the perpetual growth rate. Practitioners therefore show the intrinsic value as a range over several WACC and growth assumptions rather than a single number, and keep the perpetual growth rate at or below long-run nominal GDP growth.

**Also known as:** DCF, discounted cash flow, fair value, intrinsic value.

**Args:**

- <u>growth_rate (float, list or dict, optional):</u> The growth rate to use for the cash flow projections. Can be
one number to use for all tickers, or a list or dict that contains a growth rate for each ticker.
Defaults to None, which uses the growth the company's reinvestment - <u>supports (Damodaran):</u> the
Reinvestment Rate times the Return on Invested Capital, its reinvestment (NOPAT minus the Free Cash
Flow to Firm) per year as a share of its invested capital (equity plus debt) over the data up to
the period valued: the latest period, or each period with `historical=True`.
- <u>perpetual_growth_rate (float, list or dict, optional):</u> The perpetual growth rate to use for the
terminal value. Can be one number to use for all tickers, or a list or dict that contains a perpetual
growth rate for each ticker. Defaults to None, which uses the company's growth (as for growth_rate)
kept within 0 and the long-run growth rate of 2.5%, and 2.5% where it has none.
- <u>weighted_average_cost_of_capital (float, list or dict, optional):</u> The weighted average cost of capital
used to discount the projected cash flows and to calculate the terminal value. Can be one number to
use for all tickers, or a list or dict that contains a weighted average cost of capital for each
ticker. Defaults to None, which uses the Weighted Average Cost of Capital of each company of the
period valued, calculated over a year (the last 4 quarters with quarterly data, with a beta of
their daily returns).
- <u>periods (int, optional):</u> The number of periods to use for the cash flow projections. Defaults to 5.
- <u>cash_flow_type (str, optional):</u> The type of cash flow to use for the cash flow projections.
Defaults to "Free Cash Flow to Firm". The other options are "Free Cash Flow" and "Operating
Cash Flow" as reported on the cash flow statement; both are after interest, so discounting
them at the WACC and subtracting the debt counts the cost of debt twice.
- <u>trailing (int &#124; None, optional):</u> The number of trailing periods to sum for the base cash flow.
The window counts calendar periods, so a period without a report makes it NaN.
When set, uses the sum of the latest N consecutive calendar periods that are all reported instead
of only the most recent period. Defaults to None, which uses 4 (the trailing twelve months) with
quarterly data and the most recent year with yearly data.
- <u>historical (bool, optional):</u> Whether to value every period instead of only the most recent one,
which gives the intrinsic value per share over time. Each period is valued from the base cash
flow ending in it and the cash, debt and shares reported at its end. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the intrinsic value and its components for each ticker, or
with `historical=True` the intrinsic value per share for each ticker (rows) and period (columns).

**Notes:**

- The results are highly dependent on the input. Therefore, think carefully about each input parameter to
ensure the results are accurate (given your beliefs)
- The growth rate, perpetual growth rate and WACC are annual rates, so the base cash flow is an annual
one: with quarterly data the four quarters of the latest year with all four reported are summed. A
company reporting half-yearly has no such year and is not valued with quarterly data (use yearly
data). Setting `trailing` with yearly data sums several years into one base cash flow, which logs a
warning.
- The WACC must be greater than the perpetual growth rate; otherwise the terminal value is infinite
and the valuation is not calculated. Within 2 percentage points of it the valuation is calculated
with a warning, as a tenth of a percentage point on either rate then moves it by about 5%.
- The Total Debt, Cash and Cash Equivalents and Short Term Investments are those of the most
recent period. Short Term Investments are added back with the cash, the same cash and marketable
securities `get_enterprise_value_breakdown` deducts, and count as 0 when the balance sheet has no
such row.
- The Equity Value is divided by the Weighted Average Shares Diluted of the most recent period.
- With `historical=True` no period uses figures reported after it, so the series shows what this
DCF gave at each period end, with the growth and WACC known at that period end when they are not given. A period whose cash flow, cash, debt or
shares are missing is NaN, while the single valuation takes the most recent value of each.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["ADBE", "CRM", "INTU"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_intrinsic_valuation().xs("Intrinsic Value", level=1)
```

Which returns:

|      |   Periods = 5 |
|:-----|--------------:|
| ADBE |      213.31   |
| CRM  |       67.9174 |
| INTU |      172.144  |

And the same valuation for every period with `historical=True`:

```python
toolkit.models.get_intrinsic_valuation(historical=True)
```



|      |     2021 |     2022 |     2023 |     2024 |    2025 |
|:-----|---------:|---------:|---------:|---------:|--------:|
| ADBE | 132.425  | 112.433  | 102.593  | 130.005  | 212.536 |
| CRM  |  18.2502 |  11.8861 |  51.1607 |  67.9382 | nan     |
| INTU | 102.101  |  60.4477 |  99.9192 |  97.2924 | 173.485 |

---

## get_free_cash_flow_to_firm
Free Cash Flow to the Firm (FCFF) is the cash flow available to all providers of capital, both debt and equity holders, after the company has paid all of its operating expenses and invested in the assets needed to sustain its operations. Because it is measured before any financing cash flows, FCFF is capital-structure neutral, making it the cash flow base typically discounted at the Weighted Average Cost of Capital (WACC) when valuing the Enterprise Value of a company directly.

The formula is as follows:

$$
\text{NOPAT} = \text{EBIT} \cdot (1 - \text{Corporate Tax Rate})
$$

$$
\text{FCFF} = \text{NOPAT} + \text{Depreciation and Amortization} - \text{Capital Expenditure} - \text{Change in Net Working Capital}
$$

**Also known as:** FCFF, unlevered free cash flow.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. The window counts
calendar periods, so a period without a report makes it NaN. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the FCFF and its components.

**Notes:**

- EBIT is the reported Operating Income, as in the Altman Z-Score and Economic Value
Added calculations elsewhere in this module.
- The Corporate Tax Rate is the effective tax rate (Income Tax Expense / Income Before Tax)
kept within 0 and 1, and 0 for a period without a pre-tax profit, the same rate the
Weighted Average Cost of Capital uses (see `get_weighted_average_cost_of_capital`).
- The Capital Expenditure and Change in Working Capital line items from the cash flow
statement are stored using a cash-flow-impact sign convention (a use of cash is
negative). This method negates them internally so that they represent positive
magnitudes (amount spent / amount of the increase), matching the standard academic
FCFF formula. See `get_free_cash_flow_to_firm` in the Intrinsic module for details.
- FCFF is the default base cash flow of `get_intrinsic_valuation`, which discounts it
at the Weighted Average Cost of Capital.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["XOM", "CVX"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_free_cash_flow_to_firm().xs("Free Cash Flow to Firm", level=1)
```

Which returns:

|     |        2021 |        2022 |        2023 |        2024 |        2025 |
|:----|------------:|------------:|------------:|------------:|------------:|
| CVX | 1.98409e+10 | 3.51075e+10 | 2.2617e+10  | 1.97109e+10 | 1.16812e+10 |
| XOM | 3.08399e+10 | 5.28525e+10 | 2.78286e+10 | 2.68446e+10 | 1.83253e+10 |

---

## get_free_cash_flow_to_equity
Free Cash Flow to Equity (FCFE) is the cash flow available to a company's common equity holders after all operating expenses, reinvestment needs, and net payments to (or from) debt holders have been accounted for. Unlike FCFF, FCFE is a levered cash flow measure and should be discounted at the Cost of Equity, not the Weighted Average Cost of Capital, when used to value equity directly.

The formula is as follows:

$$
\text{FCFE} = \text{Net Income} + \text{Depreciation and Amortization} - \text{Capital Expenditure} - \text{Change in Net Working Capital} + \text{Net Borrowing}
$$

**Also known as:** FCFE, levered free cash flow.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. The window counts
calendar periods, so a period without a report makes it NaN. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the FCFE and its components.

**Notes:**

- The Capital Expenditure and Change in Working Capital line items from the cash flow
statement are stored using a cash-flow-impact sign convention (a use of cash is
negative). This method negates them internally so that they represent positive
magnitudes, matching the standard academic FCFE formula. Net Debt Issued (used as
Net Borrowing) is already reported using the cash-flow-impact convention (a positive
value means the company was a net borrower) and is therefore used as-is.
- FCFE is the natural cash-flow-based counterpart to Residual Income
(`get_residual_income`) for equity-only valuation, in the same way FCFF is the
counterpart to Economic Value Added for firm-level valuation.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["CMCSA", "CHTR", "VZ"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_free_cash_flow_to_equity().xs("Free Cash Flow to Equity", level=1)
```

Which returns:

|       |       2021 |       2022 |       2023 |        2024 |       2025 |
|:------|-----------:|-----------:|-----------:|------------:|-----------:|
| CHTR  | 1.5532e+10 | 1.1e+10    | 1.955e+09  | -1.31e+09   | 2.43e+09   |
| CMCSA | 6.168e+09  | 3.618e+09  | 1.1394e+10 |  1.6448e+10 | 2.1732e+10 |
| VZ    | 3.9649e+10 | 1.5507e+10 | 8.042e+09  |  1.0354e+10 | 2.3559e+10 |

---

## get_gordon_growth_model
The Gordon Growth Model, also known as the Dividend Discount Model (DDM) with Constant Growth, is a method used to estimate the intrinsic value of a stock based on its expected future dividends. The model assumes that dividends will grow at a constant rate indefinitely.

The formula is as follows:

$$
\text{Intrinsic Value} = \frac{\text{Dividends Per Share} \cdot (1 + \text{Growth Rate})}{\text{Rate of Return} - \text{Growth Rate}}
$$

The formula essentially discounts the future expected dividends to their present value, taking into account the required rate of return and the growth rate. The numerator represents the expected dividend in the next period. The denominator represents the required rate of return minus the growth rate.

Investors often use the Gordon Growth Model to compare the intrinsic value of a stock with its current market price. If the intrinsic value is higher than the market price, some investors may interpret it as an indication that the stock is undervalued.

It's important to note that the Gordon Growth Model is based on several assumptions, including the assumption of constant growth in dividends. It is most applicable to mature companies with stable and predictable dividend growth. If a company's dividend growth is expected to fluctuate or if it does not pay dividends, alternative valuation models may be more appropriate.

The assumption of constant growth of dividends is often unrealistic. In reality, dividends may fluctuate or even be suspended. Therefore, the Gordon Growth Model should be used with caution and in conjunction with other valuation methods.

The Rate of Return must exceed the growth rate; periods where it doesn't are left out with a warning. Within 2 percentage points of it the value is calculated with a warning, as a tenth of a percentage point on either rate then moves it by about 5%.

**Also known as:** Gordon Growth Model, DDM, dividend discount model, GGM.

**Args:**

- <u>rate_of_return (float, list or dict, optional):</u> The required rate of return, one
number, or a list or dict with a rate per ticker. Defaults to None, which uses
each company's Cost of Equity of the period - <u>valued (the last one for the
projections):</u> the CAPM with the equity risk premium of its country and a beta
of a year of daily returns, as in `get_weighted_average_cost_of_capital`.
- <u>growth_rate (float, list or dict, optional):</u> The growth rate of the dividends,
which holds forever. Defaults to None, which uses the compound annual growth of
the company's Dividends per Share up to the period valued, kept within 0 and the
long-run growth rate of 2.5% (2.5% where it has none).
- <u>project_periods (int, optional):</u> The number of years to project the intrinsic value for, beyond the
last complete period. Defaults to 5.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the intrinsic value for each ticker over time.

**Notes:**

- The results are highly dependent on the input. Therefore, think carefully about each input parameter to
ensure the results are accurate (given your beliefs)
- The rate of return and the growth rate are annual rates, so the model values an annual dividend:
the Dividends per Share of each year, or with quarterly data the sum of the trailing four complete
quarters. The first three quarters of quarterly data lack a full trailing year and are left out.
- Each historical period is valued off that period's *actual* annual Dividends per Share, and only
the years beyond the last complete period are projected forward at the given growth rate, one year
per projection period (four quarters apart with quarterly data). With yearly data the current,
unfinished year is projected as well, since its dividends so far cover only part of it. The first
year of the historical window will often be understated, since it only covers the part of the year
that falls inside the requested date range and so captures only part of the year's dividends. Use a
start_date at least one full year before the first period you intend to read.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["KO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_gordon_growth_model()
```

Which returns:

|      |       KO |
|:-----|---------:|
| 2021 | 133.744  |
| 2022 |  68.4186 |
| 2023 |  59.3591 |
| 2024 | 102.976  |
| 2025 | 104.728  |
| 2026 | 107.347  |
| 2027 | 110.03   |
| 2028 | 112.781  |
| 2029 | 115.601  |
| 2030 | 118.491  |

---

## get_two_stage_dividend_discount_model
The Two-Stage Dividend Discount Model extends the (single-stage) Gordon Growth Model to companies that are not expected to grow at a constant rate forever. It explicitly projects and discounts dividends over an initial high-growth phase, and then values everything from the end of that phase onward as a perpetuity growing at a lower, more sustainable stable rate (a Gordon Growth terminal value).

The formula is as follows:

$$
\text{Dividend Projection}_{t} = \text{Dividends Per Share} \cdot (1 + \text{High Growth Rate})^{t}
$$

$$
\text{High-Growth Phase Present Value} = \sum_{t} \frac{\text{Dividend Projection}_{t}}{(1 + \text{Rate of Return})^{t}},\;\; \text{for}\;\; t = 1,\; \ldots,\; \text{High Growth Periods}
$$

$$
\text{Terminal Value} = \frac{\text{Last Dividend Projection} \cdot (1 + \text{Stable Growth Rate})}{\text{Rate of Return} - \text{Stable Growth Rate}}
$$

$$
\text{Intrinsic Value} = \text{High-Growth Phase Present Value} + \frac{\text{Terminal Value}}{(1 + \text{Rate of Return})^{\text{High Growth Periods}}}
$$

With transition periods it becomes the Three-Stage Dividend Discount Model: between the high-growth and the stable phase, the growth rate declines in equal steps from the high to the stable rate, and those dividends are discounted explicitly as well. In transition period k (of n), dividends grow at High Growth Rate - (High Growth Rate - Stable Growth Rate) * k / (n + 1), and the Terminal Value is taken at the end of the transition phase.

**Also known as:** two-stage DDM, two-stage dividend discount model, three-stage DDM, three-stage dividend discount model.

**Args:**

- <u>rate_of_return (float, list or dict, optional):</u> The required rate of return
(discount rate) used to discount both phases. Can be one number to use for all
tickers, or a list or dict that contains a rate of return for each ticker. Defaults
to None, which uses the latest Cost of Equity of each company: the CAPM with the
equity risk premium of its country, as in `get_weighted_average_cost_of_capital`.
- <u>high_growth_rate (float, list or dict, optional):</u> The constant growth rate applied
to dividends during the explicit high-growth phase. Can be one number to use for all
tickers, or a list or dict that contains a high growth rate for each ticker.
Defaults to None, which uses the compound annual growth of the company's Dividends
per Share up to the latest period.
- <u>stable_growth_rate (float, list or dict, optional):</u> The perpetual (terminal) growth
rate applied to dividends from the end of the high-growth phase onward. Can be one
number to use for all tickers, or a list or dict that contains a stable growth rate
for each ticker. Defaults to None, which uses the company's dividend growth kept
within 0 and the long-run growth rate of 2.5% (2.5% where it has none).
- <u>high_growth_periods (int, optional):</u> The number of years in the explicit
high-growth phase. Defaults to 5.
- <u>transition_periods (int, optional):</u> The number of years in which the growth rate
declines linearly from the high to the stable growth rate (the Three-Stage Dividend
Discount Model). Defaults to 0, no transition phase.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the intrinsic value and its components for
each ticker, including the present value of the transition phase when there is
one.

**Notes:**

- The results are highly dependent on the input. Therefore, think carefully about
each input parameter to ensure the results are accurate (given your beliefs).
- The Rate of Return must be greater than the Stable Growth Rate, otherwise the
Terminal Value formula divides by a non-positive number. Within 2 percentage points of
it the value is calculated with a warning, as a tenth of a percentage point on either
rate then moves it by about 5%.
- The base dividend used for the projection is the annual Dividends Per Share of the last complete
period for each ticker: the last complete year, or with quarterly data the sum of the last four
complete quarters, since the rates are annual and each projection period is a year. The current,
unfinished period is left out since its dividends so far cover only part of it. For companies that
do not pay a dividend, this model is not meaningful (the projections and resulting intrinsic value
will be zero).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["JNJ", "PG", "PEP"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_two_stage_dividend_discount_model().xs(
    "Intrinsic Value", level=1
)
```

Which returns:

|     |   High-Growth Periods = 5 |
|:----|--------------------------:|
| JNJ |                   296.375 |
| PEP |                   294.698 |
| PG  |                   201.233 |

---

## get_h_model
The H-Model of Fuller and Hsia (1984) values a stock whose dividend growth starts at a high rate and declines linearly to a stable rate over a number of years, after which it grows at the stable rate forever. It is a closed-form approximation of the three-stage dividend discount model (see `get_two_stage_dividend_discount_model` with `transition_periods`): the Gordon Growth Model at the stable rate plus the value of the extra growth during the decline, which is about half the high-growth period (H) times the extra growth.

The formula is as follows:

$$
H = \frac{\text{High Growth Periods}}{2}
$$

$$
\text{Intrinsic Value} = \frac{\text{Dividends Per Share} \cdot (1 + \text{Stable Growth Rate})}{\text{Rate of Return} - \text{Stable Growth Rate}} + \frac{\text{Dividends Per Share} \cdot H \cdot (\text{High Growth Rate} - \text{Stable Growth Rate})}{\text{Rate of Return} - \text{Stable Growth Rate}}
$$

Like the Gordon Growth Model, each period is valued off that period's actual annual Dividends per Share, which gives the intrinsic value over time.

**Also known as:** H-Model, Fuller-Hsia model, H model dividend discount model.

**Args:**

- <u>rate_of_return (float, list or dict, optional):</u> The required rate of return, which
must be greater than the stable growth rate; one number, or a list or dict with a
rate per ticker. Defaults to None, which uses each company's Cost of Equity of
the period valued: the CAPM with the equity risk premium of its country, as in
`get_weighted_average_cost_of_capital`.
- <u>high_growth_rate (float, list or dict, optional):</u> The growth rate of the dividends
at the start of the decline. Defaults to None, which uses the compound annual
growth of the company's Dividends per Share up to the period valued.
- <u>stable_growth_rate (float, list or dict, optional):</u> The growth rate the decline ends
at, which holds forever after it. Defaults to None, which uses the company's
dividend growth up to the period valued, kept within 0 and the long-run growth
rate of 2.5% (2.5% where it has none).
- <u>high_growth_periods (int, optional):</u> The number of years over which the growth
rate declines from the high to the stable rate. Defaults to 10.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the Toolkit (4 unless set
otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The intrinsic value per share for each period (rows) and ticker
(columns).

**Notes:**

- The results depend heavily on the inputs, in particular the high growth rate and
how long it lasts. A rate of return within 2 percentage points of the stable growth
rate is valued with a warning, as a tenth of a percentage point on either rate then
moves the value by about 5%.
- The H-Model is close to the exact value of a linearly declining growth rate when
the high-growth period is short or the gap between the growth rates is small, and
overstates it as either grows.
- The rates are annual, so the model values an annual dividend: the Dividends per
Share of each year, or with quarterly data the sum of the trailing four complete
quarters. The first year of the window often covers only part of the year's
dividends, so start the window a year before the first period you intend to read.
- Fuller, R. J. and C.-C. Hsia, "A Simplified Common Stock Valuation Model,"
Financial Analysts Journal 40(5), 1984, pp. 49-56.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["KO", "PEP"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_h_model()
```

Which returns:

|      |       KO |     PEP |
|:-----|---------:|--------:|
| 2022 |  75.9677 | 211.132 |
| 2023 |  65.5951 | 203.877 |
| 2024 | 115.099  | 382.255 |
| 2025 | 117.365  | 292.194 |

---

## get_justified_multiples
The justified multiples are the Price-to-Earnings and Price-to-Book ratios the dividend discount and residual income models imply for a company with a constant payout ratio, Return on Equity and growth rate. Comparing them with the actual multiples shows whether the market prices a company above or below what its profitability, payout and growth justify at a given required rate of return.

The formula is as follows:

$$
\text{Growth Rate} = \text{Return on Equity} \cdot (1 - \text{Payout Ratio})
$$

$$
\text{Justified Trailing} \;\text{P/E} = \frac{\text{Payout Ratio} \cdot (1 + \text{Growth Rate})}{\text{Rate of Return} - \text{Growth Rate}}
$$

$$
\text{Justified Leading} \;\text{P/E} = \frac{\text{Payout Ratio}}{\text{Rate of Return} - \text{Growth Rate}}
$$

$$
\text{Justified} \;\text{P/B} = \frac{\text{Return on Equity} - \text{Growth Rate}}{\text{Rate of Return} - \text{Growth Rate}}
$$

$$
\text{Price-to-Earnings Ratio} = \frac{\text{Share Price}}{\frac{\text{Net Income}}{\text{Weighted Average Shares}}}
$$

$$
\text{Price-to-Book Ratio} = \frac{\text{Share Price}}{\frac{\text{Total Shareholder Equity}}{\text{Weighted Average Shares}}}
$$

The Growth Rate is the sustainable growth rate above unless a growth rate is given.

**Also known as:** justified P/E, justified P/B, fundamental P/E, warranted multiples.

**Args:**

- <u>rate_of_return (float, list or dict, optional):</u> The required rate of return on
equity, one number, or a list or dict with a rate per ticker. Defaults to None,
which uses each company's Cost of Equity of each period: the CAPM with the equity
risk premium of its country, as in `get_weighted_average_cost_of_capital`.
- <u>growth_rate (float &#124; None, optional):</u> The constant growth rate of the earnings,
dividends and book value. Defaults to None, which uses the sustainable growth
rate of each period kept within 0 and the long-run growth rate of 2.5%, as a
growth rate that holds forever can't exceed the growth of the economy.
- <u>diluted (bool, optional):</u> Whether to use the diluted share count for the actual
multiples. Defaults to True.
- <u>trailing (int &#124; None, optional):</u> Sum the flows over this many periods and measure
the Return on Equity on the equity that many periods back. The window counts
calendar periods, so a period without a report makes it NaN. Defaults to
None, which is 4 for quarterly data (a trailing twelve months) and 1
otherwise.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the Toolkit (4 unless set
otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker and period the Payout Ratio, Return on Equity, Growth
Rate, Justified Trailing P/E, Justified Leading P/E, Justified P/B and the actual
Price-to-Earnings and Price-to-Book Ratios.

**Notes:**

- The justified multiples are NaN where the growth rate is at or above the rate of
return, since the models then have no finite value, and they mean little for a
company that pays no dividend or makes a loss.
- The Return on Equity is measured on the equity at the beginning of the period, as
in the sustainable growth rate (Higgins), so the first period has none.
- The actual multiples use the share price at the period end and the reported Net
Income and equity per share, without the adjustment for preferred dividends that
`toolkit.ratios.get_price_to_earnings_ratio` makes.
- CFA Institute, "Equity Valuation: Applications and Processes" and "Market-Based
Valuation: Price and Enterprise Value Multiples," CFA Program Curriculum Level II.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["KO", "PEP", "PG"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_justified_multiples().loc["KO"]
```

Which returns:

|                         |    2021 |    2022 |    2023 |    2024 |    2025 |
|:------------------------|--------:|--------:|--------:|--------:|--------:|
| Payout Ratio            |  0.7422 |  0.7982 |  0.7422 |  0.7863 |  0.6698 |
| Return on Equity        |  0.5063 |  0.4149 |  0.4445 |  0.4098 |  0.5273 |
| Growth Rate             |  0.025  |  0.025  |  0.025  |  0.025  |  0.025  |
| Justified Trailing P/E  | 58.5587 | 31.0455 | 23.9391 | 41.6972 | 34.3992 |
| Justified Leading P/E   | 57.1304 | 30.2883 | 23.3552 | 40.6802 | 33.5602 |
| Justified P/B           | 37.0476 | 14.7954 | 13.1996 | 19.9092 | 25.1687 |
| Price-to-Earnings Ratio | 26.2994 | 28.9985 | 23.8657 | 25.2999 | 23.0046 |
| Price-to-Book Ratio     | 11.1732 | 11.4791 |  9.8569 | 10.8209 |  9.3731 |

---

## get_residual_income
Residual Income is a measure of the profit a company generates in excess of the return required by its equity holders. It is the equity-side counterpart to Economic Value Added (EVA), and underpins the Residual Income Model, an alternative equity valuation lens to a traditional Discounted Cash Flow (DCF) that is particularly useful when a company's free cash flows are negative or unpredictable but its accounting earnings are more stable.

The formula is as follows:

$$
\text{Residual Income}_{t} = \text{Net Income}_{t} - (\text{Cost of Equity} \cdot \text{Book Value of Equity}_{t-1})
$$

**Also known as:** RI, economic profit (equity variant), abnormal earnings.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. The window counts
calendar periods, so a period without a report makes it NaN. Defaults to None.
- <u>market_risk_premium (float &#124; None, optional):</u> The annual equity risk premium the Cost of Equity
uses. Defaults to None, which takes the equity risk premium of each company's country
(Damodaran's Total Equity Risk Premium, see get_market_risk_premium) and, where that is
not available, the benchmark's average return above the risk-free rate over the data.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the Residual Income and its components.

**Notes:**

- A positive Residual Income indicates that the company generated more profit than
equity holders required given the capital they have invested. A negative Residual
Income indicates the company failed to earn its equity holders' required return, even
if it still reported a positive Net Income.
- The Cost of Equity follows from the Capital Asset Pricing Model (CAPM), as in
`get_weighted_average_cost_of_capital`: the risk-free rate of the period plus Beta times
the market risk premium, by default the equity risk premium of the company's country
(see `market_risk_premium`). It covers the span of the Net Income: a
quarter with quarterly data, and the per-period rate times `trailing` when the Net Income
is a trailing sum (an annual rate for trailing twelve months, trailing=4 with quarterly data),
with the Beta estimated from the daily returns of the same trailing periods.
- The Book Value of Equity is the Total Shareholder Equity minus Preferred Stock at the
beginning of the period (the previous period's closing balance, or that of `trailing` periods
back with `trailing` set), the capital the shareholders had invested while the Net Income was
earned. Preferred equity is excluded since Residual Income (like Net Income) belongs to common
equity holders only.

References:
- Ohlson, James A. "Earnings, Book Values, and Dividends in Equity Valuation."
Contemporary Accounting Research, Vol. 11, No. 2, 1995, pp. 661-687.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["V", "MA", "AXP"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2022-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_residual_income().xs("Residual Income", level=1)
```

Which returns:

|     |        2022 |        2023 |        2024 |        2025 |
|:----|------------:|------------:|------------:|------------:|
| AXP | 5.62881e+09 | 5.94452e+09 | 7.56109e+09 | 7.62666e+09 |
| MA  | 9.35653e+09 | 1.06972e+10 | 1.23826e+10 | 1.44721e+10 |
| V   | 1.24393e+10 | 1.48221e+10 | 1.71906e+10 | 1.69441e+10 |

---

## get_present_value_of_growth_opportunities
The Present Value of Growth Opportunities (PVGO) is a financial metric that represents the present value of a company's future growth opportunities. It is calculated as the difference between the share price and the value of the company's current earnings as a perpetuity without growth, i.e. Earnings per Share divided by the Cost of Equity.

The formula is as follows:

$$
\text{PVGO} = \text{Stock Price} - \frac{\text{Earnings Per Share}}{\text{Cost of Equity}}
$$

**Also known as:** PVGO, growth value.

**Args:**

- <u>calculate_daily (bool, optional):</u> Whether to calculate the PVGO using daily historical data.
Defaults to False.
- <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
- <u>include_dividends (bool, optional):</u> Whether to deduct Preferred Dividends Paid from Net
Income when calculating the Earnings per Share, so that the earnings figure reflects what is
attributable to common shareholders only. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. The window counts
calendar periods, so a period without a report makes it NaN. Defaults to None.
- <u>market_risk_premium (float &#124; None, optional):</u> The annual equity risk premium the Cost of Equity
uses. Defaults to None, which takes the equity risk premium of each company's country
(Damodaran's Total Equity Risk Premium, see get_market_risk_premium) and, where that is
not available, the benchmark's average return above the risk-free rate over the data.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the PVGO values.

**Notes:**

- The no-growth value (Earnings per Share / r) is discounted at the Cost of Equity, since both
the share price and the Earnings per Share are equity-only, per-share quantities (Brealey, Myers
and Allen, "Principles of Corporate Finance"; Bodie, Kane and Marcus, "Investments"). The Cost of
Equity is the CAPM Cost of Equity of `get_weighted_average_cost_of_capital`.
- The Cost of Equity uses the same `trailing` as the Earnings per Share, so both cover the same
span (with quarterly data, a quarter without `trailing` and a year with trailing=4).
- When the Earnings per Share is negative, the no-growth value is negative and the PVGO
exceeds the share price, which has no meaningful interpretation.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NVDA", "TXN", "ADI"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2022-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_present_value_of_growth_opportunities()
```

Which returns:

| Date   |      ADI |     NVDA |      TXN |
|:-------|---------:|---------:|---------:|
| 2022   |  84.5011 |  18.9955 |  44.4789 |
| 2023   |  91.829  |  51.8345 |  96.3404 |
| 2024   | 196.881  | 124.329  | 136.656  |
| 2025   | 193.895  | nan      | 119.909  |

---

## get_graham_number
Calculate the Graham Number, a conservative estimate of a stock's fair value based on its earnings and book value, as devised by Benjamin Graham.

The Graham Number is intended as an upper bound on the price a defensive investor should pay for a stock. It is most meaningful for stable, profitable companies with positive book value - for companies with negative earnings or negative book value the result is not meaningful (the square root of a negative number is undefined and will show up as NaN).

The formula is as follows:

$$
\text{Graham Number} = \sqrt{22.5 \cdot \text{Earnings per Share} \cdot \text{Book Value per Share}}
$$

The constant 22.5 is Graham's limit of a price-to-earnings ratio of 15 times a price-to-book ratio of 1.5, so the Graham Number is the price at which the product of the two ratios reaches that limit. For companies whose value lies mostly in intangibles, or that buy back many shares, book value is small and the Graham Number sits far below the market price.

**Also known as:** Graham fair value.

**Args:**

- <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. The window counts
calendar periods, so a period without a report makes it NaN. Defaults to None, which uses 4
(the trailing twelve months of earnings) with quarterly data and a single period with yearly
data.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the Graham Number values.

**Notes:**

- Graham's limits of 15 times earnings and 1.5 times book value refer to annual earnings, so
with quarterly data the Earnings per Share are the sum of the last four quarters by default.
- Earnings and Book Value per Share use the Weighted Average Shares Diluted (or the Weighted
Average Shares with diluted=False).
- Only the Earnings per Share are trailing: the earnings are a flow over the trailing periods,
divided by the average shares over those periods. The Book Value per Share is a stock, the Total
Shareholder Equity minus the Preferred Stock at the end of the period divided by the shares of
that period.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["BAC", "C", "WFC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_graham_number()
```

Which returns:

|     |     2021 |     2022 |    2023 |     2024 |     2025 |
|:----|---------:|---------:|--------:|---------:|---------:|
| BAC |  47.9904 |  46.3468 | 47.4941 |  50.4045 |  56.4118 |
| C   | 142.751  | 120.826  | 93.472  | 117.004  | 127.785  |
| WFC |  68.3912 |  55.5576 | 69.7188 |  74.7554 |  85.6834 |

---

## get_graham_intrinsic_value
Calculate the intrinsic value of a share with Benjamin Graham's growth formula, the value of a growth stock from its earnings, their expected growth and the yield of high grade corporate bonds.

Graham gave the formula in The Intelligent Investor (fourth revised edition, 1973, chapter 11) as Earnings per Share x (8.5 + 2g), with 8.5 the price-to-earnings ratio of a company without growth and g the growth rate of its earnings expected over the next 7 to 10 years, in percent. In 1974 he scaled it by 4.4 / Y, with 4.4 the average yield of AAA corporate bonds in 1962 and Y their current yield, so that the value falls when interest rates rise.

The formula is as follows:

$$
\text{Intrinsic Value} = \frac{\text{Earnings per Share} \cdot (8.5 + 2 x g) \cdot 4.4}{Y}
$$

Graham wrote g and Y in percent (5 for 5%). The growth rate and the bond yield of this method are decimals like every rate in the Finance Toolkit (0.05 for 5%), and the formula multiplies them by 100 before it applies Graham's constants, so the value is Graham's. The bond yield is Moody's seasoned Aaa corporate bond yield, the yield to maturity of bonds with 20 years or more to maturity that Moody's publishes on their semi-annual coupon basis, used as published, as Graham's 4.4 was.

Graham meant the formula as a way to compare growth stocks and warned that growth projections are unreliable: a higher g raises the value without limit, so the value of a fast grower rests mostly on the growth assumed. A company with a loss has no value by the formula, so it is NaN.

**Also known as:** Graham formula, Graham growth formula, Benjamin Graham intrinsic value, revised Graham formula.

**Args:**

- <u>growth_rate (float, list or dict, optional):</u> The expected annual growth rate of the
earnings per share over the next 7 to 10 years, as a decimal: one number, or a
list or dict with a rate per ticker. Defaults to None, which uses the compound
annual growth of the company's Earnings per Share over the 10 years up to each
period (or all the years before it when there are fewer, at least three, NaN
with less history), kept within 0 and 0.20, the range of Graham's own table of
growth rates, and NaN where the earnings at either end are not positive.
- <u>bond_yield (float, list or dict, optional):</u> The yield of AAA corporate bonds, as a
decimal: one number, or a list or dict with a yield per ticker. Defaults to None,
which uses Moody's seasoned Aaa corporate bond yield (FRED series DAAA) on the
last day up to the end of each fiscal period, which needs a FRED API key.
- <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. The window counts
calendar periods, so a period without a report makes it NaN. Defaults to None, which uses 4
(the trailing twelve months of earnings) with quarterly data and a single period with yearly
data.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: DataFrame containing the intrinsic value per share.

**Notes:**

- Graham's formula takes the earnings of the last twelve months, so with quarterly data the
Earnings per Share are the sum of the last four quarters by default; it is the Net Income divided
by the Weighted Average Shares Diluted (or the Weighted Average Shares with diluted=False), as in
`get_graham_number`.
- The default growth rate looks back, while Graham's g is the growth expected ahead: pass a
growth_rate (e.g. from analyst estimates, see `toolkit.get_analyst_estimates`) to value on a
forecast. Each period only uses the earnings up to it, and the bond yield of the end of that
period, so no period is valued with figures that were only known later. The growth reaches back
as far as the statements the Toolkit holds (a year before the start date) and needs three
years of them, so the first periods are NaN and an earlier start_date gives a longer growth
window.
- Compare the value with the share price (`toolkit.get_historical_data`) for Graham's margin of
safety.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["KO", "PEP", "JNJ"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    fred_api_key="FRED_API_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_graham_intrinsic_value()
```

Which returns:

|     |   2021 |   2022 |    2023 |     2024 |     2025 |
|:----|-------:|-------:|--------:|---------:|---------:|
| JNJ |    nan |    nan | 630.081 |  51.9832 | 349.49   |
| KO  |    nan |    nan |  72.556 |  50.1366 |  76.9353 |
| PEP |    nan |    nan | 160.224 | 138.396  |  74.4379 |

---

## get_reverse_discounted_cash_flow
Calculate the growth rate the share price implies, a reverse Discounted Cash Flow (DCF). Instead of estimating growth to arrive at a value, it takes the current share price as given and solves for the yearly cash flow growth over the projection periods at which the DCF value per share equals that price. The answer is the market's expectation, which can then be compared with the company's history: an implied growth far above what the company has achieved signals optimism.

The DCF is the same as in `get_intrinsic_valuation`, by default on the Free Cash Flow to the Firm:

$$
\text{Cash Flow Projection}_{t} = \text{Cash Flow}_{t-1} \cdot (1 + \text{Implied Growth Rate})
$$

$$
\text{Terminal Value} = \frac{\text{Last Projection} \cdot (1 + \text{Perpetual Growth Rate})}{\text{WACC} - \text{Perpetual Growth Rate}}
$$

$$
\text{Equity Value} = \text{Present Value of Projections and Terminal Value} + \text{Cash} + \text{Short Term Investments} - \text{Total Debt} - \text{Minority Interest} - \text{Preferred Stock}
$$

$$
\text{Implied Growth Rate solves} \;\frac{\text{Equity Value}}{\text{Shares Outstanding}} = \text{Share Price}
$$

For more information, see the following book:

- Rappaport, A. and Mauboussin, M.J. (2001). "Expectations Investing: Reading Stock Prices for Better Returns." Harvard Business School Press.

**Also known as:** reverse DCF, market-implied growth, expectations investing.

**Args:**

- <u>perpetual_growth_rate (float &#124; dict[str, float], optional):</u> The growth after the
projection periods, one number or a number per ticker. Defaults to the
long-run growth rate of 2.5%.
- <u>weighted_average_cost_of_capital (float &#124; dict[str, float] &#124; None, optional):</u>
The discount rate, one number or a number per ticker. Defaults to None,
which uses the latest Weighted Average Cost of Capital of each company,
calculated over a year (the last 4 quarters with quarterly data) whatever
`trailing` the cash flows use, as the rate is a yearly one.
- <u>periods (int, optional):</u> The number of projection periods. Defaults to 5.
- <u>cash_flow_type (str, optional):</u> The cash flow to project: "Free Cash Flow to
Firm" (see `get_free_cash_flow_to_firm`), the cash flow to debt and equity
holders that the WACC discounts into an enterprise value; or "Free Cash Flow"
or "Operating Cash Flow" as reported, which are after interest (cash flows
to equity), so that discounting them at the WACC and subtracting the debt
counts the cost of debt twice. Defaults to "Free Cash Flow to Firm".
- <u>trailing (int &#124; None, optional):</u> Sum the cash flow over this many periods (e.g.
4 quarters) instead of taking the latest one. The window counts calendar
periods, so a period without a report makes it NaN. Defaults to None, which
sums the last 4 quarters (a trailing twelve months) for quarterly data and
takes the latest year otherwise, as the projection periods are years.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker the Share Price, the Cash Flow used, the Weighted
Average Cost of Capital, the Perpetual Growth Rate, the Implied Growth Rate and,
for comparison, the Historical Growth Rate (the compound annual growth of the
cash flow as used, so summed over `trailing` periods where set, from the first
to the latest reported period).

**Notes:**

- A negative cash flow, or a discount rate at or below the perpetual growth rate,
has no implied growth rate and gives NaN.
- The Historical Growth Rate counts four quarters as a year with quarterly data and
is NaN when the first or latest cash flow is not positive. The years are those
between the first and the latest cash flow on the calendar, and a trailing sum
that includes a missing period is NaN rather than one over more periods.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "NVDA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_reverse_discounted_cash_flow(weighted_average_cost_of_capital=0.09)
```

Which returns:

|      |   Share Price |   Cash Flow |   Weighted Average Cost of Capital |   Perpetual Growth Rate |   Implied Growth Rate |   Historical Growth Rate |
|:-----|--------------:|------------:|-----------------------------------:|------------------------:|----------------------:|-------------------------:|
| AAPL |        271.86 | 8.62639e+10 |                               0.09 |                   0.025 |                0.3068 |                   0.0545 |
| MSFT |        483.62 | 7.0121e+10  |                               0.09 |                   0.025 |                0.328  |                   0.1183 |
| NVDA |        186.5  | 5.98933e+10 |                               0.09 |                   0.025 |                0.4431 |                   1.0031 |

---

## get_earnings_power_value
Calculate the Earnings Power Value (EPV), the value of a company's current earnings if they never grew. Bruce Greenwald uses it to separate what is known (today's earnings power) from what is speculative (growth): the operating margin is averaged over several years and applied to the latest yearly revenue, taxed, and capitalized at the cost of capital.

- Normalized Operating Income = Average Operating Margin * Latest Revenue
- NOPAT = Normalized Operating Income * (1 - Average Tax Rate)
- Earnings Power Value = NOPAT / WACC
- EPV per Share = (EPV + Cash + Short Term Investments - Total Debt - Minority Interest - Preferred Stock) / Shares Outstanding

A share price well above the EPV per share means the market pays for growth, which only adds value when the company earns more than its cost of capital on it.

For more information, see the following book:

- Greenwald, B.C.N., Kahn, J., Sonkin, P.D. and van Biema, M. (2001). "Value Investing: From Graham to Buffett and Beyond." Wiley.

**Also known as:** EPV, no-growth value, Greenwald valuation.

**Args:**

- <u>weighted_average_cost_of_capital (float &#124; dict[str, float] &#124; None, optional):</u>
The discount rate, one number or a number per ticker. Defaults to None,
which uses the latest Weighted Average Cost of Capital of each company,
calculated over a year (the last 4 quarters with quarterly data) whatever
`trailing` the cash flows use, as the rate is a yearly one.
- <u>periods (int, optional):</u> The number of periods the operating margin and tax rate
are averaged over; with `trailing`, the number of trailing sums, `trailing`
calendar periods apart so that they do not overlap, counted back from the
latest reported one. A sum that includes a missing period is left out of
the average. Defaults to 5.
- <u>trailing (int &#124; None, optional):</u> Sum the revenue, operating income, taxes and
income before tax over this many periods (e.g. 4 quarters), so that the
margin is applied to a year of revenue. The window counts calendar periods,
so a period without a report makes it NaN. Defaults to None, which uses 4 (a
trailing twelve months) for quarterly data and the yearly figures otherwise.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker the Average Operating Margin, Normalized Operating
Income, Tax Rate, Normalized NOPAT, Weighted Average Cost of Capital, Earnings
Power Value, Equity Value, Earnings Power Value per Share, Share Price and the
Price to EPV ratio.

**Notes:**

- Maintenance capital expenditure is assumed to equal depreciation, so operating
income stands in for the cash the business could pay out without shrinking.
- With quarterly data and the default trailing twelve months, the margins of the
last five years are averaged and applied to the revenue of the last four quarters,
as with yearly data.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "KO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_earnings_power_value(weighted_average_cost_of_capital=0.08)
```

Which returns:

|      |   Average Operating Margin |   Normalized Operating Income |   Tax Rate |   Normalized NOPAT |   Weighted Average Cost of Capital |   Earnings Power Value |   Equity Value |   Earnings Power Value per Share |   Share Price |   Price to EPV |
|:-----|---------------------------:|------------------------------:|-----------:|-------------------:|-----------------------------------:|-----------------------:|---------------:|---------------------------------:|--------------:|---------------:|
| AAPL |                     0.3067 |                   1.27656e+11 |     0.1679 |        1.06229e+11 |                               0.08 |            1.32786e+12 |    1.27018e+12 |                          84.652  |        271.86 |         3.2115 |
| KO   |                     0.2534 |                   1.21476e+10 |     0.1861 |        9.88662e+09 |                               0.08 |            1.23583e+11 |    8.81348e+10 |                          20.4347 |         69.91 |         3.4211 |
| MSFT |                     0.4314 |                   1.2153e+11  |     0.1636 |        1.01652e+11 |                               0.08 |            1.27066e+12 |    1.25303e+12 |                         167.853  |        483.62 |         2.8812 |

---

## get_monte_carlo_intrinsic_valuation
Calculate the distribution of the intrinsic value per share when the inputs of the Discounted Cash Flow model are uncertain. A single DCF value hides how sensitive it is to its assumptions; here the growth rate, the perpetual growth rate and the discount rate are drawn from normal distributions around their expected values in every simulation, and the DCF of `get_intrinsic_valuation` is calculated for each draw. The spread of the outcomes, and the probability that the value exceeds the share price, show how robust the conclusion is.

Draws in which the discount rate does not exceed the perpetual growth rate by at least half a percentage point are redrawn, as the terminal value is undefined there.

For more information, see the following book:

- Damodaran, A. (2012). "Investment Valuation: Tools and Techniques for Determining the Value of Any Asset." Wiley, 3rd edition, chapter 33 (probabilistic approaches).

**Also known as:** Monte Carlo DCF, probabilistic valuation, DCF simulation.

**Args:**

- <u>growth_rate (float &#124; dict[str, float] &#124; None, optional):</u> The expected yearly
growth over the projection periods, one number or a number per ticker. Defaults
to None, which uses the growth the company's reinvestment supports, as in
`get_intrinsic_valuation`.
- <u>growth_rate_volatility (float, optional):</u> The standard deviation of the growth
rate. Defaults to 0.02.
- <u>perpetual_growth_rate (float &#124; dict[str, float] &#124; None, optional):</u> The expected
growth after the projection periods. Defaults to None, which uses the company's
growth kept within 0 and the long-run growth rate of 2.5% (2.5% where it has none).
- <u>perpetual_growth_rate_volatility (float, optional):</u> Its standard deviation.
Defaults to 0.005.
- <u>weighted_average_cost_of_capital (float &#124; dict[str, float] &#124; None, optional):</u>
The expected discount rate. Defaults to None, which uses the latest Weighted
Average Cost of Capital of each company, calculated over a year (the last 4
quarters with quarterly data) whatever `trailing` the cash flows use, as the
rate is a yearly one.
- <u>weighted_average_cost_of_capital_volatility (float, optional):</u> Its standard
deviation. Defaults to 0.01.
- <u>periods (int, optional):</u> The number of projection periods. Defaults to 5.
- <u>simulations (int, optional):</u> The number of simulations. Defaults to 10,000.
- <u>cash_flow_type (str, optional):</u> The cash flow to project: "Free Cash Flow to
Firm" (see `get_free_cash_flow_to_firm`), the cash flow to debt and equity
holders that the WACC discounts into an enterprise value; or "Free Cash Flow"
or "Operating Cash Flow" as reported, which are after interest (cash flows
to equity), so that discounting them at the WACC and subtracting the debt
counts the cost of debt twice. Defaults to "Free Cash Flow to Firm".
- <u>trailing (int &#124; None, optional):</u> Sum the cash flow over this many periods (e.g.
4 quarters) instead of taking the latest one. The window counts calendar
periods, so a period without a report makes it NaN. Defaults to None, which
sums the last 4 quarters (a trailing twelve months) for quarterly data and
takes the latest year otherwise, as the projection periods are years.
- <u>seed (int &#124; None, optional):</u> The seed of the random numbers, so that results
can be reproduced. Defaults to 0; None gives different draws every time.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker the Mean, Standard Deviation and the 5th, 25th, 50th,
75th and 95th Percentile of the value per share, the Share Price and the
Probability Undervalued (the share of simulations above the share price).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_monte_carlo_intrinsic_valuation()
```

Which returns:

|      |     Mean |   Standard Deviation |   5th Percentile |   25th Percentile |   50th Percentile |   75th Percentile |   95th Percentile |   Share Price |   Probability Undervalued |
|:-----|---------:|---------------------:|-----------------:|------------------:|------------------:|------------------:|------------------:|--------------:|--------------------------:|
| AAPL |  83.9988 |              16.3235 |          62.3819 |           72.7029 |           81.6781 |           92.6049 |           113.888 |        271.86 |                    0.0001 |
| MSFT | 209.732  |              54.4736 |         146.029  |          174.188  |          199.786  |          233.56   |           305.64  |        483.62 |                    0.0026 |

---

## get_peer_comparison
Compare every company with its peers on valuation, profitability, growth and leverage. For each metric it shows the company's latest value, the median and mean of its peers and the company's percentile among them (the share of peers with a lower value), which tells at a glance whether a company is expensive or cheap, and better or worse run, than comparable companies.

The metrics are the Price-to-Earnings, EV-to-EBITDA, Price-to-Book and Price-to-Sales ratios, the Gross, Operating and Net Profit Margin, the Return on Equity and on Invested Capital, Revenue Growth, the Debt-to-Equity ratio and the Dividend Yield, all of the latest period up to the Toolkit's end date: the fiscal year, or with quarterly=True the quarter, with the ratios over the trailing year and the Revenue Growth over the same quarter a year earlier. The peers are retrieved with the Toolkit's settings (quarterly, point_in_time and convert_currency), so the Company column equals the Toolkit's own ratios of that period.

The Peer Mean of the four valuation multiples is the harmonic mean of the positive values, the standard average of multiples: the arithmetic mean is dominated by peers with earnings (or book value, or sales) close to zero, and a negative multiple says nothing about the price paid. The other metrics use the arithmetic mean.

For more information, see the following papers:

- Baker, M. and Ruback, R.S. (1999). "Estimating Industry Multiples." Working paper, Harvard University.
- Liu, J., Nissim, D. and Thomas, J. (2002). "Equity Valuation Using Multiples." Journal of Accounting Research, 40(1), 135-172.

**Also known as:** comparable companies analysis, comps, relative valuation, peer group analysis.

**Args:**

- <u>peers (dict[str, list[str]] &#124; None, optional):</u> The peers per ticker, e.g.
{"AAPL": ["MSFT", "GOOGL"]}. Defaults to None, which uses the peers
Financial Modeling Prep lists for each company (same sector and exchange,
similar size).
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker and metric the Company value, the Peer Median and Peer
Mean (harmonic for the valuation multiples), the Percentile (0 to 1) and the
number of Peers with a value.

**Notes:**

- A high percentile is not always good: for valuation ratios it means expensive,
for margins and returns it means strong.
- Retrieving the peers' financial statements takes a few seconds per peer.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_peer_comparison()
```

Which returns:

|                                        |   Company |   Peer Median |   Peer Mean |   Percentile |   Peers |
|:---------------------------------------|----------:|--------------:|------------:|-------------:|--------:|
| ('MSFT', 'Price-to-Earnings')          |   36.4636 |       30.6062 |     29.3028 |          0.7 |      10 |
| ('MSFT', 'EV-to-EBITDA')               |   22.9332 |       20.9841 |     19.0334 |          0.6 |      10 |
| ('MSFT', 'Price-to-Book')              |   10.8105 |        7.3435 |      6.5553 |          0.7 |      10 |
| ('MSFT', 'Price-to-Sales')             |   13.1802 |        6.2949 |      4.5172 |          1   |      10 |
| ('MSFT', 'Gross Margin')               |    0.6882 |        0.6508 |      0.6211 |          0.5 |      10 |
| ('MSFT', 'Operating Margin')           |    0.4562 |        0.1875 |      0.2187 |          1   |      10 |
| ('MSFT', 'Net Profit Margin')          |    0.3615 |        0.1602 |      0.1816 |          1   |      10 |
| ('MSFT', 'Return on Equity')           |    0.3328 |        0.2406 |      0.3172 |          0.6 |      10 |
| ('MSFT', 'Return on Invested Capital') |    0.2576 |        0.1339 |      0.1691 |          0.8 |      10 |
| ('MSFT', 'Revenue Growth')             |    0.1493 |        0.0962 |      0.1108 |          0.8 |      10 |
| ('MSFT', 'Debt-to-Equity')             |    0.3266 |        0.22   |      0.9011 |          0.6 |      10 |
| ('MSFT', 'Dividend Yield')             |    0.0065 |        0.008  |      0.009  |          0.5 |      10 |

---

