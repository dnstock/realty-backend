from fastapi import APIRouter
from controllers import UnitController, LeaseController
from schemas import BaseSchema, UnitSchema, LeaseSchema
from app.api.v1.deps import serialize_results

router: APIRouter = APIRouter()

@router.get("/{unit_id}", response_model=UnitSchema.Read)
def read_unit(
    unit_id: int, 
    # _ = Depends(lambda: validate_ownership(model_name="Unit", resource_id=unit_id))
):
    return UnitController.get_by_id(id=unit_id)

@router.put("/{unit_id}", response_model=UnitSchema.Read)
def update_unit(
    unit_id: int, unit: UnitSchema.Update, 
    # _ = Depends(lambda: validate_ownership(model_name="Unit", resource_id=unit_id))
):
    return UnitController.update_and_commit(schema=unit, id=unit_id)

@router.post("/{unit_id}/leases/", response_model=LeaseSchema.Read)
def create_lease(
    unit_id: int, lease: LeaseSchema.Create, 
    # _ = Depends(lambda: validate_ownership(model_name="Unit", resource_id=unit_id))
):
    return LeaseController.create_and_commit(schema=lease, parent_id=unit_id)

@router.get("/{unit_id}/leases/", response_model=BaseSchema.PaginatedResults)
def read_leases(
    unit_id: int, skip: int = 0, limit: int = 10, 
    # _ = Depends(lambda: validate_ownership(model_name="Unit", resource_id=unit_id))
):
    results = LeaseController.get_all_paginated(parent_id=unit_id, skip=skip, limit=limit)
    return serialize_results(results, LeaseSchema.Read)
