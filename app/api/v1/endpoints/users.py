from fastapi import APIRouter, Depends, HTTPException, status
from app.api.v1.deps import (
    get_request_context,
    serialize_results,
    PaginatedResults,
    RequestContext,
)
from controllers import UserController
from schemas import UserSchema

router: APIRouter = APIRouter()

@router.post('/', response_model=UserSchema.Read, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserSchema.Create,
    context: RequestContext = Depends(get_request_context),
):
    if UserController.exists_where(db=context.db, key='email', val=user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User already exists',
        )
    return UserController.create_and_commit(db=context.db, schema=user)

@router.get('/', response_model=PaginatedResults)
def read_users(
    skip: int = 0, limit: int = 10,
    context: RequestContext = Depends(get_request_context),
):
    results = UserController.get_all_paginated(db=context.db, skip=skip, limit=limit)
    return serialize_results(results, UserSchema.Read)

@router.get('/{user_id}', response_model=UserSchema.Read)
def read_user(
    user_id: int,
    context: RequestContext = Depends(get_request_context),
):
    return UserController.get_by_id(db=context.db, id=user_id)

@router.put('/{user_id}', response_model=UserSchema.Read)
def update_user(
    user_id: int, user: UserSchema.Update,
    context: RequestContext = Depends(get_request_context),
):
    return UserController.update_and_commit(db=context.db, schema=user, id=user_id)
