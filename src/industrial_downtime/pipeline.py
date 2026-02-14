from pathlib import Path
from src.utils.logger import logger
from src.config.config import RAW_DATA_DIR
from src.ingestion.run_generation import run_data_generation_pipeline

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
    # 1. Generate mock production data
    # =========================
    logger.info("▶ Generating mock production data")
    run_data_generation_pipeline()
    logger.info("✔ Mock data generated")

    # =========================
    # 2. DATABASE STRUCTURE
    # =========================
    logger.info("▶ Initializing database schemas & tables")
    run_sql_file(SQL_DIR / "ddl/00_create_staging_schema.sql")
    run_sql_file(SQL_DIR / "ddl/19_create_stg_shift_supervision_table.sql")
    run_sql_file(SQL_DIR / "ddl/20_create_stg_shift_operator_assignment_table.sql")
    run_sql_file(SQL_DIR / "ddl/21_create_stg_hourly_production_table.sql")
    run_sql_file(SQL_DIR / "ddl/22_create_stg_production_events_table.sql")

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

    # =========================
    # 4. DATA WAREHOUSE LOAD
    # =========================
    logger.info("▶ Reseting dimensions & facts")
    run_sql_file(SQL_DIR / "dml/05_load_ops_factory.sql")
    run_sql_file(SQL_DIR / "dml/06_load_ops_operator.sql")
    run_sql_file(SQL_DIR / "dml/07_load_ops_team_lead.sql")
    run_sql_file(SQL_DIR / "dml/08_load_ops_workshop.sql")
    run_sql_file(SQL_DIR / "dml/09_load_ops_production_line.sql")
    run_sql_file(SQL_DIR / "dml/10_load_ops_shift_supervision.sql")
    run_sql_file(SQL_DIR / "dml/11_load_ops_shift_operator_assignment.sql")
    run_sql_file(SQL_DIR / "dml/12_load_ops_hourly_production.sql")
    run_sql_file(SQL_DIR / "dml/13_load_ops_production_events.sql")

    run_sql_file(SQL_DIR / "dml/14_load_dim_machine.sql")
    run_sql_file(SQL_DIR / "dml/15_load_dim_time.sql")

    run_sql_file(SQL_DIR / "dml/16_load_dim_team.sql")
    run_sql_file(SQL_DIR / "dml/17_load_dim_organe_element.sql")
    
    run_sql_file(SQL_DIR / "dml/18_load_fact_hourly_performance.sql")
    run_sql_file(SQL_DIR / "dml/19_load_fact_production_events.sql")






    logger.info("✔ Data warehouse load completed")
    logger.info("✅ END-TO-END PIPELINE COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()
