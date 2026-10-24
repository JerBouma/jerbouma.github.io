## Reference

The reference is generated from the docstrings in the package, so it says what `help(...)` says in Python: what each class and function does, a worked example with real output where the docstring has one, and the arguments and return value folded underneath.

The factor and model classes are reached through a `Scenarios` object, after `scenarios = Scenarios.from_profiles(...)`:

```python
scenarios.equities               # Equities
scenarios.fx                     # FX
scenarios.commodities            # Commodities
scenarios.real_estate            # RealEstate
scenarios.dividend_yield         # DividendYield
scenarios.dividend_growth        # DividendGrowth
scenarios.credit                 # Credit
scenarios.credit_term_structure  # CreditTermStructure
scenarios.credit_migration       # CreditMigration
```

`rating_migration` imports as follows:

```python
from financescenarios import rating_migration
```

### Equities

Simulate equity prices: a broad stock index, a sector, a region or an investment style, each tracked through one
ticker such as SPY or an ETF.

The model is the regime-switching lognormal model of [Hardy (2001)](https://doi.org/10.1080/10920277.2001.10595984).
Markets alternate between calm stretches of steady gains and turbulent stretches of losses and large swings, and
once turbulent they tend to stay so for months. Each regime has its own mean and volatility of log-returns, and the
market switches between them with fitted chances. A single lognormal understates crashes; the mixture of regimes
gives the fatter left tail and the clustered, multi-period drawdowns that matter for guarantees, capital and
tail metrics, while prices stay positive. Each equity, such as SPY or a sector, region or style ETF, follows its own
regime path and is linked to the other factors through the correlation matrix.

The options:

- `method`: `regime_switching` (the default); `hibbert_regime_switching`, the same model on the return above a short
  interest rate (Hibbert, Mowbray and Turnbull
  [(2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf));
  `wilkie_derived`, the price as dividends divided by the dividend yield (see
  [Wilkie (1986)](https://doi.org/10.1017/S0071368600009009));
  `knw_sv`, the equity leg of the Koijen, Nijman and Werker model, fitted together with its interest rate;
  or `cp2022`, the equity index of De Nederlandsche Bank's CP2022 model, read by `Cp2022`.
- `condition_on_business_cycle`: turbulence becomes more likely when the leading indicator signals a downturn
  as in [Filardo (1994)](https://doi.org/10.1080/07350015.1994.10524545).
- `condition_on_inflation`: turbulence becomes far more likely when inflation runs high, the ticker keeping its
  own regimes, with the sensitivity read from US history since 1946 (see `calibrate_inflation_tvtp`).
- `regime_history`: how often and how long the market is calm or turbulent come from a long index of it, such as
  Ken French's US market since 1926, at the ticker's own average return and volatility (see
  `calibrate_on_regime_history`).
- `measure: risk_neutral`: one volatility and a drift of the risk-free rate minus the dividend yield, for
  market-consistent valuation as in [Black and Scholes (1973)](https://doi.org/10.1086/260062), or a volatility
  that moves with `volatility_source: heston`, as in [Heston (1993)](https://doi.org/10.1093/rfs/6.2.327).
- `beliefs`: your own regime means and volatilities instead of the fitted ones.

Prices are each ticker's adjusted closes (dividends reinvested) from the Finance Toolkit; any ticker worldwide works.
Total returns are what Hardy fitted: Ahlgrim, D'Arcy and Gorvett (2005, section 3) note that Hardy uses total equity
returns, dividends and the compensation for the risk-free rate included. The default monthly frequency is also
the providers' own: Barrie & Hibbert's results use a one-month step in Hibbert, Mowbray and Turnbull (2001, section
5.2.1), and Ahlgrim, D'Arcy and Gorvett (2005, section 3) fit monthly excess returns.

The `equities[i]` keys of a factor set and their defaults are listed under
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/configuration#configuration-classes).

Beliefs cannot be combined with `measure: risk_neutral` or `wilkie_derived`; in a regime YAML, address one entry as
`"equities.<name>"`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Equities(toolkit: Toolkit)
```

</details>

#### Equities.calibrate

Calibrate one equity from its price history: the mean and volatility of its log-return in each regime, and the
chance of moving between regimes each period.

The scenarios inherit the market's own history of calm and turbulent stretches: how deep and how long its
drawdowns were, and how often they came. The diagonal of the transition matrix is the chance of staying in a
regime one more period, so the expected stay is 1 / (1 - that chance): a 0.90 monthly chance of staying calm means
calm stretches last about ten months. Regime 0 is always the one with the lowest mean return.

The regimes are never observed, only the returns, so the fit is the Baum-Welch expectation-maximization algorithm
for hidden Markov models of [Baum, Petrie, Soules and Weiss (1970)](https://doi.org/10.1214/aoms/1177697196).
Means and volatilities are annual; the transition matrix is per period of the data.

Also known as: regime-switching lognormal (RSLN), hidden Markov model of equity returns.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.equities.equities_controller import Equities

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2005-01-01", benchmark_ticker=None)
equities = Equities(toolkit)

equities.calibrate("us_broad", "SPY", period="monthly")
```

Which returns (calibrated on 2026-10-04):

| regime | regime_mean | regime_volatility | chance of staying | long-run share |
|-------:|------------:|------------------:|------------------:|---------------:|
| 0 | -0.0009 | 0.2020 | 0.8715 | 0.4377 |
| 1 | 0.1853 | 0.0793 | 0.9000 | 0.5623 |

The S&P 500's turbulent regime has a flat average return at 20% volatility, its calm one 18.5% a year at 8%.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(name: str, ticker: str, n_regimes: int = 2, period: str = 'monthly') -> RegimeParams
```

**Args:**

- <u>name (str):</u> the equity's name in the scenarios, e.g. "us_broad".
- <u>ticker (str):</u> the ticker to fit, such as "SPY" or a sector, regional or style ETF.
- <u>n_regimes (int):</u> the number of regimes, at least 2. Defaults to 2 (calm and turbulent, as in Hardy (2001)).
- <u>period (str):</u> the price frequency: "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "monthly".

**Returns:**

<u>RegimeParams:</u> `regime_means`, `regime_volatilities`, `transition_matrix`, `stationary_distribution` (long-run share of time per regime), `initial_regime` and `initial_value` (the last price).

**Raises:**

- <u>ValueError:</u> if `period`, `n_regimes` or `ticker` is invalid, there are fewer than `n_regimes * 5` prices, or a regime ends up with almost no observations.

</details>

#### Equities.calibrate_tvtp

Calibrate one equity whose regime switching follows the business cycle: regimes whose chance of switching is tied
to the leading indicator, fitted together.

With `calibrate()` the chance of a calm market turning turbulent is the same every month. Here it rises when the
leading indicator (the OECD Composite Leading Indicator, around 100 in a normal economy) signals a downturn, so
turbulent stretches cluster around weak economies. This is the time-varying transition probability (TVTP) model of
[Filardo (1994)](https://doi.org/10.1080/07350015.1994.10524545), estimated with the expectation-maximization
algorithm of [Diebold, Lee and Weinbach (1994)](https://doi.org/10.1093/oso/9780198773917.003.0010): the regimes,
their means and volatilities and the logit of each switching chance on the indicator's level in one likelihood
(`fit_regime_switching_tvtp_em`), as for inflation-driven switching, rather than classifying the regimes first and
regressing afterwards (`fit_regime_switching_tvtp`).

In a factor set this is `condition_on_business_cycle: true`, which needs `leading_indicator.enabled: true`.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.equities.equities_controller import Equities
from financescenarios.factors.leading_indicator.leading_indicator_controller import LeadingIndicator

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2005-01-01", benchmark_ticker=None)
leading_indicator = LeadingIndicator(toolkit)
leading_indicator.calibrate(country="United States", period="monthly")

equities = Equities(toolkit)
params = equities.calibrate_tvtp(
    "us_broad", "SPY", leading_indicator.series, leading_indicator.dates, period="monthly"
)
```

Which returns (calibrated on 2026-10-19):

| regime | regime_mean | regime_volatility | baseline_log_odds | covariate_sensitivity |
|-------:|------------:|------------------:|:------------------|:----------------------|
| 0 | 0.0091 | 0.2001 | [0.0, -39.6029] | [0.0, 0.3800] |
| 1 | 0.1842 | 0.0765 | [0.0, -17.0365] | [0.0, 0.1894] |

In the calm regime (row 1) the chance of turning turbulent is 5.5% a month at a leading indicator of 105 and 27.7%
at 95, so a weakening economy shortens calm stretches from about 18 months to under four. The two-step fit read
a far weaker link from the same data (5.8% and 8.8%), as classifying the regimes first blurs the months around
each switch.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_tvtp(
    name: str,
    ticker: str,
    business_cycle_covariate: pl.Series,
    business_cycle_covariate_dates: pl.Series,
    n_regimes: int = 2,
    period: str = 'monthly',
) -> RegimeParams
```

**Args:**

- <u>name (str):</u> the equity's name in the scenarios.
- <u>ticker (str):</u> the ticker to fit, as in `calibrate()`.
- <u>business_cycle_covariate (pl.Series):</u> the leading indicator's historical levels, e.g. `LeadingIndicator.series`.
- <u>business_cycle_covariate_dates (pl.Series):</u> the dates of those levels, e.g. `LeadingIndicator.dates`.
- <u>n_regimes (int):</u> the number of regimes, at least 2. Defaults to 2.
- <u>period (str):</u> the price frequency, as in `calibrate()`. Defaults to "monthly".

**Returns:**

<u>RegimeParams:</u> the regime fit, with `tvtp` holding `baseline_log_odds` and `covariate_sensitivity`, one row per starting regime.

**Raises:**

- <u>ValueError:</u> if `period`, `n_regimes` or `ticker` is invalid, too few prices line up with the indicator by date, or a regime has too few observed transitions to fit.

</details>

#### Equities.calibrate_inflation_tvtp

Calibrate one equity whose chance of turning turbulent rises with inflation: `calibrate()`'s regimes, with
switching chances that follow the inflation level.

Stocks have done badly when inflation ran high. On Shiller's S&P total return and CPI for 1947-2025, the real
return averaged about -1.5% a year in years with inflation above 5%, against about 12% under 3%: higher
inflation raises interest rates and the rate future earnings are discounted at, which weighs on valuations.
Fama and Schwert [(1977)](https://doi.org/10.1016/0304-405X(77)90014-9) found US stock returns negatively
related to expected inflation. Here each regime's switching chance is a logit in the inflation level, as in
the time-varying transition probabilities of [Filardo (1994)](https://doi.org/10.1080/07350015.1994.10524545),
so a scenario whose inflation climbs spends more of its time in the turbulent regime.

The ticker's own history (SPY from 1993) holds almost no high-inflation years, so the slopes come from
`covariate_sensitivity`, normally `LongHistory.fit_equity_inflation_sensitivity()`: the US market since 1946
read through this equity's own regimes. With `regime_means` and `regime_volatilities` from `calibrate()` the
regimes stay exactly the plain fit's and only the intercepts are fitted on the ticker, by the joint estimation
of [Diebold, Lee and Weinbach (1994)](https://doi.org/10.1093/oso/9780198773917.003.0010), so at the inflation
of the ticker's own years it switches as often as `calibrate()` says. Whatever is not given is fitted on the
ticker too.

In a factor set this is `condition_on_inflation: true` with `inflation_name` naming the inflation entry.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.equities.equities_controller import Equities
from financescenarios.factors.inflation.inflation_controller import Inflation
from financescenarios.long_history.long_history_controller import LongHistory

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2000-01-01", benchmark_ticker=None)
inflation = Inflation(toolkit)
inflation.calibrate("united_states_inflation", country="United States")

equities = Equities(toolkit)
plain = equities.calibrate("us_broad", "SPY")
history = LongHistory().fit_equity_inflation_sensitivity(plain.regime_means, plain.regime_volatilities)
equities.calibrate_inflation_tvtp(
    "us_broad",
    "SPY",
    inflation.series("united_states_inflation"),
    inflation.dates("united_states_inflation"),
    covariate_sensitivity=history.tvtp.covariate_sensitivity,
    regime_means=plain.regime_means,
    regime_volatilities=plain.regime_volatilities,
)
```

Which returns (calibrated on 2026-10-17):

| regime | regime_mean | regime_volatility | baseline_log_odds | covariate_sensitivity |
|-------:|------------:|------------------:|:------------------|:----------------------|
| 0 | -0.0144 | 0.1965 | [0.0, -2.2374] | [0.0, -4.4912] |
| 1 | 0.1715 | 0.0816 | [0.0, 3.5545] | [0.0, -40.3134] |

In the calm regime (row 1) the chance of turning turbulent is 7.5% a month at 2.6% inflation, the average of
SPY's own years, and 42% at 8%, while a turbulent month stays turbulent with 91% to 93%. At 8% inflation the
market spends about 86% of its time in the turbulent regime instead of 47%; read through the same regimes, the
US market was turbulent in 74% of the months since 1946 with inflation above 6%, against 40% under 3%.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_inflation_tvtp(
    name: str,
    ticker: str,
    inflation: pl.Series,
    inflation_dates: pl.Series,
    covariate_sensitivity: list[list[float]] | None = None,
    regime_means: list[float] | None = None,
    regime_volatilities: list[float] | None = None,
    n_regimes: int = 2,
    period: str = 'monthly',
) -> RegimeParams
```

**Args:**

- <u>name (str):</u> the equity's name in the scenarios.
- <u>ticker (str):</u> the ticker to fit, as in `calibrate()`.
- <u>inflation (pl.Series):</u> the inflation entry's history, year over year as decimals, e.g. `Inflation.series()`.
- <u>inflation_dates (pl.Series):</u> the dates of those values, e.g. `Inflation.dates()`.
- <u>covariate_sensitivity (list[list[float]] &#124; None):</u> the slopes to hold fixed, n_regimes x n_regimes. Defaults to None, fitted on the ticker.
- <u>regime_means (list[float] &#124; None):</u> annual regime means to hold fixed, lowest first. Defaults to None.
- <u>regime_volatilities (list[float] &#124; None):</u> annual regime volatilities to hold fixed, with `regime_means`. Defaults to None.
- <u>n_regimes (int):</u> the number of regimes, at least 2. Defaults to 2.
- <u>period (str):</u> the price frequency, as in `calibrate()`. Defaults to "monthly".

**Returns:**

<u>RegimeParams:</u> the regime fit, with `tvtp` holding `baseline_log_odds` and `covariate_sensitivity`, one row per starting regime.

**Raises:**

- <u>ValueError:</u> if `period`, `n_regimes` or `ticker` is invalid, too few prices line up with the inflation history by date, or a regime has too few observations to fit.

</details>

#### Equities.calibrate_on_regime_history

Calibrate one equity whose calm and turbulent regimes come from a long index of its market, at the ticker's
own average return and volatility.

A fund with twenty years of prices has lived through two or three bear markets, which is too few to say how
often they come and how long they last: fitted on 2000-2026, SPY spends 47% of its time in its turbulent
regime, against 17% for Ken French's US market since 1926. Here the switching chances and the long-run share
of each regime come from the index, held fixed, and each regime's mean and volatility are Hardy's (2001) model
fitted on the fund's own returns by maximum likelihood under that switching (see
`fit_regimes_with_index_switching`). The level and size of the swings are the fund's; the rhythm of crises is
the market's long one.

In a factor set this is `regime_history`, e.g. `regime_history: us_small_caps` on IWM; the index fits come
from `LongHistory.fit_regime_history()`. With `condition_on_inflation` as well, `index_params` is the index's
history read with switching that follows inflation (`LongHistory.fit_equity_inflation_sensitivity()` through
the index's regimes), and each of the fund's months switches at that month's inflation.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.equities.equities_controller import Equities
from financescenarios.long_history.long_history_controller import LongHistory

toolkit = Toolkit(["IWM"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2000-01-01", benchmark_ticker=None)
equities = Equities(toolkit)

small_caps = LongHistory().fit_regime_history("us_small_caps")
equities.calibrate_on_regime_history("small_cap", "IWM", small_caps)
```

Which returns (calibrated on 2026-10-19):

| regime | regime_mean | regime_volatility | chance of staying | long-run share |
|-------:|------------:|------------------:|------------------:|---------------:|
| 0 | -0.0875 | 0.2749 | 0.8913 | 0.2237 |
| 1 | 0.1525 | 0.1529 | 0.9687 | 0.7763 |

Read on Ken French's small caps since 1926, the turbulent regime takes 22% of the time and lasts about nine
months, against 33% and six months in IWM's own fit since 2000; IWM's own returns (7.9% a year at 20%
volatility) set each regime's level and swings: 27% volatility in turbulent months, 15% in calm ones.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_on_regime_history(
    name: str,
    ticker: str,
    index_params: RegimeParams,
    period: str = 'monthly',
    inflation: pl.Series | None = None,
    inflation_dates: pl.Series | None = None,
) -> RegimeParams
```

**Args:**

- <u>name (str):</u> the equity's name in the scenarios.
- <u>ticker (str):</u> the ticker, as in `calibrate()`.
- <u>index_params (RegimeParams):</u> the regime fit on the long index, normally `LongHistory.fit_regime_history()`.
- <u>period (str):</u> the price frequency, which must be the index's ("monthly"). Defaults to "monthly".
- <u>inflation (pl.Series &#124; None):</u> with switching that follows inflation, the inflation entry's history, e.g. `Inflation.series()`, averaged over the ticker's months. Defaults to None.
- <u>inflation_dates (pl.Series &#124; None):</u> the dates of those values, e.g. `Inflation.dates()`. Defaults to None.

**Returns:**

<u>RegimeParams:</u> the index's switching chances and long-run shares, with regime means and volatilities scaled to the ticker, today's most likely regime and the last price.

**Raises:**

- <u>ValueError:</u> if `period` is not recognized or differs from the index's, the ticker has too few prices, or switching that follows inflation comes without the inflation history.

</details>

#### Equities.calibrate_hibbert_regime_switching

Calibrate one equity on its return above a short interest rate, as in the Barrie & Hibbert model of
[Hibbert, Mowbray and Turnbull (2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf).

The fit is the same as in `calibrate()`, but on the extra return stocks earn over cash (the equity risk premium):
each period's log-return minus the short rate times the period length. When simulating, the paired interest rate's
simulated level is added back each step, so higher rates mean higher expected equity returns, while the premium on
top keeps its own calm and turbulent regimes.

In a factor set this is `method: hibbert_regime_switching`, with `nominal_rate_name` naming the interest rate; it
has no risk-neutral version.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.equities.equities_controller import Equities
from financescenarios.factors.interest_rates.interest_rates_controller import InterestRates

toolkit = Toolkit(
    ["SPY", "^IRX"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2005-01-01", benchmark_ticker=None
)
rates = InterestRates(toolkit)
rates.calibrate("us_short_rate", ticker="^IRX", period="monthly")

equities = Equities(toolkit)
equities.calibrate_hibbert_regime_switching(
    "us_premium", "SPY", rates.series("us_short_rate"), period="monthly"
)
```

Which returns (calibrated on 2026-10-04):

| regime | regime_mean | regime_volatility | chance of staying | long-run share |
|-------:|------------:|------------------:|------------------:|---------------:|
| 0 | -0.0149 | 0.2016 | 0.8735 | 0.4389 |
| 1 | 0.1651 | 0.0799 | 0.9010 | 0.5611 |

Against the 13-week Treasury bill, the S&P 500's calm regime earns 16.5% a year above cash and its turbulent
regime 1.5% below it.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_hibbert_regime_switching(
    name: str,
    ticker: str,
    risk_free_rate: pl.Series,
    n_regimes: int = 2,
    period: str = 'monthly',
) -> RegimeParams
```

**Args:**

- <u>name (str):</u> the equity's name in the scenarios.
- <u>ticker (str):</u> the ticker to fit, as in `calibrate()`.
- <u>risk_free_rate (pl.Series):</u> the paired interest rate's historical levels (annual, as decimals), e.g. `InterestRates.series(name)`, sampled at the same `period` as the prices.
- <u>n_regimes (int):</u> the number of regimes, at least 2. Defaults to 2.
- <u>period (str):</u> the price frequency, as in `calibrate()`. Defaults to "monthly".

**Returns:**

<u>RegimeParams:</u> the regime fit, with `regime_means` as annual returns above the short rate.

**Raises:**

- <u>ValueError:</u> if `period`, `n_regimes` or `ticker` is invalid, there are fewer than `n_regimes * 5` prices, or a regime ends up with almost no observations.

</details>

#### Equities.calibrate_risk_neutral

Calibrate one equity for pricing rather than forecasting: a constant volatility and a drift of the risk-free rate
minus the dividend yield, as in Black and Scholes [(1973)](https://doi.org/10.1086/260062) and Merton
[(1973)](https://doi.org/10.2307/3003143).

`calibrate()` forecasts how the market will behave, with an equity risk premium and regimes; this matches today's
market prices instead. Every path is expected to earn the risk-free rate, so discounted scenario values
reproduce today's prices and an option or guarantee valued on them has its market-consistent value, as a
Solvency II best estimate or an IFRS 17 fulfillment value requires. The price follows
`d(log S) = (r - q - 0.5 * sigma^2) dt + sigma dW`, with `r` the risk-free rate, `q` the dividend yield and
`sigma` the volatility.

`volatility_source` picks `sigma`:

- `"implied"`: the options market's at-the-money volatility at one expiration, the average of the
  out-of-the-money call and put nearest today's price.
- `"svi"`: the at-the-money point of the Finance Toolkit's smoothed volatility surface
  at the longest expiration; [Gatheral and Jacquier (2014, section 5)](https://doi.org/10.1080/14697688.2013.819986)
  calibrate the widely used SVI parameterization of the implied volatility smile so that it is free of static
  arbitrage.
- `"realized"`: the ticker's own historical volatility, for tickers without liquid options.

The first two fall back to `"realized"`, with a warning, without options data; `calibrate_heston` lets the
volatility itself move. Whichever is chosen is held flat for the whole horizon. `"implied"` reads the first
expiry at least a week out, so for guarantees running many years `"svi"`, at the longest expiry, is the closer
match (a judgement: one-month and one-year volatilities can differ by several points).

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.equities.equities_controller import Equities

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2005-01-01", benchmark_ticker=None)
equities = Equities(toolkit)

runs = [("implied", "2026-12-18"), ("svi", None), ("realized", None)]
for source, expiration in runs:
    equities.calibrate_risk_neutral(
        f"spy_{source}_{expiration}", "SPY", risk_free_rate=0.0399, dividend_yield=0.0115,
        volatility_source=source, expiration_date=expiration,
    )
```

Which returns (calibrated on 2026-10-04):

| volatility_source | drift | volatility |
|:------------------|------:|-----------:|
| implied | 0.0284 | 0.1426 |
| svi | 0.0284 | 0.1349 |
| realized | 0.0284 | 0.1486 |

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_risk_neutral(
    name: str,
    ticker: str,
    risk_free_rate: float,
    dividend_yield: float,
    volatility_source: str = 'implied',
    expiration_date: str | None = None,
    period: str = 'monthly',
) -> FXParams
```

**Args:**

- <u>name (str):</u> the equity's name in the scenarios.
- <u>ticker (str):</u> the ticker, such as "SPY".
- <u>risk_free_rate (float):</u> today's annual risk-free rate, as a decimal (0.04 is 4%).
- <u>dividend_yield (float):</u> today's annual dividend yield, as a decimal.
- <u>volatility_source (str):</u> "implied", "svi" or "realized". Defaults to "implied".
- <u>expiration_date (str &#124; None):</u> the option expiration for "implied". Defaults to None, the first one at least a week away.
- <u>period (str):</u> the price frequency, as in `calibrate()`. Defaults to "monthly".

**Returns:**

<u>FXParams:</u> `drift` (risk-free rate minus dividend yield), `volatility` and `initial_value` (today's price).

**Raises:**

- <u>ValueError:</u> if `volatility_source` or `period` is not recognized, or a rate is not a finite number.

</details>

#### Equities.calibrate_derived

Set up an equity price derived from dividends, as in Wilkie
[(1986)](https://doi.org/10.1017/S0071368600009009):
the price is the dividend index divided by the dividend yield, both already calibrated as their own factors.

A dividend yield is the yearly dividend divided by the price, so the price is the dividend divided by the yield.
Wilkie's model simulates dividends and yields, and the price follows from them: when dividends grow or yields
fall, the price rises. There is no data fetch, no fit and no separate equity shock; the starting price is
`P(0) = D(0) / Y(0)`. It is the last link of Wilkie's cascade, where inflation drives the dividend yield and
dividend growth, which in turn give the price.

In a factor set this is `method: wilkie_derived` with `dividend_growth_name` and `dividend_yield_name`; `ticker`,
`n_regimes` and `period` are ignored, and beliefs and `measure: risk_neutral` are not allowed.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.dividend_growth.dividend_growth_controller import DividendGrowth
from financescenarios.factors.dividend_yield.dividend_yield_controller import DividendYield
from financescenarios.factors.dividend_yield.dividend_yield_model import reconstruct_dividend_yield_residuals
from financescenarios.factors.equities.equities_controller import Equities
from financescenarios.factors.inflation.inflation_controller import Inflation

toolkit = Toolkit(
    ["JNJ"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1995-01-01", end_date="2019-12-31",
    benchmark_ticker=None,
)
inflation = Inflation(toolkit)
inflation.calibrate("inflation", country="United States", period="monthly", method="wilkie_ar1")
dividend_yield = DividendYield(toolkit)
yield_params = dividend_yield.calibrate("dividend_yield", ticker="JNJ", period="monthly")
yield_residual = reconstruct_dividend_yield_residuals(
    dividend_yield.series("dividend_yield"), yield_params, dividend_yield.time_step("dividend_yield")
)
dividend_growth = DividendGrowth(toolkit)
growth_params = dividend_growth.calibrate(
    "dividend_growth", inflation.series("inflation"), yield_residual, ticker="JNJ", period="monthly"
)

equities = Equities(toolkit)
equities.calibrate_derived(
    "equity",
    dividend_growth_changes=dividend_growth.changes("dividend_growth"),
    dividend_growth_initial_value=growth_params.initial_value,
    dividend_yield_changes=dividend_yield.changes("dividend_yield"),
    dividend_yield_initial_value=yield_params.initial_value,
)
```

Which returns (calibrated on 2026-10-04):

| dividend index D(0) | dividend yield Y(0) | initial_value P(0) |
|--------------------:|--------------------:|-------------------:|
| 3.75 | 0.0263 | 142.47 |

Johnson & Johnson's $3.75 dividend at a 2.63% yield gives a starting price of $142.47 at the end of 2019, close to
its actual closing price of $145.87.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_derived(
    name: str,
    dividend_growth_changes: pl.DataFrame,
    dividend_growth_initial_value: float,
    dividend_yield_changes: pl.DataFrame,
    dividend_yield_initial_value: float,
) -> EquityDerivedParams
```

**Args:**

- <u>name (str):</u> the equity's name in the scenarios.
- <u>dividend_growth_changes (pl.DataFrame):</u> the dividend growth entry's `changes()` output (`date` and `value`).
- <u>dividend_growth_initial_value (float):</u> that entry's calibrated `initial_value`, the dividend index D(0).
- <u>dividend_yield_changes (pl.DataFrame):</u> the dividend yield entry's `changes()` output (`date` and `value`).
- <u>dividend_yield_initial_value (float):</u> that entry's calibrated `initial_value`, the yield Y(0).

**Returns:**

<u>EquityDerivedParams:</u> `initial_value`, the starting price D(0) / Y(0).

</details>

#### Equities.calibrate_heston

Calibrate one equity for pricing with the Heston [(1993)](https://doi.org/10.1093/rfs/6.2.327) model, in which the
volatility itself moves, fitted to today's option prices.

A flat volatility treats a 20% fall and a 20% rise as equally likely and every horizon as equally uncertain.
Option prices disagree: crash protection costs more than a bet on a rally (the skew), and a year's volatility
differs from a month's (the term structure). Heston's variance moves, returns to a long-run level and rises when
prices fall, which reproduces both, so an option valued on these paths prices close to the market's own quote.

The fit uses the Finance Toolkit's smoothed volatility surface at the expirations nearest 1, 2, 3, 6, 9 and 12
months, on strikes within 20% of today's price; the drift is as in `calibrate_risk_neutral`. Paths use the
quadratic-exponential scheme with martingale correction of [Andersen (2008)](https://doi.org/10.21314/jcf.2008.189),
which reproduces the closed-form prices at a monthly step (`HestonStepper`). Without
usable options data this falls back to `calibrate_risk_neutral` with `volatility_source="realized"` and logs a
warning.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.equities.equities_controller import Equities

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", benchmark_ticker=None)
params = Equities(toolkit).calibrate_heston("spy", "SPY", risk_free_rate=0.0399, dividend_yield=0.0115)
```

Which returns (calibrated on 2026-10-07 on 545 quotes):

| Field | Value |
|:------|------:|
| drift | 0.0284 |
| initial_variance | 0.0201 |
| mean_reversion_speed | 14.62 |
| long_run_variance | 0.0219 |
| volatility_of_variance | 1.18 |
| correlation | -0.51 |
| initial_value | 779.09 |
| fit_error | 0.0050 |

Today's volatility is 14.2% (the square root of 0.0201), the long-run level 14.8%, and the -0.51 correlation is
the skew.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_heston(
    name: str,
    ticker: str,
    risk_free_rate: float,
    dividend_yield: float,
    period: str = 'monthly',
) -> HestonParams | FXParams
```

**Args:**

- <u>name (str):</u> the equity's name in the scenarios.
- <u>ticker (str):</u> the ticker whose options to fit; it needs a liquid options market, such as SPY.
- <u>risk_free_rate (float):</u> today's risk-free rate, annual, as a decimal.
- <u>dividend_yield (float):</u> today's dividend yield, annual, as a decimal.
- <u>period (str):</u> the frequency of the price history behind `changes()` and the fallback. Defaults to "monthly".

**Returns:**

<u>HestonParams &#124; FXParams:</u> the Heston fit, or the flat-volatility fallback.

**Raises:**

- <u>ValueError:</u> if `period` is not recognized or a rate is not a finite number.

</details>

#### Equities.names

The names of every equity calibrated so far, in calibration order.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
equities.names  # property -> list[str]
```

</details>

#### Equities.params

The calibrated parameters for one equity: `RegimeParams` for a regime fit, `FXParams` for a risk-neutral one,
`HestonParams` for a Heston fit and `EquityDerivedParams` for a Wilkie-derived one.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
params(name: str) -> RegimeParams | FXParams | HestonParams | EquityDerivedParams
```

**Args:**

- <u>name (str):</u> the equity's name, as passed to a `calibrate` method.

**Raises:**

- <u>RuntimeError:</u> if no `calibrate` method has been called for `name` yet.

</details>

#### Equities.step_function

The price step of the regime-switching lognormal model: a lognormal move with the current regime's mean and
volatility.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
equities.step_function  # property
```

</details>

#### Equities.changes

The historical log-returns of one equity, by date, from which its correlations with the other factors are
estimated.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
changes(name: str) -> pl.DataFrame
```

**Args:**

- <u>name (str):</u> the equity's name, as passed to a `calibrate` method.

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if no `calibrate` method has been called for `name` yet.

</details>

### FX

Simulate exchange rates: how many units of a foreign currency one US dollar buys, such as euros, yen or pounds per
dollar, for valuing foreign assets and liabilities or reporting in another currency.

Each currency pair is correlated with the other factors, so a scenario where US equities fall can also be one
where the dollar strengthens, as it tends to in a flight to safety. FX is opt-in: `fx` is empty by default.

The model is a geometric Brownian motion (GBM): a random walk in the logarithm of the rate, so the rate can rise or
fall without limit but never turns negative,

```text
d(log S) = (mu - 0.5 * sigma^2) dt + sigma * dW
```

with `mu` the annual drift and `sigma` the annual volatility. Shocks are permanent, so the range of outcomes keeps
widening with the horizon; this random walk is the standard treatment, surveyed in
[Gorvett (2001)](https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf). The trend is the
assumption that matters most over long horizons, so it has four options:

- `drift_mode: random_walk`, the default: no trend, so the median rate stays at today's level
  as in [Meese and Rogoff (1983)](https://doi.org/10.1016/0022-1996(83)90017-X). Barrie & Hibbert's model has
  exchange rates respect purchasing power parity over long horizons in Hibbert, Mowbray and Turnbull (2001,
  section 9.3), so no provider carries a fitted trend forward for decades.
- `drift_mode: historical`: the trend fitted on the calibration window, a currency view.
- `drift_mode: irp`: the drift at every step is the gap between two simulated short rates, foreign minus US (uncovered
  interest rate parity, a real-world view: the higher-rate currency is expected to weaken by about the rate gap).
- `drift_mode: ppp`: purchasing power parity at long horizons. The rate follows the gap between the two currencies'
  simulated inflation, and its real value reverts with a half-life of `ppp_half_life` years, 4 by default, the
  middle of the three to five years the long-horizon studies agree on in
  [Rogoff (1996, section 5.B, p. 656)](https://ideas.repec.org/a/aea/jeclit/v34y1996i2p647-668.html), to its average
  since the calibration window's start (`ppp_anchor: history`, the default, from the two inflation entries' consumer
  price indices) or to today's (`ppp_anchor: today`). The average of 26 years of a real rate that halves a gap in
  four years is known only to within about sigma / (kappa * sqrt(T)) = 0.105 in logs, about as far as the euro and
  the pound sit from it. Over a month or a year the rate still moves as a random walk; over
  decades it stays in the range a real exchange rate keeps instead of widening without limit: at the euro's 9.3%
  volatility since 2000, the log real rate settles at a standard deviation of 0.16, where a random walk's log rate
  reaches 0.51 after 30 years.
- `measure: risk_neutral`: for pricing, the no-arbitrage drift in the dollar measure, the simulated foreign minus US
  short rate plus the variance (Garman and Kohlhagen (1983)); see `calibrate_risk_neutral`.
- `source: gmdb`: the Global Macro Database instead of the OECD, for countries such as Brazil, India or China, yearly
  only.

The data are exchange rates in national currency per US dollar, with no API key needed: by default the rate at the
end of each month, quarter or year from the Bank for International Settlements (`end_of_period: true`). The OECD
and Global Macro Database publish averages over each period instead, which smooth the changes: for a random walk
the changes of averages keep only about two-thirds of the variance, as Working (1960)
shows, https://doi.org/10.2307/1907574. On 2021-2026 monthly data the end-of-month rates give a volatility of 7.4% for
the euro and 10.8% for the yen, against 5.9% and 8.6% from the OECD averages. The Global Macro Database has no
end-of-period series, so there the volatility is scaled up by Working's factor instead; `end_of_period: false`
fits the averages as they are. Use `EA20` for the euro area, as `Germany` has no exchange rate of its own there.
Volatility is always historical, as there is no FX options data.

The `fx[i]` keys of a factor set and their defaults are listed under
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/configuration#configuration-classes).

`beliefs.drift` cannot be combined with `drift_mode: irp` or `ppp`, and no belief with `measure: risk_neutral`, which
also takes no `ppp`. In a regime YAML, address one entry with a dotted `"fx.<name>"` key.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
FX(toolkit: Toolkit)
```

</details>

#### FX.calibrate

Calibrate one currency pair from its history: fetch the US dollar exchange rate against `country`'s currency and
fit its annual drift and volatility.

A volatility of 0.07 means a typical year moves the rate by about 7% either way; a drift near 0 means no built-in
tendency for the dollar to strengthen or weaken. Both are annualized from the historical log-returns; a fitted
drift carries the sample's own dollar cycle forward, and over decades that can dominate a foreign portfolio's
result, which is why the trend is a choice.

`drift_mode` sets the trend: `"random_walk"`, the default, drops it (the median rate stays at today's level, as
the random-walk evidence of Meese and Rogoff (1983) and the long-run parity of Hibbert, Mowbray and Turnbull
(2001) both suggest), `"historical"` fits it, and `"irp"` replaces it each step with the gap between two simulated
short rates, foreign minus US (uncovered interest rate parity: the higher-rate currency is expected to weaken by
the rate gap), named in a factor set by `domestic_rate_name` and `foreign_rate_name`. As the rate is in foreign
currency per dollar, a higher US rate pulls it down. `"ppp"` keeps the random walk's volatility but adds
purchasing power parity at long horizons: the rate follows the two currencies' simulated inflation gap and its
real value reverts with a half-life of `ppp_half_life` years, the three to five years of Rogoff (1996, section
5.B, p. 656), to its average over the same window when `ppp_price_countries` names the two countries whose
consumer price indices (OECD) give the real rate, or to today's otherwise; its parameters are `FXPPPParams`.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.fx.fx_controller import FX

toolkit = Toolkit(["AAPL"])
fx = FX(toolkit)

fx.calibrate("eur", country="EA20", period="monthly")
fx.calibrate("jpy", country="Japan", period="monthly")
fx.calibrate("brl", country="Brazil", period="yearly", source="gmdb")
```

Which returns (calibrated on 2026-10-14):

| name | drift | volatility | initial_value |
|:-----|------:|-----------:|--------------:|
| eur | 0.0027 | 0.0736 | 0.8807 |
| jpy | 0.0058 | 0.1080 | 156.9969 |
| brl | 0.0024 | 0.0696 | 5.5896 |

A dollar buys 0.88 euros, 157.00 yen and 5.59 reais at the latest month- or year-end. Each drift is half the
variance, so the median rate stays flat. With `drift_mode="historical"` the yen would get a 7.1% yearly drift
from the dollar's strong run against it over the Toolkit's default five-year window: carried forward for
decades, a strong currency view that no provider builds in.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(
    name: str,
    country: str = 'EA20',
    period: str = 'monthly',
    source: str = 'oecd',
    drift_mode: str = 'random_walk',
    end_of_period: bool = True,
    ppp_half_life: float = PPP_HALF_LIFE_YEARS,
    ppp_price_countries: tuple[str, str] | None = None,
) -> FXParams
```

**Args:**

- <u>name (str):</u> the pair's name in the simulation and in `params()`/`changes()`, e.g. "eur".
- <u>country (str):</u> the country or currency area paired against the dollar. Defaults to "EA20", the euro area.
- <u>period (str):</u> the data frequency: "monthly", "quarterly" or "yearly" ("yearly" only with `source="gmdb"`). Defaults to "monthly".
- <u>source (str):</u> "oecd" or "gmdb" (Global Macro Database, for non-OECD countries). Defaults to "oecd".
- <u>drift_mode (str):</u> "random_walk", "historical", "irp" or "ppp", as above. Defaults to "random_walk".
- <u>end_of_period (bool):</u> fit on the rate at the end of each period (BIS) rather than its average, or with `source="gmdb"` scale the averages' volatility up by Working's factor. Defaults to True.
- <u>ppp_half_life (float):</u> with `drift_mode="ppp"`, the years for half of a deviation from parity to fade. Defaults to 4.0.
- <u>ppp_price_countries (tuple[str, str] &#124; None):</u> with `drift_mode="ppp"`, the US and the foreign country whose consumer price indices turn the rate into a real rate, e.g. ("United States", "Germany"); its average is the level the real rate reverts to. A country without a price index up to within a year of the last rate warns and reverts to today's real rate instead. Defaults to None, today's real rate.

**Returns:**

<u>FXParams:</u> `drift`, `volatility` and `initial_value` (the last rate, in foreign currency per US dollar).

**Raises:**

- <u>ValueError:</u> if an argument is not recognized, no exchange rate comes back for `country` (such as "Germany" instead of "EA20", or a rate-limited OECD request), the history has fewer than 3 rates or one at or below zero, or `ppp_half_life` is not a positive number.

</details>

#### FX.calibrate_risk_neutral

Calibrate one currency pair for pricing: the drift comes from the two interest rates and the volatility from
history.

A risk-neutral run asks which drift is consistent with today's market prices, so anything priced off the simulated
rate allows no riskless profit (an arbitrage). For a currency pair the two interest rates fix that drift: holding
the higher-rate currency earns more interest, so its forward price must be lower. In the US dollar measure the run
discounts in, the dollar price of one unit of foreign currency grows at the US minus the foreign rate, the drift
of the currency option model of [Garman and Kohlhagen (1983)](https://doi.org/10.1016/S0261-5606(83)80001-1). The
quote here is the other way round, foreign currency per dollar, whose drift is then the foreign minus the US rate
plus the variance: the reciprocal of a lognormal rate gains sigma^2 a year in expectation ([Siegel
(1972)](https://doi.org/10.2307/1880565)). Without that term a euro deposit converted to dollars and discounted at
the US rate would be worth e^(sigma^2 T) of its price, 9% too much after ten years at a 9% volatility. With a
4.25% US rate, a 2% euro rate and a 7.4% volatility, the euros-per-dollar quote drifts down about 1.7% a year.

The drift stored here is today's; in a run each step reads the two simulated short rates at its start
(`step_fx_process_risk_neutral`), so the deposit stays a martingale as the rates move. In a factor set this is
`measure: risk_neutral`, which takes today's levels of the configured United States interest rate and the
interest rate for `country`; both must be configured.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.fx.fx_controller import FX

toolkit = Toolkit(["AAPL"])
fx = FX(toolkit)

fx.calibrate_risk_neutral("eur_q", domestic_rate=0.0425, foreign_rate=0.0200, country="EA20")
```

Which returns (calibrated on 2026-10-14):

| name | drift | volatility | initial_value |
|:-----|------:|-----------:|--------------:|
| eur_q | -0.0171 | 0.0736 | 0.8807 |

The drift is 2.00% - 4.25% + 0.0736^2 = -1.71% a year; volatility and today's rate match `calibrate("eur", ...)`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_risk_neutral(
    name: str,
    domestic_rate: float,
    foreign_rate: float,
    volatility_source: str = 'historical',
    country: str = 'EA20',
    period: str = 'monthly',
    source: str = 'oecd',
    end_of_period: bool = True,
) -> FXParams
```

**Args:**

- <u>name (str):</u> the pair's name in the simulation and in `params()`/`changes()`.
- <u>domestic_rate (float):</u> today's US short rate, annual, as a decimal (0.0425 is 4.25%).
- <u>foreign_rate (float):</u> today's short rate for `country`, annual, as a decimal.
- <u>volatility_source (str):</u> only "historical", as there is no FX options data. Defaults to "historical".
- <u>country (str):</u> the country or currency area, as in `calibrate()`. Defaults to "EA20".
- <u>period (str):</u> the data frequency, as in `calibrate()`. Defaults to "monthly".
- <u>source (str):</u> "oecd" or "gmdb", as in `calibrate()`. Defaults to "oecd".
- <u>end_of_period (bool):</u> fit the volatility on end-of-period rates, as in `calibrate()`. Defaults to True.

**Returns:**

<u>FXParams:</u> `drift` (foreign_rate - domestic_rate + volatility^2), with `volatility` and `initial_value` as in `calibrate()`.

**Raises:**

- <u>ValueError:</u> if `volatility_source`, `period` or `source` is not recognized, a rate is not a finite number, or no exchange rate comes back for `country`.

</details>

#### FX.names

The names of every currency pair calibrated so far, in calibration order.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
fx.names  # property -> list[str]
```

</details>

#### FX.params

The calibrated drift, volatility and starting rate for one currency pair.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
params(name: str) -> FXParams
```

**Args:**

- <u>name (str):</u> the pair's name, as passed to `calibrate()` or `calibrate_risk_neutral()`.

**Raises:**

- <u>RuntimeError:</u> if neither has been called for `name` yet.

</details>

#### FX.step_function

The one-step exchange rate update for a fixed-drift currency pair: geometric Brownian motion.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
fx.step_function  # property
```

</details>

#### FX.changes

The dated period log-changes of one currency pair's exchange rate: the history its correlations with the other
factors are estimated from.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
changes(name: str) -> pl.DataFrame
```

**Args:**

- <u>name (str):</u> the pair's name, as passed to `calibrate()` or `calibrate_risk_neutral()`.

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if neither has been called for `name` yet.

</details>

### Commodities

The Commodities module simulates commodity prices, such as crude oil or gold, as prices that swing widely but are
pulled back toward a normal level over time.

Each entry in `commodities` (an empty list by default) becomes a simulated price path, correlated with the other
factors (oil with inflation and the business cycle, gold often against equities in a sell-off) and usable as a
portfolio holding.

Unlike a stock index, a commodity has a natural price level: storage costs and the convenience yield (the benefit of
holding the physical good, such as keeping a refinery running) pull the spot price back toward what it costs to
produce and store, as [Schwartz (1997)](https://doi.org/10.1111/j.1540-6261.1997.tb02721.x) showed. The default model
(`method="single_factor"`) lets the log price revert to a long-run level:

```text
d(log S) = kappa * (mu - log S) dt + sigma * dW
```

where `kappa` is the speed of the pull, `mu` the long-run log price and `sigma` the volatility. Working in logs keeps
the price positive.

The two-factor model of [Schwartz and Smith (2000)](https://doi.org/10.1287/mnsc.46.7.893.12034)
(`method="schwartz_smith"`) writes the log price as `chi + xi`: a short-term deviation that fades back to zero plus a
long-term level that drifts as a random walk, the convenience-yield economics of
[Gibson and Schwartz (1990)](https://doi.org/10.1111/j.1540-6261.1990.tb05114.x) in another form. It separates a
temporary shock, such as a supply outage, from a lasting change in costs. The parts are simulated as `{name}_chi` and
`{name}_xi`, the price itself under `name`. With `measure="risk_neutral"` the drifts match today's futures prices
instead.

Gold is held as an asset rather than consumed: a year's mine supply adds about 1.5% to the stock above ground, so a
high price brings out little new metal and nothing pulls it back toward a cost of production ([Erb and Harvey,
2013, pp. 28-29](https://doi.org/10.2469/faj.v69.n4.1)). `method="random_walk"` (`calibrate_random_walk`) models
such a commodity as a random walk in its log price with only its volatility fitted, drifting with a simulated
inflation rate (`inflation_name`) so its median real price stays at today's level: the long-run zero real return
of gold (Erb and Harvey, 2013, p. 11).

Data: the "Adj Close" of any commodity or futures ticker in the `Toolkit` (Yahoo Finance, no API key needed), such as
`CL=F` (WTI crude oil) or `GC=F` (gold). The two-factor model also reads today's futures curve, available for crude
oil, natural gas, gold, silver, copper, corn, wheat and soybeans.

The `commodities[i]` keys of a factor set and their defaults are listed under
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/configuration#configuration-classes).

A belief's `long_run_mean` is a log price: for 70 USD, set `log(70)`, about 4.25.

**References:**

- Schwartz, E.S. (1997). "The Stochastic Behavior of Commodity Prices: Implications for Valuation and Hedging." Journal of Finance, 52(3), 923-973. <https://doi.org/10.1111/j.1540-6261.1997.tb02721.x>
- Gibson, R., Schwartz, E.S. (1990). "Stochastic Convenience Yield and the Pricing of Oil Contingent Claims." Journal of Finance, 45(3), 959-976. <https://doi.org/10.1111/j.1540-6261.1990.tb05114.x>
- Schwartz, E., Smith, J.E. (2000). "Short-Term Variations and Long-Term Dynamics in Commodity Prices." Management Science, 46(7), 893-911. <https://doi.org/10.1287/mnsc.46.7.893.12034>
- Erb, C.B., Harvey, C.R. (2013). "The Golden Dilemma." Financial Analysts Journal, 69(4), 10-42. <https://doi.org/10.2469/faj.v69.n4.1>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Commodities(toolkit: Toolkit)
```

</details>

#### Commodities.calibrate

Calibrate one commodity's single-factor model from its price history.

It fits how fast the log price returns to its normal level (`mean_reversion_speed`), what that level is
(`long_run_mean`) and how much it swings (`volatility`). A speed of 1.37 a year means half of a price spike fades
in about six months (ln 2 / 1.37). `long_run_mean` is a log price, so `exp(long_run_mean)` is the price the
process is pulled toward, while `initial_value` is today's actual price.

The fit regresses each period's change in log price on the previous log price by ordinary least squares, the exact
discrete form of the [Schwartz (1997)](https://doi.org/10.1111/j.1540-6261.1997.tb02721.x) model. A price that
trends rather than settles back, such as gold monthly since 2016, raises an error; over a longer window the same
trend can pass as a slow pull toward a level far above history (gold on daily data since 2000 settles at 24,103
USD), and `calibrate_random_walk` is the model for such a commodity.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.commodities.commodities_controller import Commodities

toolkit = Toolkit(["CL=F", "NG=F"], start_date="2016-01-01")
commodities = Commodities(toolkit)

commodities.calibrate("crude_oil", ticker="CL=F", period="monthly")
commodities.calibrate("natural_gas", ticker="NG=F", period="monthly")
```

Which returns (calibrated on 2026-10-19):

| name | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-----|---------------------:|--------------:|-----------:|--------------:|
| crude_oil | 0.9443 | 4.2115 | 0.4622 | 96.9200 |
| natural_gas | 1.2135 | 1.1296 | 0.5898 | 3.0950 |

Crude oil starts at 96.92 USD and is pulled toward exp(4.2115) = 67.46 USD; without the finite-sample correction
of the speed the pull would be 1.3390 a year. A price far above that level falls on average in the scenarios:
in the default factor set on 2026-10-19, Brent (`BZ=F`, daily since July 2007) started at 108.00 USD against
exp(4.3431) = 76.95 USD with a speed of 0.46 (a half-life of 1.5 years), so its median price falls 5.9% a year
over five years. The futures market priced a steeper fall on 2026-10-17: WTI for November 2026 at 101.41 USD
and for September 2031 at 61.49 USD.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(
    name: str,
    ticker: str = 'CL=F',
    period: str = 'daily',
    volatility_model: str = 'constant',
    business_cycle_covariate: pl.Series | None = None,
    business_cycle_covariate_dates: pl.Series | None = None,
) -> CommodityParams | GARCHParams | OUCovariateParams
```

**Args:**

- <u>name (str):</u> the commodity's name in the output.
- <u>ticker (str):</u> any commodity or futures ticker in the Toolkit. Defaults to "CL=F" (WTI crude).
- <u>period (str):</u> the fit's time step: "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>volatility_model (str):</u> "constant", or "garch" for volatility that clusters as in [Bollerslev (1986)](https://doi.org/10.1016/0304-4076(86)90063-1). Defaults to "constant".
- <u>business_cycle_covariate (pl.Series &#124; None):</u> a leading indicator's history, such as `LeadingIndicator.series`; when given, the price also moves with its change. Defaults to None.
- <u>business_cycle_covariate_dates (pl.Series &#124; None):</u> the dates of `business_cycle_covariate`, required with it. Defaults to None.

**Returns:**

<u>CommodityParams &#124; GARCHParams &#124; OUCovariateParams:</u> `mean_reversion_speed`, `long_run_mean`, `volatility` and `initial_value`, or their GARCH or business-cycle form.

**Raises:**

- <u>ValueError:</u> if an option is not recognised or the covariate is combined with "garch", the ticker has no data, a price is not strictly positive (daily WTI crude closed at -37.63 USD on 2020-04-20) or the price shows no mean reversion.

</details>

#### Commodities.calibrate_random_walk

Calibrate a commodity held as an asset rather than consumed, such as gold, as a random walk in its log price
with no long-run level to return to.

The single-factor model pulls the price back toward a long-run level, the cost of production and storage that
new supply and the convenience yield enforce for oil or copper. Gold has no such pull: a year's mine supply adds
about 1.5% to the stock already above ground, so a higher price brings out little new metal, as [Erb and Harvey
(2013, pp. 28-29)](https://doi.org/10.2469/faj.v69.n4.1) show. Fitted on its history since 2000, the
single-factor model reads gold's 25-year rise as a slow pull toward a level far above anything it has traded at.
Here only the volatility is fitted; the median real price stays at today's level once the entry is linked to an
inflation factor (`inflation_name` in a factor set), the golden constant of a long-run real return of about zero
(Erb and Harvey, 2013, p. 11), and the median price stays at today's level without one.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.commodities.commodities_controller import Commodities

toolkit = Toolkit(["GC=F"], start_date="2000-01-01")
commodities = Commodities(toolkit)

commodities.calibrate_random_walk("gold", ticker="GC=F", period="monthly")
```

Which returns (calibrated on 2026-10-17):

| name | drift | volatility | initial_value |
|:-----|------:|-----------:|--------------:|
| gold | 0.0137 | 0.1657 | 4181.1001 |

Gold's monthly moves since 2000 give a 16.6% yearly volatility, against 17.9% on daily data and 15.8% from one
year-end to the next, so the monthly fit matches the yearly risk more closely.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_random_walk(
    name: str,
    ticker: str = 'GC=F',
    period: str = 'monthly',
) -> CommodityRandomWalkParams
```

**Args:**

- <u>name (str):</u> the commodity's name in the output.
- <u>ticker (str):</u> any commodity or futures ticker in the Toolkit. Defaults to "GC=F" (gold).
- <u>period (str):</u> the fit's time step: "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "monthly", the run's usual step.

**Returns:**

<u>CommodityRandomWalkParams:</u> `drift` (half the variance, which keeps the median flat), `volatility` and `initial_value`.

**Raises:**

- <u>ValueError:</u> if `period` is not recognised, the ticker has no data, or a price is not strictly positive.

</details>

#### Commodities.calibrate_schwartz_smith

Calibrate one commodity's two-factor Schwartz and Smith model from its price history and today's futures curve.

The log price is split into a short-term deviation `chi` that fades back to zero and a long-term level `xi` that
drifts as a random walk. It separates a temporary dislocation (a refinery outage) from a lasting change in
production costs. The temporary part halves in ln 2 / `chi.mean_reversion_speed` years and today's price is
`exp(chi.initial_value + xi.initial_value)`.

[Schwartz and Smith (2000)](https://doi.org/10.1287/mnsc.46.7.893.12034) estimate the model from years of futures
prices. Only today's curve is available here, so `xi` is a trailing average of the log price and `chi` the rest,
which sets the speed and today's split. The volatilities and their correlation are fitted to the recent swings of
each listed futures contract. When the curve cannot separate the two parts, `xi`'s volatility comes from the
longest contract, whose volatility tends to it as maturity grows (Schwartz and Smith, section 3.1), and the
rest from the price history, with a warning. Without any futures curve the price history sets all three,
which understates `xi`'s volatility by more than an order of magnitude.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.commodities.commodities_controller import Commodities

toolkit = Toolkit(["CL=F"], start_date="2021-01-01")
commodities = Commodities(toolkit)

commodities.calibrate_schwartz_smith("oil", ticker="CL=F", period="daily")
```

Which returns (calibrated on 2026-10-14):

| factor | mean_reversion_speed | long_run_mean | drift | volatility | initial_value |
|:-------|---------------------:|--------------:|------:|-----------:|--------------:|
| oil_chi | 2.5872 | 0.0000 | | 0.4162 | 0.2508 |
| oil_xi | | | -0.0246 | 0.1984 | 4.2983 |

Today's 94.55 USD price splits into a long-term level of exp(4.2983) = 73.6 USD and a 29% short-term
premium. The long-term volatility of 19.8% a year compares with 14.5% in Schwartz and Smith's own oil fit.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_schwartz_smith(
    name: str,
    ticker: str = 'CL=F',
    period: str = 'daily',
    contracts: int = 12,
    long_term_window_years: float = 3.0,
) -> SchwartzSmithParams
```

**Args:**

- <u>name (str):</u> the commodity's name; its parts are stored as `{name}_chi` and `{name}_xi`.
- <u>ticker (str):</u> the spot ticker. A futures curve exists for "CL=F", "NG=F", "GC=F", "SI=F", "HG=F", "ZC=F", "ZW=F" and "ZS=F". Defaults to "CL=F".
- <u>period (str):</u> time step of the price history, "daily" to "yearly". Defaults to "daily".
- <u>contracts (int):</u> monthly futures contracts to try to fetch, at least 2. Defaults to 12.
- <u>long_term_window_years (float):</u> years of prices averaged into `xi`. Defaults to 3.0.

**Returns:**

<u>SchwartzSmithParams:</u> `chi` (speed, a long-run mean of 0, volatility, today's value) and `xi` (drift, volatility, today's value).

**Raises:**

- <u>ValueError:</u> if an input is invalid, the price history is too short or not strictly positive, `chi` does not mean-revert, or the futures curve comes back empty.

</details>

#### Commodities.calibrate_schwartz_smith_risk_neutral

Calibrate one commodity's two-factor Schwartz and Smith model so that it reproduces today's futures prices.

Instead of asking how the price has behaved, this asks what path the futures market prices in (the risk-neutral
view). A curve that slopes down (backwardation) gives the long-term level `xi` a negative drift; one that slopes
up (contango), a positive one. Use it for pricing and hedging, not as a forecast.

The speed and volatilities are fitted as in `calibrate_schwartz_smith`, since they are the same under both views.
Only the two drifts are fitted here, by ordinary least squares on the futures pricing formula of
[Schwartz and Smith (2000, eq. 9)](https://doi.org/10.1287/mnsc.46.7.893.12034). This needs a futures curve and
raises without one.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.commodities.commodities_controller import Commodities

toolkit = Toolkit(["CL=F"], start_date="2021-01-01")
commodities = Commodities(toolkit)

commodities.calibrate_schwartz_smith_risk_neutral("oil_q", ticker="CL=F", period="daily")
```

Which returns (calibrated on 2026-10-14):

| factor | mean_reversion_speed | long_run_mean | drift | volatility | initial_value |
|:-------|---------------------:|--------------:|------:|-----------:|--------------:|
| oil_q_chi | 2.5872 | 0.2474 | | 0.4162 | 0.2508 |
| oil_q_xi | | | -0.1850 | 0.1984 | 4.2983 |

Only the drifts differ from the real-world fit. The crude curve that day fell from 94.14 USD (November 2026) to
83.02 USD (September 2027), so the market prices the long-term level falling about 18.5% a year, against 2.5% in
the real-world fit.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_schwartz_smith_risk_neutral(
    name: str,
    ticker: str = 'CL=F',
    period: str = 'daily',
    contracts: int = 12,
    long_term_window_years: float = 3.0,
) -> SchwartzSmithParams
```

**Args:**

- <u>name (str):</u> the commodity's name; its parts are stored as `{name}_chi` and `{name}_xi`.
- <u>ticker (str):</u> a spot ticker with a futures curve: "CL=F", "NG=F", "GC=F", "SI=F", "HG=F", "ZC=F", "ZW=F" or "ZS=F". Defaults to "CL=F".
- <u>period (str):</u> time step of the price history, "daily" to "yearly". Defaults to "daily".
- <u>contracts (int):</u> monthly futures contracts to try to fetch, at least 2. Defaults to 12.
- <u>long_term_window_years (float):</u> years of prices averaged into `xi`. Defaults to 3.0.

**Returns:**

<u>SchwartzSmithParams:</u> the real-world fit, with `chi`'s `long_run_mean` and `xi`'s `drift` set by today's futures prices.

**Raises:**

- <u>ValueError:</u> if an input is invalid, the ticker has no futures curve, the price history fails the real-world fit, or fewer than 2 futures contracts have a price today.

</details>

#### Commodities.names

The names of every commodity calibrated so far, in calibration order; a two-factor entry is listed as its `_chi`
and `_xi` parts.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
commodities.names  # property -> list[str]
```

</details>

#### Commodities.params

The calibrated parameters of one commodity, or of one `_chi` or `_xi` part of a two-factor entry.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
params(
    name: str,
) -> CommodityParams | CommodityRandomWalkParams | OUParams | RandomWalkParams | GARCHParams | OUCovariateParams
```

**Args:**

- <u>name (str):</u> the name as calibrated, e.g. "crude_oil" or "oil_chi".

**Raises:**

- <u>RuntimeError:</u> if `name` has not been calibrated yet.

</details>

#### Commodities.step_function

The one-step price update of the single-factor model: the exact mean-reverting step on the log price.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
commodities.step_function  # property
```

</details>

#### Commodities.changes

The dated period-to-period changes in one commodity's log price (or its `_chi` or `_xi` part): the history its
correlations with the other factors are estimated from.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
changes(name: str) -> pl.DataFrame
```

**Args:**

- <u>name (str):</u> the name as calibrated, e.g. "crude_oil" or "oil_chi".

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if `name` has not been calibrated yet.

</details>

### RealEstate

The Real Estate module simulates the growth rate of property prices: how fast house prices (or commercial property
prices) rise or fall each year. Property booms and busts tend to fade back toward a normal growth rate over a few
years, and that is the behavior this module captures. Growth can turn negative, so price slumps such as 2008 are
in the scenario set, and because growth is persistent, a slump lasts several years rather than one bad quarter.

Enable it and every simulated scenario gets a property-price growth path, linked to interest rates, inflation,
equities and the rest through the correlation matrix, so a portfolio or liability that holds property can be put
through the same scenarios. It is opt-in (`real_estate.enabled`, `false` in a bare config), though the shipped
`default.yaml` and `broad.yaml` factor sets turn it on for the United States.

The model is a mean-reverting (Ornstein-Uhlenbeck) process on the growth rate:

```text
d(re) = a * (theta - re) * dt + sigma * dW
```

Growth is pulled toward a normal level `theta` at speed `a`, with random swings of size `sigma`. It is the real estate
process of the
[Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf)
scenario generator (their eq. 3.18), which fits two separate Ornstein-Uhlenbeck models to quarterly NCREIF returns
from 1978 to 2001 (section 3, Real Estate (Property)). The growth rate is
modelled rather than the price index, because an index level has no normal level to return to over decades, while
its growth rate does. Where the paper fits quarterly returns, this fits year-over-year growth sampled each quarter,
so residential and commercial read on one scale (a judgement; FRED publishes commercial prices only as Percent
Change from Year Ago). Consecutive year-over-year readings share three of their four quarters, so a
quarter-to-quarter regression would read that overlap as slow reversion; each value is regressed on the value a
year earlier instead, as the paper does for inflation, where noisy monthly data led the authors to select the
parameters from annual regressions (section 3).
`volatility_model: garch` lets the size of the swings vary over time
as in [Bollerslev (1986)](https://doi.org/10.1016/0304-4076(86)90063-1), and `condition_on_business_cycle` adds a pull
from the leading indicator, so property growth tends to slow as the economy does; the two cannot be combined.
`condition_on_interest_rate` slows each scenario's growth in the year after its own long rate rises, with a
sensitivity fitted on the OECD's history since 1971 (`calibrate_rate_link`).

Two data sources (`source`), both through the Finance Toolkit and both as year-over-year growth (0.04 is 4% a year):

- `house_price` (default): the OECD residential house-price index for `country`, quarterly or yearly, no API
  key.
- `commercial`: FRED's US Commercial Real Estate Prices
  ([COMREPUSQ159N](https://fred.stlouisfed.org/series/COMREPUSQ159N), from the IMF), published as Percent Change
  from Year Ago. United States and quarterly only, and it needs a FRED API key.

Neither is the appraisal-based NCREIF index the paper was calibrated on, which has no open equivalent.

The `real_estate` keys of a factor set and their defaults are listed under
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/configuration#configuration-classes).

**References:**

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Uhlenbeck, G.E., Ornstein, L.S. (1930). "On the Theory of the Brownian Motion." Physical Review, 36(5), 823-841. <https://doi.org/10.1103/PhysRev.36.823>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
RealEstate(toolkit: Toolkit)
```

</details>

#### RealEstate.calibrate

Calibrate the real estate growth process: fetch the house-price (or commercial property price) growth series, then
fit how fast growth returns to its normal rate (`mean_reversion_speed`), what that rate is (`long_run_mean`) and
how much it swings (`volatility`).

This learns how property price growth has behaved, so the simulated scenarios boom and cool the way the real
market has. A speed of 0.5 a year means a boom has faded by half after about 1.4 years (ln 2 / 0.5). All values
are annualized decimals: a `long_run_mean` of 0.04 is 4% growth a year, and `initial_value` is the latest growth
rate, where every simulated path starts. Give the Toolkit an early `start_date`: its default window is too short
for a stable fit.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.real_estate.real_estate_controller import RealEstate

toolkit = Toolkit(
    ["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", fred_api_key="FRED_KEY", start_date="2000-01-01"
)
real_estate = RealEstate(toolkit)

real_estate.calibrate(country="United States", period="quarterly")
real_estate.calibrate(source="commercial", period="quarterly")
```

Which returns (calibrated on 2026-10-14):

| source | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-------|---------------------:|--------------:|-----------:|--------------:|
| house_price | 0.3689 | 0.0429 | 0.0492 | 0.0214 |
| commercial | 1.8231 | 0.0535 | 0.1064 | 0.0224 |

US house prices are 2.1% higher than a year ago and are pulled toward 4.3% a year, a slump fading by half in about
1.9 years; commercial prices revert within about five months. The quarter-to-quarter fit (`ou_fit="step"`) gives
house prices a speed of 0.1221, a half-life of 5.7 years, because it reads the overlap of year-over-year
readings as persistence; both fits give growth the same long-run spread, about 5.7%.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(
    country: str = 'United States',
    period: str = 'quarterly',
    volatility_model: str = 'constant',
    source: str = 'house_price',
    business_cycle_covariate: pl.Series | None = None,
    business_cycle_covariate_dates: pl.Series | None = None,
    ou_fit: str = 'year_apart',
) -> OUParams | GARCHParams | OUCovariateParams
```

**Args:**

- <u>country (str):</u> the house-price country; "United States" for "commercial". Defaults to "United States".
- <u>period (str):</u> "quarterly" or "yearly"; "commercial" needs "quarterly". Defaults to "quarterly".
- <u>volatility_model (str):</u> "constant" or "garch". Defaults to "constant".
- <u>source (str):</u> "house_price" (OECD) or "commercial" (FRED, key needed). Defaults to "house_price".
- <u>business_cycle_covariate (pl.Series &#124; None):</u> leading indicator history to condition on. Defaults to None.
- <u>business_cycle_covariate_dates (pl.Series &#124; None):</u> its dates, needed with it. Defaults to None.
- <u>ou_fit (str):</u> "year_apart" (default) reads persistence from values a year apart; "step" from neighbouring quarters, which reads their overlap as slow reversion (the fit before October 2026).

**Returns:**

<u>OUParams &#124; GARCHParams &#124; OUCovariateParams:</u> the fitted process; GARCHParams with "garch", OUCovariateParams with a covariate.

**Raises:**

- <u>ValueError:</u> if an option is not recognized or not allowed with "commercial", "garch" is combined with a covariate, or no data come back (an unsupported country, a missing FRED key or an OECD rate limit).

</details>

#### RealEstate.calibrate_history

Refit how fast house-price growth returns to normal and how much it swings on the OECD's history since 1971,
so one boom and bust cannot set the size of every scenario's swings; today's growth and normal rate stay.

Fitted on the window since 2000, house-price growth takes its swings from the 2006-2011 bust and the 2021 boom,
the two largest moves in the US series: its yearly shock comes out at 4.1% against 3.2% over 1971-2025, and
about a quarter of 30-year scenarios lose more than 20% of their price index within a decade, which the US
did once, from 2006 to 2011. Fitted on every quarter since 1971 with the same year-apart regression
(`fit_year_apart_ou_process`, the annual regressions of
[Ahlgrim, D'Arcy and Gorvett (2005, section 3)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf)),
growth keeps its momentum, 71% of a gap left after a year (a year of rising prices tends to be followed by
another, as [Case and Shiller (1988, Table 2, p. 9)](https://doi.org/10.3386/w2506) find for US cities), with
swings that match five decades rather than two. The normal growth rate stays the recent window's: nominal
growth since 1971 averages 5.4% because consumer prices rose 3.9% a year against 2.6% since 2000, while real
growth was 1.5% against 2.2%.

With `regimes`, growth's shocks switch between a calm and a turbulent regime fitted on the quarter-on-quarter
growth of the same index (`fit_volatility_regimes`): on 1971-2026 the quarterly shocks are 0.24% in calm
stretches and 1.02% in turbulent ones, which last about six and eight years on average, so bust years such as
2008 get a real chance instead of almost none. Two regimes beat one shock size by a log-likelihood of 61, where
99 histories of the same length simulated with one constant size gave at most 4.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.real_estate.real_estate_controller import RealEstate

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2000-01-01")
real_estate = RealEstate(toolkit)

real_estate.calibrate(country="United States", period="quarterly")
real_estate.calibrate_history(country="United States")
```

Which returns (calibrated on 2026-10-17, US data 1971-2026):

| mean_reversion_speed | long_run_mean | volatility | initial_value |
|---------------------:|--------------:|-----------:|--------------:|
| 0.3448 | 0.0429 | 0.0387 | 0.0214 |

Against the window since 2000 (speed 0.3689, volatility 0.0492), a boom fades at about the same pace and the
long-run spread of growth falls from 5.7% to 4.7%, the 4.6% the US has shown since 1971.

**References:**

- Case, K.E., Shiller, R.J. (1988). "The Efficiency of the Market for Single-Family Homes." NBER Working Paper 2506; published in the American Economic Review, 79(1), 125-137 (1989). <https://doi.org/10.3386/w2506>
- Hamilton, J.D. (1989). "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle." Econometrica, 57(2), 357-384. <https://doi.org/10.2307/1912559>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_history(
    country: str = 'United States',
    economics: Economics | None = None,
    regimes: bool = False,
) -> OUParams | RegimeOUParams
```

**Args:**

- <u>country (str):</u> the country of the OECD history. Defaults to "United States".
- <u>economics (Economics &#124; None):</u> a Finance Toolkit `Economics` reaching back to 1970; built on first use.
- <u>regimes (bool):</u> fit calm and turbulent volatility regimes. Defaults to False.

**Returns:**

<u>OUParams &#124; RegimeOUParams:</u> the long-history speed and volatility (or regimes) with the recent window's normal growth and today's growth.

**Raises:**

- <u>RuntimeError:</u> if `calibrate()` has not been called yet.
- <u>ValueError:</u> if the fitted process is not a constant-volatility Ornstein-Uhlenbeck one, or the history is missing, too short or shows no pull toward a normal growth rate.

</details>

#### RealEstate.regime_fit

The calm and turbulent regimes `calibrate_history(regimes=True)` fitted, with their log-likelihood against one
normal shock.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
realestate.regime_fit  # property -> VolatilityRegimeFit
```

**Raises:**

- <u>RuntimeError:</u> if no regimes were fitted.

</details>

#### RealEstate.history_fit

The growth process `calibrate_history` fitted on the long history, its own long-run mean and last value
included, before today's normal rate and starting point were put back.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
realestate.history_fit  # property -> OUParams
```

**Raises:**

- <u>RuntimeError:</u> if no long-history fit was made.

</details>

#### RealEstate.calibrate_rate_link

Fit how much house-price growth slows in the year after long-term interest rates rise, on decades of history,
and build that link into the growth process already fitted with `calibrate`.

On its own the growth process ignores interest rates, so a scenario in which rates climb by three points keeps
the same housing market as one in which they fall, while in history dearer mortgages cooled house prices within
a year or two, as in 1980-1982, 2006-2008 and 2022-2023. With this link each scenario's house-price growth
answers to its own simulated long rate, which mortgage rates follow, a year later.

The sensitivity comes from the OECD's quarterly house-price growth and long-term rate for `country` (from 1971
for the United States, keyless), each quarter's growth regressed on its own value a year earlier and the long
rate's change over the year before, as in `fit_rate_link` and
[Iacoviello (2005)](https://doi.org/10.1257/0002828054201477). The speed, normal growth rate and starting point
stay as `calibrate` fitted them on its window; the volatility gives up the part of growth's yearly moves the link
explains.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.real_estate.real_estate_controller import RealEstate

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2000-01-01")
real_estate = RealEstate(toolkit)

real_estate.calibrate(country="United States", period="quarterly")
real_estate.calibrate_rate_link(country="United States")
```

Which returns (calibrated on 2026-10-17, US data 1973-2026):

| interest_rate_sensitivity | lag | mean_reversion_speed | long_run_mean | volatility |
|--------------------------:|----:|---------------------:|--------------:|-----------:|
| -0.8601 | 1.0 | 0.3689 | 0.0429 | 0.0477 |

A long rate one point higher than a year ago lowers house-price growth by 0.86 points a year later.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_rate_link(
    country: str = 'United States',
    economics: Economics | None = None,
) -> RateLinkedOUParams | RegimeOUParams
```

**Args:**

- <u>country (str):</u> the country of the long history. Defaults to "United States".
- <u>economics (Economics &#124; None):</u> a Finance Toolkit `Economics` reaching back to 1970; built on first use.

**Returns:**

<u>RateLinkedOUParams:</u> the growth process with `interest_rate_sensitivity` and `lag`.

**Raises:**

- <u>RuntimeError:</u> if `calibrate()` has not been called yet.
- <u>ValueError:</u> if the fitted process is not a constant-volatility Ornstein-Uhlenbeck one (not GARCH or conditioned on the business cycle), or the history is missing or too short.

</details>

#### RealEstate.rate_link_fit

The rate link fitted by `calibrate_rate_link`: the sensitivity, its standard error, the share of growth's
yearly moves it explains and the dates used.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
realestate.rate_link_fit  # property -> RateLinkFit
```

**Raises:**

- <u>RuntimeError:</u> if no rate link was fitted.

</details>

#### RealEstate.params

The calibrated growth process: reversion speed, normal growth rate, volatility and today's growth rate.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
realestate.params  # property -> OUParams | GARCHParams | OUCovariateParams | RateLinkedOUParams | RegimeOUParams
```

**Raises:**

- <u>RuntimeError:</u> if `calibrate()` has not been called yet.

</details>

#### RealEstate.step_function

The one-step update of the growth rate: an exact Ornstein-Uhlenbeck step.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
realestate.step_function  # property
```

</details>

#### RealEstate.rate_linked_step_function

The one-step update of rate-linked growth: the exact step plus the long rate's push a year earlier.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
realestate.rate_linked_step_function  # property
```

</details>

#### RealEstate.changes

Dated period-over-period changes of the growth rate: the history its correlations with the other factors are
estimated from.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
realestate.changes  # property -> pl.DataFrame
```

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if `calibrate()` has not been called yet.

</details>

### DividendYield

Simulate the dividend yield of a stock or fund: the dividends it paid over the past year divided by its current
price.

A yield rises when prices fall or payouts grow, and over long stretches it drifts back toward a typical level: a
market priced cheaply against its dividends tends to re-rate, a dear one to cheapen. Simulating the yield gives
dividend income its own path, which matters for pension and income planning, and, in the Wilkie model, it is half
of what sets the equity price. Each entry, such as SPY, is linked to the other factors through the correlation
matrix.

The model comes from Ahlgrim, D'Arcy and Gorvett
([2005](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf)) (eq. 3.17): the log yield is
pulled back toward a normal level,

```text
d(log y) = kappa * (mu - log y) * dt + sigma * dW
```

where `kappa` is the speed of the pull, `exp(mu)` the normal yield and `sigma` the size of the swings. Working in logs
keeps the yield positive and makes its swings proportional to its level, so a 1% yield moves less in absolute terms
than a 5% one. The pull is slow: the authors find a mean reversion speed not significantly different from
zero, so yields can stay far from normal for years. A history with no pull at all raises an error.

Three options change the model; only one can be used at a time:

- `condition_on_inflation` adds the inflation term of Wilkie (1986): the yield also moves with a named inflation
  entry, so higher inflation pushes yields up and prices down. It is the dividend yield of the Wilkie model (the
  `wilkie` factor set) that `DividendGrowth` builds on.
- `volatility_model="garch"` lets the size of the swings vary over time, so calm and volatile spells each persist,
  as in [Bollerslev (1986)](https://doi.org/10.1016/0304-4076(86)90063-1).
- `condition_on_business_cycle` makes the yield move with the leading indicator (requires
  `leading_indicator.enabled: true`).

Data: the dividends paid over the trailing `window` trading days divided by the unadjusted closing price, from the
Finance Toolkit. A ticker that pays no dividends raises an error. Use Yahoo Finance (no API key): the Financial
Modeling Prep Free plan returns only the last five payments, too few for a trailing-year yield.

The `dividend_yield[i]` keys of a factor set and their defaults are listed under
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/configuration#configuration-classes).

A belief's `long_run_mean` is a log yield: a 2% target is `log(0.02)`, about -3.9.

**References:**

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92, eq. 3.17. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://doi.org/10.1017/S0071368600009009>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
DividendYield(toolkit: Toolkit)
```

</details>

#### DividendYield.calibrate

Calibrate one ticker's dividend yield: how fast its logarithm returns to a normal level (`mean_reversion_speed`),
that level (`long_run_mean`) and how much it swings (`volatility`).

A speed of 0.15 a year halves a gap from the normal level in about 4.6 years (ln 2 / 0.15), so scenarios that
start from an unusually low yield, as today's US market does, drift back up only slowly: yield, and with it
dividend income per unit invested, stays low for years. `exp(long_run_mean)` is the normal yield and
`initial_value` today's yield (0.0099 is 0.99%).

Each day's yield is the dividends of the last `window` trading days divided by that day's price, averaged per
`period`; the log yield is then fitted by ordinary least squares, following Ahlgrim, D'Arcy and Gorvett
([2005](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf)). Without mean reversion
it raises; a longer history or a coarser `period` usually helps.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.dividend_yield.dividend_yield_controller import DividendYield

toolkit = Toolkit(["SPY", "JNJ"], start_date="1995-01-01", benchmark_ticker=None)
dividend_yield = DividendYield(toolkit)

dividend_yield.calibrate("spy_yield", ticker="SPY", period="monthly")
dividend_yield.calibrate("jnj_yield", ticker="JNJ", period="monthly")
```

Which returns (calibrated on 2026-10-04):

| name | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-----|---------------------:|--------------:|-----------:|--------------:|
| spy_yield | 0.1481 | -4.2784 | 0.1525 | 0.0099 |
| jnj_yield | 0.1281 | -3.7328 | 0.1638 | 0.0205 |

SPY yields 0.99% today and is pulled toward exp(-4.2784) = 1.39%.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(
    name: str,
    ticker: str = 'SPY',
    window: int = 252,
    period: str = 'daily',
    inflation_covariate: pl.Series | None = None,
    volatility_model: str = 'constant',
    business_cycle_covariate: pl.Series | None = None,
    business_cycle_covariate_dates: pl.Series | None = None,
    inflation_level: bool = False,
) -> DividendYieldParams | GARCHParams | OUCovariateParams
```

**Args:**

- <u>name (str):</u> the entry's name.
- <u>ticker (str):</u> any dividend-paying ticker in the Toolkit. Defaults to "SPY".
- <u>window (int):</u> trading days of dividends summed for one yield, about a year. Defaults to 252.
- <u>period (str):</u> the fit's time step, "daily" to "yearly". Defaults to "daily".
- <u>inflation_covariate (pl.Series &#124; None):</u> a paired inflation entry's history at the same period, adding the inflation term of Wilkie ([1986](https://doi.org/10.1017/S0071368600009009)). Defaults to None.
- <u>volatility_model (str):</u> "constant", or "garch" for swings whose size varies. Defaults to "constant".
- <u>business_cycle_covariate (pl.Series &#124; None):</u> a leading indicator's history (`LeadingIndicator.series`) for the yield to follow. Defaults to None.
- <u>business_cycle_covariate_dates (pl.Series &#124; None):</u> the dates of `business_cycle_covariate`, required with it. Defaults to None.
- <u>inflation_level (bool):</u> with `inflation_covariate`, Wilkie's own form, in which the pull acts on the log yield less its inflation term (`fit_dividend_yield_process`). Defaults to False.

**Returns:**

<u>DividendYieldParams &#124; GARCHParams &#124; OUCovariateParams:</u> `mean_reversion_speed`, `long_run_mean`, `volatility` and `initial_value` (plus `inflation_sensitivity` with an inflation covariate).

**Raises:**

- <u>ValueError:</u> if an option is not recognised or combined with another, `window` is not positive, the ticker has no price or dividend data, or the yield is not positive or does not mean-revert.

</details>

#### DividendYield.names

The names of every dividend yield entry calibrated so far, in calibration order.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
dividendyield.names  # property -> list[str]
```

</details>

#### DividendYield.params

The calibrated parameters of one dividend yield entry.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
params(name: str) -> DividendYieldParams | GARCHParams | OUCovariateParams
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if `name` has not been calibrated yet.

</details>

#### DividendYield.step_function

The step that moves a dividend yield forward: its log is pulled toward the normal level and shocked.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
dividendyield.step_function  # property
```

</details>

#### DividendYield.series

The historical trailing dividend yield one entry was calibrated on, as a decimal. `DividendGrowth` uses it to
rebuild this yield's past surprises.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
series(name: str) -> pl.Series
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if `name` has not been calibrated yet.

</details>

#### DividendYield.time_step

The time step, in years, between the observations one entry was calibrated on (1/12 for monthly). Used with
`series` to rebuild the yield's past surprises.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
time_step(name: str) -> float
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if `name` has not been calibrated yet.

</details>

#### DividendYield.changes

The historical changes in one entry's log yield, by date, from which its correlations with the other factors
are estimated.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
changes(name: str) -> pl.DataFrame
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if `name` has not been calibrated yet.

</details>

### DividendGrowth

Simulate how a company's or fund's dividends grow, as a dividend index: the dividends paid over the past year,
tracked through time.

It is part of the Wilkie model (the `wilkie` factor set), a cascade in which inflation drives the other variables.
Over the long run dividends are a real quantity: companies raise payouts with prices, but only partly at once and
the rest over the following years. Equities are therefore an inflation hedge in the long run but not in the short
run, and an inflation shock first lowers real dividends before they catch up. Divided by the paired dividend yield,
the index gives the simulated share price (`equities[].method="wilkie_derived"`). Every entry needs a paired
`inflation[]` and `dividend_yield[]` entry.

The model is the share dividend index of Wilkie (1986, section 3.7), in the form of his Reduced Standard Basis
(Table 1), the simpler version without the DB term that section 3.9 describes:

```text
dln D(t) = DMU + DW * DM(t) + DX * dlnQ(t) + DY * YE(t-1) + DSD * DZ(t)
DM(t) = DD * dlnQ(t) + (1 - DD) * DM(t-1)
```

where `dln D(t)` is the growth of the log dividend index and `dlnQ(t)` the inflation rate in log terms. Each
coefficient has a plain reading:

- `DMU` (`long_run_drift`): long-term real dividend growth, net of inflation.
- `DM`, with weight `DD` (`carried_forward_weight`, Wilkie's 0.2 a year): a slowly updating average of past
  inflation, so dividends keep catching up after inflation moves; `DW` (`lagged_inflation_weight`) is its effect.
- `DX` (`direct_inflation_weight`): how much of this period's inflation passes straight into dividends.
- `DY` (`yield_residual_sensitivity`): the effect of last period's surprise in the dividend yield, `YE(t-1)`.
- `DSD` (`volatility`): the size of the index's own random shock.

Wilkie's model has unit gain, DW + DX = 1 (section 3.7: a given percentage rise in the Retail Prices Index
ends up as the same percentage rise in the dividend index), and the fit imposes it; his bases use
DW = 0.8 and DX = 0.2 (section 3.9).

Data: the Finance Toolkit has no dividend index series, so the `Dividends` paid over the trailing `window` trading
days are summed, the numerator `DividendYield` divides by the price. An entry runs at its paired inflation entry's
period, and the paired dividend yield must use the plain fit (no `garch` or business-cycle option).

The `dividend_growth[i]` keys of a factor set and their defaults are listed under
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/configuration#configuration-classes).

**References:**

- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://doi.org/10.1017/S0071368600009009>
- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. The modular framework that positions itself against Wilkie's model. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
DividendGrowth(toolkit: Toolkit)
```

</details>

#### DividendGrowth.calibrate

Calibrate one ticker's Wilkie (1986) dividend growth model from its dividend history.

It fits how much of current inflation reaches dividends at once (`direct_inflation_weight`, Wilkie's DX), the
rest arriving through the carried-forward average (`lagged_inflation_weight`, DW = 1 - DX), plus the dividend
yield's last surprise (`yield_residual_sensitivity`), the real drift (`long_run_drift`) and the swings
(`volatility`). As in Wilkie
([1986](https://doi.org/10.1017/S0071368600009009)),
DW + DX = 1, so inflation passes fully into dividends in the long run and equities keep their real value. A
negative `yield_residual_sensitivity` means a jump in the yield (a price fall) is followed by slower dividend
growth, as when a falling market anticipates dividend cuts. Wilkie's DD is a yearly weight and inflation a
yearly rate, so both are converted to the data's period. The inputs are matched by length, so they must share
a period and end date.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.dividend_growth.dividend_growth_controller import DividendGrowth
from financescenarios.factors.dividend_yield.dividend_yield_controller import DividendYield
from financescenarios.factors.dividend_yield.dividend_yield_model import reconstruct_dividend_yield_residuals
from financescenarios.factors.inflation.inflation_controller import Inflation

toolkit = Toolkit(["JNJ"], start_date="1995-01-01", end_date="2019-12-31", benchmark_ticker=None)

inflation = Inflation(toolkit)
inflation.calibrate("inflation", country="United States", period="monthly", method="wilkie_ar1")
inflation_series = inflation.series("inflation")

dividend_yield = DividendYield(toolkit)
yield_params = dividend_yield.calibrate(
    "dividend_yield", ticker="JNJ", period="monthly", inflation_covariate=inflation_series
)

yield_level = dividend_yield.series("dividend_yield")
length = min(yield_level.len(), inflation_series.len())
yield_residual = reconstruct_dividend_yield_residuals(
    yield_level.tail(length),
    yield_params,
    dividend_yield.time_step("dividend_yield"),
    inflation=inflation_series.tail(length),
)

dividend_growth = DividendGrowth(toolkit)
dividend_growth.calibrate(
    "dividend_growth", inflation=inflation_series, yield_residual=yield_residual, ticker="JNJ", period="monthly"
)
```

Which returns (calibrated on 2026-10-14):

| Parameter | Value |
|:----------|------:|
| long_run_drift (DMU) | 0.0020 |
| direct_inflation_weight (DX) | 1.6891 |
| lagged_inflation_weight (DW) | -0.6891 |
| yield_residual_sensitivity (DY) | -0.0923 |
| volatility (DSD) | 0.0355 |
| initial_value | 3.7500 |

Johnson & Johnson's dividends grew 0.2% a month above inflation. They took up inflation faster than Wilkie's
0.2 / 0.8 split: a rise lifts them at once and the slow average then gives part back, one for one in the end.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(
    name: str,
    inflation: pl.Series,
    yield_residual: np.ndarray,
    ticker: str = 'SPY',
    window: int = 252,
    period: str = 'daily',
    carried_forward_weight: float = 0.2,
    unit_gain: bool = True,
    residual_lag: str = 'step',
) -> DividendGrowthParams
```

**Args:**

- <u>name (str):</u> the entry's name.
- <u>inflation (pl.Series):</u> the paired inflation entry's history of annual rates (`Inflation.series`).
- <u>yield_residual (np.ndarray):</u> the paired dividend yield's past surprises, rebuilt as in the example.
- <u>ticker (str):</u> any dividend-paying ticker in the Toolkit. Defaults to "SPY".
- <u>window (int):</u> trading days of dividends summed for one index value. Defaults to 252.
- <u>period (str):</u> the fit's time step, "daily" to "yearly", matching both inputs. Defaults to "daily".
- <u>carried_forward_weight (float):</u> `DD`, the yearly weight of current inflation in the carried-forward average, strictly between 0 and 1. Defaults to 0.2, Wilkie's value (section 3.9).
- <u>unit_gain (bool):</u> impose Wilkie's DW + DX = 1. Defaults to True; False gives the earlier free fit.
- <u>residual_lag (str):</u> "step" (default) reads the yield's surprise one observation back, "year" one year back, Wilkie's YE(t-1) in his yearly model.

**Returns:**

<u>DividendGrowthParams:</u> the five fitted coefficients, plus `initial_value` (the last dividend index level) and `initial_carried_forward_inflation`.

**Raises:**

- <u>ValueError:</u> if an input is invalid, the ticker has no dividend data, or the history is too short.

</details>

#### DividendGrowth.names

The names of every dividend growth entry calibrated so far, in calibration order.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
dividendgrowth.names  # property -> list[str]
```

</details>

#### DividendGrowth.params

The calibrated parameters of one dividend growth entry.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
params(name: str) -> DividendGrowthParams
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if `name` has not been calibrated yet.

</details>

#### DividendGrowth.changes

The historical changes in one entry's log dividend index, by date, from which its correlations with the other
factors are estimated.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
changes(name: str) -> pl.DataFrame
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if `name` has not been calibrated yet.

</details>

### Credit

The Credit module simulates credit spreads: the extra yield corporate bonds pay over government bonds as
compensation for default and liquidity risk. Each `credit[i]` entry is one spread series, correlated with the other
factors (typically widening when equities fall); `credit` is empty by default.

The model assumes a spread has a normal level it returns to: it widens sharply in a sell-off such as 2008 and
tightens again once the stress fades, rather than wandering off: the Ornstein-Uhlenbeck process of
[Uhlenbeck and Ornstein (1930)](https://doi.org/10.1103/PhysRev.36.823). Fitting the logarithm of the spread, the
default, is a judgement: it keeps every simulated spread positive and makes the swings proportional to the level,
so a wide spread moves more in basis points than a tight one and the distribution of future spreads is skewed
toward sharp widenings, as in credit history. A series that has touched zero or below is
fitted on its level instead.

`volatility_model: garch` lets the size of the swings cluster in time, so a volatile month tends to be followed by
another, as in [Bollerslev (1986)](https://doi.org/10.1016/0304-4076(86)90063-1), and `condition_on_business_cycle`
adds a pull from the leading indicator, so spreads tend to widen as the economy slows.

The data come through the Finance Toolkit, chosen with `dimension`:

- `maturity` or `rating`: ICE BofA spreads of US corporate bonds by maturity or rating, from FRED (API key
  needed), which keeps only the last three years of them from April 2026 (the series notes on
  [FRED](https://fred.stlouisfed.org/series/BAMLC0A4CBBB)), so the shipped factor sets leave
  credit off.
- `moodys`: Moody's Aaa and Baa yields over the 10-year Treasury, monthly from 1953 (FRED key).
- `corporate`: corporate bond spreads over government bonds, monthly, no key: Germany from 1957
  ([Bundesbank](https://www.bundesbank.de/en/statistics/money-and-capital-markets)) or Australia's A and BBB by
  maturity from 2005 ([RBA table F3](https://www.rba.gov.au/statistics/tables/)).
- `borrowing_cost`: the ECB's cost of new bank loans to euro area companies, monthly from 2003
  ([ECB MIR](https://data.ecb.europa.eu/data/datasets/MIR)), no key; a rate level rather than a spread.

Set `toolkit.start_date` back for the longer histories. For ratings that move and default see `CreditMigration`,
for a whole spread curve `CreditTermStructure`.

The `credit[i]` keys of a factor set and their defaults are listed under
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/configuration#configuration-classes).

A belief about the normal level of a log-fitted spread is a log too: a 2% target is `log(0.02)`, about `-3.9`.

Fitted on 2026-10-07 on data from 2000, Germany's spread reverts to 1.57% with a one-year half-life and the euro
area's borrowing cost to 2.54%.

**References:**

- Uhlenbeck, G.E., Ornstein, L.S. (1930). "On the Theory of the Brownian Motion." Physical Review, 36(5), 823-841. <https://doi.org/10.1103/PhysRev.36.823>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Credit(toolkit: Toolkit)
```

</details>

#### Credit.calibrate

Calibrate one credit spread from its history: how fast it returns to its normal level
(`mean_reversion_speed`), what that level is (`long_run_mean`) and how much it swings (`volatility`).

Fitting these to the observed spread means the scenarios widen and tighten at the speed and with the size the
real market has shown. The speed sets how long a credit shock lasts: a speed of
3 a year means a widening fades by half in about three months (ln 2 / 3 years), so short-horizon stresses are
severe while long-horizon spreads cluster around the normal level. The default fit works on the log of the
spread, a judgement that keeps every spread positive: `exp(long_run_mean)` is the level it is pulled toward,
and every path starts from `initial_value`, today's spread as a decimal.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.credit.credit_controller import Credit

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", fred_api_key="FRED_KEY")
credit = Credit(toolkit)

credit.calibrate("ig_7_10y", maturity_bucket="7-10 Years", period="monthly")
credit.calibrate("high_yield_bb", dimension="rating", rating_bucket="BB", period="monthly")
```

Which returns (calibrated on 2026-10-19):

| name | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-----|---------------------:|--------------:|-----------:|--------------:|
| ig_7_10y | 1.4217 | -4.6028 | 0.2133 | 0.0102 |
| high_yield_bb | 4.6098 | -4.0042 | 0.3430 | 0.0193 |

The investment-grade spread starts at 1.02% and is pulled toward exp(-4.6028) = 1.00%, the BB spread toward 1.82%.
The window is short, so the finite-sample correction of the speed matters: the plain estimates are 2.95 and 6.51.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(
    name: str,
    dimension: str = 'maturity',
    maturity_bucket: str = '7-10 Years',
    rating_bucket: str = 'BBB',
    period: str = 'daily',
    volatility_model: str = 'constant',
    business_cycle_covariate: pl.Series | None = None,
    business_cycle_covariate_dates: pl.Series | None = None,
    country: str | None = None,
) -> OUParams | GARCHParams | OUCovariateParams
```

**Args:**

- <u>name (str):</u> the spread's name in the scenarios.
- <u>dimension (str):</u> "maturity" or "rating" (ICE BofA), "moodys", "corporate" or "borrowing_cost". Defaults to "maturity".
- <u>maturity_bucket (str):</u> "1-3 Years" up to "15+ Years", for "maturity". Defaults to "7-10 Years", a judgement: a medium-to-long investment-grade maturity.
- <u>rating_bucket (str):</u> "AAA" to "CCC", Moody's "Aaa", "Baa" or "Baa - Aaa", or e.g. "BBB 10Y" for "corporate". Defaults to "BBB".
- <u>period (str):</u> "daily" up to "yearly"; a coarser period averages the data. Defaults to "daily".
- <u>volatility_model (str):</u> "constant" or "garch". Defaults to "constant".
- <u>business_cycle_covariate (pl.Series &#124; None):</u> the leading indicator history the spread moves with, so it widens as the economy slows. Defaults to None.
- <u>business_cycle_covariate_dates (pl.Series &#124; None):</u> the dates of that history, needed with it. Defaults to None.
- <u>country (str &#124; None):</u> "Germany" or "Australia" ("corporate"), "Euro Area" or a member ("borrowing_cost"). Defaults to None.

**Returns:**

<u>OUParams &#124; GARCHParams &#124; OUCovariateParams:</u> the fitted speed, level and volatility, plus the GARCH terms or the business-cycle sensitivity when those are used.

**Raises:**

- <u>ValueError:</u> if an option, bucket or country is not recognized, "garch" is combined with a covariate, or no data come back.

</details>

#### Credit.names

The names of every credit bucket calibrated so far, in calibration order.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
credit.names  # property -> list[str]
```

</details>

#### Credit.params

The calibrated parameters of one credit spread: its speed of mean reversion, normal level and volatility.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
params(name: str) -> OUParams | GARCHParams | OUCovariateParams
```

**Args:**

- <u>name (str):</u> the spread's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if that spread has not been calibrated yet.

</details>

#### Credit.step_function

The one-step move of a constant-volatility spread: the exact mean-reverting step on the log of the spread (or on
its plain level for a spread that has touched zero), so simulated spreads keep the fitted speed and stay
positive. GARCH and business-cycle-conditioned spreads move with their own step.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
credit.step_function  # property
```

</details>

#### Credit.changes

The historical period-over-period changes of one spread, the input for its correlation with the other factors
(how far spreads widen when equities fall, for example).

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
changes(name: str) -> pl.DataFrame
```

**Args:**

- <u>name (str):</u> the spread's name, as passed to `calibrate`.

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if that spread has not been calibrated yet.

</details>

### CreditTermStructure

The Credit Term Structure module simulates a whole credit spread curve: the extra yield corporate bonds pay over
government bonds at every maturity, rather than one spread per bucket. Three numbers (level, slope and curvature)
move the curve through time, so the spread at any maturity can be read off a simulated scenario.

Where `Credit` gives a handful of fixed spread buckets (1-3 years, 7-10 years, BBB), this gives a
continuous curve, so a 4-year or a 12-year spread exists in every scenario. Added to the simulated government
curve (`yield_curve`), it gives the discount curve a risky bond is priced off, which `BondPricer` uses. It is
opt-in (`credit_term_structure.enabled`) and runs next to `credit`, not instead of it.

The model is the dynamic Nelson-Siegel curve of [Nelson and Siegel (1987)](https://doi.org/10.1086/296409) and
[Diebold and Li (2006)](https://doi.org/10.1016/j.jeconom.2005.03.005) that `yield_curve` uses, applied to corporate
spreads as in [Yu and Zivot (2011)](https://doi.org/10.1016/j.ijforecast.2010.04.002): `credit_level` is the
long-maturity spread, `credit_slope` how far the short end sits below or above it and `credit_curvature` a hump at
medium maturities. Each moves as its own mean-reverting process, correlated with the rest of the model, so the
curve can widen in parallel, steepen or invert (short spreads above long ones, as in 2008) but returns toward its
usual shape. Three factors are enough because spread curves, like yield curves, move mostly in these three ways,
and they keep every maturity consistent with every other. The factors are normally distributed, so a spread can
turn slightly negative in a benign tail scenario. The
`decay` matches `yield_curve.decay` (0.7308) on purpose: two Nelson-Siegel curves with the same decay add up, so
the government curve plus this spread curve is again one. The value is Diebold and Li's: they put the curvature
factor's peak at 30 months, the average of the two- and three-year maturities commonly used, which gives
λ = 0.0609 in [Diebold and Li (2006, section 3.2)](https://doi.org/10.1016/j.jeconom.2005.03.005), monthly, so
0.0609 × 12 = 0.7308 a year.

Two data sources are available through `source`:

- `hqm` (default): the US Treasury's High Quality Market (HQM) corporate bond curve
  ([US Treasury](https://home.treasury.gov/data/treasury-coupon-issues-and-corporate-bond-yield-curves)) as a
  spread over Treasuries at 2, 5, 10 and 30 years, monthly from 1984, with a free FRED key. It is the
  investment-grade curve, built from corporate bonds rated AAA, AA or A, see
  [Girola (2011, slide 2)](https://home.treasury.gov/system/files/226/ycp_oct2011.pdf), "The HQM Yield Curve:
  Basic Concepts".
- `bond_panel`: the [Open Source Bond Asset Pricing](https://openbondassetpricing.com/) panel of US corporate bond
  trades (TRACE) from July 2002 to March 2025, a 1.8 GB download. It has no ratings, so it is the average spread
  across all bonds, and it starts from its last month, not today.

Like `yield_curve`, it is fitted to history, with no guarantee against arbitrage between maturities.

The `credit_term_structure` keys of a factor set and their defaults are listed under
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/configuration#configuration-classes).

**References:**

- Nelson, C.R., Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." The Journal of Business, 60(4), 473-489. <https://doi.org/10.1086/296409>
- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. <https://doi.org/10.1016/j.jeconom.2005.03.005>
- Yu, W., Zivot, E. (2011). "Forecasting the Term Structures of Treasury and Corporate Yields Using Dynamic Nelson-Siegel Models." International Journal of Forecasting, 27(2), 579-591. <https://doi.org/10.1016/j.ijforecast.2010.04.002>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
CreditTermStructure(bond_panel: BondPanel | None = None, toolkit: Toolkit | None = None)
```

</details>

#### CreditTermStructure.calibrate

Calibrate the credit spread curve from history: summarize each period's spread curve by its Nelson-Siegel
level, slope and curvature, then fit each as its own mean-reverting process.

Fitting to history means the simulated curves shift, tilt and bend the way the real one has, with the same
speed of recovery after a credit shock. Each factor gets a speed (`mean_reversion_speed`), a normal level
(`long_run_mean`), a swing size (`volatility`) and a starting value (`initial_value`), in decimals.
`level` is the long-maturity spread and `level + slope` the shortest one. A level speed of 1.24 a year means a
shock halves in about seven months (ln 2 / 1.24).

The method is that of [Diebold and Li (2006)](https://doi.org/10.1016/j.jeconom.2005.03.005), applied to
corporate spreads as in [Yu and Zivot (2011)](https://doi.org/10.1016/j.ijforecast.2010.04.002).

**As an example:**

```python
from financescenarios.factors.credit_term_structure.credit_term_structure_controller import (
    CreditTermStructure,
)

credit_curve = CreditTermStructure()
credit_curve.calibrate(tenors=[1, 2, 3, 5, 7, 10, 15, 20], period="monthly")
```

Which returns (calibrated on 2026-10-19, 270 monthly curves from July 2002 to December 2024):

| factor | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-------|---------------------:|--------------:|-----------:|--------------:|
| level | 1.0517 | 0.0236 | 0.0196 | 0.0100 |
| slope | 1.2451 | -0.0128 | 0.0637 | -0.0125 |
| curvature | 3.1999 | 0.0363 | 0.0959 | 0.0261 |

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(
    tenors: list[float],
    period: str = 'monthly',
    decay: float = 0.7308,
    source: str = 'bond_panel',
) -> YieldCurveParams
```

**Args:**

- <u>tenors (list[float]):</u> bond panel maturities in years, at least 3; each bond goes to the nearest one. Unused by "hqm".
- <u>period (str):</u> fitting frequency and time step: "daily", "weekly", "monthly", "quarterly" or "yearly" ("hqm": the last three). Defaults to "monthly", as daily bond spreads are too noisy.
- <u>decay (float):</u> the Nelson-Siegel decay (lambda), annualized; fixed, not fitted. Defaults to 0.7308, as for `yield_curve`, so the two curves add up.
- <u>source (str):</u> "bond_panel" (TRACE trades; the first call downloads about 1.8 GB) or "hqm" (the Treasury's HQM curve; FRED key). Defaults to "bond_panel"; a config defaults to "hqm".

**Returns:**

<u>YieldCurveParams:</u> the fitted `level`, `slope` and `curvature` processes and the `decay`.

**Raises:**

- <u>ValueError:</u> if `source`, `period`, `decay` or `tenors` is invalid, or the HQM curve cannot be read (no Toolkit or FRED key).

</details>

#### CreditTermStructure.fetch_hqm_spreads

The Treasury's High Quality Market (HQM) corporate spread curve: the yield of high-grade (AAA to A) US corporate
bonds over Treasuries at 2, 5, 10 and 30 years, monthly from 1984, averaged to `period`. This is the history
the default `hqm` source calibrates on.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fetch_hqm_spreads(period: str) -> tuple[pl.Series, dict[float, pl.Series]]
```

**Args:**

- <u>period (str):</u> "monthly", "quarterly" or "yearly".

**Returns:**

<u>tuple[pl.Series, dict[float, pl.Series]]:</u> the dates, and one spread series per maturity in years.

**Raises:**

- <u>ValueError:</u> if no Toolkit was given, or nothing comes back (no FRED key, or a window before 1984).

</details>

#### CreditTermStructure.params

The calibrated spread curve: the level, slope and curvature processes and the decay.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
credittermstructure.params  # property -> YieldCurveParams
```

**Raises:**

- <u>RuntimeError:</u> if the curve has not been calibrated yet.

</details>

#### CreditTermStructure.step_function

The one-step move of each curve factor: the exact mean-reverting step, so the speed of recovery does not depend
on the time step.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
credittermstructure.step_function  # property
```

</details>

#### CreditTermStructure.changes

The historical period-over-period changes of `credit_level`, `credit_slope` and `credit_curvature`, the input
for their correlation with each other and with the other factors.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
credittermstructure.changes  # property -> dict[str, pl.DataFrame]
```

**Returns:**

<u>dict[str, pl.DataFrame]:</u> one table per factor, with a `date` and a `value` column.

**Raises:**

- <u>RuntimeError:</u> if the curve has not been calibrated yet.

</details>

### CreditMigration

The Credit Migration module simulates how corporate credit ratings move and default over time, driven by a simulated
credit cycle: the `credit_cycle` factor, an index that is high in good years (few downgrades and defaults) and low in
bad ones.

A bond rated BBB has a small chance of defaulting each year, but those chances are not independent across bonds or
years: in a recession many companies are downgraded and default together. This factor captures that shared swing.
Every rating's chance of an upgrade, a downgrade or default in a year follows from that year's cycle value, so
defaults bunch in the scenarios and years where the cycle turns bad. `rating_migration` then rolls a bond portfolio's
rating mix forward along the cycle, giving the share defaulted and the loss in every scenario.

The model is the one-factor ("Vasicek") credit-cycle model of rating migration of
[Vasicek (2002)](https://www.risk.net/risk-management/credit-risk/1500333/loan-portfolio-value) and Belkin, Suchower
and Forest (1998), as presented in
[Kim (1999)](https://www.msci.com/www/research-report/a-way-to-condition-transition/018440984), the structure behind
the Basel internal-ratings formula. A share of every borrower's credit quality, the `asset_correlation`, moves with
the shared cycle; the rest is its own luck. The cycle is fitted year by year from default rates and simulated as a
mean-reverting process around 0, so bad years cluster but the economy recovers, and it is correlated with the other
factors, so a weak credit cycle can come with falling equities and wider spreads in the same scenario. A one-factor
model is a sensible choice here: default history is short and sparse, and one shared driver captures the common
year-to-year swing in default rates across ratings.

The data come from CEREP, the European Securities and Markets Authority's central repository of credit rating
statistics, through the Finance Toolkit, with no API key needed: every agency registered in the EU (S&P, Moody's,
Fitch and others) in its own rating scale. On S&P's corporate ratings from 2000 to 2025 the worst years come out
as 2009, 2001, 2020 and 2002, the asset correlation is about 0.10, and a shock to the cycle halves in about 8
months. That correlation sits below Basel's supervisory 12% to 24% for corporates, which is set to be prudent
in [BCBS (2005, section 5.2)](https://www.bis.org/bcbs/irbriskweight.pdf); a half-life well under a year means the
yearly cycle values are close to independent from one year to the next.

The matrix pools every year of the default-rate history, as Basel CRE36.79 asks of PD estimation: the observation
period covers at least five years for at least one source, a longer relevant and material period is used whenever
one is available, and the data hold a representative mix of good and bad years
([BCBS, CRE36.79](https://www.bis.org/basel_framework/chapter/CRE/36.htm)). One choice is judgement rather than
taken from a source: the cycle is simulated as a mean-reverting process held at a long-run mean of 0, so the
simulated matrix averages back to the through-the-cycle one.

It does not derive spreads from the ratings (use `credit` for spreads by rating), recovery rates are a fixed input of
`rating_migration`, and the cycle is one index for all sectors and regions.

The `credit_migration` keys of a factor set and their defaults are listed under
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/configuration#configuration-classes).

**References:**

- Vasicek, O. (2002). "Loan portfolio value." Risk, December 2002. <https://www.risk.net/risk-management/credit-risk/1500333/loan-portfolio-value>
- Kim, J. (1999). "A Way to Condition the Transition Matrix on Wind." RiskMetrics Group (MSCI). <https://www.msci.com/www/research-report/a-way-to-condition-transition/018440984>
- ESMA. "CEREP: Central Repository of credit rating activity." <https://registers.esma.europa.eu/cerep-publication/>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
CreditMigration(toolkit: Toolkit)
```

</details>

#### CreditMigration.calibrate

Calibrate the credit cycle from an agency's rating history: the average one-year transition matrix, the asset
correlation and the yearly cycle, which is then fitted as a mean-reverting process.

The transition matrix pools the agency's rating changes over every year of the default-rate history, so it
reflects how often each rating is upgraded, downgraded or defaults in an average year across good and bad years
(Basel CRE36.79 requires the longer observation period wherever one is available). The
asset correlation and the historical cycle come from the default rates per rating, as in
[Vasicek (2002)](https://www.risk.net/risk-management/credit-risk/1500333/loan-portfolio-value) and
[Kim (1999)](https://www.msci.com/www/research-report/a-way-to-condition-transition/018440984): they measure
how strongly good and bad years move all ratings together. A higher correlation means more years like 2009 in
the scenarios and a fatter tail of portfolio losses; a faster mean reversion means downturns pass sooner.

The default-rate history spans the Toolkit's start and end dates (CEREP covers 1989 onward, S&P's own reporting
starts in 2000); a long history matters, since it needs several recessions to pin down the correlation. CEREP
answers slowly, so the first calibration takes a few minutes.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.credit_migration.credit_migration_controller import CreditMigration

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2000-01-01")
credit_migration = CreditMigration(toolkit)

params = credit_migration.calibrate(agency="S&P", rating_type="corporate")
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(
    agency: str = 'S&P',
    rating_type: str = 'corporate',
    region: str | None = None,
    matrix_years: int | None = None,
    pd_floor: float = PD_FLOOR,
) -> CreditCycleParams
```

**Args:**

- <u>agency (str):</u> the rating agency as CEREP names it, e.g. "S&P", "Moody's", "Fitch". Defaults to "S&P".
- <u>rating_type (str):</u> "corporate", "sovereign", "structured_finance" or "covered_bonds". Defaults to "corporate".
- <u>region (str &#124; None):</u> limit to rated entities in one region, e.g. "Europe". Defaults to None (all regions).
- <u>matrix_years (int &#124; None):</u> how many recent years of transition counts to pool, at least 1. Defaults to None: every year from the first year of the default-rate history, the same window as the default probabilities (Basel CRE36.79).
- <u>pd_floor (float):</u> the lowest one-year default probability any rating gets. Defaults to 0.0005, the Basel III / CRR3 corporate floor; 0.0003 gives the Basel II floor.

**Returns:**

<u>CreditCycleParams:</u> the cycle's `mean_reversion_speed`, `long_run_mean` (0), `volatility` and `initial_value`, plus `ratings`, `transition_matrix`, `asset_correlation` and `agency`.

**Raises:**

- <u>ValueError:</u> if `matrix_years` is below 1, or CEREP returns no transition counts or too few years of default rates.

</details>

#### CreditMigration.params

The calibrated credit cycle: its mean-reverting process, average transition matrix and asset correlation.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
creditmigration.params  # property -> CreditCycleParams
```

**Raises:**

- <u>RuntimeError:</u> if the cycle has not been calibrated yet.

</details>

#### CreditMigration.cycle

The historical credit cycle, one value per year: strongly negative in years such as 2001 and 2009, when
defaults spiked. Raises a `RuntimeError` before calibration.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
creditmigration.cycle  # property -> pl.DataFrame
```

</details>

#### CreditMigration.changes

The yearly changes of the historical cycle, the input for its correlation with the other factors.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
creditmigration.changes  # property -> pl.DataFrame
```

</details>

#### CreditMigration.step_function

The one-step move of the cycle: an exact mean-reverting (Ornstein-Uhlenbeck) step back toward 0.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
creditmigration.step_function  # property
```

</details>

### rating_migration

Roll a bond portfolio's rating mix forward through a run's simulated credit cycle, one year at a time: the share of
the portfolio in each rating and in default, and the loss to default, in every simulation and year.

Given, say, 40% A-rated, 50% BBB and 10% BB bonds, this shows how much of the portfolio has been downgraded or has
defaulted after each year in every scenario, and what that costs once the recovery on defaulted bonds is counted. Each
simulated year's cycle value picks that year's transition matrix, so a bad year pushes every rating toward downgrade
and default at once. Scenarios with a bad credit cycle therefore carry far more defaults than the average, and the gap
between the mean and a high quantile in `summary()` shows how large that tail is.

**As an example:**

```python
from financescenarios import rating_migration

# result: the ScenarioSet of a run with credit_migration.enabled: true
migration = rating_migration(result, {"A": 40, "BBB": 50, "BB": 10})
migration.summary()
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
rating_migration(
    scenario_set: ScenarioSet,
    holdings: Mapping[str, float],
    recovery_rate: float = 0.4,
    params: CreditCycleParams | None = None,
) -> RatingMigrationResult
```

**Args:**

- <u>scenario_set (ScenarioSet):</u> a run with `credit_migration.enabled: true`, so it holds `credit_cycle`.
- <u>holdings (Mapping[str, float]):</u> exposure per starting rating, e.g. {"A": 40, "BBB": 50, "BB": 10}.
- <u>recovery_rate (float):</u> the share of a defaulted exposure recovered, in [0, 1). Defaults to 0.4, the senior unsecured bond recovery by the rating held a year before default: "$39.0" per $100 par for all ratings, 1982-2004, in Moody's (2005, Exhibit 28) (https://www.bu.edu/econ/files/2015/01/Moodys_Default_1920-2004.pdf).
- <u>params (CreditCycleParams &#124; None):</u> the calibrated cycle. Defaults to None, which takes it from the run; pass `calibration.calibrated_params["credit_cycle"]` for a run read back from disk.

**Returns:**

<u>RatingMigrationResult:</u> `distribution`, `cumulative_default` and `loss` per simulation and whole year, with `summary()` for the mean and quantiles per year.

**Raises:**

- <u>KeyError:</u> if the run has no `credit_cycle`.
- <u>ValueError:</u> if the calibrated cycle is not available, a holding names an unknown rating or is negative, or the recovery rate is outside [0, 1).

</details>

### How It Is Calculated

The model functions behind this page, each with the formula it implements.

{% raw %}
#### rescale_transition_matrix

Convert regime-switching probabilities fitted on one data frequency to another, so calm and turbulent
stretches last just as long in calendar time whatever step the scenarios use.

A transition matrix fitted on monthly returns gives the chance of switching regime per month. Applied
unchanged to weekly steps, the market would switch about 4.3 times too often and turbulent spells would be
far too short. The matrix is turned into a continuous-time rate of switching (its generator) and back into
probabilities at the new step, as is standard for rating migration matrices, see Israel, Rosenthal and Wei
(2001). The long-run share of time in each regime is unchanged. Where no exact generator exists Israel, Rosenthal
and Wei (2001, section 3) show how to obtain an approximate one; here negative
entries of the converted matrix are set to zero and each row rescaled to sum to 1, a simpler judgement.

The formula is as follows:

$$
Q = \operatorname{logm}(P) / \text{from\_dt}
$$

$$
P_{\text{rescaled}} = \operatorname{expm}(Q \cdot \text{to\_dt})
$$

$$
P_{\text{rescaled}} = \text{Pi} + \lambda ^{\text{to\_dt} / \text{from\_dt}} \cdot (I - \text{Pi}),\;\; \lambda = p_{00} + p_{11} - 1 (\text{two regimes})
$$

Where Pi has both rows equal to the stationary distribution, pi_0 = (1 - p_11) / (2 - p_00 - p_11). The
two-regime closed form applies when 0 < lambda < 1 and gives the same answer as the general one.

**References:**

- Israel, R.B., Rosenthal, J.S., Wei, J.Z. (2001). "Finding Generators for Markov Chains via Empirical Transition Matrices, with Applications to Credit Ratings." Mathematical Finance, 11(2), 245-265. <https://doi.org/10.1111/1467-9965.00114>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
rescale_transition_matrix(
    transition_matrix: list[list[float]],
    from_dt: float,
    to_dt: float,
) -> list[list[float]]
```

**Args:**

- <u>transition_matrix (list[list[float]]):</u> the chances of moving between regimes per period of the fit.
- <u>from_dt (float):</u> the length of that period, in years (1/12 for monthly).
- <u>to_dt (float):</u> the length of the scenario step, in years.

**Returns:**

<u>list[list[float]]:</u> the chances of moving between regimes per scenario step; unchanged when the two periods match.

</details>
{% endraw %}

#### fit_regime_switching_lognormal

Fit Hardy's (2001) regime-switching lognormal model to an equity's price history: a calm and a turbulent
market, each with its own mean return and volatility, and the chance of moving between them.

A single lognormal return distribution understates crashes: real equity returns have fatter tails and
volatility comes in clusters. Hardy's model keeps returns normal within each regime but lets the market sit
in a high-volatility regime for months at a time, so a mixture of the two produces the fat left tail and the
clustered losses that guarantees and capital requirements are most sensitive to. It is widely used for
equity-linked guarantees such as segregated funds and variable annuities.

The regimes are never observed, so the fit is Baum-Welch expectation-maximization: Hamilton's (1989) filter
gives the chance of each regime at every date, the parameters are re-estimated as weighted averages, and the
two steps repeat until the likelihood stops improving. It maximizes the same likelihood as Hardy's direct maximum
likelihood fit, which Ahlgrim, D'Arcy and Gorvett (2005, section 3) describe as maximizing the likelihood
implied by the regime-switching process. Two regimes is the default because, as they summarize in the same
section, Hardy (2001) finds only a marginal improvement in fit from more than two regimes.
For comparison, their fit on Shiller's large-stock excess returns for 1871-2002 has monthly means of
0.8% and -1.1%, volatilities of 3.9% and 11.3% and switching chances of 1.1% and 5.9%, and the base calibration of
Barrie & Hibbert's monthly model in Hibbert, Mowbray and Turnbull (2001, Exhibit 7.1A) has means of 0.118 and -0.136,
volatilities of 0.098 and 0.244 and chances of staying of 0.929 and 0.879. A history needs at least five prices
per regime (a judgement: two moments and a row of switching chances per regime).

The formula is as follows:

$$
r_{t} | s_{t} = k \sim \operatorname{Normal}(\mu_{k},\; \sigma_{k} ^{2}),\;\; P(s_{t+1} = j | s_{t} = i) = p_{ij}
$$

$$
\alpha_{t}(j) = e_{t}(j) \cdot \sum_{i} \alpha_{t-1} (i) \cdot p_{ij} / c_{t}
$$

$$
\beta_{t}(i) = \sum_{j} p_{ij} \cdot e_{t+1}(j) \cdot \beta_{t+1}(j) / c_{t+1}
$$

$$
\gamma_{t}(k) = \alpha_{t}(k) \cdot \beta_{t}(k) / \sum_{j} \alpha_{t} (j) \cdot \beta_{t}(j)
$$

$$
p_{ij} < - \sum_{t} \alpha_{t} (i) \cdot p_{ij} \cdot e_{t+1}(j) \cdot \beta_{t+1}(j) / c_{t+1},\;\; \text{each row rescaled to sum to 1}
$$

$$
\mu_{k} = \sum_{t} \gamma_{t} (k) \cdot r_{t} / \sum_{t} \gamma_{t} (k)
$$

$$
\sigma_{k} ^{2} = \sum_{t} \gamma_{t} (k) \cdot (r_{t} - \mu_{k}) ^{2} / \sum_{t} \gamma_{t} (k)
$$

$$
\text{log}\; L = \sum_{t} \;\text{log} (c_{t})
$$

Where r_t is the log-return, e_t(k) the normal density of r_t in regime k, c_t the scale that makes alpha_t sum
to 1 and gamma_t(k) the smoothed probability of regime k at t. Means and volatilities are reported per year;
the switching chances stay per period of the data.

**References:**

- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. <https://doi.org/10.1080/10920277.2001.10595984>
- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92, sections 2 and 3 (Equity Returns). <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert Limited, Exhibit 7.1A. <https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf>
- Hamilton, J.D. (1989). "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle." Econometrica, 57(2), 357-384. <https://doi.org/10.2307/1912559>
- Alswaidan, A., Jin, C., Varner, J.D. (2026). "Continuous Hidden Markov Models for Equity Returns: Heavy-Tail Emission Families and Regime-Conditional Value-at-Risk." arXiv:2606.23492. <https://arxiv.org/abs/2606.23492>. Its Gaussian fitting algorithm only.
- Baum, L.E., Petrie, T., Soules, G., Weiss, N. (1970). "A Maximization Technique Occurring in the Statistical Analysis of Probabilistic Functions of Markov Chains." The Annals of Mathematical Statistics, 41(1), 164-171. <https://doi.org/10.1214/aoms/1177697196>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_regime_switching_lognormal(
    prices: pl.Series,
    time_step: float,
    n_regimes: int = 2,
    max_iterations: int = _MAX_EM_ITERATIONS,
    tolerance: float = 1e-06,
) -> RegimeParams
```

**Args:**

- <u>prices (pl.Series):</u> the equity's price history, evenly spaced in time.
- <u>time_step (float):</u> the time between prices, in years (1/12 for monthly).
- <u>n_regimes (int):</u> the number of regimes, default 2 (calm and turbulent, as in Hardy (2001)).
- <u>max_iterations (int):</u> the most fitting rounds before stopping.
- <u>tolerance (float):</u> stop once the likelihood improves by less than this.

**Returns:**

<u>RegimeParams:</u> each regime's annual mean and volatility, the chances of switching, the long-run share of time per regime, today's most likely regime and the last price.

**Raises:**

- <u>ValueError:</u> if there are fewer than `n_regimes * 5` prices, or a regime ends up with almost no observations.

**Warns:**

- <u>UserWarning:</u> if the fit does not settle within `max_iterations`, or the likelihood falls between rounds.

</details>

#### fit_hibbert_regime_switching

Fit the regime-switching equity of Hibbert, Mowbray and Turnbull (2001): Hardy's calm and turbulent regimes,
fitted on the return stocks earn above cash rather than on the total return.

Equity returns are cash plus a risk premium. Modeling the premium, not the total return, ties equities to the
rate environment: in a scenario where short rates climb to 6%, expected equity returns climb with them, and in
a zero-rate world they fall. That consistency between asset classes is what the Barrie & Hibbert model was
built for, and it matters for long-horizon ALM, where a fixed equity return next to a moving yield curve would
make equities look too cheap or too dear against bonds. The premium itself keeps its regimes, so the fat
left tail and clustered losses of the plain model remain. In the scenarios the simulated short rate is added
back each step. Hibbert, Mowbray and Turnbull (2001, section 5.2.1) apply the regime-switching model to log
equity returns in excess of the log riskless return, and Ahlgrim, D'Arcy and Gorvett (2005, section 3) fit it
to excess equity returns too. When the two histories differ in length they are lined up
on their latest observations (a judgement; the dated join of the business-cycle fit is the stricter option).

The formula is as follows:

$$
x_{t} = \ln(S_{t} / S_{t-1}) - r_{t} \cdot \text{dt}
$$

$$
x_{t} | s_{t} = k \sim \operatorname{Normal}(\mu_{k} \cdot \text{dt},\; \sigma_{k} ^{2} \cdot \text{dt})
$$

Where r_t is the annualized short rate and s_t the hidden regime.

**References:**

- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert Limited. <https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf>
- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. <https://doi.org/10.1080/10920277.2001.10595984>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_hibbert_regime_switching(
    prices: pl.Series,
    risk_free_rate: pl.Series,
    time_step: float,
    n_regimes: int = 2,
    max_iterations: int = _MAX_EM_ITERATIONS,
    tolerance: float = 1e-06,
) -> RegimeParams
```

**Args:**

- <u>prices (pl.Series):</u> the equity's price history, evenly spaced in time.
- <u>risk_free_rate (pl.Series):</u> the short rate's history at the same frequency, annual, as decimals; the two are lined up on their latest observations.
- <u>time_step (float):</u> the time between prices, in years.
- <u>n_regimes (int):</u> the number of regimes, default 2 (calm and turbulent).
- <u>max_iterations (int):</u> the most fitting rounds before stopping.
- <u>tolerance (float):</u> stop once the likelihood improves by less than this.

**Returns:**

<u>RegimeParams:</u> each regime's annual mean and volatility of the return above cash, the chances of switching, today's most likely regime and the last price.

**Raises:**

- <u>ValueError:</u> if there are fewer than `n_regimes * 5` prices, or a regime ends up with almost no observations.

</details>

#### fit_regimes_with_index_switching

Carry the regimes of a long index history over to a ticker with a much shorter one: how often and for how long
the market is calm or turbulent come from the index, each regime's mean and volatility are fitted on the ticker.

Twenty years of a fund hold two or three bear markets, too few to say how often they come and how long they last;
an index with sixty to a hundred years holds a dozen. So the switching chances are the index's, held fixed, and the
regime means and volatilities are Hardy's (2001) regime-switching lognormal model fitted to the ticker's own
returns by maximum likelihood under that switching: the EM algorithm with Hamilton's (1989) filter and smoother in
the E-step and only the means and volatilities in the M-step. The fit starts from the index's regimes shifted and
scaled to the ticker's mean and variance. Today's regime is the one the ticker's own returns point to.

When the index's switching follows a covariate such as inflation (its `tvtp`), each month's switching chances are
the logit's at that month's covariate (`covariate_path`), and the long-run shares reported are those at
`covariate_level`, normally the covariate's average over the ticker's own years.

A caveat: the fund's twenty-odd years then set each regime's level and swings alone. On year-end backtests from
2000 to 2022 this lowered Japan's (EWJ on the Nikkei 225's switching) four-year CRPS skill from +0.25 to +0.06 on
the 18 holdout origins against the earlier shift-and-scale of the index's regimes, while Europe's rose from +0.25
to +0.34 and the US funds' held.

The formula is as follows:

$$
r_{t} | s_{t} = k \sim \operatorname{Normal}(m_{k},\; v_{k}),\;\; P(s_{t} = j | s_{t-1} = i) = p_{ij} \;\text{fixed at the index's}
$$

$$
\text{E-step:}\;\; w_{tk} = P(s_{t} = k | r_{1},\; ...,\; r_{T}),\;\; \text{Hamilton's filter and smoother}
$$

$$
\text{M-step:}\;\; m_{k} = \sum_{t} w_{tk} \cdot r_{t} / \sum_{t} w_{tk},\;\; v_{k} = \sum_{t} w_{tk} \cdot (r_{t} - m_{k}) ^{2} / \sum_{t} w_{tk}
$$

Where r_t are the ticker's log returns per step and p_ij the index's switching chances (at each step's covariate,
when they follow one).

**References:**

- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. <https://doi.org/10.1080/10920277.2001.10595984>
- Hamilton, J.D. (1989). "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle." Econometrica, 57(2), 357-384. <https://doi.org/10.2307/1912559>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_regimes_with_index_switching(
    index_params: RegimeParams,
    prices: pl.Series,
    time_step: float,
    covariate_level: float | None = None,
    covariate_path: np.ndarray | None = None,
) -> RegimeParams
```

**Args:**

- <u>index_params (RegimeParams):</u> the regime fit on the long index history, at the ticker's time step.
- <u>prices (pl.Series):</u> the ticker's price history, evenly spaced in time.
- <u>time_step (float):</u> the time between the ticker's prices, in years.
- <u>covariate_level (float &#124; None):</u> with time-varying switching, the covariate level whose switching sets the long-run shares, e.g. the average inflation over the ticker's years. Defaults to None (fixed switching).
- <u>covariate_path (np.ndarray &#124; None):</u> with time-varying switching, the covariate at the end of each of the ticker's prices (one per price, nulls not allowed), whose switching moves the chain into the next return; None uses `covariate_level` for every step. Defaults to None.

**Returns:**

<u>RegimeParams:</u> the index's switching chances (at `covariate_level`, with its `tvtp`, when they vary) and long-run shares, with regime means and volatilities fitted on the ticker, today's most likely regime and the ticker's last price.

**Raises:**

- <u>ValueError:</u> if the index was fitted at another time step, `covariate_level` is missing for time-varying switching or given for fixed switching, `covariate_path` does not have one value per price, or there are fewer than five prices per regime.

</details>

#### expected_regime_shares

The long-run share of time in each regime when the switching follows a simulated covariate: the expected regime
probabilities carried along every covariate path, averaged over the paths and over the steps after a burn-in.

With switching that follows inflation, the share of turbulent months depends on where inflation goes, not on one
level of it: the logit is convex in inflation, so the months above the average add more turbulence than the
months below take away. Averaging the expected probabilities along simulated paths of the covariate is the
simulated method of moments of McFadden (1989) and Duffie and Singleton (1993): the regime chain itself is never
drawn, so the only sampling noise is the covariate's.

The formula is as follows:

$$
p_{t+1} = p_{t} \cdot P(z_{t}),\;\; p_{0} = e_{s0}
$$

$$
\text{share} = \text{mean over paths and over}\; t \geq \text{burn-in of}\; p_{t}
$$

Where P(z) is the transition matrix at covariate level z (see `RegimeTVTPParams`), z_t the covariate at the start
of step t, and s0 today's regime.

**References:**

- McFadden, D. (1989). "A Method of Simulated Moments for Estimation of Discrete Response Models Without Numerical Integration." Econometrica, 57(5), 995-1026. <https://doi.org/10.2307/1913621>
- Duffie, D., Singleton, K.J. (1993). "Simulated Moments Estimation of Markov Models of Asset Prices." Econometrica, 61(4), 929-952. <https://doi.org/10.2307/2951768>
- Filardo, A.J. (1994). "Business-Cycle Phases and Their Transitional Dynamics." Journal of Business & Economic Statistics, 12(3), 299-308. <https://doi.org/10.1080/07350015.1994.10524545>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
expected_regime_shares(
    params: RegimeParams,
    covariate_paths: np.ndarray,
    burn_in_steps: int = 0,
) -> np.ndarray
```

**Args:**

- <u>params (RegimeParams):</u> regimes whose switching follows the covariate (`tvtp` set).
- <u>covariate_paths (np.ndarray):</u> simulated covariate levels, shape (n_paths, n_steps + 1), one step per step of the regime fit.
- <u>burn_in_steps (int):</u> the first steps to leave out, so today's regime and covariate have worn off. Defaults to 0.

**Returns:**

<u>np.ndarray:</u> the long-run share of each regime, summing to one.

**Raises:**

- <u>ValueError:</u> if `params` has no `tvtp` or the burn-in leaves no step.

</details>

{% raw %}
#### shift_regimes_to_premium

Make an equity earn a long-run premium over the short rate instead of the average return of the fund's own years,
keeping its regimes, their volatilities and how often the market moves between them.

A fund's twenty-odd years carry one era's luck into every scenario: a market that happened to boom or stagnate
over those years is projected to do so for decades. How much stocks earn above cash is far better pinned down by a
century and a half across many countries. Every regime mean moves by the same amount, so in the long run the log
return above the short rate averages ln(1 + premium), and the scenarios add the simulated short rate back each
step, as in the excess-return equity of Hibbert, Mowbray and Turnbull (2001, section 5.2.1). Calm and turbulent
regimes stay as far apart as fitted, so crashes keep their depth.

The premium is geometric (compound), the way Jordà, Knoll, Kuvshinov, Schularick and Taylor (2019, Table II)
report it, because the regime means are log returns: a geometric premium G is exactly a mean log return of
ln(1 + G) above cash. An arithmetic premium A converts with the volatility of the series it was measured on,
roughly G = A - sigma^2 / 2: Table II's 5.85% with a volatility of 21.27% gives 3.6%, close to its geometric 3.77%.
The default is that 3.77%, the equity return above bills across 16 countries from 1870 to 2015.

With switching that follows inflation or the business cycle, the long-run shares are `regime_shares`, the shares
the run's own simulated covariate gives (`expected_regime_shares`), so the market earns the premium on average
over the inflation the scenarios simulate, the way the premium itself averages over every inflation history saw;
it earns more while inflation is low and less while it is high. Taking the shares at one inflation level instead
(the fund's own years' average) leaves out how much more turbulent the months of high inflation are: with the
default's US inflation the market then earns about 2.7% over cash, not 3.77%.

The formula is as follows:

$$
m = \sum_{k} \pi_{k} \cdot \mu_{k}
$$

$$
\text{mu'}_{k} = \mu_{k} - m + \ln(1 + G)
$$

$$
\ln(S_{t+dt} / S_{t}) = (\text{mu'}_{k} + r_{t}) \cdot \text{dt} + \sigma_{k} \cdot \sqrt{\text{dt}} \cdot z
$$

Where pi is the long-run share of each regime, mu_k and sigma_k the regime means and volatilities (annual), G the
premium and r the simulated short rate.

**References:**

- Jordà, Ò., Knoll, K., Kuvshinov, D., Schularick, M., Taylor, A.M. (2019). "The Rate of Return on Everything, 1870-2015." Quarterly Journal of Economics, 134(3), 1225-1298. <https://doi.org/10.1093/qje/qjz012>
- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert Limited. <https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
shift_regimes_to_premium(
    params: RegimeParams,
    premium: float = LONG_RUN_EQUITY_PREMIUM,
    regime_shares: np.ndarray | None = None,
) -> RegimeParams
```

**Args:**

- <u>params (RegimeParams):</u> the fitted regimes, with annual regime means of the total log return.
- <u>premium (float):</u> the long-run geometric premium over the short rate, as a decimal. Defaults to 0.0377.
- <u>regime_shares (np.ndarray &#124; None):</u> the long-run share of each regime to average over, which then also replaces `stationary_distribution`; None (the default) uses `stationary_distribution`.

**Returns:**

<u>RegimeParams:</u> the same regimes with each mean shifted to a return above the short rate.

**Raises:**

- <u>ValueError:</u> if the premium is -100% or below.

</details>
{% endraw %}

#### fit_regime_switching_tvtp

Fit a regime-switching equity whose chance of turning turbulent depends on the business cycle, the
time-varying transition probabilities of Filardo (1994).

In the plain regime model a calm market is as likely to turn turbulent in a boom as in a slowdown. In practice
bear markets cluster around recessions. Here the chance of switching moves with a business-cycle indicator
such as the OECD leading indicator, so scenarios that start or pass through a weak economy carry a higher
chance of an equity drawdown, and equity losses line up with weak growth across the other factors.

The fit takes two steps rather than the joint estimation of Filardo and of Diebold, Lee and Weinbach (1994):
first the plain regime model, then, for each starting regime, a logit regression of which regime came next on
the indicator. A small penalty keeps the regression finite when the data separate perfectly.

The formula is as follows:

$$
s_{t} = \text{argmax}_{k} P (s_{t} = k | r_{1},\; ...,\; r_{T})
$$

$$
\text{max over (theta\_i, gamma\_i) of sum\_t:s\_t=i ln p\_i},\;\; s_{t+1}(z_{t}) - 0.01 \cdot (| \theta_{i} | ^{2} + | \gamma_{i} | ^{2})
$$

$$
p_{ij}(z_{t}) = \exp(\theta_{ij} + \gamma_{ij} \cdot z_{t}) / \sum_{k} \;\text{exp} (\theta_{ik} + \gamma_{ik} \cdot z_{t})
$$

Where P(s_t = k | r_1, ..., r_T) is the smoothed regime probability and z_t the indicator's level at the end of
return t.

**References:**

- Filardo, A.J. (1994). "Business-Cycle Phases and Their Transitional Dynamics." Journal of Business & Economic Statistics, 12(3), 299-308. <https://doi.org/10.1080/07350015.1994.10524545>
- Diebold, F.X., Lee, J.H., Weinbach, G.C. (1994). "Regime Switching with Time-Varying Transition Probabilities." In Hargreaves, C. (ed.), Nonstationary Time Series Analysis and Cointegration, Oxford University Press, 283-302. The joint EM estimator this two-step fit approximates. <https://doi.org/10.1093/oso/9780198773917.003.0010>
- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. <https://doi.org/10.1080/10920277.2001.10595984>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_regime_switching_tvtp(
    prices: pl.Series,
    price_dates: pl.Series,
    business_cycle_covariate: pl.Series,
    business_cycle_covariate_dates: pl.Series,
    time_step: float,
    n_regimes: int = 2,
    max_iterations: int = _MAX_EM_ITERATIONS,
    tolerance: float = 1e-06,
) -> RegimeParams
```

**Args:**

- <u>prices (pl.Series):</u> the equity's price history, evenly spaced in time.
- <u>price_dates (pl.Series):</u> the date of each price.
- <u>business_cycle_covariate (pl.Series):</u> the business-cycle indicator's history, such as `LeadingIndicator.series`.
- <u>business_cycle_covariate_dates (pl.Series):</u> the date of each indicator value; only dates both share are used.
- <u>time_step (float):</u> the time between prices, in years.
- <u>n_regimes (int):</u> the number of regimes, default 2 (calm and turbulent).
- <u>max_iterations (int):</u> the most fitting rounds for the regime fit.
- <u>tolerance (float):</u> stop the regime fit once the likelihood improves by less than this.

**Returns:**

<u>RegimeParams:</u> the plain regime fit on the shared dates, plus `tvtp`, the logit coefficients that tie each regime's switching chances to the indicator.

**Raises:**

- <u>ValueError:</u> if fewer than `n_regimes * 5` prices share a date with the indicator, a regime ends up with almost no observations, or a regime has too few observed switches to fit (ten per regime with two regimes).

</details>

#### fit_regime_switching_tvtp_em

Fit a regime-switching equity whose chance of switching regime depends on an economic series, such as inflation,
with the time-varying transition probabilities of Filardo (1994) estimated jointly by maximum likelihood (with a
weak ridge penalty on the logit coefficients, so switches the covariate separates perfectly keep finite odds).

Stocks have done badly in high-inflation years: on Shiller's S&P total return and CPI for 1947-2025, the real
return averaged about -1.5% a year in years with inflation above 5%, against about 12% when it stayed under 3%.
In a two-regime model that shows up as a turbulent regime entered far more often when inflation is high, so a
scenario in which inflation climbs also carries a higher chance of an equity bear market.

The fit is the expectation-maximization algorithm of Diebold, Lee and Weinbach (1994): regimes, regime means and
volatilities, and the logit of each switching chance on the covariate are estimated together, unlike the
two-step `fit_regime_switching_tvtp`, which classifies the regimes first and regresses afterwards. With
`fixed_covariate_sensitivity` the slopes are held at given values, for example ones read from a longer history,
and with `fixed_regime_means` and `fixed_regime_volatilities` the regimes are, so a long history can be read
through a ticker's own regimes and the ticker keeps them.

The formula is as follows:

$$
r_{t} | s_{t} = k \sim \operatorname{Normal}(\mu_{k},\; \sigma_{k} ^{2})
$$

$$
P(s_{t+1} = j | s_{t} = i,\; z_{t}) = \exp(\theta_{ij} + \gamma_{ij} \cdot z_{t}) / \sum_{k} \;\text{exp} (\theta_{ik} + \gamma_{ik} \cdot z_{t})
$$

Where z_t is the covariate's level at the end of return t and theta_i0 = gamma_i0 = 0.

**References:**

- Filardo, A.J. (1994). "Business-Cycle Phases and Their Transitional Dynamics." Journal of Business & Economic Statistics, 12(3), 299-308. <https://doi.org/10.1080/07350015.1994.10524545>
- Diebold, F.X., Lee, J.H., Weinbach, G.C. (1994). "Regime Switching with Time-Varying Transition Probabilities." In Hargreaves, C. (ed.), Nonstationary Time Series Analysis and Cointegration, Oxford University Press, 283-302. <https://doi.org/10.1093/oso/9780198773917.003.0010>
- Fama, E.F., Schwert, G.W. (1977). "Asset Returns and Inflation." Journal of Financial Economics, 5(2), 115-146. <https://doi.org/10.1016/0304-405X(77>)90014-9

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_regime_switching_tvtp_em(
    prices: pl.Series,
    price_dates: pl.Series,
    covariate: pl.Series,
    covariate_dates: pl.Series,
    time_step: float,
    n_regimes: int = 2,
    fixed_covariate_sensitivity: list[list[float]] | None = None,
    fixed_regime_means: list[float] | None = None,
    fixed_regime_volatilities: list[float] | None = None,
    max_iterations: int = _MAX_TVTP_EM_ITERATIONS,
    tolerance: float = 1e-06,
) -> RegimeParams
```

**Args:**

- <u>prices (pl.Series):</u> the equity's total-return price history, evenly spaced in time.
- <u>price_dates (pl.Series):</u> the date of each price.
- <u>covariate (pl.Series):</u> the economic series, such as year-over-year inflation as a decimal.
- <u>covariate_dates (pl.Series):</u> the date of each covariate value; only dates both share are used.
- <u>time_step (float):</u> the time between prices, in years.
- <u>n_regimes (int):</u> the number of regimes, default 2.
- <u>fixed_covariate_sensitivity (list[list[float]] &#124; None):</u> slopes gamma to hold fixed, n_regimes x n_regimes with column 0 at zero. Default None, fitted.
- <u>fixed_regime_means (list[float] &#124; None):</u> annual regime means to hold fixed, lowest first. Default None.
- <u>fixed_regime_volatilities (list[float] &#124; None):</u> annual regime volatilities to hold fixed, with `fixed_regime_means`. Default None.
- <u>max_iterations (int):</u> the most fitting rounds.
- <u>tolerance (float):</u> stop once the likelihood improves by less than this.

**Returns:**

<u>RegimeParams:</u> the regime means and volatilities, `tvtp` with the logit coefficients, and as `transition_matrix` the average switching chances over the sample.

**Raises:**

- <u>ValueError:</u> if the inputs differ in length, fewer than `n_regimes * 5` prices share a date with the covariate, a regime collapses or has fewer expected switches than its logit needs, or a fixed input has the wrong shape.

</details>

{% raw %}
#### simulate_regime_path

Draw the sequence of calm and turbulent regimes each scenario passes through, starting from today's most
likely regime.

Each step the market stays in its regime or switches, with the fitted chances. Because regimes persist, a
scenario that enters the turbulent regime tends to stay there for several periods, which produces the
multi-period drawdowns that a single lognormal distribution cannot. The regime path is drawn separately from
the return shocks, so the regime decides each period's mean and volatility while the shock, correlated with
the other factors, decides where in that distribution the return lands. Each equity follows its own regime
path; Ahlgrim, D'Arcy and Gorvett (2005, section 3) note that the regime switches of different equities are
correlated, so small stocks are more likely to be in the low-volatility regime when large stocks are, which
the engine setting `shared_equity_regimes` (on in the default settings) reproduces by
drawing every equity's switches from one random stream. Each scenario starts in the regime most likely at the
last date (a judgement; the alternative, drawing it from the filtered probabilities, adds no data), or, with
`initial_regime_shares`, spread over the regimes in those shares (`starting_regimes`).

The formula is as follows:

$$
s_{t+1} = \text{number of}\; j \;\text{with}\; u_{t} > p_{s_{t}},\;\; \text{0 + ... + p\_s\_t},\;\; \text{j},\;\; u_{t} \sim \operatorname{Uniform}(0,\; 1)
$$

**References:**

- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. <https://doi.org/10.1080/10920277.2001.10595984>
- Alswaidan, A., Jin, C., Varner, J.D. (2026). "Continuous Hidden Markov Models for Equity Returns: Heavy-Tail Emission Families and Regime-Conditional Value-at-Risk." arXiv:2606.23492. <https://arxiv.org/abs/2606.23492>
- Israel, R.B., Rosenthal, J.S., Wei, J.Z. (2001). "Finding Generators for Markov Chains via Empirical Transition Matrices, with Applications to Credit Ratings." Mathematical Finance, 11(2), 245-265. <https://doi.org/10.1111/1467-9965.00114>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
simulate_regime_path(
    params: RegimeParams,
    n_simulations: int,
    n_steps: int,
    rng: np.random.Generator | None,
    simulation_time_step: float | None = None,
    draws: np.ndarray | None = None,
    dtype: type[np.integer] | type[int] = int,
) -> np.ndarray
```

**Args:**

- <u>params (RegimeParams):</u> the calibrated switching chances and today's regime.
- <u>n_simulations (int):</u> the number of scenarios.
- <u>n_steps (int):</u> the number of steps per scenario.
- <u>rng (np.random.Generator &#124; None):</u> the random number generator; unused when `draws` is given.
- <u>simulation_time_step (float &#124; None):</u> the scenario step in years; when it differs from the data frequency the switching chances are converted first (see `rescale_transition_matrix`). Default None, no conversion.
- <u>draws (np.ndarray &#124; None):</u> the uniform draws of shape (n_simulations, n_steps) to switch on instead of drawing them from `rng`, so equities on one shared regime stream share one set. Default None.
- <u>dtype (type):</u> the integer type of the result; np.int8 holds up to 127 regimes in an eighth of the memory. Default int.

**Returns:**

<u>np.ndarray:</u> the regime of every scenario at every step, starting from today's regime.

**Raises:**

- <u>ValueError:</u> if neither `rng` nor `draws` is given.

</details>
{% endraw %}

#### fit_risk_neutral_equity

Set up a risk-neutral equity for market-consistent valuation: a lognormal price that grows at the risk-free
rate minus the dividend yield, with one volatility, as in Black and Scholes (1973) and Merton (1973).

Under the risk-neutral measure every asset is expected to earn the risk-free rate, so the equity risk premium
drops out and the only parameter to choose is the volatility. Discounted at the risk-free rate, the expected
simulated price then equals today's price, which is what a market-consistent valuation of guarantees or
options (for example a Solvency II best estimate) requires. The dividend yield is subtracted because the
holder of the index receives it in cash, not in price. Returns are normal in log terms with no regimes, so
tail risk is set by the volatility alone. This is the provider practice too: Hibbert, Mowbray and Turnbull
(2001), section 9.6, set the mean return of every asset to the risk-free rate and estimate the expected cash
flow of a derivative by Monte Carlo.

The formula is as follows:

$$
\text{dS}_{t} = (r - q) \cdot S_{t} \cdot \text{dt} + \sigma \cdot S_{t} \cdot \text{dW}_{t}
$$

**References:**

- Black, F., Scholes, M. (1973). "The Pricing of Options and Corporate Liabilities." Journal of Political Economy, 81(3), 637-654. <https://doi.org/10.1086/260062>
- Merton, R.C. (1973). "Theory of Rational Option Pricing." Bell Journal of Economics and Management Science, 4(1), 141-183. <https://doi.org/10.2307/3003143>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_risk_neutral_equity(
    risk_free_rate: float,
    dividend_yield: float,
    volatility: float,
    initial_value: float,
) -> FXParams
```

**Args:**

- <u>risk_free_rate (float):</u> today's continuously compounded risk-free rate, annual, as a decimal.
- <u>dividend_yield (float):</u> today's dividend yield, annual, as a decimal.
- <u>volatility (float):</u> the annual volatility, implied by options or realized.
- <u>initial_value (float):</u> today's price.

**Returns:**

<u>FXParams:</u> `drift` (the risk-free rate minus the dividend yield), `volatility` and `initial_value`.

</details>

{% raw %}
#### step_regime_switching

Move an equity price one step forward in the regime the scenario is in, the price step of Hardy's (2001)
regime-switching lognormal model.

Within a regime the log-return is normal, so the price stays positive and returns compound. Between regimes the mean
and volatility jump: a turbulent step can have a volatility two to three times that of a calm one and a mean near zero
or below (11.3% against 3.9% a month in the fit of Ahlgrim, D'Arcy and Gorvett (2005), 0.244 against 0.098 in the base
calibration of Hibbert, Mowbray and Turnbull (2001)). Over a horizon the result is a mixture of normals, with a fatter
left tail and more clustered losses than any single lognormal with the same average volatility. The shock is the
equity's correlated draw, so equities still move with rates, credit and the other factors within a step.

The formula is as follows:

$$
S_{t+dt} = S_{t} \cdot \exp(m + v \cdot z),\;\; m = \mu_{k} \cdot \text{dt},\;\; v = \sigma_{k} \cdot \sqrt{\text{dt}}
$$

Where k is the regime over the step and z the standard normal shock.

**References:**

- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. <https://doi.org/10.1080/10920277.2001.10595984>
- Alswaidan, A., Jin, C., Varner, J.D. (2026). "Continuous Hidden Markov Models for Equity Returns: Heavy-Tail Emission Families and Regime-Conditional Value-at-Risk." arXiv:2606.23492. <https://arxiv.org/abs/2606.23492>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_regime_switching(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    mean: np.ndarray | float,
    volatility: np.ndarray | float,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's price in each scenario.
- <u>shock (np.ndarray &#124; float):</u> the equity's correlated standard normal shock for this step.
- <u>mean (np.ndarray &#124; float):</u> the regime's mean log-return over the step (annual mean times the step).
- <u>volatility (np.ndarray &#124; float):</u> the regime's volatility over the step (annual volatility times the square root of the step).

**Returns:**

<u>np.ndarray:</u> the price at the end of the step.

</details>
{% endraw %}

{% raw %}
#### fit_fx_process

Estimate an exchange rate's annual drift and volatility from its history, for a geometric Brownian motion.

The model assumes the log exchange rate is a random walk with a constant trend: currencies have no natural
level to return to, so shocks are permanent, the spread of outcomes widens with the square root of the horizon
and the rate can never turn negative; FX rates are a geometric Brownian motion in
[Gorvett (2001, p. 40)](https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf). Gorvett
(2001, p. 42) leaves the parameter estimation outside the scope of the paper, so the moment estimates
below are the plain choice.
The estimates are the mean and standard deviation of the log-returns, annualized. The average log-return is the
median growth of the rate, so half the variance is added back to get the expected growth mu. A drift fitted
on a short window extrapolates that window's trend for decades, which is why `random_walk` and `irp` exist.

Rates that are averages over each period (the OECD and Global Macro Database series) smooth the changes: for a
random walk the changes of averages keep only about two-thirds of the variance, as Working (1960)
shows, https://doi.org/10.2307/1907574, so with `period_averages=True` the variance is scaled back up by 3/2.
End-of-period rates need no correction.

The formula is as follows:

$$
r_{t} = \ln(S_{t} / S_{t-1})
$$

$$
\sigma = \operatorname{std}(r_{t}) / \sqrt{\text{dt}},\;\; \text{divided by sqrt(2/3) for period averages}
$$

$$
\mu = \operatorname{mean}(r_{t}) / \text{dt} + \sigma ^{2} / 2
$$

**References:**

- Gorvett, R.W. (2001). "Foreign Exchange Rate Risk: Institutional Issues and Stochastic Modeling." CAS Discussion Paper Program. <https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_fx_process(
    exchange_rate: pl.Series,
    time_step: float,
    period_averages: bool = False,
) -> FXParams
```

**Args:**

- <u>exchange_rate (pl.Series):</u> the historical rate in foreign currency per US dollar, evenly spaced, all above 0.
- <u>time_step (float):</u> the time between observations, in years.
- <u>period_averages (bool):</u> whether each rate is an average over its period rather than the rate at its end. Defaults to False.

**Returns:**

<u>FXParams:</u> the annual drift and volatility, and the latest rate as the starting point.

**Raises:**

- <u>ValueError:</u> if there are fewer than 3 observations or any rate is zero or negative.

</details>
{% endraw %}

{% raw %}
#### step_fx_process

Move the exchange rate one step forward under geometric Brownian motion.

Each step multiplies the rate by a lognormal shock, so the rate stays positive, moves are proportional to its
level and the distribution of future rates is skewed: a currency can appreciate further than it can fall.
The step is exact, so the result does not depend on the simulation frequency.

The formula is as follows:

$$
S_{t+dt} = S_{t} \cdot \exp((\mu - \sigma ^{2} / 2) \cdot \text{dt} + \sigma \cdot \sqrt{\text{dt}} \cdot z)
$$

**References:**

- Gorvett, R.W. (2001). "Foreign Exchange Rate Risk: Institutional Issues and Stochastic Modeling." CAS Discussion Paper Program. <https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_fx_process(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: FXParams,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's exchange rate.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw.
- <u>time_step (float):</u> the step length, in years.
- <u>params (FXParams):</u> the calibrated drift and volatility.

**Returns:**

<u>np.ndarray:</u> the exchange rate one step later, always above zero.

</details>
{% endraw %}

#### fit_fx_process_random_walk

Estimate an exchange rate process with historical volatility but no trend, so the median rate stays at
today's level.

A drift fitted on five or ten years of data mostly reflects that window's dollar cycle; projecting it for decades
would build a strong currency view into every scenario. [Meese and Rogoff
(1983)](https://doi.org/10.1016/0022-1996(83)90017-X) found a random walk forecasts exchange rates out of sample at
least as well as the structural models of the time, so a trend-free rate is the neutral choice for long horizons. The
scenarios still spread out with the historical volatility. Gorvett (2001, p. 40) cites the same finding from Rosenberg
(1996): at short and medium horizons a random walk describes exchange rates better than most fundamentals-based
models. Over long horizons Hibbert, Mowbray and Turnbull (2001, section 9.3, p. 69) have exchange rates respect
purchasing power parity, which also rules out a lasting trend beyond the inflation gap; this is the default
`drift_mode`, and `fit_fx_process_ppp` adds that long-horizon pull.

The formula is as follows:

$$
\mu = \sigma ^{2} / 2,\;\; \text{so}\; d (\text{log}\; S_{t}) = \sigma \cdot \text{dW}_{t}
$$

**References:**

- Meese, R.A. and Rogoff, K. (1983). "Empirical exchange rate models of the seventies: Do they fit out of sample?" Journal of International Economics, 14(1-2), 3-24. <https://doi.org/10.1016/0022-1996(83>)90017-X
- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert Limited, section 9.3. <https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_fx_process_random_walk(
    exchange_rate: pl.Series,
    time_step: float,
    period_averages: bool = False,
) -> FXParams
```

**Args:**

- <u>exchange_rate (pl.Series):</u> the historical rate in foreign currency per US dollar, evenly spaced, all above 0.
- <u>time_step (float):</u> the time between observations, in years.
- <u>period_averages (bool):</u> whether each rate is a period average; see `fit_fx_process`. Defaults to False.

**Returns:**

<u>FXParams:</u> the historical volatility, the latest rate and a drift that leaves the median rate flat.

**Raises:**

- <u>ValueError:</u> if there are fewer than 3 observations or any rate is zero or negative.

</details>

{% raw %}
#### step_fx_process_irp

Move the exchange rate one step forward with its trend set by the simulated interest rate gap (uncovered
interest rate parity).

Uncovered interest rate parity says the higher-rate currency is expected to weaken by about the rate gap, so a
holder of the foreign currency earns the same expected return as at home. Measured in dollars that holder earns a
little more, the variance sigma^2 a year, because a currency's expected move and its reciprocal's cannot both be
zero (Siegel (1972)); the risk-neutral step adds that term (`step_fx_process_risk_neutral`). Tying the trend to
the two simulated short rates makes currencies respond to the rate scenarios: when US rates rise relative to the
foreign rate, the dollar is expected to weaken over the following period, and FX and rates stay consistent in every
path. Parity is a
long-run tendency rather than a short-run law (the carry trade profits from its failure), so treat this as a
structural, not a forecasting, choice. Gorvett (2001, p. 43) states parity as equal returns in the two
currencies once the expected change in the exchange rate is counted. Barrie & Hibbert's model instead makes
exchange rates respect purchasing power parity over long horizons in Hibbert, Mowbray and
Turnbull (2001, section 9.3), which `drift_mode: ppp` does (`step_fx_process_ppp`).

The formula is as follows:

$$
S_{t+dt} = S_{t} \cdot \exp((r_{f},\; t - r_{d},\; t - \sigma ^{2} / 2) \cdot \text{dt} + \sigma \cdot \sqrt{\text{dt}} \cdot z)
$$

Where S is units of foreign currency per US dollar, r_f the foreign and r_d the US short rate: a higher US rate
makes the quote fall, the same direction as the risk-neutral drift.

**References:**

- Gorvett, R.W. (2001). "Foreign Exchange Rate Risk: Institutional Issues and Stochastic Modeling." CAS Discussion Paper Program. <https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf>
- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert Limited, section 9.3. <https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf>
- Siegel, J.J. (1972). "Risk, Interest Rates and the Forward Exchange." Quarterly Journal of Economics, 86(2), 303-309. <https://doi.org/10.2307/1880565>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_fx_process_irp(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: FXParams,
    rate_differential: np.ndarray | float,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's exchange rate.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw.
- <u>time_step (float):</u> the step length, in years.
- <u>params (FXParams):</u> the calibrated volatility; the fitted drift is not used.
- <u>rate_differential (np.ndarray &#124; float):</u> the simulated foreign short rate minus the US short rate, annual.

**Returns:**

<u>np.ndarray:</u> the exchange rate one step later, always above zero.

</details>
{% endraw %}

{% raw %}
#### step_fx_process_risk_neutral

Move the exchange rate one step forward under the risk-neutral measure of a US dollar investor, the measure the
run's discounting uses.

A foreign deposit grows at the foreign short rate; converted to dollars and discounted at the US rate it must keep
its value on average, or the scenarios would price in a free profit. Garman and Kohlhagen (1983) give the drift
that does this for the dollar price of the foreign currency, 1 / S, which grows at the US minus the foreign rate.
For S itself, foreign currency per dollar, the drift is the foreign minus the US rate plus the variance: the
reciprocal of a lognormal rate gains sigma^2 a year in expectation (Siegel (1972)). Each step takes the rates the
scenario starts the step at, the left-endpoint step the discounting reads, so the deposit is a martingale in every
path, not only at today's rates.

The formula is as follows:

$$
S_{t+dt} = S_{t} \cdot \exp((r_{f},\; t - r_{d},\; t + \sigma ^{2} / 2) \cdot \text{dt} + \sigma \cdot \sqrt{\text{dt}} \cdot z)
$$

$$
1 / S_{t+dt} = (1 / S_{t}) \cdot \exp((r_{d},\; t - r_{f},\; t - \sigma ^{2} / 2) \cdot \text{dt} - \sigma \cdot \sqrt{\text{dt}} \cdot z)
$$

Where S is units of foreign currency per US dollar, r_f the foreign and r_d the US short rate at the start of the
step; the second line is Garman and Kohlhagen's dollar price of one unit of foreign currency.

**References:**

- Garman, M.B., Kohlhagen, S.W. (1983). "Foreign currency option values." Journal of International Money and Finance, 2(3), 231-237. <https://doi.org/10.1016/S0261-5606(83>)80001-1
- Siegel, J.J. (1972). "Risk, Interest Rates and the Forward Exchange." Quarterly Journal of Economics, 86(2), 303-309. <https://doi.org/10.2307/1880565>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_fx_process_risk_neutral(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: FXParams,
    rate_differential: np.ndarray | float,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's exchange rate, in foreign currency per US dollar.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw.
- <u>time_step (float):</u> the step length, in years.
- <u>params (FXParams):</u> the calibrated volatility; the fitted drift is not used.
- <u>rate_differential (np.ndarray &#124; float):</u> the foreign minus the US short rate at the start of the step, annual.

**Returns:**

<u>np.ndarray:</u> the exchange rate one step later, always above zero.

</details>
{% endraw %}

#### fit_ppp_level

How far today's real exchange rate sits from its average over the history: the log move the real rate is expected
to make back toward purchasing power parity.

The real exchange rate is the rate adjusted for the two price levels. The studies Rogoff (1996, section 5) surveys
find it reverting to its long-run average, so a dollar that buys more abroad than it usually has is expected to
lose that edge over a few years. The average is taken over the same window the volatility is fitted on.

The formula is as follows:

$$
q_{t} = \ln(S_{t}) - \ln(P_{f}(t) / P_{us}(t))
$$

$$
g = \operatorname{mean}(q_{t}) - (\ln(S_{T}) - \ln(P_{f}(L) / P_{us}(L)))
$$

Where S is the rate in foreign currency per US dollar, P_f and P_us the foreign and US consumer price indices, T the
last exchange rate and L the last date with both price indices, so prices are taken as unchanged since.

**References:**

- Rogoff, K. (1996). "The Purchasing Power Parity Puzzle." Journal of Economic Literature, 34(2), 647-668, section 5. <https://ideas.repec.org/a/aea/jeclit/v34y1996i2p647-668.html>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_ppp_level(exchange_rate: pl.Series, price_ratio: pl.Series) -> float
```

**Args:**

- <u>exchange_rate (pl.Series):</u> the historical rate in foreign currency per US dollar, all above 0.
- <u>price_ratio (pl.Series):</u> the foreign over the US consumer price index on the same dates, null where missing.

**Returns:**

<u>float:</u> g, the log distance from today's real exchange rate to its historical average.

**Raises:**

- <u>ValueError:</u> if the two series differ in length, fewer than 3 dates have both, or a value is zero or negative.

</details>

{% raw %}
#### fit_fx_process_ppp

Estimate an exchange rate process that moves like a random walk from month to month but respects purchasing power
parity over decades.

Over a month or a year a currency moves as a random walk, which forecasts exchange rates out of sample at least as
well as the structural models of the time in [Meese and Rogoff (1983)](https://doi.org/10.1016/0022-1996(83)90017-X).
Over decades a random walk lets the spread of outcomes grow without limit, to levels a currency pair has never
reached. Real exchange rates do revert: the long-horizon studies surveyed in [Rogoff
(1996)](https://ideas.repec.org/a/aea/jeclit/v34y1996i2p647-668.html) agree on a half-life of three to five years
(section 5.B, p. 656), deviations fading at roughly 15% a year (section 5.C, pp. 657-658), and the short-run
volatility of real exchange rates is of the same order as that of nominal ones (section 1, p. 647). So the
volatility is the rate's own historical one and the half-life is that consensus. With the two consumer price indices
the real rate reverts to its average over the same history (`fit_ppp_level`), the purchasing power parity level of
those studies; without them it reverts to today's, no view on whether the dollar is dear, only that its value
follows the inflation gap. Exchange rates respect purchasing power parity at long horizons in Hibbert, Mowbray and
Turnbull (2001, section 9.3), and Gorvett (2001, p. 44) points to it as a long-run equilibrium a model can impose
while allowing short-term deviations.

The formula is as follows:

$$
\sigma = \operatorname{std}(r_{t}) / \sqrt{\text{dt}}
$$

$$
\kappa = \ln(2) / \text{half\_life}
$$

$$
g = \operatorname{mean}(q_{t}) - q_{T}
$$

Where r_t are the log changes of the rate, as in `fit_fx_process`, and g the real rate's average minus today's,
0 without price indices.

**References:**

- Rogoff, K. (1996). "The Purchasing Power Parity Puzzle." Journal of Economic Literature, 34(2), 647-668, sections 1 and 5. <https://ideas.repec.org/a/aea/jeclit/v34y1996i2p647-668.html>
- Meese, R.A. and Rogoff, K. (1983). "Empirical exchange rate models of the seventies: Do they fit out of sample?" Journal of International Economics, 14(1-2), 3-24. <https://doi.org/10.1016/0022-1996(83>)90017-X
- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert Limited, section 9.3. <https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_fx_process_ppp(
    exchange_rate: pl.Series,
    time_step: float,
    period_averages: bool = False,
    half_life: float = PPP_HALF_LIFE_YEARS,
    price_ratio: pl.Series | None = None,
) -> FXPPPParams
```

**Args:**

- <u>exchange_rate (pl.Series):</u> the historical rate in foreign currency per US dollar, evenly spaced, all above 0.
- <u>time_step (float):</u> the time between observations, in years.
- <u>period_averages (bool):</u> whether each rate is a period average; see `fit_fx_process`. Defaults to False.
- <u>half_life (float):</u> the years for half of a deviation from parity to fade. Defaults to 4.0, the middle of Rogoff's (1996, section 5.B, p. 656) three to five years.
- <u>price_ratio (pl.Series &#124; None):</u> the foreign over the US consumer price index on the exchange rate's dates, for the real rate's historical average; None reverts to today's real rate. Defaults to None.

**Returns:**

<u>FXPPPParams:</u> the historical volatility, the latest rate, the reversion speed, the long-run deviation, and a drift that leaves the median rate flat, kept for comparison.

**Raises:**

- <u>ValueError:</u> if there are fewer than 3 observations, any rate is zero or negative, the half-life is not a positive number, or `price_ratio` does not line up with the rate.

</details>
{% endraw %}

#### step_fx_process_ppp

Move the exchange rate one step forward: by the inflation gap between the two currencies, plus the change in its
real value, which is pulled toward its long-run level.

A currency whose inflation runs higher loses value by the gap, the relative form of purchasing power parity; on top
of that the real exchange rate takes the same random shocks as a random walk, but its distance from the long-run
level fades with a half-life of ln(2) / kappa years. Over a month the pull is a fraction of a percent, so the rate
still moves like a random walk; over decades the real rate settles into a stable range of standard deviation
sigma / sqrt(2 * kappa) around that level instead of widening without limit. The step of the real rate is exact,
so the result does not depend on the simulation frequency, and the rate stays positive.

The formula is as follows:

$$
q_{t+dt} = g + (q_{t} - g) \cdot \exp(- \kappa \cdot \text{dt}) + \sigma \cdot \sqrt{(1 - \exp(- 2 \cdot \kappa \cdot \text{dt})) / (2 \cdot \kappa)} \cdot z
$$

$$
S_{t+dt} = S_{t} \cdot \exp((\ln(1 + \pi_{f}(t)) - \ln(1 + \pi_{us}(t))) \cdot \text{dt} + q_{t+dt} - q_{t})
$$

Where q is the log real exchange rate's deviation from today's, g the long-run deviation, and pi_f and pi_us the
foreign and US inflation rates at the start of the step, year-over-year rates whose price indices grow by
ln(1 + pi) a year (`ScenarioSet.cumulative_index`).

**References:**

- Rogoff, K. (1996). "The Purchasing Power Parity Puzzle." Journal of Economic Literature, 34(2), 647-668, section 5. <https://ideas.repec.org/a/aea/jeclit/v34y1996i2p647-668.html>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_fx_process_ppp(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: FXPPPParams,
    real_deviation: np.ndarray | float,
    inflation_gap: np.ndarray | float,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's exchange rate, in foreign currency per US dollar.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw.
- <u>time_step (float):</u> the step length, in years.
- <u>params (FXPPPParams):</u> the volatility, the speed of the pull and the long-run level.
- <u>real_deviation (np.ndarray &#124; float):</u> q_t, the log real exchange rate's deviation from its starting level.
- <u>inflation_gap (np.ndarray &#124; float):</u> ln(1 + pi_f) - ln(1 + pi_us) over the step, the yearly gap between the two price indices' log growth.

**Returns:**

<u>np.ndarray:</u> the exchange rate one step later, always above zero.

</details>

#### fit_commodity_process

Estimate a commodity's mean-reverting price model from its spot price history, after Schwartz (1997).

A commodity, unlike a stock index, has a natural price level: when the price is high, producers expand supply and
inventories build, and the convenience yield of holding the physical good falls, so the price is pulled back
toward its cost of production and storage. The model lets the log price revert to a long-run level at speed kappa,
which keeps the price positive and makes price spikes temporary. This is the first, one-factor model of Schwartz
(1997), who also reports strong mean reversion in the commercial commodities (copper and oil). The fit
is a regression of each period's change in log price on the previous level; the slope gives the speed, the
intercept the long-run level and the residuals the volatility, using the exact discrete form of the process so the
time step adds no bias, and the speed has the finite-sample bias of Tang and Chen (2009, Theorem 3.1.1) taken off
(`ou_speed_bias`): about 4 / T a year over T years, so on 27 years of Brent the half-life rises from about 1.0 to
1.4 years. Schwartz estimates the model from futures prices with a Kalman filter;
regressing on the spot (front-month) price is a judgement that needs no futures history, and it includes each
month's roll from one contract to the next.

The formula is as follows:

$$
X_{t+1} - X_{t} = c + b \cdot X_{t} + e_{t},\;\; X_{t} = \ln(S_{t})
$$

$$
\kappa = - \ln(1 + b) / \text{dt} - (5 / 2 + (1 + b) ^{-1} + (1 + b) ^{-2} / 2) / (n \cdot \text{dt}),\;\; \mu = - c / b
$$

$$
\sigma = \operatorname{std}(e_{t}) / \sqrt{(1 - \exp(- 2 \cdot \kappa \cdot \text{dt})) / (2 \cdot \kappa)}
$$

A price that trends rather than reverts at the chosen frequency gives no pull to estimate and raises an error.

**References:**

- Schwartz, E.S. (1997). "The Stochastic Behavior of Commodity Prices: Implications for Valuation and Hedging." Journal of Finance, 52(3), 923-973. <https://doi.org/10.1111/j.1540-6261.1997.tb02721.x>
- Tang, C.Y., Chen, S.X. (2009). "Parameter estimation and bias correction for diffusion processes." Journal of Econometrics, 149(1), 65-81. Section 3.1, Theorem 3.1.1. <https://doi.org/10.1016/j.jeconom.2008.11.001>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_commodity_process(prices: pl.Series, time_step: float) -> CommodityParams
```

**Args:**

- <u>prices (pl.Series):</u> the historical spot price, evenly spaced, all above 0.
- <u>time_step (float):</u> the time between observations, in years.

**Returns:**

<u>CommodityParams:</u> the reversion speed, the long-run log price, the log-price volatility and today's price as the starting point.

**Raises:**

- <u>ValueError:</u> if the history is too short, a price is zero or negative, or the price shows no mean reversion.

</details>

#### step_commodity_process

Move a commodity's spot price one step forward under the Schwartz (1997) mean-reverting model.

The log price is pulled toward its long-run level, so a spike above the normal price is expected to fade (a gap
halves in ln(2) / kappa years) while the shock keeps prices volatile. Over long horizons the price settles into a
stable lognormal range around exp(mu), rather than drifting without limit as an equity index does; that makes
commodity scenarios narrower at 30 years than a random walk with the same short-term volatility. The step is exact,
so the result does not depend on the simulation frequency, and the price is always positive.

The formula is as follows:

$$
X_{t+dt} = \mu + (X_{t} - \mu) \cdot \exp(- \kappa \cdot \text{dt}) + \sigma \cdot \sqrt{(1 - \exp(- 2 \cdot \kappa \cdot \text{dt})) / (2 \cdot \kappa)} \cdot z
$$

$$
S_{t+dt} = \exp(X_{t+dt})
$$

**References:**

- Schwartz, E.S. (1997). "The Stochastic Behavior of Commodity Prices: Implications for Valuation and Hedging." Journal of Finance, 52(3), 923-973. <https://doi.org/10.1111/j.1540-6261.1997.tb02721.x>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_commodity_process(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: CommodityParams,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's spot price, above 0.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw.
- <u>time_step (float):</u> the step length, in years.
- <u>params (CommodityParams):</u> the reversion speed, long-run log price and log-price volatility.

**Returns:**

<u>np.ndarray:</u> the spot price one step later, always above zero.

</details>

{% raw %}
#### fit_commodity_random_walk

Estimate the volatility of a commodity whose price behaves like an asset's, a random walk with no level to return
to, and leave its median real price at today's level.

Schwartz's (1997) pull toward a long-run price rests on supply and the convenience yield: a high oil price brings
out new supply and draws down inventories. Gold's supply barely responds: about 2,500 tonnes are mined a year,
which adds about 1.5% a year to an above-ground stock of about 171,300 tonnes (Erb and Harvey, 2013, pp. 28-29),
and that supply did not rise while the price rose fivefold in the decade to 2012 (p. 10). Fitted by regression,
gold's history since 2000 shows a trend rather than a pull: on GC=F daily data to 2026-10-16 the single-factor fit
settles at 24,103 USD with a half-life of 21 years, far above its year-end prices of 272 to 4,341 USD, a level set
by the run-up since 2000 rather than by any force pulling the price back. Over the long run gold has kept its
purchasing power, Jastram's golden constant of a long-run real return of about zero (p. 11), while its real price
swings about as much as its nominal one (p. 12). Linked to an inflation factor, the price therefore drifts with
simulated inflation and its median real price stays at today's level; without one, its median price does. A pull
back toward an average real price would rest on what is arguably one historical episode, the fall after 1980, as
Erb and Harvey (2013, p. 15) caution, so none is fitted.

The formula is as follows:

$$
r_{t} = \ln(S_{t} / S_{t-1})
$$

$$
\sigma = \operatorname{std}(r_{t}) / \sqrt{\text{dt}}
$$

$$
\mu = \sigma ^{2} / 2
$$

**References:**

- Erb, C.B., Harvey, C.R. (2013). "The Golden Dilemma." Financial Analysts Journal, 69(4), 10-42, pp. 10-12, 15 and 28-29. <https://doi.org/10.2469/faj.v69.n4.1>
- Schwartz, E.S. (1997). "The Stochastic Behavior of Commodity Prices: Implications for Valuation and Hedging." Journal of Finance, 52(3), 923-973. <https://doi.org/10.1111/j.1540-6261.1997.tb02721.x>
- Tang, C.Y., Chen, S.X. (2009). "Parameter estimation and bias correction for diffusion processes." Journal of Econometrics, 149(1), 65-81. Section 3.1, Theorem 3.1.1. <https://doi.org/10.1016/j.jeconom.2008.11.001>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_commodity_random_walk(prices: pl.Series, time_step: float) -> CommodityRandomWalkParams
```

**Args:**

- <u>prices (pl.Series):</u> the historical spot price, evenly spaced, all above 0.
- <u>time_step (float):</u> the time between observations, in years.

**Returns:**

<u>CommodityRandomWalkParams:</u> the log-price volatility, today's price, and a drift that keeps the median real price flat.

**Raises:**

- <u>ValueError:</u> if there are fewer than 3 observations or a price is zero or negative.

</details>
{% endraw %}

{% raw %}
#### step_commodity_random_walk

Move a commodity's price one step forward as a random walk that drifts with inflation.

Each step adds the price index's log growth, ln(1 + inflation), and a lognormal shock, so the price stays positive and
has no level to return to: a fall is as permanent as a rise, as for an equity index. With the fitted drift the median
real price stays at today's level, Jastram's golden constant as Erb and Harvey (2013, p. 11) describe it. The step is
exact for the inflation rate held over the step, so the result does not depend on the simulation frequency beyond
that.

The formula is as follows:

$$
S_{t+dt} = S_{t} \cdot \exp((\ln(1 + \pi_{t}) + \mu - \sigma ^{2} / 2) \cdot \text{dt} + \sigma \cdot \sqrt{\text{dt}} \cdot z)
$$

**References:**

- Erb, C.B., Harvey, C.R. (2013). "The Golden Dilemma." Financial Analysts Journal, 69(4), 10-42, p. 11. <https://doi.org/10.2469/faj.v69.n4.1>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_commodity_random_walk(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: CommodityRandomWalkParams,
    inflation: np.ndarray | float = 0.0,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's price, above 0.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw.
- <u>time_step (float):</u> the step length, in years.
- <u>params (CommodityRandomWalkParams):</u> the drift above inflation and the volatility.
- <u>inflation (np.ndarray &#124; float):</u> the annual inflation rate over the step, 0 without a linked inflation factor. Defaults to 0.0.

**Returns:**

<u>np.ndarray:</u> the price one step later, always above zero.

</details>
{% endraw %}

#### fit_schwartz_smith_process

Estimate the Schwartz and Smith (2000) two-factor commodity model from a spot price history.

The model splits the log price into a short-term deviation chi, which fades back to zero, and a long-term level
xi, which drifts as a random walk. That matches how commodity markets behave: a supply outage or a cold winter moves
the front of the futures curve but barely touches the long end, while a change in production technology or demand
shifts the whole curve for good. In the scenarios, short-term shocks fade but long-term uncertainty keeps growing
with the horizon.

The paper estimates both parts from years of futures prices with a Kalman filter. In its section 2, changes in the
short-term deviation are temporary price moves that are not expected to last, such as unusual weather or a supply
disruption, while changes in the equilibrium level are fundamental and expected to persist. Without that history, xi
is proxied by a trailing average of the log price and chi by the deviation from it; chi is then fitted as a
mean-reverting process around zero and xi as a random walk with drift.

The formula is as follows:

$$
\xi_{t} = \operatorname{mean}(\text{ln}\; S_{s})
$$

$$
\chi_{t} = \ln(S_{t}) - \xi_{t}
$$

$$
\chi_{t+1} - \chi_{t} = b \cdot \chi_{t} + e_{t},\;\; \kappa = - \ln(1 + b) / \text{dt}
$$

$$
\sigma_{\chi} = \operatorname{std}(e_{t}) / \sqrt{(1 - \exp(- 2 \cdot \kappa \cdot \text{dt})) / (2 \cdot \kappa)}
$$

$$
\rho = \operatorname{corr}(e_{t},\; \xi_{t+1} - \xi_{t})
$$

The mean runs over the last w observations s up to t, with w = long_term_window_years / dt.

The reversion speed and today's split between the two parts are reliable. The volatilities, their correlation and
the long-term drift are not: averaging smooths the long-term level, so its volatility comes out far too small (0.6%
a year for WTI on 2026-10-14, against 14.5% in Schwartz and Smith's Table 2). When a futures curve is available,
the volatilities and correlation are refitted from the futures contracts instead.

**References:**

- Schwartz, E., Smith, J.E. (2000). "Short-Term Variations and Long-Term Dynamics in Commodity Prices." Management Science, 46(7), 893-911. <https://doi.org/10.1287/mnsc.46.7.893.12034>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_schwartz_smith_process(
    prices: pl.Series,
    time_step: float,
    long_term_window_years: float = 3.0,
) -> tuple[SchwartzSmithParams, float, np.ndarray, np.ndarray]
```

**Args:**

- <u>prices (pl.Series):</u> the historical spot price, evenly spaced, all above 0.
- <u>time_step (float):</u> the time between observations, in years.
- <u>long_term_window_years (float):</u> the years of prices averaged into the long-term level. The 3-year default is a judgement: long enough to average out short-term deviations, whose half-life is ln 2 / kappa (about half a year at Schwartz and Smith's kappa of 1.49), short enough to follow the long-term level. Their three-factor note reports a half-life of about 3 years, but only for the equilibrium growth rate.

**Returns:**

<u>tuple[SchwartzSmithParams, float, np.ndarray, np.ndarray]:</u> the two fitted parts, the correlation of their shocks, and the history of each part's period changes.

**Raises:**

- <u>ValueError:</u> if the history is shorter than the averaging window, a price is zero or negative, or the short-term part shows no mean reversion.

</details>

#### fit_schwartz_smith_diffusion_from_forward_curve

Estimate the volatilities of the short-term and long-term commodity factors, and their correlation, from how much
each futures contract has moved.

In the Schwartz and Smith (2000) model the volatility of a futures contract depends on its maturity: near
contracts carry the full short-term shock, while the short-term part has faded out of distant contracts, leaving
only the long-term volatility. So the term structure of futures volatilities pins down both parts, which the spot
history alone cannot separate. Each contract's own recent volatility is matched to the model, with the reversion
speed taken from the spot fit; the relation is then linear, so one least-squares fit recovers the three values.

The formula is as follows:

$$
\sigma ^{2} (F_{T}) = \exp(- 2 \cdot \kappa \cdot T) \cdot \sigma_{\chi} ^{2} + \sigma_{\xi} ^{2} + 2 \cdot \exp(- \kappa \cdot T) \cdot \rho \cdot \sigma_{\chi} \cdot \sigma_{\xi}
$$

Schwartz and Smith (2000, section 3.1) derive this from their futures price (eq. 9): the
volatility does not depend on the state variables, and for a contract at maturity (T = 0) it equals the volatility
of the sum of the short- and long-term factors. Fixing kappa is a judgement: with the dozen or
so maturities a futures curve has, also fitting kappa overstated it about sevenfold in this package's own
simulation check, while this fit was unbiased. The correlation is the least precise of the three.

**References:**

- Schwartz, E., Smith, J.E. (2000). "Short-Term Variations and Long-Term Dynamics in Commodity Prices." Management Science, 46(7), 893-911. <https://doi.org/10.1287/mnsc.46.7.893.12034>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_schwartz_smith_diffusion_from_forward_curve(
    maturities: np.ndarray,
    volatilities: np.ndarray,
    kappa: float,
) -> tuple[float, float, float]
```

**Args:**

- <u>maturities (np.ndarray):</u> each listed futures contract's time to expiry, in years.
- <u>volatilities (np.ndarray):</u> each contract's recent annualized volatility, in the same order; at least 3.
- <u>kappa (float):</u> the short-term part's reversion speed, from the spot fit.

**Returns:**

<u>tuple[float, float, float]:</u> the short-term volatility, the long-term volatility and their correlation.

**Raises:**

- <u>ValueError:</u> if fewer than 3 maturities are supplied.

</details>

#### long_term_volatility_from_contract

The long-term factor's volatility implied by one futures contract's volatility, given the short-term factor's
volatility, speed and correlation: the futures volatility formula of Schwartz and Smith (2000) solved for
sigma_xi.

As the maturity grows, a contract's instantaneous volatility approaches that of the equilibrium price level, sigma_xi,
as Schwartz and Smith (2000, section 3.1) show. The longest listed contract is therefore the one that measures
sigma_xi best when the three-parameter fit to the whole curve cannot separate the two factors. A spot price history
alone smooths the long-term level away: on WTI on 2026-10-14 it gave 0.6% a year against about 20% from the longest
contract, where Schwartz and Smith's own oil estimates are 14.5% (futures data) and 11.5% (Enron data) in Table 2.

The formula is as follows:

$$
\sigma ^{2} (F_{T}) = \exp(- 2 \cdot \kappa \cdot T) \cdot \sigma_{\chi} ^{2} + \sigma_{\xi} ^{2} + 2 \cdot \exp(- \kappa \cdot T) \cdot \rho \cdot \sigma_{\chi} \cdot \sigma_{\xi}
$$

$$
\sigma_{\xi} = - d \cdot \rho \cdot \sigma_{\chi} + \sqrt{\sigma ^{2} (F_{T}) - d ^{2} \cdot \sigma_{\chi} ^{2} \cdot (1 - \rho ^{2})},\;\; d = \exp(- \kappa \cdot T)
$$

Where sigma(F_T) is the contract's volatility; when the root has no positive solution the contract's own
volatility is returned, its value as T grows.

**References:**

- Schwartz, E., Smith, J.E. (2000). "Short-Term Variations and Long-Term Dynamics in Commodity Prices." Management Science, 46(7), 893-911. <https://doi.org/10.1287/mnsc.46.7.893.12034>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
long_term_volatility_from_contract(
    maturity: float,
    contract_volatility: float,
    kappa: float,
    sigma_chi: float,
    rho: float,
) -> float
```

**Args:**

- <u>maturity (float):</u> the contract's time to expiry, in years.
- <u>contract_volatility (float):</u> the contract's recent annualized volatility.
- <u>kappa (float):</u> the short-term factor's reversion speed.
- <u>sigma_chi (float):</u> the short-term factor's volatility.
- <u>rho (float):</u> the correlation of the two factors' shocks.

**Returns:**

<u>float:</u> the long-term factor's annual volatility.

</details>

{% raw %}
#### fit_schwartz_smith_risk_neutral

Fit the risk-neutral version of the Schwartz and Smith (2000) model to today's futures curve, for pricing and
hedging.

Under the risk-neutral measure the model must reproduce today's futures prices, so the curve's shape sets the two
drifts. A curve that slopes down (backwardation, typical when inventories are tight and the convenience yield is
high) gives a negative drift; one that slopes up (contango, ample storage) a positive one. The speed, volatilities
and correlation are the same under both measures, so they come from the real-world fit; only the short-term risk
premium lambda_chi and the risk-adjusted long-term drift mu_Q are fitted here. The paper's futures price
(eq. 9) is linear in those two, so ordinary least squares over the listed maturities recovers them.

The formula is as follows:

$$
d\chi_{t} = (- \kappa \cdot \chi_{t} - \lambda_{\chi}) \cdot \text{dt} + \sigma_{\chi} \cdot \text{dW}_{t} ^{\chi}
$$

$$
d\xi_{t} = \mu_{Q} \cdot \text{dt} + \sigma_{\xi} \cdot \text{dW}_{t} ^{\xi}
$$

$$
\text{ln}\; F (0,\; T) = \exp(- \kappa \cdot T) \cdot \chi_{0} + \xi_{0} + A(T)
$$

$$
A(T) = - (1 - \exp(- \kappa \cdot T)) / \kappa \cdot \lambda_{\chi} + \mu_{Q} \cdot T + (V_{\chi} + V_{\xi} + 2 \cdot V_{\text{cross}}) / 2
$$

$$
V_{\chi} = \sigma_{\chi} ^{2} \cdot (1 - \exp(- 2 \cdot \kappa \cdot T)) / (2 \cdot \kappa),\;\; V_{\xi} = \sigma_{\xi} ^{2} \cdot T
$$

$$
V_{\text{cross}} = \rho \cdot \sigma_{\chi} \cdot \sigma_{\xi} \cdot (1 - \exp(- \kappa \cdot T)) / \kappa
$$

Where, under Q, chi is an OU process reverting to -lambda_chi / kappa and xi drifts at mu_Q, and W is the
risk-neutral Brownian motion.

**References:**

- Schwartz, E., Smith, J.E. (2000). "Short-Term Variations and Long-Term Dynamics in Commodity Prices." Management Science, 46(7), 893-911. <https://doi.org/10.1287/mnsc.46.7.893.12034>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_schwartz_smith_risk_neutral(
    maturities: np.ndarray,
    forward_prices: np.ndarray,
    chi_0: float,
    xi_0: float,
    kappa: float,
    sigma_chi: float,
    sigma_xi: float,
    rho: float,
) -> SchwartzSmithParams
```

**Args:**

- <u>maturities (np.ndarray):</u> each traded futures contract's time to expiry, in years.
- <u>forward_prices (np.ndarray):</u> each contract's price today, in the same order, all above 0.
- <u>chi_0 (float):</u> today's short-term deviation, from the real-world fit.
- <u>xi_0 (float):</u> today's long-term log price, from the real-world fit.
- <u>kappa (float):</u> the short-term part's reversion speed, from the real-world fit.
- <u>sigma_chi (float):</u> the short-term volatility, from the real-world fit.
- <u>sigma_xi (float):</u> the long-term volatility, from the real-world fit.
- <u>rho (float):</u> the correlation of the two parts' shocks, from the real-world fit.

**Returns:**

<u>SchwartzSmithParams:</u> the two parts under the risk-neutral measure, with the real-world speed and volatilities and the drifts implied by today's futures curve.

**Raises:**

- <u>ValueError:</u> if fewer than 2 maturities are supplied or a futures price is zero or negative.

</details>
{% endraw %}

#### fit_rate_link

Estimate how much house-price growth slows in the year after long-term interest rates rise, from decades of history.

Higher rates make mortgages dearer and cool the housing market with a delay: Iacoviello (2005, section I, Figure 1,
p. 741) finds that tighter money lowers real house prices in US data from 1974 to 2003. This fit measures the
link on the growth rate the package simulates, with the long rate, which mortgage rates follow, as the driver.
Each quarter's year-over-year growth is regressed on its own value a year earlier and the long rate's change over
the year ending `lag_steps` earlier: the year-apart regression of `fit_ou_process_with_covariate`, since
neighbouring year-over-year readings share three of their four quarters and would otherwise pass for persistence.
On US data from 1971 to 2026 a one-point rise in the long rate lowers growth by about 0.8 points a year later.

The formula is as follows:

$$
g(t) = c + Q \cdot g(\text{t-k}) + \beta \cdot (L(\text{t-l}) - L(\text{t-l-k})) + e(t)
$$

Where k is `steps_per_year`, l `lag_steps`, g growth and L the long rate. The share the link explains is the drop
in residual variance against the same regression without it.

**References:**

- Iacoviello, M. (2005). "House Prices, Borrowing Constraints, and Monetary Policy in the Business Cycle." American Economic Review, 95(3), 739-764. <https://doi.org/10.1257/0002828054201477>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_rate_link(
    dates: pl.Series,
    growth: pl.Series,
    long_rate: pl.Series,
    steps_per_year: int = 4,
    lag_steps: int = RATE_LINK_LAG_QUARTERS,
) -> RateLinkFit
```

**Args:**

- <u>dates (pl.Series):</u> the dates of the observations, evenly spaced and in order.
- <u>growth (pl.Series):</u> year-over-year house-price growth on those dates, as decimals.
- <u>long_rate (pl.Series):</u> the long-term interest rate on those dates, as decimals.
- <u>steps_per_year (int):</u> k, observations per year. Defaults to 4 (quarterly).
- <u>lag_steps (int):</u> l, the observations between the rate move and the response. Defaults to four quarters.

**Returns:**

<u>RateLinkFit:</u> the sensitivity, its standard error and the variance it explains.

**Raises:**

- <u>ValueError:</u> if the series differ in length or fewer than `MINIMUM_RATE_LINK_PAIRS` pairs have every value.

</details>

#### step_rate_linked_ou

Move house-price growth one step forward: the exact mean-reverting step plus the push from the long rate's move a
year earlier, so a scenario whose rates climb sees its house prices cool the following year.

The formula is as follows:

$$
g(t + \text{dt}) = \theta + (g(t) - \theta) \cdot \exp(- a \cdot \text{dt}) + w \cdot \beta \cdot \text{dL} + \sigma \cdot \sqrt{(1 - \exp(- 2a \cdot \text{dt})) / (2a)} \cdot z
$$

Where dL is the long rate's change over one step `lag` years earlier, w = `yearly_sensitivity_weight(a, dt)` and
z a standard normal draw.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_rate_linked_ou(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: RateLinkedOUParams,
    rate_change: np.ndarray | float,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's growth rate.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw.
- <u>time_step (float):</u> the step length, in years.
- <u>params (RateLinkedOUParams):</u> the fitted process and link.
- <u>rate_change (np.ndarray &#124; float):</u> dL, the long rate's change over one step, `lag` years earlier.

**Returns:**

<u>np.ndarray:</u> the growth rate one step later.

</details>

{% raw %}
#### fit_volatility_regimes

Find a calm and a turbulent regime in the shocks to house prices, so the scenarios hold their long quiet stretches
and their booms and busts rather than one bell curve of shocks.

The regimes are read from quarter-on-quarter growth of the house-price index, the data Crawford and Fratantoni
(2003) fit their regime-switching model to: each quarter is a new observation, so Hamilton's (1989) filter sees as
many independent shocks as there are quarters. Year-over-year growth sampled every quarter would not do: each
reading shares three quarters with the one before, so its residuals are strongly autocorrelated (0.89 at one
quarter) and two regimes beat one shock by a log-likelihood of about 57 even on data with one constant volatility.
Quarterly log growth follows an autoregression whose shock size switches between two regimes (Hamilton's model with
a switching variance), fitted by maximum likelihood through the filter from two starts (regimes split by the size
and by the sign of the residual), keeping the better.

Year-over-year growth moves each quarter by that quarter's growth less the growth of the quarter it drops, so its
new shock each quarter is the quarterly one: the regimes' sizes carry over in proportion. They are scaled so their
long-run average variance is the growth process's own (`volatility`, the year-apart fit's), and the switching
chances are converted to any scenario step by `rescale_transition_matrix`. The regimes move the size of the shocks,
not their average: drifts are zero.

The formula is as follows:

$$
x_{t} = \ln(1 + q_{t}) = c + \phi \cdot x_{t-1} + s_{k} \cdot e_{t},\;\; e_{t} \sim \operatorname{Normal}(0,\; 1),\;\; P(k_{t+1} = j | k_{t} = i) = p_{ij}
$$

$$
\sigma_{k} = \sigma \cdot s_{k} / \sqrt{\sum_{j} \pi_{j} \cdot s_{j} ^{2}},\;\; d_{k} = 0
$$

Where q_t is quarter-on-quarter growth, pi the regimes' long-run shares and sigma the growth process's volatility.

**References:**

- Crawford, G.W., Fratantoni, M.C. (2003). "Assessing the Forecasting Performance of Regime-Switching, ARIMA and GARCH Models of House Prices." Real Estate Economics, 31(2), 223-243. <https://doi.org/10.1111/1540-6229.00064>
- Hamilton, J.D. (1989). "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle." Econometrica, 57(2), 357-384. <https://doi.org/10.2307/1912559>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_volatility_regimes(
    quarterly_growth: np.ndarray,
    time_step: float,
    volatility: float,
) -> VolatilityRegimeFit
```

**Args:**

- <u>quarterly_growth (np.ndarray):</u> quarter-on-quarter growth of the house-price index, in date order, as decimals.
- <u>time_step (float):</u> the years between them (0.25 for quarterly data).
- <u>volatility (float):</u> sigma, the growth process's volatility to split between the regimes.

**Returns:**

<u>VolatilityRegimeFit:</u> the regimes and the likelihoods against one constant shock size.

**Raises:**

- <u>ValueError:</u> if there are too few quarters or a regime collapses.

</details>
{% endraw %}

#### step_regime_ou

Move house-price growth one step forward in each scenario's own regime: the exact mean-reverting step with that
regime's volatility and drift, plus the long rate's push a year earlier when the rate link is on.

The formula is as follows:

- g(t + dt) = theta + (g(t) - theta) * exp(-a * dt) + w * (d_k * dt + beta * dL)
  + sigma_k * sqrt((1 - exp(-2a * dt)) / (2a)) * z

Where k is the scenario's regime over the step, w = `yearly_sensitivity_weight(a, dt)` and dL the long rate's
change over one step `lag` years earlier.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_regime_ou(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: RegimeOUParams,
    regime: np.ndarray,
    rate_change: np.ndarray | float | None = None,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's growth rate.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw.
- <u>time_step (float):</u> the step length, in years.
- <u>params (RegimeOUParams):</u> the fitted process.
- <u>regime (np.ndarray):</u> each scenario's regime over the step.
- <u>rate_change (np.ndarray &#124; float &#124; None):</u> dL; required when the rate link is on.

**Returns:**

<u>np.ndarray:</u> the growth rate one step later.

**Raises:**

- <u>ValueError:</u> if the rate link is on but no rate change is given.

</details>

#### fit_dividend_yield_process

Fit the mean-reverting log-dividend-yield process of Ahlgrim, D'Arcy and Gorvett (2005, eq. 3.17) to a historical
trailing-yield series: the discretized-OU OLS regression of `calibration_model.fit_ou_process`, run on the *log*
yield, as `fit_commodity_process` does for a spot price. Passing `inflation` adds Wilkie's (1986) inflation term
as an extra regression column. The slope maps to the exact OU transition, so a simulation at a coarser step than
the data stays stable.

The formula is as follows:

$$
\text{ln}\; y (t) - \text{ln}\; y (t-1) = c + b \cdot \text{ln}\; y (t-1) + w \cdot (\pi(t) - \pi(t-1)) + e(t)
$$

$$
\kappa = - \ln(1 + b) / \text{dt}
$$

$$
\mu = - c / b
$$

$$
\sigma = \operatorname{std}(e) / \sqrt{(1 - \exp(- 2 \cdot \kappa \cdot \text{dt})) / (2 \cdot \kappa)}
$$

Where pi is the inflation rate (the w term only when `inflation` is given) and std(e) the residual standard
deviation, with one degree of freedom per fitted coefficient.

With `inflation_level`, Wilkie's (1986, section 3.5) form lnY(t) = YW.I(t) + YN(t), w is first read from a
regression of ln y(t) on [1, pi(t), ln y(t-1), pi(t-1)] (its pi(t) coefficient), and the OU fit above then runs
on YN(t) = ln y(t) - w * pi(t) without the w term; a judgement, as Wilkie fits the two together.

**References:**

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92, eq. 3.17. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. Share dividend yield equation. <https://doi.org/10.1017/S0071368600009009>
- Schwartz, E.S. (1997). "The Stochastic Behavior of Commodity Prices: Implications for Valuation and Hedging." Journal of Finance, 52(3), 923-973. The same log-space OLS fit. <https://doi.org/10.1111/j.1540-6261.1997.tb02721.x>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_dividend_yield_process(
    yields: pl.Series,
    time_step: float,
    inflation: pl.Series | None = None,
    inflation_level: bool = False,
) -> DividendYieldParams
```

**Args:**

- <u>yields (pl.Series):</u> historical trailing dividend-yield observations, evenly spaced in time, all > 0.
- <u>time_step (float):</u> time increment between observations, in years.
- <u>inflation (pl.Series &#124; None):</u> historical inflation-rate observations, the same length and time index as `yields`. When supplied, adds Wilkie's inflation-sensitivity term to the fit.
- <u>inflation_level (bool):</u> fit Wilkie's level form, the pull on ln y - w * inflation; needs `inflation`. Defaults to False, the pull on ln y.

**Returns:**

<u>DividendYieldParams:</u> the calibrated mean-reversion speed, long-run log-yield level, log-yield volatility, and the series' last (actual, not log) value as the simulation starting point. `inflation_sensitivity` is set only when `inflation` was supplied.

**Raises:**

- <u>ValueError:</u> if fewer than `MINIMUM_OBSERVATIONS_OU` observations are supplied, any observation is not strictly positive, `inflation` is supplied with a different length than `yields`, or the fitted mean-reversion speed is non-positive (the series shows no mean reversion at this time step; Ahlgrim/D'Arcy/Gorvett's own finding that dividend yield sits close to a random walk means this is a real possibility, not just an edge case).

</details>

#### reconstruct_dividend_yield_residuals

Recover this process's own realised shock at every historical step: the actual log-yield change minus the
drift `step_dividend_yield_process` applies. Runs store levels, not shocks, so a consumer that needs the
dividend yield's own shock (Wilkie's (1986) YE(t-1) in the dividend index model) rebuilds it this way.

The formula is as follows:

$$
\operatorname{YE}(t) = \text{ln}\; y (t) - \text{ln}\; y (t-1) - (\mu - \text{ln}\; y (t-1)) \cdot (1 - \exp(- \kappa \cdot \text{dt})) - w \cdot (\pi(t) - \pi(t-1))
$$

Where the w term applies only when `params` were conditioned on inflation.

**References:**

- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. The YE(t) yield residual in the dividend equation. <https://doi.org/10.1017/S0071368600009009>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
reconstruct_dividend_yield_residuals(
    yields: pl.Series,
    params: DividendYieldParams,
    time_step: float,
    inflation: pl.Series | None = None,
) -> np.ndarray
```

**Args:**

- <u>yields (pl.Series):</u> the same historical trailing-yield series `params` was fit from (or a like-for-like series at the same period/dt).
- <u>params (DividendYieldParams):</u> this process's calibrated parameters.
- <u>time_step (float):</u> the time increment between observations, in years; must match what `params` was fit with.
- <u>inflation (pl.Series &#124; None):</u> the same inflation series `params` was conditioned on, if `params.inflation_sensitivity is not None`. Must be the same length as `yields`.

**Returns:**

<u>np.ndarray:</u> one residual per step-to-step transition, length `yields.len() - 1`; index i is the shock realised moving from observation i to observation i+1.

**Raises:**

- <u>ValueError:</u> if `inflation` is required (params.inflation_sensitivity is not None) but not supplied, or supplied with a different length than `yields`.

</details>

#### step_dividend_yield_process

Move a dividend yield one step forward: its logarithm is pulled toward the normal level and shocked, as in
Ahlgrim, D'Arcy and Gorvett (2005).

Modeling the log keeps the yield positive and makes its swings proportional to its level, so the simulated
yield is lognormal around its normal value: it can spike after a market fall but never turns negative. The
pull is slow, so a low starting yield stays low for years in most scenarios. The step is exact, so the
result does not depend on the step size. With the Wilkie inflation term, a rise in inflation over the step
lifts the yield by `w` times that rise, the channel through which inflation lowers equity prices in the
Wilkie model.

The formula is as follows:

$$
\text{ln}\; y (t + \text{dt}) = \text{ln}\; y (t) + (\mu - \text{ln}\; y (t)) \cdot (1 - \exp(- \kappa \cdot \text{dt})) + w \cdot d(\text{inflation}) + s \cdot z
$$

$$
s = \sigma \cdot \sqrt{(1 - \exp(- 2 \cdot \kappa \cdot \text{dt})) / (2 \cdot \kappa)}
$$

Where kappa is `mean_reversion_speed`, mu `long_run_mean` (a log yield), sigma `volatility`, w
`inflation_sensitivity` and z the yield's correlated standard normal shock. With `inflation_level` (Wilkie's own
form) the pull acts on ln y(t) - w * inflation(t) instead of ln y(t). A `volatility` per scenario replaces sigma,
as when the yield's volatility follows the equity regime (Hibbert, Mowbray and Turnbull (2001, section 5.2.2)).

**References:**

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92, eq. 3.17. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_dividend_yield_process(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: DividendYieldParams,
    inflation_change: np.ndarray | float = 0.0,
    inflation_now: np.ndarray | float = 0.0,
    volatility: np.ndarray | float | None = None,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's dividend yield in each scenario, as a decimal.
- <u>shock (np.ndarray &#124; float):</u> the yield's correlated standard normal shock for this step.
- <u>time_step (float):</u> the step length, in years.
- <u>params (DividendYieldParams):</u> the calibrated reversion speed, normal log yield, volatility and, with the Wilkie term, the inflation sensitivity.
- <u>inflation_change (np.ndarray &#124; float):</u> the change in simulated inflation over the step; only used with the Wilkie term.
- <u>inflation_now (np.ndarray &#124; float):</u> simulated inflation at the start of the step; only used with `inflation_level`.
- <u>volatility (np.ndarray &#124; float &#124; None):</u> sigma for this step in each scenario; None (default) uses the parameters' own.

**Returns:**

<u>np.ndarray:</u> the dividend yield at the end of the step, always positive.

</details>

{% raw %}
#### fit_dividend_growth_process

Fit Wilkie's (1986) share dividend index to a dividend history, a paired inflation history and the paired
dividend yield's past shocks.

Wilkie ties dividends to inflation with unit gain. A given percentage rise in the Retail Prices Index ends up as
the same percentage rise in the dividend index (section 3.7). Part of the effect is immediate (DX) and part
arrives through a slowly
updating average of past inflation (DW); his bases use DW = 0.8 and DX = 0.2 (section 3.9). The fit imposes
DW + DX = 1, so equities hold their real value against inflation in the long run, and estimates DX, DMU and DY
by one ordinary least squares regression. DD is fixed, not fitted: Wilkie's DD is a yearly weight, the share of
the current inflation rate that enters the dividend model each year (section 3.8), so it is
converted to the data's step, as is the inflation rate, which is quoted per year.

The formula is as follows:

$$
d = 1 - (1 - \text{DD}) ^{\text{dt}}
$$

$$
\operatorname{DM}(t) = d \cdot I(t) + (1 - d) \cdot \operatorname{DM}(t-1),\;\; \operatorname{DM}(0) = I(0)
$$

$$
\text{ln}\; D (t) - \text{ln}\; D (t-1) - \operatorname{DM}(t) \cdot \text{dt} = \text{DMU} + \text{DX} \cdot (I(t) - \operatorname{DM}(t)) \cdot \text{dt} + \text{DY} \cdot \operatorname{YE}(t-1) + e(t)
$$

$$
\text{DW} = 1 - \text{DX}
$$

$$
\text{DSD} = \sqrt{\text{sum}\; e (t) ^{2} / (n - 3)}
$$

Where I(t) is the annual inflation rate, dt the step in years, n the number of regression rows and YE(t-1) zero
on the first row. With `unit_gain=False` the earlier free fit is used instead: DW and DX unrestricted, inflation
and DD taken per step as given.

**References:**

- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. Sections 3.7-3.9 and Table 1. <https://doi.org/10.1017/S0071368600009009>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_dividend_growth_process(
    dividend_index: pl.Series,
    inflation: pl.Series,
    yield_residual: np.ndarray,
    carried_forward_weight: float = 0.2,
    time_step: float = 1.0,
    unit_gain: bool = True,
    residual_lag: int = 1,
) -> DividendGrowthParams
```

**Args:**

- <u>dividend_index (pl.Series):</u> the dividend index history, evenly spaced, all above 0.
- <u>inflation (pl.Series):</u> the paired annual inflation rate, same length and dates as `dividend_index`.
- <u>yield_residual (np.ndarray):</u> the paired dividend yield's past shocks (see `reconstruct_dividend_yield_residuals`), one shorter than `dividend_index`.
- <u>carried_forward_weight (float):</u> DD, Wilkie's yearly weight of current inflation in DM(t); default 0.2, his value in both bases (Table 1).
- <u>time_step (float):</u> the time between observations, in years; default 1.0, Wilkie's yearly step.
- <u>unit_gain (bool):</u> impose Wilkie's DW + DX = 1 (default); False gives the free fit.
- <u>residual_lag (int):</u> how many observations back YE is read; 1 (default) is the previous one, the number of observations in a year is Wilkie's YE(t-1) of a year earlier on monthly or quarterly data.

**Returns:**

<u>DividendGrowthParams:</u> the fitted parameters, with DW and DX in Wilkie's own terms.

**Raises:**

- <u>ValueError:</u> if the inputs differ in length, there are too few rows, a dividend index value is not above 0, or `carried_forward_weight` is not strictly between 0 and 1.

</details>
{% endraw %}

#### conditional_default_rate

The default rate of a rating in a year with credit-cycle value Z, from Vasicek's one-factor model: a high Z is a
good year with fewer defaults, a low Z a recession with many.

Every borrower's credit quality is a standard normal variable, part shared cycle and part its own luck, and it
defaults when that quality falls below the threshold set by its long-run default rate PD. The asset correlation rho is
the shared part: the higher it is, the more a bad year lifts every default rate at once, and the fatter the tail of
portfolio losses. The long-run PD is still the average across years, so the model redistributes defaults over good and
bad years rather than adding to them. This is the structure behind the Basel internal-ratings formula, where Vasicek's
extension of Merton's model to an asymptotic single risk factor portfolio model is the basis in BCBS (2005, section
4.2), "An Explanatory Note on the Basel II IRB Risk Weight Functions", https://www.bis.org/bcbs/irbriskweight.pdf.
Basel's supervisory corporate rho moves between limit correlations of 12% and 24% (BCBS (2005, section 5.2)), a
deliberately
prudent value; rho here is fitted to default history.

The formula is as follows:

$$
\operatorname{PD}(Z) = \Phi((\Phi ^{-1} (\text{PD}) - \sqrt{\rho} \cdot Z) / \sqrt{1 - \rho})
$$

Where Phi is the standard normal CDF and rho the asset correlation, as in
[Vasicek (2002)](https://www.risk.net/risk-management/credit-risk/1500333/loan-portfolio-value).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
conditional_default_rate(
    probability: np.ndarray,
    asset_correlation: float,
    cycle: np.ndarray,
) -> np.ndarray
```

</details>

#### fit_credit_cycle

Read the credit cycle off history: the asset correlation and one cycle value per year, from the default rates per
rating. This is the one-parameter representation of transition matrices of Belkin, Suchower and Forest (1998), as
presented in [Kim (1999)](https://www.msci.com/www/research-report/a-way-to-condition-transition/018440984), built
on a credit cycle index for the credit state of the market as a whole.

Each year's cycle value is the one that best explains that year's default rates across all ratings at once, so
years such as 2009 and 2001 come out strongly negative and quiet years positive. The asset correlation is the one at
which those yearly values have unit variance, as the model assumes: if defaults swing a lot from year to year, a
higher correlation is needed to explain it. Rare defaults in the top ratings carry little information, so each
rating is weighted by the binomial variance of its long-run rate.

The formula is as follows:

$$
Z_{t} = \operatorname{argmin}(\operatorname{sum}(w_{k} \cdot (\text{DR}_{k} - \text{PD}_{k}(Z)) ^{2})),\;\; \text{over ratings k in year t}
$$

$$
w_{k} = 1 / (\text{PD}_{k} \cdot (1 - \text{PD}_{k}))
$$

$$
\operatorname{var}(Z_{t}) = 1,\;\; \text{solved for rho}
$$

Where DR_k is the observed default rate, PD_k the long-run rate, PD_k(Z) is `conditional_default_rate` and the
weights are the binomial variance of each rating's long-run rate.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_credit_cycle(
    default_rates: pl.DataFrame,
    default_probabilities: Mapping[str, float],
) -> tuple[float, pl.DataFrame]
```

**Args:**

- <u>default_rates (pl.DataFrame):</u> the observed default rate per rating and year, as decimals.
- <u>default_probabilities (Mapping[str, float]):</u> the long-run default rate per rating.

**Returns:**

<u>tuple[float, pl.DataFrame]:</u> the asset correlation, and the cycle value per year.

**Raises:**

- <u>ValueError:</u> if fewer than five years are given, or no correlation gives the index unit variance.

</details>

{% raw %}
#### conditional_transition_matrix

The one-year rating transition matrix in a year with credit-cycle value Z, after Belkin, Suchower and Forest
(1998), as presented in [Kim (1999)](https://www.msci.com/www/research-report/a-way-to-condition-transition/018440984).

The average through-the-cycle matrix is what an agency reports; this conditions it on the state of the economy.
Each row's cumulative probabilities, counted from default upward, become thresholds on a standard normal credit
quality, as in CreditMetrics, and the cycle shifts that quality by sqrt(rho) * Z. A bad year (Z below 0) moves
weight from upgrades toward downgrades and default for every rating at once; a good year does the reverse. Because
the same Z drives every row, downgrades and defaults bunch in the same years, which is what makes a credit
portfolio's loss distribution fat-tailed.

The formula is as follows:

$$
C_{j} = \operatorname{sum}(M_{k} \;\text{for}\; k \;\text{from}\; j \;\text{down to default})
$$

$$
C_{j}(Z) = \Phi((\Phi ^{-1} (C_{j}) - \sqrt{\rho} \cdot Z) / \sqrt{1 - \rho})
$$

$$
M_{j}(Z) = C_{j}(Z) - C_{\text{next}}(Z)
$$

Where M is one row of the matrix, j a rating and C_next the cumulative probability of the next-worse state.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
conditional_transition_matrix(
    matrix: np.ndarray,
    asset_correlation: float,
    cycle: np.ndarray,
) -> np.ndarray
```

**Args:**

- <u>matrix (np.ndarray):</u> the average through-the-cycle transition matrix, best rating first and default last.
- <u>asset_correlation (float):</u> rho, the share of credit quality that moves with the cycle.
- <u>cycle (np.ndarray):</u> the credit-cycle values Z to condition on.

**Returns:**

<u>np.ndarray:</u> one transition matrix per cycle value, every row summing to 1.

</details>
{% endraw %}

#### migrate_ratings

Roll a portfolio's rating mix forward one year at a time along simulated credit cycles: each scenario's cycle
value in a year picks that year's transition matrix, so downgrades and defaults bunch in the scenarios and years
where the cycle turns bad, as they do in recessions. A portfolio downgraded in a bad year starts the next year
from a weaker mix, so a run of bad years compounds. Losses apply a fixed recovery rate to the defaulted share.
Recovery in fact falls when defaults rise: Moody's (2005, Exhibit 10) fits a recovery rate of 0.52 minus 6.9
times the default rate, so a fixed rate understates the loss in the worst years.

The formula is as follows:

$$
d_{t} = d_{t-1} \cdot M(Z_{t})
$$

$$
\text{loss}_{t} = D_{t} \cdot \text{exposure} \cdot (1 - R)
$$

Where d_t is the row vector of rating shares, M(Z_t) is `conditional_transition_matrix`, D_t the share in default
and R the recovery rate.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
migrate_ratings(
    cycle_paths: np.ndarray,
    params: CreditCycleParams,
    holdings: Mapping[str, float],
    recovery_rate: float = 0.4,
) -> RatingMigrationResult
```

**Args:**

- <u>cycle_paths (np.ndarray):</u> the simulated `credit_cycle` per scenario at each whole year; the value at the end of a year drives that year's transitions.
- <u>params (CreditCycleParams):</u> the calibrated cycle, matrix and asset correlation.
- <u>holdings (Mapping[str, float]):</u> exposure per starting rating, e.g. {"A": 40, "BBB": 50, "BB": 10}.
- <u>recovery_rate (float):</u> the share of a defaulted exposure recovered, in [0, 1). Defaults to 0.4 (Moody's (2005, Exhibit 28): senior unsecured bonds recover "$39.0" per $100 par, all ratings held a year before default).

**Returns:**

<u>RatingMigrationResult:</u> the rating shares, cumulative default share and loss per scenario and year.

**Raises:**

- <u>ValueError:</u> if a holding names an unknown rating, is negative, or the recovery rate is outside [0, 1).

</details>
