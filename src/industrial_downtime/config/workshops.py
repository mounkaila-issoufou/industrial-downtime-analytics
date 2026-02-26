from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class LineConfig:
    code: str
    theoretical_capacity_per_hour: int
    units_per_minute: int
    reliability_target: float

@dataclass(frozen=True)
class Workshop:
    name: str
    lines: Dict[str, LineConfig]


# ==========================
# OV LINES
# ==========================
OV_LINES = {
    "L_OV_MS": LineConfig("L_OV_MS", 1200, 20, 0.60),
    "L_OV_ES": LineConfig("L_OV_ES", 1500, 25, 0.65),
    "L_OV_X": LineConfig("L_OV_X", 1800, 30, 0.70),
    "L_OV_Y": LineConfig("L_OV_Y", 1560, 26, 0.63),
    "L_OV_Z": LineConfig("L_OV_Z", 1380, 23, 0.58),
}

# ==========================
# CAMEMBERT LINES
# ==========================
CAM_LINES = {
    "L_CAM_A": LineConfig("L_CAM_A", 1020, 17, 0.55),
    "L_CAM_B": LineConfig("L_CAM_B", 1080, 18, 0.57),
    "L_CAM_C": LineConfig("L_CAM_C", 1320, 22, 0.62),
}

# ==========================
# PORTION LINES
# ==========================
PORTION_LINES = {
    "L_PORTION_1": LineConfig("L_PORTION_1", 900, 15, 0.66),
    "L_PORTION_2": LineConfig("L_PORTION_2", 960, 16, 0.68),
}

WORKSHOPS: Dict[str, Workshop] = {
    "OVALE": Workshop("OVALE", OV_LINES),
    "CAMEMBERT": Workshop("CAMEMBERT", CAM_LINES),
    "PORTION": Workshop("PORTION", PORTION_LINES),
}