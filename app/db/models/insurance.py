from sqlalchemy import Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from db import Base
if TYPE_CHECKING:
    from models import Tenant

class Insurance(Base):
    __tablename__ = 'insurances'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    policy_number: Mapped[str] = mapped_column(String, index=True)
    expiration_date: Mapped[Date] = mapped_column(Date)
    tenant_id: Mapped[int] = mapped_column(ForeignKey('tenants.id'))

    tenant: Mapped['Tenant'] = relationship('Tenant', back_populates='insurances')
