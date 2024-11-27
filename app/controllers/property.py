from sqlalchemy.orm import Session
from typing import Optional
from schemas import PropertySchema
from db.models import Property
from schemas.base import PaginatedResults
from . import base

def get_by_id(db: Session, id: int) -> Optional[Property]:
    return base.get_by_id(db=db, model=Property, id=id)

def get_all_paginated(db: Session, parent_id: int, skip: int = 0, limit: int = 10) -> PaginatedResults:
    return base.get_all_paginated(db=db, model=Property, parent_key='manager_id', parent_value=parent_id, skip=skip, limit=limit)

def create_and_commit(db: Session, schema: PropertySchema.Create, parent_id: int) -> Optional[Property]:
    return base.create_and_commit(db=db, model=Property, schema=schema, parent_key='manager_id', parent_value=parent_id)

def update_and_commit(db: Session, schema: PropertySchema.Update, id: int) -> Optional[Property]:
    return base.update_and_commit(db=db, model=Property, schema=schema)
