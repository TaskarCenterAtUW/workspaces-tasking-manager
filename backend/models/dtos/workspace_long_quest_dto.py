from schematics import Model
from schematics.types import (
    StringType,
    IntType,
    UTCDateTimeType,
    UUIDType,
)

class WorkspaceLongQuestDTO(Model):
    workspace_id = IntType()
    definition = StringType(required=True)
    modifiedAt = UTCDateTimeType()
    modifiedBy = UUIDType()
    modifiedByName = StringType()
