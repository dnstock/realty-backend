from datetime import datetime, timedelta, timezone
from typing import Any
from typing_extensions import Literal
from fastapi import HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError
from core import settings
from schemas import UserSchema
from controllers import UserController
from core.logger import log_exception

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Generate JWT token
def create_token(data: dict[str, Any], token_type: Literal['access', 'refresh']) -> str:
    expire = datetime.now(timezone.utc)
    if token_type == 'access':
        expire += timedelta(minutes=settings.jwt_access_token_expire_minutes)
    elif token_type == 'refresh':  
        expire += timedelta(days=settings.jwt_refresh_token_expire_days)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

# Set tokens as HttpOnly cookies
def set_token_cookie(response: Response, token_type: Literal['access', 'refresh'], token: str) -> None:
    response.set_cookie(
        key=f'{token_type}_token', 
        value=token, 
        httponly=True, 
        secure=settings.app_env == 'DEVELOPMENT',  # Set to False if not using HTTPS, but keep True in production
        samesite='lax'
    )
    
def delete_token_cookies(response: Response) -> None:
    response.delete_cookie(key="access_token", httponly=True)
    response.delete_cookie(key="refresh_token", httponly=True)

def create_and_set_token_cookie(response: Response, token_type: Literal['access', 'refresh'], data: dict[str, Any]) -> str:
    token = create_token(data=data, token_type=token_type)
    set_token_cookie(response=response, token_type=token_type, token=token)
    return token
    
def verify_token(token: str, credentials_exception: HTTPException) -> UserSchema.Read:
    try:
        # Decode token and validate "exp" claim
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        email = payload.get("sub")
        if not email:
            raise credentials_exception
    except ExpiredSignatureError:
        # Re-raise to allow get_current_user to handle token expiration
        raise
    except JWTError as exc:
        # Log and raise for any other JWT-related errors
        log_exception(exc, "Error decoding token")
        raise credentials_exception from exc

    user = UserController.get_by_email(email=email)
    if not user:
        raise credentials_exception

    return UserSchema.Read.model_validate(user)

def get_current_user(request: Request, response: Response) -> UserSchema.Read:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = request.cookies.get('access_token')
    if not token:
        raise credentials_exception

    try:
        return verify_token(token, credentials_exception)

    except ExpiredSignatureError:
        # Handle expired access token by using refresh token
        refresh_token = request.cookies.get('refresh_token')
        if not refresh_token:
            raise credentials_exception

        try:
            # Verify refresh token
            refresh_payload = jwt.decode(
                refresh_token, 
                settings.jwt_secret_key, 
                algorithms=[settings.jwt_algorithm]
            )
            email = refresh_payload.get("sub")
            if not email:
                raise credentials_exception

            user = UserController.get_by_email(email=email)
            if not user:
                raise credentials_exception
            
            # Set the new access token in response cookies
            create_and_set_token_cookie(response=response, token_type='access', data={'sub': email})

            return UserSchema.Read.model_validate(user)

        except JWTError as exc:
            log_exception(exc, "Error decoding refresh token")
            raise credentials_exception

    except JWTError:
        raise credentials_exception
