from fastapi import APIRouter, Depends
from app.api.v1.deps import (
    get_request_context,
    validate_ownership,
    serialize_results,
    PaginatedResults,
    RequestContext,
)
from controllers import PropertyController, BuildingController
from schemas import PropertySchema, BuildingSchema

router: APIRouter = APIRouter()

@router.post('/', response_model=PropertySchema.Read)
def create_property(
    property: PropertySchema.Create,
    context: RequestContext = Depends(get_request_context),
):
    return PropertyController.create_and_commit(db=context.db, schema=property, parent_id=context.get_user_id())

@router.get('/', response_model=PaginatedResults)
def read_properties(
    skip: int = 0, limit: int = 10,
    context: RequestContext = Depends(get_request_context),
):
    results = PropertyController.get_all_paginated(db=context.db, parent_id=context.get_user_id(), skip=skip, limit=limit)
    return serialize_results(results, PropertySchema.Read)

@router.get('/{property_id}', response_model=PropertySchema.Read)
def read_property(
    property_id: int,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context,model_name='Property', resource_id=property_id)
    return PropertyController.get_by_id(db=context.db, id=property_id)

@router.put('/{property_id}', response_model=PropertySchema.Read)
def update_property(
    property_id: int, property: PropertySchema.Update,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context, model_name='Property', resource_id=property_id)
    return PropertyController.update_and_commit(db=context.db, schema=property, id=property_id)

@router.post('/{property_id}/buildings/', response_model=BuildingSchema.Read)
def create_building(
    property_id: int, building: BuildingSchema.Create,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context, model_name='Property', resource_id=property_id)
    return BuildingController.create_and_commit(db=context.db, schema=building, parent_id=property_id)

@router.get('/{property_id}/buildings/', response_model=PaginatedResults)
def read_buildings(
    property_id: int, skip: int = 0, limit: int = 10,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context, model_name='Property', resource_id=property_id)
    results = BuildingController.get_all_paginated(db=context.db, parent_id=property_id, skip=skip, limit=limit)
    return serialize_results(results, BuildingSchema.Read)
