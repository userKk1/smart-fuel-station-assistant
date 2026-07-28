# simulator/ETL/load.py

import sqlite3
from pathlib import Path


class DataLoader:

    def __init__(self, datasets):

        self.datasets = datasets
        self.database_path = Path(
            "database/station.db"
        )

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def load(self):

        print("=" * 50)
        print("CHARGEMENT DANS SQLITE")
        print("=" * 50)

        connection = sqlite3.connect(
            self.database_path
        )

        for table_name, df in self.datasets.items():

            df.to_sql(

                name=table_name,
                con=connection,
                if_exists="replace",
                index=False

            )

            print(
                f"{table_name:<25}"
                f"{len(df):>8} lignes chargées."
            )

        connection.commit()
        connection.close()

        print("\nBase SQLite créée avec succès.\n")


# ----------------------------------
# Test du module
# ----------------------------------

if __name__ == "__main__":

    from extract import DataExtractor
    from transform import DataTransformer

    datasets = DataExtractor().extract()

    datasets = DataTransformer(
        datasets
    ).transform()

    loader = DataLoader(datasets)

    loader.load()