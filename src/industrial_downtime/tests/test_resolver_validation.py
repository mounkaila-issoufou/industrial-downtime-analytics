import collections
import matplotlib.pyplot as plt
from collections import Counter

from industrial_downtime.core.resolver.event_resolver import (
    resolve_event,
    ResolutionContext,
)
from industrial_downtime.core.markov_engine import LineState
from industrial_downtime.config.workshops import LineConfig
from industrial_downtime.config.shifts import Shift


# =========================
# SIMULATION
# =========================
def run_simulation(n=10000):
    line = LineConfig(name="line_x", robustness=0.6)
    shift = Shift(name="JOUR")

    results = []

    for _ in range(n):
        ctx = ResolutionContext(
            state=LineState.MICRO_STOP,
            line=line,
            shift=shift,
            repetition_count=1,
        )

        res = resolve_event(ctx)
        results.append(res.event_key)

    return results


# =========================
# PLOT
# =========================
def plot_distribution(results, title="Event Distribution", save=True):
    counter = Counter(results)

    events = list(counter.keys())
    counts = list(counter.values())

    plt.figure()
    plt.bar(events, counts)
    plt.xticks(rotation=90)
    plt.title(title)
    plt.xlabel("Events")
    plt.ylabel("Count")
    plt.tight_layout()

    if save:
        plt.savefig(f"{title}.png")
        print(f"[INFO] Plot saved as {title}.png")
    else:
        plt.show()

    plt.close()  # 🔥 IMPORTANT (évite mémoire + conflits)


# =========================
# TESTS
# =========================
def test_distribution():
    results = run_simulation(5000)

    counter = collections.Counter(results)

    print("\n=== DISTRIBUTION ===")
    for k, v in counter.most_common():
        print(f"{k}: {v}")

    # diversité
    assert len(counter) > 5, "Pas assez de diversité"

    # domination
    most_common_ratio = counter.most_common(1)[0][1] / len(results)
    assert most_common_ratio < 0.5, "Un event domine trop"


def test_state_coherence():
    line = LineConfig(name="line_A", robustness=0.6)
    shift = Shift(name="JOUR")

    ctx = ResolutionContext(
        state=LineState.FAILURE,
        line=line,
        shift=shift,
        repetition_count=1,
    )

    results = [resolve_event(ctx).event_key for _ in range(200)]

    forbidden = ["operator_break", "cleaning"]

    for r in results:
        assert r not in forbidden, f"Incohérence: {r}"


def test_robustness_impact():
    shift = Shift(name="JOUR")

    low = LineConfig(name="line_A", robustness=0.2)
    high = LineConfig(name="line_A", robustness=0.9)

    def run(line):
        return [
            resolve_event(
                ResolutionContext(LineState.FAILURE, line, shift)
            ).event_key
            for _ in range(500)
        ]

    low_res = run(low)
    high_res = run(high)

    low_mech = sum("jam" in e or "fault" in e for e in low_res)
    high_mech = sum("jam" in e or "fault" in e for e in high_res)

    assert low_mech > high_mech, "Robustness n'impacte pas correctement"


def test_distribution_visual():
    results = run_simulation(5000)

    plot_distribution(results, title="MICRO_STOP_distribution", save=True)

    counter = Counter(results)
    assert len(counter) > 5


# =========================
# DEBUG MODE (RUN DIRECT)
# =========================
if __name__ == "__main__":
    results = run_simulation(5000)
    plot_distribution(results, "MICRO_STOP_distribution", save=False)