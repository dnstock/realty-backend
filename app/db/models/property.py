from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from db import ResourceBase
if TYPE_CHECKING:
    from models import User, Building

class Property(ResourceBase):
    __tablename__ = 'properties'
    _resource_parent = 'manager'
    _resource_child = 'building'

    name: Mapped[str] = mapped_column(String, index=True)
    address: Mapped[str] = mapped_column(String, index=True)
    city: Mapped[str] = mapped_column(String, index=True)
    state: Mapped[str] = mapped_column(String, index=True)
    zip_code: Mapped[str] = mapped_column(String, index=True)
    type: Mapped[str] = mapped_column(String, index=True)
    manager_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True, nullable=False)

    manager: Mapped['User'] = relationship('User', back_populates='properties')
    buildings: Mapped[list['Building']] = relationship('Building', back_populates='property')
