# etl/transform.py
import polars as pl


def transform_stock_data(df: pl.DataFrame) -> pl.DataFrame:
    """
    Takes raw OHLCV data and adds:
    - 20-day & 50-day moving averages
    - Daily % change
    - Rolling 20-day volatility
    - Cleans nulls and normalizes column names
    """
    print("  Transforming data...")

    # Normalize column names to lowercase
    df = df.rename({col: col.lower() for col in df.columns})

    # Ensure date column is proper date type and sort
    df = df.with_columns(
        pl.col("date").cast(pl.Date)
    ).sort(["ticker", "date"])

    # Calculate indicators per ticker
    df = df.with_columns([

        # 20-day simple moving average
        pl.col("close")
          .rolling_mean(window_size=20)
          .over("ticker")
          .alias("sma_20"),

        # 50-day simple moving average
        pl.col("close")
          .rolling_mean(window_size=50)
          .over("ticker")
          .alias("sma_50"),

        # Daily % change
        (
            (pl.col("close") - pl.col("close").shift(1).over("ticker"))
            / pl.col("close").shift(1).over("ticker")
            * 100
        ).alias("pct_change"),

        # 20-day rolling volatility (std dev of % change)
        pl.col("close")
          .pct_change()
          .rolling_std(window_size=20)
          .over("ticker")
          .alias("volatility_20"),

    ])

    # Drop rows where close is null
    df = df.filter(pl.col("close").is_not_null())

    print(f"  ✅ Transform complete. Shape: {df.shape}")
    print(f"  Columns: {df.columns}")
    return df


if __name__ == "__main__":
    from etl.extract import fetch_stock_data
    raw = fetch_stock_data()
    transformed = transform_stock_data(raw)
    print(transformed.head(10))
