from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from schemas import PropertySchema

class Base(BaseModel):
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
    properties: list['PropertySchema.Read'] = []

    model_config = ConfigDict(from_attributes=True)
