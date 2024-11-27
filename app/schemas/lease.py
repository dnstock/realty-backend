from pydantic import Field
from datetime import date
from schemas.base import BaseModel, BaseModelWithId
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from schemas import UnitSchema, TenantSchema

class Base(BaseModel):
    start_date: date
    end_date: date
    unit_id: int

class Create(Base):
    pass

class Update(Base, BaseModelWithId):
    pass

class Read(Base, BaseModelWithId):
    unit: 'UnitSchema.Read'

class ReadFull(Read):
    tenants: list['TenantSchema.Read'] = Field(default_factory=list)
