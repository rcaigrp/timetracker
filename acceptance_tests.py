import pytest
import responses
import sys
import os
import json

sys.path.insert(0, '/workspace/projects/TimeTracker')
from app import app, load_config, save_config

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

class TestAcceptanceCriteria:
    
    def test_criterion_1_launch(self, client):
        """App launches cleanly with a working dashboard."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Dashboard' in response.data
    
    @responses.activate
    def test_criterion_4_jira_api(self, client):
        """App fetches projects from Jira API."""
        # Mock Jira API response
        responses.add(
            responses.GET,
            'http://jira.example.com/rest/api/2/project',
            json=[{"name": "Proj1", "id": "1"}],
            status=200
        )
        
        # Set config
        config = {"url": "http://jira.example.com", "api_key": "test_key"}
        save_config(config)
        
        response = client.get('/api/jira/projects')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
    
    def test_criterion_3_settings_store(self, client):
        """Settings screen accepts Jira base URL and stores it."""
        config_data = {
            "url": "https://example.atlassian.net",
            "username": "user@company.com",
            "api_key": "abc123"
        }
        response = client.post('/api/settings', json=config_data)
        assert response.status_code == 201
        
        # Verify persistence
        response = client.get('/api/settings')
        loaded = json.loads(response.data)
        assert loaded['url'] == config_data['url']
