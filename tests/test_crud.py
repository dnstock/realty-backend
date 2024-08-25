import pytest, os, uuid
from pydantic import ValidationError
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import schemas, crud, models, auth

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Generate a unique email addresses
def generate_test_email():
    return f"test_{uuid.uuid4()}@example.com"

## SCHEMAS

schema_user_create = schemas.UserCreate(
    name="Test User", 
    email=generate_test_email(),
    password="test1234#$"
)
schema_property_create = schemas.PropertyCreate(
    address="123 Main St", 
    city="Springfield", 
    state="IL", 
    zip_code="62701", 
    manager_id=1
)
schema_building_create = schemas.BuildingCreate(
    name="Building 1", 
    property_id=1
)
schema_unit_create = schemas.UnitCreate(
    number="101", 
    building_id=1
)
schema_lease_create = schemas.LeaseCreate(
    start_date=date(2021, 1, 1), 
    end_date=date(2021, 12, 31), 
    unit_id=1
)
schema_tenant_create = schemas.TenantCreate(
    name="John Doe", 
    email=generate_test_email(), 
    phone="555-555-5555", 
    lease_id=1
)
schema_insurance_create = schemas.InsuranceCreate(
    policy_number="12345", 
    expiration_date=date(2022, 12, 31), 
    tenant_id=1
)

@pytest.fixture(scope="module")
def db():
    # Setup
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    # Teardown
    models.Base.metadata.drop_all(bind=engine)
    if os.path.exists("test.db"):
        os.remove("test.db")

@pytest.fixture(scope="module")
def test_user(db):
    schema_user_create.email = generate_test_email()  # Generate new email for each test
    user = crud.create_user(db, schema_user_create)
    yield user

@pytest.fixture(scope="module")
def test_property(db, test_user):
    property = crud.create_property(db, schema_property_create, test_user.id)
    yield property
    
@pytest.fixture(scope="module")
def test_building(db, test_property):
    building = crud.create_building(db, schema_building_create, test_property.id)
    yield building
    
@pytest.fixture(scope="module")
def test_unit(db, test_building):
    unit = crud.create_unit(db, schema_unit_create, test_building.id)
    yield unit
    
@pytest.fixture(scope="module")
def test_lease(db):
    lease = crud.create_lease(db, schema_lease_create, 1)
    yield lease

@pytest.fixture(scope="module")
def test_tenant(db):
    schema_tenant_create.email = generate_test_email()  # Generate new email for each test
    tenant = crud.create_tenant(db, schema_tenant_create, 1)
    yield tenant
    
@pytest.fixture(scope="module")
def test_insurance(db):
    insurance = crud.create_insurance(db, schema_insurance_create, 1)
    yield insurance

## User tests

def test_create_user(db):
    user = crud.create_user(db, schema_user_create)
    assert user.id is not None
    
def test_create_user_with_invalid_data(db):
    schema_user_invalid_data = {
        "name": "Test User",
        "email": "invalid-email",
        "password": "short"
    }
    # Assert that the schema will raise a validation error
    with pytest.raises(ValidationError):
        schema = schemas.UserCreate(**schema_user_invalid_data)
        crud.create_user(db, schema)
    
def test_update_user(db, test_user):
    new_email = generate_test_email()
    schema_user_update = schemas.UserUpdate(
        name="new_username",
        email=new_email,
        password="new_password"
    )
    updated_user = crud.update_user(db, schema_user_update, test_user.id)
    assert updated_user is not None
    assert updated_user.name == "new_username"
    assert updated_user.email == new_email
    assert auth.verify_password("new_password", updated_user.password)
    
def test_update_user_with_invalid_data(db, test_user):
    schema_user_invalid_data = {
        "name": "Test User",
        "email": "invalid-email",
        "password": "short"
    }
    # Assert that the schema will raise a validation error
    with pytest.raises(ValidationError):
        schema = schemas.UserUpdate(**schema_user_invalid_data)
        crud.update_user(db, schema, test_user.id)
    
def test_get_user(db):
    user = crud.get_user(db, 1)
    assert user is not None
    
def test_get_users(db):
    users = crud.get_users(db)
    assert users is not None
    
## Property tests

def test_create_property(db, test_user):
    property = crud.create_property(db, schema_property_create, test_user.id)
    assert property.id is not None
    
def test_update_property(db, test_property):
    schema_property_update = schemas.PropertyUpdate(
        address="456 Elm St", 
        city="Springfield", 
        state="IL", 
        zip_code="62701", 
        manager_id=1
    )
    updated_property = crud.update_property(db, schema_property_update, test_property.id)
    assert updated_property is not None
    assert updated_property.address == "456 Elm St"
    
def test_get_property(db):
    property = crud.get_property(db, 1)
    assert property is not None
    
def test_get_properties(db):
    properties = crud.get_properties(db, 1)
    assert properties is not None

## Building tests

def test_create_building(db, test_property):
    building = crud.create_building(db, schema_building_create, test_property.id)
    assert building.id is not None    
    
def test_update_building(db, test_building):
    schema_building_update = schemas.BuildingUpdate(
        name="Building 2", 
        property_id=1
    )
    updated_building = crud.update_building(db, schema_building_update, test_building.id)
    assert updated_building is not None
    assert updated_building.name == "Building 2"
    
def test_get_building(db):
    building = crud.get_building(db, 1)
    assert building is not None
    
def test_get_buildings(db):
    buildings = crud.get_buildings(db, 1)
    assert buildings is not None
    
## Unit tests

def test_create_unit(db, test_building):
    unit = crud.create_unit(db, schema_unit_create, test_building.id)
    assert unit.id is not None
    
def test_update_unit(db, test_unit):
    schema_unit_update = schemas.UnitUpdate(
        number="102", 
        building_id=1
    )
    updated_unit = crud.update_unit(db, schema_unit_update, test_unit.id)
    assert updated_unit is not None
    assert updated_unit.number == "102"    
    
def test_get_unit(db):
    unit = crud.get_unit(db, 1)
    assert unit is not None
    
def test_get_units(db):
    units = crud.get_units(db, 1)
    assert units is not None
    
## Lease tests

def test_create_lease(db, test_unit):
    lease = crud.create_lease(db, schema_lease_create, test_unit.id)
    assert lease.id is not None
    
def test_update_lease(db, test_lease):
    schema_lease_update = schemas.LeaseUpdate(
        start_date=date(2022, 1, 1), 
        end_date=date(2022, 12, 31), 
        unit_id=1
    )
    updated_lease = crud.update_lease(db, schema_lease_update, test_lease.id)
    assert updated_lease is not None
    assert updated_lease.start_date == date(2022, 1, 1)
        
def test_get_lease(db):
    lease = crud.get_lease(db, 1)
    assert lease is not None
    
def test_get_leases(db):
    leases = crud.get_leases(db, 1)
    assert leases is not None
    
## Tenant tests

def test_create_tenant(db, test_lease):
    tenant = crud.create_tenant(db, schema_tenant_create, test_lease.id)
    assert tenant.id is not None    
    
def test_create_tenant_with_invalid_data(db, test_lease):
    schema_tenant_invalid_data = {
        "name": "John Doe",
        "email": "invalid-email",
        "phone": "555-555-5555",
        "lease_id": 1
    }
    # Assert that the schema will raise a validation error
    with pytest.raises(ValidationError):
        schema = schemas.TenantCreate(**schema_tenant_invalid_data)
        crud.create_tenant(db, schema, test_lease.id)
    
def test_update_tenant(db, test_tenant):
    new_email = generate_test_email()
    schema_tenant_update = schemas.TenantUpdate(
        name="Jane Doe", 
        email=new_email,
        phone="555-555-5555", 
        lease_id=1
    )
    updated_tenant = crud.update_tenant(db, schema_tenant_update, test_tenant.id)
    assert updated_tenant is not None
    assert updated_tenant.name == "Jane Doe"
    assert updated_tenant.email == new_email
    
def test_update_tenant_with_invalid_data(db, test_tenant):
    schema_tenant_invalid_data = {
        "name": "John Doe",
        "email": "invalid-email",
        "phone": "555-555-5555",
        "lease_id": 1
    }
    # Assert that the schema will raise a validation error
    with pytest.raises(ValidationError):
        schema = schemas.TenantUpdate(**schema_tenant_invalid_data)
        crud.update_tenant(db, schema, test_tenant.id)
    
def test_get_tenant(db):
    tenant = crud.get_tenant(db, 1)
    assert tenant is not None
    
def test_get_tenants(db):
    tenants = crud.get_tenants(db, 1)
    assert tenants is not None
    
## Insurance tests

def test_create_insurance(db, test_tenant):
    insurance = crud.create_insurance(db, schema_insurance_create, test_tenant.id)
    assert insurance.id is not None
    
def test_update_insurance(db, test_insurance):
    schema_insurance_update = schemas.InsuranceUpdate(
        policy_number="54321", 
        expiration_date=date(2022, 12, 31), 
        tenant_id=1
    )
    updated_insurance = crud.update_insurance(db, schema_insurance_update, test_insurance.id)
    assert updated_insurance is not None
    assert updated_insurance.policy_number == "54321"    

def test_get_insurance(db):
    insurance = crud.get_insurance(db, 1)
    assert insurance is not None
    
def test_get_insurances(db):
    insurances = crud.get_insurances(db, 1)
    assert insurances is not None
