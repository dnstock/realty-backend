from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from db import Base
if TYPE_CHECKING:
    from models import Lease, Insurance

class Tenant(Base):
    __tablename__ = 'tenants'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, index=True, unique=True)
    phone: Mapped[str] = mapped_column(String, index=True)
    lease_id: Mapped[int] = mapped_column(ForeignKey('leases.id'))

    lease: Mapped['Lease'] = relationship('Lease', back_populates='tenants')
    insurances: Mapped[list['Insurance']] = relationship('Insurance', back_populates='tenant')
