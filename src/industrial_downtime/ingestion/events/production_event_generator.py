from industrial_downtime.core.ids import generate_id
from industrial_downtime.config.event_catalog import (
    EVENT_CATALOG,
    pick_root_cause,
    MICRO_STOP_CATEGORIES,
    FAILURE_CATEGORIES,
)
from industrial_downtime.core.markov_engine import LineState


def generate_production_events(hourly_prod_id: str, events: list) -> list[dict]:
    """
    Transforme les états Markov en événements métier exploitables.

    Args:
        hourly_prod_id: ID de la production horaire
        events: liste de tuples (state, duration)

    Returns:
        Liste de production_events
    """

    production_events = []

    for state, duration in events:

        # 🟢 On ignore les périodes normales
        if state == LineState.RUNNING:
            continue

        # 🔴 Mapping état → type d’événement
        if state == LineState.MICRO_STOP:
            event_key = pick_root_cause(MICRO_STOP_CATEGORIES)

        elif state == LineState.FAILURE:
            event_key = pick_root_cause(FAILURE_CATEGORIES)

        else:
            continue

        event_def = EVENT_CATALOG[event_key]

        production_events.append(
            {
                "event_id": generate_id("EV"),
                "hourly_prod_id": hourly_prod_id,
                "event_type": event_key,
                "cause_family": event_def.category,
                "organ": event_def.organ,
                "element": event_def.element,
                "operator_action": event_def.operator_action,
                "duration_minutes": duration,
                "comment": "Generated from Markov + root cause model",
            }
        )

    return production_events
