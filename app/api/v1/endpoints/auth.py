from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.oauth2 import create_and_set_token_cookie, delete_token_cookies
from core.security import verify_password
from core.logger import log_exception
from controllers import UserController
from schemas import UserSchema
from db import get_db
from api.v1.deps import get_request_context_optional
from schemas.base import RequestContext

router: APIRouter = APIRouter()

@router.post('/login', response_model=UserSchema.Read)
def login_for_access_token(
    response: Response,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = UserController.get_by_email(db=db, email=form_data.username)
    if not user or not verify_password(plain_password=form_data.password, hashed_password=user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password.',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    create_and_set_token_cookie(response=response, token_type='access', data={'sub': user.email})
    create_and_set_token_cookie(response=response, token_type='refresh', data={'sub': user.email})
    return user

@router.post('/logout', response_model=dict)
def logout(response: Response):
    delete_token_cookies(response)
    return {'message': 'Logout successful'}

# Return current user info and refresh access token if expired
@router.get('/me', response_model=UserSchema.Read | None)
def get_user_info(
    response: Response,
    context: RequestContext = Depends(get_request_context_optional)
):
    if context.current_user is None:
        return None
    try:
        if not context.is_user_active():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Inactive user'
            )
        return UserSchema.Read.model_validate(context.current_user)
    except Exception as exc:
        log_exception(exc, 'GET /auth/me endpoint')
        return None
