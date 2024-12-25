from pydantic import Field
from datetime import date
from typing import TYPE_CHECKING
from .base import BaseModel, BaseModelWithId
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
