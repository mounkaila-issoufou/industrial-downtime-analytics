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

    # pause opérateur
    if random.random() < 0.05:
        extra_events.append("short_break")

    # problème supply
    if random.random() < 0.03:
        extra_events.append("material_shortage")

    return extra_events


def generate_production_events(hourly_prod_id: str, events: list) -> list[dict]:
    """
    Génération d'événements enrichis (niveau industriel).
    """

    production_events = []
    total_duration = 0
    current_time = 0  # minutes dans l'heure

    last_event_type = None
    repetition_count = 0

    for state, duration in events:

        if state == LineState.RUNNING:
            current_time += duration
            continue

        # =========================
        # 1. ROOT CAUSE (EXTENDED)
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
            current_time += duration
            continue


        event_key = pick_root_cause(families)
        event_def = EVENT_CATALOG[event_key]

        # =========================
        # 2. DURÉE RÉALISTE
        # =========================
        real_duration = max(
            1,
            int(random.gauss(event_def.mean_duration, event_def.duration_std))
        )

        real_duration = min(real_duration, duration)

        total_duration += real_duration

        # =========================
        # 3. SEVERITY (affinée)
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
        # 4. CRITICITÉ BUSINESS (🔥)
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
        # 5. ESCALATION
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
        # 6. DÉTECTION RÉPÉTITION (🔥 très utile ML)
        # =========================
        if event_key == last_event_type:
            repetition_count += 1
        else:
            repetition_count = 1

        last_event_type = event_key

        is_recurrent = repetition_count >= 3

        # =========================
        # 7. TIMESTAMP (🔥 indispensable)
        # =========================
        start_minute = current_time
        end_minute = current_time + real_duration

        current_time += real_duration

        # =========================
        # 8. BUILD EVENT (ULTRA ENRICHI)
        # =========================
        production_events.append(
            {
                "event_id": generate_id("EV"),
                "hourly_prod_id": hourly_prod_id,
                "event_type": event_key,

                # ======================
                # STRUCTURE ANALYTIQUE
                # ======================
                "cause_category": event_def.category.value,
                "cause_family": event_def.family.value,
                "organ": event_def.organ,
                "element": event_def.element,

                # ======================
                # TEMPOREL
                # ======================
                "start_minute": start_minute,
                "end_minute": end_minute,

                # ======================
                # KPI
                # ======================
                "duration_minutes": real_duration,
                "severity": severity,
                "severity_score": severity_score,
                "business_impact": business_impact,

                # ======================
                # OPERATIONNEL
                # ======================
                "operator_action": event_def.operator_action,
                "escalation": escalation,

                # ======================
                # SMART FEATURES 🔥
                # ======================
                "is_recurrent": is_recurrent,
                "repetition_count": repetition_count,

                # ======================
                # META
                # ======================
                "source": "markov_simulation",
                "comment": f"{severity} {state.name.lower()} event",
            }
        )

    # =========================
    # 9. NORMALISATION DURÉE
    # =========================
    if production_events:
        total = sum(e["duration_minutes"] for e in production_events)

        if total > 0:
            factor = sum(d for _, d in events) / total

            for e in production_events:
                e["duration_minutes"] = max(
                    1,
                    int(e["duration_minutes"] * factor)
                )

    return production_events


