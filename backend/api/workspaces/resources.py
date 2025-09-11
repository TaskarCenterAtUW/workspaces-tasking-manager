import json
import geojson
import jsonschema
from backend.services.users.authentication_service import token_auth
from backend.config import EnvironmentConfig

from typing import cast
from geoalchemy2 import Geometry, Geography
from geoalchemy2.functions import ST_GeomFromGeoJSON, ST_SetSRID, ST_MakePoint, ST_Buffer, ST_Intersects

from flask import Response, jsonify
from flask_restful import Resource, current_app, request
from schematics.exceptions import DataError

from backend.models.postgis.utils import NotFound
from backend.models.postgis.workspace import Workspace
from backend.models.postgis.workspace_long_quest import WorkspaceLongQuest
from backend.services.workspaces_service import WorkspacesService
from backend.utils.validate_schema import validate_json_against_schema

class WorkspacesRestAPI(Resource):
    @token_auth.login_required
    def get(self, workspace_id: int):
        authenticated_user = token_auth.current_user()      
        if authenticated_user is None:
            return {"Error": "Authentication is not valid.", "SubCode": "Not Authorized"}, 401

        try:
            workspace =  WorkspacesService.get_workspace(workspace_id, authenticated_user.get("project_group_ids")).as_dto().to_primitive()
            imagery_list = WorkspacesService.get_workspace_imagery(workspace.get("id"), authenticated_user.get("project_group_ids"))
            longform_quest_obj = WorkspacesService.get_workspace_long_form_quest(workspace.get("id"), authenticated_user.get("project_group_ids"))
            longform_quest = longform_quest_obj.as_dto() if longform_quest_obj else None
            workspace["imageryListDef"] = imagery_list.definition if imagery_list else []
            workspace["longFormQuestDef"] = longform_quest.definition if longform_quest else {}
            return workspace
        except NotFound:
            return {"Error": "Workspace not found", "SubCode": "NotFound"}, 404

    @token_auth.login_required
    def patch(self, workspace_id: int):
        authenticated_user = token_auth.current_user()      
        if authenticated_user is None:
            return {"Error": "Authentication is not valid.", "SubCode": "Not Authorized"}, 401

        try:
            error_type = None
            payload = request.get_json()
            workspace = WorkspacesService.get_workspace(workspace_id, authenticated_user.get("project_group_ids"))

            if "title" in payload:
                workspace.title = payload["title"]
            if "description" in payload:
                workspace.description = payload["description"]
            if "externalAppAccess" in payload:
                workspace.externalAppAccess = payload["externalAppAccess"]

            workspace.update()

            return Response(status=204)
        except jsonschema.ValidationError as e:
            return {"Error": f"Invalid {error_type}: {e.message} at {list(e.path)}",  "SubCode": "InvalidData"}, 400
        except NotFound:
            return {"Error": "Workspace not found", "SubCode": "NotFound"}, 404

    @token_auth.login_required
    def delete(self, workspace_id: int):
        authenticated_user = token_auth.current_user()      
        if authenticated_user is None:
            return {"Error": "Authentication is not valid.", "SubCode": "Not Authorized"}, 401

        try:
            WorkspacesService.delete_workspace(workspace_id, authenticated_user.get("project_group_ids"))
            return Response(status=204)
        except NotFound:
            return {"Error": "Workspace not found", "SubCode": "NotFound"}, 404

# filter these once auth is working
class WorkspacesMineAPI(Resource):
    def get(self):
        return WorkspacesListAPI.get(self)

class WorkspacesListAPI(Resource):
    @token_auth.login_required
    def get(self):
        authenticated_user = token_auth.current_user()      
        if authenticated_user is None:
            return {"Error": "Authentication is not valid.", "SubCode": "Not Authorized"}, 401

        externalAppOnly = False
        if 'gig_only' in request.args:
            externalAppOnly = (request.args['gig_only'] == "true" 
                               or request.args['gig_only'] == "1")

        if 'externalAppAccess' in request.args:
            externalAppOnly = (request.args['externalAppAccess'] == "true" 
                               or request.args['externalAppAccess'] == "1")
        
        r = []
        for w in WorkspacesService.list_workspaces(externalAppOnly, authenticated_user.get("project_group_ids")):
#            tdeiMetadata = {}
                        
#            if 'lat' in request.args and 'lon' in request.args:
#                try:
#                    if w.tdeiMetadata is not None:
#                        tdeiMetadata = json.loads(w.tdeiMetadata)
#                except json.JSONDecodeError:
#                    pass
                    
#                if ('metadata' in tdeiMetadata and
#                    'dataset_detail' in tdeiMetadata['metadata'] and
#                    'dataset_area' in tdeiMetadata['metadata']['dataset_detail']):
#                        dataset_area = tdeiMetadata['metadata']['dataset_detail']['dataset_area']

#                        if dataset_area is not None:
#                            dataset_area_object = geojson.loads(json.dumps(dataset_area))

#                            for feature in dataset_area_object['features']:
#                                datasetAreaGeom = ST_GeomFromGeoJSON(feature['geometry'])
#                                userLocationGeom = ST_SetSRID(ST_MakePoint(request.args['lon'], request.args['lat']), 4326)

#                                if 'radius' in request.args:
#                                    try:
#                                        userLocationGeom = ST_Buffer(
#                                                                ST_SetSRID(ST_MakePoint(request.args['lon'], request.args['lat']), 4326), 
#                                                                int(request.args['radius'])
#                                                            )
#                                    except ValueError:
#                                        pass
                            
#                                # dataset area intersects with user location
#                                if ST_Intersects(datasetAreaGeom, userLocationGeom):
#                                    r.append(w.as_dto().to_primitive())

#                        # dataset has no area, so include (FIXME?)
#                        else:
#                            r.append(w.as_dto().to_primitive())

#                # dataset has no metadata, include
#                else:
#                    r.append(w.as_dto().to_primitive())
#                    
#            # no user location provided, so include
#            else:
            
            r.append(w.as_dto().to_primitive())
            
        return r

    @token_auth.login_required
    def post(self):
        authenticated_user = token_auth.current_user()      
        if authenticated_user is None:
            return {"Error": "User is not authenticated", "SubCode": "Not Authorized"}, 401

        try:
            payload = request.get_json()
            workspace = Workspace()
            workspace.title = payload["title"]
            workspace.type = payload["type"]
            workspace.tdeiRecordId = payload.get("tdeiRecordId")
            workspace.tdeiProjectGroupId = payload["tdeiProjectGroupId"]

            if workspace.tdeiProjectGroupId not in authenticated_user.get("project_group_ids"):
                return {"Error": "No permission for that project group", "SubCode": "Not Authorized"}, 401

            workspace.tdeiServiceId = payload.get("tdeiServiceId")
            workspace.tdeiMetadata = payload.get("tdeiMetadata")
            workspace.createdBy = payload["createdBy"]
            workspace.createdByName = payload["createdByName"]

            # workspace.validate()
        except DataError as e:
            current_app.logger.error(f"error validating request: {str(e)}")
            return {"Error": "Unable to create workspace", "SubCode": "InvalidData"}, 400

        workspace.create()

        return {"workspaceId": workspace.id}, 201


class WorkspacesStaticQuestAPI(Resource):
  def get(self, workspace_id: int):
        return jsonify([
            "AddCrossingMarking",
            "AddCrossingRamps",
            "AddCrossingKerbHeight",
            "AddKerbHeight",
            "AddSidewalkWidth",
            "AddHandrail",
            "AddStepsRamp",
            "AddStepsIncline",
            "AddTactilePavingSteps",
            "AddStairNumber",
            "AddWayLit",
            "AddSidewalkSurface"
        ])


class WorkspacesLongFormQuestAPI(Resource):
    @token_auth.login_required
    def get(self, workspace_id: int):
        authenticated_user = token_auth.current_user()      
        if authenticated_user is None:
            return {"Error": "User is not authenticated", "SubCode": "Not Authorized"}, 401
        
        try:
            longform_quest = WorkspacesService.get_workspace_long_form_quest(workspace_id, authenticated_user.get("project_group_ids"))
            if longform_quest is None:
                raise NotFound()
            return Response(
                response=longform_quest.definition,
                status=200,
                mimetype="application/json"
            )
        except NotFound as e:
            return Response(status=204)

    @token_auth.login_required
    def put(self, workspace_id: int):
        authenticated_user = token_auth.current_user()      
        if authenticated_user is None:
            return {"Error": "User is not authenticated", "SubCode": "Not Authorized"}, 401

        definitionJson = request.get_data(True, True)
        WorkspacesService.save_long_form_quest(workspace_id, definitionJson, authenticated_user.get("project_group_ids"))
        return Response(status=204)