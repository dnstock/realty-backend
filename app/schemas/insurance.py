from datetime import date
from . import BaseConfigModel
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from schemas import TenantSchema

class Base(BaseConfigModel):
    policy_number: str
    expiration_date: date
    tenant_id: int

class Create(Base):
    pass

class Update(Base):
    pass

class Read(Base):
    id: int
    tenant: 'TenantSchema.Read'

