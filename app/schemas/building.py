from pydantic import Field, StrictInt
from . import BaseConfigModel
from typing import TYPE_CHECKING, Annotated
if TYPE_CHECKING:
    from schemas import PropertySchema, UnitSchema

class Base(BaseConfigModel):
    name: str
    unit_count: Annotated[StrictInt, Field(gt=0)]
    property_id: int

class Create(Base):
    pass

class Update(Base):
    id: int

class Read(Base):
    id: int
    property: 'PropertySchema.Read'

class ReadFull(Read):
    units: list['UnitSchema.Read'] = Field(default_factory=list)
