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
def test_db():
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
    manager_id=1,
)
schema_building_create = BuildingSchema.Create(
    name='Building 1',
    unit_count=10,
    property_id=1,
)
schema_unit_create = UnitSchema.Create(
    number='101',
    building_id=1,
)
schema_lease_create = LeaseSchema.Create(
    start_date=date(2021, 1, 1),
    end_date=date(2021, 12, 31),
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

@pytest.fixture(scope='module')
def test_property(test_db: Session, test_user: UserSchema.Create):
    property = PropertyController.create_and_commit(
        db=test_db,
        schema=schema_property_create,
        parent_id=getattr(test_user, 'id'),
    )
    yield property

@pytest.fixture(scope='module')
def test_building(test_db: Session, test_property: PropertySchema.Create):
    building = BuildingController.create_and_commit(
        db=test_db,
        schema=schema_building_create,
        parent_id=getattr(test_property, 'id'),
    )
    yield building

@pytest.fixture(scope='module')
def test_unit(test_db: Session, test_building: BuildingSchema.Create):
    unit = UnitController.create_and_commit(
        db=test_db,
        schema=schema_unit_create,
        parent_id=getattr(test_building, 'id'),
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

def test_update_user(test_db: Session, test_user: UserSchema.Create):
    new_email = generate_test_email()
    schema_user_update = UserSchema.Update(
        id=getattr(test_user, 'id'),
        name='new_username',
        email=new_email,
        password='new_password',

    )
    updated_user = UserController.update_and_commit(db=test_db, schema=schema_user_update)
    assert updated_user is not None
    assert getattr(updated_user, 'name') == 'new_username'
    assert getattr(updated_user, 'email') == new_email
    assert security.verify_password('new_password', updated_user.password)

def test_update_user_with_invalid_data(test_db: Session, test_user: UserSchema.Create):
    # Assert that the schema will raise a validation error
    with pytest.raises(ValidationError):
        schema_user_invalid_data = UserSchema.Update(
            id=getattr(test_user, 'id'),
            name='Test User',
            email='invalid-email',
            password='short',
            is_active=True,
        )
        UserController.update_and_commit(db=test_db, schema=schema_user_invalid_data)

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

def test_create_property(test_db: Session, test_user: UserSchema.Create):
    property = PropertyController.create_and_commit(
        db=test_db,
        schema=schema_property_create,
        parent_id=getattr(test_user, 'id'),
    )
    assert getattr(property, 'id') is not None

def test_update_property(test_db: Session, test_property: PropertySchema.Create):
    schema_property_update = PropertySchema.Update(
        id=getattr(test_property, 'id'),
        name='Property 2',
        address='456 Elm St',
        city='Springfield',
        state='IL',
        zip_code='62701',
        type='commercial',
        manager_id=1,
    )
    updated_property = PropertyController.update_and_commit(
        db=test_db,
        schema=schema_property_update,
        id=getattr(test_property, 'id'),
    )
    assert updated_property is not None
    assert getattr(updated_property, 'address') == '456 Elm St'

def test_get_property(test_db: Session):
    property = PropertyController.get_by_id(db=test_db, id=1)
    assert property is not None

def test_get_properties_paginated(test_db: Session):
    properties = PropertyController.get_all_paginated(db=test_db, parent_id=1, skip=0, limit=10)
    assert properties is not None

## Building tests

def test_create_building(test_db: Session, test_property: PropertySchema.Create):
    building = BuildingController.create_and_commit(
        db=test_db,
        schema=schema_building_create,
        parent_id=getattr(test_property, 'id'),
    )
    assert getattr(building, 'id') is not None

def test_update_building(test_db: Session, test_building: BuildingSchema.Create):
    schema_building_update = BuildingSchema.Update(
        id=getattr(test_building, 'id'),
        name='Building 2',
        unit_count=20,
        property_id=1,
    )
    updated_building = BuildingController.update_and_commit(
        db=test_db,
        schema=schema_building_update,
        id=getattr(test_building, 'id'),
    )
    assert updated_building is not None
    assert getattr(updated_building, 'name') == 'Building 2'

def test_get_building(test_db: Session):
    building = BuildingController.get_by_id(db=test_db, id=1)
    assert building is not None

def test_get_buildings_paginated(test_db: Session):
    buildings = BuildingController.get_all_paginated(db=test_db, parent_id=1, skip=0, limit=10)
    assert buildings is not None

## Unit tests

def test_create_unit(test_db: Session, test_building: BuildingSchema.Create):
    unit = UnitController.create_and_commit(
        db=test_db,
        schema=schema_unit_create,
        parent_id=getattr(test_building, 'id'),
    )
    assert getattr(unit, 'id') is not None

def test_update_unit(test_db: Session, test_unit: UnitSchema.Create):
    schema_unit_update = UnitSchema.Update(
        id=getattr(test_unit, 'id'),
        number='102',
        building_id=1,
    )
    updated_unit = UnitController.update_and_commit(
        db=test_db,
        schema=schema_unit_update,
        id=getattr(test_unit, 'id'),
    )
    assert updated_unit is not None
    assert getattr(updated_unit, 'number') == '102'

def test_get_unit(test_db: Session):
    unit = UnitController.get_by_id(db=test_db, id=1)
    assert unit is not None

def test_get_units_paginated(test_db: Session):
    units = UnitController.get_all_paginated(db=test_db, parent_id=1, skip=0, limit=10)
    assert units is not None

## Lease tests

def test_create_lease(test_db: Session, test_unit: UnitSchema.Create):
    lease = LeaseController.create_and_commit(
        db=test_db,
        schema=schema_lease_create,
        parent_id=getattr(test_unit, 'id'),
    )
    assert getattr(lease, 'id') is not None

def test_update_lease(test_db: Session, test_lease: LeaseSchema.Create):
    schema_lease_update = LeaseSchema.Update(
        id=getattr(test_lease, 'id'),
        start_date=date(2022, 1, 1),
        end_date=date(2022, 12, 31),
        unit_id=1,
    )
    updated_lease = LeaseController.update_and_commit(
        db=test_db,
        schema=schema_lease_update,
        id=getattr(test_lease, 'id'),
    )
    assert updated_lease is not None
    assert getattr(updated_lease, 'start_date') == date(2022, 1, 1)

def test_get_lease(test_db: Session):
    lease = LeaseController.get_by_id(db=test_db, id=1)
    assert lease is not None

def test_get_leases_paginated(test_db: Session):
    leases = LeaseController.get_all_paginated(db=test_db, parent_id=1, skip=0, limit=10)
    assert leases is not None

## Tenant tests

def test_create_tenant(test_db: Session, test_lease: LeaseSchema.Create):
    tenant = TenantController.create_and_commit(
        db=test_db,
        schema=schema_tenant_create,
        parent_id=getattr(test_lease, 'id'),
    )
    assert getattr(tenant, 'id') is not None

def test_create_tenant_with_invalid_data(test_db: Session, test_lease: LeaseSchema.Create):
    # Assert that the schema will raise a validation error
    with pytest.raises(ValidationError):
        schema_tenant_invalid_data = TenantSchema.Create(
            name='John Doe',
            email='invalid-email',
            phone='555-555-5555',
            lease_id=getattr(test_lease, 'id'),
        )
        TenantController.create_and_commit(
            db=test_db,
            schema=schema_tenant_invalid_data,
            parent_id=getattr(test_lease, 'id'),
        )

def test_update_tenant(test_db: Session, test_tenant: TenantSchema.Create):
    new_email = generate_test_email()
    schema_tenant_update = TenantSchema.Update(
        id=getattr(test_tenant, 'id'),
        name='Jane Doe',
        email=new_email,
        phone='555-555-5555',
        lease_id=1,
    )
    updated_tenant = TenantController.update_and_commit(
        db=test_db,
        schema= schema_tenant_update,
        id=getattr(test_tenant, 'id'),
    )
    assert updated_tenant is not None
    assert getattr(updated_tenant, 'name') == 'Jane Doe'
    assert getattr(updated_tenant, 'email') == new_email

def test_update_tenant_with_invalid_data(test_db: Session, test_tenant: TenantSchema.Create):
    # Assert that the schema will raise a validation error
    with pytest.raises(ValidationError):
        schema_tenant_invalid_data = TenantSchema.Update(
            id=getattr(test_tenant, 'id'),
            name='John Doe',
            email='invalid-email',
            phone='555-555-5555',
            lease_id=1,
        )
        TenantController.update_and_commit(
            db=test_db,
            schema=schema_tenant_invalid_data,
            id=getattr(test_tenant, 'id'),
        )

def test_get_tenant(test_db: Session):
    tenant = TenantController.get_by_id(db=test_db, id=1)
    assert tenant is not None

def test_get_tenants_paginated(test_db: Session):
    tenants = TenantController.get_all_paginated(db=test_db, parent_id=1, skip=0, limit=10)
    assert tenants is not None

## Insurance tests

def test_create_insurance(test_db: Session, test_tenant: TenantSchema.Create):
    insurance = InsuranceController.create_and_commit(
        db=test_db,
        schema=schema_insurance_create,
        parent_id=getattr(test_tenant, 'id'),
    )
    assert getattr(insurance, 'id') is not None

def test_update_insurance(test_db: Session, test_insurance: InsuranceSchema.Create):
    schema_insurance_update = InsuranceSchema.Update(
        id=getattr(test_insurance, 'id'),
        policy_number='54321',
        expiration_date=date(2022, 12, 31),
        tenant_id=1
    )
    updated_insurance = InsuranceController.update_and_commit(
        db=test_db,
        schema=schema_insurance_update,
        id=getattr(test_insurance, 'id'),
    )
    assert updated_insurance is not None
    assert getattr(updated_insurance, 'policy_number') == '54321'

def test_get_insurance(test_db: Session):
    insurance = InsuranceController.get_by_id(db=test_db, id=1)
    assert insurance is not None

def test_get_insurances_paginated(test_db: Session):
    insurances = InsuranceController.get_all_paginated(db=test_db, parent_id=1, skip=0, limit=10)
    assert insurances is not None
