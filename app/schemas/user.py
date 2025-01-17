from pydantic import EmailStr, Field, field_validator
from typing import Annotated
from core import security
from .base import BaseModel
from .utils.partial_models import make_partial_model

class Base(BaseModel):
    name: str
    email: EmailStr
    password: Annotated[str, Field(min_length=8)]

    @field_validator('password')
    def hashed_password(cls, password: str) -> str:
        return security.get_password_hash(password)

class Create(Base):
    pass

class Update(make_partial_model(Base)):
    pass

class Read(Base):
    password: Annotated[str, Field(exclude=True)]
