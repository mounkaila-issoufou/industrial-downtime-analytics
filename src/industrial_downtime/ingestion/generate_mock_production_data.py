import random
from datetime import datetime, date

from industrial_downtime.config.event_catalog import (
    EVENT_CATALOG,
)
from industrial_downtime.core.ids import generate_id
from industrial_downtime.core.context_store import context
from industrial_downtime.config.shifts import SHIFTS, ShiftName
#from industrial_downtime.core.quality_engine import generate_quality_for_hour
from industrial_downtime.config.workshops import WORKSHOPS
from industrial_downtime.core.markov_engine import (
    LineState,
    next_state,
    generate_duration,
)
from industrial_downtime.ingestion.events.production_event_generator import generate_production_events
from industrial_downtime.ingestion.quality.quality_generator import generate_quality_for_hour
from industrial_downtime.ingestion.production.kpi_calculator import compute_kpis


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
        raise TypeError(f"shift_date must be str or date, got {type(shift_date)}")

    return date_obj.toordinal() % 2 == 0


# =========================
# EVENT GENERATION
# =========================


def generate_events_for_hour(
    prod_id: str, shift_type: str, is_break_day: bool, total_downtime: int
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

        events.append(
            {
                "event_id": generate_id("EV"),
                "hourly_prod_id": prod_id,
                "event_type": "operator_break",
                "cause_family": "planned",
                "organ": "human",
                "element": "break",
                "operator_action": "break",
                "duration_minutes": duration,
                "comment": f"Scheduled pause at {pause.start}",
            }
        )

    # --- Pause alternée ---
    if is_break_day and remaining > 0:
        duration = min(10, remaining)
        remaining -= duration

        event_def = EVENT_CATALOG["short_break"]

        events.append(
            {
                "event_id": generate_id("EV"),
                "hourly_prod_id": prod_id,
                "event_type": "short_break",
                "duration_minutes": duration,
                "comment": "Alternating daily break",
                "cause_family": event_def.category,
                "organ": event_def.organ,
                "element": event_def.element,
                "operator_action": event_def.operator_action,
            }
        )

    # --- Autres événements ---
    event_types = list(EVENT_CATALOG.keys())
    print(event_types)

    while remaining > 0:

        event_type = random.choices(
            event_types,
            weights=[EVENT_CATALOG[e].base_probability for e in event_types],
            k=1
        )[0]
        event_def = EVENT_CATALOG[event_type]

        duration = (
            remaining if remaining <= 3 else random.randint(3, min(remaining, 20))
        )

        remaining -= duration

        events.append(
            {
                "event_id": generate_id("EV"),
                "hourly_prod_id": prod_id,
                "event_type": event_type,
                "cause_family": event_def.category,
                "organ": event_def.organ,
                "element": event_def.element,
                "operator_action": event_def.operator_action,
                "duration_minutes": duration,
                "comment": "Generated production event",
            }
        )

    return events


# =========================
# PRODUCTION GENERATION
# =========================


def generate_production():
    hourly_production = []
    production_events = []
    quality_inspections = []
    quality_events = []

    for shift in context.shifts:
        performance_factor = 1.0

        shift_id = shift["shift_supervision_id"]
        shift_date = shift["date"]
        shift_type = shift["session"]
        team_lead_id = shift["team_lead_id"]
        workshop_id = shift["workshop_id"]
        line_id = shift["line_id"]

        shift_config = SHIFTS[ShiftName(shift_type)]
        workshop = WORKSHOPS[workshop_id]
        line_config = workshop.lines[line_id]

        theoretical_production = line_config.theoretical_capacity_per_hour
        reliability_target = line_config.reliability_target
        units_per_minute = line_config.units_per_minute
        assignment = next(
            a for a in context.operator_assignments
            if a["shift_supervision_id"] == shift_id
        )

        operator_id = assignment["operator_id"]
        # 👉 on peut distinguer opérateur / inspecteur si besoin
        inspector_id = operator_id  # simple pour l’instant
        for hour_index in range(int(shift_config.hours)):

            prod_id = generate_id("HP")

            # ======================
            # 1. SIMULATION
            # ======================
            if hour_index == 0:
                events = []
                
                # petit bruit réaliste
                noise = random.uniform(0.85, 1.0)

                actual_production = int(theoretical_production * noise)
                non_production_minutes = int(60 - (60*actual_production/theoretical_production))
            else:
                events = simulate_hour(line_config)
                micro_stop_minutes = sum(
                    duration for state, duration in events
                    if state == LineState.MICRO_STOP
                )

                failure_minutes = sum(
                    duration for state, duration in events
                    if state == LineState.FAILURE
                )
                performance_factor -= micro_stop_minutes * 0.0015
                performance_factor -= failure_minutes * 0.004

                # sécurité
                performance_factor = max(0.75, min(1.0, performance_factor))
                non_production_minutes = int(sum(d for _, d in events))
                productive_minutes = max(0, 60 - non_production_minutes)

                #actual_production = productive_minutes * line_config.units_per_minute
                actual_production = int(
                    productive_minutes * units_per_minute * performance_factor
                )
  
            # ======================
            # 2. KPI
            # ======================

            kpis = compute_kpis(
                actual_production=actual_production,
                theoretical_production=theoretical_production,
                reliability_target=reliability_target,
                non_production_minutes=int(non_production_minutes),
            )
            # ======================
            # 3. FACT TABLE
            # ======================
            hourly_production.append(
                {
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
                    # KPI injectés directement
                    **kpis,
                }
            )

            # ======================
            # 4. EVENTS
            # ======================
            prod_events = generate_production_events(prod_id, events)
            production_events.extend(prod_events)

            # ======================
            # 5. QUALITY
            # ======================
            inspections, defects = generate_quality_for_hour(
                prod_id,
                actual_production
            )

            # petit bruit défauts
            for d in defects:
                d["defective_units"] = int(
                    d["defective_units"] * random.uniform(0.8, 1.2)
                )

            # ======================
            # 6. QUALITY ENRICHMENT (🔥 IMPORTANT)
            # ======================
            for ins in inspections:
                ins.update({
                    "inspection_date": shift_date,
                    "session": shift_type,
                    "shift_supervision_id": shift_id,
                    "inspector_id": inspector_id,
                    "workshop_id": workshop_id,
                    "line_id": line_id,
                    "source_file_name": "mock_quality.csv",
                })



            quality_inspections.extend(inspections)
            quality_events.extend(defects)


    return (
        hourly_production,
        production_events,
        quality_inspections,
        quality_events,
    )
