---
title: Ratios
excerpt: The Ratios Module contains over 50+ ratios that can be used to analyse companies. These ratios are divided into 5 categories which are efficiency, liquidity, profitability, solvency and valuation. Each ratio is calculated using the data from the Toolkit module.
description: The Ratios Module contains over 50+ ratios that can be used to analyse companies. These ratios are divided into 5 categories which are efficiency, liquidity, profitability, solvency and valuation. Each ratio is calculated using the data from the Toolkit module.
author_profile: false
permalink: /projects/financetoolkit/docs/ratios
classes: wide-sidebar
layout: single
redirect_from:
    - /ratios
sidebar:
    nav: "financetoolkit-docs-ratios"
---

The Ratios Module contains over 50+ ratios that can be used to analyse companies. These ratios are divided into 5 categories which are efficiency, liquidity, profitability, solvency and valuation. Each ratio is calculated using the data from the Toolkit module.

To install the FinanceToolkit it simply requires the following:

{% include code_header.html %}
{% highlight bash %}
pip install financetoolkit -U
{% endhighlight %}

If you are looking for documentation regarding the toolkit, discovery, models, technicals, fixed income, risk, performance and economics, please have a look below:

<div style="display: flex; justify-content: space-between;" class="show-on-desktop">
    <a href="/projects/financetoolkit/docs" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Toolkit</a>
    <a href="/projects/financetoolkit/docs/discovery" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Discovery</a>
    <a href="/projects/financetoolkit/docs/ratios" class="btn btn--warning" style="flex: 1;font-size:10px;margin-right:5px">Ratios</a>
    <a href="/projects/financetoolkit/docs/models" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Models</a>
    <a href="/projects/financetoolkit/docs/options" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Options</a>
    <a href="/projects/financetoolkit/docs/technicals" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Technicals</a>
    <a href="/projects/financetoolkit/docs/fixedincome" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Fixed Income</a>
    <a href="/projects/financetoolkit/docs/risk" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Risk</a>
    <a href="/projects/financetoolkit/docs/performance" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Performance</a>
    <a href="/projects/financetoolkit/docs/economics" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Economics</a>
    <a href="/projects/financetoolkit/docs/portfolio" class="btn btn--info" style="flex: 1;font-size:10px;">Portfolio</a>
</div>

{% include algolia.html %}

## __init__
Initializes the Ratios Controller Class.

**Args:**
 - <u>tickers (str | list[str]):</u> The tickers to use for the calculations.
 - <u>historical (pd.DataFrame):</u> The historical data to use for the calculations.
 - <u>balance (pd.DataFrame):</u> The balance sheet data to use for the calculations.
 - <u>income (pd.DataFrame):</u> The income statement data to use for the calculations.
 - <u>cash (pd.DataFrame):</u> The cash flow statement data to use for the calculations.
 an optional parameter given that you can also define the custom ratios through the Toolkit initialization.
 - <u>quarterly (bool, optional):</u> Whether to use quarterly data. Defaults to False.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

profitability_ratios = toolkit.ratios.collect_profitability_ratios()

profitability_ratios.loc['AAPL']
{% endhighlight %}


Which returns:

| | 2018 | 2019 | 2020 | 2021 | 2022 |
 |:--------------------------------------------|---------:|---------:|---------:|---------:|---------:|
 | Gross Margin | 0.383437 | 0.378178 | 0.382332 | 0.417794 | 0.433096 |
 | Operating Margin | 0.26694 | 0.24572 | 0.241473 | 0.297824 | 0.302887 |
 | Net Profit Margin | 0.224142 | 0.212381 | 0.209136 | 0.258818 | 0.253096 |
 | Interest Burden Ratio | 1.02828 | 1.02827 | 1.01211 | 1.00237 | 0.997204 |
 | Income Before Tax Profit Margin | 0.274489 | 0.252666 | 0.244398 | 0.298529 | 0.30204 |
 | Effective Tax Rate | 0.183422 | 0.159438 | 0.144282 | 0.133023 | 0.162045 |
 | Return on Assets (ROA) | 0.162775 | 0.16323 | 0.177256 | 0.269742 | 0.282924 |
 | Return on Equity (ROE) | 0.555601 | 0.610645 | 0.878664 | 1.50071 | 1.96959 |
 | Return on Invested Capital (ROIC) | 0.269858 | 0.293721 | 0.344126 | 0.503852 | 0.562645 |
 | Return on Capital Employed (ROCE) | 0.305968 | 0.297739 | 0.320207 | 0.495972 | 0.613937 |
 | Return on Tangible Assets | 0.555601 | 0.610645 | 0.878664 | 1.50071 | 1.96959 |
 | Income Quality Ratio | 1.30073 | 1.25581 | 1.4052 | 1.09884 | 1.22392 |
 | Net Income per EBT | 0.816578 | 0.840562 | 0.855718 | 0.866977 | 0.837955 |
 | Free Cash Flow to Operating Cash Flow Ratio | 0.828073 | 0.848756 | 0.909401 | 0.893452 | 0.912338 |
 | EBT to EBIT Ratio | 0.957448 | 0.948408 | 0.958936 | 0.976353 | 0.975982 |
 | EBIT to Revenue | 0.286688 | 0.26641 | 0.254864 | 0.305759 | 0.309473 |

## collect_all_ratios
Calculates and collects all ratios based on the provided data.

**Args:**
 - <u>include_dividends (bool, optional):</u> Whether to include dividends in the calculations.
 Defaults to False.
 - <u>diluted (bool, optional):</u> Whether to use diluted shares for the calculation.
 Defaults to True.
 - <u>days (int, optional):</u> The number of days to use for the calculation. Defaults to 365.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.Series or pd.DataFrame: Ratios calculated based on the specified parameters.

 **Notes:**
 - The method calculates various ratios for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.ratios.collect_all_ratios()
{% endhighlight %}

## collect_custom_ratios
Calculates all Custom Ratios based on the data provided.

Note that any of the following characters are considered as operators: +, 
-, *, /, **, %, //, <, >, ==, !=, >=, <=, (, ) using any of the above characters as part of the column naming will result into an error.

**Args:**
 - <u>custom_ratios (dict):</u> A dictionary containing the custom ratios to calculate.
 - <u>options (bool):</u> Whether to return the available names to use in the custom ratios.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Custom ratios calculated based on the specified parameters.

 **Notes:**
 - The method calculates various custom ratios for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

custom_ratios = {
'WC / Net Income as %': '(Working Capital / Net Income) * 100',
'Large Revenues': 'Revenue > 1000000000',
'Quick Assets': 'Cash and Short Term Investments + Accounts Receivable',
'Cash Op Expenses':'Cost of Goods Sold + Selling, General and Administrative Expenses '
'- Depreciation and Amortization',
'Daily Cash Op Expenses': 'Cash Op Expenses / 365',
'Defensive Interval':'Quick Assets / Daily Cash Op Expenses'
}

companies = Toolkit(
tickers=["AAPL", "MSFT", "GOOGL", "AMZN"],
api_key="FINANCIAL_MODELING_PREP_KEY",
start_date="2022-10-01",
quarterly=True
)

custom_ratios = companies.ratios.collect_custom_ratios(
custom_ratios_dict=custom_ratios
)

custom_ratios.loc['AMZN']
{% endhighlight %}


Which returns:

| | 2022Q4 | 2023Q1 | 2023Q2 | 2023Q3 |
 |:-----------------------|---------------:|---------------:|---------------:|---------------:|
 | WC / Net Income as % | 463.349 | 427.335 | 398.924 | 371.423 |
 | Large Revenues | 1 | 1 | 1 | 1 |
 | Quick Assets | 1.35341e+11 | 1.41847e+11 | 1.5995e+11 | 1.80898e+11 |
 | Cash Op Expenses | 2.1056e+10 | 1.9972e+10 | 2.2854e+10 | 1.9042e+10 |
 | Daily Cash Op Expenses | 5.76877e+07 | 5.47178e+07 | 6.26137e+07 | 5.21699e+07 |
 | Defensive Interval | 2346.1 | 2592.34 | 2554.55 | 3467.48 |

## collect_efficiency_ratios
Calculates and collects all Efficiency Ratios based on the provided data.

**Args:**
 - <u>days (int, optional):</u> The number of days to use for the calculation. Defaults to 365.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.Series or pd.DataFrame: Efficiency ratios calculated based on the specified parameters.

 **Notes:**
 - The method calculates various efficiency ratios for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.ratios.collect_efficiency_ratios()
{% endhighlight %}

## get_asset_turnover_ratio
Calculate the asset turnover ratio, an efficiency ratio that measures how efficiently a company uses its assets to generate sales.

The asset turnover ratio is calculated by dividing the company's net sales (revenue) by its average total assets. It measures how well a company utilizes its assets to generate revenue. A higher asset turnover ratio indicates that the company is generating more revenue per unit of assets, which is generally seen as a positive sign of operational efficiency.

The formula is as follows:


- Asset Turnover Ratio = Net Sales / Average Total Assets

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.Series: Asset turnover ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the asset turnover ratio
 for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

asset_turnover_ratios = toolkit.ratios.get_asset_turnover_ratio()
{% endhighlight %}

## get_inventory_turnover_ratio
Calculate the inventory turnover ratio, an efficiency ratio that measures how quickly a company sells its inventory.

The inventory turnover ratio is calculated by dividing the cost of goods sold (COGS) by the average inventory value. It indicates how many times a company's inventory is sold and replaced over a period. A higher inventory turnover ratio suggests that a company is effectively managing its inventory by quickly converting it into sales.

The formula is as follows:


- Inventory Turnover Ratio = Cost of Goods Sold / Average Inventory

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.Series: Inventory turnover ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the inventory turnover ratio
 for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

inventory_turnover_ratios = toolkit.ratios.get_inventory_turnover_ratio()
{% endhighlight %}

## get_days_of_inventory_outstanding
Calculate the days sales in inventory ratio, an efficiency ratio that measures how long it takes a company to sell its inventory.

The days sales in inventory ratio (DSI) is calculated by dividing the average inventory by the cost of goods sold (COGS) and then multiplying by the number of days in the period. It represents the average number of days it takes for a company to sell its inventory. A lower DSI indicates that the company is selling its inventory more quickly.

The formula is as follows:


- Days Sales in Inventory Ratio = (Average Inventory / Cost of Goods Sold) * Days

**Args:**
 - <u>days (int, optional):</u> The number of days to use for the calculation. Defaults to 365.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Days sales in inventory ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the DSI ratio for each
 asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.ratios.get_days_of_inventory_outstanding()
{% endhighlight %}

## get_days_of_sales_outstanding
Calculate the days of sales outstanding ratio, an efficiency ratio that measures the average number of days it takes a company to collect payment on its credit sales.

The days of sales outstanding (DSO) ratio is calculated by dividing the accounts receivable by the total credit sales and then multiplying by the number of days in the period. It represents the average number of days it takes for a company to collect payment on its credit sales. A lower DSO indicates that the company is collecting payments more quickly.

The formula is as follows:


- Days of Sales Outstanding Ratio = (Accounts Receivable / Total Credit Sales) * Days

**Args:**
 - <u>days (int, optional):</u> The number of days to use for the calculation. Defaults to 365.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Days of sales outstanding ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the DSO ratio for each
 asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

dso_ratios = toolkit.ratios.get_days_of_sales_outstanding()
{% endhighlight %}

## get_operating_cycle
Calculate the operating cycle ratio, an efficiency ratio that measures the average number of days it takes a company to turn its inventory into cash.

The operating cycle represents the total time required to purchase inventory, convert it into finished goods, sell the goods to customers, and collect the accounts receivable. It is calculated by adding the days sales in inventory (DSI) and the days of sales outstanding (DSO).

The formula is as follows:


- Operating Cycle Ratio = Days of Sales in Inventory + Days of Sales Outstanding

**Args:**
 - <u>days (int, optional):</u> The number of days to use for the calculation. Defaults to 365.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Operating cycle ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the operating cycle ratio for each
 asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

operating_cycle_ratios = toolkit.ratios.get_operating_cycle()
{% endhighlight %}

## get_accounts_payables_turnover_ratio
Calculate the accounts payable turnover ratio, an efficiency ratio that measures how quickly a company pays its suppliers.

The accounts payable turnover ratio indicates how many times, on average, a company pays off its accounts payable during a specific period. A higher turnover ratio is generally favorable, as it suggests that the company is efficiently managing its payments to suppliers.

The formula is as follows:


- Accounts Payable Turnover Ratio = Cost of Goods Sold / Average Accounts Payable

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Accounts payable turnover ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the accounts payable turnover ratio for each
 asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

ap_turnover_ratios = toolkit.ratios.get_accounts_payables_turnover_ratio()
{% endhighlight %}

## get_days_of_accounts_payable_outstanding
Calculate the days payables outstanding, an efficiency ratio that measures the number of days it takes a company to pay its suppliers.

The days payables outstanding (DPO) ratio is used to assess how efficiently a company manages its accounts payable. It calculates the average number of days it takes for a company to pay its suppliers after receiving an invoice. A higher DPO ratio indicates that the company is taking longer to pay its suppliers, which may have implications for its relationships with suppliers.

The formula is as follows:


- Days Payables Outstanding = (Average Accounts Payable / Cost of Goods Sold) * Days

**Args:**
 - <u>days (int, optional):</u> The number of days to use for the calculation. Defaults to 365.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Days payables outstanding (DPO) ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the DPO ratio for each
 asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

dpo_ratios = toolkit.ratios.get_days_of_accounts_payable_outstanding()
{% endhighlight %}

## get_cash_conversion_cycle
Calculate the Cash Conversion Cycle, which measures the amount of time it takes for a company to convert its investments in inventory and accounts receivable into cash, while considering the time it takes to pay its accounts payable. This ratio is also known as Cash
-to
-Cash Cycle (C2C) or Net Operating Cycle.

The Cash Conversion Cycle (CCC) is an important measure of a company's liquidity management and efficiency in managing its working capital. It takes into account the time it takes to sell inventory, collect payments from customers, and pay suppliers. A shorter CCC indicates that a company is able to quickly convert its investments into cash, which can be a positive sign of efficient operations.

The formula is as follows:


- Cash Conversion Cycle = Days of Sales in Inventory + Days of Sales Outstanding 
- Days of Accounts Payable Outstanding

**Args:**
 - <u>days (int, optional):</u> The number of days to use for the calculation. Defaults to 365.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Cash Conversion Cycle (CCC) values.

 **Notes:**
 - The method retrieves historical data and calculates the CCC for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the CCC values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

ccc_values = toolkit.ratios.get_cash_conversion_cycle()
{% endhighlight %}

## get_cash_conversion_efficiency
Calculate the cash conversion efficiency, an efficiency ratio that measures how efficiently a company converts its sales into cash. It is also known as the cash conversion ratio.

The cash conversion efficiency ratio is calculated by dividing the operating cash flow by the revenue. It indicates how much of a company's sales are converted into cash. A higher cash conversion efficiency ratio is generally favorable, as it suggests that the company is able to convert its sales into cash more efficiently.

The formula is as follows:


- Cash Conversion Efficiency Ratio = Operating Cash Flow / Revenue

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Cash conversion efficiency ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the operating ratio for each
 asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.ratios.get_cash_conversion_efficiency()
{% endhighlight %}

## get_receivables_turnover
Calculate the receivables turnover, a ratio that measures how efficiently a company uses its assets by comparing the amount of credit extended to customers to the amount of sales generated.

The receivables turnover ratio is an important measure of how well a company manages its accounts receivable. It indicates how quickly a company collects payments from its customers. A higher turnover ratio is generally favorable as it suggests that the company is collecting payments more quickly, which improves its cash flow and working capital management.

The formula is as follows:


- Receivables Turnover Ratio = Net Credit Sales / Average Accounts Receivable

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.
 **Returns:**
 pd.DataFrame: Receivables turnover ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the receivables turnover ratio for each
 asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

receivables_turnover = toolkit.ratios.get_receivables_turnover()
{% endhighlight %}

## get_sga_to_revenue_ratio
Calculate the sales, general, and administrative (SG&A) expenses to revenue ratio, which measures the SG&A expenses relative to the revenue of the company.

The SG&A to revenue ratio is calculated by dividing the total SG&A expenses by the company's revenue and then multiplying by 100 to express it as a percentage. It provides insight into the efficiency of a company's cost management and its ability to control its overhead costs.

The formula is as follows:


- SG&A to Revenue Ratio = SG&A Expenses / Revenue

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: SG&A to revenue ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the SG&A to revenue ratio for
 each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

sga_to_revenue_ratios = toolkit.ratios.get_sga_to_revenue_ratio()
{% endhighlight %}

## get_fixed_asset_turnover
Calculate the Fixed Asset Turnover ratio, an efficiency ratio that measures how efficiently a company uses its fixed assets to generate sales.

The Fixed Asset Turnover ratio is calculated by dividing the company's net sales by the average fixed assets. It indicates how well a company is utilizing its fixed assets to generate revenue. A higher ratio suggests more efficient utilization of fixed assets.

The formula is as follows:


- Fixed Asset Turnover Ratio = Net Sales / Average Fixed Assets

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Fixed Asset Turnover ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the Fixed Asset Turnover ratio
 for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

fixed_asset_turnover_ratios = toolkit.ratios.get_fixed_asset_turnover()
{% endhighlight %}

## get_operating_ratio
Calculate the operating ratio, a financial metric that measures the efficiency of a company's operations by comparing its operating expenses to its revenue.

The operating ratio is calculated by dividing the company's operating expenses by its net sales and multiplying by 100 to express it as a percentage. It provides insight into how efficiently a company is managing its operations.

The formula is as follows:


- Operating Ratio = (Operating Expenses + Cost of Goods Sold) / Revenue

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Operating ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the operating ratio for each
 asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

operating_ratios = toolkit.ratios.get_operating_ratio()
{% endhighlight %}

## collect_liquidity_ratios
Calculates and collects all Liquidity Ratios based on the provided data.

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Liquidity ratios calculated based on the specified parameters.

 **Notes:**
 - The method calculates various liquidity ratios for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

liquidity_ratios = toolkit.ratios.collect_liquidity_ratios()
{% endhighlight %}

## get_current_ratio
Calculate the current ratio, a liquidity ratio that measures a company's ability to pay off its short
-term liabilities with its current assets.

The current ratio is calculated by dividing a company's current assets by its current liabilities. It indicates whether a company can meet its short
-term obligations using its short
-term assets.

The formula is as follows:


- Current Ratio = Current Assets / Current Liabilities

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Current ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the current ratio for each
 asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

current_ratios = toolkit.ratios.get_current_ratio()
{% endhighlight %}

## get_quick_ratio
Calculate the quick ratio (also known as the acid
-test ratio), a more stringent measure of liquidity that excludes inventory from current assets.

This ratio is also referred to as the Acid Test Ratio.

The quick ratio is calculated by subtracting inventory from current assets and then dividing the result by current liabilities. It provides insight into a company's ability to cover its short
-term liabilities using its most liquid assets without relying on inventory.

The formula is as follows:


- Quick Ratio = (Cash and Cash Equivalents + Short Term Investments + Accounts Receivable) / Current Liabilities

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Quick ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the quick ratio for each
 asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit
toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

quick_ratios = toolkit.ratios.get_quick_ratio()
{% endhighlight %}

## get_cash_ratio
Calculate the cash ratio, a liquidity ratio that measures a company's ability to pay off its short
-term liabilities with its cash and cash equivalents.

The cash ratio is calculated by dividing the sum of cash and cash equivalents by current liabilities. It provides insight into a company's immediate ability to cover its short
-term obligations using its most liquid assets.

The formula is as follows:


- Cash Ratio = (Cash and Cash Equivalents + Short Term Investments) / Current Liabilities

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Cash ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the cash ratio for each
 asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

cash_ratios = toolkit.ratios.get_cash_ratio()
{% endhighlight %}

## get_working_capital
Calculate the working capital, which is the difference between a company's current assets and current liabilities.

The working capital is calculated by subtracting total current liabilities from total current assets. It represents the company's short
-term financial health and its ability to cover its current obligations using its liquid assets.

The formula is as follows:


- Working Capital = Current Assets - Current Liabilities

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Working capital values.

 **Notes:**
 - The method retrieves historical data and calculates the working capital for each
 asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the working capital
 values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

working_capitals = toolkit.ratios.get_working_capital()
{% endhighlight %}

## get_operating_cash_flow_ratio
Calculate the operating cash flow ratio, a liquidity ratio that measures a company's ability to pay off its current liabilities with its operating cash flow.

The operating cash flow ratio is calculated by dividing operating cash flow by current liabilities. It indicates whether a company's operating cash flow is sufficient to cover its short
-term obligations.

The formula is as follows:


- Operating Cash Flow Ratio = Cash Flow from Operations / Current Liabilities

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Operating cash flow ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the operating cash flow ratio for each
 asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

operating_cash_flow_ratios = toolkit.ratios.get_operating_cash_flow_ratio()
{% endhighlight %}

## get_operating_cash_flow_sales_ratio
Calculate the operating cash flow to sales ratio, a liquidity ratio that measures the ability of a company to generate cash from its sales.

The operating cash flow to sales ratio is calculated by dividing operating cash flow by sales revenue. It indicates the proportion of sales revenue that is converted into cash from operating activities.

The formula is as follows:


- Operating Cash Flow to Sales Ratio = Cash Flow from Operations / Revenue

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Operating cash flow to sales ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the operating cash flow to sales ratio for each
 asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

operating_cash_flow_sales_ratios = toolkit.ratios.get_operating_cash_flow_sales_ratio()
{% endhighlight %}

## get_short_term_coverage_ratio
Calculate the short
-term coverage ratio, a liquidity ratio that measures a company's ability to pay off its short
-term obligations with its operating cash flow.

The short
-term coverage ratio is calculated by dividing operating cash flow by short
-term debt. It assesses the company's ability to meet its short
-term obligations using its operating cash flow.

The formula is as follows:


- Short Term Coverage Ratio = Cash Flow from Operations / (Accounts Receivable + Inventory - Accounts Payable)

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.ratios.get_short_term_coverage_ratio()
{% endhighlight %}

## collect_profitability_ratios
Calculates and collects all Profitability Ratios based on the provided data.

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Profitability ratios calculated based on the specified parameters.

 **Notes:**
 - The method calculates various profitability ratios for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

profitability_ratios = toolkit.ratios.collect_profitability_ratios()
{% endhighlight %}

## get_gross_margin
Calculate the gross margin, a profitability ratio that measures the percentage of revenue that exceeds the cost of goods sold.

The gross margin ratio is calculated by subtracting the cost of goods sold (COGS) from the total revenue and then dividing the result by the total revenue. It represents the portion of revenue that contributes to covering other expenses and generating profit.

The formula is as follows:


- Gross Margin Ratio = (Revenue - Cost of Goods Sold) / Revenue

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Gross margin ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the gross margin ratio for each
 asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

gross_margin_ratios = toolkit.ratios.get_gross_margin()
{% endhighlight %}

## get_operating_margin
Calculate the operating margin, a profitability ratio that measures the percentage of revenue that remains after deducting operating expenses.

The operating margin ratio is calculated by subtracting the operating expenses from the total revenue and then dividing the result by the total revenue. It indicates how efficiently a company is managing its operating expenses in relation to its revenue.

The formula is as follows:


- Operating Margin Ratio = Operating Income / Revenue

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Operating margin ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the operating margin ratio for each
 asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

operating_margin_ratios = toolkit.ratios.get_operating_margin()
{% endhighlight %}

## get_net_profit_margin
Calculate the net profit margin, a profitability ratio that measures the percentage of profit a company earns per dollar of revenue.

The net profit margin ratio is calculated by dividing the net income by the total revenue. It indicates the portion of each dollar of revenue that represents profit after all expenses have been deducted. A higher net profit margin is generally considered favorable.

The formula is as follows:


- Net Profit Margin Ratio = Net Income / Revenue

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Net profit margin ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the net profit margin ratio for each
 asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

net_profit_margin_ratios = toolkit.ratios.get_net_profit_margin()
{% endhighlight %}

## get_interest_burden_ratio
Compute the Interest Coverage Ratio, a metric that reveals a company's ability to cover its interest expenses with its pre
-tax profits. This ratio measures the proportion of pre
-tax profits required to pay for interest payments and is crucial in determining a company's financial health.

The Interest Coverage Ratio is calculated by dividing the earnings before interest and taxes (EBIT) by the interest expenses. A higher ratio indicates that the company has more earnings to cover its interest expenses, which is generally considered favorable.

The formula is as follows:


- Interest Coverage Ratio = EBIT (or Operating Income) / Interest Expenses

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Interest Coverage Ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the Interest Coverage Ratio for each
 asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

interest_coverage_ratios = toolkit.ratios.get_interest_burden_ratio()
{% endhighlight %}

## get_income_before_tax_profit_margin
Calculate the Pretax Profit Margin, which is the ratio of a company's pre
-tax profit to its revenue, indicating how much profit a company makes before paying taxes on its earnings.

The Pretax Profit Margin is calculated by dividing the pre
-tax profit by the revenue. It provides insight into how efficiently a company is able to generate profits from its revenue.

The formula is as follows:


- Pretax Profit Margin = Income Before Tax / Revenue

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Pretax Profit Margin values.

 **Notes:**
 - The method retrieves historical data and calculates the Pretax Profit Margin for each
 asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

pretax_profit_margin = toolkit.ratios.get_income_before_tax_profit_margin()
{% endhighlight %}

## get_effective_tax_rate
Calculate the effective tax rate, a financial ratio that measures the percentage of pretax income that is paid as taxes.

The effective tax rate is calculated by dividing the income tax expense by the pre
-tax income.

The formula is as follows:


- Effective Tax Rate = Income Tax Expense / Income Before Tax

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Effective tax rate values.

 **Notes:**
 - The method retrieves historical data and calculates the effective tax rate for each
 asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

effective_tax_rate = toolkit.ratios.get_effective_tax_rate()
{% endhighlight %}

## get_return_on_assets
Calculate the return on assets (ROA), a profitability ratio that measures how efficiently a company uses its assets to generate profits.

The return on assets is calculated by dividing the net income by the average total assets. Note that it is false to take the total assets at the end of the period given that income statements report over the period whereas a balance sheet reports on the period.

The formula is as follows:


- Return on Assets = Net Income / Average Total Assets

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Return on assets (ROA) values.

 **Notes:**
 - The method retrieves historical data and calculates the ROA for each asset in the
 Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

roa_ratios = toolkit.ratios.get_return_on_assets()
{% endhighlight %}

## get_return_on_equity
Calculate the return on equity (ROE), a profitability ratio that measures how efficiently a company generates profits using its shareholders' equity.

The return on equity is calculated by dividing the net income by the average shareholders' equity. Shareholders' equity represents the residual interest in the assets of a company after deducting liabilities. Note that it is false to take the total assets at the end of the period given that income statements report over the period whereas a balance sheet reports on the period.

ROE provides insight into the company's ability to generate profits from the investments made by its shareholders. A higher ROE indicates that the company is using its equity effectively to generate higher returns for its shareholders.

The formula is as follows:


- Return on Equity = Net Income / Average Shareholders' Equity (or Total Equity)

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Return on equity (ROE) values.

 **Notes:**
 - The method retrieves historical data and calculates the ROE for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

roe_ratios = toolkit.ratios.get_return_on_equity()
{% endhighlight %}

## get_return_on_invested_capital
Calculate the return on invested capital (ROIC), a financial ratio that measures the company's return on the capital invested in it, including both equity and debt.

The return on invested capital is calculated by dividing the net operating profit after taxes (NOPAT) by the average invested capital. Invested capital includes both equity and debt, making this ratio a valuable measure of how efficiently a company generates returns for all of its investors.

The formula is as follows:


- Return on Invested Capital = (Net Income - Paid Dividends) / Average Invested Capital

**Args:**
 - <u>dividend_adjusted (bool, optional):</u> Whether to adjust the net operating profit after taxes
 with the dividends paid. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Return on invested capital (ROIC) values.

 **Notes:**
 - The method retrieves historical data and calculates the ROIC for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

roic_ratios = toolkit.ratios.get_return_on_invested_capital()
{% endhighlight %}

## get_income_quality_ratio
Calculate the income quality ratio, a financial metric that measures the cash flow from operating activities relative to the net income of the company.

The income quality ratio provides insights into the quality of a company's reported earnings. By comparing the cash flow from operating activities to the net income, this ratio helps assess whether a company's reported profits are backed by actual cash flow. A higher income quality ratio suggests higher earnings quality and a better ability to convert profits into cash flow.

The formula is as follows:


- Income Quality Ratio = Cash Flow from Operations / Net Income

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Income quality ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the income quality ratio for each asset
 in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

income_quality_ratios = toolkit.ratios.get_income_quality_ratio()
{% endhighlight %}

## get_return_on_tangible_assets
Calculate the return on tangible assets, a financial ratio that measures the amount of profit generated by a company's tangible assets.

The return on tangible assets (ROTA) provides insights into the efficiency with which a company utilizes its tangible assets to generate profits. Tangible assets include physical assets such as buildings, machinery, and equipment. ROTA indicates how well a company can generate profits from its core operational assets.

The formula is as follows:


- Return on Tangible Assets = Net Income / Average Tangible Assets

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Return on tangible assets (ROTA) values.

 **Notes:**
 - The method retrieves historical data and calculates the ROTA for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

rota_ratios = toolkit.ratios.get_return_on_tangible_assets()
{% endhighlight %}

## get_return_on_capital_employed
Calculate the return on capital employed (ROCE), a profitability ratio that measures the amount of return a company generates from the capital it has invested in the business.

Return on capital employed (ROCE) is a crucial financial metric that evaluates the efficiency and profitability of a company's utilization of both equity and debt capital to generate profits. It assesses how well the company generates earnings relative to the total capital invested in the business.

The formula is as follows:


- Return on Capital Employed = EBIT / (Total Assets - Current Liabilities)

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Return on capital employed (ROCE) values.

 **Notes:**
 - The method retrieves historical data and calculates the ROCE for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

roce_ratios = toolkit.ratios.get_return_on_capital_employed()
{% endhighlight %}

## get_net_income_per_ebt
Calculate the net income per earnings before taxes (EBT), a profitability ratio that measures the net income generated for each dollar of EBT.

The net income per earnings before taxes (EBT) ratio helps evaluate the extent to which a company's net income is generated from its operating activities before considering the impact of income taxes. It gives insights into how effectively a company generates profit relative to its taxable income.

The formula is as follows:


- Net Income per EBT = Net Income / Income Before Tax

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Net income per earnings before taxes (EBT) values.

 **Notes:**
 - The method retrieves historical data and calculates the net income per EBT for each asset in
 the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values using
 the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

net_income_per_ebt_ratios = toolkit.ratios.get_net_income_per_ebt()
{% endhighlight %}

## get_free_cash_flow_operating_cash_flow_ratio
Calculate the free cash flow to operating cash flow ratio, a profitability ratio that measures the amount of free cash flow a company generates for every dollar of operating cash flow.

The free cash flow to operating cash flow ratio helps assess how well a company's operating activities translate into free cash flow, which is the cash available after all expenses and investments. A higher ratio indicates that the company is generating strong free cash flow relative to its operating cash flow, which could signify efficient capital management.

The formula is as follows:


- Free Cash Flow to Operating Cash Flow Ratio = Free Cash Flow / Cash Flow from Operations

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Free cash flow to operating cash flow ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the ratio for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

fcf_to_ocf_ratios = toolkit.ratios.get_free_cash_flow_operating_cash_flow_ratio()
{% endhighlight %}

## get_tax_burden_ratio
Calculate the tax burden ratio, which is the ratio of a company's net income to its income before tax, indicating how much of a company's income is retained after taxes.

The tax burden ratio measures the portion of a company's earnings that is paid as taxes. A higher ratio indicates that a larger portion of the income is being retained by the company after taxes. This ratio provides insights into the tax efficiency of the company and its ability to manage its tax liabilities.

The formula is as follows:


- Tax Burden Ratio = Net Income / Income Before Tax

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Tax burden ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the ratio for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

tax_burden_ratios = toolkit.ratios.get_tax_burden_ratio()
{% endhighlight %}

## get_EBT_to_EBIT
Calculate the EBT to EBIT, which is the ratio of a company's earnings before tax to its earnings before interest and taxes, indicating how much of a company's earnings are generated before paying interest on debt.

The EBT to EBIT ratio measures the proportion of a company's earnings that is generated before paying interest and taxes. It provides insights into how a company's operating performance is impacted by interest expenses and tax obligations. A higher ratio indicates that a larger portion of the company's earnings is generated from its core operations before considering interest payments and taxes.

The formula is as follows:


- EBT to EBIT = (Net Income + Income Tax Expense) / (Net Income + Income Tax Expense + Interest Expense)

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: EBT to EBIT ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the ratio for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

ebt_to_ebit_ratios = toolkit.ratios.get_EBT_to_EBIT()
{% endhighlight %}

## get_EBIT_to_revenue
Calculate the EBIT per Revenue, which is the ratio of a company's earnings before interest and taxes to its revenue, indicating how much profit a company generates from its operations before paying interest on debt and taxes on its earnings.

The EBIT to Revenue ratio measures the company's ability to generate profit from its core operations relative to its revenue. It provides insights into the operational efficiency and profitability of the company, as it excludes the impact of interest expenses and taxes on its earnings. A higher ratio indicates that a larger portion of the company's revenue is converted into operating profit.

The formula is as follows:


- EBIT to Revenue = EBIT / Revenue

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: EBIT to Revenue ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the ratio for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

ebit_to_revenue_ratios = toolkit.ratios.get_EBIT_to_revenue()
{% endhighlight %}

## collect_solvency_ratios
Calculates and collects all Solvency Ratios based on the provided data.

**Args:**
 - <u>diluted (bool, optional):</u> Whether to use diluted shares for the calculation. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Solvency ratios calculated based on the specified parameters.

 **Notes:**
 - The method calculates various solvency ratios for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

solvency_ratios = toolkit.ratios.collect_solvency_ratios()
{% endhighlight %}

## get_debt_to_assets_ratio
Calculate the debt to assets ratio, a solvency ratio that measures the proportion of a company's assets that are financed by debt.

This ratio, also known as the Debt Ratio, indicates the percentage of a company's total assets that are funded by debt. It is a measure of a company's financial leverage and indicates the extent to which a company relies on borrowed funds to finance its operations. A higher ratio implies a higher level of debt in the company's capital structure, which could increase financial risk.

The formula is as follows:


- Debt to Assets Ratio = Total Debt / Total Assets

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Debt to assets ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the ratio for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

debt_to_assets_ratios = toolkit.ratios.get_debt_to_assets_ratio()
{% endhighlight %}

## get_debt_to_equity_ratio
Calculate the debt to equity ratio, a solvency ratio that measures the proportion of a company's equity that is financed by debt. This ratio is also known as the Gearing Ratio.

The debt to equity ratio, for short the D/E ratio, indicates the relative contribution of debt and equity to a company's capital structure. It helps assess the level of financial risk a company carries due to its debt obligations. A higher ratio implies a higher reliance on debt to finance the business, which could increase risk but also potentially lead to higher returns for shareholders.

The formula is as follows:


- Debt to Equity Ratio = Total Debt / Total Equity

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Debt to equity ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the ratio for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

debt_to_equity_ratios = toolkit.ratios.get_debt_to_equity_ratio()
{% endhighlight %}

## get_interest_coverage_ratio
Calculate the interest coverage ratio, a solvency ratio that measures a company's ability to pay its interest expenses on outstanding debt.

The interest coverage ratio evaluates a company's ability to meet its interest obligations from its operating income. A higher ratio indicates a company's stronger ability to cover its interest payments using its earnings, implying lower financial risk. Conversely, a lower ratio suggests a company may have difficulty meeting its interest obligations and could be at higher risk of default.

The formula is as follows:


- Interest Coverage Ratio = Operating Income / (Interest Expense + Depreciation and Amortization)

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Interest coverage ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the ratio for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

interest_coverage_ratios = toolkit.ratios.get_interest_coverage_ratio()
{% endhighlight %}

## get_equity_multiplier
Calculate the equity multiplier, a solvency ratio that measures the degree to which a company uses borrowed money (debt) to finance its operations and growth.

The equity multiplier helps assess the financial leverage of a company by indicating how much of its assets are financed by equity versus debt. A higher equity multiplier suggests that the company relies more on debt financing, which can amplify returns but also increases financial risk. Conversely, a lower equity multiplier indicates a larger portion of assets is financed by equity, potentially lowering financial risk.

The formula is as follows:


- Equity Multiplier = Average Total Assets / Average Total Equity

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Equity multiplier values.

 **Notes:**
 - The method retrieves historical data and calculates the ratio for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

equity_multipliers = toolkit.ratios.get_equity_multiplier()
{% endhighlight %}

## get_debt_service_coverage_ratio
Calculate the debt service coverage ratio, a solvency ratio that measures a company's ability to service its debt with its net operating income.

The debt service coverage ratio provides insights into a company's ability to meet its debt obligations from its operating income. It is especially important for companies with significant debt obligations, as a lower ratio indicates higher financial risk and potential difficulties in servicing debt payments.

The formula is as follows:


- Debt Service Coverage Ratio = Operating Income / Total Current Liabilities

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Debt service coverage ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the ratio for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

debt_service_coverage_ratios = toolkit.ratios.get_debt_service_coverage_ratio()
{% endhighlight %}

## get_free_cash_flow_yield
Calculates the free cash flow yield ratio, which measures the free cash flow relative to the market capitalization of the company.

The free cash flow yield ratio is a measure of how efficiently a company generates free cash flow relative to its market value. It provides insights into whether the company's valuation is reasonable compared to the amount of cash it generates.

The formula is as follows:


- Free Cash Flow Yield Ratio = Free Cash Flow / Market Capitalization

**Args:**
 - <u>diluted (bool, optional):</u> Whether to use diluted shares for market capitalization. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Free cash flow yield ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the ratio for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

free_cash_flow_yield_ratios = toolkit.ratios.get_free_cash_flow_yield()
{% endhighlight %}

## get_net_debt_to_ebitda_ratio
Calculates the net debt to EBITDA ratio, which measures the net debt of the company relative to its EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization).

The net debt to EBITDA ratio is a measure of a company's ability to manage its debt obligations in relation to its earnings and cash flow. A lower ratio indicates better financial health and a stronger ability to manage debt.

The formula is as follows:


- Net Debt to EBITDA Ratio = Net Debt / EBITDA

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Net debt to EBITDA ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the ratio for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

net_debt_to_ebitda_ratios = toolkit.ratios.get_net_debt_to_ebitda_ratio()
{% endhighlight %}

## get_cash_flow_coverage_ratio
Calculate the cash flow coverage ratio, a solvency ratio that measures a company's ability to pay off its debt with its operating cash flow.

The cash flow coverage ratio assesses a company's ability to meet its debt obligations by comparing its operating cash flow to its total debt. A higher ratio indicates a stronger ability to cover its debt with cash generated from operations.

The formula is as follows:


- Cash Flow Coverage Ratio = Cash Flow from Operations / Total Debt

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Cash flow coverage ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the ratio for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

cash_flow_coverage_ratios = toolkit.ratios.get_cash_flow_coverage_ratio()
{% endhighlight %}

## get_capex_coverage_ratio
Calculate the capital expenditure coverage ratio, a solvency ratio that measures a company's ability to cover its capital expenditures with its cash flow from operations.

The capex coverage ratio evaluates a company's ability to fund its capital expenditures, which are essential for maintaining and growing its business, using the cash generated from its operations. A higher ratio indicates a stronger ability to fund capital investments from operating cash flow.

The formula is as follows:


- Capital Expenditure Coverage Ratio = Cash Flow from Operations / Capital Expenditure

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Capital expenditure coverage ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the ratio for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

capex_coverage_ratios = toolkit.ratios.get_capex_coverage_ratio()
{% endhighlight %}

## get_capex_dividend_coverage_ratio
Calculate the dividend paid and capital expenditure coverage ratio, a solvency ratio that measures a company's ability to cover both its capital expenditures and dividend payments with its cash flow from operations.

The capex dividend coverage ratio assesses whether a company's cash flow from operations is sufficient to cover both its capital expenditures (which are essential for maintaining and growing its business) and its dividend payments to shareholders. A higher ratio indicates a stronger ability to fund both capex and dividends from operating cash flow.

The formula is as follows:


- Dividend Paid and Capital Expenditure Coverage Ratio = Cash Flow from Operations / (Capital Expenditure + Dividends Paid)

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Dividend paid and capex coverage ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the ratio for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

capex_dividend_coverage_ratios = toolkit.ratios.get_capex_dividend_coverage_ratio()
{% endhighlight %}

## collect_valuation_ratios
Calculates and collects all Valuation Ratios based on the provided data.

**Args:**
 - <u>include_dividends (bool, optional):</u> Whether to include dividends in the calculations. Defaults to False.
 - <u>diluted (bool, optional):</u> Whether to use diluted shares for the calculation. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Valuation ratios calculated based on the specified parameters.

 **Notes:**
 - The method calculates various valuation ratios for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

valuation_ratios = toolkit.ratios.collect_valuation_ratios()
{% endhighlight %}

## get_earnings_per_share
Calculate the earnings per share (EPS), a valuation ratio that measures the amount of net income earned per share of outstanding common stock.

The earnings per share (EPS) is a widely used financial metric that helps investors understand the profitability of a company on a per
-share basis. It provides insight into the portion of a company's earnings that is allocated to each outstanding share of its common stock. EPS is an important measure for investors and analysts when assessing a company's financial performance and comparing it to other companies.

The formula is as follows:


- Earnings per Share (EPS) = (Net Income 
- Preferred Dividends Paid) / Weighted Average Shares

**Args:**
 - <u>include_dividends (bool, optional):</u> Whether to include dividends in the EPS calculation. Defaults to False.
 - <u>diluted (bool, optional):</u> Whether to use diluted earnings per share. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Earnings per share (EPS) values.

 **Notes:**
 - The method retrieves historical data and calculates the EPS for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the EPS values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

eps_ratios = toolkit.ratios.get_earnings_per_share()
{% endhighlight %}

## get_revenue_per_share
Calculate the revenue per share, a valuation ratio that measures the amount of revenue generated per outstanding share of a company's stock.

The revenue per share is an important metric that provides insight into a company's ability to generate revenue on a per
-share basis. It can help investors understand the company's revenue
-generation efficiency and its overall financial health.

The formula is as follows:


- Revenue per Share = Revenue / Weighted Average (Diluted) Shares

**Args:**
 - <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Revenue per share values.

 **Notes:**
 - The method retrieves historical data and calculates the revenue per share for each asset in
 the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the revenue per share values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

revenue_per_share = toolkit.ratios.get_revenue_per_share()
{% endhighlight %}

## get_price_earnings_ratio
Calculate the price earnings ratio (P/E), a valuation ratio that compares a company's stock price to its earnings per share.

The price earnings ratio is a widely used valuation metric that helps investors assess the relative value of a company's stock. A higher P/E ratio may indicate that the market has high expectations for the company's future growth, while a lower P/E ratio may suggest that the company is undervalued.

The formula is as follows:


- Price Earnings Ratio (P/E) = Share Price / Earnings per Share (EPS)

**Args:**
 - <u>include_dividends (bool, optional):</u> Whether to include dividends in the calculation. Defaults to False.
 - <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Price earnings ratio (P/E) values.

 **Notes:**
 - The method retrieves historical data and calculates the P/E ratio for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the P/E ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

pe_ratio = toolkit.ratios.get_price_earnings_ratio()
{% endhighlight %}

## get_price_to_earnings_growth_ratio
Calculate the price earnings to growth (PEG) ratio, a valuation metric that measures the ratio of the price
-to
-earnings ratio to earnings growth rate.

The price
-to
-earnings growth (PEG) ratio provides a more comprehensive valuation measure compared to the P/E ratio alone. It takes into account a company's earnings growth rate, allowing investors to assess whether a stock is overvalued or undervalued relative to its growth prospects.

The formula is as follows:


- Price Earnings to Growth Ratio (PEG) = Price Earnings Ratio (P/E) / Earnings per Share Growth

**Args:**
 - <u>include_dividends (bool, optional):</u> Whether to include dividends in the calculation. Defaults to False.
 - <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Price earnings to growth (PEG) ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the PEG ratio for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the PEG ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

peg_ratio = toolkit.ratios.get_price_to_earnings_growth_ratio()
{% endhighlight %}

## get_book_value_per_share
Calculate the book value per share, a valuation ratio that measures the amount of common equity value per share outstanding.

The book value per share is a fundamental valuation metric that reflects the net worth of a company attributed to each outstanding share of common stock.

The formula is as follows:


- Book Value per Share = (Total Shareholder Equity - Preferred Stock) / Weighted Average (Diluted) Shares

**Args:**
 - <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Book value per share values.

 **Notes:**
 - The method retrieves historical data and calculates the book value per share for each asset
 in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the book value per share values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

book_value_per_share = toolkit.ratios.get_book_value_per_share()
{% endhighlight %}

## get_price_to_book_ratio
Calculate the price to book ratio, a valuation ratio that compares a company's market price to its book value per share.

The price to book ratio is a key valuation metric that helps investors assess whether a company's stock is overvalued or undervalued relative to its underlying net asset value.

The formula is as follows:


- Price to Book Ratio = Share Price / Book Value per Share

**Args:**
 - <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Price to book ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the price to book ratio for each asset
 in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the price to book ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

price_to_book_ratio = toolkit.ratios.get_price_to_book_ratio()
{% endhighlight %}

## get_interest_debt_per_share
Calculate the interest debt per share, a valuation ratio that measures the amount of interest expense incurred per outstanding share of a company's stock.

The interest debt per share ratio provides insight into how much interest a company pays on its debt relative to its shareholder base. It can help investors assess the financial burden of interest expenses on the company's profitability.

The formula is as follows:


- Interest Debt per Share = (Interest Expense / Total Debt) / Weighted Average (Diluted) Shares

**Args:**
 - <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Interest debt per share values.

 **Notes:**
 - The method retrieves historical data and calculates the interest debt per share ratio for each asset
 in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the interest debt per share values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

interest_debt_per_share = toolkit.ratios.get_interest_debt_per_share()
{% endhighlight %}

## get_capex_per_share
Calculate the capex per share, a valuation ratio that measures the amount of capital expenditures made per outstanding share of a company's stock.

The capex per share ratio provides insight into how much capital a company invests in its operations and growth initiatives relative to its shareholder base. It can help investors assess the level of reinvestment into the business.

The formula is as follows:


- CAPEX per Share = Capital Expenditure / Weighted Average (Diluted) Shares

**Args:**
 - <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Capex per share values.

 **Notes:**
 - The method retrieves historical data and calculates the capex per share ratio for each asset
 in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the capex per share values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

capex_per_share = toolkit.ratios.get_capex_per_share()
{% endhighlight %}

## get_dividend_yield
Calculate the dividend yield ratio, a valuation ratio that measures the amount of dividends distributed per share of stock relative to the stock's price.

The dividend yield ratio is used by investors to assess the income potential of an investment in a company's stock based on the dividends it pays out. A higher dividend yield can be attractive to income
-seeking investors.

The formula is as follows:


- Dividend Yield = Dividends per Share / Share Price

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Dividend yield values.

 **Notes:**
 - The method retrieves historical data and calculates the dividend yield ratio for each asset
 in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the dividend yield values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

dividend_yield = toolkit.ratios.get_dividend_yield()
{% endhighlight %}

## get_weighted_dividend_yield
Calculate the weighted dividend yield ratio, a valuation ratio that measures the amount of dividends distributed per share of stock relative to the stock's price.

This dividend yield ratio takes into account the (diluted) weighted average shares and actual dividends paid as found in the cash flow statement. It provides a more accurate reflection of the dividends paid out per share, considering any changes in the number of shares.

The formula is as follows:


- Weighted Dividend Yield = Dividends Paid / Weighted Average (Diluted) Shares * Share Price

**Args:**
 - <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Weighted dividend yield values.

 **Notes:**
 - The method retrieves historical data and calculates the weighted dividend yield ratio for each asset
 in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the weighted dividend yield values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

weighted_dividend_yield = toolkit.ratios.get_weighted_dividend_yield()
{% endhighlight %}

## get_price_to_cash_flow_ratio
Calculate the price to cash flow ratio, a valuation ratio that compares a company's market price to its operating cash flow per share.

The price to cash flow ratio is a key valuation metric that helps investors assess the relative value of a company's stock. It is similar to the price to earnings ratio, but uses cash flow instead of earnings in the denominator.

The formula is as follows:


- Price to Cash Flow Ratio = Share Price / Cash Flow from Operations per Share

**Args:**
 - <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Price to cash flow ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the price to cash flow ratio for each asset
 in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the price to cash flow ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

price_to_cash_flow_ratio = toolkit.ratios.get_price_to_cash_flow_ratio()
{% endhighlight %}

## get_price_to_free_cash_flow_ratio
Calculate the price to free cash flow ratio, a valuation ratio that compares a company's market price to its free cash flow per share.

This ratio provides insight into how the market values a company's ability to generate free cash flow.

The formula is as follows:


- Price to Free Cash Flow Ratio = Market Cap / Free Cash Flow

**Args:**
 - <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Price to free cash flow ratio values.

 **Notes:**
 - The method retrieves historical data and calculates the price to free cash flow ratio for each asset
 in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the price to free cash flow ratio values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

price_to_free_cash_flow_ratio = toolkit.ratios.get_price_to_free_cash_flow_ratio()
{% endhighlight %}

## get_market_cap
Calculates the market capitalization of the company.

Market capitalization, often referred to as "market cap," is the total value of a company's outstanding shares of stock in the stock market. It is calculated by multiplying the current market price per share by the total number of outstanding shares.

The formula is as follows:


- Market Capitalization = Share Price * Weighted Average (Diluted) Shares

**Args:**
 - <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Market capitalization values.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

market_cap = toolkit.ratios.get_market_cap()
{% endhighlight %}

## get_enterprise_value
Calculates the Enterprise Value (EV) of a company. The Enterprise Value (EV) is a measure of a company's total value, often used as a more comprehensive alternative to market capitalization. It is calculated as the sum of a company's market capitalization, outstanding debt, minority interest, and preferred equity, minus the cash and cash equivalents.

The formula is as follows:


- Enterprise Value = Market Capitalization + Total Debt + Minority Interest + Preferred Equity - Cash and Cash Equivalents

**Args:**
 - <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Enterprise Value values.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

enterprise_value = toolkit.ratios.get_enterprise_value()
{% endhighlight %}

## get_ev_to_sales_ratio
Calculate the EV to sales ratio, a valuation ratio that compares a company's enterprise value (EV) to its total revenue.

This ratio compares the enterprise value (EV) to the total revenue generated by the company. It can provide insights into how efficiently a company is using its revenue to generate value for its investors.

The formula is as follows:


- Enterprise Value to Sales Ratio = Enterprise Value / Total Revenue

**Args:**
 - <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: EV to Sales Ratio values.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

ev_to_sales_ratio = toolkit.ratios.get_ev_to_sales_ratio()
{% endhighlight %}

## get_ev_to_ebitda_ratio
Calculate the enterprise value over EBITDA ratio, a valuation ratio that measures a company's total value (including debt and equity) relative to its EBITDA.

This ratio helps investors understand how many times the enterprise value exceeds the company's EBITDA, providing insights into the company's debt load and operating performance.

The formula is as follows:


- Enterprise Value to EBITDA Ratio = Enterprise Value / EBITDA

**Args:**
 - <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: EV to EBITDA Ratio values.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

ev_to_ebitda_ratio = toolkit.ratios.get_ev_to_ebitda_ratio()
{% endhighlight %}

## get_ev_to_operating_cashflow_ratio
Calculate the enterprise value over operating cash flow ratio, a valuation ratio that measures a company's total value (including debt and equity) relative to its operating cash flow.

The ratio is a valuation metric that helps investors assess the company's valuation relative to its operating cash flow. This ratio provides insights into how many times the enterprise value exceeds the company's operating cash flow, indicating the company's ability to generate cash from its operations.

The formula is as follows:


- Enterprise Value to Operating Cash Flow Ratio = Enterprise Value / Operating Cash Flow

**Args:**
 - <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: EV to Operating Cash Flow Ratio values.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

ev_to_operating_cashflow_ratio = toolkit.ratios.get_ev_to_operating_cashflow_ratio()
{% endhighlight %}

## get_earnings_yield
Calculate the earnings yield ratio, a valuation ratio that measures the earnings per share relative to the market price per share.

The earnings yield ratio is a valuation metric that provides insights into how much a company's earnings contribute to its stock price. It compares the earnings per share to the market price per share, helping investors understand the earnings potential of the company relative to its current market value

The formula is as follows:


- Earnings Yield Ratio = Earnings per Share / Share Price

**Args:**
 - <u>include_dividends (bool, optional):</u> Whether to include dividends in the calculation. Defaults to False.
 - <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Earnings Yield Ratio values.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

earnings_yield_ratio = toolkit.ratios.get_earnings_yield()
{% endhighlight %}

## get_dividend_payout_ratio
Calculate the Dividend payout ratio, a financial metric that measures the proportion of earnings paid out as dividends to shareholders.

The payout ratio is a financial metric that helps investors assess the portion of a company's earnings that is being distributed to shareholders in the form of dividends. It's a valuable indicator for dividend investors as it indicates the sustainability of dividend payments and the company's approach to distributing profits.

The formula is as follows:


- Dividend Payout Ratio = Dividends Paid / Net Income

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Payout Ratio values.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.ratios.get_dividend_payout_ratio()
{% endhighlight %}

## get_reinvestment_rate
Calculate the Reinvestment rate, a financial metric that measures the proportion of earnings retained by the company.

The reinvestment rate is a financial metric that helps investors assess the portion of a company's earnings that is being retained by the company for future growth. It's a valuable indicator for dividend investors as it indicates the sustainability of dividend payments and the company's approach to distributing profits.

The formula is as follows:


- Reinvestment Rate = 1 - Dividend Payout Ratio

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Reinvestment Rate values.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.ratios.get_reinvestment_rate()
{% endhighlight %}

## get_tangible_asset_value
Calculate the tangible asset value, a financial metric that represents the total value of a company's assets that can be used to generate revenue. Tangible assets are those physical assets that have a finite monetary value and can be sold, used, or consumed.

The formula is as follows:


- Tangible Asset Value = Total Assets - Total Liabilities - Goodwill

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Tangible Asset Value values.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

tangible_asset_value = toolkit.ratios.get_tangible_asset_value()
{% endhighlight %}

## get_net_current_asset_value
Calculate the net current asset value, a financial metric that represents the total value of a company's current assets minus its current liabilities. It indicates the extent to which a company's short
-term assets exceed its short
-term liabilities.

The formula is as follows:


- Net Current Asset Value = Total Current Assets - Total Current Liabilities

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Net Current Asset Value values.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

net_current_asset_value = toolkit.ratios.get_net_current_asset_value()
{% endhighlight %}

## get_ev_to_ebit
Calculate the enterprise value over earnings before interest and taxes (EBIT) ratio, which is a valuation metric that compares a company's total value (including debt and equity) relative to its earnings before interest and taxes.

The formula is as follows:


- Enterprise Value to EBIT Ratio = Enterprise Value / EBIT

**Args:**
 - <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
 - <u>trailing (int):</u> Defines whether to select a trailing period.
 E.g. when selecting 4 with quarterly data, the TTM is calculated.

 **Returns:**
 pd.DataFrame: Enterprise Value over EBIT values.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

ev_to_ebit_ratio = toolkit.ratios.get_ev_to_ebit()
{% endhighlight %}

