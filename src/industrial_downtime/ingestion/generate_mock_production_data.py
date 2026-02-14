import random
from datetime import datetime, date

from industrial_downtime.core.ids import generate_id
from industrial_downtime.core.context_store import context
from industrial_downtime.config.constants import (
    PAUSE_RULES,
    EVENT_CLASSIFICATION,
)

# =========================
# CONSTANTES KPI
# =========================

THEORETICAL_PER_HOUR = 4800
UNITS_PER_MINUTE = 80


# =========================
# UTILITAIRE
# =========================

def is_break_day(shift_date) -> bool:
    """
    Alternating daily break (1 day out of 2).
    Accepte date ou string.
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


# =========================
# EVENT GENERATION
# =========================

def generate_events_for_hour(
    prod_id: str,
    shift_type: str,
    is_break_day: bool,
    total_downtime: int
) -> list[dict]:
    """
    Génère des événements expliquant le downtime horaire.
    """

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
            "duration_minutes": duration,
            "comment": "Alternating daily break",
        })

    # --- Autres événements (technique, maintenance, etc.) ---
    event_types = list(EVENT_CLASSIFICATION.keys())

    while remaining > 0:

        event_type = random.choice(event_types)
        cause_family = EVENT_CLASSIFICATION[event_type]

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
            "cause_family": cause_family,
            "duration_minutes": duration,
            "comment": "Generated production event",
        })

    return events


# =========================
# PRODUCTION GENERATION
# =========================

def generate_production():
    """
    Génère :
    - hourly_production (avec KPI core + dérivés)
    - production_events (avec cause_family)
    """

    hourly_production = []
    production_events = []

    for shift in context.shifts:

        shift_id = shift["shift_supervision_id"]
        shift_date = shift["date"]
        shift_type = shift["session"]
        team_lead_id = shift["team_lead_id"]
        workshop_id = shift["workshop_id"]
        line_id = shift["line_id"]

        break_day = is_break_day(shift_date)

        # Récupérer opérateur affecté
        assignment = next(
            a for a in context.operator_assignments
            if a["shift_supervision_id"] == shift_id
        )
        operator_id = assignment["operator_id"]

        # 8 heures par shift
        for hour_index in range(8):

            prod_id = generate_id("HP")

            # ---- 1 heure parfaite garantie par shift ----
            if hour_index == 0:
                actual_production = THEORETICAL_PER_HOUR
                non_production_minutes = 0
            else:
                actual_production = random.randint(
                    3500,
                    THEORETICAL_PER_HOUR
                )
                non_production_minutes = max(
                    0,
                    int(
                        (THEORETICAL_PER_HOUR - actual_production)
                        / UNITS_PER_MINUTE
                    ),
                )

            # ======================
            # KPI CORE
            # ======================

            theoretical_production = THEORETICAL_PER_HOUR

            # Répartition pertes
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

            explained_ratio = (
                explained_minutes / non_production_minutes
                if non_production_minutes > 0 else 0
            )

            unexplained_ratio = (
                unexplained_minutes / non_production_minutes
                if non_production_minutes > 0 else 0
            )

            # ======================
            # ENREGISTREMENT PROD
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

                # KPI core
                "theoretical_production": theoretical_production,
                "actual_production": actual_production,

                # pertes
                "non_production_minutes": non_production_minutes,
                "explained_minutes": explained_minutes,
                "unexplained_minutes": unexplained_minutes,

                # KPI dérivés
                "reliability_rate": reliability_rate,
                "explained_ratio": explained_ratio,
                "unexplained_ratio": unexplained_ratio,
            })

            # ======================
            # GÉNÉRATION ÉVÉNEMENTS
            # ======================

            production_events.extend(
                generate_events_for_hour(
                    prod_id=prod_id,
                    shift_type=shift_type,
                    is_break_day=break_day,
                    total_downtime=non_production_minutes,
                )
            )

    return hourly_production, production_events
