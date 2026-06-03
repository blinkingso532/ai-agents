"""Test Demo."""


class TestClass:
    """Test Class"""

    def test_one(self):
        """Test one."""
        x = "this"
        assert "h" in x

    def test_two(self):
        """Test two."""
        x = "Hello"
        assert hasattr(x, "check")


from dataclasses import dataclass
from typing import Annotated, Generic, override

from pydantic import BaseModel


class DataModel(BaseModel):
    number: int


class Response[DataT](BaseModel):
    data: DataT


# Generic test.
@dataclass
class Request[ReqDataT]:
    nonce_str: str
    timestamp: int
    data: ReqDataT

    @override
    def __str__(self) -> str:
        return f"Request(nonce_str={self.nonce_str}, timestamp={self.timestamp}, data={self.data})"


def test_request():
    """Test request."""
    request = Request[str](nonce_str="123", timestamp=1694502400, data="hello")
    print(str(request))


def test_response():
    """Test response."""
    data = DataModel(number=100)
    response = Response(data=data)
    assert response.data.number == 100


from typing import TypeVar

T = TypeVar("T")
F = TypeVar("F")
Q = TypeVar("Q")


class BaseClass(BaseModel, Generic[T, F]):
    x: T
    y: F


class ChildClass(BaseClass[int, F], Generic[F, Q]):
    z: Q


def test_generic():
    """Test generic."""
    child = ChildClass[str, int](x=1, y="hello", z=100)
    print(child.model_dump_json())
    assert child.z == 100


# Parametrized generic models as types in other models
class ResponseModel(BaseModel, Generic[T]):
    content: T


class Product(BaseModel):
    name: str
    price: float


class Order(BaseModel):
    id: int
    product: ResponseModel[Product]


def test_parametrized_generic():
    product = Product(name="apple", price=0.5)
    response = ResponseModel[Product](content=product)
    order = Order(id=1, product=response)
    order.model_dump_json()
    assert order.product.content.name == "apple"
    assert order.product.content.price == 0.5
    print(repr(order))


from pydantic import ValidationError


class InnerT(BaseModel, Generic[T]):
    inner: T


class OuterT(BaseModel, Generic[T]):
    outer: T
    nested: InnerT[T]


def test_nested_generic():
    nested = InnerT[int](inner=1)
    print(OuterT[int](outer=1, nested=nested))
    try:
        print(OuterT[int](outer="a", nested=InnerT[int](inner=2)))
    except ValidationError as e:
        print(e)


# Advanced example
from pydantic import Field, PrivateAttr, create_model

DynamicModel = create_model(
    "DynamicModel",
    foo=(str, Field(description="The foo field", alias="FOO")),
    bar=Annotated[str, Field(description="Bar Field")],
    _private=(int, PrivateAttr(default=1)),
    __config__={"populate_by_name": True},
)


class StaticModel(BaseModel):
    foo: str = Field(alias="FOO")
    bar: Annotated[str, Field(description="Bar Field")]
    _private: int = PrivateAttr(default=1)


def test_dynamic_model():
    """Test dynamic model."""
    dynamic_model = DynamicModel(FOO="hello", bar="world")
    dynamic_model = DynamicModel(foo="hello", bar="world")
    print(dynamic_model.model_dump_json())
    assert "foo" in dynamic_model.__class__.model_fields.keys()
