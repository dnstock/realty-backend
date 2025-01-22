from pydantic import Field
from .base import BaseModel

# Base class for all resource data models in the application.
class BaseResourceModel(BaseModel):
    owner_id: int
    resource_info: dict[str, str | None] = Field(default_factory=dict)

    def is_owner(self, user_id: int) -> bool:
        return self.owner_id == user_id
