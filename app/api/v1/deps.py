from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Type
from core.oauth2 import get_current_user, get_current_user_optional
from schemas.user import Read as CurrentUser
from schemas.request import PaginatedResults, RequestContext
from schemas.base import T
from db import get_db

# Get the current active user and a new database session
def get_request_context(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
) -> RequestContext:
    return RequestContext(db=db, current_user=current_user)

# Get the current active user and a new database session if user is found and token is valid,
# otherwise return only the database session without raising an exception
def get_request_context_optional(
    db: Session = Depends(get_db),
    current_user: CurrentUser | None = Depends(get_current_user_optional)
) -> RequestContext:
    return RequestContext(db=db, current_user=current_user)

# Serialize resultset
def serialize_results(
    results: PaginatedResults,
    schema: Type[T],
) -> PaginatedResults:
    results.rows = [schema.model_validate(item) for item in results.rows]
    return results
