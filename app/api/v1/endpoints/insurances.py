from fastapi import APIRouter, Depends
from app.api.v1.deps import (
    get_request_context,
    validate_ownership,
    RequestContext,
)
from controllers import InsuranceController
from schemas import InsuranceSchema

router: APIRouter = APIRouter()

@router.get('/{insurance_id}', response_model=InsuranceSchema.Read)
def read_insurance(
    insurance_id: int,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context, model_name='Insurance', resource_id=insurance_id)
    return InsuranceController.get_by_id(db=context.db, id=insurance_id)

@router.put('/{insurance_id}', response_model=InsuranceSchema.Read)
def update_insurance(
    insurance_id: int, insurance: InsuranceSchema.Update,
    context: RequestContext = Depends(get_request_context),
):
    validate_ownership(context=context, model_name='Insurance', resource_id=insurance_id)
    return InsuranceController.update_and_commit(db=context.db, schema=insurance, id=insurance_id)
