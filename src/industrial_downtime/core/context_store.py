class ContextStore:
    """
    Stocke les objets générés pour garantir la cohérence inter-fichiers
    """
    def __init__(self):
        self.shifts = []
        self.operator_assignments = []

context = ContextStore()
