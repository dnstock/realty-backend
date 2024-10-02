from fastapi import APIRouter
from controllers import LeaseController, TenantController
from schemas import BaseSchema, LeaseSchema, TenantSchema
from app.api.v1.deps import serialize_results

router: APIRouter = APIRouter()

@router.get("/{lease_id}", response_model=LeaseSchema.Read)
def read_lease(
    lease_id: int, 
    # _ = Depends(lambda: validate_ownership(model_name="Lease", resource_id=lease_id))
):
    return LeaseController.get_by_id(id=lease_id)

@router.put("/{lease_id}", response_model=LeaseSchema.Read)
def update_lease(
    lease_id: int, lease: LeaseSchema.Update, 
    # _ = Depends(lambda: validate_ownership(model_name="Lease", resource_id=lease_id))
):
    return LeaseController.update_and_commit(schema=lease, id=lease_id)

@router.post("/{lease_id}/tenants/", response_model=TenantSchema.Read)
def create_tenant(
    lease_id: int, tenant: TenantSchema.Create, 
    # _ = Depends(lambda: validate_ownership(model_name="Lease", resource_id=lease_id))
):
    return TenantController.create_and_commit(schema=tenant, parent_id=lease_id)

@router.get("/{lease_id}/tenants/", response_model=BaseSchema.PaginatedResults)
def read_tenants(
    lease_id: int, skip: int = 0, limit: int = 10, 
    # _ = Depends(lambda: validate_ownership(model_name="Lease", resource_id=lease_id))
):
    results = TenantController.get_all_paginated(parent_id=lease_id, skip=skip, limit=limit)
    return serialize_results(results, TenantSchema.Read)
