from src.db.connection import get_connection
from src.utils.logger import logger

def run_sql_file(path):
    logger.info(f"Executing SQL file: {path.name}")

    conn = get_connection()
    cur = conn.cursor()

    try:
        with open(path, "r", encoding="utf-8") as f:
            cur.execute(f.read())
        conn.commit()
        logger.info(f"SUCCESS: {path.name}")
    except Exception as e:
        conn.rollback()
        logger.error(f"FAILED: {path.name}")
        logger.error(str(e))
        raise
    finally:
        cur.close()
        conn.close()
    logger.info(f"Finished executing SQL file: {path.name}")