from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from core import security, oauth2, settings
from controllers import UserController
from schemas import TokenSchema, UserSchema

router: APIRouter = APIRouter()

@router.post('/login', response_model=TokenSchema.Base)
def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, Any]:
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
    
    # Return the user details (tokens are now stored in cookies)
    return {
        'user': dict(UserSchema.Login.model_validate(user))
    }

@router.post('/refresh', response_model=TokenSchema.Base)
def refresh_token(request: Request, response: Response) -> dict[str, Any]:
    # Get refresh token from cookies
    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token missing',
        )

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    
    # Verify the refresh token
    user_from_token = oauth2.verify_token(token=refresh_token, credentials_exception=credentials_exception)
    
    # Create a new access token
    new_access_token = oauth2.create_access_token(data={'sub': user_from_token.email})
    
    # Set the new access token as a cookie
    response.set_cookie(
        key='access_token', 
        value=new_access_token, 
        httponly=True, 
        secure=True, 
        samesite='lax'
    )
    
    # Return user information (tokens are stored in cookies)
    return {
        'user': dict(UserSchema.Login.model_validate(user_from_token))
    }

@router.post('/logout')
def logout(response: Response) -> Any:
    # Clear the cookies by setting them to expire
    response.delete_cookie(key="access_token", httponly=True)
    response.delete_cookie(key="refresh_token", httponly=True)
    
    return {"message": "Logout successful"}
