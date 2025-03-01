from fastapi import APIRouter, Depends
from app.api.v1.deps import (
    get_request_context,
    serialize_results,
    PaginatedResults,
    RequestContext,
)
from controllers import PropertyController, BuildingController
from schemas import PropertySchema, BuildingSchema

router: APIRouter = APIRouter()

@router.post('/', response_model=PropertySchema.Read)
def create(
    property: PropertySchema.Create,
    context: RequestContext = Depends(get_request_context),
):
    return PropertyController.create_and_commit(context=context, schema=property)

@router.get('/', response_model=PaginatedResults)
def index(
    skip: int = 0, limit: int = 10,
    context: RequestContext = Depends(get_request_context),
):
    results = PropertyController.get_all(context=context, skip=skip, limit=limit)
    return serialize_results(results, PropertySchema.Read)

@router.get('/{property_id}', response_model=PropertySchema.Read)
def read(
    property_id: int,
    context: RequestContext = Depends(get_request_context),
):
    return PropertyController.get_by_id(context=context, id=property_id)

@router.put('/{property_id}', response_model=PropertySchema.Read)
def update(
    property_id: int, property: PropertySchema.Update,
    context: RequestContext = Depends(get_request_context),
):
    return PropertyController.update_and_commit(context=context, schema=property, id=property_id)

@router.get('/{property_id}/buildings/', response_model=PaginatedResults)
def subindex(
    property_id: int, skip: int = 0, limit: int = 10,
    context: RequestContext = Depends(get_request_context),
):
    results = BuildingController.get_all_from_parent(context=context, parent_id=property_id, skip=skip, limit=limit)
    return serialize_results(results, BuildingSchema.Read)
