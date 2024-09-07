from sqlalchemy.orm import Session
from typing import Optional, List
from schemas import UnitSchema
from db.models import Unit
from . import base

def get_by_id(db: Session, id: int) -> Optional[Unit]:
    return base.get_by_id(db=db, model=Unit, id=id)

def get_all(db: Session, parent_id: int, skip: int = 0, limit: int = 10) -> List[Unit]:
    return base.get_all(db=db, model=Unit, parent_key="building_id", parent_value=parent_id, skip=skip, limit=limit)

def create_and_commit(db: Session, schema: UnitSchema.Create, parent_id: int) -> Optional[Unit]:
    return base.create_and_commit(db=db, model=Unit, schema=schema, parent_key="building_id", parent_value=parent_id)

def update_and_commit(db: Session, schema: UnitSchema.Update, id: int) -> Optional[Unit]:
    return base.update_and_commit(db=db, model=Unit, schema=schema, id=id)
