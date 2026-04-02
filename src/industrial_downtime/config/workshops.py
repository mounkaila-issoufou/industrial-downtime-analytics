from dataclasses import dataclass
from typing import Dict

from numpy import random
from industrial_downtime.core.markov_engine import LineState


def build_transition_matrix(
    robustness: float,
) -> dict[LineState, dict[LineState, float]]:
    """
    Matrice de transition enrichie — 8 états couverts.
    robustness = 0.0 (fragile) → plus de pannes
    robustness = 1.0 (robuste) → très stable
    """

    r = robustness  # alias court

    # ── Depuis RUNNING ──────────────────────────────────────────
    failure_prob      = 0.08 * (1 - r)
    micro_stop_prob   = 0.18 * (1 - r)
    quality_prob      = 0.04 * (1 - r)
    organization_prob = 0.03                   # indépendant de la robustesse
    human_prob        = 0.02                   # idem
    changeover_prob   = 0.01                   # rare, planifié
    maintenance_prob  = 0.02 * (1 - r)
    running_prob      = 1.0 - (
        failure_prob + micro_stop_prob + quality_prob +
        organization_prob + human_prob + changeover_prob + maintenance_prob
    )

    # ── Depuis MICRO_STOP ────────────────────────────────────────
    # Majorité retourne en RUNNING, petit risque d'escalade en FAILURE
    ms_to_running = 0.85 + 0.10 * r           # robuste → récupère plus vite
    ms_to_failure = 1.0 - ms_to_running

    # ── Depuis FAILURE ───────────────────────────────────────────
    # Toujours vers REPAIR (jamais retour direct en RUNNING)
    # Depuis REPAIR → RUNNING (avec risque de re-failure si fragile)
    repair_to_running  = 0.80 + 0.15 * r
    repair_to_failure  = 1.0 - repair_to_running

    # ── Depuis QUALITY ───────────────────────────────────────────
    quality_to_running  = 0.75
    quality_to_ms       = 0.15                # ajustement machine → micro-stop
    quality_to_stop     = 0.10                # escalade org / planifié

    # ── Depuis ORGANIZATION ──────────────────────────────────────
    org_to_running      = 0.80
    org_to_human        = 0.20                # attente opérateur

    # ── Depuis HUMAN ─────────────────────────────────────────────
    human_to_running    = 0.90
    human_to_org        = 0.10

    # ── Depuis CHANGEOVER ────────────────────────────────────────
    # Long mais déterministe → retour en RUNNING
    changeover_to_running = 1.0

    # ── Depuis MAINTENANCE ───────────────────────────────────────
    maint_to_running    = 0.85 + 0.10 * r
    maint_to_failure    = 1.0 - maint_to_running

    return {
        LineState.RUNNING: {
            LineState.RUNNING:      running_prob,
            LineState.MICRO_STOP:   micro_stop_prob,
            LineState.FAILURE:      failure_prob,
            LineState.QUALITY:      quality_prob,
            LineState.ORGANIZATION: organization_prob,
            LineState.HUMAN:        human_prob,
            LineState.CHANGEOVER:   changeover_prob,
            LineState.MAINTENANCE:  maintenance_prob,
        },
        LineState.MICRO_STOP: {
            LineState.RUNNING:  ms_to_running,
            LineState.FAILURE:  ms_to_failure,
        },
        LineState.FAILURE: {
            LineState.REPAIR: 1.0,
        },
        LineState.REPAIR: {
            LineState.RUNNING: repair_to_running,
            LineState.FAILURE: repair_to_failure,
        },
        LineState.QUALITY: {
            LineState.RUNNING:    quality_to_running,
            LineState.MICRO_STOP: quality_to_ms,
            LineState.PLANNED_STOP: quality_to_stop,
        },
        LineState.ORGANIZATION: {
            LineState.RUNNING: org_to_running,
            LineState.HUMAN:   org_to_human,
        },
        LineState.HUMAN: {
            LineState.RUNNING:      human_to_running,
            LineState.ORGANIZATION: human_to_org,
        },
        LineState.CHANGEOVER: {
            LineState.RUNNING: changeover_to_running,
        },
        LineState.MAINTENANCE: {
            LineState.RUNNING:  maint_to_running,
            LineState.FAILURE:  maint_to_failure,
        },
        LineState.PLANNED_STOP: {
            LineState.RUNNING: 1.0,
        },
    }


@dataclass(frozen=True)
class LineConfig:
    code: str
    theoretical_capacity_per_hour: int
    units_per_minute: int
    reliability_target: float
    robustness: float  # 0.0 fragile → 1.0 très robuste
    transition_matrix: dict[LineState, dict[LineState, float]]


@dataclass(frozen=True)
class Workshop:
    name: str
    lines: Dict[str, LineConfig]


# ==========================
# OV LINES
# ==========================
OV_LINES = {
    "L_OV_MS": LineConfig("L_OV_MS", 1200, 20, 0.60, 0.8, build_transition_matrix(0.5)),
    "L_OV_ES": LineConfig("L_OV_ES", 1500, 25, 0.65, 0.6, build_transition_matrix(0.6)),
    "L_OV_X": LineConfig("L_OV_X", 1800, 30, 0.70, 0.7, build_transition_matrix(0.7)),
    "L_OV_Y": LineConfig("L_OV_Y", 1560, 26, 0.63, 0.75, build_transition_matrix(0.55)),
    "L_OV_Z": LineConfig("L_OV_Z", 1380, 23, 0.58, 0.45, build_transition_matrix(0.45)),
}

# ==========================
# CAMEMBERT LINES
# ==========================
CAM_LINES = {
    "L_CAM_A": LineConfig("L_CAM_A", 1020, 17, 0.55, 0.5, build_transition_matrix(0.5)),
    "L_CAM_B": LineConfig(
        "L_CAM_B", 1080, 18, 0.57, 0.55, build_transition_matrix(0.55)
    ),
    "L_CAM_C": LineConfig("L_CAM_C", 1320, 22, 0.62, 0.6, build_transition_matrix(0.6)),
}

# ==========================
# PORTION LINES
# ==========================
PORTION_LINES = {
    "L_PORTION_1": LineConfig(
        "L_PORTION_1", 900, 15, 0.66, 0.5, build_transition_matrix(0.5)
    ),
    "L_PORTION_2": LineConfig(
        "L_PORTION_2", 960, 16, 0.68, 0.55, build_transition_matrix(0.55)
    ),
}

WORKSHOPS: Dict[str, Workshop] = {
    "OVALE": Workshop("OVALE", OV_LINES),
    "CAMEMBERT": Workshop("CAMEMBERT", CAM_LINES),
    "PORTION": Workshop("PORTION", PORTION_LINES),
}

STATE_DURATION = {
    LineState.MICRO_STOP: (4, 1),  # moyenne 4 min
    LineState.REPAIR: (18, 5),  # moyenne 18 min
}
