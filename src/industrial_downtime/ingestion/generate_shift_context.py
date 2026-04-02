from industrial_downtime.core.context_store import context
from industrial_downtime.core.ids import generate_id
from industrial_downtime.core.calendar import iter_shifts
from industrial_downtime.config.settings import (
    FACTORY_ID,
    OPERATORS,
    TEAM_LEADS,
)
from industrial_downtime.config.shifts import SHIFTS, ShiftName
from industrial_downtime.config.workshops import WORKSHOPS

# =========================
# STRUCTURE ATELIERS / LIGNES
# =========================

WORKSHOP_MAP = {
    workshop_id: list(workshop.lines.keys())
    for workshop_id, workshop in WORKSHOPS.items()
}

WORKSHOP_IDS = list(WORKSHOP_MAP.keys())


def _pick_rotating(values: list, index: int):
    return values[index % len(values)]

def generate_shift_context():
    context.shifts.clear()
    context.operator_assignments.clear()
    op_idx = 0
    tl_idx = 0

    for shift in iter_shifts():
        shift_enum = ShiftName(shift["session"])
        shift_config = SHIFTS[shift_enum]

        # ── Une supervision par ligne, pas par atelier rotatif ──
        for workshop_id, line_ids in WORKSHOP_MAP.items():
            for line_id in line_ids:

                shift_id = generate_id("SS")
                team_lead_id = _pick_rotating(TEAM_LEADS, tl_idx)
                operator_id  = _pick_rotating(OPERATORS, op_idx)

                context.shifts.append({
                    "shift_supervision_id": shift_id,
                    "date":       shift["date"],
                    "session":    shift_enum.value,
                    "factory_id": FACTORY_ID,
                    "workshop_id": workshop_id,
                    "line_id":    line_id,
                    "team_lead_id": team_lead_id,
                    "start_time": shift_config.start,
                    "end_time":   shift_config.end,
                })

                context.operator_assignments.append({
                    "shift_operator_assignment_id": generate_id("SOA"),
                    "shift_supervision_id": shift_id,
                    "operator_id": operator_id,
                    "line_id":     line_id,
                    "date":        shift["date"],
                    "session":     shift_enum.value,
                })

                op_idx += 1
                tl_idx += 1

        # Compter exactement ce que la boucle génère
        total = sum(
            len(line_ids)
            for line_ids in WORKSHOP_MAP.values()
        )
        shifts = list(iter_shifts())
        print(f"Lignes total      : {total}")          # doit être 10
        print(f"Shifts iter       : {len(shifts)}")    # doit être ~78
        print(f"Supervisions      : {total * len(shifts)}")  # doit être ~780
        print(f"Lignes par workshop:")
        for wid, lids in WORKSHOP_MAP.items():
            print(f"  {wid}: {len(lids)} lignes → {lids}")