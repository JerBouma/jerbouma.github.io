---
title: Performance
excerpt: The Performance module is meant to calculate important performance metrics such as Sharpe Ratio, Sortino Ratio, Treynor Ratio, Information Ratio, Jensen's Alpha, Beta, Capital Asset Pricing Model, R-Squared and more.
description: The Performance module is meant to calculate important performance metrics such as Sharpe Ratio, Sortino Ratio, Treynor Ratio, Information Ratio, Jensen's Alpha, Beta, Capital Asset Pricing Model, R-Squared and more.
author_profile: false
permalink: /projects/financetoolkit/docs/performance
classes: wide-sidebar
layout: single
redirect_from:
  - /ratios
sidebar:
  nav: "financetoolkit-docs-performance"
---
The Performance module is meant to calculate important performance metrics such as Sharpe Ratio, Sortino Ratio, Treynor Ratio, Information Ratio, Jensen's Alpha, Beta, Capital Asset Pricing Model, R-Squared and more.

If you are looking for documentation regarding the toolkit, ratios, models, technicals, risk and economics, please have a look at the [Toolkit](/projects/financetoolkit/docs), [Ratios](/projects/financetoolkit/docs/ratios), [Models](/projects/financetoolkit/docs/models), [Technicals](/projects/financetoolkit/docs/technicals), [Risk](/projects/financetoolkit/docs/risk) and [Economics](/projects/financetoolkit/docs/economics) pages.

{% include algolia.html %}

## __init__
Initializes the Performance Controller Class.

**Args:**
 - <u>tickers (str | list[str]):</u> The tickers to use for the calculations.
 - <u>historical_data (dict[str, pd.DataFrame]):</u> The historical data to use for the calculations.
 - <u>risk_free_rate_data (pd.DataFrame):</u> The risk free rate data to use for the calculations.
 - <u>quarterly (bool | None, optional):</u> Whether to use quarterly data. Defaults to None.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>start_date (str | None, optional):</u> The start date to use for the calculations. Defaults to None.
 - <u>end_date (str | None, optional):</u> The end date to use for the calculations. Defaults to None.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key=FMP_KEY)

toolkit.performance.get_capital_asset_pricing_model(period='quarterly')
{% endhighlight %}


Which returns:

| Date | AAPL | TSLA |
 |:-------|--------:|--------:|
 | 2022Q3 | -0.0684 | -0.1047 |
 | 2022Q4 | 0.0857 | 0.0828 |
 | 2023Q1 | 0.075 | 0.1121 |
 | 2023Q2 | 0.0922 | 0.1342 |
 | 2023Q3 | 0.0052 | -0.0482 |

## get_beta
Calculate the Beta, a measurement that assess the systematic risk of a stock or investment.

Beta is a financial metric used to assess the systematic risk of a stock or investment in relation to the overall market. It provides valuable insights into how a particular asset's returns tend to move in response to fluctuations in the broader market. A stock's Beta is calculated by analyzing its historical price movements and their correlation with the movements of a market index, typically the benchmark index like the S&P 500.

The formula is as follows:


- Beta = Covariance of Asset Returns and Benchmark Returns / Variance of Benchmark Returns

For a given period, for example monthly, this translates into the following:


- Beta = Monthly Covariance of Asset Returns and Benchmark Returns / Monthly Variance of Benchmark Returns

See definition: [https://en.wikipedia.org/wiki/Beta_(finance)](https://en.wikipedia.org/wiki/Beta_(finance)){:target="_blank"}

**Args:**
 - <u>period (str, optional):</u> The period to use for the calculation. Defaults to None which
 results in basing it off the quarterly parameter as defined in the class instance.
 - <u>rolling (int, optional):</u> The rolling period to use for the calculation. If you select
 period = 'monthly' and set rolling to 12 you obtain the rolling 12-month Sharpe Ratio.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.

 Returns:
 pd.DataFrame: Beta values.

 Notes:
 - Daily Beta is not an option as the standard deviation for 1 day is close to zero. Therefore, it does
 not give any useful insights.
 - The method retrieves historical data and calculates the Beta for each asset in the Toolkit instance.
 - The risk-free rate is often represented by the return of a risk-free investment, such as a Treasury bond.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "AMZN"], api_key=FMP_KEY)

toolkit.performance.get_beta()
{% endhighlight %}

## get_capital_asset_pricing_model
CAPM, or the Capital Asset Pricing Model, is a financial model used to estimate the expected return on an investment, such as a stock or portfolio of stocks. It provides a framework for evaluating the risk and return trade
-off of an asset or portfolio in relation to the overall market. CAPM is based on the following key components:


- Risk
-Free Rate (Rf): This is the theoretical return an investor could earn from an investment with no risk of financial loss. It is typically based on the yield of a government bond. 
- Market Risk Premium (Rm 
- Rf): This represents the additional return that investors expect to earn for taking on the risk of investing in the overall market as opposed to a risk
-free asset. It is calculated as the difference between the expected return of the market (Rm) and the risk
-free rate (Rf). 
- Beta (β): Beta is a measure of an asset's or portfolio's sensitivity to market movements. It quantifies how much an asset's returns are expected to move in relation to changes in the overall market. A beta of 1 indicates that the asset moves in line with the market, while a beta greater than 1 suggests higher volatility, and a beta less than 1 indicates lower volatility.

The Capital Asset Pricing Model (CAPM) is a widely used financial model that helps in determining the expected return of an asset or portfolio based on its systematic risk and the prevailing risk
-free rate in the market. CAPM provides insights into how an asset or investment should be priced in order to offer an appropriate rate of return, given its level of risk compared to the overall market.

The formula is as follows:

Capital Asset Pricing Model = Risk Free Rate + Beta * (Benchmark Returns 
- Risk Free Rate)

See definition: [https://en.wikipedia.org/wiki/Capital_asset_pricing_model](https://en.wikipedia.org/wiki/Capital_asset_pricing_model){:target="_blank"}

**Args:**
 - <u>period (str, optional):</u> The period to use for the calculation. Defaults to None which
 results in basing it off the quarterly parameter as defined in the class instance.
 - <u>show_full_results (bool, optional):</u> Whether to show the full results. Defaults to False.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.

 Returns:
 pd.DataFrame: CAPM values.

 Notes:
 - Daily CAPM is not an option as the standard deviation for 1 day is close to zero. Therefore, it does
 not give any useful insights.
 - The method retrieves historical data and calculates the CAPM for each asset in the Toolkit instance.
 - The risk-free rate is often represented by the return of a risk-free investment, such as a Treasury bond.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key=FMP_KEY)

toolkit.performance.get_capital_asset_pricing_model()
{% endhighlight %}

## get_factor_asset_correlations
Calculates factor exposures for each asset.

The major difference between the Fama and French Model here is that the correlation is taken as opposed to a Linear Regression in which the R
-squared or Slope can be used to understand the exposure to each factor.

For assessing the exposure or influence of a stock to external factors, it's often preferable to use R
-squared (R²) or Beta because it explicitly measures how well the factors explain the stock's returns. A higher R² indicates that the stock's returns are more closely related to the factors, and thus, the factors have a greater influence on the stock's performance.

However, since the results are closely related and tend to point into the same direction it could be fine to use correlations as well depending on the level of accuracy required.

**Args:**
 - <u>period (str, optional):</u> The period to use for the calculation. Defaults to None which
 results in basing it off the quarterly parameter as defined in the class instance.
 - <u>factors_to_calculate (list of str, optional):</u> List of factors to calculate scores and residuals for.
 Defaults to ["Mkt-RF", "SMB", "HML", "RMW", "CMA"].
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.

 Returns:
 pd.DataFrame: Factor Asset Correlations.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key=FMP_KEY)

toolkit.performance.get_factor_asset_correlations()
{% endhighlight %}

## get_factor_correlations
Calculates factor correlations between each factor. This is useful to understand how correlated each factor is to each other. This is based off the Fama and French 5 Factor model which includes:


- Market Risk Premium (Mkt
-RF): Represents the additional return that investors expect to earn for taking on the risk of investing in the overall market as opposed to a risk
-free asset. 
- Size Premium (SMB): Reflects the historical excess return of small
-cap stocks over large
-cap stocks. 
- Value Premium (HML): Captures the historical excess return of value stocks over growth stocks. 
- Profitability (RMW): Measures the historical excess return of high profitability stocks over low profitability stocks. 
- Investment (CMA): Quantifies the historical excess return of low investment stocks over high investment stocks.

Optionally, it is also possible to see the correlation between the risk
-free rate and each factor.

**Args:**
 - <u>period (str, optional):</u> The period to use for the calculation. Defaults to None which
 results in basing it off the quarterly parameter as defined in the class instance.
 - <u>factors_to_calculate (list of str, optional):</u> List of factors to calculate scores and residuals for.
 Defaults to ["Mkt-RF", "SMB", "HML", "RMW", "CMA"].
 - <u>exclude_risk_free (bool, optional):</u> Whether to exclude the risk-free rate from the results. Defaults to True.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.

 Returns:
 pd.DataFrame: Factor Correlations.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key=FMP_KEY)

toolkit.performance.get_factor_correlations()
{% endhighlight %}

## get_fama_and_french_model
Calculate Fama and French 5 Factor model scores and residuals for a set of financial assets.

The Fama and French 5 Factor model is a widely used financial model that helps estimate the expected return of financial assets, such as stocks or portfolios, based on five key factors:


- Market Risk Premium (Mkt
-RF): Represents the additional return that investors expect to earn for taking on the risk of investing in the overall market as opposed to a risk
-free asset. 
- Size Premium (SMB): Reflects the historical excess return of small
-cap stocks over large
-cap stocks. 
- Value Premium (HML): Captures the historical excess return of value stocks over growth stocks. 
- Profitability (RMW): Measures the historical excess return of high profitability stocks over low profitability stocks. 
- Investment (CMA): Quantifies the historical excess return of low investment stocks over high investment stocks.

The model can perform both a Simple Linear Regression on each factor as well as a Multi Linear Regression which includes all factors. Generally, a multi linear regression is applied but if you wish to see individual R
-squared values for each factor you can select the simple linear regression method.

The model performs a Linear Regression on each factor and defines the regression parameters and residuals for each asset over time based on its exposure to these factors.

These results can be validated by comparing them to the period returns obtained from the historical data. E.g. the regression formula is as follows for the Multi Linear Regression:


- Excess Return = Intercept + Beta1 * Mkt
-RF + Beta2 * SMB + Beta3 * HML + Beta4 * RMW + Beta5 * CMA + Residuals

And the following for the Simple Linear Regression:


- Excess Return = Intercept + Slope * Factor Value + Residuals

So for a given factor, it should hold that the Excess Return equals the entire regression. Note that in this calculation the Excess Return refers to the Asset Return minus the Risk Free Rate as reported in the Fama and French dataset and will not be the same as the defined Excess Return in the historical data given that this is based on the Risk Free Rate defined in the initialization.

What is relevant to look at is the influence these factors have on each stock and how much each factor explains the stock return. E.g. you will generally see a pretty high influence (Beta or Slope) for the Market Risk Premium (Mkt
-RF) factor as this is the main factor that explains the stock return (as also prevalent in the CAPM). The other factors can fluctuate greatly between stocks depending on which stocks you look at.

**Args:**
 - <u>period (str, optional):</u> The period for the calculation (e.g., "weekly", "monthly", "quarterly", "yearly").
 Defaults to None, using class-defined quarterly or yearly period.
 - <u>method (str, optional):</u> The regression method to use for the calculation. Defaults to 'multi'.
 - <u>factors_to_calculate (list of str, optional):</u> List of factors to calculate scores and residuals for.
 Defaults to ["Mkt-RF", "SMB", "HML", "RMW", "CMA"].
 - <u>include_residuals (bool, optional):</u> Whether to include residuals in the results. Defaults to False.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratio values. Defaults to False.
 - <u>lag (int or list of int, optional):</u> The lag to use for the growth calculation. Defaults to 1.

 Returns:
 pd.DataFrame: Fama and French 5 Factor model scores for the specified assets.

 Notes:
 - The dataset from Fama and French is not always fully up to date. Therefore, some periods could be excluded.
 - Daily Fama and French results is not an option as it would attempt to do a linear regression on a
 single data point which will not give any meaningful results.
 - The method retrieves historical data and calculates regression parameters and residuals for each asset.
 - The risk-free rate is typically represented by the return of a risk-free investment, such as a Treasury bond.
 In this case, the Risk Free Rate from the Fama and French dataset is used.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 Example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key=FMP_KEY)

# Calculate Fama and French 5 Factor model scores
toolkit.performance.get_fama_and_french_model()
{% endhighlight %}

## get_alpha
Alpha, in a general sense, represents the excess return an investment generates relative to a benchmark or a risk
-adjusted return. It can be positive (indicating the investment outperformed the benchmark) or negative (indicating underperformance).

The formula is as follows:


- Alpha = Asset's Actual Return 
- Benchmark's Actual Return

See definition: [https://en.wikipedia.org/wiki/Alpha_(finance)](https://en.wikipedia.org/wiki/Alpha_(finance)){:target="_blank"}

**Args:**
 - <u>period (str, optional):</u> The period to use for the calculation. Defaults to None which
 results in basing it off the quarterly parameter as defined in the class instance.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.

 Returns:
 pd.DataFrame: Alpha values.

 Notes:
 - The method retrieves historical data and calculates the Alpha for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key=FMP_KEY)

toolkit.performance.get_alpha()
{% endhighlight %}

## get_jensens_alpha
Calculate Jensen's Alpha, a measure of an asset's performance relative to its expected return based on the Capital Asset Pricing Model (CAPM).

Jensen's Alpha is used to assess whether an investment has outperformed or underperformed its expected return given its systematic risk, as represented by the asset's Beta.

The formula for Jensen's Alpha is as follows:


- Jensen's Alpha = Asset's Actual Return 
- [Risk
-Free Rate + Beta * (Benchmark Return 
- Risk
-Free Rate)]

See definition: [https://en.wikipedia.org/wiki/Jensen%27s_alpha](https://en.wikipedia.org/wiki/Jensen%27s_alpha){:target="_blank"}

**Args:**
 - <u>period (str, optional):</u> The period to use for the calculation. Defaults to None which
 results in basing it off the quarterly parameter as defined in the class instance.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.

 Returns:
 pd.DataFrame: Jensen's Alpha values.

 Notes:
 - Daily Jensen's Alpha is not an option as the standard deviation for 1 day is close to zero. Therefore, it does
 not give any useful insights.
 - The method retrieves historical data and calculates the CAPM for each asset in the Toolkit instance.
 - The risk-free rate is often represented by the return of a risk-free investment, such as a Treasury bond.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key=FMP_KEY)

toolkit.performance.get_jensens_alpha()
{% endhighlight %}

## get_treynor_ratio
The Treynor Ratio, also known as Treynor's Measure or the Reward
-to
-Variability Ratio, is a financial metric used to assess the risk
-adjusted performance of an investment portfolio or asset. It measures the excess return generated by the portfolio per unit of systematic or market risk, often represented by Beta. The Treynor Ratio is a valuable tool for evaluating the performance of investments in relation to their market risk exposure.

The formula is as follows:


- Treynor Ratio = (Portfolio's Return 
- Risk
-Free Rate) / Portfolio Beta

See definition: [https://en.wikipedia.org/wiki/Treynor_ratio](https://en.wikipedia.org/wiki/Treynor_ratio){:target="_blank"}

**Args:**
 - <u>period (str, optional):</u> The period to use for the calculation. Defaults to None which
 results in basing it off the quarterly parameter as defined in the class instance.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.

 Returns:
 pd.DataFrame: Treynor Ratio values.

 Notes:
 - Daily Treynor Ratio is not an option as the standard deviation for 1 day is close to zero. Therefore,
 it does not give any useful insights.
 - The method retrieves historical data and calculates the TR for each asset in the Toolkit instance.
 - The risk-free rate is often represented by the return of a risk-free investment, such as a Treasury bond.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key=FMP_KEY)

toolkit.performance.get_treynor_ratio()
{% endhighlight %}

## get_sharpe_ratio
Calculate the Sharpe ratio, a measure of risk
-adjusted return that evaluates the excess return of an investment portfolio or asset per unit of risk taken.

The Sharpe ratio is calculated as the difference between the expected return of the asset or portfolio and the risk
-free rate of return, divided by the standard deviation of the asset or portfolio's excess return. It quantifies the amount of return generated for each unit of risk assumed, providing insights into the investment's performance relative to the risk taken.

The formula is as follows:


- Sharpe Ratio = Excess Return / Excess Standard Deviation

For a given period, for example monthly, this translates into the following:


- Sharpe Ratio = Average Monthly Excess Return / Standard Deviation of Monthly Excess Returns

For a rolling period, this translates into the following:


- Sharpe Ratio = Average Rolling Excess Return / Standard Deviation of Rolling Excess Returns

Note that this is explicitly already subtracts the Risk Free Rate.

See definition: [https://en.wikipedia.org/wiki/Sharpe_ratio](https://en.wikipedia.org/wiki/Sharpe_ratio){:target="_blank"}

**Args:**
 - <u>period (str, optional):</u> The period to use for the calculation. Defaults to None which
 results in basing it off the quarterly parameter as defined in the class instance.
 - <u>rolling (int, optional):</u> The rolling period to use for the calculation. If you select
 period = 'monthly' and set rolling to 12 you obtain the rolling 12-month Sharpe Ratio.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.

 Returns:
 pd.DataFrame: Sharpe ratio values.

 Notes:
 - Daily Sharpe Ratio is not an option as the standard deviation for 1 day is close to zero. Therefore, it does
 not give any useful insights.
 - The method retrieves historical data and calculates the Sharpe ratio for each asset in the Toolkit instance.
 - The risk-free rate is often represented by the return of a risk-free investment, such as a Treasury bond.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key=FMP_KEY)

toolkit.performance.get_sharpe_ratio()
{% endhighlight %}

## get_sortino_ratio
The Sortino Ratio is a financial metric used to assess the risk
-adjusted performance of an investment portfolio or asset by considering only the downside risk. It measures the excess return generated by the portfolio per unit of downside risk, specifically, the standard deviation of negative returns. The Sortino Ratio is particularly useful for investors who are primarily concerned with minimizing the downside risk of their investments.

The formula is as follows:


- Sortino Ratio = Excess Return / Excess Downside Risk

For a given period, for example monthly, this translates into the following:


- Sortino Ratio = Average Monthly Excess Return / Average Monthly Excess Downside Risk

For a rolling period, this translates into the following:


- Sortino Ratio = Average Rolling Excess Return / Rolling Downside Risk

Note that this is explicitly already subtracts the Risk Free Rate.

See definition: [https://en.wikipedia.org/wiki/Sortino_ratio](https://en.wikipedia.org/wiki/Sortino_ratio){:target="_blank"}

**Args:**
 - <u>period (str, optional):</u> The period to use for the calculation. Defaults to None which
 results in basing it off the quarterly parameter as defined in the class instance.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.

 Returns:
 pd.DataFrame: Sortino ratio values.

 Notes:
 - Daily Sortino Ratio is not an option as the standard deviation for 1 day is close to zero. Therefore, it does
 not give any useful insights.
 - The method retrieves historical data and calculates the Sortino ratio for each asset in the Toolkit instance.
 - The risk-free rate is often represented by the return of a risk-free investment, such as a Treasury bond.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key=FMP_KEY)

toolkit.performance.get_sortino_ratio()
{% endhighlight %}

## get_ulcer_performance_index
Calculate the Ulcer Performance Index (UPI), alternatively called Martin ratio, a measure of risk
-adjusted return that evaluates the excess return of an investment portfolio or asset per unit of risk taken.

It can be used to compare volatilities in different stocks or show stocks go into Ulcer territory. Similar to the Sharpe Ratio, a higher UPI is better than a lower one (since investors prefer more return for less risk).

**Args:**
 - <u>period (str, optional):</u> The period to use for the calculation. Defaults to None which
 results in basing it off the quarterly parameter as defined in the class instance.
 - <u>rolling (int):</u> The rolling period to use to calculate the Ulcer Index. Defaults to 14.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.

 Returns:
 pd.DataFrame: Ulcer Performance Index values.

 Notes:
 - The method retrieves historical data and calculates the UPI for each asset in the Toolkit instance.
 - The risk-free rate is often represented by the return of a risk-free investment, such as a Treasury bond.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key=FMP_KEY)

toolkit.performance.get_ulcer_performance_index()
{% endhighlight %}

## get_m2_ratio
The M2 Ratio, also known as the Modigliani
-Modigliani Measure, is a financial metric used to evaluate the risk
-adjusted performance of an investment portfolio or strategy. It assesses the excess return generated by the portfolio relative to a risk
-free investment, taking into account the portfolio's volatility or risk. The M2 Ratio helps investors and portfolio managers determine whether the portfolio is delivering returns that justify its level of risk.

The formula is as follows:


- M2 Ratio = (Portfolio's Return 
- Risk
-Free Rate) / Portfolio Standard Deviation

See definition: [https://en.wikipedia.org/wiki/Modigliani_risk
-adjusted_performance](https://en.wikipedia.org/wiki/Modigliani_risk
-adjusted_performance){:target="_blank"}

**Args:**
 - <u>period (str, optional):</u> The period to use for the calculation. Defaults to None which
 results in basing it off the quarterly parameter as defined in the class instance.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.

 Returns:
 pd.DataFrame: M2 ratio values.

 Notes:
 - Daily M2 is not an option as the standard deviation for 1 day is close to zero. Therefore, it does
 not give any useful insights.
 - The method retrieves historical data and calculates the M2 for each asset in the Toolkit instance.
 - The risk-free rate is often represented by the return of a risk-free investment, such as a Treasury bond.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key=FMP_KEY)

toolkit.performance.get_m2_ratio()
{% endhighlight %}

## get_tracking_error
Tracking Error is a financial metric that quantifies the volatility or dispersion of the difference between the returns of an investment portfolio or asset and the returns of a benchmark index. It measures how closely the portfolio tracks its benchmark and provides insights into the consistency of the portfolio's performance relative to the benchmark. A higher Tracking Error indicates greater divergence from the benchmark, while a lower Tracking Error suggests that the portfolio closely follows the benchmark.

The formula is as follows:


- Tracking Error (TE) = Standard Deviation of (Portfolio Returns 
- Benchmark Returns)

See definition: [https://en.wikipedia.org/wiki/Tracking_error](https://en.wikipedia.org/wiki/Tracking_error){:target="_blank"}

**Args:**
 - <u>period (str, optional):</u> The period to use for the calculation. Defaults to None which
 results in basing it off the quarterly parameter as defined in the class instance.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.

 Returns:
 pd.DataFrame: Tracking error values.

 Notes:
 - Daily Tracking Error is not an option as the standard deviation for 1 day is close to zero. Therefore, it does
 not give any useful insights.
 - The method retrieves historical data and calculates the TE for each asset in the Toolkit instance.
 - The risk-free rate is often represented by the return of a risk-free investment, such as a Treasury bond.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key=FMP_KEY)

toolkit.performance.get_tracking_error()
{% endhighlight %}

## get_information_ratio
The Information Ratio (IR), also known as the Information Coefficient, is a financial metric that assesses the risk
-adjusted performance of a portfolio or investment strategy relative to a benchmark index. It quantifies how much excess return the portfolio generates for each unit of tracking error (volatility of tracking error). The Information Ratio is commonly used by portfolio managers, financial analysts, and investors to evaluate the skill of a portfolio manager in generating returns beyond what would be expected based on the risk taken.


- IR > 0: A positive Information Ratio indicates that the portfolio has generated excess returns compared to the benchmark, suggesting that the portfolio manager has added value. 
- IR = 0: An Information Ratio of zero implies that the portfolio's excess return is in line with the benchmark, meaning the portfolio manager has not added or lost value relative to the benchmark. 
- IR < 0: A negative Information Ratio suggests that the portfolio has underperformed the benchmark, potentially indicating that the portfolio manager has detracted value.

The formula is as follows:


- Information Ratio (IR) = (Portfolio's Excess Return 
- Benchmark's Excess Return) / Tracking Error

See definition: [https://en.wikipedia.org/wiki/Information_ratio](https://en.wikipedia.org/wiki/Information_ratio){:target="_blank"}

**Args:**
 - <u>period (str, optional):</u> The period to use for the calculation. Defaults to None which
 results in basing it off the quarterly parameter as defined in the class instance.
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.

 Returns:
 pd.DataFrame: Information ratio values.

 Notes:
 - Daily Information Ratio is not an option as the standard deviation for 1 day is close to zero.
 Therefore, it does not give any useful insights.
 - The method retrieves historical data and calculates the IR for each asset in the Toolkit instance.
 - The risk-free rate is often represented by the return of a risk-free investment, such as a Treasury bond.
 - If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key=FMP_KEY)

toolkit.performance.get_information_ratio()
{% endhighlight %}

## get_compound_growth_rate
This function calculates the Compound Growth Rate (CGR) for different periods: yearly, quarterly, monthly, weekly, and daily.

The CGR is a measure that provides the mean growth rate of an investment over a specified period of time. It is a useful measure for comparing the performance of investments over different time periods or across different asset classes. The CGR is calculated by taking the ratio of the final value to the initial value, raising it to the inverse of the number of periods, and then subtracting one.

The formula is as follows:


- CGR = (Final Value / Initial Value) ^ (1 / Number of Periods) 
- 1

**Args:**
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. If not provided,
 the function will use the default rounding value set in the class instance.

 Returns:
 pd.DataFrame: A DataFrame containing the CGR for each period. The DataFrame has the periods
 as the index and the CGR values as the column.

 Notes:
 - When verifying the calculation, note that rounding applies and it could be slightly off because of that
 This is mostly noticeable when looking at the Compound Daily Growth Rate. Adjust the rounding with the
 rounding parameter accordingly to get a more precise figure.

 Example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key=FMP_KEY)

toolkit.performance.get_compound_growth_rate()
{% endhighlight %}

