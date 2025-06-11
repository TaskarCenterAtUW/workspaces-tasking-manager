from sqlalchemy.dialects.postgresql import UUID

from databases import Database
from sqlalchemy import (
    Unicode,
    BigInteger,
    Column,
    ForeignKey,
    DateTime
)

from backend.models.dtos.workspace_long_quest_dto import WorkspaceLongQuestDTO
from backend.models.postgis.workspace import Workspace

from backend.db import Base
from backend.models.dtos.workspace_dto import WorkspaceDTO
from backend.models.postgis.utils import timestamp

class WorkspaceLongQuest(Base):
    """Stores mobile app quest definitions for a workspace"""

    __tablename__ = "workspaces_long_quests"

    workspace_id = Column(BigInteger, ForeignKey(Workspace.id), primary_key=True)
    definition = Column(Unicode, nullable=False)
    modifiedAt = Column(DateTime, nullable=False, default=timestamp, onupdate=timestamp)
    modifiedBy = Column(UUID(as_uuid=True), nullable=False)
    modifiedByName = Column(Unicode, nullable=False)

    def create(self, db: Database):
        """Creates and saves the current model to the DB"""
        db.session.add(self)
        db.session.commit()

    def update(self, db: Database):
        """Updates the DB with the current state of the model"""
        db.session.commit()

    def delete(self, db: Database):
        """Deletes the current model from the DB"""
        db.session.delete(self)
        db.session.commit()

    def as_dto(self, db: Database):
        dto = WorkspaceLongQuestDTO()
        dto.workspace_id = self.workspace_id
        dto.definition = self.definition
        dto.modifiedAt = self.createdAt
        dto.modifiedBy = self.createdBy
        dto.modifiedByName = self.createdByName

        return dto
