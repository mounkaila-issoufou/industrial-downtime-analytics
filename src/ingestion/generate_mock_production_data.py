import random
from datetime import datetime, date
from typing import List, Dict

from src.core.ids import generate_id
from src.core.context_store import context
from src.config.constants import PAUSE_RULES, EVENT_TYPES


# ----------------------------------------------------------
# Helpers
# ----------------------------------------------------------

def is_break_day(shift_date) -> bool:
    """
    Alternating daily break (1 day out of 2).
    Accepts datetime.date or YYYY-MM-DD string.
    """
    if isinstance(shift_date, str):
        date_obj = datetime.strptime(shift_date, "%Y-%m-%d").date()
    elif isinstance(shift_date, date):
        date_obj = shift_date
    else:
        raise TypeError(
            f"shift_date must be str or date, got {type(shift_date)}"
        )

    return date_obj.toordinal() % 2 == 0


def _add_event(events: list, **kwargs) -> None:
    """Centralise la création d’événement pour éviter la duplication."""
    events.append({
        "event_id": generate_id("EV"),
        **kwargs,
    })


# ----------------------------------------------------------
# Génération des événements
# ----------------------------------------------------------

def generate_events_for_hour(
    prod_id: str,
    shift_type: str,
    is_break_day: bool,
    total_downtime: int
) -> List[Dict]:

    events = []
    remaining = total_downtime

    # --- Planned pauses ---
    for pause in PAUSE_RULES.get(shift_type, []):
        if remaining <= 0:
            break

        duration = min(pause["duration"], remaining)
        remaining -= duration

        _add_event(
            events,
            hourly_prod_id=prod_id,
            event_type="operator_break",
            event_category="planned",
            duration_minutes=duration,
            comment=f"Scheduled pause at {pause['time']}"
        )

    # --- Alternating short break ---
    if is_break_day and remaining > 0:
        duration = min(10, remaining)
        remaining -= duration

        _add_event(
            events,
            hourly_prod_id=prod_id,
            event_type="short_break",
            event_category="planned",
            duration_minutes=duration,
            comment="Alternating daily break"
        )

    # --- Technical downtime ---
    while remaining > 0:
        if remaining <= 3:
            duration = remaining
        else:
            duration = random.randint(3, min(remaining, 20))

        remaining -= duration

        _add_event(
            events,
            hourly_prod_id=prod_id,
            event_type=random.choice(EVENT_TYPES),
            event_category="technical",
            duration_minutes=duration,
            comment="Operator intervention on machine element"
        )

    return events


# ----------------------------------------------------------
# Génération horaire
# ----------------------------------------------------------

def _compute_downtime_from_production(actual_prod: int, capacity: int = 4800) -> int:
    """
    Règle métier explicite pour dériver le downtime.
    """
    return max(0, int((capacity - actual_prod) / 80))


def generate_production():
    hourly_production = []
    production_events = []

    for shift in context.shifts:

        shift_id = shift["shift_supervision_id"]
        shift_date = shift["date"]
        shift_type = shift["session"]

        break_day = is_break_day(shift_date)

        # Récupération propre de l’opérateur affecté
        assignment = next(
            a for a in context.operator_assignments
            if a["shift_supervision_id"] == shift_id
        )
        operator_id = assignment["operator_id"]

        # --- 8 heures par shift ---
        for hour_index in range(8):

            prod_id = generate_id("HP")

            actual_prod = random.randint(1500, 4200)
            total_downtime = _compute_downtime_from_production(actual_prod)

            hourly_production.append({
                "hourly_prod_id": prod_id,
                "date": shift_date,
                "session": shift_type,
                "shift_supervision_id": shift_id,
                "operator_id": operator_id,
                "team_lead_id": shift["team_lead_id"],
                "line_id": shift["line_id"],
                "hour_index": hour_index,
                "actual_production": actual_prod,
                "non_production_minutes": total_downtime,
            })

            production_events.extend(
                generate_events_for_hour(
                    prod_id=prod_id,
                    shift_type=shift_type,
                    is_break_day=break_day,
                    total_downtime=total_downtime,
                )
            )

    return hourly_production, production_events
