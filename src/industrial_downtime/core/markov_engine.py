import random
from enum import Enum

class LineState(Enum):
    RUNNING = "running"
    MICRO_STOP = "micro_stop"
    FAILURE = "failure"
    REPAIR = "repair"

STATE_DURATION = {
    LineState.MICRO_STOP: (4, 1),   # moyenne 4 min
    LineState.REPAIR: (18, 5),      # moyenne 18 min
}

def next_state(current_state, transition_matrix):
    transitions = transition_matrix[current_state]
    states = list(transitions.keys())
    probs = list(transitions.values())
    return random.choices(states, weights=probs)[0]

def generate_duration(state):
    if state not in STATE_DURATION:
        return 0
    mean, std = STATE_DURATION[state]
    return max(1, int(random.gauss(mean, std)))