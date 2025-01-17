from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from db import ResourceBase
if TYPE_CHECKING:
    from models import Building

class Property(ResourceBase):
    __tablename__ = 'properties'
    _resource_child = 'building'

    name: Mapped[str] = mapped_column(String, index=True)
    address: Mapped[str] = mapped_column(String, index=True)
    city: Mapped[str] = mapped_column(String, index=True)
    state: Mapped[str] = mapped_column(String, index=True)
    zip_code: Mapped[str] = mapped_column(String, index=True)
    type: Mapped[str] = mapped_column(String, index=True)
    manager: Mapped[str] = mapped_column(String, nullable=True)

    buildings: Mapped[list['Building']] = relationship('Building', back_populates='property')
