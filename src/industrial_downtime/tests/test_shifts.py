from industrial_downtime.config.shifts import SHIFTS, ShiftName
from datetime import time


def test_shifts_structure():
    for shift_name, shift in SHIFTS.items():
        assert (
            shift_name in ShiftName.__members__.values()
            or shift_name in ShiftName.__dict__.values()
        )
        assert isinstance(shift.start, time)
        assert isinstance(shift.end, time)
        for brk in shift.breaks:
            assert isinstance(brk.start, time)
            assert isinstance(brk.duration_minutes, int)
