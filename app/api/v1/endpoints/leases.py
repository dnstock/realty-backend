from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers import LeaseController
from schemas import LeaseSchema
from app.api.v1.deps import get_db, validate_ownership

router: APIRouter = APIRouter()

@router.post("/units/{unit_id}/leases/", response_model=LeaseSchema.Read)
def create_lease(
    unit_id: int, lease: LeaseSchema.Create, db: Session = Depends(get_db), 
    # _ = Depends(lambda: validate_ownership(model_name="Unit", resource_id=unit_id))
):
    return LeaseController.create_and_commit(db=db, schema=lease, parent_id=unit_id)

@router.get("/units/{unit_id}/leases/", response_model=list[LeaseSchema.Read])
def read_leases(
    unit_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), 
    # _ = Depends(lambda: validate_ownership(model_name="Unit", resource_id=unit_id))
):
    return LeaseController.get_all(db=db, parent_id=unit_id, skip=skip, limit=limit)

@router.get("/leases/{lease_id}", response_model=LeaseSchema.Read)
def read_lease(
    lease_id: int, db: Session = Depends(get_db), 
    # _ = Depends(lambda: validate_ownership(model_name="Lease", resource_id=lease_id))
):
    return LeaseController.get_by_id(db=db, id=lease_id)

@router.put("/leases/{lease_id}", response_model=LeaseSchema.Read)
def update_lease(
    lease_id: int, lease: LeaseSchema.Update, db: Session = Depends(get_db), 
    # _ = Depends(lambda: validate_ownership(model_name="Lease", resource_id=lease_id))
):
    return LeaseController.update_and_commit(db=db, schema=lease, id=lease_id)