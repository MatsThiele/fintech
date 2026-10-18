# Project 1: Predicting Stock Returns Using Machine Learning

Course: Intro to Fintech. Goal: predict next-month returns of ~60 large US stocks.

## Setup (GitHub Codespaces)

```bash
pip install -r requirements.txt
```

Then open `notebooks/01_data.ipynb` and run all cells (select the Python 3 kernel).

## Structure

```
data/raw/         downloaded raw data (not in git, reproducible)
data/processed/   monthly data (not in git, reproducible)
notebooks/        01_data -> 02_features -> 03_models -> 04_evaluation
src/              config.py (universe, dates), data.py (download helpers)
tests/            synthetic data to test the logic offline
report/           final report
```

## Pipeline

1. `01_data`: download prices (Yahoo Finance) and macro data (FRED), quality checks, monthly aggregation
2. `02_features`: lagged returns, volatility, momentum, technical indicators, macro features, target = next-month return
3. `03_models`: Linear, Ridge, Lasso, Random Forest, XGBoost, (LSTM) with time-series cross-validation
4. `04_evaluation`: out-of-sample MSE / MAE / R2, long-short backtest, Sharpe ratio, feature importance
