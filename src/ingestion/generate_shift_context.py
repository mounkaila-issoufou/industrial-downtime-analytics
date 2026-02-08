from src.core.context_store import context
from src.core.ids import generate_id
from src.core.calendar import iter_shifts
from src.config.settings import (
    FACTORY_ID,
    WORKSHOPS,
    LINES,
    OPERATORS,
    TEAM_LEADS,
)


def _pick_rotating(values: list, index: int):
    """Helper déterministe pour alterner proprement."""
    return values[index % len(values)]


def generate_shift_context():
    """
    Génère :
    - shift_supervision
    - shift_operator_assignment

    Règles simples et lisibles :
    - rotation ateliers/lignes
    - rotation opérateurs
    - rotation team leads
    """

    op_idx = 0
    tl_idx = 0

    for i, shift in enumerate(iter_shifts()):

        shift_id = generate_id("SS")

        workshop_id = _pick_rotating(WORKSHOPS, i)
        line_id = _pick_rotating(LINES, i)
        team_lead_id = _pick_rotating(TEAM_LEADS, tl_idx)
        operator_id = _pick_rotating(OPERATORS, op_idx)

        # --- SHIFT SUPERVISION ---
        context.shifts.append({
            "shift_supervision_id": shift_id,
            "date": shift["date"],
            "session": shift["session"],
            "factory_id": FACTORY_ID,
            "workshop_id": workshop_id,
            "line_id": line_id,
            "team_lead_id": team_lead_id,
            "start_time": shift["start_time"],
            "end_time": shift["end_time"],
        })

        # --- AFFECTATION OPERATEUR ---
        context.operator_assignments.append({
            "shift_operator_assignment_id": generate_id("SOA"),
            "shift_supervision_id": shift_id,
            "operator_id": operator_id,
            "line_id": line_id,
            "date": shift["date"],
            "session": shift["session"],
        })

        op_idx += 1
        tl_idx += 1
