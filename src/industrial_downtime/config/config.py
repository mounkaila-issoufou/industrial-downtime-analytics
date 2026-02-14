from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
CURATED_DATA_DIR = DATA_DIR / "curated"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
CURATED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Files
RAW_FILES = {
    "sales_performance": "sales_performance_raw.csv",
}


# PostgreSQL
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "industrial_db",
    "user": "postgres",
    "password": "0000"
}
