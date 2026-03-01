import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path("data/raw")


def export_csv(records: list[dict], filename: str):
    """
    Exporte une liste de dictionnaires en CSV.
    """
    if not records:
        print(f"⚠ Aucun enregistrement à exporter pour {filename}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(records)
    output_path = OUTPUT_DIR / filename
    df.to_csv(output_path, index=False)

    print(f"✔ Exporté : {output_path}")
