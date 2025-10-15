import json
import jsonschema
from enum import Enum
from schematics import Model
from schematics.exceptions import ValidationError
from schematics.types import (
    StringType,
    BaseType,
    IntType,
    DictType,
    UTCDateTimeType,
    UUIDType,
)

from backend.config import EnvironmentConfig
from backend.utils.validate_schema import validate_json_against_schema


def is_known_type(value):
    """Validates that supplied quest definition type is a known value"""
    try:
        QuestDefinitionType[value]
    except KeyError:
        raise ValidationError(
            f"Unknown type: '{value}'. Valid values are "
            f"{QuestDefinitionType.JSON.name}, {QuestDefinitionType.URL.name}"
        )

class QuestDefinitionType(Enum):
    NONE = 0
    JSON = 1
    URL = 2


class WorkspaceLongQuestDTO(Model):
    workspace_id = IntType()
    type = StringType(validators=[is_known_type])
    definition  = StringType()
    url = StringType()
    modified_at = UTCDateTimeType()
    modified_by = UUIDType()
    modified_by_name = StringType()

    def validate_definition(self, data, value):
        if QuestDefinitionType[data["type"]] == QuestDefinitionType.NONE:
            if not value:
                return None
            raise ValidationError("'definition' field not allowed.")

        if QuestDefinitionType[data["type"]] != QuestDefinitionType.JSON:
            return value

        if not value:
            raise ValidationError("This field is required.")
        if data["url"]:
            raise ValidationError("'url' field not allowed.")

        try:
            parsed = json.loads(value)
            if not parsed or not isinstance(parsed, dict):
                raise ValidationError("must be a JSON object.")
            validate_json_against_schema(parsed, EnvironmentConfig.WS_LONGFORM_SCHEMA_URL)
        except json.JSONDecodeError as e:
            return ValidationError(e);
        except jsonschema.ValidationError as e:
            raise ValidationError(f"{e.message} at {list(e.path)}")

        return value

    def validate_url(self, data, value):
        if QuestDefinitionType[data["type"]] == QuestDefinitionType.NONE:
            if not value:
                return None
            raise ValidationError("'url' field not allowed.")

        if QuestDefinitionType[data["type"]] != QuestDefinitionType.URL:
            return value

        if not value:
            raise ValidationError("This field is required.")
        if data["definition"]:
            raise ValidationError("'definition' field not allowed.")

        return value
