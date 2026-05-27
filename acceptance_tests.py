import pytest
from unittest.mock import patch, mock_open
import json
from app import app, Project, Timer, Settings

class MockResponse:
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

# Test criterion 1: Application launches cleanly with working dashboard
def test_criterion_1_dashboard_access():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'TimeTracker Dashboard'

# Test criterion 2: Users can create projects, start/stop timer, and view elapsed time
def test_criterion_2_project_timer_operations():
    with app.test_client() as client:
        # Create a project
        response = client.post('/projects', json={'name': 'Test Project'})
        assert response.status_code == 201
        project_data = json.loads(response.data)
        assert project_data['name'] == 'Test Project'
        
        project_id = project_data['id']
        
        # Start timer for project
        response = client.post(f'/projects/{project_id}/start')
        assert response.status_code == 200
        
        # Stop timer for project
        response = client.post(f'/projects/{project_id}/stop')
        assert response.status_code == 200
        
        # Get timer data
        response = client.get(f'/projects/{project_id}/timer')
        assert response.status_code == 200
        timer_data = json.loads(response.data)
        assert 'elapsed_time' in timer_data

# Test criterion 3: Settings screen accepts Jira credentials
def test_criterion_3_jira_settings():
    with app.test_client() as client:
        # Set Jira settings
        response = client.post('/settings', json={
            'jira_base_url': 'https://example.atlassian.net',
            'jira_username': 'test@example.com',
            'jira_api_key': 'test-api-key'
        })
        assert response.status_code == 200
        
        # Verify settings are stored
        response = client.get('/settings')
        assert response.status_code == 200
        settings_data = json.loads(response.data)
        assert settings_data['jira_base_url'] == 'https://example.atlassian.net'
        assert settings_data['jira_username'] == 'test@example.com'
        assert settings_data['jira_api_key'] == 'test-api-key'