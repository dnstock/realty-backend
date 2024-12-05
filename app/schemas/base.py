from pydantic import ConfigDict, BaseModel as PydanticBaseModel
from sqlalchemy.orm import Session
from typing import TYPE_CHECKING, Any, List, TypeVar
if TYPE_CHECKING:
    from schemas import UserSchema

class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        from_attributes = True,
        validate_assignment = True,
        str_strip_whitespace = True,
        str_min_length = 1,
    )

# Generic type for base schemas (e.g. Create schemas)
T = TypeVar('T', bound=BaseModel)

# Generic schema for models with an id
class BaseModelWithId(BaseModel):
    id: int

# Generic type for schemas with an id (e.g. Read and Update schemas)
Tid = TypeVar('Tid', bound=BaseModelWithId)

class RequestContext(PydanticBaseModel):
    current_user: 'UserSchema.Read | None'
    db: Session

    def get_user_id(self) -> int:
        return self.current_user.id if self.current_user else 0

    def is_user_active(self) -> bool:
        return bool(self.current_user and self.current_user.is_active)

    def get_active_user_id(self) -> int:
        return self.get_user_id() if self.is_user_active() else 0

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

class AllResults(BaseModel):
    rows: List[Any]
    totalCount: int

class PaginatedResults(AllResults):
    pageStart: int
    pageEnd: int
