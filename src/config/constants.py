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
# PRODUCTION
# =========================

THEORETICAL_CAPACITY_PER_HOUR = 4800
UNITS_PER_MINUTE = 80

# =========================
# EVENT CLASSIFICATION
# =========================

EVENT_CLASSIFICATION = {
    # ======================
    # TECHNICAL
    # ======================
    "infeed_conveyor_failure": "mechanical",
    "outfeed_conveyor_failure": "mechanical",
    "door_safety_fault": "electrical",
    "delta_sensor_fault_1": "electrical",
    "delta_sensor_fault_2": "electrical",
    "base_plate_transfer_fault": "mechanical",
    "base_plate_position_fault": "mechanical",
    "product_detachment_fault": "mechanical",
    "stacker_jam": "mechanical",
    "destacker_jam": "mechanical",
    "empty_tray_before_stacker": "process",
    "tray_blocked_in_stacker": "mechanical",
    "axis_collision": "mechanical",
    "photoelectric_sensor_fault": "electrical",

    # ======================
    # PROCESS / QUALITY
    # ======================
    "sticker_application_fault": "process",
    "sticker_rewinder_belt_break": "mechanical",
    "film_retake": "process",
    "missing_film_imprint": "quality",
    "product_length_out_of_range": "quality",
    "cassette_sticker_adjustment": "process",
    "conveyor_output_jam": "mechanical",

    # ======================
    # ORGANIZATION / HUMAN
    # ======================
    "material_shortage": "organization",
    "poor_material_supply": "organization",
    "small_product_output": "process",
    "label_ribbon_replacement": "operator",
    "ink_ribbon_replacement": "operator",

    # ======================
    # CHANGEOVER
    # ======================
    "intermediate_changeover": "changeover",
    "paper_roll_change": "changeover",
    "sticker_roll_change": "changeover",
    "article_code_change": "changeover",
    "date_marking_change": "changeover",
    "weigher_tank_change": "changeover",
    "case_packer_format_change": "changeover",

    # ======================
    # PLANNED
    # ======================
    "cleaning": "planned",
    "machine_warmup": "planned",
    "shift_handover": "planned",
    "operator_break": "planned",
    "meeting": "planned",

    # ======================
    # MAINTENANCE
    # ======================
    "planned_maintenance": "maintenance",
    "unplanned_maintenance": "maintenance",

    # ======================
    # OTHER
    # ======================
    "unknown_event": "other",
    "other": "other",
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
