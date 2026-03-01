from pathlib import Path

from industrial_downtime.utils.logger import logger
from industrial_downtime.config.config import RAW_DATA_DIR
from industrial_downtime.ingestion.run_generation import run_data_generation_pipeline
from industrial_downtime.db.run_sql import run_sql_file


SQL_DIR = Path("sql")


# ==========================================================
# DATABASE INITIALIZATION (DDL ONLY)
# ==========================================================

def init_db():
    logger.info("🧱 Initializing database structure (DDL)")

    # Schemas
    run_sql_file(SQL_DIR / "ddl/00_create_staging_schema.sql")
    run_sql_file(SQL_DIR / "ddl/01_create_operational_schema.sql")
    run_sql_file(SQL_DIR / "ddl/11_create_schema_analytique.sql")

    # Staging tables
    run_sql_file(SQL_DIR / "ddl/19_create_stg_shift_supervision_table.sql")
    run_sql_file(SQL_DIR / "ddl/20_create_stg_shift_operator_assignment_table.sql")
    run_sql_file(SQL_DIR / "ddl/21_create_stg_hourly_production_table.sql")
    run_sql_file(SQL_DIR / "ddl/22_create_stg_production_events_table.sql")

    # Operational tables
    run_sql_file(SQL_DIR / "ddl/02_create_factory_table.sql")
    run_sql_file(SQL_DIR / "ddl/03_create_workshop_table.sql")
    run_sql_file(SQL_DIR / "ddl/04_create_production_line_table.sql")
    run_sql_file(SQL_DIR / "ddl/05_create_operator_table.sql")
    run_sql_file(SQL_DIR / "ddl/06_create_team_lead_table.sql")
    run_sql_file(SQL_DIR / "ddl/07_create_shift_supervision_table.sql")
    run_sql_file(SQL_DIR / "ddl/08_create_shift_operator_assignment_table.sql")
    run_sql_file(SQL_DIR / "ddl/09_create_hourly_production_table.sql")
    run_sql_file(SQL_DIR / "ddl/10_create_production_events_table.sql")

    # Data Warehouse tables
    run_sql_file(SQL_DIR / "ddl/12_create_dim_time_table.sql")
    run_sql_file(SQL_DIR / "ddl/13_create_dim_machine_table.sql")
    run_sql_file(SQL_DIR / "ddl/14_create_dim_team_table.sql")
    run_sql_file(SQL_DIR / "ddl/15_create_dim_organe_element_table.sql")
    run_sql_file(SQL_DIR / "ddl/16_create_fact_hourly_performance_table.sql")
    run_sql_file(SQL_DIR / "ddl/17_create_fact_production_events_table.sql")

    logger.info("✔ Database structure ready")


# ==========================================================
# DATA RESET (OPTIONAL)
# ==========================================================

def reset_data():
    logger.info("🔄 Resetting data layers (TRUNCATE)")

    run_sql_file(SQL_DIR / "reset/01_truncate_staging_tables.sql")
    run_sql_file(SQL_DIR / "reset/00_truncate_ops_tables.sql")
    run_sql_file(SQL_DIR / "reset/02_truncate_dw_tables.sql")

    logger.info("✔ Data reset completed")


# ==========================================================
# DATA PIPELINE (DML ONLY)
# ==========================================================

def run_pipeline():
    logger.info("🚀 PIPELINE STARTED")

    # ------------------------------------------------------
    # 1️⃣ Generate mock data
    # ------------------------------------------------------
    logger.info("▶ Generating mock production data")
    run_data_generation_pipeline()
    logger.info("✔ Mock data generated")

    # ------------------------------------------------------
    # 2️⃣ Load staging
    # ------------------------------------------------------
    logger.info("▶ Loading staging tables")

    run_sql_file(
        SQL_DIR / "dml/01_load_stg_shift_supervision.sql",
        RAW_DATA_DIR / "shift_supervision.csv"
    )

    run_sql_file(
        SQL_DIR / "dml/02_load_stg_shift_operator_assignment.sql",
        RAW_DATA_DIR / "shift_operator_assignment.csv"
    )

    run_sql_file(
        SQL_DIR / "dml/03_load_stg_hourly_production.sql",
        RAW_DATA_DIR / "hourly_production.csv"
    )

    run_sql_file(
        SQL_DIR / "dml/04_load_stg_production_events.sql",
        RAW_DATA_DIR / "production_events.csv"
    )

    logger.info("✔ Staging loaded")

    # ------------------------------------------------------
    # 3️⃣ Load operational layer
    # ------------------------------------------------------
    logger.info("▶ Loading operational layer")

    run_sql_file(SQL_DIR / "dml/05_load_ops_factory.sql")
    run_sql_file(SQL_DIR / "dml/06_load_ops_operator.sql")
    run_sql_file(SQL_DIR / "dml/07_load_ops_team_lead.sql")
    run_sql_file(SQL_DIR / "dml/08_load_ops_workshop.sql")
    run_sql_file(SQL_DIR / "dml/09_load_ops_production_line.sql")
    run_sql_file(SQL_DIR / "dml/10_load_ops_shift_supervision.sql")
    run_sql_file(SQL_DIR / "dml/11_load_ops_shift_operator_assignment.sql")
    run_sql_file(SQL_DIR / "dml/12_load_ops_hourly_production.sql")
    run_sql_file(SQL_DIR / "dml/13_load_ops_production_events.sql")

    # ------------------------------------------------------
    # 4️⃣ Load Data Warehouse
    # ------------------------------------------------------
    logger.info("▶ Loading data warehouse")

    run_sql_file(SQL_DIR / "dml/14_load_dim_machine.sql")
    run_sql_file(SQL_DIR / "dml/15_load_dim_time.sql")
    run_sql_file(SQL_DIR / "dml/16_load_dim_team.sql")
    run_sql_file(SQL_DIR / "dml/17_load_dim_organe_element.sql")
    run_sql_file(SQL_DIR / "dml/18_load_fact_hourly_performance.sql")
    run_sql_file(SQL_DIR / "dml/19_load_fact_production_events.sql")

    logger.info("✔ Data warehouse load completed")
    logger.info("✅ END-TO-END PIPELINE COMPLETED SUCCESSFULLY")