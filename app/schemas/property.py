from pydantic import Field, constr, field_validator
from schemas.base import BaseConfigModel
from typing import TYPE_CHECKING, Annotated, Literal, Optional
if TYPE_CHECKING:
    from schemas import UserSchema, BuildingSchema

class Base(BaseConfigModel):
    name: str
    address: str
    city: str
    state: Annotated[str, constr(min_length=2, max_length=2, to_upper=True)]
    zip_code: Annotated[str, constr(pattern=r'^\d{5}$')]
    type: Annotated[Literal["commercial", "residential"], constr(to_lower=True)]
    manager_id: Optional[int] = None
    
    @field_validator('type', mode='before')
    def normalize_type(cls, value: str) -> str:
        return value.lower()
    
    @field_validator('city', mode='before')
    def capitalize_city(cls, value: str) -> str:
        return value.capitalize()
    
class Create(Base):
    pass

class Update(Base):
    id: int

class Read(Base):
    id: int
    manager: 'UserSchema.Read'

class ReadFull(Read):
    buildings: list['BuildingSchema.Read'] = Field(default_factory=list)
