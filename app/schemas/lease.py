from pydantic import Field
from datetime import date
from typing import TYPE_CHECKING
from .base import BaseModel
from .utils.partial_models import make_partial_model
if TYPE_CHECKING:
    from schemas import UnitSchema, TenantSchema

class Base(BaseModel):
    start_date: date
    end_date: date
    rent: float
    unit_id: int

class Create(Base):
    pass

class Update(make_partial_model(Base)):
    pass

class Read(Base):
    unit: 'UnitSchema.Read'

class ReadFull(Read):
    tenants: list['TenantSchema.Read'] = Field(default_factory=list)
