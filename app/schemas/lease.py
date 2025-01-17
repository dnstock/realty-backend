from pydantic import Field
from datetime import date
from typing import TYPE_CHECKING
from .base import ResourceBaseModel
from .utils.partial_models import make_partial_model
if TYPE_CHECKING:
    from schemas import UnitSchema, TenantSchema

class Base(ResourceBaseModel):
    start_date: date
    end_date: date
    rent: float
    deposit: float | None = None
    unit_id: int

class Create(Base):
    pass

class Update(make_partial_model(Base)):
    pass

class Read(Base):
    unit: 'UnitSchema.Read'

class ReadFull(Read):
    tenants: list['TenantSchema.Read'] = Field(default_factory=list)
