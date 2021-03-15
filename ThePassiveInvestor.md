---
layout: page
title: The Passive Investor
---
**Theories and research about the stock market have stated that the semi-strong form of market efficiency seems to
hold.** This means that all public information is accurately reflected in the price of an financial instrument. This
makes the job of a portfolio manager primarily managing the desired risk appetite of the client and not explicitly
trying to outperform the market. This fact in combination with Finance professionals all around the world looking for
that 'edge' to make their investment decisions as profitable as possible, makes it so the average joe can not compete.

**Therefore, the term 'Passive Investing' is often coined around.** This refers to buying funds
(either ETFs or Mutual Funds) that follow the index (i.e. S&P 500, Dow Jones Index) or a broad market
(Developed Markets, MSCI World) for diversification benefits. This means that a sudden decrease in performance of one
stock within the index does not (on average) lead to a significant decline in the index as a whole. This allows the
holder to spend limited time monitoring his holdings, therefore the term 'Passive'.

With a large increase in ETFs available (over 5,000 in 2020), it can become difficult to make the best choice in what
you wish to invest. There are many different providers (iShares, Vanguard, Invesco) as well as with changes to the
underlying stocks (i.e. High Yield, Super Dividends, Equal Weighted). This is quickly reflected when looking for a S&P
500 ETF as there are over 20 different ETFs available.

With this program, I wish to make investment decisions easier to make and manage.

[![ThePassiveInvestor](https://jerbouma.github.io/public/page_images/programExample.png)](https://jerbouma.github.io/public/page_images/programExample.png)

## Set-Up / Installation

Installing the program and running an analysis:

1. Download the most recent release [here](https://github.com/JerBouma/ThePassiveInvestor/releases).
2. Unpack the ZIP file to your prefered location and run the file "ThePassiveInvestor.exe"
3. Go to the [FinanceDatabase](https://github.com/JerBouma/FinanceDatabase) and search the database for your preferred
   tickers. Then, place the tickers in an Excel sheet with the tickers listed vertically. See the example on the page of
   the FinanceDatabase.
    * You can also use the Yahoo Finance Screener ([ETFs](https://finance.yahoo.com/screener/etf/new)
      or [Mutual Funds](https://finance.yahoo.com/screener/mutualfund/new)), select your preferences and click
      "Find ETFs". Then you can copy the URL.
    * You can also use 'Quote Lookup' ([example](https://finance.yahoo.com/lookup/etf?s=developed%20markets))
    * You can also use your own Excel file that has the tickers listed vertically.
4. Open the program, enter your save location (i.e. C:/Documents/DevelopedMarketsETF.xlsx) and input the URL or
   Excelfile you decided to use in Step 2. Note that you <u>do not</u> have to create an Excel file, the program does
   this for you. However, it does not create folders.
5. Run the program, this takes less than a minute to complete.
6. Analyse the Excelfile created

## Functionality

The program is able to output an overview of each fund on a seperate sheet. In this overview the following data is
shown:

* The title of the fund
* A summary about the fund's purpose/goal
* Sector Holdings (% in each sector)
* Company Holdings (top 10 companies with highest %)
* Risk Statistics (several measures of risk)
    * Displayed in 3, 5 and 10 years
    * Alpha
    * Beta
    * Mean Annual Return
    * R Squared
    * Standard Deviation
    * Sharpe Ratio
    * Treynor Ratio
* Characteristics of the instrument
    * Inception date (start of fund)
    * Category
    * Total assets
    * Currency
    * Net Asset Value
    * Latest close price
* Morningstar Style Box (style of the fund)
* Last five annual returns
* Graph depicting the adjusted close prices over the last 10 years
* Last 10 years of adjusted close prices for all Tickers (hidden sheet)

The input should either be an Excel File (with solely tickers in it) or via Yahoo Finance's ETF or Mutual Fund
Screener (see [here](https://finance.yahoo.com/screener/etf/new)
and [here](https://finance.yahoo.com/screener/mutualfund/new)). Note that the program <i>can not</i>
handle stocks, bonds or anything else that is not a fund. This is because the data used is only available for funds and
equity investing is not considered Passive Investing.

An example of the output can be found in the GIF below. This depicts several ETFs collected
from [the Top ETFs according to Yahoo Finance](https://finance.yahoo.com/etfs).

[![ThePassiveInvestor](https://jerbouma.github.io/public/page_images/outputExample.gif)](https://jerbouma.github.io/public/page_images/outputExample.gif)
