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

@router.get('/{building_id}', response_model=BuildingSchema.Read)
def read_building(
    building_id: int,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context, model_name='Building', resource_id=building_id)
    return BuildingController.get_by_id(db=context.db, id=building_id)

@router.put('/{building_id}', response_model=BuildingSchema.Read)
def update_building(
    building_id: int, building: BuildingSchema.Update,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context, model_name='Building', resource_id=building_id)
    return BuildingController.update_and_commit(db=context.db, schema=building, id=building_id)

@router.post('/{building_id}/units/', response_model=UnitSchema.Read)
def create_unit(
    building_id: int, unit: UnitSchema.Create,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context, model_name='Building', resource_id=building_id)
    return UnitController.create_and_commit(db=context.db, schema=unit, parent_id=building_id)

@router.get('/{building_id}/units/', response_model=PaginatedResults)
def read_units(
    building_id: int, skip: int = 0, limit: int = 10,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context, model_name='Building', resource_id=building_id)
    results = UnitController.get_all_paginated(db=context.db, parent_id=building_id, skip=skip, limit=limit)
    return serialize_results(results, UnitSchema.Read)
