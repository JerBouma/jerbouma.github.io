"""Charts for the Technicals guide: the same calls as the code on that page."""

import pandas as pd
from financetoolkit import Toolkit
from financetoolkit.technicals import momentum_model, volatility_model

from .common import API_KEY, line

TICKERS = ["MSFT", "ASML", "MU", "AMZN"]
NAMES = {"MSFT": "Microsoft", "ASML": "ASML", "MU": "Micron", "AMZN": "Amazon", "Benchmark": "S&P 500"}
# the colours of the renderer's palette, to keep a price and its levels apart
PRICE, BAND, MID, ACCENT, MUTED = "#38bdf8", "#818cf8", "#a78bfa", "#f97316", "#94a3b8"
# the last three months of 2023: short enough to see the daily levels
LAST_DAYS = 63


def with_reference(spec: dict, levels: dict) -> dict:
    """Add dashed reference lines (thresholds) to a line chart."""
    for name, level in levels.items():
        spec["series"].append({"name": name, "data": [level] * len(spec["x"]), "reference": True})
    return spec


def style(spec: dict, styles: dict) -> dict:
    """Set colour and dash per series name."""
    for s in spec["series"]:
        s.update(styles.get(s["name"], {}))
    return spec


def build() -> dict:
    companies = Toolkit(TICKERS, api_key=API_KEY, start_date="2023-01-01", end_date="2024-01-01")
    charts = {}

    indicators = companies.technicals.collect_all_indicators()
    print("Indicators:", list(dict.fromkeys(indicators.columns.get_level_values(0))))
    print(indicators.iloc[-1].unstack(0).T.round(2).to_string())

    close = companies.get_historical_data()["Close"]

    # Bollinger Bands, and their width as a share of the middle band
    bollinger_bands = companies.technicals.get_bollinger_bands()
    msft = bollinger_bands.xs("MSFT", level=1, axis=1)
    width = (msft["Upper Band"] - msft["Lower Band"]) / msft["Middle Band"]
    bands_chart = style(line(msft.index, {"Close": msft["Close"], "Upper band": msft["Upper Band"],
                                          "Middle band": msft["Middle Band"], "Lower band": msft["Lower Band"]}, fmt="price"),
                        {"Close": {"color": PRICE}, "Upper band": {"color": BAND, "dashed": True},
                         "Middle band": {"color": MUTED, "dashed": True}, "Lower band": {"color": BAND, "dashed": True}})
    width_chart = line(width.index, {"Band width": width}, fmt="percent")
    width_chart["series"][0].update({"area": True, "color": BAND})
    charts["technicals-bollinger"] = {
        "type": "tabs",
        "title": "Microsoft's Bollinger Bands squeezed to their narrowest of the year in December",
        "tabs": [{"label": "Bands", **bands_chart}, {"label": "Band width", **width_chart}],
    }
    above = int((msft["Close"] > msft["Upper Band"]).sum())
    below = int((msft["Close"] < msft["Lower Band"]).sum())
    print("Bollinger MSFT above upper", above, "below lower", below, "width min", width.idxmin(), round(width.min(), 4),
          "max", width.idxmax(), round(width.max(), 4))

    # ADX over 20 days: the level with the usual thresholds, and its growth
    adx_level = companies.technicals.get_average_directional_index(window=20)
    adx = companies.technicals.get_average_directional_index(window=20, growth=True, lag=[1, 3, 5, 10])
    level_chart = with_reference(line(adx_level.index, {"ADX (20 days)": adx_level["MSFT"]}, fmt="number"),
                                 {"Trending (25)": 25, "No trend (20)": 20})
    level_chart["series"][0].update({"area": True, "color": PRICE})
    growth_chart = line(adx.index, {"Over 1 day": adx["MSFT"]["Lag 1"], "Over 10 days": adx["MSFT"]["Lag 10"]}, fmt="percent")
    growth_chart["series"][1].update({"area": True, "color": ACCENT})
    growth_chart["series"][0]["color"] = PRICE
    charts["technicals-adx-growth"] = {
        "type": "tabs",
        "title": "Microsoft trended from April to July and again in December, and drifted in the autumn",
        "tabs": [{"label": "ADX", **level_chart}, {"label": "Growth over 1 and 10 days", **growth_chart}],
    }
    level = adx_level["MSFT"]
    print("ADX MSFT >25", int((level > 25).sum()), "<20", int((level < 20).sum()), "max", level.idxmax(), round(level.max(), 1),
          "min", level.idxmin(), round(level.min(), 1), "last", round(level.iloc[-1], 1))
    print("ADX growth MSFT last:", adx["MSFT"].iloc[-1].round(4).to_dict(), "lag10 max", adx["MSFT"]["Lag 10"].idxmax(),
          round(adx["MSFT"]["Lag 10"].max(), 3))

    # RSI: the days overbought and oversold, then the RSI itself per ticker
    rsi = companies.technicals.get_relative_strength_index()
    overbought, oversold = (rsi > 70).sum(), (rsi < 30).sum()
    order = TICKERS + ["Benchmark"]
    days_chart = line([NAMES[t] for t in order], {"Days above 70": overbought.reindex(order).reset_index(drop=True),
                                                 "Days below 30": oversold.reindex(order).reset_index(drop=True)},
                      kind="bar", fmt="number")
    days_chart["format"] = "amount"
    days_chart["series"][0]["color"] = ACCENT
    days_chart["series"][1]["color"] = PRICE
    rsi_tabs = [{"label": "Days overbought and oversold", **days_chart}]
    for t in order:
        spec = with_reference(line(rsi.index, {"RSI": rsi[t]}, fmt="number"), {"Overbought (70)": 70, "Oversold (30)": 30})
        spec["series"][0]["color"] = PRICE
        rsi_tabs.append({"label": NAMES[t], **spec})
    charts["technicals-rsi"] = {
        "type": "tabs",
        "title": "The S&P 500 was overbought on 41 days of 2023, more than any of the four stocks",
        "tabs": rsi_tabs,
    }
    print("RSI days above 70:", overbought.to_dict(), "below 30:", oversold.to_dict())

    # Donchian Channels and the Hull Moving Average
    donchian_channels = companies.technicals.get_donchian_channels()
    hull = companies.technicals.get_hull_moving_average()
    donchian = donchian_channels.xs("MSFT", level=1, axis=1)
    msft_close = close["MSFT"]
    donchian_chart = style(line(donchian.index, {"Close": msft_close.reindex(donchian.index),
                                                 "Upper channel": donchian["Upper Channel"],
                                                 "Middle channel": donchian["Middle Channel"],
                                                 "Lower channel": donchian["Lower Channel"]}, fmt="price"),
                           {"Close": {"color": PRICE}, "Upper channel": {"color": "#34d399"},
                            "Middle channel": {"color": MUTED, "dashed": True}, "Lower channel": {"color": "#f472b6"}})
    hull_chart = style(line(hull.index, {"Close": msft_close.reindex(hull.index), "Hull Moving Average": hull["MSFT"]},
                            fmt="price"), {"Close": {"color": PRICE}, "Hull Moving Average": {"color": ACCENT}})
    breakouts = int((msft_close >= donchian["Upper Channel"]).sum())
    breakdowns = int((msft_close <= donchian["Lower Channel"]).sum())
    charts["technicals-donchian-hull"] = {
        "type": "tabs",
        "title": f"Microsoft closed at a new 20-day high on {breakouts} days of 2023, at a new low on {breakdowns}",
        "tabs": [{"label": "Donchian Channels", **donchian_chart}, {"label": "Hull Moving Average", **hull_chart}],
    }
    print("Donchian MSFT breakouts", breakouts, "breakdowns", breakdowns)

    # VWAP over the year, the Parabolic SAR and the Pivot Points over the last three months
    vwap = companies.technicals.get_volume_weighted_average_price()
    sar = companies.technicals.get_parabolic_sar()
    pivots = companies.technicals.get_pivot_points()
    print("Pivot columns:", list(dict.fromkeys(pivots.columns.get_level_values(0))))
    pivot = pivots.xs("MSFT", level=1, axis=1).iloc[-LAST_DAYS:]
    recent_sar = sar["MSFT"].iloc[-LAST_DAYS:]
    side = msft_close > sar["MSFT"]
    flips = int((side != side.shift()).iloc[1:].sum())
    recent_flips = int((side != side.shift()).iloc[-LAST_DAYS:].sum())
    vwap_chart = style(line(vwap.index, {"Close": msft_close.reindex(vwap.index), "VWAP": vwap["MSFT"]}, fmt="price"),
                       {"Close": {"color": PRICE}, "VWAP": {"color": ACCENT}})
    sar_chart = style(line(recent_sar.index, {"Close": msft_close.reindex(recent_sar.index), "Parabolic SAR": recent_sar},
                           fmt="price"), {"Close": {"color": PRICE}, "Parabolic SAR": {"color": ACCENT, "dashed": True}})
    pivot_chart = style(line(pivot.index, {"Close": msft_close.reindex(pivot.index), "Resistance 1": pivot["Resistance 1"],
                                           "Pivot Point": pivot["Pivot Point"], "Support 1": pivot["Support 1"]}, fmt="price"),
                        {"Close": {"color": PRICE}, "Resistance 1": {"color": "#34d399", "dashed": True},
                         "Pivot Point": {"color": MUTED, "dashed": True}, "Support 1": {"color": "#f472b6", "dashed": True}})
    charts["technicals-overlap"] = {
        "type": "tabs",
        "title": f"Microsoft held above its VWAP for most of 2023; the Parabolic SAR flipped {recent_flips} times in the fourth quarter",
        "tabs": [
            {"label": "VWAP", **vwap_chart},
            {"label": "Parabolic SAR, Q4", **sar_chart},
            {"label": "Pivot Points, Q4", **pivot_chart},
        ],
    }
    above_vwap = int((msft_close > vwap["MSFT"]).sum())
    print("VWAP MSFT last", round(vwap["MSFT"].iloc[-1], 2), "days above", above_vwap, "of", int(vwap["MSFT"].notna().sum()),
          "SAR flips", flips, "Q4 flips", recent_flips)

    # volatility cone: the range of realized volatility per window, and today's
    cone = companies.technicals.get_volatility_cone().xs("MSFT", level=1, axis=1)
    cone_styles = {
        "Max": {"color": MUTED, "dashed": True}, "Min": {"color": MUTED, "dashed": True},
        "75th Percentile": {"color": BAND, "dashed": True}, "25th Percentile": {"color": BAND, "dashed": True},
        "Median": {"color": BAND}, "Current": {"color": ACCENT},
    }
    order_cone = [c for c in ["Max", "75th Percentile", "Median", "25th Percentile", "Min", "Current"] if c in cone.columns]
    cone_chart = style(line([str(w) for w in cone.index], {c: cone[c] for c in order_cone}, fmt="percent",
                            xname="Window (trading days)"), cone_styles)
    cone_chart["series"][-1]["area"] = True
    cone_chart["title"] = "Microsoft ended 2023 at the bottom of its volatility cone for every window"
    charts["technicals-volatility-cone"] = cone_chart
    print(cone.round(4).to_string())

    # breadth: the TRIN (smoothed, since single days spike far above 1) and New Highs - New Lows
    breadth = companies.technicals.collect_breadth_indicators()
    print("Breadth:", list(dict.fromkeys(breadth.columns.get_level_values(0))))
    trin = companies.technicals.get_trin()
    highs_lows = companies.technicals.get_new_highs_new_lows(window=60)
    smooth_trin = trin["MSFT"].rolling(10, min_periods=5).median()
    trin_chart = with_reference(line(trin.index, {"TRIN, 10-day median": smooth_trin}, fmt="ratio"), {"Neutral (1.0)": 1.0})
    trin_chart["series"][0].update({"color": PRICE, "area": True})
    # summed per month: a bar per trading day is too dense to read
    monthly = highs_lows["MSFT"].groupby(highs_lows.index.month).sum()
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    nhnl_chart = line([months[m - 1] for m in monthly.index], {"New Highs - New Lows (60 days), monthly sum": monthly.reset_index(drop=True)},
                      fmt="number", kind="bar")
    nhnl_chart["format"] = "amount"
    nhnl_chart["series"][0]["color"] = "#34d399"
    below_one = float((smooth_trin < 1).sum() / smooth_trin.notna().sum())
    charts["technicals-breadth"] = {
        "type": "tabs",
        "title": "The TRIN of the five stayed mostly below 1, and new lows outnumbered new highs only from August to October",
        "tabs": [{"label": "TRIN", **trin_chart}, {"label": "New Highs - New Lows", **nhnl_chart}],
    }
    print("TRIN median", trin["MSFT"].median(), "max", trin["MSFT"].max(), trin["MSFT"].idxmax(), "days > 3", int((trin["MSFT"] > 3).sum()),
          "smoothed below 1 share", round(below_one, 3), "NHNL range", highs_lows["MSFT"].min(), highs_lows["MSFT"].max(),
          "NHNL monthly", monthly.to_dict())

    ichimoku = momentum_model.get_ichimoku_cloud(
        prices_low=pd.Series(range(70, 140, 1)),
        prices_high=pd.Series(range(90, 160, 1)),
        conversion_window=9,
        base_window=20,
        lead_span_b_window=40,
    )
    charts["technicals-ichimoku-direct"] = line([str(i) for i in ichimoku.index], {c: ichimoku[c] for c in ichimoku.columns},
                                                fmt="number", xname="Period", cloud=["Leading Span A", "Leading Span B"],
                                                title="In a steady uptrend every Ichimoku line points up and the cloud stays below")
    print(ichimoku.dropna().head(3).to_string())

    bands = volatility_model.get_bollinger_bands(prices=pd.Series([100, 105, 113, 126, 148]), window=2, num_std_dev=2)
    print(bands.round(2).to_string())
    return charts
