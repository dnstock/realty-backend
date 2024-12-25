from sqlalchemy.orm import Session
from schemas import TenantSchema
from db.models import Tenant
from schemas.request import PaginatedResults
from . import base

def get_by_id(db: Session, id: int) -> Tenant | None:
    return base.get_by_id(db=db, model=Tenant, id=id)

def get_all_paginated(db: Session, parent_id: int, skip: int = 0, limit: int = 10) -> PaginatedResults:
    return base.get_all_paginated(db=db, model=Tenant, parent_key='lease_id', parent_value=parent_id, skip=skip, limit=limit)

def create_and_commit(db: Session, schema: TenantSchema.Create, parent_id: int) -> Tenant | None:
    return base.create_and_commit(db=db, model=Tenant, schema=schema, parent_key='lease_id', parent_value=parent_id)

def update_and_commit(db: Session, schema: TenantSchema.Update, id: int) -> Tenant | None:
    return base.update_and_commit(db=db, model=Tenant, schema=schema)
