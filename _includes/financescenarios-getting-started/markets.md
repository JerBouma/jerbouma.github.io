## Getting Started

The Markets module simulates equities, currencies, commodities, house prices, dividends and credit. In the default factor set each stock market switches between calm and turbulent regimes and earns the simulated short rate plus a long-run premium, the euro and the pound revert to purchasing power parity, gold has no trend of its own in real terms, oil swings around a level, and house prices slow after the long rate rises.

This section uses the run from the [overview](/projects/financescenarios/docs): the default settings and factor set, calibrated on 19 October 2026, with 2,000 scenarios and seed 42.

### Stock Markets

The default factor set holds five stock markets, each fitted to one fund: US stocks (SPY), US small caps, Europe, Japan and emerging markets. To simulate them:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)
result = scenarios.simulate(n_simulations=2000, seed=42)

result.describe()
```

Which gives, for the stock markets, the annualized return from today to the end of the run:

| factor | terminal_mean | terminal_q05 | terminal_q95 |
|:-------|--------------:|-------------:|-------------:|
| us_broad | 0.0849 | -0.0569 | 0.2082 |
| small_cap | 0.0935 | -0.0767 | 0.2657 |
| europe | 0.0933 | -0.0753 | 0.2487 |
| japan | 0.0947 | -0.0511 | 0.2393 |
| emerging_markets | 0.0934 | -0.0990 | 0.2725 |

Every market returns between 8.49% and 9.47% a year on average, and they differ mostly in their spread: one emerging-market scenario in twenty loses more than 9.90% a year, against 5.69% for US stocks. When plotted, the 5th percentile, median and 95th percentile per market:

{% include ft-chart.html id="markets-equity-returns" src="/assets/data/financescenarios-guides/markets.json" label="5th percentile, median and 95th percentile of the five-year annualized return of US stocks, US small caps, European, Japanese and emerging-market stocks" %}

The fitted parameters show the two regimes. To read them for US stocks:

```python
calibration = scenarios.calibrate()

calibration.calibrated_params["us_broad"]
```

Which shows a calm regime with a yearly return of 9.31% and a volatility of 9.9%, and a turbulent regime with -17.24% and 21.6%. In the long run the market is turbulent 21% of the time, and a turbulent month is followed by another with a chance of 84%, so bad months cluster. The regimes are timed on decades of the market's own index and scaled to the fund; How It Works below derives each number.

`metric_paths` returns a variable's paths as an array, here the price of each fund with `levels=True`. To follow 100 invested in three of the markets:

```python
def growth_of_100(factor):
    prices = result.metric_paths(factor, levels=True)
    return 100 * prices / prices[:, :1]

index = {name: growth_of_100(factor) for name, factor in
         {"US": "us_broad", "Europe": "europe", "Emerging markets": "emerging_markets"}.items()}
```

When plotted, the median and 5-95% band of each:

{% include ft-chart.html id="markets-equity-index" src="/assets/data/financescenarios-guides/markets.json" label="Median and 5-95% band of the value of 100 invested in US, European and emerging-market stocks over five years" %}

The same arrays give the deepest fall from a peak that each scenario goes through, the drawdown an investor has to sit out on the way. To compute it per market:

```python
import numpy as np

markets = {"US": "us_broad", "US small caps": "small_cap", "Europe": "europe", "Japan": "japan",
           "Emerging markets": "emerging_markets"}

for name, factor in markets.items():
    level = growth_of_100(factor)
    worst = (level / np.maximum.accumulate(level, axis=1) - 1).min(axis=1)
    print(name, np.quantile(worst, [0.05, 0.5, 0.95]))
```

The median US scenario falls 19.5% from a peak at some point within five years and one in twenty falls 47.2% or more, against 27.1% and 60.7% for emerging markets. When plotted:

{% include ft-chart.html id="markets-drawdown" src="/assets/data/financescenarios-guides/markets.json" label="Worst 5%, median and best 5% of the deepest fall from a peak within five years, per stock market" %}

### Currencies

Each currency is simulated against the US dollar, as the amount of it one dollar buys. The euro and the pound revert to purchasing power parity with a half-life of four years; the yen has no trend. To read the euro's parameters:

```python
calibration.calibrated_params["eur"]
```

Which gives a speed of 0.173 a year (ln 2 over four years), a volatility of 9.3% a year and a distance of 0.105 in log terms between today's real exchange rate and its average since 2000 (`long_run_deviation`): in real terms the dollar buys about 11% more euros than usual. A dollar buys 0.8807 euros, 0.7526 pounds and 157.0 yen at the start; after five years the median scenario has it buying 0.8145 euros and 0.7040 pounds, as the dollar loses part of that edge, and still 156.8 yen. When plotted with `levels=True`, one currency per tab:

{% include ft-chart.html id="markets-fx" src="/assets/data/financescenarios-guides/markets.json" label="Median, 25-75% and 5-95% band of the number of euros, pounds and yen one US dollar buys over five years" %}

### Gold and Oil

Gold follows a random walk with a small real drift and oil a mean-reverting log price. To read both:

```python
calibration.calibrated_params["gold"]

calibration.calibrated_params["crude_oil"]
```

Which gives gold a drift of 1.6% a year and a volatility of 17.9%, from $4,182.60 an ounce, and oil a long-run level of $76.98 a barrel (a log level of 4.343), a speed of 0.46 a year and a volatility of 38.3%, from $108.44. After five years the median gold price is $4,778.65, with a 90% range of $2,470.89 to $9,231.47, and the median oil price is $79.31, between $42.30 and $156.28. When plotted:

{% include ft-chart.html id="markets-commodities" src="/assets/data/financescenarios-guides/markets.json" label="Median, 25-75% and 5-95% band of the gold price in dollars an ounce and the crude oil price in dollars a barrel over five years" %}

### House Prices

US house-price growth reverts to its long-run level and slows when the long rate has risen a year earlier. To read its parameters and its range after one, three and five years:

```python
calibration.calibrated_params["real_estate"]

result.horizon_summary([1, 3, 5], factors=["real_estate"])
```

Which gives a long-run growth of 4.29% a year, a speed of 0.37 and a sensitivity of -0.86 to the long rate's change a year earlier: a rise of one point in the 10-year rate takes 0.86 points off house-price growth a year later. Growth starts at 2.14%; its median rises to 2.83% after one year and 3.93% after five, with one scenario in twenty below -4.93%. When plotted:

{% include ft-chart.html id="markets-real-estate" src="/assets/data/financescenarios-guides/markets.json" label="Median, 25-75% and 5-95% band of US house-price growth over five years" %}

### How the Markets Move Together

Besides the direct links, such as stocks earning the short rate and currencies following inflation, all variables are tied together by one correlation matrix of their historical shocks. `correlation_frame` returns it as a table, one row and one column per variable. To get it:

```python
calibration.correlation_frame()
```

US and European stocks have a correlation of 0.72, oil moves with stocks (0.32 in the US, 0.35 in Europe) and with US inflation (0.26), and European stocks move against the euro (-0.54): the euro is measured here as euros per dollar, so European stocks tend to fall when the dollar strengthens. When plotted, nine of the 27 variables:

{% include ft-chart.html id="markets-correlation" src="/assets/data/financescenarios-guides/markets.json" label="Correlations of the fitted shocks of US inflation, the US short and 10-year rates, US unemployment, US and European stocks, the euro, gold and crude oil" %}

### Wider Coverage

The `broad` factor set adds what the default leaves out: Japan, Canada, Australia and India, US sectors and styles, more countries' stock markets, silver, copper and natural gas, five more currencies and SPY's dividend yield. Credit spreads by rating come from the ICE BofA indices and need the FRED key. To see what it holds without calibrating it:

```python
from financescenarios import load_profiles

load_profiles(settings_id="default", factor_set_id="broad").describe()
```

Which lists 68 variables against the default's 27, among them 23 stock markets, 14 interest rates, 8 currencies and 5 commodities. Dividend yield and growth, credit spreads, the credit curve and rating migration each have their own section in How It Works below.

{% include ft-charts-script.html %}
