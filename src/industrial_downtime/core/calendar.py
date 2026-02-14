from datetime import timedelta
from src.config.settings import START_DATE, END_DATE
from src.config.constants import SHIFTS


def iter_dates():
    """
    Génère toutes les dates entre START_DATE et END_DATE incluses.
    """
    current = START_DATE
    while current <= END_DATE:
        yield current
        current += timedelta(days=1)


def get_sessions_for_date(date):
    """
    Retourne les sessions applicables selon le jour :
    - semaine : matin / soir / nuit
    - week-end : SD
    """
    if date.weekday() >= 5:  # samedi = 5, dimanche = 6
        return ["SD"]
    return ["MATIN", "SOIR", "NUIT"]


def iter_shifts():
    """
    Génère les shifts réels (date + session + horaires).
    """
    for date in iter_dates():
        for session in get_sessions_for_date(date):
            shift_cfg = SHIFTS[session]

            yield {
                "date": date,
                "session": session,
                "start_time": shift_cfg["start"],
                "end_time": shift_cfg["end"],
                "duration_hours": shift_cfg["hours"]
            }
