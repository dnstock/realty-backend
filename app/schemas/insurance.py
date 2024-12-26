from datetime import date
from typing import TYPE_CHECKING
from .base import BaseModel
if TYPE_CHECKING:
    from schemas import TenantSchema

class Base(BaseModel):
    policy_number: str
    expiration_date: date
    tenant_id: int

class Create(Base):
    pass

class Update(Base, BaseModelWithId):
    pass

class Read(Base):
    tenant: 'TenantSchema.Read'

class ReadFull(Read):
    pass
