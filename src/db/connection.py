import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine

from src.config.config import DB_CONFIG


def get_connection():
    """
    Low-level psycopg2 connection
    Used for executing raw SQL scripts
    """
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=str(DB_CONFIG["password"]),
        options="-c client_encoding=UTF8",
        cursor_factory=RealDictCursor
    )


def get_sqlalchemy_engine():
    """
    SQLAlchemy engine
    Used for pandas.to_sql and bulk loading
    """
    db_url = (
        f"postgresql+psycopg2://"
        f"{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}"
        f"/{DB_CONFIG['database']}"
    )

    return create_engine(db_url)
