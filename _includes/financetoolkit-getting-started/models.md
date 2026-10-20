## Getting Started

The Models module combines ratios, market data and financial statements into the well-known models an analyst reaches for when a single ratio isn't enough: DuPont analysis to see what drives Return on Equity, the Weighted Average Cost of Capital (WACC), a Discounted Cash Flow (DCF) valuation, the Altman Z-Score, Piotroski F-Score and Beneish M-Score for financial health and earnings quality, and growth models such as the Sustainable Growth Rate and the Graham Number. Every model is calculated for each ticker and each period, so you see how the result changed over time rather than a single snapshot.

This section uses Apple, Tesla, Meta and Amazon from 2005 onwards.

### Loading the Data

The Models module is part of the `Toolkit` class. Financial statements, historical prices and treasury rates are collected the first time a model needs them and reused for every call after that, which keeps the number of requests to a minimum. This example uses annual data; add `quarterly=True` for quarterly data, which requires a premium plan from Financial Modeling Prep.

To load the data for the four companies:

```python
import numpy as np
import pandas as pd

from financetoolkit import Toolkit

companies = Toolkit(
    ["AAPL", "TSLA", "META", "AMZN"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2005-01-01",
)
```

### Extended DuPont Analysis

The DuPont analysis explains Return on Equity by splitting it into parts. The extended (five-step) version multiplies the interest burden (how much of operating profit survives interest), the tax burden (how much survives tax), the operating margin, the asset turnover and the equity multiplier. Two companies with the same ROE can get there in very different ways: one through margins, another through leverage, and that difference matters for how sustainable the return is.

To run the extended DuPont analysis for every company:

```python
companies.models.get_extended_dupont_analysis()
```

Which gives the five components and the resulting ROE, here for the last ten years with a tab per company:

{% include ft-chart.html id="models-dupont-extended" src="/assets/data/financetoolkit-guides/models.json" label="Extended DuPont analysis of Apple, Tesla, Meta and Amazon" %}

Apple's ROE of well over 100% comes mostly from its equity multiplier: years of share buybacks have left it with very little book equity, so each dollar of profit is spread over a small equity base. Meta earns an even higher operating margin with little leverage, which is why its ROE is far lower but arguably of higher quality. Amazon's early years (not shown in the chart) are an example of why the decomposition matters: with equity close to zero in 2005, its ROE came out at several thousand percent.

### Weighted Average Cost of Capital

The WACC is the blended return a company has to earn for its shareholders and lenders, weighted by the market value of equity and debt. The cost of equity follows from the Capital Asset Pricing Model (the risk-free rate plus beta times the market risk premium), the cost of debt from interest expense over total debt, after tax.

Like almost every function in the Toolkit, the WACC accepts `growth=True` to return the change from one period to the next instead of the level, and `lag` sets how many periods back that change is measured. A list of lags returns all of them at once. To calculate the growth of every WACC component over one, two and three years:

```python
companies.models.get_weighted_average_cost_of_capital(growth=True, lag=[1, 2, 3])
```

Which gives, for Apple's WACC itself:

| Apple's WACC growth | 2022 | 2023 | 2024 | 2025 |
|:--------------------|-----:|-----:|-----:|-----:|
| Lag 1 | -1.65 | -2.19 | -0.15 | -0.12 |
| Lag 2 | -2.16 | -0.23 | -2.01 | -0.26 |
| Lag 3 | -1.53 | 0.38 | -0.35 | -1.89 |

The level itself is more useful for most analyses, and `standardize=True` converts each component into standard deviations from its own historical mean, which puts the market value of equity (in dollars) and the cost of debt (a rate) on the same scale. `show_full_results=True` returns the components next to the WACC. To get both views:

```python
wacc = companies.models.get_weighted_average_cost_of_capital()

companies.models.get_weighted_average_cost_of_capital(
    standardize=True, show_full_results=True
).loc["AMZN"]
```

Which shows the WACC of the four companies over the last ten years, and in the second tab Amazon's components in standard deviations:

{% include ft-chart.html id="models-wacc" src="/assets/data/financetoolkit-guides/models.json" label="WACC of Apple, Tesla, Meta and Amazon, and Amazon's standardized WACC components" %}

<div class="fs-callout" markdown="1"><p class="fs-callout__title">The market return is the realized return of that year</p>

The cost of equity uses the benchmark's realized return in each year as the market return, so the WACC follows the market: it turned negative for all four companies in 2022, when the S&P 500 fell, and jumped in 2023. For a valuation you will usually want a long-run expected market return instead, for example by taking an average of the WACC over several years.
</div>

### Altman Z-Score and Piotroski F-Score

The Altman Z-Score combines five ratios (working capital, retained earnings, EBIT, the market value of equity against liabilities, and sales, each relative to total assets) into one measure of the chance of bankruptcy. A score above 2.99 is considered safe, below 1.81 a sign of distress. The Piotroski F-Score awards one point for each of nine criteria on profitability, leverage and liquidity, and operating efficiency, so a score of 8 or 9 points to a company whose fundamentals are improving and 0 to 2 to one whose fundamentals are deteriorating.

To calculate the Altman Z-Score and select Amazon:

```python
altman_z_score = companies.models.get_altman_z_score()

altman_z_score.loc["AMZN"]
```

Which gives the Z-Score of the four companies with both thresholds, and Amazon's five components in the second tab:

{% include ft-chart.html id="models-altman" src="/assets/data/financetoolkit-guides/models.json" label="Altman Z-Score of Apple, Tesla, Meta and Amazon, and Amazon's components" %}

All four are far into the safe zone in recent years; Amazon came closest to the threshold in 2022, at about 2.9, when its market value dropped and EBIT turned slightly negative.

To calculate the Piotroski F-Score and select Apple:

```python
piotroski_score = companies.models.get_piotroski_score()

piotroski_score.loc["AAPL"]
```

Which shows, for the last five years, which criteria Apple met (1) or missed (0):

| Criterion | 2021 | 2022 | 2023 | 2024 | 2025 |
|:----------|-----:|-----:|-----:|-----:|-----:|
| Return on Assets | 1 | 1 | 1 | 1 | 1 |
| Operating Cash Flow | 1 | 1 | 1 | 1 | 1 |
| Change in Return on Assets | 1 | 1 | 0 | 0 | 1 |
| Accruals | 1 | 1 | 1 | 1 | 0 |
| Change in Leverage | 0 | 1 | 1 | 1 | 1 |
| Change in Current Ratio | 0 | 0 | 1 | 0 | 1 |
| Number of Shares | 0 | 1 | 1 | 1 | 1 |
| Gross Margin | 1 | 1 | 1 | 1 | 1 |
| Asset Turnover | 1 | 1 | 0 | 1 | 1 |
| **Piotroski Score** | **6** | **8** | **7** | **7** | **8** |

To compare the total score of all four companies over time:

```python
piotroski_score.loc[:, "Piotroski Score", :].T
```

Which gives:

{% include ft-chart.html id="models-piotroski" src="/assets/data/financetoolkit-guides/models.json" label="Piotroski F-Score of Apple, Tesla, Meta and Amazon per year" %}

### Enterprise Value and Intrinsic Valuation

The Enterprise Value breakdown shows how the Toolkit gets from market capitalization to enterprise value: add total debt, minority interest and preferred equity, and subtract cash. The intrinsic valuation runs a DCF: it projects free cash flow forward at a growth rate, adds a terminal value at the perpetual growth rate, discounts both at the WACC and divides the resulting equity value by the number of shares. The three inputs are yours to set, which makes it easy to test how sensitive the fair value is to each of them.

To get the Enterprise Value breakdown, and a DCF with 5% growth, 2.5% perpetual growth and a WACC of 9.4%:

```python
companies.models.get_enterprise_value_breakdown()

companies.models.get_intrinsic_valuation(
    growth_rate=0.05, perpetual_growth_rate=0.025, weighted_average_cost_of_capital=0.094
)
```

Which gives, for Apple's Enterprise Value in USD billions:

| Apple (USD billions) | 2023 | 2024 | 2025 |
|:---------------------|-----:|-----:|-----:|
| Market Capitalization | 3,008 | 3,831 | 4,068 |
| + Total Debt | 124 | 119 | 112 |
| + Minority Interest | 0 | 0 | 0 |
| + Preferred Equity | 0 | 0 | 0 |
| - Cash and Cash Equivalents | 30 | 30 | 36 |
| **Enterprise Value** | **3,102** | **3,920** | **4,145** |

And for the intrinsic value per share next to the latest share price:

| | Intrinsic value | Latest price |
|:--|--:|--:|
| Apple | $103.69 | $339.50 |
| Tesla | $31.44 | $373.71 |
| Meta | $277.39 | $694.25 |
| Amazon | $5.63 | $262.63 |

With these inputs, every company trades well above its DCF value, which mostly says that the market expects much more than 5% growth. Amazon shows the limits of a free cash flow DCF: it reinvests most of its operating cash flow, so its free cash flow, and with it the intrinsic value, is small compared to the size of the business.

### DuPont Analysis and Growth Opportunities

The base DuPont analysis splits Return on Equity into three parts: the net profit margin, the asset turnover and the equity multiplier, which shows whether ROE is driven by profitability, efficient use of assets or leverage. The Present Value of Growth Opportunities (PVGO) splits the share price into the value of the current earnings, if they stayed flat forever (earnings per share divided by the WACC), and the remainder, which is what the market pays for future growth.

To run the DuPont analysis standardized for Apple, and the PVGO for every company:

```python
companies.models.get_dupont_analysis(standardize=True).loc["AAPL"]

companies.models.get_present_value_of_growth_opportunities()
```

Which shows how far each component of Apple's ROE is from its own historical average, in standard deviations:

{% include ft-chart.html id="models-dupont-standardized" src="/assets/data/financetoolkit-guides/models.json" label="Standardized DuPont analysis for Apple" %}

And the PVGO per share of the four companies:

{% include ft-chart.html id="models-pvgo" src="/assets/data/financetoolkit-guides/models.json" label="Present Value of Growth Opportunities of Apple, Tesla, Meta and Amazon" %}

At the end of 2025, about $550 of Meta's share price of roughly $660 was growth the market expected rather than earnings it already made. The sharp drops in 2011 and 2015 come from a WACC of about 1% in those flat market years, which makes earnings divided by the WACC very large; it is one more reason to smooth the WACC before using it in a valuation.

### Beneish M-Score

The Beneish M-Score is a probabilistic model for detecting earnings manipulation, a companion to the Altman Z-Score and the Piotroski F-Score. It combines eight indices, such as days sales in receivables, gross margin, asset quality and total accruals, each comparing this year to last year. A score above roughly -1.78 suggests a higher likelihood that earnings are being manipulated.

To calculate the Beneish M-Score and select Meta:

```python
beneish_m_score = companies.models.get_beneish_m_score()

beneish_m_score.loc["META"]
```

Which gives the M-Score of the four companies over the last ten years against the -1.78 threshold, and Meta's eight indices in the second tab:

{% include ft-chart.html id="models-beneish" src="/assets/data/financetoolkit-guides/models.json" label="Beneish M-Score of Apple, Tesla, Meta and Amazon, and Meta's components" %}

Tesla crossed the threshold in 2023, at about -1.6, while the other three stay well below it. A single year above it is a reason to look closer at the components (a jump in receivables or accruals, for example), not proof of manipulation.

### Sustainable and Internal Growth Rate

The Sustainable Growth Rate (SGR) and the Internal Growth Rate (IGR) estimate how fast a company can grow without raising new equity. The SGR is ROE times the retention ratio and assumes leverage stays the same; the IGR is based on ROA and assumes no new debt at all, so it is always the more conservative of the two.

To calculate both:

```python
companies.models.get_sustainable_growth_rate()

companies.models.get_internal_growth_rate()
```

Which gives, for the last ten years with a tab per measure:

{% include ft-chart.html id="models-growth-rates" src="/assets/data/financetoolkit-guides/models.json" label="Sustainable and internal growth rate of Apple, Tesla, Meta and Amazon" %}

Apple's SGR of over 100% is another effect of its small equity base; its IGR of around 30% is the more realistic figure for how fast it could grow from its own profits.

### Graham Number

The Graham Number is Benjamin Graham's conservative estimate of the most a defensive investor should pay for a share: the square root of 22.5 times earnings per share times book value per share. It only has meaning for profitable companies with a positive book value; otherwise the result is empty.

To compare the latest Graham Number with the current share price:

```python
graham_number = companies.models.get_graham_number().iloc[:, -1]
current_price = companies.get_historical_data()["Adj Close"].iloc[-1].drop("Benchmark")

pd.DataFrame({"Graham Number": graham_number, "Current Price": current_price})
```

Which gives:

{% include ft-chart.html id="models-graham" src="/assets/data/financetoolkit-guides/models.json" label="Graham Number against the current share price of Apple, Tesla, Meta and Amazon" %}

None of the four comes close to Graham's limit, which is what you would expect for growth companies: the formula has no room for growth at all and was written for a very different kind of stock.

### Using the Models Directly

Every model is also available as a plain function in `financetoolkit.models`, so you can run it on your own numbers without the `Toolkit` class. This is useful when you have data from another source or want to test a scenario. The example below fills the DuPont analysis with Apple's reported figures for fiscal 2018 to 2022:

```python
from financetoolkit.models import dupont_model

years = [2018, 2019, 2020, 2021, 2022]

dupont_model.get_dupont_analysis(
    net_income=pd.Series(
        [59531000000, 55256000000, 57411000000, 94680000000, 99803000000], index=years
    ),
    total_revenue=pd.Series(
        [265595000000, 260174000000, 274515000000, 365817000000, 394328000000],
        index=years,
    ),
    average_total_assets=pd.Series(
        [np.nan, 365725000000, 338516000000, 323888000000, 351002000000],
        index=years,
    ),
    average_total_equity=pd.Series(
        [np.nan, 107147000000, 90488000000, 65339000000, 63090000000], index=years
    ),
)
```

Which returns:

| | 2018 | 2019 | 2020 | 2021 | 2022 |
|:--|--:|--:|--:|--:|--:|
| Net Profit Margin | 0.2241 | 0.2124 | 0.2091 | 0.2588 | 0.2531 |
| Asset Turnover | | 0.7114 | 0.8109 | 1.1295 | 1.1234 |
| Equity Multiplier | | 3.4133 | 3.7410 | 4.9570 | 5.5635 |
| Return on Equity | | 0.5157 | 0.6345 | 1.4491 | 1.5819 |

These results closely match the figures Apple reports for those fiscal years, which end in September.

{% include ft-charts-script.html %}
