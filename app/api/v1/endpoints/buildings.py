from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers import BuildingController
from schemas import BuildingSchema
from app.api.v1.deps import get_db, validate_ownership

router: APIRouter = APIRouter()

@router.post("/properties/{property_id}/buildings/", response_model=BuildingSchema.Read)
def create_building(
    property_id: int, building: BuildingSchema.Create, db: Session = Depends(get_db), 
    # _ = Depends(lambda: validate_ownership(model_name="Property", resource_id=property_id))
):
    return BuildingController.create_and_commit(db=db, schema=building, parent_id=property_id)

@router.get("/properties/{property_id}/buildings/", response_model=list[BuildingSchema.Read])
def read_buildings(
    property_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), 
    # _ = Depends(lambda: validate_ownership(model_name="Property", resource_id=property_id))
):
    return BuildingController.get_all(db=db, parent_id=property_id, skip=skip, limit=limit)

@router.get("/buildings/{building_id}", response_model=BuildingSchema.Read)
def read_building(
    building_id: int, db: Session = Depends(get_db), 
    # _ = Depends(lambda: validate_ownership(model_name="Building", resource_id=building_id))
):
    return BuildingController.get_by_id(db=db, id=building_id)

@router.put("/buildings/{building_id}", response_model=BuildingSchema.Read)
def update_building(
    building_id: int, building: BuildingSchema.Update, db: Session = Depends(get_db), 
    # _ = Depends(lambda: validate_ownership(model_name="Building", resource_id=building_id))
):
    return BuildingController.update_and_commit(db=db, schema=building, id=building_id)
