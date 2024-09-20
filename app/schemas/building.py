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
    units: list['UnitSchema.Read'] = []

