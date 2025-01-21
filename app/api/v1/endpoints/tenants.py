from fastapi import APIRouter, Depends
from app.api.v1.deps import (
    get_request_context,
    serialize_results,
    PaginatedResults,
    RequestContext,
)
from controllers import TenantController, InsuranceController
from schemas import TenantSchema, InsuranceSchema

router: APIRouter = APIRouter()

@router.post('/', response_model=TenantSchema.Read)
def create(
    lease_id: int, tenant: TenantSchema.Create,
    context: RequestContext = Depends(get_request_context),
):
    return TenantController.create_and_commit(context=context, schema=tenant, parent_id=lease_id)

@router.get('/', response_model=PaginatedResults)
def index(
    skip: int = 0, limit: int = 10,
    context: RequestContext = Depends(get_request_context),
):
    results = TenantController.get_all(context=context, skip=skip, limit=limit)
    return serialize_results(results, TenantSchema.Read)

@router.get('/{tenant_id}', response_model=TenantSchema.Read)
def read(
    tenant_id: int,
    context: RequestContext = Depends(get_request_context),
):
    return TenantController.get_by_id(context=context, id=tenant_id)

@router.put('/{tenant_id}', response_model=TenantSchema.Read)
def update(
    tenant_id: int, tenant: TenantSchema.Update,
    context: RequestContext = Depends(get_request_context),
):
    return TenantController.update_and_commit(context=context, schema=tenant, id=tenant_id)

@router.get('/{tenant_id}/insurances/', response_model=PaginatedResults)
def subindex(
    tenant_id: int, skip: int = 0, limit: int = 10,
    context: RequestContext = Depends(get_request_context),
):
    results = InsuranceController.get_all_from_parent(context=context, parent_id=tenant_id, skip=skip, limit=limit)
    return serialize_results(results, InsuranceSchema.Read)
