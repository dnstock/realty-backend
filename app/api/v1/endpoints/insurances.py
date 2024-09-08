from fastapi import APIRouter
from controllers import InsuranceController
from schemas import InsuranceSchema
from app.api.v1.deps import validate_ownership

router: APIRouter = APIRouter()

@router.post("/tenants/{tenant_id}/insurances/", response_model=InsuranceSchema.Read)
def create_insurance(
    tenant_id: int, insurance: InsuranceSchema.Create, 
    # _ = Depends(lambda: validate_ownership(model_name="Tenant", resource_id=tenant_id))
):
    return InsuranceController.create_and_commit(schema=insurance, parent_id=tenant_id)

@router.get("/tenants/{tenant_id}/insurances/", response_model=list[InsuranceSchema.Read])
def read_insurances(
    tenant_id: int, skip: int = 0, limit: int = 10, 
    # _ = Depends(lambda: validate_ownership(model_name="Tenant", resource_id=tenant_id))
):
    return InsuranceController.get_all(parent_id=tenant_id, skip=skip, limit=limit)

@router.get("/insurances/{insurance_id}", response_model=InsuranceSchema.Read)
def read_insurance(
    insurance_id: int, 
    # _ = Depends(lambda: validate_ownership(model_name="Insurance", resource_id=insurance_id))
):
    return InsuranceController.get_by_id(id=insurance_id)

@router.put("/insurances/{insurance_id}", response_model=InsuranceSchema.Read)
def update_insurance(
    insurance_id: int, insurance: InsuranceSchema.Update, 
    # _ = Depends(lambda: validate_ownership(model_name="Insurance", resource_id=insurance_id))
):
    return InsuranceController.update_and_commit(schema=insurance, id=insurance_id)