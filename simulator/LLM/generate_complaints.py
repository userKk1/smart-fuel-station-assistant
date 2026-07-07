import pandas as pd
from pathlib import Path

from prompts import COMPLAINT_PROMPT
from llm_client import generate


INPUT_FILE = "data/complaints.csv"

OUTPUT_FOLDER = Path("llm/documents/complaints")


def generate_complaint():

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    complaints = pd.read_csv(INPUT_FILE)

    print(f"{len(complaints)} réclamations à générer...\n")

    for _, row in complaints.iterrows():

        prompt = COMPLAINT_PROMPT.format(

            station=row["station_name"],

            date=row["date"],

            category=row["category"],

            reason=row["reason"],

            affected=row["affected_customers"],

            severity=row["severity"]

        )

        text = generate(prompt)

        output_file = OUTPUT_FOLDER / f"{row['complaint_id']}.txt"

        with open(output_file, "w", encoding="utf-8") as f:

            f.write(text)

        print(f"✔ {output_file.name}")

    print("\nTous les documents de réclamation ont été générés.")


if __name__ == "__main__":

    generate_complaint()