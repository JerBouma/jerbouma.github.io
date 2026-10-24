"""Charts and outputs of the Equities, Currencies, Commodities and Real Estate pages (markets/) and the
Dependence page (under-the-hood/dependence.md)."""

import numpy as np

from common import NUMBERS, bar, default_run, fan, labels, tabs, values, write
from financescenarios import load_profiles

TITLES = {
    "markets-equity-returns": "Five-Year Annualized Return per Stock Market",
    "markets-equity-index": "Value of 100 Invested in US, European and Emerging-Market Stocks",
    "markets-drawdown": "Deepest Fall from a Peak within Five Years per Stock Market",
    "markets-fx": "Euros, Pounds and Yen per US Dollar",
    "markets-commodities": "Gold and Crude Oil",
    "markets-real-estate": "US House-Price Growth",
    "markets-correlation": "Correlations of the Fitted Shocks",
}
EQUITIES = {"US": "us_broad", "US small caps": "small_cap", "Europe": "europe", "Japan": "japan",
            "Emerging markets": "emerging_markets"}
charts = {}

scenarios, calibration, result = default_run()
summary = result.describe()
print(summary.filter(summary["category"].is_in(["equities", "fx", "commodities", "real_estate"])))

# markets-equity-returns: the terminal_q05, median and terminal_q95 of result.describe() per stock market
terminal = {name: result.metric_paths(factor)[:, -1] for name, factor in EQUITIES.items()}
charts["markets-equity-returns"] = bar(
    list(EQUITIES), {
        "5th percentile": [np.quantile(t, 0.05) for t in terminal.values()],
        "Median": [np.median(t) for t in terminal.values()],
        "95th percentile": [np.quantile(t, 0.95) for t in terminal.values()],
    },
)
NUMBERS["equity medians"] = {k: float(np.median(t)) for k, t in terminal.items()}

p = calibration.calibrated_params["us_broad"]
print("us_broad", "means", np.round(p.regime_means, 4), "vols", np.round(p.regime_volatilities, 4), "stationary",
      np.round(p.stationary_distribution, 3), "matrix", np.round(np.asarray(p.transition_matrix), 4), "initial",
      p.initial_regime)

# markets-equity-index: the price paths, result.metric_paths(factor, levels=True), rescaled to start at 100
def growth_of_100(factor):
    prices = result.metric_paths(factor, levels=True)
    return 100 * prices / prices[:, :1]


index = {name: growth_of_100(f) for name, f in
         {"US": "us_broad", "Europe": "europe", "Emerging markets": "emerging_markets"}.items()}
charts["markets-equity-index"] = fan(result, index, fmt="number")

# markets-drawdown: the deepest fall from a running peak of each scenario's index, per market
drawdown = {}
for name, factor in EQUITIES.items():
    level = growth_of_100(factor)
    worst = (level / np.maximum.accumulate(level, axis=1) - 1).min(axis=1)
    drawdown[name] = [np.quantile(worst, 0.05), np.median(worst), np.quantile(worst, 0.95)]
charts["markets-drawdown"] = bar(
    list(EQUITIES), {"Worst 5%": [d[0] for d in drawdown.values()], "Median": [d[1] for d in drawdown.values()],
                     "Best 5%": [d[2] for d in drawdown.values()]},
)
NUMBERS["drawdown"] = drawdown

# markets-fx: the exchange rates as levels, result.metric_paths(factor, levels=True)
for f in ["eur", "gbp", "jpy"]:
    print(f, result.metric_description(f, levels=True), calibration.calibrated_params[f])
charts["markets-fx"] = tabs({
    "Euro": fan(result, {"Euros per dollar": "eur"}, fmt="ratio", levels=True, inner=True),
    "Pound": fan(result, {"Pounds per dollar": "gbp"}, fmt="ratio", levels=True, inner=True),
    "Yen": fan(result, {"Yen per dollar": "jpy"}, fmt="number", levels=True, inner=True),
})
for f in ["eur", "gbp", "jpy", "gold", "crude_oil"]:
    level = result.metric_paths(f, levels=True)
    NUMBERS[f"{f} level"] = {"start": float(level[0, 0]), "q05": float(np.quantile(level[:, -1], 0.05)),
                            "median": float(np.median(level[:, -1])), "q95": float(np.quantile(level[:, -1], 0.95))}

print("gold", calibration.calibrated_params["gold"], "oil", calibration.calibrated_params["crude_oil"])
print("oil long-run level", np.exp(calibration.calibrated_params["crude_oil"].long_run_mean))
charts["markets-commodities"] = tabs({
    "Gold": fan(result, {"Gold, dollars per ounce": "gold"}, fmt="price", levels=True, inner=True),
    "Crude oil": fan(result, {"Crude oil, dollars per barrel": "crude_oil"}, fmt="price", levels=True, inner=True),
})

print("real estate", calibration.calibrated_params["real_estate"])
print(result.horizon_summary([1, 3, 5], factors=["real_estate"]).select("factor", "horizon", "q0.05", "q0.5", "q0.95"))
charts["markets-real-estate"] = fan(result, {"US house-price growth": "real_estate"}, inner=True)

# markets-correlation: calibration.correlation_frame(), nine of the 27 factors
names = ["united_states_inflation", "united_states_short_rate", "united_states_long_rate",
         "united_states_unemployment", "us_broad", "europe", "eur", "gold", "crude_oil"]
short = ["US inflation", "US short rate", "US 10-year", "US unemployment", "US stocks", "European stocks", "Euro",
         "Gold", "Crude oil"]
frame = calibration.correlation_frame()
print(frame.columns[:3], frame.shape)
order = list(calibration.factor_names)
matrix = np.asarray(calibration.correlation_matrix)[np.ix_([order.index(n) for n in names],
                                                           [order.index(n) for n in names])]
charts["markets-correlation"] = {"type": "heatmap", "x": short, "y": short, "values": [values(r, 2) for r in matrix],
                                 "min": -1, "max": 1}
NUMBERS["correlations"] = {f"{a}/{b}": round(float(matrix[i, j]), 2) for i, a in enumerate(short)
                           for j, b in enumerate(short) if i < j}

broad = load_profiles(settings_id="default", factor_set_id="broad")
print(broad.describe())

write("markets", charts, TITLES)
