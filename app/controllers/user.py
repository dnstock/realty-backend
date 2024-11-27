from typing import Any
from sqlalchemy.sql.expression import and_
from sqlalchemy.sql import exists
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from core.logger import log_exception
from schemas import UserSchema
from db.models import User
from sqlalchemy.orm import Session
from schemas.base import PaginatedResults, AllResults

def exists_where(db: Session, key: str, val: Any) -> bool:
    return db.query(exists().where(getattr(User, key) == val)).scalar()

def is_active(db: Session, email: str) -> bool:
    return db.query(exists().where(and_(User.email == email, User.is_active == True))).scalar()

def get_by(db: Session, key: str, val: Any) -> User | None:
    try:
        return db.query(User).filter(getattr(User, key) == val).one()
    except NoResultFound as exc:
        log_exception(exc, f'No User record found where {key} = {val}')
        return None
    except MultipleResultsFound as exc:
        log_exception(exc, f'Multiple User records found where {key} = {val}')
        return None

def get_by_id(db: Session, id: int) -> User | None:
    return get_by(db=db, key='id', val=id)

def get_by_email(db: Session, email: str) -> User | None:
    return get_by(db=db, key='email', val=email)

def get_all(db: Session) -> AllResults:
    query = db.query(User)
    totalCount = query.count()
    rows = query.all()
    return AllResults(rows=rows, totalCount=totalCount)

def get_all_paginated(db: Session, skip: int = 0, limit: int = 10) -> PaginatedResults:
    query = db.query(User)
    totalCount = query.count()
    rows = query.offset(skip).limit(limit).all()
    return PaginatedResults(rows=rows, totalCount=totalCount, pageStart=min(skip, totalCount), pageEnd=min(skip + limit, totalCount))

def create_and_commit(db: Session, schema: UserSchema.Create) -> User | None:
    try:
        db_obj = User(**schema.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except Exception as exc:
        log_exception(exc, 'Error creating user')
        db.rollback()
        return None

def update_and_commit(db: Session, schema: UserSchema.Update) -> User | None:
    try:
        user = db.query(User).filter(User.id == schema.id).one()
        for key, value in schema.model_dump().items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user
    except NoResultFound as exc:
        log_exception(exc, f'No record found for id {id}')
        return None
    except MultipleResultsFound as exc:
        log_exception(exc, f'Multiple records found for id {id}')
        return None
    except Exception as exc:
        log_exception(exc, 'Error updating user')
        db.rollback()
        return None
