from sqlalchemy.exc import NoResultFound, MultipleResultsFound, IntegrityError
from pydantic import BaseModel
from typing import Type, TypeVar, Optional, List
from core.logger import log_exception
from db import Base, get_db

## HEIRARCHY OF RESOURCES
# Manager -> Property -> Building -> Unit -> Lease -> Tenant -> Insurance
# Note: Manager is an authenticated end user
##

# Define a generic type for models
T = TypeVar('T', bound=Base)

def get_by_id(model: 'Type[T]', id: int) -> 'Optional[T]':
    db = get_db()
    try:
        return db.query(model).filter(getattr(model, 'id') == id).one()
    except NoResultFound as exc:
        log_exception(exc, f"No record found for id {id}")
        return None
    except MultipleResultsFound as exc:
        log_exception(exc, f"Multiple records found for id {id}")
        return None

def get_all(model: Type[T], parent_key: str, parent_value: int, skip: int = 0, limit: int = 10) -> List[T]:
    db = get_db()
    return db.query(model).filter(getattr(model, parent_key) == parent_value).offset(skip).limit(limit).all()

def create_and_commit(model: Type[T], schema: BaseModel, parent_key: str, parent_value: int) -> Optional[T]:
    db = get_db()
    try:
        db_obj = model(**schema.model_dump())
        db_obj.__setattr__(parent_key, parent_value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except IntegrityError as exc:
        log_exception(exc, "Database integrity error occurred")
        db.rollback()
        return None
    except Exception as exc:
        log_exception(exc, "An error occurred")
        db.rollback()
        return None

def update_and_commit(model: Type[T], schema: BaseModel, id: int) -> Optional[T]:
    db = get_db()
    try:
        db_obj = db.query(model).filter(getattr(model, 'id') == id).one()
        
        primary_key = {key.name for key in getattr(model, '__table__').primary_key}
        
        for key, value in schema.model_dump().items():
            if key in primary_key:
                continue
            setattr(db_obj, key, value)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except NoResultFound as exc:
        log_exception(exc, f"No record found for id {id}")
        return None
    except MultipleResultsFound as exc:
        log_exception(exc, f"Multiple records found for id {id}")
        return None
    except IntegrityError as exc:
        log_exception(exc, "Database integrity error occurred.")
        db.rollback()
        return None
    except Exception as exc:
        log_exception(exc, "An error occurred")
        db.rollback()
        return None
