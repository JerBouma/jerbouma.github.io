---
permalink: /projects/financetoolkit
title: Finance Toolkit
excerpt: This is an open-source toolkit in which 100+ financial ratios, indicators and performance measurements are written down in the most simplistic way allowing for complete transparency of the calculation method. This allows you to not have to rely on metrics from other providers and, given a financial statement, allow for efficient manual calculations. This leads to one uniform method of calculation being applied that is available and understood by everyone.
description: This is an open-source toolkit in which 100+ financial ratios, indicators and performance measurements are written down in the most simplistic way allowing for complete transparency of the calculation method. This allows you to not have to rely on metrics from other providers and, given a financial statement, allow for efficient manual calculations. This leads to one uniform method of calculation being applied that is available and understood by everyone.
classes: wide-sidebar
author_profile: false
redirect_from:
  - /financetoolkit
sidebar:
  nav: "financetoolkit"
---

While browsing a variety of websites, I kept finding that the same financial metric can greatly vary per source and so do the financial statements reported while little information is given how the metric was calculated.

For example, Microsoft's Price-to-Earnings (PE) ratio on the 6th of May, 2023 is reported to be 28.93 (Stockopedia), 32.05 (Morningstar), 32.66 (Macrotrends), 33.09 (Finance Charts), 33.66 (Y Charts), 33.67 (Wall Street Journal), 33.80 (Yahoo Finance) and 34.4 (Companies Market Cap). All of these calculations are correct, however the method applied varies leading to different results. Therefore, collecting data from multiple sources can lead to wrong interpretation of the results given that one source could be applying a different calculation method than another. And that is, if it is even freely available. Often the calculation is hidden behind a paid subscription.

**This is why I designed the FinanceToolkit**, this is an open-source toolkit in which 100+ financial ratios, indicators and performance measurements are written down in the most simplistic way allowing for complete transparency of the calculation method. This allows you to not have to rely on metrics from other providers and, given a financial statement, allow for efficient manual calculations. This leads to one uniform method of calculation being applied that is available and understood by everyone.

The Finance Toolkit is complimented very well with the [Finance Database 🌎](/projects/financedatabase), a database that features 300.000+ symbols containing Equities, ETFs, Funds, Indices, Currencies, Cryptocurrencies and Money Markets. By utilising both, it is possible to do a fully-fledged competitive analysis with the tickers found from the FinanceDatabase inputted into the FinanceToolkit.

<p align="center">
    <img src="https://github.com/JerBouma/FinanceToolkit/blob/main/examples/Finance%20Toolkit%20-%206.%20Video%20Demo.gif?raw=true" alt="Finance Toolkit Illustration" width="100%" onerror="this.style.display = 'none'"/>
</p>

## Installation

Before installation, consider starring the project on GitHub which helps others find the project as well. **Click the image to visit the repository and Star the project.**

<a href="https://github.com/JerBouma/FinanceToolkit" target="_blank"><img width="1415" alt="image" src="https://github.com/JerBouma/FinanceToolkit/assets/46355364/014109fe-0c68-47d4-99bd-217c69dcea8d">

To install the FinanceToolkit it simply requires the following:

```bash
pip install financetoolkit
```

Then within Python use:

```python
from financetoolkit import Toolkit
```
To be able to get started, you need to obtain an API Key from FinancialModelingPrep. This is used to gain access to 30+ years of financial statement both annually and quarterly. Note that the Free plan is limited to 250 requests each day, 5 years of data and only features companies listed on US exchanges.

___

<p><b><div align="center">Obtain an API Key from FinancialModelingPrep <a href="https://site.financialmodelingprep.com/developer/docs/pricing/jeroen/">here</a>.</div></b></p>
___

Through the link you are able to subscribe for the free plan and also premium plans at a **15% discount**. This is an affiliate link and thus supports the project at the same time. I have chosen FinancialModelingPrep as a source as I find it to be the most transparent, reliable and at an affordable price. I have yet to find a platform offering such low prices for the amount of data offered. When you notice that the data is inaccurate or have any other issue related to the data, note that I simply provide the means to access this data and I am not responsible for the accuracy of the data itself. For this, use [their contact form](https://site.financialmodelingprep.com/contact) or provide the data yourself. 

Within this package the following things are included:

- Company profiles (`get_profile`), including country, sector, ISIN and general characteristics (from FinancialModelingPrep)
- Company quotes (`get_quote`), including 52 week highs and lows, volume metrics and current shares outstanding (from FinancialModelingPrep)
- Company ratings (`get_rating`), based on key indicators like PE and DE ratios (from FinancialModelingPrep)
- Historical market data (`get_historical_data`), which can be retrieved on a daily, weekly, monthly and yearly basis. This includes OHLC, dividends, returns, cumulative returns and volatility calculations for each corresponding period. (from Yahoo Finance)
- Treasury Rates (`get_treasury_data`) for several months and several years over the last 3 months which allows yield curves to be constructed (from FinancialModelingPrep)
- Analyst Estimates (`get_analyst_estimates`) that show the expected EPS and Revenue from the past and future from a range of analysts (from FinancialModelingPrep)
- Earnings Calendar (`get_earnings_calendar`) which shows the exact dates earnings are released in the past and in the future including expectations (from FinancialModelingPrep)
- Revenue Geographic Segmentation (`get_revenue_geographic_segmentation`) which shows the revenue per company from each country and Revenue Product Segmentation (`get_revenue_product_segmenttion`) which shows the revenue per company from each product (from FinancialModelingPrep)
- Balance Sheet Statements (`get_balance_sheet_statement`), Income Statements (`get_income_statement`), Cash Flow Statements (`get_cash_flow_statement`) and Statistics Statement (`get_statistics_statement`), obtainable from FinancialModelingPrep or the source of your choosing through custom input. These functions are accompanied with a normalization function so that for any source, the same ratio analysis can be performed. Please see [this Jupyter Notebook](https://www.jeroenbouma.com/projects/financetoolkit/external-datasets) that explains how to use a custom source.
- Efficiency ratios (`ratios.collect_efficiency_ratios`), liquidity ratios (`ratios.collect_liquidity_ratios`), profitability ratios (`ratios._collect_profitability_ratios`), solvency ratios (`ratios.collect_solvency_ratios`) and valuation ratios (`ratios.collect_valuation_ratios`) functionality that automatically calculates the most important ratios based on the inputted balance sheet, income and cash flow statements. Any of the underlying ratios can also be called individually such as `ratios.get_return_on_equity`. Next to that, it is also possible to input your own custom ratios (`ratios.collect_custom_ratios`). See also [this Notebook](https://www.jeroenbouma.com/projects/financetoolkit/custom-ratios) or [this section](#defining-custom-ratios) for more information.
- Models like DUPONT analysis (`models.get_extended_dupont_analysis`) or Enterprise Breakdown (`models.get_enterprise_value_breakdown`) that can be used to perform in-depth financial analysis through a single function. These functions combine much of the functionality throughout the Toolkit to provide advanced calculations. 
- Technical indicators like Relative Strength Index (`technicals.get_relative_strength_index`),  Exponential Moving Average (`models.get_exponential_moving_average`) and Bollinger Bands (`technicals.get_bollinger_bands`) that can be used to perform in-depth momentum and trend analysis. These functions allow for the calculation of technical indicators based on the historical market data.

The dependencies of the package are on purpose *very slim* so that it will work well with any combination of packages and not result in conflicts.

## How-To Guides for the FinanceToolkit

This section contains a list of How-To guides for the Finance Toolkit. These guides are meant to show you how to use the Finance Toolkit and how to perform a financial analysis. The guides are written in the form of Jupyter Notebooks. You can view the notebooks by clicking on the button below the description.

<div class="row">
<div markdown="1" class="fifty-column-left mobile-max-column-width">

### Getting Started with the Finance Toolkit

The Finance Toolkit offers a comprehensive set of tools designed to empower users with in-depth insights into the world of finance. By demonstrating each functionality and its practical application. This notebook will show you how to get started with the Finance Toolkit.

[Open the Notebook](/projects/financetoolkit/getting-started){: .btn .btn--info}

</div>
<div markdown="1" class="fifty-column-right mobile-max-column-width">

### Visit the Code Documentation

Besides the practical examples, there exists a fully fledged documentation of the code. This documentation contains a description of each function, its parameters and an example. This allows you to quickly find the function you are looking for and understand how to use it.

[Visit the Code Documentation](/projects/financetoolkit/docs){: .btn .btn--warning}

</div>
</div>
<div markdown="1" class="fifty-column-left mobile-max-column-width">

### The Finance Database and the Finance Toolkit

This Notebooks demonstrates how to use the Finance Toolkit with the Finance Database to perform a complete financial analysis. Through the Finance Database you are able to find companies that are in the same country, sector and industry as the company you are analysing. This allows you to perform a complete competitive analysis with the help of the Finance Toolkit.

[Open the Notebook](/projects/financetoolkit/finance-database){: .btn .btn--info}

</div>

<div class="row">
<div markdown="1" class="fifty-column-right mobile-max-column-width">

### Creating Custom Ratios

The Finance Toolkit has an abundance of financial ratios, however it could be that you are looking for a specific ratio that is currently not provided. First and foremost, I encourage you to [create a Pull Request](https://github.com/JerBouma/FinanceToolkit/pulls) to add these ratios in but there is also an option to add custom ratios as follows. This feature was designed by [sword134](https://github.com/sword134).

[Open the Notebook](/projects/financetoolkit/custom-ratios){: .btn .btn--info}


</div>
</div>
<div markdown="1" class="fifty-column-left mobile-max-column-width">

### Calling Functions Directly

If you possess your own financial statements data or have a different particular use-case in mind, it could be that you wish to directly use the functions in the FinanceToolkit. This Notebook illustrates the process of accomplishing this.

[Open the Notebook](/projects/financetoolkit/functional-toolkit){: .btn .btn--info}

</div>

<div class="row">
<div markdown="1" class="fifty-column-right mobile-max-column-width">

### Using External Datasets

The Finance Toolkit has the ability to leverage custom datasets from any data provider as well. This makes it possible to work with your preferred data and not be limited to the data source the Finance Toolkit currently provides. With this, it is possible to work with datasets from Yahoo Finance, OpenBB, Quandl, EODH, Bloomberg and much more.

[Open the Notebook](/projects/financetoolkit/external-datasets){: .btn .btn--info}

</div>
</div>