from schemas import InsuranceSchema
from db.models import Insurance
from schemas.request import PaginatedResults, RequestContext
from . import base

def get_by_id(context: RequestContext, id: int) -> Insurance | None:
    return base.get_by_id(context=context, model=Insurance, id=id)

def get_all(context: RequestContext, skip: int = 0, limit: int = 10) -> PaginatedResults:
    return base.get_all(context=context, model=Insurance, skip=skip, limit=limit)

def get_all_from_parent(context: RequestContext, parent_id: int, skip: int = 0, limit: int = 10) -> PaginatedResults:
    return base.get_all_from_parent(context=context, model=Insurance, parent_key='tenant_id', parent_value=parent_id, skip=skip, limit=limit)

def create_and_commit(context: RequestContext, schema: InsuranceSchema.Create, parent_id: int) -> Insurance | None:
    return base.create_and_commit(context=context, model=Insurance, schema=schema, parent_key='tenant_id', parent_value=parent_id)

def update_and_commit(context: RequestContext, schema: InsuranceSchema.Update, id: int) -> Insurance | None:
    return base.update_and_commit(context=context, model=Insurance, schema=schema, id=id)
