from sqlalchemy.orm import Session
from schemas import LeaseSchema
from db.models import Lease
from schemas.request import PaginatedResults
from . import base

def get_by_id(db: Session, id: int) -> Lease | None:
    return base.get_by_id(db=db, model=Lease, id=id)

def get_all(db: Session, skip: int = 0, limit: int = 10) -> PaginatedResults:
    return base.get_all(db=db, model=Lease, skip=skip, limit=limit)

def get_all_from_parent(db: Session, parent_id: int, skip: int = 0, limit: int = 10) -> PaginatedResults:
    return base.get_all_from_parent(db=db, model=Lease, parent_key='unit_id', parent_value=parent_id, skip=skip, limit=limit)

def create_and_commit(db: Session, schema: LeaseSchema.Create, parent_id: int) -> Lease | None:
    return base.create_and_commit(db=db, model=Lease, schema=schema, parent_key='unit_id', parent_value=parent_id)

def update_and_commit(db: Session, schema: LeaseSchema.Update, id: int) -> Lease | None:
    return base.update_and_commit(db=db, model=Lease, schema=schema, id=id)
