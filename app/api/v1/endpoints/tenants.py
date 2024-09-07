from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers import TenantController
from schemas import TenantSchema
from app.api.v1.deps import get_db, validate_ownership

router: APIRouter = APIRouter()

@router.post("/leases/{lease_id}/tenants/", response_model=TenantSchema.Read)
def create_tenant(
    lease_id: int, tenant: TenantSchema.Create, db: Session = Depends(get_db), 
    # _ = Depends(lambda: validate_ownership(model_name="Lease", resource_id=lease_id))
):
    return TenantController.create_and_commit(db=db, schema=tenant, parent_id=lease_id)

@router.get("/leases/{lease_id}/tenants/", response_model=list[TenantSchema.Read])
def read_tenants(
    lease_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), 
    # _ = Depends(lambda: validate_ownership(model_name="Lease", resource_id=lease_id))
):
    return TenantController.get_all(db=db, parent_id=lease_id, skip=skip, limit=limit)

@router.get("/tenants/{tenant_id}", response_model=TenantSchema.Read)
def read_tenant(
    tenant_id: int, db: Session = Depends(get_db), 
    # _ = Depends(lambda: validate_ownership(model_name="Tenant", resource_id=tenant_id))
):
    return TenantController.get_by_id(db=db, id=tenant_id)

@router.put("/tenants/{tenant_id}", response_model=TenantSchema.Read)
def update_tenant(
    tenant_id: int, tenant: TenantSchema.Update, db: Session = Depends(get_db), 
    # _ = Depends(lambda: validate_ownership(model_name="Tenant", resource_id=tenant_id))
):
    return TenantController.update_and_commit(db=db, schema=tenant, id=tenant_id)