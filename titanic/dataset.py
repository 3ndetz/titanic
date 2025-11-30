from pathlib import Path

from loguru import logger
import pandas as pd
import pandera as pa
from tqdm import tqdm
import typer
import yaml

from titanic.config import PROCESSED_DATA_DIR, RAW_DATA_DIR
from titanic.schema.dataset_schema import TitanicRow


def load_csv(path):
    """For loading raw csv dataset."""
    return pd.read_csv(path)


def load_metadata(yaml_path):
    """For loading metadata from a yaml file."""
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["columns"]


def check_structure(df, metadata):
    """Checks if dataframe structure matches the metadata."""
    missing = [col for col in metadata if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    # Проверка типов и допустимых значений
    for col, props in metadata.items():
        if "values" in props:
            valid_values = props["values"]
            invalid = df[col].apply(lambda x: x is not None and x not in valid_values)
            if invalid.any():
                logger.error(f"Invalid values in column {col}: {df.loc[invalid, col].unique()}")


def validate_rows(df) -> list[tuple[int, str]]:
    """Validates each row against the TitanicRow schema."""
    errors = []
    for idx, row in tqdm(df.iterrows()):
        try:
            TitanicRow(**row.to_dict())
        except Exception as e:
            errors.append((idx, str(e)))
    return errors


def validate_dataset(df: pd.DataFrame) -> bool:
    """
    Validates the Titanic dataset against the schema and metadata.

    Returns:
        True if valid, False otherwise.
    """
    df = df.where(pd.notnull(df), None)  # fix nan to None for pydantic
    metadata = load_metadata(RAW_DATA_DIR / "train_metadata.yaml")
    check_structure(df, metadata)
    errors = validate_rows(df)
    print(df.head())
    if errors:
        logger.info("Validation errors found:")
        for idx, err in errors:
            logger.info(f"Row {idx}: {err}")
    else:
        logger.info("All rows are valid.")
    return not errors


def generate_yaml_schema(df: pd.DataFrame, output_path: Path) -> None:
    """
    Generates a YAML schema for the processed dataset.
    """
    schema = pa.infer_schema(df)
    output_yaml_path = str(output_path).replace(".parquet", "_metadata.yaml")
    schema.to_yaml(output_yaml_path)


def process_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processsing the Titanic dataset - cleaning and feature engineering
    """
    # Пример обработки: заполнение пропущенных значений в 'Age' медианой
    num_cols = df.select_dtypes(include="number").columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    # Заполняем пропуски
    num_cols = df.select_dtypes(include="number").columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].fillna("")

    # Encode Sex
    df["Sex"] = df["Sex"].map({"male": 0, "female": 1})

    # Encode Embarked
    embarked_map = {"C": 0, "Q": 1, "S": 2}
    df["Embarked"] = df["Embarked"].map(embarked_map).fillna(-1)

    # Create family size feature
    df["FamilySize"] = df["SibSp"] + df["Parch"]

    # Drop columns not needed for modeling
    df = df.drop(columns=["Ticket", "Name", "Cabin"])

    return df


def save_dataset(df: pd.DataFrame, output_path: Path) -> None:
    """Saves the processed dataset to a parquet file."""
    df.to_parquet(output_path)


def prepare_dataset(
    input_path,
    output_path,
) -> None:
    """
    Process the Titanic dataset.
    """
    logger.info("Starting dataset preparation...")

    logger.info(f"Loading dataset from {input_path}...")
    df = load_csv(input_path)
    logger.info("Validating dataset...")
    if not validate_dataset(df):
        logger.error("Validation failed. Check the input data and schemas.")
        return
    logger.success("Validation successful.")

    logger.info("Processing dataset...")
    df = process_dataset(df)
    logger.success("Dataset processing complete.")

    logger.info(f"Saving processed dataset to {output_path}...")
    save_dataset(df, output_path)
    generate_yaml_schema(df, output_path)

    logger.success("Preparing dataset complete.")


app = typer.Typer()


@app.command()
def main(
    input_path: Path = RAW_DATA_DIR / "train.csv",
    output_path: Path = PROCESSED_DATA_DIR / "processed.parquet",
):
    """
    Process the Titanic dataset.
    """
    prepare_dataset(input_path, output_path)


if __name__ == "__main__":
    app()
