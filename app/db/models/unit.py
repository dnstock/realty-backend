from sqlalchemy import Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from db import Base
if TYPE_CHECKING:
    from models import Building, Lease

class Unit(Base):
    __tablename__ = 'units'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    unit_number: Mapped[int] = mapped_column(String, nullable=False)
    floor_number: Mapped[int] = mapped_column(Integer, nullable=False)
    bedrooms: Mapped[int] = mapped_column(Integer)
    bathrooms: Mapped[float] = mapped_column(Float)
    sqft: Mapped[int] = mapped_column(Integer)
    is_vacant: Mapped[bool] = mapped_column(Boolean, index=True, nullable=False, server_default='true')
    building_id: Mapped[int] = mapped_column(ForeignKey('buildings.id'))

    building: Mapped['Building'] = relationship('Building', back_populates='units')
    leases: Mapped[list['Lease']] = relationship('Lease', back_populates='unit')
