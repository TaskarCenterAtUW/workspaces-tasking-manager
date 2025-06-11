from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union

from fastapi import HTTPException
from pydantic import BaseModel, Field, root_validator, field_validator

class WorkspaceDTO(BaseModel):
    id: int = Field(alias="id")

    type: str = Field(alias="type")
    title: str = Field(alias="title")

    description: str = Field(alias="description")

    tdeiRecordId: str = Field(alias="tdeiRecordId")
    tdeiProjectGroupId: str = Field(alias="tdeiProjectGroupId")
    tdeiServiceId: str = Field(alias="tdeiServiceId")
    tdeiMetadata: str = Field(alias="tdeiMetadata")

    createdAt: Optional[datetime] = None

    createdBy: str = Field(alias="createdBy")
    createdByName: Optional[str] = Field(None, alias="createdByName")

    externalAppAccess: Optional[int] = Field(None, alias="externalAppAccess")
    kartaViewToken: Optional[str] = Field(None, alias="kartaViewToken")
