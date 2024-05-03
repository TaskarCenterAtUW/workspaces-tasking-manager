import uuid
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import UUID

from backend import db
from backend.models.dtos.workspace_dto import WorkspaceDTO
from backend.models.postgis.utils import timestamp


class Workspace(db.Model):
    """Describes a TDEI Workspace"""

    __tablename__ = "workspaces"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode)
    description = db.Column(db.Unicode)
    tdeiRecordId = db.Column(UUID(as_uuid=True), default=uuid.uuid4)
    tdeiProjectGroupId = db.Column(UUID(as_uuid=True), default=uuid.uuid4)
    tdeiServiceId = db.Column(UUID(as_uuid=True), default=uuid.uuid4)
    tdeiMetadata = db.Column(db.Unicode)
    createdAt = db.Column(db.DateTime, default=timestamp)
    createdBy = db.Column(UUID(as_uuid=True), default=uuid.uuid4)
    createdByName = db.Column(db.Unicode)
    geometry = db.Column(Geometry("MULTIPOLYGON", srid=4326))

    def create(self):
        """Creates and saves the current model to the DB"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates the DB with the current state of the Task"""
        db.session.commit()

    def delete(self):
        """Deletes the current model from the DB"""
        db.session.delete(self)
        db.session.commit()

    def as_dto(self):
        dto = WorkspaceDTO()
        dto.id = self.id
        dto.title = self.title
        dto.description = self.description
        dto.tdeiRecordId = self.tdeiRecordId
        dto.tdeiProjectGroupId = self.tdeiProjectGroupId
        dto.tdeiServiceId = self.tdeiServiceId
        dto.tdeiMetadata = self.tdeiMetadata
        dto.createdAt = self.createdAt
        dto.createdBy = self.createdBy
        dto.createdByName = self.createdByName

        return dto
