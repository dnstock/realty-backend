from pydantic import Field
from .base import BaseModel
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from schemas import UserSchema

# Base class for all resource data models in the application.
class BaseResourceModel(BaseModel):
    owner_id: int
    owner: 'UserSchema.Read'
    resource_info: dict[str, str | None] = Field(default_factory=dict)
