import json
import os
from pathlib import Path
import pickle

from loguru import logger
from omegaconf import DictConfig, OmegaConf
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
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

    # Now support random forest, gradient boosting and neural network pipelines
    if params.train.pipeline == "random_forest":
        logger.info("Chosen random forest pipeline")
        model = RandomForestClassifier(
            n_estimators=params.train.n_estimators,
            max_depth=params.train.max_depth,
            random_state=seed,
        )
    elif params.train.pipeline == "gradient_boosting":
        logger.info("Chosen gradient boosting pipeline")
        model = GradientBoostingClassifier(
            n_estimators=params.train.n_estimators,
            max_depth=params.train.max_depth,
            random_state=seed,
        )
    elif params.train.pipeline == "neural_network":
        logger.info("Chosen neural network pipeline")
        model = MLPClassifier(
            hidden_layer_sizes=(params.train.x_size, params.train.y_size),
            max_iter=params.train.max_iter,
            random_state=seed,
        )
    else:
        raise ValueError(f"Unsupported pipeline: {params.train.pipeline}")

    # Load data
    processed_data = pd.read_parquet(PROCESSED_DATA_DIR / "processed.parquet")

    # Split train and val
    train_data, val_data = train_test_split(
        processed_data, test_size=test_size, random_state=seed, stratify=processed_data["Survived"]
    )

    # Train model
    y_train = train_data["Survived"]
    y_val = val_data["Survived"]

    features = ["Pclass", "Sex", "SibSp", "Parch"]

    # Final data before train

    X_train = pd.get_dummies(train_data[features])  # noqa: C103
    X_val = pd.get_dummies(val_data[features])  # noqa: C103

    # Model train
    logger.info("Training the model...")
    model.fit(X_train, y_train)
    logger.success("Model training complete.")

    # Model validation
    logger.info("Making predictions on the validation set...")
    predictions = model.predict(X_val)
    probabilities = model.predict_proba(X_val)[:, 1]

    # Calculate metrics
    metrics = {
        "accuracy": accuracy_score(y_val, predictions),
        "f1_score": f1_score(y_val, predictions),
        "roc_auc": roc_auc_score(y_val, probabilities),
        "precision": precision_score(y_val, predictions),
        "recall": recall_score(y_val, predictions),
    }

    # Сохраняем метрики
    os.makedirs(MODELS_DIR, exist_ok=True)
    with open(MODELS_DIR / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f)

    logger.info(f"Metrics: {metrics}")

    # Final predictions for submission
    # TODO load test data
    # logger.info("Making predictions on the test set...")
    # predictions = model.predict(X_test)

    # Save model
    logger.info("Saving the model...")
    save_model(model, MODELS_DIR / "model.pkl")

    test_data = None

    # Save submission
    if test_data is not None:
        output = pd.DataFrame({"PassengerId": test_data.PassengerId, "Survived": predictions})
        output.to_csv(EXTERNAL_DATA_DIR / "submission.csv", index=False)
        logger.success("Final submission was successfully saved!")


@app.command()
def main():
    """Train the ML model."""
    train_model()


if __name__ == "__main__":
    app()
