from sqlalchemy.dialects.postgresql import UUID

from backend import db
from backend.models.dtos.workspace_imagery_dto import WorkspaceImageryDTO
from backend.models.postgis.utils import timestamp
from backend.models.postgis.workspace import Workspace


class WorkspaceImagery(db.Model):
    """Stores imagery list for a workspace"""

    __tablename__ = "workspaces_imagery"

    workspace_id = db.Column(db.Integer, db.ForeignKey(Workspace.id), primary_key=True)
    definition = db.Column(db.JSON, nullable=False, default=list)
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
        dto = WorkspaceImageryDTO()
        dto.workspace_id = self.workspace_id
        dto.definition = self.definition
        dto.modifiedAt = self.modifiedAt
        dto.modifiedBy = self.modifiedBy
        dto.modifiedByName = self.modifiedByName

        return dto