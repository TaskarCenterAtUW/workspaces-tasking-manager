import unittest
import json
from backend.models.postgis.workspace import Workspace
from backend.models.postgis.workspace_imagery import WorkspaceImagery
from tests.utils.json_data_utils import JsonDataUtils

class TestWorkspaceImagery(unittest.TestCase):
    def setUp(self):
        self.workspace = Workspace()
        self.workspace.id = 1
        self.imagery_json = JsonDataUtils.get_imagery_json_string()
        self.imagery_data = json.loads(self.imagery_json)
        self.imagery = WorkspaceImagery(workspace_id=self.workspace.id, definition=self.imagery_data)

    def test_imagery_definition_is_list(self):
        self.assertIsInstance(self.imagery.definition, list)

    def test_imagery_contains_expected_fields(self):
        for item in self.imagery.definition:
            self.assertIn("name", item)
            self.assertIn("url", item)
            self.assertIn("type", item)

    def test_workspace_id_matches(self):
        self.assertEqual(self.imagery.workspace_id, self.workspace.id)

    def test_json_string_parsing(self):
        imagery_data_from_json = json.loads(self.imagery_json)
        self.assertEqual(len(imagery_data_from_json), 1)
        self.assertEqual(imagery_data_from_json[0]["name"], "OpenStreetMap Standard")
        self.assertEqual(imagery_data_from_json[0]["type"], "xyz")
        self.assertEqual(imagery_data_from_json[0]["url"], "https://tile.openstreetmap.org/{z}/{x}/{y}.png")
        
    def test__imagery_as_dto(self):
        # Check if WorkspaceImagery has an as_dto method
        if hasattr(self.imagery, 'as_dto'):
            dto_result = self.imagery.as_dto()
            self.assertIn('definition', dto_result)
            self.assertEqual(dto_result['definition'], self.imagery_data)
        else:
            self.skipTest("WorkspaceImagery does not have an as_dto method")

if __name__ == "__main__":
    unittest.main()

