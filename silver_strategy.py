import numpy as np


def add_rolling_vol(df, window=30):
    df = df.copy()
    df["rolling_vol"] = df["returns"].rolling(window).std() * np.sqrt(252)
    df.dropna(inplace=True)
    return df


def assign_regimes(df):
    df = df.copy()
    low_thresh = df["rolling_vol"].quantile(0.33)
    high_thresh = df["rolling_vol"].quantile(0.67)

    def label(v):
        if v <= low_thresh:
            return "low"
        elif v <= high_thresh:
            return "medium"
        else:
            return "high"

    df["regime"] = df["rolling_vol"].apply(label)
    return df


def assign_exposure(df):
    df = df.copy()
    exposure_map = {"low": 1.0, "medium": 0.6, "high": 0.3}
    df["exposure"] = df["regime"].map(exposure_map)
    return df


def compute_returns(df):
    df = df.copy()
    df["strategy_returns"] = df["returns"] * df["exposure"].shift(1)
    df["benchmark_returns"] = df["returns"]
    df.dropna(inplace=True)
    return df