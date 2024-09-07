from pydantic import BaseModel, ConfigDict
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from schemas import UserSchema, BuildingSchema

class Base(BaseModel):
    address: str
    city: str
    state: str
    zip_code: str
    manager_id: int

class Create(Base):
    pass

class Update(Base):
    pass

class Read(Base):
    id: int
    manager: 'UserSchema.Read'
    buildings: list['BuildingSchema.Read'] = []

    model_config = ConfigDict(from_attributes=True)
