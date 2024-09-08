from fastapi import APIRouter, Depends
from controllers import PropertyController
from schemas import PropertySchema, UserSchema
from app.api.v1.deps import get_current_active_user, validate_ownership

router: APIRouter = APIRouter()

def validate_property_ownership(property_id: int) -> None:
    validate_ownership(model_name="Property", resource_id=property_id)

@router.post("/properties/", response_model=PropertySchema.Read)
def create_property(
    property: PropertySchema.Create,
    current_user: UserSchema.Read = Depends(get_current_active_user)
):
    return PropertyController.create_and_commit(schema=property, parent_id=current_user.id)

@router.get("/properties/", response_model=list[PropertySchema.Read])
def read_properties(
    skip: int = 0, limit: int = 10, 
    current_user: UserSchema.Read = Depends(get_current_active_user)
):
    return PropertyController.get_all(parent_id=current_user.id, skip=skip, limit=limit)

@router.get("/properties/{property_id}", response_model=PropertySchema.Read)
def read_property(
    property_id: int,
    _: None = Depends(validate_property_ownership)
):
    return PropertyController.get_by_id(id=property_id)

@router.put("/properties/{property_id}", response_model=PropertySchema.Read)
def update_property(
    property_id: int, property: PropertySchema.Update, 
    _: None = Depends(validate_property_ownership)
    # _ = Depends(lambda: validate_ownership(model_name="Property", resource_id=property_id))
):
    return PropertyController.update_and_commit(schema=property, id=property_id)
