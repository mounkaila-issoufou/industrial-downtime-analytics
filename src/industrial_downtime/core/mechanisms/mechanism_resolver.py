import random
from typing import Optional

from industrial_downtime.core.markov_engine import LineState
from industrial_downtime.config.workshops import LineConfig
from industrial_downtime.config.shifts import Shift

from industrial_downtime.core.mechanisms.mechanism_catalog import (
    Mechanism,
    STATE_MECHANISMS,
    MECHANISM_WEIGHTS,
)


# =========================
# CONTEXT (léger)
# =========================
class MechanismContext:
    def __init__(
        self,
        state: LineState,
        line: LineConfig,
        shift: Shift,
        repetition_count: int = 1,
    ):
        self.state = state
        self.line = line
        self.shift = shift
        self.repetition_count = repetition_count


# =========================
# RESOLVER
# =========================
def resolve_mechanism(ctx: MechanismContext) -> Mechanism:
    """
    Retourne un mécanisme causal en fonction :
    - du state
    - de la robustesse ligne
    - du shift
    - de la répétition
    """

    candidates = STATE_MECHANISMS.get(ctx.state)

    if not candidates:
        return Mechanism.UNKNOWN

    weights = []

    for mech in candidates:
        w = MECHANISM_WEIGHTS.get(mech, 1.0)

        # -------------------------
        # Robustness impact
        # -------------------------
        if ctx.line.robustness < 0.5:
            if mech in (
                Mechanism.WEAR,
                Mechanism.MISALIGNMENT,
                Mechanism.LUBRICATION_ISSUE,
            ):
                w *= 1.3

        # -------------------------
        # Night shift impact
        # -------------------------
        if ctx.shift.name.value == "NUIT":
            if mech in (Mechanism.FATIGUE, Mechanism.HUMAN_ERROR):
                w *= 1.4

        # -------------------------
        # Repetition impact
        # -------------------------
        if ctx.repetition_count >= 3:
            if mech in (
                Mechanism.WEAR,
                Mechanism.PROCESS_DRIFT,
            ):
                w *= 1.2

        # -------------------------
        # Noise (réalisme)
        # -------------------------
        w *= random.uniform(0.9, 1.1)

        weights.append(w)

    # =========================
    # RANDOM PICK
    # =========================
    total = sum(weights)

    if total <= 0:
        return Mechanism.UNKNOWN

    pick = random.uniform(0, total)
    cumulative = 0.0

    for mech, w in zip(candidates, weights):
        cumulative += w
        if pick <= cumulative:
            return mech

    return candidates[-1]