
from industrial_downtime.core.markov_engine import LineState


from industrial_downtime.ingestion.events.production_event_generator import generate_production_events
def test_generate_events():
    events = [(LineState.FAILURE, 10)]

    result = generate_production_events("HP_1", events)

    assert len(result) == 1
    assert result[0]["duration_minutes"] == 10
