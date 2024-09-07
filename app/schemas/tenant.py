from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from schemas import LeaseSchema, InsuranceSchema

class Base(BaseModel):
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

    model_config = ConfigDict(from_attributes=True)
