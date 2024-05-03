from schematics import Model
from schematics.types import (
    StringType,
    IntType,
    UTCDateTimeType,
    UUIDType,
)


class WorkspaceDTO(Model):
    id = IntType()
    title = StringType(required=True)
    description = StringType()
    tdeiRecordId = UUIDType()
    tdeiProjectGroupId = UUIDType()
    tdeiServiceId = UUIDType()
    tdeiMetadata = StringType()
    createdAt = UTCDateTimeType()
    createdBy = UUIDType()
    createdByName = StringType()
