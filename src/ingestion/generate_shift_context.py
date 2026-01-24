from src.core.context_store import context
from src.core.ids import generate_id
from src.core.calendar import iter_shifts
from src.config.settings import FACTORY_ID, WORKSHOP_ID, LINE_ID, OPERATORS, TEAM_LEADS

def generate_shift_context():
    op_idx, tl_idx = 0, 0

    for shift in iter_shifts():
        shift_id = generate_id("SS")
        team_lead_id = TEAM_LEADS[tl_idx % len(TEAM_LEADS)]
        operator_id = OPERATORS[op_idx % len(OPERATORS)]

        context.shifts.append({
            "shift_supervision_id": shift_id,
            "date": shift["date"],
            "session": shift["session"],
            "factory_id": FACTORY_ID,
            "workshop_id": WORKSHOP_ID,
            "line_id": LINE_ID,
            "team_lead_id": team_lead_id,
            "start_time": shift["start_time"],
            "end_time": shift["end_time"]
        })

        context.operator_assignments.append({
            "shift_operator_assignment_id": generate_id("SOA"),
            "shift_supervision_id": shift_id,
            "operator_id": operator_id,
            "date": shift["date"],
            "session": shift["session"]
        })

        op_idx += 1
        tl_idx += 1
