from pydantic import ConfigDict, BaseModel as PydanticBaseModel
from sqlalchemy.orm import Session
from typing import TYPE_CHECKING, Any, List
from .base import BaseModelConfig
if TYPE_CHECKING:
    from schemas import UserSchema

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

class AllResults(BaseModelConfig):
    rows: List[Any]
    totalCount: int

class PaginatedResults(AllResults):
    pageStart: int
    pageEnd: int
