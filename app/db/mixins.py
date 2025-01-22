from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, String, TIMESTAMP, text, Integer
from datetime import datetime
from typing import Optional
from core import settings

class AutoIdMixin:
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

class TimestampMixin:
    # Ensure the database always stores timestamps in UTC
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text(settings.database_timestamp_utc)
    )
    # This column is managed by a database trigger and handled by db migrations (defined in /alembic/env.py)
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text(settings.database_timestamp_utc)
    )

class ActiveFlaggedMixin:
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    is_flagged: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

class NotesMixin:
    notes: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )

class CommonMixins(AutoIdMixin, TimestampMixin, ActiveFlaggedMixin, NotesMixin):
    pass
