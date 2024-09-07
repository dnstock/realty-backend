from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Generator
from db import get_db as db_session
from core.oauth2 import get_current_user, oauth2_scheme
from controllers import UserController
from schemas import UserSchema

# Dependency to get the database session
def get_db() -> Generator[Session, None, None]:
    return db_session()

# Dependency to get the current active user
def get_current_active_user(
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
) -> UserSchema.Read:
    current_user = get_current_user(db, token)
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

# Dependency to validate ownership
def validate_ownership(
    model_name: str,
    resource_id: int,
    # db: Session,
    current_user: UserSchema.Read = Depends(get_current_active_user),
) -> None:
    if not UserController.validate_ownership(model_name=model_name, resource_id=resource_id, current_user=current_user):#, db=db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this ${model_name}")
