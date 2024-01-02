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

The Models module is meant to execute well-known models such as DUPONT and the Discounted Cash Flow (DCF) model. These models are also directly related to the data retrieved from the Toolkit module.

To install the FinanceToolkit it simply requires the following:

{% include code_header.html %}
{% highlight bash %}
pip install financetoolkit -U
{% endhighlight %}

If you are looking for documentation regarding the toolkit, discovery, ratios, technicals, risk, performance and economics, please have a look below:

<div style="display: flex; justify-content: space-between;" class="show-on-desktop">
    <a href="/projects/financetoolkit/docs" class="btn btn--info" style="flex: 1;margin-right:5px">Toolkit</a>
    <a href="/projects/financetoolkit/docs/discovery" class="btn btn--info" style="flex: 1;margin-right:5px">Discovery</a>
    <a href="/projects/financetoolkit/docs/ratios" class="btn btn--info" style="flex: 1;margin-right:5px">Ratios</a>
    <a href="/projects/financetoolkit/docs/models" class="btn btn--warning" style="flex: 1;margin-right:5px">Models</a>
    <a href="/projects/financetoolkit/docs/technicals" class="btn btn--info" style="flex: 1;margin-right:5px">Technicals</a>
    <a href="/projects/financetoolkit/docs/risk" class="btn btn--info" style="flex: 1;margin-right:5px">Risk</a>
    <a href="/projects/financetoolkit/docs/performance" class="btn btn--info" style="flex: 1;margin-right:5px">Performance</a>
    <a href="/projects/financetoolkit/docs/economics" class="btn btn--info" style="flex: 1; ">Economics</a>
</div>

{% include algolia.html %}

## __init__
Initializes the Models Controller Class.

**Args:**
 - <u>tickers (str | list[str]):</u> The ticker(s) to use for the models.
 - <u>daily_historical (pd.DataFrame):</u> The daily historical data.
 - <u>period_historical (pd.DataFrame):</u> The period historical data.
 - <u>risk_free_rate (pd.DataFrame):</u> The risk free rate data.
 - <u>balance (pd.DataFrame):</u> The balance sheet data.
 - <u>income (pd.DataFrame):</u> The income statement data.
 - <u>cash (pd.DataFrame):</u> The cash flow statement data.
 - <u>quarterly (bool, optional):</u> Whether to use quarterly or yearly data. Defaults to False.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to 4.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["TSLA", "AMZN"], api_key=FMP_KEY, quarterly=True, start_date='2022-12-31')

dupont_analysis = toolkit.models.get_extended_dupont_analysis()

dupont_analysis.loc['AMZN']
{% endhighlight %}


Which returns:

| | 2022Q2 | 2022Q3 | 2022Q4 | 2023Q1 | 2023Q2 |
 |:------------------------|------------:|----------:|------------:|----------:|----------:|
 | Interest Burden Ratio | -1.24465 | 0.858552 | -2.88409 | 1.20243 | 1.01681 |
 | Tax Burden Ratio | -0.611396 | 1.13743 | 0.101571 | 0.640291 | 0.878792 |
 | Operating Profit Margin | -0.0219823 | 0.0231391 | -0.00636042 | 0.0323498 | 0.0562125 |
 | Asset Turnover | nan | 0.299735 | 0.3349 | 0.274759 | 0.285319 |
 | Equity Multiplier | nan | 3.15403 | 3.14263 | 3.08433 | 2.91521 |
 | Return on Equity | nan | 0.0213618 | 0.00196098 | 0.0211066 | 0.0417791 |

## get_dupont_analysis
Perform a Dupont analysis to breakdown the return on equity (ROE) into its components.

The Dupont analysis is a method used to dissect and understand the factors that drive a company's return on equity (ROE). It breaks down the ROE into three key components: Profit Margin, Asset Turnover, and Financial Leverage.

The formula is as follows:


- Profit Margin = Net Income / Revenue 
- Asset Turnover = Revenue / Average Total Assets 
- Financial Leverage = Average Total Assets / Average Total Equity 
- ROE = Profit Margin * Asset Turnover * Financial Leverage

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.

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

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

dupont_analysis = toolkit.models.get_dupont_analysis()
{% endhighlight %}

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

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.

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

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

extended_dupont_analysis = toolkit.models.get_extended_dupont_analysis()
{% endhighlight %}

## get_enterprise_value_breakdown
Calculate the Enterprise Value (EV) breakdown, providing a detailed view of its components.

The Enterprise Value breakdown includes the following components for each quarter or year:


- Share Price: The market price per share of the company's stock. 
- Market Capitalization (Market Cap): The total value of a company's outstanding common and preferred shares. 
- Debt: The sum of long
-term and short
-term debt on the company's balance sheet. 
- Preferred Equity: The value of preferred shares, if applicable. 
- Minority Interest: The equity value of a subsidiary with less than 50% ownership. 
- Cash and Cash Equivalents: The total amount of liquid assets including cash, marketable securities, and short
-term investments.

The Enterprise Value is calculated as the sum of Market Cap, Debt, Preferred Equity, Minority Interest, minus Cash and Cash Equivalents.

This breakdown is displayed in a DataFrame for each company and includes the option to show growth values as well.

**Args:**
 - <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.

 **Returns:**
 pd.DataFrame: DataFrame containing the Enterprise Value breakdown, including the calculated components.

 **Notes:**
 - All the inputs must be in the same currency and unit for accurate calculations.
 - The Enterprise Value is an important metric used for valuation and investment analysis.
 - A positive Enterprise Value indicates that the company is financed primarily by equity and has excess cash.
 - A negative Enterprise Value may indicate financial distress or unusual financial situations.
 - Understanding the Enterprise Value breakdown can provide insights into the sources of a
 company's value and potential risks.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

enterprise_value_breakdown = toolkit.models.get_enterprise_value_breakdown()
{% endhighlight %}

## get_weighted_average_cost_of_capital
The Weighted Average Cost of Capital (WACC) is a financial metric used to estimate the cost of capital for a company. It represents the average rate of return a company must pay to its investors for using their capital. WACC takes into account the cost of both equity and debt, weighted by their respective proportions in the company's capital structure.

The formula is as follows:


- Market Value of Equity = Share Price * Total Shares Outstanding 
- Market Value of Debt = Total Debt 
- Total Market Value = Market Value of Equity + Market Value of Debt 
- Cost of Equity = Risk Free Rate + Beta * (Benchmark Return 
- Risk Free Rate) 
- Cost of Debt = Interest Expense / Total Debt 
- WACC = (Market Value of Equity / Total Market Value) * Cost of Equity + (Market Value of Debt / Total Market Value) * Cost of Debt * (1 
- Corporate Tax Rate)

Cost of Equity (Re): The cost of equity represents the return required by the company's shareholders or equity investors. It is the cost of raising funds by selling equity (such as common stock). The cost of equity is often estimated using methods like the Capital Asset Pricing Model (CAPM) or the Dividend Discount Model (DDM).

Cost of Debt (Rd): The cost of debt is the interest rate the company pays on its outstanding debt. It is the cost of raising funds through borrowing, such as issuing bonds or taking loans. The cost of debt is typically based on the prevailing interest rates in the market and the company's creditworthiness.

Corporate Tax Rate (Tc): The corporate tax rate is the percentage of a company's profits that is paid in taxes. It is used to calculate the tax shield on interest payments. Interest expenses on debt reduce taxable income, and the tax shield represents the tax savings resulting from these deductions.

Market Value of Equity (E): The market value of equity is the total value of the company's outstanding shares of common stock. It is calculated by multiplying the current stock price by the number of shares outstanding.

Market Value of Debt (D): The market value of debt is the total value of the company's outstanding debt obligations, such as bonds and loans. It represents the current market price of the debt instruments.

Total Market Value of Capital (V): The total market value of capital is the sum of the market value of equity and the market value of debt (V = E + D). It represents the total value of the company's financing, both through equity and debt.

**Args:**
 - <u>show_full_results (bool, optional):</u> Whether to show the full results or just the WACC values.
 Defaults to True.
 - <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.

 **Returns:**
 pd.DataFrame: DataFrame containing Dupont analysis results, including Profit Margin, Asset
 Turnover, Financial Leverage, and the calculated ROE values.

 **Notes:**
 - The Cost of Equity is approximated with the Capital Asset Pricing Model (CAPM).
 - The Market Value of Debt is approximated as the Total Debt.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.models.get_weighted_average_cost_of_capital()
{% endhighlight %}

## get_intrinsic_valuation
Intrinsic value is a fundamental concept in finance and investing that represents the true worth or value of an asset, security, or investment, independent of its current market price or prevailing market sentiment. It is a concept often associated with the value investing philosophy, made famous by legendary investors like Benjamin Graham and Warren Buffett. Understanding intrinsic value is crucial for investors looking to make informed decisions about where to allocate their capital.

This functionality uses DCF, or Discounted Cash Flow which is a widely used financial valuation method that allows investors and analysts to estimate the intrinsic value of an investment or business based on its expected future cash flows. It is a fundamental tool in finance and investment analysis, providing a systematic way to assess the present value of future cash flows while considering the time value of money.

The formula is as follows:


- Cash Flow Projection_t = Cash Flow_t
-1 * (1 + Growth Rate) 
- Terminal Value = Last Cash Flow Projection * (1 + Perpetual Growth Rate) / (Weighted Average Cost of Capital 
- Perpetual Growth Rate) 
- Enterprise Value = Sum of Present Value of Cash Flow Projections + Terminal Value 
- Equity Value = Enterprise Value 
- Total Debt + Cash and Cash Equivalents 
- Intrinsic Value = Equity Value / Total Shares Outstanding

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
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.

 **Returns:**
 pd.DataFrame: DataFrame containing the intrinsic value for each ticker.

 **Notes:**
 - The results are highly dependent on the input. Therefore, think carefully about each input parameter to
 ensure the results are accurate (given your beliefs)

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.models.get_intrinsic_valuation(0.05, 0.025, 0.094)
{% endhighlight %}

## get_altman_z_score
Calculates the Altman Z
-Score, a financial metric used to predict the likelihood of a company going bankrupt. The Altman Z
-Score is calculated using several financial ratios, including working capital to total assets, retained earnings to total assets, earnings before interest and taxes (EBIT) to total assets, market value of equity to book value of total liabilities, and sales to total assets.

The formula is as follows:


- Working Capital to Total Assets = Working Capital / Total Assets 
- Retained Earnings to Total Assets = Retained Earnings / Total Assets 
- EBIT to Total Assets = EBIT / Total Assets 
- Market Value to Total Liabilities = Market Value of Equity / Total Liabilities 
- Sales to Total Assets = Sales / Total Assets 
- Altman Z
-Score = 1.2 * Working Capital to Total Assets + 1.4 * Retained Earnings to Total Assets + 3.3 * EBIT to Total Assets + 0.6 * Market Value to Total Liabilities + 1.0 * Sales to Total Assets

The Altman Z
-Score can be interpreted as follows:


- A Z
-Score of less than 1.81 indicates a high likelihood of bankruptcy. 
- A Z
-Score between 1.81 and 2.99 indicates a gray area. 
- A Z
-Score of greater than 2.99 indicates a low likelihood of bankruptcy.

**Args:**
 - <u>diluted (bool, optional):</u> Whether to use diluted shares outstanding in the calculation. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.

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

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

altman_z_score = toolkit.models.get_altman_z_score()
{% endhighlight %}

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

Please see Piotroski, Joseph D. "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers." Journal of Accounting Research, Vol. 38, No. 3, 1999, pp. 1
-41.

**Args:**
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.

 **Returns:**
 pd.DataFrame: DataFrame containing the Piotroski F-Score and its components.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA", "MSFT"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.models.get_piotroski_score()
{% endhighlight %}

