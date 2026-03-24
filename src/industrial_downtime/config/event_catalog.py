from dataclasses import dataclass
from enum import Enum
from typing import Dict
import random

# ==========================
# Catégories (niveau macro)
# ==========================

class EventCategory(str, Enum):
    TECHNICAL = "technical"
    PROCESS = "process"
    QUALITY = "quality"
    ORGANIZATION = "organization"
    HUMAN = "human"
    PLANNED = "planned"


# ==========================
# Familles (🔥 clé BI)
# ==========================

class EventFamily(str, Enum):
    MECHANICAL = "mechanical"
    ELECTRICAL = "electrical"
    SENSOR = "sensor"
    CONVEYOR = "conveyor"
    SAFETY = "safety"
    BREAK = "break"
    MICRO_STOP = "micro_stop"
    FAILURE = "failure"


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
# Catalogue
# ==========================

EVENT_CATALOG: Dict[str, Event] = {

    # ======================
    # CONVEYOR
    # ======================
    "infeed_conveyor_failure": Event(
        event="infeed_conveyor_failure",
        category=EventCategory.TECHNICAL,
        family=EventFamily.CONVEYOR,
        organ="stacker",
        element="infeed_conveyor",
        operator_action="check product feed",
        base_probability=0.02,
        mean_duration=15,
        duration_std=5,
        is_planned=False,
    ),

    "outfeed_conveyor_failure": Event(
        event="outfeed_conveyor_failure",
        category=EventCategory.TECHNICAL,
        family=EventFamily.CONVEYOR,
        organ="case_packer",
        element="outfeed_conveyor",
        operator_action="clear jam",
        base_probability=0.03,
        mean_duration=12,
        duration_std=4,
        is_planned=False,
    ),

    # ======================
    # SAFETY
    # ======================
    "door_safety_fault": Event(
        event="door_safety_fault",
        category=EventCategory.TECHNICAL,
        family=EventFamily.SAFETY,
        organ="safety_system",
        element="safety_door",
        operator_action="reset safety",
        base_probability=0.02,
        mean_duration=10,
        duration_std=2,
        is_planned=False,
    ),

    # ======================
    # SENSORS
    # ======================
    "delta_sensor_fault": Event(
        event="delta_sensor_fault",
        category=EventCategory.TECHNICAL,
        family=EventFamily.SENSOR,
        organ="delta_robot",
        element="sensor",
        operator_action="sensor cleaning",
        base_probability=0.02,
        mean_duration=5,
        duration_std=1,
        is_planned=False,
    ),

    # ======================
    # MECHANICAL
    # ======================
    "base_plate_transfer_fault": Event(
        event="base_plate_transfer_fault",
        category=EventCategory.TECHNICAL,
        family=EventFamily.MECHANICAL,
        organ="base_plate_system",
        element="transfer",
        operator_action="realign plates",
        base_probability=0.04,
        mean_duration=20,
        duration_std=6,
        is_planned=False,
    ),

    # ======================
    # HUMAN / PLANNED
    # ======================
    "short_break": Event(
        event="short_break",
        category=EventCategory.PLANNED,
        family=EventFamily.BREAK,
        organ="human",
        element="break",
        operator_action="pause",
        base_probability=0.01,
        mean_duration=5,
        duration_std=1,
        is_planned=True,
    ),
}


# ==========================
# GROUPES POUR MARKOV
# ==========================

MICRO_STOP_FAMILIES = [
    EventFamily.SENSOR,
    EventFamily.CONVEYOR,
]

FAILURE_FAMILIES = [
    EventFamily.MECHANICAL,
    EventFamily.SAFETY,
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
