from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
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

    @hybrid_property
    def unit_count(self) -> int:
        return len(self.units)

    @hybrid_property
    def vacant_units(self) -> int:
        return self.unit_count - sum(1 for unit in self.units if not unit.is_vacant)

    @hybrid_property
    def vacancy_rate(self) -> float:
        return self.vacant_units / self.unit_count if self.unit_count else 0.0

    @hybrid_property
    def vacancy(self) -> dict[str, float | int]:
        return {
            'count': self.vacant_units,
            'rate': self.vacancy_rate,
        }

    @hybrid_property
    def occupied_units(self) -> int:
        return self.unit_count - self.vacant_units

    @hybrid_property
    def occupancy_rate(self) -> float:
        return self.occupied_units / self.unit_count if self.unit_count else 0.0

    @hybrid_property
    def occupancy(self) -> dict[str, float | int]:
        return {
            'count': self.occupied_units,
            'rate': self.occupancy_rate,
        }

    @hybrid_property
    def average_sqft(self) -> float:
        return sum(unit.sqft for unit in self.units) / self.unit_count if self.unit_count else 0.0

    @hybrid_property
    def average_bedrooms(self) -> float:
        return sum(unit.bedrooms for unit in self.units) / self.unit_count if self.unit_count else 0.0

    @hybrid_property
    def average_bathrooms(self) -> float:
        return sum(unit.bathrooms for unit in self.units) / self.unit_count if self.unit_count else 0.0

    @hybrid_property
    def average_rent(self) -> float:
        return sum(lease.rent for unit in self.units for lease in unit.leases) / self.unit_count if self.unit_count else 0.0
