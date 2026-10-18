"""Download and basic preparation of price and macro data."""

import pandas as pd

FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"
PRICE_COLS = ["open", "high", "low", "close", "volume"]


def download_prices(tickers, start, end=None):
    """Download daily OHLCV data from Yahoo Finance.

    Returns a long data frame with columns
    date, open, high, low, close, volume, ticker.
    'close' is split- and dividend-adjusted (auto_adjust=True).
    """
    import yfinance as yf  # imported here so the module also works without it

    tickers = list(tickers)
    raw = yf.download(tickers, start=start, end=end, auto_adjust=True,
                      group_by="ticker", progress=False, threads=True)

    frames = []
    for t in tickers:
        try:
            sub = raw[t] if isinstance(raw.columns, pd.MultiIndex) else raw
        except KeyError:
            print(f"WARNING: no data returned for {t}")
            continue
        sub = sub.dropna(how="all")
        if sub.empty:
            print(f"WARNING: empty data for {t}")
            continue
        sub = sub.rename(columns=str.lower)[PRICE_COLS].copy()
        sub.index = pd.to_datetime(sub.index).tz_localize(None)
        sub.index.name = "date"
        sub["ticker"] = t
        frames.append(sub.reset_index())

    if not frames:
        raise RuntimeError("No price data downloaded. Check your internet connection.")
    return pd.concat(frames, ignore_index=True)


def download_fred(series_ids, start):
    """Download macro series from FRED (public CSV endpoint, no API key)."""
    series = []
    for sid in series_ids:
        df = pd.read_csv(FRED_URL.format(sid))
        df.columns = ["date", sid]  # first column is DATE or observation_date
        df["date"] = pd.to_datetime(df["date"])
        df[sid] = pd.to_numeric(df[sid], errors="coerce")  # '.' = missing
        series.append(df.set_index("date")[sid])
    macro = pd.concat(series, axis=1).sort_index()
    return macro.loc[start:]


def quality_report(prices):
    """Per-ticker overview to spot gaps, short histories and extreme returns."""
    df = prices.sort_values(["ticker", "date"]).copy()
    df["ret"] = df.groupby("ticker")["close"].pct_change()
    report = df.groupby("ticker").agg(
        first_date=("date", "min"),
        last_date=("date", "max"),
        n_days=("date", "count"),
        n_missing_close=("close", lambda s: int(s.isna().sum())),
        max_abs_daily_ret=("ret", lambda s: s.abs().max()),
    )
    return report.sort_values("n_days")


def to_monthly(prices, drop_current_month=True):
    """Aggregate daily prices to month-end values per ticker.

    Adds ret_1m = simple return of the month (close_t / close_{t-1} - 1).
    The running (incomplete) month is dropped because its return is not final.
    """
    df = prices.copy()
    df["date"] = pd.to_datetime(df["date"])
    out = []
    for ticker, g in df.groupby("ticker"):
        g = g.set_index("date").sort_index()
        m = g.resample("ME").agg({"open": "first", "high": "max", "low": "min",
                                  "close": "last", "volume": "sum"})
        m = m.dropna(subset=["close"])
        m["ticker"] = ticker
        m["ret_1m"] = m["close"].pct_change()
        out.append(m.reset_index())
    monthly = pd.concat(out, ignore_index=True)

    if drop_current_month:
        this_month_end = pd.Timestamp.today().normalize() + pd.offsets.MonthEnd(0)
        monthly = monthly[monthly["date"] < this_month_end]
    return monthly.reset_index(drop=True)


def macro_to_monthly(macro):
    """Month-end value of every macro series (forward-filled).

    Note: CPI and unemployment are published weeks after the month they describe.
    The publication lag is handled in the feature step (02_features).
    """
    return macro.resample("ME").last().ffill()
