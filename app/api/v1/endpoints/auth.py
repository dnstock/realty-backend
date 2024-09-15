from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from core.oauth2 import create_and_set_token_cookie, get_current_user, delete_token_cookies
from core.security import verify_password
from core.logger import log_exception
from controllers import UserController
from schemas import UserSchema

router: APIRouter = APIRouter()

@router.post('/login', response_model=UserSchema.Me)
def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = UserController.get_by_email(email=form_data.username)
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
    return {"message": "Logout successful"}

# Return current user info and refresh access token if expired
@router.get('/me', response_model=UserSchema.Me | None)
def get_user_info(request: Request, response: Response):
    if not request.cookies.get('access_token'):
        return None
    try:
        return get_current_user(request=request, response=response)
    except HTTPException as exc:
        log_exception(exc, "Error getting current user")
        delete_token_cookies(response)
        return None
