from fastapi import Depends, HTTPException, status
from core.oauth2 import get_current_user, oauth2_scheme
from controllers import UserController
from schemas import UserSchema

# Dependency to get the current active user
def get_current_active_user(
    token: str = Depends(oauth2_scheme)
) -> UserSchema.Read:
    current_user = get_current_user(token)
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

# Dependency to validate ownership
def validate_ownership(
    model_name: str,
    resource_id: int,
    current_user: UserSchema.Read = Depends(get_current_active_user),
) -> None:
    if not UserController.validate_ownership(model_name=model_name, resource_id=resource_id, current_user=current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this ${model_name}")
