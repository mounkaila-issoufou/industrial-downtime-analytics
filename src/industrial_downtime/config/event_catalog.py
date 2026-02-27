from dataclasses import dataclass
from enum import Enum
from typing import Dict

# ==========================
# Catégories d'événements
# ==========================
class EventCategory(str, Enum):
    MECHANICAL = "mechanical"
    ELECTRICAL = "electrical"
    PROCESS = "process"
    QUALITY = "quality"
    ORGANIZATION = "organization"
    OPERATOR = "operator"
    CHANGEOVER = "changeover"
    PLANNED = "planned"
    MAINTENANCE = "maintenance"
    OTHER = "other"

# ==========================
# Dataclass événement
# ==========================
@dataclass(frozen=True)
class Event:
    event: str
    category: EventCategory
    organ: str
    element: str
    operator_action: str

# ==========================
# Référentiel complet
# ==========================
EVENT_CATALOG: Dict[str, Event] = {
    "infeed_conveyor_failure": Event(
        event="infeed_conveyor_failure",
        category=EventCategory.MECHANICAL,
        organ="stacker",
        element="conveyor",
        operator_action="conveyor supply",
    ),
    "outfeed_conveyor_failure": Event(
        event="outfeed_conveyor_failure",
        category=EventCategory.MECHANICAL,
        organ="case_packer",
        element="conveyor",
        operator_action="product evacuation",
    ),
    "door_safety_fault": Event(
        event="door_safety_fault",
        category=EventCategory.ELECTRICAL,
        organ="safety_system",
        element="safety_door",
        operator_action="reset safety",
    ),
    "delta_sensor_fault_1": Event(
        event="delta_sensor_fault_1",
        category=EventCategory.ELECTRICAL,
        organ="delta_robot",
        element="sensor",
        operator_action="sensor check",
    ),
    "delta_sensor_fault_2": Event(
        event="delta_sensor_fault_2",
        category=EventCategory.ELECTRICAL,
        organ="delta_robot",
        element="sensor",
        operator_action="sensor check",
    ),
    "base_plate_transfer_fault": Event(
        event="base_plate_transfer_fault",
        category=EventCategory.MECHANICAL,
        organ="base_plate_system",
        element="transfer",
        operator_action="plate transfer",
    ),
    "short_break": Event(
        event="short_break",
        category=EventCategory.PLANNED,
        organ="human",
        element="micro_break",
        operator_action="pause"
    ),
    # ... ajouter tous les autres événements existants de ton constants/settings
}