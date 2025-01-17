from datetime import date
from typing import TYPE_CHECKING
from .base import ResourceBaseModel
from .utils.partial_models import make_partial_model
if TYPE_CHECKING:
    from schemas import TenantSchema

class Base(ResourceBaseModel):
    policy_number: str
    expiration_date: date
    tenant_id: int

class Create(Base):
    pass

class Update(make_partial_model(Base)):
    pass

class Read(Base):
    tenant: 'TenantSchema.Read'

class ReadFull(Read):
    pass
