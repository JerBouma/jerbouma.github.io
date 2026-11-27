---
title: Options
seo_title: "Black-Scholes and Option Greeks in Python | Finance Toolkit"
seo_title_suffix: false
excerpt: The Options module is meant to calculate important options metrics such as the First, Second and Third Order Greeks, the Black Scholes Model and the Option Chains as well as Implied Volatilities, Breeden Litzenberger and more.
description: "Price options with Black-Scholes and the binomial model, calculate every Greek and implied volatility and read option chains in Python with the Finance Toolkit."
author_profile: false
permalink: /projects/financetoolkit/docs/options
classes: wide-sidebar
layout: single
redirect_from:
    - /options
    - /projects/financetoolkit/options-notebook
    - /projects/financetoolkit/options-module
sidebar:
    nav: "financetoolkit-docs-options"
---

The Options module calculates important options metrics including First, Second and Third Order Greeks, the Black-Scholes Model, Option Chains, Implied Volatilities, Breeden–Litzenberger and more.

Use it in Claude, ChatGPT or another AI assistant through the [Finance Toolkit MCP](/projects/financetoolkit/mcp), or install the Python package:

```python
pip install financetoolkit -U
```

{% include docs-search.html %}

{% include financetoolkit-getting-started/options.md %}

## get_option_chains
Get the Option Chains: the currently available options of each ticker as reported by Yahoo Finance, with their prices, volume, open interest and implied volatility.

This returns the Expiration Date, Contract Symbol, Last Trade Date, Last Price, Bid, Ask, Change, Percent Change, Volume, Open Interest, Implied Volatility, whether the option is In The Money and the Currency.

Every ticker has its own expiration dates (one lists weekly options, another only monthly ones). Without an expiration date each ticker shows its nearest expiry; with one, a ticker that has no options expiring on that date is left out with a warning that lists its own expiration dates.

The data comes from Yahoo Finance. When Yahoo Finance has no options for a ticker, it is advised to use the theoretical calculations as provided by the Black Scholes Model as well as the Greeks to get a better understanding of the option prices over time.

**Also known as:** calls, puts, strike prices, expiry dates, option data.

**Args:**

- <u>expiration_date (str &#124; None, optional):</u> The expiration date to use. Defaults to None which means each
ticker uses its own nearest expiration date.
- <u>put_option (bool, optional):</u> Whether to show the put options instead of the call options.
Defaults to False.
- <u>show_expiration_dates (bool, optional):</u> Whether to return the available expiration dates instead of
the option chains: a list for a single ticker and a list per ticker (a dictionary) for several.
Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>strike_price_range (float &#124; None, optional):</u> Only the strikes within this fraction of the
current stock price, e.g. 0.05 for strikes within 5% of it. Defaults to None, which
keeps every strike.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: the option chains with the tickers and strike prices as the index
and the contract details (Expiration Date, Contract Symbol, Last Trade Date, Last
Price, Bid, Ask, Change, Percent Change (a decimal), Volume, Open Interest, Implied
Volatility, In The Money and Currency) as the columns. When every ticker shares
the expiration date, it is also stored as the DataFrame's name. If
show_expiration_dates is True, it returns the expiration dates instead.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["MSFT"], api_key="FINANCIAL_MODELING_PREP_KEY")

option_chains = toolkit.options.get_option_chains(strike_price_range=0.05)

option_chains.loc["MSFT", ["Bid", "Ask"]]
```

Which returns:

|   Strike Price |   Bid |   Ask |
|---------------:|------:|------:|
|          502.5 | 16.6  | 18.75 |
|          507.5 | 13.25 | 14.4  |
|          512.5 |  9.7  | 10.55 |
|          517.5 |  6.8  |  7.35 |
|          522.5 |  4.25 |  4.8  |
|          527.5 |  2.6  |  2.88 |
|          532.5 |  1.45 |  1.6  |
|          537.5 |  0.71 |  0.98 |
|          542.5 |  0.34 |  0.4  |

---

## collect_all_greeks
Calculate all Greeks of an option based on the Black Scholes Model: how the option value responds to the price of the underlying asset, the strike price, the volatility, time, the risk free rate and the dividend yield.

This will return the following Greeks per Strike Price and Expiration Date:

**First Order Greeks:**

- Delta: measures the rate of change of the theoretical option value with respect to changes in the underlying asset's price.
- Dual Delta: the first derivative of the option price with respect to the strike price. Up to the discount factor and a sign it is the risk-neutral probability of the option finishing in the money, negative for a call and positive for a put.
- Vega: measures sensitivity to volatility. Vega is the derivative of the option value with respect to the volatility of the underlying asset.
- Theta: measures the sensitivity of the value of the derivative to the passage of time, the "time decay."
- Rho: measures sensitivity to the interest rate: it is the derivative of the option value with respect to the risk-free interest rate (for the relevant outstanding term).
- Epsilon: measures the change in option value per unit (1.00) change in the dividend yield, the derivative of the value with respect to the dividend yield, a measure of the dividend risk.
- Lambda: measures the percentage change in option value per percentage change in the underlying price, a measure of leverage, sometimes called gearing. This greek is also sometimes called Omega or Elasticity.

**Second Order Greeks:**

- Gamma: measures the rate of change in the delta with respect to changes in the underlying price. Gamma is the second derivative of the value function with respect to the underlying price.
- Dual Gamma: the second derivative of the option value with respect to the strike price rather than the underlying price. It is the discounted risk-neutral probability density of the underlying at expiration.
- Vanna: also referred to as DvegaDspot and DdeltaDvol, is a second-order derivative of the option value, once to the underlying spot price and once to volatility.
- Charm: Charm or delta decay measures the instantaneous rate of change of delta over the passage of time.
- Vomma: also referred to as volga, vega convexity, or DvegaDvol measures second-order sensitivity to volatility. Vomma is the second derivative of the option value with respect to the volatility, or, stated another way, vomma measures the rate of change to vega as volatility changes.
- Veta: also referred to as DvegaDtime, measures the rate of change in the vega with respect to the passage of time. Veta is the second derivative of the value function; once to volatility and once to time.
- Vera: also referred to as rhova, measures the rate of change in rho with respect to volatility. Vera is the second derivative of the value function; once to volatility and once to interest rate.
- Partial Derivative: the second derivative of the option price with respect to the strike price, the rate at which the dual delta changes with the strike.

**Third Order Greeks:**

- Speed: measures the rate of change in Gamma with respect to changes in the underlying price.
- Zomma: measures the rate of change of Gamma with respect to changes in volatility.
- Color: also referred to as gamma decay or DgammaDtime measures the rate of change of gamma over the passage of time.
- Ultima: measures the sensitivity of the option vomma with respect to change in volatility.

For a deeper explanation, please have a look at: [https://en.wikipedia.org/wiki/Greeks_(finance)](https://en.wikipedia.org/wiki/Greeks_(finance)){:target="_blank"} and the references to the literature as found on this page.

By default the stock price (the traded close), risk free rate, dividend yield and volatility of the most recent date are used; changing the start date prices the option as of that date instead. The volatility is the annualized standard deviation of the daily returns over the year before that date and the dividend yield the dividends of the 365 days up to that date relative to its close, so an earlier start date only uses what was known on that date. The exception is a date in the first year of the price history: without a full year before it, it takes the dividend yield of the first date that has one.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None, which
uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>put_option (bool, optional):</u> Whether to calculate the put option delta. Defaults to False which means
it will calculate the call option delta.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: the greeks values containing the tickers and strike prices as the index and the
time to expiration and greeks as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["TSLA", "MU"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

all_greeks = toolkit.options.collect_all_greeks(start_date='2024-01-03')

all_greeks.loc['TSLA', '2024-01-04']
```

Which returns:

|   Strike Price |   Delta |   Dual Delta |   Vega |   Theta |    Rho |   Epsilon |   Lambda |   Gamma |   Dual Gamma |   Vanna |    Charm |   Vomma |    Vera |    Veta |     PD |   Speed |   Zomma |   Color |   Ultima |
|---------------:|--------:|-------------:|-------:|--------:|-------:|----------:|---------:|--------:|-------------:|--------:|---------:|--------:|--------:|--------:|-------:|--------:|--------:|--------:|---------:|
|            180 |  1      |      -0.9999 | 0      | -0.0191 | 0.4931 |   -0.6533 |   4.0782 |  0      |       0      |  0      |   0      |  0      |  0      |  0      | 0      |  0      |  0      |  0      |   0      |
|            185 |  1      |      -0.9999 | 0      | -0.0196 | 0.5068 |   -0.6533 |   4.4595 |  0      |       0      |  0      |   0      |  0      |  0      |  0      | 0      |  0      |  0      |  0      |   0      |
|            190 |  1      |      -0.9999 | 0      | -0.0201 | 0.5205 |   -0.6533 |   4.9195 |  0      |       0      |  0      |   0      |  0      |  0      |  0      | 0      |  0      |  0      |  0      |   0      |
|            195 |  1      |      -0.9999 | 0      | -0.0207 | 0.5342 |   -0.6533 |   5.4853 |  0      |       0      |  0      |   0      |  0      |  0      |  0      | 0      |  0      |  0      |  0      |   0      |
|            200 |  1      |      -0.9999 | 0      | -0.0212 | 0.5479 |   -0.6533 |   6.1981 |  0      |       0      |  0      |   0      |  0      |  0      |  0      | 0      |  0      |  0      |  0      |   0.0001 |
|            205 |  1      |      -0.9999 | 0      | -0.0217 | 0.5616 |   -0.6533 |   7.1239 |  0      |       0      |  0      |   0.0002 |  0.0001 |  0      |  0      | 0      |  0      |  0      | -0.0002 |   0.0071 |
|            210 |  1      |      -0.9999 | 0      | -0.0223 | 0.5753 |   -0.6533 |   8.3748 |  0      |       0      | -0.0001 |   0.0124 |  0.0071 | -0.0001 |  0      | 0      |  0      |  0.0001 | -0.0079 |   0.2259 |
|            215 |  0.9999 |      -0.9998 | 0.0001 | -0.0243 | 0.5889 |   -0.6532 |  10.1573 |  0.0001 |       0.0001 | -0.0031 |   0.3046 |  0.1422 | -0.002  | -0.0004 | 0.0001 |  0      |  0.0016 | -0.1539 |   2.7473 |
|            220 |  0.9979 |      -0.9976 | 0.0008 | -0.0454 | 0.6013 |   -0.6519 |  12.8781 |  0.001  |       0.0011 | -0.0345 |   3.3878 |  1.2328 | -0.0227 | -0.0037 | 0.0011 | -0.0004 |  0.0129 | -1.2629 |  11.7206 |
|            225 |  0.9808 |      -0.9794 | 0.0058 | -0.1807 | 0.6037 |   -0.6408 |  17.2971 |  0.0069 |       0.0078 | -0.1766 |  17.3413 |  4.5652 | -0.1169 | -0.0152 | 0.0078 | -0.0022 |  0.0414 | -4.0651 |  10.4164 |
|            230 |  0.9022 |      -0.8971 | 0.0216 | -0.6039 | 0.5653 |   -0.5894 |  24.4771 |  0.0256 |       0.0275 | -0.4047 |  39.6564 |  6.5366 | -0.2703 | -0.0283 | 0.0275 | -0.005  |  0.0303 | -2.9376 | -16.4877 |
|            235 |  0.7031 |      -0.6932 | 0.0432 | -1.1837 | 0.4463 |   -0.4593 |  35.2284 |  0.0513 |       0.0528 | -0.3236 |  31.4261 |  2.1544 | -0.2232 | -0.0273 | 0.0528 | -0.0043 | -0.0694 |  6.8815 | -10.9032 |
|            240 |  0.4163 |      -0.4053 | 0.0487 | -1.3253 | 0.2665 |   -0.272  |  49.5403 |  0.0579 |       0.0571 |  0.173  | -17.591  |  0.4563 |  0.0997 | -0.0256 | 0.0571 |  0.0016 | -0.1017 | 10.0103 |  -2.5052 |
|            245 |  0.1734 |      -0.1663 | 0.032  | -0.8683 | 0.1116 |   -0.1133 |  66.7064 |  0.038  |       0.036  |  0.4598 | -45.6743 |  5.398  |  0.2916 | -0.0307 | 0.036  |  0.0051 | -0.0062 |  0.5661 | -20.8824 |
|            250 |  0.0489 |      -0.0461 | 0.0127 | -0.343  | 0.0316 |   -0.032  |  85.8355 |  0.015  |       0.0137 |  0.316  | -31.2885 |  6.5283 |  0.203  | -0.024  | 0.0137 |  0.0036 |  0.0497 | -4.9376 |  -2.5834 |
|            255 |  0.0092 |      -0.0086 | 0.0031 | -0.0841 | 0.006  |   -0.006  | 106.18   |  0.0037 |       0.0032 |  0.1098 | -10.8605 |  3.2292 |  0.0709 | -0.0103 | 0.0032 |  0.0013 |  0.0315 | -3.1214 |  15.6375 |
|            260 |  0.0012 |      -0.0011 | 0.0005 | -0.0132 | 0.0008 |   -0.0008 | 127.21   |  0.0006 |       0.0005 |  0.0222 |  -2.1897 |  0.8415 |  0.0143 | -0.0025 | 0.0005 |  0.0003 |  0.0089 | -0.8827 |   9.8817 |
|            265 |  0.0001 |      -0.0001 | 0      | -0.0014 | 0.0001 |   -0.0001 | 148.577  |  0.0001 |       0      |  0.0028 |  -0.2738 |  0.1286 |  0.0018 | -0.0004 | 0      |  0      |  0.0014 | -0.1401 |   2.5989 |
|            270 |  0      |       0      | 0      | -0.0001 | 0      |    0      | 170.056  |  0      |       0      |  0.0002 |  -0.0222 |  0.0123 |  0.0001 |  0      | 0      |  0      |  0.0001 | -0.0137 |   0.37   |
|            275 |  0      |       0      | 0      |  0      | 0      |    0      | 191.505  |  0      |       0      |  0      |  -0.0012 |  0.0008 |  0      |  0      | 0      |  0      |  0      | -0.0009 |   0.0317 |
|            280 |  0      |       0      | 0      |  0      | 0      |    0      | 212.831  |  0      |       0      |  0      |   0      |  0      |  0      |  0      | 0      |  0      |  0      |  0      |   0.0017 |
|            285 |  0      |       0      | 0      |  0      | 0      |    0      | 233.975  |  0      |       0      |  0      |   0      |  0      |  0      |  0      | 0      |  0      |  0      |  0      |   0.0001 |
|            290 |  0      |       0      | 0      |  0      | 0      |    0      | 254.901  |  0      |       0      |  0      |   0      |  0      |  0      |  0      | 0      |  0      |  0      |  0      |   0      |
|            295 |  0      |       0      | 0      |  0      | 0      |    0      | 275.584  |  0      |       0      |  0      |   0      |  0      |  0      |  0      | 0      |  0      |  0      |  0      |   0      |

---

## collect_first_order_greeks
Calculate the first order Greeks of an option based on the Black Scholes Model: how the option value responds to the price of the underlying asset, the strike price, the volatility, time, the risk free rate and the dividend yield.

This will return the following Greeks per Strike Price and Expiration Date:

- Delta: measures the rate of change of the theoretical option value with respect to changes in the underlying asset's price.
- Dual Delta: the first derivative of the option price with respect to the strike price. Up to the discount factor and a sign it is the risk-neutral probability of the option finishing in the money, negative for a call and positive for a put.
- Vega: measures sensitivity to volatility. Vega is the derivative of the option value with respect to the volatility of the underlying asset.
- Theta: measures the sensitivity of the value of the derivative to the passage of time, the "time decay."
- Rho: measures sensitivity to the interest rate: it is the derivative of the option value with respect to the risk-free interest rate (for the relevant outstanding term).
- Epsilon: measures the change in option value per unit (1.00) change in the dividend yield, the derivative of the value with respect to the dividend yield, a measure of the dividend risk.
- Lambda: measures the percentage change in option value per percentage change in the underlying price, a measure of leverage, sometimes called gearing. This greek is also sometimes called Omega or Elasticity.

For a deeper explanation, please have a look at: [https://en.wikipedia.org/wiki/Greeks_(finance)](https://en.wikipedia.org/wiki/Greeks_(finance)){:target="_blank"} and the references to the literature as found on this page.

By default the stock price (the traded close), risk free rate, dividend yield and volatility of the most recent date are used; changing the start date prices the option as of that date instead. The volatility is the annualized standard deviation of the daily returns over the year before that date and the dividend yield the dividends of the 365 days up to that date relative to its close, so an earlier start date only uses what was known on that date. The exception is a date in the first year of the price history: without a full year before it, it takes the dividend yield of the first date that has one.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None, which
uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>put_option (bool, optional):</u> Whether to calculate the put option delta. Defaults to False which means
it will calculate the call option delta.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: the first order greek values containing the tickers and strike prices as the index
and the time to expiration and greeks as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "ASML"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.options.collect_first_order_greeks().loc["AAPL"]
```

Which returns:

|   Strike Price |   (Period('2026-01-01', 'D'), 'Delta') |   (Period('2026-01-01', 'D'), 'Dual Delta') |   (Period('2026-01-01', 'D'), 'Vega') |   (Period('2026-01-01', 'D'), 'Theta') |   (Period('2026-01-01', 'D'), 'Rho') |   (Period('2026-01-01', 'D'), 'Epsilon') |   (Period('2026-01-01', 'D'), 'Lambda') |   (Period('2026-01-02', 'D'), 'Delta') |   (Period('2026-01-02', 'D'), 'Dual Delta') |   (Period('2026-01-02', 'D'), 'Vega') |   (Period('2026-01-02', 'D'), 'Theta') |   (Period('2026-01-02', 'D'), 'Rho') |   (Period('2026-01-02', 'D'), 'Epsilon') |   (Period('2026-01-02', 'D'), 'Lambda') |   (Period('2026-01-03', 'D'), 'Delta') |   (Period('2026-01-03', 'D'), 'Dual Delta') |   (Period('2026-01-03', 'D'), 'Vega') |   (Period('2026-01-03', 'D'), 'Theta') |   (Period('2026-01-03', 'D'), 'Rho') |   (Period('2026-01-03', 'D'), 'Epsilon') |   (Period('2026-01-03', 'D'), 'Lambda') |   (Period('2026-01-04', 'D'), 'Delta') |   (Period('2026-01-04', 'D'), 'Dual Delta') |   (Period('2026-01-04', 'D'), 'Vega') |   (Period('2026-01-04', 'D'), 'Theta') |   (Period('2026-01-04', 'D'), 'Rho') |   (Period('2026-01-04', 'D'), 'Epsilon') |   (Period('2026-01-04', 'D'), 'Lambda') |   (Period('2026-01-05', 'D'), 'Delta') |   (Period('2026-01-05', 'D'), 'Dual Delta') |   (Period('2026-01-05', 'D'), 'Vega') |   (Period('2026-01-05', 'D'), 'Theta') |   (Period('2026-01-05', 'D'), 'Rho') |   (Period('2026-01-05', 'D'), 'Epsilon') |   (Period('2026-01-05', 'D'), 'Lambda') |   (Period('2026-01-06', 'D'), 'Delta') |   (Period('2026-01-06', 'D'), 'Dual Delta') |   (Period('2026-01-06', 'D'), 'Vega') |   (Period('2026-01-06', 'D'), 'Theta') |   (Period('2026-01-06', 'D'), 'Rho') |   (Period('2026-01-06', 'D'), 'Epsilon') |   (Period('2026-01-06', 'D'), 'Lambda') |   (Period('2026-01-07', 'D'), 'Delta') |   (Period('2026-01-07', 'D'), 'Dual Delta') |   (Period('2026-01-07', 'D'), 'Vega') |   (Period('2026-01-07', 'D'), 'Theta') |   (Period('2026-01-07', 'D'), 'Rho') |   (Period('2026-01-07', 'D'), 'Epsilon') |   (Period('2026-01-07', 'D'), 'Lambda') |   (Period('2026-01-08', 'D'), 'Delta') |   (Period('2026-01-08', 'D'), 'Dual Delta') |   (Period('2026-01-08', 'D'), 'Vega') |   (Period('2026-01-08', 'D'), 'Theta') |   (Period('2026-01-08', 'D'), 'Rho') |   (Period('2026-01-08', 'D'), 'Epsilon') |   (Period('2026-01-08', 'D'), 'Lambda') |   (Period('2026-01-09', 'D'), 'Delta') |   (Period('2026-01-09', 'D'), 'Dual Delta') |   (Period('2026-01-09', 'D'), 'Vega') |   (Period('2026-01-09', 'D'), 'Theta') |   (Period('2026-01-09', 'D'), 'Rho') |   (Period('2026-01-09', 'D'), 'Epsilon') |   (Period('2026-01-09', 'D'), 'Lambda') |   (Period('2026-01-10', 'D'), 'Delta') |   (Period('2026-01-10', 'D'), 'Dual Delta') |   (Period('2026-01-10', 'D'), 'Vega') |   (Period('2026-01-10', 'D'), 'Theta') |   (Period('2026-01-10', 'D'), 'Rho') |   (Period('2026-01-10', 'D'), 'Epsilon') |   (Period('2026-01-10', 'D'), 'Lambda') |   (Period('2026-01-11', 'D'), 'Delta') |   (Period('2026-01-11', 'D'), 'Dual Delta') |   (Period('2026-01-11', 'D'), 'Vega') |   (Period('2026-01-11', 'D'), 'Theta') |   (Period('2026-01-11', 'D'), 'Rho') |   (Period('2026-01-11', 'D'), 'Epsilon') |   (Period('2026-01-11', 'D'), 'Lambda') |   (Period('2026-01-12', 'D'), 'Delta') |   (Period('2026-01-12', 'D'), 'Dual Delta') |   (Period('2026-01-12', 'D'), 'Vega') |   (Period('2026-01-12', 'D'), 'Theta') |   (Period('2026-01-12', 'D'), 'Rho') |   (Period('2026-01-12', 'D'), 'Epsilon') |   (Period('2026-01-12', 'D'), 'Lambda') |   (Period('2026-01-13', 'D'), 'Delta') |   (Period('2026-01-13', 'D'), 'Dual Delta') |   (Period('2026-01-13', 'D'), 'Vega') |   (Period('2026-01-13', 'D'), 'Theta') |   (Period('2026-01-13', 'D'), 'Rho') |   (Period('2026-01-13', 'D'), 'Epsilon') |   (Period('2026-01-13', 'D'), 'Lambda') |   (Period('2026-01-14', 'D'), 'Delta') |   (Period('2026-01-14', 'D'), 'Dual Delta') |   (Period('2026-01-14', 'D'), 'Vega') |   (Period('2026-01-14', 'D'), 'Theta') |   (Period('2026-01-14', 'D'), 'Rho') |   (Period('2026-01-14', 'D'), 'Epsilon') |   (Period('2026-01-14', 'D'), 'Lambda') |   (Period('2026-01-15', 'D'), 'Delta') |   (Period('2026-01-15', 'D'), 'Dual Delta') |   (Period('2026-01-15', 'D'), 'Vega') |   (Period('2026-01-15', 'D'), 'Theta') |   (Period('2026-01-15', 'D'), 'Rho') |   (Period('2026-01-15', 'D'), 'Epsilon') |   (Period('2026-01-15', 'D'), 'Lambda') |   (Period('2026-01-16', 'D'), 'Delta') |   (Period('2026-01-16', 'D'), 'Dual Delta') |   (Period('2026-01-16', 'D'), 'Vega') |   (Period('2026-01-16', 'D'), 'Theta') |   (Period('2026-01-16', 'D'), 'Rho') |   (Period('2026-01-16', 'D'), 'Epsilon') |   (Period('2026-01-16', 'D'), 'Lambda') |   (Period('2026-01-17', 'D'), 'Delta') |   (Period('2026-01-17', 'D'), 'Dual Delta') |   (Period('2026-01-17', 'D'), 'Vega') |   (Period('2026-01-17', 'D'), 'Theta') |   (Period('2026-01-17', 'D'), 'Rho') |   (Period('2026-01-17', 'D'), 'Epsilon') |   (Period('2026-01-17', 'D'), 'Lambda') |   (Period('2026-01-18', 'D'), 'Delta') |   (Period('2026-01-18', 'D'), 'Dual Delta') |   (Period('2026-01-18', 'D'), 'Vega') |   (Period('2026-01-18', 'D'), 'Theta') |   (Period('2026-01-18', 'D'), 'Rho') |   (Period('2026-01-18', 'D'), 'Epsilon') |   (Period('2026-01-18', 'D'), 'Lambda') |   (Period('2026-01-19', 'D'), 'Delta') |   (Period('2026-01-19', 'D'), 'Dual Delta') |   (Period('2026-01-19', 'D'), 'Vega') |   (Period('2026-01-19', 'D'), 'Theta') |   (Period('2026-01-19', 'D'), 'Rho') |   (Period('2026-01-19', 'D'), 'Epsilon') |   (Period('2026-01-19', 'D'), 'Lambda') |   (Period('2026-01-20', 'D'), 'Delta') |   (Period('2026-01-20', 'D'), 'Dual Delta') |   (Period('2026-01-20', 'D'), 'Vega') |   (Period('2026-01-20', 'D'), 'Theta') |   (Period('2026-01-20', 'D'), 'Rho') |   (Period('2026-01-20', 'D'), 'Epsilon') |   (Period('2026-01-20', 'D'), 'Lambda') |   (Period('2026-01-21', 'D'), 'Delta') |   (Period('2026-01-21', 'D'), 'Dual Delta') |   (Period('2026-01-21', 'D'), 'Vega') |   (Period('2026-01-21', 'D'), 'Theta') |   (Period('2026-01-21', 'D'), 'Rho') |   (Period('2026-01-21', 'D'), 'Epsilon') |   (Period('2026-01-21', 'D'), 'Lambda') |   (Period('2026-01-22', 'D'), 'Delta') |   (Period('2026-01-22', 'D'), 'Dual Delta') |   (Period('2026-01-22', 'D'), 'Vega') |   (Period('2026-01-22', 'D'), 'Theta') |   (Period('2026-01-22', 'D'), 'Rho') |   (Period('2026-01-22', 'D'), 'Epsilon') |   (Period('2026-01-22', 'D'), 'Lambda') |   (Period('2026-01-23', 'D'), 'Delta') |   (Period('2026-01-23', 'D'), 'Dual Delta') |   (Period('2026-01-23', 'D'), 'Vega') |   (Period('2026-01-23', 'D'), 'Theta') |   (Period('2026-01-23', 'D'), 'Rho') |   (Period('2026-01-23', 'D'), 'Epsilon') |   (Period('2026-01-23', 'D'), 'Lambda') |   (Period('2026-01-24', 'D'), 'Delta') |   (Period('2026-01-24', 'D'), 'Dual Delta') |   (Period('2026-01-24', 'D'), 'Vega') |   (Period('2026-01-24', 'D'), 'Theta') |   (Period('2026-01-24', 'D'), 'Rho') |   (Period('2026-01-24', 'D'), 'Epsilon') |   (Period('2026-01-24', 'D'), 'Lambda') |   (Period('2026-01-25', 'D'), 'Delta') |   (Period('2026-01-25', 'D'), 'Dual Delta') |   (Period('2026-01-25', 'D'), 'Vega') |   (Period('2026-01-25', 'D'), 'Theta') |   (Period('2026-01-25', 'D'), 'Rho') |   (Period('2026-01-25', 'D'), 'Epsilon') |   (Period('2026-01-25', 'D'), 'Lambda') |   (Period('2026-01-26', 'D'), 'Delta') |   (Period('2026-01-26', 'D'), 'Dual Delta') |   (Period('2026-01-26', 'D'), 'Vega') |   (Period('2026-01-26', 'D'), 'Theta') |   (Period('2026-01-26', 'D'), 'Rho') |   (Period('2026-01-26', 'D'), 'Epsilon') |   (Period('2026-01-26', 'D'), 'Lambda') |   (Period('2026-01-27', 'D'), 'Delta') |   (Period('2026-01-27', 'D'), 'Dual Delta') |   (Period('2026-01-27', 'D'), 'Vega') |   (Period('2026-01-27', 'D'), 'Theta') |   (Period('2026-01-27', 'D'), 'Rho') |   (Period('2026-01-27', 'D'), 'Epsilon') |   (Period('2026-01-27', 'D'), 'Lambda') |   (Period('2026-01-28', 'D'), 'Delta') |   (Period('2026-01-28', 'D'), 'Dual Delta') |   (Period('2026-01-28', 'D'), 'Vega') |   (Period('2026-01-28', 'D'), 'Theta') |   (Period('2026-01-28', 'D'), 'Rho') |   (Period('2026-01-28', 'D'), 'Epsilon') |   (Period('2026-01-28', 'D'), 'Lambda') |   (Period('2026-01-29', 'D'), 'Delta') |   (Period('2026-01-29', 'D'), 'Dual Delta') |   (Period('2026-01-29', 'D'), 'Vega') |   (Period('2026-01-29', 'D'), 'Theta') |   (Period('2026-01-29', 'D'), 'Rho') |   (Period('2026-01-29', 'D'), 'Epsilon') |   (Period('2026-01-29', 'D'), 'Lambda') |
|---------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------------:|----------------------------------------:|
|            290 |                                 0.0001 |                                     -0.0001 |                                     0 |                                -0.0007 |                               0.0001 |                                  -0.0001 |                                 250.96  |                                 0.0038 |                                     -0.0035 |                                0.0023 |                                -0.0185 |                               0.0056 |                                  -0.0056 |                                 136.168 |                                 0.0149 |                                     -0.0138 |                                0.0093 |                                -0.0506 |                               0.033  |                                  -0.0333 |                                 96.9339 |                                 0.0304 |                                     -0.0282 |                                0.0196 |                                -0.0803 |                               0.0895 |                                  -0.0907 |                                 76.8328 |                                 0.0475 |                                     -0.0438 |                                0.0315 |                                -0.1034 |                               0.174  |                                  -0.1768 |                                 64.4894 |                                 0.0644 |                                     -0.0593 |                                0.0439 |                                -0.1204 |                               0.2829 |                                  -0.288  |                                 56.0783 |                                 0.0807 |                                     -0.0741 |                                0.0563 |                                -0.1327 |                               0.4123 |                                  -0.4208 |                                 49.9447 |                                 0.096  |                                     -0.088  |                                0.0685 |                                -0.1415 |                               0.5593 |                                  -0.5719 |                                 45.2537 |                                 0.1102 |                                     -0.1008 |                                0.0804 |                                -0.1478 |                               0.7211 |                                  -0.7389 |                                 41.5368 |                                 0.1235 |                                     -0.1127 |                                0.0918 |                                -0.1522 |                               0.8957 |                                  -0.9195 |                                 38.5103 |                                 0.1357 |                                     -0.1237 |                                0.1029 |                                -0.1552 |                               1.0813 |                                  -1.1122 |                                 35.9922 |                                 0.1472 |                                     -0.1339 |                                0.1135 |                                -0.1573 |                               1.2766 |                                  -1.3154 |                                 33.8598 |                                 0.1578 |                                     -0.1433 |                                0.1237 |                                -0.1585 |                               1.4804 |                                  -1.5281 |                                 32.0276 |                                 0.1677 |                                     -0.1521 |                                0.1336 |                                -0.1592 |                               1.6917 |                                  -1.7492 |                                 30.4338 |                                 0.177  |                                     -0.1602 |                                0.1431 |                                -0.1594 |                               1.9098 |                                  -1.978  |                                 29.0328 |                                 0.1858 |                                     -0.1679 |                                0.1523 |                                -0.1593 |                               2.134  |                                  -2.2136 |                                 27.7901 |                                 0.1939 |                                     -0.175  |                                0.1612 |                                -0.1589 |                               2.3636 |                                  -2.4557 |                                 26.6792 |                                 0.2017 |                                     -0.1817 |                                0.1698 |                                -0.1583 |                               2.5982 |                                  -2.7035 |                                 25.679  |                                 0.2089 |                                     -0.188  |                                0.1782 |                                -0.1576 |                               2.8374 |                                  -2.9568 |                                 24.7732 |                                 0.2158 |                                     -0.1939 |                                0.1863 |                                -0.1568 |                               3.0808 |                                  -3.215  |                                 23.9482 |                                 0.2224 |                                     -0.1995 |                                0.1942 |                                -0.1558 |                               3.3279 |                                  -3.4779 |                                 23.1931 |                                 0.2286 |                                     -0.2047 |                                0.2019 |                                -0.1548 |                               3.5787 |                                  -3.7451 |                                 22.499  |                                 0.2345 |                                     -0.2097 |                                0.2094 |                                -0.1538 |                               3.8327 |                                  -4.0164 |                                 21.8583 |                                 0.2401 |                                     -0.2145 |                                0.2167 |                                -0.1527 |                               4.0897 |                                  -4.2916 |                                 21.2648 |                                 0.2454 |                                     -0.219  |                                0.2239 |                                -0.1516 |                               4.3497 |                                  -4.5703 |                                 20.7132 |                                 0.2506 |                                     -0.2233 |                                0.2308 |                                -0.1505 |                               4.6122 |                                  -4.8524 |                                 20.1989 |                                 0.2555 |                                     -0.2274 |                                0.2376 |                                -0.1494 |                               4.8773 |                                  -5.1378 |                                 19.7181 |                                 0.2602 |                                     -0.2313 |                                0.2443 |                                -0.1483 |                               5.1447 |                                  -5.4263 |                                 19.2673 |                                 0.2647 |                                     -0.235  |                                0.2508 |                                -0.1471 |                               5.4142 |                                  -5.7177 |                                 18.8438 |
|            295 |                                 0      |                                      0      |                                     0 |                                 0      |                               0      |                                   0      |                                 305.85  |                                 0.0004 |                                     -0.0003 |                                0.0003 |                                -0.0021 |                               0.0005 |                                  -0.0005 |                                 162.339 |                                 0.0029 |                                     -0.0027 |                                0.0022 |                                -0.0121 |                               0.0065 |                                  -0.0066 |                                113.802  |                                 0.0087 |                                     -0.0079 |                                0.0067 |                                -0.0275 |                               0.0256 |                                  -0.0259 |                                 89.1597 |                                 0.017  |                                     -0.0154 |                                0.0134 |                                -0.0439 |                               0.0624 |                                  -0.0633 |                                 74.1468 |                                 0.0268 |                                     -0.0243 |                                0.0216 |                                -0.0591 |                               0.118  |                                  -0.1199 |                                 63.9872 |                                 0.0374 |                                     -0.0339 |                                0.0307 |                                -0.0722 |                               0.1918 |                                  -0.1952 |                                 56.624  |                                 0.0484 |                                     -0.0437 |                                0.0404 |                                -0.0832 |                               0.2825 |                                  -0.2882 |                                 51.0232 |                                 0.0592 |                                     -0.0534 |                                0.0504 |                                -0.0923 |                               0.3886 |                                  -0.3972 |                                 46.6075 |                                 0.0699 |                                     -0.0629 |                                0.0604 |                                -0.0997 |                               0.5086 |                                  -0.5207 |                                 43.0281 |                                 0.0803 |                                     -0.0721 |                                0.0703 |                                -0.1058 |                               0.6411 |                                  -0.6576 |                                 40.0622 |                                 0.0902 |                                     -0.0809 |                                0.0802 |                                -0.1108 |                               0.7849 |                                  -0.8064 |                                 37.5601 |                                 0.0998 |                                     -0.0893 |                                0.0899 |                                -0.1148 |                               0.9388 |                                  -0.9661 |                                 35.4176 |                                 0.1089 |                                     -0.0974 |                                0.0994 |                                -0.118  |                               1.1019 |                                  -1.1357 |                                 33.56   |                                 0.1177 |                                     -0.105  |                                0.1087 |                                -0.1206 |                               1.2733 |                                  -1.3145 |                                 31.9321 |                                 0.126  |                                     -0.1123 |                                0.1178 |                                -0.1227 |                               1.4524 |                                  -1.5016 |                                 30.4922 |                                 0.134  |                                     -0.1192 |                                0.1267 |                                -0.1244 |                               1.6384 |                                  -1.6964 |                                 29.2084 |                                 0.1416 |                                     -0.1258 |                                0.1354 |                                -0.1257 |                               1.8307 |                                  -1.8984 |                                 28.0555 |                                 0.1489 |                                     -0.1321 |                                0.1439 |                                -0.1267 |                               2.029  |                                  -2.107  |                                 27.0137 |                                 0.1559 |                                     -0.1381 |                                0.1522 |                                -0.1275 |                               2.2327 |                                  -2.3218 |                                 26.067  |                                 0.1625 |                                     -0.1438 |                                0.1603 |                                -0.1281 |                               2.4414 |                                  -2.5423 |                                 25.2024 |                                 0.1689 |                                     -0.1493 |                                0.1682 |                                -0.1284 |                               2.6548 |                                  -2.7682 |                                 24.4092 |                                 0.1751 |                                     -0.1545 |                                0.176  |                                -0.1287 |                               2.8726 |                                  -2.9992 |                                 23.6785 |                                 0.181  |                                     -0.1595 |                                0.1835 |                                -0.1288 |                               3.0944 |                                  -3.235  |                                 23.0028 |                                 0.1866 |                                     -0.1643 |                                0.1909 |                                -0.1287 |                               3.32   |                                  -3.4753 |                                 22.3759 |                                 0.1921 |                                     -0.1689 |                                0.1982 |                                -0.1286 |                               3.5492 |                                  -3.7199 |                                 21.7924 |                                 0.1973 |                                     -0.1733 |                                0.2053 |                                -0.1285 |                               3.7817 |                                  -3.9685 |                                 21.2477 |                                 0.2024 |                                     -0.1775 |                                0.2123 |                                -0.1282 |                               4.0173 |                                  -4.2209 |                                 20.7378 |                                 0.2073 |                                     -0.1816 |                                0.2191 |                                -0.1279 |                               4.256  |                                  -4.477  |                                 20.2595 |
|            300 |                                 0      |                                      0      |                                     0 |                                 0      |                               0      |                                   0      |                                 361.004 |                                 0      |                                      0      |                                0      |                                -0.0002 |                               0      |                                   0      |                                 188.866 |                                 0.0004 |                                     -0.0004 |                                0.0004 |                                -0.0021 |                               0.001  |                                  -0.001  |                                130.973  |                                 0.002  |                                     -0.0018 |                                0.0018 |                                -0.0075 |                               0.006  |                                  -0.0061 |                                101.738  |                                 0.0052 |                                     -0.0046 |                                0.0048 |                                -0.0155 |                               0.0191 |                                  -0.0193 |                                 84.0149 |                                 0.0098 |                                     -0.0088 |                                0.0091 |                                -0.0249 |                               0.0432 |                                  -0.0438 |                                 72.0749 |                                 0.0156 |                                     -0.0139 |                                0.0147 |                                -0.0345 |                               0.0799 |                                  -0.0811 |                                 63.457  |                                 0.0222 |                                     -0.0197 |                                0.0213 |                                -0.0437 |                               0.1297 |                                  -0.132  |                                 56.9267 |                                 0.0293 |                                     -0.026  |                                0.0285 |                                -0.0521 |                               0.1926 |                                  -0.1964 |                                 51.7959 |                                 0.0368 |                                     -0.0326 |                                0.0362 |                                -0.0597 |                               0.268  |                                  -0.2738 |                                 47.6504 |                                 0.0444 |                                     -0.0393 |                                0.0442 |                                -0.0664 |                               0.3554 |                                  -0.3636 |                                 44.2256 |                                 0.052  |                                     -0.046  |                                0.0525 |                                -0.0723 |                               0.4539 |                                  -0.4652 |                                 41.3445 |                                 0.0597 |                                     -0.0527 |                                0.0609 |                                -0.0775 |                               0.5629 |                                  -0.5778 |                                 38.8839 |                                 0.0672 |                                     -0.0592 |                                0.0693 |                                -0.082  |                               0.6816 |                                  -0.7007 |                                 36.7558 |                                 0.0746 |                                     -0.0656 |                                0.0777 |                                -0.086  |                               0.8093 |                                  -0.8332 |                                 34.895  |                                 0.0818 |                                     -0.0719 |                                0.086  |                                -0.0894 |                               0.9455 |                                  -0.9748 |                                 33.2528 |                                 0.0888 |                                     -0.078  |                                0.0944 |                                -0.0924 |                               1.0894 |                                  -1.1248 |                                 31.7915 |                                 0.0957 |                                     -0.0839 |                                0.1026 |                                -0.0949 |                               1.2406 |                                  -1.2827 |                                 30.4819 |                                 0.1023 |                                     -0.0896 |                                0.1107 |                                -0.0972 |                               1.3986 |                                  -1.448  |                                 29.3006 |                                 0.1088 |                                     -0.0951 |                                0.1187 |                                -0.0991 |                               1.563  |                                  -1.6204 |                                 28.2291 |                                 0.115  |                                     -0.1004 |                                0.1266 |                                -0.1008 |                               1.7332 |                                  -1.7992 |                                 27.2521 |                                 0.1211 |                                     -0.1056 |                                0.1344 |                                -0.1022 |                               1.909  |                                  -1.9843 |                                 26.3573 |                                 0.127  |                                     -0.1106 |                                0.142  |                                -0.1035 |                               2.0901 |                                  -2.1753 |                                 25.5342 |                                 0.1327 |                                     -0.1154 |                                0.1496 |                                -0.1045 |                               2.276  |                                  -2.3717 |                                 24.7742 |                                 0.1382 |                                     -0.12   |                                0.157  |                                -0.1054 |                               2.4665 |                                  -2.5734 |                                 24.07   |                                 0.1436 |                                     -0.1245 |                                0.1643 |                                -0.1062 |                               2.6614 |                                  -2.7801 |                                 23.4155 |                                 0.1488 |                                     -0.1289 |                                0.1714 |                                -0.1069 |                               2.8604 |                                  -2.9916 |                                 22.8053 |                                 0.1538 |                                     -0.1331 |                                0.1785 |                                -0.1074 |                               3.0633 |                                  -3.2075 |                                 22.2349 |                                 0.1587 |                                     -0.1372 |                                0.1854 |                                -0.1078 |                               3.2698 |                                  -3.4278 |                                 21.7004 |
|            305 |                                 0      |                                      0      |                                     0 |                                 0      |                               0      |                                   0      |                                 416.007 |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                 215.505 |                                 0.0001 |                                      0      |                                0.0001 |                                -0.0003 |                               0.0001 |                                  -0.0001 |                                148.289  |                                 0.0004 |                                     -0.0003 |                                0.0004 |                                -0.0016 |                               0.0012 |                                  -0.0012 |                                114.455  |                                 0.0014 |                                     -0.0012 |                                0.0014 |                                -0.0046 |                               0.005  |                                  -0.005  |                                 94.0084 |                                 0.0032 |                                     -0.0028 |                                0.0033 |                                -0.0091 |                               0.0139 |                                  -0.0141 |                                 80.2749 |                                 0.0058 |                                     -0.0051 |                                0.0062 |                                -0.0146 |                               0.0299 |                                  -0.0303 |                                 70.3903 |                                 0.0092 |                                     -0.0081 |                                0.01   |                                -0.0206 |                               0.0542 |                                  -0.0551 |                                 62.92   |                                 0.0133 |                                     -0.0117 |                                0.0146 |                                -0.0267 |                               0.0879 |                                  -0.0895 |                                 57.0652 |                                 0.018  |                                     -0.0157 |                                0.0199 |                                -0.0327 |                               0.1313 |                                  -0.1338 |                                 52.3459 |                                 0.023  |                                     -0.0201 |                                0.0257 |                                -0.0385 |                               0.1844 |                                  -0.1883 |                                 48.4555 |                                 0.0283 |                                     -0.0247 |                                0.0319 |                                -0.0439 |                               0.2473 |                                  -0.2529 |                                 45.1895 |                                 0.0338 |                                     -0.0294 |                                0.0385 |                                -0.0489 |                               0.3195 |                                  -0.3273 |                                 42.4058 |                                 0.0394 |                                     -0.0343 |                                0.0453 |                                -0.0536 |                               0.4009 |                                  -0.4112 |                                 40.0026 |                                 0.0451 |                                     -0.0392 |                                0.0524 |                                -0.0578 |                               0.4909 |                                  -0.5042 |                                 37.9051 |                                 0.0509 |                                     -0.0441 |                                0.0595 |                                -0.0617 |                               0.5893 |                                  -0.6061 |                                 36.0571 |                                 0.0566 |                                     -0.049  |                                0.0667 |                                -0.0652 |                               0.6955 |                                  -0.7163 |                                 34.4153 |                                 0.0622 |                                     -0.0538 |                                0.074  |                                -0.0683 |                               0.8092 |                                  -0.8345 |                                 32.9461 |                                 0.0679 |                                     -0.0586 |                                0.0813 |                                -0.0712 |                               0.93   |                                  -0.9604 |                                 31.6229 |                                 0.0734 |                                     -0.0633 |                                0.0886 |                                -0.0738 |                               1.0576 |                                  -1.0935 |                                 30.4243 |                                 0.0789 |                                     -0.0679 |                                0.0959 |                                -0.0761 |                               1.1915 |                                  -1.2336 |                                 29.3329 |                                 0.0842 |                                     -0.0724 |                                0.1031 |                                -0.0783 |                               1.3315 |                                  -1.3802 |                                 28.3346 |                                 0.0895 |                                     -0.0769 |                                0.1103 |                                -0.0802 |                               1.4772 |                                  -1.5331 |                                 27.4174 |                                 0.0947 |                                     -0.0812 |                                0.1175 |                                -0.0819 |                               1.6283 |                                  -1.692  |                                 26.5716 |                                 0.0997 |                                     -0.0854 |                                0.1246 |                                -0.0834 |                               1.7846 |                                  -1.8566 |                                 25.7888 |                                 0.1047 |                                     -0.0896 |                                0.1316 |                                -0.0848 |                               1.9458 |                                  -2.0267 |                                 25.0619 |                                 0.1095 |                                     -0.0936 |                                0.1386 |                                -0.0861 |                               2.1117 |                                  -2.202  |                                 24.3851 |                                 0.1142 |                                     -0.0975 |                                0.1454 |                                -0.0872 |                               2.282  |                                  -2.3823 |                                 23.753  |                                 0.1189 |                                     -0.1014 |                                0.1522 |                                -0.0883 |                               2.4565 |                                  -2.5674 |                                 23.1612 |
|            310 |                                 0      |                                      0      |                                     0 |                                 0      |                               0      |                                   0      |                                 470.625 |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                 242.104 |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                165.639  |                                 0.0001 |                                     -0.0001 |                                0.0001 |                                -0.0003 |                               0.0002 |                                  -0.0002 |                                127.229  |                                 0.0003 |                                     -0.0003 |                                0.0004 |                                -0.0012 |                               0.0011 |                                  -0.0011 |                                104.064  |                                 0.0009 |                                     -0.0008 |                                0.0011 |                                -0.0029 |                               0.004  |                                  -0.004  |                                 88.5364 |                                 0.002  |                                     -0.0017 |                                0.0023 |                                -0.0055 |                               0.01   |                                  -0.0102 |                                 77.3824 |                                 0.0035 |                                     -0.003  |                                0.0043 |                                -0.0087 |                               0.0207 |                                  -0.021  |                                 68.9684 |                                 0.0056 |                                     -0.0048 |                                0.0068 |                                -0.0125 |                               0.037  |                                  -0.0377 |                                 62.3859 |                                 0.0082 |                                     -0.0071 |                                0.0101 |                                -0.0165 |                               0.0599 |                                  -0.0609 |                                 57.089  |                                 0.0112 |                                     -0.0096 |                                0.0139 |                                -0.0207 |                               0.0898 |                                  -0.0915 |                                 52.7297 |                                 0.0145 |                                     -0.0125 |                                0.0181 |                                -0.0249 |                               0.1271 |                                  -0.1297 |                                 49.0758 |                                 0.0182 |                                     -0.0156 |                                0.0229 |                                -0.029  |                               0.172  |                                  -0.1758 |                                 45.9661 |                                 0.022  |                                     -0.0189 |                                0.028  |                                -0.033  |                               0.2245 |                                  -0.2298 |                                 43.2852 |                                 0.0261 |                                     -0.0223 |                                0.0334 |                                -0.0368 |                               0.2845 |                                  -0.2916 |                                 40.9486 |                                 0.0303 |                                     -0.0259 |                                0.0391 |                                -0.0404 |                               0.352  |                                  -0.3613 |                                 38.8926 |                                 0.0346 |                                     -0.0296 |                                0.0449 |                                -0.0438 |                               0.4267 |                                  -0.4386 |                                 37.0683 |                                 0.039  |                                     -0.0333 |                                0.051  |                                -0.047  |                               0.5085 |                                  -0.5233 |                                 35.4378 |                                 0.0435 |                                     -0.037  |                                0.0572 |                                -0.05   |                               0.5971 |                                  -0.6152 |                                 33.971  |                                 0.0479 |                                     -0.0408 |                                0.0635 |                                -0.0527 |                               0.6923 |                                  -0.7142 |                                 32.6438 |                                 0.0524 |                                     -0.0445 |                                0.0698 |                                -0.0553 |                               0.7938 |                                  -0.8199 |                                 31.4367 |                                 0.0569 |                                     -0.0482 |                                0.0762 |                                -0.0577 |                               0.9014 |                                  -0.9321 |                                 30.3336 |                                 0.0613 |                                     -0.052  |                                0.0827 |                                -0.0599 |                               1.0149 |                                  -1.0507 |                                 29.3212 |                                 0.0657 |                                     -0.0556 |                                0.0892 |                                -0.062  |                               1.1339 |                                  -1.1753 |                                 28.3884 |                                 0.0701 |                                     -0.0593 |                                0.0957 |                                -0.0639 |                               1.2583 |                                  -1.3058 |                                 27.526  |                                 0.0745 |                                     -0.0629 |                                0.1021 |                                -0.0657 |                               1.3879 |                                  -1.4419 |                                 26.726  |                                 0.0787 |                                     -0.0664 |                                0.1086 |                                -0.0673 |                               1.5225 |                                  -1.5834 |                                 25.9816 |                                 0.083  |                                     -0.0699 |                                0.115  |                                -0.0688 |                               1.6618 |                                  -1.7302 |                                 25.287  |                                 0.0871 |                                     -0.0733 |                                0.1215 |                                -0.0702 |                               1.8057 |                                  -1.8821 |                                 24.6373 |
|            315 |                                 0      |                                      0      |                                     0 |                                 0      |                               0      |                                   0      |                                 524.724 |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                 268.562 |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                182.949  |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                140.001  |                                 0.0001 |                                     -0.0001 |                                0.0001 |                                -0.0003 |                               0.0002 |                                  -0.0002 |                                114.135  |                                 0.0002 |                                     -0.0002 |                                0.0003 |                                -0.0008 |                               0.001  |                                  -0.001  |                                 96.8211 |                                 0.0006 |                                     -0.0005 |                                0.0008 |                                -0.0018 |                               0.0031 |                                  -0.0031 |                                 84.4009 |                                 0.0012 |                                     -0.001  |                                0.0016 |                                -0.0034 |                               0.0072 |                                  -0.0073 |                                 75.0445 |                                 0.0022 |                                     -0.0019 |                                0.0029 |                                -0.0053 |                               0.0145 |                                  -0.0147 |                                 67.7343 |                                 0.0035 |                                     -0.003  |                                0.0047 |                                -0.0077 |                               0.0255 |                                  -0.0259 |                                 61.8593 |                                 0.0051 |                                     -0.0043 |                                0.0069 |                                -0.0104 |                               0.0411 |                                  -0.0418 |                                 57.0302 |                                 0.007  |                                     -0.006  |                                0.0097 |                                -0.0132 |                               0.0617 |                                  -0.0629 |                                 52.9872 |                                 0.0093 |                                     -0.0078 |                                0.0128 |                                -0.0162 |                               0.0879 |                                  -0.0897 |                                 49.5503 |                                 0.0117 |                                     -0.0099 |                                0.0163 |                                -0.0192 |                               0.1198 |                                  -0.1225 |                                 46.5907 |                                 0.0144 |                                     -0.0122 |                                0.0202 |                                -0.0222 |                               0.1578 |                                  -0.1614 |                                 44.0139 |                                 0.0173 |                                     -0.0146 |                                0.0244 |                                -0.0252 |                               0.2018 |                                  -0.2067 |                                 41.7487 |                                 0.0204 |                                     -0.0172 |                                0.0289 |                                -0.0281 |                               0.252  |                                  -0.2585 |                                 39.741  |                                 0.0236 |                                     -0.0198 |                                0.0336 |                                -0.0309 |                               0.3082 |                                  -0.3166 |                                 37.9482 |                                 0.0269 |                                     -0.0226 |                                0.0386 |                                -0.0336 |                               0.3706 |                                  -0.3811 |                                 36.3369 |                                 0.0303 |                                     -0.0254 |                                0.0437 |                                -0.0362 |                               0.4389 |                                  -0.4518 |                                 34.8802 |                                 0.0338 |                                     -0.0283 |                                0.049  |                                -0.0387 |                               0.513  |                                  -0.5288 |                                 33.5565 |                                 0.0373 |                                     -0.0312 |                                0.0544 |                                -0.0411 |                               0.5929 |                                  -0.6118 |                                 32.3479 |                                 0.0409 |                                     -0.0342 |                                0.0599 |                                -0.0433 |                               0.6783 |                                  -0.7007 |                                 31.2395 |                                 0.0445 |                                     -0.0371 |                                0.0655 |                                -0.0454 |                               0.7692 |                                  -0.7955 |                                 30.2192 |                                 0.0481 |                                     -0.0401 |                                0.0712 |                                -0.0474 |                               0.8653 |                                  -0.8959 |                                 29.2765 |                                 0.0517 |                                     -0.0431 |                                0.0769 |                                -0.0493 |                               0.9665 |                                  -1.0018 |                                 28.4026 |                                 0.0553 |                                     -0.046  |                                0.0827 |                                -0.0511 |                               1.0727 |                                  -1.1131 |                                 27.5901 |                                 0.059  |                                     -0.049  |                                0.0885 |                                -0.0528 |                               1.1837 |                                  -1.2296 |                                 26.8326 |                                 0.0626 |                                     -0.0519 |                                0.0943 |                                -0.0544 |                               1.2994 |                                  -1.3511 |                                 26.1244 |
|            320 |                                 0      |                                      0      |                                     0 |                                 0      |                               0      |                                   0      |                                 578.226 |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                 294.817 |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                200.169  |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                152.73   |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                124.187  |                                 0.0001 |                                      0      |                                0.0001 |                                -0.0002 |                               0.0002 |                                  -0.0002 |                                105.1    |                                 0.0002 |                                     -0.0001 |                                0.0002 |                                -0.0006 |                               0.0008 |                                  -0.0009 |                                 91.4214 |                                 0.0004 |                                     -0.0003 |                                0.0006 |                                -0.0012 |                               0.0023 |                                  -0.0024 |                                 81.1271 |                                 0.0008 |                                     -0.0007 |                                0.0012 |                                -0.0021 |                               0.0052 |                                  -0.0053 |                                 73.0919 |                                 0.0014 |                                     -0.0012 |                                0.002  |                                -0.0033 |                               0.0102 |                                  -0.0103 |                                 66.6404 |                                 0.0022 |                                     -0.0018 |                                0.0033 |                                -0.0049 |                               0.0177 |                                  -0.018  |                                 61.3423 |                                 0.0032 |                                     -0.0027 |                                0.0048 |                                -0.0066 |                               0.0284 |                                  -0.0289 |                                 56.9107 |                                 0.0045 |                                     -0.0037 |                                0.0067 |                                -0.0085 |                               0.0427 |                                  -0.0435 |                                 53.1468 |                                 0.006  |                                     -0.005  |                                0.009  |                                -0.0106 |                               0.0611 |                                  -0.0623 |                                 49.9084 |                                 0.0077 |                                     -0.0064 |                                0.0116 |                                -0.0128 |                               0.0838 |                                  -0.0856 |                                 47.0912 |                                 0.0095 |                                     -0.0079 |                                0.0146 |                                -0.015  |                               0.1112 |                                  -0.1137 |                                 44.6167 |                                 0.0116 |                                     -0.0096 |                                0.0178 |                                -0.0173 |                               0.1433 |                                  -0.1468 |                                 42.4251 |                                 0.0138 |                                     -0.0114 |                                0.0213 |                                -0.0195 |                               0.1804 |                                  -0.185  |                                 40.4697 |                                 0.0161 |                                     -0.0134 |                                0.025  |                                -0.0218 |                               0.2225 |                                  -0.2284 |                                 38.7135 |                                 0.0186 |                                     -0.0154 |                                0.029  |                                -0.024  |                               0.2697 |                                  -0.2771 |                                 37.1271 |                                 0.0212 |                                     -0.0175 |                                0.0331 |                                -0.0261 |                               0.3219 |                                  -0.3312 |                                 35.6864 |                                 0.0238 |                                     -0.0197 |                                0.0375 |                                -0.0283 |                               0.3792 |                                  -0.3905 |                                 34.3718 |                                 0.0266 |                                     -0.0219 |                                0.042  |                                -0.0303 |                               0.4414 |                                  -0.4552 |                                 33.1672 |                                 0.0294 |                                     -0.0242 |                                0.0466 |                                -0.0323 |                               0.5087 |                                  -0.525  |                                 32.0589 |                                 0.0322 |                                     -0.0265 |                                0.0514 |                                -0.0342 |                               0.5807 |                                  -0.6001 |                                 31.0356 |                                 0.0351 |                                     -0.0288 |                                0.0562 |                                -0.036  |                               0.6576 |                                  -0.6802 |                                 30.0876 |                                 0.0381 |                                     -0.0312 |                                0.0612 |                                -0.0378 |                               0.7392 |                                  -0.7654 |                                 29.2067 |                                 0.041  |                                     -0.0336 |                                0.0662 |                                -0.0394 |                               0.8253 |                                  -0.8555 |                                 28.3859 |                                 0.044  |                                     -0.036  |                                0.0713 |                                -0.041  |                               0.916  |                                  -0.9504 |                                 27.619  |
|            325 |                                 0      |                                      0      |                                     0 |                                 0      |                               0      |                                   0      |                                 631.087 |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                 320.826 |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                217.263  |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                165.387  |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                134.196  |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                113.352  |                                 0      |                                      0      |                                0.0001 |                                -0.0002 |                               0.0002 |                                  -0.0002 |                                 98.425  |                                 0.0001 |                                     -0.0001 |                                0.0002 |                                -0.0004 |                               0.0007 |                                  -0.0007 |                                 87.1996 |                                 0.0003 |                                     -0.0002 |                                0.0004 |                                -0.0008 |                               0.0018 |                                  -0.0018 |                                 78.4441 |                                 0.0005 |                                     -0.0004 |                                0.0008 |                                -0.0014 |                               0.0038 |                                  -0.0038 |                                 71.4193 |                                 0.0009 |                                     -0.0007 |                                0.0014 |                                -0.0021 |                               0.0072 |                                  -0.0073 |                                 65.6545 |                                 0.0014 |                                     -0.0012 |                                0.0023 |                                -0.0031 |                               0.0124 |                                  -0.0126 |                                 60.8359 |                                 0.0021 |                                     -0.0017 |                                0.0034 |                                -0.0043 |                               0.0198 |                                  -0.0201 |                                 56.7461 |                                 0.0029 |                                     -0.0024 |                                0.0047 |                                -0.0056 |                               0.0298 |                                  -0.0304 |                                 53.2297 |                                 0.0039 |                                     -0.0032 |                                0.0064 |                                -0.007  |                               0.0427 |                                  -0.0436 |                                 50.1726 |                                 0.0051 |                                     -0.0041 |                                0.0083 |                                -0.0086 |                               0.0589 |                                  -0.0602 |                                 47.4892 |                                 0.0064 |                                     -0.0052 |                                0.0105 |                                -0.0102 |                               0.0786 |                                  -0.0804 |                                 45.1141 |                                 0.0078 |                                     -0.0064 |                                0.0129 |                                -0.0119 |                               0.1021 |                                  -0.1045 |                                 42.9961 |                                 0.0094 |                                     -0.0077 |                                0.0156 |                                -0.0136 |                               0.1294 |                                  -0.1327 |                                 41.0952 |                                 0.0111 |                                     -0.009  |                                0.0185 |                                -0.0153 |                               0.1608 |                                  -0.165  |                                 39.379  |                                 0.0129 |                                     -0.0105 |                                0.0217 |                                -0.0171 |                               0.1963 |                                  -0.2016 |                                 37.8213 |                                 0.0148 |                                     -0.012  |                                0.025  |                                -0.0188 |                               0.236  |                                  -0.2427 |                                 36.4008 |                                 0.0168 |                                     -0.0137 |                                0.0285 |                                -0.0205 |                               0.28   |                                  -0.2882 |                                 35.0998 |                                 0.0189 |                                     -0.0154 |                                0.0322 |                                -0.0223 |                               0.3282 |                                  -0.3382 |                                 33.9035 |                                 0.0211 |                                     -0.0171 |                                0.036  |                                -0.0239 |                               0.3807 |                                  -0.3927 |                                 32.7995 |                                 0.0233 |                                     -0.0189 |                                0.04   |                                -0.0256 |                               0.4375 |                                  -0.4517 |                                 31.7773 |                                 0.0256 |                                     -0.0207 |                                0.0441 |                                -0.0272 |                               0.4985 |                                  -0.5152 |                                 30.8279 |                                 0.028  |                                     -0.0226 |                                0.0483 |                                -0.0287 |                               0.5637 |                                  -0.5832 |                                 29.9436 |                                 0.0303 |                                     -0.0245 |                                0.0526 |                                -0.0302 |                               0.633  |                                  -0.6555 |                                 29.1178 |
|            330 |                                 0      |                                      0      |                                     0 |                                 0      |                               0      |                                   0      |                                 683.285 |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                 346.564 |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                234.207  |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                177.951  |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                144.141  |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                121.56   |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                105.397  |                                 0      |                                      0      |                                0.0001 |                                -0.0001 |                               0.0002 |                                  -0.0002 |                                 93.2495 |                                 0.0001 |                                     -0.0001 |                                0.0001 |                                -0.0003 |                               0.0006 |                                  -0.0006 |                                 83.7795 |                                 0.0002 |                                     -0.0001 |                                0.0003 |                                -0.0005 |                               0.0013 |                                  -0.0014 |                                 76.1857 |                                 0.0003 |                                     -0.0003 |                                0.0006 |                                -0.0009 |                               0.0028 |                                  -0.0028 |                                 69.9574 |                                 0.0006 |                                     -0.0005 |                                0.001  |                                -0.0014 |                               0.0051 |                                  -0.0052 |                                 64.7543 |                                 0.0009 |                                     -0.0007 |                                0.0016 |                                -0.002  |                               0.0087 |                                  -0.0089 |                                 60.3405 |                                 0.0014 |                                     -0.0011 |                                0.0024 |                                -0.0028 |                               0.0139 |                                  -0.0142 |                                 56.5474 |                                 0.0019 |                                     -0.0015 |                                0.0034 |                                -0.0037 |                               0.0209 |                                  -0.0213 |                                 53.2516 |                                 0.0026 |                                     -0.0021 |                                0.0045 |                                -0.0047 |                               0.0301 |                                  -0.0307 |                                 50.3602 |                                 0.0034 |                                     -0.0027 |                                0.0059 |                                -0.0058 |                               0.0417 |                                  -0.0426 |                                 47.8021 |                                 0.0043 |                                     -0.0034 |                                0.0076 |                                -0.0069 |                               0.0559 |                                  -0.0572 |                                 45.5223 |                                 0.0053 |                                     -0.0042 |                                0.0094 |                                -0.0082 |                               0.073  |                                  -0.0747 |                                 43.477  |                                 0.0064 |                                     -0.0052 |                                0.0115 |                                -0.0095 |                               0.0931 |                                  -0.0954 |                                 41.6313 |                                 0.0076 |                                     -0.0061 |                                0.0137 |                                -0.0108 |                               0.1165 |                                  -0.1195 |                                 39.957  |                                 0.009  |                                     -0.0072 |                                0.0162 |                                -0.0122 |                               0.1431 |                                  -0.147  |                                 38.4308 |                                 0.0104 |                                     -0.0083 |                                0.0188 |                                -0.0135 |                               0.1732 |                                  -0.178  |                                 37.0335 |                                 0.0119 |                                     -0.0095 |                                0.0216 |                                -0.0149 |                               0.2068 |                                  -0.2128 |                                 35.7493 |                                 0.0135 |                                     -0.0108 |                                0.0246 |                                -0.0163 |                               0.244  |                                  -0.2513 |                                 34.5647 |                                 0.0152 |                                     -0.0121 |                                0.0277 |                                -0.0177 |                               0.2848 |                                  -0.2936 |                                 33.4684 |                                 0.0169 |                                     -0.0135 |                                0.031  |                                -0.0191 |                               0.3292 |                                  -0.3397 |                                 32.4505 |                                 0.0187 |                                     -0.0149 |                                0.0344 |                                -0.0204 |                               0.3774 |                                  -0.3897 |                                 31.5029 |                                 0.0205 |                                     -0.0164 |                                0.0379 |                                -0.0218 |                               0.4291 |                                  -0.4436 |                                 30.6183 |
|            335 |                                 0      |                                      0      |                                     0 |                                 0      |                               0      |                                   0      |                                 734.808 |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                 372.013 |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                250.985  |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                190.406  |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                154.011  |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                129.713  |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                112.328  |                                 0      |                                      0      |                                0      |                                 0      |                               0      |                                   0      |                                 99.2668 |                                 0      |                                      0      |                                0      |                                -0.0001 |                               0.0002 |                                  -0.0002 |                                 89.0894 |                                 0.0001 |                                      0      |                                0.0001 |                                -0.0002 |                               0.0004 |                                  -0.0004 |                                 80.9316 |                                 0.0001 |                                     -0.0001 |                                0.0002 |                                -0.0003 |                               0.001  |                                  -0.001  |                                 74.2438 |                                 0.0002 |                                     -0.0002 |                                0.0004 |                                -0.0006 |                               0.002  |                                  -0.0021 |                                 68.6591 |                                 0.0004 |                                     -0.0003 |                                0.0007 |                                -0.0009 |                               0.0037 |                                  -0.0038 |                                 63.9236 |                                 0.0006 |                                     -0.0005 |                                0.0011 |                                -0.0013 |                               0.0062 |                                  -0.0063 |                                 59.8559 |                                 0.0009 |                                     -0.0007 |                                0.0017 |                                -0.0018 |                               0.0099 |                                  -0.0101 |                                 56.3229 |                                 0.0013 |                                     -0.001  |                                0.0024 |                                -0.0024 |                               0.0148 |                                  -0.0151 |                                 53.2246 |                                 0.0017 |                                     -0.0014 |                                0.0032 |                                -0.0031 |                               0.0214 |                                  -0.0218 |                                 50.4847 |                                 0.0023 |                                     -0.0018 |                                0.0043 |                                -0.0039 |                               0.0297 |                                  -0.0303 |                                 48.0438 |                                 0.0029 |                                     -0.0023 |                                0.0055 |                                -0.0048 |                               0.04   |                                  -0.0409 |                                 45.8549 |                                 0.0036 |                                     -0.0029 |                                0.0069 |                                -0.0057 |                               0.0525 |                                  -0.0537 |                                 43.8804 |                                 0.0044 |                                     -0.0035 |                                0.0084 |                                -0.0066 |                               0.0673 |                                  -0.0689 |                                 42.0898 |                                 0.0053 |                                     -0.0042 |                                0.0102 |                                -0.0076 |                               0.0846 |                                  -0.0868 |                                 40.4583 |                                 0.0063 |                                     -0.005  |                                0.0121 |                                -0.0087 |                               0.1046 |                                  -0.1074 |                                 38.9653 |                                 0.0073 |                                     -0.0058 |                                0.0141 |                                -0.0097 |                               0.1274 |                                  -0.1309 |                                 37.5935 |                                 0.0084 |                                     -0.0067 |                                0.0164 |                                -0.0108 |                               0.153  |                                  -0.1573 |                                 36.3286 |                                 0.0096 |                                     -0.0076 |                                0.0187 |                                -0.0119 |                               0.1816 |                                  -0.1869 |                                 35.1582 |                                 0.0109 |                                     -0.0086 |                                0.0213 |                                -0.0131 |                               0.2131 |                                  -0.2196 |                                 34.0721 |                                 0.0123 |                                     -0.0096 |                                0.0239 |                                -0.0142 |                               0.2478 |                                  -0.2555 |                                 33.0613 |                                 0.0136 |                                     -0.0107 |                                0.0267 |                                -0.0153 |                               0.2856 |                                  -0.2948 |                                 32.118  |

---

## get_delta
Calculate the delta of an option based on the Black Scholes Model: how much the option value changes for a 1.00 change in the price of the underlying asset.

The Black Scholes Model is a mathematical model used to estimate the price of European-style options. The delta is the rate of change of the option price with respect to the price of the underlying asset.

The delta calculation is the theoretical value of the delta. The actual delta can differ from this value due to several factors such as the volatility of the underlying asset, the time to expiration, the risk free rate and more.

The formula is as follows:

$$
d_{1} = \frac{\ln\left(\frac{S}{K}\right) + \left(r - q + \frac{\sigma^{2}}{2}\right) \cdot t}{\sigma \cdot \sqrt{t}}
$$

$$
\text{Call Option Delta} = e^{- q \cdot t} \cdot N(d_{1})
$$

$$
\text{Put Option Delta} = - e^{- q \cdot t} \cdot N(- d_{1})
$$

Where S is the stock price, K is the strike price, r is the risk free rate, q is the dividend yield, $$\sigma$$ is the volatility, t is the time to expiration, N(d1) is the cumulative normal distribution of d1 and N(d2) is the the cumulative normal distribution of d2.

The Delta can be interpreted as follows:

- For call options, Delta is positive, indicating that the option price tends to move in the same direction as the underlying asset's price.
- For put options, Delta is negative, indicating that the option price tends to move in the opposite direction to the underlying asset's price.

Note that the delta of a call option is always between 0 and $$e^{- q \cdot t}$$, while the delta of a put option is always between $$- e^{- q \cdot t}$$ and 0. Without a dividend yield those bounds collapse to the familiar 0 to 1 and -1 to 0.

Delta is read as the hedge ratio: a call with a delta of 0.6 moves about $0.60 for a $1 move in the stock, so a market maker that is short calls on 100 shares buys 60 shares to stay neutral. It is often used as a quick gauge of how far in or out of the money an option is (traders talk of "25-delta" puts), and loosely as the chance of finishing in the money, although that (risk-neutral) probability is N(d2), which `get_dual_delta` gives up to discounting and sign. Delta changes with the stock price and with time (see gamma and charm), so a delta hedge has to be rebalanced.

**Also known as:** option price sensitivity to underlying, hedge ratio.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None, which
uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>put_option (bool, optional):</u> Whether to calculate the put option delta. Defaults to False which means
it will calculate the call option delta.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: the delta values containing the tickers and strike prices as the index and the
time to expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.options.get_delta(
    strike_price_range=0.15, strike_step_size=5, expiration_time_range=91
).loc["AMZN", ["2026-01-30", "2026-03-01", "2026-03-31"]]
```

Which returns:

|   Strike Price |   2026-01-30 |   2026-03-01 |   2026-03-31 |
|---------------:|-------------:|-------------:|-------------:|
|            195 |       0.9632 |       0.9073 |       0.8707 |
|            200 |       0.9374 |       0.8735 |       0.8369 |
|            205 |       0.9003 |       0.8331 |       0.7989 |
|            210 |       0.8508 |       0.7865 |       0.7571 |
|            215 |       0.7886 |       0.7344 |       0.7121 |
|            220 |       0.7154 |       0.6778 |       0.6647 |
|            225 |       0.6338 |       0.6183 |       0.6156 |
|            230 |       0.5476 |       0.5572 |       0.5658 |
|            235 |       0.461  |       0.496  |       0.516  |
|            240 |       0.378  |       0.4362 |       0.467  |
|            245 |       0.3018 |       0.379  |       0.4195 |
|            250 |       0.2346 |       0.3254 |       0.374  |
|            255 |       0.1778 |       0.2762 |       0.3311 |
|            260 |       0.1313 |       0.2318 |       0.2911 |

---

## get_dual_delta
Calculate the dual delta of an option based on the Black Scholes Model: how much the option value changes for a 1.00 change in the strike price.

The Black Scholes Model is a mathematical model used to estimate the price of European-style options. The dual delta is the first derivative of the option price with respect to the strike price; up to the discount factor and its sign it is the risk-neutral probability of the option finishing in the money.

The dual delta calculation is the theoretical value of the dual delta. The actual dual delta can differ from this value due to several factors such as the volatility of the underlying asset, the time to expiration, the risk free rate and more.

The formula is as follows:

$$
d_{1} = \frac{\ln\left(\frac{S}{K}\right) + \left(r - q + \frac{\sigma^{2}}{2}\right) \cdot t}{\sigma \cdot \sqrt{t}}
$$

$$
d_{2} = d_{1} - \sigma \cdot \sqrt{t}
$$

$$
\text{Call Dual Delta} = - e^{- r \cdot t} \cdot N(d_{2})
$$

$$
\text{Put Dual Delta} = e^{- r \cdot t} \cdot N(- d_{2})
$$

Where S is the stock price, K is the strike price, r is the risk free rate, q is the dividend yield, $$\sigma$$ is the volatility, t is the time to expiration, N(d1) is the cumulative normal distribution of d1 and N(d2) is the the cumulative normal distribution of d2.

The Dual Delta is the sensitivity of the option value to the strike price rather than to the underlying price. Up to the discount factor and a sign it is the risk-neutral probability that the option finishes in the money: a call Dual Delta of -0.5 corresponds to a roughly 50% chance of finishing in the money. It is negative for a call, since raising the strike lowers the call's value, and positive for a put.

**Also known as:** strike delta, binary option delta.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None, which
uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>put_option (bool, optional):</u> Whether to calculate the put option dual delta. Defaults to False which means
it will calculate the call option dual delta.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: the dual delta values containing the tickers and strike prices as the index and the
time to expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["JPM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.options.get_dual_delta(
    strike_price_range=0.15, strike_step_size=5, expiration_time_range=91
).loc["JPM", ["2026-01-30", "2026-03-01", "2026-03-31"]]
```

Which returns:

|   Strike Price |   2026-01-30 |   2026-03-01 |   2026-03-31 |
|---------------:|-------------:|-------------:|-------------:|
|            275 |      -0.9832 |      -0.9341 |      -0.8885 |
|            280 |      -0.9717 |      -0.91   |      -0.8603 |
|            285 |      -0.9533 |      -0.8798 |      -0.8278 |
|            290 |      -0.9258 |      -0.8433 |      -0.791  |
|            295 |      -0.8873 |      -0.8005 |      -0.7504 |
|            300 |      -0.8368 |      -0.7518 |      -0.7065 |
|            305 |      -0.7742 |      -0.6982 |      -0.6598 |
|            310 |      -0.7008 |      -0.6406 |      -0.6113 |
|            315 |      -0.6194 |      -0.5805 |      -0.5616 |
|            320 |      -0.5336 |      -0.5193 |      -0.5116 |
|            325 |      -0.4474 |      -0.4585 |      -0.4621 |
|            330 |      -0.3649 |      -0.3995 |      -0.4139 |
|            335 |      -0.2892 |      -0.3435 |      -0.3676 |
|            340 |      -0.2228 |      -0.2915 |      -0.3237 |
|            345 |      -0.1667 |      -0.2441 |      -0.2827 |
|            350 |      -0.1213 |      -0.2018 |      -0.2449 |
|            355 |      -0.0858 |      -0.1647 |      -0.2105 |
|            360 |      -0.0591 |      -0.1327 |      -0.1795 |
|            365 |      -0.0396 |      -0.1057 |      -0.1518 |

---

## get_vega
Calculate the vega of an option based on the Black Scholes Model: how much the option value changes for a 1.00 change in the volatility of the underlying asset.

The Black Scholes Model is a mathematical model used to estimate the price of European-style options. The vega is the rate of change of the option price with respect to the volatility of the underlying asset.

The vega calculation is the theoretical value of the vega. The actual vega can differ from this value due to several factors such as the volatility of the underlying asset, the time to expiration, the risk free rate and more.

The formula is as follows:

$$
d_{1} = \frac{\ln\left(\frac{S}{K}\right) + \left(r - q + \frac{\sigma^{2}}{2}\right) \cdot t}{\sigma \cdot \sqrt{t}}
$$

$$
\text{Vega} = \frac{S \cdot e^{- q \cdot t} \cdot N'(d_{1}) \cdot \sqrt{t}}{100}
$$

Where S is the stock price, K is the strike price, r is the risk free rate, q is the dividend yield, $$\sigma$$ is the volatility, t is the time to expiration, N'(d1) is the standard normal probability density at d1 and N(d2) is the cumulative normal distribution of d2.

The division by 100 expresses Vega per 1 percentage point change in volatility, the usual market quote. The higher order volatility Greeks (Vanna, Vomma, Zomma, Vera, Ultima) are reported unscaled, per 1.00 of volatility; only Vega and Veta carry this factor.

The Vega can be interpreted as follows:

- If Vega is positive, it indicates that the option value will increase as the volatility increases, and vice versa.
- If Vega is negative, it implies that the option value will decrease as the volatility increases, and vice versa.

Note that the vega of a call option and put option are equal to each other.

Vega is quoted per volatility point: a vega of 0.25 means the option gains about $0.25 when volatility rises from 20% to 21%. It is largest for at-the-money options and grows with the square root of the time to expiry, so long-dated options are mostly a bet on volatility while short-dated ones are mostly a bet on gamma. Desks sum vega across positions per expiry, since short- and long-dated implied volatilities rarely move by the same amount.

**Also known as:** option sensitivity to volatility changes.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None, which
uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: the vega values containing the tickers and strike prices as the index and the
time to expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NFLX"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.options.get_vega(
    strike_price_range=0.15, strike_step_size=2, expiration_time_range=91
).loc["NFLX", ["2026-01-30", "2026-03-01", "2026-03-31"]]
```

Which returns:

|   Strike Price |   2026-01-30 |   2026-03-01 |   2026-03-31 |
|---------------:|-------------:|-------------:|-------------:|
|             80 |       0.0248 |       0.0678 |       0.1032 |
|             82 |       0.037  |       0.0837 |       0.1196 |
|             84 |       0.0515 |       0.0998 |       0.1354 |
|             86 |       0.067  |       0.1149 |       0.1498 |
|             88 |       0.0819 |       0.1283 |       0.1623 |
|             90 |       0.0945 |       0.1392 |       0.1723 |
|             92 |       0.1032 |       0.1468 |       0.1797 |
|             94 |       0.1071 |       0.1509 |       0.1842 |
|             96 |       0.1059 |       0.1514 |       0.1857 |
|             98 |       0.1001 |       0.1486 |       0.1845 |
|            100 |       0.0908 |       0.1427 |       0.1806 |
|            102 |       0.0791 |       0.1343 |       0.1744 |
|            104 |       0.0664 |       0.1241 |       0.1664 |
|            106 |       0.0538 |       0.1126 |       0.1568 |

---

## get_theta
Calculate the theta of an option based on the Black Scholes Model: how much the option value changes as time passes, its time decay.

The Black Scholes Model is a mathematical model used to estimate the price of European-style options. The theta is the rate of change of the option price with respect to the passage of time.

The theta calculation is the theoretical value of the theta. The actual theta can differ from this value due to several factors such as the volatility of the underlying asset, the time to expiration, the risk free rate and more.

The formula is as follows:

$$
d_{1} = \frac{\ln\left(\frac{S}{K}\right) + \left(r - q + \frac{\sigma^{2}}{2}\right) \cdot t}{\sigma \cdot \sqrt{t}}
$$

$$
d_{2} = d_{1} - \sigma \cdot \sqrt{t}
$$

$$
\text{Call Theta} = \frac{- \frac{e^{- q \cdot t} \cdot (S \cdot N'(d_{1}) \cdot \sigma)}{2 \cdot \sqrt{t}} - r \cdot K \cdot e^{- r \cdot t} \cdot N(d_{2}) + q \cdot S \cdot e^{- q \cdot t} \cdot N(d_{1})}{365}
$$

$$
\text{Put Theta} = \frac{- \frac{e^{- q \cdot t} \cdot (S \cdot N'(d_{1}) \cdot \sigma)}{2 \cdot \sqrt{t}} + r \cdot K \cdot e^{- r \cdot t} \cdot N(- d_{2}) - q \cdot S \cdot e^{- q \cdot t} \cdot N(- d_{1})}{365}
$$

Where S is the stock price, K is the strike price, r is the risk free rate, q is the dividend yield, $$\sigma$$ is the volatility, t is the time to expiration, N'(d1) is the standard normal probability density at d1 and N(d2) is the cumulative normal distribution of d2.

Theta is the derivative with respect to calendar time elapsed, not with respect to the remaining time to maturity, and the division by 365 expresses it per calendar day rather than per year. Charm, Veta and Color measure the same passage of time in the same direction.

The Theta can be interpreted as follows:

- If Theta is negative, the option loses value with each day that passes, all else equal. This is the normal case for a long option, whose time value erodes towards expiration.
- If Theta is positive, the option gains value with each day that passes. This happens for instance on a deep in-the-money European put, where the discounting of the strike dominates.

Theta is the cost of holding an option for one more calendar day, all else equal, and is the other side of gamma: a long at-the-money option close to expiry has the most gamma and pays for it with the most negative theta. Because it is per calendar day, a weekend counts as two days of decay; desks that use a trading-day convention divide the yearly figure by 252 instead, which gives a larger daily number.

**Also known as:** time decay, option time value erosion.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None, which
uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>put_option (bool, optional):</u> Whether to calculate the put option theta. Defaults to False which means
it will calculate the call option theta.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: the theta values containing the tickers and strike prices as the index and the
time to expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AVGO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.options.get_theta(
    strike_price_range=0.15, strike_step_size=10
).loc["AVGO", ["2026-01-07", "2026-01-14", "2026-01-28"]]
```

Which returns:

|   Strike Price |   2026-01-07 |   2026-01-14 |   2026-01-28 |
|---------------:|-------------:|-------------:|-------------:|
|            290 |      -0.0622 |      -0.1333 |      -0.18   |
|            300 |      -0.1273 |      -0.2073 |      -0.2285 |
|            310 |      -0.2475 |      -0.2972 |      -0.2762 |
|            320 |      -0.4168 |      -0.3897 |      -0.3185 |
|            330 |      -0.5935 |      -0.4679 |      -0.3511 |
|            340 |      -0.7151 |      -0.5166 |      -0.3711 |
|            350 |      -0.7359 |      -0.5271 |      -0.3771 |
|            360 |      -0.6538 |      -0.5    |      -0.3696 |
|            370 |      -0.5072 |      -0.4432 |      -0.3502 |
|            380 |      -0.347  |      -0.3691 |      -0.3217 |
|            390 |      -0.2115 |      -0.2901 |      -0.2871 |

---

## get_rho
Calculate the rho of an option based on the Black Scholes Model: how much the option value changes for a 1.00 change in the risk free rate.

The Black Scholes Model is a mathematical model used to estimate the price of European-style options. The rho is the rate of change of the option price with respect to the risk free interest rate.

The rho calculation is the theoretical value of the rho. The actual rho can differ from this value due to several factors such as the volatility of the underlying asset, the time to expiration, the risk free rate and more.

The formula is as follows:

$$
d_{1} = \frac{\ln\left(\frac{S}{K}\right) + \left(r - q + \frac{\sigma^{2}}{2}\right) \cdot t}{\sigma \cdot \sqrt{t}}
$$

$$
d_{2} = d_{1} - \sigma \cdot \sqrt{t}
$$

$$
\text{Call Rho} = K \cdot t \cdot e^{- r \cdot t} \cdot N(d_{2})
$$

$$
\text{Put Rho} = - K \cdot t \cdot e^{- r \cdot t} \cdot N(- d_{2})
$$

Where S is the stock price, K is the strike price, r is the risk free rate, q is the dividend yield, $$\sigma$$ is the volatility, t is the time to expiration, N(d1) is the cumulative normal distribution of d1 and N(d2) is the the cumulative normal distribution of d2.

The Rho can be interpreted as follows:

- If Rho is positive, it indicates that the option value will increase as the risk free rate increases, and vice versa.
- If Rho is negative, it implies that the option value will decrease as the risk free rate increases, and vice versa.

Rho is reported unscaled, as the amount of money per share of the underlying that the value of the option gains or loses per 1.00 change in the risk-free rate. Divide by 100 for the more commonly quoted move per 1.0% per annum (100 basis points). Epsilon and Vera follow the same unscaled convention, while Vega and Veta are already divided by 100.

**Also known as:** option sensitivity to interest rate.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None, which
uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>put_option (bool, optional):</u> Whether to calculate the put option rho. Defaults to False which means
it will calculate the call option rho.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: the rho values containing the tickers and strike prices as the index and the
time to expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["PG"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.options.get_rho(
    strike_price_range=0.15, strike_step_size=5, expiration_time_range=181
).loc["PG", ["2026-01-30", "2026-03-31", "2026-06-29"]]
```

Which returns:

|   Strike Price |   2026-01-30 |   2026-03-31 |   2026-06-29 |
|---------------:|-------------:|-------------:|-------------:|
|            120 |       9.8242 |      28.3968 |      52.5187 |
|            125 |      10.1774 |      28.2215 |      50.9318 |
|            130 |      10.2553 |      26.8656 |      47.8678 |
|            135 |       9.5388 |      24.1422 |      43.4471 |
|            140 |       7.6094 |      20.2487 |      38.0035 |
|            145 |       4.885  |      15.739  |      32.0077 |
|            150 |       2.4331 |      11.3016 |      25.96   |
|            155 |       0.9288 |       7.4961 |      20.293  |
|            160 |       0.2726 |       4.6014 |      15.3096 |

---

## get_epsilon
Calculate the epsilon of an option based on the Black Scholes Model: how much the option value changes for a 1.00 change in the dividend yield.

The Black Scholes Model is a mathematical model used to estimate the price of European-style options. The epsilon is the rate of change of the option price with respect to the dividend yield.

The epsilon calculation is the theoretical value of the epsilon. The actual epsilon can differ from this value due to several factors such as the volatility of the underlying asset, the time to expiration, the risk free rate and more.

The formula is as follows:

$$
d_{1} = \frac{\ln\left(\frac{S}{K}\right) + \left(r - q + \frac{\sigma^{2}}{2}\right) \cdot t}{\sigma \cdot \sqrt{t}}
$$

$$
\text{Call Epsilon} = - S \cdot t \cdot e^{- q \cdot t} \cdot N(d_{1})
$$

$$
\text{Put Epsilon} = S \cdot t \cdot e^{- q \cdot t} \cdot N(- d_{1})
$$

Where S is the stock price, K is the strike price, r is the risk free rate, q is the dividend yield, $$\sigma$$ is the volatility, t is the time to expiration, N(d1) is the cumulative normal distribution of d1 and N(d2) is the the cumulative normal distribution of d2.

Epsilon is reported unscaled, per 1.00 change in the dividend yield, matching Rho and Vera.

The Epsilon can be interpreted as follows:

- If Epsilon is positive, it indicates that the option value will increase as the dividend yield increases, and vice versa.
- If Epsilon is negative, it implies that the option value will decrease as the dividend yield increases, and vice versa.

**Also known as:** option sensitivity to dividend yield.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None, which
uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>put_option (bool, optional):</u> Whether to calculate the put option epsilon. Defaults to False which means
it will calculate the call option epsilon.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: the epsilon values containing the tickers and strike prices as the index and the
time to expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["KO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.options.get_epsilon(
    strike_price_range=0.15, strike_step_size=2, expiration_time_range=181
).loc["KO", ["2026-01-30", "2026-03-31", "2026-06-29"]]
```

Which returns:

|   Strike Price |   2026-01-30 |   2026-03-31 |   2026-06-29 |
|---------------:|-------------:|-------------:|-------------:|
|             60 |      -5.7266 |     -16.5449 |     -30.9929 |
|             62 |      -5.6895 |     -15.8742 |     -29.2736 |
|             64 |      -5.5271 |     -14.7661 |     -27.0636 |
|             66 |      -5.0612 |     -13.1819 |     -24.4224 |
|             68 |      -4.153  |     -11.1972 |     -21.4687 |
|             70 |      -2.9116 |      -8.9943 |     -18.3604 |
|             72 |      -1.6884 |      -6.8063 |     -15.2669 |
|             74 |      -0.7967 |      -4.8441 |     -12.3419 |
|             76 |      -0.3046 |      -3.2422 |      -9.7037 |
|             78 |      -0.0947 |      -2.043  |      -7.425  |

---

## get_lambda
Calculate the lambda of an option based on the Black Scholes Model: the percentage change in the option value per percentage change in the price of the underlying asset, the leverage the option gives.

The Black Scholes Model is a mathematical model used to estimate the price of European-style options. The lambda, or elasticity, is the percentage change in the option price for a 1% change in the price of the underlying asset, i.e. the leverage the option gives.

The lambda calculation is the theoretical value of the lambda. The actual lambda can differ from this value due to several factors such as the volatility of the underlying asset, the time to expiration, the risk free rate and more.

The formula is as follows:

$$
d_{1} = \frac{\ln\left(\frac{S}{K}\right) + \left(r - q + \frac{\sigma^{2}}{2}\right) \cdot t}{\sigma \cdot \sqrt{t}}
$$

$$
d_{2} = d_{1} - \sigma \cdot \sqrt{t}
$$

$$
\text{Call Delta} = e^{- q \cdot t} \cdot N(d_{1}),\;\; \text{Put Delta} = - e^{- q \cdot t} \cdot N(- d_{1})
$$

$$
\text{Call Option Price} = S \cdot e^{- q \cdot t} \cdot N(d_{1}) - K \cdot e^{- r \cdot t} \cdot N(d_{2})
$$

$$
\text{Put Option Price} = K \cdot e^{- r \cdot t} \cdot N(- d_{2}) - S \cdot e^{- q \cdot t} \cdot N(- d_{1})
$$

$$
\Lambda = \Delta \cdot \frac{\text{Stock Price}}{\text{Call Option Price or Put Option Price}}
$$

Where S is the stock price, K is the strike price, r is the risk free rate, q is the dividend yield, $$\sigma$$ is the volatility, t is the time to expiration, N(d1) is the cumulative normal distribution of d1 and N(d2) is the the cumulative normal distribution of d2.

The Lambda can be interpreted as follows:

- If Lambda is positive, it indicates that the option value will increase as the underlying price increases, and vice versa.
- If Lambda is negative, it implies that the option value will decrease as the underlying price increases, and vice versa.

**Also known as:** option elasticity, leverage factor.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None, which
uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>put_option (bool, optional):</u> Whether to calculate the put option lambda. Defaults to False which means
it will calculate the call option lambda.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: the lambda values containing the tickers and strike prices as the index and the
time to expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["V"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.options.get_lambda(
    strike_price_range=0.1, strike_step_size=5, expiration_time_range=91
).loc["V", ["2026-01-30", "2026-03-01", "2026-03-31"]]
```

Which returns:

|   Strike Price |   2026-01-30 |   2026-03-01 |   2026-03-31 |
|---------------:|-------------:|-------------:|-------------:|
|            315 |       9.0902 |       8.0791 |       7.3278 |
|            320 |      10.1194 |       8.7387 |       7.8119 |
|            325 |      11.2886 |       9.4486 |       8.322  |
|            330 |      12.601  |      10.2075 |       8.857  |
|            335 |      14.0561 |      11.0131 |       9.4157 |
|            340 |      15.6492 |      11.8631 |       9.9965 |
|            345 |      17.3729 |      12.7543 |      10.5978 |
|            350 |      19.2169 |      13.6837 |      11.2182 |
|            355 |      21.1699 |      14.6477 |      11.8559 |
|            360 |      23.2196 |      15.6431 |      12.5094 |
|            365 |      25.3536 |      16.6664 |      13.177  |
|            370 |      27.5599 |      17.7143 |      13.8571 |
|            375 |      29.8274 |      18.7837 |      14.5484 |
|            380 |      32.1457 |      19.8717 |      15.2494 |

---

## collect_second_order_greeks
Calculate the second order Greeks of an option based on the Black Scholes Model: how the first order Greeks themselves respond to the price of the underlying asset, the strike price, the volatility and time.

This will return the following Greeks per Strike Price and Expiration Date:

- Gamma: measures the rate of change in the delta with respect to changes in the underlying price. Gamma is the second derivative of the value function with respect to the underlying price.
- Dual Gamma: the second derivative of the option value with respect to the strike price rather than the underlying price. It is the discounted risk-neutral probability density of the underlying at expiration.
- Vanna: also referred to as DvegaDspot and DdeltaDvol, is a second-order derivative of the option value, once to the underlying spot price and once to volatility.
- Charm: Charm or delta decay measures the instantaneous rate of change of delta over the passage of time.
- Vomma: also referred to as volga, vega convexity, or DvegaDvol measures second-order sensitivity to volatility. Vomma is the second derivative of the option value with respect to the volatility, or, stated another way, vomma measures the rate of change to vega as volatility changes.
- Veta: also referred to as DvegaDtime, measures the rate of change in the vega with respect to the passage of time. Veta is the second derivative of the value function; once to volatility and once to time.
- Vera: also referred to as rhova, measures the rate of change in rho with respect to volatility. Vera is the second derivative of the value function; once to volatility and once to interest rate.
- Partial Derivative: the second derivative of the option price with respect to the strike price, the rate at which the dual delta changes with the strike.

For a deeper explanation, please have a look at: [https://en.wikipedia.org/wiki/Greeks_(finance)](https://en.wikipedia.org/wiki/Greeks_(finance)){:target="_blank"} and the references to the literature as found on this page.

By default the stock price (the traded close), risk free rate, dividend yield and volatility of the most recent date are used; changing the start date prices the option as of that date instead. The volatility is the annualized standard deviation of the daily returns over the year before that date and the dividend yield the dividends of the 365 days up to that date relative to its close, so an earlier start date only uses what was known on that date. The exception is a date in the first year of the price history: without a full year before it, it takes the dividend yield of the first date that has one.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None which
means it will use the current dividend yield.
- <u>put_option (bool, optional):</u> Whether to calculate the put option delta. Defaults to False which means
it will calculate the call option delta.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: the second order greeks values containing the tickers and strike prices as the index and the
time to expiration and greeks as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.options.collect_second_order_greeks().loc["AAPL"]
```

Which returns:

|   Strike Price |   (Period('2026-01-01', 'D'), 'Gamma') |   (Period('2026-01-01', 'D'), 'Dual Gamma') |   (Period('2026-01-01', 'D'), 'Vanna') |   (Period('2026-01-01', 'D'), 'Charm') |   (Period('2026-01-01', 'D'), 'Vomma') |   (Period('2026-01-01', 'D'), 'Vera') |   (Period('2026-01-01', 'D'), 'Veta') |   (Period('2026-01-01', 'D'), 'PD') |   (Period('2026-01-02', 'D'), 'Gamma') |   (Period('2026-01-02', 'D'), 'Dual Gamma') |   (Period('2026-01-02', 'D'), 'Vanna') |   (Period('2026-01-02', 'D'), 'Charm') |   (Period('2026-01-02', 'D'), 'Vomma') |   (Period('2026-01-02', 'D'), 'Vera') |   (Period('2026-01-02', 'D'), 'Veta') |   (Period('2026-01-02', 'D'), 'PD') |   (Period('2026-01-03', 'D'), 'Gamma') |   (Period('2026-01-03', 'D'), 'Dual Gamma') |   (Period('2026-01-03', 'D'), 'Vanna') |   (Period('2026-01-03', 'D'), 'Charm') |   (Period('2026-01-03', 'D'), 'Vomma') |   (Period('2026-01-03', 'D'), 'Vera') |   (Period('2026-01-03', 'D'), 'Veta') |   (Period('2026-01-03', 'D'), 'PD') |   (Period('2026-01-04', 'D'), 'Gamma') |   (Period('2026-01-04', 'D'), 'Dual Gamma') |   (Period('2026-01-04', 'D'), 'Vanna') |   (Period('2026-01-04', 'D'), 'Charm') |   (Period('2026-01-04', 'D'), 'Vomma') |   (Period('2026-01-04', 'D'), 'Vera') |   (Period('2026-01-04', 'D'), 'Veta') |   (Period('2026-01-04', 'D'), 'PD') |   (Period('2026-01-05', 'D'), 'Gamma') |   (Period('2026-01-05', 'D'), 'Dual Gamma') |   (Period('2026-01-05', 'D'), 'Vanna') |   (Period('2026-01-05', 'D'), 'Charm') |   (Period('2026-01-05', 'D'), 'Vomma') |   (Period('2026-01-05', 'D'), 'Vera') |   (Period('2026-01-05', 'D'), 'Veta') |   (Period('2026-01-05', 'D'), 'PD') |   (Period('2026-01-06', 'D'), 'Gamma') |   (Period('2026-01-06', 'D'), 'Dual Gamma') |   (Period('2026-01-06', 'D'), 'Vanna') |   (Period('2026-01-06', 'D'), 'Charm') |   (Period('2026-01-06', 'D'), 'Vomma') |   (Period('2026-01-06', 'D'), 'Vera') |   (Period('2026-01-06', 'D'), 'Veta') |   (Period('2026-01-06', 'D'), 'PD') |   (Period('2026-01-07', 'D'), 'Gamma') |   (Period('2026-01-07', 'D'), 'Dual Gamma') |   (Period('2026-01-07', 'D'), 'Vanna') |   (Period('2026-01-07', 'D'), 'Charm') |   (Period('2026-01-07', 'D'), 'Vomma') |   (Period('2026-01-07', 'D'), 'Vera') |   (Period('2026-01-07', 'D'), 'Veta') |   (Period('2026-01-07', 'D'), 'PD') |   (Period('2026-01-08', 'D'), 'Gamma') |   (Period('2026-01-08', 'D'), 'Dual Gamma') |   (Period('2026-01-08', 'D'), 'Vanna') |   (Period('2026-01-08', 'D'), 'Charm') |   (Period('2026-01-08', 'D'), 'Vomma') |   (Period('2026-01-08', 'D'), 'Vera') |   (Period('2026-01-08', 'D'), 'Veta') |   (Period('2026-01-08', 'D'), 'PD') |   (Period('2026-01-09', 'D'), 'Gamma') |   (Period('2026-01-09', 'D'), 'Dual Gamma') |   (Period('2026-01-09', 'D'), 'Vanna') |   (Period('2026-01-09', 'D'), 'Charm') |   (Period('2026-01-09', 'D'), 'Vomma') |   (Period('2026-01-09', 'D'), 'Vera') |   (Period('2026-01-09', 'D'), 'Veta') |   (Period('2026-01-09', 'D'), 'PD') |   (Period('2026-01-10', 'D'), 'Gamma') |   (Period('2026-01-10', 'D'), 'Dual Gamma') |   (Period('2026-01-10', 'D'), 'Vanna') |   (Period('2026-01-10', 'D'), 'Charm') |   (Period('2026-01-10', 'D'), 'Vomma') |   (Period('2026-01-10', 'D'), 'Vera') |   (Period('2026-01-10', 'D'), 'Veta') |   (Period('2026-01-10', 'D'), 'PD') |   (Period('2026-01-11', 'D'), 'Gamma') |   (Period('2026-01-11', 'D'), 'Dual Gamma') |   (Period('2026-01-11', 'D'), 'Vanna') |   (Period('2026-01-11', 'D'), 'Charm') |   (Period('2026-01-11', 'D'), 'Vomma') |   (Period('2026-01-11', 'D'), 'Vera') |   (Period('2026-01-11', 'D'), 'Veta') |   (Period('2026-01-11', 'D'), 'PD') |   (Period('2026-01-12', 'D'), 'Gamma') |   (Period('2026-01-12', 'D'), 'Dual Gamma') |   (Period('2026-01-12', 'D'), 'Vanna') |   (Period('2026-01-12', 'D'), 'Charm') |   (Period('2026-01-12', 'D'), 'Vomma') |   (Period('2026-01-12', 'D'), 'Vera') |   (Period('2026-01-12', 'D'), 'Veta') |   (Period('2026-01-12', 'D'), 'PD') |   (Period('2026-01-13', 'D'), 'Gamma') |   (Period('2026-01-13', 'D'), 'Dual Gamma') |   (Period('2026-01-13', 'D'), 'Vanna') |   (Period('2026-01-13', 'D'), 'Charm') |   (Period('2026-01-13', 'D'), 'Vomma') |   (Period('2026-01-13', 'D'), 'Vera') |   (Period('2026-01-13', 'D'), 'Veta') |   (Period('2026-01-13', 'D'), 'PD') |   (Period('2026-01-14', 'D'), 'Gamma') |   (Period('2026-01-14', 'D'), 'Dual Gamma') |   (Period('2026-01-14', 'D'), 'Vanna') |   (Period('2026-01-14', 'D'), 'Charm') |   (Period('2026-01-14', 'D'), 'Vomma') |   (Period('2026-01-14', 'D'), 'Vera') |   (Period('2026-01-14', 'D'), 'Veta') |   (Period('2026-01-14', 'D'), 'PD') |   (Period('2026-01-15', 'D'), 'Gamma') |   (Period('2026-01-15', 'D'), 'Dual Gamma') |   (Period('2026-01-15', 'D'), 'Vanna') |   (Period('2026-01-15', 'D'), 'Charm') |   (Period('2026-01-15', 'D'), 'Vomma') |   (Period('2026-01-15', 'D'), 'Vera') |   (Period('2026-01-15', 'D'), 'Veta') |   (Period('2026-01-15', 'D'), 'PD') |   (Period('2026-01-16', 'D'), 'Gamma') |   (Period('2026-01-16', 'D'), 'Dual Gamma') |   (Period('2026-01-16', 'D'), 'Vanna') |   (Period('2026-01-16', 'D'), 'Charm') |   (Period('2026-01-16', 'D'), 'Vomma') |   (Period('2026-01-16', 'D'), 'Vera') |   (Period('2026-01-16', 'D'), 'Veta') |   (Period('2026-01-16', 'D'), 'PD') |   (Period('2026-01-17', 'D'), 'Gamma') |   (Period('2026-01-17', 'D'), 'Dual Gamma') |   (Period('2026-01-17', 'D'), 'Vanna') |   (Period('2026-01-17', 'D'), 'Charm') |   (Period('2026-01-17', 'D'), 'Vomma') |   (Period('2026-01-17', 'D'), 'Vera') |   (Period('2026-01-17', 'D'), 'Veta') |   (Period('2026-01-17', 'D'), 'PD') |   (Period('2026-01-18', 'D'), 'Gamma') |   (Period('2026-01-18', 'D'), 'Dual Gamma') |   (Period('2026-01-18', 'D'), 'Vanna') |   (Period('2026-01-18', 'D'), 'Charm') |   (Period('2026-01-18', 'D'), 'Vomma') |   (Period('2026-01-18', 'D'), 'Vera') |   (Period('2026-01-18', 'D'), 'Veta') |   (Period('2026-01-18', 'D'), 'PD') |   (Period('2026-01-19', 'D'), 'Gamma') |   (Period('2026-01-19', 'D'), 'Dual Gamma') |   (Period('2026-01-19', 'D'), 'Vanna') |   (Period('2026-01-19', 'D'), 'Charm') |   (Period('2026-01-19', 'D'), 'Vomma') |   (Period('2026-01-19', 'D'), 'Vera') |   (Period('2026-01-19', 'D'), 'Veta') |   (Period('2026-01-19', 'D'), 'PD') |   (Period('2026-01-20', 'D'), 'Gamma') |   (Period('2026-01-20', 'D'), 'Dual Gamma') |   (Period('2026-01-20', 'D'), 'Vanna') |   (Period('2026-01-20', 'D'), 'Charm') |   (Period('2026-01-20', 'D'), 'Vomma') |   (Period('2026-01-20', 'D'), 'Vera') |   (Period('2026-01-20', 'D'), 'Veta') |   (Period('2026-01-20', 'D'), 'PD') |   (Period('2026-01-21', 'D'), 'Gamma') |   (Period('2026-01-21', 'D'), 'Dual Gamma') |   (Period('2026-01-21', 'D'), 'Vanna') |   (Period('2026-01-21', 'D'), 'Charm') |   (Period('2026-01-21', 'D'), 'Vomma') |   (Period('2026-01-21', 'D'), 'Vera') |   (Period('2026-01-21', 'D'), 'Veta') |   (Period('2026-01-21', 'D'), 'PD') |   (Period('2026-01-22', 'D'), 'Gamma') |   (Period('2026-01-22', 'D'), 'Dual Gamma') |   (Period('2026-01-22', 'D'), 'Vanna') |   (Period('2026-01-22', 'D'), 'Charm') |   (Period('2026-01-22', 'D'), 'Vomma') |   (Period('2026-01-22', 'D'), 'Vera') |   (Period('2026-01-22', 'D'), 'Veta') |   (Period('2026-01-22', 'D'), 'PD') |   (Period('2026-01-23', 'D'), 'Gamma') |   (Period('2026-01-23', 'D'), 'Dual Gamma') |   (Period('2026-01-23', 'D'), 'Vanna') |   (Period('2026-01-23', 'D'), 'Charm') |   (Period('2026-01-23', 'D'), 'Vomma') |   (Period('2026-01-23', 'D'), 'Vera') |   (Period('2026-01-23', 'D'), 'Veta') |   (Period('2026-01-23', 'D'), 'PD') |   (Period('2026-01-24', 'D'), 'Gamma') |   (Period('2026-01-24', 'D'), 'Dual Gamma') |   (Period('2026-01-24', 'D'), 'Vanna') |   (Period('2026-01-24', 'D'), 'Charm') |   (Period('2026-01-24', 'D'), 'Vomma') |   (Period('2026-01-24', 'D'), 'Vera') |   (Period('2026-01-24', 'D'), 'Veta') |   (Period('2026-01-24', 'D'), 'PD') |   (Period('2026-01-25', 'D'), 'Gamma') |   (Period('2026-01-25', 'D'), 'Dual Gamma') |   (Period('2026-01-25', 'D'), 'Vanna') |   (Period('2026-01-25', 'D'), 'Charm') |   (Period('2026-01-25', 'D'), 'Vomma') |   (Period('2026-01-25', 'D'), 'Vera') |   (Period('2026-01-25', 'D'), 'Veta') |   (Period('2026-01-25', 'D'), 'PD') |   (Period('2026-01-26', 'D'), 'Gamma') |   (Period('2026-01-26', 'D'), 'Dual Gamma') |   (Period('2026-01-26', 'D'), 'Vanna') |   (Period('2026-01-26', 'D'), 'Charm') |   (Period('2026-01-26', 'D'), 'Vomma') |   (Period('2026-01-26', 'D'), 'Vera') |   (Period('2026-01-26', 'D'), 'Veta') |   (Period('2026-01-26', 'D'), 'PD') |   (Period('2026-01-27', 'D'), 'Gamma') |   (Period('2026-01-27', 'D'), 'Dual Gamma') |   (Period('2026-01-27', 'D'), 'Vanna') |   (Period('2026-01-27', 'D'), 'Charm') |   (Period('2026-01-27', 'D'), 'Vomma') |   (Period('2026-01-27', 'D'), 'Vera') |   (Period('2026-01-27', 'D'), 'Veta') |   (Period('2026-01-27', 'D'), 'PD') |   (Period('2026-01-28', 'D'), 'Gamma') |   (Period('2026-01-28', 'D'), 'Dual Gamma') |   (Period('2026-01-28', 'D'), 'Vanna') |   (Period('2026-01-28', 'D'), 'Charm') |   (Period('2026-01-28', 'D'), 'Vomma') |   (Period('2026-01-28', 'D'), 'Vera') |   (Period('2026-01-28', 'D'), 'Veta') |   (Period('2026-01-28', 'D'), 'PD') |   (Period('2026-01-29', 'D'), 'Gamma') |   (Period('2026-01-29', 'D'), 'Dual Gamma') |   (Period('2026-01-29', 'D'), 'Vanna') |   (Period('2026-01-29', 'D'), 'Charm') |   (Period('2026-01-29', 'D'), 'Vomma') |   (Period('2026-01-29', 'D'), 'Vera') |   (Period('2026-01-29', 'D'), 'Veta') |   (Period('2026-01-29', 'D'), 'PD') |
|---------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|---------------------------------------:|--------------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|------------------------------------:|
|            290 |                                 0.0001 |                                      0.0001 |                                 0.0035 |                                -0.2099 |                                 0.1908 |                                0.0026 |                               -0.0003 |                              0.0001 |                                 0.0017 |                                      0.0015 |                                 0.0936 |                                -2.7872 |                                 5.0326 |                                0.1382 |                               -0.0047 |                              0.0015 |                                 0.0047 |                                      0.0041 |                                 0.2558 |                                -5.0935 |                                13.6993 |                                0.564  |                               -0.009  |                              0.0041 |                                 0.0075 |                                      0.0066 |                                 0.4054 |                                -6.0728 |                                21.626  |                                1.1864 |                               -0.0113 |                              0.0066 |                                 0.0096 |                                      0.0084 |                                 0.5212 |                                -6.265  |                                27.6937 |                                1.8979 |                               -0.0123 |                              0.0084 |                                 0.0111 |                                      0.0098 |                                 0.6061 |                                -6.0897 |                                32.0779 |                                2.6364 |                               -0.0125 |                              0.0098 |                                 0.0123 |                                      0.0108 |                                 0.6671 |                                -5.763  |                                35.1702 |                                3.3701 |                               -0.0123 |                              0.0108 |                                 0.0131 |                                      0.0115 |                                 0.7106 |                                -5.3877 |                                37.3152 |                                4.0839 |                               -0.012  |                              0.0115 |                                 0.0136 |                                      0.012  |                                 0.7413 |                                -5.0109 |                                38.7726 |                                4.7708 |                               -0.0116 |                              0.012  |                                 0.014  |                                      0.0123 |                                 0.7626 |                                -4.6535 |                                39.7296 |                                5.4282 |                               -0.0112 |                              0.0123 |                                 0.0142 |                                      0.0125 |                                 0.777  |                                -4.3235 |                                40.3201 |                                6.0559 |                               -0.0108 |                              0.0125 |                                 0.0144 |                                      0.0127 |                                 0.7863 |                                -4.0227 |                                40.6404 |                                6.6547 |                               -0.0104 |                              0.0127 |                                 0.0145 |                                      0.0127 |                                 0.7918 |                                -3.7503 |                                40.7599 |                                7.2258 |                               -0.01   |                              0.0127 |                                 0.0145 |                                      0.0128 |                                 0.7944 |                                -3.5042 |                                40.7294 |                                7.7709 |                               -0.0097 |                              0.0128 |                                 0.0145 |                                      0.0128 |                                 0.7948 |                                -3.282  |                                40.5865 |                                8.2914 |                               -0.0094 |                              0.0128 |                                 0.0145 |                                      0.0127 |                                 0.7935 |                                -3.0811 |                                40.3592 |                                8.7891 |                               -0.0091 |                              0.0127 |                                 0.0144 |                                      0.0127 |                                 0.791  |                                -2.8992 |                                40.0686 |                                9.2652 |                               -0.0088 |                              0.0127 |                                 0.0144 |                                      0.0126 |                                 0.7876 |                                -2.7341 |                                39.7306 |                                9.7213 |                               -0.0085 |                              0.0126 |                                 0.0143 |                                      0.0126 |                                 0.7834 |                                -2.5839 |                                39.3575 |                               10.1586 |                               -0.0082 |                              0.0126 |                                 0.0142 |                                      0.0125 |                                 0.7787 |                                -2.447  |                                38.9587 |                               10.5782 |                               -0.008  |                              0.0125 |                                 0.0141 |                                      0.0124 |                                 0.7735 |                                -2.3217 |                                38.5415 |                               10.9812 |                               -0.0078 |                              0.0124 |                                 0.014  |                                      0.0123 |                                 0.7681 |                                -2.2069 |                                38.1117 |                               11.3686 |                               -0.0076 |                              0.0123 |                                 0.0139 |                                      0.0122 |                                 0.7624 |                                -2.1014 |                                37.6735 |                               11.7412 |                               -0.0074 |                              0.0122 |                                 0.0138 |                                      0.0121 |                                 0.7566 |                                -2.0042 |                                37.2305 |                               12.1    |                               -0.0072 |                              0.0121 |                                 0.0136 |                                      0.012  |                                 0.7507 |                                -1.9144 |                                36.7854 |                               12.4456 |                               -0.007  |                              0.012  |                                 0.0135 |                                      0.0119 |                                 0.7448 |                                -1.8314 |                                36.3403 |                               12.7787 |                               -0.0069 |                              0.0119 |                                 0.0134 |                                      0.0118 |                                 0.7388 |                                -1.7543 |                                35.8969 |                               13.1    |                               -0.0067 |                              0.0118 |                                 0.0133 |                                      0.0117 |                                 0.7329 |                                -1.6827 |                                35.4564 |                               13.41   |                               -0.0066 |                              0.0117 |                                 0.0132 |                                      0.0116 |                                 0.727  |                                -1.6161 |                                35.0199 |                               13.7093 |                               -0.0065 |                              0.0116 |
|            295 |                                 0      |                                      0      |                                 0.0001 |                                -0.0035 |                                 0.004  |                                0      |                                0      |                              0      |                                 0.0002 |                                      0.0002 |                                 0.0137 |                                -0.4073 |                                 0.9328 |                                0.0203 |                               -0.0008 |                              0.0002 |                                 0.0011 |                                      0.001  |                                 0.0772 |                                -1.5337 |                                 5.2396 |                                0.1707 |                               -0.0032 |                              0.001  |                                 0.0026 |                                      0.0022 |                                 0.1756 |                                -2.6237 |                                11.8853 |                                0.5159 |                               -0.0057 |                              0.0022 |                                 0.0041 |                                      0.0035 |                                 0.2805 |                                -3.3605 |                                18.9235 |                                1.0262 |                               -0.0076 |                              0.0035 |                                 0.0055 |                                      0.0047 |                                 0.3769 |                                -3.7722 |                                25.3505 |                                1.6488 |                               -0.0088 |                              0.0047 |                                 0.0067 |                                      0.0057 |                                 0.46   |                                -3.9557 |                                30.8431 |                                2.3392 |                               -0.0095 |                              0.0057 |                                 0.0077 |                                      0.0065 |                                 0.5294 |                                -3.9932 |                                35.3875 |                                3.0657 |                               -0.0098 |                              0.0065 |                                 0.0085 |                                      0.0072 |                                 0.5865 |                                -3.9419 |                                39.083  |                                3.8072 |                               -0.01   |                              0.0072 |                                 0.0092 |                                      0.0078 |                                 0.6331 |                                -3.8388 |                                42.0574 |                                4.5498 |                               -0.01   |                              0.0078 |                                 0.0097 |                                      0.0083 |                                 0.6709 |                                -3.7074 |                                44.4333 |                                5.2849 |                               -0.0099 |                              0.0083 |                                 0.0102 |                                      0.0086 |                                 0.7016 |                                -3.5622 |                                46.3178 |                                6.0068 |                               -0.0098 |                              0.0086 |                                 0.0105 |                                      0.0089 |                                 0.7263 |                                -3.4122 |                                47.8004 |                                6.7123 |                               -0.0096 |                              0.0089 |                                 0.0108 |                                      0.0092 |                                 0.7462 |                                -3.2629 |                                48.9544 |                                7.3994 |                               -0.0094 |                              0.0092 |                                 0.011  |                                      0.0094 |                                 0.7621 |                                -3.1176 |                                49.8392 |                                8.0671 |                               -0.0092 |                              0.0094 |                                 0.0112 |                                      0.0095 |                                 0.7747 |                                -2.9781 |                                50.5031 |                                8.7152 |                               -0.009  |                              0.0095 |                                 0.0114 |                                      0.0096 |                                 0.7845 |                                -2.8454 |                                50.9852 |                                9.3436 |                               -0.0088 |                              0.0096 |                                 0.0115 |                                      0.0097 |                                 0.7922 |                                -2.7198 |                                51.3171 |                                9.9526 |                               -0.0086 |                              0.0097 |                                 0.0115 |                                      0.0098 |                                 0.7979 |                                -2.6014 |                                51.5248 |                               10.5427 |                               -0.0084 |                              0.0098 |                                 0.0116 |                                      0.0098 |                                 0.8021 |                                -2.4901 |                                51.6294 |                               11.1145 |                               -0.0082 |                              0.0098 |                                 0.0116 |                                      0.0099 |                                 0.805  |                                -2.3855 |                                51.6482 |                               11.6686 |                               -0.008  |                              0.0099 |                                 0.0116 |                                      0.0099 |                                 0.8068 |                                -2.2874 |                                51.5956 |                               12.2057 |                               -0.0078 |                              0.0099 |                                 0.0117 |                                      0.0099 |                                 0.8076 |                                -2.1953 |                                51.4835 |                               12.7263 |                               -0.0077 |                              0.0099 |                                 0.0116 |                                      0.0099 |                                 0.8077 |                                -2.1089 |                                51.3216 |                               13.2312 |                               -0.0075 |                              0.0099 |                                 0.0116 |                                      0.0099 |                                 0.8071 |                                -2.0277 |                                51.1182 |                               13.721  |                               -0.0073 |                              0.0099 |                                 0.0116 |                                      0.0099 |                                 0.806  |                                -1.9514 |                                50.8802 |                               14.1963 |                               -0.0072 |                              0.0099 |                                 0.0116 |                                      0.0098 |                                 0.8044 |                                -1.8797 |                                50.6134 |                               14.6577 |                               -0.007  |                              0.0098 |                                 0.0115 |                                      0.0098 |                                 0.8024 |                                -1.8122 |                                50.3227 |                               15.1056 |                               -0.0069 |                              0.0098 |                                 0.0115 |                                      0.0098 |                                 0.8001 |                                -1.7486 |                                50.0121 |                               15.5408 |                               -0.0068 |                              0.0098 |
|            300 |                                 0      |                                      0      |                                 0      |                                 0      |                                 0      |                                0      |                                0      |                              0      |                                 0      |                                      0      |                                 0.0012 |                                -0.0359 |                                 0.0993 |                                0.0018 |                               -0.0001 |                              0      |                                 0.0002 |                                      0.0002 |                                 0.0164 |                                -0.3246 |                                 1.3409 |                                0.0362 |                               -0.0008 |                              0.0002 |                                 0.0007 |                                      0.0006 |                                 0.0577 |                                -0.8602 |                                 4.7163 |                                0.1698 |                               -0.0022 |                              0.0006 |                                 0.0014 |                                      0.0012 |                                 0.1198 |                                -1.4324 |                                 9.7716 |                                0.4397 |                               -0.0037 |                              0.0012 |                                 0.0023 |                                      0.0019 |                                 0.1918 |                                -1.915  |                                15.6051 |                                0.8422 |                               -0.005  |                              0.0019 |                                 0.0032 |                                      0.0026 |                                 0.2653 |                                -2.2748 |                                21.5282 |                                1.355  |                               -0.0061 |                              0.0026 |                                 0.004  |                                      0.0033 |                                 0.3354 |                                -2.5212 |                                27.1441 |                                1.9517 |                               -0.0069 |                              0.0033 |                                 0.0048 |                                      0.004  |                                 0.3996 |                                -2.6761 |                                32.2648 |                                2.6087 |                               -0.0075 |                              0.004  |                                 0.0055 |                                      0.0045 |                                 0.4573 |                                -2.7616 |                                36.8261 |                                3.307  |                               -0.0079 |                              0.0045 |                                 0.0061 |                                      0.005  |                                 0.5083 |                                -2.7963 |                                40.8303 |                                4.0315 |                               -0.0082 |                              0.005  |                                 0.0067 |                                      0.0055 |                                 0.5531 |                                -2.7946 |                                44.3123 |                                4.771  |                               -0.0083 |                              0.0055 |                                 0.0071 |                                      0.0059 |                                 0.5922 |                                -2.7674 |                                47.3205 |                                5.5172 |                               -0.0084 |                              0.0059 |                                 0.0075 |                                      0.0062 |                                 0.6262 |                                -2.7226 |                                49.9069 |                                6.2637 |                               -0.0084 |                              0.0062 |                                 0.0079 |                                      0.0065 |                                 0.6557 |                                -2.6661 |                                52.122  |                                7.0061 |                               -0.0084 |                              0.0065 |                                 0.0082 |                                      0.0067 |                                 0.6812 |                                -2.602  |                                54.012  |                                7.7409 |                               -0.0083 |                              0.0067 |                                 0.0085 |                                      0.0069 |                                 0.7033 |                                -2.5334 |                                55.6186 |                                8.4658 |                               -0.0083 |                              0.0069 |                                 0.0087 |                                      0.0071 |                                 0.7224 |                                -2.4624 |                                56.9785 |                                9.1791 |                               -0.0082 |                              0.0071 |                                 0.0089 |                                      0.0073 |                                 0.7388 |                                -2.3906 |                                58.1238 |                                9.8797 |                               -0.0081 |                              0.0073 |                                 0.009  |                                      0.0074 |                                 0.753  |                                -2.3191 |                                59.0822 |                               10.5667 |                               -0.008  |                              0.0074 |                                 0.0092 |                                      0.0075 |                                 0.7652 |                                -2.2487 |                                59.8779 |                               11.2398 |                               -0.0078 |                              0.0075 |                                 0.0093 |                                      0.0076 |                                 0.7756 |                                -2.1799 |                                60.5317 |                               11.8986 |                               -0.0077 |                              0.0076 |                                 0.0094 |                                      0.0077 |                                 0.7844 |                                -2.113  |                                61.0616 |                               12.5431 |                               -0.0076 |                              0.0077 |                                 0.0095 |                                      0.0078 |                                 0.7919 |                                -2.0483 |                                61.4832 |                               13.1733 |                               -0.0075 |                              0.0078 |                                 0.0096 |                                      0.0079 |                                 0.7983 |                                -1.9859 |                                61.81   |                               13.7894 |                               -0.0074 |                              0.0079 |                                 0.0096 |                                      0.0079 |                                 0.8036 |                                -1.9259 |                                62.0536 |                               14.3915 |                               -0.0072 |                              0.0079 |                                 0.0097 |                                      0.0079 |                                 0.8079 |                                -1.8682 |                                62.2244 |                               14.9799 |                               -0.0071 |                              0.0079 |                                 0.0097 |                                      0.008  |                                 0.8115 |                                -1.8129 |                                62.331  |                               15.5548 |                               -0.007  |                              0.008  |                                 0.0097 |                                      0.008  |                                 0.8144 |                                -1.7599 |                                62.3813 |                               16.1166 |                               -0.0069 |                              0.008  |
|            305 |                                 0      |                                      0      |                                 0      |                                 0      |                                 0      |                                0      |                                0      |                              0      |                                 0      |                                      0      |                                 0.0001 |                                -0.002  |                                 0.0064 |                                0.0001 |                                0      |                              0      |                                 0      |                                      0      |                                 0.0025 |                                -0.0498 |                                 0.2407 |                                0.0056 |                               -0.0001 |                              0      |                                 0.0002 |                                      0.0001 |                                 0.0148 |                                -0.2199 |                                 1.4114 |                                0.0435 |                               -0.0006 |                              0.0001 |                                 0.0004 |                                      0.0003 |                                 0.0416 |                                -0.4972 |                                 3.974  |                                0.1532 |                               -0.0014 |                              0.0003 |                                 0.0008 |                                      0.0007 |                                 0.0818 |                                -0.8151 |                                 7.7871 |                                0.36   |                               -0.0024 |                              0.0007 |                                 0.0014 |                                      0.0011 |                                 0.1309 |                                -1.1199 |                                12.4342 |                                0.6704 |                               -0.0034 |                              0.0011 |                                 0.0019 |                                      0.0015 |                                 0.1846 |                                -1.3843 |                                17.4963 |                                1.0777 |                               -0.0042 |                              0.0015 |                                 0.0025 |                                      0.002  |                                 0.2395 |                                -1.5993 |                                22.6518 |                                1.5691 |                               -0.005  |                              0.002  |                                 0.003  |                                      0.0024 |                                 0.2933 |                                -1.7661 |                                27.6846 |                                2.1301 |                               -0.0056 |                              0.0024 |                                 0.0036 |                                      0.0028 |                                 0.3447 |                                -1.8901 |                                32.4637 |                                2.7466 |                               -0.006  |                              0.0028 |                                 0.0041 |                                      0.0032 |                                 0.3928 |                                -1.978  |                                36.9182 |                                3.4062 |                               -0.0064 |                              0.0032 |                                 0.0045 |                                      0.0036 |                                 0.4374 |                                -2.0366 |                                41.0173 |                                4.0983 |                               -0.0067 |                              0.0036 |                                 0.0049 |                                      0.0039 |                                 0.4783 |                                -2.0716 |                                44.7551 |                                4.814  |                               -0.0069 |                              0.0039 |                                 0.0053 |                                      0.0042 |                                 0.5157 |                                -2.0879 |                                48.1412 |                                5.5461 |                               -0.0071 |                              0.0042 |                                 0.0057 |                                      0.0045 |                                 0.5496 |                                -2.0897 |                                51.1938 |                                6.2887 |                               -0.0072 |                              0.0045 |                                 0.006  |                                      0.0048 |                                 0.5803 |                                -2.0803 |                                53.9356 |                                7.0371 |                               -0.0073 |                              0.0048 |                                 0.0063 |                                      0.005  |                                 0.6081 |                                -2.0622 |                                56.3907 |                                7.7874 |                               -0.0073 |                              0.005  |                                 0.0065 |                                      0.0052 |                                 0.6331 |                                -2.0376 |                                58.5838 |                                8.5366 |                               -0.0073 |                              0.0052 |                                 0.0067 |                                      0.0054 |                                 0.6557 |                                -2.0082 |                                60.5382 |                                9.2824 |                               -0.0073 |                              0.0054 |                                 0.007  |                                      0.0055 |                                 0.6761 |                                -1.9752 |                                62.2762 |                               10.0227 |                               -0.0073 |                              0.0055 |                                 0.0071 |                                      0.0057 |                                 0.6944 |                                -1.9397 |                                63.8185 |                               10.7562 |                               -0.0072 |                              0.0057 |                                 0.0073 |                                      0.0058 |                                 0.7108 |                                -1.9025 |                                65.1838 |                               11.4816 |                               -0.0072 |                              0.0058 |                                 0.0075 |                                      0.0059 |                                 0.7256 |                                -1.8642 |                                66.3893 |                               12.198  |                               -0.0071 |                              0.0059 |                                 0.0076 |                                      0.006  |                                 0.7389 |                                -1.8254 |                                67.4506 |                               12.9047 |                               -0.0071 |                              0.006  |                                 0.0077 |                                      0.0061 |                                 0.7508 |                                -1.7864 |                                68.3816 |                               13.6013 |                               -0.007  |                              0.0061 |                                 0.0078 |                                      0.0062 |                                 0.7614 |                                -1.7476 |                                69.1951 |                               14.2873 |                               -0.0069 |                              0.0062 |                                 0.0079 |                                      0.0063 |                                 0.771  |                                -1.7091 |                                69.9024 |                               14.9626 |                               -0.0068 |                              0.0063 |                                 0.008  |                                      0.0064 |                                 0.7795 |                                -1.6711 |                                70.5137 |                               15.6269 |                               -0.0068 |                              0.0064 |
|            310 |                                 0      |                                      0      |                                 0      |                                 0      |                                 0      |                                0      |                                0      |                              0      |                                 0      |                                      0      |                                 0      |                                -0.0001 |                                 0.0003 |                                0      |                                0      |                              0      |                                 0      |                                      0      |                                 0.0003 |                                -0.0057 |                                 0.0313 |                                0.0006 |                                0      |                              0      |                                 0      |                                      0      |                                 0.003  |                                -0.0447 |                                 0.328  |                                0.0089 |                               -0.0001 |                              0      |                                 0.0001 |                                      0.0001 |                                 0.012  |                                -0.143  |                                 1.3078 |                                0.0442 |                               -0.0005 |                              0.0001 |                                 0.0003 |                                      0.0002 |                                 0.0297 |                                -0.2955 |                                 3.232  |                                0.1309 |                               -0.001  |                              0.0002 |                                 0.0005 |                                      0.0004 |                                 0.0561 |                                -0.4791 |                                 6.0915 |                                0.2878 |                               -0.0016 |                              0.0004 |                                 0.0008 |                                      0.0006 |                                 0.0895 |                                -0.6703 |                                 9.7071 |                                0.5241 |                               -0.0023 |                              0.0006 |                                 0.0012 |                                      0.0009 |                                 0.1279 |                                -0.8527 |                                13.8449 |                                0.8406 |                               -0.0029 |                              0.0009 |                                 0.0015 |                                      0.0012 |                                 0.1693 |                                -1.017  |                                18.2846 |                                1.2331 |                               -0.0035 |                              0.0012 |                                 0.0019 |                                      0.0015 |                                 0.2119 |                                -1.1592 |                                22.8457 |                                1.6943 |                               -0.0041 |                              0.0015 |                                 0.0023 |                                      0.0018 |                                 0.2545 |                                -1.2784 |                                27.3924 |                                2.2155 |                               -0.0045 |                              0.0018 |                                 0.0027 |                                      0.0021 |                                 0.2963 |                                -1.3759 |                                31.8286 |                                2.7879 |                               -0.0049 |                              0.0021 |                                 0.003  |                                      0.0023 |                                 0.3367 |                                -1.4537 |                                36.0903 |                                3.4033 |                               -0.0053 |                              0.0023 |                                 0.0034 |                                      0.0026 |                                 0.3751 |                                -1.5141 |                                40.1375 |                                4.054  |                               -0.0056 |                              0.0026 |                                 0.0037 |                                      0.0029 |                                 0.4116 |                                -1.5596 |                                43.948  |                                4.7333 |                               -0.0058 |                              0.0029 |                                 0.004  |                                      0.0031 |                                 0.4458 |                                -1.5923 |                                47.5122 |                                5.4353 |                               -0.006  |                              0.0031 |                                 0.0043 |                                      0.0033 |                                 0.4778 |                                -1.6144 |                                50.8291 |                                6.1549 |                               -0.0061 |                              0.0033 |                                 0.0046 |                                      0.0035 |                                 0.5077 |                                -1.6275 |                                53.9036 |                                6.8876 |                               -0.0062 |                              0.0035 |                                 0.0048 |                                      0.0037 |                                 0.5355 |                                -1.6332 |                                56.7445 |                                7.6298 |                               -0.0063 |                              0.0037 |                                 0.0051 |                                      0.0039 |                                 0.5613 |                                -1.6328 |                                59.3628 |                                8.3783 |                               -0.0064 |                              0.0039 |                                 0.0053 |                                      0.0041 |                                 0.5853 |                                -1.6274 |                                61.7707 |                                9.1305 |                               -0.0064 |                              0.0041 |                                 0.0055 |                                      0.0042 |                                 0.6074 |                                -1.6179 |                                63.9811 |                                9.884  |                               -0.0065 |                              0.0042 |                                 0.0057 |                                      0.0044 |                                 0.6279 |                                -1.6051 |                                66.007  |                               10.6369 |                               -0.0065 |                              0.0044 |                                 0.0058 |                                      0.0045 |                                 0.6468 |                                -1.5896 |                                67.8609 |                               11.3878 |                               -0.0065 |                              0.0045 |                                 0.006  |                                      0.0046 |                                 0.6642 |                                -1.572  |                                69.5551 |                               12.1351 |                               -0.0065 |                              0.0046 |                                 0.0061 |                                      0.0047 |                                 0.6803 |                                -1.5528 |                                71.1012 |                               12.878  |                               -0.0065 |                              0.0047 |                                 0.0063 |                                      0.0048 |                                 0.6952 |                                -1.5323 |                                72.5101 |                               13.6153 |                               -0.0064 |                              0.0048 |                                 0.0064 |                                      0.0049 |                                 0.7089 |                                -1.5108 |                                73.7921 |                               14.3464 |                               -0.0064 |                              0.0049 |
|            315 |                                 0      |                                      0      |                                 0      |                                 0      |                                 0      |                                0      |                                0      |                              0      |                                 0      |                                      0      |                                 0      |                                 0      |                                 0      |                                0      |                                0      |                              0      |                                 0      |                                      0      |                                 0      |                                -0.0005 |                                 0.003  |                                0.0001 |                                0      |                              0      |                                 0      |                                      0      |                                 0.0005 |                                -0.0073 |                                 0.0605 |                                0.0015 |                                0      |                              0      |                                 0      |                                      0      |                                 0.0029 |                                -0.0346 |                                 0.3552 |                                0.0107 |                               -0.0001 |                              0      |                                 0.0001 |                                      0.0001 |                                 0.0093 |                                -0.0924 |                                 1.1365 |                                0.0411 |                               -0.0003 |                              0.0001 |                                 0.0002 |                                      0.0001 |                                 0.0211 |                                -0.1801 |                                 2.5758 |                                0.1085 |                               -0.0007 |                              0.0001 |                                 0.0003 |                                      0.0002 |                                 0.0387 |                                -0.2893 |                                 4.7138 |                                0.2269 |                               -0.0011 |                              0.0002 |                                 0.0005 |                                      0.0004 |                                 0.0616 |                                -0.4097 |                                 7.4875 |                                0.4054 |                               -0.0015 |                              0.0004 |                                 0.0007 |                                      0.0005 |                                 0.0888 |                                -0.5324 |                                10.7784 |                                0.6482 |                               -0.002  |                              0.0005 |                                 0.001  |                                      0.0007 |                                 0.1192 |                                -0.6509 |                                14.4513 |                                0.9557 |                               -0.0025 |                              0.0007 |                                 0.0012 |                                      0.0009 |                                 0.1518 |                                -0.7611 |                                18.3769 |                                1.3254 |                               -0.0029 |                              0.0009 |                                 0.0015 |                                      0.0011 |                                 0.1858 |                                -0.8606 |                                22.4432 |                                1.7531 |                               -0.0033 |                              0.0011 |                                 0.0018 |                                      0.0013 |                                 0.2202 |                                -0.9486 |                                26.5585 |                                2.2334 |                               -0.0037 |                              0.0013 |                                 0.0021 |                                      0.0015 |                                 0.2546 |                                -1.0249 |                                30.6512 |                                2.761  |                               -0.0041 |                              0.0015 |                                 0.0023 |                                      0.0017 |                                 0.2884 |                                -1.0901 |                                34.6673 |                                3.33   |                               -0.0044 |                              0.0017 |                                 0.0026 |                                      0.0019 |                                 0.3214 |                                -1.1449 |                                38.5676 |                                3.9351 |                               -0.0046 |                              0.0019 |                                 0.0028 |                                      0.0021 |                                 0.3533 |                                -1.1902 |                                42.3247 |                                4.5711 |                               -0.0048 |                              0.0021 |                                 0.0031 |                                      0.0023 |                                 0.384  |                                -1.2271 |                                45.9206 |                                5.2335 |                               -0.005  |                              0.0023 |                                 0.0033 |                                      0.0025 |                                 0.4134 |                                -1.2565 |                                49.3445 |                                5.9181 |                               -0.0052 |                              0.0025 |                                 0.0036 |                                      0.0026 |                                 0.4413 |                                -1.2794 |                                52.5912 |                                6.621  |                               -0.0053 |                              0.0026 |                                 0.0038 |                                      0.0028 |                                 0.4679 |                                -1.2964 |                                55.6592 |                                7.3389 |                               -0.0055 |                              0.0028 |                                 0.004  |                                      0.003  |                                 0.493  |                                -1.3085 |                                58.5505 |                                8.0688 |                               -0.0056 |                              0.003  |                                 0.0042 |                                      0.0031 |                                 0.5168 |                                -1.3162 |                                61.2688 |                                8.808  |                               -0.0056 |                              0.0031 |                                 0.0043 |                                      0.0032 |                                 0.5393 |                                -1.3202 |                                63.8195 |                                9.5543 |                               -0.0057 |                              0.0032 |                                 0.0045 |                                      0.0034 |                                 0.5604 |                                -1.321  |                                66.2088 |                               10.3056 |                               -0.0058 |                              0.0034 |                                 0.0047 |                                      0.0035 |                                 0.5804 |                                -1.319  |                                68.4439 |                               11.0601 |                               -0.0058 |                              0.0035 |                                 0.0048 |                                      0.0036 |                                 0.5991 |                                -1.3147 |                                70.5319 |                               11.8164 |                               -0.0058 |                              0.0036 |                                 0.005  |                                      0.0037 |                                 0.6168 |                                -1.3085 |                                72.4803 |                               12.5729 |                               -0.0058 |                              0.0037 |
|            320 |                                 0      |                                      0      |                                 0      |                                 0      |                                 0      |                                0      |                                0      |                              0      |                                 0      |                                      0      |                                 0      |                                 0      |                                 0      |                                0      |                                0      |                              0      |                                 0      |                                      0      |                                 0      |                                 0      |                                 0.0002 |                                0      |                                0      |                              0      |                                 0      |                                      0      |                                 0.0001 |                                -0.001  |                                 0.009  |                                0.0002 |                                0      |                              0      |                                 0      |                                      0      |                                 0.0006 |                                -0.0071 |                                 0.0809 |                                0.0022 |                                0      |                              0      |                                 0      |                                      0      |                                 0.0025 |                                -0.0252 |                                 0.3434 |                                0.0112 |                               -0.0001 |                              0      |                                 0.0001 |                                      0      |                                 0.007  |                                -0.0601 |                                 0.9527 |                                0.0363 |                               -0.0002 |                              0      |                                 0.0001 |                                      0.0001 |                                 0.015  |                                -0.1122 |                                 2.029  |                                0.0883 |                               -0.0005 |                              0.0001 |                                 0.0002 |                                      0.0001 |                                 0.0269 |                                -0.1788 |                                 3.6264 |                                0.1774 |                               -0.0007 |                              0.0001 |                                 0.0003 |                                      0.0002 |                                 0.0426 |                                -0.2553 |                                 5.7373 |                                0.3118 |                               -0.001  |                              0.0002 |                                 0.0005 |                                      0.0003 |                                 0.0618 |                                -0.3371 |                                 8.3104 |                                0.4966 |                               -0.0014 |                              0.0003 |                                 0.0006 |                                      0.0004 |                                 0.084  |                                -0.4202 |                                11.2712 |                                0.7346 |                               -0.0017 |                              0.0004 |                                 0.0008 |                                      0.0006 |                                 0.1085 |                                -0.5016 |                                14.5367 |                                1.0262 |                               -0.0021 |                              0.0006 |                                 0.001  |                                      0.0007 |                                 0.1347 |                                -0.5792 |                                18.0258 |                                1.37   |                               -0.0024 |                              0.0007 |                                 0.0012 |                                      0.0009 |                                 0.1621 |                                -0.6515 |                                21.6646 |                                1.7637 |                               -0.0028 |                              0.0009 |                                 0.0014 |                                      0.001  |                                 0.1903 |                                -0.7178 |                                25.3887 |                                2.2041 |                               -0.0031 |                              0.001  |                                 0.0016 |                                      0.0012 |                                 0.2188 |                                -0.7777 |                                29.1444 |                                2.6876 |                               -0.0034 |                              0.0012 |                                 0.0018 |                                      0.0013 |                                 0.2473 |                                -0.8311 |                                32.8876 |                                3.2104 |                               -0.0036 |                              0.0013 |                                 0.002  |                                      0.0014 |                                 0.2755 |                                -0.8782 |                                36.5834 |                                3.7686 |                               -0.0039 |                              0.0014 |                                 0.0022 |                                      0.0016 |                                 0.3032 |                                -0.9194 |                                40.2047 |                                4.3585 |                               -0.0041 |                              0.0016 |                                 0.0024 |                                      0.0017 |                                 0.3304 |                                -0.9551 |                                43.7309 |                                4.9765 |                               -0.0043 |                              0.0017 |                                 0.0026 |                                      0.0019 |                                 0.3567 |                                -0.9856 |                                47.1469 |                                5.6194 |                               -0.0044 |                              0.0019 |                                 0.0028 |                                      0.002  |                                 0.3822 |                                -1.0115 |                                50.4421 |                                6.2838 |                               -0.0046 |                              0.002  |                                 0.003  |                                      0.0021 |                                 0.4069 |                                -1.033  |                                53.6096 |                                6.967  |                               -0.0047 |                              0.0021 |                                 0.0031 |                                      0.0023 |                                 0.4306 |                                -1.0508 |                                56.6452 |                                7.6663 |                               -0.0048 |                              0.0023 |                                 0.0033 |                                      0.0024 |                                 0.4534 |                                -1.0651 |                                59.547  |                                8.3792 |                               -0.0049 |                              0.0024 |                                 0.0035 |                                      0.0025 |                                 0.4752 |                                -1.0763 |                                62.3151 |                                9.1037 |                               -0.005  |                              0.0025 |                                 0.0036 |                                      0.0026 |                                 0.4961 |                                -1.0847 |                                64.9508 |                                9.8377 |                               -0.0051 |                              0.0026 |                                 0.0037 |                                      0.0027 |                                 0.516  |                                -1.0907 |                                67.4563 |                               10.5794 |                               -0.0051 |                              0.0027 |
|            325 |                                 0      |                                      0      |                                 0      |                                 0      |                                 0      |                                0      |                                0      |                              0      |                                 0      |                                      0      |                                 0      |                                 0      |                                 0      |                                0      |                                0      |                              0      |                                 0      |                                      0      |                                 0      |                                 0      |                                 0      |                                0      |                                0      |                              0      |                                 0      |                                      0      |                                 0      |                                -0.0001 |                                 0.0011 |                                0      |                                0      |                              0      |                                 0      |                                      0      |                                 0.0001 |                                -0.0013 |                                 0.0156 |                                0.0004 |                                0      |                              0      |                                 0      |                                      0      |                                 0.0006 |                                -0.006  |                                 0.0902 |                                0.0027 |                                0      |                              0      |                                 0      |                                      0      |                                 0.0021 |                                -0.0179 |                                 0.3115 |                                0.0108 |                               -0.0001 |                              0      |                                 0      |                                      0      |                                 0.0053 |                                -0.0394 |                                 0.7819 |                                0.0311 |                               -0.0002 |                              0      |                                 0.0001 |                                      0.0001 |                                 0.0107 |                                -0.0713 |                                 1.588  |                                0.071  |                               -0.0003 |                              0.0001 |                                 0.0001 |                                      0.0001 |                                 0.0188 |                                -0.1128 |                                 2.7829 |                                0.1381 |                               -0.0005 |                              0.0001 |                                 0.0002 |                                      0.0001 |                                 0.0297 |                                -0.1619 |                                 4.383  |                                0.2392 |                               -0.0007 |                              0.0001 |                                 0.0003 |                                      0.0002 |                                 0.0433 |                                -0.2164 |                                 6.3741 |                                0.3795 |                               -0.001  |                              0.0002 |                                 0.0004 |                                      0.0003 |                                 0.0593 |                                -0.274  |                                 8.721  |                                0.5623 |                               -0.0012 |                              0.0003 |                                 0.0005 |                                      0.0004 |                                 0.0775 |                                -0.3327 |                                11.376  |                                0.7898 |                               -0.0015 |                              0.0004 |                                 0.0006 |                                      0.0005 |                                 0.0974 |                                -0.3909 |                                14.286  |                                1.0624 |                               -0.0018 |                              0.0005 |                                 0.0008 |                                      0.0006 |                                 0.1188 |                                -0.4474 |                                17.3977 |                                1.3797 |                               -0.0021 |                              0.0006 |                                 0.0009 |                                      0.0007 |                                 0.1413 |                                -0.5014 |                                20.6603 |                                1.7404 |                               -0.0023 |                              0.0007 |                                 0.0011 |                                      0.0008 |                                 0.1646 |                                -0.5521 |                                24.0279 |                                2.1427 |                               -0.0026 |                              0.0008 |                                 0.0013 |                                      0.0009 |                                 0.1884 |                                -0.5992 |                                27.4597 |                                2.5842 |                               -0.0028 |                              0.0009 |                                 0.0014 |                                      0.001  |                                 0.2124 |                                -0.6426 |                                30.9207 |                                3.0623 |                               -0.003  |                              0.001  |                                 0.0016 |                                      0.0011 |                                 0.2365 |                                -0.6822 |                                34.3811 |                                3.5744 |                               -0.0032 |                              0.0011 |                                 0.0017 |                                      0.0012 |                                 0.2605 |                                -0.7181 |                                37.8164 |                                4.1179 |                               -0.0034 |                              0.0012 |                                 0.0019 |                                      0.0013 |                                 0.2843 |                                -0.7504 |                                41.2064 |                                4.6899 |                               -0.0036 |                              0.0013 |                                 0.002  |                                      0.0014 |                                 0.3077 |                                -0.7791 |                                44.5349 |                                5.2878 |                               -0.0038 |                              0.0014 |                                 0.0022 |                                      0.0015 |                                 0.3306 |                                -0.8047 |                                47.789  |                                5.9093 |                               -0.0039 |                              0.0015 |                                 0.0023 |                                      0.0016 |                                 0.353  |                                -0.8271 |                                50.959  |                                6.5518 |                               -0.004  |                              0.0016 |                                 0.0025 |                                      0.0017 |                                 0.3749 |                                -0.8467 |                                54.0375 |                                7.2132 |                               -0.0042 |                              0.0017 |                                 0.0026 |                                      0.0018 |                                 0.3962 |                                -0.8637 |                                57.0192 |                                7.8912 |                               -0.0043 |                              0.0018 |                                 0.0028 |                                      0.0019 |                                 0.4168 |                                -0.8783 |                                59.9005 |                                8.5841 |                               -0.0044 |                              0.0019 |
|            330 |                                 0      |                                      0      |                                 0      |                                 0      |                                 0      |                                0      |                                0      |                              0      |                                 0      |                                      0      |                                 0      |                                 0      |                                 0      |                                0      |                                0      |                              0      |                                 0      |                                      0      |                                 0      |                                 0      |                                 0      |                                0      |                                0      |                              0      |                                 0      |                                      0      |                                 0      |                                 0      |                                 0.0001 |                                0      |                                0      |                              0      |                                 0      |                                      0      |                                 0      |                                -0.0002 |                                 0.0026 |                                0.0001 |                                0      |                              0      |                                 0      |                                      0      |                                 0.0001 |                                -0.0013 |                                 0.0208 |                                0.0006 |                                0      |                              0      |                                 0      |                                      0      |                                 0.0006 |                                -0.0048 |                                 0.0908 |                                0.0029 |                                0      |                              0      |                                 0      |                                      0      |                                 0.0017 |                                -0.0126 |                                 0.272  |                                0.01   |                               -0.0001 |                              0      |                                 0      |                                      0      |                                 0.0039 |                                -0.0262 |                                 0.6336 |                                0.0261 |                               -0.0001 |                              0      |                                 0      |                                      0      |                                 0.0077 |                                -0.0462 |                                 1.2392 |                                0.0567 |                               -0.0002 |                              0      |                                 0.0001 |                                      0.0001 |                                 0.0133 |                                -0.0725 |                                 2.1352 |                                0.1074 |                               -0.0003 |                              0.0001 |                                 0.0001 |                                      0.0001 |                                 0.0209 |                                -0.1044 |                                 3.3466 |                                0.1836 |                               -0.0005 |                              0.0001 |                                 0.0002 |                                      0.0001 |                                 0.0305 |                                -0.1408 |                                 4.8784 |                                0.2898 |                               -0.0007 |                              0.0001 |                                 0.0003 |                                      0.0002 |                                 0.0421 |                                -0.1805 |                                 6.7188 |                                0.4298 |                               -0.0009 |                              0.0002 |                                 0.0003 |                                      0.0002 |                                 0.0555 |                                -0.2223 |                                 8.8444 |                                0.6061 |                               -0.0011 |                              0.0002 |                                 0.0004 |                                      0.0003 |                                 0.0705 |                                -0.2651 |                                11.2241 |                                0.8202 |                               -0.0013 |                              0.0003 |                                 0.0005 |                                      0.0004 |                                 0.0869 |                                -0.308  |                                13.8229 |                                1.073  |                               -0.0015 |                              0.0004 |                                 0.0006 |                                      0.0004 |                                 0.1046 |                                -0.3502 |                                16.6046 |                                1.3645 |                               -0.0017 |                              0.0004 |                                 0.0008 |                                      0.0005 |                                 0.1232 |                                -0.3912 |                                19.5338 |                                1.694  |                               -0.0019 |                              0.0005 |                                 0.0009 |                                      0.0006 |                                 0.1425 |                                -0.4305 |                                22.5768 |                                2.0606 |                               -0.0022 |                              0.0006 |                                 0.001  |                                      0.0007 |                                 0.1625 |                                -0.4679 |                                25.7029 |                                2.4626 |                               -0.0024 |                              0.0007 |                                 0.0011 |                                      0.0008 |                                 0.1828 |                                -0.5031 |                                28.8844 |                                2.8986 |                               -0.0025 |                              0.0008 |                                 0.0012 |                                      0.0008 |                                 0.2034 |                                -0.536  |                                32.0968 |                                3.3667 |                               -0.0027 |                              0.0008 |                                 0.0014 |                                      0.0009 |                                 0.2242 |                                -0.5665 |                                35.3188 |                                3.8649 |                               -0.0029 |                              0.0009 |                                 0.0015 |                                      0.001  |                                 0.2449 |                                -0.5947 |                                38.532  |                                4.3913 |                               -0.0031 |                              0.001  |                                 0.0016 |                                      0.0011 |                                 0.2655 |                                -0.6206 |                                41.7208 |                                4.9438 |                               -0.0032 |                              0.0011 |                                 0.0017 |                                      0.0012 |                                 0.2859 |                                -0.6443 |                                44.8721 |                                5.5206 |                               -0.0033 |                              0.0012 |                                 0.0019 |                                      0.0013 |                                 0.3061 |                                -0.6658 |                                47.975  |                                6.1196 |                               -0.0035 |                              0.0013 |                                 0.002  |                                      0.0014 |                                 0.326  |                                -0.6852 |                                51.0208 |                                6.7391 |                               -0.0036 |                              0.0014 |
|            335 |                                 0      |                                      0      |                                 0      |                                 0      |                                 0      |                                0      |                                0      |                              0      |                                 0      |                                      0      |                                 0      |                                 0      |                                 0      |                                0      |                                0      |                              0      |                                 0      |                                      0      |                                 0      |                                 0      |                                 0      |                                0      |                                0      |                              0      |                                 0      |                                      0      |                                 0      |                                 0      |                                 0      |                                0      |                                0      |                              0      |                                 0      |                                      0      |                                 0      |                                 0      |                                 0.0004 |                                0      |                                0      |                              0      |                                 0      |                                      0      |                                 0      |                                -0.0002 |                                 0.0042 |                                0.0001 |                                0      |                              0      |                                 0      |                                      0      |                                 0.0001 |                                -0.0012 |                                 0.0238 |                                0.0007 |                                0      |                              0      |                                 0      |                                      0      |                                 0.0005 |                                -0.0037 |                                 0.086  |                                0.0029 |                                0      |                              0      |                                 0      |                                      0      |                                 0.0013 |                                -0.0089 |                                 0.2319 |                                0.0089 |                                0      |                              0      |                                 0      |                                      0      |                                 0.0029 |                                -0.0176 |                                 0.5098 |                                0.0216 |                               -0.0001 |                              0      |                                 0      |                                      0      |                                 0.0056 |                                -0.0304 |                                 0.9665 |                                0.0451 |                               -0.0002 |                              0      |                                 0.0001 |                                      0      |                                 0.0095 |                                -0.0474 |                                 1.6406 |                                0.0835 |                               -0.0002 |                              0      |                                 0.0001 |                                      0.0001 |                                 0.0148 |                                -0.0684 |                                 2.5584 |                                0.1411 |                               -0.0004 |                              0.0001 |                                 0.0001 |                                      0.0001 |                                 0.0217 |                                -0.0929 |                                 3.7335 |                                0.2217 |                               -0.0005 |                              0.0001 |                                 0.0002 |                                      0.0001 |                                 0.03   |                                -0.1202 |                                 5.1674 |                                0.3287 |                               -0.0006 |                              0.0001 |                                 0.0002 |                                      0.0001 |                                 0.0399 |                                -0.1498 |                                 6.8519 |                                0.4648 |                               -0.0008 |                              0.0001 |                                 0.0003 |                                      0.0002 |                                 0.0511 |                                -0.1808 |                                 8.7717 |                                0.6321 |                               -0.0009 |                              0.0002 |                                 0.0004 |                                      0.0002 |                                 0.0636 |                                -0.2128 |                                10.9061 |                                0.8319 |                               -0.0011 |                              0.0002 |                                 0.0004 |                                      0.0003 |                                 0.0773 |                                -0.2451 |                                13.2316 |                                1.0652 |                               -0.0013 |                              0.0003 |                                 0.0005 |                                      0.0003 |                                 0.092  |                                -0.2773 |                                15.7231 |                                1.3321 |                               -0.0015 |                              0.0003 |                                 0.0006 |                                      0.0004 |                                 0.1075 |                                -0.309  |                                18.3554 |                                1.6326 |                               -0.0016 |                              0.0004 |                                 0.0007 |                                      0.0005 |                                 0.1237 |                                -0.3398 |                                21.104  |                                1.966  |                               -0.0018 |                              0.0005 |                                 0.0008 |                                      0.0005 |                                 0.1405 |                                -0.3696 |                                23.9454 |                                2.3317 |                               -0.002  |                              0.0005 |                                 0.0009 |                                      0.0006 |                                 0.1578 |                                -0.3982 |                                26.858  |                                2.7284 |                               -0.0022 |                              0.0006 |                                 0.001  |                                      0.0007 |                                 0.1755 |                                -0.4254 |                                29.8219 |                                3.1551 |                               -0.0023 |                              0.0007 |                                 0.0011 |                                      0.0007 |                                 0.1933 |                                -0.4511 |                                32.8191 |                                3.6104 |                               -0.0025 |                              0.0007 |                                 0.0012 |                                      0.0008 |                                 0.2113 |                                -0.4753 |                                35.8336 |                                4.0928 |                               -0.0026 |                              0.0008 |                                 0.0013 |                                      0.0009 |                                 0.2294 |                                -0.498  |                                38.8513 |                                4.6009 |                               -0.0027 |                              0.0009 |                                 0.0014 |                                      0.0009 |                                 0.2475 |                                -0.5192 |                                41.8597 |                                5.1332 |                               -0.0029 |                              0.0009 |

---

## get_gamma
Calculate the gamma of an option based on the Black Scholes Model: how much the delta changes for a 1.00 change in the price of the underlying asset.

The Black Scholes Model is a mathematical model used to estimate the price of European-style options. The gamma is the rate of change of the delta with respect to the price of the underlying asset.

The gamma calculation is the theoretical value of the gamma. The actual gamma can differ from this value due to several factors such as the volatility of the underlying asset, the time to expiration, the risk free rate and more.

The formula is as follows:

$$
d_{1} = \frac{\ln\left(\frac{S}{K}\right) + \left(r - q + \frac{\sigma^{2}}{2}\right) \cdot t}{\sigma \cdot \sqrt{t}}
$$

$$
\Gamma = \frac{e^{- q \cdot t} \cdot N'(d_{1})}{S \cdot \sigma \cdot \sqrt{t}}
$$

Where S is the stock price, K is the strike price, r is the risk free rate, q is the dividend yield, $$\sigma$$ is the volatility, t is the time to expiration, N'(d1) is the standard normal probability density at d1 and N(d2) is the cumulative normal distribution of d2.

The Gamma can be interpreted as follows:

- If Gamma is high, it indicates that the option's Delta is highly sensitive to changes in the underlying asset's price. The option's Delta will change more significantly with small movements in the stock price.
- If Gamma is low, it suggests that the option's Delta is relatively insensitive to changes in the underlying asset's price. The option's Delta changes more gradually with movements in the stock price.

Note that the gamma of a call option and put option are equal to each other.

Gamma is largest for at-the-money options close to expiry, which is where a delta hedge needs the most frequent rebalancing and where a short option position can lose money fastest on a sharp move. Because it is per $1 move in the underlying, it is not comparable across stocks with different prices; risk reports therefore use dollar gamma (Gamma x $$S^{2} / 100$$, the change in the dollar delta for a 1% move) when they add up gamma across underlyings.

**Also known as:** rate of change of delta, option convexity.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None which
means it will use the current dividend yield.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: the gamma values containing the tickers and strike prices as the index and the
time to expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["PFE"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.options.get_gamma(
    strike_price_range=0.2, strike_step_size=1
).loc["PFE", ["2026-01-07", "2026-01-14", "2026-01-28"]]
```

Which returns:

|   Strike Price |   2026-01-07 |   2026-01-14 |   2026-01-28 |
|---------------:|-------------:|-------------:|-------------:|
|             19 |       0      |       0      |       0.0002 |
|             20 |       0      |       0      |       0.0022 |
|             21 |       0      |       0.0012 |       0.0135 |
|             22 |       0.0012 |       0.0165 |       0.0502 |
|             23 |       0.0395 |       0.0929 |       0.1195 |
|             24 |       0.2623 |       0.24   |       0.1926 |
|             25 |       0.4397 |       0.3115 |       0.22   |
|             26 |       0.2178 |       0.2197 |       0.1852 |
|             27 |       0.0366 |       0.0902 |       0.119  |
|             28 |       0.0023 |       0.0229 |       0.06   |

---

## get_dual_gamma
Calculate the dual gamma of an option based on the Black Scholes Model: how much the dual delta changes for a 1.00 change in the strike price.

The Black Scholes Model is a mathematical model used to estimate the price of European-style options. The dual gamma is the second derivative of the option price with respect to the strike price, i.e. the rate of change of the dual delta as the strike price changes. It is the strike-space counterpart of gamma and describes the (discounted) risk-neutral probability density of the underlying finishing at the strike.

The dual gamma calculation is the theoretical value of the dual gamma. The actual dual gamma can differ from this value due to several factors such as the volatility of the underlying asset, the time to expiration, the risk free rate and more.

The formula is as follows:

$$
d_{1} = \frac{\ln\left(\frac{S}{K}\right) + \left(r - q + \frac{\sigma^{2}}{2}\right) \cdot t}{\sigma \cdot \sqrt{t}}
$$

$$
d_{2} = d_{1} - \sigma \cdot \sqrt{t}
$$

$$
\text{Dual Gamma} = \frac{e^{- r \cdot t} \cdot N'(d_{2})}{K \cdot \sigma \cdot \sqrt{t}}
$$

Where S is the stock price, K is the strike price, r is the risk free rate, q is the dividend yield, $$\sigma$$ is the volatility, t is the time to expiration, N'(d2) is the standard normal probability density at d2 and N(d1) is the cumulative normal distribution of d1. Note that Dual Gamma is a second derivative with respect to the strike price, so it is the strike and not the stock price that appears in the denominator.

Note that the dual gamma of a call option and put option are equal to each other.

**Also known as:** strike gamma, binary option gamma.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None which
means it will use the current dividend yield.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: the dual gamma values containing the tickers and strike prices as the index and the
time to expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["T"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.options.get_dual_gamma(
    strike_price_range=0.2, strike_step_size=1
).loc["T", ["2026-01-07", "2026-01-14", "2026-01-28"]]
```

Which returns:

|   Strike Price |   2026-01-07 |   2026-01-14 |   2026-01-28 |
|---------------:|-------------:|-------------:|-------------:|
|             19 |       0      |       0      |       0      |
|             20 |       0      |       0      |       0.0007 |
|             21 |       0      |       0.0003 |       0.0081 |
|             22 |       0.0003 |       0.009  |       0.0446 |
|             23 |       0.0255 |       0.0866 |       0.1339 |
|             24 |       0.2943 |       0.2845 |       0.2348 |
|             25 |       0.5059 |       0.3613 |       0.2564 |
|             26 |       0.1614 |       0.198  |       0.1841 |
|             27 |       0.0115 |       0.0514 |       0.0911 |
|             28 |       0.0002 |       0.0069 |       0.0324 |

---

## get_vanna
Calculate the vanna of an option based on the Black Scholes Model: how much the delta changes for a 1.00 change in the volatility, or equally the vega for a 1.00 change in the price of the underlying asset.

The Black Scholes Model is a mathematical model used to estimate the price of European-style options. The vanna is the rate of change of the vega with respect to the price of the underlying asset.

The vanna calculation is the theoretical value of the vanna. The actual vanna can differ from this value due to several factors such as the volatility of the underlying asset, the time to expiration, the risk free rate and more.

The formula is as follows:

$$
d_{1} = \frac{\ln\left(\frac{S}{K}\right) + \left(r - q + \frac{\sigma^{2}}{2}\right) \cdot t}{\sigma \cdot \sqrt{t}}
$$

$$
d_{2} = d_{1} - \sigma \cdot \sqrt{t}
$$

$$
\text{Vanna} = - e^{- q \cdot t} \cdot N'(d_{1}) \cdot \frac{d_{2}}{\sigma}
$$

Where S is the stock price, K is the strike price, r is the risk free rate, q is the dividend yield, $$\sigma$$ is the volatility, t is the time to expiration, N(d1) is the cumulative normal distribution of d1 and N(d2) is the the cumulative normal distribution of d2.

The Vanna can be interpreted as follows:

- If Vanna is positive, it indicates that the Delta of the option becomes more positive as both the underlying asset's price and implied volatility increase, and more negative as they both decrease.
- If Vanna is negative, it suggests that the Delta of the option becomes more negative as both the underlying asset's price and implied volatility increase, and more positive as they both decrease.

Note that the vanna of a call option and put option are equal to each other.

**Also known as:** delta-vega cross-derivative.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None which
means it will use the current dividend yield.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: the vanna values containing the tickers and strike prices as the index and the
time to expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["DIS"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.options.get_vanna(
    strike_price_range=0.15, strike_step_size=2, expiration_time_range=91
).loc["DIS", ["2026-01-30", "2026-03-01", "2026-03-31"]]
```

Which returns:

|   Strike Price |   2026-01-30 |   2026-03-01 |   2026-03-31 |
|---------------:|-------------:|-------------:|-------------:|
|             96 |      -0.3178 |      -0.595  |      -0.6673 |
|             98 |      -0.4447 |      -0.6644 |      -0.6908 |
|            100 |      -0.5731 |      -0.706  |      -0.6877 |
|            102 |      -0.6795 |      -0.7114 |      -0.6556 |
|            104 |      -0.7374 |      -0.675  |      -0.5939 |
|            106 |      -0.7247 |      -0.5955 |      -0.504  |
|            108 |      -0.6296 |      -0.4753 |      -0.3894 |
|            110 |      -0.4551 |      -0.3213 |      -0.2548 |
|            112 |      -0.2189 |      -0.1429 |      -0.1063 |
|            114 |       0.0498 |       0.048  |       0.0496 |
|            116 |       0.3173 |       0.2394 |       0.2062 |
|            118 |       0.5519 |       0.4197 |       0.3572 |
|            120 |       0.7301 |       0.5791 |       0.497  |
|            122 |       0.8397 |       0.7105 |       0.621  |
|            124 |       0.8799 |       0.8093 |       0.726  |
|            126 |       0.8593 |       0.874  |       0.8097 |
|            128 |       0.7923 |       0.9056 |       0.8714 |

---

## get_charm
Calculate the charm of an option based on the Black Scholes Model: how much the delta changes as time passes, the delta decay.

The Black Scholes Model is a mathematical model used to estimate the price of European-style options. The charm is the rate of change of the delta with respect to the time to expiration.

The charm calculation is the theoretical value of the charm. The actual charm can differ from this value due to several factors such as the volatility of the underlying asset, the time to expiration, the risk free rate and more.

The formula is as follows:

$$
d_{1} = \frac{\ln\left(\frac{S}{K}\right) + \left(r - q + \frac{\sigma^{2}}{2}\right) \cdot t}{\sigma \cdot \sqrt{t}}
$$

$$
d_{2} = d_{1} - \sigma \cdot \sqrt{t}
$$

$$
\text{Call Charm} = q \cdot e^{- q \cdot t} \cdot N(d_{1}) - \frac{e^{- q \cdot t} \cdot N'(d_{1}) \cdot (2 \cdot (r - q) \cdot t - d_{2} \cdot \sigma \cdot \sqrt{t})}{2 \cdot t \cdot \sigma \cdot \sqrt{t}}
$$

$$
\text{Put Charm} = - q \cdot e^{- q \cdot t} \cdot N(- d_{1}) - \frac{e^{- q \cdot t} \cdot N'(d_{1}) \cdot (2 \cdot (r - q) \cdot t - d_{2} \cdot \sigma \cdot \sqrt{t})}{2 \cdot t \cdot \sigma \cdot \sqrt{t}}
$$

Where S is the stock price, K is the strike price, r is the risk free rate, q is the dividend yield, $$\sigma$$ is the volatility, t is the time to expiration, N'(d1) is the standard normal probability density at d1 and N(d1) is the cumulative normal distribution of d1.

Charm is the derivative with respect to calendar time elapsed, in the same direction as Theta, but it is reported per year rather than per day. Divide by 365 for delta decay per calendar day. Color follows the same per-year convention.

The Charm can be interpreted as follows:

- If Charm is positive, it suggests that the option's Delta is becoming more positive over time. In other words, the option is gaining sensitivity to changes in the underlying asset's price as time passes.
- If Charm is negative, it indicates that the option's Delta is becoming more negative over time. The option is losing sensitivity to changes in the underlying asset's price as time passes.

**Also known as:** delta time decay, delta bleed.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None which
means it will use the current dividend yield.
- <u>put_option (bool, optional):</u> Whether to calculate the put option charm. Defaults to False which means
it will calculate the call option charm.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: the charm values containing the tickers and strike prices as the index and the
time to expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["HD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.options.get_charm(
    strike_price_range=0.15, strike_step_size=5
).loc["HD", ["2026-01-07", "2026-01-14", "2026-01-28"]]
```

Which returns:

|   Strike Price |   2026-01-07 |   2026-01-14 |   2026-01-28 |
|---------------:|-------------:|-------------:|-------------:|
|            290 |       0.0264 |       0.0405 |       0.1977 |
|            295 |       0.0268 |       0.076  |       0.332  |
|            300 |       0.0307 |       0.1726 |       0.5239 |
|            305 |       0.057  |       0.3914 |       0.7663 |
|            310 |       0.1843 |       0.8006 |       1.0315 |
|            315 |       0.6286 |       1.4229 |       1.2704 |
|            320 |       1.7336 |       2.1641 |       1.4208 |
|            325 |       3.6153 |       2.7782 |       1.4233 |
|            330 |       5.5281 |       2.9352 |       1.2406 |
|            335 |       5.8384 |       2.3897 |       0.8727 |
|            340 |       3.3616 |       1.1521 |       0.3608 |
|            345 |      -1.0896 |      -0.4685 |      -0.2214 |
|            350 |      -5.0641 |      -1.9984 |      -0.7863 |
|            355 |      -6.6128 |      -3.0258 |      -1.2543 |
|            360 |      -5.729  |      -3.3722 |      -1.5714 |
|            365 |      -3.7544 |      -3.1181 |      -1.7176 |
|            370 |      -1.9575 |      -2.5022 |      -1.7048 |
|            375 |      -0.8345 |      -1.7834 |      -1.5678 |
|            380 |      -0.2961 |      -1.1451 |      -1.352  |
|            385 |      -0.0886 |      -0.6688 |      -1.1021 |
|            390 |      -0.0226 |      -0.358  |      -0.8539 |

---

## get_vomma
Calculate the vomma of an option based on the Black Scholes Model: how much the vega changes for a 1.00 change in the volatility, the convexity of the option value in the volatility.

The Black Scholes Model is a mathematical model used to estimate the price of European-style options. The vomma is the rate of change of the vega with respect to the volatility of the underlying asset.

The vomma calculation is the theoretical value of the vomma. The actual vomma can differ from this value due to several factors such as the volatility of the underlying asset, the time to expiration, the risk free rate and more.

The formula is as follows:

$$
d_{1} = \frac{\ln\left(\frac{S}{K}\right) + \left(r - q + \frac{\sigma^{2}}{2}\right) \cdot t}{\sigma \cdot \sqrt{t}}
$$

$$
d_{2} = d_{1} - \sigma \cdot \sqrt{t}
$$

$$
\text{Vomma} = \frac{S \cdot e^{- q \cdot t} \cdot N'(d_{1}) \cdot \sqrt{t} \cdot (d_{1} \cdot d_{2})}{\sigma}
$$

Where S is the stock price, K is the strike price, r is the risk free rate, q is the dividend yield, $$\sigma$$ is the volatility, t is the time to expiration, N(d1) is the cumulative normal distribution of d1 and N(d2) is the the cumulative normal distribution of d2.

The vomma can be interpreted as follows:

- If Vomma is high, it indicates that the option's Vega is highly sensitive to changes in implied volatility. The option's value will experience more significant fluctuations with variations in implied volatility.
- If Vomma is low, it suggests that the option's Vega is relatively less sensitive to changes in implied volatility.

**Also known as:** volga, vega convexity.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None which
means it will use the current dividend yield.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: the vomma values containing the tickers and strike prices as the index and the
time to expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["UNH"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.options.get_vomma(
    strike_price_range=0.15, strike_step_size=5, expiration_time_range=91
).loc["UNH", ["2026-01-30", "2026-03-01", "2026-03-31"]]
```

Which returns:

|   Strike Price |   2026-01-30 |   2026-03-01 |   2026-03-31 |
|---------------:|-------------:|-------------:|-------------:|
|            280 |      51.2097 |      52.1616 |      47.8182 |
|            285 |      47.8381 |      45.2178 |      40.3535 |
|            290 |      42.7853 |      37.8675 |      32.9635 |
|            295 |      36.4289 |      30.4352 |      25.8688 |
|            300 |      29.2674 |      23.2408 |      19.2724 |
|            305 |      21.8715 |      16.5838 |      13.3537 |
|            310 |      14.8278 |      10.7301 |       8.2647 |
|            315 |       8.6846 |       5.9013 |       4.1267 |
|            320 |       3.9039 |       2.2678 |       1.0291 |
|            325 |       0.8251 |      -0.0552 |      -0.9709 |
|            330 |      -0.3565 |      -1.0091 |      -1.8476 |
|            335 |       0.4045 |      -0.5891 |      -1.6048 |
|            340 |       3.0113 |       1.1589 |      -0.2734 |
|            345 |       7.245  |       4.1456 |       2.0917 |
|            350 |      12.7927 |       8.2446 |       5.4153 |
|            355 |      19.2798 |      13.3011 |       9.6054 |
|            360 |      26.3039 |      19.1402 |      14.5571 |
|            365 |      33.4654 |      25.575  |      20.1562 |
|            370 |      40.3941 |      32.4143 |      26.2832 |
|            375 |      46.7696 |      39.4695 |      32.8159 |

---

## get_vera
Calculate the vera of an option based on the Black Scholes Model: how much the rho changes for a 1.00 change in the volatility.

The Black Scholes Model is a mathematical model used to estimate the price of European-style options. The vera is the rate of change of the rho with respect to volatility.

The vera calculation is the theoretical value of the vera. The actual vera can differ from this value due to several factors such as the volatility of the underlying asset, the time to expiration, the risk free rate and more.

The formula is as follows:

$$
d_{1} = \frac{\ln\left(\frac{S}{K}\right) + \left(r - q + \frac{\sigma^{2}}{2}\right) \cdot t}{\sigma \cdot \sqrt{t}}
$$

$$
d_{2} = d_{1} - \sigma \cdot \sqrt{t}
$$

$$
\text{Vera} = - K \cdot t \cdot e^{- r \cdot t} \cdot N'(d_{2}) \cdot \frac{d_{1}}{\sigma}
$$

Where S is the stock price, K is the strike price, r is the risk free rate, q is the dividend yield, $$\sigma$$ is the volatility, t is the time to expiration, N'(d2) is the standard normal probability density at d2 and N(d1) is the cumulative normal distribution of d1.

Vera is reported unscaled, per 1.00 of volatility and per 1.00 of the risk free rate, matching Rho.

The Vera can be interpreted as follows:

- If Vera is positive, it indicates that the option's Rho becomes more positive as implied volatility rises. In other words, the option gains sensitivity to the risk free rate when volatility increases.
- If Vera is negative, it suggests that the option's Rho becomes more negative as implied volatility rises. The option loses sensitivity to the risk free rate when volatility increases.

Note that the vera of a call option and put option are equal to each other.

**Also known as:** rho-vega cross-derivative.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None which
means it will use the current dividend yield.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: the vera values containing the tickers and strike prices as the index and the
time to expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["LLY"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.options.get_vera(
    strike_price_range=0.15, strike_step_size=20, expiration_time_range=181
).loc["LLY", ["2026-01-30", "2026-03-31", "2026-06-29"]]
```

Which returns:

|   Strike Price |   2026-01-30 |   2026-03-31 |   2026-06-29 |
|---------------:|-------------:|-------------:|-------------:|
|            920 |     -45.0096 |    -157.215  |    -295.291  |
|            940 |     -50.1022 |    -152.342  |    -280.248  |
|            960 |     -52.6538 |    -143.623  |    -261.571  |
|            980 |     -52.0109 |    -131.27   |    -239.609  |
|           1000 |     -47.8614 |    -115.641  |    -214.763  |
|           1020 |     -40.299  |     -97.212  |    -187.471  |
|           1040 |     -29.8143 |     -76.5443 |    -158.19   |
|           1060 |     -17.2215 |     -54.2545 |    -127.386  |
|           1080 |      -3.5354 |     -30.9812 |     -95.5234 |
|           1100 |      10.1711 |      -7.3547 |     -63.0518 |
|           1120 |      22.9037 |      16.0281 |     -30.3999 |
|           1140 |      33.8555 |      38.6251 |       2.0327 |
|           1160 |      42.4735 |      59.9646 |      33.8803 |
|           1180 |      48.481  |      79.6557 |      64.8152 |
|           1200 |      51.8615 |      97.3928 |      94.55   |
|           1220 |      52.8126 |     112.957  |     122.838  |

---

## get_veta
Calculate the veta of an option based on the Black Scholes Model: how much the vega changes as time passes.

The Black Scholes Model is a mathematical model used to estimate the price of European-style options. The veta is the rate of change of the vega with respect to the time to expiration.

The veta calculation is the theoretical value of the veta. The actual veta can differ from this value due to several factors such as the volatility of the underlying asset, the time to expiration, the risk free rate and more.

The formula is as follows:

$$
d_{1} = \frac{\ln\left(\frac{S}{K}\right) + \left(r - q + \frac{\sigma^{2}}{2}\right) \cdot t}{\sigma \cdot \sqrt{t}}
$$

$$
d_{2} = d_{1} - \sigma \cdot \sqrt{t}
$$

$$
\text{Veta} = \frac{S \cdot e^{- q \cdot t} \cdot N'(d_{1}) \cdot \sqrt{t} \cdot \left(q + \frac{(r - q) \cdot d_{1}}{\sigma \cdot \sqrt{t}} - \frac{1 + d_{1} \cdot d_{2}}{2 \cdot t}\right)}{100 \cdot 365}
$$

Where S is the stock price, K is the strike price, r is the risk free rate, q is the dividend yield, $$\sigma$$ is the volatility, t is the time to expiration, N'(d1) is the standard normal probability density at d1 and N(d2) is the cumulative normal distribution of d2.

This expression equals dVega/dt, the change in Vega as calendar time passes (the negative of the derivative with respect to the remaining time to maturity t), and is used as is, without a change of sign. Veta thus, like Theta, Charm and Color, measures the change per unit of time that passes: an option close to the money loses Vega as expiry approaches, so its Veta is typically negative.

It is common practice to divide the mathematical result of veta by 100 times the number of days per year to express it as the change in Vega (per percentage point of volatility) per calendar day. This is also done here.

The Veta can be interpreted as follows:

- If Veta is positive, it indicates that the option's Vega is becoming more positive over time. In other words, the option is gaining sensitivity to changes in implied volatility as time passes.
- If Veta is negative, it suggests that the option's Vega is becoming more negative over time. The option is losing sensitivity to changes in implied volatility as time passes.

**Also known as:** vega time decay.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None which
means it will use the current dividend yield.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: the veta values containing the tickers and strike prices as the index and the
time to expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AZO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.options.get_veta(
    strike_price_range=0.1, strike_step_size=50
).loc["AZO", ["2026-01-07", "2026-01-14", "2026-01-28"]]
```

Which returns:

|   Strike Price |   2026-01-07 |   2026-01-14 |   2026-01-28 |
|---------------:|-------------:|-------------:|-------------:|
|           3050 |      -0.0051 |      -0.0325 |      -0.0541 |
|           3100 |      -0.0189 |      -0.0561 |      -0.0651 |
|           3150 |      -0.051  |      -0.0816 |      -0.0722 |
|           3200 |      -0.1    |      -0.1011 |      -0.0746 |
|           3250 |      -0.1436 |      -0.1082 |      -0.0728 |
|           3300 |      -0.1551 |      -0.1037 |      -0.0692 |
|           3350 |      -0.1403 |      -0.096  |      -0.0664 |
|           3400 |      -0.1344 |      -0.0946 |      -0.0665 |
|           3450 |      -0.1525 |      -0.1026 |      -0.0701 |
|           3500 |      -0.1688 |      -0.1146 |      -0.0762 |
|           3550 |      -0.154  |      -0.1213 |      -0.0826 |
|           3600 |      -0.1108 |      -0.1163 |      -0.0869 |
|           3650 |      -0.063  |      -0.0994 |      -0.0875 |
|           3700 |      -0.0288 |      -0.0759 |      -0.0835 |

---

## get_partial_derivative
Calculate the partial derivative of an option based on the Black Scholes Model: how fast the dual delta changes with the strike price, the second derivative of the option value with respect to the strike price.

The Black Scholes Model is a mathematical model used to estimate the price of European-style options. The partial derivative is the second derivative of the option price with respect to the strike price, the rate at which the dual delta changes with the strike.

Note that this uses a single, flat assumed volatility (the same value at every strike price) rather than the market's actual implied volatility smile. This means it is NOT the Breeden-Litzenberger risk-neutral density -- with a flat volatility input the second derivative can only ever recover a lognormal density, regardless of what the real market smile looks like, which defeats the entire purpose of that theorem. For the actual market-implied (smile-consistent) risk-neutral density, see `get_risk_neutral_density`, which uses this same second-derivative relationship but applied to a volatility surface calibrated to real market option prices instead of a flat assumption.

The formula is as follows:

$$
\text{Partial Derivative} \;(\text{PD}) = e^{- r \cdot t} \cdot \frac{1}{K} \cdot \frac{1}{\sqrt{2 \cdot \pi \cdot \sigma^{2} \cdot t}} \cdot e^{- \frac{1}{2 \cdot \sigma^{2} \cdot t} \cdot \left(\ln\left(\frac{K}{S}\right) - ((r - q) - (0.5 \cdot \sigma^{2})) \cdot t\right)^{2}}
$$

Where S is the stock price, K is the strike price, r is the risk free rate, q is the dividend yield, $$\sigma$$ is the volatility and t is the time to expiration. This expression is algebraically identical to $$e^{- r \cdot t} \cdot N' (d_{2}) / (K \cdot \sigma \cdot \sqrt{t})$$, i.e. to the Dual Gamma, since both are the second derivative of the option price with respect to the strike price.

**Also known as:** second strike derivative, lognormal risk-neutral density.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None which
means it will use the current dividend yield.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: the partial derivative values containing the tickers and strike prices as the index and the
time to expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["BAC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.options.get_partial_derivative(
    strike_price_range=0.2, strike_step_size=1
).loc["BAC", ["2026-01-07", "2026-01-14", "2026-01-28"]]
```

Which returns:

|   Strike Price |   2026-01-07 |   2026-01-14 |   2026-01-28 |
|---------------:|-------------:|-------------:|-------------:|
|             44 |       0      |       0      |       0.0014 |
|             45 |       0      |       0.0001 |       0.0032 |
|             46 |       0      |       0.0005 |       0.0066 |
|             47 |       0      |       0.0019 |       0.0124 |
|             48 |       0.0003 |       0.0056 |       0.0213 |
|             49 |       0.0017 |       0.014  |       0.0333 |
|             50 |       0.008  |       0.0296 |       0.0478 |
|             51 |       0.0269 |       0.0536 |       0.0635 |
|             52 |       0.0665 |       0.0833 |       0.0783 |
|             53 |       0.1241 |       0.1125 |       0.09   |
|             54 |       0.1768 |       0.1328 |       0.0967 |
|             55 |       0.1955 |       0.1382 |       0.0975 |
|             56 |       0.17   |       0.1275 |       0.0927 |
|             57 |       0.1178 |       0.105  |       0.0832 |
|             58 |       0.0657 |       0.0776 |       0.0708 |
|             59 |       0.0299 |       0.0518 |       0.0573 |
|             60 |       0.0112 |       0.0314 |       0.0441 |
|             61 |       0.0035 |       0.0173 |       0.0325 |
|             62 |       0.0009 |       0.0088 |       0.0229 |
|             63 |       0.0002 |       0.0041 |       0.0155 |
|             64 |       0      |       0.0018 |       0.0101 |
|             65 |       0      |       0.0007 |       0.0063 |

---

## collect_third_order_greeks
Calculate the third order Greeks of an option based on the Black Scholes Model: how the second order Greeks themselves respond to the price of the underlying asset, the volatility and time.

This will return the following Greeks per Strike Price and Expiration Date:

- Speed: measures the rate of change in Gamma with respect to changes in the underlying price.
- Zomma: measures the rate of change of gamma with respect to changes in volatility.
- Color: also referred to as gamma decay or DgammaDtime measures the rate of change of gamma over the passage of time.
- Ultima: measures the sensitivity of the option vomma with respect to change in volatility.

For a deeper explanation, please have a look at: [https://en.wikipedia.org/wiki/Greeks_(finance)](https://en.wikipedia.org/wiki/Greeks_(finance)){:target="_blank"} and the references to the literature as found on this page.

By default the stock price (the traded close), risk free rate, dividend yield and volatility of the most recent date are used; changing the start date prices the option as of that date instead. The volatility is the annualized standard deviation of the daily returns over the year before that date and the dividend yield the dividends of the 365 days up to that date relative to its close, so an earlier start date only uses what was known on that date. The exception is a date in the first year of the price history: without a full year before it, it takes the dividend yield of the first date that has one.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None which
means it will use the current dividend yield.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: the third order greeks values containing the tickers and strike prices as the index and the
time to expiration and greeks as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["MU", "AMZN"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.options.collect_third_order_greeks().loc["MU"]
```

Which returns:

|   Strike Price |   (Period('2026-01-01', 'D'), 'Speed') |   (Period('2026-01-01', 'D'), 'Zomma') |   (Period('2026-01-01', 'D'), 'Color') |   (Period('2026-01-01', 'D'), 'Ultima') |   (Period('2026-01-02', 'D'), 'Speed') |   (Period('2026-01-02', 'D'), 'Zomma') |   (Period('2026-01-02', 'D'), 'Color') |   (Period('2026-01-02', 'D'), 'Ultima') |   (Period('2026-01-03', 'D'), 'Speed') |   (Period('2026-01-03', 'D'), 'Zomma') |   (Period('2026-01-03', 'D'), 'Color') |   (Period('2026-01-03', 'D'), 'Ultima') |   (Period('2026-01-04', 'D'), 'Speed') |   (Period('2026-01-04', 'D'), 'Zomma') |   (Period('2026-01-04', 'D'), 'Color') |   (Period('2026-01-04', 'D'), 'Ultima') |   (Period('2026-01-05', 'D'), 'Speed') |   (Period('2026-01-05', 'D'), 'Zomma') |   (Period('2026-01-05', 'D'), 'Color') |   (Period('2026-01-05', 'D'), 'Ultima') |   (Period('2026-01-06', 'D'), 'Speed') |   (Period('2026-01-06', 'D'), 'Zomma') |   (Period('2026-01-06', 'D'), 'Color') |   (Period('2026-01-06', 'D'), 'Ultima') |   (Period('2026-01-07', 'D'), 'Speed') |   (Period('2026-01-07', 'D'), 'Zomma') |   (Period('2026-01-07', 'D'), 'Color') |   (Period('2026-01-07', 'D'), 'Ultima') |   (Period('2026-01-08', 'D'), 'Speed') |   (Period('2026-01-08', 'D'), 'Zomma') |   (Period('2026-01-08', 'D'), 'Color') |   (Period('2026-01-08', 'D'), 'Ultima') |   (Period('2026-01-09', 'D'), 'Speed') |   (Period('2026-01-09', 'D'), 'Zomma') |   (Period('2026-01-09', 'D'), 'Color') |   (Period('2026-01-09', 'D'), 'Ultima') |   (Period('2026-01-10', 'D'), 'Speed') |   (Period('2026-01-10', 'D'), 'Zomma') |   (Period('2026-01-10', 'D'), 'Color') |   (Period('2026-01-10', 'D'), 'Ultima') |   (Period('2026-01-11', 'D'), 'Speed') |   (Period('2026-01-11', 'D'), 'Zomma') |   (Period('2026-01-11', 'D'), 'Color') |   (Period('2026-01-11', 'D'), 'Ultima') |   (Period('2026-01-12', 'D'), 'Speed') |   (Period('2026-01-12', 'D'), 'Zomma') |   (Period('2026-01-12', 'D'), 'Color') |   (Period('2026-01-12', 'D'), 'Ultima') |   (Period('2026-01-13', 'D'), 'Speed') |   (Period('2026-01-13', 'D'), 'Zomma') |   (Period('2026-01-13', 'D'), 'Color') |   (Period('2026-01-13', 'D'), 'Ultima') |   (Period('2026-01-14', 'D'), 'Speed') |   (Period('2026-01-14', 'D'), 'Zomma') |   (Period('2026-01-14', 'D'), 'Color') |   (Period('2026-01-14', 'D'), 'Ultima') |   (Period('2026-01-15', 'D'), 'Speed') |   (Period('2026-01-15', 'D'), 'Zomma') |   (Period('2026-01-15', 'D'), 'Color') |   (Period('2026-01-15', 'D'), 'Ultima') |   (Period('2026-01-16', 'D'), 'Speed') |   (Period('2026-01-16', 'D'), 'Zomma') |   (Period('2026-01-16', 'D'), 'Color') |   (Period('2026-01-16', 'D'), 'Ultima') |   (Period('2026-01-17', 'D'), 'Speed') |   (Period('2026-01-17', 'D'), 'Zomma') |   (Period('2026-01-17', 'D'), 'Color') |   (Period('2026-01-17', 'D'), 'Ultima') |   (Period('2026-01-18', 'D'), 'Speed') |   (Period('2026-01-18', 'D'), 'Zomma') |   (Period('2026-01-18', 'D'), 'Color') |   (Period('2026-01-18', 'D'), 'Ultima') |   (Period('2026-01-19', 'D'), 'Speed') |   (Period('2026-01-19', 'D'), 'Zomma') |   (Period('2026-01-19', 'D'), 'Color') |   (Period('2026-01-19', 'D'), 'Ultima') |   (Period('2026-01-20', 'D'), 'Speed') |   (Period('2026-01-20', 'D'), 'Zomma') |   (Period('2026-01-20', 'D'), 'Color') |   (Period('2026-01-20', 'D'), 'Ultima') |   (Period('2026-01-21', 'D'), 'Speed') |   (Period('2026-01-21', 'D'), 'Zomma') |   (Period('2026-01-21', 'D'), 'Color') |   (Period('2026-01-21', 'D'), 'Ultima') |   (Period('2026-01-22', 'D'), 'Speed') |   (Period('2026-01-22', 'D'), 'Zomma') |   (Period('2026-01-22', 'D'), 'Color') |   (Period('2026-01-22', 'D'), 'Ultima') |   (Period('2026-01-23', 'D'), 'Speed') |   (Period('2026-01-23', 'D'), 'Zomma') |   (Period('2026-01-23', 'D'), 'Color') |   (Period('2026-01-23', 'D'), 'Ultima') |   (Period('2026-01-24', 'D'), 'Speed') |   (Period('2026-01-24', 'D'), 'Zomma') |   (Period('2026-01-24', 'D'), 'Color') |   (Period('2026-01-24', 'D'), 'Ultima') |   (Period('2026-01-25', 'D'), 'Speed') |   (Period('2026-01-25', 'D'), 'Zomma') |   (Period('2026-01-25', 'D'), 'Color') |   (Period('2026-01-25', 'D'), 'Ultima') |   (Period('2026-01-26', 'D'), 'Speed') |   (Period('2026-01-26', 'D'), 'Zomma') |   (Period('2026-01-26', 'D'), 'Color') |   (Period('2026-01-26', 'D'), 'Ultima') |   (Period('2026-01-27', 'D'), 'Speed') |   (Period('2026-01-27', 'D'), 'Zomma') |   (Period('2026-01-27', 'D'), 'Color') |   (Period('2026-01-27', 'D'), 'Ultima') |   (Period('2026-01-28', 'D'), 'Speed') |   (Period('2026-01-28', 'D'), 'Zomma') |   (Period('2026-01-28', 'D'), 'Color') |   (Period('2026-01-28', 'D'), 'Ultima') |   (Period('2026-01-29', 'D'), 'Speed') |   (Period('2026-01-29', 'D'), 'Zomma') |   (Period('2026-01-29', 'D'), 'Color') |   (Period('2026-01-29', 'D'), 'Ultima') |
|---------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|---------------------------------------:|---------------------------------------:|---------------------------------------:|----------------------------------------:|
|            215 |                                 0      |                                 0      |                                 0      |                                  0      |                                 0      |                                 0      |                                 0      |                                  0.0002 |                                 0      |                                 0      |                                -0.0001 |                                  0.0462 |                                 0      |                                 0      |                                -0.0012 |                                  0.6517 |                                 0      |                                 0.0002 |                                -0.0046 |                                  2.8961 |                                 0      |                                 0.0005 |                                -0.01   |                                  7.3099 |                                 0      |                                 0.001  |                                -0.0163 |                                 13.4344 |                                 0      |                                 0.0016 |                                -0.0224 |                                 20.3143 |                                 0      |                                 0.0022 |                                -0.0277 |                                 27.0161 |                                 0      |                                 0.0028 |                                -0.0318 |                                 32.8626 |                                 0      |                                 0.0034 |                                -0.0346 |                                 37.4632 |                                 0      |                                 0.0039 |                                -0.0364 |                                 40.6573 |                                 0      |                                 0.0043 |                                -0.0373 |                                 42.4422 |                                 0      |                                 0.0047 |                                -0.0374 |                                 42.9098 |                                -0.0001 |                                 0.0049 |                                -0.037  |                                 42.202  |                                -0.0001 |                                 0.0052 |                                -0.0362 |                                 40.4798 |                                -0.0001 |                                 0.0053 |                                -0.0351 |                                 37.9056 |                                -0.0001 |                                 0.0054 |                                -0.0338 |                                 34.6322 |                                -0.0001 |                                 0.0055 |                                -0.0323 |                                 30.7979 |                                -0.0001 |                                 0.0055 |                                -0.0308 |                                 26.5244 |                                -0.0001 |                                 0.0055 |                                -0.0292 |                                 21.9169 |                                -0.0001 |                                 0.0055 |                                -0.0277 |                                 17.0648 |                                -0.0001 |                                 0.0054 |                                -0.0262 |                                 12.0433 |                                -0.0001 |                                 0.0053 |                                -0.0247 |                                  6.9149 |                                -0.0001 |                                 0.0052 |                                -0.0232 |                                  1.7314 |                                -0.0001 |                                 0.0051 |                                -0.0219 |                                 -3.465  |                                -0.0001 |                                 0.005  |                                -0.0205 |                                 -8.6399 |                                -0.0001 |                                 0.0049 |                                -0.0193 |                                -13.7657 |                                -0.0001 |                                 0.0048 |                                -0.0181 |                                -18.8205 |
|            220 |                                 0      |                                 0      |                                 0      |                                  0      |                                 0      |                                 0      |                                 0      |                                  0.0023 |                                 0      |                                 0      |                                -0.0007 |                                  0.2279 |                                 0      |                                 0.0002 |                                -0.0045 |                                  1.9556 |                                 0      |                                 0.0005 |                                -0.0124 |                                  6.4192 |                                 0      |                                 0.0012 |                                -0.0222 |                                 13.1727 |                                 0      |                                 0.0019 |                                -0.0315 |                                 20.7745 |                                 0      |                                 0.0028 |                                -0.0389 |                                 27.857  |                                 0      |                                 0.0035 |                                -0.0442 |                                 33.5461 |                                 0      |                                 0.0042 |                                -0.0473 |                                 37.4484 |                                -0.0001 |                                 0.0048 |                                -0.0488 |                                 39.5045 |                                -0.0001 |                                 0.0052 |                                -0.0489 |                                 39.8469 |                                -0.0001 |                                 0.0056 |                                -0.0481 |                                 38.6988 |                                -0.0001 |                                 0.0058 |                                -0.0465 |                                 36.3117 |                                -0.0001 |                                 0.006  |                                -0.0446 |                                 32.9304 |                                -0.0001 |                                 0.0061 |                                -0.0424 |                                 28.7768 |                                -0.0001 |                                 0.0061 |                                -0.04   |                                 24.0431 |                                -0.0001 |                                 0.0061 |                                -0.0376 |                                 18.8907 |                                -0.0001 |                                 0.006  |                                -0.0352 |                                 13.453  |                                -0.0001 |                                 0.0059 |                                -0.0329 |                                  7.838  |                                -0.0001 |                                 0.0058 |                                -0.0307 |                                  2.1323 |                                -0.0001 |                                 0.0057 |                                -0.0285 |                                 -3.5957 |                                -0.0001 |                                 0.0055 |                                -0.0265 |                                 -9.2924 |                                -0.0001 |                                 0.0053 |                                -0.0246 |                                -14.9166 |                                -0.0001 |                                 0.0052 |                                -0.0228 |                                -20.4368 |                                -0.0001 |                                 0.005  |                                -0.0211 |                                -25.8298 |                                -0.0001 |                                 0.0048 |                                -0.0195 |                                -31.0786 |                                -0.0001 |                                 0.0046 |                                -0.018  |                                -36.1715 |                                -0.0001 |                                 0.0044 |                                -0.0167 |                                -41.1007 |
|            225 |                                 0      |                                 0      |                                 0      |                                  0      |                                 0      |                                 0      |                                -0.0001 |                                  0.0214 |                                 0      |                                 0.0001 |                                -0.0032 |                                  0.8894 |                                 0      |                                 0.0005 |                                -0.014  |                                  4.8702 |                                 0      |                                 0.0013 |                                -0.0293 |                                 12.1181 |                                 0      |                                 0.0023 |                                -0.0439 |                                 20.5173 |                                 0      |                                 0.0034 |                                -0.0548 |                                 27.9778 |                                 0      |                                 0.0044 |                                -0.0615 |                                 33.339  |                                -0.0001 |                                 0.0051 |                                -0.0646 |                                 36.2508 |                                -0.0001 |                                 0.0058 |                                -0.065  |                                 36.839  |                                -0.0001 |                                 0.0062 |                                -0.0636 |                                 35.4428 |                                -0.0001 |                                 0.0065 |                                -0.061  |                                 32.4608 |                                -0.0001 |                                 0.0067 |                                -0.0577 |                                 28.2735 |                                -0.0001 |                                 0.0067 |                                -0.054  |                                 23.212  |                                -0.0001 |                                 0.0067 |                                -0.0502 |                                 17.5493 |                                -0.0001 |                                 0.0066 |                                -0.0464 |                                 11.5032 |                                -0.0001 |                                 0.0065 |                                -0.0427 |                                  5.2435 |                                -0.0001 |                                 0.0063 |                                -0.0392 |                                 -1.1    |                                -0.0001 |                                 0.0061 |                                -0.0359 |                                 -7.43   |                                -0.0001 |                                 0.0059 |                                -0.0328 |                                -13.6744 |                                -0.0001 |                                 0.0057 |                                -0.03   |                                -19.7812 |                                -0.0001 |                                 0.0055 |                                -0.0273 |                                -25.7141 |                                -0.0001 |                                 0.0052 |                                -0.0249 |                                -31.4482 |                                -0.0001 |                                 0.005  |                                -0.0227 |                                -36.9681 |                                -0.0001 |                                 0.0047 |                                -0.0206 |                                -42.2649 |                                -0.0001 |                                 0.0045 |                                -0.0187 |                                -47.3352 |                                -0.0001 |                                 0.0043 |                                -0.017  |                                -52.179  |                                -0.0001 |                                 0.004  |                                -0.0155 |                                -56.7994 |                                -0.0001 |                                 0.0038 |                                -0.014  |                                -61.2015 |
|            230 |                                 0      |                                 0      |                                 0      |                                  0      |                                 0      |                                 0      |                                -0.0009 |                                  0.1466 |                                 0      |                                 0.0003 |                                -0.0126 |                                  2.7617 |                                 0      |                                 0.0013 |                                -0.0367 |                                 10.0594 |                                 0      |                                 0.0027 |                                -0.0608 |                                 19.3768 |                                -0.0001 |                                 0.0041 |                                -0.0774 |                                 27.319  |                                -0.0001 |                                 0.0053 |                                -0.086  |                                 32.2265 |                                -0.0001 |                                 0.0063 |                                -0.0883 |                                 33.8626 |                                -0.0001 |                                 0.0069 |                                -0.0865 |                                 32.6687 |                                -0.0001 |                                 0.0073 |                                -0.0821 |                                 29.2873 |                                -0.0001 |                                 0.0075 |                                -0.0765 |                                 24.3399 |                                -0.0001 |                                 0.0075 |                                -0.0703 |                                 18.3477 |                                -0.0001 |                                 0.0074 |                                -0.064  |                                 11.7171 |                                -0.0001 |                                 0.0073 |                                -0.0579 |                                  4.7523 |                                -0.0001 |                                 0.007  |                                -0.0522 |                                 -2.326  |                                -0.0001 |                                 0.0068 |                                -0.0469 |                                 -9.362  |                                -0.0001 |                                 0.0064 |                                -0.042  |                                -16.2482 |                                -0.0001 |                                 0.0061 |                                -0.0376 |                                -22.9134 |                                -0.0001 |                                 0.0058 |                                -0.0336 |                                -29.3124 |                                -0.0001 |                                 0.0055 |                                -0.03   |                                -35.4191 |                                -0.0001 |                                 0.0051 |                                -0.0267 |                                -41.2206 |                                -0.0001 |                                 0.0048 |                                -0.0238 |                                -46.7137 |                                -0.0001 |                                 0.0045 |                                -0.0212 |                                -51.9017 |                                -0.0001 |                                 0.0042 |                                -0.0188 |                                -56.7925 |                                -0.0001 |                                 0.0039 |                                -0.0167 |                                -61.3966 |                                -0.0001 |                                 0.0036 |                                -0.0148 |                                -65.7265 |                                -0.0001 |                                 0.0033 |                                -0.013  |                                -69.7957 |                                -0.0001 |                                 0.0031 |                                -0.0115 |                                -73.618  |                                -0.0001 |                                 0.0028 |                                -0.0101 |                                -77.2074 |
|            235 |                                 0      |                                 0      |                                 0      |                                  0.0003 |                                 0      |                                 0.0001 |                                -0.006  |                                  0.7369 |                                 0      |                                 0.0011 |                                -0.0402 |                                  6.8209 |                                 0      |                                 0.0029 |                                -0.0824 |                                 17.1105 |                                -0.0001 |                                 0.0049 |                                -0.1103 |                                 25.8464 |                                -0.0001 |                                 0.0064 |                                -0.1216 |                                 30.285  |                                -0.0001 |                                 0.0075 |                                -0.1215 |                                 30.3906 |                                -0.0001 |                                 0.0082 |                                -0.115  |                                 27.1327 |                                -0.0001 |                                 0.0084 |                                -0.1054 |                                 21.593  |                                -0.0001 |                                 0.0084 |                                -0.0947 |                                 14.6651 |                                -0.0001 |                                 0.0083 |                                -0.0841 |                                  7.0056 |                                -0.0001 |                                 0.008  |                                -0.0741 |                                 -0.9318 |                                -0.0001 |                                 0.0076 |                                -0.0649 |                                 -8.8472 |                                -0.0001 |                                 0.0071 |                                -0.0567 |                                -16.55   |                                -0.0001 |                                 0.0067 |                                -0.0494 |                                -23.9252 |                                -0.0001 |                                 0.0062 |                                -0.043  |                                -30.9089 |                                -0.0001 |                                 0.0058 |                                -0.0373 |                                -37.4714 |                                -0.0001 |                                 0.0053 |                                -0.0324 |                                -43.6049 |                                -0.0001 |                                 0.0049 |                                -0.028  |                                -49.3159 |                                -0.0001 |                                 0.0045 |                                -0.0242 |                                -54.6196 |                                -0.0001 |                                 0.0041 |                                -0.0208 |                                -59.5361 |                                -0.0001 |                                 0.0037 |                                -0.0178 |                                -64.0882 |                                -0.0001 |                                 0.0033 |                                -0.0152 |                                -68.2999 |                                -0.0001 |                                 0.003  |                                -0.013  |                                -72.1949 |                                -0.0001 |                                 0.0027 |                                -0.0109 |                                -75.7964 |                                -0.0001 |                                 0.0023 |                                -0.0091 |                                -79.1265 |                                -0.0001 |                                 0.0021 |                                -0.0076 |                                -82.2061 |                                -0.0001 |                                 0.0018 |                                -0.0062 |                                -85.0546 |                                -0.0001 |                                 0.0015 |                                -0.0049 |                                -87.6902 |
|            240 |                                 0      |                                 0      |                                -0.0002 |                                  0.0079 |                                 0      |                                 0.0005 |                                -0.0292 |                                  2.7239 |                                 0      |                                 0.0028 |                                -0.1053 |                                 13.2964 |                                -0.0001 |                                 0.0056 |                                -0.1584 |                                 23.4961 |                                -0.0001 |                                 0.0077 |                                -0.1751 |                                 27.6952 |                                -0.0002 |                                 0.009  |                                -0.1694 |                                 26.08   |                                -0.0002 |                                 0.0095 |                                -0.1535 |                                 20.5215 |                                -0.0002 |                                 0.0096 |                                -0.1344 |                                 12.7461 |                                -0.0002 |                                 0.0093 |                                -0.1155 |                                  3.965  |                                -0.0002 |                                 0.0088 |                                -0.0982 |                                 -5.0605 |                                -0.0002 |                                 0.0082 |                                -0.083  |                                -13.8837 |                                -0.0002 |                                 0.0075 |                                -0.0698 |                                -22.2608 |                                -0.0002 |                                 0.0069 |                                -0.0586 |                                -30.0726 |                                -0.0002 |                                 0.0062 |                                -0.049  |                                -37.275  |                                -0.0002 |                                 0.0056 |                                -0.0409 |                                -43.8674 |                                -0.0002 |                                 0.005  |                                -0.034  |                                -49.8736 |                                -0.0002 |                                 0.0044 |                                -0.0281 |                                -55.3296 |                                -0.0002 |                                 0.0039 |                                -0.0232 |                                -60.2772 |                                -0.0001 |                                 0.0034 |                                -0.0189 |                                -64.7595 |                                -0.0001 |                                 0.0029 |                                -0.0153 |                                -68.8186 |                                -0.0001 |                                 0.0025 |                                -0.0122 |                                -72.4942 |                                -0.0001 |                                 0.0021 |                                -0.0095 |                                -75.8232 |                                -0.0001 |                                 0.0017 |                                -0.0072 |                                -78.8393 |                                -0.0001 |                                 0.0014 |                                -0.0053 |                                -81.5732 |                                -0.0001 |                                 0.0011 |                                -0.0036 |                                -84.0525 |                                -0.0001 |                                 0.0007 |                                -0.0021 |                                -86.3021 |                                -0.0001 |                                 0.0005 |                                -0.0008 |                                -88.3441 |                                -0.0001 |                                 0.0002 |                                 0.0003 |                                -90.1987 |                                -0.0001 |                                 0      |                                 0.0012 |                                -91.8837 |
|            245 |                                 0      |                                 0      |                                -0.0028 |                                  0.107  |                                 0      |                                 0.0019 |                                -0.1076 |                                  7.3596 |                                -0.0001 |                                 0.006  |                                -0.2274 |                                 19.9799 |                                -0.0002 |                                 0.0092 |                                -0.2596 |                                 24.7341 |                                -0.0002 |                                 0.0107 |                                -0.2416 |                                 21.3396 |                                -0.0002 |                                 0.011  |                                -0.2069 |                                 13.2918 |                                -0.0002 |                                 0.0106 |                                -0.1707 |                                  3.3131 |                                -0.0002 |                                 0.0099 |                                -0.1383 |                                 -7.0298 |                                -0.0002 |                                 0.009  |                                -0.111  |                                -16.9456 |                                -0.0002 |                                 0.008  |                                -0.0886 |                                -26.0822 |                                -0.0002 |                                 0.007  |                                -0.0705 |                                -34.3207 |                                -0.0002 |                                 0.0061 |                                -0.0558 |                                -41.6595 |                                -0.0002 |                                 0.0052 |                                -0.0438 |                                -48.1522 |                                -0.0002 |                                 0.0044 |                                -0.0342 |                                -53.875  |                                -0.0002 |                                 0.0037 |                                -0.0263 |                                -58.9102 |                                -0.0002 |                                 0.003  |                                -0.0199 |                                -63.3373 |                                -0.0002 |                                 0.0024 |                                -0.0146 |                                -67.23   |                                -0.0002 |                                 0.0019 |                                -0.0102 |                                -70.654  |                                -0.0002 |                                 0.0014 |                                -0.0067 |                                -73.6678 |                                -0.0002 |                                 0.0009 |                                -0.0037 |                                -76.3224 |                                -0.0001 |                                 0.0005 |                                -0.0012 |                                -78.6621 |                                -0.0001 |                                 0.0001 |                                 0.0008 |                                -80.7256 |                                -0.0001 |                                -0.0002 |                                 0.0025 |                                -82.5462 |                                -0.0001 |                                -0.0006 |                                 0.0039 |                                -84.1532 |                                -0.0001 |                                -0.0008 |                                 0.0051 |                                -85.5716 |                                -0.0001 |                                -0.0011 |                                 0.0061 |                                -86.8235 |                                -0.0001 |                                -0.0014 |                                 0.0069 |                                -87.928  |                                -0.0001 |                                -0.0016 |                                 0.0076 |                                -88.9017 |                                -0.0001 |                                -0.0018 |                                 0.0081 |                                -89.7592 |
|            250 |                                 0      |                                 0.0003 |                                -0.0306 |                                  0.8572 |                                -0.0001 |                                 0.0054 |                                -0.3043 |                                 14.2006 |                                -0.0002 |                                 0.0106 |                                -0.4024 |                                 21.678  |                                -0.0003 |                                 0.0127 |                                -0.3589 |                                 16.771  |                                -0.0003 |                                 0.0126 |                                -0.2843 |                                  6.0745 |                                -0.0003 |                                 0.0115 |                                -0.2159 |                                 -5.9652 |                                -0.0003 |                                 0.0101 |                                -0.1611 |                                -17.4028 |                                -0.0003 |                                 0.0086 |                                -0.1192 |                                -27.5629 |                                -0.0003 |                                 0.0071 |                                -0.0875 |                                -36.3189 |                                -0.0003 |                                 0.0058 |                                -0.0635 |                                -43.7584 |                                -0.0003 |                                 0.0046 |                                -0.0454 |                                -50.0391 |                                -0.0002 |                                 0.0036 |                                -0.0315 |                                -55.3289 |                                -0.0002 |                                 0.0026 |                                -0.0208 |                                -59.7821 |                                -0.0002 |                                 0.0018 |                                -0.0126 |                                -63.5334 |                                -0.0002 |                                 0.0011 |                                -0.0062 |                                -66.6964 |                                -0.0002 |                                 0.0004 |                                -0.0012 |                                -69.366  |                                -0.0002 |                                -0.0001 |                                 0.0027 |                                -71.6207 |                                -0.0002 |                                -0.0006 |                                 0.0058 |                                -73.5258 |                                -0.0002 |                                -0.0011 |                                 0.0082 |                                -75.1352 |                                -0.0002 |                                -0.0015 |                                 0.01   |                                -76.4938 |                                -0.0002 |                                -0.0018 |                                 0.0115 |                                -77.639  |                                -0.0001 |                                -0.0022 |                                 0.0126 |                                -78.6019 |                                -0.0001 |                                -0.0024 |                                 0.0135 |                                -79.4087 |                                -0.0001 |                                -0.0027 |                                 0.0142 |                                -80.0814 |                                -0.0001 |                                -0.0029 |                                 0.0146 |                                -80.6388 |                                -0.0001 |                                -0.0031 |                                 0.015  |                                -81.0966 |                                -0.0001 |                                -0.0033 |                                 0.0152 |                                -81.4682 |                                -0.0001 |                                -0.0035 |                                 0.0154 |                                -81.7651 |                                -0.0001 |                                -0.0036 |                                 0.0154 |                                -81.9973 |
|            255 |                                 0      |                                 0.0019 |                                -0.2109 |                                  4.0061 |                                -0.0003 |                                 0.0115 |                                -0.655  |                                 18.248  |                                -0.0004 |                                 0.0152 |                                -0.5732 |                                 13.2126 |                                -0.0004 |                                 0.0144 |                                -0.4056 |                                 -0.3183 |                                -0.0004 |                                 0.0121 |                                -0.2723 |                                -14.2004 |                                -0.0004 |                                 0.0097 |                                -0.1794 |                                -26.0917 |                                -0.0004 |                                 0.0074 |                                -0.1163 |                                -35.7063 |                                -0.0003 |                                 0.0054 |                                -0.0733 |                                -43.3254 |                                -0.0003 |                                 0.0037 |                                -0.0437 |                                -49.3264 |                                -0.0003 |                                 0.0023 |                                -0.023  |                                -54.0499 |                                -0.0003 |                                 0.0011 |                                -0.0085 |                                -57.7723 |                                -0.0003 |                                 0.0001 |                                 0.0018 |                                -60.7097 |                                -0.0002 |                                -0.0008 |                                 0.0092 |                                -63.029  |                                -0.0002 |                                -0.0015 |                                 0.0144 |                                -64.8587 |                                -0.0002 |                                -0.0021 |                                 0.0182 |                                -66.2982 |                                -0.0002 |                                -0.0026 |                                 0.0208 |                                -67.425  |                                -0.0002 |                                -0.0031 |                                 0.0226 |                                -68.2995 |                                -0.0002 |                                -0.0035 |                                 0.0238 |                                -68.9696 |                                -0.0002 |                                -0.0038 |                                 0.0246 |                                -69.473  |                                -0.0002 |                                -0.0041 |                                 0.025  |                                -69.8402 |                                -0.0002 |                                -0.0044 |                                 0.0252 |                                -70.0954 |                                -0.0001 |                                -0.0046 |                                 0.0252 |                                -70.2585 |                                -0.0001 |                                -0.0048 |                                 0.0251 |                                -70.3456 |                                -0.0001 |                                -0.005  |                                 0.0248 |                                -70.3698 |                                -0.0001 |                                -0.0051 |                                 0.0245 |                                -70.342  |                                -0.0001 |                                -0.0052 |                                 0.0241 |                                -70.2711 |                                -0.0001 |                                -0.0053 |                                 0.0237 |                                -70.1646 |                                -0.0001 |                                -0.0054 |                                 0.0233 |                                -70.0287 |                                -0.0001 |                                -0.0055 |                                 0.0228 |                                -69.8686 |
|            260 |                                -0.0002 |                                 0.008  |                                -0.9052 |                                 10.3989 |                                -0.0006 |                                 0.0185 |                                -1.0466 |                                 11.7618 |                                -0.0006 |                                 0.0166 |                                -0.6246 |                                 -4.8618 |                                -0.0006 |                                 0.0123 |                                -0.3431 |                                -20.4075 |                                -0.0005 |                                 0.0082 |                                -0.1818 |                                -31.9627 |                                -0.0005 |                                 0.005  |                                -0.0893 |                                -40.1559 |                                -0.0004 |                                 0.0024 |                                -0.035  |                                -45.9201 |                                -0.0004 |                                 0.0004 |                                -0.0023 |                                -49.9803 |                                -0.0003 |                                -0.0011 |                                 0.0176 |                                -52.8433 |                                -0.0003 |                                -0.0023 |                                 0.0298 |                                -54.8557 |                                -0.0003 |                                -0.0033 |                                 0.0371 |                                -56.2561 |                                -0.0003 |                                -0.0041 |                                 0.0414 |                                -57.2105 |                                -0.0002 |                                -0.0047 |                                 0.0437 |                                -57.8362 |                                -0.0002 |                                -0.0052 |                                 0.0447 |                                -58.2172 |                                -0.0002 |                                -0.0056 |                                 0.0448 |                                -58.4149 |                                -0.0002 |                                -0.006  |                                 0.0444 |                                -58.4742 |                                -0.0002 |                                -0.0062 |                                 0.0437 |                                -58.4288 |                                -0.0002 |                                -0.0065 |                                 0.0427 |                                -58.3042 |                                -0.0002 |                                -0.0067 |                                 0.0415 |                                -58.1195 |                                -0.0002 |                                -0.0068 |                                 0.0403 |                                -57.8895 |                                -0.0001 |                                -0.0069 |                                 0.0391 |                                -57.6258 |                                -0.0001 |                                -0.007  |                                 0.0378 |                                -57.3371 |                                -0.0001 |                                -0.0071 |                                 0.0366 |                                -57.0304 |                                -0.0001 |                                -0.0072 |                                 0.0354 |                                -56.7112 |                                -0.0001 |                                -0.0072 |                                 0.0342 |                                -56.3837 |                                -0.0001 |                                -0.0073 |                                 0.033  |                                -56.0514 |                                -0.0001 |                                -0.0073 |                                 0.0319 |                                -55.7168 |                                -0.0001 |                                -0.0073 |                                 0.0309 |                                -55.3822 |                                -0.0001 |                                -0.0073 |                                 0.0298 |                                -55.0491 |
|            265 |                                -0.0008 |                                 0.0208 |                                -2.3611 |                                 12.3941 |                                -0.001  |                                 0.0202 |                                -1.1439 |                                 -6.1306 |                                -0.0009 |                                 0.0116 |                                -0.4336 |                                -23.5887 |                                -0.0007 |                                 0.0051 |                                -0.1389 |                                -33.9313 |                                -0.0006 |                                 0.0007 |                                -0.0104 |                                -39.8485 |                                -0.0005 |                                -0.0023 |                                 0.0481 |                                -43.2327 |                                -0.0004 |                                -0.0043 |                                 0.0747 |                                -45.1384 |                                -0.0004 |                                -0.0058 |                                 0.086  |                                -46.1536 |                                -0.0003 |                                -0.0068 |                                 0.0896 |                                -46.6172 |                                -0.0003 |                                -0.0076 |                                 0.0891 |                                -46.732  |                                -0.0003 |                                -0.0081 |                                 0.0867 |                                -46.6233 |                                -0.0002 |                                -0.0085 |                                 0.0832 |                                -46.3707 |                                -0.0002 |                                -0.0088 |                                 0.0794 |                                -46.026  |                                -0.0002 |                                -0.009  |                                 0.0754 |                                -45.6238 |                                -0.0002 |                                -0.0092 |                                 0.0715 |                                -45.187  |                                -0.0002 |                                -0.0093 |                                 0.0677 |                                -44.7316 |                                -0.0002 |                                -0.0093 |                                 0.0642 |                                -44.2683 |                                -0.0002 |                                -0.0094 |                                 0.0608 |                                -43.8046 |                                -0.0001 |                                -0.0094 |                                 0.0577 |                                -43.3456 |                                -0.0001 |                                -0.0094 |                                 0.0548 |                                -42.8947 |                                -0.0001 |                                -0.0094 |                                 0.0521 |                                -42.4543 |                                -0.0001 |                                -0.0093 |                                 0.0496 |                                -42.026  |                                -0.0001 |                                -0.0093 |                                 0.0473 |                                -41.6105 |                                -0.0001 |                                -0.0093 |                                 0.0451 |                                -41.2085 |                                -0.0001 |                                -0.0092 |                                 0.0431 |                                -40.8201 |                                -0.0001 |                                -0.0092 |                                 0.0412 |                                -40.4454 |                                -0.0001 |                                -0.0091 |                                 0.0394 |                                -40.0842 |                                -0.0001 |                                -0.0091 |                                 0.0378 |                                -39.7362 |                                -0.0001 |                                -0.009  |                                 0.0362 |                                -39.4012 |
|            270 |                                -0.0018 |                                 0.0296 |                                -3.3565 |                                 -1.1373 |                                -0.0014 |                                 0.0102 |                                -0.568  |                                -22.8451 |                                -0.001  |                                -0.0007 |                                 0.0379 |                                -31.1609 |                                -0.0007 |                                -0.0062 |                                 0.1856 |                                -34.1545 |                                -0.0006 |                                -0.0092 |                                 0.2156 |                                -35.0519 |                                -0.0005 |                                -0.0108 |                                 0.2108 |                                -35.0499 |                                -0.0004 |                                -0.0118 |                                 0.1959 |                                -34.6438 |                                -0.0003 |                                -0.0123 |                                 0.1789 |                                -34.058  |                                -0.0003 |                                -0.0126 |                                 0.1625 |                                -33.4007 |                                -0.0003 |                                -0.0127 |                                 0.1476 |                                -32.7262 |                                -0.0002 |                                -0.0127 |                                 0.1344 |                                -32.062  |                                -0.0002 |                                -0.0127 |                                 0.1228 |                                -31.4219 |                                -0.0002 |                                -0.0126 |                                 0.1126 |                                -30.8125 |                                -0.0002 |                                -0.0125 |                                 0.1036 |                                -30.2362 |                                -0.0002 |                                -0.0124 |                                 0.0957 |                                -29.6932 |                                -0.0002 |                                -0.0122 |                                 0.0887 |                                -29.1828 |                                -0.0001 |                                -0.0121 |                                 0.0825 |                                -28.7034 |                                -0.0001 |                                -0.0119 |                                 0.077  |                                -28.2532 |                                -0.0001 |                                -0.0118 |                                 0.072  |                                -27.8305 |                                -0.0001 |                                -0.0116 |                                 0.0675 |                                -27.4333 |                                -0.0001 |                                -0.0115 |                                 0.0635 |                                -27.0599 |                                -0.0001 |                                -0.0113 |                                 0.0598 |                                -26.7087 |                                -0.0001 |                                -0.0112 |                                 0.0565 |                                -26.378  |                                -0.0001 |                                -0.0111 |                                 0.0535 |                                -26.0664 |                                -0.0001 |                                -0.0109 |                                 0.0507 |                                -25.7726 |                                -0.0001 |                                -0.0108 |                                 0.0482 |                                -25.4954 |                                -0.0001 |                                -0.0107 |                                 0.0458 |                                -25.2336 |                                -0.0001 |                                -0.0105 |                                 0.0437 |                                -24.9863 |                                -0.0001 |                                -0.0104 |                                 0.0417 |                                -24.7525 |
|            275 |                                -0.0028 |                                 0.0104 |                                -1.1551 |                                -17.2898 |                                -0.0014 |                                -0.0119 |                                 0.6953 |                                -23.4002 |                                -0.0009 |                                -0.0175 |                                 0.6759 |                                -23.3625 |                                -0.0006 |                                -0.0191 |                                 0.5505 |                                -22.3833 |                                -0.0005 |                                -0.0193 |                                 0.4456 |                                -21.3102 |                                -0.0004 |                                -0.0191 |                                 0.3664 |                                -20.3193 |                                -0.0003 |                                -0.0186 |                                 0.3069 |                                -19.4415 |                                -0.0003 |                                -0.0181 |                                 0.2613 |                                -18.6715 |                                -0.0002 |                                -0.0176 |                                 0.2257 |                                -17.9959 |                                -0.0002 |                                -0.0171 |                                 0.1974 |                                -17.4008 |                                -0.0002 |                                -0.0166 |                                 0.1744 |                                -16.8741 |                                -0.0002 |                                -0.0162 |                                 0.1556 |                                -16.4056 |                                -0.0002 |                                -0.0158 |                                 0.1399 |                                -15.9866 |                                -0.0002 |                                -0.0154 |                                 0.1266 |                                -15.6103 |                                -0.0001 |                                -0.015  |                                 0.1153 |                                -15.271  |                                -0.0001 |                                -0.0146 |                                 0.1056 |                                -14.9638 |                                -0.0001 |                                -0.0143 |                                 0.0971 |                                -14.6849 |                                -0.0001 |                                -0.014  |                                 0.0898 |                                -14.4309 |                                -0.0001 |                                -0.0137 |                                 0.0833 |                                -14.1989 |                                -0.0001 |                                -0.0134 |                                 0.0776 |                                -13.9866 |                                -0.0001 |                                -0.0132 |                                 0.0724 |                                -13.792  |                                -0.0001 |                                -0.0129 |                                 0.0679 |                                -13.6133 |                                -0.0001 |                                -0.0127 |                                 0.0638 |                                -13.449  |                                -0.0001 |                                -0.0125 |                                 0.06   |                                -13.2976 |                                -0.0001 |                                -0.0123 |                                 0.0567 |                                -13.1582 |                                -0.0001 |                                -0.0121 |                                 0.0536 |                                -13.0297 |                                -0.0001 |                                -0.0119 |                                 0.0508 |                                -12.9111 |                                -0.0001 |                                -0.0117 |                                 0.0483 |                                -12.8016 |                                -0.0001 |                                -0.0115 |                                 0.0459 |                                -12.7007 |
|            280 |                                -0.0024 |                                -0.0372 |                                 4.2755 |                                -11.6654 |                                -0.001  |                                -0.0362 |                                 2.0747 |                                 -9.6792 |                                -0.0006 |                                -0.0325 |                                 1.2421 |                                 -8.3993 |                                -0.0004 |                                -0.0295 |                                 0.8448 |                                 -7.5475 |                                -0.0003 |                                -0.0271 |                                 0.6212 |                                 -6.9398 |                                -0.0003 |                                -0.0252 |                                 0.4812 |                                 -6.4836 |                                -0.0002 |                                -0.0236 |                                 0.3868 |                                 -6.1286 |                                -0.0002 |                                -0.0223 |                                 0.3197 |                                 -5.845  |                                -0.0002 |                                -0.0212 |                                 0.2699 |                                 -5.6139 |                                -0.0002 |                                -0.0202 |                                 0.2319 |                                 -5.4229 |                                -0.0001 |                                -0.0194 |                                 0.202  |                                 -5.2632 |                                -0.0001 |                                -0.0186 |                                 0.178  |                                 -5.1285 |                                -0.0001 |                                -0.0179 |                                 0.1584 |                                 -5.0143 |                                -0.0001 |                                -0.0173 |                                 0.1422 |                                 -4.9171 |                                -0.0001 |                                -0.0168 |                                 0.1285 |                                 -4.8342 |                                -0.0001 |                                -0.0163 |                                 0.117  |                                 -4.7634 |                                -0.0001 |                                -0.0158 |                                 0.107  |                                 -4.703  |                                -0.0001 |                                -0.0154 |                                 0.0984 |                                 -4.6517 |                                -0.0001 |                                -0.015  |                                 0.0909 |                                 -4.6084 |                                -0.0001 |                                -0.0147 |                                 0.0843 |                                 -4.5721 |                                -0.0001 |                                -0.0143 |                                 0.0785 |                                 -4.5421 |                                -0.0001 |                                -0.014  |                                 0.0733 |                                 -4.5177 |                                -0.0001 |                                -0.0137 |                                 0.0686 |                                 -4.4983 |                                -0.0001 |                                -0.0135 |                                 0.0645 |                                 -4.4834 |                                -0.0001 |                                -0.0132 |                                 0.0607 |                                 -4.4728 |                                -0.0001 |                                -0.013  |                                 0.0573 |                                 -4.4658 |                                -0.0001 |                                -0.0127 |                                 0.0542 |                                 -4.4624 |                                -0.0001 |                                -0.0125 |                                 0.0514 |                                 -4.4622 |                                -0.0001 |                                -0.0123 |                                 0.0488 |                                 -4.4649 |
|            285 |                                -0.0004 |                                -0.068  |                                 7.7675 |                                 -0.1059 |                                -0.0002 |                                -0.0482 |                                 2.7508 |                                 -0.094  |                                -0.0002 |                                -0.0394 |                                 1.4983 |                                 -0.0977 |                                -0.0001 |                                -0.0341 |                                 0.9736 |                                 -0.1072 |                                -0.0001 |                                -0.0305 |                                 0.6969 |                                 -0.1202 |                                -0.0001 |                                -0.0279 |                                 0.5303 |                                 -0.1357 |                                -0.0001 |                                -0.0258 |                                 0.4209 |                                 -0.153  |                                -0.0001 |                                -0.0241 |                                 0.3446 |                                 -0.172  |                                -0.0001 |                                -0.0228 |                                 0.2889 |                                 -0.1924 |                                -0.0001 |                                -0.0216 |                                 0.2467 |                                 -0.2141 |                                -0.0001 |                                -0.0206 |                                 0.2139 |                                 -0.237  |                                -0.0001 |                                -0.0197 |                                 0.1878 |                                 -0.2609 |                                -0.0001 |                                -0.0189 |                                 0.1666 |                                 -0.2859 |                                -0.0001 |                                -0.0182 |                                 0.1491 |                                 -0.3118 |                                -0.0001 |                                -0.0176 |                                 0.1344 |                                 -0.3386 |                                -0.0001 |                                -0.0171 |                                 0.1221 |                                 -0.3663 |                                -0.0001 |                                -0.0166 |                                 0.1115 |                                 -0.3949 |                                -0.0001 |                                -0.0161 |                                 0.1023 |                                 -0.4243 |                                -0.0001 |                                -0.0157 |                                 0.0944 |                                 -0.4544 |                                -0.0001 |                                -0.0153 |                                 0.0874 |                                 -0.4854 |                                -0.0001 |                                -0.0149 |                                 0.0813 |                                 -0.517  |                                -0.0001 |                                -0.0146 |                                 0.0758 |                                 -0.5494 |                                -0.0001 |                                -0.0142 |                                 0.0709 |                                 -0.5824 |                                -0.0001 |                                -0.0139 |                                 0.0665 |                                 -0.6162 |                                 0      |                                -0.0137 |                                 0.0626 |                                 -0.6506 |                                 0      |                                -0.0134 |                                 0.059  |                                 -0.6856 |                                 0      |                                -0.0132 |                                 0.0558 |                                 -0.7213 |                                 0      |                                -0.0129 |                                 0.0529 |                                 -0.7576 |                                 0      |                                -0.0127 |                                 0.0502 |                                 -0.7945 |
|            290 |                                 0.0018 |                                -0.0469 |                                 5.3291 |                                 -8.8672 |                                 0.0006 |                                -0.0407 |                                 2.3116 |                                 -6.8532 |                                 0.0003 |                                -0.0354 |                                 1.3414 |                                 -5.7178 |                                 0.0002 |                                -0.0316 |                                 0.8991 |                                 -4.9793 |                                 0.0001 |                                -0.0288 |                                 0.6554 |                                 -4.452  |                                 0.0001 |                                -0.0266 |                                 0.5049 |                                 -4.0522 |                                 0      |                                -0.0249 |                                 0.4042 |                                 -3.7367 |                                 0      |                                -0.0234 |                                 0.3331 |                                 -3.4801 |                                 0      |                                -0.0222 |                                 0.2806 |                                 -3.2671 |                                 0      |                                -0.0211 |                                 0.2406 |                                 -3.0871 |                                 0      |                                -0.0202 |                                 0.2093 |                                 -2.9332 |                                 0      |                                -0.0194 |                                 0.1842 |                                 -2.8002 |                                 0      |                                -0.0187 |                                 0.1638 |                                 -2.6844 |                                 0      |                                -0.018  |                                 0.1469 |                                 -2.5829 |                                 0      |                                -0.0175 |                                 0.1327 |                                 -2.4936 |                                 0      |                                -0.0169 |                                 0.1206 |                                 -2.4146 |                                 0      |                                -0.0165 |                                 0.1103 |                                 -2.3447 |                                 0      |                                -0.016  |                                 0.1014 |                                 -2.2827 |                                 0      |                                -0.0156 |                                 0.0936 |                                 -2.2277 |                                 0      |                                -0.0152 |                                 0.0868 |                                 -2.1789 |                                 0      |                                -0.0149 |                                 0.0807 |                                 -2.1357 |                                 0      |                                -0.0145 |                                 0.0754 |                                 -2.0974 |                                 0      |                                -0.0142 |                                 0.0706 |                                 -2.0638 |                                 0      |                                -0.0139 |                                 0.0663 |                                 -2.0343 |                                 0      |                                -0.0137 |                                 0.0624 |                                 -2.0086 |                                 0      |                                -0.0134 |                                 0.0589 |                                 -1.9864 |                                 0      |                                -0.0132 |                                 0.0557 |                                 -1.9674 |                                 0      |                                -0.0129 |                                 0.0527 |                                 -1.9514 |                                 0      |                                -0.0127 |                                 0.0501 |                                 -1.9383 |
|            295 |                                 0.0027 |                                 0.0005 |                                -0.0931 |                                -18.806  |                                 0.0012 |                                -0.019  |                                 1.0689 |                                -21.4282 |                                 0.0006 |                                -0.0226 |                                 0.8532 |                                -20.2199 |                                 0.0004 |                                -0.0231 |                                 0.6528 |                                -18.7406 |                                 0.0003 |                                -0.0226 |                                 0.512  |                                -17.4118 |                                 0.0002 |                                -0.0219 |                                 0.4132 |                                -16.2709 |                                 0.0002 |                                -0.0211 |                                 0.3417 |                                -15.2942 |                                 0.0001 |                                -0.0203 |                                 0.2883 |                                -14.4521 |                                 0.0001 |                                -0.0196 |                                 0.2473 |                                -13.7192 |                                 0.0001 |                                -0.019  |                                 0.2151 |                                -13.0753 |                                 0.0001 |                                -0.0184 |                                 0.1893 |                                -12.5048 |                                 0      |                                -0.0178 |                                 0.1682 |                                -11.9953 |                                 0      |                                -0.0173 |                                 0.1508 |                                -11.5373 |                                 0      |                                -0.0168 |                                 0.1361 |                                -11.1231 |                                 0      |                                -0.0163 |                                 0.1237 |                                -10.7465 |                                 0      |                                -0.0159 |                                 0.1131 |                                -10.4025 |                                 0      |                                -0.0155 |                                 0.1039 |                                -10.0869 |                                 0      |                                -0.0152 |                                 0.0959 |                                 -9.7963 |                                 0      |                                -0.0149 |                                 0.0888 |                                 -9.5279 |                                 0      |                                -0.0145 |                                 0.0826 |                                 -9.2793 |                                 0      |                                -0.0142 |                                 0.0771 |                                 -9.0483 |                                 0      |                                -0.014  |                                 0.0721 |                                 -8.8333 |                                 0      |                                -0.0137 |                                 0.0677 |                                 -8.6326 |                                 0      |                                -0.0134 |                                 0.0637 |                                 -8.4451 |                                 0      |                                -0.0132 |                                 0.0601 |                                 -8.2695 |                                 0      |                                -0.013  |                                 0.0568 |                                 -8.1049 |                                 0      |                                -0.0128 |                                 0.0538 |                                 -7.9503 |                                 0      |                                -0.0126 |                                 0.0511 |                                 -7.805  |                                 0      |                                -0.0124 |                                 0.0486 |                                 -7.6682 |
|            300 |                                 0.0022 |                                 0.0289 |                                -3.3231 |                                 -7.8444 |                                 0.0013 |                                 0.0042 |                                -0.2538 |                                -26.4755 |                                 0.0008 |                                -0.0065 |                                 0.2387 |                                -31.5828 |                                 0.0006 |                                -0.0113 |                                 0.3162 |                                -32.6    |                                 0.0004 |                                -0.0136 |                                 0.306  |                                -32.2457 |                                 0.0003 |                                -0.0148 |                                 0.2769 |                                -31.4023 |                                 0.0002 |                                -0.0153 |                                 0.2463 |                                -30.3985 |                                 0.0002 |                                -0.0155 |                                 0.2186 |                                -29.3676 |                                 0.0002 |                                -0.0155 |                                 0.1947 |                                -28.3651 |                                 0.0001 |                                -0.0154 |                                 0.1742 |                                -27.4134 |                                 0.0001 |                                -0.0153 |                                 0.1568 |                                -26.5201 |                                 0.0001 |                                -0.0151 |                                 0.142  |                                -25.6858 |                                 0.0001 |                                -0.0149 |                                 0.1292 |                                -24.908  |                                 0.0001 |                                -0.0146 |                                 0.1182 |                                -24.1829 |                                 0.0001 |                                -0.0144 |                                 0.1086 |                                -23.5064 |                                 0      |                                -0.0142 |                                 0.1002 |                                -22.8744 |                                 0      |                                -0.014  |                                 0.0928 |                                -22.283  |                                 0      |                                -0.0137 |                                 0.0863 |                                -21.7287 |                                 0      |                                -0.0135 |                                 0.0805 |                                -21.2081 |                                 0      |                                -0.0133 |                                 0.0753 |                                -20.7185 |                                 0      |                                -0.0131 |                                 0.0706 |                                -20.2571 |                                 0      |                                -0.0129 |                                 0.0664 |                                -19.8217 |                                 0      |                                -0.0127 |                                 0.0626 |                                -19.4101 |                                 0      |                                -0.0125 |                                 0.0591 |                                -19.0204 |                                 0      |                                -0.0124 |                                 0.056  |                                -18.6511 |                                 0      |                                -0.0122 |                                 0.0531 |                                -18.3005 |                                 0      |                                -0.012  |                                 0.0504 |                                -17.9673 |                                 0      |                                -0.0119 |                                 0.048  |                                -17.6502 |                                 0      |                                -0.0117 |                                 0.0458 |                                -17.3482 |
|            305 |                                 0.0012 |                                 0.0282 |                                -3.2278 |                                  9.1553 |                                 0.0012 |                                 0.0187 |                                -1.083  |                                -15.6878 |                                 0.0009 |                                 0.0074 |                                -0.2912 |                                -30.891  |                                 0.0006 |                                 0.0003 |                                -0.0165 |                                -38.2668 |                                 0.0005 |                                -0.004  |                                 0.086  |                                -41.7381 |                                 0.0004 |                                -0.0068 |                                 0.1238 |                                -43.2291 |                                 0.0003 |                                -0.0085 |                                 0.1353 |                                -43.6692 |                                 0.0003 |                                -0.0097 |                                 0.1353 |                                -43.5318 |                                 0.0002 |                                -0.0105 |                                 0.1304 |                                -43.0714 |                                 0.0002 |                                -0.011  |                                 0.1235 |                                -42.4311 |                                 0.0002 |                                -0.0114 |                                 0.116  |                                -41.6942 |                                 0.0001 |                                -0.0116 |                                 0.1085 |                                -40.9103 |                                 0.0001 |                                -0.0118 |                                 0.1015 |                                -40.1097 |                                 0.0001 |                                -0.0118 |                                 0.0949 |                                -39.3108 |                                 0.0001 |                                -0.0119 |                                 0.0888 |                                -38.5249 |                                 0.0001 |                                -0.0118 |                                 0.0832 |                                -37.7587 |                                 0.0001 |                                -0.0118 |                                 0.0782 |                                -37.0161 |                                 0.0001 |                                -0.0118 |                                 0.0735 |                                -36.299  |                                 0.0001 |                                -0.0117 |                                 0.0693 |                                -35.6085 |                                 0      |                                -0.0116 |                                 0.0654 |                                -34.9444 |                                 0      |                                -0.0115 |                                 0.0618 |                                -34.3064 |                                 0      |                                -0.0114 |                                 0.0586 |                                -33.6937 |                                 0      |                                -0.0113 |                                 0.0556 |                                -33.1055 |                                 0      |                                -0.0112 |                                 0.0528 |                                -32.5408 |                                 0      |                                -0.0111 |                                 0.0503 |                                -31.9985 |                                 0      |                                -0.011  |                                 0.0479 |                                -31.4776 |                                 0      |                                -0.0109 |                                 0.0457 |                                -30.977  |                                 0      |                                -0.0108 |                                 0.0437 |                                -30.4958 |                                 0      |                                -0.0107 |                                 0.0418 |                                -30.0329 |
|            310 |                                 0.0005 |                                 0.0159 |                                -1.8152 |                                 14.1154 |                                 0.0008 |                                 0.0224 |                                -1.2862 |                                  2.4962 |                                 0.0008 |                                 0.0159 |                                -0.6122 |                                -18.04   |                                 0.0006 |                                 0.0093 |                                -0.2734 |                                -32.4401 |                                 0.0005 |                                 0.0044 |                                -0.1059 |                                -41.551  |                                 0.0004 |                                 0.0008 |                                -0.0198 |                                -47.2149 |                                 0.0004 |                                -0.0018 |                                 0.0257 |                                -50.6996 |                                 0.0003 |                                -0.0038 |                                 0.05   |                                -52.7898 |                                 0.0003 |                                -0.0052 |                                 0.0627 |                                -53.9701 |                                 0.0002 |                                -0.0063 |                                 0.0688 |                                -54.5454 |                                 0.0002 |                                -0.0071 |                                 0.0712 |                                -54.7122 |                                 0.0002 |                                -0.0077 |                                 0.0713 |                                -54.6002 |                                 0.0001 |                                -0.0082 |                                 0.0702 |                                -54.2971 |                                 0.0001 |                                -0.0086 |                                 0.0683 |                                -53.8626 |                                 0.0001 |                                -0.0089 |                                 0.066  |                                -53.3388 |                                 0.0001 |                                -0.0091 |                                 0.0635 |                                -52.7552 |                                 0.0001 |                                -0.0093 |                                 0.061  |                                -52.1328 |                                 0.0001 |                                -0.0094 |                                 0.0584 |                                -51.487  |                                 0.0001 |                                -0.0095 |                                 0.056  |                                -50.8286 |                                 0.0001 |                                -0.0096 |                                 0.0536 |                                -50.1658 |                                 0.0001 |                                -0.0096 |                                 0.0513 |                                -49.5044 |                                 0.0001 |                                -0.0097 |                                 0.0492 |                                -48.8485 |                                 0      |                                -0.0097 |                                 0.0471 |                                -48.2012 |                                 0      |                                -0.0097 |                                 0.0452 |                                -47.5646 |                                 0      |                                -0.0097 |                                 0.0433 |                                -46.9404 |                                 0      |                                -0.0096 |                                 0.0416 |                                -46.3295 |                                 0      |                                -0.0096 |                                 0.04   |                                -45.7325 |                                 0      |                                -0.0096 |                                 0.0384 |                                -45.1499 |                                 0      |                                -0.0096 |                                 0.037  |                                -44.5818 |
|            315 |                                 0.0002 |                                 0.0062 |                                -0.7113 |                                  9.4638 |                                 0.0005 |                                 0.0186 |                                -1.0681 |                                 16.2431 |                                 0.0006 |                                 0.0185 |                                -0.7095 |                                  0.1321 |                                 0.0005 |                                 0.0145 |                                -0.4214 |                                -17.5555 |                                 0.0005 |                                 0.0104 |                                -0.2429 |                                -31.5765 |                                 0.0004 |                                 0.0068 |                                -0.135  |                                -41.885  |                                 0.0004 |                                 0.004  |                                -0.0688 |                                -49.3073 |                                 0.0003 |                                 0.0017 |                                -0.0274 |                                -54.617  |                                 0.0003 |                                -0.0002 |                                -0.0011 |                                -58.3983 |                                 0.0002 |                                -0.0017 |                                 0.0158 |                                -61.0701 |                                 0.0002 |                                -0.0028 |                                 0.0267 |                                -62.9293 |                                 0.0002 |                                -0.0038 |                                 0.0336 |                                -64.1874 |                                 0.0002 |                                -0.0046 |                                 0.038  |                                -64.9967 |                                 0.0002 |                                -0.0052 |                                 0.0406 |                                -65.4679 |                                 0.0001 |                                -0.0058 |                                 0.042  |                                -65.6828 |                                 0.0001 |                                -0.0062 |                                 0.0425 |                                -65.7022 |                                 0.0001 |                                -0.0066 |                                 0.0425 |                                -65.5721 |                                 0.0001 |                                -0.0069 |                                 0.0421 |                                -65.3272 |                                 0.0001 |                                -0.0071 |                                 0.0415 |                                -64.9944 |                                 0.0001 |                                -0.0073 |                                 0.0406 |                                -64.5944 |                                 0.0001 |                                -0.0075 |                                 0.0397 |                                -64.1434 |                                 0.0001 |                                -0.0077 |                                 0.0387 |                                -63.6539 |                                 0.0001 |                                -0.0078 |                                 0.0376 |                                -63.1359 |                                 0.0001 |                                -0.0079 |                                 0.0366 |                                -62.5975 |                                 0.0001 |                                -0.008  |                                 0.0355 |                                -62.0447 |                                 0.0001 |                                -0.008  |                                 0.0344 |                                -61.4826 |                                 0      |                                -0.0081 |                                 0.0334 |                                -60.9151 |                                 0      |                                -0.0081 |                                 0.0324 |                                -60.3455 |                                 0      |                                -0.0082 |                                 0.0314 |                                -59.7764 |
|            320 |                                 0      |                                 0.0018 |                                -0.208  |                                  4.0675 |                                 0.0003 |                                 0.0124 |                                -0.7105 |                                 20.4355 |                                 0.0004 |                                 0.0168 |                                -0.6437 |                                 15.6615 |                                 0.0004 |                                 0.0161 |                                -0.4649 |                                  0.63   |                                 0.0004 |                                 0.0137 |                                -0.317  |                                -15.1564 |                                 0.0004 |                                 0.0109 |                                -0.212  |                                -28.7858 |                                 0.0003 |                                 0.0083 |                                -0.1397 |                                -39.8192 |                                 0.0003 |                                 0.006  |                                -0.09   |                                -48.5363 |                                 0.0003 |                                 0.0041 |                                -0.0555 |                                -55.3576 |                                 0.0002 |                                 0.0025 |                                -0.0312 |                                -60.674  |                                 0.0002 |                                 0.0011 |                                -0.014  |                                -64.8074 |                                 0.0002 |                                -0.0001 |                                -0.0016 |                                -68.0115 |                                 0.0002 |                                -0.0011 |                                 0.0072 |                                -70.4833 |                                 0.0002 |                                -0.0019 |                                 0.0136 |                                -72.3752 |                                 0.0002 |                                -0.0027 |                                 0.0182 |                                -73.8055 |                                 0.0001 |                                -0.0033 |                                 0.0215 |                                -74.8663 |                                 0.0001 |                                -0.0038 |                                 0.0239 |                                -75.6297 |                                 0.0001 |                                -0.0043 |                                 0.0255 |                                -76.1527 |                                 0.0001 |                                -0.0047 |                                 0.0265 |                                -76.4807 |                                 0.0001 |                                -0.005  |                                 0.0272 |                                -76.6498 |                                 0.0001 |                                -0.0053 |                                 0.0275 |                                -76.689  |                                 0.0001 |                                -0.0056 |                                 0.0277 |                                -76.6221 |                                 0.0001 |                                -0.0058 |                                 0.0276 |                                -76.4681 |                                 0.0001 |                                -0.006  |                                 0.0274 |                                -76.2428 |                                 0.0001 |                                -0.0062 |                                 0.0271 |                                -75.9591 |                                 0.0001 |                                -0.0063 |                                 0.0268 |                                -75.6275 |                                 0.0001 |                                -0.0065 |                                 0.0263 |                                -75.257  |                                 0.0001 |                                -0.0066 |                                 0.0259 |                                -74.8548 |                                 0      |                                -0.0067 |                                 0.0254 |                                -74.4271 |
|            325 |                                 0      |                                 0.0004 |                                -0.0471 |                                  1.2505 |                                 0.0001 |                                 0.007  |                                -0.3988 |                                 17.2785 |                                 0.0003 |                                 0.013  |                                -0.4987 |                                 24.0019 |                                 0.0003 |                                 0.015  |                                -0.4314 |                                 16.3753 |                                 0.0003 |                                 0.0145 |                                -0.3349 |                                  2.9038 |                                 0.0003 |                                 0.013  |                                -0.2502 |                                -11.395  |                                 0.0003 |                                 0.0111 |                                -0.1841 |                                -24.5228 |                                 0.0003 |                                 0.0092 |                                -0.1342 |                                -35.8895 |                                 0.0003 |                                 0.0074 |                                -0.097  |                                -45.4719 |                                 0.0002 |                                 0.0058 |                                -0.0692 |                                -53.4473 |                                 0.0002 |                                 0.0044 |                                -0.0482 |                                -60.0437 |                                 0.0002 |                                 0.0031 |                                -0.0323 |                                -65.4825 |                                 0.0002 |                                 0.002  |                                -0.0202 |                                -69.9586 |                                 0.0002 |                                 0.0011 |                                -0.011  |                                -73.6368 |                                 0.0002 |                                 0.0002 |                                -0.0038 |                                -76.6536 |                                 0.0001 |                                -0.0005 |                                 0.0017 |                                -79.1213 |                                 0.0001 |                                -0.0012 |                                 0.006  |                                -81.1318 |                                 0.0001 |                                -0.0017 |                                 0.0094 |                                -82.7604 |                                 0.0001 |                                -0.0023 |                                 0.0119 |                                -84.0691 |                                 0.0001 |                                -0.0027 |                                 0.0139 |                                -85.1088 |                                 0.0001 |                                -0.0031 |                                 0.0155 |                                -85.9217 |                                 0.0001 |                                -0.0035 |                                 0.0166 |                                -86.5427 |                                 0.0001 |                                -0.0038 |                                 0.0175 |                                -87.001  |                                 0.0001 |                                -0.0041 |                                 0.0181 |                                -87.3211 |                                 0.0001 |                                -0.0043 |                                 0.0186 |                                -87.5234 |                                 0.0001 |                                -0.0045 |                                 0.0189 |                                -87.6251 |                                 0.0001 |                                -0.0047 |                                 0.0191 |                                -87.641  |                                 0.0001 |                                -0.0049 |                                 0.0191 |                                -87.5835 |                                 0.0001 |                                -0.0051 |                                 0.0191 |                                -87.463  |
|            330 |                                 0      |                                 0.0001 |                                -0.0085 |                                  0.2902 |                                 0.0001 |                                 0.0034 |                                -0.194  |                                 11.4717 |                                 0.0002 |                                 0.009  |                                -0.3423 |                                 24.9764 |                                 0.0002 |                                 0.0124 |                                -0.3557 |                                 26.2306 |                                 0.0003 |                                 0.0135 |                                -0.3116 |                                 18.3284 |                                 0.0003 |                                 0.0133 |                                -0.2554 |                                  6.3315 |                                 0.0003 |                                 0.0123 |                                -0.2034 |                                 -6.6745 |                                 0.0003 |                                 0.011  |                                -0.1598 |                                -19.1847 |                                 0.0002 |                                 0.0096 |                                -0.1247 |                                -30.5727 |                                 0.0002 |                                 0.0082 |                                -0.0967 |                                -40.6498 |                                 0.0002 |                                 0.0069 |                                -0.0746 |                                -49.4309 |                                 0.0002 |                                 0.0057 |                                -0.0571 |                                -57.0173 |                                 0.0002 |                                 0.0047 |                                -0.0432 |                                -63.54   |                                 0.0002 |                                 0.0037 |                                -0.0321 |                                -69.1327 |                                 0.0002 |                                 0.0028 |                                -0.0232 |                                -73.9199 |                                 0.0002 |                                 0.002  |                                -0.016  |                                -78.0129 |                                 0.0001 |                                 0.0013 |                                -0.0102 |                                -81.5087 |                                 0.0001 |                                 0.0006 |                                -0.0055 |                                -84.491  |                                 0.0001 |                                 0      |                                -0.0017 |                                -87.0312 |                                 0.0001 |                                -0.0005 |                                 0.0014 |                                -89.1905 |                                 0.0001 |                                -0.001  |                                 0.0039 |                                -91.0207 |                                 0.0001 |                                -0.0014 |                                 0.006  |                                -92.5662 |                                 0.0001 |                                -0.0018 |                                 0.0077 |                                -93.8649 |                                 0.0001 |                                -0.0022 |                                 0.0091 |                                -94.9491 |                                 0.0001 |                                -0.0025 |                                 0.0102 |                                -95.8465 |                                 0.0001 |                                -0.0028 |                                 0.0111 |                                -96.5811 |                                 0.0001 |                                -0.003  |                                 0.0118 |                                -97.1732 |                                 0.0001 |                                -0.0033 |                                 0.0124 |                                -97.6407 |                                 0.0001 |                                -0.0035 |                                 0.0128 |                                -97.9989 |
|            335 |                                 0      |                                 0      |                                -0.0012 |                                  0.0526 |                                 0      |                                 0.0015 |                                -0.0833 |                                  6.3455 |                                 0.0001 |                                 0.0056 |                                -0.2125 |                                 21.1018 |                                 0.0001 |                                 0.0093 |                                -0.2675 |                                 29.558  |                                 0.0002 |                                 0.0115 |                                -0.2647 |                                 28.5708 |                                 0.0002 |                                 0.0123 |                                -0.2369 |                                 21.1676 |                                 0.0002 |                                 0.0122 |                                -0.2023 |                                 10.5125 |                                 0.0002 |                                 0.0116 |                                -0.1687 |                                 -1.306  |                                 0.0002 |                                 0.0108 |                                -0.1391 |                                -13.1035 |                                 0.0002 |                                 0.0098 |                                -0.1138 |                                -24.272  |                                 0.0002 |                                 0.0087 |                                -0.0928 |                                -34.538  |                                 0.0002 |                                 0.0077 |                                -0.0753 |                                -43.8119 |                                 0.0002 |                                 0.0067 |                                -0.0609 |                                -52.1018 |                                 0.0002 |                                 0.0058 |                                -0.049  |                                -59.4638 |                                 0.0002 |                                 0.0049 |                                -0.0392 |                                -65.9752 |                                 0.0002 |                                 0.0041 |                                -0.0311 |                                -71.7194 |                                 0.0001 |                                 0.0034 |                                -0.0243 |                                -76.7785 |                                 0.0001 |                                 0.0027 |                                -0.0187 |                                -81.2291 |                                 0.0001 |                                 0.0021 |                                -0.014  |                                -85.1413 |                                 0.0001 |                                 0.0015 |                                -0.01   |                                -88.5775 |                                 0.0001 |                                 0.001  |                                -0.0067 |                                -91.5934 |                                 0.0001 |                                 0.0005 |                                -0.0039 |                                -94.2379 |                                 0.0001 |                                 0      |                                -0.0015 |                                -96.5542 |                                 0.0001 |                                -0.0004 |                                 0.0005 |                                -98.5799 |                                 0.0001 |                                -0.0007 |                                 0.0022 |                               -100.348  |                                 0.0001 |                                -0.0011 |                                 0.0036 |                               -101.888  |                                 0.0001 |                                -0.0014 |                                 0.0048 |                               -103.225  |                                 0.0001 |                                -0.0017 |                                 0.0058 |                               -104.382  |                                 0.0001 |                                -0.002  |                                 0.0067 |                               -105.377  |
|            340 |                                 0      |                                 0      |                                -0.0001 |                                  0.0076 |                                 0      |                                 0.0006 |                                -0.0319 |                                  3.0177 |                                 0      |                                 0.0032 |                                -0.1209 |                                 15.3892 |                                 0.0001 |                                 0.0065 |                                -0.1863 |                                 27.7438 |                                 0.0001 |                                 0.0091 |                                -0.209  |                                 33.0366 |                                 0.0002 |                                 0.0106 |                                -0.2043 |                                 31.2554 |                                 0.0002 |                                 0.0113 |                                -0.1866 |                                 24.5975 |                                 0.0002 |                                 0.0114 |                                -0.1645 |                                 15.1676 |                                 0.0002 |                                 0.011  |                                -0.1421 |                                  4.4673 |                                 0.0002 |                                 0.0104 |                                -0.1214 |                                 -6.5493 |                                 0.0002 |                                 0.0097 |                                -0.103  |                                -17.3181 |                                 0.0002 |                                 0.0089 |                                -0.087  |                                -27.5287 |                                 0.0002 |                                 0.0081 |                                -0.0733 |                                -37.0282 |                                 0.0002 |                                 0.0073 |                                -0.0616 |                                -45.7591 |                                 0.0002 |                                 0.0065 |                                -0.0516 |                                -53.7193 |                                 0.0001 |                                 0.0058 |                                -0.0431 |                                -60.9379 |                                 0.0001 |                                 0.0051 |                                -0.0359 |                                -67.4605 |                                 0.0001 |                                 0.0044 |                                -0.0297 |                                -73.3397 |                                 0.0001 |                                 0.0038 |                                -0.0244 |                                -78.63   |                                 0.0001 |                                 0.0032 |                                -0.0199 |                                -83.3849 |                                 0.0001 |                                 0.0027 |                                -0.016  |                                -87.6549 |                                 0.0001 |                                 0.0022 |                                -0.0127 |                                -91.487  |                                 0.0001 |                                 0.0017 |                                -0.0098 |                                -94.9242 |                                 0.0001 |                                 0.0013 |                                -0.0074 |                                -98.0055 |                                 0.0001 |                                 0.0009 |                                -0.0052 |                               -100.766  |                                 0.0001 |                                 0.0005 |                                -0.0034 |                               -103.238  |                                 0.0001 |                                 0.0001 |                                -0.0018 |                               -105.449  |                                 0.0001 |                                -0.0002 |                                -0.0004 |                               -107.424  |                                 0.0001 |                                -0.0005 |                                 0.0008 |                               -109.188  |
|            345 |                                 0      |                                 0      |                                 0      |                                  0.0009 |                                 0      |                                 0.0002 |                                -0.011  |                                  1.2588 |                                 0      |                                 0.0017 |                                -0.0636 |                                  9.9869 |                                 0.0001 |                                 0.0042 |                                -0.1213 |                                 22.977  |                                 0.0001 |                                 0.0068 |                                -0.1553 |                                 32.6056 |                                 0.0001 |                                 0.0087 |                                -0.1662 |                                 36.1614 |                                 0.0001 |                                 0.0099 |                                -0.1624 |                                 34.2431 |                                 0.0001 |                                 0.0105 |                                -0.151  |                                 28.3973 |                                 0.0002 |                                 0.0106 |                                -0.1364 |                                 20.0943 |                                 0.0002 |                                 0.0104 |                                -0.1211 |                                 10.4568 |                                 0.0002 |                                 0.0101 |                                -0.1064 |                                  0.2635 |                                 0.0002 |                                 0.0096 |                                -0.0928 |                                 -9.9754 |                                 0.0002 |                                 0.009  |                                -0.0806 |                                -19.9413 |                                 0.0001 |                                 0.0083 |                                -0.0698 |                                -29.4465 |                                 0.0001 |                                 0.0077 |                                -0.0603 |                                -38.3896 |                                 0.0001 |                                 0.0071 |                                -0.052  |                                -46.7256 |                                 0.0001 |                                 0.0064 |                                -0.0448 |                                -54.4449 |                                 0.0001 |                                 0.0058 |                                -0.0385 |                                -61.5604 |                                 0.0001 |                                 0.0052 |                                -0.033  |                                -68.0975 |                                 0.0001 |                                 0.0047 |                                -0.0282 |                                -74.0892 |                                 0.0001 |                                 0.0042 |                                -0.024  |                                -79.5715 |                                 0.0001 |                                 0.0037 |                                -0.0203 |                                -84.5816 |                                 0.0001 |                                 0.0032 |                                -0.0171 |                                -89.156  |                                 0.0001 |                                 0.0027 |                                -0.0143 |                                -93.3297 |                                 0.0001 |                                 0.0023 |                                -0.0118 |                                -97.1357 |                                 0.0001 |                                 0.0019 |                                -0.0097 |                               -100.605  |                                 0.0001 |                                 0.0016 |                                -0.0077 |                               -103.766  |                                 0.0001 |                                 0.0012 |                                -0.0061 |                               -106.644  |                                 0.0001 |                                 0.0009 |                                -0.0046 |                               -109.264  |
|            350 |                                 0      |                                 0      |                                 0      |                                  0.0001 |                                 0      |                                 0.0001 |                                -0.0035 |                                  0.4671 |                                 0      |                                 0.0008 |                                -0.0312 |                                  5.8737 |                                 0      |                                 0.0026 |                                -0.0745 |                                 17.2698 |                                 0.0001 |                                 0.0048 |                                -0.1094 |                                 28.8862 |                                 0.0001 |                                 0.0067 |                                -0.1286 |                                 36.5375 |                                 0.0001 |                                 0.0082 |                                -0.1346 |                                 39.1848 |                                 0.0001 |                                 0.0092 |                                -0.1321 |                                 37.4404 |                                 0.0001 |                                 0.0097 |                                -0.1247 |                                 32.4049 |                                 0.0001 |                                 0.0099 |                                -0.1148 |                                 25.1434 |                                 0.0001 |                                 0.0099 |                                -0.1042 |                                 16.5173 |                                 0.0001 |                                 0.0097 |                                -0.0936 |                                  7.1678 |                                 0.0001 |                                 0.0093 |                                -0.0835 |                                 -2.4513 |                                 0.0001 |                                 0.0089 |                                -0.0741 |                                -12.0304 |                                 0.0001 |                                 0.0084 |                                -0.0656 |                                -21.3656 |                                 0.0001 |                                 0.0079 |                                -0.058  |                                -30.3287 |                                 0.0001 |                                 0.0074 |                                -0.0511 |                                -38.8445 |                                 0.0001 |                                 0.0069 |                                -0.045  |                                -46.8741 |                                 0.0001 |                                 0.0063 |                                -0.0396 |                                -54.4032 |                                 0.0001 |                                 0.0058 |                                -0.0347 |                                -61.4341 |                                 0.0001 |                                 0.0053 |                                -0.0304 |                                -67.9799 |                                 0.0001 |                                 0.0049 |                                -0.0266 |                                -74.0599 |                                 0.0001 |                                 0.0044 |                                -0.0233 |                                -79.6977 |                                 0.0001 |                                 0.004  |                                -0.0202 |                                -84.9187 |                                 0.0001 |                                 0.0036 |                                -0.0176 |                                -89.7488 |                                 0.0001 |                                 0.0032 |                                -0.0152 |                                -94.2139 |                                 0.0001 |                                 0.0028 |                                -0.013  |                                -98.3392 |                                 0.0001 |                                 0.0025 |                                -0.0111 |                               -102.149  |                                 0.0001 |                                 0.0021 |                                -0.0094 |                               -105.665  |

---

## get_speed
Calculate the speed of an option based on the Black Scholes Model: how much the gamma changes for a 1.00 change in the price of the underlying asset.

The Black Scholes Model is a mathematical model used to estimate the price of European-style options. The speed is the rate of change of the gamma with respect to the price of the underlying asset.

The speed calculation is the theoretical value of the speed. The actual speed can differ from this value due to several factors such as the volatility of the underlying asset, the time to expiration, the risk free rate and more.

The formula is as follows:

$$
d_{1} = \frac{\ln\left(\frac{S}{K}\right) + \left(r - q + \frac{\sigma^{2}}{2}\right) \cdot t}{\sigma \cdot \sqrt{t}}
$$

$$
\text{Speed} = - e^{- q \cdot t} \cdot \frac{N'(d_{1})}{S^{2} \cdot \sigma \cdot \sqrt{t}} \cdot \left(\frac{d_{1}}{\sigma \cdot \sqrt{t}} + 1\right)
$$

Where S is the stock price, K is the strike price, r is the risk free rate, q is the dividend yield, $$\sigma$$ is the volatility, t is the time to expiration and N'(d1) is the standard normal probability density at d1.

The Speed can be interpreted as follows:

- If Speed is positive, the option's Gamma rises as the underlying price rises, so the position's convexity builds up on the way up.
- If Speed is negative, the option's Gamma falls as the underlying price rises, which is the usual case just below the strike where Gamma is already close to its peak.

Note that the speed of a call option and put option are equal to each other.

**Also known as:** gamma rate of change.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None which
means it will use the current dividend yield.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: the speed values containing the tickers and strike prices as the index and the
time to expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["F"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.options.get_speed(
    strike_price_range=0.25, strike_step_size=1
).loc["F", ["2026-01-07", "2026-01-14", "2026-01-28"]]
```

Which returns:

|   Strike Price |   2026-01-07 |   2026-01-14 |   2026-01-28 |
|---------------:|-------------:|-------------:|-------------:|
|              9 |       0      |       0      |      -0.0002 |
|             10 |       0      |      -0.0003 |      -0.0094 |
|             11 |      -0.0025 |      -0.0357 |      -0.0821 |
|             12 |      -0.3206 |      -0.3006 |      -0.181  |
|             13 |      -0.2865 |      -0.1279 |      -0.0636 |
|             14 |       0.5608 |       0.31   |       0.1256 |
|             15 |       0.0475 |       0.137  |       0.1331 |

---

## get_zomma
Calculate the zomma of an option based on the Black Scholes Model: how much the gamma changes for a 1.00 change in the volatility.

The Black Scholes Model is a mathematical model used to estimate the price of European-style options. The zomma is the rate of change of the gamma with respect to volatility.

The zomma calculation is the theoretical value of the zomma. The actual zomma can differ from this value due to several factors such as the volatility of the underlying asset, the time to expiration, the risk free rate and more.

The formula is as follows:

$$
d_{1} = \frac{\ln\left(\frac{S}{K}\right) + \left(r - q + \frac{\sigma^{2}}{2}\right) \cdot t}{\sigma \cdot \sqrt{t}}
$$

$$
d_{2} = d_{1} - \sigma \cdot \sqrt{t}
$$

$$
\text{Zomma} = \frac{e^{- q \cdot t} \cdot (N'(d_{1}) \cdot (d_{1} \cdot d_{2} - 1))}{S \cdot \sigma^{2} \cdot \sqrt{t}}
$$

Where S is the stock price, K is the strike price, r is the risk free rate, q is the dividend yield, $$\sigma$$ is the volatility, t is the time to expiration and N'(d1) is the standard normal probability density at d1. This is equivalently Gamma * $$(d_{1} \cdot d_{2} - 1) / \sigma$$, and it is reported unscaled, per 1.00 of volatility.

The Zomma can be interpreted as follows:

- If Zomma is positive, the option's Gamma rises as implied volatility rises, which is typical for strikes well away from the money.
- If Zomma is negative, the option's Gamma falls as implied volatility rises, which is typical for strikes near the money where Gamma is already at its peak.

Note that the zomma of a call option and put option are equal to each other.

**Also known as:** gamma sensitivity to volatility.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None which
means it will use the current dividend yield.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: the zomma values containing the tickers and strike prices as the index and the
time to expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["CSCO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.options.get_zomma(
    strike_price_range=0.15, strike_step_size=2
).loc["CSCO", ["2026-01-07", "2026-01-14", "2026-01-28"]]
```

Which returns:

|   Strike Price |   2026-01-07 |   2026-01-14 |   2026-01-28 |
|---------------:|-------------:|-------------:|-------------:|
|             64 |       0      |       0.0022 |       0.0379 |
|             66 |       0.0002 |       0.0169 |       0.085  |
|             68 |       0.0062 |       0.0729 |       0.1319 |
|             70 |       0.0671 |       0.1714 |       0.1245 |
|             72 |       0.2478 |       0.177  |       0.0181 |
|             74 |       0.1558 |      -0.0714 |      -0.1588 |
|             76 |      -0.4946 |      -0.4013 |      -0.3027 |
|             78 |      -0.5371 |      -0.4263 |      -0.3183 |
|             80 |       0.1029 |      -0.1275 |      -0.2014 |
|             82 |       0.2942 |       0.1513 |      -0.032  |
|             84 |       0.1312 |       0.2137 |       0.0996 |
|             86 |       0.0274 |       0.1414 |       0.1536 |

---

## get_color
Calculate the color of an option based on the Black Scholes Model: how much the gamma changes as time passes.

The Black Scholes Model is a mathematical model used to estimate the price of European-style options. The color is the rate of change of the gamma with respect to time to expiration.

The color calculation is the theoretical value of the color. The actual color can differ from this value due to several factors such as the volatility of the underlying asset, the time to expiration, the risk free rate and more.

The formula is as follows:

$$
d_{1} = \frac{\ln\left(\frac{S}{K}\right) + \left(r - q + \frac{\sigma^{2}}{2}\right) \cdot t}{\sigma \cdot \sqrt{t}}
$$

$$
d_{2} = d_{1} - \sigma \cdot \sqrt{t}
$$

$$
\text{Color} = e^{- q \cdot t} \cdot \frac{N'(d_{1})}{2 \cdot S \cdot t \cdot \sigma \cdot \sqrt{t}} \cdot \left(2 \cdot q \cdot t + 1 + \frac{2 \cdot (r - q) \cdot t - d_{2} \cdot \sigma \cdot \sqrt{t}}{\sigma \cdot \sqrt{t}} \cdot d_{1}\right)
$$

Where S is the stock price, K is the strike price, r is the risk free rate, q is the dividend yield, $$\sigma$$ is the volatility, t is the time to expiration and N'(d1) is the standard normal probability density at d1.

This expression equals dGamma/dt, the change in Gamma as calendar time passes (the negative of the derivative with respect to the remaining time to maturity t), so Color, like Theta, Charm and Veta, measures the change per unit of time that passes. Tables that print the expression with a leading minus sign give the derivative with respect to the time to maturity instead. The result is per year, matching Charm; divide by 365 for gamma decay per calendar day.

The Color can be interpreted as follows:

- If Color is positive, the option's Gamma builds up with each day that passes, which is what happens to a near-the-money option as expiration approaches.
- If Color is negative, the option's Gamma bleeds away with each day that passes, which is what happens to a strike far from the money that is running out of time to reach it.

Note that the color of a call option and put option are equal to each other.

**Also known as:** gamma time decay.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None which
means it will use the current dividend yield.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: the color values containing the tickers and strike prices as the index and the
time to expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["PEP"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.options.get_color(
    strike_price_range=0.15, strike_step_size=5
).loc["PEP", ["2026-01-07", "2026-01-14", "2026-01-28"]]
```

Which returns:

|   Strike Price |   2026-01-07 |   2026-01-14 |   2026-01-28 |
|---------------:|-------------:|-------------:|-------------:|
|            120 |       0      |      -0.0035 |      -0.0324 |
|            125 |      -0.0026 |      -0.0528 |      -0.0911 |
|            130 |      -0.1388 |      -0.2563 |      -0.1154 |
|            135 |      -0.9333 |      -0.2702 |       0.0109 |
|            140 |       0.6316 |       0.475  |       0.2228 |
|            145 |       1.9639 |       0.756  |       0.2789 |
|            150 |      -0.8502 |       0.0104 |       0.1184 |
|            155 |      -0.6023 |      -0.3775 |      -0.0688 |
|            160 |      -0.069  |      -0.2174 |      -0.1353 |

---

## get_ultima
Calculate the ultima of an option based on the Black Scholes Model: how much the vomma changes for a 1.00 change in the volatility.

The Black Scholes Model is a mathematical model used to estimate the price of European-style options. The ultima is the rate of change of the vomma with respect to volatility.

The ultima calculation is the theoretical value of the ultima. The actual gamma can differ from this value due to several factors such as the volatility of the underlying asset, the time to expiration, the risk free rate and more.

The formula is as follows:

$$
d_{1} = \frac{\ln\left(\frac{S}{K}\right) + \left(r - q + \frac{\sigma^{2}}{2}\right) \cdot t}{\sigma \cdot \sqrt{t}}
$$

$$
d_{2} = d_{1} - \sigma \cdot \sqrt{t}
$$

$$
\text{Ultima} = \left(- \frac{\text{vega}}{\sigma^{2}}\right) \cdot (d_{1} \cdot d_{2} \cdot (1 - d_{1} \cdot d_{2}) + d_{1}^{2} + d_{2}^{2})
$$

Where S is the stock price, K is the strike price, r is the risk free rate, q is the dividend yield, $$\sigma$$ is the volatility, t is the time to expiration and vega is the unscaled $$S \cdot e^{- q \cdot t} \cdot N' (d_{1}) \cdot \sqrt{t}$$, i.e. the Vega before the division by 100 that `get_vega` applies. Ultima itself is likewise reported unscaled, per 1.00 of volatility.

The Ultima can be interpreted as follows:

- If Ultima is positive, the option's Vomma rises as implied volatility rises, so the volatility convexity of the position builds up in a rising volatility regime.
- If Ultima is negative, the option's Vomma falls as implied volatility rises, which is the usual case for strikes near the money.

Note that the ultima of a call option and put option are equal to each other.

**Also known as:** third-order vega.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None which
means it will use the current dividend yield.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: the ultima values containing the tickers and strike prices as the index and the
time to expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NKE"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.options.get_ultima(
    strike_price_range=0.15, strike_step_size=2, expiration_time_range=91
).loc["NKE", ["2026-01-30", "2026-03-01", "2026-03-31"]]
```

Which returns:

|   Strike Price |   2026-01-30 |   2026-03-01 |   2026-03-31 |
|---------------:|-------------:|-------------:|-------------:|
|             54 |     -30.462  |     -65.1596 |     -73.0513 |
|             56 |     -46.1469 |     -58.2358 |     -57.7726 |
|             58 |     -42.7099 |     -40.8971 |     -37.7182 |
|             60 |     -25.0057 |     -20.7534 |     -18.6318 |
|             62 |      -6.6506 |      -5.5439 |      -5.3419 |
|             64 |      -0.2363 |      -0.4387 |      -0.7623 |
|             66 |      -9.4787 |      -6.7179 |      -5.544  |
|             68 |     -28.2953 |     -21.9944 |     -18.308  |
|             70 |     -45.8728 |     -41.5316 |     -36.2623 |

---

## get_put_call_ratio
Calculate the put-call ratio of every expiry, by volume and by open interest: how many puts are traded or held per call, which is usually read as hedging demand or bearish sentiment when above one.

The ratio is the number of puts divided by the number of calls, and an unusually low ratio is read as complacency. The volume ratio reflects today's trading; the open interest ratio the positions that remain.

**Also known as:** PCR, put/call ratio, options sentiment.

**Args:**

- <u>expiration_dates (list[str] &#124; None, optional):</u> The expiries to use. Defaults to
None, the nearest `number_of_expirations` expiries.
- <u>number_of_expirations (int, optional):</u> The number of nearest expiries to use when
no dates are given, at least 1. Defaults to 6.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker and expiry, and over all of them ("All"), the Days to
Expiration, Call Volume, Put Volume, Volume Put-Call Ratio, Call Open Interest,
Put Open Interest and Open Interest Put-Call Ratio.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.options.get_put_call_ratio(number_of_expirations=3)
```

Which returns:

|                 |   Days to Expiration |   Call Volume |   Put Volume |   Volume Put-Call Ratio |   Call Open Interest |   Put Open Interest |   Open Interest Put-Call Ratio |
|:----------------|---------------------:|--------------:|-------------:|------------------------:|---------------------:|--------------------:|-------------------------------:|
| ('AAPL', 'All') |                  nan |        117895 |       172939 |                  1.4669 |               467397 |              454917 |                         0.9733 |
| ('TSLA', 'All') |                  nan |        222838 |       192067 |                  0.8619 |               383562 |              508747 |                         1.3264 |

---

## get_max_pain
Calculate the max pain strike of every expiry: the expiry price at which the options outstanding would pay their holders the least, the sum over every call of open interest times max(price - strike, 0) and over every put of open interest times max(strike - price, 0) being smallest. Option writers, often market makers, profit most there, and some traders expect the price to drift towards it as the expiry nears; the evidence for that is mixed, so it is best read as a description of where open interest is concentrated.

**Also known as:** max pain theory, option pain, maximum pain.

**Args:**

- <u>expiration_dates (list[str] &#124; None, optional):</u> The expiries to use. Defaults to
None, the nearest `number_of_expirations` expiries.
- <u>number_of_expirations (int, optional):</u> The number of nearest expiries to use when
no dates are given, at least 1. Defaults to 6.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker and expiry the Days to Expiration, Max Pain strike,
Stock Price and the Distance to Max Pain (as a fraction of the price).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.options.get_max_pain(number_of_expirations=4)
```

Which returns:

|                        |   Days to Expiration |   Max Pain |   Stock Price |   Distance to Max Pain |
|:-----------------------|---------------------:|-----------:|--------------:|-----------------------:|
| ('AAPL', '2026-11-18') |                    2 |      355   |        352.78 |                 0.0063 |
| ('AAPL', '2026-11-20') |                    4 |      337.5 |        352.78 |                -0.0433 |
| ('AAPL', '2026-11-23') |                    7 |      355   |        352.78 |                 0.0063 |
| ('AAPL', '2026-11-25') |                    9 |      357.5 |        352.78 |                 0.0134 |

---

## get_gamma_exposure
Calculate the dealer gamma exposure (GEX): the dollar value of shares market makers would have to buy or sell for every 1% move in the underlying to keep their option books delta-neutral. Following the common convention, dealers are assumed long the calls and short the puts that investors trade:

- Gamma Exposure = Gamma x Open Interest x 100 x Price² x 0.01
- positive for calls, negative for puts, summed over strikes and expiries

With positive exposure dealers buy dips and sell rallies, which dampens volatility; with negative exposure they trade in the direction of the move and amplify it. The gamma flip point is the price at which the total exposure changes sign.

**Also known as:** GEX, dealer gamma, gamma positioning, net gamma.

**References:**

- paper | SqueezeMetrics (2017). "Gamma Exposure (GEX)." White paper.
- paper | Perfiliev, S. (2021). "How to Calculate Gamma Exposure (GEX) and Zero Gamma Level." [https://perfiliev.com/blog/how-to-calculate-gamma-exposure-and-zero-gamma-level/](https://perfiliev.com/blog/how-to-calculate-gamma-exposure-and-zero-gamma-level/){:target="_blank"}

**Args:**

- <u>expiration_dates (list[str] &#124; None, optional):</u> The expiries to include. Defaults
to None, the nearest `number_of_expirations` expiries.
- <u>number_of_expirations (int, optional):</u> The number of nearest expiries to include
when no dates are given, at least 1. Defaults to 6.
- <u>by_strike (bool, optional):</u> Whether to return the exposure per strike instead of
the totals. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker the Stock Price, Call, Put and Net Gamma Exposure (in
dollars per 1% move) and the Gamma Flip Point; or, when returned per strike, the
Call, Put and Net Gamma Exposure per ticker and strike.

**Notes:**

- The assumption about who holds which side is the main uncertainty: when
investors sell calls (covered calls) the sign of that part flips.
- Gamma uses each option's own implied volatility (Black-Scholes).
- The stock price is the price of the underlying quoted with the live option chain
(Yahoo Finance's regular market price), so both come from the same moment; when
the chain quotes none, the traded Close of the last historical date is used. The
risk free rate and dividend yield come from the historical data as well, so
leave end_date at today: a warning is logged when the history ends more than 5
days before today.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["QQQ", "AAPL"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.options.get_gamma_exposure()
```

Which returns:

|      |   Stock Price |   Call Gamma Exposure |   Put Gamma Exposure |   Net Gamma Exposure |   Gamma Flip Point |
|:-----|--------------:|----------------------:|---------------------:|---------------------:|-------------------:|
| QQQ  |        661.75 |           1.57107e+09 |         -4.27908e+09 |         -2.708e+09   |            689.003 |
| AAPL |        352.78 |           1.02921e+09 |         -6.02256e+08 |          4.26958e+08 |            346.506 |

---

## get_implied_volatility_term_structure
Calculate the term structure of implied volatility: the at-the-money implied volatility of every expiry, interpolated at the current price and averaged over calls and puts. Normally longer expiries carry a higher volatility (contango); an inverted curve, with short-dated options dearer than long-dated ones, shows that the market expects turbulence soon, as around earnings or in a sell-off.

**Also known as:** volatility term structure, IV curve, volatility curve.

**Args:**

- <u>expiration_dates (list[str] &#124; None, optional):</u> The expiries to use. Defaults to
None, the nearest `number_of_expirations` expiries.
- <u>number_of_expirations (int, optional):</u> The number of nearest expiries to use when
no dates are given, at least 1. Defaults to 10.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker and expiry the Days to Expiration and the At-the-Money
Volatility (annualized, as a decimal).

**Notes:**

- The stock price is the price of the underlying quoted with the live option chain
(Yahoo Finance's regular market price), so both come from the same moment; when
the chain quotes none, the traded Close of the last historical date is used. The
risk free rate and dividend yield come from the historical data as well, so
leave end_date at today: a warning is logged when the history ends more than 5
days before today.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.options.get_implied_volatility_term_structure(number_of_expirations=5)
```

Which returns:

|                        |   Days to Expiration |   At-the-Money Volatility |
|:-----------------------|---------------------:|--------------------------:|
| ('AAPL', '2026-11-18') |                    2 |                    0.2889 |
| ('AAPL', '2026-11-20') |                    4 |                    0.2983 |
| ('AAPL', '2026-11-23') |                    7 |                    0.2516 |
| ('AAPL', '2026-11-25') |                    9 |                    0.2711 |
| ('AAPL', '2026-11-27') |                   11 |                    0.2508 |
| ('TSLA', '2026-11-18') |                    2 |                    0.6121 |
| ('TSLA', '2026-11-20') |                    4 |                    0.6225 |
| ('TSLA', '2026-11-23') |                    7 |                    0.526  |
| ('TSLA', '2026-11-25') |                    9 |                    0.5349 |
| ('TSLA', '2026-11-27') |                   11 |                    0.5078 |

---

## get_volatility_skew
Calculate the volatility skew of every expiry: how much more the market pays for downside than for upside protection, from the 25-delta options, the standard way to compare skew across underlyings and dates:

$$
\text{25-Delta} \;\text{Risk Reversal} = \operatorname{IV}(\text{25-delta} \;\text{call}) - \operatorname{IV}(\text{25-delta} \;\text{put})
$$

$$
\text{25-Delta} \;\text{Butterfly} = \frac{\operatorname{IV}(\text{25-delta} \;\text{call}) + \operatorname{IV}(\text{25-delta} \;\text{put})}{2} - \text{ATM IV}
$$

For equities the risk reversal is usually negative: out-of-the-money puts are dearer than calls because investors pay for crash protection. A more negative risk reversal means more fear of a fall; the butterfly measures how much both tails cost relative to the centre. The deltas follow from each option's implied volatility, and the volatility at exactly 25 delta is interpolated.

**Also known as:** risk reversal, volatility smile, skew, butterfly spread volatility.

**References:**

- paper | Gatheral, J. (2006). "The Volatility Surface: A Practitioner's Guide." Wiley.

**Args:**

- <u>expiration_dates (list[str] &#124; None, optional):</u> The expiries to use. Defaults to
None, the nearest `number_of_expirations` expiries.
- <u>number_of_expirations (int, optional):</u> The number of nearest expiries to use when
no dates are given, at least 1. Defaults to 6.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker and expiry the Days to Expiration, the 25-Delta Put,
At-the-Money and 25-Delta Call Volatility, the 25-Delta Risk Reversal and the
25-Delta Butterfly.

**Notes:**

- The stock price is the price of the underlying quoted with the live option chain
(Yahoo Finance's regular market price), so both come from the same moment; when
the chain quotes none, the traded Close of the last historical date is used. The
risk free rate and dividend yield come from the historical data as well, so
leave end_date at today: a warning is logged when the history ends more than 5
days before today.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["QQQ", "AAPL"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.options.get_volatility_skew(number_of_expirations=3)
```

Which returns:

|                        |   Days to Expiration |   25-Delta Put Volatility |   At-the-Money Volatility |   25-Delta Call Volatility |   25-Delta Risk Reversal |   25-Delta Butterfly |
|:-----------------------|---------------------:|--------------------------:|--------------------------:|---------------------------:|-------------------------:|---------------------:|
| ('QQQ', '2026-11-17')  |                    1 |                    0.4167 |                    0.3999 |                     0.3738 |                  -0.0429 |              -0.0047 |
| ('QQQ', '2026-11-18')  |                    2 |                    0.4336 |                    0.4161 |                     0.3949 |                  -0.0387 |              -0.0019 |
| ('QQQ', '2026-11-19')  |                    3 |                    0.4302 |                    0.4128 |                     0.3904 |                  -0.0398 |              -0.0025 |
| ('AAPL', '2026-11-18') |                    2 |                    0.3172 |                    0.2889 |                     0.2724 |                  -0.0448 |               0.0059 |
| ('AAPL', '2026-11-20') |                    4 |                    0.3142 |                    0.2983 |                     0.2728 |                  -0.0414 |              -0.0048 |
| ('AAPL', '2026-11-23') |                    7 |                    0.27   |                    0.2516 |                     0.2324 |                  -0.0376 |              -0.0004 |

---

## get_implied_move
Calculate the move the options market expects up to every expiry: the size of the move, in either direction, that the price of the at-the-money straddle (buying the call and the put at the strike closest to the current price) prices in:

$$
\text{Implied Move} = \frac{\text{Call Price} + \text{Put Price}}{\text{Stock Price}}
$$

$$
\text{Expected Range} = \text{Stock Price} \;\pm \;\text{Straddle Price}
$$

$$
\text{Bid-Ask Spread} = \frac{\text{Call Ask} - \text{Call Bid} + \text{Put Ask} - \text{Put Bid}}{\text{Straddle Price}}
$$

The straddle pays the absolute move, so its price is the market's expected size of the move, regardless of direction. Around earnings the first expiry after the next earnings date is used, which gives the move the market prices for the earnings announcement (an expiry on the announcement day itself settles at that day's close, before the usual after-the-close announcement).

**Also known as:** expected move, straddle move, earnings move, implied earnings move.

**Args:**

- <u>expiration_dates (list[str] &#124; None, optional):</u> The expiries to use. Defaults to
None, the nearest `number_of_expirations` expiries.
- <u>number_of_expirations (int, optional):</u> The number of nearest expiries to use when
no dates are given, at least 1. Defaults to 4.
- <u>around_earnings (bool, optional):</u> Whether to use the first expiry after the next
earnings date instead. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker and expiry the Days to Expiration, Straddle Strike,
Straddle Price, Bid-Ask Spread (as a fraction of the straddle price), Last Trade
Legs, Implied Move (as a fraction of the price) and the Lower and Upper Price of
the expected range.

**Notes:**

- The move up to an expiry after earnings also includes the ordinary daily moves
until then; the closer the expiry is to the announcement, the purer the measure.
- The prices are the middle of the bid and ask, or the last traded price of an option
without a two-sided quote that is still held or traded. The Bid-Ask Spread shows
how firmly the straddle is quoted (NaN when a leg has no two-sided quote) and the
Last Trade Legs how many of the two legs (0, 1 or 2) are priced from their last
trade, which can be days or weeks old.
- A warning names the ticker, expiry and strike when a leg is priced from its last
trade (with its last trade date and open interest) or when the bid-ask spread is
wider than half the straddle (above 0.5), as the implied move then may not reflect
the live market. Outside US market hours Yahoo Finance reports a bid and ask of 0,
so every leg is priced from its last trade; one warning then names the expiries.
- The stock price is the price of the underlying quoted with the live option chain
(Yahoo Finance's regular market price), so both come from the same moment; when
the chain quotes none, the traded Close of the last historical date is used. The
risk free rate and dividend yield come from the historical data as well, so
leave end_date at today: a warning is logged when the history ends more than 5
days before today.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "NVDA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.options.get_implied_move(around_earnings=True)
```

Which returns:

|                        | Earnings Date   |   Days to Expiration |   Straddle Strike |   Straddle Price |   Bid-Ask Spread |   Last Trade Legs |   Implied Move |   Lower Price |   Upper Price |
|:-----------------------|:----------------|---------------------:|------------------:|-----------------:|-----------------:|------------------:|---------------:|--------------:|--------------:|
| ('AAPL', '2027-02-19') | 2027-02-04      |                   85 |               360 |           36.925 |           0.0447 |                 0 |         0.1038 |       318.655 |       392.505 |
| ('NVDA', '2027-03-19') | 2027-02-24      |                  113 |               150 |           38.725 |           0.0374 |                 0 |         0.2594 |       110.575 |       188.025 |

---

## get_model_free_implied_volatility
Calculate the model-free implied volatility with the Cboe VIX methodology, for any ticker with listed options: the volatility the options market expects over the coming days, without a pricing model.

Rather than inverting a pricing model, it reads the expected variance directly from the prices of out-of-the-money options across all strikes, weighted by $$1 / K^{2}$$, for the two expiries around the target maturity, and interpolates their variances to a constant maturity:

$$
\sigma^{2} = \frac{2}{T} \sum\left(\frac{\Delta K_{i}}{K_{i}^{2}}\right) e^{\text{RT}} Q(K_{i}) - \left(\frac{1}{T}\right) \left(\frac{F}{K_{0}} - 1\right)^{2}
$$

$$
\text{Volatility} = \sqrt{\text{interpolated variance at} \;\text{days}}
$$

Applied to the S&P 500 index options ("^SPX") over 30 days it approximates the VIX, within about a tenth of a volatility point: the Cboe counts the time to expiry in minutes, uses Treasury rates for each expiry and the Friday expiries between 23 and 37 days away. For a single stock it gives the equivalent volatility index.

**Also known as:** VIX methodology, model-free volatility, variance swap volatility.

**References:**

- paper | Cboe Global Markets (2023). "Cboe Volatility Index (VIX) White Paper."
- paper | Britten-Jones, M. and Neuberger, A. (2000). "Option Prices, Implied Price Processes, and Stochastic Volatility." The Journal of Finance, 55(2), 839-866.

**Args:**

- <u>days (int, optional):</u> The constant maturity in calendar days, at least 1. Defaults to 30.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker the Near-Term and Next-Term Expiration and Volatility,
the Forward Price and the Model-Free Implied Volatility (annualized, as a
decimal).

**Notes:**

- Options without a bid are left out of the strip, as in the Cboe method. Outside
market hours Yahoo Finance reports a bid and ask of 0, so a ValueError names the
ticker and expiry. Last traded prices are not used instead: they are of different
moments of the session, so put-call parity and the tails no longer agree.
- A target shorter than the nearest usable expiry (at least 7 days away) is
extrapolated from the two nearest terms, as in the Cboe method. A target beyond
the longest usable expiry raises a ValueError naming the ticker and that expiry,
since there is no later term to interpolate towards.
- The time to each expiry runs from the current time to 16:00 New York time on the
expiration date, in minutes over the 525,600 minutes of a year as in the Cboe method, and
the variance of a term and its weight in the interpolation use that same time.
- The risk free rate comes from the historical data, so leave end_date at today: a
warning is logged when the history ends more than 5 days before today.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["^SPX", "AAPL"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.options.get_model_free_implied_volatility()
```

Which returns:

|      | Near-Term Expiration   | Next-Term Expiration   |   Near-Term Volatility |   Next-Term Volatility |   Forward Price |   Model-Free Implied Volatility |
|:-----|:-----------------------|:-----------------------|-----------------------:|-----------------------:|----------------:|--------------------------------:|
| ^SPX | 2026-12-16             | 2026-12-17             |                 0.2274 |                 0.2284 |        7436.64  |                          0.2276 |
| AAPL | 2026-12-11             | 2026-12-18             |                 0.2655 |                 0.2724 |         353.871 |                          0.2709 |

---

## get_volatility_risk_premium
Calculate the volatility risk premium: the model-free implied volatility over the coming `days` minus the volatility the stock actually realized over the same span in the past, and the same in variance units. Implied volatility usually exceeds realized volatility, because investors pay a premium for protection, which is the return option sellers earn. A premium that turns negative means the market prices less movement than it has just seen, often after a shock.

- Realized Volatility = standard deviation of the daily returns over the last `days` calendar days, annualized
- Volatility Risk Premium = Implied Volatility - Realized Volatility
- Variance Risk Premium = Implied Volatility² - Realized Volatility²

Both compare the implied figure with the realized one of the past, which is known today, as Bollerslev, Tauchen and Zhou (2009) do. Carr and Wu (2009) measure the premium after the fact instead: the variance realized over the coming `days` minus the variance swap rate, which is negative on average.

**Also known as:** VRP, implied minus realized volatility, variance risk premium.

**References:**

- paper | Bollerslev, T., Tauchen, G. and Zhou, H. (2009). "Expected Stock Returns and Variance Risk Premia." The Review of Financial Studies, 22(11), 4463-4492.
- paper | Carr, P. and Wu, L. (2009). "Variance Risk Premiums." The Review of Financial Studies, 22(3), 1311-1341.

**Args:**

- <u>days (int, optional):</u> The horizon in calendar days of both volatilities, at least 1.
Defaults to 30.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker the Implied Volatility, Realized Volatility, Volatility
Risk Premium, Variance Risk Premium and the ratio of implied to realized
volatility.

**Notes:**

- The realized volatility covers the last `days` calendar days of the historical
data, while the implied volatility comes from the live option chains. Leave
end_date at today so both describe the same moment: a warning is logged when the
history ends more than 5 days before today.
- A `days` beyond the longest usable expiry raises a ValueError, see
get_model_free_implied_volatility.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["QQQ", "AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.options.get_volatility_risk_premium()
```

Which returns:

|      |   Implied Volatility |   Realized Volatility |   Volatility Risk Premium |   Variance Risk Premium |   Implied to Realized Ratio |
|:-----|---------------------:|----------------------:|--------------------------:|------------------------:|----------------------------:|
| QQQ  |               0.3272 |                0.3555 |                   -0.0283 |                 -0.0193 |                      0.9203 |
| AAPL |               0.2709 |                0.2745 |                   -0.0036 |                 -0.002  |                      0.9867 |
| TSLA |               0.5498 |                0.5943 |                   -0.0445 |                 -0.0509 |                      0.9251 |

---

## get_risk_neutral_moments
Calculate the risk-neutral (option-implied) volatility, skewness and kurtosis of the log return up to every expiry: the shape of the return distribution that the option prices imply, with the method of Bakshi, Kapadia and Madan (2003).

Any payoff can be built from a position in the underlying and a strip of out-of-the-money options (Carr and Madan, 2001), so the prices of the quadratic, cubic and quartic contracts on the log return follow from the option prices, and with them the moments the market prices in, without a pricing model. A negative skewness means the options price a larger chance of a fall than of a rise of the same size; a kurtosis above 3 means fatter tails than a normal distribution.

The formula is as follows, with $$R = \ln (S_{T} / K_{0})$$, $$y_{i} = \ln (K_{i} / K_{0})$$ and the strikes $$K_{i}$$, prices $$Q (K_{i})$$ and intervals $$\Delta K_{i}$$ of the VIX methodology:

$$
V = \frac{\sum 2 (1 - y_{i}) Q(K_{i}) \Delta K_{i}}{K_{i}^{2}}
$$

$$
W = \frac{\sum(6 y_{i} - 3 y_{i}^{2}) Q(K_{i}) \Delta K_{i}}{K_{i}^{2}}
$$

$$
X = \frac{\sum(12 y_{i}^{2} - 4 y_{i}^{3}) Q(K_{i}) \Delta K_{i}}{K_{i}^{2}}
$$

$$
\mu = \frac{F}{K_{0}} - 1 - \frac{e^{rT} V}{2} - \frac{e^{rT} W}{6} - \frac{e^{rT} X}{24}
$$

$$
\text{Skewness} = \frac{e^{rT} W - 3 \mu e^{rT} V + 2 \mu^{3}}{(e^{rT} V - \mu^{2})^{\frac{3}{2}}}
$$

$$
\text{Kurtosis} = \frac{e^{rT} X - 4 \mu e^{rT} W + 6 e^{rT} \mu^{2} V - 3 \mu^{4}}{(e^{rT} V - \mu^{2})^{2}}
$$

$$
\text{Volatility} = \sqrt{\frac{e^{rT} V - \mu^{2}}{T}}
$$

$$
\text{Expected Log Return} = E\left[\ln\left(\frac{S_{T}}{F}\right)\right] = \mu - \ln\left(\frac{F}{K_{0}}\right)
$$

The integrals of the paper are discretised as in the Cboe VIX methodology: the forward price F follows from put-call parity at the strike where call and put prices are closest, $$K_{0}$$ is the first strike at or below it, $$Q (K_{i})$$ is the put price below $$K_{0}$$, the call price above and their average at $$K_{0}$$, and $$\Delta K_{i}$$ is half the distance between the neighbouring strikes (the distance to the one neighbour at the ends). Puts and calls are added away from $$K_{0}$$ while they have a bid, up to two consecutive strikes without one. The paper expands around the spot price without dividends ($$F / S = e^{\text{rT}}$$); the expansion around $$K_{0}$$ keeps the replication exact and takes in dividends through the forward price, and leaves the skewness and kurtosis unchanged. r is the continuously compounded risk free rate.

**Also known as:** option-implied moments, implied skewness, implied kurtosis, BKM moments.

**References:**

- paper | Bakshi, G., Kapadia, N. and Madan, D. (2003). "Stock Return Characteristics, Skew Laws, and the Differential Pricing of Individual Equity Options." The Review of Financial Studies, 16(1), 101-143.
- paper | Carr, P. and Madan, D. (2001). "Optimal Positioning in Derivative Securities." Quantitative Finance, 1(1), 19-37.
- paper | Cboe Global Markets (2023). "Cboe Volatility Index (VIX) White Paper."

**Args:**

- <u>expiration_dates (list[str] &#124; None, optional):</u> The expiries to use. Defaults to
None, the nearest `number_of_expirations` expiries.
- <u>number_of_expirations (int, optional):</u> The number of nearest expiries to use when
no dates are given, at least 1. Defaults to 4.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker and expiry the Days to Expiration, Forward Price,
Expected Log Return (relative to the forward price, over the time to
expiration), Volatility (annualized), Skewness and Kurtosis of the log return.

**Notes:**

- The sums approximate the integrals over the strikes, so the moments depend on how
finely the strikes are spaced and how far they reach into the tails; the kurtosis is
the most sensitive. On a Black-Scholes chain (20% volatility, 30 days) with strikes
from 50% to 150% of the price, the kurtosis is within 0.031 of the normal value of 3
(and the skewness within 0.001 of 0) for strikes 1% of the price apart, and within
0.001 for strikes 0.1% apart; strikes from 10% to 190% give the same values, as the
options beyond 50% and 150% are worth almost nothing. The reach matters when the
strip ends within a few standard deviations of the price: from 80% to 120% (3.5
standard deviations) the kurtosis is 0.008 low at the finest spacing.
- Prices are the middle of the bid and ask, or the last price of an option with
volume or open interest when there is no two-sided quote. Outside market hours,
when bids are missing, an expiry has no strip and its moments are NaN.
- The time to each expiry runs from the current time to 16:00 New York time on the
expiration date, in minutes over the 525,600 minutes of a year. The risk free rate
comes from the historical data, so leave end_date at today: a warning is logged
when the history ends more than 5 days before today.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["^SPX", "AAPL"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.options.get_risk_neutral_moments(
    number_of_expirations=3, show_columns=["Volatility", "Skewness", "Kurtosis"]
)
```

Which returns:

|                        |   Volatility |   Skewness |   Kurtosis |
|:-----------------------|-------------:|-----------:|-----------:|
| ('^SPX', '2026-11-19') |       0.2852 |    -0.9794 |    10.6888 |
| ('^SPX', '2026-11-20') |       0.2745 |    -2.5062 |    28.0073 |
| ('^SPX', '2026-11-23') |       0.2381 |    -3.069  |    41.0756 |
| ('AAPL', '2026-11-20') |       0.3401 |    -1.4245 |    12.0253 |
| ('AAPL', '2026-11-23') |       0.2615 |    -1.4104 |     9.5121 |
| ('AAPL', '2026-11-25') |       0.2763 |    -1.4946 |     8.8768 |

---

## get_skew_index
Calculate a SKEW index with the Cboe SKEW Index methodology, for any ticker with listed options: the risk-neutral skewness S of the log return over the coming `days`, read from the prices of out-of-the-money options and expressed as 100 - 10 S. A SKEW of 100 means the options price a symmetric distribution; the higher the index, the more the options price a large fall (tail risk). The Cboe SKEW of the S&P 500 has mostly ranged between 110 and 150.

The formula is as follows, per expiry with $$R = \ln (S_{T} / F_{0})$$, $$y_{i} = \ln (K_{i} / F_{0})$$ and the strikes $$K_{i}$$, prices $$Q (K_{i})$$ and intervals $$\Delta K_{i}$$ of the VIX methodology:

$$
P_{1} = - \frac{e^{rT} \sum Q(K_{i}) \Delta K_{i}}{K_{i}^{2}} + \epsilon_{1}
$$

$$
P_{2} = \frac{e^{rT} \sum 2 (1 - y_{i}) Q(K_{i}) \Delta K_{i}}{K_{i}^{2}} + \epsilon_{2}
$$

$$
P_{3} = \frac{e^{rT} \sum 3 (2 y_{i} - y_{i}^{2}) Q(K_{i}) \Delta K_{i}}{K_{i}^{2}} + \epsilon_{3}
$$

$$
\epsilon_{1} = - \left(1 + \ln\left(\frac{F_{0}}{K_{0}}\right) - \frac{F_{0}}{K_{0}}\right)
$$

$$
\epsilon_{2} = 2 \ln\left(\frac{K_{0}}{F_{0}}\right) \left(\frac{F_{0}}{K_{0}} - 1\right) + \ln\left(\frac{K_{0}}{F_{0}}\right)^{2}
$$

$$
\epsilon_{3} = 3 \ln\left(\frac{K_{0}}{F_{0}}\right)^{2}\left(\frac{\ln\left(\frac{K_{0}}{F_{0}}\right)}{3} - 1 + \frac{F_{0}}{K_{0}}\right)
$$

$$
S = \frac{P_{3} - 3 P_{1} P_{2} + 2 P_{1}^{3}}{(P_{2} - P_{1}^{2})^{\frac{3}{2}}}
$$

and over the near and next term around `days`:

$$
w = \frac{T_{\text{next}} - T_{\text{days}}}{T_{\text{next}} - T_{\text{near}}}
$$

$$
\text{Skewness} = w S_{\text{near}} + (1 - w) S_{\text{next}}
$$

$$
\text{SKEW Index} = 100 - 10 \;\text{Skewness}
$$

$$P_{1}$$, $$P_{2}$$ and $$P_{3}$$ are the prices of R, $$R^{2}$$ and $$R^{3}$$, the $$\epsilon$$ terms correct for the expansion around the forward price $$F_{0}$$ while the puts and calls are split at $$K_{0}$$, the first strike at or below it, and r is the continuously compounded risk free rate. The terms, the forward price, $$K_{0}$$ and the strikes used are those of the VIX methodology (see get_model_free_implied_volatility), as the white paper prescribes. $$\epsilon_{2}$$ holds the full $$\ln (K_{0} / F_{0})^{2}$$ of the expansion of $$R^{2}$$ around $$K_{0}$$, where the white paper prints half of it (see market_metrics_model.get_cboe_skewness); for index options the difference is negligible. Unlike the variance of the VIX, the skewness is interpolated linearly in time. Applied to the S&P 500 index options ("^SPX") over 30 days it approximates the Cboe SKEW Index, which uses the Cboe's own quotes and Treasury bill rates per expiry.

**Also known as:** Cboe SKEW, tail risk index, black swan index, implied skewness index.

**References:**

- paper | Cboe Global Markets (2010). "The Cboe SKEW Index - SKEW." White paper.
- paper | Bakshi, G., Kapadia, N. and Madan, D. (2003). "Stock Return Characteristics, Skew Laws, and the Differential Pricing of Individual Equity Options." The Review of Financial Studies, 16(1), 101-143.

**Args:**

- <u>days (int, optional):</u> The constant maturity in calendar days, at least 1. Defaults to 30.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker the Near-Term and Next-Term Expiration and Skewness, the
Forward Price of the near term, the Skewness at `days` and the SKEW Index.

**Notes:**

- The skewness depends on how far the strikes reach into the tails, so a stock with
few listed strikes shows a SKEW closer to 100 than its options imply.
- A target shorter than the nearest usable expiry (at least 7 days away) is
extrapolated from the two nearest terms, as in the Cboe method. A target beyond
the longest usable expiry raises a ValueError naming the ticker and that expiry.
- Outside market hours (at the weekend) Yahoo Finance reports a bid and ask of 0, so
a ValueError names the ticker and expiry instead of a NaN index. Last traded
prices are not used: they are of different moments of the session, which gives a
forward price and tails that do not agree (for ^SPX a skewness of -12 on a Sunday).
- The near and next term are the expiries just before and after `days` (at least 7
days away), whichever weekday they expire on. The Cboe VIX only uses the SPX
options that expire on a Friday, more than 23 and less than 37 days away, so for
^SPX the terms can be daily expiries with fewer strikes than the Cboe's.
- The time to each expiry runs from the current time to 16:00 New York time on the
expiration date, in minutes over the 525,600 minutes of a year. The risk free rate
comes from the historical data, so leave end_date at today: a warning is logged
when the history ends more than 5 days before today.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["^SPX", "AAPL"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.options.get_skew_index(
    show_columns=["Near-Term Expiration", "Next-Term Expiration", "Skewness", "SKEW Index"]
)
```

Which returns:

|      | Near-Term Expiration   | Next-Term Expiration   |   Skewness |   SKEW Index |
|:-----|:-----------------------|:-----------------------|-----------:|-------------:|
| ^SPX | 2026-12-18             | 2026-12-21             |    -4.2626 |      142.626 |
| AAPL | 2026-12-18             | 2026-12-24             |    -1.7288 |      117.288 |

---

## get_variance_swap
Calculate the fair strike of a variance swap up to every expiry from the option chain: the variance at which a swap on the stock's realized variance is worth nothing today, replicated with the discrete strike weights of Demeterfi, Derman, Kamal and Zou (1999), and with a strike the value of a swap, also of one traded in the past.

A variance swap pays the variance the stock realizes up to maturity minus the strike; the fair strike is the price of a portfolio of out-of-the-money options that replicates the log contract, whose payoff grows with the realized variance whatever the path:

$$
f(S) = \left(\frac{2}{T}\right) \left[\frac{S - S^{*}}{S^{*}} - \ln\left(\frac{S}{S^{*}}\right)\right]
$$

$$
w(K_{i}) = \text{the change in the slope of}\; f \;\text{at}\; K_{i},\;\; \text{with } f \text{ linear between the strikes}
$$

$$
\text{Fair Variance} = \left(\frac{2}{T}\right) \left[\ln\left(\frac{F}{S^{*}}\right) - \left(\frac{F}{S^{*}} - 1\right)\right] + e^{rT}\left[\sum w(K_{p}) P(K_{p}) + \sum w(K_{c}) C(K_{c})\right]
$$

$$
\text{Fair Volatility} = \sqrt{\text{Fair Variance}}
$$

$$
\text{Realized Variance} = \frac{252}{n} \sum \ln\left(\frac{S_{i}}{S_{i-1}}\right)^{2},\;\; \text{over the } n \text{ returns since trade\_date}
$$

$$
\text{Value} = e^{- r (T - t)}\left[\frac{t}{T} \;\text{Realized Variance} + \frac{T - t}{T} \;\text{Fair Variance} - \text{Strike}^{2}\right]
$$

with the forward price F and the boundary strike $$S^{*} = K_{0}$$, the highest strike at or below it, from put-call parity as in the Cboe VIX methodology, puts below S* and calls above it. The Cboe Variance column is the VIX methodology's variance of the same expiry (see get_model_free_implied_volatility): it discretises the same integral with the midpoint rule, so the two agree when the strikes are close together and the Fair Variance replicates the payoff at the quoted strikes exactly when they are not.

**Also known as:** variance swap rate, variance strike, fair variance, DDKZ replication.

**References:**

- paper | Demeterfi, K., Derman, E., Kamal, M. and Zou, J. (1999). "More Than You Ever Wanted to Know About Volatility Swaps." Goldman Sachs Quantitative Strategies Research Notes.
- paper | Carr, P. and Madan, D. (1998). "Towards a Theory of Volatility Trading." In Volatility: New Estimation Techniques for Pricing Derivatives, Risk Books, 417-427.
- library | Referenced against QuantLib's [ReplicatingVarianceSwapEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_replicating_variance_swap_engine.html){:target="_blank"}
- library | Referenced against FinancePy's [EquityVarianceSwap.fair_strike](https://github.com/domokane/FinancePy/blob/V1.1.2/financepy/products/equity/equity_variance_swap.py#L102){:target="_blank"}
- library | Referenced against FinancePy's [EquityVarianceSwap.value](https://github.com/domokane/FinancePy/blob/V1.1.2/financepy/products/equity/equity_variance_swap.py#L61){:target="_blank"}
- library | Shares similar logic as QuantLib's [VarianceSwap](https://www.quantlib.org/reference/class_quant_lib_1_1_variance_swap.html){:target="_blank"}

**Args:**

- <u>expiration_dates (list[str] &#124; None, optional):</u> The expiries to use, the maturities
of the swaps. Defaults to None, the nearest `number_of_expirations` expiries.
- <u>number_of_expirations (int, optional):</u> The number of nearest expiries to use when
no dates are given, at least 1. Defaults to 4.
- <u>strike (float &#124; None, optional):</u> The volatility strike of the swap as a decimal
(0.25 for 25%), whose square is the variance strike. Defaults to None, which
gives the fair strike only.
- <u>trade_date (str &#124; None, optional):</u> The date the swap was traded, whose returns
since then count towards the realized variance. Requires a strike. Defaults to
None, a swap traded today.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker and expiry the Days to Expiration, Forward Price, Boundary
Strike, Fair Variance, Fair Volatility and Cboe Variance (annualized, as decimals),
and with a strike the Variance Strike, the Realized Variance and its share of the
swap (Elapsed Fraction) and the Variance Swap Value per unit of variance notional.

**Notes:**

- The value is per unit of variance notional, paying $$\sigma^{2} - K^{2}$$ on decimal variances. A
vega notional $$N_{\text{vega}}$$, the profit per volatility point, is $$N_{\text{vega}}$$ / (2 Strike) units of
variance notional, so Value × 100 / (2 Strike) is the value per unit of vega notional
in volatility points.
- The fair strike uses the strip of the Cboe methodology: options with a bid, walking
away from $$K_{0}$$ until two strikes in a row have none. Outside US market hours Yahoo
Finance reports a bid of 0, and the fair strike is NaN.
- The realized variance counts the daily log returns of the Adjusted Close since
trade_date, without subtracting their mean, as variance swaps settle. The share t/T
counts those returns against the returns still to come, the weekdays up to the
expiry, and the value discounts over the time to expiration with the risk free rate
of the historical data (continuously compounded). Leave end_date at today: a warning
is logged when the history ends more than 5 days before today.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "^SPX"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.options.get_variance_swap(
    number_of_expirations=2,
    strike=0.3,
    show_columns=["Forward Price", "Fair Variance", "Fair Volatility", "Cboe Variance", "Variance Swap Value"],
)
```

Which returns:

|                        |   Forward Price |   Fair Variance |   Fair Volatility |   Cboe Variance |   Variance Swap Value |
|:-----------------------|----------------:|----------------:|------------------:|----------------:|----------------------:|
| ('AAPL', '2026-11-25') |          349.55 |          0.1281 |            0.358  |          0.1281 |                0.0381 |
| ('AAPL', '2026-11-27') |          349.65 |          0.0887 |            0.2979 |          0.0887 |               -0.0013 |
| ('^SPX', '2026-11-24') |         7253.05 |          0.1076 |            0.328  |          0.1076 |                0.0176 |
| ('^SPX', '2026-11-25') |         7255    |          0.1055 |            0.3248 |          0.1055 |                0.0155 |

---

## get_delta_hedging_backtest
Calculate the realized profit and loss of selling a European option on each ticker and delta hedging it on the ticker's own prices until it expires `days` trading days later: how much the hedged seller gained or lost when the volatility the stock realized differed from the one the option was sold at (Hull, 2022, chapter 19).

The option is sold at its Black-Scholes value, the hedge holds its delta in shares, pays a proportional cost on every trade, receives the dividends on the shares held and keeps the rest in cash at the risk free rate:

$$
\text{Option Value} = \text{Black-Scholes value at the volatility}\; \sigma \;\text{on the start date}
$$

$$
\text{Cash}_{i+1} = \text{Cash}_{i} e^{r \Delta t} + \Delta_{i} D_{i+1} - (\Delta_{i+1} - \Delta_{i}) S_{i+1} - k \left|\Delta_{i+1} - \Delta_{i}\right| S_{i+1}
$$

$$
\text{Profit and Loss} = e^{- rT}\left[\text{Cash}_{T} + \Delta_{T} S_{T} - \operatorname{Payoff}(S_{T})\right]
$$

The profit and loss shows what the volatility the option was sold at earned against the volatility the stock then realized: the seller gains about ½ $$\Gamma S^{2} (\sigma^{2} - \sigma_{\text{realized}}^{2})$$ per unit of time (Wilmott, 2006), so a positive result means the stock moved less than the option priced, less the costs of hedging (Leland, 1985).

**Also known as:** delta hedging P&L, hedged option P&L, gamma scalping backtest, realized hedging error.

**References:**

- paper | Hull, J. C. (2022). "Options, Futures, and Other Derivatives." 11th edition, chapter 19.
- paper | Leland, H. E. (1985). "Option Pricing and Replication with Transactions Costs." The Journal of Finance, 40(5), 1283-1301.
- paper | Wilmott, P. (2006). "Paul Wilmott on Quantitative Finance." 2nd edition, chapter 12.

**Args:**

- <u>days (int, optional):</u> The trading days from the sale to expiration, at least 1. Defaults to 63,
about three months.
- <u>start_date (str &#124; None, optional):</u> The date the option is sold, or the last
trading day before it. Defaults to None, `days` trading days before the end
of the historical data, so the option expires on its last date.
- <u>moneyness (float, optional):</u> The strike as a fraction of the stock price on the
start date. Defaults to 1.0, at the money.
- <u>volatility (float &#124; None, optional):</u> The volatility the option is sold and hedged
at, such as an implied volatility, for every ticker, 0 or above (at 0 the option
is sold at its discounted intrinsic value and the delta is 0 or 1). Defaults to
None, the volatility of the year of daily returns up to the start date, which is
known on that date.
- <u>put_option (bool, optional):</u> Whether the option is a put. Defaults to False.
- <u>transaction_cost (float, optional):</u> The cost of a trade as a fraction of its value
(0.001 is 10 basis points), 0 or above. Defaults to 0.0.
- <u>rebalancing_days (int, optional):</u> The trading days between rebalances. Defaults to
1, daily.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker the Start Date, Expiration Date, Stock Price, Strike Price,
Volatility, Realized Volatility, Option Value, Payoff, Transaction Costs and Profit
and Loss. The costs and the profit and loss are discounted to the start date.

**Raises:**

InvalidArgumentError: When the days or rebalancing days are below 1, the moneyness
is not positive, or the volatility or transaction cost is negative.

**Notes:**

- Time runs on each ticker's own trading days, 252 to a year, the same clock as the
volatility, so the option's time value and the variance the stock realizes count
the same days.
- The stock follows the traded Close and the hedge receives the cash dividends on
their ex-dates; the option is valued with the trailing dividend yield and the risk
free rate on the start date, both continuously compounded.
- At expiration the hedge moves to the position the option settles with (one share
for a call in the money, none out of the money), and that trade pays the cost as
well, as for physical settlement.
- The Realized Volatility is the square root of the mean squared daily log return of
the Adjusted Close over the option's life, annualized, as a variance swap settles.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2023-01-01", end_date="2025-12-31"
)

toolkit.options.get_delta_hedging_backtest(
    start_date="2025-06-02",
    transaction_cost=0.0005,
    show_columns=["Volatility", "Realized Volatility", "Option Value", "Payoff", "Transaction Costs", "Profit and Loss"],
)
```

Which returns:

|      |   Volatility |   Realized Volatility |   Option Value |   Payoff |   Transaction Costs |   Profit and Loss |
|:-----|-------------:|----------------------:|---------------:|---------:|--------------------:|------------------:|
| AAPL |       0.3304 |                0.2141 |        14.2012 |    28.02 |              0.2146 |            2.9596 |
| MSFT |       0.2574 |                0.1516 |        25.7479 |    43.15 |              0.3291 |            5.2927 |

---

## get_delta_hedging_simulation
Calculate the distribution of the hedging error of selling a European option and delta hedging it: how much the hedged seller can gain or lose across simulated Geometric Brownian Motion paths of the stock from its price on the start date.

Each path is hedged as in get_delta_hedging_backtest: the option is sold at its Black-Scholes value at the implied volatility, the hedge holds its delta, rebalanced every `rebalancing_days` trading days at a proportional cost, while the stock moves with the volatility:

$$
S(t + \Delta t) = S(t) e^{\left(r - q - \frac{\sigma^{2}}{2}\right) \Delta t + \sigma \sqrt{\Delta t} Z},\;\; Z \sim N(0,\; 1),\;\; \Delta t = \frac{1}{252}
$$

$$
\text{Profit and Loss} = e^{- rT}\left[\text{Cash}_{T} + \Delta_{T} S_{T} - \operatorname{Payoff}(S_{T})\right],\;\; \text{per path}
$$

$$
\text{Approximate Standard Deviation} = \frac{\sqrt{\frac{\pi}{4}} \cdot \text{Vega} \cdot \sigma}{\sqrt{N}}
$$

Hedging at discrete times leaves an error whose mean is near zero and whose standard deviation falls with the square root of the number of rebalances N, as Boyle and Emanuel (1980) and Derman and Kamal (1999) derive for an at-the-money option; the last column gives their approximation. An implied volatility above the volatility gives the seller a profit on average, transaction costs a loss that grows as the hedge is rebalanced more often (Leland, 1985).

FinancePy's simulate_hedge_paths reports the profit and loss at expiration rather than discounted and closes the hedge in cash at expiration.

**Also known as:** hedging error distribution, discrete hedging simulation, delta hedging Monte Carlo.

**References:**

- paper | Boyle, P. P. and Emanuel, D. (1980). "Discretely Adjusted Option Hedges." Journal of Financial Economics, 8(3), 259-282.
- paper | Derman, E. and Kamal, M. (1999). "When You Cannot Hedge Continuously: The Corrections of Black-Scholes." Risk, 12(1), 82-85.
- paper | Leland, H. E. (1985). "Option Pricing and Replication with Transactions Costs." The Journal of Finance, 40(5), 1283-1301.
- library | Referenced against FinancePy's [simulate_hedge_paths](https://github.com/domokane/FinancePy/blob/V1.1.2/financepy/models/black_scholes_hedging_sim.py#L592){:target="_blank"}

**Args:**

- <u>days (int, optional):</u> The trading days to expiration, at least 1. Defaults to 63, about three
months.
- <u>start_date (str &#124; None, optional):</u> The date of the stock price, volatility, risk
free rate and dividend yield, or the last trading day before it. Defaults to
None, the last date of the historical data.
- <u>moneyness (float, optional):</u> The strike as a fraction of the stock price. Defaults
to 1.0, at the money.
- <u>volatility (float &#124; None, optional):</u> The volatility the stock moves with, for every
ticker, 0 or above (at 0 every path grows at the risk free rate less the
dividend yield). Defaults to None, the volatility of the year of daily returns
up to the start date.
- <u>implied_volatility (float &#124; None, optional):</u> The volatility the option is sold and
hedged at, 0 or above (at 0 the option is sold at its discounted intrinsic value
and the delta is 0 or 1). Defaults to None, the volatility the stock moves with.
- <u>put_option (bool, optional):</u> Whether the option is a put. Defaults to False.
- <u>transaction_cost (float, optional):</u> The cost of a trade as a fraction of its value
(0.001 is 10 basis points), 0 or above. Defaults to 0.0.
- <u>rebalancing_days (int, optional):</u> The trading days between rebalances. Defaults to
1, daily.
- <u>simulations (int, optional):</u> The number of simulated paths, at least 1. Defaults to 10,000.
- <u>seed (int &#124; None, optional):</u> The seed of the random numbers, None for a different
draw on every call. Defaults to 0.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker the Stock Price, Strike Price, Volatility, Implied
Volatility, Option Value, the Mean, Standard Deviation and 5% and 95% Quantiles of
the Profit and Loss, the Mean Transaction Costs (both discounted to the start date)
and the Approximate Standard Deviation.

**Raises:**

InvalidArgumentError: When the days or rebalancing days are below 1, the moneyness
is not positive, the simulations are not a whole number of at least 1, or the
volatility, implied volatility or transaction cost is negative.

**Notes:**

- The paths drift at the risk free rate. The real-world drift barely moves the hedging
error, since the hedge removes the exposure to the direction of the stock.
- The dividend yield is the trailing yield on the start date, continuously
compounded, paid on the shares held; the risk free rate is continuously compounded.
- The approximate standard deviation holds near the money without costs; the
simulated one also covers other strikes and costs.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2024-01-01", end_date="2025-12-31"
)

toolkit.options.get_delta_hedging_simulation(
    start_date="2025-12-31",
    rebalancing_days=5,
    transaction_cost=0.0005,
    show_columns=["Option Value", "Mean Profit and Loss", "Standard Deviation", "Approximate Standard Deviation"],
)
```

Which returns:

|      |   Option Value |   Mean Profit and Loss |   Standard Deviation |   Approximate Standard Deviation |
|:-----|---------------:|-----------------------:|---------------------:|---------------------------------:|
| AAPL |        18.7557 |                -0.2161 |               4.1012 |                           4.2758 |
| MSFT |        25.3213 |                -0.3942 |               5.4501 |                           5.6839 |

---

## get_exchange_option
Calculate the price of an option to exchange a second asset (the benchmark by default) for each ticker, an outperformance option: what the right to receive the ticker for the second asset at expiration is worth, with the formula of Margrabe (1978).

The option receives one share of the ticker and delivers the number of units of the second asset that are worth the exchange ratio times the ticker's price today, so at an exchange ratio of 1 it pays at expiration what the ticker gained over the second asset since today, if anything, per share of the ticker.

Measured in units of the second asset the payoff is a call on the ratio of the two prices, so the risk-free rate drops out and the volatility is that of the ratio. An American option may be exercised at any time, which is an American call on the ticker with the second asset as strike, a risk-free rate of q2 and a dividend yield of q1 (Bjerksund and Stensland, 1993), priced with the QD+ exercise boundary and its integral (Li, 2010; Andersen, Lake and Offengenden, 2016), within about 0.1% of a 999-step Leisen-Reimer tree. Without a dividend yield on the ticker early exercise is never optimal and the American option is worth the European one.

The formula is as follows:

$$
S_{2} = \text{Exchange Ratio} \cdot S_{1},\;\; \text{the value today of the units of the second asset delivered}
$$

$$
\text{Exchange} = S_{1} \cdot e^{- q_{1} \cdot T} \cdot N(d_{1}) - S_{2} \cdot e^{- q_{2} \cdot T} \cdot N(d_{2})
$$

$$
\sigma = \sqrt{\sigma 1^{2} + \sigma 2^{2} - 2 \rho \sigma 1 \sigma 2}
$$

$$
d_{1} = \frac{\ln\left(\frac{S_{1}}{S_{2}}\right) + \left(q_{2} - q_{1} + \frac{\sigma^{2}}{2}\right) \cdot T}{\sigma \sqrt{T}},\;\; d_{2} = d_{1} - \sigma \sqrt{T}
$$

Where S1 is the ticker's price (the traded close on the pricing date), S2 the second asset's price, $$\sigma_{1}$$ and $$\sigma_{2}$$ the annualized volatilities (the standard deviation of the daily returns over the trailing 252 trading days of each times √252), $$\rho$$ the correlation of the daily returns of the two over the trailing 252 days on which both traded, q1 and q2 the dividend yields (ln(1 + dividend yield), continuously compounded), T the time to expiration in years (days / 365) and N the cumulative standard normal distribution.

Options on other two-asset payoffs, and the exchange option on prices and correlations of your own, are priced by the model functions in financetoolkit.options.multiasset.multi_asset_model.

See: Margrabe, W. (1978), "The Value of an Option to Exchange One Asset for Another", Journal of Finance, 33(1), 177-186; Bjerksund, P. & Stensland, G. (1993), "American Exchange Options and a Put-Call Transformation: A Note", Journal of Business Finance & Accounting, 20(5), 761-764; Haug, E. G. (2007), The Complete Guide to Option Pricing Formulas, 2nd ed., chapter 5. The American value is checked against a Leisen-Reimer tree of 999 steps on the call it equals (QuantLib's AnalyticAmericanMargrabeEngine takes the Bjerksund-Stensland (1993) approximation, a lower bound about 1% below it).

**Also known as:** Margrabe option, exchange option, outperformance option, swap option.

**References:**

- library | Referenced against QuantLib's [AnalyticEuropeanMargrabeEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_analytic_european_margrabe_engine.html){:target="_blank"}
- library | Shares similar logic as QuantLib's [AnalyticAmericanMargrabeEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_analytic_american_margrabe_engine.html){:target="_blank"}

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose prices, volatilities and correlation the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price or a month of returns shared with the second asset is left out with a warning.
Defaults to None, which uses the last date of the historical data.
- <u>second_ticker (str &#124; None, optional):</u> The asset delivered, "Benchmark" or one of the tickers (which is
then left out of the rows). Defaults to None, which uses the benchmark.
- <u>american_option (bool, optional):</u> Whether the option can be exercised before expiration. Defaults to
False.
- <u>exchange_ratio (float, optional):</u> The value today of the units of the second asset delivered, as a
share of the ticker's price: below 1 the option is in the money, above 1 out of the money. Defaults
to 1.0, at the money.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Exchange option values per share of the ticker, with the tickers as the index and the
expiration dates as the columns.

**Raises:**

InvalidArgumentError: If exchange_ratio is not positive.
ValueError: If the second asset is not in the historical data.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

exchange_option = toolkit.options.get_exchange_option(expiration_time_range=91)

exchange_option[["2026-01-30", "2026-03-01", "2026-03-31"]]
```

Which returns:

| Ticker   |   2026-01-30 |   2026-03-01 |   2026-03-31 |
|:---------|-------------:|-------------:|-------------:|
| AAPL     |       6.7664 |       9.5415 |      11.659  |
| MSFT     |       9.5013 |      13.351  |      16.2696 |

---

## get_spread_option
Calculate the price of a European spread option of each ticker over a second asset (the benchmark by default): what an option on how much the ticker gains over the second asset is worth, with the closed-form approximation of Bjerksund and Stensland (2011) or of Kirk (1995).

The option is on one share of the ticker less the units of the second asset worth the same today, so the spread starts at 0 and the call pays max(S1 - S2 - K, 0) at expiration, where S1 - S2 is what the ticker gained over the second asset per share. The strikes run from the strike price range below to the strike price range above a spread of 0, as a share of the ticker's price.

The spread of two lognormal prices has no closed-form distribution. Kirk takes F2 + K as one lognormal price, and Bjerksund and Stensland exercise where F1 exceeds a boundary fitted to the exercise region, which gives a lower bound that is closer to the exact price. At a strike of 0 both are Margrabe's exact exchange option (get_exchange_option).

The formula is as follows:

$$
F_{1} = S_{1} \cdot e^{(r - q_{1}) \cdot T},\;\; F_{2} = S_{2} \cdot e^{(r - q_{2}) \cdot T},\;\; \text{with}\;\; S_{2} = S_{1} \;\text{today}
$$

$$
\text{Kirk Call} = e^{- rT} \cdot (F_{1} \cdot N(d_{1}) - (F_{2} + K) \cdot N(d_{1} - \sigma K \sqrt{T})),\;\; \sigma K^{2} = \sigma 1^{2} - 2 \rho \sigma 1 \sigma 2 \cdot b + \sigma 2^{2} \cdot b^{2},\;\; b = \frac{F_{2}}{F_{2} + K}
$$

$$
d_{1} = \frac{\ln\left(\frac{F_{1}}{F_{2} + K}\right) + \frac{\sigma K^{2} \cdot T}{2}}{\sigma K \sqrt{T}}
$$

$$
\text{Bjerksund-Stensland Call} = e^{- rT} \cdot (F_{1} \cdot N(e_{1}) - F_{2} \cdot N(e_{2}) - K \cdot N(e_{3}))
$$

$$
e_{1} = \frac{\ln\left(\frac{F_{1}}{F_{2} + K}\right) + \left(\frac{\sigma 1^{2}}{2} - b \rho \sigma 1 \sigma 2 + \frac{b^{2} \sigma 2^{2}}{2}\right) \cdot T}{\sigma K \sqrt{T}}
$$

$$
e_{2} = \frac{\ln\left(\frac{F_{1}}{F_{2} + K}\right) + \left(- \frac{\sigma 1^{2}}{2} + \rho \sigma 1 \sigma 2 + \frac{b^{2} \sigma 2^{2}}{2} - b \sigma 2^{2}\right) \cdot T}{\sigma K \sqrt{T}}
$$

$$
e_{3} = \frac{\ln\left(\frac{F_{1}}{F_{2} + K}\right) + \left(- \frac{\sigma 1^{2}}{2} + \frac{b^{2} \sigma 2^{2}}{2}\right) \cdot T}{\sigma K \sqrt{T}}
$$

$$
\text{Put} = \text{Call} - e^{- rT} \cdot (F_{1} - F_{2} - K)
$$

Where S1 is the ticker's price (the traded close on the pricing date), K the strike price, r the continuously compounded risk-free rate, q1 and q2 the dividend yields (ln(1 + dividend yield), continuously compounded), $$\sigma_{1}$$ and $$\sigma_{2}$$ the annualized volatilities (the standard deviation of the daily returns over the trailing 252 trading days of each times √252), $$\rho$$ the correlation of the daily returns of the two over the trailing 252 days on which both traded, T the time to expiration in years (days / 365) and N the cumulative standard normal distribution.

Spread options on prices, strikes and correlations of your own (such as a crack or a calendar spread of futures), are priced by the model function financetoolkit.options.multiasset.multi_asset_model.get_spread_option.

See: Kirk, E. (1995), "Correlation in the Energy Markets", in Managing Energy Price Risk, Risk Publications, 71-78; Bjerksund, P. & Stensland, G. (2014), "Closed Form Spread Option Valuation", Quantitative Finance, 14(10), 1785-1794; Haug, E. G. (2007), The Complete Guide to Option Pricing Formulas, 2nd ed., chapter 5.

**Also known as:** spread option, relative performance option, Kirk's approximation.

**References:**

- library | Referenced against QuantLib's [BjerksundStenslandSpreadEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_bjerksund_stensland_spread_engine.html){:target="_blank"}
- library | Referenced against QuantLib's [KirkEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_kirk_engine.html){:target="_blank"}

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose prices, volatilities, correlation and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price or a month of returns shared with the second asset is left out with a warning.
Defaults to None, which uses the last date of the historical data.
- <u>second_ticker (str &#124; None, optional):</u> The second asset, "Benchmark" or one of the tickers (which is
then left out of the rows). Defaults to None, which uses the benchmark.
- <u>put_option (bool, optional):</u> Whether the option is a put. Defaults to False.
- <u>method (str, optional):</u> The approximation. Options are: "bjerksund_stensland" (Bjerksund and Stensland,
2011, the more accurate), "kirk" (Kirk, 1995). Defaults to "bjerksund_stensland".
- <u>strike_price_range (float):</u> The range of the strike prices around a spread of 0, as a share of the
ticker's price, at most 0.5 (both approximations take the second asset's forward price plus the strike
as a lognormal price, which lower strikes bring close to zero). Defaults to 0.25, which gives strikes from -25 to 25 for a price of 100.
- <u>strike_step_size (float):</u> The step size of the strike prices. Defaults to 5, which gives the strikes
-25, -20, ..., 20 and 25 for a price of 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Spread option values per share of the ticker, with the tickers and strike prices as the
index and the expiration dates as the columns.

**Raises:**

InvalidArgumentError: If strike_price_range is not between 0 and 0.5, strike_step_size is not above 0 or
the method is not one of the two.
ValueError: If the second asset is not in the historical data.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

spread_option = toolkit.options.get_spread_option(
    strike_price_range=0.1, expiration_time_range=91
)

spread_option.loc["AAPL", ["2026-01-30", "2026-03-01", "2026-03-31"]]
```

Which returns:

|   Strike Price |   2026-01-30 |   2026-03-01 |   2026-03-31 |
|---------------:|-------------:|-------------:|-------------:|
|            -30 |      29.995  |      30.5915 |      31.4131 |
|            -25 |      25.2477 |      26.2471 |      27.3611 |
|            -20 |      20.7127 |      22.1749 |      23.58   |
|            -15 |      16.4979 |      18.431  |      20.1017 |
|            -10 |      12.7141 |      15.0607 |      16.9489 |
|             -5 |       9.4529 |      12.0938 |      14.1342 |
|              0 |       6.7664 |       9.5415 |      11.659  |
|              5 |       4.6569 |       7.3963 |       9.5148 |
|             10 |       3.0798 |       5.6345 |       7.6844 |
|             15 |       1.9575 |       4.2199 |       6.1438 |
|             20 |       1.1965 |       3.1087 |       4.8645 |
|             25 |       0.7041 |       2.2539 |       3.8161 |
|             30 |       0.3994 |       1.6094 |       2.9672 |

---

## get_black_scholes_model
Calculate the Black Scholes Model: what European calls and puts on each ticker are worth today, for a range of strike prices and times to expiration, when the stock follows a lognormal process with a constant volatility.

The Black Scholes Model is a mathematical model used to estimate the price of European-style options. It is widely used by traders and investors to determine the theoretical value of an option, and to assess the potential risks and rewards of a position.

Within Risk Management, defining the theoretical value of an option is important to assess the potential risk and rewards of an option position. A position that could be used to hedge a portfolio, for example, is a long put option. The theoretical value of this option can be used to determine the potential risk and rewards of this position.

The Black Scholes Model is based on several assumptions, including the following:

- The option is European and can only be exercised at expiration.
- The underlying stock follows a lognormal distribution.
- The risk-free rate and volatility of the underlying stock are known and constant.
- The returns on the underlying stock are normally distributed.

By default the stock price (the traded close), risk free rate, dividend yield and volatility of the most recent date are used; changing the start date prices the option as of that date instead. The volatility is the annualized standard deviation of the daily returns over the year before that date and the dividend yield the dividends of the 365 days up to that date relative to its close, so an earlier start date only uses what was known on that date. The exception is a date in the first year of the price history: without a full year before it, it takes the dividend yield of the first date that has one.

The formulas are as follows:

$$
d_{1} = \frac{\ln\left(\frac{S}{K}\right) + \left(r - q + \frac{\sigma^{2}}{2}\right) \cdot t}{\sigma \cdot \sqrt{t}}
$$

$$
d_{2} = d_{1} - \sigma \cdot \sqrt{t}
$$

$$
\text{Call Option Price} = S \cdot e^{- q \cdot t} \cdot N(d_{1}) - K \cdot e^{- r \cdot t} \cdot N(d_{2})
$$

$$
\text{Put Option Price} = K \cdot e^{- r \cdot t} \cdot N(- d_{2}) - S \cdot e^{- q \cdot t} \cdot N(- d_{1})
$$

Where S is the stock price, K is the strike price, r is the risk free rate, q is the dividend yield, $$\sigma$$ is the volatility, t is the time to expiration, N(d1) is the cumulative normal distribution of d1 and N(d2) is the the cumulative normal distribution of d2.

The model price is only as good as its volatility input, and here that input is realised (historical) volatility, while traded options are priced off implied volatility, which usually differs from it and varies by strike and expiry. Practitioners therefore use the Black Scholes value as a benchmark and compare it with market prices from `get_option_chains`, or back the market's volatility out with `get_implied_volatility`. Deep out-of-the-money options are most sensitive to that choice, since the model's flat volatility ignores the skew.

Dividends are paid in cash on their ex-dividend dates, which the dividend yield q spreads evenly over the year. For short options that difference matters: an option that expires just after an ex-date loses the whole dividend, one that expires just before it none of it. With the escrowed or the Haug-Haug-Lewis dividend model the dividend yield is replaced by the projected cash dividends: the latest dividend per share before the pricing date, repeated at the median interval between its last ex-dates (see options_model.get_projected_dividends), so a past pricing date only uses what was known on that date.

- Escrowed (Hull, 2022, chapter 17): the Black-Scholes formula with $$q = 0$$ on $$S^{*} = S - \sum D_{i} \cdot e^{- r \cdot t_{i}}$$, the stock price net of the present value of the dividends up to expiration.
- Haug-Haug-Lewis (Haug, Haug and Lewis, 2003): the stock price drops by $$D_{i}$$ at $$t_{i}$$ and the option value is integrated over the lognormal stock price at each ex-date, from the Black-Scholes value after the last dividend backwards: $$V_{i} (x) = e^{- r \cdot (t_{i + 1} - t_{i})} \cdot E [V_{i + 1} (S_{t_{i + 1}} - D_{i + 1})]$$.

Where $$D_{i}$$ is the cash dividend with ex-date $$t_{i}$$ years after the pricing date. The escrowed model is the market convention; it applies the volatility to S* instead of S, which the Haug-Haug-Lewis method does not, so the latter gives slightly higher prices when the dividends are large.

**Also known as:** BSM, Black-Scholes-Merton, option pricing model, escrowed dividend model, discrete dividends.

**References:**

- library | Referenced against QuantLib's [AnalyticDividendEuropeanEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_analytic_dividend_european_engine.html){:target="_blank"} (escrowed)
- library | Referenced against QuantLib's [CashDividendEuropeanEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_cash_dividend_european_engine.html){:target="_blank"} (Haug-Haug-Lewis)

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>put_option (bool, optional):</u> Whether to calculate the put option price. Defaults to False which means
it will calculate the call option price.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None, which
uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield. Only used with
dividends="yield".
- <u>dividends (str, optional):</u> How the dividends enter the price. Options are: "yield" (a continuous
dividend yield), "escrowed" (the projected cash dividends, escrowed model), "haug_haug_lewis" (the
projected cash dividends, stock price dropping on each ex-date). Defaults to "yield".
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Black Scholes values containing the tickers and strike prices as the index and the
time to expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NVDA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

black_scholes = toolkit.options.get_black_scholes_model(
    strike_price_range=0.15, strike_step_size=5, expiration_time_range=91
)

black_scholes.loc["NVDA", ["2026-01-30", "2026-03-01", "2026-03-31"]]
```

Which returns:

|   Strike Price |   2026-01-30 |   2026-03-01 |   2026-03-31 |
|---------------:|-------------:|-------------:|-------------:|
|            160 |      28.7163 |      31.7618 |      34.5225 |
|            165 |      24.6254 |      28.1297 |      31.1413 |
|            170 |      20.8379 |      24.7547 |      27.9827 |
|            175 |      17.3918 |      21.6473 |      25.0494 |
|            180 |      14.313  |      18.8122 |      22.3412 |
|            185 |      11.6133 |      16.2484 |      19.855  |
|            190 |       9.29   |      13.9503 |      17.5848 |
|            195 |       7.3277 |      11.9077 |      15.5227 |
|            200 |       5.7004 |      10.1071 |      13.6589 |
|            205 |       4.3748 |       8.5321 |      11.9824 |
|            210 |       3.3136 |       7.1649 |      10.4811 |

---

## get_binomial_model
Calculate the Binomial Option Pricing Model: what European and American calls and puts on each ticker are worth at every node of a binomial tree of stock prices, from the payoffs at expiration back to today.

It creates a binomial tree of price paths for the underlying asset and works backwards through the tree to determine the price of the option at each node.

The tree of Cox, Ross and Rubinstein (1979) is the default. The variants choose the up and down movements and the probability differently, which changes how fast and how smoothly the price converges as the number of time steps grows:

- Jarrow-Rudd: equal probabilities of 1/2, with the moves centred on the drift.
- Tian: matches the first three moments of the lognormal distribution in each step.
- Trigeorgis: equal steps in the logarithm of the price with the drift in the probability, a tree that keeps its probability between 0 and 1 longer than Cox-Ross-Rubinstein.
- Leisen-Reimer: centred on the strike so the price converges smoothly at a rate of $$1 / n^{2}$$ instead of oscillating at 1 / n, with the probabilities from the Peizer-Pratt inversion of the normal distribution.
- Exact inversion: the Leisen-Reimer tree with the exact inverse of the binomial distribution, of which Joshi (2010) takes a fourth order expansion. It prices a European option at its Black-Scholes value at every number of steps and converges fastest for American options.

The Leisen-Reimer and exact inversion trees need an odd number of time steps; an even number is raised by one (the default of 10 becomes 11).

By default the stock price (the traded close), risk free rate, dividend yield and volatility of the most recent date are used; changing the start date prices the option as of that date instead. The volatility is the annualized standard deviation of the daily returns over the year before that date and the dividend yield the dividends of the 365 days up to that date relative to its close, so an earlier start date only uses what was known on that date. The exception is a date in the first year of the price history: without a full year before it, it takes the dividend yield of the first date that has one.

The formulas are as follows:

$$
\text{time step} \;(\Delta t) = \frac{T}{n}
$$

$$
\text{up movement} \;(u) = e^{\sigma \cdot \sqrt{\Delta t}}
$$

$$
\text{down movement} \;(d) = \frac{1}{u}
$$

$$
\text{risk neutral probability} \;(p) = \frac{e^{(r - q) \cdot \Delta t} - d}{u - d}
$$

$$
\text{Jarrow-Rudd:}\;\; u = e^{\nu \Delta t + \sigma \sqrt{\Delta t}},\;\; d = e^{\nu \Delta t - \sigma \sqrt{\Delta t}},\;\; p = \frac{1}{2}
$$

$$
\text{Tian:}\;\; v = e^{\sigma^{2} \Delta t},\;\; u = \frac{e^{(r - q) \Delta t} \cdot v}{2} \cdot (v + 1 + \sqrt{v^{2} + 2v - 3}),\;\; d = \frac{e^{(r - q) \Delta t} \cdot v}{2} \cdot (v + 1 - \sqrt{v^{2} + 2v - 3}),\;\; p = \frac{e^{(r - q) \Delta t} - d}{u - d}
$$

$$
\text{Trigeorgis:}\;\; \Delta x = \sqrt{\sigma^{2} \Delta t + \nu^{2} \Delta t^{2}},\;\; u = e^{\Delta x},\;\; d = \frac{1}{u},\;\; p = \frac{1}{2} + \frac{\nu \Delta t}{2 \Delta x}
$$

$$
\text{Leisen-Reimer and exact inversion:}\;\; p = h(d_{2}),\;\; u = \frac{e^{(r - q) \Delta t} \cdot h(d_{1})}{h(d_{2})},\;\; d = \frac{e^{(r - q) \Delta t} - p \cdot u}{1 - p}
$$

$$
\text{Peizer-Pratt (Leisen-Reimer):}\;\; h(z) = \frac{1}{2} + \frac{\operatorname{sign}(z)}{2} \cdot \sqrt{1 - e^{- \left(\frac{z}{n + \frac{1}{3} + \frac{0.1}{n + 1}}\right)^{2} \cdot \left(n + \frac{1}{6}\right)}}
$$

$$
\text{exact inversion:}\;\; h(z) \;\text{is the}\; p \;\text{at which} \;I_{p}\left(\frac{n + 1}{2},\; \frac{n + 1}{2}\right) = N(z)
$$

$$
\text{stock price at each node} = S \cdot u^{j} \cdot d^{n - j}
$$

$$
\text{call option price at expiration date} = \max(S - K,\; 0)
$$

$$
\text{put option price at expiration date} = \max(K - S,\; 0)
$$

For European Style options:

$$
\text{call option price at each node} = (p \cdot C_{u} + (1 - p) \cdot C_{d}) \cdot e^{- r \cdot \Delta t}
$$

$$
\text{put option price at each node} = (p \cdot P_{u} + (1 - p) \cdot P_{d}) \cdot e^{- r \cdot \Delta t}
$$

For American Style options:

$$
\text{call option price at each node} = \max(S - K,\; (p \cdot C_{u} + (1 - p) \cdot C_{d}) \cdot e^{- r \cdot \Delta t})
$$

$$
\text{put option price at each node} = \max(K - S,\; (p \cdot P_{u} + (1 - p) \cdot P_{d}) \cdot e^{- r \cdot \Delta t})
$$

Where S is the stock price, K is the strike price, r is the risk free rate, q is the dividend yield, $$\sigma$$ is the volatility, T is the time to expiration, $$\Delta t$$ is the length of one time step, j is the number of up movements, $$\nu = r - q - \sigma^{2} / 2$$, $$d_{1} = (\ln (S / K) + (r - q + \sigma^{2} / 2) \cdot T) / (\sigma \sqrt{T})$$, $$d_{2} = d_{1} - \sigma \sqrt{T}$$, $$I_{p}$$ is the regularized incomplete beta function, n is the number of time steps, $$C_{u}$$ is the call option price at the up movement, $$C_{d}$$ is the call option price at the down movement, $$P_{u}$$ is the put option price at the up movement and $$P_{d}$$ is the put option price at the down movement.

The resulting output is a DataFrame containing the tickers, strike prices and movements as the index and the time to expiration as the columns. The movements index contains the number of up movements and the number of down movements. The output is the binomial tree displayed in a table. E.g. when using 10 time steps, the table for each strike price from each company will contain the actual binomial tree as also depicted in the image found here: [https://en.wikipedia.org/wiki/Binomial_options_pricing_model#Method](https://en.wikipedia.org/wiki/Binomial_options_pricing_model#Method){:target="_blank"}

See: Cox, J. C., Ross, S. A., & Rubinstein, M. (1979), "Option Pricing: A Simplified Approach", Journal of Financial Economics, 7(3), 229-263; Jarrow, R., & Rudd, A. (1983), "Option Pricing", Irwin; Trigeorgis, L. (1991), "A Log-Transformed Binomial Numerical Analysis Method for Valuing Complex Multi-Option Investments", Journal of Financial and Quantitative Analysis, 26(3), 309-326; Tian, Y. (1993), "A Modified Lattice Approach to Option Pricing", Journal of Futures Markets, 13(5), 563-577; Leisen, D. P. J., & Reimer, M. (1996), "Binomial Models for Option Valuation - Examining and Improving Convergence", Applied Mathematical Finance, 3(4), 319-346; Joshi, M. S. (2010), "Achieving Higher Order Convergence for the Prices of European Options in Binomial Trees", Mathematical Finance, 20(1), 89-103. The Jarrow-Rudd, Tian, Trigeorgis and Leisen-Reimer trees agree with QuantLib's within 1e-9 and its J4 tree, Joshi's expansion, lies within 1e-6 of the exact inverse at 101 steps. An equal probabilities tree that matches the mean and variance of the log price is the Jarrow-Rudd tree.

**Also known as:** binomial tree, lattice model, option pricing, CRR, Leisen-Reimer, Jarrow-Rudd, Tian tree.

**References:**

- library | Referenced against QuantLib's [BinomialJRVanillaEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_binomial_vanilla_engine.html){:target="_blank"} (Jarrow-Rudd)
- library | Referenced against QuantLib's [BinomialTianVanillaEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_binomial_vanilla_engine.html){:target="_blank"} (Tian)
- library | Referenced against QuantLib's [BinomialTrigeorgisVanillaEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_binomial_vanilla_engine.html){:target="_blank"} (Trigeorgis)
- library | Referenced against QuantLib's [BinomialLRVanillaEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_binomial_vanilla_engine.html){:target="_blank"} (Leisen-Reimer)
- library | Referenced against QuantLib's [BinomialJ4VanillaEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_binomial_vanilla_engine.html){:target="_blank"} (exact inversion)

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>put_option (bool, optional):</u> Whether to calculate the put option price. Defaults to False which means
it will calculate the call option price.
- <u>american_option (bool, optional):</u> Whether to value an American option, which can be exercised at every
node, instead of a European option. Defaults to False.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>time_to_expiration (float):</u> The number of years to use for the time to expiration, above 0. Defaults to 1 which equals
one year.
- <u>time_steps (int):</u> The number of time steps to use for the binomial tree, from 1 to 1,000. Defaults to 10 which equals 10
time steps. This will be evenly distributed over the time to expiration.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None, which
uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>show_input_info (bool, optional):</u> Whether to show the input information, with the up and down movement
and the risk neutral probability per ticker, or per ticker and strike for the Leisen-Reimer and exact
inversion trees, which are centred on the strike. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.
- <u>method (str, optional):</u> The tree. Options are: "cox_ross_rubinstein" (Cox-Ross-Rubinstein),
"jarrow_rudd" (Jarrow-Rudd), "tian" (Tian), "trigeorgis" (Trigeorgis), "leisen_reimer"
(Leisen-Reimer), "exact_inversion" (exact inversion of the binomial distribution). Defaults to
"cox_ross_rubinstein".

**Returns:**

pd.DataFrame: Binomial Trees values containing the tickers, strike prices and movements as the index and the
time steps as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["KO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

binomial_model = toolkit.options.get_binomial_model(
    strike_price_range=0, strike_step_size=1, time_steps=5
)

binomial_model.loc["KO"]
```

Which returns:

|               |   2025-12-31 |   2026-03-14 |   2026-05-26 |   2026-08-07 |   2026-10-19 |   2026-12-31 |
|:--------------|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| (70, 'UUUUU') |       5.3445 |       8.4014 |      12.7664 |      18.5956 |      25.7101 |      33.495  |
| (70, 'DUUUU') |     nan      |       2.4212 |       4.24   |       7.2343 |      11.8932 |      18.4642 |
| (70, 'DDUUU') |     nan      |     nan      |       0.6695 |       1.3603 |       2.764  |       5.6163 |
| (70, 'DDDUU') |     nan      |     nan      |     nan      |       0      |       0      |       0      |
| (70, 'DDDDU') |     nan      |     nan      |     nan      |     nan      |       0      |       0      |
| (70, 'DDDDD') |     nan      |     nan      |     nan      |     nan      |     nan      |       0      |

---

## get_stock_price_simulation
Simulate the Stock Price based on the Binomial Model: the prices each ticker can reach after every combination of up and down movements up to expiration.

The binomial model is a mathematical model used to estimate the price of European and American style options. It creates a binomial tree of price paths for the underlying asset based on the stock price, its volatility and the time to expiration: each step multiplies the price by $$u = e^{\sigma \cdot \sqrt{\Delta t}}$$ or by $$d = 1 / u$$. The stock price is then simulated based on these up and down movements.

By default the most recent stock price is used, you can alter this by changing the start date. The volatility is the annualized standard deviation of the daily returns over the year before that date, so an earlier start date only uses what was known on that date.

The formulas are as follows:

$$
\text{up movement} \;(u) = e^{\sigma \cdot \sqrt{\Delta t}}
$$

$$
\text{down movement} \;(d) = \frac{1}{u}
$$

$$
\text{stock price at each node} = S \cdot u^{j} \cdot d^{n - j}
$$

Where S is the stock price, $$\sigma$$ is the volatility, $$\Delta t$$ is the length of a time step (the time to expiration divided by the number of time steps), j is the number of up movements and n is the number of time steps. The risk free rate and the dividend yield do not affect the tree.

The resulting output is a DataFrame containing the tickers and movements as the index and the time to expiration as the columns. The movements index contains the number of up movements and the number of down movements. The output is the binomial tree displayed in a table. E.g. when using 10 time steps, the table from each company will contain the actual binomial tree's stock prices as also depicted in the image found here: [https://en.wikipedia.org/wiki/Binomial_options_pricing_model#Method](https://en.wikipedia.org/wiki/Binomial_options_pricing_model#Method){:target="_blank"}

**Hint:** consider plotting the resulting DataFrame for each company to visualize the binomial tree. For example for below's example use `stock_price_simulation.loc['AMD'].T.plot(legend=False)`

**Also known as:** binomial tree, stock price tree, stock price path, lattice.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>time_to_expiration (float):</u> The number of years to use for the time to expiration, above 0. Defaults to 1 which equals
one year.
- <u>time_steps (int):</u> The number of time steps to use for the binomial tree, from 1 to 1,000, and at
most 16 when listing every path (show_unique_combinations=False). Defaults to 10 which equals 10
time steps. This will be evenly distributed over the time to expiration.
- <u>risk_free_rate (float, optional):</u> The risk free rate shown with show_input_info; it does not affect the
simulated prices. Defaults to None, which uses the Toolkit's risk-free rate on the pricing date: the
10-year Treasury yield unless the Toolkit's risk_free_rate parameter selects '13w', '5y' or '30y',
converted from its semi-annual bond-equivalent quote to continuous compounding. A rate passed here is used
as given, as a continuously compounded rate.
- <u>show_unique_combinations (bool, optional):</u> Whether to show the unique combinations of the stock prices.
Defaults to False.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Simulated Stock Price values containing the tickers and movements as the index and the
time steps as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

stock_price_simulation = toolkit.options.get_stock_price_simulation(
    time_steps=5, show_unique_combinations=True
)

stock_price_simulation.loc["AMD"]
```

Which returns:

| Movement   |   2025-12-31 |   2026-03-14 |   2026-05-26 |   2026-08-07 |   2026-10-19 |   2026-12-31 |
|:-----------|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| UUUUU      |       214.16 |      280.99  |      368.676 |     483.724  |     634.674  |     832.73   |
| DUUUU      |       214.16 |      163.225 |      214.16  |     280.99   |     368.676  |     483.724  |
| DDUUU      |       214.16 |      163.225 |      124.403 |     163.225  |     214.16   |     280.99   |
| DDDUU      |       214.16 |      163.225 |      124.403 |      94.8154 |     124.403  |     163.225  |
| DDDDU      |       214.16 |      163.225 |      124.403 |      94.8154 |      72.2646 |      94.8154 |
| DDDDD      |       214.16 |      163.225 |      124.403 |      94.8154 |      72.2646 |      55.0773 |

---

## get_put_call_parity
Calculate the Put-Call Parity gap, the amount by which Black-Scholes call and put prices deviate from the no-arbitrage relationship between them.

Put-Call Parity states that, for European options sharing the same strike price and time to expiration, the following relationship must hold in order to prevent arbitrage: $$C - P = S \cdot e^{- q \cdot t} - K \cdot e^{- r \cdot t}$$.

The formula is as follows:

$$
\text{Parity Gap} = (C - P) - (S \cdot e^{- q \cdot t} - K \cdot e^{- r \cdot t})
$$

Where C is the Black-Scholes call option price, P is the Black-Scholes put option price, S is the stock price, K is the strike price, r is the continuously compounded risk-free rate, q is the continuous dividend yield (ln(1 + dividend yield)) and t is the time to expiration in years (days / 365).

This method computes the Black-Scholes call and put price for each ticker, strike price and time to expiration and then calculates the parity gap, i.e. the amount by which (C - P) deviates from $$S \cdot e^{- qt} - K \cdot e^{- rt}$$. Because both prices come from the same Black-Scholes model and inputs, the gap is (up to floating point precision) always zero - this is a useful diagnostic to confirm that a set of option prices is internally consistent, or, when plugging in externally observed call and put prices, to detect potential arbitrage.

**Also known as:** Put-Call Parity, PCP, the no-arbitrage relationship between calls and puts.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None, which
uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Put-Call Parity gap containing the tickers and strike prices as the index and the
time to expiration as the columns. Values should be (approximately) zero.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["JNJ"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

parity_gap = toolkit.options.get_put_call_parity(
    strike_price_range=0.1, strike_step_size=5
)

parity_gap.loc["JNJ", ["2026-01-07", "2026-01-14", "2026-01-28"]]
```

Which returns:

|   Strike Price |   2026-01-07 |   2026-01-14 |   2026-01-28 |
|---------------:|-------------:|-------------:|-------------:|
|            185 |            0 |            0 |            0 |
|            190 |            0 |            0 |            0 |
|            195 |            0 |            0 |            0 |
|            200 |            0 |            0 |            0 |
|            205 |            0 |            0 |            0 |
|            210 |            0 |            0 |            0 |
|            215 |            0 |            0 |            0 |
|            220 |            0 |            0 |            0 |

---

## get_garman_kohlhagen
Calculate the Garman-Kohlhagen Model: what European calls and puts on each currency pair are worth, the Black-Scholes model with the foreign interest rate in the role of a dividend yield.

Because holding foreign currency earns the foreign risk-free rate (analogous to a continuous dividend yield on a stock), the Garman-Kohlhagen model uses the foreign risk-free rate in place of the dividend yield used in the standard Black-Scholes model.

The formulas are as follows:

$$
d_{1} = \frac{\ln\left(\frac{S}{K}\right) + \left(r - r_{f} + \frac{\sigma^{2}}{2}\right) \cdot t}{\sigma \cdot \sqrt{t}}
$$

$$
d_{2} = d_{1} - \sigma \cdot \sqrt{t}
$$

$$
\text{Call Option Price} = S \cdot e^{- r_{f} \cdot t} \cdot N(d_{1}) - K \cdot e^{- r \cdot t} \cdot N(d_{2})
$$

$$
\text{Put Option Price} = K \cdot e^{- r \cdot t} \cdot N(- d_{2}) - S \cdot e^{- r_{f} \cdot t} \cdot N(- d_{1})
$$

Where S is the spot exchange rate, K is the strike price, r is the domestic risk-free rate, $$r_{f}$$ is the foreign risk-free rate, $$\sigma$$ is the volatility, t is the time to expiration, N(d1) is the cumulative normal distribution of d1 and N(d2) is the cumulative normal distribution of d2.

**Also known as:** the Black-Scholes model for currency options, FX option pricing model.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>put_option (bool, optional):</u> Whether to calculate the put option price. Defaults to False which means
it will calculate the call option price.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The domestic risk free rate to use for the calculation. Defaults to
None, which uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the
Toolkit's risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual
bond-equivalent quote to continuous compounding. A rate passed here is used as given, as a continuously
compounded rate.
- <u>foreign_risk_free_rate (float, optional):</u> The foreign risk free rate to use for the calculation, which
plays the role of the dividend yield in the standard Black-Scholes model. Defaults to 0.0.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Garman-Kohlhagen values containing the tickers and strike prices as the index and the
time to expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["USDJPY"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

garman_kohlhagen = toolkit.options.get_garman_kohlhagen(
    strike_price_range=0.05,
    strike_step_size=2,
    expiration_time_range=91,
    risk_free_rate=0.0075,
    foreign_risk_free_rate=0.0375,
)

garman_kohlhagen.loc["USDJPY", ["2026-01-30", "2026-03-01", "2026-03-31"]]
```

Which returns:

|   Strike Price |   2026-01-30 |   2026-03-01 |   2026-03-31 |
|---------------:|-------------:|-------------:|-------------:|
|            148 |       8.4856 |       8.2657 |       8.1457 |
|            150 |       6.555  |       6.4899 |       6.4972 |
|            152 |       4.7419 |       4.8787 |       5.018  |
|            154 |       3.15   |       3.4876 |       3.7399 |
|            156 |       1.8838 |       2.3562 |       2.6819 |
|            158 |       0.9965 |       1.4964 |       1.8457 |
|            160 |       0.4596 |       0.8896 |       1.2167 |
|            162 |       0.183  |       0.4935 |       0.767  |

---

## get_binary_option
Calculate the price of a Binary (Digital) Option: what a payoff of all or nothing at expiration is worth, a fixed cash amount or the stock itself when the option ends in the money, using the Black-Scholes framework.

A binary option pays out a fixed amount if the option expires in-the-money and nothing otherwise. Two variants are supported: the cash-or-nothing option (the default) pays a fixed cash amount and the asset-or-nothing option pays the value of the underlying asset if the option expires in-the-money.

The formula is as follows:

$$
d_{1} = \frac{\ln\left(\frac{S}{K}\right) + \left(r - q + \frac{\sigma^{2}}{2}\right) \cdot t}{\sigma \cdot \sqrt{t}}
$$

$$
d_{2} = d_{1} - \sigma \cdot \sqrt{t}
$$

$$
\text{Cash-or-Nothing Call} = \text{Cash Payout} \cdot e^{- r \cdot t} \cdot N(d_{2}),\;\; \text{with Cash Payout defaulting to 1}
$$

$$
\text{Cash-or-Nothing Put} = \text{Cash Payout} \cdot e^{- r \cdot t} \cdot N(- d_{2})
$$

$$
\text{Asset-or-Nothing Call} = S \cdot e^{- q \cdot t} \cdot N(d_{1})
$$

$$
\text{Asset-or-Nothing Put} = S \cdot e^{- q \cdot t} \cdot N(- d_{1})
$$

Where S is the stock price (the traded close on the pricing date), K is the strike price, r is the continuously compounded risk-free rate, q is the continuous dividend yield (ln(1 + dividend yield)), $$\sigma$$ is the annualized volatility (the standard deviation of the daily returns over the trailing 252 trading days times √252), t is the time to expiration in years (days / 365) and N is the cumulative standard normal distribution.

**Also known as:** digital option, all-or-nothing option, cash-or-nothing option, asset-or-nothing option.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>put_option (bool, optional):</u> Whether to calculate the put option price. Defaults to False which means
it will calculate the call option price.
- <u>option_type (str, optional):</u> The payoff. Options are: "cash-or-nothing" (a fixed cash amount),
"asset-or-nothing" (the value of the stock). Defaults to "cash-or-nothing".
- <u>cash_payout (float, optional):</u> The fixed cash amount paid out by a cash-or-nothing option when it
expires in-the-money. Ignored for asset-or-nothing options. Defaults to 1.0.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None, which
uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Binary Option values containing the tickers and strike prices as the index and the
time to expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["GOOGL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

binary_option = toolkit.options.get_binary_option(
    strike_price_range=0.1, strike_step_size=5, expiration_time_range=91
)

binary_option.loc["GOOGL", ["2026-01-30", "2026-03-01", "2026-03-31"]]
```

Which returns:

|   Strike Price |   2026-01-30 |   2026-03-01 |   2026-03-31 |
|---------------:|-------------:|-------------:|-------------:|
|            280 |       0.8793 |       0.7914 |       0.7413 |
|            285 |       0.8376 |       0.7516 |       0.7053 |
|            290 |       0.7881 |       0.7086 |       0.6678 |
|            295 |       0.7315 |       0.6631 |       0.6291 |
|            300 |       0.6693 |       0.6157 |       0.5896 |
|            305 |       0.6029 |       0.5674 |       0.5498 |
|            310 |       0.5345 |       0.5187 |       0.5101 |
|            315 |       0.4662 |       0.4705 |       0.4709 |
|            320 |       0.3998 |       0.4234 |       0.4325 |
|            325 |       0.3371 |       0.3781 |       0.3952 |
|            330 |       0.2795 |       0.335  |       0.3595 |
|            335 |       0.2278 |       0.2945 |       0.3254 |
|            340 |       0.1827 |       0.257  |       0.2931 |

---

## get_american_option
Calculate American option prices: what calls and puts on each ticker that may be exercised at any time up to expiration are worth, with the method of choice.

The methods are the QD+ method of Li (2010) and Andersen, Lake and Offengenden (2016), the quadratic approximations of Barone-Adesi and Whaley (1987) and Ju and Zhong (1999), the closed-form approximations of Bjerksund and Stensland (2002 and 1993), finite differences, and the exact value from the exercise boundary solved as a fixed point (Andersen, Lake and Offengenden, 2016).

Listed options on single stocks are American: they can be exercised at any time up to expiration, which makes an in-the-money put, or a call on a stock with a high dividend yield, worth more than the European option the Black-Scholes model prices. These methods value that early exercise right without a tree:

- QD+ (the default): the European price plus the early exercise premium integrated over the exercise boundary, with the boundary at each time to expiration from the QD+ equation of Li (2010). The most accurate of the approximations, within 0.3% of the exact value across typical inputs, and slower.
- Barone-Adesi-Whaley: the early exercise premium is a power of S, fitted to the exercise value at the critical stock price S*, found numerically. Fast, and within about 1% of the exact value for most options, but several percent off for maturities of a year or more.
- Ju-Zhong: Barone-Adesi-Whaley with a correction for the term it drops, which divides the premium by $$1 - \chi (S)$$, a quadratic in ln(S / S*). As fast and within about 0.3% for most options.
- QD fixed point: the QD+ integral with the boundary that solves the integral equation of Kim (1990), iterated as a fixed point from the QD+ boundary until it changes less than 1e-12. It converges to the exact American value, within about 1e-6 (1e-8 for most options), at about 30 to 150 ms per price, so it is the slowest and best suited to a few strikes and expirations.
- Finite differences: the Black-Scholes equation solved backwards from expiration with Crank-Nicolson (Rannacher start-up) on a grid of 1,000 steps in ln(S / K) and at least 400 time steps (4 per expiration day beyond 100 days), with the exercise constraint solved at every step by Brennan and Schwartz (1977). As $$V (S , K , \tau) = K \cdot v (S / K , \tau)$$, one solve gives every strike, and the expirations are solved in groups whose longest is at most four times their shortest, each on a grid sized for it, so that an expiration a day away is as precise as one months away: within about 1e-3 of the exact value for a stock price of 100 (7.3e-4 at most from a day to a quarter at volatilities up to 100%; the error scales with the price), see ``finite_difference_model.get_finite_difference_option_values``.
- Bjerksund-Stensland (2002): a closed form that assumes the early exercise boundary is flat in steps: once the stock price crosses the trigger price, immediate exercise is assumed optimal. The option's life is split at $$t_{1} = \tfrac{1}{2} (\sqrt{5} - 1) \cdot T$$ into two periods, each with its own flat trigger price, which brings the price closer to the exact American value than a single flat trigger.
- Bjerksund-Stensland (1993): the original version, with one flat trigger price over the option's whole life, which is faster and slightly further below the exact American value.

The formulas are as follows, with $$\phi = 1$$ for a call and -1 for a put:

$$
\alpha = \frac{2r}{\sigma^{2}},\;\; \beta = \frac{2(r - q)}{\sigma^{2}},\;\; h = 1 - e^{- rT}
$$

$$
\lambda = \frac{- (\beta - 1) + \phi \cdot \sqrt{(\beta - 1)^{2} + \frac{4 \alpha}{h}}}{2}
$$

$$
S^{*} \;\text{solves}\; \phi \cdot (S^{*} - K) = V_{E}(S^{*}) + \frac{\phi \cdot (1 - e^{- qT} \cdot N(\phi \cdot \operatorname{d1}(S^{*}))) \cdot S^{*}}{\lambda}
$$

$$
\text{Barone-Adesi-Whaley} = V_{E}(S) + \frac{\phi \cdot (1 - e^{- qT} \cdot N(\phi \cdot \operatorname{d1}(S^{*}))) \cdot S^{*}}{\lambda} \cdot \left(\frac{S}{S^{*}}\right)^{\lambda}
$$

$$
\text{Ju-Zhong} = V_{E}(S) + \frac{(\phi \cdot (S^{*} - K) - V_{E}(S^{*})) \cdot \left(\frac{S}{S^{*}}\right)^{\lambda}}{1 - b \cdot \ln\left(\frac{S}{S^{*}}\right)^{2} - c \cdot \ln\left(\frac{S}{S^{*}}\right)}
$$

$$
\text{QD}^{+} \;\text{Put} = p(S) + \text{∫}_{0}^{T}\left[r \cdot K \cdot e^{- \text{rt}} \cdot N\left(- \operatorname{d2}\left(t,\; \frac{S}{B(T - t)}\right)\right) - q \cdot S \cdot e^{- \text{qt}} \cdot N\left(- \operatorname{d1}\left(t,\; \frac{S}{B(T - t)}\right)\right)\right] \,\mathrm{d}t
$$

$$
\text{QD fixed point:}\;\; B(\tau) = \frac{K \cdot e^{- (r - q) \tau} \cdot N(\tau,\; B)}{D(\tau,\; B)},\;\; \text{iterated at 25 Chebyshev nodes in} \;\sqrt{\tau},\;\; \text{with } N \text{ and } D \text{ the integrals of the FP-A equation of Andersen, Lake and Offengenden (2016), and the put priced with the integral of QD+}
$$

$$
\text{QD}^{+} \;\text{Call} \;(S,\; K,\; r,\; q) = \text{QD}^{+} \;\text{Put} \;(K,\; S,\; q,\; r),\;\; \text{the put-call symmetry of McDonald and Schroder (1998)}
$$

$$
\text{Finite differences:}\;\; V_{\tau} = \frac{\sigma^{2}}{2} \cdot V_{xx} + \left(r - q - \frac{\sigma^{2}}{2}\right) \cdot V_{x} - r \cdot V \;\text{on}\; x = \ln\left(\frac{S}{K}\right),\;\; \text{stepped with} \;\left(I - \frac{\Delta \tau}{2} \cdot L\right) \cdot V(\tau + \Delta \tau) = \left(I + \frac{\Delta \tau}{2} \cdot L\right) \cdot V(\tau) \;\text{subject to}\; V \geq \phi \cdot (S - K)
$$

The Bjerksund-Stensland formulas are as follows (for a call, with cost of carry $$b = r - q$$ smaller than r):

$$
\beta = \left(0.5 - \frac{b}{\sigma^{2}}\right) + \sqrt{\left(\frac{b}{\sigma^{2}} - 0.5\right)^{2} + \frac{2r}{\sigma^{2}}}
$$

$$
B_{\infty} = \frac{\beta}{\beta - 1} \cdot K
$$

$$
B_{0} = \max\left(K,\; \frac{r}{r - b} \cdot K\right)
$$

$$
h(t) = - \frac{(b \cdot t + 2 \sigma \sqrt{t}) \cdot K^{2}}{(B_{\infty} - B_{0}) \cdot B_{0}}
$$

$$
I(t) = B_{0} + (B_{\infty} - B_{0}) \cdot (1 - e^{h(t)}),\;\; \text{with}\;\; I_{1} = I(t_{1})\;\;\text{and}\;\; I_{2} = I(T)
$$

$$
\text{Call} \;(2002) = \max(\text{Approximation},\; \text{European Black-Scholes Call},\; \max(S - K,\; 0)),\;\; \text{where the Approximation is}\; S - K \;\text{when}\; S \geq I_{2} \;\text{and otherwise combines univariate} \;(\text{first period}) \;\text{and bivariate} \;(\text{both periods}) \;\text{normal terms},\;\; \text{see black\_scholes\_model.get\_bjerksund\_stensland}
$$

$$
\text{Put} \;(S,\; K,\; T,\; r,\; b,\; \sigma) = \text{Call} \;(K,\; S,\; T,\; r - b,\; - b,\; \sigma),\;\; \text{the put-call transformation}
$$

The 1993 version keeps one flat trigger price over the option's whole life:

$$
h(T) = - \frac{(b \cdot T + 2 \sigma \sqrt{T}) \cdot B_{0}}{B_{\infty} - B_{0}}
$$

$$
I = B_{0} + (B_{\infty} - B_{0}) \cdot (1 - e^{h(T)}),\;\; \alpha = (I - K) \cdot I^{- \beta}
$$

$$
\text{Call} \;(1993) = \alpha \cdot S^{\beta} - \alpha \cdot \phi(S,\; T,\; \beta,\; I,\; I) + \phi(S,\; T,\; 1,\; I,\; I) - \phi(S,\; T,\; 1,\; K,\; I) - K \cdot \phi(S,\; T,\; 0,\; I,\; I) + K \cdot \phi(S,\; T,\; 0,\; K,\; I),\;\; \text{with } \phi \text{ the univariate knock-out claim of black\_scholes\_model.\_phi}
$$

Where each formula holds on the side of S* (or of the boundary B(T)) where holding the option is optimal, and the option is worth its exercise value $$\phi \cdot (S - K)$$ beyond it. S is the stock price (the traded close on the pricing date), K is the strike price, r is the continuously compounded risk-free rate, q is the continuous dividend yield (ln(1 + dividend yield)), $$\sigma$$ is the annualized volatility (the standard deviation of the daily returns over the trailing 252 trading days times √252), T is the time to expiration in years (days / 365), $$V_{E}$$ and p are the European Black-Scholes prices, d1 and d2 are those of the Black-Scholes model, b and c are the Ju-Zhong coefficients (see ``american_model.get_ju_zhong``) and $$B (\tau)$$ is the QD+ exercise boundary of a put with $$\tau$$ years to expiration (see ``american_model.get_qd_plus``).

A call on a stock without dividends is never exercised early and a put at a non-positive rate neither; these are worth the Black-Scholes price, floored at the exercise value. With Bjerksund-Stensland, a call whose cost of carry b is at least r is likewise worth the Black-Scholes price, and where the boundary I2 falls to or below the strike, a 1,000-step binomial tree prices the option instead. At zero days to expiration the value is the exercise value.

Bjerksund-Stensland can undervalue an option when the risk-free rate or the cost of carry is negative: its flat boundaries can fall back to the European value while early exercise is worth more (with $$r = - 2 \%$$, $$q = - 3 \%$$, $$\sigma = 1 \%$$ and $$T = 1$$, an at-the-money put of 0.0854 against 0.1669 for a 10,000-step binomial tree). A warning names the tickers this applies to; QD+ prices them accurately.

See: Barone-Adesi, G., & Whaley, R. E. (1987), "Efficient Analytic Approximation of American Option Values", The Journal of Finance, 42(2), 301-320; Ju, N., & Zhong, R. (1999), "An Approximate Formula for Pricing American Options", The Journal of Derivatives, 7(2), 31-40; Li, M. (2010), "Analytical Approximations for the Critical Stock Prices of American Options: A Performance Comparison", Review of Derivatives Research, 13(1), 75-99; Andersen, L., Lake, M., & Offengenden, D. (2016), "High-Performance American Option Pricing", Journal of Computational Finance, 20(1), 39-87; Kim, I. J. (1990), "The Analytic Valuation of American Options", The Review of Financial Studies, 3(4), 547-572; Brennan, M. J., & Schwartz, E. S. (1977), "The Valuation of American Put Options", The Journal of Finance, 32(2), 449-462; Bjerksund, P., & Stensland, G. (2002), "Closed Form Valuation of American Options", Working paper, NHH; Bjerksund, P., & Stensland, G. (1993), "Closed-Form Approximation of American Options", Scandinavian Journal of Management, 9, S87-S99, both as presented in Haug, E. G. (2007), "The Complete Guide to Option Pricing Formulas" (2nd ed.), sections 3.1.4 and 3.1.3.

**Also known as:** BAW, quadratic approximation, American option price, early exercise premium, QD+, QdFp, BS2002, Bjerksund-Stensland approximation.

**References:**

- library | Referenced against QuantLib's [QdPlusAmericanEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_qd_plus_american_engine.html){:target="_blank"} (QD+)
- library | Referenced against QuantLib's [BaroneAdesiWhaleyApproximationEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_barone_adesi_whaley_approximation_engine.html){:target="_blank"} (Barone-Adesi-Whaley)
- library | Referenced against QuantLib's [JuQuadraticApproximationEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_ju_quadratic_approximation_engine.html){:target="_blank"} (Ju-Zhong)
- library | Referenced against QuantLib's [QdFpAmericanEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_qd_fp_american_engine.html){:target="_blank"} (QD fixed point)
- library | Referenced against QuantLib's [FdBlackScholesVanillaEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_fd_black_scholes_vanilla_engine.html){:target="_blank"} (QD fixed point)
- library | Referenced against QuantLib's [FdBlackScholesVanillaEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_fd_black_scholes_vanilla_engine.html){:target="_blank"} (Bjerksund-Stensland 2002)
- library | Referenced against QuantLib's [BjerksundStenslandApproximationEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_bjerksund_stensland_approximation_engine.html){:target="_blank"} (Bjerksund-Stensland 1993)
- library | Shares similar logic as QuantLib's [FdBlackScholesVanillaEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_fd_black_scholes_vanilla_engine.html){:target="_blank"} (finite differences)
- library | Shares similar logic as FinancePy's [black_scholes_fd](https://github.com/domokane/FinancePy/blob/V1.1.2/financepy/models/finite_difference.py#L318){:target="_blank"} (finite differences)
- library | Shares similar logic as FinancePy's [baw_value](https://github.com/domokane/FinancePy/blob/V1.1.2/financepy/models/black_scholes_analytic.py#L682){:target="_blank"} (Barone-Adesi-Whaley)

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>put_option (bool, optional):</u> Whether to calculate the put option price. Defaults to False which means
it will calculate the call option price.
- <u>method (str, optional):</u> The pricing method. Options are: "qd_plus" (QD+), "barone_adesi_whaley"
(Barone-Adesi-Whaley), "ju_zhong" (Ju-Zhong), "qd_fixed_point" (QD fixed point), "finite_difference"
(Crank-Nicolson finite differences), "bjerksund_stensland" (Bjerksund-Stensland 2002, two flat trigger
prices) and "bjerksund_stensland_1993" (Bjerksund-Stensland 1993, one flat trigger price). Defaults to
"qd_plus".
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None, which
uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: American option values containing the tickers and strike prices as the index and the time
to expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["VZ"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

american_put = toolkit.options.get_american_option(
    put_option=True, strike_price_range=0.15, strike_step_size=1, expiration_time_range=91
)

american_put.loc["VZ", ["2026-01-30", "2026-03-01", "2026-03-31"]]
```

Which returns:

|   Strike Price |   2026-01-30 |   2026-03-01 |   2026-03-31 |
|---------------:|-------------:|-------------:|-------------:|
|             34 |       0.001  |       0.0226 |       0.0764 |
|             35 |       0.005  |       0.0551 |       0.1464 |
|             36 |       0.0193 |       0.1202 |       0.2605 |
|             37 |       0.0606 |       0.2369 |       0.4335 |
|             38 |       0.1584 |       0.4268 |       0.6798 |
|             39 |       0.3523 |       0.71   |       1.0107 |
|             40 |       0.6807 |       1.1012 |       1.4332 |
|             41 |       1.1664 |       1.6063 |       1.9493 |
|             42 |       1.8081 |       2.2221 |       2.5554 |
|             43 |       2.5816 |       2.9372 |       3.2441 |
|             44 |       3.4518 |       3.735  |       4.0046 |
|             45 |       4.3838 |       4.5974 |       4.8251 |
|             46 |       5.3505 |       5.507  |       5.6935 |
|             47 |       6.3345 |       6.449  |       6.5986 |

---

## get_cev_model
Calculate European option prices in the constant elasticity of variance (CEV) model of Cox (1975): what calls and puts on each ticker are worth when the volatility rises as the stock price falls, with the non-central chi-squared formula of Schroder (1989).

In the CEV model the stock's volatility depends on its price, $$\sigma (S) = \delta \cdot S^{\beta - 1}$$. With an elasticity $$\beta$$ below 1 the volatility rises as the price falls (the leverage effect), so out-of-the-money puts are worth more and out-of-the-money calls less than in the Black-Scholes model ($$\beta = 1$$): the downward sloping skew of equity options. $$\beta = 0.5$$ is the square-root process and $$\beta = 0$$ an absolute (normal) volatility. The stock is absorbed at zero.

The historical volatility is taken as the local volatility at today's price, $$\delta = \sigma \cdot S^{1 - \beta}$$, so the at-the-money options are priced close to Black-Scholes and $$\beta$$ only adds the skew. $$\beta$$ is a model choice rather than data: fitted to an option chain it is typically between 0 and 1 for stocks and indices.

The formulas are as follows:

$$
\delta = \sigma \cdot S^{1 - \beta},\;\; F = S \cdot e^{(r - q) T},\;\; \nu = \frac{1}{1 - \beta}
$$

$$
v = \frac{\delta^{2} \cdot (e^{2(r - q) (1 - \beta) T} - 1)}{2(r - q) (1 - \beta)},\;\; \text{or}\;\; \delta^{2} \cdot T \;\text{when}\; r = q
$$

$$
x = \frac{F^{2(1 - \beta)}}{(1 - \beta)^{2} \cdot v},\;\; y = \frac{K^{2(1 - \beta)}}{(1 - \beta)^{2} \cdot v}
$$

$$
\text{Call} = e^{- rT} \cdot \left[F \cdot (1 - \chi^{2}(y ; \nu + 2,\; x)) - K \cdot \chi^{2}(x ; \nu,\; y)\right]
$$

$$
\text{Put} = e^{- rT} \cdot \left[K \cdot (1 - \chi^{2}(x ; \nu,\; y)) - F \cdot \chi^{2}(y ; \nu + 2,\; x)\right]
$$

Where S is the stock price (the traded close on the pricing date), K is the strike price, r is the continuously compounded risk-free rate, q is the continuous dividend yield (ln(1 + dividend yield)), $$\sigma$$ is the annualized volatility (the standard deviation of the daily returns over the trailing 252 trading days times √252), $$\beta$$ is the elasticity, T is the time to expiration in years (days / 365), F is the futures price of the expiration and $$\chi^{2} (z ; k , \lambda)$$ is the distribution function of the non-central chi-squared distribution with k degrees of freedom and non-centrality $$\lambda$$. With $$\beta = 1$$ the values are those of the Black-Scholes model. At zero days to expiration the value is the exercise value.

See: Cox, J. C. (1975), "Notes on Option Pricing I: Constant Elasticity of Variance Diffusions", working paper, Stanford University (reprinted in The Journal of Portfolio Management, 23(2), 1996); Schroder, M. (1989), "Computing the Constant Elasticity of Variance Option Pricing Formula", The Journal of Finance, 44(1), 211-219.

**Also known as:** CEV model, constant elasticity of variance, CEV option price, leverage effect skew.

**References:**

- library | Referenced against QuantLib's [AnalyticCEVEngine](https://github.com/lballabio/QuantLib/blob/v1.44/ql/pricingengines/vanilla/analyticcevengine.hpp#L62){:target="_blank"}

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>put_option (bool, optional):</u> Whether to calculate the put option price. Defaults to False which means
it will calculate the call option price.
- <u>beta (float, optional):</u> The elasticity $$\beta$$, between 0 and 1, where 1 is the Black-Scholes model. Defaults to
0.5, the square-root process.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None, which
uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: CEV option values containing the tickers and strike prices as the index and the time to
expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

cev_put = toolkit.options.get_cev_model(
    put_option=True, beta=0.5, strike_price_range=0.15, strike_step_size=10, expiration_time_range=91
)

cev_put.loc["AAPL", ["2026-01-30", "2026-03-01", "2026-03-31"]]
```

Which returns:

|   Strike Price |   2026-01-30 |   2026-03-01 |   2026-03-31 |
|---------------:|-------------:|-------------:|-------------:|
|            230 |       0.3865 |       1.6792 |       3.1579 |
|            240 |       1.0437 |       3.082  |       5.0247 |
|            250 |       2.4176 |       5.2461 |       7.6031 |
|            260 |       4.8871 |       8.3465 |      10.9942 |
|            270 |       8.7686 |      12.5031 |      15.2615 |
|            280 |      14.1992 |      17.7584 |      20.424  |
|            290 |      21.0882 |      24.072  |      26.4555 |
|            300 |      29.1649 |      31.3332 |      33.2904 |
|            310 |      38.084  |      39.386  |      40.8347 |
|            320 |      47.5269 |      48.0578 |      48.9786 |

---

## get_black_76_model
Calculate the Black (1976) model: what European calls and puts on futures and forwards are worth, the Black-Scholes model with each ticker's price taken as the futures price.

A futures price already contains the cost of carry of the underlying (interest, storage, dividends or the convenience yield of a commodity), so it grows at no rate under the risk-neutral measure and the option only discounts its payoff. Use it for tickers that quote futures prices, such as commodities (GCUSD for gold, CLUSD for crude oil) and index futures. It assumes the option expires with the futures contract, so the futures price of each expiration is the one quoted today; for an option that expires before its futures contract the price is the same with the time to the option's expiration.

The formulas are as follows:

$$
d_{1} = \frac{\ln\left(\frac{F}{K}\right) + \frac{\sigma^{2}}{2} \cdot t}{\sigma \cdot \sqrt{t}}
$$

$$
d_{2} = d_{1} - \sigma \cdot \sqrt{t}
$$

$$
\text{Call Option Price} = e^{- r \cdot t} \cdot (F \cdot N(d_{1}) - K \cdot N(d_{2}))
$$

$$
\text{Put Option Price} = e^{- r \cdot t} \cdot (K \cdot N(- d_{2}) - F \cdot N(- d_{1}))
$$

Where F is the futures price (the traded close on the pricing date), K is the strike price, r is the continuously compounded risk-free rate, $$\sigma$$ is the annualized volatility of the futures price (the standard deviation of the daily returns over the trailing 252 trading days times √252), t is the time to expiration in years (days / 365) and N is the standard normal distribution. At zero days to expiration the value is the exercise value. The implied volatility of a quoted option on a futures contract is ``black_scholes_model.get_black_76_implied_volatility``.

See: Black, F. (1976), "The Pricing of Commodity Contracts", Journal of Financial Economics, 3(1-2), 167-179.

**Also known as:** Black-76, Black's model, options on futures, options on forwards, commodity options.

**References:**

- library | Referenced against QuantLib's [blackFormula](https://www.quantlib.org/reference/namespace_quant_lib.html#adfe71f9b0b157cae6e4bd53faaa676af){:target="_blank"}
- library | Shares similar logic as FinancePy's [Black](https://github.com/domokane/FinancePy/blob/V1.1.2/financepy/models/black.py#L18){:target="_blank"}

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>put_option (bool, optional):</u> Whether to calculate the put option price. Defaults to False which means
it will calculate the call option price.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current futures price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current futures price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Black-76 values containing the tickers and strike prices as the index and the time to
expiration as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["GCUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

black_76 = toolkit.options.get_black_76_model(
    strike_price_range=0.1, strike_step_size=100, expiration_time_range=91
)

black_76.loc["GCUSD", ["2026-01-30", "2026-03-01", "2026-03-31"]]
```

Which returns:

|   Strike Price |   2026-01-30 |   2026-03-01 |   2026-03-31 |
|---------------:|-------------:|-------------:|-------------:|
|           3900 |     442.905  |     454.105  |     468.105  |
|           4000 |     349.15   |     368.535  |     388.087  |
|           4100 |     262.153  |     290.585  |     315.343  |
|           4200 |     185.691  |     222.011  |     250.855  |
|           4300 |     123.028  |     163.997  |     195.201  |
|           4400 |      75.7173 |     116.939  |     148.498  |
|           4500 |      43.0764 |      80.4062 |     110.409  |
|           4600 |      22.5863 |      53.2835 |      80.2235 |
|           4700 |      10.9008 |      34.0278 |      56.973  |
|           4800 |       4.843  |      20.9478 |      39.5581 |

---

## get_monte_carlo_option_price
Calculate option prices through Monte Carlo simulation: what European calls and puts on each ticker are worth on simulated Geometric Brownian Motion (GBM) stock price paths, or American ones by least-squares Monte Carlo (Longstaff and Schwartz, 2001).

The Monte Carlo method prices an option by simulating a large number of possible future paths for the underlying stock price under the risk-neutral measure, computing the option's payoff at expiration for each simulated path, and then discounting the average payoff back to the present.

The formula is as follows:

$$
\Delta t = \frac{T}{\text{Time Steps}},\;\; \text{with Time Steps defaulting to 100}
$$

$$
S(t + \Delta t) = S(t) \cdot e^{\left(r - q - \frac{\sigma^{2}}{2}\right) \cdot \Delta t + \sigma \cdot \sqrt{\Delta t} \cdot Z}
$$

$$
\text{Call Price} = e^{- r \cdot T} \cdot \operatorname{MEAN}(\max(S(T) - K,\; 0)),\;\; \text{averaged over the simulated paths (10,000 by default)}
$$

$$
\text{Put Price} = e^{- r \cdot T} \cdot \operatorname{MEAN}(\max(K - S(T),\; 0))
$$

$$
\text{Standard Error} = \frac{\text{Sample Standard Deviation} \;(\text{ddof} = 1) \;\text{of the} \;\text{Discounted Payoffs}}{\sqrt{\text{Simulations}}}
$$

Where S(t) is the stock price at time t (starting from the traded close on the pricing date), K is the strike price, r is the continuously compounded risk-free rate, q is the continuous dividend yield (ln(1 + dividend yield)), $$\sigma$$ is the annualized volatility (the standard deviation of the daily returns over the trailing 252 trading days times √252), T is the time to expiration in years (days / 365) and Z is a standard normal random variable.

An American option can be exercised at each of the time steps: stepping back from expiration, the discounted cash flows of the paths in the money are regressed on a constant and the weighted Laguerre polynomials $$e^{- x / 2} \cdot L_{n} (x)$$, $$n = 0$$, 1, 2, of $$x = S (t) / K$$, and a path is exercised where its exercise value beats the fitted continuation value (see ``monte_carlo_model.get_longstaff_schwartz_option``):

$$
C(t) = \beta_{0} + \sum \beta_{n} \cdot e^{- \frac{x}{2}} \cdot L_{n}(x),\;\; \text{fitted on the in-the-money paths at } t
$$

$$
\text{Cash Flow}(t) = \phi \cdot (S(t) - K) \;\text{if}\; \phi \cdot (S(t) - K) > C(t),\;\; \text{else}\;\; e^{- r \cdot \Delta t} \cdot \text{Cash Flow}(t + \Delta t)
$$

$$
\text{American Price} = \max(\phi \cdot (S - K),\; \operatorname{MEAN}(e^{- r \cdot \Delta t} \cdot \text{Cash Flow}(\Delta t)))
$$

Two variance reductions and quasi-random numbers narrow the standard error at the same number of paths (Glasserman, 2003, chapters 4 and 5):

- Antithetic variates: every path Z is paired with -Z (simulations must be even) and the standard error comes from the averages of the pairs.
- Control variate: Price = MEAN(Y - $$\beta \cdot (X - E [X])$$), $$\beta = \operatorname{Cov} (Y , X) / \operatorname{Var} (X)$$, with X the discounted stock price at expiration ($$E [X] = S \cdot e^{- q \cdot T}$$) for a European option and the discounted European payoff (E[X] its Black-Scholes price) for an American option.
- Sobol sequence: scrambled Sobol points with a Brownian bridge in 16 independently scrambled replications, whose spread gives the standard error; the error shrinks close to 1 / simulations rather than $$1 / \sqrt{\text{simulations}}$$.

All strike prices of an expiry are priced on the same simulated paths (common random numbers), which keeps the prices consistent across strikes and means the paths are simulated once per expiry rather than once per strike. The European expiries share one set of standardised shocks, each scaled to its own time to expiration, which with a seed gives the prices of simulating every expiry with that seed.

As it is a simulation, the result comes with sampling error. Showing the standard error additionally returns the standard error of each estimate - as a rule of thumb, the true price lies within plus or minus 2 times the standard error roughly 95% of the time. The seed makes the results reproducible; without one (None) every call draws new paths.

See: Boyle, P. P. (1977), "Options: A Monte Carlo Approach", Journal of Financial Economics, 4(3), 323-338; Longstaff, F. A., & Schwartz, E. S. (2001), "Valuing American Options by Simulation: A Simple Least-Squares Approach", The Review of Financial Studies, 14(1), 113-147; Glasserman, P. (2003), "Monte Carlo Methods in Financial Engineering", Springer. The libraries below draw their own random numbers, which give other paths.

**Also known as:** Monte Carlo option pricing, simulation-based option pricing.

**References:**

- library | Shares similar logic as QuantLib's [MCEuropeanEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_m_c_european_engine.html){:target="_blank"} (European)
- library | Shares similar logic as QuantLib's [MCAmericanEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_m_c_american_engine.html){:target="_blank"} (American)
- library | Shares similar logic as FinancePy's [equity_lsmc](https://github.com/domokane/FinancePy/blob/V1.1.2/financepy/models/equity_lsmc.py#L39){:target="_blank"} (American)

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>put_option (bool, optional):</u> Whether to calculate the put option price. Defaults to False which means
it will calculate the call option price.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None, which
uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>simulations (int, optional):</u> The number of simulated stock price paths, at least 1. Defaults to 10,000.
- <u>time_steps (int, optional):</u> The number of time steps used to build each simulated path, at least 1.
Defaults to 100.
- <u>seed (int &#124; None, optional):</u> The seed used to initialize the random number generator, ensuring
reproducible results; None draws new paths on every call. Defaults to 0.
- <u>show_standard_error (bool, optional):</u> Whether to also return the standard error of each Monte Carlo
estimate as a second DataFrame. Defaults to False.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.
- <u>american_option (bool, optional):</u> Whether to price American options by least-squares Monte
Carlo, exercisable at each time step. Defaults to False.
- <u>variance_reduction (str &#124; None, optional):</u> The variance reduction. Options are: None (none),
"antithetic" (antithetic variates), "control_variate" (control variate). Defaults to None.
- <u>sequence (str, optional):</u> The random numbers. Options are: "pseudo_random" (pseudo-random numbers),
"sobol" (scrambled Sobol points, at least 32 simulations). Defaults to "pseudo_random".

**Returns:**

pd.DataFrame: Monte Carlo option values containing the tickers and strike prices as the index and the
time to expiration as the columns. If show_standard_error is True, a tuple of (prices, standard_errors)
is returned instead.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["COST"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

monte_carlo = toolkit.options.get_monte_carlo_option_price(
    strike_price_range=0.1, strike_step_size=10, expiration_time_range=31, seed=42
)

monte_carlo.loc["COST", ["2026-01-07", "2026-01-14", "2026-01-30"]]
```

Which returns:

|   Strike Price |   2026-01-07 |   2026-01-14 |   2026-01-30 |
|---------------:|-------------:|-------------:|-------------:|
|            770 |      92.8712 |      93.4178 |      95.1631 |
|            780 |      82.8804 |      83.4928 |      85.5947 |
|            790 |      72.8944 |      73.6473 |      76.2372 |
|            800 |      62.9375 |      63.9363 |      67.1776 |
|            810 |      53.0607 |      54.4486 |      58.49   |
|            820 |      43.3666 |      45.3481 |      50.2664 |
|            830 |      34.0541 |      36.7981 |      42.5944 |
|            840 |      25.4471 |      28.9931 |      35.5504 |
|            850 |      17.8995 |      22.0913 |      29.1762 |
|            860 |      11.7123 |      16.2119 |      23.5432 |
|            870 |       7.0923 |      11.4611 |      18.6827 |
|            880 |       3.9767 |       7.8036 |      14.5838 |
|            890 |       2.0394 |       5.1199 |      11.2047 |
|            900 |       0.961  |       3.213  |       8.4756 |
|            910 |       0.4225 |       1.9345 |       6.2838 |
|            920 |       0.1698 |       1.1303 |       4.5777 |
|            930 |       0.0582 |       0.6374 |       3.2774 |
|            940 |       0.018  |       0.3432 |       2.3097 |
|            950 |       0.0049 |       0.1773 |       1.6158 |

---

## get_barrier_option
Calculate the closed-form price of a barrier option: what a European option on each ticker is worth that knocks in or out when the stock price touches a barrier, single (up or down) with the Reiner & Rubinstein (1991) formulas, double, partial-time, soft or discretely watched.

A barrier option is a path-dependent option whose payoff (and existence) depends on whether the underlying stock price touches a pre-specified barrier level at any point before expiration:

- Knock-out: the option becomes worthless if the barrier is touched.
- Knock-in: the option only comes into existence if the barrier is touched.
- Down barrier: the barrier is below the current stock price.
- Up barrier: the barrier is above the current stock price.

The barrier level is defined relative to the current stock price as a percentage, e.g. a value of 0.9 sets the barrier at 90% of the current stock price (a sensible default for a down barrier).

Besides the single barrier watched continuously over the whole life, the barrier can be:

- Double: a lower barrier and an upper barrier, each a percentage of the stock price; the knock-out pays only when the stock price stays between the two, priced with the series of Ikeda and Kunitomo (1992) for flat barriers.
- Partial-time: watched only during the first (a start window) or the last (an end window) share of the life (Heynen & Kat, 1994). With an end window the option is also knocked out (or in) when the stock price is beyond the barrier at the start of the window.
- Soft: a band between the barrier and a second, soft barrier through which the option knocks out gradually (Hart & Ross, 1994): a soft down-and-out pays the vanilla payoff times (min S - L) / (U - L), the share of the band the lowest price did not reach, which is the average of the hard barrier prices over the band.
- Discretely watched (daily, weekly or monthly): checked only at each close, which is priced by moving the barriers away from the stock price by $$e^{0.5826 \cdot \sigma \cdot \sqrt{\Delta} t}$$, with $$\Delta t = \tfrac{1}{252}$$, 1/52 or 1/12 (Broadie, Glasserman & Kou, 1997). A daily barrier is crossed noticeably less often than a continuous one, so it is worth setting for a knock-out with a barrier close to the stock price.

The formula is as follows (Reiner & Rubinstein, 1991, in the notation of Haug, 2007):

$$
H = \text{Barrier Percentage} \cdot S,\;\; \text{with Barrier Percentage defaulting to 0.9}
$$

$$
b = r - q,\;\; \mu = \frac{b - \frac{\sigma^{2}}{2}}{\sigma^{2}},\;\; \lambda = \sqrt{\mu^{2} + \frac{2r}{\sigma^{2}}},\;\; \phi = 1 \;\text{for a call and} \;\mathord{-} 1 \;\text{for a put},\;\; \eta = 1 \;\text{for a down barrier and} \;\mathord{-} 1 \;\text{for an up barrier}
$$

$$
x_{1} = \frac{\ln\left(\frac{S}{K}\right)}{\sigma \sqrt{T}} + (1 + \mu) \sigma \sqrt{T},\;\; x_{2} = \frac{\ln\left(\frac{S}{H}\right)}{\sigma \sqrt{T}} + (1 + \mu) \sigma \sqrt{T}
$$

$$
y_{1} = \frac{\ln\left(\frac{H^{2}}{S \cdot K}\right)}{\sigma \sqrt{T}} + (1 + \mu) \sigma \sqrt{T},\;\; y_{2} = \frac{\ln\left(\frac{H}{S}\right)}{\sigma \sqrt{T}} + (1 + \mu) \sigma \sqrt{T}
$$

$$
z = \frac{\ln\left(\frac{H}{S}\right)}{\sigma \sqrt{T}} + \lambda \sigma \sqrt{T}
$$

$$
A = \phi S \cdot e^{(b - r) T} \cdot N(\phi x_{1}) - \phi K \cdot e^{- rT} \cdot N(\phi x_{1} - \phi \sigma \sqrt{T}),\;\; \text{and } B \text{ the same with } x_{2} \text{ in place of } x_{1}
$$

$$
C = \phi S \cdot e^{(b - r) T} \cdot \left(\frac{H}{S}\right)^{2(\mu + 1)} \cdot N(\eta y_{1}) - \phi K \cdot e^{- rT} \cdot \left(\frac{H}{S}\right)^{2 \mu} \cdot N(\eta y_{1} - \eta \sigma \sqrt{T}),\;\; \text{and } D \text{ the same with } y_{2} \text{ in place of } y_{1}
$$

$$
E = \text{Rebate} \cdot e^{- rT} \cdot \left(N(\eta x_{2} - \eta \sigma \sqrt{T}) - \left(\frac{H}{S}\right)^{2 \mu} \cdot N(\eta y_{2} - \eta \sigma \sqrt{T})\right)
$$

$$
F = \text{Rebate} \cdot \left(\left(\frac{H}{S}\right)^{\mu + \lambda} \cdot N(\eta z) + \left(\frac{H}{S}\right)^{\mu - \lambda} \cdot N(\eta z - 2 \eta \lambda \sigma \sqrt{T})\right)
$$

$$
\text{Down-and-Out Call} \;(\text{the default}) = A - C + F \;\text{if}\; K > H,\;\; \text{else}\;\; B - D + F
$$

$$
\text{Down-and-In Call} = C + E \;\text{if}\; K > H,\;\; \text{else}\;\; A - B + D + E
$$

$$
\text{Up-and-Out Call} = F \;\text{if}\; K > H,\;\; \text{else}\;\; A - B + C - D + F
$$

$$
\text{Up-and-In Call} = A + E \;\text{if}\; K > H,\;\; \text{else}\;\; B - C + D + E
$$

$$
\text{Down-and-Out Put} = A - B + C - D + F \;\text{if}\; K > H,\;\; \text{else } F
$$

$$
\text{Down-and-In Put} = B - C + D + E \;\text{if}\; K > H,\;\; \text{else}\;\; A + E
$$

$$
\text{Up-and-Out Put} = B - D + F \;\text{if}\; K > H,\;\; \text{else}\;\; A - C + F
$$

$$
\text{Up-and-In Put} = A - B + D + E \;\text{if}\; K > H,\;\; \text{else}\;\; C + E
$$

$$
\text{Double Knock-out Call} = S \cdot e^{(b - r) T} \cdot \Sigma_{n} \left[\left(\frac{U^{n}}{L^{n}}\right)^{\mu'} \cdot (N(d_{1}) - N(d_{2})) - \left(\frac{L^{n + 1}}{U^{n} \cdot S}\right)^{\mu'} \cdot (N(d_{3}) - N(d_{4}))\right]
$$

$$
K \cdot e^{- rT} \cdot \Sigma_{n} \left[\left(\frac{U^{n}}{L^{n}}\right)^{\mu' - 2} \cdot (N(d_{1} - \sigma \sqrt{T}) - N(d_{2} - \sigma \sqrt{T})) - \left(\frac{L^{n + 1}}{U^{n} \cdot S}\right)^{\mu' - 2} \cdot (N(d_{3} - \sigma \sqrt{T}) - N(d_{4} - \sigma \sqrt{T}))\right],\;\; \text{with}\;\; \mu' = \frac{2b}{\sigma^{2}} + 1,\;\; d_{1} = \frac{\ln\left(\frac{S \cdot U^{2n}}{K' \cdot L^{2n}}\right) + \left(b + \frac{\sigma^{2}}{2}\right) T}{\sigma \sqrt{T}},\;\; d_{2} \text{ the same with } U \text{ in place of K'},\;\; d_{3} = \frac{\ln\left(\frac{L^{2n + 2}}{K' \cdot S \cdot U^{2n}}\right) + \left(b + \frac{\sigma^{2}}{2}\right) T}{\sigma \sqrt{T}},\;\; d_{4} \text{ the same with } U \text{ in place of K'},\;\; K' = \max(K,\; L),\;\; \text{and the put the same way over the prices between } L \text{ and min(} K \text{, } U \text{)}
$$

$$
\text{Partial-time Knock-out},\;\; \text{start window up to}\; t_{1} = \text{Window Share} \cdot \text{T:} e^{- r t_{1}} \cdot \{E\left[\operatorname{BS}(S(t_{1})) \cdot 1 \{\eta S(t_{1}) > \eta H\}\right]\}
$$

$$
\left(\frac{H}{S}\right)^{2 \mu} \cdot E\left[\operatorname{BS}\left(S(t_{1}) \cdot \left(\frac{H}{S}\right)^{2}\right) \cdot 1 \{\eta S(t_{1}) \cdot \left(\frac{H}{S}\right)^{2} > \eta H\}\right] \;\text{\}},\; \text{with BS the Black-Scholes price over}\; T - t_{1}
$$

$$
\text{Partial-time Knock-out},\;\; \text{end window from}\; t_{1} = (1 - \text{Window Share}) \cdot \text{T:} e^{- r t_{1}} \cdot E\left[\operatorname{KO}(S(t_{1})) \cdot 1 \{\eta S(t_{1}) > \eta H\}\right],\;\; \text{with KO the knock-out price above over}\; T - t_{1};\;\; \text{both expectations are closed form with the bivariate normal distribution}
$$

$$
\text{Soft Knock-out} = \frac{1}{U - L} \cdot \text{∫}_{L}^{U} \;\operatorname{Knock-out}(H) \,\mathrm{d}H \;\text{over the band} \;\left[L,\; U\right]
$$

$$
\text{Discrete monitoring:}\;\; H \text{→} H \cdot e^{0.5826 \cdot \sigma \cdot \sqrt{\Delta t}} \;\text{for a barrier above and}\; H \cdot e^{- 0.5826 \cdot \sigma \cdot \sqrt{\Delta t}} \;\text{for one below}\; S
$$

$$
\text{Every Knock-in of the double},\;\; \text{partial-time and soft barriers} = \text{Black-Scholes price} - \text{Knock-out}
$$

Where S is the stock price (the traded close on the pricing date), K is the strike price, H is the barrier, r is the continuously compounded risk-free rate, q is the continuous dividend yield (ln(1 + dividend yield)), $$\sigma$$ is the annualized volatility (the standard deviation of the daily returns over the trailing 252 trading days times √252), T is the time to expiration in years (days / 365), N is the cumulative standard normal distribution and the Rebate defaults to 0.

A useful identity is in-out parity: without a rebate, a knock-in option plus its corresponding knock-out option (same direction and barrier) equals the price of the equivalent vanilla Black-Scholes option, since the underlying either does or does not touch the barrier. With a rebate, both legs pay it in the scenario where they do not exist, so the sum exceeds the vanilla price by the value of those rebates.

See: Reiner, E., & Rubinstein, M. (1991), "Breaking Down the Barriers", Risk, 4(8), 28-35; Ikeda, M., & Kunitomo, N. (1992), "Pricing Options with Curved Boundaries", Mathematical Finance, 2(4), 275-298; Heynen, R. C., & Kat, H. M. (1994), "Partial Barrier Options", The Journal of Financial Engineering, 3(3/4), 253-274; Hart, I., & Ross, M. (1994), "Striking Continuity", Risk, 7(6), 51-56; Broadie, M., Glasserman, P., & Kou, S. (1997), "A Continuity Correction for Discrete Barrier Options", Mathematical Finance, 7(4), 325-349; Haug, E. G. (2007), The Complete Guide to Option Pricing Formulas, 2nd ed., section 4.17.

**Also known as:** knock-in option, knock-out option, down-and-out, down-and-in, up-and-out, up-and-in option, double barrier option, partial barrier option, window barrier option, soft barrier option, discrete barrier option.

**References:**

- library | Referenced against QuantLib's [AnalyticDoubleBarrierEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_analytic_double_barrier_engine.html){:target="_blank"} (double)
- library | Referenced against QuantLib's [AnalyticPartialTimeBarrierOptionEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_analytic_partial_time_barrier_option_engine.html){:target="_blank"} (partial-time)
- library | Referenced against QuantLib's [AnalyticSoftBarrierEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_analytic_soft_barrier_engine.html){:target="_blank"} (soft)
- library | Shares similar logic as QuantLib's [AnalyticBarrierEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_analytic_barrier_engine.html){:target="_blank"} (single)
- library | Shares similar logic as FinancePy's [EquityBarrierOption](https://github.com/domokane/FinancePy/blob/V1.1.2/financepy/products/equity/equity_barrier_option.py#L28){:target="_blank"} (discretely watched)

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>put_option (bool, optional):</u> Whether to calculate the put option price. Defaults to False which means
it will calculate the call option price.
- <u>barrier_percentage (float, optional):</u> The barrier level as a percentage of the current stock price,
above 0. Defaults to 0.9 which equals 90% of the current stock price. A down barrier needs a value below 1
and an up barrier a value above 1; otherwise the barrier is already breached.
- <u>barrier_direction (str, optional):</u> The side of the barrier. Options are: "down" (below the stock
price), "up" (above the stock price), "double" (barrier_percentage is then the lower and
upper_barrier_percentage the upper barrier). Defaults to "down".
- <u>knock_type (str, optional):</u> The knock. Options are: "in" (knock-in), "out" (knock-out). Defaults to
"out".
- <u>rebate (float, optional):</u> The fixed cash amount paid out if the option knocks out (or fails to knock
in), for a single barrier watched over the whole life only. Defaults to 0.0.
- <u>upper_barrier_percentage (float, optional):</u> The upper barrier of a double barrier option as a
percentage of the current stock price. Defaults to 1.1, 110% of the current stock price.
- <u>barrier_window (str, optional):</u> When the barrier is watched. Options are: "full" (the whole life),
"start" (the first window_share of the life), "end" (the last window_share of the life). Defaults to
"full".
- <u>window_share (float, optional):</u> The share of the life a "start" or "end" window covers, above 0 and at
most 1. Defaults to 0.5.
- <u>soft_barrier_percentage (float &#124; None, optional):</u> The other edge of a soft barrier band (the first is
barrier_percentage), on the same side of the stock price. Defaults to None, a hard barrier.
- <u>monitoring (str, optional):</u> How often the barrier is checked. Options are: "continuous"
(continuously), "daily" (252 times a year), "weekly" (52 times a year), "monthly" (12 times a year).
Defaults to "continuous".
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None, which
uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Barrier option values containing the tickers and strike prices as the index and the
time to expiration as the columns.

**Raises:**

InvalidArgumentError: If barrier_percentage is not above 0 or puts the barrier at or beyond the current stock price for the
given barrier_direction (at or below 1 for "up", at or above 1 for "down", or outside the lower and
upper barrier for "double"), since such a barrier is breached at the start and every price would
be the rebate (knock-out) or the vanilla price (knock-in); or when a rebate is combined with a
double, partial-time or soft barrier, or two of those are combined, or monitoring is not one of its values.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["META"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

barrier_option = toolkit.options.get_barrier_option(
    strike_price_range=0.1, strike_step_size=10, expiration_time_range=91
)

barrier_option.loc["META", ["2026-01-30", "2026-03-01", "2026-03-31"]]
```

Which returns:

|   Strike Price |   2026-01-30 |   2026-03-01 |   2026-03-31 |
|---------------:|-------------:|-------------:|-------------:|
|            590 |      70.2113 |      70.5597 |      71.0164 |
|            600 |      63.6597 |      65.6622 |      66.9713 |
|            610 |      57.1768 |      60.7954 |      62.9442 |
|            620 |      50.8683 |      56.0068 |      58.9631 |
|            630 |      44.827  |      51.3397 |      55.0541 |
|            640 |      39.1295 |      46.8319 |      51.2401 |
|            650 |      33.8345 |      42.5151 |      47.5413 |
|            660 |      28.9823 |      38.4145 |      43.9749 |
|            670 |      24.5957 |      34.5495 |      40.5549 |
|            680 |      20.6814 |      30.9334 |      37.2922 |
|            690 |      17.2323 |      27.5738 |      34.1949 |
|            700 |      14.23   |      24.4735 |      31.2686 |
|            710 |      11.6473 |      21.6308 |      28.5162 |
|            720 |       9.4508 |      19.0403 |      25.9385 |

---

## get_asian_option
Calculate the price of an average price Asian option: what an option on each ticker is worth whose payoff depends on the average stock price over its life rather than the price at expiration.

The geometric average is priced in closed form (Kemna & Vorst, 1990) and the arithmetic average, the kind that is traded, with the approximations of Turnbull and Wakeman (1991) or Curran (1994), or a Monte Carlo simulation with the geometric option as control variate.

An Asian option's payoff, max(A - K, 0) for a call and max(K - A, 0) for a put, depends on the average A of the stock price rather than its price at expiration, which typically makes it cheaper than the equivalent vanilla option (the averaging reduces variance). The average is taken continuously, or over a number of equally spaced fixings, the first a 1/n-th of the life from now and the last at expiration. The methods are:

- Geometric: the geometric average of a lognormal price is lognormal, so this is a Black-Scholes option on it. It never exceeds the arithmetic average, so it is a lower bound for the arithmetic call and an upper bound for the arithmetic put.
- Turnbull-Wakeman: takes the arithmetic average to be lognormal with its exact first two moments. Fast and close at low volatilities and short maturities, but it loses accuracy as both grow (off by up to 0.8 on a stock price of 100 at 60% volatility over two years). For a continuous average that starts today, Levy (1992) matches the same two moments with a lognormal and gives the same price; the two differ only for an average that has already started.
- Curran: conditions on the geometric average, which is exact for the paths on which the geometric average ends above the strike (there A ≥ G ≥ K) and approximates the others. The most accurate of the approximations: within 0.05 of a simulation with 200,000 paths on a stock price of 100 up to 60% volatility and two years, and within 0.002 at 15% volatility.
- Monte Carlo: simulates the arithmetic average along each path and corrects the simulation error with the geometric option, whose price is known, which makes it about 50 to 100 times more precise than a plain simulation. A continuous average is approximated by a number of fixings.

The formula is as follows:

$$
\text{Geometric:}\;\; E\left[\ln G\right] = \ln S + \frac{\left(b - \frac{\sigma^{2}}{2}\right) \cdot T}{2}\;\;\text{and}\;\; \text{Var}\left[\ln G\right] = \frac{\sigma^{2} \cdot T}{3} \;\text{for a continuous average},\;\; E\left[\ln G\right] = \ln S + \frac{\left(b - \frac{\sigma^{2}}{2}\right) \cdot T \cdot (n + 1)}{2n}\;\;\text{and}\;\; \text{Var}\left[\ln G\right] = \frac{\sigma^{2} \cdot T \cdot (n + 1) (2n + 1)}{6n^{2}} \;\text{for}\; n \;\text{fixings},\;\; \text{Call} = e^{- rT} \cdot \left(e^{E\left[\ln G\right] + \frac{\text{Var}\left[\ln G\right]}{2}} \cdot N(d_{1}) - K \cdot N(d_{2})\right),\;\; d_{1} = \frac{E\left[\ln G\right] - \ln K + \text{Var}\left[\ln G\right]}{\sqrt{\text{Var}} \left[\ln G\right]},\;\; d_{2} = d_{1} - \sqrt{\text{Var}} \left[\ln G\right]
$$

$$
\text{Turnbull-Wakeman:}\;\; M_{1} = \frac{E\left[A\right]}{S},\;\; M_{2} = \frac{E\left[A^{2}\right]}{S^{2}},\;\; F_{A} = S \cdot M_{1},\;\; v = \ln\left(\frac{M_{2}}{M_{1}^{2}}\right),\;\; \text{Call} = e^{- rT} \cdot (F_{A} \cdot N(d_{1}) - K \cdot N(d_{2})),\;\; d_{1} = \frac{\ln\left(\frac{F_{A}}{K}\right) + \frac{v}{2}}{\sqrt{v}},\;\; d_{2} = d_{1} - \sqrt{v},\;\; \text{with}\;\; M_{1} = \frac{e^{bT} - 1}{bT}\;\;\text{and}\;\; M_{2} = \frac{\frac{2}{T^{2}} \cdot \text{∫}_{0}^{T} e^{\text{bt}} \cdot (e^{(b + \sigma^{2}) t} - 1)}{b + \sigma^{2}} \,\mathrm{d}t \;\text{for a continuous average}\;\;\text{and}\;\; M_{1} = \frac{\sum e^{b t_{i}}}{n},\;\; M_{2} = \frac{\Sigma_{i} \Sigma_{j} e^{b(t_{i} + t_{j}) + \sigma^{2} \min(t_{i},\; t_{j})}}{n^{2}} \;\text{for fixings}\; t_{i} = \frac{iT}{n}
$$

$$
\text{Curran:}\;\; \mu_{i} = \ln S + \left(b - \frac{\sigma^{2}}{2}\right) \cdot t_{i},\;\; \sigma_{i}^{2} = \sigma^{2} \cdot t_{i},\;\; \mu_{G} = \frac{\sum \mu_{i}}{n},\;\; \sigma_{G}^{2} = \frac{\sigma^{2} \cdot \Sigma_{i} \Sigma_{j} \min(t_{i},\; t_{j})}{n^{2}},\;\; \sigma_{iG} = \frac{\sigma^{2} \cdot \Sigma_{j} \min(t_{i},\; t_{j})}{n},\;\; \hat{K} = 2K - \frac{\sum e^{\mu_{i} + \frac{\sigma_{iG}}{\sigma_{G}^{2}} \cdot (\ln K - \mu_{G}) + \frac{\sigma_{i}^{2} - \frac{\sigma_{iG}^{2}}{\sigma_{G}^{2}}}{2}}}{n},\;\; \text{Call} = e^{- rT} \cdot \left[\frac{\sum e^{\mu_{i} + \frac{\sigma_{i}^{2}}{2}} \cdot N\left(\frac{\mu_{G} - \ln \hat{K}}{\sigma_{G}} + \frac{\sigma_{iG}}{\sigma_{G}}\right)}{n} - K \cdot N\left(\frac{\mu_{G} - \ln \hat{K}}{\sigma_{G}}\right)\right],\;\; \text{with integrals over [0, } T \text{] in place of the sums for a continuous average}
$$

$$
\text{Monte Carlo:}\;\; S(t_{i}) = S(\text{t\_i-1}) \cdot e^{\left(b - \frac{\sigma^{2}}{2}\right) \cdot \Delta t + \sigma \cdot \sqrt{\Delta t} \cdot Z} \;\text{at}\; n \;\text{fixings} \;(\text{time\_steps} \;\text{for a continuous average}),\;\; Y = e^{- rT} \cdot \max(A - K,\; 0)\;\;\text{and}\;\; X = e^{- rT} \cdot \max(G - K,\; 0) \;\text{per path},\;\; \text{Call} = \operatorname{MEAN}(Y) - \beta \cdot (\operatorname{MEAN}(X) - \text{Geometric Call}),\;\; \beta = \frac{\operatorname{Cov}(Y,\; X)}{\operatorname{Var}(X) (\text{ddof} = 1)}
$$

$$
\text{Put} = \text{Call} - e^{- rT} \cdot (E\left[A\right] - K) \;\text{by put-call parity of the average} \;(\text{the geometric put and the Monte Carlo put are priced directly})
$$

Where S is the stock price (the traded close on the pricing date), K is the strike price, r is the continuously compounded risk-free rate, q is the continuous dividend yield (ln(1 + dividend yield)), $$b = r - q$$ is the cost of carry, $$\sigma$$ is the annualized volatility (the standard deviation of the daily returns over the trailing 252 trading days times √252), T is the time to expiration in years (days / 365), n is the number of fixings, G and A are the geometric and arithmetic average and N is the cumulative standard normal distribution.

The Monte Carlo prices are reproducible with a seed, and all strike prices of an expiry are priced on the same paths. Its standard error is around 0.1% of the price with the defaults.

See: Kemna, A. G. Z., & Vorst, A. C. F. (1990), "A Pricing Method for Options Based on Average Asset Values", Journal of Banking & Finance, 14(1), 113-129; Turnbull, S. M., & Wakeman, L. M. (1991), "A Quick Algorithm for Pricing European Average Options", Journal of Financial and Quantitative Analysis, 26(3), 377-389; Levy, E. (1992), "Pricing European Average Rate Currency Options", Journal of International Money and Finance, 11(5), 474-491; Curran, M. (1994), "Valuing Asian and Portfolio Options by Conditioning on the Geometric Mean Price", Management Science, 40(12), 1705-1711; Haug, E. G. (2007), The Complete Guide to Option Pricing Formulas, 2nd ed., section 4.20.

**Also known as:** Asian option, average rate option, average price option, arithmetic Asian option, geometric Asian option.

**References:**

- library | Referenced against QuantLib's [AnalyticDiscreteGeometricAveragePriceAsianEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_analytic_discrete_geometric_average_price_asian_engine.html){:target="_blank"} (geometric, fixings)
- library | Referenced against QuantLib's [TurnbullWakemanAsianEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_turnbull_wakeman_asian_engine.html){:target="_blank"} (Turnbull-Wakeman)
- library | Referenced against QuantLib's [ContinuousArithmeticAsianLevyEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_continuous_arithmetic_asian_levy_engine.html){:target="_blank"} (Turnbull-Wakeman, continuous)
- library | Referenced against QuantLib's [MCDiscreteArithmeticAPEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_m_c_discrete_arithmetic_a_p_engine.html){:target="_blank"} (Curran, Monte Carlo)
- library | Shares similar logic as QuantLib's [AnalyticContinuousGeometricAveragePriceAsianEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_analytic_continuous_geometric_average_price_asian_engine.html){:target="_blank"} (geometric, continuous)
- library | Shares similar logic as FinancePy's [EquityAsianOption.value_geometric](https://github.com/domokane/FinancePy/blob/V1.1.2/financepy/products/equity/equity_asian_option.py#L180){:target="_blank"} (geometric)
- library | Shares similar logic as FinancePy's [EquityAsianOption.value_turnbull_wakeman](https://github.com/domokane/FinancePy/blob/V1.1.2/financepy/products/equity/equity_asian_option.py#L332){:target="_blank"} (Turnbull-Wakeman)
- library | Shares similar logic as FinancePy's [EquityAsianOption.value_curran](https://github.com/domokane/FinancePy/blob/V1.1.2/financepy/products/equity/equity_asian_option.py#L256){:target="_blank"} (Curran)

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>put_option (bool, optional):</u> Whether to calculate the put option price. Defaults to False which means
it will calculate the call option price.
- <u>method (str, optional):</u> The pricing method. Options are: "geometric" (the geometric average),
"turnbull_wakeman" (Turnbull-Wakeman, arithmetic average), "curran" (Curran, arithmetic average),
"monte_carlo" (Monte Carlo, arithmetic average). Defaults to "geometric".
- <u>fixings (int &#124; None, optional):</u> The number of equally spaced fixings of the average, at least 1, the last on the
expiration date. Defaults to None, which averages continuously.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None, which
uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>simulations (int, optional):</u> The number of simulated paths of the Monte Carlo method, at least 1. Defaults
to 10,000.
- <u>time_steps (int, optional):</u> The fixings that approximate a continuous average with the Monte Carlo method,
at least 1 (fixings, when given, take their place). Defaults to 100.
- <u>seed (int &#124; None, optional):</u> The seed of the random number generator of the Monte Carlo method, which
makes the results reproducible; None draws new paths on every call. Defaults to 0.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Asian option values containing the tickers and strike prices as the index and the time to
expiration as the columns.

**Raises:**

InvalidArgumentError: If method is not one of the methods or fixings, simulations or time_steps is not a whole
number of at least 1.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

asian_option = toolkit.options.get_asian_option(
    method="curran", fixings=21, strike_price_range=0.1, strike_step_size=2, expiration_time_range=91
)

asian_option.loc["XOM", ["2026-01-30", "2026-03-01", "2026-03-31"]]
```

Which returns:

|   Strike Price |   2026-01-30 |   2026-03-01 |   2026-03-31 |
|---------------:|-------------:|-------------:|-------------:|
|            108 |      12.3465 |      12.4086 |      12.5336 |
|            110 |      10.3676 |      10.5055 |      10.7123 |
|            112 |       8.4205 |       8.678  |       8.9842 |
|            114 |       6.5487 |       6.9662 |       7.3786 |
|            116 |       4.8214 |       5.4133 |       5.9236 |
|            118 |       3.3215 |       4.0579 |       4.6412 |
|            120 |       2.1184 |       2.9257 |       3.5445 |
|            122 |       1.2399 |       2.0242 |       2.6359 |
|            124 |       0.6617 |       1.3417 |       1.9077 |
|            126 |       0.3207 |       0.8511 |       1.3431 |
|            128 |       0.1408 |       0.5164 |       0.9198 |
|            130 |       0.056  |       0.2997 |       0.6128 |
|            132 |       0.0202 |       0.1665 |       0.3973 |
|            134 |       0.0066 |       0.0885 |       0.2507 |

---

## get_lookback_option
Calculate the closed-form price of a lookback option: what an option on each ticker is worth whose payoff depends on the highest or lowest stock price over its life.

The formulas are those of Conze and Viswanathan (1991) for a fixed strike, Goldman, Sosin and Gatto (1979) for a floating strike and Heynen and Kat (1994) for a partial-time lookback.

- Fixed strike: the call pays $$\max (S_{\text{max}} - K , 0)$$ and the put $$\max (K - S_{\text{min}} , 0)$$, the best price reached against the strike.
- Floating strike: the call pays $$S (T) - S_{\text{min}}$$, buying at the lowest price, and the put $$S_{\text{max}} - S (T)$$, selling at the highest. It has no strike, so the result has a row per ticker.
- Partial-time (a lookback period below 1): the extreme is only watched during part of the life, the first part for a floating strike and the last part for a fixed strike, which makes the option cheaper.

The options start on the pricing date, so the highest and lowest price so far are the stock price.

The formula is as follows:

$$
x = \frac{\ln\left(\frac{S}{E}\right) + \left(b + \frac{\sigma^{2}}{2}\right) \cdot T}{\sigma \sqrt{T}},\;\; \text{with}\;\; E \text{ the extreme so far:}\;\; E = \max(S,\; K) \;\text{for a fixed call},\;\; \text{min(} S \text{, } K \text{) for a fixed put and } S \text{ for a floating strike}
$$

$$
\text{Fixed Call} = e^{- rT} \cdot (E - K) + S \cdot e^{(b - r) T} \cdot N(x) - E \cdot e^{- rT} \cdot N(x - \sigma \sqrt{T}) + \frac{S \cdot e^{- rT} \cdot \sigma^{2}}{2b} \cdot \left[- \left(\frac{S}{E}\right)^{- \frac{2b}{\sigma^{2}}} \cdot N\left(x - \frac{2b \sqrt{T}}{\sigma}\right) + e^{bT} \cdot N(x)\right]
$$

$$
\text{Fixed Put} = e^{- rT} \cdot (K - E) - S \cdot e^{(b - r) T} \cdot N(- x) + E \cdot e^{- rT} \cdot N(- x + \sigma \sqrt{T}) + \frac{S \cdot e^{- rT} \cdot \sigma^{2}}{2b} \cdot \left[\left(\frac{S}{E}\right)^{- \frac{2b}{\sigma^{2}}} \cdot N\left(- x + \frac{2b \sqrt{T}}{\sigma}\right) - e^{bT} \cdot N(- x)\right]
$$

$$
\text{Floating Call} = S \cdot e^{(b - r) T} \cdot N(x) - E \cdot e^{- rT} \cdot N(x - \sigma \sqrt{T}) + \frac{S \cdot e^{- rT} \cdot \sigma^{2}}{2b} \cdot \left[\left(\frac{S}{E}\right)^{- \frac{2b}{\sigma^{2}}} \cdot N\left(- x + \frac{2b \sqrt{T}}{\sigma}\right) - e^{bT} \cdot N(- x)\right]
$$

$$
\text{Floating Put} = E \cdot e^{- rT} \cdot N(- x + \sigma \sqrt{T}) - S \cdot e^{(b - r) T} \cdot N(- x) + \frac{S \cdot e^{- rT} \cdot \sigma^{2}}{2b} \cdot \left[- \left(\frac{S}{E}\right)^{- \frac{2b}{\sigma^{2}}} \cdot N\left(x - \frac{2b \sqrt{T}}{\sigma}\right) + e^{bT} \cdot N(x)\right]
$$

$$
\text{Partial Fixed},\;\; \text{watched from}\; t_{1} = (1 - \text{Lookback Period}) \cdot \text{T:} e^{- r t_{1}} \cdot E\left[\operatorname{Fixed}(S(t_{1}),\; T - t_{1})\right],\;\; \text{in closed form with the bivariate normal distribution}
$$

$$
\text{Partial Floating},\;\; \text{watched up to}\; t_{1} = \text{Lookback Period} \cdot \text{T:} S \cdot e^{(b - r) t_{1}} \cdot E'\left[c(e^{- X},\; T - t_{1})\right] \;\text{for a call},\;\; \text{with}\;\; c \;\text{the Black-Scholes call on a unit stock price and}\; X = \ln\left(\frac{S(t_{1})}{S_{min}(t_{1})}\right),\;\; \text{which is distributed as the running maximum of a Brownian motion with drift}\; b + \frac{\sigma^{2}}{2} \;(\text{time reversal}),\;\; \text{integrated over its density}
$$

Where S is the stock price (the traded close on the pricing date), K is the strike price, r is the continuously compounded risk-free rate, q is the continuous dividend yield (ln(1 + dividend yield)), $$b = r - q$$ is the cost of carry, $$\sigma$$ is the annualized volatility (the standard deviation of the daily returns over the trailing 252 trading days times √252), T is the time to expiration in years (days / 365) and N is the cumulative standard normal distribution. Where $$b = 0$$ the formulas are taken at b = ±0.00001 and averaged, which equals their limit to within $$O (b^{2})$$.

See: Goldman, M. B., Sosin, H. B., & Gatto, M. A. (1979), "Path Dependent Options: Buy at the Low, Sell at the High", The Journal of Finance, 34(5), 1111-1127; Conze, A., & Viswanathan (1991), "Path Dependent Options: The Case of Lookback Options", The Journal of Finance, 46(5), 1893-1907; Heynen, R. C., & Kat, H. M. (1994), "Selective Memory", Risk, 7(11), 73-76; Haug, E. G. (2007), The Complete Guide to Option Pricing Formulas, 2nd ed., section 4.15.

**Also known as:** lookback option, fixed strike lookback, floating strike lookback, partial lookback, hindsight option, no-regret option.

**References:**

- library | Referenced against QuantLib's [AnalyticContinuousFixedLookbackEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_analytic_continuous_fixed_lookback_engine.html){:target="_blank"} (fixed strike)
- library | Referenced against QuantLib's [AnalyticContinuousFloatingLookbackEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_analytic_continuous_floating_lookback_engine.html){:target="_blank"} (floating strike)
- library | Referenced against QuantLib's [AnalyticContinuousPartialFixedLookbackEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_analytic_continuous_partial_fixed_lookback_engine.html){:target="_blank"} (partial fixed strike)
- library | Referenced against QuantLib's [AnalyticContinuousPartialFloatingLookbackEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_analytic_continuous_partial_floating_lookback_engine.html){:target="_blank"} (partial floating strike)

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>put_option (bool, optional):</u> Whether to calculate the put option price. Defaults to False which means
it will calculate the call option price.
- <u>strike_type (str, optional):</u> The strike. Options are: "fixed" (fixed strike), "floating" (floating
strike). Defaults to "fixed".
- <u>lookback_period (float, optional):</u> The share of the life over which the extreme is watched, above 0 and
at most 1: the start of the life for a floating strike and the end for a fixed strike. Defaults to 1,
the whole life.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100. Not used for a
floating strike.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100. Not used for a
floating strike.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None, which
uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker (and strike price). Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Lookback option values containing the tickers and strike prices (only the tickers for a
floating strike) as the index and the time to expiration as the columns.

**Raises:**

InvalidArgumentError: If strike_type is not "fixed" or "floating" or lookback_period is not above 0 and at most 1.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NVDA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

lookback_option = toolkit.options.get_lookback_option(
    strike_price_range=0.1, strike_step_size=5, expiration_time_range=91
)

lookback_option.loc["NVDA", ["2026-01-30", "2026-03-01", "2026-03-31"]]
```

Which returns:

|   Strike Price |   2026-01-30 |   2026-03-01 |   2026-03-31 |
|---------------:|-------------:|-------------:|-------------:|
|            165 |      43.8427 |      53.7637 |      61.6312 |
|            170 |      38.8596 |      48.7974 |      56.6817 |
|            175 |      33.8765 |      43.8312 |      51.7322 |
|            180 |      28.8934 |      38.8649 |      46.7827 |
|            185 |      23.9103 |      33.8986 |      41.8332 |
|            190 |      19.1196 |      29.0713 |      36.9989 |
|            195 |      15.0553 |      24.7714 |      32.6025 |
|            200 |      11.6939 |      20.9915 |      28.6406 |
|            205 |       8.9622 |      17.694  |      25.0864 |
|            210 |       6.7797 |      14.8381 |      21.9116 |
TABLE_LOOKBACK

---

## get_touch_option
Calculate the closed-form price of a one-touch, no-touch, double one-touch or double no-touch option: what a binary option on whether the stock price of each ticker touches a barrier before expiration is worth.

The formulas are those of Reiner and Rubinstein (1991) for a single barrier and Hui (1996) for two barriers.

A touch option is a binary option on whether the stock price touches a barrier before expiration:

- One-touch: pays the cash payout once the barrier at barrier_percentage of the stock price is touched, at that moment or at expiration (see payment).
- No-touch: pays the cash payout at expiration when the barrier is never touched.
- Double one-touch: pays at expiration when either the lower barrier (barrier_percentage) or the upper barrier (upper_barrier_percentage) is touched.
- Double no-touch: pays at expiration when the stock price stays between the two barriers.

A barrier below the stock price (barrier_percentage below 1) is touched when the price falls to it, one above (barrier_percentage above 1) when the price rises to it. The price of a one-touch paid at expiration is the discounted risk-neutral probability of touching the barrier, so with a cash payout of 1 and the discounting removed it reads as that probability.

The formula is as follows:

$$
P(\text{touch}) = N\left(\frac{\eta(h - \nu T)}{\sigma \sqrt{T}}\right) + \left(\frac{H}{S}\right)^{2 \mu} \cdot N\left(\frac{\eta(h + \nu T)}{\sigma \sqrt{T}}\right)
$$

$$
\text{One-touch},\;\; \text{paid at expiration} = \text{Cash} \cdot e^{- rT} \cdot P(\text{touch}),\;\; \text{with Cash defaulting to 1}
$$

$$
\text{One-touch},\;\; \text{paid at the hit} = \text{Cash} \cdot \left[\left(\frac{H}{S}\right)^{\mu + \lambda} \cdot N(\eta z) + \left(\frac{H}{S}\right)^{\mu - \lambda} \cdot N(\eta z - 2 \eta \lambda \sigma \sqrt{T})\right],\;\; z = \frac{h}{\sigma \sqrt{T}} + \lambda \sigma \sqrt{T}
$$

$$
\text{No-touch} = \text{Cash} \cdot e^{- rT} \cdot (1 - P(\text{touch}))
$$

$$
P(\text{stay}) = \Sigma_{n} \left[e^{\frac{\text{2nZ} \nu}{\sigma^{2}}} \cdot \left(N\left(\frac{u - \text{2nZ} - \nu T}{\sigma \sqrt{T}}\right) - N\left(\frac{l - \text{2nZ} - \nu T}{\sigma \sqrt{T}}\right)\right)\right]
$$

$$
e^{\frac{2 \nu(l - nZ)}{\sigma^{2}}} \cdot \left(N\left(\frac{u - 2l + \text{2nZ} - \nu T}{\sigma \sqrt{T}}\right) - N\left(\frac{- l + \text{2nZ} - \nu T}{\sigma \sqrt{T}}\right)\right) \;\text{]}
$$

$$
\text{Double no-touch} = \text{Cash} \cdot e^{- rT} \cdot P(\text{stay})
$$

$$
\text{Double one-touch} = \text{Cash} \cdot e^{- rT} \cdot (1 - P(\text{stay}))
$$

$$
\text{Discrete monitoring:}\;\; H \text{→} H \cdot e^{0.5826 \cdot \sigma \cdot \sqrt{\Delta t}} \;\text{for a barrier above and}\; H \cdot e^{- 0.5826 \cdot \sigma \cdot \sqrt{\Delta t}} \;\text{for one below the stock price},\;\; \text{with}\;\; \Delta t = \frac{1}{252},\; \frac{1}{52} \;\text{or} \;\frac{1}{12} \;(\text{Broadie},\; \text{Glasserman}\; \text{\&} \;\text{Kou},\; 1997)
$$

Where S is the stock price (the traded close on the pricing date), H is the barrier, $$h = \ln (H / S)$$, $$l = \ln (L / S)$$ and $$u = \ln (U / S)$$ with L and U the lower and upper barrier, $$Z = u - l$$, r is the continuously compounded risk-free rate, q is the continuous dividend yield (ln(1 + dividend yield)), $$\nu = r - q - \sigma^{2} / 2$$, $$\mu = \nu / \sigma^{2}$$, $$\lambda = \sqrt{\mu^{2} + 2 r / \sigma^{2}}$$, $$\eta = 1$$ for a barrier below and -1 for one above the stock price, $$\sigma$$ is the annualized volatility (the standard deviation of the daily returns over the trailing 252 trading days times √252), T is the time to expiration in years (days / 365) and N is the cumulative standard normal distribution. P(stay) is the probability of staying between the barriers from the method of images, summed until its terms are below machine precision; Hui (1996) writes the same probability as a sine series.

See: Reiner, E., & Rubinstein, M. (1991), "Unscrambling the Binary Code", Risk, 4(9), 75-83; Hui, C. H. (1996), "One-Touch Double Barrier Binary Option Values", Applied Financial Economics, 6(4), 343-346; Broadie, M., Glasserman, P., & Kou, S. (1997), "A Continuity Correction for Discrete Barrier Options", Mathematical Finance, 7(4), 325-349; Haug, E. G. (2007), The Complete Guide to Option Pricing Formulas, 2nd ed., section 4.19.

**Also known as:** one-touch option, no-touch option, double one-touch, double no-touch, American digital option, barrier binary option, touch probability.

**References:**

- library | Referenced against QuantLib's [AnalyticDigitalAmericanEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_analytic_digital_american_engine.html){:target="_blank"} (one-touch)
- library | Referenced against QuantLib's [AnalyticBinaryBarrierEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_analytic_binary_barrier_engine.html){:target="_blank"} (no-touch)
- library | Referenced against QuantLib's [AnalyticDoubleBarrierBinaryEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_analytic_double_barrier_binary_engine.html){:target="_blank"} (double one-touch, double no-touch)

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>option_type (str, optional):</u> The kind of touch option. Options are: "one-touch" (one-touch),
"no-touch" (no-touch), "double-one-touch" (double one-touch), "double-no-touch" (double no-touch).
Defaults to "one-touch".
- <u>barrier_percentage (float, optional):</u> The barrier (the lower barrier of a double touch option) as a
percentage of the current stock price, above 0. Defaults to 0.9, 90% of the current stock price.
- <u>upper_barrier_percentage (float, optional):</u> The upper barrier of a double touch option as a percentage of
the current stock price. Defaults to 1.1, 110% of the current stock price.
- <u>payment (str, optional):</u> When a one-touch option pays. Options are: "expiration" (at expiration),
"hit" (when the barrier is touched). The other touch options pay at expiration. Defaults to
"expiration".
- <u>cash_payout (float, optional):</u> The cash amount paid. Defaults to 1.0.
- <u>monitoring (str, optional):</u> How often the barrier is checked. Options are: "continuous"
(continuously), "daily" (252 times a year), "weekly" (52 times a year), "monthly" (12 times a year).
Defaults to "continuous".
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None, which
uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Touch option values containing the tickers as the index and the time to expiration as the
columns.

**Raises:**

InvalidArgumentError: If option_type, payment or monitoring is not one of its values, a touch option other
than the one-touch is asked to pay at the hit, barrier_percentage is not above 0, the barrier is at the
current stock price or a double touch option's barriers do not lie on either side of it.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["TSLA", "KO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

touch_option = toolkit.options.get_touch_option(
    option_type="double-no-touch", barrier_percentage=0.9, upper_barrier_percentage=1.1,
    expiration_time_range=91,
)

touch_option[["2026-01-07", "2026-01-30", "2026-03-01", "2026-03-31"]]
```

Which returns:

| Ticker   |   2026-01-07 |   2026-01-30 |   2026-03-01 |   2026-03-31 |
|:---------|-------------:|-------------:|-------------:|-------------:|
| TSLA     |       0.4951 |       0.0223 |       0.0004 |       0      |
| KO       |       0.9991 |       0.9028 |       0.6768 |       0.4958 |
TABLE_TOUCH

---

## get_chooser_option
Calculate the closed-form price of a simple chooser option: what the right to decide at the choice time whether the option on each ticker becomes a European call or a European put is worth, with the formula of Rubinstein (1991).

The call and the put share the strike price and expiration, so the chooser is worth at least as much as either and at most as much as the straddle of both.

The choice is made after a share of the life, the choice period: at a choice period of 0 the chooser is the larger of the call and the put today, at 1 a straddle. By put-call parity at the choice time t the chooser is a call on (K, T) plus a put on ($$K \cdot e^{- (r - q) (T - t)} , t$$), scaled by $$e^{- q (T - t)}$$.

The formula is as follows:

$$
t = \text{Choice Period} \cdot T
$$

$$
d = \frac{\ln\left(\frac{S}{K}\right) + \left(r - q + \frac{\sigma^{2}}{2}\right) \cdot T}{\sigma \sqrt{T}}
$$

$$
y = \frac{\ln\left(\frac{S}{K}\right) + (r - q) \cdot T + \frac{\sigma^{2} \cdot t}{2}}{\sigma \sqrt{t}}
$$

$$
\text{Chooser} = S \cdot e^{- qT} \cdot N(d) - K \cdot e^{- rT} \cdot N(d - \sigma \sqrt{T}) - S \cdot e^{- qT} \cdot N(- y) + K \cdot e^{- rT} \cdot N(- y + \sigma \sqrt{t})
$$

Where S is the stock price (the traded close on the pricing date), K is the strike price, r is the continuously compounded risk-free rate, q is the continuous dividend yield (ln(1 + dividend yield)), $$\sigma$$ is the annualized volatility (the standard deviation of the daily returns over the trailing 252 trading days times √252), T is the time to expiration in years (days / 365) and N is the cumulative standard normal distribution.

A complex chooser, which chooses between a call and a put with their own strike and expiration, is priced by the model function financetoolkit.options.pricing.compound_model.get_chooser_option with put_strike_price and put_time_to_expiration.

See: Rubinstein, M. (1991), "Options for the Undecided", Risk, 4(4), 43; Haug, E. G. (2007), The Complete Guide to Option Pricing Formulas, 2nd ed., section 4.10.

**Also known as:** chooser option, as-you-like-it option, pay now choose later option.

**References:**

- library | Referenced against QuantLib's [AnalyticSimpleChooserEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_analytic_simple_chooser_engine.html){:target="_blank"}
- library | Shares similar logic as FinancePy's [EquityChooserOption](https://github.com/domokane/FinancePy/blob/V1.1.2/financepy/products/equity/equity_chooser_option.py#L67){:target="_blank"}

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>choice_period (float, optional):</u> The share of the life after which the holder chooses between the call
and the put, at least 0 and at most 1. Defaults to 0.5, halfway.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which equals
25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that the
strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None, which
uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Chooser option values containing the tickers and strike prices as the index and the time
to expiration as the columns.

**Raises:**

InvalidArgumentError: If choice_period is not at least 0 and at most 1.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NVDA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

chooser_option = toolkit.options.get_chooser_option(
    strike_price_range=0.1, strike_step_size=5, expiration_time_range=91
)

chooser_option.loc["NVDA", ["2026-01-30", "2026-03-01", "2026-03-31"]]
```

Which returns:

|   Strike Price |   2026-01-30 |   2026-03-01 |   2026-03-31 |
|---------------:|-------------:|-------------:|-------------:|
|            165 |      25.515  |      30.5881 |      35.0495 |
|            170 |      22.4621 |      28.3685 |      33.27   |
|            175 |      20.1357 |      26.7519 |      32.0089 |
|            180 |      18.6412 |      25.7699 |      31.2783 |
|            185 |      18.0413 |      25.4352 |      31.0788 |
|            190 |      18.3475 |      25.7412 |      31.4009 |
|            195 |      19.5216 |      26.6638 |      32.226  |
|            200 |      21.485  |      28.1649 |      33.5281 |
|            205 |      24.1331 |      30.1962 |      35.2753 |
|            210 |      27.3507 |      32.7032 |      37.4324 |

---

## get_forward_start_option
Calculate the closed-form price of a forward-start option: what a European option on each ticker is worth whose strike is set later at a share of the stock price then, with the formula of Rubinstein (1990), or of a cliquet (ratchet) option, a series of them, or of their performance versions.

- Forward-start (one period): a European option whose strike is set after the start period of the life to moneyness times the stock price then, paying $$\max (S (T) - \alpha \cdot S (t_{1}) , 0)$$ for a call.
- Cliquet (more than one period): the time from the start to expiration is split into equal periods, and each period is a forward-start option whose strike is reset to moneyness times the stock price at its start and whose payoff is paid at its end. With a start period of 0 the first period starts today.
- Performance: each period pays the return S(t(i+1)) / S(ti) beyond the moneyness instead, max(S(t(i+1)) / S(ti) - $$\alpha$$, 0) for a call, a decimal per unit of notional.

The options have no strike today, so the result has a row per ticker.

The formula is as follows:

$$
t_{1} = \text{Start Period} \cdot T,\;\; \text{ti} = t_{1} + \frac{(i - 1) \cdot (T - t_{1})}{\text{Periods}}\;\;\text{and}\;\; t(\text{Periods} + 1) = T
$$

$$
\text{Forward Start} = \sum S \cdot e^{- q \;\text{ti}} \cdot \operatorname{BS}(1,\; \alpha,\; t(i + 1) - \text{ti})
$$

$$
\text{Performance} = \sum e^{- r \;\text{ti}} \cdot \operatorname{BS}(1,\; \alpha,\; t(i + 1) - \text{ti})
$$

$$
\operatorname{BS}(1,\; \alpha,\; \tau) = e^{- q \tau} \cdot N(d_{1}) - \alpha \cdot e^{- r \tau} \cdot N(d_{1} - \sigma \sqrt{\tau}) \;\text{for a call and}\; \alpha \cdot e^{- r \tau} \cdot N(- d_{1} + \sigma \sqrt{\tau})
$$

$$
e^{- q \tau} \cdot N(- d_{1}) \;\text{for a put},\;\; d_{1} = \frac{\ln\left(\frac{1}{\alpha}\right) + \left(r - q + \frac{\sigma^{2}}{2}\right) \cdot \tau}{\sigma \sqrt{\tau}}
$$

Where S is the stock price (the traded close on the pricing date), $$\alpha$$ is the moneyness, r is the continuously compounded risk-free rate, q is the continuous dividend yield (ln(1 + dividend yield)), $$\sigma$$ is the annualized volatility (the standard deviation of the daily returns over the trailing 252 trading days times √252), T is the time to expiration in years (days / 365) and N is the cumulative standard normal distribution. A performance option is a forward-start option divided by S only when $$r = q$$.

See: Rubinstein, M. (1990), "Pay Now, Choose Later", Risk, 3(2); Haug, E. G. (2007), The Complete Guide to Option Pricing Formulas, 2nd ed., section 4.6.

**Also known as:** forward-start option, delayed option, cliquet option, ratchet option, performance option.

**References:**

- library | Referenced against QuantLib's [AnalyticCliquetEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_analytic_cliquet_engine.html){:target="_blank"} (cliquet)
- library | Referenced against QuantLib's [AnalyticPerformanceEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_analytic_performance_engine.html){:target="_blank"} (performance)
- library | Shares similar logic as QuantLib's [ForwardEuropeanEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_forward_vanilla_engine.html){:target="_blank"} (forward-start)

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>put_option (bool, optional):</u> Whether to calculate the put option price. Defaults to False which means
it will calculate the call option price.
- <u>start_period (float, optional):</u> The share of the life after which the (first) strike is set, at least
0 and below 1. Defaults to 0.5, halfway.
- <u>moneyness (float, optional):</u> The strike as a share of the stock price at each start, above 0. Defaults
to 1, at the money.
- <u>periods (int, optional):</u> The number of equal periods from the start to expiration, 1 for a
forward-start option and more for a cliquet. Defaults to 1.
- <u>performance (bool, optional):</u> Whether each period pays its return beyond the moneyness instead of the
price difference. Defaults to False.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 days after the start date, so at least 2. Defaults to 30, which gives
expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None, which
uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Forward-start option values containing the tickers as the index and the time to expiration
as the columns.

**Raises:**

InvalidArgumentError: If start_period is not at least 0 and below 1, moneyness is not positive or periods is not
a positive whole number.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NVDA", "AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

forward_start_option = toolkit.options.get_forward_start_option(
    expiration_time_range=91
)

forward_start_option[["2026-01-30", "2026-03-01", "2026-03-31"]]
```

Which returns:

| Ticker   |   2026-01-30 |   2026-03-01 |   2026-03-31 |
|:---------|-------------:|-------------:|-------------:|
| NVDA     |       7.6351 |      10.8773 |      13.393  |
| AAPL     |       7.3395 |      10.4915 |      12.9514 |
| MSFT     |       9.834  |      14.0922 |      17.4287 |

---

## get_strategy_payoff
Calculate the net expiration profit and loss (P&L) profile of a multi-leg option (and, optionally, stock) strategy: what the combined position earns or loses at expiration across a range of stock prices.

A strategy is expressed as a list of "legs". Each leg is a dictionary describing either an option position or a stock position:

- For an option leg: "instrument": "option" (default), "strike_price" (float, required), "put_option" (bool, defaults to False), "position" ("long" or "short", defaults to "long"), "premium" (float, defaults to 0).
- For a stock leg: "instrument": "stock", "position" ("long" or "short", defaults to "long"), "premium" (float, the entry price, defaults to 0).

This single, generic building block can express many common strategies by combining legs, for example:

- Straddle: long call + long put, same strike.
- Strangle: long call + long put, different (OTM) strikes.
- Bull call spread: long call (lower strike) + short call (higher strike).
- Bear put spread: long put (higher strike) + short put (lower strike).
- Covered call: long stock + short call.
- Protective put: long stock + long put.
- Iron condor: short put + long put (lower strikes) + short call + long call (higher strikes).

The formula is as follows, for each stock price at expiration S(T) and one unit per leg:

$$
\text{Call Leg Value} = \max(S(T) - K,\; 0)
$$

$$
\text{Put Leg Value} = \max(K - S(T),\; 0)
$$

$$
\text{Stock Leg Value} = S(T)
$$

$$
\text{Leg P\&L} = \text{Leg Value} - \text{Premium for a long leg},\;\; \text{Premium} - \text{Leg Value for a short leg}
$$

$$
\text{Strategy P\&L} = \sum(\text{Leg P\&L}) \;\text{over all legs}
$$

Where K is the leg's strike price and the premium is the price paid (long) or received (short) for the leg, or the entry price of a stock leg. The P&L is not discounted.

**Also known as:** option strategy payoff diagram, P&L profile.

**Args:**

- <u>legs (list[dict] &#124; None, optional):</u> A list of leg dictionaries as described above. Must
contain at least one leg. The same legs are applied to every ticker, so
strike prices should be chosen with the relevant tickers' price levels in
mind. Defaults to None, which buys an at-the-money straddle on each ticker: a
call and a put with the stock price on the start date as strike and 30 days to
expiration, priced with the Black Scholes model on the volatility, risk free rate
and dividend yield of that date, as `get_black_scholes_model` does.
- <u>start_date (str &#124; None, optional):</u> The date whose price, volatility and rates the values
start from; a date without prices (a weekend or a holiday) uses the last trading day before it, and a
ticker without a price on that day is left out with a warning. Defaults to None, which uses the
last date of the historical data.
- <u>stock_price_range (float):</u> The percentage range to use for the stock prices at expiration. Defaults
to 0.5 which equals 50% and thus results in stock prices from 50 to 150 if the current stock price is
100.
- <u>stock_price_step_size (int):</u> The step size to use for the stock prices at expiration. Defaults to 1.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The strategy's net P&L with the range of stock prices at expiration as the index and the
tickers as the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.options.get_strategy_payoff(stock_price_range=0.25, stock_price_step_size=5)
```

Which returns:

|   Stock Price |     TSLA |
|--------------:|---------:|
|           335 |  49.7822 |
|           340 |  44.7822 |
|           345 |  39.7822 |
|           350 |  34.7822 |
|           355 |  29.7822 |
|           360 |  24.7822 |
|           365 |  19.7822 |
|           370 |  14.7822 |
|           375 |   9.7822 |
|           380 |   4.7822 |
|           385 |  -0.2178 |
|           390 |  -5.2178 |
|           395 | -10.2178 |
|           400 | -15.2178 |
|           405 | -20.2178 |
|           410 | -25.2178 |
|           415 | -30.2178 |
|           420 | -35.2178 |
|           425 | -40.2178 |
|           430 | -45.2178 |
|           435 | -50.2178 |
|           440 | -55.2178 |
|           445 | -60.2178 |
|           450 | -64.6578 |
|           455 | -59.6578 |
|           460 | -54.6578 |
|           465 | -49.6578 |
|           470 | -44.6578 |
|           475 | -39.6578 |
|           480 | -34.6578 |
|           485 | -29.6578 |
|           490 | -24.6578 |
|           495 | -19.6578 |
|           500 | -14.6578 |
|           505 |  -9.6578 |
|           510 |  -4.6578 |
|           515 |   0.3422 |
|           520 |   5.3422 |
|           525 |  10.3422 |
|           530 |  15.3422 |
|           535 |  20.3422 |
|           540 |  25.3422 |
|           545 |  30.3422 |
|           550 |  35.3422 |
|           555 |  40.3422 |

---

## get_implied_volatility
Calculate the Implied Volatility (IV): the volatility at which the Black Scholes Model (or the American price) reproduces the actual option prices, for any of the available expiration dates.

Implied Volatility (IV) is a measure of how much the market expects the price of the underlying asset to fluctuate in the future. It is a key component of options pricing and can also be used to calculate the theoretical value of an option.

The price of the underlying quoted with the option chain and the most recent risk free rate and dividend yield are used, and the implied volatility is the volatility at which the Black Scholes price equals the option's mid price, the middle of its bid and ask (the last traded price when the option has no two-sided quote, for example outside market hours). A strike without a two-sided quote and without open interest or volume has no implied volatility: its last trade can be weeks old, from when the underlying stood elsewhere.

The formulas are as follows:

$$
d_{1} = \frac{\ln\left(\frac{S}{K}\right) + \left(r - q + \frac{\sigma^{2}}{2}\right) \cdot t}{\sigma \cdot \sqrt{t}}
$$

$$
d_{2} = d_{1} - \sigma \cdot \sqrt{t}
$$

$$
\text{Call Option Price} = S \cdot e^{- q \cdot t} \cdot N(d_{1}) - K \cdot e^{- r \cdot t} \cdot N(d_{2})
$$

$$
\text{Put Option Price} = K \cdot e^{- r \cdot t} \cdot N(- d_{2}) - S \cdot e^{- q \cdot t} \cdot N(- d_{1})
$$

Where S is the stock price, K is the strike price, r is the risk free rate, q is the dividend yield, $$\sigma$$ is the volatility, t is the time to expiration (the minutes up to 16:00 New York time on the expiration date over the 525,600 minutes of a year, as the Cboe counts it), N(d1) is the cumulative normal distribution of d1 and N(d2) is the the cumulative normal distribution of d2.

In which the Implied Volatility is then calculated as follows:

$$
\text{Implied Volatility} = \text{the}\; \sigma \;\text{for which Black Scholes Theoretical Price}(\sigma) - \text{Actual Option Price} = 0
$$

To determine the Implied Volatility, the Black Scholes Model is used to calculate the theoretical option price in which sigma ($$\sigma$$) is the only unknown variable. Since that price rises strictly with $$\sigma$$, the implied volatility is the root of the difference between the theoretical and actual option price, found with Brent's method on the interval [1e-6, 5]. Prices outside the no-arbitrage bounds have no root and return NaN.

Listed options on single stocks are American and can be exercised before expiration, which the Black Scholes price leaves out. For American options the implied volatility is the $$\sigma$$ at which the American price of the QD+ method (Li, 2010; Andersen, Lake and Offengenden, 2016, see ``get_american_option``) equals the mid price, found with Brent's method on [0.001, 5]. The European volatility attributes the value of exercising early to a higher volatility, so in-the-money puts and calls on stocks with a high dividend yield show a lower American implied volatility; for out-of-the-money options the two hardly differ. Index options such as those on the S&P 500 (^SPX) are European. The prices of QuantLib's QdPlusAmericanEngine invert to the volatility they were priced at.

Mid prices and the underlying price quoted with the chain describe the same moment, unlike last traded prices, which can be hours or days old for illiquid strikes. Deep in-the-money and far out-of-the-money strikes still have wide quotes and can show extreme values (above 100%) that say more about the spread than about the market's view. Practitioners read the smile around the money, where trading is liquid, and use `get_volatility_surface`, which filters outliers and fits a smooth curve, when they need values across all strikes.

The quotes, the underlying price quoted with them and the time to expiration are live, while the risk free rate and the dividend yield come from the last historical date, as does the stock price when a chain quotes no price of the underlying. When that date lies more than five days before today (for example with an end_date in the past), a warning is logged.

**Also known as:** IV, option-implied volatility.

**References:**

- library | Referenced against QuantLib's [QdPlusAmericanEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_qd_plus_american_engine.html){:target="_blank"} (American)

**Args:**

- <u>expiration_date (str &#124; None, optional):</u> The expiration date to use for the calculation. Defaults to None,
which uses the first expiration date at least one calendar day away (an expiry of today has hardly any
time left to price) that every ticker lists, if they share one. A ticker without options expiring on the
date is left out with a warning.
- <u>put_option (bool, optional):</u> Whether to calculate the put option price. Defaults to False which means
it will calculate the call option price.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None, which
uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>american_option (bool, optional):</u> Whether to solve the volatility of the American price (QD+) instead of the
European Black Scholes price. Defaults to False.
- <u>show_expiration_dates (bool, optional):</u> Whether to show the expiration dates: a list for a single ticker
and a list per ticker (a dictionary) for several. Defaults to False.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series &#124; list[str]: Implied Volatility values indexed by ticker and strike price, with the expiration
date as the Series name. If show_expiration_dates is True, it returns the expiration dates.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL"], api_key="FINANCIAL_MODELING_PREP_KEY")

implied_volatility = toolkit.options.get_implied_volatility()

implied_volatility.loc["AAPL"].tail(20)
```

Which returns:

|   Strike Price |   2026-11-18 |
|---------------:|-------------:|
|          347.5 |       0.3258 |
|          352.5 |       0.2814 |
|          357.5 |       0.2722 |
|          362.5 |       0.2576 |
|          367.5 |       0.2675 |
|          372.5 |       0.2898 |
|          377.5 |       0.3803 |

---

## get_volatility_surface
Calibrate an implied volatility surface across multiple expiries: the smooth smile of each expiry that fits the market-implied smile (see `get_implied_volatility`), a raw SVI curve (Gatheral 2004) per expiry, an SSVI surface (Gatheral and Jacquier 2014) across all expiries at once, or a SABR smile (Hagan et al. 2002) per expiry.

A single per-expiry smile only tells you the shape of the market's volatility skew at that one maturity. Stitching several calibrated slices together instead gives a full surface, which is what is needed to price/interpolate options at maturities or strikes that don't trade directly, and to check for term-structure inconsistencies (see Notes).

The formulas are as follows:

$$
\text{SVI:}\;\; w(k) = a + b \cdot (\rho \cdot (k - m) + \sqrt{(k - m)^{2} + \sigma^{2}}),\;\; \text{per expiry}
$$

$$
\text{SSVI:}\;\; w(k,\; \theta_{t}) = \frac{\theta_{t}}{2} \cdot (1 + \rho \cdot \phi(\theta_{t}) \cdot k + \sqrt{(\phi(\theta_{t}) \cdot k + \rho)^{2} + 1 - \rho^{2}})
$$

$$
\text{SSVI curvature:}\;\; \phi(\theta) = \frac{\eta}{\theta^{\gamma} \cdot (1 + \theta)^{1 - \gamma}}
$$

$$
\text{SABR:}\;\; \sigma(K) = \frac{\alpha}{(F \cdot K)^{\frac{1 - \beta}{2}} \cdot D} \cdot \frac{z}{x(z)} \cdot (1 + I \cdot T),\;\; \text{per expiry}
$$

Where w is the total implied variance (implied volatility squared times the time to expiration t), k the log-moneyness ln(K / F) with K the strike and F the forward price, $$\theta_{t}$$ the at-the-money total variance of the expiry and D, z, x(z) and I the terms of Hagan et al. (see `sabr_model.get_sabr_volatility`). The implied volatility is sqrt(w(k) / t) for SVI and SSVI.

- SVI fits five parameters per expiry and follows each smile closely, but a slice can carry butterfly arbitrage and two slices can cross. The fit keeps the total variance non-negative through Gatheral's condition $$a + b \cdot \sigma \cdot \sqrt{1 - \rho^{2}} \geq 0$$.
- SSVI takes $$\theta_{t}$$ from each expiry's at-the-money total variance and fits three parameters, $$\rho$$, $$\eta$$ and $$\gamma$$, to all expiries together with $$\eta \cdot (1 + \vert \rho \vert) \leq 2$$ and $$0 < \gamma \leq \tfrac{1}{2}$$, which keeps every slice free of butterfly arbitrage and the surface free of calendar-spread arbitrage when $$\theta_{t}$$ rises with the expiry. It follows each smile less closely than SVI.
- SABR fits $$\rho$$ and $$\nu$$ per expiry with $$\beta$$ fixed and $$\alpha$$ set by the at-the-money volatility (West 2005), the smile model of the rates market and a common alternative for equities.

Before fitting, strikes whose market-implied volatility is a statistical outlier relative to its neighbors (a common symptom of a stale or wide-bid/ask illiquid quote) are dropped via a median-absolute-deviation filter, since a single bad quote can otherwise dominate the least-squares fit for that whole expiry. Every fit is bounded and runs from a fixed grid of starting points, so the same quotes always give the same surface.

The option chains, the price of the underlying quoted with them and the time to expiration (to 16:00 New York time on the expiration date) are live, while the risk free rate and the dividend yield come from the last historical date; a warning is logged when that date lies more than five days before today. The forward price is $$F = S \cdot e^{(r - q) \cdot t}$$ with the continuously compounded rate r and yield q.

See: Gatheral, J. (2004), "A parsimonious arbitrage-free implied volatility parameterization with application to the valuation of volatility derivatives"; Gatheral, J., & Jacquier, A. (2014), "Arbitrage-free SVI volatility surfaces", Quantitative Finance, 14(1), 59-71; Hagan, P. S., Kumar, D., Lesniewski, A. S., & Woodward, D. E. (2002), "Managing smile risk", Wilmott Magazine; West, G. (2005), "Calibration of the SABR model in illiquid markets", Applied Mathematical Finance.

**Also known as:** SVI surface, SSVI surface, SABR smile, implied volatility surface.

Notes: For SVI and SSVI a warning is logged (not raised) if the fitted surface has calendar-spread arbitrage, total implied variance decreasing with time to expiration at some log-moneyness, or butterfly arbitrage, $$g (k) < 0$$ for some slice (see `svi_model.check_butterfly_arbitrage`). These reflect inconsistent market quotes or a slice SVI cannot fit without arbitrage, and are only checked, not corrected; SSVI avoids the butterfly arbitrage by construction.

**References:**

- library | Referenced against QuantLib's [sabrVolatility](https://github.com/lballabio/QuantLib/blob/v1.44/ql/termstructures/volatility/sabr.cpp#L163){:target="_blank"} (SABR)
- library | Referenced against FinancePy's [volatility_fns.g](https://github.com/domokane/FinancePy/blob/V1.1.2/financepy/models/volatility_fns.py#L247){:target="_blank"} (butterfly arbitrage)
- library | Shares similar logic as QuantLib's [SABRInterpolation](https://www.quantlib.org/reference/class_quant_lib_1_1_s_a_b_r_interpolation.html){:target="_blank"} (SABR)
- library | Shares similar logic as FinancePy's [SABR](https://github.com/domokane/FinancePy/blob/V1.1.2/financepy/models/sabr.py#L157){:target="_blank"} (SABR)
- library | Shares similar logic as rateslib's [IRSabrSmile](https://rateslib.com/py/en/2.7.x/api/rateslib.volatility.IRSabrSmile.html){:target="_blank"} (SABR)
- library | Shares similar logic as FinancePy's [volatility_fns.ssvi](https://github.com/domokane/FinancePy/blob/V1.1.2/financepy/models/volatility_fns.py#L148){:target="_blank"} (SSVI)

**Args:**

- <u>expiration_dates (list[str] &#124; None, optional):</u> The expiration dates to
fit the surface over. Defaults to None, meaning the first
`number_of_expirations` expiration dates at least one calendar day away
(those every ticker lists, if they share any).
- <u>put_option (bool, optional):</u> Whether to use put options instead of call
options. Defaults to False.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded
rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the
calculation. Defaults to None, which uses the dividend yield on the
pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>number_of_expirations (int, optional):</u> The number of near-term
expiration dates to fit when `expiration_dates` is not given.
Defaults to 6.
- <u>outlier_threshold (float, optional):</u> The number of median absolute
deviations from the median implied volatility beyond which a quote
is treated as an outlier and dropped before fitting. Defaults to
5.0.
- <u>method (str, optional):</u> The smile model. Options are: "svi" (raw SVI per expiry), "ssvi"
(SSVI across the expiries), "sabr" (SABR per expiry). Defaults to "svi".
- <u>sabr_beta (float, optional):</u> The SABR elasticity $$\beta$$ between 0 and 1, only used
for the SABR method: 1 is a lognormal backbone, the usual choice for equities.
Defaults to 1.0.
- <u>show_parameters (bool, optional):</u> Whether to return the fitted parameters per
ticker and expiration date instead of the surface. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The fitted implied volatility, indexed by (ticker, strike price),
with one column per expiration date, NaN where a given strike wasn't part of
that expiry's calibration. With show_parameters, the time to expiration (in
years), the forward price and the fitted parameters (a, b, rho, m and sigma for
SVI; theta, rho, eta and gamma for SSVI; alpha, beta, rho and nu for SABR),
indexed by (ticker, expiration date).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["JPM"], api_key="FINANCIAL_MODELING_PREP_KEY")

volatility_surface = toolkit.options.get_volatility_surface(number_of_expirations=4)

volatility_surface.loc["JPM"]
```

Which returns:

|   Strike Price |   2026-11-27 |   2026-12-04 |   2026-12-11 |   2026-12-18 |
|---------------:|-------------:|-------------:|-------------:|-------------:|
|          160   |     nan      |     nan      |     nan      |       1.7956 |
|          190   |     nan      |     nan      |     nan      |       1.5848 |
|          210   |     nan      |     nan      |     nan      |       1.448  |
|          220   |     nan      |     nan      |     nan      |       1.3798 |
|          235   |     nan      |     nan      |     nan      |       1.2768 |
|          240   |     nan      |     nan      |     nan      |       1.2422 |
|          245   |     nan      |     nan      |     nan      |       1.2073 |
|          250   |     nan      |     nan      |     nan      |       1.1721 |
|          255   |     nan      |     nan      |     nan      |       1.1365 |
|          260   |     nan      |     nan      |     nan      |       1.1005 |
|          265   |       0.9504 |     nan      |     nan      |     nan      |
|          270   |     nan      |     nan      |     nan      |       1.0269 |
|          275   |     nan      |     nan      |     nan      |       0.9892 |
|          280   |     nan      |     nan      |     nan      |       0.9507 |
|          285   |       0.8015 |     nan      |     nan      |       0.9113 |
|          287.5 |       0.7829 |     nan      |     nan      |     nan      |
|          290   |       0.7643 |     nan      |     nan      |       0.8708 |
|          292.5 |       0.7459 |     nan      |     nan      |     nan      |
|          295   |       0.7274 |     nan      |     nan      |       0.8291 |
|          297.5 |       0.7091 |     nan      |     nan      |     nan      |
|          300   |       0.6909 |     nan      |     nan      |       0.786  |
|          302.5 |     nan      |       0.4209 |     nan      |     nan      |
|          305   |       0.6549 |       0.4109 |     nan      |       0.7411 |
|          307.5 |       0.6372 |     nan      |     nan      |     nan      |
|          310   |       0.6198 |       0.3907 |       0.3787 |       0.6941 |
|          312.5 |       0.6027 |       0.3804 |     nan      |     nan      |
|          315   |       0.5859 |       0.3701 |       0.3506 |       0.6445 |
|          317.5 |       0.5697 |       0.3598 |     nan      |     nan      |
|          320   |       0.5539 |       0.3494 |       0.3262 |       0.5917 |
|          322.5 |       0.5388 |       0.3391 |     nan      |     nan      |
|          325   |       0.5245 |       0.3291 |       0.3061 |       0.5346 |
|          327.5 |       0.5111 |       0.3194 |     nan      |     nan      |
|          330   |       0.4987 |       0.3104 |       0.2908 |       0.4717 |
|          332.5 |       0.4876 |       0.3025 |     nan      |     nan      |
|          335   |       0.4778 |       0.2966 |       0.2806 |       0.4002 |
|          337.5 |       0.4697 |     nan      |     nan      |     nan      |
|          340   |       0.4634 |       0.2938 |       0.2758 |       0.3143 |
|          342.5 |       0.4592 |       0.2983 |     nan      |     nan      |
|          345   |       0.4573 |       0.3062 |       0.2762 |       0.1955 |
|          347.5 |       0.4579 |       0.3166 |     nan      |     nan      |
|          350   |       0.4613 |       0.3285 |       0.2816 |       0.1748 |
|          352.5 |       0.4676 |     nan      |     nan      |     nan      |
|          355   |       0.477  |       0.3543 |       0.2913 |       0.2102 |
|          357.5 |       0.4897 |     nan      |     nan      |     nan      |
|          360   |       0.5056 |       0.3802 |       0.3047 |       0.2399 |
|          362.5 |       0.5251 |     nan      |     nan      |     nan      |
|          365   |       0.548  |       0.4052 |       0.321  |       0.2661 |
|          367.5 |       0.5745 |       0.4173 |     nan      |     nan      |
|          370   |       0.6047 |       0.429  |       0.3397 |       0.2895 |
|          375   |       0.6765 |       0.4516 |       0.3601 |       0.311  |
|          380   |       0.7646 |       0.4731 |       0.3819 |       0.3308 |
|          385   |       0.8712 |     nan      |       0.4046 |       0.3492 |
|          390   |       0.9999 |     nan      |     nan      |       0.3665 |
|          395   |       1.1562 |     nan      |     nan      |       0.3828 |
|          400   |     nan      |       0.5492 |     nan      |       0.3982 |
|          405   |     nan      |     nan      |     nan      |       0.4129 |
|          410   |     nan      |     nan      |     nan      |       0.4269 |
|          415   |     nan      |     nan      |     nan      |       0.4403 |
|          420   |     nan      |     nan      |     nan      |       0.4532 |
|          425   |     nan      |     nan      |     nan      |       0.4655 |
|          430   |     nan      |     nan      |     nan      |       0.4774 |
|          435   |     nan      |     nan      |     nan      |       0.4889 |
|          440   |     nan      |     nan      |     nan      |       0.4999 |
|          445   |     nan      |     nan      |     nan      |       0.5107 |
|          450   |     nan      |     nan      |     nan      |       0.521  |
|          455   |     nan      |     nan      |     nan      |       0.5311 |
|          460   |     nan      |     nan      |     nan      |       0.5409 |
|          465   |     nan      |     nan      |     nan      |       0.5504 |
|          470   |     nan      |     nan      |     nan      |       0.5596 |
|          480   |     nan      |     nan      |     nan      |       0.5774 |
|          490   |     nan      |     nan      |     nan      |       0.5942 |

---

## get_local_volatility_surface
Calculate the Dupire (1994) local volatility surface: the volatility of the stock at each price and time that reproduces the SVI or SSVI implied volatility surface fitted to the option chains (see `get_volatility_surface`).

The local volatility $$\sigma_{\text{loc}} (K , T)$$ is the volatility, as a function of the price of the underlying and the time, of the only diffusion $$dS / S = (r - q) dt + \sigma_{\text{loc}} (S , t) dW$$ that reprices every European option of the surface. Where the implied volatility at a strike is an average of the volatility along the paths to expiration, the local volatility is the instantaneous volatility the market prices for the moment the underlying stands at K at time T. It is the input of local volatility models for pricing path-dependent options consistently with the smile, and it shows the skew more steeply than the implied volatility (about twice as steep near the money).

The formula is as follows:

$$
\sigma_{loc}^{2}(k,\; T) = \frac{\frac{\partial w}{\partial T}}{g(k)}
$$

$$
g(k) = 1 - \frac{k}{w} \cdot \frac{\partial w}{\partial k} + \frac{1}{4} \cdot \left(- \frac{1}{4} - \frac{1}{w} + \frac{k^{2}}{w^{2}}\right) \cdot \left(\frac{\partial w}{\partial k}\right)^{2} + \frac{\frac{1}{2} \cdot \text{∂}^{2} w}{\partial k^{2}}
$$

Where w(k, T) is the total implied variance (implied volatility squared times the time to expiration T) of the fitted surface, $$k = \ln (K / F_{T})$$ the log-moneyness with $$F_{T}$$ the forward price of the expiry. The derivatives in k are analytic per slice and $$\partial w / \partial T$$ is taken at fixed k by finite differences between the expiries (three-point for unequal spacing at the inner expiries, one-sided at the first and the last), so the surface needs at least two expiries. The local volatility exists where $$g (k) > 0$$ (no butterfly arbitrage) and $$\partial w / \partial T \geq 0$$ (no calendar-spread arbitrage) and is NaN elsewhere, which SSVI avoids by construction where the at-the-money variance rises with the expiry.

The strikes are an evenly spaced grid around the price of the underlying quoted with the chains, from (1 - strike_price_range) to (1 + strike_price_range) times it, the same for every expiry. The forward price is $$F_{T} = S \cdot e^{(r - q) \cdot T}$$ with the continuously compounded rate r and yield q.

See: Dupire, B. (1994), "Pricing with a smile", Risk, 7(1), 18-20; Gatheral, J. (2006), "The Volatility Surface: A Practitioner's Guide", Wiley, eq. 1.10; and Gatheral, J., & Jacquier, A. (2014), "Arbitrage-free SVI volatility surfaces", Quantitative Finance, 14(1), 59-71.

**Also known as:** Dupire local volatility, local vol surface.

**References:**

- library | Referenced against QuantLib's [LocalVolSurface](https://www.quantlib.org/reference/class_quant_lib_1_1_local_vol_surface.html){:target="_blank"}
- library | Referenced against FinancePy's [volatility_fns.ssvi_local_varg](https://github.com/domokane/FinancePy/blob/V1.1.2/financepy/models/volatility_fns.py#L318){:target="_blank"}

**Args:**

- <u>expiration_dates (list[str] &#124; None, optional):</u> The expiration dates to build the
surface over, at least two. Defaults to None, meaning the first
`number_of_expirations` expiration dates at least one calendar day away (those
every ticker lists, if they share any).
- <u>put_option (bool, optional):</u> Whether to fit the implied volatility of the put
options instead of the call options. Defaults to False.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded
rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None,
which uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative
to its close, as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>number_of_expirations (int, optional):</u> The number of near-term expiration dates
when `expiration_dates` is not given. Defaults to 6.
- <u>outlier_threshold (float, optional):</u> The number of median absolute deviations
from the median implied volatility beyond which a quote is treated as an
outlier and dropped before fitting. Defaults to 5.0.
- <u>method (str, optional):</u> The implied volatility surface to start from. Options are: "svi"
(raw SVI per expiry), "ssvi" (SSVI across the expiries). Defaults to "svi".
- <u>strike_price_range (float, optional):</u> The range of strikes, as a fraction of the
price of the underlying in each direction. Defaults to 0.25, from 75% to 125%.
- <u>number_of_strikes (int, optional):</u> The number of strikes in the grid. Defaults to
11.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the Toolkit (4 unless set
otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The local volatility, indexed by (ticker, strike price), with one
column per expiration date; NaN where the fitted surface has arbitrage.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["JPM"], api_key="FINANCIAL_MODELING_PREP_KEY")

local_volatility = toolkit.options.get_local_volatility_surface(
    method="ssvi", number_of_expirations=4
)

local_volatility.loc["JPM"]
```

Which returns:

|   Strike Price |   2026-11-27 |   2026-12-04 |   2026-12-11 |   2026-12-18 |
|---------------:|-------------:|-------------:|-------------:|-------------:|
|         232.9  |       1.1416 |       1.182  |       0.9117 |       0.4401 |
|         248.42 |       1.0243 |       1.0581 |       0.8129 |       0.3938 |
|         263.95 |       0.8972 |       0.922  |       0.7033 |       0.3424 |
|         279.48 |       0.7504 |       0.7622 |       0.5753 |       0.2822 |
|         295    |       0.5552 |       0.5563 |       0.421  |       0.2093 |
|         310.53 |       0.2814 |       0.3193 |       0.2673 |       0.1359 |
|         326.06 |       0.3109 |       0.3004 |       0.2297 |       0.1165 |
|         341.58 |       0.4285 |       0.4135 |       0.2958 |       0.1467 |
|         357.11 |       0.5112 |       0.5059 |       0.3678 |       0.1803 |
|         372.64 |       0.5768 |       0.5786 |       0.4277 |       0.2083 |
|         388.16 |       0.6323 |       0.6391 |       0.4775 |       0.2316 |

---

## get_risk_neutral_density
Calculate the market-implied risk-neutral probability density of the underlying's price at expiration: how likely the market prices each price at expiration, via the Breeden-Litzenberger (1978) theorem, applied to a volatility smile calibrated to real market option prices (see `get_implied_volatility`) rather than a single flat assumed volatility.

`get_partial_derivative` computes the same second-derivative relationship but with one flat volatility value applied at every strike -- with a flat volatility input, the second derivative can only ever recover a lognormal density regardless of what the real market smile looks like, which defeats the entire purpose of the theorem. This method instead first calibrates a raw SVI (Gatheral 2004) curve to the actual market smile (see `get_volatility_surface`) and evaluates the density from that.

The formula is as follows:

$$
f(K) = e^{r \cdot t} \cdot \frac{\mathrm{d}^{2} C(K)}{\,\mathrm{d}K^{2}}
$$

Where C(K) is the Black-Scholes call price at strike K, using the SVI-smoothed implied volatility at that strike, r is the risk-free rate and t is the time to expiration. The second derivative is approximated numerically via the three-point central difference $$(C (K - h) - 2 \cdot C (K) + C (K + h)) / h^{2}$$ on a fine, evenly-spaced strike grid with spacing h, since the smile only gives implied volatility at a sparse set of traded strikes. The first and last grid points have no neighbor on one side and are left out.

The option chains, the price of the underlying quoted with them and the time to expiration (to 16:00 New York time on the expiration date) are live, while the risk free rate and the dividend yield come from the last historical date; a warning is logged when that date lies more than five days before today.

See the paper: Breeden, D.T., & Litzenberger, R.H. (1978), "Prices of State-Contingent Claims Implicit in Option Prices", Journal of Business, 51(4), 621-651. [https://www.jstor.org/stable/2352653](https://www.jstor.org/stable/2352653){:target="_blank"}

**Also known as:** Breeden-Litzenberger, implied risk-neutral distribution.

Notes: A warning is logged (not raised) for any ticker whose density goes negative at some strike -- this indicates a butterfly-arbitrage violation (the call price is not convex in the strike) in the underlying market quotes or the SVI fit, which a well-calibrated, liquid smile should not produce.

**Args:**

- <u>expiration_date (str &#124; None, optional):</u> The expiration date to use.
Defaults to None which means it will use the first available
expiration date.
- <u>put_option (bool, optional):</u> Whether to use put options instead of call
options. Defaults to False.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded
rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the
calculation. Defaults to None, which uses the dividend yield on the
pricing date (the dividends of the 365 days up to it relative to its close,
as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>strike_price_range (float, optional):</u> The range of strikes to evaluate
the density over, as a fraction of the forward price in each
direction. Defaults to 0.5, i.e. from 50% to 150% of the forward
price.
- <u>number_of_strikes (int, optional):</u> The number of strikes in the
evaluation grid, at least 3. Defaults to 200.
- <u>outlier_threshold (float, optional):</u> The number of median absolute
deviations from the median implied volatility beyond which a quote
is treated as an outlier and dropped before fitting. Defaults to
5.0.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Raises:**

ValueError: If no implied volatility could be determined for the given
expiration date.

**Returns:**

pd.DataFrame: The risk-neutral probability density, indexed by strike
price, with one column per ticker.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", benchmark_ticker=None)

toolkit.options.get_risk_neutral_density(strike_price_range=0.1, number_of_strikes=81)
```

Which returns:

|   Strike Price |    SPY |
|---------------:|-------:|
|        667.867 | 0      |
|        669.717 | 0      |
|        671.567 | 0      |
|        673.417 | 0      |
|        675.267 | 0      |
|        677.117 | 0.0001 |
|        678.968 | 0.0001 |
|        680.818 | 0.0001 |
|        682.668 | 0.0001 |
|        684.518 | 0.0001 |
|        686.368 | 0.0001 |
|        688.218 | 0.0001 |
|        690.068 | 0.0001 |
|        691.918 | 0.0002 |
|        693.768 | 0.0002 |
|        695.618 | 0.0002 |
|        697.468 | 0.0003 |
|        699.318 | 0.0003 |
|        701.168 | 0.0004 |
|        703.018 | 0.0004 |
|        704.868 | 0.0005 |
|        706.718 | 0.0006 |
|        708.568 | 0.0008 |
|        710.418 | 0.001  |
|        712.268 | 0.0012 |
|        714.118 | 0.0015 |
|        715.968 | 0.002  |
|        717.819 | 0.0025 |
|        719.669 | 0.0033 |
|        721.519 | 0.0043 |
|        723.369 | 0.0056 |
|        725.219 | 0.0075 |
|        727.069 | 0.01   |
|        728.919 | 0.0133 |
|        730.769 | 0.0177 |
|        732.619 | 0.0233 |
|        734.469 | 0.0302 |
|        736.319 | 0.0378 |
|        738.169 | 0.0455 |
|        740.019 | 0.0518 |
|        741.869 | 0.0549 |
|        743.719 | 0.0537 |
|        745.569 | 0.0479 |
|        747.419 | 0.0389 |
|        749.269 | 0.0289 |
|        751.119 | 0.0198 |
|        752.969 | 0.0127 |
|        754.82  | 0.0078 |
|        756.67  | 0.0046 |
|        758.52  | 0.0028 |
|        760.37  | 0.0016 |
|        762.22  | 0.001  |
|        764.07  | 0.0006 |
|        765.92  | 0.0004 |
|        767.77  | 0.0003 |
|        769.62  | 0.0002 |
|        771.47  | 0.0001 |
|        773.32  | 0.0001 |
|        775.17  | 0.0001 |
|        777.02  | 0      |
|        778.87  | 0      |
|        780.72  | 0      |
|        782.57  | 0      |
|        784.42  | 0      |
|        786.27  | 0      |
|        788.12  | 0      |
|        789.97  | 0      |
|        791.82  | 0      |
|        793.671 | 0      |
|        795.521 | 0      |
|        797.371 | 0      |
|        799.221 | 0      |
|        801.071 | 0      |
|        802.921 | 0      |
|        804.771 | 0      |
|        806.621 | 0      |
|        808.471 | 0      |
|        810.321 | 0      |
|        812.171 | 0      |

---

## get_heston_parameters
Calibrate the Heston (1993) stochastic volatility model to each ticker's option chain: the one set of parameters per ticker that reproduces the market's implied volatility across the term structure, from about a month to a year and a half, at once.

In the Heston model the variance of the stock follows a mean-reverting square-root process correlated with the stock, $$dS = (r - q) S dt + \sqrt{v} S$$ dW_1 and $$dv = \kappa (\theta - v) dt + \sigma \sqrt{v}$$ dW_2 with dW_1 dW_2 = $$\rho dt$$. Its five parameters read directly: $$\sqrt{v_{0}}$$ is today's volatility, $$\sqrt{\theta}$$ the volatility the market expects in the long run, $$\kappa$$ how fast it gets there (a half-life of $$\ln (2) / \kappa$$ years), $$\sigma$$ the volatility of the variance (the curvature of the smile) and $$\rho$$ the correlation of the stock with its variance (the skew: negative for equities, whose volatility rises as they fall).

By default the fit uses the listed expiration nearest to each of 1, 2, 3, 6, 9, 12 and 18 months (expiration_months), leaving out those less than 14 calendar days away, so that $$\kappa$$ and $$\theta$$, which describe how the variance moves across the term structure, are pinned down by expirations far apart. Each expiration contributes its out-of-the-money quotes: the puts below the forward price and the calls above it. Those are the liquid side of the chain; an in-the-money option is mostly its exercise value, so its implied volatility is dominated by the bid-ask spread. The implied volatility of each side (see `get_implied_volatility`) is cleaned of outliers with the same median-absolute-deviation filter as `get_volatility_surface`.

The parameters minimize the vega-weighted price errors, to first order the errors in implied volatility, with a soft-l1 loss so that a few stale quotes cannot dominate. Quotes whose vega is below 5% of the at-the-money vega of their expiration are left out. The fit is a bounded least squares from two fixed starting points (see `heston_model.get_heston_parameters`), with every expiration priced by the COS method of Fang and Oosterlee (2008) with as many terms as the fitted parameters need, so the same quotes always give the same parameters.

The formulas are as follows:

$$
\phi(u) = \exp(C + D \cdot v_{0}),\;\; \text{the characteristic function of} \;\ln\left(\frac{S_{T}}{F}\right) \;\text{in the form of Albrecher et}\; \text{al.} \;(2007)
$$

$$
\text{Call} = S \cdot e^{- qT} - \frac{\frac{\sqrt{F \cdot K} \cdot e^{- rT}}{\pi} \cdot \text{∫}_{0}^{\infty} \;\text{Re}\left[e^{\text{iu} \cdot \ln\left(\frac{F}{K}\right)} \cdot \phi\left(u - \frac{i}{2}\right)\right]}{\left(u^{2} + \frac{1}{4}\right) \,\mathrm{d}u}
$$

$$
\text{minimize}\; \Sigma_{i} \text{soft-l1}\left(\frac{\text{Call}_{\text{Heston}}(K_{i},\; T_{i}) - \text{Call}_{\text{BS}}(K_{i},\; T_{i},\; \sigma_{i})}{\text{Vega}_{\text{BS}}(K_{i},\; T_{i},\; \sigma_{i})}\right)
$$

$$
\text{Feller Ratio} = \frac{2 \kappa \theta}{\sigma^{2}}
$$

Where S is the price of the underlying quoted with the nearest chain, K the strike, F the forward price, r the continuously compounded risk-free rate, q the continuous dividend yield, T the time to expiration in years (to 16:00 New York time on the expiration date) and $$\sigma_{i}$$ the market implied volatility of quote i (a put and a call of the same strike have the same implied volatility error, as both models satisfy put-call parity). A Feller ratio of 1 or more keeps the variance above zero. It is reported rather than imposed: fits to equity smiles commonly break it, because the steep skew asks for a high $$\sigma$$.

The RMSE is the root mean squared difference between the implied volatility of the fitted Heston prices, from a COS series converged to 1e-10 per unit of the strike, and the market's, over the quotes fitted.

See: Heston, S. L. (1993), "A Closed-Form Solution for Options with Stochastic Volatility with Applications to Bond and Currency Options", The Review of Financial Studies, 6(2), 327-343; Albrecher, H., Mayer, P., Schoutens, W. and Tistaert, J. (2007), "The Little Heston Trap", Wilmott Magazine; Fang, F. and Oosterlee, C. W. (2008), "A Novel Pricing Method for European Options Based on Fourier-Cosine Series Expansions", SIAM Journal on Scientific Computing, 31(2), 826-848.

**Also known as:** Heston calibration, stochastic volatility calibration, Heston model fit.

Notes: Heston is calibrated across the term structure because its parameters describe it: with one expiration, or several within a few weeks, $$\kappa$$ and $$\theta$$ are hardly identified separately and $$\kappa$$ and $$\sigma$$ run to their bounds. The expirations under 14 days are left out by default: their smiles are dominated by jump risk (earnings and other events) and by the bid-ask spread, which a diffusion like Heston cannot produce without an implausibly fast mean reversion and volatile variance. The At Bound column names the parameters that end at a bound of the search (v0 and $$\theta$$ from 0.0001 to 4, $$\kappa$$ from 0.001 to 20, a half-life of under two weeks at 20, $$\sigma$$ from 0.01 to 5 and $$\rho$$ from -0.999 to 0.999), and a warning is logged with it. A parameter at its bound is a sign that the quotes ask for more than the model has, such as jumps or a humped term structure, and the other parameters then compensate for it, so they are less meaningful. Even within the bounds $$\kappa$$ and $$\sigma$$ trade off: a faster mean reversion with a more volatile variance gives much the same smile, so on a real surface the fit is flat along that direction and two similar smiles can give a quite different $$\kappa$$. The long-run level $$\theta$$, the Feller ratio and the at-the-money term structure are far better determined than $$\kappa$$ and $$\sigma$$ separately. Listed options on single stocks are American; the fit treats their implied volatility as European, as `get_volatility_surface` does. The Heston prices themselves are available as `heston_model.get_heston_price`.

**References:**

- library | Referenced against QuantLib's [HestonModelHelper](https://www.quantlib.org/reference/class_quant_lib_1_1_heston_model_helper.html){:target="_blank"}
- library | Referenced against QuantLib's [AnalyticHestonEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_analytic_heston_engine.html){:target="_blank"}
- library | Shares similar logic as QuantLib's [COSHestonEngine](https://www.quantlib.org/reference/class_quant_lib_1_1_c_o_s_heston_engine.html){:target="_blank"}

**Args:**

- <u>expiration_dates (list[str] &#124; None, optional):</u> The expiration dates to fit over, used
as given (also those under 14 days). Defaults to None, which picks them with
expiration_months.
- <u>expiration_months (list[float] &#124; None, optional):</u> The times to expiration, in months,
whose nearest listed expiration (at least 14 days away, among each ticker's own
dates) is fitted; an expiration nearest to several of them is fitted once. Defaults to None, which uses 1, 2, 3, 6, 9, 12 and 18 months.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the calculation. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded
rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None, which
uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to its
close, as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>outlier_threshold (float, optional):</u> The number of median absolute deviations from the
median implied volatility of an expiration beyond which a quote is dropped before
fitting. Defaults to 5.0.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker, v0, kappa, theta, sigma and rho, the Feller Ratio, the RMSE
in implied volatility, the number of quotes and the number of expirations fitted, and
At Bound, the parameters that end at a bound of the search (empty when none does).

**Raises:**

ValueError: If no ticker lists an expiration 14 days or more away.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "MSFT"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.options.get_heston_parameters()
```

Which returns:

| Ticker   |     v0 |   kappa |   theta |   sigma |     rho |   Feller Ratio |   RMSE |   Quotes |   Expirations | At Bound   |
|:---------|-------:|--------:|--------:|--------:|--------:|---------------:|-------:|---------:|--------------:|:-----------|
| AAPL     | 0.0611 |  6.2395 |  0.0974 |  1.5007 | -0.5683 |         0.5398 | 0.0196 |      364 |             7 |            |
| MSFT     | 0.1404 | 11.815  |  0.1373 |  2.5277 | -0.5619 |         0.5077 | 0.0277 |      375 |             7 |            |

---

## get_heston_nandi_model
Calculate European option prices in the GARCH model of Heston and Nandi (2000): what calls and puts on each ticker are worth when its variance follows a GARCH process with a leverage effect, with the GARCH parameters fitted on each ticker's own daily returns.

Where the Black-Scholes model takes one volatility for the whole life of the option, the Heston-Nandi model lets the daily variance follow a GARCH(1, 1) process with a leverage effect: it starts from the variance the GARCH filter forecasts for tomorrow, reverts to its long-run level at the speed the returns show, and rises more after a fall than after a rise. The prices therefore follow the current volatility regime of the stock and carry a skew, without any option prices as input. It is the GARCH option pricing model with a closed form.

The parameters are fitted by maximum likelihood on the daily log returns (from the Adj Close) over the risk-free rate of the historical data up to the pricing date (see `garch_option_model.get_heston_nandi_parameters`), so a past pricing date only uses what was known then. Under the risk-neutral measure the price of risk $$\lambda$$ becomes -½ and the asymmetry $$\gamma$$ becomes $$\gamma + \lambda$$ + ½, and the price follows from the moment generating function of the log price by Fourier inversion.

The formulas are as follows:

$$
R_{t} - \frac{r_{t}}{252} = \lambda \cdot h_{t} + \sqrt{h} \;\text{}_{t} \cdot z_{t}
$$

$$
h_{t+1} = \omega + \beta \cdot h_{t} + \alpha \cdot (z_{t} - \gamma \cdot \sqrt{h} \;\text{}_{t})^{2}
$$

$$
E\left[S_{T}^{\phi}\right] = S^{\phi} \cdot \exp(A + B \cdot h),\;\; \text{with A and } B \text{ from a backward recursion over the trading days}
$$

$$
\text{Call} = S \cdot e^{- qT} - \frac{\frac{\sqrt{F \cdot K} \cdot e^{- rT}}{\pi} \cdot \text{∫}_{0}^{\infty} \;\text{Re}\left[e^{\text{iu} \cdot \ln\left(\frac{F}{K}\right)} \cdot \phi_{X}\left(u - \frac{i}{2}\right)\right]}{\left(u^{2} + \frac{1}{4}\right) \,\mathrm{d}u}
$$

Where $$R_{t}$$ is the daily log return, $$r_{t}$$ the risk-free rate of that day, $$h_{t}$$ the conditional variance, $$z_{t}$$ the standard normal shock, $$\omega$$, $$\alpha$$, $$\beta$$, $$\gamma$$ and $$\lambda$$ the fitted parameters, S the traded close on the pricing date, K the strike, h the variance forecast for the next trading day, r the continuously compounded risk-free rate, q the continuous dividend yield (ln(1 + dividend yield)), T the number of trading days to expiration over 252 and $$\phi_{X}$$ the characteristic function of $$\ln (S_{T} / F)$$ with F the forward price. The trading days to an expiration are the weekdays after the pricing date up to and including it, so an expiration on a weekend has the value of the Friday before it and one on the next weekday is one GARCH step away. The prices are computed with the COS method of Fang and Oosterlee (2008), which agrees with the Fourier integral within 1e-10 here and prices all strikes of an expiration at once.

See: Heston, S. L. and Nandi, S. (2000), "A Closed-Form GARCH Option Valuation Model", The Review of Financial Studies, 13(3), 585-625. Checked against a Monte Carlo simulation of the risk-neutral process and the Black-Scholes price at $$\alpha = \beta = 0$$.

**Also known as:** Heston-Nandi model, GARCH option pricing, HN-GARCH.

**Args:**

- <u>start_date (str &#124; None, optional):</u> The date whose price, rates and fitted variance the
values start from; the GARCH parameters are fitted on the returns up to it. A date
without prices (a weekend or a holiday) uses the last trading day before it. Defaults
to None, which uses the last date of the historical data.
- <u>put_option (bool, optional):</u> Whether to calculate the put option price. Defaults to False which means
it will calculate the call option price.
- <u>strike_price_range (float):</u> The percentage range to use for the strike prices, between 0 and 1. Defaults to 0.25 which
equals 25% and thus results in strike prices from 75 to 125 if the current stock price is 100.
- <u>strike_step_size (float):</u> The step size to use for the strike prices, above 0. Defaults to 5 which means that
the strike prices will be 75, 80, 85, ..., 120 and 125 if the current stock price is 100.
- <u>expiration_time_range (int):</u> The number of days to use for the time to expiration: the columns are the
expirations 1 up to expiration_time_range - 1 calendar days after the start date, so at least 2. Defaults to 30,
which gives expirations of 1 to 29 days.
- <u>risk_free_rate (float, optional):</u> The risk free rate to use for the pricing. Defaults to None, which
uses the Toolkit's risk-free rate on the pricing date: the 10-year Treasury yield unless the Toolkit's
risk_free_rate parameter selects '13w', '5y' or '30y', converted from its semi-annual bond-equivalent
quote to continuous compounding. A rate passed here is used as given, as a continuously compounded
rate. The excess returns of the fit always use the Toolkit's daily rate.
- <u>dividend_yield (float, optional):</u> The dividend yield to use for the calculation. Defaults to None,
which uses the dividend yield on the pricing date (the dividends of the 365 days up to it relative to
its close, as the continuously compounded ln(1 + q)). A given value is used as a continuous yield.
- <u>show_parameters (bool, optional):</u> Whether to return the fitted GARCH parameters per ticker instead of
the prices: omega, alpha, beta, gamma and lambda (daily), the persistence $$\beta + \alpha \gamma^{2}$$, the annualized
long-run and next-day volatility (√(252 * variance)) and the log-likelihood. Defaults to False.
- <u>show_input_info (bool, optional):</u> Whether to show the input information. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None,
which uses the rounding of the Toolkit (4 unless set otherwise).
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result across the
time to expiration columns for each ticker and strike price. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Heston-Nandi option values with the tickers and strike prices as the index and the
expiration dates as the columns, or with show_parameters the fitted parameters per ticker.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2016-01-01",
    end_date="2025-12-31",
)

heston_nandi_put = toolkit.options.get_heston_nandi_model(
    put_option=True, strike_price_range=0.15, strike_step_size=10, expiration_time_range=91
)

heston_nandi_put.loc["AAPL", ["2026-01-30", "2026-03-01", "2026-03-31"]]
```

Which returns:

|   Strike Price |   2026-01-30 |   2026-03-01 |   2026-03-31 |
|---------------:|-------------:|-------------:|-------------:|
|            230 |       0.3272 |       1.3428 |       2.6223 |
|            240 |       0.7636 |       2.367  |       4.1069 |
|            250 |       1.6753 |       3.9993 |       6.216  |
|            260 |       3.4452 |       6.477  |       9.1009 |
|            270 |       6.6014 |      10.0485 |      12.8997 |
|            280 |      11.6765 |      14.9192 |      17.7135 |
|            290 |      18.8495 |      21.1766 |      23.5828 |
|            300 |      27.6358 |      28.7298 |      30.4716 |
|            310 |      37.2321 |      37.313  |      38.2669 |
|            320 |      47.1053 |      46.5792 |      46.7986 |

---

