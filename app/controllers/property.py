from schemas import PropertySchema
from db.models import Property
from schemas.request import PaginatedResults, RequestContext
from . import base

def get_by_id(context: RequestContext, id: int) -> Property | None:
    return base.get_by_id(context=context, model=Property, id=id)

def get_all(context: RequestContext, skip: int = 0, limit: int = 10) -> PaginatedResults:
    return base.get_all(context=context, model=Property, skip=skip, limit=limit)

def create_and_commit(context: RequestContext, schema: PropertySchema.Create) -> Property | None:
    return base.create_and_commit(context=context, model=Property, schema=schema, parent_key=None, parent_value=None)

def update_and_commit(context: RequestContext, schema: PropertySchema.Update, id: int) -> Property | None:
    return base.update_and_commit(context=context, model=Property, schema=schema, id=id)
