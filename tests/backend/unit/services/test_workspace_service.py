import unittest
from unittest.mock import patch, MagicMock
from backend.services.workspaces_service import WorkspacesService
from backend.models.postgis.workspace import Workspace
from tests.utils.json_data_utils import JsonDataUtils

class TestWorkspaceService(unittest.TestCase):
    
    def setUp(self):
        self.workspace_id = '1'
        self.project_group_ids = ['1', '2']

    def test_list_workspaces_externalAppOnly_False(self):
        # Create a mock query object
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_workspace1 = MagicMock()
        mock_workspace2 = MagicMock()
        mock_filter.all.return_value = [mock_workspace1, mock_workspace2]
        mock_query.filter.return_value = mock_filter

        # Pass the mock query object to the service method
        result = WorkspacesService.list_workspaces(
            externalAppOnly=False,
            projectGroupIds=[1,2],
            query_obj=mock_query
        )
        self.assertEqual(len(result), 2)
        
        
    def test_list_workspaces_externalAppOnly_True(self):
        # Create a mock query object
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_workspace1 = MagicMock()
        mock_filter.all.return_value = [mock_workspace1]
        mock_query.filter.return_value = mock_filter

        # Pass the mock query object to the service method
        result = WorkspacesService.list_workspaces(
            externalAppOnly=False,
            projectGroupIds=[1,2],
            query_obj=mock_query
        )
        self.assertEqual(len(result), 1)
    
    
    
    @patch('backend.models.postgis.workspace.db.session')
    def test_get_workspace(self, mock_db_get):
        # Arrange: mock the Workspace returned by db.session.get
        mock_workspace = MagicMock(spec=Workspace)
        mock_workspace.id = self.workspace_id
        mock_workspace.tdeiProjectGroupId = self.project_group_ids[0]
        mock_db_get.get.return_value = mock_workspace

        # Act: call the real method
        result = WorkspacesService.get_workspace(self.workspace_id, self.project_group_ids)

        # Assert: check the result
        self.assertEqual(result.id, self.workspace_id)
        self.assertEqual(result.tdeiProjectGroupId, str(self.project_group_ids[0]))
        
    @patch('backend.models.postgis.workspace.db.session')
    def test_get_workspace_project_group_id_not_present(self, mock_db_get):
        # Arrange: mock the Workspace returned by db.session.get
        mock_workspace = MagicMock(spec=Workspace)
        mock_workspace.id = self.workspace_id
        mock_workspace.tdeiProjectGroupId = '3'
        mock_db_get.get.return_value = mock_workspace

        with self.assertRaises(Exception) as context:
            WorkspacesService.get_workspace(self.workspace_id, self.project_group_ids)
        self.assertEqual(type(context.exception).__name__, "NotFound")
        
    @patch('backend.models.postgis.workspace.db.session')
    def test_get_workspace_invalid_workspace_id(self, mock_db_get):
        # Arrange: mock the Workspace returned by db.session.get
        mock_db_get.get.return_value = None
       
        with self.assertRaises(Exception) as context:
            WorkspacesService.get_workspace(self.workspace_id, self.project_group_ids)
        self.assertEqual(type(context.exception).__name__, "NotFound")
        
    @patch('backend.models.postgis.workspace.db.session')
    def test_delete_workspace(self, mock_db_get):
        # Arrange: mock the Workspace returned by db.session.get
        mock_workspace = MagicMock(spec=Workspace)
        mock_workspace.id = self.workspace_id
        mock_workspace.tdeiProjectGroupId = self.project_group_ids[0]
        mock_db_get.get.return_value = mock_workspace

        # Act: call the real method
        WorkspacesService.delete_workspace(self.workspace_id, self.project_group_ids)

        # Assert: check that the workspace was deleted
        mock_db_get.delete.assert_called_once_with(mock_workspace)
        mock_db_get.commit.assert_called_once()
        
    @patch('backend.models.postgis.workspace.db.session')
    def test_delete_workspace_invalid_workspace(self, mock_db_get):
         # Arrange: mock the Workspace returned by db.session.get
        mock_db_get.get.return_value = None
       
        with self.assertRaises(Exception) as context:
            WorkspacesService.delete_workspace(self.workspace_id, self.project_group_ids)
        self.assertEqual(type(context.exception).__name__, "NotFound")
        
    @patch('backend.models.postgis.workspace.db.session')
    def test_get_workspace_long_form_quest(self, mock_db_get):
        # Arrange: mock the WorkspaceLongQuest and Workspace returned by db.session.get
        mock_quest = MagicMock()
        mock_workspace = MagicMock(spec=Workspace)
        mock_workspace.id = self.workspace_id
        mock_workspace.tdeiProjectGroupId = self.project_group_ids[0]
        
        def side_effect(model, id):
            if model.__name__ == 'WorkspaceLongQuest':
                return mock_quest
            elif model.__name__ == 'Workspace':
                return mock_workspace
            return None
        
        mock_db_get.get.side_effect = side_effect

        # Act: call the real method
        result = WorkspacesService.get_workspace_long_form_quest(self.workspace_id, self.project_group_ids)

        # Assert: check the result
        self.assertEqual(result, mock_quest)

    @patch('backend.models.postgis.workspace.db.session')
    def test_get_workspace_long_form_quest_invalid_workspace(self, mock_db_get):
        # Arrange: mock the Workspace returned by db.session.get
        mock_db_get.get.side_effect = lambda model, _: None if model.__name__ == 'Workspace' else MagicMock()

        with self.assertRaises(Exception) as context:
            WorkspacesService.get_workspace_long_form_quest(self.workspace_id, self.project_group_ids)
        self.assertEqual(type(context.exception).__name__, "NotFound")
    
    @patch('backend.models.postgis.workspace.db.session')
    def test_get_workspace_long_form_quest_invalid_project_group(self, mock_db_get):
        # Arrange: mock the WorkspaceLongQuest and Workspace returned by db.session.get
        mock_quest = MagicMock()
        mock_workspace = MagicMock(spec=Workspace)
        mock_workspace.id = self.workspace_id
        mock_workspace.tdeiProjectGroupId = self.project_group_ids[0]
        
        def side_effect(model, id):
            if model.__name__ == 'WorkspaceLongQuest':
                return mock_quest
            elif model.__name__ == 'Workspace':
                return mock_workspace
            return None
        
        mock_db_get.get.side_effect = side_effect

        # Assert: check the result
        with self.assertRaises(Exception) as context:
            WorkspacesService.get_workspace_long_form_quest(self.workspace_id, ['3'])
        self.assertEqual(type(context.exception).__name__, "NotFound")
        
    @patch('backend.models.postgis.workspace.db.session')
    def test_get_workspace_long_form_quest_none_quest(self, mock_db_get):
        # Arrange: mock the Workspace returned by db.session.get
        mock_db_get.get.side_effect = lambda model, _: None if model.__name__ == 'WorkspaceLongQuest' else MagicMock()

        with self.assertRaises(Exception) as context:
            WorkspacesService.get_workspace_long_form_quest(self.workspace_id, self.project_group_ids)
        self.assertEqual(type(context.exception).__name__, "NotFound")

    @patch('backend.models.postgis.workspace.db.session')
    def test_get_workspace_imagery_found(self, mock_db_get):
        # Arrange: mock the imagery returned by db.session.get
        mock_imagery = MagicMock()
        mock_workspace = MagicMock(spec=Workspace)
        mock_workspace.id = self.workspace_id
        mock_workspace.tdeiProjectGroupId = self.project_group_ids[0]
        
        def side_effect(model, id):
            if model.__name__ == 'WorkspaceImagery':
                return mock_imagery
            elif model.__name__ == 'Workspace':
                return mock_workspace
            return None
        
        mock_db_get.get.side_effect = side_effect

        # Act: call the real method
        result = WorkspacesService.get_workspace_imagery(self.workspace_id, self.project_group_ids)

        # Assert: check the result
        self.assertEqual(result, mock_imagery)

    @patch('backend.models.postgis.workspace.db.session')
    def test_get_workspace_imagery_none(self, mock_db_get):
        # Arrange: mock db.session.get to return None
        mock_db_get.get.side_effect = lambda model, _: None if model.__name__ == 'WorkspaceImagery' else MagicMock()

        # Assert: check the result is None
        with self.assertRaises(Exception) as context:
            WorkspacesService.get_workspace_imagery(self.workspace_id, self.project_group_ids)
        self.assertEqual(type(context.exception).__name__, "NotFound")

    @patch('backend.models.postgis.workspace.db.session')
    def test_get_workspace_imagery_invalid_workspace(self, mock_db_get):
        mock_db_get.get.side_effect = lambda model, id: None if model.__name__ == 'Workspace' else MagicMock()
        
        with self.assertRaises(Exception) as context:
            WorkspacesService.get_workspace_imagery(self.workspace_id, self.project_group_ids)
        self.assertEqual(type(context.exception).__name__, "NotFound")
        
    @patch('backend.models.postgis.workspace.db.session')
    def test_get_workspace_imagery_invalid_project_group_id(self, mock_db_get):
        mock_db_get.get.side_effect = lambda model, id: None if model.__name__ == 'Workspace' else MagicMock()
        
        with self.assertRaises(Exception) as context:
            WorkspacesService.get_workspace_imagery(self.workspace_id, ['invalid_project_group_id'])
        self.assertEqual(type(context.exception).__name__, "NotFound")
    
    @patch('backend.models.postgis.workspace.db.session')
    def test_save_long_form_quest_create_new(self, mock_db_get):
        # Arrange: mock the Workspace returned by db.session.get
        mock_workspace = MagicMock(spec=Workspace)
        mock_workspace.id = self.workspace_id
        mock_workspace.tdeiProjectGroupId = self.project_group_ids[0]
        
        def side_effect(model, id):
            if model.__name__ == 'WorkspaceLongQuest':
                return None  # Simulate no existing quest
            elif model.__name__ == 'Workspace':
                return mock_workspace
            return None
        
        mock_db_get.get.side_effect = side_effect

        # Act: call the real method
        WorkspacesService.save_long_form_quest(self.workspace_id, JsonDataUtils.get_long_form_quest_json_string(), self.project_group_ids)

        # Assert: check that a new quest was added and committed
        mock_db_get.add.assert_called_once()
        mock_db_get.commit.assert_called_once()
        
    @patch('backend.models.postgis.workspace.db.session')
    def test_save_long_form_quest_update_existing(self, mock_db_get):
        # Arrange: mock the Workspace returned by db.session.get
        mock_workspace = MagicMock(spec=Workspace)
        mock_workspace.id = self.workspace_id
        mock_workspace.tdeiProjectGroupId = self.project_group_ids[0]
        
        def side_effect(model, id):
            if model.__name__ == 'WorkspaceLongQuest':
                return MagicMock()  # Simulate existing quest
            elif model.__name__ == 'Workspace':
                return mock_workspace
            return None
        
        mock_db_get.get.side_effect = side_effect

        # Act: call the real method
        WorkspacesService.save_long_form_quest(self.workspace_id, JsonDataUtils.get_long_form_quest_json_string(), self.project_group_ids)

        # Assert: check that a new quest was not added but changes were committed
        mock_db_get.add.assert_not_called()
        mock_db_get.commit.assert_called_once()
        
    @patch('backend.models.postgis.workspace.db.session')
    def test_save__long_form_quest_invalid_workspace(self, mock_db_get):
        # Arrange: mock the Workspace returned by db.session.get
        def side_effect(model, _):
            if model.__name__ == 'WorkspaceLongQuest':
                return MagicMock()  # Simulate existing quest
            elif model.__name__ == 'Workspace':
                return None  # Simulate invalid workspace
            return None
        
        mock_db_get.get.side_effect = side_effect
        
        with self.assertRaises(Exception) as context:
            WorkspacesService.save_long_form_and_imagery_definition(
            self.workspace_id, JsonDataUtils.get_long_form_quest_json_string(),
            JsonDataUtils.get_imagery_json_string(), self.project_group_ids
            )
        self.assertEqual(type(context.exception).__name__, "NotFound")
        
    @patch('backend.models.postgis.workspace.db.session')
    def test_save__long_form_quest_invalid_project_groups(self, mock_db_get):
        mock_workspace = MagicMock(spec=Workspace)
        mock_workspace.id = self.workspace_id
        mock_workspace.tdeiProjectGroupId = self.project_group_ids[0]
        
        def side_effect(model, id):
            if model.__name__ == 'WorkspaceLongQuest':
                return MagicMock()  # Simulate existing quest
            elif model.__name__ == 'Workspace':
                return mock_workspace
            return None
        
        mock_db_get.get.side_effect = side_effect

        # Act: call the real method        
        with self.assertRaises(Exception) as context:
            WorkspacesService.save_long_form_and_imagery_definition(
            self.workspace_id, JsonDataUtils.get_long_form_quest_json_string(),
            JsonDataUtils.get_imagery_json_string(), ['3']
            )
        self.assertEqual(type(context.exception).__name__, "NotFound")
        

        # Act: call the real method
        WorkspacesService.save_long_form_and_imagery_definition(
            self.workspace_id, None,
            JsonDataUtils.get_imagery_json_string(), self.project_group_ids
            )

        # Assert: check that a new imagery was added and committed
        mock_db_get.add.assert_called_once()
        mock_db_get.commit.assert_called_once()
        
    
    @patch('backend.models.postgis.workspace.db.session')
    def test_save__workspace_imagery_invalid_workspace(self, mock_db_get):
        # Arrange: mock the Workspace returned by db.session.get
        def side_effect(model, _):
            if model.__name__ == 'WorkspaceImagery':
                return MagicMock()  # Simulate existing imagery
            elif model.__name__ == 'Workspace':
                return None  # Simulate invalid workspace
            return None
        
        mock_db_get.get.side_effect = side_effect
        
        with self.assertRaises(Exception) as context:
            WorkspacesService.save_long_form_and_imagery_definition(
            self.workspace_id, JsonDataUtils.get_long_form_quest_json_string(),
            JsonDataUtils.get_imagery_json_string(), self.project_group_ids
            )
        self.assertEqual(type(context.exception).__name__, "NotFound")
        
    @patch('backend.models.postgis.workspace.db.session')
    def test_save__workspace_imagery_invalid_project_groups(self, mock_db_get):
        mock_workspace = MagicMock(spec=Workspace)
        mock_workspace.id = self.workspace_id
        mock_workspace.tdeiProjectGroupId = self.project_group_ids[0]
        
        def side_effect(model, id):
            if model.__name__ == 'WorkspaceImagery':
                return MagicMock()  # Simulate existing imagery
            elif model.__name__ == 'Workspace':
                return mock_workspace
            return None
        
        mock_db_get.get.side_effect = side_effect

        # Act: call the real method        
        with self.assertRaises(Exception) as context:
            WorkspacesService.save_long_form_and_imagery_definition(
            self.workspace_id, JsonDataUtils.get_long_form_quest_json_string(),
            JsonDataUtils.get_imagery_json_string(), ['3']
            )
        self.assertEqual(type(context.exception).__name__, "NotFound")

    @patch('backend.models.postgis.workspace.db.session')
    def test_save__long_form_and_imagery_definition_both_none_already_exists(self, mock_db_get):
        mock_workspace = MagicMock(spec=Workspace)
        mock_workspace.id = self.workspace_id
        mock_workspace.tdeiProjectGroupId = self.project_group_ids[0]
        
        def side_effect(model, id):
            if model.__name__ == 'WorkspaceImagery':
                return MagicMock()  # Simulate existing imagery
            if model.__name__ == 'WorkspaceLongQuest':
                return MagicMock()
            elif model.__name__ == 'Workspace':
                return mock_workspace
            return None
        
        mock_db_get.get.side_effect = side_effect
        
        WorkspacesService.save_long_form_and_imagery_definition(
            self.workspace_id, None,
            None, self.project_group_ids
        )
        
        self.assertTrue(True)
        self.assertEqual(mock_db_get.add.call_count, 0)
        self.assertEqual(mock_db_get.commit.call_count, 1)
        
    @patch('backend.models.postgis.workspace.db.session')
    def test_save__long_form_and_imagery_definition_both_none_does_not_exist(self, mock_db_get):
        mock_workspace = MagicMock(spec=Workspace)
        mock_workspace.id = self.workspace_id
        mock_workspace.tdeiProjectGroupId = self.project_group_ids[0]
        
        def side_effect(model, id):
            if model.__name__ == 'Workspace':
                return mock_workspace
            return None
        
        mock_db_get.get.side_effect = side_effect
        
        WorkspacesService.save_long_form_and_imagery_definition(
            self.workspace_id, None,
            None, self.project_group_ids
        )
        
        self.assertTrue(True)
        self.assertEqual(mock_db_get.add.call_count, 2)
        self.assertEqual(mock_db_get.commit.call_count, 1)
        
    @patch('backend.models.postgis.workspace.db.session')
    def test_save__long_form_and_imagery_definition_both_valid_data(self, mock_db_get):
        mock_workspace = MagicMock(spec=Workspace)
        mock_workspace.id = self.workspace_id
        mock_workspace.tdeiProjectGroupId = self.project_group_ids[0]
        
        def side_effect(model, id):
            if model.__name__ == 'WorkspaceImagery':
                return MagicMock()  # Simulate existing imagery
            if model.__name__ == 'WorkspaceLongQuest':
                return MagicMock()
            elif model.__name__ == 'Workspace':
                return mock_workspace
            return None
        
        mock_db_get.get.side_effect = side_effect
        
        WorkspacesService.save_long_form_and_imagery_definition(
            self.workspace_id, JsonDataUtils.get_long_form_quest_json_string(),
            JsonDataUtils.get_imagery_json_string(), self.project_group_ids
        )
        
        self.assertTrue(True)
        self.assertEqual(mock_db_get.add.call_count, 0)
        self.assertEqual(mock_db_get.commit.call_count, 1)
        
        
if __name__ == "__main__":
    unittest.main()
