import uuid


def generate_id(prefix: str) -> str:
    """
    Génère un identifiant unique lisible et traçable.

    Exemple :
    - SS_a3f9c2d1   (shift_supervision)
    - SOA_91bd22fa  (shift_operator_assignment)
    - HP_12a6bd53   (hourly_production)
    - EV_88c10a9e   (production_event)
    """
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
