"""Central settings for Project 1 (stock return prediction).

Change the universe or the dates here, not in the notebooks.
"""

# Start of the data history (one year of buffer before the first model year,
# because rolling features need a warm-up period).
START = "2009-01-01"
END = None  # None = until today

# ~60 large US stocks that were already listed in 2009 (long, complete history).
# Note: choosing today's large caps introduces survivorship bias
# (companies that failed or were removed are missing). Mention in the report.
TICKERS = [
    "AAPL", "MSFT", "AMZN", "GOOGL", "NVDA", "JPM", "JNJ", "XOM", "PG", "V",
    "UNH", "HD", "KO", "PEP", "WMT", "CVX", "MRK", "BAC", "PFE", "CSCO",
    "ORCL", "INTC", "ADBE", "CRM", "MCD", "NKE", "T", "VZ", "DIS", "ABT",
    "TMO", "COST", "AMGN", "HON", "IBM", "TXN", "QCOM", "CAT", "BA", "GS",
    "MMM", "LMT", "UPS", "MDT", "LOW", "SBUX", "AXP", "GE", "MO", "WFC",
    "C", "TGT", "DE", "BMY", "GILD", "CVS", "LLY", "NEE", "DUK", "SO",
]

# Market-wide series from Yahoo Finance
MARKET_TICKERS = ["^GSPC", "^VIX"]  # S&P 500, volatility index

# Macro series from FRED (no API key needed for the CSV download)
FRED_SERIES = {
    "DGS10": "10-year Treasury yield (daily)",
    "DGS3MO": "3-month Treasury yield (daily)",
    "FEDFUNDS": "Effective federal funds rate (monthly)",
    "CPIAUCSL": "Consumer price index (monthly, published with delay)",
    "UNRATE": "Unemployment rate (monthly, published with delay)",
}
