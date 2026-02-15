import random
from datetime import datetime, date

from industrial_downtime.core.ids import generate_id
from industrial_downtime.core.context_store import context
from industrial_downtime.config.constants import (
    PAUSE_RULES
    )
from industrial_downtime.config.settings import (
    WORKSHOPS, 
    EVENT_CLASSIFICATION
    )


# =========================
# BUILD LINE CONFIG
# =========================

LINE_CONFIG = {}

for workshop in WORKSHOPS:
    LINE_CONFIG.update(workshop)


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

    # --- Pauses planifiées ---
    for pause in PAUSE_RULES.get(shift_type.lower(), []):
        if remaining <= 0:
            break

        duration = min(pause["duration"], remaining)
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
            "comment": f"Scheduled pause at {pause['time']}",
        })

    # --- Pause alternée ---
    if is_break_day and remaining > 0:
        duration = min(10, remaining)
        remaining -= duration

        events.append({
            "event_id": generate_id("EV"),
            "hourly_prod_id": prod_id,
            "event_type": "short_break",
            "cause_family": "planned",
            "organ": "human",
            "element": "break",
            "operator_action": "break",
            "duration_minutes": duration,
            "comment": "Alternating daily break",
        })

    # --- Autres événements ---
    event_types = list(EVENT_CLASSIFICATION.keys())

    while remaining > 0:

        event_type = random.choice(event_types)
        event_def = EVENT_CLASSIFICATION[event_type]

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
            "cause_family": event_def["event_category"],
            "organ": event_def["organ"],
            "element": event_def["element"],
            "operator_action": event_def["operator_action"],
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

        if line_id not in LINE_CONFIG:
            raise ValueError(f"Unknown line_id {line_id}")

        line_config = LINE_CONFIG[line_id]

        theoretical_production = line_config["THEORETICAL_CAPACITY_PER_HOUR"]
        units_per_minute = line_config["UNITS_PER_MINUTE"]
        reliability_target = line_config["RELIABILITY_TARGET"]

        break_day = is_break_day(shift_date)

        assignment = next(
            a for a in context.operator_assignments
            if a["shift_supervision_id"] == shift_id
        )
        operator_id = assignment["operator_id"]

        for hour_index in range(8):

            prod_id = generate_id("HP")

            # 1 heure parfaite garantie
            if hour_index == 0:
                actual_production = theoretical_production
                non_production_minutes = 0
            else:
                reliability_real = random.uniform(
                    reliability_target - 0.05,
                    reliability_target + 0.05
                )

                reliability_real = max(0.3, min(1.0, reliability_real))

                actual_production = int(
                    theoretical_production * reliability_real
                )

                non_production_minutes = max(
                    0,
                    int(
                        (theoretical_production - actual_production)
                        / units_per_minute
                    ),
                )

            # ======================
            # Répartition pertes
            # ======================

            if non_production_minutes > 0:
                explained_minutes = int(
                    non_production_minutes * random.uniform(0.6, 0.9)
                )
                unexplained_minutes = (
                    non_production_minutes - explained_minutes
                )
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

            production_events.extend(
                generate_events_for_hour(
                    prod_id=prod_id,
                    shift_type=shift_type,
                    is_break_day=break_day,
                    total_downtime=non_production_minutes,
                )
            )

    return hourly_production, production_events
