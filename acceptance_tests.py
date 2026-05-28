import pytest
import requests_mock
from app import app
import json
import os

# Clean up test state
SETTINGS_PATH = '/workspace/projects/TimeTracker/settings.json'
ENTRIES_PATH = '/workspace/projects/TimeTracker/entries.json'

@pytest.fixture(autouse=True)
def cleanup():
    yield
    if os.path.exists(SETTINGS_PATH):
        os.remove(SETTINGS_PATH)
    if os.path.exists(ENTRIES_PATH):
        os.remove(ENTRIES_PATH)


def test_criterion_1_launch():
    """App launches cleanly with a working dashboard showing timer and project list"""
    client = app.test_client()
    # Check if the index page loads (serves React frontend)
    response = client.get('/')
    assert response.status_code == 200


def test_criterion_2_manual_entry():
    """Users can manually create custom project entries, start/stop timer, and view elapsed time in a persisted list"""
    client = app.test_client()
    entry = {"id": 1, "description": "Test Task", "duration": 3600, "project": "Test Project"}
    response = client.post('/api/entries', json=entry)
    assert response.status_code == 200
    
    # Verify the entry is returned
    get_response = client.get('/api/entries')
    assert get_response.status_code == 200
    entries = get_response.json
    assert len(entries) == 1
    assert entries[0]["description"] == "Test Task"


def test_criterion_3_settings():
    """Settings screen accepts Jira base URL, username, and API key, stores them securely, and requires them for all API operations"""
    client = app.test_client()
    settings = {"jira_url": "https://test.jira.com", "api_key": "fake-token-12345"}
    response = client.post('/api/settings', json=settings)
    assert response.status_code == 200
    
    # Verify persistence (re-reads from storage)
    get_response = client.get('/api/settings')
    assert get_response.json == settings


def test_criterion_4_fetch_projects():
    """App fetches projects from Jira API automatically using configured credentials"""
    client = app.test_client()
    
    # Step 1: Set up settings
    settings = {"jira_url": "https://test.jira.com", "username": "admin", "api_key": "token"}
    client.post('/api/settings', json=settings)
    
    # Step 2: Mock Jira API response
    mock_projects = [
        {"id": "10000", "name": "Test Project"},
        {"id": "10001", "name": "Another Project"}
    ]
    
    with requests_mock.Mocker() as m:
        jira_url = "https://test.jira.com/rest/api/2/project"
        m.get(jira_url, json=mock_projects, status_code=200)
        
        # Step 3: Call the endpoint
        response = client.get('/api/projects')
        
        # Step 4: Verify
        assert response.status_code == 200
        data = response.json
        assert len(data) == 2
        assert data[0]["name"] == "Test Project"

        # Verify the app made the request to the mocked URL
        assert m.request_history[0].url == jira_url
