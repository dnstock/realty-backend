from schemas import BuildingSchema
from db.models import Building
from schemas.request import PaginatedResults, RequestContext
from . import base

def get_by_id(context: RequestContext, id: int) -> Building | None:
    return base.get_by_id(context=context, model=Building, id=id)

def get_all(context: RequestContext, skip: int = 0, limit: int = 10) -> PaginatedResults:
    return base.get_all(context=context, model=Building, skip=skip, limit=limit)

def get_all_from_parent(context: RequestContext, parent_id: int, skip: int = 0, limit: int = 10) -> PaginatedResults:
    return base.get_all_from_parent(context=context, model=Building, parent_key='property_id', parent_value=parent_id, skip=skip, limit=limit)

def create_and_commit(context: RequestContext, schema: BuildingSchema.Create, parent_id: int) -> Building | None:
    return base.create_and_commit(context=context, model=Building, schema=schema, parent_key='property_id', parent_value=parent_id)

def update_and_commit(context: RequestContext, schema: BuildingSchema.Update, id: int) -> Building | None:
    return base.update_and_commit(context=context, model=Building, schema=schema, id=id)
