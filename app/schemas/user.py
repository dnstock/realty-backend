from pydantic import EmailStr, Field
from schemas.base import BaseConfigModel
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from schemas import PropertySchema

class Base(BaseConfigModel):
    name: str
    email: EmailStr
    is_active: Optional[bool] = None
    password: str = Field(exclude=True)  # Non-serializable

class Create(Base):
    pass

class Update(Base):
    id: int

class Read(Base):
    id: int

class ReadFull(Read):
    properties: list['PropertySchema.Read'] = Field(default_factory=list)
