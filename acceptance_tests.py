import unittest
from unittest.mock import patch, MagicMock
import responses
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, get_projects_from_jira

class TestTimeTrackerAcceptance(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        self.app_context.pop()
    
    @responses.activate
    def test_criterion_1_dashboard_loads(self):
        # Mock the Jira API call
        responses.add(
            responses.GET,
            'https://test.atlassian.net/rest/api/3/project',
            json=[{
                "id": "10000",
                "key": "PROJ",
                "name": "Test Project"
            }],
            status=200
        )
        
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
    @responses.activate
    def test_criterion_2_manual_entry_and_persistence(self):
        # Test manual entry and persistence
        with patch('app.save_time_entry') as mock_save:
            response = self.app.post('/api/time_entries', json={
                'project_name': 'Test Project',
                'description': 'Testing entry'
            })
            self.assertEqual(response.status_code, 200)
            mock_save.assert_called_once()
            
    @responses.activate
    def test_criterion_3_settings_screen_stores_credentials(self):
        # Test that settings are stored in environment
        with patch.dict(os.environ, {}, clear=True):  # Clear env for clean test
            response = self.app.post('/settings', data={
                'jira_base_url': 'https://test.atlassian.net',
                'jira_username': 'user@example.com',
                'jira_api_key': 'test-api-key'
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(os.environ.get('JIRA_BASE_URL'), 'https://test.atlassian.net')
            
    @responses.activate
    def test_criterion_4_fetches_projects_from_jira(self):
        # Mock the Jira API call
        responses.add(
            responses.GET,
            'https://test.atlassian.net/rest/api/3/project',
            json=[{
                "id": "10000",
                "key": "PROJ",
                "name": "Test Project"
            }],
            status=200
        )
        
        projects = get_projects_from_jira()
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0]['name'], 'Test Project')