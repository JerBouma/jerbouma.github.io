## Getting Started

The Finance Toolkit computes 500+ financial ratios, indicators and models from the underlying data with one transparent formula each, so a margin or a Sharpe ratio means the same thing for every company and every period. This section covers the basics: loading a set of companies, retrieving their prices and financial statements, the options that work across nearly every function, and the company data beyond the statements. Each module's own documentation page opens with a Getting Started section of its own.

### Data and API Keys

Most data comes from Financial Modeling Prep, which needs an API key. The free plan allows 250 requests a day, five years of history and companies listed on US exchanges; the paid plans give 30+ years of annual and quarterly statements. You can get a key [through this link](/fmp){:target="_blank"}, which also gives 15% off the paid plans and supports the project. Without a key, or when a request is outside your plan, the Toolkit falls back to Yahoo Finance; set `enforce_source="FinancialModelingPrep"` to switch that off.

### Loading the Toolkit

Everything starts with a `Toolkit` instance for one or more tickers. The data is retrieved once and kept, so every ratio, model and indicator afterwards is computed from the same statements and prices without asking the data provider again. Annual statements are the default; add `quarterly=True` for quarterly statements (a paid Financial Modeling Prep plan).

To load Apple, Microsoft, Alphabet and Amazon from 2005 onwards:

```python
from financetoolkit import Toolkit

API_KEY = "FINANCIAL_MODELING_PREP_KEY"

companies = Toolkit(
    ["AAPL", "MSFT", "GOOGL", "AMZN"], api_key=API_KEY, start_date="2005-01-01"
)
```

Every example below uses this `companies` instance.

### Historical Data

`get_historical_data` returns open, high, low, close, adjusted close, volume, dividends, returns and cumulative returns for every ticker, plus the benchmark (the S&P 500 through SPY by default; change it with `benchmark_ticker`). The period can be `daily` (the default), `weekly`, `monthly`, `quarterly` or `yearly`.

To retrieve daily, yearly and quarterly prices:

```python
# Daily prices for every company and the benchmark
daily = companies.get_historical_data()

# One row per year
yearly = companies.get_historical_data(period="yearly")

# The cumulative return per quarter
cumulative_returns = companies.get_historical_data(period="quarterly")["Cumulative Return"]
```

The columns hold two levels, the field and the ticker, so `daily["Close"]` gives the closing prices of all companies and `daily.xs("AAPL", axis=1, level=1)` everything for Apple. The cumulative returns start at 1, so a value of 10 means the investment grew tenfold:

{% include ft-chart.html id="getting-started-cumulative" src="/assets/data/financetoolkit-guides/getting-started.json" label="Cumulative quarterly returns of Apple, Microsoft, Alphabet, Amazon and the S&P 500 since 2005" %}

When tickers trade on different exchanges or in different currencies, it helps to check what each one is. To see the currency, exchange and listing details of every ticker:

```python
companies.get_historical_statistics()
```

Which shows, among other fields:

|                  | AAPL       | MSFT       | GOOGL      | AMZN       |
|:-----------------|:-----------|:-----------|:-----------|:-----------|
| Currency         | USD        | USD        | USD        | USD        |
| Exchange Name    | NMS        | NMS        | NMS        | NMS        |
| Instrument Type  | EQUITY     | EQUITY     | EQUITY     | EQUITY     |
| First Trade Date | 1980-12-12 | 1986-03-13 | 2004-08-19 | 1997-05-15 |

### Financial Statements

The balance sheet, income statement and cash flow statement come back in one standardized layout for every company: the rows are the ticker and the line item, the columns the fiscal years (or quarters with `quarterly=True`). Because the line items have the same names for every company, comparing Apple's equity with Amazon's is a matter of selecting a row.

To retrieve the three statements:

```python
balance_sheet = companies.get_balance_sheet_statement()
income_statement = companies.get_income_statement()
cash_flow_statement = companies.get_cash_flow_statement()

# The balance sheet of Amazon only
balance_sheet.loc["AMZN"]

# One line item for every company
equity = balance_sheet.xs("Total Shareholder Equity", level=1)
```

The last line selects total shareholder equity for all four companies, which plotted per fiscal year gives:

{% include ft-chart.html id="getting-started-equity" src="/assets/data/financetoolkit-guides/getting-started.json" label="Total shareholder equity of Apple, Microsoft, Alphabet and Amazon per fiscal year" %}

### Growth, Trailing, Rolling and Z-Scores

A handful of parameters work across nearly every function in the Toolkit, from the statements to the ratios, risk and performance metrics.

`growth=True` returns the period-over-period change instead of the value itself. To get the revenue growth of each company:

```python
income_statement_growth = companies.get_income_statement(growth=True)

income_statement_growth.loc[:, "Revenue", :]
```

Which gives the year-over-year revenue growth, one company per tab, from 2008:

{% include ft-chart.html id="getting-started-revenue-growth" src="/assets/data/financetoolkit-guides/getting-started.json" label="Year-over-year revenue growth of Apple, Microsoft, Alphabet and Amazon since 2008" %}

By default growth is measured against the previous period. `lag` changes that, and a list of lags returns each of them side by side, e.g. the growth over one, two and three years. To get the growth of every income statement item over three lags:

```python
companies.get_income_statement(growth=True, lag=[1, 2, 3])
```

Three more parameters turn a single number per period into something more useful:

- **`trailing`** sums or averages a metric over the last N periods. On quarterly data `trailing=4` gives the trailing twelve months (TTM); on annual data, as here, it covers four years.
- **`standardize=True`** converts the values into a Z-Score: the number of standard deviations a value is from that company's own historical mean. It makes metrics on very different scales comparable and shows when a reading is unusual for that company.
- **`rolling`** calculates a metric over a sliding window, which turns a metric into a time series of itself. It is available in the Risk, Performance and Economics modules.

To calculate a trailing net profit margin, a standardized operating margin and a rolling 12-month beta:

```python
# Trailing: the net profit margin over the last four periods
companies.ratios.get_net_profit_margin(trailing=4)

# Standardize: the operating margin as a Z-Score
companies.ratios.get_operating_margin(standardize=True)

# Rolling: the beta against the S&P 500 over the last 12 months
companies.performance.get_beta(period="monthly", rolling=12)
```

The trailing net profit margin, with the latest value per company and its path since 2015:

{% include ft-chart.html id="getting-started-trailing" src="/assets/data/financetoolkit-guides/getting-started.json" label="Trailing four-year net profit margin of Apple, Microsoft, Alphabet and Amazon since 2015" %}

The operating margin as a Z-Score per company and year, blue above the company's own average and pink below:

{% include ft-chart.html id="getting-started-standardized" src="/assets/data/financetoolkit-guides/getting-started.json" label="Operating margin Z-Scores of Apple, Microsoft, Alphabet and Amazon since 2015" %}

The rolling beta of Apple and Alphabet, with the market's beta of 1 dashed:

{% include ft-chart.html id="getting-started-beta" src="/assets/data/financetoolkit-guides/getting-started.json" label="Rolling 12-month beta of Apple and Alphabet against the S&P 500 since 2015" %}

### Analyst Estimates and ESG Scores

Beyond the reported figures, the Toolkit also retrieves the analyst consensus for the coming years: the low, high and average estimates of revenue, EBITDA, EBIT, net income, SG&A and EPS, and the number of analysts behind each. The ESG scores give the environmental, social and governance scores per year, and a combined ESG score.

To retrieve both:

```python
analyst_estimates = companies.get_analyst_estimates()

esg_scores = companies.get_esg_scores()
```

When plotted, the earnings per share estimates for the years that at least five analysts cover, with the average as a line and the range from the lowest to the highest estimate shaded:

{% include ft-chart.html id="getting-started-estimates" src="/assets/data/financetoolkit-guides/getting-started.json" label="Average, low and high analyst estimates of earnings per share for Apple, Microsoft, Alphabet and Amazon" %}

The combined ESG score per company and year, on a scale from 0 to 100:

{% include ft-chart.html id="getting-started-esg" src="/assets/data/financetoolkit-guides/getting-started.json" label="ESG scores of Apple, Microsoft, Alphabet and Amazon since 2015" %}

### Revenue Segmentation

Most large companies also report their revenue split by product line and by region. The Toolkit returns both segmentations with the segment names as each company reports them, so they differ per company and can change over the years when a company reorganises its reporting.

To retrieve the product and geographic segmentation, and select Apple's:

```python
product_segmentation = companies.get_revenue_product_segmentation()
geographic_segmentation = companies.get_revenue_geographic_segmentation()

product_segmentation.loc["AAPL"]
```

When plotted, Apple's revenue per product line since 2019, the first year it reported all five, and per region since 2015:

{% include ft-chart.html id="getting-started-segments" src="/assets/data/financetoolkit-guides/getting-started.json" label="Apple's revenue by product line since 2019 and by region since 2015" %}

The earnings calendar, dividend calendar, company profiles, quotes, news and more are available in the same way; the sidebar lists every function.

{% include ft-charts-script.html %}
