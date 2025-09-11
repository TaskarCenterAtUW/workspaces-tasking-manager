from schematics import Model
from schematics.types import (
    StringType,
    BaseType,
    IntType,
    DictType,
    UTCDateTimeType,
    UUIDType,
)

class WorkspaceLongQuestDTO(Model):
    workspace_id = IntType()
    definition  = DictType(StringType, BaseType)
    modifiedAt = UTCDateTimeType()
    modifiedBy = UUIDType()
    modifiedByName = StringType()
