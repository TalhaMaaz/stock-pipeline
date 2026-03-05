# run_pipeline.py
from etl.extract import fetch_stock_data
from etl.transform import transform_stock_data
from etl.load import load_to_sqlite

def run():
    print("🚀 Starting ETL pipeline...\n")

    print("📥 [1/3] Extract")
    raw = fetch_stock_data()

    print("\n🔄 [2/3] Transform")
    transformed = transform_stock_data(raw)

    print("\n🗄️  [3/3] Load")
    load_to_sqlite(transformed)

    print("\n✅ Pipeline complete.")

if __name__ == "__main__":
    run()
