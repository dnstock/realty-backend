from datetime import datetime
from pydantic import BaseModel as PydanticBaseModel, ConfigDict, Field
from typing import TypeVar

class BaseModelConfig(PydanticBaseModel):
    model_config = ConfigDict(
        from_attributes = True,
        validate_assignment = True,
        str_strip_whitespace = True,
        str_min_length = 1,
    )

# Metadata for all models
class BaseModel(BaseModelConfig):
    id: int | None = None
    notes: str | None = None
    is_active: bool = True
    is_flagged: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None

    resource_info: dict[str, str | None] = Field(default_factory=dict)

# Generic type for base schemas (e.g. Create schemas)
T = TypeVar('T', infer_variance=True, bound=BaseModel)








