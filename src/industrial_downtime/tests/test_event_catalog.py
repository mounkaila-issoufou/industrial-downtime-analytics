import pytest
from industrial_downtime.config.event_catalog import (
    EVENT_CATALOG,
    EventCategory,
    Event,
)
def test_event_catalog_keys():
    for event_name, event in EVENT_CATALOG.items():
        assert isinstance(event, Event)
        assert isinstance(event.category, EventCategory)
        assert event.event == event_name
        assert all(hasattr(event, attr) for attr in ["organ", "element", "operator_action"])