# User -> Property -> Building -> Unit -> Lease -> Tenant -> Insurance
from . import (
    base as BaseSchema,
    user as UserSchema,
    property as PropertySchema,
    building as BuildingSchema,
    unit as UnitSchema,
    lease as LeaseSchema,
    tenant as TenantSchema,
    insurance as InsuranceSchema,
)

__all__ = [
    "BaseSchema",
    "UserSchema",
    "BuildingSchema",
    "UnitSchema",
    "LeaseSchema",
    "TenantSchema",
    "InsuranceSchema",
    "PropertySchema",
]

# Resolve forward references (while avoiding circular imports)
UserSchema.Read.model_rebuild()
PropertySchema.Read.model_rebuild()
BuildingSchema.Read.model_rebuild()
UnitSchema.Read.model_rebuild()
LeaseSchema.Read.model_rebuild()
TenantSchema.Read.model_rebuild()
InsuranceSchema.Read.model_rebuild()
