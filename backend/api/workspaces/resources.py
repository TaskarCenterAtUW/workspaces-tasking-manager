import json
import geojson
from flask import Response, jsonify
from flask_restful import Resource, current_app, request
from schematics.exceptions import DataError

from backend.models.postgis.utils import NotFound
from backend.models.postgis.workspace import Workspace
from backend.services.workspaces_service import WorkspacesService


class WorkspacesRestAPI(Resource):
    def get(self, workspace_id: int):
        try:
            return WorkspacesService.get_workspace(workspace_id).as_dto().to_primitive()
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
        return [w.as_dto().to_primitive() for w in WorkspacesService.list_workspaces()]

    def post(self):
        try:
            payload = request.get_json()
            workspace = Workspace()
            workspace.title = payload["title"]
            workspace.tdeiRecordId = payload["tdeiRecordId"]
            workspace.tdeiProjectGroupId = payload["tdeiProjectGroupId"]
            workspace.tdeiServiceId = payload["tdeiServiceId"]
            workspace.tdeiMetadata = payload["tdeiMetadata"]

            # workspace.validate()
        except DataError as e:
            current_app.logger.error(f"error validating request: {str(e)}")
            return {"Error": "Unable to create workspace", "SubCode": "InvalidData"}, 400

        workspace.create()
        return {"workspaceId": workspace.id}, 201

class WorkspacesStaticQuestAPI(Resource):
    def get(self):
        return

class WorkspacesLongFormQuestAPI(Resource):
    def get(self, workspace_id: int):
        return jsonify([
          {
            "element_type": "Sidewalks",
            "quest_query": "ways with (highway = footway and footway = sidewalk)",
            "quests": [
              {
                "quest_id": 1,
                "quest_title": "What is the type of surface of the sidewalk?",
                "quest_description": "Choose the type of urface of the sidewalk",
                "quest_type": "ExclusiveChoie",
                "quest_tag": "surface",
                "quest_answer_choices": [
                  {
                    "value": "asphalt",
                    "choice_text": "Asphalt",
                    "image_url": "http://some_url.com/image.jpg"
                  },
                  {
                    "value": "concrete",
                    "choice_text": "Concrete",
                    "image_url": "http://some_url.com/image.jpg"
                  },
                  {
                    "value": "other",
                    "choice_text": "Brick",
                    "image_url": "http://some_url.com/image.jpg"
                  }
                ]
              },
              {
                "quest_id": 2,
                "quest_type": "Numeric",
                "quest_title": "What is the width of the sidewalk?",
                "quest_description": "Enter the width of the sidewalk in meters",
                "quest_tag": "width",
                "quest_answer_choices": [],
                "quest_answer_validation": {
                  "min": 0,
                  "max": 10
                }
              },
              {
                "quest_id": 2,
                "quest_title": "A title for multiple choices",
                "quest_query": "query_string_goes_here",
                "quest_type": "MultipleChoice",
                "quest_answer_choices": [
                  "Choice 1",
                  "Choice 2",
                  "Choice 3"
                ]
              },
              {
                "quest_id": 3,
                "quest_title": "A free form quest",
                "quest_query": "query_string_goes_here",
                "quest_type": "FreeForm",
                "quest_answer_choices": []
              }
            ]
          },
          {
            "element_type": "Kerb",
            "quest_query": "nodes, ways with (barrier = kerb)",
            "quests": [
              {
                "quest_id": 3,
                "quest_title": " What is the type of curb?",
                "quest_description": "Choose the type of curb",
                "quest_type": "ExclusiveChoie",
                "quest_tag": "curb",
                "quest_answer_choices": [
                  {
                    "value": "rolled",
                    "choice_text": "Rolled",
                    "image_url": "http://some_url.com/image.jpg"
                  },
                  {
                    "value": "flush",
                    "choice_text": "Flush",
                    "image_url": "http://some_url.com/image.jpg"
                  },
                  {
                    "value": "lowered",
                    "choice_text": "Lowered",
                    "image_url": "http://some_url.com/image.jpg"
                  }
                ],
                "child": [
                  {
                    "quest_id": 4,
                    "condition": "lowered"
                  }
                ]
              },
              {
                "quest_id": 4,
                "dependent_on": 3,
                "quest_title": "Is there a tactile strip on this curb?",
                "quest_description": "Choose the presence of tactile strip",
                "quest_type": "ExclusiveChoie",
                "quest_tag": "tactile_strip",
                "quest_answer_choices": [
                  {
                    "value": "yes",
                    "choice_text": "Yes",
                    "image_url": "http://some_url.com/image.jpg"
                  },
                  {
                    "value": "no",
                    "choice_text": "No",
                    "image_url": "http://some_url.com/image.jpg"
                  }
                ]
              }
            ]
          }
        ])
