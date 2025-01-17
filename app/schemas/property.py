from pydantic import Field, constr, field_validator
from typing import TYPE_CHECKING, Annotated, Literal
from .base import BaseModel
from .utils.partial_models import make_partial_model
if TYPE_CHECKING:
    from schemas import BuildingSchema

class Base(BaseModel):
    name: str
    address: str
    city: str
    state: Annotated[str, constr(min_length=2, max_length=2, to_upper=True)]
    zip_code: Annotated[str, constr(pattern=r'^\d{5}$')]
    type: Annotated[Literal['commercial', 'residential'], constr(to_lower=True)]
    manager: str | None

    @field_validator('type', mode='before')
    def normalize_type(cls, value: str) -> str:
        return value.lower()

    @field_validator('city', mode='before')
    def capitalize_city(cls, value: str) -> str:
        return value.capitalize()

class Create(Base):
    pass

class Update(make_partial_model(Base)):
    pass

class Read(Base):
    pass

class ReadFull(Read):
    buildings: list['BuildingSchema.Read'] = Field(default_factory=list)
