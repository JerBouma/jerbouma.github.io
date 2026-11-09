## Getting Started

The Fixed Income module covers two sides of the bond market. The first is individual bonds: prices, yields, duration and convexity for every US Treasury and for thousands of corporate bonds, calculated from their market prices. The second is market data: Euribor, the policy rates of the European Central Bank and the Federal Reserve, government bond yields for 40+ countries and the ICE BofA corporate bond indices by rating and maturity.

The Treasury prices come from the Treasury's own daily FedInvest prices and the market data from public sources, so neither needs an API key. The corporate bonds come from the published holdings of bond ETFs, and their spread over Treasuries uses the Treasury par yield curve, which takes a FinancialModelingPrep API key.

### Loading the Module

The Fixed Income module can be imported on its own, or reached through `companies.fixedincome` after you initialise a `Toolkit`. Here it is imported directly. To set it up with market data from 2012 onwards:

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date="2012-01-01", api_key="FINANCIAL_MODELING_PREP_KEY")
```

The `start_date` only affects the market data functions; the bond functions price on a single day, the latest by default or the one you pass as `date`.

### Bond Statistics of the Benchmark Treasuries

`collect_bond_statistics` returns the key figures of individual bonds in one call. Without bonds or an issuer it takes the benchmark Treasuries: the note or bond maturing closest to 2, 3, 5, 7, 10, 20 and 30 years after the price date. To calculate their statistics on 5 November 2026 and keep the main columns:

```python
statistics = fixedincome.collect_bond_statistics(date="2026-11-05")

statistics[["Coupon", "Maturity", "Price", "Yield to Maturity", "Modified Duration", "DV01", "Convexity"]]
```

Which returns:

| CUSIP     |   Coupon | Maturity   |    Price |   Yield to Maturity |   Modified Duration |   DV01 |   Convexity |
|:----------|---------:|:-----------|---------:|--------------------:|--------------------:|-------:|------------:|
| 91282CRU7 |   0.0462 | 2028-10-31 | 100.3125 |              0.0446 |              1.8777 | 0.0188 |      4.5145 |
| 91282CLR0 |   0.0412 | 2029-10-31 |  98.875  |              0.0453 |              2.7748 | 0.0275 |      9.2977 |
| 91282CRT0 |   0.0475 | 2031-10-31 | 100.6875 |              0.0459 |              4.3963 | 0.0443 |     22.7527 |
| 91282CRV5 |   0.0488 | 2033-10-31 | 101.0625 |              0.0469 |              5.8687 | 0.0593 |     40.7069 |
| 91282CRF0 |   0.0462 | 2036-08-15 |  98.4375 |              0.0483 |              7.6914 | 0.0765 |     71.6857 |
| 912810RU4 |   0.0288 | 2046-11-15 |  70.0312 |              0.0533 |             13.6289 | 0.0973 |    241.4593 |
| 912810UW6 |   0.0512 | 2056-08-15 |  98.125  |              0.0525 |             14.8801 | 0.1477 |    333.2043 |

The yield rises from 4.46% at two years to 5.33% at twenty, and the 30-year bond yields a little less than the 20-year one. The modified duration says how much the price moves for a one percentage point change in the yield: 1.9% for the two-year note against 14.9% for the 30-year bond. The DV01 puts that in money, 0.15 per 100 of par for a one basis point move in the 30-year yield. The 20-year bond trades at 70 because its 2.88% coupon is far below today's yields.

The same statistics are available for any bond by CUSIP or ISIN with `bonds=`, for an issuer's bonds with `issuer=`, or for every bill, note and bond in a maturity range.

### Every Treasury Security on One Day

`get_treasury_securities` lists every marketable US Treasury, about 460 bills, notes, bonds, TIPS and floating rate notes, with its price, yield to maturity and modified duration. To get them for the same day:

```python
treasuries = fixedincome.get_treasury_securities(date="2026-11-05")
```

Which gives one row per security. Averaged per year to maturity, the nominal bills, notes and bonds set against the TIPS, whose yield is a real yield:

{% include ft-chart.html id="fixed-income-treasuries" src="/assets/data/financetoolkit-guides/fixed-income.json" label="Average yield to maturity of US Treasuries and TIPS by years to maturity" %}

The nominal yields climb from 4.16% within a year to about 5.3% from twenty years out. TIPS yield 2.35% to 3.1% over the same maturities, so the gap between the two, the inflation the market prices in, is about 2.2 percentage points at ten years and at thirty.

### Corporate Bonds from ETF Holdings

Prices of individual corporate bonds are not published for free, but bond ETFs publish their holdings every day. `get_bond_universe` reads them, about 8,000 investment grade and high yield bonds by default, and calculates each bond's yield, duration and G-spread, its yield over the Treasury curve at the same maturity. To get the bonds of Apple:

```python
apple_bonds = fixedincome.get_bond_universe(issuer="APPLE INC")
```

Which gives Apple's bonds from 2028 to 2062, here with the yield to maturity and the G-spread in a tab each:

{% include ft-chart.html id="fixed-income-corporate" src="/assets/data/financetoolkit-guides/fixed-income.json" label="Yield to maturity and G-spread of Apple's bonds by maturity" %}

Apple's 43 bonds yield from 4.6% for 2028 to 6.0% for the 2050s and 2060s, at 0.17 to 0.32 percentage points over Treasuries up to 2032 and about 0.7 points for the bonds maturing after 2040. The bonds maturing from 2049, most issued with coupons of 2.4% to 3% when rates were low, trade at 50 to 62.

### Euribor and Central Bank Rates

Swaps reference a benchmark rate such as Euribor or SOFR, and those in turn follow the policy rates of the central banks. To get the Euribor rates for four maturities:

```python
euribor = fixedincome.get_euribor_rates()
```

Which gives monthly rates since 2012, here with the European Central Bank's hiking cycle shaded:

{% include ft-chart.html id="fixed-income-euribor" src="/assets/data/financetoolkit-guides/fixed-income.json" label="Euribor rates by maturity since 2012" %}

The 3-month Euribor was below zero from May 2015 to June 2022, bottomed at -0.6% at the end of 2021, and then rose to 4% by October 2023 as the European Central Bank fought inflation. It came back to about 2% in 2025, and the 12-month rate climbing above the shorter maturities again shows the market expecting higher rates ahead.

The policy rates themselves are available for the European Central Bank (refinancing, marginal lending and deposit facility rates) and the Federal Reserve (the effective federal funds rate, its percentiles and volume, and the target range). To get both:

```python
ecb_rates = fixedincome.get_european_central_bank_rates()

fed_rates = fixedincome.get_federal_reserve_rates()
```

Which gives daily series, shown here as one observation per month. The first tab sets the ECB deposit rate against the effective federal funds rate, the other two show each central bank's rates in full, with the Federal Reserve's target range shaded:

{% include ft-chart.html id="fixed-income-central-banks" src="/assets/data/financetoolkit-guides/fixed-income.json" label="Policy rates of the European Central Bank and the Federal Reserve" %}

The two took very different paths into the same hiking cycle. The ECB kept its deposit rate below zero from 2014 to 2022, at -0.5% from 2019, while the Federal Reserve had already raised rates to 2.4% by 2019. Both then hiked hard in 2022 and 2023, the ECB to 4% and the Fed to a target range of 5.25%-5.50%, with the effective rate at 5.33%. Today the deposit rate is 2.5% and the effective federal funds rate 3.88%.

### Government Bond Yields

Government bond yields are the risk-free benchmark against which every other bond is priced. `get_government_bond_yield` returns the 10-year yield by default and the 3-month yield with `short_term=True`. To get the 10-year yields and select five large bond markets:

```python
government_bond_yields = fixedincome.get_government_bond_yield(short_term=False)

government_bond_yields[["United States", "Japan", "Germany", "China", "United Kingdom"]]
```

Which gives quarterly yields for the five markets, and in the second tab the latest yield of every country, ranked:

{% include ft-chart.html id="fixed-income-government" src="/assets/data/financetoolkit-guides/fixed-income.json" label="10-year government bond yields for the United States, Japan, Germany, China and the United Kingdom, and the latest yield per country" %}

German and Japanese yields went below zero around 2019 and 2020, with Germany at -0.6%, while the United States and the United Kingdom are now at about 4.8% and 5%. China moved the other way, from about 4.5% in 2014 to 1.7%. Across countries, the latest 10-year yields range from 12.3% in Colombia to 0.5% in Switzerland, with emerging markets such as Mexico, Brazil and South Africa near 9%.

### Corporate Bonds: ICE BofA Indices

The ICE BofA corporate bond indices are widely used benchmarks for valuing fixed income portfolios. The option-adjusted spread (OAS) is the spread of an index over the Treasury curve after removing the value of embedded options such as call features, in basis points. It is the cleanest measure of what the market charges for credit risk. To get the spreads per credit rating:

```python
fixedincome.get_ice_bofa_option_adjusted_spread(maturity=False)
```

Which gives a daily spread per rating, shown here weekly and split into high yield and investment grade, with the April 2025 tariff shock shaded:

{% include ft-chart.html id="fixed-income-oas" src="/assets/data/financetoolkit-guides/fixed-income.json" label="ICE BofA option-adjusted spread by credit rating" %}

Spreads run from about 40 basis points for AAA to more than 1,000 for CCC, and every rating jumped in the tariff shock of April 2025 before coming back within weeks. Since then the CCC bucket has widened on its own, to 1,310 basis points, the widest in the three years shown, while BB and B at 200 and 336 and the investment grade ratings are still close to the tight end of their range.

The yield to worst is the lowest yield an investor can receive on a bond without the issuer defaulting, taking into account that the issuer may call the bond early. That makes it the conservative yield measure for callable bonds. To get it per maturity bucket:

```python
fixedincome.get_ice_bofa_yield_to_worst(maturity=True)
```

Which gives a daily yield per maturity bucket. The first tab compares the curve at the start of the data with the latest one, the second shows it weekly over time:

{% include ft-chart.html id="fixed-income-ytw" src="/assets/data/financetoolkit-guides/fixed-income.json" label="ICE BofA yield to worst by maturity" %}

In October 2023 the corporate curve was almost flat, from 6.1% for 1-3 years to 6.5% for 15+ years. Short yields have since fallen to 5.3% with the policy rate, while the long end stayed at 6.5%, so the curve is now upward sloping by more than a percentage point.

The same indices are available as effective yield (`get_ice_bofa_effective_yield`) and total return (`get_ice_bofa_total_return`), each by rating or by maturity.

{% include ft-charts-script.html %}
