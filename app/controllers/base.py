from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, MultipleResultsFound, IntegrityError
from pydantic import BaseModel
from typing import Type, TypeVar, Optional, List
from core import logger
from db import Base, get_db_session

## HEIRARCHY OF RESOURCES
# Manager -> Property -> Building -> Unit -> Lease -> Tenant -> Insurance
# Note: Manager is an authenticated end user
##

# Define a generic type for models
T = TypeVar('T', bound=Base)

def get_by_id(model: 'Type[T]', id: int, db: Session = get_db_session()) -> 'Optional[T]':
    try:
        return db.query(model).filter(getattr(model, 'id') == id).one()
    except NoResultFound:
        return None
    except MultipleResultsFound:
        return None

def get_all(model: Type[T], parent_key: str, parent_value: int, skip: int = 0, limit: int = 10, db: Session = get_db_session()) -> List[T]:
    return db.query(model).filter(getattr(model, parent_key) == parent_value).offset(skip).limit(limit).all()

def create_and_commit(model: Type[T], schema: BaseModel, parent_key: str, parent_value: int, db: Session = get_db_session()) -> Optional[T]:
    try:
        db_obj = model(**schema.model_dump())
        db_obj.__setattr__(parent_key, parent_value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except IntegrityError as e:
        db.rollback()
        logger.error(f"IntegrityError: {e}")
        return None
    except Exception as e:
        db.rollback()
        logger.error(f"An error occurred: {e}")
        return None

def update_and_commit(model: Type[T], schema: BaseModel, id: int, db: Session = get_db_session()) -> Optional[T]:
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
    except NoResultFound:
        logger.error(f"NoResultFound: No record found for id {id}")
        return None
    except MultipleResultsFound:
        logger.error(f"MultipleResultsFound: Multiple records found for id {id}")
        return None
    except IntegrityError as e:
        db.rollback()
        logger.error(f"IntegrityError: {e}")
        return None
    except Exception as e:
        db.rollback()
        logger.error(f"An error occurred: {e}")
        return None
