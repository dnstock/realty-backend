from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers import UnitController
from schemas import UnitSchema
from app.api.v1.deps import get_db, validate_ownership

router: APIRouter = APIRouter()

@router.post("/buildings/{building_id}/units/", response_model=UnitSchema.Read)
def create_unit(
    building_id: int, unit: UnitSchema.Create, db: Session = Depends(get_db), 
    # _ = Depends(lambda: validate_ownership(model_name="Building", resource_id=building_id))
):
    return UnitController.create_and_commit(db=db, schema=unit, parent_id=building_id)

@router.get("/buildings/{building_id}/units/", response_model=list[UnitSchema.Read])
def read_units(
    building_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), 
    # _ = Depends(lambda: validate_ownership(model_name="Building", resource_id=building_id))
):
    return UnitController.get_all(db=db, parent_id=building_id, skip=skip, limit=limit)

@router.get("/units/{unit_id}", response_model=UnitSchema.Read)
def read_unit(
    unit_id: int, db: Session = Depends(get_db), 
    # _ = Depends(lambda: validate_ownership(model_name="Unit", resource_id=unit_id))
):
    return UnitController.get_by_id(db=db, id=unit_id)

@router.put("/units/{unit_id}", response_model=UnitSchema.Read)
def update_unit(
    unit_id: int, unit: UnitSchema.Update, db: Session = Depends(get_db), 
    # _ = Depends(lambda: validate_ownership(model_name="Unit", resource_id=unit_id))
):
    return UnitController.update_and_commit(db=db, schema=unit, id=unit_id)