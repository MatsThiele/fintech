"""Synthetic data to test the pipeline logic without internet access."""

import numpy as np
import pandas as pd


def synthetic_prices(tickers, start, end="2025-09-30", seed=0):
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range(start, end)
    frames = []
    for i, t in enumerate(tickers):
        first = dates[0] if i % 7 else dates[500]  # some tickers start later
        d = dates[dates >= first]
        r = rng.normal(0.0004, 0.015, len(d))
        close = 50 * np.exp(np.cumsum(r))
        df = pd.DataFrame({
            "date": d,
            "open": close * (1 + rng.normal(0, 0.003, len(d))),
            "high": close * 1.01,
            "low": close * 0.99,
            "close": close,
            "volume": rng.integers(1_000_000, 5_000_000, len(d)),
            "ticker": t,
        })
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def synthetic_fred(series_ids, start, end="2025-09-30", seed=1):
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range(start, end)
    return pd.DataFrame({s: 2 + np.cumsum(rng.normal(0, 0.02, len(idx)))
                         for s in series_ids}, index=idx)
