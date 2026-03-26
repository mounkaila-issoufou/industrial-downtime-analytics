import uuid

def generate_id(prefix: str) -> str:
    """
    Génère un identifiant unique (sans collision).
    """
    return f"{prefix}_{uuid.uuid4().hex}"