---
title: Documentation
seo_title: Finance Toolkit Documentation
excerpt: This the documentation of the FinanceToolkit. This is an open-source toolkit in which 500+ financial methods are written down in the most simplistic way allowing for complete transparency of the calculation method.
description: "Documentation for the Finance Toolkit, an open-source Python package with 500+ transparent financial methods: a reference for every module and function."
author_profile: false
permalink: /projects/financetoolkit/docs
classes: wide-sidebar
layout: single
redirect_from:
    - /docs
    - /projects/financetoolkit/getting-started
sidebar:
    nav: "financetoolkit-docs"
---

These pages document the Finance Toolkit, an open-source toolkit in which all relevant financial methods (500+) are written down in the most simplistic way allowing for complete transparency of the calculation method. Each class has an introduction page like this one, and the sidebar leads to a page for every function that shows how to use it through the [Finance Toolkit MCP](/projects/financetoolkit/mcp) in an AI assistant and in Python. The Python examples are also embedded in the code. For simplicity sake, only the controller modules are included here given that the models themselves should be relatively straightforward. Make sure to also have a look at the [Getting Started](#getting-started) section below and the one that opens every module page.

The Toolkit Module is a collection of functions that collect and parse data, including historical data, fundamental data (balance, income and cash flow statements) and metrics from Financial Modeling Prep such as enterprise values, company profiles and more. From this module you can access all related sub-modules.

Use it in Claude, ChatGPT or another AI assistant through the [Finance Toolkit MCP](/projects/financetoolkit/mcp), or install the Python package:

```python
pip install financetoolkit -U
```

{% include algolia.html %}

{% include financetoolkit-getting-started/getting-started.md %}

## ratios
The Ratios Module contains over 50+ ratios that can be used to analyse companies. These ratios are divided into 5 categories which are efficiency, liquidity, profitability, solvency and valuation. Each ratio is calculated using the data from the Toolkit module.

Some examples of ratios are the Current Ratio, Debt to Equity Ratio, Return on Assets (ROA), Return on Equity (ROE), Return on Invested Capital (ROIC), Return on Capital Employed (ROCE), Price to Earnings Ratio (P/E), Price to Book Ratio (P/B), Price to Sales Ratio (P/S), Price to Cash Flow Ratio (P/CF), Price to Free Cash Flow Ratio (P/FCF), Dividend Yield and Dividend Payout Ratio.

Next to that, it is also possible to define custom ratios.

See the following link for more information: [https://www.jeroenbouma.com/projects/financetoolkit/docs/ratios](https://www.jeroenbouma.com/projects/financetoolkit/docs/ratios){:target="_blank"}


```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

profitability_ratios = toolkit.ratios.collect_profitability_ratios()

profitability_ratios.loc['AAPL']
```

Which returns:

|                                             |    2021 |    2022 |    2023 |     2024 |     2025 |
|:--------------------------------------------|--------:|--------:|--------:|---------:|---------:|
| Gross Margin                                |  0.4178 |  0.4331 |  0.4413 |   0.4621 |   0.4691 |
| Operating Margin                            |  0.2978 |  0.3029 |  0.2982 |   0.3151 |   0.3197 |
| Net Profit Margin                           |  0.2588 |  0.2531 |  0.2531 |   0.2397 |   0.2692 |
| EBITDA Margin                               |  0.3287 |  0.331  |  0.3283 |   0.3444 |   0.3478 |
| Free Cash Flow Margin                       |  0.2541 |  0.2826 |  0.2598 |   0.2783 |   0.2373 |
| Interest Coverage Ratio                     | 41.1905 | 40.7496 | 29.062  | nan      | nan      |
| Income Before Tax Profit Margin             |  0.2985 |  0.302  |  0.2967 |   0.3158 |   0.3189 |
| Effective Tax Rate                          |  0.133  |  0.162  |  0.1472 |   0.2409 |   0.1561 |
| Return on Assets                            |  0.2806 |  0.2836 |  0.275  |   0.2613 |   0.3093 |
| Cash Return on Assets                       |  0.3083 |  0.3471 |  0.3134 |   0.3296 |   0.3079 |
| Return on Equity                            |  1.4744 |  1.7546 |  1.7195 |   1.5741 |   1.7142 |
| Return on Invested Capital                  |  0.4879 |  0.5229 |  0.528  |   0.5166 |   0.6201 |
| Return on Capital Employed                  |  0.4831 |  0.6009 |  0.5514 |   0.6534 |   0.6872 |
| Return on Tangible Assets                   |  0.2806 |  0.2836 |  0.275  |   0.2613 |   0.3093 |
| Income Quality Ratio                        |  1.0988 |  1.2239 |  1.1397 |   1.2616 |   0.9953 |
| Net Income per EBT                          |  0.867  |  0.838  |  0.8528 |   0.7591 |   0.8439 |
| Free Cash Flow to Operating Cash Flow Ratio |  0.8935 |  0.9123 |  0.9009 |   0.9201 |   0.8859 |
| EBT to EBIT Ratio                           |  0.9764 |  0.976  |  0.9666 |   1      |   1      |
| EBIT to Revenue                             |  0.3058 |  0.3095 |  0.307  |   0.3158 |   0.3189 |
| Cash Tax Rate                               |  0.2324 |  0.1643 |  0.1642 |   0.2114 |   0.3267 |
| Tax Rate Divergence                         |  0.0994 |  0.0023 |  0.017  |  -0.0295 |   0.1706 |

---

## models
Gives access to the Models module. The Models module is meant to execute well-known models such as DUPONT and the Discounted Cash Flow (DCF) model. These models are also directly related to the data retrieved from the Toolkit module.

See the following link for more information: [https://www.jeroenbouma.com/projects/financetoolkit/docs/models](https://www.jeroenbouma.com/projects/financetoolkit/docs/models){:target="_blank"}


```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["TSLA", "AMZN"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    quarterly=True,
    start_date='2022-12-31',
    end_date="2025-12-31",
)

dupont_analysis = toolkit.models.get_extended_dupont_analysis()

dupont_analysis.loc['AMZN']
```

Which returns:

|                         |   2022Q4 |   2023Q1 |   2023Q2 |   2023Q3 |   2023Q4 |   2024Q1 |   2024Q2 |   2024Q3 |   2024Q4 |   2025Q1 |   2025Q2 |   2025Q3 |   2025Q4 |
|:------------------------|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|
| Interest Burden Ratio   |  -0.3467 |   0.863  |   0.9835 |   1.0891 |   1.0361 |   0.8426 |   1.0395 |   1.0358 |   1.0531 |   1.1779 |   1.0872 |   1.6127 |   1.0465 |
| Tax Burden Ratio        |  -0.2929 |   0.7699 |   0.8936 |   0.8108 |   0.7763 |   0.8087 |   0.8841 |   0.85   |   0.8959 |   0.79   |   0.8715 |   0.7541 |   0.8108 |
| Operating Profit Margin |   0.0183 |   0.0375 |   0.0572 |   0.0782 |   0.0777 |   0.1068 |   0.0992 |   0.1096 |   0.1129 |   0.1182 |   0.1143 |   0.0967 |   0.1171 |
| Asset Turnover          | nan      |   0.2748 |   0.2853 |   0.2967 |   0.335  |   0.2707 |   0.2726 |   0.2789 |   0.3105 |   0.2455 |   0.2531 |   0.2555 |   0.2761 |
| Equity Multiplier       | nan      |   3.0843 |   2.9152 |   2.7433 |   2.6367 |   2.5298 |   2.3963 |   2.2991 |   2.2188 |   2.1427 |   2.0721 |   2.0047 |   1.9802 |
| Return on Equity        | nan      |   0.0211 |   0.0418 |   0.0562 |   0.0552 |   0.0498 |   0.0595 |   0.0619 |   0.0734 |   0.0579 |   0.0568 |   0.0602 |   0.0543 |

---

## options
This gives access to the Options module. The Options Module is meant to provide Options valuations based on real market data. This includes the Black-Scholes model and in the future the Binomial model and the Monte Carlo model. It also includes all available first-order, second-order and third-order Greeks such as Delta, Gamma, Theta, Vega, Rho, Charm, Vanna, Vomma, Veta, Speed and Zomma.

It gives insights in the sensitivity of an option to changes in the underlying asset price, volatility, years to maturity, dividend yilds and interest rates and several derivatives of these sensitivities.

See the following link for more information: [https://www.jeroenbouma.com/projects/financetoolkit/docs/options](https://www.jeroenbouma.com/projects/financetoolkit/docs/options){:target="_blank"}


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
|            180 |  1      |      -0.9999 | 0      | -0.0191 | 0.4931 |   -0.6533 |   4.0782 |  0      |       0      | -0      |   0      |  0      | -0      | -0      | 0      | -0      |  0      | -0      |   0      |
|            185 |  1      |      -0.9999 | 0      | -0.0196 | 0.5068 |   -0.6533 |   4.4595 |  0      |       0      | -0      |   0      |  0      | -0      | -0      | 0      | -0      |  0      | -0      |   0      |
|            190 |  1      |      -0.9999 | 0      | -0.0202 | 0.5205 |   -0.6533 |   4.9195 |  0      |       0      | -0      |   0      |  0      | -0      | -0      | 0      | -0      |  0      | -0      |   0      |
|            195 |  1      |      -0.9999 | 0      | -0.0207 | 0.5342 |   -0.6533 |   5.4853 |  0      |       0      | -0      |   0      |  0      | -0      | -0      | 0      | -0      |  0      | -0      |   0      |
|            200 |  1      |      -0.9999 | 0      | -0.0212 | 0.5479 |   -0.6533 |   6.1981 |  0      |       0      | -0      |   0      |  0      | -0      | -0      | 0      | -0      |  0      | -0      |   0.0001 |
|            205 |  1      |      -0.9999 | 0      | -0.0217 | 0.5616 |   -0.6533 |   7.1239 |  0      |       0      | -0      |   0.0002 |  0.0001 | -0      | -0      | 0      | -0      |  0      | -0.0002 |   0.0071 |
|            210 |  1      |      -0.9999 | 0      | -0.0223 | 0.5753 |   -0.6533 |   8.3748 |  0      |       0      | -0.0001 |   0.0124 |  0.0071 | -0.0001 | -0      | 0      | -0      |  0.0001 | -0.0079 |   0.2261 |
|            215 |  0.9999 |      -0.9998 | 0.0001 | -0.0243 | 0.5889 |   -0.6532 |  10.1573 |  0.0001 |       0.0001 | -0.0031 |   0.3048 |  0.1423 | -0.002  | -0.0004 | 0.0001 | -0      |  0.0016 | -0.1539 |   2.7483 |
|            220 |  0.9979 |      -0.9976 | 0.0008 | -0.0454 | 0.6013 |   -0.6519 |  12.8781 |  0.001  |       0.0011 | -0.0345 |   3.3891 |  1.2332 | -0.0227 | -0.0037 | 0.0011 | -0.0004 |  0.0129 | -1.2633 |  11.7212 |
|            225 |  0.9808 |      -0.9794 | 0.0058 | -0.1808 | 0.6037 |   -0.6408 |  17.297  |  0.0069 |       0.0078 | -0.1766 |  17.3444 |  4.5655 | -0.117  | -0.0152 | 0.0078 | -0.0022 |  0.0414 | -4.0652 |  10.4124 |
|            230 |  0.9022 |      -0.8971 | 0.0216 | -0.604  | 0.5653 |   -0.5894 |  24.4765 |  0.0256 |       0.0275 | -0.4047 |  39.6576 |  6.5361 | -0.2703 | -0.0283 | 0.0275 | -0.005  |  0.0303 | -2.9369 | -16.4877 |
|            235 |  0.7031 |      -0.6932 | 0.0432 | -1.1838 | 0.4463 |   -0.4593 |  35.2268 |  0.0513 |       0.0528 | -0.3236 |  31.4245 |  2.1541 | -0.2232 | -0.0273 | 0.0528 | -0.0043 | -0.0694 |  6.8815 | -10.901  |
|            240 |  0.4163 |      -0.4053 | 0.0487 | -1.3254 | 0.2665 |   -0.272  |  49.5371 |  0.0579 |       0.0571 |  0.173  | -17.5904 |  0.4562 |  0.0997 | -0.0256 | 0.0571 |  0.0016 | -0.1017 | 10.0098 |  -2.5045 |
|            245 |  0.1735 |      -0.1663 | 0.032  | -0.8684 | 0.1116 |   -0.1133 |  66.7011 |  0.038  |       0.036  |  0.4598 | -45.6744 |  5.3973 |  0.2916 | -0.0307 | 0.036  |  0.0051 | -0.0062 |  0.5668 | -20.8797 |
|            250 |  0.049  |      -0.0461 | 0.0127 | -0.343  | 0.0316 |   -0.032  |  85.8277 |  0.015  |       0.0137 |  0.316  | -31.292  |  6.5283 |  0.203  | -0.024  | 0.0137 |  0.0036 |  0.0497 | -4.9373 |  -2.5872 |
|            255 |  0.0092 |      -0.0086 | 0.0031 | -0.0841 | 0.006  |   -0.006  | 106.169  |  0.0037 |       0.0032 |  0.1099 | -10.8635 |  3.2297 |  0.0709 | -0.0103 | 0.0032 |  0.0013 |  0.0315 | -3.1218 |  15.635  |
|            260 |  0.0012 |      -0.0011 | 0.0005 | -0.0132 | 0.0008 |   -0.0008 | 127.197  |  0.0006 |       0.0005 |  0.0222 |  -2.1908 |  0.8418 |  0.0143 | -0.0025 | 0.0005 |  0.0003 |  0.0089 | -0.8831 |   9.8831 |
|            265 |  0.0001 |      -0.0001 | 0      | -0.0014 | 0.0001 |   -0.0001 | 148.561  |  0.0001 |       0      |  0.0028 |  -0.2741 |  0.1287 |  0.0018 | -0.0004 | 0      |  0      |  0.0014 | -0.1402 |   2.6    |
|            270 |  0      |      -0      | 0      | -0.0001 | 0      |   -0      | 170.037  |  0      |       0      |  0.0002 |  -0.0222 |  0.0123 |  0.0001 | -0      | 0      |  0      |  0.0001 | -0.0137 |   0.3703 |
|            275 |  0      |      -0      | 0      | -0      | 0      |   -0      | 191.483  |  0      |       0      |  0      |  -0.0012 |  0.0008 |  0      | -0      | 0      |  0      |  0      | -0.0009 |   0.0317 |
|            280 |  0      |      -0      | 0      | -0      | 0      |   -0      | 212.807  |  0      |       0      |  0      |  -0      |  0      |  0      | -0      | 0      |  0      |  0      | -0      |   0.0017 |
|            285 |  0      |      -0      | 0      | -0      | 0      |   -0      | 233.949  |  0      |       0      |  0      |  -0      |  0      |  0      | -0      | 0      |  0      |  0      | -0      |   0.0001 |
|            290 |  0      |      -0      | 0      | -0      | 0      |   -0      | 254.872  |  0      |       0      |  0      |  -0      |  0      |  0      | -0      | 0      |  0      |  0      | -0      |   0      |
|            295 |  0      |      -0      | 0      | -0      | 0      |   -0      | 275.552  |  0      |       0      |  0      |  -0      |  0      |  0      | -0      | 0      |  0      |  0      | -0      |   0      |

---

## technicals
This gives access to the Technicals module. The Technicals Module contains nearly 50 Technical Indicators that can be used to analyse companies. These indicators are divided into 3 categories: breadth, overlap and volatility. Each indicator is calculated using the data from the Toolkit module.

Some examples of technical indicators are the Average Directional Index (ADX), the Accumulation/Distribution Line (ADL), the Average True Range (ATR), the Bollinger Bands (BBANDS), the Commodity Channel Index (CCI), the Chaikin Oscillator (CHO), the Chaikin Money Flow (CMF), the Double Exponential Moving Average (DEMA), the Exponential Moving Average (EMA) and the Moving Average Convergence Divergence (MACD).

See the following link for more information: [https://www.jeroenbouma.com/projects/financetoolkit/docs/technicals](https://www.jeroenbouma.com/projects/financetoolkit/docs/technicals){:target="_blank"}


```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

average_directional_index = toolkit.technicals.get_average_directional_index()
```

Which returns:

| Date       |    AAPL |    TSLA |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2025-12-24 | 22.018  | 24.0777 |     14.0995 |
| 2025-12-26 | 20.9256 | 24.3229 |     14.8314 |
| 2025-12-29 | 20.0592 | 23.2159 |     14.7624 |
| 2025-12-30 | 19.276  | 21.7824 |     14.6983 |
| 2025-12-31 | 18.7175 | 20.3475 |     13.7116 |

---

## performance
This gives access to the Performance module. The Performance Module is meant to calculate metrics related to the risk-return relationship. These are things such as Beta, Sharpe Ratio, Sortino Ratio, CAPM, Alpha and the Treynor Ratio.

It gives insights in the performance a stock has to e.g. a benchmark that is not easily identified by looking at the raw data. This class is closely related to the Risk class which highlights things such as Value at Risk (VaR) and Maximum Drawdown.

See the following link for more information: [https://www.jeroenbouma.com/projects/financetoolkit/docs/performance](https://www.jeroenbouma.com/projects/financetoolkit/docs/performance){:target="_blank"}


```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_capital_asset_pricing_model(period='quarterly')
```

Which returns:

| Date   |    AAPL |    TSLA |
|:-------|--------:|--------:|
| 2021Q2 |  0.1154 |  0.1364 |
| 2021Q3 |  0.0066 |  0.0052 |
| 2021Q4 |  0.1214 |  0.1869 |
| 2022Q1 | -0.0575 | -0.1007 |
| 2022Q2 | -0.2134 | -0.332  |
| 2022Q3 | -0.0594 | -0.0818 |
| 2022Q4 |  0.106  |  0.0998 |
| 2023Q1 |  0.083  |  0.1515 |
| 2023Q2 |  0.1032 |  0.1762 |
| 2023Q3 | -0.0414 | -0.1013 |
| 2023Q4 |  0.1021 |  0.2457 |
| 2024Q1 |  0.1038 |  0.1407 |
| 2024Q2 |  0.0524 |  0.0588 |
| 2024Q3 |  0.0571 |  0.1518 |
| 2024Q4 |  0.0215 |  0.0531 |
| 2025Q1 | -0.0386 | -0.1508 |
| 2025Q2 |  0.1473 |  0.2035 |
| 2025Q3 |  0.1029 |  0.1764 |
| 2025Q4 |  0.0236 |  0.0498 |

---

## risk
This gives access to the Risk module. The Risk Module is meant to calculate metrics related to risk such as Value at Risk (VaR), Conditional Value at Risk (cVaR), EMWA/GARCH models and similar models. It also houses cross-asset systemic risk and liquidity measures (CoVaR, Tail Dependence, Amihud Illiquidity, Roll Spread).

Note that the time-series diagnostic and econometric tests (unit root tests, cointegration, Granger causality, ARCH-LM, Jarque-Bera and similar tests) live in the separate Econometrics module instead.

It gives insights in the risk a stock composes that is not perceived as easily by looking at the data. This class is closely related to the Performance class which highlights things such as Sharpe Ratio and Sortino Ratio.

See the following link for more information: [https://www.jeroenbouma.com/projects/financetoolkit/docs/risk](https://www.jeroenbouma.com/projects/financetoolkit/docs/risk){:target="_blank"}


```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_value_at_risk(period='yearly')
```

Which returns:

|           |   Value |
|:----------|--------:|
| AAPL      | -0.2108 |
| TSLA      | -0.5357 |
| Benchmark | -0.1279 |

---

## econometrics
This gives access to the Econometrics module, a thin wrapper that funnels this Toolkit's price/return data through `statsmodels` and `linearmodels` -- regression (OLS/WLS/GLS/ Logit/Probit/Quantile), panel data (Fixed/Random Effects, Hausman), causal inference (IV-2SLS, Difference-in-Differences, Regression Discontinuity, Propensity Score Matching), specification/hypothesis tests (Breusch-Pagan, White, Durbin-Watson, VIF, RESET, Chow, t/F/LR/Wald tests), stationarity (Augmented Dickey-Fuller, KPSS, Phillips-Perron, Zivot-Andrews unit root tests), long-run equilibrium relationships (Engle-Granger and Johansen cointegration), predictive lead-lag relationships (Granger causality), model/ residual diagnostics (ARCH-LM, Jarque-Bera, Ljung-Box, Variance Ratio, CUSUM), forecast comparison (Diebold-Mariano), and time series forecasting (ARIMA, VAR, VECM).

This class is closely related to the Risk class, which houses the risk measures (VaR, CVaR, GARCH) that these tests often inform the choice of.

Requires the optional `financetoolkit[econometrics]` extra (`statsmodels` and `linearmodels`) -- install with `pip install financetoolkit[econometrics]`.

See the following link for more information: [https://www.jeroenbouma.com/projects/financetoolkit/docs/econometrics](https://www.jeroenbouma.com/projects/financetoolkit/docs/econometrics){:target="_blank"}


```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.econometrics.get_augmented_dickey_fuller(period='yearly')
```

---

## etf
The ETF module analyzes the Toolkit's exchange traded funds (and other funds): their holdings, sector and country weightings, profile and premium or discount to NAV, how closely they track the Benchmark, how concentrated and how much alike they are, what their holdings are valued at and how liquid they are.

See the following link for more information: [https://www.jeroenbouma.com/projects/financetoolkit/docs/etf](https://www.jeroenbouma.com/projects/financetoolkit/docs/etf){:target="_blank"}


```python
from financetoolkit import Toolkit

toolkit = Toolkit(["VOO", "QQQ", "AGG"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.etf.get_profile()
```

---

## portfolio
This gives access to the Portfolio Construction module, which builds and examines portfolios from the assets of this Toolkit: optimal weights (minimum variance, maximum Sharpe ratio, mean-variance, risk parity, Hierarchical Risk Parity, inverse volatility, minimum CVaR and Black-Litterman), the efficient frontier, risk contributions, historical stress tests, look-through exposure of funds and a Brinson-Fachler attribution against the benchmark.

When the Toolkit comes from a Portfolio (`Portfolio.toolkit`), the methods that take weights use the Portfolio's latest weights by default.

See the following link for more information: [https://www.jeroenbouma.com/projects/financetoolkit/docs/portfolio-optimization](https://www.jeroenbouma.com/projects/financetoolkit/docs/portfolio-optimization){:target="_blank"}


```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_risk_parity_weights()
```

---

## fixedincome
This gives access to the Fixed Income module. This module contains a wide variety of fixed income related calculations such as the Effective Yield, the Macaulay Duration, the Modified Duration, the Convexity, the Yield to Maturity and models such as Black and Bachelier to valuate derivative instruments such as Swaptions.

Next to that, it is also possible to acquire Central Bank Rates and ICE BofA Indices such as the ICE BofA US High Yield Index, the ICE BofA US Corporate Index and the ICE BofA US Treasury Index.

Note that this class can also be directly accessed by importing the FixedIncome class directly via from financetoolkit import FixedIncome. This is useful if you only want to use the FixedIncome class and not the other classes within the Toolkit module.

See the following link for more information: [https://www.jeroenbouma.com/projects/financetoolkit/docs/fixedincome](https://www.jeroenbouma.com/projects/financetoolkit/docs/fixedincome){:target="_blank"}


```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(
    start_date='2024-01-01',
    end_date='2024-01-15',
    fred_api_key='FRED_API_KEY',
)

fixedincome.get_ice_bofa_effective_yield(maturity=False)
```

Which returns:

| Date       |      AAA |       AA |        A |      BBB |       BB |        B |      CCC |
|:-----------|---------:|---------:|---------:|---------:|---------:|---------:|---------:|
| 2024-01-01 | nan      | nan      | nan      | nan      | nan      | nan      | nan      |
| 2024-01-02 |   0.0459 |   0.0473 |   0.0509 |   0.0543 |   0.0622 |   0.0763 |   0.1333 |
| 2024-01-03 |   0.0459 |   0.0474 |   0.051  |   0.0544 |   0.0634 |   0.0779 |   0.1358 |
| 2024-01-04 |   0.0466 |   0.0481 |   0.0518 |   0.0551 |   0.0639 |   0.0784 |   0.1367 |
| 2024-01-05 |   0.047  |   0.0485 |   0.0521 |   0.0554 |   0.0641 |   0.0787 |   0.137  |
| 2024-01-08 |   0.0465 |   0.0481 |   0.0517 |   0.055  |   0.0633 |   0.0776 |   0.1365 |
| 2024-01-09 |   0.0464 |   0.048  |   0.0516 |   0.0548 |   0.0629 |   0.0771 |   0.1359 |
| 2024-01-10 |   0.0464 |   0.048  |   0.0515 |   0.0547 |   0.0622 |   0.0762 |   0.1351 |
| 2024-01-11 |   0.0456 |   0.0472 |   0.0507 |   0.054  |   0.0619 |   0.076  |   0.1344 |
| 2024-01-12 |   0.0451 |   0.0467 |   0.0502 |   0.0534 |   0.0613 |   0.0753 |   0.1338 |
| 2024-01-15 |   0.0451 |   0.0467 |   0.0501 |   0.0533 |   0.0611 |   0.0751 |   0.1328 |

---

## economics
This gives access to the Economics module. This module contains a wide variety of economic data obtained from OECD. These include things such as the Consumer Price Index (CPI), the Producer Price Index (PPI), the Unemployment Rate, the GDP Growth Rate, the Long and Short Term Interest Rate and the Consumer Confidence Index.

Note that this class can also be directly accessed by importing the Economics class directly via from financetoolkit import Economics. This is useful if you only want to use the Economics class and not the other classes within the Toolkit module.

See the following link for more information: [https://www.jeroenbouma.com/projects/financetoolkit/docs/economics](https://www.jeroenbouma.com/projects/financetoolkit/docs/economics){:target="_blank"}


```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AMZN", "ASML"], start_date="2021-01-01", end_date="2025-12-31")

cpi = toolkit.economics.get_consumer_price_index(period='yearly')

cpi.loc['2015':, ['United States', 'Netherlands', 'Japan']]
```

Which returns:

|      |   United States |   Netherlands |   Japan |
|:-----|----------------:|--------------:|--------:|
| 2021 |         114.325 |       110.389 | 101.567 |
| 2022 |         123.474 |       121.426 | 104.112 |
| 2023 |         128.557 |       126.092 | 107.503 |
| 2024 |         132.349 |       130.311 | 110.457 |
| 2025 |         135.831 |       134.486 | 113.98  |

---

## get_profile
Obtain the profile of the specified tickers. These include important metrics such as the beta, market capitalization, currency, isin, industry, and ipo date that give an overall understanding about the company.

**Also known as:** company description, sector, industry, CEO, employee count.

**Args:**

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["ASML.AS", "SAP.DE", "MC.PA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.get_profile().loc[["Industry", "Exchange", "Currency", "ISIN", "Beta"]]
```

Which returns:

|          | ASML.AS        | SAP.DE                 | MC.PA        |
|:---------|:---------------|:-----------------------|:-------------|
| Industry | Semiconductors | Software - Application | Luxury Goods |
| Exchange | AMS            | XETRA                  | PAR          |
| Currency | EUR            | EUR                    | EUR          |
| ISIN     | NL0010273215   | DE0007164600           | FR0000121014 |
| Beta     | 1.302          | 0.775                  | 0.879        |

---

## get_quote
Get the quote of the specified tickers: the price and its change, the day's open, low and high, the previous close, the year low and high, the 50 and 200 day average prices, the volume, the market capitalization, the exchange and the time of the quote.

**Also known as:** real-time price, current stock price, live quote.

**Args:**

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["V", "MA", "AXP"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.get_quote().loc[["Price", "Year High", "Year Low"]]
```

Which returns:

|           |      V |     MA |    AXP |
|:----------|-------:|-------:|-------:|
| Price     | 407.92 | 623.6  | 313.03 |
| Year High | 414.6  | 633.29 | 387.49 |
| Year Low  | 293.89 | 464.52 | 290.97 |

---

## get_rating
Get the rating of the specified tickers: a letter rating and an overall score based on six scores from 1 (weak) to 5 (strong). These scores are categorized as follows:

- An overall rating (the letter rating and the Rating Score)

- Discounted Cash Flow (DCF)

- Return on Equity (ROE)

- Return on Assets (ROA)

- Debt to Equity (DE)

- Price Earnings (PE)

- Price to Book (PB)

**Also known as:** stock rating, fundamental score, quantitative rating.

**Args:**

**Returns:**

pd.DataFrame: The stock rating information for the specified tickers.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["V"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

rating = toolkit.get_rating()

rating[["DCF Score", "ROE Score", "ROA Score", "DE Score", "PE Score", "PB Score"]].tail(1)
```

Which returns:

| date                |   DCF Score |   ROE Score |   ROA Score |   DE Score |   PE Score |   PB Score |
|:--------------------|------------:|------------:|------------:|-----------:|-----------:|-----------:|
| 2025-12-31 00:00:00 |           4 |           5 |           5 |          2 |          1 |          1 |

---

## get_analyst_estimates
Obtain analyst estimates regarding revenues, EBITDA, EBIT, Net Income SGA Expenses and EPS. The number of analysts are also reported.

Note that this information requires a Premium FMP subscription.

**Also known as:** earnings estimates, revenue estimates, analyst consensus.

**Args:**

- <u>overwrite (bool, optional):</u> Defines whether to overwrite the existing data. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> Defines the number of decimal places to round the data to. Defaults to None.
- <u>growth (bool, optional):</u> Defines whether to return the growth of the data. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> Defines the number of periods to lag the growth data by. Defaults to 1.
- <u>show_columns (list[str] &#124; None):</u> A list of column names to keep in the result. Invalid
names are reported and ignored. Defaults to None, which keeps every column.

**Returns:**

pandas.DataFrame: The analyst estimates for the specified tickers.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NVDA", "AMD", "AVGO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2026-01-01",
    end_date="2028-12-31",
)

toolkit.get_analyst_estimates(show_columns=["Estimated Revenue Average"])
```

Which returns:

|      |        2026 |        2027 |        2028 |        2029 |        2030 |          2031 |
|:-----|------------:|------------:|------------:|------------:|------------:|--------------:|
| NVDA | 2.13656e+11 | 4.09929e+11 | 6.95178e+11 | 9.25214e+11 | 1.10649e+12 |   1.21149e+12 |
| AMD  | 5.13395e+10 | 9.04101e+10 | 1.25666e+11 | 1.6376e+11  | 2.32364e+11 | nan           |
| AVGO | 1.06009e+11 | 1.74279e+11 | 2.81861e+11 | 4.16476e+11 | 5.52387e+11 | nan           |

---

## get_earnings_calendar
Obtain Earnings Calendars for any range of companies. You have the option to obtain the actual dates or to convert to the corresponding quarters.

Note that this information requires a Premium FMP subscription.

The surprise is the reported EPS against the estimate, usually as a percentage of the estimate. Most companies report above the consensus, so a small beat is the norm, and the share price tends to react to the size of the surprise, to revenue against its estimate and to the guidance given on the call rather than to a beat as such.

**Also known as:** earnings dates, earnings schedule, reporting date.

**Args:**

- <u>actual_dates (bool):</u> Defines whether to return the actual dates or the corresponding quarters.
- <u>overwrite (bool):</u> Defines whether to overwrite the existing data.
- <u>show_columns (list[str] &#124; None):</u> A list of column names to keep in the result. Invalid
names are reported and ignored. Defaults to None, which keeps every column.
- <u>rounding (int &#124; None):</u> The number of decimals to round the results to. Defaults to None,
which uses the rounding set on the Toolkit.

**Returns:**

pd.DataFrame: The earnings calendar for the specified tickers.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["COST"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.get_earnings_calendar(show_columns=["EPS", "Estimated EPS"])
```

Which returns:

| date                |   EPS |   Estimated EPS |
|:--------------------|------:|----------------:|
| 2024-03-07 00:00:00 |  3.92 |            3.62 |
| 2024-05-30 00:00:00 |  3.78 |            3.7  |
| 2024-09-26 00:00:00 |  5.29 |            5.08 |
| 2024-12-12 00:00:00 |  4.04 |            3.79 |
| 2025-03-06 00:00:00 |  4.02 |            4.09 |
| 2025-05-29 00:00:00 |  4.28 |            4.24 |
| 2025-09-25 00:00:00 |  5.87 |            5.8  |
| 2025-12-11 00:00:00 |  4.5  |            4.27 |

---

## get_stock_news
Obtain the latest news articles for the tickers of this Toolkit instance, whether they are stocks, cryptocurrencies or currency pairs. Qualitative companion to the toolkit's quantitative data. Automatically filtered to this Toolkit instance's start_date and end_date.

Each ticker is matched with the right news feed. A currency pair such as EURUSD or EURUSD=X is searched in the forex news. Any other ticker is searched in both the stock and the crypto news, since a ticker such as BTCUSD cannot be told apart from a stock by its format; the feed it does not belong to simply returns nothing.

**Also known as:** ticker news, company news feed, crypto news, forex news.

**Args:**

- <u>pages (int, optional):</u> The number of pages to collect per news feed, each page is a
separate API call, e.g. pages=5 makes 5 calls. Defaults to 1.
- <u>limit (int, optional):</u> The number of articles to return per page. Defaults to 100.
- <u>show_columns (list[str] &#124; None):</u> A list of column names to keep in the result. Invalid
names are reported and ignored. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The latest news articles for the specified tickers, newest first.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

stock_news = toolkit.get_stock_news(limit=5)

stock_news[["Symbol", "Publisher", "Title"]]
```

Which returns:

| Published Date      | Symbol   | Publisher       | Title                                                               |
|:--------------------|:---------|:----------------|:--------------------------------------------------------------------|
| 2025-12-31 17:34:00 | AAPL     | GuruFocus       | Market Today: Buffett era ends; Tesla warns; stocks cap strong 2025 |
| 2025-12-31 16:11:00 | AAPL     | The Motley Fool | Here Are My Top 2 Stocks to Buy for 2026 and Beyond                 |
| 2025-12-31 14:35:53 | AAPL     | Schwab Network  | Ca$htag$: Apple (AAPL) Strong Holiday Season                        |
| 2025-12-31 14:15:00 | MSFT     | The Motley Fool | The Best Tech Stocks to Buy in January for 2026 Gains               |
| 2025-12-31 14:14:48 | AAPL     | CNBC Television | Apple's AI challenges in 2026                                       |

---

## get_press_releases
Obtain the latest official company press releases for the tickers of this Toolkit instance, such as earnings announcements and corporate communications. Automatically filtered to this Toolkit instance's start_date and end_date.

**Also known as:** corporate announcements, company press release feed.

**Args:**

- <u>pages (int, optional):</u> The number of pages to collect, each page is a
separate API call, e.g. pages=5 makes 5 calls. Defaults to 1.
- <u>limit (int, optional):</u> The number of articles to return per page. Defaults to 100.
- <u>show_columns (list[str] &#124; None):</u> A list of column names to keep in the result. Invalid
names are reported and ignored. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The latest press releases for the specified tickers.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

press_releases = toolkit.get_press_releases(limit=5)

press_releases[["Symbol", "Publisher", "Title"]]
```

Which returns:

| Published Date      | Symbol   | Publisher     | Title                                                                                                 |
|:--------------------|:---------|:--------------|:------------------------------------------------------------------------------------------------------|
| 2025-12-18 09:00:00 | MSFT     | PRNewsWire    | Cognizant and Microsoft Expand Partnership to Advance AI Transformation and Frontier Firm Experiences |
| 2025-12-18 04:00:00 | MSFT     | Business Wire | Reply Recognized as a Microsoft Azure Expert Managed Services Provider for the Sixth Consecutive Year |
| 2025-12-17 20:00:00 | AAPL     | Business Wire | Apple announces changes to iOS in Japan                                                               |
| 2025-12-17 16:30:00 | MSFT     | Accesswire    | ProsperOps Achieves Microsoft Azure IP Co-Sell Status                                                 |
| 2025-12-17 08:00:00 | MSFT     | Business Wire | EcoVadis Wins Microsoft Local Partner Award FY25 in AI Transformation - Scale Category                |

---

## get_revenue_geographic_segmentation
Obtain revenue by geographic segmentation (e.g. United States, Europe, Asia).

Note that this information requires a Premium FMP subscription.

**Also known as:** revenue by region, geographic revenue breakdown.

**Args:**

- <u>overwrite (bool):</u> Defines whether to overwrite the existing data.
- <u>show_columns (list[str] &#124; None):</u> A list of column names to keep in the result. Invalid
names are reported and ignored. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The revenue by geographic segmentation for the specified tickers.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.get_revenue_geographic_segmentation()
```

Which returns:

|              |        2021 |        2022 |       2023 |        2024 |        2025 |
|:-------------|------------:|------------:|-----------:|------------:|------------:|
| Americas     | 1.53306e+11 | 1.69658e+11 | 1.6256e+11 | 1.67045e+11 | 1.78353e+11 |
| Asia Pacific | 2.6356e+10  | 2.9375e+10  | 2.9615e+10 | 3.0658e+10  | 3.3696e+10  |
| China        | 6.8366e+10  | 7.42e+10    | 7.2559e+10 | 6.6952e+10  | 6.4377e+10  |
| Europe       | 8.9307e+10  | 9.5118e+10  | 9.4294e+10 | 1.01328e+11 | 1.11032e+11 |
| Japan        | 2.8482e+10  | 2.5977e+10  | 2.4257e+10 | 2.5052e+10  | 2.8703e+10  |

---

## get_revenue_product_segmentation
Obtain revenue by product segmentation (e.g. iPad, Advertisement, Windows).

Note that this information requires a Premium FMP subscription.

**Also known as:** revenue by product, product segment revenue.

**Args:**

- <u>overwrite (bool):</u> Defines whether to overwrite the existing data.
- <u>show_columns (list[str] &#124; None):</u> A list of column names to keep in the result. Invalid
names are reported and ignored. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The revenue by product segmentation for the specified tickers.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NVDA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.get_revenue_product_segmentation()
```

Which returns:

|                            |      2021 |       2022 |       2023 |       2024 |        2025 |
|:---------------------------|----------:|-----------:|-----------:|-----------:|------------:|
| Automotive                 | 5.36e+08  | 5.66e+08   | 9.03e+08   | 1.091e+09  | 1.694e+09   |
| Data Center                | 6.696e+09 | 1.0613e+10 | 1.5005e+10 | 4.7525e+10 | 1.15186e+11 |
| Gaming                     | 7.759e+09 | 1.2462e+10 | 9.067e+09  | 1.0447e+10 | 1.135e+10   |
| Oem And Other              | 6.31e+08  | 1.162e+09  | 4.55e+08   | 3.06e+08   | 3.89e+08    |
| Professional Visualization | 1.053e+09 | 2.111e+09  | 1.544e+09  | 1.553e+09  | 1.878e+09   |

---

## get_historical_data
Returns historical data for the specified tickers. This contains the following columns:

- Open: The opening price for the period.
- High: The highest price for the period.
- Low: The lowest price for the period.
- Close: The closing price for the period.
- Adj Close: The adjusted closing price for the period.
- Volume: The volume for the period.
- Dividends: The dividends for the period.
- Return: The return for the period.
- Cumulative Return: The cumulative return for the period.

Volatility, Excess Return and Excess Volatility are not included here. These are available as dedicated calculations in the Risk module (e.g. toolkit.risk.get_volatility, toolkit.risk.get_excess_volatility) and the Performance module (e.g. toolkit.performance.get_excess_return) instead.

If a benchmark ticker is selected, it also calculates the benchmark ticker together with the results. By default this is set to "SPY" (S&P 500 Index) but can be any ticker. This is relevant for calculations for models such as CAPM, Alpha and Beta.

Important to note is that when an api_key is included in the Toolkit initialization that the data collection defaults to FinancialModelingPrep which is a more stable source and utilises your subscription. However, if this is undesired, it can be disabled by setting enforce_source to "YahooFinance". If data collection fails from FinancialModelingPrep it automatically reverts back to YahooFinance.

**Also known as:** OHLCV, price history, open high low close volume.

**Args:**

- <u>enforce_source (str, optional):</u> A string containing the historical source you wish to enforce.
This can be either FinancialModelingPrep or YahooFinance. Defaults to no enforcement.
- <u>period (str):</u> The interval at which the historical data should be
returned - daily, weekly, monthly, quarterly, or yearly.
Defaults to "daily".
- <u>return_column (str):</u> The column to use for the return calculation. Defaults to "Adj Close".
- <u>include_dividends (bool):</u> Defines whether to include dividends in the return calculation.
Defaults to True.
- <u>fill_nan (bool):</u> Defines whether to forward fill NaN values. This defaults
to True to prevent holes in the dataset. This is especially relevant for
technical indicators.
- <u>overwrite (bool):</u> Defines whether to overwrite the existing data. If this is not enabled, the function
will return the earlier retrieved data. This is done to prevent too many API calls. Defaults to False.
- <u>rounding (int):</u> Defines the number of decimal places to round the data to.
- <u>show_ticker_seperation (bool, optional):</u> A boolean representing whether to show which tickers
acquired data from FinancialModelingPrep and which tickers acquired data from YahooFinance.
- <u>show_columns (list[str], optional):</u> A list of columns to include in the output. Valid columns
are Open, High, Low, Close, Adj Close, Volume, Dividends, Return and Cumulative Return.
Invalid column names are logged as warnings. If all
provided columns are invalid the full dataset is returned. Defaults to None (all columns).

**Raises:**

ValueError: If an invalid value is specified for period.

**Returns:**

pandas.DataFrame: The historical data for the specified tickers.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["CAT", "DE", "URI"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.get_historical_data(show_columns=["Close"]).tail()
```

Which returns:

| Date       |    CAT |     DE |    URI |   Benchmark |
|:-----------|-------:|-------:|-------:|------------:|
| 2025-12-24 | 583.76 | 467.44 | 824.77 |      690.38 |
| 2025-12-26 | 583    | 468.93 | 827.94 |      690.31 |
| 2025-12-29 | 578.71 | 470.24 | 819.51 |      687.85 |
| 2025-12-30 | 577.39 | 469.94 | 817.25 |      687.01 |
| 2025-12-31 | 572.87 | 465.57 | 809.32 |      681.92 |

---

## get_intraday_data
Returns intraday historical data for the specified tickers. This contains the following columns:

- Open: The opening price for the period.
- High: The highest price for the period.
- Low: The lowest price for the period.
- Close: The closing price for the period.
- Volume: The volume for the period.
- Return: The return for the period.
- Cumulative Return: The cumulative return for the period.

Volatility is not included here. This is available as a dedicated calculation in the Risk module instead (e.g. toolkit.risk.get_volatility).

Keep in mind that this data is available for a shorter period. This means that the start date is ignored if the difference between the start and end date is bigger than the maximum period.

If a benchmark ticker is selected, it also calculates the benchmark ticker together with the results. By default this is set to "SPY" (S&P 500 Index) but can be any ticker. This is relevant for calculations for models such as CAPM, Alpha and Beta.

Please note that this functionality is only available through Financial Modeling Prep. Therefore, an api_key is required to use this functionality.

**Also known as:** tick data, minute data, intraday price history.

**Args:**

- <u>period (str, optional):</u> The intraday interval to fetch (e.g. "1min", "5min", "1hour").
Defaults to "1hour".
- <u>return_column (str, optional):</u> The column to use for the return calculation. Defaults to "Close".
- <u>fill_nan (bool, optional):</u> Defines whether to forward fill NaN values. Defaults to True.
- <u>rounding (int &#124; None, optional):</u> Defines the number of decimal places to round the data to. Defaults to None.
- <u>show_columns (list[str] &#124; None):</u> A list of column names to keep in the result. Invalid
names are reported and ignored. Defaults to None, which keeps every column.

**Returns:**

pandas.DataFrame: The intraday data for the specified tickers.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NVDA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-12-29",
    end_date="2025-12-31",
)

toolkit.get_intraday_data(period="1hour", show_columns=["Close"]).tail()
```

Which returns:

| date             |   ('Close', 'NVDA') |   ('Close', 'Benchmark') |
|:-----------------|--------------------:|-------------------------:|
| 2025-12-31 11:00 |              188.92 |                   685    |
| 2025-12-31 12:00 |              188.97 |                   685.35 |
| 2025-12-31 13:00 |              188.05 |                   685.04 |
| 2025-12-31 14:00 |              187.13 |                   682.69 |
| 2025-12-31 15:00 |              186.53 |                   681.87 |

---

## get_dividend_calendar
Obtain Dividend Calendars for any range of companies. It includes the following columns:

- Date: The date of the dividend.
- Adj Dividend: The adjusted dividend amount.
- Dividend: The dividend amount.
- Yield: The annualized dividend yield at the time of the dividend, as a decimal (0.0054 is 0.54%).
- Record Date: The record date of the dividend.
- Payment Date: The payment date of the dividend.
- Declaration Date: The declaration date of the dividend.

If a company does not pay any dividend, the function will mention that it was not able to find any dividend data for that company.

**Also known as:** dividend dates, ex-dividend date, dividend history.

**Args:**

- <u>overwrite (bool):</u> Defines whether to overwrite the existing data.
- <u>rounding (int):</u> Defines the number of decimal places to round the data to.
- <u>show_columns (list[str] &#124; None):</u> A list of column names to keep in the result. Invalid
names are reported and ignored. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The dividend calendar for the specified tickers.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["JNJ"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.get_dividend_calendar(show_columns=["Dividend"])
```

Which returns:

| date       |   Dividend |
|:-----------|-----------:|
| 2021-02-22 |       1.01 |
| 2021-05-24 |       1.06 |
| 2021-08-23 |       1.06 |
| 2021-11-22 |       1.06 |
| 2022-02-18 |       1.06 |
| 2022-05-23 |       1.13 |
| 2022-08-22 |       1.13 |
| 2022-11-21 |       1.13 |
| 2023-02-17 |       1.13 |
| 2023-05-22 |       1.19 |
| 2023-08-25 |       1.19 |
| 2023-11-20 |       1.19 |
| 2024-02-16 |       1.19 |
| 2024-05-20 |       1.24 |
| 2024-08-27 |       1.24 |
| 2024-11-26 |       1.24 |
| 2025-02-18 |       1.24 |
| 2025-05-27 |       1.3  |
| 2025-08-26 |       1.3  |
| 2025-11-25 |       1.3  |

---

## get_esg_scores
ESG scores, which stands for Environmental, Social, and Governance scores, are a crucial metric used by investors and organizations to assess a company's sustainability and ethical practices. These scores provide valuable insights into a company's performance in three key areas:

- Environmental (E): The environmental component evaluates a company's impact on the planet and its efforts to mitigate environmental risks. It includes factors like carbon emissions, energy efficiency, water management, and waste reduction. A high environmental score indicates a company's commitment to eco-friendly practices and reducing its ecological footprint.
- Social (S): The social component focuses on how a company interacts with its employees, customers, suppliers, and the communities in which it operates. Key factors in the social score include labor practices, diversity and inclusion, human rights, product safety, and community engagement. A strong social score reflects a company's dedication to fostering positive relationships and contributing positively to society.
- Governance (G): Governance examines a company's internal structures, policies, and leadership. It assesses aspects such as board independence, executive compensation, transparency, and the presence of anti-corruption measures. A high governance score signifies strong leadership and a commitment to maintaining high ethical standards and accountability

ESG scores provide investors with a holistic view of a company's sustainability and ethical practices, allowing them to make more informed investment decisions. These scores are increasingly used to identify socially responsible investments and guide capital towards companies that prioritize long-term sustainability and responsible business practices. As the importance of ESG considerations continues to grow, companies are motivated to improve their ESG scores, not only for ethical reasons but also to attract investors who value sustainable and responsible business practices.

**Also known as:** environmental social governance, sustainability, ESG rating.

**Args:**

- <u>overwrite (bool):</u> Defines whether to overwrite the existing data.
- <u>rounding (int):</u> Defines the number of decimal places to round the data to.
- <u>show_columns (list[str] &#124; None):</u> A list of column names to keep in the result. Invalid
names are reported and ignored. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The ESG scores for the specified tickers.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["XOM", "SHEL", "BP"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.get_esg_scores(show_columns=["ESG Score"])
```

Which returns:

| date   |   ('ESG Score', 'XOM') |   ('ESG Score', 'SHEL') |   ('ESG Score', 'BP') |
|:-------|-----------------------:|------------------------:|----------------------:|
| 2021   |                  66.43 |                  nan    |                 66.14 |
| 2022   |                  68.75 |                   65.39 |                 67.54 |
| 2023   |                  69.98 |                   60.49 |                 70.49 |
| 2024   |                  68    |                   64.17 |                 62.26 |
| 2025   |                  68.75 |                   61.74 |                 64.47 |

---

## get_market_risk_premium
Obtains the equity risk premium by country -- the equity risk premium of a mature market plus a country risk premium, the country's default spread scaled by the volatility of its equities relative to its bonds, following the approach popularized by Aswath Damodaran -- which is widely used to calibrate country-specific costs of equity and discount rates in a multi-country setting.

In a cost of equity the premium is applied in one of two common ways: beta times the Total Equity Risk Premium, or beta times the mature market premium with the Country Risk Premium added on top. For a company that earns its revenue in several countries the premium is often weighted by where the revenue comes from rather than by where the company is listed.

**Also known as:** country risk premium, Damodaran equity risk premium.

**Args:**

- <u>overwrite (bool):</u> Defines whether to overwrite the existing data.

**Returns:**

pd.DataFrame: The market risk premium by country, including the continent, Country
Risk Premium and Total Equity Risk Premium (both as decimals, 0.0446 for 4.46%).

The premiums are decimal fractions (0.0446 for 4.46%).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

market_risk_premium = toolkit.get_market_risk_premium()

market_risk_premium.loc[
    ["United States", "Germany", "Japan", "Brazil", "India", "South Africa"],
    ["Country Risk Premium", "Total Equity Risk Premium"],
]
```

Which returns:

| Country       |   Country Risk Premium |   Total Equity Risk Premium |
|:--------------|-----------------------:|----------------------------:|
| United States |                 0.0023 |                      0.0446 |
| Germany       |                 0      |                      0.0423 |
| Japan         |                 0.0091 |                      0.0514 |
| Brazil        |                 0.0324 |                      0.0747 |
| India         |                 0.0285 |                      0.0708 |
| South Africa  |                 0.039  |                      0.0813 |

---

## get_commitment_of_traders
Obtains the CFTC Commitment of Traders (COT) report for the tickers the Toolkit was initialized with. Published weekly by the U.S. Commodity Futures Trading Commission, it breaks down open interest in futures markets by trader type -- Non-Commercial (large speculators), Commercial (hedgers) and Non-Reportable (small traders) -- and is widely used to gauge positioning and sentiment in commodity, currency, interest rate and stock index futures markets.

Note that this data is only available for CFTC-tracked futures markets. Tickers without a corresponding futures contract (e.g. most individual equities) return no data.

Positioning is usually read from the net position of the non-commercial traders (long minus short), often as a share of open interest and against its own history: an extreme reading means a crowded trade. Commercial traders are mostly hedgers whose positions mirror their physical business, so a large commercial net short in a commodity is normal rather than a bearish view. The report shows the positions of Tuesday and is published on Friday.

**Also known as:** COT report, CFTC positioning data, speculator/hedger positioning.

**Args:**

- <u>overwrite (bool):</u> Defines whether to overwrite the existing data.

**Returns:**

pd.DataFrame: The Commitment of Traders report for the specified tickers.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["GC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.get_commitment_of_traders()[["Non-Commercial Long", "Non-Commercial Short"]].tail()
```

Which returns:

| date                |   Non-Commercial Long |   Non-Commercial Short |
|:--------------------|----------------------:|-----------------------:|
| 2025-12-02 00:00:00 |                261331 |                  43771 |
| 2025-12-09 00:00:00 |                268485 |                  44599 |
| 2025-12-16 00:00:00 |                280920 |                  46942 |
| 2025-12-23 00:00:00 |                290161 |                  49461 |
| 2025-12-30 00:00:00 |                275592 |                  44419 |

---

## get_executives
Obtain the key executives of each company: their title, pay, gender, year of birth and whether they are still active. This shows who leads the company and how the leadership team is composed, which is useful when assessing management quality or when following a change at the top.

**Also known as:** management team, company officers, leadership.

**Args:**

- <u>overwrite (bool):</u> Defines whether to overwrite the existing data.
- <u>show_columns (list[str] &#124; None):</u> A list of column names to keep in the result. Invalid
names are reported and ignored. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The executives per ticker, indexed by their name. Pay is only
disclosed for the executives named in the proxy statement, so the best paid
come first and the executives without disclosed pay follow.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["JPM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.get_executives(show_columns=["Title", "Year Born"])
```

Which returns:

| Name                 | Title                                                                             |   Year Born |
|:---------------------|:----------------------------------------------------------------------------------|------------:|
| Mary Callahan Erdoes | Chief Executive Officer of Asset & Wealth Management and Executive Vice President |        1967 |
| Douglas Petno        | CEO of the Commercial & Investment Bank and Co-President                          |        1966 |
| Troy Larry Rohrbaugh | CEO of Consumer & Community Banking and Co-President                              |        1970 |
| Jeremy Barnum        | Executive Vice President & Chief Financial Officer                                |        1973 |
| James Dimon          | Chairman & Chief Executive Officer                                                |        1956 |
| Jennifer A. Piepszak | Chief Operating Officer                                                           |        1971 |
| Daniel Eduardo Pinto | Vice Chairman                                                                     |        1963 |
| Todd Anthony Combs   | Head Strategic Investment Group of Security & Resiliency Initiative               |        1971 |
| Lori Ann Beer        | Global Chief Information Officer                                                  |        1968 |
| Elena A. Korablina   | MD, Firmwide Controller & Principal Accounting Officer                            |        1974 |

---

## get_executive_compensation
Obtain the compensation of each company's executives per year as reported in the proxy statement (DEF 14A): salary, bonus, stock and option awards, incentive plan compensation, other compensation and the total. Comparing pay with the company's performance shows how well management incentives are aligned with shareholders.

Automatically filtered to the years of this Toolkit instance's start_date and end_date.

**Also known as:** executive pay, management compensation, proxy statement compensation.

**Args:**

- <u>overwrite (bool):</u> Defines whether to overwrite the existing data.
- <u>show_columns (list[str] &#124; None):</u> A list of column names to keep in the result. Invalid
names are reported and ignored. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The compensation per ticker, indexed by year and executive.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["JPM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.get_executive_compensation(show_columns=["Salary", "Incentive Plan Compensation"])
```

Which returns:

|                                                               |   Salary |   Incentive Plan Compensation |
|:--------------------------------------------------------------|---------:|------------------------------:|
| (2025, 'Douglas Petno Co-CEO, Commercial & Investment Bank')  |  1000000 |                      26500000 |
| (2025, 'James Dimon Chairman and CEO')                        |  1500000 |                      41500000 |
| (2025, 'Jeremy Barnum CFO')                                   |  1000000 |                      18500000 |
| (2025, 'Mary Callahan Erdoes CEO, Asset & Wealth Management') |  1000000 |                      30000000 |
| (2025, 'Troy Rohrbaugh Co-CEO, Commercial & Investment Bank') |  1000000 |                      26500000 |

---

## get_company_notes
Obtain the securities other than common stock that each company has registered for listing, mostly notes with their coupon and maturity in the title (e.g. "1.625% Notes due 2026") and the exchange they are listed on. The list can include notes that have since matured or been redeemed and other securities such as depositary shares of preferred stock, so it shows which debt a company has listed rather than what is outstanding today.

**Also known as:** listed debt, bonds issued, debt securities.

**Args:**

- <u>overwrite (bool):</u> Defines whether to overwrite the existing data.
- <u>show_columns (list[str] &#124; None):</u> A list of column names to keep in the result. Invalid
names are reported and ignored. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The notes per ticker, indexed by their title.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["KO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.get_company_notes(show_columns=["Exchange"])
```

Which returns:

| Title                        | Exchange   |
|:-----------------------------|:-----------|
| Floating Rate Notes Due 2019 | NYSE       |
| 0.000% Notes Due 2021        | NYSE       |
| 1.125% Notes Due 2022        | NYSE       |
| 0.75% Notes Due 2023         | NYSE       |
| 0.500% Notes Due 2024        | NYSE       |
| 1.875% Notes Due 2026        | NYSE       |
| 1.125% Notes Due 2027        | NYSE       |
| 1.625% Notes Due 2035        | NYSE       |
| 1.100% Notes Due 2036        | NYSE       |

---

## get_employee_count
Obtain the number of employees each company reported in its annual filings over time. The most recent row is the current employee count and the rows before it show how the workforce developed, which can be set against revenue or profit to see how productive the workforce is.

Automatically filtered to this Toolkit instance's start_date and end_date.

**Also known as:** headcount, number of employees, workforce size.

**Args:**

- <u>overwrite (bool):</u> Defines whether to overwrite the existing data.

**Returns:**

pd.DataFrame: The employee count per reporting year (rows) and ticker (columns).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["WMT", "AMZN"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.get_employee_count()
```

Which returns:

| Period   |     WMT |    AMZN |
|:---------|--------:|--------:|
| 2021     | 2300000 | 1608000 |
| 2022     | 2300000 | 1541000 |
| 2023     | 2100000 | 1525000 |
| 2024     | 2100000 | 1556000 |
| 2025     | 2100000 | 1576000 |

---

## get_shares_float
Obtain the free float of each company: the number of shares available for public trading, the number of shares outstanding and the free float as the share of the outstanding shares that can be traded (as a decimal). A low free float means few shares change hands, which tends to make a stock less liquid and more volatile.

**Also known as:** free float, float shares, public float, share liquidity.

**Args:**

- <u>overwrite (bool):</u> Defines whether to overwrite the existing data.

**Returns:**

pd.DataFrame: The share float figures (rows) per ticker (columns).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["META", "GOOGL", "BRK-B"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.get_shares_float().loc[["Free Float"]]
```

Which returns:

|            |     META |    GOOGL |    BRK-B |
|:-----------|---------:|---------:|---------:|
| Free Float | 0.863739 | 0.893911 | 0.656007 |

---

## get_mergers_acquisitions
Obtain the mergers and acquisitions each company took part in, as the acquirer or as the target, based on the merger filings (S-4) with the SEC. Every deal comes with the other party, the filing date and a link to the filing.

The search uses the company name from the profile, so the profile is retrieved first when it is not available yet. Deals of companies with a similar name are left out: only the deals in which the ticker itself is involved are kept.

Automatically filtered to this Toolkit instance's start_date and end_date.

**Also known as:** M&A, acquisitions, mergers, takeovers.

**Args:**

- <u>overwrite (bool):</u> Defines whether to overwrite the existing data.
- <u>show_columns (list[str] &#124; None):</u> A list of column names to keep in the result. Invalid
names are reported and ignored. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The deals per ticker, indexed by their transaction date.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["CVX"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.get_mergers_acquisitions(show_columns=["Role", "Acquirer Name", "Target Name"])
```

Which returns:

| Transaction Date    | Role     | Acquirer Name   | Target Name      |
|:--------------------|:---------|:----------------|:-----------------|
| 2021-03-22 00:00:00 | Acquirer | CHEVRON CORP    | NBLX             |
| 2023-06-20 00:00:00 | Acquirer | CHEVRON CORP    | PDC Energy, Inc. |
| 2023-08-03 00:00:00 | Acquirer | CHEVRON CORP    | PDC              |
| 2024-02-26 00:00:00 | Acquirer | CHEVRON CORP    | Hess             |

---

## get_stock_splits
Obtain the stock splits of each company, with the split ratio as a numerator and denominator: a 4-for-1 split has numerator 4 and denominator 1, while a reverse split has a numerator smaller than its denominator. Splits change the number of shares but not the value of the company, which is why historical prices are adjusted for them.

Automatically filtered to this Toolkit instance's start_date and end_date.

**Also known as:** share splits, reverse splits, split history.

**Args:**

- <u>overwrite (bool):</u> Defines whether to overwrite the existing data.

**Returns:**

pd.DataFrame: The splits per ticker, indexed by their date.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NVDA", "AAPL", "TSLA", "GOOGL", "AMZN"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2020-01-01",
    end_date="2025-12-31",
)

toolkit.get_stock_splits()[["Numerator", "Denominator"]]
```

Which returns:

|                         |   Numerator |   Denominator |
|:------------------------|------------:|--------------:|
| ('NVDA', '2021-07-20')  |           4 |             1 |
| ('NVDA', '2024-06-10')  |          10 |             1 |
| ('AAPL', '2020-08-31')  |           4 |             1 |
| ('TSLA', '2020-08-31')  |           5 |             1 |
| ('TSLA', '2022-08-25')  |           3 |             1 |
| ('GOOGL', '2022-07-18') |          20 |             1 |
| ('AMZN', '2022-06-06')  |          20 |             1 |

---

## get_insider_trade_statistics
Obtain quarterly statistics on the trades of each company's insiders (officers, directors and large shareholders), based on their Form 4 filings: the number of acquisitions and disposals, their ratio, the number of shares acquired and disposed of, and the number of open market purchases and sales.

Insiders know their company best, so heavy buying can signal confidence while persistent selling can be worth a closer look. Note that many disposals are routine, such as sales to cover taxes on vested stock awards.

Automatically filtered to this Toolkit instance's start_date and end_date.

**Also known as:** insider trading, insider transactions, Form 4 statistics.

**Args:**

- <u>overwrite (bool):</u> Defines whether to overwrite the existing data.
- <u>rounding (int):</u> Defines the number of decimal places to round the data to.
- <u>show_columns (list[str] &#124; None):</u> A list of column names to keep in the result. Invalid
names are reported and ignored. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The statistics per ticker, indexed by quarter.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["META"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.get_insider_trade_statistics(show_columns=["Acquired Transactions", "Disposed Transactions"])
```

Which returns:

| Period   |   Acquired Transactions |   Disposed Transactions |
|:---------|------------------------:|------------------------:|
| 2024Q1   |                     206 |                    1965 |
| 2024Q2   |                      59 |                     322 |
| 2024Q3   |                      38 |                     664 |
| 2024Q4   |                      56 |                     487 |
| 2025Q1   |                      77 |                     992 |
| 2025Q2   |                      67 |                     194 |
| 2025Q3   |                      50 |                     271 |
| 2025Q4   |                      41 |                      82 |

---

## get_stock_grades
Obtain the grades analysts gave each company: per date and grading company the previous and the new grade, and whether the grade was upgraded, downgraded or maintained. Following how the grades change over time shows how sentiment among analysts develops, with upgrades and downgrades by well-followed firms often moving the share price.

Automatically filtered to this Toolkit instance's start_date and end_date.

**Also known as:** analyst ratings, upgrades and downgrades, analyst grades.

**Args:**

- <u>overwrite (bool):</u> Defines whether to overwrite the existing data.
- <u>show_columns (list[str] &#124; None):</u> A list of column names to keep in the result. Invalid
names are reported and ignored. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The grades per ticker, indexed by date and grading company.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NKE"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-10-01",
    end_date="2025-12-31",
)

toolkit.get_stock_grades()
```

Which returns:

|                                         | Previous Grade   | New Grade      | Action   |
|:----------------------------------------|:-----------------|:---------------|:---------|
| ('2025-10-01', 'Barclays')              | Equal Weight     | Equal Weight   | Maintain |
| ('2025-10-01', 'JP Morgan')             | Overweight       | Overweight     | Maintain |
| ('2025-10-01', 'Morgan Stanley')        | Equal Weight     | Equal Weight   | Maintain |
| ('2025-10-01', 'Needham')               | Buy              | Buy            | Maintain |
| ('2025-10-01', 'Piper Sandler')         | Overweight       | Overweight     | Maintain |
| ('2025-10-01', 'Stifel')                | Hold             | Hold           | Maintain |
| ('2025-10-01', 'Telsey Advisory Group') | Market Perform   | Market Perform | Maintain |
| ('2025-10-01', 'Truist Securities')     | Buy              | Buy            | Maintain |
| ('2025-10-02', 'Keybanc')               | Sector Weight    | Overweight     | Upgrade  |
| ('2025-11-13', 'Wells Fargo')           | Equal Weight     | Overweight     | Upgrade  |
| ('2025-12-09', 'Citigroup')             | Neutral          | Neutral        | Maintain |
| ('2025-12-10', 'Telsey Advisory Group') | Market Perform   | Market Perform | Maintain |
| ('2025-12-12', 'BTIG')                  | Buy              | Buy            | Maintain |
| ('2025-12-19', 'B of A Securities')     | Buy              | Buy            | Maintain |
| ('2025-12-19', 'Barclays')              | Equal Weight     | Equal Weight   | Maintain |
| ('2025-12-19', 'Bernstein')             | Outperform       | Outperform     | Maintain |
| ('2025-12-19', 'Citigroup')             | Neutral          | Neutral        | Maintain |
| ('2025-12-19', 'Goldman Sachs')         | Buy              | Buy            | Maintain |
| ('2025-12-19', 'Guggenheim')            | Buy              | Buy            | Maintain |
| ('2025-12-19', 'Needham')               | Buy              | Buy            | Maintain |
| ('2025-12-19', 'Piper Sandler')         | Overweight       | Overweight     | Maintain |
| ('2025-12-19', 'Stifel')                | Hold             | Hold           | Maintain |
| ('2025-12-19', 'Telsey Advisory Group') | Market Perform   | Market Perform | Maintain |
| ('2025-12-19', 'Truist Securities')     | Buy              | Buy            | Maintain |
| ('2025-12-19', 'UBS')                   | Neutral          | Neutral        | Maintain |
| ('2025-12-19', 'Wells Fargo')           | Overweight       | Overweight     | Maintain |

---

## get_earnings_call_transcripts
Obtain the earnings call transcripts of each company: the full text of the call, with management's prepared remarks followed by the questions of analysts and the answers. Transcripts explain the numbers in the financial statements in management's own words, and with that are a strong input for text analysis and AI models, e.g. to track sentiment, guidance or recurring themes over time.

A transcript is long (often 40,000 to 60,000 characters) and every quarter is a separate request. By default only the most recent transcript is retrieved. With fiscal_period (e.g. "2025Q4") the call of that fiscal quarter is retrieved, and with latest=False every transcript between this Toolkit instance's start_date and end_date. A fiscal period without a transcript is logged together with the most recent periods that do have one. Each transcript is cached on its own, since a published transcript does not change, so a quarter is only retrieved once.

**Also known as:** earnings call, conference call transcript, earnings transcript.

**Args:**

- <u>latest (bool):</u> Whether to only retrieve the most recent transcript. When False,
every transcript between the start_date and end_date is retrieved. Defaults to True.
- <u>fiscal_period (str &#124; None):</u> The fiscal quarter of the call to retrieve, written as
"2025Q4" (or "2025-Q4", "Q4 2025"). It is the company's own fiscal year, which
differs from the calendar year for e.g. Apple and Microsoft. Takes precedence
over latest. Defaults to None.
- <u>overwrite (bool):</u> Defines whether to overwrite the existing data.

**Returns:**

pd.DataFrame: The date and transcript per ticker, indexed by fiscal period.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NVDA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

transcripts = toolkit.get_earnings_call_transcripts(fiscal_period="2025Q4")

transcripts["Transcript"].str[:80]
```

Which returns:

| Fiscal Period   | Transcript                                                                       |
|:----------------|:---------------------------------------------------------------------------------|
| 2025Q4          | Christa: Good afternoon. My name is Christa, and I will be your conference opera |

---

## get_historical_statistics
Retrieve statistics about each ticker's historical data. This is especially useful to understand why certain tickers might fluctuate more than others as it could be due to local regulations or the currency the instrument is denoted in. It returns:

- Currency: The currency the instrument is denoted in.
- Symbol: The symbol of the instrument.
- Exchange Name: The name of the exchange the instrument is listed on.
- Instrument Type: The type of instrument.
- First Trade Date: The date the instrument was first traded.
- Regular Market Time: The time the instrument is traded.
- GMT Offset: The GMT offset.
- Timezone: The timezone the instrument is traded in.
- Exchange Timezone Name: The name of the timezone the instrument is traded in.

**Also known as:** listing details, instrument information, exchange and currency.

**Returns:**

pd.DataFrame: A DataFrame containing the statistics for each ticker.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["ASML.AS", "ASML"],
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.get_historical_statistics().loc[
    ["Currency", "Exchange Name", "Instrument Type", "First Trade Date", "Exchange Timezone Name"]
]
```

Which returns:

|                        | ASML.AS          | ASML             |
|:-----------------------|:-----------------|:-----------------|
| Currency               | EUR              | USD              |
| Exchange Name          | AMS              | NMS              |
| Instrument Type        | EQUITY           | EQUITY           |
| First Trade Date       | 1998-07-20       | 1995-03-15       |
| Exchange Timezone Name | Europe/Amsterdam | America/New_York |

---

## get_treasury_data
Retrieve daily, weekly, monthly, quarterly or yearly US Treasury yields for four maturities, 13 weeks, 5 years, 10 years and 30 years, from FinancialModelingPrep or, as a free alternative, YahooFinance. With the default divide_ohlc_by of 100 the yields are returned as decimals (0.042 is 4.2%).

A week, month, quarter or year holds the first (Open), highest, lowest and last (Close) yield of the period. The risk free rate the Performance, Risk and Models modules use for such a period is instead the average of the daily yields within it, which approximates what a holder earned over the period rather than where the yield happened to close at its end.

**Also known as:** US Treasury yields, yield curve, treasury rates.

**Args:**

- <u>period (str):</u> The interval at which the treasury data should be returned - daily, weekly, monthly, quarterly, or yearly.
- <u>fill_nan (bool):</u> Defines whether to forward fill NaN values. This defaults
to True to prevent holes in the dataset. This is especially relevant for
technical indicators.
- <u>risk_free_rate (str &#124; None, optional):</u> One maturity to return ('13w', '5y', '10y' or
'30y'). Defaults to None, which returns all four. The Toolkit's own risk free rate
stays the maturity set on the Toolkit either way.
- <u>divide_ohlc_by (int &#124; float &#124; None, optional):</u> A value to divide the yields by. Treasury
yields are published in percent, so this defaults to 100 to return decimals.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding set on the Toolkit.
- <u>show_errors (bool, optional):</u> Whether to report retrieval errors. Defaults to False.
- <u>enforce_source (str &#124; None, optional):</u> Forces this specific call to use a given
source, either "FinancialModelingPrep" or "YahooFinance". This takes precedence
over the source set on the Toolkit itself. Defaults to None, which falls back to
the Toolkit's own enforce_source.

**Returns:**

pd.DataFrame: A DataFrame containing the treasury data.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.get_treasury_data(period="monthly")["Close"]
```

Which returns:

| Date    |   13 Week |   5 Year |   10 Year |   30 Year |
|:--------|----------:|---------:|----------:|----------:|
| 2025-01 |    0.0419 |   0.0436 |    0.0457 |    0.0481 |
| 2025-02 |    0.0419 |   0.0403 |    0.0423 |    0.0452 |
| 2025-03 |    0.0419 |   0.0398 |    0.0425 |    0.0461 |
| 2025-04 |    0.0419 |   0.0375 |    0.0418 |    0.0468 |
| 2025-05 |    0.0423 |   0.0398 |    0.0442 |    0.0493 |
| 2025-06 |    0.0419 |   0.038  |    0.0423 |    0.0478 |
| 2025-07 |    0.0424 |   0.0396 |    0.0436 |    0.0489 |
| 2025-08 |    0.0404 |   0.037  |    0.0423 |    0.0492 |
| 2025-09 |    0.0385 |   0.0373 |    0.0415 |    0.0473 |
| 2025-10 |    0.0372 |   0.0372 |    0.041  |    0.0467 |
| 2025-11 |    0.037  |   0.036  |    0.0402 |    0.0466 |
| 2025-12 |    0.0355 |   0.0372 |    0.0416 |    0.0484 |

---

## get_exchange_rates
This functionality looks at the exchange rates between the currency of the historical data and the currency of the financial statements. Given that these can deviate from each other, e.g. the historical data is in USD but the financial statements are in EUR, it is important to adjust for this. This is especially relevant for models that use the historical data and the financial statements.

This function therefore shows the exchange rates that are used to convert the financial statements to the currency of the historical data. The historical market data is quote currency and the financial statements are base currency.

Note that you can get currency data from any currency as well by supplying the currency as a ticker. For example, if you want to get the exchange rates between USD and EUR you can use USDEUR=X as a ticker.

Important to note is that when an api_key is included in the Toolkit initialization that the data collection defaults to FinancialModelingPrep which is a more stable source and utilises your subscription. However, if this is undesired, it can be disabled by setting enforce_source to "YahooFinance". If data collection fails from FinancialModelingPrep it automatically reverts back to YahooFinance.

**Also known as:** currency exchange, FX rates, foreign exchange rates.

**Args:**

- <u>period (str):</u> The interval at which the historical data should be
returned - daily, weekly, monthly, quarterly, or yearly.
Defaults to "daily".
- <u>return_column (str):</u> The column to use for the return calculation. Defaults to "Adj Close".
- <u>fill_nan (bool):</u> Defines whether to forward fill NaN values. This defaults
to True to prevent holes in the dataset. This is especially relevant for
technical indicators.
- <u>overwrite (bool):</u> Defines whether to overwrite the existing data.
- <u>rounding (int):</u> Defines the number of decimal places to round the returned data to. Defaults
to None, which uses the rounding of the Toolkit. The rates the financial statements are
translated with are never rounded.
- <u>show_ticker_seperation (bool, optional):</u> A boolean representing whether to show which tickers
acquired data from FinancialModelingPrep and which tickers acquired data from YahooFinance.

**Raises:**

ValueError: If an invalid value is specified for period.

**Returns:**

pandas.DataFrame: The historical exchange rate data.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    "ASML",
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.get_exchange_rates(period="monthly")
```

Which returns:

| Date    |   Open |   High |    Low |   Close |   Adj Close |      Volume |   Return |   Cumulative Return |
|:--------|-------:|-------:|-------:|--------:|------------:|------------:|---------:|--------------------:|
| 2025-03 | 1.0402 | 1.0954 | 1.0388 |  1.0815 |        1.08 | 1.1265e+07  |   0.0385 |              0.8926 |
| 2025-04 | 1.0815 | 1.1573 | 1.0778 |  1.1328 |        1.13 | 1.3243e+07  |   0.0463 |              0.9339 |
| 2025-05 | 1.1328 | 1.1422 | 1.1065 |  1.1346 |        1.13 | 9.02118e+06 |   0      |              0.9339 |
| 2025-06 | 1.1346 | 1.1788 | 1.1345 |  1.1787 |        1.18 | 8.07454e+06 |   0.0442 |              0.9752 |
| 2025-07 | 1.1787 | 1.183  | 1.1401 |  1.1415 |        1.14 | 7.03696e+06 |  -0.0339 |              0.9421 |
| 2025-08 | 1.1417 | 1.1743 | 1.1392 |  1.1707 |        1.17 | 3.44184e+06 |   0.0263 |              0.9669 |
| 2025-09 | 1.1696 | 1.1919 | 1.1608 |  1.1734 |        1.17 | 3.49176e+06 |   0      |              0.9669 |
| 2025-10 | 1.1736 | 1.1779 | 1.1522 |  1.1536 |        1.15 | 4.08101e+06 |  -0.0171 |              0.9504 |
| 2025-11 | 1.153  | 1.1656 | 1.1469 |  1.1601 |        1.16 | 3.2838e+06  |   0.0087 |              0.9587 |
| 2025-12 | 1.1594 | 1.1808 | 1.1589 |  1.1746 |        1.17 | 2.67505e+06 |   0.0086 |              0.9669 |

---

## get_balance_sheet_statement
Retrieves the balance sheet statement data for the specified tickers. The balance sheet statement is a financial statement that provides a snapshot of a company's financial position at a specific point in time. It shows the company's assets, liabilities, and shareholders' equity. The balance sheet statement is divided into three main sections:

- Assets: Assets are resources owned by the company that have economic value and can be used to generate revenue. Assets are typically divided into current assets and non-current assets.
- Liabilities: Liabilities are obligations that the company owes to external parties. Liabilities are also divided into current liabilities and non-current liabilities.
- Shareholders' Equity: Shareholders' equity represents the company's net worth or book value. It is calculated as the difference between the company's assets and liabilities.

Note that the balance sheet statement is a financial statement that provides a snapshot of a company's financial position at a specific point in time. Therefore, trailing results are not available for this statement.

With convert_currency, the statement is converted to the currency of the historical data at the closing rate, the exchange rate at the end of each period (IAS 21.39).

**Also known as:** assets, liabilities, shareholders equity, financial position.

**Args:**

- <u>enforce_source (str &#124; None, optional):</u> Forces this specific call to use a given
source, either "FinancialModelingPrep" or "YahooFinance". This takes precedence
over the source set on the Toolkit itself, so one instance can pull historical
data from the free Yahoo Finance source while still using a FinancialModelingPrep
key for the financial statements (or the other way around). Defaults to None,
which falls back to the Toolkit's own enforce_source.
- <u>overwrite (bool):</u> Defines whether to overwrite the existing data.
- <u>rounding (int):</u> Defines the number of decimal places to round the data to.
- <u>growth (bool):</u> Defines whether to return the growth of the data.
- <u>lag (int &#124; list[int]):</u> Defines the number of periods to lag the growth data by.
E.g. 4 with quarterly data gives the growth against the same quarter a year earlier.
- <u>show_columns (list[str] &#124; None):</u> A list of column names to keep in the result. Invalid
names are reported and ignored. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: A pandas DataFrame with the retrieved balance sheet statement data.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NEE", "DUK", "SO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.get_balance_sheet_statement(show_columns=["Total Debt"])
```

Which returns:

|     |       2021 |       2022 |       2023 |       2024 |       2025 |
|:----|-----------:|-----------:|-----------:|-----------:|-----------:|
| DUK | 6.8263e+10 | 7.4911e+10 | 8.0457e+10 | 8.523e+10  | 9.0869e+10 |
| NEE | 5.4827e+10 | 6.4966e+10 | 7.3211e+10 | 8.2333e+10 | 9.5619e+10 |
| SO  | 5.547e+10  | 5.9135e+10 | 6.349e+10  | 6.6277e+10 | 7.4075e+10 |

---

## get_income_statement
Retrieves the income statement data for the specified tickers. The income statement is a financial statement that shows a company's revenues and expenses over a specific period. It is used to calculate a company's net income.

The income statement is a financial statement that shows a company's revenues and expenses over a specific period. Therefore, trailing results are available for this statement. A trailing result sums each item over the window, except the Weighted Average Shares, Weighted Average Shares Diluted and Tax Rate for Calcs rows, which keep the value of the latest period.

With convert_currency, the statement is converted to the currency of the historical data at the average exchange rate of each period, as IAS 21.39-40 does for income and expenses. EPS and EPS Diluted are converted as well; share counts and ratios are not.

**Also known as:** profit and loss, revenue, net income, earnings, P&L statement.

**Args:**

- <u>enforce_source (str &#124; None, optional):</u> Forces this specific call to use a given
source, either "FinancialModelingPrep" or "YahooFinance". This takes precedence
over the source set on the Toolkit itself, so one instance can pull historical
data from the free Yahoo Finance source while still using a FinancialModelingPrep
key for the financial statements (or the other way around). Defaults to None,
which falls back to the Toolkit's own enforce_source.
- <u>overwrite (bool):</u> Defines whether to overwrite the existing data.
- <u>rounding (int):</u> Defines the number of decimal places to round the data to.
- <u>growth (bool):</u> Defines whether to return the growth of the data.
- <u>lag (int &#124; list[int]):</u> Defines the number of periods to lag the growth data by.
- <u>trailing (int):</u> Defines whether to select a trailing period.
E.g. when selecting 4 with quarterly data, the TTM is calculated.
- <u>show_columns (list[str] &#124; None):</u> A list of column names to keep in the result. Invalid
names are reported and ignored. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: A pandas DataFrame with the retrieved income statement data.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NKE"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.get_income_statement(show_columns=["Revenue", "Net Income"])
```

Which returns:

|            |      2021 |       2022 |       2023 |       2024 |       2025 |
|:-----------|----------:|-----------:|-----------:|-----------:|-----------:|
| Revenue    | 4.671e+10 | 5.1217e+10 | 5.1362e+10 | 4.6309e+10 | 4.6398e+10 |
| Net Income | 6.046e+09 | 5.07e+09   | 5.7e+09    | 3.219e+09  | 3.108e+09  |

---

## get_cash_flow_statement
Retrieves the cash flow statement data for the specified tickers. The cash flow statement is a financial statement that shows how changes in balance sheet accounts and income affect cash and cash equivalents. It breaks the analysis down to operating, investing and financing activities.

The cash flow statement is a financial statement that shows how changes in balance sheet accounts and income affect cash and cash equivalents. Therefore, trailing results are available for this statement. A trailing result sums each cash flow over the window, while Cash Beginning of Period is the cash at the beginning of the first period of the window and Cash End of Period the cash at the end of the last one.

With convert_currency, the cash flows are converted to the currency of the historical data at the average exchange rate of each period (IAS 7.25), Cash End of Period at the closing rate of the period and Cash Beginning of Period at the closing rate of the period before, so it equals the Cash End of Period before it. Net Change in Cash is the change in the converted cash and Forex Changes on Cash holds the effect of the exchange rate changes on the cash held (IAS 7.28).

**Also known as:** operating cash flow, investing activities, financing activities.

**Args:**

- <u>enforce_source (str &#124; None, optional):</u> Forces this specific call to use a given
source, either "FinancialModelingPrep" or "YahooFinance". This takes precedence
over the source set on the Toolkit itself, so one instance can pull historical
data from the free Yahoo Finance source while still using a FinancialModelingPrep
key for the financial statements (or the other way around). Defaults to None,
which falls back to the Toolkit's own enforce_source.
- <u>overwrite (bool):</u> Defines whether to overwrite the existing data.
- <u>rounding (int):</u> Defines the number of decimal places to round the data to.
- <u>growth (bool):</u> Defines whether to return the growth of the data.
- <u>lag (int &#124; list[int]):</u> Defines the number of periods to lag the growth data by.
- <u>trailing (int):</u> Defines whether to select a trailing period.
E.g. when selecting 4 with quarterly data, the TTM is calculated.
- <u>show_columns (list[str] &#124; None):</u> A list of column names to keep in the result. Invalid
names are reported and ignored. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: A pandas DataFrame with the retrieved cash flow statement data.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["CVX"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.get_cash_flow_statement(
    show_columns=["Operating Cash Flow", "Capital Expenditure", "Free Cash Flow", "Dividends Paid"]
)
```

Which returns:

|                     |        2021 |        2022 |        2023 |        2024 |        2025 |
|:--------------------|------------:|------------:|------------:|------------:|------------:|
| Operating Cash Flow |  2.9187e+10 |  4.9602e+10 |  3.5609e+10 |  3.1492e+10 |  3.3939e+10 |
| Capital Expenditure | -8.1e+09    | -1.1974e+10 | -1.5829e+10 | -1.6448e+10 | -1.7347e+10 |
| Free Cash Flow      |  2.1087e+10 |  3.7628e+10 |  1.978e+10  |  1.5044e+10 |  1.6592e+10 |
| Dividends Paid      | -1.0179e+10 | -1.0968e+10 | -1.1336e+10 | -1.18e+10   | -1.2751e+10 |

---

## get_statistics_statement
Retrieves the filing details of each financial statement period: the reported currency, the CIK, the filing and acceptance dates, the fiscal period and the links to the filing. With convert_currency, the Toolkit uses the reported currency to convert the financial statements to the currency of the historical data.

Note that this also obtains the balance sheet statement at the same time given that it's the same API call. This is done to reduce the number of API calls to FinancialModelingPrep.

**Also known as:** filing details, reporting metadata, reported currency.

**Args:**

- <u>enforce_source (str &#124; None, optional):</u> Forces this specific call to use a given
source, either "FinancialModelingPrep" or "YahooFinance". This takes precedence
over the source set on the Toolkit itself, so one instance can pull historical
data from the free Yahoo Finance source while still using a FinancialModelingPrep
key for the financial statements (or the other way around). Defaults to None,
which falls back to the Toolkit's own enforce_source.
- <u>overwrite (bool):</u> Defines whether to overwrite the existing data.
- <u>rounding (int):</u> Defines the number of decimal places to round the data to.
- <u>show_columns (list[str] &#124; None):</u> A list of column names to keep in the result. Invalid
names are reported and ignored. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: A pandas DataFrame with the retrieved statistics statement data.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["KO", "PEP"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.get_statistics_statement(show_columns=["Accepted Date"]).T
```

Which returns:

| date   | KO                  | PEP                 |
|:-------|:--------------------|:--------------------|
| 2020   | 2021-02-25 13:47:17 | 2021-02-10 17:41:49 |
| 2021   | 2022-02-22 15:45:48 | 2022-02-09 18:03:39 |
| 2022   | 2023-02-21 16:03:20 | 2023-02-08 18:06:37 |
| 2023   | 2024-02-20 13:21:24 | 2024-02-08 17:58:51 |
| 2024   | 2025-02-20 15:17:12 | 2025-02-03 18:22:47 |
| 2025   | 2026-02-20 09:46:32 | 2026-02-02 18:07:04 |

---

## get_normalization_files
Copies the normalization files to a folder based on path. By default, this is the path of the 'Downloads' folder.

This function is relevant if you want to supply your own datasets. See the external datasets guide for how: [https://www.jeroenbouma.com/projects/financetoolkit/docs/external-datasets](https://www.jeroenbouma.com/projects/financetoolkit/docs/external-datasets){:target="_blank"}

The same function is available without a Toolkit instance as `from financetoolkit import get_normalization_files`.

**Args:**

- <u>path (str, optional):</u> The folder to save the files to. Defaults to "", which
saves them to the 'Downloads' folder of your home directory.

**Returns:**

None: The four csv files (balance, income, cash and statistics) are saved to
the chosen folder.

---

## get_cache_contents
Show what the cache currently holds, grouped by source and dataset.

The cache stores data per source, per dataset and per entity (a ticker, a country, a series identifier), which makes it possible to remove part of it rather than all of it. This method is the counterpart to clear_cache: it shows what is there so that removing something is an informed decision.

The cache is inspected even when this Toolkit was created with use_cached_data=False, so a cache filled by an earlier session can always be reviewed.

**Returns:**

pd.DataFrame: One row per source and dataset combination, with the number
of entities, the number of stored entries and when they were written.
An empty DataFrame when the cache holds nothing.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.get_historical_data()

toolkit.get_cache_contents()
```

Which returns:

|    | source                | dataset                             |   entities |   entries | oldest_write        | newest_write        |
|---:|:----------------------|:------------------------------------|-----------:|----------:|:--------------------|:--------------------|
| 25 | FinancialModelingPrep | earnings_calendar                   |          4 |         4 | 2026-10-24 18:40:06 | 2026-10-24 18:40:06 |
| 26 | FinancialModelingPrep | earnings_call_transcripts           |          2 |         2 | 2026-10-24 18:41:46 | 2026-10-24 18:41:46 |
| 27 | FinancialModelingPrep | earnings_call_transcripts_selection |          2 |         2 | 2026-10-24 18:41:46 | 2026-10-24 18:41:46 |
| 28 | FinancialModelingPrep | employee_count                      |          2 |         2 | 2026-10-24 18:41:06 | 2026-10-24 18:41:06 |
| 29 | FinancialModelingPrep | esg_scores                          |          3 |         3 | 2026-10-24 18:40:40 | 2026-10-24 18:40:40 |

---

## clear_cache
Remove cached data, either all of it or only the part you specify.

The Finance Toolkit never clears the cache on its own. A cache can represent a large amount of downloaded data and a meaningful part of an API quota, so discarding it is always an explicit action. Even a change in the cache's own internal structure only produces a warning pointing at this method rather than removing anything.

Because the cache is stored per source, per dataset and per entity, removal can be narrowed instead of wholesale. Clearing a single stale ticker, or everything retrieved from one provider, leaves the rest of the cache intact.

**Args:**

- <u>source (str &#124; None):</u> Only remove data from this source, for example
"FinancialModelingPrep", "YahooFinance", "OECD", "FRED" or
"GlobalMacroDatabase". These match the names used by enforce_source.
Defaults to None, which matches every source.
- <u>dataset (str &#124; None):</u> Only remove this dataset within the source, for
example "historical", "intraday" or "statements". Defaults to None,
which matches every dataset.
- <u>ticker (str &#124; None):</u> Only remove this entity, for example "AAPL" or a
country code for macroeconomic data. Defaults to None, which matches
every entity.
- <u>confirm (bool):</u> Required to be True when no source, dataset or ticker is
given, since that removes the entire cache. Defaults to False.

**Raises:**

ValueError: If the whole cache would be removed without confirm being set.

**Returns:**

int: The number of stored entries that were removed.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "MSFT"], api_key="FINANCIAL_MODELING_PREP_KEY")

# Remove only the price history of a single ticker
toolkit.clear_cache(source="YahooFinance", ticker="AAPL")

# Remove everything retrieved from the OECD
toolkit.clear_cache(source="OECD")

# Remove the entire cache
toolkit.clear_cache(confirm=True)
```

---

