from pydantic import EmailStr, Field
from schemas.base import BaseModel, BaseModelWithId
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from schemas import PropertySchema

class Base(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(exclude=True)  # Non-serializable
    is_active: bool | None = None

class Create(Base):
    pass

class Update(Base, BaseModelWithId):
    pass

class Read(Base, BaseModelWithId):
    pass

class ReadFull(Read):
    properties: list['PropertySchema.Read'] = Field(default_factory=list)
