from dataclasses import dataclass
from datetime import time
from typing import List, Dict
from enum import Enum


# ==========================
# Enum pour shifts
# ==========================
class ShiftName(str, Enum):
    MATIN = "MATIN"
    SOIR = "SOIR"
    NUIT = "NUIT"
    SD = "SD"


# ==========================
# Pause / break
# ==========================
@dataclass(frozen=True)
class Break:
    start: time
    duration_minutes: int


@dataclass(frozen=True)
class Shift:
    name: ShiftName
    start: time
    end: time
    hours: float
    breaks: List[Break]


SHIFTS: Dict[ShiftName, Shift] = {
    ShiftName.MATIN: Shift(
        name=ShiftName.MATIN,
        start=time(5, 0),
        end=time(13, 15),
        hours=8,
        breaks=[
            Break(start=time(7, 30), duration_minutes=20),
            Break(start=time(10, 30), duration_minutes=30),
        ],
    ),
    ShiftName.SOIR: Shift(
        name=ShiftName.SOIR,
        start=time(13, 15),
        end=time(21, 30),
        hours=8,
        breaks=[
            Break(start=time(15, 30), duration_minutes=20),
            Break(start=time(18, 30), duration_minutes=30),
        ],
    ),
    ShiftName.NUIT: Shift(
        name=ShiftName.NUIT,
        start=time(21, 30),
        end=time(5, 0),
        hours=8,
        breaks=[
            Break(start=time(23, 30), duration_minutes=20),
            Break(start=time(2, 30), duration_minutes=30),
        ],
    ),
    ShiftName.SD: Shift(
        name=ShiftName.SD,
        start=time(6, 0),
        end=time(10, 0),
        hours=4,
        breaks=[],
    ),
}
