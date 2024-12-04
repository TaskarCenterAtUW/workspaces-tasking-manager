import uuid

from backend import db
from backend.models.postgis.utils import NotFound
from backend.models.postgis.workspace import Workspace
from backend.models.postgis.workspace_long_quest import WorkspaceLongQuest


class WorkspacesService:
    @staticmethod
    def list_workspaces(externalAppOnly: bool = False):
        query = Workspace.query

        if externalAppOnly:
            query = query.filter(Workspace.externalAppAccess > 0)

        return query.all()

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

    @staticmethod
    def get_workspace_long_form_quest(workspace_id: int) -> WorkspaceLongQuest:
        quest = db.session.get(WorkspaceLongQuest, workspace_id)

        if quest is None:
            raise NotFound()

        return quest

    def save_long_form_quest(workspace_id: int, definition: str):
        quest = db.session.get(WorkspaceLongQuest, workspace_id)

        if quest is None:
            quest = WorkspaceLongQuest()
            quest.workspace_id = workspace_id
            db.session.add(quest)

        quest.definition = definition
        quest.modifiedBy = uuid.UUID(int=0)
        quest.modifiedByName = ""
        db.session.commit()
