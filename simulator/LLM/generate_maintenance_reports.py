from pathlib import Path

import pandas as pd

from llm_client import generate
from prompts import MAINTENANCE_PROMPT


INPUT_FILE = "data/maintenance.csv"

OUTPUT_FOLDER = Path("llm/documents/maintenance")


def generate_maintenance_reports():

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    maintenance = pd.read_csv(INPUT_FILE)

    print(f"{len(maintenance)} rapports à générer...\n")

    for _, row in maintenance.iterrows():

        prompt = MAINTENANCE_PROMPT.format(

            date=row["date"],

            station=row["station_name"],

            city=row["city"],

            pump=row["pump_id"],

            failure=row["failure_type"],

            repair_time=row["repair_days"],

            technician=row["technician"]

        )

        report = generate(prompt)

        output_file = OUTPUT_FOLDER / f"{row['maintenance_id']}.txt"

        with open(output_file, "w", encoding="utf-8") as f:

            f.write(report)

        print(f"✔ {output_file.name}")

    print("\nTous les rapports ont été générés.")

if __name__ == "__main__":
    
    generate_maintenance_reports()