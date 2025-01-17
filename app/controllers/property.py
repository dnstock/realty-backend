from sqlalchemy.orm import Session
from schemas import PropertySchema
from db.models import Property
from schemas.request import PaginatedResults
from . import base

def get_by_id(db: Session, id: int) -> Property | None:
    return base.get_by_id(db=db, model=Property, id=id)

def get_all_paginated(db: Session, parent_id: int, skip: int = 0, limit: int = 10) -> PaginatedResults:
    return base.get_all_paginated(db=db, model=Property, parent_key='manager_id', parent_value=parent_id, skip=skip, limit=limit)

def create_and_commit(db: Session, schema: PropertySchema.Create) -> Property | None:
    return base.create_and_commit(db=db, model=Property, schema=schema, parent_key=None, parent_value=None)

def update_and_commit(db: Session, schema: PropertySchema.Update, id: int) -> Property | None:
    return base.update_and_commit(db=db, model=Property, schema=schema, id=id)
