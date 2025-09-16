import uuid

from backend import db
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
    def get_workspace_long_form_quest(workspace_id: int, projectGroupIds: list) -> WorkspaceLongQuest:
        workspace = db.session.get(Workspace, workspace_id)

        if workspace is None:
            raise NotFound()

        if str(workspace.tdeiProjectGroupId) not in projectGroupIds:
            raise NotFound()    
        
        quest = db.session.get(WorkspaceLongQuest, workspace_id)
        
        if quest is None:
            return None
        
        return quest

    @staticmethod
    def save_long_form_quest(workspace_id: int, definition: str, projectGroupIds: list):
        workspace = db.session.get(Workspace, workspace_id)
        
        if workspace is None:
            raise NotFound()
        
        if str(workspace.tdeiProjectGroupId) not in projectGroupIds:
            raise NotFound()    
        
        quest = db.session.get(WorkspaceLongQuest, workspace_id)

        if quest is None:
            quest = WorkspaceLongQuest()
            quest.workspace_id = workspace_id
            db.session.add(quest)

        quest.definition = definition
        quest.modifiedBy = uuid.UUID(int=0)
        quest.modifiedByName = ""
        db.session.commit()
        
    @staticmethod
    def save_long_form_and_imagery_definition(workspace_id: int, long_form_definition: str, imagery_definition: str, projectGroupIds: list):
        workspace = db.session.get(Workspace, workspace_id)
        
        if workspace is None:
            raise NotFound()
        
        if str(workspace.tdeiProjectGroupId) not in projectGroupIds:
            raise NotFound()    
        
        quest = db.session.get(WorkspaceLongQuest, workspace_id)

        if quest is None:
            quest = WorkspaceLongQuest()
            quest.workspace_id = workspace_id
            db.session.add(quest)

        quest.definition = long_form_definition
        quest.modifiedBy = uuid.UUID(int=0)
        quest.modifiedByName = ""
        
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

        if imagery is None:
            return None

        return imagery