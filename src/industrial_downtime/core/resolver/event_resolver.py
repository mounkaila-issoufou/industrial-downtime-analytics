from dataclasses import dataclass
from typing import Dict, Tuple

from industrial_downtime.core.markov_engine import LineState
from industrial_downtime.config.workshops import LineConfig
from industrial_downtime.config.shifts import Shift
from industrial_downtime.config.event_catalog import EVENT_CATALOG


# =========================
# CONTEXT
# =========================
@dataclass(frozen=True)
class ResolutionContext:
    state: LineState
    line: LineConfig
    shift: Shift
    repetition_count: int = 1


# =========================
# OUTPUT
# =========================
@dataclass(frozen=True)
class ResolvedEvent:
    event_key: str
    source: str
    confidence: float


# =========================
# SCORING ENGINE V3
# =========================
def resolve_event(ctx: ResolutionContext) -> ResolvedEvent:
    """
    V3:
    - système de scoring multi-facteurs
    - plus de logique if/else métier lourde
    - extensible (MES-like design)
    """

    r = ctx.line.robustness
    is_night = ctx.shift.name.value == "NUIT"
    rep = ctx.repetition_count

    # =========================
    # SCORE MAP INITIALIZATION
    # =========================
    scores: Dict[str, float] = {}

    def add(event: str, value: float):
        scores[event] = scores.get(event, 0.0) + value

    # =========================
    # BASE SCORES BY STATE
    # =========================


    if ctx.repetition_count >= 3:
        # forcer une panne mécanique (exemple simple)
        return ResolvedEvent(
            event_key="stacker_jam",
            source="resolver_rule_repetition_escalation"
        )
    if ctx.state == LineState.FAILURE:
        add("standard_machine_failure", 0.6)
        add("critical_machine_failure", 0.4 * (1 - r))

    elif ctx.state == LineState.MICRO_STOP:
        add("micro_stop_generic", 0.5)
        add("micro_stop_operator_latency", 0.3 if is_night else 0.1)

    elif ctx.state == LineState.QUALITY:
        add("quality_check_adjustment", 0.4)
        add("quality_deviation_process", 0.4 * (1 - r))

    elif ctx.state == LineState.HUMAN:
        add("human_intervention", 0.4)
        add("operator_fatigue_error", 0.4 if is_night else 0.1)

    elif ctx.state == LineState.ORGANIZATION:
        add("planning_delay", 0.7)

    elif ctx.state == LineState.CHANGEOVER:
        add("standard_changeover", 0.5)
        add("long_changeover_issue", 0.3 * (1 - r))

    elif ctx.state == LineState.MAINTENANCE:
        add("standard_maintenance", 0.5)
        add("preventive_maintenance_delay", 0.3 * (1 - r))

    else:
        add("unknown_stop", 1.0)

    # =========================
    # CROSS FACTORS
    # =========================

    # Robustness penalty (fragile lines = more critical events)
    if r < 0.5:
        add("critical_machine_failure", 0.2)

    # Night shift penalty (fatigue)
    if is_night:
        add("operator_fatigue_error", 0.2)

    # Repetition escalation
    if rep >= 3:
        add("recurrent_micro_stop", 0.3)
        add("systemic_issue_detected", 0.2)

    # =========================
    # PICK BEST EVENT
    # =========================
    best_event, best_score = max(scores.items(), key=lambda x: x[1])

    # =========================
    # VALIDATION CATALOG
    # =========================
    if best_event not in EVENT_CATALOG:
        best_event = "unknown_stop"
        best_score = 0.3

    # =========================
    # CONFIDENCE NORMALIZATION
    # =========================
    confidence = min(1.0, max(0.1, best_score))

    return ResolvedEvent(
        event_key=best_event,
        source="resolver_v3_scoring",
        confidence=confidence,
    )