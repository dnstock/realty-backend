from pydantic import Field, StrictInt
from typing import TYPE_CHECKING, Annotated
from .resource import BaseResourceModel
from .utils.partial_models import make_partial_model
if TYPE_CHECKING:
    from schemas import PropertySchema, UnitSchema

class Base(BaseResourceModel):
    name: str
    floor_count: Annotated[StrictInt, Field(gt=0)]
    has_elevator: bool = False
    has_pool: bool = False
    has_gym: bool = False
    has_parking: bool = False
    has_doorman: bool = False
    property_id: int

class Create(Base):
    pass

class Update(make_partial_model(Base)):
    pass

class Read(Base):
    unit_count: int
    vacancy: dict[str, float | int] = Field(default_factory=dict)  # count, rate
    occupancy: dict[str, float | int] = Field(default_factory=dict)  # count, rate
    average_stats: dict[str, float] = Field(default_factory=dict)  # sqft, bedrooms, bathrooms, rent

    property: 'PropertySchema.Read'

class ReadFull(Read):
    units: list['UnitSchema.Read'] = Field(default_factory=list)
