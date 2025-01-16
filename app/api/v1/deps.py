from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Type, Any
from functools import lru_cache
from core.oauth2 import get_current_user, get_current_user_optional
from schemas.user import Read as CurrentUser
from schemas.request import PaginatedResults, RequestContext
from schemas.base import T
from db import models, get_db
from core.logger import logger, log_exception

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

# Static mapping of model paths to manager_id
OWNER_PATHS = {
    'Property': 'manager_id',
    'Building': 'property.manager_id',
    'Unit': 'building.property.manager_id',
    'Lease': 'unit.building.property.manager_id',
    'Tenant': 'lease.unit.building.property.manager_id',
    'Insurance': 'tenant.lease.unit.building.property.manager_id',
}

# Validate ownership of parent resource
def validate_ownership(
    model_name: str,
    resource_id: int,
    context: RequestContext = Depends(get_request_context),
) -> None:
    @lru_cache(maxsize=128)
    def get_owner_id(obj: Any, path: str) -> int:
        """Navigate object relationships using cached path"""
        value = obj
        for attr in path.split('.'):
            value = getattr(value, attr)
        return value

    access_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f'Not authorized to access this {model_name}'
    )

    try:
        # Get model and validate existence
        model_class = getattr(models, model_name)
        db_obj = context.db.query(model_class).filter_by(id=resource_id).one_or_none()
        if not db_obj:
            raise access_exception

        # Get and validate owner path
        owner_path = OWNER_PATHS.get(model_name)
        if not owner_path:
            logger.error(f'Ownership validation not supported for {model_name}')
            raise access_exception

        # Compare owner IDs
        if get_owner_id(db_obj, owner_path) != context.get_user_id():
            logger.warning(f'User {context.get_user_id()} denied access to {model_name} {resource_id}')
            raise access_exception

    except Exception as exc:
        log_exception(exc, 'Ownership validation failed')
        raise access_exception
