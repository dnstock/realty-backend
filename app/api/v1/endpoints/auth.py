from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from core import security, oauth2
from controllers import UserController
from schemas import TokenSchema, UserSchema

router: APIRouter = APIRouter()

@router.post('/login', response_model=TokenSchema.Base)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, Any]:
    user = UserController.get_by_email(email=form_data.username)
    if not user or not security.verify_password(plain_password=form_data.password, hashed_password=user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = oauth2.create_access_token(data={'sub': user.email})
    refresh_token = oauth2.create_refresh_token(data={'sub': user.email})
    return {
        'access_token': access_token, 
        'refresh_token': refresh_token, 
        'user': dict(UserSchema.Login.model_validate(user))
    }

@router.post('/refresh', response_model=TokenSchema.Base)
def refresh_token(refresh_token: str) -> dict[str, Any]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    user_from_token = oauth2.verify_token(token=refresh_token, credentials_exception=credentials_exception)
    new_access_token = oauth2.create_access_token(data={'sub': user_from_token.email})
    return {
        'access_token': new_access_token, 
        'refresh_token': refresh_token, 
        'user': dict(UserSchema.Login.model_validate(user_from_token))
    }
