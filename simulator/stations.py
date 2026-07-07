# simulator/stations.py

from pathlib import Path
import pandas as pd

from config import STATIONS

class StationGenerator:
    """
    Génère les informations des stations à partir du fichier config.py.
    """

    def __init__(self):
        self.stations = STATIONS

    def generate(self):
        """
        Génère un DataFrame contenant toutes les stations.
        """

        rows = []

        for idx, (station_name, info) in enumerate(self.stations.items(), start=1):

            rows.append({

                "station_id": f"ST{idx:03d}",

                "station_name": station_name,

                "city": info["city"],

                "station_type": info["type"],

                "num_pumps": info["num_pumps"],

                "employees": info["employees"],

                "base_customers": info["base_customers"],

                "location_factor": info["location_factor"],

                "gasoil_capacity": info["tank_capacity"]["Gasoil"],

                "sans_plomb_capacity": info["tank_capacity"]["Sans Plomb"]

            })

        return pd.DataFrame(rows)

    def save(self, output_folder="data"):
        """
        Sauvegarde les stations dans un fichier CSV.
        """

        output_folder = Path(output_folder)
        output_folder.mkdir(exist_ok=True)

        df = self.generate()

        output_file = output_folder / "stations.csv"

        df.to_csv(output_file, index=False)

        print(f"{len(df)} stations générées.")

        print(f"Fichier sauvegardé : {output_file}")

        return df
    
