from sqlalchemy.orm import Session
from schemas import PropertySchema
from db.models import Property
from schemas.request import PaginatedResults
from . import base

def get_by_id(db: Session, id: int) -> Property | None:
    return base.get_by_id(db=db, model=Property, id=id)

def get_all(db: Session, skip: int = 0, limit: int = 10) -> PaginatedResults:
    return base.get_all(db=db, model=Property, skip=skip, limit=limit)

def create_and_commit(db: Session, schema: PropertySchema.Create) -> Property | None:
    return base.create_and_commit(db=db, model=Property, schema=schema, parent_key=None, parent_value=None)

def update_and_commit(db: Session, schema: PropertySchema.Update, id: int) -> Property | None:
    return base.update_and_commit(db=db, model=Property, schema=schema, id=id)
