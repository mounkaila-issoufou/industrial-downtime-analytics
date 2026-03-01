import random
from datetime import datetime, date

from industrial_downtime.config.event_catalog import EVENT_CATALOG, EventCategory, pick_root_cause, MICRO_STOP_CATEGORIES, FAILURE_CATEGORIES
from industrial_downtime.core.ids import generate_id
from industrial_downtime.core.context_store import context
from industrial_downtime.config.shifts import SHIFTS, ShiftName
from industrial_downtime.config.workshops import WORKSHOPS
from industrial_downtime.core.markov_engine import (
    LineState,
    next_state,
    generate_duration
)


def simulate_hour(line_config, total_minutes=60):

    state = LineState.RUNNING
    minutes_remaining = total_minutes
    events = []

    while minutes_remaining > 0:

        state = next_state(state, line_config.transition_matrix)

        if state == LineState.RUNNING:
            minutes_remaining -= 1
            continue

        duration = generate_duration(state)

        duration = min(duration, minutes_remaining)
        minutes_remaining -= duration

        events.append((state, duration))

    return events




# =========================
# UTILITAIRE
# =========================

def is_break_day(shift_date) -> bool:
    if isinstance(shift_date, str):
        date_obj = datetime.strptime(shift_date, "%Y-%m-%d").date()
    elif isinstance(shift_date, date):
        date_obj = shift_date
    else:
        raise TypeError(
            f"shift_date must be str or date, got {type(shift_date)}"
        )

    return date_obj.toordinal() % 2 == 0


# =========================
# EVENT GENERATION
# =========================

def generate_events_for_hour(
    prod_id: str,
    shift_type: str,
    is_break_day: bool,
    total_downtime: int
) -> list[dict]:

    events = []
    remaining = total_downtime

    shift_enum = ShiftName(shift_type)
    shift_config = SHIFTS[shift_enum]

    # --- Pauses planifiées ---
    for pause in shift_config.breaks:
        if remaining <= 0:
            break

        duration = min(pause.duration_minutes, remaining)
        remaining -= duration

        events.append({
            "event_id": generate_id("EV"),
            "hourly_prod_id": prod_id,
            "event_type": "operator_break",
            "cause_family": "planned",
            "organ": "human",
            "element": "break",
            "operator_action": "break",
            "duration_minutes": duration,
            "comment": f"Scheduled pause at {pause.start}",
        })

    # --- Pause alternée ---
    if is_break_day and remaining > 0:

        duration = min(10, remaining)
        remaining -= duration

        event_def = EVENT_CATALOG["short_break"]

        events.append({
            "event_id": generate_id("EV"),
            "hourly_prod_id": prod_id,
            "event_type": "short_break",
            "duration_minutes": duration,
            "comment": "Alternating daily break",
            "cause_family": event_def.category,
            "organ": event_def.organ,
            "element": event_def.element,
            "operator_action": event_def.operator_action,
        })

    # --- Autres événements ---
    event_types = list(EVENT_CATALOG.keys())

    while remaining > 0:

        event_type = random.choice(event_types)
        event_def = EVENT_CATALOG[event_type]

        duration = (
            remaining
            if remaining <= 3
            else random.randint(3, min(remaining, 20))
        )

        remaining -= duration

        events.append({
            "event_id": generate_id("EV"),
            "hourly_prod_id": prod_id,
            "event_type": event_type,
            "cause_family": event_def.category,
            "organ": event_def.organ,
            "element": event_def.element,
            "operator_action": event_def.operator_action,
            "duration_minutes": duration,
            "comment": "Generated production event",
        })

    return events


# =========================
# PRODUCTION GENERATION
# =========================

def generate_production():

    hourly_production = []
    production_events = []

    for shift in context.shifts:

        shift_id = shift["shift_supervision_id"]
        shift_date = shift["date"]
        shift_type = shift["session"]
        team_lead_id = shift["team_lead_id"]
        workshop_id = shift["workshop_id"]
        line_id = shift["line_id"]

        # ======================
        # SHIFT CONFIG
        # ======================

        shift_enum = ShiftName(shift_type)
        shift_config = SHIFTS[shift_enum]

        # ======================
        # WORKSHOP / LINE
        # ======================

        if workshop_id not in WORKSHOPS:
            print(f"Unknown workshop_id {workshop_id}")
            raise ValueError(f"Unknown workshop_id {workshop_id}")

        workshop = WORKSHOPS[workshop_id]

        if line_id not in workshop.lines:
            raise ValueError(f"Unknown line_id {line_id}")

        line_config = workshop.lines[line_id]

        theoretical_production = line_config.theoretical_capacity_per_hour
        units_per_minute = line_config.units_per_minute
        reliability_target = line_config.reliability_target

        break_day = is_break_day(shift_date)

        assignment = next(
            a for a in context.operator_assignments
            if a["shift_supervision_id"] == shift_id
        )
        operator_id = assignment["operator_id"]


        for hour_index in range(int(shift_config.hours)):

            prod_id = generate_id("HP")

            # ======================
            # Simulation Markov
            # ======================

            if hour_index == 0:
                events = []
                actual_production = theoretical_production
                non_production_minutes = 0
            else:
                events = simulate_hour(line_config, total_minutes=60)

                non_production_minutes = sum(duration for _, duration in events)

                productive_minutes = 60 - non_production_minutes

                actual_production = productive_minutes * units_per_minute
            # ======================
            # Répartition pertes
            # ======================

            if non_production_minutes > 0:
                explained_minutes = non_production_minutes
                unexplained_minutes = 0
            else:
                explained_minutes = 0
                unexplained_minutes = 0

            # ======================
            # KPI DÉRIVÉS
            # ======================

            reliability_rate = (
                actual_production / theoretical_production
                if theoretical_production > 0 else 0
            )

            reliability_gap = reliability_rate - reliability_target

            explained_ratio = (
                explained_minutes / non_production_minutes
                if non_production_minutes > 0 else 0
            )

            unexplained_ratio = (
                unexplained_minutes / non_production_minutes
                if non_production_minutes > 0 else 0
            )

            # ======================
            # ENREGISTREMENT
            # ======================

            hourly_production.append({
                "hourly_prod_id": prod_id,
                "date": shift_date,
                "session": shift_type,
                "shift_supervision_id": shift_id,
                "operator_id": operator_id,
                "team_lead_id": team_lead_id,
                "workshop_id": workshop_id,
                "line_id": line_id,

                "hour_index": hour_index,

                # Capacités
                "theoretical_production": theoretical_production,
                "actual_production": actual_production,

                # Objectif
                "reliability_target": reliability_target,

                # Pertes
                "non_production_minutes": non_production_minutes,
                "explained_minutes": explained_minutes,
                "unexplained_minutes": unexplained_minutes,

                # KPI
                "reliability_rate": reliability_rate,
                "reliability_gap": reliability_gap,
                "explained_ratio": explained_ratio,
                "unexplained_ratio": unexplained_ratio,
            })

            for state, duration in events:

                if state == LineState.MICRO_STOP:
                    event_key = pick_root_cause(MICRO_STOP_CATEGORIES)

                elif state == LineState.FAILURE:
                    event_key = pick_root_cause(FAILURE_CATEGORIES)

                else:
                    continue

                event_def = EVENT_CATALOG[event_key]

                production_events.append({
                    "event_id": generate_id("EV"),
                    "hourly_prod_id": prod_id,
                    "event_type": event_key,
                    "cause_family": event_def.category,
                    "organ": event_def.organ,
                    "element": event_def.element,
                    "operator_action": event_def.operator_action,
                    "duration_minutes": duration,
                    "comment": "Generated from Markov + root cause model",
                })

    return hourly_production, production_events
