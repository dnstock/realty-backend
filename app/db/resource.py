from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

# Base class for all resource tables in the database.
class ResourceBase(Base):
    __abstract__ = True

    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True, nullable=False)

    _resource_parent: str | None = None
    _resource_child: str | None = None

    @property
    def _resource(self) -> str:
        return self.__class__.__module__.lower().split('.')[-1]

    @property
    def resource_info(self) -> dict[str, str | None]:
        return {
            'name': self._resource,
            'parent': self._resource_parent,
            'child': self._resource_child,
            '__table__': self.__tablename__,
        }
