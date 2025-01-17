from fastapi import APIRouter, Depends
from app.api.v1.deps import (
    get_request_context,
    validate_ownership,
    serialize_results,
    PaginatedResults,
    RequestContext,
)
from controllers import BuildingController, UnitController
from schemas import BuildingSchema, UnitSchema

router: APIRouter = APIRouter()

@router.post('/', response_model=BuildingSchema.Read)
def create(
    property_id: int, building: BuildingSchema.Create,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context, model_name='Property', resource_id=property_id)
    return BuildingController.create_and_commit(context=context, schema=building, parent_id=property_id)

@router.get('/', response_model=PaginatedResults)
def index(
    skip: int = 0, limit: int = 10,
    context: RequestContext = Depends(get_request_context),
):
    results = BuildingController.get_all(context=context, skip=skip, limit=limit)
    return serialize_results(results, BuildingSchema.Read)

@router.get('/{building_id}', response_model=BuildingSchema.Read)
def read(
    building_id: int,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context, model_name='Building', resource_id=building_id)
    return BuildingController.get_by_id(context=context, id=building_id)

@router.put('/{building_id}', response_model=BuildingSchema.Read)
def update(
    building_id: int, building: BuildingSchema.Update,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context, model_name='Building', resource_id=building_id)
    return BuildingController.update_and_commit(context=context, schema=building, id=building_id)

@router.get('/{building_id}/units/', response_model=PaginatedResults)
def subindex(
    building_id: int, skip: int = 0, limit: int = 10,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context, model_name='Building', resource_id=building_id)
    results = UnitController.get_all_from_parent(context=context, parent_id=building_id, skip=skip, limit=limit)
    return serialize_results(results, UnitSchema.Read)
