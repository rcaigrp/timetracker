import pytest
import responses
import json
from app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

@responses.activate
def test_timer_start(client):
    response = client.post('/timer/start', json={"project": "TEST-123"})
    assert response.status_code == 200
    data = response.get_json()
    assert data['active'] == True
    assert 'start_time' in data

@responses.activate
def test_timer_stop(client):
    # Mock the start endpoint first
    client.post('/timer/start', json={"project": "TEST-123"})
    response = client.post('/timer/stop')
    assert response.status_code == 200
    data = response.get_json()
    assert data['active'] == False
    assert 'end_time' in data

@responses.activate
def test_settings_save(client):
    response = client.post('/settings', json={'jira_url': 'http://mock-jira.com', 'api_key': 'mock_key'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'saved'

@responses.activate
def test_jira_projects_fetch(client):
    # Setup settings with the mocked URL
    client.post('/settings', json={'jira_url': 'http://mock-jira.com', 'api_key': 'mock_key'})
    
    # Mock the Jira API response
    responses.add(
        responses.GET,
        'http://mock-jira.com/rest/api/3/search',
        json={'issues': [{'key': 'PROJ-1', 'fields': {'name': 'Project 1'}}]},
        status=200
    )
    
    response = client.get('/jira/projects')
    assert response.status_code == 200
    assert response.json()['issues'][0]['key'] == 'PROJ-1'
