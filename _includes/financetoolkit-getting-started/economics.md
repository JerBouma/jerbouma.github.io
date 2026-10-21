## Getting Started

The Economics module puts the macro backdrop next to the company data: GDP, inflation, consumer and business confidence, interest rates, house prices, unemployment and dozens of other indicators for 60+ countries, each returned as a DataFrame with one column per country. It is the place to start when you want to know whether a slowdown is local or global, how far real rates have moved, or which housing markets ran ahead of the rest.

Every function needs no API key and follows the same pattern, so once you know one indicator you know them all. This section uses data from 2015 onwards.

### Loading the Module

The Economics module can be imported on its own, or reached through `companies.economics` after you initialise a `Toolkit`. Here it is imported directly. To set it up with data from 2015 onwards:

```python
from financetoolkit import Economics

economics = Economics(start_date="2015-01-01")
```

Nothing is downloaded until you call a function, and each indicator is collected for every country it covers, so selecting countries afterwards is a plain column selection.

### Gross Domestic Product and Inflation

The two most fundamental macro indicators are Gross Domestic Product (GDP) and the inflation rate. With `inflation_adjusted=True` the GDP is in constant prices, so it shows real growth rather than growth flattered by inflation. Each country reports in its own currency, which makes the levels impossible to compare directly; dividing by the first year turns them into an index where 2015 is 100. To get real GDP for the four largest economies and rebase it:

```python
gdp = economics.get_gross_domestic_product(inflation_adjusted=True)

gdp_index = gdp.loc[:, ["United States", "China", "Germany", "Japan"]]
gdp_index = gdp_index / gdp_index.iloc[0] * 100
```

When plotted, with the Covid year marked:

{% include ft-chart.html id="economics-gdp" src="/assets/data/financetoolkit-guides/economics.json" label="Real GDP of the United States, China, Germany and Japan, 2015 = 100" %}

China's real output is 72% higher than in 2015 and the United States' 27%, while Germany and Japan grew only 8% and 5% in ten years. Covid cost every economy except China a year of growth in 2020, and Germany has hardly grown since 2022.

The inflation rate is returned as a decimal fraction (0.03 is 3%), like every rate in the Finance Toolkit. To get it for four countries with very different inflation histories:

```python
inflation = economics.get_inflation_rate()

inflation.loc[:, ["United States", "United Kingdom", "Brazil", "Turkey"]]
```

Which gives the annual inflation rate per country, here with the 2021-2023 inflation shock shaded:

{% include ft-chart.html id="economics-inflation" src="/assets/data/financetoolkit-guides/economics.json" label="Inflation rate of the United States, United Kingdom, Brazil and Turkey" %}

Turkey's inflation is in a different league: 72% in 2022 and still above 50% in 2023 and 2024, where the other three peaked at 8% to 9% in 2022. The second tab leaves Turkey out, which shows that Brazil, with inflation of 9% in 2015, came into the shock from a much higher level than the United States and the United Kingdom.

### Smoothing with Rolling and Trailing Windows

Most functions in the Economics module accept `rolling` and `trailing`. `rolling=<n>` applies a simple moving average over `n` periods, which takes the noise out of a volatile series, and `trailing=<n>` sums over the last `n` periods, for example to turn a quarterly flow into a trailing annual figure. Inflation is annual by default, so a rolling window of 3 gives a three-year average. To calculate it:

```python
smoothed_inflation = economics.get_inflation_rate(rolling=3)

smoothed_inflation.loc[:, ["United States", "United Kingdom", "Brazil", "Turkey"]]
```

Set against the annual rates from before for the United States and the United Kingdom, the dashed lines being the annual rates:

{% include ft-chart.html id="economics-inflation-rolling" src="/assets/data/financetoolkit-guides/economics.json" label="Annual and three-year rolling average inflation rate for the United States and the United Kingdom" %}

The rolling average turns the sharp 2022 peaks of 8.0% and 9.1% into a broader hump that tops out a year later, at 5.6% for the United States and 6.3% for the United Kingdom, and is back at 3.3% and 4.4% in 2025. It lags the turn, which is the price of the smoother line.

The same parameters work next to `growth=True` and `standardize=True`, the latter converting a series into standard deviations from its own mean so that indicators on different scales can be compared.

### Consumer Confidence

Confidence indicators are survey-based and move ahead of the hard data, which makes them useful for spotting a turn in consumer spending before it shows up in retail sales or GDP. The Consumer Confidence Index (CCI) is set so that its long-term average is 100: a reading below 100 means households are more pessimistic than usual about their finances and the economy. To get the monthly index and select four countries:

```python
cci = economics.get_consumer_confidence_index()

cci.loc[:, ["United States", "China", "Spain", "Germany"]]
```

Which gives the index per month, shown here with the long-term average of 100 as a dashed line and the two shocks shaded:

{% include ft-chart.html id="economics-cci" src="/assets/data/financetoolkit-guides/economics.json" label="Consumer Confidence Index for the United States, China, Spain and Germany" %}

Confidence broke twice: in the 2020 lockdowns, when Spain's index fell from above 100 to below 96 within months, and in 2022, when inflation hit household budgets and Spain and Germany reached their lowest readings of the period. Europe has since recovered to just below the average, while China's index never came back after its 2022 collapse and confidence in the United States, at 96.1, is near its lowest point since 2015.

The Business Confidence Index (`get_business_confidence_index`) and the Composite Leading Indicator (`get_composite_leading_indicator`) work the same way.

### Interest Rates

The long-term interest rate is the yield on 10-year government bonds, the short-term rate the 3-month interbank or treasury rate. Together they give the slope of the yield curve, and the short rate tracks the policy rate of the central bank closely. Both accept `period` to choose monthly, quarterly or annual data. To get both on a quarterly basis:

```python
countries = ["United States", "United Kingdom", "Germany", "Canada", "Japan"]

long_term_interest_rates = economics.get_long_term_interest_rate(period="quarterly")
short_term_interest_rates = economics.get_short_term_interest_rate(period="quarterly")

long_term_interest_rates.loc[:, countries]
short_term_interest_rates.loc[:, countries]
```

Putting the two rates of each country side by side shows the yield curve at work. The shaded periods are where the 3-month rate rose above the 10-year yield, an inverted curve:

{% include ft-chart.html id="economics-rates" src="/assets/data/financetoolkit-guides/economics.json" label="10-year yield and 3-month rate per country, with the periods of an inverted yield curve shaded" %}

Short rates went from around zero (below zero in Germany) to more than 5% in the United States and the United Kingdom in 2023, and overtook the 10-year yield by as much as 1.5 percentage points. The curve stayed inverted for about two years, from late 2022 to the end of 2024 in the United States and Canada and from 2023 into 2024 and early 2025 in the United Kingdom and Germany, and has since turned upward again. Japan is the exception: its short rate stayed near zero until 2024, so its curve never inverted in any meaningful way.

### House Prices

House prices reflect both the economic situation of a country and its policies, from interest rates to building permits and tax rules. The house price index is set to 100 in 2015 for every country, so the values show the cumulative change since then. To get the index for all countries, rank a selection of large housing markets by their latest value and follow five of them over time:

```python
house_prices = economics.get_house_prices()

major_markets = [
    "United States", "Canada", "Mexico", "Brazil", "United Kingdom", "Ireland",
    "Netherlands", "Spain", "Portugal", "Germany", "France", "Italy", "Sweden",
    "Japan", "South Korea", "China", "India", "Australia",
]

house_prices.iloc[-1][major_markets].sort_values(ascending=False)
house_prices[["Australia", "United States", "United Kingdom", "Spain", "Brazil"]]
```

Which gives the ranking for 2025, with the United States highlighted, and the path of the five markets in the second tab:

{% include ft-chart.html id="economics-house-prices" src="/assets/data/financetoolkit-guides/economics.json" label="House price index for 18 large housing markets in 2025, and over time for five of them" %}

Portugal's house prices nearly tripled since 2015 (an index of 275), and Mexico, the Netherlands, Ireland, Spain and the United States all rose by more than 80%. At the other end, prices in Italy are up 18% and in China only 6%, which in real terms is a decline. Over time, the United States pulled ahead during the pandemic, and Spain, after a steadier climb, rose fast enough in 2024 and 2025 to draw level with it.

The index is nominal, so high inflation shows up in it directly: Turkey's index went from 100 in 2015 to more than 2,000, which is why it is not among the selection.

### Calling the Data Models Directly

The Economics class is a thin layer over the models that collect the data, so you can also call those models yourself. That is useful when you want the full history rather than the window set by `start_date`, as the models return everything the source has. To get the quarterly unemployment rate for all countries straight from the OECD model:

```python
from financetoolkit.economics import oecd_model

unemployment_rate = oecd_model.get_unemployment_rate(period="quarterly")

unemployment_rate.loc["1990":, ["United States", "Germany", "Japan", "Spain", "Canada"]]
```

Which gives 36 years of quarterly data, here with the financial crisis, the euro crisis and Covid shaded:

{% include ft-chart.html id="economics-unemployment" src="/assets/data/financetoolkit-guides/economics.json" label="Quarterly unemployment rate for the United States, Germany, Japan, Spain and Canada since 1990" %}

Labour markets respond very differently to the same shocks. Spain's unemployment rose from 8% before the financial crisis to a peak of 26.3% in early 2013, at the height of the euro crisis, and is still above 10%. The United States and Canada saw a short spike to 13% in 2020 that was gone within two years, Germany brought its rate down from 11% in 2005 to below 4%, and Japan's never went above 5.4%.

The series goes back to 1955 for some countries; the selection above starts in 1990 to keep the comparison readable.

{% include ft-charts-script.html %}
