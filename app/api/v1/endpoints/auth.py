from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from core.security import verify_password
from core.oauth2 import create_and_set_token_cookie, get_current_user
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
    response.delete_cookie(key="access_token", httponly=True)
    response.delete_cookie(key="refresh_token", httponly=True)
    return {"message": "Logout successful"}

# Return current user info and refresh access token if expired
@router.get('/me', response_model=UserSchema.Me)
def get_user_info(request: Request, response: Response):
    user = get_current_user(request=request, response=response)
    return user
