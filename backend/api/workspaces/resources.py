import json
import geojson

from typing import cast
from geoalchemy2 import Geometry, Geography
from geoalchemy2.functions import ST_GeomFromGeoJSON, ST_SetSRID, ST_MakePoint, ST_Buffer, ST_Intersects

from backend.models.postgis.utils import NotFound
from backend.models.postgis.workspace import Workspace
from backend.models.postgis.workspace_long_quest import WorkspaceLongQuest
from backend.services.workspaces_service import WorkspacesService

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from databases import Database

from backend.db import get_db
from backend.models.dtos.user_dto import AuthUserDTO, UserSearchQuery
from backend.services.project_service import ProjectService
from backend.services.users.authentication_service import login_required
from backend.services.users.user_service import UserService

router = APIRouter(
    prefix="/workspaces",
    tags=["workspaces"],
    responses={404: {"description": "Not found"}},
)

class WorkspacesRestAPI():
    @router.get("/{workspace_id}")
    def get(
        request: Request,
        workspace_id: int,
        request_user: AuthUserDTO = Depends(login_required),
        db: Database = Depends(get_db)
    ):
        try:
            return WorkspacesService.get_workspace(workspace_id, db).as_dto().to_primitive()
        except NotFound:
            return {"Error": "Workspace not found", "SubCode": "NotFound"}, 404

    @router.patch("/{workspace_id}")
    def patch(
        request: Request,
        workspace_id: int,
        request_user: AuthUserDTO = Depends(login_required),
        db: Database = Depends(get_db)
    ):
        try:
            payload = request.get_json()
            workspace = WorkspacesService.get_workspace(workspace_id, db)

            if "title" in payload:
                workspace.title = payload["title"]
            if "description" in payload:
                workspace.description = payload["description"]
            if "externalAppAccess" in payload:
                workspace.externalAppAccess = payload["externalAppAccess"]

            workspace.update(db)

            return Response(status=204)

        except NotFound:
            return {"Error": "Workspace not found", "SubCode": "NotFound"}, 404

    @router.delete("/{workspace_id}")
    def delete(
        request: Request,
        workspace_id: int,
        request_user: AuthUserDTO = Depends(login_required),
        db: Database = Depends(get_db)
    ):
        try:
            WorkspacesService.delete_workspace(workspace_id, db)
            return Response(status=204)
        except NotFound:
            return {"Error": "Workspace not found", "SubCode": "NotFound"}, 404

# filter these once auth is working
class WorkspacesMineAPI():
    @router.get("/mine")
    def get(
        request: Request,
        request_user: AuthUserDTO = Depends(login_required),
        db: Database = Depends(get_db)    
    ):
        return WorkspacesListAPI.get(request, request_user, db)

class WorkspacesListAPI():
    @router.get("/")
    def get(
        request: Request,
        request_user: AuthUserDTO = Depends(login_required),
        db: Database = Depends(get_db)    
    ):
        externalAppOnly = False
        
        if 'gig_only' in request.args:
            externalAppOnly = (request.args['gig_only'] == "True")

        if 'externalAppAccess' in request.args:
            externalAppOnly = (request.args['externalAppAccess'] == "True")
        
        r = []
        for w in WorkspacesService.list_workspaces(externalAppOnly, db):
            tdeiMetadata = {};
            
            if 'lat' in request.args and 'lon' in request.args:
                try:
                    if w.tdeiMetadata is not None:
                        tdeiMetadata = json.loads(w.tdeiMetadata)
                except json.JSONDecodeError as e:
                    pass
                    
                if ('metadata' in tdeiMetadata and
                    'dataset_detail' in tdeiMetadata['metadata'] and
                    'dataset_area' in tdeiMetadata['metadata']['dataset_detail']):
                        dataset_area = tdeiMetadata['metadata']['dataset_detail']['dataset_area'];

                        if dataset_area is not None:
                            dataset_area_object = geojson.loads(json.dumps(dataset_area));

                            for feature in dataset_area_object['features']:
                                datasetAreaGeom = ST_GeomFromGeoJSON(feature['geometry'])
                                userLocationGeom = ST_SetSRID(ST_MakePoint(request.args['lon'], request.args['lat']), 4326)

                                if 'radius' in request.args:
                                    try:
                                        userLocationGeom = cast(ST_Buffer(cast(
                                            ST_SetSRID(ST_MakePoint(request.args['lon'], request.args['lat']), 4326), 
                                            Geography), int(request.args['radius'])), Geometry)
                                    except ValueError:
                                        pass
                            
                                # dataset area intersects with user location
                                if ST_Intersects(datasetAreaGeom, userLocationGeom) == True:
                                    r.append(w.as_dto().to_primitive())

                        # dataset has no area, so include (FIXME?)
                        else:
                            r.append(w.as_dto().to_primitive())

                # dataset has no metadata, include
                else:
                    r.append(w.as_dto().to_primitive())
                    
            # no user location provided, so include
            else:
                r.append(w.as_dto().to_primitive())
            
        return r

    @router.post("/")
    def post(
        request: Request,
        request_user: AuthUserDTO = Depends(login_required),
        db: Database = Depends(get_db)       
    ):
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

        workspace.create(db)

        return {"workspaceId": workspace.id}, 201


class WorkspacesStaticQuestAPI():
  def get(
      request: Request,
      workspace_id: int,
      request_user: AuthUserDTO = Depends(login_required),
      db: Database = Depends(get_db)              
  ):
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


class WorkspacesLongFormQuestAPI():
    def get(self, workspace_id: int):
        try:
            return Response(
                response=WorkspacesService.get_workspace_long_form_quest(workspace_id, db).definition,
                status=200,
                mimetype="application/json"
            )
        except NotFound as e:
            return Response(status=204)

    def put(self, workspace_id: int):
        definitionJson = request.get_data(True, True)
        WorkspacesService.save_long_form_quest(workspace_id, definitionJson, db)
        return Response(status=204)
