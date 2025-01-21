from sqlalchemy import select, func
from sqlalchemy.exc import NoResultFound, MultipleResultsFound, IntegrityError
from typing import Type, Any
from core.logger import log_exception
from schemas.base import BaseModel
from schemas.request import AllResults, PaginatedResults, RequestContext
from db import T

def _owned_by(model: Type[T], context: RequestContext):
    return getattr(model, 'owner_id') == context.get_user_id()

def exists_where(context: RequestContext, model: Type[T], key: str, val: Any) -> bool:
    session = context.db
    stmt = select(func.count("*")).select_from(model).where(
        getattr(model, key) == val,
        _owned_by(model, context)
    )
    count = session.scalar(stmt)
    return (count or 0) > 0

def get_by(context: RequestContext, model: Type[T], key: str, val: Any) -> T | None:
    session = context.db
    try:
        stmt = select(model).where(
            getattr(model, key) == val,
            _owned_by(model, context)
        )
        # scalar_one() or scalars(...).one() both raise NoResultFound / MultipleResultsFound
        return session.scalars(stmt).one()
    except NoResultFound as exc:
        log_exception(exc, f'No {model.__name__} record found where {key} = {val}')
        return None
    except MultipleResultsFound as exc:
        log_exception(exc, f'Multiple {model.__name__} records found where {key} = {val}')
        return None

def get_by_id(context: RequestContext, model: Type[T], id: int) -> T | None:
    return get_by(context=context, model=model, key='id', val=id)

def get_all_unpaginated(context: RequestContext, model: Type[T]) -> AllResults:
    session = context.db
    # Count
    count_stmt = select(func.count('*')).select_from(model).where(_owned_by(model, context))
    row_count = session.scalar(count_stmt) or 0

    # Rows
    select_stmt = select(model).where(_owned_by(model, context))
    rows = session.scalars(select_stmt).all()

    return AllResults(rows=rows, rowCount=row_count)

def get_all(context: RequestContext, model: Type[T], skip: int = 0, limit: int = 10) -> PaginatedResults:
    session = context.db
    # Count
    # count_stmt = select(func.count('*')).select_from(model).where(_owned_by(model, context))
    # row_count = session.scalar(count_stmt) or 0
    row_count = 100

    # Paginated rows
    select_stmt = (
        select(model)
        .where(_owned_by(model, context))
        .offset(skip)
        .limit(limit)
    )
    print('+'*50)
    print('GET_ALL SELECT START')
    print('-'*50)
    rows = session.scalars(select_stmt).all()
    print('-'*50)
    print('GET_ALL SELECT END')
    print('+'*50)


    return PaginatedResults(
        rows=rows,
        rowCount=row_count,
        pageStart=min(skip, row_count),
        pageEnd=min(skip + limit, row_count)
    )

def get_all_from_parent(
    context: RequestContext,
    model: Type[T],
    parent_key: str,
    parent_value: int,
    skip: int = 0,
    limit: int = 10
) -> PaginatedResults:
    session = context.db
    # Count
    count_stmt = select(func.count('*')).select_from(model).where(
        getattr(model, parent_key) == parent_value,
        _owned_by(model, context)
    )
    row_count = session.scalar(count_stmt) or 0

    # Paginated rows
    select_stmt = (
        select(model)
        .where(getattr(model, parent_key) == parent_value)
        .where(_owned_by(model, context))
        .offset(skip)
        .limit(limit)
    )
    rows = session.scalars(select_stmt).all()

    return PaginatedResults(
        rows=rows,
        rowCount=row_count,
        pageStart=min(skip, row_count),
        pageEnd=min(skip + limit, row_count)
    )

def create_and_commit(
    context: RequestContext,
    model: Type[T],
    schema: BaseModel,
    parent_key: str | None,
    parent_value: int | None
) -> T | None:
    """Create a new record and commit the changes."""
    session = context.db
    db_obj = model(**schema.model_dump(exclude_unset=True))

    # Ownership + Hierarchical relationships
    if hasattr(db_obj, 'owner_id'):
        setattr(db_obj, 'owner_id', context.get_user_id())
    if parent_key is not None:
        setattr(db_obj, parent_key, parent_value)

    try:
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj
    except IntegrityError as exc:
        log_exception(exc, 'Database integrity error occurred')
        session.rollback()
        return None
    except Exception as exc:
        log_exception(exc, 'An error occurred')
        session.rollback()
        return None

def update_and_commit(context: RequestContext, model: Type[T], schema: BaseModel, id: int) -> T | None:
    session = context.db

    try:
        stmt = select(model).where(
            getattr(model, 'id') == id,
            _owned_by(model, context)
        )
        db_obj = session.scalars(stmt).one()

        # Exclude primary keys and foreign keys from updates
        primary_keys = {col.name for col in model.__table__.primary_key}
        # For complex FKs we might need a different approach, but this is fine for now
        foreign_keys = {fk.parent.name for fk in model.__table__.foreign_keys}

        for key, value in schema.model_dump(
            exclude_unset=True,
            exclude=primary_keys | foreign_keys
        ).items():
            setattr(db_obj, key, value)

        session.commit()
        session.refresh(db_obj)
        return db_obj
    except NoResultFound as exc:
        log_exception(exc, f'No record found for id {id}')
        return None
    except MultipleResultsFound as exc:
        log_exception(exc, f'Multiple records found for id {id}')
        return None
    except IntegrityError as exc:
        log_exception(exc, 'Database integrity error occurred.')
        session.rollback()
        return None
    except Exception as exc:
        log_exception(exc, 'An error occurred')
        session.rollback()
        return None

def delete_and_commit(context: RequestContext, model: Type[T], id: int) -> bool:
    session = context.db

    try:
        stmt = select(model).where(
            getattr(model, 'id') == id,
            _owned_by(model, context)
        )
        db_obj = session.scalars(stmt).one()

        session.delete(db_obj)
        session.commit()
        return True
    except NoResultFound as exc:
        log_exception(exc, f'No record found for id {id}')
        return False
    except MultipleResultsFound as exc:
        log_exception(exc, f'Multiple records found for id {id}')
        return False
    except Exception as exc:
        log_exception(exc, 'An error occurred')
        session.rollback()
        return False
