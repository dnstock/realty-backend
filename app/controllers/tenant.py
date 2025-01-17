from schemas import TenantSchema
from db.models import Tenant
from schemas.request import PaginatedResults, RequestContext
from . import base

def get_by_id(context: RequestContext, id: int) -> Tenant | None:
    return base.get_by_id(context=context, model=Tenant, id=id)

def get_all(context: RequestContext, skip: int = 0, limit: int = 10) -> PaginatedResults:
    return base.get_all(context=context, model=Tenant, skip=skip, limit=limit)

def get_all_from_parent(context: RequestContext, parent_id: int, skip: int = 0, limit: int = 10) -> PaginatedResults:
    return base.get_all_from_parent(context=context, model=Tenant, parent_key='lease_id', parent_value=parent_id, skip=skip, limit=limit)

def create_and_commit(context: RequestContext, schema: TenantSchema.Create, parent_id: int) -> Tenant | None:
    return base.create_and_commit(context=context, model=Tenant, schema=schema, parent_key='lease_id', parent_value=parent_id)

def update_and_commit(context: RequestContext, schema: TenantSchema.Update, id: int) -> Tenant | None:
    return base.update_and_commit(context=context, model=Tenant, schema=schema, id=id)
