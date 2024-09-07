from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core import security, oauth2
from controllers import UserController
from schemas import TokenSchema
from app.api.v1.deps import get_db

router: APIRouter = APIRouter()

@router.post("/login", response_model=TokenSchema.Base)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = UserController.get_by_email(email=form_data.username, db=db)
    if not user or not security.verify_password(plain_password=form_data.password, hashed_password=user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = oauth2.create_access_token(data={"sub": user.email})
    refresh_token = oauth2.create_refresh_token(data={"sub": user.email})
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/refresh", response_model=TokenSchema.Base)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = oauth2.verify_token(db=db, token=refresh_token, credentials_exception=credentials_exception)
    new_access_token = oauth2.create_access_token(data={"sub": token_data.email})
    return {"access_token": new_access_token, "refresh_token": refresh_token}
