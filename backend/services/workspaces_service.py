from backend import db
from backend.models.postgis.utils import NotFound
from backend.models.postgis.workspace import Workspace


class WorkspacesService:
    @staticmethod
    def list_workspaces():
        return Workspace.query.all()

    @staticmethod
    def get_workspace(id: int) -> Workspace:
        workspace = db.session.get(Workspace, id)

        if workspace is None:
            raise NotFound()

        return workspace

    @staticmethod
    def delete_workspace(id: int):
        workspace = db.session.get(Workspace, id)

        if workspace is None:
            raise NotFound()

        db.session.delete(workspace)
        db.session.commit()
