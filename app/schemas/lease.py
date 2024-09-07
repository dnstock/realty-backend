from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from schemas import UnitSchema, TenantSchema

class Base(BaseModel):
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
    tenants: list['TenantSchema.Read'] = []

    model_config = ConfigDict(from_attributes=True)
