# etl/extract.py
import yfinance as yf
import polars as pl
from config import TICKERS, PERIOD, INTERVAL


def fetch_stock_data(tickers: list[str] = TICKERS) -> pl.DataFrame:
    """
    Pull OHLCV data for a list of tickers from yfinance.
    Returns a single polars DataFrame with all tickers combined.
    """
    all_frames = []

    for ticker in tickers:
        print(f"  Fetching {ticker}...")
        raw = yf.download(
            ticker,
            period=PERIOD,
            interval=INTERVAL,
            auto_adjust=True,
            progress=False
        )

        if raw.empty:
            print(f"  ⚠️  No data for {ticker}, skipping.")
            continue

        # Flatten MultiIndex columns if present
        if isinstance(raw.columns, __import__("pandas").MultiIndex):
            raw.columns = [col[0] for col in raw.columns]

        # Reset index so Date becomes a column
        raw = raw.reset_index()

        # Convert to polars
        df = pl.from_pandas(raw)

        # Add ticker column
        df = df.with_columns(pl.lit(ticker).alias("ticker"))

        all_frames.append(df)

    if not all_frames:
        raise ValueError("No data was fetched. Check your tickers or connection.")

    combined = pl.concat(all_frames, how="diagonal")
    print(f"\n✅ Extracted {len(combined)} rows across {len(tickers)} tickers.")
    return combined


if __name__ == "__main__":
    df = fetch_stock_data()
    print(df.head(10))
