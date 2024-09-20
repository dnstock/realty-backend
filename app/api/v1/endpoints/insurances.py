from fastapi import APIRouter
from controllers import InsuranceController
from schemas import InsuranceSchema
# from app.api.v1.deps import validate_ownership

router: APIRouter = APIRouter()

@router.get("/{insurance_id}", response_model=InsuranceSchema.Read)
def read_insurance(
    insurance_id: int, 
    # _ = Depends(lambda: validate_ownership(model_name="Insurance", resource_id=insurance_id))
):
    return InsuranceController.get_by_id(id=insurance_id)

@router.put("/{insurance_id}", response_model=InsuranceSchema.Read)
def update_insurance(
    insurance_id: int, insurance: InsuranceSchema.Update, 
    # _ = Depends(lambda: validate_ownership(model_name="Insurance", resource_id=insurance_id))
):
    return InsuranceController.update_and_commit(schema=insurance, id=insurance_id)