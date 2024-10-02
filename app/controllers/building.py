from typing import Optional
from schemas import BuildingSchema
from db.models import Building
from schemas.base import PaginatedResults
from . import base

def get_by_id(id: int) -> Optional[Building]:
    return base.get_by_id(model=Building, id=id)

def get_all_paginated(parent_id: int, skip: int = 0, limit: int = 10) -> PaginatedResults:
    return base.get_all_paginated(model=Building, parent_key="property_id", parent_value=parent_id, skip=skip, limit=limit)

def create_and_commit(schema: BuildingSchema.Create, parent_id: int) -> Optional[Building]:
    return base.create_and_commit(model=Building, schema=schema, parent_key="property_id", parent_value=parent_id)

def update_and_commit(schema: BuildingSchema.Update, id: int) -> Optional[Building]:
    return base.update_and_commit(model=Building, schema=schema, id=id)
