from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    properties = relationship("Property", back_populates="manager")

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    city = Column(String, index=True)
    state = Column(String, index=True)
    zip_code = Column(String, index=True)
    manager_id = Column(Integer, ForeignKey("users.id"))

    manager = relationship("User", back_populates="properties")
    buildings = relationship("Building", back_populates="property")

class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))

    property = relationship("Property", back_populates="buildings")
    units = relationship("Unit", back_populates="building")

class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, index=True)
    building_id = Column(Integer, ForeignKey("buildings.id"))

    building = relationship("Building", back_populates="units")
    leases = relationship("Lease", back_populates="unit")

class Lease(Base):
    __tablename__ = "leases"

    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date)
    end_date = Column(Date)
    unit_id = Column(Integer, ForeignKey("units.id"))

    unit = relationship("Unit", back_populates="leases")
    tenants = relationship("Tenant", back_populates="lease")

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True)
    lease_id = Column(Integer, ForeignKey("leases.id"))

    lease = relationship("Lease", back_populates="tenants")
    insurances = relationship("Insurance", back_populates="tenant")

class Insurance(Base):
    __tablename__ = "insurances"

    id = Column(Integer, primary_key=True, index=True)
    policy_number = Column(String, index=True)
    expiration_date = Column(Date)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))

    tenant = relationship("Tenant", back_populates="insurances")
    