import json
import geojson
from flask import Response, jsonify
from flask_restful import Resource, current_app, request
from schematics.exceptions import DataError

from backend.models.postgis.utils import NotFound
from backend.models.postgis.workspace import Workspace
from backend.models.postgis.workspace_long_quest import WorkspaceLongQuest
from backend.services.workspaces_service import WorkspacesService


class WorkspacesRestAPI(Resource):
    def get(self, workspace_id: int):
        try:
            return WorkspacesService.get_workspace(workspace_id).as_dto().to_primitive()
        except NotFound:
            return {"Error": "Workspace not found", "SubCode": "NotFound"}, 404

    def patch(self, workspace_id: int):
        try:
            payload = request.get_json()
            workspace = WorkspacesService.get_workspace(workspace_id)

            if "title" in payload:
                workspace.title = payload["title"]
            if "description" in payload:
                workspace.description = payload["description"]
            if "externalAppAccess" in payload:
                workspace.externalAppAccess = payload["externalAppAccess"]

            workspace.update()

            return Response(status=204)

        except NotFound:
            return {"Error": "Workspace not found", "SubCode": "NotFound"}, 404

    def delete(self, workspace_id: int):
        try:
            WorkspacesService.delete_workspace(workspace_id)
            return Response(status=204)
        except NotFound:
            return {"Error": "Workspace not found", "SubCode": "NotFound"}, 404


class WorkspacesMineAPI(Resource):
    def get(self):
        return [w.as_dto().to_primitive() for w in WorkspacesService.list_workspaces()]


class WorkspacesListAPI(Resource):
    def get(self):
        externalAppOnly = 'gig_only' in request.args

        return [
            w.as_dto().to_primitive()
            for w
            in WorkspacesService.list_workspaces(externalAppOnly)
        ]

    def post(self):
        try:
            payload = request.get_json()
            workspace = Workspace()
            workspace.title = payload["title"]
            workspace.type = payload["type"]
            workspace.tdeiRecordId = payload.get("tdeiRecordId")
            workspace.tdeiProjectGroupId = payload["tdeiProjectGroupId"]
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
    def get(self, workspace_id: int):
        try:
            return Response(
                response=WorkspacesService.get_workspace_long_form_quest(workspace_id).definition,
                status=200,
                mimetype="application/json"
            )
        except NotFound as e:
            return Response(status=204)

    def put(self, workspace_id: int):
        definitionJson = request.get_data(True, True)
        WorkspacesService.save_long_form_quest(workspace_id, definitionJson)
        return Response(status=204)
