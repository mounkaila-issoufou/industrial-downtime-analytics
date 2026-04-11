from typing import Dict, Optional
import json
from pathlib import Path
import logging
import math

from industrial_downtime.config.event_catalog import EVENT_CATALOG

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]
BASELINE_DIR = BASE_DIR / "config" / "base"


class EventCalibrator:

    def __init__(self, baseline_dir: Optional[str] = None):

        self.event_counts: Dict[str, int] = {}
        self.total_events: int = 0

        self.base_path = Path(baseline_dir) if baseline_dir else BASELINE_DIR

        self.baselines = {
            "global": {},
            "lines": {},
            "shifts": {},
            "scenarios": {},
        }

        self.load_all_baselines()

    # =========================
    # LOAD
    # =========================
    def load_all_baselines(self):

        base = self.base_path

        self.baselines["global"] = self._safe_load(base / "baseline.json")

        for f in (base / "lines").glob("*.json"):
            self.baselines["lines"][f.stem] = self._safe_load(f)

        for f in (base / "shifts").glob("*.json"):
            self.baselines["shifts"][f.stem] = self._safe_load(f)

        for f in (base / "scenarios").glob("*.json"):
            self.baselines["scenarios"][f.stem] = self._safe_load(f)

    def _safe_load(self, path: Path) -> Dict:
        if not path.exists():
            return {}

        try:
            return json.load(open(path, "r")).get("events", {})
        except Exception as e:
            logger.warning(f"Baseline load failed {path}: {e}")
            return {}

    # =========================
    # STATS
    # =========================
    def update(self, event_key: str):
        self.event_counts[event_key] = self.event_counts.get(event_key, 0) + 1
        self.total_events += 1

    def reset(self):
        self.event_counts.clear()
        self.total_events = 0

    def get_frequency(self, event_key: str) -> float:
        if self.total_events == 0:
            return 0.0
        return self.event_counts.get(event_key, 0) / self.total_events

    # =========================
    # TARGET RESOLUTION (CLEAN + PRIORITY)
    # =========================
    def _get_target(self, event: str, line: str, shift: str, scenario: str, fallback: float):

        # 1. SCENARIO (MAX PRIORITY)
        if scenario and event in self.baselines["scenarios"].get(scenario, {}):
            return self.baselines["scenarios"][scenario][event]["base_probability"]

        # 2. SHIFT
        if shift and event in self.baselines["shifts"].get(shift, {}):
            return self.baselines["shifts"][shift][event]["base_probability"]

        # 3. LINE
        if line and event in self.baselines["lines"].get(line, {}):
            return self.baselines["lines"][line][event]["base_probability"]

        # 4. GLOBAL
        if event in self.baselines["global"]:
            return self.baselines["global"][event]["base_probability"]

        return fallback

    # =========================
    # CALIBRATION CORE
    # =========================
    def calibrate(
        self,
        scores: Dict[str, float],
        line: Optional[str] = None,
        shift: Optional[str] = None,
        scenario: Optional[str] = None,
    ) -> Dict[str, float]:

        if not scores:
            return {}

        raw = {}

        # 1. build stable raw weights
        for event, score in scores.items():

            catalog = EVENT_CATALOG.get(event)
            if not catalog:
                continue

            base = catalog.base_probability
            freq = self.get_frequency(event)

            target = self._get_target(event, line, shift, scenario, base)

            drift = target - freq

            correction = max(0.5, min(1.5, 1.0 + drift))

            anti_dom = 1.0 - min(freq, 0.5)

            rarity = 1.0 + max(0.0, 0.1 - freq)

            weight = score * correction * anti_dom * rarity

            raw[event] = max(weight, 1e-6)

        if not raw:
            logger.warning("Calibration fallback triggered")
            return scores

        # 2. normalize (IMPORTANT FIX)
        total = sum(raw.values())

        calibrated = {
            k: v / total for k, v in raw.items()
        }

        return calibrated

    # =========================
    # DRIFT
    # =========================
    def compute_drift(self):

        out = {}

        for event, cat in EVENT_CATALOG.items():
            obs = self.get_frequency(event)
            target = self._get_target(event, None, None, None, cat.base_probability)
            out[event] = obs - target

        return out


# =========================
# SINGLETON
# =========================
calibrator = EventCalibrator()