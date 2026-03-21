from industrial_downtime.ingestion.production.compute_production import compute_production
from industrial_downtime.config.workshops import WORKSHOPS
def test_compute_production():
    
    actual, downtime, events = compute_production(line_config, 1)

    assert actual >= 0
    assert downtime >= 0
