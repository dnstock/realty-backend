from sqlalchemy import Date, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from db import ResourceBase
if TYPE_CHECKING:
    from models import Unit, Tenant

class Lease(ResourceBase):
    __tablename__ = 'leases'
    _resource_parent = 'unit'
    _resource_child = 'tenant'

    start_date: Mapped[Date] = mapped_column(Date)
    end_date: Mapped[Date] = mapped_column(Date)
    rent: Mapped[float] = mapped_column(Float)
    deposit: Mapped[float] = mapped_column(Float, nullable=True)
    unit_id: Mapped[int] = mapped_column(ForeignKey('units.id'), index=True, nullable=False)

    unit: Mapped['Unit'] = relationship(
        'Unit',
        back_populates='leases',
        lazy='joined',
    )
    tenants: Mapped[list['Tenant']] = relationship(
        'Tenant',
        back_populates='lease',
        lazy='selectin',
    )
