"""Test for pydantic library."""

from pydantic import ValidationError
from pydantic import BaseModel, PositiveInt
from datetime import datetime


class User(BaseModel):
    """User model."""

    id: int
    name: str = "John Doe"
    signup_ts: datetime | None
    tastes: dict[str, PositiveInt]


external_data = {
    "id": 1,
    "signup_ts": "2024-06-01T12:00:00",
    "tastes": {"music": 10, "movies": 5},
}

user = User(**external_data)
print(user.id)
print(user.model_dump())
print(user.model_dump_json())

# If validation fails, Pydantic will raise an error

external_data = {"id": "not and int", "tastes": {}}

try:
    user = User(**external_data)
except ValidationError as e:
    print(e.errors())

from typing import Annotated, Literal
from annotated_types import Gt


def pl():
    """Print line."""
    print("=====" * 20)


class Fruit(BaseModel):
    """Fruit model."""

    name: str
    color: Literal["red", "green"]
    weight: Annotated[float, Gt(0)]
    bazam: dict[str, list[tuple[int, bool, float]]]


pl()

print(
    Fruit(
        name="apple",
        color="red",
        weight=100,
        bazam={"apple": [(1, True, 1.0)]},
    )
)
