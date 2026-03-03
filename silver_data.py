import yfinance as yf
import pandas as pd


def fetch_silver_data(start="2015-01-01"):
    raw = yf.download("SI=F", start=start, auto_adjust=True)
    df = raw[["Close"]].copy()
    df.columns = ["close"]
    df.dropna(inplace=True)
    df["returns"] = df["close"].pct_change()
    df.dropna(inplace=True)
    return df