---
title: Models
seo_title: "Models Module | Finance Toolkit"
seo_title_suffix: false
excerpt: The Models module is meant to execute well-known models such as DUPONT and the Discounted Cash Flow (DCF) model. These models are also directly related to the data retrieved from the Toolkit module.
description: "Reference for every function and parameter in the Finance Toolkit's Models module: DuPont analysis, Discounted Cash Flow (DCF) and valuation models."
author_profile: false
permalink: /projects/financetoolkit/docs/models
classes: wide-sidebar
layout: single
redirect_from:
    - /models
    - /projects/financetoolkit/models-notebook
sidebar:
    nav: "financetoolkit-docs-models"
---

The Models module executes well-known models such as DuPont analysis and the Discounted Cash Flow (DCF) model, using data retrieved from the Toolkit module.

Use it in Claude, ChatGPT or another AI assistant through the [Finance Toolkit MCP](/projects/financetoolkit/mcp), or install the Python package:

```python
pip install financetoolkit -U
```

{% include algolia.html %}

{% include financetoolkit-getting-started/models.md %}

## get_dupont_analysis
Perform a Dupont analysis to breakdown the return on equity (ROE) into its components.

The Dupont analysis is a method used to dissect and understand the factors that drive a company's return on equity (ROE). It breaks down the ROE into three key components: Net Profit Margin, Asset Turnover, and Equity Multiplier.

The formula is as follows:

$$
\text{Net Profit Margin} = \text{Net Income} / \text{Revenue}
$$

$$
\text{Asset Turnover} = \text{Revenue} / \text{Average Total Assets}
$$

$$
\text{Equity Multiplier} = \text{Average Total Assets} / \text{Average Total Equity}
$$

$$
\text{ROE} = \text{Net Profit Margin} \cdot \text{Asset Turnover} \cdot \text{Equity Multiplier}
$$

The value of the decomposition is in comparing the three factors with peers and over time: a retailer earns its return on equity through asset turnover, a software company through its margin and a bank through leverage. A rising return on equity driven only by the Equity Multiplier, for example through share buybacks that shrink equity, is of lower quality than one driven by margin or turnover, and with negative equity the decomposition stops being meaningful.

**Also known as:** DuPont, ROE decomposition, three-factor DuPont.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. Defaults to None.
- <u>show_columns (list[str] &#124; None, optional):</u> Restrict the result to these columns. Defaults to None,
which shows all columns.

**Returns:**

pd.DataFrame: DataFrame containing Dupont analysis results, including Net Profit Margin, Asset
Turnover, Equity Multiplier, and the calculated ROE values.

**Notes:**

- The Net Profit Margin is the ratio of Net Income to Total Revenue, indicating the percentage
of revenue that translates into profit.
- Asset Turnover measures the efficiency of a company's use of its assets to generate sales
revenue.
- The Equity Multiplier measures financial leverage, the use of debt to finance a company's
operations, which can amplify returns as well as risks.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["GOOGL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_dupont_analysis()
```

Which returns:

|                   |   2021 |   2022 |   2023 |   2024 |   2025 |
|:------------------|-------:|-------:|-------:|-------:|-------:|
| Net Profit Margin | 0.2951 | 0.212  | 0.2401 | 0.286  | 0.3281 |
| Asset Turnover    | 0.759  | 0.7807 | 0.8009 | 0.821  | 0.7706 |
| Equity Multiplier | 1.4317 | 1.4269 | 1.4228 | 1.4013 | 1.4122 |
| Return on Equity  | 0.3207 | 0.2362 | 0.2736 | 0.3291 | 0.357  |

---

## get_extended_dupont_analysis
Perform an Extended Dupont analysis to breakdown the return on equity (ROE) into its components, while considering additional financial metrics.

The Extended Dupont analysis splits the three-factor decomposition's Net Profit Margin into three separate drivers - the Tax Burden, the Interest Burden and the Operating Profit Margin - so that the effect of taxation, of financing costs and of operating performance on the return on equity (ROE) can be read separately.

The formula is as follows:

$$
\text{Interest Burden Ratio} = \text{Income Before Tax} / \text{Operating Income}
$$

$$
\text{Tax Burden Ratio} = \text{Net Income} / \text{Income Before Tax}
$$

$$
\text{Operating Profit Margin} = \text{Operating Income} / \text{Revenue}
$$

$$
\text{Asset Turnover} = \text{Revenue} / \text{Average Total Assets}
$$

$$
\text{Equity Multiplier} = \text{Average Total Assets} / \text{Average Total Equity}
$$

$$
\text{ROE} = \text{Interest Burden Ratio} \cdot \text{Tax Burden Ratio} \cdot \text{Operating Profit Margin} \cdot \text{Asset Turnover} \cdot \text{Equity Multiplier}
$$

**Also known as:** extended DuPont, five-factor DuPont, ROE breakdown.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. Defaults to None.
- <u>show_columns (list[str] &#124; None, optional):</u> Restrict the result to these columns. Defaults to None,
which shows all columns.

**Returns:**

pd.DataFrame: DataFrame containing Extended Dupont analysis results, including the Interest
Burden Ratio, Tax Burden Ratio, Operating Profit Margin, Asset Turnover, Equity
Multiplier, and the calculated ROE values.

**Notes:**

- The Interest Burden Ratio (Income Before Tax / Operating Income) measures how much of
operating profit survives the cost of debt financing. It equals 1 for a company with no
net interest expense and falls as interest costs rise.
- The Tax Burden Ratio (Net Income / Income Before Tax) measures how much of pre-tax
profit survives taxation, i.e. it equals (1 - Effective Tax Rate).
- The Operating Profit Margin measures operating performance before financing and tax
effects.
- Asset Turnover measures the efficiency of a company's use of its assets to generate
sales revenue.
- The Equity Multiplier represents the use of debt to finance a company's operations,
which can amplify returns as well as risks.
- Multiplying the first three components back together reproduces the Net Profit Margin
of the three-factor `get_dupont_analysis`, so both decompositions resolve to the same ROE.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_extended_dupont_analysis()
```

Which returns:

|                         |   2021 |   2022 |   2023 |   2024 |   2025 |
|:------------------------|-------:|-------:|-------:|-------:|-------:|
| Interest Burden Ratio   | 1.017  | 1.004  | 1.0089 | 0.985  | 0.9619 |
| Tax Burden Ratio        | 0.8617 | 0.8689 | 0.8102 | 0.8177 | 0.8237 |
| Operating Profit Margin | 0.4159 | 0.4206 | 0.4177 | 0.4464 | 0.4562 |
| Asset Turnover          | 0.5293 | 0.5676 | 0.5456 | 0.5305 | 0.4981 |
| Equity Multiplier       | 2.4399 | 2.2643 | 2.0839 | 1.9468 | 1.8484 |
| Return on Equity        | 0.4708 | 0.4715 | 0.3882 | 0.3713 | 0.3328 |

---

## get_enterprise_value_breakdown
Calculate the Enterprise Value (EV) breakdown, providing a detailed view of its components.

The Enterprise Value breakdown includes the following components for each quarter or year:

- Share Price: The market price per share of the company's stock.
- Market Capitalization (Market Cap): The total value of a company's outstanding common shares, i.e. the share price multiplied by the shares outstanding. Preferred shares are excluded here and enter as their own component below, so that they are counted once rather than twice.
- Debt: The sum of long-term and short-term debt on the company's balance sheet.
- Preferred Equity: The value of preferred shares, if applicable.
- Minority Interest: The equity value of a subsidiary with less than 50% ownership.
- Cash and Cash Equivalents: The cash and the investments that are readily convertible to cash within three months, such as money market funds and Treasury bills.
- Short Term Investments: The marketable securities that are not cash equivalents.

Cash and marketable securities are deducted together (Damodaran), the same Enterprise Value as toolkit.ratios.get_enterprise_value returns.

The formula is as follows:

$$
\text{Market Capitalization} = \text{Share Price} \cdot \text{Weighted Average Shares Diluted} (\text{Weighted Average Shares when diluted} = \text{False}),\;\; \text{with the share price the traded close at the end of each quarter or year}
$$

$$
\text{Enterprise Value} = \text{Market Capitalization} + \text{Total Debt} + \text{Preferred Equity} + \text{Minority Interest} - \text{Cash and Cash Equivalents} - \text{Short Term Investments}
$$

This breakdown is displayed in a DataFrame for each company and includes the option to show growth values as well.

**Also known as:** EV breakdown, enterprise value components, EV bridge.

**Args:**

- <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (list[str] &#124; None, optional):</u> Restrict the result to these columns. Defaults to None,
which shows all columns.

**Returns:**

pd.DataFrame: DataFrame containing the Enterprise Value breakdown, including the calculated components.

**Notes:**

- All the inputs must be in the same currency and unit for accurate calculations.
- The Enterprise Value is an important metric used for valuation and investment analysis.
It represents the cost of acquiring the entire business: the equity is bought at its market
value, the debt (and any preferred equity and minority interest) is assumed, and the acquired
cash reduces the effective price, which is why cash is subtracted rather than added.
- Enterprise Value is positive for essentially every going concern. It only turns negative
when a company's cash exceeds its market capitalization plus its debt, which is a sign of a
cash-rich balance sheet priced below its net cash — not of financial distress. A distressed,
heavily indebted company shows the opposite: an Enterprise Value far above its market
capitalization.
- Understanding the Enterprise Value breakdown can provide insights into the sources of a
company's value and potential risks.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["F"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_enterprise_value_breakdown().loc[
    ["Market Capitalization", "Total Debt", "Cash and Cash Equivalents", "Enterprise Value"]
]
```

Which returns:

|                           |        2021 |        2022 |        2023 |        2024 |        2025 |
|:--------------------------|------------:|------------:|------------:|------------:|------------:|
| Market Capitalization     | 8.37862e+10 | 4.66828e+10 | 4.92598e+10 | 3.98079e+10 | 5.22045e+10 |
| Total Debt                | 1.39485e+11 | 1.40474e+11 | 1.51107e+11 | 1.60862e+11 | 1.67573e+11 |
| Cash and Cash Equivalents | 2.054e+10   | 2.5134e+10  | 2.4862e+10  | 2.2935e+10  | 2.3356e+10  |
| Enterprise Value          | 1.73781e+11 | 1.43012e+11 | 1.60221e+11 | 1.62345e+11 | 1.81318e+11 |

---

## get_tobins_q_ratio
Calculate Tobin's Q Ratio, a valuation metric developed by economist James Tobin that compares the market value of a company to the cost of replacing its assets.

The formula is as follows:

$$
\text{Market Value of Equity} = \text{Share Price} \cdot \text{Total Shares Outstanding}
$$

$$
\text{Tobin's}\; Q \;\text{Ratio} = (\text{Market Value of Equity} + \text{Total Liabilities}) / \text{Total Assets}
$$

Tobin's Q Ratio can be interpreted as follows:

- A Q ratio greater than 1 indicates that the market values the company above the cost of replacing its assets, which can reflect growth expectations, unrecognized intangible value, or overvaluation.
- A Q ratio less than 1 indicates that the market values the company below the cost of replacing its assets, which can reflect undervaluation or declining growth prospects.

Because the book value of assets leaves out most intangibles (brands, software, research), companies built on them show a Q far above 1 without being overvalued in Tobin's sense, so the ratio is most informative within an industry and over time. In macroeconomics the aggregate Q of the corporate sector is read as a signal for investment: a Q above 1 makes new capital worth more than it costs.

**Also known as:** Tobin's Q, Q ratio.

**Args:**

- <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. Defaults to None.
- <u>show_columns (list[str] &#124; None, optional):</u> List of columns to show in the results. If None, all
columns will be shown. Defaults to None.

**Returns:**

pd.DataFrame: DataFrame containing the Market Value of Equity, Total Liabilities,
Total Assets and Tobin's Q Ratio.

**Notes:**

- This implementation approximates the market value of debt with the book value of
Total Liabilities, and the replacement cost of assets with the book value of Total
Assets, consistent with the simplifications used in the Weighted Average Cost of
Capital calculation elsewhere in this module.

References:
- Tobin, James. "A General Equilibrium Approach to Monetary Theory." Journal of Money,
Credit and Banking, Vol. 1, No. 1, 1969, pp. 15-29.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["INTC", "QCOM", "TXN"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_tobins_q_ratio().xs("Tobin's Q Ratio", level=1)
```

Which returns:

|      |   2021 |   2022 |   2023 |   2024 |   2025 |
|:-----|-------:|-------:|-------:|-------:|-------:|
| INTC | 1.6843 | 1.0312 | 1.5308 | 0.9022 | 1.2499 |
| QCOM | 5.8537 | 3.1828 | 3.7679 | 3.671  | 4.3465 |
| TXN  | 7.6086 | 6.0875 | 5.3046 | 5.3769 | 5.1094 |

---

## get_weighted_average_cost_of_capital
The Weighted Average Cost of Capital (WACC) is a financial metric used to estimate the cost of capital for a company. It represents the average rate of return a company must pay to its investors for using their capital. WACC takes into account the cost of both equity and debt, weighted by their respective proportions in the company's capital structure.

The formula is as follows:

$$
\text{Market Value of Equity} = \text{Share Price} \cdot \text{Total Shares Outstanding}
$$

$$
\text{Market Value of Debt} = \text{Total Debt}
$$

$$
\text{Total Market Value} = \text{Market Value of Equity} + \text{Market Value of Debt}
$$

$$
\text{Cost of Equity} = \text{Risk Free Rate} + \text{Beta} \cdot \text{Market Risk Premium}
$$

$$
\text{Cost of Debt} = \text{Interest Expense} / \text{Total Debt}
$$

$$
\text{WACC} = (\text{Market Value of Equity} / \text{Total Market Value}) \cdot \text{Cost of Equity} + (\text{Market Value of Debt} / \text{Total Market Value}) \cdot \text{Cost of Debt} \cdot (1 - \text{Corporate Tax Rate})
$$

Cost of Equity (Re): The cost of equity represents the return required by the company's shareholders or equity investors. It is the cost of raising funds by selling equity (such as common stock). The cost of equity is often estimated using methods like the Capital Asset Pricing Model (CAPM) or the Dividend Discount Model (DDM).

Cost of Debt (Rd): The cost of debt is the interest rate the company pays on its outstanding debt. It is the cost of raising funds through borrowing, such as issuing bonds or taking loans. The cost of debt is typically based on the prevailing interest rates in the market and the company's creditworthiness.

Corporate Tax Rate (Tc): The corporate tax rate is the percentage of a company's profits that is paid in taxes. It is used to calculate the tax shield on interest payments. Interest expenses on debt reduce taxable income, and the tax shield represents the tax savings resulting from these deductions.

Market Value of Equity (E): The market value of equity is the total value of the company's outstanding shares of common stock. It is calculated by multiplying the current stock price by the number of shares outstanding.

Market Value of Debt (D): The market value of debt is the total value of the company's outstanding debt obligations, such as bonds and loans. It represents the current market price of the debt instruments.

Total Market Value of Capital (V): The total market value of capital is the sum of the market value of equity and the market value of debt (V = E + D). It represents the total value of the company's financing, both through equity and debt.

The WACC is the discount rate for the free cash flow to the firm and the hurdle rate for new investments, so analysts usually build it from forward-looking inputs: a long-term government bond yield, an equity risk premium of a few percent, a beta measured over several years and the yield on the company's debt. Small changes matter: in a DCF with 2.5% perpetual growth, moving the WACC from 8% to 9% lowers the terminal value by about 15%.

**Also known as:** WACC, blended cost of capital, discount rate.

**Args:**

- <u>show_full_results (bool, optional):</u> Whether to show the full results or just the WACC values.
Defaults to True.
- <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. Defaults to None.
- <u>market_risk_premium (float &#124; None, optional):</u> The annual equity risk premium the Cost of Equity
uses. Defaults to None, which takes the benchmark's average return above the risk-free rate
over every period of the data.
- <u>show_columns (list[str] &#124; None, optional):</u> Restrict the result to these columns. Defaults to None,
which shows all columns.

**Returns:**

pd.DataFrame: DataFrame containing the WACC values.

**Notes:**

- The Cost of Equity follows from the Capital Asset Pricing - <u>Model (CAPM):</u> the risk-free rate of
the period plus Beta times the market risk premium, which defaults to the benchmark's average
return above the risk-free rate over every period of the data (set `market_risk_premium` to use
another premium, e.g. an implied equity risk premium). Beta is estimated from the period's daily
returns. With quarterly data the rates are per quarter, the risk-free yield divided by four.
- With `trailing` set, the Interest Expense is summed over the trailing periods, so the Cost of
Debt covers that span, and the risk-free rate and premium of the Cost of Equity are the per-period
rates times `trailing`. With quarterly data and trailing=4, every rate is an annual rate.
- The Market Value of Debt is approximated as the Total Debt.
- The Cost of Debt is the Interest Expense divided by the Total Debt at the end of the period
(the average over the trailing periods with `trailing` set), so debt raised or repaid during the
period moves it away from the rate on the average debt outstanding.
- The Corporate Tax Rate is the effective tax rate (Income Tax Expense / Income Before Tax),
kept within 0 and 1 so that a tax benefit does not turn the tax shield negative, and 0 for a
period without a pre-tax profit, which leaves no taxable income for the interest to shield.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["VZ", "T", "TMUS"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2022-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_weighted_average_cost_of_capital().xs(
    "Weighted Average Cost of Capital", level=1
)
```

Which returns:

|      |   2022 |   2023 |   2024 |   2025 |
|:-----|-------:|-------:|-------:|-------:|
| T    | 0.0787 | 0.0754 | 0.0259 | 0.0496 |
| TMUS | 0.1087 | 0.0776 | 0.072  | 0.0645 |
| VZ   | 0.0562 | 0.0727 | 0.0346 | 0.0425 |

---

## get_economic_value_added
Economic Value Added (EVA) is a measure of a company's financial performance that represents the value created in excess of the required return of the company's capital providers. It captures whether a company is generating returns above its true cost of capital, which distinguishes it from purely accounting-based measures such as Net Income.

The formula is as follows:

$$
\text{NOPAT} = \text{EBIT} \cdot (1 - \text{Corporate Tax Rate})
$$

$$
\text{Invested Capital} = \text{Total Equity} + \text{Total Debt}
$$

$$
\text{EVA} = \text{NOPAT} - (\text{Weighted Average Cost of Capital} \cdot \text{Invested Capital})
$$

EVA is mostly used to compare value creation across business units or companies and over time, and as a basis for management compensation. It is equivalent to (Return on Invested Capital - WACC) * Invested Capital, so a company with a high return on capital but a small capital base can create less EVA than a larger, less profitable one.

**Also known as:** EVA, economic profit.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. Defaults to None.
- <u>market_risk_premium (float &#124; None, optional):</u> The annual equity risk premium the Cost of Equity
uses. Defaults to None, which takes the benchmark's average return above the risk-free rate
over every period of the data.
- <u>show_columns (list[str] &#124; None, optional):</u> List of columns to show in the results. If None, all
columns will be shown. Defaults to None.

**Returns:**

pd.DataFrame: DataFrame containing the EVA and its components.

**Notes:**

- A positive EVA indicates that the company is generating returns in excess of its cost of
capital, i.e. it is creating value for its capital providers. A negative EVA indicates the
company is destroying value.
- EBIT is the reported Operating Income, as in the other models of this module and the
EBIT based ratios of the Ratios module.
- The Corporate Tax Rate is the effective tax rate (Income Tax Expense / Income Before Tax)
kept within 0 and 1, and 0 for a period without a pre-tax profit, the same rate the
Weighted Average Cost of Capital uses (see `get_weighted_average_cost_of_capital`).
- Invested Capital is the sum of the two-period average of Total Equity and the two-period
average of Total Debt, i.e. the capital employed over the course of the period rather than
its closing balance, consistent with the Return on Invested Capital calculation in the
Ratios module.
- The Weighted Average Cost of Capital comes from `get_weighted_average_cost_of_capital`,
with the market risk premium given by `market_risk_premium` (by default the benchmark's
average return above the risk-free rate over the data) and the same `trailing`, so that it
covers the span of the NOPAT (an annual rate for trailing=4 with quarterly data).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["V", "MA", "HD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2022-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_economic_value_added().xs("Economic Value Added", level=1)
```

Which returns:

|    |        2022 |        2023 |        2024 |        2025 |
|:---|------------:|------------:|------------:|------------:|
| HD | 9.57216e+09 | 5.61294e+09 | 6.25513e+09 | 5.96403e+09 |
| MA | 6.03519e+09 | 7.72427e+09 | 1.00151e+10 | 1.06193e+10 |
| V  | 3.68483e+09 | 6.85635e+09 | 1.04752e+10 | 8.9369e+09  |

---

## get_market_value_added
Market Value Added (MVA) is a measure of a company's financial performance that represents the difference between the current market value of a company (both its equity and its debt) and the total capital that has historically been invested in it. It is the market-priced counterpart to Economic Value Added (EVA): where EVA measures a single period's excess return over the cost of capital, MVA reflects the market's cumulative, forward-looking verdict on all of a company's expected future EVA.

The formula is as follows:

$$
\text{Market Value of Equity} = \text{Share Price} \cdot \text{Total Shares Outstanding}
$$

$$
\text{Invested Capital} = \text{Total Equity} + \text{Total Debt}
$$

$$
\text{MVA} = (\text{Market Value of Equity} + \text{Market Value of Debt}) - \text{Invested Capital}
$$

**Also known as:** MVA, market value added.

**Args:**

- <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. Defaults to None.
- <u>show_columns (list[str] &#124; None, optional):</u> List of columns to show in the results. If None, all
columns will be shown. Defaults to None.

**Returns:**

pd.DataFrame: DataFrame containing the MVA and its components.

**Notes:**

- A positive MVA indicates that the market believes management has created value in
excess of the capital invested in the company. A negative MVA indicates the market
values the company below the capital that has historically been invested in it.
- The Market Value of Debt is approximated as the closing book value of Total Debt,
the same simplification used in the Weighted Average Cost of Capital calculation
elsewhere in this module.
- Invested Capital is the sum of the two-period average of Total Equity and the
two-period average of Total Debt, i.e. the capital that was employed *during* the
period, matching the Economic Value Added calculation elsewhere in this module. Note
that this leaves the two sides of the MVA measured on slightly different bases: the
market value is a closing (point-in-time) figure while the invested capital is an
average over the period.

References:
- Stern, Joel M., G. Bennett Stewart, and Donald H. Chew. "The EVA Financial
Management System." Journal of Applied Corporate Finance, Vol. 8, No. 2, 1995, pp. 32-46.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["LLY", "JNJ", "MRK"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_market_value_added().xs("Market Value Added", level=1)
```

Which returns:

|     |        2021 |        2022 |        2023 |        2024 |        2025 |
|:----|------------:|------------:|------------:|------------:|------------:|
| JNJ | 3.88033e+11 | 3.9811e+11  | 3.23373e+11 | 2.84859e+11 | 4.31897e+11 |
| LLY | 2.56073e+11 | 3.37326e+11 | 5.20216e+11 | 6.89575e+11 | 9.49091e+11 |
| MRK | 1.63289e+11 | 2.38554e+11 | 2.37969e+11 | 2.11776e+11 | 2.20502e+11 |

---

## get_intrinsic_valuation
Intrinsic value is a fundamental concept in finance and investing that represents the true worth or value of an asset, security, or investment, independent of its current market price or prevailing market sentiment. It is a concept often associated with the value investing philosophy, made famous by legendary investors like Benjamin Graham and Warren Buffett. Understanding intrinsic value is crucial for investors looking to make informed decisions about where to allocate their capital.

This functionality uses DCF, or Discounted Cash Flow which is a widely used financial valuation method that allows investors and analysts to estimate the intrinsic value of an investment or business based on its expected future cash flows. It is a fundamental tool in finance and investment analysis, providing a systematic way to assess the present value of future cash flows while considering the time value of money.

The formula is as follows:

$$
\text{Cash Flow Projection}_{t} = \text{Cash Flow}_{t-1} \cdot (1 + \text{Growth Rate})
$$

$$
\text{Terminal Value} = \text{Last Cash Flow Projection} \cdot (1 + \text{Perpetual Growth Rate}) / (\text{Weighted Average Cost of Capital} - \text{Perpetual Growth Rate})
$$

$$
\text{Enterprise Value} = \text{Sum of Present Value of Cash Flow Projections} + \text{Terminal Value} / (1 + \text{Weighted Average Cost of Capital}) ^{\text{Periods}}
$$

$$
\text{Equity Value} = \text{Enterprise Value} - \text{Total Debt} + \text{Cash and Cash Equivalents} + \text{Short Term Investments}
$$

$$
\text{Intrinsic Value} = \text{Equity Value} / \text{Weighted Average Shares Diluted}
$$

The base cash flow is by default the Free Cash Flow to the Firm (see `get_free_cash_flow_to_firm`), the cash flow available to both debt and equity holders. That is the cash flow the Weighted Average Cost of Capital discounts into an Enterprise Value, from which the debt is then subtracted.

In a five-year DCF the discounted terminal value is often 60% to 80% of the enterprise value, so the result is driven mostly by the gap between the WACC and the perpetual growth rate. Practitioners therefore show the intrinsic value as a range over several WACC and growth assumptions rather than a single number, and keep the perpetual growth rate at or below long-run nominal GDP growth.

**Also known as:** DCF, discounted cash flow, fair value, intrinsic value.

**Args:**

- <u>growth_rate (float, list or dict):</u> The growth rate to use for the cash flow projections. Can be one number
to use for all tickers, or a list or dict that contains a growth rate for each ticker.
- <u>perpetual_growth_rate (float, list or dict):</u> The perpetual growth rate to use for the terminal value.
Can be one number to use for all tickers, or a list or dict that contains a perpetual growth rate for
each ticker.
- <u>weighted_average_cost_of_capital (float, list or dict):</u> The weighted average cost of capital used to
discount the projected cash flows and to calculate the terminal value. Can be one number to use for
all tickers, or a list or dict that contains a weighted average cost of capital for each ticker.
- <u>periods (int, optional):</u> The number of periods to use for the cash flow projections. Defaults to 5.
- <u>cash_flow_type (str, optional):</u> The type of cash flow to use for the cash flow projections.
Defaults to "Free Cash Flow to Firm". The other options are "Free Cash Flow" and "Operating
Cash Flow" as reported on the cash flow statement; both are after interest, so discounting
them at the WACC and subtracting the debt counts the cost of debt twice.
- <u>trailing (int &#124; None, optional):</u> The number of trailing periods to sum for the base cash flow.
When set, uses the sum of the last N periods instead of only the most recent period. Defaults to
None, which uses 4 (the trailing twelve months) with quarterly data and the most recent year with
yearly data.
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.

**Returns:**

pd.DataFrame: DataFrame containing the intrinsic value for each ticker.

**Notes:**

- The results are highly dependent on the input. Therefore, think carefully about each input parameter to
ensure the results are accurate (given your beliefs)
- The growth rate, perpetual growth rate and WACC are annual rates, so the base cash flow is an annual
one: with quarterly data the last four quarters are summed. Setting `trailing` with yearly data sums
several years into one base cash flow, which logs a warning.
- The WACC must be greater than the perpetual growth rate; otherwise the terminal value is infinite
and the valuation is not calculated.
- The Total Debt, Cash and Cash Equivalents and Short Term Investments are those of the most
recent period. Short Term Investments are added back with the cash, the same cash and marketable
securities `get_enterprise_value_breakdown` deducts, and count as 0 when the balance sheet has no
such row.
- The Equity Value is divided by the Weighted Average Shares Diluted of the most recent period.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["ADBE", "CRM", "INTU"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_intrinsic_valuation(
    growth_rate=0.08,
    perpetual_growth_rate=0.025,
    weighted_average_cost_of_capital=0.09,
).xs("Intrinsic Value", level=1)
```

Which returns:

|      |   Periods = 5 |
|:-----|--------------:|
| ADBE |       389.526 |
| CRM  |       190.408 |
| INTU |       304.583 |

---

## get_free_cash_flow_to_firm
Free Cash Flow to the Firm (FCFF) is the cash flow available to all providers of capital, both debt and equity holders, after the company has paid all of its operating expenses and invested in the assets needed to sustain its operations. Because it is measured before any financing cash flows, FCFF is capital-structure neutral, making it the cash flow base typically discounted at the Weighted Average Cost of Capital (WACC) when valuing the Enterprise Value of a company directly.

The formula is as follows:

$$
\text{NOPAT} = \text{EBIT} \cdot (1 - \text{Corporate Tax Rate})
$$

$$
\text{FCFF} = \text{NOPAT} + \text{Depreciation and Amortization} - \text{Capital Expenditure} - \text{Change in Net Working Capital}
$$

**Also known as:** FCFF, unlevered free cash flow.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. Defaults to None.
- <u>show_columns (list[str] &#124; None, optional):</u> List of columns to show in the results. If None, all
columns will be shown. Defaults to None.

**Returns:**

pd.DataFrame: DataFrame containing the FCFF and its components.

**Notes:**

- EBIT is the reported Operating Income, as in the Altman Z-Score and Economic Value
Added calculations elsewhere in this module.
- The Corporate Tax Rate is the effective tax rate (Income Tax Expense / Income Before Tax)
kept within 0 and 1, and 0 for a period without a pre-tax profit, the same rate the
Weighted Average Cost of Capital uses (see `get_weighted_average_cost_of_capital`).
- The Capital Expenditure and Change in Working Capital line items from the cash flow
statement are stored using a cash-flow-impact sign convention (a use of cash is
negative). This method negates them internally so that they represent positive
magnitudes (amount spent / amount of the increase), matching the standard academic
FCFF formula. See `get_free_cash_flow_to_firm` in the Intrinsic module for details.
- FCFF is the default base cash flow of `get_intrinsic_valuation`, which discounts it
at the Weighted Average Cost of Capital.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["XOM", "CVX"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_free_cash_flow_to_firm().xs("Free Cash Flow to Firm", level=1)
```

Which returns:

|     |        2021 |        2022 |        2023 |        2024 |        2025 |
|:----|------------:|------------:|------------:|------------:|------------:|
| CVX | 1.98409e+10 | 3.51075e+10 | 2.2617e+10  | 1.97109e+10 | 1.16812e+10 |
| XOM | 3.08399e+10 | 5.28525e+10 | 2.78286e+10 | 2.68446e+10 | 1.83253e+10 |

---

## get_free_cash_flow_to_equity
Free Cash Flow to Equity (FCFE) is the cash flow available to a company's common equity holders after all operating expenses, reinvestment needs, and net payments to (or from) debt holders have been accounted for. Unlike FCFF, FCFE is a levered cash flow measure and should be discounted at the Cost of Equity, not the Weighted Average Cost of Capital, when used to value equity directly.

The formula is as follows:

$$
\text{FCFE} = \text{Net Income} + \text{Depreciation and Amortization} - \text{Capital Expenditure} - \text{Change in Net Working Capital} + \text{Net Borrowing}
$$

**Also known as:** FCFE, levered free cash flow.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. Defaults to None.
- <u>show_columns (list[str] &#124; None, optional):</u> List of columns to show in the results. If None, all
columns will be shown. Defaults to None.

**Returns:**

pd.DataFrame: DataFrame containing the FCFE and its components.

**Notes:**

- The Capital Expenditure and Change in Working Capital line items from the cash flow
statement are stored using a cash-flow-impact sign convention (a use of cash is
negative). This method negates them internally so that they represent positive
magnitudes, matching the standard academic FCFE formula. Net Debt Issued (used as
Net Borrowing) is already reported using the cash-flow-impact convention (a positive
value means the company was a net borrower) and is therefore used as-is.
- FCFE is the natural cash-flow-based counterpart to Residual Income
(`get_residual_income`) for equity-only valuation, in the same way FCFF is the
counterpart to Economic Value Added for firm-level valuation.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["CMCSA", "CHTR", "VZ"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_free_cash_flow_to_equity().xs("Free Cash Flow to Equity", level=1)
```

Which returns:

|       |       2021 |       2022 |       2023 |        2024 |       2025 |
|:------|-----------:|-----------:|-----------:|------------:|-----------:|
| CHTR  | 1.5532e+10 | 1.1e+10    | 1.955e+09  | -1.31e+09   | 2.43e+09   |
| CMCSA | 6.168e+09  | 3.618e+09  | 1.1394e+10 |  1.6448e+10 | 2.1732e+10 |
| VZ    | 3.9649e+10 | 1.5507e+10 | 8.042e+09  |  1.0354e+10 | 2.3559e+10 |

---

## get_gorden_growth_model
The Gordon Growth Model, also known as the Dividend Discount Model (DDM) with Constant Growth, is a method used to estimate the intrinsic value of a stock based on its expected future dividends. The model assumes that dividends will grow at a constant rate indefinitely.

The formula is as follows:

$$
\text{Intrinsic Value} = (\text{Dividends Per Share} \cdot (1 + \text{Growth Rate})) / (\text{Rate of Return} - \text{Growth Rate})
$$

The formula essentially discounts the future expected dividends to their present value, taking into account the required rate of return and the growth rate. The numerator represents the expected dividend in the next period. The denominator represents the required rate of return minus the growth rate.

Investors often use the Gordon Growth Model to compare the intrinsic value of a stock with its current market price. If the intrinsic value is higher than the market price, some investors may interpret it as an indication that the stock is undervalued.

It's important to note that the Gordon Growth Model is based on several assumptions, including the assumption of constant growth in dividends. It is most applicable to mature companies with stable and predictable dividend growth. If a company's dividend growth is expected to fluctuate or if it does not pay dividends, alternative valuation models may be more appropriate.

The assumption of constant growth of dividends is often unrealistic. In reality, dividends may fluctuate or even be suspended. Therefore, the Gordon Growth Model should be used with caution and in conjunction with other valuation methods.

**Also known as:** Gordon Growth Model, DDM, dividend discount model, GGM.

**Args:**

- <u>rate_of_return (float):</u> The required rate of return.
- <u>growth_rate (float):</u> The growth rate of the dividends.
- <u>project_periods (int, optional):</u> The number of years to project the intrinsic value for, beyond the
last complete period. Defaults to 5.
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.

**Returns:**

pd.DataFrame: DataFrame containing the intrinsic value for each ticker over time.

**Notes:**

- The results are highly dependent on the input. Therefore, think carefully about each input parameter to
ensure the results are accurate (given your beliefs)
- The rate of return and the growth rate are annual rates, so the model values an annual dividend:
the Dividends per Share of each year, or with quarterly data the sum of the trailing four complete
quarters. The first three quarters of quarterly data lack a full trailing year and are left out.
- Each historical period is valued off that period's *actual* annual Dividends per Share, and only
the years beyond the last complete period are projected forward at the given growth rate, one year
per projection period (four quarters apart with quarterly data). With yearly data the current,
unfinished year is projected as well, since its dividends so far cover only part of it. The first
year of the historical window will often be understated, since it only covers the part of the year
that falls inside the requested date range and so captures only part of the year's dividends. Use a
start_date at least one full year before the first period you intend to read.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["KO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_gorden_growth_model(rate_of_return=0.08, growth_rate=0.04)
```

Which returns:

|      |      KO |
|:-----|--------:|
| 2021 | 43.68   |
| 2022 | 45.76   |
| 2023 | 47.84   |
| 2024 | 50.44   |
| 2025 | 53.04   |
| 2026 | 55.1616 |
| 2027 | 57.3681 |
| 2028 | 59.6628 |
| 2029 | 62.0493 |
| 2030 | 64.5313 |

---

## get_two_stage_dividend_discount_model
The Two-Stage Dividend Discount Model extends the (single-stage) Gordon Growth Model to companies that are not expected to grow at a constant rate forever. It explicitly projects and discounts dividends over an initial high-growth phase, and then values everything from the end of that phase onward as a perpetuity growing at a lower, more sustainable stable rate (a Gordon Growth terminal value).

The formula is as follows:

$$
\text{Dividend Projection}_{t} = \text{Dividends Per Share} \cdot (1 + \text{High Growth Rate}) ^{t}
$$

$$
\text{High-Growth Phase Present Value} = \text{Sum of Dividend Projection}_{t} / (1 + \text{Rate of Return}) ^{t},\;\; \text{for} \;\; t = 1,\;\; \text{...},\;\; \text{High Growth Periods}
$$

$$
\text{Terminal Value} = \text{Last Dividend Projection} \cdot (1 + \text{Stable Growth Rate}) / (\text{Rate of Return} - \text{Stable Growth Rate})
$$

$$
\text{Intrinsic Value} = \text{High-Growth Phase Present Value} + (\text{Terminal Value} / (1 + \text{Rate of Return}) ^{\text{High}} \text{Growth Periods})
$$

**Also known as:** two-stage DDM, two-stage dividend discount model.

**Args:**

- <u>rate_of_return (float, list or dict):</u> The required rate of return (discount rate)
used to discount both phases. Can be one number to use for all tickers, or a list
or dict that contains a rate of return for each ticker.
- <u>high_growth_rate (float, list or dict):</u> The constant growth rate applied to
dividends during the explicit high-growth phase. Can be one number to use for all
tickers, or a list or dict that contains a high growth rate for each ticker.
- <u>stable_growth_rate (float, list or dict):</u> The perpetual (terminal) growth rate
applied to dividends from the end of the high-growth phase onward. Can be one
number to use for all tickers, or a list or dict that contains a stable growth
rate for each ticker.
- <u>high_growth_periods (int, optional):</u> The number of years in the explicit
high-growth phase. Defaults to 5.
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.

**Returns:**

pd.DataFrame: DataFrame containing the intrinsic value and its components for
each ticker.

**Notes:**

- The results are highly dependent on the input. Therefore, think carefully about
each input parameter to ensure the results are accurate (given your beliefs).
- The Rate of Return must be greater than the Stable Growth Rate, otherwise the
Terminal Value formula divides by a non-positive number.
- The base dividend used for the projection is the annual Dividends Per Share of the last complete
period for each ticker: the last complete year, or with quarterly data the sum of the last four
complete quarters, since the rates are annual and each projection period is a year. The current,
unfinished period is left out since its dividends so far cover only part of it. For companies that
do not pay a dividend, this model is not meaningful (the projections and resulting intrinsic value
will be zero).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["JNJ", "PG", "PEP"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_two_stage_dividend_discount_model(
    rate_of_return=0.08,
    high_growth_rate=0.06,
    stable_growth_rate=0.03,
).xs("Intrinsic Value", level=1)
```

Which returns:

|     |   High-Growth Periods = 5 |
|:----|--------------------------:|
| JNJ |                  120.743  |
| PEP |                  132.078  |
| PG  |                   98.1193 |

---

## get_residual_income
Residual Income is a measure of the profit a company generates in excess of the return required by its equity holders. It is the equity-side counterpart to Economic Value Added (EVA), and underpins the Residual Income Model, an alternative equity valuation lens to a traditional Discounted Cash Flow (DCF) that is particularly useful when a company's free cash flows are negative or unpredictable but its accounting earnings are more stable.

The formula is as follows:

$$
\text{Residual Income}_{t} = \text{Net Income}_{t} - (\text{Cost of Equity} \cdot \text{Book Value of Equity}_{t-1})
$$

**Also known as:** RI, economic profit (equity variant), abnormal earnings.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. Defaults to None.
- <u>market_risk_premium (float &#124; None, optional):</u> The annual equity risk premium the Cost of Equity
uses. Defaults to None, which takes the benchmark's average return above the risk-free rate
over every period of the data.
- <u>show_columns (list[str] &#124; None, optional):</u> List of columns to show in the results. If None, all
columns will be shown. Defaults to None.

**Returns:**

pd.DataFrame: DataFrame containing the Residual Income and its components.

**Notes:**

- A positive Residual Income indicates that the company generated more profit than
equity holders required given the capital they have invested. A negative Residual
Income indicates the company failed to earn its equity holders' required return, even
if it still reported a positive Net Income.
- The Cost of Equity follows from the Capital Asset Pricing Model (CAPM), as in
`get_weighted_average_cost_of_capital`: the risk-free rate of the period plus Beta times
the market risk premium, by default the benchmark's average return above the risk-free
rate over the data (see `market_risk_premium`). It covers the span of the Net Income: a
quarter with quarterly data, and the per-period rate times `trailing` when the Net Income
is a trailing sum (an annual rate for trailing twelve months, trailing=4 with quarterly data).
- The Book Value of Equity is the Total Shareholder Equity minus Preferred Stock at the
beginning of the period (the previous period's closing balance, or that of `trailing` periods
back with `trailing` set), the capital the shareholders had invested while the Net Income was
earned. Preferred equity is excluded since Residual Income (like Net Income) belongs to common
equity holders only.

References:
- Ohlson, James A. "Earnings, Book Values, and Dividends in Equity Valuation."
Contemporary Accounting Research, Vol. 11, No. 2, 1995, pp. 661-687.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["V", "MA", "AXP"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2022-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_residual_income().xs("Residual Income", level=1)
```

Which returns:

|     |        2022 |        2023 |        2024 |        2025 |
|:----|------------:|------------:|------------:|------------:|
| AXP | 2.05135e+09 | 1.68244e+09 | 3.53878e+09 | 1.9205e+09  |
| MA  | 8.21049e+09 | 9.901e+09   | 1.17405e+10 | 1.37721e+10 |
| V   | 7.63433e+09 | 1.11901e+10 | 1.3996e+10  | 1.28472e+10 |

---

## get_altman_z_score
Calculates the Altman Z-Score, a financial metric used to predict the likelihood of a company going bankrupt. The Altman Z-Score is calculated using several financial ratios, including working capital to total assets, retained earnings to total assets, earnings before interest and taxes (EBIT) to total assets, market value of equity to book value of total liabilities, and sales to total assets.

The formula is as follows:

$$
\text{Working Capital to Total Assets} = \text{Working Capital} / \text{Total Assets}
$$

$$
\text{Retained Earnings to Total Assets} = \text{Retained Earnings} / \text{Total Assets}
$$

$$
\text{EBIT to Total Assets} = \text{EBIT} / \text{Total Assets}
$$

$$
\text{Market Value to Total Liabilities} = \text{Market Value of Equity} / \text{Total Liabilities}
$$

$$
\text{Sales to Total Assets} = \text{Sales} / \text{Total Assets}
$$

$$
\text{Altman Z-Score} = 1.2 \cdot \text{Working Capital to Total Assets} + 1.4 \cdot \text{Retained Earnings to Total Assets} + 3.3 \cdot \text{EBIT to Total Assets} + 0.6 \cdot \text{Market Value to Total Liabilities} + 1.0 \cdot \text{Sales to Total Assets}
$$

The Altman Z-Score can be interpreted as follows:

- A Z-Score of less than 1.81 indicates a high likelihood of bankruptcy.
- A Z-Score between 1.81 and 2.99 indicates a gray area.
- A Z-Score of greater than 2.99 indicates a low likelihood of bankruptcy.

The original Z-Score was estimated on US listed manufacturers, and its thresholds are not meant for banks, insurers or most service companies; Altman's later Z'' variant drops the sales term for non-manufacturers. Share buybacks charged to retained earnings and accumulated losses both lower the retained earnings term, so a company that returns most of its earnings scores lower without being closer to distress, which is why the score is best read as a trend and next to the market-based term.

**Also known as:** Altman Z-score, bankruptcy prediction, financial distress score.

**Args:**

- <u>diluted (bool, optional):</u> Whether to use diluted shares outstanding in the calculation. Defaults to True.
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. Defaults to None.
- <u>show_columns (list[str] &#124; None, optional):</u> Restrict the result to these columns. Defaults to None,
which shows all columns.

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
- EBIT is the reported Operating Income, as in the EBIT based ratios of the Ratios module.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["BA", "LMT", "GD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_altman_z_score().xs("Altman Z-Score", level=1)
```

Which returns:

|     |   2021 |   2022 |   2023 |   2024 |   2025 |
|:----|-------:|-------:|-------:|-------:|-------:|
| BA  | 1.4229 | 1.3175 | 1.5588 | 1.0004 | 1.5145 |
| GD  | 3.2646 | 3.4357 | 3.4691 | 3.6147 | 4.2102 |
| LMT | 4.1234 | 4.104  | 3.8137 | 3.5273 | 3.3165 |

---

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

Piotroski designed the F-Score to separate winners from losers among value stocks (high book-to-market), where scores of 8 or 9 marked the strongest companies and scores of 0 or 1 the weakest. Because most criteria compare this year with last year, the score measures the direction of change rather than the level of financial strength, and a single strong year after a weak one can score highly.

Following Piotroski (2000), the Return on Assets, the Operating Cash Flow in the accruals signal and the Asset Turnover are scaled by the total assets at the beginning of the period, while the leverage signal divides long-term debt by the average of the beginning and ending total assets.

The formula is as follows, where (t-1) is the same period a year earlier (the previous column on yearly data, four quarters back on quarterly data, so quarterly comparisons are year over year) and Beginning Total Assets are the total assets at the end of the previous period (`trailing` periods back when set, one year earlier with trailing=4 on quarterly data):

$$
\text{Return on Assets} (\text{ROA}) = \text{Net Income} / \text{Beginning Total Assets}
$$

$$
\text{Return on Assets Criteria} = 1 \;\text{if ROA} > 0,\;\; \text{else 0}
$$

$$
\text{Operating Cashflow Criteria} = 1 \;\text{if Operating Cash Flow} > 0,\;\; \text{else 0}
$$

$$
\text{Change in Return on Assets Criteria} = 1 \;\text{if ROA} (t) > \text{ROA} (t-1),\;\; \text{else 0}
$$

$$
\text{Accruals Criteria} = 1 \;\text{if Operating Cash Flow} / \text{Beginning Total Assets} > \text{ROA},\;\; \text{else 0}
$$

$$
\text{Average Total Assets} = (\text{Beginning Total Assets} + \text{Total Assets}) / 2
$$

$$
\text{Change in Leverage Criteria} = 1 \;\text{if Long Term Debt} / \text{Average Total Assets is lower than in} (t-1),\;\; \text{else 0}
$$

$$
\text{Change in Current Ratio Criteria} = 1 \;\text{if Total Current Assets} / \text{Total Current Liabilities is higher than in} (t-1),\;\; \text{else 0}
$$

$$
\text{Number of Shares Criteria} = 1 \;\text{if Common Stock Issued} = 0,\;\; \text{else 0}
$$

$$
\text{Gross Margin Criteria} = 1 \;\text{if} (\text{Revenue} - \text{Cost of Goods Sold}) / \text{Revenue is higher than in} (t-1),\;\; \text{else 0}
$$

$$
\text{Asset Turnover Criteria} = 1 \;\text{if Revenue} / \text{Beginning Total Assets is higher than in} (t-1),\;\; \text{else 0}
$$

$$
\text{Piotroski Score} = \text{SUM of the nine criteria} (0 \;\text{to}\; 9)
$$

With `trailing`, the flows (net income, operating cash flow, revenue, cost of goods sold and common stock issued) are summed over the trailing periods, while the balance sheet items (total assets, long term debt, current assets and current liabilities) are taken at the end of each period.

Please see Piotroski, Joseph D. "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers." Journal of Accounting Research, Vol. 38, Supplement, 2000, pp. 1-41.

**Also known as:** Piotroski F-score, financial strength, quality score.

**Args:**

- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. Defaults to None.
- <u>show_columns (list[str] &#124; None, optional):</u> List of columns to show in the results. If None, all columns
will be shown. Defaults to None.

**Returns:**

pd.DataFrame: DataFrame containing the Piotroski F-Score and its components.

Periods for which the financial statements have not been reported yet are returned as NaN
rather than being scored zero across the board.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["F", "GM", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_piotroski_score().xs("Piotroski Score", level=1)
```

Which returns:

|      |   2022 |   2023 |   2024 |   2025 |
|:-----|-------:|-------:|-------:|-------:|
| F    |      5 |      6 |      6 |      3 |
| GM   |      6 |      6 |      7 |      5 |
| TSLA |      8 |      3 |      4 |      5 |

---

## get_beneish_m_score
The Beneish M-Score is a probabilistic model, developed by Messod Beneish, that uses eight financial ratios derived from a company's financial statements to identify whether a company has manipulated its earnings. It is a natural companion to the Altman Z-Score and Piotroski F-Score, using the same normalized financial statements as its input.

The formula is as follows, where (t-1) is the same period a year earlier (the previous column on yearly data, four quarters back on quarterly data, so quarterly comparisons are year over year):

$$
\text{DSRI} (\text{Days Sales in Receivables Index}) = (\text{Net Receivables} / \text{Revenue}) (t) / (\text{Net Receivables} / \text{Revenue}) (t-1)
$$

$$
\text{GMI} (\text{Gross Margin Index}) = \text{Gross Margin} (t-1) / \text{Gross Margin} (t),\;\; \text{with Gross Margin} = (\text{Revenue} - \text{Cost of Goods Sold}) / \text{Revenue}
$$

$$
\text{AQI} (\text{Asset Quality Index}) = \text{Asset Quality} (t) / \text{Asset Quality} (t-1),\;\; \text{with Asset Quality} = 1 - (\text{Total Current Assets} + \text{Property},\; \text{Plant and Equipment}) / \text{Total Assets}
$$

$$
\text{SGI} (\text{Sales Growth Index}) = \text{Revenue} (t) / \text{Revenue} (t-1)
$$

$$
\text{DEPI} (\text{Depreciation Index}) = \text{Depreciation Rate} (t-1) / \text{Depreciation Rate} (t),\;\; \text{with Depreciation Rate} = \text{Depreciation and Amortization} / (\text{Depreciation and Amortization} + \text{Property},\; \text{Plant and Equipment})
$$

$$
\text{SGAI} (\text{SG\&A} \;\text{Expenses Index}) = (\text{SG\&A} \;\text{Expenses} / \text{Revenue}) (t) / (\text{SG\&A} \;\text{Expenses} / \text{Revenue}) (t-1)
$$

$$
\text{LVGI} (\text{Leverage Index}) = \text{Leverage} (t) / \text{Leverage} (t-1),\;\; \text{with Leverage} = (\text{Total Current Liabilities} + \text{Long Term Debt}) / \text{Total Assets}
$$

$$
\text{TATA} (\text{Total Accruals to Total Assets}) = (\text{Net Income} - \text{Operating Cash Flow}) / \text{Total Assets}
$$

$$
\text{M-Score} = - 4.84 + 0.92 \cdot \text{DSRI} + 0.528 \cdot \text{GMI} + 0.404 \cdot \text{AQI} + 0.892 \cdot \text{SGI} + 0.115 \cdot \text{DEPI} - 0.172 \cdot \text{SGAI} + 4.679 \cdot \text{TATA} - 0.327 \cdot \text{LVGI}
$$

With `trailing`, the flows are summed over the trailing periods, while the balance sheet items are taken at the end of each period.

The -1.78 threshold belongs to this eight-variable model; the five-variable version uses -2.22. Fast-growing companies are flagged more often because sales growth itself raises the score, and the model was estimated without financial companies and is not suited to banks and insurers, so a score above the threshold is a prompt to read the accounts, not a finding.

**Also known as:** Beneish M-Score, earnings manipulation score.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. Defaults to None.
- <u>show_columns (list[str] &#124; None, optional):</u> List of columns to show in the results. If None, all
columns will be shown. Defaults to None.

**Returns:**

pd.DataFrame: DataFrame containing the Beneish M-Score and its components.

**Notes:**

- A M-Score greater than -1.78 suggests that the company is likely to be an earnings
manipulator. A M-Score lower than -1.78 suggests the company is unlikely to be a manipulator.
- As with the Altman Z-Score and Piotroski F-Score, this is a probabilistic, not a
definitive, indicator and should be combined with further fundamental analysis.
- Every index compares the current period with the same period a year earlier, so the first
year of the results (one period on yearly data, four on quarterly data) has no M-Score.
- Total Accruals are Net Income minus Cash Flow from Operations, the cash flow form of
Beneish, Lee and Nichols (2013), rather than the balance sheet form of Beneish (1999).
- The Depreciation Index uses Depreciation and Amortization, since statements report the two
as one line, where Beneish (1999) uses depreciation alone.

References:
- Beneish, Messod D. "The Detection of Earnings Manipulation." Financial Analysts Journal,
Vol. 55, No. 5, 1999, pp. 24-36.
- Beneish, Messod D., Charles M. C. Lee, and D. Craig Nichols. "Earnings Manipulation and
Expected Returns." Financial Analysts Journal, Vol. 69, No. 2, 2013, pp. 57-82.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NFLX", "DIS", "CMCSA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_beneish_m_score().xs("Beneish M-Score", level=1)
```

Which returns:

|       |    2021 |    2022 |    2023 |    2024 |    2025 |
|:------|--------:|--------:|--------:|--------:|--------:|
| CMCSA | -2.6609 | -2.8625 | -2.661  | -2.6852 | -2.734  |
| DIS   | -2.5143 | -2.5357 | -2.6392 | -2.6963 | -2.595  |
| NFLX  | -1.6697 | -1.3345 | -2.5628 | -2.3319 | -2.1611 |

---

## get_ohlson_o_score
Calculates the Ohlson O-Score, a financial metric used to predict the likelihood of a company going bankrupt. Unlike the Altman Z-Score, which is built with multiple discriminant analysis, the O-Score's coefficients come from a fitted logistic regression (logit) model. This is why the two models are usually reported side by side rather than one being treated as a replacement for the other: the Z-Score is only meaningful compared against Altman's empirically derived threshold bands, while the O-Score is directly interpretable as a probability of bankruptcy once passed through the logistic transform.

The formula is as follows:

$$
\text{SIZE} = \ln(\text{Total Assets})
$$

$$
\text{TLTA} = \text{Total Liabilities} / \text{Total Assets}
$$

$$
\text{WCTA} = \text{Working Capital} / \text{Total Assets}
$$

$$
\text{CLCA} = \text{Current Liabilities} / \text{Current Assets}
$$

$$
\text{OENEG} = 1 \;\text{if Total Liabilities} > \text{Total Assets else}\; 0
$$

$$
\text{NITA} = \text{Net Income} / \text{Total Assets}
$$

$$
\text{FUTL} = \text{Operating Cash Flow} / \text{Total Liabilities}
$$

$$
\text{INTWO} = 1 \;\text{if Net Income was negative for the last two years else}\; 0
$$

$$
\text{CHIN} = (\text{Net Income} (t) - \text{Net Income} (t-1)) / (| \text{Net Income} (t) | + | \text{Net Income} (t-1) |)
$$

$$
\text{O-Score} = - 1.32 - 0.407 \cdot \text{SIZE} + 6.03 \cdot \text{TLTA} - 1.43 \cdot \text{WCTA} + 0.0757 \cdot \text{CLCA}
$$

$$
1.72 \cdot \text{OENEG} - 2.37 \cdot \text{NITA} - 1.83 \cdot \text{FUTL} + 0.285 \cdot \text{INTWO} - 0.521 \cdot \text{CHIN}
$$

$$
\text{Bankruptcy Probability} = 1 / (1 + e ^{- \text{O-Score}})
$$

The Ohlson O-Score can be interpreted as follows:

- Ohlson's (1980) original cutoff is a bankruptcy probability of 0.038 (3.8%), the threshold that minimized the sum of Type I and Type II misclassification errors on his sample. It is deliberately far below the naive 0.50 midpoint because bankruptcy is a rare event. Equivalently, in raw O-Score terms the cutoff sits at ln(0.038 / 0.962), i.e. approximately -3.23. Since this implementation omits Ohlson's price-level deflator, its scores sit about 2.6 below Ohlson's scale and this cutoff flags far too few companies (see the Notes).
- A higher probability indicates a higher likelihood of bankruptcy.

**Also known as:** Ohlson O-Score, bankruptcy prediction, financial distress score.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. Defaults to None.
- <u>show_columns (list[str] &#124; None, optional):</u> List of columns to show in the results. If None, all
columns will be shown. Defaults to None.

**Returns:**

pd.DataFrame: DataFrame containing the Ohlson O-Score, its bankruptcy probability, and its
components.

**Notes:**

- Ohlson's (1980) original SIZE term deflates Total Assets by the US GNP price-level index
(rebased to 1968), a US-specific 1970s macro series that isn't available in this toolkit and
isn't meaningful outside the original US sample. This implementation omits that deflator and
uses ln(Total Assets) in nominal terms instead. This lowers every O-Score by roughly 0.407 *
ln(price index); with the US price level of the 2020s at roughly six times its 1968 level (an
index of about 600 to 650), that is about 2.6. The resulting probabilities are therefore much
lower than in Ohlson's study and the 0.038 cutoff (-3.23) flags far too few companies; it
corresponds to roughly -5.8 on this scale. The *ranking* of companies relative to one another
within a given currency and period is unaffected.
- Ohlson's original FUTL term uses "Funds from Operations", an accounting-flow concept that
predates standardized cash flow statements. This implementation approximates Funds from
Operations with Operating Cash Flow, the standard simplification used in modern
reproductions of the O-Score.
- The Beneish M-Score, Altman Z-Score, Piotroski F-Score and Ohlson O-Score are natural
companions, using the same normalized financial statements as their input.
- As with the other bankruptcy and distress models, this is a probabilistic, not a
definitive, indicator and should be combined with further fundamental analysis.

References:
- Ohlson, James A. "Financial Ratios and the Probabilistic Prediction of Bankruptcy." Journal of
Accounting Research, Vol. 18, No. 1, 1980, pp. 109-131.

Note that the first period is NaN because the Change in Net Income and Negative Income
Indicator components require a prior period to compare against.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["CCL", "RCL", "NCLH"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_ohlson_o_score().xs("Ohlson O-Score", level=1)
```

Which returns:

|      |    2021 |    2022 |    2023 |    2024 |    2025 |
|:-----|--------:|--------:|--------:|--------:|--------:|
| CCL  | -5.7604 | -5.4419 | -6.2136 | -6.8358 | -6.78   |
| NCLH | -4.4192 | -4.1038 | -5.0639 | -5.269  | -4.9984 |
| RCL  | -4.9997 | -5.0496 | -6.2194 | -6.3642 | -6.6839 |

---

## get_zmijewski_score
Calculates the Zmijewski Score, a financial metric used to predict the likelihood of a company going bankrupt. It is a simpler, three-variable model compared to both the Altman Z-Score and the Ohlson O-Score, and is commonly used as a robustness check when those two models disagree, since it is estimated on a different sample and with a different statistical technique (a probit model rather than discriminant analysis or logistic regression).

The formula is as follows:

$$
\text{Net Income to Total Assets} = \text{Net Income} / \text{Total Assets}
$$

$$
\text{Total Liabilities to Total Assets} = \text{Total Liabilities} / \text{Total Assets}
$$

$$
\text{Current Assets to Current Liabilities} = \text{Current Assets} / \text{Current Liabilities}
$$

$$
X = - 4.336 - 4.513 \cdot \text{Net Income to Total Assets} + 5.679 \cdot \text{Total Liabilities to Total Assets}
$$

$$
0.004 \cdot \text{Current Assets to Current Liabilities}
$$

$$
\text{Bankruptcy Probability} = \Phi(X),\;\; \text{the standard normal cumulative distribution function}
$$

The Zmijewski Score can be interpreted as follows:

- A higher X (and therefore a higher bankruptcy probability) indicates a higher likelihood of financial distress.

**Also known as:** Zmijewski Score, ZFC score, bankruptcy prediction, financial distress score.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. Defaults to None.
- <u>show_columns (list[str] &#124; None, optional):</u> List of columns to show in the results. If None, all
columns will be shown. Defaults to None.

**Returns:**

pd.DataFrame: DataFrame containing the Zmijewski Score, its bankruptcy probability, and its
components.

**Notes:**

- Unlike the Ohlson O-Score, which uses a logistic (sigmoid) link to convert its score into
a probability, the Zmijewski Score uses a probit link (the standard normal CDF). Applying a
logistic transform to the Zmijewski Score instead would produce an incorrect probability.
- As with the Altman Z-Score, Piotroski F-Score, Beneish M-Score and Ohlson O-Score, this is
a probabilistic, not a definitive, indicator and should be combined with further fundamental
analysis.

References:
- Zmijewski, Mark E. "Methodological Issues Related to the Estimation of Financial Distress
Prediction Models." Journal of Accounting Research, Vol. 22, 1984, pp. 59-82.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["DAL", "UAL", "AAL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_zmijewski_score().xs("Zmijewski Score", level=1)
```

Which returns:

|     |   2021 |   2022 |   2023 |    2024 |    2025 |
|:----|-------:|-------:|-------:|--------:|--------:|
| AAL | 2.1018 | 1.8402 | 1.7502 |  1.6446 |  1.6755 |
| DAL | 1.017  | 0.7425 | 0.2026 | -0.0177 | -0.3885 |
| UAL | 1.0493 | 0.7082 | 0.4288 |  0.1763 |  0.0073 |

---

## get_springate_score
Calculates the Springate Score, a financial metric used to predict the likelihood of a company going bankrupt. It follows the same multiple discriminant analysis methodology as the Altman Z-Score, but was calibrated on a smaller, Canadian-firm sample using four financial ratios instead of five.

The formula is as follows:

$$
\text{Working Capital to Total Assets} = \text{Working Capital} / \text{Total Assets}
$$

$$
\text{EBIT to Total Assets} = \text{EBIT} / \text{Total Assets}
$$

$$
\text{EBT to Current Liabilities} = \text{Earnings Before Taxes} / \text{Total Current Liabilities}
$$

$$
\text{Sales to Total Assets} = \text{Sales} / \text{Total Assets}
$$

$$
\text{Springate Score} = 1.03 \cdot \text{Working Capital to Total Assets} + 3.07 \cdot \text{EBIT to Total Assets} + 0.66 \cdot \text{EBT to Current Liabilities} + 0.4 \cdot \text{Sales to Total Assets}
$$

The Springate Score can be interpreted as follows:

- A Springate Score of less than 0.862 indicates a high likelihood of bankruptcy.
- A Springate Score of greater than 0.862 indicates a low likelihood of bankruptcy.

**Also known as:** Springate Score, S-Score, bankruptcy prediction, financial distress score.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. Defaults to None.
- <u>show_columns (list[str] &#124; None, optional):</u> List of columns to show in the results. If None, all
columns will be shown. Defaults to None.

**Returns:**

pd.DataFrame: DataFrame containing the Springate Score and its components.

**Notes:**

- As with the Altman Z-Score, Piotroski F-Score, Beneish M-Score, Ohlson O-Score and
Zmijewski Score, this is a probabilistic, not a definitive, indicator and should be
combined with further fundamental analysis.
- EBIT is the reported Operating Income, as in the Altman Z-Score calculation elsewhere
in this module.

References:
- Springate, Gordon L.V. "Predicting the Possibility of Failure in a Canadian Firm."
Unpublished M.B.A. Research Project, Simon Fraser University, 1978.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["M", "KSS", "GAP"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_springate_score().xs("Springate Score", level=1)
```

Which returns:

|     |   2021 |   2022 |   2023 |   2024 |   2025 |
|:----|-------:|-------:|-------:|-------:|-------:|
| GAP | 0.8575 | 0.6249 | 0.9346 | 1.1942 | 1.1859 |
| KSS | 1.2226 | 0.5896 | 0.809  | 0.6373 | 0.759  |
| M   | 1.2937 | 1.1721 | 0.7495 | 0.9653 | 1.015  |

---

## get_grover_score
Calculates the Grover Score, a financial metric used to predict the likelihood of a company going bankrupt. It was developed by re-estimating the coefficients of a reduced-form Altman Z-Score and adding a Return on Assets term, using a sample that paired each of Altman's original bankrupt firms with a matched non-bankrupt firm from the same industry and year.

The formula is as follows:

$$
\text{Working Capital to Total Assets} = \text{Working Capital} / \text{Total Assets}
$$

$$
\text{EBIT to Total Assets} = \text{EBIT} / \text{Total Assets}
$$

$$
\text{Return on Assets} = \text{Net Income} / \text{Total Assets}
$$

$$
\text{Grover Score} = 1.65 \cdot \text{Working Capital to Total Assets} + 3.404 \cdot \text{EBIT to Total Assets} - 0.016 \cdot \text{Return on Assets} + 0.057
$$

The Grover Score can be interpreted as follows:

- A Grover Score of -0.02 or lower indicates a high likelihood of bankruptcy.
- A Grover Score of 0.01 or higher indicates a low likelihood of bankruptcy (per some secondary sources), leaving a gray area in between the two thresholds.

**Also known as:** Grover Score, G-Score, bankruptcy prediction, financial distress score.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. Defaults to None.
- <u>show_columns (list[str] &#124; None, optional):</u> List of columns to show in the results. If None, all
columns will be shown. Defaults to None.

**Returns:**

pd.DataFrame: DataFrame containing the Grover Score and its components.

**Notes:**

- As with the Altman Z-Score, Springate Score, Ohlson O-Score and Zmijewski Score,
this is a probabilistic, not a definitive, indicator and should be combined with
further fundamental analysis.
- EBIT is the reported Operating Income, as in the Altman Z-Score calculation elsewhere
in this module. Return on
Assets uses the point-in-time Total Assets balance (not averaged), matching the
original Grover (2001) specification.

References:
- Grover, Jeffrey S. "Validating the Grover Bankruptcy Model." Doctoral dissertation,
University of North Texas, 2003.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["F", "GM", "STLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_grover_score().xs("Grover Score", level=1)
```

Which returns:

|      |   2021 |   2022 |   2023 |   2024 |    2025 |
|:-----|-------:|-------:|-------:|-------:|--------:|
| F    | 0.2398 | 0.2688 | 0.2442 | 0.2194 |  0.1363 |
| GM   | 0.2379 | 0.2474 | 0.2157 | 0.2846 |  0.1825 |
| STLA | 0.477  | 0.5941 | 0.5796 | 0.2001 | -0.3018 |

---

## get_fulmer_h_score
Calculates the Fulmer H-Score, a financial metric used to predict the likelihood of a company going bankrupt. Unlike the Altman Z-Score, which was built on relatively large, listed manufacturing companies, the Fulmer H-Score was calibrated on a matched-pair sample of small, failed and non-failed U.S. companies, using nine financial ratios selected via step-wise multiple discriminant analysis.

The formula is as follows:

$$
V_{1} = \text{Retained Earnings} / \text{Total Assets}
$$

$$
V_{2} = \text{Revenue} / \text{Total Assets}
$$

$$
V_{3} = \text{Income Before Tax} (\text{EBT}) / \text{Total Equity}
$$

$$
V_{4} = \text{Operating Cash Flow} / \text{Total Liabilities}
$$

$$
V_{5} = \text{Total Debt} / \text{Total Assets}
$$

$$
V_{6} = \text{Total Current Liabilities} / \text{Total Assets}
$$

$$
V_{7} = \ln(\text{Total Assets} - \text{Goodwill and Intangible Assets})
$$

$$
V_{8} = (\text{Total Current Assets} - \text{Total Current Liabilities}) / \text{Total Liabilities}
$$

$$
V_{9} = \ln(\text{EBIT} / \text{Interest Expense}),\;\; \text{with EBIT the reported Operating Income}
$$

$$
\text{H-Score} = 5.528 \cdot V_{1} + 0.212 \cdot V_{2} + 0.073 \cdot V_{3} + 1.270 \cdot V_{4} - 0.120 \cdot V_{5} + 2.335 \cdot V_{6} + 0.575 \cdot V_{7} + 1.083 \cdot V_{8} + 0.894 \cdot V_{9} - 6.075
$$

With `trailing`, the flows are summed and the balance sheet items averaged over the trailing periods.

The Fulmer H-Score can be interpreted as follows:

- An H-Score of less than 0 predicts failure.
- An H-Score of greater than 0 predicts non-failure.

**Also known as:** Fulmer H-Score, H factor, bankruptcy prediction, financial distress score.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. Defaults to None.
- <u>show_columns (list[str] &#124; None, optional):</u> List of columns to show in the results. If None, all
columns will be shown. Defaults to None.

**Returns:**

pd.DataFrame: DataFrame containing the Fulmer H-Score and its components.

**Notes:**

- Because V7 and V9 involve a natural logarithm, periods where Tangible Total Assets
is zero or negative, where EBIT and Interest Expense do not share the same sign, or
where the company reports no Interest Expense at all, will produce NaN and therefore
no H-Score for that period. This is a structural limitation of the log-linear Fulmer
specification, not a bug — the same kind of limitation documented for the Graham
Number elsewhere in this toolkit.
- Because V7 uses an un-normalized dollar figure, the H-Score is sensitive to the
absolute scale of a company's total assets; treat results for very large companies
(far outside the small-firm sample the model was calibrated on) with additional
caution.
- EBIT is the reported Operating Income, as in the Altman Z-Score calculation elsewhere
in this module.
- As with the Altman Z-Score, Springate Score and Grover Score, this is a
probabilistic, not a definitive, indicator and should be combined with further
fundamental analysis.

References:
- Fulmer, John G., James E. Moon, Thomas A. Gavin, and Michael J. Erwin. "A
Bankruptcy Classification Model for Small Firms." Journal of Commercial Bank
Lending, Vol. 66, No. 11, 1984, pp. 25-37.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["DIS", "FOXA", "CMCSA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_fulmer_h_score().xs("Fulmer H-Score", level=1)
```

Which returns:

|       |    2021 |    2022 |    2023 |    2024 |    2025 |
|:------|--------:|--------:|--------:|--------:|--------:|
| CMCSA | 11.6317 | 11.6248 | 11.7028 | 11.8104 | 11.9431 |
| DIS   | 10.8945 | 11.5241 | 12.0105 | 12.4096 | 12.7101 |
| FOXA  | 10.9776 | 11.0388 | 10.9996 | 11.0274 | 11.8441 |

---

## get_present_value_of_growth_opportunities
The Present Value of Growth Opportunities (PVGO) is a financial metric that represents the present value of a company's future growth opportunities. It is calculated as the difference between the share price and the value of the company's current earnings as a perpetuity without growth, i.e. Earnings per Share divided by the Cost of Equity.

The formula is as follows:

$$
\text{PVGO} = \text{Stock Price} - \text{Earnings Per Share} / \text{Cost of Equity}
$$

**Also known as:** PVGO, growth value.

**Args:**

- <u>calculate_daily (bool, optional):</u> Whether to calculate the PVGO using daily historical data.
Defaults to False.
- <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
- <u>include_dividends (bool, optional):</u> Whether to deduct Preferred Dividends Paid from Net
Income when calculating the Earnings per Share, so that the earnings figure reflects what is
attributable to common shareholders only. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. Defaults to None.
- <u>market_risk_premium (float &#124; None, optional):</u> The annual equity risk premium the Cost of Equity
uses. Defaults to None, which takes the benchmark's average return above the risk-free rate
over every period of the data.
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: DataFrame containing the PVGO values.

**Notes:**

- The no-growth value (Earnings per Share / r) is discounted at the Cost of Equity, since both
the share price and the Earnings per Share are equity-only, per-share quantities (Brealey, Myers
and Allen, "Principles of Corporate Finance"; Bodie, Kane and Marcus, "Investments"). The Cost of
Equity is the CAPM Cost of Equity of `get_weighted_average_cost_of_capital`.
- The Cost of Equity uses the same `trailing` as the Earnings per Share, so both cover the same
span (with quarterly data, a quarter without `trailing` and a year with trailing=4).
- When the Earnings per Share is negative, the no-growth value is negative and the PVGO
exceeds the share price, which has no meaningful interpretation.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NVDA", "TXN", "ADI"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2022-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_present_value_of_growth_opportunities()
```

Which returns:

| Date   |     ADI |     NVDA |     TXN |
|:-------|--------:|---------:|--------:|
| 2022   | 144.669 |  14.2204 | 124.854 |
| 2023   | 174.632 |  46.6789 | 144.668 |
| 2024   | 203.027 | 128.862  | 169.902 |
| 2025   | 257.776 | 174.087  | 154.735 |

---

## get_sustainable_growth_rate
The Sustainable Growth Rate (SGR) is the maximum rate at which a company can grow its revenue, using internally generated funds only, without having to raise additional equity or increase its financial leverage.

The formula is as follows:

$$
\text{Return on Equity} = \text{Net Income} / \text{Total Equity at the beginning of the period}
$$

$$
\text{Retention Ratio} = 1 - \text{Dividend Payout Ratio}
$$

$$
\text{SGR} = \text{Return on Equity} \cdot \text{Retention Ratio}
$$

The SGR assumes the company keeps its leverage and pays out only through dividends. Companies that return cash mainly through share buybacks have a low payout ratio on paper and a return on equity inflated by a shrinking equity base, so their SGR overstates what they can fund internally.

**Also known as:** SGR, self-sustainable growth rate.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. Defaults to None.

**Returns:**

pd.DataFrame: DataFrame containing the Sustainable Growth Rate.

**Notes:**

- Growing faster than the SGR without external financing typically requires either
improving profitability, reducing the dividend payout, or increasing leverage.
- Following Higgins ("Analysis for Financial Management"), the Return on Equity is measured
on the equity at the beginning of the - <u>period (the previous period's closing balance, or that of
`trailing` periods back with `trailing` set):</u> the retained earnings then grow that equity by
exactly the SGR. The two forms are equal under the model's assumption that equity grows only
through retained earnings: with that assumption the SGR equals ROE * b / (1 - ROE * b) with the
Return on Equity measured on the ending equity. Share issuance, buybacks and other changes in
equity break the equality.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NKE", "LULU", "DECK"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_sustainable_growth_rate()
```

Which returns:

|      |   2021 |   2022 |   2023 |   2024 |   2025 |
|:-----|-------:|-------:|-------:|-------:|-------:|
| DECK | 0.3129 | 0.3359 | 0.4302 | 0.4584 | 0.4075 |
| LULU | 0.3812 | 0.312  | 0.4923 | 0.4288 | 0.3652 |
| NKE  | 0.3297 | 0.2001 | 0.2521 | 0.0637 | 0.0531 |

---

## get_internal_growth_rate
The Internal Growth Rate (IGR) is the maximum rate at which a company can grow its revenue using only its retained earnings, without raising any external financing (neither debt nor equity).

The formula is as follows:

$$
\text{Return on Assets} = \text{Net Income} / \text{Total Assets at the end of the period}
$$

$$
\text{Retention Ratio} = 1 - \text{Dividend Payout Ratio}
$$

$$
\text{IGR} = (\text{Return on Assets} \cdot \text{Retention Ratio}) / (1 - (\text{Return on Assets} \cdot \text{Retention Ratio}))
$$

**Also known as:** IGR.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. Defaults to None.

**Returns:**

pd.DataFrame: DataFrame containing the Internal Growth Rate.

**Notes:**

- The IGR is more conservative than the Sustainable Growth Rate (SGR) since it assumes
no additional debt is raised to fund growth, whereas the SGR assumes the company
maintains its current level of financial leverage.
- The Return on Assets is measured on the Total Assets at the end of the period, as in
Ross, Westerfield and Jaffe ("Corporate Finance"). Under the model's assumption that assets
grow only through retained earnings, the formula equals the Return on Assets on the beginning
Total Assets times the Retention Ratio, the growth the retained earnings add to the beginning
assets, consistent with the beginning-equity definition of the Sustainable Growth Rate. Assets
funded otherwise (new debt, equity or payables) break the equality.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["ADBE", "INTU", "ADSK"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_internal_growth_rate()
```

Which returns:

|      |   2021 |   2022 |   2023 |   2024 |   2025 |
|:-----|-------:|-------:|-------:|-------:|-------:|
| ADBE | 0.2151 | 0.2122 | 0.2229 | 0.2254 | 0.3188 |
| ADSK | 0.0613 | 0.0955 | 0.1006 | 0.1144 | 0.0991 |
| INTU | 0.1004 | 0.0489 | 0.0569 | 0.0639 | 0.0782 |

---

## get_graham_number
Calculate the Graham Number, a conservative estimate of a stock's fair value based on its earnings and book value, as devised by Benjamin Graham.

The Graham Number is intended as an upper bound on the price a defensive investor should pay for a stock. It is most meaningful for stable, profitable companies with positive book value - for companies with negative earnings or negative book value the result is not meaningful (the square root of a negative number is undefined and will show up as NaN).

The formula is as follows:

$$
\text{Graham Number} = \sqrt{22.5 x \;\text{Earnings per Share}\; x \;\text{Book Value per Share}}
$$

The constant 22.5 is Graham's limit of a price-to-earnings ratio of 15 times a price-to-book ratio of 1.5, so the Graham Number is the price at which the product of the two ratios reaches that limit. For companies whose value lies mostly in intangibles, or that buy back many shares, book value is small and the Graham Number sits far below the market price.

**Also known as:** Graham fair value.

**Args:**

- <u>diluted (bool, optional):</u> Whether to use diluted shares in the calculation. Defaults to True.
- <u>trailing (int &#124; None, optional):</u> The trailing period to use for the calculation. Defaults to None,
which uses 4 (the trailing twelve months of earnings) with quarterly data and a single period
with yearly data.
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: DataFrame containing the Graham Number values.

**Notes:**

- Graham's limits of 15 times earnings and 1.5 times book value refer to annual earnings, so
with quarterly data the Earnings per Share are the sum of the last four quarters by default.
- Earnings and Book Value per Share use the Weighted Average Shares Diluted (or the Weighted
Average Shares with diluted=False).
- Only the Earnings per Share are trailing: the earnings are a flow over the trailing periods,
divided by the average shares over those periods. The Book Value per Share is a stock, the Total
Shareholder Equity minus the Preferred Stock at the end of the period divided by the shares of
that period.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["BAC", "C", "WFC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_graham_number()
```

Which returns:

|     |     2021 |     2022 |    2023 |     2024 |     2025 |
|:----|---------:|---------:|--------:|---------:|---------:|
| BAC |  47.9904 |  46.3468 | 47.4941 |  50.4045 |  56.4118 |
| C   | 142.751  | 120.826  | 93.472  | 117.004  | 127.785  |
| WFC |  68.3912 |  55.5576 | 69.7188 |  74.7554 |  85.6834 |

---

## get_reverse_discounted_cash_flow
Calculate the growth rate the share price implies, a reverse Discounted Cash Flow (DCF). Instead of estimating growth to arrive at a value, it takes the current share price as given and solves for the yearly cash flow growth over the projection periods at which the DCF value per share equals that price. The answer is the market's expectation, which can then be compared with the company's history: an implied growth far above what the company has achieved signals optimism.

The DCF is the same as in `get_intrinsic_valuation`, by default on the Free Cash Flow to the Firm:

$$
\text{Cash Flow Projection}_{t} = \text{Cash Flow}_{t-1} \cdot (1 + \text{Implied Growth Rate})
$$

$$
\text{Terminal Value} = \text{Last Projection} \cdot (1 + \text{Perpetual Growth Rate}) / (\text{WACC} - \text{Perpetual Growth Rate})
$$

$$
\text{Equity Value} = \text{Present Value of Projections and Terminal Value} + \text{Cash} - \text{Total Debt}
$$

$$
\text{Implied Growth Rate solves Equity Value} / \text{Shares Outstanding} = \text{Share Price}
$$

For more information, see the following book:

- Mauboussin, M.J. and Rappaport, A. (2001). "Expectations Investing: Reading Stock Prices for Better Returns." Harvard Business School Press.

**Also known as:** reverse DCF, market-implied growth, expectations investing.

**Args:**

- <u>perpetual_growth_rate (float &#124; dict[str, float], optional):</u> The growth after the
projection periods, one number or a number per ticker. Defaults to 0.025.
- <u>weighted_average_cost_of_capital (float &#124; dict[str, float] &#124; None, optional):</u>
The discount rate, one number or a number per ticker. Defaults to None,
which uses the latest Weighted Average Cost of Capital of each company,
calculated over a year (the last 4 quarters with quarterly data) whatever
`trailing` the cash flows use, as the rate is a yearly one.
- <u>periods (int, optional):</u> The number of projection periods. Defaults to 5.
- <u>cash_flow_type (str, optional):</u> The cash flow to project: "Free Cash Flow to
Firm" (see `get_free_cash_flow_to_firm`), the cash flow to debt and equity
holders that the WACC discounts into an enterprise value; or "Free Cash Flow"
or "Operating Cash Flow" as reported, which are after interest (cash flows
to equity), so that discounting them at the WACC and subtracting the debt
counts the cost of debt twice. Defaults to "Free Cash Flow to Firm".
- <u>trailing (int &#124; None, optional):</u> Sum the cash flow over this many periods (e.g.
4 quarters) instead of taking the latest one. Defaults to None, which sums
the last 4 quarters (a trailing twelve months) for quarterly data and takes
the latest year otherwise, as the projection periods are years.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.

**Returns:**

pd.DataFrame: Per ticker the Share Price, the Cash Flow used, the Weighted
Average Cost of Capital, the Perpetual Growth Rate, the Implied Growth Rate and,
for comparison, the Historical Growth Rate (the compound annual growth of the
cash flow as used, so summed over `trailing` periods where set, from the first
to the latest reported period).

**Notes:**

- A negative cash flow, or a discount rate at or below the perpetual growth rate,
has no implied growth rate and gives NaN.
- The Historical Growth Rate counts four quarters as a year with quarterly data and
is NaN when the first or latest cash flow is not positive. The years are those
between the first and the latest cash flow on the calendar, and a trailing sum
that includes a missing period is NaN rather than one over more periods.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "NVDA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_reverse_discounted_cash_flow(weighted_average_cost_of_capital=0.09)
```

Which returns:

|      |   Share Price |   Cash Flow |   Weighted Average Cost of Capital |   Perpetual Growth Rate |   Implied Growth Rate |   Historical Growth Rate |
|:-----|--------------:|------------:|-----------------------------------:|------------------------:|----------------------:|-------------------------:|
| AAPL |        271.86 | 8.62639e+10 |                               0.09 |                   0.025 |                0.308  |                   0.0545 |
| MSFT |        483.62 | 7.0121e+10  |                               0.09 |                   0.025 |                0.333  |                   0.1183 |
| NVDA |        186.5  | 9.15284e+10 |                               0.09 |                   0.025 |                0.3182 |                   0.8976 |

---

## get_earnings_power_value
Calculate the Earnings Power Value (EPV), the value of a company's current earnings if they never grew. Bruce Greenwald uses it to separate what is known (today's earnings power) from what is speculative (growth): the operating margin is averaged over several years and applied to the latest yearly revenue, taxed, and capitalized at the cost of capital.

- Normalized Operating Income = Average Operating Margin * Latest Revenue
- NOPAT = Normalized Operating Income * (1 - Average Tax Rate)
- Earnings Power Value = NOPAT / WACC
- EPV per Share = (EPV + Cash - Total Debt) / Shares Outstanding

A share price well above the EPV per share means the market pays for growth, which only adds value when the company earns more than its cost of capital on it.

For more information, see the following book:

- Greenwald, B.C.N., Kahn, J., Sonkin, P.D. and van Biema, M. (2001). "Value Investing: From Graham to Buffett and Beyond." Wiley.

**Also known as:** EPV, no-growth value, Greenwald valuation.

**Args:**

- <u>weighted_average_cost_of_capital (float &#124; dict[str, float] &#124; None, optional):</u>
The discount rate, one number or a number per ticker. Defaults to None,
which uses the latest Weighted Average Cost of Capital of each company,
calculated over a year (the last 4 quarters with quarterly data) whatever
`trailing` the cash flows use, as the rate is a yearly one.
- <u>periods (int, optional):</u> The number of periods the operating margin and tax rate
are averaged over; with `trailing`, the number of trailing sums, `trailing`
calendar periods apart so that they do not overlap, counted back from the
latest reported one. A sum that includes a missing period is left out of
the average. Defaults to 5.
- <u>trailing (int &#124; None, optional):</u> Sum the revenue, operating income, taxes and
income before tax over this many periods (e.g. 4 quarters), so that the
margin is applied to a year of revenue. Defaults to None, which uses 4 (a
trailing twelve months) for quarterly data and the yearly figures otherwise.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.

**Returns:**

pd.DataFrame: Per ticker the Average Operating Margin, Normalized Operating
Income, Tax Rate, Normalized NOPAT, Weighted Average Cost of Capital, Earnings
Power Value, Equity Value, Earnings Power Value per Share, Share Price and the
Price to EPV ratio.

**Notes:**

- Maintenance capital expenditure is assumed to equal depreciation, so operating
income stands in for the cash the business could pay out without shrinking.
- With quarterly data and the default trailing twelve months, the margins of the
last five years are averaged and applied to the revenue of the last four quarters,
as with yearly data.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "KO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_earnings_power_value(weighted_average_cost_of_capital=0.08)
```

Which returns:

|      |   Average Operating Margin |   Normalized Operating Income |   Tax Rate |   Normalized NOPAT |   Weighted Average Cost of Capital |   Earnings Power Value |   Equity Value |   Earnings Power Value per Share |   Share Price |   Price to EPV |
|:-----|---------------------------:|------------------------------:|-----------:|-------------------:|-----------------------------------:|-----------------------:|---------------:|---------------------------------:|--------------:|---------------:|
| AAPL |                     0.3067 |                   1.27656e+11 |     0.1679 |        1.06229e+11 |                               0.08 |            1.32786e+12 |    1.25141e+12 |                          83.4015 |        271.86 |         3.2597 |
| KO   |                     0.2534 |                   1.21476e+10 |     0.1861 |        9.88662e+09 |                               0.08 |            1.23583e+11 |    8.66388e+10 |                          20.0878 |         69.91 |         3.4802 |
| MSFT |                     0.4314 |                   1.2153e+11  |     0.1636 |        1.01652e+11 |                               0.08 |            1.27066e+12 |    1.18871e+12 |                         159.238  |        483.62 |         3.0371 |

---

## get_monte_carlo_intrinsic_valuation
Calculate the distribution of the intrinsic value per share when the inputs of the Discounted Cash Flow model are uncertain. A single DCF value hides how sensitive it is to its assumptions; here the growth rate, the perpetual growth rate and the discount rate are drawn from normal distributions around their expected values in every simulation, and the DCF of `get_intrinsic_valuation` is calculated for each draw. The spread of the outcomes, and the probability that the value exceeds the share price, show how robust the conclusion is.

Draws in which the discount rate does not exceed the perpetual growth rate by at least half a percentage point are redrawn, as the terminal value is undefined there.

For more information, see the following book:

- Damodaran, A. (2012). "Investment Valuation: Tools and Techniques for Determining the Value of Any Asset." Wiley, 3rd edition, chapter 33 (probabilistic approaches).

**Also known as:** Monte Carlo DCF, probabilistic valuation, DCF simulation.

**Args:**

- <u>growth_rate (float &#124; dict[str, float]):</u> The expected yearly growth over the
projection periods, one number or a number per ticker.
- <u>growth_rate_volatility (float, optional):</u> The standard deviation of the growth
rate. Defaults to 0.02.
- <u>perpetual_growth_rate (float &#124; dict[str, float], optional):</u> The expected growth
after the projection periods. Defaults to 0.025.
- <u>perpetual_growth_rate_volatility (float, optional):</u> Its standard deviation.
Defaults to 0.005.
- <u>weighted_average_cost_of_capital (float &#124; dict[str, float] &#124; None, optional):</u>
The expected discount rate. Defaults to None, which uses the latest Weighted
Average Cost of Capital of each company, calculated over a year (the last 4
quarters with quarterly data) whatever `trailing` the cash flows use, as the
rate is a yearly one.
- <u>weighted_average_cost_of_capital_volatility (float, optional):</u> Its standard
deviation. Defaults to 0.01.
- <u>periods (int, optional):</u> The number of projection periods. Defaults to 5.
- <u>simulations (int, optional):</u> The number of simulations. Defaults to 10,000.
- <u>cash_flow_type (str, optional):</u> The cash flow to project: "Free Cash Flow to
Firm" (see `get_free_cash_flow_to_firm`), the cash flow to debt and equity
holders that the WACC discounts into an enterprise value; or "Free Cash Flow"
or "Operating Cash Flow" as reported, which are after interest (cash flows
to equity), so that discounting them at the WACC and subtracting the debt
counts the cost of debt twice. Defaults to "Free Cash Flow to Firm".
- <u>trailing (int &#124; None, optional):</u> Sum the cash flow over this many periods (e.g.
4 quarters) instead of taking the latest one. Defaults to None, which sums
the last 4 quarters (a trailing twelve months) for quarterly data and takes
the latest year otherwise, as the projection periods are years.
- <u>seed (int &#124; None, optional):</u> The seed of the random numbers, so that results
can be reproduced. Defaults to 0; None gives different draws every time.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.

**Returns:**

pd.DataFrame: Per ticker the Mean, Standard Deviation and the 5th, 25th, 50th,
75th and 95th Percentile of the value per share, the Share Price and the
Probability Undervalued (the share of simulations above the share price).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_monte_carlo_intrinsic_valuation(
    growth_rate=0.08, weighted_average_cost_of_capital=0.09
)
```

Which returns:

|      |    Mean |   Standard Deviation |   5th Percentile |   25th Percentile |   50th Percentile |   75th Percentile |   95th Percentile |   Share Price |   Probability Undervalued |
|:-----|--------:|---------------------:|-----------------:|------------------:|------------------:|------------------:|------------------:|--------------:|--------------------------:|
| AAPL | 113.466 |              24.52   |          82.0179 |           96.6542 |           109.564 |           125.871 |           158.283 |        271.86 |                    0.0004 |
| MSFT | 182.735 |              40.0623 |         131.353  |          155.267  |           176.361 |           203.002 |           255.96  |        483.62 |                    0.0002 |

---

## get_merton_distance_to_default
Calculate the distance to default and probability of default with the Merton (1974) structural credit model. Equity is seen as a call option on the company's assets with its debt as strike price: shareholders receive what is left after the debt is repaid. The market value and volatility of the assets, which cannot be observed, are solved from the market value and volatility of the equity:

$$
E = V N (d_{1}) - D e ^{- \text{rT}} N(d_{2})
$$

$$
\sigma_{E} E = N(d_{1}) \sigma_{V} V
$$

$$
\text{Distance to Default} = (\ln(V / D) + (r - \sigma_{V} ^{2} / 2) T) / (\sigma_{V} \;\text{sqrt} (T))
$$

$$
\text{Probability of Default} = N(- \text{Distance to Default})
$$

where E is the market capitalization, σ_E the volatility of the share price over the year before, D the default point (short-term debt plus half of the long-term debt, the KMV convention), r the risk free rate and T the time horizon. The distance to default is the number of standard deviations the asset value is above the default point; it reacts to the share price immediately, long before a rating changes.

The risk free rate is the Toolkit's (the 10-year Treasury yield unless set otherwise with `risk_free_rate`) at every period end, where Vassalou and Xing (2004) and Bharath and Shumway (2008) use the one-year rate for a one-year horizon; the difference moves the distance to default only slightly.

For more information, see the following papers:

- Merton, R.C. (1974). "On the Pricing of Corporate Debt: The Risk Structure of Interest Rates." The Journal of Finance, 29(2), 449-470.
- Crosbie, P. and Bohn, J. (2003). "Modeling Default Risk." Moody's KMV.
- Vassalou, M. and Xing, Y. (2004). "Default Risk in Equity Returns." The Journal of Finance, 59(2), 831-868.
- Bharath, S.T. and Shumway, T. (2008). "Forecasting Default with the Merton Distance to Default Model." The Review of Financial Studies, 21(3), 1339-1369.

**Also known as:** KMV model, structural credit model, expected default frequency.

**Args:**

- <u>time_horizon (float, optional):</u> The horizon in years over which default is
measured. Defaults to 1.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (list[str] &#124; None, optional):</u> The periods to show. Defaults to None,
all periods.

**Returns:**

pd.DataFrame: Per ticker and period the Equity Value, Equity Volatility, Default
Point, Asset Value, Asset Volatility, Distance to Default and Probability of
Default (a decimal).

**Notes:**

- The probability is the model's risk-neutral probability; it ranks companies by
credit risk well but tends to understate the actual default rate of safe ones.
- Financial companies, whose debt is their raw material, are outside the model's
intended use.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["F", "AAPL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_merton_distance_to_default().loc["F"]
```

Which returns:

|                        |        2021 |        2022 |        2023 |        2024 |        2025 |
|:-----------------------|------------:|------------:|------------:|------------:|------------:|
| Equity Value           | 8.37862e+10 | 4.66828e+10 | 4.92598e+10 | 3.98079e+10 | 5.22045e+10 |
| Equity Volatility      | 0.4163      | 0.491       | 0.355       | 0.36        | 0.3319      |
| Default Point          | 9.3892e+10  | 9.45665e+10 | 9.945e+10   | 1.07294e+11 | 1.1133e+11  |
| Asset Value            | 1.76267e+11 | 1.3761e+11  | 1.44934e+11 | 1.42307e+11 | 1.58997e+11 |
| Asset Volatility       | 0.1979      | 0.1675      | 0.1207      | 0.1008      | 0.109       |
| Distance to Default    | 3.1592      | 2.3878      | 3.3814      | 3.2062      | 3.5969      |
| Probability of Default | 0.0008      | 0.0085      | 0.0004      | 0.0007      | 0.0002      |

---

## get_synthetic_credit_rating
Calculate a synthetic credit rating and the cost of debt that comes with it, from the interest coverage ratio (EBIT divided by interest expense), following Aswath Damodaran. Most companies have no traded bonds or rating of their own; the coverage ratio is the measure that explains ratings best, so it is mapped to the rating that companies with a similar ratio have, and to that rating's default spread over the risk free rate:

- Interest Coverage Ratio = EBIT / Interest Expense
- Rating and Default Spread from Damodaran's synthetic rating table
- Pre-tax Cost of Debt = Risk Free Rate + Default Spread

The table, with this year's default spreads, is read from Damodaran's website. Large and small companies use different coverage ranges, as smaller companies need a higher coverage for the same rating.

For more information, see the following book and data:

- Damodaran, A. (2012). "Investment Valuation." Wiley, 3rd edition, chapter 8.
- Damodaran, A. "Ratings, Interest Coverage Ratios and Default Spread." [https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ratings.html](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ratings.html){:target="_blank"}

**Also known as:** implied credit rating, interest coverage rating, cost of debt.

**Args:**

- <u>firm_type (str, optional):</u> The table to use: "large" (market capitalization above
five billion), "small" (smaller and riskier firms), "financial" (banks and
other financial firms) or "auto", which picks large or small from the market
capitalization of every period. Defaults to "auto".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (list[str] &#124; None, optional):</u> The periods to show. Defaults to None,
all periods.

**Returns:**

pd.DataFrame: Per ticker and period the Interest Coverage Ratio, Rating, Default
Spread, Risk Free Rate and Pre-tax Cost of Debt.

**Notes:**

- A company that reports an interest expense of zero gets the best rating; its
coverage ratio, which is infinite, shows as NaN. A period without a reported
interest expense gets no rating.
- A coverage ratio below the lowest bound of the table gets the worst rating.
- The market capitalization is compared with five billion in the reporting
currency; for companies that do not report in US dollars, pass the firm type.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["F", "AAPL", "T"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_synthetic_credit_rating()
```

Which returns:

|                                     | 2021     | 2022    | 2023    | 2024    | 2025    |
|:------------------------------------|:---------|:--------|:--------|:--------|:--------|
| ('AAPL', 'Interest Coverage Ratio') | 41.1905  | 40.7496 | 29.062  | nan     | nan     |
| ('AAPL', 'Rating')                  | Aaa/AAA  | Aaa/AAA | Aaa/AAA | Aaa/AAA | Aaa/AAA |
| ('AAPL', 'Default Spread')          | 0.004    | 0.004   | 0.004   | 0.004   | 0.004   |
| ('AAPL', 'Risk Free Rate')          | 0.0151   | 0.0388  | 0.0387  | 0.0457  | 0.0416  |
| ('AAPL', 'Pre-tax Cost of Debt')    | 0.0191   | 0.0428  | 0.0427  | 0.0497  | 0.0456  |
| ('F', 'Interest Coverage Ratio')    | 2.7915   | 5.0905  | 4.1306  | 4.5695  | 2.0191  |
| ('F', 'Rating')                     | Baa2/BBB | A2/A    | A3/A-   | A2/A    | Ba2/BB  |
| ('F', 'Default Spread')             | 0.0111   | 0.0078  | 0.0089  | 0.0078  | 0.0184  |
| ('F', 'Risk Free Rate')             | 0.0151   | 0.0388  | 0.0387  | 0.0457  | 0.0416  |
| ('F', 'Pre-tax Cost of Debt')       | 0.0262   | 0.0466  | 0.0476  | 0.0535  | 0.06    |
| ('T', 'Interest Coverage Ratio')    | 3.8675   | -0.7472 | 3.7011  | 3.5969  | 3.6743  |
| ('T', 'Rating')                     | A3/A-    | D2/D    | A3/A-   | A3/A-   | A3/A-   |
| ('T', 'Default Spread')             | 0.0089   | 0.19    | 0.0089  | 0.0089  | 0.0089  |
| ('T', 'Risk Free Rate')             | 0.0151   | 0.0388  | 0.0387  | 0.0457  | 0.0416  |
| ('T', 'Pre-tax Cost of Debt')       | 0.024    | 0.2288  | 0.0476  | 0.0546  | 0.0505  |

---

## get_peer_comparison
Compare every company with its peers on valuation, profitability, growth and leverage. For each metric it shows the company's latest value, the median and mean of its peers and the company's percentile among them (the share of peers with a lower value), which tells at a glance whether a company is expensive or cheap, and better or worse run, than comparable companies.

The metrics are the Price-to-Earnings, EV-to-EBITDA, Price-to-Book and Price-to-Sales ratios, the Gross, Operating and Net Profit Margin, the Return on Equity and on Invested Capital, Revenue Growth, the Debt-to-Equity ratio and the Dividend Yield, all of the latest fiscal year.

The Peer Mean of the four valuation multiples is the harmonic mean of the positive values, the standard average of multiples: the arithmetic mean is dominated by peers with earnings (or book value, or sales) close to zero, and a negative multiple says nothing about the price paid. The other metrics use the arithmetic mean.

For more information, see the following papers:

- Baker, M. and Ruback, R.S. (1999). "Estimating Industry Multiples." Working paper, Harvard University.
- Liu, J., Nissim, D. and Thomas, J. (2002). "Equity Valuation Using Multiples." Journal of Accounting Research, 40(1), 135-172.

**Also known as:** comparable companies analysis, comps, relative valuation, peer group analysis.

**Args:**

- <u>peers (dict[str, list[str]] &#124; None, optional):</u> The peers per ticker, e.g.
{"AAPL": ["MSFT", "GOOGL"]}. Defaults to None, which uses the peers
Financial Modeling Prep lists for each company (same sector and exchange,
similar size).
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.

**Returns:**

pd.DataFrame: Per ticker and metric the Company value, the Peer Median and Peer
Mean (harmonic for the valuation multiples), the Percentile (0 to 1) and the
number of Peers with a value.

**Notes:**

- A high percentile is not always good: for valuation ratios it means expensive,
for margins and returns it means strong.
- Retrieving the peers' financial statements takes a few seconds per peer.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_peer_comparison()
```

Which returns:

|                                        |   Company |   Peer Median |   Peer Mean |   Percentile |   Peers |
|:---------------------------------------|----------:|--------------:|------------:|-------------:|--------:|
| ('MSFT', 'Price-to-Earnings')          |   29.2276 |       30.5776 |     27.5171 |          0.5 |      10 |
| ('MSFT', 'EV-to-EBITDA')               |   20.7309 |       19.8087 |     17.9245 |          0.5 |      10 |
| ('MSFT', 'Price-to-Book')              |    8.8365 |        7.2576 |      6.1536 |          0.6 |      10 |
| ('MSFT', 'Price-to-Sales')             |   11.7803 |        6.1724 |      4.2807 |          0.9 |      10 |
| ('MSFT', 'Gross Margin')               |    0.6794 |        0.6242 |      0.6164 |          0.6 |      10 |
| ('MSFT', 'Operating Margin')           |    0.4678 |        0.1998 |      0.2226 |          1   |      10 |
| ('MSFT', 'Net Profit Margin')          |    0.4031 |        0.1682 |      0.187  |          1   |      10 |
| ('MSFT', 'Return on Equity')           |    0.3404 |        0.2392 |      0.287  |          0.6 |      10 |
| ('MSFT', 'Return on Invested Capital') |    0.209  |        0.1001 |      0.1434 |          0.8 |      10 |
| ('MSFT', 'Revenue Growth')             |    0.1779 |        0.1146 |      0.128  |          0.8 |      10 |
| ('MSFT', 'Debt-to-Equity')             |    0.2912 |        0.3313 |      0.7928 |          0.5 |      10 |
| ('MSFT', 'Dividend Yield')             |    0.0052 |        0.0088 |      0.0096 |          0.4 |      10 |

---

## get_magic_formula
Calculate Joel Greenblatt's Magic Formula ranking. Companies are ranked on two measures and the ranks are added; the lowest total combines a good business with a low price:

$$
\text{Earnings Yield} = \text{EBIT} / \text{Enterprise Value} (\text{how cheap the company is})
$$

$$
\text{Return on Capital} = \text{EBIT} / (\text{Net Working Capital} + \text{Net Fixed Assets}) (\text{how good the business is})
$$

Net working capital excludes cash and short-term debt, so the return on capital measures the operating business. The ranking is across the Toolkit's tickers, so pass the universe to choose from.

For more information, see the following book:

- Greenblatt, J. (2006). "The Little Book That Beats the Market." Wiley.

**Also known as:** Greenblatt formula, earnings yield and return on capital ranking.

**Args:**

- <u>diluted (bool, optional):</u> Whether to use the diluted share count for the market
capitalization. Defaults to True.
- <u>trailing (int &#124; None, optional):</u> Sum the operating income over this many
periods (e.g. 4 quarters, a trailing twelve months). The enterprise value and
the capital are taken at the period end. Defaults to None, which is 4 for
quarterly data (a year of operating income) and 1 otherwise.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (list[str] &#124; None, optional):</u> The periods to show. Defaults to None,
all periods.

**Returns:**

pd.DataFrame: Per ticker and period the Earnings Yield, Return on Capital, their
ranks and the Magic Formula Rank (1 is the most attractive).

**Notes:**

- With quarterly data and the default trailing twelve months, the first ranks are in
the fourth quarter of statements. When the statements cover fewer periods, the
result is empty and a warning names the number of periods needed; set an earlier
`start_date` to obtain the ranks.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "GOOGL", "META", "INTC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_magic_formula().xs("Magic Formula Rank", level=1)
```

Which returns:

|       |   2021 |   2022 |   2023 |   2024 |   2025 |
|:------|-------:|-------:|-------:|-------:|-------:|
| AAPL  |      2 |      1 |      1 |      2 |      2 |
| GOOGL |      4 |      2 |      2 |      1 |      4 |
| INTC  |      3 |      5 |      5 |      5 |      5 |
| META  |      1 |      2 |      2 |      4 |      2 |
| MSFT  |      5 |      4 |      4 |      2 |      1 |

---

## get_mohanram_g_score
Calculate Partha Mohanram's G-Score, a score from 0 to 8 that separates winners from losers among growth (low book-to-market) companies, where value measures such as the Piotroski F-Score say little. Each signal is 1 when the company does better than the median of its peers, the Toolkit's tickers:

- Profitability: return on assets (G1) and cash flow return on assets (G2) above the median, and cash flow above net income (G3).
- Naive extrapolation: a lower than median variance of the return on assets (G4) and of revenue growth (G5).
- Accounting conservatism: research and development (G6), capital expenditure (G7) and advertising (G8, selling and marketing expenses) relative to assets above the median, as these investments depress current earnings.

As in the paper, the return on assets, the cash flow return on assets and the three intensities are scaled by the total assets at the start of the year, the variances are taken over the past five years with at least three available, and a signal that cannot be calculated for a company (a missing item, or too short a history) scores 0.

For more information, see the following paper:

- Mohanram, P.S. (2005). "Separating Winners from Losers among Low Book-to-Market Stocks using Financial Statement Analysis." Review of Accounting Studies, 10, 133-170.

**Also known as:** G-Score, growth stock score.

**Args:**

- <u>variance_periods (int, optional):</u> The number of yearly values the variances of
G4 (return on assets) and G5 (revenue growth) are calculated over, of which at
least three (or all, when fewer are asked for) must be available. With
`trailing` the values are `trailing` periods apart (one a year with 4
quarters); without it, one per period. Defaults to 5, the five years of the
paper.
- <u>trailing (int &#124; None, optional):</u> Sum the flows over this many periods (e.g. 4
quarters, a trailing twelve months) and compare with the values `trailing`
periods back, so that with quarterly data every change is year over year.
Balance sheet items are taken at the period end. Defaults to None, which is
4 for quarterly data (a year) and 1 otherwise; pass 1 for quarterly data to
compare quarter over quarter.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (list[str] &#124; None, optional):</u> The periods to show. Defaults to None,
all periods.

**Returns:**

pd.DataFrame: Per ticker and period the eight signals and the G-Score.

**Notes:**

- The paper compares with industry medians; here the medians are those of the
tickers given, so pass a peer group of the same industry.
- The variances need three yearly values and revenue growth needs the year before
the first, so the first G-Score is in the fourth year of statements (with
quarterly data, the sixteenth quarter). A company with a shorter history than its
peers scores 0 on G4 and G5. When the statements cover fewer periods than that,
the result is empty and a warning names the number of periods needed; set an
earlier `start_date` to obtain the score.
- Net Income stands in for the net income before extraordinary items of the paper, as
the statements do not report extraordinary items separately.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "GOOGL", "META", "NVDA", "ADBE"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_mohanram_g_score().xs("G-Score", level=1)
```

Which returns:

|       |   2023 |   2024 |   2025 |
|:------|-------:|-------:|-------:|
| AAPL  |      4 |      4 |      3 |
| ADBE  |      5 |      5 |      5 |
| GOOGL |      4 |      4 |      6 |
| META  |      6 |      5 |      4 |
| MSFT  |      4 |      5 |      4 |
| NVDA  |      3 |      3 |      3 |

---

## get_dechow_f_score
Calculate the Dechow F-Score, the probability that a company's financial statements are misstated relative to the average company. It was estimated on companies the SEC charged with misstating their earnings, and combines:

- Accrual quality: RSST accruals (the change in non-cash working capital, non-current operating assets and financial assets), the changes in receivables and inventory, and the share of soft assets (assets other than cash and short-term investments and net property, plant and equipment).
- Performance: the change in cash sales and in return on assets.
- Incentives: whether the company issued long-term debt or stock.

Predicted Value = -7.893 + 0.790 RSST Accruals + 2.518 ΔReceivables + 1.191 ΔInventory + 1.979 Soft Assets + 0.171 ΔCash Sales - 0.932 ΔROA + 1.029 Issuance Probability = e^PV / (1 + e^PV), F-Score = Probability / 0.0037

An F-Score of 1 is average risk; above 1 the risk is elevated, above 1.85 substantial and above 2.45 high.

For more information, see the following paper:

- Dechow, P.M., Ge, W., Larson, C.R. and Sloan, R.G. (2011). "Predicting Material Accounting Misstatements." Contemporary Accounting Research, 28(1), 17-82.

**Also known as:** F-Score (Dechow), misstatement score, earnings manipulation probability.

**Args:**

- <u>trailing (int &#124; None, optional):</u> Sum the flows over this many periods (e.g. 4
quarters, a trailing twelve months) and compare with the values `trailing`
periods back, so that with quarterly data every change is year over year.
Balance sheet items are taken at the period end. Defaults to None, which is
4 for quarterly data (a year) and 1 otherwise; pass 1 for quarterly data to
compare quarter over quarter.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (list[str] &#124; None, optional):</u> The periods to show. Defaults to None,
all periods.

**Returns:**

pd.DataFrame: Per ticker and period the seven inputs, the Predicted Value, the
Probability of Misstatement and the F-Score.

**Notes:**

- The paper counts the gross issuance of long-term debt. Where the statements only
report the net issuance (issuance minus repayments), as Financial Modeling Prep's
do, a company that issued debt but repaid more counts as not issuing.
- The model was estimated on yearly statements, so with quarterly data the flows
are summed over the trailing twelve months by default.
- The changes compare with the year before and the change in return on assets with
the return a year back, so the first F-Score is in the third year of statements
(with quarterly data and the default trailing twelve months, the ninth quarter).
When the statements cover fewer periods, the result is empty and a warning names
the number of periods needed; set an earlier `start_date` to obtain the score.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "SMCI"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_dechow_f_score().xs("F-Score", level=1)
```

Which returns:

|      |   2022 |   2023 |   2024 |   2025 |
|:-----|-------:|-------:|-------:|-------:|
| AAPL | 0.4226 | 0.3916 | 0.4136 | 0.4214 |
| MSFT | 0.811  | 0.7759 | 1.018  | 0.8628 |
| SMCI | 2.8035 | 0.6471 | 6.128  | 0.8275 |

---

## get_montier_c_score
Calculate James Montier's C-Score, a count from 0 to 6 of warning signs that a company is "cooking the books". Each sign is 1 when present:

- A growing gap between net income and cash flow from operations.
- Rising days sales outstanding: receivables growing faster than sales.
- Rising days sales of inventory: inventory growing faster than cost of sales.
- Rising other current assets relative to revenue, a place to park costs.
- Falling depreciation relative to gross property, plant and equipment, which flatters earnings.
- Total asset growth above 10%, typical of serial acquirers.

Montier found that companies scoring 5 or 6 underperformed the market markedly.

For more information, see the following paper:

- Montier, J. (2008). "Cooking the Books, or, More Sailing Under the Black Flag." Société Générale, Mind Matters.

**Also known as:** C-Score, cooking the books score.

**Args:**

- <u>trailing (int &#124; None, optional):</u> Sum the flows over this many periods (e.g. 4
quarters, a trailing twelve months) and compare with the values `trailing`
periods back, so that with quarterly data every change is year over year.
Balance sheet items are taken at the period end. Defaults to None, which is
4 for quarterly data (a year) and 1 otherwise; pass 1 for quarterly data to
compare quarter over quarter.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (list[str] &#124; None, optional):</u> The periods to show. Defaults to None,
all periods.

**Returns:**

pd.DataFrame: Per ticker and period the six signals and the C-Score.

**Notes:**

- Gross property, plant and equipment is reported by Yahoo Finance but not by
Financial Modeling Prep; for a company without it, depreciation is compared with
the net amount, whose ratio also rises as the assets age and so can hide a decline.
- The signs compare with the year before, so the first C-Score is in the second year
of statements (with quarterly data and the default trailing twelve months, the
eighth quarter). When the statements cover fewer periods, the result is empty and a
warning names the number of periods needed; set an earlier `start_date` to obtain
the score.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "SMCI"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_montier_c_score().xs("C-Score", level=1)
```

Which returns:

|      |   2021 |   2022 |   2023 |   2024 |   2025 |
|:-----|-------:|-------:|-------:|-------:|-------:|
| AAPL |      4 |      2 |      3 |      2 |      3 |
| MSFT |      5 |      2 |      5 |      3 |      2 |
| SMCI |      3 |      5 |      2 |      5 |      2 |

---

## get_accruals_ratio
Calculate the accruals ratios: the part of earnings that is not backed by cash, relative to the average of the total assets at the start and the end of the year. Richard Sloan showed that earnings driven by accruals are less persistent than cash earnings and that companies with high accruals earn lower future returns (the accrual anomaly).

- Balance Sheet Accruals Ratio = [(ΔCurrent Assets - ΔCash) - (ΔCurrent Liabilities - ΔShort-term Debt - ΔTaxes Payable) - Depreciation] / Average Total Assets
- Cash Flow Accruals Ratio = (Net Income - Cash Flow from Operations - Cash Flow from Investing) / Average Total Assets

The balance sheet version is Sloan's (1996). The cash flow version, earnings minus free cash flow, takes the accruals from the cash flow statement instead: Hribar and Collins (2002) showed that balance sheet changes misstate accruals when a company acquires, divests or discontinues operations (their own measure is earnings before extraordinary items minus cash flow from operations), and subtracting the investing cash flow as well counts the investment in long-term operating assets as an accrual, as the broad accruals of Richardson, Sloan, Soliman and Tuna (2005) do. Values near zero or negative are a sign of high earnings quality.

For more information, see the following papers:

- Sloan, R.G. (1996). "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows about Future Earnings?" The Accounting Review, 71(3), 289-315.
- Hribar, P. and Collins, D.W. (2002). "Errors in Estimating Accruals: Implications for Empirical Research." Journal of Accounting Research, 40(1), 105-134.
- Richardson, S.A., Sloan, R.G., Soliman, M.T. and Tuna, I. (2005). "Accrual Reliability, Earnings Persistence and Stock Prices." Journal of Accounting and Economics, 39(3), 437-485.

**Also known as:** Sloan ratio, accrual ratio, earnings quality ratio.

**Args:**

- <u>trailing (int &#124; None, optional):</u> Sum the flows over this many periods (e.g. 4
quarters, a trailing twelve months) and compare with the values `trailing`
periods back, so that with quarterly data every change is year over year.
Balance sheet items are taken at the period end. Defaults to None, which is
4 for quarterly data (a year) and 1 otherwise; pass 1 for quarterly data to
compare quarter over quarter.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (list[str] &#124; None, optional):</u> The periods to show. Defaults to None,
all periods.

**Returns:**

pd.DataFrame: Per ticker and period the Balance Sheet Accruals Ratio and the Cash
Flow Accruals Ratio.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.models.get_accruals_ratio()
```

Which returns:

|                                          |    2021 |    2022 |    2023 |    2024 |    2025 |
|:-----------------------------------------|--------:|--------:|--------:|--------:|--------:|
| ('AAPL', 'Balance Sheet Accruals Ratio') | -0.1047 | -0.0446 | -0.0115 | -0.0285 | -0.108  |
| ('AAPL', 'Cash Flow Accruals Ratio')     |  0.0154 |  0      | -0.0489 | -0.0765 | -0.0405 |
| ('MSFT', 'Balance Sheet Accruals Ratio') | -0.0687 | -0.1109 | -0.0683 | -0.1017 | -0.0735 |
| ('MSFT', 'Cash Flow Accruals Ratio')     |  0.0381 |  0.0401 |  0.0192 |  0.144  |  0.0677 |

---

