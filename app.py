# app.py
import sqlite3
import json
from flask import Flask, jsonify, render_template
from config import DB_PATH

app = Flask(__name__)


def query_db(sql: str, params: tuple = ()) -> list[dict]:
    """Helper — runs a query and returns rows as a list of dicts."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


# --- Routes ---

@app.route("/")
def index():
    """Serve the dashboard."""
    return render_template("index.html")


@app.route("/api/tickers")
def get_tickers():
    """Return list of all available tickers."""
    rows = query_db("SELECT DISTINCT ticker FROM stock_data ORDER BY ticker")
    tickers = [r["ticker"] for r in rows]
    return jsonify(tickers)


@app.route("/api/stock/<ticker>")
def get_stock(ticker: str):
    """Return all data for a single ticker."""
    rows = query_db(
        """
        SELECT date, close, sma_20, sma_50, pct_change, volatility_20, volume
        FROM stock_data
        WHERE ticker = ?
        ORDER BY date ASC
        """,
        (ticker.upper(),)
    )
    return jsonify(rows)


@app.route("/api/latest")
def get_latest():
    """Return the latest close price for all tickers."""
    rows = query_db(
        """
        SELECT ticker, date, close, pct_change
        FROM stock_data
        WHERE date = (
            SELECT MAX(date) FROM stock_data s2
            WHERE s2.ticker = stock_data.ticker
        )
        ORDER BY ticker
        """
    )
    return jsonify(rows)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port = 5000, debug=True)
