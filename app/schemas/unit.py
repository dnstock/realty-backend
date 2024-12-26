from pydantic import Field
from typing import TYPE_CHECKING
from .base import BaseModel
from .utils.partial_models import make_partial_model
if TYPE_CHECKING:
    from schemas import BuildingSchema, LeaseSchema

class Base(BaseModel):
    unit_number: str
    floor_number: int
    bedrooms: int
    bathrooms: float
    sqft: int
    is_vacant: bool = True
    building_id: int

class Create(Base):
    pass

class Update(make_partial_model(Base)):
    pass

class Read(Base):
    building: 'BuildingSchema.Read'

class ReadFull(Read):
    leases: list['LeaseSchema.Read'] = Field(default_factory=list)
