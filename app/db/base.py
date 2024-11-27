from sqlalchemy.orm import DeclarativeBase
from typing import TypeVar

# Base class for models
class Base(DeclarativeBase):
    pass

# Define a generic type for models
T = TypeVar('T', bound=Base)
