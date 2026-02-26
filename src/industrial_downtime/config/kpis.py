from enum import Enum

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