from industrial_downtime.config.kpis import RELIABILITY, EXPLAINED_LOSS_RATE, PRODUCTION_VOLUME

def test_kpi_values():
    for kpi in [RELIABILITY, EXPLAINED_LOSS_RATE, PRODUCTION_VOLUME]:
        assert hasattr(kpi, "code")
        assert hasattr(kpi, "description")
        assert hasattr(kpi, "target")
        assert hasattr(kpi, "unit")