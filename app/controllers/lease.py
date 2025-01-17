from schemas import LeaseSchema
from db.models import Lease
from schemas.request import PaginatedResults, RequestContext
from . import base

def get_by_id(context: RequestContext, id: int) -> Lease | None:
    return base.get_by_id(context=context, model=Lease, id=id)

def get_all(context: RequestContext, skip: int = 0, limit: int = 10) -> PaginatedResults:
    return base.get_all(context=context, model=Lease, skip=skip, limit=limit)

def get_all_from_parent(context: RequestContext, parent_id: int, skip: int = 0, limit: int = 10) -> PaginatedResults:
    return base.get_all_from_parent(context=context, model=Lease, parent_key='unit_id', parent_value=parent_id, skip=skip, limit=limit)

def create_and_commit(context: RequestContext, schema: LeaseSchema.Create, parent_id: int) -> Lease | None:
    return base.create_and_commit(context=context, model=Lease, schema=schema, parent_key='unit_id', parent_value=parent_id)

def update_and_commit(context: RequestContext, schema: LeaseSchema.Update, id: int) -> Lease | None:
    return base.update_and_commit(context=context, model=Lease, schema=schema, id=id)
