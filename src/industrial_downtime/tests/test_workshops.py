from industrial_downtime.config.workshops import WORKSHOPS


def test_workshops_lines():
    for ws_name, ws in WORKSHOPS.items():
        assert hasattr(ws, "lines")
        for line_code, line in ws.lines.items():
            assert hasattr(line, "theoretical_capacity_per_hour")
            assert hasattr(line, "units_per_minute")
            assert hasattr(line, "reliability_target")
