from pydantic import BaseModel, ConfigDict
from typing import Any, List, TypeVar

class BaseConfigModel(BaseModel):
    model_config = ConfigDict(
        from_attributes = True,
        validate_assignment = True,
        str_strip_whitespace = True,
        str_min_length = 1,
    )
    
class AllResults(BaseConfigModel):
    rows: List[Any]
    totalCount: int

class PaginatedResults(AllResults):
    pageStart: int
    pageEnd: int

T = TypeVar('T', bound=BaseConfigModel)
