from typing import TypeVar
from .base import Base
from .mixins import CommonMixins
from .resource import ResourceBase
from .polymorphic import PolymorphicBase
from .session import engine, SessionLocal, get_db
from . import mixins
from . import models

# Define a generic type for models
T = TypeVar('T', infer_variance=True, bound=Base)

__all__ = [
    'Base',
    'ResourceBase',
    'CommonMixins',
    'PolymorphicBase',
    'T',
    'engine',
    'SessionLocal',
    'get_db',
    'models',
    'mixins',  # Usage ex: mixins.AutoIdMixin
]
