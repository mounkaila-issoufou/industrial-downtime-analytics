# =========================
# SHIFTS / SESSIONS
# =========================

SHIFTS = {
    "MATIN": {"start": "05:00", "end": "13:15", "hours": 8},
    "SOIR": {"start": "13:15", "end": "21:30", "hours": 8},
    "NUIT": {"start": "21:30", "end": "05:00", "hours": 8},
    "SD": {"start": "06:00", "end": "10:00", "hours": 4},
}


# =========================
# OPTIONAL: reverse mapping
# =========================

CAUSE_FAMILY_LABELS = {
    "mechanical": "Technical - Mechanical",
    "electrical": "Technical - Electrical",
    "process": "Process",
    "quality": "Quality",
    "organization": "Organization",
    "operator": "Human / Operator",
    "changeover": "Changeover",
    "planned": "Planned Stop",
    "maintenance": "Maintenance",
    "other": "Other",
}

# =========================
# BREAK RULES
# =========================

PAUSE_RULES = {
    "morning": [
        {"time": "07:30", "duration": 20},
        {"time": "10:30", "duration": 30},
    ],
    "afternoon": [
        {"time": "15:30", "duration": 20},
        {"time": "18:30", "duration": 30},
    ],
    "night": [
        {"time": "23:30", "duration": 20},
        {"time": "02:30", "duration": 30},
    ],
}
