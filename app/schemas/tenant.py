from pydantic import EmailStr, Field
from typing import TYPE_CHECKING
from .base import BaseModel
from .utils.partial_models import make_partial_model
if TYPE_CHECKING:
    from schemas import LeaseSchema, InsuranceSchema

class Base(BaseModel):
    name: str
    email: EmailStr | None = None
    phone: str | None = None
    lease_id: int

class Create(Base):
    pass

class Update(make_partial_model(Base)):
    pass

class Read(Base):
    lease: 'LeaseSchema.Read'

class ReadFull(Read):
    insurances: list['InsuranceSchema.Read'] = Field(default_factory=list)
