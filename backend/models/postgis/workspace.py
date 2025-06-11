from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import UUID

from databases import Database
from sqlalchemy import (
    Unicode,
    SmallInteger,
    BigInteger,
    Column,
    DateTime,
    Integer,
    UnicodeText
)

from backend.db import Base
from backend.models.dtos.workspace_dto import WorkspaceDTO
from backend.models.postgis.utils import timestamp

class Workspace(Base):
    """Describes a TDEI Workspace"""

    __tablename__ = "workspaces"

    id = Column(BigInteger, primary_key=True)
    type = Column(UnicodeText, nullable=False)
    title = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText)

    tdeiProjectGroupId = Column(UUID(as_uuid=True), nullable=False)
    tdeiRecordId = Column(UUID(as_uuid=True))
    tdeiServiceId = Column(UUID(as_uuid=True))
    tdeiMetadata = Column(UnicodeText)

    createdAt = Column(DateTime, nullable=False, default=timestamp)
    createdBy = Column(UUID(as_uuid=True), nullable=False)
    createdByName = Column(UnicodeText)

    geometry = Column(Geometry("MULTIPOLYGON", srid=4326))

    # GoInfoGame visibility: 0 = none, 1 = public, 2 = project group
    externalAppAccess = Column(SmallInteger, nullable=False, default=0)

    kartaViewToken = Column(Unicode)

    def create(self, db: Database):
        """Creates and saves the current model to the DB"""
        db.session.add(self)
        db.session.commit()

    def update(self, db: Database):
        """Updates the DB with the current state of the Task"""
        db.session.commit()

    def delete(self, db: Database):
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
