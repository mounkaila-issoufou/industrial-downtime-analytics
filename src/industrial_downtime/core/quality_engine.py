import random

from industrial_downtime.core.ids import generate_id
from industrial_downtime.config.quality_catalog import pick_defect

def generate_quality_for_hour(prod_id, actual_production):
    """
    Génère :
    - 1 inspection qualité par heure
    - plusieurs défauts associés

    Parameters
    ----------
    prod_id : str
    actual_production : int

    Returns
    -------
    inspections : list[dict]
    defects : list[dict]
    """

    inspections = []
    defects = []

    # Pas de production = pas de qualité
    if actual_production == 0:
        return inspections, defects

    inspected_units = actual_production

    # Taux de défaut réaliste (0.5% → 3%)
    defect_rate = random.uniform(0.005, 0.03)

    defective_units = int(inspected_units * defect_rate)

    inspection_id = generate_id("QI")

    # ======================
    # INSPECTION
    # ======================
    inspections.append(
        {
            "inspection_id": inspection_id,
            "hourly_prod_id": prod_id,
            "inspected_units": inspected_units,
            "defective_units": defective_units,
            "good_units": inspected_units - defective_units,
        }
    )

    # ======================
    # DÉFAUTS DÉTAILLÉS
    # ======================
    remaining = defective_units

    while remaining > 0:
        defect = pick_defect()

        units = random.randint(1, min(remaining, 5))
        remaining -= units

        defects.append(
            {
                "quality_event_id": generate_id("QE"),
                "inspection_id": inspection_id,
                "defect_type": defect.defect_type,
                "defect_category": defect.category,
                "defective_units": units,
            }
        )

    return inspections, defects
