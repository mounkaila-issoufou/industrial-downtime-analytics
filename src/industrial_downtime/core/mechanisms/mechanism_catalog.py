from enum import Enum
from typing import Dict, List
from industrial_downtime.core.markov_engine import LineState


# =========================
# MECHANISMS (ROOT CAUSES)
# =========================
class Mechanism(Enum):
    # mécanique
    WEAR = "wear"
    MISALIGNMENT = "misalignment"
    LUBRICATION_ISSUE = "lubrication_issue"

    # process
    PROCESS_DRIFT = "process_drift"
    CALIBRATION_LOSS = "calibration_loss"

    # humain
    FATIGUE = "fatigue"
    HUMAN_ERROR = "human_error"

    # flux / orga
    SUPPLY_DELAY = "supply_delay"
    PLANNING_ISSUE = "planning_issue"

    # micro causes
    SENSOR_NOISE = "sensor_noise"
    MICRO_JAM = "micro_jam"

    UNKNOWN = "unknown"


# =========================
# STATE → MECHANISMS MAPPING
# =========================
STATE_MECHANISMS: Dict[LineState, List[Mechanism]] = {
    LineState.FAILURE: [
        Mechanism.WEAR,
        Mechanism.MISALIGNMENT,
        Mechanism.LUBRICATION_ISSUE,
    ],
    LineState.MICRO_STOP: [
        Mechanism.SENSOR_NOISE,
        Mechanism.MICRO_JAM,
    ],
    LineState.QUALITY: [
        Mechanism.PROCESS_DRIFT,
        Mechanism.CALIBRATION_LOSS,
    ],
    LineState.HUMAN: [
        Mechanism.FATIGUE,
        Mechanism.HUMAN_ERROR,
    ],
    LineState.ORGANIZATION: [
        Mechanism.SUPPLY_DELAY,
        Mechanism.PLANNING_ISSUE,
    ],
}


# =========================
# OPTIONAL: BASE WEIGHTS
# =========================
MECHANISM_WEIGHTS: Dict[Mechanism, float] = {
    Mechanism.WEAR: 1.0,
    Mechanism.MISALIGNMENT: 0.8,
    Mechanism.LUBRICATION_ISSUE: 0.6,
    Mechanism.PROCESS_DRIFT: 0.9,
    Mechanism.CALIBRATION_LOSS: 0.7,
    Mechanism.FATIGUE: 0.8,
    Mechanism.HUMAN_ERROR: 0.7,
    Mechanism.SUPPLY_DELAY: 0.9,
    Mechanism.PLANNING_ISSUE: 0.6,
    Mechanism.SENSOR_NOISE: 1.0,
    Mechanism.MICRO_JAM: 0.9,
    Mechanism.UNKNOWN: 0.1,
}