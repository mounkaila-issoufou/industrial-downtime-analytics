from dataclasses import dataclass
from typing import List, Dict, Optional
import random

from industrial_downtime.core.markov_engine import LineState
from industrial_downtime.config.workshops import LineConfig
from industrial_downtime.config.shifts import Shift
from industrial_downtime.config.event_catalog import (
    EVENT_CATALOG,
    EventFamily,
    MICRO_STOP_FAMILIES,
    FAILURE_FAMILIES,
    QUALITY_FAMILIES,
    ORGANIZATIONAL_FAMILIES,
    HUMAN_FAMILIES,
    CHANGEOVER_FAMILIES,
    MAINTENANCE_FAMILIES,
)
from industrial_downtime.core.resolver.calibration import calibrator
from industrial_downtime.core.mechanisms.mechanism_resolver import (
    resolve_mechanism,
    MechanismContext,
)

ENABLE_CALIBRATION = True


# =========================
# CONTEXT
# =========================
@dataclass(frozen=True)
class ResolutionContext:
    state: LineState
    line: LineConfig
    shift: Shift
    repetition_count: int = 1
    scenario: Optional[str] = None


# =========================
# OUTPUT
# =========================
@dataclass(frozen=True)
class ResolvedEvent:
    event_key: str
    source: str
    confidence: float = 0.5


# =========================
# INTERNAL HELPERS
# =========================
def _apply_mechanism_rules(weight: float, e, mechanism) -> float:
    """
    Ajuste le poids en fonction du mécanisme causal
    """

    if not mechanism:
        return weight

    mech = mechanism.value

    # 🎯 matching direct (ex: micro_jam → "jam")
    if mech in e.event:
        weight *= 1.3

    # 🎯 règles métier (propagation causale)
    if mech == "wear" and e.family == EventFamily.MECHANICAL:
        weight *= 1.25

    if mech == "micro_jam" and "jam" in e.event:
        weight *= 1.4

    if mech == "fatigue" and e.family == EventFamily.HUMAN_ACTION:
        weight *= 1.5

    if mech == "drift" and e.family == EventFamily.PROCESS_DRIFT:
        weight *= 1.3

    return weight


# =========================
# RESOLVER V4
# =========================
def resolve_event(ctx: ResolutionContext) -> ResolvedEvent:

    r = ctx.line.robustness
    is_night = ctx.shift.name.value == "NUIT"
    rep = ctx.repetition_count

    # =========================
    # 0. MECHANISM (NEW 🔥)
    # =========================
    mech_ctx = MechanismContext(
        state=ctx.state,
        line=ctx.line,
        shift=ctx.shift,
        repetition_count=rep,
    )

    mechanism = resolve_mechanism(mech_ctx)

    # =========================
    # 1. MAP STATE → FAMILIES
    # =========================
    if ctx.state == LineState.MICRO_STOP:
        families = MICRO_STOP_FAMILIES
    elif ctx.state == LineState.FAILURE:
        families = FAILURE_FAMILIES
    elif ctx.state == LineState.QUALITY:
        families = QUALITY_FAMILIES
    elif ctx.state == LineState.ORGANIZATION:
        families = ORGANIZATIONAL_FAMILIES
    elif ctx.state == LineState.HUMAN:
        families = HUMAN_FAMILIES
    elif ctx.state == LineState.CHANGEOVER:
        families = CHANGEOVER_FAMILIES
    elif ctx.state == LineState.MAINTENANCE:
        families = MAINTENANCE_FAMILIES
    else:
        families = None

    # =========================
    # 2. FILTER CANDIDATES
    # =========================
    candidates = [
        e for e in EVENT_CATALOG.values()
        if families is None or e.family in families
    ]

    if not candidates:
        return ResolvedEvent(
            event_key="unknown_stop",
            source="resolver_empty",
            confidence=0.1,
        )

    # =========================
    # 3. WEIGHTING ENGINE
    # =========================
    scores: Dict[str, float] = {}

    for e in candidates:
        weight = e.base_probability

        # -------------------------
        # Robustness impact
        # -------------------------
        if r < 0.5 and e.family in (
            EventFamily.MECHANICAL,
            EventFamily.CONVEYOR,
        ):
            weight *= 1.3

        # -------------------------
        # Night shift impact
        # -------------------------
        if is_night and e.family == EventFamily.HUMAN_ACTION:
            weight *= 1.5

        # -------------------------
        # Repetition impact
        # -------------------------
        if rep >= 3:
            if e.family == EventFamily.MECHANICAL:
                weight *= 1.25
            elif e.family == EventFamily.PROCESS_DRIFT:
                weight *= 1.15

        # -------------------------
        # 🔥 MECHANISM IMPACT (FIXED)
        # -------------------------
        weight = _apply_mechanism_rules(weight, e, mechanism)

        # -------------------------
        # Noise (réalisme)
        # -------------------------
        weight *= random.uniform(0.9, 1.1)

        scores[e.event] = weight
        print(f"[MECH] {mechanism.value} → {e.event} (fam: {e.family.value}) : weight={weight:.3f}")
    # =========================
    # 4. CALIBRATION (CONTEXTUAL)
    # =========================
    if ENABLE_CALIBRATION:
        scores = calibrator.calibrate(
            scores,
            line=ctx.line.code,                 # ✅ FIX
            shift=ctx.shift.name.value,
            scenario=ctx.scenario,
        )

    # =========================
    # 5. WEIGHTED RANDOM PICK
    # =========================
    total_weight = sum(scores.values())

    if total_weight <= 0:
        return ResolvedEvent(
            event_key="unknown_stop",
            source="resolver_zero_weight",
            confidence=0.1,
        )

    pick = random.uniform(0, total_weight)

    cumulative = 0.0
    selected_event = None
    selected_weight = 0.0

    for event_key, weight in scores.items():
        cumulative += weight
        if pick <= cumulative:
            selected_event = event_key
            selected_weight = weight
            break

    # =========================
    # 6. FALLBACK SAFE
    # =========================
    if not selected_event:
        selected_event = list(scores.keys())[-1]
        selected_weight = scores[selected_event]

    # =========================
    # 7. UPDATE CALIBRATOR
    # =========================
    if ENABLE_CALIBRATION:
        calibrator.update(selected_event)

    # =========================
    # 8. CONFIDENCE
    # =========================
    confidence = min(1.0, max(0.1, selected_weight / total_weight * 3))

    return ResolvedEvent(
        event_key=selected_event,
        source="resolver_v4_mechanism_calibrated",
        confidence=confidence,
    )