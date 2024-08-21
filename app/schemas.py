from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date

## Token

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    email: Optional[str] = None

## User

class UserBase(BaseModel):
    name: str
    email: str
    password: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int
    properties: List['Property'] = []

    model_config = ConfigDict(from_attributes=True)

## Property

class PropertyBase(BaseModel):
    address: str
    city: str
    state: str
    zip_code: str
    manager_id: int

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(PropertyBase):
    pass

class Property(PropertyBase):
    id: int
    manager: User
    buildings: List['Building'] = []

    model_config = ConfigDict(from_attributes=True)

## Building

class BuildingBase(BaseModel):
    name: str
    property_id: int

class BuildingCreate(BuildingBase):
    pass

class BuildingUpdate(BuildingBase):
    pass

class Building(BuildingBase):
    id: int
    property: Property
    units: List['Unit'] = []

    model_config = ConfigDict(from_attributes=True)

## Unit

class UnitBase(BaseModel):
    number: str
    building_id: int

class UnitCreate(UnitBase):
    pass

class UnitUpdate(UnitBase):
    pass

class Unit(UnitBase):
    id: int
    building: Building
    leases: List['Lease'] = []

    model_config = ConfigDict(from_attributes=True)

## Lease

class LeaseBase(BaseModel):
    start_date: date
    end_date: date
    unit_id: int

class LeaseCreate(LeaseBase):
    pass

class LeaseUpdate(LeaseBase):
    pass

class Lease(LeaseBase):
    id: int
    unit: Unit
    tenants: List['Tenant'] = []

    model_config = ConfigDict(from_attributes=True)

## Tenant

class TenantBase(BaseModel):
    name: str
    email: str
    phone: str
    lease_id: int

class TenantCreate(TenantBase):
    pass

class TenantUpdate(TenantBase):
    pass

class Tenant(TenantBase):
    id: int
    lease: Lease
    insurances: List['Insurance'] = []

    model_config = ConfigDict(from_attributes=True)

## Insurance

class InsuranceBase(BaseModel):
    policy_number: str
    expiration_date: date
    tenant_id: int

class InsuranceCreate(InsuranceBase):
    pass

class InsuranceUpdate(InsuranceBase):
    pass

class Insurance(InsuranceBase):
    id: int
    tenant: Tenant

    model_config = ConfigDict(from_attributes=True)
