from sqlalchemy.orm import Session
from typing import Optional, List
from schemas import BuildingSchema
from db.models import Building
from . import base

def get_by_id(db: Session, id: int) -> Optional[Building]:
    return base.get_by_id(db=db, model=Building, id=id)

def get_all(db: Session, parent_id: int, skip: int = 0, limit: int = 10) -> List[Building]:
    return base.get_all(db=db, model=Building, parent_key="property_id", parent_value=parent_id, skip=skip, limit=limit)

def create_and_commit(db: Session, schema: BuildingSchema.Create, parent_id: int) -> Optional[Building]:
    return base.create_and_commit(db=db, model=Building, schema=schema, parent_key="property_id", parent_value=parent_id)

def update_and_commit(db: Session, schema: BuildingSchema.Update, id: int) -> Optional[Building]:
    return base.update_and_commit(db=db, model=Building, schema=schema, id=id)
