
import random

from industrial_downtime.config.settings import RANDOM_SEED
from industrial_downtime.ingestion.generate_shift_context import (
    generate_shift_context,
)
from industrial_downtime.ingestion.generate_mock_production_data import (
    generate_production,
)
from industrial_downtime.utils.export import export_csv
from industrial_downtime.core.context_store import context
from industrial_downtime.utils.logger import logger


def run_data_generation_pipeline():
    logger.info("🎲 Starting mock data generation")

    # --------------------------
    # Seed (reproductibilité)
    # --------------------------
    random.seed(RANDOM_SEED)

    # --------------------------
    # 1️⃣ Generate shift context
    # --------------------------
    logger.info("▶ Generating shift context")
    generate_shift_context()

    # --------------------------
    # 2️⃣ Generate production + quality
    # --------------------------
    logger.info("▶ Generating production & quality data")

    (
        hourly_production,
        production_events,
        quality_inspections,
        quality_events,
    ) = generate_production()

    # --------------------------
    # 3️⃣ Export CSV (RAW layer)
    # --------------------------
    logger.info("▶ Exporting CSV files")

    export_csv(context.shifts, "shift_supervision.csv")
    export_csv(context.operator_assignments, "shift_operator_assignment.csv")

    export_csv(hourly_production, "hourly_production.csv")
    export_csv(production_events, "production_events.csv")

    # ✅ QUALITY EXPORT
    export_csv(quality_inspections, "quality_inspections.csv")
    export_csv(quality_events, "quality_events.csv")
    logger.info("✔ Mock data generation completed successfully")


run_data_generation_pipeline()