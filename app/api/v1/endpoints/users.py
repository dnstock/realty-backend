from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from controllers import UserController
from schemas import UserSchema
from app.api.v1.deps import get_db

router: APIRouter = APIRouter()

@router.post("/", response_model=UserSchema.Read, status_code=status.HTTP_201_CREATED)
def create_new_user(user_in: UserSchema.Create, db: Session = Depends(get_db)):
    user = UserController.get_by_email(email=user_in.email, db=db)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    return UserController.create_and_commit(db=db, schema=user_in)

@router.get("/", response_model=list[UserSchema.Read])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return UserController.get_all(db=db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserSchema.Read)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = UserController.get_by_id(db=db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

@router.put("/{user_id}", response_model=UserSchema.Read)
def update_user(user_id: int, user: UserSchema.Update, db: Session = Depends(get_db)):
    updated_user = UserController.update_and_commit(db=db, schema=user, id=user_id)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return updated_user
