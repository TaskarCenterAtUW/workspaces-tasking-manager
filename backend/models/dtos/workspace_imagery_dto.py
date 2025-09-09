from schematics import Model
from schematics.types import (
    StringType,
    IntType,
    ListType,
    UTCDateTimeType,
    UUIDType,
)

class WorkspaceImageryDTO(Model):
    workspace_id = IntType()
    definition = ListType(StringType())
    modifiedAt = UTCDateTimeType()
    modifiedBy = UUIDType()
    modifiedByName = StringType()
