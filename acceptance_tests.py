import pytest
import responses
import os
import sys
import json

# Ensure we are in the project directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

class TestAC1Dashboard:
    def test_app_launches(self, client):
        result = client.get('/api/config')
        assert result.status_code == 200
        json_result = result.get_json()
        assert json_result == {"logs": [], "settings": {}}

class TestAC3Settings:
    @responses.activate
    def test_save_jira_settings(self, client):
        # Mock Jira API call after settings are saved
        responses.add(
            responses.GET,
            'http://jira.example.com/rest/api/2/project',
            json=[{"id": "PROJ-1", "name": "Test Project", "key": "TEST"}],
            status=200
        )
        response = client.post('/api/config', json={
            "url": "http://jira.example.com",
            "username": "user@example.com",
            "api_key": "secret_token"
        })
        assert response.status_code == 200
        assert response.json['success'] == True
        # Verify the settings were saved
        get_resp = client.get('/api/config')
        assert get_resp.json['jira_url'] == "http://jira.example.com"
        # Verify the API was called
        assert len(responses.calls) == 1

class TestAC4JiraProjects:
    @responses.activate
    def test_fetch_jira_projects(self, client):
        responses.add(
            responses.GET,
            'http://jira.example.com/rest/api/2/project',
            json=[{"id": "PROJ-1", "name": "Test Project", "key": "TEST"}],
            status=200
        )
        response = client.get('/api/jira/projects')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['name'] == 'Test Project'

class TestAC5Persistence:
    def test_logs_persist(self, client):
        # Start a timer
        client.post('/api/timer', json={"action": "start", "project": "Proj A", "timestamp": 1000})
        # Stop it
        client.post('/api/timer', json={"action": "stop", "timestamp": 2000})
        
        # Check persistence
        logs = client.get('/api/timer').json
        assert len(logs) == 1
        assert logs[0]['status'] == 'stopped'
        assert logs[0]['project'] == 'Proj A'
