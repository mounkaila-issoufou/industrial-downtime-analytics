from enum import Enum
from dataclasses import dataclass
from typing import Dict

from numpy import random
from industrial_downtime.core.markov_engine import LineState 


def build_transition_matrix(robustness: float) -> dict[LineState, dict[LineState, float]]:
    """
    Génère une matrice de transition simple basée sur la robustesse.
    robustness = 0.0 (fragile) → plus de pannes
    robustness = 1.0 (robuste) → très stable
    """

    # Base probabilities
    failure_prob = 0.10 * (1 - robustness)
    micro_stop_prob = 0.20 * (1 - robustness)
    running_prob = 1.0 - (failure_prob + micro_stop_prob)

    return {
        LineState.RUNNING: {
            LineState.RUNNING: running_prob,
            LineState.MICRO_STOP: micro_stop_prob,
            LineState.FAILURE: failure_prob,
        },
        LineState.MICRO_STOP: {
            LineState.RUNNING: 1.0,
        },
        LineState.FAILURE: {
            LineState.REPAIR: 1.0,
        },
        LineState.REPAIR: {
            LineState.RUNNING: 1.0,
        },
    }

@dataclass(frozen=True)
class LineConfig:
    code: str
    theoretical_capacity_per_hour: int
    units_per_minute: int
    reliability_target: float
    robustness: float  # 0.0 fragile → 1.0 très robuste
    transition_matrix: dict[LineState, dict[LineState, float]]

@dataclass(frozen=True)
class Workshop:
    name: str
    lines: Dict[str, LineConfig]


# ==========================
# OV LINES
# ==========================
OV_LINES = {
    "L_OV_MS": LineConfig(
        "L_OV_MS", 1200, 20, 0.60, 0.5,
        build_transition_matrix(0.5)
    ),
    "L_OV_ES": LineConfig(
        "L_OV_ES", 1500, 25, 0.65, 0.6,
        build_transition_matrix(0.6)
    ),
    "L_OV_X": LineConfig(
        "L_OV_X", 1800, 30, 0.70, 0.7,
        build_transition_matrix(0.7)
    ),
    "L_OV_Y": LineConfig(
        "L_OV_Y", 1560, 26, 0.63, 0.55,
        build_transition_matrix(0.55)
    ),
    "L_OV_Z": LineConfig(
        "L_OV_Z", 1380, 23, 0.58, 0.45,
        build_transition_matrix(0.45)
    ),
}

# ==========================
# CAMEMBERT LINES
# ==========================
CAM_LINES = {
    "L_CAM_A": LineConfig("L_CAM_A", 1020, 17, 0.55, 0.5, build_transition_matrix(0.5)),
    "L_CAM_B": LineConfig("L_CAM_B", 1080, 18, 0.57, 0.55, build_transition_matrix(0.55)),
    "L_CAM_C": LineConfig("L_CAM_C", 1320, 22, 0.62, 0.6, build_transition_matrix(0.6)),
}

# ==========================
# PORTION LINES
# ==========================
PORTION_LINES = {
    "L_PORTION_1": LineConfig("L_PORTION_1", 900, 15, 0.66, 0.5, build_transition_matrix(0.5)),
    "L_PORTION_2": LineConfig("L_PORTION_2", 960, 16, 0.68, 0.55, build_transition_matrix(0.55)),
}

WORKSHOPS: Dict[str, Workshop] = {
    "OVALE": Workshop("OVALE", OV_LINES),
    "CAMEMBERT": Workshop("CAMEMBERT", CAM_LINES),
    "PORTION": Workshop("PORTION", PORTION_LINES),
}

STATE_DURATION = {
    LineState.MICRO_STOP: (4, 1),   # moyenne 4 min
    LineState.REPAIR: (18, 5),      # moyenne 18 min
}

def generate_duration(state):
    if state not in STATE_DURATION:
        return 0
    mean, std = STATE_DURATION[state]
    return max(1, int(random.gauss(mean, std)))