from pydantic import Field, StrictInt
from schemas.base import BaseModel, BaseModelWithId
from typing import TYPE_CHECKING, Annotated
if TYPE_CHECKING:
    from schemas import PropertySchema, UnitSchema

class Base(BaseModel):
    name: str
    unit_count: Annotated[StrictInt, Field(gt=0)]
    property_id: int

class Create(Base):
    pass

class Update(Base, BaseModelWithId):
    pass

class Read(Base, BaseModelWithId):
    property: 'PropertySchema.Read'

class ReadFull(Read):
    units: list['UnitSchema.Read'] = Field(default_factory=list)
