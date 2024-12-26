from typing import Type
from pydantic import create_model
from schemas.base import BaseModel

# Dynamically create a partial model where all fields are optional
def make_partial_model(model: Type[BaseModel]) -> Type[BaseModel]:
    fields = {field_name: (field.annotation, None) for field_name, field in model.model_fields.items()}
    return create_model(
        f"Partial{model.__name__}",
        __base__=model,
        **fields # type: ignore
    )
