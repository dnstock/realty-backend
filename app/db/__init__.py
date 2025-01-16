from typing import TypeVar
from .base import Base
from .polymorphic import PolymorphicBase
from .session import engine, SessionLocal, get_db
from . import models

# Define a generic type for models
T = TypeVar('T', infer_variance=True, bound=Base)

__all__ = [
    'Base',
    'PolymorphicBase',
    'T',
    'engine',
    'SessionLocal',
    'get_db',
    'models',
]
