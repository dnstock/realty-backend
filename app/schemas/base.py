from datetime import datetime
from pydantic import ConfigDict, BaseModel as PydanticBaseModel
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
    notes: str | None
    is_active: bool
    is_flagged: bool
    created_at: datetime
    updated_at: datetime
    id: int | None = None


# Generic type for base schemas (e.g. Create schemas)
T = TypeVar('T', infer_variance=True, bound=BaseModel)








