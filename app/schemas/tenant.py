from pydantic import EmailStr, Field
from schemas.base import BaseConfigModel
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
    id: int

class Read(Base):
    id: int
    lease: 'LeaseSchema.Read'

class ReadFull(Read):
    insurances: list['InsuranceSchema.Read'] = Field(default_factory=list)
