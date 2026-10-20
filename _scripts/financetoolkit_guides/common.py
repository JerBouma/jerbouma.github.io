"""Shared helpers for the Getting Started guide chart builders."""

import os
from datetime import date

import numpy as np
import pandas as pd

API_KEY = os.environ.get("FINANCIAL_MODELING_PREP_KEY", "")


def label(value) -> str:
    """Dates, periods and numbers as short axis labels."""
    if isinstance(value, pd.Period):
        if value.freqstr.startswith("W"):
            return value.end_time.strftime("%Y-%m-%d")
        return str(value)
    if isinstance(value, (pd.Timestamp, date)):
        return pd.Timestamp(value).strftime("%Y-%m-%d")
    return str(value)


def values(series, digits: int = 4) -> list:
    """A series as a JSON list, with gaps as null."""
    return [None if pd.isna(v) or np.isinf(v) else round(float(v), digits) for v in series]


def line(x, series: dict, fmt: str = "num", kind: str = "line", title: str = "", **extra) -> dict:
    """A line or bar chart; periods where every series is empty are left out."""
    x = [label(v) for v in x]
    data = {name: values(s) for name, s in series.items()}
    keep = [i for i in range(len(x)) if any(d[i] is not None for d in data.values())]
    return {
        "type": kind,
        "title": title,
        "x": [x[i] for i in keep],
        "series": [{"name": str(name), "data": [d[i] for i in keep]} for name, d in data.items()],
        "format": fmt,
        **extra,
    }


def frame_chart(df: pd.DataFrame, fmt: str = "num", kind: str = "line", title: str = "", **extra) -> dict:
    """A chart with one series per column of a DataFrame indexed by date or period."""
    return line(df.index, {col: df[col] for col in df.columns}, fmt=fmt, kind=kind, title=title, **extra)
