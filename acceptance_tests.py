import pytest
import responses
from app import app, CONFIG
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.fixture
def api_client():
    return client

@responses.activate
def test_criterion_1_launch_cleanly():
    resp = responses.get(
        'http://localhost:5000/api/settings',
        json={"JIRA_BASE_URL": ""},
        status=200
    )
    response = client.get('/api/settings')
    assert response.status_code == 200

@responses.activate
def test_criterion_2_manual_entry_and_timer():
    # Mock the start endpoint
    responses.post(
        'http://localhost:5000/api/timer/start',
        json={'running': True, 'log': {'start': '2023-01-01T00:00:00', 'end': '2023-01-01T00:01:00', 'duration': 60.0, 'project': 'DEV'}},
        status=200
    )
    response = client.get('/api/timer')
    assert response.status_code == 200
    assert response.json['running'] == True
    
    response = client.post('/api/timer/start')
    assert response.status_code == 200
    assert response.json['running'] == True

def test_criterion_3_settings_storage():
    data = {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_API_KEY': '12345',
        'JIRA_USERNAME': 'test@test.com'
    }
    response = client.post('/api/settings', json=data)
    assert response.status_code == 200
    assert response.json['config']['JIRA_BASE_URL'] == 'https://test.atlassian.net'

@responses.activate
def test_criterion_4_jira_projects():
    # Mock the external Jira call
    responses.add(
        responses.GET, 
        'https://test.atlassian.net/rest/api/3/project',
        json=[{"id": "PROJ1", "name": "Dev", "key": "DEV"}],
        status=200
    )
    # Override config for this test
    original_url = CONFIG.get('JIRA_BASE_URL')
    CONFIG['JIRA_BASE_URL'] = 'https://test.atlassian.net'
    
    response = client.get('/api/projects')
    assert response.status_code == 200
    assert response.json[0]['id'] == 'PROJ1'
