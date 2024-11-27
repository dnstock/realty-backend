from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
from typing import TYPE_CHECKING, Any, List, TypeVar
if TYPE_CHECKING:
    from schemas import UserSchema

class BaseConfigModel(BaseModel):
    model_config = ConfigDict(
        from_attributes = True,
        validate_assignment = True,
        str_strip_whitespace = True,
        str_min_length = 1,
    )

T = TypeVar('T', bound=BaseConfigModel)

class RequestContext(BaseModel):
    current_user: 'UserSchema.Read'
    db: Session

    def get_user_id(self) -> int:
        return self.current_user.id

    def is_user_active(self) -> bool:
        return self.current_user.is_active if self.current_user.is_active else False

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

class AllResults(BaseConfigModel):
    rows: List[Any]
    totalCount: int

class PaginatedResults(AllResults):
    pageStart: int
    pageEnd: int
