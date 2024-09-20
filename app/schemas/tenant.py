from pydantic import EmailStr, Field
from . import BaseConfigModel
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from schemas import LeaseSchema, InsuranceSchema

class Base(BaseConfigModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    lease_id: int

class Create(Base):
    pass

class Update(Base):
    pass

class Read(Base):
    id: int
    lease: 'LeaseSchema.Read'
    insurances: list['InsuranceSchema.Read'] = []

