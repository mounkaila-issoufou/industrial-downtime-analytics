from datetime import date

START_DATE = date(2026, 1, 3)
END_DATE = date(2026, 2, 10)

FACTORY_ID = "F_DOM"

LINES = ["L_OV_MS", "L_OV_ES", "L_OV_X", "L_OV_Y", "L_OV_Z"]

OPERATORS = ["OP_001", "OP_002", "OP_003", "OP_004", "OP_005", "OP_006", "OP_007", "OP_008", "OP_009", "OP_010"]
TEAM_LEADS = ["TL_001", "TL_002", "TL_003"]

RANDOM_SEED = 42

W_OV = {
    "L_OV_MS": {
        "THEORETICAL_CAPACITY_PER_HOUR": 1200,
        "UNITS_PER_MINUTE": 20,
        "RELIABILITY_TARGET": 0.60
    },
    "L_OV_ES": {
        "THEORETICAL_CAPACITY_PER_HOUR": 1500,
        "UNITS_PER_MINUTE": 25,
        "RELIABILITY_TARGET": 0.65
    },
    "L_OV_X": {
        "THEORETICAL_CAPACITY_PER_HOUR": 1800,
        "UNITS_PER_MINUTE": 30,
        "RELIABILITY_TARGET": 0.70
    },
    "L_OV_Y": {
        "THEORETICAL_CAPACITY_PER_HOUR": 1560,
        "UNITS_PER_MINUTE": 26,
        "RELIABILITY_TARGET": 0.63
    },
    "L_OV_Z": {
        "THEORETICAL_CAPACITY_PER_HOUR": 1380,
        "UNITS_PER_MINUTE": 23,
        "RELIABILITY_TARGET": 0.58
    }
}

W_CAM = {
    "L_CAM_A": {
        "THEORETICAL_CAPACITY_PER_HOUR": 1020,
        "UNITS_PER_MINUTE": 17,
        "RELIABILITY_TARGET": 0.55
    },
    "L_CAM_B": {
        "THEORETICAL_CAPACITY_PER_HOUR": 1080,
        "UNITS_PER_MINUTE": 18,
        "RELIABILITY_TARGET": 0.57
    },
    "L_CAM_C": {
        "THEORETICAL_CAPACITY_PER_HOUR": 1320,
        "UNITS_PER_MINUTE": 22,
        "RELIABILITY_TARGET": 0.62
    },
}

W_PORTION = {
    "L_PORTION_1": {
        "THEORETICAL_CAPACITY_PER_HOUR": 900,
        "UNITS_PER_MINUTE": 15,
        "RELIABILITY_TARGET": 0.66
    },
    "L_PORTION_2": {
        "THEORETICAL_CAPACITY_PER_HOUR": 960,
        "UNITS_PER_MINUTE": 16,
        "RELIABILITY_TARGET": 0.68
    },
}

WORKSHOPS = [W_CAM, W_OV, W_PORTION]


EVENT_CLASSIFICATION = {
    # ======================
    # TECHNICAL
    # ======================
    "infeed_conveyor_failure": {
        "event": "infeed_conveyor_failure",
        "event_category": "mechanical",
        "organ": "stacker",
        "element": "conveyor",
        "operator_action": "conveyor supply"
    },
    "outfeed_conveyor_failure": {
        "event": "outfeed_conveyor_failure",
        "event_category": "mechanical",
        "organ": "case_packer",
        "element": "conveyor",
        "operator_action": "product evacuation"
    },
    "door_safety_fault": {
        "event": "door_safety_fault",
        "event_category": "electrical",
        "organ": "safety_system",
        "element": "safety_door",
        "operator_action": "reset safety"
    },
    "delta_sensor_fault_1": {
        "event": "delta_sensor_fault_1",
        "event_category": "electrical",
        "organ": "delta_robot",
        "element": "sensor",
        "operator_action": "sensor check"
    },
    "delta_sensor_fault_2": {
        "event": "delta_sensor_fault_2",
        "event_category": "electrical",
        "organ": "delta_robot",
        "element": "sensor",
        "operator_action": "sensor check"
    },
    "base_plate_transfer_fault": {
        "event": "base_plate_transfer_fault",
        "event_category": "mechanical",
        "organ": "base_plate_system",
        "element": "transfer",
        "operator_action": "plate transfer"
    },
    "base_plate_position_fault": {
        "event": "base_plate_position_fault",
        "event_category": "mechanical",
        "organ": "base_plate_system",
        "element": "positioning",
        "operator_action": "plate alignment"
    },
    "product_detachment_fault": {
        "event": "product_detachment_fault",
        "event_category": "mechanical",
        "organ": "delta_robot",
        "element": "gripper",
        "operator_action": "product pick"
    },
    "stacker_jam": {
        "event": "stacker_jam",
        "event_category": "mechanical",
        "organ": "stacker",
        "element": "tray_flow",
        "operator_action": "tray clearance"
    },
    "destacker_jam": {
        "event": "destacker_jam",
        "event_category": "mechanical",
        "organ": "destacker",
        "element": "tray_flow",
        "operator_action": "tray clearance"
    },
    "empty_tray_before_stacker": {
        "event": "empty_tray_before_stacker",
        "event_category": "process",
        "organ": "stacker",
        "element": "tray_supply",
        "operator_action": "tray refill"
    },
    "tray_blocked_in_stacker": {
        "event": "tray_blocked_in_stacker",
        "event_category": "mechanical",
        "organ": "stacker",
        "element": "guide",
        "operator_action": "tray alignment"
    },
    "axis_collision": {
        "event": "axis_collision",
        "event_category": "mechanical",
        "organ": "robot_axis",
        "element": "axis",
        "operator_action": "axis reset"
    },
    "photoelectric_sensor_fault": {
        "event": "photoelectric_sensor_fault",
        "event_category": "electrical",
        "organ": "conveyor",
        "element": "photoelectric_sensor",
        "operator_action": "sensor cleaning"
    },

    # ======================
    # PROCESS / QUALITY
    # ======================
    "sticker_application_fault": {
        "event": "sticker_application_fault",
        "event_category": "process",
        "organ": "labeling_unit",
        "element": "applicator",
        "operator_action": "sticker adjustment"
    },
    "sticker_rewinder_belt_break": {
        "event": "sticker_rewinder_belt_break",
        "event_category": "mechanical",
        "organ": "labeling_unit",
        "element": "belt",
        "operator_action": "belt replacement"
    },
    "film_retake": {
        "event": "film_retake",
        "event_category": "process",
        "organ": "film_unit",
        "element": "film",
        "operator_action": "film reposition"
    },
    "missing_film_imprint": {
        "event": "missing_film_imprint",
        "event_category": "quality",
        "organ": "printing_unit",
        "element": "print_head",
        "operator_action": "print check"
    },
    "product_length_out_of_range": {
        "event": "product_length_out_of_range",
        "event_category": "quality",
        "organ": "measurement_system",
        "element": "length_control",
        "operator_action": "product rejection"
    },
    "cassette_sticker_adjustment": {
        "event": "cassette_sticker_adjustment",
        "event_category": "process",
        "organ": "labeling_unit",
        "element": "cassette",
        "operator_action": "cassette adjust"
    },
    "conveyor_output_jam": {
        "event": "conveyor_output_jam",
        "event_category": "mechanical",
        "organ": "outfeed_conveyor",
        "element": "product_flow",
        "operator_action": "jam removal"
    },

    # ======================
    # ORGANIZATION / HUMAN
    # ======================
    "material_shortage": {
        "event": "material_shortage",
        "event_category": "organization",
        "organ": "supply_chain",
        "element": "raw_material",
        "operator_action": "material supply"
    },
    "poor_material_supply": {
        "event": "poor_material_supply",
        "event_category": "organization",
        "organ": "supply_chain",
        "element": "logistics",
        "operator_action": "supply adjustment"
    },
    "small_product_output": {
        "event": "small_product_output",
        "event_category": "process",
        "organ": "upstream_process",
        "element": "throughput",
        "operator_action": "process check"
    },
    "label_ribbon_replacement": {
        "event": "label_ribbon_replacement",
        "event_category": "operator",
        "organ": "labeling_unit",
        "element": "ribbon",
        "operator_action": "ribbon replacement"
    },
    "ink_ribbon_replacement": {
        "event": "ink_ribbon_replacement",
        "event_category": "operator",
        "organ": "printing_unit",
        "element": "ink_ribbon",
        "operator_action": "ribbon replacement"
    },

    # ======================
    # CHANGEOVER
    # ======================
    "intermediate_changeover": {
        "event": "intermediate_changeover",
        "event_category": "changeover",
        "organ": "line",
        "element": "format",
        "operator_action": "changeover"
    },
    "paper_roll_change": {
        "event": "paper_roll_change",
        "event_category": "changeover",
        "organ": "printing_unit",
        "element": "paper_roll",
        "operator_action": "roll change"
    },
    "sticker_roll_change": {
        "event": "sticker_roll_change",
        "event_category": "changeover",
        "organ": "labeling_unit",
        "element": "sticker_roll",
        "operator_action": "roll change"
    },
    "article_code_change": {
        "event": "article_code_change",
        "event_category": "changeover",
        "organ": "control_system",
        "element": "article_code",
        "operator_action": "code update"
    },
    "date_marking_change": {
        "event": "date_marking_change",
        "event_category": "changeover",
        "organ": "printing_unit",
        "element": "date_format",
        "operator_action": "date setup"
    },
    "weigher_tank_change": {
        "event": "weigher_tank_change",
        "event_category": "changeover",
        "organ": "weigher",
        "element": "tank",
        "operator_action": "tank change"
    },
    "case_packer_format_change": {
        "event": "case_packer_format_change",
        "event_category": "changeover",
        "organ": "case_packer",
        "element": "format",
        "operator_action": "format change"
    },

    # ======================
    # PLANNED
    # ======================
    "cleaning": {
        "event": "cleaning",
        "event_category": "planned",
        "organ": "line",
        "element": "cleaning",
        "operator_action": "cleaning"
    },
    "machine_warmup": {
        "event": "machine_warmup",
        "event_category": "planned",
        "organ": "machine",
        "element": "startup",
        "operator_action": "warmup"
    },
    "shift_handover": {
        "event": "shift_handover",
        "event_category": "planned",
        "organ": "organization",
        "element": "handover",
        "operator_action": "handover"
    },
    "operator_break": {
        "event": "operator_break",
        "event_category": "planned",
        "organ": "human",
        "element": "break",
        "operator_action": "break"
    },
    "meeting": {
        "event": "meeting",
        "event_category": "planned",
        "organ": "organization",
        "element": "meeting",
        "operator_action": "meeting"
    },

    # ======================
    # MAINTENANCE
    # ======================
    "planned_maintenance": {
        "event": "planned_maintenance",
        "event_category": "maintenance",
        "organ": "maintenance",
        "element": "planned",
        "operator_action": "maintenance"
    },
    "unplanned_maintenance": {
        "event": "unplanned_maintenance",
        "event_category": "maintenance",
        "organ": "maintenance",
        "element": "unplanned",
        "operator_action": "maintenance"
    },

    # ======================
    # OTHER
    # ======================
    "unknown_event": {
        "event": "unknown_event",
        "event_category": "other",
        "organ": "unknown",
        "element": "unknown",
        "operator_action": "unknown"
    },
    "other": {
        "event": "other",
        "event_category": "other",
        "organ": "unknown",
        "element": "unknown",
        "operator_action": "unknown"
    },
}
