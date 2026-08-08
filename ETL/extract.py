# simulator/ETL/extract.py

from pathlib import Path
import pandas as pd


class DataExtractor:

    def __init__(self):

        self.data_folder = Path("data")

    def extract(self):

        datasets = {}

        print("=" * 50)
        print("EXTRACTION DES DONNÉES")
        print("=" * 50)

        for file_path in self.data_folder.glob("*.csv"):

            table_name = file_path.stem

            df = pd.read_csv(file_path)

            datasets[table_name] = df

            print(
                f"{table_name:<25}"
                f"{len(df):>8} lignes"
            )

        print("\nExtraction terminée.\n")

        return datasets


if __name__ == "__main__":

    extractor = DataExtractor()

    datasets = extractor.extract()

    print("Fichiers extraits :")

    for name in datasets.keys():

        print(f"- {name}")