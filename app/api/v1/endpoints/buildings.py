from fastapi import APIRouter
from controllers import BuildingController, UnitController
from schemas import BaseSchema, BuildingSchema, UnitSchema
from app.api.v1.deps import serialize_results

router: APIRouter = APIRouter()

@router.get("/{building_id}", response_model=BuildingSchema.Read)
def read_building(
    building_id: int, 
    # _ = Depends(lambda: validate_ownership(model_name="Building", resource_id=building_id))
):
    return BuildingController.get_by_id(id=building_id)

@router.put("/{building_id}", response_model=BuildingSchema.Read)
def update_building(
    building_id: int, building: BuildingSchema.Update, 
    # _ = Depends(lambda: validate_ownership(model_name="Building", resource_id=building_id))
):
    return BuildingController.update_and_commit(schema=building, id=building_id)

@router.post("/{building_id}/units/", response_model=UnitSchema.Read)
def create_unit(
    building_id: int, unit: UnitSchema.Create, 
    # _ = Depends(lambda: validate_ownership(model_name="Building", resource_id=building_id))
):
    return UnitController.create_and_commit(schema=unit, parent_id=building_id)

@router.get("/{building_id}/units/", response_model=BaseSchema.PaginatedResults)
def read_units(
    building_id: int, skip: int = 0, limit: int = 10, 
    # _ = Depends(lambda: validate_ownership(model_name="Building", resource_id=building_id))
):
    results = UnitController.get_all_paginated(parent_id=building_id, skip=skip, limit=limit)
    return serialize_results(results, UnitSchema.Read)
