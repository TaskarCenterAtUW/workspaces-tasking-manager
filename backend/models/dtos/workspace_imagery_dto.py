from schematics import Model
from schematics.types import (
    BaseType,
    StringType,
    IntType,
    ListType,
    DictType,
    UTCDateTimeType,
    UUIDType,
)

class WorkspaceImageryDTO(Model):
    workspace_id = IntType()
    definition = ListType(DictType(StringType, BaseType))
    modifiedAt = UTCDateTimeType()
    modifiedBy = UUIDType()
    modifiedByName = StringType()
