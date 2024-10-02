from fastapi import APIRouter, Depends
from controllers import PropertyController, BuildingController
from schemas import PropertySchema, UserSchema, BuildingSchema
from schemas.base import PaginatedResults
from app.api.v1.deps import get_current_active_user, authorize_access, serialize_results

router: APIRouter = APIRouter()

def validate_property_ownership(property_id: int, current_user: UserSchema.Read) -> None:
    authorize_access(model_name='Property', resource_id=property_id, current_user=current_user)

@router.post('/', response_model=PropertySchema.Read)
def create_property(
    property: PropertySchema.Create,
    current_user: UserSchema.Read = Depends(get_current_active_user)
):
    return PropertyController.create_and_commit(schema=property, parent_id=current_user.id)

@router.get('/', response_model=PaginatedResults)
def read_properties(
    skip: int = 0, limit: int = 10,
    current_user: UserSchema.Read = Depends(get_current_active_user)
):
    results = PropertyController.get_all_paginated(parent_id=current_user.id, skip=skip, limit=limit)
    return serialize_results(results, PropertySchema.Read)

@router.get('/{property_id}', response_model=PropertySchema.Read)
def read_property(
    property_id: int,
    current_user: UserSchema.Read = Depends(get_current_active_user)
):
    authorize_access(model_name='Property', resource_id=property_id, current_user=current_user)
    return PropertyController.get_by_id(id=property_id)

@router.put('/{property_id}', response_model=PropertySchema.Read)
def update_property(
    property_id: int, property: PropertySchema.Update, 
    _: None = Depends(validate_property_ownership)
    # _ = Depends(lambda: validate_ownership(model_name='Property', resource_id=property_id))
):
    return PropertyController.update_and_commit(schema=property, id=property_id)

@router.post('/{property_id}/buildings/', response_model=BuildingSchema.Read)
def create_building(
    property_id: int, building: BuildingSchema.Create, 
    current_user: UserSchema.Read = Depends(get_current_active_user)
    # _ = Depends(lambda: validate_ownership(model_name='Property', resource_id=property_id))
):
    return BuildingController.create_and_commit(schema=building, parent_id=property_id)

@router.get('/{property_id}/buildings/', response_model=PaginatedResults)
def read_buildings(
    property_id: int, skip: int = 0, limit: int = 10, 
    # _ = Depends(lambda: validate_ownership(model_name='Property', resource_id=property_id))
):
    results = BuildingController.get_all_paginated(parent_id=property_id, skip=skip, limit=limit)
    return serialize_results(results, BuildingSchema.Read)
