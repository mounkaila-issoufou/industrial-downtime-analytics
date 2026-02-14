from src.db.loader import load_parquet_to_staging

def load_all_staging():
    mapping = {
        "sales_orders_clean": "sales_orders_clean.parquet",

    }

    for table, file in mapping.items():
        load_parquet_to_staging(table, file)
