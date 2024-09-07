from pydantic import BaseModel, ConfigDict, EmailStr
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from schemas import PropertySchema

class Base(BaseModel):
    name: str
    email: EmailStr
    password: str
    is_active: bool = True

class Create(Base):
    pass

class Update(Base):
    pass

class Read(Base):
    id: int
    properties: list['PropertySchema.Read'] = []

    model_config = ConfigDict(from_attributes=True)
