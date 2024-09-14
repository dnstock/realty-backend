from pydantic import BaseModel, ConfigDict
from typing import Any

class Base(BaseModel):
    user: dict[str, Any]

class Read(Base):
    model_config = ConfigDict(from_attributes=True)
