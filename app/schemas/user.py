from pydantic import EmailStr, Field
from schemas.base import BaseConfigModel
from typing import TYPE_CHECKING, Optional, Annotated
if TYPE_CHECKING:
    from schemas import PropertySchema

class Base(BaseConfigModel):
    name: str
    email: EmailStr
    is_active: Optional[bool] = None
    password: Annotated[str, Field(exclude=True)]  # Exclude from serialization
    
class Create(Base):
    pass

class Update(Base):
    id: int
    
class Read(Base):
    id: int

class ReadFull(Read):
    properties: list['PropertySchema.Read'] = Field(default_factory=list)
