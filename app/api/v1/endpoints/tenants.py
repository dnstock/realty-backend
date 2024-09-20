from fastapi import APIRouter
from controllers import TenantController, InsuranceController
from schemas import TenantSchema, InsuranceSchema
# from app.api.v1.deps import validate_ownership

router: APIRouter = APIRouter()

@router.get("/{tenant_id}", response_model=TenantSchema.Read)
def read_tenant(
    tenant_id: int, 
    # _ = Depends(lambda: validate_ownership(model_name="Tenant", resource_id=tenant_id))
):
    return TenantController.get_by_id(id=tenant_id)

@router.put("/{tenant_id}", response_model=TenantSchema.Read)
def update_tenant(
    tenant_id: int, tenant: TenantSchema.Update, 
    # _ = Depends(lambda: validate_ownership(model_name="Tenant", resource_id=tenant_id))
):
    return TenantController.update_and_commit(schema=tenant, id=tenant_id)

@router.post("/{tenant_id}/insurances/", response_model=InsuranceSchema.Read)
def create_insurance(
    tenant_id: int, insurance: InsuranceSchema.Create, 
    # _ = Depends(lambda: validate_ownership(model_name="Tenant", resource_id=tenant_id))
):
    return InsuranceController.create_and_commit(schema=insurance, parent_id=tenant_id)

@router.get("/{tenant_id}/insurances/", response_model=list[InsuranceSchema.Read])
def read_insurances(
    tenant_id: int, skip: int = 0, limit: int = 10, 
    # _ = Depends(lambda: validate_ownership(model_name="Tenant", resource_id=tenant_id))
):
    return InsuranceController.get_all(parent_id=tenant_id, skip=skip, limit=limit)

