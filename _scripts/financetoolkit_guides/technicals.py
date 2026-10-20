"""Charts for the Technicals guide: the same calls as the code on that page."""

import pandas as pd
from financetoolkit import Toolkit
from financetoolkit.technicals import momentum_model, volatility_model

from .common import API_KEY, frame_chart, line

TICKERS = ["MSFT", "ASML", "MU", "AMZN"]
NAMES = {"MSFT": "Microsoft", "ASML": "ASML", "MU": "Micron", "AMZN": "Amazon", "Benchmark": "S&P 500"}


def with_reference(spec: dict, levels: dict) -> dict:
    """Add dashed reference lines (thresholds) to a line chart."""
    for name, level in levels.items():
        spec["series"].append({"name": name, "data": [level] * len(spec["x"]), "reference": True})
    return spec


def build() -> dict:
    companies = Toolkit(TICKERS, api_key=API_KEY, start_date="2023-01-01", end_date="2024-01-01")
    charts = {}

    indicators = companies.technicals.collect_all_indicators()
    print("Indicators:", list(dict.fromkeys(indicators.columns.get_level_values(0))))
    print(indicators.iloc[-1].unstack(0).T.round(2).to_string())

    close = companies.get_historical_data()["Close"]

    bollinger_bands = companies.technicals.get_bollinger_bands()
    msft = bollinger_bands.xs("MSFT", level=1, axis=1)
    charts["technicals-bollinger"] = frame_chart(msft[["Close", "Upper Band", "Middle Band", "Lower Band"]], fmt="price",
                                                 title="Bollinger Bands for Microsoft")

    adx = companies.technicals.get_average_directional_index(window=20, growth=True, lag=[1, 3, 5, 10])
    charts["technicals-adx-growth"] = frame_chart(adx["MSFT"], fmt="percent",
                                                  title="Growth of Microsoft's Average Directional Index (20 days)")
    print("ADX growth MSFT last:", adx["MSFT"].iloc[-1].round(4).to_dict())

    rsi = companies.technicals.get_relative_strength_index()
    charts["technicals-rsi"] = {
        "type": "tabs",
        "title": "Relative Strength Index (14 days)",
        "tabs": [
            {"label": NAMES[t], **with_reference(line(rsi.index, {"RSI": rsi[t]}, fmt="number"),
                                                 {"Overbought (70)": 70, "Oversold (30)": 30})}
            for t in TICKERS + ["Benchmark"]
        ],
    }
    print("RSI days above 70:", (rsi > 70).sum().to_dict(), "below 30:", (rsi < 30).sum().to_dict())

    donchian_channels = companies.technicals.get_donchian_channels()
    hull = companies.technicals.get_hull_moving_average()
    donchian = donchian_channels.xs("MSFT", level=1, axis=1)
    charts["technicals-donchian-hull"] = {
        "type": "tabs",
        "title": "Donchian Channels and Hull Moving Average for Microsoft",
        "tabs": [
            {"label": "Donchian Channels", **line(donchian.index, {"Close": close["MSFT"].reindex(donchian.index),
                                                                   **{c: donchian[c] for c in donchian.columns}}, fmt="price")},
            {"label": "Hull Moving Average", **line(hull.index, {"Close": close["MSFT"].reindex(hull.index),
                                                                 "Hull Moving Average": hull["MSFT"]}, fmt="price")},
        ],
    }

    vwap = companies.technicals.get_volume_weighted_average_price()
    sar = companies.technicals.get_parabolic_sar()
    pivots = companies.technicals.get_pivot_points()
    print("Pivot columns:", list(dict.fromkeys(pivots.columns.get_level_values(0))))
    pivot = pivots.xs("MSFT", level=1, axis=1)
    pivot_cols = [c for c in ["Resistance 1", "Pivot Point", "Support 1"] if c in pivot.columns]
    charts["technicals-overlap"] = {
        "type": "tabs",
        "title": "VWAP, Parabolic SAR and Pivot Points for Microsoft",
        "tabs": [
            {"label": "VWAP", **line(vwap.index, {"Close": close["MSFT"].reindex(vwap.index), "VWAP": vwap["MSFT"]}, fmt="price")},
            {"label": "Parabolic SAR", **line(sar.index, {"Close": close["MSFT"].reindex(sar.index), "Parabolic SAR": sar["MSFT"]}, fmt="price")},
            {"label": "Pivot Points", **line(pivot.index, {"Close": close["MSFT"].reindex(pivot.index),
                                                           **{c: pivot[c] for c in pivot_cols}}, fmt="price")},
        ],
    }

    cone = companies.technicals.get_volatility_cone().xs("MSFT", level=1, axis=1)
    order = [c for c in ["Max", "90th Percentile", "75th Percentile", "Median", "25th Percentile", "10th Percentile", "Min", "Current"]
             if c in cone.columns]
    charts["technicals-volatility-cone"] = line([str(w) for w in cone.index], {c: cone[c] for c in order}, fmt="percent",
                                                xname="Window (trading days)", title="Volatility cone for Microsoft")
    print(cone.round(4).to_string())

    breadth = companies.technicals.collect_breadth_indicators()
    print("Breadth:", list(dict.fromkeys(breadth.columns.get_level_values(0))))
    trin = companies.technicals.get_trin()
    highs_lows = companies.technicals.get_new_highs_new_lows(window=60)
    charts["technicals-breadth"] = {
        "type": "tabs",
        "title": "Breadth of Microsoft, ASML, Micron, Amazon and the S&P 500",
        "tabs": [
            {"label": "TRIN", **with_reference(line(trin.index, {"TRIN": trin["MSFT"]}, fmt="ratio"), {"Neutral (1.0)": 1.0})},
            {"label": "New Highs - New Lows", **line(highs_lows.index, {"New Highs - New Lows (60 days)": highs_lows["MSFT"]},
                                                     fmt="number", kind="bar")},
        ],
    }
    print("TRIN median", trin["MSFT"].median(), "max", trin["MSFT"].max(), "NHNL range", highs_lows["MSFT"].min(), highs_lows["MSFT"].max())

    ichimoku = momentum_model.get_ichimoku_cloud(
        prices_low=pd.Series(range(70, 140, 1)),
        prices_high=pd.Series(range(90, 160, 1)),
        conversion_window=9,
        base_window=20,
        lead_span_b_window=40,
    )
    charts["technicals-ichimoku-direct"] = line([str(i) for i in ichimoku.index], {c: ichimoku[c] for c in ichimoku.columns},
                                                fmt="number", xname="Period", cloud=["Leading Span A", "Leading Span B"],
                                                title="Ichimoku Cloud on a steadily rising price series")
    print(ichimoku.dropna().head(3).to_string())

    bands = volatility_model.get_bollinger_bands(prices=pd.Series([100, 105, 113, 126, 148]), window=2, num_std_dev=2)
    print(bands.round(2).to_string())
    return charts
