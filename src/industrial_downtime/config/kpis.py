from enum import Enum
from dataclasses import dataclass


# ==========================
# KPI Dataclass
# ==========================
@dataclass(frozen=True)
class KPI:
    code: str
    description: str
    target: float
    unit: str


# ==========================
# KPI Instances
# ==========================
RELIABILITY = KPI(
    code="reliability",
    description="Reliability",
    target=0.95,
    unit="%",
)

EXPLAINED_LOSS_RATE = KPI(
    code="explained_loss_rate",
    description="Explained Loss Rate",
    target=0.90,
    unit="%",
)

PRODUCTION_VOLUME = KPI(
    code="production_volume",
    description="Production Volume",
    target=1000,
    unit="units",
)


class EventCategoryEnum(str, Enum):
    MECHANICAL = "mechanical"
    ELECTRICAL = "electrical"
    PROCESS = "process"
    QUALITY = "quality"
    ORGANIZATION = "organization"
    OPERATOR = "operator"
    CHANGEOVER = "changeover"
    PLANNED = "planned"
    MAINTENANCE = "maintenance"
    OTHER = "other"
