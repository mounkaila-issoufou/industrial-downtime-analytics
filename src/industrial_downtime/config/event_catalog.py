from dataclasses import dataclass
from enum import Enum
from typing import Dict
import random

from dataclasses import dataclass
from enum import Enum
from typing import Dict
import random


# ==========================
# Catégories (macro BI)
# ==========================

class EventCategory(str, Enum):
    TECHNICAL = "technical"
    PROCESS = "process"
    QUALITY = "quality"
    ORGANIZATION = "organization"
    HUMAN = "human"
    CHANGEOVER = "changeover"
    PLANNED = "planned"
    MAINTENANCE = "maintenance"


# ==========================
# Familles (🔥 BI + Markov)
# ==========================

class EventFamily(str, Enum):
    MECHANICAL = "mechanical"
    ELECTRICAL = "electrical"
    SENSOR = "sensor"
    CONVEYOR = "conveyor"
    SAFETY = "safety"
    PROCESS_DRIFT = "process_drift"
    QUALITY_DEFECT = "quality_defect"
    SUPPLY = "supply"
    HUMAN_ACTION = "human_action"
    CHANGEOVER = "changeover"
    BREAK = "break"
    MAINTENANCE = "maintenance"


# ==========================
# Dataclass enrichie
# ==========================

@dataclass(frozen=True)
class Event:
    event: str
    category: EventCategory
    family: EventFamily

    organ: str
    element: str

    operator_action: str

    base_probability: float

    mean_duration: int
    duration_std: int

    is_planned: bool


# ==========================
# Catalogue complet
# ==========================

EVENT_CATALOG: Dict[str, Event] = {

    # ======================
    # CONVEYORS
    # ======================

    "infeed_conveyor_failure": Event(
        "infeed_conveyor_failure", EventCategory.TECHNICAL, EventFamily.CONVEYOR,
        "stacker", "infeed_conveyor",
        "check upstream flow / remove jam",
        0.04, 15, 5, False
    ),

    "outfeed_conveyor_failure": Event(
        "outfeed_conveyor_failure", EventCategory.TECHNICAL, EventFamily.CONVEYOR,
        "case_packer", "outfeed_conveyor",
        "clear jam / restart line",
        0.05, 12, 4, False
    ),

    "conveyor_output_jam": Event(
        "conveyor_output_jam", EventCategory.TECHNICAL, EventFamily.CONVEYOR,
        "outfeed_zone", "belt",
        "remove blocked product",
        0.06, 8, 3, False
    ),

    # ======================
    # SAFETY
    # ======================

    "door_safety_fault": Event(
        "door_safety_fault", EventCategory.TECHNICAL, EventFamily.SAFETY,
        "safety_system", "door",
        "reset safety circuit",
        0.02, 10, 2, False
    ),

    "axis_collision": Event(
        "axis_collision", EventCategory.TECHNICAL, EventFamily.SAFETY,
        "robot", "axis",
        "reset + inspect collision",
        0.01, 25, 8, False
    ),

    # ======================
    # SENSORS / ELECTRICAL
    # ======================

    "delta_sensor_fault_1": Event(
        "delta_sensor_fault_1", EventCategory.TECHNICAL, EventFamily.SENSOR,
        "delta_robot", "sensor_1",
        "clean sensor",
        0.03, 5, 1, False
    ),

    "delta_sensor_fault_2": Event(
        "delta_sensor_fault_2", EventCategory.TECHNICAL, EventFamily.SENSOR,
        "delta_robot", "sensor_2",
        "check alignment",
        0.025, 6, 2, False
    ),

    "photoelectric_sensor_fault": Event(
        "photoelectric_sensor_fault", EventCategory.TECHNICAL, EventFamily.SENSOR,
        "line", "photoeye",
        "clean / recalibrate",
        0.04, 4, 1, False
    ),

    # ======================
    # MECHANICAL
    # ======================

    "base_plate_transfer_fault": Event(
        "base_plate_transfer_fault", EventCategory.TECHNICAL, EventFamily.MECHANICAL,
        "base_plate_system", "transfer",
        "realign plates",
        0.05, 20, 6, False
    ),

    "base_plate_position_fault": Event(
        "base_plate_position_fault", EventCategory.TECHNICAL, EventFamily.MECHANICAL,
        "base_plate_system", "positioning",
        "adjust positioning",
        0.04, 18, 5, False
    ),

    "product_detachment_fault": Event(
        "product_detachment_fault", EventCategory.TECHNICAL, EventFamily.MECHANICAL,
        "gripper", "vacuum",
        "check suction / grip",
        0.03, 10, 3, False
    ),

    "stacker_jam": Event(
        "stacker_jam", EventCategory.TECHNICAL, EventFamily.MECHANICAL,
        "stacker", "tray",
        "remove jam",
        0.06, 14, 4, False
    ),

    "destacker_jam": Event(
        "destacker_jam", EventCategory.TECHNICAL, EventFamily.MECHANICAL,
        "destacker", "tray",
        "clear blockage",
        0.05, 13, 4, False
    ),

    "tray_blocked_in_stacker": Event(
        "tray_blocked_in_stacker", EventCategory.TECHNICAL, EventFamily.MECHANICAL,
        "stacker", "tray_path",
        "remove stuck tray",
        0.04, 12, 3, False
    ),

    # ======================
    # PROCESS
    # ======================

    "empty_tray_before_stacker": Event(
        "empty_tray_before_stacker", EventCategory.PROCESS, EventFamily.PROCESS_DRIFT,
        "infeed", "tray_presence",
        "refill trays",
        0.05, 7, 2, False
    ),

    "film_retake": Event(
        "film_retake", EventCategory.PROCESS, EventFamily.PROCESS_DRIFT,
        "wrapper", "film",
        "adjust film tension",
        0.03, 6, 2, False
    ),

    "cassette_sticker_adjustment": Event(
        "cassette_sticker_adjustment", EventCategory.PROCESS, EventFamily.PROCESS_DRIFT,
        "labeler", "cassette",
        "adjust alignment",
        0.02, 10, 3, False
    ),

    # ======================
    # QUALITY
    # ======================

    "missing_film_imprint": Event(
        "missing_film_imprint", EventCategory.QUALITY, EventFamily.QUALITY_DEFECT,
        "printer", "ink",
        "check printer",
        0.02, 9, 3, False
    ),

    "product_length_out_of_range": Event(
        "product_length_out_of_range", EventCategory.QUALITY, EventFamily.QUALITY_DEFECT,
        "forming", "cutting",
        "adjust format",
        0.015, 12, 4, False
    ),

    # ======================
    # ORGANIZATION
    # ======================

    "material_shortage": Event(
        "material_shortage", EventCategory.ORGANIZATION, EventFamily.SUPPLY,
        "supply_chain", "material",
        "wait for supply",
        0.03, 30, 10, False
    ),

    "poor_material_supply": Event(
        "poor_material_supply", EventCategory.ORGANIZATION, EventFamily.SUPPLY,
        "supply_chain", "flow",
        "stabilize supply",
        0.025, 20, 6, False
    ),

    # ======================
    # HUMAN
    # ======================

    "label_ribbon_replacement": Event(
        "label_ribbon_replacement", EventCategory.HUMAN, EventFamily.HUMAN_ACTION,
        "printer", "ribbon",
        "replace ribbon",
        0.02, 8, 2, True
    ),

    "ink_ribbon_replacement": Event(
        "ink_ribbon_replacement", EventCategory.HUMAN, EventFamily.HUMAN_ACTION,
        "printer", "ink_ribbon",
        "replace ink",
        0.02, 7, 2, True
    ),

    # ======================
    # CHANGEOVER
    # ======================

    "format_changeover": Event(
        "format_changeover", EventCategory.CHANGEOVER, EventFamily.CHANGEOVER,
        "line", "format",
        "perform changeover",
        0.015, 45, 10, True
    ),

    # ======================
    # PLANNED
    # ======================

    "operator_break": Event(
        "operator_break", EventCategory.PLANNED, EventFamily.BREAK,
        "human", "break",
        "pause",
        0.01, 10, 2, True
    ),

    "cleaning": Event(
        "cleaning", EventCategory.PLANNED, EventFamily.BREAK,
        "line", "cleaning",
        "clean machine",
        0.01, 20, 5, True
    ),

    # ======================
    # MAINTENANCE
    # ======================

    "planned_maintenance": Event(
        "planned_maintenance", EventCategory.MAINTENANCE, EventFamily.MAINTENANCE,
        "line", "maintenance",
        "scheduled maintenance",
        0.01, 60, 15, True
    ),

    "unplanned_maintenance": Event(
        "unplanned_maintenance", EventCategory.MAINTENANCE, EventFamily.MAINTENANCE,
        "line", "repair",
        "repair failure",
        0.02, 50, 20, False
    ),
}

# ==========================
# GROUPES MARKOV (niveau expert)
# ==========================

# 🔹 Micro-arrêts (courts, fréquents, faible impact unitaire)
MICRO_STOP_FAMILIES = [
    EventFamily.SENSOR,
    EventFamily.CONVEYOR,
    EventFamily.PROCESS_DRIFT,
]

# 🔹 Pannes (impact fort, arrêt long)
FAILURE_FAMILIES = [
    EventFamily.MECHANICAL,
    EventFamily.SAFETY,
    EventFamily.ELECTRICAL,
]

# 🔹 Problèmes qualité (peuvent ne pas arrêter la ligne)
QUALITY_FAMILIES = [
    EventFamily.QUALITY_DEFECT,
]

# 🔹 Arrêts organisationnels (externes machine)
ORGANIZATIONAL_FAMILIES = [
    EventFamily.SUPPLY,
]

# 🔹 Actions humaines (semi-planifiées / dépend opérateur)
HUMAN_FAMILIES = [
    EventFamily.HUMAN_ACTION,
]

# 🔹 Changements de série
CHANGEOVER_FAMILIES = [
    EventFamily.CHANGEOVER,
]

# 🔹 Arrêts planifiés
PLANNED_FAMILIES = [
    EventFamily.BREAK,
]

# 🔹 Maintenance (planifiée + corrective)
MAINTENANCE_FAMILIES = [
    EventFamily.MAINTENANCE,
]


# ==========================
# ROOT CAUSE PICKER (fixé)
# ==========================

def pick_root_cause(families: list[EventFamily]) -> str:

    candidates = [
        e for e in EVENT_CATALOG.values()
        if e.family in families
    ]

    if not candidates:
        raise ValueError("No candidates found for given families")

    total_weight = sum(e.base_probability for e in candidates)

    r = random.uniform(0, total_weight)
    cumulative = 0

    for event in candidates:
        cumulative += event.base_probability
        if r <= cumulative:
            return event.event

    return candidates[-1].event
