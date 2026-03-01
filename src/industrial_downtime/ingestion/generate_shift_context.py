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
    """
    Génère :
    - shift_supervision
    - shift_operator_assignment

    Règles :
    - rotation ateliers
    - ligne choisie dans l'atelier
    - rotation opérateurs
    - rotation team leads
    """

    op_idx = 0
    tl_idx = 0

    for i, shift in enumerate(iter_shifts()):
        shift_id = generate_id("SS")
        shift_enum = ShiftName(shift["session"])
        shift_config = SHIFTS[shift_enum]

        # --- Atelier ---
        workshop_id = _pick_rotating(WORKSHOP_IDS, i)

        # --- Ligne appartenant à l’atelier ---
        lines_for_workshop = WORKSHOP_MAP[workshop_id]
        line_id = _pick_rotating(lines_for_workshop, i)

        # --- RH rotation ---
        team_lead_id = _pick_rotating(TEAM_LEADS, tl_idx)
        operator_id = _pick_rotating(OPERATORS, op_idx)

        # =========================
        # SHIFT SUPERVISION
        # =========================

        context.shifts.append(
            {
                "shift_supervision_id": shift_id,
                "date": shift["date"],
                "session": shift_enum.value,  # toujours string pour compatibilité
                "factory_id": FACTORY_ID,
                "workshop_id": workshop_id,
                "line_id": line_id,
                "team_lead_id": team_lead_id,
                "start_time": shift_config.start,
                "end_time": shift_config.end,
            }
        )

        context.operator_assignments.append(
            {
                "shift_operator_assignment_id": generate_id("SOA"),
                "shift_supervision_id": shift_id,
                "operator_id": operator_id,
                "line_id": line_id,
                "date": shift["date"],
                "session": shift_enum.value,
            }
        )

        op_idx += 1
        tl_idx += 1
