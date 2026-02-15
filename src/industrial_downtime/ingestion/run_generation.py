import random

from industrial_downtime.config.settings import RANDOM_SEED
from industrial_downtime.ingestion.generate_shift_context import generate_shift_context
from industrial_downtime.ingestion.generate_mock_production_data import generate_production
from industrial_downtime.utils.export import export_csv
from industrial_downtime.core.context_store import context


def run_data_generation_pipeline():
    random.seed(RANDOM_SEED)

    # 1) Génération du contexte shifts
    generate_shift_context()

    # 2) Génération des faits production
    hourly_prod, events = generate_production()

    # 3) Export en CSV (couche raw / staging)
    export_csv(context.shifts, "shift_supervision.csv")
    export_csv(context.operator_assignments, "shift_operator_assignment.csv")
    export_csv(hourly_prod, "hourly_production.csv")
    export_csv(events, "production_events.csv")

    print("✔ Génération cohérente terminée")


run_data_generation_pipeline()