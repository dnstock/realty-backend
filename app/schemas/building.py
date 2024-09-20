from pydantic import Field, StrictInt
from . import BaseConfigModel
if TYPE_CHECKING:
    from schemas import PropertySchema, UnitSchema

class Base(BaseConfigModel):
    name: str
    property_id: int

class Create(Base):
    pass

class Update(Base):
    pass

class Read(Base):
    id: int
    property: 'PropertySchema.Read'

class ReadFull(Read):
    units: list['UnitSchema.Read'] = Field(default_factory=list)
