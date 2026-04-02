import random
from datetime import timedelta

from industrial_downtime.core.ids import generate_id
from industrial_downtime.config.event_catalog import (
    EVENT_CATALOG,
    pick_root_cause,
    MICRO_STOP_FAMILIES,
    FAILURE_FAMILIES,
    QUALITY_FAMILIES,
    ORGANIZATIONAL_FAMILIES,
    HUMAN_FAMILIES,
    CHANGEOVER_FAMILIES,
    PLANNED_FAMILIES,
    MAINTENANCE_FAMILIES
)
from industrial_downtime.core.markov_engine import LineState


def inject_external_events(current_time: int) -> list[dict]:
    extra_events = []

    if random.random() < 0.05:
        extra_events.append("short_break")

    if random.random() < 0.03:
        extra_events.append("material_shortage")

    return extra_events


def generate_production_events(hourly_prod_id: str, events: list, rng) -> list[dict]:
    """
    Génération d'événements enrichis (niveau industriel).
    GARANTIT : somme des durées <= 60 minutes
    """

    production_events = []
    current_time = 0  # timeline stricte

    last_event_type = None
    repetition_count = 0

    for state, duration in events:

        # =========================
        # SKIP RUNNING
        # =========================
        if state == LineState.RUNNING:
            current_time += duration
            if current_time >= 60:
                break
            continue

        # =========================
        # STOP HARD LIMIT
        # =========================
        if current_time >= 60:
            break

        # =========================
        # CLAMP DURATION (CRITIQUE)
        # =========================
        real_duration = min(duration, 60 - current_time)

        # Après (assertif, détecte les régressions) :
        assert duration <= (60 - current_time), (
            f"simulate_hour a envoyé une durée invalide : {duration} "
            f"alors que current_time={current_time}"
        )
        real_duration = duration
        if real_duration <= 0:
            break

        # =========================
        # ROOT CAUSE
        # =========================
        if state == LineState.MICRO_STOP:
            families = MICRO_STOP_FAMILIES
        elif state == LineState.FAILURE:
            families = FAILURE_FAMILIES
        elif state == LineState.QUALITY:
            families = QUALITY_FAMILIES
        elif state == LineState.ORGANIZATION:
            families = ORGANIZATIONAL_FAMILIES
        elif state == LineState.HUMAN:
            families = HUMAN_FAMILIES
        elif state == LineState.CHANGEOVER:
            families = CHANGEOVER_FAMILIES
        elif state == LineState.PLANNED_STOP:
            families = PLANNED_FAMILIES
        elif state == LineState.MAINTENANCE:
            families = MAINTENANCE_FAMILIES
        else:
            event_key = "unknown_stop"
            event_def = EVENT_CATALOG[event_key]
            families = None

        if families:
            event_key = pick_root_cause(families)
            event_def = EVENT_CATALOG[event_key]

        # =========================
        # SEVERITY
        # =========================
        if real_duration <= 3:
            severity = "minor"
            severity_score = 1
        elif real_duration <= 10:
            severity = "medium"
            severity_score = 2
        else:
            severity = "critical"
            severity_score = 3

        # =========================
        # BUSINESS IMPACT
        # =========================
        if event_def.family in FAILURE_FAMILIES:
            business_impact = "high"
        elif event_def.family in MICRO_STOP_FAMILIES:
            business_impact = "medium"
        elif event_def.family in QUALITY_FAMILIES:
            business_impact = "medium"
        elif event_def.family in ORGANIZATIONAL_FAMILIES:
            business_impact = "medium"
        elif event_def.family in HUMAN_FAMILIES:
            business_impact = "low"
        elif event_def.family in CHANGEOVER_FAMILIES:
            business_impact = "high"
        elif event_def.family in MAINTENANCE_FAMILIES:
            business_impact = "high"
        else:
            business_impact = "low"

        # =========================
        # ESCALATION
        # =========================
        if event_def.family in FAILURE_FAMILIES:
            escalation = "maintenance"
        elif event_def.family in HUMAN_FAMILIES:
            escalation = "team_lead"
        elif event_def.family in QUALITY_FAMILIES:
            escalation = "quality_team"
        elif event_def.family in ORGANIZATIONAL_FAMILIES:
            escalation = "planning"
        else:
            escalation = None

        # =========================
        # REPETITION TRACKING
        # =========================
        if event_key == last_event_type:
            repetition_count += 1
        else:
            repetition_count = 1

        last_event_type = event_key
        is_recurrent = repetition_count >= 3

        # =========================
        # TIMESTAMP (SAFE)
        # =========================
        start_minute = current_time
        end_minute = current_time + real_duration
        current_time = end_minute

        # =========================
        # BUILD EVENT
        # =========================
        production_events.append(
            {
                "event_id": generate_id("EV"),
                "hourly_prod_id": hourly_prod_id,
                "event_type": event_key,

                "cause_category": event_def.category.value,
                "cause_family": event_def.family.value,
                "organ": event_def.organ,
                "element": event_def.element,

                "start_minute": start_minute,
                "end_minute": end_minute,

                "duration_minutes": real_duration,
                "severity": severity,
                "severity_score": severity_score,
                "business_impact": business_impact,

                "operator_action": event_def.operator_action,
                "escalation": escalation,

                "is_recurrent": is_recurrent,
                "repetition_count": repetition_count,

                "source": "markov_simulation",
                "comment": f"{severity} {state.name.lower()} event",
            }
        )

    # =========================
    # FINAL SAFETY CHECK
    # =========================
    total = sum(e["duration_minutes"] for e in production_events)

    if total > 60:
        raise ValueError(f"❌ Total duration exceeded: {total}")

    if current_time > 60:
        raise ValueError(f"❌ Timeline overflow: {current_time}")

    return production_events