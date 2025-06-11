import uuid

from databases import Database

from backend.models.postgis.utils import NotFound
from backend.models.postgis.workspace import Workspace
from backend.models.postgis.workspace_long_quest import WorkspaceLongQuest


class WorkspacesService:
    @staticmethod
    def list_workspaces(externalAppOnly: bool, db: Database):
        query = Workspace.query

        if externalAppOnly:
            query = query.filter(Workspace.externalAppAccess > 0)

        return query.all()

    @staticmethod
    def get_workspace(workspace_id: int, db: Database) -> Workspace:
        workspace = db.session.get(Workspace, workspace_id)

        if workspace is None:
            raise NotFound("Workspace not found")

        return workspace

    @staticmethod
    def delete_workspace(workspace_id: int, db: Database):
        workspace = db.session.get(Workspace, workspace_id)

        if workspace is None:
            raise NotFound("Workspace not found")

        db.session.delete(workspace)
        db.session.commit()

    @staticmethod
    def get_workspace_long_form_quest(workspace_id: int, db: Database) -> WorkspaceLongQuest:
        quest = db.session.get(WorkspaceLongQuest, workspace_id)

        if quest is None:
            raise NotFound("Workspace not found")

        return quest

    def save_long_form_quest(workspace_id: int, definition: str, db: Database):
        quest = db.session.get(WorkspaceLongQuest, workspace_id)

        if quest is None:
            quest = WorkspaceLongQuest()
            quest.workspace_id = workspace_id
            db.session.add(quest)

        quest.definition = definition
        quest.modifiedBy = uuid.UUID(int=0)
        quest.modifiedByName = ""
        db.session.commit()
