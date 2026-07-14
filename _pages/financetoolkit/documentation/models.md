---
title: Models
excerpt: The Models module is meant to execute well-known models such as DUPONT and the Discounted Cash Flow (DCF) model. These models are also directly related to the data retrieved from the Toolkit module.
description: The Models module is meant to execute well-known models such as DUPONT and the Discounted Cash Flow (DCF) model. These models are also directly related to the data retrieved from the Toolkit module.
author_profile: false
permalink: /projects/financetoolkit/docs/models
classes: wide-sidebar
layout: single
redirect_from:
    - /models
sidebar:
    nav: "financetoolkit-docs-models"
---

The Models module executes well-known models such as DuPont analysis and the Discounted Cash Flow (DCF) model, using data retrieved from the Toolkit module.

To install the FinanceToolkit it simply requires the following:

```python
pip install financetoolkit -U
```

{% include algolia.html %}

## get_dupont_analysis
Perform a Dupont analysis to breakdown the return on equity (ROE) into its components.

The Dupont analysis is a method used to dissect and understand the factors that drive a company's return on equity (ROE). It breaks down the ROE into three key components: Profit Margin, Asset Turnover, and Financial Leverage.

The formula is as follows:

- Profit Margin = Net Income / Revenue
- Asset Turnover = Revenue / Average Total Assets
- Financial Leverage = Average Total Assets / Average Total Equity
- ROE = Profit Margin * Asset Turnover * Financial Leverage

**Also known as:** DuPont, ROE decomposition, three-factor DuPont.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int | None, optional):</u> The trailing period to use for the calculation. Defaults to None.

**Returns:**

pd.DataFrame: DataFrame containing Dupont analysis results, including Profit Margin, Asset
Turnover, Financial Leverage, and the calculated ROE values.

**Notes:**

- The Profit Margin is the ratio of Net Income to Total Revenue, indicating the percentage of
revenue that translates into profit.
- Asset Turnover measures the efficiency of a company's use of its assets to generate sales
revenue.
- Financial Leverage represents the use of debt to finance a company's operations, which can
amplify returns as well as risks.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

dupont_analysis = toolkit.models.get_dupont_analysis()

dupont_analysis.loc["AAPL"]
```

Which returns:

|                   |   2021 |   2022 |   2023 |   2024 |   2025 |
|:------------------|-------:|-------:|-------:|-------:|-------:|
| Net Profit Margin | 0.2588 | 0.2531 | 0.2531 | 0.2397 | 0.2692 |
| Asset Turnover    | 1.0841 | 1.1206 | 1.0868 | 1.0899 | 1.1493 |
| Equity Multiplier | 5.255  | 6.1862 | 6.252  | 6.0251 | 5.5418 |
| Return on Equity  | 1.4744 | 1.7546 | 1.7195 | 1.5741 | 1.7142 |


---

## get_extended_dupont_analysis
Perform an Extended Dupont analysis to breakdown the return on equity (ROE) into its components, while considering additional financial metrics.

The Extended Dupont analysis is an advanced method used to break down the return on equity (ROE) into multiple components, providing a more detailed insight into the factors influencing a company's profitability. It considers additional metrics such as Return on Assets (ROA), Total Asset Turnover, Financial Leverage, and more.

The formula is as follows:

- Profit Margin = Net Income / Revenue
- Asset Turnover = Revenue / Average Total Assets
- Financial Leverage = Average Total Assets / Average Total Equity
- ROA = Net Income / Average Total Assets
- Total Asset Turnover = Revenue / Average Total Assets
- ROE = Profit Margin * Asset Turnover * Financial Leverage * ROA * Total Asset Turnover

**Also known as:** extended DuPont, five-factor DuPont, ROE breakdown.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int | None, optional):</u> The trailing period to use for the calculation. Defaults to None.

**Returns:**

pd.DataFrame: DataFrame containing Extended Dupont analysis results, including Profit Margin, Asset Turnover,
Financial Leverage, ROA, Total Asset Turnover, and the calculated ROE values.

**Notes:**

- The Profit Margin is the ratio of Net Income to Total Revenue, indicating the percentage of
revenue that translates into profit.
- Asset Turnover measures the efficiency of a company's use of its assets to generate
sales revenue.
- Financial Leverage represents the use of debt to finance a company's operations, which can
amplify returns as well as risks.
- Return on Assets (ROA) measures the efficiency of a company's use of its assets to
generate profit.
- Total Asset Turnover considers all assets, including both equity and debt financing.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

extended_dupont_analysis = toolkit.models.get_extended_dupont_analysis()

extended_dupont_analysis.loc["AAPL"]
```

Which returns:

|                         |   2021 |   2022 |   2023 |   2024 |   2025 |
|:------------------------|-------:|-------:|-------:|-------:|-------:|
| Interest Burden Ratio   | 0.9976 | 1.0028 | 1.005  | 0.9978 | 1.0024 |
| Tax Burden Ratio        | 0.869  | 0.8356 | 0.8486 | 0.7607 | 0.8419 |
| Operating Profit Margin | 0.2985 | 0.302  | 0.2967 | 0.3158 | 0.3189 |
| Asset Turnover          | 1.0841 | 1.1206 | 1.0868 | 1.0899 | 1.1493 |
| Equity Multiplier       | 5.255  | 6.1862 | 6.252  | 6.0251 | 5.5418 |
| Return on Equity        | 1.4744 | 1.7546 | 1.7195 | 1.5741 | 1.7142 |


---

## get_enterprise_value_breakdown
Calculate the Enterprise Value (EV) breakdown, providing a detailed view of its components.

The Enterprise Value breakdown includes the following components for each quarter or year:

- Share Price: The market price per share of the company's stock. - Market Capitalization (Market Cap): The total value of a company's outstanding common and preferred shares. - Debt: The sum of long-term and short-term debt on the company's balance sheet. - Preferred Equity: The value of preferred shares, if applicable. - Minority Interest: The equity value of a subsidiary with less than 50% ownership. - Cash and Cash Equivalents: The total amount of liquid assets including cash, marketable securities, and short-term investments.

The Enterprise Value is calculated as the sum of Market Cap, Debt, Preferred Equity, Minority Interest, minus Cash and Cash Equivalents.

This breakdown is displayed in a DataFrame for each company and includes the option to show growth values as well.

**Also known as:** EV breakdown, enterprise value components, EV bridge.

**Args:**

- <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: DataFrame containing the Enterprise Value breakdown, including the calculated components.

**Notes:**

- All the inputs must be in the same currency and unit for accurate calculations.
- The Enterprise Value is an important metric used for valuation and investment analysis.
- A positive Enterprise Value indicates that the company is financed primarily by equity and has excess cash.
- A negative Enterprise Value may indicate financial distress or unusual financial situations.
- Understanding the Enterprise Value breakdown can provide insights into the sources of a
company's value and potential risks.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

enterprise_value_breakdown = toolkit.models.get_enterprise_value_breakdown()

enterprise_value_breakdown.loc["AAPL"]
```

Which returns:

|                           |          2021 |          2022 |          2023 |          2024 |          2025 |
|:--------------------------|--------------:|--------------:|--------------:|--------------:|--------------:|
| Share Price               | 177.57        | 129.93        | 192.53        | 250.42        | 271.86        |
| Market Capitalization     |   2.9947e+12  |   2.12121e+12 |   3.04439e+12 |   3.8585e+12  |   4.07918e+12 |
| Total Debt                |   1.36522e+11 |   1.3248e+11  |   1.2393e+11  |   1.19059e+11 |   1.12377e+11 |
| Minority Interest         |   0           |   0           |   0           |   0           |   0           |
| Preferred Equity          |   0           |   0           |   0           |   0           |   0           |
| Cash and Cash Equivalents |   3.494e+10   |   2.3646e+10  |   2.9965e+10  |   2.9943e+10  |   3.5934e+10  |
| Enterprise Value          |   3.09629e+12 |   2.23005e+12 |   3.13835e+12 |   3.94761e+12 |   4.15562e+12 |


---

## get_weighted_average_cost_of_capital
The Weighted Average Cost of Capital (WACC) is a financial metric used to estimate the cost of capital for a company. It represents the average rate of return a company must pay to its investors for using their capital. WACC takes into account the cost of both equity and debt, weighted by their respective proportions in the company's capital structure.

The formula is as follows:

- Market Value of Equity = Share Price * Total Shares Outstanding - Market Value of Debt = Total Debt - Total Market Value = Market Value of Equity + Market Value of Debt - Cost of Equity = Risk Free Rate + Beta * (Benchmark Return - Risk Free Rate) - Cost of Debt = Interest Expense / Total Debt - WACC = (Market Value of Equity / Total Market Value) * Cost of Equity + (Market Value of Debt / Total Market Value) * Cost of Debt * (1 - Corporate Tax Rate)

Cost of Equity (Re): The cost of equity represents the return required by the company's shareholders or equity investors. It is the cost of raising funds by selling equity (such as common stock). The cost of equity is often estimated using methods like the Capital Asset Pricing Model (CAPM) or the Dividend Discount Model (DDM).

Cost of Debt (Rd): The cost of debt is the interest rate the company pays on its outstanding debt. It is the cost of raising funds through borrowing, such as issuing bonds or taking loans. The cost of debt is typically based on the prevailing interest rates in the market and the company's creditworthiness.

Corporate Tax Rate (Tc): The corporate tax rate is the percentage of a company's profits that is paid in taxes. It is used to calculate the tax shield on interest payments. Interest expenses on debt reduce taxable income, and the tax shield represents the tax savings resulting from these deductions.

Market Value of Equity (E): The market value of equity is the total value of the company's outstanding shares of common stock. It is calculated by multiplying the current stock price by the number of shares outstanding.

Market Value of Debt (D): The market value of debt is the total value of the company's outstanding debt obligations, such as bonds and loans. It represents the current market price of the debt instruments.

Total Market Value of Capital (V): The total market value of capital is the sum of the market value of equity and the market value of debt (V = E + D). It represents the total value of the company's financing, both through equity and debt.

**Also known as:** WACC, blended cost of capital, discount rate.

**Args:**

- <u>show_full_results (bool, optional):</u> Whether to show the full results or just the WACC values.
Defaults to True.
- <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int | None, optional):</u> The trailing period to use for the calculation. Defaults to None.

**Returns:**

pd.DataFrame: DataFrame containing the WACC values.

**Notes:**

- The Cost of Equity is approximated with the Capital Asset Pricing Model (CAPM).
- The Market Value of Debt is approximated as the Total Debt.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.models.get_weighted_average_cost_of_capital().loc["AAPL"]
```

Which returns:

|                                  |        2021 |         2022 |        2023 |        2024 |        2025 |
|:---------------------------------|------------:|-------------:|------------:|------------:|------------:|
| Market Value Equity              | 2.9947e+12  |  2.12121e+12 | 3.04439e+12 | 3.8585e+12  | 4.07918e+12 |
| Market Value Debt                | 1.36522e+11 |  1.3248e+11  | 1.2393e+11  | 1.19059e+11 | 1.12377e+11 |
| Cost of Equity                   | 0.3494      | -0.2646      | 0.2633      | 0.2266      | 0.1938      |
| Cost of Debt                     | 0.0194      |  0.0221      | 0.0317      | 0           | 0           |
| Corporate Tax Rate               | 0.133       |  0.162       | 0.1472      | 0.2409      | 0.1561      |
| Weighted Average Cost of Capital | 0.3349      | -0.248       | 0.2541      | 0.2198      | 0.1886      |


---

## get_economic_value_added
Economic Value Added (EVA) is a measure of a company's financial performance that represents the value created in excess of the required return of the company's capital providers. It captures whether a company is generating returns above its true cost of capital, which distinguishes it from purely accounting-based measures such as Net Income.

The formula is as follows:

- NOPAT = EBIT * (1 - Effective Tax Rate)
- Invested Capital = Total Equity + Total Debt
- EVA = NOPAT - (Weighted Average Cost of Capital * Invested Capital)

**Also known as:** EVA, economic profit.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int | None, optional):</u> The trailing period to use for the calculation. Defaults to None.
- <u>show_columns (list[str] | None, optional):</u> List of columns to show in the results. If None, all
columns will be shown. Defaults to None.

**Returns:**

pd.DataFrame: DataFrame containing the EVA and its components.

**Notes:**

- A positive EVA indicates that the company is generating returns in excess of its cost of
capital, i.e. it is creating value for its capital providers. A negative EVA indicates the
company is destroying value.
- EBIT is approximated as Net Income + Income Tax Expense + Interest Expense, consistent
with the Altman Z-Score calculation elsewhere in this module.
- Invested Capital is approximated as the average of Total Equity and Total Debt, consistent
with the Return on Invested Capital calculation in the Ratios module.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "MSFT"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.models.get_economic_value_added().loc["AAPL"]
```

Which returns:

|                                   |        2021 |          2022 |
|:----------------------------------|-------------:|-------------:|
| Net Operating Profit After Taxes  |  9.69732e+10 |  1.02259e+11 |
| Invested Capital                  |  1.93614e+11 |  1.91382e+11 |
| Weighted Average Cost of Capital  |       0.3598 |      -0.2326 |
| Economic Value Added              |  2.73107e+10 |  1.46775e+11 |


---

## get_intrinsic_valuation
Intrinsic value is a fundamental concept in finance and investing that represents the true worth or value of an asset, security, or investment, independent of its current market price or prevailing market sentiment. It is a concept often associated with the value investing philosophy, made famous by legendary investors like Benjamin Graham and Warren Buffett. Understanding intrinsic value is crucial for investors looking to make informed decisions about where to allocate their capital.

This functionality uses DCF, or Discounted Cash Flow which is a widely used financial valuation method that allows investors and analysts to estimate the intrinsic value of an investment or business based on its expected future cash flows. It is a fundamental tool in finance and investment analysis, providing a systematic way to assess the present value of future cash flows while considering the time value of money.

The formula is as follows:

- Cash Flow Projection_t = Cash Flow_t-1 * (1 + Growth Rate) - Terminal Value = Last Cash Flow Projection * (1 + Perpetual Growth Rate) / (Weighted Average Cost of Capital - Perpetual Growth Rate) - Enterprise Value = Sum of Present Value of Cash Flow Projections + Terminal Value - Equity Value = Enterprise Value - Total Debt + Cash and Cash Equivalents - Intrinsic Value = Equity Value / Total Shares Outstanding

**Also known as:** DCF, discounted cash flow, fair value, intrinsic value.

**Args:**

- <u>growth_rate (float, list or dict):</u> The growth rate to use for the cash flow projections. Can be one number
to use for all tickers, or a list or dict that contains a growth rate for each ticker.
- <u>perpetual_growth_rate (float, list or dict):</u> The perpetual growth rate to use for the terminal value.
Can be one number to use for all tickers, or a list or dict that contains a perpetual growth rate for
each ticker.
- <u>weighted_average_cost_of_capital (float, list or dict):</u> The weighted average cost of capital to use for
the terminal value. Can be one number to use for all tickers, or a list or dict that contains a
weighted average cost of capital for each ticker.
- <u>periods (int, optional):</u> The number of periods to use for the cash flow projections. Defaults to 5.
- <u>cash_flow_type (str, optional):</u> The type of cash flow to use for the cash flow projections.
Defaults to "Free Cash Flow". Other options are "Operating Cash Flow", "Change in Working Capital",
and "Capital Expenditure".
- <u>trailing (int | None, optional):</u> The number of trailing periods to sum for the base cash flow.
When set, uses the sum of the last N periods instead of only the most recent period. Defaults to None.
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.

**Returns:**

pd.DataFrame: DataFrame containing the intrinsic value for each ticker.

**Notes:**

- The results are highly dependent on the input. Therefore, think carefully about each input parameter to
ensure the results are accurate (given your beliefs)

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.models.get_intrinsic_valuation(0.05, 0.025, 0.094).loc["AAPL"]
```

Which returns:

|                      |   Periods = 5 |
|:---------------------|--------------:|
| Terminal Value       |   1.87255e+12 |
| Cash Flow Projection |   1.9986e+12  |
| Enterprise Value     |   1.58232e+12 |
| Equity Value         |   1.50588e+12 |
| Intrinsic Value      | 100.36        |


---

## get_gorden_growth_model
The Gordon Growth Model, also known as the Dividend Discount Model (DDM) with Constant Growth, is a method used to estimate the intrinsic value of a stock based on its expected future dividends. The model assumes that dividends will grow at a constant rate indefinitely.

The formula is as follows:

- Intrinsic Value = (Dividends Per Share * (1 + Growth Rate)) / (Rate of Return - Growth Rate)

The formula essentially discounts the future expected dividends to their present value, taking into account the required rate of return and the growth rate. The numerator represents the expected dividend in the next period. The denominator represents the required rate of return minus the growth rate.

Investors often use the Gordon Growth Model to compare the intrinsic value of a stock with its current market price. If the intrinsic value is higher than the market price, some investors may interpret it as an indication that the stock is undervalued.

It's important to note that the Gordon Growth Model is based on several assumptions, including the assumption of constant growth in dividends. It is most applicable to mature companies with stable and predictable dividend growth. If a company's dividend growth is expected to fluctuate or if it does not pay dividends, alternative valuation models may be more appropriate.

The assumption of constant growth of dividends is often unrealistic. In reality, dividends may fluctuate or even be suspended. Therefore, the Gordon Growth Model should be used with caution and in conjunction with other valuation methods.

**Also known as:** Gordon Growth Model, DDM, dividend discount model, GGM.

**Args:**

- <u>rate_of_return (float):</u> The required rate of return.
- <u>growth_rate (float):</u> The growth rate of the dividends.
- <u>project_periods (int, optional):</u> The number of periods to project the the stock price. Defaults to 5.
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.

**Returns:**

pd.DataFrame: DataFrame containing the intrinsic value for each ticker over time.

**Notes:**

- The results are highly dependent on the input. Therefore, think carefully about each input parameter to
ensure the results are accurate (given your beliefs)

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "MSFT"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.models.get_gorden_growth_model(0.20, 0.05)
```

Which returns:

|      |   AAPL |    MSFT |
|:-----|-------:|--------:|
| 2022 | 0      |  0      |
| 2023 | 0      |  0      |
| 2024 | 0      |  0      |
| 2025 | 5.46   | 12.18   |
| 2026 | 5.733  | 12.789  |
| 2027 | 6.0196 | 13.4284 |
| 2028 | 6.3206 | 14.0999 |
| 2029 | 6.6367 | 14.8049 |
| 2030 | 6.9685 | 15.5451 |
| 2031 | 7.3169 | 16.3224 |


---

## get_altman_z_score
Calculates the Altman Z-Score, a financial metric used to predict the likelihood of a company going bankrupt. The Altman Z-Score is calculated using several financial ratios, including working capital to total assets, retained earnings to total assets, earnings before interest and taxes (EBIT) to total assets, market value of equity to book value of total liabilities, and sales to total assets.

The formula is as follows:

- Working Capital to Total Assets = Working Capital / Total Assets - Retained Earnings to Total Assets = Retained Earnings / Total Assets - EBIT to Total Assets = EBIT / Total Assets - Market Value to Total Liabilities = Market Value of Equity / Total Liabilities - Sales to Total Assets = Sales / Total Assets - Altman Z-Score = 1.2 * Working Capital to Total Assets + 1.4 * Retained Earnings to Total Assets + 3.3 * EBIT to Total Assets + 0.6 * Market Value to Total Liabilities + 1.0 * Sales to Total Assets

The Altman Z-Score can be interpreted as follows:

- A Z-Score of less than 1.81 indicates a high likelihood of bankruptcy.
- A Z-Score between 1.81 and 2.99 indicates a gray area.
- A Z-Score of greater than 2.99 indicates a low likelihood of bankruptcy.

**Also known as:** Altman Z-score, bankruptcy prediction, financial distress score.

**Args:**

- <u>diluted (bool, optional):</u> Whether to use diluted shares outstanding in the calculation. Defaults to True.
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int | None, optional):</u> The trailing period to use for the calculation. Defaults to None.

**Returns:**

pd.DataFrame: DataFrame containing the Altman Z-Score and its components.

**Notes:**

- The Altman Z-Score is a financial metric used to predict the likelihood of a company going bankrupt.
- The Z-Score is calculated using several financial ratios, including working capital to total assets,
retained earnings to total assets, earnings before interest and taxes (EBIT) to total assets, market value
of equity to book value of total liabilities, and sales to total assets.
- A Z-Score of less than 1.81 indicates a high likelihood of bankruptcy, while a Z-Score of greater than 2.99
indicates a low likelihood of bankruptcy.
- The Z-Score is most effective when used to analyze manufacturing companies with assets of
$1 million or more.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

altman_z_score = toolkit.models.get_altman_z_score()

altman_z_score.loc["AAPL"]
```

Which returns:

|                                   |    2021 |    2022 |    2023 |    2024 |    2025 |
|:----------------------------------|--------:|--------:|--------:|--------:|--------:|
| Working Capital to Total Assets   |  0.0267 | -0.0527 | -0.0049 | -0.0641 | -0.0492 |
| Retained Earnings to Total Assets |  0.0158 | -0.0087 | -0.0006 | -0.0525 | -0.0397 |
| EBIT to Total Assets              |  0.3187 |  0.3459 |  0.3337 |  0.3383 |  0.3695 |
| Market Value to Total Liabilities | 10.4015 |  7.022  | 10.4821 | 12.5264 | 14.2874 |
| Sales to Total Assets             |  1.0422 |  1.1179 |  1.0871 |  1.0714 |  1.1584 |
| Altman Z-Score                    |  8.3888 |  6.3973 |  8.4709 |  9.5533 | 10.8355 |


---

## get_piotroski_score
Calculate the Piotroski Score, a comprehensive financial assessment tool that helps investors and analysts evaluate a company's financial health and fundamental strength.

The Piotroski Score was developed by Joseph Piotroski and is based on a set of nine fundamental financial criteria. Each criterion is assigned a score of 0 or 1, and the scores are then summed to calculate the Piotroski Score.

The nine criteria are categorized into three groups:

1. Profitability: - Return on Assets (ROA) Criteria: Measures the profitability of the company. - Operating Cash Flow Criteria: Evaluates the company's ability to generate cash from its operations. - Change in ROA Criteria: Assesses the trend in ROA over time. - Accruals Criteria: Examines the quality of earnings.

2. Leverage, Liquidity, and Operating Efficiency: - Change in Leverage Criteria: Analyzes changes in the company's leverage (debt). - Change in Current Ratio Criteria: Evaluates changes in the current ratio. - Number of Shares Criteria: Assesses the issuance of common shares.

3. Operating Efficiency and Asset Utilization: - Gross Margin Criteria: Examines the company's gross margin, a measure of profitability. - Asset Turnover Ratio Criteria: Evaluates the efficiency of asset utilization and sales generation.

The Piotroski Score is calculated by summing the scores assigned to each of the nine criteria. The maximum possible score is 9, indicating the highest financial strength, while the minimum score is 0, suggesting potential financial weaknesses.

Note that the Piostroski Score has been developed many decades ago and that it is important to always compare the same sectors. E.g. it could be that it is quite normal that a firm issues shares each year which nets a lower score even though it is a normal practice in that sector.

Please see Piotroski, Joseph D. "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers." Journal of Accounting Research, Vol. 38, No. 3, 1999, pp. 1-41.

**Also known as:** Piotroski F-score, financial strength, quality score.

**Args:**

- <u>trailing (int | None, optional):</u> The trailing period to use for the calculation. Defaults to None.
- <u>show_columns (list[str] | None, optional):</u> List of columns to show in the results. If None, all columns
will be shown. Defaults to None.

**Returns:**

pd.DataFrame: DataFrame containing the Piotroski F-Score and its components.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA", "MSFT"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.models.get_piotroski_score().loc["AAPL"]
```

Which returns:

|                                     |   2021 |   2022 |   2023 |   2024 |   2025 |
|:------------------------------------|-------:|-------:|-------:|-------:|-------:|
| Return on Assets Criteria           |      1 |      1 |      1 |      1 |      1 |
| Operating Cashflow Criteria         |      1 |      1 |      1 |      1 |      1 |
| Change in Return on Assets Criteria |      0 |      0 |      0 |      0 |      1 |
| Accruals Criteria                   |      1 |      1 |      1 |      1 |      1 |
| Change in Leverage Criteria         |      0 |      1 |      1 |      1 |      1 |
| Change in Current Ratio Criteria    |      0 |      0 |      1 |      0 |      1 |
| Number of Shares Criteria           |      0 |      1 |      1 |      1 |      1 |
| Gross Margin Criteria               |      1 |      1 |      1 |      1 |      1 |
| Asset Turnover Criteria             |      0 |      1 |      0 |      1 |      1 |
| Piotroski Score                     |      4 |      7 |      7 |      7 |      9 |


---

## get_beneish_m_score
The Beneish M-Score is a probabilistic model, developed by Messod Beneish, that uses eight financial ratios derived from a company's financial statements to identify whether a company has manipulated its earnings. It is a natural companion to the Altman Z-Score and Piotroski F-Score, using the same normalized financial statements as its input.

The formula is as follows:

M-Score = -4.84 + 0.92 * DSRI + 0.528 * GMI + 0.404 * AQI + 0.892 * SGI + 0.115 * DEPI - 0.172 * SGAI + 4.679 * TATA - 0.327 * LVGI

The eight variables are:

- DSRI: Days Sales in Receivables Index
- GMI: Gross Margin Index
- AQI: Asset Quality Index
- SGI: Sales Growth Index
- DEPI: Depreciation Index
- SGAI: Selling, General and Administrative Expenses Index
- TATA: Total Accruals to Total Assets
- LVGI: Leverage Index

**Also known as:** Beneish M-Score, earnings manipulation score.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int | None, optional):</u> The trailing period to use for the calculation. Defaults to None.
- <u>show_columns (list[str] | None, optional):</u> List of columns to show in the results. If None, all
columns will be shown. Defaults to None.

**Returns:**

pd.DataFrame: DataFrame containing the Beneish M-Score and its components.

**Notes:**

- A M-Score greater than -1.78 suggests that the company is likely to be an earnings
manipulator. A M-Score lower than -1.78 suggests the company is unlikely to be a manipulator.
- As with the Altman Z-Score and Piotroski F-Score, this is a probabilistic, not a
definitive, indicator and should be combined with further fundamental analysis.
- Every component compares the current period to the prior period, so the very first
period in the results will always be NaN.

References:
- Beneish, Messod D. "The Detection of Earnings Manipulation." Financial Analysts Journal,
Vol. 55, No. 5, 1999, pp. 24-36.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "MSFT"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.models.get_beneish_m_score().loc["AAPL"]
```

Which returns:

|                                  |    2021 |    2022 |    2023 |
|:---------------------------------|--------:|--------:|--------:|
| Days Sales in Receivables Index  |  1.0322 |  1.0975 |  1.0297 |
| Gross Margin Index               |  0.9151 |  0.9647 |  0.9814 |
| Asset Quality Index              |  1.1404 |  0.9841 |  0.9387 |
| Sales Growth Index               |  1.3326 |  1.0779 |  0.972  |
| Depreciation Index               |  1.0566 |  1.0635 |  0.9982 |
| SGA Expenses Index               |  0.8279 |  1.0595 |  1.0222 |
| Leverage Index                   |  1.0608 |  1.0729 |  0.9516 |
| Total Accruals to Total Assets   | -0.0267 | -0.0634 | -0.0384 |
| Beneish M-Score                  | -2.2503 | -2.6691 | -2.6802 |


---

## get_present_value_of_growth_opportunities
The Present Value of Growth Opportunities (PVGO) is a financial metric that represents the present value of a company's future growth opportunities. It is calculated as the difference between the company's current stock price and the discounted value of its future cash flows.

The formula is as follows:

- PVGO = Stock Price - Earnings Per Share / Weighted Average Cost of Capital

**Also known as:** PVGO, growth value.

**Args:**

- <u>calculate_daily (bool, optional):</u> Whether to calculate the PVGO using daily historical data.
Defaults to False.
- <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
- <u>include_dividends (bool, optional):</u> Whether to include dividends in the calculation.
Defaults to False.
- <u>trailing (int | None, optional):</u> The trailing period to use for the calculation. Defaults to None.
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: DataFrame containing the PVGO values.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.models.get_present_value_of_growth_opportunities()
```

Which returns:

|      |    AAPL |    TSLA |
|:-----|--------:|--------:|
| 2021 | 160.807 | 348.912 |
| 2022 | 154.58  | 133.203 |
| 2023 | 168.39  | 239.608 |
| 2024 | 222.742 | 399.662 |
| 2025 | 232.279 | 446.273 |


---

## get_sustainable_growth_rate
The Sustainable Growth Rate (SGR) is the maximum rate at which a company can grow its revenue, using internally generated funds only, without having to raise additional equity or increase its financial leverage.

The formula is as follows:

- Retention Ratio = 1 - Dividend Payout Ratio
- SGR = Return on Equity * Retention Ratio

**Also known as:** SGR, self-sustainable growth rate.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int | None, optional):</u> The trailing period to use for the calculation. Defaults to None.

**Returns:**

pd.DataFrame: DataFrame containing the Sustainable Growth Rate.

**Notes:**

- Growing faster than the SGR without external financing typically requires either
improving profitability, reducing the dividend payout, or increasing leverage.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "MSFT"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.models.get_sustainable_growth_rate()
```

Which returns:

|      |   2021 |   2022 |   2023 |
|:-----|-------:|-------:|-------:|
| AAPL | 1.2491 | 1.4937 | 1.4531 |
| MSFT | 0.3438 | 0.354  | 0.282  |


---

## get_internal_growth_rate
The Internal Growth Rate (IGR) is the maximum rate at which a company can grow its revenue using only its retained earnings, without raising any external financing (neither debt nor equity).

The formula is as follows:

- Retention Ratio = 1 - Dividend Payout Ratio
- IGR = (Return on Assets * Retention Ratio) / (1 - (Return on Assets * Retention Ratio))

**Also known as:** IGR.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int | None, optional):</u> The trailing period to use for the calculation. Defaults to None.

**Returns:**

pd.DataFrame: DataFrame containing the Internal Growth Rate.

**Notes:**

- The IGR is more conservative than the Sustainable Growth Rate (SGR) since it assumes
no additional debt is raised to fund growth, whereas the SGR assumes the company
maintains its current level of financial leverage.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "MSFT"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.models.get_internal_growth_rate()
```

Which returns:

|      |   2021 |   2022 |   2023 |
|:-----|-------:|-------:|-------:|
| AAPL | 0.3118 | 0.3183 | 0.3028 |
| MSFT | 0.164  | 0.1853 | 0.1565 |


---

## get_graham_number
Calculate the Graham Number, a conservative estimate of a stock's fair value based on its earnings and book value, as devised by Benjamin Graham.

The Graham Number is intended as an upper bound on the price a defensive investor should pay for a stock. It is most meaningful for stable, profitable companies with positive book value - for companies with negative earnings or negative book value the result is not meaningful (the square root of a negative number is undefined and will show up as NaN).

The formula is as follows:

- Graham Number = √(22.5 x Earnings per Share x Book Value per Share)

**Also known as:** Graham fair value.

**Args:**

- <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
- <u>trailing (int | None, optional):</u> The trailing period to use for the calculation. Defaults to None.
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: DataFrame containing the Graham Number values.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.models.get_graham_number()
```

Which returns:

|      |    2021 |    2022 |    2023 |    2024 |    2025 |
|:-----|--------:|--------:|--------:|--------:|--------:|
| AAPL | 21.7378 | 20.662  | 23.2901 | 22.4927 | 28.7292 |
| TSLA | 18.1054 | 32.3757 | 41.7451 | 30.9185 | 23.7345 |


---

