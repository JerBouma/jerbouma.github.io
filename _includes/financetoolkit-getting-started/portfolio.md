## Getting Started

The Portfolio module analyses your own portfolio from a list of transactions: what you bought and sold, when, at what price and at what cost. From that list it builds the positions over time, the return and profit-and-loss of every asset and transaction, and the same transactions made in a benchmark, so you can see whether your decisions beat simply buying the index. The portfolio is also connected to the rest of the Finance Toolkit, which means any of the 500+ ratios, risk and performance metrics and technical indicators can be calculated for the assets you hold and for the portfolio as a whole, weighted by its positions over time.

### The Portfolio Template

The module reads your transactions from an XLSX, XLS or CSV file in a fixed format. The template, which doubles as the example portfolio used in this section, is in the Finance Toolkit repository on GitHub as [example_portfolio.xlsx](https://github.com/JerBouma/FinanceToolkit/blob/main/financetoolkit/portfolio/example_datasets/example_portfolio.xlsx) and [example_portfolio.csv](https://github.com/JerBouma/FinanceToolkit/blob/main/financetoolkit/portfolio/example_datasets/example_portfolio.csv). It has the following columns:

| Column       | What it holds                                                    | Example      |
|:-------------|:-----------------------------------------------------------------|:-------------|
| `Date`       | The date of the transaction                                      | 2021-01-01   |
| `Identifier` | The ticker of the traded asset                                   | AAPL         |
| `Currency`   | The currency of the asset                                        | USD          |
| `Volume`     | The number of shares or contracts, negative for a sale           | 10 or -10    |
| `Price`      | The price per share at the time of the transaction               | 100          |
| `Costs`      | The transaction costs, as a negative number                      | -3           |

The first rows of the example portfolio look like this:

| Date       | Identifier | Currency | Volume | Price | Costs |
|:-----------|:-----------|:---------|-------:|------:|------:|
| 2000-01-07 | ASML       | USD      |   9.00 | 30.82 | -3.00 |
| 2000-01-10 | SKY        | USD      |  12.00 | 15.23 | -2.00 |
| 2000-01-28 | AMZN       | USD      |   8.00 |  3.06 | -3.00 |
| 2000-02-23 | FIX        | USD      |   8.00 |  6.99 |  0.00 |
| 2000-02-28 | MSFT       | USD      |  13.00 | 28.35 |  0.00 |

Replace these rows with your own transactions, keeping the column names and formats as they are. For the `Identifier`, use the ticker as Yahoo Finance writes it (for example `ASML.AS` for ASML on Euronext Amsterdam). Calling `Portfolio` without a `portfolio_dataset` loads the example portfolio and also copies the template into your working directory as `portfolio_template.xlsx` and `portfolio_template.csv`.

To load your own portfolio from the filled-in template, with the S&P 500 as the benchmark:

```python
from financetoolkit import Portfolio

portfolio = Portfolio(
    portfolio_dataset="portfolio_template.xlsx",
    api_key="FINANCIAL_MODELING_PREP_KEY",
    benchmark_ticker="^GSPC",
)
```

### Loading the Example Portfolio

The rest of this section uses the example portfolio: about 300 transactions in 26 stocks and ETFs, from 2000 onwards. To load it:

```python
from financetoolkit import Portfolio

portfolio = Portfolio(example=True, api_key="FINANCIAL_MODELING_PREP_KEY", benchmark_ticker="^GSPC")
```

The historical prices of every asset and of the benchmark are collected on the first call, and the currency of each asset is converted where needed.

### The Portfolio Overview

The portfolio overview aggregates all transactions into one row per asset: the volume held, the costs, the average purchase price, the amount invested, the latest value, the return, the volatility, alpha and beta against the benchmark, and the weight in the portfolio. With `include_portfolio=True` it adds a row for the portfolio as a whole. To get the overview:

```python
portfolio_overview = portfolio.get_portfolio_overview(include_portfolio=True)
```

Which gives the following for the portfolio as a whole, where a return of 6.41 means the portfolio is worth about 7.4 times what was invested:

| Portfolio            |          Value |
|:---------------------|---------------:|
| Invested             |       $139,539 |
| Latest Value         |     $1,023,949 |
| Return               |           6.41 |
| Benchmark Return     |           1.71 |
| Volatility           |         28.7%  |
| Benchmark Volatility |         12.9%  |
| Alpha                |           4.70 |
| Beta                 |           1.39 |

The benchmark return is what the same amounts, invested on the same dates in the S&P 500, would have returned, so the alpha of 4.70 is the outperformance of the stock picks over the index. It came with a beta of about 1.4 and more than twice the volatility of the index. The same overview per asset also holds the `Return Value`, the profit in dollars of each position, which ranks the positions as follows:

{% include ft-chart.html id="portfolio-overview" src="/assets/data/financetoolkit-guides/portfolio.json" label="Profit in dollars of each position in the example portfolio" %}

A handful of positions explain most of the result. ASML, Comfort Systems (`FIX`), Monolithic Power (`MPWR`) and Fair Isaac (`FICO`) made $578,000 of the $894,000 profit, almost two thirds of it. Measured by the return, Comfort Systems, Nvidia, ASML and Fair Isaac all returned more than 18 times the amount invested, but Nvidia's position was too small to matter much in dollars. Netflix (`NFLX`) and Kraft Heinz (`KHC`) are the only two below what was paid for them.

### Positions over Time

Where the portfolio overview gives one row per asset, the positions overview tracks every position day by day: the volume, the costs, the invested amount, the realised proceeds, the current value, the cumulative return and the invested and current weights. To get it and add up the invested amount and the current value of all positions:

```python
import pandas as pd

positions = portfolio.get_positions_overview()

portfolio_value = pd.DataFrame(
    {
        "Invested Amount": positions["Invested Amount"].sum(axis=1),
        "Current Value": positions["Current Value"].sum(axis=1),
    }
)
```

Which gives the following, shown at the end of each month:

{% include ft-chart.html id="portfolio-value" src="/assets/data/financetoolkit-guides/portfolio.json" label="Invested amount and current value of the example portfolio" %}

The value grew away from the amount put in, slowly at first and steeply after 2016, as the winners compounded. The setbacks along the way were deep: the value fell from $16,900 in October 2007 to $8,000 in February 2009, roughly halving, and from $424,000 at the end of 2021 to $281,000 in September 2022, a third lower, even while more money was being added.

### Transactions and Profit and Loss

The transactions overview shows the same information for every single transaction, together with its profit and loss (PnL). The `pnl_method` sets how sales are matched to earlier purchases: `FIFO` (first in, first out, the default), `LIFO` (last in, first out) or `AVERAGE` (average cost). To get the overview with FIFO:

```python
transactions_overview = portfolio.get_transactions_overview(pnl_method="FIFO")
```

Which gives the following for the first five transactions, where the `% Return` is a fraction, so 51.35 means the shares bought are now worth more than 50 times their purchase price:

| Date       | Identifier |  Price | Volume | Costs | Invested Amount | Current Value | % Return |
|:-----------|:-----------|-------:|-------:|------:|----------------:|--------------:|---------:|
| 2000-01-07 | ASML       |  30.82 |      9 |    -3 |          280.39 |     14,677.56 |    51.35 |
| 2000-01-10 | SKY        |  15.23 |     12 |    -2 |          184.79 |        916.32 |     3.96 |
| 2000-01-28 | AMZN       |   3.06 |      8 |    -3 |           27.45 |      2,101.04 |    75.55 |
| 2000-02-23 | FIX        |   6.99 |      8 |     0 |           55.88 |     11,176.72 |   199.00 |
| 2000-02-28 | MSFT       |  28.35 |     13 |     0 |          368.60 |      6,914.31 |    17.76 |

The realised PnL is booked on the sales, and by default the overview leaves out the sales, so the purchases above show no PnL while the cumulative PnL holds the total. To see the profit or loss of every sale:

```python
transactions_overview = portfolio.get_transactions_overview(pnl_method="FIFO", exclude_sold_positions=False)
```

### Performance per Period

Both overviews also exist per period, `yearly`, `quarterly`, `monthly`, `weekly` or `daily`, which shows how the portfolio and each transaction did within each period rather than since the start. The transactions performance adds the benchmark return and the alpha of every transaction in that period. To get the portfolio performance per year, the transactions performance per quarter, and the value of each position and the total invested amount at the end of each year:

```python
portfolio_performance = portfolio.get_portfolio_performance(period="yearly")

transactions_performance = portfolio.get_transactions_performance(period="quarterly")

yearly_value = portfolio_performance["Current Value"].unstack("Identifier")

yearly_invested = portfolio_performance.groupby(level="Date")["Invested Amount"].sum()
```

Which gives the following year-end values for the four largest positions today, with every other position grouped together and the dashed line showing the amount invested:

{% include ft-chart.html id="portfolio-yearly" src="/assets/data/financetoolkit-guides/portfolio.json" label="Year-end value of the four largest positions and the rest of the example portfolio" %}

ASML, Comfort Systems, Monolithic Power and Fair Isaac made up about a quarter of the portfolio in 2000 and 60% of it now. The drawdowns of 2008 and 2022 are clearly visible against a steadily growing invested amount, and in 2022 the four held up better than the rest, rising from 45% to 55% of the portfolio.

### Connecting to the Finance Toolkit

What makes the module powerful is that the portfolio connects directly to the `Toolkit`. The `toolkit` property returns a `Toolkit` with every asset in the portfolio, the benchmark and the portfolio itself as a ticker called `Portfolio`, a weighted average of the positions over time. Assign it to a variable once, so the data is collected only once. To create it:

```python
toolkit = portfolio.toolkit
```

#### Financial Ratios

Any ratio can now be calculated for the holdings and for the portfolio. The example portfolio holds ETFs as well, which have no financial statements, so their ratios stay empty. To calculate the net profit margin:

```python
net_profit_margin = toolkit.ratios.get_net_profit_margin()

net_profit_margin.loc["Portfolio"]
```

Which gives one net profit margin per year for the portfolio, weighted by the positions it held at the time:

{% include ft-chart.html id="portfolio-net-profit-margin" src="/assets/data/financetoolkit-guides/portfolio.json" label="Net profit margin of the example portfolio" %}

The margin rose from between 4% and 17% in the 2000s to between 23% and 30% since 2020, as highly profitable holdings such as ASML grew into a large part of the portfolio. The most recent year, in orange, jumps to 40% because it only holds the companies whose fiscal year has already ended.

#### Risk and Performance against the Benchmark

The risk and performance metrics compare the portfolio to the benchmark again, which shows whether you run a higher or lower risk profile than the index. To calculate the beta and the Value at Risk per year:

```python
beta = toolkit.performance.get_beta(period="yearly")

# The benchmark has a beta of 1 by definition
beta["Benchmark"] = 1

value_at_risk = toolkit.risk.get_value_at_risk(period="yearly", within_period=True)
```

Which gives the following, with the dashed line at the benchmark's beta of 1 and the tabs switching to the Value at Risk:

{% include ft-chart.html id="portfolio-beta-var" src="/assets/data/financetoolkit-guides/portfolio.json" label="Beta and Value at Risk of the example portfolio and the benchmark" %}

The beta was above 1 in 26 of the 27 years, 2002 being the exception, and has risen from about 1.2 in the 2000s to between 1.4 and 1.8 in recent years. The daily Value at Risk is deeper than that of the S&P 500 in every single year, typically about twice as deep, with the worst at -6.6% in 2008 against -4.4% for the index.

#### Technical Indicators

The technical indicators work the same way, for example to see whether the portfolio or its largest positions look overbought or oversold. To calculate the Relative Strength Index and select the portfolio and three of its largest positions over the last year of trading days:

```python
rsi = toolkit.technicals.get_relative_strength_index()

rsi[["Portfolio", "ASML", "FIX", "MPWR"]].iloc[-252:]
```

Which gives the following, one tab per series, with the dashed lines at 70 and 30 marking the levels that are usually read as overbought and oversold:

{% include ft-chart.html id="portfolio-rsi" src="/assets/data/financetoolkit-guides/portfolio.json" label="Relative Strength Index of the example portfolio and three positions" %}

The positions swing much further than the portfolio. Monolithic Power closed above 70 on 23 trading days in the last year, Comfort Systems on 19 and ASML on 15, while the portfolio as a whole stayed between 37 and 67, as the swings of its holdings partly cancel out.

{% include ft-charts-script.html %}
