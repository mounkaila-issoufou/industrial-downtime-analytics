from datetime import timedelta, date as date_type

from industrial_downtime.config.settings import START_DATE, END_DATE
from industrial_downtime.config.shifts import SHIFTS, ShiftName


# =========================
# DATE ITERATOR
# =========================

def iter_dates():
    """
    Génère toutes les dates entre START_DATE et END_DATE incluses.
    """
    current = START_DATE
    while current <= END_DATE:
        yield current
        current += timedelta(days=1)


# =========================
# SESSION LOGIC
# =========================

def get_sessions_for_date(day: date_type) -> list[ShiftName]:
    """
    Retourne les sessions applicables selon le jour :
    - semaine : MATIN / SOIR / NUIT
    - week-end : SD
    """

    if day.weekday() >= 5:  # 5 = samedi, 6 = dimanche
        return [ShiftName.SD]

    return [
        ShiftName.MATIN,
        ShiftName.SOIR,
        ShiftName.NUIT,
    ]


# =========================
# SHIFT GENERATOR
# =========================

def iter_shifts():
    """
    Génère les shifts réels (date + session + horaires).
    """

    for day in iter_dates():
        for session in get_sessions_for_date(day):

            shift_cfg = SHIFTS[session]

            yield {
                "date": day,
                "session": session.value,  # 👈 important
                "start_time": shift_cfg.start,
                "end_time": shift_cfg.end,
                "duration_hours": shift_cfg.hours,
            }