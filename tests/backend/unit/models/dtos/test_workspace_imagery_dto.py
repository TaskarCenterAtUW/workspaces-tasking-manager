import unittest
import json
from backend.models.dtos.workspace_imagery_dto import WorkspaceImageryDTO
from tests.utils.json_data_utils import JsonDataUtils

class TestWorkspaceImageryDTO(unittest.TestCase):
    def setUp(self):
        self.imagery_json = JsonDataUtils.get_imagery_json_string()
        self.imagery_data = json.loads(self.imagery_json)
        self.dto = WorkspaceImageryDTO()
        self.dto.definition = self.imagery_data

    def test_dto_definition_is_list(self):
        self.assertIsInstance(self.dto.definition, list)

    def test_dto_contains_expected_fields(self):
        for item in self.dto.definition:
            self.assertIn("name", item)
            self.assertIn("url", item)
            self.assertIn("type", item)

if __name__ == "__main__":
    unittest.main()
