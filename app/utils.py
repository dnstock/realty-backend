from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas

# Check if an resource belongs to a user
def validate_ownership(db: Session, user: schemas.User, resource_type: str, resource_id: int):
    try:
        resource = db.query(getattr(models, resource_type)).filter_by(id=resource_id).first()
    except AttributeError:
        raise HTTPException(status_code=404, detail="Invalid resource type")
    
    if resource is None:
        raise HTTPException(status_code=404, detail=f"{resource_type} not found")
    
    valid = False
    if resource_type == "Property":
        valid = resource.manager_id == user.id
    elif resource_type == "Building":
        valid = resource.property.manager_id == user.id
    elif resource_type == "Unit":
        valid = resource.building.property.manager_id == user.id
    elif resource_type == "Lease":
        valid = resource.unit.building.property.manager_id == user.id
    elif resource_type == "Tenant":
        valid = resource.lease.unit.building.property.manager_id == user.id
    elif resource_type == "Insurance":
        valid = resource.tenant.lease.unit.building.property.manager_id == user.id
    
    if not valid:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return valid
