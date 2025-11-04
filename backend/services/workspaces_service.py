import requests
import uuid
from flask_restful import current_app

from backend import db
from backend.models.dtos.workspace_long_quest_dto import (
    QuestDefinitionType,
    WorkspaceLongQuestDTO
)
from backend.models.postgis import workspace
from backend.models.postgis.utils import NotFound
from backend.models.postgis.workspace import Workspace
from backend.models.postgis.workspace_long_quest import WorkspaceLongQuest
from backend.models.postgis.workspace_imagery import WorkspaceImagery


class WorkspacesService:
    @staticmethod
    def list_workspaces(externalAppOnly: bool, projectGroupIds: list, query_obj=None):
        query = query_obj or Workspace.query
        query = query.filter(Workspace.tdeiProjectGroupId.in_(projectGroupIds))

        if externalAppOnly:
            query = query.filter(Workspace.externalAppAccess > 0)

        return query.all()

    @staticmethod
    def get_workspace(id: int, projectGroupIds: list) -> Workspace:
        workspace = db.session.get(Workspace, id)

        if workspace is None:
            raise NotFound()

        if str(workspace.tdeiProjectGroupId) not in projectGroupIds:
            raise NotFound()

        return workspace

    @staticmethod
    def delete_workspace(id: int, projectGroupIds: list):
        workspace = db.session.get(Workspace, id)

        if workspace is None:
            raise NotFound()

        if str(workspace.tdeiProjectGroupId) not in projectGroupIds:
            raise NotFound()

        db.session.delete(workspace)
        db.session.commit()

    @staticmethod
    def get_long_form_quest(workspace_id: int, projectGroupIds: list) -> WorkspaceLongQuest:
        workspace = db.session.get(Workspace, workspace_id)

        if workspace is None:
            raise NotFound()

        if str(workspace.tdeiProjectGroupId) not in projectGroupIds:
            raise NotFound()

        return db.session.get(WorkspaceLongQuest, workspace_id)

    @staticmethod
    def get_long_form_quest_def(workspace_id: int, project_group_ids: list) -> str:
        quest = WorkspacesService.get_long_form_quest(workspace_id, project_group_ids)

        if quest is None:
            return None

        type = QuestDefinitionType(quest.type)

        if type == QuestDefinitionType.NONE:
            return None
        if type == QuestDefinitionType.JSON:
            return quest.definition

        try:
            response = requests.get(quest.url)
            return response.content
        except Exception as e:
            current_app.logger.info(f"Fetch quest def failed for {quest.url}: {str(e)}")

        return None

    @staticmethod
    def save_long_form_quest(settings: WorkspaceLongQuestDTO, user):
        settings.validate();
        workspace = db.session.get(Workspace, settings.workspace_id)

        if workspace is None:
            raise NotFound()
        if str(workspace.tdeiProjectGroupId) not in user.get("project_group_ids"):
            raise NotFound()

        quest = db.session.get(WorkspaceLongQuest, settings.workspace_id)

        if quest is None:
            quest = WorkspaceLongQuest()
            quest.workspace_id = settings.workspace_id
            db.session.add(quest)

        quest.type = QuestDefinitionType[settings.type].value
        quest.definition = settings.definition
        quest.url = settings.url
        quest.modifiedBy = uuid.UUID(user.get("id"))
        quest.modifiedByName = ""
        db.session.commit()

    @staticmethod
    def save_imagery_definition(workspace_id: int, imagery_definition: str, projectGroupIds: list):
        workspace = db.session.get(Workspace, workspace_id)

        if workspace is None:
            raise NotFound()

        if str(workspace.tdeiProjectGroupId) not in projectGroupIds:
            raise NotFound()

        imagery = db.session.get(WorkspaceImagery, workspace_id)

        if imagery is None:
            imagery = WorkspaceImagery()
            imagery.workspace_id = workspace_id
            db.session.add(imagery)

        imagery.definition = imagery_definition
        imagery.modifiedBy = uuid.UUID(int=0)
        imagery.modifiedByName = ""

        db.session.commit()

    @staticmethod
    def get_workspace_imagery(workspace_id: int,  projectGroupIds: list) -> WorkspaceImagery:
        workspace = db.session.get(Workspace, workspace_id)

        if workspace is None:
            raise NotFound()

        if str(workspace.tdeiProjectGroupId) not in projectGroupIds:
            raise NotFound()

        imagery = db.session.get(WorkspaceImagery, workspace_id)

        return imagery
