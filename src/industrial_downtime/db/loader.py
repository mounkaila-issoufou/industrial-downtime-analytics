import pandas as pd
from sqlalchemy import create_engine

from industrial_downtime.db.connection import get_sqlalchemy_engine
from industrial_downtime.config import PROCESSED_DATA_DIR


def load_parquet_to_staging(table_name: str, parquet_file: str):
    engine = get_sqlalchemy_engine()

    file_path = PROCESSED_DATA_DIR / parquet_file

    df = pd.read_parquet(file_path)
    print(f"➡ Loading {parquet_file} into staging.{table_name} ({len(df)} rows)")
    print(df.head(2))
    print("...................................................")
    # Load into staging (replace = idempotent)
    df.to_sql(
        name=table_name,
        con=engine,
        schema="staging",
        if_exists="replace",
        index=False
    )

    print(f"✅ Loaded {parquet_file} into staging.{table_name}")
