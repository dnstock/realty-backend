from sqlalchemy.orm import Session
from . import models, schemas, auth

## HEIRARCHY OF RESOURCES
# Manager -> Property -> Building -> Unit -> Lease -> Tenant -> Insurance
# Note: Manager is an authenticated end user
##

""" HELPER FUNCTIONS """

def get_one(db: Session, model, id: int):
    return db.query(model).filter(model.id == id).first()

#(HARDEN THIS FUNCTION BEFORE USING)
# def get_one_by(db: Session, model, **kwargs):
#     return db.query(model).filter_by(**kwargs).first()

def get_all(db: Session, model, parent_key, parent_value, skip: int = 0, limit: int = 10):
    return db.query(model).filter(getattr(model, parent_key) == parent_value).offset(skip).limit(limit).all()

def create_and_commit(db: Session, model, schema, parent_key, parent_value):
    db_obj = model(**schema.model_dump())
    db_obj.__setattr__(parent_key, parent_value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# TODO: Ensure user input does not override primary key or foreign key values!
def update_and_commit(db: Session, model, schema, id):
    db_obj = db.query(model).filter(model.id == id).first()
    for key, value in schema.model_dump().items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

#(DELETE WILL BE IMPLEMENTED LATER)
# def delete_and_commit(db: Session, model, id):
#     db_obj = db.query(model).filter(model.id == id).first()
#     db.delete(db_obj)
#     db.commit()
#     return db_obj


""" RESOURCE OPERATIONS """

## User (user == manager)
## This model does not have a parent resource so we will not be using the helper functions

def get_user(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, schema: schemas.UserCreate):
    db_obj = models.User(**schema.model_dump())
    db_obj.__setattr__("password", auth.get_password_hash(schema.password))
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_user(db: Session, schema: schemas.UserUpdate, id: int):
    db_obj = db.query(models.User).filter(models.User.id == id).first()
    for key, value in schema.model_dump().items():
        if key == "hashed_password":
            value = auth.get_password_hash(value)
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


## Property

def get_property(db: Session, id: int):
    return get_one(db, models.Property, id)

def get_properties(db: Session, parent_id: int, skip: int = 0, limit: int = 10):
    return get_all(db, models.Property, "manager_id", parent_id, skip, limit)

def create_property(db: Session, schema: schemas.PropertyCreate, parent_id: int):
    return create_and_commit(db, models.Property, schema, "manager_id", parent_id)

def update_property(db: Session, schema: schemas.PropertyUpdate, id: int):
    return update_and_commit(db, models.Property, schema, id)


## Building

def get_building(db: Session, id: int):
    return get_one(db, models.Building, id)

def get_buildings(db: Session, parent_id: int, skip: int = 0, limit: int = 10):
    return get_all(db, models.Building, "property_id", parent_id, skip, limit)

def create_building(db: Session, schema: schemas.BuildingCreate, parent_id: int):
    return create_and_commit(db, models.Building, schema, "property_id", parent_id)

def update_building(db: Session, schema: schemas.BuildingUpdate, id: int):
    return update_and_commit(db, models.Building, schema, id)


## Unit

def get_unit(db: Session, id: int):
    return get_one(db, models.Unit, id)

def get_units(db: Session, parent_id: int, skip: int = 0, limit: int = 10):
    return get_all(db, models.Unit, "building_id", parent_id, skip, limit)

def create_unit(db: Session, schema: schemas.UnitCreate, parent_id: int):
    return create_and_commit(db, models.Unit, schema, "building_id", parent_id)

def update_unit(db: Session, schema: schemas.UnitUpdate, id: int):
    return update_and_commit(db, models.Unit, schema, id)


## Lease

def get_lease(db: Session, id: int):
    return get_one(db, models.Lease, id)

def get_leases(db: Session, parent_id: int, skip: int = 0, limit: int = 10):
    return get_all(db, models.Lease, "unit_id", parent_id, skip, limit)

def create_lease(db: Session, schema: schemas.LeaseCreate, parent_id: int):
    return create_and_commit(db, models.Lease, schema, "unit_id", parent_id)

def update_lease(db: Session, schema: schemas.LeaseUpdate, id: int):
    return update_and_commit(db, models.Lease, schema, id)


## Tenant

def get_tenant(db: Session, id: int):
    return get_one(db, models.Tenant, id)

def get_tenants(db: Session, parent_id: int, skip: int = 0, limit: int = 10):
    return get_all(db, models.Tenant, "lease_id", parent_id, skip, limit)

def create_tenant(db: Session, schema: schemas.TenantCreate, parent_id: int):
    return create_and_commit(db, models.Tenant, schema, "lease_id", parent_id)

def update_tenant(db: Session, schema: schemas.TenantUpdate, id: int):
    return update_and_commit(db, models.Tenant, schema, id)


## Insurance

def get_insurance(db: Session, id: int):
    return get_one(db, models.Insurance, id)

def get_insurances(db: Session, parent_id: int, skip: int = 0, limit: int = 10):
    return get_all(db, models.Insurance, "tenant_id", parent_id, skip, limit)

def create_insurance(db: Session, schema: schemas.InsuranceCreate, parent_id: int):
    return create_and_commit(db, models.Insurance, schema, "tenant_id", parent_id)

def update_insurance(db: Session, schema: schemas.InsuranceUpdate, id: int):
    return update_and_commit(db, models.Insurance, schema, id)
