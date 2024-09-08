from fastapi import APIRouter
from controllers import BuildingController
from schemas import BuildingSchema
from app.api.v1.deps import validate_ownership

router: APIRouter = APIRouter()

@router.post("/properties/{property_id}/buildings/", response_model=BuildingSchema.Read)
def create_building(
    property_id: int, building: BuildingSchema.Create, 
    # _ = Depends(lambda: validate_ownership(model_name="Property", resource_id=property_id))
):
    return BuildingController.create_and_commit(schema=building, parent_id=property_id)

@router.get("/properties/{property_id}/buildings/", response_model=list[BuildingSchema.Read])
def read_buildings(
    property_id: int, skip: int = 0, limit: int = 10, 
    # _ = Depends(lambda: validate_ownership(model_name="Property", resource_id=property_id))
):
    return BuildingController.get_all(parent_id=property_id, skip=skip, limit=limit)

@router.get("/buildings/{building_id}", response_model=BuildingSchema.Read)
def read_building(
    building_id: int, 
    # _ = Depends(lambda: validate_ownership(model_name="Building", resource_id=building_id))
):
    return BuildingController.get_by_id(id=building_id)

@router.put("/buildings/{building_id}", response_model=BuildingSchema.Read)
def update_building(
    building_id: int, building: BuildingSchema.Update, 
    # _ = Depends(lambda: validate_ownership(model_name="Building", resource_id=building_id))
):
    return BuildingController.update_and_commit(schema=building, id=building_id)
