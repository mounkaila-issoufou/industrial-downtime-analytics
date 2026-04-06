import json
from pathlib import Path


def load_baseline():
    base_path = Path(__file__).resolve().parents[2]
    path = base_path / "industrial_downtime" / "config" / "base" / "baseline.json"

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    