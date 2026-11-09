---
title: Performance
seo_title: "Performance Module | Finance Toolkit"
seo_title_suffix: false
excerpt: The Performance module is meant to calculate important performance metrics such as Sharpe Ratio, Sortino Ratio, Treynor Ratio, Information Ratio, Jensen's Alpha, Beta, Capital Asset Pricing Model, R-Squared and more.
description: "Reference for every function and parameter in the Finance Toolkit's Performance module: Sharpe, Sortino, Treynor ratios, Jensen's Alpha, Beta and CAPM."
author_profile: false
permalink: /projects/financetoolkit/docs/performance
classes: wide-sidebar
layout: single
redirect_from:
    - /performance
    - /projects/financetoolkit/performance-notebook
sidebar:
    nav: "financetoolkit-docs-performance"
---

The Performance module calculates important performance metrics such as the Sharpe Ratio, Sortino Ratio, Treynor Ratio, Information Ratio, Jensen's Alpha, Beta, Capital Asset Pricing Model (CAPM), R-Squared and more.

Use it in Claude, ChatGPT or another AI assistant through the [Finance Toolkit MCP](/projects/financetoolkit/mcp), or install the Python package:

```python
pip install financetoolkit -U
```

{% include algolia.html %}

{% include financetoolkit-getting-started/performance.md %}

## collect_all_metrics
Calculates and collects all performance metrics.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the
Toolkit is initialised with quarterly=True, otherwise "yearly".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Performance metrics calculated based on the specified parameters, with a
Multi Index of (metric, ticker) as the columns. For a single-ticker Toolkit the ticker
level is dropped. `Returns` and `Excess Return` are only included when `period` is not
"daily".

**Notes:**

- The method calculates various performance metrics for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the ratio values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.performance.collect_all_metrics().xs("AAPL", level=1, axis=1)
```

Which returns:

|      |    Alpha |   Beta |     CAPM |   Jensen's Alpha |   Treynor Ratio |   Sharpe Ratio |   Sortino Ratio |   Ulcer Performance Index |   Calmar Ratio |   Sterling Ratio |   Burke Ratio |   Omega Ratio |   Kappa Ratio |   Gain to Pain Ratio |   Win Rate |   Upside Capture Ratio |   Downside Capture Ratio |   M2 Ratio |   Tracking Error |   Information Ratio |   Appraisal Ratio |   STARR Ratio |   Rachev Ratio |   Returns |   Excess Return |
|:-----|---------:|-------:|---------:|-----------------:|----------------:|---------------:|----------------:|--------------------------:|---------------:|-----------------:|--------------:|--------------:|--------------:|---------------------:|-----------:|-----------------------:|-------------------------:|-----------:|-----------------:|--------------------:|------------------:|--------------:|---------------:|----------:|----------------:|
| 2022 |  -0.0822 | 1.3025 |  -0.2458 |          -0.0182 |         -0.2254 |        -0.0482 |         -0.0675 |                   -4.4186 |        -0.8706 |          -1.0669 |       -0.1137 |        0.8943 |       -0.052  |              -0.1057 |     0.4781 |                 1.3036 |                   1.3242 |    -0.1698 |           0.0115 |             -0.025  |           -0.1098 |       -0.4128 |         1.0788 |   -0.2638 |         -0.2934 |
| 2023 |   0.2283 | 1.1148 |   0.2873 |           0.2028 |          0.4041 |         0.1189 |          0.1839 |                   13.8927 |         3.2719 |           3.3669 |        0.5152 |        1.4099 |        0.1284 |               0.4099 |     0.576  |                 1.1755 |                   0.9726 |     0.3296 |           0.009  |              0.0794 |            1.44   |        1.0736 |         1.0726 |    0.489  |          0.4494 |
| 2024 |   0.0583 | 0.9686 |   0.2423 |           0.0648 |          0.2736 |         0.07   |          0.1071 |                    7.7225 |         1.9958 |           1.9699 |        0.2621 |        1.2509 |        0.0767 |               0.2509 |     0.5    |                 1.1049 |                   1.0583 |     0.189  |           0.0121 |              0.0207 |            0.3386 |        0.5644 |         1.1443 |    0.3069 |          0.2648 |
| 2025 |  -0.0867 | 1.2551 |   0.2115 |          -0.121  |          0.0379 |         0.0188 |          0.0283 |                    0.9488 |         0.2913 |           0.445  |        0.0249 |        1.0903 |        0.0186 |               0.0903 |     0.472  |                 1.0147 |                   1.1139 |     0.0714 |           0.0139 |             -0.0127 |           -0.5668 |        0.0659 |         1.0729 |    0.0904 |          0.0475 |
| 2021 | nan      | 1.3196 | nan      |         nan      |        nan      |         0.0859 |          0.129  |                  nan      |       nan      |         nan      |      nan      |        1.2632 |        0.0943 |               0.2632 |     0.4921 |                 1.3706 |                   1.432  |   nan      |           0.0118 |              0.0266 |          nan      |      nan      |         0.9957 |    0.3811 |          0.3667 |

---

## get_beta
Calculate the Beta, a measurement that assess the systematic risk of a stock or investment.

Beta is a financial metric used to assess the systematic risk of a stock or investment in relation to the overall market. It provides valuable insights into how a particular asset's returns tend to move in response to fluctuations in the broader market. A stock's Beta is calculated by analyzing its historical price movements and their correlation with the movements of a market index, typically the benchmark index like the S&P 500.

The formula is as follows:

$$
\text{Beta} = \text{Covariance of Asset Returns and Benchmark Returns} / \text{Variance of Benchmark Returns}
$$

For a given period, for example monthly, this translates into the following:

$$
\text{Beta} = \text{Monthly Covariance of Asset Returns and Benchmark Returns} / \text{Monthly Variance of Benchmark Returns}
$$

Beta is read against 1, the benchmark's own beta: above 1 the asset tends to amplify market moves, below 1 to dampen them. Each period's Beta comes from the daily returns within that period, so a yearly figure rests on about 250 observations and can swing with a single turbulent month; a rolling window (for example period='monthly' with rolling=36) gives a steadier estimate for cost of capital work. A Beta close to zero can come from a low correlation with the market rather than from low volatility, so it is worth checking both before calling a stock defensive.

**See definition:** [https://en.wikipedia.org/wiki/Beta_(finance)](https://en.wikipedia.org/wiki/Beta_(finance)){:target="_blank"}

**Also known as:** market sensitivity, systematic risk.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If you select
period = 'monthly' and set rolling to 12 you obtain the rolling 12-month Beta. Defaults to None.
- <u>method (str, optional):</u> The estimator of the Beta. Defaults to "ols". Choose from:
- "ols": the covariance over the benchmark variance (the formula above).
- "blume": the adjusted Beta of Bloomberg, 0.67 x OLS Beta + 0.33 (Blume, 1971, 1975).
- "vasicek": the OLS Beta shrunk towards the mean Beta of the tickers by the precision of
each estimate (Vasicek, 1973).
- "dimson": the sum of the slopes on the lagged, same and leading benchmark returns
(Dimson, 1979).
- "scholes_williams": the lagged, same and leading slopes over the benchmark's
autocorrelation (Scholes and Williams, 1977).
- "upside" or "downside": the OLS Beta on the days the benchmark rose or fell.
- <u>lags (int, optional):</u> The number of leads and lags of the Dimson Beta. Defaults to 1.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Beta values.

**Notes:**

- Daily Beta is not an option as the standard deviation for 1 day is close to zero. Therefore, it does
not give any useful insights.
- The method retrieves historical data and calculates the Beta for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.
- The OLS Beta of a stock that trades thinly or reacts to the market a day late understates its market
risk, because part of the reaction falls on the next day. Dimson and Scholes-Williams add the slopes on
the neighbouring benchmark returns to correct for that; their leads and lags come from the full history,
so the first day of a period uses the benchmark return of the day before.
- Blume found that Betas move towards 1 between estimation windows by about a third. Vasicek shrinks
each Beta in proportion to its uncertainty: the prior is the mean and sample variance (ddof=1) of the
OLS Betas of the tickers in the same period, so it depends on which tickers are passed. A single
ticker gets a prior mean of 1 (the market's Beta) with a variance of 0.25.
- The upside and downside Betas show asymmetric market exposure: a stock with a downside Beta above
its upside Beta falls harder in down markets than it rises in up markets. They follow empyrical's
up_alpha_beta and down_alpha_beta, which pick the observations by the benchmark's direction.
- Every estimator needs at least three observations in a period (Dimson: more than the number of
slopes plus one), otherwise the period is NaN.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NVDA", "TSLA", "JPM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_beta()
```

Which returns:

| Date   |   NVDA |   TSLA |    JPM |
|:-------|-------:|-------:|-------:|
| 2021   | 2.0431 | 1.9542 | 0.8376 |
| 2022   | 2.2001 | 1.7404 | 0.8815 |
| 2023   | 2.0217 | 2.247  | 0.8723 |
| 2024   | 2.6583 | 2.38   | 0.8006 |
| 2025   | 1.8727 | 2.2342 | 0.9481 |

The downside Beta shows how the same stocks moved on the days the S&P 500 fell:

```python
toolkit.performance.get_beta(method="downside")
```



| Date   |   NVDA |   TSLA |    JPM |
|:-------|-------:|-------:|-------:|
| 2021   | 2.0938 | 1.6149 | 0.7877 |
| 2022   | 1.9875 | 1.5848 | 0.7921 |
| 2023   | 2.1135 | 2.5952 | 1.048  |
| 2024   | 2.0508 | 2.6545 | 0.9306 |
| 2025   | 1.8311 | 1.9833 | 0.9638 |

---

## get_beta_implied_return
Calculate the Beta-Implied Return, the part of an asset's return that its Beta to the benchmark explains, and the Residual, the part that is the asset's own.

When the market falls 4% and a stock with a Beta of 1.8 falls 9%, the Beta accounts for about 7.2% of the fall (1.8 × 4%) and the remaining 1.8% is specific to the stock: news, earnings or sector moves that the market as a whole did not share. This is the market model of Sharpe (1963) without its intercept, the split behind event studies and return attribution, which reads a move against what the market alone would have produced.

The formula is as follows:

$$
\text{Implied Return} = \text{Beta} \cdot \text{Benchmark Return}
$$

$$
\text{Residual} = \text{Actual Return} - \text{Implied Return}
$$

The Beta of each period is estimated from the daily returns over the `beta_window` trading days that end on the day before the period starts, so the move being explained never helps estimate the Beta that explains it, and the figure is what an investor could have known at the start of the period. With the default daily period every row explains one day's move; a monthly or yearly period explains that month or year with the Beta known when it began.

**See definition:** [https://en.wikipedia.org/wiki/Single-index_model](https://en.wikipedia.org/wiki/Single-index_model){:target="_blank"}

**Also known as:** beta-adjusted return, market-implied move, idiosyncratic return, abnormal return.

**Args:**

- <u>period (str, optional):</u> The period whose returns are explained: "daily", "weekly", "monthly",
"quarterly" or "yearly". Defaults to "daily".
- <u>beta_window (int, optional):</u> The number of daily returns the Beta is estimated on. Defaults
to 252, about one year of trading days, a common length for a market model's
estimation window that is long enough for a stable Beta and short enough to follow
changes in the business.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).

**Returns:**

pd.DataFrame: The periods as rows and a MultiIndex of (measure, ticker) as columns, with the
measures Beta, Benchmark Return, Implied Return, Actual Return and Residual. All returns are
decimals.

**Notes:**

- Returns are total returns (Adj Close), the asset's and the benchmark's over the same period.
- The Implied Return leaves out the risk free rate: the CAPM's expected return, Risk Free Rate +
Beta × (Benchmark Return — Risk Free Rate), differs from it by (1 — Beta) × the risk free rate,
a few basis points per day, and is available through `get_capital_asset_pricing_model`.
- A period whose window has fewer than `beta_window` daily returns before it (the start of the
data or a recent listing) has no Beta, so its Implied Return and Residual are empty. Start the
Toolkit at least `beta_window` trading days before the first period of interest.
- The Beta is the ordinary least squares Beta of `get_beta`, on the daily returns of the window.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NVDA", "KO", "AMD", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-06-01",
    end_date="2026-11-05",
)

toolkit.performance.get_beta_implied_return().loc["2026-11-05"].unstack()
```

Which returns:

|                  |    NVDA |      KO |     AMD |    TSLA |
|:-----------------|--------:|--------:|--------:|--------:|
| Beta             |  1.8757 | -0.2777 |  3.2846 |  2.1039 |
| Benchmark Return | -0.0441 | -0.0441 | -0.0441 | -0.0441 |
| Implied Return   | -0.0827 |  0.0122 | -0.1448 | -0.0928 |
| Actual Return    | -0.0926 | -0.0007 | -0.1726 | -0.1077 |
| Residual         | -0.0099 | -0.0129 | -0.0278 | -0.0149 |

---

## get_capital_asset_pricing_model
CAPM, or the Capital Asset Pricing Model, is a financial model used to estimate the expected return on an investment, such as a stock or portfolio of stocks. It provides a framework for evaluating the risk and return trade-off of an asset or portfolio in relation to the overall market. CAPM is based on the following key components:

- Risk-Free Rate (Rf): This is the theoretical return an investor could earn from an investment with no risk of financial loss. It is typically based on the yield of a government bond.
- Market Risk Premium (Rm - Rf): This represents the additional return that investors expect to earn for taking on the risk of investing in the overall market as opposed to a risk-free asset. It is calculated as the difference between the expected return of the market (Rm) and the risk-free rate (Rf).
- Beta (β): Beta is a measure of an asset's or portfolio's sensitivity to market movements. It quantifies how much an asset's returns are expected to move in relation to changes in the overall market. A beta of 1 indicates that the asset moves in line with the market, while a beta greater than 1 suggests higher volatility, and a beta less than 1 indicates lower volatility.

The Capital Asset Pricing Model (CAPM) is a widely used financial model that helps in determining the expected return of an asset or portfolio based on its systematic risk and the prevailing risk-free rate in the market. CAPM provides insights into how an asset or investment should be priced in order to offer an appropriate rate of return, given its level of risk compared to the overall market.

The formula is as follows:

$$
\text{Capital Asset Pricing Model} = \text{Risk Free Rate} + \text{Beta} \cdot (\text{Benchmark Returns} - \text{Risk Free Rate})
$$

The CAPM here uses the benchmark's realised return of each period, so the result is the return the asset should have earned given what the market actually did. That makes it a yardstick for Jensen's Alpha rather than a forward-looking expected return. For a cost of equity, practitioners use an expected market risk premium instead of the realised one (see the Toolkit's `get_market_risk_premium`) together with a longer-run Beta. In periods in which the benchmark returns less than the risk-free rate, a high-Beta asset gets a lower required return than a low-Beta one.

**See definition:** [https://en.wikipedia.org/wiki/Capital_asset_pricing_model](https://en.wikipedia.org/wiki/Capital_asset_pricing_model){:target="_blank"}

**Also known as:** CAPM, expected return model.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>rolling (int, optional):</u> The rolling window size to use for the Beta component of the
calculation. If set, Beta is estimated over a rolling window of this many periods across
the full return history instead of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: CAPM values.

**Notes:**

- Daily CAPM is not an option as the standard deviation for 1 day is close to zero. Therefore, it does
not give any useful insights.
- The method retrieves historical data and calculates the CAPM for each asset in the Toolkit instance.
- The risk-free rate is the Toolkit's risk_free_rate, the 10-year US Treasury yield by default. Many
textbook definitions (Sharpe, 1994; the Ken French factors) use a short-term Treasury bill instead, which
the Toolkit uses when initialised with risk_free_rate="13w".
- If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["JPM", "GS", "MS"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2020-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_capital_asset_pricing_model()
```

Which returns:

| Date   |     JPM |      GS |      MS |
|:-------|--------:|--------:|--------:|
| 2021   |  0.2426 |  0.2808 |  0.3177 |
| 2022   | -0.1567 | -0.173  | -0.1915 |
| 2023   |  0.2334 |  0.276  |  0.3055 |
| 2024   |  0.2077 |  0.28   |  0.2632 |
| 2025   |  0.1702 |  0.221  |  0.2174 |

---

## get_factor_asset_correlations
Calculates factor exposures for each asset.

The major difference between the Fama and French Model here is that the correlation is taken as opposed to a Linear Regression in which the R-squared or Slope can be used to understand the exposure to each factor.

For assessing the exposure or influence of a stock to external factors, it's often preferable to use R-squared (R²) or Beta because it explicitly measures how well the factors explain the stock's returns. A higher R² indicates that the stock's returns are more closely related to the factors, and thus, the factors have a greater influence on the stock's performance.

However, since the results are closely related and tend to point into the same direction it could be fine to use correlations as well depending on the level of accuracy required.

The formula is as follows:

$$
\text{Excess Return} = \text{Daily Asset Return} - \text{Daily Risk Free Rate} (\text{RF})
$$

$$
\text{Factor Asset Correlation} = \text{Pearson Correlation} (\text{Daily Excess Return},\; \text{Daily Factor Return}),\;\; \text{using the daily Fama and French 5 Factor returns within each period (e.g. each year)}
$$

**Also known as:** factor exposure, asset correlations.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>factors_to_calculate (list of str, optional):</u> List of factors to calculate scores and residuals for.
Defaults to ["Mkt-RF", "SMB", "HML", "RMW", "CMA"].
- <u>region (str, optional):</u> The region whose factors to use: "United States", "Developed",
"Developed ex US", "Europe", "Japan", "Asia Pacific ex Japan" or "North America" (the
factors of Ken French's library for that region's stocks). Every region's factors are
U.S. dollar returns with the U.S. one-month Treasury bill as the risk-free rate (RF),
so a ticker quoted in another currency is best analysed with its U.S. dollar returns;
otherwise the exchange rate's moves end up in the factor loadings, mostly the market
beta. Defaults to "United States".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (list of str, optional):</u> Restrict the result to these top level columns.
Defaults to None, which returns every column.

**Returns:**

pd.DataFrame: Factor Asset Correlations, with a Multi Index of (ticker, factor)
as the columns and one row per period.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["CAT", "PFE", "ORCL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_factor_asset_correlations()["CAT"]
```

Which returns:

|      |   Mkt-RF |    SMB |     HML |     RMW |     CMA |
|:-----|---------:|-------:|--------:|--------:|--------:|
| 2025 |    0.698 | 0.2883 | -0.2279 | -0.2868 | -0.0246 |

---

## get_factor_correlations
Calculates factor correlations between each factor. This is useful to understand how correlated each factor is to each other. This is based off the Fama and French 5 Factor model which includes:

- Market Risk Premium (Mkt-RF): Represents the additional return that investors expect to earn for taking on the risk of investing in the overall market as opposed to a risk-free asset.
- Size Premium (SMB): Reflects the historical excess return of small-cap stocks over large-cap stocks.
- Value Premium (HML): Captures the historical excess return of value stocks over growth stocks.
- Profitability (RMW): Measures the historical excess return of high profitability stocks over low profitability stocks.
- Investment (CMA): Quantifies the historical excess return of low investment stocks over high investment stocks.

Optionally, it is also possible to see the correlation between the risk-free rate and each factor.

The formula is as follows:

$$
\text{Factor Correlation} = \text{Pearson Correlation} (\text{Daily Factor}\; A \;\text{Return},\; \text{Daily Factor}\; B \;\text{Return}),\;\; \text{using the daily Fama and French 5 Factor returns within each period (e.g. each year)}
$$

**Also known as:** factor model correlations.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>factors_to_calculate (list of str, optional):</u> List of factors to calculate scores and residuals for.
Defaults to ["Mkt-RF", "SMB", "HML", "RMW", "CMA"].
- <u>exclude_risk_free (bool, optional):</u> Whether to exclude the risk-free rate from the results. Defaults to True.
- <u>region (str, optional):</u> The region whose factors to use: "United States", "Developed",
"Developed ex US", "Europe", "Japan", "Asia Pacific ex Japan" or "North America" (the
factors of Ken French's library for that region's stocks). Every region's factors are
U.S. dollar returns with the U.S. one-month Treasury bill as the risk-free rate (RF).
Defaults to "United States".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).

**Returns:**

pd.DataFrame: Factor Correlations. One correlation matrix per period, stacked
into a Multi Index of (period, factor) rows with the factors as the columns and
restricted to the Toolkit's date range.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["SPY"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
    benchmark_ticker=None,
)

toolkit.performance.get_factor_correlations()
```

Which returns:

|                    |   Mkt-RF |     SMB |     HML |     RMW |    CMA |
|:-------------------|---------:|--------:|--------:|--------:|-------:|
| ('2025', 'Mkt-RF') |   1      |  0.1744 | -0.3814 | -0.4273 | 0.0586 |
| ('2025', 'SMB')    |   0.1744 |  1      |  0.2143 | -0.2924 | 0.2143 |
| ('2025', 'HML')    |  -0.3814 |  0.2143 |  1      |  0.3573 | 0.2218 |
| ('2025', 'RMW')    |  -0.4273 | -0.2924 |  0.3573 |  1      | 0.0657 |
| ('2025', 'CMA')    |   0.0586 |  0.2143 |  0.2218 |  0.0657 | 1      |

---

## get_fama_and_french_model
Calculate Fama and French 5 Factor model scores and residuals for a set of financial assets.

The Fama and French 5 Factor model is a widely used financial model that helps estimate the expected return of financial assets, such as stocks or portfolios, based on five key factors:

- Market Risk Premium (Mkt-RF): Represents the additional return that investors expect to earn for taking on the risk of investing in the overall market as opposed to a risk-free asset.
- Size Premium (SMB): Reflects the historical excess return of small-cap stocks over large-cap stocks.
- Value Premium (HML): Captures the historical excess return of value stocks over growth stocks.
- Profitability (RMW): Measures the historical excess return of high profitability stocks over low profitability stocks.
- Investment (CMA): Quantifies the historical excess return of low investment stocks over high investment stocks.

The model can perform both a Simple Linear Regression on each factor as well as a Multi Linear Regression which includes all factors. Generally, a multi linear regression is applied but if you wish to see individual R-squared values for each factor you can select the simple linear regression method.

The model performs a Linear Regression on each factor and defines the regression parameters and residuals for each asset over time based on its exposure to these factors.

The regression formula is as follows for the Multi Linear Regression:

$$
\text{Excess Return} = \text{Intercept} + \text{Beta1} \cdot \text{Mkt-RF} + \text{Beta2} \cdot \text{SMB} + \text{Beta3} \cdot \text{HML} + \text{Beta4} \cdot \text{RMW} + \text{Beta5} \cdot \text{CMA} + \text{Residuals}
$$

And the following for the Simple Linear Regression:

$$
\text{Excess Return} = \text{Intercept} + \text{Slope} \cdot \text{Factor Value} + \text{Residuals}
$$

So for a given factor, it should hold that the Excess Return equals the entire regression. Note that in this calculation the Excess Return refers to the Asset Return minus the Risk Free Rate as reported in the Fama and French dataset and will not be the same as the defined Excess Return in the historical data given that this is based on the Risk Free Rate defined in the initialization.

The regression is estimated on the daily observations falling inside each period, so its Intercept, Slope and Residuals are all on a daily scale. The `Factor Value` and `Residuals` columns reported by the Simple Linear Regression therefore describe the **last daily observation** within the period, which is the only reading for which the identity above holds - they are not period-aggregated quantities.

What is relevant to look at is the influence these factors have on each stock and how much each factor explains the stock return. E.g. you will generally see a pretty high influence (Beta or Slope) for the Market Risk Premium (Mkt-RF) factor as this is the main factor that explains the stock return (as also prevalent in the CAPM). The other factors can fluctuate greatly between stocks depending on which stocks you look at.

The slopes are read as tilts: a positive HML slope is a value tilt and a negative one a growth tilt, a negative SMB slope marks a large-cap profile, and RMW and CMA show exposure to profitable and conservatively investing firms. With about 250 daily observations per year the slopes of the smaller factors are noisy, so only loadings that are large and persist across periods say much about a stock or fund. The R Squared shows how much of the daily excess return the factors explain; a low value leaves most of the return to stock-specific news.

**Also known as:** Fama-French model, three-factor model, five-factor model, FF3, FF5.

**Args:**

- <u>period (str, optional):</u> The period for the calculation (e.g., "weekly", "monthly", "quarterly", "yearly").
Defaults to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise "yearly".
- <u>method (str, optional):</u> The regression method to use for the calculation. Defaults to 'multi'.
- <u>factors_to_calculate (list of str, optional):</u> List of factors to calculate scores and residuals for.
Defaults to ["Mkt-RF", "SMB", "HML", "RMW", "CMA"].
- <u>include_daily_residuals (bool, optional):</u> Whether to also return the pointwise (daily)
regression residuals as a second DataFrame. Defaults to False.
- <u>region (str, optional):</u> The region whose factors to use: "United States", "Developed",
"Developed ex US", "Europe", "Japan", "Asia Pacific ex Japan" or "North America" (the
factors of Ken French's library for that region's stocks). Every region's factors are
U.S. dollar returns with the U.S. one-month Treasury bill as the risk-free rate (RF),
so a ticker quoted in another currency is best analysed with its U.S. dollar returns;
otherwise the exchange rate's moves end up in the factor loadings, mostly the market
beta. Defaults to "United States".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratio values. Defaults to False.
- <u>lag (int or list of int, optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (list of str, optional):</u> Restrict the result to these top level columns.
Defaults to None, which returns every column.

**Returns:**

pd.DataFrame: Fama and French 5 Factor model scores for the specified assets, with a
Multi Index of (ticker, parameter) as the columns and one row per period. When
`include_daily_residuals` is True a tuple of (scores, residuals) is returned instead.

**Notes:**

- The dataset from Fama and French is not always fully up to date. Therefore, some periods could be excluded.
- Daily Fama and French results is not an option as it would attempt to do a linear regression on a
single data point which will not give any meaningful results.
- The method retrieves historical data and calculates regression parameters and residuals for each asset.
- The risk-free rate is typically represented by the return of a risk-free investment, such as a Treasury bond.
In this case, the Risk Free Rate from the Fama and French dataset is used.
- If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["IWM", "VTV", "MTUM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# Calculate Fama and French 5 Factor model scores
toolkit.performance.get_fama_and_french_model()["IWM"].drop(columns="Mean Squared Error (MSE)")
```

Which returns:

|      |   Intercept |   Mkt-RF Slope |   SMB Slope |   HML Slope |   RMW Slope |   CMA Slope |   R Squared |
|:-----|------------:|---------------:|------------:|------------:|------------:|------------:|------------:|
| 2021 |     -0.0003 |         1.0529 |      0.8267 |      0.0728 |     -0.1204 |     -0.0334 |      0.9868 |
| 2022 |     -0.0001 |         1.0343 |      0.893  |      0.0645 |     -0.0553 |      0.0654 |      0.9917 |
| 2023 |     -0.0001 |         1.0292 |      0.8647 |      0.141  |     -0.0731 |      0.0794 |      0.9871 |
| 2024 |      0      |         1.0396 |      0.8723 |      0.1568 |     -0.0685 |      0.0143 |      0.9838 |
| 2025 |      0      |         0.9702 |      0.8649 |      0.1317 |     -0.1871 |     -0.0235 |      0.9826 |

---

## get_carhart_four_factor_model
Calculate Carhart Four Factor model scores for a set of financial assets.

The Carhart Four Factor model extends the Fama and French Three Factor model with a momentum factor, based on the observation that stocks with high prior returns (winners) tend to keep outperforming stocks with low prior returns (losers) over the medium term:

- Market Risk Premium (Mkt-RF): The excess return of the market over the risk-free rate.
- Size Premium (SMB): The historical excess return of small-cap stocks over large-cap stocks.
- Value Premium (HML): The historical excess return of value stocks over growth stocks.
- Momentum (MOM): The historical excess return of prior winner stocks over prior loser stocks.

The model performs a Multi Linear Regression (ordinary least squares) on all four factors and defines the regression parameters for each asset over time based on its exposure to these factors.

The formula is as follows:

$$
\text{Excess Return} = \text{Daily Asset Return} - \text{Daily Risk Free Rate} (\text{RF},\; \text{from the Fama and French dataset})
$$

$$
\text{Excess Return} = \text{Intercept} + \text{Beta1} \cdot \text{Mkt-RF} + \text{Beta2} \cdot \text{SMB} + \text{Beta3} \cdot \text{HML} + \text{Beta4} \cdot \text{MOM} + \text{Residuals},\;\; \text{fitted on the daily returns within each period (e.g. each quarter)}
$$

For more information about the method, see the following paper:

- Carhart, M.M. (1997). "On Persistence in Mutual Fund Performance." The Journal of Finance, 52(1), 57-82.

**Also known as:** Carhart model, four-factor model, momentum-augmented Fama-French model.

**Args:**

- <u>period (str, optional):</u> The period for the calculation (e.g., "weekly", "monthly", "quarterly", "yearly").
Defaults to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise "yearly".
- <u>region (str, optional):</u> The region whose factors to use: "United States", "Developed",
"Developed ex US", "Europe", "Japan", "Asia Pacific ex Japan" or "North America" (the
factors of Ken French's library for that region's stocks). Every region's factors are
U.S. dollar returns with the U.S. one-month Treasury bill as the risk-free rate (RF),
so a ticker quoted in another currency is best analysed with its U.S. dollar returns;
otherwise the exchange rate's moves end up in the factor loadings, mostly the market
beta. Defaults to "United States".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratio values. Defaults to False.
- <u>lag (int or list of int, optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (list of str, optional):</u> Restrict the result to these top level columns.
Defaults to None, which returns every column.

**Returns:**

pd.DataFrame: Carhart Four Factor model scores for the specified assets, with a Multi
Index of (ticker, parameter) as the columns and one row per period.

**Notes:**

- The dataset from Ken French is not always fully up to date. Therefore, some periods could be excluded.
- Daily Carhart results is not an option as it would attempt to do a linear regression on a single data
point which will not give any meaningful results.
- The factors come from the Fama and French **three** factor file rather than the five factor file
used by `get_fama_and_french_model`. The two files agree on Mkt-RF, HML and RF but not on SMB: the
five factor SMB averages three separate size legs, while Carhart (1997) extends the three factor
model and therefore requires the three factor SMB.
- The risk-free rate is the Risk Free Rate reported in the Fama and French dataset (used here, rather
than the Toolkit's own risk-free rate, to stay consistent with the momentum factor's construction).
- If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["XOM", "HD", "ADBE"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_carhart_four_factor_model(period="quarterly")["XOM"].drop(
    columns="Mean Squared Error (MSE)"
)
```

Which returns:

|        |   Intercept |   Mkt-RF Slope |   SMB Slope |   HML Slope |   MOM Slope |   R Squared |
|:-------|------------:|---------------:|------------:|------------:|------------:|------------:|
| 2025Q1 |      0.0021 |         0.7335 |      0.2739 |      0.4818 |     -0.7225 |      0.317  |
| 2025Q2 |     -0.0002 |         0.8881 |     -0.7307 |      1.6062 |     -0.7248 |      0.6805 |
| 2025Q3 |      0.0003 |         0.3232 |     -0.1805 |      0.6496 |     -0.2369 |      0.2179 |
| 2025Q4 |      0.0005 |         0.4852 |     -0.2193 |      0.6778 |     -0.0933 |      0.1938 |

---

## get_style_analysis
Calculate the returns-based style analysis (Sharpe, 1992) of every ticker: the mix of style indices, such as growth and value, large and small caps or bonds, whose returns track the ticker's returns most closely. The weights are found by minimizing the variance of the difference between the ticker's return and the weighted style returns, with every weight between 0 and 1 and the weights adding up to 1, so they read as the effective asset mix of a fund without knowing its holdings.

The R Squared is the share of the ticker's variance the styles explain; what they do not explain is the Selection Return (the return of the manager's own choices, annualized) with its volatility, the Tracking Error. These three are in-sample: they are measured over the same returns the weights are fitted to, which flatters the fit, as the weights are chosen to explain exactly those returns.

A window estimates the weights over a rolling number of periods instead, which shows how a fund's style drifts over time, and adds Sharpe's out-of-sample measure of selection: the Out-of-Sample Selection Return of a date is the ticker's return of that period minus the return of that period of the style mix estimated over the window that ends one period earlier (Sharpe uses the previous 60 months). It is a return per period, not annualized, and NaN for the first window, which has no earlier estimate. Its average shows whether the manager added value beyond a passive mix of the styles the fund was known to follow.

By default the styles are Sharpe's asset classes as ETFs: IWD and IWF for US large cap value and growth, IWN and IWO for small cap value and growth, AGG for bonds and BIL for cash. Style tickers that are not in the Toolkit are retrieved for the same dates, and every Toolkit ticker that is not a style is analyzed against them. "Benchmark" can be one of them.

For more information, see the following paper:

- Sharpe, W.F. (1992). "Asset Allocation: Management Style and Performance Measurement." The Journal of Portfolio Management, 18(2), 7-19.

**Also known as:** returns-based style analysis, RBSA, style regression, effective asset mix, selection return.

**Args:**

- <u>style_tickers (str &#124; list[str] &#124; None, optional):</u> The tickers of the style indices, as a
list or a comma-separated string. Defaults to None, which uses IWD, IWF, IWN, IWO,
AGG and BIL.
- <u>period (str, optional):</u> The return frequency (daily, weekly, monthly, quarterly or
yearly). Defaults to "monthly".
- <u>window (int &#124; None, optional):</u> The number of periods to estimate the weights over on a
rolling basis, which adds the Out-of-Sample Selection Return. Defaults to None,
which uses every period.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the Toolkit.

**Returns:**

pd.DataFrame: Per ticker the weight of every style, the R Squared, the Selection Return
and the Tracking Error, or with a window the same and the Out-of-Sample Selection
Return per date (the last date of every window) and ticker. A ticker with no more
returns than there are styles (in a window) is NaN.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["ARKK", "BRK-B"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2019-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_style_analysis()
```

Which returns:

|       |    IWD |    IWF |   IWN |    IWO |   AGG |    BIL |   R Squared |   Selection Return |   Tracking Error |
|:------|-------:|-------:|------:|-------:|------:|-------:|------------:|-------------------:|-----------------:|
| ARKK  | 0      | 0.0091 |     0 | 0.9909 |     0 | 0      |      0.6123 |             0.0638 |           0.2632 |
| BRK-B | 0.8793 | 0      |     0 | 0      |     0 | 0.1207 |      0.5662 |             0.0425 |           0.1304 |

---

## get_alpha
Alpha, in a general sense, represents the excess return an investment generates relative to a benchmark or a risk-adjusted return. It can be positive (indicating the investment outperformed the benchmark) or negative (indicating underperformance).

The formula is as follows:

$$
\text{Alpha} = \text{Asset's Actual Return} - \text{Benchmark's Actual Return}
$$

**See definition:** [https://en.wikipedia.org/wiki/Alpha_(finance)](https://en.wikipedia.org/wiki/Alpha_(finance)){:target="_blank"}

**Also known as:** excess return, outperformance, active return.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>show_full_results (bool, optional):</u> Whether to show the actual and benchmark returns next to the
Alpha. Defaults to False.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set,
Alpha is calculated as the rolling mean excess return over this many periods across
the full return history instead of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Alpha values.

**Notes:**

- The method retrieves historical data and calculates the Alpha for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["COST", "WMT", "TGT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2020-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_alpha()
```

Which returns:

| Date   |    COST |     WMT |     TGT |
|:-------|--------:|--------:|--------:|
| 2021   |  0.2309 | -0.2676 |  0.0418 |
| 2022   | -0.0087 |  0.1772 | -0.1606 |
| 2023   |  0.2282 | -0.133  | -0.2753 |
| 2024   |  0.1474 |  0.4911 | -0.2715 |
| 2025   | -0.2311 |  0.0677 | -0.4221 |

---

## get_jensens_alpha
Calculate Jensen's Alpha, a measure of an asset's performance relative to its expected return based on the Capital Asset Pricing Model (CAPM).

Jensen's Alpha is used to assess whether an investment has outperformed or underperformed its expected return given its systematic risk, as represented by the asset's Beta.

The formula is as follows:

$$
\text{Jensen's Alpha} = \text{Asset's Actual Return} - \left[\text{Risk-Free Rate} + \text{Beta} \cdot (\text{Benchmark Return} - \text{Risk-Free Rate})\right]
$$

**See definition:** [https://en.wikipedia.org/wiki/Jensen%27s_alpha](https://en.wikipedia.org/wiki/Jensen%27s_alpha){:target="_blank"}

**Also known as:** Jensen alpha, risk-adjusted excess return.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>rolling (int, optional):</u> The rolling window size to use for the Beta component of the
calculation. If set, Beta is estimated over a rolling window of this many periods across
the full return history instead of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Jensen's Alpha values.

**Notes:**

- Daily Jensen's Alpha is not an option as the standard deviation for 1 day is close to zero. Therefore, it does
not give any useful insights.
- The method retrieves historical data and calculates the CAPM for each asset in the Toolkit instance.
- The risk-free rate is the Toolkit's risk_free_rate, the 10-year US Treasury yield by default. Many
textbook definitions (Sharpe, 1994; the Ken French factors) use a short-term Treasury bill instead, which
the Toolkit uses when initialised with risk_free_rate="13w".
- If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["UNH", "JNJ", "PFE"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2020-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_jensens_alpha()
```

Which returns:

| Date   |     UNH |     JNJ |     PFE |
|:-------|--------:|--------:|--------:|
| 2021   |  0.2601 | -0.0093 |  0.6493 |
| 2022   |  0.1608 |  0.0945 | -0.0261 |
| 2023   | -0.0951 | -0.2013 | -0.5539 |
| 2024   | -0.0911 | -0.0803 | -0.1158 |
| 2025   | -0.4155 |  0.4249 | -0.0976 |

---

## get_treynor_ratio
The Treynor Ratio, also known as Treynor's Measure or the Reward-to-Volatility Ratio, is a financial metric used to assess the risk-adjusted performance of an investment portfolio or asset. It measures the excess return generated by the portfolio per unit of systematic or market risk, often represented by Beta. The Treynor Ratio is a valuable tool for evaluating the performance of investments in relation to their market risk exposure.

The formula is as follows:

$$
\text{Treynor Ratio} = (\text{Portfolio's Return} - \text{Risk-Free Rate}) / \text{Portfolio Beta}
$$

**See definition:** [https://en.wikipedia.org/wiki/Treynor_ratio](https://en.wikipedia.org/wiki/Treynor_ratio){:target="_blank"}

**Also known as:** reward-to-volatility ratio.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>rolling (int, optional):</u> The rolling window size to use for the Beta component of the
calculation. If set, Beta is estimated over a rolling window of this many periods across
the full return history instead of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Treynor Ratio values.

**Notes:**

- Daily Treynor Ratio is not an option as the standard deviation for 1 day is close to zero. Therefore,
it does not give any useful insights.
- The method retrieves historical data and calculates the TR for each asset in the Toolkit instance.
- The risk-free rate is the Toolkit's risk_free_rate, the 10-year US Treasury yield by default. Many
textbook definitions (Sharpe, 1994; the Ken French factors) use a short-term Treasury bill instead, which
the Toolkit uses when initialised with risk_free_rate="13w".
- If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["UNP", "UPS", "FDX"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2020-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_treynor_ratio()
```

Which returns:

| Date   |     UNP |     UPS |     FDX |
|:-------|--------:|--------:|--------:|
| 2021   |  0.2344 |  0.3677 | -0.0077 |
| 2022   | -0.2789 | -0.2134 | -0.3426 |
| 2023   |  0.2003 | -0.0898 |  0.4279 |
| 2024   | -0.163  | -0.3386 |  0.1571 |
| 2025   | -0.0065 | -0.2648 |  0.008  |

---

## get_sharpe_ratio
Calculate the Sharpe ratio, a measure of risk-adjusted return that evaluates the excess return of an investment portfolio or asset per unit of risk taken.

The Sharpe ratio is calculated as the difference between the expected return of the asset or portfolio and the risk-free rate of return, divided by the standard deviation of the asset or portfolio's excess return. It quantifies the amount of return generated for each unit of risk assumed, providing insights into the investment's performance relative to the risk taken.

The formula is as follows:

$$
\text{Sharpe Ratio} = \text{Excess Return} / \text{Excess Standard Deviation}
$$

By default one Sharpe ratio is reported per `period`, computed from the **daily** excess returns falling inside that period. For a given period, for example monthly, this translates into the following:

$$
\text{Sharpe Ratio} = \text{Average Daily Excess Return within the Month} / \text{Standard Deviation of the Daily Excess Returns within the Month}
$$

For a rolling period, `period` instead sets the frequency of the returns themselves and the ratio is computed over a rolling window of `rolling` such returns:

$$
\text{Sharpe Ratio} = \text{Average Rolling Excess Return} / \text{Standard Deviation of Rolling Excess Returns}
$$

Note that the Risk Free Rate is already subtracted from these returns. The Toolkit's risk free rate is the 10-year US Treasury yield by default, while Sharpe (1994) and the Ken French factor files use a short-term Treasury bill. Initialise the Toolkit with risk_free_rate="13w" (the 13-week Treasury bill; "5y", "10y" and "30y" are the other options) to use a short rate instead.

By default the result is **not annualized**: it is a per-observation Sharpe ratio, so a value computed from daily returns is roughly SQRT(252) smaller than the annualized figure usually quoted in the literature (SQRT(52), SQRT(12) and SQRT(4) for weekly, monthly and quarterly returns respectively). Set annualize=True to multiply by that factor, to compare against published annualized Sharpe ratios.

The plain Sharpe ratio only looks at the mean and standard deviation of returns, implicitly assuming Gaussian, i.i.d. returns and ignoring how much uncertainty surrounds the estimate itself. The `method` parameter selects one of four corrections for that, each keeping the same excess returns and therefore the same underlying Sharpe ratio as its starting point:

- `"lo"` - the annualized Sharpe ratio of Lo (2002), which corrects the annualization for serially correlated returns. SQRT(q) * SR assumes independent returns; with autocorrelated returns (smoothed prices of illiquid assets, hedge funds, momentum or mean reversion) the variance of a yearly return is no longer q times the variance of one return, and the yearly Sharpe ratio becomes:

$$
\operatorname{SR}(q) = \operatorname{η}(q) \cdot \text{SR},\;\; \operatorname{η}(q) = q / \sqrt{q + 2 \cdot \text{Σ\_\{k} = \text{1\}} ^{\text{\{q-1\}}} (q - k) \cdot \rho_{k}}
$$

where q is the number of observations in a year and ρ_k the sample autocorrelation of the excess returns at lag k. Positive autocorrelation lowers the annualized ratio below SQRT(q) * SR, negative autocorrelation raises it. Sample autocorrelations at lags close to the sample size rest on a handful of pairs, so the sum runs over `lags` lags and takes the autocorrelations beyond them as 0. Each ρ_k is corrected for its small-sample bias −(n − k) / (n · (n − 1)) (Moran, 1948), which the (q − k) weights would otherwise turn into an overstated ratio on short samples, and fewer than 30 observations give NaN: a week or a month of daily returns, or a rolling window below 30, so use quarterly or yearly periods or a longer window. The result is always annualized.

- `"adjusted"` - the Adjusted Sharpe Ratio (ASR, Pezier & White, 2006) penalizes (or rewards) the Sharpe ratio for negative skewness and excess kurtosis using a Cornish-Fisher-style expansion, so that two strategies with the same Sharpe ratio but different tail shapes are no longer scored identically:

$$
\text{ASR} = \text{SR} \cdot \left[1 + (S / 6) \cdot \text{SR} - ((K - 3) / 24) \cdot \text{SR} ^{2}\right]
$$

- `"probabilistic"` - the Probabilistic Sharpe Ratio (PSR) is the probability that the true (population) Sharpe ratio exceeds `benchmark_sharpe_ratio`, folding the skewness and (non-excess) kurtosis of the underlying returns into the standard error of the Sharpe ratio so that a short, lumpy sample no longer looks more convincing than it is:

$$
\operatorname{PSR}(\text{SR} \cdot) = \Phi((\text{SR̂} - \text{SR} \cdot) \cdot \sqrt{n - 1} / \sqrt{1 - \text{γ₃} \cdot \text{SR̂} + ((\text{γ₄} - 1) / 4) \cdot \text{SR̂} ^{2}})
$$

- `"deflated"` - the Deflated Sharpe Ratio (DSR) is the Probabilistic Sharpe Ratio corrected for the fact that a reported Sharpe ratio is often the best of many strategy variations, parameter combinations, or lookback windows tried during a backtest (multiple testing / selection bias / "backtest overfitting"). It estimates the Sharpe ratio one would expect to observe purely by chance as the maximum of `n_trials` independent trials under the null hypothesis of no skill, and uses that expected maximum as the benchmark SR* in the Probabilistic Sharpe Ratio formula instead of a naive benchmark such as 0:

$$
\text{SR} \cdot = \sqrt{\text{Var} \left[\text{SR\_trials}\right]} \cdot \left[(1 - \text{γ}) \cdot \operatorname{Phi⁻¹}(1 - 1 / N) + \text{γ} \cdot \operatorname{Phi⁻¹}(1 - 1 / (N \cdot e))\right]
$$

Where SR̂ is the observed Sharpe ratio, S (γ₃) is the skewness and K (γ₄) the non-excess (raw) kurtosis of the same returns, n is the number of return observations, N is `n_trials`, Var[SR_trials] is the variance of the Sharpe ratios observed across those N trials, γ ≈ 0.5772 is the Euler-Mascheroni constant and Φ is the standard normal CDF. Since DSR = PSR(SR*), it is always less than or equal to the Probabilistic Sharpe Ratio computed against a benchmark of 0.

This codebase does not track "N literal strategy trials" - there is no record of how many parameter combinations were tried before arriving at the current Toolkit configuration. As a documented approximation, `Var[SR_trials]` is estimated from the variance of an auxiliary *rolling* Sharpe ratio series (see `get_rolling_sharpe_ratio`) computed over a `trials_window`-sized window across the full return history, and `n_trials` defaults to the number of valid (non-NaN) values in that same rolling series. That series is built from the same returns as the Sharpe ratio being deflated, so both are on the same scale: the daily excess returns (the observations within each period) for the Sharpe ratio per period, and the excess returns of `period` itself for a rolling Sharpe ratio. This treats each rolling window as if it were one "trial" - a reasonable proxy for how dispersed the Sharpe ratio could plausibly have been under different choices, but not a substitute for passing the actual number of variations tried (via `n_trials`) when that is known, since the quality of the correction depends directly on it.

**See definition:** [https://en.wikipedia.org/wiki/Sharpe_ratio](https://en.wikipedia.org/wiki/Sharpe_ratio){:target="_blank"}

**Also known as:** risk-adjusted return, reward-to-variability ratio. The variants are also known as the Pezier and White Adjusted Sharpe Ratio (ASR), the Sharpe ratio significance probability (PSR) and the backtest overfitting or selection-bias-adjusted Sharpe ratio (DSR).

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>rolling (int, optional):</u> The rolling period to use for the calculation. If you select
period = 'monthly' and set rolling to 12 you obtain the rolling 12-month Sharpe Ratio.
- <u>method (str, optional):</u> Which Sharpe ratio to calculate, one of "standard", "lo",
"adjusted", "probabilistic" or "deflated", as described above. Defaults to "standard".
- <u>benchmark_sharpe_ratio (float, optional):</u> The hypothesized or benchmark Sharpe ratio
(SR*) to test the observed Sharpe ratio against. Only used when method="probabilistic".
Defaults to 0.0, i.e. testing whether the strategy has any skill at all above doing nothing.
- <u>trials_window (int, optional):</u> The window size of the auxiliary rolling Sharpe ratio
series that approximates `Var[SR_trials]` and the default `n_trials`, see above. Only
used when method="deflated". It counts observations of the returns the Sharpe ratio is
computed from: daily (or intraday) observations for the Sharpe ratio per period, and
observations of `period` when `rolling` is set. Defaults to None, which uses the median
number of observations per period (so each trial spans about one period) for the Sharpe
ratio per period, and half of the available return history for a rolling Sharpe ratio
so that enough overlapping windows exist regardless of `period` or date range.
- <u>n_trials (int, optional):</u> The number of independent (or effectively independent)
strategy variations, parameter combinations, or lookback windows tried before
arriving at the reported Sharpe ratio. Only used when method="deflated". Defaults to
None, which falls back to the number of valid values in the auxiliary rolling Sharpe
ratio series described above. Pass this explicitly whenever the actual number of trials
is known.
- <u>lags (int, optional):</u> The number of autocorrelation lags in Lo's η(q). Only used when
method="lo". Defaults to None, which uses the Newey and West (1994) rule
floor(4 * (n / 100)^(2/9)) on the n observations (4 for a year of daily returns),
capped at q − 1.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>annualize (bool, optional):</u> Whether to annualize the Sharpe ratio, multiplying it by
the square root of the number of observations in a year: 252 for the daily
returns within each period, 252 times the median number of bars per day for the
intraday returns within a day (period="daily" with an intraday_period), or the
periods in a year for a rolling Sharpe ratio (e.g. 12 for monthly). Only for method="standard" and "adjusted", since the
probabilistic and deflated methods return probabilities; method="lo" is annualized
either way. Defaults to False.

**Returns:**

pd.DataFrame: Sharpe ratio values. For method="probabilistic" and method="deflated"
these are probabilities between 0 and 1 rather than ratios.

**Notes:**

- period="daily" needs intraday - <u>data (initialise the Toolkit with an intraday_period):</u> the ratio per day
is then computed from the intraday bars within each day, with the daily risk free rate spread over the
bars of a day. Without intraday data a single day holds one return, so the result is empty and logs why.
- The method retrieves historical data and calculates the Sharpe ratio for each asset in the Toolkit instance.
- The risk-free rate is the Toolkit's risk_free_rate, the 10-year US Treasury yield by default; choose
risk_free_rate="13w" when initialising the Toolkit for the short-term rate Sharpe (1994) uses.
- The "adjusted", "probabilistic" and "deflated" variants use the **non-excess (raw)** kurtosis
convention, i.e. a Normal distribution has a kurtosis of 3, not 0. Internally this calls
`risk_model.get_kurtosis(..., fisher=False)`.
- If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.
- `get_sharpe_ratio(method="probabilistic")` returns the probability that each Sharpe ratio is genuine,
i.e. above `benchmark_sharpe_ratio` once the sample length, skewness and kurtosis are accounted for.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["SPY", "TLT", "GLD", "BTCUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
    benchmark_ticker=None,
)

toolkit.performance.get_sharpe_ratio(annualize=True)
```

Which returns:

| Date   |     SPY |     TLT |     GLD |   BTCUSD |
|:-------|--------:|--------:|--------:|---------:|
| 2021   |  1.9355 | -0.2283 | -0.6241 |   0.6316 |
| 2022   | -0.608  | -0.9215 |  0.4971 |  -1.1891 |
| 2023   |  1.1567 |  0.7714 |  0.8362 |   1.6139 |
| 2024   |  1.5203 | -0.6917 |  1.4238 |   1.3959 |
| 2025   |  0.3606 |  0.2664 |  1.7105 |  -0.1906 |

---

## get_sortino_ratio
The Sortino Ratio is a financial metric used to assess the risk-adjusted performance of an investment portfolio or asset by considering only the downside risk. It measures the excess return generated by the portfolio per unit of downside risk, specifically, the standard deviation of negative returns. The Sortino Ratio is particularly useful for investors who are primarily concerned with minimizing the downside risk of their investments.

The formula is as follows:

$$
\text{Sortino Ratio} = \text{Excess Return} / \text{Downside Deviation}
$$

$$
\text{Downside Deviation} = \sqrt{(1 / N) \cdot \operatorname{SUM}(\min(\text{Excess Return},\; 0) ^{2})}
$$

Where N is the *total* number of observations, not just the negative ones, following Sortino & Price (1994). By default one Sortino ratio is reported per `period`, computed from the **daily** excess returns falling inside that period. For a given period, for example monthly, this translates into the following:

$$
\text{Sortino Ratio} = \text{Average Daily Excess Return within the Month} / \text{Downside Deviation of the Daily Excess Returns within the Month}
$$

For a rolling period, `period` instead sets the frequency of the returns themselves and the ratio is computed over a rolling window of `rolling` such returns:

$$
\text{Sortino Ratio} = \text{Average Rolling Excess Return} / \text{Rolling Downside Deviation}
$$

Note that the Risk Free Rate is already subtracted from these returns. It is the Toolkit's risk_free_rate, the 10-year US Treasury yield by default; initialise the Toolkit with risk_free_rate="13w" for a short-term Treasury bill rate instead.

A period needs at least two observations for a Sortino ratio, with a single one the ratio would only show its sign, so such periods are left out.

As with the Sharpe Ratio, the result is **not annualized**: it is a per-observation ratio, so multiply by SQRT(252), SQRT(52), SQRT(12) or SQRT(4) for daily, weekly, monthly or quarterly returns respectively before comparing against published annualized figures.

**See definition:** [https://en.wikipedia.org/wiki/Sortino_ratio](https://en.wikipedia.org/wiki/Sortino_ratio){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set,
the Sortino ratio is calculated over a rolling window of this many periods across the
full return history instead of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Sortino ratio values.

**Notes:**

- period="daily" needs intraday - <u>data (initialise the Toolkit with an intraday_period):</u> the ratio per day
is then computed from the intraday bars within each day, with the daily risk free rate spread over the
bars of a day. Without intraday data a single day holds one return, so the result is empty and logs why.
- The method retrieves historical data and calculates the Sortino ratio for each asset in the Toolkit instance.
- The risk-free rate is the Toolkit's risk_free_rate, the 10-year US Treasury yield by default. Many
textbook definitions (Sharpe, 1994; the Ken French factors) use a short-term Treasury bill instead, which
the Toolkit uses when initialised with risk_free_rate="13w".
- If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["V", "MA", "AXP"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_sortino_ratio()
```

Which returns:

| Date   |       V |      MA |     AXP |
|:-------|--------:|--------:|--------:|
| 2021   |  0.0058 |  0.0163 |  0.1221 |
| 2022   | -0.0049 | -0.001  | -0.0138 |
| 2023   |  0.129  |  0.1007 |  0.0922 |
| 2024   |  0.0911 |  0.1065 |  0.1909 |
| 2025   |  0.038  |  0.0273 |  0.0726 |

---

## get_ulcer_performance_index
Calculate the Ulcer Performance Index (UPI), alternatively called Martin ratio, a measure of risk-adjusted return that evaluates the excess return of an investment portfolio or asset per unit of risk taken.

The formula is as follows:

$$
\text{Ulcer Performance Index} = (\text{Period Return} - \text{Risk-Free Rate}) / \text{Ulcer Index}
$$

$$
\text{Ulcer Index} = \sqrt{\operatorname{MEAN}(\text{Drawdown} ^{2})},\;\; \text{with each day's drawdown measured from the highest value of the trailing rolling days within the period}
$$

It measures the excess return earned per unit of drawdown pain: the depth and the duration of the declines both weigh in, where the Sharpe Ratio treats upward and downward swings alike. Similar to the Sharpe Ratio, a higher UPI is better than a lower one (since investors prefer more return for less risk).

**Also known as:** UPI, Martin ratio.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>rolling (int):</u> The rolling period to use to calculate the Ulcer Index. Defaults to 14.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Ulcer Performance Index values.

**Notes:**

- The method retrieves historical data and calculates the UPI for each asset in the Toolkit instance.
- The risk-free rate is the Toolkit's risk_free_rate, the 10-year US Treasury yield by default. Many
textbook definitions (Sharpe, 1994; the Ken French factors) use a short-term Treasury bill instead, which
the Toolkit uses when initialised with risk_free_rate="13w".
- If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["VZ", "T", "TMUS"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2020-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_ulcer_performance_index()
```

Which returns:

| Date   |      VZ |       T |    TMUS |
|:-------|--------:|--------:|--------:|
| 2021   | -3.7069 | -2.0886 | -3.7462 |
| 2022   | -4.3869 |  0.7109 |  4.3646 |
| 2023   | -0.3236 | -1.4171 |  3.5546 |
| 2024   |  2.6617 | 15.933  | 13.5977 |
| 2025   |  1.4725 |  2.6824 | -2.3337 |

---

## get_calmar_ratio
Calculate the Calmar Ratio of an investment portfolio or asset's returns.

The Calmar Ratio is a risk-adjusted return metric that divides the return of an investment portfolio or asset over each period (a calendar-year return for period='yearly', a quarterly return for period='quarterly') by its Maximum Drawdown, providing insight into the return achieved per unit of the worst historical loss of value.

The formula is as follows:

$$
\text{Calmar Ratio} = \text{Return} / | \text{Maximum Drawdown} |
$$

**See definition:** [https://en.wikipedia.org/wiki/Calmar_ratio](https://en.wikipedia.org/wiki/Calmar_ratio){:target="_blank"}

**Also known as:** Drawdown ratio.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>within_period (bool, optional):</u> Whether to calculate the Maximum Drawdown within the
specified period or for the entire period. Thus whether to look at the Maximum Drawdown
within a specific year (if period = 'yearly') or look at the entirety of all years.
Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Calmar Ratio values.

**Notes:**

- The method retrieves historical data and calculates the Calmar Ratio for each asset in
the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the ratio values using
the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["VTI", "VEA", "VWO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2020-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_calmar_ratio()
```

Which returns:

| Date   |     VTI |     VEA |     VWO |
|:-------|--------:|--------:|--------:|
| 2021   |  4.9482 |  1.643  |  0.0948 |
| 2022   | -0.7709 | -0.5338 | -0.6106 |
| 2023   |  2.4416 |  1.483  |  0.7946 |
| 2024   |  2.7771 |  0.3321 |  1.1734 |
| 2025   |  0.8851 |  2.6195 |  1.7646 |

---

## get_sterling_ratio
Calculate the Sterling Ratio of an investment portfolio or asset's returns.

The Sterling Ratio is a risk-adjusted return metric that divides the return of an investment portfolio or asset over each period (a calendar-year return for period='yearly', a quarterly return for period='quarterly') by its Average Drawdown plus a fixed adjustment (conventionally 10%), providing insight into the return achieved relative to the typical depth of its drawdowns rather than only the single worst one (as with the Calmar Ratio).

The formula is as follows:

$$
\text{Sterling Ratio} = \text{Return} / (| \text{Average Drawdown} | + \text{Adjustment})
$$

Where the Average Drawdown is the mean drawdown from the running peak over all observations on which the asset is below that peak (by default every such day within the period), not the average of the largest drawdowns.

**Also known as:** Sterling-Calmar ratio.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>within_period (bool, optional):</u> Whether to calculate the Average Drawdown within the
specified period or for the entire period. Thus whether to look at the Average Drawdown
within a specific year (if period = 'yearly') or look at the entirety of all years.
Defaults to True.
- <u>adjustment (float, optional):</u> The fixed adjustment added to the Average Drawdown,
conventionally 0.1 (10%). Defaults to 0.1.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Sterling Ratio values.

**Notes:**

- The method retrieves historical data and calculates the Sterling Ratio for each asset in
the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the ratio values using
the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NEE", "DUK", "SO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2020-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_sterling_ratio()
```

Which returns:

| Date   |     NEE |     DUK |     SO |
|:-------|--------:|--------:|-------:|
| 2021   |  1.2842 |  1.4182 | 1.2009 |
| 2022   | -0.3726 |  0.1186 | 0.4819 |
| 2023   | -0.8979 | -0.0838 | 0.1342 |
| 2024   |  1.307  |  1.1541 | 1.5685 |
| 2025   |  0.9868 |  0.9407 | 0.6777 |

---

## get_burke_ratio
Calculate the Burke Ratio of an investment portfolio or asset's returns.

The Burke Ratio is a risk-adjusted return metric that divides the excess return (return minus the risk-free rate) of an investment portfolio or asset by the square root of the sum of its squared drawdowns, penalizing both the frequency and depth of drawdowns more heavily than the Calmar or Sterling Ratios.

The formula is as follows:

$$
\text{Burke Ratio} = (\text{Return} - \text{Risk-Free Rate}) / \sqrt{\operatorname{SUM}(\text{Drawdown}_{d} ^{2})}
$$

Where Drawdown_d is the drawdown from the running peak at every observation d on which the asset is below that peak, which by default is every such day within the period. This weighs the time spent under water as well as the depth, so the ratio differs from the version that sums one drawdown per episode.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>within_period (bool, optional):</u> Whether to calculate the drawdowns within the specified
period or for the entire period. Thus whether to look at the drawdowns within a specific
year (if period = 'yearly') or look at the entirety of all years. Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Burke Ratio values.

**Notes:**

- The method retrieves historical data and calculates the Burke Ratio for each asset in
the Toolkit instance.
- The risk-free rate is the Toolkit's risk_free_rate, the 10-year US Treasury yield by default. Many
textbook definitions (Sharpe, 1994; the Ken French factors) use a short-term Treasury bill instead, which
the Toolkit uses when initialised with risk_free_rate="13w".
- If `growth` is set to True, the method calculates the growth of the ratio values using
the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["BA", "LMT", "RTX"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2020-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_burke_ratio()
```

Which returns:

| Date   |      BA |     LMT |     RTX |
|:-------|--------:|--------:|--------:|
| 2021   | -0.0305 |  0.014  |  0.3334 |
| 2022   | -0.0181 |  0.3247 |  0.109  |
| 2023   |  0.2136 | -0.0588 | -0.0744 |
| 2024   | -0.0697 |  0.0508 |  0.6619 |
| 2025   |  0.1203 | -0.0134 |  1.0527 |

---

## get_m2_ratio
The M2 Ratio, also known as the Modigliani-Modigliani Measure, is a financial metric used to evaluate the risk-adjusted performance of an investment portfolio or strategy. It assesses the excess return generated by the portfolio relative to a risk-free investment, taking into account the portfolio's volatility or risk. The M2 Ratio helps investors and portfolio managers determine whether the portfolio is delivering returns that justify its level of risk.

The formula is as follows:

$$
M_{2} \;\text{Ratio} = \text{Risk-Free Rate} + \left[(\text{Portfolio's Return} - \text{Risk-Free Rate}) / \text{Portfolio Standard Deviation}\right] \cdot \text{Benchmark Standard Deviation}
$$

This rescales the (dimensionless) Sharpe ratio back into return-space by asking what return the portfolio would have earned had it been leveraged or de-leveraged, via risk-free borrowing or lending, to match the benchmark's volatility exactly -- producing a number directly comparable to the benchmark's actual return. Requires a `benchmark_ticker` to be set on the Toolkit instance, since the benchmark's standard deviation is part of the formula.

**See definition:** [https://en.wikipedia.org/wiki/Modigliani_risk-adjusted_performance](https://en.wikipedia.org/wiki/Modigliani_risk-adjusted_performance){:target="_blank"}

**Also known as:** Modigliani-Modigliani measure, M2, risk-adjusted performance.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set,
the M2 ratio is calculated over a rolling window of this many periods across the full
return history instead of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: M2 ratio values.

**Notes:**

- Daily M2 is not an option as the standard deviation for 1 day is close to zero. Therefore, it does
not give any useful insights.
- The method retrieves historical data and calculates the M2 for each asset in the Toolkit instance.
- The risk-free rate is the Toolkit's risk_free_rate, the 10-year US Treasury yield by default. Many
textbook definitions (Sharpe, 1994; the Ken French factors) use a short-term Treasury bill instead, which
the Toolkit uses when initialised with risk_free_rate="13w".
- If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["HD", "LOW"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2020-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_m2_ratio()
```

Which returns:

| Date   |      HD |     LOW |
|:-------|--------:|--------:|
| 2021   |  0.39   |  0.3481 |
| 2022   | -0.1634 | -0.1482 |
| 2023   |  0.0932 |  0.0955 |
| 2024   |  0.1083 |  0.0921 |
| 2025   | -0.0718 |  0.0055 |

---

## get_tracking_error
Tracking Error is a financial metric that quantifies the volatility or dispersion of the difference between the returns of an investment portfolio or asset and the returns of a benchmark index. It measures how closely the portfolio tracks its benchmark and provides insights into the consistency of the portfolio's performance relative to the benchmark. A higher Tracking Error indicates greater divergence from the benchmark, while a lower Tracking Error suggests that the portfolio closely follows the benchmark.

The formula is as follows:

$$
\text{Tracking Error} (\text{TE}) = \text{Standard Deviation of} (\text{Portfolio Returns} - \text{Benchmark Returns})
$$

By default one Tracking Error is reported per `period`, computed from the daily returns within that period, so it is a daily figure: multiply by SQRT(252) to compare it with the annualized tracking error funds report. With `rolling`, the returns of `period` itself are used instead.

**See definition:** [https://en.wikipedia.org/wiki/Tracking_error](https://en.wikipedia.org/wiki/Tracking_error){:target="_blank"}

**Also known as:** active risk, benchmark deviation.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set,
Tracking Error is calculated over a rolling window of this many periods across the
full return history instead of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Tracking error values.

**Notes:**

- Daily Tracking Error is not an option as the standard deviation for 1 day is close to zero. Therefore, it does
not give any useful insights.
- The method retrieves historical data and calculates the TE for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["VOO", "RSP", "QQQ"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_tracking_error()
```

Which returns:

| Date   |    VOO |    RSP |    QQQ |
|:-------|-------:|-------:|-------:|
| 2021   | 0.0002 | 0.0038 | 0.0059 |
| 2022   | 0.0003 | 0.0034 | 0.0067 |
| 2023   | 0.0002 | 0.0038 | 0.005  |
| 2024   | 0.0003 | 0.0046 | 0.0047 |
| 2025   | 0.001  | 0.0051 | 0.0041 |

---

## get_information_ratio
The Information Ratio (IR) is a financial metric that assesses the risk-adjusted performance of a portfolio or investment strategy relative to a benchmark index. It quantifies how much active return (the return above the benchmark) the portfolio generates per unit of tracking error, the volatility of that active return. The Information Ratio is commonly used by portfolio managers, financial analysts, and investors to evaluate the skill of a portfolio manager in generating returns beyond what would be expected based on the risk taken.

- IR > 0: A positive Information Ratio indicates that the portfolio has generated excess returns compared to the benchmark, suggesting that the portfolio manager has added value.
- IR = 0: An Information Ratio of zero implies that the portfolio's excess return is in line with the benchmark, meaning the portfolio manager has not added or lost value relative to the benchmark.
- IR < 0: A negative Information Ratio suggests that the portfolio has underperformed the benchmark, potentially indicating that the portfolio manager has detracted value.

The formula is as follows:

$$
\text{Information Ratio} (\text{IR}) = \operatorname{Mean}(\text{Portfolio Return} - \text{Benchmark Return}) / \text{Tracking Error}
$$

By default it is computed from the daily returns within each period and is not annualized: multiply by SQRT(252) to compare it with the annualized figures in the literature, where an IR of 0.5 is considered good. With `rolling`, the returns of `period` itself are used instead.

**See definition:** [https://en.wikipedia.org/wiki/Information_ratio](https://en.wikipedia.org/wiki/Information_ratio){:target="_blank"}

**Also known as:** active return per risk.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set,
the Information Ratio is calculated over a rolling window of this many periods across
the full return history instead of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Information ratio values.

**Notes:**

- Daily Information Ratio is not an option as the standard deviation for 1 day is close to zero.
Therefore, it does not give any useful insights.
- The method retrieves historical data and calculates the IR for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["XLK", "XLE", "XLV"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_information_ratio()
```

Which returns:

| Date   |     XLK |     XLE |     XLV |
|:-------|--------:|--------:|--------:|
| 2021   |  0.0377 |  0.047  | -0.0204 |
| 2022   | -0.0557 |  0.1406 |  0.0776 |
| 2023   |  0.147  | -0.0655 | -0.1316 |
| 2024   | -0.0053 | -0.0549 | -0.1084 |
| 2025   |  0.042  | -0.0246 | -0.0114 |

---

## get_upside_capture_ratio
Calculate the Upside Capture Ratio of an investment portfolio or asset's returns.

The Upside Capture Ratio measures how well an investment portfolio or asset performs relative to a benchmark during periods in which the benchmark's return is positive. A ratio above 1 (or 100%) indicates the asset captured more of the benchmark's gains than the benchmark itself.

The formula is as follows:

$$
\text{Upside Capture Ratio} = \text{Geometric Average Return in Up Periods} / \text{Geometric Average Benchmark Return in Up Periods}
$$

$$
\text{Geometric Average Return} = (\operatorname{PRODUCT}(1 + \text{Return})) ^{1 / n} - 1
$$

Where the up periods are the observations (days within each period) with a positive benchmark return and n is their number, following Morningstar's definition. Geometric rather than arithmetic averages make the ratio reflect the compounded return captured, so it does not depend on how volatile the returns within the up periods were.

Upside and downside capture (see `get_downside_capture_ratio`) are read together: an upside capture above the downside capture means the asset kept more of the benchmark's gains than of its losses, which is what defensive and low-volatility strategies aim for even with both ratios below 1. Both are computed from the daily returns within each period, while fund factsheets usually use monthly returns over three to five years, so the figures are not directly comparable with published ones.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Upside Capture Ratio values.

**Notes:**

- The method retrieves historical data and calculates the Upside Capture Ratio for each
asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the ratio values using
the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["QQQ", "SCHD", "USMV"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_upside_capture_ratio()
```

Which returns:

| Date   |    QQQ |   SCHD |   USMV |
|:-------|-------:|-------:|-------:|
| 2021   | 1.1827 | 0.832  | 0.6961 |
| 2022   | 1.2845 | 0.7129 | 0.7051 |
| 2023   | 1.3244 | 0.765  | 0.6077 |
| 2024   | 1.3372 | 0.5237 | 0.5323 |
| 2025   | 1.2056 | 0.5019 | 0.4674 |

---

## get_downside_capture_ratio
Calculate the Downside Capture Ratio of an investment portfolio or asset's returns.

The Downside Capture Ratio measures how well an investment portfolio or asset performs relative to a benchmark during periods in which the benchmark's return is negative. A ratio below 1 (or 100%) indicates the asset lost less than the benchmark during those periods.

The formula is as follows:

$$
\text{Downside Capture Ratio} = \text{Geometric Average Return in Down Periods} / \text{Geometric Average Benchmark Return in Down Periods}
$$

$$
\text{Geometric Average Return} = (\operatorname{PRODUCT}(1 + \text{Return})) ^{1 / n} - 1
$$

Where the down periods are the observations (days within each period) with a negative benchmark return and n is their number, following Morningstar's definition. As with the Upside Capture Ratio, both ratios are computed from the daily returns within each period, while fund factsheets usually use monthly returns over three to five years.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Downside Capture Ratio values.

**Notes:**

- The method retrieves historical data and calculates the Downside Capture Ratio for each
asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the ratio values using
the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["XLU", "SPLV", "ARKK"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_downside_capture_ratio()
```

Which returns:

| Date   |    XLU |   SPLV |   ARKK |
|:-------|-------:|-------:|-------:|
| 2021   | 0.3911 | 0.5358 | 2.0537 |
| 2022   | 0.4698 | 0.4991 | 2.5005 |
| 2023   | 0.7024 | 0.6177 | 2.3265 |
| 2024   | 0.2051 | 0.3127 | 2.5483 |
| 2025   | 0.3459 | 0.3223 | 2.0919 |

---

## get_win_rate
Calculate the Win Rate of an investment portfolio or asset's returns.

The Win Rate is the share of days within each period in which the asset's return exceeds the benchmark's return.

The formula is as follows:

$$
\text{Win Rate} = \text{Number of Days with Asset Return} > \text{Benchmark Return} / \text{Number of Days with both an Asset and}\; a \;\text{Benchmark Return},\;\; \text{using the daily returns within each period (e.g. each year)},\;\; \text{as}\; a \;\text{decimal} (0.55 = 55\%)
$$

Days on which the asset or the benchmark has no return are left out of both counts rather than counted as losses.

**Also known as:** batting average.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Win Rate values.

**Notes:**

- The method retrieves historical data and calculates the Win Rate for each asset in the
Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the ratio values using
the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "GOOGL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_win_rate()
```

Which returns:

| Date   |   AAPL |   MSFT |   GOOGL |
|:-------|-------:|-------:|--------:|
| 2021   | 0.494  | 0.5139 |  0.5299 |
| 2022   | 0.4781 | 0.4582 |  0.4502 |
| 2023   | 0.576  | 0.512  |  0.524  |
| 2024   | 0.5    | 0.4881 |  0.5317 |
| 2025   | 0.472  | 0.484  |  0.564  |

---

## get_kappa_ratio
Calculate the Kappa Ratio of an investment portfolio or asset's returns.

The Kappa Ratio is a generalization of the Sortino Ratio that penalizes downside risk using a higher-order lower partial moment. The Sortino Ratio is the special case of the Kappa Ratio with order=2.

Note that this already subtracts the Risk Free Rate.

The formula is as follows:

$$
\text{Daily Excess Return} = \text{Daily Return} - \text{Daily Risk Free Rate},\;\; \text{with Daily Risk Free Rate} = (1 + \text{Annual Risk Free Rate}) ^{1 / 252} - 1
$$

$$
\text{Lower Partial Moment} (\text{LPM}) = \operatorname{MEAN}(\max(- \text{Daily Excess Return},\; 0) ^{\text{Order}}),\;\; \text{averaged over all days in the period (days with a non-negative excess return count as 0)}
$$

$$
\text{Kappa Ratio} = \operatorname{MEAN}(\text{Daily Excess Return}) / \text{LPM} ^{1 / \text{Order}},\;\; \text{per period and not annualized},\;\; \text{with Order defaulting to 3}
$$

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>order (int, optional):</u> The order of the lower partial moment used in the denominator.
Defaults to 3.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Kappa Ratio values.

**Notes:**

- Daily Kappa Ratio is not an option as the standard deviation for 1 day is close to zero.
Therefore, it does not give any useful insights.
- The method retrieves historical data and calculates the Kappa Ratio for each asset in
the Toolkit instance.
- The risk-free rate is the Toolkit's risk_free_rate, the 10-year US Treasury yield by default. Many
textbook definitions (Sharpe, 1994; the Ken French factors) use a short-term Treasury bill instead, which
the Toolkit uses when initialised with risk_free_rate="13w".
- If `growth` is set to True, the method calculates the growth of the ratio values using
the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["LLY", "MRK", "ABBV"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_kappa_ratio()
```

Which returns:

| Date   |    LLY |     MRK |    ABBV |
|:-------|-------:|--------:|--------:|
| 2021   | 0.1248 |  0.0091 |  0.0811 |
| 2022   | 0.0844 |  0.1426 |  0.0552 |
| 2023   | 0.1351 | -0.004  | -0.0059 |
| 2024   | 0.0652 | -0.0191 |  0.0298 |
| 2025   | 0.0513 |  0.0193 |  0.064  |

---

## get_omega_ratio
Calculate the Omega Ratio of an investment portfolio or asset's returns.

The Omega Ratio is a risk-return measure that divides the sum of gains above a minimum acceptable return (MAR) by the sum of losses below it, capturing the full shape of the return distribution rather than only its first two moments (unlike the Sharpe Ratio).

The formula is as follows:

$$
\text{Omega Ratio} = \operatorname{SUM}(\text{Gains above MAR}) / \operatorname{SUM}(\text{Losses below MAR})
$$

**See definition:** [https://en.wikipedia.org/wiki/Omega_ratio](https://en.wikipedia.org/wiki/Omega_ratio){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>within_period (bool, optional):</u> Whether to calculate the Omega Ratio within the specified
period or for the entire period. Thus whether to look at the Omega Ratio within a specific
year (if period = 'yearly') or look at the entirety of all years. Defaults to True.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the
Omega Ratio is calculated over a rolling window of this many periods across the full
return history instead of per `period`. Defaults to None.
- <u>minimum_acceptable_return (float, optional):</u> The minimum acceptable return (MAR) used as
the threshold between gains and losses. Defaults to 0.0.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Omega Ratio values.

**Notes:**

- The method retrieves historical data and calculates the Omega Ratio for each asset in
the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the ratio values using
the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["BLK", "SCHW", "BX"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_omega_ratio()
```

Which returns:

|      |    BLK |   SCHW |     BX |
|:-----|-------:|-------:|-------:|
| 2021 | 1.2446 | 1.3257 | 1.5958 |
| 2022 | 0.9272 | 1.0318 | 0.8945 |
| 2023 | 1.1525 | 0.9625 | 1.3792 |
| 2024 | 1.2732 | 1.094  | 1.2109 |
| 2025 | 1.0728 | 1.2867 | 0.9944 |

---

## get_morningstar_risk_adjusted_return
Calculate the Morningstar Risk-Adjusted Return (MRAR), the measure Morningstar ranks funds on within their category for its star rating.

MRAR is the annualized certainty equivalent of the monthly geometric excess returns for an investor with risk aversion gamma: the return such an investor would accept with certainty instead of the uncertain returns. It equals the annualized geometric mean excess return when every month returns the same and falls further below it the more the returns vary, penalizing downside variation most. Morningstar uses a gamma of 2 and rates funds on 36, 60 and 120 months (three, five and ten years), which rolling=36, rolling=60 and rolling=120 give, weighting them 20%, 30% and 50% in the overall rating. For US dollar funds its risk-free rate is the three-month Treasury bill (auction average), which risk_free_rate="13w" follows. Morningstar also adjusts for tax-advantaged dividends where appropriate, which these total returns don't.

The formula is as follows:

$$
\text{Geometric Excess Return} = (1 + \text{Monthly Total Return}) / (1 + \text{Monthly Risk Free Rate}) - 1
$$

$$
\operatorname{MRAR}(\gamma) = \left[1 / T \cdot \operatorname{SUM}((1 + \text{Geometric Excess Return}\; t) ^{-\gamma})\right] ^{- 12 / \gamma} - 1
$$

with T the number of months. With a gamma of 0 it is the annualized geometric mean of the excess returns, Morningstar Return.

For more information, see the following:

- Morningstar (2023). "The Morningstar Rating for Funds." Morningstar Methodology, April 2023. [https://s25.q4cdn.com/634000362/files/doc_downloads/1/1157231.pdf](https://s25.q4cdn.com/634000362/files/doc_downloads/1/1157231.pdf){:target="_blank"}
- Morningstar (2009). "MRAR Illustrated." [https://www.morningstar.com/content/dam/marketing/apac/au/pdfs/Legal/MRARIllustrated_Factsheet.pdf](https://www.morningstar.com/content/dam/marketing/apac/au/pdfs/Legal/MRARIllustrated_Factsheet.pdf){:target="_blank"}

**Args:**

- <u>gamma (float, optional):</u> The risk aversion, 0 or higher. Defaults to 2.0, which
Morningstar uses for its ratings.
- <u>period (str, optional):</u> The period to group the monthly returns by, "yearly" or
"quarterly". Defaults to "yearly".
- <u>within_period (bool, optional):</u> Whether to calculate the MRAR of the months within
each period or of all months in the range. Defaults to True.
- <u>rolling (int, optional):</u> The number of months in a rolling window, e.g. 36 for the
three year MRAR at every month end. Overrides period and within_period.
Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the Toolkit (4 unless set
otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to
False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: The MRAR per period (rows) and ticker (columns) as decimals, or one
value per ticker over the whole range with within_period=False.

**Notes:**

- The returns are monthly total returns from the adjusted close, so dividends count.
Morningstar also deducts sales loads, which an exchange-traded fund does not have.
- Morningstar uses a three-month Treasury bill as the risk-free rate for US funds,
which `Toolkit(..., risk_free_rate="13w")` matches; the Toolkit's default is the
10-year Treasury yield, each converted to a monthly return.
- A month's risk-free return is the month's average yield, compounded to a month.
- A period is annualized from the months it has: the first month of the range has no
return (it has no earlier close), so the first year counts eleven months, which is
why 2021 in the example is above the funds' calendar-year return.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["VOO", "QQQ", "SCHD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
    risk_free_rate="13w",
)

toolkit.performance.get_morningstar_risk_adjusted_return()
```

Which returns:

| Date   |     VOO |     QQQ |    SCHD |
|:-------|--------:|--------:|--------:|
| 2021   |  0.3176 |  0.278  |  0.3201 |
| 2022   | -0.235  | -0.3837 | -0.0851 |
| 2023   |  0.1796 |  0.4298 | -0.023  |
| 2024   |  0.1793 |  0.1826 |  0.0485 |
| 2025   |  0.1198 |  0.135  | -0.01   |

---

## get_morningstar_risk
Calculate Morningstar Risk, the return a risk-averse investor would give up to remove the variation of the returns: Morningstar Return (the annualized geometric mean excess return) minus the Morningstar Risk-Adjusted Return. It is zero for returns that never vary and grows with their variation, most with variation on the downside. Morningstar rates funds Low to High on it within their category, over 36, 60 and 120 months (rolling=36, 60 and 120).

The formula is as follows:

$$
\text{Morningstar Risk} = \operatorname{MRAR}(0) - \operatorname{MRAR}(\gamma)
$$

with MRAR the Morningstar Risk-Adjusted Return (see get_morningstar_risk_adjusted_return) and MRAR(0) Morningstar Return.

For more information, see the following:

- Morningstar (2023). "The Morningstar Rating for Funds." Morningstar Methodology, April 2023. [https://s25.q4cdn.com/634000362/files/doc_downloads/1/1157231.pdf](https://s25.q4cdn.com/634000362/files/doc_downloads/1/1157231.pdf){:target="_blank"}

**Args:**

- <u>gamma (float, optional):</u> The risk aversion, 0 or higher. Defaults to 2.0, which
Morningstar uses for its ratings.
- <u>period (str, optional):</u> The period to group the monthly returns by, "yearly" or
"quarterly". Defaults to "yearly".
- <u>within_period (bool, optional):</u> Whether to calculate the risk of the months within
each period or of all months in the range. Defaults to True.
- <u>rolling (int, optional):</u> The number of months in a rolling window, e.g. 36 for the
three year figure at every month end. Overrides period and within_period.
Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the Toolkit (4 unless set
otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to
False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Morningstar Risk per period (rows) and ticker (columns) as decimals,
or one value per ticker over the whole range with within_period=False.

**Notes:**

- The returns and the risk-free rate are those of get_morningstar_risk_adjusted_return;
`Toolkit(..., risk_free_rate="13w")` matches Morningstar's three-month Treasury bill.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["VOO", "QQQ", "SCHD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
    risk_free_rate="13w",
)

toolkit.performance.get_morningstar_risk()
```

Which returns:

| Date   |    VOO |    QQQ |   SCHD |
|:-------|-------:|-------:|-------:|
| 2021   | 0.0148 | 0.0205 | 0.0214 |
| 2022   | 0.0375 | 0.0449 | 0.0339 |
| 2023   | 0.023  | 0.0445 | 0.0183 |
| 2024   | 0.0121 | 0.0145 | 0.016  |
| 2025   | 0.0125 | 0.0256 | 0.0126 |

---

## get_gain_to_pain_ratio
Calculate the Gain-to-Pain Ratio of an investment portfolio or asset's returns.

The Gain-to-Pain Ratio, popularized by Jack Schwager, divides the sum of all returns by the sum of the absolute value of all losses, summarizing the entire return history into a single measure of return earned per unit of pain endured.

The formula is as follows:

$$
\text{Gain-to-Pain Ratio} = \operatorname{SUM}(\text{Returns}) / \operatorname{SUM}(| \text{Losses} |)
$$

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>within_period (bool, optional):</u> Whether to calculate the Gain-to-Pain Ratio within the
specified period or for the entire period. Thus whether to look at the Gain-to-Pain Ratio
within a specific year (if period = 'yearly') or look at the entirety of all years.
Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Gain-to-Pain Ratio values.

**Notes:**

- The method retrieves historical data and calculates the Gain-to-Pain Ratio for each asset
in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the ratio values using
the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["GCUSD", "SIUSD", "HGUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_gain_to_pain_ratio()
```

Which returns:

|      |   GCUSD |   SIUSD |   HGUSD |
|:-----|--------:|--------:|--------:|
| 2021 | -0.0617 | -0.0653 |  0.1797 |
| 2022 |  0.0115 |  0.0413 | -0.0663 |
| 2023 |  0.1812 |  0.0233 |  0.0337 |
| 2024 |  0.3038 |  0.1403 |  0.0446 |
| 2025 |  0.5152 |  0.5701 |  0.2573 |

---

## get_kelly_criterion
Calculate the Kelly Criterion, the share of capital to put at risk that maximizes the expected logarithmic growth of wealth, from the returns of an investment portfolio or asset.

The discrete form is Kelly's (1956) bet: a probability of winning and a ratio of the average win to the average loss, as the QuantStats package calculates it from returns. The continuous form is Thorp's (2006) for returns that are close to normally distributed: the average excess return over the risk free rate divided by the variance of the excess returns. Since investors rarely bet the full Kelly amount, whose wealth swings widely, `fraction` gives a fractional Kelly such as half Kelly.

The formulas are as follows:

$$
\text{Discrete:}\;\; \text{Kelly} = \text{Win Rate} - (1 - \text{Win Rate}) / \text{Payoff Ratio}
$$

$$
\text{Continuous:}\;\; \text{Kelly} = \text{Average Excess Return} / \text{Variance of the Excess Returns}
$$

$$
\text{Win Rate} = \text{Number of Positive Returns} / \text{Number of Non-Zero Returns}
$$

$$
\text{Payoff Ratio} = \text{Average Positive Return} / | \text{Average Negative Return} |
$$

A value of 0.25 means putting a quarter of the capital at risk, a value above 1 means borrowing to invest and a negative value means the history shows a negative edge.

For more information, see the following sources:

- Kelly, J.L. (1956). "A New Interpretation of Information Rate." Bell System Technical Journal, 35(4), 917-926.
- Thorp, E.O. (2006). "The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market." Handbook of Asset and Liability Management, Volume 1, 385-428.
- MacLean, L.C., Thorp, E.O. & Ziemba, W.T. (2011). "The Kelly Capital Growth Investment Criterion." World Scientific.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>within_period (bool, optional):</u> Whether to calculate the Kelly Criterion from the daily
returns within each period (e.g. each year if period = 'yearly') or from the returns
of the periods themselves over the whole history. Defaults to True.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the
Kelly Criterion is calculated over a rolling window of this many periods across the
full return history instead of per `period`. Defaults to None.
- <u>method (str, optional):</u> "discrete" (Kelly's bet from the win rate and payoff ratio) or
"continuous" (average excess return over its variance). Defaults to "discrete".
- <u>fraction (float, optional):</u> The share of the full Kelly bet, e.g. 0.5 for half Kelly.
Defaults to 1.0.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Kelly Criterion values.

**Notes:**

- A zero return counts as neither a win nor a loss. The discrete form is NaN without wins
or without losses, the continuous form without variance.
- The continuous form does not depend on the return frequency, since the average and the
variance of the excess returns scale alike.
- There is no Portfolio row: a weighted average of each asset's Kelly Criterion is not the
Kelly Criterion of the portfolio.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "KO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_kelly_criterion()
```

Which returns:

|      |    AAPL |    MSFT |      KO |
|:-----|--------:|--------:|--------:|
| 2021 |  0.1113 |  0.1649 |  0.0911 |
| 2022 | -0.056  | -0.0611 |  0.0557 |
| 2023 |  0.1639 |  0.1547 | -0.0248 |
| 2024 |  0.1137 |  0.0601 |  0.061  |
| 2025 |  0.0433 |  0.0694 |  0.0717 |

---

## get_return_statistics
Calculate the statistics traders report about the returns of an investment portfolio or asset: how often it wins, how large its wins and losses are, how long its winning and losing streaks run and how its gains relate to its drawdown and tails.

Unlike the Win Rate of `get_win_rate`, which counts the periods an asset beats its benchmark, these statistics are absolute: a win is a positive return.

The formulas are as follows:

$$
\text{Win Rate} = \text{Number of Positive Returns} / \text{Number of Non-Zero Returns}
$$

$$
\text{Average Win} = \text{Average of the Positive Returns}
$$

$$
\text{Average Loss} = \text{Average of the Negative Returns}
$$

$$
\text{Payoff Ratio} = \text{Average Win} / | \text{Average Loss} |
$$

$$
\text{Profit Factor} = \text{Sum of the Positive Returns} / | \text{Sum of the Negative Returns} |
$$

$$
\text{Expectancy} = \text{Win Rate}\; x \;\text{Average Win} + (1 - \text{Win Rate}) x \;\text{Average Loss}
$$

$$
\text{Max Consecutive Wins} (\text{Losses}) = \text{The longest run of positive} (\text{negative}) \text{returns}
$$

$$
\text{Recovery Factor} = \text{Cumulative Return} / | \text{Maximum Drawdown} |
$$

$$
\text{Common Sense Ratio} = \text{Profit Factor}\; x \;\text{Tail Ratio} (\text{95th} / \text{5th} \;\text{percentile})
$$

The definitions follow the QuantStats package, except that the Recovery Factor compounds the returns into the cumulative return and keeps its sign (QuantStats takes the absolute value of the summed returns), so a history that lost money does not appear to recover.

For more information, see the following sources:

- Tharp, V.K. (2006). "Trade Your Way to Financial Freedom." 2nd ed., McGraw-Hill.
- Aroussi, R. "QuantStats: Portfolio analytics for quants." [https://github.com/ranaroussi/quantstats](https://github.com/ranaroussi/quantstats){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The period of the returns over the whole history, or with
within_period=True the period the daily returns are grouped by. Defaults to "daily",
or with within_period=True to "quarterly" if the Toolkit is initialised with
quarterly=True, otherwise "yearly".
- <u>within_period (bool, optional):</u> Whether to calculate the statistics from the daily returns
within each period (e.g. each year if period = 'yearly') instead of from the returns of
`period` over the whole history. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).

**Returns:**

pd.DataFrame: Over the whole history, the statistics as the index and the tickers as the
columns. Within periods, the periods as the index and (statistic, ticker) as the columns.

**Notes:**

- A zero return is neither a win nor a loss: it is left out of the Win Rate and ends a
streak. Each ticker is measured over its own returns.
- A statistic without the returns it needs, such as the Profit Factor or the Payoff Ratio
without losses, is NaN, as for the Omega Ratio.
- There is no Portfolio column: a weighted average of streak lengths or payoff ratios is
not the statistic of the portfolio.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "KO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_return_statistics()
```

Which returns:

|                        |    AAPL |    MSFT |      KO |
|:-----------------------|--------:|--------:|--------:|
| Win Rate               |  0.5316 |  0.524  |  0.5326 |
| Average Win            |  0.0125 |  0.0121 |  0.0073 |
| Average Loss           | -0.0126 | -0.0116 | -0.0075 |
| Payoff Ratio           |  0.9963 |  1.0407 |  0.9769 |
| Profit Factor          |  1.1306 |  1.1458 |  1.1131 |
| Expectancy             |  0.0008 |  0.0008 |  0.0004 |
| Max Consecutive Wins   | 11      |  9      |  9      |
| Max Consecutive Losses |  8      |  8      |  7      |
| Recovery Factor        |  3.4734 |  3.5343 |  3.1047 |
| Common Sense Ratio     |  1.0549 |  1.0935 |  1.196  |

---

## get_compound_growth_rate
This function calculates the Compound Growth Rate (CGR) for different periods: yearly, quarterly, monthly, weekly, and daily.

The CGR is a measure that provides the mean growth rate of an investment over a specified period of time. It is a useful measure for comparing the performance of investments over different time periods or across different asset classes. The CGR is calculated by taking the ratio of the final value to the initial value, raising it to the inverse of the number of periods, and then subtracting one.

The formula is as follows:

$$
\text{Years} = (\text{Last Date} - \text{First Date}) / 365.25 \;\text{days}
$$

$$
\text{CAGR} = (\text{Final Value} / \text{Initial Value}) ^{1 / \text{Years}} - 1
$$

$$
\text{Period Rate} = (1 + \text{CAGR}) ^{1 / \text{Periods per Year}} - 1
$$

The CAGR is measured on calendar time: each asset from its own first to its own last close between the start and end date, with the years in between counted in calendar days. The rate thereby does not depend on how often an asset trades, so a stock (which trades on weekdays) and a cryptocurrency (which trades every day) in the same Toolkit are measured over the same years, and an asset without a close on the first or last date of the range is measured over the dates it has. The quarterly, monthly, weekly and daily rates follow from the CAGR with 4 quarters, 12 months, 52 weeks and 252 trading days to a year, so the rates are consistent with each other: (1 + CDGR) ^ 252 equals 1 + CAGR.

**Also known as:** CAGR, compound annual growth rate, annualized return.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. If not provided,
the function will use the default rounding value set in the class instance.

**Returns:**

pd.DataFrame: A DataFrame containing the CGR for each period. The DataFrame has the periods
as the index and the CGR values as the column.

**Notes:**

- When verifying the calculation, note that rounding applies and it could be slightly off because of that
This is mostly noticeable when looking at the Compound Daily Growth Rate. Adjust the rounding with the
rounding parameter accordingly to get a more precise figure.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["BTCUSD", "ETHUSD", "^GSPC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_compound_growth_rate()
```

Which returns:

|                                       |   BTCUSD |   ETHUSD |   ^GSPC |   Benchmark |
|:--------------------------------------|---------:|---------:|--------:|------------:|
| Compound Annual Growth Rate (CAGR)    |   0.2438 |   0.3236 |  0.1312 |      0.1469 |
| Compound Quarterly Growth Rate (CQGR) |   0.0561 |   0.0726 |  0.0313 |      0.0348 |
| Compound Monthly Growth Rate (CMGR)   |   0.0183 |   0.0236 |  0.0103 |      0.0115 |
| Compound Weekly Growth Rate (CWGR)    |   0.0042 |   0.0054 |  0.0024 |      0.0026 |
| Compound Daily Growth Rate (CDGR)     |   0.0009 |   0.0011 |  0.0005 |      0.0005 |

---

## get_returns
Calculate the Return of an investment portfolio or asset for a given period based on the daily historical returns.

The period Return is obtained by compounding the daily returns within each period. If cumulative is set to True, the period returns within the selected date range are compounded further into a cumulative return (growth of 1) instead.

The formula is as follows:

$$
\text{Period Return} = ((1 + \text{Daily Return}\; 1) \cdot (1 + \text{Daily Return}\; 2) \cdot ... \cdot (1 + \text{Daily Return}\; N)) - 1
$$

$$
\text{Cumulative Return} = (1 + \text{Period Return}\; 1) \cdot (1 + \text{Period Return}\; 2) \cdot ... \cdot (1 + \text{Period Return}\; N)
$$

The compounding starts at 1 at the beginning of the date range, so the first value is 1 plus the return of the first period.

The first daily return in the range is that of the second trading day: the prices start at the start_date, so the move from the previous close into the first day is not part of it. For a year-to-date or calendar-year return, set start_date to the last trading day of the previous year (e.g. start_date="2025-12-31" for the return of 2026 so far), so the first period starts from that close.

A period without any daily return for a ticker (before it listed, or a gap in its history) is NaN rather than 0, and the cumulative return carries the previous value past such a period.

**Also known as:** periodic return.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (weekly, monthly, quarterly, or yearly). Defaults
to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise "yearly".
- <u>cumulative (bool, optional):</u> Whether to return the cumulative return over time
instead of the discrete return per period. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Return values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: Return values with time as the index.

**Notes:**

- The method retrieves the daily historical return data and calculates the Return for
the specified `period` for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of Return values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["ASML.AS", "SAP.DE", "MC.PA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_returns()
```

Which returns:

| Date   |   ASML.AS |   SAP.DE |   MC.PA |   Benchmark |
|:-------|----------:|---------:|--------:|------------:|
| 2021   |    0.748  |   0.2018 |  0.4345 |      0.3058 |
| 2022   |   -0.2789 |  -0.2049 | -0.0478 |     -0.1818 |
| 2023   |    0.3664 |   0.4709 |  0.0958 |      0.2615 |
| 2024   |    0.0035 |   0.7229 | -0.1179 |      0.2493 |
| 2025   |    0.3709 |  -0.115  |  0.0393 |      0.1778 |

---

## get_excess_return
Calculate the Excess Return of an investment portfolio or asset for a given period based on the daily historical returns.

The Excess Return is defined as the period Return minus the risk free rate earned over that period. If cumulative is set to True, the excess returns within the selected date range are compounded further into a cumulative excess return (growth of 1) instead.

The formula is as follows:

$$
\text{Period Return} = ((1 + \text{Daily Return}\; 1) \cdot (1 + \text{Daily Return}\; 2) \cdot ... \cdot (1 + \text{Daily Return}\; N)) - 1
$$

$$
\text{Period Risk Free Rate} = (1 + \text{Average Annual Risk Free Rate}) ^{1 / \text{Periods per Year}} - 1,\;\; \text{with the average taken over the daily Treasury yields within the period}
$$

$$
\text{Excess Return} = \text{Period Return} - \text{Period Risk Free Rate}
$$

$$
\text{Cumulative Excess Return} = (1 + \text{Excess Return}\; 1) \cdot (1 + \text{Excess Return}\; 2) \cdot ... \cdot (1 + \text{Excess Return}\; N)
$$

The compounding starts at 1 at the beginning of the date range, so the first value is 1 plus the excess return of the first period.

A period without any daily return for a ticker (before it listed, or a gap in its history) is NaN rather than 0, and the cumulative excess return carries the previous value past such a period.

**Also known as:** return minus the risk-free rate.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (weekly, monthly, quarterly, or yearly). Defaults
to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise "yearly".
- <u>cumulative (bool, optional):</u> Whether to return the cumulative excess return over time
instead of the discrete excess return per period. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Excess Return values over time.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: Excess Return values with time as the index.

**Notes:**

- The method retrieves the daily historical return data and calculates the Excess Return for
the specified `period` for each asset in the Toolkit instance.
- The risk-free rate is the Toolkit's risk_free_rate, the 10-year US Treasury yield by default. Many
textbook definitions (Sharpe, 1994; the Ken French factors) use a short-term Treasury bill instead, which
the Toolkit uses when initialised with risk_free_rate="13w".
- If `growth` is set to True, the method calculates the growth of Excess Return values using the
specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["MCD", "SBUX", "CMG"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_excess_return()
```

Which returns:

| Date   |     MCD |    SBUX |     CMG |   Benchmark |
|:-------|--------:|--------:|--------:|------------:|
| 2021   |  0.2901 |  0.1399 |  0.3099 |      0.2912 |
| 2022   | -0.0255 | -0.1604 | -0.2359 |     -0.2112 |
| 2023   |  0.1112 | -0.0511 |  0.6093 |      0.222  |
| 2024   | -0.0405 | -0.0669 |  0.2772 |      0.2071 |
| 2025   |  0.0359 | -0.0956 | -0.4292 |      0.1347 |

---

## get_correlation_matrix
Calculate the full pairwise Correlation Matrix across all assets (and the benchmark) in the Toolkit instance, based on the returns at the frequency given by `period`.

Unlike `get_beta`, which relates a single asset to the benchmark, this computes the correlation between every pair of assets at once. This is a prerequisite for portfolio variance calculations and any mean-variance optimization work.

The `period` sets the return frequency, and with it the number of observations: yearly returns over five years give only a handful of points per pair, which makes the correlations close to meaningless, so monthly or weekly returns over the same span are the usual choice for diversification and portfolio work. Correlations between risky assets tend to rise in sell-offs, so a matrix estimated over a calm stretch understates how much assets fall together when it matters.

The formula is as follows:

$$
\text{Correlation} (A,\; B) = \text{Covariance} (\text{Return}\; A,\; \text{Return}\; B) / (\text{Standard Deviation}\; A \cdot \text{Standard Deviation}\; B),\;\; \text{the Pearson correlation of the period returns (e.g. monthly) within the Toolkit's date range},\;\; \text{using the overlapping (pairwise complete) observations of each pair}
$$

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (weekly, monthly, quarterly, or yearly). Defaults
to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise "yearly".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).

**Returns:**

pd.DataFrame: The N x N Correlation Matrix, with assets as both the index and
the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["TLT", "GLD", "EFA", "VNQ"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_correlation_matrix(period="monthly")
```

Which returns:

|           |    TLT |    GLD |    EFA |    VNQ |   Benchmark |
|:----------|-------:|-------:|-------:|-------:|------------:|
| TLT       | 1      | 0.3747 | 0.6185 | 0.6626 |      0.5646 |
| GLD       | 0.3747 | 1      | 0.3918 | 0.2266 |      0.1283 |
| EFA       | 0.6185 | 0.3918 | 1      | 0.781  |      0.7999 |
| VNQ       | 0.6626 | 0.2266 | 0.781  | 1      |      0.8282 |
| Benchmark | 0.5646 | 0.1283 | 0.7999 | 0.8282 |      1      |

---

## get_covariance_matrix
Calculate the full pairwise Covariance Matrix across all assets (and the benchmark) in the Toolkit instance, based on the returns at the frequency given by `period`.

Unlike `get_covariance`, which relates a single asset to the benchmark, this computes the covariance between every pair of assets at once. This is a prerequisite for portfolio variance calculations and any mean-variance optimization work.

The formula is as follows:

$$
\text{Covariance} (A,\; B) = \operatorname{SUM}((\text{Return}\; A - \text{Mean Return}\; A) \cdot (\text{Return}\; B - \text{Mean Return}\; B)) / (N - 1),\;\; \text{the sample covariance (ddof=1) of the period returns (e.g. monthly) within the Toolkit's date range},\;\; \text{per period and not annualized},\;\; \text{using the overlapping (pairwise complete) observations of each pair}
$$

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (weekly, monthly, quarterly, or yearly). Defaults
to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise "yearly".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).

**Returns:**

pd.DataFrame: The N x N Covariance Matrix, with assets as both the index and
the columns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["^GSPC", "EURUSD", "GCUSD", "CLUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_covariance_matrix(period="monthly")
```

Which returns:

|           |   ^GSPC |   EURUSD |   GCUSD |   CLUSD |   Benchmark |
|:----------|--------:|---------:|--------:|--------:|------------:|
| ^GSPC     |  0.0019 |   0.0003 |  0.0003 |  0.0003 |      0.0019 |
| EURUSD    |  0.0003 |   0.0005 |  0.0005 | -0.0001 |      0.0003 |
| GCUSD     |  0.0003 |   0.0005 |  0.0018 | -0.0007 |      0.0003 |
| CLUSD     |  0.0003 |  -0.0001 | -0.0007 |  0.0067 |      0.0003 |
| Benchmark |  0.0019 |   0.0003 |  0.0003 |  0.0003 |      0.0019 |

---

## get_appraisal_ratio
Calculate the Appraisal Ratio, i.e. Jensen's Alpha divided by the idiosyncratic (residual, unsystematic) standard deviation left over from the CAPM regression that produced that Alpha.

Jensen's Alpha (see `get_jensens_alpha`) measures how much return a manager generated above what CAPM would predict given the asset's Beta. However, a large Alpha achieved with wildly noisy, unpredictable residual returns is far less attractive than the same Alpha achieved consistently. The Appraisal Ratio normalizes Alpha by that noise (the "specific risk" not explained by market exposure), giving a Sharpe-ratio-like measure of stock-picking or timing skill per unit of idiosyncratic risk taken.

The formula is as follows:

$$
\text{Appraisal Ratio} = \text{Jensen's Alpha} / \text{Residual Standard Deviation}
$$

Where the residual standard deviation is the standard deviation of the pointwise CAPM regression residuals (Asset Excess Return − Beta * Benchmark Excess Return), reusing the exact same CAPM regression formula as `get_jensens_alpha`.

**See definition:** [https://en.wikipedia.org/wiki/Information_ratio](https://en.wikipedia.org/wiki/Information_ratio){:target="_blank"}

**Also known as:** Treynor-Black Appraisal Ratio.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>rolling (int, optional):</u> The rolling window size to use for the Beta component of the
calculation. If set, Beta is estimated over a rolling window of this many periods across
the full return history instead of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Appraisal Ratio values.

**Notes:**

- Daily Appraisal Ratio is not an option as the standard deviation for 1 day is close to
zero. Therefore, it does not give any useful insights.
- The method retrieves historical data and calculates Jensen's Alpha and the CAPM
regression residuals for each asset in the Toolkit instance, reusing the same Beta and
CAPM formula as `get_jensens_alpha`.
- If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["ADBE", "CRM", "ORCL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2020-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_appraisal_ratio()
```

Which returns:

| Date   |    ADBE |     CRM |    ORCL |
|:-------|--------:|--------:|--------:|
| 2021   | -1.1711 | -0.8087 |  0.5274 |
| 2022   | -0.4641 | -0.6351 |  0.5198 |
| 2023   |  1.5758 |  2.7157 |  0.1366 |
| 2024   | -1.6901 | -0.1944 |  0.9946 |
| 2025   | -1.4152 | -1.4877 | -0.1032 |

---

## get_fama_decomposition
Calculate the Fama (1972) decomposition of total excess return into Selectivity and Diversification.

Jensen's Alpha alone conflates two very different sources of excess return: genuine stock/timing selection skill, and simply carrying more total risk than the market by holding an under-diversified portfolio (which, in a CAPM world, should be compensated with extra return even absent any skill). Fama's decomposition separates the two by comparing the portfolio's actual return against two different CAPM-implied return benchmarks: one using the portfolio's actual Beta (systematic risk only), and one using the portfolio's actual *total* risk ratio (Sigma_Portfolio / Sigma_Market) in place of Beta.

The formulas are as follows:

$$
\text{Selectivity} = (\text{Asset Return} - \text{Risk-Free Rate}) - (\text{Sigma\_Portfolio} / \text{Sigma\_Market}) \cdot (\text{Benchmark Return} - \text{Risk-Free Rate})
$$

$$
\text{Diversification} = \left[\text{Risk-Free Rate} + (\text{Sigma\_Portfolio} / \text{Sigma\_Market}) \cdot (\text{Benchmark Return} - \text{Risk-Free Rate})\right] - \left[\text{Risk-Free Rate} + \text{Beta} \cdot (\text{Benchmark Return} - \text{Risk-Free Rate})\right]
$$

Selectivity is the return earned above what would be required for a fully diversified portfolio carrying the same total risk, i.e. genuine security selection or timing skill. Diversification is the extra return the manager left on the table (if positive, it is a cost) by taking on unsystematic risk that a fully diversified portfolio of the same total risk would not have. Selectivity plus Diversification equals Jensen's Alpha (see `get_jensens_alpha`).

**Also known as:** Fama's Net Selectivity, Fama performance decomposition.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>rolling (int, optional):</u> The rolling window size to use for the Beta component of the
calculation. If set, Beta is estimated over a rolling window of this many periods across
the full return history instead of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Selectivity and Diversification values, with a Multi Index of
(ticker, component) as the columns.

**Notes:**

- Daily Fama Decomposition is not an option as the standard deviation for 1 day is close
to zero. Therefore, it does not give any useful insights.
- The method retrieves historical data and calculates Beta, the asset's and benchmark's
standard deviation, and the Selectivity and Diversification components for each asset in
the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["QQQ", "IWM", "XLE"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2020-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_fama_decomposition().xs("Selectivity", level=1, axis=1)
```

Which returns:

| Date   |     QQQ |     IWM |     XLE |
|:-------|--------:|--------:|--------:|
| 2021   | -0.123  | -0.3304 | -0.1035 |
| 2022   | -0.0751 |  0.0106 |  0.9216 |
| 2023   |  0.2052 | -0.2125 | -0.4352 |
| 2024   | -0.0824 | -0.2697 | -0.28   |
| 2025   |  0.0022 | -0.0738 | -0.1338 |

---

## get_starr_ratio
Calculate the STARR (Stable Tail Adjusted Return Ratio) of an investment portfolio or asset's returns.

The Sharpe ratio penalizes upside and downside volatility equally via the standard deviation. The STARR ratio instead scales the mean excess return by the Conditional Value at Risk (CVaR / Expected Shortfall), a coherent tail-risk measure that only looks at the average magnitude of losses beyond the `alpha` quantile. This makes STARR more appropriate than the Sharpe ratio for return distributions with fat left tails.

The formula is as follows:

$$
\text{STARR Ratio} = \text{Excess Return} / | \operatorname{CVaR}(\alpha) |
$$

**See definition:** [https://en.wikipedia.org/wiki/Expected_shortfall](https://en.wikipedia.org/wiki/Expected_shortfall){:target="_blank"}

**Also known as:** Stable Tail Adjusted Return Ratio, Conditional Sharpe Ratio.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>within_period (bool, optional):</u> Whether to calculate the CVaR within the specified
period or for the entire period. Thus whether to look at the CVaR within a specific
year (if period = 'yearly') or look at the entirety of all years. Defaults to True.
- <u>alpha (float, optional):</u> The confidence level used for the CVaR calculation (e.g. 0.05
for the worst 5% of outcomes). Defaults to 0.05.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: STARR Ratio values.

**Notes:**

- The method retrieves historical data and calculates the STARR Ratio for each asset in
the Toolkit instance.
- Periods with very few return observations (e.g. a partial period at the very start of
the selected date range) can produce a degenerate (e.g. zero or ±infinite) CVaR, since
CVaR is not a meaningful statistic with only one or two data points. This mirrors the
analogous caveat for the Sharpe Ratio needing enough observations for its standard
deviation to be meaningful.
- If `growth` is set to True, the method calculates the growth of the ratio values using
the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["CAT", "DE", "HON"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2020-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_starr_ratio()
```

Which returns:

| Date   |    CAT |      DE |     HON |
|:-------|-------:|--------:|--------:|
| 2021   | 0.287  |  0.4693 | -0.0376 |
| 2022   | 0.2125 |  0.2897 |  0.0386 |
| 2023   | 0.3701 | -0.1499 | -0.0915 |
| 2024   | 0.3598 |  0.063  |  0.1513 |
| 2025   | 0.8327 |  0.1243 | -0.1867 |

---

## get_rachev_ratio
Calculate the Rachev Ratio (R-Ratio) of an investment portfolio or asset's returns.

The Rachev ratio compares the "quality" of the best outcomes to the "quality" of the worst outcomes by taking the ratio of the right-tail Expected Shortfall (the average of the best `alpha` fraction of returns) to the left-tail Expected Shortfall (the average magnitude of the worst `alpha` fraction of returns). A ratio above 1 indicates that the average size of extreme gains outweighs the average size of extreme losses.

The formula is as follows:

$$
\text{Rachev Ratio} = \operatorname{ES\_right}(\alpha) / \operatorname{ES\_left}(\alpha)
$$

**Also known as:** R-Ratio.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>within_period (bool, optional):</u> Whether to calculate the Rachev Ratio within the
specified period or for the entire period. Thus whether to look at the return
distribution within a specific year (if period = 'yearly') or look at the entirety of
all years. Defaults to True.
- <u>alpha (float, optional):</u> The confidence level used for both tails (e.g. 0.05 for the
best/worst 5% of outcomes). Defaults to 0.05.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Rachev Ratio values.

**Notes:**

- The method retrieves historical data and calculates the Rachev Ratio for each asset in
the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the ratio values using
the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["TSLA", "AMD", "PLTR"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_rachev_ratio()
```

Which returns:

|      |   TSLA |    AMD |   PLTR |
|:-----|-------:|-------:|-------:|
| 2021 | 1.2069 | 1.1556 | 1.2789 |
| 2022 | 0.9469 | 0.9396 | 0.9301 |
| 2023 | 1.1169 | 1.3483 | 1.6236 |
| 2024 | 1.3081 | 0.8908 | 2.0305 |
| 2025 | 1.0925 | 1.4024 | 1.0683 |

---

## get_treynor_mazuy_model
Calculate the Treynor-Mazuy market timing model for each asset in the Toolkit instance.

Jensen's Alpha and Beta from a plain CAPM regression cannot distinguish stock-picking skill (selectivity) from market-timing skill (shifting exposure ahead of market moves). The Treynor-Mazuy model adds a quadratic term in the benchmark excess return to the regression: a manager who successfully increases (decreases) market exposure ahead of up (down) markets will show a return profile that curves upward as a function of the benchmark return, captured by a positive quadratic coefficient (Gamma).

The formula is as follows:

$$
\text{Excess Return} = \text{Alpha} + \text{Beta} \cdot \text{Benchmark Excess Return} + \text{Gamma} \cdot \text{Benchmark Excess Return} ^{2} + \text{Residuals}
$$

Gamma > 0 indicates positive market-timing ability; Gamma <= 0 indicates no timing ability.

**Also known as:** Treynor-Mazuy quadratic timing model, TM model.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Alpha, Beta, Gamma and R Squared values, with a Multi Index of
(ticker, parameter) as the columns.

**Notes:**

- Daily and weekly Treynor-Mazuy results are not an option as there would be too few
observations within each period to run a meaningful regression.
- The method retrieves historical data and performs a quadratic regression for each asset
in the Toolkit instance, within each period.
- If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["ARKK", "JEPI"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_treynor_mazuy_model().xs("ARKK", level=0, axis=1)
```

Which returns:

|      |   Alpha |   Beta |    Gamma |   R Squared |
|:-----|--------:|-------:|---------:|------------:|
| 2021 | -0.0034 | 1.6646 |  12.4821 |      0.2937 |
| 2022 | -0.0035 | 2.1567 |   6.9512 |      0.5959 |
| 2023 |  0.0015 | 2.2614 | -14.8854 |      0.529  |
| 2024 | -0.001  | 2.1368 |  -3.1566 |      0.5658 |
| 2025 |  0.0006 | 1.8994 |  -1.3437 |      0.6767 |

---

## get_henriksson_merton_model
Calculate the Henriksson-Merton market timing model for each asset in the Toolkit instance.

Like the Treynor-Mazuy model (see `get_treynor_mazuy_model`), this separates market-timing skill from selectivity, but models timing as a piecewise (rather than quadratic) change in Beta: a "down-market" Beta and an "up-market" Beta.

The formula is as follows:

$$
\text{Excess Return} = \text{Alpha} + \text{Beta} \cdot \text{Benchmark Excess Return} + \text{Up Market Beta} \cdot \max(\text{Benchmark Excess Return},\; 0) + \text{Residuals}
$$

Beta is the "down-market" Beta (the portfolio's market exposure when the benchmark excess return is negative), and Beta + Up Market Beta is the "up-market" Beta. Up Market Beta > 0 indicates positive market-timing ability; Up Market Beta <= 0 indicates no timing ability.

**Also known as:** Henriksson-Merton piecewise timing model, HM model.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: Alpha, Beta, Up Market Beta and R Squared values, with a Multi Index of
(ticker, parameter) as the columns.

**Notes:**

- Daily and weekly Henriksson-Merton results are not an option as there would be too few
observations within each period to run a meaningful regression.
- The method retrieves historical data and performs a piecewise regression for each asset
in the Toolkit instance, within each period.
- If `growth` is set to True, the method calculates the growth of the ratio values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["BRK-B", "FBCG"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_henriksson_merton_model().xs("FBCG", level=0, axis=1)
```

Which returns:

|      |   Alpha |   Beta |   Up Market Beta |   R Squared |
|:-----|--------:|-------:|-----------------:|------------:|
| 2021 | -0.0004 | 1.4217 |          -0.064  |      0.7204 |
| 2022 | -0.0009 | 1.4208 |           0.0312 |      0.885  |
| 2023 |  0.0004 | 1.359  |           0.0602 |      0.8342 |
| 2024 |  0      | 1.4674 |           0.0496 |      0.8536 |
| 2025 |  0.0002 | 1.3907 |          -0.0759 |      0.8893 |

---

## get_factor_analysis
Factor analysis (predictive power) of the performance metrics, or of a factor of your own: whether the tickers that score high on a metric go on to return more than those that score low. Per period, the information coefficient (IC) is the Spearman rank correlation between the metric of the tickers in the period and their return over the following horizon: 1 means the metric ranks the later returns perfectly, -1 in reverse and 0 that it says nothing about them. The IC measures skill in Grinold and Kahn's fundamental law of active management, IR ≈ IC × √breadth: a small but consistent IC across many tickers and periods gives a high information ratio.

The summary has a row per metric and horizon with the mean IC, its standard deviation, the IC information ratio (mean divided by standard deviation), the t-statistic of the mean with its p-value, the share of periods with a positive IC, the number of periods, the top minus bottom spread (the mean forward return of the highest quantile minus that of the lowest), the mean turnover of the top and bottom quantiles and the mean rank autocorrelation of the metric from one period to the next. With detail, it returns one of those parts per period (or per quantile) for a single metric.

Each metric is measured within each period (e.g. the volatility of a month's daily returns) and compared with the returns from the close of the period's last trading day onwards, using the dividend and split adjusted close, so a metric never overlaps the returns it is compared with. Each ticker keeps its own history: a ticker without a value or a return in a period is left out of that period only.

A factor of your own is a DataFrame with the dates as index and the tickers as columns, applied from each date on, or with the tickers as index and periods as columns, applied from the end of each period. Make sure each value was known on the date it is given for, or the analysis looks ahead.

**Args:**

- <u>metrics (str &#124; list[str] &#124; pd.DataFrame):</u> A performance method name with a value per ticker and
period, e.g. "get_sharpe_ratio", a list of them, "all", or a factor of your own
as a DataFrame. "all" holds the returns, excess return, beta, Sharpe, Sortino,
Treynor and information ratios, tracking error, Jensen's alpha, Calmar and
Omega ratios and the win rate. Defaults to "all".
- <u>period (str, optional):</u> The frequency at which the metrics are measured and
evaluated: weekly, monthly, quarterly or yearly. Each metric is calculated
within each period from that period's daily returns, so use monthly or longer
for enough returns per period. Defaults to "monthly".
- <u>horizons (list[int] &#124; int &#124; None, optional):</u> The number of periods the forward
returns cover. Defaults to None, which uses about a period, a quarter and a
year ahead (1, 3 and 12 months for monthly).
- <u>quantiles (int, optional):</u> The number of quantiles the tickers are sorted into per
period. Defaults to 5.
- <u>periods_apart (int, optional):</u> The number of periods between the dates the
quantile turnover and the rank autocorrelation compare. Defaults to 1.
- <u>detail (str &#124; None, optional):</u> Returns one part of the analysis of a single metric
instead of the summary: "information_coefficient" (per period and horizon),
"quantile_returns" (the mean forward return per quantile and horizon),
"quantile_turnover" (per period and quantile) or "rank_autocorrelation" (per
period). Defaults to None.
- <u>column (str &#124; None, optional):</u> The output to use of a metric with several.
Defaults to None, which uses the first.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
**kwargs: Parameters passed to the metrics that take them, e.g. alpha=0.05.

**Returns:**

pd.DataFrame: The summary per metric and horizon, or with detail that part of the
analysis of the metric.

**Notes:**

- The IC is reported as measured: short-term reversal, where last month's
winners go on to lag, shows as a negative IC for the monthly return. Read the
sign as the direction of the relationship.
- The cross-section is the tickers of the Toolkit, so use at least ten and
preferably twenty or more for a meaningful rank correlation and quantiles.
- A horizon longer than one period makes consecutive returns overlap, which
inflates the t-statistic; judge those horizons by their mean IC and IC
information ratio.
- Based on alphalens (Quantopian) and on Grinold and Kahn (2000), Active Portfolio
Management.

Also known as: predictive power, information coefficient, factor testing, alpha signal

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "JPM", "JNJ",
     "XOM", "PG", "KO", "WMT", "V", "UNH", "HD", "CVX"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2016-01-01",
    end_date="2025-12-31",
)

# Momentum: the return over the previous twelve months, without the latest month.
prices = toolkit.get_historical_data()["Adj Close"]
momentum = (prices.shift(21) / prices.shift(252) - 1).drop(columns="Benchmark")

toolkit.performance.get_factor_analysis(momentum, horizons=[1, 12])
```

Which returns:

|                                |   Mean IC |   IC Standard Deviation |   IC Information Ratio |   t-Statistic |   p-Value |   Positive Share |   Observations |   Top Minus Bottom |   Quantile Turnover |   Rank Autocorrelation |
|:-------------------------------|----------:|------------------------:|-----------------------:|--------------:|----------:|-----------------:|---------------:|-------------------:|--------------------:|-----------------------:|
| ('Custom Factor', '1 Month')   |    0.018  |                  0.3745 |                 0.0481 |        0.498  |    0.6195 |           0.4953 |            107 |             0.004  |              0.2391 |                 0.8822 |
| ('Custom Factor', '12 Months') |    0.1122 |                  0.419  |                 0.2678 |        2.6242 |    0.0101 |           0.5729 |             96 |             0.0195 |              0.2391 |                 0.8822 |

---

## get_sharpe_ratio_standard_error
Calculate the standard error of the Sharpe ratio: how far the measured Sharpe ratio may lie from the true one. A Sharpe ratio measured over a year of daily returns is an estimate, and roughly 95% of the time the true ratio lies within two standard errors of it.

The formulas are as follows, with SR the Sharpe ratio of one observation (the Sharpe ratio of `get_sharpe_ratio` without annualizing) and n the number of observations:

$$
\text{"iid":}\;\; \text{SE} = \sqrt{(1 + \text{SR} ^{2} / 2) / n},\;\; \text{for normally and independently distributed returns (Lo, 2002, equation 9)}
$$

$$
\text{"non\_normal":}\;\; \text{SE} = \sqrt{(1 - \text{γ₃} \cdot \text{SR} + ((\text{γ₄} - 1) / 4) \cdot \text{SR} ^{2}) / (n - 1)},\;\; \text{for independent but skewed and fat-tailed returns},\;\; \text{with γ₃ the skewness and γ₄ the non-excess (raw) kurtosis (Mertens, 2002; the standard error inside the Probabilistic Sharpe Ratio of Bailey and López de Prado, 2012)}
$$

$$
\text{"gmm":}\;\; \text{SE} = \sqrt{\text{∂g} / \text{∂theta} \cdot \text{Σ} \cdot \text{∂g} / \text{∂theta'} / n},\;\; \text{for} \;\; \text{returns that may also be serially correlated and heteroskedastic} (\text{Lo},\; 2002,\; \text{Appendix}) . \;\text{With}\; \theta = (\mu,\; \sigma ^{2}) \text{and}\; g (\theta) = \mu / \sigma,\;\; \text{∂g} / \text{∂theta} = (1 / \sigma,\; - \mu / (\text{2sigma} ^{3})) \text{and}\; \text{Σ} \;\text{is the Newey and West} (1987) \text{long-run covariance of the moment conditions} (r_{t} - \mu,\; (r_{t} - \mu) ^{2} - \sigma ^{2})
$$

Negative skewness, fat tails and positive autocorrelation all widen the standard error, so the same Sharpe ratio is then less certain. The standard error is on the scale of the Sharpe ratio of one observation; multiply by SQRT(252) to compare it with a Sharpe ratio annualized by SQRT(252) (exact for the "iid" and "non_normal" errors, a rescaling of the same estimate for "gmm").

For more information about the method, see the following papers:

- Lo, A.W. (2002). "The Statistics of Sharpe Ratios." Financial Analysts Journal, 58(4), 36-52.
- Mertens, E. (2002). "Comments on Variance of the IID Estimator in Lo (2002)." Working Paper, University of Basel.
- Bailey, D.H., & López de Prado, M. (2012). "The Sharpe Ratio Efficient Frontier." Journal of Risk, 15(2), 3-44.
- Newey, W.K., & West, K.D. (1987). "A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix." Econometrica, 55(3), 703-708.

**Also known as:** Sharpe ratio confidence interval, Sharpe ratio estimation error.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>method (str, optional):</u> "iid", "non_normal" or "gmm", as described above. Defaults
to "iid".
- <u>lags (int, optional):</u> The number of lags in the Newey-West covariance, only used
when method="gmm". Defaults to None, which uses the Newey and West (1994) rule
floor(4 * (n / 100)^(2/9)), 4 for a year of daily returns.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the standard errors. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: The standard error of the Sharpe ratio per period.

**Notes:**

- The Sharpe ratio is computed from the daily excess returns within each period, as in
`get_sharpe_ratio`; period="daily" needs intraday data (initialise the Toolkit with an
intraday_period).
- The "non_normal" error uses the bias-corrected sample skewness and kurtosis, as
`get_sharpe_ratio(method="probabilistic")` does; the "gmm" error uses the moments of
GMM (σ² with 1 / n).
- If `growth` is set to True, the method calculates the growth of the values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["SPY", "TLT", "GLD", "BTCUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
    benchmark_ticker=None,
)

toolkit.performance.get_sharpe_ratio_standard_error(method="gmm")
```

Which returns:

| Date   |    SPY |    TLT |    GLD |   BTCUSD |
|:-------|-------:|-------:|-------:|---------:|
| 2021   | 0.0586 | 0.0585 | 0.0635 |   0.0605 |
| 2022   | 0.0602 | 0.0567 | 0.0624 |   0.0589 |
| 2023   | 0.0635 | 0.0564 | 0.0609 |   0.0605 |
| 2024   | 0.0645 | 0.063  | 0.0617 |   0.0585 |
| 2025   | 0.0554 | 0.0611 | 0.0623 |   0.0634 |

---

## get_minimum_track_record_length
Calculate the Minimum Track Record Length (MinTRL): how many return observations are needed before the measured Sharpe ratio is, with the given confidence, above the benchmark Sharpe ratio. A short track record with a high Sharpe ratio can still be luck; the MinTRL says how long the record has to be for it not to be, taking the skewness and fat tails of the returns into account.

The formula is as follows:

$$
\text{MinTRL} = 1 + (1 - \text{γ₃} \cdot \text{SR} + ((\text{γ₄} - 1) / 4) \cdot \text{SR} ^{2}) \cdot (Z_{\alpha} / (\text{SR} - \text{SR} \cdot)) ^{2}
$$

Where SR is the Sharpe ratio of one observation (not annualized), SR* the benchmark Sharpe ratio on the same scale, γ₃ the skewness and γ₄ the non-excess (raw) kurtosis of the excess returns (3 for a normal distribution) and Z_α the standard normal quantile at `confidence_level` (1.645 for 95%). With n = MinTRL observations, the Probabilistic Sharpe Ratio, `get_sharpe_ratio(method="probabilistic")`, equals `confidence_level`. Negative skewness and fat tails lengthen the record needed. When SR does not exceed SR*, no track record is long enough and the value is left out (NaN).

By default one MinTRL is reported per `period`, computed from the daily excess returns within that period, so it counts trading days (divide by 252 for years). For a rolling period, `period` sets the frequency of the returns and the measure is computed over a rolling window of `rolling` such returns, so it counts periods (e.g. months).

For more information about the method, see the following paper:

- Bailey, D.H., & López de Prado, M. (2012). "The Sharpe Ratio Efficient Frontier." Journal of Risk, 15(2), 3-44.

**Also known as:** MinTRL, minimum track record, required track record length.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>rolling (int, optional):</u> The rolling window size, in observations of `period`.
Defaults to None, one value per period.
- <u>benchmark_sharpe_ratio (float, optional):</u> The benchmark Sharpe ratio SR*, on the scale
of one observation (e.g. 1 / SQRT(252) for an annualized benchmark of 1 on daily
returns). Defaults to 0.0, i.e. any skill at all.
- <u>confidence_level (float, optional):</u> The confidence level. Defaults to 0.95.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: The minimum number of return observations per period.

**Notes:**

- The skewness and kurtosis are the bias-corrected sample estimates, as in
`get_sharpe_ratio(method="probabilistic")`.
- period="daily" without rolling needs intraday data (initialise the Toolkit with an
intraday_period).
- If `growth` is set to True, the method calculates the growth of the values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["SPY", "TLT", "GLD", "BTCUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
    benchmark_ticker=None,
)

toolkit.performance.get_minimum_track_record_length()
```

Which returns:

| Date   |      SPY |    TLT |      GLD |   BTCUSD |
|:-------|---------:|-------:|---------:|---------:|
| 2021   |  176.151 |    nan |  nan     | 1701.64  |
| 2023   |  282.904 | 627999 | 1490.71  |  247.195 |
| 2024   |  319.167 |    nan |  381.29  |  337.604 |
| 2025   | 1220.25  | 197659 |  135.453 |  nan     |

---

## get_coskewness
Calculate the co-skewness of each asset with the benchmark: how the asset's return moves with the squared, i.e. large, moves of the market in either direction. An asset with a negative co-skewness does worse when the market makes large moves and adds to the downside skewness of a market portfolio, so investors demand a higher return for holding it (Kraus and Litzenberger, 1976; Harvey and Siddique, 2000). A positive co-skewness works as a hedge against large market moves.

The formulas are as follows:

$$
\text{"standardized":}\;\; \text{Co-Skewness} = E \left[(r_{i} - \mu_{i}) (r_{m} - \mu_{m}) ^{2}\right] / (\sigma_{i} \cdot \sigma_{m} ^{2})
$$

$$
\text{"residual":}\;\; \beta_{SKD} = E \left[\epsilon_{i} \cdot \epsilon_{m} ^{2}\right] / (\sqrt{E \left[\epsilon_{i} ^{2}\right]} \cdot E \left[\epsilon_{m} ^{2}\right]) (\text{Harvey and Siddique},\; 2000)
$$

Where r_i is the asset return, r_m the benchmark return, ε_m = r_m − μ_m and ε_i the residual of the regression r_i = α + β·r_m + ε_i. The residual version only looks at the part of the asset's return the market does not explain, so the market's own skewness does not enter through the beta. For the benchmark itself the standardized co-skewness is the benchmark's skewness.

By default one value is reported per `period`, computed from the daily returns within that period on the dates both the asset and the benchmark have a return. The expectations are population moments (1 / n), so σ_i and σ_m use 1 / n as well and the measure does not depend on the scale of the returns.

For more information about the method, see the following papers:

- Harvey, C.R., & Siddique, A. (2000). "Conditional Skewness in Asset Pricing Tests." Journal of Finance, 55(3), 1263-1295.
- Kraus, A., & Litzenberger, R.H. (1976). "Skewness Preference and the Valuation of Risk Assets." Journal of Finance, 31(4), 1085-1100.

**Also known as:** coskewness, systematic skewness, co-skewness beta.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>method (str, optional):</u> "standardized" or "residual", as described above. Defaults to
"standardized".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: The co-skewness of each asset with the benchmark per period.

**Notes:**

- The returns are the total returns (Adj Close), as for `get_beta`; the risk free rate,
nearly constant within a period, drops out with the means.
- period="daily" needs intraday data (initialise the Toolkit with an intraday_period).
- If `growth` is set to True, the method calculates the growth of the values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "TLT", "GLD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_coskewness()
```

Which returns:

| Date   |    AAPL |    MSFT |     TLT |     GLD |
|:-------|--------:|--------:|--------:|--------:|
| 2021   | -0.1202 | -0.1723 | -0.069  | -0.0972 |
| 2022   |  0.1063 |  0.09   |  0.1369 |  0.0849 |
| 2023   |  0.1241 |  0.085  |  0.0816 |  0.059  |
| 2024   | -0.423  | -0.6011 | -0.0005 | -0.418  |
| 2025   |  1.4001 |  1.4254 |  0.2683 |  0.6826 |

---

## get_cokurtosis
Calculate the co-kurtosis of each asset with the benchmark: how the asset's return moves with the cubed moves of the market, i.e. how much it shares the market's extreme moves. An asset with a high co-kurtosis adds to the fat tails of a market portfolio, and Dittmar (2002) shows that investors who dislike kurtosis demand a higher return for holding it.

The formulas are as follows:

$$
\text{"standardized":}\;\; \text{Co-Kurtosis} = E \left[(r_{i} - \mu_{i}) (r_{m} - \mu_{m}) ^{3}\right] / (\sigma_{i} \cdot \sigma_{m} ^{3})
$$

$$
\text{"residual":}\;\; E \left[\epsilon_{i} \cdot \epsilon_{m} ^{3}\right] / (\sqrt{E \left[\epsilon_{i} ^{2}\right]} \cdot E \left[\epsilon_{m} ^{2}\right] ^{3 / 2})
$$

Where r_i is the asset return, r_m the benchmark return, ε_m = r_m − μ_m and ε_i the residual of the regression r_i = α + β·r_m + ε_i, the residual form Harvey and Siddique (2000) use for co-skewness. For the benchmark itself the standardized co-kurtosis is the benchmark's non-excess kurtosis (3 for normal returns); for an asset with a correlation ρ to normally distributed market returns it is 3ρ.

By default one value is reported per `period`, computed from the daily returns within that period on the dates both the asset and the benchmark have a return. The expectations are population moments (1 / n), so σ_i and σ_m use 1 / n as well.

For more information about the method, see the following papers:

- Dittmar, R.F. (2002). "Nonlinear Pricing Kernels, Kurtosis Preference, and Evidence from the Cross Section of Equity Returns." Journal of Finance, 57(1), 369-403.
- Harvey, C.R., & Siddique, A. (2000). "Conditional Skewness in Asset Pricing Tests." Journal of Finance, 55(3), 1263-1295.

**Also known as:** cokurtosis, systematic kurtosis, co-kurtosis beta.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "quarterly" if the Toolkit is
initialised with quarterly=True, otherwise "yearly".
- <u>method (str, optional):</u> "standardized" or "residual", as described above. Defaults to
"standardized".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: The co-kurtosis of each asset with the benchmark per period.

**Notes:**

- The returns are the total returns (Adj Close), as for `get_beta`; the risk free rate,
nearly constant within a period, drops out with the means.
- period="daily" needs intraday data (initialise the Toolkit with an intraday_period).
- If `growth` is set to True, the method calculates the growth of the values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "TLT", "GLD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.performance.get_cokurtosis()
```

Which returns:

| Date   |    AAPL |    MSFT |     TLT |    GLD |
|:-------|--------:|--------:|--------:|-------:|
| 2021   |  2.3149 |  2.4305 | -0.3616 | 0.761  |
| 2022   |  3.0324 |  2.9407 |  0.6437 | 1.1731 |
| 2023   |  2.0735 |  1.5943 |  0.3763 | 0.0201 |
| 2024   |  2.5064 |  3.5367 | -0.2675 | 1.2651 |
| 2025   | 22.5236 | 18.9645 |  1.749  | 7.2913 |

---

