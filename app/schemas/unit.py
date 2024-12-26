from pydantic import Field
from typing import TYPE_CHECKING
from .base import BaseModel
if TYPE_CHECKING:
    from schemas import BuildingSchema, LeaseSchema

class Base(BaseModel):
    number: str
    building_id: int

class Create(Base):
    pass

class Update(Base, BaseModelWithId):
    pass

class Read(Base):
    building: 'BuildingSchema.Read'

class ReadFull(Read):
    leases: list['LeaseSchema.Read'] = Field(default_factory=list)
