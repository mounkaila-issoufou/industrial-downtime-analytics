from dataclasses import dataclass
from enum import Enum
from typing import Dict
import random


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
    UNPLANNED = "unplanned"
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
@dataclass(frozen=True)
class Event:
    event: str
    category: EventCategory
    organ: str
    element: str
    operator_action: str
    base_probability: float
    mean_duration: int
    duration_std: int
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
        base_probability=0.05,
        mean_duration=15,
        duration_std=5,
    ),
    "outfeed_conveyor_failure": Event(
        event="outfeed_conveyor_failure",
        category=EventCategory.MECHANICAL,
        organ="case_packer",
        element="conveyor",
        operator_action="product evacuation",
        base_probability=0.03,
        mean_duration=12,
        duration_std=4,
    ),
    "door_safety_fault": Event(
        event="door_safety_fault",
        category=EventCategory.ELECTRICAL,
        organ="safety_system",
        element="safety_door",
        operator_action="reset safety",
        base_probability=0.02,
        mean_duration=10,
        duration_std=2,
    ),
    "delta_sensor_fault_1": Event(
        event="delta_sensor_fault_1",
        category=EventCategory.ELECTRICAL,
        organ="delta_robot",
        element="sensor",
        operator_action="sensor check",
        base_probability=0.01,
        mean_duration=5,
        duration_std=1,
    ),
    "delta_sensor_fault_2": Event(
        event="delta_sensor_fault_2",
        category=EventCategory.ELECTRICAL,
        organ="delta_robot",
        element="sensor",
        operator_action="sensor check",
        base_probability=0.01,
        mean_duration=5,
        duration_std=1,
    ),
    "base_plate_transfer_fault": Event(
        event="base_plate_transfer_fault",
        category=EventCategory.MECHANICAL,
        organ="base_plate_system",
        element="transfer",
        operator_action="plate transfer",
        base_probability=0.04,
        mean_duration=20,
        duration_std=6,
    ),
    "short_break": Event(
        event="short_break",
        category=EventCategory.PLANNED,
        organ="human",
        element="micro_break",
        operator_action="pause",
        base_probability=0.01,
        mean_duration=5,
        duration_std=1,
    ),
    "micro_stop": Event(
        event="micro_stop",
        category=EventCategory.UNPLANNED,
        organ="machine",
        element="minor_stoppage",
        operator_action="restart",
        base_probability=0.02,
        mean_duration=4,
        duration_std=1,
    ),
    "failure": Event(
        event="failure",
        category=EventCategory.UNPLANNED,
        organ="machine",
        element="major_stoppage",
        operator_action="repair",
        base_probability=0.01,
        mean_duration=18,
        duration_std=5,
    ),
    # ... ajouter tous les autres événements existants de ton constants/settings
}

MICRO_STOP_CATEGORIES = [
    EventCategory.ELECTRICAL,
    EventCategory.PROCESS,
]

FAILURE_CATEGORIES = [
    EventCategory.MECHANICAL,
    EventCategory.ELECTRICAL,
]

def pick_root_cause(categories: list[EventCategory]) -> str:

    candidates = [
        e for e in EVENT_CATALOG.values()
        if e.category in categories
    ]

    total_weight = sum(e.base_probability for e in candidates)

    r = random.uniform(0, total_weight)
    cumulative = 0

    for event in candidates:
        cumulative += event.base_probability
        if r <= cumulative:
            return event.event

    return candidates[-1].event