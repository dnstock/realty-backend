from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from db import ResourceBase
if TYPE_CHECKING:
    from models import Tenant

class Insurance(ResourceBase):
    __tablename__ = 'insurances'
    _resource_parent = 'tenant'

    policy_number: Mapped[str] = mapped_column(String, index=True)
    expiration_date: Mapped[Date] = mapped_column(Date)
    tenant_id: Mapped[int] = mapped_column(ForeignKey('tenants.id'))

    tenant: Mapped['Tenant'] = relationship('Tenant', back_populates='insurances')
