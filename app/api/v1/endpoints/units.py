from fastapi import APIRouter, Depends
from app.api.v1.deps import (
    get_request_context,
    validate_ownership,
    serialize_results,
    PaginatedResults,
    RequestContext,
)
from controllers import UnitController, LeaseController
from schemas import UnitSchema, LeaseSchema

router: APIRouter = APIRouter()

@router.post('/', response_model=UnitSchema.Read)
def create(
    building_id: int, unit: UnitSchema.Create,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context, model_name='Building', resource_id=building_id)
    return UnitController.create_and_commit(context=context, schema=unit, parent_id=building_id)

@router.get('/', response_model=PaginatedResults)
def index(
    skip: int = 0, limit: int = 10,
    context: RequestContext = Depends(get_request_context),
):
    results = UnitController.get_all(context=context, skip=skip, limit=limit)
    return serialize_results(results, UnitSchema.Read)

@router.get('/{unit_id}', response_model=UnitSchema.Read)
def read(
    unit_id: int,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context, model_name='Unit', resource_id=unit_id)
    return UnitController.get_by_id(context=context, id=unit_id)

@router.put('/{unit_id}', response_model=UnitSchema.Read)
def update(
    unit_id: int, unit: UnitSchema.Update,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context, model_name='Unit', resource_id=unit_id)
    return UnitController.update_and_commit(context=context, schema=unit, id=unit_id)

@router.get('/{unit_id}/leases/', response_model=PaginatedResults)
def subindex(
    unit_id: int, skip: int = 0, limit: int = 10,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context, model_name='Unit', resource_id=unit_id)
    results = LeaseController.get_all_from_parent(context=context, parent_id=unit_id, skip=skip, limit=limit)
    return serialize_results(results, LeaseSchema.Read)
