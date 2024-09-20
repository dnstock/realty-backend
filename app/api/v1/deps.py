from fastapi import HTTPException, status, Request, Response
from core.oauth2 import get_current_user
from controllers import UserController
from schemas import UserSchema

# Dependency to get the current active user
def get_current_active_user(request: Request, response: Response) -> UserSchema.Read:
    current_user = get_current_user(request, response)
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Inactive user"')
    return current_user

# Dependency to validate ownership
def validate_ownership(
    model_name: str,
    resource_id: int,
    current_user: UserSchema.Read
) -> None:
    # print debugging
    print(f"Validating ownership for {model_name} with ID {resource_id} by user {current_user}")
    if not UserController.validate_ownership(model_name=model_name, resource_id=resource_id, current_user=current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized to access this {model_name}')
