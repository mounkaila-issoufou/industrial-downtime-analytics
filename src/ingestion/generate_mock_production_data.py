from src.core.context_store import context
from src.core.ids import generate_id
import random

def generate_production():
    hourly_prod = []
    events = []

    for shift in context.shifts:
        for hour in range(8):  # 8h par shift
            prod_id = generate_id("HP")

            theoretical = 4800
            actual = random.randint(2500, 4200)
            downtime = int((theoretical - actual) / 80)

            hourly_prod.append({
                "hourly_prod_id": prod_id,
                "date": shift["date"],
                "session": shift["session"],
                "operator_id": shift["team_lead_id"],  # contexte
                "team_lead_id": shift["team_lead_id"],
                "actual_production": actual,
                "non_production_minutes": downtime
            })

            if downtime > 0:
                events.append({
                    "event_id": generate_id("EV"),
                    "hourly_prod_id": prod_id,
                    "event_type": "machine_stop",
                    "duration_minutes": downtime,
                    "comment": "Défaut trainard entrée"
                })

    return hourly_prod, events
