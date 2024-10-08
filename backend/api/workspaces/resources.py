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
        return jsonify([
            {
                "element_type": "Sidewalks",
                "quest_query": "highway=footway and footway=sidewalk",
                "quests": [
                    {
                        "quest_id": 1,
                        "quest_title": "What type of surface is the sidewalk?",
                        "quest_description": "Choose the type of surface of the sidewalk",
                        "quest_type": "ExclusiveChoice",
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
                                "value": "brick",
                                "choice_text": "Brick",
                                "image_url": "http://some_url.com/image.jpg"
                            }
                        ]
                    },
                    {
                        "quest_id": 2,
                        "quest_title": "Are there small surface cracks or disruptions?",
                        "quest_description": "Identify if there are any cracks or disruptions in the sidewalk surface that are smaller than 3 inch vertical or horizontal displacement, or smaller than 3 inch gaps",
        		"quest_image_url":  "http://some_url.com/image.jpg",
                        "quest_type": "ExclusiveChoice",
                        "quest_tag": "small_surface_cracks",
                        "quest_answer_choices": [
                            {
                                "value": "no",
                                "choice_text": "No",
                                "image_url": "http://some_url.com/image.jpg"
                            },
                            {
                                "choice_text": "1-5 small cracks or disruptions along this sidewalk",
                                "value": "1-5",
          			"choice_follow_up" : "Please take a picture of the largest disruption in this sidewalk"
                            },
                            {
                                "choice_text": "6-10 small cracks or disruptions along this sidewalk",
                                "value": "6-10",
          			"choice_follow_up" : "Please take a picture of the largest disruption in this sidewalk"
                            },
                            {
                                "choice_text": "more than 10 small cracks or disruptions along this sidewalk",
                                "value": ">10",
          			"choice_follow_up" : "Please take a picture of the largest disruption in this sidewalk"
                            }
                        ]
                    },
                    {
                        "quest_id": 3,
                        "quest_title": "Are there large surface cracks, large disruptions, tree uproots, or large gaps in the sidewalk?",
                        "quest_description": "Identify if there are any large surface disruptions (greater than 3 inches in any direction) in the sidewalk surface",
        		"quest_image_url":  "http://some_url.com/image.jpg",
                        "quest_type": "ExclusiveChoice",
                        "quest_tag": "large_surface_cracks",
                        "quest_answer_choices": [
                            {
                                "value": "0",
                                "choice_text": "No"
                            },
                            {
                                "choice_text": "1-5 large disruptions or gaps along this sidewalk",
                                "value": "<5",
                                "image_url": "http://some_url.com/image.jpg",
          			"choice_follow_up" : "Please take a picture of the largest disruption in this sidewalk"
                            },
                            {
                                "choice_text": "6-10 large disruptions or gaps along this sidewalk",
                                "value": "<10",
                                "image_url": "http://some_url.com/image.jpg",
          			"choice_follow_up" : "Please take a picture of the largest disruption in this sidewalk"
                            },
                            {
                                "choice_text": "more than 10 large disruptions or gaps along this sidewalk",
                                "value": ">10",
                                "image_url": "http://some_url.com/image.jpg",
          			"choice_follow_up" : "Please take a picture of the largest disruption in this sidewalk"
                            }
                        ]
                    },
                    {
                        "quest_id": 4,
                        "quest_title": "Is the sidewalk complete along the entire block?",
                        "quest_description": "Check if the sidewalk extends continuously along the entire block",
        		"quest_image_url":  "http://some_url.com/image.jpg",
                        "quest_type": "ExclusiveChoice",
                        "quest_tag": "sidewalk_complete",
                        "quest_answer_choices": [
                            {
                                "value": "yes",
                                "choice_text": "Yes",
                                "image_url": "http://some_url.com/image.jpg"
                            },
                            {
                                "value": "no",
                                "choice_text": "No",
                                "image_url": "http://some_url.com/image.jpg",
          			"choice_follow_up" : "Please take a picture of the gap or missing sidewalk"

                            }
                        ]
                    },
                    {
                        "quest_id": 5,
                        "quest_title": "Does the sidewalk narrow?",
                        "quest_description": "Identify if there are any sections where the sidewalk narrows",
        		"quest_image_url":  "http://some_url.com/image.jpg",
                        "quest_type": "ExclusiveChoice",
                        "quest_tag": "sidewalk_narrows",
                        "quest_answer_choices": [
                            {
                                "value": "yes",
                                "choice_text": "Yes",
                                "image_url": "http://some_url.com/image.jpg",
        			"choice_follow_up" : "Please take a picture of the narrowest place on this sidewalk"
                            },
                            {
                                "value": "no",
                                "choice_text": "No",
                                "image_url": "http://some_url.com/image.jpg"
                            }
                        ]
                    },
                    {
                        "quest_id": 6,
                        "quest_title": "How many driveways intersect the sidewalk?",
                        "quest_description": "Enter the number of driveways that intersect the sidewalk",
         		"quest_image_url":  "http://some_url.com/image.jpg",
                        "quest_type": "Numeric",
                        "quest_tag": "driveways",
                        "quest_answer_choices": [],
                        "quest_answer_validation": {
                            "min": 0
                        }
                    },
                    {
                        "quest_id": 7,
                        "quest_title": "How many light poles are along the sidewalk?",
                        "quest_description": "Enter the number of light poles along the sidewalk",
        		"quest_image_url":  "http://some_url.com/image.jpg",
                        "quest_type": "Numeric",
                        "quest_tag": "light_poles",
                        "quest_answer_choices": [],
                        "quest_answer_validation": {
                            "min": 0
                        }
                    },
                    {
                        "quest_id": 8,
                        "quest_title": "How many manholes are on the sidewalk?",
                        "quest_description": "Enter the number of manholes on the sidewalk",
        		"quest_image_url":  "http://some_url.com/image.jpg",
                        "quest_type": "Numeric",
                        "quest_tag": "manholes",
                        "quest_answer_choices": [],
                        "quest_answer_validation": {
                            "min": 0
                        }
                    },
                    {
                        "quest_id": 9,
                        "quest_title": "Is there a crossing in the middle of this block?",
                        "quest_description": "Check if there is a pedestrian crossing in the middle of the block",
        		"quest_image_url":  "http://some_url.com/image.jpg",
                        "quest_type": "ExclusiveChoice",
                        "quest_tag": "midblock_crossing",
                        "quest_answer_choices": [
                            {
                                "value": "yes",
                                "choice_text": "Yes"
                            },
                            {
                                "value": "no",
                                "choice_text": "No"
                            }
                        ]
                    }
                ]
            },
            {
                "element_type": "Kerb",
                "quest_query": "barrier=kerb",
                "quests": [
                    {
                        "quest_id": 1,
                        "quest_title": "Is there a traffic island directly reachable from this curb?",
                        "quest_description": "Check if there is a traffic island directly reachable from this curbpoint",
                        "quest_type": "ExclusiveChoice",
                        "quest_tag": "traffic_island",
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
                    },
                    {
                        "quest_id": 2,
                        "quest_title": "Is there a roundabout or traffic circle  at this intersection?",
                        "quest_description": "Check if there is a roundabout at this intersection",
                        "quest_type": "ExclusiveChoice",
                        "quest_tag": "traffic_circle",
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
                    },
                    {
                        "quest_id": 3,
                        "quest_title": "Is there a curb extension at this corner?",
                        "quest_description": "Check if there is a curb extension at this corner",
                        "quest_type": "ExclusiveChoice",
                        "quest_tag": "curb_extension",
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
                    },
                    {
                        "quest_id": 4,
                        "quest_title": "Are there 0, 1 or 2 curb cuts at this corner?",
                        "quest_description": "Indicate if there are 1 or 2 curb cuts at this corner",
                        "quest_type": "ExclusiveChoice",
                        "quest_tag": "curb_cuts",
                        "quest_answer_choices": [
                            {
                                "value": "0",
                                "choice_text": "No Curb ramps here",
                                "image_url": "http://some_url.com/image.jpg"
                            },
                            {
                                "value": "1",
                                "choice_text": "1",
                                "image_url": "http://some_url.com/image.jpg"
                            },
                            {
                                "value": "2",
                                "choice_text": "2",
                                "image_url": "http://some_url.com/image.jpg"
                            }
                        ]
                    },
                    {
                        "quest_id": 5,
                        "quest_title": "If there is 1, is it facing only one side of the street, or is the curb ramp facing toward the middle of the intersection?",
                        "quest_description": "Specify the orientation of the single curb cut",
                        "quest_type": "ExclusiveChoice",
                        "quest_tag": "curb_cut_orientation",
                        "quest_answer_choices": [
                            {
                                "value": "one_side",
                                "choice_text": "One side of the street",
                                "image_url": "http://some_url.com/image.jpg"
                            },
                            {
                                "value": "middle_intersection",
                                "choice_text": "Middle of the intersection",
                                "image_url": "http://some_url.com/image.jpg"
                            }
                        ],
                        "quest_answer_dependency": {
                            "question_id": 4,
                            "required_value": "1"
                        }
                    },
                    {
                        "quest_id": 6,
                        "quest_title": "If there is a curb cut, is there tactile paving on this curb cut?",
                        "quest_description": "Check if there is tactile paving on the curb cut",
                        "quest_type": "ExclusiveChoice",
                        "quest_tag": "tactile_paving",
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
                        ],
                        "quest_answer_dependency": {
                            "question_id": 4,
                            "required_value": ["1", "2"]
                        }
                    },
                    {
                        "quest_id": 7,
                        "quest_title": "If there are no curb cuts, is there a raised curb here or is it flush with the street?",
                        "quest_description": "Specify if the curb is raised or flush with the street when there are no curb cuts",
                        "quest_type": "ExclusiveChoice",
                        "quest_tag": "curb_status",
                        "quest_answer_choices": [
                            {
                                "value": "raised",
                                "choice_text": "Raised",
                                "image_url": "http://some_url.com/image.jpg"
                            },
                            {
                                "value": "flush",
                                "choice_text": "Flush",
                                "image_url": "http://some_url.com/image.jpg"
                            }
                        ],
                        "quest_answer_dependency": {
                            "question_id": 4,
                            "required_value": "0"
                        }
                    },
                    {
                        "quest_id": 8,
                        "quest_title": "Is there a bike lane immediately after you get off the curb at this corner?",
                        "quest_description": "Check if there is a bike lane immediately after the curb",
                        "quest_type": "ExclusiveChoice",
                        "quest_tag": "bike_lane",
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
            },
            {
                "element_type": "Crossings",
                "quest_query": "highway=footway and footway=crossing",
                "quests": [
                    {
                        "quest_id": 1,
                        "quest_title": "Does this crossing have markings?",
                        "quest_description": "Check if there are any markings on the crossing",
                        "quest_type": "ExclusiveChoice",
                        "quest_tag": "crossing_markings",
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
                    },
                    {
                        "quest_id": 2,
                        "quest_title": "Does this crossing have traffic signals for cars?",
                        "quest_description": "Check if there are traffic signals for cars at this crossing",
                        "quest_type": "ExclusiveChoice",
                        "quest_tag": "traffic_signals_cars",
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
                    },
                    {
                        "quest_id": 3,
                        "quest_title": "Does this crossing have stop signals for cars?",
                        "quest_description": "Check if there are stop signals for cars at this crossing",
                        "quest_type": "ExclusiveChoice",
                        "quest_tag": "stop_signals_cars",
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
                    },
                    {
                        "quest_id": 4,
                        "quest_title": "Does this crossing have signals for pedestrians?",
                        "quest_description": "Check if there are signals for pedestrians at this crossing",
                        "quest_type": "ExclusiveChoice",
                        "quest_tag": "pedestrian_signals",
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
                    },
                    {
                        "quest_id": 5,
                        "quest_title": "If there's a pedestrian signal, is there a call button for it?",
                        "quest_description": "Check if there is a call button for the pedestrian signal",
                        "quest_type": "ExclusiveChoice",
                        "quest_tag": "call_button",
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
                        ],
                        "quest_answer_dependency": {
                            "question_id": 4,
                            "required_value": "yes"
                        }
                    },
                    {
                        "quest_id": 6,
                        "quest_title": "If there's a pedestrian signal, is there a sound or speech that tells you the signal is on?",
                        "quest_description": "Check if there is a sound or speech that indicates the pedestrian signal is on",
                        "quest_type": "ExclusiveChoice",
                        "quest_tag": "audio_signal",
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
                        ],
                        "quest_answer_dependency": {
                            "question_id": 4,
                            "required_value": "yes"
                        }
                    },
                    {
                        "quest_id": 7,
                        "quest_title": "If there's a pedestrian signal, is there a vibrating plate that tells you the signal is on?",
                        "quest_description": "Check if there is a vibrating plate that indicates the pedestrian signal is on",
                        "quest_type": "ExclusiveChoice",
                        "quest_tag": "vibrating_plate",
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
                        ],
                        "quest_answer_dependency": {
                            "question_id": 4,
                            "required_value": "yes"
                        }
                    },
                    {
                        "quest_id": 8,
                        "quest_title": "Is the surface of this crossing raised?",
                        "quest_description": "Check if the surface of this crossing is raised",
                        "quest_type": "ExclusiveChoice",
                        "quest_tag": "raised_surface",
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
