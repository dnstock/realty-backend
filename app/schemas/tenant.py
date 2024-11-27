from pydantic import EmailStr, Field
from schemas.base import BaseModel, BaseModelWithId
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from schemas import LeaseSchema, InsuranceSchema

class Base(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    lease_id: int

class Create(Base):
    pass

class Update(Base, BaseModelWithId):
    pass

class Read(Base, BaseModelWithId):
    lease: 'LeaseSchema.Read'

class ReadFull(Read):
    insurances: list['InsuranceSchema.Read'] = Field(default_factory=list)
