## How It Works

An ESG replaces a single forecast with a distribution. That is what ALM studies, strategic asset allocation, pension and retirement planning, reserving and Solvency II valuation need: the median path, but also the bad years and the tail. Installation and a first run are on the [Finance Scenarios page](/projects/financescenarios#installation); the Getting Started section below shows every part with real output.

### What Is Modeled

Each factor follows a model suited to how it behaves: rates, inflation and spreads revert to a long-run level at their own historical speed, equities switch between calm and crisis regimes so bad months cluster, and currencies keep their historical volatility.

| Area | What is simulated | Model | Guide |
|:-----|:------------------|:------|:------|
| Short and long rates | One rate per country, short or long end | Vasicek (default, can go negative; Hull-White when fitted to today's curve, EIOPA's in a risk-neutral run), CIR (rates kept near or above zero), Wilkie, Hibbert two-factor | [Interest rates](/projects/financescenarios/docs/interest-rates) |
| Yield curve | Level, slope and curvature of the whole curve | Dynamic Nelson-Siegel | [Interest rates](/projects/financescenarios/docs/interest-rates) |
| Forward curve | The full forward curve, arbitrage-free | Two-factor Gaussian HJM | [Interest rates](/projects/financescenarios/docs/interest-rates) |
| Rates and inflation jointly | Nominal and real rates, inflation, optionally equities | KNW, with stochastic volatility or priced like the market | [KNW](/projects/financescenarios/docs/interest-rates#knw) |
| Inflation | Year-over-year inflation per country | Mean-reverting (Ornstein-Uhlenbeck) or Wilkie AR(1); risk-neutral, random around the breakeven curve | [Economy](/projects/financescenarios/docs/economy) |
| Unemployment | Unemployment rate per country | Mean-reverting with a Phillips-curve link to inflation | [Economy](/projects/financescenarios/docs/economy) |
| Business cycle | OECD composite leading indicator | Mean-reverting | [Economy](/projects/financescenarios/docs/economy) |
| Longevity | Mortality improvement by age | Cairns-Blake-Dowd | [Economy](/projects/financescenarios/docs/economy) |
| Equities | Indices, sectors, regions, styles | Regime-switching lognormal | [Markets](/projects/financescenarios/docs/markets) |
| Currencies | Each currency against the dollar | Lognormal with no trend by default, or a historical or interest-rate-parity drift | [Markets](/projects/financescenarios/docs/markets) |
| Commodities | Gold, oil and other futures | Mean-reverting log price (Schwartz), or two-factor | [Markets](/projects/financescenarios/docs/markets) |
| Real estate | House-price growth | Mean-reverting | [Markets](/projects/financescenarios/docs/markets) |
| Dividends | Dividend yield and dividend growth | Mean-reverting log yield, Wilkie-style growth | [Markets](/projects/financescenarios/docs/markets) |
| Credit | Spreads by maturity or rating, the credit curve, rating migration and default | Mean-reverting spreads, Nelson-Siegel credit curve, a credit cycle driving migration | [Markets](/projects/financescenarios/docs/markets) |
| Stress and climate | Fed and ESRB stress tests, NGFS climate pathways, your own narratives | Overlays on a run | [Regimes](/projects/financescenarios/docs/regimes) |

Interest rates, inflation, equities and unemployment are always simulated; the rest is switched on per factor set. [Coverage](/projects/financescenarios/docs/coverage) lists every model, calibration choice and known gap, and the [reference](/projects/financescenarios/docs) documents each model's parameters.

### How the Factors Are Linked

When equities fall, spreads, rates and currencies should move the way they did in past sell-offs. Where theory says one variable drives another (inflation driving unemployment, a rate gap driving an exchange rate), the driver's simulated path feeds the next factor; everything else is tied together by one correlation matrix of the historical shocks. The direct links run one way, from driver to follower:

<div class="fs-diagram">
<div class="fs-links">
  <div class="fs-links__row">
    <div class="fs-node"><b>Leading indicator</b><small>business cycle, opt-in</small></div>
    <div class="fs-links__to">
      <div class="fs-link is-dashed"><em>drift</em><div class="fs-node"><b>Inflation</b></div></div>
      <div class="fs-link is-dashed"><em>drift</em><div class="fs-node"><b>Interest rates</b></div></div>
      <div class="fs-link is-dashed"><em>drift</em><div class="fs-node"><b>Credit spreads</b></div></div>
      <div class="fs-link is-dashed"><em>crisis odds</em><div class="fs-node"><b>Equities</b></div></div>
    </div>
  </div>
  <div class="fs-links__row">
    <div class="fs-node is-accent"><b>Inflation</b><small>top of the cascade</small></div>
    <div class="fs-links__to">
      <div class="fs-link"><em>Phillips curve</em><div class="fs-node"><b>Unemployment</b></div></div>
      <div class="fs-link"><em>Wilkie and KNW</em><div class="fs-node"><b>Interest rates</b></div></div>
      <div class="fs-link"><em>Wilkie-style</em><div class="fs-node"><b>Dividends</b></div></div>
    </div>
  </div>
  <div class="fs-links__row">
    <div class="fs-node"><b>Dividends</b><small>Wilkie-style</small></div>
    <div class="fs-links__to">
      <div class="fs-link"><em>share prices</em><div class="fs-node"><b>Equities</b></div></div>
    </div>
  </div>
  <div class="fs-links__row">
    <div class="fs-node"><b>Interest rates</b></div>
    <div class="fs-links__to">
      <div class="fs-link"><em>rate gap</em><div class="fs-node"><b>Exchange rates</b><small>interest-rate parity</small></div></div>
    </div>
  </div>
</div>
<p class="fs-diagram__note">Dashed: only with business-cycle conditioning. Each arrow is a direct link in the model's equations.</p>
</div>

Everything else, the yield curve, real estate, commodities and mortality among it, is linked only through the correlation matrix. [How a run is built](/projects/financescenarios/docs/architecture#dependence) explains both mechanisms.

### Real-World and Risk-Neutral Runs

Every run is simulated under one of two measures, each answering its own question:

<div class="ca-cards">
  <div><i class="ca-icon fas fa-globe" aria-hidden="true"></i><p class="ca-card-title">Real-world: what could happen?</p><p>Keeps each factor's historical drift and risk premia. For ALM studies, asset allocation and capital.</p></div>
  <div><i class="ca-icon fas fa-scale-balanced" aria-hidden="true"></i><p class="ca-card-title">Risk-neutral: what is this worth?</p><p>Grows every asset at the risk-free rate, so it reproduces today's prices. For guarantees and the Solvency II best estimate.</p></div>
</div>

[Configuration](/projects/financescenarios/docs/configuration#real-world-and-risk-neutral-measures) explains the difference and which factors have a risk-neutral form. Both come from the same configuration:

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(settings="default", factor_set="default")

real_world = scenarios.simulate()                         # ALM, allocation, risk
risk_neutral = scenarios.simulate(measure="risk_neutral")  # valuation, best estimate
real_world.describe()                                     # every factor at a glance
```

All history comes from the [Finance Toolkit](https://github.com/JerBouma/FinanceToolkit); most factors calibrate on free OECD and Yahoo Finance data without any API key. Each factor is simulated in its own currency and can be converted into one reporting currency afterwards.
