from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from functools import cached_property
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

    property: Mapped['Property'] = relationship(
        'Property',
        back_populates='buildings',
        lazy='dynamic',
    )
    units: Mapped[list['Unit']] = relationship(
        'Unit',
        back_populates='building',
        lazy='dynamic',
    )

    @cached_property
    def unit_count(self) -> int:
        return len(self.units)

    @cached_property
    def vacant_unit_count(self) -> int:
        return sum(1 for unit in self.units if unit.is_vacant)

    @cached_property
    def vacancy(self) -> dict[str, float | int]:
        return {
            'units': self.vacant_unit_count,
            'rate': self.vacant_unit_count / self.unit_count if self.unit_count else 0.0
        }

    @cached_property
    def occupancy(self) -> dict[str, float | int]:
        occupied = self.unit_count - self.vacant_unit_count
        return {
            'units': occupied,
            'rate': occupied / self.unit_count if self.unit_count else 0.0
        }

    @cached_property
    def average_stats(self) -> dict[str, float]:
        if not self.unit_count:
            return {'sqft': 0.0, 'bedrooms': 0.0, 'bathrooms': 0.0, 'rent': 0.0}

        active_units = [u for u in self.units if u.is_active]
        if not active_units:
            return {'sqft': 0.0, 'bedrooms': 0.0, 'bathrooms': 0.0, 'rent': 0.0}

        unit_count = len(active_units)
        return {
            'sqft': sum(u.sqft for u in active_units) / unit_count,
            'bedrooms': sum(u.bedrooms for u in active_units) / unit_count,
            'bathrooms': sum(u.bathrooms for u in active_units) / unit_count,
            'rent': sum(l.rent for u in active_units for l in u.leases if l.is_active) / unit_count
        }
