from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

# Base class for all polymorphic tables in the database.

# Example usage:
#
# class Vehicle(BaseInheritance):
#     __tablename__ = 'vehicles'
#     __mapper_args__ = {'polymorphic_identity': 'vehicle'}
#     id: Mapped[int] = mapped_column(primary_key=True)
#     make: Mapped[str]
#     model: Mapped[str]
#
# class Car(Vehicle):
#     __mapper_args__ = {'polymorphic_identity': 'car'}
#     doors: Mapped[int]
#
# class Motorcycle(Vehicle):
#     __mapper_args__ = {'polymorphic_identity': 'motorcycle'}
#     has_sidecar: Mapped[bool]
#

class PolymorphicBase(Base):
    __abstract__ = True

    type: Mapped[str] = mapped_column(String, index=True, nullable=False)
    __mapper_args__ = {'polymorphic_on': type}
