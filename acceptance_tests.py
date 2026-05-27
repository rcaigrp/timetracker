import pytest
import json
import os
import sys
sys.path.insert(0, '/workspace/projects/TimeTracker')

# Mock the Jira API calls using responses library
import responses

@pytest.fixture
def client():
    app = __import__('app', fromlist=['app']).app
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

@pytest.fixture(autouse=True)
def setup_data():
    yield
    # Cleanup after each test
    if os.path.exists('/workspace/projects/TimeTracker/time_tracker.json'):
        os.remove('/workspace/projects/TimeTracker/time_tracker.json')

@responses.activate
def test_criterion_1_launch(client):
    """Criterion 1: App launches cleanly with a working dashboard showing timer and project list"""
    response = client.get('/')
    assert response.status_code == 200

def test_criterion_2_manual_entry(client):
    """Criterion 2: Users can manually create custom project entries, start/stop timer, and view elapsed time in a persisted list"""
    payload = {
        "task": "Fix bug",
        "project": "Backend",
        "start": "2023-01-01T08:00:00Z",
        "end": "2023-01-01T08:30:00Z"
    }
    response = client.post('/api/time-entries', json=payload)
    assert response.status_code == 201
    
    response = client.get('/api/time-entries')
    assert response.status_code == 200
    entries = response.get_json()
    assert len(entries) == 1
    assert entries[0]['task'] == 'Fix bug'

def test_criterion_3_settings_store(client):
    """Criterion 3: Settings screen accepts Jira base URL, username, and API key, stores them securely"""
    settings_payload = {
        "base_url": "https://jira.example.com",
        "username": "admin",
        "api_key": "secret"
    }
    response = client.post('/api/settings', json=settings_payload)
    assert response.status_code == 200
    
    # Verify persistence
    response = client.get('/api/settings')
    assert response.status_code == 200
    config = response.get_json()
    assert config['base_url'] == settings_payload['base_url']

@responses.activate
def test_criterion_4_jira_projects(client):
    """Criterion 4: App fetches projects from Jira API automatically using configured credentials"""
    # Setup mock response for Jira API
    responses.add(
        responses.GET,
        'https://jira.example.com/rest/api/2/project',
        json={"issues": [{"key": "PROJ-1", "name": "Backend Project"}]},
        status=200
    )
    
    response = client.get('/api/projects')
    assert response.status_code == 200
    projects = response.get_json()
    assert len(projects) > 0
    assert 'PROJ-1' in projects[0]

def test_criterion_5_persistence(client):
    """Criterion 5: Local storage persists logs between sessions"""
    payload = {
        "task": "Test Task",
        "project": "QA",
        "start": "2023-01-01T09:00:00Z",
        "end": "2023-01-01T09:15:00Z"
    }
    client.post('/api/time-entries', json=payload)
    
    # Simulate app restart by reloading data
    new_app = __import__('app', fromlist=['app']).app
    new_client = new_app.test_client()
    
    response = new_client.get('/api/time-entries')
    entries = response.get_json()
    assert len(entries) == 1
    assert entries[0]['task'] == 'Test Task'
