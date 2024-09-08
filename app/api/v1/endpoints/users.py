from fastapi import APIRouter, HTTPException, status
from controllers import UserController
from schemas import UserSchema

router: APIRouter = APIRouter()

@router.post("/", response_model=UserSchema.Read, status_code=status.HTTP_201_CREATED)
def create_new_user(user_in: UserSchema.Create):
    user = UserController.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    return UserController.create_and_commit(schema=user_in)

@router.get("/", response_model=list[UserSchema.Read])
def read_users(skip: int = 0, limit: int = 10):
    return UserController.get_all(skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserSchema.Read)
def read_user(user_id: int):
    user = UserController.get_by_id(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

@router.put("/{user_id}", response_model=UserSchema.Read)
def update_user(user_id: int, user: UserSchema.Update):
    updated_user = UserController.update_and_commit(schema=user, id=user_id)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return updated_user
