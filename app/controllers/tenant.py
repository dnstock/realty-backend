from typing import Optional
from schemas import TenantSchema
from db.models import Tenant
from schemas.base import PaginatedResults
from . import base

def get_by_id(id: int) -> Optional[Tenant]:
    return base.get_by_id(model=Tenant, id=id)

def get_all_paginated(parent_id: int, skip: int = 0, limit: int = 10) -> PaginatedResults:
    return base.get_all_paginated(model=Tenant, parent_key="lease_id", parent_value=parent_id, skip=skip, limit=limit)

def create_and_commit(schema: TenantSchema.Create, parent_id: int) -> Optional[Tenant]:
    return base.create_and_commit(model=Tenant, schema=schema, parent_key="lease_id", parent_value=parent_id)

def update_and_commit(schema: TenantSchema.Update, id: int) -> Optional[Tenant]:
    return base.update_and_commit(model=Tenant, schema=schema, id=id)
