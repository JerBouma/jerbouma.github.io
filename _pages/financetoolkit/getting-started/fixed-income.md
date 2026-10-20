---
title: "Fixed Income"
seo_title: "Fixed Income Guide | Finance Toolkit"
seo_title_suffix: false
excerpt: "How to value bonds and swaptions, and follow benchmark rates, government yields and corporate credit spreads with the Finance Toolkit's Fixed Income module."
description: "Value bonds and swaptions and track Euribor, ECB and Fed rates, government bond yields and ICE BofA credit spreads in Python with the Finance Toolkit."
author_profile: false
permalink: /projects/financetoolkit/docs/getting-started/fixed-income
classes: wide-sidebar
layout: single
redirect_from:
  - /projects/financetoolkit/fixed-income-notebook
sidebar:
  nav: "financetoolkit-guides"
---

The Fixed Income module covers two sides of the bond market. The first is valuation: present value, yields, duration and convexity for any bond you describe, and the Black and Bachelier models for interest rate derivatives such as swaptions. The second is market data: Euribor, the policy rates of the European Central Bank and the Federal Reserve, government bond yields for 40+ countries and the ICE BofA corporate bond indices by rating and maturity.

The valuation functions work on the numbers you pass in, so they need no data at all. The market data comes from public sources and needs no API key either.

## Loading the Module

The Fixed Income module can be imported on its own, or reached through `companies.fixedincome` after you initialise a `Toolkit`. Here it is imported directly. To set it up with market data from 2012 onwards:

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date="2012-01-01")
```

The `start_date` only affects the market data functions; the valuation functions below ignore it.

## Bond Statistics

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

## Duration across Coupons and Maturities

Without a coupon rate or maturity, `get_duration` calculates the duration for a grid of both: coupon rates from 0.5% to 15% against maturities of one to ten years, at a yield to maturity of 8% and annual coupons by default. That shows at a glance how the two drive interest rate risk. To calculate the modified duration for the whole grid:

```python
duration = fixedincome.get_duration()
```

Which shows duration rising with maturity and falling with the coupon rate, since a higher coupon returns more of the cash earlier; at ten years, a 1% coupon bond has a duration of 8.7 against 6.6 for a 9% coupon:

{% include ft-chart.html id="fixed-income-duration" src="/assets/data/financetoolkit-guides/fixed-income.json" label="Modified duration by coupon rate and years to maturity" %}

Set `duration_type` to `"macaulay"`, `"effective"` or `"dollar"` for the other measures, or pass `coupon_rate` and `years_to_maturity` to calculate a single bond.

## Pricing Swaptions with Black and Bachelier

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

Which returns a price for each strike rate and maturity, with the swap's tenor equal to the maturity by default. The at-the-money swaption (strike 3.25%) with five years to maturity is worth about 246,000 under Black and 248,000 under Bachelier; the models only part ways for deep out-of-the-money strikes, where the normal distribution gives low rates more probability:

{% include ft-chart.html id="fixed-income-swaption" src="/assets/data/financetoolkit-guides/fixed-income.json" label="Receiver swaption prices by strike rate for the Black and Bachelier models" %}

<div class="fs-callout" markdown="1"><p class="fs-callout__title">Volatility quotes</p>

Passing a lognormal quote such as 0.20 to the Bachelier model without `volatility_type` treats it as 2,000 basis points of normal volatility and overprices the swaption many times over. A normal volatility quote of, say, 65 basis points is passed as `volatility=0.0065`.
</div>

## Euribor and Central Bank Rates

Swaps reference a benchmark rate such as Euribor or SOFR, and those in turn follow the policy rates of the central banks. To get the Euribor rates for four maturities:

```python
euribor = fixedincome.get_euribor_rates()
```

Which shows the full cycle since 2012: Euribor dropped below zero from 2015, bottomed around -0.6% at the end of 2021 and rose to about 4% in late 2023 when the European Central Bank fought inflation:

{% include ft-chart.html id="fixed-income-euribor" src="/assets/data/financetoolkit-guides/fixed-income.json" label="Euribor rates by maturity since 2012" %}

The policy rates themselves are available for the European Central Bank (refinancing, marginal lending and deposit facility rates) and the Federal Reserve (the effective federal funds rate, its percentiles and volume, and the target range). To get both:

```python
ecb_rates = fixedincome.get_european_central_bank_rates()

fed_rates = fixedincome.get_federal_reserve_rates()
```

Which gives daily series, shown here as one observation per week, with the ECB deposit rate at -0.5% in 2019 and 4% at its 2023-2024 peak, and the Federal Reserve's target range peaking at 5.25%-5.50%:

{% include ft-chart.html id="fixed-income-central-banks" src="/assets/data/financetoolkit-guides/fixed-income.json" label="Policy rates of the European Central Bank and the Federal Reserve" %}

## Government Bond Yields

Government bond yields are the risk-free benchmark against which every other bond is priced. `get_government_bond_yield` returns the 10-year yield by default and the 3-month yield with `short_term=True`. To get the 10-year yields and select five large bond markets:

```python
government_bond_yields = fixedincome.get_government_bond_yield(short_term=False)

government_bond_yields[["United States", "Japan", "Germany", "China", "United Kingdom"]]
```

Which shows German and Japanese yields below zero around 2019 and 2020, and the United States and United Kingdom now at close to 5%, while China moved the other way, from about 4.5% in 2014 to below 2%:

{% include ft-chart.html id="fixed-income-government" src="/assets/data/financetoolkit-guides/fixed-income.json" label="10-year government bond yields for the United States, Japan, Germany, China and the United Kingdom" %}

## Corporate Bonds: ICE BofA Indices

The ICE BofA corporate bond indices are widely used benchmarks for valuing fixed income portfolios. The option-adjusted spread (OAS) is the spread of an index over the Treasury curve after removing the value of embedded options such as call features, in basis points. It is the cleanest measure of what the market charges for credit risk. To get the spreads per credit rating:

```python
fixedincome.get_ice_bofa_option_adjusted_spread(maturity=False)
```

Which shows spreads from about 40 basis points for AAA to well over 1,000 for CCC, with investment grade spreads near the tight end of their range and the CCC bucket widening on its own:

{% include ft-chart.html id="fixed-income-oas" src="/assets/data/financetoolkit-guides/fixed-income.json" label="ICE BofA option-adjusted spread by credit rating" %}

The yield to worst is the lowest yield an investor can receive on a bond without the issuer defaulting, taking into account that the issuer may call the bond early. That makes it the conservative yield measure for callable bonds. To get it per maturity bucket:

```python
fixedincome.get_ice_bofa_yield_to_worst(maturity=True)
```

Which shows an upward-sloping corporate curve, with the 1-3 year bucket at about 5.3% and the 15+ year bucket at about 6.5%, steeper than in 2023 when the buckets were almost level:

{% include ft-chart.html id="fixed-income-ytw" src="/assets/data/financetoolkit-guides/fixed-income.json" label="ICE BofA yield to worst by maturity" %}

The same indices are available as effective yield (`get_ice_bofa_effective_yield`) and total return (`get_ice_bofa_total_return`), each by rating or by maturity.

<div class="fs-ref"><a href="/projects/financetoolkit/docs/fixedincome"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Fixed Income</a></div>

{% include ft-charts-script.html %}
