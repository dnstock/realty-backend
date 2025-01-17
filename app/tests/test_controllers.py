from typing import no_type_check
import pytest, uuid
from pathlib import Path
from pydantic import ValidationError
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from core import security
from db import Base
from controllers import (
    UserController,
    PropertyController,
    BuildingController,
    UnitController,
    LeaseController,
    TenantController,
    InsuranceController,
)
from schemas import (
    UserSchema,
    PropertySchema,
    BuildingSchema,
    UnitSchema,
    LeaseSchema,
    TenantSchema,
    InsuranceSchema,
)

@pytest.fixture(scope='module')
def test_db_sqlite():
    db_name = 'test.db'
    engine = create_engine(f'sqlite:///./{db_name}')  # Use an in-memory database
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)  # Create all the tables
    db = TestingSessionLocal()
    try:
        yield db  # Run the test
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        if Path(db_name).exists():
            Path(db_name).unlink()  # Remove the database file

@pytest.fixture(scope='module')
def test_db():
    engine = create_engine('postgresql+psycopg://admin:admin@localhost/realty_test')
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

# Generate a unique email addresses
def generate_test_email():
    return f'test_{uuid.uuid4()}@example.com'

## SCHEMAS

schema_user_create = UserSchema.Create(
    name='Test User',
    email=generate_test_email(),
    password='test1234#$',
    is_active=True,
)
schema_property_create = PropertySchema.Create(
    name='Property 1',
    address='123 Main St',
    city='Springfield',
    state='IL',
    zip_code='62701',
    type='residential',
    manager='John Doe',
)
schema_building_create = BuildingSchema.Create(
    name='Building 1',
    unit_count=10,
    floor_count=5,
    has_elevator=True,
    has_pool=False,
    has_gym=True,
    has_parking=True,
    has_doorman=False,
    property_id=1,
)
schema_unit_create = UnitSchema.Create(
    floor_number=5,
    unit_number='501',
    bedrooms=2,
    bathrooms=1.5,
    sqft=1000,
    is_vacant=True,
    building_id=1,
)
schema_lease_create = LeaseSchema.Create(
    start_date=date(2021, 1, 1),
    end_date=date(2021, 12, 31),
    rent=2500.00,
    unit_id=1,
)
schema_tenant_create = TenantSchema.Create(
    name='John Doe',
    email=generate_test_email(),
    phone='555-555-5555',
    lease_id=1,
)
schema_insurance_create = InsuranceSchema.Create(
    policy_number='12345',
    expiration_date=date(2022, 12, 31),
    tenant_id=1,
)

@pytest.fixture(scope='module')
def test_user(test_db: Session):
    schema_user_create.email = generate_test_email()  # Generate new email for each test
    user = UserController.create_and_commit(db=test_db, schema=schema_user_create)
    yield user

@no_type_check
@pytest.fixture(scope='module')
def test_property(test_db: Session, test_user: UserSchema.Create):
    property = PropertyController.create_and_commit(
        db=test_db,
        schema=schema_property_create,
        parent_id=test_user.id,
    )
    yield property

@no_type_check
@pytest.fixture(scope='module')
def test_building(test_db: Session, test_property: PropertySchema.Create):
    building = BuildingController.create_and_commit(
        db=test_db,
        schema=schema_building_create,
        parent_id=test_property.id,
    )
    yield building

@no_type_check
@pytest.fixture(scope='module')
def test_unit(test_db: Session, test_building: BuildingSchema.Create):
    unit = UnitController.create_and_commit(
        db=test_db,
        schema=schema_unit_create,
        parent_id=test_building.id,
    )
    yield unit

@pytest.fixture(scope='module')
def test_lease(test_db: Session, ):
    lease = LeaseController.create_and_commit(
        db=test_db,
        schema=schema_lease_create,
        parent_id=1,
    )
    yield lease

@pytest.fixture(scope='module')
def test_tenant(test_db: Session, ):
    schema_tenant_create.email = generate_test_email()  # Generate new email for each test
    tenant = TenantController.create_and_commit(
        db=test_db,
        schema=schema_tenant_create,
        parent_id=1,
    )
    yield tenant

@pytest.fixture(scope='module')
def test_insurance(test_db: Session, ):
    insurance = InsuranceController.create_and_commit(
        db=test_db,
        schema=schema_insurance_create,
        parent_id=1,
    )
    yield insurance

## User tests

def test_create_user(test_db: Session, test_user: UserSchema.Create):
    assert UserController.exists_where(
        db=test_db,
        key='email',
        val=test_user.email,
    ) == True
    assert UserController.exists_where(
        db=test_db,
        key='email',
        val='nonexistent@example.com',
    ) == False

def test_create_user_with_invalid_data(test_db: Session):
    # Assert that the schema will raise a validation error
    with pytest.raises(ValidationError):
        schema_user_invalid_data = UserSchema.Create(
            name='Test User',
            email='invalid-email',
            password='short',
            is_active=True,
        )
        UserController.create_and_commit(db=test_db, schema=schema_user_invalid_data)

@no_type_check
def test_update_user(test_db: Session, test_user: UserSchema.Create):
    new_email = generate_test_email()
    id = test_user.id
    schema_user_update = UserSchema.Update(
        name='new_username',
        email=new_email,
        password='new_password',

    )
    updated_user = UserController.update_and_commit(db=test_db, schema=schema_user_update, id=id)
    assert updated_user is not None
    assert updated_user.name == 'new_username'
    assert updated_user.email == new_email
    assert security.verify_password('new_password', updated_user.password)

@no_type_check
def test_update_user_with_invalid_data(test_db: Session, test_user: UserSchema.Create):
    # Assert that the schema will raise a validation error
    with pytest.raises(ValidationError):
        id = test_user.id
        schema_user_invalid_data = UserSchema.Update(
            name='Test User',
            email='invalid-email',
            password='short',
            is_active=True,
        )
        UserController.update_and_commit(db=test_db, schema=schema_user_invalid_data, id=id)

def test_get_user(test_db: Session):
    user = UserController.get_by_id(db=test_db, id=1)
    assert user is not None

def test_get_users_paginated(test_db: Session):
    users = UserController.get_all_paginated(db=test_db, skip=0, limit=10)
    assert users is not None

def test_get_users_all(test_db: Session):
    users = UserController.get_all(db=test_db)
    assert users is not None

def test_user_exists(test_db: Session):
    user = UserController.get_by_id(db=test_db, id=1)
    assert user is not None
    assert UserController.exists_where(db=test_db,
        key='email',
        val=user.email,
    ) == True

def test_user_does_not_exist(test_db: Session):
    assert UserController.exists_where(
        db=test_db,
        key='email',
        val='nonexistent@example.com',
    ) == False

def test_user_is_active(test_db: Session):
    user = UserController.get_by_id(db=test_db, id=1)
    assert user is not None
    assert user.is_active == True

def test_user_is_not_active(test_db: Session):
    schema_user_create.is_active = False
    user = UserController.create_and_commit(db=test_db, schema=schema_user_create)
    assert user is not None
    assert user.is_active == False

## Property tests

@no_type_check
def test_create_property(test_db: Session, test_user: UserSchema.Create):
    property = PropertyController.create_and_commit(
        db=test_db,
        schema=schema_property_create,
        parent_id=test_user.id,
    )
    assert property.id is not None

@no_type_check
def test_update_property(test_db: Session, test_property: PropertySchema.Create):
    id = test_property.id
    schema_property_update = PropertySchema.Update(
        name='Property 2',
        address='456 Elm St',
        city='Springfield',
        state='IL',
        zip_code='62701',
        type='commercial',
        manager='Jane Doe',
    )
    updated_property = PropertyController.update_and_commit(
        db=test_db,
        schema=schema_property_update,
        id=id,
    )
    assert updated_property is not None
    assert updated_property.name == 'Property 2'
    assert updated_property.address == '456 Elm St'
    assert updated_property.type == 'commercial'
    assert updated_property.manager == 'Jane Doe'

def test_get_property(test_db: Session):
    property = PropertyController.get_by_id(db=test_db, id=1)
    assert property is not None

def test_get_properties_paginated(test_db: Session):
    properties = PropertyController.get_all_paginated(db=test_db, parent_id=1, skip=0, limit=10)
    assert properties is not None

## Building tests

@no_type_check
def test_create_building(test_db: Session, test_property: PropertySchema.Create):
    building = BuildingController.create_and_commit(
        db=test_db,
        schema=schema_building_create,
        parent_id=test_property.id,
    )
    assert building.id is not None

@no_type_check
def test_update_building(test_db: Session, test_building: BuildingSchema.Create):
    id = test_building.id
    schema_building_update = BuildingSchema.Update(
        name='Building 2',
        unit_count=20,
        floor_count=10,
        has_elevator=False,
        has_pool=True,
        has_gym=False,
        has_parking=True,
        has_doorman=True,
        property_id=1,
    )
    updated_building = BuildingController.update_and_commit(
        db=test_db,
        schema=schema_building_update,
        id=id,
    )
    assert updated_building is not None
    assert updated_building.name == 'Building 2'
    assert updated_building.unit_count == 20
    assert updated_building.floor_count == 10
    assert updated_building.has_elevator == False
    assert updated_building.has_pool == True
    assert updated_building.has_gym == False
    assert updated_building.has_parking == True
    assert updated_building.has_doorman == True

def test_get_building(test_db: Session):
    building = BuildingController.get_by_id(db=test_db, id=1)
    assert building is not None

def test_get_buildings_paginated(test_db: Session):
    buildings = BuildingController.get_all_paginated(db=test_db, parent_id=1, skip=0, limit=10)
    assert buildings is not None

## Unit tests

@no_type_check
def test_create_unit(test_db: Session, test_building: BuildingSchema.Create):
    unit = UnitController.create_and_commit(
        db=test_db,
        schema=schema_unit_create,
        parent_id=test_building.id,
    )
    assert unit.id is not None

@no_type_check
def test_update_unit(test_db: Session, test_unit: UnitSchema.Create):
    id = test_unit.id
    schema_unit_update = UnitSchema.Update(
        floor_number=3,
        unit_number='302',
        bedrooms=1,
        bathrooms=1.5,
        sqft=750,
        is_vacant=True,
        building_id=1,
    )
    updated_unit = UnitController.update_and_commit(
        db=test_db,
        schema=schema_unit_update,
        id=id,
    )
    assert updated_unit is not None
    assert updated_unit.floor_number == 3
    assert updated_unit.unit_number == '302'
    assert updated_unit.bedrooms == 1
    assert updated_unit.bathrooms == 1.5
    assert updated_unit.sqft == 750
    assert updated_unit.is_vacant == True

def test_get_unit(test_db: Session):
    unit = UnitController.get_by_id(db=test_db, id=1)
    assert unit is not None

def test_get_units_paginated(test_db: Session):
    units = UnitController.get_all_paginated(db=test_db, parent_id=1, skip=0, limit=10)
    assert units is not None

## Lease tests

@no_type_check
def test_create_lease(test_db: Session, test_unit: UnitSchema.Create):
    lease = LeaseController.create_and_commit(
        db=test_db,
        schema=schema_lease_create,
        parent_id=test_unit.id,
    )
    assert lease.id is not None

@no_type_check
def test_update_lease(test_db: Session, test_lease: LeaseSchema.Create):
    id = test_lease.id
    schema_lease_update = LeaseSchema.Update(
        start_date=date(2022, 1, 1),
        end_date=date(2022, 12, 31),
        rent=3000.00,
        unit_id=1,
    )
    updated_lease = LeaseController.update_and_commit(
        db=test_db,
        schema=schema_lease_update,
        id=id,
    )
    assert updated_lease is not None
    assert updated_lease.start_date == date(2022, 1, 1)
    assert updated_lease.end_date == date(2022, 12, 31)
    assert updated_lease.rent == 3000.00

def test_get_lease(test_db: Session):
    lease = LeaseController.get_by_id(db=test_db, id=1)
    assert lease is not None

def test_get_leases_paginated(test_db: Session):
    leases = LeaseController.get_all_paginated(db=test_db, parent_id=1, skip=0, limit=10)
    assert leases is not None

## Tenant tests

@no_type_check
def test_create_tenant(test_db: Session, test_lease: LeaseSchema.Create):
    tenant = TenantController.create_and_commit(
        db=test_db,
        schema=schema_tenant_create,
        parent_id=test_lease.id,
    )
    assert tenant.id is not None

@no_type_check
def test_create_tenant_with_invalid_data(test_db: Session, test_lease: LeaseSchema.Create):
    # Assert that the schema will raise a validation error
    with pytest.raises(ValidationError):
        schema_tenant_invalid_data = TenantSchema.Create(
            name='John Doe',
            email='invalid-email',
            phone='555-555-5555',
            lease_id=test_lease.id,
        )
        TenantController.create_and_commit(
            db=test_db,
            schema=schema_tenant_invalid_data,
            parent_id=test_lease.id,
        )

@no_type_check
def test_update_tenant(test_db: Session, test_tenant: TenantSchema.Create):
    new_email = generate_test_email()
    id = test_tenant.id
    schema_tenant_update = TenantSchema.Update(
        name='Jane Doe',
        email=new_email,
        phone='555-555-5555',
        lease_id=1,
    )
    updated_tenant = TenantController.update_and_commit(
        db=test_db,
        schema= schema_tenant_update,
        id=id,
    )
    assert updated_tenant is not None
    assert updated_tenant.name == 'Jane Doe'
    assert updated_tenant.email == new_email

@no_type_check
def test_update_tenant_with_invalid_data(test_db: Session, test_tenant: TenantSchema.Create):
    # Assert that the schema will raise a validation error
    with pytest.raises(ValidationError):
        id = test_tenant.id
        schema_tenant_invalid_data = TenantSchema.Update(
            name='John Doe',
            email='invalid-email',
            phone='555-555-5555',
            lease_id=1,
        )
        TenantController.update_and_commit(
            db=test_db,
            schema=schema_tenant_invalid_data,
            id=id,
        )

def test_get_tenant(test_db: Session):
    tenant = TenantController.get_by_id(db=test_db, id=1)
    assert tenant is not None

def test_get_tenants_paginated(test_db: Session):
    tenants = TenantController.get_all_paginated(db=test_db, parent_id=1, skip=0, limit=10)
    assert tenants is not None

## Insurance tests

@no_type_check
def test_create_insurance(test_db: Session, test_tenant: TenantSchema.Create):
    insurance = InsuranceController.create_and_commit(
        db=test_db,
        schema=schema_insurance_create,
        parent_id=test_tenant.id,
    )
    assert insurance.id is not None

@no_type_check
def test_update_insurance(test_db: Session, test_insurance: InsuranceSchema.Create):
    id = test_insurance.id
    schema_insurance_update = InsuranceSchema.Update(
        policy_number='54321',
        expiration_date=date(2022, 12, 31),
        tenant_id=1
    )
    updated_insurance = InsuranceController.update_and_commit(
        db=test_db,
        schema=schema_insurance_update,
        id=id,
    )
    assert updated_insurance is not None
    assert updated_insurance.policy_number == '54321'

def test_get_insurance(test_db: Session):
    insurance = InsuranceController.get_by_id(db=test_db, id=1)
    assert insurance is not None

def test_get_insurances_paginated(test_db: Session):
    insurances = InsuranceController.get_all_paginated(db=test_db, parent_id=1, skip=0, limit=10)
    assert insurances is not None
