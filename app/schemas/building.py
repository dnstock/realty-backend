from pydantic import BaseModel, ConfigDict
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from schemas import PropertySchema, UnitSchema

class Base(BaseModel):
    name: str
    property_id: int

class Create(Base):
    pass

class Update(Base):
    pass

class Read(Base):
    id: int
    property: 'PropertySchema.Read'
    units: list['UnitSchema.Read'] = []

    model_config = ConfigDict(from_attributes=True)
