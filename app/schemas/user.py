from pydantic import EmailStr, Field
from schemas.base import BaseModel, BaseModelWithId
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from schemas import PropertySchema

class Base(BaseModel):
    name: str
    email: EmailStr
    is_active: Optional[bool] = None
    password: str = Field(exclude=True)  # Non-serializable

class Create(Base):
    pass

class Update(Base, BaseModelWithId):
    pass

class Read(Base, BaseModelWithId):
    pass

class ReadFull(Read):
    properties: list['PropertySchema.Read'] = Field(default_factory=list)
