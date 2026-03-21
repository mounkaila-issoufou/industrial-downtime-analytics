
from industrial_downtime.ingestion.quality import generate_quality_for_hour



def test_quality():
    ins, defects = generate_quality_for_hour("HP_1", 200)

    assert len(ins) > 0
    assert isinstance(defects, list)
