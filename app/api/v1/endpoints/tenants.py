from fastapi import APIRouter
from controllers import TenantController
from schemas import TenantSchema
from app.api.v1.deps import validate_ownership

router: APIRouter = APIRouter()

@router.post("/leases/{lease_id}/tenants/", response_model=TenantSchema.Read)
def create_tenant(
    lease_id: int, tenant: TenantSchema.Create, 
    # _ = Depends(lambda: validate_ownership(model_name="Lease", resource_id=lease_id))
):
    return TenantController.create_and_commit(schema=tenant, parent_id=lease_id)

@router.get("/leases/{lease_id}/tenants/", response_model=list[TenantSchema.Read])
def read_tenants(
    lease_id: int, skip: int = 0, limit: int = 10, 
    # _ = Depends(lambda: validate_ownership(model_name="Lease", resource_id=lease_id))
):
    return TenantController.get_all(parent_id=lease_id, skip=skip, limit=limit)

@router.get("/tenants/{tenant_id}", response_model=TenantSchema.Read)
def read_tenant(
    tenant_id: int, 
    # _ = Depends(lambda: validate_ownership(model_name="Tenant", resource_id=tenant_id))
):
    return TenantController.get_by_id(id=tenant_id)

@router.put("/tenants/{tenant_id}", response_model=TenantSchema.Read)
def update_tenant(
    tenant_id: int, tenant: TenantSchema.Update, 
    # _ = Depends(lambda: validate_ownership(model_name="Tenant", resource_id=tenant_id))
):
    return TenantController.update_and_commit(schema=tenant, id=tenant_id)