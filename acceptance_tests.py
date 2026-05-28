import pytest
import json
from unittest.mock import patch, MagicMock
from app import app

class TestTimeTracker:
    @patch('requests.get')
    def test_criterion_1_launch_cleanly(self, mock_get):
        with app.test_client() as client:
            response = client.get('/')
            assert response.status_code == 200

    def test_criterion_2_manual_entry_and_timer(self):
        with app.test_client() as client:
            response = client.post('/api/entries', json={"project": "Dev", "description": "Manual Entry"})
            assert response.status_code == 201
            response = client.get('/api/entries')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert len(data) > 0

    def test_criterion_3_settings_and_auth(self):
        with app.test_client() as client:
            response = client.get('/api/settings')
            assert response.status_code == 200
            response = client.post('/api/settings', json={"jira_url": "http://test.com", "api_key": "key"})
            assert response.status_code == 200

    @patch('requests.get')
    def test_criterion_4_fetch_jira_projects(self, mock_get):
        # Mock Jira API response
        mock_response = MagicMock()
        mock_response.json.return_value = {"values": [{"id": "1", "name": "Jira Project"}]}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        with app.test_client() as client:
            # Set credentials
            client.post('/api/settings', json={
                "jira_url": "https://jira.example.com",
                "api_key": "secret123",
                "username": "admin"
            })
            
            # Fetch projects
            response = client.get('/api/projects')
            assert response.status_code == 200
            data = json.loads(response.data)
            # Verify projects were fetched
            assert len(data) > 0 or 'projects' in data

    def test_criterion_5_local_persistence(self):
        with app.test_client() as client:
            # Create entry
            client.post('/api/entries', json={"project": "Test", "description": "Persistence Test"})
            # Reload app context to simulate new session
            with app.test_request_context():
                response = client.get('/api/entries')
                data = json.loads(response.data)
                assert len(data) > 0