from industrial_downtime.core.config_loader import load_baseline
from industrial_downtime.config.event_catalog import EVENT_CATALOG


def main():
    config = load_baseline()

    events_config = config.get("events", {})

    print("\n=== LINK TEST ===")

    # on prend 1 event réel du catalogue
    sample_event_name = next(iter(EVENT_CATALOG))
    sample_event = EVENT_CATALOG[sample_event_name]

    print(f"\nEvent from catalog: {sample_event_name}")
    print(f"Default probability: {sample_event.base_probability}")

    # si override existe dans config
    if sample_event_name in events_config:
        override = events_config[sample_event_name]
        print("Override found in config:")
        print(override)
    else:
        print("No override in config")


if __name__ == "__main__":
    main()