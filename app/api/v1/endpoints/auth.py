from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from core import security, oauth2, settings
from controllers import UserController
from schemas import UserSchema

router: APIRouter = APIRouter()

@router.post('/login', response_model=UserSchema.Me)
def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = UserController.get_by_email(email=form_data.username)
    if not user or not security.verify_password(plain_password=form_data.password, hashed_password=user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    
    # Generate tokens
    access_token = oauth2.create_access_token(data={'sub': user.email})
    refresh_token = oauth2.create_refresh_token(data={'sub': user.email})
    
    # Set tokens as HttpOnly cookies
    response.set_cookie(
        key='access_token', 
        value=access_token, 
        httponly=True, 
        secure=settings.app_env == 'DEVELOPMENT', # Set to False if not using HTTPS (for local development), but keep True in production
        samesite='lax'
    )
    response.set_cookie(
        key='refresh_token', 
        value=refresh_token, 
        httponly=True, 
        secure=settings.app_env == 'DEVELOPMENT', 
        samesite='lax'
    )
    
    return user

@router.post('/refresh', response_model=UserSchema.Me)
def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token missing',
        )

    user = oauth2.verify_token(token=refresh_token, credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    ))
    
    new_access_token = oauth2.create_access_token(data={'sub': user.email})
    
    # Set the new access token as a cookie
    response.set_cookie(
        key='access_token', 
        value=new_access_token, 
        httponly=True, 
        secure=settings.app_env == 'DEVELOPMENT', 
        samesite='lax'
    )
    
    return user

@router.get('/me', response_model=UserSchema.Me)
def get_current_user(request: Request):
    access_token = request.cookies.get('access_token')
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Access token missing',
        )

    user = oauth2.verify_token(token=access_token, credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    ))
    
    return user

@router.post('/logout')
def logout(response: Response) -> Any:
    response.delete_cookie(key="access_token", httponly=True)
    response.delete_cookie(key="refresh_token", httponly=True)
    
    return {"message": "Logout successful"}
