from sqlalchemy import String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from db import ResourceBase
if TYPE_CHECKING:
    from models import Tenant

class Insurance(ResourceBase):
    __tablename__ = 'insurances'
    _resource_parent = 'tenant'

    provider: Mapped[str] = mapped_column(String, nullable=True)
    policy_type: Mapped[str] = mapped_column(String, nullable=True)  # e.g. Renters, Homeowners, Condo, etc.
    policy_number: Mapped[str] = mapped_column(String)
    premium: Mapped[float] = mapped_column(Float, nullable=True)
    effective_date: Mapped[Date] = mapped_column(Date, nullable=True)
    expiration_date: Mapped[Date] = mapped_column(Date)
    tenant_id: Mapped[int] = mapped_column(ForeignKey('tenants.id'), index=True, nullable=False)

    tenant: Mapped['Tenant'] = relationship(
        'Tenant',
        back_populates='insurances',
        lazy='joined',
    )
