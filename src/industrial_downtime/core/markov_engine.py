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
    LineState.FAILURE: (12, 4),
    LineState.REPAIR: (18, 5),
    LineState.QUALITY: (6, 2),
    LineState.ORGANIZATION: (8, 3),
    LineState.HUMAN: (5, 2),
    LineState.CHANGEOVER: (10, 3),
    LineState.PLANNED_STOP: (10, 5),
    LineState.MAINTENANCE: (20, 6),
}

# =========================
# TRANSITION
# =========================

def get_dynamic_matrix(line_config, hour_index, shift_type):
    base = line_config.transition_matrix

    # deep copy safe
    matrix = {
        state: transitions.copy()
        for state, transitions in base.items()
    }

    robustness = line_config.robustness

    def safe_mul(state, target, factor):
        if state in matrix and target in matrix[state]:
            matrix[state][target] *= factor

    # =========================
    # PATTERNS INDUSTRIELS
    # =========================

    # 🔥 démarrage
    if 5 <= hour_index <= 8:
        safe_mul(LineState.RUNNING, LineState.FAILURE, 1.3 - robustness)

    # 🌙 nuit
    elif 0 <= hour_index <= 4:
        safe_mul(LineState.RUNNING, LineState.MICRO_STOP, 1.2 - robustness)

    # 🍽 fatigue
    elif 12 <= hour_index <= 13 or 18 <= hour_index <= 19:
        safe_mul(LineState.RUNNING, LineState.MICRO_STOP, 1.3)

    # =========================
    # NORMALISATION SAFE
    # =========================

    for state, transitions in matrix.items():
        total = sum(transitions.values())

        if total <= 0:
            continue

        for k in transitions:
            transitions[k] /= total

    return matrix


def next_state(current_state, transition_matrix):
    """
    Retourne l'état suivant selon la matrice de transition.
    """
    transitions = transition_matrix[current_state]

    if not transitions:
        return current_state  # fallback safe

    states = list(transitions.keys())
    probs = list(transitions.values())

    return random.choices(states, weights=probs, k=1)[0]


def generate_duration(state):
    """
    Génère une durée réaliste pour un état donné
    """
    if state not in STATE_DURATION:
        return 0

    mean, std = STATE_DURATION[state]

    return max(1, int(random.gauss(mean, std)))