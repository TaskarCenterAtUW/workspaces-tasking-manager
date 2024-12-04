from sqlalchemy.dialects.postgresql import UUID

from backend import db
from backend.models.dtos.workspace_long_quest_dto import WorkspaceLongQuestDTO
from backend.models.postgis.utils import timestamp
from backend.models.postgis.workspace import Workspace


class WorkspaceLongQuest(db.Model):
    """Stores mobile app quest definitions for a workspace"""

    __tablename__ = "workspaces_long_quests"

    workspace_id = db.Column(db.Integer, db.ForeignKey(Workspace.id), primary_key=True)
    definition = db.Column(db.Unicode, nullable=False)
    modifiedAt = db.Column(db.DateTime, nullable=False, default=timestamp, onupdate=timestamp)
    modifiedBy = db.Column(UUID(as_uuid=True), nullable=False)
    modifiedByName = db.Column(db.Unicode, nullable=False)

    def create(self):
        """Creates and saves the current model to the DB"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates the DB with the current state of the model"""
        db.session.commit()

    def delete(self):
        """Deletes the current model from the DB"""
        db.session.delete(self)
        db.session.commit()

    def as_dto(self):
        dto = WorkspaceLongQuestDTO()
        dto.workspace_id = self.workspace_id
        dto.definition = self.definition
        dto.modifiedAt = self.createdAt
        dto.modifiedBy = self.createdBy
        dto.modifiedByName = self.createdByName

        return dto
