# etl/load.py
import sqlite3
import polars as pl
from config import DB_PATH


def load_to_sqlite(df: pl.DataFrame, table_name: str = "stock_data") -> None:
    """
    Loads a Polars DataFrame into a SQLite database.
    Replaces the table on each run (full refresh strategy).
    """
    print(f"  Loading {len(df)} rows into SQLite table '{table_name}'...")

    # Convert polars → pandas for sqlite compatibility
    pandas_df = df.to_pandas()

    conn = sqlite3.connect(DB_PATH)

    pandas_df.to_sql(
        name=table_name,
        con=conn,
        if_exists="replace",   # full refresh each run
        index=False
    )

    # Verify the write
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]

    conn.close()
    print(f"  ✅ Load complete. {count} rows in '{table_name}'.")


if __name__ == "__main__":
    from etl.extract import fetch_stock_data
    from etl.transform import transform_stock_data

    raw = fetch_stock_data()
    transformed = transform_stock_data(raw)
    load_to_sqlite(transformed)
