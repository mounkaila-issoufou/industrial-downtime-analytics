from collections import defaultdict
import random
from datetime import datetime, date, timedelta

from sqlalchemy import events

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
    generate_duration, get_dynamic_matrix
)
from industrial_downtime.ingestion.events.production_event_generator import generate_production_events
from industrial_downtime.ingestion.quality.quality_generator import generate_quality_for_hour
from industrial_downtime.ingestion.production.kpi_calculator import compute_kpis

def simulate_hour(line_config, hour_index, shift_type, shift_date, rng):
    state = LineState.RUNNING
    minutes_remaining = 60
    stop_budget = 60  # ← budget dédié aux stops
    events = []

    if 5 <= hour_index <= 8:
        failure_boost = 1.3
    elif 12 <= hour_index <= 13:
        failure_boost = 1.1
    elif 0 <= hour_index <= 4:
        failure_boost = 1.2
    else:
        failure_boost = 1.0

    while minutes_remaining > 0:
        matrix = get_dynamic_matrix(line_config, hour_index, shift_type)
        state = next_state(state, matrix)

        if state == LineState.RUNNING:
            minutes_remaining -= 1
            continue

        # Plus de budget stop → on court-circuite le reste en RUNNING
        if stop_budget <= 0:
            minutes_remaining -= 1
            continue

        duration = generate_duration(state)
        duration = max(1, int(duration * rng.uniform(0.8, 1.3) * failure_boost))

        # Double clamp : respecte le temps restant ET le budget stop
        duration = min(duration, minutes_remaining, stop_budget)

        minutes_remaining -= duration
        stop_budget -= duration  # ← décrémenter le budget

        events.append((state, duration))

    # Invariant garanti ici
    assert sum(d for _, d in events) <= 60, "stop budget violated"
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
# PRODUCTION GENERATION
# =========================


def generate_production():
    hourly_production = []
    production_events = []
    quality_inspections = []
    quality_events = []

    for shift in context.shifts:

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
        inspector_id = operator_id

        shift_start = datetime.combine(shift_date, shift_config.start)

        performance_factor = random.uniform(0.9, 1.0)  # 🎯 variation initiale

        for h in range(shift_config.hours):
            rng = random.Random(f"{shift_date}-{h}-{shift_type}-{line_id}")

            hour_timestamp = shift_start + timedelta(hours=h)
            hour_index = hour_timestamp.hour

            prod_id = generate_id("HP")

            # ======================
            # 🔥 SIMULATION CORRIGÉE
            # ======================
            events = simulate_hour(
                line_config,
                hour_index,
                shift_type,
                shift_date,
                rng,
            )

            micro_stop_minutes = sum(
                d for state, d in events if state == LineState.MICRO_STOP
            )

            failure_minutes = sum(
                d for state, d in events if state == LineState.FAILURE
            )

            # 🎯 dérive progressive réaliste
            performance_factor -= micro_stop_minutes * 0.001
            performance_factor -= failure_minutes * 0.003

            # bruit naturel
            performance_factor *= rng.uniform(0.97, 1.03)
            performance_factor = max(0.7, min(1.05, performance_factor))

            non_production_minutes = int(sum(d for _, d in events))

            productive_minutes = max(0, 60 - non_production_minutes)

            actual_production = int(
                productive_minutes * units_per_minute * performance_factor
            )

            # ======================
            # KPI
            # ======================
            kpis = compute_kpis(
                actual_production=actual_production,
                theoretical_production=theoretical_production,
                reliability_target=reliability_target,
                non_production_minutes=non_production_minutes,
            )

            # ======================
            # FACT
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
                    #"hour_timestamp": hour_timestamp,
                    "theoretical_production": theoretical_production,
                    "actual_production": actual_production,
                    "reliability_target": reliability_target,
                    "non_production_minutes": non_production_minutes,
                    **kpis,
                }
            )

            # ======================
            # EVENTS
            # ======================
            prod_events = generate_production_events(prod_id, events, rng)
            production_events.extend(prod_events)



            # ======================
            # QUALITY
            # ======================
            inspections, defects = generate_quality_for_hour(
                prod_id,
                actual_production
            )

            # 🎯 bruit qualité réaliste
            for d in defects:
                d["defective_units"] = int(
                    d["defective_units"] * random.uniform(0.7, 1.3)
                )

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

            # ======================
            # VÉRIFICATION FINALE
            # ======================

            duration_by_hour = defaultdict(int)
            for e in production_events:
                duration_by_hour[e["hourly_prod_id"]] += e["duration_minutes"]


            violations = {
                hid: total
                for hid, total in duration_by_hour.items()
                if total > 60
            }

            if violations:
                raise ValueError(
                    f"❌ {len(violations)} hourly_prod_id(s) dépassent 60 min :\n"
                    + "\n".join(f"  {hid}: {total} min" for hid, total in violations.items())
                )
            for hid, total in violations.items():
                print(f"⚠️  {hid}: {total} min > 60")


            for e in production_events:
                assert e["duration_minutes"] == e["end_minute"] - e["start_minute"], (
                    f"Incohérence start/end sur {e['event_id']}"
                )
                assert e["end_minute"] <= 60, (
                    f"end_minute={e['end_minute']} > 60 sur {e['event_id']}"
    )

            assert non_production_minutes <= 60
            assert sum(e["duration_minutes"] for e in prod_events) <= 60
    return (
        hourly_production,
        production_events,
        quality_inspections,
        quality_events,
    )