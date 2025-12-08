from typing import Optional

from pydantic import BaseModel, Field


class RawTitanicRow(BaseModel):
    """
    Schema for a single row in the Titanic dataset.
    """

    PassengerId: int
    Survived: int = Field(..., ge=0, le=1)
    Pclass: int = Field(..., ge=1, le=3)
    Name: str
    Sex: str
    Age: Optional[float]
    SibSp: int
    Parch: int
    Ticket: str
    Fare: float
    Cabin: Optional[str]
    Embarked: Optional[str]


class ProcessedTitanicRow(BaseModel):
    """
    Schema for a single row in the processed Titanic dataset.
    """

    PassengerId: int
    Survived: int
    Pclass: int
    Sex: int
    Age: float
    SibSp: int
    Parch: int
    Fare: float
    Embarked: float
    FamilySize: int
