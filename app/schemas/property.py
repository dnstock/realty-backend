from typing import TYPE_CHECKING
from pydantic import Field, constr, field_validator
from . import BaseConfigModel
if TYPE_CHECKING:
    from schemas import UserSchema, BuildingSchema

class Base(BaseConfigModel):
    address: str
    city: str
    state: str
    zip_code: str
    manager_id: int

class Create(Base):
    pass

class Update(Base):
    id: int

class Read(Base):
    id: int
    manager: 'UserSchema.Read'

class ReadFull(Read):
    buildings: list['BuildingSchema.Read'] = Field(default_factory=list)
