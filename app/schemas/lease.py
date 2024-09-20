from pydantic import Field
from datetime import date
from . import BaseConfigModel
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from schemas import UnitSchema, TenantSchema

class Base(BaseConfigModel):
    start_date: date
    end_date: date
    unit_id: int

class Create(Base):
    pass

class Update(Base):
    pass

class Read(Base):
    id: int
    unit: 'UnitSchema.Read'

class ReadFull(Read):
    tenants: list['TenantSchema.Read'] = Field(default_factory=list)
