from fastapi import APIRouter
from controllers import UnitController
from schemas import UnitSchema
from app.api.v1.deps import validate_ownership

router: APIRouter = APIRouter()

@router.post("/buildings/{building_id}/units/", response_model=UnitSchema.Read)
def create_unit(
    building_id: int, unit: UnitSchema.Create, 
    # _ = Depends(lambda: validate_ownership(model_name="Building", resource_id=building_id))
):
    return UnitController.create_and_commit(schema=unit, parent_id=building_id)

@router.get("/buildings/{building_id}/units/", response_model=list[UnitSchema.Read])
def read_units(
    building_id: int, skip: int = 0, limit: int = 10, 
    # _ = Depends(lambda: validate_ownership(model_name="Building", resource_id=building_id))
):
    return UnitController.get_all(parent_id=building_id, skip=skip, limit=limit)

@router.get("/units/{unit_id}", response_model=UnitSchema.Read)
def read_unit(
    unit_id: int, 
    # _ = Depends(lambda: validate_ownership(model_name="Unit", resource_id=unit_id))
):
    return UnitController.get_by_id(id=unit_id)

@router.put("/units/{unit_id}", response_model=UnitSchema.Read)
def update_unit(
    unit_id: int, unit: UnitSchema.Update, 
    # _ = Depends(lambda: validate_ownership(model_name="Unit", resource_id=unit_id))
):
    return UnitController.update_and_commit(schema=unit, id=unit_id)