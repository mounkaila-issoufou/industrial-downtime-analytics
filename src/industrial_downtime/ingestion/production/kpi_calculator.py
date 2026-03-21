import random

def compute_kpis(
    actual_production: int,
    theoretical_production: int,
    reliability_target: float,
    non_production_minutes: int,
) -> dict:
    """
    Calcule les KPI industriels pour une heure donnée.

    Returns:
        dict contenant tous les KPI
    """

    # 🟢 Sécurité division
    if theoretical_production > 0:
        reliability_rate = actual_production / theoretical_production
    else:
        reliability_rate = 0

    reliability_gap = reliability_rate - reliability_target

    if non_production_minutes > 0:

        unexplained_ratio = random.uniform(0.05, 0.2)

        unexplained_minutes = int(non_production_minutes * unexplained_ratio)
        explained_minutes = non_production_minutes - unexplained_minutes


        explained_ratio = explained_minutes / non_production_minutes
        unexplained_ratio = unexplained_minutes / non_production_minutes
    else:
        explained_minutes = 0
        unexplained_minutes = 0

        explained_ratio = 0
        unexplained_ratio = 0

    return {
        "explained_minutes": int(explained_minutes),
        "unexplained_minutes": int(unexplained_minutes),
        "reliability_rate": reliability_rate,
        "reliability_gap": reliability_gap,
        "explained_ratio": explained_ratio,
        "unexplained_ratio": unexplained_ratio,
    }
