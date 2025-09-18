from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import UUID

from backend import db
from backend.models.dtos.workspace_dto import WorkspaceDTO
from backend.models.postgis.utils import timestamp


class Workspace(db.Model):
    """Describes a TDEI Workspace"""

    __tablename__ = "workspaces"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Unicode, nullable=False)
    title = db.Column(db.Unicode, nullable=False)
    description = db.Column(db.Unicode)
    tdeiProjectGroupId = db.Column(UUID(as_uuid=True), nullable=False)
    tdeiRecordId = db.Column(UUID(as_uuid=True))
    tdeiServiceId = db.Column(UUID(as_uuid=True))
    tdeiMetadata = db.Column(db.Unicode)
    createdAt = db.Column(db.DateTime, nullable=False, default=timestamp)
    createdBy = db.Column(UUID(as_uuid=True), nullable=False)
    createdByName = db.Column(db.Unicode)
    geometry = db.Column(Geometry("MULTIPOLYGON", srid=4326))
    # GoInfoGame visibility: 0 = none, 1 = public, 2 = project group
    externalAppAccess = db.Column(db.SmallInteger, nullable=False, default=0)
    kartaViewToken = db.Column(db.Unicode)

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
        dto.type = self.type
        dto.title = self.title
        dto.description = self.description
        dto.tdeiRecordId = self.tdeiRecordId
        dto.tdeiProjectGroupId = self.tdeiProjectGroupId
        dto.tdeiServiceId = self.tdeiServiceId
        dto.tdeiMetadata = self.tdeiMetadata
        dto.createdAt = self.createdAt
        dto.createdBy = self.createdBy
        dto.createdByName = self.createdByName
        dto.externalAppAccess = self.externalAppAccess
        dto.kartaViewToken = self.kartaViewToken

        return dto
