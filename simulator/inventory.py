from pathlib import Path
import random

import pandas as pd

from config import DELIVERY_THRESHOLD, FUELS


class InventoryGenerator:

    def __init__(self, stations_file="data/stations.csv"):
        self.stations_file = stations_file

    def generate(self):

        stations = pd.read_csv(self.stations_file)

        rows = []

        inventory_counter = 1

        for _, station in stations.iterrows():

            capacities = {
                "Gasoil": station["gasoil_capacity"],
                "Sans Plomb": station["sans_plomb_capacity"]
            }

            for fuel in FUELS:

                capacity = capacities[fuel]

                current_stock = capacity

                rows.append({

                    "inventory_id": f"INV{inventory_counter:03d}",

                    "station_id": station["station_id"],

                    "station_name": station["station_name"],

                    "fuel_type": fuel,

                    "tank_capacity": capacity,

                    "current_stock": current_stock,

                    "reorder_level": int(capacity * DELIVERY_THRESHOLD)

                })

                inventory_counter += 1

        return pd.DataFrame(rows)

    def save(self, output_folder="data"):

        output_folder = Path(output_folder)
        output_folder.mkdir(exist_ok=True)

        df = self.generate()

        output_file = output_folder / "inventory.csv"

        df.to_csv(output_file, index=False)

        print(f"{len(df)} stocks générés.")

        print(f"Fichier sauvegardé : {output_file}")

        return df