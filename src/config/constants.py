# =========================
# SHIFTS / SESSIONS
# =========================

SHIFTS = {
    "MATIN": {
        "start": "05:00",
        "end": "13:15",
        "hours": 8
    },
    "SOIR": {
        "start": "13:15",
        "end": "21:30",
        "hours": 8
    },
    "NUIT": {
        "start": "21:30",
        "end": "05:00",
        "hours": 8
    },
    "SD": {
        "start": "06:00",
        "end": "10:00",
        "hours": 4
    }
}

# =========================
# PRODUCTION
# =========================

THEORETICAL_CAPACITY_PER_HOUR = 4800
UNITS_PER_MINUTE = 80

# =========================
# EVENTS
# =========================

EVENT_TYPES = [
    # --- Technical failures (machine / mechanical) ---
    "infeed_conveyor_failure",
    "outfeed_conveyor_failure",
    "door_safety_fault",
    "delta_sensor_fault_1",
    "delta_sensor_fault_2",
    "base_plate_transfer_fault",
    "base_plate_position_fault",
    "product_detachment_fault",
    "stacker_jam",
    "destacker_jam",
    "empty_tray_before_stacker",
    "tray_blocked_in_stacker",
    "axis_collision",
    "photoelectric_sensor_fault",

    # --- Packaging process issues ---
    "sticker_application_fault",
    "sticker_rewinder_belt_break",
    "film_retake",
    "missing_film_imprint",
    "product_length_out_of_range",
    "cassette_sticker_adjustment",
    "conveyor_output_jam",

    # --- Organizational / operational stops ---
    "material_shortage",
    "poor_material_supply",
    "small_product_output",
    "label_ribbon_replacement",
    "ink_ribbon_replacement",

    # --- Changeover & setup ---
    "intermediate_changeover",
    "paper_roll_change",
    "sticker_roll_change",
    "article_code_change",
    "date_marking_change",
    "weigher_tank_change",
    "case_packer_format_change",

    # --- Planned activities ---
    "cleaning",
    "machine_warmup",
    "shift_handover",
    "operator_break",
    "meeting",

    # --- Maintenance ---
    "planned_maintenance",
    "unplanned_maintenance",

    # --- Misc ---
    "unknown_event",
    "other"
]

# --- Configuration métier ---
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