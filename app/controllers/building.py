from sqlalchemy.orm import Session
from schemas import BuildingSchema
from db.models import Building
from schemas.request import PaginatedResults
from . import base

def get_by_id(db: Session, id: int) -> Building | None:
    return base.get_by_id(db=db, model=Building, id=id)

def get_all(db: Session, skip: int = 0, limit: int = 10) -> PaginatedResults:
    return base.get_all(db=db, model=Building, skip=skip, limit=limit)

def get_all_from_parent(db: Session, parent_id: int, skip: int = 0, limit: int = 10) -> PaginatedResults:
    return base.get_all_from_parent(db=db, model=Building, parent_key='property_id', parent_value=parent_id, skip=skip, limit=limit)

def create_and_commit(db: Session, schema: BuildingSchema.Create, parent_id: int) -> Building | None:
    return base.create_and_commit(db=db, model=Building, schema=schema, parent_key='property_id', parent_value=parent_id)

def update_and_commit(db: Session, schema: BuildingSchema.Update, id: int) -> Building | None:
    return base.update_and_commit(db=db, model=Building, schema=schema, id=id)
