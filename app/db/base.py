from datetime import datetime
from sqlalchemy import String, TIMESTAMP, text
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from typing import TypeVar
from core.types import BooleanInteger
from core import settings

# Base class with metadata for models
class Base(DeclarativeBase):
    is_active: Mapped[bool] = mapped_column(BooleanInteger, index=True, nullable=False, server_default='1')
    is_flagged: Mapped[bool] = mapped_column(BooleanInteger, index=True, nullable=False, server_default='0')
    notes: Mapped[str] = mapped_column(String, nullable=True)
    # Ensure the database always stores timestamps in UTC
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), index=True, nullable=False, server_default=text(settings.database_timestamp_utc)
    )
    # A database trigger will manage this column (defined in /alembic/env.py and handled by Alembic migrations)
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text(settings.database_timestamp_utc)
    )

# Define a generic type for models
T = TypeVar('T', bound=Base)
