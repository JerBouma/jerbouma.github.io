## Getting Started

The Fixed Income module covers two sides of the bond market. The first is valuation: present value, yields, duration and convexity for any bond you describe, and the Black and Bachelier models for interest rate derivatives such as swaptions. The second is market data: Euribor, the policy rates of the European Central Bank and the Federal Reserve, government bond yields for 40+ countries and the ICE BofA corporate bond indices by rating and maturity.

The valuation functions work on the numbers you pass in, so they need no data at all. The market data comes from public sources and needs no API key either.

### Loading the Module

The Fixed Income module can be imported on its own, or reached through `companies.fixedincome` after you initialise a `Toolkit`. Here it is imported directly. To set it up with market data from 2012 onwards:

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date="2012-01-01")
```

The `start_date` only affects the market data functions; the valuation functions below ignore it.

### Bond Statistics

`collect_bond_statistics` returns the key figures of a single bond in one call. Take a bond with a par value of 1,000, a 5% coupon paid twice a year, five years to maturity and a yield to maturity of 8%. Because the yield is above the coupon rate, the bond has to trade below par to give the buyer that yield. To calculate its statistics:

```python
fixedincome.collect_bond_statistics(
    par_value=1000,
    coupon_rate=0.05,
    years_to_maturity=5,
    yield_to_maturity=0.08,
    frequency=2,
)
```

Which gives a present value of 878.34, a discount of about 12% to par:

| Statistic           |    Value |
|:--------------------|---------:|
| Present Value       |   878.34 |
| Current Yield       |    5.69% |
| Effective Yield     |    5.06% |
| Macaulay's Duration |     4.44 |
| Modified Duration   |     4.27 |
| Effective Duration  |     4.27 |
| Dollar Duration     |    37.53 |
| DV01                |     0.38 |
| Convexity           |    21.70 |

The current yield is the annual coupon of 50 divided by the price, and the effective yield is the coupon rate compounded over the two payments in a year. The modified duration of 4.27 says the price falls by roughly 4.27% when the yield rises by one percentage point, and the DV01 puts that in currency: about 0.38 per bond for a one basis point move. Convexity measures how much that sensitivity itself changes as yields move, the correction you add for larger rate shocks.

### Duration across Coupons and Maturities

Without a coupon rate or maturity, `get_duration` calculates the duration for a grid of both: coupon rates from 0.5% to 15% against maturities of one to ten years, at a yield to maturity of 8% and annual coupons by default. That shows at a glance how the two drive interest rate risk. To calculate the modified duration for the whole grid:

```python
duration = fixedincome.get_duration()
```

Which gives a duration for every combination, shown here for five coupon rates:

{% include ft-chart.html id="fixed-income-duration" src="/assets/data/financetoolkit-guides/fixed-income.json" label="Modified duration by coupon rate and years to maturity" %}

Duration rises with maturity and falls with the coupon rate, since a higher coupon returns more of the cash earlier. At one year every bond has a duration of 0.93, but at ten years a 1% coupon bond has a duration of 8.7 against 6.6 for a 9% coupon: the same move in yields hits the low-coupon bond about a third harder.

Set `duration_type` to `"macaulay"`, `"effective"` or `"dollar"` for the other measures, or pass `coupon_rate` and `years_to_maturity` to calculate a single bond.

### Pricing Swaptions with Black and Bachelier

A swaption gives the holder the right, but not the obligation, to enter an interest rate swap at a fixed strike rate. A receiver swaption, the default, pays off when rates fall below the strike, which makes it a hedge against falling rates. `get_derivative_price` values it with either the Black model, which assumes the swap rate is lognormally distributed, or the Bachelier model, which assumes normally distributed rates and therefore also works when rates are negative.

The two models quote volatility differently: Black reads `volatility=0.20` as 20% of the forward rate, Bachelier as an absolute 20 percentage points. To price both on the same market, a forward swap rate of 3.25% with 20% lognormal volatility, pass `volatility_type="lognormal"` to the Bachelier model so it converts the quote. To price a range of strike rates and maturities on a notional of 10 million:

```python
black = fixedincome.get_derivative_price(
    model="black",
    forward_rate=0.0325,
    volatility=0.20,
    risk_free_rate=0.02,
    notional=10_000_000,
)

bachelier = fixedincome.get_derivative_price(
    model="bachelier",
    forward_rate=0.0325,
    volatility=0.20,
    volatility_type="lognormal",
    risk_free_rate=0.02,
    notional=10_000_000,
)
```

Which returns a price for each strike rate and maturity, with the swap's tenor equal to the maturity by default. The first tab puts the two models side by side for five years to maturity and the strikes up to just above the money, where they differ most; the other tabs show each model across maturities:

{% include ft-chart.html id="fixed-income-swaption" src="/assets/data/financetoolkit-guides/fixed-income.json" label="Receiver swaption prices by strike rate for the Black and Bachelier models" %}

At the money (strike 3.25%) the five-year swaption is worth 246,000 under Black and 248,000 under Bachelier. Deep out of the money the models part ways: at a strike of 1.75% Bachelier gives 48,800 against 17,000 for Black, and at 0.75% about 10,800 against almost nothing, because the normal distribution gives low and even negative rates far more probability than the lognormal one. Above the money the two converge again, as the value becomes mostly intrinsic. Longer maturities are worth more at every strike, since the option covers more years of swap payments.

<div class="fs-callout" markdown="1"><p class="fs-callout__title">Volatility quotes</p>

Passing a lognormal quote such as 0.20 to the Bachelier model without `volatility_type` treats it as 2,000 basis points of normal volatility and overprices the swaption many times over. A normal volatility quote of, say, 65 basis points is passed as `volatility=0.0065`.
</div>

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
