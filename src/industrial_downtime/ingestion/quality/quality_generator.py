import random
from typing import List, Tuple, Dict

from industrial_downtime.core.ids import generate_id
from industrial_downtime.config.quality_catalog import pick_defect


def generate_quality_for_hour(
    hourly_prod_id: str,
    actual_production: int,
) -> Tuple[List[Dict], List[Dict]]:
    """
    Génère les inspections qualité et les événements défauts associés.
    Compatible avec stg.quality_inspection & stg.quality_events
    """

    quality_inspections = []
    quality_events = []



    if actual_production == 0:
        return [], []

    # 🟢 Fréquence inspections (réaliste)
    inspection_count = max(1, actual_production // 100)

    for _ in range(inspection_count):

        inspection_id = generate_id("QI")

        # 🟢 Taille échantillon dynamique
        sample_size = min(actual_production, random.randint(10, 30))

        # 🟢 Probabilité défaut (dépend du volume → plus réaliste)
        base_defect_rate = 0.03
        defect_probability = base_defect_rate + random.uniform(0, 0.02)

        defect_units = sum(
            1 for _ in range(sample_size)
            if random.random() < defect_probability
        )

        inspected_units = actual_production

        # Taux de défaut réaliste (0.5% → 3%)
        defect_rate = random.uniform(0.005, 0.03)

        defective_units = int(inspected_units * defect_rate)

        # 🟢 Création inspection
        quality_inspections.append(
            {
                "inspection_id": inspection_id,
                "hourly_prod_id": hourly_prod_id,
                "inspection_type": "VISUAL",
                "inspected_units": sample_size,
                "inspected_units": inspected_units,
                #"defective_units": defective_units,
                #"good_units": inspected_units - defective_units,
            }
        )

        # 🔴 Si aucun défaut → skip events
        if defect_units == 0:
            continue

        # 🟠 Regrouper les défauts par type (plus réaliste)
        defect_buckets = {}

        for _ in range(defect_units):
            defect = pick_defect()

            key = defect.defect_type

            if key not in defect_buckets:
                defect_buckets[key] = {
                    "defect": defect,
                    "count": 0,
                }

            defect_buckets[key]["count"] += 1

        # 🔴 Création events agrégés
        for bucket in defect_buckets.values():

            defect = bucket["defect"]
            count = bucket["count"]

            # 🟢 Scrap vs rework logique métier
            scrap_units = 0
            reworked_units = 0

            for _ in range(count):
                if defect.severity in ("high", "critical"):
                    scrap_units += 1
                else:
                    # 50% reworkable
                    if random.random() < 0.5:
                        reworked_units += 1
                    else:
                        scrap_units += 1

            quality_events.append(
                {
                    "quality_event_id": generate_id("QE"),
                    "inspection_id": inspection_id,
                    #"hourly_prod_id": hourly_prod_id,
                    "defect_category": defect.category.upper(),
                    "defect_family": defect.defect_type.split("_")[0],
                    "defect_type": defect.defect_type,
                    "defective_units": count,
                    "scrap_units": scrap_units,
                    "reworked_units": reworked_units,
                    "comment": "Auto-generated defect",
                }
            )

    return quality_inspections, quality_events