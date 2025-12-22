from typing import Literal, Union

from pydantic import BaseModel, Field


class RandomForestConfig(BaseModel):
    """Конфиг для Random Forest"""

    n_estimators: int = Field(default=10, gt=0)
    max_depth: int = Field(default=5, gt=0)
    test_size: float = Field(default=0.1, gt=0, lt=1)
    seed: int = Field(default=1, ge=0)
    pipeline: Literal["random_forest"] = "random_forest"


class GradientBoostingConfig(BaseModel):
    """Конфиг для Gradient Boosting"""

    n_estimators: int = Field(default=10, gt=0)
    max_depth: int = Field(default=5, gt=0)
    test_size: float = Field(default=0.1, gt=0, lt=1)
    seed: int = Field(default=1, ge=0)
    pipeline: Literal["gradient_boosting"] = "gradient_boosting"


class NeuralNetworkConfig(BaseModel):
    """Конфиг для Neural Network"""

    x_size: int = Field(default=150, gt=0)
    y_size: int = Field(default=100, gt=0)
    max_iter: int = Field(default=1000, gt=0)
    test_size: float = Field(default=0.1, gt=0, lt=1)
    seed: int = Field(default=1, ge=0)
    pipeline: Literal["neural_network"] = "neural_network"


# Union type для выбора нужного конфига
# (будет пытаться валидировать по очереди, долго но достоверно)
TrainConfig = Union[RandomForestConfig, GradientBoostingConfig, NeuralNetworkConfig]


class Config(BaseModel):
    """Абстраткный конфиг проекта titanic"""

    train: TrainConfig
