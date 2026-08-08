# simulator/ETL/validate.py

import pandas as pd


class DataValidator:

    def __init__(self, datasets):

        self.datasets = datasets
        self.errors = []

    # ----------------------------------
    # Vérifier les valeurs manquantes
    # ----------------------------------

    def check_missing_values(self, table_name, df):

        if df.isnull().sum().sum() > 0:

            self.errors.append(
                f"{table_name} contient des valeurs manquantes."
            )

    # ----------------------------------
    # Vérifier les doublons
    # ----------------------------------

    def check_duplicates(self, table_name, df):

        if df.duplicated().sum() > 0:

            self.errors.append(
                f"{table_name} contient des lignes dupliquées."
            )

    # ----------------------------------
    # Vérifier les DataFrames vides
    # ----------------------------------

    def check_empty_dataframe(self, table_name, df):

        if df.empty:

            self.errors.append(
                f"{table_name} est vide."
            )

    # ----------------------------------
    # Vérifier certaines colonnes numériques
    # ----------------------------------

    def check_negative_values(self, table_name, df):

        numeric_columns = [

            "current_stock",
            "tank_capacity",
            "liters",
            "amount",
            "quantity",
            "repair_days"

        ]

        for column in numeric_columns:

            if column in df.columns:

                if (df[column] < 0).any():

                    self.errors.append(
                        f"{table_name} contient des valeurs négatives dans '{column}'."
                    )

    # ----------------------------------
    # Validation globale
    # ----------------------------------

    def validate(self):

        print("=" * 50)
        print("VALIDATION DES DONNÉES")
        print("=" * 50)

        for table_name, df in self.datasets.items():

            self.check_empty_dataframe(table_name, df)
            self.check_missing_values(table_name, df)
            self.check_duplicates(table_name, df)
            self.check_negative_values(table_name, df)

        # Affichage des résultats

        if len(self.errors) == 0:

            print("Aucune erreur détectée.\n")

        else:

            print("\nErreurs détectées :\n")

            for error in self.errors:

                print(f"- {error}")

        return self.errors


# ---------------------------------------------------
# Test du module
# ---------------------------------------------------

if __name__ == "__main__":

    from data.ETL.extract import DataExtractor

    datasets = DataExtractor().extract()

    validator = DataValidator(datasets)

    validator.validate()