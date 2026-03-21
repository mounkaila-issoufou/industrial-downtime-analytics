from industrial_downtime.core.markov_engine import simulate_hour


def compute_production(line_config, hour_index: int) -> tuple[int, int, list]:
    """
    Simule la production pour une heure donnée.

    Returns:
        actual_production (int): unités produites
        non_production_minutes (int): minutes perdues
        events (list): liste des états (state, duration)
    """

    theoretical = line_config.theoretical_capacity_per_hour
    units_per_minute = line_config.units_per_minute

    # 🟢 Première heure = parfaite (warm-up industriel)
    if hour_index == 0:
        return theoretical, 0, []

    # 🔁 Simulation Markov
    events = simulate_hour(line_config, total_minutes=60)

    # ⛔ Temps perdu
    non_production_minutes = sum(duration for _, duration in events)

    # ✅ Temps productif
    productive_minutes = 60 - non_production_minutes

    # 📦 Production réelle
    actual_production = int(productive_minutes * units_per_minute)

    return actual_production, non_production_minutes, events
