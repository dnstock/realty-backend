# User -> Property -> Building -> Unit -> Lease -> Tenant -> Insurance
from . import (
    user as UserSchema,
    property as PropertySchema,
    building as BuildingSchema,
    unit as UnitSchema,
    lease as LeaseSchema,
    tenant as TenantSchema,
    insurance as InsuranceSchema,
    token as TokenSchema,
)

__all__ = [
    "TokenSchema",
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
