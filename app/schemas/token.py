from pydantic import BaseModel, ConfigDict
from typing import Any

class Base(BaseModel):
    access_token: str
    refresh_token: str
    user: dict[str, Any]

class Read(Base):
    model_config = ConfigDict(from_attributes=True)
