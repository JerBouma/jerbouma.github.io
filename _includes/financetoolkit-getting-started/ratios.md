## Getting Started

Ratios are where most company analysis starts: they turn the raw line items of the balance sheet, income statement and cash flow statement into numbers you can compare across companies and over time. The Ratios module calculates 80+ of them in five categories, efficiency, liquidity, profitability, solvency and valuation, each with one documented formula, so a margin or a coverage ratio means the same thing for every company. Where the built-in set falls short, you define your own.

### Loading the Data

The Ratios module works on the statements of a `Toolkit` instance. This section uses Apple, Amazon, Meta and Walmart from 2005 onwards, four companies with very different business models. Annual statements are the default; add `quarterly=True` for quarterly statements (a paid Financial Modeling Prep plan).

To load the four companies:

```python
from financetoolkit import Toolkit

API_KEY = "FINANCIAL_MODELING_PREP_KEY"

companies = Toolkit(
    ["AAPL", "AMZN", "META", "WMT"], api_key=API_KEY, start_date="2005-01-01"
)
```

The statements and prices are retrieved the first time a ratio needs them and are reused for every ratio after that. Walmart's fiscal year ends in January, so the Toolkit maps its fiscal years to calendar years to line them up with the others.

### Collecting All Ratios

The module makes a distinction between `collect_` and `get_` functions. A `collect_` function returns a whole group at once, such as `collect_profitability_ratios` or `collect_all_ratios`, while a `get_` function returns one ratio.

To calculate every ratio for every company and year:

```python
companies.ratios.collect_all_ratios()
```

This returns one table with the ticker and the ratio as rows and the years as columns. A selection of the ratios for the latest fiscal year:

|                                | Apple  | Amazon | Meta   | Walmart |
|:-------------------------------|-------:|-------:|-------:|--------:|
| Gross Margin                   | 46.9%  | 50.3%  | 82.0%  | 24.9%   |
| Return on Equity               | 171.4% | 22.3%  | 30.2%  | 21.5%   |
| Current Ratio                  | 0.89   | 1.05   | 2.60   | 0.79    |
| Debt-to-Equity Ratio           | 1.52   | 0.37   | 0.39   | 0.63    |
| Price-to-Earnings              | 36.3   | 32.2   | 28.0   | 40.6    |
| Cash Conversion Cycle (days)   | -71.8  | -42.2  | -50.3  | 3.2     |

The cash conversion cycle shows the differences in business model at a glance: Apple, Amazon and Meta collect cash from their customers weeks before they pay their suppliers, while Walmart's cycle is close to zero. Apple's return on equity above 100% is the result of its small equity base after years of buybacks, not of exceptional margins.

The gross margin from the same table, per company since 2015:

{% include ft-chart.html id="ratios-gross-margin" src="/assets/data/financetoolkit-guides/ratios.json" label="Gross margin of Apple, Amazon, Meta and Walmart since 2015" %}

Amazon's gross margin rose from 33% to 50% over the decade and Apple's from 40% to 47%, while Meta's stayed above 80% and Walmart's at about 25%, the margin of a retailer that mostly sells other companies' products.

### Individual Ratios

When you need only one ratio, call its `get_` function. The effective tax rate, the income tax expense divided by the income before tax, is a good example of a ratio that tells a story over time.

To calculate the effective tax rate of each company:

```python
companies.ratios.get_effective_tax_rate()
```

Which gives the effective tax rate per fiscal year, shown here from 2015, one company per tab, against the US federal corporate rate:

{% include ft-chart.html id="ratios-effective-tax-rate" src="/assets/data/financetoolkit-guides/ratios.json" label="Effective tax rate of Apple, Amazon, Meta and Walmart since 2015" %}

The returned table goes back to 2005, but Amazon's and Meta's income before tax was close to zero in their early years, which pushes the rate far outside the 0–100% range (Amazon's comes out at about -226% in 2014). Walmart's rate is the most stable, between about 23% and 37%, while Apple's fell from about 26% to around 15% after the 2017 US tax reform cut the federal rate from 35% to 21%. Its jump to 24% in 2024 is a one-off: the European Commission's state aid ruling added a tax charge of about $10 billion that year. Amazon's 54% in 2022 is not a high tax bill: it made a loss before tax that year, and the rate reflects the tax benefit on that loss.

### Ratio Options

Several ratios accept options where more than one calculation method is common. `diluted`, for example, sets whether per-share ratios use the diluted or the basic number of shares. All ratios also accept `growth=True`, which returns the change from one period to the next instead of the ratio itself, so you can see whether a company's leverage or coverage is improving or deteriorating.

To collect the solvency ratios with the basic number of shares, as growth rates:

```python
companies.ratios.collect_solvency_ratios(diluted=False, growth=True)
```

Which gives, for Walmart, among other ratios:

|                          | 2023   | 2024   | 2025   |
|:-------------------------|-------:|-------:|-------:|
| Debt-to-Equity Ratio     | -3.5%  | -9.1%  | 2.7%   |
| Debt-to-Capital Ratio    | -2.1%  | -5.7%  | 1.7%   |
| Net-Debt to EBITDA Ratio | -17.4% | -8.8%  | 6.1%   |
| Cash Flow Coverage Ratio | 19.0%  | 4.1%   | 2.2%   |

Growth works the same for a single ratio. To get the growth of the price-to-book ratio:

```python
companies.ratios.get_price_to_book_ratio(growth=True)
```

Which gives the year-over-year change of each company's price-to-book ratio over the last ten years, one cell per company and year:

{% include ft-chart.html id="ratios-price-to-book-growth" src="/assets/data/financetoolkit-guides/ratios.json" label="Year-over-year growth of the price-to-book ratio since 2013" %}

The 2022 sell-off stands out: Meta's price-to-book ratio fell by about two thirds and Amazon's by half, before Meta's more than doubled again in 2023.

By default growth is measured against the previous period. `lag` sets how many periods back to compare with, and a list of lags returns each of them. To get the growth of the current ratio over one, two and three years:

```python
companies.ratios.get_current_ratio(growth=True, lag=[1, 2, 3])
```

Which gives the three growth rates per company since 2015, one company per tab:

{% include ft-chart.html id="ratios-current-ratio-lags" src="/assets/data/financetoolkit-guides/ratios.json" label="Growth of the current ratio over one, two and three years" %}

Longer lags smooth out a single unusual year and show whether a trend persists: Apple's current ratio, for example, has been lower than three years earlier in most recent years.

### Trailing Ratios

`trailing` calculates a ratio over the last N periods instead of one period. On quarterly data, `trailing=4` gives the trailing twelve months (TTM), the usual basis for earnings per share. On annual data, as in this section, the same setting sums four years, which smooths the earnings of cyclical companies; set `quarterly=True` in the Toolkit for TTM figures.

To calculate the trailing earnings per share and its growth:

```python
companies.ratios.get_earnings_per_share(trailing=4)

companies.ratios.get_earnings_per_share(trailing=4, growth=True)
```

Which gives the earnings per share summed over four years and its growth, one per tab; the growth starts in 2019, as Amazon's jump of 401% in 2016 would dwarf every other year:

{% include ft-chart.html id="ratios-trailing-eps" src="/assets/data/financetoolkit-guides/ratios.json" label="Earnings per share summed over four years, and its growth" %}

Meta's four-year earnings per share has risen to about $72, more than eight times Walmart's $8.54, while Amazon's has more than doubled in the last three years, from $6.24 to $15.21.

### Forward Valuation

The forward P/E and forward PEG ratios use the analyst consensus estimate of earnings per share for a future year instead of the reported figure. They show what the market pays for expected rather than past earnings, which matters most for companies whose earnings are growing fast. The analyst estimates are retrieved automatically the first time either function is called, and require a paid Financial Modeling Prep plan.

To calculate the forward P/E and forward PEG ratios:

```python
companies.ratios.get_forward_price_earnings_ratio()

companies.ratios.get_forward_price_earnings_growth_ratio()
```

The forward P/E for the next three fiscal years, based on the share price and the consensus at the time of the calculation:

|         | 2026 | 2027 | 2028 |
|:--------|-----:|-----:|-----:|
| Apple   | 38.4 | 35.4 | 31.8 |
| Amazon  | 20.5 | 24.6 | 18.4 |
| Meta    | 22.7 | 20.5 | 17.7 |
| Walmart | 44.7 | 40.8 | 36.6 |

Measured on expected earnings, Amazon and Meta are the cheapest of the four and Walmart the most expensive. The forward PEG divides the forward P/E by the expected growth of earnings per share, so it swings widely when the expected growth is small and turns negative when the estimates expect earnings to fall.

### Shareholder Yield and Debt-to-Capital

The dividend yield understates what companies that prefer buybacks return to their shareholders. The shareholder yield adds the buyback yield to the dividend yield, which makes Apple and Walmart comparable even though they split their payouts differently. The debt-to-capital ratio, debt divided by debt plus equity, stays between 0 and 1, unlike the debt-to-equity ratio, which makes capital structures easier to compare across companies with very different leverage.

To calculate both:

```python
companies.ratios.get_shareholder_yield()

companies.ratios.get_debt_to_capital_ratio()
```

Which gives the two ratios from 2013, Apple against Walmart:

{% include ft-chart.html id="ratios-shareholder-yield" src="/assets/data/financetoolkit-guides/ratios.json" label="Shareholder yield and debt-to-capital ratio since 2013" %}

Apple returned between about 2.5% and 11.5% of its market value a year, at the lower end in recent years, and Walmart between 1.5% and 8%. Apple's debt-to-capital ratio rose from about 12% to above 60% over the same period, as it borrowed to fund those buybacks, while Walmart's stayed between 36% and 47%. Amazon is left out of the comparison: it returns next to nothing to its shareholders and reinvests its cash, so its shareholder yield is zero in most years.

### Custom Ratios

When a ratio you need isn't built in, define it yourself. A custom ratio is a name with a formula written in the Toolkit's own line item names, which are the same for every company. A formula can contain:

- **Simple operations:** `"Quick Assets": "Cash and Short Term Investments + Accounts Receivable"`
- **Multiple operations:** `"Cash Op Expenses": "Cost of Goods Sold + Selling, General and Administrative Expenses - Depreciation and Amortization"`
- **Brackets:** `"WC / Net Income as %": "(Working Capital / Net Income) * 100"`
- **A criterion:** `"Large Revenues": "Revenue > 1000000000"`, which returns 1 when it holds and 0 when it doesn't
- **Numbers:** `"Daily Cash Op Expenses": "Cash Op Expenses / 365"`
- **Earlier custom ratios:** `"Defensive Interval": "Quick Assets / Daily Cash Op Expenses"`

The formulas can use any line item from the three statements and any built-in ratio. To list every name you can use:

```python
companies.ratios.collect_custom_ratios(options=True)
```

Which returns the names in alphabetical order, such as `Buyback Yield`, `CAPEX Coverage Ratio`, `CAPEX per Share`, `Capital Expenditure` and `Capital Lease Obligations`.

To define the six ratios above and calculate them:

```python
custom_ratios = {
    "WC / Net Income as %": "(Working Capital / Net Income) * 100",
    "Large Revenues": "Revenue > 1000000000",
    "Quick Assets": "Cash and Short Term Investments + Accounts Receivable",
    "Cash Op Expenses": "Cost of Goods Sold + Selling, General and Administrative Expenses "
    "- Depreciation and Amortization",
    "Daily Cash Op Expenses": "Cash Op Expenses / 365",
    "Defensive Interval": "Quick Assets / Daily Cash Op Expenses",
}

companies.ratios.collect_custom_ratios(custom_ratios_dict=custom_ratios)
```

Which gives, for the latest fiscal year:

|         | Quick Assets | Daily Cash Op Expenses | Defensive Interval (days) | WC / Net Income as % |
|:--------|-------------:|-----------------------:|--------------------------:|---------------------:|
| Apple   | $94.5B       | $649M                  | 146                       | -15.8                |
| Amazon  | $190.8B      | $956M                  | 200                       | 14.3                 |
| Meta    | $101.4B      | $114M                  | 887                       | 110.6                |
| Walmart | $21.9B       | $1,833M                | 12                        | -103.2               |

The defensive interval is the number of days a company could pay its cash operating expenses from its quick assets alone. Meta could cover more than two years, Walmart less than two weeks, which is normal for a retailer whose inventory turns into cash quickly.

### Using the Ratio Formulas Directly

The `Toolkit` retrieves the statements for you, but every ratio is also available as a plain function in the underlying models. These take pandas Series or DataFrames, so you can apply the same formulas to data from any source.

To calculate five ratios from your own numbers (dummy data here):

```python
import pandas as pd

from financetoolkit.ratios import (
    efficiency_model,
    liquidity_model,
    profitability_model,
    solvency_model,
    valuation_model,
)

asset_turnover = efficiency_model.get_asset_turnover_ratio(
    sales=pd.Series([100, 110, 120, 130, 80]),
    average_total_assets=pd.Series([500, 400, 300, 200, 100]),
)

quick_ratio = liquidity_model.get_quick_ratio(
    cash_and_equivalents=pd.Series([100, 110, 120, 130, 80]),
    accounts_receivable=pd.Series([30, 20, 30, 20, 40]),
    marketable_securities=pd.Series([30, 10, 30, 20, 40]),
    current_liabilities=pd.Series([130, 120, 110, 150, 100]),
)

return_on_assets = profitability_model.get_return_on_assets(
    net_income=pd.Series([80, 40, 40, 30, 20]),
    average_total_assets=pd.Series([150, 200, 300, 400, 500]),
)

debt_to_assets = solvency_model.get_debt_to_assets_ratio(
    total_debt=pd.Series([100, 110, 120, 130, 80]),
    total_assets=pd.Series([200, 140, 160, 160, 300]),
)

price_to_earnings = valuation_model.get_price_to_earnings_ratio(
    stock_price=pd.Series([30, 11, 12, 10, 30]),
    earnings_per_share=pd.Series([0.5, 0.4, 0.1, 1.1, 1.2]),
)

pd.DataFrame(
    {
        "Asset Turnover": asset_turnover,
        "Quick Ratio": quick_ratio,
        "Return on Assets": return_on_assets,
        "Debt to Assets": debt_to_assets,
        "Price to Earnings": price_to_earnings,
    }
)
```

Which gives:

|   | Asset Turnover | Quick Ratio | Return on Assets | Debt to Assets | Price to Earnings |
|--:|---------------:|------------:|-----------------:|---------------:|------------------:|
| 0 | 0.20           | 1.23        | 0.53             | 0.50           | 60.0              |
| 1 | 0.28           | 1.17        | 0.20             | 0.79           | 27.5              |
| 2 | 0.40           | 1.64        | 0.13             | 0.75           | 120.0             |
| 3 | 0.65           | 1.13        | 0.08             | 0.81           | 9.1               |
| 4 | 0.80           | 1.60        | 0.04             | 0.27           | 25.0              |

To run the whole Toolkit, not only single formulas, on your own statements, see [Using External Datasets](/projects/financetoolkit/docs#using-external-datasets).

{% include ft-charts-script.html %}
