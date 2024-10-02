from typing import Optional
from schemas import PropertySchema
from db.models import Property
from schemas.base import PaginatedResults
from . import base

def get_by_id(id: int) -> Optional[Property]:
    return base.get_by_id(model=Property, id=id)

def get_all_paginated(parent_id: int, skip: int = 0, limit: int = 10) -> PaginatedResults:
    return base.get_all_paginated(model=Property, parent_key="manager_id", parent_value=parent_id, skip=skip, limit=limit)

def create_and_commit(schema: PropertySchema.Create, parent_id: int) -> Optional[Property]:
    return base.create_and_commit(model=Property, schema=schema, parent_key="manager_id", parent_value=parent_id)

def update_and_commit(schema: PropertySchema.Update, id: int) -> Optional[Property]:
    return base.update_and_commit(model=Property, schema=schema, id=id)
