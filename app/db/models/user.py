from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from sqlalchemy import String
from db import Base
if TYPE_CHECKING:
    from models import Property

class User(Base):
    __tablename__ = 'users'
    _resource_child = 'property'

    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)

    properties: Mapped[list['Property']] = relationship('Property', back_populates='manager', lazy='select')
