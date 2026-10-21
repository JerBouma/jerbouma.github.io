## Getting Started

A correlation matrix is where most analyses of how stocks relate start, and too often where they end. The Econometrics module goes further with the methods you'd otherwise set up by hand in `statsmodels` or `linearmodels`: regressions with proper standard errors, normality and unit root tests, Granger causality, cointegration, panel estimators, causal inference and forecasting models, all run directly on the tickers of a `Toolkit`.

This section follows one question from start to finish: **is Apple's stock really tied to its chip suppliers and megacap peers, or does it only look that way from pairwise correlations?** The universe holds Apple's RF, modem and foundry suppliers (`QCOM`, `SWKS`, `TSM`), other megacap tech (`MSFT`, `GOOGL`, `AMZN`, `META`, `NVDA`) and two names from unrelated sectors as a contrast (`XOM`, `PG`). The benchmark is left out on purpose, so the results are not just the whole market moving together.

### Installation and Loading the Data

The module depends on `statsmodels` and `linearmodels`, so it ships as an optional extra. To install it:

```bash
pip install "financetoolkit[econometrics]" -U
```

Then load four years of data, from 2019 up to 2023, for the eleven tickers:

```python
from financetoolkit import Toolkit

companies = Toolkit(
    ["AAPL", "TSM", "QCOM", "SWKS", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "XOM", "PG"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2019-01-01",
    end_date="2023-01-01",
)
```

### Does Anything Explain Apple's Returns?

An OLS regression of Apple's weekly returns on all the other tickers at once controls for every regressor at the same time, unlike a pairwise correlation, which can mislead when the regressors are correlated with each other. Without arguments, the first ticker of the `Toolkit` is the dependent variable and every other ticker an independent variable. To run the regression:

```python
companies.econometrics.get_ols(period="weekly")
```

Which returns the coefficient, standard error, t-statistic and p-value of each regressor:

|           |   Coefficient |   Std. Error |   t-Statistic |   P-Value |
|:----------|--------------:|-------------:|--------------:|----------:|
| Intercept |        0.0028 |       0.0017 |        1.6788 |    0.0948 |
| TSM       |       -0.0043 |       0.0523 |       -0.0815 |    0.9351 |
| QCOM      |        0.1429 |       0.0361 |        3.9547 |    0.0001 |
| SWKS      |        0.2137 |       0.0485 |        4.4017 |    0.0000 |
| MSFT      |        0.3039 |       0.0866 |        3.5098 |    0.0006 |
| GOOGL     |        0.1444 |       0.0691 |        2.0901 |    0.0379 |
| AMZN      |        0.0616 |       0.0530 |        1.1616 |    0.2468 |
| META      |       -0.0132 |       0.0390 |       -0.3379 |    0.7358 |
| NVDA      |       -0.0024 |       0.0414 |       -0.0571 |    0.9545 |
| XOM       |       -0.0290 |       0.0374 |       -0.7758 |    0.4388 |
| PG        |        0.2858 |       0.0709 |        4.0298 |    0.0001 |

The same coefficients with their 95% confidence intervals, where the coloured ones are significant at the 5% level:

{% include ft-chart.html id="econometrics-ols" src="/assets/data/financetoolkit-guides/econometrics.json" label="OLS coefficients with 95% confidence intervals" %}

Only some of the plausible relationships survive. The chip suppliers `QCOM` and `SWKS` and the megacap peers `MSFT` and `GOOGL` are significant, while `AMZN`, `META`, `NVDA` and the unrelated `XOM` are not. Two results go against intuition: `PG`, a consumer staples company picked as an unrelated contrast, is significant, while Apple's own foundry `TSM` is not. That is a first hint of multicollinearity: when the regressors move together, a multiple regression can both hide and manufacture relationships. Use `dependent_ticker` and `independent_tickers` to choose the variables yourself, `include_benchmark=True` to add the market, and `cov_type="HC1"` or `"HAC"` for robust standard errors.

How much the regressors move together shows in the correlation matrix of the same weekly returns. To calculate it, leaving out the benchmark again:

```python
weekly_returns = companies.get_historical_data(period="weekly")["Return"]

weekly_returns.drop(columns="Benchmark").corr()
```

Which gives the following, with the darker blue cells the most closely related pairs:

{% include ft-chart.html id="econometrics-correlations" src="/assets/data/financetoolkit-guides/econometrics.json" label="Correlation matrix of the weekly returns of the eleven stocks" %}

Apart from `XOM`, every pair correlates between about 0.25 and 0.75. Apple's own correlation with `TSM` is 0.51, not far below its 0.61 with `QCOM` and 0.66 with `SWKS`, but `TSM` is in turn correlated at 0.57 with both of them, so once they are in the regression there is little left for `TSM` to explain. `MSFT` correlates at 0.73 with both Apple and `GOOGL`, the strongest pairs in the matrix.

### Can the P-Values Be Trusted?

The t-tests of OLS assume well-behaved residuals, and returns that are far from normal would undermine them. The Jarque-Bera test combines skewness and excess kurtosis into one statistic, with normality as the null hypothesis. To run it on the quarterly returns of Apple and its three chip suppliers:

```python
jarque_bera = companies.econometrics.get_jarque_bera_test(
    period="quarterly", within_period=False
)

jarque_bera[["AAPL", "SWKS", "QCOM", "TSM"]]
```

Which gives the following:

|                       |   AAPL |   SWKS |   QCOM |    TSM |
|:----------------------|-------:|-------:|-------:|-------:|
| Jarque-Bera Statistic | 0.4592 | 1.3654 | 1.5212 | 0.7283 |
| P-Value               | 0.7949 | 0.5052 | 0.4674 | 0.6948 |

None of the four comes close to rejecting normality, with every p-value well above 0.05, so there is no red flag for the significance calls above. Keep in mind that four years of quarterly returns is a small sample, which makes the test lenient; on daily returns, normality is almost always rejected.

### Is the Relationship Predictive?

`SWKS` has one of the strongest coefficients, but that only shows the two stocks moved together in the same week. Granger causality asks whether the past values of one ticker help predict the other beyond its own history, which would point to a lead-lag relationship. `get_granger_causality` tests every ordered pair of tickers in one go. To run it and select the Apple and Skyworks pairs:

```python
granger_causality = companies.econometrics.get_granger_causality(period="weekly")

granger_causality.loc[[("AAPL", "SWKS"), ("SWKS", "AAPL")]]
```

Which gives the following:

| Dependent | Independent |   F-Statistic |   P-Value | Granger-Causes (5%) |
|:----------|:------------|--------------:|----------:|:--------------------|
| AAPL      | SWKS        |        0.9018 |    0.4810 | False               |
| SWKS      | AAPL        |        1.2622 |    0.2820 | False               |

Neither direction is significant: the relationship between Skyworks and Apple is contemporaneous, the two move together in the same week, and neither helps forecast the other.

The same result holds every ticker against Apple. The p-value of each test with Apple as the dependent variable, with the dashed line at 0.05:

{% include ft-chart.html id="econometrics-granger" src="/assets/data/financetoolkit-guides/econometrics.json" label="Granger causality p-values of each ticker for Apple's weekly returns" %}

Only `AMZN` falls below the line, with a p-value of 0.006, so Amazon's past weekly returns carried some information about Apple's next ones over this window. With ten tests at the 5% level, one false positive is not unusual, so treat it as a lead to check on another period rather than a trading signal.

### What about the Long Run?

`TSM` is Apple's foundry partner, yet its returns were not significant. Short-run returns and long-run price levels answer different questions, though: two price series can share a long-run equilibrium (cointegration) without any short-run relationship in their returns. Before testing for that, the Augmented Dickey-Fuller (ADF) test checks whether the price levels are non-stationary, which is its null hypothesis and what you would expect of a price. The Engle-Granger test then checks every ordered pair for cointegration. To look at the two prices first, and then run both tests on quarterly prices:

```python
prices = companies.get_historical_data(period="weekly")["Adj Close"][["AAPL", "TSM"]]

adf = companies.econometrics.get_augmented_dickey_fuller(period="quarterly")

print(adf[["AAPL", "TSM"]])

cointegration = companies.econometrics.get_engle_granger_cointegration(period="quarterly")

print(cointegration.loc[[("AAPL", "TSM"), ("TSM", "AAPL")]])
```

The weekly prices of the two, each on its own axis, Apple on the left and TSMC on the right:

{% include ft-chart.html id="econometrics-prices" src="/assets/data/financetoolkit-guides/econometrics.json" label="Weekly adjusted close of Apple and TSMC" %}

The two rose together until the turn of 2022, Apple from $35 to a high of $175 and TSMC from $31 to $132, but TSMC then fell by more than half at its low and ended 2022 down 46% from its high, while Apple gave up about a quarter. Neither price shows a level it is pulled back to, which is what the tests check formally.

Which gives the following ADF results:

|                       |    AAPL |     TSM |
|:----------------------|--------:|--------:|
| ADF Statistic         | -1.5128 | -4.0395 |
| P-Value               |  0.5272 |  0.0012 |
| Lags Used             |       0 |       4 |
| Observations          |      15 |      11 |
| Critical Value 5%     | -3.0849 | -3.1894 |
| Reject Unit Root (5%) |   False |    True |

And the following Engle-Granger results:

| Dependent | Independent |   P-Value | Cointegrated (5%) |
|:----------|:------------|----------:|:------------------|
| AAPL      | TSM         |    0.9859 | False             |
| TSM       | AAPL        |    0.9859 | False             |

Apple's price does not reject the unit root, as expected of a price level. `TSM` does reject it at the 5% level, but with only 11 usable observations that is a result to treat with caution rather than at face value. Either way, the Engle-Granger test finds no cointegration between the two: over this window, even Apple's own foundry shows no detectable long-run price equilibrium with Apple, at least not with this few observations. Monthly or weekly prices give the tests far more observations to work with.

### Does the Whole Panel Share a Common Factor?

Rather than one pair at a time, `get_fixed_effects` treats every remaining ticker as an entity in a panel and estimates one common sensitivity to `SWKS`, after removing each entity's own time-invariant average return (its entity effect). To fit the panel on weekly returns:

```python
fixed_effects = companies.econometrics.get_fixed_effects(
    independent_tickers="SWKS",
    dependent_tickers=["TSM", "QCOM", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "XOM", "PG"],
    period="weekly",
)

fixed_effects
```

Which gives a coefficient on `SWKS` of 0.47, with a standard error of 0.02 and a t-statistic above 24, and the following entity effects, the average weekly return that belongs to each stock itself:

{% include ft-chart.html id="econometrics-entity-effects" src="/assets/data/financetoolkit-guides/econometrics.json" label="Entity effects of the fixed effects panel regression" %}

Nvidia stands out with 0.75% a week on top of what `SWKS` explains, about twice `QCOM`, `TSM` and `MSFT` at 0.34% to 0.38%, while Amazon and Meta are slightly negative. The whole panel shares a highly significant sensitivity to `SWKS`, including `XOM` and `PG`, the two names picked for being unrelated. That is the giveaway: with the benchmark excluded, the return of `SWKS` stands in for market-wide comovement rather than a genuine semiconductor supply chain effect. A cleaner test adds the market factor explicitly, for example with `include_benchmark=True` in `get_ols`, and checks what is left.

### Using the Models with Your Own Data

Every method is also available as a plain function in `financetoolkit.econometrics`, which works on any pandas Series or DataFrame, for example a factor you constructed yourself. To regress a simulated asset return on a simulated factor and test the asset return for normality:

```python
import numpy as np
import pandas as pd

from financetoolkit.econometrics import diagnostics_model, regression_model

np.random.seed(42)

factor = pd.Series(np.random.normal(0, 1, 100), name="Factor")
asset_return = 2.5 * factor + pd.Series(np.random.normal(0, 0.5, 100))
asset_return.name = "Asset Return"

result = regression_model.get_ols(asset_return, factor)

print(regression_model.regression_summary_table(result))

print(diagnostics_model.get_jarque_bera_test(asset_return))
```

Which recovers the true slope of 2.5 closely, with an estimate of 2.43 (standard error 0.05, p-value close to zero) and an intercept that is not significant (p-value 0.94). The Jarque-Bera test gives a statistic of 0.09 and a p-value of 0.95, so the normally distributed simulated returns pass as normal.

The module holds 48 methods, including [KPSS](/projects/financetoolkit/docs/econometrics#get_kpss_test), [Phillips-Perron](/projects/financetoolkit/docs/econometrics#get_phillips_perron_test) and [Zivot-Andrews](/projects/financetoolkit/docs/econometrics#get_zivot_andrews_test) unit root tests, [Johansen cointegration](/projects/financetoolkit/docs/econometrics#get_johansen_cointegration), [random effects](/projects/financetoolkit/docs/econometrics#get_random_effects) and the [Hausman test](/projects/financetoolkit/docs/econometrics#get_hausman_test), causal inference with [Difference-in-Differences](/projects/financetoolkit/docs/econometrics#get_difference_in_differences) and [Synthetic Control](/projects/financetoolkit/docs/econometrics#get_synthetic_control), forecasting with [ARIMA](/projects/financetoolkit/docs/econometrics#get_arima_forecast) and [VAR](/projects/financetoolkit/docs/econometrics#get_var_forecast), and [event studies](/projects/financetoolkit/docs/econometrics#get_event_study).

{% include ft-charts-script.html %}
