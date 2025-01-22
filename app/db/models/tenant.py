from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from db import ResourceBase
if TYPE_CHECKING:
    from models import Lease, Insurance

class Tenant(ResourceBase):
    __tablename__ = 'tenants'
    _resource_parent = 'lease'
    _resource_child = 'insurance'

    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    lease_id: Mapped[int] = mapped_column(ForeignKey('leases.id'), index=True, nullable=False)

    lease: Mapped['Lease'] = relationship(
        'Lease',
        back_populates='tenants',
        lazy='joined',
    )
    insurances: Mapped[list['Insurance']] = relationship(
        'Insurance',
        back_populates='tenant',
        lazy='selectin',
    )
