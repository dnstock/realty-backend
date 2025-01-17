from datetime import date
from typing import TYPE_CHECKING
from .resource import BaseResourceModel
from .utils.partial_models import make_partial_model
if TYPE_CHECKING:
    from schemas import TenantSchema

class Base(BaseResourceModel):
    provider: str | None = None
    policy_type: str | None = None
    policy_number: str
    premium: float | None = None
    effective_date: date | None = None
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
