from datetime import date
from schemas.base import BaseModel, BaseModelWithId
from typing import TYPE_CHECKING
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

class Read(Base, BaseModelWithId):
    tenant: 'TenantSchema.Read'

class ReadFull(Read):
    pass
