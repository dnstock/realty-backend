# User -> Property -> Building -> Unit -> Lease -> Tenant -> Insurance
from . import (
    base as BaseSchema,
    request as RequestSchema,
    user as UserSchema,
    property as PropertySchema,
    building as BuildingSchema,
    unit as UnitSchema,
    lease as LeaseSchema,
    tenant as TenantSchema,
    insurance as InsuranceSchema,
)

__all__ = [
    'BaseSchema',
    'RequestSchema',
    'UserSchema',
    'BuildingSchema',
    'UnitSchema',
    'LeaseSchema',
    'TenantSchema',
    'InsuranceSchema',
    'PropertySchema',
]

# Resolve forward references (while avoiding circular imports)
UserSchema.ReadFull.model_rebuild()
PropertySchema.ReadFull.model_rebuild()
BuildingSchema.ReadFull.model_rebuild()
UnitSchema.ReadFull.model_rebuild()
LeaseSchema.ReadFull.model_rebuild()
TenantSchema.ReadFull.model_rebuild()
InsuranceSchema.ReadFull.model_rebuild()
RequestSchema.RequestContext.model_rebuild()
