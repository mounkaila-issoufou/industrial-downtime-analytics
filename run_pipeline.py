from pathlib import Path
from src.utils.logger import logger



# =========================
# Database pipeline
# =========================
from src.db.run_sql import run_sql_file


SQL_DIR = Path("sql")


def main():
    logger.info("🚀 PIPELINE STARTED")

    # =========================
    # 1. PYTHON DATA PIPELINE
    # =========================
    logger.info("▶ Starting Python data pipeline")


    # =========================
    # 2. DATABASE STRUCTURE
    # =========================
    logger.info("▶ Initializing database schemas & tables")

    run_sql_file(SQL_DIR / "ddl/01_create_operational_schema.sql")
    run_sql_file(SQL_DIR / "ddl/02_create_factory_table.sql")
    run_sql_file(SQL_DIR / "ddl/03_create_workshop_table.sql")
    run_sql_file(SQL_DIR / "ddl/04_create_production_line_table.sql")
    run_sql_file(SQL_DIR / "ddl/05_create_operator_table.sql")
    run_sql_file(SQL_DIR / "ddl/06_create_team_lead_table.sql")
    run_sql_file(SQL_DIR / "ddl/07_create_shift_supervision_table.sql")
    run_sql_file(SQL_DIR / "ddl/08_create_shift_operator_assignment_table.sql")
    run_sql_file(SQL_DIR / "ddl/09_create_hourly_production_table.sql")
    run_sql_file(SQL_DIR / "ddl/10_create_production_events_table.sql")

    run_sql_file(SQL_DIR / "ddl/11_create_schema_analytique.sql")
    run_sql_file(SQL_DIR / "ddl/12_create_dim_time_table.sql")
    run_sql_file(SQL_DIR / "ddl/13_create_dim_machine_table.sql")
    run_sql_file(SQL_DIR / "ddl/14_create_dim_team_table.sql")
    run_sql_file(SQL_DIR / "ddl/15_create_dim_organe_element_table.sql")
    run_sql_file(SQL_DIR / "ddl/16_create_fact_hourly_performance_table.sql")
    run_sql_file(SQL_DIR / "ddl/17_create_fact_production_events_table.sql")
    
    logger.info("✔ Database structure ready")

    # =========================
    # 3. LOAD STAGING
    # =========================
    logger.info("▶ Loading staging tables")

    logger.info("✔ Staging loaded")

    # =========================
    # 4. DATA WAREHOUSE LOAD
    # =========================
    logger.info("▶ Reseting dimensions & facts")




    logger.info("✔ Data warehouse load completed")
    logger.info("✅ END-TO-END PIPELINE COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()
