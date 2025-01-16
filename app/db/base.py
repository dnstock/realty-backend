from datetime import datetime
from sqlalchemy import Integer, String, Boolean, TIMESTAMP, text
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from core import settings

# Base class with metadata for models
class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    is_active: Mapped[bool] = mapped_column(Boolean, index=True, nullable=False, server_default=text('true'))
    is_flagged: Mapped[bool] = mapped_column(Boolean, index=True, nullable=False, server_default=text('false'))
    notes: Mapped[str] = mapped_column(String, nullable=True)
    # Ensure the database always stores timestamps in UTC
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), index=True, nullable=False, server_default=text(settings.database_timestamp_utc)
    )
    # A database trigger will manage this column (defined in /alembic/env.py and handled by Alembic migrations)
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text(settings.database_timestamp_utc)
    )

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
