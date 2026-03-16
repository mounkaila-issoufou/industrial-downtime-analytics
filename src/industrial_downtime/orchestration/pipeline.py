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
    run_sql_file(SQL_DIR / "ddl/stg/00_create_staging_schema.sql")
    run_sql_file(SQL_DIR / "ddl/ops/01_create_operational_schema.sql")
    run_sql_file(SQL_DIR / "ddl/dw/01_create_schema_analytique.sql")

    # Staging tables
    run_sql_file(SQL_DIR / "ddl/stg/01_create_stg_shift_supervision_table.sql")
    run_sql_file(SQL_DIR / "ddl/stg/02_create_stg_shift_operator_assignment_table.sql")
    run_sql_file(SQL_DIR / "ddl/stg/03_create_stg_hourly_production_table.sql")
    run_sql_file(SQL_DIR / "ddl/stg/04_create_stg_production_events_table.sql")
    #run_sql_file(SQL_DIR / "ddl/stg/05_create_stg_quality_events.sql")
    #run_sql_file(SQL_DIR / "ddl/stg/06_create_stg_quality_inspection.sql")

    # Operational tables
    run_sql_file(SQL_DIR / "ddl/ops/02_create_factory_table.sql")
    run_sql_file(SQL_DIR / "ddl/ops/03_create_workshop_table.sql")
    run_sql_file(SQL_DIR / "ddl/ops/04_create_production_line_table.sql")
    run_sql_file(SQL_DIR / "ddl/ops/05_create_operator_table.sql")
    run_sql_file(SQL_DIR / "ddl/ops/06_create_team_lead_table.sql")
    run_sql_file(SQL_DIR / "ddl/ops/07_create_shift_supervision_table.sql")
    run_sql_file(SQL_DIR / "ddl/ops/08_create_shift_operator_assignment_table.sql")
    run_sql_file(SQL_DIR / "ddl/ops/09_create_hourly_production_table.sql")
    run_sql_file(SQL_DIR / "ddl/ops/10_create_production_events_table.sql")
    #run_sql_file(SQL_DIR / "ddl/ops/11_create_quality_event.sql")
    #run_sql_file(SQL_DIR / "ddl/ops/12_create_quality_inspection.sql")
    #run_sql_file(SQL_DIR / "ddl/ops/13_create_quality_defect.sql")


    # Data Warehouse tables
    run_sql_file(SQL_DIR / "ddl/dw/dimensions/02_create_dim_time_table.sql")
    run_sql_file(SQL_DIR / "ddl/dw/dimensions/03_create_dim_machine_table.sql")
    run_sql_file(SQL_DIR / "ddl/dw/dimensions/04_create_dim_team_table.sql")
    run_sql_file(SQL_DIR / "ddl/dw/dimensions/05_create_dim_organe_element_table.sql")
    run_sql_file(SQL_DIR / "ddl/dw/facts/06_create_fact_hourly_performance_table.sql")
    run_sql_file(SQL_DIR / "ddl/dw/facts/07_create_fact_production_events_table.sql")
    #run_sql_file(SQL_DIR / "ddl/dw/dimensions/08_create_dim_quality_defect.sql")
    #run_sql_file(SQL_DIR / "ddl/dw/dimensions/09_create_dim_quality_inspection.sql")
    #run_sql_file(SQL_DIR / "ddl/dw/facts/09_fact_quality_events.sql")

    # PARTITIONS INITIAL SETUP
    run_sql_file(SQL_DIR / "ddl/dw/partitions/partitioning_setup.sql")

    # INDEXES
    run_sql_file(SQL_DIR / "ddl/dw/indexes/indexes_dw.sql")
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
        SQL_DIR / "dml/stg/01_load_stg_shift_supervision.sql",
        RAW_DATA_DIR / "shift_supervision.csv",
    )

    run_sql_file(
        SQL_DIR / "dml/stg/02_load_stg_shift_operator_assignment.sql",
        RAW_DATA_DIR / "shift_operator_assignment.csv",
    )

    run_sql_file(
        SQL_DIR / "dml/stg/03_load_stg_hourly_production.sql",
        RAW_DATA_DIR / "hourly_production.csv",
    )

    run_sql_file(
        SQL_DIR / "dml/stg/04_load_stg_production_events.sql",
        RAW_DATA_DIR / "production_events.csv",
    )
    #run_sql_file(
    #    SQL_DIR / "dml/stg/05_load_stg_quality_events.sql",
    #    RAW_DATA_DIR / "quality_events.csv",
    #)


    logger.info("✔ Staging loaded")

    # ------------------------------------------------------
    # 3️⃣ Load operational layer
    # ------------------------------------------------------
    logger.info("▶ Loading operational layer")

    run_sql_file(SQL_DIR / "dml/ops/01_load_ops_factory.sql")
    run_sql_file(SQL_DIR / "dml/ops/02_load_ops_operator.sql")
    run_sql_file(SQL_DIR / "dml/ops/03_load_ops_team_lead.sql")
    run_sql_file(SQL_DIR / "dml/ops/06_load_ops_workshop.sql")
    run_sql_file(SQL_DIR / "dml/ops/04_load_ops_production_line.sql")
    run_sql_file(SQL_DIR / "dml/ops/05_load_ops_shift_supervision.sql")
    run_sql_file(SQL_DIR / "dml/ops/07_load_ops_shift_operator_assignment.sql")
    run_sql_file(SQL_DIR / "dml/ops/08_load_ops_hourly_production.sql")
    run_sql_file(SQL_DIR / "dml/ops/09_load_ops_production_events.sql")
    #run_sql_file(SQL_DIR / "dml/ops/10_load_ops_quality_inspection.sql")
    #run_sql_file(SQL_DIR / "dml/ops/11_load_ops_quality_events.sql")
    #run_sql_file(SQL_DIR / "dml/ops/12_load_ops_quality_defect.sql")

    # ------------------------------------------------------
    # 4️⃣ Load Data Warehouse
    # ------------------------------------------------------
    logger.info("▶ Loading data warehouse")
    run_sql_file(SQL_DIR / "ddl/dw/partitions/create_partitions.sql")
    logger.info("✔ Partition check completed")
    run_sql_file(SQL_DIR / "dml/dw/01_load_dim_machine.sql")
    run_sql_file(SQL_DIR / "dml/dw/02_load_dim_time.sql")
    run_sql_file(SQL_DIR / "dml/dw/03_load_dim_team.sql")
    run_sql_file(SQL_DIR / "dml/dw/04_load_dim_organe_element.sql")
    run_sql_file(SQL_DIR / "dml/dw/05_load_fact_hourly_performance.sql")
    run_sql_file(SQL_DIR / "dml/dw/06_load_fact_production_events.sql")
    #run_sql_file(SQL_DIR / "dml/dw/07_load_dim_quality_defect.sql")
    #run_sql_file(SQL_DIR / "dml/dw/08_load_fact_quality_events.sql")




    logger.info("✔ Data warehouse load completed")
    logger.info("✅ END-TO-END PIPELINE COMPLETED SUCCESSFULLY")
