import random
from enum import Enum


class LineState(Enum):
    RUNNING = "running"

    # existants
    MICRO_STOP = "micro_stop"
    FAILURE = "failure"
    REPAIR = "repair"

    # 🔥 nouveaux (non cassants)
    QUALITY = "quality"
    HUMAN = "human"
    ORGANIZATION = "organization"
    CHANGEOVER = "changeover"
    PLANNED_STOP = "planned_stop"
    MAINTENANCE = "maintenance"


# =========================
# DURÉES PAR ÉTAT
# =========================

STATE_DURATION = {
    LineState.MICRO_STOP: (4, 1),
    LineState.FAILURE: (12, 4),         # 🔥 NEW (avant implicite)
    LineState.REPAIR: (18, 5),

    # 🔥 nouveaux états
    LineState.QUALITY: (6, 2),
    LineState.HUMAN: (5, 2),
    LineState.ORGANIZATION: (10, 3),
    LineState.CHANGEOVER: (25, 8),
    LineState.PLANNED_STOP: (15, 5),
    LineState.MAINTENANCE: (30, 10),
}


# =========================
# TRANSITION
# =========================

def next_state(current_state, transition_matrix):
    transitions = transition_matrix[current_state]
    states = list(transitions.keys())
    probs = list(transitions.values())
    return random.choices(states, weights=probs)[0]


# =========================
# DURÉE
# =========================

def generate_duration(state):
    if state not in STATE_DURATION:
        return 0
    mean, std = STATE_DURATION[state]
    return max(1, int(random.gauss(mean, std)))