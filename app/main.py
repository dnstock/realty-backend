from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from . import models, schemas, crud, database, auth
from .config import settings
from .utils import validate_ownership

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)    


## Authentication Management

# Define the allowed origins
origins = [
    "http://localhost:3000",  # React development server
]

# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers (Authorization, Content-Type, etc.)
)

@app.post("/login", response_model=schemas.AuthResponse)
async def login_for_access_token(db: Session = Depends(database.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
        }
    }


## User Management

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_obj = crud.get_user_by_email(db, user.email)
    if db_obj:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_obj = crud.get_user(db, user_id)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_obj

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(database.get_db)):
    return crud.update_user(db, user, user_id)


## Property Management

@app.post("/properties/", response_model=schemas.Property)
def create_property(
    property: schemas.PropertyCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    return crud.create_property(db, property, parent_id=current_user.id)

@app.get("/properties/", response_model=List[schemas.Property])
def read_properties(
    skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    return crud.get_properties(db, parent_id=current_user.id, skip=skip, limit=limit)

@app.get("/properties/{property_id}", response_model=schemas.Property)
def read_property(
    property_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    validate_ownership(db, current_user, "Property", property_id)
    return crud.get_property(db, property_id)

@app.put("/properties/{property_id}", response_model=schemas.Property)
def update_property(
    property_id: int, property: schemas.PropertyUpdate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    validate_ownership(db, current_user, "Property", property_id)
    return crud.update_property(db, property, property_id)


## Building Management

@app.post("/properties/{property_id}/buildings/", response_model=schemas.Building)
def create_building(
    property_id: int, building: schemas.BuildingCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    validate_ownership(db, current_user, "Property", property_id)
    return crud.create_building(db, building, parent_id=property_id)

@app.get("/properties/{property_id}/buildings/", response_model=List[schemas.Building])
def read_buildings(
    property_id, skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    validate_ownership(db, current_user, "Property", property_id)
    return crud.get_buildings(db, parent_id=property_id, skip=skip, limit=limit)

@app.get("/buildings/{building_id}", response_model=schemas.Building)
def read_building(
    building_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    validate_ownership(db, current_user, "Building", building_id)
    return crud.get_building(db, building_id)

@app.put("/buildings/{building_id}", response_model=schemas.Building)
def update_building(
    building_id: int, building: schemas.BuildingUpdate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    validate_ownership(db, current_user, "Building", building_id)
    return crud.update_building(db, building, building_id)


## Unit Management

@app.post("/buildings/{building_id}/units/", response_model=schemas.Unit)
def create_unit(
    building_id: int, unit: schemas.UnitCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    validate_ownership(db, current_user, "Building", building_id)
    return crud.create_unit(db, unit, parent_id=building_id)

@app.get("/buildings/{building_id}/units/", response_model=List[schemas.Unit])
def read_units(
    building_id, skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    validate_ownership(db, current_user, "Building", building_id)
    return crud.get_units(db, parent_id=building_id, skip=skip, limit=limit)

@app.get("/units/{unit_id}", response_model=schemas.Unit)
def read_unit(
    unit_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    validate_ownership(db, current_user, "Unit", unit_id)
    return crud.get_unit(db, unit_id)

@app.put("/units/{unit_id}", response_model=schemas.Unit)
def update_unit(
    unit_id: int, unit: schemas.UnitUpdate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    validate_ownership(db, current_user, "Unit", unit_id)
    return crud.update_unit(db, unit, unit_id)


## Lease Management

@app.post("/units/{unit_id}/leases/", response_model=schemas.Lease)
def create_lease(
    unit_id: int, lease: schemas.LeaseCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    validate_ownership(db, current_user, "Unit", unit_id)
    return crud.create_lease(db, lease, parent_id=unit_id)

@app.get("/units/{unit_id}/leases/", response_model=List[schemas.Lease])
def read_leases(
    unit_id, skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    validate_ownership(db, current_user, "Unit", unit_id)
    return crud.get_leases(db, parent_id=unit_id, skip=skip, limit=limit)

@app.get("/leases/{lease_id}", response_model=schemas.Lease)
def read_lease(
    lease_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    validate_ownership(db, current_user, "Lease", lease_id)
    return crud.get_lease(db, lease_id)

@app.put("/leases/{lease_id}", response_model=schemas.Lease)
def update_lease(
    lease_id: int, lease: schemas.LeaseUpdate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    validate_ownership(db, current_user, "Lease", lease_id)
    return crud.update_lease(db, lease, lease_id)


## Tenant Management

@app.post("/leases/{lease_id}/tenants/", response_model=schemas.Tenant)
def create_tenant(
    lease_id: int, tenant: schemas.TenantCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    validate_ownership(db, current_user, "Lease", lease_id)
    return crud.create_tenant(db, tenant, parent_id=lease_id)

@app.get("/leases/{lease_id}/tenants/", response_model=List[schemas.Tenant])
def read_tenants(
    lease_id, skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    validate_ownership(db, current_user, "Lease", lease_id)
    return crud.get_tenants(db, parent_id=lease_id, skip=skip, limit=limit)

@app.get("/tenants/{tenant_id}", response_model=schemas.Tenant)
def read_tenant(
    tenant_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    validate_ownership(db, current_user, "Tenant", tenant_id)
    return crud.get_tenant(db, tenant_id)

@app.put("/tenants/{tenant_id}", response_model=schemas.Tenant)
def update_tenant(
    tenant_id: int, tenant: schemas.TenantUpdate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    validate_ownership(db, current_user, "Tenant", tenant_id)
    return crud.update_tenant(db, tenant, tenant_id)


## Insurance Management

@app.post("/tenants/{tenant_id}/insurances/", response_model=schemas.Insurance)
def create_insurance(
    tenant_id: int, insurance: schemas.InsuranceCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    validate_ownership(db, current_user, "Tenant", tenant_id)
    return crud.create_insurance(db, insurance, parent_id=tenant_id)

@app.get("/tenants/{tenant_id}/insurances/", response_model=List[schemas.Insurance])
def read_insurances(
    tenant_id, skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    validate_ownership(db, current_user, "Tenant", tenant_id)
    return crud.get_insurances(db, parent_id=tenant_id, skip=skip, limit=limit)

@app.get("/insurances/{insurance_id}", response_model=schemas.Insurance)
def read_insurance(
    insurance_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    validate_ownership(db, current_user, "Insurance", insurance_id)
    return crud.get_insurance(db, insurance_id)

@app.put("/insurances/{insurance_id}", response_model=schemas.Insurance)
def update_insurance(
    insurance_id: int, insurance: schemas.InsuranceUpdate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    validate_ownership(db, current_user, "Insurance", insurance_id)
    return crud.update_insurance(db, insurance, insurance_id)

