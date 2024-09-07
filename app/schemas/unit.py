from pydantic import BaseModel, ConfigDict
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from schemas import BuildingSchema, LeaseSchema

class Base(BaseModel):
    number: str
    building_id: int

class Create(Base):
    pass

class Update(Base):
    pass

class Read(Base):
    id: int
    building: 'BuildingSchema.Read'
    leases: list['LeaseSchema.Read'] = []

    model_config = ConfigDict(from_attributes=True)
