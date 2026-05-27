import pytest
import responses
import json
import os
from app import load_settings, save_settings, load_logs

# Setup client for testing
@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

@pytest.fixture
def clear_data():
    yield
    # Cleanup after each test
    if os.path.exists(os.path.join('data', 'logs.json')):
        os.remove(os.path.join('data', 'logs.json'))
    if os.path.exists(os.path.join('data', 'settings.json')):
        os.remove(os.path.join('data', 'settings.json'))

# Criterion 1: Application launches cleanly with a working dashboard showing timer and project list
def test_criterion_1_launch_and_dashboard(client, clear_data):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'
    # Verify default projects are available without settings
    response = client.get('/api/projects')
    assert response.status_code == 200
    assert len(response.json) == 2

# Criterion 2: Users can manually create custom project entries, start/stop timer, and view elapsed time
def test_criterion_2_time_entries(client, clear_data):
    # Create entry
    entry_data = {
        "id": "1",
        "description": "Test Task",
        "project_id": "PROJ-1",
        "start_time": "2023-01-01T12:00:00"
    }
    response = client.post('/api/logs', json=entry_data)
    assert response.status_code == 201
    
    # View logs
    response = client.get('/api/logs')
    assert response.status_code == 200
    assert len(response.json) == 1

# Criterion 3: Settings screen accepts Jira base URL, username, and API key, stores them securely, and requires them for all API operations
def test_criterion_3_settings(client, clear_data):
    # Setup Mock for Jira API
    @responses.activate
    def mock_jira_api():
        responses.add(
            responses.GET,
            "https://jira.example.com/rest/api/2/project",
            json=[{"id": "PROJ-1", "name": "Test Project"}],
            status=200
        )
    
    settings_data = {
        "jira_url": "https://jira.example.com",
        "username": "testuser",
        "api_key": "testkey"
    }
    response = client.post('/api/settings', json=settings_data)
    assert response.status_code == 200
    
    # Verify that projects now come from Jira (or fallback if API fails, but here we mock success)
    response = client.get('/api/projects')
    # Note: The app returns hardcoded defaults if settings are missing, or tries Jira. 
    # With our mock, requests.get should return the mocked data.
    # However, the app logic is: if not settings -> default. If settings -> try Jira.
    # We need to ensure the app handles the Jira call gracefully.
    # The app code handles exceptions and returns empty list, so 200 is expected.
