# config.py
import os

# --- Tickers to track ---
TICKERS = ["AAPL", "MSFT", "GOOGL", "NVDA", "TSLA"]

# --- How much history to pull ---
PERIOD = "3mo"       # 3 months of daily data
INTERVAL = "1d"      # daily candles

# --- Database ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "stock_data.db")
