from schemas import UnitSchema
from db.models import Unit
from schemas.request import PaginatedResults, RequestContext
from . import base

def get_by_id(context: RequestContext, id: int) -> Unit | None:
    return base.get_by_id(context=context, model=Unit, id=id)

def get_all(context: RequestContext, skip: int = 0, limit: int = 10) -> PaginatedResults:
    return base.get_all(context=context, model=Unit, skip=skip, limit=limit)

def get_all_from_parent(context: RequestContext, parent_id: int, skip: int = 0, limit: int = 10) -> PaginatedResults:
    return base.get_all_from_parent(context=context, model=Unit, parent_key='building_id', parent_value=parent_id, skip=skip, limit=limit)

def create_and_commit(context: RequestContext, schema: UnitSchema.Create, parent_id: int) -> Unit | None:
    return base.create_and_commit(context=context, model=Unit, schema=schema, parent_key='building_id', parent_value=parent_id)

def update_and_commit(context: RequestContext, schema: UnitSchema.Update, id: int) -> Unit | None:
    return base.update_and_commit(context=context, model=Unit, schema=schema, id=id)
