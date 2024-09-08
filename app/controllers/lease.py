from typing import Optional, List
from schemas import LeaseSchema
from db.models import Lease
from . import base

def get_by_id(id: int) -> Optional[Lease]:
    return base.get_by_id(model=Lease, id=id)

def get_all(parent_id: int, skip: int = 0, limit: int = 10) -> List[Lease]:
    return base.get_all(model=Lease, parent_key="unit_id", parent_value=parent_id, skip=skip, limit=limit)

def create_and_commit(schema: LeaseSchema.Create, parent_id: int) -> Optional[Lease]:
    return base.create_and_commit(model=Lease, schema=schema, parent_key="unit_id", parent_value=parent_id)

def update_and_commit(schema: LeaseSchema.Update, id: int) -> Optional[Lease]:
    return base.update_and_commit(model=Lease, schema=schema, id=id)
