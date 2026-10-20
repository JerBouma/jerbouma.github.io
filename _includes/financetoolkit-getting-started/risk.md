## Getting Started

The Risk module answers the question that comes before any return figure: what could go wrong, and how badly? It calculates Value at Risk (VaR), Conditional Value at Risk (CVaR), drawdown measures, the Ulcer Index, EWMA and GARCH volatility, the Hurst Exponent and more, for every ticker you load and for the benchmark next to them. Every metric works on the same historical data, so you can look at it per week, month, quarter or year without preparing anything yourself.

This section uses Microsoft, Apple, Amazon and Meta from 2013 onwards, with the S&P 500 as the benchmark.

### Loading the Data

The Risk module is part of the `Toolkit` class, so the only setup is choosing the tickers and the start date. To load the data for the four companies:

```python
from financetoolkit import Toolkit

companies = Toolkit(
    ["MSFT", "AAPL", "AMZN", "META"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2013-01-01",
)
```

The historical prices and the treasury rates are collected the first time you call a risk function and reused for every call after that.

### Value at Risk and Conditional Value at Risk

Value at Risk is the loss that is not exceeded with a given probability: with the default `alpha=0.05`, a monthly VaR of -8% means that in 95% of months the return was better than -8%. Conditional Value at Risk (also called Expected Shortfall) is the average loss in the months that were worse than the VaR. VaR tells you where the tail starts, CVaR tells you how heavy it is, which is why risk managers and regulators increasingly prefer the latter.

The `period` parameter sets the return frequency. Without anything else, you get one figure per ticker for the whole sample, based on its monthly returns. To calculate both for monthly returns since 2013:

```python
value_at_risk = companies.risk.get_value_at_risk(period="monthly")

conditional_value_at_risk = companies.risk.get_conditional_value_at_risk(period="monthly")
```

Which gives one VaR and one CVaR per ticker, side by side:

{% include ft-chart.html id="risk-var-sample" src="/assets/data/financetoolkit-guides/risk.json" label="Monthly VaR and CVaR at 95% of Microsoft, Apple, Amazon, Meta and the S&P 500 since 2013" %}

Meta is the riskiest of the four on both measures. Its VaR of -11.9% is close to that of Apple and Amazon, but its CVaR of -17.9% is far deeper: when Meta has a bad month, it tends to be very bad. The S&P 500, as a diversified index, has the mildest tail at -6.0% and -8.3%, and Microsoft comes closest to it among the four.

With `within_period=True` the module instead calculates the metric for each period from the daily returns within it, so you see how the daily tail risk changed from quarter to quarter. Adding `rolling=12` turns the monthly VaR into a rolling twelve-month window, which is the worst stretch of the past year rather than of a single month. To calculate all three:

```python
quarterly_var = companies.risk.get_value_at_risk(period="quarterly", within_period=True)

quarterly_cvar = companies.risk.get_conditional_value_at_risk(period="quarterly", within_period=True)

rolling_var = companies.risk.get_value_at_risk(period="monthly", rolling=12)
```

Which gives the daily VaR and CVaR of each company against the VaR of the S&P 500, with the last tab showing the rolling twelve-month VaR:

{% include ft-chart.html id="risk-var" src="/assets/data/financetoolkit-guides/risk.json" label="Quarterly VaR and CVaR of daily returns per company against the S&P 500, and the rolling 12-month VaR" %}

In the first quarter of 2020 the daily VaR of Microsoft, Apple and the S&P 500 reached -5% to -6.7%, against a usual -1% to -3%, and the CVaR of Microsoft hit -9.5%. Meta's worst quarters came in 2022 instead, with a CVaR of -10.5% in the first quarter and -10.8% in the last. The rolling view shows the same year from a monthly angle: with Meta's 31% fall in October 2022 inside the window, its rolling VaR dropped to -31.9%.

VaR also accepts `distribution="gaussian"`, `"studentt"`, `"cornish-fisher"` or `"evt"` (a Peak-over-Threshold fit for the tail) when you'd rather not rely on the historical distribution alone.

### The Ulcer Index and Growth

The Ulcer Index measures the depth and duration of declines from the most recent high, so it only punishes downside volatility. Each function accepts `growth=True` (and a `lag`) to show the change over time instead of the level, which makes it easy to see in which years the stress rose. To calculate the year-on-year change in the Ulcer Index:

```python
companies.risk.get_ulcer_index(period="yearly", growth=True)
```

Which gives one cell per ticker and year, pink where stress rose and blue where it fell:

{% include ft-chart.html id="risk-ulcer" src="/assets/data/financetoolkit-guides/risk.json" label="Year-on-year change in the Ulcer Index" %}

The stress came in waves. The Ulcer Index of every ticker rose sharply in 2018, 2020 and 2022, with the S&P 500 up 449% in 2018 and 266% in 2022, and fell back in 2019, 2021 and 2023 as prices recovered.

### Conditional Drawdown at Risk and the Tail Ratio

VaR and CVaR look at returns one period at a time. The Conditional Drawdown at Risk (CDaR) applies the same idea to the drawdown series: rather than asking how bad one period could be, it asks how deep the cumulative peak-to-trough loss could get. That is the measure that matters to an investor who holds through a bad stretch. The Tail Ratio compares the size of the best-case tail of returns (the 95th percentile) to the worst-case tail (the 5th percentile); above 1 means the gains outsize the losses.

To calculate the quarterly CDaR and the yearly Tail Ratio:

```python
conditional_drawdown_at_risk = companies.risk.get_conditional_drawdown_at_risk(
    period="quarterly", within_period=True
)

tail_ratio = companies.risk.get_tail_ratio(period="yearly", within_period=True)
```

Which gives the following CDaR for Meta, Microsoft and the S&P 500:

{% include ft-chart.html id="risk-cdar" src="/assets/data/financetoolkit-guides/risk.json" label="Quarterly Conditional Drawdown at Risk of Meta, Microsoft and the S&P 500" %}

Two quarters stand out. In the Covid crash the CDaR of the S&P 500 reached -31%, with Microsoft at -27%, while Meta's deepest reading came in the first quarter of 2022 at -44.5%, when the stock fell by more than a quarter in a single day after its results.

The Tail Ratio per ticker and year, grey near 1 where the best and worst tails are the same size and pink where the worst tail is the heavier one:

{% include ft-chart.html id="risk-tail" src="/assets/data/financetoolkit-guides/risk.json" label="Yearly Tail Ratio of Microsoft, Apple, Amazon, Meta and the S&P 500" %}

In 2022 the Tail Ratio of every ticker dropped below 1, between 0.84 and 0.95, so the bad days outsized the good ones; in 2023 every ticker rose above 1 again.

### Drawdown Duration and Recovery Time

The size of a drawdown is only half the story; how long it lasts matters just as much to anyone who has to explain it. The Maximum Drawdown Duration is the number of trading days the worst decline in each period took, from the peak to the trough. The Maximum Drawdown Recovery Time is the number of trading days it then took to get back to the previous high, and is empty when the price had not recovered by the end of the period. To calculate both per year:

```python
drawdown_duration = companies.risk.get_maximum_drawdown_duration(
    period="yearly", within_period=True
)

recovery_time = companies.risk.get_maximum_drawdown_recovery_time(
    period="yearly", within_period=True
)
```

Which gives the following, with the tabs switching between the duration and the recovery time:

{% include ft-chart.html id="risk-drawdown-duration" src="/assets/data/financetoolkit-guides/risk.json" label="Maximum drawdown duration and recovery time per year in trading days" %}

In most years the worst decline was over within 100 trading days. 2022 is the exception: it lasted 195 to 248 trading days for every ticker, close to the whole year, and none of them had recovered by year-end, which is why 2022 (like 2018, when the decline came in the last quarter) is empty in the recovery tab.

### EWMA Volatility and the Hurst Exponent

The EWMA volatility follows the RiskMetrics methodology: it weights recent returns more heavily than older ones (with a decay factor `lambda_` of 0.94 by default), so it reacts to a change in the volatility regime much faster than a fixed rolling window. The Hurst Exponent says something about the character of a return series: below 0.5 it tends to mean-revert, around 0.5 it behaves like a random walk and above 0.5 it tends to trend.

To calculate the daily EWMA volatility and the Hurst Exponent of each ticker:

```python
ewma_volatility = companies.risk.get_ewma_volatility()

hurst_exponent = companies.risk.get_hurst_exponent()
```

Which gives the EWMA volatility of each company against that of the S&P 500, shown at the end of each week:

{% include ft-chart.html id="risk-ewma" src="/assets/data/financetoolkit-guides/risk.json" label="EWMA volatility of Microsoft, Apple, Amazon and Meta against the S&P 500" %}

Volatility comes in bursts that fade within a few months. In March 2020 the daily volatility of Microsoft reached 6.5%, Apple 6.0% and the S&P 500 5.1%, and each company stays above the index for most of the period, with Meta the most volatile today at 2.8% a day against 0.6% for the S&P 500.

The Hurst Exponent is one number per ticker, and for these five it ends up between about 0.46 and 0.49, just under 0.5. Daily returns of large, liquid stocks behave close to a random walk, with at most a slight tendency to mean-revert.

### Returns against the Maximum Drawdown

Putting the returns next to the drawdowns shows how much pain came with the gains. To get the weekly returns and the maximum drawdown in each quarter:

```python
weekly_returns = companies.get_historical_data(period="weekly")["Return"]

maximum_drawdown = companies.risk.get_maximum_drawdown(period="quarterly", within_period=True)
```

The weekly returns of Meta, counted in bins of one percentage point, with the worst week and the 5% quantiles of Meta and the S&P 500 marked:

{% include ft-chart.html id="risk-returns" src="/assets/data/financetoolkit-guides/risk.json" label="Distribution of the weekly returns of Meta" %}

Three quarters of Meta's weeks stay within ±5%, but the left tail runs far out: one week in twenty lost more than 6.9%, against 3.0% for the S&P 500, and the worst week, at the end of October 2022, lost 23.7%.

Each ticker's worst quarterly drawdown against its compounded annual return over the whole period, with the S&P 500 in orange:

{% include ft-chart.html id="risk-max-drawdown" src="/assets/data/financetoolkit-guides/risk.json" label="Worst quarterly drawdown against the annual return" %}

The four companies returned about 24% to 26% a year, against 15% for the S&P 500, but the pain that came with it differs widely. Meta's worst quarter, early 2022, came with a drawdown of 45%, while Microsoft earned the same return with a worst quarter of -28%, shallower even than the S&P 500's -34% in the first quarter of 2020.

### Using the Risk Models with Your Own Data

Every metric in the module is a plain function underneath, which you can call on any pandas Series or DataFrame of returns. That is useful for a fund's own return history, a backtest or simulated returns that don't come from a ticker. The models live in `financetoolkit.risk`. To calculate a set of statistics for four series of random returns:

```python
import random

import pandas as pd

from financetoolkit.risk import evar_model, risk_model, var_model

return_statistics = {}

for seed, stock_name in enumerate(["Stock A", "Stock B", "Stock C", "Stock D"], start=1):
    random.seed(seed)
    returns = pd.Series([random.randint(-15, 15) / 100 for _ in range(100)])

    return_statistics[stock_name] = {
        "Standard Deviation": returns.std(),
        "Skewness": risk_model.get_skewness(returns=returns),
        "Kurtosis": risk_model.get_kurtosis(returns=returns),
        "Max Drawdown": risk_model.get_max_drawdown(returns=returns),
        "Value at Risk": var_model.get_var_historic(returns=returns, alpha=0.05),
        "Entropic Value at Risk": evar_model.get_evar_gaussian(returns=returns, alpha=0.05),
    }

pd.DataFrame(return_statistics).round(4)
```

Which returns the statistics per series, with a negative (excess) kurtosis as you would expect from uniformly distributed returns, and the Entropic VaR as the most conservative of the tail measures:

|                    |   Stock A |   Stock B |   Stock C |   Stock D |
|:-------------------|----------:|----------:|----------:|----------:|
| Standard Deviation |    0.0934 |    0.0889 |    0.0865 |    0.0938 |
| Skewness           |   -0.1721 |   -0.0527 |   -0.1820 |    0.1677 |
| Kurtosis           |   -1.1688 |   -1.1309 |   -1.0048 |   -1.3330 |
| Max Drawdown       |   -0.5058 |   -0.6082 |   -0.4528 |   -0.6631 |
| Value at Risk      |   -0.1500 |   -0.1305 |   -0.1305 |   -0.1400 |
| Entropic Value at Risk |   -0.2176 |   -0.2023 |   -0.1970 |   -0.2311 |

The module covers many more metrics than shown here, among them [GARCH](/projects/financetoolkit/docs/risk#get_garch), [GJR-GARCH](/projects/financetoolkit/docs/risk#get_gjr_garch) and [EGARCH](/projects/financetoolkit/docs/risk#get_egarch) with forecasts, [copulas](/projects/financetoolkit/docs/risk#get_best_fitting_copula), [CoVaR](/projects/financetoolkit/docs/risk#get_covar), [marginal](/projects/financetoolkit/docs/risk#get_marginal_value_at_risk) and [component VaR](/projects/financetoolkit/docs/risk#get_component_value_at_risk) and [VaR backtests](/projects/financetoolkit/docs/risk#get_var_backtest).

{% include ft-charts-script.html %}
