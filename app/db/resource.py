from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from functools import cached_property
from .base import Base
from .mixins import CommonMixins

# Base class for all resource tables in the database.
class ResourceBase(CommonMixins, Base):
    __abstract__ = True

    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True, nullable=False)

    _resource_parent: str | None = None
    _resource_child: str | None = None

    @cached_property
    def _resource(self) -> str:
        return self.__class__.__module__.lower().split('.')[-1]

    @cached_property
    def resource_info(self) -> dict[str, str | None]:
        return {
            'name': self._resource,
            'parent': self._resource_parent,
            'child': self._resource_child,
            '__table__': self.__tablename__,
        }
