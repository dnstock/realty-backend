from sqlalchemy.exc import NoResultFound, MultipleResultsFound, IntegrityError
from sqlalchemy.sql import exists
from typing import Type, Any
from core.logger import log_exception
from schemas.base import BaseModel
from schemas.request import AllResults, PaginatedResults, RequestContext
from db import T

## HEIRARCHY OF RESOURCES
# Manager -> Property -> Building -> Unit -> Lease -> Tenant -> Insurance
# Note: Manager is an authenticated end user
##

def exists_where(context: RequestContext, model: Type[T], key: str, val: Any) -> bool:
    return context.db.query(exists().where(getattr(model, key) == val)).scalar()

def get_by(context: RequestContext, model: Type[T], key: str, val: Any) -> T | None:
    try:
        return context.db.query(model).filter(getattr(model, key) == val).one()
    except NoResultFound as exc:
        log_exception(exc, f'No {model} record found where {key} = {val}')
        return None
    except MultipleResultsFound as exc:
        log_exception(exc, f'Multiple {model} records found where {key} = {val}')
        return None

def get_by_id(context: RequestContext, model: Type[T], id: int) -> T | None:
    return get_by(context=context, model=model, key='id', val=id)

def get_all_unpaginated(context: RequestContext, model: Type[T], parent_key: str, parent_value: int) -> AllResults:
    query = context.db.query(model).filter(getattr(model, parent_key) == parent_value)
    rowCount = query.count()
    rows = query.all()
    return AllResults(rows=rows, rowCount=rowCount)

def get_all(context: RequestContext, model: Type[T], skip: int = 0, limit: int = 10) -> PaginatedResults:
    query = context.db.query(model)
    rowCount = query.count()
    rows = query.offset(skip).limit(limit).all()
    return PaginatedResults(rows=rows, rowCount=rowCount, pageStart=min(skip, rowCount), pageEnd=min(skip + limit, rowCount))

def get_all_from_parent(context: RequestContext, model: Type[T], parent_key: str, parent_value: int, skip: int = 0, limit: int = 10) -> PaginatedResults:
    query = context.db.query(model).filter(getattr(model, parent_key) == parent_value)
    rowCount = query.count()
    rows = query.offset(skip).limit(limit).all()
    return PaginatedResults(rows=rows, rowCount=rowCount, pageStart=min(skip, rowCount), pageEnd=min(skip + limit, rowCount))

def create_and_commit(context: RequestContext, model: Type[T], schema: BaseModel, parent_key: str | None, parent_value: int | None) -> T | None:
    try:
        db_obj = model(**schema.model_dump(exclude_unset=True))
        setattr(db_obj, parent_key, parent_value) if parent_key else None
        context.db.add(db_obj)
        context.db.commit()
        context.db.refresh(db_obj)
        return db_obj
    except IntegrityError as exc:
        log_exception(exc, 'Database integrity error occurred')
        context.db.rollback()
        return None
    except Exception as exc:
        log_exception(exc, 'An error occurred')
        context.db.rollback()
        return None

def update_and_commit(context: RequestContext, model: Type[T], schema: BaseModel, id: int) -> T | None:
    try:
        db_obj = context.db.query(model).filter(getattr(model, 'id') == id).one()

        primary_key = {str(key.name) for key in model.__table__.primary_key}
        foreign_keys = {str(key.name) for key in model.__table__.foreign_keys}

        for key, value in schema.model_dump(
            exclude_unset=True,
            exclude=primary_key | foreign_keys,
        ).items():
            setattr(db_obj, key, value)

        context.db.commit()
        context.db.refresh(db_obj)
        return db_obj
    except NoResultFound as exc:
        log_exception(exc, f'No record found for id {id}')
        return None
    except MultipleResultsFound as exc:
        log_exception(exc, f'Multiple records found for id {id}')
        return None
    except IntegrityError as exc:
        log_exception(exc, 'Database integrity error occurred.')
        context.db.rollback()
        return None
    except Exception as exc:
        log_exception(exc, 'An error occurred')
        context.db.rollback()
        return None
