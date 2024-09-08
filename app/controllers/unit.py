from typing import Optional, List
from schemas import UnitSchema
from db.models import Unit
from . import base

def get_by_id(id: int) -> Optional[Unit]:
    return base.get_by_id(model=Unit, id=id)

def get_all(parent_id: int, skip: int = 0, limit: int = 10) -> List[Unit]:
    return base.get_all(model=Unit, parent_key="building_id", parent_value=parent_id, skip=skip, limit=limit)

def create_and_commit(schema: UnitSchema.Create, parent_id: int) -> Optional[Unit]:
    return base.create_and_commit(model=Unit, schema=schema, parent_key="building_id", parent_value=parent_id)

def update_and_commit(schema: UnitSchema.Update, id: int) -> Optional[Unit]:
    return base.update_and_commit(model=Unit, schema=schema, id=id)
