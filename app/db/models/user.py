from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from core.types import BooleanInteger
from db import Base
if TYPE_CHECKING:
    from models import Property

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    is_active: Mapped[bool] = mapped_column(BooleanInteger, default=True, nullable=False)

    properties: Mapped[list['Property']] = relationship('Property', back_populates='manager', lazy='select')
