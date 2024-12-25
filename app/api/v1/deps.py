from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Type, Callable
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

# Validate ownership of parent resource
def validate_ownership(
    model_name: str,
    resource_id: int,
    context: RequestContext = Depends(get_request_context),
) -> None:
    access_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f'Not authorized to access this {model_name}'
    )
    try:
        db_obj = context.db.query(getattr(models, model_name)).filter_by(id=resource_id).one_or_none()
        if db_obj is None:
            logger.error(f'{model_name} with ID {resource_id} not found')
            raise access_exception

        owner_map: dict[str, Callable[[object], int]] = {
            'Property': lambda obj: obj.manager_id, # type: ignore
            'Building': lambda obj: obj.property.manager_id, # type: ignore
            'Unit': lambda obj: obj.building.property.manager_id, # type: ignore
            'Lease': lambda obj: obj.unit.building.property.manager_id, # type: ignore
            'Tenant': lambda obj: obj.lease.unit.building.property.manager_id, # type: ignore
            'Insurance': lambda obj: obj.tenant.lease.unit.building.property.manager_id, # type: ignore
        }

        owner_id = owner_map.get(model_name)
        if owner_id is None:
            logger.error(f'Ownership validation not supported for {model_name}')
            raise access_exception

        if owner_id(db_obj) != context.get_user_id():
            logger.warning(f'User {context.get_user_id()} does not have permission to access {model_name} with ID {resource_id}')
            raise access_exception

    except AttributeError as exc:
        log_exception(exc, 'Attribute error during ownership validation')
        raise access_exception
    except Exception as exc:
        log_exception(exc, 'Error during ownership validation')
        raise access_exception
