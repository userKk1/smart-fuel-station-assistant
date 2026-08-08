# simulator/ETL/pipeline.py

from extract import DataExtractor
from validate import DataValidator
from transform import DataTransformer
from load import DataLoader


def run_pipeline():

    # Extraction
    datasets = DataExtractor().extract()

    # Validation
    validator = DataValidator(datasets)
    validator.validate()

    # Transformation
    transformer = DataTransformer(datasets)
    datasets = transformer.transform()

    # Chargement dans SQLite
    loader = DataLoader(datasets)
    loader.load()

    print("=" * 50)
    print("PIPELINE ETL TERMINÉ AVEC SUCCÈS")
    print("=" * 50)


if __name__ == "__main__":

    run_pipeline()