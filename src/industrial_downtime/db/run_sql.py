from pathlib import Path
from industrial_downtime.db.connection import get_connection
from industrial_downtime.utils.logger import logger


def run_sql_file(sql_path: Path, data_path: Path | None = None):
    logger.info(f"Executing SQL file: {sql_path.name}")

    conn = get_connection()
    cur = conn.cursor()

    try:
        with open(sql_path, "r", encoding="utf-8") as f:
            sql = f.read()

        # Détection COPY FROM STDIN (bonne pratique)
        if "COPY" in sql.upper() and "FROM STDIN" in sql.upper():
            if data_path is None:
                raise ValueError(
                    f"COPY FROM STDIN détecté dans {sql_path.name} "
                    f"mais aucun fichier data fourni"
                )

            logger.info(f"Loading data file: {data_path.name}")

            with open(data_path, "r", encoding="utf-8") as data_file:
                cur.copy_expert(sql, data_file)
        else:
            cur.execute(sql)

        conn.commit()
        logger.info(f"SUCCESS: {sql_path.name}")

    except Exception as e:
        conn.rollback()
        logger.error(f"FAILED: {sql_path.name}")
        logger.exception(e)
        raise

    finally:
        cur.close()
        conn.close()
        logger.info(f"Finished executing SQL file: {sql_path.name}")
