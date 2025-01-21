from fastapi import APIRouter, Depends
from app.api.v1.deps import (
    get_request_context,
    serialize_results,
    PaginatedResults,
    RequestContext,
)
from controllers import LeaseController, TenantController
from schemas import LeaseSchema, TenantSchema

router: APIRouter = APIRouter()

@router.post('/', response_model=LeaseSchema.Read)
def create(
    unit_id: int, lease: LeaseSchema.Create,
    context: RequestContext = Depends(get_request_context),
):
    return LeaseController.create_and_commit(context=context, schema=lease, parent_id=unit_id)

@router.get('/', response_model=PaginatedResults)
def index(
    skip: int = 0, limit: int = 10,
    context: RequestContext = Depends(get_request_context),
):
    results = LeaseController.get_all(context=context, skip=skip, limit=limit)
    return serialize_results(results, LeaseSchema.Read)

@router.get('/{lease_id}', response_model=LeaseSchema.Read)
def read(
    lease_id: int,
    context: RequestContext = Depends(get_request_context),
):
    return LeaseController.get_by_id(context=context, id=lease_id)

@router.put('/{lease_id}', response_model=LeaseSchema.Read)
def update(
    lease_id: int, lease: LeaseSchema.Update,
    context: RequestContext = Depends(get_request_context),
):
    return LeaseController.update_and_commit(context=context, schema=lease, id=lease_id)

@router.get('/{lease_id}/tenants/', response_model=PaginatedResults)
def subindex(
    lease_id: int, skip: int = 0, limit: int = 10,
    context: RequestContext = Depends(get_request_context),
):
    results = TenantController.get_all_from_parent(context=context, parent_id=lease_id, skip=skip, limit=limit)
    return serialize_results(results, TenantSchema.Read)
