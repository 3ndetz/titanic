import os
from pathlib import Path
import pickle

from loguru import logger
from omegaconf import DictConfig, OmegaConf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import typer

from titanic.config import EXTERNAL_DATA_DIR, MODELS_DIR, PROCESSED_DATA_DIR, PROJ_ROOT

app = typer.Typer()


def load_params(params_path: Path = Path(PROJ_ROOT / "params.yaml")) -> DictConfig:
    """Load parameters from a YAML file using OmegaConf."""
    return OmegaConf.load(params_path)


def save_model(model, model_path: Path):
    """Saves the trained model to a file."""
    os.makedirs(Path(model_path).parent, exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(model, f)


def load_saved_model(model_path: Path) -> RandomForestClassifier:
    """Loads a saved model from a file."""
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model


def train_model():
    """
    Train a machine learning model based on the provided parameters.
    """
    # Load experiment params
    params = load_params()

    # Universal params
    seed = params.train.seed
    test_size = params.train.test_size

    # Now support only random forest pipeline
    if params.train.pipeline == "random_forest":
        logger.info("Chosen random forest pipeline")
    else:
        raise ValueError(f"Unsupported pipeline: {params.train.pipeline}")

    n_estimators = params.train.n_estimators
    max_depth = params.train.max_depth

    # Load data
    processed_data = pd.read_parquet(PROCESSED_DATA_DIR / "processed.parquet")

    # Split train and val

    train_data, test_data = train_test_split(
        processed_data, test_size=test_size, random_state=seed
    )

    # Train model
    y = train_data["Survived"]

    features = ["Pclass", "Sex", "SibSp", "Parch"]

    # Final data before train
    X = pd.get_dummies(train_data[features])  # noqa: C103
    X_test = pd.get_dummies(test_data[features])  # noqa: C103

    # Model init
    model = RandomForestClassifier(
        n_estimators=n_estimators, max_depth=max_depth, random_state=seed
    )

    # Model train
    logger.info("Training the model...")
    model.fit(X, y)

    # Inference
    logger.info("Making predictions on the test set...")
    predictions = model.predict(X_test)

    # Save model
    logger.info("Saving the model...")
    save_model(model, MODELS_DIR / "model.pkl")

    # Save submission
    output = pd.DataFrame({"PassengerId": test_data.PassengerId, "Survived": predictions})
    output.to_csv(EXTERNAL_DATA_DIR / "submission.csv", index=False)
    logger.success("Final submission was successfully saved!")


@app.command()
def main():
    """Train the ML model."""
    train_model()


if __name__ == "__main__":
    app()
