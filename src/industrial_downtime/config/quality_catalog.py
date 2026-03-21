# ==========================================================
# QUALITY CATALOG
# Génération et gestion des défauts qualité (simulation industrielle)
# ==========================================================

from dataclasses import dataclass
from typing import List, Optional
import random


# ==========================================================
# DATA MODEL
# ==========================================================

@dataclass
class QualityDefect:
    defect_type: str
    category: str
    severity: str
    probability: float


# ==========================================================
# CATALOG DES DÉFAUTS
# ==========================================================

QUALITY_CATALOG: List[QualityDefect] = [

    # -------------------------
    # PACKAGING (très fréquent)
    # -------------------------
    QualityDefect("label_missing", "packaging", "medium", 0.03),
    QualityDefect("label_misaligned", "packaging", "low", 0.04),
    QualityDefect("package_not_centered", "packaging", "low", 0.025),
    QualityDefect("paper_wrinkle", "packaging", "low", 0.02),
    QualityDefect("sticker_missing", "packaging", "medium", 0.015),

    # -------------------------
    # PRODUCT
    # -------------------------
    QualityDefect("weight_too_low", "product", "high", 0.01),
    QualityDefect("weight_too_high", "product", "medium", 0.008),

    # -------------------------
    # FOOD SAFETY (critique)
    # -------------------------
    QualityDefect("foreign_body", "safety", "critical", 0.002),

    # -------------------------
    # TECHNIQUE
    # -------------------------
    QualityDefect("seal_failure", "packaging", "high", 0.007),
]


# ==========================================================
# UTILS
# ==========================================================

def normalize_probabilities(defects: List[QualityDefect]) -> List[float]:
    total = sum(d.probability for d in defects)
    if total == 0:
        raise ValueError("Total probability cannot be zero")

    return [d.probability / total for d in defects]


# ==========================================================
# CORE FUNCTION
# ==========================================================

def pick_defect(
    defects: List[QualityDefect] = QUALITY_CATALOG,
    category: Optional[str] = None,
    severity: Optional[str] = None
) -> QualityDefect:
    """
    Tire un défaut aléatoire selon les probabilités pondérées.

    Paramètres:
    - category: filtre par catégorie (packaging, product, safety...)
    - severity: filtre par niveau de sévérité (low, medium, high, critical)
    """

    # 🔎 Filtrage dynamique
    filtered = [
        d for d in defects
        if (category is None or d.category == category)
        and (severity is None or d.severity == severity)
    ]

    if not filtered:
        raise ValueError("No defects match the given filters")

    weights = normalize_probabilities(filtered)

    # 🎯 Tirage pondéré
    return random.choices(filtered, weights=weights, k=1)[0]


# ==========================================================
# CONTEXT-AWARE GENERATION
# ==========================================================

def pick_defect_with_context(
    machine_wear: float = 1.0,
    quality_level: float = 1.0
) -> QualityDefect:
    """
    Génère un défaut en fonction du contexte industriel.

    Paramètres:
    - machine_wear: >1 = machine usée → plus de défauts
    - quality_level: <1 = mauvaise qualité → plus de défauts critiques
    """

    adjusted: List[QualityDefect] = []

    for d in QUALITY_CATALOG:

        # Ajustement probabilité globale
        prob = d.probability * machine_wear

        # Boost défauts critiques si qualité mauvaise
        if d.severity in ("high", "critical"):
            prob *= (2 - quality_level)

        adjusted.append(
            QualityDefect(
                defect_type=d.defect_type,
                category=d.category,
                severity=d.severity,
                probability=prob
            )
        )

    return pick_defect(adjusted)


# ==========================================================
# BULK GENERATION (dataset / simulation)
# ==========================================================

def generate_defects(n: int) -> List[QualityDefect]:
    """
    Génère une liste de défauts (simulation de production)
    """
    return [pick_defect() for _ in range(n)]

