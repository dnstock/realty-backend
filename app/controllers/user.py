from typing import Any
from sqlalchemy import select, exists, and_, func
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from contextlib import contextmanager
from core.logger import log_exception
from schemas import UserSchema
from db.models import User
from sqlalchemy.orm import Session
from schemas.request import PaginatedResults, AllResults

@contextmanager
def transaction(session: Session):
    try:
        yield
        session.commit()
    except Exception as exc:
        session.rollback()
        raise exc

def exists_where(db: Session, key: str, val: Any) -> bool:
    stmt = select(exists().where(getattr(User, key) == val))
    return bool(db.scalar(stmt))

def is_active(db: Session, email: str) -> bool:
    stmt = select(exists().where(and_(
        User.email == email,
        User.is_active.is_(True)
    )))
    return bool(db.scalar(stmt))

def get_by(db: Session, key: str, val: Any) -> User | None:
    try:
        stmt = select(User).where(getattr(User, key) == val)
        return db.scalar(stmt)
    except NoResultFound as exc:
        log_exception(exc, f'No User found where {key} = {val}')
        return None
    except MultipleResultsFound as exc:
        log_exception(exc, f'Multiple Users found where {key} = {val}')
        return None

def get_by_id(db: Session, id: int) -> User | None:
    return get_by(db=db, key='id', val=id)

def get_by_email(db: Session, email: str) -> User | None:
    return get_by(db=db, key='email', val=email)

def get_all(db: Session) -> AllResults:
    stmt = select(User)
    count_stmt = select(func.count()).select_from(User)
    return AllResults(
        rows=db.scalars(stmt).all(),
        rowCount=db.scalar(count_stmt) or 0
    )

def get_all_paginated(
    db: Session,
    skip: int = 0,
    limit: int = 10
) -> PaginatedResults:
    stmt = select(User).offset(skip).limit(limit)
    count_stmt = select(func.count()).select_from(User)
    rowCount = db.scalar(count_stmt) or 0
    return PaginatedResults(
        rows=db.scalars(stmt).all(),
        rowCount=rowCount,
        pageStart=min(skip, rowCount),
        pageEnd=min(skip + limit, rowCount)
    )

def create_and_commit(db: Session, schema: UserSchema.Create) -> User | None:
    try:
        with transaction(db):
            db_obj = User(**schema.model_dump(exclude_unset=True))
            db.add(db_obj)
            db.refresh(db_obj)
            return db_obj
    except Exception as exc:
        log_exception(exc, 'Error creating user')
        return None

def update_and_commit(db: Session, schema: UserSchema.Update, id: int) -> User | None:
    try:
        with transaction(db):
            stmt = select(User).where(User.id == id)
            user = db.scalar(stmt)
            if not user:
                raise NoResultFound

            for key, value in schema.model_dump(
                exclude_unset=True,
                exclude={'id'}
            ).items():
                setattr(user, key, value)

            db.refresh(user)
            return user
    except NoResultFound as exc:
        log_exception(exc, f'No user found with id {id}')
        return None
    except Exception as exc:
        log_exception(exc, f'Error updating user {id}')
        return None

def delete_and_commit(db: Session, id: int) -> bool:
    try:
        with transaction(db):
            stmt = select(User).where(User.id == id)
            user = db.scalar(stmt)
            if not user:
                raise NoResultFound

            db.delete(user)
            return True
    except NoResultFound as exc:
        log_exception(exc, f'No user found with id {id}')
        return False
    except Exception as exc:
        log_exception(exc, f'Error deleting user {id}')
        return False
