from fastapi import APIRouter, Depends
from app.api.v1.deps import (
    get_request_context,
    validate_ownership,
    serialize_results,
    PaginatedResults,
    RequestContext,
)
from controllers import UnitController, LeaseController
from schemas import UnitSchema, LeaseSchema

router: APIRouter = APIRouter()

@router.get('/{unit_id}', response_model=UnitSchema.Read)
def read_unit(
    unit_id: int,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context, model_name='Unit', resource_id=unit_id)
    return UnitController.get_by_id(db=context.db, id=unit_id)

@router.put('/{unit_id}', response_model=UnitSchema.Read)
def update_unit(
    unit_id: int, unit: UnitSchema.Update,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context, model_name='Unit', resource_id=unit_id)
    return UnitController.update_and_commit(db=context.db, schema=unit, id=unit_id)

@router.post('/{unit_id}/leases/', response_model=LeaseSchema.Read)
def create_lease(
    unit_id: int, lease: LeaseSchema.Create,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context, model_name='Unit', resource_id=unit_id)
    return LeaseController.create_and_commit(db=context.db, schema=lease, parent_id=unit_id)

@router.get('/{unit_id}/leases/', response_model=PaginatedResults)
def read_leases(
    unit_id: int, skip: int = 0, limit: int = 10,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context, model_name='Unit', resource_id=unit_id)
    results = LeaseController.get_all_paginated(db=context.db, parent_id=unit_id, skip=skip, limit=limit)
    return serialize_results(results, LeaseSchema.Read)
