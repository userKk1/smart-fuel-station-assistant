# simulator/ETL/transform.py

import pandas as pd


class DataTransformer:

    def __init__(self, datasets):

        self.datasets = datasets

    # ----------------------------------
    # Transactions
    # ----------------------------------

    def transform_transactions(self):

        if "transactions" not in self.datasets:
            return

        df = self.datasets["transactions"].copy()

        df["datetime"] = pd.to_datetime(df["datetime"])

        df["year"] = df["datetime"].dt.year
        df["month"] = df["datetime"].dt.month
        df["day"] = df["datetime"].dt.day
        df["hour"] = df["datetime"].dt.hour
        df["weekday"] = df["datetime"].dt.day_name()

        df["is_weekend"] = (
            df["datetime"].dt.weekday >= 5
        )

        self.datasets["transactions"] = df

    # ----------------------------------
    # Inventory History
    # ----------------------------------

    def transform_inventory_history(self):

        if "inventory_history" not in self.datasets:
            return

        df = self.datasets["inventory_history"].copy()

        df["stock_ratio"] = (
            df["current_stock"] /
            df["tank_capacity"]
        ).round(2)

        self.datasets["inventory_history"] = df

    # ----------------------------------
    # Complaints
    # ----------------------------------

    def transform_complaints(self):

        if "complaints" not in self.datasets:
            return

        df = self.datasets["complaints"].copy()

        severity_score = {

            "Low": 1,
            "Medium": 2,
            "High": 3

        }

        df["severity_score"] = (
            df["severity"].map(severity_score)
        )

        self.datasets["complaints"] = df

    # ----------------------------------
    # Maintenance
    # ----------------------------------

    def transform_maintenance(self):

        if "maintenance" not in self.datasets:
            return

        df = self.datasets["maintenance"].copy()

        if "repair_days" in df.columns:

            df["repair_hours"] = (
                df["repair_days"] * 24
            )

        self.datasets["maintenance"] = df

    # ----------------------------------
    # Transformation globale
    # ----------------------------------

    def transform(self):

        print("=" * 50)
        print("TRANSFORMATION DES DONNÉES")
        print("=" * 50)

        self.transform_transactions()
        self.transform_inventory_history()
        self.transform_complaints()
        self.transform_maintenance()

        print("Transformation terminée.\n")

        return self.datasets


# ----------------------------------
# Test du module
# ----------------------------------

if __name__ == "__main__":

    from extract import DataExtractor

    datasets = DataExtractor().extract()

    transformer = DataTransformer(datasets)

    datasets = transformer.transform()

    print("Transformation réussie.")