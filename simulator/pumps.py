from pathlib import Path
from datetime import date
import random

import pandas as pd

from config import (
    FUELS,
    PUMP_INSTALLATION_START_YEAR,
    PUMP_INSTALLATION_END_YEAR,
)


class PumpGenerator:

    def __init__(self, stations_file="data/stations.csv"):
        self.stations_file = stations_file

    def generate(self):

        stations = pd.read_csv(self.stations_file)

        rows = []

        pump_counter = 1

        for _, station in stations.iterrows():

            n_pumps = station["num_pumps"]

            gasoil_pumps = round(n_pumps * 0.7)
            sp_pumps = n_pumps - gasoil_pumps

            fuel_list = (
                ["Gasoil"] * gasoil_pumps +
                ["Sans Plomb"] * sp_pumps
            )

            random.shuffle(fuel_list)

            for fuel in fuel_list:

                year = random.randint(
                    PUMP_INSTALLATION_START_YEAR,
                    PUMP_INSTALLATION_END_YEAR
                )

                month = random.randint(1, 12)

                day = random.randint(1, 28)

                install_date = date(year, month, day)

                rows.append({

                    "pump_id": f"P{pump_counter:04d}",

                    "station_id": station["station_id"],

                    "station_name": station["station_name"],

                    "fuel_type": fuel,

                    "installation_date": install_date,

                    "age": 2025 - year,

                    "status": "Operational",

                    "usage_count": 0

                })

                pump_counter += 1

        return pd.DataFrame(rows)

    def save(self, output_folder="data"):

        output_folder = Path(output_folder)
        output_folder.mkdir(exist_ok=True)

        df = self.generate()

        output_file = output_folder / "pumps.csv"

        df.to_csv(output_file, index=False)

        print(f"{len(df)} pompes générées.")

        print(f"Fichier sauvegardé : {output_file}")

        return df