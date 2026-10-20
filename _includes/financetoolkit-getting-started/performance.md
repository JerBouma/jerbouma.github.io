## Getting Started

A return on its own says little. Whether 15% a year is good depends on how much risk was taken to get it and on what the market did in the meantime. The Performance module answers that question with the risk-adjusted measures analysts use every day: Jensen's Alpha, the Capital Asset Pricing Model (CAPM), Beta, the Sharpe, Sortino and Treynor Ratios, the Information Ratio, capture ratios and factor models such as Fama-French. Each stock is compared to the benchmark of the `Toolkit` (the S&P 500 unless you set `benchmark_ticker`) and to the risk-free rate.

This section uses ASML, Microsoft, Apple and Walmart from 2005 onwards.

### Loading the Data

The Performance module is part of the `Toolkit` class. To load the data for the four companies:

```python
from financetoolkit import Toolkit

companies = Toolkit(
    ["ASML", "MSFT", "AAPL", "WMT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2005-01-01",
)
```

The prices of the four stocks, the benchmark and the 10-year treasury rate (the risk-free rate) are collected on the first call and reused afterwards.

### Jensen's Alpha and the Capital Asset Pricing Model

CAPM gives the return you would expect from a stock given its Beta, the market return and the risk-free rate: the risk-free rate plus Beta times the market risk premium. Jensen's Alpha is the difference between the actual return and that expected return. A positive alpha means the stock did better than its market exposure alone explains, a negative alpha means it did worse.

Every function takes a `period` of `weekly`, `monthly`, `quarterly` or `yearly`, and calculates Beta, variances and returns from the daily data within each period. To calculate Jensen's Alpha per quarter and the CAPM expected return per year:

```python
jensens_alpha = companies.performance.get_jensens_alpha(period="quarterly")

capm = companies.performance.get_capital_asset_pricing_model(period="yearly")
```

Which gives the following Jensen's Alpha, where Apple has the highest average alpha of the four at about 5% per quarter, and every stock swings between clearly positive and clearly negative quarters:

{% include ft-chart.html id="performance-alpha" src="/assets/data/financetoolkit-guides/performance.json" label="Jensen's Alpha per quarter of ASML, Microsoft, Apple and Walmart" %}

The CAPM expected return follows the market, scaled by Beta. ASML, with the highest Beta, has the largest expected returns in strong years and the largest expected losses in years such as 2008 and 2022, while Walmart, with a low Beta, stays much closer to zero:

{% include ft-chart.html id="performance-capm" src="/assets/data/financetoolkit-guides/performance.json" label="Expected return per year according to CAPM" %}

### The Sharpe Ratio over Time

The Sharpe Ratio divides the excess return over the risk-free rate by the standard deviation of returns, which puts stocks with different volatility on the same footing. Because each period is calculated from the days within it, `rolling` gives a value that evolves through time instead of one number per period. To calculate the 12-month rolling Sharpe Ratio:

```python
companies.performance.get_sharpe_ratio(period="monthly", rolling=12)
```

Which shows how the risk-adjusted return of each stock moved with the market cycle, dropping below zero in 2008, 2022 and other sell-offs, while Walmart, the defensive name of the four, stayed positive through 2008:

{% include ft-chart.html id="performance-sharpe" src="/assets/data/financetoolkit-guides/performance.json" label="12-month rolling Sharpe Ratio" %}

Set `annualize=True` to scale the ratio to a yearly figure, which is how Sharpe Ratios are usually quoted in fund documents.

### The Sortino and Treynor Ratios

Two variations of the Sharpe Ratio change the risk in the denominator. The Sortino Ratio only counts downside volatility, so a stock is not penalised for large upward moves. The Treynor Ratio uses Beta, the systematic risk, instead of the standard deviation; that is the more relevant measure for a stock held within a diversified portfolio, where the stock-specific risk is diversified away. To calculate both per year:

```python
sortino_ratio = companies.performance.get_sortino_ratio(period="yearly")

treynor_ratio = companies.performance.get_treynor_ratio(period="yearly")
```

Which gives the following, with the tabs switching between the two ratios:

{% include ft-chart.html id="performance-sortino-treynor" src="/assets/data/financetoolkit-guides/performance.json" label="Sortino and Treynor Ratio per year" %}

<div class="fs-callout" markdown="1"><p class="fs-callout__title">When Beta is close to zero</p>

The Treynor Ratio divides by Beta, so it becomes unstable when a stock barely moves with the market. Walmart shows this in some recent years, with values far outside the range of the other three. Check the Beta with `get_beta` before reading much into an extreme Treynor Ratio.
</div>

### Fama-French Factor Exposures

CAPM explains returns with one factor, the market. The Fama-French five-factor model adds four more, each the return of a long-short portfolio:

- **Market Risk Premium (Mkt-RF):** the return of the market over the risk-free rate, comparable to CAPM's Beta but based on the whole US market instead of the benchmark you chose.
- **Size Premium (SMB):** the excess return of small-cap stocks over large-cap stocks.
- **Value Premium (HML):** the excess return of value stocks over growth stocks.
- **Profitability (RMW):** the excess return of highly profitable companies over unprofitable ones.
- **Investment (CMA):** the excess return of companies that invest conservatively over those that invest aggressively.

The model regresses each stock's daily returns on the factors within every period. With `method="simple"` it runs a separate regression per factor, and with the default `method="multi"` one regression on all five at once. To run the simple regressions per year:

```python
fama_and_french = companies.performance.get_fama_and_french_model(
    period="yearly", method="simple"
)
```

The result holds the intercept, slope, R-squared, p-value, standard error and factor value for every ticker, factor and year. The R-squared shows how much of a stock's daily returns each factor explains on its own. To select it for Apple:

```python
fama_and_french["AAPL"].xs("R Squared", level=1, axis=1)
```

Which, for each of the four stocks in the tabs below, shows the market factor doing most of the work, explaining up to about three quarters of Apple's daily returns in 2022, with the other factors adding far less on their own:

{% include ft-chart.html id="performance-fama-french" src="/assets/data/financetoolkit-guides/performance.json" label="R-squared of each Fama-French factor per year" %}

The correlations between the factors themselves, and between the factors and the asset returns, are available through `get_factor_correlations` and `get_factor_asset_correlations`. To calculate the correlations of each stock with the factors per quarter:

```python
companies.performance.get_factor_asset_correlations(period="quarterly")
```

Which shows a strong positive correlation with the market for all four, and for ASML, Apple and Microsoft a negative correlation with the value (HML) and investment (CMA) factors, the signature of growth stocks:

{% include ft-chart.html id="performance-factor-correlations" src="/assets/data/financetoolkit-guides/performance.json" label="Quarterly correlation with the Fama-French factors" %}

### Using the Fama-French Dataset Directly

The functions behind the `Toolkit` can also be used on their own. For example, the daily Fama-French factor returns from [Kenneth French's data library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html), which go back to 1963. To download them:

```python
from financetoolkit.performance import performance_model

factors = performance_model.obtain_fama_and_french_dataset()
```

Which returns the daily factor returns and the risk-free rate as decimal fractions, starting with:

| Date       |   Mkt-RF |     SMB |     HML |     RMW |     CMA |     RF |
|:-----------|---------:|--------:|--------:|--------:|--------:|-------:|
| 1963-07-01 |  -0.0067 |  0.0000 | -0.0033 | -0.0001 |  0.0016 | 0.0001 |
| 1963-07-02 |   0.0079 | -0.0026 |  0.0026 | -0.0007 | -0.0020 | 0.0001 |
| 1963-07-03 |   0.0063 | -0.0017 | -0.0010 |  0.0018 | -0.0034 | 0.0001 |
| 1963-07-05 |   0.0040 |  0.0008 | -0.0027 |  0.0009 | -0.0034 | 0.0001 |
| 1963-07-08 |  -0.0063 |  0.0004 | -0.0018 | -0.0029 |  0.0014 | 0.0001 |

The module covers many more measures, among them the [Information Ratio](/projects/financetoolkit/docs/performance#get_information_ratio), [upside](/projects/financetoolkit/docs/performance#get_upside_capture_ratio) and [downside capture ratios](/projects/financetoolkit/docs/performance#get_downside_capture_ratio), the [Calmar](/projects/financetoolkit/docs/performance#get_calmar_ratio) and [Omega Ratios](/projects/financetoolkit/docs/performance#get_omega_ratio), the [Carhart four-factor model](/projects/financetoolkit/docs/performance#get_carhart_four_factor_model) and market-timing models such as [Treynor-Mazuy](/projects/financetoolkit/docs/performance#get_treynor_mazuy_model).

{% include ft-charts-script.html %}
