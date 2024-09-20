from typing import Optional, TYPE_CHECKING
from pydantic import EmailStr, Field
from . import BaseConfigModel
if TYPE_CHECKING:
    from schemas import PropertySchema

class Base(BaseConfigModel):
    name: str
    email: EmailStr
    is_active: Optional[bool] = None

class Create(Base):
    password: str

class Update(Base):
    password: Optional[str] = None
    
class Me(Base):  # User details returned to the client (e.g. after login)
    pass

    model_config = ConfigDict(from_attributes=True)

class Read(Base):
    id: int

class ReadFull(Read):
    properties: list['PropertySchema.Read'] = Field(default_factory=list)
