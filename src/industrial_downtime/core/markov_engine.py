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
    LineState.FAILURE:    (12, 4),  # ← ajouter
    LineState.REPAIR:     (18, 5),
    LineState.QUALITY:    (6, 2),
    LineState.ORGANIZATION: (8, 3),
    LineState.HUMAN:      (5, 2),
    LineState.CHANGEOVER: (3, 8),
    LineState.PLANNED_STOP: (10, 5),
    LineState.MAINTENANCE: (20, 6),
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




def get_dynamic_matrix(line_config, hour_index, shift_type):
    base = line_config.transition_matrix

    # copie pour modification
    matrix = {s: probs.copy() for s, probs in base.items()}

    # 🎯 facteur robustesse (machine)
    robustness = line_config.robustness

    # =========================
    # PATTERNS INDUSTRIELS
    # =========================

    # 🔥 démarrage (matin)
    if 5 <= hour_index <= 8:
        matrix[LineState.RUNNING][LineState.FAILURE] *= (1.3 - robustness)

    # 🌙 nuit
    elif 0 <= hour_index <= 4:
        matrix[LineState.RUNNING][LineState.MICRO_STOP] *= (1.2 - robustness)

    # 🍽 pause / fatigue
    elif 12 <= hour_index <= 13 or 18 <= hour_index <= 19:
        matrix[LineState.RUNNING][LineState.MICRO_STOP] *= 1.3

    # =========================
    # NORMALISATION
    # =========================
    for state, transitions in matrix.items():
        total = sum(transitions.values())
        for k in transitions:
            transitions[k] /= total

    return matrix