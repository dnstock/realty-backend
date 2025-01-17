from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from db import ResourceBase
if TYPE_CHECKING:
    from models import Property, Unit

class Building(ResourceBase):
    __tablename__ = 'buildings'
    _resource_parent = 'property'
    _resource_child = 'unit'

    name: Mapped[str] = mapped_column(String)
    floor_count: Mapped[int] = mapped_column(Integer)
    has_elevator: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default='false')
    has_pool: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default='false')
    has_gym: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default='false')
    has_parking: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default='false')
    has_doorman: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default='false')
    property_id: Mapped[int] = mapped_column(ForeignKey('properties.id'), index=True, nullable=False)

    property: Mapped['Property'] = relationship('Property', back_populates='buildings')
    units: Mapped[list['Unit']] = relationship('Unit', back_populates='building')
