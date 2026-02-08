from src.core.context_store import context
from src.core.ids import generate_id
from src.core.calendar import iter_shifts
from src.config.settings import FACTORY_ID, WORKSHOP_ID, LINE_ID, OPERATORS, TEAM_LEADS


def _next_cyclic(items: list, index: int):
    """Helper simple pour rotation propre sur une liste."""
    return items[index % len(items)]


def build_shift_supervision(shift: dict, team_lead_id: str) -> dict:
    """Factory pure pour une ligne shift_supervision."""
    shift_id = generate_id("SS")

    return {
        "shift_supervision_id": shift_id,
        "date": shift["date"],
        "session": shift["session"],
        "factory_id": FACTORY_ID,
        "workshop_id": WORKSHOP_ID,
        "line_id": LINE_ID,
        "team_lead_id": team_lead_id,
        "start_time": shift["start_time"],
        "end_time": shift["end_time"],
    }


def build_operator_assignment(shift_id: str, shift: dict, operator_id: str) -> dict:
    """Factory pure pour une affectation opérateur."""
    return {
        "shift_operator_assignment_id": generate_id("SOA"),
        "shift_supervision_id": shift_id,
        "operator_id": operator_id,
        "line_id": LINE_ID,
        "date": shift["date"],
        "session": shift["session"],
    }


def generate_shift_context() -> None:
    """
    Peuple context.shifts et context.operator_assignments
    à partir du calendrier des shifts.
    """

    op_idx, tl_idx = 0, 0

    for shift in iter_shifts():

        team_lead_id = _next_cyclic(TEAM_LEADS, tl_idx)
        operator_id = _next_cyclic(OPERATORS, op_idx)

        shift_row = build_shift_supervision(shift, team_lead_id)
        context.shifts.append(shift_row)

        assignment_row = build_operator_assignment(
            shift_id=shift_row["shift_supervision_id"],
            shift=shift,
            operator_id=operator_id,
        )
        context.operator_assignments.append(assignment_row)

        op_idx += 1
        tl_idx += 1
