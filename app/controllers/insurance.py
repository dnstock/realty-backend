from sqlalchemy.orm import Session
from typing import Optional
from schemas import InsuranceSchema
from db.models import Insurance
from schemas.base import PaginatedResults
from . import base

def get_by_id(db: Session, id: int) -> Optional[Insurance]:
    return base.get_by_id(db=db, model=Insurance, id=id)

def get_all_paginated(db: Session, parent_id: int, skip: int = 0, limit: int = 10) -> PaginatedResults:
    return base.get_all_paginated(db=db, model=Insurance, parent_key='tenant_id', parent_value=parent_id, skip=skip, limit=limit)

def create_and_commit(db: Session, schema: InsuranceSchema.Create, parent_id: int) -> Optional[Insurance]:
    return base.create_and_commit(db=db, model=Insurance, schema=schema, parent_key='tenant_id', parent_value=parent_id)

def update_and_commit(db: Session, schema: InsuranceSchema.Update, id: int) -> Optional[Insurance]:
    return base.update_and_commit(db=db, model=Insurance, schema=schema, id=id)
