from pathlib import Path

import pandas as pd

from .llm_client import generate
from .prompts import MAINTENANCE_PROMPT


INPUT_FILE = "data/maintenance.csv"

OUTPUT_FOLDER = Path("simulator/llm/documents/maintenance")


def generate_maintenance_reports():

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    maintenance = pd.read_csv(INPUT_FILE)

    print(f"{len(maintenance)} rapports à générer...\n")

    for _, row in maintenance.iterrows():

        prompt = MAINTENANCE_PROMPT.format(

            date=row["start_date"],

            station_id=row["station_id"],

            station_name=row["station_name"],

            pump_id=row["pump_id"],

            failure_type=row["failure_type"],

            start_date=row["start_date"],

            expected_end_date=row["expected_end_date"],

            end_date=row["end_date"],

            technician=row["technician"],

            status=row["status"]

        )

        report = generate(prompt)

        output_file = OUTPUT_FOLDER / f"{row['maintenance_id']}.txt"

        with open(output_file, "w", encoding="utf-8") as f:

            f.write(report)

        print(f"✔ {output_file.name}")

    print("\nTous les rapports ont été générés.")

if __name__ == "__main__":
    
    generate_maintenance_reports()