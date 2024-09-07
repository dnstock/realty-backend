from sqlalchemy import Integer, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from db import Base
if TYPE_CHECKING:
    from models import Unit, Tenant

class Lease(Base):
    __tablename__ = "leases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    start_date: Mapped[Date] = mapped_column(Date)
    end_date: Mapped[Date] = mapped_column(Date)
    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"))

    unit: Mapped["Unit"] = relationship("Unit", back_populates="leases")
    tenants: Mapped[list["Tenant"]] = relationship("Tenant", back_populates="lease")
