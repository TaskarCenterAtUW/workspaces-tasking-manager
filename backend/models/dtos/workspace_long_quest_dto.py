from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union

from fastapi import HTTPException
from pydantic import BaseModel, Field, root_validator, field_validator

class WorkspaceLongQuestDTO(BaseModel):

    workspace_id: int = Field(alias="workspace_id")
    definition: str = Field(alias="definition")

    modifiedAt: Optional[datetime] = None

    modifiedBy: str = Field(alias="modifiedBy")
    modifiedByName: str = Field(alias="modifiedByName")
