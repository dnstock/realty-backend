from fastapi import APIRouter, Depends
from app.api.v1.deps import (
    get_request_context,
    validate_ownership,
    serialize_results,
    PaginatedResults,
    RequestContext,
)
from controllers import InsuranceController
from schemas import InsuranceSchema

router: APIRouter = APIRouter()

@router.post('/', response_model=InsuranceSchema.Read)
def create(
    tenant_id: int, insurance: InsuranceSchema.Create,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context, model_name='Tenant', resource_id=tenant_id)
    return InsuranceController.create_and_commit(context=context, schema=insurance, parent_id=tenant_id)

@router.get('/', response_model=PaginatedResults)
def index(
    skip: int = 0, limit: int = 10,
    context: RequestContext = Depends(get_request_context),
):
    results = InsuranceController.get_all(context=context, skip=skip, limit=limit)
    return serialize_results(results, InsuranceSchema.Read)

@router.get('/{insurance_id}', response_model=InsuranceSchema.Read)
def read(
    insurance_id: int,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context, model_name='Insurance', resource_id=insurance_id)
    return InsuranceController.get_by_id(context=context, id=insurance_id)

@router.put('/{insurance_id}', response_model=InsuranceSchema.Read)
def update(
    insurance_id: int, insurance: InsuranceSchema.Update,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context, model_name='Insurance', resource_id=insurance_id)
    return InsuranceController.update_and_commit(context=context, schema=insurance, id=insurance_id)
