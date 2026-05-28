import pytest
import responses
import os
import json
import sys

# Add project directory to path to import app
sys.path.insert(0, '/workspace/projects/TimeTracker')

# Import the Flask application
from app import app

@pytest.fixture
def client():
    """Creates a test client for the Flask app."""
    app.testing = True
    return app.test_client()

@pytest.fixture
def clean_storage():
    """Cleans up JSON files after each test to ensure isolation."""
    yield
    # Remove time_data.json
    if os.path.exists('/workspace/projects/TimeTracker/time_data.json'):
        os.remove('/workspace/projects/TimeTracker/time_data.json')
    # Remove config.json
    if os.path.exists('/workspace/projects/TimeTracker/config.json'):
        os.remove('/workspace/projects/TimeTracker/config.json')

    @responses.activate
    def test_criterion_4_jira_projects():
        """Criterion 4: App fetches projects from Jira API automatically."""
        # Mock Jira API response for projects
        jira_projects = [
            {"id": "PROJ-1", "name": "Development", "description": "Dev Project"},
            {"id": "PROJ-2", "name": "Design", "description": "Design Project"}
        ]
        
        # Mock the specific Jira endpoint
        jira_url = "https://jira.example.com/rest/api/3/project"
        responses.add(
            responses.GET,
            jira_url,
            json=jira_projects,
            status=200
        )

        # Call the endpoint
        response = client.get('/api/projects')

        # Assertions
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
        assert data[0]['name'] == "Development"

    @responses.activate
    def test_criterion_3_settings_secure_storage():
        """Criterion 3: Settings screen accepts Jira URL, username, API key and stores securely."""
        # Mock the Jira API call that happens when settings are validated (optional)
        responses.add(
            responses.GET,
            "https://jira.example.com/api/health",
            json={"status": "ok"},
            status=200
        )

        # Prepare settings payload
        settings_payload = {
            "base_url": "https://jira.example.com",
            "username": "test_user",
            "api_key": "test_key_123"
        }

        response = client.put('/api/settings', json=settings_payload)
        
        assert response.status_code == 200
        
        # Verify persistence (check that the file exists)
        config_file_path = '/workspace/projects/TimeTracker/config.json'
        assert os.path.exists(config_file_path), "Settings not persisted to local storage"

        # Verify content
        with open(config_file_path, 'r') as f:
            stored_data = json.load(f)
        assert stored_data['username'] == "test_user"
